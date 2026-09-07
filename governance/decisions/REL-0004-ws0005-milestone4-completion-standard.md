---
decision_id: REL-0004
date: 2026-08-04
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, REL-0002, REL-0003, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded Lane G (`OPS-0009` §1) governance-
and-factual-synchronization filing to: (1) define the formal WS-0005 Milestone 4 completion
standard; (2) record the verified post-merge facts from PR #241 (`REL-0003`); (3) determine what
evidence would be required before Milestone 4 may later be declared complete; (4) create no new
relationship-content authorization; (5) make no Milestone 4 completion determination in this
filing. This unit performs no relationship research, creates no `intelligence/relationships/`
record, computes no correlation, edits no Company or Theme Intelligence record, and does not itself
determine Milestone 4 complete or incomplete.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`607832d07e2849051c74f4f83cf05627fce2fc8c`, working tree clean. **PR #241** (`REL-0003`, "second
WS-0005 Milestone 4 relationship-content batch — eight remaining evidence-ready pairs")
independently re-confirmed via the GitHub API: `state: MERGED`, `baseRefName: main`,
`headRefName: claude/rel0003-remaining-eight-relationships`, `mergeCommit.oid` identical to the
`origin/main` tip above, `mergedAt: 2026-08-04T16:31:28Z`. Its independent exact-head review
(`4856585060`, anchored to head `23b3b16c49a10bd4f5415e82a5e4e2a8a0fbc8db`, verdict CHANGES
REQUIRED — one MINOR finding on the competitor-triad sourcing disclosure) was followed by a bounded
correction commit (`fe81561`) and an exact-head delta review (`4856745242`, anchored to the
corrected head, verdict APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE — zero remaining BLOCKING,
MAJOR, or MINOR findings), a retained principal-acceptance comment naming exact head
`fe815617488c6223a472920c57cfe759095c1507` (`issuecomment-5181876227`), and merge at the SHA above.
Exact-head CI (`test` check run `30929553777`) confirmed `completed`/`success` at the merge commit.
**Zero open pull requests** (`gh pr list --state open` returns an empty list).

`relationship_validator.py` independently re-run this session: `OK (9 record(s))`. Nine
`intelligence/relationships/` pairs confirmed present: `AMZN_GOOGL`, `AMZN_MSFT`, `AVGO_GOOGL`,
`AVGO_META`, `CEG_MSFT`, `ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`, `GOOGL_MSFT` — `CEG_MSFT` from `REL-0002`
(PR #240), the remaining eight from `REL-0003` (PR #241). The full pytest suite independently
re-run this session against this exact base: **2581 passed, 0 failed** (139.77s). `governance/
decisions/` (68 `.md` files, excluding `README.md`) and `governance/decisions.yaml` (68 rows)
confirmed 1:1; `portfolio_hq.dashboard.decisions.build_catalog('.')` — 68 decisions, `legacy` 12,
`issues == ()`. **`REL-0004` independently confirmed the next unused identifier** in the already-
established `REL-####` series (`REL-0001`, `REL-0002`, `REL-0003` are the only existing entries;
`REL-0001` §"Decision-identifier determination" already established this prefix as a genuinely new,
non-`PI-####`, non-`OPS-####` domain — this filing continues that same series rather than minting a
further new prefix, since a Milestone 4 completion *standard* is the same relationship-mapping-
governance domain `REL-0001`/`REL-0002`/`REL-0003` already occupy, not a distinct one).

**`WS-0005`'s current live state, independently re-derived**, not assumed from any prior session's
own text: Milestone 3 remains `status: complete` (`PI-0037`, unedited, not reopened). Milestone 4
(`milestone-4-portfolio-relationship-mapping` gate) remains `status: proposed` — no accepted
decision anywhere in this repository has ever set it to `in_progress` or `complete`. `WS-0005`'s
top-level `status` remains `in_progress`, `priority` remains `primary`, the repository's sole
`priority: primary` workstream, both unchanged by this filing. `WS-0005`'s own `active_branch`/
`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields read
`claude/rel0003-remaining-eight-relationships` / `241` / `7305dc21bf6e7f30e62d75e70b82275ef3530d09`
/ `"2026-08-04"` at this filing's own start — stale on exactly the fact that `REL-0003`'s own PR has
since merged and `origin/main` has advanced past it, matching the mechanical staleness pattern this
repository has recorded and corrected after every prior WS-0005 filing's own merge (`PI-0035`,
`PI-0037`, `REL-0002`, `REL-0003` each left an identical stale self-reference for the next filing to
correct). This filing corrects exactly that fact (§K below) and performs no other `operations/
WORKSTREAMS.yaml` change.

**The `REL-0001` §I inventory audit's own §9 advisory-recommendation table is now fully actioned.**
Independently re-confirmed against the retained artifact
(`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`) and the nine filed
records: all four §9 candidate rows — `CEG_MSFT`; `AVGO_GOOGL`/`AVGO_META`;
`GNRC_GEV`/`GNRC_ETN`/`GNRC_PWR` (filed as `GEV_GNRC`/`ETN_GNRC`/`GNRC_PWR` per `REL-0001` §B's
alphabetical-filename rule); `MSFT_GOOGL`/`AMZN_GOOGL`/`AMZN_MSFT` (filed as `GOOGL_MSFT`/
`AMZN_GOOGL`/`AMZN_MSFT`) — are now filed, merged, and independently reviewed. **This exhausts the
one existing inventory's own recommended candidate set; it does not by itself establish that
Milestone 4 is complete, and this filing does not claim otherwise** — see §B below for why
candidate-set exhaustion is a necessary but insufficient completion signal under the standard this
filing defines.

## Decision

**`REL-0004` defines the WS-0005 Milestone 4 ("Portfolio Relationship Mapping") completion
standard: eight numbered, evidence-based, finite, auditable criteria (§C); a bounded reopening-
trigger model for coverage discovered after a future completion determination (§D); and an explicit
restatement of Milestone 4's boundaries against target/tier/allocator policy, measured price
correlation, chart evidence, Milestone 5, and "Eureka" (§E). This filing records the independently
re-verified post-merge facts of PR #241 (§ Preflight above) and performs the minimum `operations/
WORKSTREAMS.yaml` self-reference synchronization those facts require (§K). It creates no
relationship-content authorization, performs no research, and — repeatedly, explicitly — does not
itself determine Milestone 4 complete or incomplete. The `milestone-4-portfolio-relationship-
mapping` gate's own `status: proposed` is unchanged by this filing.**

### A. Why a completion standard is needed now, and why not yet a determination

`REL-0001` froze Milestone 4's schema, taxonomy, evidence standard, and one bounded inventory-only
unit, but never defined what "complete" means for this milestone — unlike Milestone 3, whose
completion standard `PI-0031` §K defined *before* any batch-count question became live. Two
relationship-content batches (`REL-0002`, `REL-0003`) have now filed and merged nine records,
exhausting the one existing inventory's own advisory candidate list (§9 of the retained audit). That
exhaustion is precisely the moment a completion standard is needed — without one, a future session
would face an ungoverned choice between declaring completion on record-count alone (arbitrary,
matching this filing's own explicit prohibition) or treating Milestone 4 as indefinitely open
(equally ungoverned, since no criterion would ever tell a future reader when to stop). This filing
resolves that gap the same way `PI-0031` §K resolved it for Milestone 3: by defining the standard
*before* the determination, so the determination itself (a future, separate filing) is a mechanical
evaluation against pre-committed criteria, not a fresh judgment call invented at determination time.

This filing does not perform that determination. Nine filed records, by themselves, satisfy none of
§C's eight criteria in full — criterion 1 requires a *fresh* re-verification that the governing
inventory's own coverage is current (not merely cited); criterion 4 requires each record's own
independent PROVISIONAL status to be freshly re-confirmed, not assumed from batch-level review
language; criterion 8 requires the determination to be its own separate, independently reviewed
filing. None of that work is performed here.

### B. Why candidate-set exhaustion is necessary but not sufficient

The `REL-0001` §I inventory (PR #238) was itself a **point-in-time** classification of evidence
already present in ten comparison artifacts, two Theme Intelligence records, and
`issuer_lookthrough.yaml`, as of `2026-08-04`. Its own §9 table explicitly recommended exactly four
candidate groupings (nine pairwise records) as the *first* coherent batch — it never claimed those
nine were the full universe of evidence-supported relationships, and its own §5/§6 sections
separately catalogued cross-batch gaps (§5.1's hyperscaler-to-semis chain, explicitly unresolved on
both sides) and canonical names with no located canonical-pair evidence at all (§6: `COST`, `V`,
`PANW`, `LLY`, `ISRG`/`TMO`, and, before `REL-0003`, `GNRC`/`RTX` — `GNRC`'s own entry is now stale,
since `REL-0003` filed three `GNRC`-anchored `complement` records the original audit's §6 table
predates). Treating "the one recommended batch is filed" as equivalent to "Milestone 4 is complete"
would silently drop: (a) the §6 list's own currency, now partly stale; (b) the §5.1 gap, which the
inventory itself flagged as the single highest-value, still-unresolved item; and (c) whether any
Company or Theme Intelligence record has been refreshed since `2026-08-04` in a way that surfaces
new evidence no inventory pass has yet classified. §C's criteria require a future determination to
re-check all of this against live state, not to reason from this filing's own point-in-time summary.

### C. WS-0005 Milestone 4 completion standard — eight criteria

A future completion-determination filing (§C.8) must evaluate all eight of the following together,
freshly re-verified against live repository and GitHub state at that filing's own preflight — not
inferred from this filing's summary, from any batch's own governance text, or from any prior
criterion's earlier evaluation.

**Criterion 1 — Full-roster inventory-pass currency.** Every canonical equity name that is not
actionable-gated and not individually deferred by accepted authority (per `gates.yaml` and the
dispositions `PI-0033`/`PI-0035` recorded, reconciled forward through any later roster change) has
been evaluated, at least once, by a systematic full-roster relationship-evidence inventory —
classifying existing evidence for that name against `REL-0001` §C's twelve frozen primitive types —
and that inventory's own coverage is confirmed **current**: either unchanged since its own
preflight, or its delta against live state (new canonical names, refreshed Company/Theme
Intelligence evidence, newly filed relationship records) is independently reconciled by the
determination filing itself. The existing `WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
artifact satisfies this criterion only for the 27-name roster and evidence base as it stood on
`2026-08-04`; a determination filed materially later must independently confirm no canonical-roster
or evidence-base drift has occurred, or must reconcile it, before relying on that artifact unchanged.

**Criterion 2 — Candidate-set exhaustion.** Every relationship candidate the governing inventory (or
any later authorized inventory refresh) identified as evidence-ready under `REL-0001` §E's standard
— i.e., recommended in an advisory table comparable to the existing audit's §9 — has either (a) a
filed, `relationship_validator.py`-passing `intelligence/relationships/` record, or (b) an explicit,
reasoned abstention or stopping-condition disclosure recorded in a retained artifact. No
evidence-ready candidate may be left silently unactioned. **Currently satisfied for the one existing
inventory's own §9 table** (all four candidate groupings, nine records, filed via `REL-0002`/
`REL-0003`) — a future determination must confirm this remains true and that no further candidate
table has since been produced and left unactioned.

**Criterion 3 — Explicit disposition for every canonical name.** Every canonical, non-gated,
non-deferred equity name carries a recorded disposition: covered by at least one filed relationship
record, **or** explicitly determined, in a retained inventory or audit artifact, to carry no
canonical-pair relationship evidence meeting `REL-0001` §E's materiality bar. A name with zero
evidenced canonical-pair relationships is a **valid, complete disposition**, not a gap — provided
the absence is itself disclosed (matching the existing audit's own §6 table) and not merely
unaddressed by silence. This criterion does **not** require every canonical name to appear in a
filed relationship record, and does **not** require exhaustive pairwise evaluation of all possible
name-pairs (up to 351 pairs across 27 names) — only that each name's own coverage question has been
asked and answered at least once, per Criterion 1.

**Criterion 4 — Per-record PROVISIONAL status.** Every `intelligence/relationships/` record existing
at determination time individually satisfies an `OPS-0007` §3-equivalent standard, applied **per
record**, not inferred from batch-level review language: eligible independent review at its exact
implementation head (`OPS-0007` §1), any required bounded correction and exact-head re-review,
explicit principal acceptance at that exact head, merge to `main`, and post-merge ancestry/
validator/test re-verification. This mirrors `PI-0037` Criterion 7's own per-record (not per-batch)
application of the same standard to Company Intelligence records. **`CEG_MSFT` and the eight
`REL-0003` records currently satisfy this standard** on the facts independently re-verified in this
filing's own Preflight — a future determination must independently re-confirm this remains true
rather than citing this filing's own statement of it.

**Criterion 5 — No unresolved MATERIAL finding.** No open BLOCKING or MAJOR finding (this
repository's existing severity vocabulary, per `OPS-0007` §1 and every prior WS-0005 review) remains
against any filed relationship record's evidence, sourcing, classification, taxonomy compliance, or
against the governing inventory artifact's own methodology. A MINOR finding or a disclosed NOTE does
not block this criterion, matching `PI-0031` §K.5's own precedent (CRM's/IBM's residual MINOR
findings and the universal 90-day-cadence NOTE did not block Milestone 3 completion).

**Criterion 6 — New-research gaps disclosed, not required.** Every relationship gap the governing
inventory (or its refresh) identified as requiring genuinely new external research beyond reuse of
already-existing evidence — for example, the existing audit's §5.1 hyperscaler-to-semis
capital/customer chain, which neither `Batch3` nor `Batch5` independently confirmed from the
counterparty side — is explicitly disclosed in the determination filing, together with an explicit
statement that it does not block completion. **New external relationship research is not itself a
prerequisite of this completion standard.** `REL-0001` authorized exactly one inventory-only unit,
already executed; it did not establish a research-wave protocol for relationship content analogous
to `OPS-0008`'s Milestone-3 batches, and this filing does not create one. This mirrors Milestone 3's
own precedent directly: `PI-0031` §K's completion criteria never required researching every
conceivable company — `DHR`, `SYK`, `EQIX`, and `UNH` remained explicitly deferred, with named
reopening triggers, and did not block Milestone 3's own completion determination (`PI-0037`). A
future principal may separately authorize new external relationship research through its own
bounded charter at any time (before or after a Milestone 4 completion determination) — such a
charter is optional, not required, and is not created, sketched, or shortcut by this filing.

**Criterion 7 — Register and validator synchronization.** The `intelligence/relationships/`
directory's contents, `relationship_validator.py`'s clean pass, `governance/decisions.yaml`, and
`operations/WORKSTREAMS.yaml`'s `WS-0005` entry are mutually consistent and current as of the
determination filing's own live-state re-verification — matching `PI-0031` §K.6's identical
requirement for Company Intelligence.

**Criterion 8 — Independent completion-determination filing.** A dedicated, later, separate Lane G
(`OPS-0009` §1) filing — itself performing no new relationship research, no new relationship record,
and no correlation study — freshly re-verifies Criteria 1 through 7 together against live
repository and GitHub state, states an explicit verdict, and is itself subject to the full
independent-review, correction-if-needed, exact-head re-review, principal-acceptance, merge, and
post-merge-verification lifecycle **before** the `milestone-4-portfolio-relationship-mapping` gate's
`status` may be set to `complete` in `operations/WORKSTREAMS.yaml`. This filing does not perform, and
is not, that determination.

### D. Reopening-trigger model (applies only after a future completion determination)

No accepted repository decision has ever reopened a milestone gate already set `complete` — this is
a designed model for a scenario that has not yet occurred (Milestone 3's own `status: complete` has
never been revisited; `PI-0036`'s GNRC/RTX coverage completed *before* `PI-0037`'s own determination,
not after it), stated explicitly as a forward design choice, not as an application of existing
precedent. The model is built from the closest available repository analogues: `gates.yaml`'s
per-name `next_gate` reopening conditions, and `PI-0033`'s/`PI-0035`'s own per-name reopening-trigger
convention.

Once a future filing determines Milestone 4 complete under §C, the following events are **named
reopening triggers** — each creates a bounded, disclosed coverage gap and its own future, separately
authorized filing requirement, but **none automatically flips the `milestone-4-portfolio-
relationship-mapping` gate's `status` back to `in_progress` or `proposed`** without its own explicit,
later, separate governance act:

1. **A new name is added to the canonical `destination:` roster.** The new name's relationship-
   evidence status is undetermined by default; it is disclosed as a bounded, named coverage gap in
   the next `operations/WORKSTREAMS.yaml` synchronization touching `WS-0005`, and closing it requires
   its own narrow future `REL-####` roster-reconciliation filing — matching `PI-0035`'s own role for
   Milestone 3 after `PHQ-2026-02`'s tier retirement, not a full Milestone 4 redo.
2. **A previously gated name clears its `gates.yaml` `next_gate` condition** and gains Company
   Intelligence coverage. Same treatment as trigger 1 — a bounded, disclosed gap, not a reopening.
3. **A covered canonical name's Company Intelligence record is materially refreshed** (via its own
   separate `PI-####` refresh authorization) in a way that surfaces a relationship claim no existing
   inventory pass classified. Disclosed as discovered work; requires its own bounded future inventory
   refresh or content-batch authorization to close; does not itself reopen the gate.
4. **A MATERIAL finding (Criterion 5) is identified against an already-filed, already-PROVISIONAL
   relationship record after completion.** Requires a bounded Lane C correction filing for that
   specific record; does not require re-evaluating every other record or the milestone as a whole.

In every case, the gap is disclosed and bounded, and closing it requires a narrow, separately
authorized future filing analogous in scope to the trigger itself — never an automatic, unbounded
reopening of the entire milestone, and never silent inaction either. This is the mechanism by which
future holdings and future Intelligence evidence are accounted for without making Milestone 4
permanently open-ended: a future completion determination is explicitly scoped to the canonical
roster and evidence base **as of its own live-state re-verification** (a snapshot, exactly as
`PI-0037` pinned Milestone 3's own 27-name roster at its own preflight) — evidence arriving after
that snapshot does not retroactively invalidate the determination; it creates a disclosed, bounded,
separately-authorized future increment.

### E. Non-authority and boundaries

This standard, and any future determination made under it, creates and will create:

- **No target, tier, gate, cluster, cap, holdings, margin, allocator, brokerage, or order authority
  of any kind.** Relationship records remain strictly advisory, per `REL-0001` §A/§L, restated here
  without narrowing or widening: a filed record or a completion determination never itself triggers,
  recommends, or implies a buy, trim, sell, gate reopening, or margin-related decision.
- **No price-correlation study or authorization of one.** `REL-0001` §G's structural-versus-measured
  separation is preserved unmodified — a Milestone 4 completion determination never requires,
  performs, or substitutes for a price-correlation study; any future such study remains its own
  separate `MARGIN-0005`/`LADDER-0001`-style pre-registered charter, not sketched or shortcut here.
- **No chart-evidence coupling.** `CHART-0001`/`CHART-0002`'s chart-evidence framework is a wholly
  separate evidence type and governance track; it is never conflated with, substituted for, or
  required by relationship-record evidence or this completion standard.
- **No Milestone 5 authorization, in any form.** A future Milestone 4 completion determination made
  under §C does not itself begin, schedule, or imply Milestone 5 (zero-based classification and tier-
  architecture review) or any later WS-0005 milestone — `OPS-0006` §5's own per-milestone
  authorization gate is unaffected and controls independently, exactly as `PI-0037` established for
  the Milestone-3-to-Milestone-4 boundary.
- **No "Eureka" (`OPS-0016`) implementation, application, graph rendering, or UI of any kind.**

### F. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — one additive gate entry recording PR #241's
independently re-verified post-merge state as a Lane M synchronization folded into this Lane G
filing per `OPS-0008` §4(a)'s convention; one additive gate entry recording this filing's own live
work; the `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference
fields); (4) `CLAUDE.md` (one concise Decisions Log pointer entry); (5)
`test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count assertions,
68→69, and the one test function name encoding that count — mechanical hygiene, matching
`REL-0002`'s and `REL-0003`'s own identical precedent, made necessary by this filing's own addition
of the 69th `governance/decisions.yaml` row). No production code beyond that one mechanical test
correction, no `intelligence/relationships/` file, no `relationship_validator.py` change, no
`governance/audits/` artifact, no other workstream, and no existing Company/Theme Intelligence
record is touched.

### G. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (`OPS-0009` Lane G — a new governance authorization, full weight,
never reduced), complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This decision does not mark
itself ready and does not authorize its own merge. Nothing in §§A-F above becomes effective, and no
completion-standard criterion in §C may be relied upon by any future filing, until this PR merges to
`main`.

## Rationale

**Why a bounded combination of criteria, not a single test.** The task authorizing this filing
explicitly warned against three failure modes: a standard satisfiable by record count alone, a
standard requiring exhaustive pairwise mapping of every possible holding combination, and a standard
that can never practically be satisfied. A single criterion cannot avoid all three simultaneously —
record count alone fails the first; requiring every one of up to 351 possible pairs to carry
evidence fails the second (and is not justified by anything in `REL-0001`, which explicitly
contemplates abstention as a valid outcome); requiring exhaustive new external research before
completion fails the third, since no research-wave protocol for relationship content currently
exists. Eight criteria addressing coverage currency, candidate exhaustion, per-name disposition,
per-record review lifecycle, finding resolution, disclosed-not-required new-research gaps,
synchronization, and a separate determination filing together bound the standard without falling
into any of the three warned-against failure modes.

**Why per-record PROVISIONAL status (Criterion 4), not batch-level citation.** `PI-0037` Criterion 7
already established, for Company Intelligence, that a batch's own governance text describing a
review as complete is not itself sufficient — GNRC and RTX required independent, fresh
re-verification via direct GitHub API query rather than trusting `PI-0036`'s own pre-implementation
governance text. The same discipline is applied here: a future Milestone 4 determination must
independently re-confirm each of the nine (or more, by then) records' own review/merge/post-merge
lifecycle, not accept `REL-0002`'s or `REL-0003`'s own narrative as proof.

**Why new external research is disclosed as a gap but not required (Criterion 6).** Requiring it
would import an unauthorized dependency: `REL-0001` authorized exactly one inventory-only unit,
already executed, and no Milestone-4-equivalent of `OPS-0008`'s Research Wave Protocol exists to
govern new relationship-content research at scale. Inventing that requirement here — inside a
completion-*standard* filing — would exceed this filing's own bounded Lane G authorization (define
the standard, do not create new research authority) and would risk making Milestone 4 practically
unsatisfiable pending a charter this filing has no authorization to write. Milestone 3's own
completion precedent (`PI-0031` §K, closed by `PI-0037`) directly supports treating disclosed,
reasoned deferral as compatible with milestone completion: `DHR`, `SYK`, `EQIX`, and `UNH` remained
uncovered, explicitly deferred, and did not block Milestone 3's `MILESTONE 3 COMPLETE` verdict.

**Why the reopening-trigger model is disclosed as a forward design, not cited as existing
precedent.** No repository decision has ever actually reopened a completed milestone gate — stating
this design as if it already had precedent would misrepresent repository history. The model instead
draws on the closest genuine analogues already in force (`gates.yaml`'s per-name `next_gate`
triggers; `PI-0033`'s and `PI-0035`'s per-name reopening-trigger convention for individual company
dispositions) and applies their same shape — a named, bounded, disclosed trigger requiring its own
separate future authorization, never automatic or silent — to the milestone-gate level for the first
time in this repository's history.

## Alternatives Considered

- **Declare Milestone 4 complete in this same filing, since the one existing inventory's advisory
  candidate set is now exhausted.** Rejected — explicitly outside this unit's authorization (task
  item 5), and substantively wrong on the merits per §B above: candidate-set exhaustion is one of
  eight necessary conditions, not a sufficient one: the governing inventory's own currency, per-name
  disposition completeness, per-record review-lifecycle status, and MATERIAL-finding-freedom are all
  independently required and none was freshly re-verified as part of a completion evaluation by this
  filing.
- **Require exhaustive pairwise coverage of every possible canonical-name combination (up to 351
  pairs across 27 names) before Milestone 4 may be considered complete.** Rejected — nothing in
  `REL-0001` requires this; §E's own evidence standard explicitly permits and expects abstention
  where no material relationship exists, and the existing inventory's own §6 table already
  demonstrates that several canonical names (`COST`, `V`, `PANW`, `LLY`, `ISRG`/`TMO`) have no
  located canonical-pair evidence at all — a valid, disclosed terminal state, not a gap requiring
  forced coverage. Requiring exhaustive pairwise mapping would also make completion practically
  unreachable without a scale of new external research this repository has never authorized for this
  domain, directly the failure mode the authorizing task warned against.
- **Set a fixed target record count (e.g., "Milestone 4 is complete once N relationship records
  exist") as the primary completion signal.** Rejected — a fixed count is arbitrary relative to the
  actual, uneven distribution of evidence across the roster (some names have several evidenced
  relationships, several have none) and was explicitly warned against by the authorizing task. Record
  count appears in this standard only indirectly, as a byproduct of Criteria 2-3, never as a target.
- **Require a new, formally authorized Research Wave Protocol for relationship content (an
  `OPS-0008`-equivalent) as a prerequisite of this completion standard, so that gaps like §5.1 could
  eventually be closed through new research before completion.** Rejected as a prerequisite (though
  left explicitly available as a future optional path, Criterion 6) — authorizing or requiring such a
  protocol exceeds this filing's own bounded scope (define a completion standard, not create new
  research authority) and would make completion contingent on a future charter this filing cannot
  itself write or guarantee will exist.
- **Leave Milestone 4 permanently open-ended, with no completion standard at all, given the absence
  of an established Milestone-4-specific research-wave protocol.** Rejected per the authorizing
  task's explicit instruction to define finite, auditable criteria and avoid an unsatisfiable
  standard — an absent standard is functionally identical to an unsatisfiable one, since no future
  session would have any criteria against which to evaluate completion.
- **Fold this filing's own definition and a completion determination into one PR, since the
  candidate set is already exhausted and the facts are fresh.** Rejected per the authorizing task's
  explicit item 5 ("make no Milestone 4 completion determination in this PR") and per this
  repository's own established practice of separating a completion *standard* from a completion
  *determination* (`PI-0031` §K vs. `PI-0037`) — collapsing the two here would repeat, for Milestone
  4, exactly the "assume batch-level language proves completion" failure mode `PI-0037`'s own
  Rationale explicitly warned against for Milestone 3.

## Consequences

**Authorized, effective only on this decision's merge:** the eight-criterion WS-0005 Milestone 4
completion standard (§C); the reopening-trigger model for a future completion determination (§D);
the explicit non-authority/boundary restatement (§E); and the minimum `operations/WORKSTREAMS.yaml`
self-reference and post-merge-fact synchronization this filing performs (§F, §K).

**Not authorized by this filing, now or ever without a further separate decision:** any
`intelligence/relationships/*.yaml` or `.md` record; any external relationship research; any
price-correlation study of any kind; any graph or "Eureka" implementation; any automatic scoring,
ranking, or aggregation; any target/tier/cap/cluster/gate/ladder/trim/sell/holdings/margin/
allocator/brokerage/order change; Milestone 5 or any later WS-0005 milestone; a new workstream; and
— stated repeatedly for clarity — **any determination, of any kind, that Milestone 4 is or is not
complete.**

**Unchanged by this decision:** every existing `intelligence/relationships/` record, all nine of
them, byte-for-byte; every existing Company/Theme Intelligence record; every existing comparison
artifact; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`,
`levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s top-level `status`, `priority`,
`authorized_scope`, `prohibited_scope`, and `completion_criteria`; the `milestone-4-portfolio-
relationship-mapping` gate's own `status: proposed`; Milestone 3's own `status: complete`
(`PI-0037`, unedited, not reopened); `REL-0001`'s, `REL-0002`'s, and `REL-0003`'s own accepted text
and scope, in full, unedited.

This decision becomes effective only when its implementing pull request merges to `main`.

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
  effective — including the `operations/WORKSTREAMS.yaml` synchronization in §K — only on this
  governance PR's own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized
  scope ends at opening this draft PR and one bounded follow-up commit setting `WS-0005`'s
  `active_pr` self-reference to this PR's own number once it exists, and reporting its exact head. No
  independent review, no correction pass, no re-review, no merge, no post-merge verification, and no
  Milestone 4 completion determination is performed by this session — each is a separate future step
  requiring a separate actor.

**No current portfolio policy, allocator behavior, or Milestone 4 completion status changes as a
result of this decision, before or after its merge.** `allocate.py`'s buy/trim/gap logic, every gate
parameter, every cap, every target weight, and every margin parameter remain exactly as
`targets.yaml`/`gates.yaml`/`holdings.yaml` currently state them, unaffected by this filing under any
circumstance. The `milestone-4-portfolio-relationship-mapping` gate's `status` remains `proposed`
before and after this filing's own merge — only a future, separate, independently reviewed
completion-determination filing (§C.8) may change it.
