"""Local-only HTTP server for the dashboard.

Binds 127.0.0.1 by default (never 0.0.0.0). Rebuilds the dashboard from current
repository state on each request so a browser refresh reflects the latest
committed/working state without writing any file. Serves nothing but the
generated HTML — no file-system browsing, no upload, no mutation endpoint,
no order path.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .model import build_model
from .render import render_html


def _make_handler(repo_root: Path):
    class DashboardHandler(BaseHTTPRequestHandler):
        server_version = "PortfolioHQDashboard/1.0"

        def _render(self) -> bytes:
            model = build_model(repo_root)
            return render_html(model).encode("utf-8")

        def do_GET(self):  # noqa: N802 (stdlib naming)
            if self.path not in ("/", "/index.html"):
                self.send_error(404, "Only the dashboard root is served.")
                return
            try:
                body = self._render()
            except Exception as exc:  # pragma: no cover - defensive
                self.send_error(500, f"Dashboard render failed: {exc}")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        # Read-only: reject every mutating method explicitly.
        def do_POST(self):  # noqa: N802
            self.send_error(405, "Read-only dashboard: no POST.")

        do_PUT = do_DELETE = do_PATCH = do_POST  # noqa: N815

        def log_message(self, fmt, *args):  # keep the console quiet-ish
            return

    return DashboardHandler


def serve(repo_root: Path | str, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start the local server (blocking). Ctrl-C to stop."""
    repo_root = Path(repo_root).resolve()
    handler = _make_handler(repo_root)
    httpd = ThreadingHTTPServer((host, port), handler)
    bound_host, bound_port = httpd.server_address[0], httpd.server_address[1]
    print(f"Portfolio-HQ dashboard serving at http://{bound_host}:{bound_port}")
    print(f"Repository root: {repo_root}")
    print("Read-only. Press Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard server.")
    finally:
        httpd.server_close()
