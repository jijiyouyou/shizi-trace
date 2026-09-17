"""Iparser trace 解码：按 iparser_trace.yaml 从 dump 中按寄存器逐项抽取。"""

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
DEFAULT_YAML = TRACE_ROOT / "iparser_trace.yaml"

BLOCK_RE = re.compile(
    r"----\s*(?P<name>[\w.]+)\s+(?P<kind>start|end)\s*----",
    re.IGNORECASE,
)
IPARSER_NAME_RE = re.compile(r"^iparser(?:_trace)?$", re.IGNORECASE)


class DecodeError(ValueError):
    """解码错误。"""


def format_value(val: int, width: int) -> dict[str, str]:
    hex_w = max(1, (width + 3) // 4)
    return {
        "dec": str(val),
        "hex": f"0x{val:0{hex_w}x}",
        "bin": f"0b{val:0{width}b}" if width <= 64 else f"0b…({width}bit)",
    }


def reverse_u32_bits(val: int) -> int:
    v = val & 0xFFFFFFFF
    return ((v & 0x000000FF) << 24) | ((v & 0x0000FF00) << 8) | ((v & 0x00FF0000) >> 8) | ((v & 0xFF000000) >> 24)


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


def decode_trace(words: list[int], layout: dict[str, Any]) -> dict[str, Any]:
    need = int(layout.get("word_count", 0))
    if need and len(words) < need:
        raise DecodeError(f"长度不足：需要 {need} 个 u32，实际 {len(words)}")
    # 允许略多：裁到 word_count；不足已在上面报错
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
        if fd.get("byte_rev") in (True, "u8x4", "rev_u8", "true"):
            value = reverse_u32_bits(value)
        rows.append(
            {
                "domain": domain,
                "name": name,
                "bits": f"[{hi}:{lo}]",
                "hi": hi,
                "lo": lo,
                "width": width,
                "value": value,
                "value_hex": format_value(value, width)["hex"],
                "value_dec": format_value(value, width)["dec"],
                "value_bin": format_value(value, width)["bin"],
                "desc": desc,
                "reserved": name.lower() in ("rsv", "reserved") or "保留" in desc
                or name.lower().endswith("_rsv")
                or "reserved" in desc.lower(),
            }
        )
    return {
        "title": layout.get("title") or "Iparser register trace",
        "word_count": need,
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
        "fields": rows,
        "errors": errors,
    }


def decode_segment(segment: str, words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    seg = segment.lower().strip()
    norm = "iparser_trace" if seg in ("iparser", "iparser_trace", "trace") else seg
    traces = layouts.get("traces") or {}
    if norm not in traces:
        raise DecodeError(f"未知子段: {segment}")
    return decode_trace(words, traces[norm])


def decode_paste(
    text: str,
    module: str,
    layouts: dict[str, Any],
    *,
    segment: str | None = None,
    mau: int | None = None,
) -> dict[str, Any]:
    module = (module or "iparser").lower().strip()
    words = parse_u32_tokens(text)
    result: dict[str, Any] = {
        "module": module,
        "word_count": len(words),
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
    }
    if module in ("iparser", "iparser_trace"):
        seg = segment or "iparser_trace"
        result["segment"] = seg
        result["decoded"] = decode_segment(seg, words, layouts)
        result["category"] = "trace"
        return result
    raise DecodeError(f"未知模块: {module}")


def parse_log(text: str, layouts: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    解析日志中的 iparser 块（---- iparser start/end ----），
    或整段粘贴的寄存器 dump。
    返回 modules.iparser 风格的 list 项，便于 viewer 接入。
    """
    layouts = layouts or load_layouts()
    layout = layouts["traces"]["iparser_trace"]
    errors: list[str] = []
    items: list[dict[str, Any]] = []

    blocks = extract_blocks(text)
    for blk in blocks:
        if not IPARSER_NAME_RE.match(blk["name"]):
            continue
        try:
            words = parse_u32_tokens(blk["text"])
        except DecodeError as e:
            errors.append(f"iparser: {e}")
            continue
        try:
            decoded = decode_trace(words, layout)
        except DecodeError as e:
            errors.append(f"iparser: {e}")
            continue
        items.append(
            {
                "source": blk["name"],
                "decoded": decoded,
                "word_count": len(words),
                "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
            }
        )

    if not items:
        # 无命名块：整段当作 dump
        try:
            words = parse_u32_tokens(text)
            decoded = decode_trace(words, layout)
            items.append(
                {
                    "source": "paste",
                    "decoded": decoded,
                    "word_count": len(words),
                    "words_hex": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
                }
            )
        except DecodeError as e:
            errors.append(str(e))

    return {
        "module": "iparser",
        "items": items,
        "errors": errors,
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="iparser dump 解码")
    ap.add_argument("textfile", nargs="?", help="含 dump 的文件；缺省读 stdin")
    ap.add_argument("-y", "--yaml", default=str(DEFAULT_YAML), help="yaml 文件路径")
    args = ap.parse_args()
    layouts = load_layouts(args.yaml)
    raw = (
        Path(args.textfile).read_text(encoding="utf-8", errors="replace")
        if args.textfile
        else __import__("sys").stdin.read()
    )
    data = parse_log(raw, layouts) if raw.strip() else {"module": "iparser", "error": "未提供文本"}
    print(json.dumps(data, ensure_ascii=False, indent=2))
