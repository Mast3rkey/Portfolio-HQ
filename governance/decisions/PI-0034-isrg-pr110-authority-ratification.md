---
decision_id: PI-0034
date: 2026-07-29
status: Proposed
category: portfolio_intelligence
related_decisions: [GOV-0002, OPS-0004, OPS-0007, OPS-0008, OPS-0009, OPS-0010, PI-0009, PI-0016, PI-0031, PI-0032, PI-0033]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin/main` fetched.** `git fetch origin main` returned no new commits; `git rev-parse origin/main`
  and local `HEAD` both confirmed `36972737b96e99b0b8c9cdc0711fe4d605d1971a`, matching this filing's
  expected preflight cutoff exactly. Working tree confirmed clean on branch
  `claude/pi-0034-isrg-ratification-09mtqi` before any edit.
- **`36972737b96e99b0b8c9cdc0711fe4d605d1971a` is PR #194's merge commit** — confirmed via `git log
  --oneline` ("Merge pull request #194: WS-0005 M3 six-record fresh-retrospective-review retention"),
  present at `origin/main`'s tip.
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open` → `[]`).
  **No overlapping ISRG governance branch** confirmed via `list_branches` — no branch beyond this
  filing's own targets the ISRG authority gap.
- **`OPS-0010`** confirmed `status: Accepted` in both its own frontmatter and `governance/decisions.yaml`,
  merged via PR #191/#192, with its own retrospective implementation (PR #193) and the six-record
  fresh-review retention unit (PR #194) both merged and present on `main` at this cutoff.
- **ISRG confirmed the sole remaining held-back Company Intelligence record.** `operations/
  WORKSTREAMS.yaml`'s WS-0005 entry and the retained `governance/audits/
  WS0005_M3_SIX_RECORD_FRESH_RETROSPECTIVE_REVIEW_RETENTION_20260729.md` (§9-§11, Set 4) both record
  the current 45-record partition as 27 confirmed PROVISIONAL + 11 eligible-pending-PR-#193's-lifecycle
  + 6 eligible-pending-PR-#194's-lifecycle + **1 held back (ISRG only)** — independently re-confirmed
  this session by direct comparison against all 45 `intelligence/companies/*.yaml` filenames.
- **The current decision index contains `PI-0033` as its highest-filed `PI-####` entry, and no
  `PI-0034` entry exists yet** — confirmed against both `governance/decisions/` (46 files, excluding
  `README.md`) and `governance/decisions.yaml` (46 entries), reconciled with no orphans.
- **Read in full this session, not relied on from memory**: `constitution/
  INVESTMENT_CONSTITUTION.md`; `GOV-0002`; `OPS-0004`; `OPS-0007`; `OPS-0008`; `OPS-0009`; `OPS-0010`;
  `PI-0016`; `PI-0031`; `PI-0032`; `PI-0033`; `governance/decisions/README.md` and `governance/
  templates/decision_template.md` (decision-file and index conventions); the retained PR #193
  independent-review comment (`https://github.com/Mast3rkey/Portfolio-HQ/pull/193#issuecomment-5117143327`,
  the merged PR #193 audit's controlling review) and its principal-acceptance comment
  (`issuecomment-5117275717`); the retained PR #194 six-record retention artifact
  (`governance/audits/WS0005_M3_SIX_RECORD_FRESH_RETROSPECTIVE_REVIEW_RETENTION_20260729.md`); the
  merged `governance/audits/WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_20260729.md` (PR #193's
  own audit artifact, §6.11 ISRG); `decision_log.yaml`'s `PI-0009` entry; current `operations/
  WORKSTREAMS.yaml`; the current `intelligence/freshness_registry.yaml` ISRG row; and PR #110's own
  commit history (`8c7755e`, disclosing "an unscheduled, principal-authorized evidence refresh
  prompted by the tier review").
- **PI-0034 confirmed the correct next identifier**, checked live against both the directory and the
  index, not assumed. No repository fact conflicts with the principal's stated design approval.

### Principal design approval

The principal approved the following design for this filing, in these terms:

> "Approve the PI-0034 design for narrow retrospective ratification of ISRG PR #110, with no ISRG
> content changes and one later freshness-registry and WORKSTREAMS synchronization unit."

**This approval authorizes drafting PI-0034. It does not constitute acceptance of this decision's
final text, does not authorize its merge, does not declare ISRG PROVISIONAL, does not close Milestone
3, and does not authorize Milestone 4.** This filing performs no research, no content review, and no
lifecycle determination itself.

### The ISRG authority gap this decision responds to

Two independent, retained sources — the merged `WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_
20260729.md` (§6.11) and the retained, independent PR #193 review comment
(`issuecomment-5117143327`) — both found, without either resolving it, that ISRG's Stage B refresh
(PR #110, merge commit `19042313909266be5f92f939cfa0bbc2dbca55f9`) has **no identifiable governing
`PI-####` (or other) authorization anywhere in `governance/decisions/` or `decision_log.yaml`**. PR
#110's own commit `8c7755e` discloses the refresh proceeded on "an unscheduled, principal-authorized
evidence refresh prompted by the tier review" — a conversational-authorization claim, not a citation
to a filed decision. This is the same category of gap `decision_log.yaml`'s own `PI-0009` entry
already disclosed for ISRG's *original* creation record (the "PI-0009 Human Approval Record" named in
PR #80's content "does not correspond to any committed repository document identified"), and the
same standard `PI-0016` §1 states directly: "Per-company selection must be its own durable,
repository-filed governance record — not an informal chat sign-off." Unlike `OPS-0004`'s Finding
FA-1 (which closed a *review-retention* gap for already-authorized work), this gap is in the
underlying refresh *action* itself, not merely in how its review was retained.

The same PR #193 review comment separately and explicitly assessed ISRG's *current* merged content
and found it sound: "Content itself is sound (schema valid, sourcing honest, disconfirming evidence
present)... 6 of 7 [held-back tickers reviewed], no BLOCKER or content-level MATERIAL finding
survived independent review... ISRG is different in kind, not degree" — its sole MATERIAL finding for
ISRG is the authority gap itself, not a content defect. "Content quality does not cure this — a
well-written record with no governing authorization remains an authority gap."

## Decision

**PI-0034 performs one narrow, present-day governance act: a retrospective ratification of the ISRG
Stage B refresh merged via PR #110, supplying the authorization that action has always lacked,
without editing any ISRG file, without claiming that authorization existed at the time PR #110
merged, and without curing or bypassing the authority requirement `PI-0016` states.** This filing
creates no Company Intelligence record, no comparison artifact, no freshness-registry edit, and no
`operations/WORKSTREAMS.yaml` edit — it authorizes exactly one later, separate, bounded
synchronization unit to make those factual updates once this decision itself is `Accepted`.

### 1. Purpose

Resolve the sole remaining WS-0005 Company Intelligence authority gap — ISRG — through a narrow,
explicit, present-day governance act, so that ISRG's lifecycle status rests on an actual filed
decision rather than an unresolved disclosure.

### 2. Factual finding

This decision records, as fact:

- PR #110 refreshed the ISRG Company Intelligence record (`intelligence/companies/ISRG.yaml` and
  `ISRG.md`), merge commit `19042313909266be5f92f939cfa0bbc2dbca55f9`.
- **No controlling accepted authorization for that refresh has been identified** — exhaustively
  searched, twice, independently, by two separate retained sources (the PR #193 audit artifact and
  the PR #193 independent review comment), against `governance/decisions/`, `governance/
  decisions.yaml`, and `decision_log.yaml`. Neither search found one.
- **Conversational or informal authorization is not sufficient repository authority.** PR #110's
  commit `8c7755e`'s own disclosed "unscheduled, principal-authorized evidence refresh" claim is
  exactly the category `PI-0016` §1 already excludes ("not an informal chat sign-off") and the same
  category `decision_log.yaml`'s own `PI-0009` entry already disclosed for a different ISRG-adjacent
  claim (the "PI-0009 Human Approval Record" naming "a conversational approval, not a committed
  document").
- **This decision does not claim authority existed historically.** It does not rewrite, backdate, or
  reinterpret PR #110's own history — the absence of authority at the time of that merge is disclosed
  as fact, not obscured.

### 3. Content-quality separation

This decision records, separately from §2, as fact:

- The retained independent PR #193 review (`issuecomment-5117143327`) found the *current* ISRG
  record substantively sound — "schema valid, sourcing honest, disconfirming evidence present" — with
  **no BLOCKER or MATERIAL content defect**, its sole MATERIAL finding for ISRG being the authority
  gap in §2, not a defect in the record's substance.
- **That review is evidence about content quality only.** It does not, and cannot, supply the missing
  authorization §2 identifies — content quality and governing authority are independent questions,
  and a sound record does not retroactively authorize the action that produced it.
- **Content quality did not cure, and does not cure, the authority gap.** No fresh company research
  or content edit is required, authorized, or performed by this decision.

### 4. Bounded ratification

**PI-0034 provides one narrow, one-time, present-day retrospective ratification of the ISRG refresh
merged through PR #110** (merge commit `19042313909266be5f92f939cfa0bbc2dbca55f9`), effective only on
this decision's own merge. This ratification:

- **Supplies authority prospectively, through this present governance act** — the authorization
  begins to exist on this decision's own accepted merge, not before.
- **Ratifies PR #110 as merged** — the content already on `main` at that merge commit, unchanged by
  this decision.
- **Does not pretend PR #110 was authorized when originally merged.** The gap disclosed in §2 remains
  true, historical fact; this decision closes it going forward, exactly as `OPS-0004` closed a
  review-provenance gap "prospectively... not retroactively erased," applied here to an authorization
  gap rather than a review-retention gap.
- **Is not a general license for unauthorized research or later ratification.** This is a one-time
  act for this one identified gap. It does not establish a standing practice of retrospectively
  ratifying future unauthorized refreshes, and does not reduce `PI-0016`'s or any other governing
  decision's authorization requirement for any other company or any future ISRG refresh.
- **Does not alter any other company record or historical work.** No other Company Intelligence
  record, decision, or merged PR is touched, reopened, or reinterpreted by this ratification.

### 5. Current ISRG record

**`intelligence/companies/ISRG.yaml` and `intelligence/companies/ISRG.md` remain unchanged by this
decision.** This filing does not reopen, revise, or edit:

- thesis;
- evidence;
- conviction (`conviction.rating: High` unchanged);
- portfolio role (`portfolio_role_ref: T2` unchanged);
- tier;
- target;
- weight;
- monitoring criteria;
- thesis-break conditions.

Nothing in this decision constitutes new company research, a content review, or a substantive
finding about ISRG's business, evidence, or thesis.

### 6. Retained review

The retained independent PR #193 review comment (`https://github.com/Mast3rkey/Portfolio-HQ/pull/
193#issuecomment-5117143327`, posted before PR #193's merge, anchored to reviewed head
`6eac98c742666d2ea8645427c16b49c994f7d57d`) is identified as the current-record content-review
evidence for ISRG, per the PR #193 review lifecycle. **That retained review may satisfy the relevant
content-review element** of any future `OPS-0007` §3 determination for ISRG's record — this decision
does not require a fresh content review to be performed as a precondition of its own ratification,
since the ratification in §4 addresses authority, not content.

**This decision's own text — the PI-0034 decision itself — requires its own independent exact-head
review**, per `OPS-0007` §1 and `OPS-0009`'s Lane G (governance authorization) discipline: full
weight, no reduction. **The reviewer of PI-0034 must verify the scope and boundaries of this
ratification and the authority gap it responds to — not repeat ISRG company research or
re-adjudicate the retained PR #193 content review.**

### 7. Principal acceptance

Before this governance PR may be marked ready or merged, a separately retained pre-merge statement,
beginning exactly:

> Principal acceptance:

must exist, meeting every requirement `OPS-0010` §2 already establishes for WS-0005 lifecycle
acceptance (this decision is filed after `OPS-0010`'s own merge, so its going-forward standard
applies in full):

1. Identify PI-0034's exact accepted head SHA.
2. Explicitly accept the narrow ratification of ISRG PR #110 described in §4 — not a general
   acceptance of "the PR" or "the change."
3. Be distinguishable from the independent-review verdict required by §6.
4. Be distinguishable from the mechanical merge action.
5. Precede merge.
6. Never be inferred from silence, authorship, timing, or merge metadata.

### 8. Later synchronization unit

**Authorized only after PI-0034 itself becomes `Accepted` controlling authority**: one later, separate,
bounded implementation PR (not opened by this filing) affecting exactly:

1. `intelligence/freshness_registry.yaml` — the ISRG row's `company_record_authority` field only,
   updated to reflect this decision as the authorization now governing the Stage B refresh (currently
   `PI-0009`, which governs Stage A/original creation only and has never been updated to reflect the
   PR #110 refresh).
2. `operations/WORKSTREAMS.yaml` — the ISRG lifecycle entry and the Milestone 3 criterion-7 partition
   (currently 27 confirmed PROVISIONAL + 17 eligible-pending-prior-PRs'-lifecycles + 1 held back),
   synchronized to reflect ISRG's new status once its own lifecycle completes — using only
   `OPS-0001`'s existing schema and status vocabulary, no new field.
3. One short audit or retention artifact under `governance/audits/`, filed only if current repository
   convention (`OPS-0008` §7's combined-artifact preference; `OPS-0009`'s Lane M discipline) requires
   one for this synchronization to be independently falsifiable.

**No ISRG YAML or Markdown file is touched by that later unit.** It is a lifecycle-and-registry
synchronization only, not a content edit.

The later unit must independently complete its own full lifecycle:

- its own independent, exact-head review, per `OPS-0007` §1;
- its own separately retained pre-merge `Principal acceptance:` statement, per `OPS-0010` §2;
- merge at its own unchanged accepted head;
- immediate post-merge verification, per `OPS-0009` §9.

### 9. Effective status

- **PI-0034's own merge, by itself, does not make ISRG effectively PROVISIONAL.** This decision
  supplies authority for the PR #110 refresh (§4) and identifies the retained content review (§6); it
  does not itself perform, or substitute for, the merge-and-post-merge-verification elements
  `OPS-0007` §3 requires.
- **ISRG remains held back until the later synchronization unit (§8) completes its own full
  lifecycle** — review, correction if required, principal acceptance, merge, and post-merge
  verification.
- **The later unit may result in all 45 currently-filed Company Intelligence records reaching
  effective PROVISIONAL status only after that unit's own merge and successful post-merge
  verification** — not on this decision's merge alone, and not as an automatic consequence of this
  ratification.

### 10. Prohibited scope

This decision, and the later synchronization unit it authorizes, prohibit, under any interpretation:

- Any edit to `intelligence/companies/ISRG.yaml` or `intelligence/companies/ISRG.md`.
- Any new ISRG research.
- Any change to ISRG's conviction, portfolio role, tier, target, weight, cluster, cap, holdings, or
  allocation.
- Any margin change.
- Any production-code or test change.
- Any `allocate.py` change.
- Any trading or order execution.
- Any automatic ranking, scoring, or policy inference.
- Any reinterpretation or silent expansion of `PI-0009`, `PI-0016`, `OPS-0007`, or `OPS-0010`'s own
  substance — this decision cites each, narrowly, and edits none.
- Any declaration that Milestone 3 is complete.
- Any Milestone 4 authorization.

### 11. Milestone boundaries

Stated explicitly, controlling over any contrary inference:

- **PI-0034 does not complete Milestone 3.**
- **Its later synchronization unit (§8) does not automatically complete Milestone 3** — even a fully
  successful synchronization, resolving ISRG to effective PROVISIONAL, does not by itself satisfy
  `PI-0031` §K's seven-criterion completion standard.
- **A separate, later Milestone 3 completion determination remains mandatory**, evaluating all seven
  of `PI-0031` §K's criteria together, exactly as `PI-0031`, `PI-0032`, and `PI-0033` already state.
- **Milestone 4 remains unauthorized** — nothing in this decision, or in the unit it authorizes,
  authorizes, implies, or narrows the gate `OPS-0006` §5 established for it.

### 12. Completion evidence

PI-0034 decision completion requires, together, not individually:

1. Eligible independent, exact-head review retained, per §6.
2. Explicit `Principal acceptance:` statement retained, per §7.
3. The unchanged accepted head merged to `main`.
4. Immediate post-merge verification complete, per `OPS-0009` §9.
5. This decision file and `governance/decisions.yaml` synchronized to `status: Accepted` through the
   repository-standard lifecycle.

**None of these conditions is currently satisfied.** This filing opens as a draft PR with `status:
Proposed` in both this file and the index; it does not mark itself, or authorize marking itself,
ready for merge.

### 13. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/PI-0034-isrg-pr110-authority-ratification.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0034`).

**No other file is touched.** No ISRG YAML/Markdown, no `intelligence/freshness_registry.yaml`, no
`operations/WORKSTREAMS.yaml`, no `CLAUDE.md`, no `targets.yaml`/`holdings.yaml`, no production code,
and no test file is created, modified, or authorized to be created by this filing — those belong
exclusively to the later, separate synchronization unit authorized in §8.

### 14. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own eligible independent review anchored to
its exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review
per `OPS-0009` §6, and receive a separately retained `Principal acceptance:` statement meeting every
requirement of §7 — identifying this decision's exact accepted head SHA — before it may be marked
ready or merged. **Nothing in §§1-12 becomes effective until this governance PR merges to `main`.**
This decision does not mark itself, or authorize marking itself, ready for merge, and does not begin
the later synchronization unit authorized in §8 — that unit's own PR is not opened by this filing.

## Rationale

**Why ratification, not silent inference or retroactive rewriting.** ISRG's Stage B refresh is real,
merged, and — per the retained independent review — substantively sound content. Leaving its
authority gap indefinitely unresolved would mean the record's lifecycle status rests permanently on a
disclosed-but-unaddressed defect; silently treating the gap as closed because the content is good
would exactly repeat the failure mode `PI-0016` §1 and `OPS-0004`'s Finding FA-1 both already guard
against — content quality substituting for missing authority. A narrow, explicit, present-day
ratification is the smallest instrument that actually closes the gap without either of those errors:
it does not rewrite history (§4), and it does not treat soundness as a substitute for authorization
(§3).

**Why content-quality and authority are treated as strictly separate questions.** The retained PR
#193 review itself draws this line explicitly: "Content quality does not cure this." This decision's
own structure preserves that separation — §2 and §3 are independent findings, and §6 tells a future
reviewer of this decision not to re-litigate content quality, which is already independently settled
evidence, and to instead verify the ratification's own scope and boundaries.

**Why the synchronization unit is deferred, not bundled here.** Following `OPS-0009`'s Lane
discipline (Lane G for this governance-authorization filing; Lane M for the later factual
synchronization), and the same sequencing this repository has used throughout WS-0005 (`OPS-0010`
itself authorized its own later implementation unit rather than performing the synchronization in
the same filing), the registry and register updates in §8 depend on facts this decision does not
itself determine (the later unit's own review/acceptance/merge/post-merge-verification outcome) —
making them here would risk the correction preceding, rather than following, the synchronization it
is meant to record.

**Why this remains `Proposed`, not `Accepted`, at filing.** Consistent with every other WS-0005
governance filing in this repository's history (`PI-0023` through `PI-0033`, `OPS-0007` through
`OPS-0010`), this decision is opened as a draft PR requiring its own independent review and separately
retained principal acceptance before merge — it does not, and cannot, mark itself ready.

## Alternatives Considered

- **Leave the ISRG authority gap disclosed but unresolved indefinitely.** Rejected — both retained
  sources (the PR #193 audit and its independent review) explicitly flag this as requiring "a
  separate, future, explicit governance decision"; deferring further with no resolution in sight
  would leave WS-0005's sole remaining held-back record permanently stuck.
- **Treat the retained PR #193 content-quality finding as sufficient, on its own, to promote ISRG to
  PROVISIONAL.** Rejected — explicitly contrary to the retained review's own conclusion ("content
  quality does not cure this") and to `PI-0016`'s standing requirement that authorization be its own
  durable, repository-filed record, not inferred from unrelated evidence.
- **Rewrite PR #110's history, or `intelligence/freshness_registry.yaml`'s `company_record_authority`
  field, to retroactively claim `PI-0009` (or some other existing decision) already covered the
  refresh.** Rejected — `PI-0009` governs Stage A (original creation) only, and no other existing
  decision names ISRG's Stage B refresh; fabricating that citation would misstate history exactly the
  way `OPS-0004`'s Finding FA-1 warns against.
- **Bundle the freshness-registry and `WORKSTREAMS.yaml` synchronization into this same filing.**
  Rejected per the principal's approved design and on the merits (see Rationale) — those updates
  depend on this decision's own later, separate acceptance and on the synchronization unit's own
  lifecycle outcome, not on anything this filing itself determines.
- **Perform a fresh, independent content re-review of ISRG as part of this filing, rather than relying
  on the retained PR #193 review.** Rejected — the retained review already independently assessed
  ISRG's current content and found no BLOCKER or MATERIAL defect; re-litigating settled content
  evidence inside an authority-focused decision would blur this filing's own narrow scope and invites
  exactly the kind of scope creep `OPS-0009` §2's mandatory/removable-control distinction exists to
  prevent.
- **Grant this ratification prospective effect for any future ISRG refresh, not just the PR #110
  refresh already merged.** Rejected — that would convert a narrow, one-time remedy into a standing
  license, contrary to the principal's approved design and to §4's explicit statement that this is
  "not a general license for unauthorized research or later ratification."

## Consequences

**Authorized, effective on this decision's own merge:** a one-time, explicit, present-day
retrospective ratification of the ISRG PR #110 refresh (§4), supplying `PI-0016`-standard
authorization for that already-merged action going forward; and authorization of exactly one later,
separate, bounded synchronization unit (§8) to update ISRG's `company_record_authority` in
`intelligence/freshness_registry.yaml` and its lifecycle entry in `operations/WORKSTREAMS.yaml`,
gated on its own full independent-review/acceptance/merge/post-merge-verification lifecycle.

**Unchanged by this decision:** `intelligence/companies/ISRG.yaml` and `ISRG.md` in full; ISRG's
conviction, portfolio role, tier, target, and weight; every other Company/Theme Intelligence record,
including all 27 confirmed-PROVISIONAL and all 17 eligible-pending records; `targets.yaml` and
`holdings.yaml`; `allocate.py` and `margin_state.py`; the 1.8x leverage cap and 30% buffer floor;
`PI-0009`, `PI-0016`, `OPS-0007`, `OPS-0008`, `OPS-0009`, and `OPS-0010`'s own substance, unedited;
`OPS-0006`'s Milestone 4-9 authorization boundary.

**No ISRG content edit, no freshness-registry edit, no `operations/WORKSTREAMS.yaml` edit, and no
Milestone 3 completion determination has been performed by this filing.** The later synchronization
unit authorized in §8 may begin only after this decision itself merges under the full review and
acceptance discipline in §6/§7/§14, and even a fully successful synchronization unit does not itself
complete Milestone 3 or authorize Milestone 4 — a separate, later, explicit completion determination
against `PI-0031` §K's seven criteria remains mandatory, exactly as §11 states.
