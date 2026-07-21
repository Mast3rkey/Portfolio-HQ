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
# It also never fetches or syncs git state on its own: it fails fast if the
# repo isn't already on a clean, synchronized main (see check_repo_sync_guard
# below) and tells you the exact command to run instead of running it for
# you. Per CLAUDE.md's git sync doctrine, resyncing with origin/main is a
# deliberate, visible action, not something this script does silently.
#
# Usage: ./run_portfolio_check.sh

set -euo pipefail

# check_repo_sync_guard — fail-fast repository-state guard.
#
# Verifies the repo is starting from a synchronized 'main' before anything
# else runs: current branch is main, the working tree is clean, origin/main
# exists locally, and local HEAD equals origin/main. It only inspects
# existing git state (whatever origin/main was last fetched to, e.g. by the
# initial clone) — it never fetches, resets, discards, stashes, switches
# branches, or otherwise mutates the repository. On any failed condition it
# prints a concise, actionable fix and returns non-zero; per CLAUDE.md's git
# sync doctrine ("no session's local copy is authoritative"), resyncing is
# an explicit, visible action the operator/agent takes, not something this
# script does silently on their behalf.
#
# Defined as a function (rather than inline top-level code) so it can be
# sourced and exercised in isolation by test_run_portfolio_check_guard.py
# without running the rest of the bootstrap.
check_repo_sync_guard() {
    local branch
    branch="$(git branch --show-current)"
    if [ "$branch" != "main" ]; then
        echo "ERROR: not on main (currently: ${branch:-detached HEAD}). Refusing to proceed." >&2
        echo "Fix: git checkout main" >&2
        return 1
    fi

    if [ -n "$(git status --porcelain)" ]; then
        echo "ERROR: working-tree changes or untracked files present. Refusing to proceed." >&2
        git status --short >&2
        echo "Fix: commit, stash, or remove the changes above, then re-run." >&2
        return 1
    fi

    if ! git rev-parse --verify --quiet refs/remotes/origin/main >/dev/null; then
        echo "ERROR: origin/main does not exist locally (no such remote-tracking ref). Refusing to proceed." >&2
        echo "Fix: git fetch origin main" >&2
        return 1
    fi

    local local_head origin_main
    local_head="$(git rev-parse HEAD)"
    origin_main="$(git rev-parse refs/remotes/origin/main)"
    if [ "$local_head" != "$origin_main" ]; then
        echo "ERROR: local main ($local_head) does not match origin/main ($origin_main). Refusing to proceed." >&2
        echo "This script does not fetch or sync automatically." >&2
        echo "Fix: git fetch origin main && git pull --ff-only origin main" >&2
        return 1
    fi

    echo "==> Repository state OK: on main, clean, synchronized with origin/main ($local_head)"
}

# Only run the full bootstrap when executed directly (./run_portfolio_check.sh),
# not when sourced (e.g. by tests wanting check_repo_sync_guard in isolation).
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return 0
fi

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "==> Checking repository state (must start from synchronized main)"
check_repo_sync_guard

echo "==> Setting up .venv (repo-local, never global, never sudo)"
if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip --quiet
.venv/bin/python -m pip install -r requirements.txt --quiet
.venv/bin/python -m pip install pytest --quiet

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
