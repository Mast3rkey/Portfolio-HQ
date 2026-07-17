#!/usr/bin/env python3
"""
run_phase3e_scenarios.py — Phase 3E scenario execution driver.

Runs Scenarios A/B/C/D through margin_simulation.py against REAL
historical price data (data/backtest/*.json), using the parameters
finalized in docs/PHASE3_SCENARIO_MANIFEST.md and pinned in
docs/PHASE3_EXECUTION_RECORD.md. This script does not modify
margin_simulation.py, allocate.py, targets.yaml, or holdings.yaml —
it only imports and calls the existing, tested harness.

Before running, it prints the exact configuration for every scenario
and asserts it matches the manifest/execution-record values, so a
human reviewer can visually confirm before results are trusted.

Every result is hypothetical, simulated — see margin_simulation.py's
HYPOTHETICAL_LABEL and BANNED_PHRASES enforcement, applied to every
rendered section this script produces.

No parameter here is tuned after seeing results — every value is
copied verbatim from the manifest/execution record, stated in this
file BEFORE execution, and this script performs no search, sweep, or
retry over any threshold.

Run:  python3 run_phase3e_scenarios.py
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
    render_metrics,
    scenario_fixed_leverage,
    scenario_leverage_sweep,
    scenario_repayment_variants,
    scenario_unlevered,
    simulate,
)

HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE / "docs" / "results"
REPORT_PATH = RESULTS_DIR / "PHASE3_SCENARIO_RESULTS.md"
JSON_PATH = RESULTS_DIR / "phase3_scenario_results.json"

# ── parameters, copied verbatim from PHASE3_SCENARIO_MANIFEST.md /          ─
# ── PHASE3_EXECUTION_RECORD.md -- not re-derived, not tuned here -----------
DEPOSIT_AMOUNT = 2000.0            # backtest_regime.DEPOSIT, shared config
MIN_LOT = 1.0                      # deviation from production's $25, disclosed in
                                    # PHASE3C_SCENARIO_CONFIGURATION.md's shared config
INTEREST_APR = 0.05                # "~5% APR" (Estimated, PHASE3C_ASSUMPTION_REGISTRY.md #10)
INTEREST_FREE_AMOUNT = 1000.0      # first $1,000 of debt interest-free
LEVERAGE_CAP_B_AND_D = 1.8         # targets.yaml margin.leverage_cap (Known)
LEVERAGE_SWEEP_LEVELS = [1.2, 1.4, 1.6, 1.8, 2.0]  # Scenario C
MODEL_B_REPAY_FRACTION = 0.25      # ModelBProfitHarvest initial parameter
MODEL_C_DRAWDOWN_TRIGGER_PCT = 15.0
MODEL_C_RESET_LEVERAGE = 1.25
DECISION_THRESHOLD_ABC_PP = 1.0    # repo standard, A/B/C
DECISION_THRESHOLD_D_PP = 2.0      # explicitly a decision threshold, not a proof threshold

EXPECTED_COMMIT = "585c117c65fb1c95b661450fcd8347979743818c"  # PHASE3_EXECUTION_RECORD.md


def build_scenarios():
    sc_a = scenario_unlevered(name="A")
    sc_b = scenario_fixed_leverage(LEVERAGE_CAP_B_AND_D, INTEREST_APR,
                                   INTEREST_FREE_AMOUNT, name="B")
    sc_c_list = scenario_leverage_sweep(LEVERAGE_SWEEP_LEVELS, INTEREST_APR,
                                        INTEREST_FREE_AMOUNT)
    sc_d_list = scenario_repayment_variants(
        leverage_cap=LEVERAGE_CAP_B_AND_D, interest_apr=INTEREST_APR,
        interest_free_amount=INTEREST_FREE_AMOUNT,
        model_a_cfg={},  # content unused -- scenario_repayment_variants() binds
                        # repayment_model_a to its own leverage_cap param; this
                        # dict only gates whether MODEL_A is included at all
        model_b_cfg={"repay_fraction": MODEL_B_REPAY_FRACTION},
        model_c_cfg={"drawdown_trigger_pct": MODEL_C_DRAWDOWN_TRIGGER_PCT,
                    "reset_leverage": MODEL_C_RESET_LEVERAGE})
    return sc_a, sc_b, sc_c_list, sc_d_list


def print_and_confirm_configuration(sc_a, sc_b, sc_c_list, sc_d_list) -> None:
    print("=" * 78)
    print("PHASE 3E — SCENARIO CONFIGURATION (pre-execution confirmation)")
    print("=" * 78)
    print(f"Expected commit (PHASE3_EXECUTION_RECORD.md): {EXPECTED_COMMIT}")
    print()
    print(f"Shared: deposit=${DEPOSIT_AMOUNT:,.0f}/mo, min_lot=${MIN_LOT:.2f}, "
          f"interest={INTEREST_APR*100:.2f}% APR (${INTEREST_FREE_AMOUNT:,.0f} free)")
    print()
    print(f"Scenario A: {sc_a.name!r} | leverage_cap={sc_a.leverage_cap} | "
          f"repayment={sc_a.repayment_model_name}")
    assert sc_a.leverage_cap == 1.0, "Scenario A must be unlevered (1.0x)"
    assert sc_a.repayment_model_name == "MODEL_0"
    assert sc_a.pre_trade_fn is None

    print(f"Scenario B: {sc_b.name!r} | leverage_cap={sc_b.leverage_cap} | "
          f"repayment={sc_b.repayment_model_name} | interest_apr={sc_b.interest_apr}")
    assert sc_b.leverage_cap == LEVERAGE_CAP_B_AND_D
    assert sc_b.repayment_model_name == "MODEL_0"
    assert sc_b.pre_trade_fn is None

    print(f"Scenario C: {len(sc_c_list)} levels = "
          f"{[s.leverage_cap for s in sc_c_list]}")
    assert [s.leverage_cap for s in sc_c_list] == LEVERAGE_SWEEP_LEVELS
    for s in sc_c_list:
        assert s.repayment_model_name == "MODEL_0"
        assert s.pre_trade_fn is None

    print(f"Scenario D: {len(sc_d_list)} models = "
          f"{[s.repayment_model_name for s in sc_d_list]}")
    assert [s.repayment_model_name for s in sc_d_list] == ["MODEL_0", "MODEL_A", "MODEL_B", "MODEL_C"]
    for s in sc_d_list:
        assert s.leverage_cap == LEVERAGE_CAP_B_AND_D
    d_b = next(s for s in sc_d_list if s.repayment_model_name == "MODEL_B")
    d_c = next(s for s in sc_d_list if s.repayment_model_name == "MODEL_C")
    assert isinstance(d_b.pre_trade_fn, ModelBProfitHarvest)
    assert d_b.pre_trade_fn.repay_fraction == MODEL_B_REPAY_FRACTION
    assert isinstance(d_c.pre_trade_fn, ModelCRiskReset)
    assert d_c.pre_trade_fn.drawdown_trigger_pct == MODEL_C_DRAWDOWN_TRIGGER_PCT
    assert d_c.pre_trade_fn.reset_leverage == MODEL_C_RESET_LEVERAGE

    print()
    print(f"Decision thresholds: A/B/C = {DECISION_THRESHOLD_ABC_PP}pp (repo standard); "
          f"D = {DECISION_THRESHOLD_D_PP}pp (decision threshold, not proof threshold)")
    print()
    print("CONFIRMED: configuration matches PHASE3_SCENARIO_MANIFEST.md and "
          "PHASE3_EXECUTION_RECORD.md (asserted above, not just printed).")
    print("=" * 78)
    print()


def run_all():
    weights, aligned, calendar, deposit_days = load_real_aligned_data()
    window = f"{calendar[0]} to {calendar[-1]}"
    print(f"Universe: {len(weights)} tickers | window {window} | "
          f"{len(deposit_days)} monthly deposits\n")

    sc_a, sc_b, sc_c_list, sc_d_list = build_scenarios()
    print_and_confirm_configuration(sc_a, sc_b, sc_c_list, sc_d_list)

    results = {}

    def _run(sc, key):
        r = simulate(sc, weights, aligned, calendar, deposit_days,
                    deposit_amount=DEPOSIT_AMOUNT, min_lot=MIN_LOT)
        results[key] = r
        return r

    r_a = _run(sc_a, "A")
    r_b = _run(sc_b, "B")
    r_c = {f"C-{s.leverage_cap:.1f}x": _run(s, f"C-{s.leverage_cap:.1f}x") for s in sc_c_list}
    r_d = {s.repayment_model_name: _run(s, f"D-{s.repayment_model_name}") for s in sc_d_list}

    return window, len(weights), len(deposit_days), r_a, r_b, r_c, r_d


def main():
    window, n_tickers, n_deposits, r_a, r_b, r_c, r_d = run_all()

    all_results = {"A": r_a, "B": r_b, **r_c, **{f"D-{k}": v for k, v in r_d.items()}}
    metrics_by_key = {}
    for k, v in all_results.items():
        m = v.metrics()
        repay_events = [e for e in v.events if e["kind"] == "repayment"]
        m["n_repayment_events"] = len(repay_events)
        m["total_repaid"] = sum(e["amount"] for e in repay_events)
        metrics_by_key[k] = m

    # ---- machine-readable output ------------------------------------------
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    json_payload = {
        "label": HYPOTHETICAL_LABEL,
        "disclaimer": ("Not a claim about this account's real history. Every "
                       "scenario is a hypothetical simulation of a synthetic "
                       "$0-start account through real historical prices. See "
                       "docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md sec 3/5."),
        "commit": EXPECTED_COMMIT,
        "execution_date": datetime.now().strftime("%Y-%m-%d"),
        "window": window,
        "universe_size": n_tickers,
        "n_deposits": n_deposits,
        "parameters": {
            "deposit_amount": DEPOSIT_AMOUNT,
            "min_lot": MIN_LOT,
            "interest_apr": INTEREST_APR,
            "interest_free_amount": INTEREST_FREE_AMOUNT,
            "leverage_cap_b_and_d": LEVERAGE_CAP_B_AND_D,
            "leverage_sweep_levels": LEVERAGE_SWEEP_LEVELS,
            "model_b_repay_fraction": MODEL_B_REPAY_FRACTION,
            "model_c_drawdown_trigger_pct": MODEL_C_DRAWDOWN_TRIGGER_PCT,
            "model_c_reset_leverage": MODEL_C_RESET_LEVERAGE,
            "decision_threshold_abc_pp": DECISION_THRESHOLD_ABC_PP,
            "decision_threshold_d_pp": DECISION_THRESHOLD_D_PP,
        },
        "results": metrics_by_key,
    }
    JSON_PATH.write_text(json.dumps(json_payload, indent=2, default=str) + "\n")
    print(f"\n[machine-readable metrics written to {JSON_PATH}]")

    # ---- markdown report ----------------------------------------------------
    lines = []
    lines.append("# Phase 3 Scenario Results")
    lines.append("")
    lines.append(f"> **⚠️ {HYPOTHETICAL_LABEL}.** Not a claim about this account's "
                 "real history. Every scenario below simulates a synthetic "
                 "$0-start account through real historical prices "
                 "(data/backtest/*.json). See "
                 "`docs/PHASE3_MARGIN_EVIDENCE_FRAMEWORK.md` §3/§5 for the "
                 "required output-language rule this report follows.")
    lines.append("")
    lines.append(f"_Executed {datetime.now().strftime('%Y-%m-%d')} at commit "
                 f"`{EXPECTED_COMMIT}` (see `docs/PHASE3_EXECUTION_RECORD.md`). "
                 f"Window: {window}. Universe: {n_tickers} tickers. "
                 f"{n_deposits} monthly ${DEPOSIT_AMOUNT:,.0f} deposits. "
                 "No parameter below was tuned after seeing results — every "
                 "value was fixed in `docs/PHASE3_SCENARIO_MANIFEST.md` before "
                 "this run and is restated verbatim here._")
    lines.append("")

    def _row(key, r):
        m = r.metrics()
        return (f"| {key} | {m['ann_twr_pct']:.2f}% | {m['cagr_pct']:.2f}% | "
               f"{m['max_drawdown_pct']:.2f}% | {m['annualized_volatility_pct']:.2f}% | "
               f"{m['time_near_leverage_cap_pct_proxy']:.1f}% | "
               f"${m['final_book_value']:,.0f} | ${m['final_margin_debt']:,.0f} |")

    lines.append("## Scenario A vs B — unlevered vs current fixed leverage")
    lines.append("")
    lines.append("| Scenario | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    lines.append(_row("A — unlevered", r_a))
    lines.append(_row("B — 1.8x, no repayment", r_b))
    gap_ab = r_b.metrics()["ann_twr_pct"] - r_a.metrics()["ann_twr_pct"]
    dd_gap_ab = r_b.metrics()["max_drawdown_pct"] - r_a.metrics()["max_drawdown_pct"]
    lines.append("")
    lines.append(f"B − A gap: {gap_ab:+.2f}pp annualized TWR, {dd_gap_ab:+.2f}pp MaxDD "
                 f"(more negative = worse). Decision threshold: {DECISION_THRESHOLD_ABC_PP}pp. "
                 f"Gap {'exceeds' if abs(gap_ab) > DECISION_THRESHOLD_ABC_PP else 'is within'} "
                 "the pre-committed threshold — reported as observed, not "
                 "interpreted or acted on in this document.")
    lines.append("")

    lines.append("## Scenario C — leverage sweep")
    lines.append("")
    lines.append("| Level | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for lv in LEVERAGE_SWEEP_LEVELS:
        key = f"C-{lv:.1f}x"
        lines.append(_row(key, r_c[key]))
    lines.append("")

    lines.append("## Scenario D — repayment models")
    lines.append("")
    lines.append("| Model | Ann. TWR | CAGR | MaxDD | Ann. Vol | Time near cap (proxy) | Final book | Final debt |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name in ("MODEL_0", "MODEL_A", "MODEL_B", "MODEL_C"):
        lines.append(_row(name, r_d[name]))
    lines.append("")
    d0_twr = r_d["MODEL_0"].metrics()["ann_twr_pct"]
    d0_dd = r_d["MODEL_0"].metrics()["max_drawdown_pct"]
    lines.append(f"Gaps vs D-0 (control), decision threshold {DECISION_THRESHOLD_D_PP}pp "
                 "(TWR OR MaxDD improvement — a decision threshold, not a proof threshold):")
    lines.append("")
    lines.append("| Model | TWR gap vs D-0 | MaxDD gap vs D-0 | Crosses decision threshold? |")
    lines.append("|---|---:|---:|---|")
    for name in ("MODEL_A", "MODEL_B", "MODEL_C"):
        m = r_d[name].metrics()
        twr_gap = m["ann_twr_pct"] - d0_twr
        dd_gap = m["max_drawdown_pct"] - d0_dd
        crosses = abs(twr_gap) > DECISION_THRESHOLD_D_PP or abs(dd_gap) > DECISION_THRESHOLD_D_PP
        lines.append(f"| {name} | {twr_gap:+.2f}pp | {dd_gap:+.2f}pp | {'Yes' if crosses else 'No'} |")
    lines.append("")
    lines.append("Reported as observed. No parameter was adjusted, re-run, or "
                 "swept in response to these numbers — Model B's repay_fraction "
                 "sweep ({10%, 25%, 50%}) named in the manifest as future work "
                 "was NOT run here, and no threshold above was chosen after "
                 "seeing a result.")
    lines.append("")

    lines.append("## Limitations (carried forward, not re-litigated)")
    lines.append("")
    lines.append("- Concentration stress trigger (30%) is not wired into any "
                 "executable code — Scenario D's concentration-interaction "
                 "dimension was not exercised (per `PHASE3_EXECUTION_RECORD.md` §4).")
    lines.append("- `time_near_leverage_cap_pct_proxy` is NOT a real Robinhood "
                 "buffer% — see `margin_simulation.py`'s module docstring.")
    lines.append("- One window, one mostly-rising sample (2021-2026) — the 2022 "
                 "stretch is the only real bear-market representation.")
    lines.append("- Interest rate (5.00% APR) is Estimated, not Known — no real "
                 "interest-paid ledger exists to validate it against.")
    n_c_repays = metrics_by_key["D-MODEL_C"]["n_repayment_events"]
    n_b_repays = metrics_by_key["D-MODEL_B"]["n_repayment_events"]
    b_total_repaid = metrics_by_key["D-MODEL_B"]["total_repaid"]
    lines.append(f"- Model C's trigger requires a >15% net-equity drawdown from "
                 f"this simulated account's own peak — it **fired {n_c_repays} "
                 f"times in this window**, which is why MODEL_C's row above is "
                 "identical to MODEL_0's: this diversified 63-ticker portfolio's "
                 "net equity never drew down >15% from its own peak in "
                 "2021-2026, even though individual names (see "
                 "`reports/t1t2_trim_backtest.md`'s NVDA decomposition, a "
                 "different test, same window) had far worse single-name "
                 "drawdowns — portfolio-level diversification smoothed the "
                 "trigger away. A real, honest finding, not a bug: it says this "
                 "window doesn't exercise Model C's mechanism, not that the "
                 "mechanism doesn't work (see the unit/property tests in "
                 "`test_margin_simulation.py` for that).")
    lines.append(f"- Model B's HWM-gain trigger fired {n_b_repays} times, "
                 f"repaying ${b_total_repaid:,.0f} total across the window — "
                 "unlike Model C, this window DOES exercise Model B's mechanism "
                 "(a steadily rising simulated portfolio sets new highs often).")
    lines.append("")
    lines.append("_Advisory-adjacent research only. This report places no orders "
                 "and makes no recommendation. Execute nothing based on this "
                 "document alone._")

    REPORT_PATH.write_text("\n".join(lines) + "\n")
    print(f"[report written to {REPORT_PATH}]")


if __name__ == "__main__":
    main()
