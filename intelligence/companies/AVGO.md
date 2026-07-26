# AVGO — Broadcom Inc.

Last updated: 2026-07-26 — created through AI-assisted research, pending
independent PR review and human approval under `PI-0025` (WS-0005 Milestone 3,
Batch 3).

## Source-access disclosure

WebFetch (direct primary-document retrieval) was attempted fresh this session
against four distinct URLs: the Q2 FY2026 earnings-release PDF hosted at
investors.broadcom.com, the SEC EDGAR browse-company page, a stocktitan.net
secondary-filing-summary page, and a non-target control domain
(example.com). **All four attempts returned HTTP 403** — including the
control domain, indicating a tool/proxy-level block for this session rather
than a Broadcom- or SEC-specific block. This is consistent with, but was
independently re-verified rather than merely assumed from, Batch 1's and
Batch 2's own disclosed identical experience. **No primary document was
directly opened and inspected by this session at any point.** Every fact
below is WebSearch-sourced: either a primary document identified but not
opened (labeled PRIMARY, NOT OPENED below and in the YAML `sources` list) or
secondary journalism/analyst/aggregator commentary about one (labeled
SECONDARY). Claims are further separated by fact/inference/uncertainty where
that distinction matters, and unresolved figures are flagged as such rather
than silently reconciled.

## Business summary

Broadcom operates two reportable segments: **Semiconductor Solutions**
(custom AI accelerators/XPUs, networking silicon, broadband, storage,
wireless, and other semiconductor products) and **Infrastructure Software**
(built substantially around the 2023 VMware acquisition, now centered on the
VMware Cloud Foundation subscription platform) [S1, S2]. Q2 FY2026
(period ended ~2026-05-03, reported ~2026-06-05) consolidated revenue was
$22.2B, up 48% year-over-year and reported as a record; Semiconductor
Solutions contributed $15.1B and Infrastructure Software $7.18B (+9% YoY)
[S1]. Consolidated non-GAAP operating margin reached ~67%, also reported as a
record [S1].

AI semiconductor revenue specifically — the fastest-growing and most
closely-watched line — was $10.8B in Q2 FY2026, up 143% year-over-year [S1].
Q3 FY2026 guidance calls for consolidated revenue of ~$29.4B (+84% YoY), AI
semiconductor revenue of ~$16B (+200%+ YoY), and infrastructure software
revenue of ~$8.9B (+31% YoY) [S1]. Management's full-year FY2026 AI
semiconductor guidance is ~$56B (+~180% YoY versus FY2025), and management
has reaffirmed an FY2027 AI-semiconductor target exceeding $100B, stated to
be backed by a ~$73B committed customer backlog including a Google TPU
supply agreement running through 2031 [S3]. **The backlog figure and the
Google-through-2031 detail are secondary-sourced (aggregated analyst/trade
coverage) and were not independently verified against a primary contract or
filing disclosure this session opened** — they are presented as reported,
not as independently confirmed facts.

## Semiconductor Solutions versus Infrastructure Software economics

Unlike AMD, MRVL, and INTC in this batch — all of which derive revenue
almost entirely from semiconductor product sales — Broadcom's Infrastructure
Software segment ($7.18B in Q2 FY2026, +9% YoY) [S1] is a materially
different economic model: recurring subscription revenue built around
VMware Cloud Foundation (VCF), reported to have moved substantially away
from legacy perpetual licensing [S2, S6]. Secondary reporting states that
**more than 87% of Broadcom's largest 10,000 customers have migrated to the
VCF subscription model**, characterized by management/analyst commentary as
driving double-digit annual-recurring-revenue (ARR) growth [S2]. This
software-revenue base is structurally more defensive against
semiconductor-cycle downturns than Broadcom's chip business, but it carries
its own distinct risk (see VMware integration/customer-relations risk
below) that a pure semiconductor company would not have.

## Custom AI accelerator and networking exposure

Broadcom's custom AI accelerator (XPU) design-services business is reported
as market-leading: at least one secondary source places Broadcom's share of
this specific market at 70%+, up from a previously-cited 60-80% range
attributed to Bloomberg Intelligence [S3]. The reported customer roster —
Google, Meta, OpenAI, Anthropic, and Apple — is named across multiple
overlapping secondary sources, with at least one source characterizing the
group as "six major customers" without naming a sixth [S3]. **This record
does not adopt an unnamed sixth customer as a confirmed fact.** Reported
deployment scale is large: OpenAI's first-generation custom accelerator is
targeted at more than 1 gigawatt of compute capacity in 2027; Anthropic is
running roughly 1 gigawatt of Google TPU compute in 2026 (a Google
relationship in which Broadcom's role is TPU co-design/production partner,
not a direct Anthropic relationship — this distinction is preserved, not
collapsed), reportedly growing to more than 3 gigawatts in 2027 [S3].

## Hyperscaler and customer concentration

The reported customer roster above (Google, Meta, OpenAI, Anthropic, Apple,
and a possible unnamed sixth) is small relative to the scale of AI-segment
revenue it drives. At least one secondary source explicitly characterizes
this concentration as "the largest single risk" to Broadcom's AI growth
trajectory [S3]. Separately, at a company-wide (not AI-specific) level,
Broadcom's FY2025 Form 10-K is reported to disclose that distributors
represent 48% of net revenue and approximately 40% of net revenue derives
from the company's top five end customers [S2] — a different, broader
concentration measure than the AI-specific customer list, and this record
does not conflate the two.

## VMware integration, debt, deleveraging, and recurring-software economics

Broadcom's VMware acquisition (closed November 2023, ~$69B total
consideration per secondary sourcing) transformed the company's revenue mix
toward recurring software [S2]. The migration to VCF subscription licensing
is reported at >87% of the largest 10,000 customers [S2], but the same body
of secondary reporting documents **customer backlash over reported 5x-10x
list-price increases** for some enterprise customers under the new bundled
model, with at least one analyst source flagging elevated customer-churn
risk over a 12-18 month forward window [S6]. **This record does not resolve
whether the ARR-growth framing or the churn-risk framing will dominate** —
both come from secondary/analyst sources, and no primary disclosure
reconciling migration economics against realized or expected churn was
located.

On the balance-sheet side: S&P is reported to have affirmed/assigned an
"A-" long-term issuer/senior-unsecured rating with a positive outlook, and
Fitch rated Broadcom's notes "BBB+", with at least one source explicitly
tying the Fitch action to AI-semiconductor opportunity [S4]. Long-term debt
and capital-lease obligations were reported at $62.655B as of Q2 FY2026,
with debt-to-EBITDA reported at 1.24x (52% below a cited 10-year median of
2.60x) and trailing free cash flow reported at $27B [S5]. **These figures
are secondary-sourced (financial-data aggregator synthesis) and were not
independently verified against primary filing text this session opened.**

## Acquisition dependence and integration risk

Broadcom's current scale — both its semiconductor breadth and its software
segment specifically — was built substantially through acquisition, most
recently VMware [S2]. Secondary coverage characterizes Broadcom's own
FY2025 10-K narrative as describing "a history of innovation that has
evolved through acquisitions" [S2]. This is treated in this record as a
structural characteristic of Broadcom's business model — continued growth
via further large acquisitions, and the associated integration, debt, and
cultural-integration risk that comes with them, is a reasonably foreseeable
future path — not as a one-time, already-resolved event. No specific future
acquisition target was identified in this research pass.

## Foundry and advanced-packaging dependencies

As a company producing both merchant semiconductor products and custom AI
silicon, Broadcom depends on external foundry and advanced-packaging
capacity. Industry-wide reporting places TSMC as the dominant advanced-node
and advanced-packaging supplier to the AI-accelerator industry broadly, and
this repository's own TSM Company Intelligence record independently
documents TSMC management's own statement that advanced-packaging capacity
is currently tight enough to constrain customer growth industry-wide. **No
Broadcom-specific, named-foundry-percentage disclosure was located in this
research pass** — the dependency is inferred from Broadcom's role as a
fabless/hybrid semiconductor company and industry-wide foundry
concentration, not confirmed against a Broadcom-specific primary source.

## Semiconductor cyclicality and export-control exposure

Broadcom's non-AI semiconductor businesses (broadband, traditional
enterprise storage, and other legacy product lines) remain subject to
ordinary semiconductor-industry cyclicality even as the AI segment grows
rapidly; analysts at Goldman Sachs and JPMorgan are reported to characterize
Broadcom's recurring software revenue as an "underappreciated" cushion
against that cyclicality [S6] — a characterization this record notes but
does not independently verify.

China exposure compounds across three distinct, separately-sourced vectors,
which this record treats as three separate risk mechanisms rather than one
risk restated three times: (1) approximately 20% of Broadcom's revenue is
reported as China-derived [S6]; (2) the US tightened its export-control
review standard for advanced AI chips to China effective 2026-01-15, moving
from a general policy posture toward case-by-case licensing review [S6]
(the exact regulatory mechanism was not independently verified against a
primary Federal Register or BIS document); and (3) in a distinct action
unrelated to US export controls, China is reported to have banned use of
VMware's cybersecurity software in January 2026 citing national-security
grounds — a direct hit to Broadcom's Infrastructure Software segment inside
China specifically, separate from any semiconductor-export mechanism [S6].

## Margin-relevant balance-sheet, gap-risk, and correlated-loss evidence

*(Factual, advisory only — no leverage, deployment-timing, or margin-ceiling
recommendation.)* Broadcom's reported credit-rating trajectory (A-/BBB+,
positive outlooks) and reported sub-1.5x debt-to-EBITDA are, if accurate,
evidence of balance-sheet resilience relative to a company with a more
strained capital structure [S4, S5] — but these figures are
secondary-sourced and unverified against primary filing text. Broadcom's
AI-segment revenue concentration in a small number of named hyperscaler/
frontier-lab customers is a **correlated-loss mechanism**: a simultaneous
pullback in AI capital expenditure by two or more of Google, Meta, OpenAI,
and Anthropic would likely affect Broadcom's fastest-growing, highest-margin
revenue line all at once, not gradually across a diversified customer base.
The VMware customer-churn risk (5x-10x price increases, disputed migration
economics) represents a second, largely independent potential revenue-shock
mechanism specific to the software segment, uncorrelated with a
semiconductor-cycle or AI-capex-cycle downturn — meaning Broadcom's two
segments do not necessarily share the same drawdown trigger, a
diversification benefit worth noting even though this record draws no
capital-allocation conclusion from it. Broadcom's compounding China exposure
(three distinct vectors, above) represents a geopolitical gap-risk pathway
that could affect both segments simultaneously if realized as an escalation
rather than a contained, single-product action (as the VMware China ban
appears to be so far).

## What exposure would be lost if AVGO were absent from the portfolio

*(Research analysis only — this section does not recommend any allocation
action.)* Broadcom is currently the portfolio's only holding combining
custom AI-accelerator/networking-silicon exposure with a large recurring
enterprise-software revenue base. NVDA (also held) provides AI-accelerator
exposure through merchant GPUs rather than custom ASIC design services —
a different position in the AI-compute value chain (merchant-silicon
platform versus fabless customer-specific ASIC design partner). This record
does not establish the degree to which NVDA's and AVGO's AI-related economic
exposure overlaps or diverges beyond that structural distinction; that
determination is deferred to any future, separately-authorized relationship-
mapping work (WS-0005 Milestone 4, not yet authorized).

## Current governed tier and target (existing policy, not research evidence)

`targets.yaml` currently places AVGO in the **T2 tier** (1.65% target),
subject to the T1/T2 mechanical concentration ceiling
(`gates.t1t2_trim_mult`, 1.5×, no RSI gate) rather than the `band` tier's
1.25× cap/RSI-gated trim, and in the `semis` correlated-cluster cap (≤25% of
book). **This is preserved here as historical, currently-governed policy
only, per `OPS-0006` §2/§3's zero-based research discipline — it is not
evidence supporting, and was not used to derive, this record's conviction
rating, role, or any other research conclusion above.**

## Review framework

- Cadence: 90 days, matching every other Batch 1/2/3 first-coverage record
  in this repository.
- Unscheduled-review triggers: a material change in disclosed AI-semiconductor
  guidance (up or down) at a subsequent earnings release; a named-customer
  loss or addition among the Google/Meta/OpenAI/Anthropic/Apple XPU roster;
  a material development in the VMware customer-churn question (either a
  disclosed churn figure or a material price-policy reversal); a credit-
  rating change; a material China-regulatory or US-export-control escalation
  affecting either segment; a large new acquisition announcement.
- Metrics worth monitoring each review: quarterly AI-semiconductor revenue
  and guidance cadence, Infrastructure Software ARR/VCF-migration commentary,
  debt-to-EBITDA and credit-rating actions, and any disclosed AI-customer
  concentration percentage (not located in this research pass).

## Conviction

**Rating: High**

**Rationale:** see the YAML `conviction.rationale` field — reproduced there
in full to avoid duplication drift between the two files.

This rating and rationale reflect AI-assisted research pending the
independent PR review and human approval this repository's first-coverage
discipline requires before this record is treated as finalized.

## Portfolio role reference

`portfolio_role_ref: T2` reflects `targets.yaml`'s current tier placement,
recorded here descriptively per PI-0003's unchanged doctrine — this field is
a human-authored reference fixed at authoring time, not an allocator input,
and does not itself authorize or derive any allocation behavior. Recording
it here does not modify or reaffirm allocator policy; `targets.yaml` remains
the sole authority for actual tier weights and allocation.

## Theme membership

None. This record does not assign AVGO to any Theme Intelligence theme.
`PI-0025` does not authorize a theme-membership determination for any
company in this batch, and no such determination is made here — consistent
with Batch 1 (ASML/AMAT/KLAC/LRCX) and Batch 2 (MU/SKHY), neither of which
received a theme assignment either.

## Sources

- [S1] Broadcom Inc., Second Quarter Fiscal Year 2026 earnings release (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://investors.broadcom.com/node/64371/pdf, ~2026-06-05
- [S2] Broadcom Inc. FY2025 Form 10-K, per SEC-filing-summary secondary coverage (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://www.stocktitan.net/sec-filings/AVGO/10-k-broadcom-inc-files-annual-report-1cab62b51a6e.html, ~2025-12-01
- [S3] SECONDARY, aggregated custom-AI-accelerator industry coverage (multiple partially-overlapping outlets, not independently reconciled to a single source), 2026-07-26
- [S4] SECONDARY, rating-agency press coverage (S&P Global Ratings / Fitch Ratings, aggregator-relayed), 2026-07-26
- [S5] SECONDARY, financial-data aggregator synthesis (gurufocus.com / ycharts.com / macrotrends.net-style sourcing), 2026-07-26
- [S6] SECONDARY, multiple overlapping financial-news outlets covering export-control tightening, VMware's China ban, and VCF pricing/churn commentary, 2026-07-26
