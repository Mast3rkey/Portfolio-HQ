---
decision_id: REL-0005
date: 2026-08-04
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, REL-0002, REL-0003, REL-0004, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0033, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md
---

## Context

### Authority for this unit

The human repository principal authorized one bounded implementation unit: a third WS-0005
Milestone 4 relationship-content batch, limited to the semiconductor manufacturing/capital-
spending-dependency relationships the `REL-0001` §I inventory audit's own §4.1/§4.2 tables
already classified against TSM — originally `NVDA_TSM`, `ASML_TSM`, and `KLAC_TSM`, later
explicitly expanded by the principal, in the same authorization thread, to a fourth pair,
`AVGO_TSM`, conditioned on this session independently re-verifying that existing accepted
repository evidence supports it under the same `REL-0001` §E standard the other three meet
before proceeding — which this session did (see "Fourth-pair verification" below) before
drafting `AVGO_TSM.yaml`/`.md`. The authorization is explicit that this unit must: verify all
repository and GitHub facts independently before use; use only repository evidence already
identified (no external research); explicitly disclose one-sided or incomplete sourcing per
pair; not infer unsupported financial magnitude, bilateral confirmation, causality, correlation,
ranking, or policy implications; abstain on any pair whose evidence does not clear `REL-0001`;
not modify any existing Company or Theme Intelligence record; not add a fifth pair; and not touch
holdings, targets, tiers, caps, clusters, gates, allocator, margin, brokerage, orders, charts,
ladders, trims, sells, Milestone 5, or "Eureka." Everything below is bounded by that authorization.

### Preflight performed this session, independently verified, not assumed

`origin` fetched and pruned in an isolated worktree, kept physically and branch-separate from a
concurrent session's own active mutation lane (`claude/rel0004-milestone4-completion-standard`,
PR #242) throughout this unit's work — no file in that other branch/worktree was read, edited, or
otherwise touched by this unit at any point. Local branch fast-forwarded cleanly from `607832d`
(the `origin/main` tip at this unit's own start) to `29761b6a12bb81e3fff7c199f5ea4de57f3d32a5`
once PR #242 was independently confirmed `MERGED` via the GitHub API (`gh pr view 242`: merge
commit `29761b6a12bb81e3fff7c199f5ea4de57f3d32a5`, merged 2026-08-04T17:46:30Z). `gh pr list
--state open` confirms no other open pull request overlaps `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, `CLAUDE.md`, `intelligence/relationships/`,
`relationship_validator.py`, `test_relationship_validator.py`, or
`test_portfolio_hq_dashboard_decisions.py` at this unit's own preflight.

`REL-0001` through `REL-0004` were all re-read (`REL-0004`, PR #242, having just merged as "WS-0005
Milestone 4 completion standard" plus its own bounded `supporting_artifact` correction). `REL-0001`:
`status: Accepted`, effective — freezes the schema/taxonomy/evidence standard this unit's four
records must satisfy, and authorizes future relationship-content batches only through their own
separate, explicit authorization (§I/§L), never automatic progression. `REL-0002`/`REL-0003`:
frontmatter `status: Proposed` in both the decision files and `governance/decisions.yaml` — a
known, disclosed, pre-existing state (the `CHART-0001`/`CHART-0002` two-step acceptance-recording
pattern, already noted by `REL-0003`'s own preflight), not a defect this filing corrects. `REL-0004`
occupies the decision identifier this unit's own three original draft records had internally
self-referenced before PR #242 merged — corrected in this same filing (see "Identifier-collision
correction" below), not left stale.

`governance/decisions.yaml` independently reconciled against `governance/decisions/*.md` (less
`README.md`) at this unit's post-fast-forward preflight: 69 files, 69 index rows, 1:1, `REL-0004`
the last-filed entry — confirming `REL-0005` as the next unused identifier, independently
re-verified immediately before use per this unit's own authorization, not assumed from an earlier
turn in this conversation. `intelligence/relationships/` was confirmed to contain exactly nine
records (`CEG_MSFT`, `AVGO_GOOGL`, `AVGO_META`, `ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`, `GOOGL_MSFT`,
`AMZN_MSFT`, `AMZN_GOOGL`) before this unit's own four additions.

### Identifier-collision correction

This unit's three original draft records (`NVDA_TSM`, `ASML_TSM`, `KLAC_TSM`) were first drafted,
in an earlier phase of this same session, under a working self-reference to
`governance/decisions/REL-0004-ws0005-milestone4-third-relationship-content-batch-semis-tsm.md` —
at that time the correct next-available identifier. A concurrent session's own, separately
authorized "WS-0005 Milestone 4 completion standard" filing then claimed `REL-0004` and merged
(PR #242) before this unit's own filing. Per this unit's own explicit authorization ("update only
the obsolete internal REL-0004 self-references that now conflict with the merged completion-standard
decision"), all six pre-existing files' internal self-references were mechanically corrected from
`REL-0004` to `REL-0005` — filename, decision-ID prose, and cross-reference text — with no change
to any pair's identity, evidence, classification, claim, or scope. `AVGO_TSM.yaml`/`.md` were
authored directly under the corrected `REL-0005` identifier and never carried the stale reference.

### Fourth-pair verification (`AVGO_TSM`)

Per the principal's explicit conditional authorization, this session independently re-verified
`AVGO_TSM` against `REL-0001` §E's evidence/abstention standard before accepting it into this
batch, using only evidence already present in the repository: `intelligence/companies/AVGO.yaml`
carries a risk entry dedicated specifically to this dependency, "Foundry and advanced-packaging
dependency" — "Broadcom's semiconductor products (both merchant chips and custom AI silicon) rely
on external foundry and advanced-packaging capacity -- industry-wide reporting places TSMC as the
dominant advanced-node/advanced-packaging supplier to the AI-accelerator industry broadly" — a
company-specific, TSMC-naming risk-factor entry, if anything more directly on-point than NVDA's
own more generic "foundry partners and contract manufacturers" language. This session directly
grepped `intelligence/companies/TSM.yaml` and `intelligence/companies/TSM.md` for "AVGO"/"Broadcom"
and found zero matches, confirming the same one-sided-sourcing pattern the other three pairs
already carry. The `REL-0001` §I inventory audit's own §4.1 table independently corroborates this
exact pairing: "AVGO → TSM | Same structural inference as above, extended explicitly to AVGO by
Batch3 §5... | inferred | current." `AVGO_TSM` therefore clears `REL-0001` §E at the same `inferred`
classification as `NVDA_TSM`, and is accepted into this batch. No pair considered for this batch
required abstention (see §E below).

## Decision

**`REL-0005` authorizes, and — in the same pull request, following `REL-0002`'s and `REL-0003`'s
own combined-PR packaging precedent — implements, the third WS-0005 Milestone 4 relationship-
content batch: four `intelligence/relationships/` records, all sharing TSM as the common
counterparty, covering two `manufacturing_dependency` records (`AVGO_TSM`, `NVDA_TSM`) and two
`capital_spending_dependency` records (`ASML_TSM`, `KLAC_TSM`) — all under `REL-0001`'s frozen
schema, all reusing only evidence already present in the repository at this unit's own preflight.
No other relationship pair, no Company or Theme Intelligence edit, no correlation study, no score
or ranking, and no policy change is authorized or performed by this filing.**

### A. What was created

Exactly eight files: `ASML_TSM.yaml`/`.md`, `AVGO_TSM.yaml`/`.md`, `KLAC_TSM.yaml`/`.md`, and
`NVDA_TSM.yaml`/`.md`, all under `intelligence/relationships/`.

| Pair | `relationship_type` | Directionality | `decision_served` | `evidence_classification` | `confidence` |
|---|---|---|---|---|---|
| `ASML_TSM` | `capital_spending_dependency` | directional, ASML subject / TSM object | `duplicate_exposure_detection`, `thesis_monitoring` | `inferred` | moderate |
| `AVGO_TSM` | `manufacturing_dependency` | directional, AVGO subject / TSM object | `duplicate_exposure_detection`, `stress_testing` | `inferred` | moderate |
| `KLAC_TSM` | `capital_spending_dependency` | directional, KLAC subject / TSM object | `duplicate_exposure_detection`, `thesis_monitoring` | `inferred` | **low** |
| `NVDA_TSM` | `manufacturing_dependency` | directional, NVDA subject / TSM object | `duplicate_exposure_detection`, `stress_testing` | `inferred` | moderate |

`KLAC_TSM` is deliberately recorded at `confidence: low`, not `moderate` — KLAC's own record labels
its only TSM-specific figure (~23% of FY2023 revenue) "secondary, single data point, not tracked
across other years," a materially weaker evidentiary tier than ASML's own more current, more
emphasized ~24%-of-net-sales figure. This distinction is preserved explicitly, not smoothed into a
uniform confidence rating across the batch.

### B. One-sided and single-source sourcing, disclosed per pair

- **`NVDA_TSM`**: disclosed from neither side. This session directly grepped `TSM.yaml`/`TSM.md`
  for "NVDA"/"NVIDIA" and found zero matches; NVDA's own Q1 FY2027 Form 10-Q risk-factor language
  discusses "foundry partners and contract manufacturers" generically, without naming TSM.
- **`AVGO_TSM`**: disclosed from AVGO's side only. This session directly grepped `TSM.yaml`/`TSM.md`
  for "AVGO"/"Broadcom" and found zero matches. AVGO's own record additionally discloses its
  underlying research was WebSearch-sourced throughout, with direct WebFetch attempts against SEC
  EDGAR and investors.broadcom.com returning HTTP 403.
- **`ASML_TSM`**: disclosed from ASML's side only, and ASML's own figure (~24% of net sales) is
  itself explicitly flagged in ASML's own record as secondary-sourced and "requir[ing]
  primary-source (20-F) verification." This session directly grepped `TSM.yaml`/`TSM.md` for "ASML"
  and found zero matches.
- **`KLAC_TSM`**: disclosed from KLAC's side only, at the weakest evidentiary tier in this batch —
  KLAC's own record labels its TSM-specific figure a single, untracked FY2023 data point, distinct
  from its separate, higher-confidence combined foundry/logic concentration figure (65-75% of
  FY2025 revenue, spanning TSMC/Intel/Samsung together, not attributable to TSM alone). This session
  directly grepped `TSM.yaml`/`TSM.md` for "KLAC"/"KLA" and found zero matches.

TSM's own Form 20-F customer-concentration disclosure (largest customer 19% of 2025 revenue,
second-largest 17%, top ten 78%) explicitly does not name any customer by identity — independently
confirmed by this session's direct inspection of `TSM.yaml`/`TSM.md`, which state this non-
disclosure as TSM's own record's express limitation, not an inference by this unit.

### C. Materiality caveats carried forward, not smoothed over

`ASML_TSM`'s own evidence explicitly discloses that TSMC is one of several named concentrated
customers (top two combined ~38%, implying a comparably-scaled second customer, most likely Samsung
per general industry context not independently confirmed here) — not an exclusive dependency.
`KLAC_TSM`'s own evidence explicitly discloses that KLAC's combined foundry/logic concentration
figure (65-75% of FY2025 revenue) spans TSMC, Intel, and Samsung together, with no company-specific
breakdown located. `NVDA_TSM`'s and `AVGO_TSM`'s own evidence explicitly discloses that neither
NVDA's nor AVGO's foundry-risk language names TSM (or any foundry) specifically — a structural
inference from fabless/hybrid status and industry-wide concentration, not a company-specific
disclosure from either side. None of these caveats is abbreviated in any record's own
`evidence[0].uncertainty`/`disconfirming_evidence` fields or its `.md` companion.

### D. What this filing does not do

No `intelligence/companies/*.yaml` or `*.md` file was modified — `NVDA.yaml`/`NVDA.md`,
`ASML.yaml`/`ASML.md`, `KLAC.yaml`/`KLAC.md`, `AVGO.yaml`/`AVGO.md`, and `TSM.yaml`/`TSM.md` were
all read only, never edited. No external research of any kind was performed. No price correlation
was computed, cited, or implied anywhere in any of the four records — each `.md` companion
explicitly states none was computed, per `REL-0001` §G. No `duplicate_economic_exposure`,
`correlated_loss_mechanism`, or `missing_exposure` conclusion was asserted anywhere — `REL-0001`
§C excludes all three as primitive record types, and every record here declares only a
`manufacturing_dependency` or `capital_spending_dependency` primitive. No holdings, targets, tiers,
caps, gates, clusters, ladders, trims, sells, margin, allocator, brokerage, order, chart-evidence,
or "Eureka" (`OPS-0016`) file or system was touched. The `milestone-4-portfolio-relationship-mapping`
gate's own `status: proposed` (`operations/WORKSTREAMS.yaml`) is not itself flipped to `in_progress`
or `complete` by this filing — thirteen total additive records (the nine from `REL-0002`/`REL-0003`
plus this batch's four) are a third step, not completion of Milestone 4, and no claim to the
contrary is made anywhere in this filing. This filing creates no standing authorization for any
future, fifth relationship-content batch or a fifth pair within this one — any such work requires
its own separate, explicit, future principal authorization, exactly as `REL-0001` §I/§L and
`REL-0002`'s/`REL-0003`'s own Rationale both already state.

### E. Pairs considered and abstained

**None.** All four authorized candidate pairs — the original three (`NVDA_TSM`, `ASML_TSM`,
`KLAC_TSM`, per the inventory audit's own §4.1/§4.2 classification) and the fourth
(`AVGO_TSM`, added on the principal's explicit, separately-conditioned authorization and
independently re-verified this session before acceptance) — were found to clear `REL-0001` §E's
evidence/abstention standard, each at the conservative classification and confidence level its own
record states. The inventory audit's own §5.1 finding — a hyperscaler-to-semis capital/customer
chain (MSFT/GOOGL/AMZN/META ↔ NVDA/AVGO) — was independently re-inspected this session and confirmed
to remain an **explicit, disclosed, unresolved evidence gap on both sides**, per Batch5's own text:
"this batch's own research does not resolve that cross-reference either... a disclosed, unresolved
evidence gap on both sides." That gap does not clear `REL-0001` §E and is not converted into a
relationship record by this filing — consistent with `REL-0001` §E's own rule that "silence in
available sources is not evidence of non-existence" but also does not itself constitute evidence
sufficient for a record. No fifth pair, from that gap or any other source, was authorized, requested,
or added to this batch.

### F. Test suite reconciliation, disclosed

Adding four further real `intelligence/relationships/` records made
`test_relationship_validator.py`'s `test_validating_the_real_repository_relationships_dir_does_not_mutate_it`
literally false on its `record_count == 9` assertion (the directory now legitimately holds thirteen
records — the prior nine plus this batch's four). That test's `_REAL_RELATIONSHIP_STEMS` list is
narrowly corrected in this same filing to add `ASML_TSM`, `AVGO_TSM`, `KLAC_TSM`, and `NVDA_TSM`,
preserving the existing before/after byte-for-byte comparison guarantee for all seventeen (now
thirteen) real stems' `.yaml`/`.md` pairs. `test_universe_loaders_never_touch_intelligence_relationships`
required no change — it already asserts before/after existence match, not an unconditional absence,
per `REL-0002`'s own prior correction. Separately, `test_portfolio_hq_dashboard_decisions.py`
hardcodes the live decision count twice (`test_real_repository_catalog_builds_all_69_with_no_issues`
and `test_real_repository_model_and_render_succeed_end_to_end`) — both updated from 69 to 70 to
match this filing's own addition to `governance/decisions.yaml`, the first test renamed to
`..._all_70_...` to match this repository's own established per-addition renaming convention.

### G. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (WS-0005 only — one additive gate entry folding in
`REL-0004`'s own post-merge verification per `OPS-0008` §4(a)'s read-only-folding convention, one
additive gate entry for this batch, one `evidence_refs` block, and the
`active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields, per
`OPS-0001`'s existing convention); (4) `CLAUDE.md` (one concise Decisions Log pointer entry); (5) the
eight `intelligence/relationships/` files listed in §A; (6) `test_relationship_validator.py` (the
one pre-existing test correction in §F above); (7) `test_portfolio_hq_dashboard_decisions.py` (the
two hardcoded-count corrections in §F above). No Company or Theme Intelligence record, no comparison
artifact, no `issuer_lookthrough.yaml`, no `targets.yaml`/`holdings.yaml`/`gates.yaml`, no
`allocate.py`/`levels.py`/`margin_state.py`, no chart-evidence file, and no "Eureka" file is touched.

### H. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (Lane G, `OPS-0009` — full weight, never reduced by this filing's
own combined-PR packaging choice), complete any required bounded correction and exact-head
re-review, and receive explicit principal acceptance before it may be marked ready or merged. This
decision does not mark itself ready and does not authorize its own merge. Nothing in §§A-G above,
and no content of any of the four records, becomes effective until this PR merges to `main`. This
filing does not self-review, does not mark itself ready, and does not merge itself.

## Rationale

**Why these exact four pairs, sharing TSM as the common counterparty.** The `REL-0001` §I inventory
audit's own §4.1/§4.2 tables independently classified all four pairs' underlying evidence against
REL-0001's taxonomy without themselves authorizing a record — this filing is the first to act on
that classification for the TSM-centered manufacturing/capex-dependency evidence, following
`REL-0002` (`CEG_MSFT`) and `REL-0003` (the eight pairs the inventory's own §9 advisory table
recommended). Unlike `REL-0003`'s eight pairs, these four were not part of the inventory's own §9
"first batch" recommendation table — they are drawn instead directly from §4.1/§4.2's evidence
classification, a distinct but equally rigorous evidentiary source within the same audit.

**Why `AVGO_TSM` as a fourth pair, added mid-session, rather than deferred to a future batch.** The
principal explicitly authorized this expansion, conditioned on independent re-verification against
`REL-0001` §E — satisfied, per the "Fourth-pair verification" preflight section above, on the
strength of AVGO's own dedicated, TSMC-naming risk entry (if anything stronger evidence than
NVDA's own more generic language) and the inventory audit's own independent §4.1 classification of
the identical pairing. Batching it with the original three, rather than filing it as a fifth,
separate single-pair decision, follows the same `OPS-0008`/`OPS-0009` proportionality discipline
`REL-0003`'s own Rationale already applied to its eight-pair batch — avoiding a second full
preflight/review/merge cycle for content whose evidence base, schema, and packaging pattern are
already established.

**Why `inferred`, not `observed`, for every record — and why `KLAC_TSM` alone is recorded at
`confidence: low`.** Mirrors `REL-0002`'s and `REL-0003`'s own Rationale exactly: the relevant test
is not "is the underlying source primary," but "is this specific pairwise claim itself directly,
bilaterally confirmed" — and in all four cases here, it is not. `KLAC_TSM`'s confidence is recorded
one notch below the other three specifically because KLAC's own record itself labels its only
TSM-specific figure a single, untracked data point — a distinction in the underlying evidence's own
self-assessed reliability that this filing preserves rather than uniformly rounding up.

**Why one combined batch rather than four (or five, counting the identifier correction) separate
filings.** Follows `REL-0003`'s own precedent and this repository's `OPS-0008`/`OPS-0009`
proportionality discipline: four one-pair governance-and-implementation cycles would each
independently repeat the same preflight, review, and merge overhead for content whose evidence base
and packaging pattern are already established and unchanged from the prior two batches.

## Alternatives Considered

- **File `AVGO_TSM` as its own separate, fifth decision, keeping this filing to the original three
  pairs.** Rejected — the principal's own explicit authorization added `AVGO_TSM` to this batch
  before this filing was drafted, and the pair's evidentiary tier and packaging pattern are
  identical to the other three; a separate filing would repeat overhead this repository's own
  proportionality discipline exists to avoid.
- **Convert the inventory's §5.1 hyperscaler-to-semis gap (MSFT/GOOGL/AMZN/META ↔ NVDA/AVGO) into a
  fifth record, since AVGO and NVDA are both already in this batch.** Rejected — explicitly out of
  scope per this unit's own authorization ("Do not add any fifth pair"), and substantively rejected
  on the merits regardless: the inventory's own §5.1 text states this remains "a disclosed,
  unresolved evidence gap on both sides," not evidence meeting `REL-0001` §E's bar.
- **Upgrade `ASML_TSM`'s or `KLAC_TSM`'s evidence_classification to `observed`, since both companies'
  own records name TSM/TSMC specifically (unlike the generic language in NVDA_TSM/AVGO_TSM).**
  Rejected — per the Rationale above, the specific pairwise claim's bilateral confirmation, not the
  underlying source's specificity alone, governs the classification; ASML's own figure is itself
  labeled secondary/unverified by ASML's own record, and KLAC's is a single untracked data point;
  neither is independently corroborated from TSM's own side.
- **Leave the three original drafts' stale `REL-0004` self-references uncorrected and simply note
  the discrepancy in this filing's prose.** Rejected — the principal's own authorization was explicit
  ("Update only the obsolete internal REL-0004 self-references that now conflict with the merged
  completion-standard decision"), and a record whose own internal citation names a decision it is
  not actually filed under would misrepresent its own provenance to any future reader.

## Consequences

**Authorized and implemented, effective only on this decision's merge:** four
`intelligence/relationships/` records (`ASML_TSM`, `AVGO_TSM`, `KLAC_TSM`, `NVDA_TSM`), the third
WS-0005 Milestone 4 relationship-content batch under `REL-0001`'s frozen schema; one corrected
pre-existing test in `test_relationship_validator.py`; two corrected decision-count assertions in
`test_portfolio_hq_dashboard_decisions.py`; two additive `operations/WORKSTREAMS.yaml` WS-0005 gate
entries (one folding in `REL-0004`'s own post-merge verification, one recording this batch); one
`governance/decisions.yaml` index row; one `CLAUDE.md` Decisions Log pointer entry.

**Not authorized by this filing, now or ever without a further separate decision:** any other
relationship pair beyond the four named above, including any pair drawn from the inventory's own
§5.1 hyperscaler-to-semis gap; any Company or Theme Intelligence record edit; any price-correlation
study of any kind; any `duplicate_economic_exposure`/`correlated_loss_mechanism`/`missing_exposure`
conclusion; any graph or "Eureka" implementation; any tier/target/holdings/cluster/cap/gate/ladder/
trim/sell/margin/allocator/brokerage/order change; Milestone 5 or any later WS-0005 milestone; and a
new workstream.

**Unchanged by this decision:** every existing Company/Theme Intelligence record, including
`intelligence/companies/NVDA.yaml`/`.md`, `ASML.yaml`/`.md`, `KLAC.yaml`/`.md`, `AVGO.yaml`/`.md`,
and `TSM.yaml`/`.md`; every existing comparison artifact; the nine prior
`intelligence/relationships/` records (`CEG_MSFT`, `AVGO_GOOGL`, `AVGO_META`, `ETN_GNRC`, `GEV_GNRC`,
`GNRC_PWR`, `GOOGL_MSFT`, `AMZN_MSFT`, `AMZN_GOOGL`); `issuer_lookthrough.yaml`; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution;
`WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; the `milestone-4-portfolio-relationship-mapping` gate's own `status: proposed`;
`REL-0001`, `REL-0002`, `REL-0003`, and `REL-0004`, all unedited and not reopened.

This decision becomes effective only when its implementing pull request merges to `main`.
