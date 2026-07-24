"""
data_acquisition.py — MARGIN-0005 G1 data acquisition and validation (v2, remediation).

Authority: governance/decisions/MARGIN-0005-margin-target-research-charter.md §1.2
(G1 data-acquisition steps, cached read-only under the research directory) and §4
(approved research-package file list, which names this module).

Scope guards (charter §2, PROTOCOL_V2.md §11, pre_registration.yaml):
  * DATA acquisition and DATA validation only. Never calls simulate(), never
    consumes a registered trial, never produces a margin signal, ranking, or
    recommendation, never places an order.
  * Writes ONLY under research/margin_target_study/data/ (production read-only).
  * Untouched-test isolation is STRUCTURAL as of v2: development-visible price
    files are truncated at the Track 2 development boundary (2025-06-30) at
    acquisition time; the post-boundary segment (charter G1: cache "refreshed
    through the run date") is split off into a SEALED archive
    (data/untouched_sealed/) whose contents no G1 or development code opens —
    validation of the sealed archive is byte-level (SHA-256) only. Unsealing is
    a G4-runner act under the candidate-freeze rules. Track 3 untouched data
    (2021-01-01 →) is never acquired at all. Loader-level enforcement (T-U1)
    remains a G2 obligation for the future research loader.
  * Total-return (adjclose) series are quarantined under data/quarantine_yahoo/
    and used exactly once, in `reconcile` (T-D3). Never merged into any primary
    dataset (protocol §4, T-D4).

Primary accounting path (principal direction D-1/D-2, 2026-07-24):
    split-adjusted, non-total-return prices
  + explicit GROSS DECLARED point-in-time cash dividends (pre-tax)
  + explicit point-in-time non-cash corporate actions (spin-offs, valued at the
    distributed security's consolidated close on the parent's ex-distribution
    session, cash-in-lieu convention for fractions)
Foreign withholding, ADR depositary fees, and broker net-cash treatment are
recorded SEPARATELY (data/dividends/withholding_register.yaml) as source-backed
sensitivities — never silently netted into the declared amount.

Sources:
  * Alpaca Market Data — split-adjusted daily bars (feed=iex; documented
    ticker-specific exception: GEV uses feed=sip, see GEV_FEED_EXCEPTION),
    v1 corporate actions (cash dividends, splits, spin-offs), v1beta3 crypto.
    Committed (repository precedent: data/backtest/).
  * Yahoo Finance chart API via curl_cffi impersonate="chrome110" (repository
    fingerprint, earnings.py) — quarantined TR validation series, Track 3
    books, ^IRX. NOT committed (licensing); reproducible; hashes recorded.
  * FRED DFF (Federal Funds Effective) — network-blocked in this environment;
    ingested from a principal-supplied fredgraph CSV via the `dff` subcommand.

Subcommands:
  prices      acquire roster bars; write dev-truncated files + sealed archive
  dividends   acquire gross-declared PIT dividend ledger v2 (+ splits)
  corpactions acquire/record PIT spin-off ledger with valuation evidence
  crypto      acquire BTC/ETH/SOL daily bars (2021-06-01 -> 2025-06-30)
  yahoo       acquire quarantined Yahoo datasets (TR validation, Track 3, ^IRX)
  dff <csv>   validate + ingest principal-supplied FRED DFF CSV; emit the
              Robinhood-observation reconstruction comparison
  inventory   hash + coverage inventory of the legacy data/backtest cache
  validate    run all deterministic G1 validators (read-only)
  reconcile   T-D3 reconciliation (primary path incl. corporate actions vs TR)
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import ssl
import sys
import tarfile
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
SEALED_DIR = DATA / "untouched_sealed"
SEALED_ARCHIVE = SEALED_DIR / "untouched_prices.tar.gz"
SEALED_INDEX = SEALED_DIR / "SEALED_INDEX.json"
DIV_DIR = DATA / "dividends"
CA_DIR = DATA / "corporate_actions"
CRYPTO_DIR = DATA / "crypto"
RATES_DIR_COMMITTED = DATA / "rates"
QUAR = DATA / "quarantine_yahoo"
TR_DIR = QUAR / "tr"
TRACK3_DIR = QUAR / "track3"
RATES_DIR = QUAR / "rates"
BACKTEST_CACHE = REPO / "data" / "backtest"

# ---- governed boundaries (pre_registration.yaml) ----
DEV_BOUNDARY_T2 = "2025-06-30"
DEV_BOUNDARY_T3 = "2020-12-31"
PRICE_START = "2020-07-01"
RUN_DATE = "2026-07-23"                   # last complete session at G1 execution
DIV_START = "2020-07-01"
CRYPTO_START = "2021-06-01"
TR_START = "2021-05-01"
T3_SPY_START = "1993-01-29"
T3_QQQ_START = "1999-03-10"
IRX_START = "1999-01-01"
DFF_START = "1999-01-01"

EXCLUDE = {"SPCX", "SKHY"}                # roster_63 convention (backtest_regime.py)
CRYPTO_SYMS = ("BTC/USD", "ETH/USD", "SOL/USD")
YAHOO_SYMBOL = {"BRK.B": "BRK-B"}

# Documented ticker-specific source exception (G1 remediation, decision D-3
# outcome A): GEV's IEX prints deviate from the consolidated tape on multiple
# dated sessions (worst 2024-12-23: 344.92 SIP vs 339.34 IEX, 1.618%; also
# 2024-09-17 0.573%, 2024-04-02 0.286%) — enough to breach the T-D3 tolerance
# over its short 1.24y listing window.  GEV therefore uses Alpaca's SIP
# (consolidated) historical feed; same vendor, same API, same adjustment mode.
GEV_FEED_EXCEPTION = {"GEV": "sip"}

# Hand-authored PIT spin-off records for events predating the vendor
# corporate-actions feed's spin_off coverage (which returns DHR/VLTO 2023 and
# WDC/SNDK 2025 but nothing for 2021).  Sources are primary/issuer documents.
HAND_AUTHORED_SPINOFFS = [
    {"parent": "IBM", "child": "KD", "ratio": 0.2,
     "announcement_date": "2020-10-08", "record_date": "2021-10-25",
     "distribution_date": "2021-11-03", "parent_ex_session": "2021-11-04",
     "cash_in_lieu": "fractional KD shares paid in cash by the distribution agent",
     "source": "IBM Form 8-K ex-99.1 (SEC EDGAR 51143/000110465921125064) + "
               "IBM investor FAQ + Kyndryl IR spin-off information page",
     "source_classification": "primary_issuer_filing_hand_recorded",
     "note": "1 KD per 5 IBM; distribution after close 2021-11-03; IBM traded "
             "ex-distribution 2021-11-04 (Yahoo pseudo-split factor 1.046 dated "
             "2021-11-04 corroborates)"},
    {"parent": "MRK", "child": "OGN", "ratio": 0.1,
     "announcement_date": "2020-02-05", "record_date": "2021-05-17",
     "distribution_date": "2021-06-02", "parent_ex_session": "2021-06-03",
     "cash_in_lieu": "fractional OGN shares paid in cash",
     "source": "Merck news release 2021-05-07 'Merck Declares Record Date and "
               "Dividend for the Organon & Co. Spinoff' (merck.com) + Form 10",
     "source_classification": "primary_issuer_announcement_hand_recorded",
     "note": "0.1 OGN per MRK; distributed 2021-06-02; MRK ex-distribution "
             "session 2021-06-03 (Yahoo factor 1.048 dated 2021-06-03 corroborates)"},
]
# Announcement dates for the vendor-supplied rows (vendor feed carries no
# announcement field); hand-recorded from issuer announcements.
SPINOFF_ANNOUNCEMENTS = {
    ("DHR", "VLTO"): ("2022-09-14", "Danaher announcement of intent to separate "
                                    "its Environmental & Applied Solutions segment"),
    ("WDC", "SNDK"): ("2023-10-30", "Western Digital board decision to separate "
                                    "HDD and Flash businesses"),
}

DISCONTINUITY_ABS_RET = 0.45
TD3_TOLERANCE_PP = 0.3

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
        except Exception as e:  # noqa: BLE001
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
    return hashlib.sha256(p.read_bytes()).hexdigest()


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


def _fetch_stock_bars(sym: str, start: str, end: str, feed: str) -> list[dict]:
    H = _alpaca_headers()
    q = urllib.parse.quote(sym, safe="")
    bars, token = [], None
    while True:
        url = (f"https://data.alpaca.markets/v2/stocks/{q}/bars"
               f"?timeframe=1Day&adjustment=split&feed={feed}"
               f"&start={start}&end={end}T23%3A59%3A59Z&limit=10000")
        if token:
            url += f"&page_token={urllib.parse.quote(token, safe='')}"
        d = _get_json(url, _alpaca_headers())
        bars += d.get("bars") or []
        token = d.get("next_page_token")
        if not token:
            break
    return bars


# --------------------------------------------------------------------------
# acquisition
# --------------------------------------------------------------------------

def acquire_prices() -> None:
    """Roster split-adjusted daily bars, PRICE_START -> RUN_DATE (charter G1:
    'refreshed through the run date').  Development-visible files are truncated
    at DEV_BOUNDARY_T2; the post-boundary segment goes into the sealed archive
    with structural integrity recorded at seal time (counts and pass/fail only —
    no values leave the archive)."""
    sealed_members: dict[str, bytes] = {}
    sealed_meta: dict[str, dict] = {}
    for sym in roster_63():
        feed = GEV_FEED_EXCEPTION.get(sym, "iex")
        bars = _fetch_stock_bars(sym, PRICE_START, RUN_DATE, feed)
        dev = [b for b in bars if _bar_date(b["t"]) <= DEV_BOUNDARY_T2]
        unt = [b for b in bars if _bar_date(b["t"]) > DEV_BOUNDARY_T2]
        _write_json(PRICES_DIR / f"{sym}.json", {
            "meta": {"symbol": sym, "source": f"alpaca_{feed}_daily",
                     "adjustment": "split", "feed": feed,
                     "feed_exception": sym in GEV_FEED_EXCEPTION,
                     "start": PRICE_START, "end": DEV_BOUNDARY_T2,
                     "acquired_at": _now_utc(),
                     "isolation": "dev_truncated_at_acquisition; post-boundary "
                                  "segment sealed in data/untouched_sealed/"},
            "bars": dev})
        # structural integrity of the untouched segment, computed once at seal
        # time; only counts/booleans are retained outside the archive.
        udates = [_bar_date(b["t"]) for b in unt]
        sealed_meta[sym] = {
            "rows": len(unt),
            "coverage": f"{udates[0]} -> {udates[-1]}" if unt else "EMPTY",
            "duplicates": len(udates) - len(set(udates)),
            "nonpositive": sum(1 for b in unt
                               if min(b["o"], b["h"], b["l"], b["c"]) <= 0),
        }
        sealed_members[f"{sym}.json"] = json.dumps(unt).encode()
        print(f"  prices {sym} [{feed}]: dev={len(dev)} "
              f"({_bar_date(dev[0]['t'])}->{_bar_date(dev[-1]['t'])}) "
              f"sealed={len(unt)}")
        time.sleep(0.15)

    # deterministic tar.gz (fixed mtimes/owners) so the sealed hash is reproducible
    SEALED_DIR.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        for name in sorted(sealed_members):
            data = sealed_members[name]
            ti = tarfile.TarInfo(name=name)
            ti.size = len(data)
            ti.mtime = 0
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            tf.addfile(ti, io.BytesIO(data))
    with open(SEALED_ARCHIVE, "wb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", mtime=0) as gz:
            gz.write(buf.getvalue())
    _write_json(SEALED_INDEX, {
        "meta": {"sealed_at": _now_utc(),
                 "boundary": DEV_BOUNDARY_T2, "run_date": RUN_DATE,
                 "rule": "UNTOUCHED-TEST SEGMENT — G4-runner unseal only, after "
                         "the candidate freeze (charter §6; pre_registration "
                         "untouched_test_isolation). No G1/G2/G3 code may open "
                         "the archive; integrity checks are byte-level (SHA-256).",
                 "archive": "untouched_prices.tar.gz",
                 "archive_sha256": sha256_file(SEALED_ARCHIVE)},
        "members": sealed_meta})
    print(f"  sealed archive: {SEALED_ARCHIVE.name} "
          f"sha256={sha256_file(SEALED_ARCHIVE)[:16]}…")


def acquire_dividends() -> None:
    """Gross-declared PIT dividend ledger v2 (principal direction D-2) + splits.

    Gross determination rule (deterministic, per event):
      1. Vendor rows are deduped and split-adjusted as in v1.
      2. For tickers whose Yahoo history is spinoff-scaled (pseudo-split
         tickers), the vendor amount IS the declared gross — Yahoo is unusable
         as a gross reference there.
      3. Otherwise each vendor amount is matched to the quarantined Yahoo gross
         event (±2d).  Match within 0.6% -> corroborated gross (vendor value).
         Vendor < Yahoo by more (net-of-withholding / fee convention) ->
         gross := Yahoo amount, vendor amount retained as vendor_net.
         Vendor > Yahoo -> vendor value kept, flagged anomaly.
         Unmatched -> vendor value kept, flagged uncorroborated.
    Withholding/fee conventions live in withholding_register.yaml — separate,
    never netted into gross."""
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

    raw_divs = _fetch("cash_dividend", DIV_START, "2025-10-31").get("cash_dividends", [])
    divs, seen = [], set()
    for d in raw_divs:
        if d["ex_date"] > DEV_BOUNDARY_T2:
            continue
        k = (d["symbol"], d["ex_date"], d["rate"], bool(d.get("special")))
        if k in seen:
            continue
        seen.add(k)
        divs.append(d)
    sp = _fetch("forward_split,reverse_split", DIV_START, RUN_DATE)
    splits = sp.get("forward_splits", []) + sp.get("reverse_splits", [])

    factors: dict[str, list[tuple[str, float]]] = {}
    for s in splits:
        factors.setdefault(s["symbol"], []).append(
            (s["ex_date"], float(s["new_rate"]) / float(s["old_rate"])))

    # Yahoo gross references + pseudo-split (spinoff-scaled) ticker set
    yahoo_div: dict[str, dict[str, float]] = {}
    spinoff_scaled: set[str] = set()
    real_split_keys = {(s["symbol"], s["ex_date"]) for s in splits}
    for sym in syms:
        trf = TR_DIR / f"{sym}.json"
        if not trf.exists():
            continue
        ydoc = json.loads(trf.read_text())
        yahoo_div[sym] = {r["date"]: r["amount"]
                          for r in ydoc["dividends_split_adjusted_yahoo"]}
        for spv in ydoc["splits"]:
            near = any(rs == sym and abs((date.fromisoformat(spv["date"])
                                          - date.fromisoformat(rd)).days) <= 3
                       for rs, rd in real_split_keys)
            if not near:
                spinoff_scaled.add(sym)

    # Gross determination runs at (symbol, ex_date) AGGREGATE level: issuers can
    # declare a regular and a special dividend on the same ex-date as separate
    # vendor rows while Yahoo reports one combined gross event (e.g. BABA
    # 2024-06-13: vendor 0.98 regular + 0.66 special vs Yahoo 1.66 combined) —
    # per-row matching would double-count the combined gross.  When the vendor
    # date-total is net-convention, the Yahoo gross total is prorated across the
    # date's constituent rows (documented approximation, <=1% per row).
    grouped: dict[tuple[str, str], list[dict]] = {}
    for d in sorted(divs, key=lambda r: (r["symbol"], r["ex_date"])):
        grouped.setdefault((d["symbol"], d["ex_date"]), []).append(d)

    ledger = []
    for (sym, ex), rows_g in grouped.items():
        adj_rows = []
        for d in rows_g:
            f = 1.0
            for exd, fac in factors.get(sym, []):
                if exd > d["ex_date"]:
                    f *= fac
            adj_rows.append((d, float(d["rate"]) / f, f))
        vendor_total = sum(a for _, a, _ in adj_rows)
        gross_total, gsrc = vendor_total, "alpaca_ca"
        corr = "corroborated"
        if sym in spinoff_scaled:
            corr = "vendor_declared (Yahoo history spinoff-scaled, unusable as gross reference)"
        elif ex < TR_START:
            corr = ("pre_cross_source_window (before TR acquisition start "
                    f"{TR_START}; outside the 2021-06-01 simulation window; "
                    "vendor value retained)")
        else:
            match = None
            yd = yahoo_div.get(sym, {})
            for k in (0, -1, 1, -2, 2):
                dd = (date.fromisoformat(ex) + timedelta(days=k)).isoformat()
                if dd in yd:
                    match = yd[dd]
                    break
            if match is None:
                corr = "UNCORROBORATED vendor-only row"
            elif abs(match - vendor_total) <= max(0.0006, 0.006 * vendor_total):
                corr = "corroborated"
            elif vendor_total < match:
                gross_total, gsrc = match, "yahoo_events_gross"
                corr = ("vendor date-total is net-convention; gross date-total "
                        "taken from Yahoo declared"
                        + (", prorated across same-ex-date rows" if len(adj_rows) > 1 else ""))
            else:
                corr = "ANOMALY vendor > yahoo (kept vendor, flagged)"
        scale = gross_total / vendor_total if vendor_total > 0 else 1.0
        for d, vendor_adj, f in adj_rows:
            gross = vendor_adj * scale
            vendor_net = vendor_adj if gsrc == "yahoo_events_gross" else None
            ledger.append({
                "symbol": sym, "ex_date": d["ex_date"],
                "gross_declared": gross,
                "gross_source": gsrc,
                "vendor_alpaca_amount": vendor_adj,
                "vendor_net": vendor_net,
                "rate_raw_unadjusted": float(d["rate"]),
                "split_adjustment_factor": f,
                "payable_date": d.get("payable_date"),
                "record_date": d.get("record_date"),
                "special": bool(d.get("special")),
                "foreign": bool(d.get("foreign")),
                "corroboration": corr,
                "alpaca_id": d.get("id")})
    ledger.sort(key=lambda r: (r["symbol"], r["ex_date"]))
    _write_json(DIV_DIR / "dividend_ledger.json", {
        "meta": {"schema": "v2_gross_declared",
                 "source": "alpaca_corporate_actions_v1 + yahoo_events_gross "
                           "(gross determination rule in data_acquisition.py)",
                 "start": DIV_START, "end": DEV_BOUNDARY_T2,
                 "acquired_at": _now_utc(),
                 "convention": "PRIMARY = gross declared pre-tax cash per share, "
                               "split-adjusted; withholding/fees/net treatment "
                               "recorded separately in withholding_register.yaml "
                               "(principal direction D-2)",
                 "credit_convention": "ex_date",
                 "isolation": "dev_bounded_max_ex_date_2025-06-30"},
        "dividends": ledger})
    _write_json(DIV_DIR / "splits.json", {
        "meta": {"source": "alpaca_corporate_actions_v1",
                 "types": "forward_split,reverse_split",
                 "start": DIV_START, "end": RUN_DATE, "acquired_at": _now_utc(),
                 "note": "coverage runs to the run date because current "
                         "split-adjusted prices embed all splits to date"},
        "splits": sorted(splits, key=lambda r: (r["symbol"], r["ex_date"]))})
    n_gross_from_yahoo = sum(1 for r in ledger if r["gross_source"] == "yahoo_events_gross")
    print(f"  dividends v2: {len(ledger)} events; gross-from-yahoo {n_gross_from_yahoo}; "
          f"splits {len(splits)}; spinoff-scaled tickers {sorted(spinoff_scaled)}")


def acquire_corporate_actions() -> None:
    """PIT non-cash corporate-action (spin-off) ledger for the roster
    (principal decision D-1).  Vendor spin_off records where the feed covers
    them; hand-authored primary-source records for 2021 events predating feed
    coverage; each event carries the distributed security's consolidated (SIP)
    close on the parent's ex-distribution session as valuation evidence."""
    H = _alpaca_headers()
    syms = roster_63()
    url = ("https://data.alpaca.markets/v1/corporate-actions"
           f"?symbols={','.join(syms)}&types=spin_off"
           f"&start={DIV_START}&end={DEV_BOUNDARY_T2}&limit=1000")
    d = _get_json(url, H)
    vendor = (d.get("corporate_actions") or {}).get("spin_offs", [])

    events = []
    for v in vendor:
        parent = v["source_symbol"]
        if parent not in syms:
            continue
        ann = SPINOFF_ANNOUNCEMENTS.get((parent, v["new_symbol"]), (None, None))
        events.append({
            "parent": parent, "child": v["new_symbol"],
            "ratio_child_per_parent": float(v["new_rate"]) / float(v["source_rate"]),
            "announcement_date": ann[0], "announcement_source": ann[1],
            "record_date": v.get("record_date"),
            "ex_date": v["ex_date"],
            "cash_in_lieu": "fractional shares paid in cash (standard distribution-agent treatment)",
            "source": "alpaca_corporate_actions_v1 spin_off record",
            "source_classification": "commercial_vendor_corporate_actions",
            "alpaca_id": v.get("id")})
    for h in HAND_AUTHORED_SPINOFFS:
        if h["parent"] not in syms:
            continue
        events.append({
            "parent": h["parent"], "child": h["child"],
            "ratio_child_per_parent": h["ratio"],
            "announcement_date": h["announcement_date"],
            "announcement_source": h["source"],
            "record_date": h["record_date"],
            "ex_date": h["parent_ex_session"],
            "distribution_date": h["distribution_date"],
            "cash_in_lieu": h["cash_in_lieu"],
            "source": h["source"],
            "source_classification": h["source_classification"],
            "note": h["note"]})

    # valuation evidence: child consolidated close on the parent's ex session
    for ev in events:
        start = ev["ex_date"]
        end = (date.fromisoformat(start) + timedelta(days=5)).isoformat()
        bars = _fetch_stock_bars(ev["child"], start, end, "sip")
        if bars and _bar_date(bars[0]["t"]) == start:
            ev["child_close_on_parent_ex_session"] = bars[0]["c"]
            ev["child_close_source"] = "alpaca_sip_daily_split_adjusted"
        else:
            ev["child_close_on_parent_ex_session"] = None
            ev["child_close_source"] = f"UNAVAILABLE (first bar {_bar_date(bars[0]['t']) if bars else 'none'})"
        time.sleep(0.2)

    events.sort(key=lambda e: (e["parent"], e["ex_date"]))
    _write_json(CA_DIR / "spinoffs.json", {
        "meta": {"acquired_at": _now_utc(),
                 "coverage": f"{DIV_START} -> {DEV_BOUNDARY_T2} (roster parents)",
                 "valuation_rule": "in-kind distribution valued at "
                                   "ratio x child consolidated close on the "
                                   "parent's ex-distribution session, credited "
                                   "as reinvestable cash that session "
                                   "(assumption A-17)",
                 "isolation": "dev_bounded",
                 "context_note": "GEV investigated (decision D-1 list): GEV is "
                                 "itself the distributed child of GE's "
                                 "2024-04-02 spin-off (GE not in roster); no "
                                 "parent-side event exists for GEV holders "
                                 "in-window — its T-D3 divergence was a price-"
                                 "feed issue resolved under D-3, not a "
                                 "corporate action"},
        "events": events})
    for e in events:
        print(f"  spinoff {e['parent']}->{e['child']} ex {e['ex_date']} "
              f"ratio {e['ratio_child_per_parent']:.6f} "
              f"child_close {e['child_close_on_parent_ex_session']}")


def acquire_crypto() -> None:
    """BTC/ETH/SOL daily bars, CRYPTO_START -> DEV_BOUNDARY_T2 only."""
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
        print(f"  crypto {sym}: {len(bars)} bars")
        time.sleep(0.2)


def _yahoo_chart(sym: str, start: str, end: str) -> dict:
    p1 = int(datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    p2 = int((datetime.strptime(end, "%Y-%m-%d").replace(tzinfo=timezone.utc)
              + timedelta(days=1)).timestamp())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}"
           f"?period1={p1}&period2={p2}&interval=1d&events=div%7Csplit")
    return _yahoo_json(url)


def _yahoo_series(sym: str, start: str, end: str) -> dict:
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
    """Quarantined Yahoo datasets (TR validation, Track 3 books, ^IRX)."""
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
        print(f"  tr {sym}: {len(s['adjclose'])} rows")
        time.sleep(0.35)
    for sym, start in (("SPY", T3_SPY_START), ("QQQ", T3_QQQ_START)):
        s = _yahoo_series(sym, start, DEV_BOUNDARY_T3)
        adj_close = [{"date": r["date"], "close": r["close"]} for r in s["close"]]
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
        print(f"  track3 {sym}: {len(adj_close)} sessions")
        time.sleep(0.35)
    s = _yahoo_series("^IRX", IRX_START, DEV_BOUNDARY_T2)
    _write_json(RATES_DIR / "irx_13w_tbill.json", {
        "meta": {"symbol": "^IRX", "source": "yahoo_v8_chart",
                 "unit": "percent_discount_yield",
                 "role": "risk-free fallback series (primary sources "
                         "network-blocked; protocol §10 disclosed-fallback-band)",
                 "start": IRX_START, "end": DEV_BOUNDARY_T2,
                 "acquired_at": _now_utc(), "isolation": "dev_bounded"},
        "close": s["close"]})
    print(f"  rates ^IRX: {len(s['close'])} rows")


# --------------------------------------------------------------------------
# DFF ingestion (principal-supplied CSV; decision D-4)
# --------------------------------------------------------------------------

DFF_EXPECTED_SCHEMA = """\
Expected file: FRED fredgraph CSV for series DFF (Federal Funds Effective Rate).
  Locator: https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF&cosd=1999-01-01
  Format:  header line 'DATE,DFF' (legacy) or 'observation_date,DFF';
           rows 'YYYY-MM-DD,<decimal percent>'; missing values '.'
  Coverage required: 1999-01-01 through at least 2025-06-30 (daily incl. weekends).
  Validation command:
    python3 research/margin_target_study/data_acquisition.py dff <path-to-csv>
  On pass it writes data/rates/dff.json (dev-bounded at 2025-06-30; FRED data is
  US-government public domain, committable) and prints the reconstruction
  comparison against the recorded Robinhood observations.
"""


def ingest_dff(csv_path: str) -> bool:
    p = Path(csv_path)
    if not p.exists():
        print(f"DFF: file not found: {csv_path}\n\n{DFF_EXPECTED_SCHEMA}")
        return False
    rows = []
    lines = p.read_text().strip().splitlines()
    header = lines[0].strip().lower()
    if header not in ("date,dff", "observation_date,dff"):
        print(f"DFF: unexpected header {lines[0]!r}\n\n{DFF_EXPECTED_SCHEMA}")
        return False
    for ln in lines[1:]:
        d0, v = ln.split(",", 1)
        v = v.strip()
        if v in (".", ""):
            continue
        rows.append({"date": d0.strip(), "rate_pct": float(v)})
    rows.sort(key=lambda r: r["date"])
    dates = [r["date"] for r in rows]
    ok = True
    if len(dates) != len(set(dates)):
        print("DFF: duplicate dates"); ok = False
    if dates[0] > DFF_START:
        print(f"DFF: coverage starts {dates[0]} (> required {DFF_START})"); ok = False
    if dates[-1] < DEV_BOUNDARY_T2:
        print(f"DFF: coverage ends {dates[-1]} (< required {DEV_BOUNDARY_T2})"); ok = False
    bad = [r for r in rows if not (0.0 <= r["rate_pct"] <= 25.0)]
    if bad:
        print(f"DFF: {len(bad)} out-of-range values"); ok = False
    gaps = []
    prev = date.fromisoformat(dates[0])
    for ds in dates[1:]:
        cur = date.fromisoformat(ds)
        if (cur - prev).days > 4:
            gaps.append((prev.isoformat(), cur.isoformat()))
        prev = cur
    if gaps:
        print(f"DFF: {len(gaps)} gaps > 4 days: {gaps[:5]}"); ok = False
    if not ok:
        return False
    dev = [r for r in rows if DFF_START <= r["date"] <= DEV_BOUNDARY_T2]
    _write_json(RATES_DIR_COMMITTED / "dff.json", {
        "meta": {"series": "DFF", "source": "FRED fredgraph CSV, principal-supplied",
                 "source_file_sha256": sha256_file(p),
                 "coverage_supplied": f"{dates[0]} -> {dates[-1]}",
                 "coverage_stored": f"{dev[0]['date']} -> {dev[-1]['date']} (dev-bounded)",
                 "acquired_at": _now_utc(),
                 "license": "US government public domain (committable)",
                 "isolation": "dev_bounded"},
        "rates": dev})
    print(f"DFF: PASS — {len(dev)} dev-window rows stored "
          f"({dev[0]['date']} -> {dev[-1]['date']}); supplied file sha256 recorded")
    # reconstruction comparison vs ALL recorded Robinhood observations
    dmap = {r["date"]: r["rate_pct"] for r in rows}

    def dff_at(d0: str) -> float | None:
        dd, k = d0, 0
        while dd not in dmap and k < 5:
            k += 1
            dd = (date.fromisoformat(d0) + timedelta(days=k)).isoformat()
        return dmap.get(dd)

    OBS = [  # (date, observed Gold lowest-tier rate %, target-range upper bound % where recorded)
        ("2020-12-21", 2.50, 0.25),   # RH-2020-12 (flat 2.5% era; target 0.00-0.25)
        ("2022-11-03", 6.50, 4.00),   # RH-2022-11 (mechanism reported: upper + 2.5)
        ("2025-12-15", 5.75, None),   # RH-2025-12 Phase 7A tier evidence (as-of Dec 2025)
        ("2026-07-22", 5.00, None),   # RH-2026-07 published schedule + account-displayed 5.00%
    ]
    print("Reconstruction comparison (pinned model: DFF + calibrated spread; "
          "target-upper mechanism = cross-check only):")
    for obs, rate, upper in OBS:
        dv = dff_at(obs)
        if dv is None:
            print(f"  {obs}: DFF value not in supplied file")
            continue
        line = f"  {obs}: observed {rate}% − DFF {dv}% = implied DFF-spread {rate - dv:.2f}pp"
        if upper is not None:
            line += (f" | target-upper {upper}% ⇒ upper-spread {rate - upper:.2f}pp; "
                     f"DFF-vs-upper base delta {upper - dv:.2f}pp")
        print(line)
    print("Materiality assessment against pre-registered bands is recorded in "
          "G1_DATA_VALIDATION_REPORT.md §7; a material divergence that could "
          "alter a candidate classification requires a MARGIN-0005 charter "
          "amendment before simulations.")
    return True


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
    out: list[str] = []
    ok = True

    def say(s: str) -> None:
        out.append(s)
        print(s)

    syms = roster_63()
    say(f"roster_63: {len(syms)} tickers")

    spy_all = [_bar_date(b["t"]) for b in _load_prices("SPY")["bars"]]
    spy_sessions_dev = [d for d in spy_all if d <= DEV_BOUNDARY_T2]
    say("\n== research price cache (dev-truncated) ==")
    disc_flags = []
    for sym in syms:
        doc = _load_prices(sym)
        assert doc["meta"]["symbol"] == sym, f"identity mismatch {sym}"
        bars = doc["bars"]
        dates = [_bar_date(b["t"]) for b in bars]
        dup = len(dates) - len(set(dates))
        nonpos = sum(1 for b in bars if min(b["o"], b["h"], b["l"], b["c"]) <= 0)
        beyond = sum(1 for d0 in dates if d0 > DEV_BOUNDARY_T2)
        first = dates[0]
        expect = [d for d in spy_sessions_dev if d >= first]
        have = set(dates)
        missing_all = [d for d in expect if d not in have]
        # the simulation window opens 2021-06-01 (pre_registration track2.train);
        # earlier sessions exist only for signal warm-up — gaps there are a
        # recorded limitation (e.g. RKLB's thin pre-merger SPAC prints), not a
        # data-gate failure.
        missing = [d for d in missing_all if d >= "2021-06-01"]
        warmup_gaps = len(missing_all) - len(missing)
        devbars = bars
        jumps = []
        for i in range(1, len(devbars)):
            r = devbars[i]["c"] / devbars[i - 1]["c"] - 1.0
            if abs(r) > DISCONTINUITY_ABS_RET:
                jumps.append((_bar_date(devbars[i]["t"]), round(r, 4)))
        if jumps:
            disc_flags.append((sym, jumps))
        stale = dates[-1] != spy_sessions_dev[-1]
        bad = dup or nonpos or beyond or (len(missing) > 3) or stale
        if bad:
            ok = False
        say(f"  {sym}: {len(bars)} bars {dates[0]}->{dates[-1]} dup={dup} "
            f"nonpos={nonpos} beyond_boundary={beyond} missing_sim={len(missing)}"
            + (f" warmup_gaps={warmup_gaps}" if warmup_gaps else "")
            + (f" MISSING={missing[:5]}" if missing else "")
            + (f" feed={doc['meta']['feed']}" if doc['meta'].get('feed_exception') else "")
            + (" FAIL" if bad else ""))
    say(f"  discontinuity flags (|ret|>{DISCONTINUITY_ABS_RET}): {disc_flags or 'none'}")

    say("\n== sealed untouched archive (byte-level only — never opened) ==")
    if SEALED_ARCHIVE.exists() and SEALED_INDEX.exists():
        idx = json.loads(SEALED_INDEX.read_text())
        h = sha256_file(SEALED_ARCHIVE)
        match = h == idx["meta"]["archive_sha256"]
        tot = sum(m["rows"] for m in idx["members"].values())
        anom = {s: m for s, m in idx["members"].items()
                if m["duplicates"] or m["nonpositive"]}
        say(f"  archive sha256 {h[:16]}… matches index: {match}; members "
            f"{len(idx['members'])}; sealed rows {tot}; seal-time structural "
            f"anomalies: {anom or 'none'}")
        if not match or anom:
            ok = False
    else:
        say("  MISSING sealed archive/index")
        ok = False

    say("\n== cross-check vs data/backtest (overlap, dev window) ==")
    mism_total = 0
    for sym in syms:
        f = BACKTEST_CACHE / f"{sym}.json"
        if not f.exists():
            continue
        prod = {_bar_date(b["t"]): b["c"] for b in json.loads(f.read_text())
                if _bar_date(b["t"]) <= DEV_BOUNDARY_T2}
        res = {_bar_date(b["t"]): b["c"] for b in _load_prices(sym)["bars"]}
        common = sorted(set(prod) & set(res))
        mism = [d for d in common if abs(prod[d] - res[d]) > 0.005]
        if mism:
            mism_total += len(mism)
            note = " (expected: GEV uses the documented SIP source exception)" \
                if sym in GEV_FEED_EXCEPTION else ""
            say(f"  {sym}: {len(mism)}/{len(common)} closes differ{note}")
            if sym not in GEV_FEED_EXCEPTION:
                ok = False
    say(f"  total differing closes: {mism_total} "
        f"(GEV differences are the documented D-3 source exception)")

    say("\n== dividend ledger v2 (gross declared) ==")
    led = json.loads((DIV_DIR / "dividend_ledger.json").read_text())
    rows = led["dividends"]
    say(f"  events: {len(rows)}; schema: {led['meta']['schema']}")
    keys = [(r["symbol"], r["ex_date"], r["special"]) for r in rows]
    dupk = len(keys) - len(set(keys))
    fut = [r for r in rows if r["ex_date"] > DEV_BOUNDARY_T2]
    neg = [r for r in rows if r["gross_declared"] <= 0]
    chron = [r for r in rows if r.get("payable_date") and r["payable_date"] < r["ex_date"]]
    netbad = [r for r in rows if r["vendor_net"] is not None
              and not (0 < r["vendor_net"] <= r["gross_declared"])]
    paydate = sum(1 for r in rows if r.get("payable_date"))
    if dupk or fut or neg or chron or netbad:
        ok = False
    say(f"  duplicate keys {dupk}; future leakage {len(fut)}; nonpositive gross "
        f"{len(neg)}; payable<ex {len(chron)}; net>gross {len(netbad)}; "
        f"payable availability {paydate}/{len(rows)}")
    from collections import Counter
    corr = Counter(r["corroboration"].split()[0] for r in rows)
    say(f"  corroboration: {dict(corr)}")
    gy = [r for r in rows if r["gross_source"] == "yahoo_events_gross"]
    say(f"  gross-from-yahoo events: {len(gy)} across "
        f"{sorted(set(r['symbol'] for r in gy))}")
    unc = [r for r in rows if r["corroboration"].startswith("UNCORROBORATED")]
    say(f"  uncorroborated vendor-only rows (flagged): "
        f"{[(r['symbol'], r['ex_date'], r['gross_declared']) for r in unc]}")
    anom = [r for r in rows if r["corroboration"].startswith("ANOMALY")]
    say(f"  vendor>yahoo anomalies: {[(r['symbol'], r['ex_date']) for r in anom] or 'none'}")
    if anom:
        ok = False

    say("\n== corporate-action (spin-off) ledger ==")
    ca = json.loads((CA_DIR / "spinoffs.json").read_text())
    evs = ca["events"]
    kk = [(e["parent"], e["ex_date"]) for e in evs]
    dup2 = len(kk) - len(set(kk))
    problems = []
    for e in evs:
        if not (e["ratio_child_per_parent"] > 0):
            problems.append((e["parent"], "ratio<=0"))
        if e.get("record_date") and e["record_date"] > e["ex_date"]:
            problems.append((e["parent"], "record>ex"))
        if e.get("announcement_date") and e["announcement_date"] >= e["ex_date"]:
            problems.append((e["parent"], "announcement>=ex"))
        if not e.get("child_close_on_parent_ex_session"):
            problems.append((e["parent"], "missing child close"))
        elif e["child_close_on_parent_ex_session"] <= 0:
            problems.append((e["parent"], "nonpositive child close"))
        if e["ex_date"] > DEV_BOUNDARY_T2:
            problems.append((e["parent"], "beyond dev boundary"))
    if dup2 or problems:
        ok = False
    say(f"  events: {len(evs)} "
        f"({[(e['parent'], e['child'], e['ex_date']) for e in evs]})")
    say(f"  duplicates {dup2}; problems: {problems or 'none'}")

    say("\n== crypto bars ==")
    for symfile in ("BTCUSD", "ETHUSD", "SOLUSD"):
        doc = json.loads((CRYPTO_DIR / f"{symfile}.json").read_text())
        bars = doc["bars"]
        dates = [_bar_date(b["t"]) for b in bars]
        dup = len(dates) - len(set(dates))
        nonpos = sum(1 for b in bars if min(b["o"], b["h"], b["l"], b["c"]) <= 0)
        d0, d1 = date.fromisoformat(dates[0]), date.fromisoformat(dates[-1])
        expected = (d1 - d0).days + 1
        missing = expected - len(set(dates))
        fut = [d for d in dates if d > DEV_BOUNDARY_T2]
        say(f"  {symfile}: {len(bars)} bars {dates[0]}->{dates[-1]} dup={dup} "
            f"nonpos={nonpos} missing_days={missing} future_leak={len(fut)}")
        if dup or nonpos or fut:
            ok = False
    say("  governed outcome: (b) CRYPTO TARGET SIZING OUT OF SCOPE — principal "
        "acceptance recorded 2026-07-24 (SOL 416-day coverage hole); the two "
        "Study B crypto configurations (B-4L) lapse; capacity not reallocatable; "
        "BTC/ETH data remain documented but support no crypto-sizing conclusion; "
        "no cash-like proxy.")

    say("\n== Track 3 books ==")
    for sym in ("SPY", "QQQ"):
        f = TRACK3_DIR / f"{sym}.json"
        if not f.exists():
            say(f"  {sym}: quarantined file absent (re-acquire via `yahoo`)")
            ok = False
            continue
        doc = json.loads(f.read_text())
        rows3 = doc["close_split_adjusted"]
        over = [r for r in rows3 if r["date"] > DEV_BOUNDARY_T3]
        say(f"  {sym}: {len(rows3)} sessions -> {rows3[-1]['date']} "
            f"beyond_boundary={len(over)}")
        if over:
            ok = False

    say("\n== rates ==")
    f = RATES_DIR / "irx_13w_tbill.json"
    if f.exists():
        doc = json.loads(f.read_text())
        vals = [r["close"] for r in doc["close"]]
        weird = sum(1 for v in vals if not (-1.0 <= v <= 20.0))
        say(f"  ^IRX: {len(vals)} rows -> {doc['close'][-1]['date']} out_of_range={weird}")
        if weird:
            ok = False
    else:
        say("  ^IRX: quarantined file absent (re-acquire via `yahoo`)")
        ok = False
    fdff = RATES_DIR_COMMITTED / "dff.json"
    if fdff.exists():
        doc = json.loads(fdff.read_text())
        say(f"  DFF: {len(doc['rates'])} rows, stored coverage "
            f"{doc['meta']['coverage_stored']}")
    else:
        say("  DFF: NOT YET SUPPLIED — awaiting principal-provided FRED CSV "
            "(see `dff` subcommand / DFF_EXPECTED_SCHEMA). BLOCKER until "
            "ingested and validated.")
        ok = False

    say("\n== account-specific Gold evidence ==")
    evf = DATA / "evidence" / "account_evidence_20260724.yaml"
    if evf.exists():
        import yaml as _yaml
        acc = _yaml.safe_load(evf.read_text())
        res = acc.get("placeholder_resolutions", {})
        bad_fields = [k for k, v in res.items()
                      if not str(v.get("status", "")).startswith(("VERIFIED", "NOT_APPLICABLE"))]
        say(f"  fields resolved: {len(res)}; "
            + "; ".join(f"{k}={v['status']}" for k, v in res.items()))
        if bad_fields or len(res) < 6:
            say(f"  INCOMPLETE: {bad_fields or 'missing fields'}")
            ok = False
    else:
        say("  MISSING account evidence record")
        ok = False

    say("\n== untouched-test boundary status ==")
    maxdiv = max(r["ex_date"] for r in rows)
    checks = [("dividend ledger max ex_date", maxdiv, DEV_BOUNDARY_T2)]
    for symfile in ("BTCUSD", "ETHUSD", "SOLUSD"):
        doc = json.loads((CRYPTO_DIR / f"{symfile}.json").read_text())
        checks.append((f"crypto {symfile} max bar",
                       max(_bar_date(b["t"]) for b in doc["bars"]), DEV_BOUNDARY_T2))
    maxpx = max(max(_bar_date(b["t"]) for b in _load_prices(s)["bars"]) for s in syms)
    checks.append(("dev price cache max bar", maxpx, DEV_BOUNDARY_T2))
    maxca = max(e["ex_date"] for e in evs)
    checks.append(("corporate-action max ex_date", maxca, DEV_BOUNDARY_T2))
    for name, got, bound in checks:
        good = got <= bound
        if not good:
            ok = False
        say(f"  {name}: {got} <= {bound}: {'OK' if good else 'FAIL'}")
    say("  untouched price segment: SEALED archive only (byte-hash-verified, "
        "never opened by this validator or any G1 code)")

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


def _bh_with_cash_events(closes: dict[str, float], sessions: list[str],
                         cash: dict[str, float]) -> float:
    shares = 1.0
    for dsess in sessions[1:]:
        amt = cash.get(dsess)
        if amt:
            shares += shares * amt / closes[dsess]
    return shares * closes[sessions[-1]] / closes[sessions[0]]


def reconcile(report_path: Path | None = None) -> bool:
    """T-D3: primary path (split-adjusted prices + gross PIT dividend cash +
    PIT spin-off cash-equivalents) vs quarantined Yahoo TR, dev window only."""
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
            by_sym[r["symbol"]].get(r["ex_date"], 0.0) + r["gross_declared"]
    ca = json.loads((CA_DIR / "spinoffs.json").read_text())
    for e in ca["events"]:
        px = e.get("child_close_on_parent_ex_session")
        if px:
            amt = e["ratio_child_per_parent"] * px
            by_sym.setdefault(e["parent"], {})
            by_sym[e["parent"]][e["ex_date"]] = \
                by_sym[e["parent"]].get(e["ex_date"], 0.0) + amt

    say("== T-D3 reconciliation v2 (gross dividends + spin-off cash-equivalents, "
        f"dev window, tolerance ±{TD3_TOLERANCE_PP}pp/yr) ==")
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
        cash = by_sym.get(sym, {})
        sset = set(sessions)
        cmap: dict[str, float] = {}
        for d0, amt in cash.items():
            if d0 < sessions[0] or d0 > sessions[-1]:
                continue
            dd, k = d0, 0
            while dd not in sset and k < 5:
                k += 1
                dd = (date.fromisoformat(d0) + timedelta(days=k)).isoformat()
            if dd in sset:
                cmap[dd] = cmap.get(dd, 0.0) + amt
        g_primary = _bh_with_cash_events(closes, sessions, cmap)
        g_tr = adj[sessions[-1]] / adj[sessions[0]]
        c_p = _cagr(1.0, g_primary, days)
        c_t = _cagr(1.0, g_tr, days)
        diff = abs(c_p - c_t) * 100.0
        verdict = "PASS" if diff <= TD3_TOLERANCE_PP else "FAIL"
        if verdict == "FAIL":
            okall = False
            g_yraw = _bh_with_cash_events(yraw, [s for s in sessions if s in yraw], cmap) \
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
        cmap = {}
        for d0, amt in divs.items():
            if d0 < sessions[0] or d0 > sessions[-1]:
                continue
            dd, k = d0, 0
            while dd not in sset and k < 5:
                k += 1
                dd = (date.fromisoformat(d0) + timedelta(days=k)).isoformat()
            if dd in sset:
                cmap[dd] = cmap.get(dd, 0.0) + amt
        g_primary = _bh_with_cash_events(closes, sessions, cmap)
        g_tr = adj[sessions[-1]] / adj[sessions[0]]
        c_p, c_t = _cagr(1.0, g_primary, days), _cagr(1.0, g_tr, days)
        diff = abs(c_p - c_t) * 100.0
        verdict = "PASS" if diff <= TD3_TOLERANCE_PP else "FAIL"
        if verdict == "FAIL":
            okall = False
        say(f"{sym} | {sessions[0]}->{sessions[-1]} | {days/365.25:.2f}y | "
            f"{c_p*100:.3f}% | {c_t*100:.3f}% | {diff:.3f} | {verdict}")

    if fails:
        say("\nFailure attribution (yahoo-raw price leg isolates price-source "
            "noise from ledger errors):")
        for sym, d1, d2 in fails:
            say(f"  {sym}: alpaca-leg {d1:.3f}pp/yr; yahoo-raw-leg "
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
    elif cmd == "corpactions":
        acquire_corporate_actions()
    elif cmd == "crypto":
        acquire_crypto()
    elif cmd == "yahoo":
        acquire_yahoo()
    elif cmd == "dff":
        if len(sys.argv) < 3:
            print(DFF_EXPECTED_SCHEMA)
            return 1
        return 0 if ingest_dff(sys.argv[2]) else 1
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
