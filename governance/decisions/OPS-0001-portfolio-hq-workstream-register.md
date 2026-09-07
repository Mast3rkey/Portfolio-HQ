---
decision_id: OPS-0001
date: 2026-07-24
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, MARGIN-0005]
supporting_artifact: operations/WORKSTREAMS.yaml
---

## Context

Portfolio-HQ is worked from multiple sessions and interfaces — Claude Code sessions, ChatGPT
conversations, branches, PRs, and now a multi-gate research program (MARGIN-0005) spanning
several PRs across a single day (#137–#140). No file currently preserves active priorities,
planning intent, dependencies, blockers, verified milestones, and exact next actions across that
span in one place: `CLAUDE.md` is the operational-synthesis/current-parameter/workflow record,
`governance/decisions/` records individual accepted decisions, and `decision_log.yaml` is the
historical margin/Intelligence ledger — none of these is a coordination register, and none is
supposed to become one. Without a dedicated register, a new session has to reconstruct "what's in
flight, what's next, what's blocked" by re-reading PR history and prior decisions from scratch
every time, which is exactly the kind of unreliable ad hoc reconstruction `CLAUDE.md`'s own git-sync
discipline exists to avoid for portfolio state. This decision establishes that register, narrowly,
under a principal authorization that explicitly bounds it to registering coordination — not
originating any new authority.

## Decision

Establishes `operations/WORKSTREAMS.yaml` as the canonical, repository-native Portfolio-HQ
workstream register — a coordination artifact, not an authority source. It preserves active
priorities, planning intent, dependencies, blockers, verified milestones, and exact next actions
across sessions, branches, PRs, and research programs. It coordinates work; it does not originate
investment policy, governance authority, research authority, approval, or implementation
authority, and it cannot override the Constitution, an accepted governance decision, a frozen
protocol, `targets.yaml`, `holdings.yaml`, production code or tests, or live GitHub state. Live
repository and GitHub facts always supersede a stale register field — the register is checked
against live state, never substituted for it.

**Schema** (`id`, `title`, `objective`, `governing_authority`, `status`, `priority`,
`dependencies`, `authorized_scope`, `prohibited_scope`, `milestones`, `evidence_refs`,
`next_action`, `completion_criteria`, `blocker`, `active_branch`, `active_pr`,
`last_verified_main_sha`, `last_verified_date`, `authorized_by`, `supersedes`, `superseded_by`) is
deliberately minimal — no `owner_session` field, since a workstream is not owned by whichever
session last touched it, and no field the schema doesn't need.

**No duplicate dashboard.** V1 ships no generated Markdown summary, no GitHub Issue mirror, and no
validator or CI addition. Owning evidence stays in its owning files (a PR, a report, a protocol)
and is referenced from `evidence_refs`, never copied into the register.

**Status vocabulary:** `proposed`, `recommended`, `authorized`, `in_progress`, `review`, `merged`,
`validated`, `effective`, `complete`, `cancelled`, `superseded`. An AI session may never
self-authorize a workstream to `authorized` status — that transition requires durable accepted
governance authority (a decision under `governance/decisions/`) or an explicit principal
authorization recorded in the entry. Factual Git/GitHub transitions (a PR merged, a branch
deleted) must still be independently verified against live state before the register is updated to
reflect them. A `complete` or `superseded` record is not silently rewritten — correct it the same
way `governance/decisions/README.md` already requires for decision files: a dated note, or a new
entry that supersedes it explicitly.

**Priority rule:** at most one workstream may carry `priority: primary` at any time.

**Active GitHub fields:** `active_branch` and `active_pr` hold only currently-live work — a branch
or PR that still exists and is unmerged. A merged historical PR belongs under `milestones` or
`evidence_refs`, never in these two fields. Both are `null` whenever no corresponding live branch
or PR exists.

**Session workflow addition (`CLAUDE.md`):** a substantial session reads
`operations/WORKSTREAMS.yaml` after its normal repository preflight — never in place of it. The
register is updated only on a meaningful status, milestone, blocker, authority, or next-action
change; routine read-only checks and ordinary questions do not require an update.

**Initial planning authority (recording only):** this decision authorizes *recording*, not
*implementing*, three durable planning intents: the unified Portfolio-HQ core architecture and
optimization audit (WS-0002); the deferred daily allocation-check user experience (WS-0003); and a
separate future guardrail-calibration research question (WS-0004). None of the three is scoped,
designed, or authorized to execute by this filing — each requires its own future, separate
authorization before any work begins.

**Populated now — four workstreams**, detailed in `operations/WORKSTREAMS.yaml`:

- **WS-0001** — MARGIN-0005 margin/target research program. `in_progress`, `priority: primary`.
  G0–G2B are merged (PRs #137, #138, #139, #140); the charter's own S2 ceiling permits at most one
  further implementation PR. The register does not authorize or begin that PR — it records that a
  read-only scope determination is the next action, and states the pre-S3 R2 integration
  constraint PR #140's independent review surfaced (a documented pre-S3 integration item, not a
  production defect, and not established as a current G2 blocker).
- **WS-0002** — Unified Portfolio-HQ core architecture and optimization audit. `recommended`,
  `priority: secondary`, `authorized_scope: none`. Durable planning intent only.
- **WS-0003** — Daily allocation-check user experience. `proposed`, `priority: secondary`,
  depends on WS-0002, `authorized_scope: none`.
- **WS-0004** — Guardrail-calibration research (1.8x cap / 30% buffer floor). `proposed`,
  `priority: secondary`, `authorized_scope: none`, contingent on WS-0001 reaching a governed
  stopping point and a separate future research charter being accepted.

**Scope exclusions:** no portfolio, margin, allocation, Intelligence, research-result, target,
holding, trading, or order behavior changes anywhere in this filing.

## Rationale

The register generalizes a pattern this repository already relies on elsewhere — `CLAUDE.md`'s
Decisions Log as a durable index, `governance/decisions/` as an append-only ADR record,
`intelligence/`'s filesystem-as-index doctrine (frozen by PI-0001, reaffirmed for Theme
Intelligence by PI-0006) — to a fourth, narrower concern: cross-session operational coordination,
which none of the existing layers is designed to hold. Keeping it strictly coordination-only,
non-authoritative, and free of a generated dashboard follows the same proportionality reasoning
GOV-0001 already applied to the documentation architecture as a whole: a solo operator's tool
does not need committee-meeting ceremony, and a second rendering of the same facts (a Markdown
summary, a GitHub Issue mirror) is exactly the kind of duplicated source of truth this repository's
governance layer exists to prevent, not create. The no-self-authorization and
verify-before-transition rules mirror Constitution §6 ("verify before acting on external review")
and this repository's repeated finding that claims from outside a live session with real file
access must be checked, not trusted.

## Alternatives Considered

- **A generated Markdown dashboard alongside the YAML.** Rejected for v1 — a second rendering of
  the same facts drifts from the source exactly the way `governance/README.md` already declined a
  parallel `intelligence/index.yaml` for the same reason (rejected on all seven of PI-0001's
  evaluation criteria). Nothing prevents a future decision from adding one if a real
  discoverability gap is demonstrated.
- **A GitHub Issue per workstream.** Rejected — it would create a second, unsynchronized home for
  the same status fields, and this repository has no existing GitHub Issue workflow to fold it
  into.
- **A validator or CI gate enforcing the schema in v1.** Rejected — no drift has yet been
  observed to justify tooling; the same evidence-before-tooling standard `governance/README.md`
  already applies to `targets.yaml` commit-message discipline applies here.
- **An `owner_session` field.** Rejected — a workstream is not owned by whichever session last
  touched it, and the field would immediately go stale across the session boundaries this
  register exists to survive.
- **Letting the register assert `authorized` status on its own read of a governance decision.**
  Rejected — even a durable accepted decision should be cited, not silently inferred, and a
  factual Git/GitHub transition must still be independently re-verified at the time the register
  is updated, since live state is authoritative over any cached field including this one.
- **Immediately scoping and starting WS-0002/WS-0003/WS-0004.** Rejected — explicitly out of
  scope for this filing; the principal's authorization permits recording these three intents, not
  implementing any of them.

## Consequences

Going forward: `operations/WORKSTREAMS.yaml` becomes the place a new session checks, after normal
repository preflight, for what's in flight, what's next, and what's blocked — verified against
live repository and GitHub state before being acted on, never in place of that verification. It is
updated only on a meaningful change, not on every read-only check. Explicitly unchanged: no
portfolio, margin, allocation, Intelligence, research-result, target, holding, trading, or order
behavior; no research file, pinned protocol hash, or trial ledger; no existing accepted governance
decision, the Constitution, or any frozen doctrine; `targets.yaml` and `holdings.yaml` remain
untouched and fully authoritative. This filing opens a draft pull request only — it does not
authorize merging, and does not itself make the register or the `CLAUDE.md` workflow addition
effective until that PR is reviewed and merged.
