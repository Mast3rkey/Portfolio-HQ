---
decision_id: REL-0002
date: 2026-08-04
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded implementation unit: the first
WS-0005 Milestone 4 relationship-content batch, limited to the single pair `CEG_MSFT`, implemented
as one combined governance-and-implementation pull request, following the planning package (the
`REL-0001`-governed inventory audit's own §9 advisory recommendation) exactly. The authorization is
explicit that this unit must: begin with full repository preflight; create only this decision file
and the single `CEG_MSFT` relationship record; use only repository evidence already identified (no
external research); explicitly disclose the one-sided sourcing on that pair; not infer unsupported
facts; not compute correlations; not modify any Company Intelligence record; and not modify
holdings, targets, tiers, caps, allocator, margin, charts, or "Eureka." Everything below is bounded
by that authorization.

### Preflight performed this session, independently verified, not assumed

The local checkout was found 581 commits behind `origin/main` at session start — fetched and
fast-forwarded to `origin/main`'s tip, `7cb22f0` (`WS-0005: post-PR #238 factual synchronization
(#239)`), working tree confirmed clean after resolving one trivial, stale, unpushed local edit to
`performance_log.csv` (a scratch re-run from an earlier, unsynced local session, superseded by
upstream's fuller and corrected history — resolved by keeping upstream's version in full, per this
repository's own "never silently overwrite unpushed state, but also never treat stale local scratch
data as authoritative over a synced upstream history" discipline).

`governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
was read in full: `status: Accepted`, effective. `governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
(the `REL-0001` §I inventory-only unit's own retained artifact, produced by PR #238, merged) was
read in full — its §9 table names `CEG_MSFT` as the smallest coherent first candidate: a
`customer_dependency` relationship (CEG's disclosed 20-year Microsoft PPA supporting the Crane Clean
Energy Center restart), evidence already fully present in `intelligence/companies/CEG.yaml`, no
MSFT-side confirmation located, no editing required to either existing Company Intelligence record,
and an explicit stopping condition: if MSFT-side confirmation cannot be found without new research,
carry `evidence_classification: inferred` and disclose the one-sided sourcing, never silently upgrade
to `observed`. This filing's implementation follows that stopping condition exactly — no new
research was performed, and `intelligence/companies/MSFT.yaml`/`MSFT.md` were directly grepped for
"Constellation"/"CEG"/"nuclear"/"power purchase"/"PPA" and confirmed to contain zero matches,
independently reconfirming the inventory's own finding rather than merely citing it.

`relationship_validator.py` and `test_relationship_validator.py` (both created by the already-merged
`REL-0001` §I inventory unit) were read in full to determine the exact schema this filing's record
must satisfy: closed twelve-item primitive taxonomy, directionality rules keyed to relationship type,
a nine-key evidence-entry standard, a closed `decision_served` vocabulary, a `review` block matching
the existing Company Intelligence freshness convention, alphabetical `<TICKER-A>_<TICKER-B>` filename
ordering, and a required Markdown companion. `intelligence/relationships/` was confirmed absent from
the repository before this unit's own work — no prior relationship record exists anywhere.

`governance/decisions.yaml` was independently reconciled against `governance/decisions/*.md` (less
`README.md`): 66 files, 66 index rows, 1:1, `REL-0001` the last-filed entry — confirming `REL-0002`
as the next unused identifier in this genuinely new-but-already-established series (per
`governance/decisions/README.md`'s own rule, `REL-0001`'s Rationale already established `REL-####` as
the correct domain for pairwise relationship-content governance; this filing continues that series
rather than minting a further new prefix, matching the `PI-0001`→`PI-0002` first-content-batch
precedent). `operations/WORKSTREAMS.yaml`'s WS-0005 entry was re-read: the
`milestone-4-portfolio-relationship-mapping` gate remains `status: proposed`; the
`rel0001-inventory-only-unit-active` gate confirms PR #238 merged and explicitly states "no further
[inventory] unit is authorized without its own separate, future, explicit principal decision" and
that "the next step after this unit completes is a separately authorized first relationship-content
batch... never automatic progression from this unit's own completion" — this filing is exactly that
separate, explicit authorization.

### Packaging: one combined PR, by explicit principal instruction

`REL-0001` §I describes future relationship-content batches as each requiring "its own separate
future authorization" and, for its own inventory-only unit, gates the future unit's *start* on the
authorizing decision's prior merge. This filing's task authorization explicitly directs a different,
narrower packaging for this specific batch: one combined governance-and-implementation pull request,
containing both this authorizing decision and the `CEG_MSFT` relationship record itself. This is a
packaging choice, not a control reduction — every substantive gate `REL-0001` §N and `OPS-0009`'s
Lane G (governance authorization, always full weight, never reduced — this filing creates new
authority, the first relationship-content batch, and is therefore Lane G in full regardless of what
else is bundled with it) require remains fully intact: this PR must remain in draft state, receive
its own independent exact-head review, complete any required bounded correction and exact-head
re-review, and receive explicit principal acceptance before it may be marked ready or merged. Nothing
in this filing or the `CEG_MSFT` record becomes effective until that full cycle completes and this PR
merges to `main`. This filing does not mark itself ready and does not authorize its own merge.

## Decision

**`REL-0002` authorizes, and — in the same pull request, per explicit principal packaging
instruction — implements, the first WS-0005 Milestone 4 relationship-content record:
`intelligence/relationships/CEG_MSFT.yaml` and `.md`, a single `customer_dependency` primitive record
(CEG depends on MSFT) under `REL-0001`'s frozen schema.** No other relationship pair, no Company or
Theme Intelligence edit, no correlation study, no score or ranking, and no policy change is authorized
or performed by this filing.

### A. What was created

Exactly two files: `intelligence/relationships/CEG_MSFT.yaml` and `intelligence/relationships/CEG_MSFT.md`.
The record classifies CEG's disclosed 20-year Microsoft PPA (supporting the planned restart of the
835 MW Crane Clean Energy Center) as a `customer_dependency` (CEG is the subject, MSFT the object,
`symmetric: false`, per `REL-0001` §D's directional-by-construction rule for this primitive type),
`relationship_status: current`, naming `thesis_monitoring` and `stress_testing` from `REL-0001` §F's
closed `decision_served` vocabulary — both taken directly from the inventory's own §9 recommendation
for this exact pair, not independently chosen by this filing.

### B. One-sided sourcing, disclosed explicitly

The sole evidence entry's `source` is `intelligence/companies/CEG.yaml`'s claim `CEG-C05` (itself
citing Constellation's 2025 Form 10-K, Item 1, page 14) — `inspected_source_type: secondary`, since
this unit did not itself open the 10-K, only CEG's own already-vetted Company Intelligence record.
`evidence_classification: inferred`, not `observed`, per the inventory's own stopping condition for
this pair — a deliberate epistemic-humility choice, not a claim that CEG's own disclosure is
unreliable. The `uncertainty` field and the `.md` companion's own "Source-access disclosure" section
both state, explicitly: this unit directly grepped `MSFT.yaml`/`MSFT.md` for any independent
mention of Constellation/CEG/the PPA and found none; no attempt was made to locate independent
MSFT-side confirmation through new research, since that would exceed this unit's authorized scope; no
contract-value or percent-of-revenue figure was located in the existing evidence base; and the Crane
restart itself is disclosed as subject to regulatory and execution conditions, not yet an operating
asset.

### C. What this filing does not do

No `intelligence/companies/CEG.yaml`, `CEG.md`, `MSFT.yaml`, or `MSFT.md` file was modified — both
were read only, for the purpose of sourcing and independently confirming the one-sided-sourcing
disclosure, never edited. No external research of any kind was performed. No price correlation was
computed, cited, or implied — the `CEG_MSFT.md` companion explicitly states none was computed, per
`REL-0001` §G's structural-versus-measured-correlation separation. No `duplicate_economic_exposure`,
`correlated_loss_mechanism`, or `missing_exposure` conclusion was asserted — `REL-0001` §C excludes
all three as primitive record types, and this record declares only `customer_dependency`. No
holdings, targets, tiers, caps, gates, clusters, ladders, trims, sells, margin, allocator, brokerage,
order, chart-evidence, or "Eureka" (`OPS-0016`) file or system was touched. The
`milestone-4-portfolio-relationship-mapping` gate's own `status: proposed` (`operations/WORKSTREAMS.yaml`)
is not itself flipped to `in_progress` or `complete` by this filing — one additive record is a first
step, not completion of Milestone 4, and no claim to the contrary is made anywhere in this filing.

### D. Test suite reconciliation, disclosed

Adding this repository's first real `intelligence/relationships/` record made two pre-existing tests'
literal assertions false on their face: `test_relationship_validator.py`'s
`test_universe_loaders_never_touch_intelligence_relationships` previously asserted the directory's
existence stayed `False` before and after calling the universe loaders (written when no relationship
record existed anywhere), and `test_validating_the_real_repository_relationships_dir_does_not_mutate_it`
previously asserted the directory did not exist at all. Both were narrowly corrected in this same
filing: the first now asserts before/after existence *matches* (the loaders still never create,
remove, or touch the directory — the guarantee is unchanged, only the now-true starting state is);
the second now asserts the directory exists, contains exactly the one `CEG_MSFT` record, validates
`True`, and that validating it never mutates its file contents (confirmed by exact before/after
byte-for-byte comparison of both files). No other test file's assertion was found to depend on
`intelligence/relationships/` remaining absent. Separately, `test_portfolio_hq_dashboard_decisions.py`
hardcodes the live decision count twice (`test_real_repository_catalog_builds_all_66_with_no_issues`
and `test_real_repository_model_and_render_succeed_end_to_end`) — both updated from 66 to 67 to match
`REL-0002`'s own addition to `governance/decisions.yaml`, the first test also renamed to
`..._all_67_...` to match this repository's own established per-addition renaming convention for that
test.

### E. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (WS-0005 only — one additive milestone-adjacent gate entry,
one `evidence_refs` pointer, and the `active_branch`/`active_pr`/`last_verified_main_sha`/
`last_verified_date` self-reference fields, per `OPS-0001`'s existing convention); (4) `CLAUDE.md`
(one concise Decisions Log pointer entry); (5) `intelligence/relationships/CEG_MSFT.yaml` and `.md`
(the authorized relationship record itself); (6) `test_relationship_validator.py` (the two
pre-existing test corrections in §D above); (7) `test_portfolio_hq_dashboard_decisions.py` (the two
hardcoded-count corrections in §D above). No Company or Theme Intelligence record, no comparison
artifact, no `issuer_lookthrough.yaml`, no `targets.yaml`/`holdings.yaml`/`gates.yaml`, no
`allocate.py`/`levels.py`/`margin_state.py`, no chart-evidence file, and no "Eureka" file is touched.

### F. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (Lane G, `OPS-0009` — full weight, never reduced by this filing's own
combined-PR packaging choice), complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This decision does not
mark itself ready and does not authorize its own merge. Nothing in §§A-E above, and no content of
`CEG_MSFT.yaml`/`.md`, becomes effective until this PR merges to `main`.

## Rationale

**Why `CEG_MSFT`, and why exactly one pair.** The inventory audit's own §9 table ranked `CEG_MSFT` as
the smallest coherent first candidate on four independent grounds: the evidence already exists in a
single already-vetted source (no new research plausibly required to *establish* the relationship,
only to strengthen it past one-sided sourcing); neither counterparty's existing Company Intelligence
record requires editing (purely additive); the relationship is, by the inventory's own comparative
assessment across every candidate considered, "the single best-documented canonical-pair relationship
found anywhere in this inventory"; and its `decision_served` values (`thesis_monitoring`,
`stress_testing`) are concrete and specific, not generic placeholders. Limiting this batch to exactly
one pair — rather than also drafting `AVGO_GOOGL`/`AVGO_META` or the `MSFT`/`GOOGL`/`AMZN`
`competitor` triad the same §9 table also names — matches this filing's own explicit, narrow
authorization scope and this repository's own repeated smallest-reversible-step discipline (`PI-0002`
through `PI-0009`'s incremental-pilot precedent, restated by `REL-0001`'s own Rationale for choosing
an inventory-only first step over content research).

**Why `evidence_classification: inferred`, not `observed`, despite a primary-source-grounded
underlying disclosure.** CEG's own 10-K disclosure of the PPA is, in isolation, a directly-stated
primary-source fact. But this filing's own evidentiary chain to that fact runs through CEG.yaml (a
repository-internal, already-vetted secondary compilation) rather than through this unit's own direct
inspection of the 10-K, and — more importantly — the relationship is confirmed from only one
counterparty's side. The inventory's own §9 stopping condition for this exact pair anticipated this
precise situation and specified the resolution: classify `inferred`, disclose the one-sided sourcing
explicitly, never silently upgrade to `observed` merely because the underlying source happens to be
primary-source-grounded on one side. This filing follows that stopping condition exactly, per its own
explicit task instruction to follow the planning package exactly.

**Why a combined governance-and-implementation PR, departing from `REL-0001`'s own "future, separate"
default.** `REL-0001` §I's own gating language governs its *own* inventory-only unit specifically; it
states that future relationship-content batches each require "their own separate future
authorization," but does not itself mandate that the authorization and the resulting content record
be filed as physically separate pull requests — this repository already has precedent for two
distinct decisions sharing one PR (`OPS-0008`+`PI-0027`, `REL-0001`+`OPS-0016`), and for a governance
decision's own PR carrying its own implementation artifact in narrower cases (e.g. `OPS-0004`'s
retained audit artifact). This filing's specific packaging — one decision plus its own directly
authorized content, in one PR — is a further, explicit principal instruction for this specific unit,
not a self-granted exception; every substantive control (independent review, principal acceptance,
merge gate, post-merge verification) remains fully intact and unweakened, per `OPS-0009` §11's hard
boundary that no lane or packaging choice may ever bypass a mandatory control.

## Alternatives Considered

- **Defer to `REL-0001`'s own two-step pattern (separate governance PR, then a later separate
  implementation PR).** Rejected for this specific unit per the task's own explicit, controlling
  packaging instruction — not rejected as a general principle; a future relationship-content batch
  authorized without that specific instruction should default back to the two-PR pattern absent a
  fresh, equally explicit combined-PR instruction.
- **Draft additional pairs from the inventory's §9 table in the same filing (`AVGO_GOOGL`,
  `AVGO_META`, the `MSFT`/`GOOGL`/`AMZN` `competitor` triad).** Rejected — this filing's own
  authorization names exactly `CEG_MSFT`; drafting additional pairs without their own explicit
  authorization would exceed this unit's bounded scope, the same discipline every prior WS-0005 batch
  (`PI-0023` through `PI-0030`) has applied to its own named ticker list.
- **Attempt new research to locate independent MSFT-side confirmation of the PPA, upgrading the
  evidence entry to `observed`.** Rejected per this filing's own explicit "no external research"
  boundary — the correct response to a one-sided-sourcing gap, under `REL-0001` §E's own abstention
  discipline, is disclosure (`inferred`, explicit `uncertainty` text), not unauthorized research to
  close it.
- **Leave the two now-false pre-existing test assertions unedited, on the theory that only the
  authorized file list should be touched.** Rejected — a test asserting a premise this filing's own
  authorized content directly falsifies is not "unrelated cleanup"; leaving it would break the
  existing, already-merged test suite for the domain this filing's own record belongs to, which
  `OPS-0009` §2 lists as a mandatory, non-removable control in every lane.

## Consequences

**Authorized and implemented, effective only on this decision's merge:** the `CEG_MSFT`
`customer_dependency` relationship record (`intelligence/relationships/CEG_MSFT.yaml`/`.md`), the
first content record under `REL-0001`'s frozen schema; the two corrected pre-existing tests in
`test_relationship_validator.py`; the two corrected decision-count assertions in
`test_portfolio_hq_dashboard_decisions.py`; one additive `operations/WORKSTREAMS.yaml` WS-0005 gate
entry recording this batch; one `governance/decisions.yaml` index row; one `CLAUDE.md` Decisions Log
pointer entry.

**Not authorized by this filing, now or ever without a further separate decision:** any other
relationship pair; any Company or Theme Intelligence record edit; any price-correlation study of any
kind; any `duplicate_economic_exposure`/`correlated_loss_mechanism`/`missing_exposure` conclusion; any
graph or "Eureka" implementation; any tier/target/holdings/cluster/cap/gate/ladder/trim/sell/margin/
allocator/brokerage/order change; Milestone 5 or any later WS-0005 milestone; and a new workstream.

**Unchanged by this decision:** every existing Company/Theme Intelligence record, including
`intelligence/companies/CEG.yaml`/`CEG.md` and `MSFT.yaml`/`MSFT.md`; every existing comparison
artifact; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`,
`levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s top-level `status`, `priority`,
`authorized_scope`, `prohibited_scope`, and `completion_criteria`; the
`milestone-4-portfolio-relationship-mapping` gate's own `status: proposed`; `REL-0001` itself,
unedited and not reopened.

This decision becomes effective only when its implementing pull request merges to `main`.
