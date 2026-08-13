---
decision_id: XASSET-0018
date: 2026-08-12
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, XASSET-0012, XASSET-0013, XASSET-0014, XASSET-0015, XASSET-0016, XASSET-0017, NUM-0001]
supporting_artifact: null
file: governance/decisions/XASSET-0018-numeric-sizing-structural-authority.md
---

## Context

### Why the first implementation must be replaced rather than further patched

`XASSET-0016` designed a deterministic Level 1 numeric sleeve-sizing method and authorized one
future implementation. That implementation was attempted in PR #309. Four independent correction
rounds progressively hardened source validation, schema closure, exact rederivation, comparative
consistency, and forbidden-content detection. The latest exact-head review, anchored to
`252777014790d452948b051c3e3cb458dd16d347`, still found one MAJOR defect: authoritative numeric
records were required to contain unrestricted English while the validator was required to prove
that the English did not imply any prohibited allocation, ranking, chart, evidence-quantity, or
residual/cash meaning. Ordinary affirmative paraphrases continued to evade each finite vocabulary.

That is a structural authority defect, not one more missing word. A finite lexical or semantic
scanner cannot exhaustively prove the absence of an implication in unrestricted natural language.
Continuing to enlarge the scanner would create an unbounded adversarial-language project while
leaving authority dependent on whichever paraphrase had not yet been imagined. The minimum lawful
correction is therefore to remove unrestricted prose from the authority-bearing representation.

### Live lifecycle preflight

This Lane G filing began from verified `origin/main` at
`993b677275bfe37eaeb49b9e0ab5b9efebbfa4ca`, the merge commit of PR #308 (`XASSET-0017`). PR #309
was the sole open PR; it was open, draft, unmerged, mergeable, based on that exact main SHA, and its
exact-head CI run `31662773072` was completed/success. The latest controlling exact-head review was
`pullrequestreview-4923106083`, with 0 BLOCKING / 1 MAJOR / 0 MINOR. The repository principal
authorized closing that attempt without merging if the live state still supported the structural
preflight conclusion. It did. PR #309 was closed unmerged on 2026-08-12; its branch
`agent/xasset-0016-level1-numeric-sizing` and exact head
`252777014790d452948b051c3e3cb458dd16d347` remain preserved and were not deleted or rewritten.
There were then zero open PRs, so this filing opened the single permitted mutation lane directly
from the verified main SHA.

## Decision

### A. Amendment scope

This decision amends only `XASSET-0016`'s numeric-sizing schema, free-text, and validator-authority
provisions. Within that narrow scope, this decision controls as the later, more specific record.
Every other `XASSET-0016` provision remains in force, including its methodology, arithmetic,
population mechanics, source chain, Level 1 boundary, provisional/non-adopted status, and
non-authorization of any allocation check or portfolio-policy change.

The prior unconsummated implementation authorization is retired only insofar as it would populate
the superseded prose-bearing schema. This decision authorizes exactly one future replacement
numeric-sizing implementation PR under the closed structured representation below. Closing PR
#309 did not make any of its records authoritative and did not consume this replacement
authorization.

### B. Sole-authority rule

Only closed structured fields may carry numeric-sizing authority. An authority-bearing numeric
record or cohort manifest may contain only:

- values from explicitly enumerated vocabularies;
- booleans, bounded decimals, timestamps, content hashes, decision identifiers, sleeve identifiers,
  rule identifiers, and repository paths validated against their own closed lexical grammars; and
- recursively closed objects and arrays whose keys, cardinalities, ordering rules, nullability, and
  cross-field relationships are fully specified.

No unrestricted natural-language string may appear anywhere in the authoritative payload. No
validator is authorized or required to infer meaning, intent, negation, causality, ranking,
allocation preference, or residual treatment from prose. A string that is not a closed enum or a
validated structural identifier is an extra-schema value and must be rejected.

### C. Authoritative schema 2.0

The replacement implementation must populate exactly six schema-2.0 records, one per governed
sleeve, plus one schema-2.0 `COHORT_MANIFEST.yaml`. The following fields replace the prose-bearing
schema provisions in `XASSET-0016` §8. This section is the complete schema, not an illustrative
minimum. A future implementation may not infer a missing key, add a convenience key, retain an old
schema-1.x key, or choose a different nesting location.

**Bounded authority-level correction after `pullrequestreview-4923753400`.** The first version of
this filing established the right structural direction but left source-reference substructures and
comparative semantics partly illustrative. §§C-D now replace those passages completely with the
normative envelopes, reference types, selectors, cardinalities, orders, null rules, comparative
orientation, and migration contract below. This correction changes representation authority only;
§G's methodology and outputs remain fixed.

#### C.0 Closed lexical domains and canonical orders

The following orders are normative wherever this decision says “canonical order”:

- sleeve order: `[cash_reserve, crypto, debt_reduction, equity, fund_broad_market,
  fund_gld_defensive]`;
- assigned-sleeve order on the preserved source state: `[crypto, equity, fund_broad_market,
  fund_gld_defensive]`, the sleeve order above filtered to live assigned records;
- rule order: `[R2, R3]`;
- secondary-condition-type order: `[evidence_partial_present, forced_abstention_present,
  overlap_or_duplication_disclosed]`; and
- relationship-record order:
  `[cash_reserve_debt_reduction, cash_reserve_equity, crypto_equity,
  crypto_fund_gld_defensive, debt_reduction_equity, equity_fund_broad_market,
  equity_fund_gld_defensive]`.

All identifiers are exact, case-sensitive members of their named vocabulary. A content hash is
exactly 64 lowercase hexadecimal characters and equals the repository's
`canonical_record_hash()` of the referenced validated record, excluding that record's own
`content_sha256` field under the existing canonical-hash rule. Numeric percentages are quoted YAML
strings matching `^[0-9]+\.[0-9]{2}$`; they are never YAML floats. `sealed_at` is an RFC-3339 UTC
timestamp and is identical across all six replacement records and all six manifest rows.

#### C.1 Closed source-reference base types

There are exactly three source kinds: `sleeve_profile`, `policy_adoption`, and
`sleeve_relationship`. Their record identifiers and paths are not authored independently:

| `source_kind` | permitted `source_record_id` | exact generated `source_path` |
|---|---|---|
| `sleeve_profile` | one of the six sleeve IDs | `intelligence/level1_sleeve_synthesis/profiles/<source_record_id>.yaml` |
| `policy_adoption` | one of the six sleeve IDs | `intelligence/level1_sleeve_synthesis/policy_adoption/<source_record_id>.yaml` |
| `sleeve_relationship` | one of the seven relationship IDs in §C.0 | `intelligence/level1_sleeve_synthesis/relationships/<source_record_id>.yaml` |

The relationship identifier is itself forced from the source record's ordered
`sleeve_pair.sleeve_a`/`sleeve_pair.sleeve_b` values joined with `_`; an arbitrary filename, path
prefix, pair order, external URI, manifest path, fragment, ticker, or instrument identifier is
invalid.

`authority_source_reference` is the only reference type permitted inside `source_authority`. Its
exact keys are:

```
source_kind
source_record_id
source_path
source_content_sha256
```

`trigger_evidence_reference` is the only reference type permitted in an
`applied_adjustments[].evidence_refs[]` array. Its exact keys are:

```
source_kind
source_record_id
source_path
source_content_sha256
selector
projection
```

`uncertainty_source_reference` is the only reference type permitted in an
`uncertainty_assertions[].source_ref`. Its exact keys are:

```
source_kind
source_record_id
source_path
source_content_sha256
selector
selector_key
projection
counterpart_sleeve_id
```

`selector_key` is either `null` or one of exactly two recursively closed objects:
`{reason_code, other_sleeve_id}` for `policy.blocking_evidence.entry`, or
`{condition_type}` for `relationship.secondary_conditions.entry`. No other key shape is valid.
`counterpart_sleeve_id` is the other endpoint relative to the containing numeric record for a
relationship source, the selected `other_sleeve_id` for a policy blocking-evidence entry, and
`null` for profile-wide assertions. It can never name the containing sleeve.

The complete selector/projection vocabulary is below. A selector or projection not listed is
invalid; the two values in a row are an inseparable pair.

| consumer | `source_kind` | exact `selector` | exact `projection` |
|---|---|---|---|
| R2 trigger evidence | `policy_adoption` | `relationship_coverage_ledger.deferred_disclosed_count` | `integer_count` |
| R3 trigger evidence | `sleeve_relationship` | `secondary_conditions.distinct_type_set` | `sorted_secondary_condition_type_set` |
| `policy_blocking_evidence` | `policy_adoption` | `policy.blocking_evidence.entry` | `reason_code_counterpart_reference_state` |
| `relationship_secondary_condition` | `sleeve_relationship` | `relationship.secondary_conditions.entry` | `condition_presence` |
| `stronger_evidence_maturity` | `sleeve_relationship` | `relationship.primary_disposition.stronger_evidence_maturity` | `presence_only` |
| equity valuation gap | `sleeve_profile` | `profile.abstention.equity_valuation_result_partial` | `presence_only` |
| equity discount-rate gap | `sleeve_profile` | `profile.abstention.equity_discount_rate_abstained` | `presence_only` |
| crypto correlation abstention | `sleeve_profile` | `profile.abstention.crypto_cross_coin_correlation_not_yet_measured` | `presence_only` |
| crypto historical divergence | `sleeve_profile` | `profile.abstention.crypto_historical_behavior_divergence_present` | `presence_only` |

`presence_only` is a boolean existence projection; it never projects a count, instrument name,
instrument-specific field path, rank, preference, or value. The equity selectors above are true
only when the validated `equity` profile contains, respectively, exactly one `abstention_index`
entry matching `{source_layer: valuation_results, field_path: result_status, value: partial}` or
exactly one matching `{source_layer: valuation_evidence, field_path: discount_rate_evidence,
value: abstained}`. The crypto correlation selector is true only when the validated `crypto`
profile contains exactly one entry matching `{source_layer: crypto_classification, field_path:
correlation_and_volatility.cross_coin_correlation_status, value: not_yet_measured}`. The crypto
historical-divergence selector is true only when that profile contains exactly one entry whose
`source_layer` is `instrument_economic_assessment`, whose value is `unable_to_determine`, and whose
validated three-component source field path ends exactly in
`.macro_behavioral_characterization.historical_equity_market_drawdown_behavior`; the first path
component is neither copied nor projected. Any zero-match or multi-match result rejects the
assertion. The numeric record may not copy the matched source field path or which instrument
supplied it.

#### C.2 Complete record envelope and applicability matrix

Every schema-2.0 numeric record has exactly these 20 top-level keys, in this YAML presentation
order, and no others:

```
schema_version
sleeve_id
source_authority
numeric_target_status
provisional_target_pct
starting_baseline_pct
applied_adjustments
governing_rule_ids
target_classification
review_conditions
uncertainty_assertions
comparative_provenance
blocking_reason_refs
authority_boundaries
record_status
sealed_at
governing_decisions
drafting_session_or_shard_id
content_sha256
cohort_manifest_entry
```

`schema_version` is forced to the string `"2.0"`. The inherited schema-1.x top-level
`policy_adoption_reference` is **replaced**, not retained or duplicated: policy authority has one
and only one home, `source_authority.policy_adoption_references`. The old fields
`review_condition`, `uncertainty_disclosure`, `comparative_consistency_note`,
`blocking_rationale`, and `sizing_boundary_note` are prohibited extra keys.

Every key above is present on both record statuses. Applicability is expressed only by the exact
value/empty/null rule below; conditional omission is never valid.

| field | assigned record | blocked record |
|---|---|---|
| `schema_version` | REQUIRED `"2.0"` | REQUIRED `"2.0"` |
| `sleeve_id` | REQUIRED assigned sleeve ID | REQUIRED blocked sleeve ID |
| `source_authority` | REQUIRED exact §C.3 object | REQUIRED exact §C.3 object |
| `numeric_target_status` | REQUIRED `provisional_target_assigned` | REQUIRED `no_provisional_target_pending_axis_c` |
| `provisional_target_pct` | REQUIRED populated two-decimal string | REQUIRED `null` |
| `starting_baseline_pct` | REQUIRED `"16.67"` | REQUIRED `null` |
| `applied_adjustments` | REQUIRED exact zero-to-two-entry §C.4 list | REQUIRED exact empty list |
| `governing_rule_ids` | REQUIRED exact projection of adjustments | REQUIRED exact empty list |
| `target_classification` | REQUIRED `provisional_governance_guardrail` | REQUIRED `null` |
| `review_conditions` | REQUIRED exact six-row §C.8 list | REQUIRED exact empty list |
| `uncertainty_assertions` | REQUIRED exact live projection under §C.5 | REQUIRED exact empty list |
| `comparative_provenance` | REQUIRED one row per other assigned sleeve | REQUIRED exact empty list |
| `blocking_reason_refs` | REQUIRED exact empty list | REQUIRED exact §C.7 projection |
| `authority_boundaries` | REQUIRED forced §C.8 object | REQUIRED forced §C.8 object |
| `record_status` | REQUIRED `sealed` | REQUIRED `sealed` |
| `sealed_at` | REQUIRED shared RFC-3339 UTC timestamp | REQUIRED same timestamp |
| `governing_decisions` | REQUIRED `[XASSET-0016, XASSET-0017, XASSET-0018]` | REQUIRED same list |
| `drafting_session_or_shard_id` | REQUIRED `xasset-0018-numeric-sizing-structural-replacement` | REQUIRED same value |
| `content_sha256` | REQUIRED live canonical record hash | REQUIRED live canonical record hash |
| `cohort_manifest_entry` | REQUIRED exact manifest path plus `#<sleeve_id>` | REQUIRED same grammar |

Only the three table cells explicitly containing `null` are nullable. Arrays and objects are never
`null`. No field is optional.

#### C.3 Source authority

`source_authority` has exactly these six keys:

```
source_validation_profile: profile_relationship_policy_chain_v1
source_validation_required: true
numeric_source_field_allowlist: axis_b_c_r2_r3_structured_fields_v1
profile_references: [...]
policy_adoption_references: [...]
relationship_references: [...]
```

Each list contains only `authority_source_reference` objects:

- `profile_references`: exactly six rows, one for every sleeve, in sleeve order;
- `policy_adoption_references`: exactly six rows, one for every sleeve, in sleeve order; and
- `relationship_references`: exactly seven rows, one for every relationship ID, in relationship
  order.

All six numeric records carry the same 19 source identities and live hashes. This is intentional:
R2/R3 extrema and the assigned population are cohort comparisons, so a record cannot present only
its own source subset. The own policy reference is the unique `policy_adoption_references` row
whose `source_record_id` equals the containing `sleeve_id`; no separate own-policy field exists.
The validator must validate all three directories before reading any projection.

The field allowlist permits numeric derivation to inspect only: profile
`evidence_coverage_profile`; policy `portfolio_function_status`,
`capital_eligibility_status`, `sizing_readiness_status`, and
`relationship_coverage_ledger[].{other_sleeve_id, coverage_state, reference}`; relationship
`sleeve_pair`, `primary_disposition`, and `secondary_conditions[]`; plus identity, lifecycle, and
hash fields needed to validate those records. Of those fields, `primary_disposition` can feed only
the nonnumeric `stronger_evidence_maturity` assertion. `favored_sleeve_id` has no permitted
projection and zero numeric influence. All source prose remains unreadable by numeric authority.

#### C.4 Numeric outcome, per-rule state, and trigger evidence

`numeric_target_status`, target, baseline, and adjustment arithmetic retain their exact
`XASSET-0016` meanings. `applied_adjustments[]` contains only fired rules, in rule order. Each
entry has exactly:

```
governing_rule_id: R2 | R3
direction: up | down
magnitude_pct: "2.00"
evidence_refs: [...]
```

No-fire is not represented by a synthetic adjustment. For every assigned sleeve and each rule,
the validator nevertheless derives exactly one rule state from `no_fire | up | down`; `no_fire`
means the rule exists but did not fire because the sleeve was not a strict unique extreme or the
relevant extreme was tied. This state is exposed only in comparative rows (§C.6). A no-fire rule
therefore has no adjustment entry and no adjustment-local `evidence_refs`; its complete evidence is
still present in the containing record's mandatory `source_authority` and is rederived.

For an R2 adjustment, `evidence_refs` contains exactly four `trigger_evidence_reference` rows, one
for each assigned policy record, in assigned-sleeve order. Every row uses the R2 selector/projection
pair in §C.1. This exact four-record comparison population proves the unique minimum, unique
maximum, or tie; a self-only reference is invalid.

For an R3 adjustment, `evidence_refs` contains exactly six `trigger_evidence_reference` rows, in
relationship order, for the preserved-state relationship IDs
`cash_reserve_equity`, `crypto_equity`, `crypto_fund_gld_defensive`,
`debt_reduction_equity`, `equity_fund_broad_market`, and
`equity_fund_gld_defensive`. These are exactly the unique sealed relationship records with at
least one assigned endpoint. Every row uses the R3 selector/projection pair in §C.1. The validator
forms each assigned sleeve's set of distinct condition types from pair membership; it never counts
occurrences and never includes the blocked-only `cash_reserve_debt_reduction` pair.

`governing_rule_ids[]` equals the rule-order projection of `applied_adjustments[]`; duplicates, R1,
unknown rules, wrong magnitude, wrong reference set, wrong order, and stored-but-live-no-fire
adjustments are invalid.

#### C.5 Typed uncertainty assertions

`uncertainty_disclosure` is removed. Each `uncertainty_assertions[]` member has exactly:

```
assertion_type
source_ref
numeric_effect: none
```

The allowed assertion types and their complete rules are:

| `assertion_type` | applicability | exact source and selector | exact cardinality/population rule |
|---|---|---|---|
| `policy_blocking_evidence` | assigned only | containing sleeve's `policy_adoption`; `policy.blocking_evidence.entry`; key `{reason_code, other_sleeve_id}` | exactly one assertion for every validated source entry; no omissions or extras |
| `relationship_secondary_condition` | assigned only | each sealed relationship incident to the sleeve; `relationship.secondary_conditions.entry`; key `{condition_type}` | exactly one per distinct `(source_record_id, condition_type)` occurrence |
| `stronger_evidence_maturity` | assigned only | each incident relationship whose validated `primary_disposition` equals that enum; presence-only selector | exactly one per qualifying relationship, regardless of `favored_sleeve_id` |
| `level2_valuation_coverage_gap` | assigned `equity` only | `equity` profile; the two equity profile selectors in §C.1 | exactly two, one for each selector, both presence-only |
| `crypto_cross_coin_correlation_abstention` | assigned `crypto` only | `crypto` profile; matching §C.1 selector | exactly one, presence-only |
| `crypto_per_coin_historical_divergence` | assigned `crypto` only | `crypto` profile; matching §C.1 selector | exactly one aggregate presence assertion; zero instrument IDs or values |

For `policy_blocking_evidence`, `selector_key` is exactly the selected source entry's
`{reason_code: reason_type, other_sleeve_id}` using the four-code vocabulary in §C.7, and
`counterpart_sleeve_id` equals that non-self `other_sleeve_id`. For
`relationship_secondary_condition`, `selector_key` is exactly `{condition_type}` and
`counterpart_sleeve_id` is the relationship's other endpoint. For
`stronger_evidence_maturity`, `selector_key` is `null` and `counterpart_sleeve_id` is the other
endpoint. All profile-backed rows force both values to `null`. Every selector must resolve exactly
one validated source entry; zero or multiple matches reject the record.

Blocked records carry no uncertainty assertions because their complete reason projection is
`blocking_reason_refs`. Within assigned records, the array is the exact mechanically selected
population above—not an author's choice. Multiple assertions of one type are permitted only when
the table's population rule yields different source-reference identities. A duplicate is an exact
duplicate of `(assertion_type, source_kind, source_record_id, selector, selector_key,
counterpart_sleeve_id)` and is rejected.

Canonical assertion-type order is the table order. Within a type, sort by source-record order,
then selector string, then selector-key enum order, then counterpart sleeve order; `null` sorts
before a sleeve ID.

The initial filing's proposed `axis_a_basis_completeness` type is not in the final allowed
vocabulary because the live source stores basis multiplicity only in prose, which numeric authority
is forbidden to interpret. The proposed `existing_level2_constraint_context` type is likewise not
in the final vocabulary: no selector over a rank, preference, capital-priority, instrument, target,
or deployment field is permitted merely to disclose its existence. Those subjects may appear only
in non-authoritative generated display under §E until a separate governance act creates a closed,
sleeve-level upstream field. Removing them from authoritative payload does not restore R1 or give
them numeric effect.

No assertion projects an evidence count, ticker, coin, instrument ID, instrument-level weight,
rank, score, preference, capital priority, chart or technical signal, deployment or execution
state, order, or trade field. `numeric_effect` is always `none`; R2/R3 effects exist only in
`applied_adjustments[]`.

#### C.6 Total structured comparative provenance

An assigned record's `comparative_provenance[]` contains exactly one row for every **other
assigned** sleeve—three rows on the preserved source state—in assigned-sleeve order with self
filtered out. It contains no self row and no blocked-sleeve row. A blocked record carries the exact
empty list.

Each row has exactly these six keys:

```
counterpart_sleeve_id
target_relation
self_rule_states
counterpart_rule_states
differing_rule_ids
cancellation_status
```

`self_rule_states` and `counterpart_rule_states` each have exactly `{R2, R3}`, in rule order, and
each value is exactly one of `no_fire | up | down` as derived in §C.4. The containing record is
always “self.” `target_relation` is from the containing record's perspective:

- self target < counterpart target → `lower`;
- self target = counterpart target → `equal`; and
- self target > counterpart target → `higher`.

`differing_rule_ids` is **not** a symmetric difference of `(rule, direction)` tuples. It is the
rule-order list of the unique rule IDs for which
`self_rule_states[rule] != counterpart_rule_states[rule]`. Thus R2 `up` versus R2 `down` yields
exactly `[R2]`; R2 `up` versus R2 `no_fire` also yields `[R2]`; equal R2 states omit R2.

`cancellation_status` is a closed enum derived as follows:

- `none` when `differing_rule_ids` is empty (the targets must then be equal);
- `cancelled_to_equal` when `differing_rule_ids` is non-empty but the live-rederived targets are
  equal; and
- `not_cancelled` when `differing_rule_ids` is non-empty and the targets are unequal.

Cancellation never erases provenance: `target_relation` remains `equal`, each differing rule
remains listed, and both sides' directions remain visible. The validator independently rederives
all six row fields; prose, stored target relation, or row order cannot override arithmetic.

The following fictional unit-increment examples are normative for structure only; `A`/`B` are not
live sleeves and no live percentage is shown:

| case | A states `(R2,R3)` | B states `(R2,R3)` | A's relation to B | differing IDs | cancellation |
|---|---|---|---|---|---|
| identical | `(no_fire,no_fire)` | `(no_fire,no_fire)` | `equal` | `[]` | `none` |
| same-rule opposite | `(up,no_fire)` | `(down,no_fire)` | `higher` | `[R2]` | `not_cancelled` |
| fire/no-fire | `(up,no_fire)` | `(no_fire,no_fire)` | `higher` | `[R2]` | `not_cancelled` |
| R3 opposite | `(no_fire,down)` | `(no_fire,up)` | `lower` | `[R3]` | `not_cancelled` |
| both differ, not cancelled | `(up,up)` | `(down,no_fire)` | `higher` | `[R2,R3]` | `not_cancelled` |
| differences cancel | `(up,down)` | `(down,up)` | `equal` | `[R2,R3]` | `cancelled_to_equal` |
| blocked A | not applicable | any assigned B | no row permitted | not applicable | not applicable |

An assigned record always applies these rules to all three assigned peers, not only peers with a
different target.

#### C.7 Structured blocking reasons

`blocking_rationale` is removed. Each `blocking_reason_refs[]` entry has exactly:

```
reason_code
other_sleeve_id
source_kind
source_record_id
source_path
source_content_sha256
source_entry_selector
```

`source_kind` is forced `policy_adoption`; `source_record_id` is the containing sleeve;
`source_path`/hash follow §C.1. `source_entry_selector` has exactly:

```
reason_type
other_sleeve_id
reference_mode
relationship_record_id
```

The only legal combinations are:

| `reason_code` = selector `reason_type` | `other_sleeve_id` | `reference_mode` | `relationship_record_id` |
|---|---|---|---|
| `axis_b_not_eligible` | `null` | `none` | `null` |
| `deferred_relationship_pair` | required other sleeve | `none` | `null` |
| `sealed_unresolved_relationship` | required other sleeve | `sealed_relationship_hash_pin` | exact canonical pair ID |
| `secondary_condition_present` | required other sleeve | `sealed_relationship_hash_pin` | exact canonical pair ID |

Top-level and selector reason/other-sleeve values must agree. For a hash-pinned mode, the selected
policy entry's own `reference.record_path` and hash must equal the relationship reference named by
the canonical pair ID; for `none`, that source entry's `reference` must be `null`. The source
`detail` string is never copied or read. The four selector components must resolve exactly one
source `blocking_evidence[]` entry; zero or multiple matches make the source projection invalid.

A blocked record contains exactly one blocking row for every entry in its own validated policy
`blocking_evidence[]`; an assigned record contains exactly zero. On the preserved state this is
five rows for `cash_reserve` and six for `debt_reduction`. Duplicates and omissions are invalid.
Canonical reason order is `[axis_b_not_eligible, sealed_unresolved_relationship,
deferred_relationship_pair, secondary_condition_present]`, then other-sleeve order, then
relationship-record order.

#### C.8 Structured authority boundaries, review conditions, and classification

`sizing_boundary_note` is removed. Every record instead carries the forced-constant object
`authority_boundaries`:

```
scope_level: level_1_sleeve_only
policy_status: provisional_not_adopted
level_2_sizing_authority: prohibited
allocation_check_authority: prohibited
portfolio_config_mutation_authority: prohibited
brokerage_execution_authority: prohibited
margin_or_leverage_input: prohibited
chart_or_deployment_input: prohibited
```

Any missing, substituted, or additional key/value is rejected.

`review_condition` is removed. Assigned records carry `review_conditions[]`, a non-empty ordered
set. It is not a draftable subset: every assigned record contains exactly these six closed objects
in this order:

1. `{condition_type: first_descriptive_risk_analysis, governed_subject: provisional_target}`
2. `{condition_type: first_targeted_sizing_backtest, governed_subject: provisional_target}`
3. `{condition_type: material_sleeve_population_change, governed_subject: provisional_target}`
4. `{condition_type: material_relationship_accounting_change, governed_subject: provisional_target}`
5. `{condition_type: baseline_specific_evidence_or_calibration_study, governed_subject: starting_baseline}`
6. `{condition_type: increment_specific_evidence_or_calibration_study, governed_subject: adjustment_increment}`

Each object has exactly `condition_type` and `governed_subject`; blocked records carry `[]`.

`target_classification` remains a forced enum: `provisional_governance_guardrail` when a target is
assigned and `null` otherwise. It carries the identical `NUM-0001` class-5 meaning already fixed by
`XASSET-0016`; no narrative restatement is authoritative.

#### C.9 Adversarial conformance uniqueness

The following are forced answers, not examples. A materially different implementation cannot
claim conformance:

| attempted choice point | only conforming answer |
|---|---|
| uncertainty source selectors | only the nine selector/projection rows in §C.1, with the exact §C.5 mechanically selected population |
| `existing_level2_constraint_context` | prohibited assertion type; no selector allowlist exists |
| R2 evidence | exactly the four assigned policy records, canonical order, count selector |
| R3 evidence | exactly the six named incident relationship records, canonical order, distinct-type-set selector |
| no-fire evidence | no adjustment row; state rederived from the mandatory 19-source snapshot |
| blocking selector | exactly the four-key grammar and four reason combinations in §C.7 |
| policy-adoption reference location | only `source_authority.policy_adoption_references`; top-level duplication prohibited |
| assigned comparative rows | exactly all three other assigned sleeves; no self/blocked rows |
| blocked comparative rows | exact empty list |
| same-rule opposite directions | one differing rule ID, with both closed directional states retained |
| cancellation | `target_relation: equal`, all differing IDs retained, `cancelled_to_equal` |
| source ordering | the sleeve and relationship orders in §C.0 |
| manifest row ordering | exactly six rows in §C.0 sleeve order |

The validator tests in §F must construct a nonconforming alternate for every row above and prove
rejection. This is the governance-text adversarial matrix required before implementation, not a
delegation of policy choice to that implementation.

### D. Complete schema-2.0 manifest, residual, and atomic migration

The schema-2.0 `COHORT_MANIFEST.yaml` has exactly these four top-level keys, in this order:

```
schema_version
governing_decisions
cohort
portfolio_reconciliation
```

`schema_version` is `"2.0"`; `governing_decisions` is exactly
`[XASSET-0016, XASSET-0017, XASSET-0018]`. No manifest self-hash or source-snapshot field is
permitted: every record carries the exact common source snapshot under §C.3, and the manifest
reconciles record hashes.

`cohort` contains exactly six rows in sleeve order. Each row has exactly these keys:

```
sleeve_id
record_path
content_sha256
schema_version
governing_decisions
numeric_target_status
drafting_session_or_shard_id
sealed_at
```

`record_path` is exactly
`intelligence/level1_sleeve_synthesis/numeric_sizing/<sleeve_id>.yaml`; the hash equals that
record's live canonical hash; every other row field equals the corresponding record field. Missing,
duplicate, extra, orphan, stale-hash, wrong-order, or status-mismatched rows are invalid.

`portfolio_reconciliation` has exactly:

```
sum_of_assigned_targets_pct: <live-rederived two-decimal string>
unsized_reserved_capital_pct: <live-rederived two-decimal string>
portfolio_total_pct: "100.00"
reconciliation_identity_holds: true
assigned_record_count: 4
blocked_record_count: 2
residual_classification:
  residual_type: unsized_unassigned_capital
  sleeve_id: null
  cash_reserve_equivalence: prohibited
  redistribution_status: prohibited_without_future_governance
  policy_target_status: not_a_target
```

`residual_classification` has exactly the five keys and forced values shown. Counts and totals are
live-rederived; the literal 4/2 values are required by the preserved unchanged source state and the
implementation must stop under §G if that state changes before implementation. The residual is not
a seventh sleeve, cash, reserve, deployable capital, or a target.

Schema-1.x numeric records are not valid schema-2.0 records. The replacement implementation must
replace all six records and the manifest atomically in one bounded PR; a mixed-version cohort,
partial migration, schema-1.x compatibility fallback, or schema-1.x manifest row is invalid. PR
#309's schema-1.0 records remain historical evidence on its preserved unmerged branch only and do
not become authority. No implementation may silently migrate a subset or treat old hashes as
current record hashes.

### E. Human-readable material is derived and non-authoritative

Human-readable explanation is permitted only in either of two forms:

1. a deterministic display rendered from the authoritative structured fields and not stored in the
   authoritative record; or
2. separate `derived_non_authoritative` material, physically outside the authoritative
   `numeric_sizing/` record/manifest set, labeled with the exact source-record hashes and a forced
   `authority_status: derived_non_authoritative` marker.

Derived material is never an input to numeric derivation, source validation, record validity,
manifest reconciliation, policy adoption, or any later governance action. It may be deleted and
regenerated without changing authoritative content. The replacement implementation is not required
to create or retain it.

### F. Validator authority and required checks

The replacement validator is authorized and required to:

1. validate the profile, relationship, and policy-adoption source directories through their
   authoritative validators before selecting the eligible population;
2. construct the exact 19-row §C.3 source snapshot from the closed path generators, then compare
   every stored source identity, path, order, and recomputed hash exactly;
3. enforce the complete §C.2 record key set and §D manifest key sets recursively, including exact
   enums, identifiers, paths, hashes, cardinality, order, nullability, and conditional values;
4. reject every selector/projection pair outside §C.1 and independently construct the exact
   uncertainty, R2, R3, and blocking reference populations before comparing them structurally;
5. derive Axis B/C eligibility from the validated live source chain and derive R2/R3 only from the
   structured source-field allowlist;
6. exactly rederive baseline, each `no_fire | up | down` state, adjustment tuples, targets, every
   comparative row, assigned sum, residual, counts, and reconciliation identity;
7. reconcile all six records bidirectionally with the manifest, including duplicate, missing,
   extra, orphan, stale-hash, wrong-status, mixed-version, and wrong-order rejection;
8. enforce R1 retirement, `stronger_evidence_maturity` non-influence, non-cascading abstention, and
   the Level 1/Level 2 boundary structurally;
9. reject any unrestricted string, arbitrary source namespace, raw field path, ticker, instrument
   ID, instrument weight or target, rank, score, preference, capital-priority, chart/technical,
   deployment/execution, order, or trade field anywhere in the authoritative payload; and
10. prove protected paths and all pre-existing sealed records are byte-identical across the
    replacement implementation.

Required adversarial tests must include: source kind/path/ID substitution; omitted, extra,
duplicated, reordered, or cross-sleeve source references; every selector/projection substitution;
wrong R2 four-policy set; wrong R3 six-relationship set; a no-fire rule carrying an adjustment;
blocking-selector component substitution; assigned/blocked applicability inversion; a blocked
comparative row; a missing assigned peer; reversed target orientation; R2 and R3 fire/no-fire;
same-rule opposite directions; two-rule cancellation to equal; a false cancellation flag; mixed
schema versions; manifest status disagreement; and every Level-2/prohibited-field family in item 9.

The validator is not authorized or required to perform semantic classification of unrestricted
English. The prose-scanner requirements in `XASSET-0016` §19 items 9-13 are superseded for schema-2.0
authoritative numeric records by the structural prohibition in item 9 above. Existing scanners remain
unchanged and authoritative for the pre-existing record layers they already govern; this amendment
does not weaken or redesign them.

### G. Methodology and numeric preservation fence

This amendment does not change:

- the closed six-sleeve taxonomy or the requirement to create one record per sleeve;
- live Axis B/C eligibility mechanics, including `XASSET-0017`'s now-live four-eligible/two-blocked
  population;
- the equal-share baseline over all six sleeves: `100.00 / 6 = 16.67`;
- R2's deferred-relationship-count rule, R3's distinct-secondary-condition-type-breadth rule, or
  either rule's strict-unique-extreme/tie-suppression mechanics;
- the fixed `±2.00` percentage-point increment per firing R2/R3 trigger;
- the closed adjustment set `{-4.00, -2.00, 0.00, +2.00, +4.00}` and per-sleeve theoretical bound
  `[12.67, 20.67]`;
- two-decimal arithmetic, exact reconciliation, null-not-zero blocked semantics, or residual
  treatment; or
- the requirement that a future implementation derive live from sealed sources rather than trust
  a point-in-time narrative.

On the live source state verified for this filing, the replacement implementation must reproduce,
not select or retune, the already-rederived provisional outputs from PR #309:

| Sleeve | Required preserved result |
|---|---:|
| `equity` | `18.67%` |
| `fund_broad_market` | `14.67%` |
| `fund_gld_defensive` | `16.67%` |
| `crypto` | `16.67%` |
| `cash_reserve` | blocked / `null` |
| `debt_reduction` | blocked / `null` |

The assigned sum remains `66.68%`; `unsized_reserved_capital_pct` remains `33.32%`; the identity
remains exactly `100.00%`. These figures are preservation constraints for the replacement
implementation on an unchanged source state, not adopted portfolio policy, not authority to edit
`targets.yaml`, and not permission to skip live rederivation. If the authoritative source hashes or
live Axis B/C population change before implementation, the implementation must stop and return for
new governance direction rather than silently producing a different result under this authorization.

### H. Exactly one replacement implementation

After this decision itself completes independent exact-head review, principal acceptance, merge, and
post-merge verification, exactly one future replacement implementation PR may:

- create the six schema-2.0 numeric-sizing records and schema-2.0 manifest;
- create or modify only the dedicated numeric-sizing validator and its focused/adversarial tests as
  required by §F;
- add the corresponding factual WORKSTREAMS synchronization; and
- reproduce the §G preservation state from the then-validated, unchanged live sources.

That future PR must receive its own full lifecycle. It may not copy files or commits from PR #309
wholesale; the preserved branch is evidence and implementation history, not authority. Reuse is
permitted only for bounded code or test mechanics independently shown to conform to schema 2.0 and
the structural-authority rule.

### I. Explicit non-authorization

This governance-only filing does not implement schema 2.0, create or edit a numeric-sizing record,
edit `COHORT_MANIFEST.yaml`, modify a validator or test, or compute a new result. It authorizes no
Level 2 work, target or tier change, portfolio membership or sleeve-membership change, allocation
check, stress test, chart work, monitoring, policy adoption, deployment, margin change, or brokerage
action. It does not alter `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `margin_state.py`, `levels.py`, any sealed profile/relationship/policy record, R2/R3,
the baseline, the increment, the provisional figures, or the residual.

## Rationale

Natural language is open-ended; authority must not depend on proving that every possible paraphrase
of a forbidden claim has been anticipated. Closed structured representation makes the permitted
meaning enumerable and the validator's obligation finite: reject unknown structure, validate sources,
and rederive every output. This preserves all substantive work in `XASSET-0016` and PR #309 while
removing only the authority surface that independent review demonstrated could not be closed.

The amendment is deliberately governance-only. Implementing schema 2.0 in the same PR would collapse
authority design and execution into one review unit, obscure whether the replacement implementation
actually follows the amended authority, and violate the repository's established design-before-
implementation separation.

## Alternatives Considered

**Continue expanding PR #309's semantic vocabulary.** Rejected. Each correction closed known phrases
and left ordinary unseen paraphrases. No finite vocabulary can prove unrestricted English free of all
prohibited implication.

**Ban all human-readable explanation everywhere.** Rejected. Explanation remains useful for people,
but it belongs in a deterministic display or separately labeled derived material, never in the
authority-bearing payload.

**Change the numeric methodology while changing its representation.** Rejected. The defect is the
authority representation, not R2/R3, the baseline, increment, arithmetic, or live outputs. Combining
the questions would expand scope without evidence.

**Implement schema 2.0 in this filing.** Rejected. A governance amendment must first become effective;
its implementation then requires a separate exact-head review against that effective authority.

## Consequences

Once accepted and merged, authoritative numeric-sizing content becomes closed, structured, and exactly
rederivable without semantic interpretation of English. PR #309 remains a closed, unmerged historical
attempt at its preserved head. One replacement implementation is authorized only after this decision's
own lifecycle completes. Until then, no numeric-sizing record is authoritative and the next action is
independent exact-head review of this filing—not schema implementation, policy adoption, or allocation.
