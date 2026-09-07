"""Sanity checks for indicators.py's pure functions.

Not a full test suite — just enough to catch a silent regression from a
future pandas/dependency upgrade. indicators.py has no side effects, so
these are cheap to keep.
"""

from indicators import atr, rsi, sma


def _bars(closes, highs=None, lows=None):
    highs = highs or closes
    lows = lows or closes
    return [{"o": c, "h": h, "l": l, "c": c, "v": 0}
            for c, h, l in zip(closes, highs, lows)]


def test_rsi_of_flat_series_is_100():
    # No losses at all -> avg_loss == 0 -> the function's explicit 100.0
    # branch, not the textbook "undefined/50" edge case. Locking in actual
    # behavior, not the intuitive-but-wrong assumption.
    bars = _bars([100.0] * 20)
    assert rsi(bars, period=14) == 100.0


def test_atr_of_constant_price_is_zero():
    bars = _bars([100.0] * 20)
    assert atr(bars, period=14) == 0.0


def test_sma_of_known_values():
    bars = _bars([float(i) for i in range(1, 11)])  # 1..10
    assert sma(bars, period=10) == 5.5


def test_sma_returns_none_below_period():
    bars = _bars([100.0] * 5)
    assert sma(bars, period=10) is None
