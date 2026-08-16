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

### C. The attestation

`level1_stage1_execution_authorization.py` implements a JSON attestation held **outside the
repository** — so it can never be committed, reviewed into existence, forged into a pull request,
or produced by editing tracked files. It must bind, and is verified against live repository facts
rather than its own claims:

repository · study · authorizing decision `XASSET-0029` · predecessor `XASSET-0028` merge SHA ·
canonical protocol SHA-256 · canonical preregistration SHA-256 · construction-universe SHA-256 ·
construction count **680** · cell count **48** · `execution_attempt_id` · independent-review id,
formal disposition, and reviewed SHA · principal-acceptance id and accepted head · merge SHA and
**both** parents · post-merge verification id · merge-commit CI run, job, status, conclusion, and
head SHA.

Canonical pins and universe identity are **recomputed live** and compared against both the bound
constants and the recorded values, so drift in either direction is refused. The schema is closed
(unknown keys rejected), duplicate JSON keys are rejected, and the payload is validated **before**
any bytes reach disk so an invalid attestation cannot occupy the one-shot slot.

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

### G. One authorized lane, one shot

`XASSET-0027` §P.1 permits exactly one later Stage-1 evaluation/results PR. The attempt identity is
`ENDPOINT-0001::STAGE_1::ATTEMPT_1` — derived from repository truth, not invented: no Stage-1
attempt has ever been executed or authorized, so the one authorized lane is the first. The
attestation and its consumption receipt are each created with `O_EXCL`, so neither can be
regenerated nor replayed, and an authorization naming one attempt can never authorize another. A
rerun after consumption requires new governance authority. **`XASSET-0029` prepares that lane and
does not consume it.**

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
preregistration_sha256: 14d166f071e579bd958a7e4d0d34ac1f5cdef999f58aecd01d1276321bebdce6
predecessor_protocol_sha256: c02b4d519267b96ddb12500e6d1d55a47aeafd9437de8e41014c8871f631618c
predecessor_preregistration_sha256: ffde86c1585050b2bf89e58033f37777a903ace86e97be46b6440a217c78ec4a
-->

- `PROTOCOL_V1.md`: `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb`
- `pre_registration.yaml`: `14d166f071e579bd958a7e4d0d34ac1f5cdef999f58aecd01d1276321bebdce6`
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
