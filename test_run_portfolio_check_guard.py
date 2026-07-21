"""Tests for check_repo_sync_guard(), the fail-fast repository-state guard
and authoritative main-sync function in run_portfolio_check.sh. No shell-
testing framework is introduced — the guard is a small, sourceable bash
function, so it's exercised the same way every other module in this repo
is: via subprocess, over disposable local git repositories (a working repo
plus a bare "remote") built fresh in tmp_path. Every repo here is local
filesystem only — no external network, and the real Portfolio-HQ repo and
its git state are never touched.

Per CLAUDE.md's "Git sync — automatic, not a request" section, resyncing
with origin/main is unprompted, first-action behavior — so the guard
itself performs `git fetch origin main --prune` then
`git pull --ff-only origin main`, and only then verifies (rather than
assumes) that local HEAD equals origin/main afterward. Covers: fails
before touching git state for the wrong branch or a dirty tree; discovers
and fast-forwards an unfetched remote commit; local-ahead and diverged
cases fail the post-sync equality assertion with distinct diagnostics
instead of being described as synchronized; missing/invalid origin fails
clearly; sourcing only defines functions.
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


def _init_local(path):
    subprocess.run(["git", "init", "-b", "main", str(path)], check=True, capture_output=True)
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "Test")


def _commit_file(repo, name, content, message):
    (repo / name).write_text(content)
    _git(repo, "add", name)
    _git(repo, "commit", "-m", message)


def _make_synced_repo(tmp_path):
    """A local repo on main, clean, pushed to and fetched from a bare
    'origin' remote — i.e. every guard condition already holds."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    _init_local(local)
    _commit_file(local, "file.txt", "hello\n", "initial")
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
    assert "Fetching and fast-forwarding main" in result.stdout
    assert "Repository state OK" in result.stdout


def test_guard_fails_when_not_on_main_before_fetch(tmp_path):
    repo = _make_synced_repo(tmp_path)
    _git(repo, "checkout", "-b", "other-branch")
    # Point origin somewhere that can't be fetched, so if the guard fetched
    # before checking the branch, it would fail with a *different* error.
    _git(repo, "remote", "set-url", "origin", str(tmp_path / "does-not-exist.git"))

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "not on main" in result.stderr
    assert "git checkout main" in result.stderr
    assert "git fetch" not in result.stderr


def test_guard_fails_when_working_tree_dirty_before_fetch(tmp_path):
    repo = _make_synced_repo(tmp_path)
    (repo / "file.txt").write_text("modified\n")
    _git(repo, "remote", "set-url", "origin", str(tmp_path / "does-not-exist.git"))

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "working-tree changes or untracked files present" in result.stderr
    assert "git fetch" not in result.stderr


def test_guard_fails_when_working_tree_has_untracked_file_before_fetch(tmp_path):
    repo = _make_synced_repo(tmp_path)
    (repo / "untracked.txt").write_text("new\n")
    _git(repo, "remote", "set-url", "origin", str(tmp_path / "does-not-exist.git"))

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "working-tree changes or untracked files present" in result.stderr
    assert "git fetch" not in result.stderr


def test_guard_discovers_and_fastforwards_unfetched_remote_commit(tmp_path):
    """The core restored behavior: a commit pushed by someone else, which
    `local` has never fetched, is discovered and local main is
    automatically fast-forwarded to it."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    other = tmp_path / "other"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    _init_local(local)
    _commit_file(local, "file.txt", "hello\n", "initial")
    _git(local, "remote", "add", "origin", str(remote))
    _git(local, "push", "-u", "origin", "main")

    subprocess.run(["git", "clone", str(remote), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "test@example.com")
    _git(other, "config", "user.name", "Test")
    _commit_file(other, "file3.txt", "third\n", "commit from elsewhere")
    _git(other, "push", "origin", "main")

    new_remote_sha = _git(other, "rev-parse", "HEAD").strip()
    assert _git(local, "rev-parse", "HEAD").strip() != new_remote_sha

    result = _run_guard(local)

    assert result.returncode == 0, result.stderr
    assert "Repository state OK" in result.stdout
    assert _git(local, "rev-parse", "HEAD").strip() == new_remote_sha


def test_guard_fails_when_local_ahead_of_origin_main(tmp_path):
    repo = _make_synced_repo(tmp_path)
    _commit_file(repo, "file2.txt", "second\n", "unpushed local commit")

    result = _run_guard(repo)

    assert result.returncode != 0
    assert "Repository state OK" not in result.stdout
    assert "is ahead of origin/main" in result.stderr


def test_guard_fails_when_diverged(tmp_path):
    """Local and origin/main each have a commit the other lacks — a plain
    fast-forward sync is impossible, so the guard must fail safely rather
    than force/reset/rebase anything."""
    remote = tmp_path / "remote.git"
    local = tmp_path / "local"
    other = tmp_path / "other"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True, capture_output=True)
    _init_local(local)
    _commit_file(local, "file.txt", "hello\n", "initial")
    _git(local, "remote", "add", "origin", str(remote))
    _git(local, "push", "-u", "origin", "main")

    subprocess.run(["git", "clone", str(remote), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "test@example.com")
    _git(other, "config", "user.name", "Test")
    _commit_file(other, "file3.txt", "third\n", "commit from elsewhere")
    _git(other, "push", "origin", "main")

    _commit_file(local, "file2.txt", "second\n", "unpushed divergent local commit")

    result = _run_guard(local)

    assert result.returncode != 0
    assert "Repository state OK" not in result.stdout
    assert "has diverged from origin/main" in result.stderr


def test_guard_fails_clearly_when_origin_missing(tmp_path):
    local = tmp_path / "local"
    _init_local(local)
    _commit_file(local, "file.txt", "hello\n", "initial")
    # No remote named "origin" configured at all.

    result = _run_guard(local)

    assert result.returncode != 0
    assert "git fetch origin main" in result.stderr
    assert "failed" in result.stderr


def test_guard_fails_clearly_when_origin_invalid(tmp_path):
    local = tmp_path / "local"
    _init_local(local)
    _commit_file(local, "file.txt", "hello\n", "initial")
    _git(local, "remote", "add", "origin", str(tmp_path / "does-not-exist.git"))

    result = _run_guard(local)

    assert result.returncode != 0
    assert "git fetch origin main" in result.stderr
    assert "failed" in result.stderr


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
