"""Pedt 解码入口：复用 view/eparser/decode.py（同一 eparser_pedt_fields.yaml）。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / "eparser" / "decode.py"
_spec = importlib.util.spec_from_file_location("trace_view_eparser_decode_pedt", _path)
if _spec is None or _spec.loader is None:
    raise SystemExit(f"无法加载 {_path}")
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)

DecodeError = _mod.DecodeError
DEFAULT_YAML = _mod.DEFAULT_YAML
load_layouts = _mod.load_layouts
layouts_to_json = _mod.layouts_to_json
parse_u32_tokens = _mod.parse_u32_tokens
decode_trace = _mod.decode_trace
decode_segment = _mod.decode_segment
decode_paste = _mod.decode_paste
parse_log = _mod.parse_log
collect_module_words = _mod.collect_module_words
is_module_block_name = _mod.is_module_block_name
