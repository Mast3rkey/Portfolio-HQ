# AMD — Advanced Micro Devices, Inc.

Last updated: 2026-07-26 — created through AI-assisted research, pending
independent PR review and human approval under `PI-0025` (WS-0005 Milestone 3,
Batch 3).

## Source-access disclosure

WebFetch (direct primary-document retrieval) was attempted fresh this session
against SEC EDGAR and ir.amd.com URLs identified during research, plus a
non-target control domain — **all attempts returned HTTP 403**, consistent
with the tool/proxy-level block independently confirmed once for this entire
batch's research session (see `AVGO.md`'s Source-access disclosure for the
control-domain test, performed once and applicable across all four
companies researched in this session). **No primary document was directly
opened and inspected by this session at any point.** Every fact below is
WebSearch-sourced: either a primary document identified but not opened
(PRIMARY, NOT OPENED) or secondary journalism/analyst commentary (SECONDARY).

## Business summary

AMD is a fabless semiconductor designer spanning four reportable segments:
Data Center (server CPUs and AI accelerators), Client (consumer/commercial
PC CPUs), Gaming (discrete GPUs and semi-custom console silicon), and
Embedded (FPGA/adaptive SoC products, substantially built around the 2022
Xilinx acquisition) [S1, S2]. Q1 FY2026 (period ended 2026-03-28, reported
~2026-05-06) total revenue was $10.3B, with Data Center net revenue of
$5.8B, up 57% year-over-year from $3.7B in the prior-year period — driven,
per management commentary, by 5th-generation EPYC server CPUs and AMD
Instinct MI350-series GPUs [S1]. Q2 FY2026 guidance calls for revenue of
approximately $11.2B (+/- $300M) with non-GAAP gross margin around 56%,
Data Center and Embedded expected to grow double-digit sequentially, and
Client/Gaming expected only modest growth [S3] — **secondary-sourced
guidance figures, not independently verified against a primary guidance
disclosure this session opened.**

## Data-center CPUs, accelerators, and AI positioning

AI accelerators (the MI300-series family, including MI350) are reported at
approximately 73% of Data Center revenue in Q1 FY2026 — more than $4.2B in
the quarter [S1, secondary-derived percentage]. AMD's forward AI-accelerator
demand visibility rests substantially on two very large disclosed hyperscaler/
frontier-lab commitments: an October 2025 product purchase agreement with
OpenAI for 6 gigawatts of AMD GPUs deployed over time (first gigawatt powered
by MI450-series products), and a separately reported Meta plan to deploy up
to 6 gigawatts of AMD Instinct GPUs (first gigawatt powered by a custom
MI450-based GPU) [S4]. The MI450 series and its associated Helios rack-scale
platform are expected, per secondary reporting, to ramp more visibly only in
the second half of calendar 2026 — meaning a substantial share of the
OpenAI/Meta commitment scale had not yet translated into recognized revenue
as of the most recent quarter researched [S4].

## Competitive relationship with NVIDIA and Intel

AMD's Data Center segment ($5.8B in Q1 FY2026) remains an order of magnitude
smaller than NVIDIA's comparable quarterly data-center revenue (well
established in public reporting as tens of billions of dollars per quarter;
not independently re-derived from a primary NVIDIA disclosure in this
research pass, since NVIDIA is outside this batch's authorized scope). AMD
competes with Intel primarily in server and client CPUs — both companies
are covered in this same batch/repository (see `INTC.md`), and this record's
own INTC record documents Intel's Q2 2026 Client Computing Group and Data
Center/AI segment results as evidence that Intel remains an active
competitor in both of AMD's core CPU markets, not a company that has ceded
the field.

## Hyperscaler and enterprise demand

AMD's FY2025 Form 10-K is reported to disclose that **two customers each
individually represented more than 10% of consolidated revenue** in fiscal
2025 [S2]. Separately, secondary coverage names Microsoft, Dell,
Hewlett-Packard Enterprise, Lenovo, Sony, and unnamed hyperscale cloud
operators as significant customers [S2] — **this record does not conflate
that broader significant-customer list with the specific two >10%-of-revenue
customers**, whose identities were not confirmed in the secondary coverage
reviewed. This concentration sits alongside the OpenAI/Meta commitment
concentration in the AI-accelerator growth story specifically (see above) —
a structurally similar risk shape to Broadcom's and Marvell's AI-customer
concentration disclosed elsewhere in this batch, though AMD's disclosed base
of named significant customers is broader than either.

## Product-roadmap execution

Q1 FY2026's 57% YoY Data Center growth and the MI350-series contribution are
verified, already-realized results [S1]. The MI450/Helios platform's
second-half-2026 ramp, and the pace at which the OpenAI/Meta multi-gigawatt
commitments convert into recognized revenue, remain forward execution
dependencies rather than demonstrated results as of this research pass [S4].

## TSMC and advanced-packaging dependence

AMD's FY2025 Form 10-K reportedly discloses that AMD uses Taiwan
Semiconductor Manufacturing Company (TSMC) for wafer production of its HPC,
FPGA, and adaptive SoC products [S2] — the same foundry-concentration
exposure shared across this batch and this repository's existing TSM and
Batch 1 equipment-maker records. This repository's own TSM record
independently documents TSMC management's own statement that advanced-
packaging capacity is currently tight enough to constrain customer growth
industry-wide; this record treats that constraint as applicable to AMD's
advanced GPU/accelerator products by inference from TSMC's disclosed
capacity position, not from an AMD-specific primary disclosure this session
opened.

## Gaming and embedded cyclicality

At least one secondary source reports AMD guided consumer and gaming
revenue to *decline* in Q2 FY2026 over rising memory and component costs,
even as the company posted record Q1 FY2026 results driven by data-center
CPU demand [S3] — illustrating that AMD's non-Data-Center segments remain
exposed to ordinary component-cost and consumer-demand cyclicality
independent of the AI-accelerator growth story. Gaming revenue was $720M in
Q1 FY2026 (+11% YoY) [S1] — a comparatively small and more volatile revenue
line relative to Data Center. Embedded segment revenue was $3.5B for
full-year 2025 (down 3% YoY) but returned to growth in Q1 FY2026 at $873M
(+6% YoY) [S1, S2]; secondary reporting characterizes the Xilinx acquisition
as having "sat dormant for years" post-close before "finally clicking" in
2025-2026 [S4] — a characterization this record notes but does not adopt as
an established fact beyond the revenue figures themselves.

## Export controls and China exposure

In April 2025, new US export restrictions on certain semiconductors to
China led to approximately $800M in inventory and related charges on AMD
Instinct MI308 Data Center GPU products in AMD's fiscal Q2 2025 [S5]. AMD
separately estimated a cumulative $1.5-1.8B revenue impact for calendar/
fiscal 2025 tied to the restrictions, concentrated in Q2 and Q3 [S5]. AMD
has since been granted some export licenses permitting MI308 shipments to
certain China-based customers, but reported recording **no** MI308
China-based-customer revenue during the quarter ended 2025-09-27 [S5] —
indicating the license grant had not yet translated into recognized revenue
as of that filing. Separately, AMD's CEO is reported to have stated China
still represents approximately 20% of AMD's overall revenue despite the
accelerator-specific export controls [S5], implying the restriction's
effect is concentrated in the AI-accelerator product line specifically
rather than uniform across AMD's business.

## Customer and ecosystem concentration

See "Hyperscaler and enterprise demand" above for the >10%-of-revenue
customer disclosure, and "Data-center CPUs, accelerators, and AI
positioning" for the OpenAI/Meta commitment concentration specific to the
AI-accelerator growth story. Both mechanisms are recorded as distinct
concentration risks, not merged into one figure.

## Margin-relevant execution, drawdown, supply-chain, and gap risks

*(Factual, advisory only — no leverage, deployment-timing, or margin-ceiling
recommendation.)* AMD's balance sheet is comparatively strong within this
batch: cash, cash equivalents, and short-term investments were $12.3B as of
2026-03-28 (up from $10.6B as of 2025-12-27), against aggregate short- and
long-term debt obligations of just $3.3B [S1] — a materially lighter debt
load than either Broadcom's reported $62.655B or Marvell's reported senior
notes obligations disclosed elsewhere in this batch. This lighter leverage
profile is a meaningful margin-relevant differentiator: a company with less
debt has less refinancing/interest-coverage risk in a downturn, all else
equal. **Correlated-loss mechanisms:** AMD shares the same AI-capex-cycle
exposure as AVGO and MRVL in this batch — a simultaneous hyperscaler
pullback (particularly by OpenAI or Meta, AMD's two named multi-gigawatt
commitment partners) would hit AMD's fastest-growing segment directly. AMD
also shares TSMC/advanced-packaging supply concentration with every other
fabless company in this batch and repository. **Gap risk:** the
China-export-control impact (a quantified $800M one-time charge plus an
estimated $1.5-1.8B cumulative 2025 revenue hit) demonstrates that a single
regulatory action can produce a sudden, discrete earnings impact rather than
a gradual one — a gap-risk pattern this record flags as realized, not
hypothetical.

## What exposure would be lost if AMD were absent from the portfolio

*(Research analysis only — this section does not recommend any allocation
action.)* AMD provides the portfolio's most diversified single-company
exposure to CPU, GPU/accelerator, gaming, and embedded/FPGA product
categories simultaneously. NVDA (also held) provides GPU/AI-accelerator
exposure without AMD's CPU or embedded diversification; INTC (also held, see
`INTC.md`) provides CPU exposure with a foundry-strategy dimension AMD
lacks. This record does not establish a precise quantitative overlap measure
between AMD and either NVDA or INTC — that determination is deferred to any
future, separately-authorized relationship-mapping work (WS-0005 Milestone
4, not yet authorized).

## Current governed tier and target (existing policy, not research evidence)

`targets.yaml` currently places AMD in the **band tier** (0.75% target, cap
1.25×, RSI-gated trim rule) and in the `semis` correlated-cluster cap (≤25%
of book). **This is preserved here as historical, currently-governed policy
only, per `OPS-0006` §2/§3's zero-based research discipline — it is not
evidence supporting, and was not used to derive, this record's conviction
rating, role, or any other research conclusion above.**

## Review framework

- Cadence: 90 days, matching every other Batch 1/2/3 first-coverage record
  in this repository.
- Unscheduled-review triggers: a material change in Data Center/AI-accelerator
  guidance; a disclosed development in the OpenAI or Meta multi-gigawatt
  commitment (deployment milestone reached, delayed, or renegotiated); a
  material change in China export-control policy or a new quantified revenue
  impact; a material change in the >10%-of-revenue customer disclosure; a
  significant MI450/Helios ramp update (on-track, delayed, or ahead of plan).
- Metrics worth monitoring each review: quarterly Data Center revenue and AI-
  accelerator share of it, cash/debt balance, Gaming/Client segment trend
  relative to guidance, and any newly-disclosed named-customer concentration
  percentage.

## Conviction

**Rating: Medium**

**Rationale:** see the YAML `conviction.rationale` field — reproduced there
in full to avoid duplication drift between the two files.

This rating and rationale reflect AI-assisted research pending the
independent PR review and human approval this repository's first-coverage
discipline requires before this record is treated as finalized.

## Portfolio role reference

`portfolio_role_ref: band` reflects `targets.yaml`'s current tier placement,
recorded here descriptively per PI-0003's unchanged doctrine — this field is
a human-authored reference fixed at authoring time, not an allocator input,
and does not itself authorize or derive any allocation behavior. Recording
it here does not modify or reaffirm allocator policy; `targets.yaml` remains
the sole authority for actual tier weights and allocation.

## Theme membership

None. This record does not assign AMD to any Theme Intelligence theme.
`PI-0025` does not authorize a theme-membership determination for any
company in this batch, and no such determination is made here — consistent
with Batch 1 (ASML/AMAT/KLAC/LRCX) and Batch 2 (MU/SKHY), neither of which
received a theme assignment either.

## Sources

- [S1] AMD Q1 2026 Financial Results press release/earnings materials (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results, 2026-05-06
- [S2] AMD FY2025 Form 10-K (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm, 2026-02-04
- [S3] SECONDARY, Q2 FY2026 guidance commentary (Tom's Hardware and overlapping outlets), 2026-07-26
- [S4] SECONDARY, multiple overlapping outlets covering the AMD-OpenAI and AMD-Meta product purchase agreements, 2026-07-26
- [S5] SECONDARY, multiple overlapping outlets covering the April 2025 export-control impact (Astute Group, qz.com, cryptobriefing.com), 2026-07-26
