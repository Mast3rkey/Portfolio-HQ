---
decision_id: OPS-0015
date: 2026-08-03
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, OPS-0011, OPS-0012, OPS-0013, OPS-0014, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
---

## Context

Portfolio-HQ's user-facing surface today is a read-only, repository-native dashboard (`OPS-0011`/`OPS-0012`/`OPS-0013`, `WS-0007`) plus historical standalone HTML reports. No decision has yet recorded why that surface exists, what it is ultimately meant to become, or how its future phases relate to one another and to the workstreams already in flight (`WS-0002`'s status/report layer, `WS-0003`'s deferred daily-check UX, `WS-0005`'s Intelligence/relationship work, `WS-0007`'s dashboard, `WS-0013`'s final-allocation-readiness roadmap). Each of those decisions is narrowly bounded to its own slice and none states the connecting mission.

Separately, this repository's session-to-session working pattern — many independent Claude Code sessions, each spun up from a fresh isolated clone with its own bounded mandate — has no single decision recording the operating defaults for how many mutation lanes may run at once (`OPS-0014` §D already answers this, but no decision cross-references it as a *parallel-work protocol*) or how a session should handle work it discovers but isn't authorized to perform.

The controlling human repository principal has explicitly authorized exactly one bounded governance-and-roadmap-synchronization unit to record: (1) that Portfolio-HQ is first being built as a personal system for the principal, not a general product; (2) a phased roadmap for a future unified, repository-native application, each phase separately gated behind its own future authorization; (3) the parallel-work and discovered-work protocols this repository's multi-session pattern already needs; and (4) that commercialization is a deferred, unauthorized, non-blocking possibility, not a current objective. No architecture audit or roadmap-reconciliation audit artifact is retained anywhere in this repository supporting this framing (see §H) — this decision records the principal's explicit direction, not an inspected audit.

## Decision

OPS-0015 records, as durable governance authority, the personal-first mission for Portfolio-HQ's current development, a phased roadmap for a future unified repository-native application, the parallel-work and discovered-work-reconciliation protocols already implicit in this repository's multi-session pattern, and an explicit, non-blocking deferral of commercialization. **This decision authorizes no application implementation, no code change, no research, no relationship mapping, no chart interpretation, no holdings/allocation/margin/brokerage/order change, and no new workstream.** It is procedural and roadmap-bearing only.

### A. Personal-first mission

Portfolio-HQ is first being developed as a deeply personal, repository-native, recommendation-only investment operating system for the human principal. Current work should optimize for: the principal's actual holdings and workflow; evidence-backed company and portfolio research; governed targets and gates; manual Robinhood execution; repository traceability; understandable recommendations and abstentions; and a unified personal application experience. Current development is explicitly **not** constrained by: App Store requirements; multi-user architecture; broad customer onboarding; subscriptions; external customer support; generalized portfolio models; or brokerage order execution.

### B. Unified repository-native application mission

Portfolio-HQ's user-facing application is one visual and interactive projection of live GitHub repository truth. It must: disclose repository, branch, exact SHA, fetch time, sync state, and validation state; visualize holdings, targets, gates, tiers, caps, Intelligence, themes, freshness, evidence, governance, workstreams, roadmap, and allocation readiness; expose source paths and provenance; call, never duplicate, `allocate.py`; remain recommendation-only; abstain when required state is stale, conflicting, or unverifiable; distinguish recommendations from confirmed execution; preserve manual Robinhood execution; and never become a competing holdings ledger, hidden database, policy store, allocator, or order system. Historical standalone HTML reports remain retained evidence artifacts, not the living application — unchanged by this decision.

### C. Phased application roadmap

The following phases are recorded as dependency-gated future roadmap items, **not** current implementation authority. Each requires its own separate future authorization unless a controlling accepted decision already covers a bounded portion of it:

- **Phase A — Repository provenance and origin-sync visibility.** Exact local/main/origin comparison; repository SHA and sync status; clean/diverged/stale state; open PR and CI visibility; system provenance. (`OPS-0011` already delivers a bounded slice of this via the dashboard's provenance panel.)
- **Phase B — Unified read-only command center.** Portfolio summary; holdings, targets, gates, and warnings; research and freshness status; governance and roadmap status; system validation health.
- **Phase C — Research, evidence, governance, and roadmap navigation.** Company Intelligence; theme Intelligence; primary-source evidence; disconfirming evidence; thesis-break conditions; charts and provenance; decision history and supersession; workstream milestones and blockers. (`OPS-0013`'s Governance Decision Explorer already delivers a bounded slice of this.)
- **Phase D — Portfolio relationship and correlated-risk visualization.** Dependencies; customers and suppliers; competitors and substitutes; duplicate exposure; shared economic drivers; correlated-loss scenarios. Depends on `WS-0005` Milestone 4 relationship mapping, which remains unauthorized.
- **Phase E — Guarded advisory allocation-check launcher.** Verify readiness; preview exact inputs; collect external facts not persisted in the repository; invoke existing `allocate.py`; display recommendations, gates, blocks, caps, warnings, and undeployed cash; record nothing without separate authority; never place orders. Overlaps `OPS-0007` §5's already-authorized scenario-display bridge, which this decision does not narrow, widen, or duplicate.
- **Phase F — Governed `OPS-0014` factual-sync interface.** Preview the exact factual delta; launch the accepted repository workflow; no silent browser-side state mutation; no direct write to `main`; principal factual confirmation and exact-head acceptance remain required.
- **Phase G — Conversational operator.** A natural-language interface over governed read, explanation, factual-sync, and allocation workflows. Requires its own separate future authority and may not create policy or execution authority. This is `WS-0003`'s eventual, still-unauthorized scope, not a new grant — see §I.

### D. Parallel-work and session protocol

- **One active repository mutation lane at a time** — this restates, and does not narrow or widen, `OPS-0014` §D: at most one active mutation lane (branch/PR) runs against Portfolio-HQ at a time; no concurrent branch/PR mutations.
- Multiple distinct read-only lanes may operate concurrently in isolated clones, since Class 0 work (`OPS-0014` §A) creates no branch or PR.
- Practical default maximum: one mutation lane plus up to three focused read-only lanes.
- Company research may be parallelized only after the governed universe, schema, scope, and evidence standard for that research are frozen by their own governing decision (`OPS-0008`'s wave protocol is the existing example for Company Intelligence batches).
- Parallel researchers do not independently edit shared tracked files; multiple research outputs require one reconciliation pass before tracked implementation.
- One implementation branch and one PR per coherent authorized unit.
- Fresh exact-head review begins only after the author's head freezes; corrections use bounded delta review unless authority, scope, or behavior materially changes (`OPS-0009`'s Lane C).
- Completed audits are not repeated without changed evidence, verified staleness, error, incompleteness, or reopening authority.
- Every handoff includes: the full terminal start directory, exact start command, absolute workspace path, role, objective, authority, allowed and prohibited scope, tests, stopping condition, and final-report requirements.
- Principal authority belongs to the human repository owner; Claude and ChatGPT sessions hold no independent acceptance or merge authority.

### E. Discovered-work reconciliation

Every substantial task should report newly identified material completion work — a task or gap, its controlling evidence, the owning workstream, current authorization, dependency and priority, a proposed milestone, an objective completion criterion, the smallest next unit, and whether repository synchronization is required. A session must not silently implement newly discovered scope, must not leave material completion work recorded only in chat, must not clutter the register with unsupported speculation, must reconcile and de-duplicate findings before implementation, and must keep factual synchronization, roadmap refinement, and new authority distinct from one another. This is a reporting discipline; it grants no standing authority to act on what is discovered.

### F. Deferred commercialization

After Portfolio-HQ reaches a stable and validated personal operating state, the principal may separately evaluate whether its architecture is useful to other investors. Any commercialization, App Store distribution, multi-user architecture, licensing, monetization, external brokerage integration, regulated-advice implication, legal review, privacy architecture, or security program requires its own future, principal-initiated charter and authority. This milestone is proposed, unauthorized, dependency-gated, non-blocking, and not a current implementation objective. Commercialization must not delay or reshape completion of the personal system.

### G. Final governed allocation check — convergence point

The roadmap above converges, eventually, on: fully synchronized live holdings, margin, cash, and account facts; complete and fresh research; completed relationship and correlated-risk analysis; a zero-based portfolio review; human principal policy approval; implementation and validation of approved policy; one advisory `allocate.py` run; manual execution or deliberate non-execution; and factual reconciliation afterward. This mirrors `WS-0013`'s already-recorded fifteen-step sequence and abstention criteria (`operations/WORKSTREAMS.yaml`, `WS-0013`) — restated here as the application roadmap's own eventual destination, not a second or competing sequence. **This decision does not authorize any step of that sequence.**

### H. Audit-provenance limit

No app-architecture audit report and no roadmap-reconciliation audit report exist as retained repository artifacts. This decision must not be read to imply that such audits were inspected as repository evidence. The mission and roadmap wording above is recorded solely because the human repository principal explicitly authorized it in this session's own prompt. No audit provenance is claimed or manufactured by this filing.

### I. Supersession and non-authority

This decision records mission, phases, and procedural boundaries. It creates no application implementation authority. It does not supersede investment policy or any accepted decision governing tiers, targets, gates, clusters, caps, margin, allocator behavior, or brokerage/order handling. It does not alter `OPS-0014` except through the explicit, narrow cross-reference in §D above — `OPS-0014`'s own text is unedited. It does not authorize `WS-0003`'s conversational-operator implementation (§C Phase G remains exactly as unauthorized as `WS-0003` already records it). It does not authorize research, relationship mapping, chart interpretation, holdings changes, allocation changes, margin, brokerage, or orders. `operations/WORKSTREAMS.yaml` remains non-authoritative — a recording register, not a source of authority, per `OPS-0001`.

## Rationale

Four future-facing workstreams (`WS-0002`, `WS-0003`, `WS-0007`, `WS-0013`) already carry pieces of an eventual personal application without any record connecting them or stating why the application exists. Leaving that mission unstated risks a future session either under-scoping a future phase's request (not realizing it fits an already-anticipated slot) or over-scoping one (treating an unrelated dashboard idea as free-standing, without the "call, never duplicate, `allocate.py`" and "recommendation-only" discipline `OPS-0011` already established). Recording the phases now, each still gated behind its own future authorization, lets a future authorization request cite a specific phase rather than re-litigating the whole shape of the application. Separately, `OPS-0014` §D's active-lane rule already governs concurrency but has never been named as part of a broader parallel-work protocol, and no decision has stated a reporting discipline for work a session discovers but isn't authorized to perform — both gaps this repository's growing multi-session pattern (dozens of isolated clones per the workspace directory listing alone) makes concrete rather than hypothetical. The commercialization deferral closes a question the "personal-first" framing would otherwise leave implicit: that a future evaluation is possible without it becoming an unstated present-day constraint on the personal system's completion.

## Alternatives Considered

**Do nothing; let each future phase justify itself independently when proposed.** Rejected — this is exactly the status quo this decision is filed to correct; without a recorded mission and phase map, `WS-0002`/`WS-0003`/`WS-0007`/`WS-0013` continue to read as four unconnected entries rather than dependency-ordered slices of one destination.

**Fold this into `WS-0007`'s register entry alone, as another dashboard milestone.** Rejected — the mission and roadmap span more than the dashboard: `WS-0002`'s status layer, `WS-0003`'s deferred UX, and `WS-0013`'s final-allocation-readiness sequence are all part of the same eventual application and none of them is a `WS-0007` phase. A governance decision, cross-referenced additively into each affected workstream, matches this repository's existing pattern (`OPS-0011`/`OPS-0012`/`OPS-0013` each did this for `WS-0007` specifically; this decision does the equivalent across four workstreams at once).

**Create a new workstream for the unified-application mission itself.** Rejected — the controlling principal authorization for this unit explicitly prohibits creating a new workstream, and the roadmap's pieces already have homes: `WS-0002` (status/report layer), `WS-0003` (daily-check UX), `WS-0007` (dashboard), `WS-0013` (final allocation). A fifth workstream would duplicate rather than connect them.

**Authorize Phase A or Phase B implementation now, since `OPS-0011` already covers adjacent ground.** Rejected — the controlling principal authorization for this unit is explicitly procedural and roadmap-bearing only; any implementation, however small, requires its own separate future authorization exactly as `OPS-0011`/`OPS-0012`/`OPS-0013` each required their own.

## Consequences

Going forward, a session working on Portfolio-HQ's application surface can cite this decision's phase map (§C) when scoping a future authorization request, and can cite §D/§E when deciding whether parallel work is safe or how to report work it discovers but isn't authorized to perform. `WS-0002`, `WS-0003`, `WS-0007`, and `WS-0013` each receive one additive cross-reference to this decision (see `operations/WORKSTREAMS.yaml`) recording how they relate to this roadmap, without any change to their status, priority, authorized_scope, prohibited_scope, or completion criteria. `OPS-0014` §D is restated by cross-reference, not edited. Commercialization stays explicitly deferred and non-blocking. **Nothing about this decision authorizes writing application code, beginning research, mapping relationships, interpreting charts, changing holdings/allocation/margin, placing or preparing brokerage orders, or creating a new workstream** — each remains gated behind its own separate future authorization exactly as before this filing.
