"""Regression coverage for levels.py's stance_for() and the regime header.

Exists to prevent a repeat of the 2026-07-15 drift (docs/PORTFOLIO_HQ_AUDIT.md,
fixed in 7b3be23): stance_for() used to BLOCK on a bearish QQQ regime, the
exact gate reports/regime_backtest.md and CLAUDE.md's Decisions Log removed
from allocate.py's plan() on 2026-07-14. Regime is informational-only,
matched between both entry points -- these tests pin that down mechanically
instead of relying on the docstring alone.
"""

from __future__ import annotations

import inspect

from levels import stance_for, _render


GATES = {"earnings_blackout_days": 7, "trend_rsi_override": 30}


def _row(*, price, sma200, rsi, l1_value):
    return {
        "price": price,
        "sma200": sma200,
        "rsi": rsi,
        "levels": [{"name": "L1", "value": l1_value, "dist_pct": 0.0, "tags": []},
                   {"name": "L2", "value": l1_value - 1, "dist_pct": 0.0, "tags": []},
                   {"name": "L3", "value": l1_value - 2, "dist_pct": 0.0, "tags": []}],
        "notes": [],
    }


def test_stance_for_has_no_regime_parameter():
    # Locks the fixed signature -- reintroducing a regime_bearish parameter
    # (the shape of the original bug) fails this test immediately.
    params = list(inspect.signature(stance_for).parameters)
    assert params == ["row", "earn_days", "gates"], (
        "stance_for() signature changed -- if a regime parameter was added "
        "back, this reintroduces the fixed drift with allocate.py's plan(), "
        "which never gates on regime (reports/regime_backtest.md verdict)."
    )


def test_stance_for_no_data():
    row = {"price": None, "sma200": None, "rsi": None, "levels": [], "notes": ["insufficient history (5 bars)"]}
    stance, reason = stance_for(row, None, GATES)
    assert stance == "NO-DATA"


def test_stance_for_earnings_blackout_blocks_regardless_of_trend():
    row = _row(price=100, sma200=90, rsi=50, l1_value=100)  # trend_ok, price at L1
    stance, reason = stance_for(row, 3, GATES)  # 3 days out, within 7-day blackout
    assert stance == "BLOCKED"
    assert "earnings" in reason


def test_stance_for_buyable_at_or_below_l1_in_uptrend():
    row = _row(price=95, sma200=90, rsi=50, l1_value=100)  # price below L1, above 200SMA
    stance, reason = stance_for(row, None, GATES)
    assert stance == "BUYABLE"


def test_stance_for_downtrend_without_rsi_override_waits_not_blocks():
    # price below 200SMA (downtrend) and RSI above the override threshold:
    # this used to be exactly the shape of market weakness the old
    # regime_bearish gate would BLOCK on. It must now be WAIT, never BLOCKED --
    # gate on it, not zero it out.
    row = _row(price=80, sma200=90, rsi=50, l1_value=100)
    stance, reason = stance_for(row, None, GATES)
    assert stance == "WAIT"
    assert "downtrend" in reason


def test_stance_for_downtrend_with_low_rsi_override_is_buyable():
    row = _row(price=95, sma200=100, rsi=25, l1_value=100)  # below 200SMA but RSI < 30
    stance, reason = stance_for(row, None, GATES)
    assert stance == "BUYABLE"


def test_render_regime_header_does_not_claim_levels_are_blocked():
    # The header text itself was the last residue of the old behavior --
    # it kept saying "levels stamped do-not-act" after stance_for() stopped
    # doing that, which is misleading independent of any stance logic bug.
    rows = [{"ticker": "TEST", "stance": "BUYABLE", "reason": "", "price": 100,
             "rsi": 50, "levels": [{"name": "L1", "value": 100, "dist_pct": 0.0, "tags": []},
                                     {"name": "L2", "value": 99, "dist_pct": -1.0, "tags": []},
                                     {"name": "L3", "value": 98, "dist_pct": -2.0, "tags": []}],
             "notes": []}]
    out = _render(rows, regime_known=True, regime_bearish=True, cfg={})
    assert "do-not-act" not in out
    assert "BELOW 200-EMA (risk-off)" in out
