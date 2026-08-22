---
decision_id: XASSET-0050
date: 2026-08-22
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_renewed_readiness_verification_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every hash below was **recomputed**, not recalled.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main`, branch base | all four exactly `a941455491cc5e4d3d868775fb6b4b88f0fe2ce3` |
| Worktree / stash | clean; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #349 | **closed, merged, not draft**; `merged_by` `Mast3rkey`; merged `2026-08-22T16:47:55Z` |
| PR #349 base | `f052efad38e3d57e3e5615799ac3bcbebe83ff5f` |
| PR #349 accepted head | `b2059e80101fc6457f4004939d7d12886e6feedf` |
| PR #349 merge parents, in order | `f052efad38e3d57e3e5615799ac3bcbebe83ff5f`, then `b2059e80101fc6457f4004939d7d12886e6feedf`; **no third parent** |
| PR #349 merge tree | `b7015b271362ae0c2fe663e8bfda9c6d10de5e7e` — **byte-identical to the accepted head's own tree**; accepted-head→merge diff empty |
| Independent FULL review | [`5000502119`](https://github.com/Mast3rkey/Portfolio-HQ/pull/349#pullrequestreview-5000502119) at `8ab773866c5959cd61a73dd48af197339c48754a` — CHANGES REQUIRED, 0 BLOCKING / **1 MAJOR** / 0 MINOR / 0 NOTE |
| Bounded correction | `8ab77386…` → `b2059e80…` |
| Exact-head DELTA re-review | [`5000581301`](https://github.com/Mast3rkey/Portfolio-HQ/pull/349#pullrequestreview-5000581301), `commit_id` `b2059e80101fc6457f4004939d7d12886e6feedf` — **0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE** |
| Principal acceptance | [`#issuecomment-5381488381`](https://github.com/Mast3rkey/Portfolio-HQ/pull/349#issuecomment-5381488381), at that exact head |
| Post-merge verification | [`#issuecomment-5381551149`](https://github.com/Mast3rkey/Portfolio-HQ/pull/349#issuecomment-5381551149) |
| Merge-commit CI | run `32585793843`, job `97061842978`, **attempt 1**, event `push`, `completed` / `success`, `head_sha` **`a941455491cc5e4d3d868775fb6b4b88f0fe2ce3`** — the exact merge SHA, not the PR head; **10952 passed** |
| Final lifecycle closure | [`#issuecomment-5381561978`](https://github.com/Mast3rkey/Portfolio-HQ/pull/349#issuecomment-5381561978), posted strictly after both post-merge verification and CI completion |
| `XASSET-0049` effectivity | **all seven conditions closed** — `XASSET-0049` is EFFECTIVE |
| `XASSET-0050` | **unused** — zero occurrences in tracked files, in `governance/decisions.yaml`, in `governance/decisions/`, and across the entire reachable history |
| `LOAD_BEARING_RELPATHS` | **18**, all unique, every one hashing identically in the worktree and in the merged tree `a941455…` |
| Effective canonical pins | `PROTOCOL_V1.md` `1ad1d060…d0c84`, `pre_registration.yaml` `898c329d…2d82f` — both matching their files exactly |
| Frozen universe | **680** constructions, **48** cells, aggregate `73c0965e…5224`; closure validator `OK (680 registered constructions across 48 cells)` |
| Construction-universe module | SHA-256 `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5` |
| `REQUIRED_LIFECYCLE_GATES` | the existing **six**-element tuple, unchanged |
| Lane state | `ABSENT`; `AUTHORIZATION_ROOT` does not exist |
| `new_execution_is_authorized()` | `False` |
| `stage_1_executability.executable` | `false` |
| `ATTEMPT_1` | `ENDPOINT-0001::STAGE_1::ATTEMPT_1` — intact, unclaimed, unconsumed |
| `stage1_results.yaml` | absent anywhere in the tree |

Regenerating the 680 / 48 / aggregate figures and reading the frozen universe is expressly authorized
read-only structural traversal under `XASSET-0036` §F.1(a), and consumes nothing: **no gate was
evaluated for any construction.**

### The question this unit answers

`XASSET-0049`'s complete seven-condition lifecycle closed, so `XASSET-0041` §I **link 2** — the
`XASSET-0030` §G.B step-8-equivalent successor operational / load-bearing rebinding — is discharged.
**Link 3 is next**, and it has **no authority**.

`XASSET-0041` §I fixes the sequence and the separateness in one place:

```
1. correction              <-- XASSET-0041 / XASSET-0042        (done)
2. rebinding                   step-8 equivalent                (done: XASSET-0048 / XASSET-0049)
3. renewed readiness           step-9 equivalent, read-only     <-- THIS decision authorizes only this
4. renewed drift check         step-10 equivalent, fail-closed  (separately authorized)
5. new step-11 authorization   XASSET-0040 is spent as a stop   (separately authorized)
```

and states that "**None of links 2 through 5 is authorized, pre-authorized, combined, or made
reachable by this decision or by the correction succeeding.**"

**`XASSET-0038` does not supply the missing authority, for two independent reasons, either sufficient
on its own.**

1. **Its grant is spent.** `XASSET-0038` §A authorized "**exactly one**" step-9 unit. That unit ran
   and returned `STEP_9_READINESS_VERIFICATION_PASS`, C1–C11 all `PASS`, recorded at
   [`#issuecomment-5336643459`](https://github.com/Mast3rkey/Portfolio-HQ/pull/338#issuecomment-5336643459)
   and relied upon as an input by `XASSET-0039` §C. An exactly-one budget that has been consumed
   cannot fund a second unit.
2. **Its anchor is dead.** `XASSET-0038` anchored its checklist to the PR #337 merge
   `637eaa30302f5a71f84ab1d215ecbd32c01399b5`, accepted head `f40c816223c78f1d1e436b718455df5fb3d77fa7`,
   **10** `LOAD_BEARING_RELPATHS`, and canonical pins `367583b6…d8971` / `768b013c…4bce1`. `XASSET-0042`
   then corrected load-bearing path #1, `XASSET-0044` amended both canonical artifacts, and the
   boundary has since grown to **18** paths. **Not one of those four anchors still describes this
   system.** A `PASS` about bytes that no longer exist is evidence about a moment that has passed, not
   a readiness finding about the bytes an attestation would authenticate.

**Five** filings after `XASSET-0038` named the renewed verification and **all five** declined to
grant it:

| Accepted text | What it says about the renewed readiness verification |
|---|---|
| `XASSET-0041` §I | Names it **link 3**; "separately authorized; step-9 equivalent, read-only"; withholds links 2–5 |
| `XASSET-0043` §G.9 | "The rebinding performs and authorizes no readiness…"; §C records that "no part of the authorized step-9 readiness verification or step-10 drift check was performed" |
| `XASSET-0046` | Withholds "renewed readiness verification" by name |
| `XASSET-0048` §G | Withholds "renewed readiness verification (`XASSET-0030` §G.B step 9 / `XASSET-0041` §I link 3)" by name |
| `XASSET-0049` | Withholds the same by name, and its Consequences state "Links 3, 4 and 5 — renewed readiness verification, renewed drift verification, and Step 11 — remain separately unauthorized" |

**The gap is therefore established by accepted repository text, not inferred from this unit's
convenience.** This decision closes it for the renewed readiness verification and for nothing else.

## Decision

### A. Determination — `RENEWED_STEP_9_READINESS_VERIFICATION_AUTHORIZED`

**Exactly one** future, separate, bounded `XASSET-0041` §I **link 3** / `XASSET-0030` §G.B **step 9**
unit is authorized: a **strictly read-only execution-readiness verification of already-reviewed,
already-bound bytes**, anchored to the PR #349 merge `a941455491cc5e4d3d868775fb6b4b88f0fe2ce3` and
its accepted head `b2059e80101fc6457f4004939d7d12886e6feedf`.

**This decision performs no part of that verification.** It runs no readiness checklist, issues no
`PASS` or `FAIL`, and **consumes none of the authority it creates**. It authorizes and defines; a
later, separately reviewed unit verifies.

**Links 4 and 5 — `XASSET-0030` §G.B steps 10 and 11 — are not authorized, here or by implication
(§K).**

#### A.1 — The distinction any summary of this filing must preserve

Stated once, in a form meant to be quoted verbatim, because the failure mode is a summary that
collapses "performs none of it" into "authorizes none of it":

> `XASSET-0050` **authorizes** exactly one future, separate **link-3** readiness verification, but
> **performs no part of it**. **Links 4 and 5** — and attestation, lane creation, arming, claim, gate
> evaluation, execution, results, allocation work, and protected `RISK` access — remain **neither
> performed nor authorized**.

**Link 3 never belongs inside a "not authorized" list.** It is the one thing this decision grants.
Every enumeration of what is withheld — §F, §K, §L, the `WS-0014` gate, and any pull-request summary
or report describing this filing — must place link 3 on the **authorized-but-unperformed** side of
that line and links 4 and 5 on the withheld side. A record that both grants and denies link 3 is not
a wording defect; it is unsafe acceptance evidence, because a reader cannot tell which half governs.

### B. This is a narrow successor to `XASSET-0038`, not a revival of it

`XASSET-0038` is **not** reopened, extended, amended, revived, or re-scoped, and its spent grant is
not restored. Its structure and its C1–C11 shape are adopted as a **template**; its *values* are
not inherited. Every anchor, count, and pin in §G is re-derived from the live system at this
filing, and the superseded values are recorded as explicit negative pins in the supporting artifact
so a silent reversion to `XASSET-0038`'s dead anchor fails a test rather than passing unnoticed.

The completed `STEP_9_READINESS_VERIFICATION_PASS` of 2026-08-19 stays exactly as it is: a true,
closed finding about the PR #337 bytes, an input `XASSET-0039` §C already consumed, and **not**
evidence about the bytes `XASSET-0049` bound. This decision neither re-adjudicates it nor relies on
it.

### C. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

§P.1's exactly-one Stage-1 **evaluation/results** PR is **not consumed, replaced, amended, or counted
against**, on the grounds `XASSET-0036` §C, `XASSET-0037` §H and `XASSET-0038` §C each already
recorded, and which apply here more strongly, not less:

- §P.1's PR delivers a **results document**; the authorized unit produces **no result of any kind**,
  and §F bars it from producing one.
- §P.1's PR sits **after arming**; this verification sits **before** it.
- §P.1's PR "may make no production configuration change"; the authorized unit makes **no repository
  change at all**, production or otherwise.

After this decision merges, §P.1's budget is exactly what it is today: **one, unspent.**

### D. Relation to `XASSET-0029` §E — this is not an activation PR, and it adds zero activation authorizations

`XASSET-0029` §E terminates the activation regress on a step that **changes no repository state** —
the runtime attestation — and states that "no additional authorization PR is ever required" for
arming.

**Nothing here reopens that.** This decision:

- generates **no** attestation and authorizes none;
- creates **no** `AUTHORIZATION_ROOT`, `READY`, `CLAIMED`, or `COMPLETED` lane state, no claim, and no
  ledger entry, and authorizes none;
- adds **zero** activation authorizations;
- leaves `stage_1_executability.executable` permanently `false` with its enforced-false check intact;
- leaves `REQUIRED_LIFECYCLE_GATES` as the existing six-element tuple, and the production
  authorization module as the load-bearing enforcement path.

**No committed value in this repository authorizes Stage-1 execution**, and **merging this decision
authorizes a future read-only verification only — it does not make Stage 1 armed or executable.**

The final activation remains what `XASSET-0029` §E, `XASSET-0036` §D, `XASSET-0037` §G and
`XASSET-0038` §D each already require: **the external one-shot runtime attestation and the operator's
act — not a merged activation PR.** This verification is neither that attestation nor arming; it is
the confirmation that the bytes an attestation would authenticate are still exactly the bytes
`XASSET-0049` bound.

### E. Authority granted — exactly one future, separate, read-only unit

The future unit **may**, and only in service of `XASSET-0041` §I link 3 / `XASSET-0030` §G.B step 9:

1. **Re-verify** the exact Git and GitHub identities of the PR #349 lifecycle and its merge, from live
   sources, treating them as authoritative over any inherited summary — including this decision's own
   §G table.
2. **Re-verify** that every one of the **18** `LOAD_BEARING_RELPATHS` matches the effective bound
   merge exactly, with expected identity **derived from the merged git tree at verification time**,
   never from a constant restated in a decision record — the mechanism the accepted implementation
   already uses and this decision does not alter.
3. **Re-verify** the effective canonical pins, the frozen universe, and the identities enumerated in
   §G.
4. **Run** the repository's validators and its non-executing ENDPOINT CLI checks.
5. **Confirm** the runner remains fail-closed while no attestation exists, that lane state remains
   `ABSENT`, and that `new_execution_is_authorized()` remains `False`.
6. **Read and structurally traverse** the real frozen construction universe, read-only, under
   `XASSET-0036` §F.1(a)'s existing permission — which this decision reuses **by reference and does
   not widen by one step**, and which remains conditional on the operation staying read-only and
   non-outcome-producing.
7. **Record** its determination as durable, externally posted evidence (§I).

Every one of these is verification of state that already exists. **None creates, edits, regenerates,
or corrects anything.**

### F. Authority withheld — absolute

The authorized unit **must not**:

- create, edit, regenerate, correct, reformat, or re-pin **any** canonical, validator, authorization,
  runner, result-production, universe, governance, or protected portfolio byte;
- **declare any defect "fixed"** during readiness verification, or repair one in passing — a defect
  found is a finding to report and a stop condition (§H), never work to perform;
- extend, reduce, re-order, or re-derive `LOAD_BEARING_RELPATHS`, or re-pin any canonical hash;
- change `REQUIRED_LIFECYCLE_GATES`, `AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`,
  `REVIEWED_BASE_SHA`, or any other constant in the production authorization module;
- produce an attestation, an `AUTHORIZATION_ROOT`, lane state, a claim, a ledger entry, a completion
  record, a recovery, or an execution;
- create `stage1_results.yaml`, or any real per-construction disposition, cell outcome, or roll-up;
- **evaluate or decide any gate (`G1`–`G12`) for any registered construction**, or consume any part of
  `ATTEMPT_1`;
- perform any portfolio construction, target-allocation calculation, or endpoint, bound, point,
  range, percentage, weight, rank, target, or allocation derivation;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result;
- acquire market, fundamental, economic, or Stage-2 data, or perform any Stage 2 work;
- reopen, re-derive, or re-argue B1, B2, or B3, any gate semantics, `XASSET-0030`'s 6/6 gate map,
  `XASSET-0024` §K.1, or `XASSET-0020` §E.1;
- change any construction identity, universe membership, ordering, cardinality, or universe hash;
- consume `XASSET-0027` §P.1's reserved results PR;
- change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- **perform or authorize `XASSET-0041` §I link 4 or link 5 — `XASSET-0030` §G.B step 10 or step 11.**

#### F.1 — Read-only means read-only

`XASSET-0036` §F.1 drew the line that protects the one-shot lane: **traversing frozen construction
identities is not execution; applying gate-evaluation semantics to them to derive Stage-1 outcomes
is.** That line is adopted here unchanged, and this unit sits further inside it than the
implementation PR did — the implementation was permitted to *write* the code it validated, and this
unit is permitted to write nothing at all.

**An actual Stage-1 run over the real 680 remains absolutely prohibited** and stays downstream of
attestation → `READY` → lawful claim → execution, exactly as §G.B steps 10–11 require.

### G. The closed renewed-readiness checklist

**Closed**: the future unit verifies these and adds no further condition of its own invention; a
condition it believes is missing is a finding to report, not a checklist item to add.

| # | Condition | Grounded in |
|---|---|---|
| **C1** | Exact PR #349 Git/GitHub identities — merge `a941455491cc5e4d3d868775fb6b4b88f0fe2ce3`; ordered parents `f052efad…` then `b2059e80…` with no third; merge tree `b7015b271362ae0c2fe663e8bfda9c6d10de5e7e` identical to the accepted-head tree; FULL review `5000502119`; clean exact-head DELTA review `5000581301` at `b2059e80…`; principal acceptance `5381488381`; post-merge verification `5381551149`; merge-commit CI run `32585793843` / job `97061842978` at the exact merge SHA; final closure `5381561978` — with **zero post-review and post-merge drift** | `XASSET-0049` §§B–C; `OPS-0009` §6 |
| **C2** | All **18** `LOAD_BEARING_RELPATHS` match the effective bound merge `a941455…` exactly, identity **derived from the merged tree at verification time**; the set is exactly 18 unique paths, neither extended nor reduced | `XASSET-0030` §G.B step 5; `XASSET-0049` §§C–D |
| **C3** | Exact identity of the **runner**, the **result validator**, the **preregistration derivation module**, the **construction-universe module**, and the **execution-authorization module** — the five Python modules inside C2's eighteen paths, each named individually because each is independently capable of affecting the 680 outcomes. Filing-time verified values: `level1_stage1_runner.py` `4a88cf6d0271da0dc3a6ca175fadb0223bf7ff8843479733cbcf0effd47ba5d9`; `level1_stage1_result_validator.py` `b4773eb767158434136b72316e9802308b9e6fb47b6e45f8f10445c02cee3b7a`; `level1_endpoint_evidence_preregistration_validator.py` `b3a87e4f8b828d420795348642c977a9f0585eafa9262a4be48df406f770233d`; `level1_construction_universe_closure_validator.py` `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5`; `level1_stage1_execution_authorization.py` `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541`. **See §G.1 — the operative expectation is the derived one.** | `XASSET-0030` §G.B steps 4–5; `XASSET-0049` §C |
| **C4** | Effective canonical pins unchanged — `research/level1_endpoint_evidence/PROTOCOL_V1.md` `1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84`, `research/level1_endpoint_evidence/pre_registration.yaml` `898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f` — the pins `XASSET-0044` left and `XASSET-0049` §G declined to amend. **These are not `XASSET-0038`'s values** | `XASSET-0044`; `XASSET-0047` §D; `XASSET-0049` §G |
| **C5** | Frozen universe exactly **680** constructions, **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` | `XASSET-0028`; `XASSET-0036` §F.1(a) |
| **C6** | Construction-universe module SHA-256 `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5` | `XASSET-0037` eighth correction, MAJOR 1 |
| **C7** | All required repository validators pass, and all ENDPOINT CLI checks exit clean **without executing Stage 1** | `XASSET-0036` §E.8 |
| **C8** | The runner remains **fail-closed while no attestation exists** | `XASSET-0029` §§B, D; `XASSET-0030` §G.B step 10 |
| **C9** | Lane state remains `ABSENT`, `new_execution_is_authorized()` remains `False`, `stage_1_executability.executable` remains `false`, and `ATTEMPT_1` remains intact, unclaimed, and unconsumed | `XASSET-0029` §B; `XASSET-0049` Consequences |
| **C10** | **No output and no persistent execution artifact is created** by the verification — no `stage1_results.yaml`, no lane directory, no attestation, no ledger entry | §F; `XASSET-0036` §F.1(b) |
| **C11** | Durable, externally posted evidence recording the determination, **without a repository mutation** | §I |

#### G.1 — Why C3 records values *and* still derives them, and how the two are reconciled

`XASSET-0038` §G deliberately declined to restate the five module hashes, reasoning that doing so
"would create a second source of truth that could silently disagree with the first."

**That concern is correct and is not waived here — it is closed by construction.** C3 records the
five filing-time verified values *and* C2's derive-from-the-merged-tree mechanism remains the
**operative** expectation. The recorded values are a redundant, independently checkable witness,
not the authority. Three rules make the redundancy safe rather than dangerous:

1. **The derived value governs.** If the tree and this record disagree, the tree is not overridden by
   the record, and the record is not quietly corrected to match.
2. **Disagreement is itself a §H stop.** A mismatch between the derived identity and the recorded
   witness is a readiness failure to report, never a discrepancy to resolve in favour of either side.
3. **The witness is pinned by test.** The supporting artifact asserts that the five recorded values
   equal the values derived from the merged tree, so a drift between them fails in CI rather than
   waiting to be noticed at verification time.

The disagreement `XASSET-0038` feared was a **silent** one. Under these three rules it cannot be
silent: it is detected by test, and if it somehow survived to verification time it stops the unit.

### H. Fail-closed

**Any** drift, missing identity, validation failure, unexpected lane state, or state the unit cannot
determine with certainty **stops the authorized unit**. On any such condition the unit must:

1. **stop** — not continue to the remaining checklist items as though the condition were minor;
2. **report** the exact condition in its externally posted evidence;
3. **change nothing** — the prohibition in §F is not relaxed by the discovery of a defect;
4. **not** issue a `PASS`.

**A defect found here requires a separately authorized correction**, and — because the corrected
bytes would no longer be the bytes `XASSET-0049` bound — **any rebinding invalidated by that
correction must itself be redone under its own separate authority**, exactly as `XASSET-0030` §G.B
step 5's own reasoning requires, as §D there already records for enforcement drift, and as the
`XASSET-0041` → `XASSET-0049` chain has now demonstrated in practice rather than in principle.

**Uncertainty is failure.** The unit may not resolve an ambiguous state in favour of readiness.

### I. Packaging and evidence

The authorized unit is **one** read-only unit. It creates **no branch, no commit, and no pull
request**, and makes **no repository mutation** — so it does not contend for the `OPS-0014` §D single
mutation lane and may run in a clean isolated clone.

Its determination is recorded as **durable, externally posted evidence** — a GitHub comment on the
`ENDPOINT-0001` record of proceedings — stating the verified identities, each checklist condition's
outcome, and an explicit statement of what remains unauthorized. **A repository mutation to record
the result is neither required nor authorized**; if a future session concludes one is genuinely
necessary, that is a finding to report under §H, not scope to assume.

### J. Effectivity — the authorized unit may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge — the repository's own six
`REQUIRED_LIFECYCLE_GATES` plus `OPS-0009` §6's exact-head discipline:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own CI
   run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this PR authorizes nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not; and post-merge verification without a successful
exact merge-commit CI run does not. **Only complete closure of all seven does** — and even then, what
becomes authorized is a **read-only verification**, never arming and never execution.

### K. Links 4 and 5 retain their own separate-authority requirement

Stated unambiguously, because the whole risk of an authorization filing is that a successor reads
more out of it than it contains:

- **Link 3 remains unperformed** until this decision's complete §J lifecycle closes, and is then
  performed only as §§E–I define it.
- **Link 4 / step 10** — fail-closed handling of post-rebinding drift in runner / result-production
  bytes before `READY` or claim — **retains its own separate-authority requirement** and is not
  authorized here. §H's stop-and-report rule is what the authorized unit does *for itself*; it is not
  a grant of link 4.
- **Link 5 / step 11** — the external one-shot attestation, arming, the claim, and the
  680-construction run — **retains its own separate-authority requirement** and is **entirely outside
  this filing**. `XASSET-0040` stays spent as a stop and is not revived.
- A `PASS`, however clean, **authorizes nothing further.** It is evidence that the bound bytes are
  unchanged; it is not permission to arm, to claim, or to execute.
- `XASSET-0027` §P.1's reserved evaluation/results PR **remains unspent** (§C).

### L. Absolute non-authorization

**Read this section against §A.1.** Everything below is a statement about what this decision
**performs**, plus what it withholds from links 4 and 5. It is **not** a denial of the link-3
authority §A grants: link 3 is authorized and unperformed; links 4 and 5 are neither.

This decision generates no attestation; creates no `AUTHORIZATION_ROOT` and no `READY`, `CLAIMED`, or
`COMPLETED` lane state or ledger entry; arms, claims, completes, executes, or recovers no Stage-1
execution; performs no part of `XASSET-0041` §I link 3, and neither performs nor authorizes links 4
or 5; evaluates no gate
for any registered construction and asserts no per-construction outcome; performs no portfolio
construction and no target-allocation calculation; creates no `stage1_results.yaml` and no runner,
result validator, or other outcome-producing code; changes no `LOAD_BEARING_RELPATHS`, no canonical
file, and no hash pin; changes no constant in the production authorization module, which remains
byte-identical to its state at `a941455491cc5e4d3d868775fb6b4b88f0fe2ce3` and remains the load-bearing
enforcement path; changes no construction identity, universe membership, ordering, cardinality, or
universe hash; consumes nothing of `ATTEMPT_1`; acquires no market, fundamental, economic, or Stage-2
data and performs no Stage 2 work; reads, lists, opens, or references no `risk_lane_boundary`
protected `RISK` result; resolves `XASSET-0024` §K.1 neither way and amends no `XASSET-0020` §E.1
scope; reopens, re-derives, or re-argues no gate semantics and neither B1, B2, nor B3; consumes no
`XASSET-0027` §P.1 results PR; weakens no validator or test; creates no endpoint, bound, point, range,
percentage, weight, rank, target, or allocation; changes no `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no
chart, ladder, deployment, trade, order, or brokerage action; and rewrites no accepted history.

## Rationale

The narrow question was whether the renewed readiness verification could simply be performed, since it
mutates nothing — or, failing that, whether `XASSET-0038` already covers it.

**Neither holds, and both failures are textual rather than theoretical.**

Performing it without a grant would read **five** express withholdings as silence. `XASSET-0041` §I names
link 3 and withholds it; `XASSET-0043`, `XASSET-0046`, `XASSET-0048` §G and `XASSET-0049` each name the
renewed readiness verification and each decline to grant it — **five in total**, and the exact set is
`XASSET-0041`, `XASSET-0043`, `XASSET-0046`, `XASSET-0048`, `XASSET-0049`. `XASSET-0036` §B established the identical
point for §G.B as a whole and chose the same remedy: **file the narrow authority rather than infer it.**

Relying on `XASSET-0038` would fail twice over. Its grant was "exactly one" and that one ran to a
recorded `PASS`. And its anchor — a merge, an accepted head, ten paths, and two canonical pins — has
been superseded on every axis by the correction, the canonical amendment, and the boundary growth to
eighteen. Treating a spent, stale grant as live authority for current bytes is precisely the
moving-reference error the `XASSET-0044` → `XASSET-0047` recovery chain already cost this program two
pull requests to correct.

**Why the authority is drawn this narrowly.** This step's entire safety value is that it is the moment
when nothing is allowed to change. `XASSET-0030` §G.B's governing invariant — *no outcome-producing
executable code may be created, changed, or left outside the bound execution identity after the final
rebinding and before `ATTEMPT_1`* — is precisely what it exists to confirm. An authorization that let
the verifying unit repair what it found would defeat the step it authorizes: the bytes attested would
then be bytes no independent review had ever seen. Hence §F's flat bar on declaring a defect "fixed",
and §H's requirement that a defect force a stop plus a **separately authorized** correction and, where
invalidated, a redone rebinding — a sequence this program has now executed once in earnest.

**Why the checklist is closed.** A readiness gate whose conditions a future session may extend is not a
gate; it is a discretion. Closing the list at C1–C11 makes a `PASS` mean one determinate thing. It also
makes the gate falsifiable: a condition the unit thinks is missing surfaces as a reported finding,
where an independent reviewer can see it, instead of being quietly satisfied.

**Why C3 both records and derives — a deliberate, disclosed departure from `XASSET-0038` §G.** The
recorded witness is redundant to the derived expectation, and §G.1 fixes which one governs, makes
disagreement a stop condition, and pins the agreement by test. `XASSET-0038`'s objection was to a
*silent* second source of truth; a redundancy that is checked in CI and that halts the unit on
mismatch is not silent, and it converts an invisible risk into a detected failure. The five values are
also, independently, what a reviewer needs in order to check this filing's own preflight claims
without re-deriving them by hand. The safeguard rather than the omission is the stronger form.

**Why this does not reopen `XASSET-0029` §E.** §E terminates the *activation* regress: arming needs no
further merged governance PR. This decision adds **zero** activation authorizations and leaves arming
exactly where §E, `XASSET-0036` §D, `XASSET-0037` §G and `XASSET-0038` §D each put it — the external
one-shot runtime attestation and the operator's act. Verifying that already-bound bytes are unchanged
is not arming, and authorizing that verification is not an activation authorization.

## Alternatives Considered

| Alternative | Why not |
|---|---|
| Perform the renewed verification now as ordinary read-only work | **Five** accepted filings withhold it by name — `XASSET-0041`, `XASSET-0043`, `XASSET-0046`, `XASSET-0048`, `XASSET-0049`; performing it would read express withholdings as silence |
| Treat `XASSET-0038` as still authorizing it | Its "exactly one" grant is spent, and its anchor — merge, head, ten paths, two pins — is superseded on every axis |
| Amend or extend `XASSET-0038` | Would rewrite a closed, accepted filing whose own unit already ran; the repository's convention is a narrow successor, not retroactive edits |
| Authorize and perform the verification in this same filing | §J requires the authority to close its own lifecycle first; and a unit that authorized itself could not be independently reviewed *as* an authorization before being relied upon |
| Authorize links 3 and 4 together | Link 4 is the fail-closed **drift-handling** gate that sits between a readiness finding and arming; batching would let one review cover both the check and the response to its failure |
| Authorize links 3–5 as one activation pass | Directly contrary to `XASSET-0041` §I, and would collapse the attestation boundary `XASSET-0029` §E protects |
| Let the authorized unit repair defects it finds | Defeats the invariant the step exists to confirm; attested bytes would then be bytes no review had seen |
| Leave the checklist open-ended | An extensible readiness gate is a discretion, not a gate; a `PASS` would not mean one determinate thing |
| Require the unit to record its result by repository mutation | Unnecessary — the finding is evidence, not state — and it would put a read-only unit into the single mutation lane |
| Omit the five module hashes from C3, following `XASSET-0038` §G exactly | Loses an independently checkable witness a reviewer needs; §G.1's three rules remove the silent-disagreement risk that motivated the original omission |
| Restate the eighteen path hashes as constants | Eighteen constants is a maintenance surface with no reviewer benefit; C2's derive-from-tree mechanism is sufficient and is the mechanism the implementation already uses |
| Amend `XASSET-0030` §G.B | §G.B is adopted unchanged; nothing found requires re-sequencing it |

## Consequences

**Effective only on complete closure of the seven §J conditions.** Until then this decision changes
nothing operationally, and Stage 1 stays exactly as it is.

Once effective, **exactly one** read-only `XASSET-0041` §I link 3 / `XASSET-0030` §G.B step-9
execution-readiness verification becomes authorized, bounded by §§E–I and closed at the §G checklist.
**Links 4 and 5 remain unperformed and unauthorized, and each requires its own separate authority.**

**Explicitly unchanged by this filing:** the frozen 680 / 48 universe and its hash `73c0965e…5224`;
every construction identity, ordering, and cardinality; every gate's index, question, class,
controlling authority, and failure disposition; B1, B2, and B3; `XASSET-0030`'s 6/6 gate map and its
§E.1 triggers; `XASSET-0024` §K.1; `XASSET-0020` §E.1; `XASSET-0031`'s `G3`; the effective canonical
pins; all eighteen `LOAD_BEARING_RELPATHS` and their bytes; `REQUIRED_LIFECYCLE_GATES` as the existing
six-element tuple; `AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`, and `REVIEWED_BASE_SHA` as
`XASSET-0049` lawfully rebound them; `level1_stage1_runner.py`, `level1_stage1_result_validator.py`,
`level1_construction_universe_closure_validator.py`,
`level1_endpoint_evidence_preregistration_validator.py`, and
`level1_stage1_execution_authorization.py`; every `intelligence/` record; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`,
`levels.py`; `XASSET-0027` §P.1's reserved, unspent results PR; `XASSET-0038`'s closed filing and its
completed `PASS`; and every accepted decision's status and text.

**Merging this decision authorizes a future read-only verification only. It does not make Stage 1
armed or executable.**

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, and unconsumed. No
construction was evaluated, no gate result asserted, and no outcome produced.**
