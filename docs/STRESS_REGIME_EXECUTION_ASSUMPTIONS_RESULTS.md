# Stress-Regime Execution Assumptions — Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history or real market liquidity conditions. Stress windows below are detected from real, already-cached OHLCV data as a volatility/liquidity **proxy** — never a measurement of actual bid-ask spread or market depth. Execution is assumed to fill instantly at each day's close, calm or stressed; this analysis does not model or resolve execution failure. The hypothetical-secondary cost multiplier is a disclosed, bounded assumption, kept **strictly separate** from the historical-primary (assumption-free) measurements below. See `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md` for the pre-approved design this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.

_Executed 2026-07-17. Window: 2021-06-01 to 2026-07-10 (1283 simulated trading days). Control (no repayment, MODEL_0, 1.8x leverage — read-only reference, not examined or changed): **35.59% ann. TWR, -26.81% MaxDD** — verified identical to the stored `docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. Each `repay_fraction` arm's gross figures were likewise verified identical to that stored file before any stress-regime analysis was applied._

**Stress-window detection** (reference: QQQ's real OHLCV data, 60-day trailing baseline, 1.5x range or 0.7x volume threshold, windows ≥3 days, merged within 5 days): **21 window(s) detected**, covering **12.2%** of the 1283 simulated trading days. All parameters are disclosed session choices, not separately pre-negotiated values.

## repay_fraction = 10%

**Gross Model B result**: 34.62% ann. TWR, -25.84% MaxDD, 314 repayment events.

### Historical-primary (real stress windows, no cost/tax assumption)

- **Repayment events during/near stress windows**: 24 inside detected stress windows, 290 outside.
- **Turnover concentration**: 5.9% of repaid dollars occurred inside stress windows, versus a base rate of 12.2% of all simulated days being stress-flagged — repayment dollar volume is **under-represented** relative to how much of the calendar stress periods occupy.
- **Recovery time**: 27 trading days (trough at simulated day 968).
- **Drawdown impact**: -25.84% MaxDD (gross, unchanged by this analysis — see `docs/results/PHASE3_MODEL_B_ANALYSIS.md` for the already-published figure this reproduces).
- **Threshold exposure**: 0.0% of simulated days spent above 95% of the 1.8x leverage cap — not material per the 5%-of-days bar.

### Hypothetical-secondary (disclosed regime-conditional cost overlay)

Base rate: 15bps (reused from the already-approved transaction-cost tier). Stress multiplier: 3.0x, applied only to events falling inside a detected stress window (disclosed, new to this analysis, not a validated real-world value).

| | Cost | Net TWR | Gap vs. control | Classification |
|---|---:|---:|---:|---|
| Flat 15bps (no regime conditioning) | $57.34 | 34.61% | -0.98pp | suggestive |
| Regime-conditional (3x inside stress windows) | $64.05 | 34.61% | -0.98pp | suggestive |

Cost delta from regime conditioning: $6.71 (the additional hypothetical cost attributable to elevating the rate specifically for in-window events, versus the flat-rate baseline).

## repay_fraction = 25%

**Gross Model B result**: 33.28% ann. TWR, -24.74% MaxDD, 296 repayment events.

### Historical-primary (real stress windows, no cost/tax assumption)

- **Repayment events during/near stress windows**: 20 inside detected stress windows, 276 outside.
- **Turnover concentration**: 5.9% of repaid dollars occurred inside stress windows, versus a base rate of 12.2% of all simulated days being stress-flagged — repayment dollar volume is **under-represented** relative to how much of the calendar stress periods occupy.
- **Recovery time**: 27 trading days (trough at simulated day 968).
- **Drawdown impact**: -24.74% MaxDD (gross, unchanged by this analysis — see `docs/results/PHASE3_MODEL_B_ANALYSIS.md` for the already-published figure this reproduces).
- **Threshold exposure**: 0.0% of simulated days spent above 95% of the 1.8x leverage cap — not material per the 5%-of-days bar.

### Hypothetical-secondary (disclosed regime-conditional cost overlay)

Base rate: 15bps (reused from the already-approved transaction-cost tier). Stress multiplier: 3.0x, applied only to events falling inside a detected stress window (disclosed, new to this analysis, not a validated real-world value).

| | Cost | Net TWR | Gap vs. control | Classification |
|---|---:|---:|---:|---|
| Flat 15bps (no regime conditioning) | $132.77 | 33.27% | -2.32pp | material |
| Regime-conditional (3x inside stress windows) | $148.56 | 33.27% | -2.33pp | material |

Cost delta from regime conditioning: $15.78 (the additional hypothetical cost attributable to elevating the rate specifically for in-window events, versus the flat-rate baseline).

## repay_fraction = 50%

**Gross Model B result**: 32.03% ann. TWR, -23.65% MaxDD, 263 repayment events.

### Historical-primary (real stress windows, no cost/tax assumption)

- **Repayment events during/near stress windows**: 20 inside detected stress windows, 243 outside.
- **Turnover concentration**: 6.9% of repaid dollars occurred inside stress windows, versus a base rate of 12.2% of all simulated days being stress-flagged — repayment dollar volume is **under-represented** relative to how much of the calendar stress periods occupy.
- **Recovery time**: 27 trading days (trough at simulated day 968).
- **Drawdown impact**: -23.65% MaxDD (gross, unchanged by this analysis — see `docs/results/PHASE3_MODEL_B_ANALYSIS.md` for the already-published figure this reproduces).
- **Threshold exposure**: 0.0% of simulated days spent above 95% of the 1.8x leverage cap — not material per the 5%-of-days bar.

### Hypothetical-secondary (disclosed regime-conditional cost overlay)

Base rate: 15bps (reused from the already-approved transaction-cost tier). Stress multiplier: 3.0x, applied only to events falling inside a detected stress window (disclosed, new to this analysis, not a validated real-world value).

| | Cost | Net TWR | Gap vs. control | Classification |
|---|---:|---:|---:|---|
| Flat 15bps (no regime conditioning) | $234.17 | 32.02% | -3.58pp | material |
| Regime-conditional (3x inside stress windows) | $266.31 | 32.01% | -3.58pp | material |

Cost delta from regime conditioning: $32.15 (the additional hypothetical cost attributable to elevating the rate specifically for in-window events, versus the flat-rate baseline).

## Materiality and outcome gate

Reused, not reinvented: 2.0pp material / 0.5pp noise floor, 5%-of-days threshold-exposure bar (`docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3/§6), and the **adopted future outcome gate** (material gap AND (repeated forced-deleveraging events OR material threshold-exposure degradation), per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adoption) — this research cycle is exactly the future cycle that adoption was written for. No new threshold was introduced or optimized by this analysis.

## What this analysis does not resolve

- **Not measured liquidity data** — the stress-window detector uses real OHLCV range/volume as a proxy; no bid-ask spread or market-depth data exists anywhere in this repo.
- **Not a model of execution failure** — every trade in every scenario, calm or stressed, is assumed to fill instantly at that day's close.
- **Not a validated regime-conditional cost multiplier** — the 3x figure is a disclosed, bounded Hypothetical assumption specific to this analysis, not a measured or expected real-world value.
- **No repayment fraction selected, no implementation recommended, no doctrine changed, no leverage cap examined or changed, no threshold optimized** — per `docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md` §6.

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
