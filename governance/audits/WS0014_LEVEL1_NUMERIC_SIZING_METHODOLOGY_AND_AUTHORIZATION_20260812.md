# WS-0014 Level 1 Numeric Sleeve-Sizing Methodology and Bounded Authorization

**Date**: 2026-08-12
**Governing decision**: `governance/decisions/XASSET-0016-ws0014-level1-numeric-sizing-methodology-and-authorization.md`
**Status**: Methodology design plus a bounded future-implementation authorization. No numeric
Level 1 target is computed, populated, or implied by this artifact or its governing decision. No
`targets.yaml`, `holdings.yaml`, or allocator change of any kind. No allocation check.

**Bounded correction (same PR, same day), independent exact-head review
`pullrequestreview-4916420679` (anchored to the original head
`f92be3fc3e66237f840e0c70baf156f56ba1d194`), 0 BLOCKING / 1 MAJOR / 1 MINOR / 3 non-actionable
NOTE, CHANGES REQUIRED — resolved by this correction.** **MAJOR**: the original §9 defined a
closed evidence category list and an explicit anti-formula prohibition, but left the actual
transformation from evidence to a specific `provisional_target_pct` value entirely to undocumented
"governance judgment... disclosed in free text" — no reproducible derivation mechanism existed, so
two independent future implementation sessions given identical sealed evidence could reach
materially different figures with no reconcilable reason. **Resolved**: §9 is replaced with a
seven-step ordered, closed, deterministic derivation procedure (§§9.1-9.7) — a zero-based equal-
share starting point over the full six-sleeve taxonomy (§9.2, never the eligible subset, never a
historical `targets.yaml` anchor), three named, closed, evidence-triggered adjustment rules
(§9.3, explicitly addressing Axis-A-completeness, relative relationship-coverage strength, and
relative secondary-condition/overlap breadth, with valuation and crypto per-coin evidence
explicitly excluded as disclosure-only), a single fixed `NUM-0001` class-5 increment applied per
firing trigger rather than a tuned or continuously-variable formula (§9.4), a mandatory
determinism and comparative-consistency check (§9.7), and a strengthened, self-contained
justification for a single provisional point over a range (§9.9) — plus new output-schema
provenance fields (§8: `starting_baseline_pct`, `applied_adjustments[]`, `governing_rule_ids[]`,
`comparative_consistency_note`), eight new future-validator/test items (§19 items 17-24, including
a full live-rederivation requirement and the review's own two named MINOR adversarial tests), and
a fictional-constant synthetic walkthrough (§21) demonstrating the mechanism's determinism without
computing, stating, or implying any real sleeve's actual figure. **MINOR**: the future validator
spec did not explicitly name adversarial tests for a pre-floor `sum_of_assigned_targets_pct`
exceeding `100.00` or a stored negative `unsized_reserved_capital_pct` — **resolved** by §19 items
20-22, both now explicitly named alongside additional neighboring-arithmetic cases (exact `100.00`,
`100.01`, zero residual, negative residual, excess precision, rounding drift). All three
non-actionable NOTEs (the weight `unsized_reserved_capital_pct` may carry in practice; the
single-point-vs-range justification resting on the class-5 label alone; an immaterial YAML-count
discrepancy in the reviewing session's own reproduction) are carried forward exactly as the review
itself characterized them — the first two are directly addressed as part of resolving the MAJOR
(§9.9's strengthened, self-contained justification; §19's cash-conflation scan, unchanged in
substance but now sitting alongside a materially stronger derivation mechanism for the reviewer's
own next-round scrutiny); the third does not bear on this filing's own committed content. No Stage
4 policy outcome, no eligibility determination, no `policy_adoption`/`sleeve_profile`/
`sleeve_relationship` record, no Level 2 content, and no actual percentage for `equity`,
`fund_gld_defensive`, or `crypto` is created, computed, or implied by this correction.

**Second bounded correction (same PR, same day), independent exact-head delta review
`pullrequestreview-4916848704` (anchored to the first-correction head
`8b883689fa0599eb590953a21713ad0299b9939f`), 0 BLOCKING / 2 new MAJOR / 0 new MINOR / 5 NOTE,
CHANGES REQUIRED — confirmed the original MAJOR and MINOR above genuinely resolved, and found two
new MAJOR findings, both resolved by this correction.** **NEW MAJOR-A**: R1 ("full Axis-A-basis
coverage") rewarded a sleeve for independently clearing more of the three lawful Axis A evidentiary
bases with a positive numeric adjustment, but neither `XASSET-0014` §3.2 nor any other governing
text ever states that basis-completeness is itself an economic or portfolio-risk reason to hold
**more capital** — Axis A's own `function_confirmed_distinct` value requires only **one** basis to
be fully satisfied (`XASSET-0014` §3, item 1); clearing two or three is evidentiary
**completeness**, i.e. confidence in the classification finding itself, not a distinct, argued case
for a larger provisional figure. The review found this concretely, foreseeably favored only
`fund_gld_defensive` today (the sole sleeve independently clearing all three bases per
`XASSET-0015` §C), for a reason unconnected to any governed risk/opportunity-cost rationale.
**Resolved**: R1 is withdrawn as a numeric trigger. §9.3 now defines **two** named, closed triggers
(R2, R3 — retained under their original identifiers, not renumbered, to minimize churn against
every cross-reference elsewhere in this document and to leave an honest trace that a third trigger
was considered and withdrawn); the Axis-A-basis-completeness fact is retained, unchanged in
substance, as a **disclosure-only** item — the same treatment this procedure already gives
`stronger_evidence_maturity`, Level 2 valuation completeness, and crypto per-coin divergence (§9.3's
own pre-existing exclusion list) — cited in a future record's own `uncertainty_disclosure` field,
never converted into, or read as justifying, a specific number or trigger. **NEW MAJOR-B**: with
R1 withdrawn as a numeric trigger, and independently confirmed even under the original three-trigger
design (R1 was up-only, `{0, +2.00}`, never `{-2.00}` — no governing text ever gave it a "down"
case), the stated theoretical bound `[10.67, 22.67]` (§9.4/§9.5, before this correction) was
arithmetically wrong: the true reachable minimum under the original design was `16.67 - 2.00 -
2.00 = 12.67`, not `10.67`. **Resolved, and simplified by the same fix that resolved NEW MAJOR-A**:
with exactly two symmetric triggers remaining (R2, R3 — each capable of firing `up`, `down`, or not
at all), the corrected, mechanically re-enumerated bound is `[-4.00, +4.00]` percentage points
around the `16.67` baseline, i.e. `[12.67, 20.67]` — independently verified below (§9.4, §9.5) by
enumerating all nine reachable `(R2, R3)` combinations, not assumed or copied from the review.
Every occurrence of the stale bound (`[-6.00, +6.00]`, `[10.67, 22.67]`, `3 x 22.67 = 68.01`) has
been located and corrected throughout this document (§§9.4, 9.5, 19 item 20, 21). The illustrative
R1-only reachability table (former §9.10) is replaced with a short disclosure-only paragraph, since
R1 no longer feeds this procedure's arithmetic and a reachability table for a non-numeric fact
serves no derivation purpose. §21's synthetic walkthrough is rewritten to exercise the corrected,
two-trigger system directly (no-trigger, up/down R2-equivalent, up/down R3-equivalent, a tie, both
triggers combined at the true synthetic minimum and true synthetic maximum) using the same
deliberately fictional labels and constants as before. No Stage 4 policy outcome, no eligibility
determination, no sealed `policy_adoption`/`sleeve_profile`/`sleeve_relationship` record, no Level 2
content, and no actual percentage for `equity`, `fund_gld_defensive`, or `crypto` is created,
computed, or implied by this second correction. **Disposition of all five NOTEs**: NOTE 1
(§9.2's starting-baseline text could more clearly separate "why `targets.yaml` is barred as
evidence" from "why equal-share is itself the right starting shape") and NOTE 2 (no stated
rationale for exactly `2.00` versus a neighboring magnitude) are both **carried forward unchanged,
non-actionable per the review's own characterization** — neither is materially affected by
withdrawing R1. NOTE 3 (R2's and R3's own rationale "could be more explicit" about the risk/
uncertainty logic connecting them to a numeric direction) is **resolved** by strengthened rationale
text added to §9.3 below. NOTE 4 (R2 and R3 are not fully orthogonal — a sleeve's own disclosed
gaps can influence both) is **resolved by explicit disclosure**, added to §9.3 below, that this is
intentional, bounded, and does not read the same raw field twice. NOTE 5 (the R1-only reachability
table, combined with this document's own published baseline/increment constants, let a reader
derive a narrowed *range*, not a point, for a real sleeve) is now **moot** — R1 is no longer a
numeric trigger, so its own reachability fact no longer combines with any published magnitude to
narrow anything; the former table is replaced with a disclosure-only paragraph in §9.10 below that
publishes no comparative or numeric information at all.

**Third bounded correction (same PR, same day), independent exact-head delta review
`pullrequestreview-4917325267` (anchored to the second-correction head
`95556d05d58e235643212c6f5a8814fa14d7fa82`), 0 BLOCKING / 1 fresh MAJOR / 0 fresh MINOR / 1
non-blocking NOTE, CHANGES REQUIRED — confirmed the original MAJOR/MINOR and both round-1 new
MAJOR findings genuinely resolved, and found one fresh MAJOR, resolved by this correction.**
**Fresh MAJOR, described structurally — this banner deliberately does not restate the specific
live counts or derived outcomes the review itself found, to avoid the exact self-defeating error
of republishing leaked information inside its own correction record.** §3's own "Live sizing-status
population" table stated each sizing-eligible sleeve's exact current relationship-coverage input
count (the same field §9.3's own R2 rule reads). The review found that combining those live,
per-sleeve counts with R2's own relative-extreme rule (fires up for the strict, unique fewest such
count among the sizing-eligible population; fires down for the strict, unique most; no fire on a
tie) let a reader of this document alone — no external repository access required — mechanically,
certainly determine R2's real directional outcome for every sizing-eligible sleeve today, which,
combined with this document's own published baseline/increment constants, narrowed each real
sleeve's eventual `provisional_target_pct` from the full five-value reachable set to a real,
certain three-value subset — the identical leakage class the withdrawal of R1's own reachability
table already eliminated (round 2 above), left open here for R2's still-live sibling trigger.
**Resolved**: §3's own table is redacted to categorical Axis A/B/C
disposition plus a citation to the governing gate/case only — no exact pair count, no relative-
extreme characterization, and no secondary-condition-type detail for any sleeve appears anywhere
in the table any longer (§3). A new standing rule, §3.1, generalizes this beyond the one table:
this governance filing must never publish current real trigger-input state for any sizing-eligible
sleeve, on any trigger, anywhere in its own committed content — the future, separately authorized
implementation must derive R2 and R3 live, itself, from the sealed source records. A full-document
audit for the identical leakage class against R3 specifically (not flagged by the review, checked
regardless per this correction's own standing discipline) found no comparable leak — no table or
passage anywhere in this document states a real sleeve's own secondary-condition-type breadth or a
relative-extreme comparison among real sleeves for R3; the only R3-adjacent fact in the former §3
table (a vague, non-quantitative "at least one of two named types" statement for `equity`) has
been removed in the same redaction, out of caution, though it was independently confirmed
insufficient on its own to determine R3's outcome for any sleeve. The single non-blocking NOTE
(the synthetic walkthrough's own seven cases don't include a literal worked "opposite-direction
cancellation to zero" example, though the underlying arithmetic is already proven correct by
§9.4's own nine-combination table) is disclosed, not corrected — it is walkthrough-completeness
only, explicitly characterized by the review itself as non-actionable. No Stage 4 policy outcome,
no eligibility determination, no sealed `policy_adoption`/`sleeve_profile`/`sleeve_relationship`
record, no Level 2 content, and no actual percentage, trigger direction, or adjustment for
`equity`, `fund_gld_defensive`, or `crypto` is created, computed, or implied by this third
correction — this correction is text-removal-and-boundary-addition only, not a redesign of R2, R3,
the baseline, the increment, or the `[12.67, 20.67]` generic theoretical range, all of which remain
unedited and unaffected.

## 0. Purpose and where this sits in the sequence

`XASSET-0014` §H/§15 defined an eleven-condition gate that must hold before numeric Level 1
sleeve-level sizing (`XASSET-0001` §J step 9) may even be authorized to begin, and stated
explicitly that satisfying the gate is "necessary, never sufficient" for a future, wholly
separate, explicitly authorized filing to begin that work. This artifact is that filing's design
layer: it independently re-verifies the gate is satisfied (§1), determines that no numeric-sizing
methodology exists anywhere in the repository to bind to (§2), and — having found none — designs
the smallest defensible methodology plus a bounded authorization for one future implementation to
apply it to the population the gate has already, mechanically, made determinate (§§3-14).

## 1. The eleven-condition gate, independently recomputed against live repository state

Every condition below was checked directly against the sealed records, the validator's own
standalone run, the repository's full test suite, and the GitHub API record of each governing
PR's review/correction/acceptance/merge/CI lifecycle — not inferred from any prior filing's own
narrative summary.

| # | Condition (`XASSET-0014` §15) | Status | Evidence |
|---|---|---|---|
| 1 | `XASSET-0014` itself merged, independently reviewed, principal-accepted | **SATISFIED** | PR #304, merge commit `f3e067fd217ef4ea4800951d663f7c89e0c7d257`. Independent review `pullrequestreview-4909703610` (1 MAJOR, resolved by bounded correction) → delta review `pullrequestreview-4910068104` (0 BLOCKING/MAJOR/MINOR, 2 non-blocking NOTE) → principal acceptance at exact head `ab93baf3e73a7237bae6c673fb45eda26c62a86f` (`issuecomment-5258025672`) → merge-commit CI `93905807614` `completed`/`success`. |
| 2 | A future, separate Stage 4b content-authorization filing has named the exact sleeve population | **SATISFIED** | `XASSET-0015`, PR #305, merge commit `90e12b2ba3441c6b3602b0fd24bc0642a3aa6952`. Independent review `pullrequestreview-4910512608` (0/0/0/2 NOTE) → principal acceptance at exact head `4890b1d2bc65b66c633d450c61a4b82924e938d0` (`issuecomment-5258589687`) → post-merge verification (`issuecomment-5258641077`) → merge-commit CI `93920752502` `completed`/`success`. §B names all six sleeves, none deferred. |
| 3 | A future, separate Stage 4c implementation has populated a record for every authorized sleeve | **SATISFIED** | PR #306, merge commit `0dc3f33c5fa539b2d44fb1579ab23df8cb730a4a` (this session's own starting `HEAD`/`origin/main`). Independently confirmed all six sealed records exist on disk (`intelligence/level1_sleeve_synthesis/policy_adoption/{equity,fund_broad_market,fund_gld_defensive,crypto,cash_reserve,debt_reduction}.yaml`, all `record_status: sealed`) plus `COHORT_MANIFEST.yaml` — no sleeve omitted. |
| 4 | Every sleeve's Axis A/B/C disposition is explicit — no unpopulated or defaulted value | **SATISFIED** | Independently read all six records' `portfolio_function_status`/`capital_eligibility_status`/`sizing_readiness_status` — every field populated with a real closed-vocabulary value (table in §3 below). |
| 5 | Every `sizing_blocked`/`sizing_conditionally_ready` sleeve's `blocking_evidence[]` is fully populated | **SATISFIED** | Independently counted: `equity` 5, `fund_broad_market` 6, `fund_gld_defensive` 5, `crypto` 5, `cash_reserve` 5, `debt_reduction` 6 — all non-empty. `fund_broad_market`'s own count (6) reflects PR #306's own bounded-correction MINOR-1, which independently re-derived every contributing reason (one Axis A gap entry, one secondary-condition entry, four deferred-pair entries) rather than a single under-disclosed entry — independently re-verified this session by direct read, not merely cited from the PR's own narrative. |
| 6 | `debt_reduction`'s own actual disposition is explicit, not assumed from any illustrative trace | **SATISFIED** | `debt_reduction.yaml`: `portfolio_function_status: function_confirmed_distinct` (Basis 1 alone, independently sufficient), `capital_eligibility_status: not_yet_eligible` (mechanically forced), `sizing_readiness_status: sizing_blocked` (Axis B failure plus its own `sealed_unresolved` pair against `cash_reserve`). Matches `XASSET-0014` §7.1's own illustrative trace, but is now the sleeve's own real, sealed, non-illustrative record. |
| 7 | `cash_reserve`'s consolidation-non-settlement note is actually populated | **SATISFIED** | Independently read `cash_reserve.yaml`'s `cash_reserve_consolidation_note` field in full — a substantive, non-templated statement restating the `CASH`/`RESERVE` question as unresolved and explicitly not settled by this record, reusing `XASSET-0008` §N's own provenance finding. |
| 8 | The counterfactual-masking non-influence proof passes for every sleeve | **SATISFIED** | Independently located and ran `test_favored_sleeve_id_masking_does_not_change_basis1_or_basis3`, `test_masking_every_relationship_ledger_state_is_unaffected`, and `test_presence_independent_regression_guard_swap_disposition_no_cross_sleeve_leak` in `test_level1_sleeve_synthesis_validator.py` — all pass, as part of this session's own full local test run (below). |
| 9 | A dedicated Stage 4 validator module exists, is independently reviewed, and passes | **SATISFIED** | The Stage 4 section of `level1_sleeve_synthesis_validator.py` (a clearly separated section, confirmed by its own distinct `# ===...===` divider, distinct from the `# ---...---` dividers used for Stage 1-3). Independent review across three rounds on PR #306: original `pullrequestreview-4911497398` (2 MAJOR/5 MINOR) → corrected → delta `pullrequestreview-4912431420` (0 MAJOR/2 new MINOR) → corrected → final delta `pullrequestreview-4914735841` (0 BLOCKING/0 MAJOR/0 MINOR/3 non-blocking NOTE) → principal acceptance at exact head `01c0c88c8e1c9b0b72ea48c14d728c9cde852ddb`. Independently run standalone this session: `level1_sleeve_synthesis_validator: OK (7 profile result(s), 8 relationship result(s), 7 policy_adoption result(s))`. Independently ran the full `test_level1_sleeve_synthesis_validator.py` suite this session: **763 passed**, matching the PR's own final reported count exactly. |
| 10 | No sleeve's `sizing_readiness_status` was upgraded by anything other than the mechanical rule; an audit trail (not a drafting assertion) proves every `sizing_ready` disposition independently satisfies all four of §5's own conditions | **SATISFIED, with a precise scope note** | Zero sleeves currently reach `sizing_ready` (all six are `sizing_conditionally_ready` or `sizing_blocked` — see §3). The condition's own "audit trail proving every `sizing_ready` disposition..." clause therefore has zero real instances to prove against today; it is satisfied vacuously for the population that exists. The condition's broader clause — "no sleeve's status was upgraded by anything other than the mechanical rule" — is affirmatively, not vacuously, satisfied: the validator's mechanical Axis C consistency check (item 6 of the twenty-four-point spec) independently re-derives every sleeve's `sizing_readiness_status` from its own Axis A/B values, `unresolved_relationships[]`, and `relationship_coverage_ledger[]`, and would reject any record whose stated status does not match that mechanical re-derivation — proven not only against the six real records (all pass) but against synthetic cases in `test_level1_sleeve_synthesis_validator.py` that construct a sleeve meeting every `sizing_ready` precondition and confirm the mechanism accepts it (the `equity`-shaped synthetic case `XASSET-0014` §21 item 23 requires). This is the audit-trail mechanism the condition demands; it has not yet had a real `sizing_ready` sleeve to apply to. |
| 11 | Every sleeve's `relationship_coverage_ledger[]` is fully populated across all five pairs, zero unaccounted-for, zero silently-clean | **SATISFIED** | Independently counted: every one of the six records carries exactly 5 ledger entries, correctly classified (`sealed_determined`/`sealed_unresolved`/`deferred_disclosed`) against the sealed seven `sleeve_relationship` records plus `XASSET-0013` §E's own eight named deferred pairs — matching `XASSET-0014` §5.1's own per-sleeve table exactly, field for field. No sleeve reaches `sizing_ready` with a `deferred_disclosed` pair outstanding. |

**All eleven conditions are satisfied.** This is a necessary, not sufficient, precondition for
this filing — §15's own text is explicit that satisfying the gate does not itself authorize
numeric sizing; a separate, explicit governance act (this filing) is still required, and this
filing does not treat gate satisfaction as self-executing.

## 2. Does a numeric Level 1 sizing methodology already exist? — independently searched, not assumed

A full-repository search for any accepted decision defining how a Level 1 sleeve weight is to be
**derived** (as opposed to merely stating that Level 1 sizing is a required future step) returns
nothing:

- `XASSET-0001` §E defines the two-level architecture and states final allocation "must compare
  opportunity cost across all governed sleeves," but its own Alternatives Considered section
  explicitly rejected attempting to quantify or pre-size Level 1 in that filing — it names the
  requirement, not a method.
- `XASSET-0012`'s own Preflight independently confirmed, at its own session: "No existing Level 1,
  sleeve-allocation, or cross-asset-synthesis methodology found anywhere in the repository" — a
  full-repository grep for "Level 1," "sleeve allocation," and "cross-asset synthesis" across
  every governance decision returned only filings that *name* Level 1 as required future work,
  none that designs it, prior to `XASSET-0012` itself. `XASSET-0012`/`XASSET-0013`/`XASSET-0014`/
  `XASSET-0015` since then designed and populated the *descriptive* (non-numeric) sleeve-synthesis
  and policy-adoption layers only — neither touches numeric derivation.
- `TIER-0001`-`TIER-0013` govern equity **instrument-level** (Level 2) classification, valuation
  archetype assignment, and policy recommendation — a materially different layer than Level 1
  sleeve allocation, and one `XASSET-0001` §J's own sequencing rule keeps strictly downstream of
  any Level 1 budget.
- `VALUATION-0001`-`VALUATION-0007` govern equity **instrument-level** (Level 2) valuation
  methodology and execution — likewise downstream of, and never a substitute for, Level 1 sizing.
- `NUM-0001` establishes a provenance/classification **standard** for any consequential numeric
  parameter once one exists (which of six classes it belongs to, required disclosure fields,
  false-precision prohibitions) — it does not itself supply a method for deriving a sleeve
  weight; it governs how any weight this filing's future implementation eventually produces must
  be labeled, sourced, and reviewed. This filing's future implementation is bound to it (§13
  below), not exempted from designing on top of it.
- `TGT-0001`/`TGT-0002` govern the **additive target-budget policy** for equity **roster**
  promotions/demotions inside `targets.yaml` — a Level 2, single-tier-change mechanism, not a
  cross-sleeve allocation method.
- The retired T1/T2 tier-weighting system (`weight_backtest.md`, superseded by `PHQ-2026-02`'s
  canonical destination architecture) predates, and was designed for, a tier structure that no
  longer exists; it was never a cross-sleeve (equity-vs-ETF-vs-crypto-vs-cash-vs-debt) mechanism
  in the first place, only an intra-equity weighting scheme.

**Conclusion: no numeric Level 1 sizing methodology exists anywhere in this repository.** This
filing is the first to design one. Options A/C from the authorizing task's own framing therefore
reduce to a genuine choice between A (this filing both designs and authorizes) and B (design here,
authorize content in a wholly separate future filing) — §4 below explains which was chosen and why.

## 3. Live sizing-status population, independently re-derived

**Table redacted by this document's own third bounded correction, resolving independent exact-head
delta review `pullrequestreview-4917325267`'s fresh MAJOR finding — described structurally here,
not by republishing the specific live counts or derived outcomes the review itself found, to avoid
the exact self-defeating error of restating leaked information inside its own correction note.**
The prior version of this table's own fifth column stated each sleeve's exact current
relationship-coverage input count (the same field §9.3's own R2 rule reads). The review found that
combining those live, per-sleeve counts with R2's own relative-extreme rule (fires up for the
sizing-eligible sleeve with the strict, unique fewest such count; fires down for the strict, unique
most; no fire on a tie) let a reader mechanically, certainly determine R2's real directional
outcome for every sizing-eligible sleeve today, which, combined with this document's own published
`starting_baseline_pct`/increment constants, narrowed each real sleeve's eventual
`provisional_target_pct` from the full five-value reachable set to a real, certain three-value
subset. This is the identical leakage class the withdrawal of R1's own reachability table (former
§9.10) already eliminated, left open here for R2. **Resolved**: the
table below states only the already-governing Axis A/B/C categorical disposition and a citation
to the specific governing gate/case where a sleeve is blocked — no exact relationship-pair count,
no relative-extreme ("fewest"/"most"/"strongest") characterization, and no secondary-condition-type
enumeration for any sleeve, sizing-eligible or blocked, appears anywhere in this table. The
underlying evidence remains fully available in the cited sealed records — this table simply no
longer performs the arithmetic-enabling work of restating it next to the newly-defined R2/R3 rules
and this document's own published constants (§3.1 below states this as a standing rule, not a
one-time table fix).

| `sleeve_id` | Axis A | Axis B | Axis C | Governing basis (categorical only) |
|---|---|---|---|---|
| `equity` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | Sealed `policy_adoption`/`sleeve_relationship` evidence supports this disposition — see the cited sealed record; current relationship-coverage and secondary-condition detail is intentionally not restated here (§3.1). |
| `fund_broad_market` | `function_status_unresolved` | `eligible_for_target_consideration` | `sizing_blocked` | Blocked via the Axis A gate alone (`XASSET-0014` §22 Case G) — Basis 1 unavailable, Basis 2 not asserted, Basis 3 available but this session's own drafting discretion (`XASSET-0015` §E) landed on the unresolved reading. |
| `fund_gld_defensive` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | Sealed `policy_adoption`/`sleeve_relationship` evidence supports this disposition — see the cited sealed record; current relationship-coverage and secondary-condition detail is intentionally not restated here (§3.1). |
| `crypto` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | Sealed `policy_adoption`/`sleeve_relationship` evidence supports this disposition — see the cited sealed record; current relationship-coverage and secondary-condition detail is intentionally not restated here (§3.1). |
| `cash_reserve` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_blocked` | Forced by its own `sealed_unresolved` pair against `debt_reduction` (`XASSET-0014` §22 Case D). Carries the mandatory `cash_reserve_consolidation_note`. |
| `debt_reduction` | `function_confirmed_distinct` | `not_yet_eligible` | `sizing_blocked` | Axis B mechanically forced by `forced_abstention` evidence coverage; also its own `sealed_unresolved` pair against `cash_reserve`. No `targets.yaml` row exists for this sleeve at all. |

**Zero sleeves reach `sizing_ready`.** Three (`equity`, `fund_gld_defensive`, `crypto`) reach
`sizing_conditionally_ready`. Three (`fund_broad_market`, `cash_reserve`, `debt_reduction`) reach
`sizing_blocked`. This split is not a judgment this filing makes — it is a mechanical fact already
sealed in the six Stage 4c records, independently re-verified above (§1's own eleven-condition
gate table, which discloses only population-level counts — e.g. "every one of the six records
carries exactly 5 ledger entries" — never a per-sleeve relative ranking among the three
sizing-eligible sleeves specifically, and is therefore not a leak of this same class), unchanged
by anything in this filing. Every sleeve's own current `deferred_disclosed` count, secondary-
condition-type breadth, and any other live relationship-coverage detail is available in its own
cited sealed record (`intelligence/level1_sleeve_synthesis/policy_adoption/<sleeve_id>.yaml` and
the sealed `sleeve_relationship` records it references) — deliberately not restated in this
governance filing (§3.1).

### 3.1 Implementation-time live-derivation boundary — added by this document's own third bounded correction

**Rule, standing and general, not limited to §3's own table.** This governance filing defines R2's
and R3's own algorithms, semantics, and constants (§9.3-§9.4) transparently and completely enough
for independent review and for a future implementer to build a live-rederivation validator (§19
item 17) — **but it must never itself publish the current real trigger-input state for any
sizing-eligible sleeve**: no exact `deferred_disclosed`/`sealed_determined` pair count, no exact
secondary-condition-type breadth or type enumeration tied to a real sleeve, no relative-extreme
characterization ("fewest," "most," "strongest," "only sleeve with...") comparing real sleeves
against each other, and no other live quantity or ranking that, combined with this document's own
published `starting_baseline_pct`/increment constants, would let a reader mechanically derive or
materially narrow any individual real sleeve's eventual `provisional_target_pct`. **The future,
separately authorized implementation this filing authorizes must derive R2 and R3 live, itself,
directly from the sealed source records at implementation time** — this design filing deliberately
stops short of performing, or pre-disclosing the inputs to, that derivation.

This is not security through obscurity: every constant, rule, tie condition, and boundary that
defines R2/R3 remains fully disclosed (§9.3, §9.4, §9.7) — a reader can understand exactly *how*
R2 and R3 work without this filing telling them *which* real sleeve currently fires which
direction. The underlying sealed evidence itself is not hidden or newly restricted — it remains
exactly as available in `intelligence/level1_sleeve_synthesis/policy_adoption/*.yaml` and the
sealed `sleeve_relationship` records as it always was (the same posture `XASSET-0015` §C's own
already-public Axis A disclosure already established for the withdrawn R1 fact) — only this
specific governance filing declines to perform the arithmetic-enabling work of restating it next
to the newly-defined trigger rules and constants in the same document.

**Adversarial check, added as an explicit governance-level requirement, not merely a drafting
intention.** Given only this filing's own committed content (this decision file and its
supporting artifact), a reader must not be able to determine, for any real sizing-eligible sleeve:
whether R2 fires up, down, or not at all; whether R3 fires up, down, or not at all; the resulting
adjustment tuple; or a narrowed target-candidate subset caused specifically by this document's own
disclosed current-evidence detail. The generic, methodology-derived range `[12.67, 20.67]` (§9.4,
§9.5) is explicitly **not** a violation of this rule — it follows from the methodology's own fixed
constants alone, identically for every sizing-eligible sleeve, and carries no information about
any real sleeve's own current trigger state. A future implementation's own populated
`numeric_sizing` records, by contrast, are exactly where real R2/R3 states and real provisional
targets belong — computed, disclosed, and independently reviewed at that later, separately
authorized stage (§20), never pre-computed or partially pre-disclosed here.

## 4. Minimality decision — Option A, with the reasoning made explicit and falsifiable

Every prior stage in this repository's cross-asset undertaking (`XASSET-0002`→`0003`/`0004`;
`XASSET-0005`→`0006`/`0007`; `XASSET-0008`→`0009`; `XASSET-0010`→`0011`; `XASSET-0012`→`0013`;
`XASSET-0014`→`0015`) split methodology design from content authorization into two separate
filings. The reason, stated explicitly in each case's own Alternatives Considered section, was
never "design and authorization must always be two filings" as a rule for its own sake — it was
that **which subset of a larger, undetermined space the first population should cover was itself
an independent judgment requiring its own scoping decision**, separate from the schema. `XASSET-0013`
§C had to independently decide which 7 of 15 possible sleeve-relationship pairs to populate first;
`XASSET-0015` §C-E had to independently determine, sleeve by sleeve, whether each of the six
sleeves was even lawfully evaluable at all. Both were genuine, non-mechanical judgment calls.

**No equivalent scoping judgment exists here.** The population question this filing would
otherwise defer to a separate "Stage-B" content-authorization filing — *which sleeves are eligible
for a provisional numeric candidate, and which are not* — is not an open judgment call requiring
its own independent authorization. It is a direct, mechanical, already-settled consequence of
`XASSET-0014` §5's own accepted Axis C rule, applied to the six already-sealed Stage 4c records
(§3 above): `sizing_conditionally_ready` sleeves are eligible for a provisional numeric candidate;
`sizing_blocked` sleeves are not, per §15 condition 6's own explicit text ("a future numeric-sizing
filing must explicitly disclose that it is proceeding without a `debt_reduction` numeric
candidate... rather than silently dropping the sleeve"). There is nothing left for a separate
content-authorization filing to decide that this filing, reading the sealed data, has not already
determined for it.

**Option A** — one filing that designs the Level 1 numeric-sizing methodology and, in the same
filing, authorizes exactly one future, bounded implementation to apply it to the population §3
already fixes — is therefore chosen not as a shortcut around this repository's own established
discipline, but because the condition that discipline exists to protect (an independent scoping
judgment happening before, not folded into, methodology design) does not apply here. If an
independent reviewer disagrees — if the population determination in §3 is found to require its
own separate authorization after all — the correction is narrow and available: split §7's
authorization out into its own future filing, leaving §§3-14's methodology design untouched. This
filing does not compute, populate, or authorize computing a single percentage anywhere in its own
text (§7, §15).

## 5. Purpose — restated precisely

The future implementation this filing authorizes answers exactly one question: **how should
capital be provisionally distributed across the six Level 1 sleeves, given the currently sealed
policy state (§3) and its own disclosed uncertainty?** It does not answer, and no future
implementation acting under this authorization may answer: which of the 27 canonical equities (or
any future equity cohort) receives capital; which ETF among SPY/VEA/VWO; which cryptocurrency
among BTC/ETH/SOL; any exact trade or dollar amount; any current-account rebalance action; or any
margin deployment decision. This restates, and does not narrow or widen, `XASSET-0001` §E's own
Level 1/Level 2 split.

## 6. Blocked-sleeve treatment — the load-bearing design choice

`XASSET-0014` §15 condition 6 is the controlling text: a `sizing_blocked` sleeve must be
represented with an **explicit no-numeric-candidate or flagged-placeholder state**, never silently
dropped from the taxonomy and never assigned a numeric value that could be read as a policy
conclusion. This filing adopts the stricter of the two options condition 6 itself offers —
**no numeric candidate at all**, never a placeholder number — for a reason specific to this
domain: a literal `0.00%` value is not an abstention, it is a policy assertion (a considered,
zero-weight allocation), indistinguishable in the record's own numeric field from a genuine
governance finding that a sleeve deserves no capital. `debt_reduction` being "not yet sizeable"
and `debt_reduction` being "sized at zero" are two entirely different, and differently
consequential, findings; only the first is what the sealed evidence actually supports. A
categorical status field, not a numeric fallback, is the only representation that cannot be
misread as the second.

**Rule**: every `sizing_blocked` sleeve's future numeric-sizing record carries
`numeric_target_status: no_provisional_target_pending_axis_c` and `provisional_target_pct: null` —
structurally required, never omissible, never substituted with `0.00`. Every
`sizing_conditionally_ready` sleeve's record carries `numeric_target_status:
provisional_target_assigned` and a populated `provisional_target_pct` (§8). `sizing_ready` (not
live today) would carry the identical `provisional_target_assigned` treatment — Axis C's own
stricter bar is a readiness distinction the sizing schema does not need to re-encode, since the
`sizing_readiness_status` field itself, cited by reference (§9), already carries it.

## 7. Exactly which future implementation this filing authorizes

Exactly one future, separate, bounded implementation PR — gated on this filing's own merge,
independent review, and principal acceptance, and requiring its own full independent-review/
correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle before it may
itself be considered authoritative — may populate:

- one `intelligence/level1_sleeve_synthesis/numeric_sizing/<SLEEVE_ID>.yaml` record for **each of
  the six sleeves** (never omitted, matching this repository's own "never silently drop a sleeve
  merely because its disposition is unfavorable" discipline, applied identically here): three
  (`equity`, `fund_gld_defensive`, `crypto`) carrying a populated `provisional_target_pct`; three
  (`fund_broad_market`, `cash_reserve`, `debt_reduction`) carrying `provisional_target_pct: null`
  per §6;
- one `COHORT_MANIFEST.yaml` for the new `numeric_sizing/` sub-namespace, parallel to (never
  merged with) `profiles/`, `relationships/`, and `policy_adoption/` — extended with the
  reconciliation block §10 defines;
- a dedicated Stage 5 section of `level1_sleeve_synthesis_validator.py` (or a new module — the
  implementing session's own choice to justify, mirroring every prior stage's identical
  deferral), implementing the full specification in §14;
- the corresponding focused/adversarial test suite;
- the required additive `operations/WORKSTREAMS.yaml` synchronization.

**Not authorized** by this filing, under any circumstance, in that future implementation or any
other: an actual `provisional_target_pct` value chosen or computed by this filing itself; any
Level 2 instrument-level content; any allocator/`targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`/`margin_state.py`/`levels.py` change; any allocation check, live or
scenario; any chart evidence; any margin/leverage change; any research on the eight still-deferred
`sleeve_relationship` pairs, the broader contender registry, `VRT`/`WMT`, or `QQQ`.

## 8. Output record schema

```
sleeve_id                        # closed, one of the six sleeve_id values, XASSET-0012 SS2
schema_version
policy_adoption_reference        # one hash pin into this sleeve's own sealed policy_adoption
                                  #   record -- canonical_record_hash(), live-recomputed, never
                                  #   trusted from a stored value
numeric_target_status            # closed: provisional_target_assigned |
                                  #   no_provisional_target_pending_axis_c -- mechanically
                                  #   derived from the cited policy_adoption record's own
                                  #   sizing_readiness_status (sizing_conditionally_ready or
                                  #   sizing_ready -> provisional_target_assigned;
                                  #   sizing_blocked -> no_provisional_target_pending_axis_c),
                                  #   zero drafting-session discretion, matching Axis B's own
                                  #   mechanical-derivation precedent (XASSET-0014 SS4)
provisional_target_pct           # nullable; populated only when numeric_target_status ==
                                  #   provisional_target_assigned; two decimal places (SS12);
                                  #   never negative; never >= 100.00 for a single sleeve; MUST
                                  #   equal, exactly, the value the SS9 derivation procedure
                                  #   independently re-produces from this same record's own
                                  #   starting_baseline_pct and applied_adjustments[] -- never
                                  #   an independently-authored number (SS9.7)
starting_baseline_pct            # required whenever provisional_target_pct is populated --
                                  #   the SS9.2 equal-share baseline value (100.00 / 6, two
                                  #   decimal places) BEFORE any adjustment; identical, fixed,
                                  #   and mechanically derived for every sizing-eligible sleeve
                                  #   -- never sleeve-specific, never self-declared
applied_adjustments[]             # required whenever provisional_target_pct is populated --
                                  #   zero or more entries, one per SS9.3 trigger that actually
                                  #   fired for this sleeve, each {governing_rule_id: R2 | R3
                                  #   -- R1 withdrawn as a numeric trigger by this document's own
                                  #   second bounded correction, SS9.3; a governing_rule_id of R1
                                  #   is structurally rejected, never a valid value, direction:
                                  #   up | down, magnitude_pct: the fixed SS9.4 increment,
                                  #   evidence_ref: a hash pin into the specific
                                  #   sealed record(s) the trigger read}; empty list is valid
                                  #   (a sleeve at its unadjusted baseline) and is not an error
governing_rule_ids[]              # required whenever provisional_target_pct is populated --
                                  #   the closed set of SS9.3 trigger identifiers this record's
                                  #   own applied_adjustments[] actually invoke; derived from,
                                  #   never independent of, applied_adjustments[] -- a
                                  #   convenience index field, not an independent claim
target_classification            # forced constant: provisional_governance_guardrail
                                  #   (NUM-0001 SS1 class 5) -- structurally rejected if any
                                  #   other class is cited (SS13); null when
                                  #   provisional_target_pct is null
review_condition                 # required, non-empty, whenever provisional_target_pct is
                                  #   populated -- an evidence- or event-driven condition
                                  #   (NUM-0001 SS6), never a bare calendar date invented
                                  #   without its own stated reason
uncertainty_disclosure           # required, non-empty, whenever provisional_target_pct is
                                  #   populated -- free text citing only: (a) this sleeve's own
                                  #   cited policy_adoption record's blocking_evidence[] and
                                  #   relationship_coverage_ledger[] entries; (b) named
                                  #   secondary_conditions on its own sealed relationship
                                  #   records not already consumed by a SS9.3 trigger; (c)
                                  #   disclosed valuation/evidence-coverage gaps per SS11,
                                  #   disclosure-only per SS9.3's own explicit exclusion; (d)
                                  #   for crypto specifically, the sleeve-wide
                                  #   cross_coin_correlation_status abstention and any
                                  #   per-coin historical-behavior divergence, disclosure-only
                                  #   per SS9.3's own explicit exclusion -- never a fabricated
                                  #   caveat, never omitted
comparative_consistency_note      # required whenever provisional_target_pct is populated --
                                  #   one sentence per other sizing-eligible sleeve at a
                                  #   materially different provisional_target_pct, naming the
                                  #   specific governing_rule_id(s) responsible for the
                                  #   difference (SS9.7); required to state "no material
                                  #   difference" where two sleeves land on the same value
blocking_rationale                # required, non-empty, whenever numeric_target_status ==
                                  #   no_provisional_target_pending_axis_c -- restates, does
                                  #   not re-derive, the cited policy_adoption record's own
                                  #   blocking_evidence[]
sizing_boundary_note              # fixed, repository-standard text restating: Level 1 only,
                                  #   no Level 2 leakage, not adopted policy, no allocation
                                  #   check authorized by this record
record_status                    # draft | sealed
sealed_at / governing_decisions / drafting_session_or_shard_id / content_sha256 /
  cohort_manifest_entry
```

No field above is a score, a rank, a composite index, or an optimization objective. No field
carries individual-instrument (Level 2) content. `provisional_target_pct` is the only numeric
field in the schema besides the structural `content_sha256`/manifest hash fields, which are not
economic values.

## 9. Numeric derivation procedure — ordered, closed, auditable, reproducible

**Bounded correction (this PR, resolving independent review `pullrequestreview-4916420679`'s
MAJOR finding).** The original §9 defined a closed list of permitted evidence categories and an
explicit prohibition on assembling them into a formula, but left the actual transformation from
evidence to number entirely to undocumented, session-specific "governance judgment... disclosed
in free text" — its own words. The review correctly found this insufficient: a future
implementer given `equity`, `fund_gld_defensive`, and `crypto`'s identical sealed evidence would
have no governed procedure telling them why a candidate figure should be 45%, 55%, or 65%, and no
mechanism preventing two independent sessions from reaching materially different figures for the
same sleeve with no reconcilable reason. This section replaces the original mechanism with a
seven-step ordered procedure (§§9.1-9.7) that is deterministic given the same sealed evidence —
not a continuously-tunable weighted formula (the review's own alternative concern, and the
directive's own explicit "do not create a formula merely for the sake of determinism" instruction),
but a small, closed table of fixed, named, class-5 adjustment increments applied to a zero-based
starting point, with every application independently re-derivable and every difference between two
sleeves' outputs traceable to a specific, named, governed rule. **Further corrected by this
document's own second bounded correction**: the original seven-step procedure named three
triggers; one (R1, "full Axis-A-basis coverage") was independently found, on a fresh exact-head
review, to reward evidentiary completeness of the classification finding itself rather than any
argued economic or risk-based reason to hold more capital — withdrawn as a numeric trigger and
retained only as a disclosure-only fact (§9.3). The procedure below now defines exactly **two**
named, closed, symmetric triggers (R2, R3).

### 9.1 Step A — establish the allocable total

Unlevered 100.00% conceptual accounting space, unchanged from the original design (§10 below).
Only `sizing_conditionally_ready` sleeves (today: `equity`, `fund_gld_defensive`, `crypto`) may
receive a `provisional_target_pct`. Blocked sleeves receive none (§6). `unsized_reserved_capital_pct`
remains an explicit, mechanically computed reconciliation figure — never `cash_reserve`, never a
policy redistribution.

### 9.2 Step B — starting point: an equal share of the full, closed six-sleeve taxonomy

**Rule**: every sizing-eligible sleeve's `starting_baseline_pct` is `100.00 / 6 = 16.67`
(rounded per §17), identical for every eligible sleeve, before any adjustment.

**Justification, from repository authority, not invented**: the denominator is **six** —
`XASSET-0012` §2's own closed, accepted, whole sleeve taxonomy — never **three**, the count of
sleeves currently eligible. Dividing by the full population, not the eligible subset, is the
direct numeric extension of the same reasoning the original design's §10 already established and
the review already found sound ("Correct choice among the alternatives... the identical
numeric-leakage risk §6/condition 6 exist to prevent, reached indirectly"): if the three eligible
sleeves' baseline were computed as an equal share of only themselves (100/3 = 33.33 each), the
three currently-blocked sleeves' own notional share would already, silently, be zero at the very
starting point — the same leakage the residual bucket was built to prevent, only moved one step
earlier in the procedure. Dividing by six means each currently-blocked sleeve's own 16.67%
notional share flows, undiminished and unadjusted, directly into `unsized_reserved_capital_pct` by
construction, before any trigger is even evaluated — an honest, disclosed starting state, not
one the eligible sleeves have to be prevented from silently absorbing.

This is a **zero-based** starting point in the same sense `OPS-0006` §§2-3 established for
`WS-0005`'s own equity review — a pure count of already-governed structure (the six-sleeve
taxonomy), containing no invented judgment, no calibration, and no historical anchor. **No
`targets.yaml` weight, current or historical, may be used as a starting point or an input to any
step of this procedure.** `OPS-0006` §2's own restated rule — "current tier/target preserved as
historical baseline only, never as research evidence" — is directly on point, one layer up: a
`target_pct` value belongs to Level 2's own, entirely separate, still-unauthorized instrument-level
sizing question (§15), and using it here would smuggle the exact pre-existing policy this
zero-based undertaking exists to test from scratch back in through the starting point. A future
Milestone-7-style **reconciliation** against current `targets.yaml` weights remains available as
its own separate, later, explicitly authorized comparison step — never as an input to this
derivation.

### 9.3 Step C — allowed directional evidence: two named, closed triggers

Each trigger is evaluated once per sizing-eligible sleeve, mechanically, from already-sealed
evidence this repository's own prior stages already produced — no new research, no new evidence
type, no citation of `favored_sleeve_id` under any framing.

**Governing hard rule, added by this document's own second bounded correction, applied to every
trigger below and to any future candidate trigger**: a numeric adjustment may exist only where the
underlying evidentiary fact is itself an accepted, governed **uncertainty- or risk-discount**
signal — more disclosed, unresolved cross-sleeve evidence gaps mean more provisional uncertainty
about the sleeve's own eventual capital claim, which this procedure treats as grounds for a
*smaller* provisional figure pending resolution, and the strict absence of such gaps (relative to
the sizing-eligible population) as grounds for a comparatively larger one. **No numeric adjustment
may exist merely because a sleeve carries more citations, more lawful evidentiary bases, more
researched relationships, or more complete documentation, considered as evidence quantity or
evidence-route multiplicity on its own** — documentation completeness is a confidence-in-
classification measure, not a portfolio-risk or opportunity-cost signal, and rewarding it
numerically would grant capital for how thoroughly a sleeve's own eligibility finding happens to be
sourced rather than for any argued economic reason to hold more of it. This is exactly the defect
an independent exact-head review (`pullrequestreview-4916848704`) found in this section's original
third trigger, R1 ("full Axis-A-basis coverage" — a sleeve independently clearing all three lawful
Axis A bases per `XASSET-0014` §3.2, rather than the single basis Axis A itself requires to reach
`function_confirmed_distinct`, received a positive adjustment). Reviewed directly against
`XASSET-0014` §3/§3.2's own controlling text: Axis A's threshold is binary (one basis suffices;
`function_confirmed_distinct` does not distinguish a one-basis finding from a three-basis one), and
no governing text anywhere states or implies that clearing additional bases is itself a reason to
size a sleeve larger. The review further found this concretely, foreseeably favored only
`fund_gld_defensive` today — the sole sleeve independently clearing all three bases per
`XASSET-0015` §C — for a reason unconnected to any governed risk or opportunity-cost basis. **R1 is
therefore withdrawn as a numeric trigger.** The underlying fact — whether a sleeve's own Axis A
finding independently clears one, two, or all three lawful bases — is retained, unchanged in
substance, as a **disclosure-only** item in a future record's own `uncertainty_disclosure` field:
it may describe what basis-completeness the sleeve's own sealed finding rests on, exactly as
`XASSET-0015` §C already discloses in plain prose, but it may never move `provisional_target_pct`,
trigger an adjustment, or constrain a maximum — matching the identical disclosure-only treatment
this section already gives `stronger_evidence_maturity`, Level 2 valuation completeness, and crypto
per-coin divergence, immediately below. This is not a new, fourth numeric trigger under a different
name — it is the same fact, now correctly labeled as confidence-in-classification context rather
than a portfolio-risk or capital-allocation signal.

- **R2 — relative relationship-coverage strength.** Fires **up** for the sleeve with the strict,
  unique **fewest** `deferred_disclosed` entries in its own `relationship_coverage_ledger[]` among
  the sizing-eligible population; fires **down** for the sleeve with the strict, unique **most**.
  No adjustment fires for any sleeve on a tie (two or more eligible sleeves sharing the same count)
  — a tie is not evidence of a difference, and this rule assigns none. **Rationale, stated in
  risk-discount terms, not documentation-volume terms**: a `deferred_disclosed` entry names a
  relationship pair this repository has not yet resolved — real, disclosed, unresolved
  cross-sleeve evidence about how this sleeve's own economic function interacts with, overlaps, or
  duplicates another sleeve's. A sleeve carrying strictly more of these than every other
  sizing-eligible sleeve carries a comparatively larger body of unresolved cross-sleeve
  opportunity-cost evidence bearing on its own eventual capital claim — a smaller provisional
  figure, pending that resolution, is the discount this repository already applies elsewhere to
  disclosed-but-unresolved evidence (`NUM-0001`'s own provisional-guardrail treatment; `TIER-0009`
  §K's proceeding-on-disclosed-partial-evidence precedent, applied here in the opposite direction —
  proceeding, but discounted). The strict absence of such gaps, relative to the same population, is
  the mirror-image case: comparatively less unresolved cross-sleeve evidence bearing against the
  sleeve, not more evidence *for* it. This is a genuine risk/uncertainty signal, not a reward for
  research effort — the direction fires against **unresolved** coverage specifically, never for raw
  relationship-record volume (a sleeve named in more sealed pairs than another, with none of them
  `deferred_disclosed`, gains nothing extra from R2 for the additional volume alone).
- **R3 — relative secondary-condition breadth.** For each sizing-eligible sleeve, compute
  `secondary_condition_breadth` = the count of **distinct** secondary-condition **types**
  (`evidence_partial_present`, `forced_abstention_present`, `overlap_or_duplication_disclosed`) —
  never distinct **occurrences** — appearing anywhere across that sleeve's own sealed
  `sleeve_relationship` records. Counting distinct types, not raw occurrences, is a deliberate
  design choice: a sleeve is not penalized merely for having more sealed relationship pairs to
  begin with (a byproduct of coverage breadth R2 already measures separately), only for the
  **variety** of distinct evidentiary gaps disclosed against it. Fires **up** for the sleeve with
  the strict, unique fewest; fires **down** for the sleeve with the strict, unique most. No
  adjustment on a tie. This is the mechanism's **overlap/concentration treatment**: a sleeve
  carrying `overlap_or_duplication_disclosed` on any of its own relationship records — the one
  concrete, sealed overlap signal presently available to any sizing-eligible sleeve — contributes
  to this trigger as a **directional adjustment**, never a bare review condition and never a hard
  ceiling on the sleeve's own maximum (directly answering the directive's own overlap-treatment
  choice requirement). **Rationale, stated in risk-discount terms**: a broader distinct-type
  breadth of secondary conditions is a broader, disclosed set of **kinds** of sizing caveat
  bearing on this specific sleeve — partial evidence somewhere in its own coverage, a forced
  abstention somewhere, a disclosed overlap with another sleeve's own function — each a genuinely
  distinct category of uncertainty a provisional figure should discount against, not merely a
  count of how thoroughly the sleeve's relationships happen to be documented. No individual
  condition type is treated as more economically severe than another here; the trigger reads only
  the **variety** of distinct types present, exactly as R2 reads only the count of unresolved
  pairs, not any pair's own individual substance — extending beyond what governing methodology
  supports (e.g. ranking one condition type as worse than another) is deliberately not attempted.

**R2 and R3 are not fully orthogonal, and this is disclosed rather than hidden.** R2 reads a
sleeve's own count of `deferred_disclosed` (still-unresolved) relationship-coverage entries; R3
reads the distinct-type breadth of `secondary_conditions` (evidence gaps already disclosed on
*sealed*, determined pairs — `evidence_partial_present`, `forced_abstention_present`,
`overlap_or_duplication_disclosed`). These read two structurally different fields on two different
categories of relationship record (unresolved-coverage entries versus sealed-pair secondary
conditions) and can co-occur or partially offset for the same sleeve without either trigger ever
reading the other's own underlying field — no hidden double-weighting of a single disclosed fact
exists, since R2's own deferred-coverage count and R3's own secondary-condition-type set are
disjoint data. That the two triggers can both fire, or fire in opposite directions, for the same
sleeve is intentional and bounded, not a design defect: a sleeve may simultaneously have
comparatively little unresolved coverage (R2 up) while carrying a comparatively broad variety of
disclosed caveats on the pairs it does have sealed (R3 down), and the resulting net adjustment
(here, `0.00`, since the two `±2.00` effects cancel) is exactly the correct, traceable outcome of
two genuinely distinct uncertainty signals pointing in different directions for the same sleeve —
not evidence that either trigger is redundant with the other.

**Explicitly excluded from both triggers — disclosure-only, never a numeric input:**

- `stronger_evidence_maturity`/`favored_sleeve_id`, under any framing — restated, not weakened,
  from the original §9: no trigger, no magnitude, and no future formula of any kind may read this
  disposition. A future implementation's `uncertainty_disclosure` field may *name* that such a
  finding exists and describe what it says about relative evidence maturity; it may never be
  converted into, or read as justifying, a specific number or trigger.
- **Axis-A basis-completeness** (the withdrawn R1 fact, above) — disclosure-only, per this
  correction.
- **Level 2 equity-valuation evidence** (the 9 of 27 `partial` `valuation_results`, the universal
  `discount_rate_evidence` abstention) — `equity`'s own Level 1 sizing eligibility and provisional
  figure are governed by Axis A/B/C and the two triggers above, never by Level 2 instrument
  valuation completeness (§11, unchanged). This partial evidence must be named in `equity`'s own
  `uncertainty_disclosure`; it may never move `provisional_target_pct` or trigger a downward
  adjustment, a maximum-value constraint, or any other numeric effect — **disclosure-only**,
  directly answering the directive's own valuation-treatment choice requirement.
- **`crypto`'s own sleeve-wide `cross_coin_correlation_status` abstention and any per-coin
  (BTC/ETH/SOL) historical-behavior divergence** — a `sleeve_profile`-level abstention and Level 2
  (per-instrument) fact, respectively, neither of which may enter a Level 1 trigger. Both are
  **disclosure-only**, cited in `crypto`'s own `uncertainty_disclosure`, never a numeric adjustment
  and never a basis for splitting `crypto`'s own single provisional figure across BTC/ETH/SOL —
  directly answering the directive's own crypto-treatment choice requirement and restating the
  Level 1/Level 2 boundary (§15) at this specific point.
- The four `not_yet_computable_interface_only` overlap-model dimensions — restating `XASSET-0013`
  §G's own citation rule, unweakened: never cited as though computed.
- Any current or historical `targets.yaml` weight (§9.2).
- Any chart, margin, leverage, or deployment-timing fact (§15, unchanged).

### 9.4 Step D — adjustment magnitude: a fixed, class-5 increment, not a tuned coefficient

Every trigger that fires moves the affected sleeve's provisional figure by exactly **±2.00
percentage points** — one fixed, repository-declared constant, identical across both triggers and
all three sizing-eligible sleeves, never sleeve-specific, never scaled by how strongly a trigger
fired (each trigger is binary: fired or did not fire). This is the smallest mechanism that is
simultaneously closed, bounded, and auditable without inventing empirical precision: the
**existence** of a governed evidentiary difference (R2/R3, §9.3) is real and disclosed; the
**size** of its effect on the provisional figure is not empirically calibrated (no backtest or
sweep has evaluated any candidate increment) and is not claimed to be — it is itself a `NUM-0001`
§1 class 5 provisional governance guardrail, the same class every resulting
`provisional_target_pct` carries (§18), with its own review condition (§9.8). A future evidence-
bounded or empirically-calibrated increment value would require its own separate, future,
evidence-driven governance decision — this filing adopts the flat, fixed increment specifically
because no such evidence exists yet, matching `NUM-0001` §8's own explicit warning against
mislabeling an evidence-bounded or provisional value as calibrated.

**Bound, mechanically re-enumerated by this document's own second bounded correction, not assumed
or copied from any prior draft or review.** With R1 withdrawn (§9.3), exactly two triggers remain,
each independently capable of firing `up` (`+2.00`), `down` (`-2.00`), or not at all (`0.00`) for
any given sizing-eligible sleeve — nine reachable `(R2, R3)` combinations in total:

| R2 | R3 | Net adjustment |
|---|---|---|
| up | up | `+4.00` |
| up | none | `+2.00` |
| up | down | `0.00` |
| none | up | `+2.00` |
| none | none | `0.00` |
| none | down | `-2.00` |
| down | up | `0.00` |
| down | none | `-2.00` |
| down | down | `-4.00` |

The reachable net-adjustment set is exactly `{-4.00, -2.00, 0.00, +2.00, +4.00}` — the minimum
reachable total is `-4.00` (both triggers fire down), the maximum is `+4.00` (both fire up). Every
sizing-eligible sleeve's total adjustment is therefore bounded, by construction, to `[-4.00,
+4.00]` percentage points from its `starting_baseline_pct` — no separate artificial cap is
required.

### 9.5 Step E — hard constraints

Only already-governed constraints apply, none newly authored (§14, unchanged): the unlevered
100.00% identity; individual-sleeve bounds `[0.00, 100.00)`; no citation of the 1.8x leverage cap
or 30% buffer floor to enlarge any figure; the six `computed_from_existing_mechanism` overlap
dimensions consulted only where they bear on a sizing-eligible sleeve, never the four uncomputed
ones. Given §9.4's own corrected, mechanically re-enumerated bound, no sleeve can be pushed
outside **`[12.67, 20.67]`** (`16.67 - 4.00` to `16.67 + 4.00`) by this procedure alone —
comfortably inside `[0.00, 100.00)` with no additional clamping needed.

### 9.6 Step F — reconcile the residual

Mechanically computed, unchanged from the original design (§10): `unsized_reserved_capital_pct =
100.00 - sum_of_assigned_targets_pct` (floored at `0.00`, though §9.4's own bound makes a
negative pre-floor value unreachable by this procedure — the floor and the reconciliation-identity
check remain mandatory defensive requirements on the future validator regardless, since a stored
record must never be trusted merely because the procedure that *should* have produced it is
bounded — see §19's new items).

### 9.7 Step G — consistency checks: identical evidence, identical output; every difference is traceable

Two mandatory, mechanically-enforced properties, required of the future validator, not merely
narrated:

1. **Determinism.** Recomputing `starting_baseline_pct`, every `applied_adjustments[]` entry, and
   the resulting `provisional_target_pct` twice from the same sealed evidence must produce
   byte-identical results both times — the same discipline this repository already applies to
   every structural hash and every mechanically-derived categorical field elsewhere in this exact
   record chain (`canonical_record_hash()`, Axis B re-derivation, the counterfactual-masking
   proof).
2. **Comparative consistency.** Whenever two sizing-eligible sleeves' `provisional_target_pct`
   values differ, at least one `applied_adjustments[]` entry must differ between them, and each
   sleeve's own `comparative_consistency_note` (§8) must name the specific `governing_rule_id`(s)
   responsible for the difference. Two sleeves with byte-identical trigger evaluations under
   §9.3-§9.4 **must** receive byte-identical `provisional_target_pct` values — this is not a
   drafting convention to remember but a direct, structural consequence of Step D's own fixed,
   non-sleeve-specific increment: there is no remaining degree of freedom after the triggers are
   evaluated, so no unexplained preference between two identically-evidenced sleeves is even
   representable in the schema, let alone permitted.

### 9.8 `NUM-0001` classification and review conditions — the procedure's own constants, not just its output

Both class-5 constants this procedure introduces — the `100.00 / 6` starting-baseline formula
(§9.2) and the `±2.00` percentage-point increment (§9.4) — are themselves `NUM-0001` class 5
provisional governance guardrails, carrying the same "not empirically optimized, explicitly
labeled, review-conditioned" treatment `NUM-0001` §6 requires of the 1.8x leverage cap and 30%
buffer floor. Stated review condition for both: revisit upon the first descriptive risk analysis
or targeted backtest performed under `roadmap_preservation` items (5)/(12) (explicitly scoped to
challenge provisional sizing, not to gate it — §14, unchanged); upon a material change to the
sealed six-sleeve population or the seven-sealed/eight-deferred relationship-pair accounting; or
upon a future, separately authorized evidence-bounded or empirically-calibrated study of either
constant specifically. A met review condition requires explicit future governance attention
(`NUM-0001` §12) — it does not, by itself, automatically change either constant or any value this
procedure has already produced.

### 9.9 Why a single provisional point, not a range — strengthened, on its own merits

The corrected procedure (§§9.1-9.7) is now fully deterministic: given the same sealed evidence,
it produces exactly one number per sizing-eligible sleeve, not a distribution or an admissible
set. Introducing a numeric range or band around that already-exact computation would misrepresent
where this procedure's real uncertainty actually lives — not in the arithmetic (which is exact and
reproducible by construction, §9.7), but in the two underlying class-5 constants themselves
(§9.8), which are already carried as explicitly-labeled, review-conditioned provisional values
rather than folded into a fabricated width around the output. A range would also blunt, rather
than sharpen, the downstream challenge process `roadmap_preservation` already anticipates:
descriptive risk analysis and targeted backtests (items (5)/(12)) are designed to test a concrete
figure and either corroborate or revise it — a range gives that future work nothing precise to
test against, and risks the range itself silently widening or narrowing across revisions with no
governed tracking, exactly the kind of untracked-precision drift `NUM-0001` §9 warns against. This
repository's own direct, load-bearing precedent — the 1.8x leverage cap and 30% buffer floor,
both exact single points under comparable epistemic conditions, neither expressed as a range — is
the closest analogue and is followed here deliberately, not merely cited as a label of
convenience.

### 9.10 No real-sleeve reachability table — disclosure-only fact, no longer part of the numeric procedure

**Superseded by this document's own second bounded correction.** The original version of this
section published a table showing which sizing-eligible sleeve independently reached R1's ("full
Axis-A-basis coverage") own reachability threshold, reasoning that R1 was a binary,
non-comparative trigger whose reachability for each sleeve was already stated in plain prose in
`XASSET-0015` §C, and that publishing it here therefore added no new numeric-leakage risk beyond
what was already public. With R1 withdrawn as a numeric trigger (§9.3), that reasoning no longer
applies to a *derivation-procedure* section: the Axis-A-basis-completeness fact no longer feeds
this procedure's arithmetic at all, so a table of its reachability has nothing left to
"demonstrate as well-defined and auditable" for the derivation itself — it would be pure
restatement of an already-public fact (`XASSET-0015` §C), serving no purpose specific to this
methodology document. **No table is published in this section.** The fact itself remains
available, as it always was, in `XASSET-0015` §C directly, and a future implementation session's
own `uncertainty_disclosure` field may cite it there (§9.3).

The comparative triggers actually governing this procedure's arithmetic, R2 and R3, are — as
before this correction — never disclosed here for any real sleeve: publishing either trigger's own
directional outcome (up, down, or none) for `equity`, `fund_gld_defensive`, or `crypto`, combined
with this document's own published `starting_baseline_pct` (§9.2) and increment (§9.4) constants,
would let a reader mechanically derive a specific `provisional_target_pct` value — precisely the
"calculate actual percentages" outcome this filing's own authorizing instruction repeatedly,
explicitly prohibits. **No starting baseline, no adjustment arithmetic, no R2/R3 directional
outcome, and no resulting `provisional_target_pct` value is computed, stated, or implied for any
real sleeve anywhere in this filing.** A future implementation session must independently perform,
and disclose, the full application of §9.2-§9.7 to real sealed evidence.

A full synthetic (non-real-sleeve, fictional-constant) walkthrough demonstrating the procedure's
determinism, including several adversarial and boundary configurations, is in §21.

## 10. Sum/reconciliation rule — no silent plug, cash included

Forcing the three sizing-eligible sleeves' `provisional_target_pct` values to sum to 100.00% would
silently assign the three blocked sleeves a de facto 0.00% by arithmetic necessity — the exact
numeric-leakage risk §6 exists to prevent, only reached indirectly through the total rather than
through any single blocked sleeve's own field. This repository already has a live, accepted
precedent for the opposite discipline: `PHQ-2026-04` (2026-08-01) removed 0.75% of `targets.yaml`'s
own destination weight without renormalizing the remainder, recording explicitly that "the removed
0.75% is unallocated cash, not redistributed" — the identical principle this filing applies one
layer up, at the sleeve level rather than the instrument level.

**Rule**: `COHORT_MANIFEST.yaml` for the `numeric_sizing/` sub-namespace carries a mechanically
computed (never self-declared) `portfolio_reconciliation` block:

```
sum_of_assigned_targets_pct        # sum of every populated provisional_target_pct, computed
                                    #   live by the validator, never trusted from any record's
                                    #   own claim
unsized_reserved_capital_pct       # 100.00 - sum_of_assigned_targets_pct, floored at 0.00,
                                    #   two decimal places, deterministic rounding (SS12)
reconciliation_identity_holds      # boolean, mechanically checked:
                                    #   sum_of_assigned_targets_pct +
                                    #   unsized_reserved_capital_pct == 100.00 exactly
unsized_capital_disclosure         # required, non-empty, fixed-shape text stating that the
                                    #   unsized/reserved figure represents capital not yet
                                    #   assigned to any sleeve pending resolution of a blocked
                                    #   sleeve's own status or additional evidence -- never a
                                    #   cash-allocation decision, never redistributed to any
                                    #   sized sleeve without its own future governance act
```

`unsized_reserved_capital_pct` is a **residual accounting figure**, not a sleeve, not
`cash_reserve`, and not itself a numeric target of any kind — it may never be read as "the
portfolio should therefore hold this much cash," restated explicitly in the required disclosure
text and enforced by a dedicated scan (§14 item 9) rejecting any free-text conflation of the
unsized bucket with the `cash_reserve` sleeve specifically.

## 11. `cash_reserve` — blocked, never used as an implicit residual

`cash_reserve` is itself `sizing_blocked` today (§3) — it may not receive a `provisional_target_pct`
of its own under §6's rule, and it may **not** be used, mechanically or by drafting convenience,
as the sleeve that silently absorbs whatever the sizing-eligible sleeves' targets leave
unaccounted for (§10's own `unsized_reserved_capital_pct` performs that accounting function
instead, as a distinct, non-sleeve-shaped figure). Treating a currently-blocked sleeve as the
system's automatic residual would grant it, through the back door, exactly the numeric candidacy
its own sealed `sizing_blocked` disposition withholds. The unresolved `CASH`/`RESERVE`
consolidation question (`XASSET-0008` §N) is unaffected, unreopened, and unresolved by this
filing.

## 12. `debt_reduction` — one competing use among six, currently unsized, not outside the denominator

`XASSET-0001` §D frames cash/reserve, GLD, and debt reduction as "competing uses of capital... as
an explicit Level 1 sleeve-allocation input, governed by the same opportunity-cost discipline as
every other sleeve, not treated as a residual or an afterthought." `debt_reduction` therefore
belongs conceptually within the same 100%-of-incremental-capital accounting every other sleeve
occupies — it is not carved out as a separate, pre-investment decision sitting outside Level 1's
own scope, and it is not treated as a special case requiring its own denominator. It simply has no
`targets.yaml` row (it is a margin-policy lever, not an asset class) and, today, no numeric
candidate at all, because its own sealed Axis B is mechanically forced `not_yet_eligible`. Its
share of the eventual 100% — whatever that turns out to be, once its own economic-assessment gap
(`DEBT_REDUCTION.yaml`'s forced `assessment_required` sub-fields) is separately closed — folds into
`unsized_reserved_capital_pct` exactly like every other currently-blocked sleeve, with no
mechanical exception.

## 13. Valuation-input treatment — sleeve-level evidence, not instrument-level completeness

Level 1 sizing is a sleeve-level question; it does not require every Level 2 instrument inside a
sleeve to be fully valued. The `equity` sleeve's own valuation corpus is genuinely incomplete —
18 of 27 canonical equities reach `valuation_results: completed`, 9 reach `partial`, and
`discount_rate_evidence` is abstained on all 27 (`VALUATION-0004`-`VALUATION-0007`, unedited,
unreopened here) — but this is disclosed **context**, not a blocker to `equity`'s own Level 1
sizing eligibility, which is already governed by Axis A/B/C (§3), not by instrument-level
valuation completeness. A future implementation's `uncertainty_disclosure` field for `equity`
must cite this gap by name (the 9 `partial` results, the universal discount-rate abstention) as
one of the reasons its own provisional figure carries disclosed uncertainty — it must not wait for
full Level 2 valuation completeness before proceeding, matching `TIER-0009` §K's own established
precedent of proceeding on disclosed partial equity-valuation evidence elsewhere in this
repository. No future implementation may claim `equity`'s Level 1 sizing is validated by, or
requires, Level 2 valuation completeness it does not have. **Chosen treatment, stated explicitly
(added by this bounded correction)**: valuation evidence is **disclosure-only** — it is not one of
§9.3's three numeric triggers, it never constrains a maximum, and it never forces a downward
adjustment; its sole effect is a mandatory citation inside `equity`'s own `uncertainty_disclosure`
field (§8).

## 14. Minimum pre-sizing risk constraints

`operations/WORKSTREAMS.yaml`'s own already-recorded `roadmap_preservation` sequencing (unedited,
restated here, not invented) places descriptive risk analysis and targeted backtests **after**
provisional sizing, to challenge and refine it — not as a universal precondition to any sizing at
all. This filing does not move that sequencing. The only constraints that must already be
respected before a future implementation produces a provisional figure are the constraints already
governed and already binding, none newly authored here:

- the 1.8x leverage cap and 30% margin-buffer floor remain unchanged and are, in any case,
  structurally inapplicable — sizing under this filing is explicitly unlevered (§10's own 100.00%
  identity assumes no leverage; nothing in this filing computes, cites, or relies on borrowing
  capacity);
- `targets.yaml`'s existing `caps.clusters` (semis, power_infra) and the 8%/40% issuer/AI-platform
  no-add ceilings are Level 2, equity-instrument-level constraints — not directly binding on a
  Level 1 sleeve figure, but a future implementation's `uncertainty_disclosure` for `equity` may
  note their existence as forward context for the Level 2 work that would eventually follow;
- the six already-sealed `computed_from_existing_mechanism` overlap-model dimensions must be
  consulted as disclosed context where they bear on a sizing-eligible sleeve (§9) — no new overlap
  or concentration model may be invented, and the four `not_yet_computable_interface_only`
  dimensions may never be cited as though they were computed.

No new descriptive-risk-analysis or backtest work is authorized or required by this filing before
a future implementation may proceed — doing so would move roadmap item (5)/(12) ahead of item
(7)-(8) in a sequencing this repository's own register does not require.

## 15. Level 1/Level 2, margin, and chart boundaries — restated, not redesigned

- **Level 1/Level 2**: no future numeric-sizing record may name, weight, or size an individual
  equity, ETF, or coin — the existing `XASSET-0012` §9 item 9 leakage scan, already proven against
  this exact corpus by three prior implementations, is reused unmodified.
- **Margin**: sizing under this filing is unlevered; no future implementation may cite the leverage
  cap or buffer floor as a means of enlarging any sleeve's provisional figure. Margin/leverage
  research remains its own, later, separately authorized roadmap item, reusing `MARGIN-0005`'s
  existing charter.
- **Chart/deployment**: chart evidence remains strictly downstream — it may never inform, adjust,
  or override a provisional Level 1 figure. `TIER-0003`/`XASSET-0001` §G are restated, not
  reopened.
- **Allocation check**: no real, live, or scenario allocation check is authorized by this filing or
  by the future implementation it authorizes. A real allocation check remains downstream of
  completed Level 1 sizing, Level 2 instrument sizing, required risk/overlap validation, and
  unlevered-portfolio validation, in that order — `OPS-0007` §5's own narrow, already-bounded
  scenario-display bridge is neither reactivated nor referenced as a shortcut.

## 16. Provisional, not adopted — scenario framing

Every `provisional_target_pct` value a future implementation populates is a **governance-derived,
disclosed, provisional finding** — the direct sleeve-level analogue of `VALUATION-0007`'s own
equity-level `valuation_results`, which likewise require their own separate, later, explicit
adoption decision before influencing any tier, target, or trade. No numeric-sizing record, however
complete, creates, implies, or authorizes any `targets.yaml` change, any trade, or any allocation
check on its own. Adoption of any Level 1 figure as controlling policy — should that ever occur —
requires its own separate, future, explicit governance decision with its own independent-review
lifecycle, exactly the same non-collapsing discipline `XASSET-0014` §K/`TIER-0011` §K already
apply one layer up.

## 17. Precision and rounding

Two decimal places, matching `targets.yaml`'s own existing `target_pct` convention (verified live
this session: every one of its 36 rows carries exactly two decimal places). Every populated
`provisional_target_pct` and every `portfolio_reconciliation` field is in `[0.00, 100.00)` for an
individual sleeve — no negative value is authorized under any circumstance, and no single sleeve
may be assigned `100.00` (that would leave zero room for the other five, an outcome no disclosed
evidence today supports and this filing does not pre-judge). The future validator must define one
explicit, deterministic rounding rule (e.g., round-half-even) and apply it uniformly across every
computed field — any sub-cent residual from that rounding is absorbed into
`unsized_reserved_capital_pct`, never silently distributed across the sized sleeves and never
causing `reconciliation_identity_holds` to report `true` on a value that does not actually sum
exactly. **Added by this bounded correction**: the future validator must reject, not silently
tolerate, a stored `sum_of_assigned_targets_pct` that exceeds `100.00` before residual flooring
and a stored literal negative `unsized_reserved_capital_pct` — named explicitly, and no longer
left merely implicit in the exact-identity requirement above, as §19 items 20-22's own dedicated
adversarial tests.

## 18. NUM-0001 classification — required on every populated value

Every populated `provisional_target_pct` is classified, structurally and without exception, as
`NUM-0001` §1 class 5 — **provisional governance guardrail**: "a deliberately conservative interim
value adopted under incomplete evidence, explicitly labeled as such, with a stated review
condition" — the same class the 1.8x leverage cap and 30% buffer floor already carry. No
`provisional_target_pct` may be labeled class 3 (empirically calibrated) — no empirical sweep or
backtest has yet evaluated any candidate figure, and `NUM-0001` §8 is explicit that only evidence
directly and uniquely favoring a specific number over tested alternatives qualifies for that
label. `target_classification` is therefore a forced constant, not a drafting choice, and a future
validator must reject any other value (§14 item 5 below).

## 19. Future validator/test specification

A future, separately authorized implementation must build a dedicated Stage 5 section (or module),
zero import coupling with `allocate.py`/`margin_state.py`, covering at minimum:

1. Closed schema at every nesting level (envelope, `portfolio_reconciliation` block, manifest row)
   — extra-key rejection, not merely missing-key checks.
2. Exactly six `sleeve_id` values, at most one numeric-sizing record per sleeve, all six present
   (never omitted).
3. Live, independent recomputation of `policy_adoption_reference`'s hash, never trusted from a
   stored value.
4. **Mechanical `numeric_target_status` re-derivation** — a dedicated test proving a record
   claiming `provisional_target_assigned` while its cited `policy_adoption` record's own
   `sizing_readiness_status` is `sizing_blocked` is rejected, and the converse (a `sizing_blocked`
   sleeve claiming `no_provisional_target_pending_axis_c` while its own cited disposition is
   `sizing_conditionally_ready`/`sizing_ready` without a populated target is also rejected).
5. **`target_classification` forced-constant check** — a dedicated test proving any value other
   than `provisional_governance_guardrail` is rejected, and that the field is `null` if and only
   if `provisional_target_pct` is `null`.
6. **`provisional_target_pct` bounds** — `[0.00, 100.00)`, two-decimal precision, non-negative,
   rejection of any value `>= 100.00`.
7. **Reconciliation-identity check** — a dedicated test proving
   `sum_of_assigned_targets_pct + unsized_reserved_capital_pct == 100.00` exactly, live-recomputed
   from the six real records, never trusted from the manifest's own self-declared value.
8. **`stronger_evidence_maturity` non-influence, extended** — the counterfactual-masking proof and
   presence-independent regression guard `XASSET-0014` §21 items 5/24 already require, re-run
   against `provisional_target_pct` specifically: masking every `favored_sleeve_id` must not
   change any populated numeric value.
9. **Cash/unsized-bucket conflation scan** — a dedicated free-text scan rejecting any claim that
   `unsized_reserved_capital_pct` is, represents, or should become a `cash_reserve` allocation.
10. Zero score/rank/composite-key scan, reused from `XASSET-0012`/`XASSET-0014`'s own design,
    unmodified.
11. The Level 1/Level 2 leakage scan (`XASSET-0012` §9 item 9), reused unmodified.
12. Zero word-boundary-matched directive/trading language, chart-domain terminology, and
    `CASH`/`RESERVE`-distinction-language scans — all three reused from the Stage 4 validator's own
    already-hardened implementation, unmodified.
13. Adversarial test coverage for ordering, negation, punctuation, conjunction, active/passive
    voice, and euphemistic paraphrase on every scan in items 9-12, with mandatory false-positive
    guards, matching this repository's own now-standard discipline for every prior scan in this
    chain.
14. A dedicated protected-path/byte-identity test proving every one of the six sealed
    `policy_adoption` records, the six `sleeve_profile` records, the seven `sleeve_relationship`
    records, and every other pre-existing sealed Intelligence record remains untouched before and
    after the future implementation.
15. Manifest bidirectional reconciliation (hash, duplicate, missing, extra, orphan) for the new
    `numeric_sizing/` sub-namespace.
16. Non-cascading abstention discipline — a `no_provisional_target_pending_axis_c` disposition on
    one sleeve never forces or implies a value on another sleeve's own record.

**Added by the first bounded correction (resolving independent review
`pullrequestreview-4916420679`'s MAJOR and MINOR findings):**

17. **Full live re-derivation of `provisional_target_pct` — the central new requirement.** The
    future validator must not merely check that a stored `provisional_target_pct` falls in
    `[0.00, 100.00)`. For every populated record, it must independently recompute
    `starting_baseline_pct` (§9.2), independently re-evaluate both triggers R2/R3 (§9.3)
    against the sleeve's own cited, live-hash-verified `policy_adoption`/`sleeve_relationship`
    evidence, independently apply §9.4's fixed increment for every trigger that actually fires,
    and reject the record outright if the live-rederived value does not exactly match the stored
    `provisional_target_pct`, the stored `starting_baseline_pct`, or the stored
    `applied_adjustments[]`/`governing_rule_ids[]` — the same "mechanically re-derived, never
    trusted from a stored value" discipline this exact record chain already applies to
    `numeric_target_status` (§8) and `capital_eligibility_status` (`XASSET-0014` §4/§21 item 4),
    generalized here to the numeric layer itself.
18. **Comparative-consistency enforcement** — a dedicated test proving that any two sizing-eligible
    sleeves sharing byte-identical R2/R3 trigger outcomes are rejected if their stored
    `provisional_target_pct` values differ, and that any two sleeves with differing
    `provisional_target_pct` values are rejected unless at least one `applied_adjustments[]` entry
    differs between them and each cites a matching `comparative_consistency_note` (§8, §9.7 item 2).
19. **Determinism test** — a dedicated test running the full §9.1-§9.7 derivation twice against the
    same synthetic sealed-evidence fixture and asserting byte-identical `starting_baseline_pct`,
    `applied_adjustments[]`, and `provisional_target_pct` output both times (§9.7 item 1).
20. **Pre-floor sum-overshoot rejection** — a dedicated adversarial test proving that a stored
    (not live-computed) `sum_of_assigned_targets_pct` exceeding `100.00` **before** residual
    flooring is rejected outright by the validator, never silently absorbed by a
    `max(0, 100.00 - sum)`-style floor on `unsized_reserved_capital_pct` — the floor applies only
    to the live-computed residual itself (§9.6), never as a mechanism for tolerating an
    out-of-bounds stored sum. §9.4/§9.5's own corrected bound makes this overshoot unreachable by a
    correctly-implemented derivation (the maximum possible three-sleeve sum is `3 x 20.67 =
    62.01`, well under `100.00`) — the test exists precisely because a stored record must never be
    trusted merely because the procedure that *should* have produced it is bounded.
21. **Negative stored-residual rejection** — a dedicated adversarial test proving that a manifest
    submitting a literal negative `unsized_reserved_capital_pct` is rejected outright, even though
    live computation (§9.6, floored at `0.00`) can never produce one — the same "never trust a
    stored value" discipline as item 20, applied to the residual field specifically.
22. **Neighboring-arithmetic adversarial cases** — dedicated tests for: `sum_of_assigned_targets_pct
    == 100.00` exactly (residual `0.00`, valid); `sum == 100.01` (invalid, rejected per item 20);
    `unsized_reserved_capital_pct == 0.00` (valid); `unsized_reserved_capital_pct` stored negative
    (invalid, rejected per item 21); a `provisional_target_pct`/`starting_baseline_pct` stored at
    excess precision (e.g. three or more decimal places — rejected, matching §17's two-decimal-
    place requirement); and a sub-cent rounding-drift case where the live-computed sum and the
    stored sum differ only in the last decimal place (rejected — item 17's exact-match requirement
    admits no tolerance).
23. **`starting_baseline_pct` uniformity check** — a dedicated test proving every populated
    record's `starting_baseline_pct` equals the identical `100.00 / 6` constant (§9.2) — never
    sleeve-specific, never self-declared at a different value.
24. **`applied_adjustments[]` magnitude/direction check** — a dedicated test proving every entry's
    `magnitude_pct` equals exactly `2.00` (§9.4, never a different value) and that no sleeve
    carries more than one `applied_adjustments[]` entry per named `governing_rule_id` (each trigger
    fires at most once per sleeve, §9.3).

**Added by this second bounded correction (resolving independent review
`pullrequestreview-4916848704`'s two new MAJOR findings):**

25. **`R1`-retirement enforcement** — a dedicated adversarial test proving that any
    `applied_adjustments[]` or `governing_rule_ids[]` entry citing `governing_rule_id: R1` is
    rejected outright, regardless of its own stated `direction`/`magnitude_pct`/`evidence_ref` —
    R1 is withdrawn as a numeric trigger by this document's own second bounded correction (§9.3)
    and is structurally not a member of the closed `R2 | R3` enum; this test exists specifically so
    a future implementation session cannot silently resurrect the withdrawn trigger by supplying an
    otherwise well-formed entry under its old identifier. A companion test must independently
    confirm that item 1's closed-schema/extra-key rejection alone is not being relied upon as the
    only backstop — this item's own test constructs an entry that is otherwise fully schema-valid
    except for the retired `governing_rule_id`, isolating the check from item 1's more general
    coverage.

## 20. Sequence — this filing does not collapse into the future implementation

1. **This filing** — methodology design plus a bounded authorization for one future
   implementation covering the population §3 already fixes. No numeric content populated.
2. **The future implementation** — its own separate, bounded PR, requiring its own full
   independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification
   lifecycle, populating the six records and the reconciliation block per §§7-19.
3. **Adoption, if it ever occurs** — its own separate, later, explicit governance decision (§16),
   not authorized, scheduled, or implied by either of the above.

No sub-step above may be collapsed into another by this design or by any future filing acting
under it.

## 21. Synthetic procedure walkthrough — fictional labels, fictional constants, no real percentages

**Added by the first bounded correction; rewritten by this document's own second bounded
correction to exercise the corrected two-trigger system directly.** Every value below uses
**deliberately fictional** labels, population size, baseline, and increment — **`W`/`X`/`Y`/`Z`/`Q`
are not any real sleeve, `20.00%` is not this filing's real `16.67%` baseline, and `5.00` is not
this filing's real `2.00` increment.** This separation is intentional: reusing the real constants
here, even with fictional sleeve labels, would let a reader mechanically combine an illustrated
trigger pattern with this filing's own real, already-published baseline/increment and arrive at a
real sleeve's actual figure — exactly the outcome §9.10 and this filing's own authorizing
instruction prohibit. This section demonstrates only that §§9.1-9.7's *mechanism* is
deterministic, bounded, and self-consistent — never that any real sleeve resolves to any
particular value.

**Fictional setup**: a closed, five-member taxonomy (`W`, `X`, `Y`, `Z`, `Q`); three members
(`A`, `B`, `C` — standing in for whichever three happen to be sizing-eligible) are eligible;
`Z`/`Q` are blocked. Fictional baseline = `100.00 / 5 = 20.00`. Fictional fixed increment =
`±5.00` per firing trigger. **Exactly two fictional triggers** — an "R2-equivalent" (relative
relationship-coverage strength) and an "R3-equivalent" (relative secondary-condition breadth) —
mirroring the real, corrected §9.3, since this document's own withdrawn third trigger (R1,
retired to disclosure-only) is not part of the numeric procedure and has no fictional
counterpart here.

**Case 1 — no trigger fires for any member (identical evidence).** `A`, `B`, `C` each stay at the
unadjusted baseline: `20.00` each. `sum_of_assigned_targets_pct = 60.00`.
`unsized_reserved_capital_pct = 40.00`. Reconciliation: `20.00 + 20.00 + 20.00 + 40.00 = 100.00`
exactly.

**Case 2 — R2-equivalent trigger: up, a tie, and the tie's own non-fire.** `A` carries the strict,
unique fewest count of the R2-equivalent measure — fires **up**. `B` and `C` are tied at the
(shared) unique-most count — a tie is not evidence of a difference, so **no** R2-equivalent
adjustment fires for either, even though both sit at the nominal "most" extreme. Result:
`A = 20.00 + 5.00 = 25.00`, `B = 20.00`, `C = 20.00`. `sum = 65.00`. `residual = 35.00`.
Reconciliation: `25.00 + 20.00 + 20.00 + 35.00 = 100.00` exactly. This demonstrates both the
**up** direction and the **tie-suppresses-the-down-side** rule in one case — a condition that
would fire under a naive "not-unique-fewest" reading is correctly withheld once the tie is
recognized.

**Case 3 — R3-equivalent trigger: up and down, no tie.** `A` carries the strict, unique fewest
secondary-condition-type breadth — fires **up**. `B` sits at a middle breadth shared by no other
member — no fire. `C` carries the strict, unique most breadth (the overlap-equivalent condition
included) — fires **down**. Result: `A = 20.00 + 5.00 = 25.00`, `B = 20.00`,
`C = 20.00 - 5.00 = 15.00`. `sum = 60.00`. `residual = 40.00`. Reconciliation holds exactly. This
demonstrates a disclosed condition being carried into the number, not merely narrated in prose —
directly answering the requirement that a disclosed condition must actually move the figure, not
sit unused beside it — for both directions of the second trigger.

**Case 4 — both triggers fire on the same member: the true synthetic minimum and maximum.**
`A` independently clears both the R2-equivalent **up** condition and the R3-equivalent **up**
condition — `20.00 + 5.00 + 5.00 = 30.00`, the true synthetic **maximum** reachable by this
fictional setup. `B` independently clears both the R2-equivalent **down** condition and the
R3-equivalent **down** condition — `20.00 - 5.00 - 5.00 = 10.00`, the true synthetic **minimum**.
`C` is untouched by either trigger — `20.00`. Result: `sum = 30.00 + 10.00 + 20.00 = 60.00`.
`residual = 40.00`. Reconciliation: `30.00 + 10.00 + 20.00 + 40.00 = 100.00` exactly. This is the
fictional-setup analogue of §9.4's corrected real bound: with exactly two triggers, each
independently capable of firing `up`/`down`/neither, the reachable per-member range is
`[baseline - 2 x increment, baseline + 2 x increment]` — here `[10.00, 30.00]`, and, in the real
setup (§9.4), `[12.67, 20.67]` — never a range built from three triggers, and never asymmetric,
since both remaining triggers are structurally identical in shape (each can fire in either
direction).

**Case 5 — two members (`A`, `B`) with byte-identical trigger-evaluation inputs, hypothetically
stored with different targets.** Under §9.7 item 2, `A` and `B` sharing identical R2/R3 outcomes
**must** receive identical `provisional_target_pct` values — there is no remaining discretion
after the triggers are evaluated. A stored record claiming, hypothetically, `A = 22.00`/
`B = 18.00` despite provably identical inputs would be rejected by two independent future
validator checks: item 17 (live re-derivation — `A`'s and `B`'s own live-rederived values would
both equal the same baseline-plus-identical-adjustments figure, and at least one stored value
would fail to match its own re-derivation) and item 18 (comparative-consistency — no
`applied_adjustments[]` entry differs between `A` and `B`, so a stored difference between them is
rejected outright regardless of any `comparative_consistency_note` text supplied).

**Case 6 — an attempted total exceeding 100%.** With exactly two fictional triggers bounded to
`±5.00` each (Case 4's own corrected shape — never three, and never `±15.00` per member), the
maximum possible net adjustment per member is `±10.00`, bounding any single member to `[10.00,
30.00]` and the maximum possible three-member sum to `90.00` in the fictional setup — already
tight, and, in this filing's own **real** setup (§9.4), the corrected real bound (`3 x 20.67 =
62.01`) makes a sum anywhere near `100.00` structurally unreachable by a correctly-implemented
derivation. A hypothetical corrupted or erroneous stored manifest claiming
`sum_of_assigned_targets_pct = 105.00` regardless — pre-flooring, and well beyond even the
fictional fully-adjusted theoretical maximum of `90.00` — is rejected outright by item 20; the
validator never silently computes `unsized_reserved_capital_pct = max(0, 100.00 - 105.00) = 0.00`
and lets the overshoot pass unflagged.

**Case 7 — exact reconciliation.** Demonstrated in Cases 1-4 above: in every case,
`sum_of_assigned_targets_pct + unsized_reserved_capital_pct` equals `100.00` exactly, by
construction (§9.6), never approximately.

Every case above is deterministic given its own stated inputs — two independent applications of
§§9.1-9.7 to the same fictional evidence configuration produce the same fictional result each
time, the property §9.7 item 1 requires of the real mechanism.
