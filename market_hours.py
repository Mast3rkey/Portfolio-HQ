"""
market_hours.py — market-hours gate (harvested from trading-intelligence scheduler).

The reliable gate is the Alpaca clock (it knows holidays/half-days). A local ET
check is the fallback when the clock call fails. Reused unchanged in spirit from
the old scheduler.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
SESSION_OPEN_MIN = 9 * 60 + 30       # 09:30 ET
SESSION_CLOSE_MIN = 16 * 60          # 16:00 ET


def is_market_hours_local(dt_et: datetime | None = None) -> bool:
    """Fallback gate: Mon-Fri, 09:30 <= t < 16:00 ET (ignores holidays)."""
    dt_et = dt_et or datetime.now(ET)
    if dt_et.weekday() >= 5:                       # Sat / Sun
        return False
    t = dt_et.hour * 60 + dt_et.minute
    return SESSION_OPEN_MIN <= t < SESSION_CLOSE_MIN


def market_open(client=None) -> bool:
    """True if the market is open. Uses the Alpaca clock (holiday-aware) and
    falls back to local ET time if the clock is unavailable.
    """
    try:
        if client is None:
            from alpaca_client import AlpacaPaperClient
            client = AlpacaPaperClient()
        return bool(client.get_clock()["is_open"])
    except Exception:
        return is_market_hours_local()


if __name__ == "__main__":
    print(f"local ET gate now: {is_market_hours_local()}")
    print(f"alpaca clock open: {market_open()}")
