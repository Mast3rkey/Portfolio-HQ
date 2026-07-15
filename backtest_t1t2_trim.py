"""
backtest_t1t2_trim.py — one-time test: T1/T2 currently have NO trim rule at
all (only band/spec trim on overweight in plan()), found 2026-07-15 during
the T1 AI-infra cluster-cap scan (declined — correlation too weak, see
Decisions Log). T1 sits at 42.1% of book vs its 30.15% target live, with
nothing mechanical pulling it back. This is a different question from
trim_backtest.md: that test covered band/spec (RSI-gated, opportunistic
trims on names that ran hot). This one asks when a CORE CONVICTION position's
overweight should get capped despite conviction, and whether capping it
costs or saves return — including the leverage/forced-selling tension that
made trim_backtest.md's verdict go against its own raw TWR number.

Same window (2021-2026), same 63-ticker T1-spec universe (no crypto), same
weight scheme, same band/spec trim rule (1.25x/RSI>60), same trend gate
(200-SMA, RSI<30 override) held at current production values throughout —
only the T1/T2 trim variant changes between arms. Trim scope is restricted
to whichever tickers are actually T1/T2 today (24 of the 63).

Four arms:
  A — current production (control): no T1/T2 trim, positions run unbounded
      past target.
  B — mechanical fixed threshold: trim any T1/T2 name above 1.5x its own
      target, no RSI gate (risk-limit breach, same category as the
      cluster-cap trims — not a profit-take).
  C — same 1.5x threshold as B, but gated off while the name is in a
      confirmed downtrend (price below its own 200-day SMA) — avoids forced
      selling a conviction name into weakness.
  D — cluster-relative (CONDITIONAL: only run/reported if B and C diverge by
      more than ADOPT_THRESHOLD_PP — no point testing a third shape if the
      first two already agree). Trims T1's AI-infra names (ASML/TSM/NVDA/
      MSFT/GOOGL/META/GEV) only when that cluster's aggregate exceeds
      CLUSTER_CAP_PCT of book, largest-own-target-overweight-first — same
      mechanism as the semis/power_infra/oil caps.

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt B or C only if it beats A by more than ADOPT_THRESHOLD_PP
    (1.0 percentage point annualized TWR) AND does not increase MaxDD versus
    A by more than MAXDD_TOLERANCE_PP -- a trim rule that "wins" on TWR by
    letting a bigger drawdown through isn't a win, per the trim_backtest.md
    precedent (never-trim won on raw TWR there but was rejected on leverage/
    drawdown grounds).
  * If A beats both B and C by more than the threshold, no T1/T2 trim rule
    is adopted — current (no rule) stays.
  * Whether to run/report D is itself pre-committed: only if
    |TWR(C) - TWR(B)| > ADOPT_THRESHOLD_PP.
  * Anything inside the threshold = noise -> "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_t1t2_trim.py   (reuses data/backtest bar cache)
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from backtest_regime import (
    CACHE, DEPOSIT, MIN_LOT, MIN_HISTORY, MIN_TICKERS_TO_START, BAND_CAP, TRIM_RSI,
    TIER_WEIGHTS, universe, load_bars, rsi_series, twr_annualized, max_drawdown,
)
from backtest_trend import sma_series, SMA_PERIOD, TREND_RSI_OVERRIDE
import json

HERE = Path(__file__).resolve().parent
REPORT = HERE / "reports" / "t1t2_trim_backtest.md"

ADOPT_THRESHOLD_PP = 1.0
MAXDD_TOLERANCE_PP = 1.0     # a TWR "win" that worsens MaxDD by more than this doesn't count
T1T2_TRIM_MULT = 1.5         # mechanical trim threshold: 1.5x a T1/T2 name's own target
AI_INFRA = {"ASML", "TSM", "NVDA", "MSFT", "GOOGL", "META", "GEV"}
CLUSTER_CAP_PCT = 35.0       # Arm D only: AI-infra cluster ceiling as % of book

ARMS = {
    "A": "A — current (no T1/T2 trim, control)",
    "B": "B — mechanical 1.5x, no RSI gate",
    "C": "C — 1.5x, gated off below own 200-SMA (no forced sell into weakness)",
    "D": f"D — AI-infra cluster cap ({CLUSTER_CAP_PCT:.0f}% of book)",
}


def simulate(mode: str, tiers: dict[str, str], weights: dict[str, float],
             aligned: dict, calendar: list[str], deposit_days: list[str]) -> dict:
    """aligned[s] = (closes, rsi, sma200, first_elig_idx)."""
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    values: list[float] = []
    flows: dict[int, float] = {}
    n_bandspec_trims = n_t1t2_trims = 0
    t1t2_trimmed = 0.0

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

                # ---- band/spec trims: identical in every arm ---------------
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
                    n_bandspec_trims += 1

                # ---- T1/T2 trim: the arm's rule -----------------------------
                if mode == "fixed" or mode == "fixed_trend_gated":
                    for s in elig:
                        if tiers[s] not in ("T1", "T2"):
                            continue
                        val = shares.get(s, 0.0) * closes[s]
                        if val <= T1T2_TRIM_MULT * targets[s]:
                            continue
                        if mode == "fixed_trend_gated":
                            sma = aligned[s][2][i]
                            if sma is not None and closes[s] < sma:
                                continue    # confirmed downtrend: skip the trim
                        excess = val - T1T2_TRIM_MULT * targets[s]
                        if excess < MIN_LOT:
                            continue
                        shares[s] -= excess / closes[s]
                        cash += excess
                        n_t1t2_trims += 1
                        t1t2_trimmed += excess
                elif mode == "cluster":
                    cluster_names = [s for s in elig if s in AI_INFRA]
                    cluster_val = sum(shares.get(s, 0.0) * closes[s] for s in cluster_names)
                    cap_dollars = book * CLUSTER_CAP_PCT / 100.0
                    if cluster_val > cap_dollars:
                        excess_total = cluster_val - cap_dollars
                        # largest-own-target-overweight-first
                        ow = sorted(
                            ((shares.get(s, 0.0) * closes[s] - targets[s], s)
                             for s in cluster_names), reverse=True)
                        for over, s in ow:
                            if excess_total < MIN_LOT:
                                break
                            if over <= 0:
                                continue
                            trim = min(over, excess_total)
                            if trim < MIN_LOT:
                                continue
                            shares[s] -= trim / closes[s]
                            cash += trim
                            excess_total -= trim
                            n_t1t2_trims += 1
                            t1t2_trimmed += trim

                # ---- buys: largest gap first, trend-gated (production) -----
                gaps = sorted(((targets[s] - shares.get(s, 0.0) * closes[s], s)
                               for s in elig), reverse=True)
                for gap, s in gaps:
                    if gap < MIN_LOT or cash < MIN_LOT:
                        break
                    sma = aligned[s][2][i]
                    rsi = aligned[s][1][i]
                    if (sma is not None and closes[s] < sma
                            and (rsi is None or rsi >= TREND_RSI_OVERRIDE)):
                        continue      # trend gate: redirect to next-ranked gap
                    spend = min(gap, cash)
                    shares[s] = shares.get(s, 0.0) + spend / closes[s]
                    cash -= spend

        v = cash
        for s, sh in shares.items():
            px = aligned[s][0][i]
            if px is not None:
                v += sh * px
        values.append(v)

    last = len(calendar) - 1
    final_vals = {s: sh * aligned[s][0][last] for s, sh in shares.items()
                  if aligned[s][0][last] is not None}
    t1_final = sum(v for s, v in final_vals.items() if tiers.get(s) in ("T1", "T2"))
    t1_pct = (t1_final / values[-1] * 100.0) if values[-1] else 0.0

    return {"ann_twr": twr_annualized(values, flows), "final": values[-1],
            "max_dd": max_drawdown(values), "n_bandspec_trims": n_bandspec_trims,
            "n_t1t2_trims": n_t1t2_trims, "t1t2_trimmed": t1t2_trimmed,
            "t1t2_final_pct": t1_pct, "deposited": DEPOSIT * len(deposit_days)}


def setup():
    tiers = universe()
    data = load_bars(sorted(tiers))
    tiers = {t: v for t, v in tiers.items() if t in data}
    print(f"Universe: {len(data)} tickers "
          f"({sum(1 for v in tiers.values() if v in ('T1','T2'))} in T1/T2)")

    spy = json.loads((CACHE / "SPY.json").read_text())
    full_cal = [b["t"][:10] for b in spy]

    aligned: dict[str, tuple] = {}
    for s, bars in data.items():
        closes_raw = [float(b["c"]) for b in bars]
        rsi_raw = rsi_series(closes_raw)
        sma_raw = sma_series(closes_raw, SMA_PERIOD)
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
    print(f"Sim window: {calendar[0]} -> {calendar[-1]}  "
          f"({len(deposit_days)} monthly deposits of ${DEPOSIT:,.0f})")
    return tiers, aligned, calendar, deposit_days


def verdict(res: dict, run_d: bool) -> str:
    a = res["A"]["ann_twr"]
    dd_a = res["A"]["max_dd"]
    winners = []
    for k in ("B", "C") + (("D",) if run_d else ()):
        x = res[k]["ann_twr"]
        dd_x = res[k]["max_dd"]
        beats_twr = x - a > ADOPT_THRESHOLD_PP
        # MaxDD is negative; "worse" means more negative than A by more than tolerance
        worse_dd = (dd_a - dd_x) > MAXDD_TOLERANCE_PP
        if beats_twr and not worse_dd:
            winners.append(k)
    if winners:
        best = max(winners, key=lambda k: res[k]["ann_twr"])
        return (f"ADOPT {best} — beats current (A) by "
                f">{ADOPT_THRESHOLD_PP}pp annualized TWR without a MaxDD "
                f"regression beyond {MAXDD_TOLERANCE_PP}pp.")
    beat_but_worse_dd = [k for k in (("B", "C") + (("D",) if run_d else ()))
                         if res[k]["ann_twr"] - a > ADOPT_THRESHOLD_PP]
    if beat_but_worse_dd:
        return (f"NO CHANGE — {', '.join(beat_but_worse_dd)} beat A on raw TWR but "
                f"only by widening MaxDD beyond the {MAXDD_TOLERANCE_PP}pp tolerance; "
                f"same tension trim_backtest.md flagged for never-trim. Current "
                f"(no T1/T2 trim) stays; question closed.")
    return (f"NO CHANGE — all arms within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). No T1/T2 trim rule adopted; question closed.")


def main() -> int:
    tiers, aligned, calendar, deposit_days = setup()
    weights = {t: TIER_WEIGHTS[tiers[t]] for t in tiers}

    res = {
        "A": simulate("none", tiers, weights, aligned, calendar, deposit_days),
        "B": simulate("fixed", tiers, weights, aligned, calendar, deposit_days),
        "C": simulate("fixed_trend_gated", tiers, weights, aligned, calendar, deposit_days),
    }
    run_d = abs(res["C"]["ann_twr"] - res["B"]["ann_twr"]) > ADOPT_THRESHOLD_PP
    if run_d:
        res["D"] = simulate("cluster", tiers, weights, aligned, calendar, deposit_days)

    v = verdict(res, run_d)
    arm_keys = ["A", "B", "C"] + (["D"] if run_d else [])

    lines = [
        "# T1/T2 trim backtest — should core-conviction overweight ever get capped?",
        f"_{date.today().isoformat()} · window {calendar[0]} -> {calendar[-1]} · "
        f"{len(tiers)} tickers (T1-spec, no crypto; "
        f"{sum(1 for v in tiers.values() if v in ('T1','T2'))} in T1/T2) · "
        f"${DEPOSIT:,.0f}/mo x {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt B or C only if it beats A "
        f"by >{ADOPT_THRESHOLD_PP}pp annualized TWR **and** doesn't widen MaxDD beyond "
        f"{MAXDD_TOLERANCE_PP}pp versus A -- a TWR win bought with a materially deeper "
        f"drawdown doesn't count, per the trim_backtest.md precedent (never-trim won on "
        f"raw TWR there but was rejected on leverage/forced-selling grounds). Arm D "
        f"(AI-infra cluster cap) only runs if |C-B| > {ADOPT_THRESHOLD_PP}pp -- no point "
        f"testing a third shape if the first two already agree. Weight scheme, band/spec "
        f"trim rule (1.25x/RSI>60), and the trend gate (200-SMA, RSI<30 override) held at "
        f"current production values in every arm -- only the T1/T2 trim variant changes. "
        f"One test, one verdict.",
        "",
        f"Arm D {'ran' if run_d else 'did not run'}: |C-B| = "
        f"{abs(res['C']['ann_twr']-res['B']['ann_twr']):.2f}pp "
        f"({'>' if run_d else '<='} {ADOPT_THRESHOLD_PP}pp threshold).",
        "",
        "| Arm | Ann. TWR | Final value | MaxDD | T1/T2 trims | $ trimmed | T1/T2 final % of book |",
        "|-----|---------:|------------:|------:|------------:|----------:|-----------------------:|",
    ]
    for k in arm_keys:
        r = res[k]
        lines.append(f"| {ARMS[k]} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"{r['max_dd']:.1f}% | {r['n_t1t2_trims']} | ${r['t1t2_trimmed']:,.0f} | "
                     f"{r['t1t2_final_pct']:.1f}% |")

    a = res["A"]["ann_twr"]
    lines += ["",
              "Gaps vs current (A): " + " · ".join(
                  f"{k}-A: {res[k]['ann_twr'] - a:+.2f}pp" for k in arm_keys if k != "A"),
              "MaxDD vs current (A): " + " · ".join(
                  f"{k}-A: {res[k]['max_dd'] - res['A']['max_dd']:+.2f}pp"
                  for k in arm_keys if k != "A"),
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One window, one mostly-rising sample with a single real bear stretch "
              "(2022). A T1/T2 trim rule's real test is exactly that kind of drawdown -- "
              "trimming a core-conviction name mid-selloff is a materially different "
              "failure mode than trimming a speculative band/spec name that ran hot, "
              "which is why this is a new test and not a rerun of trim_backtest.md. "
              "MaxDD reported alongside TWR because that tension is the whole reason "
              "this backtest exists._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
