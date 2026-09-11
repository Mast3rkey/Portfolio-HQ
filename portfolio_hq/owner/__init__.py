"""portfolio_hq.owner — the private owner interface and chart inbox.

Two halves, one deliberate trust boundary
-----------------------------------------
**Build-time (trusted, in-repository).** ``export.build_owner_export`` runs
beside the repository, reuses Portfolio-HQ's own canonical calculations
(``dashboard.model.build_model``, ``level1_policy_summary``, ``allocate``'s
observation classifiers and protected-capital weights) and emits one JSON
presentation export. It computes no new portfolio number and implements no
second allocator.

**Runtime (hosted, minimal).** ``service`` serves that JSON to an
authenticated owner and accepts chart images into ``chart_inbox``. It imports
no investment code, reads only the export file and the inbox directory, and
writes only inside the inbox. It cannot produce a portfolio figure of its own.

Hard boundaries
---------------
* Authentication is mandatory on every host. Missing configuration means the
  service refuses to start, never anonymous access.
* Chart intake is evidence receipt, not adoption: an uploaded image is
  quarantined as unreviewed and changes no holding, target, sleeve weight,
  policy, cap, cluster, margin setting, recommendation or Stage-1 state.
* No brokerage connection, no credential use, no order path, anywhere.
* ``portfolio_hq.dashboard`` is untouched by this package and remains
  loopback-only, GET-only and read-only.
"""

from .export_io import EXPORT_SCHEMA_VERSION, load_export, write_export

__all__ = [
    "EXPORT_SCHEMA_VERSION",
    "build_owner_export",
    "load_export",
    "write_export",
]


def __getattr__(name: str):
    """Expose ``build_owner_export`` lazily (PEP 562).

    Importing it eagerly here would drag the build-time half — and through it
    ``allocate``, ``pandas`` and the brokerage client module — into every
    process that merely imports ``portfolio_hq.owner.service``. Python executes
    a package's ``__init__`` before any submodule, so an eager import here
    would silently dissolve the trust boundary this package is built around.
    """
    if name == "build_owner_export":
        from .export import build_owner_export

        return build_owner_export
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
