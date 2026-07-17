# Phase 6A — Tax Lot Analysis Results

> **⚠️ hypothetical, simulated.** Not a claim about this account's real history, real cost basis, or real tax liability. The FIFO lot ledger is built entirely from a synthetic $0-start account's own simulated purchase history through real historical prices — never from real trade data. FIFO is a disclosed default convention (`docs/PHASE6A_ASSUMPTION_REGISTRY.md` #3), not a confirmed fact about this account's real elected convention. The 15%/32% rate tiers remain disclosed Hypothetical illustrative federal brackets. State tax, wash-sale rules, AMT, and NIIT remain excluded, not assumed zero-impact. See `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` for the pre-approved design this run follows.

_Executed 2026-07-17. Window: 2021-06-01 to 2026-07-10. Control (no repayment, MODEL_0, 1.8x leverage): **35.59% ann. TWR, -26.81% MaxDD** — verified identical to the stored `docs/results/PHASE3_SENSITIVITY_RESULTS.json` value before this run proceeded. Each `repay_fraction` arm's gross TWR/MaxDD/event count were likewise re-verified identical to that stored file (the same verify-before-comparing gate already run interactively) before any tax computation was applied._

## repay_fraction = 10%

**Gross Model B result**: 34.62% ann. TWR, -25.84% MaxDD, 314 repayment events.

### 1. Tax realization metrics (FIFO lot ledger)

- Disposal events: 19450 (14293 gain, 5156 loss)
- Total proceeds: $37,879.11
- Total cost basis: $23,484.23
- Total realized gains: $16,235.40
- Total realized losses: $-1,840.52
- Net realized gain: $14,394.88
- Average holding period (proceeds-weighted): 1149.9 days
- Gain split: 1.4% short-term ($228.46), 98.6% long-term ($16,006.94)

### 2. Tax sensitivity (FIFO-realistic taxable base)

FIFO-realistic taxable base (net realized gain, floored at $0 — `phase6a_tax_lot_lib.net_taxable_base()`): **$14,394.88**

| Rate tier | Label | Tax drag | Net TWR | Gap vs. control | Classification |
|---|---|---:|---:|---:|---|
| 0% | Known (no tax, control) | $0.00 | 34.62% | -0.98pp | suggestive |
| 15% | Hypothetical (illustrative federal bracket) | $2,159.23 | 34.47% | -1.12pp | suggestive |
| 32% | Hypothetical (illustrative federal bracket) | $4,606.36 | 34.30% | -1.29pp | suggestive |

### 3. Comparison against the Phase 3G worst-case upper-bound tax model

Upper-bound taxable base (100% of every repaid dollar treated as gain, `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json`): **$38,225.89**
FIFO-realistic taxable base: **$14,394.88** — a **62.3% reduction** from the upper bound.

| Rate tier | Upper-bound net TWR | Upper-bound gap | FIFO-realistic net TWR | FIFO-realistic gap |
|---|---:|---:|---:|---:|
| 0% | 34.62% | -0.98pp (suggestive) | 34.62% | -0.98pp (suggestive) |
| 15% | 34.22% | -1.37pp (suggestive) | 34.47% | -1.12pp (suggestive) |
| 32% | 33.76% | -1.83pp (suggestive) | 34.30% | -1.29pp (suggestive) |

**Outcome category (per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adopted three-way framework, applied to the 15%/32% tiers): Evidence inconclusive**

## repay_fraction = 25%

**Gross Model B result**: 33.28% ann. TWR, -24.74% MaxDD, 296 repayment events.

### 1. Tax realization metrics (FIFO lot ledger)

- Disposal events: 19344 (14781 gain, 4563 loss)
- Total proceeds: $88,491.20
- Total cost basis: $50,272.17
- Total realized gains: $41,302.11
- Total realized losses: $-3,083.08
- Net realized gain: $38,219.04
- Average holding period (proceeds-weighted): 961.7 days
- Gain split: 1.2% short-term ($495.92), 98.8% long-term ($40,806.19)

### 2. Tax sensitivity (FIFO-realistic taxable base)

FIFO-realistic taxable base (net realized gain, floored at $0 — `phase6a_tax_lot_lib.net_taxable_base()`): **$38,219.04**

| Rate tier | Label | Tax drag | Net TWR | Gap vs. control | Classification |
|---|---|---:|---:|---:|---|
| 0% | Known (no tax, control) | $0.00 | 33.28% | -2.32pp | material |
| 15% | Hypothetical (illustrative federal bracket) | $5,732.86 | 32.87% | -2.73pp | material |
| 32% | Hypothetical (illustrative federal bracket) | $12,230.09 | 32.40% | -3.20pp | material |

### 3. Comparison against the Phase 3G worst-case upper-bound tax model

Upper-bound taxable base (100% of every repaid dollar treated as gain, `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json`): **$88,516.45**
FIFO-realistic taxable base: **$38,219.04** — a **56.8% reduction** from the upper bound.

| Rate tier | Upper-bound net TWR | Upper-bound gap | FIFO-realistic net TWR | FIFO-realistic gap |
|---|---:|---:|---:|---:|
| 0% | 33.28% | -2.32pp (material) | 33.28% | -2.32pp (material) |
| 15% | 32.32% | -3.27pp (material) | 32.87% | -2.73pp (material) |
| 32% | 31.20% | -4.39pp (material) | 32.40% | -3.20pp (material) |

**Outcome category (per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adopted three-way framework, applied to the 15%/32% tiers): Evidence supports**

## repay_fraction = 50%

**Gross Model B result**: 32.03% ann. TWR, -23.65% MaxDD, 263 repayment events.

### 1. Tax realization metrics (FIFO lot ledger)

- Disposal events: 17738 (13933 gain, 3805 loss)
- Total proceeds: $156,112.51
- Total cost basis: $88,970.43
- Total realized gains: $71,771.08
- Total realized losses: $-4,629.00
- Net realized gain: $67,142.08
- Average holding period (proceeds-weighted): 813.7 days
- Gain split: 1.3% short-term ($907.04), 98.7% long-term ($70,864.04)

### 2. Tax sensitivity (FIFO-realistic taxable base)

FIFO-realistic taxable base (net realized gain, floored at $0 — `phase6a_tax_lot_lib.net_taxable_base()`): **$67,142.08**

| Rate tier | Label | Tax drag | Net TWR | Gap vs. control | Classification |
|---|---|---:|---:|---:|---|
| 0% | Known (no tax, control) | $0.00 | 32.03% | -3.56pp | material |
| 15% | Hypothetical (illustrative federal bracket) | $10,071.31 | 31.29% | -4.31pp | material |
| 32% | Hypothetical (illustrative federal bracket) | $21,485.46 | 30.42% | -5.18pp | material |

### 3. Comparison against the Phase 3G worst-case upper-bound tax model

Upper-bound taxable base (100% of every repaid dollar treated as gain, `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.json`): **$156,112.51**
FIFO-realistic taxable base: **$67,142.08** — a **57.0% reduction** from the upper bound.

| Rate tier | Upper-bound net TWR | Upper-bound gap | FIFO-realistic net TWR | FIFO-realistic gap |
|---|---:|---:|---:|---:|
| 0% | 32.03% | -3.56pp (material) | 32.03% | -3.56pp (material) |
| 15% | 30.27% | -5.33pp (material) | 31.29% | -4.31pp (material) |
| 32% | 28.14% | -7.45pp (material) | 30.42% | -5.18pp (material) |

**Outcome category (per `docs/PHASE4A_OUTCOME_GATE_REVIEW.md`'s adopted three-way framework, applied to the 15%/32% tiers): Evidence supports**

## 4. Materiality framework applied

Reused, not reinvented: 2.0pp material / 0.5pp noise floor (`docs/PHASE4A_MATERIALITY_THRESHOLDS.md` §2/§3), and the three-way outcome framework (Evidence supports / Evidence does not support / Evidence inconclusive) adopted in `docs/PHASE4A_OUTCOME_GATE_REVIEW.md` and reused throughout every sensitivity pass since. No new threshold introduced or optimized by this analysis.

## Summary: did realistic FIFO lot accounting change the interpretation?

- **10%**: taxable base fell 62.3% ($38,225.89 → $14,394.88); outcome category **Evidence inconclusive**.
- **25%**: taxable base fell 56.8% ($88,516.45 → $38,219.04); outcome category **Evidence supports**.
- **50%**: taxable base fell 57.0% ($156,112.51 → $67,142.08); outcome category **Evidence supports**.

## What this analysis does not resolve

- **Not this account's real cost basis** — the FIFO lot ledger is built entirely from the synthetic simulation's own purchase history.
- **Not this account's real elected lot-consumption convention** — FIFO is a disclosed default, not a confirmed fact.
- **Not this account's real tax rate, filing status, or jurisdiction** — the 0%/15%/32% tiers remain illustrative federal brackets only.
- **Not a model of wash-sale rules, AMT, NIIT, or loss carryforward benefit** — a net realized loss is floored at $0 taxable base, not treated as a deduction against other income.
- **No repayment fraction selected, no implementation recommended, no doctrine changed, no leverage cap examined or changed** — per `docs/PHASE6A_IMPLEMENTATION_APPROVAL.md` §3.

_Advisory-adjacent research only. This report places no orders and makes no recommendation about Model B, any repay_fraction, or any production change. Execute nothing based on this document alone._
