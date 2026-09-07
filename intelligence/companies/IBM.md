# IBM — International Business Machines Corporation

Last updated: 2026-07-28 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0030-ws0005-milestone3-batch8-enterprise-software-cybersecurity.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior IBM Company Intelligence record existed). Portfolio HQ's
WS-0005 Milestone 3 Batch 8, alongside `NOW`, `CRM`, `ORCL`, `CRWD`, and `PANW`
("Enterprise Software and Cybersecurity"). `EQIX` and `UNH` are not part of
this batch and remain uncovered and unauthorized.

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
this Claude session** -- see `IBM.yaml`'s `sources[]`.

## Business summary

IBM operates a heterogeneous, four-segment portfolio -- Software,
Consulting, Infrastructure, and Financing -- pursuing a stated strategy of
hybrid cloud and AI combined with enterprise incumbency and partner
distribution. This is not a pure software-subscription business: the
segment mix means aggregate metrics can conceal materially different
underlying economics, and mainframe-style switching costs should not be
generalized to Consulting or the broader Software portfolio.

## Preliminary second-quarter 2026 execution -- mixed, not final

On 2026-07-14, IBM furnished (not filed as final) selected preliminary
second-quarter 2026 results: **total revenue up 1%, Software up 5%,
Consulting flat, and Infrastructure down 7%**, with management's own
disclaimer that the close was not final and results could differ. This is
genuinely mixed execution evidence, not a uniform acceleration or a stalled
turnaround -- Software growth alongside Infrastructure contraction in the
same preliminary period. The final Q2 2026 Form 10-Q was not available at
this record's 2026-07-28 evidence cutoff.

## Moat and competitive position

IBM's own Form 10-K describes differentiation through breadth, expertise,
integration capability, mission-critical systems, and trust, while in the
same filing naming extensive competition and material open-source
dependence. Durability varies by segment and product cycle: hyperscalers,
global consultancies, and open-source alternatives constrain the moat's
reach outside IBM's most entrenched systems (e.g. mainframe/zSystems).

## Capital allocation

IBM suspended its common-stock repurchase program at the 2019 Red Hat
closing; the 2025 Form 10-K still showed unused authorization, indicating
dividends, debt management, and acquisitions have held capital-allocation
priority over active repurchases since that closing. Unused authorization
preserves optionality but is not itself a commitment to resume repurchases.

## AI monetization -- watsonx

This record's evidence base does not establish watsonx's current revenue,
margin, or retention contribution specifically; the preliminary Q2 2026
letter reports segment-level trends (Software +5%) without isolating AI
"book of business" economics at the claim level this record relies on. This
is a disclosed evidence gap, not a finding that watsonx lacks traction.

## Mainframe (zSystems) durability

This record's evidence base does not establish the current zSystems cycle
position or renewal economics specifically -- a disclosed unresolved
question, not a finding of weakness or strength.

## Competitors, substitutes, and shared drivers

IBM's own filing names hundreds of competitors across its four segments,
plus hyperscalers and global consultancies as constraints on its Consulting
and Infrastructure moat specifically. See
`BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` for IBM's distinct
position relative to the batch's other five companies.

## Disconfirming evidence

- Preliminary Q2 2026 segment performance was mixed, with Infrastructure
  down 7% in the same period Software grew 5%.
- Client-budget conditions, innovation-execution risk, open-source
  alternatives, and Consulting-intensity all challenge a simple
  hybrid-cloud-and-AI acceleration narrative.
- The final Q2 2026 Form 10-Q, watsonx's own revenue/margin/retention
  contribution, the current zSystems cycle, and IBM's post-Q2 debt/pension
  position are all unresolved as of this record's cutoff.

## Thesis-break conditions

A thesis-break condition would include sustained Software and
Infrastructure underperformance combined with failure to convert AI demand
into durable revenue and free cash flow, especially if Consulting cannot
offset segment weakness. A single weak quarter or a normal mainframe-cycle
trough would not, on its own, establish this condition.

## Unresolved questions

- Final second-quarter 2026 Form 10-Q and final segment results (the
  preliminary 2026-07-14 letter is not a substitute).
- Current watsonx revenue, margin, and retention contribution.
- Current zSystems cycle and renewal economics.
- Updated debt and pension position after the second-quarter close.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, IBM currently sits in the **band** tier (0.75% target
weight, 1.25x cap). IBM is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital priority and next-dollar considerations

**Business quality**, per the evidence above, shows a diversified,
century-scale enterprise franchise with real current AI (watsonx) and
hybrid-cloud (Red Hat) strategic positioning, disciplined capital allocation
since 2019 (suspended buybacks, prioritized dividends/debt management), and
genuine — if uneven — current execution (Software +5% preliminary Q2 2026).

**Capital priority is a separate question, and IBM's own current band
placement (0.75% target, 1.25x cap) -- shared with NOW, CRM, ORCL, CRWD, and
PANW in this batch -- is itself a data point this record preserves as
historical policy, not evidence.** IBM's distinct exposure within this batch
is the only diversified infrastructure/consulting/hybrid-cloud incumbent --
a materially different mechanism from the batch's five more purely
software-or-platform-centered peers, and the only company whose Consulting
segment mix and services intensity make simple SaaS-style metric comparisons
(ARR, NGS ARR, RPO, renewal, attrition) inapplicable in the first place.
**What would be lost if IBM were absent:** exposure to a differently
structured enterprise-technology economic function -- consulting/services
and infrastructure/hardware alongside software -- that none of NOW, CRM,
ORCL, CRWD, or PANW replicates, plus IBM's demonstrated century-scale
capital-allocation discipline through multiple technology cycles.

**Factors that could support greater capital priority** include IBM's
demonstrated multi-decade capital discipline, real current AI/hybrid-cloud
strategic execution, and the genuinely distinct (non-duplicative) economic
exposure it adds to this batch. **Factors favoring an alternative use of
capital** include the mixed, preliminary (not yet finalized) nature of the
most recent segment results, the batch's own required caution that IBM is
"not a pure software-subscription company" (making growth-multiple-style
comparisons with NOW/CRM/CRWD/PANW inappropriate), and the unresolved
watsonx-monetization and zSystems-cycle questions this record's evidence
base does not settle. A reviewer weighting demonstrated, fully disclosed
recurring-revenue metrics (as NOW's 98% renewal rate or CRWD's ARR growth
provide) more heavily than a diversified, partially-services-based model
could reasonably favor one of those peers instead.

Business quality and portfolio capital priority are separate judgments.
This record does not determine the governed target: IBM's current band tier
and 0.75% target remain binding, this Intelligence record does not change
them, and a final next-dollar decision requires portfolio-wide comparison
and principal approval.

## Freshness and next-review requirements

Research cutoff: **2026-07-28**. Known unavailable material: IBM's final
Q2 2026 Form 10-Q was not available by the cutoff per the governing evidence
bundle -- only the preliminary, furnished 2026-07-14 investor letter was
inspected. Next review due **2026-10-26** (90-day cadence), or sooner on
publication of the final Q2 2026 Form 10-Q, new mainframe-cycle disclosures,
a material AI-book monetization update, or an acquisition or capital-return
policy change.
