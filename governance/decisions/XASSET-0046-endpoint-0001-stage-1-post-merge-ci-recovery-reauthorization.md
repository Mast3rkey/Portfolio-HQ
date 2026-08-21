---
decision_id: XASSET-0046
date: 2026-08-21
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_merge_ci_recovery_reauthorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `2f8cdebe14925021171b9779453946be1f69b506` |
| Worktree / worktrees | clean; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #345 | `merged: true`, `state: closed`, merged by `Mast3rkey` at `2026-08-21T14:11:20Z`, 12 files, 4 commits |
| PR #345 base | `f5dedce1d1d3116ed8a6845c4447388c85a5414c` |
| PR #345 accepted head | `61e629f0f655ce8ca4ccd7eaa370d132d593515c` |
| Merge parents, in order | `f5dedce1d1d3116ed8a6845c4447388c85a5414c`, then `61e629f0f655ce8ca4ccd7eaa370d132d593515c` |
| Merge tree / accepted-head tree | both `e5eb890550d55aa74c7430871f176761526b1ecf` — **zero merge drift**; accepted-head-to-merge diff empty |
| Final clean review | [`4993994386`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#pullrequestreview-4993994386) @ `61e629f0…` — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE |
| Principal acceptance | [`5370936620`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#issuecomment-5370936620) @ `61e629f0…` |
| Post-merge verification | [`5370989769`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#issuecomment-5370989769) |
| Merge-commit CI | run [`32490789238`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32490789238) / job `96797667282` — `event: push`, attempt 1, `head_sha` = `2f8cdebe…`, **`completed` / `failure`**, `1 failed, 10348 passed` |
| Auditable stop | [`5371158269`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#issuecomment-5371158269) — no lifecycle-closure comment posted |
| `AUTHORIZING_DECISION` / `AUTHORIZING_PULL_REQUEST` | `XASSET-0044` / `344` — unchanged, and unchanged by this filing |
| `LOAD_BEARING_RELPATHS` | **14**; `test_overlap_model_validator.py` independently confirmed **not** a member |
| Universe | **680** constructions over **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` |
| Lane | **ABSENT** — `AUTHORIZATION_ROOT` does not exist |
| `new_execution_is_authorized()` | `False` |
| `stage_1_executability.executable` | `false` |
| `ATTEMPT_1` | `ENDPOINT-0001::STAGE_1::ATTEMPT_1` — intact, unclaimed, unconsumed |
| `stage1_results.yaml` | absent — zero artifacts anywhere in the repository |
| Next unused identifier | `XASSET-0046`, verified unused against live repository state: no decision file, no catalog entry, no register mention; its only two repository occurrences are **negative guards** in predecessor suites forbidding a successor identifier from being *reserved* |

Read in full before designing: `XASSET-0043` (all of §§A–N), `XASSET-0044` (§§A–N, especially §L),
`XASSET-0045` (§§A–N), reviews [`4989608238`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#pullrequestreview-4989608238),
[`4993351528`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#pullrequestreview-4993351528) and
[`4993994386`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#pullrequestreview-4993994386), the
acceptance, post-merge and stop comments above, the failed run and job logs, `OPS-0001`,
`OPS-0007` §1, and `OPS-0009`.

### The question this unit answers

`XASSET-0045` §M makes seven conditions **conjunctively** necessary. Six completed. The sixth —
*successful merge-commit CI whose `head_sha` is the exact merge SHA* — **failed**. The seventh, final
post-CI lifecycle closure, therefore never occurred and was correctly not manufactured.

`XASSET-0045` was itself the recovery authorization for `XASSET-0044`'s identically-stopped lifecycle.
Its own stop leaves the repository one layer deeper in the same state: two merged, reviewed, accepted,
drift-free filings whose governing decisions are **not effective**, whose production authorization
mechanism still names the older of them, and whose authorizing predecessors are spent. Nothing in
`XASSET-0043` §F, `XASSET-0044` §L, or `XASSET-0045` §F authorizes a unit to recover from that state.

**This decision authorizes exactly one such unit and performs no part of the recovery.** It does
perform two narrow, separately principal-authorized, test-only corrections — see §K.

## Decision

### A. Determination — `POST_MERGE_CI_RECOVERY_REAUTHORIZED`

Exactly one future, separate recovery/reconciliation unit is authorized, bounded by §§F–J and
forbidden everything in §H.

This filing is **governance plus two narrow, separately principal-authorized, test-only corrections**
(§K). It performs **no** part of the recovery, edits no load-bearing implementation, no runner, no
result validator, no universe module, no canonical artifact, and no protected portfolio path, and adds
**no activation authority of any kind**.

### B. The defect, reproduced read-only before anything was authorized

The failure is **a moving test anchor**. It is neither merge drift nor outcome-surface drift, and it
is the **same defect class `XASSET-0045` itself existed to correct** — reintroduced by `XASSET-0045`
in its own new supporting artifact, one layer up from the guard it repaired.

The failing assertion sits at
**`test_level1_stage1_post_merge_ci_recovery_authorization.py:662`**, in
`TestFilingIsGovernancePlusOneEnablingCorrection::test_the_enabling_correction_was_actually_performed`.
Its subject is immutable history — *what PR #345 changed* — but it measured that subject with a
comparison whose base moves:

```python
changed = set(_git("diff", "--name-only", "origin/main").splitlines())
assert ENABLING_CORRECTION_RELPATH in changed
```

```
on the PR branch:   origin/main = f5dedce1… (PR #345's base)
                    diff -> the 12 files PR #345 changed
                    -> 'test_overlap_model_validator.py' in changed  -> assertion HOLDS

on merged main:     origin/main = 2f8cdebe… = HEAD
                    diff -> EMPTY
                    -> 'test_overlap_model_validator.py' in set()    -> assertion FAILS
```

Both branches of that table were re-derived directly from the object store in this session, and the
failure was reproduced locally at `2f8cdebe…` through the real public test, byte-identically to CI:

```
AssertionError: assert 'test_overlap_model_validator.py' in set()
test_level1_stage1_post_merge_ci_recovery_authorization.py:662
```

The immutable job log records exactly **`1 failed, 10348 passed`**, the failure isolated to that one
assertion, with steps 1–6 of the workflow green.

**A second, quieter defect of the same class was found by auditing the whole artifact rather than
only the reported line.** The immediately preceding test,
`test_no_protected_path_was_touched_by_this_filing`, used the identical moving comparison. On merged
`main` its input is likewise empty, so its protected-path claim is satisfied **without measuring PR
#345 at all** — a **vacuous pass**. It was not reported by CI because it did not fail; it could not
fail. A guard that cannot fail protects nothing, and it would have carried forward silently.

The two defects point in opposite directions from one cause, and that is the whole finding: the same
moving anchor produces a loud false failure in one assertion and a silent false success in the other.

**The guards' underlying subjects are intact.** Over the closed, immutable range
`f5dedce1d1d3116ed8a6845c4447388c85a5414c → 61e629f0f655ce8ca4ccd7eaa370d132d593515c` the enabling
correction `XASSET-0045` performed — its re-anchoring of `test_overlap_model_validator.py`, which is
the file the failing assertion names as its target — is genuinely present, and its object identities
are exact:

| `test_overlap_model_validator.py` over the closed range | |
|---|---|
| old blob at base | `5b916d881ed83db164233091863f2af87fa50828` |
| new blob at accepted head | `536bf08bb7db81ffad15dcfa1de6e9ce4fca4899` |
| status | `M` — a modification, never an addition, deletion, rename or copy |
| protected-path intersection over that range | **empty, over a 12-file non-empty input** |

The distinction matters and is stated rather than left to inference: the file **carrying** the two
defects, `test_level1_stage1_post_merge_ci_recovery_authorization.py`, was **added** by PR #345 and
has status `A` with no blob at the base; the file the corrected assertions **measure**,
`test_overlap_model_validator.py`, is the one that carries the `M` transition above. Conflating the
two would produce a proof that cannot resolve, which is how this was caught.

The properties both guards exist to enforce are therefore **true**; only the anchor they measured
against was wrong.

### C. What is not in question

Independently re-verified in this session and **explicitly outside** the recovery unit's remit to
change:

- the merge has **exactly two parents in the correct order**, base then accepted head;
- the merge tree `e5eb8905…` is **byte-identical** to the accepted-head tree — zero merge drift, and
  the accepted-head-to-merge diff is empty;
- the outcome surface is untouched: `level1_stage1_runner.py`, `level1_stage1_result_validator.py`,
  `level1_construction_universe_closure_validator.py`, every gate, disposition rule, B1/B2/B3,
  `comparison_subject_kind`, `unordered_pair_id`, and construction identity;
- the universe is **680 / 48** with aggregate `73c0965e…5224`;
- the other **10348** tests pass; no production, canonical, protected-portfolio, `intelligence/`, or
  `governance/evidence/` content is implicated.

### D. `XASSET-0045` is permanently not effective, and no later run can change that

`XASSET-0045` §M.6 requires, verbatim, *"successful merge-commit CI whose `head_sha` is the exact
merge SHA — not the PR head's own run, and not a run against any other commit."*

The exact merge SHA is `2f8cdebe14925021171b9779453946be1f69b506`. Run `32490789238` / job
`96797667282` is the merge-commit CI at that `head_sha`, and it **failed**. That commit is immutable
and its recorded history is immutable with it.

A green run at any **other** commit — a successor merge, a re-run of a different SHA, a later `main` —
is by §M.6's own words *"a run against any other commit"* and is therefore **excluded by the condition
itself**, not merely unpersuasive. No subsequent CI success anywhere can convert `2f8cdebe…`'s failure
into the success §M.6 demands.

**Run `32490789238` / job `96797667282` is immutable adverse history.** It may never be re-run in
place, relabelled successful, deleted, suppressed, waived, described as passing, or represented as
satisfying `XASSET-0045` §M.6. The stop notice
[`5371158269`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#issuecomment-5371158269) must
likewise be preserved. The failure was correctly not retried: checkout, dependency installation and
the YAML parse check all succeeded and the test body executed to completion with a deterministic
result, so no infrastructure-fault allowance reaches it.

**`XASSET-0045`'s final lifecycle closure was correctly not posted**, and must never be posted
retrospectively. Consequently `MERGE_COMMIT_CI_SUCCESS` is permanently unsatisfiable for PR #345, §M
is permanently unsatisfiable as written for that pull request, and `XASSET-0045` is **not effective
and cannot become effective through PR #345**.

The identical determination stands unchanged for its predecessor: `XASSET-0044` remains not effective,
and **its own** failed merge-commit CI run `32439614683` / job `96647501864` at merge `f5dedce1…`
remains immutable adverse history on exactly the same footing. Nothing here repairs, reinterprets, or
reopens either.

### E. `XASSET-0045` authorizes no successor unit; its requirements survive only as design input

`XASSET-0045` §F grants its recovery unit authority **"[e]ffective only on this decision's own
complete lifecycle closure (§M)"**. That closure did not occur and cannot occur (§D). The grant
therefore **never took effect**, and `XASSET-0045` authorizes no unit — not the recovery unit it
names, and not any other.

This is a different failure mode from `XASSET-0043`'s, and the distinction is load-bearing.
`XASSET-0043` §F's grant was **spent by being used**: PR #344 was that unit, opened and merged, and a
grant is consumed whether or not effectivity later completed. `XASSET-0045` §F's grant was never
spent, because it never became available to spend. Both roads end in the same place — neither
decision can supply authority to anything — but they end there for opposite reasons, and conflating
them would let a future session argue that an unspent grant is therefore still available.

Accordingly:

- **`XASSET-0043` remains spent** and may not be reused;
- **`XASSET-0044` remains not effective** and may not be treated as effective, partially effective, or
  provisionally effective;
- **`XASSET-0045` remains not effective**, authorizes nothing, and may not be cited as the authority
  for any unit.

**`XASSET-0045`'s substantive requirements are preserved as historical design input, not as effective
authority.** Its §§B–K were independently reviewed to a clean disposition and contain work worth
keeping: the moving-anchor diagnosis, the closed-range discipline, the trust-boundary reasoning, and
the successor-lifecycle-anchor requirement. This decision **restates directly, in §G, every operative
property and prohibition the authorized unit must satisfy**, so that the recovery unit derives its
obligations from **this** decision and from nothing ineffective. Where §G reaches the same requirement
`XASSET-0045` reached, that is because the requirement is right, not because `XASSET-0045` makes it
binding. A reader may consult `XASSET-0045` for reasoning; a future unit may not cite it for authority.

### F. Authority granted — exactly one future, separate recovery/reconciliation unit

Effective only on this decision's own complete lifecycle closure (§M), **exactly one** future,
separate, bounded pull request may perform the recovery/reconciliation described in §G. It is one
unit and one pull request. A future session that finds a concrete technical reason to package it
differently must **stop and disclose**, not decide it silently.

**No second unit is authorized by this decision, and completing the authorized unit does not authorize
another.**

### G. Required properties of the authorized recovery unit

Stated directly and completely here. The authorized unit **must**:

**G.1 — File its own decision.** Under the **next `XASSET-####` identifier verified unused against
live repository state at the time it is filed** — never predicted, reserved, or assumed here. This
decision deliberately names no successor identifier.

**G.2 — Preserve and independently re-prove both corrected historical guards.** The two assertions in
`test_level1_stage1_post_merge_ci_recovery_authorization.py` were repaired by **this** filing under
the separate principal authorization recorded in §K, so the future unit does **not** perform that
correction again. It must instead **preserve** them and **independently re-prove** that each still
compares the immutable closed range

```
f5dedce1d1d3116ed8a6845c4447388c85a5414c -> 61e629f0f655ce8ca4ccd7eaa370d132d593515c
```

rather than any moving base, and that neither depends on where `HEAD` or `origin/main` point when it
runs. The same obligation extends to the guard `XASSET-0045` repaired in
`test_overlap_model_validator.py` over the range
`0709d2f05ab031ecb6f69c40465ed4a227983aed → 9c2821ab9e0e0dff09f5a03da5a6034775b00750`: that repair
survives its authorizing decision's ineffectivity because it is merged repository content, and it may
not be reverted, weakened, or re-anchored to a moving reference. Re-proving means running the guards
and confirming the property from repository truth — never citing this filing's word for it.

**G.3 — Prove the merge identity.** The accepted head `61e629f0…` must be proven to be the **second
parent** of merge `2f8cdebe14925021171b9779453946be1f69b506`, with `f5dedce1…` the first, and its tree
proven **byte-identical** to the merge tree `e5eb890550d55aa74c7430871f176761526b1ecf`.

**G.4 — Continue proving the enabling correction was exactly exercised.** `XASSET-0045`'s enabling
correction to **`test_overlap_model_validator.py`** must still be proven genuinely present within that
closed range — old blob `5b916d88…`, new blob `536bf08b…`, status `M` — with each conjunct
independently required, and the protected-path intersection proven empty **over a non-empty input**.

**G.5 — Preserve every failed run as immutable adverse history.** Run `32490789238` / job
`96797667282` (`XASSET-0045`, merge `2f8cdebe…`) and run `32439614683` / job `96647501864`
(`XASSET-0044`, merge `f5dedce1…`) must both be retained, by exact identity, as failed merge-commit
CI. Neither **may ever** be relabelled successful, deleted, suppressed, re-run in place, described as
passing, or represented as satisfying its decision's own effectivity condition. Both auditable stops
must likewise be preserved.

**G.6 — Establish a lawful successor lifecycle anchor.** Production currently binds authorization
truth to `XASSET-0044` / PR #344 and to that pull request's failed exact-merge CI —
`AUTHORIZING_DECISION = "XASSET-0044"`, `AUTHORIZING_PULL_REQUEST = 344`. Because §M.6-equivalent
conditions are permanently unsatisfiable for both PR #344 and PR #345 (§D), the recovery unit must
establish a successor lifecycle anchor against **its own** decision, pull request, accepted head,
merge, successful exact-merge CI, and final closure.

**G.7 — Rebind only as strictly necessary.** The operational-authorization mechanism may be rebound
**only** to the extent the successor lifecycle anchor requires. No unrelated configuration, identity,
threshold, gate, or evidence requirement may be changed under cover of the rebinding, and the
mechanism may not be made more permissive in any respect.

**G.8 — Preserve the predecessor evidence as independently authenticated.** For PR #345: the accepted
head, the merge, the zero-drift tree, the final clean review `4993994386`, the principal acceptance
`5370936620`, the post-merge verification `5370989769`, the failed CI run/job, and the stop notice
`5371158269`. For PR #344: the corresponding record its own predecessor filing preserved. All must be
retained and labelled, never erased, overwritten, or silently re-pointed.

**G.9 — Preserve every outcome-producing semantic.** The runner, the result validator, the
construction-universe membership, order, and aggregate hash `73c0965e…5224`, the canonical inputs, all
protected paths, and every valid actor-evidence correction must be preserved unchanged.

**G.10 — Use exact closed transitions for every lawfully changed load-bearing byte.** Any guard that
asserts historical byte identity must do so against a closed, immutable commit range. **No moving
`HEAD`/`origin/main` guard may claim historical byte identity** — the exact defect this decision
exists to remedy must not be reintroduced anywhere, in any file, at any layer.

**G.11 — Audit for the defect class rather than for the reported symptom.** A historical claim
anchored to a moving reference fails loudly in one direction and passes vacuously in the other, and
only the loud direction reaches a CI log. Before relying on any assertion about immutable history, the
unit must classify every use of `HEAD`, `origin/main`, `merge-base`, and any working-tree comparison in
the files it touches by whether that use's **subject** is live state or immutable history, and
re-anchor every historical one. Fixing only the assertion a failure names is not sufficient.

**G.12 — Complete a full lifecycle.** Independent **FULL** exact-head review under `OPS-0007` §1;
any required bounded correction and exact-head re-review; explicit principal exact-head acceptance;
normal merge; immediate post-merge verification; **successful merge-commit CI at the future recovery
merge SHA**; and final post-CI closure.

**G.13 — Weaken nothing.** No existing assertion may be deleted, skipped, `xfail`ed, weakened, or
replaced with a less falsifiable one. Guards may be re-anchored and strengthened; they may not be
relaxed. A guard rewritten into a shape that still runs while proving less — a defaulted lookup, a
hard-coded empty input, a bound every input satisfies — is a weakening, not a re-anchoring.

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

It may **not** reuse `XASSET-0043`, reuse `XASSET-0045`, treat `XASSET-0044` or `XASSET-0045` as
effective, re-open `ATTEMPT_1`, revive `XASSET-0040` (which stays spent as
`STOPPED_BEFORE_ATTESTATION`), or consume `XASSET-0027` §P.1 (which remains one and unspent).

`stage_1_executability.executable` stays permanently `false`. **No committed value in this repository
authorizes Stage-1 execution**, and this decision adds none.

### I. Fail-closed

Every unobtainable fact is an **error**, never silent agreement. If the recovery unit cannot
independently verify the merge parentage, the tree identity, the closed-range transition, either
failed run's identity, or its own lifecycle evidence, it must **stop and disclose** rather than
proceed, assume, or downgrade the requirement. Ambiguity, drift, or any condition that would require
expanding this authority is a **stop**, not a judgement call.

### J. Packaging and evidence

One coherent draft pull request, carrying its own decision record and the recovery in one unit, with
its own adversarial mechanism-based supporting artifact, catalog and `WS-0014` register
synchronization, and full verification evidence. It must not self-review, self-accept, mark itself
ready, merge itself, or post its own lifecycle closure.

### K. Scope of this filing — governance plus two narrow, separately authorized corrections

This filing is **not** purely design-only, and does not claim to be.

It performs **two** narrow, **test-only** corrections, both in
`test_level1_stage1_post_merge_ci_recovery_authorization.py` and both re-anchored from
`git diff --name-only origin/main` to the immutable closed range `f5dedce1…` → `61e629f0…`, together
with the merge's exact two-parent ordering, byte-identical accepted-head/merge trees, the enabling
correction's exact status and both blob ends, and a non-empty-input requirement so the protected-path
claim can no longer be satisfied by measuring nothing.

**The authority for those corrections is not created by this decision.** `XASSET-0046` cannot
authorize its own enabling repair without circularity, and does not attempt to: an ineffective
`XASSET-0045` cannot supply it either, and a decision that granted itself the repair its own
effectivity depends on would be exercising authority it minted in the same document. The authority is
a **separate, explicit principal authorization**, given after run `32490789238` failed and the
lifecycle stopped, and covering exactly these two historical-proof corrections and this governance
replacement. Every other scope limit and every Stage-1 prohibition remained, and remains, fully
operative.

The corrections are **strictly narrowing in effect**: every conjunct the previous guards proved is
still proved, and the parent-ordering, tree-identity, status, blob-identity, and non-vacuity proofs are
new. Nothing was deleted, skipped, `xfail`ed, weakened, or replaced with a less falsifiable assertion.
One further audit finding is disclosed and corrected in the same narrowing direction: a leftover
`origin/main` skip guard on a historical proof whose own computation was already fully pinned, removed
so that a historical proof can no longer be silenced by where a live reference points.

Beyond those test-only corrections, this filing still edits **no** load-bearing implementation, no
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

### N. This filing can attain both green PR-head and green merge-commit CI

Condition §M.6 is only meaningful if it is attainable. `XASSET-0045` failed that test twice over: at
its first reviewed head it required successful merge-commit CI while simultaneously declaring that CI
impossible, and after that deadlock was corrected it merged carrying a fresh assertion that could not
survive its own merge. Both were the same error — a filing whose own effectivity condition its own
contents made unreachable.

This filing states the condition and demonstrably meets it. Its two corrected proofs read **no**
moving reference at all: every anchor is an immutable object identity, verified from the git object
store. That is not merely asserted — it is proved three ways in the supporting artifact:

- **structurally**, by a shared detector that refuses any moving-reference literal inside a declared
  historical proof, exercised against known-bad and known-good synthetic source so that disabling it
  fails its own falsifiability test rather than silently reporting clean;
- **behaviourally**, by running the corrected proofs for real under **five** simulated repository ref
  states — a feature branch, merged `main`, a later `main`, `HEAD` equal to a later `origin/main`, and
  unrelated later commits — each built inside an **isolated clone**, never a `git worktree`, which
  shares the ref namespace;
- **adversarially**, by mutation probes covering the restored moving comparison, each wrong anchor,
  reversed parent order, tree drift, wrong status, either wrong blob end, an unexercised allowance, a
  hollowed-out assertion, a disabled or unreachable detector, and a removed invariance scenario.

A **combined non-deadlock guard** refuses the conjunction directly: this decision may not both require
successful exact-merge CI and contain any claim that its own CI cannot succeed. The guard is
non-vacuous — satisfying it by dropping the successful-CI requirement instead is itself a failure.

**A red exact-head or merge-commit CI result is a stop, not an accepted deviation.** §M.6 is unchanged
and remains fully required. Nothing here retroactively repairs PR #345's or PR #344's own failed
merge-commit CI: runs `32490789238` / job `96797667282` and `32439614683` / job `96647501864` remain
immutable adverse history (§D, §G.5), `XASSET-0045` and `XASSET-0044` remain not effective, and
`XASSET-0043` remains spent.

## Rationale

The mechanism worked, twice. `MERGE_COMMIT_CI_SUCCESS` went unsatisfied, final closure was correctly
not manufactured, and Stage 1 stayed unarmed with `ATTEMPT_1` untouched. The correct response to a
fail-closed stop is a **separately authorized** recovery unit, not an improvised repair inside a
lifecycle operation that has no authority to edit files.

Authority for that unit had to come from somewhere. `XASSET-0043`'s single grant is spent,
`XASSET-0044` is not effective, and `XASSET-0045`'s grant never became available (§E), so no existing
decision could carry it. Filing a narrow replacement authorization is the smallest lawful step that
unblocks the recovery without deciding it.

What is genuinely new here is not the authorization — that shape is `XASSET-0045`'s, and it was right.
It is the finding in §B. `XASSET-0045` corrected a moving-anchor guard and, in the same pull request,
wrote two more. Its reviews were thorough: three rounds, two BLOCKING findings, both of this exact
class, both corrected. The class still survived, in a file the reviews had read, because each round
asked whether the *reported* defect was fixed rather than whether the *defect class* was absent.

That is why §G.11 exists, and why this filing audited the whole artifact instead of line 662. The
second defect it found had never failed anything and never would have: it was a claim satisfied by
measuring nothing. A guard that fails loudly gets fixed; a guard that passes vacuously gets trusted.
The second is the more expensive of the two, and it was one line away from the first.

The same reasoning shaped the verification. A prose prohibition against moving anchors is what
`XASSET-0045` §G.10 already contained, and it did not prevent this. So the prohibition is mechanical
here: a detector that refuses the shape, proved falsifiable against synthetic source, and a regression
that runs the corrected proofs in the ref state that actually broke them. Mutation testing found three
probes surviving on the first pass — each a named guard hollowed out while a sibling test independently
re-derived the same fact — and those were closed at the shape level rather than by adding a fourth
redundant re-derivation. Redundancy keeps a suite honest; it does not keep a *guard* honest.

Separating authorization from execution also preserves reviewability: the recovery's own decision, PR,
review, acceptance, merge, CI, and closure are all still ahead of it, each independently gated. Nothing
here shortens that chain, and nothing here touches the outcome surface.

## Alternatives Considered

**Post `XASSET-0045`'s lifecycle closure anyway, since only one test failed.** Rejected outright. §M
is conjunctive and says in terms that none of its conditions is individually sufficient; the sixth
failed. Closing on six of seven would rewrite an accepted effectivity condition to accommodate its own
failure, which is precisely the class of move the fail-closed design exists to prevent.

**Re-run the failed CI job.** Rejected on the condition's own words: §M.6 names the exact merge SHA and
excludes runs against any other commit; a re-run cannot alter the recorded failure of run
`32490789238`, and treating a re-run as satisfaction would rewrite adverse history. The failure was
also not an infrastructure fault — the test body executed to completion and returned a deterministic
result — so no retry allowance reaches it.

**Amend `XASSET-0045` §M to accept a later run, or edit `XASSET-0045` to remove the failing test.**
Rejected. `XASSET-0045` is merged, independently reviewed, accepted history. Editing it to make its own
failure disappear is the same move as the previous alternative wearing different clothes.

**Treat `XASSET-0045` §F's grant as still available because it was never used.** Rejected, and this is
the subtlest temptation available here. §F's grant is conditioned on complete lifecycle closure, which
did not occur; an unspent grant that never vested is not a grant in reserve. §E states the distinction
between `XASSET-0043`'s spent-by-use grant and `XASSET-0045`'s never-vested one precisely so that a
future session cannot reach for the second by analogy to the first.

**Cite `XASSET-0045` §G for the recovery unit's obligations and file only the delta.** Rejected. An
ineffective decision cannot bind a future unit, and a filing that incorporated it by reference would
build the recovery's obligations on an authority that does not exist. §G therefore restates every
operative property directly, at the cost of length, and `XASSET-0045` survives as reasoning a reader
may consult rather than authority a unit may cite.

**Correct only the assertion CI reported.** Rejected — it was the first thing this session tried to
scope, and auditing the file rather than the line is what found the vacuous sibling. Fixing the loud
half of a symmetric defect and leaving the silent half is how this class survived three reviews
already.

**Repair the guards by loosening them** (skip, `xfail`, delete the assertions, or relax the status
filter). Rejected outright: the properties are sound and were never the problem; only their anchor
moved. Loosening would trade a false-red for a false-green and destroy exactly the protection the
guards exist to provide.

**Perform the recovery in this filing, since the authorization keeps failing to take effect.**
Rejected. Two stopped lifecycles are an argument for more care about effectivity, not for collapsing
authorization into execution. §N addresses the real problem — a filing whose own contents made its
effectivity condition unreachable — mechanically, rather than by removing the condition.

## Consequences

On this decision's complete lifecycle closure, exactly one future recovery/reconciliation unit becomes
authorized to begin, bounded by §§F–J and forbidden everything in §H. Until then it may not be opened,
drafted, or begun.

`XASSET-0045` remains not effective and authorizes nothing. `XASSET-0044` remains not effective.
`XASSET-0043` remains spent. Run `32490789238` / job `96797667282` remains the failed merge-commit CI
for `2f8cdebe…`, and run `32439614683` / job `96647501864` remains the failed merge-commit CI for
`f5dedce1…`, permanently. `XASSET-0027` §P.1 remains one and unspent. `XASSET-0040` remains spent as
`STOPPED_BEFORE_ATTESTATION`.

Stage 1 remains **UNARMED and NOT EXECUTABLE**, the lane **ABSENT**, `ATTEMPT_1` intact, unclaimed and
unconsumed, and no `stage1_results.yaml` exists anywhere in the repository.
