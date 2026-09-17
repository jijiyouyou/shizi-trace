#!/usr/bin/env python3
"""将 mau / iparser / eparser+pedt yaml 嵌入生成离线 trace_viewer.html。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAU_DIR = HERE / "mau"
IPARSER_DIR = HERE / "iparser"
EPARSER_DIR = HERE / "eparser"
if str(MAU_DIR) not in sys.path:
    sys.path.insert(0, str(MAU_DIR))

from decode import DEFAULT_YAML, layouts_to_json, load_layouts  # noqa: E402

TEMPLATE = HERE / "viewer_template.html"
DEFAULT_OUT = HERE / "trace_viewer.html"
IPARSER_YAML = HERE.parent / "iparser_trace.yaml"
EPARSER_YAML = HERE.parent / "eparser_pedt_fields.yaml"


def _load_side_layouts(decode_path: Path, yaml_path: Path, mod_name: str) -> dict:
    spec = importlib.util.spec_from_file_location(mod_name, decode_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"无法加载 {decode_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.load_layouts(yaml_path)


def build(
    yaml_path: Path | None = None,
    out_path: Path | None = None,
    result_json: Path | None = None,
    iparser_yaml: Path | None = None,
    eparser_yaml: Path | None = None,
) -> Path:
    layouts = load_layouts(yaml_path or DEFAULT_YAML)
    iparser_layouts = _load_side_layouts(
        IPARSER_DIR / "decode.py",
        iparser_yaml or IPARSER_YAML,
        "trace_view_iparser_decode_build",
    )
    eparser_layouts = _load_side_layouts(
        EPARSER_DIR / "decode.py",
        eparser_yaml or EPARSER_YAML,
        "trace_view_eparser_decode_build",
    )
    tpl = TEMPLATE.read_text(encoding="utf-8")
    layouts_js = layouts_to_json(layouts)
    iparser_js = json.dumps(iparser_layouts, ensure_ascii=False, separators=(",", ":"))
    eparser_js = json.dumps(eparser_layouts, ensure_ascii=False, separators=(",", ":"))
    result_js = "null"
    if result_json:
        data = json.loads(Path(result_json).read_text(encoding="utf-8"))
        result_js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    html = (
        tpl.replace("__LAYOUTS_JSON__", layouts_js)
        .replace("__IPARSER_LAYOUTS_JSON__", iparser_js)
        .replace("__EPARSER_LAYOUTS_JSON__", eparser_js)
        .replace("__RESULT_JSON__", result_js)
    )
    out = out_path or DEFAULT_OUT
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="生成 Trace Viewer HTML")
    ap.add_argument("-y", "--yaml", default=str(DEFAULT_YAML), help="mau_trace.yaml 路径")
    ap.add_argument(
        "--iparser-yaml",
        default=str(IPARSER_YAML),
        help="iparser_trace.yaml 路径",
    )
    ap.add_argument(
        "--eparser-yaml",
        default=str(EPARSER_YAML),
        help="eparser_pedt_fields.yaml 路径",
    )
    ap.add_argument("-o", "--output", default=str(DEFAULT_OUT), help="输出 HTML")
    ap.add_argument("-i", "--input", dest="result", default=None, help="预解析 result.json")
    args = ap.parse_args()
    path = build(
        yaml_path=Path(args.yaml),
        out_path=Path(args.output),
        result_json=Path(args.result) if args.result else None,
        iparser_yaml=Path(args.iparser_yaml),
        eparser_yaml=Path(args.eparser_yaml),
    )
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
