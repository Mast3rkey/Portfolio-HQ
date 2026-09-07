"""
alpaca_client.py — Alpaca PAPER connection (harvested from trading-intelligence).

Reusable, dependency-light client for the Alpaca paper account. Credentials come
from the environment or a git-ignored .env file — never hardcoded. A PAPER_ONLY
guard refuses any non-paper base URL, so this can never touch real money.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from datetime import datetime, timedelta, timezone
from pathlib import Path

import certifi

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_BASE = "https://data.alpaca.markets/v2/stocks"
CRYPTO_BASE = "https://data.alpaca.markets/v1beta3/crypto/us"
PAPER_BASE = "https://paper-api.alpaca.markets/v2"
TRUSTED_ALPACA_HOSTS = frozenset({"paper-api.alpaca.markets", "data.alpaca.markets"})


def _trusted_https_url(url: str, *, hosts: frozenset[str] = TRUSTED_ALPACA_HOSTS):
    """Return parsed *url* only when credentials may safely be sent to it."""
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"refusing malformed Alpaca endpoint {url!r}") from exc
    if (
        parsed.scheme != "https"
        or parsed.hostname not in hosts
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
        or parsed.fragment
    ):
        raise RuntimeError(f"refusing untrusted Alpaca endpoint {url!r}")
    return parsed


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Never forward credential-bearing requests across an HTTP redirect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError(f"refusing redirected Alpaca request to {newurl!r}")


def load_credentials() -> dict:
    """Load Alpaca creds from real env vars first, then .env. No keys in code."""
    creds = {k: os.environ.get(k) for k in
             ("ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_BASE_URL")}
    if all(creds.values()):
        return creds
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                creds.setdefault(k.strip(), None)
                if not creds.get(k.strip()):
                    creds[k.strip()] = v.strip()
    missing = [k for k, v in creds.items() if not v]
    if missing:
        raise RuntimeError(f"missing Alpaca credentials: {missing}")
    return creds


class AlpacaPaperClient:
    def __init__(self):
        creds = load_credentials()
        configured_base = creds["ALPACA_BASE_URL"].rstrip("/")
        parsed = _trusted_https_url(configured_base, hosts=frozenset({"paper-api.alpaca.markets"}))
        if parsed.path != "/v2" or parsed.query:
            raise RuntimeError(
                f"PAPER_ONLY guard: expected exact paper API base {PAPER_BASE!r}, "
                f"got {configured_base!r}"
            )
        self.base = PAPER_BASE
        self._headers = {"APCA-API-KEY-ID": creds["ALPACA_API_KEY"],
                         "APCA-API-SECRET-KEY": creds["ALPACA_API_SECRET"],
                         "Content-Type": "application/json"}
        self._ctx = ssl.create_default_context(cafile=certifi.where())
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=self._ctx),
            _RejectRedirects(),
        )

    def _req(self, method: str, url: str, body: dict | None = None,
             retries: int = 3) -> dict | list:
        if method != "GET" or body is not None:
            raise RuntimeError("advisory-only Alpaca client permits GET requests without a body only")
        _trusted_https_url(url)
        req = urllib.request.Request(url, method="GET", headers=self._headers)
        last = None
        for attempt in range(retries):
            try:
                with self._opener.open(req, timeout=30) as r:
                    txt = r.read().decode()
                    return json.loads(txt) if txt else {}
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"{method} {url} -> HTTP {e.code}: {e.read().decode()[:300]}")
            except (urllib.error.URLError, TimeoutError) as e:
                last = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"request failed after {retries} retries: {last}")

    # get_position() was removed here (2026-07-15 cleanup) -- zero callers
    # anywhere, including this file's own __main__ self-test. get_account()
    # and get_clock() are kept below: unused by the live workflow, but this
    # file's __main__ block (`python3 alpaca_client.py`) is a real connectivity/
    # credentials diagnostic that calls both -- a legitimate runtime caller
    # the audit's cross-file grep didn't count since it excluded this file's
    # own references.

    def get_account(self) -> dict:
        return self._req("GET", f"{self.base}/account")

    def get_clock(self) -> dict:
        return self._req("GET", f"{self.base}/clock")

    # NOTE: order-placement methods (submit_order / get_order / cancel_order)
    # were deliberately REMOVED for band-validation. This project is advisory
    # only — it must never place, modify, or cancel an order. Do not re-add them.

    # --- market data ------------------------------------------------------ #

    def get_bars(self, symbol: str, timeframe: str, limit: int,
                 days_back: int, adjustment: str = "split") -> list[dict]:
        """Most-recent `limit` bars (chronological). NOTE: the bars endpoint needs
        a start window; sort=desc + limit gets the newest, which we reverse.
        Uses the free IEX feed (paper tier). Split-adjusted by default so SMAs
        are continuous across splits."""
        start = (datetime.now(timezone.utc) - timedelta(days=days_back)).date().isoformat()
        url = (f"{DATA_BASE}/{symbol}/bars?timeframe={timeframe}&start={start}"
               f"&limit={limit}&adjustment={adjustment}&feed=iex&sort=desc")
        bars = self._req("GET", url).get("bars") or []
        return sorted(bars, key=lambda b: b["t"])

    def get_crypto_bars(self, symbol: str, days_back: int = 420) -> list[dict]:
        """Daily bars for a crypto pair like 'BTC/USD' (chronological, same
        o/h/l/c/v dict shape as stock bars)."""
        from urllib.parse import quote
        start = (datetime.now(timezone.utc) - timedelta(days=days_back)).date().isoformat()
        url = (f"{CRYPTO_BASE}/bars?symbols={quote(symbol, safe='/')}"
               f"&timeframe=1Day&start={start}&limit=1000")
        bars = (self._req("GET", url).get("bars") or {}).get(symbol) or []
        return sorted(bars, key=lambda b: b["t"])

    def get_crypto_latest(self, symbols: list[str]) -> dict[str, float]:
        """Latest trade price for crypto pairs like 'BTC/USD'. Returns
        {symbol: price} for whatever the feed returns (missing symbols omitted)."""
        if not symbols:
            return {}
        q = ",".join(symbols)
        from urllib.parse import quote
        url = f"{CRYPTO_BASE}/latest/trades?symbols={quote(q, safe='/,')}"
        trades = self._req("GET", url).get("trades") or {}
        return {sym: float(t["p"]) for sym, t in trades.items() if t and "p" in t}


if __name__ == "__main__":
    c = AlpacaPaperClient()
    acct = c.get_account()
    clock = c.get_clock()
    print(f"connected: {c.base}")
    print(f"account: equity ${float(acct['equity']):,.0f}  status {acct['status']}")
    print(f"clock: open={clock['is_open']}  next_open={clock.get('next_open','?')[:16]}")
