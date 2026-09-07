# WS-0014 Level 1 Cross-Asset Sleeve-Allocation Synthesis — Methodology Design

**Date**: 2026-08-11
**Governing decision**: `governance/decisions/XASSET-0012-ws0014-level1-cross-asset-synthesis-methodology.md`
**Status**: Design only. No sleeve profile, no sleeve relationship, no weight, no eligibility
disposition is populated by this artifact or its governing decision.

## 0. Purpose of this artifact

`XASSET-0001` §E defines two decision layers — Level 1 (sleeve allocation) and Level 2
(instrument allocation inside a sleeve) — and states that final allocation "must compare
opportunity cost across all governed sleeves," but does not itself design how that comparison
would work. This artifact is that design: the smallest coherent methodology that lets a future,
separately authorized implementation populate a first, provisional Level 1 sleeve-comparison
artifact from evidence that already exists in this repository today. It performs no such
population itself.

## 1. Live evidence inventory this design is built from

Independently re-derived this session (2026-08-11), not assumed from any prior summary:

| Directory | Population | Governing decision(s) |
|---|---|---|
| `intelligence/classification/` | 27 (Milestone 6, four-axis) | `TIER-0001`–`TIER-0006` |
| `intelligence/valuation_archetype/` | 27 | `VALUATION-0003` |
| `intelligence/valuation_evidence/` | 27 | `VALUATION-0004`/`VALUATION-0005` |
| `intelligence/valuation_results/` | 27 (18 `completed` / 9 `partial` / 0 `unable_to_determine`) | `VALUATION-0006`/`VALUATION-0007` |
| `intelligence/etf_classification/` | 4 (SPY, VEA, VWO, GLD) | `XASSET-0002`/`XASSET-0003` |
| `intelligence/crypto_classification/` | 3 (BTC, ETH, SOL) | `XASSET-0002`/`XASSET-0004` |
| `intelligence/functional_doctrine/` | 4 (CASH, RESERVE, GLD_DEFENSIVE_ROLE, DEBT_REDUCTION) | `XASSET-0005`/`XASSET-0006` |
| `intelligence/overlap_model/` | 10 dimensions (6 `computed_from_existing_mechanism`, 4 `not_yet_computable_interface_only`) | `XASSET-0005`/`XASSET-0007` |
| `intelligence/economic_assessment/` | 2 (GLD, CASH_LIKE_CAPITAL) | `XASSET-0008`/`XASSET-0009` |
| `intelligence/instrument_economic_assessment/` | 6 (SPY, VEA, VWO, BTC, ETH, SOL) | `XASSET-0010`/`XASSET-0011` |
| `intelligence/relationships/` | 13 pairwise equity records | `REL-0001`–`REL-0006` |
| `intelligence/recommendations/` | 1 (Milestone 8 package, equity-scoped) | `TIER-0009`/`TIER-0010` |
| `intelligence/reconciliation/` | 1 (Milestone 7 package, equity-scoped) | `TIER-0007`/`TIER-0008` |
| `intelligence/contender_evaluation/` | 2 (VRT, WMT — non-canonical, evidence-parity only) | `CONTENDER-0003` |
| `intelligence/contenders/registry.yaml` | 84 entries | `CONTENDER-0002` |

Every module above exposes its own `canonical_record_hash(data: dict) -> str` function
(independently grepped: `classification_validator.py:252`, `etf_classification_validator.py:322`,
`crypto_classification_validator.py:347`, `functional_doctrine_validator.py:355`,
`overlap_model_validator.py:356`, `economic_assessment_validator.py:848`,
`instrument_economic_assessment_validator.py:582`, `valuation_archetype_validator.py:58`,
`valuation_evidence_validator.py:512`, `valuation_result_validator.py:534`,
`contender_evaluation_validator.py:140`) — the established repository pattern for a downstream
schema to reference a sealed record's exact content without duplicating it. This design reuses
that pattern exclusively; it invents no new hashing or reference scheme.

`targets.yaml`'s own `asset_class` vocabulary is `equity | fund | crypto | reserve | cash` — five
values, with `fund` undifferentiated between SPY/VEA/VWO and GLD. `XASSET-0001` §E's own Level 1
sleeve list is six categories, splitting `fund` into "ETFs" and "GLD/defensive assets" and adding
"debt reduction" (a margin-policy lever with no `targets.yaml` row at all). **Level 1's sleeve
taxonomy is therefore a functional categorization layer on top of `asset_class`, not a restatement
of it** — the same relationship `XASSET-0008` already established between GLD's ETF structural
identity (`instrument_id: GLD`) and its separate functional identity
(`capital_use_type: GLD_DEFENSIVE_ROLE`, `analytical_subject: GLD`). Different layers using
different identifiers for the same real-world sleeve, cross-referenced by hash rather than forced
into one shared vocabulary, is this repository's established pattern, not a new one.

## 2. Sleeve taxonomy — six sleeves, closed vocabulary

| `sleeve_id` | `targets.yaml` `asset_class` scope | Primary governed layers (structural) | Secondary governed layers (functional/economic) |
|---|---|---|---|
| `equity` | `equity` (27 rows) | `classification/` | `valuation_archetype/`, `valuation_evidence/`, `valuation_results/` |
| `fund_broad_market` | `fund` — SPY, VEA, VWO only | `etf_classification/{SPY,VEA,VWO}.yaml` | `instrument_economic_assessment/{SPY,VEA,VWO}.yaml` |
| `fund_gld_defensive` | `fund` — GLD only | `etf_classification/GLD.yaml` | `functional_doctrine/GLD_DEFENSIVE_ROLE.yaml`, `economic_assessment/GLD.yaml` |
| `crypto` | `crypto` (BTC, ETH, SOL) | `crypto_classification/` | `instrument_economic_assessment/{BTC,ETH,SOL}.yaml` |
| `cash_reserve` | `cash` + `reserve` | `functional_doctrine/{CASH,RESERVE}.yaml` | `economic_assessment/CASH_LIKE_CAPITAL.yaml` |
| `debt_reduction` | none (margin lever) | `functional_doctrine/DEBT_REDUCTION.yaml` | `margin_state.py` output (cited, never recomputed), `CLAUDE.md` Portfolio Doctrine (cited, never restated as a number) |

`cash_reserve` treats `CASH` and `RESERVE` as one combined family, reusing — not reopening —
`XASSET-0008`'s own principal-directed provenance finding that the two identifiers have never been
established as distinct economic functions and must not be treated as such absent a future,
separately authorized decision (`CASH_LIKE_CAPITAL.yaml`'s own sealed record already applies this
combined treatment; this design does not revisit it).

Cross-cutting, not owned by any single sleeve: `overlap_model/` (10 dimensions, referenced by any
sleeve pair where applicable, never recomputed or duplicated).

**Explicitly excluded from the first synthesis's input-layer set** (§7 restates as a binding rule):
`intelligence/contender_evaluation/` (VRT, WMT), `intelligence/contenders/registry.yaml` (the
broader 84-entry contender universe), and any Company Intelligence field not already surfaced
through the classification/valuation/ETF/crypto/functional-doctrine/economic-assessment layers
above (avoiding re-litigating raw prose at the sleeve level). `intelligence/recommendations/` and
`intelligence/reconciliation/` may be cited as **equity-scoped context only** — never generalized
into a whole-portfolio finding, restating `XASSET-0001` §H's own boundary.

## 3. Two record types, reusing two already-accepted repository patterns

**Sleeve profile** — one record per sleeve (up to 6), non-comparative, descriptive. Reuses the
"one record per subject, one directory, one manifest" pattern already used by `classification/`,
`etf_classification/`, `crypto_classification/`, `functional_doctrine/`, `economic_assessment/`,
`instrument_economic_assessment/`.

**Sleeve relationship** — one record per unordered sleeve pair, comparative, closed disposition
vocabulary. Reuses `REL-0001`'s exact pairwise convention: filename `<A>_<B>.yaml` in
deterministic alphabetical order (never `<B>_<A>`), one-way authority (a relationship record
references sleeve profiles, never the reverse), no stored graph — the filesystem is the index,
matching `relationship_validator.py`'s own alphabetical-ordering enforcement
(`relationship_validator.py:19`, `:382`).

Different schema, different directory, matching this repository's own settled convention
(independently restated by `CONTENDER-0003` §D as recently as the immediately preceding filing):
`intelligence/level1_sleeve_synthesis/profiles/<SLEEVE_ID>.yaml` and
`intelligence/level1_sleeve_synthesis/relationships/<SLEEVE_A>_<SLEEVE_B>.yaml`, one
`COHORT_MANIFEST.yaml` per subdirectory.

**Full C(6,2) = 15-pair coverage is not required of the first implementation.** Matching
`CONTENDER-0003`'s own two-of-nineteen bounded pilot and `XASSET-0002`'s original five-instrument
scope before its own later scale-up amendment, a future content-authorization filing may bound the
first relationship batch to fewer than 15 pairs, disclosing exactly which pairs are covered and
which are deferred — never silently treating partial coverage as complete.

## 4. Sleeve profile — field design

```
sleeve_id                      # closed, one of the six §2 values
schema_version
evidence_layer_references[]    # list of {layer_name, module, directory, population_count,
                                #   aggregate_status_counts, manifest_content_sha256,
                                #   sleeve_subject_scope (required iff the layer's own manifest is
                                #     shared across more than one sleeve -- SS4.1.1; forbidden
                                #     otherwise), as_of_note}
economic_role_summary          # free-text rationale, may cite only structural evidence layer
                                #   references above — no new primary research, no fabrication
evidence_coverage_profile      # closed, mechanically derived — see SS4.2
functional_role_note           # optional; populated only for sleeves with a functional_doctrine
                                #   or economic_assessment layer (fund_gld_defensive, cash_reserve,
                                #   debt_reduction) — echoes that layer's own governed category
                                #   value(s), never a new judgment
abstention_index[]             # reconciles every unable_to_determine-shaped value present, at both
                                #   the whole-record and the sub-field level -- see SS4.2.1
record_status                  # draft | sealed
sealed_at / governing_decisions / drafting_session_or_shard_id / content_sha256 /
  cohort_manifest_entry
```

### 4.1 Evidence-layer references — aggregate by default, not per-instrument

A sleeve profile references its input layers **at the layer level** (population count, aggregate
status tally, one hash into that layer's own `COHORT_MANIFEST.yaml` — or, for a single-record
layer like `economic_assessment/GLD.yaml`, one direct `canonical_record_hash()` pin), not one hash
per individual ticker, **except where §4.1.1 below requires a sleeve-scoped subject list**. This is
a deliberate boundary, not a simplification of convenience: Level 1 is sleeve-scoped by
`XASSET-0001` §E's own definition, and referencing 27 individual equity records' hashes inside a
sleeve-level profile would blur the Level 1 / Level 2 boundary §8 exists to keep intact. A future
implementation may still cite specific individual records inside a `rationale` field's prose where
genuinely necessary (e.g., naming which tickers drive a disclosed gap), but the schema's own
structural-reference mechanism stays layer-scoped by default.

### 4.1.1 Shared-manifest sub-scoping — required whenever one manifest spans more than one sleeve

**The problem, independently confirmed live**: `intelligence/etf_classification/` has exactly one
`COHORT_MANIFEST.yaml` covering all four sealed records (SPY, VEA, VWO, GLD), but two different
sleeves draw from it — `fund_broad_market` (SPY, VEA, VWO) and `fund_gld_defensive` (GLD). A single
manifest-level hash pin, as §4.1's default aggregate design would otherwise require, cannot let a
future validator determine which of the four instruments actually belong to *this* sleeve's own
profile — both `fund_broad_market`'s and `fund_gld_defensive`'s own profiles would cite the
identical manifest hash, and nothing in the record itself would establish the {SPY,VEA,VWO} versus
{GLD} split. This is the one genuine exception to §4.1's aggregate-only design, not a reason to
abandon it: every other layer in §1's inventory maps to exactly one sleeve (`crypto_classification`
→ `crypto` only; `functional_doctrine` → whichever `capital_use_type` the record names; and so on),
so this sub-scoping mechanism activates only for `etf_classification`, not by default everywhere.

**Design — a closed, deterministic subject list alongside the existing manifest hash, never a
duplication of source-record content**: whenever a sleeve profile's `evidence_layer_references[]`
entry names a layer whose own `COHORT_MANIFEST.yaml` cohort spans more than one sleeve's authorized
population, that entry must additionally carry a `sleeve_subject_scope` object:

```
sleeve_subject_scope: {
  referenced_subject_ids: [...]              # closed list, e.g. ["SPY", "VEA", "VWO"] or ["GLD"]
  referenced_record_content_sha256: {         # one canonical_record_hash() pin per named subject,
    <subject_id>: <hash>, ...                 #   live-recomputed at validation time, never trusted
  }                                           #   from a stored value (matching every other
}                                             #   structural reference in this design)
```

This does **not** reintroduce per-instrument synthesis content — `referenced_subject_ids` is an
identity list only (which sealed records this sleeve's profile is entitled to draw evidence from),
never a per-ticker judgment, weight, or conclusion; the sleeve profile's own `economic_role_summary`
and `evidence_coverage_profile` remain aggregate, sleeve-level fields exactly as §4.1 already
specifies, computed from the *scoped subset* the `sleeve_subject_scope` identifies rather than from
the manifest's full, unscoped population.

**Future validator requirements** (folded into §9's numbered list below, not restated twice):

- A sleeve profile referencing a shared-manifest layer without a `sleeve_subject_scope` is a hard
  schema failure — the aggregate-only shortcut is unavailable the moment a layer's own manifest is
  confirmed (by the validator, not by drafting-session assertion) to span more than one sleeve.
- Every `referenced_subject_ids` entry must be present in the cited layer's own sealed
  `COHORT_MANIFEST.yaml` — an unknown subject is a hard failure.
- Every `referenced_subject_ids` entry must belong to *this* sleeve's own authorized population per
  §2's mapping table (e.g. `GLD` inside `fund_broad_market`'s scope, or any of `SPY`/`VEA`/`VWO`
  inside `fund_gld_defensive`'s scope, is a hard failure) — a live cross-check against §2's fixed
  sleeve-to-subject mapping, not a self-declared list.
- The subject set must be exact — neither missing a subject that belongs to this sleeve (e.g.
  `fund_broad_market` naming only `["SPY", "VEA"]`) nor including an extra one outside the shared
  manifest's own real population (e.g. citing `QQQ`, which has no sealed `etf_classification`
  record at all) validates.
- Every `referenced_record_content_sha256` value is live-recomputed via the source module's own
  `canonical_record_hash()` at validation time; a stale or mismatched hash for any named subject is
  a hard failure, matching the "never trust a stored value" discipline already established for
  every other structural reference in this repository.

### 4.2 `evidence_coverage_profile` — mechanically derived, never self-declared

A closed four-value vocabulary, computed by a validator-enforced rule from the layer's own
aggregate status counts (scoped to §4.1.1's subject subset where applicable) — never hand-typed by
a drafting session:

- `fully_computed` — every governed layer this sleeve depends on has 100% of its own (sleeve-scoped)
  population at its own layer-specific "complete" status (e.g., `valuation_results.result_status ==
  completed` for every record; `overlap_model` dimensions cited as `computed_from_existing_
  mechanism`) **and** carries no forced sub-field-level abstention anywhere in that scoped
  population — see §4.2.1.
- `substantially_computed_with_disclosed_gaps` — at least one layer has a non-trivial
  `partial`/equivalent share, or a disclosed sub-field-level abstention (§4.2.1), but the sleeve's
  primary structural layer (classification / etf_classification / crypto_classification /
  functional_doctrine, as applicable) is fully sealed.
- `materially_incomplete` — the sleeve's own primary structural layer itself is not fully sealed
  for its own (sleeve-scoped) population (not a live state for any of the six sleeves today, per
  §1's inventory, but the value must exist for a future, larger contender-driven sleeve refresh).
- `forced_abstention` — the sleeve's own economic-assessment-equivalent layer is itself structurally
  forced to an abstention state at the **whole-record** level (the live example today:
  `debt_reduction`, whose `functional_doctrine/DEBT_REDUCTION.yaml` carries
  `economic_assessment_readiness` forced to `assessment_required` on both sub-fields, per
  `XASSET-0006`'s own sealed implementation) — distinct from a sub-field-level abstention within an
  otherwise-sealed, otherwise-complete record, which is disclosed via §4.2.1's own mechanism instead
  of forcing the whole sleeve to this value.

This is a **computed check, not a self-declared field** — learning directly from this
repository's own repeated disclosed lesson (`reconciliation_validator.py`'s MINOR
defense-in-depth gap; `etf_classification_validator.py`'s MINOR-1 on `structural_risk_flags`
presence) that a field asserting a status must be independently re-derivable by the validator from
the underlying data it claims to summarize, never merely schema-shape-checked.

### 4.2.1 Sub-field-level abstention roll-up — a governed record's own internal abstentions must never disappear

**The problem, independently confirmed live**: `evidence_coverage_profile`'s four-value vocabulary,
as originally specified, cleanly handles a layer whose own schema exposes one whole-record status
enum (`valuation_results.result_status`, `overlap_model.computation_status`). It did not specify
what happens when a forced abstention lives at a **sub-field** level inside an otherwise-sealed,
otherwise-`record_status: sealed` record — the live examples independently confirmed today:
`crypto_classification`'s `correlation_and_volatility.cross_coin_correlation_status`, forced
`not_yet_measured` on all three sealed `BTC`/`ETH`/`SOL` records; and any per-record sub-field
abstention inside `instrument_economic_assessment` (e.g. a coin's own `macro_behavioral_
characterization` sub-field genuinely abstaining while its sibling sub-field and the record's own
`record_status` remain `sealed`/determined).

**Rule**: a sleeve profile's `evidence_coverage_profile` derivation must independently scan every
*sub-field* of every record in its scoped input layers for a governed abstention token (the
repository's own standard `unable_to_determine`/`not_yet_measured`/`not_yet_computable_interface_
only`/`requires_future_authorization`/`assessment_required` family — the exact closed vocabulary
each source schema already defines, never invented anew here), not merely each record's own
top-level `record_status`/family-status field. A record being `sealed` at the whole-record level
must never be read as "therefore every sub-field within it is fully computed" — that would let a
governed sub-field abstention silently disappear the moment its parent record is otherwise
complete, exactly the failure mode the directive that authorized this design (and MINOR-2 of the
independent review that required this correction) both prohibit.

**Mechanical roll-up, no invented numeric completeness percentage**:

1. Any sub-field-level abstention found anywhere in a sleeve's scoped input population is echoed
   into that sleeve profile's own `abstention_index[]` — one entry per distinct abstaining
   sub-field/record pair, never merged or summarized away.
2. A sleeve whose primary structural layer is otherwise fully sealed, but which carries one or more
   disclosed sub-field-level abstentions, receives `evidence_coverage_profile:
   substantially_computed_with_disclosed_gaps` — the identical value already used for a
   whole-record `partial` share, deliberately not a fifth vocabulary value, since both cases mean
   the same thing from Level 1's own vantage point: "the sleeve's primary structural identity is
   settled; some part of its own governed detail is not yet available."
3. Multiple independent sub-field abstentions within the same sleeve remain **all** individually
   visible in `abstention_index[]` — the roll-up never collapses several distinct gaps into one
   generic flag, and a completed sibling sub-field or a completed sibling record never erases or
   offsets an abstained one elsewhere in the same scoped population.
4. No numeric completeness percentage, ratio, or count-based score is computed or stored anywhere —
   §6's zero-numeric-field rule applies to this roll-up exactly as it does to every other field in
   both record types; the roll-up is a **set of disclosed abstention entries**, not a fraction.

## 5. Sleeve relationship — field design (the opportunity-cost comparison)

```
sleeve_pair                    # {sleeve_a, sleeve_b}, alphabetically ordered by sleeve_id
schema_version
profile_references[]           # exactly two hash pins, into both sleeves' own sealed profiles
primary_disposition            # closed, exactly one of four values -- SS5.1
favored_sleeve_id              # required iff primary_disposition == stronger_evidence_maturity;
                                #   must equal sleeve_a or sleeve_b; forced null otherwise
secondary_conditions[]         # closed set, zero to three -- SS5.2
overlap_dimension_references[] # required iff overlap_or_duplication_disclosed is set; list of
                                #   {dimension_id, referenced_content_sha256}; every cited
                                #   dimension_id's own computation_status must equal
                                #   computed_from_existing_mechanism (SS5.3)
rationale                      # free text; may cite only the two profiles above and, where
                                #   overlap is disclosed, the cited dimension record(s) -- no
                                #   fabricated evidence, no comparative-investment-superiority
                                #   language (SS8)
abstention_index[]
record_status / sealed_at / governing_decisions / drafting_session_or_shard_id /
  content_sha256 / cohort_manifest_entry
```

### 5.1 `primary_disposition` — exactly one, closed, four values

1. **`stronger_evidence_maturity`** — one named sleeve's own governed evidence base (structural
   completeness, evidence-quality maturity, valuation-readiness where the layer applies) is
   materially more complete or more mature than the other's. **This is an evidence-completeness
   finding only — never an investment-merit, expected-return, or "should be sized larger" claim**,
   matching `CONTENDER-0003` §E.6's own identical restriction on its pairwise
   `evidence_parity_finding` field. Requires `favored_sleeve_id`.
2. **`role_preserving`** — the two sleeves serve genuinely distinct portfolio functions (e.g.,
   growth exposure versus survival/liquidity/defensive function) such that an evidence-completeness
   comparison between them does not bear on whether either belongs in the portfolio — directly
   applying `XASSET-0001` §A's objective language that risk, liquidity, concentration, leverage,
   and survival constraints are never silently netted against expected-capital-gains evidence.
3. **`coexistence_supported`** — no governed evidence identifies the two sleeves as competing for
   the same marginal capital in a way that requires prioritizing one over the other.
4. **`unable_to_determine`** — the universal abstention token this repository already uses
   throughout (`classification`'s `economic_role`, `functional_doctrine`'s `functional_role`,
   `valuation_archetype`'s `primary_archetype`) — used when even a disclosed reason for
   `role_preserving`/`coexistence_supported` cannot be established from the two profiles' own
   governed content. Requires a non-empty `abstention_reason` inside the relationship's own
   `abstention_index` entry for this field.

Four values, not five or six — merging what an earlier draft of this design held as two separate
escape hatches (`evidence_insufficient` and `unable_to_determine`) into one, on the directive's own
"smallest set that avoids ambiguity" instruction and this repository's own settled convention that
`unable_to_determine` is already the standard abstention token everywhere else — a second,
differently-named abstention value here would create exactly the kind of ambiguity the directive
warns against, not resolve it.

### 5.2 `secondary_conditions` — orthogonal to the primary value, closed set of three

Mirrors the two-tier primary-status-plus-secondary-flags design `TIER-0009` (seven-value primary
status plus `unresolved_evidence`/`structural_measurement_gap` secondary flags) and `VALUATION-0006`
(`result_status` plus `conflicts_carried_forward`) both already established — a secondary condition
is never a substitute for a reachable primary value, and is never itself scored or weighted.

- `overlap_or_duplication_disclosed` — see §5.3.
- `evidence_partial_present` — at least one of the two sleeves' own profile carries
  `evidence_coverage_profile != fully_computed`.
- `forced_abstention_present` — at least one of the two sleeves' own profile carries
  `evidence_coverage_profile == forced_abstention`, or either profile's own referenced layer
  contains a structurally forced abstention field (e.g., crypto's
  `correlation_and_volatility.cross_coin_correlation_status: not_yet_measured`; any
  `overlap_model` dimension at `not_yet_computable_interface_only`).

A pair may legitimately carry `stronger_evidence_maturity` **and** `evidence_partial_present`
simultaneously (e.g., the `equity` sleeve's own 18/27-`completed` valuation-result state does not
disqualify it from a `stronger_evidence_maturity` finding against `debt_reduction`, whose own
`economic_assessment_readiness` is fully forced-abstained) — this is the structural mechanism that
satisfies the "no absence of evidence may silently become neutral, zero, favorable, unfavorable, or
equal-weight" requirement: the gap stays visible as a secondary flag no matter what the primary
disposition says.

### 5.3 Overlap citation rule — computed dimensions only

`overlap_or_duplication_disclosed` may cite **only** `overlap_model` dimension records whose own
`computation_status == computed_from_existing_mechanism` (six of the ten today: issuer overlap,
economic-role overlap, correlated-loss mechanisms, sleeve concentration, ETF/direct-equity
duplication, leverage/debt interaction). Citing a `not_yet_computable_interface_only` or
`requires_future_authorization` dimension as evidence *of* overlap would assert a finding the
source record itself does not support — the correct treatment for those four dimensions
(crypto-correlation, defensive-offset, geographic/currency-exposure, whole-portfolio
volatility/drawdown-concentration) is `forced_abstention_present`, never
`overlap_or_duplication_disclosed`. This rule is stated here as a mechanically enforceable
validator requirement (§9), not merely a drafting convention.

## 6. Zero numeric fields, no carve-out

Both record types carry no numeric field of any kind — no weight, no percentage, no score, no
rank, no confidence number, no range. This is **stricter** than the ETF framework's own
`expense_ratio_pct` carve-out and matches the posture `XASSET-0005` (functional doctrine, overlap
model), `XASSET-0010` (ETF/crypto economic assessment), and `CONTENDER-0003` (evidence-parity)
already chose for the identical reason: any numeric field on a *comparison* schema, however
innocuous-seeming (even a bare "evidence completeness: 80%"), would be indistinguishable in
practice from a hidden weight — precisely what §D of the governing decision, and the
directive that authorized this design, prohibit outright. `favored_sleeve_id` is a categorical
identifier, not a magnitude, and carries no implicit ordering beyond "this side, not that side."

## 7. Contender, ETF, and Level-2 boundaries — restated as binding design rules

- **Contender boundary**: `VRT`, `WMT`, and every other `intelligence/contenders/registry.yaml`
  entry are excluded from the first synthesis's governed evidence base. Neither record type may
  cite `intelligence/contender_evaluation/` as a structural reference. `CONTENDER-0003` §G already
  establishes that no capital-priority conclusion exists for either pilot ticker — citing them here
  would smuggle that unresolved question into a sleeve-level finding through the back door. A
  future, separately authorized synthesis *refresh* may incorporate contender-driven evidence once
  a capital-priority conclusion for a specific contender actually exists (it does not today).
- **ETF/QQQ boundary**: `fund_broad_market`'s governed population is exactly {SPY, VEA, VWO}. `QQQ`
  carries `primary_disposition: benchmark_or_index` in the contender registry and is not eligible.
  No sleeve profile or relationship record may assert or imply that the current ETF set is
  globally optimal — every profile's own `economic_role_summary` must describe currently governed
  evidence only, refreshable later, never a closed-universe claim.
- **Level 1 / Level 2 boundary**: neither record type may name an individual equity ticker's,
  fund's, or coin's own weight, target, or size — that is Level 2, `XASSET-0001` §J's own explicit
  rule that "a Level 2 instrument target inside a sleeve is only meaningful once that sleeve's own
  Level 1 budget is set," and therefore must never be decided in the same filing or the same record
  type as Level 1. A dedicated leakage scan (§9) enforces this mechanically, not by convention.
- **Portfolio-selection boundary — the narrowest of the two designs weighed**: this methodology
  produces **comparative evidence findings only**. It does not, and no future first-population
  implementation authorized under it may, produce a sleeve-level "in/out," "eligible," or "should
  be part of the portfolio" disposition. Five of the six sleeves already exist as live
  `targets.yaml` rows today (equity, fund_broad_market, fund_gld_defensive, crypto, cash_reserve);
  the sixth, `debt_reduction`, is an existing margin-policy lever, not a candidate for admission —
  so an eligibility question is not even live for any of the six. The alternative design considered
  (permitting a provisional sleeve eligibility/inclusion disposition) is rejected in the governing
  decision's own Alternatives Considered section.

## 8. Forbidden-language boundary

`rationale` fields on both record types are barred from any comparative-investment-superiority
language, reusing `CONTENDER-0003` §F's own materially separate scan design (distinct mechanism
from the plain forbidden-key-name scan): "stronger investment," "should outperform," "inferior
to," "preferable to," "superior," "better positioned," "weaker investment than," and equivalents
are all rejected, while legitimate descriptive language about evidence completeness, evidence
maturity, or abstention validates cleanly (adversarial true/false examples specified in §9).

### 8.1 Portfolio-membership / eligibility / inclusion-language boundary — its own materially separate scan

**The problem this closes**: §7's portfolio-selection boundary ("comparative evidence findings
only, no sleeve eligibility/inclusion disposition of any kind") is this filing's own central,
most-argued design choice — an entire Alternatives Considered entry in the governing decision
rejects the wider reading. Until this correction, the only free-text content scan in §9 bearing on
that boundary was item 12's comparative-investment-superiority scan, whose own listed examples
("stronger investment," "superior," "better positioned") are all investment-merit-shaped, not
eligibility/membership-shaped — a rationale could read "this sleeve should remain in the
portfolio" or "this sleeve warrants exclusion" without tripping that scan at all, since neither
phrase claims one sleeve is a *stronger investment* than another. Every other explicitly-prohibited
language category in this design (numeric, chart-domain, directive/trading, contender-citation,
comparative-investment-superiority) already gets its own dedicated scan item in §9 — this is the
missing one for the boundary the filing works hardest to establish narratively.

**Design — a materially separate mechanism from every other scan in this design**, not a subset or
rewording of item 12 (investment-merit), item 10 (directive/trading), or item 9
(target/weight/tier-leakage):

Rejected, on both record types' free-text fields (`economic_role_summary`, `rationale`,
`functional_role_note`), any phrase asserting or implying a portfolio-membership conclusion for a
sleeve — the closed term/phrase list below, matched case-insensitively with word-boundary anchors,
never a generic sentiment/NLP classifier (matching every other pattern-based scan already accepted
throughout this repository's validator history):

- "include ... in the portfolio" / "should be included in the portfolio" / "warrants inclusion" /
  "merits inclusion" / "deserves inclusion"
- "exclude ... from the portfolio" / "should be excluded from the portfolio" / "remove ... from the
  portfolio"
- "eligible for the portfolio" / "portfolio-eligible" / "ineligible for the portfolio"
- "should be in the portfolio" / "should not be in the portfolio" / "should remain in the
  portfolio" / "should not remain in the portfolio"
- "portfolio membership" (as an assigned conclusion, e.g. "X's portfolio membership is
  confirmed/warranted" — not the bare noun phrase used descriptively, see the false-positive guards
  below)
- "final selection" / "selected for the portfolio" / "not selected for the portfolio"
- a bare "IN" / "OUT" judgment token applied to a sleeve as a portfolio-membership verdict (e.g.
  "sleeve: IN", "this sleeve is OUT") — a closed, narrowly-scoped pattern, not a rejection of the
  ordinary English words "in" or "out" appearing anywhere in free text

**Mandatory false-positive guards** — the future implementation must prove, with adversarial tests,
that the scan does **not** reject legitimate descriptive uses of "include(d)"/"exclude(d)" that
plainly refer to evidence or process scope rather than portfolio membership, e.g.:

- "included in the evidence inventory"
- "excluded from this calculation because evidence is unavailable"
- "the manifest includes four instruments"
- "this record is included in the sleeve's own evidence-layer references"
- "excluded from the first synthesis's governed evidence base" (§7's own boundary language, which
  the design's own decision/artifact text must itself remain free to use without self-triggering a
  future content-record's scan — the distinction is that these two documents are governance/design
  text, never a populated `sleeve_profile`/`sleeve_relationship` record subject to this validator)

This item is specified here, and folded into §9's numbered list as item 17, for a later, separate
implementing PR to build — not implemented in this design-only filing.

## 9. Future validator/test specification

A future, separately authorized implementing PR must build two dedicated validator modules (or one
module covering both record types, the implementing session's own choice to justify, mirroring
`XASSET-0006` §A point 3's identical deferral for functional-doctrine-versus-overlap-model), with
zero import coupling to `allocate.py`/`margin_state.py` in either direction, at minimum:

1. Closed schema at every nesting level (envelope, evidence-layer-reference entry,
   evidence-coverage-profile, abstention-index entry, profile-reference, overlap-dimension-reference
   entry, provenance source, manifest row) — **extra-key rejection**, not merely missing-key checks
   (learning directly from `contender_registry_validator.py`'s own disclosed MAJOR finding).
2. Exactly six `sleeve_id` values, closed; sleeve-relationship filenames restricted to
   deterministic-alphabetical `<A>_<B>` ordering, mirroring `relationship_validator.py`'s own
   enforcement exactly.
3. Live, independent recomputation of every structural/profile/overlap-dimension reference hash,
   never trusting a stored value — a dedicated stale-hash rejection test for each reference type.
4. `evidence_coverage_profile` re-derived live from the referenced layer's own current aggregate
   state, never accepted as self-declared — a dedicated test proving a record claiming
   `fully_computed` while its own cited layer shows a `partial` member is rejected.
5. §5.3's overlap-citation rule mechanically enforced: citing a
   `not_yet_computable_interface_only`/`requires_future_authorization` dimension inside
   `overlap_dimension_references` is a hard failure, independent of whatever the record's own
   `secondary_conditions` claims.
6. `favored_sleeve_id` required if and only if `primary_disposition == stronger_evidence_maturity`;
   forced `null` otherwise; must equal one of the pair's own two `sleeve_id` values, never a third.
7. Zero numeric fields anywhere — a bare-digit/percent/ratio scan **plus** a written-out
   magnitude-comparison-word scan (times/twice/doubled/tripled/-fold/halved), learning directly from
   `instrument_economic_assessment_validator.py`'s own disclosed MINOR-1 finding (a spelled-out
   "three times lower" claim a digit-only pattern missed) and `contender_evaluation_validator.py`'s
   own identical scan, built in from the start rather than discovered post-review.
8. Zero score/rank/composite/weight/priority-index-shaped key name anywhere, matching every prior
   filing's own forbidden-key-name scan convention.
9. Zero `target_pct`/`max_position_size`/tier/gate/cluster/holding-shaped key name or value anywhere
   (the Level 1/Level 2 leakage scan, §7).
10. Zero word-boundary-matched directive/trading language (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/
    `wait`/`stage`), matching every prior filing's own established scan, with the same
    citation-field exemption pattern used elsewhere only where genuinely needed.
11. Zero chart-domain terminology (the same ~16-17-term list used by every prior `TIER-####`/
    `XASSET-####`/`VALUATION-####` schema).
12. The §8 comparative-investment-superiority scan, as its own materially separate mechanism from
    the forbidden-key-name scan — with adversarial false-positive tests proving genuine
    evidence-completeness/abstention/uncertainty language still validates cleanly (mirroring
    `CONTENDER-0003` §F's own six required-clean examples).
13. Zero citation of `intelligence/contender_evaluation/` or `intelligence/contenders/` anywhere
    (the contender boundary, §7).
14. A dedicated protected-path/byte-identity test proving every consumed source record across all
    twelve input layers (§1's table) remains untouched before and after the future implementation —
    matching `economic_assessment_validator.py`'s and `functional_doctrine_validator.py`'s own
    established `test_protected_intelligence_records_untouched` precedent.
15. Manifest bidirectional reconciliation (hash, duplicate, missing, extra, orphan) for both
    subdirectories' own `COHORT_MANIFEST.yaml`, matching every prior manifest's own required checks.
16. Non-cascading abstention discipline — an abstention on one field never forces or implies a
    value on another, matching every schema in this repository since `TIER-0002`.
17. **§8.1's eligibility/inclusion-language scan**, as its own materially separate mechanism from
    item 9 (structural target/weight/tier key leakage), item 10 (directive/trading language), and
    item 12 (comparative-investment-superiority language) — none of the other three catches a
    membership-shaped claim that names no investment merit, no numeric target, and no buy/sell verb.
    Adversarial tests must prove both directions: every §8.1 example phrase rejected, and every
    §8.1 false-positive-guard example still validates cleanly.
18. **§4.1.1's shared-manifest sub-scoping enforcement** — a sleeve profile referencing a
    shared-manifest layer (currently: `etf_classification`, split between `fund_broad_market` and
    `fund_gld_defensive`) without a `sleeve_subject_scope` is a hard schema failure; every named
    subject must be live-cross-checked against both the source layer's own sealed
    `COHORT_MANIFEST.yaml` and §2's fixed sleeve-to-subject mapping table (rejecting an out-of-scope
    subject, e.g. `GLD` claimed inside `fund_broad_market`, or `SPY`/`VEA`/`VWO` claimed inside
    `fund_gld_defensive`); the subject set must be exact, rejecting both an incomplete set (missing
    a subject that genuinely belongs to the sleeve) and an extra one (a subject absent from the
    manifest entirely, e.g. `QQQ`); every `referenced_record_content_sha256` value is
    live-recomputed, never trusted from a stored value, with a dedicated stale-hash rejection test
    per named subject.
19. **§4.2.1's sub-field-level abstention roll-up** — a dedicated test suite proving: (a) a single
    sub-field abstention within an otherwise-sealed, otherwise-fully-computed record (e.g. a coin's
    own `cross_coin_correlation_status: not_yet_measured`) correctly forces that sleeve's own
    `evidence_coverage_profile` away from `fully_computed` and produces exactly one corresponding
    `abstention_index[]` entry; (b) multiple independent sub-field abstentions across different
    records in the same sleeve all remain individually visible in `abstention_index[]`, never merged
    or summarized into one generic flag; (c) a completed sibling sub-field, or a completed sibling
    record, never erases or offsets an abstained one elsewhere in the same scoped population; (d) no
    numeric completeness percentage, ratio, or count is computed or stored anywhere in the roll-up.

## 10. Design sequence — four stages, never collapsed

1. **Stage 1 — this design** (`XASSET-0012`). Methodology only.
2. **Stage 2 — future content authorization.** A future, separate, bounded filing must name the
   exact sleeve-profile population (up to six) and the exact sleeve-relationship-pair population
   (up to fifteen, bounded coverage explicitly permitted per §3) it authorizes, before any record
   is drafted — matching `TIER-0004`→`TIER-0005`'s and `XASSET-0005`→`XASSET-0006`/`XASSET-0007`'s
   own design-then-authorize-content sequence.
3. **Stage 3 — future implementation/population.** Builds the validator(s) and populates exactly
   the records Stage 2 authorized — nothing more, matching every prior WS-0014 content
   implementation's own "the future PR does not itself authorize a second batch" discipline.
4. **Stage 4 — future policy adoption / portfolio selection, if separately authorized.** A sleeve
   profile or relationship record, however complete, creates no allocation, weight, eligibility, or
   trade authority on its own — matching `XASSET-0001` §H's own restated Milestone 9 boundary
   ("any adoption requires its own separate accepted governance decision") one level up, from the
   equity sleeve to the whole portfolio.

No stage may be collapsed into another by this design or by any future filing acting under it.
