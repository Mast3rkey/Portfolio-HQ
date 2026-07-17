# Phase 6A: Implementation Approval

> **⚠️ Governance/scope-freeze record, not a result.** No code has been written or modified by this document. This freezes what Phase 6A's implementation is allowed to touch and conclude, before any lot-accounting figure exists to see.

_Written 2026-07-17. Confirms acceptance of `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md`, `docs/PHASE6A_ASSUMPTION_REGISTRY.md`, and `docs/PHASE6A_DATA_REQUIREMENTS.md`, and freezes implementation scope before any code is written — the same "design approved, scope frozen, then and only then implement" gate used before every prior execution phase in this project (`PHASE3_SCENARIO_MANIFEST.md` → 3E; `PHASE4A_ASSUMPTION_RESOLUTION.md` → Phase 4A; `TRANSACTION_COST_SENSITIVITY_PLAN.md`/`TAX_TREATMENT_SENSITIVITY_PLAN.md` → their respective runs; `STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md` → its run)._

---

## 1. Design documents accepted

- `docs/PHASE6A_TAX_LOT_MODELING_PLAN.md` — objective, scope, FIFO rationale, allowed/prohibited conclusions.
- `docs/PHASE6A_ASSUMPTION_REGISTRY.md` — 12-item Known/Estimated/Hypothetical registry.
- `docs/PHASE6A_DATA_REQUIREMENTS.md` — confirms no external data acquisition needed; validation plan (lot-ledger consistency, zero-behavior-change check, hand-checkable FIFO test).

All three are treated as final for this implementation pass. Any deviation discovered mid-implementation (e.g., a data assumption that turns out wrong) is a **stop-and-report** event, not a silent scope adjustment — matching the "verify before proceeding" discipline used throughout this project (e.g., the Model C "zero events" recount in Phase 3G, reported honestly rather than reconciled quietly).

## 2. Allowed changes

**Simulation harness only** (`margin_simulation.py`, plus new test/driver files):

- Add additive per-ticker lot tracking (`ticker`, `shares`, `acquisition_date`/`acquisition_day_idx`, `cost_basis_price`), created at the exact point purchases currently increment the aggregate `shares[ticker]` count.
- Add FIFO lot consumption inside `_fund_repayment()`'s sale path, computing realized proceeds, realized gain, and holding period (short/long-term via the 365-day rule) per lot consumed.
- Preserve every existing output field (`portfolio value`, `debt`, `events`, `returns`) exactly as-is; add new fields (`tax_lot_events`, `realized_gain_metrics` or equivalently named) additively, never replacing or renaming an existing field.
- Preserve every existing scenario configuration and every existing repayment mechanic (`ModelBProfitHarvest`, `ModelCRiskReset`) unchanged — the lot ledger observes what already happens, it does not change when or how much is repaid.
- Add tests for: lot creation, FIFO consumption, holding-period classification, partial-lot liquidation (a sale that only partially consumes a lot), and multi-event repayment behavior (multiple repayments drawing across several lots over time).
- Add a new driver script (following the `run_tax_treatment_sensitivity.py` / `run_stress_regime_sensitivity.py` pattern) that re-verifies existing arms before computing the new FIFO-lot comparison, per §4's validation order.

## 3. Not allowed

**No production files:**
- `allocate.py`
- `targets.yaml`
- `holdings.yaml`
- `margin_state.py`
- `CLAUDE.md`

**No strategy changes:**
- No Model B parameter changes (`repay_fraction` stays exactly {10%, 25%, 50%}, reused not re-swept).
- No new repayment logic or trigger mechanic.
- No leverage cap changes (1.8x remains a read-only reference throughout, per every prior phase's constant convention).
- No allocation-logic changes.

**No retroactive reinterpretation:**
- Phase 3/4/5 conclusions remain unchanged, unedited, and are not recomputed. `docs/PHASE3_MODEL_B_COMPLETE_EVIDENCE_RECORD.md`, `docs/TAX_TREATMENT_SENSITIVITY_RESULTS.md`, `docs/PHASE4A_RESEARCH_REPORT.md`, `docs/PHASE5B_GOVERNANCE_DECISION.md` are read-only reference points for this phase, not editable in light of its findings.
- **This phase answers exactly one question, and no other:** *"How much of the modeled tax friction survives when replacing the worst-case upper-bound assumption with realistic FIFO lot accounting?"* It does not reopen the return-effect question (3E), the transaction-cost question (closed), the stress-timing question (closed), or the concentration question (4A) — none of those are touched by adding lot tracking.
- **Does not reopen the Phase 5B governance decision.** "Maintain current doctrine" stands regardless of Phase 6A's outcome; this phase's result feeds a *future*, separately-approved reconsideration of that decision if warranted — it does not itself constitute or trigger that reconsideration.

## 4. Implementation order (frozen)

1. **Lot ledger** — minimal structure (`ticker`, `shares`, `acquisition_date`, `cost_basis`), created on every simulated purchase (deposit-funded allocation buys), additive to the existing `shares[ticker]` aggregate, never replacing it.
2. **FIFO disposal** — `_fund_repayment()`'s existing `reduce shares / calculate proceeds` sequence gains a parallel `consume FIFO lots / calculate realized proceeds, realized gain, holding period` step. The existing share-reduction and proceeds arithmetic themselves are not altered — the lot consumption is a read-and-record operation layered alongside them, not a replacement of them.
3. **Regression gate before any new test is written**: run the existing suite and confirm **260 passed**, unchanged, with the lot ledger present but not yet exercised by any new assertion. Only after that passes does implementation proceed to Phase 6A-specific tests (lot creation, FIFO consumption, holding-period classification, partial-lot liquidation, multi-event repayment).
4. **Verify-before-comparing gate**: before computing any FIFO-lot tax figure, re-run the existing `repay_fraction` arms and confirm gross TWR/event counts match `docs/results/PHASE3_SENSITIVITY_RESULTS.json` exactly (`<1e-6` tolerance) — the same pattern every prior sensitivity pass in this line has followed.
5. Only after steps 1-4 pass does the new FIFO-lot vs. upper-bound comparison get computed and reported.

## 5. Expected research output (framed, not prejudged)

| Case | Question |
|---|---|
| Upper-bound tax model (already recorded) | What was the maximum possible friction? |
| FIFO lot model (this phase) | What friction remains under realistic accounting? |
| Difference | How much of the earlier result was driven by the conservative 100%-gain assumption specifically? |

Three possible outcomes, **none pre-selected or favored by this approval**:

- **Outcome A — tax impact remains material.** The concern survives realistic accounting; the upper bound wasn't just an artifact of conservatism.
- **Outcome B — tax impact shrinks substantially.** The earlier result was mainly an upper-bound artifact; realistic basis materially narrows the gap.
- **Outcome C — mixed.** Some `repay_fraction`/tax-tier cells remain material, others don't; no single universal conclusion.

All three are equally valid, reportable outcomes. This approval does not treat Outcome B as a "success" or Outcome A as a "failure" — consistent with the three-way outcome framework (Evidence supports / does not support / inconclusive) adopted in Phase 4A and reused throughout every sensitivity pass since.

## 6. Validation requirements before commit (unchanged pattern)

- Full test suite passes, 260 prior + new Phase 6A tests, zero regressions.
- `_assert_no_banned_language()` passes on every new report/JSON output.
- `git diff --stat` against `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, `CLAUDE.md` is empty.
- `git diff --stat` against every prior Phase 3/4/5/transaction-cost/tax-treatment/stress-regime artifact is empty.
- Stage only the new/changed files explicitly named in §2; commit with the established message pattern; push; **stop for review** before any further phase.

---

## What this document deliberately does not do

- Does not write, modify, or run any code.
- Does not pre-select an outcome (§5) or a `repay_fraction`/tax-tier "winner."
- Does not reopen or reinterpret any Phase 3/4/5 conclusion.
- Does not authorize any production-file change under any implementation result.

Stopping here. This is the scope freeze. The next action, if approved, is implementation exactly within this scope — nothing broader, nothing narrower, and no code before this document is confirmed.
