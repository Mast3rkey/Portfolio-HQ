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
    python allocate.py update-holdings   # paste "TICKER value" lines, Ctrl-D
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
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

DAILY_LIMIT = 300
DAYS_BACK = 420


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


# ── core allocation logic ──────────────────────────────────────────────────────

def plan(targets, holdings, roster, metrics, regime_ok, regime_known, cash):
    gates = targets.get("gates", {})
    caps = targets.get("caps", {})
    min_lot = float(gates.get("min_lot_dollars", 25))
    trend_rsi_override = float(gates.get("trend_rsi_override", 30))
    blackout_days = int(gates.get("earnings_blackout_days", 7))
    trim_rsi = float(gates.get("trim_rsi", 60))
    semis = {s.upper() for s in caps.get("semis_tickers", [])}
    semis_cap_pct = float(caps.get("semis_cluster_pct", 25))

    book = sum(float(v) for v in holdings.values()) + float(cash)
    semis_value = sum(float(holdings.get(t, 0)) for t in semis)

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

        buy_candidates.append({**base, "is_semis": tk in semis,
                               "max_by_name": max_by_name,
                               "want": min(gap, max_by_name),
                               "earn_flag": base.get("earn_flag", "")})

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
                "gap": sleeve_gap, "is_semis": False, "max_by_name": sleeve_gap,
                "want": sleeve_gap,
                "earn_flag": f"sleeve {'/'.join(sleeve_coins)}, no timing gates"})

    # ---- greedy allocation to largest passing gaps -----------------------
    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    cash_left = float(cash)
    buys: list[dict] = []
    for c in buy_candidates:
        want = min(c["gap"], c["max_by_name"])
        # semis cluster cap
        if c["is_semis"]:
            semis_room = book * semis_cap_pct / 100.0 - semis_value
            if semis_room < min_lot:
                rows.append({**c, "action": "BLOCKED", "dollars": 0,
                             "reason": f"semis cluster cap {semis_cap_pct:.0f}%"})
                continue
            want = min(want, semis_room)
        alloc = min(want, cash_left)
        if alloc < min_lot:
            if cash_left < min_lot and cash > 0:
                rows.append({**c, "action": "BLOCKED", "dollars": 0,
                             "reason": "cash exhausted"})
            continue
        buys.append({**c, "action": "BUY", "dollars": alloc,
                     "reason": c.get("earn_flag", "")})
        cash_left -= alloc
        if c["is_semis"]:
            semis_value += alloc

    buy_candidates.sort(key=lambda r: r["gap"], reverse=True)
    crypto_coins = {c.upper() for c in targets.get("crypto", {}).get("coins", [])}
    orphans = {t: float(v) for t, v in holdings.items()
               if t.upper() not in roster and t.upper() not in crypto_coins}
    return {
        "book": book, "cash": float(cash), "cash_left": cash_left,
        "buys": buys, "trims": trims, "blocked": rows,
        "underweight": buy_candidates, "orphans": orphans,
        "regime_ok": regime_ok, "regime_known": regime_known,
        "semis_value": semis_value, "semis_cap_pct": semis_cap_pct,
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

    L.append(f"# Allocation advisory — {date.today().isoformat()}")
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
        L.append(f"- Deployed **${deployed:,.0f}** of ${result['cash']:,.0f} across "
                 f"**{n_buy} buy(s)**; ${result['cash_left'] if not bearish else result['cash']:,.0f} left as cash.")
    L.append(f"- Regime **{regime}**"
             + ("  → holding cash." if bearish else "."))
    L.append(f"- **{len(result['trims'])} trim(s)**, "
             f"**{len(result['blocked'])} blocked**; semis cluster "
             f"${result['semis_value']:,.0f} "
             f"({result['semis_value']/result['book']*100 if result['book'] else 0:.1f}% "
             f"of book, cap {result['semis_cap_pct']:.0f}%).")
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
    L.append("")
    L.append("_Advisory only. This tool places no orders. Execute manually._")
    return "\n".join(L)


# ── update-holdings ─────────────────────────────────────────────────────────────

BOOK_CHANGE_WARN_PCT = 30.0   # abort write if book moves more than this without --confirm


def update_holdings(replace: bool = False, confirm: bool = False):
    mode = "REPLACE all" if replace else "MERGE into existing"
    print(f"Paste 'TICKER value' lines (e.g. 'NVDA 1234.56'). End with Ctrl-D.\n"
          f"Mode: {mode} holdings. Pasted tickers are updated; others kept "
          f"(use --replace to overwrite the whole file).\n", file=sys.stderr)
    # Accept any whitespace layout: one pair per line OR many pairs per line.
    # Walk tokens, pairing a ticker with the numeric value that follows it.
    text = sys.stdin.read().replace("$", "").replace(",", "")
    tokens = text.split()
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
        new[pending] = round(val, 2)
        pending = None
    if pending is not None:
        print(f"  skipped (no value for {pending!r})", file=sys.stderr)

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

    with open(HOLDINGS_FILE, "w") as f:
        f.write("# holdings.yaml — {ticker: market_value}. Written by "
                "'allocate.py update-holdings' (merge unless --replace).\nholdings:\n")
        if merged:
            for t in sorted(merged):
                f.write(f"  {t}: {round(merged[t], 2)}\n")
        else:
            f.write("  {}\n")
    action = "wrote" if replace else f"merged {len(new)} into"
    print(f"{action} {len(merged)} total positions in {HOLDINGS_FILE}", file=sys.stderr)


# ── main ────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "update-holdings":
        update_holdings(replace="--replace" in sys.argv,
                        confirm="--confirm" in sys.argv)
        return

    ap = argparse.ArgumentParser(description="Manual-allocation advisor (no orders).")
    ap.add_argument("--cash", type=float, default=0.0, help="new cash to deploy")
    ap.add_argument("--review", action="store_true", help="rebalance check, no new cash")
    ap.add_argument("--levels", action="store_true", help="buy-level staging report")
    ap.add_argument("--ticker", type=str, default=None, help="limit --levels to one ticker")
    args = ap.parse_args()
    if args.review:
        args.cash = 0.0

    if args.levels:
        from levels import run_levels
        targets = load_yaml(TARGETS_FILE)
        out = run_levels(targets, AlpacaPaperClient(), only_ticker=args.ticker)
        print(out)
        LOGS_DIR.mkdir(exist_ok=True)
        log_path = LOGS_DIR / f"levels-{date.today().isoformat()}.md"
        log_path.write_text(out + "\n")
        print(f"\n[logged to {log_path}]", file=sys.stderr)
        return

    targets = load_yaml(TARGETS_FILE)
    holdings = (load_yaml(HOLDINGS_FILE) or {}).get("holdings", {}) or {}
    roster = build_roster(targets)
    if not roster:
        print("No tickers in targets.yaml — paste your roster into the tier lists.",
              file=sys.stderr)
        sys.exit(1)

    client = AlpacaPaperClient()
    metrics, regime_ok, regime_known = fetch_market(
        client, list(roster), targets.get("regime_ticker", "QQQ"))

    result = plan(targets, holdings, roster, metrics, regime_ok, regime_known, args.cash)

    # Crypto sleeve — priced live, valued from holdings.yaml, never gated/traded.
    crypto_cfg = targets.get("crypto", {})
    coins = crypto_cfg.get("coins", []) or []
    if coins:
        prices = fetch_crypto(client, coins, crypto_cfg.get("coingecko_ids", {}) or {})
        crypto_holdings = {c: float(holdings.get(c, 0.0)) for c in coins}
        result["crypto"] = {
            "coins": coins, "prices": prices, "holdings": crypto_holdings,
            "sleeve_total": sum(crypto_holdings.values()),
            "sleeve_pct": float(crypto_cfg.get("sleeve_pct", 10)),
        }

    out = render(result, review=args.review)
    print(out)

    LOGS_DIR.mkdir(exist_ok=True)
    log_path = LOGS_DIR / f"allocation-{date.today().isoformat()}.md"
    log_path.write_text(out + "\n")
    print(f"\n[logged to {log_path}]", file=sys.stderr)


if __name__ == "__main__":
    main()
