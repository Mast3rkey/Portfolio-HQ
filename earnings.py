"""
earnings.py — next-earnings-date lookup with graceful degradation.

Primary source: yfinance (free). Alpaca's standard data API has no earnings
calendar, so yfinance is the practical option. If the date can't be determined
for any reason, we return None and the caller reports the ticker as
"earnings: unavailable" rather than silently treating it as safe.

Results are cached per-run to avoid duplicate network calls.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

_CACHE: dict[str, date | None] = {}


def next_earnings_date(ticker: str) -> date | None:
    """Return the next upcoming earnings date (>= today), or None if unknown."""
    if ticker in _CACHE:
        return _CACHE[ticker]

    result: date | None = None
    try:
        import logging
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        import yfinance as yf
        session = None
        try:
            # yfinance's default curl_cffi fingerprint (impersonate="chrome",
            # latest) gets connection-reset by this environment's proxy;
            # an older fingerprint passes through cleanly. Harmless outside
            # this environment — just a different valid TLS fingerprint.
            from curl_cffi.requests import Session as CurlSession
            session = CurlSession(impersonate="chrome110")
        except Exception:
            session = None
        tk = yf.Ticker(ticker, session=session)
        today = datetime.now(timezone.utc).date()

        # 1) earnings_dates DataFrame (most reliable when populated)
        try:
            ed = tk.get_earnings_dates(limit=12)
            if ed is not None and len(ed):
                upcoming = [d.date() if hasattr(d, "date") else d
                            for d in ed.index]
                future = sorted(d for d in upcoming if d >= today)
                if future:
                    result = future[0]
        except Exception:
            pass

        # 2) calendar fallback
        if result is None:
            try:
                cal = tk.calendar
                ev = None
                if isinstance(cal, dict):
                    ev = cal.get("Earnings Date")
                if ev:
                    d = ev[0] if isinstance(ev, (list, tuple)) else ev
                    d = d.date() if hasattr(d, "date") else d
                    if d >= today:
                        result = d
            except Exception:
                pass
    except Exception:
        result = None

    _CACHE[ticker] = result
    return result


def days_until_earnings(ticker: str) -> int | None:
    """Calendar days until next earnings, or None if unknown."""
    d = next_earnings_date(ticker)
    if d is None:
        return None
    return (d - datetime.now(timezone.utc).date()).days


if __name__ == "__main__":
    import sys
    for t in sys.argv[1:] or ["AAPL", "NVDA"]:
        d = next_earnings_date(t)
        print(f"{t}: {d}  ({days_until_earnings(t)} days)" if d
              else f"{t}: unavailable")
