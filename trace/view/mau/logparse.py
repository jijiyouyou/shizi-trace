"""日志 / 粘贴文本切段：识别 mau_trace.cli 风格 ---- name start/end ---- 块。"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from decode import (
    STAT_SEGMENTS,
    TRACE_SEGMENTS,
    DecodeError,
    EPP_MAUS,
    IPP_MAUS,
    decode_mpl,
    decode_segment,
    decode_statistics_section,
    load_layouts,
    mau_direction,
    parse_u32_tokens,
    segment_category,
)

BLOCK_RE = re.compile(
    r"----\s*(?P<name>.+?)\s+(?P<kind>start|end)\s*----",
    re.IGNORECASE,
)

MAU_NAME_RE = re.compile(r"^mau(\d+)$", re.IGNORECASE)
VME_NAME_RE = re.compile(r"^vme(\d+)(?:_trace)?$", re.IGNORECASE)
MPL_NAME_RE = re.compile(r"^mpl(?:_trace|_req|_dump)?$", re.IGNORECASE)
IPARSER_NAME_RE = re.compile(r"^iparser(?:_trace)?$", re.IGNORECASE)
EPARSER_PEDT_BLOCK_RE = re.compile(
    r"^(?:eparser|pedt)(?:_trace)?(?:\s|$)",
    re.IGNORECASE,
)
STAT_NAME_RE = re.compile(r"^(?:mau_)?stat(?:istics)?(?:_trace)?$", re.IGNORECASE)

_IPARSER_DECODE = None
_EPARSER_DECODE = None


def _iparser_decode():
    """惰性加载 view/iparser/decode.py（避免与 mau/decode 同名冲突）。"""
    global _IPARSER_DECODE
    if _IPARSER_DECODE is not None:
        return _IPARSER_DECODE
    path = Path(__file__).resolve().parents[1] / "iparser" / "decode.py"
    spec = importlib.util.spec_from_file_location("trace_view_iparser_decode", path)
    if spec is None or spec.loader is None:
        raise DecodeError(f"无法加载 iparser 解码: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    _IPARSER_DECODE = mod
    return mod


def _eparser_decode():
    """惰性加载 view/eparser/decode.py（eparser + pedt）。"""
    global _EPARSER_DECODE
    if _EPARSER_DECODE is not None:
        return _EPARSER_DECODE
    path = Path(__file__).resolve().parents[1] / "eparser" / "decode.py"
    spec = importlib.util.spec_from_file_location("trace_view_eparser_decode", path)
    if spec is None or spec.loader is None:
        raise DecodeError(f"无法加载 eparser 解码: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    _EPARSER_DECODE = mod
    return mod


def _normalize_seg(name: str) -> str:
    n = name.strip().lower()
    if n.endswith("_trace"):
        base = n[: -len("_trace")]
    else:
        base = n
    if base in STAT_SEGMENTS or n in STAT_SEGMENTS:
        return base if base in STAT_SEGMENTS else n
    if base in ("llr", "lrr"):
        return "lrr"
    if base in ("cls", "keygen", "egr", "lrr"):
        return base
    m = VME_NAME_RE.match(n)
    if m:
        return f"vme{m.group(1)}"
    if base.startswith("vme") and base[3:].isdigit():
        return base
    if STAT_NAME_RE.match(n) or STAT_NAME_RE.match(base):
        return "statistics"
    return n


def extract_blocks(text: str) -> list[dict[str, Any]]:
    """切出命名块，含 start/end 字符区间，便于子段归属 mau。"""
    matches = list(BLOCK_RE.finditer(text))
    if not matches:
        return [{"name": "raw", "text": text, "kind": "raw", "start": 0, "end": len(text)}]

    stack: list[tuple[str, int, int]] = []
    blocks: list[dict[str, Any]] = []
    for m in matches:
        name = m.group("name")
        kind = m.group("kind").lower()
        if kind == "start":
            stack.append((name, m.end(), m.start()))
        else:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0].lower() == name.lower():
                    sname, content_start, _ = stack.pop(i)
                    blocks.append(
                        {
                            "name": sname,
                            "text": text[content_start : m.start()],
                            "kind": "block",
                            "start": content_start,
                            "end": m.start(),
                        }
                    )
                    break
    return blocks


def _owning_mau(seg_start: int, mau_spans: list[tuple[int, int, int]]) -> int | None:
    for mau_idx, a, b in mau_spans:
        if a <= seg_start < b:
            return mau_idx
    return None


def _empty_mau_node(mau_idx: int, direction: str) -> dict[str, Any]:
    return {
        "mau": mau_idx,
        "direction": direction,
        "categories": {
            "trace": {},
            "statistics": {},
        },
        "segments": {},
    }


def parse_log(text: str, layouts: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    解析整份日志：
      modules.mau[ipp|epp][mauN].categories.trace|statistics
      modules.mpl  ← 独立 mpl 块（不是 keygen）
    """
    layouts = layouts or load_layouts()
    blocks = extract_blocks(text)
    errors: list[str] = []

    mau_spans: list[tuple[int, int, int]] = []
    for blk in blocks:
        m = MAU_NAME_RE.match(blk["name"])
        if m and blk.get("kind") == "block":
            mau_spans.append((int(m.group(1)), blk["start"], blk["end"]))

    mau_data: dict[int, dict[str, Any]] = {
        idx: {"trace": {}, "statistics": {}} for idx, _, _ in mau_spans
    }
    mpl_raw: list[dict[str, Any]] = []
    iparser_raw: list[dict[str, Any]] = []
    orphan_segments: list[dict[str, Any]] = []

    for blk in blocks:
        name = blk["name"]
        body = blk["text"]
        if MAU_NAME_RE.match(name):
            continue

        # 独立 mpl 模块块
        if MPL_NAME_RE.match(name):
            try:
                words = parse_u32_tokens(body)
                mpl_raw.append({"label": name, "words": words})
            except DecodeError as e:
                errors.append(f"mpl: {e}")
            continue

        # 独立 iparser 模块块（调用 view/iparser 解码）
        if IPARSER_NAME_RE.match(name):
            try:
                words = parse_u32_tokens(body)
                iparser_raw.append({"label": name, "words": words})
            except DecodeError as e:
                errors.append(f"iparser: {e}")
            continue

        # eparser / pedt 子块与整段由 collect_module_words 统一处理
        if EPARSER_PEDT_BLOCK_RE.match(name):
            continue

        # 外层 statistics 包裹块：子段已单独切出，跳过
        if name.lower() in ("statistics", "mau_statistics"):
            continue

        seg = _normalize_seg(name)
        if seg == "raw" or name.lower() == "raw":
            try:
                words = parse_u32_tokens(body)
                orphan_segments.append({"name": "raw", "words": words})
            except DecodeError as e:
                errors.append(str(e))
            continue

        is_trace_seg = seg in TRACE_SEGMENTS or bool(re.fullmatch(r"vme\d", seg))
        is_stat = seg in STAT_SEGMENTS

        if is_trace_seg or is_stat:
            try:
                words = parse_u32_tokens(body) if body.strip() else []
            except DecodeError as e:
                if is_stat and not body.strip():
                    words = []
                else:
                    errors.append(f"{name}: {e}")
                    continue
            owner = _owning_mau(blk.get("start", 0), mau_spans)
            meta = {
                "label": name,
                "words": words,
                "word_count": len(words),
                "category": "statistics" if is_stat else "trace",
            }
            bucket = "statistics" if is_stat else "trace"
            key_name = seg
            if owner is None:
                orphan_segments.append({"name": key_name, **meta})
            else:
                mau_data.setdefault(owner, {"trace": {}, "statistics": {}})
                mau_data[owner][bucket][key_name] = meta
            continue

    if not mau_data and not orphan_segments and not mpl_raw and not iparser_raw:
        try:
            words = parse_u32_tokens(text)
            orphan_segments.append({"name": "raw", "words": words})
        except DecodeError as e:
            errors.append(str(e))

    ipp: dict[str, Any] = {}
    epp: dict[str, Any] = {}

    for mau_idx, info in sorted(mau_data.items()):
        try:
            direction = mau_direction(mau_idx)
        except DecodeError as e:
            errors.append(str(e))
            continue
        node = _empty_mau_node(mau_idx, direction)

        for seg, meta in info.get("trace", {}).items():
            words = meta["words"]
            try:
                entry = {
                    **meta,
                    "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
                    "decoded": decode_segment(seg, words, layouts),
                }
            except DecodeError as e:
                errors.append(f"mau{mau_idx}.{seg}: {e}")
                entry = {**meta, "error": str(e)}
            node["categories"]["trace"][seg] = entry
            node["segments"][seg] = entry

        for seg, meta in info.get("statistics", {}).items():
            words = meta.get("words") or []
            try:
                entry = {
                    **meta,
                    "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
                    "decoded": decode_statistics_section(seg, words, layouts)
                    if words
                    else {
                        "kind": "statistics",
                        "section": seg,
                        "title": seg,
                        "registers": [],
                        "fields": [],
                        "errors": ["空输入"],
                    },
                }
            except DecodeError as e:
                errors.append(f"mau{mau_idx}.{seg}: {e}")
                entry = {**meta, "error": str(e)}
            node["categories"]["statistics"][seg] = entry
            node["segments"][f"stat:{seg}"] = entry

        key = f"mau{mau_idx}"
        (ipp if direction == "ipp" else epp)[key] = node

    mpl_list: list[dict[str, Any]] = []
    for i, raw in enumerate(mpl_raw):
        try:
            mpl_list.append(
                {
                    "source": raw.get("label") or f"mpl#{i}",
                    "decoded": decode_mpl(raw["words"], layouts),
                    "word_count": len(raw["words"]),
                }
            )
        except DecodeError as e:
            errors.append(f"mpl[{i}]: {e}")

    iparser_list: list[dict[str, Any]] = []
    if iparser_raw:
        try:
            ip_dec = _iparser_decode()
            ip_layouts = ip_dec.load_layouts()
            for i, raw in enumerate(iparser_raw):
                try:
                    decoded = ip_dec.decode_segment(
                        "iparser_trace", raw["words"], ip_layouts
                    )
                    iparser_list.append(
                        {
                            "source": raw.get("label") or f"iparser#{i}",
                            "decoded": decoded,
                            "word_count": len(raw["words"]),
                            "words_hex": [
                                f"0x{w & 0xFFFFFFFF:08x}" for w in raw["words"]
                            ],
                        }
                    )
                except Exception as e:  # noqa: BLE001
                    errors.append(f"iparser[{i}]: {e}")
        except Exception as e:  # noqa: BLE001
            errors.append(f"iparser: {e}")

    eparser_list: list[dict[str, Any]] = []
    pedt_list: list[dict[str, Any]] = []
    try:
        ep_dec = _eparser_decode()
        ep_layouts = ep_dec.load_layouts()
        for mod, layout_key, dest in (
            ("eparser", "eparser_trace", eparser_list),
            ("pedt", "pedt_trace", pedt_list),
        ):
            for i, raw in enumerate(ep_dec.collect_module_words(text, mod)):
                try:
                    decoded = ep_dec.decode_segment(
                        layout_key, raw["words"], ep_layouts
                    )
                    dest.append(
                        {
                            "source": raw.get("label") or f"{mod}#{i}",
                            "decoded": decoded,
                            "word_count": len(raw["words"]),
                            "words_hex": [
                                f"0x{w & 0xFFFFFFFF:08x}" for w in raw["words"]
                            ],
                        }
                    )
                except Exception as e:  # noqa: BLE001
                    errors.append(f"{mod}[{i}]: {e}")
    except Exception as e:  # noqa: BLE001
        errors.append(f"eparser/pedt: {e}")

    orphans_out = []
    for o in orphan_segments:
        words = o["words"]
        entry: dict[str, Any] = {
            "name": o["name"],
            "word_count": len(words),
            "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
            "category": o.get("category") or segment_category(o["name"]),
        }
        if o["name"] in STAT_SEGMENTS:
            try:
                entry["decoded"] = decode_statistics_section(o["name"], words, layouts)
            except DecodeError as e:
                entry["error"] = str(e)
                errors.append(str(e))
        elif o["name"] not in ("raw", "statistics") and not str(o["name"]).startswith("stat"):
            try:
                entry["decoded"] = decode_segment(o["name"], words, layouts)
            except DecodeError as e:
                entry["error"] = str(e)
                errors.append(str(e))
        orphans_out.append(entry)

    return {
        "modules": {
            "mpl": mpl_list,
            "mau": {
                "ipp": ipp,
                "epp": epp,
                "expected_ipp": [f"mau{i}" for i in IPP_MAUS],
                "expected_epp": [f"mau{i}" for i in EPP_MAUS],
            },
            "iparser": iparser_list,
            "eparser": eparser_list,
            "pedt": pedt_list,
        },
        "orphans": orphans_out,
        "errors": errors,
    }


def parse_file(path: Path | str, layouts: dict[str, Any] | None = None) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    out = parse_log(text, layouts)
    out["source"] = str(path)
    return out


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="解析 mau_trace 日志")
    ap.add_argument("logfile")
    ap.add_argument("-o", "--output", help="写入 JSON")
    args = ap.parse_args()
    result = parse_file(args.logfile)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text)
