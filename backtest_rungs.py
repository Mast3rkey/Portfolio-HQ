"""
backtest_rungs.py — one-time test: do buy rungs deserve to exist?

Three arms, identical deposits, identical tickers, entry timing is the ONLY
difference:
  A — current production rungs (levels.compute_levels: 50SMA − {1,2,3}×ATR14,
      L3 floored at 200SMA)
  B — S/R rungs (pivot swing lows: 5-bar pivots over a 60-session lookback,
      the 3 nearest confirmed levels below price)
  C — baseline: market-buy the full deposit at the deposit-day close

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt B only if its annualized TWR beats BOTH A and C by more than
    ADOPT_THRESHOLD_PP (1.0 percentage point).
  * If C beats A by more than the same threshold, the finding is that the
    current rung module is cash drag → deposits should market-buy.
  * Anything inside the threshold = noise → "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_rungs.py            (fetches+caches bars on first run)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

from alpaca_client import AlpacaPaperClient
from levels import compute_levels
from backtest_regime import twr_annualized, max_drawdown

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "backtest"
REPORT = HERE / "reports" / "rung_backtest.md"

# ── pre-committed parameters (do not tune after results) ────────────────────────
ADOPT_THRESHOLD_PP = 1.0      # B must win by > this (annualized TWR, pct points)
DEPOSIT = 2000.0              # first trading day of each month
PIVOT_K = 5                   # bar on each side to confirm a swing low
SR_LOOKBACK = 60              # sessions searched for pivots (matches levels cfg)
N_RUNGS = 3                   # rungs per ticker per cycle (matches production)
MIN_HISTORY = 210             # sessions before a ticker joins the sim
MIN_TICKERS_TO_START = 20     # sim starts the first month this many are eligible
EXCLUDE = {"SPCX", "SKHY"}    # no/insufficient data (documented previously)
FETCH_LIMIT, FETCH_DAYS = 3000, 2400


# ── data ─────────────────────────────────────────────────────────────────────────

def roster_tickers() -> list[str]:
    t = yaml.safe_load(open(HERE / "targets.yaml"))
    out = []
    for tier in t["tiers"].values():
        out += [s.upper() for s in tier.get("tickers", [])]
    return sorted(set(out) - EXCLUDE)


def load_bars(tickers: list[str]) -> dict[str, list[dict]]:
    CACHE.mkdir(parents=True, exist_ok=True)
    client = None
    out = {}
    for sym in tickers:
        f = CACHE / f"{sym.replace('/', '_')}.json"
        if f.exists():
            out[sym] = json.loads(f.read_text())
            continue
        client = client or AlpacaPaperClient()
        try:
            bars = client.get_bars(sym, "1Day", FETCH_LIMIT, FETCH_DAYS,
                                   adjustment="split")
        except RuntimeError as e:
            print(f"  ! {sym}: fetch failed ({str(e)[:80]}) — excluded")
            continue
        if len(bars) < MIN_HISTORY:
            print(f"  ! {sym}: only {len(bars)} bars — excluded")
            continue
        f.write_text(json.dumps(bars))
        out[sym] = bars
        print(f"  + {sym}: {len(bars)} bars cached")
    return out


# ── pure rung functions (unit-tested) ────────────────────────────────────────────

def rungs_current(bars_upto: list[dict], cfg: dict) -> list[float]:
    """Arm A: the PRODUCTION rung math via levels.compute_levels. Only rungs
    strictly below the current close are stageable."""
    lv = compute_levels(bars_upto, cfg)
    price = lv.get("price")
    out = []
    for r in lv.get("levels", []):
        val = r.get("value")
        if val is not None and price is not None and val < price:
            out.append(float(val))
    return out[:N_RUNGS]


def pivot_lows(lows: list[float], k: int = PIVOT_K) -> list[int]:
    """Indices i where lows[i] is the minimum of lows[i-k .. i+k] (confirmed
    pivots only — needs k bars after, so no lookahead when sliced correctly)."""
    idx = []
    for i in range(k, len(lows) - k):
        w = lows[i - k:i + k + 1]
        if lows[i] == min(w):
            idx.append(i)
    return idx


def rungs_sr(bars_upto: list[dict]) -> list[float]:
    """Arm B: the 3 nearest confirmed pivot-low levels below the current close,
    searched over the last SR_LOOKBACK sessions."""
    if len(bars_upto) < PIVOT_K * 2 + 2:
        return []
    window = bars_upto[-(SR_LOOKBACK + PIVOT_K):]
    lows = [float(b["l"]) for b in window]
    price = float(bars_upto[-1]["c"])
    levels = sorted({round(lows[i], 2) for i in pivot_lows(lows)
                     if lows[i] < price}, reverse=True)
    return levels[:N_RUNGS]


def fill_price(level: float, bar_open: float, bar_low: float) -> float | None:
    """A resting limit fills if the session trades at/below it; gap-down opens
    fill at the open, not the limit."""
    if bar_low <= level:
        return min(level, bar_open)
    return None


# twr_annualized, max_drawdown imported from backtest_regime.py above
# (2026-07-15 dedup) -- verified byte-identical logic (only a docstring
# differed) before removing the local copies here. load_bars stays local:
# this file's version fetches+caches live from Alpaca on a cache miss,
# genuinely different behavior from backtest_regime.py's cache-read-only
# version -- not a duplicate.


# ── simulation ────────────────────────────────────────────────────────────────────

def simulate(arm: str, data: dict, calendar: list[str], deposit_days: list[str],
             levels_cfg: dict) -> dict:
    """One arm over the full window. Orders placed at a deposit-day close are
    active the NEXT session; unfilled orders expire at the next deposit day and
    market-buy at that day's close (cash drag is real, deployment is eventual)."""
    day_idx = {d: i for i, d in enumerate(calendar)}
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    pending: list[dict] = []          # {sym, level, dollars, placed, expiry}
    values: list[float] = []
    flows: dict[int, float] = {}
    staged = filled = 0.0
    discounts: list[float] = []

    # per-ticker date→bar index
    tix = {s: {b["t"][:10]: j for j, b in enumerate(bars)} for s, bars in data.items()}

    next_dep = {d: (deposit_days[k + 1] if k + 1 < len(deposit_days) else calendar[-1])
                for k, d in enumerate(deposit_days)}

    for d in calendar:
        i = day_idx[d]
        # 1) fills on resting orders (active strictly after placement day)
        still = []
        for o in pending:
            j = tix[o["sym"]].get(d)
            done = False
            if j is not None and d > o["placed"]:
                bar = data[o["sym"]][j]
                fp = fill_price(o["level"], float(bar["o"]), float(bar["l"]))
                if fp:
                    shares[o["sym"]] = shares.get(o["sym"], 0) + o["dollars"] / fp
                    cash -= o["dollars"]
                    filled += o["dollars"]
                    ref = o["ref_close"]
                    discounts.append((ref - fp) / ref * 100.0)
                    done = True
            if not done and d >= o["expiry"]:
                j = tix[o["sym"]].get(d)
                px = float(data[o["sym"]][j]["c"]) if j is not None else None
                if px:
                    shares[o["sym"]] = shares.get(o["sym"], 0) + o["dollars"] / px
                    cash -= o["dollars"]
                    done = True
            if not done:
                still.append(o)
        pending = still

        # 2) deposit day: add flow, stage this cycle's buys
        if d in dep_set:
            flows[i] = DEPOSIT
            cash += DEPOSIT
            elig = [s for s in data
                    if s in tix and d in tix[s] and tix[s][d] + 1 >= MIN_HISTORY]
            if elig:
                per = DEPOSIT / len(elig)
                for s in elig:
                    j = tix[s][d]
                    close = float(data[s][j]["c"])
                    if arm == "C":
                        shares[s] = shares.get(s, 0) + per / close
                        cash -= per
                        continue
                    upto = data[s][:j + 1]
                    rungs = (rungs_current(upto, levels_cfg) if arm == "A"
                             else rungs_sr(upto))
                    if not rungs:                      # nothing stageable → buy now
                        shares[s] = shares.get(s, 0) + per / close
                        cash -= per
                        continue
                    slice_ = per / len(rungs)
                    for lv in rungs:
                        staged += slice_
                        pending.append({"sym": s, "level": lv, "dollars": slice_,
                                        "placed": d, "expiry": next_dep[d],
                                        "ref_close": close})

        # 3) mark portfolio
        v = cash
        for s, sh in shares.items():
            j = tix[s].get(d)
            if j is None:                              # holiday for this ticker
                j = max(k for dt, k in tix[s].items() if dt <= d)
            v += sh * float(data[s][j]["c"])
        values.append(v)

    return {"ann_twr": twr_annualized(values, flows),
            "final": values[-1], "max_dd": max_drawdown(values),
            "fill_rate": (filled / staged * 100.0) if staged else None,
            "avg_discount": (sum(discounts) / len(discounts)) if discounts else None,
            "deposited": DEPOSIT * len(deposit_days)}


# ── verdict + report ─────────────────────────────────────────────────────────────

def verdict(res: dict) -> str:
    a, b, c = res["A"]["ann_twr"], res["B"]["ann_twr"], res["C"]["ann_twr"]
    if b - max(a, c) > ADOPT_THRESHOLD_PP:
        return ("ADOPT B — S/R rungs beat both current rungs and market-buy by "
                f">{ADOPT_THRESHOLD_PP}pp annualized.")
    if c - a > ADOPT_THRESHOLD_PP:
        return ("KILL RUNGS — market-buy beats the current rung module by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. The module is cash drag; "
                "deposits should market-buy. S/R adoption moot.")
    return ("NO CHANGE — all arms within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). Keep it simple; question closed.")


def main() -> int:
    cfg = yaml.safe_load(open(HERE / "targets.yaml")).get("levels", {})
    tickers = roster_tickers()
    print(f"Universe: {len(tickers)} roster tickers (excl. {sorted(EXCLUDE)})")
    data = load_bars(tickers)
    print(f"Loaded {len(data)} tickers with data")

    # master calendar from SPY; deposit = first trading day of month once
    # enough tickers are eligible
    spy = data["SPY"]
    calendar = [b["t"][:10] for b in spy]
    dep_all = []
    seen = set()
    for d in calendar:
        if d[:7] not in seen:
            seen.add(d[:7])
            dep_all.append(d)
    tix = {s: {b["t"][:10] for b in bars[MIN_HISTORY:]} for s, bars in data.items()}
    deposit_days = [d for d in dep_all
                    if sum(1 for s in tix if d in tix[s]) >= MIN_TICKERS_TO_START]
    calendar = [d for d in calendar if d >= deposit_days[0]]
    print(f"Sim window: {calendar[0]} → {calendar[-1]}  "
          f"({len(deposit_days)} monthly deposits of ${DEPOSIT:,.0f})")

    res = {arm: simulate(arm, data, calendar, deposit_days, cfg)
           for arm in ("A", "B", "C")}
    v = verdict(res)

    lines = [
        "# Rung backtest — do buy rungs deserve to exist?",
        f"_{date.today().isoformat()} · window {calendar[0]} → {calendar[-1]} · "
        f"{len(data)} tickers · ${DEPOSIT:,.0f}/mo × {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt B only if it beats "
        f"both A and C by >{ADOPT_THRESHOLD_PP}pp annualized TWR; C beating A by the "
        f"same margin kills the rung module; inside the threshold = no change. "
        f"One test, one verdict.",
        "",
        "| Arm | Ann. TWR | Final value | Deposited | MaxDD | Fill rate | Avg fill discount |",
        "|-----|---------:|------------:|----------:|------:|----------:|------------------:|",
    ]
    names = {"A": "A — current rungs", "B": "B — S/R rungs", "C": "C — market-buy"}
    for k in ("A", "B", "C"):
        r = res[k]
        fr = f"{r['fill_rate']:.0f}%" if r["fill_rate"] is not None else "—"
        di = f"{r['avg_discount']:+.2f}%" if r["avg_discount"] is not None else "—"
        lines.append(f"| {names[k]} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"${r['deposited']:,.0f} | {r['max_dd']:.1f}% | {fr} | {di} |")
    ca = res["C"]["ann_twr"] - res["A"]["ann_twr"]
    ba = res["B"]["ann_twr"] - res["A"]["ann_twr"]
    bc = res["B"]["ann_twr"] - res["C"]["ann_twr"]
    lines += ["",
              f"**C − A gap (does rung-waiting cost money?): {ca:+.2f}pp annualized**",
              f"B − A: {ba:+.2f}pp · B − C: {bc:+.2f}pp",
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One 6-year, mostly-rising window = one sample. The threshold exists "
              "because a small edge in one sample is noise, not signal._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
