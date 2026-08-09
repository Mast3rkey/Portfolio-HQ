# WS-0014 GLD/Cash-like-capital Economic Assessment Methodology — retained design artifact

**Filed under**: `XASSET-0008` (`governance/decisions/XASSET-0008-gld-cash-reserve-economic-assessment-methodology.md`)
**Date**: 2026-08-09
**Scope**: `XASSET-0005` §5 step 2's own restated sequence ("perform asset-appropriate valuation/economic
assessment — future, separate, undesigned") — restricted to two analytical subjects: `GLD` and
`CASH_LIKE_CAPITAL` (an analytical family/projection over the legacy `CASH`/`RESERVE` identifiers, per the
bounded correction in §0). Design only. No record is populated, no economic finding is stated for either
subject, and no `economic_assessment_readiness` value on any sealed functional-doctrine record is
superseded by this artifact.

This artifact is the full field-by-field methodology design. The decision file summarizes it and carries
the authorization/consequences text; this document is the retained detail, matching the
`TIER-0001`→`TIER-0002` and `XASSET-0001`→`XASSET-0005` supporting-artifact precedent.

---

## 0. Bounded correction (same day, this PR): CASH/RESERVE provenance and redesign

**This artifact's original submission** designed the closed question set (§3, as it then was) around
**three** independent population members — `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE` — sharing one schema,
with `RESERVE`'s functional-doctrine abstention preserved via a worked non-cascading-abstention example
and `CASH`'s own sealed `functional_role.role_category: operational_liquidity_float` implicitly treated as
settled ground.

**Before any further work, the controlling principal directed a read-only, repository-wide, full-history
provenance investigation** into whether `CASH` and `RESERVE` were ever established as genuinely distinct
economic concepts. Full findings are recorded in the decision file's own Bounded-correction section; the
governing facts, restated here because they drive this artifact's own schema redesign:

- `CASH` and `RESERVE` first appear together, simultaneously, in commit `b3afa70` (2026-07-31) — no
  earlier commit in the repository's full, unshallowed history (844 commits, back to the actual root
  commit) mentions either.
- Both rows' weights are sourced verbatim from an external, non-retained committee document
  (`Portfolio_HQ_Grand_Master_Architecture_v1_30.csv`, cited only by SHA-256) — its own internal rationale,
  if any, is not inspectable from this repository.
- Zero mechanical distinction exists anywhere in this repository's code: `allocate.py`/`levels.py` group
  `("reserve", "cash")` as one identical tuple in every conditional branch; `margin_state.py`,
  `gates.yaml`, and `issuer_lookthrough.yaml` carry no `RESERVE`-specific logic at all; neither is
  persisted as a tracked `holdings.yaml` balance.
- Zero principal-authorized text anywhere establishes a substantive distinction. The only prior attempts
  to characterize one (`CASH.yaml`'s own `operational_liquidity_float` determination; `XASSET-0005`'s
  supporting artifact's own "difference in role only" language) are themselves AI-authored inferences from
  the same sparse evidence base, not principal-sourced facts.

**The controlling principal's explicit decision**: `CASH` and `RESERVE` are not presently recognized as
distinct economic functions. Treat them as semantically equivalent, unresolved members of one cash-like
capital family unless and until a future, separately authorized, principal-approved decision establishes a
genuine distinction. The different labels and the different `target_pct` values (4.00%/1.00%) may not be
read as evidence of distinct purpose. No later AI-authored description may bootstrap itself into evidence
of a distinction.

**Resulting redesign, applied throughout this artifact**:

- The population (§3, formerly "§2") collapses from three independent members to **two analytical
  subjects**: `GLD` (unchanged) and `CASH_LIKE_CAPITAL` (new — an analytical family/projection, never a
  production concept).
- The closed question set (§4, formerly "§3") is restructured: `deployability_and_optionality` is now
  computed **once**, for the combined `CASH_LIKE_CAPITAL` family, never once per legacy identifier. The
  GLD-only compound axis (§4.3, formerly "§3.3") is entirely unaffected.
- The structural-reference mechanism (§5, formerly "§4") is redesigned for `CASH_LIKE_CAPITAL`: rather
  than one required pin into one sealed functional-doctrine record (the original per-member design), a
  future `CASH_LIKE_CAPITAL` record carries a **list of exactly two legacy structural references** — one
  into `CASH.yaml`, one into `RESERVE.yaml` — cited as provenance context only, never as content to copy
  or restate.
- The `RESERVE` section (§7, formerly "§6") is rewritten as "CASH/RESERVE as legacy structural
  identifiers — provenance only, no distinct interpretation," and a new validator rule (§11 point 15,
  formerly absent) mechanically forbids any future record from asserting a distinct `CASH`-versus-`RESERVE`
  purpose.
- GLD's own methodology (§4.3, §6 formerly "§5", §8 formerly "§7") is **entirely unaffected** by this
  correction.

This correction landed before any independent review occurred on this PR (zero reviews posted at
correction time) — a same-session, pre-review redesign responding to new principal-directed evidence, not
a post-review defect fix. Every section below reflects the corrected design directly; where a section is
unchanged from the original submission, it is marked so explicitly.

## 1. Why this design does not duplicate the equity valuation methodology work

`VALUATION-0001` designed a research charter comparing seven valuation-methodology families against seven
business-economics archetypes for the equity roster — a genuinely different problem shape than this one.
Three structural reasons this design does not, and should not, import that machinery (unaffected by the
§0 correction — the population shrinking from three members to two does not change this argument):

- **Population size and kind.** The equity study needed a 7×7 matrix because 27 companies span materially
  different business-economics archetypes requiring different methodology families. `GLD` and
  `CASH_LIKE_CAPITAL` are two fixed analytical subjects with no archetype-differentiation question to
  research between them.
- **Evidence shape.** GLD's economic characteristics (deployability, cost/tracking quality, historical
  inflation/drawdown behavior) and `CASH_LIKE_CAPITAL`'s own single deployability question are direct,
  sourceable, single-subject questions — closer in shape to `VALUATION-0004`'s RQ4 evidence-architecture
  design (define a schema for evidence a future session will gather) than to `VALUATION-0001`'s
  methodology-comparison charter.
- **No archetype taxonomy needed.** Nothing in this design needs an analogous taxonomy — `GLD` and
  `CASH_LIKE_CAPITAL` are each their own fixed category, no methodology-family selection question to
  resolve first.

**What this design does borrow from the `VALUATION-####` series, deliberately**: the design-then-
authorize-content separation; the closed, non-numeric, evidence-sufficiency-gated output vocabulary
discipline (`VALUATION-0002` §3's false-precision protections); and the explicit "this evidence does not
itself resolve the forced default" boundary (`VALUATION-0002` §6.3(b)'s own precise reading of what
"closes" a research gap — merge to `main`, not merely accepted content). None of the equity-specific
content (archetype categories, methodology families, the 49-cell matrix) is imported.

## 2. Method: reuse general classification hygiene, do not reuse asset-shaped fields (unchanged by §0)

Same starting question `TIER-0001`/`TIER-0002` and `XASSET-0002`/`XASSET-0005` all asked: *does this field
exist in currently-authoritative repository evidence, and does representing it as a standing fact
materially improve a future decision that today requires manual cross-referencing or is not represented at
all?* Two structural moves carry over from every prior framework in this repository:

- **Narrative-judgment fields are kept separate from mechanically-computed fields** — the same split
  `TIER-0002`, `XASSET-0002`, and `XASSET-0005` each already applied, reused here for
  `deployability_and_optionality`/`instrument_specific_economic_characterization` versus `evidence_
  quality`.
- **Evidence quality and abstention are per-field disciplines, not a bolted-on axis** — the same
  `not_applicable`/`unable_to_determine` two-state discipline `TIER-0004`/`XASSET-0002`/`XASSET-0005`
  already established.

One structural move is reused, not new, from `XASSET-0005`: a **cross-schema reference-by-hash
mechanism** (§5) — this design needs it twice: once for `GLD` (pinning into its own sealed ETF record,
exactly as `GLD_DEFENSIVE_ROLE.yaml` already does) and, as of the §0 correction, once for
`CASH_LIKE_CAPITAL` (pinning into **two** sealed functional-doctrine records as provenance-only legacy
references, a new variant of the same mechanism — a *list* of references rather than a single required
pin, since this family has no one sealed record of its own to anchor to).

## 3. Population — two analytical subjects, `DEBT_REDUCTION` explicitly excluded (redesigned by §0)

### `GLD` (unchanged)

A single-instrument economic-assessment subject referencing GLD's own sealed ETF structural record
(`intelligence/etf_classification/GLD.yaml`) and functional-doctrine record
(`intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml`) by hash pin (§5).

### `CASH_LIKE_CAPITAL` (new, replacing the original design's separate `CASH`/`RESERVE` members)

An **analytical family/projection**, not a new target row, not a new investable symbol, and not created in
`targets.yaml`, `holdings.yaml`, allocator code, or any production configuration. It represents the
unresolved, combined analytical treatment of the two legacy structural identifiers `CASH` and `RESERVE` —
reused as provenance/reference sources only (§5, §7), never independently interpreted as two separate
economic subjects. `CASH_LIKE_CAPITAL` exists exclusively inside this future economic-assessment
methodology's own schema; it has no corresponding sealed functional-doctrine record of its own (`CASH.yaml`
and `RESERVE.yaml` remain the only sealed records, each an independent, unedited, pre-existing artifact
this new schema references but does not supersede).

### `DEBT_REDUCTION` — out of scope (unchanged by §0)

Its own economic-assessment gap (`avoided_borrowing_cost_readiness` / `survivability_and_buffer_benefit_
readiness`, `XASSET-0005` §3.5) belongs to the separately governed margin/leverage-policy track (the 1.8x
leverage cap, the 30% buffer floor, `MARGIN-0005`'s own bounded research charter) — not touched, not
reopened, not weakened by this design. No equity, ETF beyond `GLD`, or cryptocurrency economic assessment
is addressed.

## 4. The closed question set — one shared axis, one GLD-only compound axis (redesigned by §0)

### 4.1 Candidate questions evaluated → disposition table (revised)

| Candidate question | Disposition | Reasoning |
|---|---|---|
| "How readily can this capital use be deployed toward a future opportunity?" | **Kept** → `deployability_and_optionality` axis (§4.2), both `GLD` and `CASH_LIKE_CAPITAL` | Genuinely new — distinct from the already-sealed `liquidity_character` axis on the legacy functional-doctrine records (which asks "is this convertible to cash," already answered `immediately_liquid` for both `CASH` and `RESERVE`) — this asks "does being in this state preserve or cost anything in the ability to act on a future opportunity." For `CASH_LIKE_CAPITAL`, computed **once**, for the combined family, never once per legacy identifier — the §0 correction's own structural change from the original per-member design. |
| "What is this capital use's functional role?" | **Not re-asked** — already sealed on the legacy records, and not asked at the `CASH_LIKE_CAPITAL` level at all | `CASH.yaml`'s and `RESERVE.yaml`'s own `functional_role` values are not re-derived, not restated, and — per the §0 correction — not treated as authoritative for `CASH_LIKE_CAPITAL`'s own analysis either. |
| "Is `CASH_LIKE_CAPITAL` functionally distinct from GLD?" | **Rejected outright, structurally impossible to ask under this design** | `GLD` is a priced, market-traded instrument with its own structural facts; `CASH_LIKE_CAPITAL` is a non-instrument capital-use family. The two-subject population itself (§3) already treats them as categorically different in kind — no comparison axis is needed or authorized. |
| "Is `CASH` functionally distinct from `RESERVE`?" | **Explicitly, permanently out of scope for this methodology** — the exact question the §0 correction resolved by principal decision, not by this design | The controlling principal's decision (§0) is that no repository evidence supports such a distinction today. This design does not ask the question in any form, under any field name — `CASH_LIKE_CAPITAL`'s combined treatment (§3) *is* the design's answer to how this question is handled: by not asking it. A dedicated future validator rule (§11 point 15) mechanically forbids any record from smuggling an answer back in via free text. |
| "Is GLD's cost/tracking-quality economically ordinary or notable for its category?" | **Kept** → `instrument_specific_economic_characterization.cost_and_tracking_economic_significance` (§4.3), `GLD` only | Unaffected by §0 — GLD's own sealed ETF classification record already carries `cost_and_tracking_quality.expense_ratio_pct: 0.40` and `tracking_quality_category: not_yet_measured` as structural facts; no categorical judgment about whether that cost profile is ordinary, elevated, or favorable exists anywhere. |
| "Is gold's historical relationship with inflation regimes established in citable literature?" | **Kept** → `instrument_specific_economic_characterization.historical_inflation_sensitivity` (§4.3), `GLD` only | Unaffected by §0. |
| "How has gold historically behaved during major equity-market drawdown periods?" | **Kept** → `instrument_specific_economic_characterization.historical_equity_drawdown_behavior` (§4.3), `GLD` only | Unaffected by §0 — single-asset, historically-grounded characterization, structurally distinct from `XASSET-0007`'s own `defensive_offset_interface` dimension (§6). |
| "Does GLD's current market price or realized return over some period suggest it is under/overvalued?" | **Rejected outright** | Unaffected by §0 — a valuation/price-target question, permanently prohibited by CLAUDE.md's Guardrails, already forced `valuation_required` on GLD's own sealed ETF record. |
| "What is `CASH_LIKE_CAPITAL`'s expected return relative to deploying the same dollars into equities?" | **Rejected outright** | Unaffected by §0 — a hurdle-rate/expected-return comparison, the cross-asset opportunity-cost synthesis's own job (`XASSET-0001` §E), not this design's. |

**Result: one shared substantive axis** (`deployability_and_optionality`, computed once per analytical
subject — twice total, once for `GLD` and once for `CASH_LIKE_CAPITAL`) **plus one GLD-only compound
axis** (`instrument_specific_economic_characterization`, `not_applicable: true` for `CASH_LIKE_CAPITAL`)
**plus `evidence_quality`** on both — a smaller, tighter shared-axis set than the original three-member
design's own "three shared axes" (the original design's `structural_reference_functional_doctrine` field
is retained but is now population-conditional in shape, §5, not a uniform third axis; the original design
had no separate axis this correction removes outright — the reduction from three population members to
two analytical subjects is the structural change, not a reduction in per-subject question depth).

### 4.2 `deployability_and_optionality` (both `GLD` and `CASH_LIKE_CAPITAL`, substantive axis)

- **Purpose**: record how readily this analytical subject can be deployed toward a future opportunity via
  the existing deposit/allocation workflow (`CLAUDE.md`'s own Workflow section — deposit,
  `allocate.py --cash` or `--margin`, present recommendation, execute manually) — the *optionality value*
  of holding this capital use, distinct from `liquidity_character`'s already-answered "is it convertible
  to cash" question on the legacy functional-doctrine records.
- **Evidence inputs**: `CLAUDE.md`'s own Workflow section (deposit cycle, $25 minimum lot, manual
  execution) and Portfolio Doctrine (the allocator's own `RESERVE`/`CASH` "never a buy candidate,
  definitionally satisfied" treatment, cited as a **shared mechanical fact about the family**, never
  parsed apart into a per-legacy-identifier claim) — structural facts about *how* deployment happens,
  never a live dollar figure or a claim about *whether* deployment is currently advisable.
- **Closed vocabulary**: `high_optionality_low_friction` | `moderate_optionality` |
  `low_optionality_or_structurally_constrained` | `unable_to_determine` (with required `abstention_
  reason`).
- **Abstention state**: no `not_applicable` — both analytical subjects have some deployability character
  by definition (even a genuinely constrained one is a determinate value, not an absence).
  `unable_to_determine` is reserved for a genuine evidence gap.
- **Prohibited inference**: no expected-return comparison against deploying the same dollars elsewhere; no
  target allocation percentage; no ranking against the other analytical subject's own optionality; no
  claim about whether deployment is *currently* advisable; **and, specific to `CASH_LIKE_CAPITAL`, no
  claim that `CASH` and `RESERVE` individually warrant a different determination on this axis** — the
  axis is computed once, for the family, full stop.
- **`CASH_LIKE_CAPITAL`-specific note, replacing the original design's RESERVE non-cascading worked
  example**: because this axis is asked of the combined family, not of `CASH` and `RESERVE` separately,
  there is no per-legacy-identifier abstention to cascade into or out of. `RESERVE.yaml`'s own sealed
  `functional_role` abstention remains exactly as sealed, unaffected by whatever this axis eventually
  determines for `CASH_LIKE_CAPITAL`.
- **Downstream use**: `deployability_summary` field of the cross-asset handoff envelope (§9); a required
  future input to any cross-asset opportunity-cost synthesis (`XASSET-0001` §E).

### 4.3 `instrument_specific_economic_characterization` (`GLD` only; `not_applicable: true` for `CASH_LIKE_CAPITAL`) — unaffected by §0

**Purpose**: `GLD` is the only analytical subject that references a priced, market-traded instrument with
its own independent economic history — `CASH_LIKE_CAPITAL` is an account-state analytical family, not an
instrument with a cost structure, a tracking benchmark, or a historical price series. This compound axis
exists to hold the GLD-specific economic questions §4.1's disposition table identifies.

A closed, structurally required compound object with three independently-abstainable sub-fields:

#### `cost_and_tracking_economic_significance`

- **Purpose**: characterize whether GLD's already-structurally-recorded expense ratio (0.40%, per
  `intelligence/etf_classification/GLD.yaml`) and (once measured) tracking quality are economically
  ordinary, elevated, or favorable for its fund category — never a numeric cost-savings or hurdle-rate
  calculation.
- **Evidence inputs**: GLD's own sealed ETF classification record (`structural_reference_etf_
  classification`, §5 — consumed by reference, never restated); a sourced comparison to other
  physical-gold-backed or comparable commodity-ETF expense ratios.
- **Closed vocabulary**: `in_line_with_category` | `elevated_vs_category` | `favorable_vs_category` |
  `unable_to_determine`.
- **Prohibited inference**: no numeric cost-savings figure; no claim that a lower-cost alternative should
  be substituted.

#### `historical_inflation_sensitivity`

- **Purpose**: a historically-grounded, sourced characterization of gold's documented relationship with
  inflation regimes — established literature only, never a forecast.
- **Evidence inputs**: citable, dated, sourced historical/academic material (§8 — not yet gathered).
- **Closed vocabulary**: `historically_positively_associated` | `historically_mixed_or_inconsistent` |
  `historically_weakly_associated` | `unable_to_determine`.
- **Prohibited inference**: no forward-looking inflation forecast of any kind; no numeric inflation-beta or
  correlation coefficient.

#### `historical_equity_drawdown_behavior`

- **Purpose**: a historically-grounded, **single-asset** characterization of gold's own price behavior
  during major historical equity-market drawdown periods — explicitly not a portfolio-level
  diversification-benefit or correlation-with-the-current-Portfolio-HQ-portfolio computation.
- **Evidence inputs**: citable, dated, sourced historical market data or academic material (§8 — not yet
  gathered).
- **Closed vocabulary**: `historically_uncorrelated_or_negatively_correlated` | `historically_mixed` |
  `historically_positively_correlated` | `unable_to_determine`.
- **Prohibited inference**: no numeric correlation coefficient or beta of any kind; no claim about GLD's
  diversification benefit *to Portfolio-HQ's own current holdings* (that is `XASSET-0007`'s
  `defensive_offset_interface` dimension — see §6's mandatory disclosure requirement).

**Abstention state (whole compound axis)**: `not_applicable: true` (literal, structural) on
`CASH_LIKE_CAPITAL` — the axis simply does not exist for a non-instrument analytical family. On `GLD`,
each of the three sub-fields independently supports `unable_to_determine` with its own `abstention_
reason` — one sub-field's abstention never cascades to the other two.

### 4.4 `evidence_quality` (unchanged)

Identical design to every prior framework's own axis (`comprehensive`/`partial`/`limited` vocabulary,
required `thesis_uncertainty_statement`). Not restated here to avoid duplication.

## 5. Structural references — reuse, never duplicate; redesigned for `CASH_LIKE_CAPITAL`

### `GLD` (unchanged)

Two independent, narrowly-scoped content-hash pins, both consuming an existing sealed record's public hash
function:

- `structural_reference_etf_classification`: pins to `intelligence/etf_classification/GLD.yaml` via
  `etf_classification_validator.canonical_record_hash()` (`etf_classification_validator.py:322`).
- `structural_reference_functional_doctrine`: pins to `intelligence/functional_doctrine/GLD_DEFENSIVE_
  ROLE.yaml` via `functional_doctrine_validator.canonical_record_hash()`
  (`functional_doctrine_validator.py:355`).

Both enforce a live hash recompute on every validator run, rejecting a stale reference — mirroring
`GLD_DEFENSIVE_ROLE.yaml`'s own identical enforcement of its own pin into `GLD.yaml`. None of the ETF
framework's own six axis key names may appear duplicated as a re-derived value anywhere in an
`economic_assessment` record for `GLD` — consumed by reference only.

### `CASH_LIKE_CAPITAL` (redesigned by §0)

The original design gave each of `CASH` and `RESERVE` its own single, required
`structural_reference_functional_doctrine` pin — a per-member mechanism that presupposed each was its own
independently meaningful subject. That presupposition is exactly what the §0 correction found unsupported.
The corrected mechanism:

- `legacy_structural_references`: a **list of exactly two entries**, one for `CASH` and one for `RESERVE`,
  each shaped identically to `GLD`'s own `structural_reference_functional_doctrine` object
  (`source_capital_use_type`, `source_schema: "functional_doctrine"`, `source_file`, `referenced_content_
  sha256` — computed via `functional_doctrine_validator.canonical_record_hash()`, the same already-
  existing, already-tested function `GLD`'s own pin reuses).
- **Purpose, explicitly stated**: these two pins exist **solely so a future reader can trace which legacy
  identifiers this analytical family combines** — provenance, not content import. Neither pinned record's
  own field values (including `CASH.yaml`'s own `functional_role.role_category:
  operational_liquidity_float` or `RESERVE.yaml`'s own `unable_to_determine`) may be copied, restated,
  paraphrased, or treated as a `CASH_LIKE_CAPITAL`-level finding anywhere in the record.
- **Enforcement**: both pins independently, live-recompute their target's hash on every validator run
  (rejecting either as stale exactly as `GLD`'s own mechanism does); a dedicated forbidden-content scan
  (§11 point 15) rejects any `CASH_LIKE_CAPITAL` field whose free text restates either legacy record's own
  `functional_role` value or asserts a distinction between the two.
- **Why a list, not a single pin**: `CASH_LIKE_CAPITAL` has no sealed record of its own to anchor a single
  pin to — it is a projection over two pre-existing, independent, unedited records. A list of exactly two
  is the smallest structurally honest representation of "this family combines these two legacy
  identifiers," without inventing a third, phantom "combined" sealed record that does not exist.

**None of the ETF framework's own six axis key names, and none of the functional-doctrine schema's own
seven axis/envelope key names** (`functional_role`, `hard_constraint_status`, `economic_assessment_
readiness`, `liquidity_character`, `capital_preservation_character`, `freshness_state`, `capital_use_
type`) may appear duplicated as a re-derived value anywhere inside a `CASH_LIKE_CAPITAL`
`economic_assessment` record.

## 6. GLD / overlap-model ownership boundary — mandatory disclosure (unchanged by §0)

`historical_equity_drawdown_behavior` (§4.3) and any future portfolio-level defensive-offset question sit
close enough together to require an explicit, structural boundary, not merely a naming convention:

| Question | Owner | Shape |
|---|---|---|
| "How has gold itself historically behaved during major equity-market drawdown episodes?" | **This design** (`historical_equity_drawdown_behavior`) | Single-asset, historical, categorical. |
| "Does GLD provide a measurable diversification benefit *to Portfolio-HQ's own current portfolio*?" | `XASSET-0007`'s `defensive_offset_interface` dimension (overlap model, content authorized, not yet populated) | Portfolio-level, forced `not_yet_computable_interface_only` today, per `XASSET-0005` §6.2's own unconditional rule. |

**Every future `GLD` economic-assessment record must carry an explicit disclosure statement** stating that
`historical_equity_drawdown_behavior`'s finding is single-asset and historical only, and does **not**
itself constitute, imply, or substitute for a computed whole-portfolio diversification-benefit finding —
that remains `defensive_offset_interface`'s own, separate, still-forced-abstention job.

## 7. `CASH`/`RESERVE` as legacy structural identifiers — provenance only, no distinct interpretation (rewritten by §0)

`RESERVE.yaml`'s sealed `functional_role.role_category: unable_to_determine` is **not resolved,
narrowed, or worked around by this design**. `CASH.yaml`'s sealed `functional_role.role_category:
operational_liquidity_float` is likewise **not treated as settled ground** for `CASH_LIKE_CAPITAL`'s own
analysis — per the §0 correction, that determination is an AI-derived inference, not a principal-sourced
fact.

**What this design does:**

1. Treats `CASH` and `RESERVE` as **one combined, undifferentiated analytical family**
   (`CASH_LIKE_CAPITAL`) for every substantive question this methodology asks — never split into a
   per-legacy-identifier answer.
2. Cites both legacy records structurally (§5), never re-derives or restates either one's own content.
3. Prohibits, mechanically (§11 point 15), any future record from asserting — in any field, in any
   free-text rationale, under any framing — that `CASH` and `RESERVE` warrant different treatment, or that
   their different `target_pct` values (4.00%/1.00%) are evidence of distinct purpose.
4. Preserves `RESERVE.yaml`'s own abstention exactly as sealed — never resolved, never inferred around,
   never bypassed by proxy through a different field name.
5. Does not create a policy answer merely to make a record complete — a `CASH_LIKE_CAPITAL` record with
   `deployability_and_optionality: unable_to_determine` is a fully valid, complete, sealed record under
   this methodology.

**What this design does not do**: it does not perform, invite, schedule, or presume a future resolution of
whether `CASH` and `RESERVE` are actually distinct, and it does not perform, invite, schedule, or presume a
future consolidation of the two `targets.yaml` rows — both remain open, separately-governed, future
questions (decision file §N), disclosed but not answered here.

## 8. Future research interface — three named, unanswered questions (unchanged by §0)

This design identifies, but does not answer, three research questions a future implementing session would
need to address before it could populate `instrument_specific_economic_characterization`'s sub-fields with
anything beyond `unable_to_determine`:

1. **GLD's own historical behavior during major equity-market drawdown periods** (feeds `historical_
   equity_drawdown_behavior`, §4.3) — requires sourced, dated historical market data or academic material;
   not gathered by this design.
2. **GLD's realized tracking quality against its own benchmark** (the LBMA Gold Price PM, per `GLD.yaml`'s
   own sealed `structure_and_methodology.benchmark_type`) — feeds `cost_and_tracking_economic_
   significance`, §4.3; not gathered by this design.
3. **A defensible, sourced, long-horizon characterization of gold's relationship to inflation regimes**
   (feeds `historical_inflation_sensitivity`, §4.3) — requires citable historical/academic literature; not
   gathered by this design.

None of these three questions concerns `CASH_LIKE_CAPITAL` — its own future research needs, if any (beyond
the one `deployability_and_optionality` axis, which this design already fully specifies), are not
identified here.

## 9. Synthesis handoff — categorical evidence only (light edit for population)

Every future `economic_assessment` record carries a `cross_asset_handoff` envelope object:

| Field | Sourced from | Explicitly excluded from this or any field in this envelope |
|---|---|---|
| `deployability_summary` | `deployability_and_optionality` (verbatim copy) | — |
| `instrument_specific_summary` | `instrument_specific_economic_characterization` (verbatim copy, or `not_applicable` marker for `CASH_LIKE_CAPITAL`) | — |
| `evidence_quality_summary` | `evidence_quality.primary_source_coverage` (verbatim copy) | — |
| `uncertainty_summary` | the envelope's own field, not re-derived | — |

**Absolutely excluded from this envelope, and from every other field in this schema, at any level**:
target weights or ranges; a rank or ranking of any kind; an IN/OUT portfolio-selection determination; a
buy/sell/hold/trim/exit/wait/stage signal or directive of any kind; a sleeve percentage or Level 1/Level 2
allocation figure; a trade-timing recommendation; a leverage amount; **and, specific to
`CASH_LIKE_CAPITAL`, any claim of distinct `CASH`-versus-`RESERVE` purpose.**

**The future synthesis, not this design, compares competing uses of capital.**

## 10. Portfolio-selection boundary — restated, binding (light edit for population)

Completing economic assessment for `GLD` and `CASH_LIKE_CAPITAL` — even a fully populated, zero-abstention
pair of sealed records — **does not select the portfolio**. It creates evidence for a later selection
mechanism that does not yet exist. The full chain, restated from `XASSET-0001` §E and `XASSET-0005` §5,
unedited by this design:

> evidence (Company/Theme/relationship/classification Intelligence; ETF/crypto classification; functional
> doctrine; **this design's own future economic-assessment records**; overlap-model dimensions) →
> cross-asset opportunity-cost synthesis (`XASSET-0001` §E/§F, wholly undesigned) → an explicit,
> human-approved adoption decision → only then, governed IN/OUT portfolio membership, sleeve targets, and
> instrument targets.

This design occupies exactly one box in that chain — an evidence-supply box, two subjects wide (reduced
from three by the §0 correction). It does not perform, shortcut, or imply any of the boxes after it — and,
per §0, it does not perform, shortcut, or imply a resolution of whether `CASH` and `RESERVE` are distinct.

## 11. Validator specification (for the future implementing PR) — revised for two-subject population

A future implementation must build one dedicated validator module (`economic_assessment_validator.py`,
matching this repository's established one-schema-one-validator-module norm) enforcing, at minimum:

1. **Exact population enforcement** — exactly two `analytical_subject` values (`GLD`, `CASH_LIKE_
   CAPITAL`), no `CASH` or `RESERVE` as a standalone `analytical_subject` value, no `DEBT_REDUCTION`, no
   third value.
2. **Closed schema at every level, rejecting extra keys, not just missing ones** — envelope, both
   structural-reference shapes (`GLD`'s two single pins; `CASH_LIKE_CAPITAL`'s two-entry
   `legacy_structural_references` list), `instrument_specific_economic_characterization` and its three
   sub-fields, `deployability_and_optionality`, `evidence_quality`, `cross_asset_handoff` (the
   `contender_registry_validator.py` MAJOR-finding lesson, §11.1 below).
3. **`analytical_subject`-conditional shape enforcement** — the two ETF/functional-doctrine single pins and
   the populated (non-`not_applicable`) form of `instrument_specific_economic_characterization` required on
   `GLD` only; the two-entry `legacy_structural_references` list required on `CASH_LIKE_CAPITAL` only,
   forbidden on `GLD`.
4. **`legacy_structural_references` shape enforcement** — exactly two entries on `CASH_LIKE_CAPITAL`, one
   with `source_capital_use_type: "CASH"`, one with `source_capital_use_type: "RESERVE"` — no duplicate,
   no third entry, no missing entry.
5. **No cross-schema field-name leakage** — a dedicated forbidden-key scan barring every equity-shaped,
   ETF-shaped, crypto-shaped, functional-doctrine-shaped, or overlap-model-shaped key name from appearing
   anywhere in an `economic_assessment` record (full list matches the original design's own §7 point 4,
   unaffected by §0).
6. **Zero numeric field anywhere** — a forbidden-key/forbidden-pattern scan for `expected_return`,
   `hurdle_rate`, `price_target`, `fair_value`, `correlation_coefficient`, `beta`, `target_pct`, `target_
   weight`, `opportunity_cost_score`, `ranking_score`, `allocation_pct`, `leverage_amount`, or any bare
   numeric-percent-shaped token — with no carve-out of any kind.
7. **`structural_reference_functional_doctrine`/`structural_reference_etf_classification` enforcement
   (`GLD`)** — required shape check; a live recompute of each pinned record's hash via the appropriate
   `canonical_record_hash()` function (read-only reuse).
8. **`legacy_structural_references` enforcement (`CASH_LIKE_CAPITAL`)** — a live recompute of both `CASH.
   yaml`'s and `RESERVE.yaml`'s own hashes via `functional_doctrine_validator.canonical_record_hash()`
   (read-only reuse), reconciled against each entry's own `referenced_content_sha256`.
9. **No chart-evidence leakage** — the same term-list free-text scan every prior validator in this
   repository already uses.
10. **No directive/trading-language leakage** — a word-boundary-matched scan for the shared eight words
    (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`).
11. **No predictive-language leakage** — a dedicated, independent scan for forward-looking terms
    (`forecast`, `predict`, `expected to`, `will likely`, `projected`) inside `historical_inflation_
    sensitivity`'s and `historical_equity_drawdown_behavior`'s own free-text fields specifically.
12. **Overlap-model non-duplication check** — a dedicated scan confirming no `GLD` record's `historical_
    equity_drawdown_behavior` sub-field is represented as a computed portfolio-level correlation or
    diversification-benefit finding.
13. **Evidence/provenance validation** — every `provenance.sources` entry carries a type and access-status
    field.
14. **Allocator/margin decoupling** — zero import coupling with `allocate.py`/`margin_state.py` in either
    direction.
15. **No `CASH`-versus-`RESERVE`-distinction leakage (new, added by §0)** — a dedicated, independent
    free-text scan across every `CASH_LIKE_CAPITAL` field (particularly `deployability_and_optionality`'s
    own rationale and `uncertainty_summary`) rejecting any claim, however hedged, that `CASH` and `RESERVE`
    individually warrant different treatment, serve different purposes, or that their different `target_
    pct` values are meaningful as evidence — including patterns like "RESERVE functions as," "CASH is used
    for, while RESERVE," "the 4% reserve suggests," or equivalent. This scan must be a materially
    independent mechanism from the `legacy_structural_references` hash-reconciliation check (point 8) —
    the historical lesson `TIER-0004`'s own correction history already established (§11.1).
16. **Deterministic generation; protected-path isolation** — repeated runs against the same input produce
    byte-identical results; zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_
    lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, every existing `intelligence/
    classification|companies|themes|relationships|etf_classification|crypto_classification|functional_
    doctrine/` record (`CASH.yaml`/`RESERVE.yaml` included, unedited), and every existing governance
    decision file.

### 11.1 Lessons explicitly carried forward from prior validator review history

- **Closed-schema checks must reject extra keys, not just missing ones**
  (`contender_registry_validator.py`'s own MAJOR finding) — point 2 above.
- **An independent second-stage check must use a materially different mechanism than the logic it
  verifies** (`TIER-0004`'s own dangling-reference correction) — the predictive-language scan (point 11),
  the overlap-model non-duplication scan (point 12), and the new distinct-purpose-claim scan (point 15)
  must each be their own free-text pass, never a byproduct of the closed-vocabulary enum check.
- **A required envelope field needs its own independent presence/type check**
  (`etf_classification_validator.py`'s own MINOR-1 finding) — applies equally to `CASH_LIKE_CAPITAL`'s own
  two-entry `legacy_structural_references` list, not only to `GLD`'s single pins.
- **A self-declared flag is not a substitute for an independent scan**
  (`reconciliation_validator.py`'s own MINOR finding) — `not_applicable: true` on `instrument_specific_
  economic_characterization` for `CASH_LIKE_CAPITAL` must be independently checked against `analytical_
  subject`, never merely trusted as self-declared.
- **A population design can itself presuppose an unverified fact** (this artifact's own §0 finding, newly
  disclosed here for future designers) — the original three-member population design presupposed `CASH`
  and `RESERVE` were separately meaningful subjects without ever verifying that against repository
  provenance. A future schema design that introduces a population of independently-assessed subjects
  should confirm each subject's own independent standing is actually supported by evidence, not merely by
  the existence of separate config rows or separate sealed records.

## 12. Test specification (for the future implementing PR) — revised for two-subject population

A future implementation's focused test suite must cover, at minimum, one test per item below:

- Happy-path record for `GLD` and for `CASH_LIKE_CAPITAL` each validates clean.
- Malformed envelope/axis schema (missing required field) rejected, for both.
- Extra unknown key at envelope level and at every nested level rejected, for both.
- Wrong `analytical_subject` value (outside the closed two, including bare `CASH` or `RESERVE` as a
  standalone value, and `DEBT_REDUCTION`) rejected.
- `legacy_structural_references` present on `GLD` rejected; missing, containing fewer/more than two
  entries, containing a duplicate `source_capital_use_type`, or missing either `CASH`/`RESERVE` entry on
  `CASH_LIKE_CAPITAL` rejected.
- `structural_reference_etf_classification`/`structural_reference_functional_doctrine` missing on `GLD`
  rejected; present on `CASH_LIKE_CAPITAL` rejected.
- `instrument_specific_economic_characterization` populated (non-`not_applicable`) on `CASH_LIKE_CAPITAL`
  rejected; `not_applicable: true` on `GLD` rejected (must be a populated compound object there).
- All structural-reference hashes (`GLD`'s two, `CASH_LIKE_CAPITAL`'s two) independently verified against a
  live recompute — a synthetic stale-hash test for each, and a live test against the real sealed records
  once they exist.
- Any cross-schema field name (equity, ETF, crypto, functional-doctrine, overlap-model) present anywhere
  rejected.
- Forbidden numeric-field leakage (each named term, individually) rejected — no positive-acceptance test.
- Chart-terminology leakage (each term individually) rejected.
- Directive/trading-language leakage (each of the shared eight words individually) rejected, including a
  false-positive-guard test.
- Predictive-language leakage (each named term individually) rejected, scoped to the two GLD sub-fields.
- Overlap-model non-duplication: a synthetic `GLD` record whose `historical_equity_drawdown_behavior`
  rationale asserts a whole-portfolio diversification claim without the required single-asset disclosure
  rejected.
- **`CASH`-versus-`RESERVE`-distinction leakage (new)**: a synthetic `CASH_LIKE_CAPITAL` record whose
  `deployability_and_optionality` rationale, or `uncertainty_summary`, asserts any of the named distinct-
  purpose patterns (point 15's own examples, each tested individually) rejected — plus a positive test
  confirming a record that cites both legacy identifiers neutrally, without asserting a distinction, is
  accepted.
- Abstention behavior: `unable_to_determine` without `abstention_reason` rejected on every substantive
  axis and sub-field; `not_applicable` used where the schema does not permit it rejected; a fully abstained
  record accepted as sealed-eligible.
- Non-cascading abstention (revised): a synthetic `CASH_LIKE_CAPITAL` record with `deployability_and_
  optionality` determined validates clean regardless of `RESERVE.yaml`'s own separately-sealed
  `functional_role` abstention — this test asserts the schema imposes no cross-schema cascade, not
  anything about `RESERVE.yaml`'s own content.
- Duplicate/missing/extra `analytical_subject` entry within a population batch rejected.
- Deterministic output: two consecutive validator runs against identical input produce byte-identical
  results.
- Protected-path isolation: zero diff on every path named in §11 point 16, explicitly including `CASH.
  yaml`/`RESERVE.yaml` themselves (referenced, never modified).
- Allocator/margin import-coupling test: a static-analysis-style check confirming the future validator
  module imports neither `allocate.py` nor `margin_state.py`.

## 13. Objective preserved, not invented (unchanged by §0)

This design does not define, redefine, or narrow Portfolio-HQ's governing objective (`XASSET-0001` §A,
unedited). It supplies categorical, evidence-based facts a future asset-appropriate valuation/economic-
assessment step and a future cross-asset opportunity-cost synthesis would need, without itself computing
an expected return, an avoided cost, a hurdle rate, or a risk-adjusted comparison of any kind, and without
asserting a `CASH`-versus-`RESERVE` distinction repository evidence does not support. The "next-dollar
opportunity-cost methodology" `XASSET-0001` §E/§A implies remains wholly undesigned by this artifact —
exactly as `XASSET-0002` §11 and `XASSET-0005` §9 already stated for the ETF/crypto and functional-
doctrine/overlap-model schemas, restated here for the same reason: this is a required future
principal/governance decision, not a byproduct of a design filing.
