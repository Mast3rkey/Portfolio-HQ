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
                                #   canonical_record_hash_sample_or_full (implementation's choice,
                                #   see SS4.1), as_of_note}
economic_role_summary          # free-text rationale, may cite only structural evidence layer
                                #   references above — no new primary research, no fabrication
evidence_coverage_profile      # closed, mechanically derived — see SS4.2
functional_role_note           # optional; populated only for sleeves with a functional_doctrine
                                #   or economic_assessment layer (fund_gld_defensive, cash_reserve,
                                #   debt_reduction) — echoes that layer's own governed category
                                #   value(s), never a new judgment
abstention_index[]             # reconciles every unable_to_determine-shaped value present
record_status                  # draft | sealed
sealed_at / governing_decisions / drafting_session_or_shard_id / content_sha256 /
  cohort_manifest_entry
```

### 4.1 Evidence-layer references — aggregate, not per-instrument

A sleeve profile references its input layers **at the layer level** (population count, aggregate
status tally, one hash into that layer's own `COHORT_MANIFEST.yaml` — or, for a single-record
layer like `economic_assessment/GLD.yaml`, one direct `canonical_record_hash()` pin), not one hash
per individual ticker. This is a deliberate boundary, not a simplification of convenience: Level 1
is sleeve-scoped by `XASSET-0001` §E's own definition, and referencing 27 individual equity
records' hashes inside a sleeve-level profile would blur the Level 1 / Level 2 boundary §8 exists
to keep intact. A future implementation may still cite specific individual records inside a
`rationale` field's prose where genuinely necessary (e.g., naming which tickers drive a disclosed
gap), but the schema's own structural-reference mechanism stays layer-scoped.

### 4.2 `evidence_coverage_profile` — mechanically derived, never self-declared

A closed four-value vocabulary, computed by a validator-enforced rule from the layer's own
aggregate status counts — never hand-typed by a drafting session:

- `fully_computed` — every governed layer this sleeve depends on has 100% of its own population at
  its own layer-specific "complete" status (e.g., `valuation_results.result_status == completed`
  for every record; `overlap_model` dimensions cited as `computed_from_existing_mechanism`).
- `substantially_computed_with_disclosed_gaps` — at least one layer has a non-trivial
  `partial`/equivalent share, but the sleeve's primary structural layer (classification /
  etf_classification / crypto_classification / functional_doctrine, as applicable) is fully sealed.
- `materially_incomplete` — the sleeve's own primary structural layer itself is not fully sealed
  for its own population (not a live state for any of the six sleeves today, per §1's inventory,
  but the value must exist for a future, larger contender-driven sleeve refresh).
- `forced_abstention` — the sleeve's own economic-assessment-equivalent layer is itself structurally
  forced to an abstention state (the live example today: `debt_reduction`, whose
  `functional_doctrine/DEBT_REDUCTION.yaml` carries `economic_assessment_readiness` forced to
  `assessment_required` on both sub-fields, per `XASSET-0006`'s own sealed implementation).

This is a **computed check, not a self-declared field** — learning directly from this
repository's own repeated disclosed lesson (`reconciliation_validator.py`'s MINOR
defense-in-depth gap; `etf_classification_validator.py`'s MINOR-1 on `structural_risk_flags`
presence) that a field asserting a status must be independently re-derivable by the validator from
the underlying data it claims to summarize, never merely schema-shape-checked.

## 5. Sleeve relationship — field design (the opportunity-cost comparison)

```
sleeve_pair                    # {sleeve_a, sleeve_b}, alphabetically ordered by sleeve_id
schema_version
profile_references[]           # exactly two hash pins, into both sleeves' own sealed profiles
primary_disposition            # closed, exactly one of four values -- SS5.1
favored_sleeve_id              # required iff primary_disposition == stronger_priority_support;
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

1. **`stronger_priority_support`** — one named sleeve's own governed evidence base (structural
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

A pair may legitimately carry `stronger_priority_support` **and** `evidence_partial_present`
simultaneously (e.g., the `equity` sleeve's own 18/27-`completed` valuation-result state does not
disqualify it from a `stronger_priority_support` finding against `debt_reduction`, whose own
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
practice from a hidden weight — precisely what §12/§18 of the governing decision, and the
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
6. `favored_sleeve_id` required if and only if `primary_disposition == stronger_priority_support`;
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
