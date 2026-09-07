"""
backtest_weights.py — one-time test: does the current tier-weight STRUCTURE
(steep T1 3.35% > T2 1.65% > ETF 2.30% > band 0.75% > spec 1.00% gradation)
beat simple alternatives, or is it arbitrary?

Four arms, identical deposits, identical universe, identical trim rule (band
1.25x / spec fixed / RSI>60 — already validated separately, held constant so
this test isolates ONLY the weighting question):
  A — current production weights
  B — equal-weight (every ticker gets the same target %, no tier distinction)
  C — flatter gradation (compressed spread across tiers)
  D — steeper gradation (amplified spread — more concentrated toward T1)

Crypto excluded (no timing gates apply to it, would confound the trim-rule
comparison). Cluster caps (semis/power_infra/oil) excluded — new, not
historically meaningful, and this test is about tier structure, not
concentration risk (see the trim/correlation backtests for those questions).

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt an alternative (B/C/D) only if it beats BOTH current (A) and every
    other alternative by more than ADOPT_THRESHOLD_PP (1.0 percentage point
    annualized TWR).
  * Anything inside the threshold = noise → "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_weights.py   (reuses data/backtest bar cache)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from backtest_regime import (
    universe, load_bars, rsi_series, twr_annualized, max_drawdown,
)

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "backtest"
REPORT = HERE / "reports" / "weight_backtest.md"

ADOPT_THRESHOLD_PP = 1.0
DEPOSIT = 2000.0
MIN_LOT = 25.0
MIN_HISTORY = 210
MIN_TICKERS_TO_START = 20
EXCLUDE = {"SPCX", "SKHY"}
BAND_CAP, TRIM_RSI = 1.25, 60.0   # held constant across arms — already validated

# universe, load_bars, rsi_series, twr_annualized, max_drawdown are imported
# from backtest_regime.py above (2026-07-15 dedup) -- verified byte-identical
# logic (only docstrings differed) before removing the local copies here.


def weight_schemes(tiers: dict[str, str]) -> dict[str, dict[str, float]]:
    n = len(tiers)
    equal_w = 100.0 / n
    schemes = {
        "A": {"T1": 3.35, "T2": 1.65, "ETF": 2.30, "band": 0.75, "spec": 1.00},
        "B": {t: equal_w for t in ("T1", "T2", "ETF", "band", "spec")},
        "C": {"T1": 2.00, "T2": 1.50, "ETF": 2.00, "band": 1.00, "spec": 1.00},
        "D": {"T1": 5.00, "T2": 1.20, "ETF": 2.30, "band": 0.40, "spec": 0.60},
    }
    return {arm: {t: tier_w[tiers[t]] for t in tiers} for arm, tier_w in schemes.items()}


# ── simulation ────────────────────────────────────────────────────────────────────

def simulate(weights: dict[str, float], tiers: dict[str, str], aligned: dict,
             calendar: list[str], deposit_days: list[str]) -> dict:
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    values: list[float] = []
    flows: dict[int, float] = {}
    n_trims = 0

    for i, d in enumerate(calendar):
        if d in dep_set:
            flows[i] = DEPOSIT
            cash += DEPOSIT
            elig = [s for s in aligned if aligned[s][2] is not None and i >= aligned[s][2]]
            if elig:
                closes = {s: aligned[s][0][i] for s in elig}
                book = cash + sum(shares.get(s, 0.0) * closes[s] for s in elig)
                w_sum = sum(weights[s] for s in elig)
                targets = {s: book * weights[s] / w_sum for s in elig}

                # ---- trims: band 1.25x / spec fixed, RSI>60 (constant rule) ----
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

                # ---- buys: largest gap first ----
                gaps = sorted(((targets[s] - shares.get(s, 0.0) * closes[s], s)
                               for s in elig), reverse=True)
                for gap, s in gaps:
                    if gap < MIN_LOT or cash < MIN_LOT:
                        break
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
            "deposited": DEPOSIT * len(deposit_days)}


# ── setup + report ───────────────────────────────────────────────────────────────

def setup():
    tiers = universe()
    data = load_bars(sorted(tiers))
    tiers = {t: v for t, v in tiers.items() if t in data}
    print(f"Universe: {len(data)} tickers (excl. {sorted(EXCLUDE)})")

    spy = json.loads((CACHE / "SPY.json").read_text())
    full_cal = [b["t"][:10] for b in spy]

    aligned: dict[str, tuple] = {}
    for s, bars in data.items():
        closes_raw = [float(b["c"]) for b in bars]
        rsi_raw = rsi_series(closes_raw)
        dix = {b["t"][:10]: j for j, b in enumerate(bars)}
        closes_al, rsi_al = [], []
        first_elig, last_j = None, None
        for i, dt in enumerate(full_cal):
            j = dix.get(dt, last_j)
            last_j = j
            closes_al.append(closes_raw[j] if j is not None else None)
            rsi_al.append(rsi_raw[j] if j is not None else None)
            if first_elig is None and j is not None and j + 1 >= MIN_HISTORY:
                first_elig = i
        aligned[s] = (closes_al, rsi_al, first_elig)

    dep_all, seen = [], set()
    for i, dt in enumerate(full_cal):
        if dt[:7] not in seen:
            seen.add(dt[:7])
            dep_all.append((i, dt))
    deposit_days = [dt for i, dt in dep_all
                    if sum(1 for s in aligned
                           if aligned[s][2] is not None and i >= aligned[s][2])
                    >= MIN_TICKERS_TO_START]
    start = deposit_days[0]
    calendar = [dt for dt in full_cal if dt >= start]
    off = full_cal.index(start)
    aligned = {s: (c[off:], r[off:], (e - off if e is not None and e >= off else
                                      (0 if e is not None else None)))
               for s, (c, r, e) in aligned.items()}
    print(f"Sim window: {calendar[0]} → {calendar[-1]}  "
          f"({len(deposit_days)} monthly deposits of ${DEPOSIT:,.0f})")
    return tiers, aligned, calendar, deposit_days


def verdict(res: dict) -> str:
    a = res["A"]["ann_twr"]
    best_alt, best_val = None, a
    for k in ("B", "C", "D"):
        if res[k]["ann_twr"] > best_val:
            best_alt, best_val = k, res[k]["ann_twr"]
    if best_alt is None:
        return (f"NO CHANGE — current weighting (A) already has the best annualized "
                f"TWR among all arms tested.")
    beats_all = all(res[best_alt]["ann_twr"] - res[k]["ann_twr"] > ADOPT_THRESHOLD_PP
                    for k in ("A", "B", "C", "D") if k != best_alt)
    if beats_all:
        return (f"ADOPT {best_alt} — beats current and every other arm by "
                f">{ADOPT_THRESHOLD_PP}pp annualized.")
    return (f"NO CHANGE — all arms within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). Current weighting stays; question closed.")


def main() -> int:
    tiers, aligned, calendar, deposit_days = setup()
    schemes = weight_schemes(tiers)
    res = {arm: simulate(w, tiers, aligned, calendar, deposit_days)
           for arm, w in schemes.items()}
    v = verdict(res)

    names = {
        "A": "A — current (T1 3.35 / T2 1.65 / ETF 2.30 / band 0.75 / spec 1.00)",
        "B": "B — equal-weight (all tickers identical)",
        "C": "C — flatter gradation (T1 2.00 / T2 1.50 / ETF 2.00 / band 1.00 / spec 1.00)",
        "D": "D — steeper gradation (T1 5.00 / T2 1.20 / ETF 2.30 / band 0.40 / spec 0.60)",
    }
    lines = [
        "# Weight backtest — is the current tier-weight structure arbitrary?",
        f"_{date.today().isoformat()} · window {calendar[0]} → {calendar[-1]} · "
        f"{len(tiers)} tickers (T1-spec, no crypto) · ${DEPOSIT:,.0f}/mo × {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt an alternative only if "
        f"it beats current AND every other arm by >{ADOPT_THRESHOLD_PP}pp annualized "
        f"TWR. Band 1.25x / spec fixed / RSI-60 trim rule held constant across all "
        f"arms — only the tier-weight scheme varies. One test, one verdict.",
        "",
        "| Arm | Ann. TWR | Final value | MaxDD | Trims |",
        "|-----|---------:|------------:|------:|------:|",
    ]
    for k in ("A", "B", "C", "D"):
        r = res[k]
        lines.append(f"| {names[k]} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"{r['max_dd']:.1f}% | {r['n_trims']} |")
    a = res["A"]["ann_twr"]
    lines += ["",
              "Gaps vs current (A): " + " · ".join(
                  f"{k}−A: {res[k]['ann_twr'] - a:+.2f}pp" for k in ("B", "C", "D")),
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One window, one mostly-rising sample. The threshold exists because a "
              "small edge in one sample is noise, not signal. Tier weight is also "
              "conviction sizing, not just a return-maximization input — even a "
              "winning alternative here wouldn't automatically override what specific "
              "names you believe in._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
