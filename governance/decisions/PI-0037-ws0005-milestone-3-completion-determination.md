---
decision_id: PI-0037
date: 2026-08-03
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, OPS-0010, PI-0031, PI-0032, PI-0033, PI-0034, PI-0035, PI-0036]
supporting_artifact: null
---

## Context

### Authority for this unit

The human repository principal authorized one bounded Lane G (`OPS-0009` §1) unit solely to
determine, on live repository and GitHub evidence, whether WS-0005 Milestone 3 satisfies the
seven-criterion completion standard `PI-0031` §K defined and `PI-0035` §C narrowly restated. This
is a completion-**determination** — it performs no new research, edits no Company Intelligence
record, reopens no gate, names no new research batch, and does not begin Milestone 4 regardless of
its own verdict.

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. **Authenticated GitHub identity**
  confirmed `Mast3rkey` (`gh auth status` / `gh api user`).
- **`origin` fetched and pruned.** `git fetch --all --prune` returned no new refs beyond what this
  session's clone already held. `git rev-parse origin/main` returned
  `926d7a4fdb740e9efc066f1563e2f45397024357`, matching this unit's expected starting SHA exactly,
  and matching this clone's local `main` (`git status` — clean, up to date).
- **PR #234 confirmed merged and closed** (`OPS-0015`, "personal-first unified-app roadmap"),
  `mergedAt: 2026-08-03T20:27:43Z`, merge commit `926d7a4fdb740e9efc066f1563e2f45397024357` —
  identical to `origin/main`'s tip, confirming no commit exists past this filing's own base. Its
  post-merge CI check (`test`) independently re-queried: `completed` / `success` at that exact SHA.
- **Zero open pull requests** confirmed via the GitHub API. Eighty-plus stale remote branches exist
  (prior sessions' abandoned or superseded work); none is a currently open PR and none overlaps this
  unit's own file scope (`governance/decisions.yaml`, `governance/decisions/PI-0037-*.md`,
  `operations/WORKSTREAMS.yaml`'s WS-0005 entry, `CLAUDE.md`) — independently confirmed by targeted
  `git log <branch> --oneline` spot checks against the branches whose names suggested overlap
  (`claude/ws-0005-m3-batch-8-to4tz7`, `claude/ws0005-post-pr232-factual-sync`,
  `claude/ws0005-register-verdict-correction-mqru0i`, `claude/pi-roster-reconciliation-xng8v6`) —
  none is an open PR; none mutates a file this unit touches.
- **Branch name confirmed unused**: `claude/ws0005-m3-completion-determination` does not appear in
  `git branch -r`.
- **`governance/decisions/` and `governance/decisions.yaml` reconciled**: 63 files (excluding
  `README.md`) = 63 indexed entries, no orphans. Highest filed `PI-####` is `PI-0036`.
  **`PI-0037` independently confirmed the next unused identifier**, checked live against both the
  directory and the index — not assumed from this filing's own suggested numbering.
- **Governing decisions read in full this session, not relied on from memory or summary**:
  `OPS-0001`, `OPS-0006`, `OPS-0007`, `OPS-0008`, `OPS-0009`, `PI-0031` (in full, including §K),
  `PI-0033`, `PI-0035` (in full), `PI-0036`, `PI-0034`, `CLAUDE.md`'s complete Decisions Log, and the
  retained audit artifacts `governance/audits/WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_20260729.md`
  and `governance/audits/WS0005_M3_SIX_RECORD_FRESH_RETROSPECTIVE_REVIEW_RETENTION_20260729.md`.
- **`operations/WORKSTREAMS.yaml` read in full** (5,933 lines; WS-0005's own entry, lines 495-3667).
  WS-0005 confirmed the sole `priority: primary` workstream; `status: in_progress` at this filing's
  own starting point.
- **Live validators and full suite independently re-run this session**, against the exact base SHA
  above, before any edit:
  - `intelligence_validator.validate_directory('intelligence/companies')` — **47/47 valid**.
  - `intelligence_validator.validate_themes_directory('intelligence/themes')` — **2/2 valid**.
  - `freshness_validator.py` — **OK**.
  - `python3 -m pytest -q` — **2441 passed, 0 failed** (124.5s).
  - `portfolio_hq.dashboard.decisions.build_catalog('.')` — **63 decisions, `issues == ()`**.
  - Exactly one `priority: primary` workstream (`WS-0005`) — confirmed by direct YAML parse.
  - `git diff --check` — clean. Working tree clean throughout.
- **Canonical governed roster independently re-derived from live `targets.yaml`**: exactly **27**
  `destination:` rows with `asset_class: equity`. **`caps.clusters`** independently re-parsed:
  `semis` (ASML, TSM, NVDA, AVGO, KLAC, 25.0%), `power_infra` (ETN, GEV, PWR, 20.0%), `oil`
  (`tickers: []`, 20.0%, no current members).
- **`gates.yaml` independently re-parsed**: exactly 6 gated tickers (SNPS, ICE, SPGI, WM, RKLB,
  TSLA), each `status: cash_pending_clearance`, `authority: PHQ-2026-01`, `allow_add: false`, each
  carrying its own `next_gate` free-text condition. **No gate's `next_gate` text is marked satisfied
  anywhere in this repository** — every one names a future evidentiary event (an investor day, a
  quarterly filing, a technical milestone) with no repository-recorded confirmation that the event
  has occurred. This audit does not attempt to determine, from outside evidence, whether any such
  event has occurred in the real world — per this unit's own bounding, that question is out of
  scope and any such trigger, if it has occurred, is separately discovered work (§ "Discovered
  work" below), not evaluated here.
- **`intelligence/companies/` independently confirmed to hold 47 `.yaml`/`.md` pairs**, all 47
  independently confirmed schema-valid this session (above). **`intelligence/freshness_registry.yaml`
  and `intelligence/freshness_checkpoints.yaml` independently confirmed to carry one row each for
  GNRC and RTX** (`company_record_authority: PI-0036`, `enrollment_authority: PI-0036`,
  `enrolled_at: "2026-08-03"`, `checkpoint_status: pending`, `monitoring_enabled: false`),
  identically shaped to every other batch's rows.
- **No repository truth conflicts with the prior read-only audits this unit relies on** (the two
  retained `governance/audits/` artifacts above): every fact this unit independently re-derived —
  the 47-record count, the 27-name canonical roster, the 6-gate list, the freshness rows, the
  validator/test results — matches what those artifacts, and the `operations/WORKSTREAMS.yaml`
  entries synchronizing them, already state. The one respect in which live state has *moved past*
  those two 2026-07-29 artifacts — GNRC and RTX's addition to both the canonical roster and Company
  Intelligence coverage via `PI-0036` (2026-08-03) — is accounted for directly in this filing (§
  "Updated roster accounting" below), not treated as a conflict.
- **Isolated worktree confirmed clean** before this unit's own first edit.

No condition in this unit's own stop list was triggered: `main` had not advanced past the expected
base in a scope-changing way (it matched exactly); no overlapping mutation lane exists; the next PI
identifier (`PI-0037`) matched expectation; no gate has actually reopened; the canonical roster
count (27) matched expectation; live evidence did not contradict the prior read-only audits; a clean
isolated workspace was established without incident.

## Decision

**PI-0037 determines, on live repository and GitHub evidence independently re-verified this
session, that WS-0005 Milestone 3 satisfies all seven of `PI-0031` §K's completion criteria as
narrowly restated by `PI-0035` §C, and accordingly sets Milestone 3's `status` to `complete` in
`operations/WORKSTREAMS.yaml`.** This decision authorizes no research, no Company Intelligence
edit, no gate reopening, no tier/target/role/cluster/cap/holdings/margin/allocator change, and — in
particular and repeatedly stated — **does not authorize, begin, schedule, or imply Milestone 4**
(portfolio relationship mapping) or any later WS-0005 milestone. It creates no investment,
allocation, or trading authority of any kind.

### A. Updated roster accounting (post-`PI-0036`)

`PI-0035` §B accounted for the 27-name canonical roster as 19 covered + 4 newly-gated-dispositioned
(SNPS, ICE, SPGI, WM) + 4 non-gated-already-`PI-0033`-dispositioned (GNRC, RTX, RKLB, TSLA).
`PI-0036` (2026-08-03, merged via PR #232, independently re-confirmed this session) subsequently
**narrowly superseded `PI-0033`'s disposition of GNRC and RTX specifically, for research-
authorization purposes only**, and its implementation completed full Company Intelligence coverage
for both. Live `targets.yaml`/`gates.yaml`/`intelligence/companies/` state, independently re-derived
this session, therefore now reads:

- **21 covered**: NVDA, TSM, ASML, AVGO, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG, TMO, V,
  COST, CEG, ETN, GEV, PWR, GNRC, RTX.
- **4 actionable-gated, disposed by `PI-0035` §D**: SNPS, ICE, SPGI, WM — each deferred to its own
  `gates.yaml` `next_gate` text, unedited, unsatisfied (per this filing's own live re-check above).
- **2 actionable-gated, disposed by `PI-0033` §A (reaffirmed, unedited, by `PI-0035` §E)**: RKLB,
  TSLA — same status.

**21 + 4 + 2 = 27.** This is a factual update to `PI-0035` §B's accounting, not a re-litigation of
it — `PI-0035`'s own text is not edited (per `governance/decisions/README.md`'s never-edit-after-
`Accepted` convention), and this section narrowly supersedes only its GNRC/RTX row-count, exactly to
the extent `PI-0036`'s own later, separately authorized coverage already made true.

### B. Criterion-by-criterion determination

**Criterion 1** (`PI-0031` §K.1, as restated by `PI-0035` §C.1 — merged with the retired
criterion 2): *Every canonical equity name that is not actionable-gated and not individually
deferred by accepted authority has a current Company Intelligence record.*
**SATISFIED.** 21 of 21 such names carry a current, schema-valid record (§A above; 47/47 valid,
independently re-run this session).

**Criterion 3** (`PI-0031` §K.3, as restated by `PI-0035` §C.3): *Every member of every active
correlated-cluster cap has a current Company Intelligence record.*
**SATISFIED.** `semis` (ASML, TSM, NVDA, AVGO, KLAC) — 5/5 covered. `power_infra` (ETN, GEV, PWR) —
3/3 covered. `oil` — `tickers: []`, no current members, no coverage question applies.

**Criterion 4**: *Every remaining uncovered canonical equity company is covered, explicitly
deferred by accepted authority with rationale, or assigned to an approved alternative research
architecture.*
**SATISFIED.** All 27 canonical names are accounted for (§A): 21 covered, 6 gated-and-deferred with
individually reasoned dispositions and named reopening triggers (`PI-0035` §D for SNPS/ICE/SPGI/WM;
`PI-0033` §A.11-12 for RKLB/TSLA, reaffirmed by `PI-0035` §E) — no residual uncovered, undispositioned
name exists.

**Criterion 5**: *No unresolved MATERIAL research-coverage finding remains.*
**SATISFIED.** The retained `WS0005_M3_CRITERION7_RETROSPECTIVE_LIFECYCLE_AUDIT_20260729.md` and
`WS0005_M3_SIX_RECORD_FRESH_RETROSPECTIVE_REVIEW_RETENTION_20260729.md` artifacts, together with the
`operations/WORKSTREAMS.yaml` entries recording PR #193/#194/#197's own completed lifecycles,
independently establish that every MATERIAL finding identified against any of the 45 pre-`PI-0036`
Company Intelligence records was a **review-provenance gap** (missing retained independent review),
not a content defect — and that every one of those gaps was closed by a fresh, eligible,
independently retained review before this filing's own preflight. `PI-0036`'s own PR #232 review
(`4846532441`, delta `4846664152`) found 0 BLOCKING / 0 MAJOR / 1 MINOR (a citation URL, resolved by
correction commit `d2b71ea`) against GNRC/RTX. CRM's and IBM's two residual findings remain recorded
as MINOR (not MATERIAL), and the universal 90-day freshness-cadence observation remains a NOTE (not
a finding of any severity) — both explicitly preserved as open and non-blocking per `PI-0031` §K.5's
own text, which does not require resolving either. **No MATERIAL finding is open against any
canonical-roster record as of this filing's own live re-verification.**

**Criterion 6**: *Coverage indexes, freshness records, and `operations/WORKSTREAMS.yaml` are
synchronized.*
**SATISFIED**, for the coverage-and-freshness content this criterion names. `intelligence/
freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` carry a correctly shaped row
for all 47 records including GNRC/RTX (independently re-confirmed this session). `operations/
WORKSTREAMS.yaml`'s WS-0005 entry carries an extensive, current, independently-verified-at-each-step
narrative recording every batch's authorization, implementation, review, correction, merge, and
post-merge verification through `PI-0036`/PR #233. **One narrow exception, disclosed, not
corrected, by this filing** (this unit's own authorization does not permit clearing it): WS-0005's
`active_branch`/`active_pr`/`last_verified_main_sha` self-reference fields are stale — they read
`claude/ws0005-post-pr232-factual-sync` / `233` / `36952f84...` (PR #232's merge commit), left behind
after PR #233 itself merged and after PR #234 (`OPS-0015`) subsequently advanced `main` further,
without an intervening WS-0005 self-reference update. `OPS-0015`'s own text already discloses this
exact category of staleness for WS-0007's and WS-0013's `active_pr` fields; WS-0005's own instance
was not separately disclosed there. This is an `OPS-0001` live-work self-reference hygiene item, not
a coverage-index or freshness-record synchronization gap — the actual coverage content these fields
sit alongside is current and independently re-verified accurate — and is recorded as discovered work
below, not corrected by this filing, per this unit's own explicit prohibition on clearing an
unrelated stale `active_branch`/`active_pr` field.

**Criterion 7**: *Every completed record has passed the required independent review, merge, and
post-merge verification lifecycle — per `OPS-0007` §3's PROVISIONAL definition, applied per record,
not merely per batch filing.*
**SATISFIED**, independently re-verified per record, not inferred from batch-level language. The two
retained retrospective audits (§ Preflight above) independently mapped all 45 pre-`PI-0036` records
against `OPS-0007` §3's five elements individually — 27 confirmed PROVISIONAL at original merge; 11
(ASML, AMAT, KLAC, LRCX, MU, SKHY, CEG, BRK.B, WMT, MLM, AAPL) reaching PROVISIONAL via PR #193's own
completed review/correction/acceptance/merge/post-merge-verification lifecycle; 6 (COST, XOM, NVDA,
GEV, TMO, TSM) reaching PROVISIONAL via PR #194's own completed lifecycle, including an independent
resolution of TSM's preserved verdict-label inconsistency; ISRG reaching PROVISIONAL via `PI-0034`'s
retrospective authority ratification plus PR #197's own completed lifecycle. **45 of 45 pre-`PI-0036`
records independently confirmed PROVISIONAL, 0 held back**, as of `operations/WORKSTREAMS.yaml`'s own
2026-08-01 entry — independently re-verified this session against current `intelligence/companies/`
state (no record removed or added between that entry and this filing except GNRC/RTX). **GNRC and
RTX independently confirmed PROVISIONAL this session** via direct GitHub API query of PR #232: review
`4846532441` (0 BLOCKING/0 MAJOR/1 MINOR) → correction `d2b71ea` → delta review `4846664152` (MINOR
resolved) → principal exact-head acceptance (`issuecomment-5169463732`, naming accepted head
`d2b71ea96dd414c57c22b3aed7f1b0b4a665e1fe`) → merge (`36952f84...`, confirmed direct-parent ancestry)
→ post-merge verification (PR #233, independently re-run `intelligence_validator.py` 47/47,
`freshness_validator.py` OK, focused dashboard tests 183/183, `decision_catalog.issues == ()`,
`git diff --check` clean, exact-head CI `30837021404` success). **All 47 currently-existing Company
Intelligence records — including all 21 covering a current, non-gated, non-deferred canonical
roster name — are confirmed PROVISIONAL under `OPS-0007` §3, independently re-verified this
session.**

### C. Verdict

**MILESTONE 3 COMPLETE.**

All seven of `PI-0031` §K's completion criteria, as narrowly restated by `PI-0035` §C and updated by
this filing's own independently re-verified roster accounting (§A), are satisfied as of this
filing's own live-state re-verification (`origin/main` at
`926d7a4fdb740e9efc066f1563e2f45397024357`). No criterion fails. No corrective unit is required to
reach this verdict.

## D. Discovered work (not performed by this filing)

1. **WS-0005's own `active_branch`/`active_pr`/`last_verified_main_sha` self-reference fields are
   stale** (§ Criterion 6 above) — a Lane M mechanical-synchronization item for a future, separately
   authorized unit; this filing does not clear it, per its own explicit authorization boundary.
2. **`PI-0035`'s own governance PR (#208) carries no GitHub-API-retrievable independent review or
   comment**, as `operations/WORKSTREAMS.yaml`'s own 2026-08-01 entry already discloses ("no
   independent-review or issue-comment record was found retained on PR #208 via the GitHub API").
   This is a review-**provenance** gap on a governance decision, not on a Company Intelligence
   record — `PI-0031` §K's criteria (and `OPS-0007` §3's PROVISIONAL definition, which this filing
   applies) are both scoped to Company Intelligence *records*, not to every governance decision's own
   review retention. `PI-0035`'s substantive content (the SNPS/ICE/SPGI/WM dispositions and the
   criteria restatement) was independently, mechanically re-verified against live `gates.yaml`/
   `targets.yaml` by this filing and found accurate. This filing does not resolve, and is not
   authorized to resolve, that governance-decision-level provenance gap — it is named here as
   separately discovered work for a future session's judgment, analogous to the fresh-review pattern
   `OPS-0010`/PR #193/#194/#197 already established for Company Intelligence records.
3. **Whether any of the six gated names' `next_gate` real-world trigger conditions (an investor day,
   a quarterly filing, a technical milestone) has since occurred** is explicitly out of this
   unit's scope (no external research is authorized) and is not evaluated here. If a future session
   determines, from repository-recorded evidence, that a trigger has occurred, that is itself
   separately discovered work requiring its own future, separately authorized unit — not addressed,
   resolved, or assumed by this filing.

None of the above blocks this filing's own verdict — each is disclosed, not corrected, exactly as
this unit's own authorization requires.

## E. What this decision does not do

- **Does not authorize, begin, schedule, or imply Milestone 4** (portfolio relationship mapping) or
  any later WS-0005 milestone (5-9). `OPS-0006` §5's own per-milestone authorization gate remains in
  force and unaddressed by this filing.
- **Does not perform, authorize, or imply any new company or theme research.**
- **Does not edit any Company Intelligence record's substance** — no `.yaml`/`.md` pair under
  `intelligence/companies/` or `intelligence/themes/` is touched by this filing.
- **Does not reopen any gate** — `gates.yaml`'s six entries, their `status`, `authority`,
  `allow_add`, and `next_gate` text are unchanged.
- **Does not perform relationship, dependency, overlap, or correlated-risk mapping of any kind.**
- **Does not change any tier, target, gate, cluster, cap, margin, holding, allocator, chart,
  brokerage, or order behavior.** `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`, and
  `margin_state.py` are untouched.
- **Does not run or log an allocation check.**
- **Does not mark this filing's own governance PR ready, request or begin independent review of it,
  post principal acceptance of it, or merge it** — this decision's own effectiveness is contingent on
  its own future, separate independent review and principal acceptance, per `OPS-0009` §1 Lane G's
  unreduced standard, exactly as every prior WS-0005 governance filing in this log has required of
  itself.
- **Creates no research, policy, allocation, or implementation authority of any kind beyond the
  single factual determination stated in §C.**

## Rationale

**Why a completion-determination decision is warranted now.** `PI-0035` §G stated explicitly that
"a future, separate completion-determination decision must evaluate all seven criteria together,
freshly verified against live state at that time, before Milestone 3 may be marked `complete`."
`PI-0036`'s subsequent completion of GNRC/RTX coverage closed the last remaining criterion-1 gap
among non-gated, non-deferred canonical names, and the two retained retrospective-lifecycle audits
already closed criterion 7's per-record verification for every other currently-covered record. No
governing decision has yet performed the "evaluate all seven together" act `PI-0035` §G reserved for
a future filing — this decision is that filing.

**Why this filing relies on, rather than re-performs, the two retained retrospective-lifecycle
audits.** `OPS-0009` §4's evidence-identity discipline permits reuse of an already-independently-
validated conclusion without repeating the underlying derivation, provided the conclusion's own
retained evidence is re-confirmed current — this filing independently re-confirmed, this session,
that every fact those two artifacts state (record counts, validator/test results, freshness rows,
decision-index counts) still holds against live `origin/main`, rather than accepting their
conclusions on trust.

**Why GNRC/RTX required independent, fresh verification rather than simple inclusion.** They post-
date both retrospective-lifecycle audits (2026-07-29) by five days — no existing retained artifact
had evaluated their lifecycle. This filing independently queried the GitHub API for PR #232's actual
review, correction, acceptance, merge, and post-merge-verification evidence rather than assuming
`PI-0036`'s own governance text (which pre-dates the implementation) was sufficient.

**Why discovered work is disclosed, not corrected.** This unit's own authorization is bounded to a
completion determination — it may not clear a stale `active_branch`/`active_pr` field, reopen a
gate, or resolve a governance decision's own review-provenance question. Disclosure without action
matches this repository's own established convention (`OPS-0004`'s Finding FA-1; `PI-0035`'s own
PR #208 disclosure) for exactly this situation.

## Alternatives Considered

- **Declare Milestone 3 complete based on `PI-0035`'s own 27-name accounting, without independently
  re-verifying GNRC/RTX's post-`PI-0036` lifecycle.** Rejected — `PI-0035` itself predates `PI-0036`
  and never addressed GNRC/RTX's coverage; skipping independent verification of the newest two
  records would be exactly the "assume batch-level language proves per-record lifecycle compliance"
  failure mode this unit's own authorization explicitly warns against.
- **Defer this determination further, pending resolution of the discovered-work items in §D.**
  Rejected — none of the three discovered-work items is a `PI-0031` §K criterion; each is either a
  mechanical hygiene field (§D.1), a governance-decision-level provenance question distinct from the
  Company-Intelligence-record-scoped criteria this filing evaluates (§D.2), or explicitly out of this
  unit's authorized scope (§D.3, real-world event verification). Deferring completion pending items
  the governing criteria do not themselves require would exceed, not honor, `PI-0031` §K's own text.
- **Re-run every prior batch's independent review from scratch instead of relying on retained
  evidence.** Rejected — `OPS-0009` §4 (evidence-identity, SHA-only reuse) and this repository's
  established practice both treat an already-independently-validated, unchanged conclusion as fully
  re-verified once its currency against live state is confirmed, not as requiring repetition.
- **Begin Milestone 4 in the same filing, since Milestone 3 is now determined complete.** Rejected —
  explicitly outside this unit's authorization; `OPS-0006` §5's separate-authorization gate for each
  milestone is unaffected by this filing under any circumstance.

## Consequences

**Authorized, effective on this decision's merge:** the factual determination that WS-0005
Milestone 3 satisfies all seven `PI-0031` §K completion criteria as of this filing's own live-state
verification, and the corresponding `status: complete` update to Milestone 3's gate in
`operations/WORKSTREAMS.yaml`.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, gate, and holding in
`targets.yaml`/`gates.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record, all 47
of them; `allocate.py`, `margin_state.py`, `intelligence_validator.py`, `freshness_validator.py`,
every freshness module, and every existing test; the 1.8x leverage cap and 30% buffer floor;
`PI-0031`'s, `PI-0033`'s, `PI-0034`'s, `PI-0035`'s, and `PI-0036`'s own accepted text and scope, in
full, unedited; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`.

**Explicitly not authorized by this decision, stated repeatedly for clarity:** Milestone 4 (portfolio
relationship mapping) or any later WS-0005 milestone; any research of any kind; any Company
Intelligence edit; any gate reopening; any tier/target/role/cluster/cap/holdings/margin/allocator/
order-behavior change; any allocation check; correction of the discovered-work items in §D. **This
decision creates no research, policy, allocation, or implementation authority beyond the single
factual determination in §C.**

### Required independent review, principal-acceptance gate, and stopping condition

- **This governance PR must remain in draft state** and must not be marked ready for review or
  merged by this session.
- **An eligible independent review is required**, anchored to this PR's exact final head, per
  `OPS-0007` §1's twelve-point capability-based standard — no self-review by the authoring session.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready, per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Explicit principal acceptance is required before merge**, at the exact head being merged.
- **This decision does not mark itself, or authorize marking itself, ready for merge.** It becomes
  effective — including the Milestone 3 `status: complete` transition — only on this governance PR's
  own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized
  scope ends at opening this draft PR (and one bounded follow-up commit setting WS-0005's `active_pr`
  self-reference to this PR's own number once it exists) and reporting its exact head. No independent
  review, no correction pass, no re-review, no merge, and no post-merge verification is performed by
  this session — each is a separate future step requiring a separate actor.

**No current portfolio policy or allocator behavior changes as a result of this decision, before or
after its merge.** `allocate.py`'s buy/trim/gap logic, every gate parameter, every cap, every target
weight, and every margin parameter remain exactly as `targets.yaml`/`gates.yaml`/`holdings.yaml`
currently state them, unaffected by this filing under any circumstance.
