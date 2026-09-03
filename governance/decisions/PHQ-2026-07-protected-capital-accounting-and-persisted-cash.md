---
decision_id: PHQ-2026-07
date: 2026-08-31
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04, PHQ-2026-05, PHQ-2026-06]
supporting_artifact: test_protected_capital_accounting.py
---

## Context

`PHQ-2026-02` recorded the then-current cash representation: `holdings.yaml`
carried no `cash` field, and a verified cash figure was supplied to the
allocator through its existing runtime `allocate.py --cash` input.
`PHQ-2026-05`, `PHQ-2026-06`, and `OPS-0014` §38 each restate that same fact.

That representation has a demonstrated defect. Because cash was a per-run
argument and was never persisted, a run that omitted it computed
`book = invested − margin debt` and understated the book by the entire cash
balance — and therefore understated every `target_pct` dollar figure derived
from it. Separately, the `CASH` (1.00%) and `RESERVE` (4.00%) destination rows
were treated as definitionally satisfied and were never checked against any
observed balance, so "satisfied" was an assumption rather than a proved fact.

An independent FULL review of PR #364 (review `5069633229`, at head
`bb6701b9d3614f3cc4b53aadf220f6d599cba7cd`) correctly found that correcting
this is a Class-4 change under `OPS-0014` §32 — it alters an allocator rule and
the cash representation itself — and that no accepted decision supplied that
authority. This decision is that authority, granted explicitly by the principal
following that review.

## Decision

The principal authorizes the following, and nothing beyond it.

**1. Cash source of truth.** `holdings.yaml` carries a persisted canonical cash
observation, `cash: {balance, synced_at}`, where `balance` is the **total**
account cash balance and never a deposit delta. This **prospectively
supersedes** the runtime-only cash representation recorded in `PHQ-2026-02`,
`PHQ-2026-05`, `PHQ-2026-06`, and `OPS-0014` §38. Those decisions remain
accurate records of the state at their own dates and are **not edited**.

**2. Book identity.**

    book = resolved invested holdings + tracked cash − margin debt

Tracked cash enters that identity **exactly once**.

**3. Protected floor.**

    protected_floor = book × (CASH target % + RESERVE target % + unreconciled %)
                    + Σ over gated names of max(0, gated target$ − held$)

Every percentage is derived at runtime from the current `targets.yaml` and
`gates.yaml` configuration. **No policy percentage is duplicated as a literal
in code or in this decision.** The floor bounds cash-funded buys and nothing
else: it changes no target, no gate, no cap, and no cluster.

**4. State semantics.** `known-current`, `known-stale`, and `unknown/invalid`
are three distinct states. Zero is never substituted for stale or unknown. A
derived fallback is never labelled "actual". When required current state is
unusable, current dollar recommendations — and every dollar figure derived from
the unknown quantity, including book, protected floor, target dollars, and
shortfalls — are **unavailable**, not estimated. A known-stale observation may
be displayed, but only as stale historical evidence carrying its own date.

**5. Freshness.** Cash and margin both use the pre-existing
`STALE_MARGIN_DAYS = 2` threshold. Failure of either freshness or validity gate
makes current dollar recommendations non-actionable.

**6. Margin.** Margin-funded buys **fail closed**. No broker cash-preservation
mechanic is modelled, because none is evidenced anywhere in this repository.
Unused margin capacity is never cash and may never disguise a shortfall. This
decision grants **no** new margin-deployment policy; the 1.8x leverage cap and
30% buffer floor are untouched.

**7. CLI.** `--cash` is **retired**. Persisted `holdings.yaml` cash is the sole
operative cash source of truth. Every active, non-historical caller,
`README.md` instruction, dashboard instruction, and test migrates. Immutable
historical evidence that merely mentions `--cash` is **not** rewritten.

**8. Performance logging.** `performance_log.csv` may gain `cash` and `book`
columns. A row may never record stale or unknown cash or margin as current.
Existing `net_equity` semantics are unchanged, and rows written before this
change carry honestly-blank new columns rather than back-filled values.

**9. Valuation completeness.** If any tracked nonzero position required for
book accounting is unpriced or unresolved, current dollar output is **blocked**
rather than silently omitting that position from the book.

**10. Nothing else.** This decision authorizes **no** change to holdings
membership, targets, tiers, any percentage (the `CASH` and `RESERVE`
percentages included), gates, issuer limits, cluster caps, the leverage cap,
the buffer floor, Stage-1 authority, orders, or trades.

## Rationale

The defect is a correctness defect in observational accounting, not a change of
investment policy — but the *representation*, *actionability*, *funding*, and
*interface* rules it necessarily touches are themselves policy choices, which
is exactly why `OPS-0014` §32 classifies it Class 4 and why it required this
explicit authorization rather than an author's judgment that it merely
"honors" existing policy. That earlier judgment, recorded in PR #364's original
description, was wrong and is superseded by this decision.

Item 4 is the strictest clause and deliberately so. The rejected alternative —
substituting zero for an unusable observation and labelling the result
"actual" — publishes a knowingly false figure, which is a worse failure than
declining to answer. Declining to answer is the correct behavior for an
advisory system whose inputs are stale.

## Alternatives considered

**Keep `--cash` as a compatibility alias.** Rejected: two cash sources of truth
reintroduce exactly the double-count ambiguity item 1 exists to remove, and a
run's authoritative balance would then depend on invocation form.

**Narrow the change to reporting only, leaving funding untouched.** Rejected:
the funding path is where the defect actually causes harm — an understated book
understates every target dollar, and an unchecked floor lets cash-funded buys
spend protected capital.

**Hardcode 12.50% as the protected weight.** Rejected under `NUM-0001`: it
duplicates governed policy percentages into code, where they would silently
drift from `targets.yaml`.

## Consequences

This decision supplies both the accepted decision and the bounded implementation
authority `OPS-0014` §32 requires. Implementation lands in PR #364 under the
`OPS-0009` Lane G lifecycle: independent FULL review at the exact corrected
head, principal exact-head acceptance, green exact-head CI, then merge. No
Stage-1 surface, lane, attestation, or `ATTEMPT_1` state is touched, and no
order or trade is placed by any code path.
