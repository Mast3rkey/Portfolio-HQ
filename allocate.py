#!/usr/bin/env python3
"""
allocate.py — manual-allocation ADVISOR. Recommendations only.

This tool NEVER places, modifies, or cancels an order anywhere. It reads your
holdings + canonical destination targets (targets.yaml, PHQ-2026-02), pulls
market data from Alpaca (read-only), applies your gates (targets.yaml,
gates.yaml, issuer_lookthrough.yaml), and prints/logs a
BUY / TRIM / NO ADD / BLOCKED table plus a short summary. You execute
manually on Robinhood.

Usage:
    python allocate.py --cash 2000       # deploy new cash
    python allocate.py --review          # rebalance check, no new cash
    python allocate.py update-shares         # paste "TICKER qty" lines, Ctrl-D (stocks/ETFs)
    python allocate.py update-crypto-shares  # paste "COIN qty" lines, Ctrl-D (BTC/ETH/SOL)
    python allocate.py update-holdings       # paste "TICKER value" lines, Ctrl-D (manual fallback)
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

from alpaca_client import AlpacaPaperClient
from indicators import compute_all
from regime_gate import regime_ok_from_closes
from earnings import days_until_earnings
from crypto import fetch_crypto
from margin_state import classify_margin_state, concentration_risk_score

HERE = Path(__file__).resolve().parent
TARGETS_FILE = HERE / "targets.yaml"
HOLDINGS_FILE = HERE / "holdings.yaml"
GATES_FILE = HERE / "gates.yaml"
LOOKTHROUGH_FILE = HERE / "issuer_lookthrough.yaml"
LOGS_DIR = HERE / "logs"
PERF_LOG_FILE = HERE / "performance_log.csv"
PERF_FIELDS = ["date", "net_equity", "gross", "margin_debt", "qqq_price", "voo_price", "note"]

DAILY_LIMIT = 320  # margin above the ~290-300 trading days in DAYS_BACK, so a
                    # holiday-heavy stretch can't starve the 200-SMA of bars
DAYS_BACK = 420
STALE_MARGIN_DAYS = 2   # warn if margin debt/buffer haven't been synced in this many days


def _margin_buffer_age_days(synced_at) -> float | None:
    """Days since holdings.yaml's margin.synced_at, or None if missing,
    unparseable, OR in the future. Fails safe: a malformed/absent/future date
    never raises and never yields a fabricated number (0 would read as
    'freshly synced' and hide real staleness; a negative number for a future
    date is nonsensical, not 'fresher than fresh') -- it yields 'age unknown',
    which every caller (render(), classify_margin_state() via main()) treats
    as 'do not judge staleness from this'. Single source of truth so the
    review banner and the risk-classifier's own reasons are always computed
    from the identical age, never contradict each other. Pair with
    _margin_buffer_age_unverifiable() at the call site to distinguish
    'no age info at all' from 'an age was attempted and is invalid' --
    this function alone conflates the two into the same None."""
    if not synced_at:
        return None
    try:
        age = (date.today() - date.fromisoformat(str(synced_at))).days
    except ValueError:
        return None
    return age if age >= 0 else None


def _margin_buffer_age_unverifiable(synced_at) -> bool:
    """True when synced_at is present but does not resolve to a valid,
    non-negative age (malformed string or a future date) or is absent
    entirely -- i.e. whenever _margin_buffer_age_days(synced_at) is None.
    Kept as a distinct call (rather than inferring this from the age being
    None at each call site) so main()'s wiring into classify_margin_state()
    reads as an explicit decision, matching that function's own explicit
    buffer_data_unverifiable parameter."""
    return _margin_buffer_age_days(synced_at) is None


# ── config / state io ──────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


# Independent review, PR #202, MAJOR finding 3: the exact, case-sensitive
# vocabulary the canonical v1.30 destination schema supports (targets.yaml's
# own header comment). No other value, and no case variant of these, is
# valid -- an unrecognized or miscased asset_class must fail loudly, never
# silently fall through as tradable ("equity") or non-tradable.
VALID_ASSET_CLASSES = frozenset({"equity", "fund", "crypto", "reserve", "cash"})


def build_roster(targets: dict) -> dict:
    """Return {ticker: {target_pct, asset_class}} from targets.yaml's
    `destination:` list — the canonical v1.30 architecture (PHQ-2026-02).
    Every row (including RESERVE/CASH synthetic sleeves) is included; callers
    that need only market-tradable tickers should filter on asset_class.

    Every row is validated at parse time (independent review, PR #202,
    MAJOR finding 3 + destination-row validation): a missing/blank/
    duplicate ticker, a missing/non-numeric/negative target_pct, or a
    missing/blank/unknown/miscased asset_class each raise loudly, naming
    the offending row, rather than silently defaulting or surfacing as an
    unlabeled KeyError/ValueError deeper in plan()."""
    roster: dict[str, dict] = {}
    for i, row in enumerate(targets.get("destination", []) or []):
        label = f"destination row #{i}"
        if not isinstance(row, dict):
            raise ValueError(f"targets.yaml {label} is not a mapping: {row!r}")

        raw_ticker = row.get("ticker")
        if not isinstance(raw_ticker, str) or not raw_ticker.strip():
            raise ValueError(f"targets.yaml {label} has a missing or blank 'ticker'")
        tk = raw_ticker.strip().upper()
        label = f"targets.yaml destination row #{i} ({tk})"
        if tk in roster:
            raise ValueError(f"{label} is a duplicate ticker")

        if "target_pct" not in row or row["target_pct"] is None:
            raise ValueError(f"{label} is missing 'target_pct'")
        try:
            target_pct = float(row["target_pct"])
        except (TypeError, ValueError):
            raise ValueError(f"{label} has a non-numeric 'target_pct': {row['target_pct']!r}")
        if target_pct < 0:
            raise ValueError(f"{label} has a negative 'target_pct': {target_pct}")

        asset_class = row.get("asset_class")
        if not isinstance(asset_class, str) or not asset_class.strip():
            raise ValueError(f"{label} has a missing or blank 'asset_class'")
        if asset_class != asset_class.strip():
            raise ValueError(f"{label} has a whitespace-padded 'asset_class': {asset_class!r}")
        if asset_class not in VALID_ASSET_CLASSES:
            raise ValueError(
                f"{label} has an unrecognized 'asset_class' {asset_class!r} — "
                f"must be exactly one of {sorted(VALID_ASSET_CLASSES)} "
                "(case-sensitive; no unknown value is silently accepted)")

        roster[tk] = {"target_pct": target_pct, "asset_class": asset_class}
    return roster


def load_gates() -> dict[str, dict]:
    """Actionable gates, represented separately from targets.yaml per
    PHQ-2026-02 — {ticker: {status, authority, allow_add, next_gate, ...}}.
    A gated ticker's target capital is never bought and never renormalized
    into any other name (see gates.yaml, plan()).

    gates.yaml is MANDATORY under the canonical PHQ-2026-02 architecture —
    a gated ticker (e.g. SPCX) becoming an ordinary, unflagged buy candidate
    because its gate config failed to load would be a silent policy breach,
    not a benign absence. Missing, unreadable, malformed, or structurally
    invalid configuration must never be interpreted as an empty gate set;
    this fails loudly instead, mirroring _resolve_margin_config()'s existing
    fail-loud convention (NUM-0001 P1-1) for the same reason: both are
    safety-critical parameters where a wrong default is worse than a crash.
    Independent review, PR #202, MAJOR finding 1."""
    if not GATES_FILE.exists():
        raise ValueError(
            f"gates.yaml is missing ({GATES_FILE}) — required under the "
            "canonical PHQ-2026-02 architecture; cannot safely treat this "
            "as 'no gates', which would let a gated ticker appear as an "
            "ordinary buy candidate")
    try:
        raw = GATES_FILE.read_text()
    except OSError as e:
        raise ValueError(f"gates.yaml could not be read ({GATES_FILE}): {e}")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise ValueError(f"gates.yaml is not valid YAML ({GATES_FILE}): {e}")
    if not isinstance(data, dict):
        raise ValueError(
            f"gates.yaml ({GATES_FILE}) must parse to a mapping with a "
            f"top-level 'gates' key, got {type(data).__name__}")
    gate_list = data.get("gates")
    if gate_list is None:
        raise ValueError(f"gates.yaml ({GATES_FILE}) is missing its top-level 'gates' key")
    if not isinstance(gate_list, list):
        raise ValueError(
            f"gates.yaml ({GATES_FILE}) 'gates' key must be a list, "
            f"got {type(gate_list).__name__}")
    result: dict[str, dict] = {}
    for i, g in enumerate(gate_list):
        if not isinstance(g, dict) or not g.get("ticker"):
            raise ValueError(
                f"gates.yaml ({GATES_FILE}) entry #{i} is missing a required "
                "'ticker' field")
        result[str(g["ticker"]).upper()] = g
    return result


def load_issuer_lookthrough() -> dict:
    """8%/40% no-add control configuration (PHQ-2026-02) — issuer
    ceiling/common-driver ceiling, the retained point-in-time 40.0284%
    measurement, and the hand-maintained ETF look-through constituent
    weights (never live-fetched — see issuer_lookthrough.yaml header)."""
    if not LOOKTHROUGH_FILE.exists():
        return {}
    return load_yaml(LOOKTHROUGH_FILE) or {}


# ── data acquisition ───────────────────────────────────────────────────────────

def fetch_market(client, tickers: list[str], regime_ticker: str) -> tuple[dict, bool, list]:
    """Fetch indicators for every ticker + the regime signal. Returns
    (metrics_by_ticker, regime_ok, regime_closes_len_flag)."""
    metrics: dict[str, dict] = {}
    all_syms = sorted(set(tickers) | {regime_ticker})
    regime_bars = None
    for sym in all_syms:
        try:
            bars = client.get_bars(sym, "1Day", DAILY_LIMIT, DAYS_BACK)
        except Exception as e:
            metrics[sym] = {"error": str(e)[:80]}
            continue
        if sym == regime_ticker:
            regime_bars = bars
        if not bars:
            metrics[sym] = {"error": "no bars"}
            continue
        metrics[sym] = compute_all(bars)

    if regime_bars:
        closes = [float(b["c"]) for b in regime_bars]
        regime_ok = regime_ok_from_closes(closes)
        regime_known = len(closes) >= 2
    else:
        regime_ok, regime_known = False, False
    return metrics, regime_ok, regime_known


def resolve_holdings(client, metrics: dict | None = None,
                     crypto_prices: dict | None = None) -> dict[str, float]:
    """Live-value every share-tracked position (qty x latest price); fall back to the
    manual dollar snapshot in 'holdings' for anything with no share/coin count or no
    live price. 'shares' and 'crypto_shares' are the source of truth
    for any ticker/coin present there; 'holdings' entries are only the fallback/override
    layer. Pass 'metrics' (from fetch_market) and 'crypto_prices' ({coin: price}, e.g.
    from crypto.fetch_crypto) to reuse prices already fetched this run and avoid a
    second round of API calls; omit either to fetch fresh (e.g. from log_performance()
    running standalone)."""
    data = load_yaml(HOLDINGS_FILE)
    shares = data.get("shares", {}) or {}
    crypto_shares = data.get("crypto_shares", {}) or {}
    result = dict(data.get("holdings", {}) or {})
    for t, qty in shares.items():
        price = metrics.get(t, {}).get("price") if metrics else None
        if price is None:
            try:
                bars = client.get_bars(t, "1Day", 1, days_back=5)
                price = bars[-1]["c"] if bars else None
            except Exception:
                price = None
        if price is not None:
            result[t] = round(float(qty) * float(price), 2)
        # else: leave whatever 'holdings' already had for t (or nothing), rather
        # than silently dropping/zeroing a position on a transient price-fetch miss.
    if crypto_shares:
        prices = crypto_prices
        if prices is None:
            try:
                raw = client.get_crypto_latest([f"{c}/USD" for c in crypto_shares])
                prices = {c: raw.get(f"{c}/USD") for c in crypto_shares}
            except Exception:
                prices = {}
        for c, qty in crypto_shares.items():
            px = (prices or {}).get(c)
            if px is not None:
                result[c] = round(float(qty) * float(px), 2)
            # else: same fallback-to-manual-value behavior as stocks above.
    return {t: v for t, v in result.items() if v}


# ── core allocation logic ──────────────────────────────────────────────────────

def _resolve_margin_config(targets: dict) -> tuple[float, float]:
    """targets.yaml is the sole canonical owner of leverage_cap/buffer_floor_pct.
    Both are safety-critical (the 1.8x cap and 30% floor) so a missing or
    malformed margin: block must fail loudly rather than silently substitute
    the historical 1.8/30.0 defaults (NUM-0001 P1-1)."""
    margin_cfg = targets.get("margin")
    if not isinstance(margin_cfg, dict):
        raise ValueError(
            "targets.yaml 'margin' block is missing or not a mapping — "
            "required keys: leverage_cap, buffer_floor_pct")
    missing = [k for k in ("leverage_cap", "buffer_floor_pct") if k not in margin_cfg]
    if missing:
        raise ValueError(
            f"targets.yaml 'margin' block missing required key(s): {', '.join(missing)}")
    try:
        leverage_cap = float(margin_cfg["leverage_cap"])
        buffer_floor_pct = float(margin_cfg["buffer_floor_pct"])
    except (TypeError, ValueError):
        raise ValueError(
            "targets.yaml 'margin' block has a non-numeric leverage_cap or "
            "buffer_floor_pct")
    return leverage_cap, buffer_floor_pct


def margin_capacity(gross, margin_debt, cash, leverage_cap, buffer_pct, buffer_floor_pct,
                    margin_requested):
    """Structural leverage-cap + buffer-floor check (July 2026 margin doctrine).
    Buffer is a capacity ceiling, not a timing throttle — hard cutoff, no taper.
    Returns (net_equity, margin_allowed, forced_delever, block_reason)."""
    net_equity = gross - margin_debt
    if buffer_pct is not None and buffer_pct < buffer_floor_pct:
        return net_equity, 0.0, True, (
            f"buffer {buffer_pct:.1f}% < {buffer_floor_pct:.0f}% floor — forced de-lever")
    max_by_leverage = max(0.0, leverage_cap * (net_equity + cash) - gross - cash)
    allowed = min(margin_requested, max_by_leverage)
    reason = "" if allowed >= margin_requested - 1e-9 else (
        f"leverage cap {leverage_cap:.2f}x (max additional margin ${max_by_leverage:,.0f})")
    return net_equity, allowed, False, reason


def _issuer_exposure(holdings: dict, book: float, lookthrough: dict) -> dict:
    """Current effective issuer/common-driver exposure computed from LIVE
    reconciled holdings + current prices (never the frozen retained
    measurement) — PHQ-2026-02 Phase 7/8. effective_pct = direct + embedded
    (via the hand-maintained, point-in-time fund_holding_weight constituent
    table in issuer_lookthrough.yaml — never a live ETF-constituent fetch)."""
    issuers = {}
    common_driver_pct = 0.0
    for iss in lookthrough.get("issuers", []) or []:
        tk = iss["ticker"].upper()
        direct_pct = (float(holdings.get(tk, 0.0)) / book * 100.0) if book > 0 else 0.0
        embedded_pct = 0.0
        for f in iss.get("funds", []) or []:
            fund_pct_of_book = (float(holdings.get(f["fund"].upper(), 0.0)) / book * 100.0) if book > 0 else 0.0
            embedded_pct += fund_pct_of_book * float(f["fund_holding_weight"])
        effective_pct = direct_pct + embedded_pct
        issuers[tk] = {"direct_pct": direct_pct, "embedded_pct": embedded_pct,
                       "effective_pct": effective_pct}
        common_driver_pct += effective_pct
    return {"issuers": issuers, "common_driver_current_pct": common_driver_pct}


def plan(targets, holdings, roster, metrics, regime_ok, regime_known, cash,
         margin_debt=0.0, margin_buffer_pct=None, margin_requested=0.0,
         gates_cfg=None, lookthrough=None):
    """PHQ-2026-02 canonical-destination allocator. `roster` is
    build_roster()'s per-ticker {target_pct, asset_class} (canonical v1.30 —
    see targets.yaml). `gates_cfg` is load_gates()'s output (actionable
    gates, represented separately — a gated ticker is never a buy candidate
    and its target capital is never renormalized into another name, it
    simply never enters buy_candidates). `lookthrough` is
    load_issuer_lookthrough()'s output (8%/40% no-add controls)."""
    gates = targets.get("gates", {})
    caps = targets.get("caps", {})
    gates_cfg = gates_cfg or {}
    lookthrough = lookthrough or {}
    min_lot = float(gates.get("min_lot_dollars", 25))
    trend_rsi_override = float(gates.get("trend_rsi_override", 30))
    blackout_days = int(gates.get("earnings_blackout_days", 7))
    issuer_ceiling = float(lookthrough.get("issuer_ceiling_pct", 8.0))
    common_driver_ceiling = float(lookthrough.get("common_driver_ceiling_pct", 40.0))
    lookthrough_issuer_tickers = {i["ticker"].upper() for i in lookthrough.get("issuers", []) or []}
    lookthrough_fund_tickers = {f["fund"].upper() for i in lookthrough.get("issuers", []) or []
                                for f in i.get("funds", []) or []}
    # Correlated-cluster concentration caps (semis, power/infra, ...) — each measured
    # against book (net equity), mechanically trimmed on breach, no RSI gate. A ticker
    # may belong to more than one cluster; every cluster it's in must have room for a buy.
    clusters = [{"name": c["name"], "pct": float(c["pct"]),
                "tickers": {t.upper() for t in c["tickers"]}}
               for c in (caps.get("clusters", []) or [])]
    leverage_cap, buffer_floor_pct = _resolve_margin_config(targets)

    gross = sum(float(v) for v in holdings.values())
    net_equity, margin_allowed, forced_delever, margin_block_reason = margin_capacity(
        gross, margin_debt, float(cash), leverage_cap, margin_buffer_pct,
        buffer_floor_pct, float(margin_requested))
    book = net_equity + float(cash)          # doctrine: book = net equity (+ new deposit)
    deployable = float(cash) + margin_allowed  # buying power for this cycle (deposit + margin)
    # per-cluster running value + per-ticker target/current, for the mechanical trim below
    cluster_value = {c["name"]: sum(float(holdings.get(t, 0)) for t in c["tickers"])
                     for c in clusters}
    cluster_info: dict[str, dict[str, dict]] = {c["name"]: {} for c in clusters}

    exposure = _issuer_exposure(holdings, book, lookthrough)
    common_driver_running_pct = exposure["common_driver_current_pct"]
    issuer_running_pct = {tk: v["effective_pct"] for tk, v in exposure["issuers"].items()}

    rows: list[dict] = []          # BLOCKED / info rows
    buy_candidates: list[dict] = []
    trims: list[dict] = []
    no_add_gated: list[dict] = []   # PHQ-2026-02: gated destination capital, held as cash

    for tk, meta in roster.items():
        asset_class = meta["asset_class"]
        m = metrics.get(tk, {}) if asset_class != "crypto" else {}
        target_dollars = book * meta["target_pct"] / 100.0
        current = float(holdings.get(tk, 0.0))
        gap = target_dollars - current
        price = m.get("price")
        rsi = m.get("rsi14")
        sma200 = m.get("sma200")
        vs200 = ((price / sma200 - 1) * 100) if (price and sma200) else None

        base = {"ticker": tk, "asset_class": asset_class, "price": price, "rsi": rsi,
                "vs200": vs200, "target": target_dollars, "current": current,
                "gap": gap}
        tk_clusters = [c["name"] for c in clusters if tk in c["tickers"]]
        gate = gates_cfg.get(tk)
        # Independent review, PR #202, MAJOR finding 2: a gated or synthetic
        # non-tradable (reserve/cash) row must never become a mechanical
        # cluster-trim candidate, even if a future config mistakenly lists
        # one as a cluster member — a gate blocks adds, it must never create
        # or permit an automatic sale. Guarded here, at the single source
        # cluster_info feeds, rather than by filtering candidates later.
        trim_eligible = asset_class not in ("reserve", "cash") and gate is None
        if trim_eligible:
            for cname in tk_clusters:
                cluster_info[cname][tk] = {"current": current, "target": target_dollars,
                                           "price": price, "rsi": rsi, "asset_class": asset_class}

        # ---- RESERVE/CASH: never a buy candidate, definitionally satisfied ----
        if asset_class in ("reserve", "cash"):
            continue

        # ---- GATED (PHQ-2026-02): target capital held as cash, no renormalize --
        if gate is not None:
            no_add_gated.append({**base, "action": "NO ADD — GATED",
                                 "status": gate.get("status"),
                                 "authority": gate.get("authority"),
                                 "next_gate": gate.get("next_gate"),
                                 "holds_existing_shares": bool(current > 0)})
            continue

        # ---- only underweight names are buy candidates -------------------
        if gap < min_lot:
            continue
        if asset_class != "crypto" and (m.get("error") or price is None):
            rows.append({**base, "action": "BLOCKED", "dollars": 0,
                         "reason": f"no-data ({m.get('error','insufficient bars')})"})
            continue

        # No trend/RSI/earnings timing gate for crypto (Decisions Log, July
        # 2026: conviction-sizing, not a timing call — unchanged by this
        # migration).
        if asset_class != "crypto":
            # ---- TREND gate -------------------------------------------------
            if sma200 is not None and price < sma200:
                if rsi is None or rsi >= trend_rsi_override:
                    rows.append({**base, "action": "BLOCKED", "dollars": 0,
                                 "reason": f"downtrend (px {vs200:+.1f}% vs 200SMA, RSI "
                                           f"{'n/a' if rsi is None else f'{rsi:.0f}'})"})
                    continue

            # ---- EARNINGS gate ------------------------------------------------
            de = days_until_earnings(tk)
            if de is None:
                base["earn_flag"] = "earnings:unavailable"
            elif 0 <= de <= blackout_days:
                rows.append({**base, "action": "BLOCKED", "dollars": 0,
                             "reason": f"earnings in {de}d"})
                continue

        max_by_name = max(0.0, target_dollars - current)  # canonical destination is the ceiling

        buy_candidates.append({**base, "clusters": tk_clusters,
                               "max_by_name": max_by_name,
                               "want": min(gap, max_by_name),
                               "earn_flag": base.get("earn_flag", "")})

    # ---- CLUSTER CAPS: mechanical trim, no RSI gate --------------------------
    # Correlation/concentration risk limit, not a return-timing call. Names
    # already trimmed (or by an earlier cluster in this loop) are skipped;
    # trims largest-overweight-first, floored at each name's own target.
    already_trimmed = {t["ticker"] for t in trims}
    for c in clusters:
        cname, cap_pct = c["name"], c["pct"]
        info = cluster_info[cname]
        cap_dollars = book * cap_pct / 100.0
        excess = cluster_value[cname] - cap_dollars
        if excess < min_lot:
            continue
        candidates = sorted(
            ({"ticker": tk, **i, "overweight": i["current"] - i["target"]}
             for tk, i in info.items()
             if tk not in already_trimmed and i["current"] - i["target"] >= min_lot),
            key=lambda x: x["overweight"], reverse=True)
        for cand in candidates:
            if excess < min_lot:
                break
            amt = min(cand["overweight"], excess)
            if amt < min_lot:
                continue
            trims.append({
                "ticker": cand["ticker"], "asset_class": cand["asset_class"],
                "price": cand["price"], "rsi": cand["rsi"], "vs200": None,
                "target": cand["target"], "current": cand["current"],
                "gap": cand["target"] - cand["current"],
                "action": "TRIM", "dollars": amt,
                "reason": f"{cname} cluster cap {cap_pct:.0f}% "
                          f"(${cand['overweight']:,.0f} over own target)"})
            cluster_value[cname] -= amt
            excess -= amt
            already_trimmed.add(cand["ticker"])
            for c2 in clusters:
                if cand["ticker"] in cluster_info[c2["name"]]:
                    cluster_info[c2["name"]][cand["ticker"]]["current"] = cand["current"] - amt

    # ---- greedy allocation to largest passing gaps -----------------------
    # PHQ-2026-02 Phase 7/8: 8% effective-issuer and 40% common-driver
    # ceilings are NO-ADD controls (never a trim/sell), applied here as a
    # clip-or-block on the buy amount, same mechanism as a cluster cap.
    cluster_pct = {c["name"]: c["pct"] for c in clusters}
    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    cash_left = deployable
    buys: list[dict] = []
    no_add_issuer: list[dict] = []
    no_add_common_driver: list[dict] = []
    for c in buy_candidates:
        tk = c["ticker"]
        want = min(c["gap"], c["max_by_name"])
        blocked_by = None
        for cname in c["clusters"]:
            room = book * cluster_pct[cname] / 100.0 - cluster_value[cname]
            if room < min_lot:
                blocked_by = cname
                break
            want = min(want, room)
        if blocked_by:
            rows.append({**c, "action": "BLOCKED", "dollars": 0,
                         "reason": f"{blocked_by} cluster cap {cluster_pct[blocked_by]:.0f}%"})
            continue

        # ---- 8% effective-issuer no-add ceiling --------------------------
        issuer_blocked = False
        if tk in lookthrough_issuer_tickers and book > 0:
            cur_pct = issuer_running_pct.get(tk, 0.0)
            if cur_pct >= issuer_ceiling:
                no_add_issuer.append({**c, "action": "NO ADD — ISSUER CEILING",
                                      "current_effective_pct": cur_pct,
                                      "ceiling_pct": issuer_ceiling})
                issuer_blocked = True
            else:
                room_pct = issuer_ceiling - cur_pct
                room_dollars = room_pct / 100.0 * book
                want = min(want, room_dollars)
        if issuer_blocked:
            continue
        # A fund purchase (SPY/VEA/VWO) embeds proportionally into every
        # issuer it backs — clip to the tightest room among all of them too.
        if tk in lookthrough_fund_tickers and book > 0:
            for iss in lookthrough.get("issuers", []) or []:
                for f in iss.get("funds", []) or []:
                    if f["fund"].upper() != tk:
                        continue
                    iss_tk = iss["ticker"].upper()
                    cur_pct = issuer_running_pct.get(iss_tk, 0.0)
                    fhw = float(f["fund_holding_weight"])
                    if fhw <= 0:
                        continue
                    if cur_pct >= issuer_ceiling:
                        want = 0.0
                        continue
                    room_pct = issuer_ceiling - cur_pct
                    room_dollars = (room_pct / fhw) / 100.0 * book
                    want = min(want, room_dollars)

        # ---- 40% AI/platform common-driver no-add ceiling ----------------
        is_common_driver_member = tk in lookthrough_issuer_tickers or tk in lookthrough_fund_tickers
        if is_common_driver_member and book > 0:
            if common_driver_running_pct >= common_driver_ceiling:
                no_add_common_driver.append({**c, "action": "NO ADD — COMMON-DRIVER CEILING",
                                             "current_common_driver_pct": common_driver_running_pct,
                                             "ceiling_pct": common_driver_ceiling})
                continue
            else:
                room_pct = common_driver_ceiling - common_driver_running_pct
                # marginal common-driver contribution per dollar of this buy:
                # direct issuer = 1:1; fund = sum of its backed issuers' fund_holding_weight
                if tk in lookthrough_issuer_tickers:
                    marginal_frac = 1.0
                else:
                    marginal_frac = sum(
                        float(f["fund_holding_weight"])
                        for iss in lookthrough.get("issuers", []) or []
                        for f in iss.get("funds", []) or []
                        if f["fund"].upper() == tk)
                if marginal_frac > 0:
                    room_dollars = (room_pct / marginal_frac) / 100.0 * book
                    want = min(want, room_dollars)

        alloc = min(want, cash_left)
        if alloc < min_lot:
            if cash_left < min_lot and deployable > 0:
                rows.append({**c, "action": "BLOCKED", "dollars": 0,
                             "reason": "cash exhausted"})
            continue
        buys.append({**c, "action": "BUY", "dollars": alloc,
                     "reason": c.get("earn_flag", "")})
        cash_left -= alloc
        for cname in c["clusters"]:
            cluster_value[cname] += alloc
        alloc_pct_of_book = (alloc / book * 100.0) if book > 0 else 0.0
        if tk in lookthrough_issuer_tickers:
            issuer_running_pct[tk] = issuer_running_pct.get(tk, 0.0) + alloc_pct_of_book
            common_driver_running_pct += alloc_pct_of_book
        elif tk in lookthrough_fund_tickers:
            for iss in lookthrough.get("issuers", []) or []:
                for f in iss.get("funds", []) or []:
                    if f["fund"].upper() != tk:
                        continue
                    iss_tk = iss["ticker"].upper()
                    delta = alloc_pct_of_book * float(f["fund_holding_weight"])
                    issuer_running_pct[iss_tk] = issuer_running_pct.get(iss_tk, 0.0) + delta
                    common_driver_running_pct += delta

    deployed_total = sum(b["dollars"] for b in buys)
    margin_used = min(margin_allowed, max(0.0, deployed_total - float(cash)))

    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    unresolved = {t: float(v) for t, v in holdings.items() if t.upper() not in roster}
    leverage_current = (gross / net_equity) if net_equity > 0 else None
    return {
        "book": book, "cash": float(cash), "cash_left": cash_left,
        "buys": buys, "trims": trims, "blocked": rows,
        "underweight": buy_candidates,
        "no_add_gated": no_add_gated,
        "no_add_issuer": no_add_issuer,
        "no_add_common_driver": no_add_common_driver,
        "unresolved": unresolved,
        "orphans": unresolved,   # retained alias — see render()
        "issuer_exposure": exposure["issuers"],
        "common_driver_current_pct": exposure["common_driver_current_pct"],
        "common_driver_ceiling_pct": common_driver_ceiling,
        "issuer_ceiling_pct": issuer_ceiling,
        "retained_common_driver_measurement": lookthrough.get("retained_common_driver_measurement"),
        "regime_ok": regime_ok, "regime_known": regime_known,
        "clusters": [
            {
                "name": c["name"], "value": cluster_value[c["name"]], "pct": c["pct"],
                "current_pct": (cluster_value[c["name"]] / book * 100.0) if book > 0 else None,
                "ratio_to_cap": (cluster_value[c["name"]] / (book * c["pct"] / 100.0))
                                if (c["pct"] > 0 and book > 0) else None,
            }
            for c in clusters
        ],
        "margin": {
            "gross": gross, "net_equity": net_equity, "debt": margin_debt,
            "buffer_pct": margin_buffer_pct, "buffer_floor_pct": buffer_floor_pct,
            "leverage_current": leverage_current, "leverage_cap": leverage_cap,
            "requested": float(margin_requested), "allowed": margin_allowed,
            "used": margin_used, "forced_delever": forced_delever,
            "block_reason": margin_block_reason,
        },
    }


# ── rendering ──────────────────────────────────────────────────────────────────

def _fmt_row(r):
    px = f"${r['price']:.2f}" if r.get("price") else "n/a"
    rsi = f"{r['rsi']:.0f}" if r.get("rsi") is not None else "n/a"
    vs = f"{r['vs200']:+.1f}%" if r.get("vs200") is not None else "n/a"
    dollars = f"${r['dollars']:,.0f}" if r.get("dollars") else "—"
    action = r["action"] + (f": {r['reason']}" if r.get("reason") else "")
    return f"| {r['ticker']:<6} | {action:<34} | {dollars:>8} | {px:>8} | {rsi:>4} | {vs:>7} |"


def render(result, review: bool) -> str:
    L = []
    regime = ("ABOVE 200-EMA (risk-on)" if result["regime_ok"]
              else "BELOW 200-EMA (risk-off)") if result["regime_known"] else "UNKNOWN"

    L.append(f"# Allocation advisory — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    L.append(f"**Book:** ${result['book']:,.0f}  |  "
             f"**New cash:** ${result['cash']:,.0f}  |  "
             f"**Regime (QQQ):** {regime}")
    L.append("")
    L.append("| Ticker | Action | Dollars | Price | RSI | vs200 |")
    L.append("|--------|--------|--------:|------:|----:|------:|")

    for r in result["trims"]:
        L.append(_fmt_row(r))
    if review:
        # rebalance view: show every underweight name that passes gates
        for r in result["underweight"]:
            rr = dict(r, action="UNDER", dollars=r["want"],
                      reason=r.get("earn_flag", "") or "to target")
            L.append(_fmt_row(rr))
    else:
        for r in result["buys"]:
            L.append(_fmt_row(r))
    for r in result["blocked"]:
        L.append(_fmt_row(r))

    rendered_any = result["trims"] or result["blocked"] or (
        result["underweight"] if review else result["buys"])
    if not rendered_any:
        L.append("| — | nothing actionable | — | — | — | — |")

    # 3-line summary
    deployed = sum(b["dollars"] for b in result["buys"])
    n_buy = len(result["buys"])
    L.append("")
    L.append("## Summary")
    if review:
        under_total = sum(r["want"] for r in result["underweight"])
        L.append(f"- **Review mode** (no new cash). {len(result['underweight'])} underweight "
                 f"name(s) totaling ${under_total:,.0f} to target; "
                 f"{len(result['trims'])} trim candidate(s); "
                 f"{len(result['blocked'])} blocked.")
    else:
        mg = result["margin"]
        margin_note = f" (incl. ${mg['used']:,.0f} margin)" if mg["used"] > 0.01 else ""
        pool = result['cash'] + mg['allowed']
        L.append(f"- Deployed **${deployed:,.0f}**{margin_note} of ${pool:,.0f} available "
                 f"(${result['cash']:,.0f} cash + ${mg['allowed']:,.0f} margin) across "
                 f"**{n_buy} buy(s)**; ${result['cash_left']:,.0f} left.")
    L.append(f"- Regime **{regime}** (informational — no longer gates buys; "
             "see `reports/regime_backtest.md`).")
    cluster_bits = "; ".join(
        f"{c['name']} ${c['value']:,.0f} "
        f"({c['value']/result['book']*100 if result['book'] else 0:.1f}% of book, "
        f"cap {c['pct']:.0f}%)"
        for c in result.get("clusters", []))
    L.append(f"- **{len(result['trims'])} trim(s)**, "
             f"**{len(result['blocked'])} blocked**"
             + (f"; {cluster_bits}." if cluster_bits else "."))
    # ---- PHQ-2026-02: NO ADD tables (gated / issuer ceiling / common-driver) --
    gated = result.get("no_add_gated") or []
    if gated:
        L.append("")
        L.append("## NO ADD — GATED (target capital held as cash, no renormalization)")
        L.append("| Ticker | Target | Current | Status | Authority | Next gate |")
        L.append("|--------|-------:|--------:|--------|-----------|-----------|")
        for r in sorted(gated, key=lambda x: x["ticker"]):
            held = "holds existing shares" if r["holds_existing_shares"] else "no position"
            L.append(f"| {r['ticker']:<6} | ${r['target']:,.0f} | ${r['current']:,.0f} "
                     f"({held}) | {r['status']} | {r['authority']} | {r['next_gate']} |")

    issuer_no_add = result.get("no_add_issuer") or []
    if issuer_no_add:
        L.append("")
        L.append("## NO ADD — ISSUER CEILING (8% effective-issuer, PHQ-2026-01/02)")
        L.append("| Ticker | Current effective | Ceiling |")
        L.append("|--------|-------------------:|--------:|")
        for r in issuer_no_add:
            L.append(f"| {r['ticker']:<6} | {r['current_effective_pct']:.2f}% | "
                     f"{r['ceiling_pct']:.1f}% |")

    cd_no_add = result.get("no_add_common_driver") or []
    if cd_no_add:
        L.append("")
        L.append("## NO ADD — COMMON-DRIVER CEILING (40% AI/platform, PHQ-2026-01/02)")
        L.append("| Ticker | Current aggregate | Ceiling |")
        L.append("|--------|-------------------:|--------:|")
        for r in cd_no_add:
            L.append(f"| {r['ticker']:<6} | {r['current_common_driver_pct']:.2f}% | "
                     f"{r['ceiling_pct']:.1f}% |")

    cd_pct = result.get("common_driver_current_pct")
    if cd_pct is not None:
        retained = result.get("retained_common_driver_measurement") or {}
        L.append("")
        L.append("## 40% AI/platform common-driver exposure")
        L.append(f"- **Current calculated: {cd_pct:.4f}%** (live, from reconciled holdings "
                 f"+ current prices, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) vs "
                 f"**{result.get('common_driver_ceiling_pct', 40.0):.1f}% ceiling**.")
        if retained:
            L.append(f"- **Retained policy measurement: {retained.get('value_pct')}%** "
                     f"(point-in-time, measured {retained.get('measured_at')}, "
                     f"{retained.get('methodology')}) — **above ceiling, not rounded into "
                     f"compliance, may not be increased without separate principal "
                     f"approval** (PHQ-2026-01 point 9, PHQ-2026-02).")

    unresolved = result.get("unresolved") or {}
    if unresolved:
        L.append("")
        L.append("## UNRESOLVED — PRINCIPAL POLICY DECISION REQUIRED")
        for t, v in sorted(unresolved.items()):
            L.append(f"- **{t}** (${v:,.0f}, counts toward book, no canonical target, "
                     "no buy/trim/exit instruction).")

    mg = result["margin"]
    if mg["debt"] > 0 or mg["requested"] > 0:
        lev_s = f"{mg['leverage_current']:.2f}x" if mg["leverage_current"] is not None else "n/a"
        buf_s = f"{mg['buffer_pct']:.1f}%" if mg["buffer_pct"] is not None else "unsynced"
        synced_at = mg.get("synced_at")
        age_days = _margin_buffer_age_days(synced_at)
        L.append("")
        L.append("## Margin")
        L.append("| | |")
        L.append("|---|---:|")
        L.append(f"| Gross / net equity | ${mg['gross']:,.0f} / ${mg['net_equity']:,.0f} |")
        L.append(f"| Margin debt | ${mg['debt']:,.0f} |")
        L.append(f"| Leverage (gross/equity) | {lev_s} vs {mg['leverage_cap']:.2f}x cap |")
        L.append(f"| Buffer (last synced) | {buf_s} vs {mg['buffer_floor_pct']:.0f}% floor |")
        if mg["requested"] > 0:
            L.append(f"| Margin requested / allowed | ${mg['requested']:,.0f} / ${mg['allowed']:,.0f} |")
        if mg["forced_delever"]:
            L.append("")
            L.append(f"> ⚠️ **FORCED DE-LEVER — {mg['block_reason']}.** "
                      "No margin-funded buying this cycle; trim or pay down debt.")
        elif mg["block_reason"]:
            L.append("")
            L.append(f"> Margin request clipped — {mg['block_reason']}.")
        stale_banner_shown = age_days is not None and age_days >= STALE_MARGIN_DAYS
        unverifiable_banner_shown = age_days is None and mg["requested"] > 0
        if stale_banner_shown:
            L.append("")
            L.append(f"> ⚠️ **Margin data is {age_days} day(s) old** (last synced {synced_at}) — "
                      "re-check Robinhood and run `update-margin` before trusting this leverage/buffer read.")
        elif unverifiable_banner_shown:
            L.append("")
            L.append("> ⚠️ **No valid sync date on record for margin state** (missing, "
                      "malformed, or in the future) — run `update-margin` to establish one.")
        ms = result.get("margin_state")
        if ms is not None:
            L.append("")
            L.append(f"**Margin risk state: {ms.current_state}**")
            if ms.reasons:
                for reason in ms.reasons:
                    # The banners above already surfaced these same facts (age +
                    # synced_at + a call to action) -- skip classify_margin_state()'s
                    # own same-fact reason line here so the two don't say the same
                    # thing twice.
                    if stale_banner_shown and reason.startswith("margin data is") \
                            and "day(s) old" in reason:
                        continue
                    if unverifiable_banner_shown and reason.startswith("margin sync date is"):
                        continue
                    L.append(f"- {reason}")
            if ms.violated_constraints:
                L.append(f"- Violated constraints: {', '.join(ms.violated_constraints)}")
            L.append(f"- Allowed actions: {', '.join(ms.allowed_actions)}")
            if ms.concentration_source:
                L.append(f"- Tightest concentration pressure: {ms.concentration_source} "
                         f"({ms.risk_metrics.get('concentration_score', 0.0):.2f})")
        L.append("")
        L.append("_Buffer is synced from Robinhood via `update-margin`, not live — "
                  "verify before any large margin-funded buy._")
    L.append("")
    L.append("_Advisory only. This tool places no orders. Execute manually._")
    return "\n".join(L)


def render_health(result) -> str:
    """Snapshot risk/health view — pure presentation. Consumes only `result`
    (plan()'s output, plus whatever main() has already attached to it, e.g.
    `margin_state`); never reads YAML, never fetches, never recomputes a
    portfolio ratio plan() didn't already compute. V1 scope: leverage, buffer,
    margin risk state, cluster caps, and 8%/40% no-add ceilings — a
    point-in-time snapshot only, no historical trend, no repayment
    recommendation, no new buy/trim/block decision of any kind."""
    L = []
    L.append(f"# Portfolio Health View — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    L.append(f"**Book:** ${result['book']:,.0f}")

    mg = result["margin"]
    lev_s = f"{mg['leverage_current']:.2f}x" if mg["leverage_current"] is not None else "n/a"
    buf_s = f"{mg['buffer_pct']:.1f}%" if mg["buffer_pct"] is not None else "unsynced"
    L.append("")
    L.append("## Margin")
    L.append("| | |")
    L.append("|---|---:|")
    L.append(f"| Leverage (gross/equity) | {lev_s} vs {mg['leverage_cap']:.2f}x cap |")
    L.append(f"| Buffer (last synced) | {buf_s} vs {mg['buffer_floor_pct']:.0f}% floor |")

    L.append("")
    L.append("## Margin risk state")
    ms = result.get("margin_state")
    if ms is None:
        L.append("> ⚠️ **UNAVAILABLE** — margin risk state was not computed for this "
                  "result (`classify_margin_state()` was never run against it). This is "
                  "a data-availability gap, not a risk finding — do not read it as NORMAL.")
    else:
        L.append(f"**{ms.current_state}**")
        for reason in ms.reasons:
            L.append(f"- {reason}")
        if ms.violated_constraints:
            L.append(f"- Violated constraints: {', '.join(ms.violated_constraints)}")
        if ms.allowed_actions:
            L.append(f"- Allowed actions: {', '.join(ms.allowed_actions)}")
        if ms.concentration_source:
            L.append(f"- Tightest concentration pressure: {ms.concentration_source} "
                     f"({ms.risk_metrics.get('concentration_score', 0.0):.2f})")

    L.append("")
    L.append("## Clusters")
    clusters = result.get("clusters") or []
    if clusters:
        L.append("| Cluster | %-of-book | Cap | Ratio-to-cap |")
        L.append("|---|---:|---:|---:|")
        for c in clusters:
            pct_s = f"{c['current_pct']:.1f}%" if c.get("current_pct") is not None else "n/a"
            ratio_s = f"{c['ratio_to_cap']:.2f}x" if c.get("ratio_to_cap") is not None else "n/a"
            L.append(f"| {c['name']} | {pct_s} | {c['pct']:.0f}% | {ratio_s} |")
    else:
        L.append("_No clusters configured._")

    L.append("")
    L.append("## 8%/40% no-add ceilings (PHQ-2026-02)")
    L.append(f"- Common-driver current: {result.get('common_driver_current_pct', 0.0):.2f}% "
             f"vs {result.get('common_driver_ceiling_pct', 40.0):.1f}% ceiling.")
    retained = result.get("retained_common_driver_measurement") or {}
    if retained:
        L.append(f"- Retained policy measurement: {retained.get('value_pct')}% "
                 f"(point-in-time, {retained.get('measured_at')}) — above ceiling.")
    issuer_exp = result.get("issuer_exposure") or {}
    if issuer_exp:
        L.append("| Issuer | Effective | Ceiling |")
        L.append("|--------|----------:|--------:|")
        for tk, v in sorted(issuer_exp.items(), key=lambda kv: -kv[1]["effective_pct"]):
            L.append(f"| {tk:<6} | {v['effective_pct']:.2f}% | "
                     f"{result.get('issuer_ceiling_pct', 8.0):.1f}% |")

    L.append("")
    L.append("_Crypto sleeve and T1/T2 proximity views retired by PHQ-2026-02's migration "
              "to the canonical v1.30 flat per-ticker destination architecture — BTC/ETH/SOL "
              "and every former T1/T2 name now report through the ordinary buy/hold/gated "
              "tables above like any other destination ticker._")

    L.append("")
    L.append("_Snapshot only — no historical trend, no repayment recommendation. "
              "Advisory only. This tool places no orders._")
    return "\n".join(L)


# ── update-holdings ─────────────────────────────────────────────────────────────

BOOK_CHANGE_WARN_PCT = 30.0   # abort write if book moves more than this without --confirm


def _parse_ticker_value_pairs(text: str) -> dict[str, float]:
    """Accept any whitespace layout: one pair per line OR many pairs per line.
    Walk tokens, pairing a ticker with the numeric value that follows it."""
    tokens = text.replace("$", "").replace(",", "").split()
    new: dict[str, float] = {}
    pending: str | None = None
    for tok in tokens:
        try:
            val = float(tok)
        except ValueError:
            if pending is not None:
                print(f"  skipped (no value for {pending!r})", file=sys.stderr)
            pending = tok.upper()
            continue
        if pending is None:
            print(f"  skipped (value {tok!r} with no ticker)", file=sys.stderr)
            continue
        new[pending] = val
        pending = None
    if pending is not None:
        print(f"  skipped (no value for {pending!r})", file=sys.stderr)
    return new


def update_holdings(replace: bool = False, confirm: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'TICKER value' lines (e.g. 'TICKER 24.45'). End with Ctrl-D.\n"
          f"Mode: {mode} manual holdings. This is only for positions NOT tracked by "
          f"share/coin count — anything in 'shares' or\n"
          f"'crypto_shares' is live-priced and overrides whatever's pasted here. Use "
          f"'update-shares' for a stock/ETF, 'update-crypto-shares' for a coin.\n",
          file=sys.stderr)
    new = {k: round(v, 2) for k, v in _parse_ticker_value_pairs(sys.stdin.read()).items()}

    # Merge (default) preserves positions you didn't paste; replace overwrites.
    prior = (load_yaml(HOLDINGS_FILE) or {}).get("holdings", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out positions

    # Sanity check: a big book-value swing usually means a partial-paste wipe.
    prior_total = sum(float(v) for v in prior.values())
    new_total = sum(merged.values())
    if prior_total > 0:
        change_pct = (new_total - prior_total) / prior_total * 100
        if abs(change_pct) > BOOK_CHANGE_WARN_PCT and not confirm:
            print(f"\n⚠️  ABORTED — book would change {change_pct:+.1f}% "
                  f"(${prior_total:,.0f} → ${new_total:,.0f}), more than "
                  f"{BOOK_CHANGE_WARN_PCT:.0f}%.\n"
                  f"    Positions: {len(prior)} → {len(merged)}. If intentional, re-run with --confirm.\n"
                  f"    Nothing was written.", file=sys.stderr)
            sys.exit(1)

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    write_state(merged, prior_yaml.get("margin"), prior_yaml.get("shares"),
               prior_yaml.get("crypto_shares"))
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} total manual positions in {HOLDINGS_FILE}", file=sys.stderr)


def update_shares(replace: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'TICKER qty' lines (e.g. 'AAPL 0.138'). End with Ctrl-D.\n"
          f"Mode: {mode} share counts. These are live-priced via Alpaca on every run — "
          f"only update a ticker here after a real buy/sell/trim changes its share "
          f"count.\n", file=sys.stderr)
    new = _parse_ticker_value_pairs(sys.stdin.read())

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    prior = prior_yaml.get("shares", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out (fully sold) positions

    write_state(prior_yaml.get("holdings"), prior_yaml.get("margin"), merged,
               prior_yaml.get("crypto_shares"))
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} share-tracked positions in {HOLDINGS_FILE}", file=sys.stderr)


def update_crypto_shares(replace: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'COIN qty' lines (e.g. 'ETH 0.209385'). End with Ctrl-D.\n"
          f"Mode: {mode} crypto coin counts. Live-priced via Alpaca on every run — "
          f"only update a coin here after a real buy/sell/trim changes its holding.\n",
          file=sys.stderr)
    new = _parse_ticker_value_pairs(sys.stdin.read())

    prior_yaml = load_yaml(HOLDINGS_FILE) if HOLDINGS_FILE.exists() else {}
    prior = prior_yaml.get("crypto_shares", {}) or {}
    existing = {} if replace else prior
    merged = {**{k.upper(): float(v) for k, v in existing.items()}, **new}
    merged = {k: v for k, v in merged.items() if v}   # drop zeroed-out (fully sold) coins

    write_state(prior_yaml.get("holdings"), prior_yaml.get("margin"),
               prior_yaml.get("shares"), merged)
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} crypto-share-tracked coins in {HOLDINGS_FILE}", file=sys.stderr)


def write_state(holdings: dict | None, margin: dict | None, shares: dict | None,
                crypto_shares: dict | None = None):
    """Write holdings.yaml. Each block is written as given — callers that aren't
    changing a given block pass through its prior value so nothing is silently
    dropped."""
    holdings = holdings or {}
    shares = shares or {}
    crypto_shares = crypto_shares or {}
    with open(HOLDINGS_FILE, "w") as f:
        f.write("# holdings.yaml — three tracks. 'shares' (ticker: qty) and\n"
                "# 'crypto_shares' (coin: qty) are the source of truth for any normally\n"
                "# -traded position or coin — live-valued every run via Alpaca (qty x\n"
                "# latest price). Update with 'allocate.py update-shares' / "
                "'update-crypto-shares'\n"
                "# after a real buy/sell/trim changes a count.\n"
                "# 'holdings' (ticker: dollar value) is the manual fallback for anything\n"
                "# NOT share-tracked. Currently empty/unused.\n"
                "# Update it with 'allocate.py update-holdings' if a future ticker needs it.\n")
        if margin:
            f.write("# margin: synced via 'allocate.py update-margin <debt> <buffer_pct>' — "
                    "buffer_pct comes from Robinhood directly (per-security maintenance\n"
                    "# ratios aren't available via Alpaca), so it's only as fresh as the "
                    "last sync. Verify on Robinhood before any large margin-funded buy.\n"
                    "# IMPORTANT: always use Robinhood's own DISPLAYED buffer % — do not derive\n"
                    "# it from (portfolio value - maint req) / portfolio value. Checked twice\n"
                    "# against real screens and it doesn't reconcile (off by several points);\n"
                    "# Robinhood's actual formula weights something this simple subtraction misses.\n"
                    "margin:\n"
                    f"  debt: {round(float(margin.get('debt', 0.0)), 2)}\n"
                    f"  buffer_pct: {round(float(margin.get('buffer_pct', 0.0)), 2)}\n"
                    f"  synced_at: {margin.get('synced_at') or date.today().isoformat()}\n")
        f.write("holdings:\n")
        if holdings:
            for t in sorted(holdings):
                f.write(f"  {t}: {round(holdings[t], 2)}\n")
        else:
            f.write("  {}\n")
        f.write("shares:\n")
        if shares:
            for t in sorted(shares):
                f.write(f"  {t}: {shares[t]}\n")
        else:
            f.write("  {}\n")
        f.write("crypto_shares:\n")
        if crypto_shares:
            for c in sorted(crypto_shares):
                f.write(f"  {c}: {crypto_shares[c]}\n")
        else:
            f.write("  {}\n")
    log_performance(quiet=True)   # auto-snapshot on every holdings/shares/margin sync


def update_margin(debt: float, buffer_pct: float):
    prior = load_yaml(HOLDINGS_FILE) or {}
    write_state(prior.get("holdings"), {"debt": debt, "buffer_pct": buffer_pct,
                          "synced_at": date.today().isoformat()}, prior.get("shares"),
               prior.get("crypto_shares"))
    print(f"margin synced: debt=${debt:,.2f} buffer={buffer_pct:.2f}% in {HOLDINGS_FILE}",
          file=sys.stderr)


# ── performance log (net equity vs QQQ/VOO) ─────────────────────────────────────
# Descriptive only — logs realized book value against a benchmark. Does not
# predict, does not gate any buy/trim decision. See render_performance() for
# the deposit/withdrawal caveat this comparison can't correct for.

def _read_perf_log() -> list[dict]:
    if not PERF_LOG_FILE.exists():
        return []
    with open(PERF_LOG_FILE, newline="") as f:
        return list(csv.DictReader(f))


def log_performance(note: str = "", client=None, quiet: bool = False,
                   resolved_holdings: dict | None = None):
    """Snapshot net equity + QQQ/VOO vs performance_log.csv. Called automatically
    after update-holdings, update-shares, update-margin, and every allocate run —
    never lets a price-fetch failure block the primary action it's piggybacking on.
    Pass 'resolved_holdings' (already live-priced, e.g. from main()'s primary flow)
    to avoid a second round of per-ticker price fetches; omit it to resolve fresh."""
    holdings_yaml = load_yaml(HOLDINGS_FILE) or {}
    margin_state = holdings_yaml.get("margin", {}) or {}
    margin_debt = float(margin_state.get("debt", 0.0))
    # Fallback gross if live resolution fails below: last raw 'holdings' dict on
    # file (misses share-tracked positions, but keeps this from crashing).
    gross = sum(float(v) for v in (holdings_yaml.get("holdings", {}) or {}).values())

    c = client or AlpacaPaperClient()
    if resolved_holdings is not None:
        gross = sum(float(v) for v in resolved_holdings.values())
    else:
        try:
            gross = sum(float(v) for v in resolve_holdings(c).values())
        except Exception as e:
            if not quiet:
                print(f"  (performance log: couldn't resolve live holdings — {e})", file=sys.stderr)
    net_equity = gross - margin_debt

    qqq_price = voo_price = None
    try:
        qqq = c.get_bars("QQQ", "1Day", limit=1, days_back=5)
        voo = c.get_bars("VOO", "1Day", limit=1, days_back=5)
        qqq_price = qqq[-1]["c"] if qqq else None
        voo_price = voo[-1]["c"] if voo else None
    except Exception as e:
        if not quiet:
            print(f"  (performance log: couldn't fetch QQQ/VOO — {e})", file=sys.stderr)

    rows = _read_perf_log()
    today = date.today().isoformat()
    rows = [r for r in rows if r["date"] != today]   # idempotent same-day re-log
    rows.append({"date": today, "net_equity": round(net_equity, 2),
                "gross": round(gross, 2), "margin_debt": round(margin_debt, 2),
                "qqq_price": qqq_price, "voo_price": voo_price, "note": note})
    rows.sort(key=lambda r: r["date"])

    with open(PERF_LOG_FILE, "w", newline="") as f:
        # csv's default "excel" dialect writes CRLF regardless of platform;
        # every other tracked file in this repo is LF-only, and CI's
        # git-diff-check step flags a rewritten CRLF row as trailing
        # whitespace. Force LF to match repo convention.
        w = csv.DictWriter(f, fieldnames=PERF_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    if quiet:
        print(f"  (performance snapshot updated: net equity ${net_equity:,.2f})", file=sys.stderr)
    else:
        print(f"logged: {today} net_equity=${net_equity:,.2f} QQQ=${qqq_price} VOO=${voo_price} "
              f"in {PERF_LOG_FILE}", file=sys.stderr)


def render_performance() -> str:
    rows = _read_perf_log()
    if len(rows) < 2:
        return ("# Performance log\n\nNot enough history yet — "
                f"{len(rows)} snapshot(s) logged. Run `log-performance` again on a "
                "future date to get a comparison.")

    first, last = rows[0], rows[-1]
    prev = rows[-2] if len(rows) >= 2 else first

    def pct(a, b):
        a, b = float(a), float(b)
        return (b / a - 1) * 100 if a else None

    def fmt(p):
        return f"{p:+.1f}%" if p is not None else "n/a"

    L = ["# Performance log — net equity vs QQQ/VOO", "",
        f"**{len(rows)} snapshot(s)** logged, {first['date']} → {last['date']}", "",
        "| | Since first log | Since last log |",
        "|---|---:|---:|",
        f"| Net equity | {fmt(pct(first['net_equity'], last['net_equity']))} "
        f"| {fmt(pct(prev['net_equity'], last['net_equity']))} |",
        f"| QQQ | {fmt(pct(first['qqq_price'], last['qqq_price']))} "
        f"| {fmt(pct(prev['qqq_price'], last['qqq_price']))} |",
        f"| VOO | {fmt(pct(first['voo_price'], last['voo_price']))} "
        f"| {fmt(pct(prev['voo_price'], last['voo_price']))} |",
        "", "_Latest snapshot:_",
        f"- {last['date']}: net equity ${float(last['net_equity']):,.0f}, "
        f"gross ${float(last['gross']):,.0f}, margin debt ${float(last['margin_debt']):,.0f}"
        + (f" — _{last['note']}_" if last.get("note") else ""),
        "",
        "> ⚠️ **This is a rough directional check, not a precise return calc.** "
        "Net equity moves from deposits, withdrawals, and margin draws/paydowns, "
        "none of which are backed out here — a big deposit between snapshots will "
        "show up as \"growth\" that has nothing to do with market performance. "
        "Treat divergence from QQQ/VOO as a prompt to look closer, not a verdict.",
    ]
    return "\n".join(L)


# ── main ────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "update-holdings":
        update_holdings(replace="--replace" in sys.argv,
                        confirm="--confirm" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-shares":
        update_shares(replace="--replace" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-crypto-shares":
        update_crypto_shares(replace="--replace" in sys.argv)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "update-margin":
        if len(sys.argv) != 4:
            print("usage: allocate.py update-margin <debt> <buffer_pct>", file=sys.stderr)
            sys.exit(1)
        update_margin(float(sys.argv[2]), float(sys.argv[3]))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "log-performance":
        log_performance(note=" ".join(sys.argv[2:]))
        return

    ap = argparse.ArgumentParser(description="Manual-allocation advisor (no orders).")
    ap.add_argument("--cash", type=float, default=0.0, help="new cash to deploy")
    ap.add_argument("--margin", type=float, default=0.0,
                    help="margin-funded buying power requested this cycle "
                         "(clipped to the 1.8x leverage cap / blocked below the buffer floor)")
    ap.add_argument("--review", action="store_true", help="rebalance check, no new cash")
    ap.add_argument("--levels", action="store_true", help="buy-level staging report")
    ap.add_argument("--ticker", type=str, default=None, help="limit --levels to one ticker")
    ap.add_argument("--performance", action="store_true",
                    help="show net-equity-vs-QQQ/VOO log (see log-performance to add a snapshot)")
    ap.add_argument("--health", action="store_true",
                    help="snapshot risk/health view (leverage, buffer, clusters, "
                         "8%%/40%% no-add ceilings) — observational, no new cash")
    ap.add_argument("--no-log", action="store_true",
                    help="suppress the timestamped allocation-log file and the "
                         "performance_log.csv snapshot this run would otherwise write, "
                         "for a genuinely read-only check. Only valid together with "
                         "--review (a real --cash/--margin run must keep its audit "
                         "trail; --health never writes a log to begin with). Standard "
                         "behavior (both writes happen) is unchanged when this flag "
                         "is omitted.")
    args = ap.parse_args()
    if args.no_log and not args.review:
        ap.error("--no-log is only valid together with --review — it exists to keep "
                 "the read-only phone check read-only. A --cash/--margin allocation "
                 "run must keep its audit trail (log file + performance_log.csv), and "
                 "--health never writes either to begin with, so --no-log is not "
                 "needed there.")
    if args.performance:
        print(render_performance())
        return
    if args.review or args.health:
        args.cash = 0.0
        args.margin = 0.0

    if args.levels:
        from levels import run_levels
        targets = load_yaml(TARGETS_FILE)
        out = run_levels(targets, AlpacaPaperClient(), only_ticker=args.ticker)
        print(out)
        LOGS_DIR.mkdir(exist_ok=True)
        log_path = LOGS_DIR / f"levels-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.md"
        log_path.write_text(out + "\n")
        print(f"\n[logged to {log_path}]", file=sys.stderr)
        return

    targets = load_yaml(TARGETS_FILE)
    holdings_yaml = load_yaml(HOLDINGS_FILE) or {}
    margin_state = holdings_yaml.get("margin", {}) or {}
    margin_debt = float(margin_state.get("debt", 0.0))
    margin_buffer_pct = margin_state.get("buffer_pct")
    margin_buffer_pct = float(margin_buffer_pct) if margin_buffer_pct is not None else None
    roster = build_roster(targets)
    if not roster:
        print("No tickers in targets.yaml — paste your roster into the "
              "destination list.", file=sys.stderr)
        sys.exit(1)
    gates_cfg = load_gates()
    lookthrough = load_issuer_lookthrough()

    client = AlpacaPaperClient()
    # RESERVE/CASH aren't market tickers — never fetch bars for them.
    market_tickers = [tk for tk, meta in roster.items()
                      if meta["asset_class"] not in ("crypto", "reserve", "cash")]
    metrics, regime_ok, regime_known = fetch_market(
        client, market_tickers, targets.get("regime_ticker", "QQQ"))

    # Crypto prices fetched BEFORE resolve_holdings so plan()'s gap math (which
    # reads crypto values straight out of 'holdings') uses live qty x price
    # too, not just the display table below. Coin list now comes from
    # targets.yaml's `destination:` (asset_class: crypto), per PHQ-2026-02 —
    # each coin carries its own target_pct there, replacing the prior
    # aggregate crypto.sleeve_pct sleeve.
    coins = [tk for tk, meta in roster.items() if meta["asset_class"] == "crypto"]
    prices = fetch_crypto(client, coins, {}) if coins else {}
    crypto_price_map = {c: d["price"] for c, d in prices.items() if d["price"] is not None}

    holdings = resolve_holdings(client, metrics, crypto_price_map)  # live qty x price

    result = plan(targets, holdings, roster, metrics, regime_ok, regime_known, args.cash,
                  margin_debt=margin_debt, margin_buffer_pct=margin_buffer_pct,
                  margin_requested=args.margin, gates_cfg=gates_cfg, lookthrough=lookthrough)
    result["margin"]["synced_at"] = margin_state.get("synced_at")

    # ---- margin risk-state classification (Phase 2D) -----------------------
    # Pure post-hoc read of plan()'s own output — computed AFTER plan() has
    # already decided every buy/trim/block; cannot influence allocation.
    # Concentration scope: cluster-cap proximities only.
    # ratio_to_cap is computed once in plan() (same guard: pct>0 and book>0) —
    # read here, never recomputed, so this formula has exactly one owner.
    cluster_proximities = {
        f"cluster:{c['name']}": c["ratio_to_cap"]
        for c in result.get("clusters", [])
        if c.get("ratio_to_cap") is not None
    }
    concentration_score, concentration_source = concentration_risk_score(cluster_proximities)
    margin_cfg = targets.get("margin", {}) or {}
    states_cfg = margin_cfg.get("states", {}) or {}
    caution_cfg = states_cfg.get("caution", {}) or {}
    restricted_cfg = states_cfg.get("restricted", {}) or {}
    concentration_cfg = margin_cfg.get("concentration_adjustment", {}) or {}
    synced_at_raw = margin_state.get("synced_at")
    buffer_data_age_days = _margin_buffer_age_days(synced_at_raw)
    buffer_data_unverifiable = _margin_buffer_age_unverifiable(synced_at_raw)
    result["margin_state"] = classify_margin_state(
        gross=result["margin"]["gross"],
        margin_debt=result["margin"]["debt"],
        buffer_pct=result["margin"]["buffer_pct"],
        leverage_cap=result["margin"]["leverage_cap"],
        buffer_floor_pct=result["margin"]["buffer_floor_pct"],
        concentration_score=concentration_score,
        concentration_source=concentration_source,
        buffer_data_age_days=buffer_data_age_days,
        stale_threshold_days=float(STALE_MARGIN_DAYS),
        buffer_data_unverifiable=buffer_data_unverifiable,
        caution_leverage_fraction=caution_cfg.get("leverage_fraction_of_cap"),
        caution_buffer_comfort_multiplier=caution_cfg.get("buffer_comfort_multiplier"),
        restricted_leverage_fraction=restricted_cfg.get("leverage_fraction_of_cap"),
        restricted_buffer_comfort_multiplier=restricted_cfg.get("buffer_comfort_multiplier"),
        concentration_tightening_coefficient=concentration_cfg.get("tightening_coefficient") or 0.0,
        concentration_min_fraction=(0.5 if concentration_cfg.get("min_fraction") is None
                                     else concentration_cfg["min_fraction"]),
    )

    if args.health:
        print(render_health(result))
        return

    out = render(result, review=args.review)
    print(out)

    if args.no_log:
        print("\n[--no-log: allocation log and performance_log.csv snapshot both "
              "suppressed]", file=sys.stderr)
    else:
        LOGS_DIR.mkdir(exist_ok=True)
        log_path = LOGS_DIR / f"allocation-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.md"
        log_path.write_text(out + "\n")
        print(f"\n[logged to {log_path}]", file=sys.stderr)
        log_performance(client=client, quiet=True, resolved_holdings=holdings)   # auto-snapshot


if __name__ == "__main__":
    main()
