# Phase 3G Sensitivity Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history. Every arm below is a hypothetical simulation of a synthetic $0-start account through real historical prices. No parameter was tuned after seeing results; no arm is presented as a winner. See `docs/PHASE3_SENSITIVITY_PLAN.md` for the pre-committed design this run follows exactly, and `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.

_Executed 2026-07-17, per `docs/PHASE3_SENSITIVITY_PLAN.md`. Window: 2021-06-01 to 2026-07-10. 62 monthly $2,000 deposits ($124,000 total). Baselines (Scenario A unlevered, Scenario B 1.8x/5% interest/no repayment) recomputed and verified identical to the stored Phase 3E results before any sensitivity arm ran — see `run_phase3g_sensitivity.py`'s assertions. Phase 3E's own result files (`docs/results/PHASE3_SCENARIO_RESULTS.md`, `docs/results/phase3_scenario_results.json`) were not modified or overwritten by this run._

**Baseline for comparison — Scenario B (1.8x leverage, 5% interest, no repayment): 35.59% ann. TWR, -26.81% MaxDD.**

## 1. Model B (Profit Harvest) repay_fraction sensitivity

**Parameters changed:** `repay_fraction` ∈ {10%, 25%, 50%}.
**Parameters held constant:** leverage_cap=1.8, interest_apr=5.00%, interest_free_amount=$1,000, Model C inactive, universe/window/deposits/weights/trim rule as shared config (`docs/PHASE3C_SCENARIO_CONFIGURATION.md`).

| repay_fraction | Ann. TWR | Gap vs baseline | CAGR | MaxDD | Gap vs baseline | Ann. Vol | Final debt | n_events | Total repaid | Turnover est. | TWR/\|MaxDD\| |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% | 34.62% | -0.98pp | 180.93% | -25.84% | +0.97pp | 25.18% | $126,784 | 314 | $38,226 | 30.8% | 1.340 |
| 25% | 33.28% | -2.32pp | 178.60% | -24.74% | +2.07pp | 24.36% | $103,959 | 296 | $88,516 | 71.4% | 1.345 |
| 50% | 32.03% | -3.56pp | 176.33% | -23.65% | +3.16pp | 23.56% | $78,857 | 263 | $156,113 | 125.9% | 1.354 |

**Monotonicity check:** TWR at 10%/25%/50% = 34.62% / 33.28% / 32.03% — monotonic across the sweep.

**Limitations:** turnover is an upper-bound estimate (the harness doesn't log the cash-vs-trim funding split per event, per `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4). No transaction-cost or tax model exists anywhere in this repo to price that turnover.

## 2. Model C (Risk Reset) drawdown_trigger_pct sensitivity

**Parameters changed:** `drawdown_trigger_pct` ∈ {10%, 12.5%, 15%, 20%}.
**Parameters held constant:** `reset_leverage`=1.25 (fixed), leverage_cap=1.8, interest_apr=5.00%, interest_free_amount=$1,000, Model B inactive, shared config as above.

| drawdown_trigger_pct | n_reset_activations | n_repayment_events | Ann. TWR | Gap vs baseline | MaxDD | Gap vs baseline | Final debt | Days effective_cap tightened |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% | 10 | 2 | 35.03% | -0.56pp | -26.81% | -0.00pp | $130,626 | 1257 |
| 12.5% | 7 | 1 | 35.09% | -0.50pp | -26.81% | +0.00pp | $131,873 | 1238 |
| 15% | 1 | 0 | 35.59% | +0.00pp | -26.81% | +0.00pp | $147,745 | 1227 |
| 20% | 1 | 0 | 35.59% | +0.00pp | -26.81% | +0.00pp | $147,745 | 1227 |

**Trigger-firing summary:** 10% fired 10 time(s); 12.5% fired 7 time(s); 15% fired 1 time(s); 20% fired 1 time(s).

**Limitations:** `reset_leverage` (1.25x) was held fixed — this sweep does not test whether a different reset target changes trigger sensitivity (it structurally can't, since the drawdown TRIGGER and the reset TARGET are independent parameters in the implementation). "Days effective_cap tightened" approximates days spent at/near the reset target via a leverage-series proxy, not a direct read of `reset_active` state (the driver's `ModelCTriggerLogger` tracks activation days only, not full-duration active windows — a possible future refinement, not done here).

## 3. Interest rate sensitivity

**Parameters changed:** `interest_apr` ∈ {0%, 5%, 8%}.
**Parameters held constant:** leverage_cap=1.8, interest_free_amount=$1,000, repayment=MODEL_0 (no repayment model active — isolates the interest-cost effect), shared config as above. Compared against Scenario A (unlevered), which is invariant to interest_apr since it never carries debt.

| interest_apr | Scenario A TWR | Levered TWR | A-vs-B TWR gap | A-vs-B MaxDD gap | Cumulative interest accrued | Final debt |
|---:|---:|---:|---:|---:|---:|---:|
| 0% | 30.01% | 35.98% | +5.97pp | -4.27pp | $0 | $147,299 |
| 5% | 30.01% | 35.59% | +5.58pp | -4.40pp | $3,921 | $147,745 |
| 8% | 30.01% | 35.35% | +5.35pp | -4.48pp | $6,294 | $148,019 |

**Direction check:** the levered account beat the unlevered baseline on TWR at all three rates (0%: +5.97pp, 5%: +5.58pp, 8%: +5.35pp) — the direction holds across the full tested range.

**Limitations:** 0% is a decomposition tool (isolating pure leverage mechanics from financing cost), not a claim about real financing terms. The 5% arm remains the primary reference point (Estimated doctrine, not derived from this sweep). This dimension does not test any interaction between interest cost and Model B/C's triggers (a combined dimension, explicitly out of scope per `docs/PHASE3_SENSITIVITY_PLAN.md`).

## Interpretation rules (restated, applied throughout)

- **No winner was chosen.** Every table above reports all arms in full; none is marked "recommended" or "best."
- **No parameter was tuned after seeing results.** All nine sweep values (plus the two baselines) were fixed in `docs/PHASE3_SENSITIVITY_PLAN.md` before this run.
- **No claim of future superiority is made.** Every finding above describes this one simulated window only.
- **No simulated result has been converted into doctrine.** `targets.yaml`'s margin schema remains entirely absent; `CLAUDE.md`'s Decisions Log is unchanged by this document.

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
