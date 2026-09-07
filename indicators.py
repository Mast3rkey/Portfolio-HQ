"""
indicators.py — small, dependency-light technical indicators for the advisor.

All functions take a chronological list of daily bars (Alpaca format: dicts with
keys o/h/l/c/v) or a pandas Series of closes, and return plain floats. Wilder's
smoothing is used for RSI and ATR to match standard charting platforms.
"""

from __future__ import annotations

import pandas as pd


def _closes(bars: list[dict]) -> pd.Series:
    return pd.Series([float(b["c"]) for b in bars], dtype=float)


def sma(bars: list[dict], period: int) -> float | None:
    s = _closes(bars)
    if len(s) < period:
        return None
    return float(s.tail(period).mean())


def rsi(bars: list[dict], period: int = 14) -> float | None:
    s = _closes(bars)
    if len(s) < period + 1:
        return None
    delta = s.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean().iloc[-1]
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return float(100 - 100 / (1 + rs))


def atr(bars: list[dict], period: int = 14) -> float | None:
    if len(bars) < period + 1:
        return None
    df = pd.DataFrame({
        "h": [float(b["h"]) for b in bars],
        "l": [float(b["l"]) for b in bars],
        "c": [float(b["c"]) for b in bars],
    })
    prev_c = df["c"].shift(1)
    tr = pd.concat([
        df["h"] - df["l"],
        (df["h"] - prev_c).abs(),
        (df["l"] - prev_c).abs(),
    ], axis=1).max(axis=1)
    return float(tr.ewm(alpha=1 / period, adjust=False).mean().iloc[-1])


def swing_low(bars: list[dict], sessions: int = 60) -> float | None:
    """Lowest low of the past `sessions` bars."""
    if not bars:
        return None
    lows = [float(b["l"]) for b in bars[-sessions:]]
    return min(lows) if lows else None


def last_price(bars: list[dict]) -> float | None:
    return float(bars[-1]["c"]) if bars else None


def compute_all(bars: list[dict]) -> dict:
    """Return the full indicator bundle for one ticker's daily bars."""
    return {
        "price":   last_price(bars),
        "sma200":  sma(bars, 200),
        "sma50":   sma(bars, 50),
        "rsi14":   rsi(bars, 14),
        "atr14":   atr(bars, 14),
        "bars":    len(bars),
    }
