---
decision_id: XASSET-0005
date: 2026-08-08
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0004, TIER-0005, TIER-0007, TIER-0009, REL-0001, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004]
supporting_artifact: governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_ARCHITECTURE_DESIGN_20260808.md
file: governance/decisions/XASSET-0005-functional-doctrine-and-overlap-concentration-architecture.md
---

## Context

### Authority for this unit

`XASSET-0001` §J names, as one batchable architecture step, "cash/GLD/debt doctrine + overlap-model
**architecture** (steps 6–7) — permitted to batch only where no asset-specific judgment occurs (i.e.,
defining the doctrine's shape and the overlap model's shape, not applying either to a specific
instrument or sleeve)." `XASSET-0001` §D independently states that cash/reserve, GLD, and debt
reduction "require governed functional doctrine as competing uses of capital, not classification... a
future, separately authorized decision must define the criteria... This filing does not itself define
that doctrine; it records that it is required and assigns its future authorship to `WS-0014`." §F makes
the parallel statement for overlap/concentration/risk accounting: "This filing does not implement any
of these models. It records them as required future work, assigned to `WS-0014`." This filing is that
future, separately authorized design unit for both steps 6 and 7 together — the same batching `XASSET-0002`
already used for ETF+crypto framework design, one level further down `WS-0014`'s roadmap. It designs; it
does not populate any doctrine content or compute any overlap figure.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0005-doctrine-overlap-l1dd71`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local branch `HEAD` and `origin/main` both confirmed
  identical at `e5446cd5c4bfce744691fd1914ec8ef098286839` — the `XASSET-0004`-authorized crypto
  classification implementation's own merge commit (PR #272).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #272`'s full lifecycle independently re-verified via the GitHub API, not assumed** (folded into
  §I below as a Lane M synchronization): implementation-summary body at head
  `6eee128ce85bdea63a3fd65f843835f42a243f0d`; first independent exact-head review
  (`pullrequestreview-4887530037`, CHANGES REQUIRED — 0 BLOCKING / 0 MAJOR / 2 MINOR / 2 non-actionable
  NOTE); bounded correction (`issuecomment-5223594454`, corrected head
  `d65cc0148ed197953e7db4e6056d7e5d56681259`, resolving both MINOR findings — an audit workstream-count
  correction and nine new `validate_cohort_manifest` negative-path tests); corrected-head delta review
  (`pullrequestreview-4887618331`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR
  / 0 MINOR / 2 non-actionable NOTE carried forward); principal acceptance (`issuecomment-5223695674`,
  accepted head `d65cc0148ed197953e7db4e6056d7e5d56681259`); merge (merge commit
  `e5446cd5c4bfce744691fd1914ec8ef098286839`, parents `7b9af50af001ed0db5933a6d65b18b19f9952ffc` and
  `d65cc0148ed197953e7db4e6056d7e5d56681259` — both independently re-confirmed via `git show -s
  --format='%H %P'`); merge-commit CI independently re-fetched — workflow run `31231452840`, job
  `93035960909`, `status: completed`/`conclusion: success`, `head_sha` matching exactly. `intelligence/
  crypto_classification/{BTC,ETH,SOL}.yaml` and `COHORT_MANIFEST.yaml` confirmed present, sealed, in the
  current working tree.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`. Ten milestone gates recorded
  through `xasset0004-crypto-classification-implementation` (`status: in_progress`, `pr: 272`) — stale
  as of this session's start, since PR #272 is, in fact, fully merged (see above); this filing
  synchronizes it (§I). `blocker` correctly names step 5 (crypto classification content) as the item
  awaiting review/merge — also now stale for the same reason.
- **`WS-0005`'s final state independently re-confirmed**: `status: complete`, `priority: secondary`.
  Zero `priority: primary` workstreams currently exist in the repository, confirmed by a direct grep of
  every `priority:` field in `operations/WORKSTREAMS.yaml`.
- **`XASSET-0001` (in full), `XASSET-0002` (decision file plus supporting artifact, §§3–10), `XASSET-0003`,
  and `XASSET-0004` read directly**, not summarized from memory — the sealed ETF (`intelligence/
  etf_classification/{SPY,VEA,VWO,GLD}.yaml`) and crypto (`intelligence/crypto_classification/
  {BTC,ETH,SOL}.yaml`) records, `etf_classification_validator.py`, and `crypto_classification_validator.py`
  were each opened directly to confirm the exact envelope field names (`instrument_id`, `asset_type`,
  `schema_version`, `provenance`, `evidence_quality_status`, `uncertainty_summary`,
  `structural_risk_flags`, `record_status`, `valuation_and_economic_assessment_readiness`,
  `cross_asset_handoff`, `abstention_index`) and the `canonical_record_hash(data: dict) -> str` function
  each validator module already exposes (`etf_classification_validator.py:322`,
  `crypto_classification_validator.py:347`) — load-bearing for §5's GLD reference-hash design below.
- **`targets.yaml` independently re-read**: `RESERVE` (`target_pct: 4.00, asset_class: reserve`), `CASH`
  (`target_pct: 1.00, asset_class: cash`), and `GLD` (`target_pct: 4.00, asset_class: fund`) confirmed at
  their current lines; the file's own header comment confirms `RESERVE`/`CASH` rows are "never buy
  candidates — their target weight is definitionally satisfied by the account's own cash balance," a
  mechanical-allocator-level identity this filing does not alter.
- **`issuer_lookthrough.yaml` independently re-read**: `funds:` entries across every issuer row name only
  `SPY`, `VEA`, `VWO` — confirming, as `XASSET-0002` §5 already established, that GLD has no
  constituent-look-through mechanism to duplicate or extend.
- **`margin_state.py` independently read in full** (`classify_margin_state()`, `MarginStateResult`,
  `concentration_risk_score()`): a pure, already-existing risk-classification calculator — computes
  `leverage_ratio`, `utilization`, a four-state classification (`NORMAL`/`CAUTION`/`RESTRICTED`/
  `FORCED_DELEVER`), and a closed `ALLOWED_ACTIONS` set containing no leverage-increasing action by
  construction. This filing's debt-reduction functional-doctrine design (§3.5, supporting artifact) and
  the overlap model's leverage/debt-interaction dimension (§4, supporting artifact) are designed to
  **cite this module's existing output as evidence**, never to recompute, duplicate, or extend its logic
  — no future implementation under this design may import `margin_state.py` from a validator module.
- **Decision catalog independently rebuilt**: **93 decisions, `issues == ()`** at the starting head, 93
  non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0005` confirmed unused: zero
  matches in `governance/decisions.yaml`, zero matches via full-repository grep;
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new decision
  domain needs one") is satisfied by continuing the existing `XASSET-####` series — this filing is the
  direct continuation of `XASSET-0001` §J steps 6–7, not a genuinely new decision domain, mirroring
  `XASSET-0002`'s identical continuation of step 3.

### Stale `WS-0014` step-5 register state — independently verified, synchronized here (Lane M)

The preflight found `operations/WORKSTREAMS.yaml`'s `xasset0004-crypto-classification-implementation`
gate reading `status: in_progress`, `pr: 272`, and the workstream's own `blocker`/`next_action` fields
describing that PR as still awaiting review — but PR #272 is, in fact, fully merged, reviewed, corrected,
and principal-accepted (see the preflight bullet above for the complete, independently re-verified
chain). **Governing basis for including this synchronization in this filing** (rather than deferring it
to its own follow-up unit): the exact `OPS-0009` Lane M pattern this repository has applied on every
directly comparable occasion — `XASSET-0002` folded in `CONTENDER-0002`'s stale gate; `XASSET-0003`
folded in `XASSET-0002`'s; `XASSET-0004` folded in `XASSET-0003`'s implementation gate. The pattern is:
**leave the original gate's own historical text unedited** (it was accurate as filed) and **add one new,
additive, separately-named gate** recording the confirmed post-merge state — never a direct edit of the
stale `status` field in place. §I performs exactly that addition.

### Correction history (this filing, same PR)

**Bounded correction, independent exact-head review of head `6b726de3fd2da7ff83f103d109db4166a70981e3`,
one finding, 0 BLOCKING / 1 MAJOR / 0 MINOR / 1 non-actionable NOTE:** the review independently re-read
`XASSET-0001` §F in full and found it enumerates **nine** "at minimum" required overlap/concentration/
risk items, not the eight this filing's original submission addressed — geographic/currency exposure and
whole-portfolio volatility/drawdown concentration had no `dimension_id` anywhere in the original design,
undisclosed. **Resolved** by adding two new dimensions, `geographic_currency_exposure` and
`whole_portfolio_volatility_drawdown_concentration` (supporting artifact §6.1, §0), both following the
identical `interface_placeholder` pattern already used for `crypto_correlation_interface`/`defensive_
offset_interface` — the population grows from eight to ten dimensions, with §F's ninth item (liquidity)
explicitly addressed as a disclosed, deliberate non-dimension (already represented per-instrument in the
ETF/crypto/functional-doctrine schemas, with no existing whole-portfolio rollup mechanism to extend)
rather than left to read as an unexplained gap. Every "eight"/"eight-dimension" reference throughout this
decision file and the supporting artifact is corrected to "ten." No functional-doctrine content, no
`structural_reference`/hash mechanism, no `hard_constraint_status`/`economic_assessment_readiness`
separation, and no validator/test lesson-carrying content changed by this correction — it is scoped
entirely to the overlap-model dimension table and the population-count references it drives downstream.
The review's own non-actionable NOTE (whether "eight, specifically" traced to a concrete principal
enumeration or this session's own synthesis of §F) is carried forward unresolved and non-actionable, per
the review's own characterization — the corrected population of ten is derived directly from `XASSET-0001`
§F's own controlling text, which supersedes the original eight-item authorizing-prompt list as the source
of population size. Full correction narrative in the supporting artifact §0.

**Second bounded correction, independent exact-head delta review of head
`a8020e1ae097e6ea31ce8e86a673c8af948aae40`, two findings, 0 BLOCKING / 0 MAJOR / 2 MINOR / 1
non-actionable NOTE carried forward:** confirmed the first correction's MAJOR genuinely resolved and every
other boundary (functional-doctrine schema, `hard_constraint_status`/`economic_assessment_readiness`
separation, GLD hash mechanism, `DEBT_REDUCTION` split, no-composite-score rule, protected-path isolation)
untouched and intact, but found two narrow textual defects. **MINOR-1, resolved**: this decision file's
own "Why the overlap-model dimensions stay ten separate records" paragraph — heading already corrected —
still read "**Eight** independently evidenced, independently abstaining records..." two lines below, a
same-paragraph contradiction; the exact stale-reference defect class the first correction was meant to
eliminate, one instance short of complete. Fixed: "Eight" → "Ten." **MINOR-2, resolved**: §6.1's (and this
file's mirrored) liquidity-exclusion rationale argued "already represented per-instrument, no aggregation
mechanism, inventing one would be asset-specific-judgment" — the review correctly found this
indistinguishable from the reasoning that justified adding the other two dimensions (both also lack an
aggregation mechanism, and were resolved by adding a placeholder, not by treating the absence as a reason
to add nothing). Replaced with the review's own suggested, textually-grounded distinction: `XASSET-0001`
§F phrases liquidity at the **per-sleeve** level, already answered by three existing per-instrument
liquidity axes, while items 4 and 6 are phrased at the **whole-portfolio/cross-sleeve** level — a
distinction in kind, not degree. Neither fix touches functional-doctrine content, the GLD mechanism, or
the validator/test specification. The original NOTE is carried forward unchanged, per the review's own
explicit confirmation that it was neither worsened nor resolved. Full correction narrative in the
supporting artifact §0.

## Decision

This filing does three things, in one bounded PR:

1. **Reconfirms (Lane M) that `XASSET-0004`'s own authorized implementation PR (#272) is fully merged,
   reviewed, corrected, principal-accepted, and post-merge verified**, and synchronizes `operations/
   WORKSTREAMS.yaml` accordingly via one additive gate entry — no edit to the original gate's own
   historical text (§I).

2. **Designs, as text only — not an authorization, not an adoption, not applied to any real cash
   balance, reserve level, GLD holding, or margin-debt figure — a functional-doctrine architecture for
   exactly four capital-use types**: `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, and `DEBT_REDUCTION`.
   **CASH and RESERVE share one doctrine schema**, distinguished by an explicit `capital_use_type` field
   rather than duplicated field sets — their two `targets.yaml` rows are already mechanically identical
   at the allocator level ("never a buy candidate, definitionally satisfied"), so the schema's
   contribution is exactly the functional-role distinction the allocator does not need and does not
   carry. `GLD_DEFENSIVE_ROLE` and `DEBT_REDUCTION` use the same shared schema shape, with two narrow,
   explicitly-scoped structural extensions: `GLD_DEFENSIVE_ROLE` carries a mandatory `structural_reference`
   sub-object that pins, by content hash, to GLD's already-sealed ETF structural record
   (`intelligence/etf_classification/GLD.yaml`) — consumed by reference only, never duplicated or
   re-derived — and `DEBT_REDUCTION` carries a two-part `economic_assessment_readiness` shape
   (`avoided_borrowing_cost_readiness` and `survivability_and_buffer_benefit_readiness`, independently
   forced, never blended into one figure), where the other three types carry a single-part shape.
   **`hard_constraint_status` is a structurally independent axis and envelope projection on every
   record, mechanically separated from `economic_assessment_readiness`** — a survival/reserve-floor
   requirement can never be converted into, derived from, or overridden by an economic-comparison figure.
   Full field-by-field detail, closed vocabularies, abstention discipline, and the GLD/debt boundary
   mechanics in the supporting artifact §§2–5.

3. **Designs, as text only, a cross-asset overlap and concentration-model architecture** — ten
   separately-preserved dimensions (issuer overlap/ETF look-through, economic-role overlap,
   correlated-loss mechanisms, sleeve concentration, ETF/direct-equity duplication, a crypto-correlation
   interface placeholder, a defensive-offset interface, leverage/debt interaction, a geographic/currency-
   exposure interface placeholder, and a whole-portfolio volatility/drawdown-concentration interface
   placeholder — the latter two added by this filing's own bounded correction, §0 of the supporting
   artifact, to fully represent `XASSET-0001` §F's nine "at minimum" required items, not merely the eight
   originally addressed), **each its own record with its own evidence source and computation status — no
   composite overlap or risk score anywhere, at any level.** Every dimension either extends an
   already-existing repository mechanism (`issuer_lookthrough.yaml`, `targets.yaml`'s `caps.clusters`,
   `intelligence/relationships/`, `targets.yaml`'s own `destination:` weights, the crypto framework's own
   `correlation_and_volatility` axis, the ETF framework's own `constituent_exposure` axis, this filing's
   own `GLD_DEFENSIVE_ROLE` interface, `margin_state.py`'s existing classification output) or is
   explicitly marked `not_yet_computable_interface_only` where no such mechanism exists yet (crypto
   cross-correlation, defensive-offset, geographic/currency-exposure aggregation, whole-portfolio
   volatility/drawdown aggregation) — never a new measurement invented by this design. §F's ninth item,
   liquidity, is deliberately not a dimension of its own — §F phrases it at the per-sleeve level ("how
   quickly each sleeve can be converted to cash"), a question the three existing per-instrument liquidity
   axes already answer, unlike items 4 and 6, which §F phrases at the whole-portfolio/cross-sleeve level
   and which therefore do need a placeholder. A disclosed scoping choice grounded in §F's own text, not a
   silent omission. Full field-by-field detail in the supporting artifact §6.

Both the functional-doctrine schema and the overlap-model schema carry **zero numeric fields of any
kind** — stricter than the ETF framework's one disclosed-fact carve-out (`expense_ratio_pct`), matching
the crypto framework's zero-numeric-field posture instead, because a "readiness" schema for debt
reduction sits close enough to an implicit avoided-interest calculation that this design deliberately
forecloses the appearance rather than draw a narrow exception (supporting artifact §3.5, §7).

This filing also specifies, for a later, separate implementing PR: a combined validator specification
(fourteen requirements — supporting artifact §7) and a focused test inventory (supporting artifact §8),
both drawing explicit lessons from this repository's own prior validator-review history (closed-schema
extra-key gaps, independent-mechanism verification, self-declared-flag-without-independent-scan gaps,
and the newer lesson `XASSET-0002`'s own implementation history surfaced — a required envelope field
needs its own independent presence/type check, not just a schema-shape check — §8.1) so a future
implementation does not rediscover any of them the expensive way.

This decision explicitly does **not**: populate any `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, or
`DEBT_REDUCTION` functional-doctrine record (no capital-use type is assigned a value on any axis by this
filing); compute any overlap, concentration, or correlation figure for any of the ten dimensions;
determine GLD's actual portfolio role (ballast, beta, or otherwise); calculate or state any
avoided-borrowing-cost number; modify `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, or `levels.py`; reopen, weaken, or restate
the 1.8x leverage cap or 30% margin-buffer floor (both remain exactly as `CLAUDE.md`'s Portfolio Doctrine
already states them, untouched); or authorize any of `WS-0014`'s remaining, later work (§I of
`XASSET-0001`, items 9–14 beyond what this filing itself performs).

## Rationale

**Why one filing for both steps.** `XASSET-0001` §J states plainly that steps 6–7 "may reasonably batch
as one architecture unit" precisely because both are shape-defining exercises with no asset-specific
judgment — the functional-doctrine schema defines what a future `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`/
`DEBT_REDUCTION` record would look like without saying what any of them currently is, and the
overlap-model schema defines what a future dimension record would look like without computing any
dimension's current value. Filing them separately would duplicate the shared abstention/evidence-quality
discipline and the validator/test specification across two documents for no review benefit — the same
economy-of-filing reasoning `XASSET-0002` already applied to its own ETF-plus-crypto batching.

**Why CASH and RESERVE share a schema rather than each getting its own.** The two `targets.yaml` rows
are already mechanically identical at the allocator level (`asset_class: reserve`/`asset_class: cash`,
both "never a buy candidate, definitionally satisfied" per the file's own header comment) — inventing two
separate schemas for two instruments the allocator itself treats identically would misrepresent the one
place they actually differ (their intended functional purpose within the portfolio, which the allocator
does not need to know and does not encode) as though it were a structural difference in kind, when it is
a difference in role only. A shared schema with an explicit `capital_use_type` discriminator states that
precisely.

**Why `GLD_DEFENSIVE_ROLE` is a separate record type from GLD's own ETF structural classification, never
a duplicate of it.** `XASSET-0002` §5 already resolved, from existing authority, that GLD receives both
(A) structural fund-mechanics treatment under the ETF framework and (B) a fully separate, future,
functional defensive-asset-role determination — and stated explicitly that neither this design nor any
future ETF classification built from it may assign GLD's role. This filing is the design of that
separate (B) track, and its own §3.4 (supporting artifact) enforces the boundary mechanically: a
`structural_reference` pin by content hash, and a forbidden-key scan barring every one of the ETF
schema's own axis names from ever appearing inside a `GLD_DEFENSIVE_ROLE` record.

**Why `hard_constraint_status` is structurally, not merely documentarily, separated from
`economic_assessment_readiness`.** The authorizing design direction requires this explicitly: "Reserve/
survival requirements cannot be converted into or overridden by a return figure." A comment or a
convention is not a boundary a future implementation session can be trusted to preserve under drift —
this design makes the separation mechanical: two independent top-level axes, two independent envelope
projections, and a validator requirement (§7 point 5, supporting artifact) that the two fields are
computed, validated, and tested by fully separate code paths with no cross-derivation of either from the
other. This mirrors the same discipline `TIER-0002` established between `risk_concentration` (computed)
and `economic_role`/`capital_priority` (narrative judgment) for the equity schema, and that `XASSET-0002`
carried forward into `overlap_and_concentration`/`correlation_and_volatility` for ETFs and crypto — this
filing is the third application of the identical principle, not a new one.

**Why the debt-reduction economic-assessment split is a schema-shape difference, not a fourth axis.**
The authorizing design direction requires avoided-borrowing-cost readiness exposed **separately** from
survivability/leverage-buffer benefit, "not blend[ed] into one score or return." Rather than invent two
new top-level axes (which would break the shared four-type schema's own symmetry for no benefit — the
other three types have no analogous split), this design keeps `economic_assessment_readiness` as the one
shared axis name across all four types and varies its **internal shape** by `capital_use_type`: a
single-part `{status, rationale}` object for `CASH`/`RESERVE`/`GLD_DEFENSIVE_ROLE`, a two-part object
(`avoided_borrowing_cost_readiness`/`survivability_and_buffer_benefit_readiness`, each independently
`{status, rationale}`) for `DEBT_REDUCTION` only. This is the same "closed schema variation keyed by a
discriminator field" pattern the crypto framework already uses (`consensus_mechanism: other_consensus`
requiring a conditional `consensus_basis` sub-field) — not a novel mechanism.

**Why the overlap-model dimensions stay ten separate records, never one aggregate.** The authorizing
design direction is explicit: "Preserve these as separate dimensions. NO composite overlap/risk score."
A composite score would itself be exactly the kind of "hidden scoring" `TIER-0009`, `recommendation_
validator.py`, and every classification framework in this repository since `TIER-0002` has been built to
prohibit — and would silently pre-empt the cross-asset opportunity-cost synthesis `XASSET-0001` §E
reserves to its own separate, later, undesigned unit. Ten independently evidenced, independently
abstaining records give a future synthesis unit exactly the raw material it needs without this design
performing any part of that synthesis itself.

**Why the functional-doctrine and overlap schemas carry zero numeric fields, stricter than the ETF
framework's own `expense_ratio_pct` carve-out.** `XASSET-0002` permitted exactly one numeric field
because a fund's expense ratio is a real, disclosed, already-governed financial fact with no
decision-value gap a categorical field could fill instead. No comparable case exists here: `CLAUDE.md`'s
own Portfolio Doctrine already discloses the account's margin-interest rate (~5% APR) in prose: this
schema restating it as a structured numeric field would sit close enough to an implicit avoided-cost
calculation — exactly what the authorizing design direction prohibits — that this design forecloses the
appearance rather than attempt a narrow, defensible exception. The crypto framework already established
that a framework may legitimately choose zero numeric fields when no clean carve-out exists; this design
makes the same choice for the same reason.

**Why `GLD_DEFENSIVE_ROLE`'s reference pin reuses `etf_classification_validator.canonical_record_hash()`
rather than defining a new hashing scheme.** `PI-0011`'s own precedent — "reusing `intelligence_validator.py`'s
public API only, not a second validator" — already establishes that a read-only cross-reference into an
existing validator's public function is the correct pattern when one schema needs to verify another's
sealed content without duplicating its hashing logic. `etf_classification_validator.py` already exposes
exactly the function needed; inventing a second, parallel hash implementation would create two sources of
truth for what "the current GLD record" hashes to.

## Alternatives Considered

**Design the functional-doctrine architecture and the overlap-model architecture as two separate
filings.** Rejected — `XASSET-0001` §J explicitly authorizes batching both steps' design, and the
two share enough method (asset-appropriate schema design, judgment-versus-computation separation,
per-field abstention discipline) that one filing avoids duplicating the shared discipline and the
validator/test specification across two documents, without violating the rule against combining design
with content, which this filing does not do for either step.

**Give `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, and `DEBT_REDUCTION` each their own independent schema.**
Rejected — the authorizing design direction explicitly requests a shared schema for `CASH`/`RESERVE`
with an explicit type distinction, and extending that same shared shape to `GLD_DEFENSIVE_ROLE`/
`DEBT_REDUCTION` (with two narrow, explicitly-scoped extensions rather than four wholly separate field
sets) keeps the validator specification, the abstention discipline, and the envelope/handoff design in
one place — mirroring how `XASSET-0002` gave ETFs and crypto genuinely separate schemas only where the
underlying evidence types were genuinely different in kind, not merely different in degree, which is not
the case among these four capital-use types.

**Fold `GLD_DEFENSIVE_ROLE`'s structural facts (expense ratio, replication method) directly into the
functional-doctrine record, rather than referencing GLD's sealed ETF record by hash.** Rejected outright
— this is exactly the duplication `XASSET-0002` §5 and the authorizing design direction both prohibit
("Do not duplicate or re-derive its seven structural fields"). A content-hash reference is the
established repository pattern (`REL-0001`'s pairwise relationship records reference, never restate,
Company Intelligence content) for exactly this situation.

**Permit `DEBT_REDUCTION`'s `avoided_borrowing_cost_readiness` to carry the account's current disclosed
margin-interest rate as a real, inherited fact, mirroring the ETF framework's `expense_ratio_pct`
carve-out.** Rejected — see Rationale above; the debt-reduction context makes even a disclosed,
non-computed rate figure sit too close to the prohibited avoided-cost calculation, and `CLAUDE.md`'s
Portfolio Doctrine already carries that fact in prose with no decision-value gap this schema needs to
fill.

**Give the overlap model a single composite record with one sub-field per dimension, rather than fully
independent records.** Rejected — a single record with one sub-field per dimension under one
`record_status`/`schema_version` envelope would create exactly one natural place to add a further field
that aggregates the others into a score, the precise failure mode the authorizing design direction
prohibits. Ten genuinely independent records, each separately sealed and separately abstaining, is a
structurally stronger guarantee against that drift than a single record with an internal convention
against aggregation.

**Design the functional-doctrine and overlap-model validators' full code as part of this filing, rather
than a specification for a future implementing PR.** Rejected, matching `TIER-0002`'s and `XASSET-0002`'s
own explicit precedent — a working validator applied against real evidence, or even built and tested
against synthetic data alone, is itself the beginning of implementation work requiring its own dedicated
authorization, not a byproduct of a filing whose stated purpose is establishing that these schemas are
needed.

## Consequences

**Changes as a direct result of this decision**: the existence of one retained, structural
functional-doctrine framework design (four capital-use types sharing one schema, two narrow
type-specific extensions), one retained overlap/concentration-model design (ten independently
preserved dimensions, no composite score), one combined validator specification, and one combined test
specification — all recorded in the supporting artifact for a future, separately authorized implementing
PR to draw on; five rejected alternatives recorded for the same future reference; confirmation, via one
additive `operations/WORKSTREAMS.yaml` gate entry, that `XASSET-0004`'s own authorized implementation PR
(#272) is fully merged, reviewed, corrected, accepted, and post-merge verified.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin behavior;
the 1.8x leverage cap or 30% margin-buffer floor; any Company, Theme, relationship, sealed classification,
sealed ETF, or sealed crypto record's content; any current cash balance, reserve level, GLD holding, or
margin-debt figure; `WS-0005`'s completed, `status: complete` state; `WS-0014`'s own `status: proposed`/
`priority: secondary` (this filing adds two design gates, it does not begin execution or change the
workstream's own status/priority); or any brokerage, trading, or order-related capability. Completing
this unit does not itself authorize populating any `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`, or
`DEBT_REDUCTION` functional-doctrine record, computing any of the ten overlap/concentration
dimensions, cross-asset synthesis (`WS-0014` item 10), sleeve- or instrument-level targets (items
11–12), chart-informed deployment (item 13), or the final independent audit (item 14) — each requires
its own separate, explicit, future principal authorization, per `XASSET-0001` §J's own dependency-ordered
roadmap and `OPS-0006` §16.4's standing rule that the register never originates authority.
