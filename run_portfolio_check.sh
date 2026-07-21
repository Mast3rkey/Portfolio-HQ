#!/usr/bin/env bash
# run_portfolio_check.sh — one-command phone-session bootstrap + read-only check.
#
# Cloud sessions are ephemeral: each one starts from a fresh clone with no
# .venv and no installed packages. This script rebuilds what's needed, runs
# the test suite, and prints --health + --review (the latter with --no-log,
# so it doesn't write the timestamped allocation log or touch
# performance_log.csv). It never writes portfolio state, never runs an
# update-* subcommand, and never places an order — order-placement methods
# don't exist in alpaca_client.py by design (see CLAUDE.md).
#
# Per CLAUDE.md's "Git sync — automatic, not a request" section, resyncing
# with origin/main is unprompted, first-action behavior, not something the
# operator/agent does by hand — so this script fetches and fast-forwards
# main itself. It still refuses to touch a repo that isn't already clean and
# on main (nothing to safely fast-forward otherwise), and it never resets,
# force-updates, discards, stashes, switches branches, deletes files, or
# overwrites uncommitted work to get there — only a plain fast-forward pull,
# verified afterward to have actually landed on origin/main.
#
# Usage: ./run_portfolio_check.sh

set -euo pipefail

# check_repo_sync_guard — fail-fast repository-state guard + authoritative
# main sync.
#
# 1. Fails before touching git state unless the current branch is main.
# 2. Fails before touching git state if the working tree has tracked or
#    untracked changes.
# 3. Prints that it is fetching and fast-forwarding main.
# 4. Runs the authorized sync: `git fetch origin main --prune` then
#    `git pull --ff-only origin main`.
# 5. Verifies afterward that origin/main exists and local HEAD exactly
#    equals it.
# 6. On any remaining mismatch, prints a concise, truthful diagnostic that
#    distinguishes "local is ahead of origin/main" from "local has
#    diverged from origin/main" from a generic still-behind case, and
#    returns non-zero.
#
# Never resets, force-updates, discards, stashes, switches branches,
# deletes files, or overwrites uncommitted work — the only mutation is the
# plain fetch + fast-forward-only pull in step 4, which by construction
# cannot discard anything (it fails instead).
#
# Defined as a function (rather than inline top-level code) so it can be
# sourced and exercised in isolation by test_run_portfolio_check_guard.py,
# against disposable local repos only, without running the rest of the
# bootstrap.
check_repo_sync_guard() {
    local branch
    branch="$(git branch --show-current)"
    if [ "$branch" != "main" ]; then
        echo "ERROR: not on main (currently: ${branch:-detached HEAD}). Refusing to sync." >&2
        echo "Fix: git checkout main" >&2
        return 1
    fi

    if [ -n "$(git status --porcelain)" ]; then
        echo "ERROR: working-tree changes or untracked files present. Refusing to sync." >&2
        git status --short >&2
        echo "Fix: commit, stash, or remove the changes above, then re-run." >&2
        return 1
    fi

    echo "==> Fetching and fast-forwarding main"
    if ! git fetch origin main --prune; then
        echo "ERROR: 'git fetch origin main' failed. Refusing to proceed." >&2
        echo "Fix: check 'git remote -v' and network connectivity, then re-run." >&2
        return 1
    fi

    if ! git rev-parse --verify --quiet refs/remotes/origin/main >/dev/null; then
        echo "ERROR: origin/main does not exist after fetch. Refusing to proceed." >&2
        echo "Fix: check 'git remote -v' — the fetch appeared to succeed but left no origin/main ref." >&2
        return 1
    fi

    if ! git pull --ff-only origin main; then
        echo "NOTE: fast-forward pull did not complete cleanly; diagnosing exact state below." >&2
    fi

    local local_head origin_main
    local_head="$(git rev-parse HEAD)"
    origin_main="$(git rev-parse refs/remotes/origin/main)"

    if [ "$local_head" = "$origin_main" ]; then
        echo "==> Repository state OK: on main, clean, synchronized with origin/main ($local_head)"
        return 0
    fi

    if git merge-base --is-ancestor origin/main HEAD 2>/dev/null; then
        echo "ERROR: local main ($local_head) is ahead of origin/main ($origin_main) — local commits exist that origin doesn't have. Refusing to proceed." >&2
        echo "This script will not push or otherwise resolve this for you." >&2
    elif git merge-base --is-ancestor HEAD origin/main 2>/dev/null; then
        echo "ERROR: local main ($local_head) is still behind origin/main ($origin_main) after a fast-forward attempt. Refusing to proceed." >&2
        echo "Fix: re-run this script, or manually: git pull --ff-only origin main" >&2
    else
        echo "ERROR: local main ($local_head) has diverged from origin/main ($origin_main) — fast-forward sync is not possible. Refusing to proceed." >&2
        echo "This script will not rebase, reset, or force-update to resolve this for you." >&2
    fi
    return 1
}

# Only run the full bootstrap when executed directly (./run_portfolio_check.sh),
# not when sourced (e.g. by tests wanting check_repo_sync_guard in isolation).
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return 0
fi

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "==> Checking repository state and synchronizing main"
check_repo_sync_guard

echo "==> Setting up .venv (repo-local, never global, never sudo)"
if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip --quiet
.venv/bin/python -m pip install -r requirements.txt --quiet

echo "==> Verifying required imports"
.venv/bin/python -c "
import pandas, numpy, yaml, requests, matplotlib, curl_cffi, yfinance, pytest
print('pandas    ', pandas.__version__)
print('numpy     ', numpy.__version__)
print('yaml      ', yaml.__version__)
print('requests  ', requests.__version__)
print('matplotlib', matplotlib.__version__)
print('curl_cffi ', curl_cffi.__version__)
print('yfinance  ', yfinance.__version__)
print('pytest    ', pytest.__version__)
"

echo "==> Running full test suite (stops here on any failure)"
.venv/bin/python -m pytest -q

echo "==> Checking Alpaca credentials (names only — values are never read here)"
MISSING=()
for v in ALPACA_API_KEY ALPACA_API_SECRET ALPACA_BASE_URL; do
    if [ -z "${!v:-}" ]; then
        MISSING+=("$v")
    fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "STOPPED before any live market-data command."
    echo "Missing environment variable(s): ${MISSING[*]}"
    echo "Set these through Claude Code's environment/secrets configuration —"
    echo "not this script, not a committed .env file, not chat. See:"
    echo "https://code.claude.com/docs/en/claude-code-on-the-web"
    exit 1
fi

echo "==> Verifying Alpaca connectivity and credentials are actually valid"
echo "    (reuses alpaca_client.py's own connectivity diagnostic; no secret values printed)"
if ! .venv/bin/python alpaca_client.py; then
    echo ""
    echo "STOPPED before any read-only report."
    echo "ALPACA_API_KEY/ALPACA_API_SECRET/ALPACA_BASE_URL are all set, but the"
    echo "live connectivity check above failed — the values may be wrong, expired,"
    echo "or ALPACA_BASE_URL may not point at the paper-api endpoint. Re-check"
    echo "them in Claude Code's environment/secrets configuration."
    exit 1
fi

echo "==> Running read-only Health View"
.venv/bin/python allocate.py --health

echo ""
echo "==> Running read-only allocation review"
.venv/bin/python allocate.py --review --no-log

echo ""
echo "==> Done. No update-* command was run. No order was placed."
