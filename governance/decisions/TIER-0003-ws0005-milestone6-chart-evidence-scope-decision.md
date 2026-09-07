---
decision_id: TIER-0003
date: 2026-08-05
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, TIER-0001, TIER-0002, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PI-0038]
supporting_artifact: null
---

## Context

### Authority for this unit

`PI-0038`'s pre-Milestone-6 roadmap (`operations/WORKSTREAMS.yaml`, `WS-0005`) records six ordered
prerequisites that must resolve before a fresh Milestone 6 (blind classification) implementation may
be authorized. Prerequisite 4, `milestone6-prereq4-chart-evidence-scope-decision`, is explicitly a
**principal decision, not a research unit**: whether Milestone 6 blind classification is (A)
fundamentals/business-evidence only, with chart evidence remaining a separate downstream analytical
layer, or (B) a combined investment-state classification requiring governed chart evidence
(`CHART-0001`/`CHART-0002`) as an input. The gate was filed `pending_principal_decision`, no default
assumed. The human repository principal has now made that decision explicitly: **Option A.**

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`71dab2d218de5c4184d5f62bc29f0bc7b409c64f` — the exact SHA reported in the authorizing task,
independently re-derived rather than trusted. Working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no active mutation lane. `PR #249`
(`REL-0007`) independently re-confirmed `merged: true` via the GitHub API at head
`1662cb038006bc677ec8a741606e7b47f966c894`, matching the exact head named in the authorizing task.

`governance/decisions.yaml` and `portfolio_hq.dashboard.decisions.build_catalog('.')` both
independently re-derived: 76 decisions, `issues == ()`, before this filing's own new row. `TIER-0003`
independently confirmed the next unused identifier: zero `TIER-####` matches beyond the already-filed
`TIER-0001`/`TIER-0002`, confirming `TIER` is the correct, already-established governance prefix for
Milestone 5/6 classification-architecture decisions — no new prefix is minted. `relationship_validator.py`
— `OK (13 record(s))`, unaffected; `intelligence_validator.py` — 53/53 valid, unaffected;
`freshness_validator.py` — OK, unaffected.

No condition met a Stop bar. This unit proceeded.

## Decision

**The human repository principal decides Option A for pre-Milestone-6 roadmap Step 4: WS-0005
Milestone 6 blind classification will be fundamentals/business-evidence only.** This filing records
that decision, makes its scope boundary explicit and auditable, and synchronizes Step 3's completed
post-merge state. It does not authorize Milestone 6, classify any ticker, ingest or interpret any
chart, or mutate any portfolio-policy or execution behavior.

### A. Permitted Milestone 6 evidence

Future blind classification may use only:

- governed Company Intelligence (`intelligence/companies/*.yaml`/`.md`);
- business and financial evidence within those records;
- disclosed risks and catalysts within those records;
- governed `intelligence/relationships/*.yaml`/`.md` records (`REL-0001` taxonomy);
- cluster-cap (`targets.yaml` `caps.clusters`) and issuer-look-through (`issuer_lookthrough.yaml`)
  dependency and concentration evidence;
- each record's evidence-quality signal under `TIER-0002`'s `evidence_quality` axis design
  (`risks[].severity` plus the required per-ticker uncertainty statement).

### B. Excluded chart evidence

Chart evidence under `CHART-0001`, `CHART-0002`, or any later chart decision is excluded from every
`TIER-0002` axis during blind drafting. This boundary is stated as binding, not discretionary. The
Milestone 6 blind-drafting process must not read, receive, cite, infer from, or reference:

- raw chart images;
- chart filenames;
- chart manifests;
- chart coverage or inventory status;
- technical indicators;
- support or resistance levels;
- momentum or trend descriptions;
- technical interpretations;
- conclusions derived from current or historical price action;
- `CHART-0001` or `CHART-0002` evidence packages (`governance/evidence/CHART-0001/`,
  `governance/evidence/CHART-0002/`).

### C. TIER-0002 axis-by-axis effect

Recorded explicitly, per axis, so chart evidence cannot enter through an unstated gap:

- `economic_role`: no chart input.
- `capital_priority`: no chart input.
- `risk_concentration`: no chart input.
- `evidence_quality`: no chart input.

Chart evidence must not create an implicit fifth classification axis. `TIER-0002`'s own four-axis
design (`governance/decisions/TIER-0002-ws0005-milestone5-candidate-classification-framework-design.md`
§3) is unedited by this filing — this decision states how chart evidence relates to those four axes
(it does not), it does not add a fifth.

### D. Permitted downstream chart uses

After blind classification is sealed, chart evidence may remain separately governed and advisory for:
monitoring; technical-risk overlays; implementation sequencing; buy-ladder analysis (`LADDER-0001`);
sell-discipline analysis; entry and exit timing; later policy-recommendation context. Any such
downstream use must remain explicitly labeled as chart-derived and kept separate from the Milestone 6
classification record — never merged into it after the fact.

### E. Prohibited automatic effects

No chart evidence, under this decision or any future one absent its own separate governance decision,
may automatically change: targets; tiers; holdings; gates; caps; clusters; allocator logic; margin
policy; buy or sell orders; trades. This restates, and does not narrow or widen, `CHART-0001`
§6/`CHART-0002`'s own existing advisory-only boundary.

### F. Step 3 synchronization

`operations/WORKSTREAMS.yaml`'s `milestone6-prereq3-relationship-gap-check` gate is updated
`status: in_progress` → `status: complete`, `pr: null` → `pr: 249`, reflecting `REL-0007` (PR #249)'s
independently re-confirmed merge at head `1662cb038006bc677ec8a741606e7b47f966c894` — matching this
gate's own stated completion condition ("this gate reaches `status: complete` only on this filing's
own merge").

### G. Step 4 status, this filing

`operations/WORKSTREAMS.yaml`'s `milestone6-prereq4-chart-evidence-scope-decision` gate is updated
`status: pending_principal_decision` → `status: in_progress`, recording this filing's own branch and
(once it exists) PR number, and Option A as decided — **not** `status: complete`, since this filing's
own governance PR is itself unmerged, unreviewed, and unaccepted as of this filing, matching every
prior WS-0005 filing's identical discipline (`TIER-0001`, `milestone6-prereq2`, `milestone6-prereq3`
above). Step 4 reaches `status: complete` only on a later filing's own Lane M synchronization once
independent review, correction if needed, principal acceptance, merge, and post-merge verification
have actually occurred.

### H. Non-authority

This decision does not authorize: Milestone 6 itself; classification of any ticker; chart ingestion or
interpretation of any kind; any Step 5 (`milestone6-prereq5-population-reconciliation`) work; any Step
6 (`milestone6-prereq6-fresh-authorization-required`) work; any edit to `CHART-0001`, `CHART-0002`,
`TIER-0001`, or `TIER-0002`'s own text or scope; any new `intelligence/relationships/` record; any
Company or Theme Intelligence edit; any tier/target/holdings/gate/cap/cluster/allocator/margin/ladder/
trade change; or any brokerage action. The `milestone-6-blind-classification` gate's own
`status: proposed`, "Not authorized to execute," is unchanged.

### I. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — the `milestone6-prereq3` and
`milestone6-prereq4` gate updates in §F/§G, plus the `active_branch`/`active_pr`/
`last_verified_main_sha`/`last_verified_date` self-reference fields per `OPS-0001`'s existing
convention); (4) `CLAUDE.md` (one concise Decisions Log pointer entry); (5)
`test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count assertions, 76→77,
made stale by this filing's own new `governance/decisions.yaml` row). No chart file, no
`intelligence/` company/theme/relationship record, no `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`, and no production allocator/margin code is touched. No new audit artifact is
created — this decision's own text is the smallest coherent record of a principal scope decision, with
no separate research or inventory content to retain.

### J. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review,
and receive explicit principal acceptance before it may be marked ready or merged. This session does
not review its own work, mark it ready, merge it, or post principal acceptance — each is a separate
future step requiring a separate actor. Nothing in this decision becomes effective until this
governance PR merges to `main`.

## Rationale

**Why the exclusion list is stated as binding rather than discretionary.** The authorizing instruction
is explicit that this boundary must not be softened into a discretionary one. A future Milestone 6
implementation session, operating under time or evidence pressure, could otherwise treat "a quick look
at the chart" as a harmless cross-check — precisely the kind of quiet scope creep this repository's own
convention (`CHART-0001`/`CHART-0002`'s own advisory-only, no-automatic-effect boundaries; `REL-0001`'s
closed taxonomy) exists to prevent. Enumerating the excluded evidence types by name, rather than a
general "no charts" statement, closes the gap a vaguer instruction would leave open.

**Why the four-axis exclusion is stated per-axis rather than once, generally.** `TIER-0002` defines
four independent classification axes. A single blanket "charts are excluded" statement could still be
read as leaving room for a chart-derived signal to enter through one axis's own evidence-quality or
risk-concentration reasoning without being named. Stating "no chart input" against each of the four
axes individually removes that ambiguity and matches this filing's own instruction not to let chart
evidence "create an implicit fifth classification axis."

**Why permitted downstream uses are recorded here rather than left to `CHART-0001`/`CHART-0002` alone.**
Those two decisions already establish chart evidence as a separate, advisory, non-automatic layer in
general. This filing's contribution is narrower and specific to Milestone 6: confirming that sealing a
Milestone 6 classification record does not retroactively fold chart evidence into it, and that any
later chart-informed monitoring or sequencing use stays labeled as chart-derived, distinct from the
classification record itself.

**Why this filing does not mark Step 4 complete.** Matching every prior WS-0005 filing in this series
(`TIER-0001`'s own independent review found a premature `status: complete` on a still-open,
self-referencing PR to be a MAJOR defect; `REL-0007` applied the same discipline to Step 3), a filing
does not mark its own still-unmerged, unreviewed work complete. That transition is recorded by a later
filing's own Lane M synchronization once independent review, correction if needed, principal
acceptance, merge, and post-merge verification have actually occurred.

## Alternatives Considered

- **Option B (combined investment-state classification requiring governed chart evidence as an
  input).** This was the live alternative the `milestone6-prereq4` gate itself named. Not selected —
  the principal's explicit decision is Option A. Recorded here only to show the choice was real, not to
  argue against Option B's merits.
- **Leave the chart-evidence boundary as a general cross-reference to `CHART-0001`/`CHART-0002` without
  a Milestone-6-specific exclusion list or axis-by-axis statement.** Rejected — the authorizing
  instruction explicitly requires the boundary to be binding and auditable, not softened into
  discretion, and a bare cross-reference would leave the "does chart evidence touch any axis" question
  answerable only by inference from two decisions that were never written with Milestone 6's four-axis
  framework in mind (`CHART-0001` predates `TIER-0002` by four days; `CHART-0002` predates it by three).
- **Fold Step 5 (population reconciliation) into this same filing, since Step 4 is now decided.**
  Rejected — the authorizing instruction is explicit that this filing advances Step 4 only, and Step 5
  requires its own separate, later, explicit principal authorization and bounded implementation PR,
  matching every other ordered-roadmap step in this series.
- **Create a new retained `governance/audits/` artifact for this decision, matching `TIER-0001`/
  `TIER-0002`'s own pattern.** Rejected — those two decisions retained substantial original research
  and design content requiring a separate artifact; this decision records a single principal scope
  choice and its direct consequences, which fit entirely within the decision file itself. Creating a
  near-empty audit artifact would add a file without adding information.

## Consequences

**Authorized, effective only on this decision's merge:** the recorded principal decision that Milestone
6 blind classification is fundamentals/business-evidence only (Option A); the binding chart-evidence
exclusion list; the per-axis `TIER-0002` exclusion statement; the recorded permitted-downstream-use
list; the restated prohibited-automatic-effects list; the `milestone6-prereq3-relationship-gap-check`
gate transition to `status: complete`; the `milestone6-prereq4-chart-evidence-scope-decision` gate
transition to `status: in_progress` recording Option A and this filing's own branch/PR.

**Not authorized by this filing, now or ever without a further separate decision:** Milestone 6 itself;
classification of any ticker; any chart ingestion or interpretation; Step 5 (population reconciliation)
or Step 6 (fresh authorization) of the pre-Milestone-6 roadmap; any edit to `CHART-0001`, `CHART-0002`,
`TIER-0001`, or `TIER-0002`'s own text; any new `intelligence/relationships/` record or external
relationship research; any Company or Theme Intelligence edit; and any tier/target/holdings/gate/cap/
cluster/allocator/margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship Intelligence record,
byte-for-byte; `CHART-0001`'s and `CHART-0002`'s own accepted text and scope, in full, unedited;
`TIER-0001`'s and `TIER-0002`'s own text and scope, in full, unedited; `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the
Constitution; `WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; Milestones 1-4's own `status: complete` (unedited, not reopened); the
`milestone-6-blind-classification`, `milestone6-prereq5-population-reconciliation`, and
`milestone6-prereq6-fresh-authorization-required` gates' own `status: proposed`/`status: blocked`
(unedited, not reopened).

This decision becomes effective only when its implementing pull request merges to `main`.
