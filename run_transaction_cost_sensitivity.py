#!/usr/bin/env python3
"""
run_transaction_cost_sensitivity.py — transaction-cost sensitivity
analysis driver, per docs/TRANSACTION_COST_SENSITIVITY_PLAN.md.

Re-runs the three already-approved Model B repay_fraction arms
(10%/25%/50%, docs/PHASE3_SCENARIO_MANIFEST.md's original values)
through the UNMODIFIED margin_simulation.py/phase3g's existing scenario
builders, verifies each arm's headline numbers match the stored
docs/results/PHASE3_SENSITIVITY_RESULTS.json before applying any cost
(same "verify identical before proceeding" discipline as run_phase3g_
sensitivity.py and run_phase4a_research.py), then applies three
disclosed, hypothetical cost tiers (0/5/15 bps) as a lump-sum,
first-order approximation (transaction_cost_lib.cost_adjusted_twr()).

No engine change: SimulationResult.events already carries every
repayment event's exact day and dollar amount. No production file
touched. No repay_fraction is selected or recommended -- see
docs/TRANSACTION_COST_SENSITIVITY_PLAN.md §10 for the full allowed/
not-allowed list this script's output must respect.

Run:  python3 run_transaction_cost_sensitivity.py
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
from phase3g_lib import estimate_turnover
from phase4a_lib import classify_gap
from transaction_cost_lib import cost_adjusted_twr, event_costs, total_transaction_cost

HERE = Path(__file__).resolve().parent
PHASE3G_JSON = HERE / "docs" / "results" / "PHASE3_SENSITIVITY_RESULTS.json"
REPORT_PATH = HERE / "docs" / "TRANSACTION_COST_SENSITIVITY_RESULTS.md"
JSON_PATH = HERE / "docs" / "results" / "TRANSACTION_COST_SENSITIVITY_RESULTS.json"

DEPOSIT_AMOUNT = 2000.0
MIN_LOT = 1.0
INTEREST_APR = 0.05
INTEREST_FREE_AMOUNT = 1000.0
LEVERAGE_CAP = 1.8

REPAY_FRACTIONS = (0.10, 0.25, 0.50)
COST_TIERS_BPS = (0.0, 5.0, 15.0)
MATERIAL_THRESHOLD_PP = 2.0
NOISE_FLOOR_PP = 0.5


def main():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"
    n_deposits = len(deposit_days)
    total_deposited = DEPOSIT_AMOUNT * n_deposits

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

        total_repaid = sum(e["amount"] for e in r.events if e["kind"] == "repayment")
        turnover = estimate_turnover(total_repaid, total_deposited)

        by_tier = {}
        for bps in COST_TIERS_BPS:
            cost = total_transaction_cost(r.events, bps)
            net_twr = cost_adjusted_twr(r.book_values, r.flows, cost)
            gap_vs_control_gross = gross_twr - control_twr
            gap_vs_control_net = net_twr - control_twr
            by_tier[bps] = {
                "bps": bps,
                "cost_label": "Known" if bps == 0.0 else "Hypothetical",
                "total_cost_dollars": cost,
                "cost_pct_of_repaid": (cost / total_repaid * 100.0) if total_repaid > 0 else 0.0,
                "cost_pct_of_deposited": (cost / total_deposited * 100.0) if total_deposited > 0 else 0.0,
                "gross_ann_twr_pct": gross_twr,
                "net_ann_twr_pct": net_twr,
                "twr_erosion_pp": gross_twr - net_twr,
                "gap_vs_control_gross_pp": gap_vs_control_gross,
                "gap_vs_control_net_pp": gap_vs_control_net,
                "gap_vs_control_gross_class": classify_gap(gap_vs_control_gross, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
                "gap_vs_control_net_class": classify_gap(gap_vs_control_net, MATERIAL_THRESHOLD_PP, NOISE_FLOOR_PP),
            }

        results[frac] = {
            "repay_fraction": frac,
            "gross_ann_twr_pct": gross_twr,
            "gross_max_drawdown_pct": gross_maxdd,
            "n_repayment_events": n_events,
            "total_repaid_dollars": total_repaid,
            "turnover_estimate": turnover,
            "by_cost_tier": by_tier,
        }

    write_outputs(window, n_deposits, total_deposited, control_twr, control_maxdd, results)


def write_outputs(window, n_deposits, total_deposited, control_twr, control_maxdd, results):
    RESULTS_DIR = JSON_PATH.parent
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history or real "
                       "trading costs. Every scenario is a hypothetical simulation "
                       "of a synthetic $0-start account through real historical "
                       "prices; the 5bps/15bps cost tiers are disclosed "
                       "Hypothetical assumptions, not measured Robinhood spread "
                       "data. See docs/TRANSACTION_COST_SENSITIVITY_PLAN.md and "
                       "docs/PHASE3_FINDINGS.md sec 8."),
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "n_deposits": n_deposits,
        "total_deposited": total_deposited,
        "control_ann_twr_pct": control_twr,
        "control_max_drawdown_pct": control_maxdd,
        "cost_tiers_bps": list(COST_TIERS_BPS),
        "material_threshold_pp": MATERIAL_THRESHOLD_PP,
        "noise_floor_pp": NOISE_FLOOR_PP,
        "results": {f"{frac:.2f}": r for frac, r in results.items()},
    }
    JSON_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    L = []
    L.append("# Transaction Cost Sensitivity Results")
    L.append("")
    L.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's real "
             "history or real trading costs. Every figure below simulates a "
             "synthetic $0-start account through real historical prices; the "
             "5bps/15bps cost tiers are disclosed Hypothetical assumptions, not "
             "measured Robinhood spread data (0bps reflects Robinhood's real, "
             "Known $0 commission structure). See "
             "`docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` for the pre-approved "
             "design this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the "
             "full disclaimer.")
    L.append("")
    L.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')}. Window: {window}. "
             f"{n_deposits} monthly ${DEPOSIT_AMOUNT:,.0f} deposits "
             f"(${total_deposited:,.0f} total). Control (no repayment, MODEL_0, "
             f"1.8x leverage): **{control_twr:.2f}% ann. TWR, {control_maxdd:.2f}% "
             "MaxDD** — verified identical to the stored "
             "`docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this "
             "run proceeded. Each `repay_fraction` arm's gross (0bps) figures "
             "were likewise verified identical to that stored file before any "
             "cost was applied. Cost is applied as a first-order, lump-sum "
             "approximation (`transaction_cost_lib.cost_adjusted_twr()`) — not a "
             "fully compounded, re-simulated cost-aware backtest — per "
             "`docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §6's disclosed "
             "simplification._")
    L.append("")

    for frac, r in results.items():
        L.append(f"## repay_fraction = {frac:.0%}")
        L.append("")
        L.append(f"1. **Gross Model B result** (0bps, unadjusted): {r['gross_ann_twr_pct']:.2f}% "
                 f"ann. TWR, {r['gross_max_drawdown_pct']:.2f}% MaxDD, "
                 f"{r['n_repayment_events']} repayment events, "
                 f"${r['total_repaid_dollars']:,.0f} total repaid.")
        L.append(f"4. **Turnover metric**: {r['turnover_estimate']*100:.1f}% of total "
                 "deposited capital (upper-bound estimate, per "
                 "`docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4's established "
                 "methodology — the harness does not separately log the "
                 "cash-vs-trim funding split per event).")
        L.append("")
        L.append("| Cost tier | Label | Total cost | Cost % of repaid | 2. Assumed cost drag (TWR) | 3. Net cost-adjusted TWR | 5. Gap vs. control (gross) | Gap vs. control (net) |")
        L.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for bps in COST_TIERS_BPS:
            t = r["by_cost_tier"][bps]
            L.append(f"| {bps:.0f}bps | {t['cost_label']} | ${t['total_cost_dollars']:,.2f} | "
                     f"{t['cost_pct_of_repaid']:.3f}% | {t['twr_erosion_pp']:.4f}pp | "
                     f"{t['net_ann_twr_pct']:.2f}% | "
                     f"{t['gap_vs_control_gross_pp']:+.2f}pp ({t['gap_vs_control_gross_class']}) | "
                     f"{t['gap_vs_control_net_pp']:+.2f}pp ({t['gap_vs_control_net_class']}) |")
        L.append("")

    L.append("## Directional observations")
    L.append("")
    L.append("Reported as observed, per `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` "
             "§8/§10 — no `repay_fraction` or cost tier is presented as preferred, "
             "and no deployment recommendation is made.")
    L.append("")
    for bps in COST_TIERS_BPS:
        costs = [results[f]["by_cost_tier"][bps]["total_cost_dollars"] for f in REPAY_FRACTIONS]
        monotonic = costs[0] <= costs[1] <= costs[2]
        L.append(f"- At {bps:.0f}bps: total cost scales with `repay_fraction` "
                 f"({', '.join(f'{f:.0%}=${c:,.2f}' for f, c in zip(REPAY_FRACTIONS, costs))}) — "
                 f"{'monotonically increasing' if monotonic else 'not monotonic (flagged for review)'}, "
                 "consistent with turnover scaling with the repayment fraction "
                 "(`docs/results/PHASE3_MODEL_B_ANALYSIS.md`'s original finding).")
    L.append("")
    all_classes = {(f, bps): results[f]["by_cost_tier"][bps]["gap_vs_control_net_class"]
                   for f in REPAY_FRACTIONS for bps in COST_TIERS_BPS}
    class_changed = any(results[f]["by_cost_tier"][0.0]["gap_vs_control_gross_class"] !=
                        results[f]["by_cost_tier"][bps]["gap_vs_control_net_class"]
                        for f in REPAY_FRACTIONS for bps in COST_TIERS_BPS)
    L.append(f"- Materiality classification (vs. control) change across any tested cost tier: "
             f"**{class_changed}** — at the tested cost magnitudes, the materiality band each "
             "`repay_fraction` arm's gap-vs-control falls into does or does not shift once cost "
             "is applied (see the per-arm tables above for the specific cells).")
    L.append("")

    L.append("## Limitations")
    L.append("")
    L.append("- **Dollar-volume cost model only** — does not account for per-trade-leg "
             "fragmentation (`_fund_repayment()` trims across every held position "
             "simultaneously per event; per-ticker trade counts are not logged "
             "anywhere in this harness). A minimum-fee-per-leg cost model, if one "
             "existed, could produce a materially different (likely higher) cost "
             "than this dollar-volume-only estimate, per "
             "`docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §3/§8.")
    L.append("- **First-order, lump-sum cost approximation** — cost is deducted once "
             "from the final book value, not compounded forward or reflected in "
             "reduced reinvestment capacity along the path.")
    L.append("- **MaxDD is not cost-adjusted** — a lagging, lump-sum deduction does "
             "not meaningfully change a peak-to-trough calculation; gross MaxDD is "
             "reported unchanged across all cost tiers for each `repay_fraction`.")
    L.append("- **5bps/15bps are disclosed Hypothetical assumptions**, not measured "
             "spread/slippage data — no real transaction-cost data exists anywhere "
             "in this repo to validate them against.")
    L.append("- **Model C is out of scope** — its measured repayment activity across "
             "every prior Phase 3G/4A run is zero or too small to price meaningfully.")
    L.append("")
    L.append("_Advisory-adjacent research only. This report places no orders and "
             "makes no recommendation. Execute nothing based on this document "
             "alone._")

    REPORT_PATH.write_text("\n".join(L) + "\n")
    print(f"\n[report written to {REPORT_PATH}]")
    print(f"[machine-readable output written to {JSON_PATH}]")


if __name__ == "__main__":
    main()
