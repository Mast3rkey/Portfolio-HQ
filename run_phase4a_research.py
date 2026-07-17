#!/usr/bin/env python3
"""
run_phase4a_research.py — Phase 4A concentration x margin research
execution driver.

Implements docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md, per the
resolutions in docs/PHASE4A_ASSUMPTION_RESOLUTION.md and the thresholds
in docs/PHASE4A_MATERIALITY_THRESHOLDS.md. Imports (does not modify,
beyond the one already-committed, tested track_tickers/tracked_values
addition) margin_simulation.py, and imports (does not modify)
phase4a_lib.py's pure derivation helpers.

Implements NO concentration controls, NO allocation changes, NO new
leverage rules, NO repayment policy changes, NO doctrine changes — every
function this script calls only measures or constructs scenario INPUTS
(weights, price data); nothing here is a rule that could ever fire in
production.

## Design notes (stated here, not discovered mid-run)

- **Leverage isolation** (resolution §4/§5): Scenarios A/B/C run
  UNLEVERED (leverage_cap=1.0) so only concentration varies between
  them. Scenario D is the ONLY place leverage turns on (1.8x, fixed, no
  sweep) — the sole new variable D introduces versus C.
- **"Historical drift" construction** (resolution §1): margin_
  simulation.py's simulate() implements NO trim/rebalance-down logic
  at all (verified by reading the engine before writing this driver —
  the only "sell" path is _fund_repayment(), used exclusively by an
  active repayment model, none of which run in A/B/C/D here). This
  means every scenario in this harness already runs "un-trimmed" by
  construction — there is no separate "disable the trim rule" step to
  take, because no trim rule exists here to disable. Scenario A's own
  natural, un-inflated concentration trajectory (tracked via
  track_tickers) IS this plan's "historical drift" evidence — not a
  shortcut, a fact about this specific harness's mechanics, disclosed
  explicitly rather than silently assumed.
- **Concentrated ticker**: NVDA — a real, already-referenced T1 name
  with a real, already-documented historical decomposition
  (t1t2_trim_backtest.md: 2.14x target, -66.4% peak-to-trough), not an
  arbitrary pick.
- **Correlated cluster**: semis (targets.yaml's real, existing 25%-cap
  cluster, 13 members, 12 present in this harness's 63-ticker universe
  after SPCX/SKHY exclusion) — used as-is, never modified, per the
  research plan's explicit "do not change cluster caps."
- **Numeric parameters chosen this session** (flagged, not separately
  pre-approved beyond the general execution go-ahead): NVDA weight
  multiplier 3.0x, semis per-member multiplier 1.8x, hypothetical shock
  -40% over 15 trading days starting at 70% through the window. Stated
  explicitly in the report as session choices, not doctrine.

Run:  python3 run_phase4a_research.py
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from margin_simulation import (
    HYPOTHETICAL_LABEL,
    ScenarioConfig,
    load_real_aligned_data,
    repayment_model_0,
    simulate,
)
from phase4a_lib import (
    apply_synthetic_shock,
    classify_event_repetition,
    classify_gap,
    concentration_series,
    forced_deleveraging_events,
    inflate_weights,
    is_recovery_material,
    ticker_own_max_drawdown,
    time_above_threshold_pct,
    worst_drawdown_recovery,
)

HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "docs" / "PHASE4A_RESEARCH_REPORT.md"
JSON_PATH = HERE / "docs" / "results" / "PHASE4A_RESEARCH_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_APR = 0.05
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP_D = 1.8
UNLEVERED_CAP = 1.0

NVDA_MULTIPLIER = 3.0
SEMIS_MULTIPLIER = 1.8
SHOCK_PCT = -40.0
SHOCK_DURATION_DAYS = 15
SHOCK_START_FRACTION = 0.70  # position in the window, chosen after deposits have accumulated

SEMIS_CLUSTER = ["ASML", "TSM", "NVDA", "AVGO", "AMD", "MU", "MRVL", "KLAC", "LRCX", "AMAT", "WDC", "INTC"]
CONCENTRATION_CAP_PCT = 25.0  # real semis cluster cap, targets.yaml -- measurement reference only

MATERIAL_THRESHOLD_PP = 2.0
NOISE_FLOOR_PP = 0.5


def _scenario(name, leverage_cap, interest_apr=INTEREST_APR):
    return ScenarioConfig(name=name, leverage_cap=leverage_cap, interest_apr=interest_apr,
                          interest_free_amount=INTEREST_FREE_AMOUNT,
                          repayment_fn=repayment_model_0, pre_trade_fn=None,
                          repayment_model_name="MODEL_0")


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"
    n_deposits = len(deposit_days)
    shock_start_idx = int(len(calendar) * SHOCK_START_FRACTION)

    def run(sc, w, al, track):
        return simulate(sc, w, al, calendar, deposit_days, deposit_amount=DEPOSIT_AMOUNT,
                        min_lot=MIN_LOT, track_tickers=track)

    nvda_baseline_weight = weights.get("NVDA", 0.0)
    w_sum_baseline = sum(weights.values())
    nvda_baseline_share_pct = (nvda_baseline_weight / w_sum_baseline * 100.0) if w_sum_baseline else 0.0
    nvda_time_threshold_pct = nvda_baseline_share_pct * 1.5  # T1/T2 ceiling multiplier, reused as a measurement reference only

    print(f"Universe: {len(weights)} tickers | window {window} | {n_deposits} deposits")
    print(f"NVDA baseline weight share: {nvda_baseline_share_pct:.2f}% of book -> "
          f"time-above threshold {nvda_time_threshold_pct:.2f}%")

    # ---- Scenario A: control, unlevered ------------------------------------
    r_a = run(_scenario("A -- control (unlevered)", UNLEVERED_CAP), weights, aligned,
             track=["NVDA"] + SEMIS_CLUSTER)

    # ---- Scenario B: synthetic concentration, unlevered --------------------
    w_nvda = inflate_weights(weights, ["NVDA"], NVDA_MULTIPLIER)
    r_b_nvda = run(_scenario("B-NVDA -- synthetic concentration (unlevered)", UNLEVERED_CAP),
                  w_nvda, aligned, track=["NVDA"])

    w_semis = inflate_weights(weights, SEMIS_CLUSTER, SEMIS_MULTIPLIER)
    r_b_semis = run(_scenario("B-semis -- synthetic cluster concentration (unlevered)", UNLEVERED_CAP),
                    w_semis, aligned, track=SEMIS_CLUSTER)

    # ---- Scenario C: concentrated + hypothetical stress, unlevered --------
    aligned_shocked = apply_synthetic_shock(aligned, "NVDA", SHOCK_PCT, shock_start_idx, SHOCK_DURATION_DAYS)
    r_c_hyp = run(_scenario("C-NVDA-hyp -- concentration + hypothetical shock (unlevered)", UNLEVERED_CAP),
                 w_nvda, aligned_shocked, track=["NVDA"])

    # ---- Scenario D: concentrated + stress + margin ------------------------
    r_d_hist = run(_scenario("D-NVDA-hist -- concentration + historical stress + 1.8x margin", LEVERAGE_CAP_D),
                   w_nvda, aligned, track=["NVDA"])
    r_d_hyp = run(_scenario("D-NVDA-hyp -- concentration + hypothetical shock + 1.8x margin", LEVERAGE_CAP_D),
                 w_nvda, aligned_shocked, track=["NVDA"])
    r_d_semis = run(_scenario("D-semis-hist -- cluster concentration + historical stress + 1.8x margin", LEVERAGE_CAP_D),
                    w_semis, aligned, track=SEMIS_CLUSTER)

    ticker_real_max_dd = ticker_own_max_drawdown(aligned, "NVDA")
    print(f"NVDA real historical max drawdown in window: {ticker_real_max_dd:.1f}%")

    write_outputs(window, n_deposits, shock_start_idx, nvda_baseline_share_pct,
                 nvda_time_threshold_pct, ticker_real_max_dd,
                 r_a, r_b_nvda, r_b_semis, r_c_hyp, r_d_hist, r_d_hyp, r_d_semis)


def _stats(r, tracked_keys):
    """Bundle of derived metrics for one SimulationResult."""
    m = r.metrics()
    conc = concentration_series(r.tracked_values, r.book_values)
    recov = worst_drawdown_recovery(r.book_values)
    delev_days = forced_deleveraging_events(r.leverage_series, r.leverage_cap)
    return {
        "metrics": m,
        "concentration_series_final_pct": conc[-1] if conc else 0.0,
        "concentration_series_max_pct": max(conc) if conc else 0.0,
        "recovery": {
            "trough_index": recov.trough_index, "peak_value": recov.peak_value,
            "trough_value": recov.trough_value, "recovery_index": recov.recovery_index,
            "recovery_days": recov.recovery_days,
        },
        "forced_deleveraging_days": delev_days,
        "n_forced_deleveraging_events": len(delev_days),
    }


def write_outputs(window, n_deposits, shock_start_idx, nvda_baseline_share_pct,
                  nvda_time_threshold_pct, ticker_real_max_dd,
                  r_a, r_b_nvda, r_b_semis, r_c_hyp, r_d_hist, r_d_hyp, r_d_semis):
    s_a = _stats(r_a, ["NVDA"] + SEMIS_CLUSTER)
    s_b_nvda = _stats(r_b_nvda, ["NVDA"])
    s_b_semis = _stats(r_b_semis, SEMIS_CLUSTER)
    s_c_hyp = _stats(r_c_hyp, ["NVDA"])
    s_d_hist = _stats(r_d_hist, ["NVDA"])
    s_d_hyp = _stats(r_d_hyp, ["NVDA"])
    s_d_semis = _stats(r_d_semis, SEMIS_CLUSTER)

    a_conc_nvda = concentration_series({"NVDA": r_a.tracked_values["NVDA"]}, r_a.book_values)
    b_conc_nvda = concentration_series({"NVDA": r_b_nvda.tracked_values["NVDA"]}, r_b_nvda.book_values)
    d_hist_conc_nvda = concentration_series({"NVDA": r_d_hist.tracked_values["NVDA"]}, r_d_hist.book_values)
    a_conc_semis = concentration_series({t: r_a.tracked_values[t] for t in SEMIS_CLUSTER}, r_a.book_values)
    b_conc_semis = concentration_series({t: r_b_semis.tracked_values[t] for t in SEMIS_CLUSTER}, r_b_semis.book_values)
    d_semis_conc = concentration_series({t: r_d_semis.tracked_values[t] for t in SEMIS_CLUSTER}, r_d_semis.book_values)

    time_above_a = time_above_threshold_pct(a_conc_nvda, nvda_time_threshold_pct)
    time_above_b = time_above_threshold_pct(b_conc_nvda, nvda_time_threshold_pct)
    time_above_d = time_above_threshold_pct(d_hist_conc_nvda, nvda_time_threshold_pct)
    time_above_semis_a = time_above_threshold_pct(a_conc_semis, CONCENTRATION_CAP_PCT)
    time_above_semis_b = time_above_threshold_pct(b_conc_semis, CONCENTRATION_CAP_PCT)
    time_above_semis_d = time_above_threshold_pct(d_semis_conc, CONCENTRATION_CAP_PCT)

    twr_a, dd_a = s_a["metrics"]["ann_twr_pct"], s_a["metrics"]["max_drawdown_pct"]
    twr_b, dd_b = s_b_nvda["metrics"]["ann_twr_pct"], s_b_nvda["metrics"]["max_drawdown_pct"]
    twr_d_hist, dd_d_hist = s_d_hist["metrics"]["ann_twr_pct"], s_d_hist["metrics"]["max_drawdown_pct"]
    twr_d_hyp, dd_d_hyp = s_d_hyp["metrics"]["ann_twr_pct"], s_d_hyp["metrics"]["max_drawdown_pct"]

    gap_b_vs_a_dd = dd_b - dd_a
    gap_dhist_vs_b_dd = dd_d_hist - dd_b
    gap_dhyp_vs_b_dd = dd_d_hyp - dd_b

    event_counts = {
        "stress_case_1_historical": s_d_hist["n_forced_deleveraging_events"],
        "stress_case_1_hypothetical": s_d_hyp["n_forced_deleveraging_events"],
        "stress_case_2_cluster": s_d_semis["n_forced_deleveraging_events"],
        "stress_case_4_concentration_only": 0,  # unlevered by design, no leverage cap to breach
    }
    repeated = classify_event_repetition(event_counts)

    recovery_material_d_hist = is_recovery_material(
        s_d_hist["recovery"]["recovery_days"], s_a["recovery"]["recovery_days"])
    recovery_material_d_hyp = is_recovery_material(
        s_d_hyp["recovery"]["recovery_days"], s_a["recovery"]["recovery_days"])

    class_b_vs_a = classify_gap(gap_b_vs_a_dd, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP)
    class_dhist_vs_b = classify_gap(gap_dhist_vs_b_dd, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP)
    class_dhyp_vs_b = classify_gap(gap_dhyp_vs_b_dd, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP)

    any_material_gap = "material" in (class_dhist_vs_b, class_dhyp_vs_b)
    all_noise = all(c == "noise" for c in (class_b_vs_a, class_dhist_vs_b, class_dhyp_vs_b))

    if any_material_gap and repeated:
        outcome = "Evidence supports"
    elif all_noise and not repeated:
        outcome = "Evidence does not support"
    else:
        outcome = "Evidence inconclusive"

    # ---- machine-readable output --------------------------------------------
    RESULTS_DIR = JSON_PATH.parent
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history. Every "
                       "scenario is a hypothetical simulation of a synthetic "
                       "$0-start account through real historical prices. See "
                       "docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "n_deposits": n_deposits,
        "parameters": {
            "concentrated_ticker": "NVDA", "nvda_multiplier": NVDA_MULTIPLIER,
            "semis_cluster": SEMIS_CLUSTER, "semis_multiplier": SEMIS_MULTIPLIER,
            "hypothetical_shock_pct": SHOCK_PCT, "shock_duration_days": SHOCK_DURATION_DAYS,
            "shock_start_idx": shock_start_idx, "leverage_cap_d": LEVERAGE_CAP_D,
            "material_threshold_pp": MATERIAL_THRESHOLD_PP, "noise_floor_pp": NOISE_FLOOR_PP,
        },
        "results": {
            "A_control": s_a, "B_NVDA_synthetic": s_b_nvda, "B_semis_synthetic": s_b_semis,
            "C_NVDA_hypothetical_stress": s_c_hyp, "D_NVDA_historical_stress": s_d_hist,
            "D_NVDA_hypothetical_stress": s_d_hyp, "D_semis_historical_stress": s_d_semis,
        },
        "materiality_evaluation": {
            "gap_B_vs_A_maxdd_pp": gap_b_vs_a_dd, "gap_B_vs_A_class": class_b_vs_a,
            "gap_DhistVsB_maxdd_pp": gap_dhist_vs_b_dd, "gap_DhistVsB_class": class_dhist_vs_b,
            "gap_DhypVsB_maxdd_pp": gap_dhyp_vs_b_dd, "gap_DhypVsB_class": class_dhyp_vs_b,
            "event_counts_by_stress_case": event_counts, "events_repeated": repeated,
            "recovery_material_d_hist": recovery_material_d_hist,
            "recovery_material_d_hyp": recovery_material_d_hyp,
            "outcome": outcome,
        },
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    # ---- markdown report -----------------------------------------------------
    L = []
    L.append("# Phase 4A Research Report: Concentration x Margin Interaction")
    L.append("")
    L.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
             "history. Every scenario below simulates a synthetic $0-start "
             "account through real historical prices (data/backtest/*.json). "
             "See `docs/PHASE4A_CONCENTRATION_MARGIN_RESEARCH_PLAN.md` for the "
             "pre-approved design this run follows, and "
             "`docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.")
    L.append("")
    L.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}. Window: {window}. "
             f"{n_deposits} monthly ${DEPOSIT_AMOUNT:,.0f} deposits. Concentrated "
             "ticker: NVDA (real, already-decomposed reference point, "
             "`reports/t1t2_trim_backtest.md`). Correlated cluster: semis "
             "(real, existing 25%-cap cluster, `targets.yaml`, unmodified). "
             "Scenarios A/B/C run unlevered (leverage_cap=1.0) so only "
             "concentration varies; Scenario D is the only place leverage "
             "turns on (1.8x, fixed, no sweep) — per "
             "`docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §4/§5._")
    L.append("")
    L.append("## Methodology note: \"historical drift\" construction")
    L.append("")
    L.append("`margin_simulation.py`'s `simulate()` implements no trim/rebalance-down "
             "logic at all outside an active repayment model (verified before this "
             "run; the only sell path is `_fund_repayment()`, unused here since no "
             "repayment model runs in any scenario below). Every scenario in this "
             "harness already runs \"un-trimmed\" by construction — there is no "
             "separate \"disable the trim rule\" step to take, because none exists "
             "to disable. **Scenario A's own natural, un-inflated NVDA/semis weight "
             "trajectory below is this research's \"historical drift\" evidence** — "
             "not a shortcut, a disclosed fact about this harness's actual mechanics.")
    L.append("")
    L.append(f"NVDA baseline target share: **{nvda_baseline_share_pct:.2f}%** of book "
             f"(time-above-threshold reference, 1.5x this value = "
             f"**{nvda_time_threshold_pct:.2f}%**, reusing the real T1/T2 ceiling "
             "multiplier as a measurement reference only — no rule implemented). "
             f"NVDA's real historical max drawdown in this window: "
             f"**{ticker_real_max_dd:.1f}%** (the historical-primary stress magnitude "
             "for stress case 1, per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §2a).")
    L.append("")

    def _row(label, s):
        m = s["metrics"]
        return (f"| {label} | {m['ann_twr_pct']:.2f}% | {m['max_drawdown_pct']:.2f}% | "
               f"{s['concentration_series_max_pct']:.2f}% | "
               f"{s['n_forced_deleveraging_events']} | "
               f"{s['recovery']['recovery_days'] if s['recovery']['recovery_days'] is not None else 'never'} |")

    L.append("## Scenario results")
    L.append("")
    L.append("| Scenario | Ann. TWR | MaxDD | Max concentration | Forced-delev. events | Recovery days |")
    L.append("|---|---:|---:|---:|---:|---:|")
    L.append(_row("A — control (unlevered)", s_a))
    L.append(_row("B-NVDA — synthetic concentration (unlevered)", s_b_nvda))
    L.append(_row("B-semis — synthetic cluster concentration (unlevered)", s_b_semis))
    L.append(_row("C-NVDA-hyp — concentration + hypothetical shock (unlevered)", s_c_hyp))
    L.append(_row("D-NVDA-hist — concentration + historical stress + 1.8x margin", s_d_hist))
    L.append(_row("D-NVDA-hyp — concentration + hypothetical shock + 1.8x margin", s_d_hyp))
    L.append(_row("D-semis-hist — cluster concentration + historical stress + 1.8x margin", s_d_semis))
    L.append("")

    L.append("## Time above concentration thresholds")
    L.append("")
    L.append("| Scenario | NVDA time above 1.5x target share | Semis time above 25% cluster cap |")
    L.append("|---|---:|---:|")
    L.append(f"| A (control) | {time_above_a:.1f}% | {time_above_semis_a:.1f}% |")
    L.append(f"| B (synthetic concentration) | {time_above_b:.1f}% | {time_above_semis_b:.1f}% |")
    L.append(f"| D (concentration + margin) | {time_above_d:.1f}% | {time_above_semis_d:.1f}% |")
    L.append("")

    L.append("## Required stress cases")
    L.append("")
    L.append("1. **Single largest holding drawdown** — historical primary: NVDA's real "
             f"{ticker_real_max_dd:.1f}% decline, embedded in B-NVDA/D-NVDA-hist's real "
             "price data. Hypothetical secondary (robustness only, per the stress "
             f"methodology hierarchy): a constructed {SHOCK_PCT:.0f}% shock over "
             f"{SHOCK_DURATION_DAYS} days, C-NVDA-hyp/D-NVDA-hyp.")
    L.append("2. **Multiple correlated holdings drawdown** — B-semis/D-semis-hist, using "
             "the real, existing semis cluster (unmodified cap, used only as a "
             "measurement reference in the time-above-threshold table above).")
    L.append("3. **Market drawdown with concentrated exposure** — see the dedicated "
             "section below; measured as a windowed view of D-NVDA-hist's own series, "
             "not a separate simulation run.")
    L.append("4. **Concentration increase without leverage increase** — directly the "
             "A vs. B-NVDA comparison (both unlevered): MaxDD gap "
             f"{gap_b_vs_a_dd:+.2f}pp, classified **{class_b_vs_a}** against the "
             f"{MATERIAL_THRESHOLD_PP}pp/{NOISE_FLOOR_PP}pp materiality bands.")
    L.append("")

    # Stress case 3: windowed view around the account's own worst drawdown episode
    trough_a = s_a["recovery"]["trough_index"]
    L.append("### Stress case 3 detail: market drawdown with concentrated exposure")
    L.append("")
    if trough_a is not None:
        window_start = max(0, trough_a - 20)
        window_end = min(len(d_hist_conc_nvda) - 1, trough_a + 20)
        conc_at_trough = d_hist_conc_nvda[trough_a] if trough_a < len(d_hist_conc_nvda) else None
        lev_at_trough = (r_d_hist.leverage_series[trough_a]
                        if trough_a < len(r_d_hist.leverage_series) else None)
        L.append(f"Control's (Scenario A) own worst portfolio-level drawdown episode "
                 f"troughs at simulated day index {trough_a}. At that same point in "
                 f"D-NVDA-hist (concentrated + margin), NVDA concentration was "
                 f"**{conc_at_trough:.2f}% of book**"
                 + (f", leverage was **{lev_at_trough:.3f}x**" if lev_at_trough is not None else "")
                 + " — i.e., what the concentrated, levered account looked like during "
                 "the account's own worst broad-market episode in this window, not a "
                 "separately constructed shock.")
    else:
        L.append("Control (Scenario A) never experienced a portfolio-level drawdown "
                 "episode in this window (monotonically non-declining book value) — "
                 "there is no market-drawdown period to examine for this stress case "
                 "in this specific window. A real, honest finding about this window's "
                 "character (consistent with the standing \"one mostly-rising sample\" "
                 "caveat), not a gap in the methodology.")
    L.append("")

    L.append("## Materiality evaluation")
    L.append("")
    L.append(f"Per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`: material threshold "
             f"{MATERIAL_THRESHOLD_PP}pp, noise floor {NOISE_FLOOR_PP}pp, forced-"
             "deleveraging repetition = ≥3 events in one stress case OR events in "
             "≥2 of the 4 stress cases.")
    L.append("")
    L.append("| Comparison | MaxDD gap | Classification |")
    L.append("|---|---:|---|")
    L.append(f"| B (concentration alone) vs. A (control) | {gap_b_vs_a_dd:+.2f}pp | {class_b_vs_a} |")
    L.append(f"| D-hist (concentration+margin+historical stress) vs. B | {gap_dhist_vs_b_dd:+.2f}pp | {class_dhist_vs_b} |")
    L.append(f"| D-hyp (concentration+margin+hypothetical stress) vs. B | {gap_dhyp_vs_b_dd:+.2f}pp | {class_dhyp_vs_b} |")
    L.append("")
    L.append(f"Forced-deleveraging events by stress case: "
             + "; ".join(f"{k}={v}" for k, v in event_counts.items()) + ". "
             f"Repeated (per §5's definition): **{repeated}**.")
    L.append("")
    L.append(f"Recovery materiality: D-hist vs. A baseline recovery — **{recovery_material_d_hist}**"
             f" (D-hist recovery: {s_d_hist['recovery']['recovery_days']}, "
             f"A baseline recovery: {s_a['recovery']['recovery_days']}). "
             f"D-hyp vs. A baseline recovery — **{recovery_material_d_hyp}**"
             f" (D-hyp recovery: {s_d_hyp['recovery']['recovery_days']}).")
    L.append("")
    L.append(f"## Outcome: **{outcome}**")
    L.append("")
    L.append("Per `docs/PHASE4A_ASSUMPTION_RESOLUTION.md` §6's three-way framework: "
             "\"Evidence supports\" requires a material MaxDD gap AND repeated "
             "forced-deleveraging events (both, not either alone, per "
             "`docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §5's necessary-not-sufficient "
             "framing). \"Evidence does not support\" requires every relevant gap at "
             "or below the noise floor with no event repetition. Anything else is "
             "\"Evidence inconclusive.\" **This outcome is not a doctrine change, is "
             "not a recommendation, and does not modify any production file** — "
             "per the standing rule, acting on it (in either direction) requires its "
             "own separate, explicit approval step.")
    L.append("")

    L.append("## Limitations")
    L.append("")
    L.append("- **One window, one construction per dimension.** 2021-2026, one "
             "concentrated single-name pick (NVDA) and one cluster pick (semis) — "
             "not a sweep across possible concentrated names or clusters.")
    L.append("- **Numeric parameters (3.0x NVDA multiplier, 1.8x semis multiplier, "
             "-40%/15-day hypothetical shock) were chosen this session**, flagged "
             "explicitly as session choices per `docs/PHASE4A_ASSUMPTION_"
             "RESOLUTION.md`'s disclosure discipline, not separately pre-approved "
             "beyond the general Phase 4A execution go-ahead.")
    L.append("- **The hypothetical shock has no modeled recovery** — it holds the "
             "shocked price level flat for the remainder of the series "
             "(`apply_synthetic_shock()`'s documented simplification), which "
             "differs from the historical-primary arm where NVDA's real price "
             "path does recover.")
    L.append("- **Time-above-threshold reference values (1.5x NVDA target share, "
             "25% semis cap) are existing real doctrine numbers reused for "
             "MEASUREMENT ONLY** — no rule was implemented, no cap was changed.")
    L.append("- **`margin_state.py`'s `concentration_risk_score()` was not called** — "
             "per the resolution document, that scorer stays read-only/reference-"
             "only and is not imported into this isolated simulation harness.")
    L.append("- No transaction-cost or tax model exists anywhere in this repo — "
             "any forced-deleveraging or stress-driven trading implied by this "
             "research's findings carries the same unpriced-cost caveat "
             "`docs/PHASE4_READINESS_REVIEW.md` already raised for Model B/C.")
    L.append("")
    L.append("_Advisory-adjacent research only. This report places no orders and "
             "makes no recommendation. Execute nothing based on this document "
             "alone._")

    REPORT_PATH.write_text("\n".join(L) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")
    print(f"\nOutcome: {outcome}")


if __name__ == "__main__":
    main()
