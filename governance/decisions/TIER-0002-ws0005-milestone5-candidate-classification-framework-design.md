---
decision_id: TIER-0002
date: 2026-08-05
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0003, PI-0004, PI-0015, PI-0016, PI-0019, PI-0020, TIER-0001, REL-0001, TGT-0001, TGT-0002]
supporting_artifact: governance/audits/WS0005_M5_CANDIDATE_CLASSIFICATION_FRAMEWORK_DESIGN_20260805.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded WS-0005 Milestone 5
candidate-classification-framework-design PR, structural only. The authorization is
explicitly limited to the four axes `TIER-0001` retained for further consideration —
economic role, capital priority, risk concentration, and uncertainty/evidence quality —
and states the framework must be "the smallest structure that materially improves
portfolio decisions." No ticker may be classified; no applied example may assign a real
holding to a category; no change to `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, caps, clusters, allocator logic, `levels.py`, `margin_state.py`,
`allocate.py`, charts, ladder files, or trades is authorized; no mechanical score or
weighted ranking; no adoption decision; Milestones 6-9 remain unauthorized.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`96020e55b5317aa6191733e22d2df84bea4a6574`, working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no active mutation lane.
`TIER-0002` confirmed unused: zero matches in `governance/decisions.yaml`, zero matches via
full-repository grep, and `TIER-0001` is the only existing `TIER-####` entry.

`TIER-0001` (PR #245) independently re-confirmed via the GitHub API, not taken on faith from
the task's own summary: `merged: true`, merge commit `96020e55b5317aa6191733e22d2df84bea4a6574`
(matching `origin/main`'s current tip exactly), independent exact-head review `4859945925`
(CHANGES REQUIRED — 2 MAJOR, 1 MINOR, 1 NOTE), correction commit `eed05c07`, independent
delta review `4860022747` ("DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"),
retained principal-acceptance comment (`issuecomment-5186141437`, exact head
`eed05c07c2604a18466f345a1bb9c8877705f5a2`), and retained post-merge-verification comment
(`issuecomment-5186176928`). `TIER-0001`'s own decision-file and `governance/decisions.yaml`
frontmatter still read `status: Proposed` — a known, pre-existing, out-of-scope state
matching the `CHART-0001`/`CHART-0002`/`REL-0002`-`REL-0005` two-step acceptance-recording
pattern already documented in CLAUDE.md's Decisions Log; not corrected here. The
`tier0001-classification-question-inventory-bounded-unit` gate in
`operations/WORKSTREAMS.yaml`, as merged, reads `status: in_progress`, `pr: null` — accurate
as filed but stale now that the PR has since merged, been reviewed, and been accepted; its
own post-merge-verification comment defers this synchronization to "a future WS-0005
session's own preflight/governance filing." This filing performs that synchronization (see
Consequences and the supporting artifact §7) as an `OPS-0009` Lane M unit folded into this
governance filing, per `OPS-0008` §4(a)'s read-only-by-default convention — matching the
`REL-0002`→`REL-0003`→`REL-0004`→`REL-0005`→`REL-0006` chain's own established pattern. The
pre-existing gate entry's own text is left unedited; a new, separate
`tier0001-post-merge-verification` gate records the confirmation.

`governance/decisions/` carries 72 decision files (excluding `README.md`) against 72
`governance/decisions.yaml` rows — confirmed 1:1 by direct count this session.
WS-0005's own register entry confirms Milestones 1-4 `status: complete`; Milestone 5 remains
`status: proposed`; Milestones 6-9 remain `status: proposed`. No existing accepted decision
anywhere in `governance/decisions.yaml` proposes a candidate Milestone-5 classification
framework or a `TIER-0002` filing — confirmed by full-repository grep.

## Decision

This filing does three things, in one bounded PR:

1. **Reconfirms (Lane M) that `TIER-0001` is fully merged, reviewed, corrected, delta-
   approved, principal-accepted, and post-merge verified**, and synchronizes
   `operations/WORKSTREAMS.yaml` accordingly via one additive gate entry — no edit to
   `TIER-0001`'s own historical gate text.
2. **Designs, as text only — not an authorization, not an adoption, not applied to any
   ticker — a candidate classification framework** covering exactly the four axes
   `TIER-0001` retained: `economic_role`, `capital_priority`, `risk_concentration`, and
   `evidence_quality`. The full field-by-field design, including allowed values, evidence
   sources, fact-versus-judgment labeling, and the design-standard test applied to every
   field, is retained at
   `governance/audits/WS0005_M5_CANDIDATE_CLASSIFICATION_FRAMEWORK_DESIGN_20260805.md`.
   In summary: a new, optional, non-coupled record namespace,
   `intelligence/classification/<TICKER>.yaml` (not created by this filing), reusing
   `docs/INVESTMENT_ONTOLOGY.md`'s already-frozen, currently-unapplied vocabulary for
   economic role; a bounded, non-numeric, `PI-0016`-comparator-shaped capital-priority
   assessment that never becomes a `target_pct` input by formula; a purely computed
   cross-reference rollup of existing cluster-cap, issuer-lookthrough, and relationship-
   record coverage for risk concentration, adding no new ceiling; and an evidence-quality
   axis that reuses the already-differentiated `risks[].severity` vocabulary and adds one
   new, narrow, required uncertainty statement per ticker, while explicitly declining to
   reuse the two fields `TIER-0001` found decorative (`monitoring_enabled`,
   `risks[].status`).
3. **Records one rejected alternative** — extending the frozen Company Intelligence YAML
   schema (§9) directly with a fifth `classification:` block — and the reasons it loses to
   the recommended new-namespace design.

This decision explicitly does **not**: classify any ticker; create
`intelligence/classification/` or any file inside it; modify
`docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, or any existing
Company, Theme, or relationship record; modify `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, or `margin_state.py`;
compute a mechanical score of any kind; or authorize Milestone 6 (blind classification),
Milestone 7 (baseline reconciliation), Milestone 8 (policy recommendation package), or
Milestone 9 (independent review and adoption). Existing tiers, targets, roles, caps, gates,
and position sizes remain the current operating policy in full force, unchanged and
unaffected by this filing, per `OPS-0006` §2's zero-based-research-discipline protocol.

## Rationale

**Why a new namespace rather than extending Company Intelligence's schema.** See the
supporting artifact §3.2 in full. In summary: extending the frozen §9 schema requires its
own separate governance decision, creates backfill pressure across 47 already-governed
records before Milestones 6-9 have even considered adoption, and mismatches
`risk_concentration`'s inherently portfolio-level (not single-company-level) cross-reference
content — the same reasoning `REL-0001` already applied to justify a new
`intelligence/relationships/` namespace over extending Company Intelligence for pairwise
data. A separate, deletable namespace preserves `OPS-0006` §2's zero-based reversibility at
maximum strength: the entire candidate framework can be discarded without touching a single
existing authoritative file.

**Why exactly these four axes, no more, no fewer.** `TIER-0001`'s own inventory (independently
re-verified this session, not merely cited) already narrowed nine candidate axes to four by
evidence: `monitoring_enabled` and `risks[].status` are 100% uniform across the full corpus
(decorative); `implementation readiness` is process metadata, not an economic ticker
attribute; `research conviction` and `dependency/relationship exposure` are already
adequately separated by existing mechanisms (`PI-0004`, `REL-0001`) with no representation
gap to close. The principal's own authorization independently confirmed this exact four-axis
scope rather than reopening the other five. This filing does not re-derive that narrowing —
it designs within it.

**Why `capital_priority` never becomes a `target_pct` formula input.** `docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §19/§20 already establishes that any tier or weight change
remains a manual `targets.yaml` edit, and `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §19 point 2
already names "suggested target, human-applied" as the loosest-coupled advisory integration
tier available. `GOV-0003` already establishes the discipline this design follows for the
conviction-to-priority question specifically: research into a conditional rule connecting two
judgment fields is one thing, adopting an automatic one is a separate, later, evidence-gated
decision — not something a structural design filing may pre-empt.

**Why `risk_concentration` is a pure cross-reference rollup, never a new cap.** `TIER-0001`
§4.4 (independently re-verified this session against live `targets.yaml`/
`intelligence/relationships/*.yaml` state) found 13 of 27 canonical names covered by neither
a cluster cap nor a relationship record — a real, evidenced, currently-invisible-without-
manual-cross-referencing gap. This axis makes that gap a standing, always-current, per-ticker
fact by computing it from three already-authoritative files, never asserting a concentration
judgment independently of them. `REL-0001` §G/§L's existing discipline (structural evidence
and measured correlation stay separate; no correlation study is pre-authorized by naming a
gap) is restated, not narrowed.

**Why `evidence_quality` reuses `risks[].severity` and rejects `risks[].status`/
`monitoring_enabled`.** `TIER-0001` §4.9 found `severity` "already meaningfully
differentiated... materially informs risk interpretation" (164 moderate / 83 low / 6 high
across 253 entries), while `status` is 100% one value across the same 253 entries. Reusing a
field that already varies and declining to re-surface one that doesn't is a direct
application of the design standard, not a new judgment.

## Alternatives Considered

- **Extend the Company Intelligence YAML schema (§9) directly with a `classification:`
  block.** Rejected — see Rationale and the supporting artifact §3.2. The one alternative
  materially useful enough to record, per the authorizing instruction's preference for "one
  recommended framework plus, only if materially useful, one rejected alternative."
- **Retain all nine of `TIER-0001`'s original candidate axes rather than the four it
  recommended.** Not seriously considered — the principal's own authorization already scoped
  this filing to exactly the four `TIER-0001` retained; reopening the other five would exceed
  this unit's bounded authorization, not merely design a framework within it.
- **Design a numeric or weighted scoring model across the four axes to produce a single
  composite classification.** Rejected outright — explicitly prohibited by the authorizing
  instruction ("no mechanical score or weighted ranking") and by `docs/
  PORTFOLIO_INTELLIGENCE_SPEC.md` §12's own standing rule that conviction "is not a formula,
  not a derived score, not something a script computes." No field in the recommended design
  is numeric or orderable by weight.
- **Include an illustrative worked example using a real ticker (e.g. NVDA or GEV) to
  demonstrate the schema.** Rejected — explicitly prohibited by the authorizing instruction
  ("no applied examples that assign real holdings to categories"). The supporting artifact's
  field tables use only abstract sub-field names and value vocabularies, never a real ticker.

## Consequences

**Changes as a direct result of this decision:** the existence of a retained, structural
candidate-classification-framework design (four axes, field definitions, allowed values,
fact-versus-judgment labeling, non-duplication check, and a per-field design-standard test)
for a future, separately authorized Milestone 6 unit to draw on; one rejected alternative
recorded for the same future reference; confirmation, via one additive
`operations/WORKSTREAMS.yaml` gate entry, that `TIER-0001` is fully merged, reviewed,
corrected, accepted, and post-merge verified.

**Does not change:** any tier, target, cap, cluster, gate, or holding; any allocator or
margin behavior; any Company, Theme, or relationship record's content;
`docs/INVESTMENT_ONTOLOGY.md`'s or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s frozen text;
`TIER-0001`'s own historical gate entry or decision-file text; WS-0005's top-level `status`
(remains `in_progress`, since Milestones 6-9 remain unauthorized); the
`milestone-5-zero-based-classification-and-tier-architecture-review` gate's own
`status: proposed` (this filing's first-step nature does not itself complete or advance the
milestone as a whole, matching `TIER-0001`'s own identical convention); or any brokerage,
trading, or order-related capability. Completing this unit does not itself authorize
Milestone 6 (blind classification), Milestone 7 (baseline reconciliation), Milestone 8
(policy recommendation package), Milestone 9 (independent review and adoption), or the
creation of `intelligence/classification/` or any file inside it — each requires its own
separate, explicit, future principal authorization, per `OPS-0006` §16.4's standing rule
that the register never originates authority and no completion claim may be inferred beyond
what was actually authorized and delivered.
