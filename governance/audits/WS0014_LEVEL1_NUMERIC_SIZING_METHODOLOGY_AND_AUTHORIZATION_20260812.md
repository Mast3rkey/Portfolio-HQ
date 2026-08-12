# WS-0014 Level 1 Numeric Sleeve-Sizing Methodology and Bounded Authorization

**Date**: 2026-08-12
**Governing decision**: `governance/decisions/XASSET-0016-ws0014-level1-numeric-sizing-methodology-and-authorization.md`
**Status**: Methodology design plus a bounded future-implementation authorization. No numeric
Level 1 target is computed, populated, or implied by this artifact or its governing decision. No
`targets.yaml`, `holdings.yaml`, or allocator change of any kind. No allocation check.

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

| `sleeve_id` | Axis A | Axis B | Axis C | Secondary conditions bearing on it |
|---|---|---|---|---|
| `equity` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | Every one of its 5 sealed relationship pairs carries `evidence_partial_present`/`forced_abstention_present` (at least one); zero `deferred_disclosed` pairs — the only sleeve with a fully `sealed_determined` ledger. |
| `fund_broad_market` | `function_status_unresolved` | `eligible_for_target_consideration` | `sizing_blocked` | Blocked via the Axis A gate alone (`XASSET-0014` §22 Case G) — Basis 1 unavailable, Basis 2 not asserted, Basis 3 available but this session's own drafting discretion (`XASSET-0015` §E) landed on the unresolved reading. 4 of 5 pairs `deferred_disclosed`. |
| `fund_gld_defensive` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | All three lawful Axis A bases available — the strongest evidentiary support of any non-equity sleeve. 3 of 5 pairs `deferred_disclosed`. |
| `crypto` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_conditionally_ready` | Basis 1 + Basis 3. 3 of 5 pairs `deferred_disclosed`; sleeve-wide forced abstention on `cross_coin_correlation_status`. |
| `cash_reserve` | `function_confirmed_distinct` | `eligible_for_target_consideration` | `sizing_blocked` | Forced by its own `sealed_unresolved` pair against `debt_reduction` (`XASSET-0014` §22 Case D). Carries the mandatory `cash_reserve_consolidation_note`. |
| `debt_reduction` | `function_confirmed_distinct` | `not_yet_eligible` | `sizing_blocked` | Axis B mechanically forced by `forced_abstention` evidence coverage; also its own `sealed_unresolved` pair against `cash_reserve`. No `targets.yaml` row exists for this sleeve at all. |

**Zero sleeves reach `sizing_ready`.** Three (`equity`, `fund_gld_defensive`, `crypto`) reach
`sizing_conditionally_ready`. Three (`fund_broad_market`, `cash_reserve`, `debt_reduction`) reach
`sizing_blocked`. This split is not a judgment this filing makes — it is a mechanical fact already
sealed in the six Stage 4c records, independently re-verified above, unchanged by anything in this
filing.

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
                                  #   never negative; never >= 100.00 for a single sleeve
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
                                  #   records; (c) disclosed valuation/evidence-coverage gaps
                                  #   per SS11 -- never a fabricated caveat, never omitted
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

## 9. `stronger_evidence_maturity` and opportunity-cost evidence — extended prohibition, not a new rule

`XASSET-0014` §6 already mechanically prohibits `stronger_evidence_maturity`/`favored_sleeve_id`
from driving any of the three categorical axes. This filing extends the identical prohibition, by
the same logic, one layer further: **no `provisional_target_pct` value or any formula computing
one may read `favored_sleeve_id`, use it as a multiplier, a ranking input, or any other numeric
influence.** If a categorical axis may not be moved by an evidence-maturity finding, a raw
percentage — a strictly more consequential, more numerically legible output — certainly may not
be either. A future implementation's `uncertainty_disclosure` field (§8) may *name* that a
`stronger_evidence_maturity` finding exists and disclose what it says about relative evidence
completeness, but the cited finding may never be converted into, or read as justifying, a specific
number.

Permitted opportunity-cost inputs for a future implementation's own (categorical, not formulaic)
judgment in choosing a `provisional_target_pct` value: the sleeve's own Axis A evidentiary
strength (how many of the three lawful bases independently clear — `fund_gld_defensive`'s three
versus `crypto`'s two is a real, disclosable distinction, cited descriptively, never converted
into an arithmetic multiplier); the sleeve's own count and severity mix of `sealed_determined`
versus `deferred_disclosed` relationship pairs; named secondary conditions on its own relationship
records; and the six already-sealed `computed_from_existing_mechanism` overlap-model dimensions
(never the four `not_yet_computable_interface_only` ones, restating `XASSET-0013` §G's own
citation rule at this layer). None of these inputs may be assembled into a hidden weighted-sum
score, an implicit ranking, or any mechanism a future reader could reconstruct as a formula — the
governance judgment itself, disclosed in free text, is the mechanism; no numeric proxy for it may
be smuggled into the schema.

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
requires, Level 2 valuation completeness it does not have.

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
exactly.

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
