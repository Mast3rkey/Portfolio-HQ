---
decision_id: XASSET-0025
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0016, XASSET-0018, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, LEVEL2-0001, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0025-level1-endpoint-source-and-authority-identification.md
---

## Context

XASSET-0024 is effective (PR #323, merge `4ec64c13552c101e6e132c295617789926b5066a`). Its Outcome A —
`ENDPOINT_BASIS_EXISTS_UNDER_CURRENT_METHODOLOGY` — determined that a lawful endpoint-origin route is
constructible *in principle* under accepted authority, and stated plainly that this is "deliberately **not**
a prediction that such a source can be produced, cheaply or at all. Feasibility in principle is a much
weaker claim than availability in fact."

That leaves exactly one question standing between the program and its next expensive commitment:

> Does any currently accepted source actually satisfy the endpoint-admissibility test for a Level-1
> sleeve-share bound, with existing authority competent for that exact purpose?

XASSET-0024 §J enumerated twelve properties a qualifying source must satisfy but applied them to nothing.
XASSET-0023 §H.8 applied its admissibility test to the frozen XASSET-0021 §C snapshot and found it
unsatisfied, but that finding was reached mechanically from the snapshot's DISCLOSURE classifications
rather than from an inventory of what the sources actually contain, and it did not reach the corpus
outside the snapshot at all. Neither determination tells a future unit whether it is looking for a missing
*authority* over evidence that already exists, or for evidence that does not exist anywhere.

Those two situations call for completely different and non-interchangeable next filings, at very different
cost. This filing distinguishes them. It is a governance/evidence-identification unit: it reads accepted
authority and accepted evidence and records what is there. It creates no endpoint, selects no sleeve,
commissions and runs no research, grants no authority, and extends no snapshot.

**Preflight, independently re-verified this session, not inherited.** GitHub `main`, `origin/main`, and
local `HEAD` all at `4ec64c13552c101e6e132c295617789926b5066a`; working tree clean; zero open pull
requests; PR #323 confirmed merged via the GitHub API with merge-commit CI run `31903743866` `completed` /
`success` at that exact `head_sha`; decision catalog 126 rows with `issues == ()`; `XASSET-0025` confirmed
unused repository-wide; `level1_application_schema.APPLICATION_AUTHORIZATION_REGISTRY` confirmed empty
(`MappingProxyType({})`); no `intelligence/level1_application/` artifact; the XASSET-0021 §N matrix
unchanged at 14 / 14 / 2 with `application_time_author_or_reviewer_judgment_remaining: 2`. All 21
XASSET-0021 §C.2 rows and the five §C.3 configuration files were re-hashed this session and **every
SHA-256 matches** the frozen snapshot exactly. No competing mutation lane exists.

## Decision

### A. Lifecycle, authority, and controlling identity

`OPS-0009` Lane G, governance-only. Effective on merge of this filing after its own independent exact-head
review, principal exact-head acceptance, and immediate post-merge verification. Until then it determines
nothing.

Controlling upstream identity, unedited by this filing: XASSET-0019, XASSET-0020, XASSET-0021,
XASSET-0022, XASSET-0023, XASSET-0024, NUM-0001, LEVEL2-0001, and the accepted RISK corpus. Where this
filing and any of them appear to differ, they control and this filing is wrong.

### B. Scope

In scope: constructing a deterministic candidate-source test from accepted authority; searching the
accepted corpus against it; adversarially rejecting false candidates; recording a per-sleeve, per-bound
result matrix; selecting one overall outcome; and — because the outcome is a null — identifying the
smallest exact future research question capable of producing qualifying evidence.

Out of scope and not performed: any endpoint, bound, percentage, range, or sizing; any sleeve selection or
preference; any research, data acquisition, backtest, or research charter; any methodology amendment; any
representation rule; any snapshot extension or schema successor; any application authority or registry
population; any Level-2 work; any liquidity determination; any RISK rerun, refresh, third attempt, or
lapsed-parameter reuse. `/private/tmp/phq-risk0001-results` was not accessed.

**Sleeve-agnosticism was maintained procedurally, not merely asserted.** All four sleeves were inspected
under the identical test before any result was recorded, and §J below explains why one genuine asymmetry
found in the evidence is nevertheless not permitted to select a sleeve.

### C. The endpoint quantity, adopted unchanged

XASSET-0024 §C's definition is adopted verbatim by reference and is not restated, reinterpreted, or
narrowed: **a LOWER or UPPER bound on one named sleeve's share of one exact normalized unit of
prospective, unlevered, asset-side capital.** Debt, debt reduction, margin buying power, leverage, and
buffer state are excluded from the denominator. `UNSIZED_UNASSIGNED_CAPITAL` is the unresolved complement
and is never an endpoint source or a residual plug.

The four Level-1 sleeves are `equity`, `fund_broad_market`, `fund_gld_defensive`, and `crypto`.

### D. The deterministic candidate test

Every criterion below is assembled from accepted authority. None is new, and none is relaxed. A candidate
must pass **all ten**; failing any one is disqualifying on its own.

| # | Criterion | Governing authority | Disqualifying condition |
|---|---|---|---|
| T1 | **Right quantity** — states or source-prescribes a value for the §C quantity | XASSET-0024 §C; XASSET-0023 §H.2 item 1; XASSET-0020 §D | Any other quantity, however expressed as a percentage |
| T2 | **Admitted subject matter** — classified DRIVER under one of XASSET-0020 §E.1's six closed classes, on the source's own subject matter, with the quantitative statement intrinsic to that evidence | XASSET-0020 §E.1, §E.3; XASSET-0023 §H.1 item 3; XASSET-0024 §D, §J.3 | DISCLOSURE classification; CONSTRAINT classification; DRIVER status claimed only because the source contains a share figure |
| T3 | **Origin route** — exactly one of R1 (uniquely stated) or R2 (uniquely source-prescribed mathematical derivation) | XASSET-0023 §H.2, §H.3 ("There is no third route"); XASSET-0024 §D | Any of non-routes N1–N8; a composed, selected, or invented derivation |
| T4 | **NUM-0001 provenance** — complete §4 field set, class from items 1–5, route-class coherence | NUM-0001 §1, §4, §7, §8, §11; XASSET-0023 §H.4; XASSET-0024 §E.3, §J.7 | Class 6; incomplete field set; class 4 or 5 without the §E.3 eight-item test satisfied upstream |
| T5 | **Competent existing authority** — accepted/effective scope already extends to fixing a Level-1 sleeve share | XASSET-0023 §H.2 item 3; XASSET-0024 §J.5 | Authority effective for another purpose; lapsed authority; reuse-barred authority |
| T6 | **Uniqueness / zero author discretion** — exactly one lawful value, nothing left for an analyst, reviewer, or application author to choose | XASSET-0021 §F; XASSET-0023 §H.2 items 2 and 5, §H.6 item 5; XASSET-0024 §E.3, §J.8 | A second lawful value; an open interval with no member-fixing rule; any tunable step |
| T7 | **Freshness / effectivity** — governed currentness rule applied as written; not stale, lapsed, superseded, or reuse-barred for the endpoint purpose | XASSET-0020 §F.1; XASSET-0021 §H; XASSET-0024 §E.3 item 8 | No governed currentness rule (remains disclosure); met lapse condition; `NEW_GOVERNANCE_AUTHORITY_REQUIRED` |
| T8 | **Snapshot position** — present in XASSET-0021 §§C.2–C.3, or in a snapshot lawfully replaced or extended by separate future authorization | XASSET-0021 §C.1; XASSET-0023 §H.1 item 2; XASSET-0024 §J.2 | Outside the frozen snapshot with no accepted extension |
| T9 | **Representation** — survives §G's self-contained or separately-ruled path, or is explicitly representation-blocked | XASSET-0021 §E.2, §E.3; XASSET-0023 §H.5; XASSET-0024 §G | Any missing, unavailable, conflicted, or disagreeing required representation, absent an accepted rule |
| T10 | **Unresolved-pair independence** — for a RANGE, the endpoint does not consume an unresolved pair as an input at all | XASSET-0020 §I; XASSET-0023 §H.5 item 4; XASSET-0024 §H.4 | Pair-dependence by construction; direction-robustness demonstrated by inspection rather than independence |

Additionally, every candidate must clear **all four limbs** of XASSET-0024 §F's firewall: wrong quantity
(Limb 1), right quantity but barred origin (Limb 2), right quantity and class but incompetent authority
scope (Limb 3), and constraint-only content (Limb 4).

**T8 has a structural consequence that must be stated before any result is read.** No accepted decision
has replaced or extended the XASSET-0021 §C snapshot; this session verified that directly. Therefore any
source outside the frozen snapshot fails T8 under existing authority regardless of its other properties,
and its best attainable result is `CANDIDATE_EXISTS_AUTHORITY_GAP` — never
`QUALIFIES_UNDER_EXISTING_AUTHORITY`. This is not a finding about any particular source; it is the shape of
the current authority.

### E. Search coverage

Search was targeted rather than exhaustive re-reading, and was designed so that a miss would require a
sleeve share to be present in a form matching none of the following.

1. **Field-name enumeration.** Every field name across all of `intelligence/` and `research/` matching
   `pct|percent|share|weight|allocation|bound|min|max|floor|ceiling|target` was enumerated and ranked by
   frequency. Sixty distinct names were reviewed; each carrying a numeric value was traced to its file.
2. **Whole-snapshot numeric inventory.** Every one of the 21 XASSET-0021 §C.2 sources was parsed and
   **every numeric scalar and numeric-valued string anywhere in its document tree** was extracted — not
   only fields with share-like names.
3. **Prose scan of the snapshot.** The same 21 sources were scanned for percent-like tokens
   (`N%`, `N percent`, `N pp`, `pct`) embedded inside free-text string values, so that a share stated in a
   narrative field could not escape step 2.
4. **RISK snapshot inspection.** `pre_registration.yaml`'s scenario blocks and its full 20-row
   `consequential_parameter_registry` were read field-by-field, and `disposition.json`'s four family
   results were read directly.
5. **Outside-snapshot sweep.** `intelligence/level1_sleeve_synthesis/numeric_sizing/`, `policy_adoption/`,
   `targets.yaml`, and every `target_pct` occurrence repository-wide were inspected.
6. **Authority sweep.** Every occurrence of "endpoint authority" across `governance/decisions/` was read.

**Result of step 2, stated exactly because it is the single most decisive fact in this filing.** Across the
21 frozen §C.2 sources there are **zero true numeric scalars**. There are **48 numeric-valued strings,
every one a `schema_version` value (`'1.0'`); 28 of those occur in
`intelligence/valuation_results/COHORT_MANIFEST.yaml`**, which carries its own plus one for each of its 27
cohort entries, the remaining 20 sources carrying exactly one each. Excluding schema, version, hash, and
count metadata, the frozen non-RISK snapshot contains **zero numeric endpoint-bearing values of any
kind.** Step 3 returned four percent-like prose hits, all in
`GLD_DEFENSIVE_ROLE.yaml`, all inside evidence-gap and provenance narrative — one of them a quotation of
CLAUDE.md's own "~5% margin cost" sector-audit remark — and none a statement of any share.

This is materially stronger than "no source states a sleeve share." There is no number in the frozen
non-RISK snapshot that could be a candidate endpoint value at all, whatever test were applied to it.

**A correction to an assumption a reader may carry from XASSET-0024 §F Limb 1.** That table names ETF
`expense_ratio_pct` values (GLD `0.4`, SPY `0.0945`, VEA `0.03`, VWO `0.06`) among the wrong-quantity
candidates. Those values live in `intelligence/etf_classification/`, which is **not** in the frozen
snapshot; the snapshot's fund economics rows are `intelligence/instrument_economic_assessment/`, which
this session verified carry no numeric scalar at all. XASSET-0024 §F is correct that such values are
wrong-quantity; this filing records additionally that they never reach T1 because they fail T8 first.
Nothing in XASSET-0024 is wrong; one firewall limb is simply not the binding one for those values.

### F. False-candidate firewall results

Every class the authorizing scope named was tested and is recorded, including those that returned nothing,
so that "rejected" is verifiable rather than assumed.

| Candidate class | Located? | Exact location and verified content | First failing criterion | Also fails |
|---|---|---|---|---|
| Historical `18.67 / 14.67 / 16.67 / 16.67` provisional targets | **Yes** | `numeric_sizing/{equity,fund_broad_market,fund_gld_defensive,crypto}.yaml` `provisional_target_pct`; and `pre_registration.yaml` `historical_reference_scenarios.values_pct` | **T3** (N7 barred origin; XASSET-0020 §M names these values) | T2, T5, T6; T8 for the `numeric_sizing` copies |
| `33.32` residual and `66.68` assigned sum | **Yes** | `numeric_sizing/COHORT_MANIFEST.yaml` `unsized_reserved_capital_pct`, `sum_of_assigned_targets_pct` | **T3** (N5 residual/plug; §M names `33.32`) | T2, T5, T8 |
| `16.67` starting baseline (historical six-way equal division) | **Yes** | `numeric_sizing/*.yaml` `starting_baseline_pct` | **T3** (N7 and XASSET-0021 §F equal division) | T2, T5, T8 |
| Freshly recomputed equal split (one quarter across four sleeves) | Constructible | Not present in the corpus | **T3** (XASSET-0021 §F equal division; XASSET-0024 §F Limb 2 reaches constructions no literal scan matches) | T1 origin, T2 |
| Fixed adjustment increment `2.00` | **Yes** | `numeric_sizing/{equity,fund_broad_market}.yaml` `magnitude_pct` | **T3** (§M fixed adjustment increment) | T1, T2, T5, T8 |
| RISK LOWER / HIGHER scenario magnitudes | **Yes** | `pre_registration.yaml` `scenario_magnitudes.values_pct`; source-declared `unit: PERCENT_OF_UNSPECIFIED_ASSET_STATE_EXPOSURE`, `portfolio_reconciliation: NOT_PERFORMED`, `residual_assignment: PROHIBITED` | **T1** (denominator is unspecified **by the source itself**) | T3 (`SYMMETRIC_RELATIVE_PERTURBATION` off a barred anchor), T4, T5, T7 |
| `RELATIVE_PERTURBATION` and the other 19 consequential parameters | **Yes** | `pre_registration.yaml` `consequential_parameter_registry`, all 20 read individually | **T5** (every row `valid_for_study_id: RISK-0001`; **no row's `binding_scope` is sleeve-share sizing**) | T7 (all 20 `lapse_condition: AUTHORIZED_STUDY_COMPLETION`, met, and all 20 reuse-barred absent new authority — `reuse_rule: NEW_GOVERNANCE_AUTHORITY_REQUIRED` on nineteen, `REVALIDATE_CONVENTION_UNDER_NEW_AUTHORITY` on `DFF_DAY_COUNT_DENOMINATOR`), T1, T2 |
| Gold peer-admission thresholds `0.995` / `0.50` / `2.00` | **Yes** | Same registry; `binding_scope: CONDITIONAL_GOLD_PEER_ADMISSION`, `evidence_status: NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED` | **T5** (admission question, not share) | T1, T4, T7 — the three-way failure XASSET-0023 §H.4 item 5 records |
| Study tolerances in `PERCENTAGE_POINTS_OF_UNSPECIFIED_ASSET_STATE` (`LOSS_CONTRIBUTION_TOLERANCE_PP` `1.00`, `OPPORTUNITY_CONTRIBUTION_TOLERANCE_PP` `1.00`, `RECOVERY_BURDEN_TOLERANCE_PPDAYS` `30.00`) | **Yes** | Same registry | **T1** (unspecified asset state; metric tolerances, not shares) | T5, T7 |
| R2 / R3 historical constructs | Referenced | Barred by name at XASSET-0020 §M; `pre_registration.yaml` records `inherited_from_xasset_0016_r2_r3: False` | **T3** (N7) | T2, T5 |
| Current targets `equity 63.25 / fund 27.0 / crypto 4.0 / reserve 4.0 / cash 1.0` | **Yes** | `targets.yaml` `destination[]`, aggregated this session | **T3** (N7 current targets; §M contamination) | T1 (current-target denominator; `fund` does not split the two fund sleeves), T2, T5, T8 |
| Cluster caps `semis 25.0`, `power_infra 20.0`, `oil 20.0` | **Yes** | `targets.yaml` `caps.clusters` | **T2 / Limb 4** (CONSTRAINT — may clip, never originate) | T1 (sub-equity cluster, not sleeve), T8 |
| 8% issuer and 40% common-driver no-add ceilings | **Yes** | `issuer_lookthrough.yaml` mechanism | **T2 / Limb 4** (CONSTRAINT) | T1, T8 |
| ETF `expense_ratio_pct` | **Yes** | `intelligence/etf_classification/*.yaml` | **T8** (outside the frozen snapshot) | T1 (within-fund denominator), T2 |
| ETF internal country/sector weights; crypto dominance / supply / staking / venue percentages | Not present as scalars in snapshot | Snapshot instrument records carry no numeric scalar | **T2** (XASSET-0020 §F.2 marks these DISCLOSURE at Level 1) | T1, T9 |
| Equity valuation price ranges, discount rates, scenario probabilities | **Yes** | `intelligence/valuation_results/`, per-company | **T1** (per-share, no accepted Level-1 aggregation) | T2 (DISCLOSURE at Level 1), T8 |
| Margin, leverage, buffer values (1.8x cap, 30% floor) | **Yes** | `targets.yaml` `margin`, CLAUDE.md doctrine | **T1** (§C excludes debt, leverage, and buffer state from the denominator entirely) | T2, T8 |
| Chart / technical values | **None found** | No chart-derived numeric enters any Level-1 source | **T2** | T8 |
| Arbitrary midpoint; residual calculation; analyst or expert judgment; score / optimizer / grid / sweep result | Constructible | Not present | **T3** (N4, N5, N8; XASSET-0020 §M) | T4, T6 |
| Any decision's own prose value | **None found** | No accepted decision states a sleeve share | **T3** (N8 — expressly including this decision's prose) | T2 |

**No barred number was rehabilitated on the strength of a correct denominator.** The `18.67` family is the
worked case: it is the right quantity in the right units at the right level — XASSET-0024 §F Limb 2 says so
— and it is rejected here on origin, exactly as that limb requires. `pre_registration.yaml` reinforces this
independently in its own governed content, labelling those values `HISTORICAL`,
`COMPUTATIONALLY_DERIVED_UNDER_SUPERSEDED_MECHANICS`, `PROVISIONAL`, `ECONOMICALLY_UNVALIDATED`,
`NOT_ADOPTED`, `NOT_BASELINE_POLICY`, `NOT_A_TARGET`, `NOT_AN_OPTIMIZATION_ANCHOR`, and
`NO_RESIDUAL_ASSIGNMENT`. The source disqualifies them on its own terms.

### G. The competent-authority finding, separately stated

Every occurrence of "endpoint authority" in `governance/decisions/` was read this session. **Every one is a
statement of its absence or its withholding**: XASSET-0021 §F ("The frozen snapshot contains no such
Level-1 endpoint authority for any sleeve"), §O (naming it a later reopen path), XASSET-0022 §§P and R
(mechanically enforcing its absence), XASSET-0023 §H.2 item 3, and XASSET-0024 §L. **No accepted decision
anywhere grants Level-1 endpoint authority to any body, source, or record.**

T5 therefore fails universally, independently of T1 through T4 and T6 through T10, and independently of
what evidence exists. Even a source that stated the §C quantity perfectly would fail, because no authority
competent to fix a Level-1 sleeve share is in force. This is worth stating separately because it is the
one criterion no evidence-production effort can satisfy.

### H. Per-sleeve, per-bound result matrix

The vocabulary is the closed set: `QUALIFIES_UNDER_EXISTING_AUTHORITY`, `CANDIDATE_EXISTS_AUTHORITY_GAP`,
`CANDIDATE_EXISTS_REPRESENTATION_GAP`, `CANDIDATE_EXISTS_OTHER_ADMISSIBILITY_GAP`, `NO_CANDIDATE_FOUND`,
`UNABLE_TO_DETERMINE`.

| Sleeve | Bound | Qualifying source? | Source identity | Route | NUM class | Authority competence | Representation state | Result |
|---|---|---|---|---|---|---|---|---|
| `equity` | LOWER | No | None | None available | N/A | None in force (§G) | Not reached — CM-14 would block | `NO_CANDIDATE_FOUND` |
| `equity` | UPPER | No | None | None available | N/A | None in force | Not reached — CM-14 would block | `NO_CANDIDATE_FOUND` |
| `fund_broad_market` | LOWER | No | None | None available | N/A | None in force | Not reached — CM-15 would block | `NO_CANDIDATE_FOUND` |
| `fund_broad_market` | UPPER | No | None | None available | N/A | None in force | Not reached — CM-15 would block | `NO_CANDIDATE_FOUND` |
| `fund_gld_defensive` | LOWER | No | None | None available | N/A | None in force | Not reached — CM-16 would block | `NO_CANDIDATE_FOUND` |
| `fund_gld_defensive` | UPPER | No | None | None available | N/A | None in force | Not reached — CM-16 would block | `NO_CANDIDATE_FOUND` |
| `crypto` | LOWER | No | None | None available | N/A | None in force | Not reached — CM-17 would block | `NO_CANDIDATE_FOUND` |
| `crypto` | UPPER | No | None | None available | N/A | None in force | Not reached — CM-17 would block | `NO_CANDIDATE_FOUND` |

**Why every cell is `NO_CANDIDATE_FOUND` rather than a gap category, stated precisely because the
distinction carries the whole outcome.** A gap result would mean a source of the right quantity exists and
is held back by a closeable governance condition. No such source exists. Every right-quantity value located
anywhere in the corpus (§F) fails at **T3, barred origin** — a categorical bar that no future authority can
lift, since XASSET-0020 §M places those values beyond "future input authority" and a filing purporting to
readmit them would be performing the barred act rather than authorizing it. Every remaining candidate fails
at T1 or T2, which are properties of what the evidence measures, not of who may certify it. The frozen
snapshot separately contains no numeric scalar at all. The failure is absence and prohibition, not a
missing permission.

**Uniformity is itself a finding.** The eight cells are identical because the binding failures — no
DRIVER-classified magnitude anywhere, no competent authority anywhere — are structural and common to all
four sleeves. Nothing here favours, disfavours, or advances any sleeve relative to another.

### I. Overall outcome

**Outcome: C — `NO_QUALIFYING_ENDPOINT_SOURCE_IN_ACCEPTED_CORPUS`.**

No accepted source presently supplies a qualifying Level-1 sleeve-share LOWER or UPPER bound for any
sleeve. The determination rests on five independently sufficient grounds, each verified directly this
session rather than cited from a prior filing:

1. **No candidate value exists in the frozen non-RISK snapshot.** All 21 §C.2 sources contain zero true
   numeric scalars; their 48 numeric-valued strings are `schema_version` values without exception; and no
   percent-bearing prose states a share (§E).
2. **The snapshot's classifications forbid it independently.** XASSET-0021 §C.2 marks every non-RISK row
   DISCLOSURE-only for current preference or an uncomputed interface, and XASSET-0020 §F.2's
   forbidden-implication column bars the DRIVER-capable classes from implying "size or preference," "a
   sleeve weight," or "a target anchor, increment, weight, or automatic preference" — so even a
   DRIVER-classified snapshot source could not carry a magnitude (T2).
3. **The RISK corpus's numbers fail on their own governed terms.** All four family results are
   `unable_to_determine`; the only sleeve-share-shaped values are self-declared `NOT_A_TARGET`; the
   scenario magnitudes' own declared unit is `PERCENT_OF_UNSPECIFIED_ASSET_STATE_EXPOSURE`; and none of the
   20 consequential parameters has a sleeve-share `binding_scope`, all being `valid_for_study_id:
   RISK-0001`, lapsed, and reuse-barred (T1, T5, T7).
4. **Every right-quantity value in the wider corpus is barred by origin** and is outside the snapshot
   besides (T3, T8).
5. **No competent Level-1 endpoint authority exists anywhere** (§G, T5).

Outcomes A, B, and D were each tested and rejected. **A** requires a source passing every existing-authority
test; none passes any of T1, T2, T3, or T5, let alone all ten. **B** requires a serious correct-quantity
candidate blocked by a closeable governance condition; the correct-quantity values that exist are blocked
by categorical origin bars and by absence of DRIVER-classifiable magnitude, neither of which a governance
filing can close, and treating them as "candidates awaiting authority" would invite exactly the
rehabilitation XASSET-0024 §F Limb 2 exists to prevent. **D** would be abstention as a substitute for
searching; the corpus was searched and the finding is definite.

This is the consequential null the program needed. It converts the next step from "find the authority for
evidence we have" into "produce evidence that does not yet exist, and obtain competent authority over it."
Both are missing, and they are **distinct requirements** rather than one. **Accepted authority does not
settle their mandatory ordering or packaging**, and this filing does not settle it either — see §O.5.
Neither is performed or authorized here.

### J. Whether the next research question can remain sleeve-agnostic

It cannot remain fully sleeve-agnostic, and the reason is doctrinal rather than practical.

XASSET-0020 §E.1's six DRIVER classes are each defined **on a sleeve or on a sleeve pair**:
`portfolio_function` is "the sleeve's directly evidenced job"; `valuation_opportunity_cost` concerns "the
marginal dollar here rather than to the direct alternative"; `downside_path_risk` and `recovery` require
"directly comparable" evidence; `diversification_cobehavior` is "direct pair evidence"; and
`sleeve_deployability` is "sleeve-level convertibility, lockup, or implementation friction." There is no
sleeve-independent DRIVER class. Since T2 requires DRIVER classification on the source's own subject
matter, any admissible endpoint-supporting evidence is necessarily sleeve-specific or pair-specific in its
content.

The **question form** can and should be stated sleeve-agnostically, as a template applying identically to
whichever sleeve is later authorized. The **evidence** cannot be.

**No first sleeve is selected here, and none is compelled.** One genuine asymmetry was found and is
recorded rather than acted on: `GLD_FUNCTION`
(`intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml`) is the only §C.2 row whose source-owned
currentness state is `current` at the snapshot, every other row lacking a governed currentness rule. That
makes `fund_gld_defensive` the only sleeve with a snapshot source that is not automatically
freshness-blocked. It does **not** compel selection: XASSET-0021 §C.2 states in the same row that the
source "cannot establish relative preference or an endpoint," XASSET-0020 §F.2 forbids it from proving "a
sleeve weight," and it carries no numeric value of any kind. Choosing a sleeve because one of its sources
happens to pass a criterion that no source passes overall would be selection by convenience, which
XASSET-0024's own Alternatives Considered rejected in terms. Sleeve selection remains a separate, later,
explicitly authorized act.

### K. The smallest exact future research question

Recorded because the outcome is C, and stated as a question only. **This is not a research charter, and
this filing commissions nothing.** A charter would additionally require a justified research design, a
protocol, pre-registration, provenance rules, trial bounds, and its own authorization — none of which is
performed or authorized here.

> **For one named Level-1 sleeve, is there directly evidenced, question-matched economic content —
> admissible as a DRIVER under exactly one of XASSET-0020 §E.1's six classes on its own subject matter —
> that intrinsically establishes a LOWER or an UPPER limit on that sleeve's share of one normalized unit of
> prospective unlevered asset-side capital, at exact precision, from a single origin, with no step whose
> coefficient, ordering, tolerance, cutoff, or selection could have been chosen differently?**

The question is deliberately shaped so that the following cannot answer it, since each is the failure mode
a naive framing would invite:

- **Wrong denominators** — the quantity is fixed to §C's normalized unlevered asset-side unit, excluding
  debt, leverage, buffer state, within-fund composition, market composition, and per-share valuation.
- **Historical anchors** — "intrinsically establishes" excludes any value carried forward from
  `18.67 / 14.67 / 16.67`, the `33.32` residual, the six-way baseline, RISK reference scenarios,
  XASSET-0016/0018 output, or current targets.
- **Optimizer or score construction** — the final clause is XASSET-0023 §H.3 item 7's operational test
  stated as an admission requirement, so a swept, tuned, or fitted value fails at the point of asking.
- **Arbitrary diversification convention** — "directly evidenced" and "on its own subject matter" exclude
  equal division, symmetry, midpoints, and default range widths.
- **Current portfolio incumbency** — no current holding, weight, tier, gate, or target may enter.
- **Lapsed RISK parameters** — "admissible" incorporates T5 and T7, which every RISK parameter fails on its
  own recorded `reuse_rule` and met `lapse_condition`.
- **Hidden analyst preference** — "from a single origin" with "no step that could have been chosen
  differently" is uniqueness plus zero discretion, and NUM-0001 class 4 or 5 additionally requires the
  selection to have already been made upstream by a competent authority (XASSET-0024 §E.2).

**A null answer to this question is a complete outcome.** If no such evidence is producible for a sleeve,
that is a governed finding under XASSET-0020 §J.3, not a defect to be patched.

**Sequencing carried forward unchanged.** XASSET-0024 §H's RANGE-first determination stands: the POINT
route's additional blocker is RISK pair determinacy, which no endpoint research can address and which the
consumed RISK-0001 authority cannot supply. A future unit should establish RANGE feasibility first unless
its evidence uniquely supplies a point.

### L. Representation-gap interface

Recorded only as to whether each gap would block a candidate. This filing **does not** define equity
aggregation, choose among SPY / VEA / VWO, resolve GLD / IAU / SGOL / GLDM, build any crypto composite, or
vote, average, or weight across representations. Representation methodology remains separate authority, and
XASSET-0023 §H.5 records that no Level-1 cross-representation aggregation or selection rule "exists
anywhere at Level 1."

| Gap | Issue | State | Would it block a candidate? |
|---|---|---|---|
| CM-14 | `equity_representation_and_level1_valuation_aggregation` | `APPLICATION_MUST_ABSTAIN` | **Yes**, for any `equity` candidate not self-contained under XASSET-0024 §G path 1 |
| CM-15 | `fund_broad_market_representation_sensitivity` | `APPLICATION_MUST_ABSTAIN` | **Yes**, on the same terms |
| CM-16 | `fund_gld_defensive_representation_sensitivity` | `APPLICATION_MUST_ABSTAIN` | **Yes**, on the same terms |
| CM-17 | `crypto_representation_sensitivity` | `APPLICATION_MUST_ABSTAIN` | **Yes**, on the same terms |

**The representation gate was not reached in this determination.** Every sleeve failed earlier, at T1, T2,
T3, or T5. CM-14 through CM-17 are therefore recorded as *latent* blockers on any future candidate, not as
the operative cause of any result above. A future candidate escapes them only by XASSET-0024 §G path 1
(self-contained) or path 2 (a separately accepted rule); otherwise abstention is mandatory. These four rows
are unchanged by this filing.

### M. Schema and application roadmap

Recorded mechanically. None of these steps is performed, authorized, scheduled, or partially granted here,
and the list creates no entitlement to any of them.

A future non-null Level-1 application will still require, as applicable and in dependency order:

1. accepted endpoint-supporting evidence satisfying XASSET-0024 §J.1–§J.12;
2. a competent Level-1 endpoint authority, separately filed, reviewed, and accepted — and for a NUM-0001
   class 4 or class 5 bound, one that has itself made and recorded the selection with §7's complete triple;
3. representation closure, whether by self-contained sources or by a separately accepted Level-1
   aggregation or selection rule;
4. a lawful XASSET-0021 snapshot successor admitting that evidence;
5. an endpoint-capable XASSET-0022 schema and generator successor;
6. an application authorization populating `APPLICATION_AUTHORIZATION_REGISTRY`; and
7. the application itself.

### N. Effect on the closure matrix and application authority

No XASSET-0021 §N row is reclassified. The matrix stands exactly as accepted at 14
`CLOSED_DETERMINISTICALLY` / 14 `APPLICATION_MUST_ABSTAIN` / 2 `SEPARATE_PREREQUISITE_REQUIRED`, with
`application_time_author_or_reviewer_judgment_remaining: 2`. CM-14 through CM-19, CM-25, and CM-26 remain
`APPLICATION_MUST_ABSTAIN`; this filing supplies no endpoint and changes nothing about them.

**Application authority remains WITHHELD.** XASSET-0021 §O's double gate is untouched, XASSET-0022 §P's
mechanical enforcement is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, and no
`intelligence/level1_application/` artifact exists or is authorized. No all-abstention application is
authorized either. Nothing in §§C–M may be read as granting, implying, scheduling, or partially granting
application authority.

### O. Recorded rather than resolved

**O.1 — Outcome C is not conditional on XASSET-0024 §K.1's open reading.** XASSET-0024 recorded that its
Outcome A depends on reading XASSET-0020 §E.1's six DRIVER classes as subject-matter classes capable of
housing a magnitude statement, and that the contrary reading would make its outcome B. This filing's
outcome is stable under **both** readings: under the subject-matter reading no admitted source states a
magnitude, and under the preference-only reading no admitted source could. §K.1 remains open and is neither
resolved nor relied upon here.

**O.2 — The bar this filing applies is existing authority, not permanent impossibility.** Outcome C is a
statement about the accepted corpus as it stands today. XASSET-0024's Outcome A — that the methodology
permits an endpoint in principle — is unaffected and unedited. The two findings are complementary: the
route exists; nothing is currently on it.

**O.3 — Absence of evidence, distinguished from evidence of absence.** That no qualifying source exists
does not establish that no such evidence could be produced. §K states the question that would test it. This
filing takes no position on whether that question is answerable, cheaply or at all.

**O.4 — Not reopened here.** XASSET-0023 §G's Level-2 subset question; §J.1's XASSET-0021 §O
strict-conjunction tension; §J.2's gold-representation labelling difference; and XASSET-0024 §K.2's
circularity discussion. None bears on any determination above, and none is resolved.

**O.5 — The ordering and packaging of the next lifecycle is UNRESOLVED, and is not settled here.** This
filing determines that two things are missing — qualifying endpoint evidence and competent Level-1
endpoint authority — and that they are **distinct requirements**. It does **not** determine which must be
acquired first, nor whether they must always be obtained through separate filings or lifecycles.

Accepted authority does not fix either point. XASSET-0024 §J is titled "Minimum evidence properties for
the next research **or authority** unit," expressly contemplating either as next. XASSET-0024 §I states
the gap conjunctively — "a qualifying source **and** a competent authority" — and describes the next
unit's work as "sourcing and authority," without ordering them. XASSET-0021 §O lists evidence admission
and endpoint authority together and fixes no sequence between them. And XASSET-0024 §K.2 draws its
distinction between **governance-time and application-time** discretion, not between one filing and two;
its NUM-0001 class-4 and class-5 route expressly contemplates a competent authority's own governed record
being the thing an application later reads, which is why §M item 2 lists that possibility rather than
excluding it.

Accordingly: the two requirements **may** ultimately need separate lifecycles, **or** may lawfully be
combined if a future, explicit authority permits a single governance record both to carry qualifying
governed content and to supply competent endpoint authority — provided that record independently satisfies
NUM-0001 provenance, evidence admission under XASSET-0020 §F.1, XASSET-0024 §J.1–§J.12, the §E.3
anti-discretion test, and every independence and scope requirement those impose. **No such combination is
authorized by this filing, and no packaging is preferred, recommended, or prescribed by it.** The exact
sequence and packaging must be determined by the next explicitly authorized governance unit, on its own
authority.

### P. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files: this decision; `governance/decisions.yaml` (one catalog
row); `operations/WORKSTREAMS.yaml` (additive XASSET-0024 post-merge closeout and XASSET-0025 lane facts,
every prior gate's own text byte-unchanged); and `test_portfolio_hq_dashboard_decisions.py` (the two
mechanical decision-count assertions, 126 → 127).

No supporting artifact is created. This is a governance determination, not a research result, and its
complete reasoning and citations are contained here — matching XASSET-0021 through XASSET-0024, each of
which carried comparable analytical weight with `supporting_artifact: null`. No Intelligence, research,
schema, generator, validator, allocator, target, holding, gate, margin, chart, ladder, or protected
portfolio file is changed.

### Q. Reopen triggers

Reopen XASSET-0025 if: XASSET-0019's, XASSET-0020's, XASSET-0021's, XASSET-0022's, XASSET-0023's, or
XASSET-0024's effective identity changes; XASSET-0020 §E.1's driver classes, §F.2's source registry, or
§L's endpoint row is amended; any XASSET-0021 §C path or hash changes, or the snapshot is lawfully replaced
or extended; a Level-1 endpoint authority is granted to any body or record; a candidate endpoint source is
proposed and its §D compliance must be assessed; a Level-1 cross-representation aggregation or selection
rule becomes accepted; separate governance grants reuse authority over any lapsed RISK parameter, or a new
RISK study is chartered; NUM-0001's classes, §7 requirements, or §8 standards change; a reviewer
establishes XASSET-0024 §K.1's contrary reading of §E.1; or the liquidity or Level-2 architecture changes a
boundary relied on here.

### R. Absolute non-authorization

This decision creates no endpoint, bound, point, range, percentage, weight, target, or allocation, and
selects, prefers, or ranks no sleeve; performs and authorizes no research, endpoint research, data
acquisition, backtest, evidence admission, direct-pair study, representation study, or RISK study;
commissions no research charter and defines no research design; produces no evidence conclusion or
historical anchor; grants no endpoint authority, no evidence-admission authority, and no application
authority, including for an abstention-only application, and populates no authorization registry; creates
no application artifact or directory; extends, replaces, or amends no XASSET-0021 snapshot; amends no
methodology and supplies no representation rule, equity aggregation, fund or gold peer selection, or crypto
composite; performs no Level-1 sizing and no Level-2 membership or sizing; makes no liquidity
determination; changes no `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
allocator, tier, cluster, cap, or margin state; authorizes no chart, ladder, optimizer, deployment, trade,
order, or brokerage action; adopts no portfolio policy; creates no XASSET-0022 schema or version successor;
grants no reuse authority over any lapsed RISK parameter or result and no authority to re-question any RISK
family; accesses, reruns, refreshes, or reuses no RISK-0001 execution artifact; edits no accepted decision;
and rewrites no accepted history.

## Rationale

XASSET-0024 established that the methodology permits an endpoint and told the next unit its work is
"sourcing and authority, not methodology reform." That is directionally right and materially incomplete,
because "sourcing and authority" names two very different tasks whose costs differ by an order of
magnitude. Obtaining authority over evidence that already exists is a governance filing. Producing evidence
that does not exist is a research program with a charter, a protocol, pre-registration, and execution. A
unit that began work without knowing which one it faced would either commission unnecessary research or,
worse, discover mid-flight that the evidence it assumed it had was barred — which is a recognizable version
of the failure PR #309 already paid for.

The determination is therefore worth making even though its answer is a null, and arguably *especially*
because its answer is a null. A null that is verified is cheap certainty; a null that is assumed is a
liability.

The single most useful finding is the one that required actually parsing the sources rather than reading
their classifications. XASSET-0023 §H.8 concluded the test fails for the snapshot on classification
grounds — every row is DISCLOSURE-only. That is correct and sufficient for its purpose, but it leaves open
a reading in which the snapshot is full of usable numbers held back by a labelling decision that a future
authority might revisit. It is not. All 21 non-RISK snapshot sources contain, between them, twenty-one
numeric scalars, and every one is a `schema_version`. There is nothing behind the classification. A future
unit hoping to unlock the snapshot by supplying an authority would find nothing to authorize.

The distinction between Outcome B and Outcome C carried the whole filing and deserved the care it got. B is
the comfortable answer: the corpus does contain sleeve shares of the normalized whole in exactly the right
units, and calling them "candidates blocked by a governance gap" would be superficially defensible and
would leave a tidy next step. It would also be wrong, and wrong in the specific direction this program has
spent four decisions guarding against. Those values are barred by origin, and an origin bar is not a gap —
it is a conclusion. XASSET-0020 §M places them beyond "future input authority," and a filing that
readmitted them would be performing the barred act rather than authorizing it. `pre_registration.yaml`
says the same thing in its own governed content, labelling them `NOT_A_TARGET` and
`NOT_AN_OPTIMIZATION_ANCHOR`. Recording C rather than B is the difference between a next unit that goes
looking for evidence and one that goes looking for a signature.

Stating the competent-authority finding separately, at §G, was a deliberate structural choice. T5 fails
universally and for a reason no research can fix, so a reader who takes away only that "the evidence is
missing" would under-scope the next lifecycle. Evidence and authority are two distinct requirements, not
one. How they must be packaged is a different question, and one this filing deliberately does not answer:
XASSET-0024 §K.2 draws its line between governance-time and application-time discretion, not between one
filing and two, and its class-4 route expressly contemplates an authority's own record carrying the
governed content an application later reads. §O.5 records the packaging as unresolved rather than
resolving it, because a filing that disclaims creating anything should not narrow a future unit's lawful
option set as a side effect of describing a gap.

Finally, the sleeve-agnosticism question had a real answer rather than a procedural one. Every one of
XASSET-0020 §E.1's six DRIVER classes is defined on a sleeve or a pair, so admissible evidence is
necessarily sleeve-specific — a constraint the next unit needs to know before it designs anything. The
`GLD_FUNCTION` currentness asymmetry is genuine and was found by inspection rather than assumed away, and
recording it while expressly declining to act on it is the honest treatment: it is a fact about the
snapshot, not a reason to pick a sleeve, and the same row that establishes it also states that the source
cannot establish an endpoint.

## Alternatives Considered

- **Determine Outcome B, treating the `18.67` family or the RISK reference scenarios as candidates blocked
  by an authority gap.** Rejected, and this was the substantive call in the filing. Both fail at barred
  origin, which is categorical rather than closeable, and `pre_registration.yaml` disqualifies its own
  values in its own governed content. Framing them as candidates would invite precisely the rehabilitation
  XASSET-0024 §F Limb 2 was written to prevent, and would hand a future unit a next step that does not
  lawfully exist.
- **Determine Outcome A on the strength of `GLD_FUNCTION`'s `current` state.** Rejected. It is the only
  snapshot row with a governed currentness rule, but it contains no numeric value, XASSET-0021 §C.2 states
  it "cannot establish relative preference or an endpoint," and XASSET-0020 §F.2 forbids it from proving a
  sleeve weight. Currentness is one criterion of ten.
- **Determine Outcome D, `UNABLE_TO_DETERMINE`.** Rejected. The corpus was searched by field-name
  enumeration, exhaustive numeric extraction, prose scanning, and parameter-level inspection, and the
  finding is definite in both directions — what exists, and what does not. Abstaining would have been
  abstention as a substitute for searching.
- **Rely on XASSET-0023 §H.8's existing finding instead of re-deriving it.** Rejected. §H.8 covers the
  snapshot only and reaches it through classification. This filing's question extends to the whole accepted
  corpus and needed to distinguish "classified out" from "not present," which only direct inspection can
  do. The two findings agree; this one is stronger and independently reached.
- **Extend the frozen snapshot so that a candidate could be assessed on its merits.** Rejected and
  expressly barred by the authorizing scope. Snapshot extension is its own authorization with its own
  review, and performing it inside an identification unit would be an amendment smuggled into a search.
- **Write the research charter in the same filing, since the outcome is C.** Rejected. §K identifies the
  exact question; a charter additionally requires a research design, protocol, pre-registration, provenance
  rules, and trial bounds, resting on a different evidentiary basis than reading accepted text.
- **Name a first sleeve to make the future charter concrete.** Rejected. No accepted evidence compels one,
  the eight-cell matrix is uniform, and selecting on the `GLD_FUNCTION` asymmetry would be selection by
  convenience — the alternative XASSET-0024 rejected in the same terms.
- **Create a supporting audit artifact for the search.** Rejected. The search coverage (§E), the firewall
  results (§F), and the matrix (§H) are the determination itself, and XASSET-0021 through XASSET-0024 each
  carried comparable weight with `supporting_artifact: null`.

## Consequences

The next unit now knows, before spending anything, that the accepted corpus contains no qualifying Level-1
endpoint source for any sleeve, on either bound; that the frozen non-RISK snapshot contains no
endpoint-bearing numeric value at all, so no authority-granting filing could unlock it; that every
right-quantity value in the wider corpus is barred by origin rather than held back by a closeable gap; and
that no competent Level-1 endpoint authority exists anywhere, so qualifying evidence and competent
authority are two distinct requirements — whose mandatory ordering and packaging accepted authority does
not settle, and which this filing leaves expressly unresolved at §O.5.

It knows the exact question new evidence would have to answer (§K), why that question cannot be answered
sleeve-agnostically even though it can be stated that way (§J), which four representation gaps would block
any future candidate that is not self-contained (§L), and the seven-step chain any eventual application
must still complete (§M).

Nothing about the portfolio changes. Application authority remains withheld, the closure matrix stands at
14 / 14 / 2, the authorization registry remains empty, no application artifact exists, the XASSET-0021
snapshot is unextended and byte-verified intact, and no endpoint, range, percentage, weight, target,
allocation, or trade is created, recommended, or authorized. XASSET-0019 through XASSET-0024, NUM-0001,
LEVEL2-0001, the RISK corpus, `intelligence/`, `research/`, and every protected portfolio file are
byte-unchanged.
