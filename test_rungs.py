"""
test_rungs.py — unit tests for the rung backtest's pure functions.
Run: python3 test_rungs.py
"""

from __future__ import annotations

import traceback

from backtest_rungs import (pivot_lows, rungs_sr, rungs_current, fill_price,
                            twr_annualized, max_drawdown)


def _bar(o, h, l, c):
    return {"t": "2025-01-01T05:00:00Z", "o": o, "h": h, "l": l, "c": c, "v": 1000}


# ── pivots / S-R rungs ──────────────────────────────────────────────────────────

def test_pivot_lows_finds_confirmed_minima():
    lows = [10, 9, 8, 7, 8, 9, 10, 11, 10, 9, 8.5, 9, 10, 11, 12, 13, 14, 15]
    idx = pivot_lows(lows, k=5)
    assert 10 in idx                   # the 8.5: k bars of context on both sides
    assert 3 not in idx                # the 7 lacks k bars of LEFT context — unconfirmable
    assert 0 not in idx and len(lows) - 1 not in idx   # edges can't confirm


def test_rungs_sr_returns_levels_below_price_nearest_first():
    # V-shape then rally: pivot low at 90 must be found; price ends at 100.
    lows = [100, 98, 96, 94, 92, 90, 92, 94, 96, 97, 95, 93, 91.5, 93, 95,
            96, 97, 98, 99, 99.5]
    bars = [_bar(l + 1, l + 2, l, l + 1) for l in lows] + [_bar(99, 101, 99, 100)]
    rungs = rungs_sr(bars)
    assert rungs and all(r < 100 for r in rungs)
    assert rungs == sorted(rungs, reverse=True)        # nearest below price first


def test_rungs_sr_empty_when_no_history():
    assert rungs_sr([_bar(100, 101, 99, 100)] * 3) == []


# ── production rungs (Arm A mirrors levels.compute_levels) ─────────────────────

def test_rungs_current_below_price_only():
    # 260 flat bars then a spike up: all rungs (50SMA − k*ATR) sit below price.
    bars = [_bar(100, 101, 99, 100) for _ in range(260)] + [_bar(100, 111, 100, 110)]
    cfg = {"rung_atr_multipliers": [1.0, 2.0, 3.0], "swing_low_sessions": 60}
    rungs = rungs_current(bars, cfg)
    assert 1 <= len(rungs) <= 3
    assert all(r < 110 for r in rungs)


# ── fills ───────────────────────────────────────────────────────────────────────

def test_fill_at_limit_when_traded_through():
    assert fill_price(95.0, bar_open=97.0, bar_low=94.0) == 95.0


def test_gap_down_fills_at_open():
    assert fill_price(95.0, bar_open=92.0, bar_low=91.0) == 92.0


def test_no_fill_above_limit():
    assert fill_price(95.0, bar_open=97.0, bar_low=95.5) is None


# ── TWR ─────────────────────────────────────────────────────────────────────────

def test_twr_ignores_flows():
    # Flat prices + a deposit: TWR must be 0, not inflated by the contribution.
    vals = [1000.0, 1000.0, 3000.0, 3000.0]
    flows = {2: 2000.0}
    assert abs(twr_annualized(vals, flows)) < 1e-9


def test_twr_positive_on_growth():
    vals = [1000.0, 1010.0, 1020.1]
    assert twr_annualized(vals, {}) > 0


def test_max_drawdown():
    assert abs(max_drawdown([100, 120, 90, 110]) - (-25.0)) < 1e-9


def _run_all() -> int:
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"  FAIL  {t.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed ({len(tests)} total)")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    sys.exit(_run_all())
