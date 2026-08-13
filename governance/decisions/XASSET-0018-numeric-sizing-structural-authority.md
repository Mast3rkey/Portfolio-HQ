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
schema provisions in `XASSET-0016` §8; all pre-existing structured numeric, lifecycle, and hash
fields remain required unless expressly replaced here.

#### C.1 Source authority

`source_authority` is a recursively closed object containing:

- `policy_adoption_reference`: `{record_path, referenced_content_sha256}` for the same sleeve;
- `source_validation_profile`: forced enum
  `profile_relationship_policy_chain_v1`;
- `source_validation_required`: forced boolean `true`; and
- `numeric_source_field_allowlist`: forced enum
  `axis_b_c_r2_r3_structured_fields_v1`.

The allowlist permits numeric authority to consume only the cited source records' structured
`sizing_readiness_status`, `relationship_coverage_ledger[].{other_sleeve_id,coverage_state,
reference}`, and sealed relationship `secondary_conditions[]` values, after the entire profile →
relationship → policy chain has passed its authoritative validators and hash checks. Source prose
such as `function_rationale`, `blocking_evidence[].detail`, `rationale`, and coordination-note text
may remain authoritative for its own pre-existing record layer, but is never an input to, evidence
for, or validator of a numeric-sizing result.

#### C.2 Numeric outcome and derivation

The existing structured fields remain authoritative and recursively closed:

- `numeric_target_status`: `provisional_target_assigned` |
  `no_provisional_target_pending_axis_c`, live-derived from Axis C;
- `provisional_target_pct`: two-decimal bounded decimal or `null`, paired exactly with status;
- `starting_baseline_pct`: forced live-derived two-decimal baseline when assigned, otherwise
  `null`;
- `applied_adjustments[]`: ordered by `governing_rule_id`, each entry exactly
  `{governing_rule_id: R2 | R3, direction: up | down, magnitude_pct: 2.00,
  evidence_refs[]}`; and
- `governing_rule_ids[]`: the exact ordered projection of `applied_adjustments[]`.

Each `evidence_refs[]` member is a closed object:
`{source_kind, record_path, referenced_content_sha256, field_selector, counterpart_sleeve_id}`.
`source_kind` is `policy_relationship_coverage` for R2 or `sealed_relationship_secondary_conditions`
for R3; `field_selector` is the matching closed selector for that source kind. No prose explanation
or arbitrary selector is permitted.

#### C.3 Typed uncertainty assertions

`uncertainty_disclosure` is removed. It is replaced by `uncertainty_assertions[]`, an ordered array
of closed objects:

```
assertion_type
source_ref
numeric_effect
```

`assertion_type` is one of:

- `policy_blocking_evidence`;
- `relationship_secondary_condition`;
- `axis_a_basis_completeness`;
- `stronger_evidence_maturity`;
- `level2_valuation_coverage_gap`;
- `crypto_cross_coin_correlation_abstention`;
- `crypto_per_coin_historical_divergence`; or
- `existing_level2_constraint_context`.

`source_ref` is a structured hash-pinned record path plus a closed field selector and, where
applicable, a counterpart sleeve or condition-type enum. `numeric_effect` is forced to `none` for
every assertion in this array. R2/R3 effects belong only in `applied_adjustments[]`; the assertion
array can neither add an effect nor narrate one.

#### C.4 Structured comparative provenance

`comparative_consistency_note` is removed. It is replaced by `comparative_provenance[]`, containing
exactly one entry for each other currently sizing-eligible sleeve, ordered by `sleeve_id`:

```
counterpart_sleeve_id
target_relation              # lower | equal | higher
adjustment_tuple_relation    # different | identical
differing_rule_ids[]         # closed subset of [R2, R3]
```

The validator derives all four fields from the two records' live-rederived adjustment tuples and
targets. `target_relation: equal` requires `adjustment_tuple_relation: identical` and an empty
`differing_rule_ids[]`; a non-equal target requires `different` and the exact symmetric difference
of the two rule/direction tuples. No comparative claim may be supplied in prose.

#### C.5 Structured blocking reasons

`blocking_rationale` is removed. A blocked sleeve instead carries `blocking_reason_refs[]`, the
exact structured projection of the cited policy record's live `blocking_evidence[]`, with each
entry restricted to:

```
reason_type
other_sleeve_id
source_record_path
source_content_sha256
source_entry_selector
```

The selector is a validator-derived composite key over the source entry's closed
`reason_type`/`other_sleeve_id`/reference fields; it never copies or interprets the source
`detail` prose. Assigned sleeves carry an empty `blocking_reason_refs[]`.

#### C.6 Structured authority boundaries

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

#### C.7 Closed review conditions

`review_condition` is removed. Assigned records carry `review_conditions[]`, a non-empty ordered
set drawn only from:

- `first_descriptive_risk_analysis`;
- `first_targeted_sizing_backtest`;
- `material_sleeve_population_change`;
- `material_relationship_accounting_change`;
- `baseline_specific_evidence_or_calibration_study`; and
- `increment_specific_evidence_or_calibration_study`.

Each entry is `{condition_type, governed_subject}`, where `governed_subject` is one of
`starting_baseline`, `adjustment_increment`, or `provisional_target`. The validator requires the
complete condition/subject set mandated by `XASSET-0016` §9.8 and rejects arbitrary calendar dates,
free text, unknown conditions, omissions, duplicates, and extras. Blocked records carry an empty
array.

#### C.8 Structured target classification

`target_classification` remains a forced enum: `provisional_governance_guardrail` when a target is
assigned and `null` otherwise. It carries the identical `NUM-0001` class-5 meaning already fixed by
`XASSET-0016`; no narrative restatement is authoritative.

### D. Structured residual classification

`portfolio_reconciliation.unsized_capital_disclosure` is removed. The manifest instead carries:

```
portfolio_reconciliation:
  sum_of_assigned_targets_pct: <live-rederived two-decimal value>
  unsized_reserved_capital_pct: <live-rederived two-decimal value>
  reconciliation_identity_holds: true
  residual_classification:
    residual_type: unsized_unassigned_capital
    sleeve_id: null
    cash_reserve_equivalence: prohibited
    redistribution_status: prohibited_without_future_governance
    policy_target_status: not_a_target
```

The object is recursively closed and forced exactly as shown. It cannot represent cash, reserve,
deployment availability, or a target for any sleeve.

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
2. recompute and verify every cited source hash;
3. enforce recursive schema closure, exact enum/value closure, typed identifier/path/hash grammars,
   cardinality, ordering, nullability, and cross-field consistency;
4. derive Axis B/C eligibility from the validated live source chain and derive R2/R3 only from the
   structured source-field allowlist;
5. exactly rederive baseline, adjustment tuples, targets, comparison provenance, assigned sum,
   residual, and reconciliation identity;
6. reconcile all six records bidirectionally with the manifest, including duplicate, missing,
   extra, orphan, and stale-hash rejection;
7. enforce R1 retirement, `stronger_evidence_maturity` non-influence, non-cascading abstention, and
   the Level 1/Level 2 boundary structurally;
8. reject unrestricted strings anywhere in the authoritative payload; and
9. prove protected paths and all pre-existing sealed records are byte-identical across the
   replacement implementation.

The validator is not authorized or required to perform semantic classification of unrestricted
English. The prose-scanner requirements in `XASSET-0016` §19 items 9-13 are superseded for schema-2.0
authoritative numeric records by the structural prohibition in item 8 above. Existing scanners remain
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
