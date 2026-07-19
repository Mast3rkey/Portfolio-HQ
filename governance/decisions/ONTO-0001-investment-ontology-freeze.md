---
decision_id: ONTO-0001
date: 2026-07-19
status: Accepted
category: analytical_vocabulary
related_decisions: [GOV-0001, PI-0001, PI-0004, PI-0006]
supporting_artifact: null
---

## Context

The economic-systems framework, four capital types, portfolio reasoning
hierarchy, five system examples, and standardized review dimensions
captured in `docs/INVESTMENT_ONTOLOGY.md` originated in prior
investment-committee discussion outside this repository. That discussion
establishes the concepts' origin and directional approval, but no
finalized, verbatim ontology artifact was ever preserved or filed in this
repository.

`governance/decisions/GOV-0001-governance-architecture-adopted.md`
separately references a parallel, broader proposal ("Project B" —
economic-systems reorganization, capital-type taxonomy, company
scorecards) and explicitly excludes it from GOV-0001's own scope. This
decision does not treat Project B, or the underlying committee discussion
generally, as already-adopted policy on the strength of that prior
discussion alone.

ONTO-0001 is the first repository formalization, and the first present,
final approval, of a deliberately bounded reference vocabulary drawn from
that discussion — materially narrower than the excluded Project B scope:
no economic-systems reorganization, no capital-type-driven reallocation,
and no company scorecard database.

## Decision

**ONTO-0001 authorizes only the existence of `docs/INVESTMENT_ONTOLOGY.md`
as a reference artifact.** This is the first repository formalization, and
the first final approval, of concepts previously discussed and
directionally approved by the investment committee — economic systems and
company roles, four capital types, a portfolio reasoning hierarchy, an
initial five-system reference list, and a ten-term company-review
vocabulary — for human research, discussion, and future governance use. It
is not a re-filing of any prior finalized artifact (none exists), and it
does not adopt the broader "Project B" scope GOV-0001 excluded. Nothing
beyond the document's own existence is authorized.

ONTO-0001 explicitly does **not** authorize, and no future implementation
may treat this decision as having authorized:

- classifying the full roster, or any subset of it, against this
  vocabulary;
- creating mandatory company ontology fields in
  `intelligence/companies/*.yaml` or anywhere else;
- creating a company scorecard database;
- any numeric quality, moat, conviction, or capital-priority score;
- any standing ranking of companies against each other;
- any next-dollar or "what to buy next" recommendation;
- promotion or demotion of any company;
- any tier, weight, target, sleeve, cap, cluster, or roster change;
- any edit to `holdings.yaml` or `targets.yaml`;
- any import or read path from `allocate.py`, `margin_state.py`, or any
  other production code;
- any change to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema, including
  its Company or Theme YAML schemas, and no new or replacement field
  (including any connection to `portfolio_role_ref`);
- any new research requirement or standing research/monitoring layer;
- any requirement that every company, or any company, belong to an
  economic system;
- any system-level target, floor, cap, or allocation sleeve keyed to an
  economic system;
- any amendment to `constitution/INVESTMENT_CONSTITUTION.md`;
- any trade or order of any kind.

A future use of this vocabulary in a Company Intelligence record, a Theme
Intelligence record, a committee review, a report, or a policy decision
requires its own separate proposal and its own separate governance
decision — this document does not pre-approve any of them. Terms defined
in `docs/INVESTMENT_ONTOLOGY.md` remain purely descriptive until such a
future decision explicitly grants them a specific use. The absence of
ontology classification on any company or theme record is normal and is
not an error. This decision does not reopen, and must not be cited as
grounds to reopen, any previously closed company, tier, scoring,
allocator, regime, trend, margin, conviction, concentration, or
target-policy question.

## Rationale

Same discipline PI-0001 already applied to Company Intelligence and
PI-0006 applied to Theme Intelligence: freezing a vocabulary or data model
is not authorization to build, classify, or integrate anything against
it — those remain separate, future, separately-justified decisions.
Framing this vocabulary as strictly descriptive (Section F's preserved
distinctions; Section G's "what this is not") is the direct application of
`constitution/INVESTMENT_CONSTITUTION.md` Principle 4 (no predictive
research, no standing scoring layer). Principle 5 remains untouched: this
vocabulary establishes no mechanical limit, computes nothing, gates
nothing, and receives no implementation authority. Bounding the vocabulary
to strictly less than the Project B scope GOV-0001 excluded — no
reorganization, no capital-type-driven reallocation, no scorecard
database — is what allows this decision to be evaluated without reopening
GOV-0001's own exclusion.

This decision's `related_decisions` include `PI-0001`, `PI-0004`, and
`PI-0006` because each states a directly applicable doctrinal precedent
this decision follows rather than originates: PI-0001 established that
freezing a specification is not authorization to implement against it —
the same posture this decision takes toward `docs/INVESTMENT_ONTOLOGY.md`.
PI-0004 froze the conviction vocabulary Section F cross-references without
altering it. PI-0006 froze Theme Intelligence's no-conviction/no-numeric-
score rule, which this document's own refusal to score economic systems or
capital types mirrors. None of these three decisions is reopened, amended,
or extended by ONTO-0001.

## Alternatives Considered

- **Adopt the full Project B scope now** (economic-systems reorganization,
  capital-type-driven reallocation, company scorecard database). Rejected:
  GOV-0001 already excluded this scope at the requester's direction, and
  it runs into the Constitution's Principle 4 no-predictive-research
  guardrail. This decision does not reopen any previously closed company,
  tier, scoring, allocator, regime, trend, margin, conviction,
  concentration, or target-policy question.
- **File this vocabulary directly as a Company/Theme Intelligence schema
  change** (e.g. new fields on `intelligence/companies/*.yaml`, or a field
  connecting to `portfolio_role_ref`). Rejected:
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s own §20/§24 require any schema
  change to be its own separate, future, separately-approved decision;
  bundling it into a vocabulary freeze would violate that boundary, and
  would risk reinterpreting `portfolio_role_ref` rather than leaving it
  untouched.
- **Continue treating the framework as informal, unfiled committee
  discussion.** Rejected now that final approval has been given: the
  underlying concepts are directionally approved and a written, bounded,
  non-authorizing artifact is more auditable than an undocumented informal
  understanding.
- **Add the vocabulary directly to
  `constitution/INVESTMENT_CONSTITUTION.md`** instead of a governance
  decision. Rejected: the Constitution's own §7 amendment process requires
  a decision explicitly categorized as a constitutional amendment, stating
  what principle changes and why the prior version no longer holds — this
  vocabulary changes no existing principle and is better suited to a
  bounded governance decision than a constitutional amendment.

## Consequences

`docs/INVESTMENT_ONTOLOGY.md` exists as a reference artifact; nothing in
the allocator, `targets.yaml`, `holdings.yaml`, `intelligence/`, or
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` changes as a result.
`governance/decisions.yaml` gains one new `Accepted` row for this entry.
CLAUDE.md's Decisions Log gains one short pointer entry, consistent with
the pattern GOV-0001 and PI-0010 already set — the full rationale stays in
this file and is not duplicated there. No company or theme file is
created, modified, or required to reference this vocabulary, and
`portfolio_role_ref` is not reinterpreted or extended. Any future proposal
to actually use this vocabulary — in scoring, classification, reporting,
schema integration, or policy — is out of scope for this decision and
requires its own governance record.
