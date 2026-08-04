# NVDA ↔ TSM — manufacturing_dependency (NVDA depends on TSM)

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
preflight: `intelligence/companies/NVDA.yaml`'s own risk-factor disclosure
(sourced to NVIDIA's Q1 FY2027 Form 10-Q, independently inspected during a
prior PR review); `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`
§5 and §16, which classify this exact structural inference; and
`intelligence/companies/TSM.yaml`/`TSM.md`'s own customer-concentration
disclosure. The advisory recommendation in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§4.1 first classified this evidence against REL-0001's taxonomy (as
`manufacturing_dependency`, `inferred`) without itself authorizing a record.

**This relationship is disclosed from neither company's own primary-source
naming of the other.** This session directly grepped
`intelligence/companies/TSM.yaml` and `intelligence/companies/TSM.md` for
"NVDA"/"NVIDIA" and found zero matches — TSM's own Form 20-F customer-
concentration disclosure (largest customer 19% of 2025 revenue,
second-largest 17%, top ten 78%) explicitly does not name any customer,
including NVDA. Conversely, `intelligence/companies/NVDA.yaml`'s own Q1
FY2027 Form 10-Q risk-factor language discusses "foundry partners and
contract manufacturers" generically and does not name TSM specifically —
standard supplier-disclosure practice on both sides, not evidence against
the relationship, but meaning neither company's own primary source
bilaterally confirms this specific pairing by name. The relationship rests
instead on this repository's own prior structural research (Batch 3's
independent cross-corroboration of public, industry-wide reporting placing
TSMC as the dominant advanced-node/advanced-packaging foundry for
fabless AI-accelerator designers), not on either company's own filing.

Neither `intelligence/companies/NVDA.yaml`/`NVDA.md` nor
`intelligence/companies/TSM.yaml`/`TSM.md` was modified by this unit.

## The relationship

NVIDIA (NVDA) is a fabless semiconductor company — it designs GPUs and
AI-accelerator products but does not own or operate leading-edge
semiconductor fabrication capacity. NVDA's own Company Intelligence record
discloses, per its Q1 FY2027 Form 10-Q, that "competitors and customers may
constrain NVIDIA's ability to procure foundry capacity and scarce inputs,"
that NVIDIA "has experienced manufacturing lead times exceeding 12 months,"
and that "foundry partners and contract manufacturers may be unable to
provide sufficient capacity" — without naming a specific foundry. This
repository's own `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`
independently found, through cross-corroborated public/industry-wide
reporting (not a company-specific disclosure from either NVDA or TSM), that
TSMC is the dominant advanced-node/advanced-packaging manufacturing partner
for this class of fabless AI-accelerator designer, while explicitly
disclosing that "none of the four companies' own records located a
company-specific, named-percentage TSMC dependence disclosure this session
opened" — a limitation that applies equally to NVDA, which Batch 3 itself
did not cover as a company record but which this record's own preflight
confirmed by directly re-inspecting NVDA.yaml.

Classified under REL-0001 §C's `manufacturing_dependency` primitive:
**NVDA (subject) depends on TSM (object)** for physical production of a
material product line (its GPU/accelerator lineup). Directional per
REL-0001 §D — `manufacturing_dependency` is directional-by-construction,
and this record declares `symmetric: false` accordingly. No claim is made
in the reverse direction (TSM depending on NVDA) — TSM's own record
discloses 534 customers in 2025 across a broad product mix, of which NVDA
(if it is among the named concentration figures at all, which is not
confirmed) would be only one.

## Why this pair, why this batch

Per the inventory audit's §4.1 classification, NVDA→TSM was identified as
existing, already-classified evidence meeting REL-0001's evidentiary bar at
an `inferred` classification — a structural inference from NVDA's disclosed
fabless status and industry-wide foundry concentration, not a
company-specific dollar or percentage figure from either side. This pair,
together with ASML→TSM and KLAC→TSM (recorded in this same batch), was
identified as the next evidence-ready content unit following `REL-0002`
(`CEG_MSFT`) and `REL-0003` (eight further pairs) — the semiconductor
capital-equipment and foundry-dependency relationships §4.1/§4.2 of the
inventory audit already classified but no prior batch had yet implemented.

## What this record does and does not establish

**Established, per the evidence above:** NVDA's own disclosed fabless
status and generic (not TSM-specific) foundry-capacity risk-factor
language; this repository's own independently-corroborated structural
finding (Batch 3) that TSMC is the dominant advanced-node/advanced-
packaging manufacturing partner for NVDA's class of product.

**Not established by this record:** any company-specific, named-percentage
figure quantifying what share of NVDA's production TSM specifically
manufactures; any confirmation from TSM's own filings that NVDA is among
its named or unnamed concentrated customers; whether NVDA uses any other
foundry (e.g., Samsung) for any portion of its production — not addressed
in the current evidence base, and this record does not claim exclusivity;
any measured historical price correlation between NVDA and TSM (REL-0001 §G
explicitly separates structural evidence of this kind from measured price
correlation — none was computed, cited, or implied here); and any
conclusion about duplicate economic exposure, correlated loss, or missing
exposure (REL-0001 §C excludes these as primitive record types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — NVDA's manufacturing dependence on
  TSM sits alongside ASML's and KLAC's own capital-spending dependence on
  the same TSM-anchored foundry-capex class (recorded in this same batch),
  and alongside the previously-declined T1 AI-infrastructure cluster-cap
  scan (`CLAUDE.md` Decisions Log) — a fact relevant to understanding
  whether the portfolio's `semis` cluster shares a common single point of
  foundry-concentration risk, not merely a correlation-scan result.
- **`stress_testing`** — a disruption at TSM (a Taiwan earthquake,
  cross-strait geopolitical event, or a major fab outage) is exactly the
  kind of disclosed, name-specific single-point-of-failure scenario a
  future portfolio-level stress scenario could reference for NVDA
  specifically, distinct from any generic semiconductor-sector stress
  assumption.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, stress-test execution, tier
change, target change, or trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to NVDA's
or TSM's tier, target, role, cluster, cap, or holding; any trade or order;
any margin use or margin-policy recommendation; any ranking, score, or
composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
