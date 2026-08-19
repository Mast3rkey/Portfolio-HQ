---
decision_id: XASSET-0038
date: 2026-08-19
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, XASSET-0037, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_readiness_verification_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `637eaa30302f5a71f84ab1d215ecbd32c01399b5` |
| Worktree / stash | clean; no stash; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #337 | merged and closed, `merged_by` `Mast3rkey` |
| PR #337 accepted head | `f40c816223c78f1d1e436b718455df5fb3d77fa7` |
| PR #337 merge parents, in order | `3e5de8f85c69c2e5dc2b75421446b5db996d7cf1`, then `f40c816223c78f1d1e436b718455df5fb3d77fa7` |
| PR #337 merge tree | `a370ecb9f24ecbc1f1f83f31042990f706ead20c` — **byte-identical to the accepted head's own tree**, so zero drift at merge |
| Independent review | [`4966846374`](https://github.com/Mast3rkey/Portfolio-HQ/pull/337#pullrequestreview-4966846374), `commit_id` `f40c816223c78f1d1e436b718455df5fb3d77fa7`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE** |
| Principal acceptance | [`#issuecomment-5335697214`](https://github.com/Mast3rkey/Portfolio-HQ/pull/337#issuecomment-5335697214), at that exact head |
| Post-merge verification | [`#issuecomment-5335849767`](https://github.com/Mast3rkey/Portfolio-HQ/pull/337#issuecomment-5335849767) |
| Merge-commit CI | run `32198881652`, job `95908324747`, `completed` / `success`, `head_sha` **`637eaa30302f5a71f84ab1d215ecbd32c01399b5`** — the exact merge SHA, not the PR head |
| `XASSET-0038` | **unused** — zero occurrences repository-wide before this filing |
| `LOAD_BEARING_RELPATHS` | **10**, every one hashing identically in the worktree and in the merged tree `637eaa30…` |
| V7 canonical pins | `PROTOCOL_V1.md` `367583b6…d8971`, `pre_registration.yaml` `768b013c…4bce1` — both matching their files exactly |
| Frozen universe | **680** constructions, **48** cells, aggregate `73c0965e…5224` |
| Construction-universe module | SHA-256 `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5` |
| Lane state | `ABSENT`; `AUTHORIZATION_ROOT`, claim, completion and ledger paths all absent |
| `new_execution_is_authorized()` | `False` |
| `ATTEMPT_1` | intact, unclaimed, unconsumed |

Regenerating the 680 / 48 / aggregate figures and reading the frozen universe is expressly
authorized read-only structural traversal under `XASSET-0036` §F.1(a), and consumes nothing:
**no gate was evaluated for any construction.**

### The question this unit answers

`XASSET-0037`'s complete seven-condition lifecycle closed, so `XASSET-0030` §G.B **step 8** — the one
successor operational-authorization / load-bearing rebinding — is done. §G.B step 9 is next:

> After rebinding, "runner execution-readiness" is **read-only verification of already-bound bytes**.
> It is **not** a phase in which outcome-producing executable code may still be created or changed.

**Step 9 has no authority.** `XASSET-0036` §F withholds "performing §G.B steps 8–11" absolutely.
`XASSET-0037` §I withholds "`XASSET-0030` §G.B steps 9, 10, or 11" by name, and its Consequences
repeat that steps 9, 10 and 11 "remain unperformed and unauthorized, and **each requires its own
separate authority**." `XASSET-0030` §G.B itself closes by stating it "authorizes none of G.A or
G.B."

This is the same shape of gap `XASSET-0036` §B found for §G.B as a whole: the step is *sequentially
reachable* and *not authorized*. **This decision closes it for step 9 and for nothing else.**

## Decision

### A. Determination — `STEP_9_READINESS_VERIFICATION_AUTHORIZED`

**Exactly one** future, separate, bounded `XASSET-0030` §G.B **step 9** unit is authorized: a
**strictly read-only execution-readiness verification of already-reviewed, already-bound bytes**,
anchored to the PR #337 merge `637eaa30302f5a71f84ab1d215ecbd32c01399b5` and its accepted head
`f40c816223c78f1d1e436b718455df5fb3d77fa7`.

**This decision performs no part of step 9.** It runs no readiness checklist and issues no step-9
`PASS` or `FAIL`. It authorizes and defines; a later unit verifies.

**Steps 10 and 11 are not authorized, here or by implication (§K).**

### B. The authority gap, reproduced from accepted text before anything was authorized

Each of the following was read at its live merged bytes, not recalled:

| Accepted text | What it says about step 9 |
|---|---|
| `XASSET-0030` §G.B step 9 | Defines step 9 as read-only verification of already-bound bytes, and expressly not a phase in which outcome-producing code may change |
| `XASSET-0030` §G.B closing | "**This decision authorizes none of G.A or G.B**, and performs no part of either." |
| `XASSET-0036` §F | Withholds "performing §G.B steps 8–11" |
| `XASSET-0037` §I | Withholds "`XASSET-0030` §G.B steps 9, 10, or 11" by name |
| `XASSET-0037` Consequences | "steps 9, 10, and 11 remain unperformed and unauthorized, and each requires its own separate authority" |

**Three filings named step 9 and three declined to grant it.** The gap is therefore established by
accepted repository text, not inferred from this unit's convenience.

**A read-only unit is not automatically self-authorizing here, and this decision does not rest on the
weaker claim that it might be.** Ordinary read-only audit is `OPS-0014` Class 0 work needing no
branch, commit, or authorization. Step 9 is different in exactly one respect that the accepted text
itself supplies: it is a **named step inside a gated activation sequence**, sitting between the
rebinding it verifies and the fail-closed drift gate and attestation that follow it. A step-9 finding
is the immediate predicate of §G.B steps 10 and 11. `XASSET-0037` §I and its Consequences settle the
question directly by withholding step 9 by name and requiring separate authority for it; that is the
ground this decision stands on.

### C. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

§P.1's exactly-one Stage-1 **evaluation/results** PR is **not consumed, replaced, amended, or counted
against**, on the grounds `XASSET-0036` §C and `XASSET-0037` §H both already recorded and which apply
here more strongly, not less:

- §P.1's PR delivers a **results document**; the step-9 unit produces **no result of any kind**, and
  §F bars it from producing one.
- §P.1's PR sits **after arming**; step 9 sits **before** it.
- §P.1's PR "may make no production configuration change"; the step-9 unit makes **no repository
  change at all**, production or otherwise.

After this decision merges, §P.1's budget is exactly what it is today: **one, unspent.**

### D. Relation to `XASSET-0029` §E — this is not an activation PR, and it adds zero activation authorizations

`XASSET-0029` §E terminates the activation regress on a step that **changes no repository state** —
the runtime attestation — and states that "no additional authorization PR is ever required" for
arming.

**Nothing here reopens that.** This decision:

- generates **no** attestation and authorizes none;
- creates **no** `AUTHORIZATION_ROOT`, `READY`, `CLAIMED` or `COMPLETED` lane state, and authorizes none;
- adds **zero** activation authorizations;
- leaves `stage_1_executability.executable` permanently `false` with its enforced-false check intact.

**No committed value in this repository authorizes Stage-1 execution**, and **merging this decision
authorizes a future read-only verification only — it does not make Stage 1 armed or executable.**

The final activation remains what `XASSET-0029` §E, `XASSET-0036` §D and `XASSET-0037` §G each
already require: **the external one-shot runtime attestation and the operator's act — not a merged
activation PR.** Step 9 is neither that attestation nor arming; it is the verification that the bytes
an attestation would authenticate are still exactly the bytes that were bound.

### E. Authority granted — exactly one future, separate, read-only step-9 unit

The future step-9 unit **may**, and only in service of `XASSET-0030` §G.B step 9:

1. **Re-verify** the exact Git and GitHub identities of the PR #337 lifecycle and its merge, from live
   sources, treating them as authoritative over any inherited summary.
2. **Re-verify** that every one of the **10** `LOAD_BEARING_RELPATHS` matches the effective bound
   merge exactly, with expected identity **derived from the merged git tree at verification time**,
   never from a constant restated in a decision record — the mechanism the accepted implementation
   already uses and this decision does not alter.
3. **Re-verify** the V7 canonical pins, the frozen universe, and the identities enumerated in §G.
4. **Run** the repository's validators and its non-executing ENDPOINT CLI checks.
5. **Confirm** the runner remains fail-closed while no attestation exists, that lane state remains
   `ABSENT`, and that `new_execution_is_authorized()` remains `False`.
6. **Read and structurally traverse** the real frozen construction universe, read-only, under
   `XASSET-0036` §F.1(a)'s existing permission — which this decision reuses **by reference and does
   not widen by one step**, and which remains conditional on the operation staying read-only and
   non-outcome-producing.
7. **Record** its determination as durable, externally posted step-9 evidence (§I).

Every one of these is verification of state that already exists. **None creates, edits, regenerates,
or corrects anything.**

### F. Authority withheld — absolute

The step-9 unit **must not**:

- create, edit, regenerate, correct, reformat, or re-pin **any** canonical, validator, authorization,
  runner, result-production, universe, governance, or protected portfolio byte;
- **declare any defect "fixed"** during readiness verification, or repair one in passing — a defect
  found is a finding to report and a stop condition (§H), never work to perform;
- extend, reduce, or re-derive `LOAD_BEARING_RELPATHS`, or re-pin any canonical hash;
- produce an attestation, an `AUTHORIZATION_ROOT`, lane state, a claim, a ledger entry, a completion
  record, a recovery, or an execution;
- create `stage1_results.yaml`, or any real per-construction disposition, cell outcome, or roll-up;
- **evaluate or decide any gate (`G1`–`G12`) for any registered construction**, or consume any part of
  `ATTEMPT_1`;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result;
- acquire market, fundamental, economic, or Stage-2 data, or perform any Stage 2 work;
- reopen, re-derive, or re-argue B1, B2, or B3, any gate semantics, `XASSET-0030`'s 6/6 gate map,
  `XASSET-0024` §K.1, or `XASSET-0020` §E.1;
- change any construction identity, universe membership, ordering, cardinality, or universe hash;
- consume `XASSET-0027` §P.1's reserved results PR;
- change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- **perform or authorize `XASSET-0030` §G.B step 10 or step 11.**

#### F.1 — Read-only means read-only

`XASSET-0036` §F.1 drew the line that protects the one-shot lane: **traversing frozen construction
identities is not execution; applying gate-evaluation semantics to them to derive Stage-1 outcomes
is.** That line is adopted here unchanged, and step 9 sits further inside it than the implementation
PR did — the implementation was permitted to *write* the code it validated, and step 9 is permitted
to write nothing at all.

**An actual Stage-1 run over the real 680 remains absolutely prohibited** and stays downstream of
attestation → `READY` → lawful claim → execution, exactly as §G.B steps 10–11 require.

### G. The closed step-9 readiness checklist

**Closed**: the future unit verifies these and adds no further condition of its own invention; a
condition it believes is missing is a finding to report, not a checklist item to add.

| # | Condition | Grounded in |
|---|---|---|
| **C1** | Exact Git/GitHub identities — merge SHA, ordered merge parents, accepted head, merge-tree identity, approving review at the exact accepted head, principal acceptance, post-merge verification — with **zero post-review and post-merge drift** | `XASSET-0037` §J; `OPS-0009` §6 |
| **C2** | All **10** `LOAD_BEARING_RELPATHS` match the effective bound merge exactly, identity derived from the merged tree at verification time | `XASSET-0030` §G.B step 5; `XASSET-0037` §§D–E |
| **C3** | Exact identity of the **runner**, the **result validator**, the **preregistration derivation module**, the **construction-universe module**, and the **execution-authorization module** — the five Python modules inside C2's ten paths, each named individually because each is independently capable of affecting the 680 outcomes | `XASSET-0030` §G.B steps 4–5; `XASSET-0037` §D.1 |
| **C4** | V7 canonical pins unchanged — `PROTOCOL_V1.md` `367583b6…d8971`, `pre_registration.yaml` `768b013c…4bce1` | `XASSET-0037` §F |
| **C5** | Frozen universe exactly **680** constructions, **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` | `XASSET-0028`; `XASSET-0036` §F.1(a) |
| **C6** | Construction-universe module SHA-256 `1fed8f42b8c80ad2908a135a0c02517463dd04bb4ee3fdb20cad9d5a9acf95c5` | `XASSET-0037` eighth correction, MAJOR 1 |
| **C7** | All required repository validators pass, and all ENDPOINT CLI checks exit clean **without executing Stage 1** | `XASSET-0036` §E.8 |
| **C8** | The runner remains **fail-closed while no attestation exists** | `XASSET-0029` §§B, D; `XASSET-0030` §G.B step 10 |
| **C9** | Lane state remains `ABSENT` and `new_execution_is_authorized()` remains `False` | `XASSET-0029` §B; `XASSET-0037` Consequences |
| **C10** | **No output and no persistent execution artifact is created** by the verification — no `stage1_results.yaml`, no lane directory, no attestation, no ledger entry | §F; `XASSET-0036` §F.1(b) |
| **C11** | Durable, externally posted step-9 evidence recording the determination, **without a repository mutation** | §I |

**C4, C5 and C6 are the only constants this decision restates**, because accepted authority already
fixes each as an exact value. Everything else in C2 and C3 is derived from the merged tree at
verification time, so this record can never become a stale second source of truth for an identity.

### H. Fail-closed

**Any** drift, missing identity, validation failure, unexpected lane state, or state the unit cannot
determine with certainty **stops the step-9 unit**. On any such condition the unit must:

1. **stop** — not continue to the remaining checklist items as though the condition were minor;
2. **report** the exact condition in its externally posted evidence;
3. **change nothing** — the prohibition in §F is not relaxed by the discovery of a defect;
4. **not** issue a step-9 `PASS`.

**A defect found at step 9 requires a separately authorized correction**, and — because the corrected
bytes would no longer be the bytes the rebinding bound — **any rebinding invalidated by that
correction must itself be redone under its own separate authority**, exactly as `XASSET-0030` §G.B
step 5's own reasoning requires and as §D there already records for enforcement drift.

**Uncertainty is failure.** The unit may not resolve an ambiguous state in favour of readiness.

### I. Packaging and evidence

The step-9 unit is **one** read-only unit. It creates **no branch, no commit, and no pull request**,
and makes **no repository mutation** — so it does not contend for the `OPS-0014` §D single mutation
lane and may run in a clean isolated clone.

Its determination is recorded as **durable, externally posted evidence** — a GitHub comment on the
`ENDPOINT-0001` record of proceedings — stating the verified identities, each checklist condition's
outcome, and an explicit statement of what remains unauthorized. **A repository mutation to record
the result is neither required nor authorized**; if a future session concludes one is genuinely
necessary, that is a finding to report under §H, not scope to assume.

### J. Effectivity — the step-9 unit may not begin before this lifecycle closes

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

### K. Steps 10 and 11 retain their own separate-authority requirement

Stated unambiguously, because the whole risk of an authorization filing is that a successor reads
more out of it than it contains:

- **Step 9 remains unperformed** until this decision's complete §J lifecycle closes, and is then
  performed only as §§E–I define it.
- **Step 10** — fail-closed handling of post-rebinding drift in runner / result-production bytes
  before `READY` or claim — **retains its own separate-authority requirement** and is not authorized
  here. §H's stop-and-report rule is what the step-9 unit does *for itself*; it is not a grant of
  step 10.
- **Step 11** — the external one-shot attestation, arming, the claim, and the 680-construction run —
  **retains its own separate-authority requirement** and is **entirely outside this filing**.
- A step-9 `PASS`, however clean, **authorizes nothing further.** It is evidence that the bound bytes
  are unchanged; it is not permission to arm, to claim, or to execute.
- `XASSET-0027` §P.1's reserved evaluation/results PR **remains unspent** (§C).

### L. Absolute non-authorization

This decision generates no attestation; creates no `AUTHORIZATION_ROOT` and no `READY`, `CLAIMED`, or
`COMPLETED` lane state or ledger entry; arms, claims, completes, executes, or recovers no Stage-1
execution; performs no part of §G.B step 9 and no part of steps 10 or 11; evaluates no gate for any
registered construction and asserts no per-construction outcome; creates no `stage1_results.yaml` and
no runner, result validator, or other outcome-producing code; changes no `LOAD_BEARING_RELPATHS`, no
canonical file, and no hash pin; changes no construction identity, universe membership, ordering,
cardinality, or universe hash; consumes nothing of `ATTEMPT_1`; acquires no market, fundamental,
economic, or Stage-2 data and performs no Stage 2 work; reads, lists, opens, or references no
`risk_lane_boundary` protected `RISK` result; resolves `XASSET-0024` §K.1 neither way and amends no
`XASSET-0020` §E.1 scope; reopens, re-derives, or re-argues no gate semantics and neither B1, B2, nor
B3; consumes no `XASSET-0027` §P.1 results PR; weakens no validator or test; creates no endpoint,
bound, point, range, percentage, weight, rank, target, or allocation; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin
state; authorizes no chart, ladder, deployment, trade, order, or brokerage action; and rewrites no
accepted history.

## Rationale

The narrow question was whether §G.B step 9 could simply be performed, since it mutates nothing.

It cannot, and the reason is textual rather than theoretical. `XASSET-0037` §I withholds step 9 **by
name**, and its Consequences state that each of steps 9, 10 and 11 "requires its own separate
authority." A session that performed step 9 without a grant would be reading an express withholding
as silence. `XASSET-0036` §B established the identical point for §G.B as a whole and chose the same
remedy: file the narrow authority rather than infer it.

**Why the authority is drawn this narrowly.** Step 9's entire safety value is that it is the moment
when nothing is allowed to change. `XASSET-0030` §G.B's governing invariant — *no outcome-producing
executable code may be created, changed, or left outside the bound execution identity after the final
rebinding and before `ATTEMPT_1`* — is precisely what step 9 exists to confirm. An authorization that
let the verifying unit repair what it found would defeat the step it authorizes: the bytes attested
would then be bytes no independent review had ever seen. Hence §F's flat bar on declaring a defect
"fixed", and §H's requirement that a defect force a stop plus a **separately authorized** correction
and, where invalidated, a redone rebinding.

**Why the checklist is closed.** A readiness gate whose conditions a future session may extend is not
a gate; it is a discretion. Closing the list at C1–C11 makes a step-9 `PASS` mean one determinate
thing. It also makes the gate falsifiable: a condition the unit thinks is missing surfaces as a
reported finding, where an independent reviewer can see it, instead of being quietly satisfied.

**Why C2 and C3 derive identity from the merged tree rather than restating hashes.** The accepted
implementation deliberately derives expected identity from the merged git tree at validation time,
"never from a hard-coded constant." Restating those five module hashes here would create a second
source of truth that could silently disagree with the first. Only the three values accepted authority
already fixes as exact constants — the canonical pins, the universe figures, and the
construction-universe module hash — are restated, and each is restated because it is already fixed.

**Why this does not reopen `XASSET-0029` §E.** §E terminates the *activation* regress: arming needs
no further merged governance PR. This decision adds **zero** activation authorizations and leaves
arming exactly where §E, `XASSET-0036` §D and `XASSET-0037` §G each put it — the external one-shot
runtime attestation and the operator's act. Verifying that already-bound bytes are unchanged is not
arming, and authorizing that verification is not an activation authorization.

## Alternatives Considered

| Alternative | Why not |
|---|---|
| Perform step 9 now as ordinary read-only work | `XASSET-0037` §I withholds step 9 by name and its Consequences require separate authority; performing it would read an express withholding as silence |
| Authorize and perform step 9 in this same filing | The instruction and §J both require the authority to close its own lifecycle first; and a unit that authorized itself could not be independently reviewed *as* an authorization before being relied upon |
| Authorize steps 9 and 10 together | Step 10 is the fail-closed **drift-handling** gate that sits between a readiness finding and arming; batching it would let one review cover both the check and the response to its failure |
| Authorize steps 9–11 as one activation pass | Directly contrary to `XASSET-0037` Consequences, and would collapse the attestation boundary `XASSET-0029` §E protects |
| Let the step-9 unit repair defects it finds | Defeats the invariant step 9 exists to confirm; attested bytes would then be bytes no review had seen |
| Leave the checklist open-ended | An extensible readiness gate is a discretion, not a gate; a `PASS` would not mean one determinate thing |
| Require the step-9 unit to record its result by repository mutation | Unnecessary — the finding is evidence, not state — and it would put a read-only unit into the single mutation lane |
| Restate the five module hashes as constants here | Creates a second source of truth that can silently disagree with the merged tree the implementation actually derives from |
| Amend `XASSET-0030` §G.B | §G.B is adopted unchanged; nothing found requires re-sequencing it |

## Consequences

**Effective only on complete closure of the seven §J conditions.** Until then this decision changes
nothing operationally, and Stage 1 stays exactly as it is.

Once effective, **exactly one** read-only `XASSET-0030` §G.B step-9 execution-readiness verification
becomes authorized, bounded by §§E–I and closed at the §G checklist. **Steps 10 and 11 remain
unperformed and unauthorized, and each requires its own separate authority.**

**Explicitly unchanged by this filing:** the frozen 680 / 48 universe and its hash `73c0965e…5224`;
every construction identity, ordering, and cardinality; every gate's index, question, class,
controlling authority, and failure disposition; B1, B2, and B3; `XASSET-0030`'s 6/6 gate map and its
§E.1 triggers; `XASSET-0024` §K.1; `XASSET-0020` §E.1; `XASSET-0031`'s `G3`; the V7 canonical pins;
all ten `LOAD_BEARING_RELPATHS` and their bytes; `level1_stage1_runner.py`,
`level1_stage1_result_validator.py`, `level1_construction_universe_closure_validator.py`,
`level1_endpoint_evidence_preregistration_validator.py`, and
`level1_stage1_execution_authorization.py`; every `intelligence/` record; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`,
`levels.py`; `XASSET-0027` §P.1's reserved, unspent results PR; and every accepted decision's status
and text.

**Merging this decision authorizes a future read-only verification only. It does not make Stage 1
armed or executable.**

**Stage 1 remains UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, and unconsumed. No
construction was evaluated, no gate result asserted, and no outcome produced.**
