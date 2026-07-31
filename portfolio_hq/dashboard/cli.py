"""Command-line surface for the dashboard: `build` and `serve`.

    python -m portfolio_hq.dashboard build --output reports/generated/portfolio_hq_dashboard.html
    python -m portfolio_hq.dashboard serve --host 127.0.0.1 --port 8000

Read-only throughout. `build` writes exactly one generated HTML file to the
path you give (a gitignored location by convention). `serve` writes nothing.
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from pathlib import Path

from .model import build_model
from .render import render_html
from .server import serve

# The repository root is the parent of the `portfolio_hq` package directory.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = "reports/generated/portfolio_hq_dashboard.html"

_HOST_ERROR = (
    "--host must be a loopback address ('127.0.0.1', '::1', or 'localhost') "
    "— got {value!r}. Binding to 0.0.0.0, a LAN address, or any other "
    "externally reachable interface is not authorized for this dashboard "
    "(OPS-0011 sections 2.4 and 5: not a default, an option, or a "
    "configurable setting)."
)


def _loopback_host(value: str) -> str:
    """argparse `type=` validator: reject any --host that isn't loopback-only."""
    if value == "localhost":
        return value
    try:
        addr = ipaddress.ip_address(value)
    except ValueError:
        raise argparse.ArgumentTypeError(_HOST_ERROR.format(value=value)) from None
    if not addr.is_loopback:
        raise argparse.ArgumentTypeError(_HOST_ERROR.format(value=value))
    return value


def cmd_build(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    model = build_model(repo_root)
    html = render_html(model)

    if args.stdout:
        sys.stdout.write(html)
        return 0

    out = Path(args.output)
    if not out.is_absolute():
        out = repo_root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    p = model.provenance
    print(f"Wrote {out}")
    print(f"  commit: {p.commit_short or 'unknown'} ({'dirty' if p.dirty else 'clean'} worktree)")
    print(f"  generated: {p.generated_at_iso}")
    if model.blockers:
        print(f"  BLOCKERS: {len(model.blockers)} — see the Overview banner.")
    if model.warnings:
        print(f"  warnings: {len(model.warnings)}")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    serve(repo_root, host=args.host, port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m portfolio_hq.dashboard",
        description="Repository-native, read-only Portfolio-HQ dashboard.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help="Repository root to read from (default: this repo).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("build", help="Generate a standalone HTML file.")
    b.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output HTML path (default: {DEFAULT_OUTPUT}).",
    )
    b.add_argument(
        "--stdout",
        action="store_true",
        help="Write HTML to stdout instead of a file (no file written).",
    )
    b.set_defaults(func=cmd_build)

    s = sub.add_parser("serve", help="Serve the dashboard on localhost.")
    s.add_argument(
        "--host",
        default="127.0.0.1",
        type=_loopback_host,
        help="Bind host — loopback only (default: 127.0.0.1). 0.0.0.0/LAN/"
        "external addresses are rejected (OPS-0011).",
    )
    s.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000).")
    s.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
