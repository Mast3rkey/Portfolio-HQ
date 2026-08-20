---
decision_id: XASSET-0044
date: 2026-08-20
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_correction_rebinding.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all
matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `0709d2f05ab031ecb6f69c40465ed4a227983aed` |
| Worktree / worktrees / mutation lane | clean; exactly one worktree; no competing lane |
| Open pull requests | **zero** |
| PR #343 | merged and closed, `merged_by` `Mast3rkey`, base `5fbfc94d…`, accepted head `8e9d65ff…`, merge `0709d2f0…`, 9 files, 2 commits |
| PR #343 merge parents | exactly two, in order: `5fbfc94d7333e552bd2654261e0c57134a172e31`, then `8e9d65ffa40991fade92b60f72f833501ce799d9` |
| PR #343 merge drift | **zero** — merge tree `b9b717d729748b1ad3ed30bac0442afd9605e43e` byte-identical to the accepted head's tree |
| PR #343 review chain | FULL [`4976985695`](https://github.com/Mast3rkey/Portfolio-HQ/pull/343#pullrequestreview-4976985695) at `b266f8c2…` (CHANGES REQUIRED, 2 MAJOR / 1 MINOR) → bounded correction → FULL [`4979065535`](https://github.com/Mast3rkey/Portfolio-HQ/pull/343#pullrequestreview-4979065535) at the exact accepted head, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0/0/0 |
| Principal acceptance | [`5351676579`](https://github.com/Mast3rkey/Portfolio-HQ/pull/343#issuecomment-5351676579) — durable `user.login` **`Mast3rkey`** |
| Post-merge verification | [`5352255915`](https://github.com/Mast3rkey/Portfolio-HQ/pull/343#issuecomment-5352255915) |
| Merge-commit CI | run [`32334941721`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32334941721) / job `96322563522` — `completed`/`success`, `event: push`, attempt 1, `head_sha` **the exact merge SHA**; queried every run at that SHA: exactly one exists, and it succeeded |
| Lifecycle closure | [`5352262629`](https://github.com/Mast3rkey/Portfolio-HQ/pull/343#issuecomment-5352262629) |
| `XASSET-0043` | **EFFECTIVE** — all seven §N conditions independently confirmed closed |
| Baseline suite before any edit | **9931 passed, 0 failed**, one pre-existing unrelated `DeprecationWarning` |
| `LOAD_BEARING_RELPATHS` at filing | **10**; `AUTHORIZING_DECISION` `XASSET-0037`; `AUTHORIZING_PULL_REQUEST` `337` |
| Lane state | exactly **`ABSENT`**; `AUTHORIZATION_ROOT` absent |
| `new_execution_is_authorized()` | **`False`** |
| `ATTEMPT_1` | **intact, unclaimed, unconsumed** |
| `stage1_results.yaml` | **absent** anywhere on the filesystem |
| `XASSET-0044` identifier | **unused** — the only two repository occurrences are a negative guard inside `XASSET-0043`'s own suite asserting no successor identifier may be *reserved*; no decision file, no catalog entry |

Read in full before designing: `XASSET-0043` (all of §§A–N), `XASSET-0042` (§§G–I and both bounded
corrections), `XASSET-0041` §I, `XASSET-0037` §§C–J, `XASSET-0030` §D and §G.B, `OPS-0001`,
`OPS-0007` §1, and `OPS-0009`.

### The question this unit answers

`XASSET-0043` §F authorizes **exactly one** future, separate, bounded rebinding unit, and performs
no part of it. This is that unit. It is not a further authorization: it files its own decision and
performs the rebinding in the same coherent pull request, exactly as §F requires and exactly as
`XASSET-0037` was both.

## Decision

### A. Determination — `POST_CORRECTION_REBINDING_PERFORMED`

The corrected load-bearing implementation merged by PR #342 is lawfully bound. The effective
structural authorization source, `AUTHORIZING_PULL_REQUEST`, and `REVIEWED_BASE_SHA` are rebound to
this unit's own verified identities; the trust boundary grows from ten paths to fourteen by direct
membership; the derivation surface gains a second exact closed transition, appended; the canonical
artifacts are amended in authorization language only, in lockstep; and the `XASSET-0042`
current-identity evidence is explicitly resolved.

**Stage 1 is not armed by this.** It becomes *armable* against the corrected implementation and
nothing more. Links 3, 4, and 5 of `XASSET-0041` §I each still require their own separate authority
and their own complete lifecycle (§I).

### B. The drift this resolves, reproduced read-only before anything was edited

Each of the ten load-bearing paths was compared, **from the git object store only**, between its
working-tree bytes and the same blob in the bound `XASSET-0037` merged tree — PR #337's merge
`637eaa30302f5a71f84ab1d215ecbd32c01399b5`. **Exactly one drifted**, and it is precisely the one
`XASSET-0042` was authorized to correct:

| Path | Bound merged tree | Working tree | Status |
|---|---|---|---|
| `level1_stage1_execution_authorization.py` | `8186a50f…d91f2fc8` | `749597ee…b50f24c7` | **drift** |
| the other nine | unchanged | unchanged | match |

`XASSET-0030` §D recorded that consequence in advance. The reproduction was performed at the
git-object level only: **no lane was created, inspected, or touched; `write_authorization` was never
called; `AUTHORIZATION_ROOT` was not created; and no part of the authorized step-9 readiness
verification or step-10 drift check was performed.**

### C. `XASSET-0030` §G.B step 8 is not consumed a second time

Step 8 authorized **one** rebinding against the executable package's exact merged bytes, and
`XASSET-0037` performed it. That budget stays spent and the package it bound stays bound. The
authority exercised here is:

1. **`XASSET-0030` §D** — a general provision for "a successor operational-authorization **or
   reconciliation lifecycle**" whenever a lawful correction of load-bearing code creates enforcement
   drift;
2. **`XASSET-0041` §I link 2** — which names the required next link as step-8 ***equivalent***: the
   same kind and rigour, separately authorized, not a second draw on step 8's own budget;
3. **`XASSET-0043` §F** — the separate governance decision that grants it.

`XASSET-0037` is preserved, not invalidated, exactly as it preserved `XASSET-0029`. Its six-gate
lifecycle really closed and remains valid accepted history. What changed is only **which merged tree
the mechanism proves load-bearing identity against**.

### D. The fifth relationship, in its own constants

`XASSET-0037` §C answered the largest failure mode available to a rebinding — overloading one
identity across relationships that are not the same relationship — with four separately named
identity families. This rebinding adds a fifth and keeps the same discipline. None of the following
is interchangeable with any other, and none is folded into `EXECUTABLE_PACKAGE_*` or
`HISTORICAL_OPERATIONAL_AUTHORIZATION_*`:

| Family | Identity | Verified from git |
|---|---|---|
| `PRIOR_SUCCESSOR_REBINDING_*` | `XASSET-0037` / PR #337 | merge `637eaa30…`, head `f40c8162…`, base `3e5de8f8…` |
| `CORRECTION_AUTHORIZING_*` | `XASSET-0041` / PR #341 | merge `9c8647f9…` |
| `CORRECTED_MODULE_*` | `XASSET-0042` / PR #342 | merge `5fbfc94d…`, head `4d5d99d6…`, base `9c8647f9…` |
| `REBINDING_AUTHORIZING_*` | `XASSET-0043` / PR #343 | merge `0709d2f0…`, head `8e9d65ff…`, base `5fbfc94d…` |

Every one of those merges was independently confirmed to have exactly two parents in order, a merge
tree **byte-identical** to its accepted head's tree — zero merge drift, proven rather than asserted —
and ancestry into this rebinding's own merge. `PREDECESSOR_*` (`XASSET-0028`, structural closure)
is deliberately **untouched** in name, meaning, and value.

`REVIEWED_BASE_SHA` equals `REBINDING_AUTHORIZING_MERGE_SHA`, and the module states that as an
equality rather than leaving it to coincidence: a rebinding branched from anywhere else has not
actually waited for `XASSET-0043`'s lifecycle to close.

### E. The trust boundary: 10 → 14, direct membership, nothing removed

`XASSET-0037` §E's principle is that the decision supplying the effective structural authorization
must sit inside the identity it authorizes, or an attestation could authenticate perfectly while its
own governing text had been edited afterwards. Applied honestly that reaches **four** files here,
because after this rebinding four decisions jointly make the corrected bytes lawful:

| File | Why it is in the chain |
|---|---|
| `XASSET-0041-…-correction-authorization.md` | authorized the actor-evidence correction |
| `XASSET-0042-…-correction.md` | implemented it, and records the corrected module's identity |
| `XASSET-0043-…-rebinding-authorization.md` | the authority for this rebinding |
| `XASSET-0044-…-operational-rebinding.md` | this decision — the effective source after it |

**Direct membership, not an equivalent.** Each joins `LOAD_BEARING_RELPATHS` and is verified by the
existing exact-byte mechanism, whose expected identity is derived from the merged git tree at
validation time. Citing `XASSET-0041` or `XASSET-0042` inside this decision would **not** be a
binding of those files, and no substitute binding is adopted.

No path is removed, exempted, made conditional, or excluded from any comparison. The pin-succession
refusal is **extended** to `XASSET-0037`'s own accepted pins, never relaxed.

### F. The derivation surface: a second exact closed transition, appended

`XASSET-0043` §G.4a's requirement was reproduced rather than taken on trust. With the frozen module
in place, advancing only the successor-lifecycle authorization language §J permits and §F.2 requires
produced exactly the predicted failures — `rebound_by`, `effective_structural_authorization_source`,
and `stage_1_executability.blocking_prerequisite` all rejected, because the module hard-codes
`XASSET-0037` in precisely the fields a successor must advance.

Therefore, and only for `level1_endpoint_evidence_preregistration_validator.py`:

1. The accepted successor blob `2b8ead2b…deb3d356` and the **existing 17-region
   package-to-successor transition are preserved** as historical anchors and accepted history.
   Neither is deleted, edited, re-derived, or weakened.
2. A **second exact closed transition is appended** — successor → rebound, **23 regions** — computed
   only after every permitted byte had stabilized. The chain is now
   `package → successor → rebound`, each link a separate frozen manifest.
3. Every region records exact source and target offsets, exact lengths, and the SHA-256 of the bytes
   it replaces and the bytes it installs.
4. Every byte outside a declared region is byte-identical, both blobs are consumed completely, and
   no gap, overlap, duplicate, reordering, resizing, addition, or removal is tolerated.
5. Every region lies inside the authorization-only surface: successor-lifecycle constants, canonical
   validation of those constants, pin succession, and rebinding-block validation.
6. The consumer-reachable and outcome-producing definitions are **re-proved unchanged** —
   semantically and byte-identically — in the supporting suite, derived from the consumers' own
   source rather than asserted.
7. No runner, result-validator, universe, construction, gate, disposition, scoring, portfolio, or
   protected-`RISK` behaviour changes. `level1_stage1_runner.py`,
   `level1_stage1_result_validator.py`, and `level1_construction_universe_closure_validator.py` are
   **byte-identical**, with no transition and no exception.

Link 1's own verification is not weakened — it is re-anchored to the commits that actually carry its
bytes, `XASSET-0037`'s accepted head and merge, which are immutable history. Both links must hold.

**The authorization boundary remains bytes.** No AST interpretation, no import or execution of the
audited module, no `eval`, and no version-dependent diff algorithm participates in the
authorization; the manifests are frozen constants verified by comparison only.

### G. Canonical amendment — authorization language only, in lockstep

`PROTOCOL_V1.md` and `pre_registration.yaml` are amended **only** in successor-lifecycle
authorization language: the fields naming the currently effective lifecycle, `rebound_by`,
`effective_structural_authorization_source`, the successor-rebinding record, and the
`must_bind_exactly` / `must_fail_closed_on` entries. **`established_by: XASSET-0029` stays** —
historical truth is not rewritten — and every superseded value is retained in an explicitly
predecessor-named field.

Every substantive thing is **unchanged**: the runner and result validator byte-identical, the
universe module unchanged, and every gate, disposition rule, B1/B2/B3, `comparison_subject_kind`,
`unordered_pair_id`, construction identity, and membership/ordering/cardinality untouched — with the
aggregate universe hash `73c0965e…5224` independently regenerated after the amendment and unchanged
at **680** / **48**. `stage_1_executability.executable` stays `false`.

### H. The `XASSET-0042` current-identity evidence — resolved by retirement, and why

`XASSET-0043` §I.2 permits either amendment or retirement-with-equivalent-replacement, and requires
the choice to be argued rather than assumed. **This unit takes (b), retirement.**

The reason is that the declaration's own name states what it is: `FINAL_CORRECTED_MODULE_SHA256` is
the identity of the module **as the `XASSET-0042` correction left it**. That is a true statement
about a closed unit. Amending it to a post-rebinding digest under option (a) would make `XASSET-0042`
claim to have produced bytes it never produced — trading a stale reading for a false one. Retirement
keeps every historical statement true and moves only the *role*.

Accordingly:

* **`XASSET-0042`'s declaration line and its digest `749597ee…` are left byte-unchanged.** Only the
  surrounding prose is re-anchored, additively, to say that the value describes the module at the
  close of the `XASSET-0042` lifecycle rather than in perpetuity, and to point at where the current
  identity now lives.
* **The current-identity role moves here.** This decision carries the single machine-readable
  `CURRENT_MODULE_SHA256:` declaration below, checked against the production module's real bytes by
  an equivalently strong guard in this unit's own suite.
* **No prior identity is dropped or conflated.** The bound `8186a50f…`, the intermediate superseded
  head `03d84212…`, `XASSET-0042`'s final `749597ee…`, and the current value are all retained, all
  labelled, and all mutually distinct.
* **`XASSET-0042`'s statements that its own unit re-pinned nothing remain true of that unit** and are
  not deleted. They are not a claim about the repository's state after this separately authorized
  rebinding, and this decision says so explicitly rather than leaving a reader to infer it: **this
  unit did re-pin, and was authorized to.**
* **The guard is re-anchored, never weakened.** Its three module-digest-coupled assertions are
  re-pointed at the truths they were meant to express — the declaration against the module's bytes
  **at the closed `XASSET-0042` anchor**, and the "this correction did not edit the module" check
  against the **closed commit range** it actually describes rather than a moving `HEAD`. Nothing is
  deleted, `skip`ped, `xfail`ed, or relaxed, and no replacement asserts less than what it replaces.

```
bound (XASSET-0037 merged tree, historical)          sha256  8186a50f71d05bbb7189183bacad6aa0752147e9c7f4e1f5b3bacabad91f2fc8
intermediate, superseded head 7573147e (historical)  sha256  03d842126913bf2d62aa5d7c070ecca236926ec847102da82414ee51e7422734
XASSET-0042 final, closed at PR #342 (historical)    sha256  749597ee9085a189e187e23ccffb7718d98860847dfe514c173e7437b50f24c7
CURRENT_MODULE_SHA256: c27437dc67f76254f00af57cc0d783c88181e0a18417281a6c8dcd3e6fb84047
```

### I. Authority withheld — absolute

This decision does **not** perform and does **not** authorize:

- `XASSET-0030` §G.B steps 9, 10, or 11, in whole or in part;
- any renewed readiness verification or renewed post-rebinding drift check;
- generating any external attestation;
- creating `AUTHORIZATION_ROOT`, any lane path, or `READY` / `CLAIMED` / `COMPLETED` lane state or
  any ledger entry;
- arming, claiming, completing, executing, or recovering any Stage-1 execution;
- consuming any part of `ATTEMPT_1`;
- evaluating any gate for any registered construction, or asserting any per-construction outcome;
- creating `stage1_results.yaml` or any disposition, cell outcome, or roll-up;
- changing any construction identity, universe membership, ordering, cardinality, or universe hash;
- reviving `XASSET-0040`, which remains spent as `STOPPED_BEFORE_ATTESTATION`;
- consuming `XASSET-0027` §P.1's reserved results PR, which stays **one, unspent**;
- reopening, re-deriving, or re-arguing B1, B2, or B3, or any gate semantics;
- resolving `XASSET-0024` §K.1, or amending `XASSET-0020` §E.1;
- any Stage 2 work, evidence acquisition, or market, fundamental, or economic data acquisition;
- reading, listing, opening, or referencing any `risk_lane_boundary` protected `RISK` result path;
- weakening any validator or test;
- creating any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  tier, cluster, cap, or margin state;
- authorizing any chart, ladder, deployment, trade, order, or brokerage action;
- authorizing any successor unit of any kind;
- rewriting any accepted history.

**Completing this rebinding authorizes the next link no more than a clean step-10 result authorized
step 11** — the inference `XASSET-0039` §K already foreclosed.

### J. Not an activation, and the regress is untouched

`XASSET-0029` §E terminates the activation regress on a step that **changes no repository state** —
the external runtime attestation. A rebinding changes repository state extensively, so it is
categorically outside the step §E terminates. **This adds one rebinding and ZERO activation
authorizations.** `stage_1_executability.executable` stays `false` permanently and keeps its
enforced-false check. **No committed value in this repository authorizes Stage-1 execution**, and
merging this decision does not change that. Final activation remains the external one-shot runtime
attestation and the operator's act — never another merged pull request.

### K. Fail-closed

Every condition above is conjunctive. An anchor that cannot be read, an identity that cannot be
reproduced, a path that cannot be matched, a guard that cannot be re-anchored without weakening, or
a canonical regeneration that does not return 680 / 48 and `73c0965e…5224` is a **stop and
disclose**, not a partial result, an exclusion, or a repair outside this unit's authorized scope. An
unobtainable anchor is never treated as agreement.

### L. Effectivity

This rebinding becomes effective **only** after **all** of the following are complete for this
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

**Merging this does not arm Stage 1, creates no lane state, claims no `ATTEMPT_1`, and executes
nothing.** Immediately after it merges, `new_execution_is_authorized()` still returns `False` and the
lane is still `ABSENT`, because arming requires an external attestation that does not exist and
cannot be pre-staged.

<!-- XASSET-0044-HASH-PINS-V1
protocol_path: research/level1_endpoint_evidence/PROTOCOL_V1.md
protocol_sha256: 1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84
preregistration_path: research/level1_endpoint_evidence/pre_registration.yaml
preregistration_sha256: 898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f
predecessor_protocol_sha256: 367583b616e1c6ab614bcf67d451fe27ce40507d073374190c57291e761d8971
predecessor_preregistration_sha256: 768b013c0129f02577fea3c2a1a3100b4340b9a42f48ee0d0dbd6e671894bce1
-->

- `PROTOCOL_V1.md`: `1ad1d060d5bf970288844b05b94e1fd38c3cc9cc87afc1481a45ed1b315d0c84`
- `pre_registration.yaml`: `898c329d9941c5c24ff2a800f842e860c63e2e500acc4257eb14646c1012d82f`

`XASSET-0037`'s accepted pins — `367583b6…1d8971` and `768b013c…894bce1` — are retained as
predecessor identity, verified verbatim rather than against the live files, and are **not** rewritten
to match the amended bytes.

## Rationale

The correction worked and it cost exactly what `XASSET-0030` §D said it would. Paying that cost is
this unit's whole job, and the two ways to pay it badly were both available.

The first is **collapsing links**. Holding a merged correction, a single visible drift, and a
mechanism one understands well, it is one short inference from rebinding to re-verifying readiness to
re-checking drift to arming. `XASSET-0041` §I foreclosed that in advance and `XASSET-0039` §K
foreclosed its general form. This unit rebinds and stops, and §I says so in the same words its
predecessors used, so the boundary does not depend on a future session's restraint.

The second is **binding the wrong thing**. The temptation is to reuse an existing identity family
rather than mint a fifth, because the corrected module *feels* like part of the package. It is not:
the package is a merged tree from PR #336, and the corrected module is a different merged tree from
PR #342 with a different authority behind it. `XASSET-0037` §C's anti-overloading rule is what keeps
those apart, and §D applies it rather than restating it.

§H is where this unit had the most room to be lazy. A guard was always going to fail here — that was
designed, and `XASSET-0043` §I named it in advance precisely so it would not be discovered under
pressure to get a suite green. The honest resolution costs more than deleting an assertion and more
than overwriting a digest, and it is the one that leaves every historical statement true.

Finally, §C's precision about step 8 is deliberate. Describing this as "step 8" would inherit a
tidier authority than this unit actually has. Step 8 was spent. What authorizes a further rebinding
is §D's reconciliation clause, `XASSET-0041` §I link 2's own word *equivalent*, and `XASSET-0043` —
a narrower claim, and one a reviewer can check against accepted text rather than against this
filing's confidence.

## Alternatives Considered

**Amend `XASSET-0042`'s declaration to the new digest (§I.2 option (a)).** Rejected. The line is
named `FINAL_CORRECTED_MODULE_SHA256` and means the module as that correction left it. Repointing it
at bytes produced by a later, separately authorized unit would make an accepted decision assert
something it did not do. Option (b) moves the role and leaves every historical statement true.

**Leave the canonical artifacts alone and rebind only the module.** Rejected as producing a false
record: `effective_structural_authorization_source` would keep naming `XASSET-0037` after it had
ceased to be the effective source. `XASSET-0043` §F.2 requires the rebinding, §J permits exactly this
amendment, and §G.4a exists because the two must move together.

**Freeze the derivation module whole-file and skip the canonical amendment.** Rejected — and not on
preference: it was reproduced as *impossible*. The frozen module hard-codes `XASSET-0037` in the
exact fields a successor must advance, so keeping the blob and telling the truth are not jointly
satisfiable. §G.4a's appended transition is the only mechanism `XASSET-0043` permits, and it is what
this unit used.

**Replace the 17-region transition with a single package→rebound manifest.** Rejected. It would
discard the reviewed link `XASSET-0037` accepted and re-derive a claim no review had seen. Appending
keeps both links separately provable and preserves accepted history, which is what §G.4a requires.

**Bind fewer than four decision files.** Rejected on `XASSET-0037` §E's own reasoning, which
`XASSET-0043`'s independent review applied directly: any of the four left outside the boundary stays
editable after an attestation has authenticated. Citing a predecessor is not byte-binding it.

**Split the decision and the rebinding into two pull requests.** Rejected — `XASSET-0043` §F requires
one coherent unit, and splitting would create a decision whose bound bytes do not yet exist and a
rebinding whose governing text is not yet inside the identity it binds.

## Consequences

**Stage 1 is now armable against the corrected implementation — never armed.** The lane is `ABSENT`,
`new_execution_is_authorized()` returns `False`, `ATTEMPT_1` is intact and unconsumed, and no
`stage1_results.yaml` exists. Arming requires an external attestation that does not exist, cannot be
pre-staged, and is not a pull request.

**The enforcement drift in §B is resolved.** The mechanism now proves load-bearing identity against
the merged tree that actually carries the corrected bytes, across fourteen paths rather than ten.

**Links 3, 4, and 5 remain unauthorized.** Each still requires its own separate authority and its own
complete lifecycle, and this unit's completion supplies none of it.

**If a future correction of load-bearing code is ever authorized again, this same cost recurs** —
by design. That is `XASSET-0030` §D working, not a defect to engineer away.
