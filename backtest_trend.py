"""
backtest_trend.py — one-time test: does the per-ticker 200-SMA trend gate
(block adds on a name trading below its 200-day SMA, unless RSI(14) < 30)
earn its keep, or is it the last untested timing gate costing money?

This is the regime gate's sibling — same trend-following idea, different cost
mechanism. The regime gate held whole deposits as CASH (pure drag, dropped
2026-07-14 after losing by 2.56pp). The trend gate only REDIRECTS money: a
blocked name's dollars flow to the next-ranked gap, still fully invested. So
the expected effect is smaller — this test exists to close the question, not
because a large edge is suspected either way.

Two arms, identical deposits, identical universe, identical weight scheme and
trim rule (current production, validated separately, held constant). No regime
gate in either arm (dropped from production before this test):
  A — current production: adds blocked while a name is below its 200-SMA,
      unless RSI(14) < 30 (the oversold override); money redirects down the
      gap ranking
  B — no trend gate: buy purely by largest-dollar-gap order

Crypto excluded (no timing gates apply to it). Earnings blackout not modeled
in either arm (historical earnings dates unavailable — untestable, held out
of both arms equally). Cluster caps excluded (new, not historically
meaningful — same scope rule as every prior backtest).

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt B (drop the trend gate) only if it beats A by more than
    ADOPT_THRESHOLD_PP (1.0 percentage point annualized TWR).
  * If A beats B by more than the threshold, the trend gate earns its keep.
  * Anything inside the threshold = noise → "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_trend.py   (reuses data/backtest bar cache)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from backtest_regime import (
    CACHE, DEPOSIT, MIN_LOT, MIN_HISTORY, MIN_TICKERS_TO_START, RSI_PERIOD,
    BAND_CAP, TRIM_RSI, TIER_WEIGHTS, universe, load_bars, rsi_series,
    twr_annualized, max_drawdown,
)

HERE = Path(__file__).resolve().parent
REPORT = HERE / "reports" / "trend_backtest.md"

ADOPT_THRESHOLD_PP = 1.0
SMA_PERIOD = 200            # production trend gate: price vs 200-day SMA
TREND_RSI_OVERRIDE = 30.0   # production: allow add below 200-SMA only if RSI < this


def sma_series(closes: list[float], period: int = SMA_PERIOD) -> list[float | None]:
    out: list[float | None] = [None] * len(closes)
    run = 0.0
    for i, c in enumerate(closes):
        run += c
        if i >= period:
            run -= closes[i - period]
        if i + 1 >= period:
            out[i] = run / period
    return out


def simulate(gate_on: bool, tiers: dict[str, str], weights: dict[str, float],
             aligned: dict, calendar: list[str], deposit_days: list[str]) -> dict:
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    values: list[float] = []
    flows: dict[int, float] = {}
    n_trims = n_blocked = 0

    for i, d in enumerate(calendar):
        if d in dep_set:
            flows[i] = DEPOSIT
            cash += DEPOSIT

            elig = [s for s in aligned if aligned[s][3] is not None and i >= aligned[s][3]]
            if elig:
                closes = {s: aligned[s][0][i] for s in elig}
                book = cash + sum(shares.get(s, 0.0) * closes[s] for s in elig)
                w_sum = sum(weights[s] for s in elig)
                targets = {s: book * weights[s] / w_sum for s in elig}

                # trims run identically in both arms (the gate only affects adds)
                for s in elig:
                    if tiers[s] not in ("band", "spec"):
                        continue
                    val = shares.get(s, 0.0) * closes[s]
                    cap = BAND_CAP if tiers[s] == "band" else 1.0
                    if val <= cap * targets[s]:
                        continue
                    r = aligned[s][1][i]
                    if r is None or r <= TRIM_RSI:
                        continue
                    excess = val - targets[s]
                    if excess < MIN_LOT:
                        continue
                    shares[s] -= excess / closes[s]
                    cash += excess
                    n_trims += 1

                gaps = sorted(((targets[s] - shares.get(s, 0.0) * closes[s], s)
                               for s in elig), reverse=True)
                for gap, s in gaps:
                    if gap < MIN_LOT:
                        break
                    if cash < MIN_LOT:
                        break
                    if gate_on:
                        sma = aligned[s][2][i]
                        rsi = aligned[s][1][i]
                        if (sma is not None and closes[s] < sma
                                and (rsi is None or rsi >= TREND_RSI_OVERRIDE)):
                            n_blocked += 1
                            continue        # redirect: next-ranked gap gets the money
                    spend = min(gap, cash)
                    shares[s] = shares.get(s, 0.0) + spend / closes[s]
                    cash -= spend

        v = cash
        for s, sh in shares.items():
            px = aligned[s][0][i]
            if px is not None:
                v += sh * px
        values.append(v)

    return {"ann_twr": twr_annualized(values, flows), "final": values[-1],
            "max_dd": max_drawdown(values), "n_trims": n_trims,
            "n_blocked": n_blocked, "deposited": DEPOSIT * len(deposit_days)}


def setup():
    tiers = universe()
    data = load_bars(sorted(tiers))
    tiers = {t: v for t, v in tiers.items() if t in data}
    print(f"Universe: {len(data)} tickers")

    spy = json.loads((CACHE / "SPY.json").read_text())
    full_cal = [b["t"][:10] for b in spy]

    # aligned[s] = (closes, rsi, sma200, first_eligible_index)
    aligned: dict[str, tuple] = {}
    for s, bars in data.items():
        closes_raw = [float(b["c"]) for b in bars]
        rsi_raw = rsi_series(closes_raw)
        sma_raw = sma_series(closes_raw)
        dix = {b["t"][:10]: j for j, b in enumerate(bars)}
        closes_al, rsi_al, sma_al = [], [], []
        first_elig, last_j = None, None
        for i, dt in enumerate(full_cal):
            j = dix.get(dt, last_j)
            last_j = j
            closes_al.append(closes_raw[j] if j is not None else None)
            rsi_al.append(rsi_raw[j] if j is not None else None)
            sma_al.append(sma_raw[j] if j is not None else None)
            if first_elig is None and j is not None and j + 1 >= MIN_HISTORY:
                first_elig = i
        aligned[s] = (closes_al, rsi_al, sma_al, first_elig)

    dep_all, seen = [], set()
    for i, dt in enumerate(full_cal):
        if dt[:7] not in seen:
            seen.add(dt[:7])
            dep_all.append((i, dt))
    deposit_days = [dt for i, dt in dep_all
                    if sum(1 for s in aligned
                           if aligned[s][3] is not None and i >= aligned[s][3])
                    >= MIN_TICKERS_TO_START]
    start = deposit_days[0]
    calendar = [dt for dt in full_cal if dt >= start]
    off = full_cal.index(start)
    aligned = {s: (c[off:], r[off:], m[off:],
                   (e - off if e is not None and e >= off else
                    (0 if e is not None else None)))
               for s, (c, r, m, e) in aligned.items()}
    print(f"Sim window: {calendar[0]} → {calendar[-1]}  "
          f"({len(deposit_days)} monthly deposits of ${DEPOSIT:,.0f})")
    return tiers, aligned, calendar, deposit_days


def verdict(res: dict) -> str:
    a, b = res["A"]["ann_twr"], res["B"]["ann_twr"]
    if b - a > ADOPT_THRESHOLD_PP:
        return (f"DROP THE TREND GATE — no-gate (B) beats current (A) by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. Redirecting away from "
                f"downtrending names cost money.")
    if a - b > ADOPT_THRESHOLD_PP:
        return (f"KEEP THE TREND GATE — current (A) beats no-gate (B) by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. The trend gate earns its keep.")
    return (f"NO CHANGE — within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). Trend gate stays; question closed.")


def main() -> int:
    tiers, aligned, calendar, deposit_days = setup()
    weights = {t: TIER_WEIGHTS[tiers[t]] for t in tiers}
    res = {
        "A": simulate(True, tiers, weights, aligned, calendar, deposit_days),
        "B": simulate(False, tiers, weights, aligned, calendar, deposit_days),
    }
    v = verdict(res)

    names = {"A": "A — current (trend gate ON, RSI<30 override)",
             "B": "B — no trend gate"}
    lines = [
        "# Trend-gate backtest — does the per-ticker 200-SMA gate earn its keep?",
        f"_{date.today().isoformat()} · window {calendar[0]} → {calendar[-1]} · "
        f"{len(tiers)} tickers (T1-spec, no crypto) · ${DEPOSIT:,.0f}/mo × {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt B (drop the gate) only "
        f"if it beats A by >{ADOPT_THRESHOLD_PP}pp annualized TWR; A beating B by the "
        f"same margin means the gate earns its keep; inside the threshold = no change. "
        f"Weight scheme and trim rule held at current production values; no regime gate "
        f"in either arm (dropped from production 2026-07-14, before this test). "
        f"One test, one verdict.",
        "",
        "Unlike the regime gate (held deposits as cash — pure drag), a trend-gate "
        "block only *redirects* money to the next-ranked gap, still fully invested — "
        "so the two arms differ only in *which* names got bought on blocked days.",
        "",
        "| Arm | Ann. TWR | Final value | MaxDD | Trims | Buy attempts blocked |",
        "|-----|---------:|------------:|------:|------:|---------------------:|",
    ]
    for k in ("A", "B"):
        r = res[k]
        lines.append(f"| {names[k]} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"{r['max_dd']:.1f}% | {r['n_trims']} | {r['n_blocked']} |")
    lines += ["",
              f"B − A gap: {res['B']['ann_twr'] - res['A']['ann_twr']:+.2f}pp annualized",
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One window, one mostly-rising sample with a single real bear stretch "
              "(2022) — the trend gate's actual test case. The threshold exists because "
              "a small edge here is noise, not signal._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
