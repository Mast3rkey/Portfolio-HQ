---
decision_id: XASSET-0043
date: 2026-08-19
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, XASSET-0035, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_correction_rebinding_authorization.py
---

## Context

### Live preflight

Performed against live git and live GitHub before any file was edited, and treated as authoritative
over every fact supplied to this session. Every value below was independently re-derived; all matched.

| Fact | Verified value |
|---|---|
| Local `HEAD`, `origin/main`, GitHub `main` | all three exactly `5fbfc94d7333e552bd2654261e0c57134a172e31` |
| Worktree / stash / worktrees | clean; no stash; exactly one worktree; no competing mutation lane |
| Open pull requests | **zero** |
| PR #342 | merged and closed, `merged_by` `Mast3rkey`, merge commit `5fbfc94d…`, 11 files, 4 commits |
| PR #342 merge parents | exactly two, in order: `9c8647f9dddacdf63825f569097214ba65299fe8`, then `4d5d99d67364d3c940aad74c3093bd2afbc3481d` |
| PR #342 merge drift | **zero** — merge tree `96215644985ae322d78915850bec21b7b247c12d` byte-identical to the accepted head's tree; `git diff` accepted-head→merge empty |
| Review chain | FULL [`4975556072`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#pullrequestreview-4975556072) at `7573147e…` → corrective DELTA [`4976030124`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#pullrequestreview-4976030124) at `c8ea6ef…` → final clean **DELTA** [`4976294690`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#pullrequestreview-4976294690) at the exact accepted head, **0/0/0/0** |
| Principal acceptance | [`5347516573`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#issuecomment-5347516573) — durable `user.login` **`Mast3rkey`**, `type: User` |
| Post-merge verification | [`5347527432`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#issuecomment-5347527432) — durable `user.login` **`Mast3rkey`**, `type: User` |
| Merge-commit CI | run [`32297842564`](https://github.com/Mast3rkey/Portfolio-HQ/actions/runs/32297842564) / job `96213267167` — `completed`/`success`, `event: push`, attempt 1, `head_sha` **the exact merge SHA** |
| Final closure | [`5347619800`](https://github.com/Mast3rkey/Portfolio-HQ/pull/342#issuecomment-5347619800) — durable `user.login` **`Mast3rkey`**, `type: User` |
| `XASSET-0042` | **EFFECTIVE** — all seven §I conditions closed |
| `XASSET-0040` | spent as `STOPPED_BEFORE_ATTESTATION`; **not revived** |
| `LOAD_BEARING_RELPATHS` | **10**, unchanged; `AUTHORIZING_DECISION` `XASSET-0037`; `AUTHORIZING_PULL_REQUEST` `337` |
| Load-bearing drift | **exactly one of ten** — see §B; the other nine byte-identical to the bound merged tree |
| Canonical artifacts | `PROTOCOL_V1.md` `367583b6…1d8971`, `pre_registration.yaml` `768b013c…894bce1` — both equal to `CANONICAL_PINS`; universe independently regenerated: **680** constructions across **48** cells |
| Lane state | exactly **`ABSENT`**; `AUTHORIZATION_ROOT` and all four lane paths **absent** |
| `new_execution_is_authorized()` | **`False`** |
| `ATTEMPT_1` | **intact, unclaimed, unconsumed** |
| `stage1_results.yaml` | **absent** anywhere on the filesystem |
| `XASSET-0043` identifier | **unused** — zero occurrences repository-wide; catalog held 144 decisions ending at `XASSET-0042` |

Read in full before designing: `XASSET-0041` (all of §§A–K, especially §I), `XASSET-0042` (especially
§§G–I and both bounded corrections), `XASSET-0030` §D and §G.B, `XASSET-0037` §§D–J and its accepted
corrections, `XASSET-0038`/`XASSET-0039`/`XASSET-0040` for the separate-link convention, `OPS-0001`,
`OPS-0007` §1, and `OPS-0009`.

### The question this unit answers

`XASSET-0041` §I enumerates five links, each requiring its **own** separate governance authority and
its **own** complete lifecycle. Link 1 — the correction — is done: `XASSET-0042` is merged and
effective. Link 2 is the rebinding, and `XASSET-0041` §I states in terms that it is **not** authorized
by the correction succeeding:

> **None of links 2 through 5 is authorized, pre-authorized, combined, or made reachable by this
> decision or by the correction succeeding.**

`XASSET-0042` §G restates the same table with link 2 marked `NOT authorized, NOT performed`, and
closes with `authorizes no successor unit of any kind`. **This decision is that authority, for the
rebinding only, and nothing more.**

## Decision

### A. Determination — `POST_CORRECTION_REBINDING_AUTHORIZED`

**Exactly one** future, separate, bounded successor operational-authorization / load-bearing
**rebinding** unit is authorized: a lifecycle that lawfully binds the corrected load-bearing
implementation merged by PR #342, resolving the enforcement drift `XASSET-0030` §D recorded in advance
and `XASSET-0042` §G handed forward.

**This filing performs no part of that rebinding.** It edits no load-bearing byte, rebinds nothing,
changes no `LOAD_BEARING_RELPATHS` entry, `AUTHORIZING_*` constant, or hash pin, amends no canonical
artifact, runs no readiness verification and no drift check, retries no part of step 11, generates no
attestation, and creates no result. It authorizes and defines; a later unit binds.

**Links 3, 4, and 5 are not authorized, here or by implication (§K).**

### B. The enforcement drift, reproduced read-only before anything was authorized

`XASSET-0030` §D recorded **in advance** that any later lawful correction of load-bearing code
"deliberately creates enforcement drift, and Stage 1 becomes non-armable until a successor
operational-authorization or reconciliation lifecycle lawfully binds the new load-bearing
implementation." `XASSET-0042` performed exactly such a correction.

That prediction was verified against live state rather than assumed. Each of the ten load-bearing
paths was compared, **from the git object store only**, between its working-tree bytes and the same
blob in the authorized merged `XASSET-0037` tree — PR #337's merge
`637eaa30302f5a71f84ab1d215ecbd32c01399b5`:

| Path | Bound merged tree | Working tree | Status |
|---|---|---|---|
| `level1_stage1_execution_authorization.py` | `8186a50f…d91f2fc8` (128,252 B) | `749597ee…b50f24c7` (153,591 B) | **drift** |
| `level1_endpoint_evidence_preregistration_validator.py` | `2b8ead2b…deb3d356` | same | match |
| `level1_construction_universe_closure_validator.py` | `1fed8f42…` | same | match |
| `level1_stage1_runner.py` | `4a88cf6d…` | same | match |
| `level1_stage1_result_validator.py` | `b4773eb7…` | same | match |
| `research/level1_endpoint_evidence/PROTOCOL_V1.md` | `367583b6…1d8971` | same | match |
| `research/level1_endpoint_evidence/pre_registration.yaml` | `768b013c…894bce1` | same | match |
| `governance/decisions/XASSET-0029-…-authorization.md` | `520bd918…` | same | match |
| `governance/decisions/XASSET-0036-…-authorization.md` | `6bd4eaa8…` | same | match |
| `governance/decisions/XASSET-0037-…-rebinding.md` | `7aa3090e…` | same | match |

**Exactly one path drifted, and it is the one `XASSET-0042` was authorized to correct.** The
production module's git blob is `d55b9e1882368a5e8ed888a336a5d00e49b2b05e`; the bound blob is
`92f64374dd1bc4dae1c5d477d5edec4ef8131206`.

The reproduction was performed **at the git-object level only** — `git rev-parse`, `git cat-file`, and
a hash of the working-tree bytes. **No lane was created, inspected, or touched; no attestation
mechanism was driven; `write_authorization` was never called; `AUTHORIZATION_ROOT` was not created;
and no part of the authorized step-9 readiness verification or step-10 drift check was performed.**
Confirming from the object store that a file changed is not those units' work, and this filing does
not claim their authority.

**An obsolete authorization that cannot authorize a corrected module is the mechanism working.**

### C. This is §D's reconciliation lifecycle, not a second consumption of §G.B step 8

Stated precisely rather than conveniently, because it is the point an independent reviewer should
press hardest.

`XASSET-0030` §G.B step 8 requires "**one** successor operational-authorization / load-bearing
rebinding lifecycle against those exact merged bytes" — the `XASSET-0036`-authorized executable
package. **`XASSET-0037` performed that one, and this decision does not reopen, re-consume, or
re-issue it.** Step 8's own single rebinding remains spent, and the package it bound remains bound.

The authority for a *further* rebinding is separate and predates the need for it:

1. **`XASSET-0030` §D** is a general statement about lawful corrections, not a one-time allowance: it
   provides for "a successor operational-authorization **or reconciliation lifecycle**" whenever a
   lawful correction of load-bearing code creates enforcement drift. `XASSET-0042` is such a
   correction; this is such a reconciliation.
2. **`XASSET-0041` §I link 2**, accepted and effective, names the required next link exactly —
   "rebinding (separately authorized; `XASSET-0030` §G.B step-8 **equivalent**)". *Equivalent*, not
   *identical*: a lifecycle of the same kind and rigour, separately authorized, not a second draw on
   step 8's own budget.
3. **`XASSET-0042` §G** carries the same five-link table forward with link 2 unauthorized and
   unperformed, and explicitly authorizes no successor.

`XASSET-0037` is preserved, not invalidated — exactly as it preserved `XASSET-0029`. Its own six-gate
lifecycle really closed and remains valid accepted history. What a further rebinding changes is not
who established the mechanism, nor which package was bound, but **which merged tree the mechanism
proves load-bearing identity against** now that one bound path has been lawfully corrected.

### D. Relation to `XASSET-0029` §E — not an activation PR, zero activation authorizations

`XASSET-0029` §E terminates the activation regress on a step that **changes no repository state** —
the external runtime attestation. A rebinding changes repository state extensively, so it is
categorically outside the step §E terminates. `XASSET-0036` §B.4 reached that conclusion for the
implementation package and `XASSET-0037` §G reached it for the step-8 rebinding, on the same
reasoning; it applies unchanged here.

**This decision adds one authorized rebinding and ZERO activation authorizations.**
`stage_1_executability.executable` stays `false` permanently and keeps its enforced-false check. **No
committed value in this repository authorizes Stage-1 execution**, and neither merging this decision
nor merging the rebinding it authorizes changes that. Final activation remains the external one-shot
runtime attestation and the operator's act — never another merged pull request.

### E. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

§P.1's exactly-one Stage-1 **evaluation/results** PR is **not consumed, replaced, amended, or counted
against** by this filing or by the rebinding it authorizes, on the grounds `XASSET-0036` §C and
`XASSET-0037` §H already recorded: §P.1's PR "may make no production configuration change," and a
rebinding is nothing but production configuration change; §P.1's deliverable is a results document,
and neither this nor a rebinding produces one; and §P.1's PR sits **after** arming while both of these
sit before it. After this merges, §P.1's budget is exactly what it is today: **one, unspent.**

### F. Authority granted — exactly one future, separate rebinding unit

Effective only on this decision's own complete lifecycle closure (§N), **exactly one** future,
separate, bounded pull request may:

1. file its **own** rebinding decision record, under the next `XASSET-####` identifier **verified
   unused against live repository state at the time it is filed**, never predicted or reserved here;
2. rebind the effective structural authorization source to that decision, and rebind
   `AUTHORIZING_PULL_REQUEST` and `REVIEWED_BASE_SHA` to that unit's own verified pull request and
   base;
3. edit `level1_stage1_execution_authorization.py` **only** to the extent the rebinding's own
   configuration, identity constants, evidence, and validation require (§G.3);
4. add its own decision file to `LOAD_BEARING_RELPATHS` (§G.8, §H);
5. amend the canonical artifacts **only** in authorization language, in lockstep (§J);
6. recompute stale identities and pins **once**, after every authorized byte has stabilized (§G.6);
7. resolve the `XASSET-0042` current-identity evidence explicitly (§I);
8. synchronize the catalog and the `WS-0014` register, and update the tests that pin the values it
   lawfully changes, **without weakening any of them** (§G.2, §I.4).

**One unit, one pull request.** The rebinding decision and the rebinding itself belong in the same
coherent PR, exactly as `XASSET-0037` was both — splitting them would create a decision whose bound
bytes do not yet exist, and a rebinding whose governing text is not yet inside the identity it binds.
A future session that finds a concrete technical reason to package this differently must **stop and
disclose**, not decide it silently.

### G. The ten required properties of the authorized rebinding

Each is a condition on the authorized unit. None is satisfied by this filing, and none may be waived
by the unit that performs it.

**G.1 — Bind only stabilized, independently reviewed exact bytes.** The rebinding binds exact
git-object identities at its own accepted head and its own merge, never a value asserted in prose,
never a value computed before the bytes stabilized, and never a working-tree value that no independent
review saw. Expected identity continues to be derived from the merged git tree at validation time, not
from a hard-coded constant.

**G.2 — Preserve all ten existing load-bearing paths; remove none; weaken no exact-byte check.** Every
one of the ten paths in §B is retained. No path is removed, exempted, made conditional, or excluded
from any comparison. The pin-succession refusal — a successor pin equal to **any** predecessor
generation's accepted pin is refused — is retained and may be strengthened, never relaxed. No test
guarding these properties may be deleted, `skip`ped, `xfail`ed, narrowed to a subset of paths, or
rewritten to assert less than it asserts today.

**G.3 — Preserve `XASSET-0042`'s actor-evidence correction byte-for-byte, except where rebinding
strictly requires otherwise.** The corrected mechanism is the reason this rebinding exists; a
rebinding that quietly re-loosened it would defeat its own purpose. Specifically preserved: the two
narrowed call-site branches; both actor-error messages, byte-unchanged; `PRINCIPAL_ACCOUNT_LOGIN` and
`LIFECYCLE_OPERATOR_LOGIN`; the isolated exception section and its exact PR #337 pins; the four
canonical-JSON record fingerprints and the ordered chronology and review-finality checks the first
bounded correction installed; and the absence of any general standing for `claude[bot]`. Changes
confined to the rebinding's own configuration, identity constants, and evidence are permitted; any
other change to that section must be **argued as strictly necessary, not assumed**, and reviewed as
such.

**G.4 — Preserve the outcome-producing surface, the universe, and canonical substance.**
`level1_stage1_runner.py` and `level1_stage1_result_validator.py` stay byte-identical across every
anchor the mechanism already compares. The transitive derivation surface,
`level1_endpoint_evidence_preregistration_validator.py`, stays at the accepted successor blob
`2b8ead2b…deb3d356`, and the exact closed 17-region package-to-successor transition manifest remains
satisfied and unweakened. `level1_construction_universe_closure_validator.py` is unchanged. Every
gate's index, question, class, controlling authority, and failure disposition; every disposition rule;
B1, B2, and B3; `comparison_subject_kind`; `unordered_pair_id`; every construction identity; and
universe membership, ordering, and cardinality are unchanged, with the aggregate universe hash
`73c0965e73de2cc505bc54ac8317aa1d75b3955eb7e624af9eeb2cddf5dc5224` independently regenerated after any
canonical amendment and unchanged at **680** / **48**.

**G.5 — Use exact identities, correct parent ordering, exact-head review, merge-tree equality, and
fail-closed drift handling.** Derived from the git object store rather than declared: the rebinding
PR's merge has exactly two parents **in order**, base then accepted head; its merge tree is
byte-identical to its accepted head's tree; every merge it inherits from is an **ancestor** of its own
merge; every load-bearing blob equals the same blob at the independently reviewed head, so the merged
tree never becomes its own source of truth; and any unmatched, absent, or unreadable anchor **fails
closed** rather than being treated as agreement.

**G.6 — Recompute stale identities only after all authorized bytes stabilize.** Canonical pins, module
digests, and every recorded identity are computed **once**, after every permitted canonical,
enforcement, and evidence byte has settled — never mid-correction, and never carried forward from a
superseded head. This is the exact failure `XASSET-0042`'s second bounded correction had to repair;
repeating it is a foreseeable defect, not an accident.

**G.7 — Resolve the `XASSET-0042` `FINAL_CORRECTED_MODULE_SHA256` evidence explicitly.** See §I. The
rebinding lawfully changes the module, which makes that declaration stale by construction. It must be
resolved by amendment or by retirement-with-equivalent-replacement, argued not assumed; it may never
be left silently false, and its guard may never be deleted or weakened.

**G.8 — Keep the effective governing rebinding decision inside the authenticated boundary, without
removing historical authority.** On `XASSET-0037` §E's principle — the decision supplying the effective
structural authorization must sit inside the identity it authorizes, or an attestation could
authenticate perfectly while its own governing text had been edited afterwards — the new rebinding
decision file joins `LOAD_BEARING_RELPATHS`. The `XASSET-0029`, `XASSET-0036`, and `XASSET-0037`
decision files are **retained**, on exactly the footing they occupy today: historical authority is
preserved, never displaced.

**G.9 — Authorize nothing downstream.** The rebinding performs and authorizes no readiness
verification, no drift verification, no part of step 11, no attestation, no arming, no claim, no
execution, no recovery, and no results work. Completing it authorizes the next link no more than a
clean step-10 result authorized step 11 — the inference `XASSET-0039` §K already foreclosed.

**G.10 — Complete its own lifecycle.** Independent **FULL** exact-head review under `OPS-0007` §1; any
required bounded correction and exact-head re-review so the review holds at the **final** accepted
head; explicit principal exact-head acceptance; normal merge; immediate post-merge verification;
**successful merge-commit CI whose `head_sha` is the exact merge SHA**; and final post-CI verification
and lifecycle closure. **None is individually sufficient.**

### H. The trust boundary grows, and nothing is removed

`LOAD_BEARING_RELPATHS` **10 → 11**, using the **existing exact-byte mechanism unchanged**. The single
addition is the new rebinding decision file itself, for the reason §G.8 states. `XASSET-0036` §E.6's
stated preference for the existing mechanism holds; a rebinding that departs from it must argue a
concrete technical reason rather than assume one.

**No load-bearing path is removed and no exact-byte check is weakened.** Growth here is the same shape
as `XASSET-0029`'s six, `XASSET-0037`'s ten, and now eleven: each generation adds the decision that
governs it and keeps every path its predecessors bound.

### I. The `XASSET-0042` current-identity evidence must be explicitly resolved

`XASSET-0042` §G carries exactly one machine-readable `FINAL_CORRECTED_MODULE_SHA256:` declaration,
`749597ee…b50f24c7`, and
`test_level1_stage1_pr337_lifecycle_actor_evidence_correction.py::TestDeclaredCorrectedIdentityMatchesTheModule`
hashes the module's own bytes and requires the two to agree. The final `XASSET-0042` review
`4976294690` examined this deliberately and recorded the intent:

> Its failure on a later module change is the intended fail-closed boundary: the separately authorized
> rebinding unit must explicitly amend/retire the current-identity evidence when it lawfully changes
> the module, rather than silently invalidating `XASSET-0042`'s declaration.

That is a designed hand-off, and this decision requires the authorized rebinding to take it:

**I.1 — The end state must contain exactly one true current declaration**, machine-checked against the
production module's real bytes. Two declarations, a declaration matched only against another
declaration, or a declaration matched against a stated constant rather than the file are all
insufficient.

**I.2 — Either resolution is permitted; the choice must be argued.** The rebinding may (a) **amend**
`XASSET-0042`'s declaration to the new post-rebinding identity, recording `749597ee…` additively as a
further historical value; or (b) **retire** the current-identity role from `XASSET-0042` — re-anchoring
its declaration to the closed head range it truthfully describes — and carry the current-identity role
in its own decision under an equivalently strong, equivalently machine-checked guard. Silence, or a
choice made without stating why, is not acceptable.

**I.3 — No prior identity may be dropped or conflated.** The bound `8186a50f…`, the intermediate
superseded-head `03d84212…`, and `XASSET-0042`'s final `749597ee…` are all retained, all labelled with
what they are, and all kept mutually distinct from whatever becomes current. `XASSET-0042`'s statements
that **its own unit** re-pinned nothing remain true of that unit and must not be deleted; they may not
be read as a claim about the repository's state after a later, separately authorized rebinding, and the
rebinding must make that distinction explicit rather than leaving a reader to infer it.

**I.4 — The guard may be re-anchored, never weakened.** Three of its nine assertions are
module-digest-coupled and will fail by design once the module lawfully changes: the declared identity
against the module's bytes, the register carrying the current identity, and the assertion that
`XASSET-0042`'s own evidence-only correction did not edit the module — the last of which compares
against a **moving** `HEAD` and must be re-anchored to the closed commit range it actually describes.
Re-anchoring each to the truth it is meant to express is required. Deleting, `skip`ping, `xfail`ing,
or relaxing any of them is prohibited, and no replacement may assert less than the assertion it
replaces.

### J. Canonical amendment — permitted only in authorization language

`PROTOCOL_V1.md` and `pre_registration.yaml` may be amended **in lockstep** and **only** in
successor-lifecycle authorization language, on exactly `XASSET-0037` §F's precedent: the fields naming
the currently effective lifecycle, `stage_1_operational_authorization`'s `rebound_by` and
`effective_structural_authorization_source`, the successor-rebinding record, and the
`must_bind_exactly` / `must_fail_closed_on` entries. `established_by: XASSET-0029` stays — historical
truth is not rewritten — and every superseded value is retained in an explicitly predecessor-named
field.

Everything §G.4 enumerates is **unchanged**, and the universe hash must be independently regenerated
after the amendment and shown unchanged at 680 / 48. `stage_1_executability.executable` stays `false`.
If no authorization-language change is actually required, none may be made merely to have amended
something.

### K. Authority withheld — absolute

This decision does **not** perform, and does **not** authorize:

- performing any part of the rebinding it authorizes — that is the future unit's own work under its
  own lifecycle;
- `XASSET-0030` §G.B steps 9, 10, or 11, in whole or in part;
- any renewed readiness verification or renewed post-rebinding drift check;
- generating any external attestation;
- creating `AUTHORIZATION_ROOT`, any lane path, or `READY` / `CLAIMED` / `COMPLETED` lane state or any
  ledger entry;
- arming, claiming, completing, executing, or recovering any Stage-1 execution;
- consuming any part of `ATTEMPT_1`;
- evaluating any gate for any registered construction, or asserting any per-construction outcome;
- creating `stage1_results.yaml` or any disposition, cell outcome, or roll-up;
- changing any construction identity, universe membership, ordering, cardinality, or universe hash;
- reviving `XASSET-0040`, which remains spent as `STOPPED_BEFORE_ATTESTATION`;
- consuming `XASSET-0027` §P.1's reserved results PR;
- reopening, re-deriving, or re-arguing B1, B2, or B3, or any gate semantics;
- resolving `XASSET-0024` §K.1, or amending `XASSET-0020` §E.1;
- any Stage 2 work, evidence acquisition, or market, fundamental, or economic data acquisition;
- reading, listing, opening, or referencing any `risk_lane_boundary` protected `RISK` result path;
- weakening any validator or test;
- creating any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  tier, cluster, cap, or margin state;
- authorizing any chart, ladder, deployment, trade, order, or brokerage action;
- authorizing any successor beyond the **one** future rebinding unit defined in §F;
- rewriting any accepted history.

### L. Fail-closed

Every condition in §G is conjunctive. If the authorized rebinding cannot establish any one of them —
an anchor it cannot read, an identity it cannot reproduce, a path it cannot match, a guard it cannot
re-anchor without weakening, a canonical regeneration that does not return 680 / 48 and
`73c0965e…5224` — it **stops and discloses**. It does not proceed on a partial result, exclude the
failing item, or repair a defect outside its own authorized scope: `XASSET-0039` §J's no-repair rule
and `XASSET-0040`'s own terminal stop are the model, and a stop costs one authorized unit rather than a
one-shot attempt.

An unobtainable anchor is never treated as agreement. A drift the rebinding is not authorized to bind
is a stop, not a widening.

### M. Packaging and evidence

One coherent draft pull request (§F), carrying its own decision record and its own adversarial
supporting suite, its exact file scope enumerated and preflighted repository-wide before editing, and
its own durable author report anchored to its real pull-request number and exact head — verified
against live GitHub after opening, never predicted. Predecessor suites that pin the shared `WS-0014`
`active_branch` / `active_pr` / `last_verified_main_sha` fields advance together under `OPS-0001`'s
Active-GitHub-fields rule. `OPS-0009` classifies this filing and the rebinding it authorizes as
**Lane G**.

### N. Effectivity

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
not; principal acceptance does not; merge does not. **Only complete closure of all seven does** — and
even then what becomes authorized is a **future rebinding unit**, not an armed Stage 1.

**Merging this decision does not arm Stage 1, does not rebind anything, creates no lane state, claims
no `ATTEMPT_1`, and executes nothing.** Immediately after it merges, `new_execution_is_authorized()`
still returns `False`, the lane is still `ABSENT`, `AUTHORIZING_DECISION` is still `XASSET-0037`, and
the enforcement drift in §B is still there — because the rebinding that resolves it has not yet been
written, reviewed, accepted, or merged.

## Rationale

The correction worked, and it cost what it was always going to cost. `XASSET-0030` §D wrote that cost
down before anyone had to pay it: correcting load-bearing code makes Stage 1 non-armable until a
lifecycle lawfully binds the corrected implementation. `XASSET-0042` corrected the module; the drift in
§B is the recorded consequence arriving on schedule, not a surprise and not a defect.

What is genuinely at stake is the shape of the next step, not whether it is needed. Two failure modes
are available and both are cheap to fall into.

The first is **collapsing links**. A session holding a merged correction, a single visible drift, and a
mechanism it understands well is one short inference away from rebinding, re-verifying readiness,
re-checking drift, and arming — each step looking like the obvious consequence of the last.
`XASSET-0041` §I foreclosed that inference in advance, and `XASSET-0039` §K foreclosed its general
form. This decision authorizes link 2 and stops, in the same words its predecessors used, so that the
boundary does not depend on a future session's restraint.

The second is **binding the wrong thing**. `XASSET-0037` §C identified the largest failure mode
available to a rebinding — overloading one identity across relationships that are not the same
relationship — and answered it with four separately named identity families. That discipline is not
restated here as decoration: this rebinding adds a fifth relationship (the corrected module and the
merge that delivered it), and the same anti-overloading rule is what keeps it from being smuggled into
`EXECUTABLE_PACKAGE_*` or `HISTORICAL_OPERATIONAL_AUTHORIZATION_*`.

§I exists because this program has already made the specific mistake it guards against. `XASSET-0042`
published a superseded module digest as current, an independent review caught it, and the repair
installed a machine-checked declaration precisely so the record could not drift from the file again.
That guard now points at a file the next unit is authorized to change. Leaving it to be discovered at
implementation time — where the path of least resistance is to delete the failing assertion — would
convert a working guard into an inconvenience. Naming it now, with the resolution options and the
prohibition on weakening stated in advance, is the cheaper and more honest order of operations.

Finally, the honesty about §G.B step 8 in §C is deliberate. It would be easy, and wrong, to describe
this as "step 8" and inherit its authority wholesale. Step 8 was consumed. What authorizes a further
rebinding is §D's reconciliation clause and `XASSET-0041` §I link 2's own word, *equivalent* — a
narrower and more accurate claim, and one a reviewer can check against the accepted text rather than
against this filing's confidence.

## Alternatives Considered

**Perform the rebinding in this filing.** Rejected. `XASSET-0041` §I and `XASSET-0042` §G both state
that link 2 is separately authorized and not made reachable by the correction succeeding. A filing that
authorized and performed the rebinding in one motion would be exercising authority it created for
itself in the same document — the precise structure this program's separate-link convention exists to
prevent, and the reason `XASSET-0038`, `XASSET-0039`, `XASSET-0040`, and `XASSET-0041` each authorized
without performing.

**Authorize links 2 through 5 together, since the chain is known.** Rejected, and the strongest
temptation here. The chain's shape is known; its *outcomes* are not. A readiness verification can fail,
a drift check can find drift the rebinding did not anticipate, and a step-11 unit can stop — as
`XASSET-0040`'s did. Pre-authorizing a link whose predecessor has not run means authorizing work whose
premises may not survive, and it is exactly the inference `XASSET-0039` §K foreclosed. One link, one
authorization, one lifecycle.

**Treat this as a second draw on `XASSET-0030` §G.B step 8.** Rejected as inaccurate. Step 8 authorized
*one* rebinding against the executable package's exact merged bytes, and `XASSET-0037` performed it.
Claiming step 8 again would either double-count a spent budget or silently redefine what step 8 bound.
§C takes the narrower and checkable route instead.

**Amend `XASSET-0037` in place to cover the corrected bytes.** Rejected. `XASSET-0037` is accepted,
independently reviewed, merged history whose own load-bearing decision file is inside the identity it
binds; editing it would change a bound byte to describe bytes its review never saw, and would rewrite
accepted history to avoid filing a new record. A new generation that preserves its predecessors is the
established pattern.

**Let the `XASSET-0042` guard fail and repair it during implementation.** Rejected. A guard discovered
failing mid-implementation, under pressure to get a suite green, is a guard likely to be weakened
rather than re-anchored. §I converts that from a discovery into a stated, reviewable requirement with
the permissible resolutions and the hard prohibition both fixed in advance.

**Bind the corrected module without adding the new decision file to the trust boundary.** Rejected on
`XASSET-0037` §E's reasoning: the decision supplying the effective structural authorization must sit
inside the identity it authorizes, or an attestation could authenticate perfectly while its own
governing text had been edited afterwards. The alternative saves one path and reopens exactly that gap.

## Consequences

**Immediately: nothing changes operationally.** Stage 1 remains `UNARMED` and `NOT EXECUTABLE`. The
lane is `ABSENT`, `new_execution_is_authorized()` returns `False`, `ATTEMPT_1` is intact and
unconsumed, and no `stage1_results.yaml` exists. `LOAD_BEARING_RELPATHS` still holds ten paths,
`AUTHORIZING_DECISION` is still `XASSET-0037`, `AUTHORIZING_PULL_REQUEST` is still `337`, no pin has
been rebound, and the §B enforcement drift is still present and still fails closed.

**On this decision's complete lifecycle closure**, exactly one future rebinding unit becomes
authorized to begin, bounded by §§F–J and forbidden everything in §K. Until then it may not be opened,
drafted as an implementation, or begun.

**When that rebinding completes**, Stage 1 becomes *armable* against the corrected implementation —
never *armed*. Links 3, 4, and 5 will each still require their own separate authority and their own
complete lifecycle, and the final activation will still be the external one-shot runtime attestation
and the operator's act.

**If the rebinding stops**, the cost is one authorized unit. `ATTEMPT_1` is untouched, every recovery
option stays open, and the drift stays fail-closed — which is the property that made the `XASSET-0040`
stop cheap, and the reason this program keeps paying for one link at a time.
