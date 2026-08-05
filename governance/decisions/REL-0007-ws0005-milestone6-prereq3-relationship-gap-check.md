---
decision_id: REL-0007
date: 2026-08-05
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, REL-0002, REL-0003, REL-0004, REL-0005, REL-0006, TIER-0001, TIER-0002, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0035, PI-0036, PI-0037, PI-0038, PI-0039, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: governance/audits/WS0005_M6PREREQ3_CLASSIFICATION_MATERIAL_RELATIONSHIP_GAP_CHECK_20260805.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one coherent Step 3 governance-and-gap-check PR:
determine whether any missing company relationship would materially affect future blind
classification across the current canonical equity roster, per `PI-0038`'s own pre-Milestone-6
roadmap's third prerequisite (`milestone6-prereq3-relationship-gap-check`). This is explicitly **not**
an authorization to build an exhaustive relationship graph. A relationship is material only if its
omission could materially change at least one `TIER-0002` classification axis (`economic_role`,
`capital_priority`, `risk_concentration`, `evidence_quality`). Existing governed evidence must be used
first; a missing relationship record may be implemented in this same PR only if it clears all four
bars the authorizing instruction states (material; clearly supported by existing governed evidence;
directionality/mechanism/confidence/uncertainty/provenance statable without new external research;
the smallest coherent correction to the graph). If no candidate clears all four bars, this unit is
required to preserve an explicit negative finding rather than invent work.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`1a91d8986652461584b4562bb4cd31b3c1b58bbd` — the exact SHA reported in the authorizing task,
independently re-derived rather than trusted. Working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no active mutation lane, and no
competing branch touches `intelligence/relationships/`, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, `CLAUDE.md`, `intelligence/companies/AMZN.yaml`, or
`test_portfolio_hq_dashboard_decisions.py`.

`PR #247` (`PI-0038`) and `PR #248` (`PI-0039`) both independently re-confirmed `merged: true` via the
GitHub API — not taken on faith from the authorizing task's own summary. `PI-0039`'s independent
review (`4863450699`), principal-acceptance comment (`issuecomment-5191738468`), and post-merge
verification comment (`issuecomment-5191791015`) were each independently re-read in full via the
GitHub API this session. Full detail, including the two accepted MINOR findings this filing resolves,
is retained in the supporting artifact's §0 and §6-§7.

`REL-0007` independently confirmed the next unused identifier: zero matches in
`governance/decisions.yaml`, zero matches via full-repository grep, zero matches via GitHub code
search. The highest filed `REL-####` is `REL-0006`. `governance/decisions/` and
`governance/decisions.yaml` independently reconciled 1:1 at 75 rows before this filing's own new row.

The canonical 27-name equity roster, the 6-name gate disposition, and the 13-record
`intelligence/relationships/` inventory were all independently re-derived from live files this
session — full detail, including a disclosed, non-blocking correction to `TIER-0001`/`TIER-0002`'s
own stated "13 of 27 unmeasured" figure (the correct three-mechanism count is 11, not 13 — `LLY` and
`TSLA` are both `issuer_lookthrough.yaml` members and were never actually unmeasured under
`TIER-0002` §3.5's own field definition), is retained in the supporting artifact §2.

Live validators and the full test suite were independently re-run against this exact base before any
edit: `relationship_validator.py` — `OK (13 record(s))`; `intelligence_validator.py` — 53/53 valid;
`freshness_validator.py` — OK; `portfolio_hq.dashboard.decisions.build_catalog('.')` — 75 decisions,
`issues == ()`; `pytest -q` — 2581 passed, 0 failed; `git diff --check` — clean.

No condition met a Stop bar. This unit proceeded.

## Decision

**`REL-0007` performs the classification-material relationship gap check `milestone6-prereq3`
requires, finds no candidate relationship clears the authorizing instruction's four-part bar for
implementation, and accordingly creates no new `intelligence/relationships/` record.** This decision
is a preserved negative finding, not an exhaustive relationship graph and not a Milestone 6
authorization of any kind. It additionally folds in two items of deferred `OPS-0009` Lane M factual
synchronization the `PI-0039` review explicitly deferred to "the next WS-0005 filing," per the
authorizing instruction's own explicit item 12.

### A. Gap-check performed

Full methodology, the recomputed three-mechanism `risk_concentration` coverage table for all 27
canonical names, every candidate relationship considered, and each candidate's disposition are
retained in full at
`governance/audits/WS0005_M6PREREQ3_CLASSIFICATION_MATERIAL_RELATIONSHIP_GAP_CHECK_20260805.md`
(§§1-5). Summarized here:

- **Eleven canonical names are genuinely unmeasured** under `TIER-0002` §3.5's own three-mechanism
  `unmeasured_flag` definition (cluster cap, issuer look-through, relationship record — not the
  two-mechanism count `TIER-0001`/`TIER-0002`'s own text states): `SNPS, PANW, ISRG, TMO, ICE, SPGI,
  V, COST, WM, RTX, RKLB`.
- **Two candidates were identified as genuinely material but not evidence-ready**: `SNPS↔NVDA`
  (a `technology_platform_dependency` claim in SNPS's own record, sourced entirely from
  weakly-disclosed WebSearch snippets and wholly uncorroborated by NVDA's own extensively-researched,
  primary-source-heavy record) and `RTX↔RKLB` (a joint government-program selection named only in
  RKLB's own record, with no clean fit to any of `REL-0001` §C's twelve primitives, and wholly absent
  from RTX's own directly-primary-source-derived record despite that record's detailed treatment of
  the same Raytheon defense segment). Both are disclosed as candidates for a possible future,
  separately authorized batch requiring new, targeted research — neither is implemented here.
- **Two previously-disclosed candidates from `REL-0006` Criterion 6 (`GEV`/`ETN`/`PWR`
  `capital_spending_dependency`; `MSFT`/`AMZN` `regulatory_or_reimbursement_dependency`) were
  re-evaluated against the `TIER-0002` axes specifically, not merely re-cited** — both are
  **DUPLICATIVE OF EXISTING STRUCTURE**: every named ticker in both candidates is already fully
  measured (cluster-cap and/or issuer-look-through and/or multiple existing relationship records), so
  implementing either would not change any `TIER-0002` axis for any of the five tickers involved. This
  confirms, rather than assumes, the authorizing instruction's own caution against treating a
  previously-mentioned candidate as material by default.
- **The five remaining genuinely-unmeasured, non-gated names** (`PANW, ISRG, TMO, V, COST`) were each
  freshly re-checked this session (direct record read plus a canonical-ticker-name grep across both
  `.yaml` and `.md`) — **zero canonical-pair relationship evidence exists for any of the five**, the
  same finding the original `REL-0001` inventory reached, independently reconfirmed unchanged by this
  session, not merely inherited.
- **The six `PI-0038` gated-name records** (`SNPS, ICE, SPGI, WM, RKLB, TSLA`) — evidence unavailable
  to any prior Milestone-4 filing — were each read in full this session specifically to check for a
  newly-disclosed relationship. Only `SNPS` (→NVDA) and `RKLB` (→RTX, mutually) surfaced a candidate;
  `ICE`, `SPGI`, `WM`, and `TSLA` name no canonical-roster counterparty anywhere in their own text.

**No candidate reached MATERIAL AND EVIDENCE-READY.** Per the authorizing instruction's own
efficiency standard, no new `intelligence/relationships/*.yaml` or `.md` record is created.

### B. Negative finding, preserved explicitly

This decision explicitly preserves, rather than discards, the finding that zero of the eleven
genuinely-unmeasured canonical names has governed evidence meeting `REL-0001` §E's "clearly supports"
bar for a new relationship record as of this filing's own live-state verification. This absence is
reported as an evidentiary gap, per `REL-0001` §E, never as proof no relationship exists, and does not
block Milestone 6 — matching `REL-0004`/`REL-0006`'s own precedent that new external relationship
research is not itself a prerequisite of a Milestone-4-scale completion standard, applied here with
equal force to this narrower gap check.

### C. `PI-0038`/`PI-0039` deferred factual synchronization (this filing's `OPS-0009` Lane M unit)

Per the authorizing instruction's explicit item 12, and per `PI-0039`'s own principal-acceptance
comment (`issuecomment-5191738468`) naming both items as deferred to "the next WS-0005 filing's own
factual synchronization":

1. `operations/WORKSTREAMS.yaml`'s `pi0038-gated-six-company-intelligence-completion` and
   `milestone6-prereq1-gated-six-intelligence-completion` gates are updated `status: in_progress` →
   `status: complete`, reflecting `PI-0038` (PR #247)'s independently re-confirmed merge — their own
   literal completion condition ("effective only on PI-0038's own merge") is satisfied.
2. `operations/WORKSTREAMS.yaml`'s `milestone6-prereq2-current-roster-freshness-verification` gate is
   updated `status: in_progress` → `status: complete`, reflecting `PI-0039` (PR #248)'s own
   post-merge-verification comment, which explicitly states the gate "is now effective as
   `status: complete`... deferred... to the next WS-0005 filing's own synchronization pass."
3. `operations/WORKSTREAMS.yaml`'s `milestone6-prereq3-relationship-gap-check` gate (this filing's own
   subject) is updated with this filing's description and `status: in_progress`, `pr: null` (a bounded
   follow-up commit sets `pr` once this PR's own number exists, per `OPS-0001`'s established
   convention) — **not** `status: complete`, since this filing's own governance PR is itself unmerged,
   unreviewed, and unaccepted as of this filing (the same discipline `TIER-0001`'s own independent
   review required after finding a premature `status: complete` on a still-open, self-referencing PR).

No other field of any of these three gates, and no other `WS-0005` field (`status`, `priority`,
`authorized_scope`, `prohibited_scope`, `completion_criteria`, or any other milestone's own gate), is
touched.

### D. AMZN bounded wording correction

Per the authorizing instruction's explicit item 12 and `PI-0039`'s own accepted MINOR finding,
`intelligence/companies/AMZN.yaml`'s competitive-advantages entry is corrected to state the ~$53B
Anthropic-related gain claim was reported across multiple outlets but is not primary-source-verified,
preserving the record's own underlying decision to exclude the figure as a one-time non-operating
item rather than because it is uncorroborated. No other AMZN content, `conviction.rating`, or any
other Company Intelligence record is touched.

### E. Non-authority

This decision does not authorize: any new `intelligence/relationships/` record; any external
relationship research; any price-correlation study; any graph or "Eureka" (`OPS-0016`)
implementation; any automatic scoring, ranking, or aggregation; any Milestone 6 population,
authorization, or classification of any kind; the `milestone6-prereq4` chart-evidence scope decision
(remains `pending_principal_decision`, undecided); any tier/target/role/cluster/cap/gate/ladder/
trim/sell/holdings/margin/allocator/brokerage/order change; or a new workstream. The
`milestone-6-blind-classification` gate's own `status: proposed`, "Not authorized to execute," is
unchanged.

### F. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `governance/audits/WS0005_M6PREREQ3_CLASSIFICATION_MATERIAL_RELATIONSHIP_GAP_CHECK_20260805.md`
(new, retained); (4) `operations/WORKSTREAMS.yaml` (`WS-0005` only — the three gate updates in §C,
plus the `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference
fields per `OPS-0001`'s existing convention); (5) `CLAUDE.md` (one concise Decisions Log pointer
entry); (6) `intelligence/companies/AMZN.yaml` (the one bounded wording correction in §D); (7)
`test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count assertions,
75→76, made stale by this filing's own new `governance/decisions.yaml` row). No
`intelligence/relationships/` file, no `relationship_validator.py` change, no other Company or Theme
Intelligence record, and no production allocator/margin code is touched.

### G. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review,
and receive explicit principal acceptance before it may be marked ready or merged. This session does
not review its own work, mark it ready, merge it, or post principal acceptance — each is a separate
future step requiring a separate actor. Nothing in this decision becomes effective until this
governance PR merges to `main`.

## Rationale

**Why the four-part implementation bar was applied strictly, producing a negative finding.** Both
identified candidates (`SNPS↔NVDA`, `RTX↔RKLB`) are real, disclosed evidence entries in already-read
Company Intelligence records, and both would resolve a genuinely unmeasured `risk_concentration` flag
— exactly the kind of material outcome the authorizing instruction asks this unit to find. But both
fail the "existing governed evidence clearly supports it" bar specifically: each rests on a single,
self-disclosed-as-weak, one-sided source, and in both cases the counterparty's own comparatively
well-sourced record is silent on a fact that record's own demonstrated depth on comparable topics
would otherwise be expected to surface. This is a materially different evidentiary posture than the
repository's own accepted one-sided-sourcing precedent (`REL-0002`'s `CEG_MSFT`), where the claim was
a specific, named, long-duration contract structure that is itself the entire relationship, not a
composite of an equity stake and an inferred technology dependency, or an unclear-mechanism joint
government-program mention. Treating a real but weakly-evidenced candidate as implementable would
convert this bounded gap check into unauthorized new research by another name.

**Why the two `REL-0006`-disclosed candidates were re-evaluated rather than simply re-cited as
optional.** The authorizing instruction explicitly warns against assuming either candidate is material
"merely because they were previously mentioned." This filing performed the actual axis-by-axis check
`REL-0006` itself did not perform (that filing disclosed both purely as residual, unevaluated items)
and found both genuinely duplicative of existing cluster-cap and issuer-look-through coverage for
`risk_concentration` specifically, with no effect on any other `TIER-0002` axis — a reasoned
disposition, not an assumption in either direction.

**Why the `TIER-0001`/`TIER-0002` 13-versus-11 discrepancy is disclosed rather than corrected in
place.** Per `governance/decisions/README.md`'s convention against silently rewriting a prior filing's
own retained text, and matching `REL-0006`'s own identical treatment of a stale `TIER-0001`-adjacent
figure (the GNRC staleness correction in `REL-0006` §A, Criterion 3), this filing records the
correction in its own text only. The correction is itself load-bearing for this gap check's own
population (§A), so it could not be omitted, but neither `TIER-0001` nor `TIER-0002`'s own file is
edited.

## Alternatives Considered

- **Implement `SNPS_NVDA` and/or `RTX_RKLB` anyway, using `evidence_classification: inferred` to flag
  the one-sided sourcing, matching the `CEG_MSFT` precedent.** Rejected — the authorizing instruction's
  own bar requires existing evidence to "clearly support" a candidate before implementation, and both
  candidates' evidentiary posture (self-disclosed weak sourcing, silent well-sourced counterparty
  record, and — for `RTX_RKLB` — no clean primitive-type fit at all) falls short of that bar in a way
  `CEG_MSFT`'s specific, named, contract-anchored claim did not. Disclosed instead as future candidates
  requiring targeted research.
- **Treat the "13 unmeasured" figure as settled and not recompute it.** Rejected — the authorizing
  instruction requires this unit to determine actual materiality against `TIER-0002`'s own axes, and
  `TIER-0002` §3.5 defines `unmeasured_flag` as a three-mechanism test; using the two-mechanism figure
  without checking `issuer_lookthrough.yaml` would have misstated which names are actually candidates
  for this gap check, incorrectly including `LLY` and `TSLA`.
- **Expand this unit into a broader relationship-content batch covering the two disclosed-as-material
  candidates once located.** Rejected — explicitly outside this unit's authorization ("not an
  authorization to build an exhaustive relationship graph"); any future batch requires its own
  separate, explicit principal authorization, matching every prior Milestone-4 batch's own precedent.
- **Set `milestone6-prereq3-relationship-gap-check`'s gate `status` to `complete` directly in this
  filing, matching `REL-0006`'s own treatment of the (pre-existing, bigger) `milestone-4` gate.**
  Considered and rejected in favor of the more conservative, more common WS-0005 pattern (`rel0002`
  through `rel0005`'s own self-referential gates, and `milestone6-prereq2`'s own treatment by
  `PI-0039`): a filing does not mark its own still-unmerged, unreviewed work `complete` — that
  transition is recorded by a later filing's own Lane M synchronization once independent review,
  correction if needed, principal acceptance, merge, and post-merge verification have actually
  occurred, exactly as this filing itself performs for `PI-0038`/`PI-0039`'s own gates.

## Consequences

**Authorized, effective only on this decision's merge:** the recorded negative finding that no
candidate relationship clears the four-part implementation bar as of this filing's own live-state
verification; the disclosed three-mechanism recomputation correcting `TIER-0001`/`TIER-0002`'s own
stated unmeasured-name count from 13 to 11; the two candidates (`SNPS↔NVDA`, `RTX↔RKLB`) disclosed as
requiring new, targeted research for any future consideration; the `pi0038-gated-six-company-
intelligence-completion`, `milestone6-prereq1-gated-six-intelligence-completion`, and `milestone6-
prereq2-current-roster-freshness-verification` gate updates to `status: complete`; the bounded AMZN
wording correction.

**Not authorized by this filing, now or ever without a further separate decision:** any new
`intelligence/relationships/*.yaml` or `.md` record; any external relationship research; any
price-correlation study of any kind; any graph or "Eureka" implementation; Milestone 6 (blind
classification) or any later WS-0005 milestone; the `milestone6-prereq4` chart-evidence scope
decision; and any tier/target/role/cluster/cap/holdings/margin/allocator/order-behavior change.

**Unchanged by this decision:** every existing `intelligence/relationships/` record, all 13 of them,
byte-for-byte; every existing Company/Theme Intelligence record except the one bounded `AMZN.yaml`
correction in §D; every existing comparison artifact; `issuer_lookthrough.yaml`; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution;
`WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; Milestones 1-4's own `status: complete` (unedited, not reopened); `TIER-0001`'s
and `TIER-0002`'s own accepted/proposed text and scope, in full, unedited; the retained
`WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` artifact, unedited.

This decision becomes effective only when its implementing pull request merges to `main`.
