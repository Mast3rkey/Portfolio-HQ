"""Read/write side of the presentation export — standard library only.

Deliberately separate from ``export.py``. Building an export needs the
repository's canonical investment code; *consuming* one needs nothing but
``json``. Keeping the reader here is what lets the hosted service load an
export without importing ``allocate``, ``pandas``, a brokerage client, or the
dashboard model — see the trust-boundary note in ``service.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

EXPORT_SCHEMA_VERSION = 1


def write_export(path: Path | str, export: dict) -> Path:
    """Write the export as deterministic JSON. Returns the path written."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(export, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return out


def load_export(path: Path | str) -> dict | None:
    """Read an export, or ``None`` if it is missing, unreadable or the wrong
    schema version.

    Returning ``None`` rather than raising is deliberate: the hosted service
    must still start, still authenticate, and still accept chart intake when
    the presentation export is absent — showing an honest "not available yet"
    state instead of a number it does not have.
    """
    try:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("schema_version") != EXPORT_SCHEMA_VERSION:
        return None
    return loaded
