---
decision_id: XASSET-0042
date: 2026-08-19
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_pr337_lifecycle_actor_evidence_correction.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as
authoritative over every fact supplied to this session. Every value was independently
re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `9c8647f9dddacdf63825f569097214ba65299fe8` |
| Worktree / worktrees | clean; exactly one; no competing mutation lane |
| Open pull requests | **zero** |
| PR #341 | merged and closed, `merged_by` `Mast3rkey`, merge commit `9c8647f9…`, 8 files, 2 commits |
| PR #341 merge parents | exactly two, in order: `f212cce50e28ae887dc8c594bf8ae491a3ef85af`, then `0449d08217b5c0e422721ff3ef76b4241fb8a95a` |
| PR #341 merge drift | **zero** — merge tree `4ebd65c58fc7486294947cdec80f0a8725c6e20e` byte-identical to the accepted head's tree |
| Independent review | [`4974291044`](https://github.com/Mast3rkey/Portfolio-HQ/pull/341#pullrequestreview-4974291044) — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0/1 NOTE, at the exact accepted head |
| Principal acceptance + §G ratification | [`5345229177`](https://github.com/Mast3rkey/Portfolio-HQ/pull/341#issuecomment-5345229177) — durable `user.login` **`Mast3rkey`**, `type: User` |
| Post-merge verification | [`5345270602`](https://github.com/Mast3rkey/Portfolio-HQ/pull/341#issuecomment-5345270602) — durable `user.login` **`Mast3rkey`** |
| Final closure | [`5345376547`](https://github.com/Mast3rkey/Portfolio-HQ/pull/341#issuecomment-5345376547) — durable `user.login` **`Mast3rkey`** |
| Merge-commit CI | run [`32278094960`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32278094960) / job `96150134005` — `completed`/`success`, `head_sha` **the exact merge SHA**, attempt 1 |
| The retracted comment `5345204885` | durable `user.login` **`claude[bot]`**, `type: Bot` — VOID, conveys nothing |
| `XASSET-0041` | **EFFECTIVE** — all seven §J conditions closed |
| `XASSET-0040` | spent as `STOPPED_BEFORE_ATTESTATION`; **not revived** |
| `level1_stage1_execution_authorization.py` | blob `92f64374…` at `HEAD` **and** at the PR #337 merge — byte-identical to the bound pre-correction version |
| Lane state | exactly **`ABSENT`**; `AUTHORIZATION_ROOT` and all four lane paths **absent** |
| `new_execution_is_authorized()` | **`False`** |
| `ATTEMPT_1` | **intact, unclaimed, unconsumed** |
| `stage1_results.yaml` | **absent** anywhere on the filesystem |
| `XASSET-0042` identifier | **unused** — zero occurrences repository-wide; catalog held 143 decisions ending at `XASSET-0041` |

Read in full before designing: `XASSET-0041` (all of §§A–K), `XASSET-0029` including BLOCKING 2,
the `XASSET-0037` lifecycle binding, `XASSET-0040` and its step-11 stop evidence, and the production
lifecycle mechanism itself.

### The defect, reproduced before and after

Reproduced through the accepted public mechanism — `build_authorization_payload` assembled and
`verify_lifecycle_against_truth` run against **live** git and GitHub — bound exactly to
`XASSET-0037` / PR #337. **`write_authorization` was never called and no byte reached disk.**

The pre-correction baseline was measured in a **transient detached worktree at `HEAD`**, not by
patching a copy's module root, so the comparison is faithful rather than an artifact of the harness:

```
BEFORE (checkout at 9c8647f9, module blob 92f64374) — 2 lifecycle errors, both actor:
  governance truth: acceptance comment 5335697214 was authored by 'claude[bot]',
    not the principal 'Mast3rkey'
  governance truth: post-merge verification 5335849767 was authored by 'claude[bot]',
    not the lifecycle operator 'Mast3rkey'

AFTER (corrected) — 0 actor errors; 1 remaining error, expected and disclosed:
  enforcement drift: level1_stage1_execution_authorization.py in the working tree hashes to
    '03d84212…' but the authorized merged tree has '8186a50f…'
```

That single remaining error is **not a failed correction**. It is exactly the consequence
`XASSET-0041` §I names: corrected bytes "are no longer the bytes the single step-8 rebinding
bound," so a **separately authorized rebinding** is required. That rebinding is link 2 of five and
**is not performed, begun, or authorized here.**

## Decision

### A. Determination — `PR337_LIFECYCLE_ACTOR_EVIDENCE_CORRECTED`

The one bounded correction `XASSET-0041` authorizes is implemented, in
`level1_stage1_execution_authorization.py`, satisfying all ten conjunctive §F properties. Nothing
beyond it is done.

### B. What was changed — two call sites and one isolated section

**Two lines of behaviour.** The acceptance actor branch and the post-merge-verification actor
branch each gain **one** additional conjunct. Both error messages are **byte-unchanged**, so every
pre-existing expectation about them still holds:

```python
elif acceptance_actor != PRINCIPAL_ACCOUNT_LOGIN and not ratification.ratifies_acceptance(
    acceptance_id, acceptance_actor
):
    errors.append(...)          # wording unchanged
```

**One structurally isolated section**, added ahead of `verify_lifecycle_against_truth`: the pins,
a frozen two-field result type, and `_derive_pr337_actor_ratification`, which is evaluated **once**
per validation and returns the all-false instance for every document that is not PR #337's exact
lifecycle.

### C. The exception is a conjunction over four independent evidence families

All must hold. Any failure yields the all-false result and the ordinary error.

1. **Scope** — the document under validation IS PR #337's lifecycle, on all five §F.5 identities:
   head `f40c816223c78f1d1e436b718455df5fb3d77fa7`, review `4966846374`, acceptance `5335697214`,
   merge `637eaa30302f5a71f84ab1d215ecbd32c01399b5`, verification `5335849767`.
2. **Live agreement** — PR #337's own durable metadata still reports that head, that merge, merged
   state, and this repository.
3. **The ratification** — `XASSET-0041`'s **complete** lifecycle: PR #341 merged at the pinned head
   and merge; an approving, non-dismissed, exact-head review owned by that PR; a principal
   acceptance whose **derived `user.login`** is `Mast3rkey`, owned by that PR, naming its own head
   and review, all five ratified identities, the ratified actor, and §G.4's ratification statement;
   a post-merge verification and a final closure both durably authored by `Mast3rkey`; and
   merge-commit CI `completed`/`success` at the **exact merge SHA**, with its job correctly paired.
4. **Git** — the ratification merge has exactly two parents in order, and zero drift.

Plus **retrospection**: the ratification must **postdate** the PR #337 merge.

### D. How each of the ten §F properties is satisfied

| §F | Property | How |
|---|---|---|
| 1 | Ordinary `Mast3rkey` requirement preserved | `PRINCIPAL_ACCOUNT_LOGIN` / `LIFECYCLE_OPERATOR_LOGIN` unchanged; the default path is untouched for every other pull request |
| 2 | `claude[bot]` never generally classified | No allow-list, no bot class, no "trusted automation" category — asserted by a test that scans every module-level container for the login |
| 3 | Identity never from body text | `_actor_login` is the sole identity source, for the ratified records and the ratification alike; body checks verify only that the ratification **names** what §G requires |
| 4 | Ordinary chronology never weakened | No chronology check altered; a backfilled acceptance still trips "merge precedes acceptance" **even with the ratification present** |
| 5 | Exactly the five PR #337 identities | Six independent scope pins, each proved individually mandatory |
| 6 | New `Mast3rkey`-authored ratification required | Pinned comment `5345229177`, derived login, nine required content tokens |
| 7 | Bound to `XASSET-0041`'s completed lifecycle; wrong evidence rejected | Family 3 above; every enumerated wrong-evidence class has its own test |
| 8 | Retrospective, never fictional, never forward permission | Postdating requirement; nothing in the mechanism admits any future bot-authored gate |
| 9 | Fail-closed everywhere else | Unreachable governance and unreachable git both relock; malformed shapes relock |
| 10 | Adversarial tests prove no generalization | 121 tests; 43/43 mutations caught |

### E. Proof — 121 tests, 43 mutations, 43 caught, 0 missed, 0 aborted

Mutations spanned: principal and operator logins generalized to the bot; each ratification method's
comment-id and actor pins dropped; unconditional grants; the default instance silently granting;
each of the six scope pins removed; live head / merge / merged-state / repository checks removed;
the ratification PR's merged state, head, and merge unpinned; the review's existence (**with a
fully valid synthetic substitute**, so no downstream check could mask it), shape guard, exact-head,
dismissal, disposition, and ownership checks dropped; the ratification's author identity, ownership,
and content requirements dropped; the comment id repointed at the retracted `5345204885`; the
ratification post-merge verification and final closure dropped; merge-commit CI success, exact-SHA,
job pairing, and job success dropped; merge parent count, parent pins, and drift check dropped;
retrospection disabled; and each actor gate removed outright.

Every needle was verified present exactly once before mutating, and every file was restored
**byte-identically**, SHA-256 checked, after each round.

**Disclosed honestly:** the first pass caught **41 of 42**. The survivor was an *under-powered*
mutation, not an escape — it replaced a missing review with a stub carrying only `commit_id`, which
the **disposition** check still refused downstream. Rather than record a masked pass, the mutation
was strengthened to substitute a **fully valid** review (the genuine adversarial question), a second
mutation was added for the shape guard, and two new tests were added giving that guard independent
coverage. All 43 are then caught.

The suite carries **zero `or`-fallback assertions** — its own AST guard caught a real one during
development, which was rewritten rather than exempted — performs no filesystem write, imports no
outcome-producing module, references no protected `RISK` results path, and evaluates no gate; each
is AST-enforced.

### F. Disclosed, deliberately **not** repaired

Gate 2's own pre-existing `(evidence.get("principal_acceptance") or {}).get(...)` raises
`AttributeError` on a **truthy non-mapping** sub-block. That fragility predates this correction,
lives outside the two lines it touches, and repairing unrelated production behaviour is outside
`XASSET-0041`'s authorized scope. It is recorded here rather than quietly fixed, and a test asserts
the **correction itself** adds no such fragility.

### G. The downstream boundary — preserved, not collapsed

The corrected bytes are no longer the bytes the step-8 rebinding bound. Identities were
**recomputed for evidence only**, exactly as `XASSET-0041` §E.3 permits and §H requires, and
**deliberately not applied**:

```
bound (merged tree)  sha256  8186a50f71d05bbb7189183bacad6aa0752147e9c7f4e1f5b3bacabad91f2fc8
corrected worktree   sha256  03d842126913bf2d62aa5d7c070ecca236926ec847102da82414ee51e7422734
```

No pin was updated. `LOAD_BEARING_RELPATHS` (10 entries), `AUTHORIZING_DECISION` (`XASSET-0037`),
`AUTHORIZING_PULL_REQUEST` (337), and the accepted PR #337 bound identities are **unchanged**.

```
1. correction              <-- THIS unit, and only this
2. rebinding                   NOT authorized, NOT performed
3. renewed readiness           NOT authorized, NOT performed
4. renewed drift check         NOT authorized, NOT performed
5. new step-11 authorization   NOT authorized, NOT performed
```

Completing the correction authorizes the next link no more than a clean step-10 result authorized
step 11. **`XASSET-0040` remains spent as a stop and is not revived.**

### H. Absolute non-authorization

This unit rebinds nothing and changes no `LOAD_BEARING_RELPATHS` entry or hash pin; re-runs no
readiness verification and no post-rebinding drift check; retries no part of step 11; generates no
attestation; creates no `AUTHORIZATION_ROOT` and no `READY`, `CLAIMED`, or `COMPLETED` lane state or
ledger entry; arms, claims, completes, executes, or recovers nothing; consumes nothing of
`ATTEMPT_1`; evaluates no gate for any registered construction and asserts no per-construction
outcome; creates no `stage1_results.yaml`; changes no construction identity, universe membership,
ordering, cardinality, or universe hash; touches no canonical artifact, runner, result validator, or
universe module; acquires no market, fundamental, economic, or Stage-2 data; reads, lists, opens, or
references no protected `RISK` result; posts, backfills, fabricates, or pre-dates no lifecycle
comment on PR #337 or anywhere else; reopens no gate semantics and neither B1, B2, nor B3; consumes
no `XASSET-0027` §P.1 results PR; weakens no validator or test; creates no endpoint, bound, point,
range, percentage, weight, rank, target, or allocation; changes no `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes
no chart, ladder, deployment, trade, order, or brokerage action; and **authorizes no successor unit
of any kind.**

### I. Effectivity

Effective only after **all** of the following complete for this unit's final accepted head and the
resulting merge: independent **FULL** exact-head review under `OPS-0007` §1; any required bounded
correction and exact-head re-review, so the review holds at the **final** head; explicit principal
exact-head acceptance; normal merge; immediate post-merge verification; **successful merge-commit CI
whose `head_sha` is the exact merge SHA**; and final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this PR authorizes nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not. **Merging this correction does not arm Stage 1,
creates no lane state, claims no `ATTEMPT_1`, and executes nothing.** Immediately after it merges,
`new_execution_is_authorized()` still returns `False` and the lane is still `ABSENT`.

## Rationale

`XASSET-0041` established that the two `claude[bot]` records are real acts of the principal and that
comment-only backfill cannot repair them — a new comment necessarily postdates the merge and trips
the chronology rule. The only honest repair is therefore to let the principal **ratify the history
as it stands**, and to make that ratification carry as much authenticating weight as the gate it
substitutes for.

That is why the exception is bound to `XASSET-0041`'s **entire** lifecycle rather than to a bare
comment. A ratification is only as strong as the process that produced it: an independently
reviewed, principal-accepted, merged, post-merge-verified, CI-green decision is a materially
stronger artifact than a comment someone could post in a second. Requiring the whole chain means the
exception cannot be unlocked by anything cheaper than the process that authorized it.

The retrospection requirement is what keeps this honest. The mechanism does not pretend a
`Mast3rkey` acceptance happened before the merge; it requires the opposite — that the ratification
came **after** — and refuses anything claiming otherwise. Ratifying history and rewriting it are
different acts, and only the first is implemented.

## Alternatives Considered

**Add `claude[bot]` to an accepted-actor set.** Rejected: forbidden by §F.2, and it would silently
extend to every future pull request. The whole value of BLOCKING 2 is that no bot account can stand
in for the principal.

**Special-case only the two comment ids.** Rejected as too weak: id equality alone would let any
record bearing those ids unlock the gates regardless of the surrounding lifecycle, and would survive
a repointed or edited ratification.

**Relax the chronology rule so a backfilled acceptance validates.** Rejected: forbidden by §F.4 and
§F.8, and it would manufacture a fictional pre-merge event — precisely what `XASSET-0041` §C ruled
out.

**Repair the pre-existing Gate 2 non-mapping fragility while here.** Rejected as outside the
authorized scope. Disclosed in §F instead.

**Fold the rebinding in, since the correction makes it necessary.** Rejected: `XASSET-0041` §I lists
it as a separate link requiring its own authority, and combining them is exactly the collapse that
decision forbids.

## Consequences

The two historical actor errors are closed for exactly the PR #337 records the principal ratified,
and for nothing else. Every other pull request, actor, comment, head, review, merge, and chronology
behaves precisely as before, and bot-authored lifecycle gates remain refused everywhere.

The corrected module no longer matches the bytes the step-8 rebinding bound, so a full live
authorization now reports **enforcement drift** instead of the two actor errors. That is the
expected, disclosed hand-off to a **separately authorized** rebinding — not a regression, and not
something this unit repairs.

Stage 1 remains `UNARMED` and `NOT EXECUTABLE`. Lane state remains `ABSENT`. `ATTEMPT_1` remains
intact, unclaimed, and unconsumed. `XASSET-0027` §P.1 remains one, unspent, and unopened.
