# WS-0014 `fund_broad_market` Level 1 Role Redetermination

**Date**: 2026-08-12
**Governing decision**: `governance/decisions/XASSET-0017-fund-broad-market-role-redetermination.md`
**Status**: Evidence-only redetermination. No other sleeve's `policy_adoption` record touched. No
numeric Level 1 or Level 2 content of any kind populated, computed, or authorized. `XASSET-0014`/
`XASSET-0015`/`XASSET-0016`'s own text unedited.

## 0. Purpose and scope

`XASSET-0016` (Stage 5's own methodology and bounded authorization for numeric Level 1 sleeve sizing)
is confirmed merged (`PR #307`), but no `numeric_sizing` record has yet been populated under it. Before
that future implementation begins, the controlling principal directed a bounded re-application of
`XASSET-0014`'s own already-accepted Axis A/B/C methodology to `fund_broad_market`, the one sleeve
whose original Stage 4c determination (`function_status_unresolved`) was explicitly, deliberately left
open to future reconsideration by `XASSET-0015` §E. This artifact records the full evidentiary
walk-through; the governing decision file records the operative determination and its consequences.

## 1. Reproducing the prior block, basis by basis

`fund_broad_market.yaml`'s prior sealed `function_rationale` (verbatim, before this filing's edit):

> "None of the lawful evidentiary bases is currently available in a form sufficient to reach
> `function_confirmed_distinct`... Basis 1 (relationship-record finding) is unavailable... Basis 2...
> is not asserted... Basis 3 (structural sleeve-definition basis) is mechanically available... That
> structural fact establishes only that the evidentiary path to a future `function_confirmed_distinct`
> finding now exists... This session judges that isolated, purely categorical fact insufficient on its
> own -- with no offsetting evidence anywhere in this sleeve's own sealed corpus -- rather than reading
> Basis 3's mere availability as a presumptive positive answer."

Independently reproduced this session, before any edit:

| Basis | Prior determination | Independently reconfirmed this session |
|---|---|---|
| Basis 1 (relationship-record finding) | Unavailable — sole relationship (`equity_fund_broad_market`) resolves `stronger_evidence_maturity` | **Unchanged, confirmed unavailable** — same relationship record, same hash (`8667974b...`), same disposition |
| Basis 2 (`CLAUDE.md` doctrine citation) | Not asserted — no dedicated passage identified | **Unchanged, confirmed not asserted** — a full-repository search for a `fund_broad_market`/broad-market-index-sleeve-specific doctrine passage, independent of `SPY`/`VEA`/`VWO`'s own individual disclosures, found none; none is manufactured here |
| Basis 3 (structural `targets.yaml` category membership) | Available, judged insufficient in isolation | **Unchanged availability, live-reconfirmed** — `targets.yaml`'s `fund` rows still scoped to `SPY`/`VEA`/`VWO` for this sleeve; re-weighed, not re-derived (§7 below) |

**Reopenability, confirmed, not assumed.** `XASSET-0015` §E's own controlling text: "This filing does
**not** convert Basis 3 into an automatic positive Axis A result... A future Stage 4c drafting session
evaluating `fund_broad_market` retains full discretion to independently judge the available evidence...
and may reach `function_confirmed_distinct`, `function_status_unresolved`, or... `unable_to_determine`,
exactly as the sealed evidence and the mechanism's own rules dictate. Nothing in this filing narrows
that discretion or pre-selects an outcome." The prior sealed record's own text independently confirms
the same: "a future drafting session could also reach a different judgment on today's identical
evidence base within that same delegated discretion, since `XASSET-0015` SS E's own text does not
pre-select an outcome." No mandatory two-basis/corroboration rule is stated anywhere in `XASSET-0014`
or `XASSET-0015` — independently confirmed by a full read of both decision files and `XASSET-0014`'s
own supporting artifact; the prior determination's own text explicitly disclaims being "a restatement
of a formal corroboration requirement the governing methodology itself states -- no such requirement is
stated anywhere in the governing text." This is reopenable discretion, not a hard block.

## 2. `SPY` — role-level evidence

`intelligence/etf_classification/SPY.yaml`: `structural_role.role_category: broad_market_beta`,
`constituent_exposure.geographic_concentration: domestic_us`, `constituent_exposure.currency_exposure:
usd_only`, `overlap_and_concentration.measured_by_existing_mechanism: true`.
`intelligence/instrument_economic_assessment/SPY.yaml`:
`cost_and_tracking_quality_economic_significance.significance_category: elevated_vs_category` — a
sourced comparison against two other major S&P 500-tracking funds found both peers charge a materially
lower cost and capture more of the index's own upside over multiple lookback periods; SPY's own
disclosed cost/tracking showing is the weakest of the three instruments in this sleeve.

**Role-level conclusion**: `SPY` strengthens the sleeve's structural existence (Basis 3's own live
`targets.yaml` fact) but is, on its own individual economic showing, the weakest case for a *distinct*
function — its domestic, USD-only, broad-market-beta exposure category structurally overlaps the
equity sleeve's own predominantly domestically-listed roster more than either other instrument in this
sleeve, and its own `elevated_vs_category` cost/tracking finding does not favor its individual
selection. This weighs **against** treating `SPY` as an independently strong contributor to a distinct
Axis A finding, but — per `XASSET-0014` §10's own binding rule — does not, by itself, license
suppressing the sleeve-level Axis A finding (§6 below).

## 3. `VEA` — role-level evidence

`intelligence/etf_classification/VEA.yaml`: `structural_role.role_category: developed_ex_us_equity`,
`constituent_exposure.geographic_concentration: developed_ex_us`, `constituent_exposure.currency_
exposure: foreign_currency_mixed`. `intelligence/instrument_economic_assessment/VEA.yaml`: `cost_and_
tracking_quality_economic_significance.significance_category: favorable_vs_category` — a sourced
comparison against two other developed-ex-US index funds found `VEA`'s own disclosed cost the lowest
of the three, with a disclosed fund-coverage-breadth caveat (broader country coverage than its named
peers).

**Role-level conclusion**: `VEA` supports a genuinely distinct geographic/diversification function.
Its own exposure category (developed markets excluding the United States, foreign-currency-mixed) has
no comparable systematic counterpart anywhere in the equity sleeve, whose own governed roster is
individually-selected, predominantly domestically-listed common stock. `VEA`'s own cost/tracking
showing is the strongest of the three instruments in this sleeve.

## 4. `VWO` — role-level evidence

`intelligence/etf_classification/VWO.yaml`: `structural_role.role_category: emerging_market_equity`,
`constituent_exposure.geographic_concentration: emerging_markets`, `constituent_exposure.currency_
exposure: foreign_currency_mixed`. `intelligence/instrument_economic_assessment/VWO.yaml`: `cost_and_
tracking_quality_economic_significance.significance_category: in_line_with_category` — a sourced
comparison against two other emerging-market index funds found `VWO`'s own disclosed cost neither
elevated nor distinctly the cheapest, sitting at the low end of its category alongside its cheapest
named peer.

**Role-level conclusion**: `VWO`, like `VEA`, supports a genuinely distinct geographic/diversification
function. Emerging-market equity exposure, foreign-currency-mixed, has no comparable systematic
counterpart in the equity sleeve's own governed roster (individually-selected common stock, no
systematic emerging-market index exposure of any kind). `VWO`'s own cost showing is unremarkable but
not disqualifying — it sits reasonably within its category.

## 5. Sleeve heterogeneity — no instrument-level unanimity required

`SPY` is materially weaker, individually, than `VEA`/`VWO`. Nothing in `XASSET-0014`'s own text
requires every instrument within a sleeve to independently satisfy Axis A's own evidentiary bar —
Basis 3 (and Basis 1/2, where available) operate at the **sleeve** level, categorically, by design; the
whole point of the Level 1/Level 2 separation this repository has maintained throughout this
undertaking is that an individual instrument's own selection quality is a Level 2 question, never an
Axis A input. `fund_broad_market`'s own already-sealed `sleeve_profile` record (a permitted `XASSET-
0014` §1 input, not a new one) already discloses this heterogeneity descriptively: "covering domestic,
developed-ex-domestic, and emerging equity exposure... a passively-managed, broadly-diversified form of
market exposure" distinct in kind from "the equity sleeve's own individually-researched, single-name
approach." Reading that already-sealed, permitted disclosure as informing (not independently
constituting) the weight given to Basis 3's own bare categorical fact is squarely within the delegated
discretion `XASSET-0015` §E reserved — it does not manufacture a fourth basis, and it does not require
`SPY` to independently clear any bar of its own.

## 6. Geographic/currency interface gap and overlap boundary

`intelligence/overlap_model/geographic_currency_exposure.yaml` remains `computation_status: not_yet_
computable_interface_only` — independently reconfirmed this session, unedited. Its own disclosed gap
is two-layered: no whole-portfolio geographic/currency aggregation mechanism exists anywhere in this
repository, **and** neither the 27 canonical equities nor the 3 crypto instruments carries a comparable
geographic/currency axis of their own to aggregate against. This filing does **not** promote the
placeholder, does **not** build a whole-portfolio rollup, and does **not** treat the per-instrument
facts already sealed on `VEA`/`VWO`'s own `etf_classification` records as a substitute for that missing
mechanism — those per-instrument facts were read only as sleeve-level role-context (§§3-4 above), never
as a portfolio-level finding.

`intelligence/overlap_model/etf_direct_equity_duplication.yaml` and `issuer_overlap_etf_lookthrough.
yaml` remain `computation_status: computed_from_existing_mechanism` — real, mechanically confirmed,
descriptive coordination evidence, unedited. `XASSET-0014` §10's own controlling text: overlap
disclosure "may never... force `fund_broad_market`'s Axis A below whatever value its own lawful
evidentiary basis... actually supports... [it] is an Axis C caveat only, never a lawful ground for
suppressing Axis A." No "overlap implies the ETF sleeve should be rejected" inference is drawn anywhere
in this filing — the disclosed overlap remains exactly what it was: a `blocking_evidence[]`/Axis C
caveat, carried forward unchanged in the resealed record.

## 7. Axis A final determination

**`function_confirmed_distinct`**, via **Basis 3** (structural `targets.yaml`-destination-category
membership, unchanged, live-reconfirmed), **informed** by `fund_broad_market`'s own already-sealed
`sleeve_profile` disclosure of genuinely heterogeneous geographic/currency exposure across its covered
funds (§5) — not a fourth basis, not a new evidentiary input, a re-weighing of the same categorical
fact in light of context already permitted under `XASSET-0014` §1. Basis 1 remains unavailable
(unchanged). Basis 2 remains not asserted (unchanged, none manufactured). `SPY`'s own weaker individual
showing and the disclosed `equity`/`fund_broad_market` overlap are explicitly, per `XASSET-0014` §10,
excluded from this determination — they remain Axis C caveats, carried forward in `blocking_evidence[]`
and `overlap_coordination_notes[]` unchanged. This is a genuine exercise of the delegated discretion
`XASSET-0015` §E reserved, not a mechanically compelled result — a differently-reasoned future session
could, in principle, reach a different judgment again on this same unchanged evidence, exactly as
`XASSET-0014` §7's own "never a permanent lock" rule states.

## 8. Supersession mechanism — alternatives considered

Three candidate mechanisms were evaluated for recording this redetermination against the sealed
record:

1. **Reseal in place, `governing_decisions` unchanged, cite `XASSET-0017` in `function_rationale`.**
   Chosen. Zero validator change; the decision-ID citation pattern is already whitelisted
   (`_DECISION_ID_LEGITIMATE_USE_PATTERN`); matches `XASSET-0014` §7's own "recomputed from scratch"
   framing for this record type; git history plus this artifact preserve full provenance.
2. **Reseal in place, widen `governing_decisions` to admit `XASSET-0017`.** Rejected — requires
   changing `validate_policy_adoption_data()`'s own hard-locked exact-set check
   (`set(governing) != {"XASSET-0014", "XASSET-0015"}`) for a fact already fully preserved via
   mechanism 1; a disproportionate validator change for no additional provenance benefit.
3. **Create a new, separate, versioned record.** Rejected — this schema has no versioning concept;
   `COHORT_MANIFEST.yaml` enforces exactly one record per `sleeve_id`; `XASSET-0014`'s own record type
   is designed as a live-derived, resealable computation, not an append-only ledger.

Mechanism 1 was applied. `level1_sleeve_synthesis_validator.py` run standalone against the resealed
record and the full corpus: `OK (7 profile result(s), 8 relationship result(s), 7 policy_adoption
result(s))`. `test_level1_sleeve_synthesis_validator.py`: three pre-existing tests updated to the newly
authorized live fixture value (renamed one non-cascading-abstention proof test whose own name asserted
the now-superseded value); full suite: 763 passed, 0 failed — matching the pre-redetermination count
exactly, confirming no test was added or removed, only three fixture expectations updated.

## 9. Numeric-sizing-eligibility consequence — categorical statement only

`fund_broad_market` becomes categorically eligible for `XASSET-0016`'s own future Stage 5 numeric
implementation to consider as a `provisional_target_assigned` candidate (mechanically derived, per
`XASSET-0016` §B's own rule, from `sizing_readiness_status == sizing_conditionally_ready`) rather than
`no_provisional_target_pending_axis_c` (the `sizing_blocked` outcome). This artifact computes **no**
`R2`/`R3` trigger state, **no** provisional percentage, and **no** reserved-capital figure — those
remain exclusively that future, separately authorized implementation's own work. `XASSET-0016`'s own
decision file (§B) states, as a point-in-time fact accurate when written, "three (`equity`,
`fund_gld_defensive`, `crypto`) are `sizing_conditionally_ready`; three (`fund_broad_market`,
`cash_reserve`, `debt_reduction`) are `sizing_blocked`" — this sentence is now stale as a live-state
citation. Per this repository's established never-silently-rewrite convention, `XASSET-0016`'s own
text is **not** edited; the staleness is disclosed here and in the governing decision's own §G, and a
future Stage 5 implementation session is directed to independently re-read the live sealed corpus
rather than trust that sentence.

## 10. Level 1 / Level 2 boundary — explicitly preserved

`SPY`/`VEA`/`VWO`'s own individual instrument weight, selection, or sizing within `fund_broad_market`
remains entirely unauthorized, unaddressed, and out of scope for this filing — a wholly separate,
later, Level 2 question. This redetermination establishes only that the sleeve has a legitimate Level 1
role; it says nothing about how any future Level 2 sizing decision should treat any of the three
instruments individually.

## 11. Bounded correction (same PR, same day)

An independent exact-head review (posted via the PR-author's own account, the disclosed same-account
platform restriction) returned 0 BLOCKING / 0 MAJOR / 1 MINOR / 3 NOTE against the original head. Every
evidentiary claim in §§1–10 above was independently re-derived by that review directly against the live
sealed records and confirmed accurate — no correction to this artifact's own factual content was
required. The one MINOR finding concerned `test_level1_sleeve_synthesis_validator.py`'s own renamed
non-cascading-abstention proof test, whose discriminating power was lost once this filing's own
redetermination made all six sleeves' `portfolio_function_status` uniformly `function_confirmed_
distinct` — resolved by correcting that test's own docstring and adding a genuinely adversarial
synthetic-fixture test, full detail in the governing decision's own Bounded Correction section. No
change to §§1–10 of this artifact.
