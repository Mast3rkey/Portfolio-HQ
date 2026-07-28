# CRWD — CrowdStrike Holdings, Inc.

Last updated: 2026-07-28 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0030-ws0005-milestone3-batch8-enterprise-software-cybersecurity.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior CrowdStrike Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 8, alongside `IBM`, `NOW`, `CRM`,
`ORCL`, and `PANW` ("Enterprise Software and Cybersecurity"). `EQIX` and
`UNH` are not part of this batch and remain uncovered and unauthorized.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-28 were tested
and confirmed blocked (HTTP 403) on SEC EDGAR, multiple company
investor-relations domains, and a neutral, non-target control domain
(`en.wikipedia.org`), confirming a session-wide network-policy denial,
matching the pattern already disclosed in this repository's Batch 1-7
records.

The governing implementation authorization supplied
`BATCH8_enterprise_software_cybersecurity_evidence_bundle_20260728_v1.yaml`,
authored by an independent primary-source evidence-recovery researcher. This
session independently verified the bundle's SHA-256
(`4ee63b1f5eb8cfaf64d404fde6fd8cb52f806ebe091f7b911e4b871e48b2b61c`) and its
measurements (1612 lines, 8139 words, 78577 bytes) against the uploaded copy
and its external `.sha256` manifest before use. The bundle is a frozen,
principal-supplied implementation input, not committed to this repository,
and is synthesized in `governance/audits/BATCH8_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260728.md`.
**Every fact below was directly inspected by the bundle's author, not by
this Claude session** -- see `CRWD.yaml`'s `sources[]`.

**Bounded correction (2026-07-28, same day, this PR).** This record's
profitability and cash-flow disclosure (below) was added after PR #177's
formal independent exact-head review (GitHub review `4797499925`, verdict
CHANGES REQUIRED) flagged the earlier draft's absence of financial-quality/
margin-relevance evidence (MATERIAL finding 1). The correction draws on a
principal-supplied, frozen supplemental evidence-recovery bundle
(`BATCH8_supplemental_evidence_recovery_20260728_v2.yaml`, SHA-256
`e07020e0d0c97ec2ca8a04fed10b5b4b07900785d3457ce78c9a2057ae5fba32`; 1019
lines, 6828 words, 60545 bytes), independently re-verified byte-for-byte by
this session against the uploaded copy and its external `.sha256` manifest,
and independently confirmed to have exact claim-level/reverse-index
reciprocity before use. That first correction was narrowly scoped to the
profitability/cash-flow figures only.

**Second bounded correction (2026-07-28, same day, this PR).** A fresh
exact-head independent reassessment (GitHub review `4798513926`, reviewed
head `e2ecda34f5c6b87946b1e422bad77fc56e3abdf4`, verdict CHANGES REQUIRED)
confirmed the first correction's new facts as accurate but found finding
1's liquidity/debt sub-component and finding 2 (AI-monetization) both still
fully open. This session's own `WebFetch` access was re-tested this same
day and reconfirmed blocked session-wide (SEC EDGAR and a neutral
non-target control domain both returned HTTP 403), so this second
correction resumes using previously unused claims from the same
already-verified `BATCH8_supplemental_evidence_recovery_20260728_v2.yaml`
bundle -- not fresh primary-source inspection performed by this session.
The liquidity/debt and Charlotte AI content below (per claims CRWD-SUP-C1,
CRWD-SUP-C3, and CRWD-SUP-C4) closes finding 1's remaining sub-component
and finding 2.

## Business summary

CrowdStrike's Falcon platform uses a cloud-native architecture and a common
sensor across endpoint, cloud, identity, SIEM, and other modules --
**reported 32 modules at fiscal year-end 2026 and 33 at filing** -- with
subscription pricing by endpoint and module. Module breadth is disclosed
platform reach, not by itself a proxy for adoption depth, retention, or
economic quality.

## Recurring-revenue quality

CrowdStrike reported fiscal-year-end 2026 Annual Recurring Revenue (ARR) of
approximately **$5.253 billion, up 24%**. The company's own ARR definition
**assumes expiring contracts renew on existing terms** and **can include
active post-expiration renewal negotiations** -- it is not GAAP revenue and
may overstate durability if renewals later contract or fail. It is not
directly comparable to Palo Alto Networks' NGS ARR or any other issuer's
RPO in this batch without accounting for each definition's own scope.

## Profitability and cash flow (Q1 fiscal 2027)

For Q1 fiscal 2027, CrowdStrike reported **$590.9 million of GAAP operating
cash flow** and **$468.5 million of issuer-defined free cash flow**. The
company reported **consolidated GAAP net income of $45.966 million**, of
which **$18.192 million was attributable to non-controlling interests**,
leaving **GAAP net income attributable to CrowdStrike of $27.774 million**.
In the same quarter, GAAP operating loss was approximately **$30.6 million**
against non-GAAP operating income of approximately **$325.7 million** --
the gap reflects stock-based compensation, acquisition-related adjustments,
and other items excluded from the non-GAAP measure. **One profitable
quarter does not establish durable GAAP profitability**: CrowdStrike carries
an accumulated deficit of approximately $1.3 billion and states it may not
sustain profitability. Free cash flow is a non-GAAP measure and should not
be read as total cash retained after all outlays.

## Liquidity and debt

At April 30, 2026, CrowdStrike reported **$4.553 billion in cash and cash
equivalents**, **$66 million in strategic investments**, and **$745.8
million of long-term debt** -- primarily the $750 million 3.00% Senior
Notes due February 2029. Cash materially exceeded reported debt at the
quarter end, and management stated existing cash and operating cash flow
were expected to cover anticipated working-capital and capital-expenditure
needs for at least 12 months. **This liquidity strength does not make the
company risk-free**: the assessment excludes an estimable ultimate loss for
the July 19 incident proceedings (no reasonable range could be determined),
acquisitions and investments remain significant uses of cash, strategic
investments may be illiquid or volatile and are not treated as cash, and
management's 12-month sufficiency statement is not a guarantee.

## Charlotte AI -- capability and monetization limit

CrowdStrike describes **Charlotte AI** as an agentic-AI capability within
the Falcon platform, with announced **AgentWorks** and **Agentic MDR**
initiatives, and an official **Charlotte Agentic SOAR** product page
offering flexible, credit-based commercial packaging -- more than a
conceptual roadmap. **However, the inspected filings and earnings materials
do not separately disclose Charlotte AI revenue, ARR, ACV, customer count,
margin, or contribution to Falcon platform economics.** The correct
characterization is "commercially packaged, but standalone economics
undisclosed" -- AI revenue should not be inferred from company-wide ARR
growth or management's pipeline/technology-wave commentary.

## The July 19, 2024 Falcon sensor incident

The July 19, 2024 Falcon sensor update caused Windows-system outages.
**Later filings state** the incident harmed sales, reputation, and partner
relationships, and led to **customer commitment packages, longer sales
cycles, and some contraction**. This record distinguishes the original,
filed incident disclosure (Item 8.01, 2024-07-22) -- which described an
evolving situation and did not quantify full consequences -- from the
company's later, fuller assessment in its fiscal 2026 Form 10-K and Form
10-Q. **The company also reported continued ARR growth (+24%) and high
retention after the incident** -- both facts are filed and neither should
be read to the exclusion of the other; this is a genuinely mixed picture,
not a one-sided negative or positive narrative.

## Unresolved legal and financial exposure

CrowdStrike states it **cannot estimate the loss range** from outage-related
proceedings and that **insurance is not expected to cover all possible
costs, claims, and liabilities**. Recorded settlement offers were described
as immaterial and offset by insurance at fiscal year-end 2026, but broader
exposure -- government inquiries, customer claims, litigation -- remained
unresolved in the inspected sources. For Q1 fiscal 2027 specifically,
CrowdStrike recorded **$18.1 million of incident expenses net of insurance
receivable** and a **$17.1 million related quarter-end balance** -- current,
filed cost figures that are small relative to the company's cash position,
but the company's own inability to estimate the ultimate loss range is
unchanged, and this recorded balance should not be read as a cap on ultimate
exposure. **This record does not, and cannot, quantify an ultimate
liability** -- doing so would exceed what the filings themselves establish.

## Competitors, substitutes, and shared drivers

Palo Alto Networks is CrowdStrike's most directly named overlapping
competitor in this batch, alongside other endpoint, XDR, and
platform-consolidation vendors more broadly. See
`BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` for the required
direct CRWD/PANW overlap comparison -- distinct architectures, incident
histories, and metric definitions mean holding both is not automatically
either genuine diversification or pure duplication; this record does not
resolve that question for CRWD alone.

## Disconfirming evidence

- Outage-related concessions, sales delays, litigation, and uncertain
  liabilities challenge the otherwise strong ARR and platform narrative.
- The company's own filings state it cannot estimate the ultimate loss
  range, and insurance is not expected to cover all possible costs and
  claims.
- Post-outage renewal cohorts, government inquiry outcomes, and
  product-level competitive win rates remain unresolved in the inspected
  sources.
- Q1 fiscal 2027 GAAP profitability ($45.966 million consolidated;
  $27.774 million attributable to CrowdStrike after non-controlling
  interests) is a single-quarter result against an accumulated deficit of
  approximately $1.3 billion, and stock-based compensation and
  acquisition-related adjustments materially affect the non-GAAP operating
  figures relative to the GAAP operating loss in the same period.
- Liquidity strength (cash of $4.553 billion versus $745.8 million of
  long-term debt) excludes any estimate of the July 19 incident's ultimate
  loss range, and management's 12-month sufficiency statement is not a
  guarantee.
- Charlotte AI has a commercial packaging architecture (credit-based
  pricing, AgentWorks, Agentic MDR) but no separately disclosed standalone
  revenue, ARR, ACV, customer count, or margin -- the AI-monetization thesis
  is not established by disclosed economics.

## Thesis-break conditions

A thesis-break condition would include sustained outage-related churn,
material uncovered liabilities, or evidence that platform expansion depends
on concessions that erode ARR quality and unit economics. Continued
net-new ARR and high retention could instead demonstrate resilience --
contract lags and litigation timing require extended, multi-quarter
monitoring, not a single data point.

## Unresolved questions

- Ultimate outage loss range and insurance recovery.
- Renewal cohorts after commitment-package expirations.
- Government inquiry outcomes.
- Product-level competitive win rates.
- Charlotte AI's standalone revenue, ARR, ACV, customer count, margin, and
  contribution to Falcon platform economics.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, CrowdStrike currently sits in the **band** tier (0.75%
target weight, 1.25x cap). CRWD is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital priority and next-dollar considerations

**Business quality**, per the evidence above, shows a cloud-native,
multi-module security platform with disclosed, filed evidence of continued
ARR growth and high retention even after a major, publicly disclosed
operational incident -- set against material, currently unquantifiable
legal and reputational tail risk from that same incident.

**Capital priority is a separate question, and CRWD's own current band
placement (0.75% target, 1.25x cap) -- shared with IBM, NOW, CRM, ORCL, and
PANW in this batch -- is itself a data point this record preserves as
historical policy, not evidence.** CrowdStrike's distinct exposure within
this batch is pure-play, cloud-native endpoint/XDR cybersecurity -- closely
overlapping with PANW's platformization strategy (see the comparison
artifact) but architecturally and historically distinct, and materially
different from the batch's four non-cybersecurity software/infrastructure
names. **What would be lost if CRWD were absent:** direct exposure to the
cloud-native endpoint-security segment specifically, and to a company that
has demonstrated (per the filed evidence) an ability to sustain ARR growth
through a major, publicly disclosed operational crisis.

**Factors that could support greater capital priority** include the
disclosed ARR growth and retention resilience shown even through the
outage's aftermath, and the platform's cloud-native architectural
differentiation. **Factors favoring an alternative use of capital** include
the currently unquantifiable legal/insurance exposure from the outage, the
unresolved question of whether post-outage renewal cohorts will hold, and
the direct competitive and metric-comparability overlap with PANW that
means the two together may duplicate rather than diversify
cybersecurity-platform exposure (see the comparison artifact's required
CRWD/PANW analysis). A reviewer weighting the resolved-tail-risk profile of
a company without comparable unquantified litigation exposure more heavily
could reasonably favor an alternative use of capital instead.

Business quality and portfolio capital priority are separate judgments.
This record does not determine the governed target: CRWD's current band
tier and 0.75% target remain binding, this Intelligence record does not
change them, and a final next-dollar decision requires portfolio-wide
comparison and principal approval.

## Freshness and next-review requirements

Research cutoff: **2026-07-28**. Known unavailable material: any material
settlement, government inquiry outcome, or litigation development in the
outage-related proceedings beyond what was disclosed in the Q1 FY2027 Form
10-Q was not available by the cutoff per the governing evidence bundle.
Next review due **2026-10-26** (90-day cadence), or sooner on a material
legal settlement or inquiry outcome, a retention or ARR definition change,
an incident-related customer claim, a major product-quality event, or
disclosure of standalone Charlotte AI revenue/ARR/margin economics.
