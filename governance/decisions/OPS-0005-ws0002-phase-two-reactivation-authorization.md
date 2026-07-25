---
decision_id: OPS-0005
date: 2026-07-25
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, OPS-0004, GOV-0002, PI-0011]
supporting_artifact: docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md
---

## Context

`OPS-0002` scoped and audited a WS-0002 planning baseline
(`docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`) but granted **no**
implementation authority (item 5: "no architecture-implementation authority is
granted"). `OPS-0003` recorded that planning-and-audit phase complete and
restored WS-0001 to `priority: primary`, while stating explicitly that "any
future Layer 2 architecture implementation... requires its own new, explicit
governance decision to reactivate and authorize it — this decision does not
do so, and does not lower that bar." `OPS-0004` retained the Phase One
independent-audit artifact and, in its own scope-withheld clause (item 6),
restated the same boundary: "no reactivation of WS-0002 beyond its existing
`status: complete` (planning-and-audit phase only)... It does not supersede
`OPS-0002` or `OPS-0003`'s substance."

Three things are therefore established as settled fact, not in tension with
each other: WS-0002's planning-and-audit phase is complete; `OPS-0002`,
`OPS-0003`, and `OPS-0004` each deliberately withheld implementation
authority; and no accepted decision anywhere in `governance/decisions/`
authorizes any WS-0002 implementation (confirmed by a repository-wide search
of every decision file for "phase two" / "phase-two," returning zero hits
before this filing). A new, explicit decision is required before any code
work begins — this is that decision, and it is deliberately narrow: it
reactivates WS-0002 for exactly one bounded slice of the blueprint's roadmap,
not for the architecture as a whole.

The principal has explicitly authorized drafting and filing exactly this
decision, the corresponding `operations/WORKSTREAMS.yaml` synchronization,
governance validation, and a draft pull request — and has explicitly withheld
authorization for Phase Two production implementation itself, any status-layer
code or tests, Phase Three, WS-0003, replacing the default daily workflow, S3
margin research, any allocator/holdings/targets change, Intelligence-to-
allocation coupling, scoring/ranking/aggregation/conviction computation, order
execution, or unrelated cleanup. This filing contains no implementation code.

## Decision

**Reactivates `WS-0002` narrowly, for exactly one bounded slice of the
blueprint's roadmap: Phase Two, a thin, consolidated, read-only status/report
layer.** Nothing else about WS-0002's architecture is reactivated by this
decision.

### 1. Finding

- WS-0002's planning-and-audit phase (`docs/PORTFOLIO_HQ_UNIFIED_CORE_BLUEPRINT_V1.md`,
  audited, accepted, merged via PR #143; provenance-reconciled via `OPS-0004`)
  is complete.
- `OPS-0002` item 5, `OPS-0003` item 1, and `OPS-0004` item 6 each
  intentionally withheld implementation authority — none of that withholding
  is disputed, weakened, or found mistaken here.
- No currently accepted decision authorizes any WS-0002 implementation.
- A new, explicit decision is therefore required before Phase Two code work
  begins. This filing is that decision, and it authorizes Phase Two only.

### 2. Grant — Phase Two, read-only status/report layer

Authorizes a thin, consolidated, read-only status/report layer that may
**display** existing system facts already computed by existing components —
it computes nothing new and derives no fact `allocate.py`, `margin_state.py`,
`intelligence_report.py`, or `freshness_validator.py`/`freshness_state.py`
does not already produce:

- portfolio/allocation health already calculated by existing components (the
  same facts `allocate.py --health` already surfaces: cluster-cap proximity,
  T1/T2 ceiling proximity, crypto-sleeve drift, leverage/buffer context);
- margin debt, buffer, risk state, sync date, and staleness (`margin_state.py`,
  `holdings.yaml`);
- market-data and earnings-data gaps already surfaced by existing components
  (`earnings.py`'s `unavailable` flags, `alpaca_client.py` pricing gaps);
- Intelligence freshness states, read through `intelligence_report.py`'s
  existing **public** API only (e.g. its staleness-collection function),
  never reimplemented — the identical reuse-not-reimplement discipline
  `PI-0011` established for `intelligence_validator.py`;
- an explicit, itemized list of missing, stale, unavailable, or degraded
  inputs — a genuine gap must be shown as a gap, never silently treated as
  current.

### 3. Permitted implementation scope — exactly one implementation PR

Authorizes **exactly one** narrow implementation pull request — the smallest
number this decision's scope requires, so that no future session may invent
additional PRs, phases, or scope under this same authorization. That one PR
may contain, and nothing else:

1. One thin status/report module (repository root, sibling to
   `intelligence_report.py`/`freshness_validator.py`; exact filename decided
   at implementation time following existing naming convention).
2. Its dedicated test module.
3. A minimal usage-documentation addition (a short `CLAUDE.md`/`README.md`
   pointer) — only if repository convention requires one for a new CLI entry
   point, matching how `intelligence_report.py` and `freshness_validator.py`
   were each documented.
4. The ordinary `operations/WORKSTREAMS.yaml` register synchronization
   recording that PR's merge (mirroring the `OPS-0003`/`PI-0011` pattern).

No generated or tracked report file is authorized — the layer is **stdout-only
and display-only**, deliberately simpler than `intelligence_report.py`'s
single-writer `staleness_report.md` pattern, so it carries no artifact of its
own to keep current or drift from its sources.

### 4. Mandatory boundaries

The Phase Two implementation must remain, at all times: advisory;
display-only; read-only by default; additive; outside `allocate.py`'s
calculation path; outside margin research and S3; and outside the default
daily workflow (`run_portfolio_check.sh` or its successor) until separately
authorized.

**Dependency direction (binding, testable):** the status module may *read
from* the already-computed, public outputs of `allocate.py`, `margin_state.py`,
`intelligence_report.py`, and the `freshness_*` modules — one-directional,
forward only. `allocate.py`, `margin_state.py`, every `intelligence/`
production code path, and every `freshness_*` module must **never** import,
read, or otherwise depend on the new status module, in any form — this is the
"reverse import" boundary Fable Audit Gate #2 (§5 below) must verify. Any
function called on an existing module must be that module's public API; no
underscore-prefixed private function may be imported, matching the
`intelligence_report.py`/`intelligence_validator.py` precedent exactly.

It must not, under any interpretation:

- alter allocator formulas, recommendations, gaps, targets, tiers, weights,
  caps, or gates — for identical inputs, the allocator's output must be
  provably unchanged with and without the new module present;
- modify `holdings.yaml` or `targets.yaml`;
- create conviction scores, rankings, opportunity scores, or aggregation of
  any kind;
- make any Company or Theme Intelligence record mathematically load-bearing
  to any allocator computation;
- create a reverse import into allocator or Intelligence production code (see
  above);
- consume any `MARGIN-0005` research output (simulation results, trial data,
  or any file under `research/margin_target_study/`);
- create a trial ledger, candidate freeze, runner, or results directory of
  any kind;
- execute or submit any order;
- silently treat stale, missing, or degraded data as current — a gap must be
  shown as a gap;
- replace `run_portfolio_check.sh` or the current daily workflow;
- begin Phase Three, or any WS-0003 (daily allocation-check UX) work.

### 5. Review and merge gate — Fable Audit Gate #2

The Phase Two implementation PR requires **Fable Audit Gate #2** — the
blueprint's §8, checkpoint 2 ("after material architecture implementation,
before it becomes the default workflow") — performed against that PR's exact
head commit, before it may be marked ready or merged. Per `OPS-0004` item 5's
forward evidentiary rule, this checkpoint is satisfied only by a **retained,
independently attributable artifact** filed under `governance/audits/` per
its README convention — narrative claimed only in a PR body or commit message
does not suffice.

The gate must verify, at minimum:

- exact scope (only the items enumerated in §3 above were added);
- dependency direction (§4's reverse-import boundary holds, both ways);
- read-only behavior (no write path exists beyond ordinary stdout/CLI output);
- no output mutation (no file the module reads is ever modified by it);
- unchanged allocator recommendations for identical inputs, before and after
  the module's addition;
- degraded-input visibility (a missing/stale/unavailable input is shown as
  such, never silently treated as current);
- test and validator results (dedicated tests, full suite, `intelligence_validator.py`,
  `freshness_validator.py` all independently re-executed, not merely cited);
- absence of any Intelligence/allocator coupling and any research/production
  coupling described in §4.

### 6. Effectivity

- This decision becomes effective only when its own governance pull request
  (this filing) merges to `main` — not when pushed, and not merely when
  opened as a draft.
- No Phase Two implementation work is authorized before that merge.
- Once effective, opening the one implementation PR authorized by §3 is
  permitted — but that PR itself may not merge until Fable Audit Gate #2
  (§5) is complete against its exact head and the principal has explicitly
  accepted both the implementation and the audit's conclusions.
- Phase Two completion does not authorize Phase Three.
- Phase Two completion does not authorize S3 (`MARGIN-0005`/WS-0001 research
  execution).
- Any integration of this status layer into the default daily workflow
  requires its own separate future governance decision.

### 7. Supersession — narrow and explicit

- **`OPS-0002` item 5** ("no architecture-implementation authority is
  granted") is **not** superseded. It remains a true, unchanged statement of
  what `OPS-0002` itself authorized (nothing). This decision is the separate,
  later grant `OPS-0002` item 7 and `OPS-0003`/`OPS-0004` each anticipated
  would eventually be required — it does not rewrite what OPS-0002 already
  said about itself.
- **`OPS-0003` item 1**'s clause "requires its own new, explicit governance
  decision to reactivate and authorize it — this decision does not do so" is
  **narrowly superseded, exactly to the extent that this filing is that new,
  explicit decision** and now reactivates WS-0002 for the bounded Phase Two
  scope in §2–§4. `OPS-0003`'s recording of the completed planning-and-audit
  phase, its WS-0001 priority restoration, and every other clause are
  unaffected and remain fully effective.
- **`OPS-0004` item 6**'s clause "no reactivation of WS-0002 beyond its
  existing `status: complete` (planning-and-audit phase only)" is **narrowly
  superseded, exactly to the extent that this filing now reactivates WS-0002**
  for Phase Two as scoped above. `OPS-0004`'s retained audit artifact, its
  FA-1 provenance reconciliation, its forward evidentiary rule for future
  audit checkpoints (which this decision relies on directly in §5), and every
  other clause are unaffected and remain fully effective.
- No other clause of `OPS-0001`, `OPS-0002`, `OPS-0003`, or `OPS-0004` is
  superseded, qualified, or reinterpreted by this decision. WS-0001's
  priority, authority, milestones, and `MARGIN-0005` charter status are
  untouched. WS-0002's own priority is **not** changed by this decision —
  it remains `priority: secondary`; re-prioritizing it would require its own
  separate, explicit decision under `OPS-0002` item 7, which this filing does
  not attempt.

## Rationale

This follows the exact discipline `OPS-0003` and `OPS-0004` already applied to
themselves: a narrow, explicit supersession of only the clauses that
anticipated this moment, leaving everything else standing. `OPS-0003` named
its own future condition precisely ("requires its own new, explicit governance
decision") and `OPS-0004` restated it; this decision is that condition being
met, not a reinterpretation of either. Scoping the grant to a read-only,
stdout-only status layer — rather than any part of the blueprint's Layer 2
recommending architecture — follows Constitution §4/§5's standing bar against
new standing analysis layers: a display of already-computed facts adds no new
prediction, score, or opportunity map, and is the narrowest possible slice of
the blueprint's roadmap that could plausibly be called "Phase Two." Requiring
Fable Audit Gate #2 with a retained artifact, rather than accepting narrative
alone, is a direct application of `OPS-0004`'s own forward rule (item 5) —
the exact evidentiary gap that decision exists to prevent recurring. The
dependency-direction rule (§4) generalizes `PI-0011`'s own binding
"zero-import-relationship-in-either-direction" pattern for
`intelligence_report.py`, adapted to this layer's different need (it must
read allocator/margin facts to display them, unlike `intelligence_report.py`,
which is barred from touching `allocate.py`/`margin_state.py` at all) — the
adaptation is the one-directional read permission stated explicitly in §4,
not a loosening of the underlying discipline.

## Alternatives Considered

- **Reactivate all of WS-0002's Layer 2 architecture at once.** Rejected —
  far exceeds the principal's explicit authorization, which is bounded to
  exactly the read-only status/report slice; the blueprint's Layer 2
  recommending role (target/tier/cluster policy recommendations) remains
  wholly unauthorized by this decision.
- **Treat `OPS-0004`'s retained Phase One audit artifact as also satisfying
  Fable Audit Gate #2.** Rejected — that artifact evaluated the Phase One
  *planning* baseline at a merged SHA before any implementation existed; it
  cannot stand in for a later audit of an implementation PR that does not yet
  exist. `OPS-0004` item 5 itself requires a fresh, retained artifact for each
  future checkpoint.
- **Skip the one-implementation-PR ceiling and let the count be decided at
  implementation time.** Rejected — `OPS-0002`/`OPS-0003`/`MARGIN-0005` all
  fix PR ceilings explicitly (the S2 charter's own ≤3-PR ceiling is the
  clearest precedent) precisely so a later session cannot invent scope; the
  same discipline applies here.
- **Authorize a generated/tracked report file**, mirroring
  `intelligence_report.py`'s `staleness_report.md`. Rejected for Phase Two —
  the task's own framing ("display-only") and this decision's narrower,
  stdout-only design avoid a second artifact that could drift from its
  sources; nothing prevents a future decision from adding one if a real need
  is demonstrated.
- **Let the status module read Intelligence records or `MARGIN-0005` research
  output directly**, rather than only already-validated public-API output.
  Rejected — would reopen exactly the coupling `PI-0011`, `ONTO-0001`, and
  `MARGIN-0005`'s isolation guards already close; §4 forecloses it explicitly.
- **Reprioritize WS-0002 to `priority: primary`** now that it is reactivated.
  Rejected — not requested by the principal's authorization, and would
  require its own separate decision under `OPS-0002` item 7; this filing
  deliberately leaves WS-0001/WS-0002 priority exactly as `OPS-0003` set it.
- **Fold the Decisions Log / `governance/decisions.yaml` index update into
  this same PR**, as `OPS-0002`/`OPS-0003`/`OPS-0004` each did. Considered,
  but the principal's authorization for this filing bounds it to exactly the
  new decision file and the `operations/WORKSTREAMS.yaml` synchronization —
  narrower than the usual convention. Recorded here as a known, deliberate
  gap: the governance index and CLAUDE.md Decisions Log pointer for OPS-0005
  are not added by this PR and would need a small, separate follow-up.

## Consequences

Going forward: WS-0002 carries a bounded, explicit implementation authority —
exactly one read-only, stdout-only status/report PR, gated on Fable Audit
Gate #2 with a retained artifact and explicit principal acceptance before it
may merge. Nothing about the blueprint's Layer 2 recommending architecture,
Phase Three, WS-0003, S3/`MARGIN-0005` research, or the default daily workflow
is authorized, reactivated, or implied by this decision. `OPS-0002` item 5 is
unaffected; `OPS-0003` item 1 and `OPS-0004` item 6 are narrowly superseded
exactly as stated in §7, and nothing else in either decision changes. No
allocator, `targets.yaml`, `holdings.yaml`, margin, Intelligence, or research
file is touched by this decision. This decision and the corresponding
`operations/WORKSTREAMS.yaml` synchronization become effective only when this
exact implementing pull request merges to `main` — not when pushed, and not
when merely opened as a draft. The next concrete step is principal review of
this draft PR, not implementation, and not merge.
