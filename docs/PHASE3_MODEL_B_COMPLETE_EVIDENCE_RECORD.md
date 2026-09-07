# Model B (Profit Harvest) — Complete Evidence Record

> **⚠️ Hypothetical, simulated.** Every figure in this document describes a synthetic $0-start account simulated through real historical prices — never a claim about this account's real history, real tax liability, or real trading costs. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies throughout.

_Written 2026-07-17. The single canonical evidence record for Model B, consolidating `docs/PHASE3_FINDINGS.md` (Phase 3E), `docs/PHASE3_SENSITIVITY_PLAN.md`/`RESULTS.md` (Phase 3G), `docs/results/PHASE3_MODEL_B_ANALYSIS.md` (Phase 3F), `docs/TRANSACTION_COST_SENSITIVITY_PLAN.md`/`RESULTS.md`, and `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md`/`RESULTS.md`. Supersedes `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` as the canonical reference — that document is not deleted (it remains an accurate, dated snapshot of the evidence as it stood before the tax-sensitivity pass) but this document is now the one to read for "what do we currently know about Model B." Documentation only — no code, no simulation, no new assumptions. Every figure below is quoted from an already-committed source, not recomputed._

---

## 1. Original observation (Phase 3E)

First execution, `repay_fraction=0.25`, against the D-0 (no-repayment) control at 1.8x leverage, 5% interest, real 2021-2026 price data, 63-ticker universe:

| | Ann. TWR | MaxDD |
|---|---:|---:|
| D-0 control | 35.59% | −26.81% |
| Model B (25%) | 33.28% | −24.74% |
| Gap | **−2.32pp** | **+2.07pp** (improvement) |

Both gaps cross the pre-committed 2.0pp decision threshold (`docs/PHASE3_SCENARIO_MANIFEST.md` §1). Phase 3G's `repay_fraction` sweep (10%/25%/50%) confirmed this is monotonic — TWR cost and MaxDD benefit both scale with the fraction at every step, no non-monotonicity found. Phase 3F's event-level detail: at 25%, 296 repayment events, $88,516.45 gross repaid, but only $43,786.24 net debt reduction versus the control (roughly half — Model B is a profit-harvesting brake, not a leverage-elimination policy, since the account's ordinary deposit-driven margin draws continue independently).

## 2. Transaction-cost sensitivity

Tested 0bps (Known — Robinhood's real $0 commission) / 5bps / 15bps (both Hypothetical spread/slippage proxies, no real data to validate against) against all three `repay_fraction` arms:

| repay_fraction | Turnover (upper bound) | Cost @ 15bps | TWR erosion |
|---:|---:|---:|---:|
| 10% | 30.8% of deposited capital | $57.34 | 0.0039pp |
| 25% | 71.4% | $132.77 | 0.0094pp |
| 50% | 125.9% | $234.17 | 0.0172pp |

**Conclusion: turnover looked large, tested costs were small.** Cost erosion, even at the 15bps ceiling, was three orders of magnitude smaller than the observed TWR/MaxDD gaps. Materiality classification (material/suggestive/noise vs. control) did not change at any tested `repay_fraction` × cost-tier combination. This closed the bid-ask-spread question specifically — it did not, and was never claimed to, address tax, market impact under stress, execution timing, or behavioral friction.

## 3. Tax sensitivity

Same repayment mechanics, same measured events, same three `repay_fraction` values — a different friction source. Applied a disclosed, upper-bound realized-gain assumption (100% of each repayment event's dollar amount treated as gain — a ceiling, never converted into an estimate, since this harness has no cost-basis tracking and none was added to produce this analysis) at 0% (Known/control) / 15% / 32% (both Hypothetical, illustrative federal brackets, not this account's confirmed rate), bracketed by an all-long-term/all-short-term holding-period assumption rather than a guessed blend:

| repay_fraction | Gross gap vs. control | Net gap @ 15% (all-LT) | Net gap @ 32% (all-ST) |
|---:|---:|---:|---:|
| 10% | −0.98pp | −1.37pp | −1.83pp |
| 25% | −2.32pp | −3.27pp | −4.39pp |
| 50% | −3.56pp | −5.33pp | −7.45pp |

**Conclusion: unlike transaction costs, tax friction under the worst-case upper bound is not negligible.** At 50%/32%, the gap more than doubles (−3.56pp → −7.45pp). The classification itself stayed "material" rather than crossing a new boundary (those cells were already material pre-tax at 25% and 50%), but the underlying magnitude changed substantially — a materially different character of finding than the transaction-cost result. **The important observation: the effect scales with repayment intensity** — exactly what a realization-based friction (more trims, more realized gains, more tax) would be expected to do, and exactly what a per-trade spread cost, which scaled but stayed small in dollar terms relative to the account, did not show as dramatically.

## 4. What changed interpretation

Before the tax pass, the working interpretation (per `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md`) was: "the previously observed Model B signal is robust to the tested transaction-cost assumptions" — a narrow, real, but limited claim, since only one friction category had been tested.

**What changed:** transaction costs and taxes are not interchangeable stand-ins for "trading friction" — they behave differently under the same mechanics. The transaction-cost result generalized to "friction doesn't matter much here." The tax result does not generalize that far; it demonstrates the opposite is possible for a different friction category applied to the exact same events. **The correct, narrower interpretation, stated precisely: under the stated worst-case realized-gain upper-bound assumptions, tax friction can materially change the *magnitude* of the Model B effect — not that Model B's effect disappears, reverses, or was wrong, but that the size of the effect is more sensitive to this particular unresolved assumption than it was to the bps-cost assumption already closed.**

### What this does show

- A repayment policy has economic friction beyond commissions/spreads.
- Higher repayment fractions create larger sensitivity to tax assumptions (the scaling relationship in §3).
- The existing gross-return comparison (§1, and every Phase 3E/3G/3F figure prior to this pass) understates *possible* real-world friction — "possible," because the tax figures are an intentionally severe upper bound, not a prediction.

### What this does not show

- That taxes will actually be this high for this account.
- That any specific tax bracket, jurisdiction, or filing status applies.
- That repayment (Model B, at any fraction) should be avoided.
- That any specific `repay_fraction` is inferior to another.

The upper-bound assumption in §3 is deliberately severe by design (§5 of `docs/TAX_TREATMENT_SENSITIVITY_PLAN.md`) — it exists to bound the worst case honestly, not to forecast the likely case.

## 5. Current Model B evidence stack

**Supports:**
- Model B produces a measurable simulated effect (§1), monotonic across the tested `repay_fraction` range.
- Transaction costs alone do not erase it (§2).
- Tax friction, under a deliberately severe upper bound, can materially reduce the magnitude of that effect (§3) — a real, evidence-based caution, not a refutation.

**Still unknown:**
- Actual cost basis (this harness has none; not modeled, not estimated).
- Holding-period distribution (bracketed by two extremes in §3, never resolved to an actual mix).
- Account-specific tax treatment (jurisdiction, marginal rate, filing status — all genuinely unknown, none assumed).
- Stress-period execution behavior (widened spreads, slippage, delayed fills under real market stress — untested by either sensitivity pass; both used flat, unconditional assumptions across the whole window).
- The single-name/leverage decomposition this project's own precedent (`t1t2_trim_backtest.md`'s NVDA case) requires before any adoption-level judgment — still not performed for Model B, unchanged since Phase 3F.

## 6. No doctrine recommendation

**This document makes no recommendation about Model B, any `repay_fraction`, or any production change.** `targets.yaml`'s margin schema remains entirely `null`. `CLAUDE.md`'s Decisions Log is unchanged. Model B remains a tested simulation policy with no live deployment status, exactly as it has been since Phase 3D. Consolidating five documents' worth of evidence into one canonical record does not itself constitute, authorize, or imply a step toward adoption — per the standing rule restated in every prior document in this line of work, any production change requires its own separate, explicit approval step, regardless of how much evidence accumulates in its favor or against it.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure — every number above is quoted from an already-committed source (§1-3 cite the specific documents).
- Does not introduce any new assumption, sensitivity case, or dimension beyond what Phases 3E/3F/3G and the transaction-cost/tax passes already produced.
- Does not select, rank, or recommend a `repay_fraction`.
- Does not change any doctrine, production file, or prior document's own conclusions — `docs/PHASE3_MODEL_B_EVIDENCE_UPDATE.md` remains on record as an accurate snapshot of its own moment, not retracted or edited.
- Does not decide what research comes next — that remains a separate decision, tracked in `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`.

Stopping here. This is a consolidation record, not a call to further action.
