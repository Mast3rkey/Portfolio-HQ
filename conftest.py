"""Repo-wide pytest fixtures.

Deterministic isolation for allocate.plan(): ordinary tests must never
reach a live earnings lookup.

allocate.py imports the function with `from earnings import
days_until_earnings` (allocate.py:31). That statement binds a *new* name,
`allocate.days_until_earnings`, to the same function object at import
time — it does not create a live alias back to `earnings.days_until_earnings`.
plan() (allocate.py:305) calls the name it resolves through allocate's own
module namespace, so patching `earnings.days_until_earnings` after import
would leave plan()'s calls completely unaffected. The correct, and only
effective, patch target is therefore `allocate.days_until_earnings`.

This fixture only ever touches that one attribute on the `allocate` module.
It does not import or patch anything in `earnings` itself, so tests that
exercise earnings.py directly (test_earnings.py) are unaffected and see
the real, unpatched module.

Individual tests that need specific earnings-gate behavior can override
this default with `monkeypatch.setattr(allocate, "days_until_earnings", ...)`
in the test body — monkeypatch's own teardown restores this fixture's
default (and then the original) automatically, so overrides never leak
between tests.
"""

import pytest

import allocate


@pytest.fixture(autouse=True)
def no_live_earnings_lookup(monkeypatch):
    """Default every plan() call to an unblocked, unavailable earnings read.

    None matches production's own graceful-degradation value (earnings.py's
    documented behavior when a lookup fails) and exercises the
    "earnings:unavailable" non-blocking annotation path by default.
    """
    monkeypatch.setattr(allocate, "days_until_earnings", lambda ticker: None)
