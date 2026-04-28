from __future__ import annotations

import argparse
import socket
import threading
import time
import urllib.parse
import webbrowser

import uvicorn

from .server import app


def _find_free_port(start: int = 8765) -> int:
    port = start
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="filesizer",
        description="Browser-based file size visualizer",
    )
    parser.add_argument("path", nargs="?", default=None, help="Directory to open on startup")
    args = parser.parse_args()

    port = _find_free_port()
    url = f"http://127.0.0.1:{port}"
    if args.path:
        url += f"?path={urllib.parse.quote(args.path)}"

    print(f"Starting filesizer at {url}")

    def _open_browser() -> None:
        time.sleep(1.2)
        webbrowser.open(url)

    threading.Thread(target=_open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")