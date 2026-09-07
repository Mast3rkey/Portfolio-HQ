# Transaction Cost Sensitivity Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history or real trading costs. Every figure below simulates a synthetic $0-start account through real historical prices; the 5bps/15bps cost tiers are disclosed Hypothetical assumptions, not measured Robinhood spread data (0bps reflects Robinhood's real, Known $0 commission structure). See `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` for the pre-approved design this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.

_Executed 2026-07-17. Window: 2021-06-01 to 2026-07-10. 62 monthly $2,000 deposits ($124,000 total). Control (no repayment, MODEL_0, 1.8x leverage): **35.59% ann. TWR, -26.81% MaxDD** — verified identical to the stored `docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. Each `repay_fraction` arm's gross (0bps) figures were likewise verified identical to that stored file before any cost was applied. Cost is applied as a first-order, lump-sum approximation (`transaction_cost_lib.cost_adjusted_twr()`) — not a fully compounded, re-simulated cost-aware backtest — per `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §6's disclosed simplification._

## repay_fraction = 10%

1. **Gross Model B result** (0bps, unadjusted): 34.62% ann. TWR, -25.84% MaxDD, 314 repayment events, $38,226 total repaid.
4. **Turnover metric**: 30.8% of total deposited capital (upper-bound estimate, per `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4's established methodology — the harness does not separately log the cash-vs-trim funding split per event).

| Cost tier | Label | Total cost | Cost % of repaid | 2. Assumed cost drag (TWR) | 3. Net cost-adjusted TWR | 5. Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|---:|---:|
| 0bps | Known | $0.00 | 0.000% | 0.0000pp | 34.62% | -0.98pp (suggestive) | -0.98pp (suggestive) |
| 5bps | Hypothetical | $19.11 | 0.050% | 0.0013pp | 34.61% | -0.98pp (suggestive) | -0.98pp (suggestive) |
| 15bps | Hypothetical | $57.34 | 0.150% | 0.0039pp | 34.61% | -0.98pp (suggestive) | -0.98pp (suggestive) |

## repay_fraction = 25%

1. **Gross Model B result** (0bps, unadjusted): 33.28% ann. TWR, -24.74% MaxDD, 296 repayment events, $88,516 total repaid.
4. **Turnover metric**: 71.4% of total deposited capital (upper-bound estimate, per `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4's established methodology — the harness does not separately log the cash-vs-trim funding split per event).

| Cost tier | Label | Total cost | Cost % of repaid | 2. Assumed cost drag (TWR) | 3. Net cost-adjusted TWR | 5. Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|---:|---:|
| 0bps | Known | $0.00 | 0.000% | 0.0000pp | 33.28% | -2.32pp (material) | -2.32pp (material) |
| 5bps | Hypothetical | $44.26 | 0.050% | 0.0031pp | 33.27% | -2.32pp (material) | -2.32pp (material) |
| 15bps | Hypothetical | $132.77 | 0.150% | 0.0094pp | 33.27% | -2.32pp (material) | -2.32pp (material) |

## repay_fraction = 50%

1. **Gross Model B result** (0bps, unadjusted): 32.03% ann. TWR, -23.65% MaxDD, 263 repayment events, $156,113 total repaid.
4. **Turnover metric**: 125.9% of total deposited capital (upper-bound estimate, per `docs/results/PHASE3_MODEL_B_ANALYSIS.md` §4's established methodology — the harness does not separately log the cash-vs-trim funding split per event).

| Cost tier | Label | Total cost | Cost % of repaid | 2. Assumed cost drag (TWR) | 3. Net cost-adjusted TWR | 5. Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|---:|---:|
| 0bps | Known | $0.00 | 0.000% | 0.0000pp | 32.03% | -3.56pp (material) | -3.56pp (material) |
| 5bps | Hypothetical | $78.06 | 0.050% | 0.0057pp | 32.03% | -3.56pp (material) | -3.56pp (material) |
| 15bps | Hypothetical | $234.17 | 0.150% | 0.0172pp | 32.02% | -3.56pp (material) | -3.58pp (material) |

## Directional observations

Reported as observed, per `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §8/§10 — no `repay_fraction` or cost tier is presented as preferred, and no deployment recommendation is made.

- At 0bps: total cost scales with `repay_fraction` (10%=$0.00, 25%=$0.00, 50%=$0.00) — monotonically increasing, consistent with turnover scaling with the repayment fraction (`docs/results/PHASE3_MODEL_B_ANALYSIS.md`'s original finding).
- At 5bps: total cost scales with `repay_fraction` (10%=$19.11, 25%=$44.26, 50%=$78.06) — monotonically increasing, consistent with turnover scaling with the repayment fraction (`docs/results/PHASE3_MODEL_B_ANALYSIS.md`'s original finding).
- At 15bps: total cost scales with `repay_fraction` (10%=$57.34, 25%=$132.77, 50%=$234.17) — monotonically increasing, consistent with turnover scaling with the repayment fraction (`docs/results/PHASE3_MODEL_B_ANALYSIS.md`'s original finding).

- Materiality classification (vs. control) change across any tested cost tier: **False** — at the tested cost magnitudes, the materiality band each `repay_fraction` arm's gap-vs-control falls into does or does not shift once cost is applied (see the per-arm tables above for the specific cells).

## Limitations

- **Dollar-volume cost model only** — does not account for per-trade-leg fragmentation (`_fund_repayment()` trims across every held position simultaneously per event; per-ticker trade counts are not logged anywhere in this harness). A minimum-fee-per-leg cost model, if one existed, could produce a materially different (likely higher) cost than this dollar-volume-only estimate, per `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` §3/§8.
- **First-order, lump-sum cost approximation** — cost is deducted once from the final book value, not compounded forward or reflected in reduced reinvestment capacity along the path.
- **MaxDD is not cost-adjusted** — a lagging, lump-sum deduction does not meaningfully change a peak-to-trough calculation; gross MaxDD is reported unchanged across all cost tiers for each `repay_fraction`.
- **5bps/15bps are disclosed Hypothetical assumptions**, not measured spread/slippage data — no real transaction-cost data exists anywhere in this repo to validate them against.
- **Model C is out of scope** — its measured repayment activity across every prior Phase 3G/4A run is zero or too small to price meaningfully.

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
