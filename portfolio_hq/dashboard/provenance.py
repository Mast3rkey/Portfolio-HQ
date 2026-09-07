"""Git provenance + input-file lineage for the dashboard.

Read-only. Shells out to `git` for repository metadata (commit, branch, dirty
status) and hashes the exact input files the dashboard consumed so the rendered
page can state precisely which repository state it reflects. Never runs any git
command that mutates the repository (only rev-parse / status / log / branch).
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class InputFile:
    """One authoritative input the dashboard read, with a content hash so the
    page can prove exactly what it displayed."""

    path: str  # repo-relative path
    exists: bool
    sha256: str | None  # short (first 12) sha256 of file bytes, None if absent
    size_bytes: int | None


@dataclass(frozen=True)
class Provenance:
    repo_name: str
    branch: str | None
    commit_sha: str | None  # full 40-char sha
    commit_short: str | None
    commit_iso: str | None  # committer date, ISO 8601
    commit_subject: str | None
    dirty: bool  # True if the worktree had uncommitted changes at generation
    dirty_paths: tuple[str, ...]  # porcelain lines when dirty (capped)
    generated_at_iso: str  # UTC generation timestamp (the one non-deterministic field)
    git_available: bool
    inputs: tuple[InputFile, ...] = field(default_factory=tuple)

    @property
    def commit_display(self) -> str:
        return self.commit_sha or "(unknown — git metadata unavailable)"


def _git(repo_root: Path, *args: str) -> str | None:
    """Run a read-only git command; return stripped stdout or None on failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def _short_sha256(path: Path) -> tuple[str | None, int | None]:
    try:
        data = path.read_bytes()
    except OSError:
        return None, None
    return hashlib.sha256(data).hexdigest()[:12], len(data)


def collect_inputs(repo_root: Path, rel_paths: list[str]) -> tuple[InputFile, ...]:
    """Hash each declared input file (repo-relative). Missing files are recorded
    as absent rather than raising — the dashboard must render even when some
    inputs are incomplete."""
    inputs: list[InputFile] = []
    for rel in rel_paths:
        p = repo_root / rel
        if p.exists() and p.is_file():
            sha, size = _short_sha256(p)
            inputs.append(InputFile(path=rel, exists=True, sha256=sha, size_bytes=size))
        else:
            inputs.append(InputFile(path=rel, exists=False, sha256=None, size_bytes=None))
    return tuple(inputs)


def collect_provenance(
    repo_root: Path,
    input_rel_paths: list[str],
    *,
    now: datetime | None = None,
) -> Provenance:
    """Gather git provenance and input lineage. `now` is injectable so tests can
    pin the single non-deterministic field (generation time)."""
    repo_root = Path(repo_root).resolve()
    generated_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    branch = _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    commit_sha = _git(repo_root, "rev-parse", "HEAD")
    git_available = commit_sha is not None

    commit_short = commit_sha[:7] if commit_sha else None
    commit_iso = _git(repo_root, "log", "-1", "--format=%cI") if git_available else None
    commit_subject = _git(repo_root, "log", "-1", "--format=%s") if git_available else None

    porcelain = _git(repo_root, "status", "--porcelain") if git_available else None
    dirty_lines = [ln for ln in (porcelain or "").splitlines() if ln.strip()]
    dirty = bool(dirty_lines)

    return Provenance(
        repo_name=repo_root.name,
        branch=branch,
        commit_sha=commit_sha,
        commit_short=commit_short,
        commit_iso=commit_iso,
        commit_subject=commit_subject,
        dirty=dirty,
        dirty_paths=tuple(dirty_lines[:40]),
        generated_at_iso=generated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        git_available=git_available,
        inputs=collect_inputs(repo_root, input_rel_paths),
    )
