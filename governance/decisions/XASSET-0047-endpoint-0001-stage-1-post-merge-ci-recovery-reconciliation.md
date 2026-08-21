---
decision_id: XASSET-0047
date: 2026-08-21
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_merge_ci_recovery_reconciliation.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all
matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` |
| Worktree / worktrees | clean; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #346 | `merged: true`, `state: closed`, merged by `Mast3rkey` at `2026-08-21T17:15:37Z`, 12 files, 6 commits |
| PR #346 base / accepted head | `2f8cdebe14925021171b9779453946be1f69b506` / `0964dc2bd6ab3be8282193f76fa04c764198db0f` |
| Merge parents, in order | `2f8cdebe…`, then `0964dc2b…` |
| Merge tree / accepted-head tree | both `a2a05c8308b3d6efe27e2517d0859934c65660a6` — **zero merge drift** |
| Superseded FULL review | [`4995297886`](https://github.com/Mast3rkey/Portfolio-HQ/pull/346#pullrequestreview-4995297886) @ `243dec3b…` — 1 BLOCKING |
| Final clean DELTA review | [`4995648329`](https://github.com/Mast3rkey/Portfolio-HQ/pull/346#pullrequestreview-4995648329) @ `0964dc2b…` — 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE |
| Principal acceptance | [`5372996734`](https://github.com/Mast3rkey/Portfolio-HQ/pull/346#issuecomment-5372996734) @ `0964dc2b…` |
| Post-merge verification | [`5373011071`](https://github.com/Mast3rkey/Portfolio-HQ/pull/346#issuecomment-5373011071) |
| Merge-commit CI | run [`32507225897`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32507225897) / job `96849995233` — `event: push`, attempt 1, run **and** job `head_sha` each `0b76c09f…`, `completed` / **`success`**, `10504 passed` |
| Final lifecycle closure | [`5373106008`](https://github.com/Mast3rkey/Portfolio-HQ/pull/346#issuecomment-5373106008) — posted strictly after both |
| **`XASSET-0046`** | all seven §M conditions closed — **EFFECTIVE** |
| `AUTHORIZING_DECISION` / `AUTHORIZING_PULL_REQUEST` before this unit | `XASSET-0044` / `344` |
| `LOAD_BEARING_RELPATHS` before this unit | **14** |
| Universe | **680** constructions over **48** cells, aggregate `73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` |
| Lane | **ABSENT** — `AUTHORIZATION_ROOT` does not exist |
| `new_execution_is_authorized()` | `False` |
| `stage_1_executability.executable` | `false` |
| `ATTEMPT_1` | `ENDPOINT-0001::STAGE_1::ATTEMPT_1` — intact, unclaimed, unconsumed |
| `stage1_results.yaml` | absent — zero artifacts anywhere in the repository |
| Full repository suite at the base | **10504 passed, 0 failed** — the exact count the merge-commit CI recorded |
| Next unused identifier | `XASSET-0047`, verified unused against live repository state: no decision file, no catalog entry, no register mention; its single repository occurrence is a **negative guard** in a predecessor suite forbidding a successor identifier from being named inside `XASSET-0046`'s own text |

Read in full before designing: `XASSET-0043`, `XASSET-0044`, `XASSET-0045`, `XASSET-0046` (all of
§§A–N, especially §§F–J and §M), reviews `4995297886` and `4995648329`, PR #346's acceptance,
post-merge verification and closure comments, both failed CI histories (run `32439614683` / job
`96647501864` and run `32490789238` / job `96797667282`), both auditable stop records, `OPS-0001`,
`OPS-0007` §1, `OPS-0009`, and the current operational-authorization implementation with every
directly coupled test, validator, runner, result validator, universe validator, catalog and
`WS-0014` register entry.

### The question this unit answers

`XASSET-0046` §F authorizes **exactly one** future, separate recovery/reconciliation unit, bounded
by §§F–J. **This is that unit.** It files its own decision and performs the recovery in one coherent
pull request, exactly as §J requires.

The state it recovers from is precise. Production binds authorization truth to `XASSET-0044` /
PR #344 — a decision whose own effectivity condition requires successful merge-commit CI at merge
`f5dedce1…`, where CI **failed**. `XASSET-0045` authorized a recovery and stopped identically at
`2f8cdebe…`. Neither is effective; neither can become effective; and an anchor naming an ineffective
decision cannot authorize anything at all.

## Decision

### A. Determination — `SUCCESSOR_LIFECYCLE_ANCHOR_REBOUND`

The operational-authorization mechanism's lifecycle anchor is rebound from `XASSET-0044` / PR #344 —
permanently unusable — to **this** decision, **this** pull request, its accepted head, its merge, its
successful exact-merge CI, and its final closure, as `XASSET-0046` §G.6 requires.

Nothing else moves. This filing performs no readiness verification, no drift verification, no
Step 11, no attestation, no lane creation, no arming, no claim, no gate evaluation, no execution, and
no results work, and it adds **zero activation authority of any kind**.

### B. Why the old anchor is permanently unusable, not merely stale

`verify_lifecycle_against_truth` authenticates the **authorizing pull request's own** lifecycle from
durable truth. Its fifth gate is `MERGE_COMMIT_CI_SUCCESS`, and `XASSET-0044` §L.6 names *the exact
merge SHA* and excludes *"a run against any other commit."*

| Stopped lifecycle | Merge | Failed merge-commit CI | Auditable stop |
|---|---|---|---|
| `XASSET-0044` / PR #344 | `f5dedce1d1d3116ed8a6845c4447388c85a5414c` | run `32439614683` / job `96647501864` | [`5364490220`](https://github.com/Mast3rkey/Portfolio-HQ/pull/344#issuecomment-5364490220) |
| `XASSET-0045` / PR #345 | `2f8cdebe14925021171b9779453946be1f69b506` | run `32490789238` / job `96797667282` | [`5371158269`](https://github.com/Mast3rkey/Portfolio-HQ/pull/345#issuecomment-5371158269) |

Both runs were independently re-fetched in this session and both are still `event: push`, attempt 1,
`completed` / **`failure`**, each at its own exact merge SHA. **Both remain immutable adverse
history.** Neither may ever be re-run in place, relabelled successful, deleted, suppressed, waived,
described as passing, or represented as satisfying its decision's own effectivity condition, and
neither lifecycle closure may be posted retrospectively. Both auditable stops are likewise preserved.

`XASSET-0043` remains **spent by use**. `XASSET-0045`'s grant **never vested**. `XASSET-0046` §E
draws that distinction precisely so an unspent grant cannot be reached for by analogy to a spent one,
and this unit relies on **neither** — its sole authority is `XASSET-0046` §F.

### C. What is not in question

Independently re-verified in this session and **untouched** by this unit:

- PR #346's merge has exactly two parents in the correct order, and its merge tree `a2a05c83…` is
  byte-identical to its accepted-head tree — zero merge drift;
- the outcome surface: `level1_stage1_runner.py`, `level1_stage1_result_validator.py`,
  `level1_construction_universe_closure_validator.py`,
  `level1_endpoint_evidence_preregistration_validator.py`, every gate, disposition rule, B1/B2/B3,
  `comparison_subject_kind`, `unordered_pair_id`, and every construction identity;
- the universe: **680 / 48**, aggregate `73c0965e…5224`;
- the canonical inputs `PROTOCOL_V1.md` and `pre_registration.yaml`;
- every protected portfolio path, `intelligence/`, and `governance/evidence/`;
- every valid actor-evidence correction, every unrelated gate, threshold and evidence rule.

### D. What moved — the complete, exhaustive list

Only `level1_stage1_execution_authorization.py`'s lifecycle anchor and the identity families that
anchor requires:

| Constant | Closed transition |
|---|---|
| `AUTHORIZING_DECISION` | `"XASSET-0044"` → `"XASSET-0047"` |
| `AUTHORIZING_PULL_REQUEST` | `344` → this pull request's own GitHub-issued number |
| `REVIEWED_BASE_SHA` | `0709d2f05ab031ecb6f69c40465ed4a227983aed` → `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` |
| `LOAD_BEARING_RELPATHS` | **14 → 16** |

plus three additions that carry no prior value and therefore have no transition: the
`RECOVERY_AUTHORIZING_*` family (`XASSET-0046` / PR #346), the `STOPPED_REBINDING_*` and
`STOPPED_RECOVERY_AUTHORIZATION_*` families, and the four refusals in
`_verify_recovery_lifecycle_anchor`.

**`REVIEWED_BASE_SHA`'s new value is not a coincidence and is stated as an equality.** It is
`XASSET-0046`'s own merge — the single event that made this unit authorized to begin — exactly as its
old value was `XASSET-0043`'s merge for the unit `XASSET-0043` authorized. The mechanism enforces
that equality against `RECOVERY_AUTHORIZING_MERGE_SHA` rather than leaving it to coincidence.

**The pull-request number was never guessed.** The first commit on this branch bound the sentinel
`0` — an impossible pull-request number that can never validate — precisely so no guessed value could
be reviewed, merged, or relied upon. The draft pull request was then opened, GitHub issued its own
number, that number was read back from live GitHub, and only then was it bound and re-verified
against the live pull request's own head, base and state.

**`LOAD_BEARING_RELPATHS` grows by direct membership, and nothing is removed.** `XASSET-0037` §E's
principle — the decision supplying the effective structural authorization must sit *inside* the
identity it authorizes, or an attestation could authenticate perfectly while its own governing text
had been edited afterwards — reaches exactly two further files once the anchor moves: `XASSET-0046`,
the authority for this recovery, on precisely the footing `XASSET-0043` already occupies for the
rebinding it authorized; and `XASSET-0047`, the effective structural authorization source after it.
`XASSET-0044`'s own decision file **stays** where `XASSET-0044` put it: a stopped lifecycle is not an
invalidated one, and a path traded away is the defect that boundary exists to catch. `XASSET-0045`'s
decision file is deliberately **not** added — it authorizes nothing, so binding it would assert an
authority relationship that does not exist.

### D.1 The module's current identity

Recomputed **once**, after every permitted byte stabilised — never mid-correction, and never
carried forward from a superseded head. That ordering is `XASSET-0043` §G.6, and it is the exact
failure `XASSET-0042`'s second bounded correction had to repair.

Every prior identity is retained, labelled, and mutually distinct: `XASSET-0044`'s own declaration
in its own decision file is accepted merged history and is **not edited**, so it no longer describes
the module — and its no longer matching is itself asserted, because a stale pin that still agreed
would mean this unit had not actually rebound anything.

```
XASSET-0044 declaration, closed at PR #344 (historical)  sha256  f89c38d49d160795795a73627777c7174d84a61583fc9ed6b5aa921648ee8df1
CURRENT_MODULE_SHA256: 67a903e55a849353ee7ea8b3ed016eaca8f62bf19f2ebbd2633ad1da571c8243
```

### E. The mechanism became stricter, never more permissive

`XASSET-0046` §G.7 forbids making the mechanism more permissive in any respect. It is measurably
stricter: every predecessor identity, every inherited merge, every exact-byte check, the
pin-succession refusal, and every lifecycle gate survive verbatim; **three** inherited merges are
added to the verification table (the recovery authority and both stopped lifecycles, each proven
from git for exact parent order, zero tree drift and ancestry); **two** closed schema blocks are
added to the attestation; and **four** new refusals are added in `_verify_recovery_lifecycle_anchor`:

1. the authorizing **decision** may not be one of `PERMANENTLY_INEFFECTIVE_DECISIONS`;
2. the authorizing **pull request** may not be one of `PERMANENTLY_INEFFECTIVE_PULL_REQUESTS`;
3. the authorized **merge** may not be a commit already recorded in `FAILED_MERGE_COMMIT_CI_RUNS`;
4. the **canonical pins** must still equal the pins `XASSET-0044` left, because §G.9 freezes them.

Refusal 4 is how §G.9 stops being a promise and starts being a check: if any future edit moves a
canonical byte without moving the succession machinery with it, the attestation is refused.

**Verifying a stopped lifecycle is not treating it as effective.** The two stopped merges are proven
from git as *history* — real, ordered, undrifted, genuinely inherited — and nowhere as authority.
Refusing to verify them is how a successor quietly disowns the history it actually stands on.

### F. Strict necessity — what deliberately did **not** move, and why

`XASSET-0046` §G.7 bounds the rebinding to what the successor lifecycle anchor requires; §G.9
independently requires the canonical inputs to be **preserved unchanged**. Those two together decide
the hardest question this unit faced.

`research/level1_endpoint_evidence/pre_registration.yaml` records
`effective_structural_authorization_source: XASSET-0044` and `rebound_by: XASSET-0044`, and
`PROTOCOL_V1.md` carries the matching amendment section. A rebinding that treated those as part of
the anchor would have to amend both canonical files, recompute `CANONICAL_PINS`, change
`level1_endpoint_evidence_preregistration_validator.py`'s bound constants and hash-pin block, and add
a **third** link to the exact closed `package → successor → rebound` transition over the
outcome-producing derivation surface.

**That is forbidden, not merely unnecessary.** §G.9 names the canonical inputs among the things that
*must be preserved unchanged*, and the derivation module is the outcome-producing surface §G.9
protects. So the canonical files are untouched, and their fields stay literally true on their own
terms: **those fields record which decision last amended the canonical bytes, and `XASSET-0044` still
is that decision, because this unit amends none of them.** Which decision last rebound the canonical
bytes and which decision's lifecycle the mechanism authenticates against are two different
relationships; `XASSET-0037` §C's whole finding is that overloading two relationships onto one
identity is how a rebinding starts binding the wrong tree.

**The residual tension is disclosed rather than smoothed over.** `XASSET-0044` is not effective as a
governance decision while remaining the last canonical amender, so a reader who reads
`effective_structural_authorization_source` as "the currently effective decision" will find a
mismatch against `AUTHORIZING_DECISION`. That reading is wrong on the field's own terms, but the
field's wording invites it, and this unit has no authority to reword a frozen canonical input. It is
recorded here, and carried forward in §K, as an observation for a future unit that is separately
authorized to amend the canonical charter — never as something this unit acted on.

### G. The `origin/main` skip guard — classified, reproduced, and corrected

`XASSET-0046` §G.11 hands this unit an observation and explicitly withholds a conclusion: it *"must
classify that use on its own evidence and, if it agrees, correct it under authority that actually
covers it — never on the strength of this paragraph alone."*

**Classified from the function's own source, not from the paragraph.**
`test_on_merged_main_the_moving_base_collapses_to_head_itself` computes
`git merge-base PR344_MERGE_SHA PR344_MERGE_SHA` and diffs that result against `PR344_MERGE_SHA`.
**Both operands are the same pinned, immutable commit.** `origin/main` appears nowhere in the
computation, in either operand, or in the assertion. The subject of the whole function is immutable
history.

**Reproduced by execution before anything was changed.** In an isolated clone with `origin` removed
so `origin/main` is genuinely unresolvable, and with PR #344's merge present:

```
origin/main resolvable:      NO
PR344 merge present:         YES
merge-base(PR344, PR344):    f5dedce1d1d3116ed8a6845c4447388c85a5414c
diff:                        [] (empty, as the test asserts)
```

The proof succeeds completely, and the pre-existing first skip guard would nonetheless have skipped
it. That is the defect exactly: **a live reference silencing a proof about immutable history for a
reason unrelated to that history.** The independent evidence agrees with §G.11's observation.

**Corrected, and only that.** The `origin/main` guard is removed. The second guard — object presence
for `PR344_MERGE_SHA` — is **kept**, because it is a genuine environment precondition in a truncated
checkout and is the same treatment `_pr345_range_is_present` already gives that case. The function is
then added to `HISTORICAL_PROOF_FUNCTIONS`, and its exclusion pin is replaced by an inclusion pin, so
the addition is **loud** rather than silent — which is precisely what that pin was written to force.

**The authority is stated, not assumed.** §G.11's first paragraph is operative on this unit: it must
*"classify every use of `HEAD`, `origin/main`, `merge-base`, and any working-tree comparison in the
files it touches"* and *"re-anchor every historical one."* This unit necessarily touches that file —
`test_production_really_does_bind_pr_344_today` reads the live module and asserts the old anchor, so
the rebinding cannot leave it alone. §G.13 permits exactly this direction of change: *"Guards may be
re-anchored and strengthened; they may not be relaxed."* Removing a skip that could silence a passing
proof makes the guard strictly harder to satisfy: it now always runs. This decision is the authority
that covers it, and §G.11 is not relied on alone.

**Contrast with what `XASSET-0046` could not do.** That filing's authority was a separate principal
authorization expressly bounded to *"exactly these two historical-proof corrections"*, so a third
correction sat outside it however sensible its direction, and independent FULL review `4995297886`
was right to find it BLOCKING. This unit's authority is different in kind: `XASSET-0046` §G.11
positively *requires* re-anchoring every historical use in the files this unit touches.

### H. The preserved historical proofs are re-proved, not restated

`XASSET-0046` §G.2 requires this unit to **preserve** the two corrected guards and **independently
re-prove** them from repository truth — never to cite that filing's word for it, and never to perform
the correction again.

- `test_the_enabling_correction_was_actually_performed` and
  `test_no_protected_path_was_touched_by_this_filing` remain anchored to the immutable closed range
  `f5dedce1d1d3116ed8a6845c4447388c85a5414c` → `61e629f0f655ce8ca4ccd7eaa370d132d593515c`, and this
  unit's supporting artifact re-derives that range's facts independently, in five simulated
  repository ref states, each in an isolated clone.
- The guard `XASSET-0045` repaired in `test_overlap_model_validator.py` remains anchored to
  `0709d2f05ab031ecb6f69c40465ed4a227983aed` → `9c2821ab9e0e0dff09f5a03da5a6034775b00750`. That
  repair is merged repository content and survives its authorizing decision's ineffectivity; it is
  neither reverted, weakened, nor re-anchored to a moving reference.
- PR #345's merge identity — `61e629f0…` the **second** parent of `2f8cdebe…` with `f5dedce1…`
  first, tree `e5eb8905…` byte-identical across accepted head and merge — is re-proved from the
  object store, as are the enabling correction's exact status `M` and both blob ends
  `5b916d88…` → `536bf08b…`, each conjunct independently required, over a non-empty input.

### I. Authority withheld — absolute

This unit adds **zero activation authority**. It does **not**:

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

It does not reuse `XASSET-0043`, reuse `XASSET-0045`, treat `XASSET-0044` or `XASSET-0045` as
effective, re-open `ATTEMPT_1`, revive `XASSET-0040` (which stays spent as
`STOPPED_BEFORE_ATTESTATION`), or consume `XASSET-0027` §P.1 (which remains one and unspent).

`stage_1_executability.executable` stays permanently `false`. **No committed value in this repository
authorizes Stage-1 execution**, and this decision adds none. **Completing this unit authorizes no
further unit** — `XASSET-0046` §F granted exactly one, and this is it.

### J. Fail-closed

Every unobtainable fact is an **error**, never silent agreement. Ambiguity, drift, a competing
worktree, a dirty tree, an unexpected open pull request, or any condition that would require
expanding this authority is a **stop**, not a judgement call.

### K. Observations carried forward — recorded, not acted on

Two audit findings are disclosed here as requirements on some future, separately authorized unit,
exactly as `XASSET-0046` §G.11 carried its own forward rather than acting outside its authority:

1. **The canonical charter's wording.** `effective_structural_authorization_source` and `rebound_by`
   name `XASSET-0044`, which is true on their own terms (§F) but invites a reading this unit cannot
   correct, because §G.9 freezes those bytes.
2. **The pin-succession refusal's coverage.** `_validate_canonical_pins` refuses a bound pin equal to
   `XASSET-0036`'s, `XASSET-0029`'s or `XASSET-0028`'s, but **not** equal to `XASSET-0037`'s, whose
   pin set is defined and unused there. That gap is pre-existing, unrelated to this unit's anchor,
   and therefore outside §G.7's *"only as strictly necessary"*. `XASSET_0044_CANONICAL_PINS` is added
   here so the same gap does not widen: it is bound and checked for **equality** by §E refusal 4
   today, and is the entry a future canonical amendment must move into the refusal loop.

Neither is authority on its own, and neither may be acted on by citing this section alone.

### L. Relation to `XASSET-0029` §E — not an activation PR

This is not an activation pull request. It generates no attestation, arms nothing, and adds **zero**
activation authorizations. `XASSET-0029` §E's no-infinite-regress rule is untouched: final activation
remains the external one-shot runtime attestation and the operator's act, never a merged
authorization pull request.

### M. Effectivity

This rebinding becomes effective — and the anchor it binds becomes usable — **only** after **all** of
the following are complete for this decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the pull request
   head's own run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request authorizes nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not.

**Merging this arms nothing.** Immediately after it merges, `new_execution_is_authorized()` still
returns `False`, the lane is still `ABSENT`, `ATTEMPT_1` is still intact and unconsumed, and no
`stage1_results.yaml` exists.

### N. This filing can attain both green PR-head and green merge-commit CI

Condition §M.6 is only meaningful if it is attainable, and it is the exact condition both `XASSET-0044`
and `XASSET-0045` failed. `XASSET-0045` failed it by writing, in the same pull request, an assertion
about immutable history measured against `git diff --name-only origin/main` — a base that collapses to
empty the moment the branch merges.

**This filing writes no such assertion anywhere.** Every claim it makes about history is anchored to
immutable object identities; every claim it makes about live state is one that remains true and
non-vacuous when `HEAD == origin/main`. That is proved three ways in the supporting artifact:

- **structurally**, by a detector that refuses any moving-reference literal inside a declared
  historical proof, exercised against known-bad **and** known-good synthetic source so that disabling
  it fails its own falsifiability test rather than silently reporting clean;
- **behaviourally**, by running every declared historical proof under **five** simulated repository
  ref states — a feature branch, merged `main` where `HEAD == origin/main`, a later `main`, `HEAD`
  equal to a later `origin/main`, and unrelated later commits — each built inside an **isolated
  clone**, never a `git worktree`, which shares the ref namespace;
- **adversarially**, by mutation probes covering each rebound constant, each new refusal, each new
  schema block, the restored skip guard, a re-added exclusion pin, wrong anchors, reversed parent
  order, tree drift, and hollowed-out assertions.

A **combined non-deadlock guard** refuses, non-vacuously, the conjunction of requiring successful
exact-merge CI with any statement disclaiming this filing's own ability to attain it. It is proved
falsifiable against synthetic text in both directions, so it cannot report clean by inspecting
nothing, and satisfying it by dropping the successful-CI requirement instead is itself a failure.

**A red exact-head or merge-commit CI result is a stop, not an accepted deviation.** §M.6 is
unchanged and remains fully required. Nothing here retroactively repairs PR #344's or PR #345's own
failed merge-commit CI: runs `32439614683` / job `96647501864` and `32490789238` / job `96797667282`
remain immutable adverse history (§B), `XASSET-0044` and `XASSET-0045` remain not effective, and
`XASSET-0043` remains spent.

## Rationale

The mechanism worked, twice, and then the authorization to repair it worked once. `XASSET-0046`
closed all seven of its own conditions, which is what made this unit possible at all — and the reason
it closed them is that it wrote nothing whose truth depended on where a reference pointed.

The substantive question here was not *whether* to move the anchor — `XASSET-0046` §G.6 settles that
— but *how far*. The honest answer was smaller than it first appeared. Following the anchor into the
canonical charter would have been defensible on consistency grounds and was the first shape this
session designed; §G.9 forbids it outright, and on inspection the canonical fields are not actually
false, because they describe canonical-byte lineage rather than lifecycle effectivity. Stopping at
the mechanism is both the lawful answer and the correct one, and the residual wording tension is
disclosed in §F rather than resolved by an edit this unit may not make.

The second question was the skip guard. `XASSET-0046` handled its own version of this exactly right —
it found the defect, could not act on it, and carried it forward — and independent review was right
to stop it from acting. The difference here is not appetite but authority: §G.11 makes re-anchoring
historical uses in touched files this unit's *duty*, and this unit necessarily touches that file
because the rebinding invalidates a live-state assertion two functions away. So the correction is
performed, with its classification reproduced by execution first, and with the exclusion pin flipped
to an inclusion pin so nothing about it is silent.

What is genuinely new is §E's fourth refusal. `XASSET-0046` §G.9 says the canonical inputs must be
preserved unchanged; before this unit, nothing in the mechanism *checked* that. A prose prohibition
is exactly what failed to prevent the moving-anchor defect three filings running, so the freeze is
now mechanical: the effective canonical pins must equal the pins the last canonical amender left, and
an attestation is refused if they ever silently diverge.

## Alternatives Considered

**Leave `AUTHORIZING_DECISION` at `XASSET-0044` and file governance only.** Rejected — `XASSET-0046`
§G.6 requires the anchor to name this unit's own decision and pull request, and the existing anchor
is not merely stale but permanently unsatisfiable, so leaving it would leave the mechanism unable to
authenticate anything ever again.

**Follow the anchor into the canonical charter, amend `PROTOCOL_V1.md` and `pre_registration.yaml`,
recompute the pins, and append a third exact closed transition.** Rejected, and this was the closest
call in the filing. §G.9 lists the canonical inputs among the things that must be preserved
unchanged, and the derivation module that enforces them is the outcome-producing surface §G.9 exists
to protect. The consistency argument for doing it is real and is answered in §F on the merits rather
than dismissed: the canonical fields describe which decision last amended canonical bytes, and that
is still `XASSET-0044`.

**Treat `XASSET-0045` §F's grant as available, since it was never spent.** Rejected. Its grant was
conditioned on complete lifecycle closure that did not occur; an unspent grant that never vested is
not a grant in reserve. `XASSET-0046` §E states the distinction from `XASSET-0043`'s spent-by-use
grant for exactly this reason, and this unit cites neither.

**Re-run either failed CI job, or post either stopped lifecycle's closure retrospectively.**
Rejected outright. Each condition names its own exact merge SHA and excludes runs against any other
commit; a re-run cannot alter a recorded failure, and treating one as satisfaction would rewrite
adverse history. Neither failure was an infrastructure fault — in both cases the test body executed
to completion and returned a deterministic result.

**Remove `XASSET-0044`'s decision file from `LOAD_BEARING_RELPATHS`, since it is ineffective.**
Rejected. A stopped lifecycle is not an invalidated one, its merged bytes are still part of the
history these bytes stand on, and the boundary's own rule is that nothing is ever removed. Growth is
additive or it is not a trust boundary.

**Leave the `origin/main` skip guard alone, as `XASSET-0046` had to.** Rejected on authority, not on
taste: §G.11 makes the classification and re-anchoring a duty of this unit for the files it touches,
and this unit must touch that file regardless. Leaving it would mean knowingly shipping a historical
proof that a live reference can silence, in a filing whose entire subject is that defect class.

**Fix the pin-succession gap around `XASSET-0037`'s pins while editing that loop.** Rejected under
§G.7. It is a pre-existing gap unrelated to this unit's anchor, and *"no unrelated configuration …
may be changed under cover of the rebinding"* is a rule about direction of fit, not about whether the
change would be an improvement. It is carried forward in §K instead.

## Consequences

On this decision's complete §M lifecycle closure, the operational-authorization mechanism's lifecycle
anchor is `XASSET-0047` and this pull request, and an attestation becomes *possible* to authenticate
for the first time since `XASSET-0044` stopped — **possible, not present, and not authorized**:
generating one is Step 11 work that neither `XASSET-0046` nor this decision authorizes.

`XASSET-0045` remains not effective and authorizes nothing. `XASSET-0044` remains not effective.
`XASSET-0043` remains spent. Run `32439614683` / job `96647501864` remains the failed merge-commit CI
for `f5dedce1…`, and run `32490789238` / job `96797667282` remains the failed merge-commit CI for
`2f8cdebe…`, permanently. `XASSET-0027` §P.1 remains one and unspent. `XASSET-0040` remains spent as
`STOPPED_BEFORE_ATTESTATION`. `XASSET-0046` §F's single grant is now **spent by use**.

Stage 1 remains **UNARMED and NOT EXECUTABLE**, the lane **ABSENT**, `ATTEMPT_1` intact, unclaimed and
unconsumed, and no `stage1_results.yaml` exists anywhere in the repository.
