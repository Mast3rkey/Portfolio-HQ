# CRM — Salesforce, Inc.

Last updated: 2026-07-28 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0030-ws0005-milestone3-batch8-enterprise-software-cybersecurity.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Salesforce Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 8, alongside `IBM`, `NOW`, `ORCL`,
`CRWD`, and `PANW` ("Enterprise Software and Cybersecurity"). `EQIX` and
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
this Claude session** -- see `CRM.yaml`'s `sources[]`.

## Business summary

Salesforce's platform thesis integrates CRM applications with Slack, Data
Cloud, MuleSoft, Tableau, and Agentforce. The annual filing explains how
Agentforce agents draw on Salesforce's own data, metadata, applications,
and MuleSoft APIs -- a genuinely integrated architecture, but one that is
also acquisition-assembled and therefore carries real integration,
competitive, and monetization risk that product-capability descriptions
alone do not resolve.

## Recurring-revenue quality

Salesforce reported fiscal-year-end 2026 remaining performance obligations
(RPO) of **$72.4 billion**, while explicitly warning that RPO is affected
by seasonality, renewal timing, contract terms, currency, new business, and
acquisitions -- including **approximately $2.2 billion tied to
Informatica**. Salesforce also disclosed an **approximately 8% attrition
rate** at 2026-01-31, excluding Slack self-service and current-year
acquisitions. Neither metric is directly comparable, without adjustment,
to Oracle's RPO, ServiceNow's renewal rate, CrowdStrike's ARR, or Palo Alto
Networks' NGS ARR.

## AI monetization -- Agentforce

This record's evidence base does not establish Agentforce's own standalone
revenue, usage, or gross-margin economics; the filing describes product
capability and integration architecture rather than disclosed AI-specific
financial results. Product-adoption narratives should not be conflated
with disclosed revenue and cash economics.

## Acquisition integration -- Informatica, Slack, Tableau, MuleSoft

The current product stack is acquisition-assembled. Informatica
specifically contributes roughly $2.2 billion of the fiscal-year-end 2026
RPO balance, and its integration milestones and return on acquisition
financing are not established in this record's evidence base. Acquisitions
can deepen the platform's moat when integration succeeds, but the
inspected sources do not themselves demonstrate that outcome.

## Capital allocation

Salesforce materially increased capital returns: **fiscal 2026 repurchases
were approximately $12.7 billion and dividends approximately $1.6
billion**, followed by a **$25 billion accelerated share repurchase (ASR)**
announced in March 2026. The ASR's final share count and effective
purchase price were not settled at initial delivery as of the inspected
Form 10-Q. Large buybacks compete with acquisitions, debt reduction, and
reinvestment; economic return depends on price paid and future per-share
cash generation.

## Competitors, substitutes, and shared drivers

Point-solution CRM, data, and collaboration vendors, along with AI-native
entrants, are Salesforce's primary named competitive set. See
`BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` for Salesforce's
position relative to the batch's other five companies and the batch-wide
metric-comparability caution.

## Disconfirming evidence

- Agentforce economics remain only partly disclosed at the claim level this
  record relies on.
- RPO is explicitly acquisition- and timing-sensitive, not a clean forward
  indicator, per Salesforce's own disclosure.
- Acquisition complexity (Slack, Tableau, MuleSoft, Informatica), debt, and
  very large capital returns create real opportunity cost and integration
  risk.

## Thesis-break conditions

A thesis-break condition would include failure to convert Agentforce and
Data Cloud adoption into durable growth while acquisition complexity, debt,
and capital returns consume cash without improving per-share economics.
Margin expansion and successful integration could offset slower top-line
growth, so this condition requires multi-period, not single-quarter,
evidence.

## Unresolved questions

- Agentforce standalone revenue, usage, and gross-margin economics.
- Informatica integration milestones and return on acquisition financing.
- Product-level retention and Slack self-service trends.
- Final accelerated-share-repurchase share count and effective price.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, Salesforce currently sits in the **band** tier (0.75%
target weight, 1.25x cap). CRM is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital priority and next-dollar considerations

**Business quality**, per the evidence above, shows a large, integrated
enterprise-software platform with meaningful disclosed recurring-revenue
scale and an aggressively deployed, currently active capital-return
program, tempered by an acquisition-assembled product stack whose newest
piece (Informatica) has unresolved integration economics.

**Capital priority is a separate question, and CRM's own current band
placement (0.75% target, 1.25x cap) -- shared with IBM, NOW, ORCL, CRWD, and
PANW in this batch -- is itself a data point this record preserves as
historical policy, not evidence.** Salesforce's distinct exposure within
this batch is its scale and the breadth of its acquisition-assembled
CRM/data/AI stack, a different mechanism from NOW's more organically-grown
single-platform model and from ORCL's infrastructure-capital-intensive
transition. **What would be lost if CRM were absent:** exposure to the
batch's largest, most acquisition-diversified enterprise-application
platform and its currently most aggressive capital-return program among the
non-Oracle software names.

**Factors that could support greater capital priority** include the scale
of disclosed RPO, the currently active and large capital-return program,
and Salesforce's demonstrated ability to integrate prior acquisitions
(Slack, Tableau, MuleSoft) into a functioning platform. **Factors favoring
an alternative use of capital** include the still-undisclosed Agentforce
economics, real integration risk from the newest and largest acquisition
(Informatica), and the general caution that very large buybacks do not by
themselves establish value creation absent favorable price and future
per-share cash generation. A reviewer preferring fully disclosed
AI-monetization evidence, or lower acquisition-integration risk, could
reasonably favor an alternative use of capital instead.

Business quality and portfolio capital priority are separate judgments.
This record does not determine the governed target: CRM's current band
tier and 0.75% target remain binding, this Intelligence record does not
change them, and a final next-dollar decision requires portfolio-wide
comparison and principal approval.

## Freshness and next-review requirements

Research cutoff: **2026-07-28**. Known unavailable material: Salesforce's
next quarterly results and any further Agentforce-specific KPI disclosure
were not available by the cutoff per the governing evidence bundle. Next
review due **2026-10-26** (90-day cadence), or sooner on Agentforce KPI
disclosure, an Informatica integration update, ASR completion, or attrition,
cRPO, or per-share cash-flow deterioration.
