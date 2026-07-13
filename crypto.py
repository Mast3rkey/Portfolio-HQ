"""
crypto.py — crypto sleeve pricing (advisory only, no trading).

Majors (BTC/ETH/SOL) come from Alpaca's crypto data feed. Coins Alpaca doesn't
carry (e.g. HYPE) come from CoinGecko's free, keyless simple-price endpoint.
Every source fails gracefully: a coin whose price can't be fetched is reported
with price=None and an error string rather than crashing the run.
"""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request

import certifi

_CTX = ssl.create_default_context(cafile=certifi.where())
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def coingecko_price(coin_id: str) -> tuple[float | None, str]:
    """Return (usd_price, '') or (None, error) for a CoinGecko coin id."""
    url = f"{COINGECKO_URL}?ids={coin_id}&vs_currencies=usd"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "band-validation/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=_CTX) as r:
            data = json.loads(r.read())
        px = data.get(coin_id, {}).get("usd")
        if px is None:
            return None, f"coingecko: no price for {coin_id!r}"
        return float(px), ""
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
        return None, f"coingecko unavailable: {str(e)[:60]}"


def coingecko_daily_bars(coin_id: str, days: int = 365) -> tuple[list[dict], str]:
    """Daily close series from CoinGecko as pseudo-bars (o=h=l=c=close), so the
    shared indicator functions work unchanged. With h==l==c, the ATR true range
    reduces to |close - prev_close| — a documented approximation for coins that
    have no OHLC feed. Returns (bars, error)."""
    url = (f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
           f"?vs_currency=usd&days={days}&interval=daily")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "band-validation/1.0"})
        with urllib.request.urlopen(req, timeout=20, context=_CTX) as r:
            data = json.loads(r.read())
        prices = data.get("prices") or []
        bars = [{"t": str(ts), "o": p, "h": p, "l": p, "c": p, "v": 0}
                for ts, p in prices if p is not None]
        if not bars:
            return [], f"coingecko: empty daily series for {coin_id!r}"
        return bars, ""
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
        return [], f"coingecko daily unavailable: {str(e)[:60]}"


def fetch_crypto(client, coins: list[str], coingecko_ids: dict[str, str]) -> dict:
    """
    Fetch a last price for every coin. Coins with a CoinGecko id use CoinGecko;
    all others use Alpaca ('COIN/USD'). Returns
    {coin: {price: float|None, source: str, error: str}}.
    """
    out: dict[str, dict] = {}

    alpaca_coins = [c for c in coins if c not in coingecko_ids]
    alpaca_syms = [f"{c}/USD" for c in alpaca_coins]
    prices: dict[str, float] = {}
    alpaca_err = ""
    if alpaca_syms:
        try:
            prices = client.get_crypto_latest(alpaca_syms)
        except Exception as e:
            alpaca_err = f"alpaca crypto unavailable: {str(e)[:60]}"

    for c in coins:
        if c in coingecko_ids:
            px, err = coingecko_price(coingecko_ids[c])
            out[c] = {"price": px, "source": "coingecko", "error": err}
        else:
            px = prices.get(f"{c}/USD")
            out[c] = {"price": px, "source": "alpaca",
                      "error": alpaca_err if px is None else ""}
    return out


if __name__ == "__main__":
    from alpaca_client import AlpacaPaperClient
    res = fetch_crypto(AlpacaPaperClient(), ["BTC", "ETH", "SOL", "HYPE"],
                       {"HYPE": "hyperliquid"})
    for coin, d in res.items():
        px = f"${d['price']:,.2f}" if d["price"] else f"n/a ({d['error']})"
        print(f"{coin:5} {px:>18}  [{d['source']}]")
