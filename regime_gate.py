"""
regime_gate.py — 200-day EMA regime gate (harvested from trading-intelligence Phase 1).

This is the regime component of the old base_signal (the OOS-Sharpe-1.28 layer),
stripped of Phases 2-12. It answers one question on QQQ (or any) DAILY bars:
is price above its 200-day EMA? Used as the regime filter for the new strategy.

Lookahead-safe: a bar on day D is gated by the EMA through day D-1.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
DAILY_DIR = PROJECT_ROOT / "data" / "daily"

REGIME_EMA_DAYS = 200


def load_daily(ticker: str) -> pd.DataFrame:
    """Load a daily OHLCV CSV, indexed by ET date, with the regime column attached."""
    path = DAILY_DIR / f"{ticker}_daily.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing daily data: {path}")
    df = pd.read_csv(path, parse_dates=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    df["date"] = df["timestamp"].dt.tz_convert("America/New_York").dt.normalize()
    return attach_regime(df)


def attach_regime(df: pd.DataFrame) -> pd.DataFrame:
    """Add ema200 (lagged one day) and regime_ok = close > lagged EMA."""
    ema = df["close"].ewm(span=REGIME_EMA_DAYS, adjust=False).mean()
    df["ema200"] = ema.shift(1)                    # lag one day -> no lookahead
    df["regime_ok"] = df["close"] > df["ema200"]
    return df


def regime_ok_from_closes(closes) -> bool:
    """Convenience for a live feed: given a chronological list/Series of daily
    closes (latest last), is the latest close above the 200-day EMA through the
    PRIOR day? Returns False if there isn't enough history.
    """
    s = pd.Series(list(closes), dtype=float)
    if len(s) < 2:
        return False
    ema_prev = s.iloc[:-1].ewm(span=REGIME_EMA_DAYS, adjust=False).mean().iloc[-1]
    return bool(s.iloc[-1] > ema_prev)


if __name__ == "__main__":
    df = load_daily("QQQ")
    latest = df.iloc[-1]
    valid = df.dropna(subset=["ema200"])
    pct_above = (valid["regime_ok"].mean() * 100)
    print(f"QQQ daily {df['date'].iloc[0].date()} .. {df['date'].iloc[-1].date()} "
          f"({len(df)} bars)")
    print(f"latest close ${latest['close']:.2f}  200d-EMA ${latest['ema200']:.2f}  "
          f"regime {'ABOVE' if latest['regime_ok'] else 'BELOW'}")
    print(f"regime ON {pct_above:.0f}% of {len(valid)} valid days")
