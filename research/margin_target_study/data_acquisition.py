"""
data_acquisition.py — MARGIN-0005 G1 data acquisition and validation.

Authority: governance/decisions/MARGIN-0005-margin-target-research-charter.md §1.2
(G1 data-acquisition steps, cached read-only under the research directory) and §4
(approved research-package file list, which names this module).

Scope guards (charter §2, PROTOCOL_V2.md §11, pre_registration.yaml):
  * This module performs DATA acquisition and DATA validation only. It never calls
    simulate(), never consumes a registered trial, never produces a margin signal,
    ranking, or recommendation, and never places an order.
  * It writes ONLY under research/margin_target_study/data/ (and reads production
    files read-only).
  * Untouched-test isolation: every return-derived computation in this module
    (discontinuity scans, T-D3 reconciliation) is truncated at the development
    boundaries (Track 2: 2025-06-30, Track 3: 2020-12-31). The roster price cache
    is refreshed through the run date because the charter's G1 gate directs it
    ("refreshed through the run date"); its untouched segment is stored but never
    summarized, charted, or reconciled here. Loader-level truncation (test T-U1)
    is a G2 implementation obligation, not claimed here.
  * Total-return (adjclose) series are quarantined under data/quarantine_yahoo/
    and are used exactly once: the T-D3 reconciliation (`reconcile`). They are
    never merged into any primary dataset (protocol §4, T-D4).

Sources:
  * Alpaca Market Data (data.alpaca.markets) — split-adjusted IEX daily bars,
    v1 corporate actions (cash dividends + splits), v1beta3 crypto daily bars.
    Credentials from environment (ALPACA_API_KEY / ALPACA_API_SECRET), same
    convention as alpaca_client.py. Committed to the repository (consistent with
    the repository's existing committed Alpaca cache, data/backtest/).
  * Yahoo Finance chart API via curl_cffi impersonate="chrome110" (the repository's
    established working fingerprint, see earnings.py) — Track 3 long-history
    SPY/QQQ raw closes + events, per-ticker adjclose TR validation series, ^IRX
    risk-free fallback. NOT committed (redistribution caution); reproducible via
    this module; SHA-256 of derived files recorded in data_manifest.yaml.

Subcommands:
  prices      acquire roster split-adjusted daily bars (2020-07-01 -> run date)
  dividends   acquire point-in-time dividend + split ledger (dev-bounded)
  crypto      acquire BTC/ETH/SOL daily bars (2021-06-01 -> 2025-06-30)
  yahoo       acquire quarantined Yahoo datasets (TR validation, Track 3, ^IRX)
  inventory   hash + coverage inventory of the existing data/backtest cache
  validate    run all deterministic G1 data validators (read-only)
  reconcile   T-D3 dividend reconciliation (primary path vs quarantined TR)
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import certifi

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DATA = HERE / "data"
PRICES_DIR = DATA / "prices"
DIV_DIR = DATA / "dividends"
CRYPTO_DIR = DATA / "crypto"
QUAR = DATA / "quarantine_yahoo"          # never committed; TR/Track3/rates
TR_DIR = QUAR / "tr"
TRACK3_DIR = QUAR / "track3"
RATES_DIR = QUAR / "rates"
BACKTEST_CACHE = REPO / "data" / "backtest"

# ---- governed boundaries (pre_registration.yaml) ----
DEV_BOUNDARY_T2 = "2025-06-30"
DEV_BOUNDARY_T3 = "2020-12-31"
PRICE_START = "2020-07-01"                # matches existing cache design (signal warm-up)
RUN_DATE = "2026-07-23"                   # last complete session at G1 execution
DIV_START = "2020-07-01"
CRYPTO_START = "2021-06-01"               # protocol §4 crypto gap row
TR_START = "2021-05-01"
T3_SPY_START = "1993-01-29"
T3_QQQ_START = "1999-03-10"
IRX_START = "1999-01-01"

EXCLUDE = {"SPCX", "SKHY"}                # roster_63 convention (backtest_regime.py)
CRYPTO_SYMS = ("BTC/USD", "ETH/USD", "SOL/USD")
YAHOO_SYMBOL = {"BRK.B": "BRK-B"}         # brokerage dot form -> Yahoo dash form

DISCONTINUITY_ABS_RET = 0.45              # flag threshold for split-shaped jumps
TD3_TOLERANCE_PP = 0.3                    # protocol T-D3, per ticker-portfolio, pp/yr

_ctx = ssl.create_default_context(cafile=certifi.where())


def _alpaca_headers() -> dict:
    key, sec = os.environ.get("ALPACA_API_KEY"), os.environ.get("ALPACA_API_SECRET")
    if not (key and sec):
        raise RuntimeError("missing ALPACA_API_KEY / ALPACA_API_SECRET")
    return {"APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": sec}


def _get_json(url: str, headers: dict | None = None, retries: int = 4) -> dict:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=60, context=_ctx) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001 - retry then surface
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {retries} tries: {url} :: {last}")


def _yahoo_json(url: str, retries: int = 4) -> dict:
    from curl_cffi import requests as cr
    last = None
    for attempt in range(retries):
        try:
            r = cr.get(url, impersonate="chrome110", timeout=45)
            if r.status_code == 200:
                return r.json()
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Yahoo GET failed after {retries} tries: {url} :: {last}")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def roster_63() -> list[str]:
    import yaml
    t = yaml.safe_load(open(REPO / "targets.yaml"))
    out = set()
    for tier in t["tiers"].values():
        for s in tier["tickers"]:
            s = s.upper()
            if s not in EXCLUDE:
                out.add(s)
    return sorted(out)


def _bar_date(t: str) -> str:
    return t[:10]


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=None, separators=(",", ":"),
                               sort_keys=False) + "\n")


# --------------------------------------------------------------------------
# acquisition
# --------------------------------------------------------------------------

def acquire_prices() -> None:
    """Roster split-adjusted IEX daily bars, PRICE_START -> RUN_DATE (charter G1:
    'refreshed through the run date'). Untouched segment stored, never consumed."""
    H = _alpaca_headers()
    for sym in roster_63():
        q = urllib.parse.quote(sym, safe="")
        bars, token = [], None
        while True:
            url = (f"https://data.alpaca.markets/v2/stocks/{q}/bars"
                   f"?timeframe=1Day&adjustment=split&feed=iex"
                   f"&start={PRICE_START}&end={RUN_DATE}T23%3A59%3A59Z&limit=10000")
            if token:
                url += f"&page_token={urllib.parse.quote(token, safe='')}"
            d = _get_json(url, H)
            bars += d.get("bars") or []
            token = d.get("next_page_token")
            if not token:
                break
        _write_json(PRICES_DIR / f"{sym}.json", {
            "meta": {"symbol": sym, "source": "alpaca_iex_daily",
                     "adjustment": "split", "feed": "iex",
                     "start": PRICE_START, "end": RUN_DATE,
                     "acquired_at": _now_utc(),
                     "isolation": "contains_untouched_segment_loader_truncation_required"},
            "bars": bars})
        print(f"  prices {sym}: {len(bars)} bars "
              f"{_bar_date(bars[0]['t'])} -> {_bar_date(bars[-1]['t'])}" if bars
              else f"  prices {sym}: EMPTY")
        time.sleep(0.15)


def acquire_dividends() -> None:
    """Point-in-time cash dividends (DIV_START -> DEV_BOUNDARY_T2) and split
    records (DIV_START -> RUN_DATE; splits are adjustment metadata and must cover
    every split already baked into the as-of-now split-adjusted price history)."""
    H = _alpaca_headers()
    syms = roster_63()

    def _fetch(types: str, start: str, end: str) -> dict[str, list]:
        acc: dict[str, list] = {}
        for i in range(0, len(syms), 15):
            batch = ",".join(syms[i:i + 15])
            token = None
            while True:
                url = ("https://data.alpaca.markets/v1/corporate-actions"
                       f"?symbols={urllib.parse.quote(batch, safe=',')}"
                       f"&types={types}&start={start}&end={end}&limit=1000")
                if token:
                    url += f"&page_token={urllib.parse.quote(token, safe='')}"
                d = _get_json(url, H)
                for kind, rows in (d.get("corporate_actions") or {}).items():
                    acc.setdefault(kind, []).extend(rows)
                token = d.get("next_page_token")
                if not token:
                    break
            time.sleep(0.2)
        return acc

    # The corporate-actions endpoint's start/end window does not reliably select
    # on ex_date (events with ex_date near the boundary but later payable/process
    # dates fall outside a tight window).  Query with a +120d buffer and filter
    # locally on ex_date <= DEV_BOUNDARY_T2 — the governed boundary is applied
    # here, deterministically, not by the vendor's window semantics.
    raw_divs = _fetch("cash_dividend", DIV_START, "2025-10-31").get("cash_dividends", [])
    divs, seen = [], set()
    for d in raw_divs:
        if d["ex_date"] > DEV_BOUNDARY_T2:
            continue
        # vendor feed carries occasional duplicate rows (same symbol/ex_date/rate,
        # distinct ids) — dedupe on the economic key, keep the first row.
        k = (d["symbol"], d["ex_date"], d["rate"], bool(d.get("special")))
        if k in seen:
            continue
        seen.add(k)
        divs.append(d)
    sp = _fetch("forward_split,reverse_split", DIV_START, RUN_DATE)
    splits = sp.get("forward_splits", []) + sp.get("reverse_splits", [])

    # split-adjust dividend amounts so they live in the same units as the
    # split-adjusted price series: divide by every split factor whose ex_date
    # is AFTER the dividend's ex_date.
    factors: dict[str, list[tuple[str, float]]] = {}
    for s in splits:
        factors.setdefault(s["symbol"], []).append(
            (s["ex_date"], float(s["new_rate"]) / float(s["old_rate"])))
    ledger = []
    for d in sorted(divs, key=lambda r: (r["symbol"], r["ex_date"])):
        f = 1.0
        for ex, fac in factors.get(d["symbol"], []):
            if ex > d["ex_date"]:
                f *= fac
        ledger.append({
            "symbol": d["symbol"], "ex_date": d["ex_date"],
            "rate_raw": float(d["rate"]),
            "rate_split_adjusted": float(d["rate"]) / f,
            "split_adjustment_factor": f,
            "payable_date": d.get("payable_date"),
            "record_date": d.get("record_date"),
            "special": bool(d.get("special")),
            "foreign": bool(d.get("foreign")),
            "alpaca_id": d.get("id")})
    _write_json(DIV_DIR / "dividend_ledger.json", {
        "meta": {"source": "alpaca_corporate_actions_v1", "types": "cash_dividend",
                 "start": DIV_START, "end": DEV_BOUNDARY_T2,
                 "acquired_at": _now_utc(),
                 "adjustment": "amounts divided by post-ex-date split factors "
                               "(split ledger below) to match split-adjusted prices",
                 "credit_convention": "ex_date (pre_registration.yaml dividends.credit)",
                 "isolation": "dev_bounded_max_ex_date_2025-06-30"},
        "dividends": ledger})
    _write_json(DIV_DIR / "splits.json", {
        "meta": {"source": "alpaca_corporate_actions_v1",
                 "types": "forward_split,reverse_split",
                 "start": DIV_START, "end": RUN_DATE, "acquired_at": _now_utc(),
                 "note": "coverage runs to the run date because current "
                         "split-adjusted prices embed all splits to date"},
        "splits": sorted(splits, key=lambda r: (r["symbol"], r["ex_date"]))})
    print(f"  dividends: {len(ledger)} events, splits: {len(splits)}")


def acquire_crypto() -> None:
    """BTC/ETH/SOL daily bars, CRYPTO_START -> DEV_BOUNDARY_T2 only (protocol §4
    crypto row: '2021-06 -> dev boundary'). No untouched-period crypto stored."""
    H = _alpaca_headers()
    for sym in CRYPTO_SYMS:
        q = urllib.parse.quote(sym, safe="")
        bars, token = [], None
        while True:
            url = ("https://data.alpaca.markets/v1beta3/crypto/us/bars"
                   f"?symbols={q}&timeframe=1Day&start={CRYPTO_START}"
                   f"&end={DEV_BOUNDARY_T2}T23%3A59%3A59Z&limit=10000")
            if token:
                url += f"&page_token={urllib.parse.quote(token, safe='')}"
            d = _get_json(url, H)
            bars += (d.get("bars") or {}).get(sym, [])
            token = d.get("next_page_token")
            if not token:
                break
        name = sym.replace("/", "")
        _write_json(CRYPTO_DIR / f"{name}.json", {
            "meta": {"symbol": sym, "source": "alpaca_crypto_v1beta3_us_daily",
                     "start": CRYPTO_START, "end": DEV_BOUNDARY_T2,
                     "acquired_at": _now_utc(),
                     "bucket": "UTC calendar day, t = bucket start 00:00Z",
                     "isolation": "dev_bounded_max_bar_2025-06-30"},
            "bars": bars})
        print(f"  crypto {sym}: {len(bars)} bars "
              f"{_bar_date(bars[0]['t'])} -> {_bar_date(bars[-1]['t'])}")
        time.sleep(0.2)


def _yahoo_chart(sym: str, start: str, end: str) -> dict:
    p1 = int(datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    p2 = int((datetime.strptime(end, "%Y-%m-%d").replace(tzinfo=timezone.utc)
              + timedelta(days=1)).timestamp())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}"
           f"?period1={p1}&period2={p2}&interval=1d&events=div%7Csplit")
    return _yahoo_json(url)


def _yahoo_series(sym: str, start: str, end: str) -> dict:
    """Extract dated close/adjclose/dividend/split series from a Yahoo chart blob."""
    from zoneinfo import ZoneInfo
    res = _yahoo_chart(sym, start, end)["chart"]["result"][0]
    tz = ZoneInfo(res["meta"].get("exchangeTimezoneName", "America/New_York"))
    stamps = res.get("timestamp") or []
    closes = res["indicators"]["quote"][0].get("close") or []
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or []
    rows, arows = [], []
    for i, ts in enumerate(stamps):
        d = datetime.fromtimestamp(ts, tz).date().isoformat()
        if i < len(closes) and closes[i] is not None:
            rows.append({"date": d, "close": closes[i]})
        if i < len(adj) and adj[i] is not None:
            arows.append({"date": d, "adjclose": adj[i]})
    evs = res.get("events") or {}
    divs = sorted(({"date": datetime.fromtimestamp(v["date"], tz).date().isoformat(),
                    "amount": v["amount"]} for v in (evs.get("dividends") or {}).values()),
                  key=lambda r: r["date"])
    spl = sorted(({"date": datetime.fromtimestamp(v["date"], tz).date().isoformat(),
                   "numerator": v["numerator"], "denominator": v["denominator"]}
                  for v in (evs.get("splits") or {}).values()), key=lambda r: r["date"])
    return {"close": rows, "adjclose": arows, "dividends": divs, "splits": spl}


def acquire_yahoo() -> None:
    """Quarantined Yahoo datasets: (1) per-ticker adjclose TR validation series,
    dev window only; (2) Track 3 SPY/QQQ constructed split-adjusted books +
    dividends + quarantined TR, through DEV_BOUNDARY_T3 only; (3) ^IRX risk-free
    fallback. All under data/quarantine_yahoo/ — never committed, hashes recorded."""
    # (1) TR validation series (T-D3 comparators)
    for sym in roster_63():
        ys = YAHOO_SYMBOL.get(sym, sym)
        s = _yahoo_series(ys, TR_START, DEV_BOUNDARY_T2)
        _write_json(TR_DIR / f"{sym}.json", {
            "meta": {"symbol": sym, "yahoo_symbol": ys,
                     "source": "yahoo_v8_chart_adjclose", "start": TR_START,
                     "end": DEV_BOUNDARY_T2, "acquired_at": _now_utc(),
                     "role": "TOTAL-RETURN VALIDATION ONLY — quarantined (T-D4); "
                             "never merged into the primary path",
                     "isolation": "dev_bounded"},
            "adjclose": s["adjclose"],
            "close_raw": s["close"],
            "dividends_split_adjusted_yahoo": s["dividends"],
            "splits": s["splits"]})
        print(f"  tr {sym}: {len(s['adjclose'])} adjclose rows, "
              f"{len(s['dividends'])} div events")
        time.sleep(0.35)

    # (2) Track 3 books — raw close split-adjusted by cumulative forward factor
    for sym, start in (("SPY", T3_SPY_START), ("QQQ", T3_QQQ_START)):
        s = _yahoo_series(sym, start, DEV_BOUNDARY_T3)
        # Yahoo's v8 chart `close` series is already split-adjusted (verified
        # empirically at G1: QQQ's 2000-03-20 2:1 split shows no discontinuity in
        # the raw series, and re-dividing created one).  Identity transform; the
        # split events are retained as metadata.
        adj_close = [{"date": row["date"], "close": row["close"]} for row in s["close"]]
        _write_json(TRACK3_DIR / f"{sym}.json", {
            "meta": {"symbol": sym, "source": "yahoo_v8_chart_close",
                     "transformation": "none (Yahoo chart close is already "
                                       "split-adjusted, non-dividend-adjusted; "
                                       "verified against the QQQ 2000-03-20 split)",
                     "start": start, "end": DEV_BOUNDARY_T3,
                     "acquired_at": _now_utc(),
                     "isolation": "track3_dev_bounded_2020-12-31"},
            "close_split_adjusted": adj_close,
            "dividends_split_adjusted_yahoo": s["dividends"],
            "splits": s["splits"],
            "adjclose_quarantined_tr": s["adjclose"]})
        print(f"  track3 {sym}: {len(adj_close)} sessions, "
              f"{len(s['dividends'])} divs, splits={s['splits']}")
        time.sleep(0.35)

    # (3) ^IRX 13-week T-bill discount yield — risk-free fallback series
    s = _yahoo_series("^IRX", IRX_START, DEV_BOUNDARY_T2)
    _write_json(RATES_DIR / "irx_13w_tbill.json", {
        "meta": {"symbol": "^IRX", "source": "yahoo_v8_chart",
                 "unit": "percent_discount_yield",
                 "role": "risk-free fallback series (primary Treasury/FRED/NYFed "
                         "sources are proxy-policy-blocked in this environment; "
                         "protocol §10 disclosed-fallback-band provision)",
                 "start": IRX_START, "end": DEV_BOUNDARY_T2,
                 "acquired_at": _now_utc(), "isolation": "dev_bounded"},
        "close": s["close"]})
    print(f"  rates ^IRX: {len(s['close'])} rows")


def inventory_existing_cache() -> list[dict]:
    rows = []
    for f in sorted(BACKTEST_CACHE.glob("*.json")):
        bars = json.loads(f.read_text())
        rows.append({"file": f"data/backtest/{f.name}", "bars": len(bars),
                     "first": _bar_date(bars[0]["t"]), "last": _bar_date(bars[-1]["t"]),
                     "sha256": sha256_file(f)})
    return rows


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def _load_prices(sym: str) -> dict:
    return json.loads((PRICES_DIR / f"{sym}.json").read_text())


def validate(report_path: Path | None = None) -> bool:
    """All deterministic G1 validators. Read-only. Returns overall pass/fail
    for the checks that are decidable from acquired data alone."""
    out: list[str] = []
    ok = True

    def say(s: str) -> None:
        out.append(s)
        print(s)

    syms = roster_63()
    say(f"roster_63: {len(syms)} tickers")

    # ---- price cache (research-side) ----
    spy_sessions_dev: list[str] = []
    spy_all = [_bar_date(b["t"]) for b in _load_prices("SPY")["bars"]]
    spy_sessions_dev = [d for d in spy_all if d <= DEV_BOUNDARY_T2]
    say("\n== research price cache ==")
    stale, disc_flags = [], []
    for sym in syms:
        doc = _load_prices(sym)
        assert doc["meta"]["symbol"] == sym, f"identity mismatch {sym}"
        bars = doc["bars"]
        dates = [_bar_date(b["t"]) for b in bars]
        dup = len(dates) - len(set(dates))
        nonpos = sum(1 for b in bars if min(b["o"], b["h"], b["l"], b["c"]) <= 0)
        # missing sessions vs SPY calendar, dev window, post-listing only
        first = dates[0]
        expect = [d for d in spy_sessions_dev if d >= first]
        have = set(d for d in dates if d <= DEV_BOUNDARY_T2)
        missing = [d for d in expect if d not in have]
        # discontinuity scan — DEV WINDOW ONLY (untouched returns never computed)
        devbars = [b for b in bars if _bar_date(b["t"]) <= DEV_BOUNDARY_T2]
        jumps = []
        for i in range(1, len(devbars)):
            r = devbars[i]["c"] / devbars[i - 1]["c"] - 1.0
            if abs(r) > DISCONTINUITY_ABS_RET:
                jumps.append((_bar_date(devbars[i]["t"]), round(r, 4)))
        if jumps:
            disc_flags.append((sym, jumps))
        if dates[-1] != spy_all[-1]:
            stale.append((sym, dates[-1]))
        bad = dup or nonpos or (len(missing) > 3)
        if bad:
            ok = False
        say(f"  {sym}: {len(bars)} bars {dates[0]}->{dates[-1]} "
            f"dup={dup} nonpos={nonpos} missing_dev={len(missing)}"
            + (f" MISSING={missing[:5]}" if missing else "")
            + (" FAIL" if bad else ""))
    say(f"  stale_end (last bar != SPY last {spy_all[-1]}): {stale or 'none'}")
    say(f"  discontinuity flags (dev window, |ret|>{DISCONTINUITY_ABS_RET}): "
        f"{disc_flags or 'none'}")

    # cross-check vs production cache on overlap (identical vendor, adjustment)
    say("\n== cross-check vs data/backtest (overlap, dev window) ==")
    mism_total = 0
    for sym in syms:
        f = BACKTEST_CACHE / f"{sym}.json"
        if not f.exists():
            say(f"  {sym}: no production cache file (skip)")
            continue
        prod = {_bar_date(b["t"]): b["c"] for b in json.loads(f.read_text())
                if _bar_date(b["t"]) <= DEV_BOUNDARY_T2}
        res = {_bar_date(b["t"]): b["c"] for b in _load_prices(sym)["bars"]
               if _bar_date(b["t"]) <= DEV_BOUNDARY_T2}
        common = sorted(set(prod) & set(res))
        mism = [d for d in common if abs(prod[d] - res[d]) > 1e-9 * max(1.0, abs(prod[d]))
                and abs(prod[d] - res[d]) > 0.005]
        if mism:
            mism_total += len(mism)
            say(f"  {sym}: {len(mism)}/{len(common)} closes differ "
                f"(first {mism[0]}: prod {prod[mism[0]]} vs res {res[mism[0]]})")
    say(f"  total differing closes: {mism_total} (re-adjustment or vendor revision "
        f"if nonzero — investigate before relying on either copy)")

    # ---- dividend ledger ----
    say("\n== dividend ledger ==")
    led = json.loads((DIV_DIR / "dividend_ledger.json").read_text())
    rows = led["dividends"]
    say(f"  events: {len(rows)}")
    keys = [(r["symbol"], r["ex_date"], r["special"]) for r in rows]
    dupk = len(keys) - len(set(keys))
    fut = [r for r in rows if r["ex_date"] > DEV_BOUNDARY_T2]
    neg = [r for r in rows if r["rate_split_adjusted"] <= 0]
    chron = [r for r in rows if r.get("payable_date") and r["payable_date"] < r["ex_date"]]
    paydate = sum(1 for r in rows if r.get("payable_date"))
    if dupk or fut or neg or chron:
        ok = False
    say(f"  duplicate (symbol,ex_date,special) keys: {dupk}")
    say(f"  future-date leakage past {DEV_BOUNDARY_T2}: {len(fut)}")
    say(f"  nonpositive amounts: {len(neg)}")
    say(f"  payable_date < ex_date: {len(chron)}")
    say(f"  payable_date availability: {paydate}/{len(rows)}")
    payers = {}
    for r in rows:
        payers.setdefault(r["symbol"], 0)
        payers[r["symbol"]] += 1
    nonpayers = [s for s in syms if s not in payers]
    say(f"  payers: {len(payers)}; non-payers in window: {sorted(nonpayers)}")

    # cross-source agreement vs quarantined Yahoo event lists (full roster)
    say("\n== dividend cross-source agreement (Alpaca vs Yahoo, dev window) ==")
    agree = disagree = a_only = y_only = 0
    detail: list[str] = []
    for sym in syms:
        trf = TR_DIR / f"{sym}.json"
        if not trf.exists():
            detail.append(f"  {sym}: no TR file (skip)")
            continue
        ydoc = json.loads(trf.read_text())
        yd = {r["date"]: r["amount"] for r in ydoc["dividends_split_adjusted_yahoo"]
              if TR_START <= r["date"] <= DEV_BOUNDARY_T2}
        ad = {}
        for r in rows:
            if r["symbol"] == sym and r["ex_date"] >= TR_START:
                ad[r["ex_date"]] = ad.get(r["ex_date"], 0.0) + r["rate_split_adjusted"]
        for d0, amt in ad.items():
            match = None
            for dd in (d0,) + tuple((date.fromisoformat(d0) + timedelta(days=k)).isoformat()
                                    for k in (-1, 1, -2, 2)):
                if dd in yd:
                    match = yd[dd]
                    break
            if match is None:
                a_only += 1
                detail.append(f"  {sym} {d0} ${amt:.4f}: Alpaca-only")
            elif abs(match - amt) <= max(0.0006, 0.006 * amt):
                agree += 1
            else:
                disagree += 1
                detail.append(f"  {sym} {d0}: Alpaca {amt:.4f} vs Yahoo {match:.4f} DISAGREE")
        for d0 in yd:
            near = any(abs((date.fromisoformat(d0) - date.fromisoformat(a)).days) <= 2
                       for a in ad)
            if not near:
                y_only += 1
                detail.append(f"  {sym} {d0} ${yd[d0]:.4f}: Yahoo-only")
    say(f"  agree={agree} disagree={disagree} alpaca_only={a_only} yahoo_only={y_only}")
    for line in detail[:60]:
        say(line)
    if disagree or y_only:
        say("  NOTE: disagreements/Yahoo-only events require cause analysis in the report")

    # spinoff scan: Yahoo pseudo-split events (spinoff price scalings) that are
    # NOT real splits in the Alpaca split ledger — these mark tickers where the
    # split-adjusted primary path and Yahoo TR diverge by construction.
    say("\n== spinoff scan (Yahoo pseudo-splits vs Alpaca real splits) ==")
    real = json.loads((DIV_DIR / "splits.json").read_text())["splits"]
    realset = {(r["symbol"], r["ex_date"]) for r in real}
    for sym in syms:
        trf = TR_DIR / f"{sym}.json"
        if not trf.exists():
            continue
        for sp in json.loads(trf.read_text())["splits"]:
            near = any(rs == sym and abs((date.fromisoformat(sp["date"])
                                          - date.fromisoformat(rd)).days) <= 3
                       for rs, rd in realset)
            ratio = sp["numerator"] / sp["denominator"]
            if not near:
                say(f"  {sym} {sp['date']} factor {ratio:.4f}: Yahoo-only pseudo-split "
                    f"(spinoff/in-kind distribution scaling — primary path diverges)")

    # ---- crypto ----
    say("\n== crypto bars ==")
    for symfile in ("BTCUSD", "ETHUSD", "SOLUSD"):
        doc = json.loads((CRYPTO_DIR / f"{symfile}.json").read_text())
        bars = doc["bars"]
        dates = [_bar_date(b["t"]) for b in bars]
        dup = len(dates) - len(set(dates))
        nonpos = sum(1 for b in bars if min(b["o"], b["h"], b["l"], b["c"]) <= 0)
        notmid = sum(1 for b in bars if not b["t"].endswith("T00:00:00Z"))
        d0, d1 = date.fromisoformat(dates[0]), date.fromisoformat(dates[-1])
        expected = (d1 - d0).days + 1
        missing = expected - len(set(dates))
        gaps = []
        prev = d0
        for ds in dates[1:]:
            cur = date.fromisoformat(ds)
            if (cur - prev).days > 1:
                gaps.append((prev.isoformat(), cur.isoformat(), (cur - prev).days - 1))
            prev = cur
        fut = [d for d in dates if d > DEV_BOUNDARY_T2]
        weekend_note = "24/7 series — weekend bars expected and required"
        bad = dup or nonpos or notmid or fut or missing > max(3, 0.005 * expected) \
            or any(g[2] > 3 for g in gaps)
        if bad:
            ok = False
        say(f"  {symfile}: {len(bars)} bars {dates[0]}->{dates[-1]} dup={dup} "
            f"nonpos={nonpos} non-midnight-utc={notmid} missing_days={missing} "
            f"max_gap={max((g[2] for g in gaps), default=0)} "
            f"future_leak={len(fut)} ({weekend_note})" + (" FAIL" if bad else ""))
        if gaps:
            say(f"    gaps: {gaps[:10]}")
        # calendar rule: every dev-window equity session must have a crypto close
        # at or before the session close: bar for UTC day (session-1) or earlier
        # within 5 days.  Bars bucket at 00:00Z; bar t=D closes 00:00Z on D+1 =
        # 19:00/20:00 ET on D, i.e. AFTER the 16:00 ET equity close on D — so the
        # qualifying bar for session D is t=D-1 (or the most recent earlier bar).
        dset = set(dates)
        unmapped = []
        for sess in spy_sessions_dev:
            if sess < CRYPTO_START or sess <= dates[0]:
                continue
            sd = date.fromisoformat(sess)
            if not any((sd - timedelta(days=k)).isoformat() in dset for k in range(1, 6)):
                unmapped.append(sess)
        if unmapped:
            ok = False
        say(f"    equity-session mapping (last crypto close <= equity close, "
            f"t-1 rule): unmapped sessions = {unmapped or 0}")

    # ---- Track 3 books ----
    say("\n== Track 3 books (constructed split-adjusted, Yahoo) ==")
    for sym in ("SPY", "QQQ"):
        f = TRACK3_DIR / f"{sym}.json"
        if not f.exists():
            say(f"  {sym}: MISSING")
            ok = False
            continue
        doc = json.loads(f.read_text())
        rows3 = doc["close_split_adjusted"]
        dates = [r["date"] for r in rows3]
        dup = len(dates) - len(set(dates))
        nonpos = sum(1 for r in rows3 if r["close"] <= 0)
        over = [d for d in dates if d > DEV_BOUNDARY_T3]
        jumps = []
        for i in range(1, len(rows3)):
            r = rows3[i]["close"] / rows3[i - 1]["close"] - 1.0
            if abs(r) > DISCONTINUITY_ABS_RET:
                jumps.append((dates[i], round(r, 4)))
        if dup or nonpos or over or jumps:
            ok = False
        say(f"  {sym}: {len(rows3)} sessions {dates[0]}->{dates[-1]} dup={dup} "
            f"nonpos={nonpos} beyond_t3_boundary={len(over)} "
            f"splits={doc['splits']} discontinuities={jumps or 'none'} "
            f"divs={len(doc['dividends_split_adjusted_yahoo'])}")

    # ---- rates ----
    say("\n== rates ==")
    f = RATES_DIR / "irx_13w_tbill.json"
    if f.exists():
        doc = json.loads(f.read_text())
        vals = [r["close"] for r in doc["close"]]
        dates = [r["date"] for r in doc["close"]]
        weird = sum(1 for v in vals if not (-1.0 <= v <= 20.0))
        say(f"  ^IRX: {len(vals)} rows {dates[0]}->{dates[-1]} "
            f"out_of_range={weird}")
        if weird:
            ok = False
    else:
        say("  ^IRX: MISSING")
        ok = False
    say("  fed_funds_effective: NOT ACQUIRED — every primary source "
        "(fred.stlouisfed.org, api.stlouisfed.org, federalreserve.gov, "
        "markets.newyorkfed.org, treasury.gov) is blocked by the environment "
        "network policy (CONNECT 403). BLOCKER recorded in the manifest.")

    # ---- untouched-boundary summary ----
    say("\n== untouched-test boundary status ==")
    maxdiv = max(r["ex_date"] for r in rows)
    say(f"  dividend ledger max ex_date: {maxdiv} (must be <= {DEV_BOUNDARY_T2}): "
        f"{'OK' if maxdiv <= DEV_BOUNDARY_T2 else 'FAIL'}")
    for symfile in ("BTCUSD", "ETHUSD", "SOLUSD"):
        doc = json.loads((CRYPTO_DIR / f"{symfile}.json").read_text())
        m = max(_bar_date(b["t"]) for b in doc["bars"])
        say(f"  crypto {symfile} max bar: {m} <= {DEV_BOUNDARY_T2}: "
            f"{'OK' if m <= DEV_BOUNDARY_T2 else 'FAIL'}")
    for sym in ("SPY", "QQQ"):
        doc = json.loads((TRACK3_DIR / f"{sym}.json").read_text())
        m = max(r["date"] for r in doc["close_split_adjusted"])
        say(f"  track3 {sym} max session: {m} <= {DEV_BOUNDARY_T3}: "
            f"{'OK' if m <= DEV_BOUNDARY_T3 else 'FAIL'}")
    for sym in syms[:1]:
        pass
    trmax = "0000"
    for sym in syms:
        f2 = TR_DIR / f"{sym}.json"
        if f2.exists():
            doc = json.loads(f2.read_text())
            if doc["adjclose"]:
                trmax = max(trmax, doc["adjclose"][-1]["date"])
    say(f"  TR validation series max date: {trmax} <= {DEV_BOUNDARY_T2}: "
        f"{'OK' if trmax <= DEV_BOUNDARY_T2 else 'FAIL'}")
    say(f"  research price cache: extends to run date {RUN_DATE} BY CHARTER "
        f"DIRECTION (G1 gate: 'refreshed through the run date'); development "
        f"consumption barred; loader truncation is gate-G2 work (T-U1); no "
        f"return-derived statistic in this validator touches any date past "
        f"{DEV_BOUNDARY_T2}.")

    say(f"\nVALIDATE OVERALL: {'PASS' if ok else 'FAIL'}")
    if report_path:
        report_path.write_text("\n".join(out) + "\n")
    return ok


# --------------------------------------------------------------------------
# T-D3 reconciliation
# --------------------------------------------------------------------------

def _cagr(v0: float, v1: float, days: int) -> float:
    yrs = days / 365.25
    return (v1 / v0) ** (1.0 / yrs) - 1.0


def _bh_with_dividends(closes: dict[str, float], sessions: list[str],
                       divs: dict[str, float]) -> float:
    """Buy-and-hold 1 share from first session; dividends credited on ex_date and
    reinvested at that session's close. Returns final value / initial value."""
    shares = 1.0
    for dsess in sessions[1:]:
        amt = divs.get(dsess)
        if amt:
            shares += shares * amt / closes[dsess]
    return shares * closes[sessions[-1]] / closes[sessions[0]]


def reconcile(report_path: Path | None = None) -> bool:
    """T-D3: primary path (split-adjusted prices + explicit PIT dividend cash,
    reinvested) vs quarantined Yahoo TR (adjclose), per ticker, dev window only.
    Tolerance ±0.3pp/yr (pre_registration.yaml dividends.reconciliation_tolerance)."""
    out: list[str] = []
    okall = True

    def say(s: str) -> None:
        out.append(s)
        print(s)

    led = json.loads((DIV_DIR / "dividend_ledger.json").read_text())
    by_sym: dict[str, dict[str, float]] = {}
    for r in led["dividends"]:
        by_sym.setdefault(r["symbol"], {})
        by_sym[r["symbol"]][r["ex_date"]] = \
            by_sym[r["symbol"]].get(r["ex_date"], 0.0) + r["rate_split_adjusted"]

    say("== T-D3 reconciliation (Track 2 roster, dev window, tolerance "
        f"±{TD3_TOLERANCE_PP}pp/yr) ==")
    say("ticker | window | yrs | primary CAGR | TR CAGR | diff pp/yr | verdict")
    fails = []
    for sym in roster_63():
        pdoc = _load_prices(sym)
        closes = {_bar_date(b["t"]): b["c"] for b in pdoc["bars"]
                  if "2021-06-01" <= _bar_date(b["t"]) <= DEV_BOUNDARY_T2}
        tdoc = json.loads((TR_DIR / f"{sym}.json").read_text())
        adj = {r["date"]: r["adjclose"] for r in tdoc["adjclose"]
               if "2021-06-01" <= r["date"] <= DEV_BOUNDARY_T2}
        yraw = {r["date"]: r["close"] for r in tdoc["close_raw"]
                if "2021-06-01" <= r["date"] <= DEV_BOUNDARY_T2}
        sessions = sorted(set(closes) & set(adj))
        if len(sessions) < 60:
            say(f"{sym} | insufficient overlap ({len(sessions)}) | SKIP-FAIL")
            okall = False
            continue
        days = (date.fromisoformat(sessions[-1]) - date.fromisoformat(sessions[0])).days
        divs = by_sym.get(sym, {})
        # map any ex_date to nearest covered session (holiday shifts)
        dmap: dict[str, float] = {}
        sset = set(sessions)
        for d0, amt in divs.items():
            if d0 < sessions[0] or d0 > sessions[-1]:
                continue
            dd = d0
            k = 0
            while dd not in sset and k < 5:
                k += 1
                dd = (date.fromisoformat(d0) + timedelta(days=k)).isoformat()
            if dd in sset:
                dmap[dd] = dmap.get(dd, 0.0) + amt
        g_primary = _bh_with_dividends(closes, sessions, dmap)
        g_tr = adj[sessions[-1]] / adj[sessions[0]]
        c_p = _cagr(1.0, g_primary, days)
        c_t = _cagr(1.0, g_tr, days)
        diff = abs(c_p - c_t) * 100.0
        verdict = "PASS" if diff <= TD3_TOLERANCE_PP else "FAIL"
        if verdict == "FAIL":
            okall = False
            # attribution: same computation with Yahoo raw closes as the price leg
            g_yraw = _bh_with_dividends(yraw, [s for s in sessions if s in yraw], dmap) \
                if all(s in yraw for s in (sessions[0], sessions[-1])) else float("nan")
            c_y = _cagr(1.0, g_yraw, days) if g_yraw == g_yraw else float("nan")
            fails.append((sym, diff, abs(c_y - c_t) * 100.0 if c_y == c_y else None))
        say(f"{sym} | {sessions[0]}->{sessions[-1]} | {days/365.25:.2f} | "
            f"{c_p*100:.3f}% | {c_t*100:.3f}% | {diff:.3f} | {verdict}")

    say("\n== T-D3 Track 3 books (same-source construction check) ==")
    for sym in ("SPY", "QQQ"):
        doc = json.loads((TRACK3_DIR / f"{sym}.json").read_text())
        closes = {r["date"]: r["close"] for r in doc["close_split_adjusted"]}
        adj = {r["date"]: r["adjclose"] for r in doc["adjclose_quarantined_tr"]}
        sessions = sorted(set(closes) & set(adj))
        start = max(sessions[0], "1999-01-04")
        sessions = [s for s in sessions if s >= start]
        days = (date.fromisoformat(sessions[-1]) - date.fromisoformat(sessions[0])).days
        divs = {r["date"]: r["amount"] for r in doc["dividends_split_adjusted_yahoo"]}
        sset = set(sessions)
        dmap = {}
        for d0, amt in divs.items():
            if d0 < sessions[0] or d0 > sessions[-1]:
                continue
            dd, k = d0, 0
            while dd not in sset and k < 5:
                k += 1
                dd = (date.fromisoformat(d0) + timedelta(days=k)).isoformat()
            if dd in sset:
                dmap[dd] = dmap.get(dd, 0.0) + amt
        g_primary = _bh_with_dividends(closes, sessions, dmap)
        g_tr = adj[sessions[-1]] / adj[sessions[0]]
        c_p, c_t = _cagr(1.0, g_primary, days), _cagr(1.0, g_tr, days)
        diff = abs(c_p - c_t) * 100.0
        verdict = "PASS" if diff <= TD3_TOLERANCE_PP else "FAIL"
        if verdict == "FAIL":
            okall = False
        say(f"{sym} | {sessions[0]}->{sessions[-1]} | {days/365.25:.2f}y | "
            f"{c_p*100:.3f}% | {c_t*100:.3f}% | {diff:.3f} | {verdict}")

    if fails:
        say("\nFailure attribution (diff with Yahoo-raw price leg, isolates "
            "price-source noise from ledger errors):")
        for sym, d1, d2 in fails:
            say(f"  {sym}: alpaca-leg diff {d1:.3f}pp/yr; yahoo-raw-leg diff "
                f"{'n/a' if d2 is None else f'{d2:.3f}pp/yr'}")
    say(f"\nT-D3 OVERALL: {'PASS' if okall else 'FAIL'}")
    if report_path:
        report_path.write_text("\n".join(out) + "\n")
    return okall


# --------------------------------------------------------------------------

def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "prices":
        acquire_prices()
    elif cmd == "dividends":
        acquire_dividends()
    elif cmd == "crypto":
        acquire_crypto()
    elif cmd == "yahoo":
        acquire_yahoo()
    elif cmd == "inventory":
        print(json.dumps(inventory_existing_cache(), indent=1))
    elif cmd == "validate":
        return 0 if validate() else 1
    elif cmd == "reconcile":
        return 0 if reconcile() else 1
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
