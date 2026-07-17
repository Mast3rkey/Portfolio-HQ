# Phase 6A — Tax Lot Evidence Record

> **⚠️ Hypothetical, simulated.** Every figure in this document describes a synthetic $0-start account simulated through real historical prices — never a claim about this account's real history, real cost basis, or real tax liability. See `docs/PHASE3_FINDINGS.md` §8 for the full disclaimer, which applies throughout.

_Written 2026-07-17. The canonical evidence record for Phase 6A (tax-lot / FIFO realized-gain modeling), consolidating `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md`, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`, `docs/PHASE6A_DATA_REQUIREMENTS.md`, `docs/PHASE6A_IMPLEMENTATION_APPROVAL.md`, and `docs/PHASE6A_TAX_LOT_ANALYSIS.md`/`.json`. Documentation only — no code, no simulation, no new assumptions. Every figure below is quoted from an already-committed source, not recomputed._

**Preserved, unchanged, by this document:** `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` (the upper-bound tax result remains on record exactly as written) and `docs/PHASE5B_GOVERNANCE_DECISION.md` (the "maintain current doctrine" decision is not revisited here — that is Prompt 7's scope, not this one).

---

## 1. What was tested

- **Objective** (per `PHASE6A_TAX_LOT_MODELING_PLAN.md` §2): how much of the already-measured worst-case upper-bound tax effect (`docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`) survives realistic per-lot cost-basis and holding-period accounting.
- **Mechanism**: a per-ticker FIFO lot ledger, added additively to `margin_simulation.py`, records every simulated purchase as a discrete lot (acquisition day, acquisition date, cost-basis price) and consumes lots oldest-first on every sale, computing realized proceeds, realized gain, and an actual (not bracketed) short/long-term classification via the real IRC §1222 365-day rule applied to the simulation's own calendar dates.
- **Scope**: the same three already-approved `repay_fraction` arms (10%/25%/50%), reused exactly, not re-swept. The same three illustrative tax-rate tiers (0%/15%/32%), reused exactly from the prior upper-bound pass.
- **Comparison**: the FIFO-realistic taxable base (net realized gain across all disposals, floored at $0) against the prior upper-bound taxable base (100% of every repaid dollar treated as gain), at each `repay_fraction` × rate-tier cell.

## 2. What was not tested

- **Lot-consumption convention sensitivity.** Only FIFO was implemented — no LIFO or specific-lot comparison, per `PHASE6A_TAX_LOT_MODELING_PLAN.md` §6/§9's explicit scoping decision to avoid drifting toward tax-optimization research.
- **State tax, wash-sale rules, AMT, NIIT, or loss-carryforward benefit.** All explicitly excluded, unchanged from the prior tax pass's own scope limitations.
- **Repayment fraction selection or Model B/C parameter changes.** The three arms are reused exactly; none is ranked, selected, or recommended.
- **This account's real cost basis, real lot history, or real elected tax treatment.** The FIFO ledger is built entirely from the synthetic $0-start simulation's own purchase history — never from real trade data, which this project has never had access to (`docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`).
- **Execution/slippage realism and broker mechanics.** Both remain untouched, separate, still-open blockers (see §7).

## 3. Engine change made solely for measurement

Per `docs/PHASE6A_IMPLEMENTATION_APPROVAL.md`'s frozen scope, `margin_simulation.py` gained:

- A `Lot` dataclass and per-ticker lot ledger, populated at the existing single purchase site.
- FIFO consumption logic (`_consume_fifo_lots`) wired into the existing `_fund_repayment()` function via new **optional** parameters (`lots`, `sale_day`, `sale_date`, `tax_lot_events`), defaulting to `None` — omitting them reproduces `_fund_repayment`'s exact pre-Phase-6A behavior.
- A new `SimulationResult.tax_lot_events` field (default empty list) — every other existing field (`book_values`, `gross_series`, `leverage_series`, `events`, `final_margin_debt`) is untouched.

**No existing computation changed.** `shares[s]`, `cash`, `gross`, `leverage_series`, and `book_values` are computed by the exact same arithmetic as before Phase 6A — the lot ledger is read-alongside bookkeeping of quantities the engine already computed and previously discarded, not a new decision input. Proven directly by a dedicated unit test (`test_fund_repayment_shares_and_cash_unchanged_whether_or_not_lots_tracked`) and by the full pre-existing test suite passing unchanged after the addition.

## 4. Regression verification

- **Before any Phase 6A test was written**: the full pre-existing suite (260 tests) was run and passed unchanged, with the lot ledger present but unconsumed — confirming zero behavioral change from the addition alone.
- **After Phase 6A tests were added**: 274/274 tests passed (260 prior + 14 new, covering lot creation, FIFO consumption — single-lot, multi-lot, partial liquidation, oldest-first ordering, loss case, over-sell guard — holding-period classification, the additive-only invariant, the lot-ledger consistency invariant, and a full `simulate()` integration test).
- **After the tax-lot analysis library was added**: 281/281 tests passed (274 prior + 7 new for `phase6a_tax_lot_lib.py`'s aggregation functions).
- **Zero regressions at every stage.**

## 5. Verify-before-comparing gate results

Before any tax computation was applied, all three `repay_fraction` arms were re-run through the Phase-6A-modified engine and asserted, with `<1e-6` tolerance, against the stored `docs/results/PHASE3_SENSITIVITY_RESULTS.json` values:

| repay_fraction | Gross TWR | Gross MaxDD | Event count | Match |
|---:|---:|---:|---:|---|
| 10% | 34.62% | −25.84% | 314 | **Exact** |
| 25% | 33.28% | −24.74% | 296 | **Exact** |
| 50% | 32.03% | −23.65% | 263 | **Exact** |

Control (MODEL_0, no repayment) also matched exactly (35.59% TWR, −26.81% MaxDD) and correctly produced zero `tax_lot_events` (a policy that never repays generates no disposals). **This gate was run twice** — once interactively before the tax-lot analysis script was written, and again as a hard assertion inside `run_phase6a_tax_lot_analysis.py` itself, which halts before computing any tax figure if it fails. Gross portfolio behavior is confirmed unchanged by the lot-tracking addition before any tax modeling was layered on.

## 6. Known / Estimated / Hypothetical separation

| Item | Label |
|---|---|
| `repay_fraction` values (10%/25%/50%), event streams, gross TWR/MaxDD/event counts | **Known** (already-verified simulation output, reused exactly) |
| `margin_simulation.py` had zero lot tracking before Phase 6A (aggregate share counts only) | **Known** (confirmed by direct code read) |
| FIFO lot-consumption convention | **Hypothetical, explicitly disclosed** — the realistic default absent any stated election, not a confirmed fact about this account |
| Short/long-term 365-day rule | **Known** (real IRC §1222 rule) applied to **Hypothetical** dates (the underlying simulated calendar is synthetic) |
| Synthetic $0-start purchase history as the sole lot-data source | **Hypothetical**, matching every prior Phase 3/4A scenario's own starting-condition convention |
| Tax rate tiers (0%/15%/32%) | **Hypothetical**, unchanged illustrative federal brackets, not this account's confirmed rate |
| Federal-only scope, no state tax | **Known scope limitation** — excluded, not assumed zero |
| Account type (standard taxable margin account) | **Estimated**, unchanged structural inference from margin usage |
| Net-realized-gain taxable base, floored at $0 (no loss-carryforward benefit modeled) | **Hypothetical, disclosed simplification** — decided during library implementation, before any result was seen, not tuned after |
| Materiality bands (2.0pp material / 0.5pp noise floor) | **Known**, reused unchanged from `docs/PHASE4A_MATERIALITY_THRESHOLDS.md` |

## 7. Results

Quoted from `docs/PHASE6A_TAX_LOT_ANALYSIS.md`/`.json`, not recomputed:

| repay_fraction | Upper-bound taxable base | FIFO-realistic taxable base | Reduction | Gross gap vs. control | Gap @ 15% (FIFO) | Gap @ 32% (FIFO) | Short-term / long-term gain split |
|---:|---:|---:|---:|---:|---:|---:|---|
| 10% | $38,225.89 | $14,394.88 | 62.3% | −0.98pp (suggestive) | −1.12pp (suggestive) | −1.29pp (suggestive) | 1.4% / 98.6% |
| 25% | $88,516.45 | $38,219.04 | 56.8% | −2.32pp (material) | −2.73pp (material) | −3.20pp (material) | 1.2% / 98.8% |
| 50% | $156,112.51 | $67,142.08 | 57.0% | −3.56pp (material) | −4.31pp (material) | −5.18pp (material) | 1.3% / 98.7% |

**Evidence shows** the FIFO-realistic taxable base is 57–62% smaller than the prior worst-case upper bound at every tested `repay_fraction` — the earlier ceiling was a real, substantial overstatement of the taxable amount, consistent with its own disclosed design as a severe upper bound (100% of every repaid dollar, including cash-funded and return-of-basis dollars, treated as gain).

**Evidence shows** that reduction did not change the materiality classification at 25%/50% — both remain "material" at every tested tax tier despite the much smaller taxable base, because the underlying gross TWR/MaxDD gap at those fractions was already well above the 2.0pp threshold before any tax was applied.

**Evidence shows** the 10% arm's gap was already "suggestive," not material, on a pre-tax basis (−0.98pp gross), and stays "suggestive" (not material) at every FIFO-realistic tax tier — no crossing occurred in either direction at this fraction.

**Evidence shows** realized gains skew heavily long-term (~99% of gain dollars at every fraction) — a direct, mechanism-level consequence of Model B's own high-water-mark trigger (it only ever fires when net equity sets a new all-time high, which structurally favors positions that have been held and appreciating for a long time), not an assumption chosen for this analysis.

**Evidence does not show** that tax friction disappears under realistic accounting — at the two fractions where it was material before, it remains material after.

**Evidence does not show** a specific `repay_fraction` is superior — the reduction and the materiality outcome are reported per-fraction; no ranking or selection is drawn.

## 8. Remaining unknowns

- This account's real cost basis, real acquisition dates, or real lot history — never modeled, never estimated; the FIFO ledger reflects only the synthetic simulation's own internal purchase record.
- This account's real elected lot-consumption convention (FIFO vs. specific-lot) — never confirmed to exist as a real election.
- This account's real marginal tax rate, filing status, or state of residence — the 0%/15%/32% tiers remain illustrative only.
- State tax liability, wash-sale rule interactions, AMT, NIIT, and any loss-carryforward benefit — all explicitly out of scope, not modeled as zero-impact.
- Execution-layer realism (slippage, spread widening under stress) and real broker margin mechanics — both remain separate, untouched blockers named in `docs/PHASE5_DECISION_GATE_REVIEW.md` §5, unaffected by this phase.
- Whether a lot-convention sensitivity check (LIFO/specific-lot) would materially change these figures — not tested, explicitly out of scope per §2 above.

## 9. Explicit prohibitions (restated, unchanged by this record)

- **No `repay_fraction` is selected.** All three arms are reported in full; none is recommended, ranked, or chosen.
- **No recommendation for or against Model B.** This record describes what the evidence shows about a simulated mechanism's tax sensitivity; it does not conclude the mechanism should or should not be used.
- **No doctrine change.** `targets.yaml`'s margin schema remains entirely `null`; `CLAUDE.md`'s Decisions Log is unchanged.
- **No production implementation.** `allocate.py`, `holdings.yaml`, and `margin_state.py` remain untouched and unaffected by this phase in every respect.
- **Phase 3's upper-bound tax result is not invalidated or retracted.** `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` and `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`/`.json` remain on record exactly as written — Phase 6A narrows the estimate, it does not correct an error or supersede the prior document's own conclusions, which were always explicitly framed as an upper bound, not a point estimate.
- **`docs/PHASE5B_GOVERNANCE_DECISION.md`'s "maintain current doctrine" decision is not revisited by this record.** Whether this evidence changes that decision is Prompt 7's scope (`docs/PHASE6A_DECISION_GATE_REVIEW.md`), not this one.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure — every number above is quoted from `docs/PHASE6A_TAX_LOT_ANALYSIS.md`/`.json`.
- Does not modify `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md` or `docs/PHASE5B_GOVERNANCE_DECISION.md` — both remain accurate, dated snapshots of their own moment.
- Does not evaluate whether this evidence should change the Phase 5B governance decision — that is a separate, future step (Prompt 7).
- Does not select, rank, or recommend a `repay_fraction`, lot convention, or tax assumption.
- Does not change any doctrine, production file, or prior document's own conclusions.

Stopping here. This is a consolidation record, not a governance review.
