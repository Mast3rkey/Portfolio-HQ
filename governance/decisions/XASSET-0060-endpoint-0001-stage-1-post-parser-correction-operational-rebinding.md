---
decision_id: XASSET-0060
date: 2026-08-27
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0036, XASSET-0037, XASSET-0040, XASSET-0041, XASSET-0042, XASSET-0043, XASSET-0044, XASSET-0045, XASSET-0046, XASSET-0047, XASSET-0048, XASSET-0049, XASSET-0050, XASSET-0051, XASSET-0052, XASSET-0053, XASSET-0055, XASSET-0056, XASSET-0057, XASSET-0058, XASSET-0059, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_post_parser_correction_operational_rebinding.py
---

## Context

`XASSET-0057` authorized **exactly one** future, separate, bounded step-8-equivalent rebinding, and
made its grant **conditional** on a separately authorized, independently reviewed, principal-accepted,
merged, exact-merge-CI-green and lifecycle-closed **parser correction** (`§F.0`). That correction has
since happened, in two lifecycles, and both have closed in full. **This is that rebinding.** It is the
single unit `XASSET-0057 §E` permits, and it performs the reconciliation that decision expressly
refused to perform itself.

### Live preflight

Every anchor below was independently re-resolved from live git and live GitHub **before anything was
edited**. Nothing is quoted from a task brief, and no identity is asserted from prose.

| Fact | Verified |
|---|---|
| Base | `301e79334876a4bda6e7b89a6156b34e8d38a605` — GitHub `main`, `origin/main`, the local checkout and this branch's base all equal it |
| Open pull requests | **zero** |
| Worktree | clean, single worktree, synchronized with `origin/main` |
| Identifier | `XASSET-0060` verified **unused** against live repository state — absent from `governance/decisions/`, from `governance/decisions.yaml`, and from every tracked file at the base tree |

### The three prerequisite lifecycles, each closed in full

`XASSET-0057 §F.0.3` is emphatic that **merged is not effective**, and that **two** lifecycles must
close on top of `XASSET-0057`'s own. All three were re-verified independently, condition by condition.

**`XASSET-0057` itself (PR #358) — its own `§J` seven conditions:**

| | Evidence |
|---|---|
| FULL review | `5026362328` @ `a7f4909…` — adverse; four bounded corrections followed |
| Final exact-head review | `5030740306` @ `53d2d3d770f379393a1a3fde4408915c9fcf81f0` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE** |
| Principal acceptance | `issuecomment-5425835377`, naming that exact head |
| Normal merge | `556a43cf91679d3e8ca95703c8d49e672b662b73` — parents `583022a5…` then `53d2d3d7…`, **in that order**; merge tree byte-identical to the accepted head's tree |
| Post-merge verification | `issuecomment-5425857818` |
| Merge-commit CI | run `32973075626`, `event: push`, `run_attempt: 1`, `completed`/`success`, `head_sha` **equal to the exact merge SHA** |
| Final closure | `issuecomment-5426014312` — "`XASSET-0057` is EFFECTIVE" |

**Lifecycle A — `XASSET-0058`, the parser-correction AUTHORIZATION (PR #359):**

| | Evidence |
|---|---|
| A1 FULL review | `5034171910` @ `48a6ea0…` — `CHANGES REQUIRED`, 2 BLOCKING |
| A2 corrected + re-reviewed | `5035960873` @ `e8d53c184a7612ab6e38ba8d7ae1e348f7046de2` — **APPROVED**, 0 BLOCKING |
| A3 principal acceptance | `issuecomment-5432460504`, naming that exact head |
| A4 normal merge | `34c45900ce23742d04d80cf12471c34aabe9682d` — parents `556a43cf…` then `e8d53c18…`; tree byte-identical to the accepted head's |
| A5 post-merge verification | `issuecomment-5432479068` |
| A6 merge-commit CI | run `33024792395`, `head_sha` **equal to the exact merge SHA**, attempt 1, `completed`/`success` |
| A7 final closure | `issuecomment-5432562310` |

**Lifecycle B — `XASSET-0059`, the parser correction ITSELF (PR #360):**

| | Evidence |
|---|---|
| B1 implementation | 7 linear commits, zero merges, 22 files |
| B2 FULL review | `5037196415` @ `ebec2f1…` — `BOUNDED CORRECTION REQUIRED`, 1 MAJOR |
| B3 corrections + re-reviews | delta `5041611657` @ `0082fae…` — MAJOR **unresolved**, a relocation rather than a removal; then delta `5044822360` @ `90b829863875223d56b8da2c62ba0bfc06fbcd7e` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0/0/0/0 |
| B4 principal acceptance | `issuecomment-5444698584`, naming that exact head |
| B5 normal merge | **`301e79334876a4bda6e7b89a6156b34e8d38a605`** — parents `34c45900…` then `90b82986…`, **in that order**; merge tree `3bf579d64fd86680668d628f557b86e66ab7e76a` **byte-identical** to the accepted head's own tree |
| B6 post-merge verification | `issuecomment-5444767925` |
| B7 merge-commit CI | run **`33112432925`**, job **`98658423867`**, both `head_sha` **equal to the exact B5 merge SHA**, `run_attempt: 1`, `completed`/`success`, 10 of 10 steps |
| B8 final closure | `issuecomment-5444905083` |

`XASSET-0057 §F.2` requires the base, the SHA tested by B7 and the SHA named by B8 to be **the same
commit**, and requires this unit to prove it. They are: `301e7933…`, in all three roles.

### What this unit is

The fail-closed condition `XASSET-0057` existed to authorize repairing is still live at this base.
`_verify_git_anchored_identity` is byte-identical to its own base and still raises `enforcement
drift`, because the register binds a module identity the merged tree no longer carries. All three
authorization predicates return `False`, the lane is `ABSENT`, and Stage 1 is **NOT EXECUTABLE**.

This unit reconciles that register with the **parser-corrected** bytes — role 3 of `§F.3`'s chain,
not role 2, which may never be bound. It moves three lifecycle constants, preserves their old values
rather than overwriting them, extends the trust boundary additively, and changes nothing else.

## Decision

### A. Determination — `POST_PARSER_CORRECTION_REBINDING_PERFORMED`

The `XASSET-0057 §E` grant is **consumed** by this unit. It authorized exactly one rebinding; this is
it, and no further rebinding may draw on it.

**Merging this decision arms nothing.** `stage_1_executability.executable` remains `false`, no
attestation is generated, the lane stays `ABSENT`, and `ATTEMPT_1` remains intact, unclaimed and
unconsumed. Authorization remains two-factor and external, exactly as `XASSET-0029` established.

### B. The base — equality, derived from the completed lifecycle and proved from the object store

`XASSET-0057 §F.2` states one rule and no exception: **the base must EQUAL the Lifecycle B
implementation's normal-merge commit at B5.** That commit was never predicted anywhere — `XASSET-0057`
was accepted before `XASSET-0059` existed — so it was **derived**:

1. Lifecycle A (`A1`–`A7`) confirmed closed, above.
2. Lifecycle B (`B1`–`B8`) confirmed closed, above.
3. PR #360's `merge_commit_sha` read from live GitHub: `301e7933…`.
4. Its parents read from the **local object store**: `34c45900…` then `90b82986…` — two, ordered,
   first parent the prior `main`, second the accepted head.
5. `origin/main` re-resolved: **exactly** `301e7933…`.

**Zero intervening commits.** `XASSET-0057 §F.2` removed every admission path — "if `main` carries
**any** commit between the B5 implementation merge and the authorized unit's base, that unit **may not
proceed on the strength of this authorization**, full stop." That clause is not reached: `main` *is*
the B5 merge. Had it not been, the only lawful route would have been a new, superseding authorization,
and this unit would have stopped.

**Equality, not descent.** Ancestry is retained as necessary history and is explicitly insufficient
authority. `_verify_post_parser_correction_base_equality` decides the whole proposition — equality,
well-formedness, and retained ancestry — as a pure function, so it refuses a later descendant even
when ancestry is granted unconditionally.

### C. The module identity chain — four roles, one ordered statement, only the last bound

`XASSET-0057 §F.3` withdrew the "two ends, already known" formulation as self-contradictory. There are
four roles, and **only role 4 is ever bound**. Every value is derived from the git object store.

| # | Role | SHA-256 | blob | Introduced at |
|---|---|---|---|---|
| 1 | **Previously bound** | `4ff289416b9a95614fb3c05b6b0ac432382c63d7464d00f0ff16af12b39d4541` | `f71b08b4ebe95f161c57cdbb2a924748f13af02d` | `8ab77386…` (`XASSET-0049`) |
| 2 | **Vulnerable intermediate** | `12eab05e64dec5113ab16383ad0fb5423f843dba0070e345652387d25be604a5` | `b5622f9e412afd604a11cde04317b79c5e57920a` | `f1bf3fd0…` (`XASSET-0056`) |
| 3 | **Parser-corrected** | `1283a2d4ccc3794fd37b81d4e5e23ac6f67a0b87b911ef3861c724d636fabd00` | `b8414a69f41e37f8fdd5c18dae13176fd847170e` | `90b82986…` (`XASSET-0059`), merged at `301e7933…` |
| 4 | **Final stabilized post-rebinding** | `ROLE4_SHA256_PENDING` | `ROLE4_BLOB_PENDING` | this unit's own final head |

**Adjacent transitions, each proved from the object store, each end bound:**

* **1 → 2** — `8ab77386…` → `f1bf3fd0…`, ancestor-ordered. Recorded as **history, not adoption**:
  role 2 is the state that existed and was **refused**, never a value the register moves to.
* **2 → 3** — `f1bf3fd0…` → `90b82986…`, ancestor-ordered. Role 3 was **derived at the parser
  correction's own merge**, per `§F.0.4`, and never predicted.
* **3 → 4** — role 3 → this unit's own stabilized bytes, recomputed once and last per `§F.9`.

**The register transition this rebinding actually performs is `4ff28941…` → role 4.** Role 1 is
preserved, not overwritten. Role 2 is a **permanent negative pin**: `NEVER_BINDABLE_MODULE_SHA256`
and `_verify_module_identity_is_not_the_vulnerable_intermediate` turn `§F.0`'s "may never be rebound"
from prose into a refusal that fires against the merged tree itself. Role 3 is never bound directly.

**Role 4 is not a constant inside the module, and cannot be** — a file cannot carry its own post-edit
SHA-256 without changing that SHA-256 by carrying it. It is derived from the merged tree at validation
time by `_verify_git_anchored_identity`, which is exactly why that function reads `blob_sha256_at`
rather than comparing against a literal. Its measured value is recorded **here**, once, last, in a
file whose bytes are not the module's.

### D. Exact closed transitions — `XASSET-0057 §F.3`

Every moved value, both ends explicit, the old end preserved rather than overwritten.

| Constant | Old — retained | New | Old value preserved as |
|---|---|---|---|
| `AUTHORIZING_DECISION` | `XASSET-0049` | `XASSET-0060` | `PRIOR_STEP8_EQUIVALENT_DECISION` |
| `AUTHORIZING_PULL_REQUEST` | `349` | `PR_NUMBER_PENDING` | `PRIOR_STEP8_EQUIVALENT_PULL_REQUEST` |
| `REVIEWED_BASE_SHA` | `f052efad38e3d57e3e5615799ac3bcbebe83ff5f` | `301e79334876a4bda6e7b89a6156b34e8d38a605` | `STEP8_EQUIVALENT_AUTHORIZING_MERGE_SHA` **and** `PRIOR_STEP8_EQUIVALENT_MERGE_BASE` |

**The prior-anchor family is mandatory, not decorative.** Reproduced against the live module *before*
this rebinding was written, exactly as `XASSET-0049` reproduced it for `XASSET-0047`: `XASSET-0049`'s
own merge `a9414554…` and accepted head `b2059e80…` appeared under **no constant anywhere**. They were
reachable only through the three fields this unit moves. Moving them without `PRIOR_STEP8_EQUIVALENT_*`
would not have weakened `XASSET-0049`'s identity — it would have **destroyed** it.

Three further families are added, each for a relationship no existing constant carried:
`POST_PARSER_CORRECTION_AUTHORIZING_*` (`XASSET-0057`, PR #358 — this unit's authority),
`PARSER_CORRECTION_AUTHORIZING_*` (`XASSET-0058`, PR #359 — Lifecycle A), and
`PARSER_CORRECTION_IMPLEMENTATION_*` (`XASSET-0059`, PR #360 — Lifecycle B, whose B5 merge this
unit's base must equal). All four new merges join the inherited-merge verification table on the same
terms as every predecessor: exact ordered parents, merge tree byte-identical to the accepted head's,
and ancestry into this rebinding's own merge.

### E. The pull-request number was never guessed

The first commit on this branch carried the sentinel `-3` — a **negative, structurally impossible**
pull-request number that can never validate by accident, and deliberately distinct from
`XASSET-0047`'s `0`, `XASSET-0048`'s `-1` and `XASSET-0049`'s `-2`, so this unit's sentinel can never
be mistaken for a predecessor's. The draft pull request was then opened, GitHub issued its own number,
that number was read back from live GitHub, and only then was it bound — and re-verified against the
live pull request's own head, base and state. A wrong number still fails closed at
`verify_lifecycle_against_truth`; the point of the sentinel is that the failure can never be silent.

### F. The trust boundary grows from eighteen to twenty-five — additive only

`XASSET-0057 §F.7` requires direct membership for **every** decision that makes the newly bound bytes
lawful, and deliberately **states no predicted final figure**, because the parser-correction chain's
length was not yet known when it was written. The count is therefore **derived from the actual
completed chain**, not guessed.

Enumerated at the base: **18**. Enumerated after: **25**. Seven additions, nothing removed, no member
altered, reordered, swapped or traded away, and the first eighteen entries byte-identical in content
and order:

| # | Added path | Relationship it protects |
|---|---|---|
| 19 | `XASSET-0053-…-parser-contract-correction-authorization.md` | accepted authorization for the parser-contract correction |
| 20 | `XASSET-0055-…-verdict-boundary-governance.md` | accepted verdict-boundary governance |
| 21 | `XASSET-0056-…-formal-disposition-parser-correction.md` | the accepted parser correction as implemented |
| 22 | `XASSET-0057-…-post-parser-correction-rebinding-authorization.md` | the authority for **this** rebinding |
| 23 | `XASSET-0058-…-parser-correction-authorization.md` | Lifecycle A |
| 24 | `XASSET-0059-…-formal-disposition-parser-correction.md` | Lifecycle B — the bytes this unit binds |
| 25 | `XASSET-0060-…-post-parser-correction-operational-rebinding.md` | **this** decision |

`§F.7` names the first four at minimum and anticipates the rest in terms: "every future accepted
decision that authorizes or implements the `§F.0` prerequisite parser correction — however many that
turns out to be". `XASSET-0058` and `XASSET-0059` are exactly that, and did not exist when `§F.7` was
written. All four of `XASSET-0053`, `XASSET-0055`, `XASSET-0056` and `XASSET-0057` were verified
**absent** from the tuple at this base before extending, as `§F.7` records.

**`XASSET-0054` remains excluded.** `§F.7` permits admission **only** on independent evidence that it
is operative, "never on the strength of appearing in a narrative, a related-decisions list, or this
enumeration". That evidence was sought and **not found**: its identifier is consumed, its pull request
closed unmerged, and no `XASSET-0054` decision file exists anywhere on `main` — verified directly
against the merged tree, not inferred. `XASSET-0045`'s file likewise stays absent, for the reason
`XASSET-0047` gave: it authorizes nothing, so binding it would assert a relationship that does not
exist. **Citation is not membership**; only a path in the tuple is inside the boundary.

### G. Canonical artifacts — an express determination, not an omission

**The canonical artifacts are not amended by this unit.** `XASSET-0057 §F.8` permits amendment "only
to the extent the rebinding requires", and `§F.4` requires the **smallest strictly necessary**
rebinding. Neither `PROTOCOL_V1.md` nor `pre_registration.yaml` carries any of the three moved values,
verified directly: they name `XASSET-0044` as `rebound_by` and as
`effective_structural_authorization_source`, which **remains literally true**, because `XASSET-0044`
is still the last decision that amended those canonical **bytes** and this unit amends none of them.

`XASSET-0047` drew that distinction and `XASSET-0049` preserved it; it is preserved again here. *Which
decision last rebound the canonical bytes* and *which decision's lifecycle the mechanism authenticates
against* are **different relationships**, and overloading them is the failure mode `XASSET-0037 §C`
named. `stage_1_executability.executable` stays `false`.

### H. Preserved unchanged — the outcome surface and all adverse history

Per `§F.5`, nothing about meaning moves. The deterministic runner, the result writer and serializer,
the result validator, the universe closure validator, the derivation surface, the canonical
construction inputs, the frozen construction identities and their **ordering**, the cardinality
**680 / 48**, the aggregate universe hash `73c0965e…5224`, `comparison_subject_kind`,
`unordered_pair_id`, every gate, every disposition rule, the accepted B1 / B2 / B3 semantics, and every
protected portfolio and `risk_lane_boundary` `RISK` path are **untouched**. This rebinding binds bytes;
it does not get to move meaning.

Per `§F.10`: `XASSET-0044` and `XASSET-0045` remain **not effective**; `XASSET-0043` remains **spent**;
`XASSET-0040` remains spent as `STOPPED_BEFORE_ATTESTATION`; `XASSET-0054` remains **consumed and never
reused**. Every retained negative pin is preserved, both failed merge-commit CI runs and both auditable
stop records remain immutable adverse history, and none is re-run in place, relabelled, deleted,
suppressed, waived or described as passing. Role 2 joins that record as a **permanent negative pin**.

### I. Three further refusals this rebinding adds

Refusals 5 and 6 still name `XASSET-0047` and `XASSET-0048` and are **not weakened** — they simply no
longer describe the anchor's live neighbours, and a refusal that has stopped naming the live pair has
stopped refusing anything. Three more are added against the current pair:

7. the **superseded anchor** may not silently remain the anchor — `XASSET-0049` / `#349` are refused;
8. the **authority** may not be mistaken for the **unit** — `XASSET-0057` / `#358` are refused, because
   `§A` of that decision says in terms that merging it performs no rebinding;
9. neither **prerequisite lifecycle** may be mistaken for this unit — `XASSET-0058` / `#359` and
   `XASSET-0059` / `#360` are refused, because `§G` forbids this unit from correcting the parser and
   an anchor naming either would claim their work as this rebinding's own.

A fourth refusal guards the identity itself: `_verify_module_identity_is_not_the_vulnerable_intermediate`
fires when the merged tree's module identity is `12eab05e…604a5`, whatever the recorded and working
values say. It is **not** redundant with the agreement checks around it: a rebinding that bound the
vulnerable module perfectly consistently would satisfy every agreement check and still install a known
fail-open parser as the accepted enforcement anchor.

### J. Relation to `XASSET-0027 §P.1` and `XASSET-0029 §E`

`XASSET-0027 §P.1`'s reserved **evaluation/results** pull request is **not consumed, replaced, or
counted against** by this unit, and stays reserved and unspent. This is a rebinding, not results work.

`XASSET-0029 §E`'s no-infinite-authorization-regress rule is **intact and unweakened**. This is not an
activation pull request: it generates no attestation, arms nothing, and adds **zero** activation
authorizations. Final activation remains the external one-shot runtime attestation and the operator's
act, never another merged pull request.

### K. Authority withheld — absolute

Carried forward verbatim in effect from `XASSET-0057 §G`. This unit does not and may not: perform
renewed readiness verification; perform renewed drift verification; perform **Step 11** in any part;
generate, pre-stage or validate any **attestation**; create `READY`, `CLAIMED` or `COMPLETED` lane
state, write `AUTHORIZATION_ROOT`, or write the lane ledger; **arm** Stage 1 or set
`stage_1_executability.executable` to anything but `false`; **claim** or consume any part of
`ATTEMPT_1`; evaluate any gate for any registered construction; execute Stage 1 or perform any results
work; produce a `stage1_results.yaml`, a per-construction disposition, a cell outcome or a roll-up;
acquire market, fundamental, economic or Stage-2 data; create any endpoint, bound, point, range,
**percentage**, weight, rank, target or allocation; change `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, the allocator, margin state, charts, ladders, trades or
orders; read, list, open or substantively reuse any `risk_lane_boundary` protected `RISK` result;
**correct the parser or alter parser semantics** — that work is `XASSET-0058`/`XASSET-0059`'s and is
complete; reopen, re-derive or re-argue B1, B2 or B3, or `XASSET-0031`'s `G3`; resolve
`XASSET-0024 §K.1` or amend `XASSET-0020 §E.1`; or consume any part of `XASSET-0027 §P.1`.

**Links 3, 4 and 5 each require their own separate authority and their own complete lifecycle.**
Completing this rebinding authorizes the next link no more than a clean step-10 result authorized step
11 — the inference `XASSET-0039 §K` foreclosed and `XASSET-0041 §I` restated.

### L. Packaging and fail-closed

`XASSET-0057 §F.12` requires the rebinding decision and the rebinding itself in **one** coherent pull
request — as `XASSET-0037`, `XASSET-0044` and `XASSET-0049` each were — because splitting them produces
a decision whose bound bytes do not yet exist, and a rebinding whose governing text is not yet inside
the identity it binds. This unit is packaged exactly that way. No concrete technical reason to package
it differently was found; had one been found, `§F.12` requires stopping and disclosing, not deciding
silently.

Every unobtainable fact is an **error**, never silent agreement (`§I`). Ambiguity, drift, a competing
worktree, a dirty tree, an unexpected open pull request, or any condition requiring expanded authority
is a **stop**.

### M. Effectivity

This rebinding becomes effective **only** after **all** of the following are complete for this
decision's final accepted head and the resulting merge:

1. independent **FULL** exact-head review under `OPS-0007 §1`;
2. any required bounded correction and exact-head re-review, so condition 1 holds at the **final**
   accepted head;
3. explicit principal exact-head acceptance at that final head;
4. normal merge;
5. immediate post-merge verification;
6. **successful merge-commit CI whose `head_sha` is the exact merge SHA** — not the pull request head's
   own run, and not a run against any other commit;
7. final post-CI verification and lifecycle closure.

**None is individually sufficient.** Opening this pull request changes nothing; a green PR-head CI run
does not; principal acceptance does not; merge does not; and post-merge verification without a
successful exact merge-commit CI run does not. **Only complete closure of all seven does.** These
mirror `REQUIRED_LIFECYCLE_GATES`, the repository's own six-element committed tuple: conditions 5–7 are
its last three members, and condition 2 is the exact-head discipline `OPS-0009 §6` applies to condition
1. `XASSET-0044` and `XASSET-0045` each merged and neither became effective, because condition 6
failed; that history is why the enumeration is stated in full rather than abbreviated.

### N. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED` or `COMPLETED`
lane state; creates no `AUTHORIZATION_ROOT`; arms and executes no Stage 1; creates no Stage-1 runner,
result writer, serializer, result validator or `stage1_results.yaml`; consumes nothing of `ATTEMPT_1`;
**evaluates no gate for any construction and asserts no per-construction outcome**; closes no gate on
satisfaction and changes no gate's class, index, question, controlling authority or failure
disposition; corrects no parser and alters no parser semantics; **amends no canonical file and changes
no hash pin, universe, cardinality, `comparison_subject_kind`, `unordered_pair_id` or construction
identity**; performs no part of `XASSET-0030 §G.B` steps 9, 10 or 11 and enters none of them; treats
neither `XASSET-0044` nor `XASSET-0045` as effective and revives neither `XASSET-0040` nor either
stopped lifecycle; reuses neither `XASSET-0054` nor any consumed identifier; consumes no part of
`XASSET-0027 §P.1`'s reserved results pull request; acquires no market, fundamental, economic or
Stage-2 data; resolves `XASSET-0024 §K.1` neither way and leaves `XASSET-0020 §E.1` unamended; reopens
neither B1, B2 nor B3, and leaves `XASSET-0031`'s `G3` untouched; grants no Stage 2 and no application
authority; selects no sleeve and creates no endpoint, bound, point, range, **percentage**, weight,
rank, target or allocation; weakens no validator and no test; **reads, lists, opens or references no
`risk_lane_boundary` protected result path** and reuses no `RISK` scenario, value, parameter, window or
result; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator,
tier, cluster, cap or margin state; authorizes no chart, ladder, deployment, trade, order or brokerage
action; and rewrites no accepted history.

**Stage 1 remains UNARMED and NOT EXECUTABLE. The lane is ABSENT. `ATTEMPT_1` is intact, unclaimed
and unconsumed.**

## Rationale

`XASSET-0056` left a deliberate, fail-closed mismatch: the parser was corrected and the register's
bound digest was not moved, so the enforcement mechanism refused rather than quietly accepting bytes
no rebinding had authorized. `XASSET-0057` was then filed to authorize repairing it — and refused to
repair it itself, on the ground that the bytes it would have bound carried a **live** parser defect.
That refusal is the reason this unit exists in the shape it does.

The distinctive feature of `XASSET-0057`'s grant is that it is **conditional on work that did not yet
exist**. `§F.0` made a separately authorized, independently reviewed, merged, CI-green and closed
parser correction a conjunctive prerequisite; `§F.0.1` established that the defect was a **family**,
not three code points, by measuring deletion, substitution, insertion, transposition and confusable
mutations across all seventeen prefix positions; `§F.0.2` set eight requirements the correction had to
satisfy; and `§F.0.3` required **two** full lifecycles to close, because this repository has twice
merged a decision that never became effective. Each of those conditions was checked here against live
evidence rather than against a summary, and the two failed predecessors are exactly why.

The base rule deserves its own note. `XASSET-0057 §F.2` **withdrew** the rule every predecessor
rebinding used — "your base equals your own authorization's merge" — because that rule and a mandatory
intervening parser correction cannot both hold. The replacement names one commit and permits no
exception and no admission path. That is why this unit's base is the `XASSET-0059` merge rather than
the `XASSET-0057` merge, why the equality is decided by a **new** pure function rather than by reusing
the step-8 one, and why the step-8 function is left completely unchanged: the two decide different
propositions about different commits, and reusing one would have produced a correct verdict under a
message that misattributes the governing rule.

Role 2 is treated as a permanent negative pin rather than as a superseded value because `§F.0` says so
in terms — "at any time, under any reading, however unchanged `main` may be". Implementing it as a
refusal rather than as a comment is the difference between a property and a hope: a rebinding that
bound the vulnerable module *consistently* would pass every agreement check the module already had.

The trust boundary grows by seven rather than by the four `§F.7` enumerates because `§F.7` deliberately
declined to name a final figure and instead required the count to be **derived** from the completed
chain. The chain turned out to be six decisions long plus this one. Binding the implementation's bytes
while leaving the decisions that define what the parser must do outside the boundary would protect the
code and not the authority over it.

## Alternatives considered

**Amend the canonical artifacts to name `XASSET-0060`.** Rejected. `§F.4` requires the smallest
strictly necessary rebinding and `§F.8` permits canonical amendment only to the extent required.
Neither canonical file carries any moved value, and `rebound_by: XASSET-0044` remains literally true.
`XASSET-0047` and `XASSET-0049` each reached the same determination expressly; a third silent departure
would overload two different relationships onto one field.

**Reuse `_verify_step8_equivalent_base_equality` with the new merge.** Rejected. The function is pure
and generically parameterised, so it would have returned the right verdict — under an error message
attributing the rule to `XASSET-0048 §F.2` and calling the `XASSET-0059` merge a "step-8-equivalent
authorization merge", which it is not. A refusal whose stated reason is false is a worse artifact than
a second small function. The original is left byte-unchanged and still exercised by its own tests.

**Rename or retire the step-8 constants now that the anchor has moved.** Rejected. `§F.10` requires
every predecessor identity family to be carried forward intact, and `STEP8_EQUIVALENT_AUTHORIZING_*`
additionally carries the old `REVIEWED_BASE_SHA` value at one of its two preserved ends.

**Record role 4 as a constant inside the module.** Impossible, not merely undesirable: a file cannot
carry its own post-edit digest. The mechanism already derives it from the merged tree, and the measured
value belongs in this decision, recomputed once and last.

**Split the decision and the rebinding into two pull requests.** Rejected — `§F.12` forbids it, and the
reason is structural: the decision file is itself member 25 of the boundary it defines.

## Consequences

The register is reconciled with the parser-corrected bytes, so `_verify_git_anchored_identity` no
longer raises `enforcement drift` for a stale digest. **This does not arm anything.** All three
authorization predicates continue to return `False` on their own terms — no attestation exists, the
lane is `ABSENT`, and `stage_1_executability.executable` is `false`. Stage 1 remains **UNARMED and NOT
EXECUTABLE**, and `ATTEMPT_1` remains intact, unclaimed and unconsumed.

The `XASSET-0057` grant is now **spent**. Any further rebinding requires its own new authority, its own
review and its own complete lifecycle, exactly as `XASSET-0048`'s grant was spent by `XASSET-0049` and
`XASSET-0043`'s by `XASSET-0044`.

The trust boundary is meaningfully larger: twenty-five paths, including for the first time every
decision that authorizes or defines the formal-disposition parser's behaviour. A future edit to any of
them after an attestation would now be caught by exact-byte identity rather than passing unnoticed.

`XASSET-0057 §M`'s disclosed residual and `XASSET-0058 §D.8`'s terminating-colon residual are
**preserved, not closed**, by this unit. Whether either warrants further work is a separate question
for a separate decision.
