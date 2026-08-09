# WS-0014 GLD/CASH/RESERVE Economic Assessment Methodology — retained design artifact

**Filed under**: `XASSET-0008` (`governance/decisions/XASSET-0008-gld-cash-reserve-economic-assessment-methodology.md`)
**Date**: 2026-08-09
**Scope**: `XASSET-0005` §5 step 2's own restated seven-step sequence ("perform asset-appropriate
valuation/economic assessment — future, separate, undesigned") — restricted to exactly three capital-use
types: `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`. Design only. No record is populated, no economic finding
is stated for any capital-use type, and no `economic_assessment_readiness` value on any sealed
functional-doctrine record is superseded by this artifact.

This artifact is the full field-by-field methodology design. The decision file summarizes it and carries
the authorization/consequences text; this document is the retained detail, matching the
`TIER-0001`→`TIER-0002` and `XASSET-0001`→`XASSET-0005` supporting-artifact precedent.

---

## 0. What gap this design closes, precisely

Every sealed functional-doctrine record (`CASH.yaml`, `RESERVE.yaml`, `GLD_DEFENSIVE_ROLE.yaml`) carries
the identical forced value on `economic_assessment_readiness.status`:

> `assessment_required` — "No governed methodology exists anywhere in this repository to compare
> [this capital-use type]'s opportunity cost against another capital-use type, sleeve, or instrument...
> This record states that absence plainly rather than inventing a figure."

`XASSET-0005` §5 names the step that would close this gap as step 2 of a seven-step sequence
("perform asset-appropriate valuation/economic-assessment") and states plainly it is "future, separate,
undesigned." This artifact is that design — but it designs a narrower thing than the forced field's own
name might suggest. **It does not design the cross-asset opportunity-cost comparison** (`XASSET-0001`
§E/§F — comparing a dollar's best use across equities, ETFs, crypto, GLD, cash/reserve, and debt
reduction; still wholly undesigned, still a future, separate, later step). It designs the layer
underneath that: **a closed set of categorical, single-instrument economic questions specific to GLD,
CASH, and RESERVE**, whose answers become new evidence a future cross-asset synthesis would need but
which this design does not itself perform. This is the same "supply the evidence, not the comparison"
relationship `XASSET-0005`'s own overlap-model design (`XASSET-0007`, content authorized) already has to
`XASSET-0001` §F's own future synthesis — this artifact is that same relationship, one layer over, for
GLD/CASH/RESERVE's own instrument-level economics rather than portfolio-level overlap.

**Populating this schema in full, once a future implementation does so, does not by itself flip any
sealed functional-doctrine record's `economic_assessment_readiness.status` away from `assessment_required`.**
That transition — deciding whether this schema's evidence is sufficient to supersede the forced default —
is its own separate, later, explicitly authorized governance decision (§9 below), matching how
`VALUATION-0002`'s methodology-doctrine adoption is a decision distinct from `VALUATION-0001`'s research
charter, and how `VALUATION-0004`'s RQ4 evidence-architecture design is distinct from any future decision
that would actually use populated valuation evidence to execute a company valuation.

## 1. Why this design does not duplicate the equity valuation methodology work

`VALUATION-0001` designed a research charter comparing seven valuation-methodology families against
seven business-economics archetypes for the equity roster — a genuinely different problem shape than
this one. Three structural reasons this design does not, and should not, import that machinery:

- **Population size and kind.** The equity study needed a 7×7 matrix because 27 companies span
  materially different business-economics archetypes requiring different methodology families. GLD,
  CASH, and RESERVE are exactly three fixed, already-schema-defined capital-use types (`XASSET-0005`
  §3.1's own closed four-value `capital_use_type` vocabulary, minus `DEBT_REDUCTION` — excluded here per
  §2 below) — there is no archetype-differentiation question to research, because there is no
  archetype population to differentiate across. A matrix built for that problem would be solving a
  problem this one does not have.
- **Evidence shape.** Equity valuation methodology selection (DCF, multiples, ROIC, etc.) is a
  methodology-comparison question answered from finance literature and each methodology family's own
  data requirements — a genuinely comparative research question. GLD/CASH/RESERVE's economic
  characteristics (deployability, cost/tracking quality, historical inflation/drawdown behavior) are
  direct, sourceable, single-subject questions each capital-use type already has (or, for GLD, already
  has a sealed structural record for) — closer in shape to `VALUATION-0004`'s RQ4 evidence-architecture
  design (define a schema for evidence a future session will gather) than to `VALUATION-0001`'s
  methodology-comparison charter.
- **No archetype taxonomy needed.** `VALUATION-0001`'s protocol §5 froze a seven-category business-
  archetype taxonomy specifically because equity valuation methodology fit varies by archetype. Nothing
  in this design needs an analogous taxonomy — GLD, CASH, and RESERVE are each their own fixed category,
  one record each, no methodology-family selection question to resolve first.

**What this design does borrow from the `VALUATION-####` series, deliberately**: the design-then-
authorize-content separation (`VALUATION-0001`/`VALUATION-0002` before any archetype work; `VALUATION-0004`
before any evidence population); the closed, non-numeric, evidence-sufficiency-gated output vocabulary
discipline (`VALUATION-0002` §3's false-precision protections — mandatory abstention path, no fabricated
precision, disclosed provenance labeling); and the explicit "this evidence does not itself resolve the
forced default" boundary (`VALUATION-0002` §6.3(b)'s own precise, narrow reading of what "closes" a
research gap — merger to `main`, not merely accepted content). None of the equity-specific content
(archetype categories, methodology families, the 49-cell matrix) is imported.

## 2. Population — exactly three, `DEBT_REDUCTION` explicitly excluded

This design applies to exactly:

- `CASH`
- `RESERVE`
- `GLD_DEFENSIVE_ROLE`

**`DEBT_REDUCTION` is out of scope for this design.** `XASSET-0005` §3.5 already gives `DEBT_REDUCTION`
its own two-part `economic_assessment_readiness` split (`avoided_borrowing_cost_readiness` /
`survivability_and_buffer_benefit_readiness`), forced `assessment_required` on both sub-fields — closing
that gap is inseparable from the margin/leverage-policy track (the 1.8x leverage cap, the 30% buffer
floor, `MARGIN-0005`'s own bounded research charter for conditional margin deployment/repayment), which
this design does not touch and is not authorized to touch. A future `DEBT_REDUCTION` economic-assessment
methodology, if one is ever designed, belongs to that separately governed track, not this one — stated
here as a disclosed scope boundary, not an oversight.

No equity, ETF (other than GLD, addressed by reference only per §4), or cryptocurrency economic
assessment is addressed by this design — those remain `TIER-0009`'s (equity, `VALUATION-####`'s own
track) and future, wholly separate ETF/crypto valuation-methodology tracks respectively (`XASSET-0001`
§C item 2/3, still undesigned for economic assessment beyond the forced
`valuation_and_economic_assessment_readiness: valuation_required` default every sealed ETF/crypto record
already carries).

## 3. The closed question set — three shared axes, one GLD-only compound axis

### 3.1 Candidate questions evaluated → four designed axes, disposition table

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "How readily can this capital use be deployed toward a future opportunity?" | **Kept** → `deployability_and_optionality` axis (§3.2), all three types | Genuinely new — distinct from the already-sealed `liquidity_character` axis (which asks "is this convertible to cash," already answered `immediately_liquid` for all three) — this asks "does being in this capital-use state preserve or cost anything in the ability to act on a future opportunity." Not answered anywhere in this repository today. |
| "What is this capital use's functional role?" | **Not re-asked** — already sealed | `functional_role` already exists on every functional-doctrine record (`XASSET-0005` §3.2); re-asking it here would duplicate a sealed axis, not add evidence. This design consumes it by reference (§4) where relevant, never re-derives it. |
| "Is this capital use's principal exposed to market risk?" | **Not re-asked** — already sealed | `capital_preservation_character` already exists on every functional-doctrine record; same reasoning as above. |
| "How liquid is this capital use?" | **Not re-asked** — already sealed | `liquidity_character` already exists; same reasoning. |
| "Is GLD's cost/tracking-quality economically ordinary or notable for its category?" | **Kept** → `instrument_specific_economic_characterization.cost_and_tracking_economic_significance` (§3.3), `GLD_DEFENSIVE_ROLE` only | GLD's sealed ETF classification record already carries `cost_and_tracking_quality.expense_ratio_pct: 0.40` and `tracking_quality_category: not_yet_measured` as *structural* facts (`XASSET-0002`'s own ETF framework). No categorical judgment about whether that cost profile is economically ordinary, elevated, or favorable relative to comparable physical-commodity-backed funds exists anywhere — a genuinely new question, sourced from a peer comparison, never a numeric hurdle-rate or expected-cost-savings calculation. |
| "Is gold's historical relationship with inflation regimes established in citable literature?" | **Kept** → `instrument_specific_economic_characterization.historical_inflation_sensitivity` (§3.3), `GLD_DEFENSIVE_ROLE` only | A historically-grounded, sourced, backward-looking characterization question — never a forecast. Explicitly not answered by this design (§7 — future research interface). |
| "How has gold historically behaved during major equity-market drawdown periods?" | **Kept** → `instrument_specific_economic_characterization.historical_equity_drawdown_behavior` (§3.3), `GLD_DEFENSIVE_ROLE` only | Single-asset, historically-grounded characterization — explicitly and structurally distinct from a portfolio-level diversification-benefit or correlation-with-the-current-portfolio computation, which is `XASSET-0007`'s (overlap model's) `defensive_offset_interface` dimension, not this design's. See §5 for the exact ownership boundary and the mandatory disclosure every future record must carry. |
| "Does GLD's current market price or realized return over some period suggest it is under/overvalued?" | **Rejected outright** | This is a valuation/price-target question, permanently prohibited by CLAUDE.md's Guardrails ("No predictive research, price targets, or 'opportunity maps'") and already forced `valuation_required` on GLD's own sealed ETF record (`XASSET-0002` §6.3) — not reopened by this design. |
| "What is CASH's/RESERVE's expected return relative to deploying the same dollars into equities?" | **Rejected outright** | A hurdle-rate/expected-return comparison, explicitly prohibited by the authorizing design direction (§D of the governing task) and by `XASSET-0005` §3.5's own rejection of exactly this category error for `DEBT_REDUCTION` ("a single 'debt-reduction score' would silently average an opportunity-cost question against a survival-risk question... return and survival are not fungible in this repository's own established doctrine"). This is the cross-asset opportunity-cost synthesis (`XASSET-0001` §E), not this design's job. |
| "Is RESERVE functionally distinct from CASH, and if so how?" | **Considered, not made a new axis** | This is precisely the question `RESERVE.yaml`'s own sealed `functional_role.abstention_reason` already leaves open, and `XASSET-0006` §C already forecloses forcing an answer merely to fill the record. Re-asking it inside this new schema would either (a) duplicate the existing abstained axis without adding evidence, or (b) implicitly pressure a future drafting session to resolve it under a different field name — exactly the failure mode §6 below exists to prevent. This design instead states explicitly (§6) what future evidence or governance action would be needed, without asking the question itself. |

**Result: three shared substantive axes** (`deployability_and_optionality`; a `structural_reference_
functional_doctrine` pin, required on all three but not a judgment axis; `evidence_quality`) **plus one
GLD-only compound axis** (`instrument_specific_economic_characterization`, `not_applicable: true` on
`CASH`/`RESERVE`), **plus one GLD-only structural pin** (`structural_reference_etf_classification`,
forbidden on `CASH`/`RESERVE`) — the same "closed schema, conditional shape by discriminator" pattern
`XASSET-0005` §3.5 already established for `DEBT_REDUCTION`'s own two-part readiness split, applied here
in the opposite direction (one type gets an extra compound axis, the other two get `not_applicable`).

### 3.2 `deployability_and_optionality` (all three types, substantive axis)

- **Purpose**: record how readily this capital use can be deployed toward a future opportunity via the
  existing deposit/allocation workflow (`CLAUDE.md`'s own Workflow section — deposit, `allocate.py --cash`
  or `--margin`, present recommendation, execute manually) — the *optionality value* of holding this
  capital use, distinct from `liquidity_character`'s already-answered "is it convertible to cash" question.
- **Evidence inputs**: `CLAUDE.md`'s own Workflow section (deposit cycle, $25 minimum lot, manual
  execution) and Portfolio Doctrine (the allocator's own `RESERVE`/`CASH` "never a buy candidate,
  definitionally satisfied" treatment) — structural facts about *how* deployment happens, never a live
  dollar figure or a claim about *whether* deployment is currently advisable (that is a cross-asset
  synthesis question, out of scope here).
- **Closed vocabulary**: `high_optionality_low_friction` | `moderate_optionality` |
  `low_optionality_or_structurally_constrained` | `unable_to_determine` (with required `abstention_reason`).
- **Abstention state**: no `not_applicable` — every one of the three types has some deployability
  character by definition (even a genuinely constrained one is a determinate value, not an absence).
  `unable_to_determine` is reserved for a genuine evidence gap.
- **Prohibited inference**: no expected-return comparison against deploying the same dollars elsewhere;
  no target allocation percentage; no ranking against another capital-use type's own optionality; no
  claim about whether deployment is *currently* advisable (a timing/opportunity-cost question, out of
  scope per §1's own boundary against importing the cross-asset synthesis).
- **Non-cascading worked example (RESERVE)**: `RESERVE.yaml`'s own sealed `functional_role.role_category`
  is `unable_to_determine` — this does **not** automatically force `deployability_and_optionality` to
  abstain too. RESERVE and CASH share the identical mechanical deployment path (both are "never a buy
  candidate, definitionally satisfied," both deploy via the same deposit/allocation workflow) — a fact
  this design considers independently determinable from RESERVE's own structural facts, without first
  knowing *why* RESERVE exists as a distinct capital-use type from CASH. A future implementing session
  may determine this axis for RESERVE on that evidence. **This is not a pre-decision of RESERVE's own
  value** — the future implementing session may still find, on its own evidentiary judgment, that this
  axis genuinely cannot be determined without first knowing RESERVE's purpose (e.g., if a future
  clarification establishes RESERVE as a margin-cushion buffer specifically, that might carry
  deployment friction CASH does not), and abstain on its own merits. The point of this worked example is
  only that abstention on `functional_role` does not *automatically* force abstention here — each axis's
  own abstention is evaluated on its own evidence, never inherited.
- **Downstream use**: `deployability_summary` field of the cross-asset handoff envelope (§8); a required
  future input to any cross-asset opportunity-cost synthesis (`XASSET-0001` §E) that would need to know
  not just whether a capital use is liquid, but how frictionlessly it converts into an actual allocation
  decision.

### 3.3 `instrument_specific_economic_characterization` (`GLD_DEFENSIVE_ROLE` only; `not_applicable: true` for `CASH`/`RESERVE`)

**Purpose**: GLD is the only one of the three capital-use types that references a priced, market-traded
instrument with its own independent economic history — CASH and RESERVE are account-state facts, not
instruments with a cost structure, a tracking benchmark, or a historical price series. This compound axis
exists to hold the GLD-specific economic questions §3.1's disposition table identifies, without inventing
parallel (and meaningless) sub-fields for CASH/RESERVE.

A closed, structurally required compound object with three independently-abstainable sub-fields:

#### `cost_and_tracking_economic_significance`

- **Purpose**: characterize whether GLD's already-structurally-recorded expense ratio (0.40%, per
  `intelligence/etf_classification/GLD.yaml`) and (once measured) tracking quality are economically
  ordinary, elevated, or favorable for its fund category — never a numeric cost-savings or
  hurdle-rate calculation.
- **Evidence inputs**: GLD's own sealed ETF classification record (`structural_reference_etf_
  classification`, §4 — consumed by reference, never restated); a sourced comparison to other
  physical-gold-backed or comparable commodity-ETF expense ratios (a categorical peer characterization,
  not a numeric peer-multiple calculation).
- **Closed vocabulary**: `in_line_with_category` | `elevated_vs_category` | `favorable_vs_category` |
  `unable_to_determine`.
- **Prohibited inference**: no numeric cost-savings figure; no claim that a lower-cost alternative
  should be substituted (that is a Level 2 instrument-selection question, `XASSET-0001` §E, out of
  scope).

#### `historical_inflation_sensitivity`

- **Purpose**: a historically-grounded, sourced characterization of gold's documented relationship with
  inflation regimes — established literature only, never a forecast or a forward-looking claim.
- **Evidence inputs**: citable, dated, sourced historical/academic material (§7 — not yet gathered by
  this design).
- **Closed vocabulary**: `historically_positively_associated` | `historically_mixed_or_inconsistent` |
  `historically_weakly_associated` | `unable_to_determine`.
- **Prohibited inference**: no forward-looking inflation forecast of any kind (an absolute prohibition,
  not merely a discouraged practice — a violation of CLAUDE.md's "No predictive research" guardrail);
  no numeric inflation-beta or correlation coefficient.

#### `historical_equity_drawdown_behavior`

- **Purpose**: a historically-grounded, **single-asset** characterization of gold's own price behavior
  during major historical equity-market drawdown periods — explicitly not a portfolio-level
  diversification-benefit or correlation-with-the-current-Portfolio-HQ-portfolio computation.
- **Evidence inputs**: citable, dated, sourced historical market data or academic material covering
  gold's own price behavior during named historical drawdown episodes (§7 — not yet gathered).
- **Closed vocabulary**: `historically_uncorrelated_or_negatively_correlated` | `historically_mixed` |
  `historically_positively_correlated` | `unable_to_determine`.
- **Prohibited inference**: no numeric correlation coefficient or beta of any kind; no claim about GLD's
  diversification benefit *to Portfolio-HQ's own current holdings* (that is `XASSET-0007`'s
  `defensive_offset_interface` dimension — see §5's mandatory disclosure requirement, binding on every
  future record populating this sub-field).

**Abstention state (whole compound axis)**: `not_applicable: true` (literal, structural) on `CASH`/
`RESERVE` — the axis simply does not exist for a non-instrument capital-use type, not an evidence gap.
On `GLD_DEFENSIVE_ROLE`, each of the three sub-fields independently supports `unable_to_determine` with
its own `abstention_reason` — one sub-field's abstention never cascades to the other two (the same
non-cascading rule §3.2 and every prior framework already apply).

### 3.4 `evidence_quality`

Identical design to every prior framework's own axis (`comprehensive`/`partial`/`limited` vocabulary,
required `thesis_uncertainty_statement`). Not restated here to avoid duplication.

## 4. Structural references — reuse, never duplicate

Two independent, narrowly-scoped content-hash pins, both consuming an existing sealed record's public
hash function rather than inventing a new hashing scheme — the same pattern `XASSET-0005` §3.4 already
established for `GLD_DEFENSIVE_ROLE`'s own pin into `GLD.yaml`, reused here a layer further out.

### `structural_reference_functional_doctrine` (required on all three population members)

- `source_capital_use_type`: `CASH` | `RESERVE` | `GLD_DEFENSIVE_ROLE` — must match this record's own
  `capital_use_type` exactly (a self-referencing pin, confirming this economic-assessment record is
  anchored to its own corresponding sealed functional-doctrine record, not a different one).
- `source_schema`: literal `"functional_doctrine"`.
- `source_file`: literal `"intelligence/functional_doctrine/<CAPITAL_USE_TYPE>.yaml"`.
- `referenced_content_sha256`: the pinned hash of the corresponding sealed functional-doctrine record,
  computed via `functional_doctrine_validator.canonical_record_hash()` — the already-existing,
  already-tested function `functional_doctrine_validator.py:355` exposes, confirmed present by direct
  inspection this session, never a newly invented hashing scheme.
- **Enforcement**: a future validator recomputes the live hash on every run and rejects a stale
  reference, mirroring `functional_doctrine_validator.py`'s own identical enforcement of its own pin
  into `etf_classification_validator.py`'s hash (§3.4 there). **None of the seven functional-doctrine
  axis names** (`functional_role`, `hard_constraint_status`, `economic_assessment_readiness`,
  `liquidity_character`, `capital_preservation_character`, `freshness_state`, plus the envelope
  discriminator `capital_use_type` itself) may appear duplicated as a re-derived value anywhere inside
  an `economic_assessment` record — they are consumed by reference (this pin), never restated.

### `structural_reference_etf_classification` (required only on `GLD_DEFENSIVE_ROLE`; forbidden on `CASH`/`RESERVE`)

- Identical shape to `GLD_DEFENSIVE_ROLE.yaml`'s own existing `structural_reference` object
  (`source_instrument_id: "GLD"`, `source_schema: "etf_classification"`,
  `source_file: "intelligence/etf_classification/GLD.yaml"`, `referenced_content_sha256`) — the exact
  same pin mechanism, reused a second time, never redefined. Computed via
  `etf_classification_validator.canonical_record_hash()` (`etf_classification_validator.py:322`).
- **Why a direct pin into `GLD.yaml`, rather than only pinning into `GLD_DEFENSIVE_ROLE.yaml` and
  reading GLD's structural facts through that one hop.** `GLD_DEFENSIVE_ROLE.yaml` itself does not
  restate GLD's cost/tracking-quality structural facts (`XASSET-0005` §3.4's own forbidden-key scan
  bars it from doing so) — the `cost_and_tracking_economic_significance` sub-field (§3.3) needs GLD's
  own `cost_and_tracking_quality.expense_ratio_pct`/`tracking_quality_category` fields directly, which
  only `GLD.yaml` itself carries. A single-hop direct reference is simpler and more auditable than
  requiring a future validator to trust a two-hop indirect path through a record that does not itself
  carry the needed fields.
- **None of the ETF framework's own six axis key names** (`structural_role`, `constituent_exposure`,
  `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`)
  may appear duplicated as a re-derived value anywhere in an `economic_assessment` record — consumed by
  reference only, identical rule to `GLD_DEFENSIVE_ROLE.yaml`'s own existing forbidden-key scan.

## 5. GLD / overlap-model ownership boundary — mandatory disclosure

`historical_equity_drawdown_behavior` (§3.3) and any future portfolio-level defensive-offset question
sit close enough together to require an explicit, structural boundary, not merely a naming convention:

| Question | Owner | Shape |
|---|---|---|
| "How has gold itself historically behaved during major equity-market drawdown episodes?" | **This design** (`historical_equity_drawdown_behavior`) | Single-asset, historical, categorical. |
| "Does GLD provide a measurable diversification benefit *to Portfolio-HQ's own current portfolio*?" | `XASSET-0007`'s `defensive_offset_interface` dimension (overlap model, content authorized, not yet populated) | Portfolio-level, forced `not_yet_computable_interface_only` today, per `XASSET-0005` §6.2's own unconditional rule. |

**Every future `GLD_DEFENSIVE_ROLE` economic-assessment record must carry an explicit disclosure
statement** (folded into `uncertainty_summary` or a dedicated note) stating that
`historical_equity_drawdown_behavior`'s finding is single-asset and historical only, and does **not**
itself constitute, imply, or substitute for a computed whole-portfolio diversification-benefit finding —
that remains `defensive_offset_interface`'s own, separate, still-forced-abstention job. This design does
not loosen `XASSET-0005` §6.2's forced value on that dimension, and does not authorize any future
`economic_assessment` record to be cited as though it already answered the overlap model's own question.

This mirrors `XASSET-0005` §3.4's identical GLD structural/functional separation discipline, applied here
one layer further: economic characterization of GLD-the-instrument (this design) is kept structurally and
textually distinct from GLD's role in the whole portfolio (functional doctrine, sealed) and from GLD's
measured relationship to the rest of the current portfolio (overlap model, unpopulated) — three separate,
non-duplicating record types, each citing the others by reference where relevant, never re-deriving.

## 6. RESERVE — preserved abstention, explicit resolution path

`RESERVE.yaml`'s sealed `functional_role.role_category: unable_to_determine` is **not resolved,
narrowed, or worked around by this design**. This section states, as required by the governing
authorization, what future evidence or governance action would actually be needed to resolve it — a
disclosure, not an attempt.

**What would resolve the abstention:**

1. **A future, separately governed functional-doctrine content-refresh decision** (mirroring `PI-0018`'s
   NVDA-refresh or `PI-0022`'s COST-refresh precedent for Company Intelligence, applied here to
   functional doctrine for the first time) that cites new `CLAUDE.md` doctrine text or an explicit
   principal statement naming RESERVE's specific intended purpose — for example, distinguishing it from
   `CASH` as a margin-cushion buffer, a deployment-timing dry-powder pool, or some other named function.
   This requires new evidence to exist first (a `CLAUDE.md` passage or an equivalent governed source),
   not merely a future session's own inference.
2. **An explicit principal statement, recorded in its own future governance filing, confirming the
   abstention should stand as RESERVE's own permanent governed doctrine** — i.e., that RESERVE
   deliberately carries no functional distinction from CASH beyond the account-structuring convenience
   of two separate `targets.yaml` rows, and no further resolution is sought. This is itself a valid,
   named resolution path (an explicit "no distinct function" finding is not the same thing as an
   unresolved gap), not merely a fallback.

**What this design does not do**: it does not perform, invite, schedule, or presume either path. It does
not add a third capital-use-type-shaped question (e.g., "is RESERVE redundant with CASH?") as a proxy for
resolving the functional-role question through a different field name — §3.1's disposition table
explicitly considered and rejected that move. `deployability_and_optionality` (§3.2) is independently
determinable for RESERVE on its own evidence and does not require this resolution first, but the
functional-role question itself remains exactly as open as `RESERVE.yaml`'s own sealed record already
states.

## 7. Future research interface — three named, unanswered questions

This design identifies, but does not answer, three research questions a future implementing session
would need to address before it could populate `instrument_specific_economic_characterization`'s
sub-fields with anything beyond `unable_to_determine`:

1. **GLD's own historical behavior during major equity-market drawdown periods** (feeds
   `historical_equity_drawdown_behavior`, §3.3) — requires sourced, dated historical market data or
   academic material; not gathered by this design.
2. **GLD's realized tracking quality against its own benchmark** (the LBMA Gold Price PM, per
   `GLD.yaml`'s own sealed `structure_and_methodology.benchmark_type`) — feeds `cost_and_tracking_
   economic_significance`, §3.3, and would also resolve GLD's own sealed ETF record's
   `tracking_quality_category: not_yet_measured` value if the implementing session's evidence proves
   sufficient (a possible, but not required, side effect — resolving that field belongs to a future ETF
   record-refresh decision, not automatically to this schema's own population); not gathered by this
   design.
3. **A defensible, sourced, long-horizon characterization of gold's relationship to inflation regimes**
   (feeds `historical_inflation_sensitivity`, §3.3) — requires citable historical/academic literature;
   not gathered by this design.

A future implementation may answer any, all, or none of these — an honest `unable_to_determine` with a
specific `abstention_reason` (e.g., "primary source X was attempted but blocked; secondary aggregation
found insufficiently corroborated") remains a fully valid, complete, sealed record, matching every prior
framework's own abstention discipline. **This design performs no research of any kind and treats none of
these three questions as already answered** — stated explicitly because a future session reading this
artifact must not mistake the existence of a well-specified question for the existence of its answer.

## 8. Synthesis handoff — categorical evidence only

Every future `economic_assessment` record carries a `cross_asset_handoff` envelope object, matching the
shape every prior classification framework in this repository already uses:

| Field | Sourced from | Explicitly excluded from this or any field in this envelope |
|---|---|---|
| `deployability_summary` | `deployability_and_optionality` (verbatim copy) | — |
| `instrument_specific_summary` | `instrument_specific_economic_characterization` (verbatim copy, or `not_applicable` marker) | — |
| `evidence_quality_summary` | `evidence_quality.primary_source_coverage` (verbatim copy) | — |
| `uncertainty_summary` | the envelope's own field, not re-derived | — |

**Absolutely excluded from this envelope, and from every other field in this schema, at any level**:
target weights or ranges; a rank or ranking of any kind; an IN/OUT portfolio-selection determination; a
buy/sell/hold/trim/exit/wait/stage signal or directive of any kind; a sleeve percentage or Level 1/Level
2 allocation figure; a trade-timing recommendation; a leverage amount or margin-deployment instruction.
This is the identical restriction every prior schema's own envelope (ETF, crypto, functional-doctrine)
already carries — restated here because a `cross_asset_handoff` object's entire purpose is to be read by
a future synthesis unit, making it exactly the place a scope-creeping field would first appear if this
design were not explicit about excluding it.

**The future synthesis, not this design, compares competing uses of capital** — restated directly from
the governing authorization, and structurally identical to `XASSET-0005` §9's own closing statement that
neither the functional-doctrine nor the overlap-model schema computes an expected return, an avoided
cost, or an overlap risk score; both supply categorical, evidence-based facts a future step would need,
without themselves performing that step.

## 9. Portfolio-selection boundary — restated, binding

Completing economic assessment for GLD, CASH, and RESERVE — even a fully populated, zero-abstention set
of three sealed records — **does not select the portfolio**. It creates evidence for a later selection
mechanism that does not yet exist. The full chain, restated from `XASSET-0001` §E and `XASSET-0005` §5,
unedited by this design:

> evidence (Company/Theme/relationship/classification Intelligence; ETF/crypto classification;
> functional doctrine; **this design's own future economic-assessment records**; overlap-model
> dimensions) → cross-asset opportunity-cost synthesis (`XASSET-0001` §E/§F, wholly undesigned) → an
> explicit, human-approved adoption decision → only then, governed IN/OUT portfolio membership, sleeve
> targets, and instrument targets.

This design occupies exactly one box in that chain — an evidence-supply box, three types wide. It does
not perform, shortcut, or imply any of the boxes after it.

## 10. Validator specification (for the future implementing PR)

A future implementation must build one dedicated validator module (`economic_assessment_validator.py`,
matching this repository's established one-schema-one-validator-module norm — `etf_classification_
validator.py`/`crypto_classification_validator.py`/`functional_doctrine_validator.py` each stand alone)
enforcing, at minimum:

1. **Exact population enforcement** — exactly three `capital_use_type` values (`CASH`, `RESERVE`,
   `GLD_DEFENSIVE_ROLE`), no `DEBT_REDUCTION`, no fourth value, no fewer than three.
2. **Closed schema at every level, rejecting extra keys, not just missing ones** — envelope, both
   structural-reference objects, `instrument_specific_economic_characterization` and its three
   sub-fields, `deployability_and_optionality`, `evidence_quality`, `cross_asset_handoff` — the
   `contender_registry_validator.py` MAJOR-finding lesson, applied from the start (§10.1 below).
3. **`capital_use_type`-conditional shape enforcement** — `structural_reference_etf_classification` and
   the populated (non-`not_applicable`) form of `instrument_specific_economic_characterization` required
   on `GLD_DEFENSIVE_ROLE` only, forbidden (rejected as an unknown key or an invalid state) on `CASH`/
   `RESERVE`.
4. **No cross-schema field-name leakage** — a dedicated forbidden-key scan barring every equity-shaped
   (`economic_role`, `capital_priority`, `risk_concentration`), ETF-shaped (`structural_role`,
   `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`,
   `structure_and_methodology`), crypto-shaped (`network_fundamentals`, `economic_model`,
   `liquidity_and_market_structure`, `custody_and_counterparty_risk`, `correlation_and_volatility`,
   `regulatory_and_structural_uncertainty`), functional-doctrine-shaped (`functional_role`,
   `hard_constraint_status`, `liquidity_character`, `capital_preservation_character`, `freshness_state`),
   or overlap-model-shaped (`dimension_id`, `dimension_type`, `source_mechanism`, `computation_status`,
   `output_shape`) key name from appearing anywhere in an `economic_assessment` record.
5. **Zero numeric field anywhere** — a forbidden-key/forbidden-pattern scan for `expected_return`,
   `hurdle_rate`, `price_target`, `fair_value`, `correlation_coefficient`, `beta`, `target_pct`,
   `target_weight`, `opportunity_cost_score`, `ranking_score`, `allocation_pct`, `leverage_amount`, or
   any bare numeric-percent-shaped token — **with no carve-out of any kind**, matching the functional-
   doctrine and overlap-model schemas' own zero-numeric-field posture (stricter than the ETF framework's
   scoped `expense_ratio_pct` exception — this schema does not restate that figure either, consuming it
   only by structural reference, §4).
6. **`structural_reference_functional_doctrine` enforcement** — required-on-all-three shape check; a
   live recompute of the corresponding sealed functional-doctrine record's hash via
   `functional_doctrine_validator.canonical_record_hash()` (read-only reuse); confirmation that
   `source_capital_use_type` matches the record's own `capital_use_type` exactly (self-consistency
   check, not merely a valid-enum check).
7. **`structural_reference_etf_classification` enforcement** — required-only-on-`GLD_DEFENSIVE_ROLE`
   shape check, forbidden on `CASH`/`RESERVE`; a live recompute of GLD's ETF record hash via
   `etf_classification_validator.canonical_record_hash()` (read-only reuse), mirroring §7 point 8 of
   `XASSET-0005`'s own overlap-model/functional-doctrine validator specification exactly.
8. **No chart-evidence leakage** — the same term-list free-text scan every prior validator in this
   repository already uses, built in from the start.
9. **No directive/trading-language leakage** — a word-boundary-matched scan for the shared eight words
   (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`), word-boundary matched so it does not
   false-positive on "holdings" or a section title.
10. **No predictive-language leakage** — a dedicated, independent scan (distinct from the historical-
    characterization vocabulary this schema legitimately uses) for forward-looking terms
    (`forecast`, `predict`, `expected to`, `will likely`, `projected`) inside
    `historical_inflation_sensitivity`'s and `historical_equity_drawdown_behavior`'s own free-text
    fields specifically — the mechanical enforcement of §3.3's "established literature only, never a
    forecast" prohibition, a defect class no prior schema in this repository needed to guard against
    (every prior framework's own free-text scans target chart/directive/policy leakage, never
    predictive-tense language specifically).
11. **Overlap-model non-duplication check** — a dedicated scan confirming no `economic_assessment`
    record's `historical_equity_drawdown_behavior` sub-field, or its `cross_asset_handoff` copy, is
    represented as a computed portfolio-level correlation or diversification-benefit finding (§5's
    mandatory disclosure requirement, enforced structurally, not merely documented) — e.g., rejecting a
    record whose `uncertainty_summary` or sub-field rationale asserts a whole-portfolio conclusion
    without the required single-asset disclosure.
12. **Evidence/provenance validation** — every `provenance.sources` entry carries a type and
    access-status field, mirroring every prior pipeline's own discipline.
13. **Allocator/margin decoupling** — zero import coupling with `allocate.py`/`margin_state.py` in
    either direction.
14. **Deterministic generation; protected-path isolation** — repeated runs against the same input
    produce byte-identical results; zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`,
    `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing
    `intelligence/classification|companies|themes|relationships|etf_classification|crypto_
    classification|functional_doctrine/` record, and every existing governance decision file.

### 10.1 Lessons explicitly carried forward from prior validator review history

- **Closed-schema checks must reject extra keys, not just missing ones**
  (`contender_registry_validator.py`'s own MAJOR finding) — point 2 above.
- **An independent second-stage check must use a materially different mechanism than the logic it
  verifies** (`TIER-0004`'s own dangling-reference correction) — the predictive-language scan (point
  10) and the overlap-model non-duplication scan (point 11) must each be their own free-text pass, never
  a byproduct of the closed-vocabulary enum check that accepts or rejects a sub-field's own categorical
  value.
- **A required envelope field needs its own independent presence/type check**
  (`etf_classification_validator.py`'s own MINOR-1 finding) — applies equally to both structural-
  reference objects, not only to the fields exercised by the first real records a future implementation
  drafts.
- **A self-declared flag is not a substitute for an independent scan**
  (`reconciliation_validator.py`'s own MINOR finding) — `not_applicable: true` on `instrument_specific_
  economic_characterization` for `CASH`/`RESERVE` must be independently checked against
  `capital_use_type`, never merely trusted as self-declared.

## 11. Test specification (for the future implementing PR)

A future implementation's focused test suite must cover, at minimum, one test per item below:

- Happy-path record for each of the three `capital_use_type` values validates clean.
- Malformed envelope/axis schema (missing required field) rejected.
- Extra unknown key at envelope level and at every nested level rejected.
- Wrong `capital_use_type` value (outside the closed three, including `DEBT_REDUCTION` specifically)
  rejected.
- `structural_reference_etf_classification` present on `CASH`/`RESERVE` rejected; missing on
  `GLD_DEFENSIVE_ROLE` rejected.
- `instrument_specific_economic_characterization` populated (non-`not_applicable`) on `CASH`/`RESERVE`
  rejected; `not_applicable: true` on `GLD_DEFENSIVE_ROLE` rejected (must be a populated compound object
  there).
- Both structural-reference hashes independently verified against a live recompute — a synthetic
  stale-hash test for each, and a live test against the real sealed `GLD.yaml`/`GLD_DEFENSIVE_ROLE.yaml`
  once populated.
- `source_capital_use_type` mismatched against the record's own `capital_use_type` rejected (e.g., a
  `CASH` record whose functional-doctrine pin names `RESERVE`).
- Any cross-schema field name (equity, ETF, crypto, functional-doctrine, overlap-model — each source
  schema's key names tested individually) present anywhere rejected.
- Forbidden numeric-field leakage (each named term in §10 point 5, individually) rejected — no positive-
  acceptance test, since this schema carries zero numeric-field exceptions.
- Chart-terminology leakage (each term individually) rejected.
- Directive/trading-language leakage (each of the shared eight words individually) rejected, including a
  false-positive-guard test for ordinary "holdings"/"funding" usage.
- Predictive-language leakage (each named term in §10 point 10, individually) rejected, scoped to the two
  named sub-fields specifically — plus a positive test confirming the same terms are *not* flagged
  elsewhere in the document where they would be false positives (e.g., inside a citation's own title).
- Overlap-model non-duplication: a synthetic record whose `historical_equity_drawdown_behavior` rationale
  asserts a whole-portfolio diversification claim without the required single-asset disclosure rejected.
- Abstention behavior: `unable_to_determine` without `abstention_reason` rejected on every substantive
  axis and sub-field; `not_applicable` used where the schema does not permit it (e.g., on
  `deployability_and_optionality`, which has no `not_applicable` path per §3.2) rejected; a fully
  abstained record (every axis `unable_to_determine` with a valid reason, where the axis supports it)
  accepted as sealed-eligible.
- Non-cascading abstention: a synthetic `RESERVE` record with `deployability_and_optionality` determined
  and no other axis abstained validates clean, proving the schema itself imposes no cascade — this test
  does not assert anything about `RESERVE.yaml`'s own `functional_role` abstention, which lives in a
  different schema entirely.
- Duplicate/missing/extra `capital_use_type` entry within a population batch rejected.
- Deterministic output: two consecutive validator runs against identical input produce byte-identical
  results.
- Protected-path isolation: zero diff on every path named in §10 point 14.
- Allocator/margin import-coupling test: a static-analysis-style check confirming the future validator
  module imports neither `allocate.py` nor `margin_state.py`.

## 12. Objective preserved, not invented

This design does not define, redefine, or narrow Portfolio-HQ's governing objective (`XASSET-0001` §A,
unedited). It supplies three categorical, evidence-based facts a future asset-appropriate valuation/
economic-assessment step and a future cross-asset opportunity-cost synthesis would need, without itself
computing an expected return, an avoided cost, a hurdle rate, or a risk-adjusted comparison of any kind.
The "next-dollar opportunity-cost methodology" `XASSET-0001` §E/§A implies remains wholly undesigned by
this artifact — exactly as `XASSET-0002` §11 and `XASSET-0005` §9 already stated for the ETF/crypto and
functional-doctrine/overlap-model schemas, restated here for the third time for the same reason: this is
a required future principal/governance decision, not a byproduct of a design filing.
