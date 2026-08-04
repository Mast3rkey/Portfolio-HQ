---
decision_id: REL-0001
date: 2026-08-04
status: Accepted
category: relationship_mapping_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: null
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded Lane G (`OPS-0009` §1) governance
filing: freeze the schema, taxonomy, evidence standard, ownership (source-of-truth) convention, and
structural-versus-price-correlation separation for WS-0005 Milestone 4 ("Portfolio Relationship
Mapping"), and authorize exactly one future, separate, inventory-only implementation unit. This
unit must not perform the inventory itself, create `relationship_validator.py` or any validator,
create any `intelligence/relationships/` record, conduct external relationship research, begin any
other Milestone 4 content work, or implement "Eureka" (`OPS-0016`). Everything in this file is
bounded by that authorization; nothing below expands it.

### Preflight performed this session, independently verified, not assumed

Fresh isolated clone established at a workspace dedicated to this unit; repository identity
confirmed `Mast3rkey/Portfolio-HQ` (`origin` fetch/push URL); authenticated GitHub identity
confirmed `Mast3rkey`. `origin` fetched and pruned; local `main` confirmed identical to `origin/main`
at `8f59041a22631a95d7cbfcd6445499faa89b2a5e`, working tree clean. PR #236 ("Record Eureka identity
and mobile/cloud decision architecture," `OPS-0016`) independently re-confirmed `MERGED`, merge
commit `8f59041a22631a95d7cbfcd6445499faa89b2a5e` (the current `origin/main` tip), with its exact-head
CI (`test` check run) `completed`/`success`. Zero open pull requests exist (`gh pr list --state open`
returns an empty list). No branch overlaps `governance/decisions.yaml`, `operations/WORKSTREAMS.yaml`,
`CLAUDE.md`, this decision file, or any directly affected test — `intelligence/relationships/` does
not exist anywhere in the repository (confirmed absent), and no branch name or diff touches it.

`governance/decisions/` carries 65 decision files (excluding `README.md`) against 65
`governance/decisions.yaml` index rows — confirmed via `portfolio_hq.dashboard.decisions.build_catalog()`:
`catalog.issues == ()`, 65 decisions loaded, zero per-decision issues, 1:1 file/index parity. No
existing accepted decision anywhere in that index freezes a relationship-record schema, taxonomy, or
evidence standard, or authorizes a relationship-content inventory — confirmed by full-repository grep
for `relationship`/`relationships`: every hit is either (a) the repeated boilerplate disclaimer "no
import relationship with `allocate.py`" used across research/validator files, (b) narrative prose
*inside* individual Company Intelligence records (e.g. `MSFT.md`'s OpenAI relationship, `ASML.yaml`'s
Zeiss relationship, `AMD.md`/`MRVL.md` explicitly naming "future, separately-authorized
relationship-mapping work (WS-0005 Milestone 4...)" as still unauthorized), or (c) `thesis_relationship`
— a field belonging to the unrelated `CHART-0001`/`CHART-0002` chart-evidence schema, a different
record type entirely. `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s frozen Company/Theme Intelligence
schema (§9-§14, §25) reserves no `relationship`/`relationships` field. This filing's proposed
`intelligence/relationships/` convention and `REL-####` prefix collide with nothing.

`WS-0005`'s current live state, independently re-derived against `operations/WORKSTREAMS.yaml` and
`PI-0037`: **Milestone 3 is `status: complete`** (the `milestone-3-intelligence-completion` gate,
effective on `PI-0037`'s own merge). **Milestone 4 (`milestone-4-portfolio-relationship-mapping`
gate) is `status: proposed`, "Not authorized to execute,"** unchanged since `OPS-0006`'s original
2026-07-25 roadmap filing. `WS-0005`'s top-level `status` remains `in_progress`; `priority` remains
`primary`, the repository's sole `priority: primary` workstream. The canonical equity roster is
independently reconfirmed at 27 names via `targets.yaml`'s `destination:` list: 21 already carrying
a Company Intelligence record (NVDA, TSM, ASML, AVGO, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY,
ISRG, TMO, V, COST, CEG, ETN, GEV, PWR, GNRC, RTX — the last two per `PI-0036`); 4 actionable-gated
and dispositioned by `PI-0035` (SNPS, ICE, SPGI, WM); 2 non-gated-cluster-adjacent but gated and
dispositioned by `PI-0033` (RKLB, TSLA) — 21 + 4 + 2 = 27, 6 gated/deferred, matching this unit's own
expected facts exactly, no material drift found.

The ten `intelligence/*COMPARISON*.md` artifacts, the two Theme Intelligence themes
(`ai_infrastructure`, `life_sciences_tools_medtech`, four files), and `issuer_lookthrough.yaml`
(repository root, not under `intelligence/`) are all independently confirmed present and unmodified
by this filing.

### Decision-identifier determination — independently derived, not assumed

`governance/decisions/README.md`'s own rule: *"A new prefix is chosen only when a genuinely new
decision domain needs one — not pre-declared in advance."* Two repository precedents already apply
this rule to mint a brand-new, single-purpose prefix rather than reuse an adjacent one:
`LADDER-0001` (buy-ladder backtest — rejected `PHQ-####` as naming a different, out-of-repository
process, and rejected `MARGIN-####` as domain-specific to margin/target-sizing) and `CHART-0001`
(chart evidence — rejected extending `PI-####`'s frozen Company Intelligence schema). Applying the
same test here: `PI-####` is Company/Theme *Intelligence* — a single-company or single-theme
evidence record, one-way authority (company/theme → nothing else), explicitly never a
cross-record graph (`PI-0006`: "the graph is a reporting view, not a stored data model"). Milestone
4's subject is structurally different — a **pairwise, cross-company, portfolio-level** record whose
two endpoints are each already-existing Company Intelligence records, with its own directionality,
evidence, and taxonomy rules that do not fit any existing Company/Theme Intelligence field.
Extending `PI-####` to cover it would silently graft a graph-shaped record type onto a schema
`PI-0006`/`PI-0009`/`PI-0011` repeatedly froze as one-way and non-relational. `OPS-####` is
workstream/operations-coordination and cross-cutting-process machinery (`OPS-0001`, `OPS-0006` through
`OPS-0016`) — this is domain content governance, not operations coordination. No `MARGIN-####`,
`CHART-####`, `LADDER-####`, `AUTO-####`, `NUM-####`, `ONTO-####`, `TGT-####`, `GOV-####`, or
`PHQ-####` domain fits either, each being either fully unrelated (margin, chart evidence, buy-ladder
execution, freshness automation, numeric provenance, ontology vocabulary, target-budget policy,
governance-architecture-itself, or the out-of-repository Portfolio-HQ committee process
respectively).

Confirmed this session that minting a new prefix requires **no schema, catalog, validator, or test
change**: `portfolio_hq/dashboard/decisions.py`'s decision-ID pattern
(`_ID_TOKEN = re.compile(r"^[A-Z][A-Z0-9]*-\d{4}(?:-\d{2})?$")`) is fully generic — it already
accepted `LADDER-0001` and `CHART-0001`/`CHART-0002` with zero code change, and will accept
`REL-0001` identically. `governance/decisions.yaml` is a hand-regenerated index with no prefix
enum. No test file (`test_portfolio_hq_dashboard_decisions.py` or any other) hardcodes a closed
prefix list. This filing therefore proceeds with the next valid, unused decision identifier in a
genuinely new domain — **`REL-0001`** — matching the read-only audit's own recommendation, per the
task's own explicit instruction not to invent a prefix "merely for aesthetics": this is not
aesthetic, it is the same domain-boundary test `LADDER-0001`/`CHART-0001` already established and
passed, independently re-applied here, not merely cited. `category: relationship_mapping_governance`
is likewise new, mirroring `CHART-0001`'s own precedent of minting a matching new category
(`chart_evidence_governance`) alongside a new prefix for a genuinely new domain.

## Decision

**`REL-0001` freezes a schema, a closed twelve-item primitive relationship taxonomy, directionality
rules, an evidence/abstention standard, a closed `decision_served` vocabulary, and the
structural-versus-measured-price-correlation separation for WS-0005 Milestone 4. It authorizes
exactly one future, separate, bounded, inventory-only implementation unit — classification of
already-existing evidence only, against the current 27-name canonical roster, with no new research,
no relationship record, and no validator created by that future unit until its own further,
separate authorization.** This filing itself creates no `intelligence/relationships/` file, no
`relationship_validator.py`, no relationship content, and performs no research. Milestone 4 remains
substantively unauthorized to execute; only this schema/taxonomy/evidence-standard freeze and the
bounded future inventory authorization are effective, and only on this decision's own merge.

### A. Purpose

WS-0005 Milestone 4 will map decision-relevant structural relationships, dependencies, overlap, and
correlated-loss mechanisms across the governed portfolio, to improve: duplicate-exposure detection;
thesis monitoring; stress testing; opportunity-cost and next-dollar comparison; missing-exposure
review; and zero-based portfolio review (Milestone 5). A relationship artifact that cannot name a
specific investment, allocation, risk, monitoring, or sell-review decision it improves must not be
created — see §F's closed `decision_served` vocabulary, which is the enforcement mechanism for this
rule.

### B. Source-of-truth model

A future pairwise relationship-record convention is frozen, not created by this filing:

```
intelligence/relationships/<TICKER-A>_<TICKER-B>.yaml
intelligence/relationships/<TICKER-A>_<TICKER-B>.md
```

- Ticker order is alphabetical and deterministic (`A_B`, never `B_A`, regardless of narrative
  subject/object — narrative direction is carried by the record's own `direction` field per §D, not
  by filename order).
- One pair must not exist in both `A_B` and `B_A` form — the alphabetical-filename rule makes this
  mechanically checkable by a future validator, not merely a style convention.
- The filesystem remains the index, matching this repository's existing Company/Theme Intelligence
  discipline (`PI-0001`/`PI-0006`: "the graph is a reporting view, not a stored data model," "no
  hidden relationship store," "no separate policy ledger") — no graph database, no
  `intelligence/relationships/index.yaml`, no hidden store.
- The graph — any future rendering of relationship records as a network/graph view — is a **derived
  reporting view only**, never the authoritative stored model. Building that view is not authorized
  by this filing.

This filing authorizes the convention only. It creates no `intelligence/relationships/` file.

### C. Primitive relationship taxonomy

Twelve primitive, independently authorable relationship types are frozen:

1. **`supplier_dependency`** — Company A sources a material input, component, or service from
   Company B such that a disruption at B is a disclosed or reasonably inferable risk to A's
   production, cost, or delivery.
2. **`customer_dependency`** — Company A derives a material, named or disclosed-as-concentrated
   share of revenue from Company B as a customer or channel.
3. **`manufacturing_dependency`** — Company A relies on Company B (or a shared third-party fab/
   contract manufacturer named by both) for physical production or assembly of a material product
   line.
4. **`technology_platform_dependency`** — Company A's product, service, or infrastructure is built
   on, licensed from, or materially dependent on a platform, architecture, or IP owned or controlled
   by Company B.
5. **`capital_spending_dependency`** — Company A's revenue or order book is materially dependent on
   Company B's (or a named class of companies' resembling B's) capital-expenditure cycle.
6. **`regulatory_or_reimbursement_dependency`** — Companies A and B share material exposure to the
   same specific regulatory regime, approval pathway, reimbursement mechanism, or policy change.
7. **`commodity_or_energy_dependency`** — Companies A and B share material exposure to the price or
   availability of the same specific commodity or energy input.
8. **`financing_or_interest_rate_dependency`** — Companies A and B share a material, named
   dependency on financing structure, credit access, or interest-rate sensitivity beyond generic
   market-wide rate exposure.
9. **`geographic_or_geopolitical_dependency`** — Companies A and B share material exposure to the
   same specific country, region, or geopolitical event class (export controls, tariffs, conflict,
   sanctions).
10. **`competitor`** — Companies A and B compete for the same customer demand in a materially
    overlapping product or service category.
11. **`substitute`** — A customer could reasonably reallocate demand from Company A's offering to
    Company B's offering (or vice versa) as a substitute, even without direct branded competition.
12. **`complement`** — Company A's product or service materially increases the value, demand, or
    viability of Company B's, or vice versa.

**Explicitly excluded as primitive authored record types**: `duplicate_economic_exposure`,
`correlated_loss_mechanism`, and `missing_exposure`. These are **derived conclusions** synthesized
from one or more primitive records (typically several, viewed together with structural evidence per
§G) — they must never be independently asserted as if directly observed. A future record may
*reference* primitive relationship records in support of such a conclusion in narrative prose or in
a future, separately authorized derived-view artifact, but no `intelligence/relationships/*.yaml`
record may declare one of these three as its own `relationship_type`.

### D. Directionality

- `supplier_dependency`, `customer_dependency`, `manufacturing_dependency`,
  `technology_platform_dependency`, and `capital_spending_dependency` are **directional** — each
  record names a `subject`, an `object`, and a `direction` (which ticker depends on which).
- `competitor` and `complement` are **normally symmetric** — recorded once per pair, with both
  tickers as co-equal subjects, not duplicated by reversing the filename or asserting the pair
  twice.
- `substitute` and any future portfolio-role-substitution conclusion **may be directional** (A is a
  substitute for B's specific use case without the reverse holding) — the record must state whether
  it is symmetric or directional for that specific pair; it is never assumed symmetric by default.
- `regulatory_or_reimbursement_dependency`, `commodity_or_energy_dependency`,
  `financing_or_interest_rate_dependency`, and `geographic_or_geopolitical_dependency` are shared
  co-exposures, not dependencies of one company on the other — recorded symmetrically, both tickers
  as co-equal subjects of the same external factor.
- Every record must identify its subject(s), object (if directional), and direction explicitly —
  no record may leave directionality implicit or inferred from filename order.
- A symmetric relationship must not be duplicated merely by reversing the two tickers — the
  alphabetical-filename rule (§B) combined with an explicit `symmetric: true`/`false` field is the
  intended mechanical enforcement for a future validator, not built by this filing.

### E. Evidence standard

Every future relationship claim must carry, at minimum:

- `claim` — the exact claim, stated narrowly enough to be falsifiable.
- `source` and `inspected_source_type` — what was consulted and whether it was a primary document
  (10-K/8-K/6-K/press release/IR material), a secondary source, or an uninspected citation.
- `source_date` and `effective_date` — when the source was published/filed and when the claim is
  asserted to hold.
- `evidence_classification` — exactly one of `observed | inferred | modeled | judgmental`.
- `relationship_status` — exactly one of `current | historical | potential | hypothetical`.
- `confidence` and `materiality` — both stated explicitly, never left to be inferred from prose tone.
- `decision_served` — at least one value from §F's closed vocabulary.
- `uncertainty` — what specifically is not known or could invalidate the claim.
- `disconfirming_evidence` — any known evidence against the claim, when known; never omitted merely
  because it complicates the record.
- A review/freshness block reusing this repository's existing conventions
  (`review.cadence_days`/`last_reviewed`/`next_due`/`log`, matching the frozen Company Intelligence
  schema — no new freshness mechanism invented).

Rules governing this standard: primary sources are preferred over secondary; every claim requires
its own citation, not a blanket source list; a search-engine snippet is not itself inspected
evidence and must be labeled as such (matching every existing WS-0005 batch's "attempted but not
directly inspected" disclosure convention); a blocked source must be disclosed, never silently
substituted with an uninspected secondary source presented as equivalent; an unknown or
confidential dependency must never be recorded as an absent one — silence in available sources is
not evidence of non-existence and must be disclosed as such; inference and judgment must be labeled
via `evidence_classification`, never blended into `observed`; an economically immaterial
relationship (per its own `materiality` field) should not receive a record merely because it exists
— materiality is a gating question, not a formality; stale, conflicting, or unverifiable evidence
may require abstention (no record filed, or an explicit `relationship_status: hypothetical`
disclosure) rather than a forced conclusion.

### F. Named decisions served

A closed initial `decision_served` vocabulary is frozen:

- `duplicate_exposure_detection`
- `thesis_monitoring`
- `stress_testing`
- `next_dollar_or_opportunity_cost`
- `missing_exposure_review`
- `zero_based_portfolio_review`

A future relationship record must name at least one value from this list. This field is explanatory
and advisory only — it creates no policy authority, and a record naming a value here never itself
triggers, recommends, or implies the named decision's outcome.

### G. Structural vs. measured relationships

Structural evidence (the twelve primitives above: business dependencies, shared customers/
suppliers, shared demand drivers, substitutes, competitors, common regulation, common geographic/
financing/energy/geopolitical risk) and measured market evidence (return correlation, beta,
drawdown co-movement, volatility, stress-period price behavior) must:

- appear as separate fields/sections in any future record or derived view, never compressed into
  one score;
- retain separate provenance and dates — a structural claim's evidence date and a correlation
  study's data window are never conflated;
- never allow low historical price correlation to be treated as disproving a documented structural
  dependency (correlation can be temporarily masked by unrelated factors);
- never allow high historical price correlation alone to be treated as proving the same underlying
  economic thesis (correlation can arise from shared macro beta with no structural link at all — the
  exact distinction this repository's own cluster-cap correlation scans, and CLAUDE.md's declined
  T1-AI-infra and enterprise-software cluster-cap proposals, already draw between a narrow shared
  mechanism and generic sector/index-flow beta).

**No price-correlation study is authorized by this decision.** Any future correlation study requires
its own separate bounded charter — methodology, data period, parameter choices, trial limits, tests,
independent review, and principal approval — matching `MARGIN-0005`'s and `LADDER-0001`'s existing
research-charter precedent exactly; this filing does not pre-authorize, sketch, or shortcut that
future charter in any way.

### H. Existing-capability reuse requirement

The future inventory unit authorized by §I must inspect and reuse, before any new research, exactly:
all ten existing `intelligence/*COMPARISON*.md` artifacts; both existing Theme Intelligence records
(`ai_infrastructure`, `life_sciences_tools_medtech`); `issuer_lookthrough.yaml`; existing cluster/cap
decisions and their retained correlation rationale (`semis`, `power_infra`, `oil` — including the
declined T1-AI-infra and enterprise-software cluster-cap scans in CLAUDE.md's Decisions Log); every
existing Company Intelligence record's own evidence (already-disclosed customer/supplier/competitor/
platform narrative content); and retained negative research or prior declined cluster proposals. No
existing artifact may be silently overwritten or reinterpreted by that future unit. Any conflict
found between existing artifacts must be disclosed and reconciled in the inventory's own report, not
silently resolved in either direction.

### I. Authorization for one future inventory-only unit

Exactly one later bounded implementation unit is authorized, effective only after **this** governance
decision is independently reviewed, principal-accepted, merged, and post-merge verified — not
effective on this filing's own merge alone for the future unit to *begin*, but the future unit's
authorization itself becomes live at that point, matching `LADDER-0001`/`CHART-0001`'s own "future PR
gated on this governance decision's own merge" convention.

**That later unit may:**

1. create `relationship_validator.py` (schema/taxonomy/evidence-standard validation only, matching
   `intelligence_validator.py`'s existing read-only, non-coupled design discipline);
2. create `test_relationship_validator.py`;
3. produce exactly one retained audit artifact under `governance/audits/`;
4. inspect the 27-name canonical roster (per §J);
5. inventory relationship evidence already present in the ten comparison artifacts, the two Theme
   Intelligence files, and `issuer_lookthrough.yaml` (per §H);
6. classify existing evidence against the twelve primitive relationship types in §C;
7. identify named cross-batch relationship gaps (evidence a comparison artifact already implies but
   no primitive record type currently captures);
8. identify which governed portfolio decisions (per §F's closed vocabulary) each existing or missing
   claim would improve.

**That later unit may not:**

- create any `intelligence/relationships/*.yaml` or `.md` record;
- conduct new external company research of any kind;
- alter any existing Company or Theme Intelligence record;
- compute price correlations of any kind;
- create scores, rankings, or any composite/aggregate metric;
- modify holdings, targets, tiers, gates, clusters, caps, ladders, trims, sells, margin, allocator,
  brokerage, or orders;
- implement "Eureka" (`OPS-0016`) in any form;
- begin Milestone 5 or any later WS-0005 milestone;
- create a new workstream.

### J. Inventory scope

The first inventory (per §I) is frozen to the current canonical 27-name equity roster only. The 26
retained non-canonical Company Intelligence records (tickers no longer in the canonical roster —
per `PI-0035`'s own classification, "retained/historical-advisory/non-current for Milestone 3
accounting") remain preserved but are outside the first inventory's scope unless separately
authorized later. The inventory must: account for all 27 canonical names; distinguish the 21 covered
from the 6 gated/deferred (4 per `PI-0035`: SNPS, ICE, SPGI, WM; 2 per `PI-0033`: RKLB, TSLA);
preserve every existing gate and disposition exactly as filed; not conduct external research to test
whether any gated name's real-world reopening-trigger event has occurred (that determination is
explicitly outside this unit's and the future inventory unit's scope, matching `PI-0037`'s own
identical disclosure); and report any unsynchronized real-world gate event it happens to notice as
discovered work, never act on it directly.

### K. Milestone status

This filing authorizes the bounded future inventory unit (§I) but does not itself perform that
inventory, and does not claim that substantive Milestone 4 relationship-mapping work is complete or
begun. `operations/WORKSTREAMS.yaml`'s WS-0005 entry is updated only to the minimum degree §L below
and the accompanying workstream-register filing require: the top-level `status: in_progress` and
`priority: primary` are unchanged; `authorized_scope` is unchanged (this filing's own future-unit
authorization is recorded via an additive milestone-adjacent entry, matching this repository's own
`OPS-0016`-cross-reference-entry precedent, not by editing the existing `authorized_scope` prose,
which continues to describe only the already-executed Milestones 1-2); `prohibited_scope` is
unchanged; `completion_criteria` is unchanged. The `milestone-4-portfolio-relationship-mapping`
gate's own `status: proposed` is unchanged by this filing — this decision freezes doctrine and
authorizes one narrow future inventory step; it does not flip Milestone 4 to `in_progress`, since
substantive relationship-mapping work has not begun and inventory-only classification of already-
existing evidence is not itself "relationship mapping" within the meaning of Milestone 4's own gate
description. The distinction between (a) this schema/taxonomy/evidence-standard freeze, (b) the
future inventory-only implementation, (c) future relationship-content batches (each requiring its
own separate future authorization, not granted here), (d) future derived views (§B, not authorized
here), and (e) the later Milestone 5 zero-based review is stated explicitly so no future reader
conflates any of the five. This filing does not activate relationship-content research of any kind.

### L. Non-authority

This decision does not authorize: any relationship-content record; any external relationship
research; any price-correlation study; any graph or "Eureka" (`OPS-0016`) implementation; any
automatic scoring, ranking, or aggregation; any policy change; any target, tier, cap, cluster, gate,
ladder, trim, sell, holdings, margin, allocator, brokerage, or order change; Milestone 5 or any later
WS-0005 milestone; or a new workstream.

### M. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (WS-0005 only — one additive milestone-adjacent entry, one
`evidence_refs` pointer, and the `active_branch`/`active_pr`/`last_verified_main_sha`/
`last_verified_date` self-reference fields per `OPS-0001`'s existing convention); (4) `CLAUDE.md`
(one concise Decisions Log pointer entry). No production code, no `intelligence/relationships/`
file, no `relationship_validator.py`, no `governance/audits/` artifact, no other workstream, and no
existing Company/Theme Intelligence record is touched.

### N. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (this is `OPS-0009` Lane G — a new governance authorization, full
weight, never reduced), complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This decision does
not mark itself ready and does not authorize its own merge. Nothing in §§A-M above becomes
effective, and the future inventory unit in §I remains unauthorized to begin, until this PR merges
to `main`.

## Rationale

**Why `REL-0001`, not `PI-####` or a new `OPS-####` entry.** See the Context section's
"Decision-identifier determination" above — restated briefly: `PI-####` is frozen as a one-way,
non-relational Company/Theme Intelligence series (`PI-0006`); Milestone 4's subject is inherently a
two-endpoint, directional/symmetric, cross-company record type that does not fit that frozen shape
without silently expanding it. `OPS-####` is operations/workstream-coordination machinery, not
domain content governance. `LADDER-0001` and `CHART-0001` already establish, and this filing
independently re-applies, the correct test: mint a new prefix exactly when the domain is genuinely
distinct, never as a default or as aesthetic preference — confirmed here by an actual schema/
taxonomy/evidence-standard difference (directionality, symmetric-pair-collision avoidance,
structural-vs-measured separation), not merely a naming preference.

**Why these exact twelve primitives, and why three specific conclusion-types are excluded.** The
twelve are chosen to be independently observable and falsifiable — each names a concrete mechanism
(a shared supplier, a shared regulator, a customer relationship) a reviewer could in principle verify
against a primary source. `duplicate_economic_exposure`, `correlated_loss_mechanism`, and
`missing_exposure` are excluded as primitives specifically because they are *conclusions drawn from*
one or more primitives plus judgment, not directly observable facts — allowing them as primitive
record types would let a future record assert a conclusion as if it were sourced evidence, exactly
the failure mode §E's evidence-classification field (`observed | inferred | modeled | judgmental`)
exists to prevent.

**Why directionality is split by relationship type rather than left uniform.** Dependency-shaped
relationships (supplier/customer/manufacturing/platform/capex) are asymmetric by construction — A
depending on B is a different fact from B depending on A. Shared-exposure relationships (regulatory,
commodity, financing, geographic) are symmetric by construction — both companies share the same
external factor. Competitive relationships sit in between (competitor/complement usually symmetric;
substitute sometimes directional) and are the one category requiring an explicit per-record
declaration rather than a fixed rule, since a real asymmetric-substitute case exists (a customer can
switch from A to B without the reverse holding, e.g. a premium good substituting for a budget one but
not vice versa) that a uniform symmetric rule would misrepresent.

**Why structural and measured-correlation evidence must never be compressed into one score.** This
repository's own Decisions Log already demonstrates the failure mode directly: the T1 AI-infrastructure
cluster (7 names, real concentration by every qualitative measure) scanned at only 0.302 average
pairwise correlation and was correctly *not* capped, while the oil cluster (2 names) scanned at 0.819
and was capped — a single blended score would have either over- or under-weighted one of these two
cases. Keeping the two evidence types separate, with separate provenance and dates, preserves exactly
the distinction that scan already required a human to draw manually; encoding it as doctrine here
keeps a future automated or semi-automated relationship view from silently discarding it.

**Why an inventory-only next step, not content research.** `OPS-0006`'s original Milestone 4 roadmap
line already anticipated "kept explicitly distinct from measured price correlation" but never defined
how; every existing comparison artifact (`BATCH1` through `BATCH9`, `WDC_SANDISK`) already contains
relationship-relevant prose that has never been classified against a taxonomy or checked for coverage
gaps. Classifying what already exists, without new research, is strictly smaller and more reversible
than beginning content research against an unfrozen taxonomy — exactly this repository's own
"smallest reversible next step" discipline (`PI-0002` through `PI-0009`'s incremental-pilot precedent,
`LADDER-0001`'s protocol-before-simulation precedent) applied to a new domain.

## Alternatives Considered

- **Reuse `PI-####` for relationship records, treating them as an extension of Company Intelligence.**
  Rejected — `PI-0006` froze Company/Theme Intelligence as explicitly one-way and non-relational
  ("the graph is a reporting view, not a stored data model"); silently reinterpreting that frozen
  doctrine to admit a two-endpoint record type would violate `governance/decisions/README.md`'s own
  rule against silently rewriting original reasoning, and would require its own separate supersession
  decision this filing is not authorized to make.
- **File this as an `OPS-####` workstream-mechanics decision.** Rejected — this is domain-content
  governance (a schema, a taxonomy, an evidence standard) for one specific workstream's one specific
  milestone, not cross-cutting operations/workstream-register machinery; every existing `OPS-####`
  entry governs process, not a single content domain's schema.
- **Defer the taxonomy/evidence-standard freeze to the future inventory unit itself, authorizing only
  "go inventory and figure out the schema as you go."** Rejected — an inventory performed against an
  unfrozen taxonomy cannot be consistently classified or later validated, and would force the
  inventory unit to make governance-level judgment calls (what counts as a primitive type, how
  directionality works) that belong to this Lane G filing, not an inventory-only implementation
  session.
- **Authorize a graph database or a stored relationship index (`intelligence/relationships/index.yaml`)
  for faster lookup.** Rejected — directly contradicts this repository's own repeatedly-reaffirmed
  filesystem-is-the-index doctrine (`PI-0001`, `PI-0006`), evaluated on the same seven criteria that
  doctrine was originally frozen against and re-failing all seven for the same reasons.
  A future rendering may compute a graph view from the filesystem at read time; it may never become
  the authoritative store.
- **Authorize a bounded price-correlation study alongside the schema freeze, since Milestone 4's
  roadmap mentions correlation.** Rejected — conflating a doctrine freeze with a live research charter
  in one filing would exceed this unit's own bounded Lane G authorization (schema/taxonomy/evidence-
  standard and one inventory unit only) and would require its own separate `MARGIN-0005`/`LADDER-0001`-
  style pre-registered protocol, charter, and review cycle this filing does not attempt.
- **Skip minting a new prefix and file this under the next available `PI-####` number purely to avoid
  process overhead.** Rejected per the task's own explicit instruction not to invent a prefix "merely
  for aesthetics," and equally not to avoid one merely for convenience — the domain-boundary test in
  the Rationale above is met on its merits, independent of which choice is procedurally lighter.

## Consequences

**Authorized, effective only on this decision's merge:** the frozen pairwise relationship-record
source-of-truth convention (§B); the closed twelve-item primitive relationship taxonomy and its three
explicitly excluded derived-conclusion types (§C); directionality rules (§D); the evidence/abstention
standard (§E); the closed `decision_served` vocabulary (§F); the structural-versus-measured-
correlation separation (§G); the existing-capability reuse requirement (§H); exactly one future,
separate, bounded inventory-only implementation unit (§I), itself gated on its own independent
review, correction if needed, re-review, principal acceptance, merge, and post-merge verification;
the canonical-27-name-roster-only inventory scope (§J).

**Not authorized by this filing, now or ever without a further separate decision:** any
`intelligence/relationships/*.yaml` or `.md` record; any external relationship research; any price-
correlation study of any kind; any graph or "Eureka" implementation; any automatic scoring, ranking,
or aggregation; any `relationship_validator.py` or `governance/audits/` artifact beyond exactly what
§I's future unit itself is separately gated to produce; any target/tier/cap/cluster/gate/ladder/
trim/sell/holdings/margin/allocator/brokerage/order change; Milestone 5 or any later WS-0005
milestone; and a new workstream.

**Unchanged by this decision:** every existing Company/Theme Intelligence record; every existing
comparison artifact; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`allocate.py`, `levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s top-level `status`,
`priority`, `authorized_scope`, `prohibited_scope`, and `completion_criteria`; the
`milestone-4-portfolio-relationship-mapping` gate's own `status: proposed`; Milestone 3's own
`status: complete` (`PI-0037`, unedited, not reopened). No relationship content, research,
correlation study, policy change, or "Eureka" implementation has occurred as a result of this
filing.

This decision becomes effective only when its implementing pull request merges to `main`.
