#!/usr/bin/env python3
"""
run_phase3g_sensitivity.py — Phase 3G sensitivity-testing execution
driver, per docs/PHASE3_SENSITIVITY_PLAN.md.

Runs the 10 arms that plan specifies (3 Model B repay_fraction values,
4 Model C drawdown_trigger_pct values, 3 interest_apr values), each
varying exactly one parameter against the shared Phase 3E baseline
configuration. Does not modify margin_simulation.py, allocate.py,
targets.yaml, or holdings.yaml. Does not modify or overwrite Phase 3E's
existing docs/results/PHASE3_SCENARIO_RESULTS.md or
phase3_scenario_results.json — this script writes to different files
(docs/PHASE3_SENSITIVITY_RESULTS.md, docs/results/
PHASE3_SENSITIVITY_RESULTS.json).

Three arms (Model B @ 25%, Model C @ 15%, interest @ 5%) are identical
in configuration to Phase 3E runs already approved and recorded. This
script recomputes them (the harness is deterministic, so this is a
verification, not new evidence) and asserts the recomputed values match
the stored Phase 3E JSON exactly, rather than silently trusting they
would. If they ever diverge, that is a determinism bug to report, not a
sensitivity finding — see the assertions in main().

Run:  python3 run_phase3g_sensitivity.py
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from margin_simulation import (
    HYPOTHETICAL_LABEL,
    ModelBProfitHarvest,
    ModelCRiskReset,
    load_real_aligned_data,
    scenario_fixed_leverage,
    scenario_unlevered,
    simulate,
)
from phase3g_lib import (
    ModelCTriggerLogger,
    estimate_turnover,
    event_amount_stats,
    gap_vs_baseline,
    twr_maxdd_ratio,
)

HERE = Path(__file__).resolve().parent
PHASE3E_JSON = HERE / "docs" / "results" / "phase3_scenario_results.json"
REPORT_PATH = HERE / "docs" / "PHASE3_SENSITIVITY_RESULTS.md"
JSON_PATH = HERE / "docs" / "results" / "PHASE3_SENSITIVITY_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP = 1.8
DECISION_THRESHOLD_PP = 2.0  # same bar Scenario D used, restated here per the plan

EXPECTED_COMMIT_AT_PLAN_TIME = "dd0941aa7a12dbabbfdb437a71fbf322b598f916"  # PHASE3_SENSITIVITY_PLAN.md commit


def _to_scenario_config_b(repay_fraction, weights, aligned, calendar, deposit_days):
    """One-off ScenarioConfig for a given Model B repay_fraction, mirroring
    scenario_repayment_variants()'s D-B construction exactly but built
    directly (that function always also includes a D-0 control, which
    this driver runs separately/once instead of once per repay_fraction)."""
    from margin_simulation import ScenarioConfig, repayment_model_0
    return ScenarioConfig(
        name=f"B-repay-{repay_fraction:.2f}", leverage_cap=LEVERAGE_CAP,
        interest_apr=0.05, interest_free_amount=INTEREST_FREE_AMOUNT,
        repayment_fn=repayment_model_0,
        pre_trade_fn=ModelBProfitHarvest(repay_fraction=repay_fraction),
        repayment_model_name="MODEL_B")


def _to_scenario_config_c(drawdown_trigger_pct, logger_holder):
    from margin_simulation import ScenarioConfig, repayment_model_0
    inner = ModelCRiskReset(drawdown_trigger_pct=drawdown_trigger_pct, reset_leverage=1.25)
    logger = ModelCTriggerLogger(inner=inner)
    logger_holder.append(logger)
    return ScenarioConfig(
        name=f"C-trigger-{drawdown_trigger_pct:g}pct", leverage_cap=LEVERAGE_CAP,
        interest_apr=0.05, interest_free_amount=INTEREST_FREE_AMOUNT,
        repayment_fn=repayment_model_0, pre_trade_fn=logger,
        repayment_model_name="MODEL_C")


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"
    n_deposits = len(deposit_days)

    def run(sc):
        return simulate(sc, weights, aligned, calendar, deposit_days,
                        deposit_amount=DEPOSIT_AMOUNT, min_lot=MIN_LOT)

    # ---- baselines (recomputed, verified against Phase 3E's stored JSON) --
    phase3e = json.loads(PHASE3E_JSON.read_text())

    r_a = run(scenario_unlevered(name="A"))
    assert r_a.metrics()["ann_twr_pct"] == pytest_approx_or_raise(
        phase3e["results"]["A"]["ann_twr_pct"], r_a.metrics()["ann_twr_pct"], "Scenario A")

    r_b0 = run(scenario_fixed_leverage(LEVERAGE_CAP, 0.05, INTEREST_FREE_AMOUNT, name="B"))
    assert r_b0.metrics()["ann_twr_pct"] == pytest_approx_or_raise(
        phase3e["results"]["B"]["ann_twr_pct"], r_b0.metrics()["ann_twr_pct"], "Scenario B (interest=5%, no repayment)")

    print(f"Baselines verified identical to Phase 3E: A={r_a.metrics()['ann_twr_pct']:.4f}%, "
          f"B={r_b0.metrics()['ann_twr_pct']:.4f}%")

    # ---- 1. Model B repay_fraction sensitivity -----------------------------
    model_b_arms = {}
    for frac in (0.10, 0.25, 0.50):
        sc = _to_scenario_config_b(frac, weights, aligned, calendar, deposit_days)
        r = run(sc)
        model_b_arms[frac] = r
        if frac == 0.25:
            stored = phase3e["results"]["D-MODEL_B"]["ann_twr_pct"]
            assert abs(r.metrics()["ann_twr_pct"] - stored) < 1e-6, (
                f"Model B 25% arm diverged from Phase 3E's stored D-MODEL_B result: "
                f"{r.metrics()['ann_twr_pct']} vs {stored}")
            print(f"Model B 25% arm verified identical to Phase 3E D-MODEL_B: "
                  f"{r.metrics()['ann_twr_pct']:.4f}%")

    # ---- 2. Model C drawdown_trigger_pct sensitivity -----------------------
    model_c_arms = {}
    model_c_loggers = {}
    for trig in (10.0, 12.5, 15.0, 20.0):
        holder = []
        sc = _to_scenario_config_c(trig, holder)
        r = run(sc)
        model_c_arms[trig] = r
        model_c_loggers[trig] = holder[0]
        if trig == 15.0:
            stored = phase3e["results"]["D-MODEL_C"]["ann_twr_pct"]
            assert abs(r.metrics()["ann_twr_pct"] - stored) < 1e-6, (
                f"Model C 15% arm diverged from Phase 3E's stored D-MODEL_C result: "
                f"{r.metrics()['ann_twr_pct']} vs {stored}")
            n_repay_events = sum(1 for e in r.events if e["kind"] == "repayment")
            stored_n_events = phase3e["results"]["D-MODEL_C"]["n_repayment_events"]
            assert n_repay_events == stored_n_events == 0, (
                f"Model C 15% arm's repayment-event count diverged from Phase "
                f"3E's stored D-MODEL_C result: {n_repay_events} vs {stored_n_events}")
            # Note: n_activations can be > 0 with 0 repayment events -- a
            # trigger can fire and find leverage already at/below the reset
            # target (see test_model_c_no_repay_needed_if_already_under_
            # target_after_crash in test_margin_simulation.py), which is
            # valid, tested behavior, not a contradiction. The TWR/debt
            # equality assert above is the real verification; activation
            # count is reported for information, not asserted against
            # Phase 3E (which never logged activation counts, only events).
            print(f"Model C 15% arm verified identical to Phase 3E D-MODEL_C: "
                  f"{r.metrics()['ann_twr_pct']:.4f}%, "
                  f"{holder[0].n_activations} trigger activation(s), "
                  f"0 repayment events (matches Phase 3E)")

    # ---- 3. Interest rate sensitivity --------------------------------------
    interest_arms = {}
    for apr in (0.0, 0.05, 0.08):
        sc = scenario_fixed_leverage(LEVERAGE_CAP, apr, INTEREST_FREE_AMOUNT, name=f"B-interest-{apr:.2f}")
        r = run(sc)
        interest_arms[apr] = r
        if apr == 0.05:
            assert abs(r.metrics()["ann_twr_pct"] - r_b0.metrics()["ann_twr_pct"]) < 1e-9
            print(f"Interest 5% arm verified identical to this run's own B baseline "
                  f"(same config): {r.metrics()['ann_twr_pct']:.4f}%")

    write_outputs(window, n_deposits, r_a, r_b0, model_b_arms, model_c_arms,
                 model_c_loggers, interest_arms)


def pytest_approx_or_raise(expected, actual, label):
    if abs(expected - actual) > 1e-6:
        raise AssertionError(f"{label} diverged from Phase 3E's stored result: "
                            f"{actual} vs {expected}")
    return actual


def write_outputs(window, n_deposits, r_a, r_b0, model_b_arms, model_c_arms,
                  model_c_loggers, interest_arms):
    total_deposited = DEPOSIT_AMOUNT * n_deposits
    baseline_twr = r_b0.metrics()["ann_twr_pct"]
    baseline_maxdd = r_b0.metrics()["max_drawdown_pct"]

    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history. Every "
                       "arm is a hypothetical simulation of a synthetic "
                       "$0-start account through real historical prices. No "
                       "parameter was tuned after seeing results; no winner "
                       "was chosen. See docs/PHASE3_SENSITIVITY_PLAN.md and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "n_deposits": n_deposits,
        "baseline_A": r_a.metrics(),
        "baseline_B_interest_5pct": r_b0.metrics(),
        "model_b_sensitivity": {},
        "model_c_sensitivity": {},
        "interest_sensitivity": {},
    }

    lines = []
    lines.append("# Phase 3G Sensitivity Results")
    lines.append("")
    lines.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's "
                 "real history. Every arm below is a hypothetical simulation of "
                 "a synthetic $0-start account through real historical prices. "
                 "No parameter was tuned after seeing results; no arm is "
                 "presented as a winner. See `docs/PHASE3_SENSITIVITY_PLAN.md` "
                 "for the pre-committed design this run follows exactly, and "
                 "`docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.")
    lines.append("")
    lines.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}, per "
                 "`docs/PHASE3_SENSITIVITY_PLAN.md`. Window: {window}. "
                 f"{n_deposits} monthly ${DEPOSIT_AMOUNT:,.0f} deposits "
                 f"(${total_deposited:,.0f} total). Baselines (Scenario A "
                 "unlevered, Scenario B 1.8x/5% interest/no repayment) "
                 "recomputed and verified identical to the stored Phase 3E "
                 "results before any sensitivity arm ran — see "
                 "`run_phase3g_sensitivity.py`'s assertions. Phase 3E's own "
                 "result files "
                 "(`docs/results/PHASE3_SCENARIO_RESULTS.md`, "
                 "`docs/results/phase3_scenario_results.json`) were not "
                 "modified or overwritten by this run._".replace("{window}", window))
    lines.append("")
    lines.append(f"**Baseline for comparison — Scenario B (1.8x leverage, 5% "
                 f"interest, no repayment): {baseline_twr:.2f}% ann. TWR, "
                 f"{baseline_maxdd:.2f}% MaxDD.**")
    lines.append("")

    # ---- Section 1: Model B ------------------------------------------------
    lines.append("## 1. Model B (Profit Harvest) repay_fraction sensitivity")
    lines.append("")
    lines.append("**Parameters changed:** `repay_fraction` ∈ {10%, 25%, 50%}.")
    lines.append(f"**Parameters held constant:** leverage_cap={LEVERAGE_CAP}, "
                 f"interest_apr=5.00%, interest_free_amount=${INTEREST_FREE_AMOUNT:,.0f}, "
                 "Model C inactive, universe/window/deposits/weights/trim rule "
                 "as shared config (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`).")
    lines.append("")
    lines.append("| repay_fraction | Ann. TWR | Gap vs baseline | CAGR | MaxDD | Gap vs baseline | Ann. Vol | Final debt | n_events | Total repaid | Turnover est. | TWR/\\|MaxDD\\| |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for frac in (0.10, 0.25, 0.50):
        r = model_b_arms[frac]
        m = r.metrics()
        stats = event_amount_stats(r.events, "repayment")
        turnover = estimate_turnover(stats["total"], total_deposited)
        ratio = twr_maxdd_ratio(m["ann_twr_pct"], m["max_drawdown_pct"])
        ratio_str = f"{ratio:.3f}" if ratio is not None else "n/a"
        twr_gap = gap_vs_baseline(m["ann_twr_pct"], baseline_twr)
        dd_gap = gap_vs_baseline(m["max_drawdown_pct"], baseline_maxdd)
        lines.append(f"| {frac*100:.0f}% | {m['ann_twr_pct']:.2f}% | {twr_gap:+.2f}pp | "
                     f"{m['cagr_pct']:.2f}% | {m['max_drawdown_pct']:.2f}% | {dd_gap:+.2f}pp | "
                     f"{m['annualized_volatility_pct']:.2f}% | ${m['final_margin_debt']:,.0f} | "
                     f"{stats['count']} | ${stats['total']:,.0f} | {turnover*100:.1f}% | "
                     f"{ratio_str} |")
        payload["model_b_sensitivity"][f"{frac:.2f}"] = {
            **m, "event_stats": stats, "turnover_estimate": turnover,
            "twr_maxdd_ratio": ratio, "twr_gap_vs_baseline_pp": twr_gap,
            "maxdd_gap_vs_baseline_pp": dd_gap,
        }
    lines.append("")
    twr_25 = model_b_arms[0.25].metrics()["ann_twr_pct"]
    twr_10 = model_b_arms[0.10].metrics()["ann_twr_pct"]
    twr_50 = model_b_arms[0.50].metrics()["ann_twr_pct"]
    monotonic = (twr_10 >= twr_25 >= twr_50) or (twr_10 <= twr_25 <= twr_50)
    lines.append(f"**Monotonicity check:** TWR at 10%/25%/50% = {twr_10:.2f}% / "
                 f"{twr_25:.2f}% / {twr_50:.2f}% — "
                 f"{'monotonic' if monotonic else 'NOT monotonic (flagged for investigation, not for picking a favorite)'} "
                 "across the sweep.")
    lines.append("")
    lines.append("**Limitations:** turnover is an upper-bound estimate (the "
                 "harness doesn't log the cash-vs-trim funding split per "
                 "event, per `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4). "
                 "No transaction-cost or tax model exists anywhere in this "
                 "repo to price that turnover.")
    lines.append("")

    # ---- Section 2: Model C ------------------------------------------------
    lines.append("## 2. Model C (Risk Reset) drawdown_trigger_pct sensitivity")
    lines.append("")
    lines.append("**Parameters changed:** `drawdown_trigger_pct` ∈ {10%, 12.5%, 15%, 20%}.")
    lines.append(f"**Parameters held constant:** `reset_leverage`=1.25 (fixed), "
                 f"leverage_cap={LEVERAGE_CAP}, interest_apr=5.00%, "
                 f"interest_free_amount=${INTEREST_FREE_AMOUNT:,.0f}, Model B inactive, "
                 "shared config as above.")
    lines.append("")
    lines.append("| drawdown_trigger_pct | n_reset_activations | n_repayment_events | Ann. TWR | Gap vs baseline | MaxDD | Gap vs baseline | Final debt | Days effective_cap tightened |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for trig in (10.0, 12.5, 15.0, 20.0):
        r = model_c_arms[trig]
        logger = model_c_loggers[trig]
        m = r.metrics()
        stats = event_amount_stats(r.events, "repayment")
        twr_gap = gap_vs_baseline(m["ann_twr_pct"], baseline_twr)
        dd_gap = gap_vs_baseline(m["max_drawdown_pct"], baseline_maxdd)
        days_tightened = sum(1 for lv in r.leverage_series if lv is not None and lv <= 1.25 + 0.05)
        lines.append(f"| {trig:g}% | {logger.n_activations} | {stats['count']} | "
                     f"{m['ann_twr_pct']:.2f}% | {twr_gap:+.2f}pp | {m['max_drawdown_pct']:.2f}% | "
                     f"{dd_gap:+.2f}pp | ${m['final_margin_debt']:,.0f} | {days_tightened} |")
        payload["model_c_sensitivity"][f"{trig:g}"] = {
            **m, "n_reset_activations": logger.n_activations,
            "activation_days": logger.activation_days, "event_stats": stats,
            "twr_gap_vs_baseline_pp": twr_gap, "maxdd_gap_vs_baseline_pp": dd_gap,
        }
    lines.append("")
    n_fired = {trig: model_c_loggers[trig].n_activations for trig in (10.0, 12.5, 15.0, 20.0)}
    any_fired = any(v > 0 for v in n_fired.values())
    lines.append(f"**Trigger-firing summary:** "
                 + ("; ".join(f"{trig:g}% fired {n} time(s)" for trig, n in n_fired.items()) + "."))
    if not any_fired:
        lines.append("")
        lines.append("**No threshold in this sweep fired.** This simulated, "
                     "diversified 63-ticker portfolio's net equity never drew "
                     "down more than 20% from its own peak in this window — "
                     "consistent with, and now extending, Phase 3E's finding "
                     "that even 15% didn't fire (`docs/PHASE3_FINDINGS.md` §6). "
                     "This is a statement about this window's character (one "
                     "mostly-rising sample, per the standing caveat), not "
                     "evidence Model C's mechanism doesn't work — see "
                     "`test_margin_simulation.py`'s unit and property tests "
                     "for direct proof the mechanism activates and deleverages "
                     "correctly on inputs engineered to trigger it.")
    lines.append("")
    lines.append("**Limitations:** `reset_leverage` (1.25x) was held fixed — "
                 "this sweep does not test whether a different reset target "
                 "changes trigger sensitivity (it structurally can't, since "
                 "the drawdown TRIGGER and the reset TARGET are independent "
                 "parameters in the implementation). \"Days effective_cap "
                 "tightened\" approximates days spent at/near the reset target "
                 "via a leverage-series proxy, not a direct read of "
                 "`reset_active` state (the driver's `ModelCTriggerLogger` "
                 "tracks activation days only, not full-duration active "
                 "windows — a possible future refinement, not done here).")
    lines.append("")

    # ---- Section 3: Interest ------------------------------------------------
    lines.append("## 3. Interest rate sensitivity")
    lines.append("")
    lines.append("**Parameters changed:** `interest_apr` ∈ {0%, 5%, 8%}.")
    lines.append(f"**Parameters held constant:** leverage_cap={LEVERAGE_CAP}, "
                 f"interest_free_amount=${INTEREST_FREE_AMOUNT:,.0f}, repayment=MODEL_0 "
                 "(no repayment model active — isolates the interest-cost effect), "
                 "shared config as above. Compared against Scenario A (unlevered), "
                 "which is invariant to interest_apr since it never carries debt.")
    lines.append("")
    lines.append("| interest_apr | Scenario A TWR | Levered TWR | A-vs-B TWR gap | A-vs-B MaxDD gap | Cumulative interest accrued | Final debt |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|")
    a_twr = r_a.metrics()["ann_twr_pct"]
    a_maxdd = r_a.metrics()["max_drawdown_pct"]
    for apr in (0.0, 0.05, 0.08):
        r = interest_arms[apr]
        m = r.metrics()
        interest_stats = event_amount_stats(r.events, "interest_accrual")
        twr_gap = gap_vs_baseline(m["ann_twr_pct"], a_twr)
        dd_gap = gap_vs_baseline(m["max_drawdown_pct"], a_maxdd)
        lines.append(f"| {apr*100:.0f}% | {a_twr:.2f}% | {m['ann_twr_pct']:.2f}% | "
                     f"{twr_gap:+.2f}pp | {dd_gap:+.2f}pp | ${interest_stats['total']:,.0f} | "
                     f"${m['final_margin_debt']:,.0f} |")
        payload["interest_sensitivity"][f"{apr:.2f}"] = {
            **m, "interest_accrued_total": interest_stats["total"],
            "twr_gap_vs_A_pp": twr_gap, "maxdd_gap_vs_A_pp": dd_gap,
        }
    lines.append("")
    gaps = {apr: gap_vs_baseline(interest_arms[apr].metrics()["ann_twr_pct"], a_twr)
           for apr in (0.0, 0.05, 0.08)}
    direction_holds = all(g > 0 for g in gaps.values())
    lines.append(f"**Direction check:** the levered account beat the unlevered "
                 f"baseline on TWR at all three rates "
                 f"({', '.join(f'{apr*100:.0f}%: {g:+.2f}pp' for apr, g in gaps.items())})"
                 f" — {'the direction holds across the full tested range.' if direction_holds else 'the direction REVERSES at the higher rate(s) — reported plainly, not discarded as unrealistic.'}")
    lines.append("")
    lines.append("**Limitations:** 0% is a decomposition tool (isolating pure "
                 "leverage mechanics from financing cost), not a claim about "
                 "real financing terms. The 5% arm remains the primary "
                 "reference point (Estimated doctrine, not derived from this "
                 "sweep). This dimension does not test any interaction between "
                 "interest cost and Model B/C's triggers (a combined dimension, "
                 "explicitly out of scope per `docs/PHASE3_SENSITIVITY_PLAN.md`).")
    lines.append("")

    # ---- Interpretation rules (restated) ------------------------------------
    lines.append("## Interpretation rules (restated, applied throughout)")
    lines.append("")
    lines.append("- **No winner was chosen.** Every table above reports all "
                 "arms in full; none is marked \"recommended\" or \"best.\"")
    lines.append("- **No parameter was tuned after seeing results.** All nine "
                 "sweep values (plus the two baselines) were fixed in "
                 "`docs/PHASE3_SENSITIVITY_PLAN.md` before this run.")
    lines.append("- **No claim of future superiority is made.** Every finding "
                 "above describes this one simulated window only.")
    lines.append("- **No simulated result has been converted into doctrine.** "
                 "`targets.yaml`'s margin schema remains entirely absent; "
                 "`CLAUDE.md`'s Decisions Log is unchanged by this document.")
    lines.append("")
    lines.append("_Advisory-adjacent research only. This report places no "
                 "orders and makes no recommendation. Execute nothing based "
                 "on this document alone._")

    REPORT_PATH.write_text("\n".join(lines) + "\n")
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")


if __name__ == "__main__":
    main()
