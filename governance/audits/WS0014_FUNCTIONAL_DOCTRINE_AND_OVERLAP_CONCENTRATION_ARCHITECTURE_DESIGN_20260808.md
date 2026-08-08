# WS-0014 Functional Doctrine + Overlap/Concentration Architecture Design — retained artifact

**Filed under**: `XASSET-0005` (`governance/decisions/XASSET-0005-functional-doctrine-and-overlap-concentration-architecture.md`)
**Date**: 2026-08-08
**Scope**: `XASSET-0001` §D + §F / §J steps 6–7 — structural design of (1) a shared functional-doctrine
schema for `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, and `DEBT_REDUCTION`, and (2) a ten-dimension
overlap/concentration-model architecture. Design only. No capital-use type is populated and no
overlap/concentration figure is computed by this artifact.

This artifact is the full field-by-field design. The decision file summarizes it and carries the
authorization/consequences text; this document is the retained detail, matching the
`TIER-0001`→`TIER-0002` and `XASSET-0001`→`XASSET-0002` supporting-artifact precedent.

---

## 0. Bounded correction (same day, this PR)

An independent exact-head review of this filing's original submission (head
`6b726de3fd2da7ff83f103d109db4166a70981e3`) returned CHANGES REQUIRED — 0 BLOCKING / 1 MAJOR / 0 MINOR /
1 non-actionable NOTE, independently confirmed before any fix. **MAJOR, resolved**: `XASSET-0001` §F
enumerates nine "at minimum" required overlap/concentration/risk items, not the eight this design
originally addressed — two items, geographic/currency exposure and whole-portfolio volatility/drawdown
concentration, had no `dimension_id` anywhere in the original §6.1 table, undisclosed. Resolved by adding
two new dimensions, `geographic_currency_exposure` and `whole_portfolio_volatility_drawdown_concentration`
(§6.1), both following the identical `interface_placeholder` pattern already used for `crypto_correlation_
interface`/`defensive_offset_interface` — the population grows from eight to ten, every "eight"
population/count reference throughout §6 and §7/§8's validator and test specifications is corrected to
"ten," and §F's ninth item (liquidity) is explicitly addressed as a disclosed, deliberate non-dimension
(already represented per-instrument in the ETF/crypto/functional-doctrine schemas, with no existing
whole-portfolio rollup mechanism to extend) rather than left to look like an unexplained omission. No
functional-doctrine content, no `structural_reference`/hash mechanism, no `hard_constraint_status`/
`economic_assessment_readiness` separation, and no validator/test lesson-carrying content changed — the
correction is scoped entirely to §6's dimension table and the population-count references it drives
downstream. The **NOTE** (whether "eight, specifically" traces to a concrete principal enumeration or
this implementing session's own synthesis of §F) is carried forward as accurate and non-actionable,
unchanged by this correction — the corrected population of ten is derived directly from `XASSET-0001` §F's
own text, not from the original eight-item authorizing-prompt list, which this correction supersedes as
the controlling source for population size.

**Second bounded correction (same day, this PR).** A fresh independent exact-head delta review of the
first correction's own head (`a8020e1ae097e6ea31ce8e86a673c8af948aae40`) confirmed the MAJOR above
genuinely resolved and every other boundary in this artifact untouched and intact, but found two new
MINOR findings, 0 BLOCKING, 0 MAJOR. **MINOR-1, resolved**: the decision file's own "Why the
overlap-model dimensions stay ten separate records" paragraph — heading already corrected — still read
"**Eight** independently evidenced, independently abstaining records..." two lines below, a
same-paragraph contradiction directly contradicting this section's own completeness claim above ("every
'eight'/'eight-dimension' reference... is corrected to 'ten'"). Fixed: "Eight" → "Ten," in the decision
file only (this artifact never had that specific line). **MINOR-2, resolved**: §6.1's liquidity-exclusion
paragraph originally argued liquidity needs no dimension because it's "already represented per-instrument"
with "no existing... mechanism to extend... inventing one here would be... asset-specific-judgment
content" — the review correctly identified this as indistinguishable from the reasoning that had just
justified adding the other two dimensions (both `geographic_currency_exposure` and `whole_portfolio_
volatility_drawdown_concentration` also lack an aggregation mechanism, and were resolved by adding a pure
`interface_placeholder` rather than treating the absence of a mechanism as a reason to add nothing).
Replaced §6.1's liquidity paragraph with the textually-grounded distinction the review itself surfaced:
`XASSET-0001` §F phrases liquidity at the **per-sleeve** level ("how quickly *each sleeve* can be
converted to cash"), already fully answered by the three existing per-instrument liquidity axes, while
items 4 and 6 are phrased at the **whole-portfolio/cross-sleeve** level (item 6 explicitly: "across the
whole portfolio, not sleeve-by-sleeve in isolation"; item 4 inherently, since geographic/currency
exposure spans multiple sleeves) — a distinction in kind, not degree, and the genuine reason liquidity
gets no placeholder while the other two do. The identical fix was mirrored in the decision file's own
shorter summary of this rationale. Neither fix touches functional-doctrine content, the GLD structural-
reference/hash mechanism, the `DEBT_REDUCTION` split, or the validator/test specification (§7/§8
unchanged by this second correction). The original NOTE above is carried forward unchanged — the review
explicitly confirmed it was neither worsened nor resolved by either correction round.

---

## 1. Why one artifact covers both architectures

`XASSET-0001` §J explicitly permits this: "cash/GLD/debt doctrine + overlap-model **architecture** (steps
6–7) — permitted to batch only where no asset-specific judgment occurs (i.e., defining the doctrine's
shape and the overlap model's shape, not applying either to a specific instrument or sleeve)." Both
schemas below are shape-only: the functional-doctrine schema defines what a future `CASH`/`RESERVE`/
`GLD_DEFENSIVE_ROLE`/`DEBT_REDUCTION` record would contain without stating what any of them currently is;
the overlap-model schema defines what a future dimension record would contain without computing any
dimension's current value for the live portfolio. Neither schema is applied to a specific instrument,
sleeve, or dollar figure anywhere in this artifact.

## 2. Method: reuse general classification hygiene, do not reuse asset-shaped fields

Same starting question `TIER-0001`/`TIER-0002` and `XASSET-0002` both asked: *does this field exist in
currently-authoritative repository evidence, and does representing it as a standing fact materially
improve a future decision that today requires manual cross-referencing or is not represented at all?*
Two structural moves carry over, because they are general classification-hygiene principles this
repository has now applied three times (equity, ETF/crypto, this design) — not equity- or fund-shaped
content:

- **Narrative-judgment fields are kept separate from mechanically-computed fields.** `TIER-0002`
  separated `economic_role`/`capital_priority` from `risk_concentration`; `XASSET-0002` separated
  `structural_role`/`constituent_exposure` from `overlap_and_concentration`, and
  `network_fundamentals`/`economic_model` from `correlation_and_volatility`. This design applies the same
  split twice more: `hard_constraint_status` (§3.2) is kept structurally independent of
  `economic_assessment_readiness` (§3.2) within the functional-doctrine schema, and the overlap model's
  own `computation_status`/`dimension_type` fields (§6) keep "what kind of evidence is this" separate from
  any judgment about what it means.
- **Evidence quality and abstention are per-field disciplines, not a bolted-on axis.** Both schemas below
  use the same `not_applicable`/`unable_to_determine` two-state discipline `TIER-0004`/`XASSET-0002`
  already established, plus a record-level `evidence_quality` axis and `abstention_index` rollup, not a
  separate "uncertainty axis."

One structural move is **new to this design**, because no prior framework in this repository needed it:
a **cross-schema reference-by-hash mechanism** (§3.4) — `GLD_DEFENSIVE_ROLE` must consume GLD's own
sealed ETF structural record without duplicating any of its seven fields, a situation `TIER-0002`'s
equity schema and `XASSET-0002`'s ETF/crypto schemas never faced, since none of them needed to point at
another schema's own sealed content.

## 3. Functional-doctrine framework — `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, `DEBT_REDUCTION`

### 3.1 Candidate fields evaluated (twelve named in the authorizing prompt) → seven designed axes plus four envelope-only fields

| Candidate (as named) | Disposition | Reasoning |
|---|---|---|
| `capital_use_type` | **Kept** → envelope discriminator, not an axis | The population identifier itself — closed to exactly four values (§3.2). Not a "judgment" field; it is which of the four fixed record types this is. |
| `functional_role` | **Kept** → axis | No existing mechanism represents "what portfolio job does this use of capital do" as a standing categorical fact — the direct functional-doctrine analogue of the ETF framework's `structural_role`. |
| `hard_constraint_status` | **Kept** → axis, deliberately also projected at the envelope level | The one field the authorizing design direction requires be *structurally*, not merely documentarily, separated from economic comparison — see §3.2 and §3.3's dual-visibility design. |
| `economic_assessment_readiness` | **Kept** → axis, shape varies by `capital_use_type` | Direct analogue of `XASSET-0002` §6.3's `valuation_and_economic_assessment_readiness` — forced abstention today, asset-appropriate name (nothing here has a market "valuation" in the equity/ETF/crypto sense; capital-use types are compared on economic *opportunity cost*, not priced). Split into two independent sub-readinesses for `DEBT_REDUCTION` only (§3.5). |
| `liquidity_character` | **Kept** → axis | Distinct evidence question from capital preservation: how quickly can this capital use be converted to, or does it already exist as, spendable cash — mirrors the ETF/crypto `liquidity`/`liquidity_and_market_structure` axes, renamed to avoid a bare-key collision with the ETF schema's own `liquidity` key (load-bearing for §7 point 4's cross-schema no-leakage check). |
| `capital_preservation_character` | **Kept** → axis | A genuinely distinct question from liquidity: does this capital use carry market/price risk to its principal, or is it structurally stable — the question that most directly separates `CASH`/`RESERVE` (no market risk to the capital itself) from `GLD_DEFENSIVE_ROLE` (references a priced, market-exposed instrument) and `DEBT_REDUCTION` (a liability reduction, not an asset at all — see §3.2's closed vocabulary). |
| `structural_risk_flags` | **Not a standalone axis** → envelope-only field, mirroring `XASSET-0002` §6.1 | A read-only rollup of `hard_constraint_status`/`economic_assessment_readiness`, never independently computed — same rule as every prior framework's own envelope design (§3.3). |
| `evidence_quality` | **Kept** → axis | Mirrors `TIER-0002`'s and `XASSET-0002`'s identical axis directly — reuses the exact `comprehensive`/`partial`/`limited` vocabulary already established twice. |
| `uncertainty_statement` | **Not a standalone axis** → envelope-only field (`uncertainty_summary`), mirroring `XASSET-0002` §6.1 | One required narrative sentence at the record level, not a seventh judgment axis — identical design choice to every prior framework. |
| freshness / stale-data state | **Kept, new** → axis (`freshness_state`) | Genuinely distinct from `evidence_quality` (how *well-sourced* the record is, at drafting time) — this axis asks how *current* the record's own factual basis is relative to a stated reference point (e.g., a holdings-sync date, a margin-classification run date), a concept no prior classification framework in this repository needed, because equity/ETF/crypto evidence is drawn from relatively slow-moving disclosures, while `CASH`/`RESERVE`/`DEBT_REDUCTION` in particular reference account-state facts that can move daily. Explicit design decision, not an omission from the equity/ETF/crypto precedent — see §3.2. |
| `later_governance_action` | **Kept** → envelope-only field | Mirrors `TIER-0007`'s reconciliation-record convention (a required-governance-action field distinct from the finding itself) — states what future authorization, if any, this record's own content implies is needed, without itself requesting it. |
| explicit abstention semantics | **Not a standalone field** → `abstention_index` envelope rollup, mirroring `XASSET-0002` §6.1 | Same mechanical rollup design as every prior framework — a list of every axis that abstained, with its stated reason, for a future synthesis unit to scan without re-reading every axis. |

**Result: 6 substantive axes** (`functional_role`, `hard_constraint_status`,
`economic_assessment_readiness`, `liquidity_character`, `capital_preservation_character`,
`freshness_state`) **plus `evidence_quality`** (the same 6-axes-plus-evidence-quality shape every prior
framework in this repository uses), and **5 envelope-only fields**
(`structural_risk_flags`, `uncertainty_summary`, `later_governance_action`, `abstention_index`, plus the
population discriminator `capital_use_type` itself).

### 3.2 Field-by-field design

For every field: **purpose**, **evidence inputs**, **closed vocabulary**, **abstention state**,
**prohibited inference**, **downstream use**.

#### `capital_use_type` (envelope discriminator, not an axis)

- **Purpose**: identify which of the four fixed capital-use types this record is.
- **Closed vocabulary**: exactly `CASH` | `RESERVE` | `GLD_DEFENSIVE_ROLE` | `DEBT_REDUCTION`. No fifth
  value; no future implementation may add a value without its own separate schema-amendment decision
  (matching `TIER-0002`→`TIER-0004`'s own narrow-schema-amendment precedent).
- **Downstream use**: selects which conditional shape `economic_assessment_readiness` (§3.5) and
  `structural_reference` (§3.4) must take; the population identifier a future implementation's validator
  enforces exactly (four records, no more, no fewer).

#### `functional_role`

- **Purpose**: record what portfolio job this use of capital does, as a categorical fact — the
  functional-doctrine analogue of the ETF framework's `structural_role`, without assigning a target
  weight or a policy verdict.
- **Evidence inputs**: `targets.yaml`'s own row (for `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE` — symbol/
  `asset_class` identity only, never `target_pct`, per §3.6's contamination rule); `CLAUDE.md`'s existing
  Portfolio Doctrine and Guardrails text, where it already states a relevant fact (e.g., the cash-tight
  guardrail, the margin-cap/buffer-floor doctrine) — cited as evidence, never restated as this record's
  own invented judgment.
- **Closed vocabulary** (`role_category`): `operational_liquidity_float` | `capital_preservation_buffer`
  | `defensive_offset_or_ballast` | `leverage_reduction` | `other_functional_role` (with a required
  one-sentence `role_basis` for `other_functional_role`, matching every prior framework's own
  open-ended-catch-all discipline).
- **Abstention state**: `unable_to_determine` with required `abstention_reason`. No `not_applicable` —
  every one of the four capital-use types has *some* functional role by definition; the question is only
  whether current evidence can name it with confidence.
- **Prohibited inference**: no target weight, no "this capital use deserves X% of book," no buy/sell/
  fund/repay directive, no ranking against another capital-use type's role.
- **Downstream use**: `role_summary` field of the cross-asset handoff envelope (§3.3); the fact a future
  cross-asset opportunity-cost synthesis (`XASSET-0001` §E) would read to know what kind of capital use
  it is comparing — this axis records *what the capital use is for*, never *what policy should assign
  it*.

#### `hard_constraint_status`

- **Purpose**: record, as a structural fact independent of any economic comparison, whether this
  capital-use type is currently subject to an already-governed hard constraint (e.g., the 30%
  margin-buffer floor's interaction with `DEBT_REDUCTION`, or a future reserve-floor rule for `RESERVE`)
  — never a policy recommendation about what the constraint should be.
- **Evidence inputs**: `CLAUDE.md`'s own Portfolio Doctrine and Guardrails sections (the 1.8x leverage
  cap, 30% buffer floor, cash-tight guardrail) where directly applicable; a future, separately governed
  functional-doctrine decision if and when one names a new hard constraint for `CASH`/`RESERVE`/
  `GLD_DEFENSIVE_ROLE` specifically (none exists today beyond the margin doctrine, which bears directly
  only on `DEBT_REDUCTION`).
- **Closed vocabulary**: `binding` (boolean — whether a currently-governed hard constraint applies to
  this capital-use type today); `constraint_source` (required citation string when `binding: true` —
  e.g., "CLAUDE.md Portfolio Doctrine: 30% margin-buffer floor, hard cutoff"; `none_currently_binding`
  literal value when `binding: false`).
- **Abstention state**: no `unable_to_determine` path — this field is a citation-backed structural fact
  (either an existing governed constraint applies, and its source can be named, or none does), not a
  judgment that can be under-evidenced in the way a narrative axis can.
- **Prohibited inference**: **this field may never be computed from, derived from, or overridden by
  `economic_assessment_readiness`'s value, and vice versa** — the mechanical enforcement of the
  authorizing design direction's own requirement. No numeric threshold restatement (the 1.8x cap and 30%
  floor are cited by reference to `CLAUDE.md`, never restated as a new number in this schema).
- **Downstream use**: `hard_constraint_signal` field of the cross-asset handoff envelope (§3.3),
  deliberately kept in its own field, never merged with `economic_assessment_readiness_summary` in the
  same handoff object — see §3.3's dual-projection design.

#### `economic_assessment_readiness`

- **Purpose**: the functional-doctrine analogue of `XASSET-0002` §6.3's forced
  `valuation_and_economic_assessment_readiness` — states plainly that no governed methodology exists yet
  to compare this capital-use type's opportunity cost against any other sleeve, rather than silently
  omitting the question.
- **Evidence inputs**: none required beyond the forced value itself — this field states an absence, not
  a finding.
- **Shape, conditional on `capital_use_type` (§3.5 gives the full split rationale)**:
  - For `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`: a **single-part** object, `{status, rationale}`.
  - For `DEBT_REDUCTION`: a **two-part** object, `{avoided_borrowing_cost_readiness: {status,
    rationale}, survivability_and_buffer_benefit_readiness: {status, rationale}}` — never blended, never
    a single combined `status`.
- **Closed vocabulary**: exactly one value today, `assessment_required`, in every `status` sub-field
  across both shapes — the direct analogue of `TIER-0009`'s own doctrinally-forced, zero-exception
  `valuation_required` design. No second value exists in the vocabulary yet; a future governed
  opportunity-cost methodology, once it exists, would itself add the value that supersedes this forced
  default (`XASSET-0002` §6.3's identical precedent).
- **Abstention state**: not applicable — the forced value itself is the record-level abstention; there
  is no further per-record abstention path on this field.
- **Prohibited inference**: no fair value, no expected return, no avoided-interest figure, no target
  allocation percentage, no ranking against another capital-use type's readiness — enforced identically
  to `TIER-0009`'s own forced-value mechanical check (§7 below).
- **Downstream use**: `economic_assessment_readiness_summary` field of the cross-asset handoff envelope
  (§3.3) — copied verbatim, never independently re-derived.

#### `liquidity_character`

- **Purpose**: record how readily this capital use exists as, or converts to, spendable cash — distinct
  from margin-buffer capacity, which is an account-level fact this schema does not touch.
- **Evidence inputs**: for `CASH`/`RESERVE`, the account's own cash-balance structure (a structural fact,
  not a dollar figure — this schema records the *character* of the liquidity, never a balance); for
  `GLD_DEFENSIVE_ROLE`, GLD's own already-sealed ETF `liquidity.liquidity_tier` value, cited by reference
  (never restated as a duplicate field — see §3.4); for `DEBT_REDUCTION`, the observation that paying
  down debt consumes liquidity rather than characterizing any liquidity of its own.
- **Closed vocabulary**: `immediately_liquid` | `liquid_via_referenced_structural_asset` |
  `not_applicable` | `unable_to_determine`.
- **Abstention state**: `not_applicable` is reserved for `DEBT_REDUCTION` specifically — a liability
  paydown does not itself have a liquidity character in the sense the other three types do; this is a
  structural fact about what kind of capital use `DEBT_REDUCTION` is, not an evidence gap.
  `unable_to_determine` (with `abstention_reason`) is reserved for a genuine evidence gap on `CASH`/
  `RESERVE`/`GLD_DEFENSIVE_ROLE`.
- **Prohibited inference**: no numeric days-to-liquidate estimate, no stress-scenario liquidity model —
  states the capital use's own structural liquidity character, nothing modeled.
- **Downstream use**: `liquidity_risk_summary` field of the cross-asset handoff envelope (§3.3); a
  required future input to `XASSET-0001` §F's whole-portfolio liquidity accounting.

#### `capital_preservation_character`

- **Purpose**: record whether this capital use's own principal carries market/price risk, or is
  structurally stable — the axis that most directly distinguishes the four types from one another in
  kind.
- **Evidence inputs**: the same structural facts as `functional_role` — no new evidence source beyond
  what `targets.yaml`'s `asset_class` tags and `CLAUDE.md`'s doctrine already establish.
- **Closed vocabulary**: `principal_stable_no_market_risk` | `market_exposed_via_referenced_structural_
  asset` | `reduces_liability_not_an_asset` | `unable_to_determine`.
- **Abstention state**: no `not_applicable` — every capital-use type has some capital-preservation
  character by definition (even `DEBT_REDUCTION`'s `reduces_liability_not_an_asset` is itself a
  determinate value, not an absence). `unable_to_determine` (with `abstention_reason`) is reserved for a
  genuine evidence gap.
- **Prohibited inference**: no derived "safer than X" ranking against another capital-use type or against
  any equity/ETF/crypto holding — states the structural character, never a comparative verdict.
- **Downstream use**: structural-risk-flag input to the cross-asset handoff envelope (§3.3); a required
  future input to the overlap model's `defensive_offset_interface` dimension (§6) — this axis is exactly
  the fact that dimension would need once `GLD_DEFENSIVE_ROLE` is ever populated.

#### `freshness_state`

- **Purpose**: record how current this record's own factual basis is, relative to a stated reference
  point — distinct from `evidence_quality` (how well-sourced the record is at drafting time).
- **Evidence inputs**: the reference point each capital-use type's own evidence naturally has — for
  `CASH`/`RESERVE`, `holdings.yaml`'s own most recent sync date; for `GLD_DEFENSIVE_ROLE`, the
  `as_of`/hash-pin date on the referenced ETF record (§3.4); for `DEBT_REDUCTION`, the date of the most
  recent `margin_state.classify_margin_state()` run this record's own evidence cites.
- **Closed vocabulary**: `current` | `stale_needs_refresh` | `unable_to_determine_freshness`, plus a
  required `as_of_reference` string naming the specific evidence date or event this record's own facts
  are pinned to.
- **Abstention state**: `unable_to_determine_freshness` (folded into the vocabulary itself, since every
  record has *some* freshness relationship to its own evidence — there is no genuine `not_applicable`
  case).
- **Prohibited inference**: no automatic "this record needs re-drafting" trigger — this field discloses a
  fact for a human or a future governed process to act on; it does not itself schedule or request any
  action (that is `later_governance_action`'s job, §3.3, stated separately and only when genuinely
  implied).
- **Downstream use**: no dedicated cross-asset-handoff field — folded into `uncertainty_summary`'s own
  free-text disclosure when material, matching how `TIER-0007`'s reconciliation records handle a
  comparable freshness disclosure without inventing a dedicated handoff slot for it.

#### `evidence_quality`

- Identical design to `TIER-0002`'s and `XASSET-0002`'s own `evidence_quality` axis — reusing the exact
  `comprehensive`/`partial`/`limited` vocabulary. Not restated here to avoid duplication.

### 3.3 Shared envelope

| Field | Purpose | Notes |
|---|---|---|
| `capital_use_type` | population discriminator | exactly `CASH` \| `RESERVE` \| `GLD_DEFENSIVE_ROLE` \| `DEBT_REDUCTION` (§3.2). |
| `schema_version` | framework schema version string | mirrors `TIER-0002`/`XASSET-0002`'s own classification-record convention. |
| `provenance` | sources list, evidence-access disclosure | each source cited with type (primary/secondary) and access status, mirroring Milestone 6/7/8 and `XASSET-0002`'s disclosed-access-failure convention. |
| `evidence_quality_status` | copy of `evidence_quality.primary_source_coverage` | read-only projection, never independently computed (§3.6's rule). |
| `uncertainty_summary` | one required narrative sentence | names the single most significant evidence gap or open question for this record. |
| `structural_risk_flags` | mechanical rollup of `hard_constraint_status`/`capital_preservation_character` | a read-only projection, never a new computation (§3.6's rule). |
| `record_status` | `draft` \| `sealed` | mirrors Milestone 6's `lifecycle_status` sealing discipline. |
| `structural_reference` | present only when `capital_use_type: GLD_DEFENSIVE_ROLE`; forbidden otherwise | §3.4 below — the content-hash pin into GLD's sealed ETF record. |
| `later_governance_action` | free text, may be `none` | states what future authorization this record's own content implies is needed, if any. |
| `abstention_index` | list of every axis that abstained, with its stated reason | mechanical rollup, matching every prior framework's own design. |

**Two separate, deliberately un-merged projections, both required on every record** — the mechanical
enforcement of the authorizing design direction's structural-separation requirement:

| Handoff field | Sourced from | Never merged with |
|---|---|---|
| `hard_constraint_signal` | `hard_constraint_status.binding` + `.constraint_source` (verbatim copy) | `economic_assessment_readiness_summary` — no shared field, no shared computation, no field that reads both. |
| `economic_assessment_readiness_summary` | `economic_assessment_readiness` (verbatim copy — single-part `status` for three types, both sub-statuses for `DEBT_REDUCTION`) | `hard_constraint_signal` — same rule, opposite direction. |

Plus the same asset-neutral projections every prior framework's `cross_asset_handoff` object carries:
`role_summary` (from `functional_role.role_category`), `evidence_quality_summary` (from
`evidence_quality.primary_source_coverage`), `uncertainty_summary` (the envelope's own field, not
re-derived), `liquidity_risk_summary` (from `liquidity_character`).

**No numeric field exists anywhere in this envelope or in either functional-doctrine axis** — see §3.5's
rationale for why this design deliberately declines the ETF framework's own `expense_ratio_pct`-style
carve-out.

### 3.4 `structural_reference` — GLD structural/functional separation, mechanically enforced

**Present only when `capital_use_type: GLD_DEFENSIVE_ROLE`; the validator must reject its presence on any
other `capital_use_type`.**

- `source_instrument_id`: literal `"GLD"`.
- `source_schema`: literal `"etf_classification"` — the only value valid today; a future second
  cross-schema reference target, if one is ever needed, requires its own schema-amendment decision, not
  a silently widened vocabulary.
- `source_file`: literal `"intelligence/etf_classification/GLD.yaml"`.
- `referenced_content_sha256`: the pinned hash of GLD's sealed ETF record **at the time this
  functional-doctrine record is drafted or last refreshed** — computed via `etf_classification_
  validator.canonical_record_hash()` (the already-existing, already-tested function `etf_classification_
  validator.py:322` exposes), never a newly invented hashing scheme.

**Validator enforcement (§7 point 8 restates this as a formal requirement)**:

1. `structural_reference` is required, with all four sub-fields present, when and only when
   `capital_use_type: GLD_DEFENSIVE_ROLE`; forbidden (rejected as an unknown key) on `CASH`/`RESERVE`/
   `DEBT_REDUCTION` records.
2. When present, the validator recomputes GLD's **live** record hash via a read-only call to
   `etf_classification_validator.canonical_record_hash()` against the current `intelligence/
   etf_classification/GLD.yaml` and confirms it matches `referenced_content_sha256` exactly — a
   mismatch means the reference is stale (GLD's structural record has changed since this functional-
   doctrine record was last drafted) and the record is rejected until refreshed, mirroring the same
   staleness-detection discipline `REL-0001`'s relationship records already apply to Company Intelligence
   references.
3. **None of the ETF framework's own six axis key names** (`structural_role`, `constituent_exposure`,
   `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`)
   may appear anywhere in a `GLD_DEFENSIVE_ROLE` record, at any nesting level — a dedicated forbidden-key
   scan, the same mechanism every prior cross-contamination check in this repository uses. (`evidence_
   quality` is deliberately **not** on this forbidden list — every framework, including this one,
   legitimately carries its own copy of that general-hygiene axis; the prohibition is specifically
   against re-deriving GLD's *structural* facts, not against the shared evidence-quality concept.)
4. This mechanism **does not itself determine GLD's functional role** — it only makes the record that
   will eventually state that determination structurally incapable of also re-deriving or drifting from
   GLD's own separately-governed structural facts. No `GLD_DEFENSIVE_ROLE` value is assigned anywhere in
   this design.

### 3.5 `DEBT_REDUCTION`'s split `economic_assessment_readiness` — full rationale

The authorizing design direction requires avoided-borrowing-cost readiness exposed **separately** from
survivability/leverage-buffer benefit, never blended into one score or return. These are genuinely
distinct questions:

- **Avoided-borrowing-cost readiness** asks: is there a governed methodology to compare the *return*
  foregone (or gained) by paying down margin debt instead of deploying capital elsewhere — an
  opportunity-cost/return-shaped question.
- **Survivability-and-buffer-benefit readiness** asks: is there a governed methodology to assess how
  paying down debt changes the account's *risk posture* relative to the 1.8x leverage cap and 30% buffer
  floor — a risk/survival-shaped question, structurally adjacent to `hard_constraint_status` but
  evaluated here as a distinct forced-abstention state, not folded into that axis (because
  `hard_constraint_status` states whether a constraint *currently binds*, a present-tense structural
  fact, while this sub-field states whether a *methodology exists* to assess future buffer benefit, a
  forward-looking readiness question — genuinely different in kind).

Blending these into one figure would be exactly the failure mode the authorizing design direction
prohibits: a single "debt-reduction score" would silently average an opportunity-cost question against a
survival-risk question, the same category error `trim_backtest.md`'s own Decisions Log entry already
identified and rejected for leverage-adjusted drawdown ("the unlevered backtest got to hold through its
worst moment, a levered account may not" — return and survival are not fungible in this repository's own
established doctrine). Keeping them as two independently forced-abstention sub-fields, both `assessment_
required` today, preserves that distinction structurally rather than trusting a future drafting session
to remember it.

### 3.6 Contamination rule and abstention summary

**Contamination rule** (mirrors `XASSET-0004` §D's blindness boundary for crypto, applied here for the
first time to functional doctrine): no functional-doctrine record's judgment axes (`functional_role`,
`hard_constraint_status`, `economic_assessment_readiness`, `liquidity_character`, `capital_preservation_
character`) may be drafted from `holdings.yaml`'s actual cash/reserve dollar figures, `targets.yaml`'s
`target_pct` values, `margin_state.py`'s live account-specific numeric output (`leverage_ratio`,
`utilization`, actual dollar buffer), or any chart/technical signal — those are all *current portfolio
state*, not the *structural/functional character* this schema records. A future implementation's
evidence standard may cite the **existence** of a governed mechanism (e.g., "the 30% buffer floor exists,
per `CLAUDE.md`") but never the **current live value** of an account-specific number computed by that
mechanism.

**Abstention summary**: the same two-state discipline as every prior framework (`not_applicable` for a
structurally absent concept — e.g., `DEBT_REDUCTION`'s own `liquidity_character`; `unable_to_determine`
for a genuine evidence gap, always with a required `abstention_reason`) and the same non-cascading rule
(`TIER-0004`'s established precedent — a bounded unresolved item on one axis is never automatic grounds
for abstaining on another).

## 4. Read-only projection, not new computation

Identical rule to `XASSET-0002` §6.2, restated for this schema: every envelope field that summarizes an
axis value (`evidence_quality_status`, `structural_risk_flags`, `hard_constraint_signal`, `economic_
assessment_readiness_summary`, every `cross_asset_handoff` field) is **explicitly a copy of an
already-computed axis field**, never a new computation performed at the envelope level. A future
validator (§7) must enforce this by checking envelope-level fields against their source axis fields for
exact consistency — the same reconciliation discipline `recommendation_validator.py` already applies to
its own aggregate block, and `etf_classification_validator.py`/`crypto_classification_validator.py`
already apply to their own `structural_risk_flags`/`cross_asset_handoff` objects.

## 5. Whole-portfolio sequencing doctrine (restated, unchanged by this design)

This design occupies exactly `XASSET-0001` §J step 6's functional-doctrine-shape portion and step 7's
overlap-model-shape portion (§6 below). It does not perform, and does not authorize, any later step of
the seven-step sequence `TIER-0012`/`TIER-0013`/`XASSET-0002` §10 most recently restated:

1. define governed asset-appropriate frameworks — equities (`TIER-0002`, exists), ETFs and crypto
   (`XASSET-0002`, exists), functional doctrine (this design, step 6's schema-shape portion), overlap/
   concentration model (this design, step 7's schema-shape portion);
2. perform asset-appropriate valuation/economic assessment (future, separate, undesigned — this
   design's own forced `economic_assessment_readiness`/`avoided_borrowing_cost_readiness`/
   `survivability_and_buffer_benefit_readiness` fields are the explicit markers of this boundary, not an
   attempt to cross it);
3. conduct cross-asset opportunity-cost and overlap/concentration synthesis (`XASSET-0001` §E/§F,
   future — this design's ten dimension records, §6, are inputs to this step, not the step itself);
4. produce Level 1 sleeve targets (future);
5. produce Level 2 instrument targets inside each sleeve (future);
6. ingest and interpret governed chart evidence for applicable market-priced instruments, deployment/
   timing only (`XASSET-0001` §G, `TIER-0003` unweakened, future — this design touches no chart evidence
   anywhere);
7. perform final synthesis and determine holdings, target weights, deployment sequencing, and execution
   discipline (future).

## 6. Overlap and concentration-model architecture

### 6.1 Candidate dimensions evaluated → ten preserved dimensions, zero merges, zero composite

**Corrected by bounded review (§0 below).** The authorizing design direction named eight illustrative
dimensions, but `XASSET-0001` §F — the actual controlling authority this filing is designing an
architecture *for* — enumerates **nine** items "at minimum": ETF look-through overlap; sector/
correlated-cluster duplication; issuer concentration; **geographic and currency exposure**; crypto
cross-correlation; **volatility and drawdown concentration across the whole portfolio, not sleeve-by-
sleeve in isolation**; liquidity; duplicated exposure across sleeves; margin/debt interaction. An
independent exact-head review of this filing's original submission found that two of those nine items —
geographic/currency exposure and whole-portfolio volatility/drawdown concentration — had no `dimension_
id` anywhere in this design, undisclosed. This section is corrected to add both as their own dimensions,
following the identical `interface_placeholder` pattern already used for `crypto_correlation_interface`/
`defensive_offset_interface` — a small, bounded, same-shape extension, not a redesign.

`XASSET-0001` §F's ninth item, liquidity, remains deliberately **not** a dimension of its own here — and
the reason is a textual distinction in §F itself, not merely "already represented elsewhere" (a rationale
an earlier version of this paragraph gave, which an independent review correctly found indistinguishable
from the reasoning that justified adding the other two dimensions below, and which this paragraph no
longer relies on). §F phrases liquidity specifically at the **per-sleeve** level — "how quickly *each
sleeve* can be converted to cash without material value loss" — a question the three existing
per-instrument liquidity axes already fully answer (the ETF framework's `liquidity` axis, the crypto
framework's `liquidity_and_market_structure` axis, and this filing's own `liquidity_character` axis,
§3.2): §F asks no *whole-portfolio rollup* question about liquidity the way it explicitly does for items
4 and 6. That is the genuine distinction from `geographic_currency_exposure` and `whole_portfolio_
volatility_drawdown_concentration` below: §F phrases item 6 explicitly at the whole-portfolio/cross-sleeve
level ("across the whole portfolio, not sleeve-by-sleeve in isolation"), and item 4 inherently so —
geographic/currency exposure spans multiple sleeves (VEA/VWO plus any future international instrument)
rather than describing any single sleeve's own character — so both genuinely lack a mechanism this design
must at least name a placeholder for, while liquidity's own §F framing never asks for one. This is a
disclosed, deliberate scoping choice grounded in §F's own text, not an assumption that liquidity is
merely "covered elsewhere."

**Every one of the ten named dimensions is preserved as its own separate record — none is merged with
another, and none is dropped.** This is a deliberate divergence from the merge-where-redundant method §2
otherwise applies, because the authorizing design direction is explicit and singular on this point:
"Preserve these as separate dimensions. NO composite overlap/risk score." Merging any two would itself be
a step toward the prohibited composite.

| Dimension (as named) | Record `dimension_id` | `dimension_type` | `source_mechanism` (extends, never duplicates) |
|---|---|---|---|
| issuer overlap / ETF look-through | `issuer_overlap_etf_lookthrough` | `mechanical_rollup` | `issuer_lookthrough.yaml`'s existing `fund_holding_weight`/8%-issuer/40%-common-driver mechanism. |
| economic-role overlap | `economic_role_overlap` | `narrative_evidence` | Company Intelligence `economic_role` (`TIER-0002`), ETF `structural_role.role_category`, crypto `network_fundamentals` (`XASSET-0002`) — cross-referenced, never re-derived. |
| correlated-loss mechanisms | `correlated_loss_mechanisms` | `narrative_evidence` | `intelligence/relationships/` (`REL-0001`–`REL-0007`'s twelve-item taxonomy) — extends the existing pairwise relationship corpus. |
| sleeve concentration | `sleeve_concentration` | `mechanical_rollup` | `targets.yaml`'s own `destination:` weights, aggregated by `asset_class` — the Level 1 sleeve breakdown `XASSET-0001` §E already names, computed (not invented) from existing config. |
| ETF/direct-equity duplication | `etf_direct_equity_duplication` | `mechanical_rollup` | The ETF framework's own `overlap_and_concentration` axis (`XASSET-0002` §3.2) — cross-referenced per-fund, not recomputed. |
| crypto-correlation interface | `crypto_correlation_interface` | `interface_placeholder` | The crypto framework's own `correlation_and_volatility.cross_coin_correlation_status` axis (`XASSET-0002` §4.3) — currently forced `not_yet_measured`; this dimension is a pass-through pointer, never a new study. |
| defensive-offset interface | `defensive_offset_interface` | `interface_placeholder` | This filing's own `GLD_DEFENSIVE_ROLE`/`capital_preservation_character` axis (§3.2) — currently unpopulated (no record exists), so this dimension has nothing to point at yet; it exists so a future populated `GLD_DEFENSIVE_ROLE` record has somewhere to be read from without a schema change at that time. |
| leverage/debt interaction | `leverage_debt_interaction` | `mechanical_rollup`, evidence sourced from a **cited, never recomputed** `margin_state.classify_margin_state()` run | `margin_state.py`'s existing four-state classifier and `DEBT_REDUCTION`'s own `hard_constraint_status` axis (§3.2) — cross-referenced, never duplicated; the overlap-model validator never imports `margin_state.py` (§7 point 12). |
| geographic/currency exposure | `geographic_currency_exposure` | `interface_placeholder` | The ETF framework's own `constituent_exposure.geographic_concentration`/`.currency_exposure` fields (`XASSET-0002` §3.2, already populated per-instrument for SPY/VEA/VWO) plus a future international/currency-denominated equity's own comparable evidence, if one is ever added — no whole-portfolio aggregation mechanism exists today to roll these per-instrument facts up across sleeves, so this dimension is a pointer to where that future aggregation would read from, never a new geography/currency study performed here. |
| whole-portfolio volatility/drawdown concentration | `whole_portfolio_volatility_drawdown_concentration` | `interface_placeholder` | The crypto framework's own `correlation_and_volatility.historical_volatility_category` axis (`XASSET-0002` §4.3, already populated per-coin) as the one currently-existing instrument-level volatility fact to point at — equities and ETFs currently carry **no** comparable volatility/drawdown axis of their own anywhere in this repository (independently confirmed: neither `TIER-0002`'s four-axis equity schema nor `XASSET-0002`'s ETF schema defines one), so a genuine whole-portfolio rollup is not yet computable even in principle until that gap is separately closed — disclosed here as a real, two-layer evidence gap (no per-instrument equity/ETF volatility axis, and no cross-sleeve aggregation mechanism), not glossed over as a simple pointer. |

### 6.2 Field-by-field design (one shared shape across all ten dimension records)

Unlike the functional-doctrine schema's four-type population, the overlap model's population is a fixed
set of exactly ten `dimension_id` values, one record each, sharing one schema shape (no per-dimension
schema variation is needed — every field below applies identically to all ten):

- **`dimension_id`**: closed vocabulary, exactly the ten values in the table above (§6.1). Population
  discriminator, not a judgment field.
- **`schema_version`**: framework schema version string, same convention as every prior framework.
- **`dimension_type`**: closed vocabulary — `mechanical_rollup` | `narrative_evidence` |
  `interface_placeholder`. States what *kind* of dimension this is (computed from files, drawn from
  narrative evidence and cross-references, or not yet computable at all) — itself a structural fact, not
  a judgment about the dimension's current value.
- **`source_mechanism`**: required citation of the specific existing repository mechanism this dimension
  extends (file path, module, or schema field — §6.1's table gives the canonical citation for each of the
  ten). A dimension record whose `source_mechanism` names a mechanism this artifact did not already
  identify in §6.1 is not authorized by this design.
- **`computation_status`**: closed vocabulary — `computed_from_existing_mechanism` |
  `not_yet_computable_interface_only` | `requires_future_authorization`. For the two `interface_
  placeholder` dimensions (`crypto_correlation_interface`, `defensive_offset_interface`), this field is
  **forced** to `not_yet_computable_interface_only` today, with no exception — the crypto framework's own
  forced `not_yet_measured` default (`XASSET-0002` §4.3) and this filing's own unpopulated
  `GLD_DEFENSIVE_ROLE` schema (§3.4) mean neither dimension has anything to compute from yet. For the
  five `mechanical_rollup`/`narrative_evidence` dimensions, a future implementation may set
  `computed_from_existing_mechanism` once it actually performs the rollup or cross-reference — **this
  design authorizes no such computation itself.**
- **`evidence_or_source_refs`**: a list of specific file/field pointers this dimension reads (e.g.,
  `issuer_lookthrough.yaml:issuers[].funds[].fund_holding_weight` for `issuer_overlap_etf_lookthrough`)
  — never a duplicated copy of the referenced values.
- **`output_shape`**: a description (schema-level, not a populated value) of what a future computed
  record for this dimension would contain — **categorical only, no numeric field, no composite score**.
  E.g., `sleeve_concentration`'s described future output shape is a per-sleeve categorical comparison
  (`within_governed_cap` | `at_or_near_governed_cap` | `exceeds_governed_cap` | `no_governed_cap_defined`)
  against whatever cap mechanism already governs that sleeve (`caps.clusters` for the equity sub-sleeves
  it already covers; no cap exists yet for the ETF/crypto/functional-doctrine sleeves as wholes) — a
  description of a future shape, not a populated value.
- **`uncertainty_or_gap_disclosure`**: required free-text sentence — for the two `interface_placeholder`
  dimensions, this is where the genuine gap ("no correlation study exists," "no `GLD_DEFENSIVE_ROLE`
  record exists yet to read from") is stated plainly, mirroring every prior framework's uncertainty-
  disclosure discipline.
- **`later_governance_action`**: same field name and purpose as the functional-doctrine schema's own
  field (§3.2) — states what future authorization this dimension's own content implies, if any (e.g.,
  `crypto_correlation_interface`'s own field would state that a future correlation study requires its own
  separate charter, matching `REL-0001` §G/§L's discipline that structural evidence and measured
  correlation stay separate governance questions).
- **`record_status`**: `draft` | `sealed`, same sealing discipline as every prior framework.

**No `abstention_index` on this schema** — unlike the four-type functional-doctrine records (which carry
several independently-abstaining axes), each overlap-model record has exactly one substantive judgment
question (`computation_status`), and its own genuine gap is already captured directly in `uncertainty_
or_gap_disclosure` — a separate rollup list would summarize a list of one, adding a field with no
information the record's own required disclosure doesn't already carry.

**No `cross_asset_handoff` sub-object on this schema** — unlike the instrument-level ETF/crypto/
functional-doctrine records (which need a normalized cross-type-comparable summary for a future synthesis
unit that reads many different instrument schemas), an overlap-model dimension record is already a
portfolio-level meta-record with one clear consumer (a future `XASSET-0001` §E/§F synthesis unit, which
would read all ten dimension records directly) — no further indirection layer is needed.

### 6.3 The no-composite-score rule, made structural

**No field, at any level of this schema, may aggregate two or more dimensions' `computation_status` or
`output_shape` values into a single number, category, rank, or score.** This is enforced two ways:

1. **Structurally**: there is no envelope object shared across the ten dimension records (unlike the
   functional-doctrine schema's shared four-type envelope) — each dimension record stands alone, with no
   natural home for a rollup field to live in even if one were later proposed. Adding a composite would
   require inventing a *new* ninth record type, not adding a field to an existing one — a materially
   higher bar than editing an existing schema, and itself a decision this filing does not authorize.
2. **By validator rule** (§7 point 7): a dedicated forbidden-key/forbidden-pattern scan for any field
   name suggesting aggregation (`composite_score`, `overall_risk`, `aggregate_concentration`,
   `overlap_index`, `risk_rank`, or any bare `score`/`rank`/`index` key not already part of this schema's
   own named fields) applied across all ten dimension records as a set, not merely within one record —
   catching a future attempt to smuggle a composite in via a ninth, ungoverned file.

## 7. Validator specification (for the future implementing PR)

A future implementation must build one combined validator module (or two closely related modules sharing
envelope-level helpers, mirroring `etf_classification_validator.py`/`crypto_classification_validator.py`'s
own sibling-module precedent) enforcing, at minimum:

1. **Exact population enforcement** — exactly four `capital_use_type` values for the functional-doctrine
   schema, exactly ten `dimension_id` values for the overlap-model schema, no more, no fewer (mirrors
   every prior population-enforcement precedent in this repository).
2. **Closed schema at every level, rejecting extra keys, not just missing ones** — envelope, per-axis,
   `structural_reference`, `economic_assessment_readiness`'s conditional two shapes, and every dimension
   record's own flat structure (the exact `contender_registry_validator.py` MAJOR-finding lesson, §8.1
   below).
3. **`capital_use_type`-conditional shape enforcement** — a `DEBT_REDUCTION` record's
   `economic_assessment_readiness` must use the two-part shape; every other type must use the
   single-part shape; the validator rejects either shape appearing on the wrong `capital_use_type`.
4. **No cross-schema field-name leakage** — a functional-doctrine record may never carry an ETF axis
   name (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_
   quality`, `liquidity`, `structure_and_methodology`), a crypto axis name (`network_fundamentals`,
   `economic_model`, `liquidity_and_market_structure`, `custody_and_counterparty_risk`, `correlation_and_
   volatility`, `regulatory_and_structural_uncertainty`), or an equity-shaped name (`economic_role`,
   `capital_priority`, `risk_concentration`); an overlap-model dimension record may never carry any
   functional-doctrine, ETF, crypto, or equity axis name either — a dedicated forbidden-key scan applied
   at every schema level, not just the top.
5. **`hard_constraint_status`/`economic_assessment_readiness` structural independence** — a dedicated
   check confirming these two fields are validated by fully separate code paths, with no shared helper
   function that reads both, and a dedicated test (§8) mutating one field's value and confirming the
   other's own validation result is entirely unaffected — the mechanical enforcement of §3.2's/§3.3's
   design requirement, not merely a documentation claim.
6. **No numeric score/rank/target/avoided-cost leakage anywhere** — a forbidden-key scan for `target_pct`,
   `target_range`, `max_position_size`, `score`, `rank`, `conviction_score`, `avoided_interest`,
   `avoided_cost`, `expected_return`, `basis_points_saved`, or any bare numeric-percent-shaped token
   anywhere in either schema's document tree — **with no carve-out of any kind** (unlike the ETF
   framework's own scoped `expense_ratio_pct` exception, §3.3/§7's own zero-numeric-field design means
   this scan has nothing to exempt).
7. **No composite-overlap-score leakage** — the dedicated forbidden-pattern scan described in §6.3 point
   2, applied across the full set of ten dimension records together, not merely within one.
8. **`GLD_DEFENSIVE_ROLE` structural-reference enforcement** — §3.4's full mechanism: required-and-only-
   present-on-`GLD_DEFENSIVE_ROLE` shape check; a live recompute of GLD's ETF record hash via
   `etf_classification_validator.canonical_record_hash()` (read-only reuse of the existing public
   function — no new hashing scheme) reconciled against `referenced_content_sha256`; the ETF-axis-name
   forbidden-key scan restated as its own dedicated check (not merely folded into point 4's general
   scan, given how safety-critical this specific boundary is).
9. **No chart evidence leakage** — an independent, free-text scan for chart-domain terminology (the same
   term list `recommendation_validator.py`/`etf_classification_validator.py`/`crypto_classification_
   validator.py` already use), built in from the start.
10. **No directive/trading-language leakage** — a word-boundary-matched scan for the same eight directive
    words (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`) plus, for the functional-doctrine
    schema specifically, `repay`/`redeploy`/`fund`/`draw` (debt/cash-specific directive verbs the equity/
    ETF/crypto schemas never needed to guard against) — word-boundary matched so it does not false-
    positive on "holdings," a section title, or the noun "fund" inside `source_mechanism`/`source_file`
    citation strings.
11. **Evidence/provenance validation** — every `provenance.sources` entry (functional-doctrine schema
    only — the overlap-model schema's `evidence_or_source_refs` is a structural pointer list, not a
    provenance-with-access-status object, since it points at other repository files, not external
    sources) must carry a type and access-status field, mirroring the equity/ETF/crypto pipeline's own
    discipline.
12. **Allocator/margin decoupling** — zero import coupling with `allocate.py`/`margin_state.py` in either
    direction, matching every prior Intelligence-adjacent validator in this repository. A functional-
    doctrine or overlap-model record may **cite** `margin_state.py`'s output in prose/provenance; the
    **validator module** never imports it.
13. **Deterministic generation** — repeated validator runs against the same input produce byte-identical
    results.
14. **Protected-path isolation** — a future implementation's own test suite must assert zero diff on
    `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_
    state.py`, `levels.py`, every existing `intelligence/classification|companies|themes|relationships|
    etf_classification|crypto_classification/` record, `COHORT_MANIFEST.yaml`, and every existing
    governance decision file.

## 8. Test specification (for the future implementing PR)

A future implementation's focused test suite must cover, at minimum, one test per item below:

- Functional-doctrine happy-path record for each of the four `capital_use_type` values (all axes
  present, valid, no abstention where not required) validates clean.
- Overlap-model happy-path record for each of the ten `dimension_id` values validates clean.
- Malformed envelope/axis schema (missing required field) rejected, for both schemas.
- Extra unknown key at envelope level and at axis level rejected, for both schemas (the
  `contender_registry_validator.py` MAJOR-finding exploit class — proactively tested here).
- Wrong `capital_use_type`/`dimension_id` value (outside the closed four/ten) rejected.
- `economic_assessment_readiness` single-part shape on a `DEBT_REDUCTION` record rejected; two-part shape
  on any non-`DEBT_REDUCTION` record rejected.
- `structural_reference` present on a non-`GLD_DEFENSIVE_ROLE` record rejected; missing on a
  `GLD_DEFENSIVE_ROLE` record rejected.
- `structural_reference.referenced_content_sha256` mismatched against a live recompute of GLD's ETF
  record hash rejected (a synthetic stale-hash test, and a live test against the real sealed
  `intelligence/etf_classification/GLD.yaml`).
- Any of the six ETF axis key names present anywhere inside a `GLD_DEFENSIVE_ROLE` record rejected
  (individually, one test per key name).
- `hard_constraint_status`/`economic_assessment_readiness` independence: a test that mutates
  `hard_constraint_status.binding` and confirms `economic_assessment_readiness`'s own validation result
  is byte-identical before and after, and vice versa.
- Forbidden numeric/score/avoided-cost key leakage (each named term in §7 point 6, individually) rejected
  — with **no** positive/accepted-numeric-field test (unlike the ETF framework's `expense_ratio_pct`
  acceptance test), since this design carries zero numeric-field exceptions.
- Forbidden composite-overlap-score pattern (each named term in §6.3 point 2, individually) rejected,
  tested against the full ten-record set together, not a single record in isolation.
- Cross-schema field-name leakage: an ETF-, crypto-, or equity-shaped key present anywhere in either the
  functional-doctrine or overlap-model schema rejected (each source schema's key names tested
  individually).
- Abstention behavior: `unable_to_determine` without `abstention_reason` rejected; `not_applicable` used
  on an axis that doesn't support it rejected (per §3.2's per-axis abstention table); a fully-populated
  abstention accepted.
- Duplicate `capital_use_type`/`dimension_id` entry within a population batch rejected; missing entry
  from the named population rejected; extra entry beyond the named population rejected.
- Chart-terminology leakage (each term individually) rejected, for both schemas.
- Directive/trading-language leakage (each of the twelve words — the shared eight plus the four
  debt/cash-specific verbs, §7 point 10) rejected individually, including a false-positive-guard test
  proving ordinary use of "fund"/"funded" inside a citation string is not flagged.
- `economic_assessment_readiness`'s forced `assessment_required` value: any other value, on either shape,
  rejected.
- Envelope-level field failing to match its source axis field (§4's read-only-projection rule) rejected —
  e.g., `hard_constraint_signal` on the envelope not matching `hard_constraint_status.binding`/
  `.constraint_source` on the axis.
- `overlap_model` `computation_status` forced-value violation: `crypto_correlation_interface` or
  `defensive_offset_interface` carrying any value other than `not_yet_computable_interface_only`
  rejected.
- Deterministic output: two consecutive validator runs against identical input produce byte-identical
  results.
- Protected-path isolation: a dedicated test asserting zero diff on every path named in §7 point 14,
  before and after a synthetic record-validation run.
- Allocator/margin import-coupling test: a static-analysis-style check confirming the future validator
  module imports neither `allocate.py` nor `margin_state.py`.

### 8.1 Lessons explicitly carried forward from prior validator review history

This design deliberately pre-empts four specific defect classes this repository has already found, in
its own review history, in adjacent validators — named here so a future implementation does not
rediscover them the expensive way:

- **Closed-schema checks must reject extra keys, not just missing ones** —
  `contender_registry_validator.py`'s own independent review found a real MAJOR gap where the schema
  check computed only the `missing` side, silently accepting smuggled extra keys. §7 point 2 and the
  test list above build the extra-key check in from the start.
- **An independent second-stage check must use a materially different mechanism than the logic it
  verifies, not merely call the same function twice** — `TIER-0004`'s own correction history ("no
  independent backstop for dangling section-title cross-references"). §7 points 7/8's forbidden-pattern
  and structural-reference-hash checks should be implemented as free-text/structural scans and a live
  hash recompute independent of whatever per-field acceptance logic a future generator uses.
- **A required envelope field needs its own independent presence/type check, not just a schema-shape
  check** — `etf_classification_validator.py`'s own disclosed MINOR-1 finding (`structural_risk_flags`
  had no independent presence/type check, masked because the field happened to be part of the canonical
  hash for the four real records). §7's every point applies equally to `structural_reference` and
  `hard_constraint_status`, not only to the axes that happen to be exercised by the first real records a
  future implementation drafts.
- **A self-declared boolean/status flag is not a substitute for an independent scan** — `reconciliation_
  validator.py`'s own disclosed MINOR finding (a self-declared `chart_evidence_used: false` flag, checked
  without an independent free-text scan). §7 points 9/10 require the independent scan from the start, not
  a flag-only check — directly relevant here because `hard_constraint_status.binding: false` and
  `economic_assessment_readiness.status: assessment_required` are exactly the kind of self-declared flags
  this lesson warns against trusting without a backing scan.

## 9. Objective preserved, not invented

This design does not define, redefine, or narrow Portfolio-HQ's governing objective, restated by
`XASSET-0001` §A and unedited here: *maximize long-term portfolio compounding and capital appreciation
within approved risk, liquidity, concentration, leverage, and survival constraints.* Neither the
functional-doctrine schema nor the overlap-model schema computes an "expected return," an "avoided cost,"
or an "overlap risk score" — both supply the categorical, evidence-based facts a future valuation/
economic-assessment step (§5 step 2) and a future cross-asset opportunity-cost synthesis (§5 step 3)
would need, without themselves performing either. **The "next-dollar opportunity-cost methodology"
`XASSET-0001` §E/§A implies remains wholly undesigned by this artifact** — exactly as `XASSET-0002` §11
already stated for the ETF/crypto frameworks, restated here for the same reason: this is a required
future principal/governance decision, not a byproduct of a design filing.
