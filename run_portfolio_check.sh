#!/usr/bin/env bash
# run_portfolio_check.sh — one-command phone-session bootstrap + read-only check.
#
# Cloud sessions are ephemeral: each one starts from a fresh clone with no
# .venv and no installed packages. This script rebuilds what's needed, runs
# the test suite, and prints --health + --review. It never writes portfolio
# state, never runs an update-* subcommand, and never places an order — order
# -placement methods don't exist in alpaca_client.py by design (see CLAUDE.md).
#
# Usage: ./run_portfolio_check.sh

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "==> Checking git state (must be on a clean 'main')"
BRANCH="$(git branch --show-current)"
if [ "$BRANCH" != "main" ]; then
    echo "ERROR: not on main (currently: ${BRANCH:-detached HEAD}). Refusing to proceed." >&2
    exit 1
fi
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "ERROR: tracked working-tree changes present. Refusing to proceed." >&2
    git status --short >&2
    exit 1
fi

echo "==> Fetching and fast-forwarding main"
git fetch origin main --prune
git pull --ff-only origin main

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
.venv/bin/python allocate.py --review

echo ""
echo "==> Done. No update-* command was run. No order was placed."
