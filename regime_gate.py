"""
regime_gate.py — 200-day EMA regime gate (harvested from trading-intelligence Phase 1).

This is the regime component of the old base_signal (the OOS-Sharpe-1.28 layer),
stripped of Phases 2-12. It answers one question on QQQ (or any) DAILY bars:
is price above its 200-day EMA? Regime status is informational only in
production (allocate.py, levels.py) -- the regime-gate backtest
(reports/regime_backtest.md, 2026-07-14) showed gating deployment on it cost
2.56pp/yr, so it's shown but never blocks.

Lookahead-safe: a bar on day D is gated by the EMA through day D-1.
"""

from __future__ import annotations

import pandas as pd

REGIME_EMA_DAYS = 200


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
    from alpaca_client import AlpacaPaperClient

    c = AlpacaPaperClient()
    bars = c.get_bars("QQQ", "1Day", 320, 420)
    closes = [float(b["c"]) for b in bars]
    ok = regime_ok_from_closes(closes)
    print(f"QQQ: {len(closes)} daily bars, latest close ${closes[-1]:.2f}")
    print(f"regime {'ABOVE' if ok else 'BELOW'} 200-EMA")
