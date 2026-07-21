"""Tests for check_repo_sync_guard(), the fail-fast repository-state guard
in run_portfolio_check.sh. No shell-testing framework is introduced — the
guard is a small, sourceable bash function, so it's exercised the same way
every other module in this repo is: via subprocess, over disposable git
repos built in tmp_path. It never touches this actual repository's git
state.

Covers exactly the four documented conditions: current branch is main, the
working tree is clean, origin/main exists locally, and local HEAD equals
origin/main — plus the pass-through case where all four hold.
"""

import subprocess
from pathlib import Path

import pytest

SCRIPT = str(Path(__file__).resolve().parent / "run_portfolio_check.sh")


def _git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"git {args} failed: {result.stderr}"
    return result.stdout


def _make_synced_repo(tmp_path):
    """A local repo on main, clean, pushed to and fetched from a bare
    'origin' remote — i.e. every guard condition holds."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "init", "-b", "main", str(local)], check=True, capture_output=True)
    _git(local, "config", "user.email", "test@example.com")
    _git(local, "config", "user.name", "Test")
    (local / "file.txt").write_text("hello\n")
    _git(local, "add", "file.txt")
    _git(local, "commit", "-m", "initial")
    _git(local, "remote", "add", "origin", str(remote))
    _git(local, "push", "-u", "origin", "main")
    return local


def _run_guard(repo):
    return subprocess.run(
        ["bash", "-c", f"source {SCRIPT!r}; check_repo_sync_guard"],
        cwd=str(repo), capture_output=True, text=True,
    )


def test_guard_passes_when_synced_clean_on_main(tmp_path):
    repo = _make_synced_repo(tmp_path)
    result = _run_guard(repo)
    assert result.returncode == 0, result.stderr
    assert "Repository state OK" in result.stdout


def test_guard_fails_when_not_on_main(tmp_path):
    repo = _make_synced_repo(tmp_path)
    _git(repo, "checkout", "-b", "other-branch")

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "not on main" in result.stderr
    assert "git checkout main" in result.stderr


def test_guard_fails_when_working_tree_dirty(tmp_path):
    repo = _make_synced_repo(tmp_path)
    (repo / "file.txt").write_text("modified\n")

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "working-tree changes or untracked files present" in result.stderr


def test_guard_fails_when_working_tree_has_untracked_file(tmp_path):
    repo = _make_synced_repo(tmp_path)
    (repo / "untracked.txt").write_text("new\n")

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "working-tree changes or untracked files present" in result.stderr


def test_guard_fails_when_origin_main_missing(tmp_path):
    local = tmp_path / "local"
    subprocess.run(["git", "init", "-b", "main", str(local)], check=True, capture_output=True)
    _git(local, "config", "user.email", "test@example.com")
    _git(local, "config", "user.name", "Test")
    (local / "file.txt").write_text("hello\n")
    _git(local, "add", "file.txt")
    _git(local, "commit", "-m", "initial")
    # No remote configured at all -> refs/remotes/origin/main can't exist.

    result = _run_guard(local)

    assert result.returncode != 0
    assert "origin/main does not exist locally" in result.stderr
    assert "git fetch origin main" in result.stderr


def test_guard_fails_when_head_ahead_of_origin_main(tmp_path):
    repo = _make_synced_repo(tmp_path)
    (repo / "file2.txt").write_text("second\n")
    _git(repo, "add", "file2.txt")
    _git(repo, "commit", "-m", "unpushed local commit")

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "does not match origin/main" in result.stderr
    assert "git fetch origin main && git pull --ff-only origin main" in result.stderr


def test_guard_fails_when_head_behind_origin_main(tmp_path):
    """The guard never fetches on its own, so it can only detect drift it's
    already been told about. This models the real 'behind' case: something
    (e.g. `git fetch`) has already updated the local origin/main tracking
    ref, but local main itself hasn't been fast-forwarded to it yet."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    other = tmp_path / "other"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "init", "-b", "main", str(local)], check=True, capture_output=True)
    _git(local, "config", "user.email", "test@example.com")
    _git(local, "config", "user.name", "Test")
    (local / "file.txt").write_text("hello\n")
    _git(local, "add", "file.txt")
    _git(local, "commit", "-m", "initial")
    _git(local, "remote", "add", "origin", str(remote))
    _git(local, "push", "-u", "origin", "main")

    # A second clone pushes a new commit that `local` then fetches (updating
    # its origin/main tracking ref) but does not merge into its own main.
    subprocess.run(["git", "clone", str(remote), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "test@example.com")
    _git(other, "config", "user.name", "Test")
    (other / "file3.txt").write_text("third\n")
    _git(other, "add", "file3.txt")
    _git(other, "commit", "-m", "commit from elsewhere")
    _git(other, "push", "origin", "main")
    _git(local, "fetch", "origin", "main")

    result = _run_guard(local)

    assert result.returncode != 0
    assert "does not match origin/main" in result.stderr


def test_guard_does_not_detect_unfetched_remote_drift(tmp_path):
    """Documents an intentional limitation: the guard makes no network call
    and never runs `git fetch`, so it cannot see remote-side commits it was
    never told about — it only catches drift already reflected in the local
    origin/main tracking ref. Staying synchronized (running `git fetch`/
    `git pull` before invoking this script) is the operator/agent's
    responsibility, per CLAUDE.md's git sync doctrine."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    other = tmp_path / "other"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "init", "-b", "main", str(local)], check=True, capture_output=True)
    _git(local, "config", "user.email", "test@example.com")
    _git(local, "config", "user.name", "Test")
    (local / "file.txt").write_text("hello\n")
    _git(local, "add", "file.txt")
    _git(local, "commit", "-m", "initial")
    _git(local, "remote", "add", "origin", str(remote))
    _git(local, "push", "-u", "origin", "main")

    # A second clone pushes a new commit that `local` never fetches.
    subprocess.run(["git", "clone", str(remote), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "test@example.com")
    _git(other, "config", "user.name", "Test")
    (other / "file3.txt").write_text("third\n")
    _git(other, "add", "file3.txt")
    _git(other, "commit", "-m", "commit from elsewhere")
    _git(other, "push", "origin", "main")

    result = _run_guard(local)

    assert result.returncode == 0, result.stderr
    assert "Repository state OK" in result.stdout


def test_script_runs_only_guard_when_sourced_not_executed(tmp_path):
    """Sourcing the script must not fall through into venv setup / pytest /
    Alpaca checks — only check_repo_sync_guard should be defined."""
    repo = _make_synced_repo(tmp_path)
    result = subprocess.run(
        ["bash", "-c", f"source {SCRIPT!r}; echo SOURCED_OK; type check_repo_sync_guard >/dev/null && echo FUNC_DEFINED"],
        cwd=str(repo), capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "SOURCED_OK" in result.stdout
    assert "FUNC_DEFINED" in result.stdout
    assert ".venv" not in result.stdout
