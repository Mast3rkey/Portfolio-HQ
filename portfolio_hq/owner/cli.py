"""Command-line surface for the private owner interface.

    # 1. Build the presentation export from an accepted repository state.
    python -m portfolio_hq.owner export --output var/owner/export.json

    # 2. Serve it privately (a token is mandatory — see docs).
    PORTFOLIO_HQ_OWNER_TOKEN=... python -m portfolio_hq.owner serve \
        --export var/owner/export.json --inbox var/owner/inbox

``export`` reads repository state and writes exactly the one output file it is
given. ``serve`` never reads repository state at all: it reads the export file
and the inbox directory, and writes only inside the inbox.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# The repository root is the parent of the `portfolio_hq` package directory.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPORT = "var/owner/export.json"
DEFAULT_INBOX = "var/owner/inbox"


def cmd_export(args: argparse.Namespace) -> int:
    # Imported here, not at module scope: `serve` must never pull the
    # build-time half (and therefore the investment code) into a hosted
    # process. See portfolio_hq/owner/__init__.py.
    from .export import build_owner_export
    from .export_io import write_export

    repo_root = Path(args.repo_root).resolve()
    export = build_owner_export(repo_root)
    out = Path(args.output)
    if not out.is_absolute():
        out = repo_root / out
    write_export(out, export)

    meta = export["meta"]
    attention = export["attention"]
    print(f"Wrote {out}")
    print(f"  source commit: {meta.get('source_commit') or 'unknown'}"
          f"{' (dirty worktree)' if meta.get('worktree_dirty') else ''}")
    print(f"  generated:     {meta.get('generated_at')}")
    print(f"  attention:     {len(attention['blockers'])} blocker(s), "
          f"{len(attention['warnings'])} warning(s)")
    print("  Recommendation-only presentation export. No order path, no "
          "brokerage connection, no repository mutation.")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from . import auth as auth_mod
    from .service import serve

    export_path = Path(args.export)
    inbox_root = Path(args.inbox)
    try:
        serve(inbox_root=inbox_root, export_path=export_path,
              host=args.host, port=args.port, analysis_path=args.chart_analysis,
              review_path=args.chart_review)
    except auth_mod.OwnerAuthNotConfigured as exc:
        # Fail closed and say exactly why, rather than starting an
        # unauthenticated instance that would expose private information.
        print(f"Refusing to start: {exc}", file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m portfolio_hq.owner",
        description="Private Portfolio-HQ owner interface and chart inbox "
                    "(recommendation-only; no brokerage connection, no order path).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    e = sub.add_parser("export", help="Build the presentation export from repository state.")
    e.add_argument("--repo-root", default=str(REPO_ROOT),
                   help="Repository root to read from (default: this repo).")
    e.add_argument("--output", default=DEFAULT_EXPORT,
                   help=f"Export output path (default: {DEFAULT_EXPORT}).")
    e.set_defaults(func=cmd_export)

    s = sub.add_parser("serve", help="Serve the private owner interface.")
    s.add_argument("--export", default=DEFAULT_EXPORT,
                   help=f"Presentation export to serve (default: {DEFAULT_EXPORT}). "
                        "A missing export is shown honestly as unavailable; the "
                        "chart inbox still works.")
    s.add_argument("--inbox", default=DEFAULT_INBOX,
                   help=f"Chart inbox directory (default: {DEFAULT_INBOX}). This is "
                        "the only path the service writes to.")
    s.add_argument("--chart-analysis", default=None,
                   help="Optional operator-provisioned private chart analysis JSON; read only.")
    s.add_argument("--chart-review", default=None,
                   help="Optional separately provisioned independent review JSON; read only.")
    s.add_argument("--host", default="127.0.0.1",
                   help="Bind host (default: 127.0.0.1). A non-loopback bind is "
                        "supported for private hosting and requires TLS "
                        "termination in front of this process.")
    s.add_argument("--port", type=int, default=8080, help="Bind port (default: 8080).")
    s.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
