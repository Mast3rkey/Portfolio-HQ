# AVGO ↔ TSM — manufacturing_dependency (AVGO depends on TSM)

Last updated: 2026-08-04 — record created through AI-assisted research and
drafting under `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
(frozen schema, taxonomy, evidence standard) and
`governance/decisions/REL-0005-ws0005-milestone4-third-relationship-content-batch-semis-tsm.md`
(this batch's own authorization). Fourth pair in the third WS-0005
Milestone 4 relationship-content batch, following `REL-0002` (`CEG_MSFT`)
and `REL-0003` (eight further pairs). Added on a separate, explicit
principal authorization alongside the batch's original three pairs
(NVDA_TSM, ASML_TSM, KLAC_TSM), independently verified against existing
repository evidence before being accepted — not inferred merely from
adjacency to the other three.

## Source-access disclosure

This record performs **zero new external research**. Every fact below is
drawn from evidence already present in the repository at this unit's own
preflight: `intelligence/companies/AVGO.yaml`'s own dedicated risk entry,
"Foundry and advanced-packaging dependency" (and `AVGO.md`'s matching
section); `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`
§5 and §16, which independently reach the same structural conclusion; and
`intelligence/companies/TSM.yaml`/`TSM.md`'s own customer-concentration
disclosure. `governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§4.1 first classified this evidence against REL-0001's taxonomy (as
`manufacturing_dependency`, `inferred`) without itself authorizing a
record — the audit's own row for this pair states: "AVGO → TSM | Same
structural inference as above, extended explicitly to AVGO by Batch3 §5...
No AVGO-specific named-percentage figure found."

**This relationship is disclosed from AVGO's side only.** This session
directly grepped `intelligence/companies/TSM.yaml` and
`intelligence/companies/TSM.md` for "AVGO"/"Broadcom" and found zero
matches — TSM's own Form 20-F customer-concentration disclosure (largest
customer 19% of 2025 revenue, second-largest 17%, top ten 78%) explicitly
does not name any customer, including AVGO. AVGO's own record additionally
discloses that its underlying research for this pass was WebSearch-sourced
throughout — direct WebFetch attempts against SEC EDGAR,
investors.broadcom.com, and a stocktitan.net secondary-filing-summary page
all returned HTTP 403, a tool/proxy-level block independently re-verified
by that record's own research session (not merely assumed from an earlier
batch's experience).

Neither `intelligence/companies/AVGO.yaml`/`AVGO.md` nor
`intelligence/companies/TSM.yaml`/`TSM.md` was modified by this unit.

## The relationship

Broadcom (AVGO) is described in its own Company Intelligence record as a
"fabless/hybrid" semiconductor company — its merchant chips and custom AI
silicon (XPU) products rely on external foundry and advanced-packaging
capacity for physical production. AVGO's own record carries a risk entry
dedicated specifically to this dependency: "Broadcom's semiconductor
products (both merchant chips and custom AI silicon) rely on external
foundry and advanced-packaging capacity -- industry-wide reporting places
TSMC as the dominant advanced-node/advanced-packaging supplier to the
AI-accelerator industry broadly, and this record's own TSM Company
Intelligence record... independently documents TSMC management's statement
that advanced-packaging capacity is currently tight enough to constrain
customer growth industry-wide." This repository's own
`BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §5 independently reaches
the same conclusion for AVGO specifically, alongside AMD and MRVL, while
explicitly disclosing that no company-specific, named-percentage TSMC
dependence figure was located for any of the three.

Classified under REL-0001 §C's `manufacturing_dependency` primitive:
**AVGO (subject) depends on TSM (object)** for physical production of a
material product line (its merchant-chip and custom-AI-silicon lineup).
Directional per REL-0001 §D — `manufacturing_dependency` is directional-
by-construction, and this record declares `symmetric: false` accordingly.
No claim is made in the reverse direction (TSM depending on AVGO) — TSM's
own record discloses 534 customers in 2025 across a broad product mix, of
which AVGO (if it is among the named concentration figures at all, which is
not confirmed) would be only one.

## Why this pair, why this batch

Per the inventory audit's §4.1 classification, AVGO→TSM was identified as
existing, already-classified evidence at the same `inferred` tier as
NVDA→TSM — a dedicated, company-specific risk entry in AVGO's own record
naming TSMC directly, which is if anything a more directly on-point
disclosure than NVDA's own more generic "foundry partners and contract
manufacturers" language. This pair was not part of the batch's original
three-pair scope (NVDA_TSM, ASML_TSM, KLAC_TSM) — it was added on a
separate, explicit principal authorization, conditioned on this session
independently re-verifying that existing accepted repository evidence
supports it under the same REL-0001 §E standard the other three pairs meet,
which it does.

## What this record does and does not establish

**Established, per the evidence above:** AVGO's own disclosed
fabless/hybrid status and its own dedicated, TSMC-naming foundry-dependency
risk-factor language; this repository's own independently-corroborated
structural finding (Batch 3 §5) that TSMC is the dominant advanced-node/
advanced-packaging manufacturing partner for AVGO's class of product.

**Not established by this record:** any company-specific, named-percentage
figure quantifying what share of AVGO's production TSM specifically
manufactures; any confirmation from TSM's own filings that AVGO is among
its named or unnamed concentrated customers; how AVGO's "hybrid" (not
purely fabless) manufacturing model divides between TSM and any other
foundry — not addressed in the current evidence base, and this record does
not claim exclusivity; any measured historical price correlation between
AVGO and TSM (REL-0001 §G explicitly separates structural evidence of this
kind from measured price correlation — none was computed, cited, or implied
here); and any conclusion about duplicate economic exposure, correlated
loss, or missing exposure (REL-0001 §C excludes these as primitive record
types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — AVGO's manufacturing dependence on
  TSM sits alongside NVDA's own manufacturing dependence on TSM, and
  ASML's/KLAC's capital-spending dependence on the same TSM-anchored
  foundry-capex class (all recorded in this same batch) — a fact relevant
  to the portfolio's `semis` cluster-cap doctrine (`targets.yaml`) and the
  previously-declined T1 AI-infrastructure cluster-cap scan (`CLAUDE.md`
  Decisions Log), both of which flag shared foundry-concentration exposure
  without having previously mapped it at this pairwise level.
- **`stress_testing`** — a disruption at TSM is exactly the kind of
  disclosed, name-specific single-point-of-failure scenario a future
  portfolio-level stress scenario could reference for AVGO specifically,
  distinct from any generic semiconductor-sector stress assumption.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, stress-test execution, tier
change, target change, or trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to AVGO's
or TSM's tier, target, role, cluster, cap, or holding; any trade or order;
any margin use or margin-policy recommendation; any ranking, score, or
composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
