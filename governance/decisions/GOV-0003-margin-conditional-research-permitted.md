---
decision_id: GOV-0003
date: 2026-07-21
status: Accepted
category: constitutional_amendment
related_decisions: [GOV-0001, GOV-0002]
supporting_artifact: null
---

## Context

Constitution §3 stated, as one fused claim, two propositions of different
kinds: (a) margin is not itself a source of edge — a mathematical identity
— and (b) there is no "right time" to borrow more or less, ever, because
"the premise is false." `docs/MARGIN_DOCTRINE.md` (incorporated into the
Constitution in full, per `GOV-0002` level 1) restated (b) in absolute
terms ("This line is absolute... no version of this system, present or
future"), and `CLAUDE.md`'s Portfolio Doctrine section restated it a third
time at the operational layer. Constitution §4 ("No predictive research")
separately forbade any standing research or scoring layer that runs ahead
of a deposit — a principle written for buy-side thesis generation, never
previously examined against a margin-specific research question.

The principal has clarified the system's actual intended objective:
discretionary or predictive market-timing of margin should remain
permanently excluded, but whether a rules-based, evidence-gated,
pre-registered conditional rule can outperform the current fixed posture,
net of cost and risk, is an open empirical question worth researching
under this system's existing evidentiary discipline.

**Level-1 atomicity.** Because `docs/MARGIN_DOCTRINE.md` and the
Constitution are both level-1 authority under `GOV-0002`, this decision
amends both simultaneously in one atomic implementation, plus the one
operational-layer document (`CLAUDE.md`) that independently restated the
same absolute claim. This decision authorizes research *permission* only —
it does not itself authorize a research charter, code, allocator behavior,
or live recommendations. Any later Margin Deployment Research, Margin
Repayment Research, Capital Efficiency Research, or Integrated Margin
Policy work requires its own separate governance decision.

**Illustrative evidence motivating the §4 question, not itself adopting
anything:** principal-supplied, dated (2026-07-21) Robinhood account
screens show a near-universal 25% maintenance ratio across the book, with
SKHY as the observed exception. The bounded, correct characterization of
that observation, carried forward exactly with no further inference, is:
*"SKHY is currently observed as a high-maintenance, low-collateral-
efficiency position that may materially reduce available margin cushion
relative to otherwise similar 25%-maintenance holdings."* Its exact effect
on buying power, initial margin, purchase eligibility, or liquidation
behavior cannot be inferred from that maintenance screenshot alone, and
the ratio itself is a dated observation, not a permanent property of the
security. This evidence motivates why "which approved assets may receive
margin-funded capital" is a real, distinct question worth researching — it
does not itself answer that question, and this decision authorizes no
asset-eligibility rule.

**PR #117.** A companion PR (#117) recorded, separately and prior to this
clarification, the closure of the Phase 3–7A margin research program
(`MARGIN-0004`, proposed) — a program whose own scope explicitly excluded
conditional/timing-based deployment as a stated boundary, not an
oversight. PR #117 was closed unmerged (branch preserved) upon this
decision's approval, precisely because it touched `docs/
MARGIN_DOCTRINE.md` under the prior, superseded principle framing. Its
underlying research findings (the static leverage-level sweep, the
repayment-model evidence, the friction sensitivity results) remain valid,
reusable evidence, unaffected by this decision. A future, separate, revised
`MARGIN-0004` workstream will reconcile that closure against this amended
doctrine.

## Decision

Amends Constitution §3 and §4, and brings `docs/MARGIN_DOCTRINE.md` and
`CLAUDE.md` into conformance, in one atomic implementation.

**§3 is narrowed, not removed.** Preserved without change: margin is not
itself alpha (a mathematical identity); margin amplifies existing returns
and losses symmetrically; the 1.8x leverage cap and 30% buffer floor are
unchanged; every future conditional rule, if ever adopted, operates
strictly inside those limits; no dynamic rule may raise the cap or lower
the floor; a favorable buffer or maintenance reading is never automatic
permission to borrow. Narrowed: discretionary or predictive margin timing
remains permanently prohibited, but whether a rules-based, pre-registered,
evidence-gated conditional rule outperforms a fixed posture is now an open
empirical question — researchable only under its own separately governed
research charter, adoptable only through its own separate governance
decision. Operator discretion is stated as asymmetric: the operator may
always decline a recommendation, use less margin than recommended or
allowed, or repay more or sooner than required; the operator may never
increase leverage beyond a governed recommendation or limit, and may never
bypass a repayment rule, cap, floor, or other hard safeguard.

**§4 gains one narrow carve-out.** A bounded, retrospective, pre-registered
backtest into conditional margin deployment or repayment is not, by
itself, the standing predictive layer §4 excludes — provided it produces
no live signal, opportunity map, price target, opaque score, continuous
"borrow now" indicator, or precomputed asset recommendation, and
authorizes no automation or production behavior on its own. Any
operational rule such research might suggest requires its own separate
governance decision. Recommendation-only, manual execution is unaffected
throughout and after any such research.

**This decision authorizes exactly:** the constitutional narrowing above,
and the conforming edits to `docs/MARGIN_DOCTRINE.md` and `CLAUDE.md`
described in the synchronized-edits section of the implementing PR.

**This decision does not authorize:** a research charter of any kind; any
code; any allocator behavior change; any live recommendation; any change
to the 1.8x cap or 30% buffer floor; resolution of the future
deployment/repayment architecture; or any second company/theme/margin
implementation. Each remains its own future, separate governance decision.

## Rationale

Constitution §7 requires stating what principle changes and why the prior
version no longer holds. What changes: the claim that testing conditional
margin deployment is *itself* an invalid question is replaced with a claim
that it is an *open, gated* question. What does not change: the "not
alpha" identity, the permanent exclusion of *discretionary* timing, every
currently fixed cap/floor, and the no-predictive-research principle for
everything outside this one bounded carve-out. The asymmetric-discretion
framing is not a new concession — it restates what this system already
does in practice (an operator has always been free to decline a
recommendation or repay early) and makes explicit that this freedom runs
one direction only, never toward more leverage than governed.

## Alternatives Considered

- **Split into two decisions (Constitution first, doctrine later).**
  Rejected — `GOV-0002` forbids leaving two level-1 sources in conflict
  even temporarily; this had to be atomic.
- **Amend §4 broadly to permit predictive research generally.** Rejected
  — the principal asked for the narrowest carve-out that fits this one
  margin question; broadening §4 beyond that would reopen every
  previously declined "new analysis layer" proposal this system has
  rejected on the same grounds.
- **State human discretion symmetrically ("operator judgment never moves
  margin usage").** Rejected — this was an earlier draft's error; it
  erases the always-legitimate ability to be more conservative than a
  recommendation, which this system has never actually forbidden.
- **Leave PR #117's merge order unaddressed, or merge it first.**
  Rejected — both PRs touch `docs/MARGIN_DOCTRINE.md`; merging PR #117
  first would leave it asserting the superseded principle framing, even
  though its specific text had no line-level overlap with this decision's
  edits. Closing it unmerged, preserving its branch, keeps its evidence
  available without that ambiguity.
- **Fold the SKHY evidence and full asset-eligibility question into
  Constitution text.** Rejected — Constitution text must stay durable and
  concise; illustrative evidence and open research questions belong in
  this ADR's Context, not in the constitutional document itself.

## Consequences

Constitution §3/§4, `docs/MARGIN_DOCTRINE.md`, and `CLAUDE.md` are brought
into mutual conformance in one atomic change. `governance/decisions.yaml`
gains one new index row.

**Explicitly unchanged:** the 1.8x leverage cap, the 30% buffer floor,
`targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`,
`margin_simulation.py`, `alpaca_client.py`, `decision_log.yaml`, every test
file, `docs/MARGIN_INTELLIGENCE_DESIGN.md`, `docs/
RESEARCH_BACKLOG_AND_PRIORITIZATION.md`, every Phase 3–7A artifact,
`intelligence/`, `reports/`, and `docs/MARGIN_DOCTRINE.md`'s "The system's
job, precisely" bullet 1 and "How this doctrine gets tested" closing
section — both remain reserved, exactly as they read today, for the
future, separate, revised `MARGIN-0004` workstream.

**Explicitly not authorized by this decision alone:** a research charter;
any code; any allocator behavior change; any live recommendation; any
resolution of the future margin deployment/repayment architecture.

This decision becomes effective only when the implementing pull request
merges to `main`.
