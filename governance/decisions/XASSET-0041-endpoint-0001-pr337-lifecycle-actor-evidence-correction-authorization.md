---
decision_id: XASSET-0041
date: 2026-08-19
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_pr337_actor_evidence_correction_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `f212cce50e28ae887dc8c594bf8ae491a3ef85af` |
| Worktree / stash / worktrees | clean; no stash; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #340 | merged and closed, `merged_by` `Mast3rkey`, merge commit `f212cce5…`, 7 files, 3 commits |
| `XASSET-0040` | **effective** — its complete §N seven-condition lifecycle closed |
| **Step-11 stop evidence** | [`#issuecomment-5343692162`](https://github.com/Mast3rkey/Portfolio-HQ/pull/340#issuecomment-5343692162) — authored by `Mast3rkey`, belongs to PR #340, records **`STOPPED_BEFORE_ATTESTATION`** |
| Lane state | exactly **`ABSENT`**; `AUTHORIZATION_ROOT` and all four lane paths **absent** |
| `new_execution_is_authorized()` | **`False`** |
| `ATTEMPT_1` | **intact, unclaimed, unconsumed** |
| `research/level1_endpoint_evidence/stage1_results.yaml` | **absent** |
| Preserved step-11 clone | `/var/tmp/phq-endpoint0001-stage1-step11-exec` — detached at `f212cce5…`, worktree clean, **untouched** |
| Preserved dry-run evidence | `/var/tmp/phq-step11-dryrun-evidence.py`, SHA-256 `46026f48…cb8e7f5f`, **untouched** |
| `XASSET-0041` identifier | **unused** — zero occurrences repository-wide; catalog holds 142 decisions ending at `XASSET-0040` |

### The question this unit answers

The `XASSET-0040` step-11 unit ran and stopped at its **first** terminal condition, §K.1
**`STOPPED_BEFORE_ATTESTATION`**. Nothing was armed, nothing was claimed, `ATTEMPT_1` is untouched.

Every §H condition verified clean **except one**. §H.4 requires the `XASSET-0037` lifecycle evidence —
all six `REQUIRED_LIFECYCLE_GATES` — re-derived from durable truth. Four authenticate. **Two do not**,
because the only durable PR #337 records that satisfy the principal-acceptance and post-merge-verification
gates are authored by **`claude[bot]`**, not by the bound `Mast3rkey`.

This is not a defect in the canonical bytes, the universe, the runner, or the lane — all verified clean.
It is a **historical governance-evidence mismatch** on a pull request that merged before the step-11 unit
existed. `XASSET-0040` §J is explicit that finding such a defect is **not** authority to repair it:
remediation requires its own separate governance authority.

**This decision is that authority, for the correction only, and nothing more.**

## Decision

### A. Determination — `PR337_LIFECYCLE_ACTOR_EVIDENCE_CORRECTION_AUTHORIZED`

**Exactly one** future, separate, bounded correction to the PR #337 lifecycle actor-evidence mechanism
is authorized: a change that **preserves actor authentication in full** while supporting **one narrowly
pinned historical ratification path** for the exact PR #337 records enumerated in §F.5.

**This filing implements no part of that correction.** It edits no load-bearing byte, posts and
backfills no ratification, rebinds nothing, re-runs no readiness or drift verification, retries no part
of step 11, and creates no result.

### B. The defect, reproduced read-only before anything was authorized

The failing condition was reproduced in this session using the **accepted production mechanism**, bound
exactly to `XASSET-0037` / PR #337 — no constant altered, no `XASSET-0040` or PR #340 field inserted,
the closed schema untouched. The payload was assembled with `build_authorization_payload` and checked
with `validate_authorization_document`. **`write_authorization` was never called and no byte reached
disk.**

Every lifecycle field was derived live rather than asserted: `authorization_head`
`f40c816223c78f1d1e436b718455df5fb3d77fa7` and `merge_commit_sha`
`637eaa30302f5a71f84ab1d215ecbd32c01399b5` from the live pull request; merge parents from git; the sole
approving exact-head review selected by scanning all ten reviews.

**Verdict: `valid = False`, two errors, verbatim:**

```
governance truth: acceptance comment 5335697214 was authored by 'claude[bot]',
  not the principal 'Mast3rkey'
governance truth: post-merge verification 5335849767 was authored by 'claude[bot]',
  not the lifecycle operator 'Mast3rkey'
```

**Four of six gates authenticate** — `INDEPENDENT_FULL_EXACT_HEAD_REVIEW` (review `4966846374`,
`Mast3rkey`, exact head, approving, final), `MERGE` (exact parents, zero merge drift),
`MERGE_COMMIT_CI_SUCCESS` (run `32198881652` / job `95908324747`, `completed`/`success`, `head_sha`
equal to the merge SHA), and `MERGED_SUCCESSOR_HASH_AND_UNIVERSE_HASH_VERIFICATION`. **Two do not:**
`PRINCIPAL_EXACT_HEAD_ACCEPTANCE` and `POST_MERGE_VERIFICATION`.

All **13** PR #337 issue comments were enumerated and tested against both gates. The only comments
naming the exact head **and** certifying review `4966846374` are `5335697214` and `5335849767`, both
`claude[bot]`; the only comment naming the merge SHA is `5335849767`, `claude[bot]`. The nine
`Mast3rkey`-authored comments all predate the final head and satisfy neither gate. **No substitute
record exists.**

### C. Why comment-only backfill cannot repair the principal-acceptance gate

This was **proved from the mechanism's own enforced chronology**, not assumed.

`verify_lifecycle_against_truth` enforces the ordinary lifecycle order **review → acceptance → merge →
post-merge verification**, including:

```python
if accepted and merged_at and str(merged_at) < str(accepted):
    errors.append(f"governance truth: merge {merged_at} precedes acceptance {accepted}")
```

The durable timestamps are fixed and unchangeable:

| Record | Timestamp |
|---|---|
| Review `4966846374` submitted | `2026-08-18T23:10:37Z` |
| Acceptance `5335697214` created (`claude[bot]`) | `2026-08-18T23:50:29Z` |
| **PR #337 merged** | **`2026-08-18T23:50:58Z`** |
| Post-merge verification `5335849767` created (`claude[bot]`) | `2026-08-19T00:12:40Z` |

**Any new `Mast3rkey` comment is necessarily created after the merge** — PR #337 merged on
2026-08-18, and no comment can be created in the past. Empirically confirmed this session: a new
comment would carry `2026-08-19T15:03:07Z`, and `str(merged_at) < str(new_comment)` evaluates **`True`**,
so a backfilled acceptance comment **necessarily triggers "merge precedes acceptance."**

**Comment-only backfill is therefore structurally impossible for the principal-acceptance gate.** It is
not merely undesirable; the mechanism's own chronology rule forbids it, and that rule is one this
decision expressly declines to weaken (§F.4).

**The asymmetry is recorded honestly.** The post-merge-verification gate is *not* chronologically
blocked — a new comment would legitimately fall after the merge. It remains blocked only on actor
identity. But backfilling it alone would leave the acceptance gate unrepaired, and would manufacture a
"post-merge verification" record dated ten months of repository history after the verification it
purports to record. **Neither gate is repaired by writing new comments, and this decision authorizes
writing none.**

### D. Why this does not weaken `XASSET-0029` BLOCKING 2

The actor check exists because of `XASSET-0029`'s third bounded correction (independent FULL review
`4946464366`), which states its own purpose exactly:

> **BLOCKING 2 — lifecycle gates did not authenticate their actor.** Acceptance and post-merge
> verification were checked for location, body, and chronology, but never for author. … **Any account
> able to comment on PR #328 could impersonate either gate.**

and, in the same correction, records the boundary of what it proves:

> Verifying the author remains load-bearing — it stops *other* accounts from impersonating the gates —
> but it is not, and is not claimed to be, a separation-of-duties proof.

The property BLOCKING 2 established is therefore **anti-impersonation**: an arbitrary third-party
account must not be able to satisfy a lifecycle gate. The authorized design preserves that property
exactly, because the historical exception is unlocked **only** by a new record whose own author is
authenticated as `Mast3rkey` by the same derived-`user.login` mechanism, naming the exact historical
identities. An arbitrary account can no more produce that ratification than it can produce a valid
acceptance today.

**What the design must not do is convert `claude[bot]` into a generally acceptable actor.** That would
extend the gate to any record any bot produced on any pull request, which is precisely the
impersonation surface BLOCKING 2 closed. §F.2 forbids it.

### E. Authority granted — exactly one future, separate bounded correction

The future correction unit **may**, and only in service of the defect reproduced in §B:

1. **Modify the lifecycle actor-evidence verification** in `level1_stage1_execution_authorization.py`
   so the design required by §F is implemented.
2. **Add adversarial tests** proving the exception cannot generalize (§F.10).
3. **Recompute** whatever identities and pins that module's own change makes stale, **only after** its
   bytes have stabilized.
4. **Record** what it did as its own durable evidence under its own lifecycle.

That is the whole of the granted authority. It is a **correction**, in `XASSET-0040` §J's exact sense,
and nothing beyond it.

### F. The ten required properties of the authorized design

The future correction **must** satisfy all ten. These are conjunctive; a design failing any one is not
the design this decision authorizes.

1. **Preserve the existing `Mast3rkey` actor requirement** for ordinary and future lifecycle records.
   The default path is unchanged for every pull request other than the exact §F.5 records.
2. **Never classify `claude[bot]` generally as the principal or lifecycle operator.** No general
   allow-list, no bot-account class, no "trusted automation" category. `PRINCIPAL_ACCOUNT_LOGIN` and
   `LIFECYCLE_OPERATOR_LOGIN` remain `Mast3rkey`.
3. **Never infer actor identity from comment body text.** Identity stays derived from durable
   `user.login`. A record with no durable author identity remains refused.
4. **Never remove or weaken the ordinary review → acceptance → merge → post-merge-verification
   chronology** for any record outside the §F.5 set.
5. **Apply only to the exact PR #337 historical records**, each pinned by exact identity:
   - final head `f40c816223c78f1d1e436b718455df5fb3d77fa7`
   - final review `4966846374`
   - acceptance comment `5335697214`
   - merge `637eaa30302f5a71f84ab1d215ecbd32c01399b5`
   - post-merge verification `5335849767`
6. **Require a new, explicit `Mast3rkey`-authored ratification record** that names **all** of those
   exact identities and states that the two `claude[bot]` lifecycle comments were **authorized acts
   performed for the principal**.
7. **Bind that ratification to this decision's own completed lifecycle**, and **reject** missing,
   wrong-actor, wrong-PR, wrong-head, wrong-review, wrong-merge, substituted-comment, altered-record,
   or ambiguous evidence.
8. **Treat the new record as retrospective ratification of the exact historical acts** — never as a
   fictional pre-merge acceptance event, and never as permission for future bot-authored lifecycle
   gates.
9. **Retain fail-closed behaviour for every other pull request, actor, comment, and chronology.** An
   unreachable source still fails closed.
10. **Add adversarial tests proving the exception cannot generalize** beyond the exact PR #337 record —
    including that substituting any other PR, head, review, merge, or comment id fails, that a
    ratification by any non-`Mast3rkey` actor fails, and that `claude[bot]` gains nothing anywhere else.

#### F.1 — The exception is retrospective, not retroactive

The ratification does not assert that a `Mast3rkey` acceptance occurred before the merge. It asserts
something narrower and true: that the two specific `claude[bot]` comments on PR #337 were acts
performed **for** the principal, and that the principal, now, durably says so. The historical record is
not rewritten — it is **ratified as it stands**, which is why the chronology rule of §C need not be
touched.

### G. The ratification record

The ratification required by §F.6 is **this decision's own principal-acceptance comment**, and it
carries requirements beyond an ordinary acceptance:

1. It **must be authored by `Mast3rkey`**, verified by derived `user.login`.
2. It must name this decision's own exact accepted head and the independent review it relies upon, as
   every principal acceptance in this repository does.
3. It must **additionally** name, explicitly, all five §F.5 identities.
4. It must **state explicitly** that acceptance comment `5335697214` and post-merge verification
   comment `5335849767`, both authored by `claude[bot]` on PR #337, were **authorized acts performed
   for the principal**.

**This authoring session specifies that requirement and does not discharge it.** It posts no principal
acceptance and no ratification. Producing that record is the principal's own act, at this decision's
own exact final head, after independent review.

### H. Authority withheld — absolute

This filing, and the correction unit it authorizes, **must not**:

- **implement the correction here** — this decision is governance-only;
- edit `level1_stage1_execution_authorization.py` or **any** load-bearing path in this filing;
- touch the runner, result validator, construction-universe module, canonical artifacts, research
  results, protected portfolio paths, or any `RISK` path;
- touch `AUTHORIZATION_ROOT`, any lane path, or the preserved step-11 clone and dry-run evidence;
- post, backfill, fabricate, or pre-date any lifecycle comment on PR #337 or anywhere else;
- **rebind** anything — no change to `LOAD_BEARING_RELPATHS`, no re-pin, no alteration of
  `AUTHORIZING_DECISION` or `AUTHORIZING_PULL_REQUEST`;
- re-run readiness verification or the post-rebinding drift check;
- **retry step 11** in any form, or attest, arm, reach `READY`, claim, execute, complete, or recover;
- consume any part of `ATTEMPT_1`;
- open, consume, or pre-empt `XASSET-0027` §P.1's reserved results PR;
- create `stage1_results.yaml` or any per-construction disposition, cell outcome, or roll-up;
- evaluate any gate for any registered construction;
- acquire market, fundamental, economic, or Stage-2 data — the GitHub source remains **governance
  metadata only**;
- read, list, open, or substantively reuse any `risk_lane_boundary` protected `RISK` result;
- reopen, re-derive, or re-argue B1, B2, B3, any gate semantics, `XASSET-0030`'s 6/6 gate map,
  `XASSET-0024` §K.1, or `XASSET-0020` §E.1;
- reopen or overturn the completed step-9 `PASS`, the completed step-10 `STEP_10_NO_DRIFT`, or the
  step-11 `STOPPED_BEFORE_ATTESTATION` determination;
- change any construction identity, universe membership, ordering, cardinality, or universe hash;
- produce any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- **authorize any successor unit of any kind.**

### I. Downstream boundary — `XASSET-0040` §J's sequence is preserved, not collapsed

The authorized correction will change `level1_stage1_execution_authorization.py`, which is
**load-bearing path #1**. `XASSET-0040` §J states the consequence directly: corrected bytes "are no
longer the bytes the single step-8 rebinding bound," so a correction requires a **rebinding**, and any
**renewed readiness verification and drift check** that correction and rebinding make necessary.

That sequence is preserved in full, and each link requires its **own** separate governance authority
and its **own** complete lifecycle:

```
1. correction              <-- THIS decision authorizes only this
2. rebinding                   (separately authorized; XASSET-0030 §G.B step-8 equivalent)
3. renewed readiness           (separately authorized; step-9 equivalent, read-only)
4. renewed drift check         (separately authorized; step-10 equivalent, fail-closed)
5. new step-11 authorization   (separately authorized; XASSET-0040 is spent as a stop)
```

**None of links 2 through 5 is authorized, pre-authorized, combined, or made reachable by this
decision or by the correction succeeding.** Completing the correction authorizes the next link no more
than a clean step-10 result authorized step 11 — the inference `XASSET-0039` §K already foreclosed.

**`XASSET-0040` is not revived by this decision.** Its single authorized unit ran and reached a
terminal §K.1 stop. A future step-11 attempt needs its own new authorization.

### J. Effectivity

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge — the repository's own six
`REQUIRED_LIFECYCLE_GATES` plus `OPS-0009` §6's exact-head discipline:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head, **carrying the §G ratification
   language**;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA**;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this PR authorizes nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not. **Only complete closure of all seven does** — and
even then what becomes authorized is a **future correction unit**, not an armed Stage 1.

**Merging this decision does not arm Stage 1, does not create lane state, does not claim `ATTEMPT_1`,
and executes nothing.** Immediately after it merges, `new_execution_is_authorized()` still returns
`False` and the lane is still `ABSENT`.

### K. Absolute non-authorization

This decision implements no correction; edits no load-bearing, canonical, validator, authorization,
runner, result-production, universe, or protected portfolio byte; posts, backfills, or fabricates no
ratification or lifecycle comment; rebinds nothing and changes no `LOAD_BEARING_RELPATHS` or hash pin;
re-runs no readiness verification and no drift check; retries no part of step 11; generates no
attestation; creates no `AUTHORIZATION_ROOT` and no `READY`, `CLAIMED`, or `COMPLETED` lane state or
ledger entry; arms, claims, completes, executes, or recovers no Stage-1 execution; consumes nothing of
`ATTEMPT_1`; evaluates no gate for any registered construction and asserts no per-construction outcome;
creates no `stage1_results.yaml`; changes no construction identity, universe membership, ordering,
cardinality, or universe hash; acquires no market, fundamental, economic, or Stage-2 data; reads,
lists, opens, or references no `risk_lane_boundary` protected `RISK` result; resolves `XASSET-0024`
§K.1 neither way and amends no `XASSET-0020` §E.1 scope; reopens no gate semantics and neither B1, B2,
nor B3; consumes no `XASSET-0027` §P.1 results PR; weakens no validator or test; creates no endpoint,
bound, point, range, percentage, weight, rank, target, or allocation; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin
state; authorizes no chart, ladder, deployment, trade, order, or brokerage action; and rewrites no
accepted history.

## Rationale

The step-11 unit did exactly what it was built to do. It verified conjunctively, found one condition
unmet, and stopped without arming — leaving `ATTEMPT_1` intact and every recovery option open. That is
the system working, and the cost of the stop was one authorized unit, not a consumed one-shot attempt.

What it surfaced is a genuine mismatch between two things that were each individually correct. PR #337's
lifecycle was conducted through this repository's ordinary tooling, which posts as `claude[bot]`. The
attestation mechanism, hardened by `XASSET-0029` BLOCKING 2, requires lifecycle records to carry the
principal's own durable login. Neither was wrong when it happened; they simply do not compose, and the
mismatch only became visible when an attestation was assembled for the first time.

The narrow question is how to repair that without giving up what BLOCKING 2 bought. Three properties
make the authorized shape the right one. First, the exception is pinned to five exact identities, so it
cannot be reached by any other pull request, head, review, merge, or comment. Second, it is unlocked
only by a record whose own actor is authenticated by the unchanged mechanism, so an arbitrary account
gains nothing — the impersonation surface stays closed. Third, it is retrospective: the principal
attests that specific past acts were performed for them, rather than the mechanism pretending a
pre-merge acceptance occurred that did not.

The chronology proof in §C is what rules out the obvious cheaper alternative. A new comment cannot
satisfy the acceptance gate, because the gate requires acceptance to precede the merge and the merge is
already in the past. That is not a policy preference; it is arithmetic on immutable timestamps, and it
is why a mechanism change — rather than more evidence — is the only honest repair.

Filing this as governance-only, ahead of any code, follows the discipline this chain has held
throughout. `XASSET-0040` §J says finding the work is not authority to do the work. The correction
touches load-bearing path #1, which invalidates the single step-8 rebinding and everything verified
against it. Authorizing the correction alone — and stating the four downstream links it does *not*
authorize — keeps each irreversible boundary behind its own review.

## Alternatives Considered

**Backfill a `Mast3rkey` acceptance comment on PR #337.** Rejected, and shown impossible in §C: the
mechanism requires acceptance to precede the merge, and any new comment necessarily follows it. Even
setting chronology aside, a comment dated after the fact and presented as the original acceptance would
misrepresent the record.

**Add `claude[bot]` to the accepted actors.** Rejected. This reopens exactly the surface BLOCKING 2
closed — a bot account able to comment could then satisfy a lifecycle gate on any pull request. §F.2
forbids it outright.

**Relax the chronology rule so a late acceptance is tolerated.** Rejected. The ordering is load-bearing
for every future lifecycle, and weakening it to fix one historical record trades a permanent property
for a one-time convenience. §F.4 forbids it.

**Re-run PR #337's lifecycle, or re-merge it under the principal's account.** Rejected. History is not
rewritten in this repository, and the merge, its parents, and its zero-drift tree are already bound into
the executable package's identity. Re-doing it would invalidate the very bytes the rebinding proved.

**Fold the correction, rebinding, renewed readiness, drift check, and a new step-11 authorization into
one filing.** Rejected. `XASSET-0040` §J requires each as a separately authorized act, and the whole
architecture of this chain is that irreversible steps do not share a review. §I keeps them separate.

**Implement the correction in this PR.** Rejected. The correction edits load-bearing path #1; doing it
inside the filing that authorizes it would mean the change was never independently reviewed against a
merged authority, which is the failure mode every prior link in this chain was built to prevent.

## Consequences

One future bounded correction to the PR #337 lifecycle actor-evidence mechanism becomes authorized once
this decision's own seven-condition lifecycle closes in full — and not before.

Actor authentication survives intact. The default path is unchanged for every pull request, every
actor, and every chronology outside the five pinned PR #337 identities, and `claude[bot]` gains no
general standing anywhere. The historical exception exists only where a `Mast3rkey`-authored
ratification naming all five identities exists, and fails closed everywhere else.

This decision's own principal acceptance carries an unusual additional duty: it is also the ratification
record §F.6 requires. It must be authored by `Mast3rkey`, name all five identities, and state that the
two `claude[bot]` comments were authorized acts performed for the principal. This authoring session
specifies that duty and does not discharge it.

Nothing downstream moves. The correction does not rebind; the rebinding is not authorized; renewed
readiness and drift verification are not authorized; and step 11 is not retried. `XASSET-0040` is spent
as a stop and is not revived, so a future attempt needs its own new authorization. `XASSET-0027` §P.1
remains **one, unspent, unopened** — there is no result to deliver, and none is created here.

**Stage 1 remains `UNARMED` and `NOT EXECUTABLE`. Lane state is `ABSENT`. `ATTEMPT_1` is intact,
unclaimed, and unconsumed. No gate was evaluated for any construction, and no part of step 11 was
performed or retried.**
