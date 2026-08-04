# ASML ↔ TSM — capital_spending_dependency (ASML depends on TSM)

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
preflight: `intelligence/companies/ASML.yaml`'s own disclosed customer-
concentration risk entry; `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`
§5 and `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §16,
which classify the shared semiconductor-capex mechanism; and
`intelligence/companies/TSM.yaml`/`TSM.md`'s own capital-intensity and
equipment-supply-risk disclosures. The advisory classification in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§4.2 first classified this evidence against REL-0001's taxonomy (as
`capital_spending_dependency`, `inferred`) without itself authorizing a
record.

**This relationship is disclosed from ASML's side only, and ASML's own
figure is itself secondary-sourced.** ASML's own Company Intelligence
record states its TSMC-concentration figure (~24% of net sales, top two
~38%, top ten >80%) is drawn from "secondary sources (not independently
traced to ASML's own 20-F disclosure this pass)" and "requires primary-
source (20-F) verification before being treated as a confirmed fact rather
than a well-corroborated estimate." This session directly grepped
`intelligence/companies/TSM.yaml` and `intelligence/companies/TSM.md` for
"ASML" and found zero matches — TSM's own record does not independently
name ASML as an equipment supplier anywhere; its "raw-material and
equipment-supply constraints" risk-factor category is disclosed generically,
without naming any specific vendor.

Neither `intelligence/companies/ASML.yaml`/`ASML.md` nor
`intelligence/companies/TSM.yaml`/`TSM.md` was modified by this unit.

## The relationship

ASML is the sole commercial supplier of EUV lithography systems worldwide
and holds a ~94% share of all lithography equipment (DUV+EUV combined).
ASML's own record discloses "extreme customer and geographic concentration"
— TSMC named specifically at roughly 24% of net sales, the largest single
concentration figure disclosed in that record, with the top two customers
combined at roughly 38% and the top ten at over 80%. This repository's own
cross-batch research (`BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §5,
`BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §16) independently
classifies the underlying mechanism: ASML sells capital equipment to
foundries and IDMs whose own capacity expansion is driven substantially by
AI-infrastructure demand, and every incremental unit of fabless-designer
demand (AVGO/AMD/MRVL, per Batch 3) that TSM fulfills by adding capacity is
mechanically incremental demand for the categories of equipment ASML sells
to TSM. TSM's own record independently corroborates the scale of this capex
cycle from its own side: Q2 2026 capital expenditure represented
approximately 39% of that quarter's revenue, amid full-year 2026 guidance
of $60-64 billion, with "raw-material and equipment-supply constraints"
disclosed as its own risk-factor category (generic, not ASML-specific).

Classified under REL-0001 §C's `capital_spending_dependency` primitive:
**ASML (subject) depends on TSM (object)** — ASML's revenue is materially
dependent on TSM's (and the wider foundry/IDM class's) capital-expenditure
cycle for lithography equipment purchases. Directional per REL-0001 §D —
`capital_spending_dependency` is directional-by-construction, and this
record declares `symmetric: false` accordingly. No reverse-direction claim
is made: TSM's own disclosed capital-intensity and equipment-supply risk
are cited only as corroborating context for the shared capex mechanism, not
as a claim that TSM itself depends on ASML.

## Why this pair, why this batch

Per the inventory audit's §4.2 classification, ASML→TSM was identified as
existing, already-classified evidence meeting REL-0001's evidentiary bar at
an `inferred` classification. This pair, together with KLAC→TSM (same
mechanism) and NVDA→TSM (manufacturing_dependency), was identified as the
next evidence-ready content unit following `REL-0002` (`CEG_MSFT`) and
`REL-0003` (eight further pairs) — the semiconductor capital-equipment and
foundry-dependency relationships §4.1/§4.2 of the inventory audit already
classified but no prior batch had yet implemented.

## What this record does and does not establish

**Established, per the evidence above:** ASML's own disclosed customer-
concentration figure naming TSMC specifically at ~24% of net sales; this
repository's own independently-corroborated structural finding (Batch 1,
Batch 3 §16) that ASML's revenue is exposed to the same foundry-capex cycle
TSM's own capital-expenditure disclosures independently corroborate the
scale of.

**Not established by this record:** independent confirmation of the ~24%
figure against ASML's own 20-F (flagged as an open verification gap in
ASML's own record, not resolved here); any confirmation from TSM's own
filings naming ASML as an equipment supplier; whether ASML's TSMC
dependence has changed in magnitude since ASML's own 2026-07-25 evidence
date; any measured historical price correlation between ASML and TSM
(REL-0001 §G explicitly separates structural evidence of this kind from
measured price correlation — none was computed, cited, or implied here);
and any conclusion about duplicate economic exposure, correlated loss, or
missing exposure (REL-0001 §C excludes these as primitive record types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — ASML's capital-spending dependence on
  TSM sits alongside KLAC's own capital-spending dependence on the same
  TSM-anchored foundry-capex class (recorded in this same batch) and
  NVDA's manufacturing dependence on TSM directly — three separate
  `semis`-cluster names sharing exposure to the same named counterparty's
  capex/manufacturing decisions, a fact relevant to the portfolio's
  existing `semis` cluster-cap doctrine (`targets.yaml`), which already
  identifies "the equipment (KLAC/LRCX/AMAT)... names" as behaving
  distinctly within the wider cluster.
- **`thesis_monitoring`** — ASML's own record already flags its TSMC-
  concentration figure as unverified against primary sources; a future
  thesis-monitoring pass over ASML should track both that verification and
  any disclosed change in TSM's own capex guidance, which this record's
  evidence identifies as a direct driver of ASML's order book.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, tier change, target change, or
trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to ASML's
or TSM's tier, target, role, cluster, cap, or holding; any trade or order;
any margin use or margin-policy recommendation; any ranking, score, or
composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
