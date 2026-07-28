---
decision_id: OPS-0009
date: 2026-07-28
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, OPS-0004, OPS-0005, OPS-0006, OPS-0007, OPS-0008, GOV-0001, GOV-0002]
supporting_artifact: null
---

## Context

`OPS-0007` established a capability-based independent-review standard and a provisional-Intelligence
bridge; `OPS-0008` established the Research Wave Protocol v1 — a source-readiness gate, a default
two-PR lifecycle, and read-only post-merge verification — specifically for WS-0005 Milestone 3
research batches. Both are working well for the scope they name, but that scope is narrow: WS-0005
research waves. The rest of this repository's governance and implementation work — process
decisions, mechanical register/index synchronization, bounded corrections to an open PR, single-file
factual updates — currently defaults to the same undifferentiated, full-weight lifecycle regardless
of how small or purely-factual the change is. That creates friction proportional to how many times a
change touches the repository, not to how much risk it actually carries, and it leaves no named,
auditable rule for *when* a lighter process is legitimate versus when it is simply skipped controls
wearing a faster label.

The principal separately identified four specific corrections to apply on top of the design this
decision would otherwise have proposed: (1) merge and post-merge verification must be one continuous
step performed immediately by the session that merges, never deferred to a later, unrelated session;
(2) a delta review after correction is legitimate only when the correction is bounded to the
reviewer's own findings, authority is unchanged, scope is unchanged, material behavior is unchanged,
and the evidence/assumptions underlying the original review remain valid — otherwise a full exact-head
re-review is required; (3) mechanical Git actions stay role-bounded (authors commit/push/open-or-update
their own draft PR; independent reviewers never edit, push, or merge; the principal or a designated
merge coordinator marks ready, merges, and performs post-merge verification; no separate session is
needed solely for a mechanical action that already belongs to the current session's assigned role); and
(4) consuming an independently validated, frozen evidence bundle requires only recomputing and matching
its SHA-256 — not repeating line/word/byte/source/claim/orphan/reciprocity counts — unless the hash
changed, no retained independent validation exists, or a specific integrity concern is documented.

**Preflight performed this session, independently verified, not assumed:** repository confirmed
`Mast3rkey/Portfolio-HQ`; `origin/main` fetched and pruned; local `main` and `origin/main` identical at
`173fef5` (the merge commit of PR #181, `PI-0031`/Batch 9 CVX); working tree clean on branch
`claude/lean-delivery-review-governance-uv4tl2`; **zero open pull requests** in the repository; no
branch or in-flight work overlapping this filing's scope. `governance/decisions.yaml` carries 42
entries, reconciling exactly against the 42 non-`README` files under `governance/decisions/` —
highest filed `OPS-####` is `OPS-0008`, highest `PI-####` is `PI-0031` — confirming **OPS-0009** as the
next unused identifier in its series, checked live against both the directory and the index. `OPS-0007`
and `OPS-0008` were re-read in full: neither defines change-type lanes, a session-continuation
(KEEP/START NEW/SESSION DONE) rule, role-bounded mechanical-Git-action boundaries as standalone
operative text, or reusable task-packet/final-report templates — this decision is new coordination
doctrine, not a restatement of either.

## Decision

**OPS-0009 adopts Lean Delivery and Review Lifecycle v1**: a lane-based lifecycle for governance and
implementation work across this repository, plus two reusable templates (a task packet, a final
report). It **cross-references, and does not restate**, `OPS-0007`'s twelve-point capability-based
review standard and five-part PROVISIONAL definition, and `OPS-0008`'s Research Wave Protocol v1
(source-readiness gate, default two-PR lifecycle, read-only post-merge verification, hard boundaries).
Both remain fully in force, unedited, for the work they already govern — `OPS-0008` for WS-0005
Milestone 3 batches specifically, `OPS-0007` §1 for any WS-0005 review gate generally. OPS-0009 governs
what neither already scopes: how much preflight, review, and process weight a given piece of
governance or implementation work needs, based on what kind of change it actually is.

This decision authorizes no research, no Company/Theme Intelligence content, no tier/target/role/
cluster/cap/holdings/margin/allocator/production-code change, no Batch 10, and no Milestone 4. It
creates no investment or trading authority of any kind. **As the founding instance of this lifecycle,
OPS-0009 is itself filed, reviewed, and merged under the full, unreduced lifecycle already in force
before this decision** — it may not invoke its own lanes to reduce its own review, principal-acceptance,
or merge requirements (see §13).

### 1. Lanes by change type

- **Lane G — Governance authorization.** A new, amending, or superseding decision record; a standing
  protocol; anything that creates, narrows, or restates repository authority. Always full weight:
  independent exact-head review, retained attribution, explicit principal acceptance. Never reduced by
  this decision.
- **Lane R — Research/Intelligence content.** Company or theme records, comparison artifacts, freshness
  rows. Governed by `OPS-0008` where WS-0005 batches apply, or by the equivalent `PI-####`
  first-coverage discipline elsewhere. OPS-0009 changes nothing about Lane R's substance — it only
  clarifies, in §§2-5 below, which of Lane R's existing steps are load-bearing controls versus
  restatable bookkeeping.
- **Lane M — Mechanical/factual synchronization.** A register or index update, a post-merge note, a
  decision-index regeneration, or a factual PR-number sync that **records an already-true, already-
  verified fact and adds no new claim, authority, or interpretation.** The leanest lane: no independent
  review is required beyond the merge coordinator's own §9 verification, provided every fact stated is
  independently re-derived from live repository/GitHub state at filing time, not copied forward.
- **Lane C — Bounded correction.** A correction responding to a specific finding on an already-open,
  already-reviewed PR. Governed by §6 (delta review vs. full re-review).

A change spanning more than one lane (e.g., a governance filing that also records a mechanical fact)
is governed by its **heaviest** applicable lane in full.

### 2. Mandatory controls vs. removable duplication

**Mandatory, in every lane except a purely mechanical Lane M change:**

- independent, exact-head review by an eligible reviewer (`OPS-0007` §1, unchanged, cross-referenced);
- a retained, attributable review (GitHub review/comment thread, or a `governance/audits/` artifact);
- explicit principal acceptance at the exact final head, before merge;
- protected-path / scope-diff verification — the merged diff matches the authorized file list exactly;
- validator/test verification for the domain each changed file actually belongs to;
- immediate post-merge verification by the merge coordinator (§9);
- disclosure of unresolved findings, evidence-access limits, and assumptions.

**Removable or reducible, only when the named condition holds — never by default assumption:**

- restating a full narrative rationale already stated in a cross-referenced decision — cross-reference
  it instead (this decision does exactly that for `OPS-0007`/`OPS-0008` above);
- a dedicated reconciliation PR filed solely to record an already-true fact — `OPS-0008` §4's read-only,
  folded-into-the-next-filing convention, unchanged, cross-referenced, not restated here;
- recomputing line/word/byte/source/claim/orphan/reciprocity counts on a frozen, already independently
  validated evidence bundle — governed by §4 below;
- running the full, unrelated investment/production-code test suite locally purely for ceremony, when
  exact-head CI already covers it and the change's own files don't implicate that domain — governed by
  §5 below;
- a fresh, one-off principal sign-off for a recovery or process pattern `OPS-0008` §2 already
  standing-preauthorizes.

No control listed as mandatory above may be reclassified as removable by any future session's own
judgment — only a future governance decision may move an item between the two lists.

### 3. Scope-sensitive preflight

Preflight depth follows the lane, not a fixed checklist:

- **Lane G:** full preflight — repository identity, `origin/main` fetch-and-prune, exact-SHA match,
  clean working tree, an open-PR/conflicting-branch scan, identifier confirmation against both the
  directory and `governance/decisions.yaml`, and a re-read of every directly governing decision — the
  same depth this filing itself performed above.
- **Lane R:** `OPS-0008` §§1-2's preflight and source-readiness gate, unchanged, not reduced.
- **Lane M:** confirm only the specific facts being recorded against live state (exact SHA, merge
  status, test/validator pass, count reconciliation) — no requirement to re-verify facts outside the
  narrow record being made.
- **Lane C:** confirm the exact head under active review has not drifted since the review being
  corrected, and confirm — explicitly, in writing — whether every §6 delta-review condition actually
  holds before choosing delta review over full re-review.

### 4. Evidence identity — SHA-only reuse

When a future session consumes an evidence bundle that has already been independently validated and
retained (a `governance/audits/` artifact, a frozen research packet, a pinned protocol hash), it need
only **recompute the bundle's SHA-256 and confirm it matches the retained, previously validated value.**
Line, word, byte, source, claim, orphan, or reciprocity counts already performed during that bundle's
own independent validation do not need to be repeated, **unless:**

- the hash does not match (the bundle has changed since it was validated);
- no retained independent validation of that exact bundle exists yet; or
- a specific, documented integrity concern is raised about that bundle.

A hash match is treated as full re-verification of everything the original validation already checked
— it is not a weaker substitute for it.

### 5. Change-sensitive local testing, exact-head CI reliance

Local testing is scoped to the validators/tests whose domain the changed files actually belong to (for
example: YAML parsing and decision-index reconciliation for a governance-only change; the Intelligence
validator suite for an Intelligence-content change). **The full unrelated investment/production-code
test suite is not required to be run locally** for a change that does not touch that code — reliance
shifts to **exact-head CI, which must still complete successfully before merge** regardless of lane.
This is a reliance shift, not a waiver: CI passing at the exact merged head remains mandatory in every
lane.

### 6. Correction, delta-review, and full re-review triggers

A **delta review** (re-review scoped only to what changed since the prior review) is permitted after a
correction **only when all four hold:**

1. the correction is bounded strictly to the reviewer's own stated findings;
2. authority is unchanged (no new tier/target/role/cluster/cap/holdings/margin/allocator claim is
   introduced by the correction);
3. scope is unchanged (no file outside the originally authorized list is touched);
4. material behavior is unchanged, and the evidence and assumptions underlying the original review
   remain valid (no new fact has surfaced that the original reviewer did not have).

**If any one of the four fails, a full exact-head re-review is required** — the same
bounded-correction-then-re-review mechanism `OPS-0007` §1.11 already establishes, with these four
conditions naming precisely when "bounded correction" stays a delta and when it must restart as a full
review. When in doubt, treat it as failing (§10).

### 7. KEEP / START NEW / SESSION DONE

A session-continuation rule for whoever is executing a lifecycle step, independent of lane:

- **KEEP** (continue the current session): the next unit of work belongs to the role this session
  already holds, targets the same exact head or the session's own direct follow-up commit, and does not
  require an independent perspective this session cannot honestly provide.
- **START NEW** (a different session must take over): the next required action is independent review of
  this session's own authored work (no self-review — `OPS-0007` §1.1, restated at §8 below); a
  different, unrelated decision or workstream needs isolated context; or the next actor is explicitly
  the principal or a designated merge coordinator rather than the author or reviewer already at work.
- **SESSION DONE**: this session's role-bounded action for the current lifecycle step is complete and
  the next step's role belongs to someone else. End the turn without extending scope — exactly the
  "open the draft PR, then stop" boundary this filing itself operates under.

### 8. Role-bounded mechanical Git actions

Restated as this protocol's own standalone text, not left to cross-reference alone:

- an **author** may commit, push, and open or update their own draft PR;
- an **independent reviewer** does not edit, push, or merge — review and retained attribution only;
- the **principal or a designated merge coordinator** may mark ready, merge, and perform post-merge
  verification;
- **no separate session is required solely for a mechanical action that already belongs to the current
  session's assigned role** — an author session does not need a second session to push its own next
  commit, and a merge-coordinator session does not need a second session to perform its own immediate
  post-merge check.

### 9. Merge and post-merge verification — one continuous step

Merge and post-merge verification are a single lifecycle step, not two. **The verification itself —
ancestry (the reviewed head is the merge commit's direct parent), scope (the merged diff matches the
authorized file list exactly), validator/test re-confirmation, and protected-path byte-identity
confirmation — must be performed immediately, by the same session that performs the merge, and must
never be deferred to a later, unrelated session.** This narrows nothing in `OPS-0008` §4 about
*packaging* — a dedicated reconciliation PR is still the exception, not the default, and the fact of a
completed verification may still be *recorded* via the next filing that already touches the relevant
register, per `OPS-0008` §4(a)/(b). What changes is *timing*: the check itself is never left for
whoever happens to open the next PR.

### 10. Conservative escalation

When lane classification is ambiguous, when an evidence bundle's validity is uncertain, when any one
of §6's four delta-review conditions is unclear, or when any control's necessity is genuinely in
doubt — **default to the heavier lane, the full re-review, and the fuller preflight, and escalate to
an explicit principal decision rather than assuming the lean path.** Ambiguity is never resolved in
favor of less control.

### 11. Hard boundaries

- Nothing in this decision may be cited to skip, weaken, or delay independent review, exact-head
  anchoring, retained attribution, principal acceptance, protected-path verification, or post-merge
  verification for any change carrying new authority or substantive content.
- **Efficiency, speed, or an informal "this is obviously fine" judgment is never itself authority to
  bypass a control listed as mandatory in §2.**
- No tier, target, role, cluster, cap, holdings, margin, allocator, or production-code change of any
  kind is created, authorized, or implied by this decision.
- No Company/Theme Intelligence content, research finding, Batch 10, or Milestone 4 work is authorized.
- This decision narrows nothing in `OPS-0007` or `OPS-0008` beyond the timing clarification in §9, which
  adds rigor rather than removing it.
- This decision is filed and must be merged under the full, unreduced lifecycle in force before it — it
  may not be cited, by this filing or any later one, as retroactively lightening its own review or
  merge requirements.

### 12. Governance package scope (this filing)

This filing touches exactly: this `OPS-0009` file; `governance/decisions.yaml` (one new entry);
`governance/templates/lean_task_packet.md`; `governance/templates/lean_final_report.md`; `CLAUDE.md`
(one concise Decisions Log pointer, not a restatement of this file). **No other file is touched.**
This is a cross-cutting process decision, not a single workstream's authorization — it therefore does
not add an entry to `operations/WORKSTREAMS.yaml`; a future workstream that adopts this lifecycle for
its own work records that fact in its own register entry when it happens, not here.

### 13. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. **Nothing in §§1-11
becomes effective until this PR merges to `main`.** This decision does not mark itself ready and does
not authorize its own merge.

## Rationale

**Why lanes, not a single reduced process for everything.** `OPS-0008`'s own audit already showed that
uniform process weight produces proportional, not risk-scaled, overhead: a mechanical register sync and
a five-company research wave were following the same three-to-four-PR shape. Naming lanes by what a
change actually is — new authority, research content, a recorded fact, or a bounded correction — lets
the process weight track the actual risk instead of the number of times a change happens to touch the
repository.

**Why SHA-only reuse is safe.** A frozen, already-independently-validated bundle's identity is fully
captured by its hash. Recomputing derived counts (lines, words, sources, claims) a second time over an
unchanged bundle adds no verification power beyond confirming the hash is unchanged — the counts were
already proven correct once, by an independent reviewer, against that exact byte sequence. A hash
mismatch, a missing prior validation, or a documented integrity concern each independently restore full
re-verification, so this reduction cannot silently paper over an actual change.

**Why immediate post-merge verification, not `OPS-0008` §4(b)'s later-filing option applied to timing.**
`OPS-0004`'s own Finding FA-1, and `OPS-0006` §16.1's "none of the following, alone, constitutes
completion," both exist because this repository has already seen what happens when a claimed
verification's provenance goes unretained or unperformed at the moment it should occur. `OPS-0008` §4(b)
answers a *packaging* question — which PR records the verification — and that answer is unchanged here.
The principal's correction answers a different, *timing* question: the check itself must happen now, by
whoever merges, not whenever the next session gets to it.

**Why role-bounded mechanical actions, restated rather than left to cross-reference.** `OPS-0007` §1.1
already forbids self-review; restating the full role split here (author / reviewer / merge coordinator)
as standalone text, the same discipline `OPS-0008` §12 already applied to its own hard boundaries,
prevents a future session from reading a "lean" lifecycle as license to blur roles that were never in
question.

**Why a named KEEP/START NEW/SESSION DONE rule.** Nothing in `OPS-0007`/`OPS-0008` currently states when
a session should hand off versus continue — that gap is exactly where "efficiency" could quietly become
an excuse to self-review or to over-extend a session past its assigned role. Naming the three outcomes
makes the hand-off decision an explicit, auditable step rather than an implicit one.

## Alternatives Considered

- **Apply `OPS-0008`'s Research Wave Protocol wholesale to all governance work, not just WS-0005
  batches.** Rejected — `OPS-0008` is purpose-built for multi-company research waves (wave sizing,
  source-readiness gate); forcing a one-file mechanical sync or a single-clause protocol decision
  through it would either dilute its research-specific discipline or add irrelevant steps to trivial
  changes.
- **Leave preflight/review depth to each future session's informal judgment, with no named lane
  structure.** Rejected — informal judgment is exactly the "efficiency as authority" failure mode this
  decision exists to prevent; naming lanes makes both the reduction and its limits explicit and
  auditable.
- **Allow delta review as the default for any correction, not just the four-condition subset.**
  Rejected per the principal's own correction — an unbounded delta-review default risks papering over a
  finding that actually changes authority, scope, or evidence validity, which a full re-review exists
  specifically to catch.
- **Defer post-merge verification's timing to whenever is convenient, matching `OPS-0008` §4(b)'s
  packaging allowance.** Rejected for timing specifically — §4(b) answers which PR records the
  verification, not whether the check happens immediately; the principal's correction requires the
  actual check now, closing the same provenance gap `OPS-0004` Finding FA-1 identified elsewhere.
- **Add a new machine-readable lane-classification schema field.** Rejected — no such schema exists to
  extend without its own separate authorization (the same reasoning `OPS-0007` §3 already applied to
  refusing an Intelligence schema field); lane classification lives in this decision's prose and the
  task-packet template, not a new machine field.

## Consequences

**Authorized, effective on this decision's merge:** Lean Delivery and Review Lifecycle v1 — lanes by
change type (§1), the mandatory-versus-removable control split (§2), scope-sensitive preflight (§3),
SHA-only evidence reuse (§4), change-sensitive local testing with exact-head CI reliance (§5),
correction/delta-review/full-re-review triggers (§6), the KEEP/START NEW/SESSION DONE rule (§7),
role-bounded mechanical Git actions (§8), immediate merge-plus-verification (§9), conservative
escalation (§10), and the hard boundaries in §11 — plus two reusable templates,
`governance/templates/lean_task_packet.md` and `governance/templates/lean_final_report.md`.

**Unchanged by this decision:** `OPS-0001` through `OPS-0008` in full, unedited; every existing tier,
target, role, cluster, cap, and holding in `targets.yaml`/`holdings.yaml`; `allocate.py`,
`margin_state.py`, every existing Company/Theme Intelligence record and validator; the 1.8x leverage cap
and 30% buffer floor; `MARGIN-0005`'s research charter and trial ceiling; `OPS-0006`'s Milestone 4-9
authorization boundary.

**Not authorized by this decision:** Batch 10; Milestone 4 or any later WS-0005 milestone; any
investment, allocation, tier, target, margin, or production-code change; any reduction of this filing's
own review, correction, or merge requirements before it merges.
