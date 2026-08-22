---
decision_id: XASSET-0049
date: 2026-08-22
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_step8_equivalent_successor_rebinding.py
---

## Context

### Live preflight

Independently re-derived this session from live git and live GitHub before any file was edited.
Nothing below is inherited from a prior session's summary or from the task that commissioned this
unit; every value was reproduced locally against real objects.

| Fact | Verified value |
|---|---|
| GitHub `main`, `origin/main`, this branch's base and `HEAD` | `f052efad38e3d57e3e5615799ac3bcbebe83ff5f` — **equal**, not merely descended |
| That commit's identity | PR #348's merge, parents `bb95ed26964b1bc7a2e230c76060fec82752efa1` then `42e3a8aec1b36c4e5f22e4cdf4210a61ed781156`, re-derived via `git log --pretty='%H %P'` |
| Merge-tree drift on PR #348 | **zero** — merge tree `514d34c7ba7df5daa9b38b0ae820dba832401429` is byte-identical to the accepted head's own tree |
| PR #348 | merged, closed, `merged_by` `Mast3rkey`, 3 commits, 14 files |
| PR #348 independent FULL review | [`4998661361`](https://github.com/Mast3rkey/Portfolio-HQ/pull/348#pullrequestreview-4998661361) at `1c103a49…` — 1 MAJOR, 2 MINOR |
| PR #348 clean exact-head DELTA review | [`4999458224`](https://github.com/Mast3rkey/Portfolio-HQ/pull/348#pullrequestreview-4999458224) at the accepted head — **0 / 0 / 0 / 0** |
| PR #348 principal exact-head acceptance | [`5380255052`](https://github.com/Mast3rkey/Portfolio-HQ/pull/348#issuecomment-5380255052) |
| PR #348 post-merge verification | [`5380287468`](https://github.com/Mast3rkey/Portfolio-HQ/pull/348#issuecomment-5380287468) |
| PR #348 merge-commit CI | run `32571799154` / job `97028166971` — run `head_sha` equals the exact merge SHA — `completed` / **`success`**, **10,813 passed** |
| PR #348 final post-CI lifecycle closure | [`5380368431`](https://github.com/Mast3rkey/Portfolio-HQ/pull/348#issuecomment-5380368431) |
| Open pull requests | **0** |
| Working tree · worktrees | clean · sole worktree, no competing mutation lane |
| `XASSET-0049` identifier | unused — 0 hits in `governance/decisions.yaml`, no decision file; the sole repository occurrence is one mutation-pin *docstring* in `XASSET-0048`'s artifact, which names it only to refuse pre-authorizing it |
| Decision catalog | **150** entries before this filing |
| `AUTHORIZING_DECISION` · `AUTHORIZING_PULL_REQUEST` · `REVIEWED_BASE_SHA` | `XASSET-0047` · `347` · `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` |
| `LOAD_BEARING_RELPATHS` | exactly **16** |
| `level1_stage1_execution_authorization.py` blob at base | `b23d762ff1f9f4c87fb1475741d61e1b49d47625` |
| Canonical pins | `PROTOCOL_V1.md` `1ad1d060…5d0c84` · `pre_registration.yaml` `898c329d…12d82f` — both match the live files |
| Frozen universe | **680** constructions · **48** cells · `73c0965e…5224` — match |
| `new_execution_is_authorized()` | `(False, …)` — "no attestation present" |
| `AUTHORIZATION_ROOT` | **absent** — lane `ABSENT` |
| `ATTEMPT_1` (`ENDPOINT-0001::STAGE_1::ATTEMPT_1`) | intact, unclaimed, unconsumed |
| `stage1_results.yaml` | **none exists anywhere** |

No `risk_lane_boundary` protected `RISK` result path was read, listed, opened, or referenced.

### What this unit is

`XASSET-0048` is effective: all seven of its `§J` conditions closed, the seventh strictly after the
merge-commit CI job completed. What it granted is **exactly one** future, separate, bounded pull
request to perform the `XASSET-0030` `§G.B` **step-8-equivalent** successor
operational-authorization / load-bearing rebinding. **This unit is that one.**

`XASSET-0048` `§A` is explicit that merging it "performs no rebinding and arms nothing," and its own
closure comment says the same. The rebinding was therefore authorized but unperformed as of this
filing's preflight. This decision performs it, in the same pull request that files it, exactly as
`§F.10` requires.

**Performing the rebinding is not arming.** Stage 1 remains **UNARMED** and **NOT EXECUTABLE**, the
lane remains **ABSENT**, and `ATTEMPT_1` remains intact, unclaimed, and unconsumed.

## Decision

### A. Determination — `STEP_8_EQUIVALENT_REBINDING_PERFORMED`

The effective structural authorization source is rebound to **this** decision, **this** pull
request, and **this** unit's own verified base, and the trust boundary is extended additively from
sixteen paths to eighteen. Every value that moves is recorded in `§C` as an **exact closed
transition**, both ends bound, the old end preserved rather than overwritten.

**Step 8 is not re-consumed.** `XASSET-0030` `§G.B` step 8 authorized **one** rebinding against the
executable package's exact merged bytes and **`XASSET-0037` performed it**; `XASSET-0043` `§C` and
`XASSET-0044` `§C` both record that budget as spent, and `XASSET-0048` `§B.1` restates it. The
authority for this unit is `XASSET-0048` `§E` — the step-8 ***equivalent*** named by `XASSET-0041`
`§I` link 2: a lifecycle of the same kind and rigour, separately authorized, and never a second draw
on step 8's own spent budget.

### B. The base — equality, derived from the completed lifecycle and proved from the object store

`XASSET-0048` `§F.2` makes **equality** operative and states descent to be *necessary history and
explicitly insufficient authority*. It also refuses to name its own merge as a literal SHA, because
it had not merged when it was written. This unit therefore **derived** that identity rather than
accepting it, and proved it:

```
required   the normal-merge commit closing XASSET-0048's own §J lifecycle
first parent   bb95ed26964b1bc7a2e230c76060fec82752efa1   (XASSET-0048's own verified main)
second parent  42e3a8aec1b36c4e5f22e4cdf4210a61ed781156   (its independently reviewed,
                                                           principal-accepted head)
merge tree     514d34c7ba7df5daa9b38b0ae820dba832401429   byte-identical to that head's own tree
merge-commit CI  run 32571799154 — head_sha equals the merge SHA — completed / success
final closure    issuecomment-5380368431, recorded after CI completion
=> the merge is f052efad38e3d57e3e5615799ac3bcbebe83ff5f

this unit's base   f052efad38e3d57e3e5615799ac3bcbebe83ff5f
EQUAL              yes — not "descends from"
```

`main` has **not** advanced past that merge: GitHub `main`, `origin/main`, this branch's base and its
`HEAD` are all the same commit, so `§F.2`'s drift-stop was checked and did not fire. **No
intervening byte is absorbed by descent**, because there is no intervening commit to absorb.

**The rule is made operative in code, not left in prose.** `_verify_step8_equivalent_base_equality`
is a pure function over three parameters that decides the whole proposition — well-formedness,
equality, and retained ancestry — and it is driven in the artifact against known-good and known-bad
values including a **real synthetic later descendant**, which it refuses *even when ancestry is
granted unconditionally*. The superseded descent-only formulation is retained beside it and shown
**accepting what the corrected rule refuses**.

### C. Exact closed transitions — `XASSET-0048` `§F.3`

Every value this rebinding moves, both ends bound, old value preserved:

| Value | Old | New |
|---|---|---|
| `AUTHORIZING_DECISION` | `XASSET-0047` | **`XASSET-0049`** |
| `AUTHORIZING_PULL_REQUEST` | `347` | **this unit's GitHub-issued number** (`§D`) |
| `REVIEWED_BASE_SHA` | `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` | **`f052efad38e3d57e3e5615799ac3bcbebe83ff5f`** |
| `LOAD_BEARING_RELPATHS` | **16** | **18** — additive only (`§E`) |
| reviewed-base equality target | `RECOVERY_AUTHORIZING_MERGE_SHA` (`XASSET-0046`) | `STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA` (`XASSET-0048`) |
| inherited-merge verification table | 7 entries | **9** — `XASSET-0047` and `XASSET-0048` appended |
| `REQUIRED_TOP_KEYS` | 24 | **26** — two new identity blocks |

**Nothing is overwritten.** The old anchor's identity is preserved in a family of its own:

```
PRIOR_RECONCILIATION_DECISION      XASSET-0047
PRIOR_RECONCILIATION_PULL_REQUEST  347
PRIOR_RECONCILIATION_MERGE_SHA     bb95ed26964b1bc7a2e230c76060fec82752efa1
PRIOR_RECONCILIATION_ACCEPTED_HEAD 8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e
PRIOR_RECONCILIATION_MERGE_BASE    0b76c09f8d1aba01780b4f06fdd692f7393fbfd3
```

**That family is mandatory, not decorative, and this was reproduced before the rebinding was
written.** Against the live module at the base, neither `bb95ed26…` nor `8ae0988d…` appeared under
**any** constant: `XASSET-0047`'s identity was reachable *only* through the three values this unit
moves. Moving them without this family would not have weakened that identity — it would have
**destroyed** it, which `§F.9` forbids.

`XASSET-0048`'s own identity is bound as the **seventh** relationship, deliberately its own family
rather than folded into `RECOVERY_AUTHORIZING_*` (which names `XASSET-0046`, the authority for a
*different* unit):

```
STEP8_EQUIVALENT_AUTHORIZING_DECISION      XASSET-0048
STEP8_EQUIVALENT_AUTHORIZING_PULL_REQUEST  348
STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA     f052efad38e3d57e3e5615799ac3bcbebe83ff5f
STEP8_EQUIVALENT_AUTHORIZING_ACCEPTED_HEAD 42e3a8aec1b36c4e5f22e4cdf4210a61ed781156
STEP8_EQUIVALENT_AUTHORIZING_MERGE_BASE    bb95ed26964b1bc7a2e230c76060fec82752efa1
```

Both new merges join the inherited-merge verification table on exactly the terms every predecessor
already occupies: exact parents in order, a merge tree byte-identical to the accepted head's tree so
zero drift is **proven**, and ancestry into this rebinding's own merge. An absent or incomplete
anchor is a **refusal**, never a skip.

The authorization module's own identity after this rebinding, recomputed **once**, strictly after
every authorized byte stabilized (`§F.8`) — never mid-correction, and never carried forward from a
superseded head:

```
CURRENT_MODULE_SHA256: PENDING_RECOMPUTE_ONCE_AFTER_THE_PULL_REQUEST_NUMBER_IS_BOUND
```

Each predecessor's own declaration is retained, unedited, in its own decision record: it describes
the module **as that unit left it**, which is an immutable fact and stays true. `XASSET-0047`'s is
`e5b509ca74734bffea788d4e7499699356395216285e941164ccf21b6159c924`, and it must no longer match the
live module — that inequality is what proves this unit really rebound rather than leaving a stale
pin agreeing by accident.

### D. The pull-request number was never guessed

The first commit on this branch carries the sentinel **`-2`** — negative, so it can never validate
as a real pull-request number by accident, and deliberately distinct from `XASSET-0047`'s own `0`
and `XASSET-0048`'s own `-1` so this unit's sentinel can never be mistaken for a predecessor's. The
draft pull request was then opened, GitHub issued its own number, that number was read back from
live GitHub, and only then was it bound — in a **subsequent fast-forward commit**, never a
force-push. A wrong number still fails closed at `verify_lifecycle_against_truth`; the point of the
sentinel is that the failure can never be a **silent** one.

### E. The trust boundary grows from sixteen to eighteen — additive only

`XASSET-0037` `§E`'s principle is that the decision supplying the effective structural authorization
must sit **inside** the identity it authorizes, or an attestation could authenticate perfectly while
its own governing text had been edited afterwards. Once the anchor moves, that reaches exactly two
further files:

* `XASSET-0048` — the authority for this rebinding, on precisely the footing `XASSET-0043` occupies
  for the rebinding it authorized and `XASSET-0046` for the recovery it authorized;
* `XASSET-0049` — this decision, the effective structural authorization source after it.

Reproduced before extending: neither appeared anywhere in the tuple, so both sat **outside** the
identity they make lawful and were editable after attestation.

**Nothing is removed, altered, reordered, swapped, or traded away.** `XASSET-0044`'s decision file
stays exactly where `XASSET-0044` put it, and `XASSET-0047`'s exactly where `XASSET-0047` put it: a
stopped lifecycle is not an invalidated one, and a superseded anchor is not a retired one.
`XASSET-0045`'s decision file remains deliberately **absent**, for the reason `XASSET-0047` gave —
it authorizes nothing, so binding it would assert an authority relationship that does not exist.

### F. What is bound, and what is preserved unchanged

`XASSET-0048` `§F.4` restates `§G.B`'s governing invariant unchanged:

> **No outcome-producing executable code may be created, changed, or left outside the bound
> execution identity after the final rebinding and before `ATTEMPT_1`.**

Coverage is proved by exact byte identity, never asserted by naming. The eighteen bound paths
comprise the canonical artifacts, the enforcement/authorization module, the deterministic derivation
surface, the universe-closure validator, the runner, the result validator, and the nine decision
files that make those bytes lawful.

**This unit changes not one outcome-producing byte.** `level1_stage1_runner.py`,
`level1_stage1_result_validator.py`, `level1_construction_universe_closure_validator.py`,
`level1_endpoint_evidence_preregistration_validator.py`, `PROTOCOL_V1.md`, and
`pre_registration.yaml` are **byte-identical to this pull request's base** — proved by blob
comparison in the artifact, not asserted here. `§F.5`'s preserved surface therefore holds trivially
and verifiably: runner semantics, result-validator semantics, universe-closure semantics,
deterministic derivation, result ordering and serialization, the frozen construction identities, the
cardinality **680 / 48**, the aggregate universe hash `73c0965e…5224`, `comparison_subject_kind`,
`unordered_pair_id`, every gate, every disposition rule, and the accepted **B1 / B2 / B3** and
`XASSET-0031` **`G3`** semantics are all unchanged. *The rebinding binds bytes; it does not get to
move meaning.*

### G. Canonical artifacts — an express determination, not an omission

`XASSET-0048` `§E.5` and `§F.7` **permit** canonical amendment: "only in authorization language, only
in lockstep, and **only to the extent the rebinding requires**." The word is *may*, and the bound is
necessity.

**This unit determines that it requires none, and amends neither canonical artifact.** The reasoning
is stated so a reviewer can check it rather than infer it:

1. `§F.4` requires the canonical artifacts to be **bound** — they are, by exact byte identity, and
   they already sit inside `LOAD_BEARING_RELPATHS` with live-matching pins. Binding is not amending.
2. This rebinding's authorization identity is carried entirely by this module's own constants. **No
   canonical byte must move for it to be lawful, coherent, or provable.**
3. Amending them would recompute two canonical pins and oblige this unit to extend the pin-succession
   machinery, materially enlarging a unit `§F.8` and `§F.10` want tight and reviewable — which is the
   enlargement `§F.7`'s "only to the extent required" exists to forbid.

**Consequence, stated plainly rather than left implicit.** The canonical `rebound_by` and
`effective_structural_authorization_source` still name `XASSET-0044`. That remains **literally true**
in the canonical's own sense — `XASSET-0044` is still the last decision that amended those *bytes*,
and this unit amends none of them. `XASSET-0047` drew exactly this distinction and it is preserved
unchanged: *which decision last rebound the canonical bytes* and *which decision's lifecycle the
mechanism authenticates against* are **different relationships**, and overloading them is the failure
mode `XASSET-0037` `§C` named.

The existing refusal that the canonical pins must still equal `XASSET-0044`'s therefore **stays live
and unweakened**. Its *justification* is re-grounded — it previously rested on `XASSET-0046` `§G.9`'s
freeze, which no longer governs this unit; it now rests on this unit's own `§F.7` determination — but
the check itself is byte-for-byte the same comparison, against a historical mapping written as
independent literals rather than derived from the thing it must outlive.

### H. Preserved: every predecessor identity, and all adverse history

`§F.9` is satisfied in full and verified in the artifact rather than asserted here:

* `XASSET-0044` and `XASSET-0045` remain **not effective**; both remain in
  `PERMANENTLY_INEFFECTIVE_DECISIONS` / `PERMANENTLY_INEFFECTIVE_PULL_REQUESTS`, and the module still
  refuses either as an anchor;
* `XASSET-0043` remains **spent**; `XASSET-0040` remains spent as `STOPPED_BEFORE_ATTESTATION`;
* both failed merge-commit CI runs — `32439614683` / job `96647501864` at `f5dedce1…`, and
  `32490789238` / job `96797667282` at `2f8cdebe…` — remain **immutable adverse history**, recorded
  with their exact identities, refused as merge SHAs, and never re-run in place, relabelled,
  deleted, suppressed, waived, or represented as passing;
* every identity family — `XASSET-0028`, `XASSET-0029`, `XASSET-0036`, the executable package,
  `XASSET-0037`, `XASSET-0041`, `XASSET-0042`, `XASSET-0043`, `XASSET-0044`, `XASSET-0045`,
  `XASSET-0046`, and now `XASSET-0047` — is carried forward intact, and none is retired, weakened, or
  collapsed into another.

**`XASSET-0047` is a closed predecessor, not a stopped one.** Its own seven-condition lifecycle
really completed. It stopped being the effective structural authorization source for one reason only:
`XASSET-0048` authorized a successor, and this unit is that successor.

### I. Two further refusals this rebinding adds

Each closes a class the anchor move newly opens, and each is stated as a **refusal in code** rather
than as a prohibition in prose:

1. **The superseded anchor may not silently remain the anchor.** An `AUTHORIZING_DECISION` or
   `AUTHORIZING_PULL_REQUEST` still naming `XASSET-0047` / `#347` is a transition with one end
   missing — drift wearing a rebinding's label — and is refused.
2. **The authority may not be mistaken for the unit.** An anchor naming `XASSET-0048` / `#348` would
   collapse *authority over a unit* into *the unit itself*, precisely the overloading `XASSET-0037`
   `§C` named. `XASSET-0048` `§A` performs no rebinding and cannot be the effective structural
   authorization source its own grant produces. Refused.

### J. Relation to `XASSET-0027` `§P.1` and `XASSET-0029` `§E`

**`§P.1` is untouched, reserved, and unconsumed.** Its exactly-one Stage-1 **evaluation/results** PR
is not consumed, replaced, amended, or counted against, on the three grounds `XASSET-0036` `§C`,
`XASSET-0043` `§E`, and `XASSET-0048` `§C` already recorded: `§P.1`'s PR "may make no production
configuration change," and a rebinding is nothing but production configuration change; `§P.1`'s
deliverable is a results document, and this unit produces none; and `§P.1`'s PR sits **after** arming
while this sits strictly before it. After this merges, `§P.1`'s budget is exactly what it is today:
**one, unspent.**

**`§E`'s activation regress is untouched.** `XASSET-0029` `§E` terminates on a step that "changes no
repository state" — the external runtime attestation. This unit changes repository state extensively
and is therefore categorically outside the step `§E` terminates; `XASSET-0036` `§B.4`, `XASSET-0037`
`§G`, `XASSET-0043` `§D`, and `XASSET-0048` `§D` each reached that conclusion on the same reasoning.
**This decision adds ZERO activation authorizations.** `stage_1_executability.executable` stays
permanently `false` and keeps its enforced-false check. **No committed value in this repository
authorizes Stage-1 execution**, and merging this does not change that. Final activation remains the
external one-shot runtime attestation and the operator's act — never a merged pull request.

### K. Authority withheld — absolute

Performing this rebinding authorizes **nothing further**. `XASSET-0048` `§G` withholds each of the
following from this unit, and none is performed, begun, entered, prepared, or implied:

- renewed readiness verification (`XASSET-0030` `§G.B` step 9 / `XASSET-0041` `§I` link 3);
- renewed drift verification (`§G.B` step 10 / link 4);
- **Step 11** in any part (`§G.B` step 11 / link 5) — `XASSET-0040` stays spent as a stop;
- generating, pre-staging, or validating any **attestation**;
- creating `READY`, `CLAIMED`, or `COMPLETED` lane state, writing `AUTHORIZATION_ROOT`, or writing
  the lane ledger;
- **arming** Stage 1, or setting `stage_1_executability.executable` to anything but `false`;
- **claiming** or consuming any part of `ATTEMPT_1`;
- evaluating any gate for any registered construction;
- executing Stage 1, or performing any results work;
- producing a `stage1_results.yaml`, a per-construction disposition, a cell outcome, or a roll-up;
- acquiring market, fundamental, economic, or Stage-2 data, or any Stage 2 work;
- creating any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- reading, listing, opening, or substantively reusing any `risk_lane_boundary` protected `RISK`
  result;
- reopening, re-deriving, or re-arguing **B1**, **B2**, or **B3**, or `XASSET-0031`'s **`G3`**;
- resolving `XASSET-0024` `§K.1`, or amending `XASSET-0020` `§E.1`;
- consuming any part of `XASSET-0027` `§P.1`'s reserved results PR.

**Links 3, 4 and 5 each require their own separate authority and their own complete lifecycle.**
Completing this rebinding authorizes the next link no more than a clean step-10 result authorized
step 11 — the inference `XASSET-0039` `§K` foreclosed and `XASSET-0041` `§I` restated.

### L. Packaging and fail-closed

One unit, one pull request, per `§F.10`: the rebinding decision and the rebinding itself are here
together, exactly as `XASSET-0037`, `XASSET-0044`, and `XASSET-0047` each were. Splitting them would
produce a decision whose bound bytes do not yet exist and a rebinding whose governing text is not yet
inside the identity it binds. No concrete technical reason to package it differently was found; had
one been, this unit would have **stopped and disclosed** rather than decided it silently.

Every unobtainable fact is an **error**, never silent agreement (`§I`). Ambiguity, drift, a competing
worktree, a dirty tree, an unexpected open pull request, or any condition that would require
expanding this authority is a **stop**, not a judgement call.

### M. Effectivity

This rebinding becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` `§1`;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the pull request
   head's own run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request effects nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not; and post-merge verification without a
successful exact merge-commit CI run does not. **Only complete closure of all seven does.**

These mirror the repository's own committed definition —
`level1_stage1_execution_authorization.REQUIRED_LIFECYCLE_GATES`, a **six-element tuple**; the tuple
is not itself a repository path, the **module containing it** is one of the eighteen load-bearing
paths. Conditions 5–7 are that tuple's last three members; condition 2 is the exact-head discipline
`OPS-0009` `§6` applies to condition 1. The lifecycle omissions that let `XASSET-0044` and
`XASSET-0045` merge with their sixth condition outstanding are not repeated.

**This unit can attain both green PR-head and green merge-commit CI.** No statement anywhere in this
decision disclaims that ability; such a statement would make condition 6 unreachable by construction,
which is the deadlock `XASSET-0045` shipped at its first reviewed head, and it is refused here in
terms. This unit changes no runner, no result validator, no universe value, and no canonical artifact;
its artifact proves its historical claims over **immutable commit ranges only**; and the full
repository suite is additionally run inside an isolated clone at a **simulated merged-`main` state
where `HEAD` equals `origin/main`** — the exact ref position that broke PR #345's assertions — before
this unit is offered for review.

### N. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or
`COMPLETED` lane state; creates no `AUTHORIZATION_ROOT`; arms and executes no Stage 1; creates no
Stage-1 runner, result writer, serializer, result validator, or `stage1_results.yaml`; consumes
nothing of `ATTEMPT_1`; **evaluates no gate for any construction and asserts no per-construction
outcome**; closes no gate on satisfaction and changes no gate's class, index, question, controlling
authority, or failure disposition; **amends no canonical file and changes no hash pin, universe,
cardinality, `comparison_subject_kind`, `unordered_pair_id`, or construction identity**; changes no
runner, result-validator, universe-closure, derivation, ordering, or serialization semantics;
performs no part of `XASSET-0030` `§G.B` steps 9, 10 or 11 and enters none of them; reuses neither
`XASSET-0043` nor `XASSET-0045`, treats neither `XASSET-0044` nor `XASSET-0045` as effective, and
revives neither `XASSET-0040` nor either stopped lifecycle; consumes no part of `XASSET-0027` `§P.1`'s
reserved results PR; acquires no market, fundamental, economic, or Stage-2 data; resolves
`XASSET-0024` `§K.1` neither way and leaves `XASSET-0020` `§E.1` unamended; reopens neither B1, B2,
nor B3, and leaves `XASSET-0031`'s `G3` untouched; grants no Stage 2 and no application authority;
selects no sleeve and creates no endpoint, bound, point, range, percentage, weight, rank, target, or
allocation; weakens no validator or test; **reads, lists, opens, or references no
`risk_lane_boundary` protected result path** and reuses no `RISK` scenario, value, parameter, window,
or result; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder, deployment, trade,
order, or brokerage action; and rewrites no accepted history.

**Stage 1 remains UNARMED and NOT EXECUTABLE. The lane is ABSENT. `ATTEMPT_1` is intact, unclaimed,
and unconsumed.**

## Rationale

`XASSET-0048` closed an authority gap: six consecutive filings had named the step-8-equivalent
rebinding and each had expressly declined to grant it. Granting it left one thing outstanding —
actually performing it — and that is the whole of this unit.

The temptation in a rebinding is to treat it as bookkeeping: change three constants, append two
paths, move on. Three properties resist that reading, and each is enforced here rather than
described.

**A moved value with one end unbound is drift.** `§F.3` makes both ends mandatory. The reason is
concrete rather than stylistic: before this unit, `XASSET-0047`'s own merge and accepted head existed
under no constant at all, so overwriting the anchor would have erased a completed lifecycle's identity
from the repository. That was reproduced against the live module before anything was edited, and the
`PRIOR_RECONCILIATION_*` family exists because of what the reproduction showed, not because a
predecessor happened to have one.

**Descent is not scope.** `XASSET-0048`'s own independent review found the ancestry-only base rule
defective and corrected it to equality before that decision was accepted. Prose corrections decay;
this unit converts it into a pure function with parameters, drives it against a real synthetic later
descendant, and keeps the superseded rule beside it *showing it accept what the corrected rule
refuses*. A rule that cannot be shown failing on the input it was written for is not yet a rule.

**Permission is not obligation.** `§F.7` permits canonical amendment. The easy reading treats a
permission as a checklist item and amends. The bound is necessity, and necessity is absent here, so
`§G` records the determination and its reasoning expressly — including the consequence that the
canonical charter continues to name `XASSET-0044` — rather than leaving a reviewer to discover an
omission and guess whether it was deliberate.

What is deliberately *not* claimed matters as much. This rebinding binds bytes. It does not verify
readiness, does not verify drift, does not enter Step 11, generates no attestation, and arms nothing.
The distance between "the anchor is correct again" and "Stage 1 may run" is three separately
authorized links and one external act, and nothing here shortens it.

## Alternatives considered

**Amend the canonical artifacts in authorization language.** Considered seriously, since `§F.7`
permits it and `XASSET-0037` — the actual step 8 — did amend them. Declined: `§F.7`'s bound is
necessity, and no canonical byte must move for this rebinding to be lawful, coherent, or provable.
Amending would recompute two pins, oblige this unit to extend the pin-succession machinery, and
enlarge a unit two other subsections want tight — for no gain in what the rebinding actually
establishes. The determination and its consequence are recorded in `§G` rather than left silent.

**Fold `XASSET-0047` into the existing `RECOVERY_AUTHORIZING_*` family.** Declined. Those constants
name `XASSET-0046`, the decision that *authorized* the reconciliation; `XASSET-0047` is the
reconciliation *itself*. Authority over a unit and the unit's own merged tree are different
relationships, and the module already keeps them apart for `XASSET-0036`/PR #336 and for
`XASSET-0041`/`XASSET-0042`. Collapsing them is the overloading `XASSET-0037` `§C` named as the
largest failure mode available to a rebinding.

**Retire `XASSET-0044`'s or `XASSET-0047`'s decision file from the trust boundary in exchange for the
two additions.** Declined outright. `§F.6` permits extension only. A stopped lifecycle is not an
invalidated one and a superseded anchor is not a retired one; a path traded away is precisely the
defect this boundary exists to catch.

**Split the decision and the rebinding into two pull requests.** Declined. `§F.10` requires one
coherent unit, and the reason is structural rather than procedural: split, the decision binds bytes
that do not yet exist and the rebinding's governing text sits outside the identity it binds.

**Predict the pull-request number.** Refused. The sentinel-first workflow exists so a guessed number
can never be reviewed, merged, or relied upon, and `-2` is chosen to be impossible *and* distinct from
both predecessors' sentinels.

## Consequences

The lifecycle anchor names an effective decision again, and — for the first time since `XASSET-0042`
lawfully corrected the module — the decision that supplies the effective structural authorization and
the decision that authorized it both sit **inside** the identity they make lawful.

`XASSET-0041` `§I`'s link 2 is discharged. Links 3, 4 and 5 — renewed readiness verification, renewed
drift verification, and a new Step-11 authorization — are exactly as unauthorized as they were before
this filing, and each still requires its own separate authority and its own complete lifecycle.

The trust boundary is eighteen paths. `XASSET-0027` `§P.1`'s reserved evaluation/results PR remains
one, unspent. Stage 1 remains **UNARMED** and **NOT EXECUTABLE**, the lane remains **ABSENT**, and
`ATTEMPT_1` remains intact, unclaimed, and unconsumed.
