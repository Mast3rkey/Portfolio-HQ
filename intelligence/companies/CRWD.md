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
unresolved in the inspected sources. **This record does not, and cannot,
quantify an ultimate liability** -- doing so would exceed what the filings
themselves establish.

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
an incident-related customer claim, or a major product-quality event.
