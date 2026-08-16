---
decision_id: XASSET-0029
date: 2026-08-16
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, LEVEL2-0001, RISK-0001]
supporting_artifact: level1_stage1_execution_authorization.py
---

## Context

### Live preflight

Verified independently before any mutation, against live GitHub and git state rather than
inherited narrative:

| Fact | Verified |
|---|---|
| `origin/main` = local `HEAD` | `c51e94609eff7ede2bdfa084844d59b8347561e5` |
| Working tree / stash | clean / empty |
| Open PRs | zero |
| Competing mutation worktrees | none (sole worktree) |
| PR #327 | merged, `merged_by` `Mast3rkey`, 4 commits, 11 files |
| Accepted head | `036606401ea569b0a03f2d716d87a057d07d71dc` |
| Merge parents | `e4b6f0b810884fcb73d1b8ee053d8005db532f3e`, `036606401ea569b0a03f2d716d87a057d07d71dc` |
| Final review `4946202326` | `APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE`, `commit_id` = accepted head |
| Principal acceptance `5307509913` | present, exact head |
| Post-merge verification `5307545846` | present |
| Merge-commit CI run `31948052529` / job `95167105752` | `completed` / `success`, `head_sha` = merge SHA |
| Construction universe | regenerated live: **680** constructions, **48** cells, `73c0965e…5224` |
| `XASSET-0029` | unused — zero matches repository-wide |

**`XASSET-0028`'s lifecycle is therefore closed in full.** Its blocking prerequisite —
`XASSET_0028_LIFECYCLE_CLOSURE` — is spent.

### The question this unit had to answer

`XASSET-0027` §P.1's two prerequisites are now both satisfied, so exactly one later Stage-1
evaluation/results PR is permitted. But the software gate remains fail-closed, and the canonical
file still reads `STRUCTURALLY_CLOSED_NOT_OPERATIONALLY_AUTHORIZED`. The question was how Stage 1
may lawfully become executable **without** opening a merge-to-execution gap, letting a results
document self-authorize, trusting a mutable boolean, weakening the public validator, executing
anything here, or creating a circular or self-certifying authorization.

### Why "flip `executable: true`" is not the answer

The obvious move fails on three independent grounds, the third dispositive and discovered by
reading the code rather than assuming it:

1. **Merge-to-execution gap.** A committed flag is effective the instant its PR merges — before
   post-merge verification, and before merge-commit CI has started, let alone concluded. The
   canonical file already promises `no_merge_to_execution_gap: true`, so a committed flag cannot be
   the mechanism without contradicting the file it lives in.

2. **A mutable boolean is not evidence.** A flag *asserts* authorization. It demonstrates that no
   gate actually closed, and is bound to no review, acceptance, merge, CI conclusion, or hash.

3. **It is already a validation error.** `_validate_stage_1_executability` enforces
   `_false(block.get("executable"))`, while `stage_1_operational_authorization_is_effective()`
   required `executable is True`. Those are mutually exclusive: **the canonical preregistration
   could never be simultaneously valid and authorizing.** The flip was never actually available.
   `XASSET-0029` preserves that lock rather than unpicking it.

## Decision

### A. `executable` stays false permanently

`stage_1_executability.executable` remains `false` and keeps its enforced-false check. Its meaning
is now explicit and load-bearing: **no committed value in this repository authorizes Stage-1
execution.** A new enforced-true sibling, `executable_is_never_the_authorization_source`, states
this so a future reader cannot mistake the flag for a switch.

### B. Authorization is two-factor

| Factor | Location | Says | Can it authorize alone? |
|---|---|---|---|
| Structural arming | `stage_1_operational_authorization` (committed, inert) | **what** a valid authorization must prove | No |
| Preexecution attestation | outside the repository (runtime, one-shot) | whether **this** execution is authorized | No |

The committed block *specifies a gate*; it never opens one. It is validated to keep saying
`currently_effective: false`, `authorization_is_committed_state: false`, and
`authorization_is_external_runtime_evidence: true`, and to retain every fail-closed condition.

### C. The attestation is authenticated, not merely well-formed

`level1_stage1_execution_authorization.py` implements a JSON attestation held **outside the
repository** — so it can never be committed, reviewed into existence, forged into a pull request,
or produced by editing tracked files.

**Supplying the attestation proves nothing.** Every lifecycle fact it records is re-derived from a
durable source on every validation and compared; a recorded value is never accepted because its
text is well-formed, and an unreachable source **fails closed**:

| Source | Supplies |
|---|---|
| **Local git object store** | merge SHA, both real parents, current ancestry, predecessor `XASSET-0028` identity, and the byte identity of load-bearing files **as they exist in the merged tree** |
| **GitHub governance metadata** | the review and its exact reviewed commit and formal disposition, the **reviewer login (derived, never self-declared)**, the principal acceptance comment, the post-merge verification comment, and the merge-commit CI run and job including their pairing |

The GitHub source is **governance metadata only**. It never fetches market, price, fundamental, or
any other economic data, and it is not — and must not become — a Stage-1 data-acquisition path.

Bound and mechanically verified: repository · study · authorizing decision · **authorizing pull
request** · `execution_attempt_id` · authorization head · **predecessor `XASSET-0028` merge SHA,
accepted head, and merge base** · canonical protocol and preregistration SHA-256 ·
construction-universe SHA-256 · count **680** · cells **48** · **load-bearing enforcement-code
identity** · **current git ancestry**. The schema is closed, duplicate JSON keys are rejected, and
the payload is validated before any bytes reach disk so an invalid attestation cannot occupy the
one-shot slot.

### D. No merge-to-execution gap

Merging `XASSET-0029` authorizes nothing: no attestation exists, and
`authorization_is_effective()` returns `False`. The attestation cannot be pre-staged, because
generating it requires evidence that does not exist until after the merge — the merge SHA, a
post-merge verification record, and a merge-commit CI run that has **concluded** success at that
exact merge SHA. CI cannot have concluded at the instant of merge. The interval between merge and
authorizability is therefore **strictly positive and enforced by evidence, not by convention**.

### E. No infinite authorization regress

Arming is a **runtime operator act**, not a further merged governance PR. `XASSET-0029` is the
final governance decision required for Stage 1; the generator is then run once, and no additional
authorization PR is ever required. The regress terminates because the final step changes no
repository state.

### F. Trust boundary

- Repository state says **what is structurally authorized**.
- The external attestation says **whether this execution is authorized**.
- A results document satisfies **neither** and is never consulted for authorization: the public
  `validate_stage1_results()` still takes no universe parameter and still checks authorization
  first.
- Private `_at`-suffixed seams exist so structural tests run without any call form implying
  authorization. **Calling them confers nothing.**

### G. One authorized lane, authenticated provenance, and an exact result binding

`XASSET-0027` §P.1 permits exactly one later Stage-1 evaluation/results PR. The attempt identity is
`ENDPOINT-0001::STAGE_1::ATTEMPT_1` — derived from repository truth, not invented.

```
ABSENT ──▶ READY ──▶ CLAIMED ──▶ COMPLETED
```

| Question | Predicate | True in |
|---|---|---|
| May a **new** execution start? | `new_execution_is_authorized()` | `READY` only |
| Did **this** execution come from the one lawful claim? | `claimed_execution_is_authorized()` | `CLAIMED`, `COMPLETED` |
| Is **this exact artifact** the one it completed? | `completed_result_is_authorized(results)` | `COMPLETED`, matching identity |

**State detection and authorization validity are different questions.** A surviving claim record
may establish that the lane *is* `CLAIMED`; it never establishes that the claim is **lawful**. Lawful
provenance additionally requires that the exact attestation still exists, still hashes to what the
claim bound, and **still validates against durable git and GitHub truth** — so canonical,
load-bearing, ancestry, or governance drift *after* the claim fails closed rather than being
grandfathered in.

**Exactly one result identity.** `stage1_result_identity()` — SHA-256 of canonical JSON — is shared
by the future Stage-1 result writer, the completion record, and the public gate. Completing result A
therefore mechanically prevents publishing result B. Structural checking of a candidate result
before completion uses the private precompletion seam and never weakens the final public boundary.

The claim is taken **atomically immediately before the first real work**, with `O_EXCL` plus an
append-only ledger. Completion binds the attempt, the exact attestation, the exact claim identity,
and the exact result identity — recovered deterministically from the ledger if the claim file is
lost, or **failing closed**, never emitting a null binding.

**Durability boundary, stated rather than overclaimed.** `O_EXCL` prevents a second creation only
while the path exists. The claim is recorded in **two** places and **either** establishes `CLAIMED`;
destroying the whole directory also destroys the attestation, so the lane becomes `ABSENT`, which is
**not** `READY`; a crash after claiming leaves the lane `CLAIMED`, with recovery a governed act. A
privileged operator deleting the entire directory is outside any filesystem-based enforcement
boundary — disclosed, not papered over.

**`XASSET-0029` prepares that lane and does not claim, complete, or consume it.**

### H. Canonical amendment

`PROTOCOL_V1.md` and `pre_registration.yaml` are amended in lockstep, `V4` → `V5`. `XASSET-0028`'s
pins are retained as predecessor identity and its pin check is demoted to history-only — exactly
the treatment `XASSET-0028` itself gave `XASSET-0027`'s pins. Accepted history is never rewritten.
The protocol mirror gains `stage_1_authorization_mechanism` and `stage_1_execution_attempt_id` so
the two canonical files cannot drift on the new fact.

**The construction universe is untouched**: `73c0965e…5224`, 680 constructions, 48 cells — all
independently regenerated after the amendment and unchanged.

<!-- XASSET-0029-HASH-PINS-V1
protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md
protocol_sha256: 6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb
preregistration_path: research/level1_endpoint_evidence/pre_registration.yaml
preregistration_sha256: dbebe44f4f7e6f487b6d3d01b5c4de19670f14073919ee1578ed878db59c100d
predecessor_protocol_sha256: c02b4d519267b96ddb12500e6d1d55a47aeafd9437de8e41014c8871f631618c
predecessor_preregistration_sha256: ffde86c1585050b2bf89e58033f37777a903ace86e97be46b6440a217c78ec4a
-->

- `PROTOCOL_V1.md`: `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb`
- `pre_registration.yaml`: `dbebe44f4f7e6f487b6d3d01b5c4de19670f14073919ee1578ed878db59c100d`
- Predecessor (`XASSET-0028`, retained): `c02b4d51…f631618c` / `ffde86c1…6b440a217c78ec4a`

## Rationale

The design borrows only **neutral engineering patterns** already proven in this repository —
canonical JSON hashing, duplicate-key rejection, immutable preexecution metadata, exact-identity
verification, `O_EXCL` one-shot creation, fail-closed validation. **No `RISK-0001` scenario,
threshold, magnitude, window, parameter, attempt identity, result value, or family conclusion is
read, imported, or reused**, and `/private/tmp/phq-risk0001-results` is not accessed.

The alternative of a second merged "activation" PR was rejected: it regresses infinitely (every
activation needs its own activation) and still lands the flag at merge instant, so it fixes
neither problem. The alternative of a committed attestation was rejected because a committed file
can be authored inside the very PR that claims it, which is self-certification.

## Consequences

Stage 1 is **still not executable** after this PR merges, and remains so until the attestation is
generated post-lifecycle. `XASSET-0029` **executes no Stage 1**, evaluates no gate, produces no
`stage1_results.yaml`, acquires no data, and consumes no execution lane.

`XASSET-0024` §K.1 remains **unresolved** with both readings preserved. §J.12 remains **deferred**.
Representation remains `SOURCE_DEPENDENT_NO_PRIOR_RULE_REQUIRED`. **Stage 2 remains unauthorized**
and application authority remains **WITHHELD**. No endpoint, bound, point, range, percentage,
weight, target, or allocation is produced, and no sleeve is selected, preferred, ranked, sequenced,
or budgeted. No `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `margin_state.py`, or `levels.py` change. No trade or order is authorized. No
dashboard, chart, ladder, or margin work is performed.

---

## Bounded correction — independent FULL review `4946327932`

The first candidate (`c1f5554`) returned **CHANGES REQUIRED**: 2 BLOCKING / 2 MAJOR / 2 MINOR /
1 NOTE. Both BLOCKING defects were **reproduced before any correction**, and the review was right
on every count.

**BLOCKING 1 — the attestation did not verify the lifecycle it claimed to attest.**
`build_authorization_payload()` accepted the head, the entire `lifecycle_evidence` block, the
author identity, and the timestamp from its caller, and validation checked only internal
consistency. An entirely fictional review/acceptance/merge/CI chain validated `True`; the previous
suite's own happy path proved exactly that. Corrected by re-deriving every lifecycle fact from the
local git object store and GitHub governance metadata on every validation, as §C now describes.
Truth sources are injectable, so tests never touch live GitHub, and a dedicated regression test
asserts the previous synthetic fiction now **fails**.

**BLOCKING 2 — the one-shot state machine contradicted the public result validator.**
`consume_authorization()` made `authorization_is_effective()` return `False`, and
`validate_stage1_results()` gated on that same predicate — so a safe pre-execution consumption made
the resulting legitimate result unvalidatable, while deferring consumption left a replay and
concurrency window. Corrected with the explicit `ABSENT → READY → CLAIMED → COMPLETED` machine and
two separate predicates, as §G now describes.

**MAJOR 1 — the contract promised bindings the implementation did not make.**
`must_bind_exactly` named `PREDECESSOR_XASSET_0028_MERGE_SHA` while `PREDECESSOR_MERGE_SHA`,
`PREDECESSOR_ACCEPTED_HEAD`, and `PREDECESSOR_MERGE_BASE` went unused. They are now verified from
git, alongside the authorizing pull request, current ancestry, and load-bearing enforcement-code
identity **derived from the merged tree** rather than a circular hard-coded self-hash. Nothing is
claimed as bound unless the validator proves it.

**MAJOR 2 — canonical V5 carried two competing current states.** Three `lifecycle_effectivity`
fields still named the spent `XASSET-0028` condition. Corrected **in place** rather than by
manufacturing a V6, since V5 is still only a proposed candidate: the single current condition is
the `XASSET-0029` lifecycle plus an authenticated external attestation plus a one-shot claim, with
`XASSET-0027` and `XASSET-0028` surviving only in explicitly predecessor-named fields.

**MINOR 1** — the large `CLAUDE.md` runtime narrative is replaced by one concise pointer to this
decision and the canonical files. **MINOR 2** — `operations/WORKSTREAMS.yaml` now records PR #328.

No test was weakened. The construction universe is unchanged (`73c0965e…5224`, 680, 48). Stage 1
remains **NOT EXECUTED** and **NOT EXECUTABLE**: no attestation, claim, completion, or ledger record
exists. Because the correction changes lifecycle-truth authentication and the execution state
machine, the corrected head requires a **NEW independent FULL exact-head review, not a DELTA**.

---

## Second bounded correction — independent FULL review `4946397399`

The corrected candidate (`674f95c`) returned **CHANGES REQUIRED**: 2 BLOCKING / 2 MAJOR / 2 MINOR /
1 NOTE. Both BLOCKING defects were **reproduced before any correction**.

**BLOCKING 1 — `CLAIMED`/`COMPLETED` bypassed the authenticated attestation.** `lane_state_at()`
recognised claim/ledger state *before* loading `authorization.json`, and
`claimed_execution_is_authorized()` then accepted any syntactically valid 64-hex hash — skipping the
comparison entirely when the attestation was absent. **A local `claim.json` carrying the registered
attempt id was enough to make the public result gate return authorized with no attestation at all,
and no review, acceptance, merge, or CI ever consulted.** Corrected: a claimed lane must re-prove
that the exact attestation exists, hashes to what the claim bound, and still validates against
durable truth. State detection may still report `CLAIMED`; lawful provenance never follows from it.

**BLOCKING 2 — nothing bound "this result".** `complete_execution()` recorded a
`result_identity_sha256` that no predicate ever read, and `validate_stage1_results()` computed no
identity for the document handed to it, so completing result A did not prevent publishing result B.
Separately, completing after a claim-file loss emitted `authorization_sha256=None` and
`claim_sha256=None`, violating the canonical `completion_binds` contract. Corrected with one
deterministic `stage1_result_identity()`, a public gate that compares the supplied artifact against
the completion record, and deterministic claim-identity recovery from the append-only ledger — or
failing closed, never a null binding.

**MAJOR 1 — the independence claim now matches what can be observed.** The canonical contract
required `SELF_AUTHORED_REVIEW_WHERE_INDEPENDENCE_IS_REQUIRED` to fail closed, but this repository
uses **one GitHub account for both roles**, so login inequality cannot observe session
independence. Rather than leave an unenforced promise or fake a check, that condition is **removed**
and replaced with one the machine genuinely proves: the principal's own durable acceptance must
**name the exact independent review pass** it relies upon. Verification now also requires the
review, acceptance, and post-merge record to **belong to PR #328**, the review to be non-dismissed,
and the chronology review → acceptance → merge → post-merge verification to hold. `author_identity`
is explicitly reclassified as **non-authorizing informational metadata**.

**MAJOR 2 — exact reviewed base and zero merge drift.** Only the second merge parent was bound, and
the merged tree became its own load-bearing reference — so base drift or a merge resolution could
silently become the authorized implementation. Corrected: parents must be exactly
`[c51e9460…, accepted_head]`, the merge tree must equal the accepted-head tree, and every
load-bearing blob must match at **both** the reviewed head and the merge.

**MINOR 1** — the public validator's docstring described the spent `XASSET-0028` lifecycle; it now
describes `XASSET-0029`, with `XASSET-0028` as predecessor history. **MINOR 2** — the public
boundary is now tested through the **real** `validate_stage1_results()`, including result
substitution.

Canonical V5 is corrected **in place**, not replaced by a V6. No test was weakened. The universe is
unchanged (`73c0965e…5224`, 680, 48). Stage 1 remains **NOT EXECUTED** and **NOT EXECUTABLE**: no
attestation, claim, completion, or ledger record exists. Because the correction changes the public
claimed/completed provenance path and exact result binding, the corrected head requires **another
NEW independent FULL exact-head review, not a DELTA**.
