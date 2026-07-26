# ETN — Eaton Corporation plc

Last updated: 2026-07-26 -- record created through AI-assisted research
and drafting under `governance/decisions/PI-0026-ws0005-milestone3-batch4-power-infrastructure.md`,
first-coverage discipline (no prior Eaton Company Intelligence record
existed). Portfolio HQ's WS-0005 Milestone 3 Batch 4, alongside `VRT`
and `PWR`, covering the three currently uncovered members of the
governed `power_infra` correlated-cluster cap (`GEV` already covered
under `PI-0007`/`PI-0019`/`PI-0020` and is not touched by this batch).

## Source-access disclosure

WebFetch was attempted and confirmed blocked (HTTP 403) on SEC EDGAR,
`eaton.com`, and a non-target control domain (`example.com`) in this
research session -- the same tool/proxy-level block already disclosed
in Batch 1-3's records (ASML/AMAT/KLAC/LRCX, MU/SKHY, AVGO/AMD/MRVL/INTC).
**No primary document (10-K, 8-K, press release) was directly opened
and inspected by this session.** Every figure below is WebSearch-sourced
-- either a search-engine reproduction of primary-filing content, or
secondary journalism/analyst commentary about a primary disclosure --
and is labeled "identified but NOT opened by this session," distinct
from independently-opened primary evidence. Where a search-engine
summary reproduced what it characterized as filing-table content, that
reproduction is treated as **unverified against the actual filing**,
not as equivalent to this session having opened the filing itself.

**Two research-integrity corrections made during drafting, disclosed
explicitly per this repository's "verify before acting on external
review" guardrail:**

1. An early search result returned a "full-year 2025 segment table"
   showing Electrical Americas revenue of only $3,253M and total
   segment sales of $6,377M -- arithmetically inconsistent with the
   well-corroborated $27.448 billion FY2025 total-company revenue
   figure. This is very likely a single quarter mislabeled as
   "full year" by a search summarizer. **This record does not use
   those figures anywhere** -- the segment table used below (Business
   summary section) is a separate, arithmetically-consistent
   reproduction that sums correctly to the corroborated total.
2. A search for Eaton and tariff-refund litigation returned multiple
   results that appeared, at a glance, to show "Eaton" as a party to
   the IEEPA tariff-refund class-action wave following the February
   2026 Supreme Court IEEPA ruling. On closer reading, every such
   result referred to **Judge Richard K. Eaton** of the U.S. Court of
   International Trade -- a person presiding over those cases, not
   Eaton Corporation. **This record makes no claim that Eaton
   Corporation is a party to IEEPA tariff-refund litigation** -- no
   evidence for that claim was found, and the apparent hits were a
   name collision.

## Business summary

Eaton is an Ireland-domiciled (post-2012 corporate inversion)
diversified power-management company, currently organized in five
reporting segments. FY2025 revenue by segment (WebSearch-reproduced
from a table attributed to Eaton's FY2025 Form 10-K, independently
arithmetic-checked -- sums to the well-corroborated $27.448 billion
total, +10% YoY):

| Segment | FY2025 | FY2024 | FY2023 |
|---|---|---|---|
| Electrical Americas | $13,276M | $11,436M | $10,098M |
| Electrical Global | $6,815M | $6,248M | $6,084M |
| Aerospace | $4,249M | $3,744M | $3,413M |
| Vehicle | $2,505M | $2,790M | $2,965M |
| eMobility | $604M | $662M | $636M |
| **Total** | **$27,448M** | **$24,878M** | **$23,196M** |

**Electrical** (Americas + Global, ~73% of FY2025 revenue) manufactures
circuit protection, switchgear, power distribution/quality equipment,
UPS systems, and wiring devices -- the segment carrying Eaton's current
data-center growth narrative. **Aerospace** (~15%) supplies fuel,
hydraulic, and fluid-conveyance systems to commercial and defense
aircraft OEMs (Boeing, Airbus named) plus a substantial aftermarket/MRO
business. **Vehicle and eMobility** (~11% combined, both segments
currently contracting -- Q4 2025 Vehicle sales -9% YoY/-13% organic,
eMobility -15% YoY/-17% organic) supply truck/auto components and
electrification systems; **on 2026-01-27 Eaton announced it will spin
off the combined Vehicle + eMobility "Mobility Group" into an
independent public company, targeted to close by end of Q1 2027** --
after which Eaton would be a pure Electrical + Aerospace company. This
record's current-tier-and-target statement (see "Governed policy"
below) describes Eaton as it is structured today; the spin-off, once
closed, will change the company's reporting structure before this
record's next scheduled review.

**FY2025 adjusted EPS $12.07 (+12% YoY). FY2026 guidance** (as of the
Q1 2026 update): adjusted EPS $13.05-$13.50 (+10% at midpoint); organic
growth raised to 9-11%. **Q4 2025 total-company segment margin reached
a reported record 24.9%; Q1 2026 segment margin contracted ~120bps to
22.7%**, which management attributes to input costs and
capacity-expansion ramp costs (described as temporary, partly offset by
pricing actions effective 2026-04-01) -- **and FY2026 full-year
segment-margin guidance was separately lowered ~50bps (to 24.1-24.5%)
in the same update that raised EPS/organic-growth guidance**, a genuine
mixed signal disclosed alongside the raise, not a clean beat-and-raise.
FY2025 operating cash flow $4.5B and free cash flow $3.6B, both
reported records.

## Data-center and electrical end-market exposure

**Fact, company-disclosed, repeated across secondary outlets, not
independently re-derived here:** at Q1 2026, Electrical Americas
data-center orders were up approximately 240% YoY and data-center
revenue was up approximately 50% YoY. Management cited approximately
32 GW of US data-center capacity under construction touching Eaton
equipment (~70% AI-related), and characterized total data-center order
backlog as "about 12 years of backlog at 2025 build rates" (228 GW
figure cited in secondary coverage). Total Electrical backlog was up
48% YoY at the Q1 2026 point -- a materially higher growth rate than
the ~29% YoY average reported across full-year 2025, consistent with
sequential acceleration rather than a steady-state run rate.

**Important counterweight, independently found:** at least one
secondary analysis (Alphastreet, "Eaton Has a Broader Electrical
Backlog Story Than the Data-Center Trade") explicitly argues that
non-data-center end markets -- utility, industrial, and institutional
spending -- still make up the majority of Electrical backlog. **This
record could not find a granular percentage breakdown of Electrical
revenue by end market** (data center vs. utility vs. industrial vs.
commercial/institutional vs. residential) -- only qualitative framing
and order/backlog growth rates were located via search. The data-center
narrative driving much of the current market attention on Eaton is
real and company-disclosed, but its precise share of total Electrical
revenue is not established by anything this record could verify.

## Moat and barriers to entry

Switchgear and switchboard products require UL 891/CE/CCC/IEC 61439
certification -- a genuine regulatory-compliance barrier, independently
corroborated by trade-press sources (Electronate), not solely by
Eaton's own materials. Standard UL-certified switchboard lead times run
50-80 weeks; transformer lead times were reported stretched to
approximately 4 years, with prices up roughly 80% over five years.
Capacity-expansion investments -- including a new medium-voltage
switchgear plant near Omaha (production starting 2027), part of a
multi-hundred-million-dollar 2023-2025 North American capacity
build-out -- take 2-3 years to bring online, a real time-based barrier
against a new entrant trying to capture the current demand surge
quickly. **Judgment:** this combination (certification + multi-year
lead times + multi-year capacity-build time) is a structural,
independently-corroborated moat specific to the current
supply-constrained environment, distinct from marketing language.

## Capital allocation and the Boyd Thermal acquisition

FY2025 capex guided ~$900M, explicitly earmarked to expand production
capacity for anticipated data-center-driven growth. Dividends paid
~$1,222M and share buybacks ~$1,669M through the first nine months of
2025 (both up modestly YoY); full-year 2025-2026 buyback guide
$2.0-2.4B.

**Recent M&A, cross-checked across multiple independent secondary
sources:** Exertherm (thermal monitoring, May 2024); NordicEPOD AS
(49% stake, standardized data-center power modules, May 2024);
Fibrebond Corporation ($1.45B, signed April 2025, modular power
enclosures); Resilient Power Systems Inc. (2025, deal value not found);
Ultra PCS Limited (aerospace/defense controls, closed January 2026).

**Boyd Thermal (the largest and most concentrated of these deals):**
agreed November 2025, approximately $9.5 billion (~22.5x Boyd Thermal's
estimated 2026 adjusted EBITDA) -- roughly **35% of Eaton's own FY2025
total revenue in deal value**, and Eaton's largest acquisition since
Cooper Industries ($13B, 2012). Boyd Thermal's own forecast 2026 sales
are ~$1.7 billion, of which ~$1.5 billion is liquid cooling for
hyperscale/AI data centers -- the deal is concentrated entirely in a
single growth thesis (data-center liquid cooling). **The exact close
date is disclosed inconsistently across secondary sources** (one states
closed 2026-03-12; another states "expected Q2 2026") and is not
resolved by this record -- what is clear is that the deal is not yet
reflected in any full-year segment financials as of this writing. This
combination -- large size relative to the company, single-thesis
concentration, and unresolved timing -- is treated here as a genuine,
current integration and thesis-concentration risk, not a settled
positive.

## Balance sheet and credit profile

Moody's affirms Eaton (and Eaton Capital Unlimited) at **A3**; outlook
moved to positive in April 2025, then back to **stable** in November
2025 -- a modest, not alarming, outlook wobble. Moody's projects
debt/EBITDA to remain below 2.5x. **This record could not
independently confirm a current S&P rating/outlook** -- only a generic
headline reference was found, no extractable rating text. **A
debt-to-equity figure surfaced inconsistently within a single secondary
source** (0.46 in one sentence, ~1.15 derived in the next, as of
2025-09-30) -- this contradiction is not resolved here and should be
checked against a primary balance sheet at the next review.

## Risks -- detail

**Margin-quality dispute, the most specific and best-evidenced current
tension:** Q1 2026 total segment margin contracted ~120bps to 22.7%.
Management's own framing is that this is temporary (input costs and
capacity-ramp expenses, addressed via pricing actions effective
2026-04-01). **UBS explicitly disputes this framing** in a rating
action downgrading ETN from Buy to Neutral, citing premium valuation
and estimating incremental margin on the new data-center-driven revenue
at only approximately 28% -- a named, specific analyst disagreement
with management's own characterization, not generic bear commentary.

**Structural separation risk:** the announced Mobility Group spin-off
(Vehicle + eMobility, ~$3B combined FY2025 revenue, both segments
currently shrinking) targeted for a Q1 2027 close carries ordinary
corporate-action execution risk (dis-synergies, stranded costs,
tax/regulatory timing) layered on top of Eaton's ordinary operating
risk.

**Boyd Thermal concentration and integration risk** -- see Capital
allocation section above.

**Hyperscaler AI-capex-cycle concentration:** a meaningful share of
Eaton's current growth/valuation narrative rests specifically on
data-center order flow (240% YoY Electrical Americas data-center order
growth cited for Q1 2026). A slowdown or pause in hyperscaler capital
spending would disproportionately affect the segment currently driving
market attention on Eaton, even though management's own qualitative
framing (and the Alphastreet counterweight above) suggests the broader
backlog is not purely a data-center story.

**Evidence gaps this record could not close via WebSearch alone:** no
current (2025/2026) customer- or project-concentration disclosure was
found for Electrical or Aerospace (only stale 1995/1999 Vehicle-segment
Ford/truck-OEM concentration data, and Vehicle is being spun off); no
granular end-market revenue-share breakdown; the debt/equity figure
noted above; the Boyd Thermal close-date inconsistency; no specific
supplier-concentration or component/casting/semiconductor-content
supply-chain risk disclosure was located (only general "input cost"
commentary from the Q1 2026 earnings call).

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, ETN currently sits in the **`band`** tier (0.75%
target weight, 1.25x cap, RSI-gated opportunistic trim) and is one of
four members of the governed **`power_infra`** correlated-cluster cap
(≤20% of book; the others are GEV, VRT, PWR). This placement is
recorded here as **existing governed policy, preserved as a historical
comparison baseline only, per `OPS-0006` §§2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion
in this record, and this record does not recommend any change to it.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Cyclicality:** Eaton has historically been a genuinely cyclical
  industrial, not a defensive holding. Documented drawdowns
  (cross-referenced across sources): **2008-09** -- approximately
  -70.5% peak-to-trough ($51.27 on 2007-07-23 to $15.13 on 2009-03-09),
  driven by real, disclosed demand deceleration in
  Automotive/Truck/Hydraulics, not merely multiple compression --
  i.e., a fundamentals-driven decline. **2020 COVID** -- approximately
  -45.0% ($105.10 on 2020-02-20 to $57.77 on 2020-03-23), recovered to
  the prior peak within roughly six months. **2022** -- approximately
  -28.4% ($174.66 on 2021-11-09 to $125.04 on 2022-07-14), a milder
  decline than one source's characterization of the broader market's
  concurrent peak-to-trough move, recovered by 2023-02-17.
- **Credit profile:** investment-grade, A3 (Moody's), stable outlook,
  debt/EBITDA projected below 2.5x -- not currently distressed.
- **Leverage/refinancing:** no confirmed near-term maturity wall or
  refinancing stress found; the debt/equity contradiction noted above
  is unresolved and should not be relied upon without primary
  confirmation.
- **Correlated-loss behavior:** the 2008-09 decline in particular was a
  genuine cyclical-industrial demand collapse, not a rate-driven
  de-rating -- relevant context for how a margin-funded position could
  behave in an actual recession, as distinct from a valuation-multiple
  correction like 2022's.
- **Current valuation context (descriptive, not a recommendation):**
  trading around $402.94 (2026-07-26 quote) against a 52-week range of
  $311.92-$436.74 (all-time high $435.78, 2026-06-22) -- roughly 7-8%
  off its all-time high, consistent with the UBS-downgrade/valuation
  narrative rather than a crash.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A slowdown/pause in hyperscaler AI capex reversing the current
  data-center order-growth trend (from +240% toward flat or negative).
- The Q1 2026 margin compression proving structural rather than
  temporary, consistent with UBS's ~28% incremental-margin estimate
  rather than management's own framing.
- A disclosed Boyd Thermal integration failure, overpayment, or
  goodwill impairment given the deal's size and single-thesis
  concentration.
- Material execution problems in the Mobility Group spin-off (delay,
  dis-synergies, unexpected stranded costs).
- A broader non-residential-construction/industrial-capex downturn,
  given Electrical remains dependent on utility/industrial/commercial
  spending beyond data centers specifically.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Consistently named across independent sources as competitors/possible
comparators: Schneider Electric (cited as data-center power-market
share leader in one market report), ABB, Vertiv (the batch's own VRT --
the most narrowly data-center-focused pure-play), Hubbell (electrical/
utility distribution overlap), Siemens, Emerson Electric, Legrand,
Delta Electronics. **These are noted as future research leads only,
per PI-0026 §B.22 -- no holding add, tier assignment, ranking, or
further research is authorized by naming them here.**

## Review framework

- **Cadence: 90 days** -- matches the existing cadence used for GEV,
  COST, and XOM's records, chosen for consistency with this
  repository's established pattern for large-cap industrials/mega-caps
  under active thesis development, not independently re-derived from
  first principles for ETN specifically.
- **Named review triggers**, drawn selectively from `OPS-0006` §12's
  candidate-trigger list (not every listed trigger applies):
  - Quarterly earnings/guidance updates, specifically watching whether
    the Q1 2026 margin contraction proves temporary (as management
    claims) or structural (as UBS argues).
  - The Boyd Thermal acquisition's close-date resolution and its first
    full reporting period inside Eaton's financials.
  - Material developments in the Mobility Group spin-off (regulatory
    filings, timeline changes, dis-synergy disclosures).
  - A material, sustained reversal in Electrical segment data-center
    order flow.
  - Any credit-rating action (Moody's or S&P) changing Eaton's
    investment-grade standing or outlook.

## Conviction

**Rating: Medium.**

**Rationale:** Eaton shows real, dated, cross-checked demand evidence
(FY2025 revenue $27.448B, +10%; adjusted EPS $12.07, +12%; a record Q4
2025 segment margin of 24.9%; accelerating Electrical backlog and
data-center order growth; raised FY2026 EPS/growth guidance) alongside
a structural moat (certification requirements, multi-year lead times
and capacity-build times) independently corroborated by trade press,
not just company materials. Conviction is held at Medium rather than
High because of three concrete, current tensions disclosed alongside
the growth: (1) a large, single, thesis-concentrated acquisition (Boyd
Thermal, ~35% of FY2025 revenue in deal value) not yet reflected in
reported financials; (2) a disclosed Q1 2026 margin contraction that
management calls temporary and at least one named analyst (UBS)
disputes as more structural, with a specific incremental-margin
estimate (~28%) cited as evidence; and (3) an announced structural
separation (Vehicle/eMobility spin-off, targeted Q1 2027 close) that
changes the company's own reporting structure before this record's
next scheduled review. This rating explicitly excludes valuation,
entry-price, allocation, trading, and margin judgments, and does not
treat Eaton's own guidance or backlog framing as validated fact without
the qualifications above.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by this session (see
  Source-access disclosure above).
- No current (2025/2026) customer- or project-concentration disclosure
  found for Electrical or Aerospace.
- No granular percentage breakdown of Electrical revenue by end market.
- No explicit book-to-bill ratio or disclosed backlog-cancellation rate.
- Current S&P credit rating/outlook not independently confirmed.
- The debt-to-equity contradiction (0.46 vs. ~1.15) as of 2025-09-30 is
  not resolved.
- The Boyd Thermal close date is disclosed inconsistently across
  sources and is not resolved here.
- No supplier-concentration or component/casting/semiconductor-content
  supply-chain-risk disclosure was located.
- The two research-integrity corrections disclosed at the top of this
  file (the internally-inconsistent segment table, and the Eaton/Judge
  Eaton name collision) should not be reintroduced in any future
  refresh of this record.

## Sources

See `ETN.yaml`'s `sources[]` for the structured register. Every entry
discloses that direct primary-document rendering was blocked in this
research environment, per the disclosure above.
