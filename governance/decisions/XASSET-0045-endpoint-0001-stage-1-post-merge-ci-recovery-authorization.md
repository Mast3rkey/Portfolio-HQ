---
decision_id: XASSET-0045
date: 2026-08-21
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_merge_ci_recovery_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `f5dedce1d1d3116ed8a6845c4447388c85a5414c` |
| Worktree / stash | clean; no competing mutation lane |
| Open pull requests | **zero** |
| PR #344 | `merged: true`, `state: closed`, merged by `Mast3rkey` at `2026-08-21T02:22:17Z` |
| PR #344 base | `0709d2f05ab031ecb6f69c40465ed4a227983aed` |
| PR #344 accepted head | `9c2821ab9e0e0dff09f5a03da5a6034775b00750` |
| Merge parents, in order | `0709d2f05ab031ecb6f69c40465ed4a227983aed`, then `9c2821ab9e0e0dff09f5a03da5a6034775b00750` |
| Merge tree / accepted-head tree | both `bd9ce6694261a7b4fb664a5121d04571f9606924` — **zero merge drift** |
| Final clean review | [`4989080551`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#pullrequestreview-4989080551) @ `9c2821ab…` — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE |
| Principal acceptance | [`5364401900`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#issuecomment-5364401900) @ `9c2821ab…` |
| Post-merge verification | [`5364422640`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#issuecomment-5364422640) |
| Merge-commit CI | run [`32439614683`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32439614683) / job `96647501864` — `event: push`, attempt 1, `head_sha` = `f5dedce1…`, **`completed` / `failure`** |
| Auditable stop | [`5364490220`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#issuecomment-5364490220) — no lifecycle-closure comment posted |
| Universe | **680** constructions over **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` |
| Lane | **ABSENT** — `AUTHORIZATION_ROOT` does not exist |
| `new_execution_is_authorized()` | `False` |
| `ATTEMPT_1` | `ENDPOINT-0001::STAGE_1::ATTEMPT_1` — intact, unclaimed, unconsumed |
| `stage1_results.yaml` | absent — zero artifacts anywhere in the repository |
| Next unused identifier | `XASSET-0045`, verified unused against live repository state |

### The question this unit answers

`XASSET-0044`'s §L makes seven conditions **conjunctively** necessary. Six completed. The sixth —
*successful merge-commit CI whose `head_sha` is the exact merge SHA* — **failed**. The seventh, final
post-CI lifecycle closure, therefore never occurred and was correctly not manufactured.

The repository is consequently in a state no prior decision anticipated: a merged, reviewed,
accepted, drift-free rebinding whose governing decision is **not effective**, whose production
authorization mechanism nevertheless already names it, and whose single authorizing predecessor unit
is spent. Nothing in `XASSET-0043` §F, `XASSET-0044` §L, or any earlier filing authorizes a unit to
recover from that state.

**This decision authorizes exactly one such unit and performs no part of the recovery.** It does
perform one narrow, separately principal-authorized, test-only enabling correction — see §K.

## Decision

### A. Determination — `POST_MERGE_CI_RECOVERY_AUTHORIZED`

Exactly one future, separate recovery/reconciliation unit is authorized, bounded by §§F–J and
forbidden everything in §H.

This filing is **governance plus one narrow, separately principal-authorized, test-only enabling
correction** (§K). It performs **no** part of the recovery, edits no load-bearing implementation, no
runner, no result validator, no universe module, no canonical artifact, and no protected portfolio
path, and adds **no activation authority of any kind**.

### B. The defect, reproduced read-only before anything was authorized

The failure is **a moving test anchor**. It is neither merge drift nor outcome-surface drift.

The failing guard is `test_overlap_model_validator.py::test_real_repository_governance_decisions_pass_the_repaired_check`,
whose final assertion at **`test_overlap_model_validator.py:1119`** requires the one-use authorized
`XASSET-0042` decision modification to have been **exactly exercised**, so that the allowance cannot
linger as dead permission. It resolves its comparison base through `_resolve_pr_base_sha`, which
returns `git merge-base HEAD origin/main`.

That base is **not fixed**. It is a function of wherever `HEAD` and `origin/main` happen to point:

```
on the PR branch:   merge-base(9c2821ab…, 0709d2f0…) = 0709d2f0…
                    diff base..worktree under governance/decisions:
                      M  governance/decisions/XASSET-0042-…-correction.md
                      A  governance/decisions/XASSET-0044-…-rebinding.md
                    -> modified == ['…XASSET-0042-…md']  -> assertion HOLDS

on merged main:     merge-base(f5dedce1…, f5dedce1…) = f5dedce1…   (HEAD is origin/main)
                    diff base..worktree under governance/decisions: EMPTY
                    -> modified == []                    -> assertion FAILS
```

Both branches of that table were re-derived directly from the object store in this session, and the
failure was reproduced locally at `f5dedce1…`, byte-identical to CI:

```
AssertionError: the authorized modification set is not exactly what this branch changed: []
assert [] == ['governance/decisions/XASSET-0042-endpoint-0001-pr337-lifecycle-actor-evidence-correction.md']
test_overlap_model_validator.py:1119
```

The immutable job log records exactly **`1 failed, 10199 passed`**, the failure isolated to that one
assertion, with steps 1–6 and 14–15 of the workflow green.

**The guard's underlying subject is intact.** Over the closed, immutable range
`0709d2f05ab031ecb6f69c40465ed4a227983aed → 9c2821ab9e0e0dff09f5a03da5a6034775b00750` the authorized
one-use transition is genuinely exercised, and its object identities match the allowance exactly:

| | |
|---|---|
| old blob at base | `e4cda7a5042da68f347598a62d9e6d5cfc40ae55` |
| new blob at accepted head | `b08a625a5adb840e9576e5cd9218be24e63bd57e` |
| status | `M` — a modification, never a rename, copy or delete |

The property the guard exists to enforce is therefore **true**; only the anchor it measures against is
wrong. This is the same defect class PR #344 itself found and re-anchored in three predecessor suites,
left in a guard it added itself — and it could only surface after its own merge, which is precisely
why every pre-merge check passed.

### C. What is not in question

Independently re-verified in this session and **explicitly outside** the recovery unit's remit to
change:

- the merge has **exactly two parents in the correct order**, base then accepted head;
- the merge tree `bd9ce669…` is **byte-identical** to the accepted-head tree — zero merge drift;
- the outcome surface is untouched: `level1_stage1_runner.py`, `level1_stage1_result_validator.py`,
  `level1_construction_universe_closure_validator.py`, every gate, disposition rule, B1/B2/B3,
  `comparison_subject_kind`, `unordered_pair_id`, and construction identity;
- the universe is **680 / 48** with aggregate `73c0965e…5224`;
- the other **10199** tests pass; no production, canonical, protected-portfolio, `intelligence/`, or
  `governance/evidence/` content is implicated.

### D. A later green CI run cannot retroactively satisfy `XASSET-0044` §L.6

§L.6 requires, verbatim, *"successful merge-commit CI whose `head_sha` is the **exact merge SHA** —
not the PR head's own run, and not a run against any other commit."*

The exact merge SHA is `f5dedce1d1d3116ed8a6845c4447388c85a5414c`. Run `32439614683` / job
`96647501864` is the merge-commit CI at that `head_sha`, and it **failed**. That commit is immutable
and its recorded history is immutable with it.

A green run at any **other** commit — a successor merge, a re-run of a different SHA, a later `main` —
is by §L.6's own words *"a run against any other commit"* and is therefore **excluded by the
condition itself**, not merely unpersuasive. No subsequent CI success anywhere can convert
`f5dedce1…`'s failure into the success §L.6 demands.

Consequently `MERGE_COMMIT_CI_SUCCESS` is **permanently unsatisfiable for PR #344**, §L is
permanently unsatisfiable as written for that pull request, and `XASSET-0044` is **not effective and
cannot become effective through PR #344**. The recovery unit must therefore establish a **lawful
successor lifecycle anchor** (§G.6) rather than attempt to repair, re-run, reinterpret, or wait out
the failed run.

### E. `XASSET-0043`'s authorized unit is spent; `XASSET-0044` is not effective

`XASSET-0043` §F authorized **"exactly one future, separate, bounded pull request"** to file its own
rebinding decision and perform the rebinding in one coherent PR. PR #344 **was that unit**: it was
opened, filed `XASSET-0044`, was independently reviewed through four rounds to a clean disposition,
was principal-accepted at its exact head, and was merged.

**The unit was consumed by being used.** §F's grant is spent whether or not §L's effectivity
conditions later completed — effectivity governs whether the *rebinding takes effect*, not whether
the *authorized unit was expended*. `XASSET-0043` therefore **may not be reused** as authority for a
second attempt, and no session may treat `XASSET-0044` as effective, partially effective, or
provisionally effective.

Both facts are load-bearing for this filing: the recovery unit derives its authority from **this**
decision, and from nothing else.

### F. Authority granted — exactly one future, separate recovery/reconciliation unit

Effective only on this decision's own complete lifecycle closure (§M), **exactly one** future,
separate, bounded pull request may perform the recovery/reconciliation described in §G. It is one
unit and one pull request. A future session that finds a concrete technical reason to package it
differently must **stop and disclose**, not decide it silently.

**No second unit is authorized by this decision, and completing the authorized unit does not
authorize another.**

### G. Required properties of the authorized recovery unit

The authorized unit **must**:

**G.1 — File its own decision.** Under the **next `XASSET-####` identifier verified unused against
live repository state at the time it is filed** — never predicted, reserved, or assumed here. This
decision deliberately names no successor identifier.

**G.2 — Preserve and independently re-prove the corrected immutable-range guard.** The guard was
repaired by **this** filing under the separate principal authorization recorded in §K, so the future
unit does **not** perform that correction again. It must instead **preserve** the repaired guard and
**independently re-prove** that it still compares the immutable closed range

```
0709d2f05ab031ecb6f69c40465ed4a227983aed  ->  9c2821ab9e0e0dff09f5a03da5a6034775b00750
```

rather than any moving merge-base involving current `HEAD` or `origin/main`, and that it still does
not depend on where `HEAD` or `origin/main` point when it runs. Re-proving means running it and
confirming the property from repository truth — never citing this filing's word for it. The guard may
not be deleted, skipped, `xfail`ed, weakened, or re-anchored to any moving reference; it may only be
strengthened.

**G.3 — Prove the merge identity.** The accepted head `9c2821ab…` must be proven to be the **second
parent** of merge `f5dedce1d1d3116ed8a6845c4447388c85a5414c`, and its tree proven **byte-identical**
to the merge tree `bd9ce6694261a7b4fb664a5121d04571f9606924`.

**G.4 — Continue proving the one-use transition was exactly exercised.** The authorized `XASSET-0042`
decision modification must still be proven genuinely exercised within that closed range — base blob
`e4cda7a5…`, new blob `b08a625a…`, status `M` — with each conjunct independently required. The
allowance must remain incapable of lingering as dead permission, and every other pre-existing
decision file must remain protected.

**G.5 — Preserve the original failed run as immutable adverse history.** Run `32439614683` / job
`96647501864` must be retained, by exact identity, as the failed merge-commit CI for `f5dedce1…`. It
**may never** be relabelled successful, deleted, suppressed, re-run in place, described as passing,
or represented as satisfying `XASSET-0044` §L.6. The auditable stop
[`5364490220`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#issuecomment-5364490220) must
likewise be preserved.

**G.6 — Establish a lawful successor lifecycle anchor.** Production currently binds authorization
truth to `XASSET-0044` / PR #344 and to that pull request's failed exact-merge CI —
`AUTHORIZING_DECISION = "XASSET-0044"`, `AUTHORIZING_PULL_REQUEST = 344`,
`REVIEWED_BASE_SHA = "0709d2f0…"`. Because §L.6 is permanently unsatisfiable for PR #344 (§D), the
recovery unit must establish a successor lifecycle anchor against **its own** decision, pull request,
accepted head, merge, successful exact-merge CI, and final closure.

**G.7 — Rebind only as strictly necessary.** The operational-authorization mechanism may be rebound
**only** to the extent the successor lifecycle anchor requires. No unrelated configuration, identity,
threshold, gate, or evidence requirement may be changed under cover of the rebinding, and the
mechanism may not be made more permissive in any respect.

**G.8 — Preserve the predecessor evidence as independently authenticated.** The accepted head, the
merge, the zero-drift tree, the final clean review `4989080551`, the principal acceptance
`5364401900`, the post-merge verification `5364422640`, the failed CI run/job, and the stop notice
must all be preserved as authenticated predecessor evidence — retained and labelled, never erased,
overwritten, or silently re-pointed.

**G.9 — Preserve every outcome-producing semantic.** The runner, the result validator, the
construction-universe membership, order, and aggregate hash, the canonical inputs, all protected
paths, and every valid actor-evidence correction must be preserved unchanged.

**G.10 — Use exact closed transitions for every lawfully changed load-bearing byte.** Any guard that
asserts historical byte identity must do so against a closed, immutable commit range. **No moving
`HEAD`/`origin/main` guard may claim historical byte identity** — the exact defect this decision
exists to remedy must not be reintroduced anywhere.

**G.11 — Complete a full lifecycle.** Independent **FULL** exact-head review under `OPS-0007` §1;
any required bounded correction and exact-head re-review; explicit principal exact-head acceptance;
normal merge; immediate post-merge verification; **successful merge-commit CI at the future recovery
merge SHA**; and final post-CI closure.

**G.12 — Weaken nothing.** No existing assertion may be deleted, skipped, `xfail`ed, weakened, or
replaced with a less falsifiable one. Guards may be re-anchored and strengthened; they may not be
relaxed.

### H. Authority withheld — absolute

The authorized recovery unit adds **zero activation authority**. It may **not**:

- perform renewed readiness verification;
- perform renewed drift verification;
- perform or authorize **Step 11**;
- generate, pre-stage, or validate any **attestation**;
- create lane state, write `AUTHORIZATION_ROOT`, or write the lane ledger;
- **arm** Stage 1, or set `stage_1_executability.executable` to anything but `false`;
- **claim** or consume `ATTEMPT_1`;
- evaluate any gate for any registered construction;
- execute Stage 1, perform recovery execution, or perform any results work;
- produce a Stage-1 result, `stage1_results.yaml`, Stage 2, endpoint value, percentage, target,
  allocation, chart, ladder, or trade;
- access protected `RISK` evidence.

It may **not** reuse `XASSET-0043`, treat `XASSET-0044` as effective, re-open `ATTEMPT_1`, revive
`XASSET-0040` (which stays spent as `STOPPED_BEFORE_ATTESTATION`), or consume `XASSET-0027` §P.1
(which remains one and unspent).

`stage_1_executability.executable` stays permanently `false`. **No committed value in this repository
authorizes Stage-1 execution**, and this decision adds none.

### I. Fail-closed

Every unobtainable fact is an **error**, never silent agreement. If the recovery unit cannot
independently verify the merge parentage, the tree identity, the closed-range transition, the failed
run's identity, or its own lifecycle evidence, it must **stop and disclose** rather than proceed,
assume, or downgrade the requirement. Ambiguity, drift, or any condition that would require expanding
this authority is a **stop**, not a judgement call.

### J. Packaging and evidence

One coherent draft pull request, carrying its own decision record and the recovery in one unit, with
its own adversarial mechanism-based supporting artifact, catalog and `WS-0014` register
synchronization, and full verification evidence. It must not self-review, self-accept, mark itself
ready, merge itself, or post its own lifecycle closure.

### K. Scope of this filing — governance plus one narrow, separately authorized enabling correction

This filing is **not** purely design-only, and does not claim to be.

It performs **one** narrow, **test-only** enabling correction: the real-repository historical guard in
`test_overlap_model_validator.py` is re-anchored from `merge-base(HEAD, origin/main)` to the immutable
closed range `0709d2f0…` → `9c2821ab…`, together with the merge's exact two-parent ordering and
byte-identical accepted-head/merge trees.

**The authority for that correction is not created by this decision.** `XASSET-0045` cannot authorize
its own enabling repair without circularity. The authority is a **separate, explicit principal
authorization**, given after independent FULL review `4989608238` returned `CHANGES REQUIRED` with
one BLOCKING finding: the filing as reviewed required successful merge-commit CI (§M.6) while
simultaneously declaring that CI necessarily impossible (§N as reviewed), so its own effectivity was
unattainable and the unit it authorizes could never lawfully begin. That principal authorization
superseded **only** the prior instruction barring this filing from editing that test file. Every other
scope limit and every Stage-1 prohibition remained, and remains, fully operative.

The correction is **strictly narrowing in effect**: every conjunct the previous guard proved is still
proved, and the parent-ordering and tree-identity proofs are new. Nothing was deleted, skipped,
`xfail`ed, weakened, or replaced with a less falsifiable assertion. `_resolve_pr_base_sha` is
deliberately **unchanged** and still serves the live working-tree guard, whose subject genuinely is a
moving base.

Beyond that one test-only correction, this filing still edits **no** load-bearing implementation, no
runner, no result validator, no universe module, no canonical artifact, no operational-authorization
mechanism, and no protected portfolio path — and adds no production, canonical, lane, results, or
Stage-1 authority of any kind. The corrected file is independently confirmed **not** to be a member of
`LOAD_BEARING_RELPATHS`.

### L. Relation to `XASSET-0029` §E — not an activation PR

This is not an activation pull request. It generates no attestation, arms nothing, and adds **zero**
activation authorizations. Final activation remains the external one-shot runtime attestation and the
operator's act, never a merged authorization PR.

### M. Effectivity

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own
   run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this PR authorizes nothing; a green PR-head CI run does
not; principal acceptance does not; merge does not.

**Merging this arms nothing.** Immediately after it merges, `new_execution_is_authorized()` still
returns `False`, the lane is still `ABSENT`, `ATTEMPT_1` is still intact and unconsumed, and no
`stage1_results.yaml` exists.

### N. Correction history — the reviewed head's failure, and its repair

**Retained as adverse history, not erased.** At reviewed head
`e6e4874aca34f383f99cb130da3b45625d8c9aa3`, exact-head CI run `32443765403` / job `96659425926`
completed **`failure`** with `1 failed, 10292 passed` — the single failure being the §B defect, then
still uncorrected in this branch. That run and its result stand exactly as recorded.

At that head this filing was barred from editing `test_overlap_model_validator.py`, so the defect
reproduced on this branch too: a newly added decision file is status `A`, which the guard skips,
leaving `modified == []`. Independent FULL review `4989608238` correctly identified the consequence
as **BLOCKING** — §M.6 requires successful merge-commit CI while §N as reviewed declared that CI
necessarily impossible, an unattainable effectivity chain.

**That premise is now removed, not weakened.** Under the separate principal authorization recorded in
§K, the guard has been re-anchored to the immutable closed range, and this filing's CI is expected to
be **green**. §M.6 is unchanged and remains fully required — a red corrected-head CI is a stop, not
an accepted deviation.

Nothing here retroactively repairs PR #344's own failed merge-commit CI. Run `32439614683` / job
`96647501864` at merge `f5dedce1…` remains immutable adverse history (§D, §G.5), `XASSET-0044`
remains not effective, and `XASSET-0043` remains spent.

## Rationale

The mechanism worked. `MERGE_COMMIT_CI_SUCCESS` went unsatisfied, final closure was correctly not
manufactured, and Stage 1 stayed unarmed with `ATTEMPT_1` untouched. The correct response to a
fail-closed stop is a **separately authorized** recovery unit, not an improvised repair inside a
lifecycle operation that is barred from editing files.

Authority for that unit had to come from somewhere. `XASSET-0043`'s single grant is spent (§E) and
`XASSET-0044` is not effective (§D), so no existing decision could carry it. Filing a narrow
authorization is the smallest lawful step that unblocks the recovery without deciding it.

The filing as first reviewed went one step too far in the other direction. By barring itself from the
one test correction its own effectivity depended on, it made §M.6 unattainable — an authorization
that could never take effect, and so a future unit that could never lawfully begin. Independent FULL
review `4989608238` found that deadlock BLOCKING, and the principal separately authorized exactly the
narrow, test-only repair needed to break it (§K). Breaking a deadlock is not the same as widening
scope: the repair touches one non-load-bearing test, proves strictly more than it did before, and
leaves every production, canonical, lane, and Stage-1 boundary exactly where it was.

Separating authorization from execution also preserves reviewability: the recovery's own decision,
PR, review, acceptance, merge, CI, and closure are all still ahead of it, each independently gated.
Nothing here shortens that chain, and nothing here touches the outcome surface.

## Alternatives Considered

**Correct the guard in this filing.** Originally rejected — it appeared to collapse authorization
and execution into one unit. **That rejection was wrong, and review `4989608238` showed why:** the
production recovery and this filing's own enabling repair are different things. Leaving the guard
broken did not preserve separation; it made this authorization permanently inert. **Now adopted**,
under separate explicit principal authority, bounded to the one test-only correction §K describes.
The production rebinding — the actual recovery — remains entirely with the future unit.

**Repair the guard by loosening it instead** (skip, `xfail`, delete the exercised-exactly assertion,
or relax the status filter). Rejected outright: the property is sound and was never the problem; only
its anchor moved. Loosening would trade a false-red for a false-green and destroy the one-use
protection the allowance depends on.

**Re-run the failed CI job.** Rejected on the condition's own words: §L.6 names the exact merge SHA
and excludes runs against any other commit; a re-run cannot alter the recorded failure of run
`32439614683`, and treating a re-run as satisfaction would rewrite adverse history.

**Treat `XASSET-0044` as effective because six of seven conditions completed.** Rejected: §L makes
the seven conjunctive and says in terms that none is individually sufficient. Six of seven is not
seven.

**Reuse `XASSET-0043` §F for a second attempt.** Rejected: §F grants exactly one unit, PR #344 was
that unit, and a spent grant is not renewed by the outcome of the unit that spent it.

**Amend `XASSET-0044` §L to accept a later run.** Rejected outright: it would retroactively weaken an
accepted effectivity condition to accommodate its own failure, which is precisely the class of move
the fail-closed design exists to prevent.

## Consequences

On this decision's complete lifecycle closure, exactly one future recovery/reconciliation unit
becomes authorized to begin, bounded by §§F–J and forbidden everything in §H. Until then it may not
be opened, drafted, or begun.

`XASSET-0044` remains not effective. `XASSET-0043` remains spent. Run `32439614683` / job
`96647501864` remains the failed merge-commit CI for `f5dedce1…`, permanently. `XASSET-0027` §P.1
remains one and unspent. `XASSET-0040` remains spent as `STOPPED_BEFORE_ATTESTATION`.

Stage 1 remains **UNARMED and NOT EXECUTABLE**, the lane **ABSENT**, `ATTEMPT_1` intact, unclaimed
and unconsumed, and no `stage1_results.yaml` exists anywhere in the repository.
