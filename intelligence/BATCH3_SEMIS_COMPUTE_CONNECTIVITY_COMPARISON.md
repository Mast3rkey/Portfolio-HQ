# WS-0005 Milestone 3, Batch 3 — Semiconductor Compute, Accelerated-Computing, Networking, and Connectivity Comparison

**AVGO, AMD, MRVL, INTC.** Authorized by
`governance/decisions/PI-0025-ws0005-milestone3-batch3-compute-networking.md`
§C (comparison requirements) and §I (completion criteria requiring this
evidence be retained). Created 2026-07-26, alongside the four companies' own
Company Intelligence records
(`intelligence/companies/{AVGO,AMD,MRVL,INTC}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema (it
introduces no new schema and is not scanned by `intelligence_validator.py`
or any other validator), and not an authoritative record any allocator or
policy decision may read. It sits at `intelligence/` root rather than inside
`companies/` (reserved for `<TICKER>.yaml`/`.md` pairs) or `governance/audits/`
(reserved for independently-authored audits per `OPS-0004` — this document is
authored by the same implementation session as the four company records, not
an independent review of them), matching `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`'s
and `intelligence/BATCH2_MEMORY_COMPARISON.md`'s own placement and scope. It
does **not** rank the four companies, does not recommend a tier/target/
cluster change, a buy/trim/exit, a margin action, or a next-best-alternative
ranking, and does not create a composite score of any kind — per `PI-0025`
§C's explicit instruction and the Constitution's standing prohibition on
predictive research or opportunity maps.

**Source-access disclosure (applies to this whole document):** every fact
below is inherited from the four companies' own Company Intelligence
records, each of which discloses that WebFetch was blocked throughout this
session's research pass — a tool/proxy-level HTTP 403 on every URL
attempted, including SEC EDGAR, each company's own investor-relations
domain, a secondary-filing-summary page, and a non-target control domain
(example.com) — confirmed once for this entire batch's research (see
`AVGO.md`'s Source-access disclosure for the control-domain test). **No
primary document was independently rendered and inspected by this session
at any point.** Each underlying record distinguishes document type (PRIMARY
— an issuer- or regulator-authored filing/press release; SECONDARY —
journalism or analyst commentary about one) from access status (every
primary document is labeled "identified but NOT opened by this session");
this document inherits that same distinction rather than re-stating it in
full. This document adds no new primary research of its own — it only
compares and cross-references what the four company records already
established.

## 1. Distinct business models within a shared AI-infrastructure theme

Unlike Batch 2 (MU, SKHY), where the two companies are direct competitors
selling substantially the same product categories, and more like Batch 1
(ASML, AMAT, KLAC, LRCX), where each company performs a distinct step in a
shared process, **this batch's four companies occupy four genuinely
different business-model positions that happen to share exposure to the
same AI-infrastructure capital-expenditure cycle:**

| Company | Core business model | Primary product categories |
|---|---|---|
| AVGO | Diversified semiconductor + recurring infrastructure-software conglomerate | Custom AI accelerators (XPUs), networking silicon, broadband/storage/wireless semiconductors; VMware-based enterprise software (VCF subscription) |
| AMD | Fabless CPU/GPU/accelerator designer | Server/client CPUs, discrete GPUs and AI accelerators (Instinct/MI-series), gaming semi-custom silicon, FPGA/adaptive SoC (Xilinx) |
| MRVL | Fabless networking/custom-silicon specialist | Custom compute ASICs (XPU/XPU-attach), Ethernet networking silicon, optical interconnect, storage controllers, SerDes |
| INTC | Integrated device manufacturer (IDM) pursuing external foundry customers | Client/server CPUs (in-house design and manufacture); Intel Foundry (18A/14A) as an emerging external-customer business |

This is a materially different comparison shape than either prior batch:
the question is not "which distinct step in one process does each perform"
(Batch 1) or "which distinct competitive position within one product
category does each hold" (Batch 2), but **"how differently structured are
these four businesses, and does the shared AI-capex-cycle exposure mean
they still move together despite that structural difference."**

## 2. CPU, accelerator, networking, custom-silicon, software, and foundry exposure

| Company | CPU | GPU/accelerator | Networking/interconnect | Custom silicon (ASIC/XPU) | Recurring software | Foundry |
|---|---|---|---|---|---|---|
| AVGO | No | No (custom accelerators only, not merchant GPUs) | Yes (networking silicon) | Yes (XPU design services, ~70%+ share of that specific market per one secondary source) | Yes (Infrastructure Software, ~$7.2B/quarter, VCF subscription) | No (fabless for its own chips) |
| AMD | Yes (EPYC server, Ryzen client) | Yes (Instinct MI-series) | No material standalone networking business identified | Limited (semi-custom console silicon; not a third-party XPU design-services business like AVGO's or MRVL's) | No | No (fabless, uses TSMC) |
| MRVL | No | No | Yes (Ethernet, optical/PAM4, switching — a core business, not adjacent) | Yes (XPU/XPU-attach ASICs, ~76% of revenue via Data Center segment) | No | No (fabless, uses external foundries) |
| INTC | Yes (Client Computing Group, Data Center and AI) | Limited (Data Center and AI segment includes some accelerator products; not a merchant-GPU leader) | No material standalone networking business identified | No (does not offer third-party custom-silicon design services at the scale AVGO/MRVL do) | No | **Yes — Intel Foundry, both in-house and (emerging) external-customer** |

**AVGO and MRVL both offer third-party custom-silicon (XPU) design
services** — a genuine overlap point, addressed in §9 below. **INTC is the
only company in this batch (or, distinctively, in this repository's entire
`semis` cluster except TSM) that manufactures its own products in-house at
scale while also selling foundry capacity to outside customers** — a
fundamentally different position from AVGO/AMD/MRVL's shared fabless model.

## 3. Fabless versus IDM economics

AVGO, AMD, and MRVL are all **fabless** — they design chips and pay external
foundries (predominantly TSMC) to manufacture them, meaning their capital
intensity is concentrated in R&D and design rather than fab construction,
and their gross margins are not directly burdened by fab-utilization risk.
INTC is an **integrated device manufacturer (IDM)** — it owns and operates
its own fabs (plus is separately trying to sell that capacity to others via
Intel Foundry), meaning INTC carries fab-construction capital intensity
(>$100B total planned US investment, >$20B guided for 2026 capex alone, per
`INTC.yaml`) that none of the other three companies in this batch carry
directly. This is the single clearest, most structural economic distinction
within the batch: **three fabless designers renting capacity from someone
else's balance sheet, and one IDM building and financing its own capacity
while also trying to rent it to others.**

## 4. Recurring software versus semiconductor-cycle economics

**AVGO is the only company in this batch (or, for that matter, in this
repository's entire `semis` cluster) with a large, subscription-based,
recurring-revenue software segment** — Infrastructure Software, ~$7.18B/
quarter in Q2 FY2026, built substantially around VMware Cloud Foundation.
AMD, MRVL, and INTC derive revenue almost entirely from semiconductor
product sales, which are inherently cyclical and order-driven rather than
subscription-based. This gives AVGO a structurally different revenue
character from the other three — a partial buffer against pure
semiconductor-cycle volatility that AMD, MRVL, and INTC do not have,
counterbalanced by AVGO's own VMware-specific risk (customer-relations/
churn concerns over VCF pricing, documented in `AVGO.yaml`) that the other
three companies do not carry.

## 5. TSMC and advanced-packaging dependence

AVGO, AMD, and MRVL all depend on external foundry capacity, and public
reporting (independently corroborated across this repository's existing TSM
record and this batch's four company records) places TSMC as the dominant
advanced-node/advanced-packaging supplier to this class of product
industry-wide. **None of the four companies' own records located a
company-specific, named-percentage TSMC dependence disclosure this session
opened** — the dependence is a structural inference from each company's
fabless status and industry-wide foundry concentration, not a confirmed
company-specific figure for any of the three fabless companies. **INTC's
relationship to TSMC is different in kind, not degree**: INTC is
simultaneously (a) a TSMC customer for some products, (b) a direct TSMC
competitor via Intel Foundry, and (c) explicitly contingent on winning
external customers away from TSMC (and other foundries) for its own 14A
node's viability, per the disclosed 14A pause/discontinuation contingency in
`INTC.yaml`. This is the batch's most complex foundry relationship, and it
is not comparable to the other three companies' simpler customer-only
relationship with TSMC.

## 6. Hyperscaler and customer concentration

All four companies show material, and in several cases severe, customer
concentration — but the shape differs:

| Company | Concentration evidence | Notably named customers/counterparties |
|---|---|---|
| AVGO | ~40% of net revenue from top 5 end customers (company-wide, FY2025 10-K per secondary coverage); AI-segment concentration in a small named roster | Google, Meta, OpenAI, Anthropic, Apple (XPU/AI roster) |
| AMD | A single secondary source's claim of two customers each >10% of FY2025 consolidated revenue is **unresolved** — neither confirmed nor refuted by independent search; identities not implied | Microsoft, Dell, HPE, Lenovo, Sony named as broader significant customers; OpenAI and Meta named for multi-gigawatt AI-accelerator commitments (a separately-evidenced concentration risk independent of the unresolved >10% claim) |
| MRVL | ~45% via single distributor; ~82% via top-10 customers; Amazon+Google reported 60%+ of Data Center revenue (undisputed even by the contrarian JPMorgan view on the separate Amazon-Trainium question, see §5) | Amazon, Google named specifically — the most concentrated, most specifically-named exposure in the batch |
| INTC | Not quantified in this research pass at the customer-percentage level | **Fortinet — Intel Foundry's one confirmed, named external customer** (Intel 4 node, disclosed 2026-07-21); separately, AMD, NVIDIA, Marvell, Microsoft, Micron, OpenAI named as hedged/unconfirmed Intel 18A design-win/commitment customers (a foundry-customer list, not a product-revenue-customer list, and a materially different confidence level than the confirmed Fortinet relationship) |

**MRVL's concentration is both the most severe and the most specifically
named** (Amazon + Google at 60%+ of its fastest-growing segment, undisputed
even by the contrarian view below), and it is the only company in the batch
with an actively **disputed** — not simply disconfirming — named
competitive-loss signal attached to that concentration: a reported analyst
downgrade's Amazon-Trainium loss claim versus a named JPMorgan contrarian
view reporting no lost customer orders and reiterated CY2026 purchase
orders (`MRVL.yaml`; both credible, secondary, and unresolved against each
other). **INTC's customer list is structurally different in kind on two
axes** — it names *foundry* customers (companies paying Intel to
manufacture their chips) rather than *product* customers (companies buying
Intel's own chips), a distinction this document preserves rather than
conflating with the other three companies' product-customer concentration;
and within that foundry-customer list, Fortinet is the batch's (and, among
this repository's covered `semis`-cluster companies, likely the only)
**confirmed, named** external-customer relationship, standing apart from
the remaining six hedged/rumored 18A design-win names.

## 7. Acquisition and integration dependence

| Company | Major relevant acquisition(s) | Integration status per available evidence |
|---|---|---|
| AVGO | VMware (~$69B, closed Nov 2023) | Migration to VCF subscription reported >87% of top 10,000 customers, but active customer-relations/pricing backlash documented |
| AMD | Xilinx (2022, embedded/FPGA) | Reported to have "sat dormant for years" before "finally clicking" in 2025-2026; Embedded segment returned to growth in Q1 FY2026 |
| MRVL | Celestial AI (~$1.0B cash + ~$2.25B stock upfront, up to $5.5B total with earnouts, closed 2026-02-02) and XConn (~$540M, ~60% cash/40% stock, closed 2026-02-10) — two distinct 2026 transactions, custom-silicon/interconnect | Too recent for integration-status evidence; both carry management-guided, back-loaded revenue-ramp targets (Celestial from FY2028; XConn from Q3 FY2027) integration execution has not yet had time to test |
| INTC | None material identified in this research pass | Not applicable |

AVGO's VMware integration and AMD's Xilinx integration are both several
years post-close and show measurable, if mixed (AVGO) or delayed-then-
positive (AMD), results. MRVL's two 2026 acquisitions are too recent for
this research pass to assess integration outcome — they are flagged as an
open, near-term execution risk in `MRVL.yaml` rather than assessed either
way. INTC is the only company in this batch without a major recent
acquisition driving its current growth story — its growth instead depends
on organic execution (18A yield/output) and a very large organic capital
program, a different risk shape from the other three's acquisition-
integration dependence.

## 8. AI-capex opportunity and common AI-capex-cycle risk

All four companies' current growth narratives are tied, directly or
indirectly, to the same AI-infrastructure buildout cycle:

- **AVGO**: AI semiconductor revenue +143% YoY, guided to ~$56B for FY2026
  and >$100B for FY2027, driven by hyperscaler/frontier-lab XPU demand.
- **AMD**: Data Center revenue +57% YoY, ~73% of which is AI accelerators,
  driven substantially by two very large forward hyperscaler/frontier-lab
  commitments (OpenAI, Meta) that have not yet fully converted to
  recognized revenue.
- **MRVL**: Data Center revenue +27% YoY (76% of total revenue), driven by
  the same hyperscaler AI-infrastructure buildout, delivered via networking/
  interconnect and custom silicon rather than accelerator chips themselves.
- **INTC**: Data Center and AI segment +59% YoY, and Intel Foundry's 18A
  external-customer thesis is itself substantially an AI-infrastructure bet
  (several of its named design-win customers — NVIDIA, Marvell, Microsoft,
  OpenAI — are themselves AI-infrastructure companies).

**This is the batch's clearest shared correlated-loss mechanism**: a
broad-based, simultaneous pullback in AI capital expenditure by the
hyperscaler/frontier-lab cohort (Google, Meta, Amazon, Microsoft, OpenAI,
Anthropic — a group that recurs, by name, across all four companies'
records) would plausibly affect all four companies' fastest-growing
segments simultaneously, even though each company's specific product
(custom accelerators, CPUs, networking, or foundry capacity) is different.
The mechanism is common; the transmission channel differs by company.

## 9. China/export-control and geopolitical exposure

| Company | China/export-control exposure | Status |
|---|---|---|
| AVGO | ~20% of revenue China-derived; US export-control review tightened 2026-01-15; China banned VMware cybersecurity software (Jan 2026), a distinct action against the software segment | Ongoing, three compounding vectors |
| AMD | Realized $800M inventory charge (Q2 FY2025) plus estimated $1.5-1.8B cumulative 2025 revenue impact from MI308 export restrictions; some licenses since granted but no recorded China MI308 revenue as of the quarter reviewed; China ~20% of overall AMD revenue per CEO commentary | Realized impact, partially licensed but not yet monetized |
| MRVL | Not separately quantified in this research pass | Not established |
| INTC | Not separately quantified in this research pass; national-security/domestic-manufacturing framing dominates INTC's geopolitical exposure instead (see §10) | Different geopolitical exposure shape (domestic-policy-driven, not China-export-driven) |

AVGO and AMD both show **realized, quantified** China/export-control
impacts — a genuine point of comparability between the two. MRVL's China
exposure was not established in this research pass (a gap, not a finding of
absence). INTC's geopolitical exposure is qualitatively different — it runs
through US domestic-manufacturing policy and a US government equity stake,
not primarily through China export restrictions on outbound product, and
this document does not conflate the two distinct geopolitical-exposure
shapes.

## 10. Subsidy and geopolitical exposure — Intel's distinctive position

INTC is the only company in this batch (or, among this repository's
covered `semis`-cluster companies, likely the only one at all) with a direct
US government equity stake arising from CHIPS Act grant conversion, plus
additional NVIDIA (~4%) and SoftBank (~2%) equity stakes. **The government
ownership percentage is reported inconsistently across sources and is not
compressed into a single range here** — `INTC.yaml`/`INTC.md` record four
distinct values found across different sources: **9%** and **10%**
(rounded/headline figures from initial announcement-era coverage, August-
September 2025, when the CHIPS-grant-to-equity conversion was first
reported); **9.9%** (a more precise figure also dated to the same
announcement window); and **8.4%** (the most recent figure found, dated
2026-03-20, sourced to a later secondary-filing-adjacent disclosure of
433,323,000 shares outstanding as of that date). This record does not adopt
one value as correct. A plausible, but independently unconfirmed, reading is
that the 8.4% figure reflects *dilution* from subsequent share issuances
(the NVIDIA and SoftBank private placements both occurred after the initial
government-stake transaction) reducing the government's percentage of a
larger total share count without necessarily changing its absolute share
count — but this record does not treat that explanation as established,
since no source directly confirms the government's absolute share count
was unchanged between the two measurement dates. Whether the differing
figures represent initial-versus-diluted ownership, different transactions,
approximate-versus-precise reporting, or genuinely different measurement
dates therefore remains an open evidentiary question, not a resolved fact
compressed for convenience. This creates a
governance and national-security-politicization dimension unique to INTC in
this batch: CHIPS Act/DFA funding terms are reported to restrict dividends
and buybacks and preserve US government remedies for breach — commercial
constraints tied to a US industrial-policy relationship, not a market-based
capital structure decision. No other company in this batch carries an
equivalent government-ownership or subsidy-conditionality structure.

## 11. Capital intensity and balance-sheet resilience

| Company | Debt/leverage evidence | Capital-intensity profile |
|---|---|---|
| AVGO | $62.655B long-term debt reported; debt/EBITDA 1.24x; A-/BBB+ ratings, positive outlooks | Moderate-to-high absolute debt (acquisition-driven), but reported low leverage ratio and improving credit trajectory |
| AMD | $3.3B aggregate debt; $12.3B cash/short-term investments | Lightest balance sheet in the batch by a wide margin |
| MRVL | Senior notes $499.9M-$750.0M across maturities; undrawn revolver available through 2030 | Comparatively light debt; contingent liquidity backstop |
| INTC | Multiple new equity infusions (government, NVIDIA, SoftBank) materially strengthening liquidity; specific debt figure not established in this research pass | Highest capital intensity in the batch by a wide margin (>$100B total US fab investment, >$20B FY2026 capex alone) |

**AMD shows the lightest, most conventionally conservative balance sheet in
this batch.** AVGO carries the largest absolute debt load but a
reportedly-improving leverage ratio and credit trajectory. MRVL's debt is
comparatively modest with a real liquidity backstop. **INTC's capital
intensity is categorically different from the other three** — it is not
primarily debt-financed in the evidence found, but equity- and subsidy-
financed (government/NVIDIA/SoftBank stakes), and its capital deployment
(fixed, large, multi-year domestic fab projects) carries a fundamentally
different risk shape (single-project delay risk, illustrated by the Ohio
project's reported delay to 2030) than the other three companies' more
flexible, non-fab-owning capital structures.

## 12. Duplicated portfolio exposure and structural/economic overlap versus measured price correlation

**Genuinely differentiated exposure across all four:**
- **AVGO** is the only company in the batch (and in this repository's
  covered `semis` names generally) combining AI-accelerator design services
  with a large recurring-software business — a business-model combination
  none of the other three replicate.
- **AMD** is the most horizontally diversified single company (CPU + GPU/
  accelerator + gaming + embedded), providing broader single-name
  diversification than AVGO, MRVL, or INTC individually offer within their
  own narrower core businesses.
- **MRVL** provides the batch's most concentrated, purest exposure to
  data-center networking/interconnect specifically — a function AVGO, AMD,
  and INTC do not offer as a standalone core business (AVGO's networking
  silicon is smaller and bundled with its broader semiconductor segment).
- **INTC** provides the batch's only IDM/foundry exposure, and the only
  direct US-government-ownership/domestic-manufacturing-policy exposure —
  neither replicated by any other holding in this batch.

**Where the four companies mostly overlap:** all four share exposure to the
same AI-infrastructure capital-expenditure cycle (§8) and, to varying
degrees, the same hyperscaler/frontier-lab customer cohort (Google, Meta,
Amazon, Microsoft, OpenAI, Anthropic recur across all four records). AVGO
and MRVL specifically overlap in offering third-party custom-silicon (XPU)
design services (§2) — the batch's clearest single point of direct
competitive overlap, though even here the companies' overall business
models remain otherwise distinct (AVGO's software segment and AMD/MRVL's
absence of one; MRVL's networking-silicon focus versus AVGO's broader
semiconductor product range).

**Structural/economic overlap versus measured historical price
correlation, per `PI-0025` §C.11 and `OPS-0006` §4 Milestone 4's own
distinction:** this document assesses only structural/economic overlap
(shared customers, shared AI-capex-cycle exposure, shared foundry
dependence where applicable) as established above. **No measured historical
price-correlation figure for any pair or subset of these four companies was
computed, sourced, or is presented in this document** — that is a distinct
analytical exercise this batch's authorization does not require and this
document does not perform, consistent with the same distinction Batch 1's
and Batch 2's own comparison documents preserved.

**Overall assessment (descriptive, not a recommendation, per `PI-0025` §C's
explicit prohibition on ranking or scoring):** these four companies add
real, evidenced differentiated exposure to distinct parts of the
semiconductor-compute/networking/foundry value chain — a software-hybrid
conglomerate, a horizontally-diversified fabless designer, a networking/
custom-silicon specialist, and the portfolio's only IDM/foundry name — while
sharing a real, common AI-infrastructure-capex-cycle correlated-loss
mechanism that a holder of any single one of the four would also be exposed
to. Whether that differentiated layer is "worth" holding all four names, at
what size, or relative to any other capital use is a capital-priority and
policy question this document is explicitly prohibited from answering
(`PI-0025` §C, §H) and defers entirely to any future, separately authorized
policy process.

## 13. Company-specific and common margin-risk amplifiers

*(Factual, advisory only — no leverage recommendation of any kind. The
1.8x leverage cap and 30% buffer floor are unchanged and out of scope.)*

**Common amplifier:** all four companies' fastest-growing revenue lines
depend on continued AI-infrastructure capital expenditure by a recurring,
overlapping cohort of hyperscalers/frontier labs (§8) — a shared,
correlated-loss pathway that would affect all four simultaneously in a
broad AI-capex pullback scenario, distinct from an idiosyncratic,
company-specific shock.

**Company-specific amplifiers:**
- **AVGO**: compounding China exposure across three distinct vectors (§9);
  VMware customer-churn uncertainty as a second, largely independent
  potential revenue-shock mechanism.
- **AMD**: realized, quantified export-control gap risk (a discrete $800M
  charge plus an estimated $1.5-1.8B cumulative impact) demonstrating
  regulatory action can produce sudden, discrete earnings hits.
- **MRVL**: the most severe simultaneous legacy-segment contraction in the
  batch (Carrier -75%, Enterprise -58% YoY), meaning less non-AI revenue to
  fall back on, plus the batch's most concentrated, most specifically-named
  customer exposure (Amazon+Google, undisputed) and its single most
  actively-*disputed* named signal (the Amazon-Trainium loss claim versus a
  named JPMorgan contrarian view) — a real, unresolved uncertainty either
  way, not a one-sided confirmed loss.
- **INTC**: the batch's highest capital intensity and only large,
  fixed-project delay risk (the Ohio project), plus a unique governance/
  national-security-politicization dimension from its new government/
  NVIDIA/SoftBank equity stakeholders, and an explicit, self-disclosed
  strategic-pivot contingency (the 14A pause/discontinuation trigger).

## 14. Thesis-deterioration detectability and likely review triggers

Each company's own record defines its own review triggers (see each
`.md`'s Review framework section); consolidated observations:

- **INTC** discloses the most observable, management-stated thesis-break
  trigger in the batch: insufficient committed 14A external demand leading
  to a pause/discontinuation — a rare case of a company pre-announcing what
  evidence would cause it to abandon a core strategic bet.
- **MRVL**'s thesis deterioration would likely be detectable first through
  a resolution of the disputed Amazon-Trainium claim (in either direction)
  or a broader Data Center guidance miss — both are named, trackable events,
  not vague sentiment shifts.
- **AMD**'s thesis deterioration would likely be detectable through a
  disclosed delay or renegotiation of the OpenAI/Meta multi-gigawatt
  commitments, or a China export-control policy change.
- **AVGO**'s thesis deterioration is the least singularly-triggered of the
  four — it could come from either an AI-segment customer pullback or a
  VMware-specific churn event, two largely independent pathways, making a
  single clean trigger harder to define than for the other three.

## 15. Where evidence is insufficient to compare confidently — consolidated

Per the same discipline Batch 1's and Batch 2's own comparison documents
applied, consolidated from all four company records' own disclosed gaps:
- **No AI-segment-specific customer-concentration percentage** was located
  for AVGO (only a company-wide top-5-customer figure); no
  customer-concentration percentage at all was located for MRVL beyond the
  batch-level figures already cited, or for INTC's product (as opposed to
  foundry) customers.
- **No company-specific, named-percentage TSMC dependence** was confirmed
  for AVGO, AMD, or MRVL — inferred structurally, not confirmed
  company-specifically.
- **The exact current US government ownership percentage in INTC** is
  reported inconsistently across four distinct values found (9%, 9.9%, 10%
  at announcement time; 8.4% at a later measurement date) — see §10 above
  for the full disclosure — and is not resolved by this document.
- **No quantified China/export-control exposure** was located for MRVL in
  this research pass.
- **MRVL's 2026 Celestial AI/XConn acquisition prices and structures were
  located** in this bounded correction pass (§7 above; both figures sourced
  to company press releases identified but not directly opened) — no longer
  an evidence gap. Integration *outcome* remains genuinely unassessable
  given both transactions' recency and management's own back-loaded revenue
  guidance.
- **No direct, quantitative AVGO-vs-MRVL competitive-overlap measure**
  (e.g., shared customer dollar amounts, or evidence of the two companies
  competing head-to-head for the same specific XPU design win) was located
  — both are reported to offer custom-silicon design services broadly, but
  no source found compared them against each other directly for the same
  customer engagement.
- **No measured historical price-correlation figure** for any pairing
  within this batch, consistent with §12's explicit scope limitation.

## 16. Cross-batch structural and correlated-risk overlap with Batch 1 (ASML, AMAT, KLAC, LRCX)

Added in this bounded correction pass (addressing independent-review finding
F8). This section is descriptive only — it does not rank companies across
batches, does not recommend a cluster-level capital-allocation change, and
does not create a composite score. All four Batch 1 companies and all four
Batch 3 companies share membership in the same governed `semis`
correlated-cluster cap (`targets.yaml`, ≤25% of book) — this section
examines *why* that shared membership is economically coherent, not merely
that it exists on paper.

**Shared exposure to AI and advanced-node semiconductor capex.** Batch 1
(ASML lithography; AMAT/KLAC/LRCX deposition/etch/process-control) sells
capital equipment to the same foundries and IDMs whose own capacity
expansion is driven substantially by the same AI-infrastructure demand this
document's §8 identifies as Batch 3's central shared risk mechanism. This is
not a coincidental overlap: Batch 1's own comparison artifact
(`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`) and this repository's
TSM Company Intelligence record both independently document that
semiconductor-capital-expenditure cycles are the equipment makers' primary
demand driver, and Batch 3's AVGO/AMD/MRVL records each depend on the same
advanced-node/advanced-packaging manufacturing capacity that Batch 1's
companies help build.

**Equipment demand depends on foundry and IDM capacity expansion — and
Batch 3 contains both the demand-side customers and, uniquely, a capacity-
building IDM.** AVGO, AMD, and MRVL are fabless — they do not buy
semiconductor capital equipment directly, but their growth drives TSMC's
(and other foundries') capacity expansion, which in turn drives foundry
purchases of ASML/AMAT/KLAC/LRCX equipment. **INTC is structurally
different and creates the batch's most direct link to Batch 1**: as an IDM
building its own fabs (Arizona, Ohio, New Mexico, Oregon; >$100B total
planned investment, per `INTC.yaml`), Intel is very likely a **direct
purchaser** of the same categories of lithography, deposition, etch, and
process-control equipment Batch 1's four companies produce — this document
does not have a confirmed, named Intel-ASML/AMAT/KLAC/LRCX supplier
relationship for the current build-out specifically (a gap, not a finding
of absence), but the structural relationship (IDM fab construction requires
this equipment category, near-universally, in current industry practice) is
a materially closer and more direct link than AVGO/AMD/MRVL's indirect,
foundry-intermediated relationship to the same equipment demand.

**How AMD/AVGO/MRVL fabless growth indirectly drives TSMC and
packaging/equipment demand.** §5 of this document already establishes that
AVGO, AMD, and MRVL all depend on TSMC and advanced-packaging capacity, and
that TSMC management has itself stated advanced-packaging capacity is
currently tight enough to constrain customer growth (per this repository's
TSM record). Every incremental unit of AVGO/AMD/MRVL demand that TSMC
fulfills by adding capacity is, mechanically, incremental demand for the
categories of equipment Batch 1's four companies sell to TSMC. This is an
indirect, foundry-intermediated transmission channel, distinct from INTC's
direct-purchaser relationship described above.

**Common downside pathways.** Both batches would plausibly be affected,
though not necessarily identically or simultaneously, by:
- **AI-capex slowdown**: a broad hyperscaler/frontier-lab AI-infrastructure
  pullback (this document's §8) would eventually reduce foundry/IDM capacity-
  expansion orders, which would reduce Batch 1's equipment demand — likely
  with a lag, since capital-equipment orders and fab construction are
  longer-cycle commitments than chip-product demand.
- **Export controls**: Batch 1's own comparison artifact documents ASML's
  and the equipment makers' own China/export-control exposure; this
  document's §9 documents AVGO's and AMD's realized China/export-control
  impacts. A broad escalation could affect both batches simultaneously,
  though through different specific mechanisms (equipment-export
  restrictions to China for Batch 1; product/chip-export restrictions for
  Batch 3).
- **Node delays**: a delay in a major foundry's or IDM's node ramp (e.g.
  INTC's own disclosed 18A/14A execution risk, or TSMC's N2/N2P/A16
  timeline per this repository's TSM record) directly delays the equipment
  purchases Batch 1 depends on, while also directly affecting the fabless
  Batch 3 companies' own product roadmaps if they are customers of the
  delayed node.
- **Customer concentration**: both batches show material customer
  concentration — Batch 1's equipment makers concentrate revenue among a
  small number of foundries/IDMs (per Batch 1's own comparison artifact);
  Batch 3's fabless companies concentrate among a small number of
  hyperscaler/frontier-lab customers (this document's §6). A shock to either
  concentrated customer base could transmit, with different lags, to the
  other batch.
- **Semiconductor-cycle contraction**: a broad, non-AI-specific
  semiconductor downturn (the kind Batch 1's and Batch 2's own comparison
  artifacts document historically, e.g. the 2022-2023 memory-cycle
  contraction) would likely reduce capital spending industry-wide,
  affecting Batch 1's equipment orders and Batch 3's non-AI product lines
  (MRVL's Carrier/Enterprise segments; AMD's Gaming/Client segments)
  simultaneously, even if the AI-specific portions of both batches remained
  comparatively insulated.

**Structural/economic overlap versus measured historical price
correlation, restated for this cross-batch comparison.** Consistent with
§12's scope limitation for within-batch comparison, **no measured
historical price-correlation figure between any Batch 1 and any Batch 3
company was computed, sourced, or is presented here.** The overlap
described above is a structural/economic-mechanism analysis only — the same
kind of analysis `OPS-0006` §4 Milestone 4's own text distinguishes from
"measured historical price correlation" — and this section does not
substitute for, or anticipate the conclusions of, the still-unauthorized
Milestone 4 relationship-mapping work.

**No ranking or capital-allocation recommendation.** This section does not
conclude that either batch is a "better" or "safer" cluster exposure, does
not recommend adjusting the `semis` cluster cap, and does not recommend any
trim, buy, or reallocation between the two batches' companies. It documents
why the existing, unchanged `targets.yaml` cluster-cap membership is
economically coherent for both batches — nothing more.

## 17. External opportunity and replacement-candidate scan — batch-level consolidation

Per each company's own record (§B.11/B.18-equivalent field). Consolidated
here as a small, evidence-supported leads list. **All items below are
future-research leads only** — none is researched as a full company, none
is added to holdings, none is assigned a tier or target, none is ranked, and
none authorizes expanding this batch or beginning research on any of them
without its own separate future authorization, per `PI-0025` §H.

| Candidate | Possible economic role | Competes against |
|---|---|---|
| NVIDIA (NVDA) | Already a current portfolio holding (not a new candidate) — named repeatedly across all four records as the dominant AI-accelerator competitor/ecosystem partner (AMD's direct competitor; AVGO's/MRVL's customer via TPU/networking partnerships; INTC's foundry-relationship counterparty and equity investor) | Not a new research candidate; recorded here only because its recurrence across all four records is itself a data point for future Milestone 4 relationship-mapping work, not a Milestone 3 finding |
| Samsung Foundry | Named in TSM's own existing Company Intelligence record as a considered-but-unestablished foundry alternative; potentially relevant to INTC's foundry-competitive-position question | Would represent a different economic role (another IDM/foundry) than an addition to this batch's existing exposure; not assessed for accessibility or investability in this pass |
| Qualcomm (QCOM) | Referenced in industry commentary (not directly cited in any of this batch's four records, but a commonly-cited adjacent fabless designer with data-center/custom-silicon ambitions) as a potential future entrant into the same custom-silicon/data-center space AVGO and MRVL currently occupy | Not independently researched in this pass; recorded only as a name that recurred in adjacent search results without being adopted as a sourced fact in any company record |

No candidate above is recommended for purchase, tier assignment, or further
research by this document. Any future research on any of them requires its
own separate authorization, per `PI-0025` §H.

## 18. Zero-based discipline note

Per `OPS-0006` §§2/3 and `PI-0025` §F, this comparison was constructed from
the four companies' own independently-researched records, each of which
reasoned its conviction rating from disclosed business/risk evidence before
— not by way of — the companies' existing governed tier/target/cluster
placement. The four companies currently hold three different tier
placements (AVGO: T2, 1.65%; AMD and MRVL: band, 0.75%; INTC: spec, 1.00%
fixed), yet two of the four (AMD, MRVL) received the same **Medium**
conviction rating as INTC, while AVGO received **High** — this document does
not treat the rating pattern as evidence the companies are more or less
alike than the structural analysis above shows; each company's own record
reasoned its rating from distinct evidence (AVGO's rating weighs its
software-segment diversification and credit trajectory most heavily against
its China/VMware risks; AMD's weighs its balance-sheet strength and
diversification against its distant-second AI-accelerator position; MRVL's
weighs its growth and design-win pipeline against its severe legacy-segment
contraction and named customer-loss signal; INTC's weighs its genuinely
strong Q2 2026 turnaround evidence against its conditional 14A contingency
and restructuring-in-progress state) — and this document's own structural
comparison above stands independent of where each rating landed on the
shared four-value scale. Any apparent tension between this batch's evidence
and current policy (for example, INTC's spec-tier fixed-target treatment
alongside a Medium rather than lower/higher conviction rating, or AVGO's T2
placement alongside the batch's only High rating) is recorded as a future
reconciliation question for the still-unauthorized Milestone 7, not resolved
or implemented here.
