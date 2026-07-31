"""portfolio_hq.dashboard — repository-native read-only dashboard.

Public entry points:
    build_model(repo_root)  -> DashboardModel   (model.py)
    render_html(model)      -> str              (render.py)
    build command / serve command               (cli.py, __main__.py)

Hard boundaries (enforced by construction, not convention):
  * Reads only repository files + local `git` metadata. No network. No Alpaca.
    No Robinhood. No credentials.
  * Never writes any authoritative file. `build` writes exactly one generated
    HTML artifact to an explicitly-provided output path (gitignored location by
    convention). `serve` writes nothing.
  * Produces no order, buy/sell control, or mutation endpoint. Any advisory
    language shown originates from repository content and is labelled advisory.
"""

from .model import DashboardModel, build_model
from .render import render_html

__all__ = ["DashboardModel", "build_model", "render_html"]
