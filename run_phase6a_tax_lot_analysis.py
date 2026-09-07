#!/usr/bin/env python3
"""
run_phase6a_tax_lot_analysis.py — Phase 6A tax-lot analysis driver, per
docs/PHASE6A_TAX_LOT_MODELING_PLAN.md / docs/PHASE6A_IMPLEMENTATION_
APPROVAL.md (Prompt 4).

Re-runs the three already-approved Model B repay_fraction arms
(10%/25%/50%) through the Phase 6A-modified margin_simulation.py,
verifies each arm's gross TWR/MaxDD/event count still match the stored
docs/results/PHASE3_SENSITIVITY_RESULTS.json values (the same gate
already passed once interactively — re-asserted here as a hard stop
before this script proceeds to any tax computation), then computes:

  1. Realized-gain summary metrics from the FIFO lot ledger's
     tax_lot_events (phase6a_tax_lot_lib.realized_gain_summary()).
  2. A FIFO-realistic taxable base (net realized gain, floored at zero —
     see phase6a_tax_lot_lib.net_taxable_base()'s own docstring for the
     disclosed loss-treatment simplification), taxed at the same three
     approved illustrative rate tiers (0%/15%/32%) already used by the
     Phase 3G upper-bound pass.
  3. A direct comparison against the stored upper-bound tax figures in
     docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json.

No engine change. No repay_fraction selection. No doctrine change. See
docs/PHASE6A_TAX_LOT_MODELING_PLAN.md §8/§9 for the full allowed/
prohibited conclusions list this script's output must respect.

Run:  python3 run_phase6a_tax_lot_analysis.py
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
from phase6a_tax_lot_lib import net_taxable_base, realized_gain_summary
from tax_treatment_lib import net_twr_after_tax, tax_drag

HERE = Path(__file__).resolve().parent
PHASE3G_JSON = HERE / "docs" / "results" / "PHASE3_SENSITIVITY_RESULTS.json"
UPPER_BOUND_JSON = HERE / "docs" / "results" / "TAX_TREATMENT_SENSITIVITY_RESULTS.json"
REPORT_PATH = HERE / "docs" / "PHASE6A_TAX_LOT_ANALYSIS.md"
JSON_PATH = HERE / "docs" / "results" / "PHASE6A_TAX_LOT_ANALYSIS_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_APR = 0.05
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP = 1.8

REPAY_FRACTIONS = (0.10, 0.25, 0.50)
TAX_RATE_TIERS_PCT = (0.0, 15.0, 32.0)
MATERIAL_THRESHOLD_PP = 2.0
NOISE_FLOOR_PP = 0.5


def _outcome_category(gap_classes: list[str]) -> str:
    """Three-way outcome framework (Phase 4A's adopted convention,
    reused unchanged): any material gap -> 'Evidence supports' (tax
    friction remains a material concern under realistic accounting);
    every gap at or below the noise floor -> 'Evidence does not
    support'; anything mixed (suggestive, or a mix of material/noise)
    -> 'Evidence inconclusive'."""
    if any(c == "material" for c in gap_classes):
        return "Evidence supports"
    if all(c == "noise" for c in gap_classes):
        return "Evidence does not support"
    return "Evidence inconclusive"


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"

    stored_3g = json.loads(PHASE3G_JSON.read_text())
    stored_upper_bound = json.loads(UPPER_BOUND_JSON.read_text())
    control_twr = stored_3g["baseline_B_interest_5pct"]["ann_twr_pct"]
    control_maxdd = stored_3g["baseline_B_interest_5pct"]["max_drawdown_pct"]

    def run(sc):
        return simulate(sc, weights, aligned, calendar, deposit_days,
                        deposit_amount=DEPOSIT_AMOUNT, min_lot=MIN_LOT)

    r_control = run(scenario_fixed_leverage(LEVERAGE_CAP, INTEREST_APR, INTEREST_FREE_AMOUNT, name="B"))
    assert abs(r_control.metrics()["ann_twr_pct"] - control_twr) < 1e-6, "control TWR diverged from stored Phase 3G value"
    assert r_control.tax_lot_events == [], "control (MODEL_0) must never generate tax lot events"
    print(f"Control (D-0/B) verified identical to stored Phase 3G value: {control_twr:.4f}% TWR")

    results = {}
    for frac in REPAY_FRACTIONS:
        scs = scenario_repayment_variants(
            leverage_cap=LEVERAGE_CAP, interest_apr=INTEREST_APR,
            interest_free_amount=INTEREST_FREE_AMOUNT,
            model_b_cfg={"repay_fraction": frac})
        sc_b = next(s for s in scs if s.repayment_model_name == "MODEL_B")
        r = run(sc_b)

        stored_arm = stored_3g["model_b_sensitivity"][f"{frac:.2f}"]
        gross_twr = r.metrics()["ann_twr_pct"]
        gross_maxdd = r.metrics()["max_drawdown_pct"]
        n_events = sum(1 for e in r.events if e["kind"] == "repayment")
        assert abs(gross_twr - stored_arm["ann_twr_pct"]) < 1e-6, (
            f"repay_fraction={frac} gross TWR diverged from stored Phase 3G value")
        assert abs(gross_maxdd - stored_arm["max_drawdown_pct"]) < 1e-6, (
            f"repay_fraction={frac} gross MaxDD diverged from stored Phase 3G value")
        assert n_events == stored_arm["event_stats"]["count"], (
            f"repay_fraction={frac} event count diverged from stored Phase 3G value")
        print(f"repay_fraction={frac:.0%} gate re-verified: {gross_twr:.4f}% TWR, "
             f"{gross_maxdd:.4f}% MaxDD, {n_events} events — MATCH")

        # ---- realized-gain summary from the FIFO lot ledger ----------------
        summary = realized_gain_summary(r.tax_lot_events)
        taxable_base_realistic = net_taxable_base(r.tax_lot_events)

        upper_bound_arm = stored_upper_bound["results"][f"{frac:.2f}"]
        taxable_base_upper_bound = upper_bound_arm["taxable_base_upper_bound"]

        by_rate = {}
        for rate_pct in TAX_RATE_TIERS_PCT:
            drag = tax_drag(taxable_base_realistic, rate_pct / 100.0)
            net_twr = net_twr_after_tax(r.book_values, r.flows, drag)
            gap_vs_control_net = net_twr - control_twr
            by_rate[rate_pct] = {
                "rate_pct": rate_pct,
                "rate_label": "Known (no tax, control)" if rate_pct == 0.0 else "Hypothetical (illustrative federal bracket)",
                "taxable_base_realistic_fifo": taxable_base_realistic,
                "tax_drag_dollars": drag,
                "net_ann_twr_pct": net_twr,
                "gap_vs_control_net_pp": gap_vs_control_net,
                "gap_vs_control_net_class": classify_gap(gap_vs_control_net, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
                # comparison point: what the SAME rate tier produced under
                # the Phase 3G upper-bound (100%-of-repaid-dollars) model
                "upper_bound_net_ann_twr_pct": upper_bound_arm["by_rate_tier"][str(rate_pct)]["net_ann_twr_pct"],
                "upper_bound_gap_vs_control_net_pp": upper_bound_arm["by_rate_tier"][str(rate_pct)]["gap_vs_control_net_pp"],
                "upper_bound_gap_vs_control_net_class": upper_bound_arm["by_rate_tier"][str(rate_pct)]["gap_vs_control_net_class"],
            }

        gap_classes_nonzero_rate = [by_rate[rp]["gap_vs_control_net_class"]
                                    for rp in TAX_RATE_TIERS_PCT if rp > 0.0]
        outcome = _outcome_category(gap_classes_nonzero_rate)

        taxable_base_reduction_pct = (
            (1.0 - taxable_base_realistic / taxable_base_upper_bound) * 100.0
            if taxable_base_upper_bound > 0 else 0.0)

        results[frac] = {
            "repay_fraction": frac,
            "gross_ann_twr_pct": gross_twr,
            "gross_max_drawdown_pct": gross_maxdd,
            "n_repayment_events": n_events,
            "realized_gain_summary": summary,
            "taxable_base_realistic_fifo": taxable_base_realistic,
            "taxable_base_upper_bound": taxable_base_upper_bound,
            "taxable_base_reduction_pct": taxable_base_reduction_pct,
            "by_rate_tier": by_rate,
            "outcome_category": outcome,
        }
        print(f"  taxable base: FIFO-realistic ${taxable_base_realistic:,.2f} vs. "
             f"upper-bound ${taxable_base_upper_bound:,.2f} "
             f"({taxable_base_reduction_pct:.1f}% reduction) — outcome: {outcome}")

    write_outputs(window, control_twr, control_maxdd, results)


def write_outputs(window, control_twr, control_maxdd, results):
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history, real cost "
                       "basis, or real tax liability. Every scenario is a "
                       "hypothetical simulation of a synthetic $0-start account "
                       "through real historical prices. The FIFO lot ledger is "
                       "built entirely from this synthetic account's own simulated "
                       "purchase history, never from real trade data. FIFO is a "
                       "disclosed default consumption convention, not a confirmed "
                       "fact about this account's real elected convention. The "
                       "15%/32% rate tiers are disclosed Hypothetical, illustrative "
                       "federal brackets, not this account's confirmed rate. State "
                       "tax, wash-sale rules, AMT, and NIIT are excluded, not "
                       "assumed zero-impact. See docs/PHASE6A_TAX_LOT_MODELING_"
                       "PLAN.md, docs/PHASE6A_ASSUMPTION_REGISTRY.md, and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "control_ann_twr_pct": control_twr,
        "control_max_drawdown_pct": control_maxdd,
        "tax_rate_tiers_pct": list(TAX_RATE_TIERS_PCT),
        "material_threshold_pp": MATERIAL_THRESHOLD_PP,
        "noise_floor_pp": NOISE_FLOOR_PP,
        "results": {f"{frac:.2f}": r for frac, r in results.items()},
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    L = []
    L.append("# Phase 6A — Tax Lot Analysis Results")
    L.append("")
    L.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
             "history, real cost basis, or real tax liability. The FIFO lot ledger "
             "is built entirely from a synthetic $0-start account's own simulated "
             "purchase history through real historical prices — never from real "
             "trade data. FIFO is a disclosed default convention "
             "(`docs/PHASE6A_ASSUMPTION_REGISTRY.md` #3), not a confirmed fact "
             "about this account's real elected convention. The 15%/32% rate "
             "tiers remain disclosed Hypothetical illustrative federal brackets. "
             "State tax, wash-sale rules, AMT, and NIIT remain excluded, not "
             "assumed zero-impact. See `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` for "
             "the pre-approved design this run follows.")
    L.append("")
    L.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}. Window: {window}. "
             f"Control (no repayment, MODEL_0, 1.8x leverage): "
             f"**{control_twr:.2f}% ann. TWR, {control_maxdd:.2f}% MaxDD** — "
             "verified identical to the stored `docs/results/"
             "PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. "
             "Each `repay_fraction` arm's gross TWR/MaxDD/event count were "
             "likewise re-verified identical to that stored file (the same "
             "verify-before-comparing gate already run interactively) before any "
             "tax computation was applied._")
    L.append("")

    for frac, r in results.items():
        s = r["realized_gain_summary"]
        L.append(f"## repay_fraction = {frac:.0%}")
        L.append("")
        L.append(f"**Gross Model B result**: {r['gross_ann_twr_pct']:.2f}% ann. TWR, "
                 f"{r['gross_max_drawdown_pct']:.2f}% MaxDD, {r['n_repayment_events']} "
                 "repayment events.")
        L.append("")
        L.append("### 1. Tax realization metrics (FIFO lot ledger)")
        L.append("")
        L.append(f"- Disposal events: {s['n_disposal_events']} ({s['n_gain_events']} gain, "
                 f"{s['n_loss_events']} loss)")
        L.append(f"- Total proceeds: ${s['total_proceeds']:,.2f}")
        L.append(f"- Total cost basis: ${s['total_cost_basis']:,.2f}")
        L.append(f"- Total realized gains: ${s['total_realized_gains']:,.2f}")
        L.append(f"- Total realized losses: ${s['total_realized_losses']:,.2f}")
        L.append(f"- Net realized gain: ${s['total_realized_gain_net']:,.2f}")
        L.append(f"- Average holding period (proceeds-weighted): "
                 f"{s['avg_holding_period_days_proceeds_weighted']:.1f} days")
        L.append(f"- Gain split: {s['short_term_gain_pct_of_gains']:.1f}% short-term "
                 f"(${s['short_term_gain_dollars']:,.2f}), "
                 f"{s['long_term_gain_pct_of_gains']:.1f}% long-term "
                 f"(${s['long_term_gain_dollars']:,.2f})")
        L.append("")
        L.append("### 2. Tax sensitivity (FIFO-realistic taxable base)")
        L.append("")
        L.append(f"FIFO-realistic taxable base (net realized gain, floored at $0 — "
                 f"`phase6a_tax_lot_lib.net_taxable_base()`): "
                 f"**${r['taxable_base_realistic_fifo']:,.2f}**")
        L.append("")
        L.append("| Rate tier | Label | Tax drag | Net TWR | Gap vs. control | Classification |")
        L.append("|---|---|---:|---:|---:|---|")
        for rate_pct in TAX_RATE_TIERS_PCT:
            t = r["by_rate_tier"][rate_pct]
            L.append(f"| {rate_pct:.0f}% | {t['rate_label']} | ${t['tax_drag_dollars']:,.2f} | "
                     f"{t['net_ann_twr_pct']:.2f}% | {t['gap_vs_control_net_pp']:+.2f}pp | "
                     f"{t['gap_vs_control_net_class']} |")
        L.append("")
        L.append("### 3. Comparison against the Phase 3G worst-case upper-bound tax model")
        L.append("")
        L.append(f"Upper-bound taxable base (100% of every repaid dollar treated as "
                 f"gain, `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json`): "
                 f"**${r['taxable_base_upper_bound']:,.2f}**")
        L.append(f"FIFO-realistic taxable base: **${r['taxable_base_realistic_fifo']:,.2f}** "
                 f"— a **{r['taxable_base_reduction_pct']:.1f}% reduction** from the upper bound.")
        L.append("")
        L.append("| Rate tier | Upper-bound net TWR | Upper-bound gap | FIFO-realistic net TWR | FIFO-realistic gap |")
        L.append("|---|---:|---:|---:|---:|")
        for rate_pct in TAX_RATE_TIERS_PCT:
            t = r["by_rate_tier"][rate_pct]
            L.append(f"| {rate_pct:.0f}% | {t['upper_bound_net_ann_twr_pct']:.2f}% | "
                     f"{t['upper_bound_gap_vs_control_net_pp']:+.2f}pp "
                     f"({t['upper_bound_gap_vs_control_net_class']}) | "
                     f"{t['net_ann_twr_pct']:.2f}% | {t['gap_vs_control_net_pp']:+.2f}pp "
                     f"({t['gap_vs_control_net_class']}) |")
        L.append("")
        L.append(f"**Outcome category (per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s "
                 f"adopted three-way framework, applied to the 15%/32% tiers): "
                 f"{r['outcome_category']}**")
        L.append("")

    L.append("## 4. Materiality framework applied")
    L.append("")
    L.append("Reused, not reinvented: 2.0pp material / 0.5pp noise floor "
             "(`docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3), and the three-way "
             "outcome framework (Evidence supports / Evidence does not support / "
             "Evidence inconclusive) adopted in `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` "
             "and reused throughout every sensitivity pass since. No new threshold "
             "introduced or optimized by this analysis.")
    L.append("")

    L.append("## Summary: did realistic FIFO lot accounting change the interpretation?")
    L.append("")
    for frac, r in results.items():
        L.append(f"- **{frac:.0%}**: taxable base fell {r['taxable_base_reduction_pct']:.1f}% "
                 f"(${r['taxable_base_upper_bound']:,.2f} → ${r['taxable_base_realistic_fifo']:,.2f}); "
                 f"outcome category **{r['outcome_category']}**.")
    L.append("")

    L.append("## What this analysis does not resolve")
    L.append("")
    L.append("- **Not this account's real cost basis** — the FIFO lot ledger is built "
             "entirely from the synthetic simulation's own purchase history.")
    L.append("- **Not this account's real elected lot-consumption convention** — FIFO "
             "is a disclosed default, not a confirmed fact.")
    L.append("- **Not this account's real tax rate, filing status, or jurisdiction** — "
             "the 0%/15%/32% tiers remain illustrative federal brackets only.")
    L.append("- **Not a model of wash-sale rules, AMT, NIIT, or loss carryforward "
             "benefit** — a net realized loss is floored at $0 taxable base, not "
             "treated as a deduction against other income.")
    L.append("- **No repayment fraction selected, no implementation recommended, no "
             "doctrine changed, no leverage cap examined or changed** — per "
             "`docs/PHASE6A_IMPLEMENTATION_APPROVAL.md` §3.")
    L.append("")
    L.append("_Advisory-adjacent research only. This report places no orders and "
             "makes no recommendation about Model B, any repay_fraction, or any "
             "production change. Execute nothing based on this document alone._")

    REPORT_PATH.write_text("\n".join(L) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")


if __name__ == "__main__":
    main()
