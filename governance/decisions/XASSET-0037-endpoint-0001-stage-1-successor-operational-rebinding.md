---
decision_id: XASSET-0037
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_successor_operational_rebinding.py
---

## Context

### Live preflight

Independently verified from live GitHub, live git, and live module state before any file was
written. Nothing below is inherited from a prior session's summary.

| Fact | Verified value |
|---|---|
| GitHub `main`, `origin/main`, local `HEAD` | `3e5de8f85c69c2e5dc2b75421446b5db996d7cf1` — all three identical |
| That commit's identity | the `XASSET-0036`-authorized executable-package merge (PR #336), parents `be90aeef…` and `07519f86…`, re-derived via `git log --pretty='%H %P'` |
| Merge-tree drift on PR #336 | **zero** — merge tree `c7d3e07f…` is byte-identical to the accepted head's own tree |
| PR #336 | merged, `merged_by` `Mast3rkey`, 5 commits, 17 files |
| Open pull requests | **0** |
| Working tree · worktrees | clean · sole worktree, no competing mutation lane |
| `XASSET-0037` identifier | unused — 0 hits in `governance/decisions.yaml`, no decision file, no code reference |
| Decision catalog | **138** entries, `issues == ()` |
| `LOAD_BEARING_RELPATHS` | exactly **9** |
| Canonical pins (V6) | `PROTOCOL_V1.md` `86b2a5e8…e40c13` · `pre_registration.yaml` `e993df9f…3f149d4` — both match |
| Frozen universe | **680** constructions · **48** cells · `73c0965e…5224` — match |
| `stage_1_executability.executable` | `False`, with `executable_is_never_the_authorization_source: True` |
| `new_execution_is_authorized()` | `(False, …)` — "no attestation present" |
| `AUTHORIZATION_ROOT` (`/var/tmp/phq-endpoint0001-stage1-authorization`) | **absent** |
| `ATTEMPT_1` (`ENDPOINT-0001::STAGE_1::ATTEMPT_1`) | intact, unclaimed, unconsumed |
| `stage1_results.yaml` · claim · completion · ledger | **none exists** |

No `risk_lane_boundary` protected `RISK` result path was read, listed, opened, or referenced.

### The question this unit answers

`XASSET-0036` authorized the `XASSET-0030` §G.B steps-2–7 executable package, and PR #336 delivered
it. `XASSET-0030` §G.B step 8 requires **one** successor operational-authorization / load-bearing
rebinding lifecycle against those exact merged bytes. This unit is that lifecycle.

## Decision

### A. Determination — `SUCCESSOR_OPERATIONAL_REBINDING_PERFORMED`

The effective structural authorization source for `ENDPOINT-0001` Stage 1 is rebound from
`XASSET-0029` (PR #328) to **`XASSET-0037`**, against the exact merged bytes of the
`XASSET-0036`-authorized executable package (PR #336, merge `3e5de8f8…`).

**`XASSET-0029` is preserved, not invalidated.** Its own six-gate lifecycle really closed, and it
remains valid accepted history — still bound, still verified against the git object store. What
changed is not who established the mechanism but **which merged tree the mechanism proves
load-bearing identity against**.

**This is not an activation step.** Stage 1 remains **UNARMED** and **NOT EXECUTABLE**, `ATTEMPT_1`
is intact, unclaimed, and unconsumed, and §G.B steps 9–11 are neither performed nor authorized.

### B. The fail-closed condition, reproduced before it was corrected

`XASSET-0030` §D recorded **in advance** that a lawful correction of the §C enforcement defect
would deliberately create enforcement drift, leaving Stage 1 non-armable "until a successor
operational-authorization or reconciliation lifecycle lawfully binds the new load-bearing
implementation."

That prediction was verified against live state rather than assumed. The nine load-bearing paths,
evaluated against the authorized merged `XASSET-0029` tree (`3cc15d58…`):

| Path | Status against the `XASSET-0029` merged tree |
|---|---|
| `governance/decisions/XASSET-0036-…-authorization.md` | **absent** |
| `level1_stage1_runner.py` | **absent** |
| `level1_stage1_result_validator.py` | **absent** |
| `level1_endpoint_evidence_preregistration_validator.py` | **drift** `f0d73166…` → `840b558b…` |
| `level1_stage1_execution_authorization.py` | **drift** `9376329d…` → `41a0c2f8…` |
| `research/level1_endpoint_evidence/PROTOCOL_V1.md` | **drift** `6c34cbbc…` → `86b2a5e8…` |
| `research/level1_endpoint_evidence/pre_registration.yaml` | **drift** `6e0c07a8…` → `e993df9f…` |
| `governance/decisions/XASSET-0029-…-authorization.md` | match |
| `level1_construction_universe_closure_validator.py` | match |

Driven end-to-end through the real public predicate — with the real local git object store, an
honest stand-in recording PR #328's real governance facts, and an **isolated temporary lane** —
`validate_authorization_document` returned `valid=False` with those seven load-bearing errors;
`write_authorization` **refused to put the attestation on disk**; and
`new_execution_is_authorized` returned `False`. The temporary lane directory was left empty.
**The real lane was never created, inspected, or touched, and no real `ATTEMPT_1` was consumed.**

**An obsolete authorization that cannot authorize a changed package is the mechanism working.**

### C. Four structurally distinct identities

The single largest failure mode available to a rebinding is overloading one "predecessor" field
across relationships that are not the same relationship, and thereby binding the wrong tree. Each
gets its own constants, its own attestation block, and its own git-derived verification.

| Relationship | Identity | Role | Constants |
|---|---|---|---|
| Structural closure predecessor | `XASSET-0028` | the construction universe | `PREDECESSOR_*` — **unchanged in name, meaning, and value** |
| Historical operational authorization | `XASSET-0029`, PR #328, merge `3cc15d58…` | established the mechanism | `HISTORICAL_OPERATIONAL_AUTHORIZATION_*` |
| Package authority | `XASSET-0036`, PR #335, merge `be90aeef…` | authorized the package's creation | `PACKAGE_AUTHORIZING_*` |
| Executable package | PR #336, merge `3e5de8f8…`, head `07519f86…`, base `be90aeef…` | the exact merged bytes bound | `EXECUTABLE_PACKAGE_*` |

`PREDECESSOR_DECISION` is deliberately **not** repointed at `XASSET-0029`. It means XASSET-0028's
structural closure and nothing else; repointing it would be exactly the overloading this section
exists to prevent.

The **authority** that permitted the package (`XASSET-0036`) and the **package** itself (PR #336)
are likewise separate: one is a governance record, the other is a merged tree, and a rebinding that
conflated them could bind a decision while leaving the code it authorized unbound.

### D. What the rebinding binds and proves

`AUTHORIZING_DECISION` → `XASSET-0037`; `AUTHORIZING_PULL_REQUEST` → **337**; `REVIEWED_BASE_SHA` →
`3e5de8f85c69c2e5dc2b75421446b5db996d7cf1`.

**Provenance of the bound pull-request number, stated exactly rather than flatteringly.** The
literal `337` was first written *before* the draft pull request existed, as the next-sequential
number, and then **verified against the real draft once it was opened** — it is #337, and the two
agree. The load-bearing property is the verification, not the authoring order: a wrong number fails
closed at `verify_lifecycle_against_truth`, which fetches that exact pull request from durable
governance metadata and compares its head, merge, and merged state. Had the real number differed,
the constant would have been corrected on the branch before review.

Every check the mechanism already performed is retained unchanged. Added on top, each derived from
the local git object store rather than declared:

1. PR #336's merge has parents `[be90aeef…, 07519f86…]`, **in that order**;
2. PR #336's merge tree is **byte-identical** to its accepted head tree — zero package merge drift;
3. PR #336's merge is an **ancestor** of the successor merge — a rebinding cannot bind a package
   outside its own history;
4. `XASSET-0029`'s and `XASSET-0036`'s merges are likewise ancestors;
5. `XASSET-0029`'s merge really has the parents the successor claims to inherit from;
6. the **outcome-producing bytes** — `level1_stage1_runner.py` and
   `level1_stage1_result_validator.py` — are byte-identical at the package's reviewed head, the
   package's merge, the successor's reviewed head, the successor's merge, **and** the working tree;
7. the **transitive outcome-producing surface** — the derivation symbols those two modules import
   from `level1_endpoint_evidence_preregistration_validator.py` — projects identically at the same
   five anchors (§D.1, added by the bounded correction below).

Points 6 and 7 are §G.B's own invariant, mechanised: *no outcome-producing executable code may be
created, changed, or left outside the bound execution identity after the final rebinding and before
`ATTEMPT_1`.* A silent runner edit — or a silent edit to the code the runner imports to decide and
order outcomes — smuggled into the rebinding that binds it **fails closed**. Neither outcome-producing
module is modified by this unit, and the projected derivation surface is identical to the accepted
PR #336 package.

#### D.1 — The transitive surface, and why it is projected rather than byte-compared

Both outcome-producing modules `import level1_endpoint_evidence_preregistration_validator as PV` and
call its `generate_cell_universe`, `derive_candidate_disposition`, `derive_cell_outcome`,
`derive_roll_up_outcome`, `required_g2_gate_result` and `is_reading_dependent`, against its gate,
disposition, and reading vocabularies. That module therefore *decides and orders* the 680 outcomes
and sits squarely inside §G.B's definition.

Whole-file equality is the wrong instrument for it: the same file also carries the canonical
lifecycle constants, the pin-succession checks, and the rebinding-block validator — **authorization-only
code this rebinding must lawfully change**. Requiring byte equality against the package would make a
lawful rebinding impossible. What is bound instead is a deterministic **semantic projection**:

- **Seeds** — the exact 18 top-level symbols the two consumers actually access, declared in
  `OUTCOME_PRODUCING_PROJECTION_SEEDS` and independently re-derived from the consumers' own source by
  the test suite, so the production tuple is never its own oracle.
- **Closure** — the transitive closure of those seeds over the module's own top-level symbols: 26 in
  total, reaching dependencies such as `CANDIDATE_DISPOSITIONS`, `CELL_OUTCOMES`, `cell_id_of`,
  `map_g2_reading`, and `generate_family_slot_grid` that no seed names directly.
- **Serialization** — sorted by symbol, location-free `ast.dump`. Reordering definitions or reflowing
  whitespace does not change identity; any change to a value, branch, comparison, or ordering does.
- **Docstrings excluded** — deliberate, narrow, and disclosed: prose cannot decide, order, serialize,
  write, or materially alter an outcome, so a docstring edit is not an outcome-semantics change. Tested
  in **both** directions.
- **Fail-closed** — unparseable source, a missing or renamed seed, a duplicated top-level symbol, an
  unreadable anchor, or an unserializable node each raise rather than yielding a partial surface.
- **Precision as well as sensitivity** — an edit to a real top-level constant *outside* the closure
  (`FAILURE_DISPOSITIONS`) correctly does **not** fire. A projection that fired on it would be byte
  equality under another name.

Determinism boundary, stated rather than overclaimed: `ast.dump`'s exact text is stable for a given
interpreter, not guaranteed identical across Python versions. That is sufficient, because every
projection compared here is computed by one interpreter in one validation pass and is never persisted
or compared across processes.

### E. The trust boundary grows, and nothing is removed

`LOAD_BEARING_RELPATHS` **9 → 10**, using the **existing exact-byte mechanism unchanged** — expected
identity is still derived from the merged git tree at validation time, never from a hard-coded
constant. `XASSET-0036` §E.6's stated preference for that mechanism holds and no concrete technical
reason to depart was found, so none is argued.

The single addition is the `XASSET-0037` decision file itself, on exactly the footing `XASSET-0029`
and `XASSET-0036` already occupy for their own authorizations: the decision supplying the effective
structural authorization must sit inside the identity it authorizes, or an attestation could
authenticate perfectly while its own governing text had been edited afterwards.

**No load-bearing path is removed and no exact-byte check is weakened.** Every one of the nine
existing paths is retained, and the pin-succession check is strengthened rather than relaxed: a
successor pin equal to **any** predecessor generation's accepted pin — `XASSET-0036`'s,
`XASSET-0029`'s, `XASSET-0028`'s, or `XASSET-0027`'s — is now refused, so a pin cannot be copied
forward *or* reverted.

### F. Canonical amendment — V6 → V7, authorization language only

`PROTOCOL_V1.md` and `pre_registration.yaml` are amended in lockstep. The amendment is confined to
successor-lifecycle truth:

- `stage_1_execution_may_begin_only_after`, `stage_1_executability.blocking_prerequisite`, and
  `stages.stage_1.executable_only_after` name the `XASSET-0037` lifecycle, with `XASSET-0029`'s
  values retained in explicitly predecessor-named fields;
- `stage_1_operational_authorization` keeps `established_by: XASSET-0029` — historical truth, not
  rewritten — and gains `rebound_by` and `effective_structural_authorization_source`;
- a new `successor_operational_rebinding` block records the four distinct identities, that the
  rebinding is not an activation step and adds **zero** activation authorizations, that the
  historical operational authorization is **not** invalidated, that the enforcement drift was
  recorded in advance, and that no load-bearing path was removed and no exact-byte check weakened;
- `must_bind_exactly` and `must_fail_closed_on` gain the successor-rebinding entries.

**Explicitly unchanged**: every gate's index, question, class, controlling authority, and failure
disposition; every disposition rule; B1, B2, and B3; `comparison_subject_kind`; `unordered_pair_id`;
every construction identity; universe membership, ordering, and cardinality; and the universe hash
`73c0965e…5224`, independently regenerated after the amendment and unchanged at **680** / **48**.

<!-- XASSET-0037-HASH-PINS-V1
protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md
protocol_sha256: 367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971
preregistration_path: research/level1_endpoint_evidence/pre_registration.yaml
preregistration_sha256: 768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1
predecessor_protocol_sha256: 86b2a5e8674247698ac592ce4734744f940b4a119ffda5fd702bc3cbf3e40c13
predecessor_preregistration_sha256: e993df9f41d2f5352e51c9921dd006d50ab69518a730d37def106696b3f149d4
-->

- `PROTOCOL_V1.md`: `367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971`
- `pre_registration.yaml`: `768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1`
- Predecessor (`XASSET-0036` executable package, retained): `86b2a5e8…e40c13` / `e993df9f…3f149d4`

Pins were recomputed **once**, after every permitted canonical and enforcement byte had stabilized.

### G. Rebinding is not arming — `XASSET-0029` §E preserved unweakened

`XASSET-0029` §E terminates the activation regress on a step that **changes no repository state** —
the runtime attestation. A rebinding changes repository state extensively, so it is categorically
outside the step §E terminates. `XASSET-0036` §B.4 already reached this conclusion for the
implementation package, on the same reasoning, and it applies unchanged here.

`XASSET-0030` — accepted **after** `XASSET-0029` — expressly anticipates this lifecycle: §D records
that a lawful correction "deliberately creates enforcement drift, and Stage 1 becomes non-armable
**until a successor operational-authorization or reconciliation lifecycle** lawfully binds the new
load-bearing implementation," and §G.B step 8 requires "**one** successor operational-authorization
/ load-bearing rebinding lifecycle." `XASSET-0036` §D restates it: after the package and "the
required successor operational-rebinding lifecycle (§G.B step 8) separately complete, **the final
activation remains the external one-shot runtime attestation and the operator's act — not another
merged activation PR.**"

**This decision adds one rebinding and ZERO activation authorizations.**
`stage_1_executability.executable` stays `false` permanently and keeps its enforced-false check.
**No committed value in this repository authorizes Stage-1 execution**, and merging `XASSET-0037`
authorizes nothing.

### H. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

§P.1's exactly-one Stage-1 **evaluation/results** PR is **not consumed, replaced, amended, or
counted against** by this unit, on the same grounds `XASSET-0036` §C recorded: §P.1's PR "may make
no production configuration change," and this rebinding is nothing but production configuration
change; §P.1's deliverable is a results document, and this produces none; and §P.1's PR sits after
arming while this sits before it. After this merges, §P.1's budget is exactly what it is today:
**one, unspent.**

### I. Authority withheld — absolute

This decision does **not** perform, and does not authorize:

- `XASSET-0030` §G.B steps 9, 10, or 11;
- generating any external attestation;
- creating `AUTHORIZATION_ROOT`, or `READY` / `CLAIMED` / `COMPLETED` lane state, or any ledger
  entry;
- arming, claiming, completing, executing, or recovering any Stage-1 execution;
- evaluating any gate for any registered construction;
- creating `stage1_results.yaml` or any real per-construction disposition, cell outcome, or roll-up;
- consuming any part of `ATTEMPT_1`;
- any Stage 2 work, evidence acquisition, or market, fundamental, or economic data acquisition;
- reading, listing, opening, or referencing any `risk_lane_boundary` protected `RISK` result path;
- resolving `XASSET-0024` §K.1, or amending `XASSET-0020` §E.1;
- reopening, re-deriving, or re-arguing B1, B2, or B3;
- changing any gate semantics, disposition, construction identity, universe membership, ordering,
  cardinality, or universe hash;
- consuming `XASSET-0027` §P.1's reserved results PR;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders.

### J. Effectivity

This rebinding becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge — the repository's own six
`REQUIRED_LIFECYCLE_GATES` plus `OPS-0009` §6's exact-head discipline:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own
   CI run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure, including merged-successor identity
   verification.

**None is individually sufficient.** Opening this PR rebinds nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not; and post-merge verification without a successful
exact merge-commit CI run does not. **Only complete closure of all seven does** — and even then,
Stage 1 becomes *armable*, never *armed*.

## Rationale

`XASSET-0030` §D is the reason this filing exists in the shape it does. It recorded the enforcement
drift **before** the package that would cause it was even authorized, and said plainly that the cost
was "a cost of the correction, not an argument against it — and it is recorded here so the successor
scopes it up front rather than discovering it at arming time." The successor did scope it up front,
and found the predicted state exactly.

**Why the identities are split four ways rather than folded.** The module already carried one
`PREDECESSOR_*` notion, meaning XASSET-0028's structural closure. Three further relationships
arrived at once — a superseded operational authorization, a package authority, and a merged package
— and every one of them is a "predecessor" in loose English. Folding any of them into the existing
field would have produced a module where the same constant meant two different commits depending on
which sentence you read, and where a future editor correcting one meaning would silently break the
other. Four relationships, four constant groups, four attestation blocks, four verifications.

**Why the outcome-producing bytes get their own check.** §G.B's invariant is not "the runner is
load-bearing"; it is that outcome-producing code may not be *created or changed* outside the bound
identity after the final rebinding. Membership in `LOAD_BEARING_RELPATHS` proves the first half.
The second half needs the byte-equality chain across the package's head, the package's merge, the
successor's head, the successor's merge, and the working tree — otherwise the rebinding is exactly
the place where an unreviewed runner change could enter, against a non-rerunnable `ATTEMPT_1`.

**Why the canonical amendment is small.** Everything the semantic sequence `XASSET-0030` through
`XASSET-0035` settled is already reconciled into the canonical artifacts by the package. The only
thing not yet true in them was *which lifecycle is operative*. Amending more would mean re-opening
resolved partitions to no benefit; amending less would leave the canonical files asserting a spent
precondition as current.

**Why `established_by` is not rewritten.** `XASSET-0029` did establish the mechanism. That is a
historical fact, and this repository's convention — applied by `XASSET-0028` to `XASSET-0027`, by
`XASSET-0029` to `XASSET-0028`, and by `XASSET-0036` to `XASSET-0029` — is that accepted history is
retained verbatim and superseded through explicitly successor-named fields, never overwritten.

## Alternatives Considered

**Amend `XASSET-0029` in place to bind the new tree.** Rejected. It would rewrite an accepted
decision to describe bytes it never saw and a lifecycle it never underwent, and would leave no
record that the drift ever existed — destroying precisely the audit trail `XASSET-0030` §D created
in advance.

**Repoint `PREDECESSOR_*` at `XASSET-0029` and add nothing.** Rejected. It is the smallest diff and
the largest hazard: one constant would mean XASSET-0028's structural closure in the canonical
contract and XASSET-0029's operational authorization in the code, with no mechanism able to tell
which was intended. This is the specific failure the four-way split exists to prevent.

**Bind only the runner and result validator, leaving the decision file out.** Rejected. `XASSET-0029`
and `XASSET-0036` are both load-bearing for their own authorizations; excluding `XASSET-0037` would
make the effective structural authorization the only governing text editable after arming without
detection.

**Remove `XASSET-0029` from `LOAD_BEARING_RELPATHS` as superseded.** Rejected outright. Removing a
load-bearing path weakens exact-byte checking to make validation convenient — the one thing a
rebinding must never do. A superseded authorization is still part of the bound identity's history.

**Treat the rebinding as an activation PR and stop, on `XASSET-0029` §E grounds.** Rejected. §E's
own stated terminating condition is a step that changes no repository state; a rebinding changes it
extensively. `XASSET-0030` §D and §G.B step 8, and `XASSET-0036` §D, all accepted after
`XASSET-0029`, expressly require this lifecycle. Reading §E to forbid it would make §G.B step 8
unperformable and strand the package permanently non-armable.

**Perform steps 8–11 in one pass.** Rejected. Steps 9–11 are read-only verification, fail-closed
drift handling, and the attestation/arm/claim/run. Folding the run into the lifecycle that binds it
would let unreviewed bytes reach `ATTEMPT_1`, which is the exact error `XASSET-0030` §G.B's own
DELTA correction removed one layer out.

## Consequences

**Effective only on complete closure of the seven §J conditions.** Until then this decision changes
nothing operationally, and Stage 1 stays exactly as it is.

Once effective, the `ENDPOINT-0001` Stage-1 authorization mechanism proves its load-bearing identity
against the `XASSET-0037` merged tree, which contains the complete `XASSET-0036`-authorized
executable package. `XASSET-0030` §G.B **steps 9, 10, and 11 remain unperformed and unauthorized**,
and each requires its own separate authority.

**Explicitly unchanged by this filing:** the frozen 680 / 48 universe and its hash
`73c0965e…5224`; every construction identity, ordering, and cardinality; every gate's index,
question, class, controlling authority, and failure disposition; B1, B2, and B3; `XASSET-0030`'s 6/6
gate map and its §E.1 triggers; `XASSET-0024` §K.1; `XASSET-0020` §E.1; `XASSET-0031`'s `G3`;
`level1_stage1_runner.py` and `level1_stage1_result_validator.py`, byte-identical to the accepted
PR #336 package; every `intelligence/` record; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`; `XASSET-0027` §P.1's
reserved, unspent results PR; and every accepted decision's status and text.

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, and unconsumed. No
construction was evaluated, no gate result asserted, and no outcome produced.**

---

## Bounded correction — independent FULL exact-head review `4955010993`

The first candidate (`f7bd5ecff747ade2ffab30574c58da3d683e4d60`) returned **CHANGES REQUIRED**:
0 BLOCKING / 1 MAJOR / 2 MINOR / 0 NOTE. **All three findings were reproduced before any correction.**

The review accepted the core determination in full and raised no objection to the four-way identity
separation, the V7 canonical succession, the 9 → 10 load-bearing extension, historical preservation,
the exact-head lifecycle checks, or the non-activation posture. **None of those changed.**

### MAJOR 1 — the outcome-producing equality boundary omitted the imported derivation surface

`EXECUTABLE_PACKAGE_OUTCOME_PRODUCING_RELPATHS` named only the runner and the result validator, but
both import their disposition, cell-outcome, roll-up, `G2`-reading and vocabulary decisions from
`level1_endpoint_evidence_preregistration_validator.py`. That module was therefore never compared
between the accepted package and this rebinding.

**Reproduced through the real public validator** with isolated truth sources: injecting different
package-head and package-merge bytes for that module, while leaving the successor head, merge, and
load-bearing identity internally consistent, returned `valid=True` with `errors=()`. The identical
mismatch on either declared path was correctly refused. The mechanism did not prove the fact it
relied on.

**Corrected by §D.1's semantic projection**, bound across all five anchors — a new fail-closed
`project_outcome_producing_surface` / `outcome_producing_projection_digest` pair, a
`blob_text_at` truth-source method (a digest cannot answer a *surface* question), and a
`_verify_outcome_producing_projection` gate. The reproduced injection is now refused, and a
non-circular adversarial suite proves drift at either package anchor, at the successor head, in a
transitive dependency, in a renamed seed, in an unparseable anchor, and in an unreadable anchor are
each rejected.

**No Stage-1 outcome semantics were changed.** `level1_stage1_runner.py` and
`level1_stage1_result_validator.py` are byte-identical to the accepted PR #336 package, and the live
projected derivation surface is identical at the package's accepted head, the package's merge, this
head, and the working tree.

### MINOR 1 — the durable register still told a different history

`operations/WORKSTREAMS.yaml` still asserted the **opposite** of the constant's own disclosed
provenance — that the number had been bound only once the draft existed, rather than written first
and verified afterwards — while the constant's comment, §D, the PR body, and two tests already
recorded the truth. The corrective commit had missed the register copy. The defective sentence is
deliberately **not** reproduced here: the regression test below forbids that exact claim on every
durable surface, and a correction record that restated it verbatim would reintroduce the thing the
test exists to keep out.

**Corrected**: the register now states that `337` was **first written before the draft existed**, as
the next sequential number, and **verified against the real draft once it opened**, with the
load-bearing property named as the post-opening verification. A parametrized regression test asserts
across all three durable surfaces that the false claim is absent and the true one present, so it
cannot return.

### MINOR 2 — the rebinding block was not actually closed-schema

`_validate_successor_operational_rebinding` checked required values but never rejected extra keys.
**Reproduced**: `smuggled: value` injected into `successor_operational_rebinding` and independently
into `distinct_identities` each left `validate(...).ok` `True`.

**Corrected**: both mappings now go through the module's own `_keys` mechanism against
`SUCCESSOR_REBINDING_KEYS` and `SUCCESSOR_REBINDING_IDENTITY_KEYS`, so missing keys, extra keys, and
key-order drift are all refused — the same treatment every other closed mapping in that validator
receives. Independent negative tests cover an unknown key in each mapping, every missing key in
both, and key-order drift.

### What this correction did not do

No canonical byte changed, so the **V7 pins are not recomputed** — `PROTOCOL_V1.md`
`367583b6…d8971` and `pre_registration.yaml` `768b013c…4bce1` are re-verified, not rewritten. The
frozen universe is unchanged at **680 / 48 / `73c0965e…5224`**. `LOAD_BEARING_RELPATHS` remains
**10**; nothing was removed and no byte check was weakened. B1, B2, B3, every gate's semantics, every
construction identity, and every disposition are untouched. No accepted decision file was edited. No
§G.B step 9, 10, or 11 was performed, no attestation generated, no lane state created, and nothing of
`ATTEMPT_1` or `XASSET-0027` §P.1 consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires an independent exact-head
**DELTA** review from `f7bd5ecff747ade2ffab30574c58da3d683e4d60`.

## Second bounded correction — independent exact-head DELTA review `4955476669`

The delta review of `eadbb8d4f44f7a2a4147c9e99f6d4ab43cdf154b` returned **CHANGES REQUIRED — 0
BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE**. It recorded MINOR 1 and MINOR 2 above as **RESOLVED**, found
the 18-seed / 26-symbol projection materially improved, and objected to none of the four-way identity
separation, V7 succession, 9 → 10 load-bearing extension, historical preservation, exact-head
lifecycle gates, truthful pull-request provenance, or non-activation posture. **None of those
changed.** One defect remained, and it is a real one.

### MAJOR 1 — ambient bindings can change what a projected AST *means*

`_top_level_symbol_table` recorded functions, classes, and assignments but not `ast.Import` or
`ast.ImportFrom`, and the closure then treated every referenced name absent from that table as "a
builtin or an import" and left it out of scope. That is a syntactic boundary, not a semantic one: a
module-level import can shadow a builtin the closure calls while every projected symbol stays
byte-for-byte identical.

**Reproduced first, in an isolated checkout, against the real public validator — the real lane was
never created, opened, or touched.** Inserting exactly one line, `from builtins import min as any`:

| Step | Result |
|---|---|
| Projected identity, original vs. mutated | **identical** — `9f61ba4b…` both times |
| One categorical `FAIL` (`G10_PAIR_INDEPENDENCE`), accepted implementation | `BLOCKED_CATEGORICALLY` |
| The same input, mutated implementation | `CONSTRUCTIBLE_CANDIDATE_IDENTIFIED` |
| Original at both package anchors, mutated at successor head / merge / working tree | internally consistent |
| `validate_authorization_document` | **`valid=True`, `errors=()`** |

Every projected `any(...)` had silently become `min(...)`, and the rebinding accepted it.

### The correction — the ambient surface joins the identity

The 18-seed → 26-symbol projection is **retained exactly**; whole-file equality was again rejected,
for the same reason as before. What is added is a second, separately derived half of the same
identity: for every name the closure resolves through the **module namespace** rather than its own
top-level symbols, the projection now records **what that name is bound to**.

- **Free names are computed scope-aware.** Parameters, local assignments, comprehension targets,
  `except … as` names, nested definitions, and function-local imports are bound and therefore not
  free. Class-body bindings do not propagate into methods, matching Python's real scoping.
  Decorators, defaults, annotations, and class bases are analysed in the scope where they execute.
- **Each free name is then resolved**, and the resolution — not merely the name — is part of the
  identity: `@ambient::any::builtin`, `@ambient::Mapping::import::from typing import Mapping`.
  Renderings are built from AST fields, so regrouping or reordering the import block changes
  nothing while changing *what a name is bound to* always changes the digest.
- **Nothing is assumed harmless.** A star import, a name the closure resolves that is bound by more
  than one module-level import, `exec` / `eval` / `globals` / `vars` / `setattr` / `delattr`, a
  `global` or `nonlocal` declaration, a module-level augmented assignment or deletion, or a
  referenced name that resolves to nothing nameable, each **fails closed** with a specific error.
- **Precision is preserved deliberately.** An import the closure never references — including a
  shadow of a builtin the closure never calls — does **not** change the identity, so lawful
  authorization-only edits outside the outcome-producing surface remain possible. That is the whole
  reason this is a projection rather than file equality.
- **The docstring exclusion is unchanged and still narrow**, and is still tested in both directions.

The projected identity therefore moved from `9f61ba4b…` to **`6da16369c2fcfd363b00f8319ffe46436a97dbfb3de886756c917eefc4673626`**
— a different value because the surface is genuinely larger, not because any outcome semantics moved.

### Proof, not assertion

Thirty new tests. Nine of them independently detect the fix being reverted — including the reported
reproduction driven through the real public validator at **both** the successor and the package
anchors — verified by re-applying the mutation in an isolated copy. The remainder pin the precision
boundary, every fail-closed edge, and the real anchors. The ambient surface is compared against a
derivation performed **independently of every production constant and helper**, walking the module's
own source, so the production declaration is never its own oracle. The disposition flip itself is
established by executing the mutated module, rather than assumed.

**Requirement: no drift at the real anchors, confirmed rather than presumed.** The corrected
projection — ambient surface included — is identical at the PR #336 accepted head, the PR #336 merge,
this head, and the working tree; and the eight module-level import nodes are AST-identical across all
four, checked separately from the digest. **No Stage-1 outcome semantics changed.**

### What this second correction did not do

No canonical byte changed, so the **V7 pins are again re-verified, not recomputed** —
`PROTOCOL_V1.md` `367583b6…d8971` and `pre_registration.yaml` `768b013c…4bce1` stand. The frozen
universe is unchanged at **680 / 48 / `73c0965e…5224`**. `LOAD_BEARING_RELPATHS` remains **10**;
nothing was removed and no byte check was weakened. `level1_stage1_runner.py` and
`level1_stage1_result_validator.py` remain byte-identical to the accepted PR #336 package, and no
outcome-producing behaviour in either was edited. B1, B2, B3, every gate's semantics, every
construction identity, every disposition, `XASSET-0024` §K.1, and `XASSET-0020` §E.1 are untouched.
No accepted decision file was edited and no protected portfolio path changed. No §G.B step 9, 10, or
11 was performed, no attestation generated, no lane state created, and nothing of `ATTEMPT_1` or
`XASSET-0027` §P.1 consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `eadbb8d4f44f7a2a4147c9e99f6d4ab43cdf154b`.

## Third bounded correction — independent exact-head DELTA review `4957056810`

The delta review of `41afe0992c7043739a5a84f92ea91a342370b863` returned **CHANGES REQUIRED — 0
BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE**. It confirmed the direct-import case from the previous round
genuinely fixed, and objected to none of the 18-seed / 26-symbol projection, scope-aware free-name
analysis, four-way identity separation, V7 succession, 9 → 10 load-bearing extension, historical
preservation, exact-head lifecycle gates, truthful pull-request provenance, closed schemas, or
non-activation posture. **None of those changed.** One defect remained, and it is the general form of
the one just fixed.

### MAJOR 1 — indirect module-scope binders still bypassed the identity

Binding discovery was **direct-node-only**: `_top_level_symbol_table` read simple-`Name` targets from
`tree.body`, and `_module_ambient_bindings` scanned `tree.body` for `Import` / `ImportFrom` nodes.
Python binds module globals through many more forms than those, and every one of them fell through
to the original builtin.

**Both reported spellings reproduced first**, in isolated checkouts against the real public
validator, with the real lane never created, opened, or touched:

| | A — conditional import | B — destructuring assignment |
|---|---|---|
| Inserted | `if True:` / `    from builtins import min as any` | `any, _unused = min, None` |
| Projected identity vs. accepted | **identical** | **identical** |
| One categorical `FAIL` (`G10_PAIR_INDEPENDENCE`) | `BLOCKED_CATEGORICALLY` → **`CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`** | same flip |
| Accepted served at both PR #336 package anchors | yes | yes |
| Mutated + matching load-bearing hashes at successor head / merge / working tree | yes | yes |
| `validate_authorization_document` | **`valid=True`, `errors=()`** | **`valid=True`, `errors=()`** |

### The correction — a complete, target-aware module-scope binder model

The fix addresses the **semantic class**, not the two spellings. `_module_ambient_bindings` is
replaced by `_module_scope_binders`, which is:

- **Recursive** through every compound statement that still executes in module scope — `if`, `try`
  (body, handlers, `else`, `finally`), `for` / `async for`, `while`, `with` / `async with`, `match`
  — while never entering a function, class, lambda, or comprehension body, since those open their
  own scope and only the definition's own name binds at module level.
- **Target-aware**, unpacking `Tuple`, `List`, and `Starred` targets to arbitrary nesting depth.
- **Complete across binder kinds**: imports, ordinary / annotated / augmented assignments, named
  expressions, loop targets, `with … as` targets, `except … as` names, match captures, and
  function / class declarations.
- **Controlling-identity aware.** A nested binding carries a rendering of each enclosing statement's
  *controlling expression* — an `if`'s test, a loop's iterable, a `with`'s items, an `except`'s type,
  a `match`'s subject — so `if True:` and `if False:` are different identities while unrelated edits
  inside the same block are not swept in.
- **Fail-closed where resolution cannot be modelled**: a star import; a closure-resolved name bound
  by more than one binder; a projected symbol conditionally rebound elsewhere in module scope
  (order-dependent — which definition runs cannot be decided statically); module-scope attribute or
  subscript mutation, which can reach an imported module, a builtin, or `globals`; `exec` / `eval` /
  `globals` / `vars` / `setattr` / `delattr`; `global` / `nonlocal`; augmented assignment; deletion.
  The predecessor's blanket refusal of augmented assignment and deletion is kept **exactly as
  strict**, now recursive rather than direct-only.
- **Independently cross-checked.** Every module-global binding CPython's own `symtable` reports must
  be represented by the binder model, or the projection fails closed. That oracle is a different
  mechanism — the compiler front end, not this module's AST walk — so a form the walk forgets is
  caught by something that did not inherit the same blind spot. On the real module the two agree
  exactly: **150 bindings, zero on either side**.

**Precision is preserved**, which is what keeps this a projection rather than whole-file equality: a
binder the closure never resolves — an unused import, an unused conditional import, a shadow of a
builtin the closure never calls, an unrelated destructuring, a loop counter — does **not** change the
identity. The lawful `if __name__ == "__main__":` CLI guard binds nothing and is untouched; the gate
refuses *mutation*, never ordinary control flow. The 18-seed → 26-symbol projection, scope-aware
free-name analysis, direct-import binding, and narrow docstring exclusion are all unchanged.

The projected identity moved to
**`574b9194b61cbc1fe9dca0f1536b91bd6b1c716d5d197df7529e27c9e0039af5`** because ambient records now
name their binder kind and controlling identity — the surface is richer, not a different subject.

### Proof, not assertion

**Seventy new tests**, including a parameterized binder matrix of sixteen forms plus a `match`
statement, ten namespace-mutation refusals, six precision cases, and direct target-unpacking cases.
The two reported reproductions are driven through the **real public validator** at both the successor
and the package anchors, and the disposition flip is established by **executing** the mutated module.
The completeness oracle is called directly from the test rather than through production code, and a
dedicated test blinds the production model to prove the oracle is **enforced**, not merely available.

**Mutation proof: reverting only the binder correction — restoring direct-node-only discovery —
fails 28 of the 70**, verified by re-applying the mutation in an isolated copy and re-running, then
restoring the fix to separate genuine detection from environment noise.

**No drift at the real anchors, confirmed rather than presumed.** The corrected projection is
identical at the PR #336 accepted head, the PR #336 merge, this head, and the working tree.

### What this third correction did not do

No canonical byte changed, so the **V7 pins are again re-verified, not recomputed** —
`PROTOCOL_V1.md` `367583b6…d8971` and `pre_registration.yaml` `768b013c…4bce1` stand. The frozen
universe is unchanged at **680 / 48 / `73c0965e…5224`**. `LOAD_BEARING_RELPATHS` remains **10**.
**No outcome-producing module was edited** — `level1_stage1_runner.py`,
`level1_stage1_result_validator.py`, and `level1_endpoint_evidence_preregistration_validator.py` are
all absent from the diff. B1, B2, B3, every gate's semantics, every construction identity, every
disposition, `XASSET-0024` §K.1, and `XASSET-0020` §E.1 are untouched. No accepted decision file was
edited and no protected portfolio path changed. No §G.B step 9, 10, or 11 was performed, no
attestation generated, no lane state created, and nothing of `ATTEMPT_1` or `XASSET-0027` §P.1
consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `41afe0992c7043739a5a84f92ea91a342370b863`.

## Fourth bounded correction — independent exact-head DELTA review `4958940810`

The delta review of `bc38501688679d3255da4703169a5c8d020441c6` returned **CHANGES REQUIRED — 0
BLOCKING / 1 MAJOR / 0 MINOR / 0 NOTE**. It confirmed the conditional-import and
destructuring-assignment bypasses genuinely fixed, that no outcome-producing module was in the
delta, and that no review-time repository, lane, or activation mutation occurred. One defect
remained — the same security property, reached through a different mechanism.

### MAJOR 1 — call-mediated namespace mutation bypassed the identity

`_reject_dynamic_namespace_mutation` recognised a dangerous call only when `call.func` was an
`ast.Name`. A **method** call — callee an `ast.Attribute`, containing no `Store` node anywhere — was
therefore neither refused nor represented. Two lines were enough:

```python
import builtins as _review_builtins
_review_builtins.__dict__.update(any=min)
```

**Reproduced first**, in an isolated checkout with disposable subprocess execution, against the real
public validator, with the real lane never created, opened, or touched. All five material proofs
held:

| # | Proof | Result |
|---|---|---|
| 1 | Accepted and mutated sources share the projection digest | **identical** — `574b9194…9af5` both |
| 2 | Executing the mutation flips the categorical-failure case | `BLOCKED_CATEGORICALLY` → **`CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`** |
| 3 | Accepted at both package anchors + mutated at successor head / merge / working tree | **`valid=True`, `errors=()`** |
| 4 | Mutated at **both package anchors** instead | **`valid=True`, `errors=()`** |
| 5 | Real authorization lane | **absent and untouched** |

The CPython `symtable` oracle cannot see this class at all, and a dedicated test now records why:
the mutation binds **no new module global** — its only new binding is the import alias itself. It
changes an *existing* namespace through a call.

*Disclosed:* the review reported digest `1cdfbbd2…c15e` where this environment computes
`574b9194…9af5`. That is the `ast.dump` cross-interpreter boundary the projection's own docstring
already states, not a disagreement — the **property** the proof turns on, accepted digest ==
mutated digest, is identical in both environments.

### The correction — a fail-closed rule over the semantic class

Every module-scope call is now routed through `_reject_call_mediated_namespace_mutation`. The rule
is structural and refuses on any of:

- **an unnameable callee** — `registry["f"]()`, `(a or b)()` — because what will run cannot be named,
  let alone proven harmless;
- **a namespace-exposing attribute anywhere in the callee's receiver chain** — `__dict__`,
  `__globals__`, `__builtins__`, `__class__`, `__bases__`, `__mro__`, `__subclasses__`,
  `__setattr__`, `__delattr__`, `__getattribute__`, `__setitem__`, `__delitem__`, `modules`;
- **an in-place mutator method** — `update`, `setdefault`, `pop`, `popitem`, `clear`, `append`,
  `extend`, `insert`, `__setitem__`, `__delitem__` — on **any** receiver, since a static projection
  cannot prove `_ns.update(any=min)` is a scratch dict rather than `builtins.__dict__`;
- **a root at a namespace-bearing module** — `builtins`, `importlib`, `gc`, `ctypes` — resolved
  **through the module-scope import binders**, so an alias is caught as readily as the bare name;
- **a namespace handed to an unknown callee as an argument**;
- the pre-existing by-name set (`exec`, `eval`, `globals`, `vars`, `setattr`, `delattr`).

**Nothing is modelled into the identity here.** A call's effect genuinely cannot be resolved
statically, so this class fails closed rather than being represented — and the projected identity is
therefore **unchanged** at `574b9194…9af5`, with the 18-seed → 26-symbol projection, scope-aware
free-name analysis, direct-import binding, recursive target-aware binder discovery,
controlling-expression identity, the `symtable` oracle, and the narrow docstring exclusion all
untouched.

**Precision is preserved deliberately, and cost real design work.** Two first-draft clauses were
found over-broad against the real module and narrowed before anything was committed: `sys` was
removed from the namespace-bearing module set, because `sys.exit(main())` is the lawful CLI guard
and mutates nothing — the genuinely dangerous `sys` avenue, `sys.modules`, is caught by the precise
attribute clause instead; and the callee decomposition now walks **through** an intermediate call, so
`Path(__file__).resolve()` keeps a nameable root. The real module's own module-scope calls —
`Path(__file__).resolve()`, `tuple(genexp)`, five `re.compile(...)` calls, and `sys.exit(main())` —
all still project without refusal. A call is never rejected merely for being a call.

### Proof, not assertion

**Thirty-three new tests.** The reported spelling is executed in a **disposable subprocess** to prove
the disposition flip — never assumed, and never run in-process, since mutating `builtins` would
corrupt the whole session. It is driven through the **real public validator** at the successor
anchors, at both package anchors, and at every anchor simultaneously. A sixteen-entry matrix covers
materially distinct routes: aliased namespace, `from`-import of the namespace itself, `vars()`
receiver, `setattr`, `getattr` chain, `sys.modules`, class-`__mro__` walk, unbound-method form,
mapping mutator on an arbitrary receiver, namespace-as-argument, `importlib.reload`, subscript
callee, conditional callee, and nesting inside `if` and `try`. A seven-entry matrix pins that
harmless calls and the lawful CLI guard are **not** rejected. Every matrix entry is written from
Python's own semantics rather than from any production constant, tuple, or allowlist, so production
and tests cannot drift together unnoticed.

**Mutation proof: disabling only the new call-mediated protection — restoring `ast.Name`-callee
recognition — fails 18 of the 33**, verified by applying the mutation in an isolated copy and then
restoring the fix to separate genuine detection from environment noise.

**No drift at the real anchors:** the projection is identical at the PR #336 accepted head, the
PR #336 merge, this head, and the working tree.

### What this fourth correction did not do

No canonical byte changed, so the **V7 pins are again re-verified, not recomputed**. The frozen
universe is unchanged at **680 / 48 / `73c0965e…5224`**; `LOAD_BEARING_RELPATHS` remains **10**.
**No outcome-producing module was edited.** All 364 pre-existing tests in the suite, including the
70 from the binder correction, still pass strictly — none weakened, skipped, deleted, xfailed, or
loosened. B1, B2, B3, gate semantics, construction identities, dispositions, `XASSET-0024` §K.1, and
`XASSET-0020` §E.1 are untouched; no accepted decision file was edited and no protected portfolio
path changed. No §G.B step 9, 10, or 11 was performed, no attestation generated, no lane state
created, and nothing of `ATTEMPT_1` or `XASSET-0027` §P.1 consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `bc38501688679d3255da4703169a5c8d020441c6`.

## Fifth bounded correction — independent exact-head DELTA review `4960897843`

The delta review of `4781ffbc06036d88884368c8dc4a7f1024fdc810` returned **CHANGES REQUIRED — 0
BLOCKING / 2 MAJOR / 0 MINOR / 0 NOTE**. It confirmed the previously reported attribute-method
spelling corrected, the delta confined to four files, the runner / result validator / derivation
module untouched, and no canonical byte, universe identity, load-bearing count, activation posture,
attempt state, or protected path changed. Two independent gaps remained in the claimed
semantic-class closure.

### MAJOR 1 — eager definition-time and class-body code was skipped wholesale

`_reject_dynamic_namespace_mutation.scan` did `continue` on every top-level `FunctionDef`,
`AsyncFunctionDef`, and `ClassDef`. That skipped code Python executes **during module
initialization** — decorators, defaults, annotations, class bases and keywords, and the class body
itself. None of those is a deferred function body.

### MAJOR 2 — imported and call-returned dangerous callables were treated as harmless

Two mechanics combined. A bare call was checked against the dangerous set **by its written root
name only**, with the import binders consulted solely when the callee carried attributes and solely
to recognise a projection-bearing *module* — so a dangerous builtin imported under an alias walked
straight through. Separately, `_callee_chain` walked through **any** intermediate `ast.Call`, so
`getattr(m, "x")()` was reported as rooted at `getattr` rather than unnameable — contradicting that
function's own documented contract.

### Reproduced first — all four forms, before any code changed

Isolated checkout, disposable subprocess execution, real public validator, **real lane never
created, opened, or touched**:

| Form | Same digest | Executed disposition | Validator, accepted@package + mutated@successor | Validator, mutated at all four anchors |
|---|---|---|---|---|
| `def _p(_x=_rb.__dict__.update(any=min))` | **yes** | `BLOCKED_CATEGORICALLY` → **`CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`** | **`valid=True, errors=()`** | **`valid=True, errors=()`** |
| `class _P: _rb.__dict__.update(any=min)` | **yes** | same flip | **`valid=True, errors=()`** | **`valid=True, errors=()`** |
| `from builtins import exec as _rexec` | **yes** | same flip | **`valid=True, errors=()`** | **`valid=True, errors=()`** |
| `getattr(_rb, "exec")("any=min")` | **yes** | same flip | **`valid=True, errors=()`** | **`valid=True, errors=()`** |

### The correction

**MAJOR 1 — an execution-aware pruning traversal.** `_iter_eager_module_scope_nodes` replaces
`ast.walk` plus the blanket skip, and is more accurate in *both* directions — the predecessor
enumerated deferred bodies it should not have scanned while skipping eager code it should have. A
function or lambda contributes its decorators, defaults, keyword defaults, argument annotations, and
return annotation, and its **body is pruned**; a class contributes its decorators, bases, keywords,
**and its entire body**, recursively; a list/set/dict comprehension is scanned in full because it
runs immediately, while a generator expression contributes only its outermost iterable — the one
part evaluated eagerly.

**MAJOR 2 — resolve the alias, and distinguish a named method from a returned callable.**
`_imported_origin` and `_resolved_import_origins` decompose each module-scope import binding into
`(module, symbol)`. A `from module import symbol` binding is judged **by its symbol** — refused when
that symbol reads or writes a namespace (`exec`, `eval`, `globals`, `vars`, `setattr`, `delattr`) or
replaces or reloads one (`reload`, `import_module`, `__import__`, `invalidate_caches`,
`get_objects`, `get_referrers`) — while an `import module` binding binds the **namespace object
itself**, so any call reached through it stays refused. `_callee_chain` now walks through an
intermediate call **only beneath an attribute**: `Path(__file__).resolve()` invokes a *named method*
on a constructed receiver and remains nameable, whereas `getattr(m, "x")()` invokes whatever the
inner call returned — nothing names it — and is refused.

**Precision was verified, not assumed, and one first-draft clause was narrowed before committing.**
Refusing every call rooted at an import *of* a projection-bearing module also rejected
`from builtins import sorted as _rsorted`, which mutates nothing; the symbol-level rule above
replaced it. All ten lawful forms — the CLI guard, `sorted(...)`, `Path(...).resolve()`,
`re.compile(...)`, `tuple(genexp)`, a `def` with safe defaults, a plain class, a decorated function,
a **deferred body that is pruned rather than scanned**, and a safe import alias — leave the identity
unchanged.

**The projected identity is unchanged at `574b9194…9af5`.** Both classes fail closed; nothing is
restated into the surface. The 18-seed → 26-symbol projection, scope-aware free-name analysis,
direct-import binding, recursive target-aware binder discovery, controlling-expression identity, the
`symtable` oracle, and the narrow docstring exclusion are all untouched.

### Proof, not assertion

**Fifty-two new tests.** Each of the four reported forms is **executed in a disposable subprocess**
to prove the flip and driven through the **real public validator** at the successor anchors and at
all four anchors. A thirteen-entry eager-execution matrix covers every module-initialization
boundary; a nine-entry matrix covers aliased and call-returned callables; a ten-entry precision
matrix pins that harmless eager code is not refused; dedicated tests prove deferred bodies are
pruned, that the traversal reaches an eager default while *not* reaching a deferred body, that a
call-returned callable is unnameable while a named method is not, and that the rendering grammar
resolves an alias to its imported symbol. Every entry is written from **Python's own execution
semantics**, not from any production constant, tuple, or allowlist.

**Mutation proof, per correction:** disabling **only** the MAJOR-1 traversal fails **16 of 52**;
disabling **only** the MAJOR-2 alias and call-chain corrections fails **14 of 52**; with both
restored all 52 pass.

### What this fifth correction did not do

No canonical byte changed, so the **V7 pins are again re-verified, not recomputed**. The frozen
universe is unchanged at **680 / 48 / `73c0965e…5224`**; `LOAD_BEARING_RELPATHS` remains **10**.
**No outcome-producing module was edited.** All 397 pre-existing tests in the suite still pass
strictly — none weakened, skipped, deleted, xfailed, or loosened. B1, B2, B3, gate semantics,
construction identities, dispositions, `XASSET-0024` §K.1, and `XASSET-0020` §E.1 are untouched; no
accepted decision file was edited and no protected portfolio path changed. No §G.B step 9, 10, or 11
was performed, no attestation generated, no lane state created, and nothing of `ATTEMPT_1` or
`XASSET-0027` §P.1 consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `4781ffbc06036d88884368c8dc4a7f1024fdc810`.

## Sixth bounded correction — independent exact-head DELTA review `4961431702`

The delta review of `d9c55d48da3abdec09c1a56d27a2f9fade3d486f` returned **CHANGES REQUIRED — 0
BLOCKING / 2 MAJOR / 1 MINOR / 0 NOTE**. It confirmed all four exact forms from review `4960897843`
now rejected, the delta confined to four files, no runner / result-validator / derivation / canonical
/ universe / protected portfolio file changed, exact-head CI green, and Stage 1 UNARMED. Two
independent gaps and one precision defect remained.

### MAJOR 1 — deferral was decided from AST node type, not from what import actually executes

`_iter_eager_module_scope_nodes` pruned every function, lambda, and generator body on node type
alone. That is unsound the moment surrounding module-initialization code *invokes or consumes* the
deferred body: a top-level helper called at module scope, a named local decorator applied implicitly
during function creation (no `ast.Call` at the decorator site), and a generator expression consumed
eagerly by its enclosing call all execute during import.

### MAJOR 2 — origins did not propagate through ordinary assignments or namespace-valued arguments

`_resolved_import_origins` resolved only a callee name bound *directly* by an import. It did not
propagate through module-scope assignments, so one ordinary binding laundered a dangerous callable.
Separately, argument inspection recognised a literal namespace-exposing `Attribute` but not a `Name`
already bound to that namespace — precisely review `4960897843`'s required "namespace aliases handed
to mutators" class, which the prior nine-case matrix did not exercise.

### MINOR 1 — postponed annotations classified as eager

The derivation source begins with `from __future__ import annotations`, under which annotation
expressions are **not** evaluated at module creation. The traversal scanned every argument and
return annotation as eager — fail-closed, but a violation of the stated execution-accurate precision
boundary, and capable of rejecting lawful authorization-only annotation edits.

### Reproduced first — all five forms, before any code changed

Reviewed-head source (`d9c55d4…`, blob `6643fa14…f585b`) loaded in isolation, real projection,
disposable subprocess execution, real public validator, **real lane never created, opened, or
touched**. Two spellings named in the review were already refused by the prior head for incidental
reasons (`_rb.__dict__.update(...)` inside a genexp hit the `__dict__`-as-argument clause; a
`_d.update(_ns, ...)` form hit the mutator-name clause); rather than report a closed class on those,
genuinely bypassing spellings were constructed for the same two mechanisms and are the ones recorded
here.

| Form | Mechanism | Reviewed head | Corrected head |
|---|---|---|---|
| `def _h(): _rb.__dict__.update(any=min)` then `_h()` | eager call into pruned body | **accepted, identical projection** | **`ProjectionError`** |
| `@_d` where `_d` mutates | implicit decorator application | **accepted, identical projection** | **`ProjectionError`** |
| `tuple(_ns.update(any=min) for _i in range(1))` | consumed generator | **accepted, identical projection** | **`ProjectionError`** |
| `_alias = _rb.__dict__.update` then `_alias(any=min)` | assignment alias | **accepted, identical projection** | **`ProjectionError`** |
| `_op(_ns, 'any', min)` with `from builtins import __dict__ as _ns` | namespace `Name` argument | **accepted, identical projection** | **`ProjectionError`** |

### The correction

**MAJOR 1 — model transitive execution reachable during module initialization.** A module-scope call
whose callee resolves to a local definition now has that definition analysed (`analyse_definition`,
cycle-guarded); a bare-`Name` decorator on an eagerly-reachable definition is treated as the
**implicit call it is**; a generator expression consumed by an enclosing eager operation is analysed
in full rather than reduced to its outermost iterable. `if __name__ == "__main__":` is recognised
(`_is_main_guard`) and still scanned for *direct* mutation, but does not make called bodies eagerly
reachable — that block provably does not execute on import, which is the only path by which the
derivation module participates in outcome production, and it is what preserves the lawful CLI
posture.

**Positive safe-call boundary, per the review's explicit direction.** Where bounded analysis cannot
prove an arbitrary call harmless, the gate no longer consults another list of dangerous spellings: a
module-scope call is **refused unless provably safe**. `_SAFE_BUILTIN_CALLABLES` is a narrow closed
set of pure builtins; `_origin_is_safe_callee` judges each resolved origin against it.

**MAJOR 2 — a fail-closed transitive origin/alias closure.** `_name_origins` and `_value_origins`
propagate origins through ordinary module-scope assignments, including destructuring, conditional,
and multi-hop bindings, with a binding cycle resolving to `("unresolvable",)` rather than looping. A
symbol import of a namespace-exposing attribute (`from builtins import __dict__ as _ns`) and a whole
-module import of a projection-bearing module both yield a `("namespace", …)` origin, so a `Name`
carrying a live namespace is refused as a call argument exactly as a literal `Attribute` already was.

**MINOR 1 — annotation traversal is now conditional on the module's real future-annotations posture.**
`_ModuleScopeContext.future_annotations` records it; argument and return annotations are scanned only
when Python will actually evaluate them. The two former must-fail annotation cases moved to the
precision matrix as `postponed-argument-annotation` / `postponed-return-annotation`, which now assert
that postponed annotations are **not** treated as executed.

### Verification

Twenty must-fail forms and fifteen must-pass forms both close completely. The live projection digest
is **unchanged at `574b9194b61cbc1fe9dca0f1536b91bd6b1c716d5d197df7529e27c9e0039af5`** — every
lawful construct in the real module, including `Path(__file__).resolve()`, `tuple(genexp)`, five
`re.compile(...)`, and `sys.exit(main())`, still projects identically. Per-mechanism mutation proof:
disabling **only** the transitive-execution analysis fails 4 targeted tests; disabling **only** the
origin closure fails 11; restoring reproduces the implementation byte-identically
(`124daadd7b6dd617f7185b9a1868c1e830a2426146e60275242730e40e35c833`) and all 57 new tests pass.

Two of the three pre-existing tests that changed were the MINOR 1 defect itself; the third
(`test_an_unresolvable_referenced_name_fails_closed`) still fails closed but reaches the refusal
earlier under a different message, so its regex was broadened **without** relaxing its
`ProjectionError` requirement. `test_an_import_alias_resolves_to_the_imported_symbol` was rewritten
against `_build_module_scope_context` on real source — strictly stronger than the removed rendering
helper it previously asserted on.

### Preserved

The four-way identity separation, `LOAD_BEARING_RELPATHS = 10`, both V7 canonical pins, the
680/48 universe and `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224`, every
protected portfolio path, and the whole non-activation posture. No gate semantics, construction
identity, or disposition was reopened. No §G.B step 9-11 work was performed, no attestation
generated, no lane state created, and nothing of `ATTEMPT_1` or `XASSET-0027` §P.1 consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `d9c55d48da3abdec09c1a56d27a2f9fade3d486f`.

## Seventh bounded correction — independent exact-head DELTA review `4962377217`

The delta review of `696795742f228a1f0ec566bacc9b34e0c02a5a30` returned **CHANGES REQUIRED — 0
BLOCKING / 2 MAJOR / 0 MINOR / 0 NOTE**. It independently confirmed the five forms from review
`4961431702` now refused, the postponed-annotation precision boundary behaving as requested, the
delta confined to four files, no runner / result-validator / derivation / canonical / universe /
protected portfolio file changed in that delta, and exact-head CI green at 9,139 passed. Two
semantic gaps remained.

### The two invariants this correction establishes

Both findings are symptoms of the same thing: the analysis decided questions *syntactically* that
Python answers *by value*. The correction is therefore stated as two conservative invariants, and
every mechanism below is an instance of one of them.

1. **Import-time execution reachability.** A construct is analysed unless it is *proven* not to run
   during module initialization. Deferral must be established by value flow and call semantics, not
   by immediate AST parentage. Ambiguous or control-dependent reachability is resolved by analysing.
2. **Callable and namespace origin proof.** A callee or argument is permitted only when *every*
   origin it can resolve to is positively proven safe. Unresolved, container-mediated, or merely
   unlisted origins are refused.

### MAJOR 1 — reachability was syntax-local, not transitively closed

Four independent mechanisms, each losing reachability at a different point: a generator assigned to
a name and consumed by a *later* call (the consumer saw only a `Name`); a `lambda` used *directly*
as a decorator (only a bare `ast.Name` decorator was treated as an implicit call, while the lambda
body was pruned); a local class whose `__init__` mutates, *instantiated* at module scope (only the
class-creation body was scanned, never construction); and two conditional definitions of one name,
where `definitions[name]` kept whichever node was written last and silently discarded the other.

### MAJOR 2 — namespace origin died in containers, and the boundary was still a denylist

`_value_origins` labelled every tuple/list/set/dict `("literal",)` regardless of contents, so a live
namespace placed in a container and selected back out by subscript was invisible. Compounding it,
`_origin_is_safe_callee` returned *safe* for any symbol or attribute rooted in a module outside
`_PROJECTION_BEARING_MODULES` unless its spelling appeared in a dangerous-name set — a denylist
wearing a positive boundary's name, which an ordinary standard-library mutator walked straight
through.

### Reproduced first — all five forms, before any code changed

Reviewed-head blobs (`level1_stage1_execution_authorization.py` `124daadd…35c833`, derivation
`2b8ead2b…b3d356`) loaded in isolation; execution only ever in **disposable child interpreters**;
the real lane never created, opened, inspected, or touched.

| Form | Mechanism | Projection at reviewed head | Executed disposition | This head |
|---|---|---|---|---|
| `_g = (…); list(_g)` | consumption through an alias | **accepted, identical** | `BLOCKED_CATEGORICALLY` → **`CONSTRUCTIBLE_CANDIDATE_IDENTIFIED`** | **`ProjectionError`** |
| `@(lambda _f: …)` | implicit decorator invocation | **accepted, identical** | same flip | **`ProjectionError`** |
| `class _C: __init__` then `_C()` | constructor execution | **accepted, identical** | same flip | **`ProjectionError`** |
| two conditional `def _p` then `_p()` | control-dependent origin | **accepted, identical** | same flip | **`ProjectionError`** |
| `_b = (ns,)` then `setitem(_b[0], …)` | container/subscript taint | **accepted, identical** | same flip | **`ProjectionError`** |

### The correction

**Invariant 1.** `_deferred_values_for_name` follows a name through any number of ordinary aliasing
assignments to the deferred values it can hold, and `analyse_consumed` analyses those bodies at
every eagerly consuming position — call arguments and `for`-loop iterables — bounded against
self-referential aliases. `analyse_decorator` replaces the bare-`Name` special case and handles each
decorator shape by **what Python does with it**: a `lambda` is invoked, so its body is analysed; a
decorator *factory* returns a callable nothing names, so it is refused; an attributed or named
decorator is judged exactly as a callee. `analyse_definition` analyses **every** definition bound to
a name, and, when one is a class that is called, the bodies of every function in its class body —
deliberately a superset of `__init__`/`__new__`/`__post_init__`, because a metaclass `__call__`,
`__init_subclass__`, or `__set_name__` can also run while the instance is produced.

**Invariant 2.** `_value_origins` propagates origins through container construction, subscript
selection, starred unpacking, conditional expressions, and boolean operators, so taint survives any
number of hops; a selection whose base cannot be proven free of namespace origins is refused rather
than assumed harmless. `_SAFE_IMPORTED_CALLABLES` and `_SAFE_CONSTRUCTED_METHODS` make the boundary
genuinely positive: `re.compile`, `pathlib.Path` plus `.resolve()`, `dataclasses.dataclass`/`field`,
and `sys.exit` are *listed* as proven; every other imported callable, attributed module call, and
multi-step module chain fails closed **because it is unlisted**, not because it was enumerated as
dangerous.

### Verification

**Twenty-eight** must-fail forms — spanning alias hops, `for`-loop consumption, decorator factories,
constructor aliases, both branch orders of a conditional definition, `try`/`except` duplicates,
nested containers, conditional expressions, and unlisted standard-library callables — all refused.
**Sixteen** must-pass forms — including every construct the real module actually performs and the
postponed-annotation boundary from review `4961431702` — all project **byte-identically**. The live
projected identity is **unchanged at
`574b9194b61cbc1fe9dca0f1536b91bd6b1c716d5d197df7529e27c9e0039af5`**.

**Mutation proof, one component at a time**: disabling only alias consumption fails 8; only the
general decorator handling, 4; only constructor modelling, 7; only multi-definition preservation, 4;
only container taint, 2; only the positive import boundary, 3. Restoring reproduces the
implementation byte-identically (`9ea848b0…59cebd3`) and all 70 new tests pass.

**Two pre-existing precision entries were corrected, and the change makes the suite stricter.** Both
asserted that `@functools.lru_cache(maxsize=1)` must not be refused. That single form is exactly
what this review required be refused, on two independent grounds — the callable a factory returns is
named by nothing, and `functools` is not positively listed. Each entry now exercises a decorator
that *is* proven (`@dataclass`, mirroring the real module's own use), and the factory form is pinned
on the must-fail side. `functools` is not imported by the derivation module at all, so no lawful
identity is affected. One test of mine also conflated two protection mechanisms — the binder model
closes an ambient rebinding by **moving** the identity, not by raising — and now asserts each by the
mechanism that actually implements it.

### Preserved

The four-way identity separation, `LOAD_BEARING_RELPATHS = 10`, both V7 canonical pins, the 680/48
universe and `73c0965e…5224`, every protected portfolio path, the outcome-producing derivation
module, runner, and result validator, and the whole non-activation posture. No gate semantics,
construction identity, or disposition was reopened. No §G.B step 9-11 work was performed, no
attestation generated, no lane state created, and nothing of `ATTEMPT_1` or `XASSET-0027` §P.1
consumed.

**Stage 1 remains UNARMED and NOT EXECUTABLE.** The corrected head requires a further independent
exact-head **DELTA** review from `696795742f228a1f0ec566bacc9b34e0c02a5a30`.
