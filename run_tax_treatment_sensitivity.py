#!/usr/bin/env python3
"""
run_tax_treatment_sensitivity.py — tax treatment sensitivity analysis
driver, per docs/TAX_TREATMENT_SENSITIVITY_PLAN.md.

Re-runs the three already-approved Model B repay_fraction arms
(10%/25%/50%) through the UNMODIFIED margin_simulation.py/phase3g
scenario builders, verifies each arm's headline numbers match the
stored docs/results/PHASE3_SENSITIVITY_RESULTS.json before applying any
tax assumption (same "verify identical before proceeding" discipline as
run_transaction_cost_sensitivity.py), then applies a disclosed,
UPPER-BOUND tax assumption: 100% of each repayment event's dollar
amount treated as realized gain (never converted into an estimate),
under three rate tiers (0%/15%/32%) crossed with a holding-period
bracket (all-long-term at 15%, all-short-term at 32% -- brackets the
unknowable true short/long-term mix rather than guessing a blend).

No engine change. No cost-basis tracking added. No repay_fraction is
selected or recommended -- see docs/TAX_TREATMENT_SENSITIVITY_PLAN.md
§8/§9 for the full allowed/prohibited conclusions list this script's
output must respect.

Run:  python3 run_tax_treatment_sensitivity.py
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
from phase4a_lib import classify_gap
from tax_treatment_lib import net_twr_after_tax, tax_drag, taxable_realization_upper_bound

HERE = Path(__file__).resolve().parent
PHASE3G_JSON = HERE / "docs" / "results" / "PHASE3_SENSITIVITY_RESULTS.json"
REPORT_PATH = HERE / "docs" / "TAX_TREATMENT_SENSITIVITY_RESULTS.md"
JSON_PATH = HERE / "docs" / "results" / "TAX_TREATMENT_SENSITIVITY_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_APR = 0.05
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP = 1.8

REPAY_FRACTIONS = (0.10, 0.25, 0.50)
TAX_RATE_TIERS_PCT = (0.0, 15.0, 32.0)  # T0 / T1 (illustrative LTCG) / T2 (illustrative ordinary income)
MATERIAL_THRESHOLD_PP = 2.0
NOISE_FLOOR_PP = 0.5

# Holding-period brackets: which tax-rate tier each bracket case uses.
# Brackets the unknowable true short/long-term mix rather than guessing
# a blend, per docs/TAX_TREATMENT_SENSITIVITY_PLAN.md §6.
HOLDING_PERIOD_CASES = {
    "all_long_term": 15.0,
    "all_short_term": 32.0,
}


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"
    n_deposits = len(deposit_days)

    stored = json.loads(PHASE3G_JSON.read_text())
    control_twr = stored["baseline_B_interest_5pct"]["ann_twr_pct"]
    control_maxdd = stored["baseline_B_interest_5pct"]["max_drawdown_pct"]

    def run(sc):
        return simulate(sc, weights, aligned, calendar, deposit_days,
                        deposit_amount=DEPOSIT_AMOUNT, min_lot=MIN_LOT)

    # verify control baseline reproduces exactly before proceeding
    r_control = run(scenario_fixed_leverage(LEVERAGE_CAP, INTEREST_APR, INTEREST_FREE_AMOUNT, name="B"))
    assert abs(r_control.metrics()["ann_twr_pct"] - control_twr) < 1e-6, "control TWR diverged from stored Phase 3G value"
    print(f"Control (D-0/B) verified identical to stored Phase 3G value: {control_twr:.4f}% TWR")

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
            f"repay_fraction={frac} gross TWR diverged from stored Phase 3G value: "
            f"{gross_twr} vs {stored_arm['ann_twr_pct']}")
        n_events = sum(1 for e in r.events if e["kind"] == "repayment")
        assert n_events == stored_arm["event_stats"]["count"], (
            f"repay_fraction={frac} event count diverged from stored Phase 3G value")
        print(f"repay_fraction={frac:.0%} verified identical to stored Phase 3G value: "
             f"{gross_twr:.4f}% TWR, {n_events} events")

        # taxable realization applies ONLY to repayment-generated amounts --
        # deposits, interest accrual, and margin draws are excluded by
        # taxable_realization_upper_bound()'s own kind filter (default
        # "repayment"), never included.
        taxable_base = taxable_realization_upper_bound(r.events)
        assert abs(taxable_base - stored_arm["event_stats"]["total"]) < 1e-6, (
            f"repay_fraction={frac} taxable base diverged from stored Phase 3G "
            f"total_repaid: {taxable_base} vs {stored_arm['event_stats']['total']}")

        by_rate = {}
        for rate_pct in TAX_RATE_TIERS_PCT:
            drag = tax_drag(taxable_base, rate_pct / 100.0)
            net_twr = net_twr_after_tax(r.book_values, r.flows, drag)
            gap_vs_control_gross = gross_twr - control_twr
            gap_vs_control_net = net_twr - control_twr
            by_rate[rate_pct] = {
                "rate_pct": rate_pct,
                "rate_label": "Known (no tax, control)" if rate_pct == 0.0 else "Hypothetical (illustrative federal bracket)",
                "taxable_base_upper_bound": taxable_base,
                "tax_drag_dollars": drag,
                "gross_ann_twr_pct": gross_twr,
                "net_ann_twr_pct": net_twr,
                "twr_erosion_pp": gross_twr - net_twr,
                "gap_vs_control_gross_pp": gap_vs_control_gross,
                "gap_vs_control_net_pp": gap_vs_control_net,
                "gap_vs_control_gross_class": classify_gap(gap_vs_control_gross, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
                "gap_vs_control_net_class": classify_gap(gap_vs_control_net, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
            }

        by_holding_period = {}
        for case_name, rate_pct in HOLDING_PERIOD_CASES.items():
            by_holding_period[case_name] = by_rate[rate_pct]

        results[frac] = {
            "repay_fraction": frac,
            "gross_ann_twr_pct": gross_twr,
            "gross_max_drawdown_pct": gross_maxdd,
            "n_repayment_events": n_events,
            "taxable_base_upper_bound": taxable_base,
            "by_rate_tier": by_rate,
            "by_holding_period": by_holding_period,
        }

    write_outputs(window, n_deposits, control_twr, control_maxdd, results)


def write_outputs(window, n_deposits, control_twr, control_maxdd, results):
    RESULTS_DIR = JSON_PATH.parent
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history or real tax "
                       "liability. Every scenario is a hypothetical simulation of a "
                       "synthetic $0-start account through real historical prices. "
                       "The taxable-realization figure is a disclosed UPPER BOUND "
                       "(100% of each repayment event's dollar amount treated as "
                       "realized gain), never converted into an estimate of actual "
                       "realized gain or actual tax owed. The 15%/32% rate tiers are "
                       "disclosed Hypothetical, illustrative federal brackets, not "
                       "this account's confirmed rate. State tax is excluded, not "
                       "assumed zero. See docs/TAX_TREATMENT_SENSITIVITY_PLAN.md and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "n_deposits": n_deposits,
        "control_ann_twr_pct": control_twr,
        "control_max_drawdown_pct": control_maxdd,
        "tax_rate_tiers_pct": list(TAX_RATE_TIERS_PCT),
        "holding_period_cases": HOLDING_PERIOD_CASES,
        "material_threshold_pp": MATERIAL_THRESHOLD_PP,
        "noise_floor_pp": NOISE_FLOOR_PP,
        "results": {f"{frac:.2f}": r for frac, r in results.items()},
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    L = []
    L.append("# Tax Treatment Sensitivity Results")
    L.append("")
    L.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
             "history or real tax liability. Every figure below simulates a "
             "synthetic $0-start account through real historical prices. The "
             "taxable-realization figure is a disclosed **upper bound** (100% of "
             "each repayment event's dollar amount treated as realized gain), "
             "**never** converted into an estimate of actual realized gain or "
             "actual tax owed. The 15%/32% rate tiers are disclosed Hypothetical, "
             "illustrative federal brackets, not this account's confirmed rate. "
             "State tax is excluded, not assumed zero. See "
             "`docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` for the pre-approved design "
             "this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the full "
             "disclaimer.")
    L.append("")
    L.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}. Window: {window}. "
             f"{n_deposits} monthly ${DEPOSIT_AMOUNT:,.0f} deposits. Control (no "
             f"repayment, MODEL_0, 1.8x leverage): **{control_twr:.2f}% ann. TWR, "
             f"{control_maxdd:.2f}% MaxDD** — verified identical to the stored "
             "`docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this run "
             "proceeded. Each `repay_fraction` arm's gross figures were likewise "
             "verified identical to that stored file before any tax assumption was "
             "applied. Tax sensitivity is applied ONLY to repayment-generated "
             "realized amounts (`taxable_realization_upper_bound()`'s "
             "`kind=\"repayment\"` filter) — deposits, interest accrual, margin "
             "draws, and unrealized gains are explicitly excluded._")
    L.append("")

    for frac, r in results.items():
        L.append(f"## repay_fraction = {frac:.0%}")
        L.append("")
        L.append(f"1. **Gross Model B result**: {r['gross_ann_twr_pct']:.2f}% ann. TWR, "
                 f"{r['gross_max_drawdown_pct']:.2f}% MaxDD, {r['n_repayment_events']} "
                 "repayment events.")
        L.append(f"2. **Upper-bound taxable realization assumption**: "
                 f"${r['taxable_base_upper_bound']:,.2f} — 100% of every repayment "
                 "event's dollar amount, treated as realized gain. This is a ceiling, "
                 "not an estimate of actual realized gain (no cost-basis tracking "
                 "exists in this harness, and none was added to produce this figure).")
        L.append("")
        L.append("| Rate tier | Label | 3. Assumed tax drag | Net TWR | Gap vs. control (gross) | Gap vs. control (net) |")
        L.append("|---|---|---:|---:|---:|---:|")
        for rate_pct in TAX_RATE_TIERS_PCT:
            t = r["by_rate_tier"][rate_pct]
            L.append(f"| {rate_pct:.0f}% | {t['rate_label']} | ${t['tax_drag_dollars']:,.2f} "
                     f"({t['twr_erosion_pp']:.4f}pp) | 4. **{t['net_ann_twr_pct']:.2f}%** | "
                     f"{t['gap_vs_control_gross_pp']:+.2f}pp ({t['gap_vs_control_gross_class']}) | "
                     f"5. {t['gap_vs_control_net_pp']:+.2f}pp ({t['gap_vs_control_net_class']}) |")
        L.append("")
        L.append("**Holding-period bracket** (brackets the unknowable true short/"
                 "long-term mix rather than guessing a blend):")
        L.append("")
        L.append("| Case | Rate used | Net TWR | Gap vs. control (net) |")
        L.append("|---|---:|---:|---:|")
        for case_name, rate_pct in HOLDING_PERIOD_CASES.items():
            t = r["by_holding_period"][case_name]
            label = "All long-term (optimistic bound)" if case_name == "all_long_term" else "All short-term (pessimistic bound)"
            L.append(f"| {label} | {rate_pct:.0f}% | {t['net_ann_twr_pct']:.2f}% | "
                     f"{t['gap_vs_control_net_pp']:+.2f}pp ({t['gap_vs_control_net_class']}) |")
        L.append("")

    L.append("## Materiality comparison summary")
    L.append("")
    class_changed_any = False
    for frac in REPAY_FRACTIONS:
        gross_class = results[frac]["by_rate_tier"][0.0]["gap_vs_control_gross_class"]
        for rate_pct in TAX_RATE_TIERS_PCT:
            net_class = results[frac]["by_rate_tier"][rate_pct]["gap_vs_control_net_class"]
            if net_class != gross_class:
                class_changed_any = True
    L.append(f"Materiality classification (vs. control) changed at any tested "
             f"`repay_fraction` × tax-rate combination: **{class_changed_any}**. "
             "Per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`'s existing 2.0pp "
             "material / 0.5pp noise-floor bands, reused unchanged.")
    L.append("")

    L.append("## What this analysis does not resolve")
    L.append("")
    L.append("- **Not an estimate of actual tax owed** — every dollar figure above "
             "is derived from the 100%-of-trim upper-bound assumption (§2 in each "
             "arm's section), never from actual cost-basis or realized-gain data, "
             "because none exists in this harness and none was added to produce "
             "this analysis (`docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` §3/§5's "
             "explicit \"no cost-basis tracking\" constraint).")
    L.append("- **Not this account's actual tax rate or jurisdiction** — 15%/32% "
             "are illustrative federal brackets only; state tax is excluded "
             "entirely, not modeled as zero.")
    L.append("- **Not the true short/long-term mix** — bracketed by two extremes "
             "(all-LT, all-ST), not estimated as a blend, because the true mix is "
             "unknowable from this harness's data.")
    L.append("- **No repayment policy conclusion** — this analysis does not select, "
             "rank, or recommend any `repay_fraction`, at any tax assumption.")
    L.append("")
    L.append("_Advisory-adjacent research only. This report places no orders and "
             "makes no recommendation. Execute nothing based on this document "
             "alone._")

    REPORT_PATH.write_text("\n".join(L) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")


if __name__ == "__main__":
    main()
