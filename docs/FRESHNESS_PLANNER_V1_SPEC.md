# Freshness Planner V1 — Research Freshness Framework Specification

_Companion specification to `governance/decisions/AUTO-0001-freshness-planner-v1.md`. This
document defines the complete data model, vocabularies, and lifecycle contracts for the
Research Freshness Framework. It is a governance and design contract, not an
implementation — no GitHub Actions workflow, executable monitor/executor code, live
adapter endpoint, action commit pin, or runtime prompt/schema file is authorized by this
document. Those belong to a future, separately reviewed implementation PR, which must
conform to everything specified here._

## 0. Purpose

Portfolio-HQ's Company Intelligence records (`intelligence/companies/*.yaml`) must not
silently go stale relative to new earnings, filings, or material company developments.
`PI-0011` already detects one dimension of this deterministically — date-based overdue
reviews, from `review.next_due` compared against the current date, reported in
`intelligence_report.py`'s generated `staleness_report.md`. This framework adds the
dimension `PI-0011` does not cover — deterministic detection of a *new source or filing
event* — plus a bounded read-only research refresh, executed only when a governed trigger
fires, and a human decision on whether and how to incorporate the result — without ever
writing to the repository itself, and without ever exercising any allocator, tier, weight,
cluster, margin, conviction, role, theme, ranking, or trading authority.

## 1. Three-layer architecture

| Layer | What it is | Invokes Claude? | Writes repository files? |
|---|---|---|---|
| A. Deterministic monitor | Scheduled, cheap, mechanical. Reads enrollment + checkpoint state, compares against newly observable official filing/earnings metadata, computes derived freshness/monitor state, creates/updates operational issues. | No. | No. |
| B. Bounded refresh executor | Created only when a governed trigger fires. Runs Claude with `--tools "Read"` against a deterministically staged, digest-verified evidence bundle. Produces a structured result. | Yes. | No. |
| C. Human-reviewed incorporation | A human reads the refresh result and, if warranted, opens their own PR updating the Company Intelligence record, the checkpoint, and/or the enrollment registry. | No. | Yes — the only layer that ever does. |

## 2. Source-of-truth ownership

| Data | Owner | Written by |
|---|---|---|
| `review.cadence_days` / `last_reviewed` / `next_due` / `log` (in each `intelligence/companies/<TICKER>.yaml`) | Company Intelligence specification and the human-approved company record | Human-reviewed PR (existing mechanism, unchanged) |
| `intelligence/reports/staleness_report.md` | PI-0011 (`intelligence_report.py`) | Generated, read-only, unchanged |
| `intelligence/freshness_registry.yaml` | AUTO-0001 | Human-reviewed registry PR |
| `intelligence/freshness_checkpoints.yaml` | AUTO-0001 | Human-reviewed incorporation, bootstrap, or correction PR only |
| `intelligence/freshness_replacements/*.yaml` | AUTO-0001 | Human-reviewed authorization PR; workflow reads only, never writes |
| Freshness state (displayed value) | AUTO-0001, derived | Computed at read time from episode fingerprint state (§9) — never stored as a tracked-file field |
| Monitor state (latest recorded value) | AUTO-0001, durable | Stored in each ticker's durable monitor-status issue (§15.1), not a tracked file — updated by the monitor every run |
| Task disposition (`covered`/`unresolved`, per fingerprint, per task instance) | AUTO-0001, task-scoped | Claude's structured result — provisional evidence coverage only, never incorporation authority |
| Episode fingerprint state (`outstanding`/`assigned`/`awaiting_human_incorporation`/`incorporated`) | AUTO-0001, episode-scoped | Workflow drives every transition except the last; only a human incorporation PR sets `incorporated` |

AUTO-0001 never duplicates `review.last_reviewed`, `review.next_due`, or
`review.cadence_days`. PI-0011 remains the sole authority for the strict overdue rule:

```
overdue  ⇔  review.next_due < as_of_date
```

A `next_due` equal to `as_of_date` is **not** overdue. If `intelligence_report.py` exposes
this comparison as a reusable function, the monitor must call it directly. If it is not
practically factored out that way (to be confirmed at implementation time), the monitor's
own helper must be proven byte-for-byte identical against `intelligence_report.py`'s actual
behavior via a shared parametrized test fixture covering `next_due == as_of_date` and both
neighboring days — never left as "close enough."

## 3. Enrollment registry (`intelligence/freshness_registry.yaml`)

One row per enrolled ticker. Fields: `ticker`, `company_record_authority` (the decision
that authorized that ticker's Company Intelligence record to exist), `enrollment_authority`
(the decision that authorized *monitoring* for that ticker — `AUTO-0001` for this initial
batch), `enrolled_at`, `template_version`, `filing_trigger_profile`
(`domestic_issuer_v1` | `foreign_private_issuer_v1`), `refresh_policy` (a fixed version tag
naming the reusable Path-A task scope, §16), `monitoring_enabled` (bool).

**Enrollment authority rule:** a registry row for a ticker that already has an existing,
separately-governed Company Intelligence record is addable via an ordinary human-reviewed
registry PR under AUTO-0001's own authority — no new numbered decision is required, since
the record's right to exist was already separately governed and enrollment only adds
monitoring, not new analytical authority. Enrolling a ticker that does **not** yet have a
Company Intelligence record is a different act (creating analytical authority, not
monitoring it) and stays outside AUTO-0001 entirely — that path requires its own new
governance decision, the same bar every existing Company Intelligence record was held to.

**Initial roster, verified directly against `intelligence/companies/*.{yaml,md}` provenance
lines (not narrative-only) at drafting time:**

| Ticker | `company_record_authority` | `filing_trigger_profile` |
|---|---|---|
| COST | PI-0003 | domestic_issuer_v1 |
| XOM | PI-0005 | domestic_issuer_v1 |
| NVDA | PI-0007 | domestic_issuer_v1 |
| GEV | PI-0007 | domestic_issuer_v1 |
| ISRG | PI-0009 | domestic_issuer_v1 |
| TMO | PI-0009 | domestic_issuer_v1 |
| TSM | PI-0012 | foreign_private_issuer_v1 |

Every row starts `monitoring_enabled: false` (see §4 — gated on checkpoint verification).

## 4. Incorporated-evidence checkpoint (`intelligence/freshness_checkpoints.yaml`)

A separate, AUTO-0001-owned file — not a sub-block of the Company Intelligence `review:`
schema, which is owned and frozen by Portfolio Intelligence governance and not amendable by
AUTO-0001 as a side effect of this filing. One row per enrolled ticker: `ticker`,
`checkpoint_status` (`pending` | `verified`), `channels` (a mapping of named channels, §5),
`established_by` (the PR/issue reference that most recently set this row's channels).

**Checkpoint lifecycle:**
- A newly enrolled row starts `checkpoint_status: pending` with an empty `channels` map,
  unless the initial checkpoint is established in the same reviewed PR that adds the row.
- A `pending` ticker's derived freshness is always `unverified` (§9) — there is nothing yet
  to compare a new filing against, so `current` can never be asserted.
- `monitoring_enabled: true` is invalid while `checkpoint_status: pending` for that ticker —
  fail-closed, validator-enforced (§4.1).
- No channel value may ever be inferred from `review.last_reviewed`, free-form
  `sources[].note` prose, a repository file timestamp, or retrieval time. Establishment is
  an explicit, structured, human-attested act.
- **Bootstrap rollout (conservative):** all seven initial rows in this filing are
  `checkpoint_status: pending` with no channel values populated. A ticker moves to
  `verified`/`monitoring_enabled: true` only in a later reviewed PR that explicitly
  establishes its channels. Whether an individual company's baseline is transcription-only
  (the correct values are already legible somewhere in its existing `sources:` list, just
  not in structured form) or requires fresh baseline research is determined **per company,
  during that reviewed work** — not pre-judged by this filing. Per §9's fully fail-closed
  precedence rule, no company is classified `current` unless **all five** of
  `monitoring_enabled: true`, `checkpoint_status: verified`, a durable monitor-status
  record existing, that record's latest `monitor_state` being `healthy`, and no
  outstanding/assigned/awaiting fingerprint hold **simultaneously** — every one of the
  seven initial rows fails at least the first two of these from the moment this filing is
  accepted, so all seven display `unverified`, not `current`, until each is independently
  bootstrapped in its own later reviewed PR.

### 4.1 Checkpoint validator requirements

1. Exactly one checkpoint row per enrolled registry ticker (bijective; no orphan on either
   side once past bootstrap).
2. A checkpoint row's `ticker` matches its registry row's `ticker`.
3. `monitoring_enabled: true` with `checkpoint_status: pending` on the same ticker is a hard
   validation failure.
4. Every populated channel's `official_form_type` is valid for that ticker's
   `filing_trigger_profile` (a `domestic_issuer_v1` ticker never populates a
   `foreign_private_issuer_v1`-only channel, and vice versa).
5. No duplicate ticker rows; no single filing/source identifier claimed as the "latest
   incorporated" value under two different tickers' channels.
6. A `checkpoint_status: verified` row's populated channel set matches the minimum required
   set for its profile (§5).

## 5. Ordered checkpoint channels

Each channel: `channel_name`, `official_form_type`, `stable_source_id` (accession or
equivalent), `official_source_date`, `fiscal_period` (nullable where inapplicable),
`incorporation_reference` (the PR/issue that set it).

| Profile | Required channels (minimum) |
|---|---|
| `domestic_issuer_v1` | `annual_filing` (10-K) · `quarterly_filing` (10-Q) · `event_filing_watermark` (most recent 8-K reviewed-through date/accession — a watermark, not a single filing ID, since 8-Ks are numerous) · `earnings_release` |
| `foreign_private_issuer_v1` | `annual_20f` · `earnings_6k_watermark` (earnings-tagged 6-K reviewed-through watermark) · `earnings_release` (nullable — only where a company issues one separately from the 6-K itself) |

**Deterministic ordering — closed rule, no discretion:**

- **SEC filing channels** (`annual_filing`, `quarterly_filing`, `event_filing_watermark`,
  `annual_20f`, `earnings_6k_watermark`): primary ordering is **official SEC acceptance
  datetime**; deterministic tie-breaker is the **accession identifier**.
- **Official company-release channels** (`earnings_release`): primary ordering is the
  **verified official publication datetime supplied by the governed adapter**; deterministic
  tie-breaker is the **stable source identifier**.
- **Retrieval time is never an ordering input, for any channel.**
- If a required adapter cannot establish the required official ordering metadata for a
  channel, the monitor does not guess — `monitor_state` becomes `degraded` (or `failed`, if
  no required adapter succeeded) for that run, per §10.
- **No regression:** a channel's value only ever advances, per the ordering rule above,
  except through a separately reviewed, explicitly labeled **correction PR** (distinct in
  kind from an ordinary incorporation PR — used only to fix a prior data-entry error).
- **Watermark channels specifically:** every triggering source up to the proposed watermark
  value must already be incorporated; an outstanding, un-incorporated earlier source
  prevents the watermark from advancing past it.

## 6. Filing-trigger profiles

Two closed profiles, selected per ticker at enrollment (§3), changeable only via a reviewed
registry PR. Neither profile makes a materiality judgment — every rule is a metadata match
(form type, exhibit tag), never content interpretation.

| Profile | Trigger behavior |
|---|---|
| `domestic_issuer_v1` | New 10-Q → trigger. New 10-K → trigger. **All** 8-Ks → trigger (no item-code materiality filtering — a deliberately conservative, purely metadata-driven rule). A deterministically-located official earnings release → trigger. |
| `foreign_private_issuer_v1` | New 20-F → trigger. 6-Ks trigger **only** when objectively tagged as earnings-related by fixed exhibit/description metadata (the same class of deterministic match used for the domestic earnings-release trigger — not content interpretation). Routine, non-earnings-tagged 6-Ks (e.g. monthly revenue disclosures) are observed in ephemeral monitor output only (§8) and never open or extend an episode. |

Investor-presentation and standalone guidance monitoring are explicitly **out of V1** —
deferred as an optional, per-company adapter capability, enableable only after a
deterministic official endpoint is independently verified for that specific ticker.

## 7. Cadence fingerprints

An overdue cadence event (PI-0011's strict rule, §2) produces its own deterministic
fingerprint even when no newer official filing exists — cadence staleness is a real trigger
in its own right, not merely a byproduct of filing detection.

A cadence fingerprint is derived from at least: `ticker`, the exact `review.next_due` value
that became overdue, and `template_version`. It moves through the same episode
fingerprint-state vocabulary as any source-derived fingerprint (§12) — `outstanding` →
`assigned` → `awaiting_human_incorporation` → `incorporated` — and participates in the same
freshness precedence (§9), snapshot/assignment-ordinal (§13), and replacement-authorization
(§14) mechanics as any other fingerprint. A **cadence-only, reviewed-no-change** incorporation
(§17) explicitly incorporates the cadence fingerprint while leaving filing checkpoint
channels unchanged, since no new filing was involved.

## 8. Monitor behavior and non-tracked writes

The monitor may: read the enrollment registry and checkpoint file (read-only); read each
enrolled company's `review:` block (read-only); compute observed freshness/monitor state;
create or update the two operational issue types (§15); produce ephemeral job output/logs,
including non-triggering routine FPI 6-K observations (§6), which are **ephemeral monitor
output only in V1** — not written into any issue.

The monitor may never write `freshness_registry.yaml`, `freshness_checkpoints.yaml`,
any company YAML, `staleness_report.md`, or any other tracked file. A tracked change of any
kind requires its own human-reviewed PR.

## 9. Freshness state vocabulary and precedence

`current` | `unverified` | `review_due` | `pending_human_review`. No fifth state is
introduced — `current` is simply made harder to reach (fully fail-closed) than before.

Freshness is never stored directly — it is derived, at read/render time, by one
deterministic precedence rule, evaluated top to bottom, first match wins:

1. **`pending_human_review`** if at least one fingerprint is `awaiting_human_incorporation`.
2. else **`review_due`** if no fingerprint awaits incorporation but at least one
   fingerprint is `outstanding` or `assigned`.
3. else **`unverified`** if no higher-precedence condition above applies, and **any** of
   the following is true:
   - `monitoring_enabled` is `false` (§3);
   - `checkpoint_status` is `pending` (§4);
   - no durable monitor-status record exists yet for this ticker (§15.1) — the monitor has
     never run;
   - the durable monitor-status record's latest `monitor_state` is `degraded` or `failed`
     (§10).
4. else **`current`** — reachable **only** if **all** of the following are true
   simultaneously:
   - `monitoring_enabled` is `true`;
   - `checkpoint_status` is `verified`;
   - a durable monitor-status record exists for this ticker;
   - that record's latest `monitor_state` is `healthy`;
   - no fingerprint is `outstanding`, `assigned`, or `awaiting_human_incorporation`.

Rank 4 is a five-way conjunction, not a fallback default — every one of the five conditions
must hold at once, and the absence of any one of them (including simply never having run
the monitor yet) resolves to `unverified`, not silently to `current`. This closes two gaps
a purely checkpoint/monitor-health-only rule left open: a ticker with `monitoring_enabled:
false` was not previously blocked from `current` by the freshness rule at all — the prior
two-condition rule never read `monitoring_enabled`, and no validator rule filled that gap
either: §4.1 prohibits `monitoring_enabled: true` together with `checkpoint_status:
pending`, not a `verified` checkpoint coexisting with `monitoring_enabled: false`, which
remains a valid, unenforced-by-any-validator combination. The corrected rule closes this
directly, not by adding a new validator restriction, but by making `monitoring_enabled:
true` an explicit rank-4 requirement — a ticker may sit at `checkpoint_status: verified`
with `monitoring_enabled: false`, and now correctly displays `unverified` rather than
`current` in that case; and a ticker whose monitor has literally never produced a durable
record had no explicit rule at all. Both are now direct, load-bearing precedence
conditions, not consequences inferred from elsewhere.

**Worked example — a new trigger arriving during pending review:** episode has fingerprint
A at `awaiting_human_incorporation` and newly-detected fingerprint B, `outstanding`. Rank 1
fires on A → displayed `pending_human_review`. A human incorporates A (→ `incorporated`,
naming only A). B is still `outstanding` → rank 1 no longer fires, rank 2 fires on B →
displayed `review_due`; the episode stays open. The rule alone — with no special case —
guarantees an older result's incorporation never silently closes an episode or produces
`current` while a newer trigger remains, because incorporation only ever names the
fingerprints it explicitly covers (§17).

**Worked example — the initial seven-ticker filing:** every row starts `monitoring_enabled:
false` and `checkpoint_status: pending`, and no monitor run has ever occurred for any of
them (no durable monitor-status record exists). All three independently satisfy rank 3 —
every one of the seven tickers displays `unverified` from the moment this filing is
accepted, and stays there until a later, separate bootstrap PR (§4) and at least one
subsequent healthy monitor run change that.

## 10. Monitor state vocabulary

`healthy` | `degraded` | `failed` — per ticker, per monitor run.

- `healthy`: every adapter required by that ticker's `filing_trigger_profile` reached and
  parsed cleanly this run.
- `degraded`: at least one required adapter failed, at least one other succeeded — a
  partial signal; "no trigger detected" cannot be trusted as complete.
- `failed`: no required adapter succeeded this run — zero signal.

The value used for gating and display is the **latest recorded state in that ticker's
durable monitor-status issue** (§15.1), not a purely in-memory value from the current run
alone — every run, healthy or not, updates that same durable record. Before that record
exists at all (the monitor has never run for this ticker), there is simply no `monitor_
state` value to read — §9 treats that absence itself as an independent `unverified`
condition, not as an unhandled or default-`current` case. Once a record exists,
`monitor_state` is one of five conjunctive conditions gating `current` (precedence rank 4,
§9), and `degraded`/`failed` is independently one of four disjunctive conditions producing
`unverified` (precedence rank 3, §9) — it never itself creates `review_due`/
`pending_human_review`. A refresh task may still be created while degraded, if a genuine
trigger was positively detected through a working adapter; a different adapter's failure
doesn't invalidate a working one's finding. **A ticker cannot be rendered `current` without
a durable, latest-recorded `healthy` monitor-status record — nor without `monitoring_
enabled: true`, a `verified` checkpoint, and zero outstanding/assigned/awaiting
fingerprints, all five simultaneously** (§9) — an ephemeral "probably fine" inference from
silence is never sufficient, and neither is any one of the five conditions alone.

## 11. Task state vocabulary

`none` | `reserved` | `running` | `completed` | `completed_with_source_limitations` |
`failed` — per task instance.

`result_status` for the non-`failed` terminal values is **workflow-derived from the
per-fingerprint disposition array** (§12), not independently trusted from Claude's own
top-level self-report: `completed` iff every fingerprint assigned to that instance is
disposed `covered`; `completed_with_source_limitations` iff at least one is `unresolved`.
`failed` is a distinct signal — the instance never produced a valid, schema-conforming
structured result at all (execution failure, not a disposition outcome).

## 12. Task disposition vs. episode fingerprint state

Two vocabularies, never merged.

- **Task disposition** (Claude's result, per fingerprint, per task instance):
  `covered` | `unresolved`. Provisional evidence coverage only — never authority to declare
  evidence incorporated.
- **Episode fingerprint state** (persists across task instances, episode-scoped):
  `outstanding` | `assigned` | `awaiting_human_incorporation` | `incorporated`.

| Event | Fingerprint-state transition | Driven by |
|---|---|---|
| Task reservation | `outstanding` → `assigned` (every fingerprint in the snapshot) | Workflow, mechanical |
| Task terminal, this fingerprint disposed `covered` | `assigned` → `awaiting_human_incorporation` | Workflow, mechanical |
| Task terminal, this fingerprint disposed `unresolved` | `assigned` → `outstanding` | Workflow, mechanical |
| Task `failed` | every fingerprint assigned to that instance → `outstanding`, regardless of any partial internal state | Workflow, mechanical |
| Human accepts / incorporates / explicitly confirms | `awaiting_human_incorporation` → `incorporated` | Human-reviewed incorporation PR (§17) |
| Human rejects / judges a covered result insufficient | `awaiting_human_incorporation` → `outstanding` | **A merged replacement-authorization record naming these exact fingerprints (§14) — never a bare issue comment, label, or undocumented manual action** |

**Only `incorporated` retires a fingerprint.** An episode cannot close while any fingerprint
is `outstanding`, `assigned`, or `awaiting_human_incorporation`.

**The rejection transition specifically requires a reviewed, version-controlled record.**
Unlike the four workflow-mechanical rows above (driven automatically by task termination),
`awaiting_human_incorporation` → `outstanding` is never triggered by an ordinary issue
comment, a label, or any other undocumented manual action. It requires a merged replacement-
authorization file (§14) that names the exact fingerprint(s) being rejected, identifies
their prior task instance(s), and records a reason and approval reference. **If a human
rejects a result without merging such a record, the fingerprint remains
`awaiting_human_incorporation`** — indefinitely, until either that record merges or a
human incorporation PR (§17) accepts it instead.

## 13. Task-instance identity — fingerprints and assignment ordinals

A task snapshot may contain multiple fingerprints with different attempt histories — a
single generation number for the whole instance is insufficient. Each snapshot instead
records, **per fingerprint**: `fingerprint`, `assignment_ordinal`.

- A fingerprint that has **never before reached `assigned`** receives `assignment_ordinal: 1`
  automatically — no authorization needed.
- A fingerprint that **has** previously reached `assigned` (regardless of what happened
  next — failed, returned unresolved, or was rejected after being covered) receives its next
  ordinal **only** when an exact, valid replacement authorization (§14) exists for it.

**Deterministic task-instance ID** = a hash of: `ticker`, `episode_id`, the sorted set of
`(fingerprint, assignment_ordinal)` pairs assigned to this instance, and `template_version`.
A snapshot may freely mix automatically-included fresh fingerprints (ordinal 1) with
authorization-covered previously-attempted fingerprints (each at its own authorized
ordinal) — inclusion is decided per fingerprint, never inferred from the presence of
unrelated new triggers in the same snapshot.

## 14. Replacement authorization

This mechanism serves **two related purposes**, both handled by the same artifact type:
(a) authorizing a previously attempted fingerprint's *next assignment*, and (b) recording a
human's decision to *reject* a `covered` result and return its fingerprint(s) to
`outstanding` (§12) — the version-controlled record that transition specifically requires.
A single filed record may do both at once (reject and simultaneously authorize the next
attempt) or only the first (reject and record why, leaving the next attempt for a later,
separate authorization) — `authorized_next_assignment_ordinal` is populated only when a
next assignment is intended in the same record.

**Single generalized rule for purpose (a):** any fingerprint that has ever reached
`assigned` requires a valid, exactly-matching replacement authorization before it can be
assigned again, for whatever reason it returned to `outstanding` — a failed instance, an
unresolved disposition, or a human-authorized rejection of a covered result. A fingerprint
that has never been assigned needs none. This single test replaces enumerating failure
modes individually.

**File and naming:** `intelligence/freshness_replacements/<ticker>-<episode>-<authorization-id>.yaml`,
one file per authorization, individually reviewed — not one growing shared ledger (a single
monolithic file would bury each authorization's diff in unrelated ones and invite merge
conflicts). `<authorization-id>` is a collision-resistant deterministic identifier (e.g. an
explicit authorization ID or a digest of the exact named fingerprint set) — chosen so the
filename stays stable and unique even as the episode's broader fingerprint set continues to
change around it. This directory is not created by this governance filing merely to
represent an empty directory (git does not track empty directories); this specification
authorizes the path and schema, and the first genuinely reviewed authorization PR creates it.

**Contents:** `episode_id`, the exact named fingerprint set this authorization covers,
`prior_task_instance_ids` (one or more — a fingerprint may have accumulated multiple prior
attempts before a human authorizes another), `authorized_next_assignment_ordinal`
(**nullable** — populated only when this same record also authorizes an immediate next
assignment; a rejection-only record that merely justifies the return to `outstanding`
leaves it null, deferring any reassignment to a later, separate record), `reason`,
`approval_reference`, `approval_date`.

**Validity:** an authorization's validity depends **only** on the named ticker and episode,
each exact named fingerprint, that fingerprint's prior task-instance and assignment history,
its current fingerprint state, the authorized next ordinal, and the approval reference — it
does **not** require equality with the episode's entire, continually-changing outstanding
fingerprint set. An authorization remains valid when unrelated new fingerprints are appended
to the episode elsewhere; it applies only to the fingerprints it names.

**Rules:** the workflow may read this file to permit a replacement assignment and/or to
permit the named fingerprint(s)' transition back to `outstanding` following a rejection; it
may never create or edit one. Every prior instance stays immutable and untouched. A
replacement instance receives its own fresh, distinct deterministic task-instance ID (§13) —
never a mutation of a prior ID. Cannot bypass enrollment, checkpoint verification, source
policy, the fixed task template, or the one-active-task-per-episode rule. Brand-new
fingerprints never need authorization, and the four workflow-mechanical fingerprint-state
transitions (§12) never need one either — only the human-rejection transition and a
same-fingerprint reassignment do. No wording in this mechanism uses "force," "retry,"
"rerun," or "bypass" — this document uses "replacement instance" and "reviewed
reassignment."

## 15. Operational issues

Two closed issue types, kept structurally and semantically separate — a monitor-status
issue never represents a freshness trigger, and a freshness episode never closes or stays
open based on adapter health.

### 15.1 Monitor-status issue (durable)

**One durable issue per enrolled ticker, created on that ticker's first attempted monitor
run — including a first run that comes back `healthy`.** It is not created only upon a
first failure, and it is not deleted or abandoned once healthy; the same issue, located by
its marker, persists and is updated for the life of that ticker's enrollment. Distinct
marker from episode issues (e.g. `<!-- freshness-monitor-status: TICKER -->`). Carries a
machine-state block (§15.3) recording: schema version, latest run time, the required
adapter set for that ticker's `filing_trigger_profile`, per-adapter outcome for the latest
run, the aggregate `monitor_state` derived from those outcomes (§10), and a state digest.

- **Open** while the latest recorded `monitor_state` is `degraded` or `failed`.
- **Closed** while the latest recorded `monitor_state` is `healthy`.
- **Updated idempotently** on every run, whether or not the state changed — the same issue
  reopens if health regresses after being closed, and closes again on recovery; it is never
  duplicated.
- **Never creates a refresh task by itself** — a trigger fingerprint (§6, §7), not monitor
  health, is what creates or extends a freshness episode.
- **Operational evidence only, not repository research authority** — nothing in this issue
  is Company Intelligence content, and nothing here is read as a research finding.

### 15.2 Freshness-episode issue

Opens only when at least one deterministic trigger fingerprint actually exists. Distinct
marker (e.g. `<!-- freshness-episode: TICKER-EPISODE_ID -->`). Owns reservation,
task-instance state and history, results, and human-incorporation references. Its record is
split into two parts (§15.3): an **append-only** history (the complete fingerprint
inventory, task-instance history, fingerprint transition history, and
incorporation/replacement-authorization references) and a **mutable current-state** block
(the four live fingerprint sets — `outstanding`, `assigned`, `awaiting_human_incorporation`,
`incorporated`, §12).

**Closure condition — fingerprint state only, independent of monitor health:** the episode
closes when, and only when, every fingerprint belonging to it is `incorporated`, none
remains `outstanding`, `assigned`, or `awaiting_human_incorporation`, and no newer trigger
has been appended to it. Monitor health (§10, §15.1) is never a closure condition for this
issue — it is tracked entirely separately, in the ticker's own monitor-status issue. **After**
an episode closes, what freshness is subsequently *displayed* for that ticker still depends
on the full fail-closed precedence rule (§9): `current` only if `monitoring_enabled: true`,
the checkpoint is `verified`, a durable monitor-status record exists, and its latest
`monitor_state` is `healthy`, all simultaneously; `unverified` if any one of those four is
unmet. That is a display computation performed after closure, not a condition of closure
itself.

### 15.3 Operational issue integrity

Both issue types carry a fail-closed **machine-state block**: a deterministic marker, a
schema version, a canonical structured state payload, a state digest, and (for the
freshness-episode issue) the append-only/mutable split described in §15.2. Human prose may
be appended outside this block for context, but carries no automation authority — the
workflow reads only the machine-state block to decide anything.

**Append-only, never overwritten or pruned:** the complete fingerprint inventory (every
fingerprint that has ever belonged to the episode); task-instance history; the fingerprint
transition history (a log of every state change); and incorporation/replacement-authorization
references. **Mutable canonical current state:** the `outstanding`, `assigned`,
`awaiting_human_incorporation`, and `incorporated` sets — a fingerprint moves between these
as events occur, but must never disappear from the append-only inventory or history.

The workflow must **fail visibly**, never recreate, overwrite, or guess, when: the marker is
missing or duplicated for a ticker; a machine-state block is malformed or fails its digest
check; a fingerprint appears in a current-state set without a corresponding entry in the
append-only inventory, or vice versa; the append-only transition history does not reconcile
with the current-state sets (e.g. a fingerprint's last logged transition doesn't match which
set it's currently in); task-instance history conflicts with the block's current state; or
one fingerprint appears assigned to two simultaneously `reserved`/`running` instances. Each
such condition halts the run for that ticker with a diagnostic, rather than silently
proceeding on an assumption.

## 16. Reusable Path-A refresh scope (fixed)

Every enrolled-company refresh task is generated only from a fixed, previously-governed
template — no new prose, no new permitted-question logic invented per run. Fixed scope:
identify newly disclosed facts; compare new official evidence against the incorporated
record (via the checkpoint, §4–§5); identify potentially stale statements; report changes
affecting documented risks/catalysts; assess representability under the frozen Company
Intelligence schema; report unresolved evidence and source limitations. **Explicitly out of
scope, always:** any repository write; any role, conviction, tier, allocation, ranking,
theme, or trading decision. A task is only auto-generable when: the ticker has a valid
enrollment row (§3) with `monitoring_enabled: true`; its checkpoint is `checkpoint_status:
verified` (§4); a deterministic trigger fired (§6, §7); and the task instance is filled
from the fixed template, parameterized only by ticker/fingerprints/checkpoint state — never
freshly authored questions.

## 17. Human incorporation

Five outcome types (the original four, with the "limitation remains / result rejected" row
split in two, per §12's distinction between a mechanical, workflow-driven transition and one
that requires a reviewed replacement-authorization record). A human incorporation PR
resolves **only** the fingerprints and channels it explicitly names — it can never
implicitly close a newer trigger that arrived after the
underlying task ran but before the PR merged (validated by checking the PR's named set is an
exact subset of currently-`awaiting_human_incorporation` fingerprints, touching nothing
else).

| Outcome | CI analytical content | `review.last_reviewed`/`next_due`/`log` | Checkpoint channels | Named fingerprints |
|---|---|---|---|---|
| Source-triggered, record changed | Updated as approved | Advanced | Every accepted channel advanced | Marked `incorporated` |
| Source-triggered, no analytical change | May remain unchanged | Advanced | Advanced to include the reviewed source | Marked `incorporated` |
| Cadence-only, no new source | Unchanged | Advanced | May remain unchanged | The cadence fingerprint (§7) marked `incorporated`; PR/`review.log` must explicitly state no newer source was incorporated |
| Source limitation remains (task's own `unresolved` disposition) | Unchanged | Not advanced for affected items | Affected channels not advanced | Already `outstanding` mechanically, via §12's workflow-driven transition — no separate PR action needed |
| Covered result rejected by a human | Unchanged | Not advanced for affected items | Affected channels not advanced | Remains `awaiting_human_incorporation` unless and until a merged replacement-authorization record (§12, §14) names it and transitions it to `outstanding` |

### 17.1 Partial incorporation

A `completed_with_source_limitations` task may leave some fingerprints `covered`
(→ `awaiting_human_incorporation`) and others `unresolved` (→ `outstanding`) within the same
instance. A human may incorporate an explicitly named `covered` subset without waiting for
the rest:

- accepted fingerprints become `incorporated`;
- accepted checkpoint channels may advance only through the exact accepted sources, and only
  when the channel's ordering (§5) remains contiguous — no skipping an intervening
  un-incorporated source;
- unresolved fingerprints remain `outstanding`; the episode stays open;
- derived freshness (§9) remains `review_due` once no fingerprint remains
  `awaiting_human_incorporation` but at least one remains `outstanding`/`assigned`;
- `review.last_reviewed`/`next_due` are **not** advanced as though the full review episode
  were complete while any required episode fingerprint remains unresolved — advancing those
  fields is reserved for the point at which every fingerprint in the episode has reached
  `incorporated`.

**Narrow exception — a `review.log` entry without advancing `last_reviewed`/`next_due`:** a
partial-incorporation PR may append a `review.log` entry documenting what was reviewed and
incorporated in that partial step (naming the accepted fingerprints/channels) without
advancing `last_reviewed`/`next_due`, since the log is an append-only narrative record, not
itself the cadence checkpoint. This is the only case where a `review.log` write is permitted
independent of `last_reviewed`/`next_due` — every other incorporation type advances the log
and the dates together, or advances neither.

At final, complete incorporation (every fingerprint in the episode `incorporated`), the
human-reviewed PR advances `review.last_reviewed`/`next_due`, appends a closing `review.log`
entry referencing the completed episode, and the episode issue closes.

## 18. Post-incorporation freshness (no unconditional "current")

A merged incorporation PR updates the accepted baseline but never unconditionally sets
freshness to `current`. Two separate questions apply immediately after merge, and they are
evaluated separately — episode closure is fingerprint-state-only (§15.2); displayed
freshness also depends on monitor state (§9, §10):

**Episode closure (fingerprint state only, §15.2):** the episode closes if and only if
every fingerprint belonging to it is `incorporated`, none remains `outstanding`, `assigned`,
or `awaiting_human_incorporation`, and no newer trigger has been appended — **regardless of
monitor health**. If any fingerprint remains in a blocking state, the episode stays open,
whatever the monitor's latest recorded state is.

**Displayed freshness (the same fully fail-closed precedence rule as §9, restated here
against post-merge state, evaluated whether or not the episode just closed):**

| Remaining state | Displayed freshness |
|---|---|
| Outstanding/assigned fingerprints remain | `review_due` |
| Awaiting-incorporation fingerprints remain (partial PR) | `pending_human_review` |
| Nothing remains in the episode, but **any** of: `monitoring_enabled` is `false`; the checkpoint is still `pending`; no durable monitor-status record exists yet; that record's latest `monitor_state` is `degraded`/`failed` | `unverified` |
| Nothing remains in the episode, **and all** of: `monitoring_enabled: true`; checkpoint `verified`; a durable monitor-status record exists; its latest `monitor_state` is `healthy` | `current` |

The episode issue's closure (top paragraph) and the ticker's displayed freshness (this
table) are independent outcomes of the same merge: an episode can close with the ticker
still showing `unverified` (e.g. all fingerprints incorporated, but the monitor is
currently unhealthy, or monitoring was never enabled for this ticker in the first place) —
in that case the episode issue itself closes normally, while whatever §9 condition is still
unmet (a monitor-status issue open per §15.1, or `monitoring_enabled` simply still `false`)
is what keeps the ticker at `unverified` rather than `current`.

## 19. Path A / Path B authority

**Path A (enrolled-company refresh):** ticker has a valid, verified enrollment row; task
drawn from the fixed template (§16); questions are exclusively the generic fixed scope —
never bespoke, ticker-specific questions.

**Path B (explicit bounded task):** a separately authorized decision (its own PI-000x or
equivalent), may cover companies without a Company Intelligence record, uses the same
secure executor architecture as Path A but is never described as an enrolled-company refresh.

**PI-0014 (INTC/SYK/DHR) is, and remains, Path B** — none of INTC/SYK/DHR appear in the
verified seven-ticker roster (§3), and PI-0014's permitted questions are bespoke and
ticker-specific, not the generic Path-A scope (§16). It is not, and does not become, the
framework's total scope; it is the framework's *intended* first Path-B pilot — identified,
not itself executed, by this specification.

**`PI-0014`'s current, accepted scope, stated precisely:** exactly one bounded,
conversation-based, read-only evidence-gathering exercise; its own findings-lifecycle
clause states findings remain conversational, with no committed research artifact and no
repository change produced by that authorization itself. This specification identifies
`PI-0014` as the Path-B template case for illustrating how the framework's execution
architecture (§1, §8, §15) would apply to it — it does **not** itself grant `PI-0014`
unattended execution, does **not** itself convert its findings into GitHub issue output, and
does **not** itself supply it a runtime prompt, schema, schedule, or activation. Persistent
issue output, unattended execution, runtime prompts/schemas, scheduling, and activation for
`PI-0014` each require their own later, explicit implementation or activation authorization,
per §21 — not granted here, and `PI-0014` must not be described as currently
"issue-output-only" until such an authorization exists.

## 20. Explicit non-goals

No repository write outside a human-reviewed PR, by any layer, ever. No automatic retry of a
failed task instance under its own ID, ever. No conviction, `portfolio_role_ref`, theme
membership, ranking, tier, target, weight, cluster, margin, trade, or allocation authority,
anywhere in this framework. No live source URL, adapter endpoint, or GitHub Actions action
pin is defined by this document — those belong to the implementation PR. No investor-
presentation/guidance monitoring in V1. No moot/waive-without-research path for a fingerprint
that never reaches `covered` — undefined in V1; a future need there is its own decision.

## 21. Implementation-phase gates (deferred, not authorized here)

A future implementation PR must, at minimum: define the GitHub Actions workflow and its
job/permission structure; define and pin every action reference by full commit SHA; define
live adapter endpoints and verify their official-metadata ordering guarantees per §5; draft
the reusable Path-A prompt/schema and confirm `intelligence_report.py`'s overdue-logic
reusability per §2; implement the checkpoint/registry/replacement validators per §4.1 and
§15.3; and pass its own separate review before merge. Separately, before `PI-0014` can run
unattended or produce issue output as this framework's Path-B pilot (§19), its own
implementation and activation each require their own explicit, separately reviewed
authorization — a runtime prompt, a runtime schema, a schedule, and an activation step, none
of which exist yet and none of which are granted by `PI-0014`'s current accepted scope or by
this document. None of this is authorized by filing this ADR or this specification.

## 22. Related decisions

`GOV-0001` (governance architecture this filing follows), `PI-0011` (staleness-reporting
authority this framework consumes and reconciles with, never duplicates), `PI-0014`
(the framework's first Path-B pilot, placed per §19). Each enrolled ticker's own
`company_record_authority` (§3) is recorded per-row in the registry, not enumerated in the
ADR's frontmatter.
