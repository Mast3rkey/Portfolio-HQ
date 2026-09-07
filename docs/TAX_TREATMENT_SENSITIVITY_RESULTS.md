# Tax Treatment Sensitivity Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history or real tax liability. Every figure below simulates a synthetic $0-start account through real historical prices. The taxable-realization figure is a disclosed **upper bound** (100% of each repayment event's dollar amount treated as realized gain), **never** converted into an estimate of actual realized gain or actual tax owed. The 15%/32% rate tiers are disclosed Hypothetical, illustrative federal brackets, not this account's confirmed rate. State tax is excluded, not assumed zero. See `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` for the pre-approved design this run follows, and `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer.

_Executed 2026-07-17. Window: 2021-06-01 to 2026-07-10. 62 monthly $2,000 deposits. Control (no repayment, MODEL_0, 1.8x leverage): **35.59% ann. TWR, -26.81% MaxDD** — verified identical to the stored `docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. Each `repay_fraction` arm's gross figures were likewise verified identical to that stored file before any tax assumption was applied. Tax sensitivity is applied ONLY to repayment-generated realized amounts (`taxable_realization_upper_bound()`'s `kind="repayment"` filter) — deposits, interest accrual, margin draws, and unrealized gains are explicitly excluded._

## repay_fraction = 10%

1. **Gross Model B result**: 34.62% ann. TWR, -25.84% MaxDD, 314 repayment events.
2. **Upper-bound taxable realization assumption**: $38,225.89 — 100% of every repayment event's dollar amount, treated as realized gain. This is a ceiling, not an estimate of actual realized gain (no cost-basis tracking exists in this harness, and none was added to produce this figure).

| Rate tier | Label | 3. Assumed tax drag | Net TWR | Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|
| 0% | Known (no tax, control) | $0.00 (0.0000pp) | 4. **34.62%** | -0.98pp (suggestive) | 5. -0.98pp (suggestive) |
| 15% | Hypothetical (illustrative federal bracket) | $5,733.88 (0.3969pp) | 4. **34.22%** | -0.98pp (suggestive) | 5. -1.37pp (suggestive) |
| 32% | Hypothetical (illustrative federal bracket) | $12,232.28 (0.8526pp) | 4. **33.76%** | -0.98pp (suggestive) | 5. -1.83pp (suggestive) |

**Holding-period bracket** (brackets the unknowable true short/long-term mix rather than guessing a blend):

| Case | Rate used | Net TWR | Gap vs. control (net) |
|---|---:|---:|---:|
| All long-term (optimistic bound) | 15% | 34.22% | -1.37pp (suggestive) |
| All short-term (pessimistic bound) | 32% | 33.76% | -1.83pp (suggestive) |

## repay_fraction = 25%

1. **Gross Model B result**: 33.28% ann. TWR, -24.74% MaxDD, 296 repayment events.
2. **Upper-bound taxable realization assumption**: $88,516.45 — 100% of every repayment event's dollar amount, treated as realized gain. This is a ceiling, not an estimate of actual realized gain (no cost-basis tracking exists in this harness, and none was added to produce this figure).

| Rate tier | Label | 3. Assumed tax drag | Net TWR | Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|
| 0% | Known (no tax, control) | $0.00 (0.0000pp) | 4. **33.28%** | -2.32pp (material) | 5. -2.32pp (material) |
| 15% | Hypothetical (illustrative federal bracket) | $13,277.47 (0.9576pp) | 4. **32.32%** | -2.32pp (material) | 5. -3.27pp (material) |
| 32% | Hypothetical (illustrative federal bracket) | $28,325.26 (2.0783pp) | 4. **31.20%** | -2.32pp (material) | 5. -4.39pp (material) |

**Holding-period bracket** (brackets the unknowable true short/long-term mix rather than guessing a blend):

| Case | Rate used | Net TWR | Gap vs. control (net) |
|---|---:|---:|---:|
| All long-term (optimistic bound) | 15% | 32.32% | -3.27pp (material) |
| All short-term (pessimistic bound) | 32% | 31.20% | -4.39pp (material) |

## repay_fraction = 50%

1. **Gross Model B result**: 32.03% ann. TWR, -23.65% MaxDD, 263 repayment events.
2. **Upper-bound taxable realization assumption**: $156,112.51 — 100% of every repayment event's dollar amount, treated as realized gain. This is a ceiling, not an estimate of actual realized gain (no cost-basis tracking exists in this harness, and none was added to produce this figure).

| Rate tier | Label | 3. Assumed tax drag | Net TWR | Gap vs. control (gross) | Gap vs. control (net) |
|---|---|---:|---:|---:|---:|
| 0% | Known (no tax, control) | $0.00 (0.0000pp) | 4. **32.03%** | -3.56pp (material) | 5. -3.56pp (material) |
| 15% | Hypothetical (illustrative federal bracket) | $23,416.88 (1.7667pp) | 4. **30.27%** | -3.56pp (material) | 5. -5.33pp (material) |
| 32% | Hypothetical (illustrative federal bracket) | $49,956.00 (3.8950pp) | 4. **28.14%** | -3.56pp (material) | 5. -7.45pp (material) |

**Holding-period bracket** (brackets the unknowable true short/long-term mix rather than guessing a blend):

| Case | Rate used | Net TWR | Gap vs. control (net) |
|---|---:|---:|---:|
| All long-term (optimistic bound) | 15% | 30.27% | -5.33pp (material) |
| All short-term (pessimistic bound) | 32% | 28.14% | -7.45pp (material) |

## Materiality comparison summary

Materiality classification (vs. control) changed at any tested `repay_fraction` × tax-rate combination: **False**. Per `docs/PHASE4A_MATERIALITY_THRESHOLDS.md`'s existing 2.0pp material / 0.5pp noise-floor bands, reused unchanged.

## What this analysis does not resolve

- **Not an estimate of actual tax owed** — every dollar figure above is derived from the 100%-of-trim upper-bound assumption (§2 in each arm's section), never from actual cost-basis or realized-gain data, because none exists in this harness and none was added to produce this analysis (`docs/TAX_TREATMENT_SENSITIVITY_PLAN.md` §3/§5's explicit "no cost-basis tracking" constraint).
- **Not this account's actual tax rate or jurisdiction** — 15%/32% are illustrative federal brackets only; state tax is excluded entirely, not modeled as zero.
- **Not the true short/long-term mix** — bracketed by two extremes (all-LT, all-ST), not estimated as a blend, because the true mix is unknowable from this harness's data.
- **No repayment policy conclusion** — this analysis does not select, rank, or recommend any `repay_fraction`, at any tax assumption.

_Advisory-adjacent research only. This report places no orders and makes no recommendation. Execute nothing based on this document alone._
