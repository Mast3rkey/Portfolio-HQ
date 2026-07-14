"""
backtest_regime.py — one-time test: does the QQQ 200-EMA regime gate (block
all new buys when QQQ is below its 200-day EMA, hold cash instead) actually
help, or is it untested infrastructure that's been treated as settled?

Two arms, identical deposits, identical universe, identical weight scheme
(current production) and trim rule (band 1.25x / spec fixed / RSI>60 —
already validated separately, held constant):
  A — current production: deposits held as cash on a bearish regime day,
      deployed on the next regime-OK cycle (cash persists, isn't lost)
  B — no regime gate: every deposit invests immediately regardless of QQQ's
      200-EMA status

Crypto excluded (no timing gates apply to it, would confound the comparison).
Cluster caps excluded (new, not historically meaningful — see the weight/trim
backtests for why those are out of scope here too).

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt B (drop the regime gate) only if it beats A by more than
    ADOPT_THRESHOLD_PP (1.0 percentage point annualized TWR).
  * If A beats B by more than the threshold, the regime gate earns its keep.
  * Anything inside the threshold = noise → "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_regime.py   (reuses data/backtest bar cache)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

from regime_gate import regime_ok_from_closes

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "backtest"
REPORT = HERE / "reports" / "regime_backtest.md"

ADOPT_THRESHOLD_PP = 1.0
DEPOSIT = 2000.0
MIN_LOT = 25.0
MIN_HISTORY = 210
MIN_TICKERS_TO_START = 20
EXCLUDE = {"SPCX", "SKHY"}
RSI_PERIOD = 14
BAND_CAP, TRIM_RSI = 1.25, 60.0
REGIME_TICKER = "QQQ"

# current production weight scheme (validated separately, held constant)
TIER_WEIGHTS = {"T1": 3.35, "T2": 1.65, "ETF": 2.30, "band": 0.75, "spec": 1.00}


def universe() -> dict[str, str]:
    t = yaml.safe_load(open(HERE / "targets.yaml"))
    tiers = {}
    for tname, tier in t["tiers"].items():
        for s in tier["tickers"]:
            s = s.upper()
            if s in EXCLUDE:
                continue
            tiers[s] = tname
    return tiers


def load_bars(tickers: list[str]) -> dict[str, list[dict]]:
    out = {}
    for sym in tickers:
        f = CACHE / f"{sym}.json"
        if not f.exists():
            print(f"  ! {sym}: no cached bars — excluded")
            continue
        bars = json.loads(f.read_text())
        if len(bars) < MIN_HISTORY:
            print(f"  ! {sym}: only {len(bars)} bars — excluded")
            continue
        out[sym] = bars
    return out


def rsi_series(closes: list[float], period: int = RSI_PERIOD) -> list[float | None]:
    n = len(closes)
    out: list[float | None] = [None] * n
    if n < 2:
        return out
    ag = al = 0.0
    for i in range(1, n):
        d = closes[i] - closes[i - 1]
        gain, loss = max(d, 0.0), max(-d, 0.0)
        if i == 1:
            ag, al = gain, loss
        else:
            ag = ag + (gain - ag) / period
            al = al + (loss - al) / period
        if i >= period:
            out[i] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    return out


def twr_annualized(daily_values: list[float], flows: dict[int, float]) -> float:
    rets = []
    for i in range(1, len(daily_values)):
        prev = daily_values[i - 1]
        if prev <= 0:
            continue
        f = flows.get(i, 0.0)
        rets.append((daily_values[i] - f) / prev - 1.0)
    if not rets:
        return 0.0
    growth = 1.0
    for r in rets:
        growth *= 1.0 + r
    return (growth ** (252.0 / len(rets)) - 1.0) * 100.0


def max_drawdown(vals: list[float]) -> float:
    peak, mdd = 0.0, 0.0
    for v in vals:
        peak = max(peak, v)
        if peak > 0:
            mdd = min(mdd, v / peak - 1.0)
    return mdd * 100.0


def simulate(gate_on: bool, tiers: dict[str, str], weights: dict[str, float],
             aligned: dict, regime_closes: list[float | None],
             calendar: list[str], deposit_days: list[str]) -> dict:
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    values: list[float] = []
    flows: dict[int, float] = {}
    n_trims = n_held_back = 0

    for i, d in enumerate(calendar):
        if d in dep_set:
            flows[i] = DEPOSIT
            cash += DEPOSIT

            bearish = False
            if gate_on:
                hist = [c for c in regime_closes[:i + 1] if c is not None]
                bearish = len(hist) >= 2 and not regime_ok_from_closes(hist)

            elig = [s for s in aligned if aligned[s][2] is not None and i >= aligned[s][2]]
            if elig:
                closes = {s: aligned[s][0][i] for s in elig}
                book = cash + sum(shares.get(s, 0.0) * closes[s] for s in elig)
                w_sum = sum(weights[s] for s in elig)
                targets = {s: book * weights[s] / w_sum for s in elig}

                # trims run regardless of regime (risk control, not a buy)
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

                if bearish:
                    n_held_back += 1
                else:
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
            "n_held_back": n_held_back, "deposited": DEPOSIT * len(deposit_days)}


def setup():
    tiers = universe()
    data = load_bars(sorted(tiers))
    tiers = {t: v for t, v in tiers.items() if t in data}
    print(f"Universe: {len(data)} tickers (excl. {sorted(EXCLUDE)})")

    spy = json.loads((CACHE / "SPY.json").read_text())
    full_cal = [b["t"][:10] for b in spy]

    regime_bars = json.loads((CACHE / f"{REGIME_TICKER}.json").read_text())
    regime_dix = {b["t"][:10]: float(b["c"]) for b in regime_bars}

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

    regime_closes_al, last_r = [], None
    for dt in full_cal:
        last_r = regime_dix.get(dt, last_r)
        regime_closes_al.append(last_r)

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
    regime_closes_al = regime_closes_al[off:]
    print(f"Sim window: {calendar[0]} → {calendar[-1]}  "
          f"({len(deposit_days)} monthly deposits of ${DEPOSIT:,.0f})")
    return tiers, aligned, regime_closes_al, calendar, deposit_days


def verdict(res: dict) -> str:
    a, b = res["A"]["ann_twr"], res["B"]["ann_twr"]
    if b - a > ADOPT_THRESHOLD_PP:
        return (f"DROP THE GATE — no-gate (B) beats current (A) by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. The regime gate is cash drag.")
    if a - b > ADOPT_THRESHOLD_PP:
        return (f"KEEP THE GATE — current (A) beats no-gate (B) by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. The regime gate earns its keep.")
    return (f"NO CHANGE — within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). Regime gate stays; question closed.")


def main() -> int:
    tiers, aligned, regime_closes, calendar, deposit_days = setup()
    res = {
        "A": simulate(True, tiers, TIER_WEIGHTS_FLAT := {t: TIER_WEIGHTS[tiers[t]] for t in tiers},
                     aligned, regime_closes, calendar, deposit_days),
        "B": simulate(False, tiers, TIER_WEIGHTS_FLAT, aligned, regime_closes,
                     calendar, deposit_days),
    }
    v = verdict(res)

    names = {"A": "A — current (regime gate ON)", "B": "B — no regime gate"}
    lines = [
        "# Regime-gate backtest — does the QQQ 200-EMA gate earn its keep?",
        f"_{date.today().isoformat()} · window {calendar[0]} → {calendar[-1]} · "
        f"{len(tiers)} tickers (T1-spec, no crypto) · ${DEPOSIT:,.0f}/mo × {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt B (drop the gate) only "
        f"if it beats A by >{ADOPT_THRESHOLD_PP}pp annualized TWR; A beating B by the "
        f"same margin means the gate earns its keep; inside the threshold = no change. "
        f"Weight scheme and trim rule held at current production values throughout. "
        f"One test, one verdict.",
        "",
        "| Arm | Ann. TWR | Final value | MaxDD | Deposits held back |",
        "|-----|---------:|------------:|------:|--------------------:|",
    ]
    for k in ("A", "B"):
        r = res[k]
        lines.append(f"| {names[k]} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"{r['max_dd']:.1f}% | {r['n_held_back']} |")
    lines += ["",
              f"B − A gap: {res['B']['ann_twr'] - res['A']['ann_twr']:+.2f}pp annualized",
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One window, one mostly-rising sample with only brief bearish stretches — "
              "the regime gate's real test is a sustained bear market, which this window "
              "barely contains. The threshold exists because a small edge here is noise, "
              "not signal._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
