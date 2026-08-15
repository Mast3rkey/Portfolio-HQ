---
decision_id: XASSET-0022
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, LEVEL2-0001]
supporting_artifact: null
file: governance/decisions/XASSET-0022-level1-application-artifact-schema-and-deterministic-generation-authority.md
---

## Context

Effective XASSET-0021 closes every economic application-time choice for the Level-1 sizing
methodology, either deterministically or by mandatory abstention, and leaves exactly two rows of its
§N matrix open: `CM-27 application_schema` and `CM-28 deterministic_trace_and_repeatability`, both
`SEPARATE_PREREQUISITE_REQUIRED`. Because a single such row withholds authority under §B, no
application may begin.

XASSET-0021 §L names the smallest unit that can close those two rows: one separate Lane G governance
unit titled, by scope, `Level-1 Application Artifact Schema and Deterministic Generation Authority`.
This is that unit. It is purely mechanical. It adds no economic evidence, parameter, endpoint,
portfolio rule, or policy, and it does not apply XASSET-0020.

## Decision

### A. Lifecycle, and the explicit design-versus-implementation authority determination

This is an OPS-0009 Lane G filing. While its pull request is open it is proposed prerequisite
governance only. It becomes effective only after independent full exact-head review, principal
exact-head acceptance, merge, immediate post-merge verification, and successful exact-head CI. The
author may commit, push, and open the draft PR but may not self-review, principal-accept, mark ready,
or merge.

**Determination: XASSET-0021 authorizes this unit both to define and to implement the minimal
mechanical subsystem in one coherent prerequisite PR.** The determination is made from the accepted
text, not from convenience:

1. §L requires this unit to define, as one reviewable contract, item 9 — "the smallest
   generator/validator/fixture mechanism necessary to **prove** that identical frozen inputs
   necessarily produce identical canonical bytes" — and item 10, "exact **rejection fixtures**
   covering every adversarial case in §M." Prose cannot prove byte identity, and a fixture is a
   concrete artifact rather than a description of one.
2. §M requires that this unit "must **supply** a closed validator/generator/fixture contract that
   **rejects** each of the following," then enumerates 29 conditions. "Rejects" is operational: a
   description rejects nothing.
3. §M's own limiting sentence is scoped to XASSET-0021, not to this unit: "This section requires
   future mechanical proof; it does not authorize that subsystem or an application **inside this
   filing**."
4. XASSET-0021's Alternatives Considered rejects closing the schema inside XASSET-0021 precisely
   because that work "is mechanical rather than economic, but still requires **its own bounded
   authority and exact-head review**." This filing is that bounded authority, and it carries its own
   independent exact-head review.
5. §O requires this unit to pass "successful exact-head CI," which is meaningful for executable
   code and tests.

The corrected independent review of XASSET-0021 (`4943931318`) reaches the same reading in its §2 and
§8, characterising the deferred work as "a new mechanical subsystem" whose defect was that it "would
have arrived unreviewed inside a correction commit."

Nothing in that determination extends to economics. §L's binding sentence controls throughout: this
unit "must remain purely mechanical and must not add economic evidence, parameters, endpoints,
portfolio rules, or policy."

### B. Controlling upstream identity

- methodology: `XASSET-0020`, accepted head `d2c0ce84f1922bc606c3de6983eb47266dbe4d72`, decision-file
  SHA-256 `f04ee116b7ed93165f621f65d91594557c5e4e3d0744d5f87ddfea5ccba999d2`, review `4943427551`,
  acceptance `5301699393`, merge `e7d66d93b5f7ab2ecd985a7a4bf680a118df6b0e`, post-merge verification
  `5301728726`, merge CI run `31878188273`;
- prerequisite closure: `XASSET-0021`, accepted head `afc3eef410dd3748c209053bdb8de7dd09c273bf`,
  review `4943931318`, acceptance `5302485718`, merge `5f94634bdfd0ff8ab603b8dd6ece2921033191df`,
  post-merge verification `5302525526`, merge CI run `31887814190`.

Any mismatch in that identity makes a future application ineligible.

### C. Exact application artifact identity

Exactly one, with no alternative:

| Element | Exact value |
|---|---|
| schema name | `level1_application` |
| schema version | `1.0` |
| canonical artifact path | `intelligence/level1_application/level1_application.json` |
| file format | JSON |
| encoding | UTF-8, no byte-order mark |
| newline | LF (`\n`) only, exactly one trailing LF, no CR anywhere |

Exactly one artifact exists under this schema. There is no cohort, manifest, or second file.

### D. Canonical serialization

The canonical form is this repository's already-accepted canonical convention, reused rather than
replaced. It is identical to the convention used by every sibling `canonical_record_hash()` and by
the retained RISK result artifacts, so no second serialization convention is introduced:

```
json.dumps(document, sort_keys=True, separators=(",", ":"),
           ensure_ascii=False, allow_nan=False) + "\n"
```

encoded UTF-8. This closes each required element exactly:

- **object/key ordering** — derived by `sort_keys=True`; never author-chosen;
- **list ordering** — canonically fixed per field in §E, never insertion-dependent;
- **whitespace and indentation** — none; compact separators only;
- **newline termination** — exactly one trailing LF;
- **string encoding/escaping** — UTF-8 with non-ASCII preserved (`ensure_ascii=False`);
- **boolean representation** — JSON `true`/`false` only;
- **null representation** — JSON `null` only; the strings `"null"`, `"none"`, and `""` are not null;
- **numeric representation** — integers only where §E permits a number. **Floats are barred anywhere
  in the document tree**, because their textual form is representation-dependent and XASSET-0021 §G
  requires exact arithmetic. Any future lawful exact value must be an exact-precision string carrying
  NUM-0001 provenance. `NaN` and `Infinity` are rejected outright;
- **duplicate keys** — rejected at parse time, before any other check;
- **extra fields** — rejected at every mapping level;
- **unknown enum values** — rejected against the closed vocabularies in §F.

Two semantically equivalent but byte-different records cannot both be lawful: an artifact's bytes are
re-serialized canonically and compared byte-for-byte against the file as committed.

### E. Complete closed field set

The authoritative machine-readable definition is `level1_application_schema.py`. Every mapping level
is closed: both extra and missing keys fail. The top level is exactly twelve keys, all required, none
nullable as a whole:

`schema_identity`, `methodology_identity`, `prerequisite_identity`, `application_authorization`,
`evidence_snapshot_identity`, `normalized_asset_state`, `evidence_snapshot`, `sleeves`, `pairs`,
`portfolio_reconciliation`, `reopen_triggers`, `authority_boundary`.

Canonical list orders, all fixed and none author-chosen:

- `evidence_snapshot` — exactly 35 entries, ascending `evidence_id`, each entry carrying exactly
  `evidence_id`, `path`, `sha256`, `source_content_sha256`, `source_class`, `governing_authority`,
  and `authority_lifecycle`, every one of which is frozen or mechanically derived and enforced by
  exact equality. `source_class` is derived from the evidence identifier and partitions the 35 items
  into exactly the six XASSET-0021 §C.1 classes (8/6/2/4/1/14); `governing_authority` and
  `authority_lifecycle` are verbatim transcriptions of that §C.1 enumeration, which also requires
  that "a future application must store the applicable lifecycle identity on every item";
- `sleeves` — exactly four, in canonical order `equity`, `fund_broad_market`, `fund_gld_defensive`,
  `crypto`;
- `pairs` — exactly six, in canonical order derived from the sleeve order. Each pair's `self_sleeve`
  and `counterpart_sleeve` are pinned to canonical sleeve order, so **a reversed pair is not
  expressible** and a duplicate pair fails its `canonical_pair_id` check;
- `driver_ledger` — exactly the six driver classes, in canonical order, on every pair;
- `deterministic_derivation_trace` — exactly the eleven steps of §H, in order, on every sleeve;
- `reopen_triggers` — exactly the seven identifiers of §I, in order.

Every field is economically non-authoritative. The artifact records governed states; it originates
none. **No field anywhere in the artifact is author-supplied free text.** Every value is either a
fixed constant, a closed-vocabulary value, or mechanically derived from the frozen snapshot, so one
governed state has exactly one lawful byte sequence.

`permitted_question`, `representation_scope`, `forbidden_implications`, `classification`,
`admission`, and `freshness_state` are deliberately **absent** from the evidence entry. No accepted
authority fixes an exact per-item value for any of them: they occur only in XASSET-0020 §O's
illustrative sketch, which XASSET-0021 §L expressly withdrew as authority. Carrying them as prose or
as caller-selected enum values would let one governed state have many lawful byte sequences, and
supplying values for them would require inventing content this unit is barred from inventing. They
are therefore removed rather than fabricated. Their governed content is unchanged and remains in
XASSET-0021 §§C.2-C.3, pinned by the snapshot identity and by all 35 per-file hashes.

### F. Closed vocabularies

Closed, exhaustive, and machine-enforced: evidence classification (`DRIVER`/`CONSTRAINT`/
`DISCLOSURE`); evidence admission; freshness; missingness; conflict; representation; driver
direction; constraint state; disclosure state; pair conclusion; sleeve outcome type; uncertainty
state; sleeve-versus-unassigned; reconciliation state; liquidity status; unassigned-capital
deployment status; provisional/adoption state; authorization status; trace output; and reopen-trigger
identifiers. No free-text synonym may control any outcome.

One vocabulary omission is deliberate and load-bearing: **`not_applicable` does not exist in the
driver-direction vocabulary.** XASSET-0021 §D holds that all six driver classes apply to every pair
and may not be marked inapplicable merely because evidence is missing, so the evasion is made
inexpressible rather than merely prohibited.

### G. Non-circular identity design, and the XASSET-0020 §O reconciliation

XASSET-0021 §L item 8 requires a non-self-referential lifecycle binding, and §M item 28 requires
rejecting "any committed artifact field that purports to contain the SHA of its own containing
commit." The corrected review's NOTE-2 asks this unit to state explicitly which reading it adopts of
XASSET-0020 §O's illustrative `application_identity: {authorization_decision, exact_head, frozen_at}`
group. **This unit adopts the reading NOTE-2 identifies:** XASSET-0020 §O was a floor that never
defined `exact_head`'s semantics, and §L item 5 still requires mechanically derived application
identities in canonical bytes, so the identity survives while only the self-referential value is
barred. Concretely:

- `authorization_decision` survives as `application_authorization.decision_id`;
- **`exact_head` is removed from the artifact entirely.** The application PR and head identity live
  in external Git/GitHub lifecycle metadata — the PR record, the independent review, and the
  acceptance and post-merge-verification comments — verified by review, and never inside the
  canonical bytes;
- `frozen_at` is removed as a wall-clock field and replaced by mechanically derived snapshot
  identity: `snapshot_id`, `source_count`, `source_tree_identity`, and `evidence_manifest_sha256`,
  the last derived by hashing the canonical form of the frozen evidence manifest itself.

Identities that *are* carried in canonical bytes reference commits other than the artifact's own
containing commit — the XASSET-0020 accepted head and merge commit, the XASSET-0021 accepted head and
merge commit, the frozen source-tree identity, and this decision's own accepted head — so none is
circular. A defence-in-depth scan independently rejects the key names `exact_head`,
`application_exact_head`, `self_commit`, `containing_commit`, `artifact_commit_sha`, and their
variants anywhere in the tree, in addition to the closed key sets that already exclude them.

### H. Metadata determinism

Canonical bytes contain no author, reviewer, wall-clock timestamp, execution time, hostname,
temporary path, branch name, environment value, or hash-map iteration artefact. Key order is derived
by sorting; list order is canonically fixed; the generator has no clock, filesystem, environment,
network, or randomness dependency. An independent scan rejects a closed set of nondeterministic key
names (`generated_at`, `timestamp`, `frozen_at`, `author`, `hostname`, `branch`, and others) anywhere
in the tree. This is a deliberate divergence from the retained RISK result artifacts, which carry
`generated_at_utc`; §L item 5 forbids that here.

### I. Deterministic trace contract

One trace structure, on every sleeve, fully populated, in exactly this order, with `step_index`
matching position: `frozen_input_identity_verified`, `evidence_admission_evaluated`,
`evidence_classification_applied`, `source_owned_freshness_recorded`, `driver_ledger_populated`,
`missingness_and_conflict_propagated`, `representation_sensitivity_evaluated`,
`endpoint_authority_evaluated`, `constraint_effects_applied`, `sleeve_outcome_determined`,
`unassigned_capital_reconciled`.

Each step carries exactly `step_id`, `step_index`, `inputs_referenced`, and `output_recorded`. Under
the frozen snapshot each step has **exactly one lawful `output_recorded` value**, so the trace is
derived rather than author-described. A future author cannot decide which steps "seem useful": an
omitted, added, reordered, or free-text step is rejected.

### J. Reopen-trigger contract

Exactly the seven XASSET-0021 §Q triggers, as machine-state identifiers in fixed canonical order. No
prose-selected list; any addition, omission, reordering, or free-text substitution is rejected.

### K. Generation contract and implementation

`level1_application_generator.py` consumes a closed two-key frozen input
(`application_authorization`, `schema_accepted_head`) and refuses any missing, extra, or invalid
input rather than filling a gap with a default. There is deliberately no per-evidence input: the
entire evidence ledger is derived from the frozen snapshot, so a caller cannot phrase, select,
reorder, or omit any part of it. It queries no market, network, or provider data; reads no current
holdings,
targets, gates, or weights; chooses no economic value and no endpoint; and makes no abstain-versus-
point/range judgment of its own — every economic state it writes is a transcription of a closure
already fixed by XASSET-0020/XASSET-0021 under the frozen snapshot. Identical frozen inputs produce
byte-identical output, proven across repeated runs and across permuted input mapping order.

### L. Validator contract and implementation

`level1_application_validator.py` is fail-closed and rejects, at minimum, every condition in
XASSET-0021 §M items 1–29: identity drift; unfrozen evidence; missing, extra, duplicate, or reversed
sleeve/pair records; missing evidence treated as neutral; transitive inference; a RISK
`unable_to_determine` state recoded as direction; a historical or current target used as an endpoint;
automatic midpoint selection; rounding that could change an outcome; unclosed materiality judgment;
historical evidence treated as a current positive driver; unassigned capital converted to cash;
forced four-sleeve exhaustion; liquidity as a fifth sleeve or as numeric zero; any point or range
despite absent endpoint authority; current holdings or targets as priors; score, confidence, tally,
utility, optimizer, or hidden weighting; Level-2 leakage; policy, adoption, deployment, or trading
language; extra or omitted fields; wrong types, invalid enums, or free-text substitution for a
governed enum; alternate list or field ordering; alternate encoding, newline, whitespace, or key
ordering; noncanonical null or numeric representation; trace mutation; reopen-trigger mutation;
schema name or version drift; a self-referential commit SHA; and non-byte-identical regeneration.

The byte-identity check is independent of the generator: bytes are parsed and re-serialized through
the canonical serializer and compared, so the validator can detect noncanonical bytes without the
generator existing. The structural checks are implemented independently of the generator's
construction logic.

The validator is mechanical authority only. It never decides an economic question, never chooses an
endpoint or representation, and never grants application authority. A missing artifact directory is a
valid zero-coverage state, matching every sibling Intelligence validator.

### M. Fixtures and golden bytes

`test_level1_application.py` supplies the minimum sufficient fixtures: one canonical valid document,
proof of byte-identical repeated generation, and adversarial rejection fixtures covering every §M
case. Every fixture is synthetic and in-memory. **No fixture is written under `intelligence/`, no
artifact directory is created, and no fixture uses or implies a portfolio percentage.** Where a
fixture represents a governed abstention state it does so only as a test value; no fixture is, or may
become, an application record or a policy result.

The frozen evidence manifest transcribed into the schema module is independently re-verified by test
against the live repository tree: all 35 paths exist and all 35 SHA-256 values match.

### N. CM-27 closure

`CM-27 application_schema` may be reclassified from `SEPARATE_PREREQUISITE_REQUIRED` to
`CLOSED_DETERMINISTICALLY` **only upon this decision becoming effective** — independently reviewed at
its exact head, principal-accepted, merged, post-merge verified, and green on exact-head CI. The
conditions are that §§C–G above are present and reviewable: one exact schema name, version, path,
format, and encoding; one canonical serialization sufficient for byte-identical reproduction; the
complete recursively closed field set with types, nullability, vocabularies, ordering, and fixed or
mechanical derivation; closed vocabularies for every governed state; and mechanically derived,
non-circular identities with no wall-clock or author-chosen metadata in canonical bytes.

This filing does not claim that closure retroactively and does not edit XASSET-0021's accepted matrix.
Until this decision is effective, CM-27 remains `SEPARATE_PREREQUISITE_REQUIRED`.

### O. CM-28 closure

`CM-28 deterministic_trace_and_repeatability` may be reclassified on the same effectivity condition,
and only if: the deterministic generation contract is exact (§K); the canonical serializer is exact
(§D); the validator and fixtures are sufficient (§§L–M); identical frozen inputs have exactly one
lawful byte output; and the non-circular lifecycle binding is solved (§G). All five are satisfied by
this filing's implementation, subject to independent review.

### P. Application-authority boundary — authority remains WITHHELD

XASSET-0021 §O installs a double gate: "Only after that effectivity may a later governance decision
determine whether one application PR can be authorized. Neither this decision nor the future
prerequisite may silently treat application authority as automatic."

**This decision therefore authorizes no application, including an abstention-only application.**
Closing CM-27 and CM-28 removes the mechanical obstacle; it does not grant authority. Schema
prerequisite closure is not application authorization.

That boundary is enforced mechanically, not merely stated. `APPLICATION_AUTHORIZATION_REGISTRY` in
the schema module is **empty**. It maps an application-authorization decision id to the exact
XASSET-0022 accepted head that decision authorizes against, so a lawful artifact must name a
registered decision, carry `authorization_status: granted`, **and** carry exactly the head bound to
that decision — registry membership alone is insufficient, and no arbitrary 40-hex value can pass.
Both the generator and the validator enforce all three independently. Consequently no artifact can
be generated or validated today, and a future separate governance decision must grant authority and
record both the decision id and its bound head before any application may begin. A test asserts the
production registry is empty.

### Q. Economic freeze

This unit alters no accepted economic consequence. Unchanged and, where applicable, mechanically
enforced under the frozen snapshot: the missing broad-market↔GLD and broad-market↔crypto pairs remain
`unable_to_determine`; no lawful current Level-1 point or range endpoint exists and
`point_or_range_or_null` must remain null; no midpoint, historical target, or current-weight prior may
create one; no transitive pair inference and no representation averaging is permitted; there is no
discretionary materiality threshold; freshness remains source-owned; all four accepted RISK family
dispositions remain `unable_to_determine`; liquidity remains unresolved with a null — not zero —
numeric value and is not a fifth sleeve; `UNSIZED_UNASSIGNED_CAPITAL` is preserved with
`deployment_status: prohibited_without_future_governance`; Level-1 economic sizing is not complete;
and Level-2 remains blocked.

### R. Legacy and current-anchor prohibition

Mechanically scanned and rejected anywhere in an artifact: the legacy numeric anchors `18.67`,
`14.67`, `16.67`, and `33.32`; `XASSET-0016` and `XASSET-0018` outputs; `holdings.yaml`,
`targets.yaml`, and `gates.yaml` references; `current_weight`, `current_target`, `current_holding`,
and incumbency priors; and score, confidence, tally, utility, rank, optimizer, solver, grid, sweep,
`target_pct`, `sleeve_weight`, and `allocation_pct` fields. Neither the schema, the generator, the
validator, nor the tests reads any current holding, target, gate, weight, margin, leverage, buffer,
chart, or ladder input.

### S. Governance package and WORKSTREAMS synchronization

This filing touches exactly eight tracked files: this decision; `governance/decisions.yaml` (one
catalog row); `operations/WORKSTREAMS.yaml` (additive XASSET-0021 closeout and XASSET-0022 lane
facts); `test_portfolio_hq_dashboard_decisions.py` (the two mechanical decision-count assertions);
and the four mechanical modules `level1_application_schema.py`, `level1_application_generator.py`,
`level1_application_validator.py`, and `test_level1_application.py`.

No supporting audit is needed: the exact schema, serialization, vocabularies, contracts, and closure
conditions are contained here and in the machine-readable modules. No Intelligence, research-result,
allocator, target, holding, gate, margin, chart, ladder, or protected portfolio file is changed. No
`intelligence/level1_application/` directory is created.

### T. Reopen triggers

Reopen XASSET-0022 if: XASSET-0020's or XASSET-0021's effective identity changes; any frozen §C path
or hash changes; a new evidence class, direct pair, representation rule, endpoint authority, or
freshness rule is proposed for use; the liquidity or Level-2 architecture changes a boundary relied
on here; an accepted RISK identity or disposition changes; review or execution reveals schema
ambiguity, hidden arithmetic, or nondeterminism; or a future application would require an artifact
field, vocabulary value, trace step, or reopen trigger not defined here.

### U. Absolute non-authorization

This decision does not apply XASSET-0020 and produces no sleeve point, range, weight, target,
allocation, example portfolio, application record, Level-2 membership or sizing, liquidity or cash
amount, reserve amount, debt-reduction amount, margin or leverage rule, chart, ladder, deployment,
optimizer, backtest, trade, order, brokerage action, or portfolio-policy adoption. It changes no
current portfolio configuration and grants no application authority.

### V. Bounded correction following independent review 4944055540

Independent full exact-head review `4944055540` of head `de6b5aa9e303b3e39d7024387332d046910af9f5`
returned CHANGES REQUIRED — 0 BLOCKING / 2 MAJOR / 2 MINOR / 2 non-actionable NOTE. All four
actionable findings were reproduced before any change and are resolved:

**MAJOR-1 — author-discretionary evidence provenance.** Reproduced: five per-evidence fields accepted
arbitrary content, and one governed state yielded **nine** distinct valid canonical byte sequences.
Resolved by eliminating the discretion rather than constraining it: `governing_authority` and
`authority_lifecycle` are now frozen per source class as verbatim §C.1 transcriptions and enforced by
exact equality; `source_class` is derived mechanically; and `permitted_question`,
`representation_scope`, `forbidden_implications`, `classification`, `admission`, and
`freshness_state` are removed for the reasons in §E. The generator's per-evidence input is deleted
entirely, so its input contract is two keys. One governed state now yields exactly **one** lawful
byte sequence.

**MAJOR-2 — bool/int type confusion.** Reproduced: because `False == 0` and `True == 1`,
`debt_excluded`, every `authority_boundary` boolean, `source_count`, and `step_index` each accepted a
byte-distinct invalid encoding. `_require_exact` is now type-strict, requiring identical concrete
types before equality, which makes bool and int mutually unsatisfiable. All 25 call sites were
audited; no other exact-value comparison carried the same ambiguity.

**MINOR-1 — NaN/Infinity crash path.** Reproduced: `json.loads` accepted the non-standard constants
and canonical re-serialization then raised an uncaught `ValueError`. Parsing now rejects them via
`parse_constant`, and canonical serialization is additionally guarded, so all three return an
ordinary structured validation failure.

**MINOR-2 — `schema_accepted_head` unbound.** Reproduced: any 40-hex value validated. The
authorization registry is now a mapping from decision id to the exact bound accepted head, and both
the generator and the validator independently require the artifact's head to equal it.

NOTE-1 (a dead no-op branch, since removed with the code it sat in) and NOTE-2 (a docstring wording
point) were non-actionable; scope was not expanded to polish them.

The correction changes no economic rule, evidence conclusion, sleeve allocation, endpoint, or policy.
The 35 frozen source identities are byte-unchanged and still reconcile 35/35 against the repository
tree; the evidence-manifest identity is unchanged; application authority remains WITHHELD with an
empty production registry; and XASSET-0021's accepted matrix is untouched.

## Rationale

The honest reading of XASSET-0021 is that the remaining obstacle is mechanical, not economic, and
that a mechanical obstacle is closed by building the mechanism and submitting it to review — not by
describing it again. §L item 9 asks for proof of byte identity; only executable artifacts can supply
that. Deferring once more would reproduce the defect the original BLOCKING finding identified: an
assertion of determinism with nothing from which the only lawful bytes could be determined.

Reusing the repository's existing canonical convention rather than inventing a second one is
deliberate. The convention is already accepted, already used by every sibling validator's content
hash, and already used on disk by the retained RISK result artifacts, so byte-identity here is
consistent with byte-identity everywhere else in this repository.

Making evasions inexpressible is preferred to prohibiting them in prose wherever the schema allows
it: `not_applicable` is absent from the driver-direction vocabulary, pair members are pinned to
canonical order so a reversed pair cannot be written, floats are barred so unsupported precision
cannot enter, and the authorization registry is empty so no artifact can validate. A rule that cannot
be expressed cannot be violated by an author acting in good faith or otherwise.

## Alternatives Considered

**Define the contract and defer implementation to yet another unit.** Rejected: §L item 9 requires a
mechanism that proves byte identity and §M requires a contract that rejects 29 conditions, neither of
which prose satisfies. A further deferral would leave CM-27 and CM-28 open with no closer date and no
new information.

**Use YAML for the artifact, matching the Intelligence record convention.** Rejected: YAML has no
equally closed byte-level convention in this repository, and byte-identical reproduction is the
explicit requirement. JSON with the accepted compact canonical form is already used on disk for the
retained RISK result artifacts.

**Permit floats for future numeric endpoints.** Rejected: float text form is
representation-dependent, and XASSET-0021 §G requires exact arithmetic with no rounding that could
change an outcome. An exact-precision string with NUM-0001 provenance is the lawful carrier. No
endpoint exists under the frozen snapshot in any case.

**Carry the application PR head inside the artifact, as XASSET-0020 §O's sketch suggested.**
Rejected as circular: writing the artifact's own containing commit SHA into the artifact changes that
SHA. The identity is preserved as external Git/GitHub lifecycle metadata instead, which is the
reading the corrected review's NOTE-2 identified.

**Treat CM-27/CM-28 closure as also granting application authority.** Rejected: XASSET-0021 §O
expressly forbids treating application authority as automatic, and requires a later separate
governance decision. The empty authorization registry enforces that mechanically rather than relying
on prose.

## Consequences

If this decision completes its full lifecycle, the mechanical prerequisite named in XASSET-0021 §L is
closed and CM-27 and CM-28 may be reclassified `CLOSED_DETERMINISTICALLY`. Application authority
nevertheless remains withheld: a separate future governance decision must grant it and be recorded in
the authorization registry before any application PR may begin. Under the current evidence boundary,
any eventual compliant application still could not lawfully create a point or range and would have to
preserve abstention and unassigned capital; a non-abstaining result would additionally require
separately accepted evidence and endpoint authority. Portfolio policy, liquidity, Level 2, targets,
holdings, and execution remain unchanged.
