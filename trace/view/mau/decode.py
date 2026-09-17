"""MAU / MPL trace 解码引擎：按 mau_trace.yaml 从 u32 Domain 抽字段。"""

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
# view/mau/decode.py → tools/trace/mau_trace.yaml
TRACE_ROOT = HERE.parents[1]
DEFAULT_YAML = TRACE_ROOT / "mau_trace.yaml"

# mau 实例 ↔ 方向
IPP_MAUS = list(range(0, 9))   # mau0..mau8
EPP_MAUS = list(range(9, 11))  # mau9..mau10

# 子段 → yaml traces 键；vme 为整段 52 word
SEGMENT_LAYOUT = {
    "cls": "cls_trace",
    "keygen": "keygen_trace",
    "lrr": "lrr_trace",
    "egr": "egr_trace",
    "vme": None,  # lama + lamb
    "vme_lama": "vme_lama_trace",
    "vme_lamb": "vme_lamb_trace",
}

SEGMENT_ALIASES = {
    "cls_trace": "cls",
    "keygen_trace": "keygen",
    "lrr_trace": "lrr",
    "llr_trace": "lrr",
    "egr_trace": "egr",
    "vme0_trace": "vme0",
    "vme1_trace": "vme1",
    "vme2_trace": "vme2",
    "vme3_trace": "vme3",
    "vme4_trace": "vme4",
}

# 子段类别：trace（mau_trace）/ statistics（mau_statistics）
TRACE_SEGMENTS = ["cls", "keygen", "vme0", "vme1", "vme2", "vme3", "vme4", "lrr", "egr"]
STAT_SEGMENTS = [
    "trace_ctrl",
    "other_cfg",
    "cfg_inst",
    "fw_init",
    "fw_ecc",
    "fw_dbg",
    "bp_stat",
    "fifo_thres",
]

_PAW_NAME_RE = re.compile(r"^Paw\d+$", re.IGNORECASE)


def segment_category(segment: str) -> str:
    """返回 'trace' | 'statistics'。"""
    seg = SEGMENT_ALIASES.get(segment, segment).lower()
    if seg.endswith("_trace"):
        seg = seg[: -len("_trace")]
    if seg in ("statistics", "mau_statistics") or "stat" in seg:
        return "statistics"
    if seg in STAT_SEGMENTS:
        return "statistics"
    if seg in TRACE_SEGMENTS or seg in ("vme", "vme_lama", "vme_lamb") or re.fullmatch(
        r"vme\d", seg
    ):
        return "trace"
    return "trace"


def group_paw_rows(fields: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    从字段列表抽出 VME Paw*：每组 4 个 u32 一行，列顺序与 yaml 一致
    （[31:0] → [63:32] → [95:64] → [127:96]）。
    返回 (其余字段, paw_rows)。
    paw_rows 项: {name, hi_lo, words_hex[4], domains}
    """
    other: list[dict[str, Any]] = []
    paw_rows: list[dict[str, Any]] = []
    i = 0
    while i < len(fields):
        f = fields[i]
        name = str(f.get("name", ""))
        if not _PAW_NAME_RE.match(name):
            other.append(f)
            i += 1
            continue
        group = [f]
        j = i + 1
        while j < len(fields) and str(fields[j].get("name", "")) == name:
            group.append(fields[j])
            j += 1
        # 每 4 个 u32 一行；顺序与 mau_trace.yaml 中同名连续条目一致
        for k in range(0, len(group), 4):
            chunk = group[k : k + 4]
            lo_desc = chunk[0].get("desc", "")
            hi_desc = chunk[-1].get("desc", "") if chunk else ""
            paw_rows.append(
                {
                    "name": name,
                    "hi_lo": f"{lo_desc} … {hi_desc}" if lo_desc else name,
                    "words_hex": [c.get("value_hex", "0x0") for c in chunk],
                    "domains": [c.get("domain") for c in chunk],
                    "width_bits": 32 * len(chunk),
                }
            )
        i = j
    return other, paw_rows


def attach_paw_view(decoded: dict[str, Any]) -> dict[str, Any]:
    """给含 Paw* 的解码结果挂上 paw_rows，并从 fields 中移出这些行。"""
    fields = decoded.get("fields") or []
    other, paw_rows = group_paw_rows(fields)
    if paw_rows:
        decoded = {**decoded, "fields": other, "paw_rows": paw_rows}
    return decoded


_CTN_IDX_RE = re.compile(r"ctn_u16_(en|val)\[(\d+)\]", re.I)


def group_ctn_u16_pairs(
    fields: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    将 ctn_u16_en[i] 与 ctn_u16_val[i] 配成 16 组；其余字段原样返回。
    pair: {index, en, val}
    """
    other: list[dict[str, Any]] = []
    en_map: dict[int, dict[str, Any]] = {}
    val_map: dict[int, dict[str, Any]] = {}
    en_seq = 0
    val_seq = 0
    for f in fields:
        name = str(f.get("name", ""))
        desc = str(f.get("desc", ""))
        m = _CTN_IDX_RE.search(desc) or _CTN_IDX_RE.search(name)
        if name == "ctn_u16_en" or (m and m.group(1).lower() == "en"):
            idx = int(m.group(2)) if m else en_seq
            en_map[idx] = f
            en_seq += 1
            continue
        if name == "ctn_u16_val" or (m and m.group(1).lower() == "val"):
            idx = int(m.group(2)) if m else val_seq
            val_map[idx] = f
            val_seq += 1
            continue
        other.append(f)
    if not en_map and not val_map:
        return fields, []
    pairs = [
        {"index": i, "en": en_map.get(i), "val": val_map.get(i)}
        for i in sorted(set(en_map) | set(val_map))
    ]
    return other, pairs


def attach_ctn_u16_view(decoded: dict[str, Any]) -> dict[str, Any]:
    fields = decoded.get("fields") or []
    other, pairs = group_ctn_u16_pairs(fields)
    if pairs:
        decoded = {**decoded, "fields": other, "ctn_u16_pairs": pairs}
    return decoded


def attach_lur_view(decoded: dict[str, Any]) -> dict[str, Any]:
    """
    将 Lur 298bit 拆成：
      lur-42  = Lur[41:0]
      lur-256 = Lur[297:42]
    并从 fields / 旧 Lur hex_blobs 中移出逐字字段。
    """
    fields = decoded.get("fields") or []
    other: list[dict[str, Any]] = []
    lur: list[dict[str, Any]] = []
    for f in fields:
        if str(f.get("name", "")).lower() == "lur":
            lur.append(f)
        else:
            other.append(f)
    if not lur:
        return decoded

    acc = 0
    bit_pos = 0
    for f in lur:
        width = int(f.get("width") or 0)
        if width <= 0:
            continue
        raw = f.get("value")
        if raw is None:
            raw = int(str(f.get("value_hex") or "0"), 16)
        mask = (1 << width) - 1
        acc |= (int(raw) & mask) << bit_pos
        bit_pos += width

    lur42 = acc & ((1 << 42) - 1)
    lur256 = (acc >> 42) & ((1 << 256) - 1)
    hex42 = f"0x{lur42:011x}"
    words256 = [f"0x{(lur256 >> (32 * i)) & 0xFFFFFFFF:08x}" for i in range(8)]

    lur_blobs = [
        {
            "name": "lur-42",
            "label": "lur-42 · Lur[41:0] · 42bit",
            "hex_line": hex42,
            "words_hex": [hex42],
            "width": 42,
            "word_count": 1,
            "bits": "[41:0]",
        },
        {
            "name": "lur-256",
            "label": "lur-256 · Lur[297:42] · 256bit（切片内低位→高位 8×u32）",
            "hex_line": " ".join(words256),
            "words_hex": words256,
            "width": 256,
            "word_count": 8,
            "bits": "[297:42]",
        },
    ]
    existing = [
        b
        for b in (decoded.get("hex_blobs") or [])
        if str(b.get("name", "")).lower() != "lur"
    ]
    return {
        **decoded,
        "fields": other,
        "hex_blobs": existing + lur_blobs,
        "lur_blobs": lur_blobs,
    }


class DecodeError(ValueError):
    """长度不足 / Domain 不符 / 非法输入。"""


def load_layouts(path: Path | str | None = None) -> dict[str, Any]:
    p = Path(path) if path else DEFAULT_YAML
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "traces" not in data:
        raise DecodeError(f"无效格式表: {p}")
    return data


def layouts_to_json(layouts: dict[str, Any]) -> str:
    return json.dumps(layouts, ensure_ascii=False, separators=(",", ":"))


def parse_bits_hi_lo(bits: Any) -> tuple[int, int, int]:
    """
    yaml bits: [hi, lo] → (hi, lo, width)。
    一字内 bit0=LSB、bit31=MSB；与 Verilog [hi:lo] 一致。
    """
    if not isinstance(bits, (list, tuple)) or len(bits) != 2:
        raise DecodeError(f"bits 须为 [hi, lo]，收到: {bits!r}")
    hi, lo = int(bits[0]), int(bits[1])
    if hi < lo:
        raise DecodeError(
            f"bits 应为 [hi, lo] 且 hi>=lo（bit0=LSB, bit31=MSB），收到 [{hi}, {lo}]"
        )
    if lo < 0 or hi > 31:
        raise DecodeError(f"非法 bits [{hi}:{lo}]（超出 u32 bit0..bit31）")
    return hi, lo, hi - lo + 1


def extract_bits(word: int, hi: int, lo: int) -> int:
    """从 u32 按绝对 bit 下标抽取 [hi:lo]（bit0=LSB）。"""
    if hi < lo or lo < 0 or hi > 31:
        raise DecodeError(f"非法 bits [{hi}:{lo}]")
    width = hi - lo + 1
    mask = (1 << width) - 1
    return ((int(word) & 0xFFFFFFFF) >> lo) & mask


def format_value(val: int, width: int) -> dict[str, str]:
    hex_w = max(1, (width + 3) // 4)
    return {
        "dec": str(val),
        "hex": f"0x{val:0{hex_w}x}",
        "bin": f"0b{val:0{width}b}" if width <= 64 else f"0b…({width}bit)",
    }


def reverse_u8x4(val: int) -> int:
    """u32 按 4×u8 反序：0x05004040 → 0x40400005。"""
    v = int(val) & 0xFFFFFFFF
    return (
        ((v & 0x000000FF) << 24)
        | ((v & 0x0000FF00) << 8)
        | ((v & 0x00FF0000) >> 8)
        | ((v & 0xFF000000) >> 24)
    ) & 0xFFFFFFFF


def apply_byte_rev(val: int, fd: dict[str, Any]) -> int:
    mode = fd.get("byte_rev")
    if not mode:
        return val
    if mode is True or str(mode) in ("u8x4", "rev_u8", "true", "1"):
        return reverse_u8x4(val)
    raise DecodeError(f"{fd.get('name', '')}: 未知 byte_rev={mode!r}")


def _field_row(
    domain: int | None,
    name: str,
    hi: int,
    lo: int,
    width: int,
    value: int,
    desc: str = "",
    *,
    domain_label: str | None = None,
    bits_label: str | None = None,
) -> dict[str, Any]:
    reserved = name.lower() in ("rsv", "reserved") or "保留" in (desc or "")
    return {
        "domain": domain,
        "domain_label": domain_label,
        "name": name,
        "bits": bits_label if bits_label is not None else f"[{hi}:{lo}]",
        "hi": hi,
        "lo": lo,
        "width": width,
        "value": value,
        "value_hex": format_value(value, width)["hex"],
        "value_dec": format_value(value, width)["dec"],
        "value_bin": format_value(value, width)["bin"],
        "desc": desc or "",
        "reserved": reserved,
    }


def decode_composed_field(
    words: list[int],
    fd: dict[str, Any],
) -> dict[str, Any]:
    """跨 Domain 拼字段：pieces[].bits → into 合成值内 [hi:lo]。"""
    name = str(fd.get("name", ""))
    desc = str(fd.get("desc", ""))
    pieces = fd.get("pieces") or []
    if not pieces:
        raise DecodeError(f"{name}: compose 字段缺少 pieces")

    logic_bits = fd.get("bits")
    if logic_bits is not None:
        a, b = int(logic_bits[0]), int(logic_bits[1])
        if a < b or b < 0:
            raise DecodeError(f"{name}: 非法逻辑 bits [{a}:{b}]")
        hi, lo, width = a, b, a - b + 1
    else:
        width = int(fd.get("width") or 0)
        if width <= 0:
            raise DecodeError(f"{name}: 缺少 bits/width")
        hi, lo = width - 1, 0

    yw = fd.get("width")
    if yw is not None and int(yw) != width:
        raise DecodeError(f"{name}: width={yw} 与 bits[{hi}:{lo}] 宽度 {width} 不一致")

    val = 0
    src_parts: list[str] = []
    domains: list[int] = []
    for p in pieces:
        d = int(p["domain"])
        phi, plo, pw = parse_bits_hi_lo(p["bits"])
        into = p.get("into")
        if into is None:
            raise DecodeError(f"{name}: piece D{d} 缺少 into: [hi, lo]")
        ihi, ilo = int(into[0]), int(into[1])
        if ihi < ilo or ilo < 0:
            raise DecodeError(f"{name}: 非法 into [{ihi}:{ilo}]")
        if ihi - ilo + 1 != pw:
            raise DecodeError(
                f"{name}: D{d}[{phi}:{plo}] 宽 {pw} 与 into[{ihi}:{ilo}] 不一致"
            )
        if d < 0 or d >= len(words):
            raise DecodeError(f"{name}: D{d} 越界（共 {len(words)} word）")
        piece = extract_bits(words[d], phi, plo)
        val |= piece << ilo
        src_parts.append(f"D{d}[{phi}:{plo}]→[{ihi}:{ilo}]")
        domains.append(d)

    dom_label = "+".join(f"D{d}" for d in dict.fromkeys(domains))
    bits_label = f"[{hi}:{lo}] ({'+'.join(src_parts)})"
    return _field_row(
        None,
        name,
        hi,
        lo,
        width,
        val & ((1 << width) - 1),
        desc,
        domain_label=dom_label,
        bits_label=bits_label,
    )


def attach_hex_blobs(decoded: dict[str, Any]) -> dict[str, Any]:
    """
    连续同名、整 u32（[31:0]）字段另出 hex 框：各 word 以空格分隔。
    不从 fields 中移除，原字段表仍保留。
    """
    fields = decoded.get("fields") or []
    blobs: list[dict[str, Any]] = []
    i = 0
    while i < len(fields):
        f = fields[i]
        name = str(f.get("name", ""))
        if (
            int(f.get("width") or 0) == 32
            and int(f.get("hi") if f.get("hi") is not None else -1) == 31
            and int(f.get("lo") if f.get("lo") is not None else -1) == 0
            and name
        ):
            group = [f]
            j = i + 1
            while j < len(fields):
                g = fields[j]
                if (
                    str(g.get("name", "")) == name
                    and int(g.get("width") or 0) == 32
                    and int(g.get("hi") if g.get("hi") is not None else -1) == 31
                    and int(g.get("lo") if g.get("lo") is not None else -1) == 0
                ):
                    group.append(g)
                    j += 1
                else:
                    break
            if len(group) >= 2:
                words_hex: list[str] = []
                for c in group:
                    hx = str(c.get("value_hex") or "0x0")
                    try:
                        words_hex.append(f"0x{int(hx, 16) & 0xFFFFFFFF:08x}")
                    except ValueError:
                        words_hex.append(hx)
                # mau_lpm_req_data：尾随同名 16bit 并入第 9 个 u32（低 16 有效）
                if name == "mau_lpm_req_data" and j < len(fields):
                    tail = fields[j]
                    if (
                        str(tail.get("name", "")) == name
                        and int(tail.get("width") or 0) == 16
                    ):
                        hx = str(tail.get("value_hex") or "0x0")
                        try:
                            words_hex.append(f"0x{int(hx, 16) & 0xFFFF:08x}")
                        except ValueError:
                            words_hex.append(hx)
                        j += 1
                lo_desc = str(group[0].get("desc") or "")
                hi_desc = str(group[-1].get("desc") or "")
                label = f"{name} · 原始" if name == "mau_lpm_req_data" else (
                    f"{name} · {lo_desc} … {hi_desc}" if lo_desc else name
                )
                blobs.append(
                    {
                        "name": name,
                        "label": label,
                        "hex_line": " ".join(words_hex),
                        "words_hex": words_hex,
                        "domains": [c.get("domain") for c in group],
                        "word_count": len(words_hex),
                    }
                )
            i = j
            continue
        i += 1
    if blobs:
        decoded = {**decoded, "hex_blobs": blobs}
    return decoded


def decode_trace(
    words: list[int],
    layout: dict[str, Any],
    *,
    allow_short: bool = False,
) -> dict[str, Any]:
    """按 traces.* 字段表解码 Domain 数组。"""
    need = int(layout.get("word_count", 0))
    domain_base = int(layout.get("domain_base", 0) or 0)
    # lamb 等：domain 为绝对下标，word_count 为段长 → 至少要 domain_base+word_count
    min_len = (domain_base + need) if (need and domain_base) else need
    if min_len and len(words) < min_len and not allow_short:
        raise DecodeError(f"长度不足：需要 {min_len} 个 Domain，实际 {len(words)}")
    # 有 domain_base 时不截断（保留绝对 Domain）；否则裁到 word_count
    if need and not domain_base and len(words) > need:
        words = words[:need]

    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for fd in layout.get("fields") or []:
        name = str(fd.get("name", ""))
        # 跨 Domain 合成字段
        if fd.get("pieces"):
            try:
                rows.append(decode_composed_field(words, fd))
            except DecodeError as e:
                errors.append(str(e))
            continue

        domain = int(fd["domain"])
        desc = str(fd.get("desc", ""))
        try:
            hi, lo, width_bits = parse_bits_hi_lo(fd["bits"])
        except DecodeError as e:
            errors.append(f"D{domain} {name}: {e}")
            continue
        # 取值严格按 bits；yaml width 不一致时以 bits 为准并告警
        width = width_bits
        yw = fd.get("width")
        if yw is not None and int(yw) != width_bits:
            errors.append(
                f"D{domain} {name}: width={yw} 与 bits[{hi}:{lo}] 宽度 {width_bits} 不一致，已按 bits 解析"
            )
        if domain < 0 or domain >= len(words):
            errors.append(f"D{domain} 越界（共 {len(words)} word）: {name}")
            continue
        try:
            val = extract_bits(words[domain], hi, lo)
            val = apply_byte_rev(val, fd)
        except DecodeError as e:
            errors.append(f"D{domain} {name}: {e}")
            continue
        row = _field_row(domain, name, hi, lo, width, val, desc)
        if fd.get("byte_rev"):
            row["byte_rev"] = fd.get("byte_rev")
        rows.append(row)

    out = {
        "title": layout.get("title") or "",
        "word_count": need,
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
        "fields": rows,
        "errors": errors,
    }
    return attach_lur_view(attach_ctn_u16_view(attach_hex_blobs(out)))


def collect_mau_lpm_req_u32s(words: list[int], keygen: dict[str, Any]) -> list[int]:
    """
    按 keygen 中 mau_lpm_req_data 字段出现顺序收集为 9×u32：
    前 8 个为整 u32，第 9 个为尾 16bit 零扩展。
    """
    out: list[int] = []
    for fd in keygen.get("fields") or []:
        if str(fd.get("name")) != "mau_lpm_req_data":
            continue
        domain = int(fd["domain"])
        hi, lo, width = parse_bits_hi_lo(fd["bits"])
        if domain >= len(words):
            raise DecodeError(f"拼包缺 Domain D{domain}")
        piece = extract_bits(words[domain], hi, lo)
        if width >= 32:
            out.append(piece & 0xFFFFFFFF)
        else:
            out.append(piece & ((1 << width) - 1))
    if len(out) != 9:
        raise DecodeError(f"mau_lpm_req_data 期望 9×u32（8×32+16），实际 {len(out)} 片")
    return out


# 第 9 个 u32 低 16bit 的 hdr 位域（相对该 16bit，不采用 yaml payload bits）
_LPM_HDR_BITS = {
    "lu_sip_vld": (15, 15),
    "lu_dip_vld": (14, 14),
    "is_ipv6": (13, 13),
    "vrf": (12, 0),
}


def decode_lpm_req_from_u32s(
    u32s: list[int],
    payload_layout: dict[str, Any],
) -> dict[str, Any]:
    """
    按 9×u32 展示规则解码（不依赖 yaml 中 sip/dip/hdr 的 bit 拼法，仅用字段名/desc）：
      u32[1..4] → dip（展示倒序 4,3,2,1）
      u32[5..8] → sip（展示倒序 8,7,6,5）
      u32[9] 低 16bit → hdr：lu_sip_vld=bit15, lu_dip_vld=bit14, is_ipv6=bit13, vrf=[12:0]
    """
    if len(u32s) != 9:
        raise DecodeError(f"lpm 需要 9×u32，实际 {len(u32s)}")
    hdr = int(u32s[8]) & 0xFFFF
    sip_disp = [int(u32s[i]) & 0xFFFFFFFF for i in (7, 6, 5, 4)]
    dip_disp = [int(u32s[i]) & 0xFFFFFFFF for i in (3, 2, 1, 0)]

    def pack_be128(ws: list[int]) -> int:
        v = 0
        for i, w in enumerate(ws):
            v |= (w & 0xFFFFFFFF) << (32 * (3 - i))
        return v

    sip_val = pack_be128(sip_disp)
    dip_val = pack_be128(dip_disp)
    words_hex_line = " ".join(f"0x{w:08x}" for w in u32s)

    rows: list[dict[str, Any]] = []
    for fd in payload_layout.get("fields") or []:
        name = str(fd.get("name", ""))
        bits = fd.get("bits")
        if not isinstance(bits, (list, tuple)) or len(bits) != 2:
            raise DecodeError(f"payload bits 须为 [hi, lo]: {bits!r}")
        hi, lo = int(bits[0]), int(bits[1])
        width = hi - lo + 1
        desc = str(fd.get("desc", ""))
        if name in _LPM_HDR_BITS:
            hi, lo = _LPM_HDR_BITS[name]
            width = hi - lo + 1
            val = (hdr >> lo) & ((1 << width) - 1)
            row = _field_row(None, name, hi, lo, width, val, desc)
        elif name == "sip":
            row = _field_row(None, name, hi, lo, 128, sip_val, desc)
            row["words_hex"] = [f"0x{w:08x}" for w in sip_disp]
            row["value_hex_words"] = " ".join(row["words_hex"])
            row["words_rev"] = True
        elif name == "dip":
            row = _field_row(None, name, hi, lo, 128, dip_val, desc)
            row["words_hex"] = [f"0x{w:08x}" for w in dip_disp]
            row["value_hex_words"] = " ".join(row["words_hex"])
            row["words_rev"] = True
        else:
            # 未知字段：跳过或按 0
            row = _field_row(None, name, hi, lo, width, 0, desc)
        hl = fd.get("highlight")
        if hl:
            row["highlight"] = hl
        rows.append(row)

    highlighted = [r for r in rows if r.get("highlight")]
    rest = [r for r in rows if not r.get("highlight")]
    return {
        "title": "lpm_mpl_req_data",
        "width": int(payload_layout.get("width") or 272),
        "bitvec_hex": words_hex_line,
        "raw_u32s": [f"0x{w:08x}" for w in u32s],
        "hex_blobs": [
            {
                "name": "mau_lpm_req_data",
                "label": "mau_lpm_req_data · 原始",
                "hex_line": words_hex_line,
                "words_hex": [f"0x{w:08x}" for w in u32s],
                "word_count": 9,
            }
        ],
        "fields": highlighted + rest,
        "enable_fields": highlighted,
        "note": payload_layout.get("note") or "",
    }


def assemble_payload_bits(
    words: list[int],
    field_name: str,
    layout: dict[str, Any],
    *,
    msb_first: bool = False,
) -> int:
    """
    从 trace 中同名字段按出现顺序拼成宽位向量。
    默认 LSB 先放；msb_first 时第一片落在最高位（与图示 hex 左高右低一致）。
    """
    pieces: list[tuple[int, int]] = []
    for fd in layout.get("fields") or []:
        if str(fd.get("name")) != field_name:
            continue
        domain = int(fd["domain"])
        hi, lo, width = parse_bits_hi_lo(fd["bits"])
        if domain >= len(words):
            raise DecodeError(f"拼包缺 Domain D{domain}")
        piece = extract_bits(words[domain], hi, lo)
        pieces.append((piece, width))
    if not msb_first:
        acc = 0
        bit_pos = 0
        for piece, width in pieces:
            acc |= piece << bit_pos
            bit_pos += width
        return acc
    total = sum(w for _, w in pieces)
    acc = 0
    bit_pos = total
    for piece, width in pieces:
        bit_pos -= width
        acc |= (piece & ((1 << width) - 1)) << bit_pos
    return acc


def decode_payload(
    bitvec: int,
    payload_layout: dict[str, Any],
    *,
    title: str | None = None,
) -> dict[str, Any]:
    width_total = int(payload_layout.get("width", 0))
    rows: list[dict[str, Any]] = []
    for fd in payload_layout.get("fields") or []:
        # payload 向量可 >32bit：仅校验 hi>=lo>=0，不限制 hi<=31
        bits = fd["bits"]
        if not isinstance(bits, (list, tuple)) or len(bits) != 2:
            raise DecodeError(f"payload bits 须为 [hi, lo]: {bits!r}")
        hi, lo = int(bits[0]), int(bits[1])
        if hi < lo or lo < 0:
            raise DecodeError(f"非法 payload bits [{hi}:{lo}]")
        width = hi - lo + 1
        yw = fd.get("width")
        if yw is not None and int(yw) != width:
            width = hi - lo + 1  # bits 为准
        mask = (1 << width) - 1
        val = (bitvec >> lo) & mask
        row = _field_row(None, str(fd.get("name", "")), hi, lo, width, val, str(fd.get("desc", "")))
        hl = fd.get("highlight")
        if hl:
            row["highlight"] = hl
        # 宽字段（如 val 256bit）附带 n×u32 空格分隔；words_rev 时高字在前
        if width >= 64:
            words = []
            nwords = (width + 31) // 32
            for i in range(nwords):
                w = (val >> (32 * i)) & 0xFFFFFFFF
                words.append(f"0x{w:08x}")
            if fd.get("words_rev"):
                words = list(reversed(words))
            row["words_hex"] = words
            row["value_hex_words"] = " ".join(words)
            if fd.get("words_rev"):
                row["words_rev"] = True
        rows.append(row)
    highlighted = [r for r in rows if r.get("highlight")]
    rest = [r for r in rows if not r.get("highlight")]
    return {
        "title": title or payload_layout.get("title") or "payload",
        "width": width_total,
        "bitvec_hex": f"0x{bitvec:x}",
        "fields": highlighted + rest,
        "enable_fields": highlighted,
        "note": payload_layout.get("note") or "",
    }


def decode_mpl(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """mpl 独立模块：将 u32 字按 LE 拼成宽位向量，按 payloads.mau_mpl_req_data 解。"""
    if not words:
        raise DecodeError("mpl：空输入")
    bitvec = 0
    for i, w in enumerate(words):
        bitvec |= (int(w) & 0xFFFFFFFF) << (32 * i)
    return decode_payload(bitvec, layouts["payloads"]["mau_mpl_req_data"], title="mau_mpl_req_data")


def preview_mpl_req_from_keygen(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """从 keygen Domain 拼出 mau_mpl_req_data 预览（属 keygen 附属，不是 mpl 模块本身）。"""
    keygen = layouts["traces"]["keygen_trace"]
    payload_def = layouts["payloads"]["mau_mpl_req_data"]
    need = int(keygen.get("word_count", 29))
    if len(words) < need:
        raise DecodeError(f"keygen 长度不足：需要 {need}，实际 {len(words)}")
    bitvec = assemble_payload_bits(words[:need], "mau_mpl_req_data", keygen)
    return decode_payload(bitvec, payload_def, title="mau_mpl_req_data")


def preview_mpl_rsp_from_lrr(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """从 lrr Domain 中 Lur 字段拼出 298bit，按 payloads.mau_mpl_rsp_data 解。"""
    payloads = layouts.get("payloads") or {}
    if "mau_mpl_rsp_data" not in payloads:
        raise DecodeError("缺少 payloads.mau_mpl_rsp_data")
    lrr = layouts["traces"]["lrr_trace"]
    need = int(lrr.get("word_count", 26))
    if len(words) < need:
        raise DecodeError(f"lrr 长度不足：需要 {need}，实际 {len(words)}")
    bitvec = assemble_payload_bits(words[:need], "Lur", lrr)
    return decode_payload(bitvec, payloads["mau_mpl_rsp_data"], title="mau_mpl_rsp_data")


def preview_lpm_req_from_keygen(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """从 keygen Domain 收集 9×u32 mau_lpm_req_data，按展示规则解字段。"""
    payloads = layouts.get("payloads") or {}
    if "lpm_mpl_req_data" not in payloads:
        raise DecodeError("缺少 payloads.lpm_mpl_req_data")
    payload = payloads["lpm_mpl_req_data"]
    keygen = layouts["traces"]["keygen_trace"]
    need = int(keygen.get("word_count", 29))
    if len(words) < need:
        raise DecodeError(f"keygen 长度不足：需要 {need}，实际 {len(words)}")
    u32s = collect_mau_lpm_req_u32s(words[:need], keygen)
    return decode_lpm_req_from_u32s(u32s, payload)


def collect_lpm_result_u32s(words: list[int], egr: dict[str, Any]) -> list[int]:
    """
    收集 egr 中 lpm_result 三片：
      2×u32 → [31:0]、[63:32]；12bit → [75:64]（D50[11:0]）。
    返回 [u32_lo, u32_mid, u12_hi]。
    """
    lo32: int | None = None
    mid32: int | None = None
    hi12: int | None = None
    for fd in egr.get("fields") or []:
        if str(fd.get("name")) != "lpm_result":
            continue
        domain = int(fd["domain"])
        hi, lo, width = parse_bits_hi_lo(fd["bits"])
        if domain >= len(words):
            raise DecodeError(f"拼包缺 Domain D{domain}")
        piece = extract_bits(words[domain], hi, lo)
        if width == 32:
            if lo32 is None:
                lo32 = piece & 0xFFFFFFFF
            elif mid32 is None:
                mid32 = piece & 0xFFFFFFFF
            else:
                raise DecodeError("lpm_result 超过 2 个 u32")
        elif width == 12:
            hi12 = piece & 0xFFF
        else:
            raise DecodeError(f"lpm_result 片宽须为 32 或 12，实际 {width}")
    if lo32 is None or mid32 is None or hi12 is None:
        raise DecodeError("lpm_result 期望 2×u32 + 12bit")
    return [lo32, mid32, hi12]


def assemble_lpm_rsp_bitvec(u32s: list[int]) -> int:
    """76bit：[31:0]=u32s[0]，[63:32]=u32s[1]，[75:64]=u32s[2] 低 12bit。"""
    if len(u32s) != 3:
        raise DecodeError(f"lpm_result 需要 3 片，实际 {len(u32s)}")
    return (
        (int(u32s[0]) & 0xFFFFFFFF)
        | ((int(u32s[1]) & 0xFFFFFFFF) << 32)
        | ((int(u32s[2]) & 0xFFF) << 64)
    )


def decode_lpm_rsp_from_u32s(
    u32s: list[int],
    payload_layout: dict[str, Any],
) -> dict[str, Any]:
    """按 payloads.lpm_mpl_rsp_data 的 bits 解析 76bit lpm_result。"""
    bitvec = assemble_lpm_rsp_bitvec(u32s)
    out = decode_payload(bitvec, payload_layout, title="lpm_mpl_rsp_data")
    words_hex = [
        f"0x{int(u32s[0]) & 0xFFFFFFFF:08x}",
        f"0x{int(u32s[1]) & 0xFFFFFFFF:08x}",
        f"0x{int(u32s[2]) & 0xFFF:08x}",
    ]
    out["raw_u32s"] = words_hex
    out["hex_blobs"] = [
        {
            "name": "lpm_result",
            "label": "lpm_result · D48|D49|D50[11:0] → [63:0]|[75:64]",
            "hex_line": " ".join(words_hex),
            "words_hex": words_hex,
            "word_count": 3,
        }
    ]
    return out


def preview_lpm_rsp_from_egr(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """从 egr Domain 拼出 lpm_result，按 payloads.lpm_mpl_rsp_data 解。"""
    payloads = layouts.get("payloads") or {}
    if "lpm_mpl_rsp_data" not in payloads:
        raise DecodeError("缺少 payloads.lpm_mpl_rsp_data")
    egr = layouts["traces"]["egr_trace"]
    need = int(egr.get("word_count", 54))
    if len(words) < need:
        raise DecodeError(f"egr 长度不足：需要 {need}，实际 {len(words)}")
    u32s = collect_lpm_result_u32s(words[:need], egr)
    return decode_lpm_rsp_from_u32s(u32s, payloads["lpm_mpl_rsp_data"])


# 兼容旧名
decode_mpl_from_keygen = preview_mpl_req_from_keygen


def decode_vme(words: list[int], layouts: dict[str, Any]) -> dict[str, Any]:
    """52 word → lama(26) + lamb(26)；Paw 按 yaml 顺序 4×u32 一行。"""
    traces = layouts["traces"]
    lama_l = traces["vme_lama_trace"]
    lamb_l = traces["vme_lamb_trace"]
    need = 52
    if len(words) < need:
        raise DecodeError(f"vme 长度不足：需要 {need}，实际 {len(words)}")
    words = words[:need]
    return {
        "title": "VME trace",
        "word_count": need,
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
        "lama": attach_paw_view(decode_trace(words, lama_l)),
        "lamb": attach_paw_view(decode_trace(words, lamb_l)),
        "errors": [],
    }


def _fmt_reset(val: Any) -> str | None:
    if val is None:
        return None
    try:
        n = int(val, 0) if isinstance(val, str) else int(val)
    except (TypeError, ValueError):
        return str(val)
    return f"0x{n:x}"


def expand_stat_register_slots(section: dict[str, Any]) -> list[dict[str, Any]]:
    """按 offset 排序，将 count>1 的寄存器展开为逐 word 槽位。"""
    regs = section.get("registers") or {}
    items: list[dict[str, Any]] = []
    for name, spec in regs.items():
        if not isinstance(spec, dict):
            continue
        offset = int(spec.get("offset", 0))
        count = int(spec.get("count", 1) or 1)
        step = int(spec.get("step", 4) or 4)
        fields = spec.get("fields") or []
        desc = str(spec.get("desc") or "")
        items_meta = spec.get("items") or []
        reg_reset = _fmt_reset(spec.get("reset")) if "reset" in spec else None
        reg_width = int(spec["width"]) if spec.get("width") is not None else None
        for i in range(count):
            item = items_meta[i] if i < len(items_meta) and isinstance(items_meta[i], dict) else {}
            item_name = str(item.get("name") or "")
            item_desc = str(item.get("desc") or "")
            slot_fields = [dict(fd) for fd in fields]
            if item_desc:
                for fd in slot_fields:
                    fd["desc"] = item_desc
            slot_name = name if count == 1 else f"{name}[{i}]"
            if item_name:
                slot_name = f"{slot_name}.{item_name}" if count > 1 else item_name
            items.append(
                {
                    "name": slot_name,
                    "base_name": name,
                    "index": None if count == 1 else i,
                    "offset": offset + i * step,
                    "fields": slot_fields,
                    "desc": item_desc or desc,
                    "reg_reset": reg_reset,
                    "reg_width": reg_width,
                }
            )
    items.sort(key=lambda x: (x["offset"], x["base_name"], x["index"] or 0))
    return items


def decode_register_fields(word: int, fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按字段 bits 解析；保留 yaml 新格式元数据 access / type / reset。"""
    rows: list[dict[str, Any]] = []
    for fd in fields:
        bits = fd.get("bits") or [31, 0]
        hi, lo, width = parse_bits_hi_lo(bits)
        name = str(fd.get("name", ""))
        desc = str(fd.get("desc", ""))
        # 解码以 bits 为准；yaml width 仅校验
        yaml_w = fd.get("width")
        if yaml_w is not None and int(yaml_w) != width:
            # 不中断：仍按 bits 取位
            pass
        val = extract_bits(int(word) & 0xFFFFFFFF, hi, lo)
        row = _field_row(None, name, hi, lo, width, val, desc)
        if fd.get("access"):
            row["access"] = str(fd["access"])
        if fd.get("type"):
            row["type"] = str(fd["type"])
        if "reset" in fd:
            row["reset"] = _fmt_reset(fd.get("reset"))
        rows.append(row)
    return rows


def decode_statistics_section(
    section_key: str,
    words: list[int],
    layouts: dict[str, Any],
) -> dict[str, Any]:
    """按 statistics.<section>.registers 解码一块统计 dump（word 顺序=offset 升序）。"""
    stats = layouts.get("statistics") or {}
    key = section_key.lower().strip()
    if key not in stats:
        raise DecodeError(f"未知统计段: {section_key}")
    section = stats[key]
    slots = expand_stat_register_slots(section)
    need = len(slots)
    errors: list[str] = []
    if need and len(words) < need:
        errors.append(f"长度不足：需要 {need} 个 Domain，实际 {len(words)}")

    registers_out: list[dict[str, Any]] = []
    flat_fields: list[dict[str, Any]] = []
    for i, slot in enumerate(slots):
        if i >= len(words):
            break
        w = int(words[i]) & 0xFFFFFFFF
        fields = decode_register_fields(w, slot["fields"])
        for f in fields:
            f = {**f, "_reg": slot["name"]}
            flat_fields.append(f)
        reg_out: dict[str, Any] = {
            "name": slot["name"],
            "base_name": slot["base_name"],
            "index": slot["index"],
            "offset": f"0x{slot['offset']:x}",
            "word": f"0x{w:08x}",
            "desc": slot["desc"],
            "fields": fields,
        }
        if slot.get("reg_reset") is not None:
            reg_out["reset"] = slot["reg_reset"]
        if slot.get("reg_width") is not None:
            reg_out["width"] = slot["reg_width"]
        registers_out.append(reg_out)

    extra_words: list[str] = []
    if len(words) > need:
        extra_words = [f"0x{int(w) & 0xFFFFFFFF:08x}" for w in words[need:]]
        errors.append(f"多余 {len(extra_words)} 个 Domain（yaml 定义 {need}）")

    return {
        "kind": "statistics",
        "section": key,
        "title": section.get("title") or key,
        "note": section.get("note") or "",
        "word_count": len(words),
        "expected_count": need,
        "registers": registers_out,
        "fields": flat_fields,
        "extra_words": extra_words,
        "errors": errors,
    }


def decode_segment(
    segment: str,
    words: list[int],
    layouts: dict[str, Any],
) -> dict[str, Any]:
    seg = SEGMENT_ALIASES.get(segment, segment).lower()
    if seg in STAT_SEGMENTS or (
        layouts.get("statistics") and seg in (layouts.get("statistics") or {})
    ):
        return decode_statistics_section(seg, words, layouts)

    traces = layouts["traces"]

    m = re.fullmatch(r"vme(\d)", seg)
    if seg == "vme" or m:
        out = decode_vme(words, layouts)
        if m:
            out["title"] = f"VME{m.group(1)} trace"
            out["vme_index"] = int(m.group(1))
        return out

    if seg in ("vme_lama", "lama"):
        return decode_trace(words, traces["vme_lama_trace"])
    if seg in ("vme_lamb", "lamb"):
        # 若传入相对 26 word，映射到绝对 domain：临时补 26 个 0
        if len(words) == 26:
            words = [0] * 26 + words
        return decode_trace(words, traces["vme_lamb_trace"])

    key = SEGMENT_LAYOUT.get(seg)
    if not key or key not in traces:
        raise DecodeError(f"未知子段: {segment}")
    out = decode_trace(words, traces[key])
    # keygen：按 payloads.mau_mpl_req_data 展示拼出的总线字段（复用 decode_payload）
    if seg == "keygen":
        try:
            out["mau_mpl_req_data"] = preview_mpl_req_from_keygen(words, layouts)
        except DecodeError as e:
            out.setdefault("errors", []).append(f"mau_mpl_req_data: {e}")
        try:
            out["lpm_mpl_req_data"] = preview_lpm_req_from_keygen(words, layouts)
        except DecodeError as e:
            out.setdefault("errors", []).append(f"lpm_mpl_req_data: {e}")
    if seg in ("lrr", "llr"):
        try:
            out["mau_mpl_rsp_data"] = preview_mpl_rsp_from_lrr(words, layouts)
        except DecodeError as e:
            out.setdefault("errors", []).append(f"mau_mpl_rsp_data: {e}")
    if seg == "egr":
        try:
            out["lpm_mpl_rsp_data"] = preview_lpm_rsp_from_egr(words, layouts)
        except DecodeError as e:
            out.setdefault("errors", []).append(f"lpm_mpl_rsp_data: {e}")
    return out


def mau_direction(mau_index: int) -> str:
    if mau_index in IPP_MAUS:
        return "ipp"
    if mau_index in EPP_MAUS:
        return "epp"
    raise DecodeError(f"mau 索引越界: {mau_index}")


def parse_u32_tokens(text: str) -> list[int]:
    """从任意文本提取 u32（0x.. / 纯 hex / 十进制）。

    支持 reg dump 行首地址前缀，例如::
        0x00011308: 0x2e800560 0x00000002 ...
    冒号前的地址不计入 Domain 数据。
    """
    if not text or not text.strip():
        raise DecodeError("空输入")
    # 去掉 "0xADDR:" / "ADDR:"（行首或空白后），避免地址被当成数据
    cleaned = re.sub(
        r"(?m)(?:^|\s)(?:0x)?[0-9a-fA-F]{1,8}\s*:",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    tokens = re.findall(
        r"0x[0-9a-fA-F]+|\b[0-9a-fA-F]{8}\b|\b\d+\b",
        cleaned,
    )
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


def decode_paste(
    text: str,
    module: str,
    layouts: dict[str, Any],
    *,
    segment: str | None = None,
    mau: int | None = None,
) -> dict[str, Any]:
    """粘贴区入口：归一化 hex → 解码。"""
    words = parse_u32_tokens(text)
    module = module.lower().strip()
    result: dict[str, Any] = {
        "module": module,
        "word_count": len(words),
        "words": [f"0x{w & 0xFFFFFFFF:08x}" for w in words],
    }

    if module == "mpl":
        # mpl 与 mau/keygen 同级独立模块，不走 keygen 解码路径
        result["decoded"] = decode_mpl(words, layouts)
        result["category"] = "mpl"
        return result

    if module == "mau":
        seg = segment or "cls"
        result["mau"] = mau
        result["direction"] = mau_direction(mau) if mau is not None else None
        result["segment"] = seg
        result["category"] = segment_category(seg)
        result["decoded"] = decode_segment(seg, words, layouts)
        return result

    if module == "iparser":
        import importlib.util

        mod_path = HERE.parent / "iparser" / "decode.py"
        if not mod_path.is_file():
            result["decoded"] = None
            result["placeholder"] = True
            result["message"] = "iparser 解析器未生成"
            return result
        spec = importlib.util.spec_from_file_location("iparser_decode", mod_path)
        if spec is None or spec.loader is None:
            raise DecodeError("无法加载 iparser 解析器")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.decode_paste(
            text,
            module,
            layouts,
            segment=segment or "iparser_trace",
            mau=mau,
        )

    if module in ("eparser", "pedt"):
        import importlib.util

        mod_path = HERE.parent / "eparser" / "decode.py"
        if not mod_path.is_file():
            result["decoded"] = None
            result["placeholder"] = True
            result["message"] = "eparser/pedt 解析器未生成"
            return result
        spec = importlib.util.spec_from_file_location("eparser_pedt_decode", mod_path)
        if spec is None or spec.loader is None:
            raise DecodeError("无法加载 eparser/pedt 解析器")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.decode_paste(
            text,
            module,
            None,
            segment=segment
            or ("eparser_trace" if module == "eparser" else "pedt_trace"),
            mau=mau,
        )

    raise DecodeError(f"未知模块: {module}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="解码一段 Domain hex")
    ap.add_argument("-y", "--yaml", default=str(DEFAULT_YAML))
    ap.add_argument("-m", "--module", default="mau", choices=["mau", "mpl", "iparser", "eparser", "pedt"])
    ap.add_argument("-s", "--segment", default="cls")
    ap.add_argument("--mau", type=int, default=None)
    ap.add_argument("hexfile", nargs="?", help="含 hex 的文件；缺省读 stdin")
    args = ap.parse_args()
    layouts = load_layouts(args.yaml)
    text = Path(args.hexfile).read_text(encoding="utf-8", errors="replace") if args.hexfile else __import__("sys").stdin.read()
    try:
        out = decode_paste(text, args.module, layouts, segment=args.segment, mau=args.mau)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except DecodeError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), flush=True)
        raise SystemExit(1)
