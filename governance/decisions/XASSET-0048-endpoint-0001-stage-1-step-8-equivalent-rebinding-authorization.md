---
decision_id: XASSET-0048
date: 2026-08-22
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0038, XASSET-0039, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_step8_equivalent_rebinding_authorization.py
---

## Context

### Live preflight

Independently re-derived this session from live git and live GitHub before any file was written.
Nothing below is inherited from a prior session's summary or from the task that commissioned this
filing.

| Fact | Verified value |
|---|---|
| GitHub `main`, `origin/main`, local `HEAD` | `bb95ed26964b1bc7a2e230c76060fec82752efa1` — all three identical |
| That commit's identity | PR #347's merge, parents `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` then `8ae0988d4c1ffc551e7fa0a1d1ee1edfa7a49a9e`, re-derived via `git log --pretty='%H %P'` |
| Merge-tree drift on PR #347 | **zero** — merge tree `c8b677f8697660bef1122a83615845961457be89` is byte-identical to the accepted head's own tree |
| PR #347 | merged, closed, `merged_by` `Mast3rkey`, 5 commits, 21 files |
| PR #347 independent FULL review | [`4997532748`](https://github.com/Mast3rkey/Portfolio-HQ/pull/347#pullrequestreview-4997532748) at `1fb5941ce1f40ca24fa187289b318e4e266730cc` — 1 MAJOR, 1 MINOR |
| PR #347 clean exact-head DELTA review | [`4997822429`](https://github.com/Mast3rkey/Portfolio-HQ/pull/347#pullrequestreview-4997822429) at the accepted head — **0 / 0 / 0 / 0** |
| PR #347 principal exact-head acceptance | [`5375989065`](https://github.com/Mast3rkey/Portfolio-HQ/pull/347#issuecomment-5375989065) |
| PR #347 post-merge verification | [`5376014867`](https://github.com/Mast3rkey/Portfolio-HQ/pull/347#issuecomment-5376014867) |
| PR #347 final post-CI lifecycle closure | [`5376069596`](https://github.com/Mast3rkey/Portfolio-HQ/pull/347#issuecomment-5376069596) |
| PR #347 merge-commit CI | run `32532487548` / job `96927108608` — run **and** job `head_sha` each equal the exact merge SHA — `completed` / **`success`**, **10,666 passed** |
| Open pull requests | **0** |
| Working tree · worktrees | clean · sole worktree, no competing mutation lane |
| `XASSET-0048` identifier | unused — 0 hits in `governance/decisions.yaml`, no decision file; the sole repository occurrence is one mutation-pin *docstring* in `XASSET-0047`'s artifact, which names it only to refuse pre-authorizing it |
| Decision catalog | **149** entries, `issues == ()` |
| `AUTHORIZING_DECISION` · `AUTHORIZING_PULL_REQUEST` · `REVIEWED_BASE_SHA` | `XASSET-0047` · `347` · `0b76c09f8d1aba01780b4f06fdd692f7393fbfd3` |
| `LOAD_BEARING_RELPATHS` | exactly **16** |
| Canonical pins | `PROTOCOL_V1.md` `1ad1d060…5d0c84` · `pre_registration.yaml` `898c329d…12d82f` — both match the live files |
| Frozen universe | **680** constructions · **48** cells · `73c0965e…5224` — match |
| `stage_1_executability.executable` | `False` |
| `new_execution_is_authorized()` | `(False, …)` — "no attestation present" |
| `AUTHORIZATION_ROOT` | **absent** — lane `ABSENT` |
| `ATTEMPT_1` (`ENDPOINT-0001::STAGE_1::ATTEMPT_1`) | intact, unclaimed, unconsumed |
| `stage1_results.yaml` | **none exists anywhere** |

No `risk_lane_boundary` protected `RISK` result path was read, listed, opened, or referenced.

### The question this unit answers

`XASSET-0047` is effective. Its own seven conditions all closed, and the operational-authorization
mechanism can once again authenticate its authorizing pull request's lifecycle from durable truth.

What it did **not** do is perform the rebinding. `XASSET-0047` §A says so — "Nothing else moves" —
and its own closure comment states the remainder plainly: arming still requires renewed readiness
verification, renewed drift verification, **the successor operational rebinding**, and an
authenticated one-shot external attestation.

That rebinding is mandatory, unperformed, and — as of this filing's preflight — **unauthorized**.
This decision authorizes exactly one future unit to perform it, and performs no part of it.

## Decision

### A. Determination — `STEP_8_EQUIVALENT_REBINDING_AUTHORIZED`

**Exactly one future, separate, bounded pull request is authorized** to perform the
`XASSET-0030` §G.B **step-8-equivalent** successor operational-authorization / load-bearing
rebinding against the exact merged bytes of the corrected executable package as they stand at that
unit's own verified base, effective only on this decision's own complete lifecycle closure (§J).

**Design only.** This filing writes no rebinding, edits
`level1_stage1_execution_authorization.py` not at all, and adds **zero activation authority**.
Stage 1 remains **UNARMED** and **NOT EXECUTABLE**, the lane remains **ABSENT**, and `ATTEMPT_1`
remains intact, unclaimed, and unconsumed.

**Merging this decision performs no rebinding and arms nothing.**

### B. The authority gap, reproduced from accepted text before anything was authorized

Each finding below is quoted from an accepted decision, not summarized from a task brief.

**B.1 — The required link is step 8's *equivalent*, and the citation is corrected rather than
repeated.** `XASSET-0030` §G.B step 8 requires "**one** successor operational-authorization /
load-bearing rebinding lifecycle against those exact merged bytes." **`XASSET-0037` performed that
one.** `XASSET-0043` §C states it exactly — "**`XASSET-0037` performed that one, and this decision
does not reopen, re-consume, or re-issue it.** Step 8's own single rebinding remains spent, and the
package it bound remains bound" — and `XASSET-0044` §C repeats it verbatim in substance.

A loose reading that "§G.B step 8 remains unperformed" is therefore **wrong on the accepted record**,
and this filing declines to adopt it. What remains mandatory and unperformed is the link
`XASSET-0041` §I names as link 2: "rebinding (separately authorized; `XASSET-0030` §G.B step-8
**equivalent**)" — *equivalent*, not *identical*: a lifecycle of the same kind and rigour, separately
authorized, and never a second draw on step 8's own spent budget. **The substance of the gap is
unchanged by this correction; only the citation is.** It is corrected here so that no future session
reads this authorization as reopening a budget three accepted decisions have recorded as spent.

**B.2 — `XASSET-0036` authorized steps 2–7 and expressly withheld 8–11.** `XASSET-0036` §A verbatim: "**Exactly
one future, separate, bounded `XASSET-0030` §G.B implementation PR is authorized**, covering §G.B
**steps 2 through 7**"; and "§G.B **steps 8 through 11** … **are NOT authorized here.**" §B.5 is
equally explicit: "Authorizing the package does not authorize the rebinding, and this decision
performs neither."

**B.3 — The link-2 grant was made, used, and permanently expended.** `XASSET-0043` §F granted
"**exactly one** future, separate, bounded pull request" to perform it. PR #344 was that unit.
`XASSET-0044` §L makes seven conditions conjunctive and its sixth requires successful merge-commit CI
at the exact merge SHA; run `32439614683` / job `96647501864` at `f5dedce1…` **failed**, permanently.
`XASSET-0045` §E states the consequence: "the *authorized unit was expended*. `XASSET-0043` therefore
**may not be reused** as authority." `XASSET-0044` remains **not effective**.

**B.4 — Neither recovery grant survives.** `XASSET-0045`'s own grant **never vested** — its lifecycle
stopped at the same condition, run `32490789238` / job `96797667282` at `2f8cdebe…`. `XASSET-0046` §F
granted exactly one recovery unit, and `XASSET-0047` §I closes it: "**Completing this unit authorizes
no further unit** — `XASSET-0046` §F granted exactly one, and this is it."

**B.5 — `XASSET-0047` repaired the anchor and nothing else.** `XASSET-0047` §A: the lifecycle anchor is rebound
"to **this** decision, **this** pull request … **Nothing else moves.**" `XASSET-0047` §I withholds, in terms, renewed
readiness verification, renewed drift verification, Step 11, any attestation, lane creation, arming,
claim, gate evaluation, execution, and results work.

**B.6 — `XASSET-0030` §D is a provision, not a grant.** §D provides for "a successor
operational-authorization **or reconciliation lifecycle**" whenever a lawful correction of
load-bearing code creates enforcement drift. It has never been treated as self-executing: `XASSET-0043`
§C lists §D as ground (1) and still required ground (3), "**the separate governance decision that
grants it**." §D says what kind of lifecycle is owed; it has never said who may open one.

**Conclusion.** Every candidate authority is spent by use, never vested, expressly withheld, or
non-executing. **No accepted authority currently permits a future step-8-equivalent rebinding unit**,
and the gap is closed here narrowly and expressly rather than by inference or by exhaustion.

### C. Relation to `XASSET-0027` §P.1 — separate, reserved, unconsumed

Stated expressly so no future author reads one permission as the other.

§P.1's exactly-one Stage-1 **evaluation/results** PR is **not consumed, replaced, amended, or counted
against** by this filing or by the rebinding it authorizes, on the three grounds `XASSET-0036` §C and
`XASSET-0043` §E already recorded: §P.1's PR "may make no production configuration change," and a
rebinding is nothing but production configuration change; §P.1's deliverable is a results document,
and neither this filing nor a rebinding produces one; and §P.1's PR sits **after** arming while both of
these sit strictly before it.

After this decision merges, and after the unit it authorizes merges, §P.1's budget is exactly what it
is today: **one, unspent.**

### D. Relation to `XASSET-0029` §E — not an activation PR, zero activation authorizations

`XASSET-0029` §E terminates the activation regress on a step that "**changes no repository state**" —
the external runtime attestation. This filing changes repository state, and the rebinding it authorizes
changes repository state extensively, so both are categorically outside the step §E terminates.
`XASSET-0036` §B.4 reached that conclusion for the implementation package, `XASSET-0037` §G for the
step-8 rebinding, and `XASSET-0043` §D for the link-2 rebinding, each on the same reasoning; it applies
unchanged here.

**This decision adds one authorized rebinding and ZERO activation authorizations.**
`stage_1_executability.executable` stays permanently `false` and keeps its enforced-false check. **No
committed value in this repository authorizes Stage-1 execution**, and neither merging this decision
nor merging the unit it authorizes changes that. Final activation remains the external one-shot runtime
attestation and the operator's act — never a merged pull request.

### E. Authority granted — exactly one future, separate rebinding unit

Effective only on this decision's own complete lifecycle closure (§J), **exactly one** future,
separate, bounded pull request may:

1. file its **own** rebinding decision record, under the next `XASSET-####` identifier **verified
   unused against live repository state at the time it is filed** — never predicted, reserved, or
   named here;
2. rebind the effective structural authorization source to that decision, and rebind
   `AUTHORIZING_PULL_REQUEST` and `REVIEWED_BASE_SHA` to that unit's own verified pull request and
   verified base (§F.1, §F.2);
3. edit `level1_stage1_execution_authorization.py` **only** to the extent that unit's own
   configuration, identity constants, evidence, refusals, and validation require (§F.3);
4. extend `LOAD_BEARING_RELPATHS` **additively** with the decision files that make the newly bound
   bytes lawful — this decision and the unit's own — removing nothing (§F.6);
5. amend the canonical artifacts **only** in authorization language, in lockstep, and only to the
   extent the rebinding's own authorization identity requires (§F.7);
6. recompute stale identities and pins **once**, after every authorized byte has stabilized (§F.8);
7. synchronize `governance/decisions.yaml` and the `WS-0014` register, and update the tests that pin
   the values it lawfully changes, **without weakening any of them**.

### F. The required properties of the authorized rebinding

Each is a condition on the authorized unit. **None is satisfied by this filing**, and none may be
waived by the unit that performs it.

**F.1 — Bind only stabilized, independently reviewed exact bytes.** The rebinding binds exact
git-object identities at its own accepted head and its own merge, never a value asserted in prose,
never a value computed before the bytes stabilized, and never a working-tree value no independent
review saw.

**F.2 — Bind against the exact merged package, re-derived live.** The bytes bound are the exact merged
state of the corrected `XASSET-0030` §G.B executable package as it stands at the authorized unit's own
verified base. That base must be re-derived from the git object store — parents in order, merge tree
byte-identical to the accepted-head tree, ancestry proved — and must be shown to descend from
`bb95ed26964b1bc7a2e230c76060fec82752efa1`, this filing's own verified `main`. A base asserted from a
task brief, a summary, or a moving reference is not a verified base.

**F.3 — Exact closed transitions, bound at both ends.** Every value the rebinding moves — each rebound
constant, each hash pin, each identity family member, each `LOAD_BEARING_RELPATHS` membership change,
and the lifecycle anchor itself — must be recorded as an **exact closed transition**: the old value and
the new value, both explicit, both bound, with the old value preserved rather than overwritten in the
record. A value that moves without both ends bound is drift wearing a rebinding's label. This is
`XASSET-0043` §G.6's ordering discipline restated as a completeness requirement, and it applies to the
lifecycle anchor (`AUTHORIZING_DECISION`, `AUTHORIZING_PULL_REQUEST`, `REVIEWED_BASE_SHA`) exactly as it
applies to every other moved value.

**F.4 — Bind canonical, enforcement, and *all* outcome-producing executable bytes.** This is
`XASSET-0030` §G.B's governing invariant, restated unchanged and not narrowed:

> **No outcome-producing executable code may be created, changed, or left outside the bound execution
> identity after the final rebinding and before `ATTEMPT_1`.**

The rebinding must therefore cover, exactly and by identity: the canonical artifacts; the
enforcement/validator surface; and every executable component capable of **deciding, ordering,
serializing, writing, or materially altering** the 680 Stage-1 outcomes — the deterministic runner, the
result writer/serializer, the result validator, and the deterministic derivation surface. Coverage must
be proved by exact byte identity, never asserted by naming.

**F.5 — Preserve the outcome surface's semantics.** The runner, the result validator, the universe
closure validator, the deterministic derivation surface, the frozen construction identities, the
cardinality **680 / 48**, the aggregate universe hash `73c0965e…5224`, `comparison_subject_kind`,
`unordered_pair_id`, every gate, every disposition rule, and the accepted B1 / B2 / B3 semantics are
**preserved unchanged**. The rebinding binds bytes; it does not get to move meaning. Any change to any
of them requires its **own separate, express** authorization and is outside this grant.

**F.6 — The trust boundary grows; nothing is removed.** `LOAD_BEARING_RELPATHS` may only be extended,
and only by the decision files that make the newly bound bytes lawful. No existing member may be
removed, swapped, or traded away, and the count must be shown to increase by exactly the additions
claimed.

**F.7 — Canonical amendment in authorization language only.** The canonical artifacts may be amended
only to carry the rebinding's own authorization identity, only in lockstep with each other, and only to
the extent the rebinding requires. No gate, threshold, disposition rule, universe value, or evidence
rule may move under cover of a canonical amendment.

**F.8 — Recompute identities and pins once, and last.** Stale module identities and canonical pins are
recomputed exactly once, strictly after every authorized byte has stabilized, so no pin carried forward
from a superseded head survives into the merged unit.

**F.9 — Preserve all adverse history and every predecessor identity.** `XASSET-0044` and `XASSET-0045`
remain **not effective**; `XASSET-0043` remains **spent**; `XASSET-0040` remains spent as
`STOPPED_BEFORE_ATTESTATION`. Both failed merge-commit CI runs — `32439614683` / job `96647501864` at
`f5dedce1…`, and `32490789238` / job `96797667282` at `2f8cdebe…` — and both auditable stop records
remain **immutable adverse history**. Neither may ever be re-run in place, relabelled successful,
deleted, suppressed, waived, described as passing, or represented as satisfying its decision's own
effectivity condition, and neither stopped lifecycle's closure may be posted retrospectively. Every
preserved predecessor identity family — `XASSET-0029`, `XASSET-0036`, the executable package,
`XASSET-0037`, `XASSET-0041`, `XASSET-0042`, `XASSET-0043`, `XASSET-0044`, `XASSET-0045`, `XASSET-0046`,
and `XASSET-0047` — is carried forward intact, and none is retired, weakened, or collapsed into another.

**F.10 — One unit, one pull request, full lifecycle.** The rebinding decision and the rebinding itself
belong in the same coherent pull request, exactly as `XASSET-0037` and `XASSET-0044` each were —
splitting them produces a decision whose bound bytes do not yet exist, and a rebinding whose governing
text is not yet inside the identity it binds. That pull request must complete, in full: independent
**FULL** exact-head review under `OPS-0007` §1; any required bounded correction and exact-head
re-review; explicit principal exact-head acceptance at the final head; normal merge; immediate
post-merge verification; **successful merge-commit CI whose `head_sha` is the exact merge SHA**; and
final post-CI verification and lifecycle closure. A future session finding a concrete technical reason
to package this differently must **stop and disclose**, never decide it silently.

### G. Authority withheld — absolute

The grant in §E **does not extend to**, and the authorized unit **must not** perform:

- renewed readiness verification (`XASSET-0030` §G.B step 9 / `XASSET-0041` §I link 3);
- renewed drift verification (§G.B step 10 / link 4);
- **Step 11** in any part (§G.B step 11 / link 5) — `XASSET-0040` stays spent as a stop;
- generating, pre-staging, or validating any **attestation**;
- creating `READY`, `CLAIMED`, or `COMPLETED` lane state, writing `AUTHORIZATION_ROOT`, or writing the
  lane ledger;
- **arming** Stage 1, or setting `stage_1_executability.executable` to anything but `false`;
- **claiming** or consuming any part of `ATTEMPT_1`;
- evaluating any gate for any registered construction;
- executing Stage 1, or performing any results work;
- producing a `stage1_results.yaml`, a per-construction disposition, a cell outcome, or a roll-up;
- acquiring market, fundamental, economic, or Stage-2 data, or any Stage 2 work;
- creating any endpoint, bound, point, range, percentage, weight, rank, target, or allocation;
- changing `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, the allocator,
  margin state, charts, ladders, trades, or orders;
- reading, listing, opening, or substantively reusing any `risk_lane_boundary` protected `RISK` result;
- reopening, re-deriving, or re-arguing B1, B2, or B3, or `XASSET-0031`'s `G3`;
- resolving `XASSET-0024` §K.1, or amending `XASSET-0020` §E.1;
- consuming any part of `XASSET-0027` §P.1's reserved results PR.

**Links 3, 4 and 5 each require their own separate authority and their own complete lifecycle.**
Completing the rebinding authorizes the next link no more than a clean step-10 result authorized
step 11 — the inference `XASSET-0039` §K already foreclosed and `XASSET-0041` §I restated.

### H. Packaging — one authorization, one rebinding unit

This decision is a **design-only Lane G governance authorization** under `OPS-0009`: it grants
authority and performs no production mutation. The rebinding is a separate unit, in a separate pull
request, with its own decision record, its own review, and its own lifecycle.

Its scope here is deliberately minimal: this decision file, its mechanism-based supporting test module,
the decision catalog row, and the factual `WS-0014` synchronization the register's own live fields
require. Advancing the register's shared `active_branch` / `active_pr` / `last_verified_main_sha`
fields necessarily updates the coupled predecessor suites that pin them; that is disclosed as
consequential, not silent, and no pinned value is weakened.

### I. Fail-closed

Every unobtainable fact is an **error**, never silent agreement. Ambiguity, drift, a competing
worktree, a dirty tree, an unexpected open pull request, or any condition that would require expanding
this authority is a **stop**, not a judgement call. This applies to the authorized unit exactly as it
applied to this filing.

### J. Effectivity — the rebinding may not begin before this lifecycle closes

This authorization becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007` §1;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the PR head's own run,
   and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request authorizes nothing; a green PR-head CI
run does not; principal acceptance does not; merge does not; and post-merge verification without a
successful exact merge-commit CI run does not. **Only complete closure of all seven does.**

These seven mirror the repository's own committed definition —
`level1_stage1_execution_authorization.REQUIRED_LIFECYCLE_GATES`, a six-element tuple that is itself
one of the sixteen load-bearing paths. **That module is cited only and is byte-unchanged by this
filing.** Conditions 5–7 are that tuple's last three members; condition 2 is the exact-head discipline
`OPS-0009` §6 applies to condition 1. `XASSET-0035`'s own lifecycle omission — an enumeration naming
four of six gates — is not repeated, and neither is the omission that let two predecessors merge with
their sixth condition outstanding.

**Merging this decision performs no rebinding and arms nothing.**

### K. This filing can attain both green PR-head and green merge-commit CI

The condition both `XASSET-0044` and `XASSET-0045` permanently failed is condition 6, so this filing
states its attainability rather than assuming it. This unit adds one decision file, one test module,
one catalog row, and factual register and coupled-suite synchronization. It changes no production
module, no canonical artifact, no validator, no runner, and no universe value. Its supporting artifact
proves its historical claims over **immutable commit ranges only**, and the full repository suite is
additionally run inside an isolated clone at a **simulated merged-`main` state where `HEAD` equals
`origin/main`** — the exact ref position that broke PR #345's assertions — before this filing is
offered for review.

No statement anywhere in this decision disclaims the ability to obtain successful merge-commit CI at
its own exact merge SHA. Such a statement would make §J.6 unreachable by construction, which is the
deadlock `XASSET-0045` shipped at its first reviewed head, and it is refused here in terms.

### L. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; creates no `AUTHORIZATION_ROOT`; arms and executes no Stage 1; creates no Stage-1 runner,
result writer, serializer, result validator, or `stage1_results.yaml`; consumes nothing of `ATTEMPT_1`;
**evaluates no gate for any construction and asserts no per-construction outcome**; closes no gate on
satisfaction and changes no gate's class, index, question, controlling authority, or failure
disposition; **performs no rebinding**, corrects no validator, extends no `LOAD_BEARING_RELPATHS`,
edits `level1_stage1_execution_authorization.py` not at all, and moves no lifecycle anchor; **amends no
canonical file and changes no hash pin, universe, cardinality, `comparison_subject_kind`,
`unordered_pair_id`, or construction identity**; performs no part of `XASSET-0030` §G.B steps 9, 10 or
11 and enters none of them; reuses neither `XASSET-0043` nor `XASSET-0045`, treats neither
`XASSET-0044` nor `XASSET-0045` as effective, and revives neither `XASSET-0040` nor either stopped
lifecycle; consumes no part of `XASSET-0027` §P.1's reserved results PR; acquires no market,
fundamental, economic, or Stage-2 data; resolves `XASSET-0024` §K.1 neither way and leaves
`XASSET-0020` §E.1 unamended; reopens neither B1, B2, nor B3, and leaves `XASSET-0031`'s `G3`
untouched; grants no Stage 2 and no application authority; selects no sleeve and creates no endpoint,
bound, point, range, percentage, weight, rank, target, or allocation; weakens no validator or test;
**reads, lists, opens, or references no `risk_lane_boundary` protected result path** and reuses no
`RISK` scenario, value, parameter, window, or result; changes no `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state; authorizes no
chart, ladder, deployment, trade, order, or brokerage action; and rewrites no accepted history.

**Stage 1 remains UNARMED and NOT EXECUTABLE. The lane is ABSENT. `ATTEMPT_1` is intact, unclaimed,
and unconsumed.**

## Rationale

The programme reached a state that is easy to misread: the lifecycle anchor works again, so the
machinery *looks* ready to proceed. It is not. `XASSET-0047` repaired the mechanism's ability to
authenticate its own authorizing pull request; it did not bind a single byte of the corrected
executable package, and it said so in terms.

The gap this closes is therefore not a defect anyone introduced. It is the deliberate result of four
consecutive filings each declining to hand the next one authority it had not earned: `XASSET-0043`
granted exactly one rebinding unit and that unit permanently stopped; `XASSET-0045`'s grant never
vested; `XASSET-0046` granted exactly one recovery unit and `XASSET-0047` spent it; and `XASSET-0047`
expressly authorized no successor. Every one of those is the right posture in isolation, and together
they leave a mandatory step with no live permission attached to it. That is precisely the situation a
governance filing exists to resolve, rather than a future implementer resolving it on momentum.

**Why an express grant rather than an inference.** Two readings were available and both were rejected
on their own terms. Reading `XASSET-0030` §D as self-executing would make the "successor
operational-authorization or reconciliation lifecycle" phrase into a standing permission — but
`XASSET-0043` §C, the only accepted filing to rely on §D, still listed a *separate governance decision*
as a distinct and necessary ground, so §D has never been treated as a grant by anything that used it.
Reading `XASSET-0030` §G.B step 8 as still unspent would contradict three accepted decisions that
record it as spent by `XASSET-0037`. §B.1 corrects that citation openly rather than quietly adopting
the convenient version, because a filing that mis-states which budget it draws on teaches a future
session to draw on the wrong one.

**Why the properties in §F are conditions rather than advice.** Each corresponds to a failure this
programme has actually had. §F.3's both-ends binding is the shape `XASSET-0043` §G.6 already required
and `XASSET-0047`'s own MAJOR finding showed can be satisfied vacuously if the historical end is
derived from the current one. §F.4 is `XASSET-0030` §G.B's own corrected invariant, added after a DELTA
review found the runner's bytes sitting outside the bound identity. §F.9 exists because two failed CI
runs and two auditable stops are the most tempting records in this repository to quietly reinterpret,
and `ATTEMPT_1` is non-rerunnable after claim.

**Why design-only.** A filing that both granted the authority and exercised it would be its own
authorizing decision — the circularity `XASSET-0046` §E refused, and the reason that filing separated a
grant from its use. Keeping this unit to a decision, a test module, a catalog row, and a register
synchronization also keeps its own condition 6 attainable, which is the condition that stopped the last
two units that tried to do more.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Treat `XASSET-0030` §G.B step 8 as still unspent and proceed under it | Contradicts `XASSET-0043` §C, `XASSET-0044` §C, and `XASSET-0037`'s own determination; would re-consume a budget three accepted decisions record as spent |
| Treat `XASSET-0030` §D as self-executing authority | §D states what kind of lifecycle is owed, never who may open one; `XASSET-0043` §C relied on §D **and** still required a separate granting decision |
| Reuse `XASSET-0043` §F for a second attempt | §F granted exactly one unit; PR #344 was it, and `XASSET-0045` §E records the grant as expended by use |
| Reuse `XASSET-0045` §F or `XASSET-0046` §F | `XASSET-0045`'s never vested; `XASSET-0046`'s was spent by `XASSET-0047`, which says so in §I |
| Read `XASSET-0047` as having performed or implied the rebinding | §A: "Nothing else moves"; §I withholds it in terms; its own closure names the rebinding as still outstanding |
| Combine the authorization and the rebinding in one filing | Circular — the unit would authorize itself, the shape `XASSET-0046` §E refused |
| Authorize links 3, 4 and 5 at the same time | `XASSET-0041` §I requires each to have its own authority and its own lifecycle; batching them is the inference `XASSET-0039` §K foreclosed |
| Also correct `XASSET-0047` §K's two carried-forward observations | Neither is authority on its own, and acting on them here would exceed "only as strictly necessary"; they remain carried forward, unacted on |
| Leave the `WS-0014` shared fields stale rather than touch coupled suites | The register's live fields would then assert a merged pull request as active work; `OPS-0001` requires the register to be verified against live state |

## Consequences

- Exactly one future, separate, bounded pull request may perform the step-8-equivalent successor
  operational-authorization / load-bearing rebinding, under §E's grant and §F's conditions, once §J's
  seven conditions all close.
- That unit files its own decision under the next live-verified `XASSET-####` identifier, which this
  filing deliberately does not name.
- `XASSET-0043` remains spent; `XASSET-0044` and `XASSET-0045` remain not effective; `XASSET-0040`
  remains spent as a stop; both failed merge-commit CI runs and both auditable stops remain immutable.
- `XASSET-0027` §P.1's results PR remains **one, unspent**.
- `XASSET-0029` §E's no-infinite-regress rule is untouched: final activation remains the external
  one-shot runtime attestation and the operator's act.
- Links 3, 4 and 5 of `XASSET-0041` §I remain unauthorized, unperformed, and unreachable without their
  own separate governance decisions.
- **Stage 1 remains UNARMED and NOT EXECUTABLE, the lane remains ABSENT, and `ATTEMPT_1` remains
  intact, unclaimed, and unconsumed.**
