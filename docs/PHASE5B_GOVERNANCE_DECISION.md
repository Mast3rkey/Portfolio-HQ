# Phase 5B — Governance Decision

> **⚠️ Governance decision record, not a re-run.** This document runs no simulation, computes no new figure, and changes no code. It records an explicit decision about the margin research line's current production status, based entirely on the evidence already inventoried in `docs/PHASE5_DECISION_GATE_REVIEW.md`. `targets.yaml`'s margin schema is not activated by this document; no entry is added to `CLAUDE.md`'s Decisions Log by this document itself — see §5 for what, if anything, that requires next.

_Written 2026-07-17. Direct follow-up to `docs/PHASE5_DECISION_GATE_REVIEW.md`, per explicit instruction to proceed to Phase 5B rather than open further research (Phase 5C). Documentation only — no code, no tests, no production files touched._

---

## 1. Decision question

**Given all evidence collected across Phases 3A–3G, 4A, and the transaction-cost/tax/stress-regime sensitivity passes, what — if anything — changes in production?**

## 2. Evidence recap (no new analysis)

Quoting `docs/PHASE5_DECISION_GATE_REVIEW.md` §1's inventory, condensed:

| Question | Answer |
|---|---|
| Return effect? | Yes, observed — monotonic across `repay_fraction` |
| Transaction-cost effect? | Small — erosion 3 orders of magnitude below the observed gap |
| Tax effect? | Potentially large — worst-case upper bound roughly doubles the gap at high intensity |
| Stress behavior? | Not a stress hedge — mechanism structurally quiet during detected stress (5.9–6.9% of repayment dollars vs. 12.2% base rate) |
| Concentration interaction? | Inconclusive under the pre-committed gate — one comparison cleared materiality (−5.14pp MaxDD) but the event-count leg did not; gate coverage gap identified and corrected for *future* cycles only |

And the blockers from `PHASE5_DECISION_GATE_REVIEW.md` §5, unresolved: real tax-lot accounting, real execution/slippage modeling, real broker margin behavior under extreme events, human override/execution workflow design, and single-window sample-size limits (2021–2026, one real bear stretch).

## 3. Evaluation of the three named options

### Decision 1 — Maintain current doctrine

**What it requires:** nothing. Margin stays research-only, `targets.yaml` unchanged, margin schema inactive, no repayment logic in production.

**Fit with the evidence:** exact match. Every research document in this line — without exception — closed with an explicit "no doctrine recommendation" / "no production implications" statement. The evidence answers *whether the mechanism behaves differently* under several conditions; it does not resolve any of the five blockers that would be needed before the mechanism's output could be trusted as an input to a real decision, even an advisory one. Choosing this option carries zero implementation risk and zero governance risk — it is the null decision, not an avoidance of one.

### Decision 2 — Advisory-only expansion

**What it requires:** a change to `allocate.py`'s output (or a new adjacent report) to surface hypothetical repayment-scenario figures inside the normal workflow. A production-file change, even though it places no orders.

**Fit with the evidence:** **not supported yet.** Two of the five blockers directly undercut this option specifically: real tax-lot accounting and real execution/slippage modeling. Surfacing a "Model B would suggest repaying $X" figure inside the actual weekly workflow, without those blockers resolved, risks presenting a severe-upper-bound-assumption hypothetical (§3 of the tax-sensitivity results: 100% of every event treated as realized gain) as if it were an actionable number — precisely the category error the stress-regime phase's own synthesis was written to prevent from recurring in a different form. This is not a rejection of the idea; it is a statement that the current evidence stack is the wrong gate for it.

### Decision 3 — Authorize future pilot design

**What it requires:** scoping-only work — pilot requirements, additional safeguards, an approval process. No live behavior, no code.

**Fit with the evidence:** **premature relative to Decision 1, but not disqualified.** Since this option produces no runtime effect, it carries the same zero-risk profile as Decision 1 on the production side. But scoping a pilot before knowing whether Decision 2's blockers are even resolvable (e.g., whether real tax-lot data can be sourced at all) risks designing around requirements that may not survive contact with those unresolved questions. Better sequenced *after* a specific blocker-resolution effort, not before one.

## 4. Decision

**Decision 1 — Maintain current doctrine.**

Margin repayment logic (Model B, Model C) remains research-only. `targets.yaml`'s margin schema remains `null`. No repayment rule, threshold, or parameter enters `allocate.py` or any production file. The workflow described in `CLAUDE.md` (deposit → allocate.py → present table → manual execution → sync) is unchanged.

**This is a valid, evidence-grounded decision, not a failure of the research program.** The research line successfully answered every question it set out to answer — a mechanism was tested, its behavior under multiple friction categories was measured, and its operating profile was characterized precisely enough to name a category error before it could be made. What it did not do, and was never asked to do, is resolve implementation-layer questions (tax lots, execution modeling, broker mechanics, human workflow) that sit outside a return/risk simulation's reach. Decision 1 correctly separates "the mechanism has been characterized" from "the mechanism is ready to inform a real decision."

## 5. What this decision does and does not do

**Does:**
- Formally closes the "does the current evidence stack justify a production change" question — no, not yet, and the reason is specific (§3's blocker analysis), not a vague "more research needed."
- Leaves every research artifact (Phase 3/4A/transaction-cost/tax/stress-regime) exactly as recorded — nothing is retroactively reinterpreted.
- Leaves Decisions 2 and 3 explicitly named and available for later reconsideration, each conditioned on specific, named prerequisites (§3), not closed off permanently.

**Does not:**
- Add any entry to `CLAUDE.md`'s Decisions Log. That log records *production* doctrine changes; this document changes nothing about production, so nothing is added. If a future decision (e.g., a later Decision 2 or 3 adoption) does change production behavior, that adoption — not this one — would be the entry.
- Authorize Phase 5C research. Per the explicit instruction accompanying this request, only one of Phase 5B or 5C opens at a time; this document is the 5B path, and closing it does not automatically open 5C.
- Rank or prioritize which blocker (tax lots, execution modeling, broker mechanics, workflow design) should be addressed first, if any future research or design effort is authorized. That remains a separate, future decision.

---

## What this document deliberately does not do

- Does not run any simulation or recompute any figure.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or `CLAUDE.md`.
- Does not change any prior research document's recorded conclusion.
- Does not open Phase 5C or any new research plan.
- Does not authorize Decision 2 or Decision 3 — both remain named, evaluated, and available for a future, separately-approved reconsideration if their respective prerequisites change.

Stopping here. The margin research line's governance question is closed: current doctrine is maintained. Awaiting direction on whether any blocker-resolution work (tax lots, execution modeling, broker mechanics, workflow design) should be scoped next, or whether this closes the margin research program for now.
