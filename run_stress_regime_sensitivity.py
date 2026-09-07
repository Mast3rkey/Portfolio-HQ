#!/usr/bin/env python3
"""
run_stress_regime_sensitivity.py — stress-regime execution assumptions
analysis driver, per docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md.

Re-runs the three already-approved Model B repay_fraction arms
(10%/25%/50%) through the UNMODIFIED margin_simulation.py scenario
builders, verifies each arm's headline numbers match the stored
docs/results/PHASE3_SENSITIVITY_RESULTS.json before any stress-regime
analysis is applied, then:

  Historical-primary: detects real stress windows from QQQ's real,
  already-cached OHLCV data (never invented), and measures where Model
  B's already-known repayment events actually fall relative to those
  windows -- no cost or tax assumption applied in this section at all,
  purely a timing/measurement analysis.

  Hypothetical-secondary, kept strictly separate: applies a disclosed,
  bounded cost multiplier (reusing the already-approved 15bps
  transaction-cost tier, elevated by a disclosed multiplier only for
  events inside a detected stress window) to test whether a regime-
  conditional friction assumption would matter, given the historical-
  primary section's own finding about event timing.

No production file touched. No repay_fraction selected. No leverage
cap examined or changed. See docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_
PLAN.md §6 for the full prohibited-conclusions list this script's
output must respect.

Run:  python3 run_stress_regime_sensitivity.py
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from margin_simulation import (
    HYPOTHETICAL_LABEL,
    load_real_aligned_data,
    scenario_fixed_leverage,
    scenario_repayment_variants,
    simulate,
)
from phase4a_lib import classify_gap, time_above_threshold_pct, worst_drawdown_recovery
from stress_regime_lib import (
    base_rate_days_in_stress,
    detect_stress_days,
    load_aligned_ohlcv,
    regime_conditional_cost,
    split_events_by_stress_window,
    stress_windows_from_days,
)
from transaction_cost_lib import total_transaction_cost, cost_adjusted_twr

HERE = Path(__file__).resolve().parent
PHASE3G_JSON = HERE / "docs" / "results" / "PHASE3_SENSITIVITY_RESULTS.json"
REPORT_PATH = HERE / "docs" / "STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.md"
JSON_PATH = HERE / "docs" / "results" / "STRESS_REGIME_EXECUTION_ASSUMPTIONS_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_APR = 0.05
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP = 1.8  # read-only reference, never varied or examined as a variable

REPAY_FRACTIONS = (0.10, 0.25, 0.50)
STRESS_TICKER = "QQQ"  # same regime-reference ticker convention as backtest_regime.py's REGIME_TICKER
TRAILING_WINDOW = 60
VOLATILITY_MULTIPLIER = 1.5
LIQUIDITY_FRACTION = 0.7
MIN_WINDOW_DAYS = 3
MERGE_GAP_DAYS = 5

BASE_COST_BPS = 15.0  # reuses the already-approved transaction-cost ceiling tier
STRESS_COST_MULTIPLIER = 3.0  # disclosed, new to this analysis

MATERIAL_THRESHOLD_PP = 2.0
NOISE_FLOOR_PP = 0.5
THRESHOLD_EXPOSURE_MATERIALITY_PCT = 5.0  # docs/PHASE4A_MATERIALITY_THRESHOLDS.md §6


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"

    stored = json.loads(PHASE3G_JSON.read_text())
    control_twr = stored["baseline_B_interest_5pct"]["ann_twr_pct"]
    control_maxdd = stored["baseline_B_interest_5pct"]["max_drawdown_pct"]

    def run(sc):
        return simulate(sc, weights, aligned, calendar, deposit_days,
                        deposit_amount=DEPOSIT_AMOUNT, min_lot=MIN_LOT)

    r_control = run(scenario_fixed_leverage(LEVERAGE_CAP, INTEREST_APR, INTEREST_FREE_AMOUNT, name="B"))
    assert abs(r_control.metrics()["ann_twr_pct"] - control_twr) < 1e-6, "control TWR diverged from stored Phase 3G value"
    print(f"Control (D-0/B) verified identical to stored Phase 3G value: {control_twr:.4f}% TWR")

    # ---- historical-primary: real stress-window detection ------------------
    ohlcv = load_aligned_ohlcv(STRESS_TICKER, calendar)
    stress_flags = detect_stress_days(
        ohlcv["h"], ohlcv["l"], ohlcv["c"], ohlcv["v"],
        trailing_window=TRAILING_WINDOW, volatility_multiplier=VOLATILITY_MULTIPLIER,
        liquidity_fraction=LIQUIDITY_FRACTION)
    windows = stress_windows_from_days(stress_flags, min_window_days=MIN_WINDOW_DAYS,
                                       merge_gap_days=MERGE_GAP_DAYS)
    base_rate_pct = base_rate_days_in_stress(windows, len(calendar))
    print(f"Detected {len(windows)} real stress window(s) from {STRESS_TICKER}'s OHLCV data "
         f"({base_rate_pct:.1f}% of {len(calendar)} simulated days)")

    results = {}
    for frac in REPAY_FRACTIONS:
        scs = scenario_repayment_variants(
            leverage_cap=LEVERAGE_CAP, interest_apr=INTEREST_APR,
            interest_free_amount=INTEREST_FREE_AMOUNT,
            model_b_cfg={"repay_fraction": frac})
        sc_b = next(s for s in scs if s.repayment_model_name == "MODEL_B")
        r = run(sc_b)

        stored_arm = stored["model_b_sensitivity"][f"{frac:.2f}"]
        gross_twr = r.metrics()["ann_twr_pct"]
        gross_maxdd = r.metrics()["max_drawdown_pct"]
        assert abs(gross_twr - stored_arm["ann_twr_pct"]) < 1e-6, (
            f"repay_fraction={frac} gross TWR diverged from stored Phase 3G value")
        n_events = sum(1 for e in r.events if e["kind"] == "repayment")
        assert n_events == stored_arm["event_stats"]["count"], (
            f"repay_fraction={frac} event count diverged from stored Phase 3G value")
        print(f"repay_fraction={frac:.0%} verified identical to stored Phase 3G value: "
             f"{gross_twr:.4f}% TWR, {n_events} events")

        # ---- historical-primary measurements (no cost/tax overlay) --------
        split = split_events_by_stress_window(r.events, windows)
        recov = worst_drawdown_recovery(r.book_values)
        leverage_exposure_pct = time_above_threshold_pct(r.leverage_series, LEVERAGE_CAP * 0.95)

        # ---- hypothetical-secondary: regime-conditional cost overlay, ------
        # kept strictly separate from historical-primary measurements above
        flat_cost = total_transaction_cost(r.events, BASE_COST_BPS)
        flat_net_twr = cost_adjusted_twr(r.book_values, r.flows, flat_cost)
        regime_cost = regime_conditional_cost(r.events, windows, BASE_COST_BPS, STRESS_COST_MULTIPLIER)
        regime_net_twr = cost_adjusted_twr(r.book_values, r.flows, regime_cost)

        results[frac] = {
            "repay_fraction": frac,
            "gross_ann_twr_pct": gross_twr,
            "gross_max_drawdown_pct": gross_maxdd,
            "n_repayment_events": n_events,
            "historical_primary": {
                "n_events_in_window": len(split.in_window),
                "n_events_outside_window": len(split.outside_window),
                "dollar_amount_in_window": split.in_window_amount,
                "dollar_amount_outside_window": split.outside_window_amount,
                "in_window_dollar_fraction_pct": split.in_window_dollar_fraction * 100.0,
                "base_rate_days_in_stress_pct": base_rate_pct,
                "turnover_concentration_over_or_under": (
                    "over-represented" if split.in_window_dollar_fraction * 100.0 > base_rate_pct
                    else "under-represented" if split.in_window_dollar_fraction * 100.0 < base_rate_pct
                    else "at base rate"),
                "recovery_trough_index": recov.trough_index,
                "recovery_index": recov.recovery_index,
                "recovery_days": recov.recovery_days,
                "leverage_time_above_95pct_of_cap_pct": leverage_exposure_pct,
                "leverage_exposure_material": leverage_exposure_pct >= THRESHOLD_EXPOSURE_MATERIALITY_PCT,
            },
            "hypothetical_secondary": {
                "base_bps": BASE_COST_BPS,
                "stress_multiplier": STRESS_COST_MULTIPLIER,
                "flat_cost_dollars": flat_cost,
                "flat_net_twr_pct": flat_net_twr,
                "regime_conditional_cost_dollars": regime_cost,
                "regime_conditional_net_twr_pct": regime_net_twr,
                "cost_delta_from_regime_conditioning": regime_cost - flat_cost,
                "gap_vs_control_flat_pp": flat_net_twr - control_twr,
                "gap_vs_control_regime_pp": regime_net_twr - control_twr,
                "gap_vs_control_flat_class": classify_gap(flat_net_twr - control_twr, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
                "gap_vs_control_regime_class": classify_gap(regime_net_twr - control_twr, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
            },
        }

    write_outputs(window, len(calendar), windows, base_rate_pct, control_twr, control_maxdd, results)


def write_outputs(window, n_days, windows, base_rate_pct, control_twr, control_maxdd, results):
    RESULTS_DIR = JSON_PATH.parent
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history or real "
                       "market liquidity conditions. Stress windows are detected "
                       "from real, already-cached OHLCV data as a volatility/"
                       "liquidity PROXY, never a measurement of actual bid-ask "
                       "spread or market depth. Execution is assumed to fill "
                       "instantly at each day's close, calm or stressed -- this "
                       "analysis does not model or resolve execution failure. The "
                       "hypothetical-secondary cost multiplier is a disclosed, "
                       "bounded assumption, kept strictly separate from the "
                       "historical-primary (assumption-free) measurements. See "
                       "docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "n_simulated_days": n_days,
        "stress_detection": {
            "reference_ticker": STRESS_TICKER,
            "method": "real OHLCV volatility/liquidity proxy, not measured spread/depth",
            "trailing_window_days": TRAILING_WINDOW,
            "volatility_multiplier": VOLATILITY_MULTIPLIER,
            "liquidity_fraction": LIQUIDITY_FRACTION,
            "min_window_days": MIN_WINDOW_DAYS,
            "merge_gap_days": MERGE_GAP_DAYS,
            "n_windows_detected": len(windows),
            "windows_day_index_ranges": windows,
            "base_rate_days_in_stress_pct": base_rate_pct,
        },
        "control_ann_twr_pct": control_twr,
        "control_max_drawdown_pct": control_maxdd,
        "materiality": {
            "material_threshold_pp": MATERIAL_THRESHOLD_PP,
            "noise_floor_pp": NOISE_FLOOR_PP,
            "threshold_exposure_materiality_pct": THRESHOLD_EXPOSURE_MATERIALITY_PCT,
            "outcome_gate": "adopted future gate: material gap AND (repeated forced-deleveraging events OR material threshold-exposure degradation), per docs/PHASE4A_OUTCOME_GATE_REVIEW.md adoption",
        },
        "results": {f"{frac:.2f}": r for frac, r in results.items()},
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    L = []
    L.append("# Stress-Regime Execution Assumptions — Results")
    L.append("")
    L.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
             "history or real market liquidity conditions. Stress windows below "
             "are detected from real, already-cached OHLCV data as a "
             "volatility/liquidity **proxy** — never a measurement of actual "
             "bid-ask spread or market depth. Execution is assumed to fill "
             "instantly at each day's close, calm or stressed; this analysis "
             "does not model or resolve execution failure. The hypothetical-"
             "secondary cost multiplier is a disclosed, bounded assumption, kept "
             "**strictly separate** from the historical-primary "
             "(assumption-free) measurements below. See "
             "`docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md` for the "
             "pre-approved design this run follows, and "
             "`docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.")
    L.append("")
    L.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}. Window: {window} "
             f"({n_days} simulated trading days). Control (no repayment, MODEL_0, "
             f"1.8x leverage — read-only reference, not examined or changed): "
             f"**{control_twr:.2f}% ann. TWR, {control_maxdd:.2f}% MaxDD** — "
             "verified identical to the stored `docs/results/"
             "PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. "
             "Each `repay_fraction` arm's gross figures were likewise verified "
             "identical to that stored file before any stress-regime analysis "
             "was applied._")
    L.append("")
    L.append(f"**Stress-window detection** (reference: {STRESS_TICKER}'s real OHLCV data, "
             f"{TRAILING_WINDOW}-day trailing baseline, {VOLATILITY_MULTIPLIER}x range or "
             f"{LIQUIDITY_FRACTION}x volume threshold, windows ≥{MIN_WINDOW_DAYS} days, "
             f"merged within {MERGE_GAP_DAYS} days): **{len(windows)} window(s) detected**, "
             f"covering **{base_rate_pct:.1f}%** of the {n_days} simulated trading days. "
             "All parameters are disclosed session choices, not separately "
             "pre-negotiated values.")
    L.append("")

    for frac, r in results.items():
        hp = r["historical_primary"]
        hs = r["hypothetical_secondary"]
        L.append(f"## repay_fraction = {frac:.0%}")
        L.append("")
        L.append(f"**Gross Model B result**: {r['gross_ann_twr_pct']:.2f}% ann. TWR, "
                 f"{r['gross_max_drawdown_pct']:.2f}% MaxDD, {r['n_repayment_events']} "
                 "repayment events.")
        L.append("")
        L.append("### Historical-primary (real stress windows, no cost/tax assumption)")
        L.append("")
        L.append(f"- **Repayment events during/near stress windows**: {hp['n_events_in_window']} "
                 f"inside detected stress windows, {hp['n_events_outside_window']} outside.")
        L.append(f"- **Turnover concentration**: {hp['in_window_dollar_fraction_pct']:.1f}% of "
                 f"repaid dollars occurred inside stress windows, versus a base rate of "
                 f"{hp['base_rate_days_in_stress_pct']:.1f}% of all simulated days being "
                 f"stress-flagged — repayment dollar volume is **{hp['turnover_concentration_over_or_under']}** "
                 "relative to how much of the calendar stress periods occupy.")
        L.append(f"- **Recovery time**: {hp['recovery_days'] if hp['recovery_days'] is not None else 'never recovered within the window'} "
                 f"trading days (trough at simulated day {hp['recovery_trough_index']}).")
        L.append(f"- **Drawdown impact**: {r['gross_max_drawdown_pct']:.2f}% MaxDD (gross, unchanged "
                 "by this analysis — see `docs/results/PHASE3_MODEL_B_ANALYSIS.md` for the "
                 "already-published figure this reproduces).")
        L.append(f"- **Threshold exposure**: {hp['leverage_time_above_95pct_of_cap_pct']:.1f}% of "
                 f"simulated days spent above 95% of the 1.8x leverage cap — "
                 f"{'material' if hp['leverage_exposure_material'] else 'not material'} per the "
                 f"{THRESHOLD_EXPOSURE_MATERIALITY_PCT:.0f}%-of-days bar.")
        L.append("")
        L.append("### Hypothetical-secondary (disclosed regime-conditional cost overlay)")
        L.append("")
        L.append(f"Base rate: {hs['base_bps']:.0f}bps (reused from the already-approved "
                 f"transaction-cost tier). Stress multiplier: {hs['stress_multiplier']:.1f}x, "
                 "applied only to events falling inside a detected stress window "
                 "(disclosed, new to this analysis, not a validated real-world value).")
        L.append("")
        L.append("| | Cost | Net TWR | Gap vs. control | Classification |")
        L.append("|---|---:|---:|---:|---|")
        L.append(f"| Flat {hs['base_bps']:.0f}bps (no regime conditioning) | "
                 f"${hs['flat_cost_dollars']:,.2f} | {hs['flat_net_twr_pct']:.2f}% | "
                 f"{hs['gap_vs_control_flat_pp']:+.2f}pp | {hs['gap_vs_control_flat_class']} |")
        L.append(f"| Regime-conditional ({hs['stress_multiplier']:.0f}x inside stress windows) | "
                 f"${hs['regime_conditional_cost_dollars']:,.2f} | "
                 f"{hs['regime_conditional_net_twr_pct']:.2f}% | "
                 f"{hs['gap_vs_control_regime_pp']:+.2f}pp | {hs['gap_vs_control_regime_class']} |")
        L.append("")
        L.append(f"Cost delta from regime conditioning: ${r['hypothetical_secondary']['cost_delta_from_regime_conditioning']:,.2f} "
                 "(the additional hypothetical cost attributable to elevating the rate "
                 "specifically for in-window events, versus the flat-rate baseline).")
        L.append("")

    L.append("## Materiality and outcome gate")
    L.append("")
    L.append("Reused, not reinvented: 2.0pp material / 0.5pp noise floor, "
             f"{THRESHOLD_EXPOSURE_MATERIALITY_PCT:.0f}%-of-days threshold-exposure bar "
             "(`docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3/§6), and the **adopted "
             "future outcome gate** (material gap AND (repeated forced-deleveraging "
             "events OR material threshold-exposure degradation), per "
             "`docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adoption) — this research cycle "
             "is exactly the future cycle that adoption was written for. No new "
             "threshold was introduced or optimized by this analysis.")
    L.append("")

    L.append("## What this analysis does not resolve")
    L.append("")
    L.append("- **Not measured liquidity data** — the stress-window detector uses real "
             "OHLCV range/volume as a proxy; no bid-ask spread or market-depth data "
             "exists anywhere in this repo.")
    L.append("- **Not a model of execution failure** — every trade in every scenario, "
             "calm or stressed, is assumed to fill instantly at that day's close.")
    L.append("- **Not a validated regime-conditional cost multiplier** — the "
             f"{STRESS_COST_MULTIPLIER:.0f}x figure is a disclosed, bounded Hypothetical "
             "assumption specific to this analysis, not a measured or expected "
             "real-world value.")
    L.append("- **No repayment fraction selected, no implementation recommended, no "
             "doctrine changed, no leverage cap examined or changed, no threshold "
             "optimized** — per `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md` §6.")
    L.append("")
    L.append("_Advisory-adjacent research only. This report places no orders and "
             "makes no recommendation. Execute nothing based on this document "
             "alone._")

    REPORT_PATH.write_text("\n".join(L) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")


if __name__ == "__main__":
    main()
