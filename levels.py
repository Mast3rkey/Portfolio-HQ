"""
levels.py — buy-level staging report (advisory only; no orders, ever).

For each roster ticker (and the crypto sleeve) compute three ATR-anchored buy
levels below the 50-SMA, apply practicality filters, and stamp a one-word
stance. Levels are staging points for limit orders the user places manually.

Rungs (multipliers config-editable in targets.yaml):
  L1 (shallow)  = 50SMA − m1×ATR
  L2 (standard) = 50SMA − m2×ATR
  L3 (deep)     = max(50SMA − m3×ATR, 200SMA)   # floored at the long-term trend

Practicality filters:
  * level above current price          → "already below — buyable now"
  * level > cap% below current price   → "unlikely near-term" (crash level)
  * L3 below the 60-session swing low  → "below recent support" (trend-break;
    a fill there calls for reassessment, not autopilot buying)
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from indicators import compute_all, swing_low
from earnings import days_until_earnings
from regime_gate import regime_ok_from_closes
from crypto import coingecko_daily_bars

HERE = Path(__file__).resolve().parent
LOGS_DIR = HERE / "logs"

DAILY_LIMIT = 320  # margin above the ~290-300 trading days in DAYS_BACK, so a
                    # holiday-heavy stretch can't starve the 200-SMA of bars
DAYS_BACK = 420

CRYPTO_MAJORS = ["BTC", "ETH", "SOL"]


# ── per-ticker computation ─────────────────────────────────────────────────────

def compute_levels(bars: list[dict], cfg: dict) -> dict:
    """Indicator bundle + the three levels with annotations. Pure function."""
    mults = cfg.get("rung_atr_multipliers", [1.0, 2.0, 3.0])
    cap_pct = float(cfg.get("practicality_cap_pct", 25))
    swing_n = int(cfg.get("swing_low_sessions", 60))

    m = compute_all(bars)
    price, sma50, sma200, atr = m["price"], m["sma50"], m["sma200"], m["atr14"]
    slow = swing_low(bars, swing_n)

    out = {"price": price, "sma50": sma50, "sma200": sma200, "atr": atr,
           "rsi": m["rsi14"], "swing_low": slow, "bars": m["bars"],
           "levels": [], "notes": []}

    if price is None or sma50 is None or atr is None:
        out["notes"].append(f"insufficient history ({m['bars']} bars)")
        return out

    raw = [sma50 - float(mu) * atr for mu in mults[:3]]
    l3, trend_floor = raw[2], False
    if sma200 is not None and sma200 > raw[2]:
        l3, trend_floor = sma200, True
    elif sma200 is None:
        out["notes"].append("no 200SMA — L3 unfloored")

    for name, val in (("L1", raw[0]), ("L2", raw[1]), ("L3", l3)):
        dist_pct = (val / price - 1) * 100        # negative = below current price
        tags = []
        if val >= price:
            tags.append("ALREADY BELOW — buyable now")
        elif dist_pct < -cap_pct:
            tags.append("unlikely near-term")
        if name == "L3":
            if trend_floor:
                tags.append("trend-floor")
            if slow is not None and l3 < slow:
                tags.append("below recent support")
        out["levels"].append({"name": name, "value": val,
                              "dist_pct": dist_pct, "tags": tags})
    return out


def stance_for(row: dict, regime_bearish: bool, earn_days: int | None,
               gates: dict) -> tuple[str, str]:
    """Return (stance, reason). Order: no-data → blocked → buyable → wait."""
    if not row["levels"]:
        return "NO-DATA", "; ".join(row["notes"]) or "no bars"
    if regime_bearish:
        return "BLOCKED", "regime bearish — do not act"
    blackout = int(gates.get("earnings_blackout_days", 7))
    if earn_days is not None and 0 <= earn_days <= blackout:
        return "BLOCKED", f"earnings in {earn_days}d — do not act"

    price, sma200, rsi = row["price"], row["sma200"], row["rsi"]
    trend_ok = (sma200 is None or price > sma200
                or (rsi is not None and rsi < float(gates.get("trend_rsi_override", 30))))
    l1 = row["levels"][0]["value"]
    if price <= l1 and trend_ok:
        return "BUYABLE", "price at/below L1"
    if not trend_ok:
        return "WAIT", "downtrend — L1 touch alone not enough"
    return "WAIT", ""


# ── orchestration ──────────────────────────────────────────────────────────────

def run_levels(targets: dict, client, only_ticker: str | None = None) -> str:
    from allocate import build_roster   # late import to avoid a cycle

    cfg = targets.get("levels", {}) or {}
    gates = targets.get("gates", {}) or {}
    crypto_cfg = targets.get("crypto", {}) or {}
    cg_ids = crypto_cfg.get("coingecko_ids", {}) or {}

    roster = build_roster(targets)
    equities = sorted(roster)
    cryptos = [c.upper() for c in crypto_cfg.get("coins", [])]
    if only_ticker:
        t = only_ticker.upper()
        equities = [x for x in equities if x == t]
        cryptos = [x for x in cryptos if x == t]
        if not equities and not cryptos:
            return f"'{only_ticker}' not in roster or crypto sleeve."

    # Regime (QQQ daily closes)
    regime_known, regime_bearish = False, False
    try:
        qbars = client.get_bars(targets.get("regime_ticker", "QQQ"),
                                "1Day", DAILY_LIMIT, DAYS_BACK)
        if len(qbars) >= 2:
            regime_known = True
            regime_bearish = not regime_ok_from_closes([float(b["c"]) for b in qbars])
    except Exception:
        pass

    rows = []
    for tk in equities:
        try:
            bars = client.get_bars(tk, "1Day", DAILY_LIMIT, DAYS_BACK)
        except Exception as e:
            rows.append({"ticker": tk, "stance": "NO-DATA", "reason": str(e)[:60],
                         "levels": [], "price": None, "rsi": None, "notes": []})
            continue
        row = compute_levels(bars, cfg)
        earn = days_until_earnings(tk) if row["levels"] else None
        stance, reason = stance_for(row, regime_bearish, earn, gates)
        rows.append({"ticker": tk, "stance": stance, "reason": reason, **row})

    for coin in cryptos:
        if coin in cg_ids:
            bars, err = coingecko_daily_bars(cg_ids[coin])
            if err:
                rows.append({"ticker": coin, "stance": "NO-DATA",
                             "reason": f"skipped — {err}", "levels": [],
                             "price": None, "rsi": None, "notes": []})
                continue
        else:
            try:
                bars = client.get_crypto_bars(f"{coin}/USD", DAYS_BACK)
            except Exception as e:
                rows.append({"ticker": coin, "stance": "NO-DATA",
                             "reason": str(e)[:60], "levels": [],
                             "price": None, "rsi": None, "notes": []})
                continue
        row = compute_levels(bars, cfg)
        stance, reason = stance_for(row, regime_bearish, None, gates)  # no earnings for crypto
        rows.append({"ticker": coin, "stance": stance, "reason": reason, **row})

    return _render(rows, regime_known, regime_bearish, cfg)


# ── rendering ──────────────────────────────────────────────────────────────────

def _lvl_cell(price, lvl) -> str:
    tag = ""
    if any("ALREADY BELOW" in t for t in lvl["tags"]):
        tag = " ✓now"
    elif any("unlikely" in t for t in lvl["tags"]):
        tag = " ⚠far"
    return f"${lvl['value']:,.2f} ({lvl['dist_pct']:+.1f}%){tag}"


def _render(rows, regime_known, regime_bearish, cfg) -> str:
    order = {"BUYABLE": 0, "WAIT": 1, "BLOCKED": 2, "NO-DATA": 3}
    rows.sort(key=lambda r: (order.get(r["stance"], 9),
                             abs(r["levels"][0]["dist_pct"]) if r["levels"] else 1e9))

    regime_s = ("UNKNOWN" if not regime_known else
                "BELOW 200-EMA (risk-off — levels stamped do-not-act)"
                if regime_bearish else "ABOVE 200-EMA (risk-on)")
    L = [f"# Buy levels — {date.today().isoformat()}", "",
         f"**Regime (QQQ):** {regime_s}  |  rungs "
         f"{cfg.get('rung_atr_multipliers', [1.0,2.0,3.0])}×ATR off 50SMA, "
         f"L3 floored at 200SMA, practicality cap {cfg.get('practicality_cap_pct', 25)}%", "",
         "| Ticker | Stance | Price | RSI | L1 shallow | L2 standard | L3 deep | Notes |",
         "|--------|--------|------:|----:|-----------:|------------:|--------:|-------|"]

    for r in rows:
        if not r["levels"]:
            L.append(f"| {r['ticker']} | {r['stance']} | n/a | n/a | — | — | — | {r['reason']} |")
            continue
        price_s = f"${r['price']:,.2f}"
        rsi_s = f"{r['rsi']:.0f}" if r.get("rsi") is not None else "n/a"
        l1, l2, l3 = (_lvl_cell(r["price"], l) for l in r["levels"])
        notes = []
        if r["reason"]:
            notes.append(r["reason"])
        notes += [t for t in r["levels"][2]["tags"] if t in ("trend-floor", "below recent support")]
        notes += r.get("notes", [])
        L.append(f"| {r['ticker']} | **{r['stance']}** | {price_s} | {rsi_s} "
                 f"| {l1} | {l2} | {l3} | {'; '.join(notes)} |")

    n = {s: sum(1 for r in rows if r["stance"] == s) for s in order}
    L += ["", f"**{n['BUYABLE']} buyable, {n['WAIT']} waiting, "
              f"{n['BLOCKED']} blocked, {n['NO-DATA']} no-data.**", "",
          "_Advisory staging points for manual limit orders. This tool places no orders._"]
    return "\n".join(L)
