#!/usr/bin/env python3
"""可选本地 HTTP 服务：提供 trace_viewer.html，并支持 /api/parse 解码。"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent  # view/mau
VIEW_DIR = HERE.parent                  # view/
if str(VIEW_DIR) not in sys.path:
    sys.path.insert(0, str(VIEW_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from build_viewer import build  # noqa: E402
from decode import DecodeError, decode_paste, load_layouts  # noqa: E402
from logparse import parse_log  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Trace View 本地服务")
    ap.add_argument("-p", "--port", type=int, default=8765)
    ap.add_argument("--no-build", action="store_true", help="不重新生成 HTML")
    args = ap.parse_args()

    if not args.no_build:
        build()
    html_path = VIEW_DIR / "trace_viewer.html"
    if not html_path.is_file():
        raise SystemExit("缺少 trace_viewer.html，请先运行 view/build_viewer.py")

    layouts = load_layouts()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *a) -> None:
            print("%s - %s" % (self.address_string(), fmt % a))

        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path in ("/", "/index.html", "/trace_viewer.html"):
                data = html_path.read_bytes()
                self._send(200, data, "text/html; charset=utf-8")
                return
            self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                req = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                self._send(400, b'{"error":"invalid json"}', "application/json")
                return

            try:
                if path == "/api/parse":
                    text = req.get("text") or ""
                    mode = (req.get("mode") or "auto").lower()
                    if mode == "auto":
                        out = parse_log(text, layouts)
                    else:
                        out = decode_paste(
                            text,
                            mode,
                            layouts,
                            segment=req.get("segment") or "cls",
                            mau=req.get("mau"),
                        )
                    body = json.dumps(out, ensure_ascii=False).encode("utf-8")
                    self._send(200, body, "application/json; charset=utf-8")
                    return
                self._send(404, b'{"error":"not found"}', "application/json")
            except DecodeError as e:
                body = json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Trace View  http://127.0.0.1:{args.port}/")
    print("Ctrl+C 退出")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
