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

**Bounded corrections, 2026-07-26 (provenance statement, two separate
passes).** This document's original draft relied on the same
WebSearch-only research as `ETN.yaml`/`.md`, `VRT.yaml`/`.md`, and
`PWR.yaml`/`.md` before their 2026-07-26 corrections. This Claude
session remained access-blocked throughout -- it did not open or
inspect any primary document at any point, including for either
correction pass. **First pass:** GPT-5.6 Thinking, acting as an
independent external auditor, inspected official documents for all
three companies (see each company's own `sources[]` for the exact
URLs) and reported specific factual corrections, applied here to
remove or correct every passage that relied on since-corrected premises
(PWR having no manufacturing activity, VRT's unsupported backlog
decline, VRT's incorrect 0.8x-1.0x current leverage, ETN's Boyd Thermal
close date being unresolved, and Eaton's Mobility Group transaction
being framed as a simple standalone spin). **Second pass:** a follow-up
independent exact-head review by GPT-5.6 Thinking found this document's
first-pass correction still materially misstated PWR's data-center
exposure as entirely indirect, and reported a further correction,
applied here across §1, §2, §3, §4, and §12 below. Both reviews are
retained verbatim at
`governance/audits/PR166_PRIMARY_SOURCE_AUDIT_20260726.md` and
`governance/audits/PR166_CORRECTED_HEAD_REVIEW_20260726.md`. The
principal explicitly authorized treating both retained, independently
inspected reviews as the bounded PI-0026 evidence-recovery method. The
high-level conclusion that the four companies occupy predominantly
distinct, complementary positions is retained only because it survives
being rebuilt on the corrected facts across both passes, not because it
was mechanically carried forward.

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
| PWR | Engineering, procurement, construction (EPC), and maintenance services for electric power, utility, and communications infrastructure | **Primarily** a labor-intensive contract-services provider, with a growing, still-secondary manufacturing capability (corrected 2026-07-26 — see below) |

**Corrected 2026-07-26 by an independent primary-source audit:** this
document's original draft characterized PWR as not manufacturing
equipment at all. Quanta's own official 2025 Form 10-K states the
company manufactures power transformers and related electrical
components and owns manufacturing facilities associated with those
businesses (see `PWR.yaml`/`PWR.md` for the full correction). PWR
remains, by primary economic function, a fundamentally different
animal from GEV/ETN/VRT — a services business that predominantly
*installs and maintains* infrastructure rather than one whose core
revenue comes from equipment sales — but the contrast is now one of
degree and primacy, not an absolute manufacturing/no-manufacturing
split. **This is still the batch's single clearest structural
finding**: three of the four (GEV, ETN, VRT) are primarily equipment
manufacturers, while PWR is primarily a services business (with a
secondary, real manufacturing capability of its own). PWR's own AEP
partnership (a 765 kV transmission EPC and domestic transformer/breaker
manufacturing-capacity agreement) is, in fact, adjacent to exactly the
kind of equipment ETN and GEV sell, and — per the correction above —
partly an extension of PWR's own secondary manufacturing capability,
not solely third-party equipment PWR installs. PWR builds the
infrastructure that carries and delivers the power ETN's switchgear/
distribution equipment and GEV's turbines generate, while VRT's
equipment sits inside the data center consuming that delivered power.
**Second correction, 2026-07-26:** the "sequential path" framing below
is not as clean a hand-off as originally described — a separate
independent review found that PWR, through its CEI subsidiary, also
performs direct, in-facility electrical design/installation/
manufacturing work for data centers (more than 20 million square feet
installed, per CEI's own official materials), meaning PWR's own work
sometimes extends inside the facility alongside VRT's, not only up to
the property line. **Read together, GEV (generation) → ETN
(distribution/switching) → PWR (transmission/grid construction, plus
some of its own transformer/component manufacturing, **and** direct
in-facility electrical work via CEI) → VRT (in-building thermal/power
management) trace a path from power generation to the chip actually
being cooled that is sequential in its dominant pattern but not a
strict one-company-per-stage hand-off** — PWR's CEI channel overlaps
with the "in-building" stage VRT also occupies. This remains a
materially different comparison shape than any prior batch, where the
shared driver (AI-data-center power/electricity demand) manifests as a
**supply chain with a partial overlap at one stage**, not a strictly
sequential chain or merely a correlated basket of similarly-exposed
equipment makers.

## 2. Direct versus indirect data-center exposure

| Company | Data-center exposure | Directness |
|---|---|---|
| VRT | Data center is essentially the whole business (cooling/power management sold directly into data-center builds); AI/hyperscaler-driven liquid cooling is the current primary growth narrative | **Most direct** — data center is not a segment, it is nearly the entire company |
| GEV (existing context) | Electrification segment discloses data-center-specific order figures (>$5B combined H1 2026 orders per GEV's own record); Power segment's gas-turbine demand is driven by broader grid/generation needs, only partly data-center-specific | Direct in Electrification, more indirect/broader in Power |
| ETN | Electrical segment discloses data center as its fastest-growing named vertical (Electrical backlog +48% YoY, Q1 2026, per ETN's official results release; a ~240% YoY data-center-order-growth figure is separately reported in secondary commentary but an independent primary-source audit could not locate it in Eaton's official Q1 2026 release — see `ETN.yaml`/`ETN.md`), and non-data-center end markets (utility, industrial, institutional) are argued by at least one secondary source to still comprise the majority of Electrical backlog; Aerospace segment has no data-center exposure at all | Partial and diluted — real, but a minority of the whole company by at least one independent read |
| PWR | **Corrected 2026-07-26 — two distinct channels, not one.** (A) **Direct, in-facility**: via Cupertino Electric, Inc. (CEI), Quanta designs, engineers, procures, constructs, installs, commissions, maintains, and manufactures modular electrical systems for data centers, serving hyperscaler and technology customers directly — CEI has more than 25 years of data-center industry experience and has installed electrical systems in more than 20 million square feet of data centers, per Quanta's own official 2025 Form 10-K and CEI acquisition materials. (B) **Indirect**: utility/grid-transmission work serving data-center-driven electricity demand from outside the facility (the AEP 765 kV partnership). This record's first correction pass still described PWR's exposure as entirely indirect — that was itself corrected by a second independent review; see `PWR.yaml`/`PWR.md` for full detail. | **Both direct and indirect** — PWR is not the batch's most-indirect member; it has genuine, official, in-facility electrical work (Channel A) alongside grid-side work (Channel B). No percentage of revenue attributable to either channel or to data centers overall is disclosed. |

**No company in this batch discloses a clean percentage of revenue
attributable to data centers specifically** — VRT's concentration is
qualitative/structural (the business is built around data centers) but
not quantified as a percentage; ETN discloses order-growth rates, not
revenue share; PWR's exposure spans a direct, named acquisition (CEI)
and an indirect, named contractual relationship (AEP), with no
disclosed dollar or percentage allocation for either channel.

## 3. Utility and grid-capital-spending exposure

PWR is the most directly levered to utility capital-spending cycles by
business model — the large majority of its revenue is contract-services
work for utilities, telecom carriers, and pipeline operators, evidenced
concretely by the AEP $72B 2026-2030 capital-plan partnership.
**Corrected 2026-07-26:** this is not PWR's entire revenue base — its
official customer end-market mix discloses Technology, Manufacturing
and Communications at 13% of revenue, and its CEI subsidiary sells
directly to hyperscaler/technology customers (see §2 and §4) — but
Utility and Power alone is 70% of revenue per the same disclosure, so
utility-capex-cycle exposure remains PWR's dominant driver even after
this correction. GEV's
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

**Corrected 2026-07-26: overlap is closer to direct than this document
previously stated, at least for PWR's CEI channel.** ETN and VRT are
both named, in their own records, as competitors to *each other* in
some overlapping categories (electrical/power-management equipment for
data centers) even while occupying different primary niches (ETN
broader/diversified, VRT data-center-pure). This document's original
correction pass stated that PWR's customers were exclusively utilities
and telecom carriers, "a different customer class than the hyperscalers
and colocation operators VRT's record describes" — **that statement was
itself corrected by a second independent review**: PWR's own official
2025 Form 10-K discloses that its customer base includes hyperscalers
and technology companies, served directly through CEI's in-facility
electrical work, and CEI's own operating-company profile confirms more
than 20 million square feet of installed data-center electrical
systems. **PWR therefore overlaps with VRT (and, to a lesser extent,
ETN) on customer class — both may ultimately serve hyperscaler/
technology-company demand for data-center electrical/thermal
infrastructure — though no record in this batch discloses a specific
named shared customer** (no single hyperscaler is named as a customer
of both PWR/CEI and VRT, or both PWR/CEI and ETN). PWR's AEP
relationship remains a separate, indirect, utility-side customer
relationship, distinct from CEI's direct hyperscaler/technology
customers. **A plausible, un-evidenced structural overlap** (judgment,
not a sourced claim): the same hyperscalers/data-center developers that
are VRT's and GEV's Electrification-segment customers, and now also
understood as CEI's direct customers, are, at the far end of the grid,
also the entities whose electricity demand growth is driving utilities
like AEP to spend the capital that funds PWR's transmission
contracts — meaning PWR may serve the same hyperscaler end-customers
through two different channels (direct via CEI, indirect via
utility-funded grid work) without either channel being a disclosed,
named, shared-customer relationship with GEV/ETN/VRT. No supplier
overlap was found or asserted across any pair in this batch: PWR does
manufacture some equipment of its own (power transformers, related
electrical components, and CEI's modular electrical systems), but no
record in this batch confirms a supplier relationship between PWR and
GEV/ETN/VRT — PWR's manufacturing capability appears to support its own
EPC/service work rather than to supply the other three companies, and
it may separately install GEV's/ETN's/VRT's products on job sites,
which none of the four companies' own records confirms directly either
way.

## 5. Backlog composition and execution risk

| Company | Backlog type | Recent figures | Execution-risk character |
|---|---|---|---|
| GEV (existing context) | Equipment order backlog | $176B total (Q2 2026, per GEV's own record) | Long-cycle, fixed/competitively-bid equipment execution risk |
| ETN | Equipment order backlog | Electrical backlog +48% YoY (Q1 2026 point; ~29% YoY full-year-2025 average) | Long lead-time equipment (transformers ~4 years, switchgear 50-80 weeks) — backlog quality tied to supply-chain/capacity-build execution |
| VRT | Equipment order backlog | $15B (Q4 2025, per Vertiv's official Q4 2025 release); a $12.45B Q1 2026 figure appeared in this document's original draft but an independent primary-source audit (2026-07-26) could not substantiate it against Vertiv's official Q1 2026 release or Form 10-Q — **it is now treated as an unresolved, unsubstantiated secondary claim with no decision-bearing weight, not a confirmed sequential decline** (see `VRT.yaml`/`VRT.md`) | Equipment backlog; the previously-asserted backlog discrepancy is corrected below and no longer a confirmed batch finding |
| PWR | Mixed: firm fixed-price RPO **plus** estimated MSA-renewal orders (an explicitly disclosed methodology distinct from the other three) | Total backlog $48.5B (Q1 2026, record, per Quanta's official results release), RPO $26.2B | **Project/contract-services backlog**, not equipment-order backlog — cancellation, rescheduling, and fixed-price cost-overrun risk apply in a way that does not apply to an equipment manufacturer's booked-order backlog |

**This is a genuinely different backlog character for PWR than for the
other three.** An equipment manufacturer's backlog (GEV, ETN, VRT) is a
booked-order count awaiting manufacture and shipment; PWR's backlog
mixes firm contracted revenue with company-estimated recurring-MSA
volume, and its execution risk runs through labor availability, fixed-
price cost overruns, and project scheduling rather than component
supply chains and capacity-build timelines. **Corrected 2026-07-26:**
this document's original draft described VRT's $15B-to-$12.45B backlog
figures as "this batch's most specific, disclosed evidence gap" and an
unreconciled sequential decline. An independent primary-source audit
inspected Vertiv's official Q1 2026 results release and Form 10-Q and
could not locate a passage substantiating the $12.45 billion figure in
either document. **This claim no longer carries that weight in this
comparison** — it is disclosed in `VRT.yaml`/`VRT.md` as an unresolved
secondary claim, not treated here as a confirmed batch-level finding,
and is not used to distinguish VRT's evidence quality from the other
three companies' backlog disclosures.

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
- **ETN**: Boyd Thermal, agreed November 2025, officially completed
  **2026-03-12** per Eaton's own completion announcement (corrected
  2026-07-26 by an independent primary-source audit; this document's
  original draft described the close date as disputed across secondary
  sources), approximately $9.5B (~22.5x Boyd Thermal's estimated 2026
  adjusted EBITDA) — roughly 35% of ETN's own FY2025 total revenue in
  deal value, concentrated entirely in liquid cooling for hyperscale/AI
  data centers. ETN's own record flags this as its largest deal since
  Cooper Industries (2012). Having closed 2026-03-12, it contributes
  only a partial-quarter stub within Q1 2026 results and is not yet
  reflected in a full quarter or full-year of segment financials.
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
predominantly complementary, not duplicative, along the value chain
described in §1 — though with one genuine overlap point corrected
2026-07-26.** GEV generates power, ETN distributes/switches it, PWR
builds and maintains the grid that carries it (and, via CEI, also
performs direct in-facility electrical work), and VRT manages power and
thermal load once it reaches the building housing the compute. Holding
all four is not the same as holding four versions of the same
equipment-manufacturer bet: PWR in particular remains a genuinely
different economic animal by primary function (labor-intensive services
vs. equipment manufacturing) that would be lost largely, though not
entirely, if the cluster consisted only of GEV/ETN/VRT — CEI's direct
data-center electrical work is the one point where PWR's exposure is
not fully distinct from VRT's in-building presence, even though the two
companies sell different things (VRT: thermal/power-management
equipment; PWR/CEI: electrical-system design, installation, and
modular-system manufacturing). Within the equipment-manufacturer
subset, ETN and VRT show the most business-model overlap (both are
named as competitors to each other in some product categories), while
GEV's broader power-generation scope and PWR's primarily-services model
(corrected 2026-07-26 to acknowledge both PWR's own secondary,
still-subordinate manufacturing capability and its direct, not merely
indirect, data-center customer channel -- see §§1-2) each add
substantial distinct exposure the other three do not replicate, even
after accounting for the CEI/VRT overlap point. **This finding is about
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
carries a large, single, thesis-concentrated acquisition (Boyd Thermal,
officially completed 2026-03-12, per the 2026-07-26 correction) and an
announced structural separation -- corrected 2026-07-26 from a
standalone spin-off to a definitive Reverse Morris Trust combination
with Dana Incorporated, a materially more complex cross-company
transaction carrying its own integration and governance risk -- as
near-term corporate-action risks; VRT carries a named hyperscaler
disintermediation threat (its most concentrated single disconfirming
risk) and a real, recent (2022) historical margin-compression episode,
while a previously-asserted backlog discrepancy was corrected 2026-07-26
to a non-decision-bearing unresolved secondary claim and its net
leverage was corrected from ~0.8x-1.0x to approximately 0.2x (a
stronger, not weaker, balance-sheet position than this document
originally stated); PWR carries fixed-price-contract execution risk and
working-capital dynamics (unbilled receivables growth) structurally
different from the other three, plus a remaining set of stale/
unresolved disclosure items (S&P rating currency, unresolved FY2025
adjusted-EBITDA figure) -- narrower than this document originally
stated, since the 2026-07-26 correction resolved PWR's customer-
concentration staleness and removed decision-bearing weight from its
two previously-cited legacy litigation matters.

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
occupy predominantly distinct, complementary positions across the
power-generation-to-data-center value chain (§1), bound together by a
real, independently-corroborated shared demand driver rather than by
operational similarity (§13) -- with one genuine, corrected overlap
point: PWR, through its Cupertino Electric (CEI) subsidiary, performs
direct, in-facility electrical work for data centers that partially
overlaps with VRT's in-building presence, distinct from PWR's separate
indirect utility/grid channel (§2, §4, §12). Each company carries its
own, company-specific set of disclosed risks and evidence gaps,
documented individually in `ETN.yaml`/`.md`, `VRT.yaml`/`.md`, and
`PWR.yaml`/`.md`.
**This document does not rank the four companies, does not recommend
any tier, target, cluster, cap, holding, allocator, trade, or margin
action, and does not alter GEV's existing record in any way.** Any
future use of this evidence — for Milestone 4 relationship mapping, for
a cluster-composition reconsideration, or for any other purpose —
requires its own separate, later, explicit governance authorization.
