"""Read-only helpers for checking frozen studies against their original Git tree."""

from __future__ import annotations

import hashlib
import io
import subprocess
import tarfile
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parent
HISTORICAL_INPUT_COMMIT = "120a2bf89f621c4b50719c3f630fd7b6551b4b45"
ORIGINAL_LOOKTHROUGH_SHA256 = (
    "6cf4e417e747d9a1ae9621e57d238c685ab593fb65539d561a5d136c7027b0b9"
)


def export_historical_tree(
    destination: Path,
    revision: str = HISTORICAL_INPUT_COMMIT,
    expected_lookthrough_sha256: str = ORIGINAL_LOOKTHROUGH_SHA256,
) -> Path:
    """Materialize the registered input tree from verified, tracked Git objects."""

    root = destination / "historical-repository"
    root.mkdir(parents=True)
    archive = subprocess.run(
        ["git", "archive", "--format=tar", revision],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        # The archive is produced locally by Git from a trusted tracked tree.
        stream.extractall(root)
    lookthrough = root / "issuer_lookthrough.yaml"
    assert hashlib.sha256(lookthrough.read_bytes()).hexdigest() == expected_lookthrough_sha256
    return root


def rebase_path_globals(monkeypatch, module: ModuleType, historical_root: Path) -> None:
    """Rebase every repository-rooted module Path, including captured defaults."""

    for name, value in vars(module).items():
        if isinstance(value, Path) and value.is_relative_to(REPOSITORY_ROOT):
            monkeypatch.setattr(
                module, name, historical_root / value.relative_to(REPOSITORY_ROOT)
            )
    path_hash = getattr(module, "market_data_path_hash", None)
    if path_hash is not None:
        monkeypatch.setattr(
            path_hash,
            "__defaults__",
            (historical_root / "research/level1_sleeve_robustness/data/transformed/candidates",),
        )


def historical_bytes(path: str, revision: str = HISTORICAL_INPUT_COMMIT) -> bytes:
    """Return one tracked historical file without consulting working-tree bytes."""

    return subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=REPOSITORY_ROOT,
        check=True, capture_output=True,
    ).stdout
