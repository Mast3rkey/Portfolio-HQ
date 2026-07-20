---
decision_id: AUTO-0001
date: 2026-07-19
status: Accepted
category: research_automation
related_decisions: [GOV-0001, PI-0011, PI-0014]
supporting_artifact: docs/FRESHNESS_PLANNER_V1_SPEC.md
---

## Context

`PI-0014` authorized one bounded, conversation-only, read-only evidence-gathering task
(INTC/SYK/DHR) but explicitly left open how such a task, or any future one like it, would
actually be triggered, executed unattended, and reported without a human at the keyboard.
A separate, multi-round design exercise built a secure unattended-execution architecture for
exactly that shape of task — three-job GitHub Actions privilege separation, artifact-verified
evidence transport, `--tools "Read"`-only Claude invocation, deterministic source
acquisition, permanent marker-based run-once locking — and progressively hardened it against
a long sequence of enforceability defects (a false claim that a working directory
constitutes filesystem isolation; an invalid `working-directory:` key on a `uses:` step; an
overclaimed absolute no-network guarantee; a temporal-qualification gap letting an
acquisition timestamp substitute for a source's actual official date; unbound source-to-
issuer provenance).

That hardened design, however, was originally architected around exactly one task ID, run
once, locked permanently. It could not answer Portfolio-HQ's actual standing need: Company
Intelligence records (`intelligence/companies/*.yaml`) accumulate real staleness over time
as new earnings, 10-Qs, 10-Ks, and material filings appear. `PI-0011` already detects one
kind of staleness deterministically — date-based overdue reviews, via `review.next_due`
compared against the current date, reported in `intelligence_report.py`'s generated
`staleness_report.md` — but nothing in the repository detects a *new source or filing
event* deterministically, and nothing re-triggers or executes a bounded review when one
appears. A further multi-round architecture review corrected this scope gap and
reconciled the result against `PI-0011` (Portfolio-HQ's existing staleness-reporting
authority over the `review.cadence_days` / `last_reviewed` / `next_due` / `log` fields) to
avoid creating a second, competing authority over the same dates.

## Decision

Authorizes a reusable **Research Freshness Framework**, specified in full in
`docs/FRESHNESS_PLANNER_V1_SPEC.md`, which this ADR incorporates by reference rather than
restating. Three layers: a deterministic monitor (no Claude invocation, no repository
writes), a bounded read-only refresh executor (Claude, `--tools "Read"` only, invoked only
when a governed trigger fires), and human-reviewed repository incorporation (the only layer
ever permitted to write a tracked file).

**Ownership, not duplication, of PI-0011's fields.** `review.cadence_days` /
`last_reviewed` / `next_due` / `log` remain owned exclusively by the Company Intelligence
specification and each human-approved company record. `PI-0011` remains the reporting
consumer of those fields and the source of the framework's strict overdue rule,
`review.next_due < as_of_date` (not "reached or passed" — a `next_due` equal to `as_of_date`
is not yet overdue). This framework is a second consumer of the same fields, never a second
owner.

**What this framework newly owns:** static enrollment (`intelligence/freshness_registry.yaml`);
an incorporated-evidence checkpoint, structured as ordered, profile-specific channels with
an explicit `pending`/`verified` lifecycle (`intelligence/freshness_checkpoints.yaml`);
two closed, structurally distinct operational issue types (a durable per-ticker
monitor-status issue, and a freshness-episode issue) with a fail-closed machine-state
block; deterministic trigger fingerprints, including cadence-overdue fingerprints in
addition to filing-derived ones; immutable, per-fingerprint-and-assignment-ordinal
task-instance identity; and a per-authorization, individually reviewed replacement
mechanism governing any re-assignment of a previously attempted fingerprint.
Complete field-level, transition-level, and validator-level detail is in the specification's
§2–§18, not restated here.

**Initial eligible roster — exactly seven tickers, each already carrying its own separately
governed Company Intelligence record**, verified directly against
`intelligence/companies/*.{yaml,md}` provenance lines at drafting time: COST (`PI-0003`),
XOM (`PI-0005`), NVDA (`PI-0007`), GEV (`PI-0007`), ISRG (`PI-0009`), TMO (`PI-0009`), TSM
(`PI-0012`). Every row in this filing's `intelligence/freshness_registry.yaml` starts
`monitoring_enabled: false`; every row in `intelligence/freshness_checkpoints.yaml` starts
`checkpoint_status: pending` with an empty channel set — no baseline filing value is
asserted, inferred, or guessed by this filing. A ticker moves to active monitoring only via
its own later, separately reviewed bootstrap PR (specification §4).

**`PI-0014` (INTC, SYK, DHR) is the framework's intended first Path-B pilot — identified,
not itself executed, by this decision.** `PI-0014`, as accepted, authorizes exactly one
bounded, conversation-based, read-only evidence-gathering exercise; its own findings-
lifecycle clause states that findings remain conversational, that the authorization
"produces no committed research artifact and changes zero repository files," and that any
future reliance on those findings requires a separate, later decision to independently
re-verify and summarize them. This decision identifies `PI-0014` as the framework's Path-B
template case — it does **not** itself convert `PI-0014`'s findings into GitHub issue
output, does **not** itself grant `PI-0014` unattended execution, and does **not** itself
supply `PI-0014` a runtime prompt, a runtime schema, a schedule, or an activation. Persistent
issue output, unattended execution, runtime prompts/schemas, scheduling, and activation for
`PI-0014` (or any future Path-B task) each require their own later, explicit implementation
or activation authorization — none of that is granted by this ADR. `PI-0014` remains
`Accepted` and wholly unchanged by this decision; its findings remain conversational exactly
as already recorded.

**No allocator, portfolio, or ranking authority anywhere in this framework**: no conviction,
`portfolio_role_ref`, theme membership, tier, target, weight, cluster, margin, trade, or
allocation fact is read, written, computed, or implied by any layer. `targets.yaml`,
`holdings.yaml`, `allocate.py`, and `margin_state.py` are untouched by this decision and by
everything it authorizes.

**Filing scope, precisely:** this decision authorizes the governance record and the
specification it points to, plus the two seed data files described above, all in a state
where every ticker is disabled and every checkpoint is pending. It does **not** authorize a
GitHub Actions workflow, executable monitor or executor code, a live adapter endpoint,
an action commit pin, a reusable Path-A prompt/schema file, a PI-0014 runtime prompt/schema
file, or an empty `intelligence/freshness_replacements/` directory (git does not track empty
directories; the first genuinely reviewed authorization creates it when needed). Those
belong to a later, separate implementation PR, itself subject to its own review before
merge, per specification §21. **Acceptance of this decision authorizes only the governance
record and the two seed data files described above — it does not itself constitute
authorization to implement, schedule, or activate anything.**

## Rationale

Single-owner discipline, generalized rather than reinvented: this framework applies the same
principle `GOV-0001` already established for the repository's documentation layers (each
concept gets exactly one authoritative home) to a new operational domain — freshness
monitoring reads and reconciles with `PI-0011`'s existing fields instead of standing up a
competing copy, which is exactly the drift risk `GOV-0001`'s own Context section identified
and moved to prevent. Company Intelligence records are human-authored and human-approved
(`PI-0003`/`PI-0005`/`PI-0007`/`PI-0009`/`PI-0012` each required explicit human sign-off);
a framework that lets any layer other than a human silently advance what counts as the
accepted, incorporated evidence behind one would quietly undo that authorship. Separating
deterministic detection (layer A), bounded read-only research (layer B), and accepted,
human-reviewed incorporation (layer C) keeps that authorship intact — the framework's only
repository-write surface is, and stays, a human, matching this repository's standing
manual-execution doctrine (`constitution/INVESTMENT_CONSTITUTION.md` §2) applied to research
automation rather than trading automation. The core problem this framework solves —
evidence silently going stale with nothing to flag it — is itself the rationale; the
mechanism is the fix, not a separate empirical claim borrowed from an unrelated domain.
Fixing the roster to exactly the seven tickers that already independently cleared their own
Company Intelligence authorization avoids smuggling new company-selection authority into an
infrastructure decision — enrollment adds monitoring to an already-approved record, it does
not create one.

The framework's mechanical complexity (per-fingerprint dispositions, assignment ordinals,
per-authorization replacement files, ordered checkpoint channels, a fail-closed machine-state
block) is the direct, traceable product of a multi-round adversarial correction process,
each round closing a specific, real enforceability or ownership gap rather than adding
unmotivated ceremony: separating Claude's provisional task disposition from authoritative
episode fingerprint state exists because a model's self-report was found capable of
implicitly retiring evidence it merely claimed to cover; per-fingerprint assignment ordinals
exist because a single per-instance generation number cannot represent a mixed snapshot's
differing attempt histories; the checkpoint's ordered-channel model exists because a single
flat "latest filing" field could not represent a domestic issuer's four independently-paced
filing types, let alone a foreign private issuer's different official form set; and the
durable monitor-status issue exists because an episode's closure and a ticker's displayed
freshness must never be allowed to silently depend on each other.

## Alternatives Considered

- **Extend the Company Intelligence `review:` schema itself with an
  `incorporated_evidence` sub-block**, rather than a separate AUTO-0001-owned checkpoint
  file. Rejected: that schema is frozen under Portfolio Intelligence's own governance
  (the same class of freeze `PI-0004` required its own decision to touch, for conviction
  vocabulary alone); AUTO-0001 has no standing to amend it as a side effect of its own
  filing, and doing so would require a second, separate Portfolio-Intelligence-side decision
  as a filing prerequisite, defeating the point of a self-contained framework decision.
- **A single global `replacement_authorizations.yaml` ledger** rather than one file per
  authorization. Rejected: a monolithic file accumulates every ticker's history in one place,
  inviting merge conflicts and burying each authorization's diff inside unrelated ones — the
  per-authorization file model keeps each reviewed change self-contained, consistent with
  this framework's existing one-thing-per-artifact pattern (one episode per issue, one
  checkpoint row per ticker).
- **A global AUTO-0001 grace interval escalating `review_due` to a `stale` status.**
  Rejected: an unmotivated numeric ceiling with no independent doctrine argument behind it
  is exactly the kind of unjustified parameter this repository's governance culture pushes
  back on (contrast the leverage cap and buffer floor, both independently argued). `stale`
  is dropped from V1; `review_due` persists, however long, until a human acts.
  A genuine SLA/escalation need, if it arises, is its own future, separately-argued decision.
- **Auto-seeding all seven initial checkpoints from each company's existing `sources:`
  list**, treating it as sufficient baseline evidence. Rejected on direct inspection: at
  least one existing record (`COST.yaml`) stores filing identifiers as free-form prose
  inside `sources[].note` strings, not as a structured, unambiguous field — exactly the kind
  of inference this framework's own rule (specification §4) prohibits as a checkpoint basis.
  Every initial row instead starts `pending`, resolved per-company in its own later,
  separately reviewed bootstrap PR.
- **Enrolling the entire `targets.yaml` universe, or prioritizing enrollment/triggers by
  tier, target weight, or holding size.** Rejected: enrollment scope and trigger urgency
  read only the enrollment registry and checkpoint file, never allocator-side facts — reading
  tier/weight/holding size into monitoring priority would be exactly the kind of
  allocator-authority creep this decision explicitly forecloses.
- **Filing a narrower, PI-0014-only automation decision first, generalizing later.**
  Rejected: building a job architecture, artifact-transport contract, and permission model
  specifically shaped around one hardcoded task ID, then immediately needing to generalize
  all of it, duplicates review effort and risks drift between the two decisions — the exact
  failure mode this repository's Decisions Log repeatedly guards against ("state it, apply
  it, don't relitigate"). Nothing about the reusable framework is less bounded than a
  pilot-only version — the fixed Path-A template (specification §16) is a strictly *tighter*
  constraint than a freely-authored one-off prompt.
- **Describing `PI-0014` as already issue-output-capable or already unattended-executable**,
  since the earlier unattended-execution architecture work assumed that shape. Rejected on
  direct re-check of `PI-0014`'s own accepted text: its findings-lifecycle clause commits
  only to conversational findings and zero repository artifacts. Overstating `PI-0014`'s
  current scope would misrepresent an already-accepted decision inside a new one — this ADR
  identifies `PI-0014` as the intended Path-B template only, leaving its actual execution
  model exactly as accepted until a future, separate implementation/activation decision.

## Consequences

Filing this decision creates two new tracked data files, `intelligence/freshness_registry.yaml`
and `intelligence/freshness_checkpoints.yaml`, both fully populated for all seven tickers but
inert — every row disabled, every checkpoint pending, no monitoring, no issue creation, no
Claude invocation occurs as a result of this filing alone. `governance/decisions.yaml` gains
one new row for this entry; `CLAUDE.md`'s Decisions Log gains one short pointer entry, per
`GOV-0001`'s established convention. No `intelligence/companies/*.yaml` file, `targets.yaml`,
`holdings.yaml`, `allocate.py`, `margin_state.py`, or any allocator-visible state is created
or modified by this decision. No GitHub Actions workflow, executable code, live adapter
endpoint, action pin, or runtime prompt/schema file exists as a result of this filing —
those remain deferred to a future, separately reviewed implementation PR (specification
§21), which does not inherit approval from this decision alone. `PI-0014` remains `Accepted`
and unchanged; its findings-lifecycle clause is unaffected; it does not begin executing
unattended, does not begin producing issue output, and does not become eligible for either
as a result of this decision — those each require their own future, explicit implementation
or activation authorization.
