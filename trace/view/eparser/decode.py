"""Eparser / Pedt register dump 解码：按 eparser_pedt_fields.yaml 抽取字段。"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("需要 PyYAML：pip install pyyaml") from exc

HERE = Path(__file__).resolve().parent
TRACE_ROOT = HERE.parents[1]
DEFAULT_YAML = TRACE_ROOT / "eparser_pedt_fields.yaml"

# 允许名称含空格：---- eparser dbg_ctrl start ----
BLOCK_RE = re.compile(
    r"----\s*(?P<name>.+?)\s+(?P<kind>start|end)\s*----",
    re.IGNORECASE,
)

MODULE_ALIAS = {
    "eparser": "eparser_trace",
    "eparser_trace": "eparser_trace",
    "pedt": "pedt_trace",
    "pedt_trace": "pedt_trace",
}


class DecodeError(ValueError):
    """解码错误。"""


def format_value(val: int, width: int) -> dict[str, str]:
    hex_w = max(1, (width + 3) // 4)
    return {
        "dec": str(val),
        "hex": f"0x{val:0{hex_w}x}",
        "bin": f"0b{val:0{width}b}" if width <= 64 else f"0b…({width}bit)",
    }


def load_layouts(path: Path | str | None = None) -> dict[str, Any]:
    p = Path(path) if path else DEFAULT_YAML
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "traces" not in data:
        raise DecodeError(f"无效格式表: {p}")
    return data


def layouts_to_json(layouts: dict[str, Any]) -> str:
    return json.dumps(layouts, ensure_ascii=False, separators=(",", ":"))


def parse_u32_tokens(text: str) -> list[int]:
    if not text or not text.strip():
        raise DecodeError("空输入")
    cleaned = re.sub(
        r"(?m)(?:^|\s)(?:0x)?[0-9a-fA-F]{1,8}\s*:",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    tokens = re.findall(r"0x[0-9a-fA-F]+|\b[0-9a-fA-F]{8}\b|\b\d+\b", cleaned)
    if not tokens:
        raise DecodeError("未找到合法 hex/数值")
    out: list[int] = []
    for t in tokens:
        try:
            if t.lower().startswith("0x"):
                v = int(t, 16)
            elif len(t) == 8 and re.fullmatch(r"[0-9a-fA-F]{8}", t):
                v = int(t, 16)
            else:
                v = int(t, 10)
        except ValueError as e:
            raise DecodeError(f"非法数值: {t}") from e
        if v < 0 or v > 0xFFFFFFFF:
            raise DecodeError(f"超出 u32: {t}")
        out.append(v)
    return out


def extract_blocks(text: str) -> list[dict[str, Any]]:
    matches = list(BLOCK_RE.finditer(text))
    if not matches:
        return [{"name": "raw", "text": text, "kind": "raw", "start": 0, "end": len(text)}]
    stack: list[tuple[str, int]] = []
    blocks: list[dict[str, Any]] = []
    for m in matches:
        name = m.group("name")
        kind = m.group("kind").lower()
        if kind == "start":
            stack.append((name, m.end()))
        else:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0].lower() == name.lower():
                    sname, content_start = stack.pop(i)
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


def _norm_module(name: str) -> str | None:
    n = name.strip().lower()
    if n in MODULE_ALIAS:
        return MODULE_ALIAS[n]
    if n.startswith("eparser ") or n.startswith("eparser_"):
        return "eparser_trace"
    if n.startswith("pedt ") or n.startswith("pedt_"):
        return "pedt_trace"
    return None


def is_module_block_name(name: str, module: str) -> bool:
    """判断 ---- name ---- 是否属于 eparser / pedt（含子寄存器块）。"""
    want = MODULE_ALIAS.get(module.lower().strip(), module.lower().strip())
    got = _norm_module(name)
    return got == want


def extract_dump_regions(text: str, module: str) -> list[dict[str, Any]]:
    """
    抽取 ====== {module} register dump start/end ====== 区间。
    pedt 的 part N/M end 不作为结束（仅 dump end / dump end (3/3)）。
    """
    mod = module.lower().strip()
    if mod in ("eparser_trace",):
        mod = "eparser"
    if mod in ("pedt_trace",):
        mod = "pedt"
    start_re = re.compile(
        rf"======\s*{re.escape(mod)}\s+register\s+dump\s+start(?:\s*\([^)]*\))?\s*======",
        re.IGNORECASE,
    )
    end_re = re.compile(
        rf"======\s*{re.escape(mod)}\s+register\s+dump\s+end(?:\s*\([^)]*\))?\s*======",
        re.IGNORECASE,
    )
    starts = list(start_re.finditer(text))
    ends = list(end_re.finditer(text))
    regions: list[dict[str, Any]] = []
    ei = 0
    for si, sm in enumerate(starts):
        while ei < len(ends) and ends[ei].start() <= sm.start():
            ei += 1
        if ei >= len(ends):
            break
        em = ends[ei]
        regions.append(
            {
                "name": f"{mod}_dump#{si}",
                "text": text[sm.end() : em.start()],
                "kind": "dump",
                "start": sm.end(),
                "end": em.start(),
            }
        )
        ei += 1
    return regions


def collect_module_words(text: str, module: str) -> list[dict[str, Any]]:
    """
    从日志中收集 eparser / pedt 的 u32 序列。
    优先整段 dump（======），其次 ---- eparser/pedt start ----，
    再拼接子寄存器块 ---- eparser xxx ----。
    返回 [{label, words}, ...]
    """
    mod = module.lower().strip()
    if mod in MODULE_ALIAS:
        layout_key = MODULE_ALIAS[mod]
        prefix = "eparser" if layout_key == "eparser_trace" else "pedt"
    elif mod in ("eparser", "pedt"):
        prefix = mod
        layout_key = MODULE_ALIAS[mod]
    else:
        raise DecodeError(f"未知模块: {module}")

    out: list[dict[str, Any]] = []

    dumps = extract_dump_regions(text, prefix)
    if dumps:
        for d in dumps:
            try:
                words = parse_u32_tokens(d["text"])
            except DecodeError:
                continue
            if words:
                out.append({"label": d["name"], "words": words})
        if out:
            return out

    blocks = extract_blocks(text)
    whole: list[dict[str, Any]] = []
    child_words: list[int] = []
    child_labels: list[str] = []
    for blk in blocks:
        name = blk["name"]
        nl = name.lower().strip()
        if nl in (prefix, f"{prefix}_trace"):
            try:
                words = parse_u32_tokens(blk["text"])
            except DecodeError:
                continue
            if words:
                whole.append({"label": name, "words": words})
            continue
        if nl.startswith(prefix + " "):
            try:
                words = parse_u32_tokens(blk["text"])
            except DecodeError:
                continue
            if words:
                child_words.extend(words)
                child_labels.append(name)

    if whole:
        return whole
    if child_words:
        return [
            {
                "label": f"{prefix}_regs({len(child_labels)})",
                "words": child_words,
            }
        ]
    return []


def decode_trace(words: list[int], layout: dict[str, Any]) -> dict[str, Any]:
    need = int(layout.get("word_count", 0))
    if need and len(words) < need:
        raise DecodeError(f"长度不足：需要 {need} 个 u32，实际 {len(words)}")
    words = words[:need] if need else words[:]

    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for fd in layout.get("fields") or []:
        domain = int(fd["domain"])
        hi, lo = int(fd["bits"][0]), int(fd["bits"][1])
        width = int(fd.get("width", hi - lo + 1))
        name = str(fd.get("name", ""))
        desc = str(fd.get("desc", ""))
        if domain < 0 or domain >= len(words):
            errors.append(f"D{domain} 越界（共 {len(words)} word）：{name}")
            continue
        word = words[domain]
        if hi < lo or lo < 0 or hi > 31:
            errors.append(f"D{domain} {name}: 非法 bits [{hi}:{lo}]")
            continue
        bit_count = hi - lo + 1
        mask = (1 << bit_count) - 1
        value = (int(word) >> lo) & mask
        rows.append(
            {
                "domain": domain,
                "name": name,
                "bits": f"[{hi}:{lo}]",
                "hi": hi,
                "lo": lo,
                "width": width,
                "word_hex": f"0x{int(word) & 0xFFFFFFFF:08x}",
                "value": value,
                "value_hex": format_value(value, width)["hex"],
                "value_dec": format_value(value, width)["dec"],
                "value_bin": format_value(value, width)["bin"],
                "desc": desc,
                "reserved": name.lower() in ("rsv", "reserved")
                or "保留" in desc
                or name.lower().endswith("_rsv")
                or "reserved" in desc.lower(),
            }
        )
    return {
        "title": layout.get("title") or "register trace",
        "word_count": need,
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
        "fields": rows,
        "errors": errors,
    }


def decode_segment(segment: str, words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    seg = segment.lower().strip()
    norm = MODULE_ALIAS.get(seg, seg)
    traces = layouts.get("traces") or {}
    if norm not in traces:
        raise DecodeError(f"未知子段: {segment}")
    return decode_trace(words, traces[norm])


def decode_paste(
    text: str,
    module: str,
    layouts: dict[str, Any] | None = None,
    *,
    segment: str | None = None,
    mau: int | None = None,
) -> dict[str, Any]:
    del mau  # 与 iparser 接口兼容，未使用
    layouts = layouts or load_layouts()
    module = (module or "eparser").lower().strip()
    words = parse_u32_tokens(text)
    result: dict[str, Any] = {
        "module": module,
        "word_count": len(words),
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
    }
    if module not in MODULE_ALIAS and module not in ("eparser", "pedt"):
        raise DecodeError(f"未知模块: {module}")
    seg = segment or MODULE_ALIAS.get(module, module)
    if seg not in ("eparser_trace", "pedt_trace"):
        seg = MODULE_ALIAS.get(module, seg)
    result["segment"] = seg
    result["decoded"] = decode_segment(seg, words, layouts)
    result["category"] = "trace"
    return result


def parse_log(text: str, layouts: dict[str, Any] | None = None) -> dict[str, Any]:
    """解析日志中的 eparser / pedt dump，返回 modules 列表项。"""
    layouts = layouts or load_layouts()
    errors: list[str] = []

    def _build(mod: str, layout_key: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        layout = layouts["traces"][layout_key]
        collected = collect_module_words(text, mod)
        if not collected:
            return items
        for i, raw in enumerate(collected):
            try:
                decoded = decode_trace(raw["words"], layout)
            except DecodeError as e:
                errors.append(f"{mod}[{i}]: {e}")
                continue
            items.append(
                {
                    "source": raw.get("label") or f"{mod}#{i}",
                    "decoded": decoded,
                    "word_count": len(raw["words"]),
                    "words_hex": [
                        f"0x{w & 0xFFFFFFFF:08x}" for w in raw["words"]
                    ],
                }
            )
        return items

    eparser_list = _build("eparser", "eparser_trace")
    pedt_list = _build("pedt", "pedt_trace")

    if not eparser_list and not pedt_list:
        # 整段粘贴：按 word_count 猜测
        try:
            words = parse_u32_tokens(text)
            n = len(words)
            ep_need = int(layouts["traces"]["eparser_trace"].get("word_count") or 0)
            pd_need = int(layouts["traces"]["pedt_trace"].get("word_count") or 0)
            if ep_need and n >= ep_need and (not pd_need or abs(n - ep_need) <= abs(n - pd_need)):
                eparser_list = [
                    {
                        "source": "paste",
                        "decoded": decode_trace(words, layouts["traces"]["eparser_trace"]),
                        "word_count": n,
                        "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
                    }
                ]
            elif pd_need and n >= pd_need:
                pedt_list = [
                    {
                        "source": "paste",
                        "decoded": decode_trace(words, layouts["traces"]["pedt_trace"]),
                        "word_count": n,
                        "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
                    }
                ]
            else:
                errors.append(f"无法识别：u32 数={n}（eparser={ep_need}, pedt={pd_need}）")
        except DecodeError as e:
            errors.append(str(e))

    return {
        "module": "eparser_pedt",
        "eparser": eparser_list,
        "pedt": pedt_list,
        "errors": errors,
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="eparser / pedt dump 解码")
    ap.add_argument("textfile", nargs="?", help="含 dump 的文件；缺省读 stdin")
    ap.add_argument("-y", "--yaml", default=str(DEFAULT_YAML), help="yaml 路径")
    ap.add_argument(
        "-m",
        "--module",
        default="auto",
        choices=["auto", "eparser", "pedt"],
        help="模块；auto 同时尝试两者",
    )
    args = ap.parse_args()
    layouts = load_layouts(args.yaml)
    raw = (
        Path(args.textfile).read_text(encoding="utf-8", errors="replace")
        if args.textfile
        else __import__("sys").stdin.read()
    )
    if not raw.strip():
        print(json.dumps({"error": "未提供文本"}, ensure_ascii=False))
        raise SystemExit(1)
    if args.module == "auto":
        data = parse_log(raw, layouts)
    else:
        paste = decode_paste(raw, args.module, layouts)
        data = {
            "module": args.module,
            "eparser": [paste] if args.module == "eparser" else [],
            "pedt": [paste] if args.module == "pedt" else [],
            "errors": [],
        }
    print(json.dumps(data, ensure_ascii=False, indent=2))
