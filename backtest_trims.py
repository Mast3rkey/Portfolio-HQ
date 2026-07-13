"""
backtest_trims.py — one-time test: is the band/spec profit-taking rule
(cap_multiple 1.25x, trim RSI > 60) the right shape, or arbitrary?

Five arms, identical deposits, identical tickers, identical gap-fill buying —
the TRIM RULE is the only difference:
  A — current production: band trims above 1.25x target, spec above 1.0x,
      both only when RSI14 > 60 (trim into strength)
  B — tighter: 1.15x / RSI 55
  C — looser: 1.40x / RSI 65
  D — never trim (control: do trims add anything at all?)
  E — mechanical 1.25x / no RSI gate (control: does the RSI gate itself help?)

Trim proceeds go to cash and are redeployed into the largest gaps the same
cycle — the production loop's behavior.

PRE-COMMITTED DECISION RULE (fixed before any results were computed):
  * Adopt an alternative (B/C/E) only if it beats BOTH A and D by more than
    ADOPT_THRESHOLD_PP (1.0 percentage point annualized TWR).
  * If D beats A by more than the threshold, the trim rule is cash drag —
    finding is "trims subtract value" (risk posture then decided separately;
    trims also serve concentration control, which TWR alone doesn't price).
  * Anything inside the threshold = noise → "no change, keep it simple".
  * One test, one verdict. No variant mining.

Run:  python3 backtest_trims.py   (reuses data/backtest bar cache)
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "backtest"
REPORT = HERE / "reports" / "trim_backtest.md"

# ── pre-committed parameters (do not tune after results) ────────────────────────
ADOPT_THRESHOLD_PP = 1.0
DEPOSIT = 2000.0              # first trading day of each month
MIN_LOT = 25.0
MIN_HISTORY = 210             # sessions before a ticker joins the sim
MIN_TICKERS_TO_START = 20
EXCLUDE = {"SPCX", "SKHY"}    # no/insufficient data (documented previously)
RSI_PERIOD = 14

ARMS = {
    "A": {"label": "A — current (1.25x / RSI 60)", "band_cap": 1.25, "trim_rsi": 60.0},
    "B": {"label": "B — tighter (1.15x / RSI 55)", "band_cap": 1.15, "trim_rsi": 55.0},
    "C": {"label": "C — looser (1.40x / RSI 65)",  "band_cap": 1.40, "trim_rsi": 65.0},
    "D": {"label": "D — never trim (control)",     "band_cap": None, "trim_rsi": None},
    "E": {"label": "E — mechanical 1.25x, no RSI gate", "band_cap": 1.25, "trim_rsi": None},
}


# ── universe ─────────────────────────────────────────────────────────────────────

def universe() -> tuple[dict[str, float], dict[str, str]]:
    """{ticker: weight_pct}, {ticker: tier} for band+spec, minus exclusions."""
    t = yaml.safe_load(open(HERE / "targets.yaml"))
    weights, tiers = {}, {}
    for tier_name in ("band", "spec"):
        tier = t["tiers"][tier_name]
        for s in tier["tickers"]:
            s = s.upper()
            if s in EXCLUDE:
                continue
            weights[s] = float(tier["weight_pct"])
            tiers[s] = tier_name
    return weights, tiers


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


# ── indicators (Wilder RSI, precomputed per ticker) ─────────────────────────────

def rsi_series(closes: list[float], period: int = RSI_PERIOD) -> list[float | None]:
    """rsi[i] uses closes[0..i]; None until period+1 closes exist. Wilder
    smoothing — matches indicators.rsi (ewm alpha=1/period, adjust=False)."""
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


# ── portfolio math (shared with rung backtest, duplicated to stay standalone) ───

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


# ── simulation ────────────────────────────────────────────────────────────────────

def simulate(arm_cfg: dict, aligned: dict, weights: dict, tiers: dict,
             calendar: list[str], deposit_days: list[str]) -> dict:
    """One arm. aligned[s] = (closes_ffill, rsi_ffill, first_elig_idx) on the
    master calendar. Deposit day: trims (per arm rule) → cash, then gap-fill
    buys largest-first, all at that day's close."""
    band_cap, trim_rsi = arm_cfg["band_cap"], arm_cfg["trim_rsi"]
    dep_set = set(deposit_days)
    cash = 0.0
    shares: dict[str, float] = {}
    values: list[float] = []
    flows: dict[int, float] = {}
    n_trims = 0
    trimmed_dollars = 0.0

    for i, d in enumerate(calendar):
        if d in dep_set:
            flows[i] = DEPOSIT
            cash += DEPOSIT
            elig = [s for s in aligned if aligned[s][2] is not None
                    and i >= aligned[s][2]]
            if elig:
                closes = {s: aligned[s][0][i] for s in elig}
                book = cash + sum(shares.get(s, 0.0) * closes[s] for s in elig)
                w_sum = sum(weights[s] for s in elig)
                targets = {s: book * weights[s] / w_sum for s in elig}

                # ---- trims (the arm's rule) --------------------------------
                if band_cap is not None:
                    for s in elig:
                        val = shares.get(s, 0.0) * closes[s]
                        cap = band_cap if tiers[s] == "band" else 1.0
                        if val <= cap * targets[s]:
                            continue
                        r = aligned[s][1][i]
                        if trim_rsi is not None and (r is None or r <= trim_rsi):
                            continue
                        excess = val - targets[s]
                        if excess < MIN_LOT:
                            continue
                        shares[s] -= excess / closes[s]
                        cash += excess
                        n_trims += 1
                        trimmed_dollars += excess

                # ---- buys: largest gap first, fill to target ---------------
                gaps = sorted(((targets[s] - shares.get(s, 0.0) * closes[s], s)
                               for s in elig), reverse=True)
                for gap, s in gaps:
                    if gap < MIN_LOT or cash < MIN_LOT:
                        break
                    spend = min(gap, cash)
                    shares[s] = shares.get(s, 0.0) + spend / closes[s]
                    cash -= spend

        # ---- mark portfolio daily -----------------------------------------
        v = cash
        for s, sh in shares.items():
            px = aligned[s][0][i]
            if px is not None:
                v += sh * px
        values.append(v)

    # diagnostic: final-day concentration (largest single position as % of sleeve)
    last = len(calendar) - 1
    final_vals = {s: sh * aligned[s][0][last] for s, sh in shares.items()
                  if aligned[s][0][last] is not None}
    max_pos_pct = (max(final_vals.values()) / values[-1] * 100.0) if final_vals else 0.0

    return {"ann_twr": twr_annualized(values, flows), "final": values[-1],
            "max_dd": max_drawdown(values), "n_trims": n_trims,
            "trimmed": trimmed_dollars, "deposited": DEPOSIT * len(deposit_days),
            "max_pos_pct": max_pos_pct,
            "max_pos_name": max(final_vals, key=final_vals.get) if final_vals else "—",
            "daily_values": values, "flows": flows}


# ── verdict + report ─────────────────────────────────────────────────────────────

def verdict(res: dict) -> str:
    a, d_ = res["A"]["ann_twr"], res["D"]["ann_twr"]
    for k in ("B", "C", "E"):
        x = res[k]["ann_twr"]
        if x - a > ADOPT_THRESHOLD_PP and x - d_ > ADOPT_THRESHOLD_PP:
            return (f"ADOPT {k} — beats both current and never-trim by "
                    f">{ADOPT_THRESHOLD_PP}pp annualized.")
    if d_ - a > ADOPT_THRESHOLD_PP:
        return (f"TRIMS ARE DRAG — never-trim beats the current rule by "
                f">{ADOPT_THRESHOLD_PP}pp annualized. TWR says drop the trim; "
                "concentration-control value must be weighed separately before acting.")
    return (f"NO CHANGE — all arms within the pre-committed noise threshold "
            f"({ADOPT_THRESHOLD_PP}pp). Current 1.25x / RSI 60 stays; question closed.")


def setup() -> tuple[dict, dict, dict, list[str], list[str]]:
    """Load + align everything the sim needs. Returns
    (aligned, weights, tiers, calendar, deposit_days)."""
    weights, tiers = universe()
    data = load_bars(sorted(weights))
    print(f"Universe: {len(data)} band/spec tickers (excl. {sorted(EXCLUDE)})")

    # master calendar from SPY (cached by the rung backtest)
    spy = json.loads((CACHE / "SPY.json").read_text())
    full_cal = [b["t"][:10] for b in spy]

    # align each ticker to the master calendar (ffill), precompute RSI
    aligned: dict[str, tuple] = {}
    for s, bars in data.items():
        closes_raw = [float(b["c"]) for b in bars]
        rsi_raw = rsi_series(closes_raw)
        dix = {b["t"][:10]: j for j, b in enumerate(bars)}
        closes_al: list[float | None] = []
        rsi_al: list[float | None] = []
        first_elig = None
        last_j = None
        for i, dt in enumerate(full_cal):
            j = dix.get(dt, last_j)
            last_j = j
            closes_al.append(closes_raw[j] if j is not None else None)
            rsi_al.append(rsi_raw[j] if j is not None else None)
            if first_elig is None and j is not None and j + 1 >= MIN_HISTORY:
                first_elig = i
        aligned[s] = (closes_al, rsi_al, first_elig)

    # deposit days: first trading day of each month once enough are eligible
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
    return aligned, weights, tiers, calendar, deposit_days


def main() -> int:
    aligned, weights, tiers, calendar, deposit_days = setup()
    res = {k: simulate(cfg, aligned, weights, tiers, calendar, deposit_days)
           for k, cfg in ARMS.items()}
    v = verdict(res)

    lines = [
        "# Trim backtest — is 1.25x / RSI 60 the right profit-taking rule?",
        f"_{date.today().isoformat()} · window {calendar[0]} → {calendar[-1]} · "
        f"{len(aligned)} band/spec tickers · ${DEPOSIT:,.0f}/mo × {len(deposit_days)} deposits_",
        "",
        f"**Pre-committed rule (fixed before results):** adopt an alternative only "
        f"if it beats BOTH the current rule (A) and never-trim (D) by "
        f">{ADOPT_THRESHOLD_PP}pp annualized TWR; D beating A by the same margin "
        f"means trims are drag; inside the threshold = no change. One test, one verdict.",
        "",
        "| Arm | Ann. TWR | Final value | MaxDD | Trims | $ trimmed | Largest final position |",
        "|-----|---------:|------------:|------:|------:|----------:|-----------------------:|",
    ]
    for k, cfg in ARMS.items():
        r = res[k]
        lines.append(f"| {cfg['label']} | {r['ann_twr']:.2f}% | ${r['final']:,.0f} | "
                     f"{r['max_dd']:.1f}% | {r['n_trims']} | ${r['trimmed']:,.0f} | "
                     f"{r['max_pos_name']} {r['max_pos_pct']:.1f}% |")
    a = res["A"]["ann_twr"]
    lines += ["",
              "Gaps vs current (A): " + " · ".join(
                  f"{k}−A: {res[k]['ann_twr'] - a:+.2f}pp" for k in ("B", "C", "D", "E")),
              "",
              f"## Verdict\n**{v}**",
              "",
              "_One window, one mostly-rising sample. The threshold exists because a "
              "small edge in one sample is noise, not signal. Trims also serve "
              "concentration control, which TWR alone doesn't price._"]
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n[written to {REPORT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
