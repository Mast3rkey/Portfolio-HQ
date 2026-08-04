# KLAC ↔ TSM — capital_spending_dependency (KLAC depends on TSM)

Last updated: 2026-08-04 — record created through AI-assisted research and
drafting under `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
(frozen schema, taxonomy, evidence standard) and
`governance/decisions/REL-0005-ws0005-milestone4-third-relationship-content-batch-semis-tsm.md`
(this batch's own authorization). Third WS-0005 Milestone 4
relationship-content batch, following `REL-0002` (`CEG_MSFT`) and `REL-0003`
(eight further pairs).

## Source-access disclosure

This record performs **zero new external research**. Every fact below is
drawn from evidence already present in the repository at this unit's own
preflight: `intelligence/companies/KLAC.md`'s own margin-relevance evidence
section (its "Semiconductor-capex sensitivity" and "Customer concentration"
subsections); `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §5 and
`intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §16, which
classify the shared semiconductor-capex mechanism; and
`intelligence/companies/TSM.yaml`/`TSM.md`'s own capital-intensity and
equipment-supply-risk disclosures. The advisory classification in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§4.2 first classified this evidence against REL-0001's taxonomy (as
`capital_spending_dependency`, `inferred`) without itself authorizing a
record.

**This relationship is disclosed from KLAC's side only, and KLAC's own
TSM-specific figure is the weakest-evidenced of the three pairs in this
batch.** KLAC's own record states its TSMC-specific concentration figure
(~23% of FY2023 revenue) is "secondary, single data point, not tracked
across other years in this research pass" — a single, lower-confidence data
point, unlike ASML's own more current and more emphasized ~24%-of-net-sales
figure (recorded in `ASML_TSM.yaml`/`.md`, this same batch). This session
directly grepped `intelligence/companies/TSM.yaml` and
`intelligence/companies/TSM.md` for "KLAC" and "KLA" and found zero
matches — TSM's own record does not independently name KLAC as an equipment
supplier anywhere.

Neither `intelligence/companies/KLAC.yaml`/`KLAC.md` nor
`intelligence/companies/TSM.yaml`/`TSM.md` was modified by this unit.

## The relationship

KLA Corporation (KLAC) supplies process-control and yield-management
equipment to semiconductor manufacturers. KLAC's own record discloses, in
its margin-relevance evidence section, that "foundry/logic customers
(TSMC, Intel, Samsung) reportedly represent roughly 65-75% of FY2025
revenue," with memory customers (SK Hynix, Micron) a separate roughly
15-25%, and — as a distinct, lower-confidence data point — that "TSMC
reportedly approximately 23% of FY2023 revenue." Both figures are
explicitly labeled secondary and unverified in KLAC's own record. This
repository's own cross-batch research (`BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`
§5, `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §16) independently
classifies the underlying mechanism as the same shared semiconductor-capex
("WFE") driver ASML's and AMAT's and LRCX's records also disclose. TSM's
own record independently corroborates the scale of this capex cycle from
its own side (Q2 2026 capex ~39% of quarterly revenue, FY2026 guidance
$60-64 billion; "raw-material and equipment-supply constraints" disclosed
generically) without naming KLAC specifically.

Classified under REL-0001 §C's `capital_spending_dependency` primitive:
**KLAC (subject) depends on TSM (object)** — KLAC's revenue is materially
dependent on TSM's (and the wider foundry/IDM class's) capital-expenditure
cycle for process-control equipment purchases. Directional per REL-0001
§D — `capital_spending_dependency` is directional-by-construction, and this
record declares `symmetric: false` accordingly. No reverse-direction claim
is made.

## Why this pair, why this batch

Per the inventory audit's §4.2 classification, KLAC→TSM was identified as
existing, already-classified evidence meeting REL-0001's evidentiary bar at
an `inferred` classification — the same batch-level mechanism ASML→TSM
rests on, but at a materially weaker company-specific evidentiary tier (a
single FY2023 data point versus ASML's more current, more emphasized
figure). This pair, together with ASML→TSM (same mechanism) and NVDA→TSM
(manufacturing_dependency), was identified as the next evidence-ready
content unit following `REL-0002` (`CEG_MSFT`) and `REL-0003` (eight
further pairs).

## What this record does and does not establish

**Established, per the evidence above:** KLAC's own disclosed combined
foundry/logic customer-concentration figure (65-75% of FY2025 revenue,
spanning TSMC/Intel/Samsung) and its separate, lower-confidence TSMC-
specific FY2023 figure (~23%); this repository's own independently-
corroborated structural finding (Batch 1, Batch 3 §16) that KLAC's revenue
is exposed to the same foundry-capex cycle TSM's own capital-expenditure
disclosures independently corroborate the scale of.

**Not established by this record:** independent confirmation of the ~23%
FY2023 figure in any subsequent fiscal year, or against KLAC's own primary
filing; any confirmation from TSM's own filings naming KLAC as an equipment
supplier; how KLAC's TSM-specific exposure compares in magnitude to its
Intel/Samsung exposure within the combined 65-75% figure (not broken out by
name in the current evidence base); any measured historical price
correlation between KLAC and TSM (REL-0001 §G explicitly separates
structural evidence of this kind from measured price correlation — none was
computed, cited, or implied here); and any conclusion about duplicate
economic exposure, correlated loss, or missing exposure (REL-0001 §C
excludes these as primitive record types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — KLAC's capital-spending dependence on
  TSM sits alongside ASML's own capital-spending dependence on the same
  TSM-anchored foundry-capex class (recorded in this same batch) and
  NVDA's manufacturing dependence on TSM directly — a fact relevant to the
  portfolio's existing `semis` cluster-cap doctrine (`targets.yaml`), which
  already identifies "the equipment (KLAC/LRCX/AMAT)... names" as behaving
  distinctly within the wider cluster.
- **`thesis_monitoring`** — KLAC's own record already flags both underlying
  figures as unverified/single-data-point; a future thesis-monitoring pass
  over KLAC should track whether a more current, better-sourced TSM-specific
  concentration figure becomes available, and any disclosed change in TSM's
  own capex guidance.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, tier change, target change, or
trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to KLAC's
or TSM's tier, target, role, cluster, cap, or holding; any trade or order;
any margin use or margin-policy recommendation; any ranking, score, or
composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
