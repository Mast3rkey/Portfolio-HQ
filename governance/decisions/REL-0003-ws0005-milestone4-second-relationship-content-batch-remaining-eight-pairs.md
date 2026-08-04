---
decision_id: REL-0003
date: 2026-08-04
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, REL-0002, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0033, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded implementation unit: a second
WS-0005 Milestone 4 relationship-content batch, limited to the eight pairs the `REL-0001` §I
inventory audit's own §9 table already identified as evidence-ready — `AVGO_GOOGL`, `AVGO_META`,
`GNRC_GEV`, `GNRC_ETN`, `GNRC_PWR`, `MSFT_GOOGL`, `MSFT_AMZN`, and `GOOGL_AMZN` (filenames as
supplied in the authorizing task; §B below corrects three of these to REL-0001 §B's own mandatory
alphabetical ordering) — implemented as one combined governance-and-implementation pull request,
following `REL-0002`'s own packaging precedent for the first such batch (`CEG_MSFT`) exactly. The
authorization is explicit that this unit must: begin with full repository preflight; create only
this decision file and the eight authorized relationship records; use only repository evidence
already identified (no external research); explicitly disclose one-sided or incomplete sourcing per
pair; not infer unsupported financial magnitude, bilateral confirmation, causality, correlation,
ranking, or policy implications; abstain on any pair whose evidence no longer clears `REL-0001` after
fresh inspection; not modify any existing Company or Theme Intelligence record (`CEG_MSFT` excepted
only for a mechanically required, independently justified compatibility correction — none was found
necessary, see §D below); and not touch holdings, targets, tiers, caps, clusters, gates, allocator,
margin, brokerage, orders, charts, ladders, trims, sells, Milestone 5, or "Eureka." Everything below
is bounded by that authorization.

### Preflight performed this session, independently verified, not assumed

`origin` fetched and pruned; local `main` confirmed identical to `origin/main` at
`7305dc21bf6e7f30e62d75e70b82275ef3530d09` (the merge commit of PR #240, `REL-0002`/`CEG_MSFT`),
working tree clean. `gh pr list --state open` returns empty — zero open pull requests. No branch or
open PR overlaps `governance/decisions.yaml`, `operations/WORKSTREAMS.yaml`, `CLAUDE.md`,
`intelligence/relationships/`, `relationship_validator.py`, `test_relationship_validator.py`, or
`test_portfolio_hq_dashboard_decisions.py`.

`REL-0001` and `REL-0002` were both re-read in full. `REL-0001`: `status: Accepted`, effective —
freezes the schema/taxonomy/evidence standard this unit's eight records must satisfy, and authorizes
future relationship-content batches only through their own separate, explicit authorization (§I/§L),
never automatic progression. `REL-0002`: frontmatter `status: Proposed` in the decision file and in
`governance/decisions.yaml` — **this is a known, disclosed, pre-existing state, not a defect this
filing corrects.** Independently verified via the GitHub API: PR #240 (`REL-0002`) is `MERGED` (merge
commit `7305dc21bf6e7f30e62d75e70b82275ef3530d09`, merged 2026-08-04T15:10:17Z), received an
independent exact-head review (review `4856012228`, anchored to head `8403a4f8d57d97367bc2243ee64c2048f89259df`,
verdict "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE," zero BLOCKING/MAJOR/MINOR findings, two
non-blocking NOTEs), and a retained `Principal acceptance:` PR comment at that exact head. `REL-0002`'s
own frontmatter `status: Proposed` therefore reflects this repository's established two-step pattern
(`CHART-0001`/`CHART-0002` precedent): a decision may be merged, independently reviewed, and
principal-accepted while still carrying `status: Proposed`, with the flip to `status: Accepted`
requiring its own later, separate acceptance-recording filing. **That acceptance-recording filing for
`REL-0002` is not part of this unit's authorized scope and is not performed here** — disclosed as
discovered, pre-existing, out-of-scope state, per this repository's own discovered-work-reconciliation
discipline (`OPS-0015`), not silently fixed.

`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` (the `REL-0001` §I
inventory audit, produced by PR #238, merged) was re-read in full, specifically its §9 candidate
table. That table names, as evidence-ready second-batch candidates beyond `CEG_MSFT`: `AVGO_GOOGL` and
`AVGO_META` (customer_dependency, AVGO's own disclosed AI-segment customer roster); `GNRC_GEV`,
`GNRC_ETN`, and `GNRC_PWR` (complement, GNRC's own disclosed data-center-power-stack analysis); and
the `MSFT`/`GOOGL`/`AMZN` `competitor` triad (three separate pairwise records, per §D's
one-record-per-pair rule) — exactly the eight pairs this filing implements, with no ninth candidate
drawn from that table and no candidate the table itself declined (the ASML/KLAC China-exposure
question and the ISRG/TMO regulatory question, §9's own "Not recommended as a near-term batch" list)
included.

`relationship_validator.py` and `test_relationship_validator.py` were re-read in full to confirm the
exact schema this unit's eight records must satisfy — unchanged since `REL-0002`. `governance/decisions.yaml`
was independently reconciled against `governance/decisions/*.md` (less `README.md`): 67 files, 67 index
rows, 1:1, `REL-0002` the last-filed entry — confirming `REL-0003` as the next unused identifier.
`intelligence/relationships/` was confirmed to contain exactly one record, `CEG_MSFT.yaml`/`.md`, before
this unit's own work.

### Fresh evidence re-inspection performed this session, not merely cited from the inventory

Per the authorizing task's explicit instruction to verify every pair independently rather than trust
the inventory's own paraphrase, this session directly re-opened and re-read, in full: `intelligence/companies/AVGO.yaml`
(competitive_advantages[1], risks[0], sources[2]); `intelligence/companies/GNRC.yaml` (claim `GNRC-C03`)
and `intelligence/companies/GNRC.md` §13; `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`
§6; and `intelligence/BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` §7. Every claim, source
citation, and materiality caveat in the eight records below is drawn directly from these re-inspected
sources, not from the inventory table's own summary text. This session additionally, independently
grepped every counterparty's own Company Intelligence record for each pair
(`GOOGL.yaml`/`GOOGL.md`/`META.yaml`/`META.md` for "AVGO"/"Broadcom"; `ETN.yaml`/`ETN.md`/`GEV.yaml`/`GEV.md`/`PWR.yaml`/`PWR.md`
for "GNRC"/"Generac"; and `AMZN.yaml`/`GOOGL.yaml`/`MSFT.yaml` cross-references for the three
`competitor` records) and found **zero independent corroboration in every case** — confirming, not
merely trusting, the one-sided/single-source-synthesis sourcing disclosed in every record below.

**Bounded correction (same PR, independent review 4856585060):** the paragraph immediately above,
as originally filed, was inaccurate for the `competitor` triad specifically. Its grep for that
triad checked only `AMZN.yaml`/`GOOGL.yaml`/`MSFT.yaml` — unlike the AVGO/GNRC clauses in the same
sentence, which named both `.yaml` **and** `.md` files for every counterparty — and the "zero
independent corroboration in every case" claim did not hold once each company's own `.md` record is
included: `AMZN.md`, `GOOGL.md`, and `MSFT.md` each contain a "capital-priority discipline" section
in which that company explicitly names the other two as competing for capital-priority ranking
(e.g. `AMZN.md`: "AMZN competes for capital priority against MSFT and GOOGL"; `GOOGL.md`: GOOGL
"compete[s] for T1's overall capital-priority ranking against MSFT... and against AMZN"; `MSFT.md`:
"the next investment dollar favors MSFT over GOOGL or AMZN... is not resolved by this record"). That
capital-priority language is a portfolio-capital-allocation concept — which name should receive the
next investment dollar — analytically distinct from the customer-demand competitive overlap
REL-0001 §C.10 defines the `competitor` primitive around, and the three `competitor` records'
`evidence[0].uncertainty` fields and `.md` "Source-access disclosure" sections now state this
distinction explicitly rather than asserting an unqualified "zero corroboration." This finding is
disclosure-accuracy only — it does not change any pair's `relationship_type`, does not upgrade any
`evidence_classification` from `inferred`, and does not affect the AVGO/GNRC triads' own accurate
"zero corroboration" findings, which the review independently re-confirmed as sound.

### Alphabetical filename correction (mechanical, §B compliance)

`REL-0001` §B requires every relationship record's filename and `tickers:` field to use strict
alphabetical ticker order (`A_B`, never `B_A`) — `relationship_validator.py` mechanically enforces
this (`_validate_tickers_field`). The authorizing task's own reference labels for three of the eight
pairs were not in alphabetical order: `GNRC_GEV` (alphabetically `GEV` precedes `GNRC`), `GNRC_ETN`
(alphabetically `ETN` precedes `GNRC`), and `MSFT_GOOGL`/`MSFT_AMZN`/`GOOGL_AMZN` (alphabetically
`GOOGL`/`AMZN`/`AMZN` each precede `MSFT`/`MSFT`/`GOOGL` respectively). This filing implements the
identical eight pairs, by identical company identity and evidence, under their REL-0001 §B-compliant
alphabetical filenames: `AVGO_GOOGL`, `AVGO_META`, `GEV_GNRC`, `ETN_GNRC`, `GNRC_PWR`, `GOOGL_MSFT`,
`AMZN_MSFT`, `AMZN_GOOGL`. This is a mechanical filename/field-ordering correction only — no pair's
identity, evidence, classification, or scope changed.

## Decision

**`REL-0003` authorizes, and — in the same pull request, following `REL-0002`'s own combined-PR
packaging precedent — implements, the second WS-0005 Milestone 4 relationship-content batch: eight
`intelligence/relationships/` records covering three `customer_dependency` records (`AVGO_GOOGL`,
`AVGO_META`), three `complement` records (`ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`), and three `competitor`
records (`GOOGL_MSFT`, `AMZN_MSFT`, `AMZN_GOOGL`) — all under `REL-0001`'s frozen schema, all reusing
only evidence already present in the repository at this unit's own preflight. No other relationship
pair, no Company or Theme Intelligence edit, no correlation study, no score or ranking, and no policy
change is authorized or performed by this filing.**

### A. What was created

Exactly sixteen files: `AVGO_GOOGL.yaml`/`.md`, `AVGO_META.yaml`/`.md`, `ETN_GNRC.yaml`/`.md`,
`GEV_GNRC.yaml`/`.md`, `GNRC_PWR.yaml`/`.md`, `GOOGL_MSFT.yaml`/`.md`, `AMZN_MSFT.yaml`/`.md`, and
`AMZN_GOOGL.yaml`/`.md`, all under `intelligence/relationships/`.

| Pair | `relationship_type` | Directionality | `decision_served` | `evidence_classification` |
|---|---|---|---|---|
| `AVGO_GOOGL` | `customer_dependency` | directional, AVGO subject / GOOGL object | `duplicate_exposure_detection`, `thesis_monitoring` | `inferred` |
| `AVGO_META` | `customer_dependency` | directional, AVGO subject / META object | `duplicate_exposure_detection`, `thesis_monitoring` | `inferred` |
| `ETN_GNRC` | `complement` | symmetric | `duplicate_exposure_detection`, `missing_exposure_review` | `inferred` |
| `GEV_GNRC` | `complement` | symmetric | `duplicate_exposure_detection`, `missing_exposure_review` | `inferred` |
| `GNRC_PWR` | `complement` | symmetric | `duplicate_exposure_detection`, `missing_exposure_review` | `inferred` |
| `GOOGL_MSFT` | `competitor` | symmetric | `duplicate_exposure_detection`, `stress_testing` | `inferred` |
| `AMZN_MSFT` | `competitor` | symmetric | `duplicate_exposure_detection`, `stress_testing` | `inferred` |
| `AMZN_GOOGL` | `competitor` | symmetric | `duplicate_exposure_detection`, `stress_testing` | `inferred` |

Every record's evidence entry is deliberately classified `inferred`, not `observed`, following
`REL-0002`'s own conservative discipline: `customer_dependency` records rest on AVGO's own record,
whose underlying source for the specific named-customer claim is itself labeled "SECONDARY (aggregated...
industry coverage)" rather than a primary filing either side opened; `complement` records rest on
GNRC's own record's synthesized analytical framing (GNRC.md §13), not a confirmed named joint contract;
`competitor` records rest on `BATCH5`'s own comparative synthesis (§7), not any individual company's
own risk-disclosure statement.

### B. One-sided and single-source sourcing, disclosed per pair

- **`AVGO_GOOGL`/`AVGO_META`**: disclosed from AVGO's side only. This session directly grepped
  `GOOGL.yaml`/`GOOGL.md` and `META.yaml`/`META.md` for "AVGO"/"Broadcom" and found zero matches in
  either. AVGO's own record additionally discloses that its FY2025 10-K and Q2 FY2026 earnings release
  — the primary documents underlying its company-wide customer-concentration figures — were each
  "identified but NOT opened" by that record's own research session; the specific AI-segment named-
  customer-roster claim is sourced to AVGO.yaml's own SECONDARY-labeled aggregated-industry-coverage
  entry.
- **`ETN_GNRC`/`GEV_GNRC`/`GNRC_PWR`**: disclosed from GNRC's side only. This session directly grepped
  `ETN.yaml`/`ETN.md`, `GEV.yaml`/`GEV.md`, and `PWR.yaml`/`PWR.md` for "GNRC"/"Generac" and found zero
  matches in any of the six files. GNRC's own record's `complement` framing (§13) is itself an explicit
  analytical synthesis, not a confirmed named joint contract linking GNRC to any one of the three by
  name; GNRC.md §13 states directly that no correlation scan against `power_infra` has ever been
  performed by any prior repository decision.
- **`GOOGL_MSFT`/`AMZN_MSFT`/`AMZN_GOOGL`**: the customer-demand competitive-overlap claim (REL-0001
  §C.10's own definition of the `competitor` primitive) is disclosed from a single batch-level
  comparative source only (`BATCH5` §7), not from any individual company's own risk disclosure — this
  session directly grepped each pair's two `.yaml` files for cross-references to each other and found
  no corroboration there (the only cross-reference located — a shared EU DMA regulatory-proceeding URL
  naming AMZN and MSFT — is a distinct regulatory matter, disclosed as context in `AMZN_MSFT.md`, not
  folded into the competitor claim itself). **Bounded correction (independent review 4856585060):**
  each company's own `.md` record does independently name the other two, but for **capital-priority
  competition** (which name should receive the next investment dollar), not customer-demand
  competitive overlap — `AMZN.md`, `GOOGL.md`, and `MSFT.md` each contain a "capital-priority
  discipline" section naming the other two batch members as capital-priority competitors. This
  distinct concept does not corroborate the customer-demand `competitor` claim these three records
  assert, and is not treated as if it did — see each record's own `evidence[0].uncertainty` and `.md`
  Source-access disclosure for the full, corrected statement.

### C. Materiality caveats carried forward, not smoothed over

The three `complement` records explicitly carry GNRC's own record's disclosed materiality caveat:
GNRC's C&I segment was only ~35% of FY2025 total company revenue, and even within C&I, data centers
are the "core driver" but not the entirety — residential demand (~54% of revenue), genuinely unrelated
to the AI-buildout mechanism, remains GNRC's majority business. This caveat is stated in full, per
pair, in each record's own `evidence[0].uncertainty`/`disconfirming_evidence` fields and its `.md`
companion — never abbreviated to imply a stronger relationship than GNRC's own record itself supports.

### D. What this filing does not do

No `intelligence/companies/*.yaml` or `*.md` file was modified — `AVGO.yaml`/`AVGO.md`, `GOOGL.yaml`/`GOOGL.md`,
`META.yaml`/`META.md`, `GNRC.yaml`/`GNRC.md`, `ETN.yaml`/`ETN.md`, `GEV.yaml`/`GEV.md`, `PWR.yaml`/`PWR.md`,
`MSFT.yaml`/`MSFT.md`, and `AMZN.yaml`/`AMZN.md` were all read only, never edited. **The authorizing
task's own contemplated "mechanically required, independently justified compatibility correction" to
`CEG_MSFT` was evaluated and found unnecessary** — `CEG_MSFT.yaml`/`.md` remain fully schema-valid and
byte-unmodified by this filing (confirmed via `git diff`, see §H). No external research of any kind was
performed. No price correlation was computed, cited, or implied anywhere in any of the eight records —
each `.md` companion explicitly states none was computed, per `REL-0001` §G. No
`duplicate_economic_exposure`, `correlated_loss_mechanism`, or `missing_exposure` conclusion was
asserted anywhere — `REL-0001` §C excludes all three as primitive record types, and every record here
declares only a `customer_dependency`, `complement`, or `competitor` primitive. No holdings, targets,
tiers, caps, gates, clusters, ladders, trims, sells, margin, allocator, brokerage, order, chart-evidence,
or "Eureka" (`OPS-0016`) file or system was touched. The `milestone-4-portfolio-relationship-mapping`
gate's own `status: proposed` (`operations/WORKSTREAMS.yaml`) is not itself flipped to `in_progress` or
`complete` by this filing — eight additional additive records are a second step, not completion of
Milestone 4, and no claim to the contrary is made anywhere in this filing. This filing creates no
standing authorization for any future, third relationship-content batch — any such batch requires its
own separate, explicit, future principal authorization, exactly as `REL-0001` §I/§L and `REL-0002`'s own
Rationale both already state.

### E. Pairs considered and abstained

**None.** Every one of the eight authorized candidate pairs was independently re-inspected this
session (per the "Fresh evidence re-inspection" preflight above) and found to clear `REL-0001` §E's
evidence/abstention standard at the conservative `inferred` classification each record declares. No
pair's underlying evidence was found to have degraded, been retracted, or otherwise failed to clear
`REL-0001` since the inventory audit's own §9 recommendation.

### F. Test suite reconciliation, disclosed

Adding eight further real `intelligence/relationships/` records made `test_relationship_validator.py`'s
`test_validating_the_real_repository_relationships_dir_does_not_mutate_it` literally false on its
`record_count == 1` assertion (the directory now legitimately holds nine records, `CEG_MSFT` plus this
batch's eight). That test is narrowly corrected in this same filing to assert `record_count == 9` and to
perform an explicit before/after byte-for-byte comparison of all eighteen files (nine `.yaml` plus nine
`.md`) — strengthening, not weakening, the existing guarantee, per the identical discipline `REL-0002`
already applied to this same test. `test_universe_loaders_never_touch_intelligence_relationships`
required no change — it already asserts before/after existence match, not an unconditional absence, per
`REL-0002`'s own prior correction. Separately, `test_portfolio_hq_dashboard_decisions.py` hardcodes the
live decision count twice (`test_real_repository_catalog_builds_all_67_with_no_issues` and
`test_real_repository_model_and_render_succeed_end_to_end`) — both updated from 67 to 68 to match this
filing's own addition to `governance/decisions.yaml`, the first test renamed to `..._all_68_...` to match
this repository's own established per-addition renaming convention.

### G. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (WS-0005 only — one additive gate entry folding in `REL-0002`'s
own post-merge verification per `OPS-0008` §4(a)'s read-only-folding convention, one additive gate entry
for this batch, one `evidence_refs` block, and the `active_branch`/`active_pr`/`last_verified_main_sha`/
`last_verified_date` self-reference fields, per `OPS-0001`'s existing convention); (4) `CLAUDE.md` (one
concise Decisions Log pointer entry); (5) the sixteen `intelligence/relationships/` files listed in §A;
(6) `test_relationship_validator.py` (the one pre-existing test correction in §F above); (7)
`test_portfolio_hq_dashboard_decisions.py` (the two hardcoded-count corrections in §F above). No Company
or Theme Intelligence record, no comparison artifact, no `issuer_lookthrough.yaml`, no
`targets.yaml`/`holdings.yaml`/`gates.yaml`, no `allocate.py`/`levels.py`/`margin_state.py`, no
chart-evidence file, and no "Eureka" file is touched.

### H. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (Lane G, `OPS-0009` — full weight, never reduced by this filing's own
combined-PR packaging choice), complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This decision does not
mark itself ready and does not authorize its own merge. Nothing in §§A-G above, and no content of any of
the eight records, becomes effective until this PR merges to `main`. This filing does not self-review,
does not mark itself ready, and does not merge itself.

## Rationale

**Why these exact eight pairs, and why one batch rather than eight separate filings.** The `REL-0001`
§I inventory audit's own §9 table independently identified all eight as evidence-ready on the same
grounds `REL-0002` already used for `CEG_MSFT` — existing evidence sufficient without new research,
purely additive (no counterparty record requires editing), and each with a specific, non-generic
`decision_served` value. Batching all eight into one filing, rather than eight sequential single-pair
filings, follows this repository's own `OPS-0008`/`OPS-0009` proportionality discipline: eight
one-pair governance-and-implementation cycles would each independently repeat the same preflight,
review, and merge overhead `OPS-0008` §4 and `OPS-0009` §2 both exist to avoid duplicating, for content
whose evidence base, schema, and packaging pattern are already established and unchanged from `REL-0002`.

**Why `inferred`, not `observed`, for every record — including the `complement` records whose
underlying GNRC source is itself a directly-fetched primary document.** GNRC's own Q2 2026 earnings
release was directly fetched and read by that record's own research session (a primary source, on
GNRC's side). But the specific claim each `complement` record makes here — that GNRC's data-center
pivot is complementary to ETN's, GEV's, or PWR's specific role — is GNRC.md §13's own synthesized
analytical judgment, not a fact GNRC's earnings release itself states about any of the three
counterparties by name, and no counterparty's own record independently corroborates it. The same
distinction applies to the `customer_dependency` and `competitor` records: a primary-source-grounded
underlying fact (AVGO's disclosed customer roster; each hyperscaler's own disclosed cloud business)
does not itself make this record's specific pairwise claim `observed` when the claim is this session's
(or a prior batch's) own synthesis rather than either counterparty's own stated fact. This mirrors
`REL-0002`'s own Rationale for `CEG_MSFT` exactly: the relevant test is not "is the underlying source
primary," but "is this specific pairwise claim itself directly, bilaterally confirmed" — and in every
one of these eight cases, it is not.

**Why alphabetical-filename correction, not the task's own reference pair-names.** `REL-0001` §B's
alphabetical-ordering rule is mechanically enforced by `relationship_validator.py` — filing under
non-alphabetical filenames would fail validation outright. Correcting the filenames (`GEV_GNRC` not
`GNRC_GEV`; `ETN_GNRC` not `GNRC_ETN`; `GOOGL_MSFT`/`AMZN_MSFT`/`AMZN_GOOGL` not
`MSFT_GOOGL`/`MSFT_AMZN`/`GOOGL_AMZN`) changes no pair's identity, evidence, or scope — it is the same
mechanical compliance step `REL-0002`'s own filename (`CEG_MSFT`, already alphabetical) never needed to
demonstrate.

## Alternatives Considered

- **File eight separate single-pair decisions, matching `REL-0002`'s own one-pair precedent exactly.**
  Rejected per this filing's own explicit, controlling batching instruction — not rejected as a general
  principle; a future pair authorized without an equally explicit batching instruction should default
  back to `REL-0002`'s own single-pair pattern absent a fresh, equally explicit instruction.
- **Include a ninth pair from the inventory's §9 table's "Not recommended" list (ASML/KLAC China
  exposure, ISRG/TMO regulatory) to round out the batch.** Rejected — the inventory's own §9 table
  explicitly found both fail `REL-0001` §C's "same specific mechanism" bar on existing evidence; neither
  is authorized by this filing's own explicit eight-pair scope, and including either would require new
  primary research this unit is not authorized to perform.
- **Upgrade the `complement`/`competitor` records to `observed` given their underlying sources include
  at least one directly-fetched primary document (GNRC's earnings release) or comparative synthesis
  from an already-reviewed batch artifact.** Rejected — per the Rationale above, the specific pairwise
  claim, not the underlying source's provenance alone, governs the classification; none of the eight
  pairwise claims is independently, bilaterally confirmed.
- **Fix `REL-0002`'s own stale `status: Proposed` frontmatter as part of this filing, since this filing
  already touches `governance/decisions.yaml`.** Rejected — that is its own separate, future,
  acceptance-recording filing (matching the `CHART-0001`/`CHART-0002` precedent for this exact kind of
  correction), outside this unit's own explicitly bounded scope; disclosed in the Preflight section
  above as discovered, out-of-scope state rather than silently left unmentioned.

## Consequences

**Authorized and implemented, effective only on this decision's merge:** eight `intelligence/relationships/`
records (`AVGO_GOOGL`, `AVGO_META`, `ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`, `GOOGL_MSFT`, `AMZN_MSFT`,
`AMZN_GOOGL`), the second WS-0005 Milestone 4 relationship-content batch under `REL-0001`'s frozen
schema; one corrected pre-existing test in `test_relationship_validator.py`; two corrected
decision-count assertions in `test_portfolio_hq_dashboard_decisions.py`; two additive
`operations/WORKSTREAMS.yaml` WS-0005 gate entries (one folding in `REL-0002`'s own post-merge
verification, one recording this batch); one `governance/decisions.yaml` index row; one `CLAUDE.md`
Decisions Log pointer entry.

**Not authorized by this filing, now or ever without a further separate decision:** any other
relationship pair beyond the eight named above; any Company or Theme Intelligence record edit; any
price-correlation study of any kind; any `duplicate_economic_exposure`/`correlated_loss_mechanism`/
`missing_exposure` conclusion; any graph or "Eureka" implementation; any tier/target/holdings/cluster/
cap/gate/ladder/trim/sell/margin/allocator/brokerage/order change; Milestone 5 or any later WS-0005
milestone; and a new workstream.

**Unchanged by this decision:** every existing Company/Theme Intelligence record, including
`intelligence/companies/AVGO.yaml`/`.md`, `GOOGL.yaml`/`.md`, `META.yaml`/`.md`, `GNRC.yaml`/`.md`,
`ETN.yaml`/`.md`, `GEV.yaml`/`.md`, `PWR.yaml`/`.md`, `MSFT.yaml`/`.md`, and `AMZN.yaml`/`.md`; every
existing comparison artifact; `intelligence/relationships/CEG_MSFT.yaml`/`.md`; `issuer_lookthrough.yaml`;
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the
Constitution; `WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; the `milestone-4-portfolio-relationship-mapping` gate's own `status: proposed`;
`REL-0001` and `REL-0002`, both unedited and not reopened.

This decision becomes effective only when its implementing pull request merges to `main`.
