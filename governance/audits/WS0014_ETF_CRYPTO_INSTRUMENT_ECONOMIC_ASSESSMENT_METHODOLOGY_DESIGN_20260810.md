# WS-0014 ETF/Crypto Instrument Economic Assessment Methodology — retained design artifact

**Filed under**: `XASSET-0010`
(`governance/decisions/XASSET-0010-etf-crypto-economic-assessment-methodology.md`)
**Date**: 2026-08-10
**Scope**: `XASSET-0005` §5 step 2's own restated sequence ("perform asset-appropriate valuation/economic
assessment"), for the six-instrument population `XASSET-0008`'s own whole-universe boundary named as
still unfinished — three ETFs (`SPY`, `VEA`, `VWO`) and three cryptocurrencies (`BTC`, `ETH`, `SOL`).
Design only. No record is populated, no economic finding is stated for any instrument, and no sealed
classification record's forced `valuation_and_economic_assessment_readiness` value is superseded by this
artifact.

This artifact is the full field-by-field methodology design. The decision file summarizes it and carries
the authorization/consequences text; this document is the retained detail, matching the
`TIER-0001`→`TIER-0002`, `XASSET-0001`→`XASSET-0005`, and `XASSET-0008`'s own supporting-artifact
precedent.

---

## 1. Why this design does not reuse `VALUATION-####`'s equity-methodology machinery

`VALUATION-0001`/`VALUATION-0002` designed a research charter comparing seven valuation-methodology
families against seven business-economics archetypes for the equity roster. Three structural reasons this
design does not import that machinery:

- **Population size and kind.** The equity study needed a 7×7 matrix because 27 companies span materially
  different business-economics archetypes requiring different methodology families. Six instruments split
  cleanly into two homogeneous asset-type groups (three broad-index ETFs; three cryptocurrencies) with no
  archetype-differentiation question inside either group.
- **Evidence shape.** None of the six instruments has financial statements, earnings, segments, or a
  capital-allocation decision-maker in the equity sense — a DCF/SOTP/relative-valuation family framework
  has no coherent input for any of them, matching exactly the same reasoning `XASSET-0001` §C already used
  to reject forcing ETF/crypto evidence into the equity Company Intelligence schema at the classification
  layer.
- **No archetype taxonomy needed.** Nothing in this design needs an analogous taxonomy — each ETF and each
  coin is already its own fixed, classified category (per its own sealed `structural_role`/
  `network_fundamentals` finding); no methodology-family selection question exists to resolve first.

**What this design does borrow from the `VALUATION-####` series and from `XASSET-0008`, deliberately**:
the design-then-authorize-content separation; the closed, non-numeric, evidence-sufficiency-gated output
vocabulary discipline (`VALUATION-0002` §3's false-precision protections); and the explicit "this evidence
does not itself resolve the forced default" boundary (`VALUATION-0002` §6.3(b)'s own precise reading of
what "closes" a research gap — merge to `main`, not merely accepted content). None of the equity-specific
content (archetype categories, methodology families, the 49-cell matrix, discount-rate mechanics) is
imported.

## 2. Method: reuse general classification hygiene, do not reuse asset-shaped fields (unchanged discipline)

Same starting question every prior framework in this repository has asked: *does this field exist in
currently-authoritative repository evidence, and does representing it as a standing fact materially
improve a future decision that today requires manual cross-referencing or is not represented at all?*
Two structural moves carry over from every prior framework:

- **Narrative-judgment fields are kept separate from mechanically-computed fields** — the same split
  `TIER-0002`, `XASSET-0002`, `XASSET-0005`, and `XASSET-0008` each already applied. This design's own
  substantive axes (§5.2, §6.2) are narrative-judgment fields, sourced from evidence, never derived by
  formula; the structural-reference hash checks (§3) are mechanical.
- **Evidence quality and abstention are per-field disciplines, not a bolted-on axis** — the same
  `not_applicable`/`unable_to_determine` two-state discipline every prior framework already established.

One structural move is reused, not new, from `XASSET-0005`/`XASSET-0008`: a **cross-schema reference-by-
hash mechanism** (§3) — simpler here than either of `XASSET-0008`'s own two variants, since every
instrument in this population already has exactly one sealed classification record of its own to pin to
(no dual reference like `GLD`'s; no legacy-reference list like `CASH_LIKE_CAPITAL`'s).

## 3. Structural references — reuse, never duplicate; one pin per instrument

Every future `instrument_economic_assessment` record carries exactly one `structural_reference` object:

| Field | Value |
|---|---|
| `source_instrument_id` | The instrument's own ticker (`SPY`, `VEA`, `VWO`, `BTC`, `ETH`, or `SOL`) — must equal the record's own top-level `instrument_id`. |
| `source_schema` | `"etf_classification"` for the ETF sub-population; `"crypto_classification"` for the crypto sub-population. |
| `source_file` | `intelligence/etf_classification/<TICKER>.yaml` or `intelligence/crypto_classification/<TICKER>.yaml`, matching `source_schema`. |
| `referenced_content_sha256` | Computed via `etf_classification_validator.canonical_record_hash()` (`etf_classification_validator.py:322`) or `crypto_classification_validator.canonical_record_hash()` (`crypto_classification_validator.py:347`), selected by `asset_type`. |

A future validator must independently, live-recompute this hash on every run — rejecting a stale
reference exactly as `GLD.yaml`'s own pin into its ETF classification record already does. None of the
ETF or crypto classification framework's own axis key names (`structural_role`, `constituent_exposure`,
`overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`,
`network_fundamentals`, `economic_model`, `liquidity_and_market_structure`, `custody_and_counterparty_
risk`, `correlation_and_volatility`, `regulatory_and_structural_uncertainty`) may appear duplicated as a
re-derived value anywhere in an `instrument_economic_assessment` record — consumed by reference only.

**Why one pin, not two or a list.** `GLD`'s own dual-pin mechanism exists because `GLD` has both an ETF
structural identity and a separate, sealed functional-doctrine (portfolio-role) record. None of the six
instruments in this population has a functional-doctrine record of its own — `CASH_LIKE_CAPITAL`'s own
two-entry legacy-reference-list mechanism exists because it is a non-instrument projection over two
pre-existing records with no sealed record of its own to anchor a single pin to. Every instrument here
already has exactly one sealed classification record and needs exactly one pin.

## 4. Shared envelope — common to both sub-populations

### 4.1 Top-level keys

| Key | Category | Notes |
|---|---|---|
| `schema_version` | Envelope | `'1.0'`. |
| `instrument_id` | Envelope | `SPY` \| `VEA` \| `VWO` \| `BTC` \| `ETH` \| `SOL` — closed, exactly six values. |
| `asset_type` | Envelope | `etf` \| `cryptocurrency` — must match `instrument_id`'s own real classification-layer `asset_type`. |
| `structural_reference` | Population-conditional shape (§3), required on every record | Single object, not a list, not asset-type-differentiated in shape — only in `source_schema`/`source_file` value. |
| `cost_and_tracking_quality_economic_significance` | Substantive axis, `etf` only (§5.2) | Forbidden (rejected as an unknown key) on `cryptocurrency` records. |
| `macro_behavioral_characterization` | Substantive axis, `cryptocurrency` only (§6.2) | Forbidden (rejected as an unknown key) on `etf` records. |
| `evidence_quality` | Shared axis (§4.4) | Required on every record. |
| `provenance` | Envelope | Required on every record. |
| `uncertainty_summary` | Envelope | Required, non-empty. |
| `evidence_quality_status` | Envelope | Verbatim copy of `evidence_quality.primary_source_coverage`. |
| `record_status` | Envelope | `draft` \| `sealed`. |
| `cross_asset_handoff` | Envelope (§4.6) | Required on every record. |
| `abstention_index` | Envelope | List, possibly empty. |
| `sealed_at` / `governing_decision` / `drafting_session_or_shard_id` / `content_sha256` / `cohort_manifest_entry` | Seal metadata | Required only when `record_status: sealed`, matching every prior framework's own convention. |

No key beyond this closed set is permitted at the top level of any record — a future validator must
reject any unknown key, not merely check for the presence of required ones (§9 point 2).

### 4.2 `cost_and_tracking_quality_economic_significance` (`etf` only — full spec, §5.2)

### 4.3 `macro_behavioral_characterization` (`cryptocurrency` only — full spec, §6.2)

### 4.4 `evidence_quality` (unchanged shape from every prior framework)

- **Keys**: `primary_source_coverage` (`comprehensive` \| `partial` \| `limited`), `thesis_uncertainty_
  statement` (required, non-empty).
- Not restated in further detail here to avoid duplication — identical to `economic_assessment_
  validator.py`'s own `_EVIDENCE_QUALITY_ALLOWED_KEYS` shape and every prior framework's own.

### 4.5 `provenance`

- **Keys**: `sources` — a list of source objects, each carrying `source_identifier`, `source_type`
  (`primary` \| `secondary`), `as_of_date`, `access_status` (`directly_inspected` \|
  `consulted_via_search_aggregation` \| `attempted_not_directly_inspected`), optional `limitation`.
  Identical shape to every prior framework's own `provenance` block.

### 4.6 `cross_asset_handoff` — exactly three fields (tighter than `GLD`'s own four)

| Field | Sourced from |
|---|---|
| `economic_characterization_summary` | The one populated substantive axis's own categorical determination(s), verbatim (a single value for `etf` records; both sub-field values, concatenated or structured, for `cryptocurrency` records). |
| `evidence_quality_summary` | `evidence_quality.primary_source_coverage` (verbatim copy). |
| `uncertainty_summary` | The envelope's own field, not re-derived. |

**No `deployability_summary` field** — unlike `GLD`/`CASH_LIKE_CAPITAL`'s own envelope, this population
has no `deployability_and_optionality` axis (§5.1, §6.1 disposition tables both reject it as already
answered at the classification layer), so no corresponding handoff field exists.

**Absolutely excluded from this envelope, and from every other field in this schema, at any level**:
target weights or ranges; a rank or ranking of any kind; an IN/OUT portfolio-selection determination; a
buy/sell/hold/trim/exit/wait/stage signal or directive of any kind; a sleeve percentage or Level 1/Level 2
allocation figure; a trade-timing recommendation; a leverage amount; a numeric coefficient of any kind
(including a cross-coin correlation coefficient — §6.1).

## 5. ETF-specific methodology (`SPY`, `VEA`, `VWO`)

### 5.1 Candidate questions evaluated → disposition table (full reasoning)

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "Is this ETF's cost/tracking-quality profile economically ordinary or notable for its category?" | **Kept** → `cost_and_tracking_quality_economic_significance` | Genuinely new — each ETF's own sealed `cost_and_tracking_quality.expense_ratio_pct` (SPY 0.0945%, VEA 0.03%, VWO 0.06%) and `tracking_quality_category: not_yet_measured` are structural facts only; no categorical judgment about whether that cost profile is ordinary, elevated, or favorable for the fund's own category exists anywhere today. |
| "How readily can this fund's position be deployed toward a future opportunity?" | **Rejected — already answered at the classification layer** | All three records' own sealed `liquidity.liquidity_tier: high_liquidity` already answers this. Unlike `GLD`/`CASH_LIKE_CAPITAL` (genuinely non-standard capital-use states whose own optionality had no prior answer), `SPY`/`VEA`/`VWO` are ordinary, highly liquid, market-traded instruments already flowing through the standard `allocate.py` deposit/allocation workflow exactly like any directly held equity — no distinguishing question remains. |
| "How has this fund historically behaved during major equity-market drawdown periods?" | **Rejected — structurally tautological for this population** | Each fund's own sealed `structural_role.role_category` (`broad_market_beta` for SPY; the developed-ex-US and emerging-market analogues for VEA/VWO) already establishes that these funds *are* broad equity-market beta by structural definition — asking how equity-market beta behaves during an equity-market drawdown restates the drawdown itself, not a distinguishing ETF-specific economic characteristic. Reintroducing this question here would also risk extending equity-methodology territory that the controlling directive reserves to the `VALUATION-####` series. |
| "Is this fund's historical relationship with inflation regimes established in citable literature?" | **Rejected — same tautology as the drawdown question** | An index-tracking broad-equity-beta fund's inflation sensitivity is, by construction, the same question as the broad equity market's own inflation sensitivity — not a distinguishing, fund-specific economic characteristic worth a dedicated axis. |
| "Is this fund's constituent look-through overlap with directly held equities economically significant?" | **Rejected — already the overlap model's own mechanism, not duplicated here** | Already computed structurally at the classification layer (`overlap_and_concentration`) and cross-referenced by `XASSET-0007`'s own sealed `issuer_overlap_etf_lookthrough` dimension (`computation_status: computed_from_existing_mechanism`). A second, narrative overlap judgment here would duplicate an already-governed mechanism, not supplement it. |
| "Does this fund's current market price suggest it is under/overvalued?" | **Rejected outright** | A valuation/price-target question, permanently prohibited by `CLAUDE.md`'s Guardrails, already forced `valuation_required` on every ETF's own sealed classification record. |

**Result: one substantive axis, `cost_and_tracking_quality_economic_significance`, plus `evidence_
quality`.** No compound axis and no second substantive axis are needed for this sub-population.

### 5.2 `cost_and_tracking_quality_economic_significance` (`etf` only, full field spec)

- **Purpose**: characterize whether an ETF's already-structurally-recorded expense ratio and (once
  measured) tracking quality are economically ordinary, elevated, or favorable for its own fund category
  — never a numeric cost-savings or hurdle-rate calculation.
- **Evidence inputs**: the instrument's own sealed ETF classification record (`structural_reference`, §3
  — consumed by reference, never restated); a sourced comparison to other funds in the same broad
  category (e.g. other broad-US-market-beta funds for `SPY`; other developed-ex-US funds for `VEA`; other
  emerging-market funds for `VWO`).
- **Keys**: `significance_category`, `rationale` (required, non-empty), `abstention_reason` (required
  only when `significance_category: unable_to_determine`).
- **Closed vocabulary**: `in_line_with_category` | `elevated_vs_category` | `favorable_vs_category` |
  `unable_to_determine`.
- **Abstention state**: no `not_applicable` — every ETF has some cost/tracking profile by definition.
  `unable_to_determine` is reserved for a genuine evidence gap.
- **Prohibited inference**: no numeric cost-savings figure; no claim that a lower-cost alternative should
  be substituted; no bare numeric-percent-shaped token anywhere in `rationale` (the already-sealed
  `expense_ratio_pct` figure may be cited by reference to the pinned structural record, never restated as
  a literal number in this schema's own free text — the identical no-carve-out rule `XASSET-0008` §G
  already applies to `GLD`).
- **Downstream use**: `economic_characterization_summary` field of the cross-asset handoff envelope
  (§4.6); a required future input to any cross-asset opportunity-cost synthesis (`XASSET-0001` §E).

## 6. Crypto-specific methodology (`BTC`, `ETH`, `SOL`)

### 6.1 Candidate questions evaluated → disposition table (full reasoning)

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "How has this coin historically behaved during major equity-market drawdown periods?" | **Kept** → `macro_behavioral_characterization.historical_equity_market_drawdown_behavior` | Genuinely new, single-asset, historically-grounded question — directly analogous to `GLD`'s own already-accepted `historical_equity_drawdown_behavior` sub-field, structurally distinct from `XASSET-0007`'s own `defensive_offset_interface` dimension (portfolio-level, still forced `not_yet_computable_interface_only`, §7 below). |
| "Is this coin's historical relationship with inflation regimes established in citable literature?" | **Kept** → `macro_behavioral_characterization.historical_inflation_sensitivity_narrative` | Directly analogous to `GLD`'s own already-accepted `historical_inflation_sensitivity` sub-field — the "digital gold"/inflation-hedge narrative attached to `BTC` specifically, and debated more broadly for crypto generally, is a genuinely citable, sourceable historical-literature question, distinct from a forward-looking forecast. |
| "Is this coin's cost/expense profile economically ordinary or notable for its category?" | **Rejected — no clean analog exists** | A cryptocurrency carries no expense ratio, fund sponsor, or tracking benchmark. The investor-facing cost that would be loosely analogous — brokerage spread, execution cost on Robinhood — is an execution-venue question entirely outside this instrument-level economic-assessment methodology's scope, not a property of the coin itself. Network-level transaction-fee/staking economics is already a classification-layer question (`economic_model.fee_accrual_applicable`/`staking_applicable`), not a new economic-assessment axis. |
| "How readily can this coin's position be deployed toward a future opportunity?" | **Rejected — already answered at the classification layer** | All three records' own sealed `liquidity_and_market_structure.liquidity_tier: high_liquidity` already answers this — identical reasoning to the ETF sub-population's own rejected deployability question (§5.1). |
| "What is this coin's network/protocol economic significance?" | **Rejected — already fully captured at the classification layer** | `network_fundamentals` (consensus mechanism, adoption trend) and `economic_model` (supply model, fee accrual, staking) already hold this territory in full; re-asking it here would duplicate, not supplement, the existing classification schema. |
| "Are `BTC`/`ETH`/`SOL` correlated with each other, and does that inform sizing or diversification within the crypto sleeve?" | **Rejected outright — a separate, future, bounded research charter's own question, not this design's** | Each record's own sealed `correlation_and_volatility.cross_coin_correlation_status: not_yet_measured` remains classification-layer territory, unresolved and untouched here. A genuine cross-coin correlation study, if ever performed, requires its own separate, bounded, pre-registered charter matching `MARGIN-0005`'s/`LADDER-0001`'s own precedent (hash-pinned protocol, pre-committed materiality threshold, no history-mining) — not authorized, designed, sketched, or implied by this filing. |
| "Does this coin's current market price suggest it is under/overvalued?" | **Rejected outright** | A valuation/price-target question, permanently prohibited by `CLAUDE.md`'s Guardrails, already forced `valuation_required` on every crypto record's own sealed classification record. |

**Result: one compound substantive axis, `macro_behavioral_characterization`, with two independently-
abstainable sub-fields, plus `evidence_quality`.**

### 6.2 `macro_behavioral_characterization` (`cryptocurrency` only, full field spec)

A closed, structurally required compound object with two independently-abstainable sub-fields, mirroring
`GLD`'s own `instrument_specific_economic_characterization` shape (which had three sub-fields — this
crypto-specific version has two, since the cost/tracking sub-field has no clean analog for a
cryptocurrency, per §6.1's own disposition table):

#### `historical_equity_market_drawdown_behavior`

- **Purpose**: a historically-grounded, **single-asset** characterization of this coin's own price
  behavior during major historical equity-market drawdown periods — explicitly not a portfolio-level
  diversification-benefit or correlation-with-the-current-Portfolio-HQ-portfolio computation.
- **Evidence inputs**: citable, dated, sourced historical market data or academic/industry-analysis
  material (§7 — not yet gathered).
- **Keys**: `behavior_category`, `rationale` (required, non-empty), `single_asset_disclosure` (required,
  non-empty — §7 below, the mandatory boundary statement), `abstention_reason` (required only when
  `behavior_category: unable_to_determine`).
- **Closed vocabulary**: `historically_uncorrelated_or_negatively_correlated` | `historically_mixed` |
  `historically_positively_correlated` | `unable_to_determine` — identical vocabulary to `GLD`'s own
  sub-field.
- **Prohibited inference**: no numeric correlation coefficient or beta of any kind; no claim about this
  coin's diversification benefit *to Portfolio-HQ's own current holdings* (that remains `XASSET-0007`'s
  `defensive_offset_interface` dimension's own job); no claim about this coin's correlation to `BTC`/
  `ETH`/`SOL` (that remains `correlation_and_volatility.cross_coin_correlation_status`'s own, still-
  unresolved classification-layer territory, §6.1).

#### `historical_inflation_sensitivity_narrative`

- **Purpose**: a historically-grounded, sourced characterization of this coin's documented (or disputed)
  relationship with inflation regimes — established, citable literature only, never a forecast.
- **Evidence inputs**: citable, dated, sourced historical/academic/industry-analysis material (§7 — not
  yet gathered).
- **Keys**: `sensitivity_category`, `rationale` (required, non-empty), `abstention_reason` (required only
  when `sensitivity_category: unable_to_determine`).
- **Closed vocabulary**: `historically_positively_associated` | `historically_mixed_or_inconsistent` |
  `historically_weakly_associated` | `unable_to_determine` — identical vocabulary to `GLD`'s own
  sub-field.
- **Prohibited inference**: no forward-looking inflation forecast of any kind; no numeric inflation-beta
  or correlation coefficient.

**Abstention state (whole compound axis)**: required, populated (never `not_applicable`) on every
`cryptocurrency` record — every coin has some historical behavioral character by definition, even if that
character is presently unknowable, in which case each sub-field independently supports `unable_to_
determine` with its own `abstention_reason`. One sub-field's abstention never cascades to the other.
`not_applicable: true` (literal, structural) is reserved for this axis's own absence on `etf` records
(where it is forbidden as an unknown key, not merely marked `not_applicable` — the axis simply does not
exist in an `etf` record's own schema shape).

## 7. Future research interface — six named, unanswered questions

This design identifies, but does not answer, one research question per instrument on the sole substantive
axis (or axis pair) each carries:

1. **`SPY`'s own cost/tracking-quality economic significance** (feeds `cost_and_tracking_quality_
   economic_significance`, §5.2) — requires a sourced comparison against other broad-US-market-beta ETFs.
2. **`VEA`'s own cost/tracking-quality economic significance** — requires a sourced comparison against
   other developed-ex-US ETFs.
3. **`VWO`'s own cost/tracking-quality economic significance** — requires a sourced comparison against
   other emerging-market ETFs.
4. **`BTC`'s, `ETH`'s, and `SOL`'s own historical behavior during major equity-market drawdown periods**
   (feeds `historical_equity_market_drawdown_behavior`, §6.2, one determination per coin) — requires
   sourced, dated historical market data or industry-analysis material.
5. **`BTC`'s, `ETH`'s, and `SOL`'s own defensible, sourced, long-horizon characterization of relationship
   to inflation regimes** (feeds `historical_inflation_sensitivity_narrative`, §6.2, one determination per
   coin) — requires citable historical/academic/industry-analysis literature.

None of these questions is answered by this design. A future content-authorization filing (§4.7 of the
decision file) would gather this evidence.

### Mandatory GLD/overlap-model non-duplication boundary (reused from `XASSET-0008` §E/§6)

Every future `BTC`/`ETH`/`SOL` `historical_equity_market_drawdown_behavior` sub-field must carry the
`single_asset_disclosure` field (§6.2) stating explicitly that the finding is single-asset and historical
only, and does **not** itself constitute, imply, or substitute for a computed whole-portfolio
diversification-benefit finding. That remains `XASSET-0007`'s own sealed `defensive_offset_interface` and
`crypto_correlation_interface` dimensions' job — both still forced `not_yet_computable_interface_only`
under `XASSET-0005` §6.2's unconditional rule.

## 8. Synthesis handoff and portfolio-selection boundary (light edit for population, §4.6 above)

Completing economic assessment for `SPY`, `VEA`, `VWO`, `BTC`, `ETH`, and `SOL` — even a fully populated,
zero-abstention set of six sealed records — **does not select the portfolio**. It creates evidence for a
later selection mechanism that does not yet exist. The full chain, restated from `XASSET-0001` §E and
`XASSET-0008` §L, unedited by this design:

> evidence (Company/Theme/relationship/classification Intelligence; ETF/crypto classification; functional
> doctrine; `GLD`/`CASH_LIKE_CAPITAL` economic assessment; **this design's own future instrument
> economic-assessment records**; overlap-model dimensions) → cross-asset opportunity-cost synthesis
> (`XASSET-0001` §E/§F, wholly undesigned) → an explicit, human-approved adoption decision → only then,
> governed IN/OUT portfolio membership, sleeve targets, and instrument targets.

This design occupies exactly one box in that chain — an evidence-supply box, six instruments wide. It does
not perform, shortcut, or imply any of the boxes after it.

## 9. Validator specification (for the future implementing PR)

A future implementation must build one dedicated validator module
(`instrument_economic_assessment_validator.py`, matching this repository's established one-schema-one-
validator-module norm) enforcing, at minimum:

1. **Exact population enforcement** — exactly six `instrument_id` values (`SPY`, `VEA`, `VWO`, `BTC`,
   `ETH`, `SOL`), no `GLD`, no `CASH_LIKE_CAPITAL`, no `DEBT_REDUCTION`, no `QQQ`, no seventh value of any
   kind.
2. **Closed schema at every level, rejecting extra keys, not just missing ones** — envelope, structural
   reference, `cost_and_tracking_quality_economic_significance`, `macro_behavioral_characterization` and
   both its sub-fields, `evidence_quality`, `cross_asset_handoff`, provenance source, manifest row (the
   `contender_registry_validator.py` MAJOR-finding lesson, §9.1 below).
3. **`asset_type`-conditional shape enforcement** — `cost_and_tracking_quality_economic_significance`
   required on `etf` only, forbidden on `cryptocurrency`; `macro_behavioral_characterization` required on
   `cryptocurrency` only, forbidden on `etf`; `asset_type` value must match the pinned `structural_
   reference`'s own `source_schema`.
4. **`structural_reference` enforcement** — a live recompute of the pinned record's hash via the correct
   `canonical_record_hash()` function selected by `asset_type` (read-only reuse of
   `etf_classification_validator`'s and `crypto_classification_validator`'s own already-existing,
   already-tested functions); `source_instrument_id` must equal the record's own `instrument_id`.
5. **No cross-schema field-name leakage** — a dedicated forbidden-key scan barring every equity-shaped,
   ETF-classification-shaped, crypto-classification-shaped, functional-doctrine-shaped, overlap-model-
   shaped, and `economic_assessment` (`GLD`/`CASH_LIKE_CAPITAL`)-shaped key name (`economic_role`,
   `capital_priority`, `risk_concentration`, `portfolio_role_ref`, `conviction`, `structural_role`,
   `constituent_exposure`, `overlap_and_concentration`, `structure_and_methodology`, `network_
   fundamentals`, `economic_model`, `custody_and_counterparty_risk`, `regulatory_and_structural_
   uncertainty`, `functional_role`, `hard_constraint_status`, `capital_use_type`, `deployability_and_
   optionality`, `instrument_specific_economic_characterization`, `analytical_subject`, `legacy_
   structural_references`, `dimension_id`, `dimension_type`) from appearing anywhere in an `instrument_
   economic_assessment` record.
6. **Zero numeric field anywhere** — a forbidden-key/forbidden-pattern scan for `expected_return`,
   `hurdle_rate`, `price_target`, `fair_value`, `correlation_coefficient`, `beta`, `target_pct`, `target_
   weight`, `opportunity_cost_score`, `ranking_score`, `allocation_pct`, `leverage_amount`, or any bare
   numeric-percent-shaped token — with no carve-out of any kind (stricter than the ETF classification
   framework's own `expense_ratio_pct` exception; the sealed fact remains referenceable only via the
   `structural_reference` hash pin, never restated as a literal number in this schema's own free text).
7. **No chart-evidence leakage** — the same term-list free-text scan every prior validator in this
   repository already uses.
8. **No directive/trading-language leakage** — a word-boundary-matched scan for the shared eight words
   (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`).
9. **No predictive-language leakage** — a dedicated, independent scan for forward-looking terms
   (`forecast`, `predict`, `expected to`, `will likely`, `projected`) inside `historical_equity_market_
   drawdown_behavior`'s and `historical_inflation_sensitivity_narrative`'s own free-text fields
   specifically.
10. **Crypto/overlap-model non-duplication check** — a dedicated scan confirming no `BTC`/`ETH`/`SOL`
    record's `historical_equity_market_drawdown_behavior` is represented as a computed portfolio-level
    correlation or diversification-benefit finding, and that `single_asset_disclosure` is present and
    non-empty on every populated (non-`unable_to_determine`) instance.
11. **Cross-coin-correlation non-leakage** — a dedicated scan rejecting any numeric correlation
    coefficient, or any claim that `BTC`/`ETH`/`SOL` are or are not correlated with each other, anywhere
    in any field of any record — a genuinely independent mechanism from check 6's own numeric-pattern
    scan, since this check is about a *claim*, not merely a *number* (the `TIER-0004`-derived lesson,
    §9.1).
12. **Evidence/provenance validation** — every `provenance.sources` entry carries a type and access-status
    field.
13. **Allocator/margin decoupling** — zero import coupling with `allocate.py`/`margin_state.py` in either
    direction.
14. **Abstention independently checked** — `unable_to_determine` requires a non-empty `abstention_reason`
    on every substantive axis/sub-field; `not_applicable` rejected everywhere except the one designed
    structural absence (§6.2's closing paragraph).
15. **`abstention_index` independently reconciled** — never a self-declared flag trusted alone; every
    genuine `unable_to_determine` value actually present in the record must have a corresponding
    `abstention_index` entry, and vice versa (the `etf_classification_validator.py` MINOR-1 /
    `reconciliation_validator.py` MINOR lesson, §9.1).
16. **Deterministic generation; protected-path isolation** — repeated runs against the same input produce
    byte-identical results; zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_
    lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/
    classification|companies|themes|relationships|etf_classification|crypto_classification|functional_
    doctrine|overlap_model|economic_assessment/` record (`GLD.yaml`/`CASH_LIKE_CAPITAL.yaml` included,
    byte-unedited), and every existing governance decision file.

### 9.1 Lessons explicitly carried forward from prior validator review history

- **Closed-schema checks must reject extra keys, not just missing ones**
  (`contender_registry_validator.py`'s own MAJOR finding) — point 2 above.
- **An independent second-stage check must use a materially different mechanism than the logic it
  verifies** (`TIER-0004`'s own dangling-reference correction) — the predictive-language scan (point 9),
  the crypto/overlap-model non-duplication scan (point 10), and the cross-coin-correlation non-leakage
  scan (point 11) must each be their own free-text pass, never a byproduct of the closed-vocabulary enum
  check.
- **A required envelope field needs its own independent presence/type check**
  (`etf_classification_validator.py`'s own MINOR-1 finding) — applies equally to `structural_reference`'s
  own required shape, not merely the substantive axes.
- **A self-declared flag is not a substitute for an independent scan**
  (`reconciliation_validator.py`'s own MINOR finding) — `abstention_index` must be independently checked
  against every genuine abstention actually present (point 15), never merely trusted as self-declared.
- **A population design can itself presuppose an unverified fact**
  (`XASSET-0008` §0's own finding, carried forward here) — this design's own §5.1/§6.1 disposition tables
  are written specifically to make explicit, for every candidate question, why it was kept or rejected —
  including questions (`deployability_and_optionality`, an ETF-drawdown-behavior axis) that a naive
  reuse of `GLD`'s own schema shape might otherwise have silently carried forward without re-examination.

## 10. Test specification (for the future implementing PR)

A future implementation's focused test suite must cover, at minimum, one test per item below:

- Happy-path record for each of the six instruments validates clean.
- Malformed envelope/axis schema (missing required field) rejected, for both asset types.
- Extra unknown key at envelope level and at every nested level rejected, for both asset types.
- Wrong `instrument_id` value (outside the closed six, including `GLD`, `CASH_LIKE_CAPITAL`, and `QQQ`)
  rejected.
- `asset_type` mismatched against `instrument_id`'s own real classification-layer asset type rejected.
- `cost_and_tracking_quality_economic_significance` present on a `cryptocurrency` record rejected;
  missing on an `etf` record rejected.
- `macro_behavioral_characterization` present on an `etf` record rejected; missing on a `cryptocurrency`
  record rejected.
- `structural_reference` hash independently verified against a live recompute — a synthetic stale-hash
  test for both `source_schema` values, and a live test against each of the six real sealed classification
  records once they exist.
- `structural_reference.source_schema`/`source_file` mismatched against `asset_type` rejected.
- Any cross-schema field name (equity, ETF classification, crypto classification, functional-doctrine,
  overlap-model, `GLD`/`CASH_LIKE_CAPITAL` economic-assessment) present anywhere rejected.
- Forbidden numeric-field leakage (each named term, individually, plus a bare numeric-percent token)
  rejected — no positive-acceptance test for any of them.
- Chart-terminology leakage (each term individually) rejected.
- Directive/trading-language leakage (each of the shared eight words individually) rejected, including a
  false-positive-guard test.
- Predictive-language leakage (each named term individually) rejected, scoped to the two crypto
  sub-fields.
- Crypto/overlap-model non-duplication: a synthetic `BTC`/`ETH`/`SOL` record whose `historical_equity_
  market_drawdown_behavior` rationale asserts a whole-portfolio diversification claim, or whose
  `single_asset_disclosure` is missing/empty, rejected.
- Cross-coin-correlation leakage: a synthetic record asserting `BTC` and `ETH` are (or are not) correlated
  with each other, in any field, rejected — plus a positive test confirming a record that discusses only
  its own single-asset historical behavior, without any cross-coin claim, is accepted.
- Abstention behavior: `unable_to_determine` without `abstention_reason` rejected on every substantive
  axis and sub-field; `not_applicable` used where the schema does not permit it rejected; a fully
  abstained record (both crypto sub-fields `unable_to_determine`, or the ETF axis `unable_to_determine`)
  accepted as sealed-eligible.
- `abstention_index` reconciliation: an `unable_to_determine` value with no corresponding
  `abstention_index` entry rejected; an `abstention_index` entry with no corresponding `unable_to_
  determine` value in the record rejected.
- Non-cascading abstention: a synthetic `BTC` record with `historical_equity_market_drawdown_behavior:
  unable_to_determine` and `historical_inflation_sensitivity_narrative` fully determined validates clean,
  and vice versa.
- Duplicate/missing/extra `instrument_id` entry within a population batch rejected.
- Deterministic output: two consecutive validator runs against identical input produce byte-identical
  results.
- Protected-path isolation: zero diff on every path named in §9 point 16, explicitly including
  `GLD.yaml`/`CASH_LIKE_CAPITAL.yaml` themselves (unreferenced by this schema, confirmed absent from any
  scan target — never modified).
- Allocator/margin import-coupling test: a static-analysis-style check confirming the future validator
  module imports neither `allocate.py` nor `margin_state.py`.

## 11. Objective preserved, not invented (unchanged discipline)

This design does not define, redefine, or narrow Portfolio-HQ's governing objective (`XASSET-0001` §A,
unedited). It supplies categorical, evidence-based facts a future cross-asset opportunity-cost synthesis
would need for six already-classified instruments, without itself computing an expected return, a
correlation coefficient, a hurdle rate, or a risk-adjusted comparison of any kind. The "next-dollar
opportunity-cost methodology" `XASSET-0001` §E/§A implies remains wholly undesigned by this artifact —
exactly as `XASSET-0002` §11, `XASSET-0005` §9, and `XASSET-0008` §13 already stated for their own
respective schemas, restated here for the same reason: this is a required future principal/governance
decision, not a byproduct of a design filing.
