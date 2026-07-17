# Model B (Profit Harvest) — Consolidated Evidence Record

> **⚠️ Hypothetical, simulated.** Every figure in this document describes a synthetic $0-start account simulated through real historical prices — never a claim about this account's real history. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies throughout.

_Written 2026-07-17. Consolidates every Model B finding scattered across `docs/PHASE3_FINDINGS.md` (Phase 3E), `docs/PHASE3_SENSITIVITY_PLAN.md`/`docs/PHASE3_SENSITIVITY_RESULTS.md` (Phase 3G), `docs/results/PHASE3_MODEL_B_ANALYSIS.md` (Phase 3F), and `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md`/`docs/TRANSACTION_COST_SENSITIVITY_RESULTS.md` into one place, so "why do we believe what we believe about Model B" is answerable from a single document rather than four. Documentation only — no code, no doctrine, no parameter changes._

---

## The headline finding, stated narrowly

**The previously observed Model B signal is robust to the tested transaction-cost assumptions.** This is not "Model B is good," "Model B should be adopted," or "some `repay_fraction` is preferred." It is the narrower, defensible claim: an unresolved limitation (unpriced transaction cost) has been tested and did not change the conclusion already on record. Nothing about Model B's production status changes as a result of this document.

---

## 1. Original result (Phase 3E)

First execution, `repay_fraction=0.25`, against the D-0 (no-repayment) control at 1.8x leverage, 5% interest, real 2021-2026 price data, 63-ticker universe:

| | Ann. TWR | MaxDD |
|---|---:|---:|
| D-0 control | 35.59% | −26.81% |
| Model B (25%) | 33.28% | −24.74% |
| Gap | **−2.32pp** | **+2.07pp** (improvement) |

Both gaps cross the pre-committed 2.0pp decision threshold (`docs/PHASE3_SCENARIO_MANIFEST.md` §1) — a real, measured cost-for-benefit trade: less return, less drawdown.

## 2. Parameter sensitivity (Phase 3G)

Swept `repay_fraction` ∈ {10%, 25%, 50%}, all else held constant:

| repay_fraction | Ann. TWR | Gap vs. control | MaxDD | Gap vs. control | Turnover (upper bound) |
|---:|---:|---:|---:|---:|---:|
| 10% | 34.62% | −0.98pp | −25.84% | +0.97pp | 30.8% of deposited capital |
| 25% | 33.28% | −2.32pp | −24.74% | +2.07pp | 71.4% |
| 50% | 32.03% | −3.56pp | −23.65% | +3.16pp | 125.9% |

**Monotonic across the full sweep** — TWR cost and MaxDD benefit both scale with `repay_fraction`, in the expected direction, at every step. No non-monotonicity was found (a non-monotonic result would have been a flag to investigate the mechanism; it did not occur).

## 3. Event-level detail (Phase 3F, `docs/results/PHASE3_MODEL_B_ANALYSIS.md`)

At `repay_fraction=0.25` specifically: **296 repayment events**, **$88,516.45 gross repaid**, but only **$43,786.24 net debt reduction** versus the control — roughly half the gross figure, because Model B's harvesting doesn't stop the account's ordinary deposit-driven margin draws from redrawing against freed-up capacity (a profit-harvesting brake, not a leverage-elimination policy). A simple TWR/|MaxDD| ratio (1.345 for Model B vs. 1.328 for control) favored Model B marginally — offered there, and here, as one descriptive lens, not a verdict; the single-name/leverage decomposition this project's precedent (`t1t2_trim_backtest.md`'s NVDA case) applies before any adoption decision **was not performed** for Model B and remains outstanding.

## 4. Transaction-cost sensitivity (this cycle)

Re-ran all three `repay_fraction` arms, applied 0bps (Known — Robinhood's real $0 commission)/5bps/15bps (both Hypothetical — no real spread/slippage data exists to validate against) as a disclosed, first-order lump-sum cost approximation:

| repay_fraction | Cost @ 15bps | TWR erosion | Materiality classification (vs. control) |
|---:|---:|---:|---|
| 10% | $57.34 | 0.0039pp | suggestive → **unchanged** |
| 25% | $132.77 | 0.0094pp | material → **unchanged** |
| 50% | $234.17 | 0.0172pp | material → **unchanged** |

Cost erosion, even at the 15bps ceiling, is **three orders of magnitude smaller** than the already-observed TWR/MaxDD gaps (0.004–0.017pp of cost drag against 0.98–3.56pp of observed effect). No materiality classification shifted at any tested `repay_fraction` × cost-tier combination.

### What this does, and does not, resolve

The turnover finding itself is **not** made irrelevant by this result — turnover is real and scales exactly as measured (30.8% → 71.4% → 125.9% of deposited capital). What's resolved is narrower: **the specific bps-based spread/slippage cost this pass tested was too small, at the tested magnitudes, to move the conclusion.** The open question was never really "can bid-ask spreads absorb 15bps of a $88,516 repaid total" — that was always going to be a small number relative to the observed multi-percentage-point gaps. The genuinely open questions this result does **not** address are the non-bps effects of frequent forced portfolio adjustment:

- **Tax treatment** — repeated trim-and-repay cycles realize gains/losses in a real taxable context; nothing in this project has ever modeled tax consequences, and this transaction-cost pass explicitly did not either (`docs/TRANSACTION_COST_SENSITIVITY_PLAN.md` never claimed to).
- **Market impact under stress** — the bps assumption was a flat, unconditional rate; it does not model spreads widening specifically during the volatile periods a forced repayment trim is most likely to coincide with.
- **Execution timing** — this harness executes every trade instantly at that day's close; nothing models slippage from actually working an order.
- **Behavioral friction** — the cost of a human executing 296 small forced trades over five years, a cost this project has never attempted to price for any mechanical rule (the same caveat `regime_backtest.md` and `t1t2_trim_backtest.md` have both carried for their own trim mechanisms).

## 5. What is now answered vs. still unresolved

| Question | Status |
|---|---|
| Does Model B show a measurable TWR/MaxDD trade-off vs. the no-repayment control? | **Answered.** Yes, material, monotonic across the tested `repay_fraction` range (§1/§2). |
| How much debt does Model B actually reduce, net of the account's ordinary re-draws? | **Answered.** Roughly half the gross repaid figure (§3). |
| Does the finding survive a bps-based transaction cost assumption? | **Answered, this cycle.** Yes, at 0/5/15bps — materiality classification unchanged (§4). |
| Does the finding survive tax treatment? | **Unresolved.** No tax model exists anywhere in this project. |
| Does the finding survive stress-regime execution conditions (widened spreads, slippage, timing)? | **Unresolved.** This window (2021-2026) is a mostly-rising sample; the bps assumption was flat and unconditional. |
| Does the finding survive behavioral-friction costs? | **Unresolved.** Never modeled for any mechanical rule in this project. |
| Has the single-name/leverage decomposition (this project's own adoption bar) been performed for Model B? | **Not performed.** Outstanding since Phase 3F. |
| Is any `repay_fraction` value preferred, optimal, or ready for selection? | **No, and this document does not change that.** The ranking across 10%/25%/50% remains a future research question, not a decision this evidence base supports making. |

## Explicit statement: no parameter selection

**This document does not conclude that 25% is optimal, that 50% is too aggressive, or that any `repay_fraction` should be preferred over another.** The only conclusion this evidence base supports is: *transaction cost sensitivity, at the tested magnitudes, did not overturn the existing Model B observation.* Selecting or recommending a specific fraction would require resolving the unanswered questions in §5 first (at minimum tax treatment and the single-name decomposition), and even then would be a separate, explicit decision this document does not make.

## No doctrine change

Nothing in this document alters `targets.yaml`'s (still entirely `null`) margin schema, `CLAUDE.md`'s Decisions Log, or any production file. Model B remains a tested simulation policy with no live deployment status, exactly as it has been since Phase 3D.

---

## What this document deliberately does not do

- Does not run any new simulation — every figure above is quoted from an already-committed source document, not recomputed.
- Does not select, rank, or recommend a `repay_fraction`.
- Does not modify any code, test, or production file.
- Does not resolve tax treatment, stress-regime execution, or behavioral-friction questions — it names them as the genuinely open items this cycle's result narrows the field down to.

Stopping here. This is a consolidation record, not a call to further action.
