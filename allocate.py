#!/usr/bin/env python3
"""
allocate.py — manual-allocation ADVISOR. Recommendations only.

This tool NEVER places, modifies, or cancels an order anywhere. It reads your
holdings + target tiers, pulls market data from Alpaca (read-only), applies your
gates, and prints/logs a BUY / TRIM / BLOCKED table plus a short summary. You
execute manually on Robinhood.

Usage:
    python allocate.py --cash 2000       # deploy new cash
    python allocate.py --review          # rebalance check, no new cash
    python allocate.py update-shares         # paste "TICKER qty" lines, Ctrl-D (stocks/ETFs)
    python allocate.py update-crypto-shares  # paste "COIN qty" lines, Ctrl-D (BTC/ETH/SOL)
    python allocate.py update-holdings       # paste "TICKER value" lines, Ctrl-D (SKHY only)
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

HERE = Path(__file__).resolve().parent
TARGETS_FILE = HERE / "targets.yaml"
HOLDINGS_FILE = HERE / "holdings.yaml"
LOGS_DIR = HERE / "logs"
PERF_LOG_FILE = HERE / "performance_log.csv"
PERF_FIELDS = ["date", "net_equity", "gross", "margin_debt", "qqq_price", "voo_price", "note"]

DAILY_LIMIT = 300
DAYS_BACK = 420
STALE_MARGIN_DAYS = 2   # warn if margin debt/buffer haven't been synced in this many days


# ── config / state io ──────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_roster(targets: dict) -> dict:
    """Return {ticker: {tier, weight_pct, fixed, cap_multiple}} across all tiers."""
    roster: dict[str, dict] = {}
    for tier_name, tier in targets.get("tiers", {}).items():
        w = float(tier.get("weight_pct", 0))
        fixed = bool(tier.get("fixed", False))
        cap_mult = float(tier.get("cap_multiple", 1.0))
        for t in tier.get("tickers", []) or []:
            roster[t.upper()] = {
                "tier": tier_name, "weight_pct": w,
                "fixed": fixed, "cap_multiple": cap_mult,
            }
    return roster


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
    live price (SKHY — permanent zero-coverage gap on the free IEX feed — is the only
    remaining manual-only entry). 'shares' and 'crypto_shares' are the source of truth
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


def plan(targets, holdings, roster, metrics, regime_ok, regime_known, cash,
         margin_debt=0.0, margin_buffer_pct=None, margin_requested=0.0):
    gates = targets.get("gates", {})
    caps = targets.get("caps", {})
    margin_cfg = targets.get("margin", {})
    min_lot = float(gates.get("min_lot_dollars", 25))
    trend_rsi_override = float(gates.get("trend_rsi_override", 30))
    blackout_days = int(gates.get("earnings_blackout_days", 7))
    trim_rsi = float(gates.get("trim_rsi", 60))
    # Correlated-cluster concentration caps (semis, power/infra, ...) — each measured
    # against book (net equity), mechanically trimmed on breach, no RSI gate. A ticker
    # may belong to more than one cluster; every cluster it's in must have room for a buy.
    clusters = [{"name": c["name"], "pct": float(c["pct"]),
                "tickers": {t.upper() for t in c["tickers"]}}
               for c in (caps.get("clusters", []) or [])]
    leverage_cap = float(margin_cfg.get("leverage_cap", 1.8))
    buffer_floor_pct = float(margin_cfg.get("buffer_floor_pct", 30.0))

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

    rows: list[dict] = []          # BLOCKED / info rows
    buy_candidates: list[dict] = []
    trims: list[dict] = []

    for tk, meta in roster.items():
        m = metrics.get(tk, {})
        target_dollars = book * meta["weight_pct"] / 100.0
        current = float(holdings.get(tk, 0.0))
        gap = target_dollars - current
        price = m.get("price")
        rsi = m.get("rsi14")
        sma200 = m.get("sma200")
        vs200 = ((price / sma200 - 1) * 100) if (price and sma200) else None

        base = {"ticker": tk, "tier": meta["tier"], "price": price, "rsi": rsi,
                "vs200": vs200, "target": target_dollars, "current": current,
                "gap": gap}
        tk_clusters = [c["name"] for c in clusters if tk in c["tickers"]]
        for cname in tk_clusters:
            cluster_info[cname][tk] = {"current": current, "target": target_dollars,
                                       "price": price, "rsi": rsi, "tier": meta["tier"]}

        # ---- TRIM check (band/spec overweight + hot RSI) ------------------
        cap_mult = meta["cap_multiple"] if meta["tier"] == "band" else (
            1.0 if meta["fixed"] else meta["cap_multiple"])
        if meta["tier"] in ("band", "spec"):
            overweight_limit = target_dollars * (1.25 if meta["tier"] == "band" else 1.0)
            if current > overweight_limit and rsi is not None and rsi > trim_rsi:
                trims.append({**base, "action": "TRIM",
                              "dollars": current - target_dollars,
                              "reason": f"> {'1.25x' if meta['tier']=='band' else '1.0x'} target, RSI {rsi:.1f}>{trim_rsi:.0f}"})
                continue

        # ---- only underweight names are buy candidates -------------------
        if gap < min_lot:
            continue
        if m.get("error") or price is None:
            rows.append({**base, "action": "BLOCKED", "dollars": 0,
                         "reason": f"no-data ({m.get('error','insufficient bars')})"})
            continue

        # ---- TREND gate ---------------------------------------------------
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

        # ---- CAPS: per-name buy ceiling ----------------------------------
        if meta["tier"] == "spec":          # fixed, never above target
            name_ceiling = target_dollars
        elif meta["tier"] == "band":
            name_ceiling = target_dollars * meta["cap_multiple"]
        else:
            name_ceiling = target_dollars
        max_by_name = max(0.0, name_ceiling - current)

        buy_candidates.append({**base, "clusters": tk_clusters,
                               "max_by_name": max_by_name,
                               "want": min(gap, max_by_name),
                               "earn_flag": base.get("earn_flag", "")})

    # ---- CLUSTER CAPS: mechanical trim, no RSI gate --------------------------
    # Correlation/concentration risk limit, not a return-timing call — unlike
    # the opportunistic band/spec RSI-gated trims above, a cap breach trims
    # regardless of momentum. Names already trimmed above (or by an earlier
    # cluster in this loop) are skipped; trims largest-overweight-first,
    # floored at each name's own tier target (never trimmed below it).
    already_trimmed = {t["ticker"] for t in trims}
    for c in clusters:
        cname, cap_pct = c["name"], c["pct"]
        info = cluster_info[cname]
        cluster_value[cname] -= sum(t["dollars"] for t in trims if t["ticker"] in c["tickers"])
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
                "ticker": cand["ticker"], "tier": cand["tier"], "price": cand["price"],
                "rsi": cand["rsi"], "vs200": None, "target": cand["target"],
                "current": cand["current"], "gap": cand["target"] - cand["current"],
                "action": "TRIM", "dollars": amt,
                "reason": f"{cname} cluster cap {cap_pct:.0f}% "
                          f"(${cand['overweight']:,.0f} over own target)"})
            cluster_value[cname] -= amt
            excess -= amt
            already_trimmed.add(cand["ticker"])
            # A ticker trimmed here may also sit in a later cluster in this
            # loop — keep that cluster's view of it consistent.
            for c2 in clusters:
                if cand["ticker"] in cluster_info[c2["name"]]:
                    cluster_info[c2["name"]][cand["ticker"]]["current"] = cand["current"] - amt

    # ---- CRYPTO sleeve competes on gap --------------------------------------
    # Decisions Log (July 2026): conviction-sizing, not a timing call — the
    # sleeve enters the ranking like any underweight, with NO timing gates
    # (no trend/RSI/earnings). Coin split within the sleeve is manual.
    crypto_cfg = targets.get("crypto", {}) or {}
    sleeve_coins = [c.upper() for c in crypto_cfg.get("coins", [])]
    sleeve_pct = float(crypto_cfg.get("sleeve_pct", 0))
    if sleeve_coins and sleeve_pct > 0:
        sleeve_val = sum(float(holdings.get(c, 0.0)) for c in sleeve_coins)
        sleeve_target = book * sleeve_pct / 100.0
        sleeve_gap = sleeve_target - sleeve_val
        if sleeve_gap >= min_lot:
            buy_candidates.append({
                "ticker": "CRYPTO", "tier": "crypto", "price": None, "rsi": None,
                "vs200": None, "target": sleeve_target, "current": sleeve_val,
                "gap": sleeve_gap, "clusters": [], "max_by_name": sleeve_gap,
                "want": sleeve_gap,
                "earn_flag": f"sleeve {'/'.join(sleeve_coins)}, no timing gates"})

    # ---- greedy allocation to largest passing gaps -----------------------
    cluster_pct = {c["name"]: c["pct"] for c in clusters}
    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    cash_left = deployable
    buys: list[dict] = []
    for c in buy_candidates:
        want = min(c["gap"], c["max_by_name"])
        # every cluster this ticker belongs to must have room
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

    deployed_total = sum(b["dollars"] for b in buys)
    margin_used = min(margin_allowed, max(0.0, deployed_total - float(cash)))

    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    crypto_coins = {c.upper() for c in targets.get("crypto", {}).get("coins", [])}
    orphans = {t: float(v) for t, v in holdings.items()
               if t.upper() not in roster and t.upper() not in crypto_coins}
    leverage_current = (gross / net_equity) if net_equity > 0 else None
    return {
        "book": book, "cash": float(cash), "cash_left": cash_left,
        "buys": buys, "trims": trims, "blocked": rows,
        "underweight": buy_candidates, "orphans": orphans,
        "regime_ok": regime_ok, "regime_known": regime_known,
        "clusters": [{"name": c["name"], "value": cluster_value[c["name"]], "pct": c["pct"]}
                    for c in clusters],
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
    bearish = result["regime_known"] and not result["regime_ok"]

    L.append(f"# Allocation advisory — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    L.append(f"**Book:** ${result['book']:,.0f}  |  "
             f"**New cash:** ${result['cash']:,.0f}  |  "
             f"**Regime (QQQ):** {regime}")
    if bearish:
        L.append("")
        L.append("> ⚠️ **REGIME RISK-OFF — recommendation is to HOLD CASH.** "
                 "The buys below are what *would* be bought if regime flips risk-on.")
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
            rr = dict(r)
            if bearish:
                rr["action"] = "HOLD"
                rr["reason"] = "regime risk-off (would-buy)"
            L.append(_fmt_row(rr))
    for r in result["blocked"]:
        L.append(_fmt_row(r))

    rendered_any = result["trims"] or result["blocked"] or (
        result["underweight"] if review else result["buys"])
    if not rendered_any:
        L.append("| — | nothing actionable | — | — | — | — |")

    # 3-line summary
    deployed = 0 if bearish else sum(b["dollars"] for b in result["buys"])
    n_buy = 0 if bearish else len(result["buys"])
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
        margin_note = (f" (incl. ${mg['used']:,.0f} margin)"
                       if not bearish and mg["used"] > 0.01 else "")
        pool = result['cash'] + mg['allowed']
        L.append(f"- Deployed **${deployed:,.0f}**{margin_note} of ${pool:,.0f} available "
                 f"(${result['cash']:,.0f} cash + ${mg['allowed']:,.0f} margin) across "
                 f"**{n_buy} buy(s)**; ${result['cash_left'] if not bearish else pool:,.0f} left.")
    L.append(f"- Regime **{regime}**"
             + ("  → holding cash." if bearish else "."))
    cluster_bits = "; ".join(
        f"{c['name']} ${c['value']:,.0f} "
        f"({c['value']/result['book']*100 if result['book'] else 0:.1f}% of book, "
        f"cap {c['pct']:.0f}%)"
        for c in result.get("clusters", []))
    L.append(f"- **{len(result['trims'])} trim(s)**, "
             f"**{len(result['blocked'])} blocked**"
             + (f"; {cluster_bits}." if cluster_bits else "."))
    cr = result.get("crypto")
    if cr and cr["coins"]:
        book = result["book"]
        sleeve = cr["sleeve_total"]
        actual_pct = (sleeve / book * 100) if book else 0
        target_pct = cr["sleeve_pct"]
        gap_pct = actual_pct - target_pct
        status = ("ON TARGET" if abs(gap_pct) < 0.5
                  else f"OVER by {gap_pct:.1f}pp" if gap_pct > 0
                  else f"UNDER by {-gap_pct:.1f}pp")
        L.append("")
        L.append("## Crypto sleeve")
        L.append("| Coin | Value | Last price | Source |")
        L.append("|------|------:|-----------:|--------|")
        for c in cr["coins"]:
            val = cr["holdings"].get(c, 0.0)
            pd_ = cr["prices"].get(c, {})
            px = pd_.get("price")
            px_s = f"${px:,.2f}" if px else f"n/a ({pd_.get('error','?')})"
            L.append(f"| {c:<4} | ${val:,.0f} | {px_s:>18} | {pd_.get('source','?')} |")
        L.append(f"\n- **Sleeve ${sleeve:,.0f} = {actual_pct:.1f}% of book** vs "
                 f"{target_pct:.0f}% target → **{status}**.")
        target_dollars = book * target_pct / 100
        L.append(f"- Target dollars at {target_pct:.0f}%: ${target_dollars:,.0f} "
                 f"({'add' if gap_pct < 0 else 'trim'} "
                 f"${abs(target_dollars - sleeve):,.0f} to reach target).")

    orphans = result.get("orphans") or {}
    if orphans:
        listing = ", ".join(f"{t} ${v:,.0f}" for t, v in sorted(orphans.items()))
        L.append(f"- ⚠️ **Held, not in roster** (counts toward book, no target): {listing}.")

    mg = result["margin"]
    if mg["debt"] > 0 or mg["requested"] > 0:
        lev_s = f"{mg['leverage_current']:.2f}x" if mg["leverage_current"] is not None else "n/a"
        buf_s = f"{mg['buffer_pct']:.1f}%" if mg["buffer_pct"] is not None else "unsynced"
        age_days = None
        synced_at = mg.get("synced_at")
        if synced_at:
            try:
                age_days = (date.today() - date.fromisoformat(str(synced_at))).days
            except ValueError:
                age_days = None
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
        if age_days is not None and age_days >= STALE_MARGIN_DAYS:
            L.append("")
            L.append(f"> ⚠️ **Margin data is {age_days} day(s) old** (last synced {synced_at}) — "
                      "re-check Robinhood and run `update-margin` before trusting this leverage/buffer read.")
        elif age_days is None and mg["requested"] > 0:
            L.append("")
            L.append("> ⚠️ **No sync date on record for margin state** — run `update-margin` "
                      "to establish one.")
        L.append("")
        L.append("_Buffer is synced from Robinhood via `update-margin`, not live — "
                  "verify before any large margin-funded buy._")
    L.append("")
    L.append("_Advisory only. This tool places no orders. Execute manually._")
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
    print(f"Paste 'TICKER value' lines (e.g. 'SKHY 24.45'). End with Ctrl-D.\n"
          f"Mode: {mode} manual holdings. This is only for positions NOT tracked by "
          f"share/coin count (SKHY is the only one left) — anything in 'shares' or\n"
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
                "# NOT share-tracked: just SKHY now (permanent zero-coverage gap on the\n"
                "# free IEX feed — RSI/trend gates can never fire for it).\n"
                "# Update it with 'allocate.py update-holdings'.\n")
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
        w = csv.DictWriter(f, fieldnames=PERF_FIELDS)
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
    args = ap.parse_args()
    if args.performance:
        print(render_performance())
        return
    if args.review:
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
        print("No tickers in targets.yaml — paste your roster into the tier lists.",
              file=sys.stderr)
        sys.exit(1)

    client = AlpacaPaperClient()
    metrics, regime_ok, regime_known = fetch_market(
        client, list(roster), targets.get("regime_ticker", "QQQ"))

    # Crypto prices fetched BEFORE resolve_holdings so plan()'s sleeve-gap math
    # (which reads crypto values straight out of 'holdings') uses live qty x
    # price too, not just the display table below.
    crypto_cfg = targets.get("crypto", {})
    coins = crypto_cfg.get("coins", []) or []
    prices = (fetch_crypto(client, coins, crypto_cfg.get("coingecko_ids", {}) or {})
              if coins else {})
    crypto_price_map = {c: d["price"] for c, d in prices.items() if d["price"] is not None}

    holdings = resolve_holdings(client, metrics, crypto_price_map)  # live qty x price; SKHY manual

    result = plan(targets, holdings, roster, metrics, regime_ok, regime_known, args.cash,
                  margin_debt=margin_debt, margin_buffer_pct=margin_buffer_pct,
                  margin_requested=args.margin)
    result["margin"]["synced_at"] = margin_state.get("synced_at")

    # Crypto sleeve — priced live via 'crypto_shares' (ETH/SOL) or manual 'holdings'
    # (BTC, until rebuilt), never gated/traded.
    if coins:
        crypto_holdings = {c: float(holdings.get(c, 0.0)) for c in coins}
        result["crypto"] = {
            "coins": coins, "prices": prices, "holdings": crypto_holdings,
            "sleeve_total": sum(crypto_holdings.values()),
            "sleeve_pct": float(crypto_cfg.get("sleeve_pct", 10)),
        }

    out = render(result, review=args.review)
    print(out)

    LOGS_DIR.mkdir(exist_ok=True)
    log_path = LOGS_DIR / f"allocation-{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.md"
    log_path.write_text(out + "\n")
    print(f"\n[logged to {log_path}]", file=sys.stderr)
    log_performance(client=client, quiet=True, resolved_holdings=holdings)   # auto-snapshot


if __name__ == "__main__":
    main()
