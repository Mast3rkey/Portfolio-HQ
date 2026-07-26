# WS-0005 Milestone 3, Batch 4 — Power Infrastructure Comparison

**ETN, VRT, PWR — with GEV as existing comparison context only.**
Authorized by
`governance/decisions/PI-0026-ws0005-milestone3-batch4-power-infrastructure.md`
§C (comparison requirements) and §I (completion criteria requiring this
evidence be retained). Created 2026-07-26, alongside the three
companies' own Company Intelligence records
(`intelligence/companies/{ETN,VRT,PWR}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or
Theme Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s
schema (it introduces no new schema and is not scanned by
`intelligence_validator.py` or any other validator), and not an
authoritative record any allocator or policy decision may read. It sits
at `intelligence/` root rather than inside `companies/` (reserved for
`<TICKER>.yaml`/`.md` pairs) or `governance/audits/` (reserved for
independently-authored audits per `OPS-0004` — this document is
authored by the same implementation session as the three company
records, not an independent review of them), matching
`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`,
`intelligence/BATCH2_MEMORY_COMPARISON.md`, and
`intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`'s own
placement and scope. **It does not rank the four companies (ETN, VRT,
PWR, and existing-context GEV), does not recommend a tier/target/
cluster change, a buy/trim/exit, a margin action, or a next-best-
alternative ranking, and does not create a composite score of any
kind** — per `PI-0026` §C's explicit instruction and the Constitution's
standing prohibition on predictive research or opportunity maps.

**GEV boundary, restated explicitly.** GEV is the `power_infra`
cluster's fourth and only-previously-covered member (`PI-0007`,
refreshed under `PI-0019`/`PI-0020`, `last_reviewed: 2026-07-22`,
`conviction.rating: Medium`). This document uses GEV's existing,
unmodified record purely as comparison context, exactly as `PI-0025`'s
own Batch 3 comparison artifact referenced Batch 1's ASML/AMAT/KLAC/LRCX
as existing comparison context without re-authorizing or editing those
records. **`intelligence/companies/GEV.yaml` and `GEV.md` are not
edited, refreshed, or reassessed by this document or by this batch under
any circumstance.**

**Source-access disclosure (applies to this whole document):** every
fact below is inherited from the three companies' own Company
Intelligence records (ETN, VRT, PWR) or from GEV's own existing record,
each of which discloses that WebFetch was blocked throughout this
session's research pass — a tool/proxy-level HTTP 403 on every URL
attempted, including SEC EDGAR, each company's own investor-relations
domain, and a non-target control domain (`example.com`) — confirmed
independently for ETN, VRT, and PWR's own research passes (see each
company's own Source-access disclosure). **No primary document was
independently rendered and inspected by this session at any point.**
Each underlying record distinguishes fact, inference, uncertainty, and
judgment, and discloses actual access status per claim; this document
inherits those distinctions rather than re-stating every one in full.
This document adds no new primary research of its own — it only
compares and cross-references what the three (plus GEV's existing)
company records already established. Consistent with `OPS-0006` §4's
distinction between structural/economic overlap and measured historical
price correlation, **no price-correlation coefficient was computed for
this document** — every correlation-relevant statement below is about
shared economic drivers, not measured historical return correlation.

## 1. Four distinct functions in the power/electrification value chain

Unlike Batch 2 (MU, SKHY, direct competitors selling substantially the
same product categories) and more like Batch 1 (ASML, AMAT, KLAC, LRCX,
each performing a distinct step in a shared process) and Batch 3 (AVGO,
AMD, MRVL, INTC, four different business-model positions sharing one
capex cycle), **this batch's three companies — plus GEV as existing
context — occupy four genuinely different functional positions within
one value chain, all bound together by the same governing cluster
rationale (`targets.yaml`: "real shared driver is AI data-center power/
electricity demand buildout"):**

| Company | Function in the value chain | Business model |
|---|---|---|
| GEV (existing context) | Power generation and grid equipment — gas turbines, electrification/grid products | Equipment manufacturer, broad power-generation scope beyond data centers |
| ETN | Electrical equipment across the full power-distribution chain (circuit protection, switchgear, power distribution/quality, UPS) plus a distinct Aerospace business | Equipment manufacturer, diversified across data center/utility/industrial/commercial/residential/aerospace end markets |
| VRT | Thermal management (liquid cooling) and power-management equipment **specifically for data centers** | Equipment manufacturer, narrowly data-center-focused — the batch's purest data-center pure-play |
| PWR | Engineering, procurement, construction (EPC), and maintenance services for electric power, utility, and communications infrastructure | Labor-intensive contract-services provider — **does not manufacture equipment at all** |

**This is the batch's single clearest structural finding**: three of
the four (GEV, ETN, VRT) are equipment manufacturers of one kind or
another, while PWR is a fundamentally different economic animal — a
services business that often *installs and maintains* the kind of
equipment GEV, ETN, and (to a lesser, more indirect extent) VRT
manufacture. PWR's own AEP partnership (a 765 kV transmission EPC and
domestic transformer/breaker manufacturing-capacity agreement) is, in
fact, adjacent to exactly the kind of equipment ETN and GEV sell — PWR
builds the infrastructure that carries and delivers the power ETN's
switchgear/distribution equipment and GEV's turbines generate, while
VRT's equipment sits inside the data center consuming that delivered
power. **Read together, GEV (generation) → ETN (distribution/
switching) → PWR (transmission/grid construction) → VRT (in-building
thermal/power management) trace a genuinely sequential path from power
generation to the chip actually being cooled** — a materially different
comparison shape than any prior batch, where the shared driver
(AI-data-center power/electricity demand) manifests as a **supply
chain**, not merely a correlated basket of similarly-exposed equipment
makers.

## 2. Direct versus indirect data-center exposure

| Company | Data-center exposure | Directness |
|---|---|---|
| VRT | Data center is essentially the whole business (cooling/power management sold directly into data-center builds); AI/hyperscaler-driven liquid cooling is the current primary growth narrative | **Most direct** — data center is not a segment, it is nearly the entire company |
| GEV (existing context) | Electrification segment discloses data-center-specific order figures (>$5B combined H1 2026 orders per GEV's own record); Power segment's gas-turbine demand is driven by broader grid/generation needs, only partly data-center-specific | Direct in Electrification, more indirect/broader in Power |
| ETN | Electrical segment discloses data center as its fastest-growing named vertical (~240% YoY order growth, Q1 2026), but non-data-center end markets (utility, industrial, institutional) are argued by at least one secondary source to still comprise the majority of Electrical backlog; Aerospace segment has no data-center exposure at all | Partial and diluted — real, but a minority of the whole company by at least one independent read |
| PWR | Data-center exposure is entirely indirect, via utility/grid-transmission work that serves data-center-driven electricity demand (the AEP 765 kV partnership is explicitly framed around "the rapidly growing data center market," but the work itself is grid infrastructure, not anything installed inside a data center) | **Most indirect** — PWR never sells anything to, or installs anything inside, a data center itself; it builds the grid that feeds it |

**No company in this batch discloses a clean percentage of revenue
attributable to data centers specifically** — VRT's concentration is
qualitative/structural (the business is built around data centers) but
not quantified as a percentage; ETN discloses order-growth rates, not
revenue share; PWR's exposure is a named contractual relationship
(AEP) without a disclosed dollar allocation to data-center-specific
work within that broader transmission agreement.

## 3. Utility and grid-capital-spending exposure

PWR is the most directly levered to utility capital-spending cycles by
business model — its entire revenue is contract-services work for
utilities, telecom carriers, and pipeline operators, evidenced
concretely by the AEP $72B 2026-2030 capital-plan partnership. GEV's
Power segment (gas turbines, grid equipment) is also directly levered
to utility/grid capex, evidenced by its own gas-equipment
backlog-and-slot-reservation growth (100 GW to 116 GW in one quarter,
per GEV's existing record). ETN's Electrical Global/Americas segments
sell into utility spending as one of several end markets, alongside
industrial, commercial, and residential. VRT's exposure to utility
capex specifically (as opposed to hyperscaler/enterprise data-center
capex) is the weakest of the four — its business is data-center-facing,
not utility-grid-facing, even though the electricity ultimately
delivered to those data centers flows through utility infrastructure.

## 4. Customer and supplier overlap

**Overlap is more indirect than direct across this batch.** ETN and VRT
are both named, in their own records, as competitors to *each other*
in some overlapping categories (electrical/power-management equipment
for data centers) even while occupying different primary niches (ETN
broader/diversified, VRT data-center-pure). Neither ETN's nor VRT's own
record discloses a shared named customer with PWR, and PWR's own record
discloses no shared named customer with GEV, ETN, or VRT — its
customers are utilities (AEP being the only one named with a specific,
dated relationship) and telecom carriers, a different customer class
than the hyperscalers and colocation operators VRT's record describes.
**A plausible, un-evidenced structural overlap** (judgment, not a
sourced claim): the same hyperscalers/data-center developers that are
VRT's and GEV's Electrification-segment customers are, at the far end
of the grid, the entities whose electricity demand growth is driving
utilities like AEP to spend the capital that funds PWR's transmission
contracts — an indirect demand-chain link, not a disclosed shared
customer relationship. No supplier overlap was found or asserted across
any pair in this batch; PWR does not manufacture equipment and so has
no equipment-supplier relationship with GEV/ETN/VRT to begin with
(though it may install their products on job sites, which none of the
four companies' own records confirms directly).

## 5. Backlog composition and execution risk

| Company | Backlog type | Recent figures | Execution-risk character |
|---|---|---|---|
| GEV (existing context) | Equipment order backlog | $176B total (Q2 2026, per GEV's own record) | Long-cycle, fixed/competitively-bid equipment execution risk |
| ETN | Equipment order backlog | Electrical backlog +48% YoY (Q1 2026 point; ~29% YoY full-year-2025 average) | Long lead-time equipment (transformers ~4 years, switchgear 50-80 weeks) — backlog quality tied to supply-chain/capacity-build execution |
| VRT | Equipment order backlog | $15B (Q4 2025) vs. $12.45B (Q1 2026) — **an unreconciled sequential decline this batch's own ETN.md/VRT.md records disclose and do not resolve** | Equipment backlog, but the batch's only company with a disclosed, unresolved backlog discrepancy in the same fiscal year |
| PWR | Mixed: firm fixed-price RPO **plus** estimated MSA-renewal orders (an explicitly disclosed methodology distinct from the other three) | Total backlog $48.47B (Q1 2026, record), RPO $26.24B (of which $15.9B convertible within 12 months) | **Project/contract-services backlog**, not equipment-order backlog — cancellation, rescheduling, and fixed-price cost-overrun risk apply in a way that does not apply to an equipment manufacturer's booked-order backlog |

**This is a genuinely different backlog character for PWR than for the
other three.** An equipment manufacturer's backlog (GEV, ETN, VRT) is a
booked-order count awaiting manufacture and shipment; PWR's backlog
mixes firm contracted revenue with company-estimated recurring-MSA
volume, and its execution risk runs through labor availability, fixed-
price cost overruns, and project scheduling rather than component
supply chains and capacity-build timelines. **VRT's unreconciled
backlog discrepancy is this batch's most specific, disclosed evidence
gap** — it is not analogous to PWR's estimation-methodology caveat;
VRT's is an unexplained sequential decline in a metric defined the same
way both quarters, per VRT's own record.

## 6. Recurring versus project-based economics

PWR discloses the clearest recurring-revenue framing of the batch:
management describes approximately 80% of the business as base-level,
MSA-driven recurring services, with large discrete projects layered on
top. VRT's record cites a single, unverified secondary estimate of an
approximately 81%/19% product-to-service revenue split — coincidentally
a similar-looking number to PWR's 80% recurring-services estimate, but
describing a completely different thing (VRT's is a product-vs-service
revenue mix within an equipment-manufacturing business; PWR's is a
recurring-vs-project characterization of an entire services business)
and should not be conflated. ETN's record contains no comparable
recurring/project breakdown — its revenue is overwhelmingly product
(equipment) sales, with backlog serving as the closest proxy for future
revenue visibility. GEV's existing record similarly frames its business
around backlog and order flow rather than a recurring/project split.

## 7. Capital intensity and working-capital behavior

ETN and VRT, as equipment manufacturers, carry manufacturing capital
intensity (ETN's ~$900M FY2025 capex explicitly earmarked for
data-center-driven capacity expansion; VRT's Tognana, Italy chiller-
capacity expansion) and inventory/backlog-driven working capital. PWR,
as a contract-services business, carries a structurally different
working-capital profile centered on **unbilled receivables and contract
assets** tied to percentage-of-completion accounting — PWR's own record
discloses unbilled receivables growing from $859.9M (2024-12-31) to
$1.19B (2025-09-30), a working-capital use of cash embedded within an
otherwise-strong free-cash-flow year. This is a materially different
capital-intensity and cash-conversion pattern than ETN's or VRT's
manufacturing-driven working capital, and is the clearest financial-
statement-level confirmation that PWR's economics genuinely differ from
the other two, not merely its business description.

## 8. Acquisitions and integration risk

All four companies in this comparison (including GEV as existing
context) have made a large, recent, thesis-concentrated acquisition:

- **GEV** (existing context): Prolec GE, closed 2026-02-02, $5.275B,
  funded with an equal mix of cash and debt, Electrification-segment
  electrical-equipment manufacturer.
- **ETN**: Boyd Thermal, agreed November 2025, approximately $9.5B
  (~22.5x Boyd Thermal's estimated 2026 adjusted EBITDA) — roughly 35%
  of ETN's own FY2025 total revenue in deal value, concentrated entirely
  in liquid cooling for hyperscale/AI data centers. ETN's own record
  flags this as its largest deal since Cooper Industries (2012).
  Close-date disclosure is inconsistent across secondary sources (one
  states 2026-03-12, another "expected Q2 2026") and is not resolved
  in ETN's own record.
- **VRT**: no single acquisition of comparable scale was found; VRT's
  M&A activity (E+I Engineering 2021, CoolTera 2023, Great Lakes Data
  Racks & Cabinets ~2025) is smaller and more capability-additive in
  character than a single company-transforming deal.
- **PWR**: Cupertino Electric, Inc. (CEI), closed 2024-07-17,
  approximately $1.54B upfront plus a potential $200M earnout — smaller
  in absolute dollars than ETN's Boyd Thermal deal and PWR's own scale,
  and one of many acquisitions in a documented serial-acquirer pattern
  (18 acquisitions per one aggregator count) rather than a single
  outsized, thesis-concentrated bet.

**ETN's Boyd Thermal deal stands out within this batch as the single
largest, most thesis-concentrated acquisition-integration risk** — both
in absolute size relative to the acquirer's own revenue and in its
singular concentration on one growth thesis (AI-data-center liquid
cooling), a materially different risk profile than PWR's pattern of
many smaller, capability-additive acquisitions or VRT's more modest
M&A activity.

## 9. Common macro and spending-cycle dependencies

All four share genuine, disclosed exposure to the AI-data-center-capex
buildout (the cluster's own governing rationale), but the **transmission
mechanism differs by company**: VRT is exposed directly to hyperscaler
capex decisions; GEV's Power segment and PWR are exposed to the
resulting utility/grid capital-spending response to that demand (a
one-step-removed transmission mechanism); ETN sits closer to VRT for
its Electrical segment's data-center order flow but is diluted by its
non-data-center end markets and separate Aerospace business. All four
are also exposed, to varying degrees, to interest-rate sensitivity via
capex-cycle financing costs (utility rate-base capex and hyperscaler
data-center capex are both partly debt-financed), though none of the
four companies' own records discloses a company-specific quantified
rate-sensitivity figure.

## 10. Raw-material, labor, regulatory, and interest-rate sensitivities

| Company | Primary input/execution risk | Regulatory/interest-rate sensitivity |
|---|---|---|
| GEV (existing context) | Global supply-chain dependency for castings, forgings, specialized components (per GEV's own record) | Tariff exposure ($100-200M net 2026 estimate, per GEV's own record) |
| ETN | Component/casting supply risk (general "input cost" commentary, not itemized); certification-driven lead times (transformers ~4yr) | Tariff exposure acknowledged, called "immaterial" to 2026 guidance by management; non-residential-construction/utility-capex rate sensitivity |
| VRT | Copper/aluminum commodity exposure (general market context, not company-quantified); component supply for liquid-cooling manufacturing scale-up | General 2026 copper-market tariff/deficit context (not VRT-specific); hyperscaler-capex-cycle sensitivity |
| PWR | **Labor** is the primary input, not materials — craft-labor availability/safety, not commodity/component supply | Utility rate-case and capital-plan approval cycles (indirect, via customers like AEP); renewable ITC/PTC policy exposure for solar/wind-adjacent work |

**PWR is again the outlier**: its primary execution risk is people
(craft labor, safety), not materials or components — a structurally
different risk category than the other three's supply-chain/component
exposure. PWR also carries a distinct regulatory exposure (renewable
tax-credit policy) that GEV, ETN, and VRT's records do not discuss with
comparable specificity, reflecting PWR's direct involvement in
renewable-energy-adjacent construction work.

## 11. Common correlated-loss mechanisms

The `power_infra` cluster's own governing rationale (`targets.yaml`:
"real shared driver is AI data-center power/electricity demand
buildout, not just market beta") is independently corroborated across
all three new records: multiple third-party sources (identified in
ETN.yaml, VRT.yaml, and PWR.yaml's own sources) group Eaton, Vertiv, and
Quanta together as complementary plays on the same AI-data-center
power-buildout demand driver — a real, named, cross-source-
corroborated shared driver, not this batch's own invention. **A
sustained reversal or pause in hyperscaler AI-capital-expenditure growth
is the single most common thesis-break condition across all four
companies' own individual records** (GEV's existing record, and this
batch's ETN/VRT/PWR records, each name a version of this same
condition independently). Beyond that shared macro driver, this batch
did not find evidence of a second, independent correlated-loss
mechanism binding all four together — e.g., no shared customer
concentration, no shared supplier, no shared financing counterparty was
identified across all four records.

## 12. Genuine diversification versus duplicated exposure

**This batch's clearest finding is that the four companies are
functionally complementary, not duplicative, along the value chain
described in §1** — GEV generates power, ETN distributes/switches it,
PWR builds and maintains the grid that carries it, and VRT manages it
(thermally and electrically) once it reaches the building housing the
compute. Holding all four is not the same as holding four versions of
the same equipment-manufacturer bet: PWR in particular is a genuinely
different economic animal (labor-intensive services vs. equipment
manufacturing) that would be lost entirely if the cluster consisted
only of GEV/ETN/VRT. Within the equipment-manufacturer subset, ETN and
VRT show the most business-model overlap (both are named as competitors
to each other in some product categories), while GEV's broader
power-generation scope and PWR's services-only model each add distinct
exposure the other three do not replicate. **This finding is about
structural/economic function, not measured price correlation** — no
correlation coefficient was computed for any pair in this batch,
consistent with `OPS-0006` §4's explicit distinction between the two
kinds of evidence.

## 13. Does `power_infra` describe one coherent risk cluster or several distinct economic functions? (advisory research finding only)

**This is an advisory research finding only, with no automatic effect
on the cluster or cap, per `PI-0026` §C's explicit instruction — any
actual change to the `power_infra` cluster or its cap requires its own
separate, later, explicit governance decision.**

The evidence assembled in this batch supports a nuanced answer, not a
clean yes-or-no:

**Evidence supporting one coherent cluster:** all four companies share
a genuine, specific, independently-corroborated demand driver (AI-
data-center power/electricity buildout), distinct from generic market
beta — the same standard the cluster's own governing comment applies,
and the same standard that led to the `power_infra` cap being
created (0.560 avg pairwise correlation among GEV/ETN/VRT/PWR, per
`targets.yaml`'s own history, a figure this batch did not re-derive or
re-measure). All four also share a common, disclosed thesis-break
condition (a hyperscaler AI-capex slowdown), and all four appear
together, by name, in independent third-party commentary as
complementary "AI-power-infrastructure" plays.

**Evidence supporting the view that this is several distinct economic
functions correlated on one demand driver, rather than one function
measured four ways:** the four companies' revenue-recognition models,
capital intensity, execution-risk profiles, and even their working-
capital dynamics are genuinely different (§§1, 5, 7, 10 above) —
equipment manufacturing (GEV, ETN, VRT) versus labor-services
contracting (PWR) is a first-order business-model split, and within the
equipment-manufacturer group, GEV's broad power-generation scope, ETN's
diversified multi-end-market Electrical business (plus an unrelated
Aerospace segment), and VRT's narrow data-center-pure focus are three
different companies by almost any operating metric other than "sells
into the same buildout." A cluster cap justified by correlated price
behavior does not require the underlying businesses to be economically
similar — correlated *loss* behavior in a downturn can coexist with
highly differentiated *businesses* in normal times, which is arguably
the more useful reading of what a correlation-based risk cap is
supposed to capture in the first place (the cap exists to bound
downside correlation, not to describe operational similarity).

**This batch's advisory conclusion**: the existing evidence is
consistent with `power_infra` being a correlation-based cluster (bound
by a shared demand driver and shared downside sensitivity) that
deliberately spans genuinely distinct economic functions, rather than a
cluster that should be read as four versions of the same company. That
is a defensible design for a correlation-based risk cap, and this
batch's evidence does not surface a reason to split the cluster or
reweight it — but this batch also did not re-measure the underlying
price correlation (§C.13's evidence is structural/economic, not a
price-correlation recomputation), so it cannot and does not confirm
that the original 0.560 correlation figure still holds today. **Any
actual reconsideration of the cluster's composition or cap remains
entirely a matter for a future, separate, explicit governance
decision**, per `PI-0026` §C and consistent with the precedent set by
the "T1 AI-infra cluster cap: scanned and declined" and the still-open
T1/T2 capital-impairment question elsewhere in this repository's
Decisions Log.

## 14. Company-specific and common margin-risk amplifiers

**Company-specific** (factual, advisory only — no leverage
recommendation, per `PI-0026` §B.20/§G): GEV carries tariff exposure
and Wind-segment margin softness (per its own existing record); ETN
carries a large, single, thesis-concentrated acquisition (Boyd Thermal)
and an announced structural separation (Mobility Group spin-off) as
near-term corporate-action risks; VRT carries the batch's most
concentrated single disconfirming risk (a named hyperscaler
disintermediation threat) and an unresolved backlog discrepancy; PWR
carries fixed-price-contract execution risk and working-capital
dynamics (unbilled receivables growth) structurally different from the
other three, plus a meaningfully larger set of stale/unresolved
disclosure items (customer concentration, S&P rating currency, legacy
litigation status) than either ETN or VRT.

**Common amplifier across all four**: each company's own record
documents a real, demonstrated historical margin-compression or
drawdown episode under macro or input-cost stress (ETN's 2008-09 and
2022 drawdowns; VRT's 2022 operating-loss quarter; GEV's ongoing Wind-
segment losses; PWR's disclosed fixed-price cost-overrun risk language) —
i.e., none of the four is a company whose current growth narrative
should be read as immune to a demonstrated, company-specific stress
scenario. This is presented as factual, comparative context only; it is
not a leverage recommendation, a safe-leverage calculation, or a
deployment-timing conclusion of any kind.

## Summary (advisory, not a ranking)

ETN, VRT, and PWR — together with existing-context GEV — complete
first-coverage research for the entire governed `power_infra` cluster.
The batch's clearest structural finding is that the four companies
occupy genuinely distinct, largely complementary positions across the
power-generation-to-data-center value chain (§1), bound together by a
real, independently-corroborated shared demand driver rather than by
operational similarity (§13). Each company carries its own,
company-specific set of disclosed risks and evidence gaps, documented
individually in `ETN.yaml`/`.md`, `VRT.yaml`/`.md`, and `PWR.yaml`/`.md`.
**This document does not rank the four companies, does not recommend
any tier, target, cluster, cap, holding, allocator, trade, or margin
action, and does not alter GEV's existing record in any way.** Any
future use of this evidence — for Milestone 4 relationship mapping, for
a cluster-composition reconsideration, or for any other purpose —
requires its own separate, later, explicit governance authorization.
