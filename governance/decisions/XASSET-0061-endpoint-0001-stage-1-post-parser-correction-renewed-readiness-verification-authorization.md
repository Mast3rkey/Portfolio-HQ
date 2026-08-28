---
decision_id: XASSET-0061
date: 2026-08-28
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, XASSET-0056, XASSET-0057, XASSET-0058, XASSET-0059, XASSET-0060, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_parser_correction_renewed_readiness_verification_authorization.py
---

# XASSET-0061 — ENDPOINT-0001 Stage 1: post-parser-correction renewed readiness-verification authorization

## Context

### Live preflight

Every value below was re-resolved this session from live `git` and the live GitHub API, and from the
git object store — never from a task statement, a prior report, or an inherited summary. Where the
brief and live evidence could have differed, live evidence governs.

| | |
|---|---|
| `origin/main`, GitHub `main`, local `HEAD`, and this branch's base | `413e033ac33741829168762ab24d73327c047d4b` — all four equal |
| Open pull requests at preflight | **0** |
| Worktree | clean; no competing mutation lane |
| PR #361 | **merged and closed**, `merged_by` `Mast3rkey`, merged `2026-08-28T07:34:37Z` |
| PR #361 accepted head | `eac06700e9ca72c30e704899f6b761a7e07717f7` |
| PR #361 base / merge first parent | `301e79334876a4bda6e7b89a6156b34e8d38a605` |
| PR #361 merge parents, in order | `301e79334876…`, then `eac06700e9ca…` — exactly two, **no third** |
| PR #361 merge tree | `998c28a3c7f349cd36796255854924fa7473dfae` — **byte-identical** to the accepted head's own tree |
| Independent FULL exact-head review | [`5047221802`](https://github.com/Mast3rkey/Portfolio-HQ/pull/361#pullrequestreview-5047221802) at `eac06700…` — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, **0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE** |
| Principal exact-head acceptance | [`#issuecomment-5449752973`](https://github.com/Mast3rkey/Portfolio-HQ/pull/361#issuecomment-5449752973) at that exact head |
| Immediate post-merge verification | [`#issuecomment-5449783195`](https://github.com/Mast3rkey/Portfolio-HQ/pull/361#issuecomment-5449783195) |
| Exact merge-commit CI | run `33151977375`, job `98785832731`, **attempt 1**, event `push`, `completed`/`success`, run `head_sha` **`413e033ac33741829168762ab24d73327c047d4b`** — the exact merge SHA, not the PR head |
| Final post-CI lifecycle closure | [`#issuecomment-5449912049`](https://github.com/Mast3rkey/Portfolio-HQ/pull/361#issuecomment-5449912049) |
| `XASSET-0060` effectivity | **all seven `§M` conditions closed** — `XASSET-0060` is EFFECTIVE |
| `LOAD_BEARING_RELPATHS` | **25**, all unique, every one present and hashing identically in the worktree and in the merged tree |
| Authorization module | SHA-256 `3f261b6b3cdcabc5f0cb228d987a52dd36e2a0f522e7fc4e57c483d3c0e3001a`, blob `a9753d1273785e9ce2ebb4de2067489dfbb9156c` |
| `AUTHORIZING_DECISION` / `AUTHORIZING_PULL_REQUEST` / `REVIEWED_BASE_SHA` | `XASSET-0060` / `361` / `301e79334876a4bda6e7b89a6156b34e8d38a605` |
| Stage 1 | **UNARMED and NOT EXECUTABLE**; `stage_1_executability.executable` is `false` |
| Execution lane | **ABSENT**; `AUTHORIZATION_ROOT`, `AUTHORIZATION_PATH`, `CLAIM_PATH`, `COMPLETION_PATH` all absent |
| `stage1_results.yaml` | **absent** — nowhere in the repository or on disk |
| `ENDPOINT-0001::STAGE_1::ATTEMPT_1` | **intact, unclaimed, unconsumed** |
| `XASSET-0061` | independently confirmed **unused** in `governance/decisions.yaml`, `governance/decisions/`, and `operations/WORKSTREAMS.yaml` before it was claimed — not predicted |

### The question this unit answers

`XASSET-0060`'s complete seven-condition `§M` lifecycle closed, so the post-parser-correction
rebinding — `XASSET-0041` `§I` **link 2** — is done. `XASSET-0060` `§K` then states the consequence
in its own words:

> **Links 3, 4 and 5 each require their own separate authority and their own complete lifecycle.**
> Completing this rebinding authorizes the next link no more than a clean step-10 result authorized
> step 11 — the inference `XASSET-0039 §K` foreclosed and `XASSET-0041 §I` restated.

So **link 3** — `XASSET-0030` `§G.B` **step 9**, the read-only execution-readiness verification of
already-bound bytes — is the next unit, and it is **unauthorized**. Nothing in the closed
`XASSET-0057` → `XASSET-0058` → `XASSET-0059` → `XASSET-0060` chain grants it, and each of those four
decisions withholds it by name.

**This filing supplies that authority and nothing else.**

## Decision

### A. Determination — `POST_PARSER_CORRECTION_RENEWED_STEP_9_READINESS_VERIFICATION_AUTHORIZED`

**Exactly one** future, separate, bounded `XASSET-0041` `§I` **link 3** / `XASSET-0030` `§G.B`
**step 9** unit is authorized: a **strictly read-only execution-readiness verification of
already-reviewed, already-bound bytes**, anchored to the complete `XASSET-0060` lifecycle — the PR
#361 merge `413e033ac33741829168762ab24d73327c047d4b` and its accepted head
`eac06700e9ca72c30e704899f6b761a7e07717f7` — and to the **current twenty-five-path binding**.

**This decision performs no part of that verification.** It runs no readiness checklist, issues no
`PASS` and no `FAIL`, and **consumes none of the authority it creates**. It authorizes and defines; a
later, separately reviewed unit verifies.

**Links 4 and 5 — `XASSET-0030` `§G.B` steps 10 and 11 — are not authorized, here or by implication
(`§K`).**

#### A.1 — The distinction any summary of this filing must preserve

Stated once, in a form meant to be quoted verbatim, because the failure mode is a summary that
collapses "performs none of it" into "authorizes none of it":

> `XASSET-0061` **authorizes** exactly one future, separate **link-3** readiness verification against
> the current twenty-five-path binding, but **performs no part of it**. **Links 4 and 5** — and
> attestation, lane creation, arming, claim, gate evaluation, execution, results, allocation work,
> and protected `RISK` access — remain **neither performed nor authorized**.

**Link 3 never belongs inside a "not authorized" list.** It is the one thing this decision grants.
Every enumeration of what is withheld — `§F`, `§K`, `§L`, the `WS-0014` gate, and any pull-request
summary or report describing this filing — must place link 3 on the **authorized-but-unperformed**
side of that line and links 4 and 5 on the withheld side. A record that both grants and denies link 3
is not a wording defect; it is unsafe acceptance evidence, because a reader cannot tell which half
governs.

### B. Why `XASSET-0050` cannot supply this authority — two independent grounds

`XASSET-0050` was the link-3 authorization of its day. It cannot be reused now, and this decision is
not a revival of it. **Either ground below is independently sufficient**; both hold.

**Ground 1 — `XASSET-0050` is spent.** Its grant was "exactly one," and that one was exercised. The
single `XASSET-0050`-authorized unit ran and returned `STEP_9_READINESS_VERIFICATION_PASS`, recorded
as durable external evidence at `issuecomment-5384453102` on PR #350, with conditions C1–C11 all
`PASS` and the **eighteen** bound identities enumerated. A one-shot grant that has been exercised
cannot be exercised again, whatever has changed since.

**Ground 2 — `XASSET-0050`'s anchor no longer describes the system.** That `PASS` verified the
**eighteen**-path boundary bound by `XASSET-0049` / PR #349, at merge
`a941455491cc5e4d3d868775fb6b4b88f0fe2ce3`, observing tree
`e0ee2d4c25066cdc3d1c936015c3ada62bed74e8`, with the authorization module at role-1 identity
`4ff289416b9a…d4541`. Every one of those four values has since moved. The binding is now
**twenty-five** paths under `XASSET-0060` / PR #361, at merge `413e033ac33741…`, tree
`998c28a3c7f3…`, with the module at role-4 identity `3f261b6b3cdc…3001a`.

`XASSET-0050` `§B` applied exactly this reasoning to *its own* predecessor, retiring `XASSET-0038`'s
anchor with the words "**Not one of those four anchors still describes this**." That sentence now
applies to `XASSET-0050` itself, on the same footing and by its own logic. `XASSET-0051` and
`XASSET-0052` are retired for the same two reasons and are likewise not revived.

#### B.1 — This is not a rerun, and it does not re-adjudicate the discharged unit

The `WS-0014` record of `XASSET-0050`'s discharge states that **link 3 must not be rerun or
re-adjudicated**. That instruction is respected in full and is not narrowed by one word.

It governs *that* determination about *those* bytes: the `PASS` at `issuecomment-5384453102`, over
the eighteen paths bound at merge `a941455…`. This decision does not reopen it, does not contradict
it, does not re-examine its conditions, does not weigh it against anything, and does not disturb the
separately preserved duplicate-exercise stop evidence at `issuecomment-5384471997`. That record
stands exactly as it is, and remains **true of what it verified**.

What this decision authorizes is a **different question about different bytes**. `XASSET-0040` `§J`
and `XASSET-0041` `§I` already fix the rule: corrected bytes "are no longer the bytes the single
step-8 rebinding bound," so a correction requires a rebinding, **and any renewed readiness
verification and drift check that correction and rebinding make necessary**. The
`XASSET-0058`/`XASSET-0059` parser correction and the `XASSET-0060` rebinding are exactly such a
correction and rebinding. They moved the module identity, grew the boundary from eighteen paths to
twenty-five, and changed the merge and tree the binding is anchored to. A readiness `PASS` over the
old set is not evidence about the new one, and asking about the new one is not asking the old
question twice.

`XASSET-0060` `§K` is the current controlling statement, filed *after* the discharge, and it treats
links 3, 4 and 5 as forward obligations each requiring their own separate authority — not as
questions already answered.

### C. Relation to `XASSET-0027` `§P.1` — separate, reserved, unconsumed

`XASSET-0027` `§P.1`'s exactly-one **evaluation/results** pull request is **not consumed, replaced,
counted against, or brought forward** by this filing. It stays reserved and unspent. This is a
governance authorization for a read-only verification that produces no result, no disposition and no
`stage1_results.yaml`; `§P.1`'s reserved unit is an output-producing results PR on the far side of
arming. The two sit on opposite sides of the arming boundary and neither consumes the other — the
same reconciliation `XASSET-0036` `§P.1` and `XASSET-0050` `§C` each recorded.

### D. Relation to `XASSET-0029` `§E` — this is not an activation PR, and it adds zero activation authorizations

`XASSET-0029` `§E`'s no-infinite-authorization-regress rule stays **intact and unweakened**.

This filing is **not** an activation PR. It generates no attestation, arms nothing, creates no lane
state, and adds **zero** activation authorizations. `XASSET-0029`'s two-factor model is untouched: no
committed value in this repository authorizes Stage-1 execution, `stage_1_executability.executable`
stays permanently `false`, and an authenticated one-shot **external** pre-execution attestation
remains separately required. Merging this decision changes none of that, and the unit it authorizes
is forbidden from changing any of it either (`§F`).

`§E`'s own terminating condition — that the final step changes no repository state — is satisfied
here in the strongest available form: the authorized unit changes **no** repository state at all
(`§I`).

### E. Authority granted — exactly one future, separate, read-only unit

The future unit **may**, and only in service of `XASSET-0041` `§I` link 3 / `XASSET-0030` `§G.B`
step 9:

1. **Re-verify**, from live `git` and live GitHub, the exact identities of the complete `XASSET-0060`
   / PR #361 lifecycle and its merge — treating live sources as authoritative over any inherited
   summary, **including this decision's own `§G` table**.
2. **Re-verify** that every one of the **25** `LOAD_BEARING_RELPATHS` matches the effective bound
   merge exactly, with the expected identity **derived from the merged git tree at verification
   time**, never from a constant restated in a decision record — the mechanism the accepted
   implementation already uses and this decision does not alter.
3. **Re-verify** the complete four-role module-identity chain, the permanent vulnerable negative pin,
   the effective canonical pins, the frozen universe, the current authorization constants, and the
   parser-correction and rebinding lifecycle continuity enumerated in `§G`.
4. **Run** the repository's validators and its non-executing ENDPOINT CLI checks.
5. **Confirm** the runner remains fail-closed while no attestation exists, that lane state remains
   `ABSENT`, and that the authorization predicates remain `False`.
6. **Read and structurally traverse** the real frozen construction universe, read-only, under
   `XASSET-0036` `§F.1(a)`'s existing permission — which this decision reuses **by reference and does
   not widen by one step**, and which remains conditional on the operation staying read-only and
   non-outcome-producing.
7. **Record** its determination as durable, externally posted evidence (`§I`).

Every one of these is verification of state that already exists. **None creates, edits, regenerates,
or corrects anything.**

### F. Authority withheld — absolute

The authorized unit **must not**:

- create, edit, regenerate, correct, reformat, or re-pin **any** canonical, validator, authorization,
  runner, result-production, universe, governance, or protected portfolio byte;
- **declare any defect "fixed"** during readiness verification, or repair one in passing — a defect
  found is a finding to report and a stop condition (`§H`), never work to perform;
- extend, reduce, re-order, or re-derive `LOAD_BEARING_RELPATHS`, or re-pin any canonical hash;
- change `REQUIRED_LIFECYCLE_GATES`, `AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`,
  `REVIEWED_BASE_SHA`, `NEVER_BINDABLE_MODULE_SHA256`, any role-1/2/3/4 module-identity constant, or
  any other constant in the production authorization module;
- **bind, rehabilitate, or treat as acceptable the role-2 vulnerable intermediate**
  `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5`, whose exclusion is permanent;
- produce an attestation, an `AUTHORIZATION_ROOT`, lane state, a claim, a ledger entry, a completion
  record, a recovery, or an execution;
- create `stage1_results.yaml`, or any real per-construction disposition, cell outcome, or roll-up;
- **evaluate or decide any gate (`G1`–`G12`) for any registered construction**, or consume any part of
  `ATTEMPT_1`;
- perform any portfolio construction, target-allocation calculation, or endpoint, bound, point,
  range, percentage, weight, rank, target, or allocation derivation;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result;
- acquire market, fundamental, economic, or Stage-2 data, or perform any Stage 2 work;
- **correct the parser or alter parser semantics** — that work is `XASSET-0058`/`XASSET-0059`'s and is
  complete;
- reopen, re-derive, or re-argue B1, B2, or B3, any gate semantics, `XASSET-0030`'s 6/6 gate map,
  `XASSET-0024` `§K.1`, or `XASSET-0020` `§E.1`;
- change any construction identity, universe membership, ordering, cardinality, or universe hash;
- consume `XASSET-0027` `§P.1`'s reserved results PR;
- change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- reopen, re-adjudicate, invalidate, or re-weigh `XASSET-0050`'s discharged link-3 determination or
  its preserved duplicate-exercise stop evidence (`§B.1`);
- **perform or authorize `XASSET-0041` `§I` link 4 or link 5 — `XASSET-0030` `§G.B` step 10 or
  step 11.**

#### F.1 — Read-only means read-only

`XASSET-0036` `§F.1` drew the line that protects the one-shot lane: **traversing frozen construction
identities is not execution; applying gate-evaluation semantics to them to derive Stage-1 outcomes
is.** That line is adopted here unchanged, and this unit sits further inside it than the
implementation PR did — the implementation was permitted to *write* the code it validated, and this
unit is permitted to write nothing at all.

**An actual Stage-1 run over the real 680 remains absolutely prohibited** and stays downstream of
attestation → `READY` → lawful claim → execution, exactly as `§G.B` steps 10–11 require.

### G. The closed renewed-readiness checklist

**Closed**: the future unit verifies these and adds no further condition of its own invention; a
condition it believes is missing is a finding to report, not a checklist item to add.

| # | Condition | Grounded in |
|---|---|---|
| **C1** | The complete `XASSET-0060` / PR #361 lifecycle and its exact identities — merged and closed; accepted head `eac06700e9ca72c30e704899f6b761a7e07717f7`; base `301e79334876a4bda6e7b89a6156b34e8d38a605`; FULL exact-head review `5047221802` at that head, 0/0/0/0; principal exact-head acceptance `5449752973`; post-merge verification `5449783195`; merge-commit CI run `33151977375` / job `98785832731`, attempt 1, `head_sha` the exact merge SHA `413e033ac33741829168762ab24d73327c047d4b`; final post-CI closure `5449912049` | `XASSET-0060` `§M`; `OPS-0009` `§6` |
| **C2** | **Zero merge drift** — merge `413e033ac33741829168762ab24d73327c047d4b` carries exactly two ordered parents, `301e79334876…` then `eac06700e9ca…`, with **no third**; merge tree `998c28a3c7f349cd36796255854924fa7473dfae` is byte-identical to the accepted head's own tree; the accepted-head→merge diff is empty | `XASSET-0060` `§§B, M`; `OPS-0009` `§6` |
| **C3** | All **25** `LOAD_BEARING_RELPATHS` match the effective bound merge exactly, identity **derived from the merged tree at verification time**; the set is exactly 25 unique paths, neither extended nor reduced, with the inherited eighteen still an **ordered prefix** and `XASSET-0054` still excluded | `XASSET-0030` `§G.B` step 5; `XASSET-0060` `§F` |
| **C4** | Exact identity of the **five** outcome-capable Python modules inside C3's twenty-five paths, each named individually because each is independently capable of affecting the 680 outcomes. Filing-time verified values: `level1_stage1_runner.py` `4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9`; `level1_stage1_result_validator.py` `b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a`; `level1_endpoint_evidence_preregistration_validator.py` `b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d`; `level1_construction_universe_closure_validator.py` `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5`; `level1_stage1_execution_authorization.py` `3f261b6b3cdcabc5f0cb228d987a52dd36e2a0f522e7fc4e57c483d3c0e3001a`. **See `§G.1` — the operative expectation is the derived one.** | `XASSET-0030` `§G.B` steps 4–5; `XASSET-0060` `§C` |
| **C5** | The complete **four-role module-identity chain** and the **permanent vulnerable negative pin** — role 1 `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541` / blob `f71b08b4ebe95f161c57cdbb2a924748f13af02d`; role 2 `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` / blob `b5622f9e412afd604a11cde04317b79c5e57920a`; role 3 `1283a2d4ccc3794fd37b81d4e5e23ac6f67a0b87b911ef3861c724d636fabd00` / blob `b8414a69f41e37f8fdd5c18dae13176fd847170e`; role 4 `3f261b6b3cdcabc5f0cb228d987a52dd36e2a0f522e7fc4e57c483d3c0e3001a` / blob `a9753d1273785e9ce2ebb4de2067489dfbb9156c`. Roles 1–3 preserved as exact history; the bound end is **role 4 alone**; role 2 remains in `NEVER_BINDABLE_MODULE_SHA256` and is enforced as a refusal, never merely documented | `XASSET-0057` `§F.0`; `XASSET-0060` `§§C, I` |
| **C6** | Effective canonical pins unchanged — `research/level1_endpoint_evidence/PROTOCOL_V1.md` `1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84`, `research/level1_endpoint_evidence/pre_registration.yaml` `898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f` — the pins `XASSET-0044` left, which `XASSET-0049` `§G` and `XASSET-0060` `§G` each expressly declined to amend | `XASSET-0044`; `XASSET-0060` `§G` |
| **C7** | Frozen universe identity unchanged — exactly **680** constructions, **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` | `XASSET-0028`; `XASSET-0036` `§F.1(a)` |
| **C8** | Current authorization constants — `AUTHORIZING_DECISION` `XASSET-0060`, `AUTHORIZING_PULL_REQUEST` `361`, `REVIEWED_BASE_SHA` `301e79334876a4bda6e7b89a6156b34e8d38a605`. `REVIEWED_BASE_SHA` is that rebinding's base, **not** a "current main" field that advances with every merge | `XASSET-0060` `§D` |
| **C9** | **Parser-correction and rebinding lifecycle continuity** — `XASSET-0057` (PR #358, merge `556a43cf9167…`), `XASSET-0058` (PR #359, merge `34c45900ce23…`, accepted head `e8d53c184a76…`) and `XASSET-0059` (PR #360, merge `301e79334876…`, accepted head `90b829863875…`) each closed in full; `XASSET-0059`'s B5 merge is exactly `XASSET-0060`'s required base; the chain from role 1 through role 4 is unbroken, with every adjacent transition provable from the object store | `XASSET-0057` `§§E, F.0`; `XASSET-0060` `§§B, C` |
| **C10** | All required repository validators pass, all ENDPOINT CLI checks exit clean **without executing Stage 1**, and the runner remains **fail-closed while no attestation exists** | `XASSET-0029` `§§B, D`; `XASSET-0030` `§G.B` step 10; `XASSET-0036` `§E.8` |
| **C11** | Execution lane remains **`ABSENT`**; `AUTHORIZATION_ROOT`, `AUTHORIZATION_PATH`, `CLAIM_PATH` and `COMPLETION_PATH` remain **absent**; **no `stage1_results.yaml`** exists in the repository, the merged tree, or on disk | `XASSET-0029` `§B`; `XASSET-0060` Consequences |
| **C12** | Every authorization predicate remains `False` — `new_execution_is_authorized()`, `claimed_execution_is_authorized()` and `active_execution_is_authorized()`; `stage_1_executability.executable` remains `false`; and `ENDPOINT-0001::STAGE_1::ATTEMPT_1` remains **intact, unclaimed, and unconsumed**. **See `§G.2` on the count.** | `XASSET-0029` `§§B, E`; `XASSET-0060` `§N` |
| **C13** | **No output and no persistent execution artifact is created** by the verification — no `stage1_results.yaml`, no lane directory, no attestation, no ledger entry — and the determination is recorded as durable, externally posted evidence **without a repository mutation** | `§§F, I`; `XASSET-0036` `§F.1(b)` |

#### G.1 — Why `§G` records values *and* still derives them, and how the two are reconciled

`§G` pins concrete filing-time values, and `§E.2` simultaneously requires the expected identity to be
**derived from the merged git tree at verification time**. That is deliberate, and the precedence is
fixed rather than left to the verifying session's judgment:

**The derived value is operative. The recorded value is a witness.** If they disagree, the unit does
**not** prefer the decision record and does **not** prefer the live tree in order to pass. A
disagreement is drift, and drift is a **stop** under `§H`.

The recorded table exists so that a discrepancy fails visibly and early — in this filing's own
supporting artifact, in CI, at the moment it appears — rather than waiting to be discovered by the
verifying session much later. It is a tripwire, never a substitute for derivation, and never a value
the verifying unit may copy forward instead of computing.

#### G.2 — On the number of authorization predicates

C12 names **three** predicates, not two. The production module defines
`new_execution_is_authorized`, `claimed_execution_is_authorized` and
`active_execution_is_authorized` as distinct pre-execution authorization predicates, all three of
which were independently evaluated `False` in this session's own read-only preflight, and all three
of which `XASSET-0060`'s own verified record enumerates. Where a brief, a summary or an inherited
description says "both," the live module governs and the count is three. Verifying three is strictly
stronger than verifying two, and the unit may not satisfy C12 by checking fewer.

### H. Fail-closed

**Any** drift, missing identity, missing evidence, mismatch, ambiguity, validation failure, unexpected
lane state, or fact the unit cannot re-derive with certainty **stops the authorized unit**. On any
such condition the unit must:

1. **stop** — not continue to the remaining checklist items as though the condition were minor;
2. **report** the exact condition in its externally posted evidence, as a stop report;
3. **change nothing** — the prohibition in `§F` is not relaxed by the discovery of a defect, and
   **no repair of any kind is authorized**;
4. **not** issue a `PASS`.

**A defect found here requires a separately authorized correction**, and — because the corrected
bytes would no longer be the bytes `XASSET-0060` bound — **any rebinding invalidated by that
correction must itself be redone under its own separate authority**, exactly as `XASSET-0030` `§G.B`
step 5's own reasoning requires, as `§D` there already records for enforcement drift, and as the
`XASSET-0041` → `XASSET-0049` and `XASSET-0053` → `XASSET-0060` chains have each now demonstrated in
practice rather than in principle.

**Uncertainty is failure.** The unit may not resolve an ambiguous state in favour of readiness, and
may not treat an unobtainable fact as silent agreement.

### I. Packaging and evidence — a no-repository-mutation unit

The authorized unit is **one** read-only unit. It creates **no branch, no commit, and no pull
request**, and makes **no repository mutation** — so it does not contend for the `OPS-0014` `§D`
single mutation lane and may run in a clean isolated clone.

Its determination is recorded as **durable, externally posted evidence** — a GitHub comment on the
`ENDPOINT-0001` record of proceedings — stating the verified identities, each checklist condition's
outcome, and an explicit statement of what remains unauthorized. **A repository mutation to record
the result is neither required nor authorized**; if a future session concludes one is genuinely
necessary, that is a finding to report under `§H`, not scope to assume.

### J. Effectivity — the authorized unit may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge — the repository's own six
`REQUIRED_LIFECYCLE_GATES` plus `OPS-0009` `§6`'s exact-head discipline:

1. independent **FULL** exact-head review under `OPS-0007` `§1`;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the pull request
   head's own run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request authorizes nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not; and post-merge verification without a
successful exact merge-commit CI run does not. **Only complete closure of all seven does** — and even
then, what becomes authorized is a **read-only verification**, never arming and never execution.

`XASSET-0044` and `XASSET-0045` each merged and neither became effective, because condition 6 failed.
That history is why this enumeration is stated in full rather than abbreviated.

### K. Links 4 and 5 retain their own separate-authority requirement

Stated unambiguously, because the whole risk of an authorization filing is that a successor reads
more out of it than it contains:

- **Link 3 remains unperformed** until this decision's complete `§J` lifecycle closes, and is then
  performed only as `§§E–I` define it.
- **Link 4 / step 10** — fail-closed handling of post-rebinding drift in runner / result-production
  bytes before `READY` or claim — **retains its own separate-authority requirement** and is not
  authorized here. `§H`'s stop-and-report rule is what the authorized unit does *for itself*; it is
  not a grant of link 4. `XASSET-0051` is spent and its eighteen-path anchor is dead; it is not
  revived, and a renewed link 4 needs its own new filing.
- **Link 5 / step 11** — the external one-shot attestation, arming, the claim, and the
  680-construction run — **retains its own separate-authority requirement** and is **entirely outside
  this filing**. `XASSET-0040` stays spent as a stop and `XASSET-0052`'s operational grant stays spent
  as a stop; neither is revived.
- A `PASS`, however clean, **authorizes nothing further.** It is evidence that the bound bytes are
  unchanged; it is not permission to arm, to claim, or to execute.
- `XASSET-0027` `§P.1`'s reserved evaluation/results PR **remains unspent** (`§C`).

### L. Absolute non-authorization

**Read this section against `§A.1`.** Everything below is a statement about what this decision
**performs**, plus what it withholds from links 4 and 5. It is **not** a denial of the link-3
authority `§A` grants.

This decision performs no readiness verification and issues no `PASS` or `FAIL`. It generates no
`XASSET-0029` attestation and creates no `READY`, `CLAIMED` or `COMPLETED` lane state. It does not
write `AUTHORIZATION_ROOT`, `AUTHORIZATION_PATH`, `CLAIM_PATH` or `COMPLETION_PATH`. It does not arm
Stage 1 and does not set `stage_1_executability.executable` to anything but `false`. It does not claim
or consume any part of `ATTEMPT_1`. It evaluates no gate for any registered construction. It executes
no Stage 1 and performs no results work. It produces no `stage1_results.yaml`, per-construction
disposition, cell outcome or roll-up. It acquires no market, fundamental, economic or Stage-2 data. It
creates no endpoint, bound, point, range, **percentage**, weight, rank, target or allocation. It
changes `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
margin state, charts, ladders, trades and orders not at all. It reads, lists, opens and substantively
reuses no `risk_lane_boundary` protected `RISK` result. It corrects no parser and alters no parser
semantics. It reopens, re-derives and re-argues neither B1, B2 nor B3, nor `XASSET-0031`'s `G3`. It
neither resolves `XASSET-0024` `§K.1` nor amends `XASSET-0020` `§E.1`. It consumes no part of
`XASSET-0027` `§P.1`. It changes no byte of
`level1_stage1_execution_authorization.py`, of any of the twenty-five load-bearing paths, of
`PROTOCOL_V1.md`, of `pre_registration.yaml`, of the runner, of the result validator, or of the
construction universe. It does not reopen, re-adjudicate or invalidate `XASSET-0050`'s discharged
link-3 determination.

**Links 4 and 5 are not authorized by this decision, in whole or in part, expressly or by
implication.**

## Rationale

The link model `XASSET-0041` `§I` fixed — correction, rebinding, renewed readiness, renewed drift
check, new step-11 authorization — is a sequence in which **each link is separately authorized and
separately reviewed**, precisely so that completing one never silently licenses the next. That
property has already been load-bearing twice: `XASSET-0039` `§K` foreclosed the inference from a clean
step-10 result to step 11, and `XASSET-0052`'s link-5 unit then stopped before attestation rather than
proceeding on a defect it discovered. The discipline works because the authority is granted narrowly
and in advance, not assumed afterwards.

The parser correction and the rebinding restarted that sequence at link 3. This is not an accident of
bookkeeping; it is the rule operating as designed. `XASSET-0040` `§J` says corrected bytes "are no
longer the bytes the single step-8 rebinding bound" — and the `XASSET-0058`/`XASSET-0059` correction
plus the `XASSET-0060` rebinding moved the module identity from role 1 to role 4, grew the boundary
from eighteen paths to twenty-five, and re-anchored the binding to a new merge and a new tree. A
readiness `PASS` taken over the old set is simply not evidence about the new one. `XASSET-0060` `§K`
records the consequence directly, and this filing is the response to it.

Two things had to be got right, and each is a place where a plausible-sounding shortcut would have
been wrong.

**First, the relationship to `XASSET-0050`.** The tempting framings are that its spent `PASS` still
covers the system, or that the instruction "link 3 must not be rerun or re-adjudicated" forecloses
this filing. Neither survives inspection. The `PASS` enumerated *eighteen* identities at a tree that
no longer exists in the binding; treating it as current would be exactly the stale-anchor error
`XASSET-0050` `§B` itself diagnosed in `XASSET-0038`. And the no-rerun instruction protects that
determination about those bytes — it is honoured here in full, and `§B.1` states so explicitly rather
than leaving it to inference. Asking a new question about different bytes is not re-asking the old
one. Both grounds in `§B` are stated because either alone would suffice, and a reader should not have
to reconstruct which one is doing the work.

**Second, the recorded-versus-derived tension.** Pinning concrete hashes in a governance record is
useful — it makes drift fail early, in CI, in this filing's own supporting artifact. But a pinned
value can also become a stale value that a later session copies forward instead of computing. `§G.1`
resolves this by fixing the precedence in advance: derived is operative, recorded is a witness, and
disagreement is a stop rather than a judgment call. That is the same ordering `XASSET-0050` `§G.1`
adopted, and it is restated here rather than cross-referenced because a precedence rule that a reader
has to go and look up is a precedence rule that will eventually be guessed at.

One smaller thing is worth recording. The brief this session worked from described "both
authorization predicates"; the live module defines three. Rather than quietly following the brief or
quietly following the module, `§G.2` names the discrepancy and fixes the count at three, which is the
stricter reading and the one the live system supports. The same discipline applied to every other
value: `origin/main`, the merge parents and tree, the review and comment identifiers, the CI run and
job, the twenty-five paths, the four module roles, the canonical pins and the universe identity were
each re-resolved from live sources this session, and the brief was treated as a hypothesis to check
rather than a fact to restate.

This decision is deliberately **not** added to `LOAD_BEARING_RELPATHS`. `XASSET-0037` `§E`'s principle
— that a decision supplying effective structural authorization must sit inside the identity it
authorizes, or an attestation could authenticate perfectly while its own governing text had been
edited afterwards — reaches decisions that make an *attestation* lawful. This one does not: it
authorizes a read-only verification that produces no attestation, writes no byte, and changes no
authorization state. The precedent is unambiguous and was checked rather than assumed —
`XASSET-0038`, `XASSET-0050`, `XASSET-0051` and `XASSET-0052`, the four prior link-3/4/5
authorizations, are each **absent** from the boundary today. Adding this one would assert a structural
relationship that does not exist, and would also require editing the production module, which is
forbidden here on independent grounds.

## Alternatives considered

**Treat `XASSET-0050`'s `PASS` as still current and skip link 3.** Rejected. It verified eighteen
identities at merge `a941455…` and tree `e0ee2d4c…`; the binding is now twenty-five identities at
merge `413e033a…` and tree `998c28a3…`, with a different module identity. Carrying that `PASS`
forward would assert readiness about bytes it never examined — the precise failure `§H`'s
stop-and-report rule exists to prevent, and the precise error `XASSET-0050` `§B` identified in its own
predecessor.

**Revive, amend or re-run `XASSET-0050`.** Rejected on two independent grounds (`§B`). Its one-shot
grant is spent, and its anchor is dead. Amending a spent, superseded authorization to cover a new
binding would also destroy the audit property that makes the link model worth having: a reader could
no longer tell which binding a given `PASS` spoke to.

**Fold link 3 into the `XASSET-0060` rebinding filing.** Not available — that lifecycle is closed —
and it would have been wrong even while open. `XASSET-0060` `§K` withholds link 3 by name, and a
rebinding that verified its own readiness would be marking its own homework.

**Authorize links 3, 4 and 5 together in one filing.** Rejected. `XASSET-0041` `§I` and `XASSET-0060`
`§K` each require separate authority and a separate complete lifecycle per link, and the sequence's
whole value is that a clean result at one link does not license the next. Bundling would also put
attestation and arming authority into a filing whose subject is a read-only check.

**Have this filing perform the verification as well as authorize it.** Rejected, and this is the
sharpest line in the document. A unit that grants itself an authority and exercises it in the same
breath produces acceptance evidence that no reviewer can decompose: the review can no longer separate
"was this authority correctly scoped" from "was it correctly exercised." `§A` grants; a later,
separately reviewed unit verifies.

**Record the future determination as a repository commit rather than external evidence.** Rejected.
The verification is defined as read-only, and a mutation to record a read-only result would make the
unit contend for the `OPS-0014` `§D` mutation lane and create a byte whose own provenance would then
need governing. `§I` requires durable external evidence instead, and makes a contrary conclusion a
`§H` finding rather than assumable scope.

**Add this decision to `LOAD_BEARING_RELPATHS`.** Rejected — see the Rationale. It supplies no
attestation-enabling structural authority, the four prior link-3/4/5 authorizations are each absent
from the boundary, and doing so would require editing the production module.

## Consequences

`XASSET-0061` is **`Proposed`** and becomes effective only on complete closure of all seven `§J`
conditions. Until then it authorizes nothing, and the link-3 unit may not begin.

On effectivity, and only then, **exactly one** future, separate, strictly read-only link-3 readiness
verification becomes authorized, bounded by the `§G` checklist, the `§F` prohibitions, the `§H`
fail-closed rule and the `§I` no-repository-mutation requirement. That unit will itself require its
own independent review of its determination; a `PASS` authorizes nothing further.

**Links 4 and 5 — renewed drift verification and Step 11 — remain separately unauthorized.** No
renewed drift-check authority is created. No Step-11 authority is created. No attestation is
generated. Nothing is armed. Nothing is claimed. Nothing is executed. No result is produced.
`XASSET-0027` `§P.1`'s reserved results PR remains one, unspent.

Merging this decision leaves the Stage-1 posture exactly as this session found it: Stage 1 **UNARMED
and NOT EXECUTABLE**, `stage_1_executability.executable` `false`, execution lane **ABSENT**,
`AUTHORIZATION_ROOT` / `AUTHORIZATION_PATH` / `CLAIM_PATH` / `COMPLETION_PATH` absent, no
`stage1_results.yaml`, all three authorization predicates `False`, and
`ENDPOINT-0001::STAGE_1::ATTEMPT_1` **intact, unclaimed and unconsumed**.

`XASSET-0050`'s discharged link-3 determination, and the preserved duplicate-exercise stop evidence
beside it, are untouched: not reopened, not re-adjudicated, not invalidated, not re-weighed. They
remain true of what they verified.
