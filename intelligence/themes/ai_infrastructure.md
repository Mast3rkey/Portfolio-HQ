# Theme: AI Infrastructure

Last updated: 2026-07-18 -- created through AI-assisted research and
drafting, finalized through explicit human review and approval under
PI-0007. Portfolio HQ's first Theme Intelligence record, authorized by
decision_log.yaml's PI-0006 (data-model freeze) and PI-0007 (bounded
pilot authorization).

## Source-access disclosure

Every direct-fetch attempt against the primary documents cited below
(SEC EDGAR, `gevernova.com`, `eia.gov`, and Microsoft's own investor
pages) returned HTTP 403 in the research environment, consistent with
the access pattern already disclosed in COST's and XOM's records. No
figure in this record was rendered directly by this repository's
research tooling. Every figure is user-inspected against the cited
primary document and independently corroborated via multiple search
results in the same research pass, including direct identification of
each primary document's URL. This caveat applies once, to the whole
record, and is not repeated per figure below.

## Description

The buildout of physical infrastructure -- compute hardware and
electrical power -- required to run large-scale AI workloads. Two
coupled but distinct demand drivers:

1. **Compute**: accelerated-computing hardware for AI training and
   inference.
2. **Power**: the electricity generation, transmission, and
   grid-connection capacity needed to power the data centers that
   hardware runs in.

This theme is deliberately framed as "compute hardware + electrical
infrastructure" rather than simply "AI," so that it can later include
additional companies without changing its identity -- a company can be
material to this theme through either driver, or both.

## Evidence

- NVIDIA's fiscal year 2026 (ended 2026-01-25) total revenue was
  $215.938 billion, up 65% year-over-year; Data Center segment revenue
  was $193.7 billion, up 68% year-over-year.
- GE Vernova's fiscal year 2025 orders were $59.3 billion (+34%
  organic); total backlog reached $150 billion (+$31.2 billion
  year-over-year); revenue was $38.1 billion; net income was $4.9
  billion, including a $2.9 billion tax benefit.
- GE Vernova's Electrification segment booked $2.4 billion in
  equipment orders supporting data centers in Q1 2026 alone -- more
  than all of 2025 combined -- and total company backlog grew more
  than $13 billion quarter-over-quarter, to $163 billion.
- The U.S. Energy Information Administration's Annual Energy Outlook
  2026 (released 2026-04-08) projects data-center-server electricity
  consumption reaching between 446 and 818 billion kilowatt-hours by
  2050; the 818 billion kWh figure is the High Electricity Demand
  case, more than 16 times the 2020 level.
- Microsoft's own FY2026 Q3 earnings call (CFO Amy Hood, 2026-04-29)
  guided approximately $190 billion of calendar-2026 capital
  expenditures, with approximately $25 billion of that attributed to
  higher component pricing.

**Interpretation, separated from the facts above:** these figures,
taken together, are consistent with a real, large-scale capital cycle
spanning both compute and power infrastructure. This is an observation
about the pattern across independently corroborated figures -- it is
not a forecast that the cycle continues, and it is not a valuation or
allocation judgment.

### Hyperscaler aggregate -- supporting context only, not evidentiary

Analyst compilations estimate combined 2026 AI-capex across Amazon,
Alphabet, Meta, and Microsoft in the range of roughly $690-770 billion.
This aggregate combines mixed-source inputs -- Microsoft's component is
user-inspected and independently corroborated (see above); Amazon's,
Alphabet's, and Meta's remain secondary-only, not independently
confirmed against each company's own primary disclosure. **This
aggregate is not relied upon to establish this theme and not relied
upon for the lifecycle recommendation below.** It is included only as
directional market context.

## Risks

- Demand concentration in a small number of hyperscaler customers.
- Long-cycle power-infrastructure execution risk.
- Export-control and geopolitical policy risk on the compute side.
- Guidance figures (Microsoft's capex guidance, the hyperscaler
  aggregate) are revisable estimates, not commitments -- this applies
  less to the realized-results figures above (NVIDIA's and GE
  Vernova's reported revenue, orders, and backlog), which describe
  what already happened, not what's guided to happen.

## Catalysts

- Continued or decelerating hyperscaler capex guidance disclosed
  quarterly.
- GE Vernova's backlog-to-revenue conversion pace, including
  management's stated target of approximately $200 billion of total
  backlog by year-end 2028. (This target predates, and was not
  accelerated by, the Q1 2026 results, which reported total backlog of
  $163 billion and more than $13 billion of sequential growth.)
- NVIDIA's next-generation architecture execution.

No other future date is asserted for any catalyst above beyond what is
cited.

## Non-membership

Membership in this theme requires that AI infrastructure -- compute
hardware or electrical power supporting AI workloads -- is a
**material driver of the company's business**, evidenced by disclosed
revenue, backlog, or segment results. It is not sufficient that a
company merely uses AI internally, sells software that incorporates
AI, or has been mentioned in AI-infrastructure commentary without a
corresponding disclosed financial connection. This is a standard for
future reviewers evaluating additional companies against this theme --
it is not a claim about any company beyond NVDA and GEV.

## Future-proofing note

**Theme membership does not imply comparable business models, risk
profiles, conviction ratings, or allocation treatment.** NVDA and GEV
are grouped here because both disclose a material, evidenced
connection to the same infrastructure buildout -- not because they are
similar businesses, carry similar risk, or should be sized similarly.
This restates PI-0006's own separation between narrative grouping
(this theme) and allocator mechanics (`targets.yaml`'s tiers and
cluster caps), which remain entirely independent of this record.

## One-way authority

This theme record does not store, list, or imply its member companies.
Authority runs one way only: a company's own record references this
theme via its `themes:` field; this file never references any company
back. Any nested or graph-like presentation of theme/company
relationships is a future generated reporting view computed by reading
company files at report time -- never a stored data structure in this
file, per PI-0006.

## Lifecycle

**Established.**

Rationale, anchored to maturity indicators rather than today's dollar
figures:

- **Multiple independent companies**: NVIDIA (compute) and GE Vernova
  (power) are unrelated businesses, both reporting activity tied to
  this theme.
- **Multiple independent industries**: semiconductor/compute hardware
  and heavy electrical/power equipment are structurally distinct
  industries, with different customers, supply chains, and regulatory
  exposure.
- **Demonstrated commercial deployment**: the evidence above is
  realized-results -- reported revenue, booked orders, and backlog --
  not projections or announced intentions.
- **Recurring disclosure across reporting periods**: both companies
  have reported AI-infrastructure-linked results across multiple
  consecutive periods (NVIDIA's FY2026 results; GE Vernova's FY2025
  results and Q1 2026 update), a sustained pattern rather than a
  single event.

An Archived theme is not deleted and remains a valid reference target
for any company that once pointed at it -- referential integrity does
not require an active lifecycle state, preserving historical memory.

## Review framework

- **Cadence: 90 days.** Matches the cadence used for COST and XOM.
- **Unscheduled-review triggers**: a material change in either
  company's disclosed AI-infrastructure-linked revenue/backlog trend;
  a material shift in hyperscaler capex guidance; a material change in
  EIA's demand projections upon the next Annual Energy Outlook
  release; any development that would materially change the
  Non-membership standard's application.

## Sources

1. NVIDIA, "NVIDIA Announces Financial Results for Fourth Quarter and
   Fiscal 2026," 2026-02-25 --
   https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026
2. GE Vernova, Q1 2026 results, Form 8-K exhibit, 2026-04-22 --
   https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000063/gevpressrelease1q26.htm
3. GE Vernova, Q4/FY2025 results press release --
   https://www.gevernova.com/news/press-releases/ge-vernova-reports-fourth-quarter-full-year-2025-financial-results
4. GE Vernova, FY2025 Form 10-K --
   https://www.sec.gov/Archives/edgar/data/1996810/000199681026000015/gev-20251231.htm
5. EIA, Annual Energy Outlook 2026 press release, 2026-04-08 --
   https://www.eia.gov/pressroom/releases/press587.php
6. EIA, "Data center server energy use grows across the commercial
   building stock" --
   https://www.eia.gov/todayinenergy/detail.php?id=67704
7. Microsoft, FY2026 Q3 earnings call (CFO Amy Hood), 2026-04-29 --
   https://www.microsoft.com/en-us/investor/events/fy-2026/
8. Hyperscaler aggregate capex compilations -- supporting context only,
   not evidentiary; not independently confirmed against each
   constituent company's own primary disclosure in this research pass.

## Approval record

All theme-level content above (narrative description, evidence, risks,
catalysts, lifecycle value, review cadence) was presented in the
PI-0007 Human Approval Packet and explicitly approved by the human
principal on 2026-07-18, item-by-item, prior to this file's creation.
