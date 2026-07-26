# VRT — Vertiv Holdings Co

Last updated: 2026-07-26 -- record created through AI-assisted research
and drafting under `governance/decisions/PI-0026-ws0005-milestone3-batch4-power-infrastructure.md`,
first-coverage discipline (no prior Vertiv Company Intelligence record
existed). Portfolio HQ's WS-0005 Milestone 3 Batch 4, alongside `ETN`
and `PWR`, covering the three currently uncovered members of the
governed `power_infra` correlated-cluster cap (`GEV` already covered
under `PI-0007`/`PI-0019`/`PI-0020` and is not touched by this batch).

## Source-access disclosure

WebFetch was attempted and confirmed blocked (HTTP 403) on SEC EDGAR,
`vertiv.com`, and a non-target control domain (`example.com`) in this
research session -- the same tool/proxy-level block already disclosed
in Batch 1-3's records. **No primary document (10-K, 8-K, press
release) was directly opened and inspected by this session.** Every
figure below is WebSearch-sourced and labeled "identified but NOT
opened by this session," distinct from independently-opened primary
evidence. One material, unresolved discrepancy in the sourced material
is disclosed explicitly below (the Q4 2025 vs. Q1 2026 backlog figures)
rather than silently reconciled or dropped.

## Business summary

Vertiv designs, manufactures, and services power equipment
(uninterruptible power supplies, DC power systems, power distribution,
switchgear/switchboard, busway, battery energy storage), thermal
management equipment (liquid cooling, heat rejection, chillers,
room/row/rack cooling), racks and enclosures, monitoring/management
software, and related services for data centers, communication
networks, and commercial/industrial facilities. Unlike ETN and GEV,
Vertiv's business is **concentrated specifically on data-center
infrastructure** rather than spanning a broader industrial/utility/
aerospace product line -- the batch's most narrowly data-center-focused
member.

**Origin, relevant to the balance-sheet discussion below:** Vertiv was
Emerson Electric's Network Power business, acquired by Platinum Equity
for approximately $4.158 billion (cash plus equity) in November 2016,
and taken public via a SPAC merger with GS Acquisition Holdings Corp in
February 2020. This private-equity/SPAC origin is the reason Vertiv's
historical leverage was materially higher than ETN's or PWR's --
addressed in the Balance sheet section below.

**FY2025 net sales $10,229.9 million (+26% organic YoY, from FY2024's
$8,011.8 million).** Geographic mix shifted toward the Americas (62%
of FY2025 sales, up from 56% in FY2024; Asia Pacific down to 20% from
22%; EMEA down to 18% from 22%) -- Americas net sales grew 41.9% YoY
while EMEA grew only 1.7%, a real regional divergence in an otherwise
strong year. **Q4 2025** (reported 2026-02-11): organic orders +252%
YoY, backlog reaching $15 billion (described as more than doubling
YoY), book-to-bill ratio approximately 2.9x, full-year adjusted
operating margin 23.2% (+170bps). **Q1 2026** (reported 2026-04-22):
net sales $2,650 million (+30% YoY: 23% organic, 4% acquisitions, 3%
FX), adjusted operating margin 20.8% (+430bps YoY), adjusted EPS $1.17
vs. $1.01 consensus, adjusted free cash flow $653 million (+147% YoY).
**FY2026 guidance was raised twice within roughly one quarter**: from
the Q4 2025 release's initial guide (net sales $13.25-13.75B, adjusted
diluted EPS $5.97-6.07) to the Q1 2026 release's raised guide (net
sales $13,500-14,000M / 29-31% organic growth, adjusted diluted EPS
$6.30-6.40).

## The unresolved backlog discrepancy

**This is the single most important unresolved item in this record.**
Vertiv reported total backlog of **$15 billion at Q4 2025** (described
as more than doubling year-over-year) but **$12.45 billion at Q1
2026** (as of 2026-03-31, described separately in the same release as
+80.8% YoY) -- a sequential decline of roughly $2.5 billion in one
quarter, despite orders reportedly still growing YoY in the same
period. This record's research pass could not reconcile the two
figures or locate an explicit management explanation via WebSearch, and
could not open the primary Q1 2026 release or earnings-call materials
directly (WebFetch blocked) to check for a restated definition,
one-time adjustment, or a plain conversion explanation (i.e., shipments
outpacing new bookings in that specific quarter). **This is presented
here as a real, disclosed discrepancy in the sourced figures, not
resolved in either direction** -- it could reflect ordinary
backlog-to-revenue conversion, or it could be an early signal of
order-flow deceleration behind the headline YoY growth framing. Either
reading is speculative without a primary-source reconciliation, which
this record does not claim to have performed.

## AI/data-center demand and the hyperscaler disintermediation risk

Company materials and multiple secondary sources describe a total
addressable market of roughly $60 billion, growing 9-11% annually, with
the data-center segment specifically (hyperscalers, "neoclouds" such as
CoreWeave, and colocation providers) growing 15-17% annually --
characterizations of company-disclosed TAM figures, not independently
verified against a primary market study. Vertiv has been expanding
liquid-cooling manufacturing capacity (Tognana, Italy campus doubling
regional chiller production capacity by end of 2026, a new large-scale
testing lab planned for early 2027) and continues a named collaboration
with NVIDIA on 800 VDC reference architectures for next-generation AI
data centers.

**Set against this, a specific and concrete disconfirming data point:**
AWS announced a custom, proprietary, rack-level liquid-cooling system
(reported as "IRHX") designed specifically for NVIDIA Blackwell GPUs --
precisely the AI-thermal-density workload central to Vertiv's own
growth narrative. Secondary commentary reports Vertiv's stock declined
on this announcement, and frames the mechanism plainly: when a
hyperscaler stops buying from a supplier and builds in-house instead,
the upstream vendor loses revenue on exactly the highest-growth segment
of its business. Vertiv continues signing third-party partnerships
(e.g., Compass Datacenters) and deepening its own NVIDIA collaboration,
which suggests hyperscaler in-house development and continued
third-party procurement are coexisting for now -- but this is a named,
specific competitive threat aimed at the center of Vertiv's growth
story, not generic competitive-risk boilerplate, and this record does
not assume it will remain contained to a single hyperscaler.

## Customer concentration and disclosure transparency

Multiple independent secondary commentators flag high customer
concentration tied to a relatively small number of hyperscale and
"neocloud" providers. At least one source explicitly characterizes
Vertiv's reduced backlog-reporting detail and vagueness regarding
customer concentration as a "less-than-bullish" signal. **This record
could not locate Vertiv's own quantified customer-concentration
disclosure** (e.g., percentage of revenue from its largest customers)
via WebSearch -- this is treated as a genuine transparency gap in what
is publicly available through search, not as confirmation that no such
disclosure exists, and it is not resolved here.

## Moat and competitive position

Cited moat mechanisms, drawn from secondary competitive-analysis
sources rather than a primary Vertiv disclosure: a large installed base
generating recurring service/maintenance revenue (one unverified
secondary estimate places the product/service revenue split around
81%/19%); long-term framework agreements and on-site service contracts
with hyperscaler/colocation customers, raising switching costs;
design-level integration with silicon providers (the NVIDIA 800 VDC
collaboration); and scale/certification requirements that limit the
practical number of suppliers able to bid for hyperscaler liquid-cooling
projects at scale. Independent analyst characterization describes this
as a "narrow," not "wide," moat -- real, but not unassailable.
Competitors named across sources: Schneider Electric (broader-line
rival), Eaton (this batch's own ETN -- broader electrical, less
data-center-pure), nVent Electric (a direct liquid-cooling-manifold
competitor), Rittal, STULZ, Boyd, CoolIT Systems (now owned by Ecolab),
and Alfa Laval. One market-research estimate places Vertiv's 2025
liquid-cooling market share at just over 11% -- a leadership position
in a still-fragmenting category, not dominance. Munters was named in
this record's original research brief as a possible competitor but no
search result in this pass confirmed or disconfirmed a competitive
relationship to Vertiv specifically.

## Financial quality and historical cyclicality

FY2025 adjusted operating margin 23.2% (+170bps), adjusted free cash
flow $1,887 million (+66% YoY). Q1 2026 adjusted operating margin
20.8% (+430bps YoY), adjusted free cash flow $653 million (+147% YoY),
operating cash flow $767 million (+153% YoY). **No gross-margin figure
was found in this research pass** -- only operating-margin figures were
located via search.

**A real, demonstrated historical margin-compression episode:** in Q1
2022, Vertiv reported an operating loss of $45 million and adjusted
operating profit of only $13 million, which its then-CEO (per secondary
reporting) attributed to inflation and supply-chain cost pressures the
company had "consistently underestimated... for both timing and
degree." The subsequent 2023 recovery was substantial (net sales +21%
to $6.9 billion, operating profit +290% to $872 million, adjusted
operating margin roughly doubling to 15.3%), but the 2022 episode
itself is a genuine, recent example of this specific company's
cost/pricing discipline failing under input-cost stress -- relevant
context distinct from the current growth narrative, not a hypothetical
stress scenario.

## Balance sheet and credit profile

**A materially de-risked balance sheet relative to Vertiv's
private-equity/SPAC origin.** Net leverage fell from approximately 2.8x
at the end of 2020 to below 2.0x by mid-2025, and to approximately
0.8x-1.0x currently (company-stated target range 1.0x-2.0x).
Debt-to-equity ratio 0.80 as of 2025-12-31, down 37.1% YoY from 1.26 a
year earlier. Credit ratings were upgraded one notch by all three major
agencies in February 2026 -- Moody's Baa3, S&P BBB-, Fitch BBB-, all
now investment grade (Vertiv's first investment-grade-rated debt
offering followed in March 2026: a $2.1 billion senior unsecured notes
offering across 10/20/30/40-year tranches, alongside a new $2.5 billion
senior unsecured revolving credit facility, with proceeds used to fully
repay the prior secured term loan). This deleveraging trend is
corroborated across multiple independent secondary sources, though this
record could not independently confirm the exact net-debt and equity
figures against a primary balance sheet.

## Supply chain and input-cost context

General (not Vertiv-specific) 2026 copper-market context: a projected
US refined-copper deficit, existing 50% Section 232 tariffs on
semi-finished copper products/derivatives, and a possible additional
duty pending a Commerce Department investigation. A reported April 2026
Section 232 tariff-scope amendment excluded GPU boards, accelerator
cards, and server racks from derivative-product tariffs; large diesel
backup generators, UPS systems, switchgear, cooling systems, and PDUs
were not included in the amended derivative list either. **This is
macro/industry context, not a Vertiv-specific disclosure** -- this
record found no company-specific quantification of copper/aluminum/
tariff cost exposure and does not present the general market data as
if it were Vertiv-reported.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, VRT currently sits in the **`band`** tier (0.75%
target weight, 1.25x cap, RSI-gated opportunistic trim) and is one of
four members of the governed **`power_infra`** correlated-cluster cap
(≤20% of book; the others are GEV, ETN, PWR). This placement is
recorded here as **existing governed policy, preserved as a historical
comparison baseline only, per `OPS-0006` §§2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion
in this record, and this record does not recommend any change to it.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Leverage:** net leverage roughly 0.8x-1.0x currently, down from
  ~2.8x in 2020; stated target range 1.0x-2.0x; investment-grade
  ratings across all three major agencies as of February 2026 -- a
  materially de-risked profile versus Vertiv's historical
  private-equity/SPAC-era leverage.
- **Liquidity:** new $2.5 billion senior unsecured revolving credit
  facility closed March 2026 (undrawn capacity not confirmed in this
  research pass); strong and growing adjusted free cash flow.
- **Refinancing risk:** the March 2026 refinancing extended
  weighted-average maturity via long-dated (10/20/30/40-year) tranches
  and was specifically used to retire the prior secured term loan,
  reducing near-term refinancing risk on the new notes.
- **Historical drawdown/volatility behavior:** one secondary source
  cites a five-year beta of 2.04 and a drawdown of roughly 25% from a
  June 2026 high, plus additional double-digit single-day price moves
  noted in 2025-2026 coverage -- VRT behaves as a high-beta,
  sentiment-sensitive name relative to broader AI-infrastructure
  narrative shifts, not as a defensive industrial, despite its
  data-center-infrastructure business description.
- **2022 precedent:** a real historical episode (Q1 2022 operating
  loss) demonstrates this company's margins can compress sharply under
  input-cost/supply-chain stress -- relevant historical context even
  though it predates the current, de-levered capital structure.
- **Correlated-loss potential:** given VRT's revenue concentration in
  hyperscaler/AI-capex-driven demand, its performance is plausibly
  correlated with other AI-capex-cycle-sensitive names already in this
  portfolio's `power_infra` cluster (GEV, ETN, PWR) and with
  semis-cluster AI-infrastructure exposure (NVDA especially, given the
  named NVIDIA collaboration). **This is an inference from the
  overlapping demand driver, not a measured price-correlation figure**
  -- no correlation coefficient was computed in this research pass,
  consistent with `OPS-0006`'s own distinction between structural/
  economic overlap and measured historical price correlation.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A confirmed, sustained deceleration in hyperscaler AI-related capex.
- Evidence that hyperscaler in-house cooling/power development (the
  AWS IRHX precedent) scales beyond a single hyperscaler and materially
  displaces Vertiv's addressable data-center opportunity, rather than
  coexisting with continued third-party procurement.
- A recurrence of 2022-style input-cost/supply-chain mispricing that
  compresses margins faster than pricing actions can offset.
- The unresolved Q4 2025-to-Q1 2026 backlog discrepancy resolving into
  a confirmed, sustained decline rather than a one-quarter conversion
  anomaly.
- A reversal of the 2020-2026 deleveraging trend (e.g., a large
  debt-funded acquisition materially increasing leverage again).

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

nVent Electric (direct liquid-cooling-manifold competitor, explicitly
framed against Vertiv in at least one comparative piece), Eaton (this
batch's own ETN, named alongside Vertiv in at least one "AI
infrastructure play" comparison despite a broader, less data-center-pure
business mix), Schneider Electric (largest named competitor, broader
ecosystem positioning), CoolIT Systems (liquid-cooling specialist, now
owned by Ecolab and not independently investable). Munters was named in
the original research brief but not found in any search result
confirming a competitive relationship. **These are noted as future
research leads only, per PI-0026 §B.22 -- no holding add, tier
assignment, ranking, or further research is authorized by naming them
here.**

## Review framework

- **Cadence: 90 days** -- matches the cadence used for GEV, COST, and
  XOM's records; shortened review would be defensible given the
  currently-unresolved backlog discrepancy and the fast-moving AI-capex
  narrative, but 90 days is chosen for consistency with this
  repository's existing pattern pending a named trigger firing sooner.
- **Named review triggers**, drawn selectively from `OPS-0006` §12's
  candidate-trigger list:
  - Any further quarterly disclosure reconciling or extending the
    $15B-to-$12.45B backlog discrepancy.
  - Any additional disclosed hyperscaler in-house
    cooling/power-development announcement beyond the AWS IRHX
    precedent.
  - Material developments in Vertiv's own customer-concentration
    disclosure practice (an improvement or further reduction in
    transparency).
  - Any credit-rating action changing Vertiv's investment-grade
    standing or outlook.
  - A material, sustained deceleration in reported orders growth.

## Conviction

**Rating: Medium.**

**Rationale:** Vertiv shows strong, cross-checked, recent demand and
margin evidence (FY2025 net sales +26% organic, Q4 2025 orders +252%
YoY, Q1 2026 adjusted operating margin +430bps YoY, two guidance raises
within roughly one quarter) alongside a materially de-risked balance
sheet compared to its private-equity/SPAC origin (net leverage roughly
0.8-1.0x vs. 2.8x in 2020, investment-grade ratings from all three
major agencies as of February 2026). Conviction is held at Medium
rather than High because of specific, concrete, currently-unresolved
tensions: (1) a named, not hypothetical, hyperscaler disintermediation
threat (AWS's in-house Blackwell-specific liquid-cooling system,
associated with a confirmed stock-price reaction) aimed directly at the
AI-thermal-density workload driving Vertiv's growth; (2) an unreconciled
backlog discrepancy ($15B to $12.45B across one quarter) this record
could not resolve via available sources; (3) a real, recent (2022)
demonstrated episode of margin compression under input-cost stress that
management itself admitted underestimating; and (4) a disclosed
customer-concentration/transparency gap flagged by independent
commentators and not resolved by any Vertiv-specific quantification
this record could locate. This rating explicitly excludes valuation,
entry-price, allocation, trading, and margin judgments.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by this session (see
  Source-access disclosure above).
- The $15B (Q4 2025) vs. $12.45B (Q1 2026) backlog discrepancy is
  disclosed and not reconciled.
- No Vertiv-specific quantified customer-concentration disclosure was
  found.
- No gross-margin figure was found (only operating-margin figures).
- No Vertiv-specific copper/aluminum/tariff cost-exposure quantification
  was found -- only general market context.
- The ~81%/19% product/service revenue-mix estimate is from a single
  secondary source and is not independently corroborated.
- Two different FY2026 full-year adjusted-operating-margin guidance
  figures (23.3% and 22.0-23.0%) appeared across different-dated
  secondary sources in this research pass, likely reflecting a
  guidance raise between the Q4 2025 and Q1 2026 releases, but not
  explicitly reconciled by anything this record located.
- Munters' competitive relationship to Vertiv, if any, was not
  confirmed or disconfirmed.

## Sources

See `VRT.yaml`'s `sources[]` for the structured register. Every entry
discloses that direct primary-document rendering was blocked in this
research environment, per the disclosure above.
