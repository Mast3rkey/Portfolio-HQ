---
decision_id: PI-0014
date: 2026-07-19
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0004, PI-0009, PI-0012, PI-0013]
supporting_artifact: null
---

## Context

`PI-0013` closed the `PI-0012` TSM pilot review gate without selecting,
ranking, or naming a next Company Intelligence candidate, and required any
future candidate-selection proposal to state and justify its own criteria.
A subsequent read-only review reconstructed the full 62-company targeted
universe and the complete committed-artifact attention inventory for every
uncovered name, then applied one consistent bar to identify research
candidates: a committed artifact must contain a specific, bounded factual
question that conversation-only research can investigate without a
company-selection, investment-quality, portfolio-policy, conviction, or
theme-membership judgment.

`PI-0012`'s ten-candidate repository review (NVDA, TSM, ASML, AVGO, AMD,
AMAT, KLAC, LRCX, MRVL, INTC) left its eight non-NVDA/TSM names "deferred,
not rejected" only at the pool level. `PI-0012` itself states its
eleven-question method and TSM-specific evidence standard were approved
"for the bounded, one-company TSM committee-review pilot" only, "not as a
standing operational process for the rest of the roster," granting "no
authority to apply this vocabulary to any company other than TSM."
`PI-0013` reaffirms both remain "TSM-only." Pool co-membership therefore
carries no research priority, and no committed artifact raises an
individual, candidate-specific question about ASML, AVGO, AMD, AMAT, KLAC,
LRCX, or MRVL — they are excluded from this authorization on that basis.

Three names each carry a specific, self-contained, committed open question
that does clear the bar:

- **INTC**: `intelligence/companies/TSM.md` §9 (Portfolio Uniqueness) and
  §10 (Replacement Candidate) each name INTC directly as a current
  Portfolio-HQ holding with some semiconductor-manufacturing/foundry-
  related exposure, and each explicitly leaves the degree of TSM/INTC
  economic-exposure overlap and operational substitutability
  "unresolved." `PI-0013` separately documents that an earlier TSM draft
  was factually wrong about INTC's actual held/spec/semis-cluster status
  before a manual pre-merge correction — a diligence flag specific to
  this ticker.
- **SYK**: `intelligence/themes/life_sciences_tools_medtech.md` defers SYK
  because its disclosed "Ortho Tech" segment reorganization (effective Q1
  2026, with 2023–2025 financials recast) "has not yet been observable
  across multiple reporting periods under the new structure."
- **DHR**: the same theme file records DHR's FY2025 disclosed segment
  picture as mixed — Biotechnology core revenue +7% against Life Sciences
  −4% and Diagnostics −1.5% — and separately, its Review Framework's
  unscheduled-review triggers explicitly list "a subsequent reporting
  period that would newly support reconsidering SYK's or DHR's deferral."
  The file treats DHR's deferral, symmetrically with SYK's, as
  time-sensitive and open to revisiting on later disclosure. This factual
  question — has DHR's mixed picture changed since FY2025 — is separable
  from, and distinct in kind from, the same paragraph's separate,
  already-settled argument that TMO is "a cleaner, more consistently
  positive alternative... to represent the same tools/diagnostics
  sub-industry." Only the former is in scope here; the latter remains
  exactly as already recorded, untouched, and is not reopened by this
  decision.

## Decision

Authorizes **one bounded, conversation-based, read-only evidence-gathering
step**, to begin only after this decision itself receives explicit human
approval and is filed. This ADR document does not itself commence any
research.

**Candidate set, fixed at exactly three names: INTC, SYK, DHR.** No other
ticker may be considered under this authorization, including any other
`PI-0012` pool member (ASML, AVGO, AMD, AMAT, KLAC, LRCX, MRVL).

**Permitted questions — INTC:**
- INTC's currently disclosed manufacturing/foundry business and segment
  structure, from primary sources;
- which disclosed facts bear on the `TSM.md`-documented unresolved
  TSM/INTC exposure-overlap and substitutability question;
- whether the existing, frozen Company Intelligence schema can represent
  those facts without modification;
- primary-source availability and any unresolved evidence limitations.

**Permitted questions — SYK:**
- how many reporting periods now exist under Stryker's reorganized
  ("Ortho Tech") segment structure;
- whether reported segment definitions and comparative figures have
  stabilized sufficiently to support a durable record;
- whether the existing, frozen Company Intelligence schema can represent
  the disclosed structure without modification;
- primary-source availability and any unresolved evidence limitations.

**Permitted questions — DHR:**
- how many subsequent reporting periods are now available after the
  FY2025 evidence the theme file used;
- DHR's currently disclosed segment structure;
- the latest disclosed segment-level revenue/core-revenue direction for
  Biotechnology, Life Sciences, and Diagnostics;
- whether those disclosures confirm or change the previously recorded
  mixed picture;
- whether the existing, frozen Company Intelligence schema could
  represent those facts without modification;
- primary-source availability and any unresolved evidence limitations.

**Explicitly prohibited, all three candidates:** determining or proposing
`portfolio_role_ref`; conviction; valuation; expected returns; capital
priority or next-dollar analysis; any tier, target, weight, cap, or
cluster conclusion; investment-attractiveness characterization; ranking
any candidate against another or naming a winner; adopting `PI-0012`'s
eleven-question methodology for any candidate; creating any Company or
Theme Intelligence file; any schema, validator, test, report, allocator,
target, holding, tier, weight, cap, cluster, margin, or policy change; any
trade or allocation recommendation. An existing theme's committed
non-membership standard may be **read** to identify which disclosed facts
would be relevant to a *future* evaluation — this authorization does not
conclude, and prohibits concluding, that any candidate meets, fails,
qualifies for, belongs to, or should reference any existing theme.

**Additionally, explicitly prohibited for DHR specifically:** comparison,
ranking, or preference versus TMO; resolving, reopening, or revisiting the
theme file's existing TMO-redundancy judgment; any theme-membership
eligibility or reference conclusion for DHR. Research under this
authorization may establish only whether DHR's disclosed segment facts
have changed since FY2025 — nothing about what that would mean for DHR's
standing relative to TMO or the theme.

**Source standard**, this decision's own, bounded standard — modeled on
prior repository practice but not itself an adoption or extension of
`PI-0012`'s TSM-specific evidence standard: primary-source-first (official
filings, issuer investor-relations materials); high-quality secondary
material permitted only for corroboration or context; transparent
disclosure wherever primary access fails; established facts, management
claims, analytical interpretation, and unresolved points kept explicitly
separate, the same separation `COST.md`/`XOM.md`/`TSM.md` already used.

**Findings lifecycle:** this authorization produces no committed research
artifact and changes zero repository files. `supporting_artifact` stays
`null` unless a future, separately authorized repository artifact actually
exists. Any findings remain conversational; a **later, separate**
selection decision must independently re-verify and summarize them before
relying on them for any further step.

**`PI-0012` methodology boundary:** this decision does not adopt
`PI-0012`'s eleven-question method or TSM-specific evidence standard for
INTC, SYK, DHR, or any other company. If a future decision explicitly
adopts that method for any of them, that future decision must incorporate
`PI-0013`'s repository-fact reconciliation gate (verification against
`targets.yaml`, `holdings.yaml`, the current `intelligence/companies/`
inventory, and relevant company-side theme references, before final human
approval of that record's Portfolio Uniqueness gate, Replacement Candidate
gate, final YAML, and final Markdown).

## Rationale

Applying one consistent bar to all candidates — a committed, bounded,
non-judgmental factual question — rather than pool membership or informal
impression, is what `PI-0013` itself requires: tier, weight, shares,
ownership, and cluster membership carry no selection authority, and
neither does undifferentiated pool-deferral status. The seven remaining
`PI-0012` names fail that bar because no committed artifact names any of
them individually with an open question; DHR initially appeared to fail it
too, but a corrected reading of `life_sciences_tools_medtech.md` shows its
mixed-segment-picture question is both specific and explicitly flagged by
the file's own review-trigger language as subject to revisiting via
subsequent reporting — the same structural treatment the file gives SYK.
Separating that factual thread from the file's distinct, already-settled
TMO-redundancy argument lets DHR's research proceed without reopening or
prejudging a judgment this decision has no authority to revisit. Including
all three candidates, rather than any subset, follows from all three
independently clearing the identical bar with no committed basis to
prefer one over another.

## Alternatives Considered

- **Exclude DHR entirely, as an earlier draft of this review proposed.**
  Rejected: that position rested on the claim that no self-contained
  factual question exists for DHR, which the theme file's own text
  contradicts — the mixed-picture evidence and the explicit "reconsidering
  SYK's or DHR's deferral" review trigger together establish a real,
  bounded, time-sensitive factual question distinct from the redundancy
  argument.
- **Include DHR but allow the research to also address whether TMO
  redundancy still holds.** Rejected: that would authorize exactly the
  theme-membership/comparative judgment this decision is scoped to avoid;
  the theme file's TMO-comparison finding stays on the record untouched.
- **Include all seven remaining `PI-0012` names on pool-membership
  grounds.** Rejected: `PI-0012` and `PI-0013` both deny any pool-wide
  methodological or priority effect; no committed artifact distinguishes
  any one of these seven from another.
- **Scope to INTC and SYK only, treating DHR's question as too entangled
  with the redundancy argument to separate.** Rejected on closer reading:
  the mixed-picture facts (specific reported figures, specific segments)
  and the redundancy argument (a comparative preference for TMO) are
  stated as two distinct clauses in the same paragraph and can be
  investigated independently — the restriction list above enforces that
  separation rather than using it as a reason to exclude DHR outright.
- **Defer this entire step (Outcome D).** Rejected: three genuine,
  already-documented, narrow, bounded questions exist now.

## Consequences

No Company or Theme Intelligence file, schema, validator, test, report,
`allocate.py`, `margin_state.py`, `targets.yaml`, or `holdings.yaml` is
created or modified by this decision or by any research it authorizes.
`governance/decisions.yaml` gains one new row for this entry. `CLAUDE.md`'s
Decisions Log gains one short pointer entry. **This decision does not
select, rank, or imply a winner among INTC, SYK, and DHR, and does not
itself constitute or authorize any Company Intelligence pilot** — it
authorizes only the bounded, conversational fact-gathering described
above, to occur after separate human approval and filing, with DHR's scope
further restricted to exclude any revisiting of its existing TMO-
redundancy finding. A future, separate decision is required before any
company record is created, before any theme-membership conclusion is
drawn for DHR, and before any adoption of `PI-0012`'s methodology for any
of the three.
