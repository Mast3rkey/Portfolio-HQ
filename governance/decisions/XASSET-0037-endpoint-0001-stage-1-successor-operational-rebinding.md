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
   package's merge, the successor's reviewed head, the successor's merge, **and** the working tree.

Point 6 is §G.B's own invariant, mechanised: *no outcome-producing executable code may be created,
changed, or left outside the bound execution identity after the final rebinding and before
`ATTEMPT_1`.* A silent runner edit smuggled into the rebinding that binds it **fails closed**.
Neither outcome-producing module is modified by this unit; both are byte-identical to the accepted
PR #336 package.

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
