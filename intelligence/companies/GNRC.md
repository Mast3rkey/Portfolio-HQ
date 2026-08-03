# GNRC — Generac Holdings Inc.

Last updated: 2026-08-03 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0036-gnrc-rtx-company-intelligence-wave.md`
(`status: Accepted` at this record's base commit
`71ac5d759b4f7adc5b8f2237f00e6d6a407f5d00`), which narrowly supersedes
`governance/decisions/PI-0033-ws0005-milestone3-residual-deferrals.md` solely
for research-authorization purposes as to GNRC -- `PI-0033`'s own text is
otherwise unedited and remains fully controlling for the other sixteen names
it addresses. First Company Intelligence coverage for GNRC (no prior record
existed). **Filed as an administrative pairing with RTX** -- identical
portfolio-governance status (held, targeted, ungated, uncovered) and
execution efficiency only. GNRC and RTX share no genuine economic mechanism;
see Section 13 below and `PI-0036` for the explicit administrative-wave-versus-
economic-coherence distinction.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts against SEC EDGAR
(`sec.gov`) were tested and confirmed **blocked (HTTP 403) on every attempt
this session**, including a text-proxy workaround -- no SEC-hosted document
was directly opened. `investors.generac.com`'s own news-release pages and
static filed-document files (10-K/10-Q/annual-report PDFs) consistently
**timed out**. One exception: this session successfully and cleanly fetched
Generac's own **Q2 2026 earnings press release via its GlobeNewswire
wire-service distribution** -- company-authored text, treated as
primary-source content despite the non-`sec.gov`/non-`generac.com` domain.

**Every other SEC-filing-sourced fact in this record traces to a
WebSearch-returned snippet or paraphrase of the underlying filing, not to
this session's own direct reading of the filing text.** This is a
materially weaker access posture than a fully-fetched-filing session (see
`RTX.md`, researched the same day with full direct SEC EDGAR access via a
working curl/User-Agent approach) and is disclosed inline throughout this
record via FACT / SECONDARY / INFERENCE / JUDGMENT / LOW CONFIDENCE
labeling, not smoothed over. A handful of specific, disclosed gaps this
session could not resolve from any source found: the identity of the
customer representing roughly 10%/7% of accounts receivable at
FY2024/FY2023 year-end; supplier concentration by name or percentage;
current dealer-network size; quantified recurring/subscription/VPP revenue
as a percentage of total revenue; and a current (post-2021) residential
market-penetration figure.

## Business summary

Generac Holdings is a global designer and manufacturer of power-generation
and energy-technology products, headquartered in Waukesha, Wisconsin,
founded 1959. [GNRC-C01] Effective March 31, 2026, the company reorganized
its reportable segments from Domestic/International to **Residential** and
**Commercial & Industrial (C&I)** -- Residential is essentially the former
Domestic segment excluding domestic C&I; C&I combines the former
International segment with domestic C&I operations. For FY2025, net sales
were approximately $4.21 billion (down 2% from $4.30 billion in FY2024),
split roughly $2.27 billion (54%) Residential and $1.46 billion (35%) C&I,
with the remainder in other categories. [GNRC-C01]

Core product lines: residential whole-home standby generators and portable
generators (the historical core of the business); "energy technology"
products including PWRcell battery storage, solar microinverters (via the
Chilicon acquisition), EV charging (Wallbox minority stake), and smart
thermostats (ecobee); and C&I generators, switchgear, and enclosures for
data-center, telecom, industrial, rental, and government/municipal
markets. [GNRC-C02], [GNRC-C03]

**Distribution and installed base.** Generac sells primarily through an
independent dealer/installer network rather than direct sales -- this
avoids heavy direct-sales overhead but ties growth capacity to partner
installation throughput, and this session could not source a current,
sourced dealer-network count. [GNRC-C01] The company markets a "Mobile
Link" remote-monitoring subscription and participates in utility Virtual
Power Plant (VPP) programs that pay fees for aggregating residential
battery/generator capacity for grid services, but **no source found this
session quantifies recurring/subscription/VPP revenue as a share of total
revenue** -- the business is described in secondary commentary as still
predominantly a hardware/equipment-revenue model. [GNRC-C02]

**Estimated market position** (SECONDARY, third-party market-research
estimate, not company-disclosed): Generac holds an estimated roughly
75-80% share of the North American residential standby-generator market;
globally, the top five players (Caterpillar, Cummins, Generac, Briggs &
Stratton, Rehlko/Kohler) hold an estimated ~42% combined. [GNRC-C01]

## Acquisition strategy and capital allocation history

Generac has grown its non-generator product lines almost entirely through
acquisition, in two distinguishable eras (INFERENCE, based on the pattern
below): a 2019-2023 push into a residential "energy ecosystem" beyond
generators, and a 2025-2026 pivot toward C&I/data-center manufacturing
capacity.

- **Pramac** (PR Industrial S.r.l.): 65% acquired March 2016; additional
  15% purchased May 2021 for $27.164 million, bringing ownership to 80%.
- **Neurio Technology** (energy monitoring/analytics): acquired March 2019.
- **Pika Energy**: acquired April 2019 -- entry into battery-storage
  manufacturing (basis for PWRcell).
- **Deep Sea Electronics**: acquired June 2021 (generator control systems).
- **Chilicon**: acquired for approximately $4.286 million in shares
  (grid-interactive solar microinverters); exact acquisition date not
  confirmed this session.
- **ecobee Inc.**: acquired December 2021 for $200 million cash plus $450
  million GNRC stock, plus up to $120 million additional stock contingent
  on performance through June 30, 2023 (smart thermostats).
- **Wallbox N.V.**: minority investment, December 2023 (EV
  charging/energy management -- not a full acquisition).
- **Enercon Engineering**: acquisition agreement announced in the
  2025/early-2026 window, still closing as of the Q2 2026 release;
  purchase price undisclosed in sources found. Explicitly positioned to
  add switchgear and generator-enclosure manufacturing for data-center
  customers.
- **Belvidere facility**: acquired (per the Q2 2026 earnings release) to
  expand large-generator manufacturing capacity.

[GNRC-C03] All items in this list carry LOW-CONFIDENCE sourcing (WebSearch
snippets of SEC filings and company disclosures, not directly opened
documents) except the Q2 2026 release content, which was directly fetched.

## Cyclicality and weather/outage dependence

**This is the single most important, best-evidenced risk in this
record.** Demand for Generac's core Residential products has historically
tracked power-outage and severe-weather activity, and the company's own
five-year history demonstrates this concretely rather than merely as a
disclosed possibility:

- Net sales grew more than 50% in 2021 (pandemic- and storm-driven
  demand), then contracted approximately 12% in 2023.
- Diluted EPS fell from $8.51 (2021) to $3.31 (2023).
- Operating margin nearly halved, from 19.9% (2021) to 9.6% (2023).
- A roughly $300 million dealer/field channel-inventory overhang was cited
  by management in 2023.
- Free cash flow was negative (approximately -$27.7 million) in FY2022.

[GNRC-C04 / SECONDARY aggregation of company-reported financials, not
independently cross-checked against the original filings by this session]

**FY2025 confirms the pattern is still live, not merely historical.**
Full-year 2025 Residential product sales declined 7% to $2.27 billion,
which the company explicitly attributed to "continued weakness in power
outage activity." [GNRC-C04]

Secondary sources (summarizing EIA data, not independently opened by this
session) report that U.S. electricity customers experienced roughly
double the prior decade's average outage-hours in 2024, with the majority
of those hours attributed to three major hurricanes -- consistent with,
but not proof of, a broader secular grid-reliability-degradation driver
Generac's own management cites as a long-term demand tailwind (see below).
This session could not source a direct, quantified housing/new-construction
attach-rate linkage from a primary document.

## Data-center / C&I growth leg (2025-2026)

Generac's C&I segment has pivoted materially toward supplying large
backup generators, switchgear, and enclosures to hyperscale data-center
operators:

- Q2 2026: C&I external sales $556 million (+29% year over year); C&I
  adjusted EBITDA margin 14.6% (versus 12.4% in the prior-year quarter),
  with the release naming "core driver: data center market expansion."
- Data-center order **backlog of $1.6 billion** at Q2 2026, up from $600
  million previously, following roughly $1 billion in new orders over
  approximately 90 days.
- Two disclosed multi-year hyperscale supply agreements: the first for
  approximately $700 million of committed 2027 volume; a second, signed
  late June 2026, disclosed by the company as "expected to be at least as
  large," with deliveries potentially spanning 2027-2028.
- Investor Day (March 25, 2026) 2028 targets: revenue of $6.2-6.6 billion
  (midpoint approximately $6.4 billion, versus FY2025's $4.21 billion) and
  EBITDA of $1.25-1.45 billion (versus FY2025's $716 million) -- a growth
  algorithm that, on its face, requires C&I to grow substantially faster
  than the high-single-digit rate guided for Residential.

[GNRC-C03, directly-fetched Q2 2026 release content plus secondary
Investor Day summary]

## Balance sheet and financial quality

**Most recent full year (FY2025):** net sales $4.21 billion (-2% YoY); net
income $160 million / $2.69 diluted EPS (versus $316 million / $5.39 in
FY2024, down roughly 50%); adjusted net income $376 million / $6.34;
adjusted EBITDA $716 million (17.0% margin, versus 18.4% FY2024). Q4 2025
alone posted a **net loss of $24 million** ($0.42/share, versus $117
million of net income in Q4 2024), driven by a $104.5 million
litigation-settlement provision (see Risks). [GNRC-C04]

**Most recent quarter (Q2 2026, ended 2026-06-30), directly fetched from
the company's own press release:** net sales $1.173 billion (+11% YoY);
gross margin 44.5% (versus 39.3% prior year, including a roughly $71
million / ~6-point non-recurring tariff-refund benefit); adjusted EBITDA
$291 million (24.8% of sales, versus 17.7% prior year); net income $143
million ($2.40 diluted, versus $74 million / $1.25 prior year); operating
cash flow (six months) $240.5 million (versus $130.3 million prior year);
free cash flow (quarter) $62.9 million (versus $14.5 million prior year);
long-term debt $1.249 billion (versus $1.260 billion at 2025-12-31); cash
$264.9 million (versus $341.4 million at 2025-12-31); **share buybacks: $0
in H1 2026, versus $147.9 million in H1 2025** (paused); capex (six
months) $87.7 million (versus $88.7 million prior year); effective tax
rate 24.6% (versus 17.2% prior year, which benefited from a non-recurring
favorable item). [GNRC-C04]

**Leverage** (WebSearch snippet of the Q3 2025 Form 10-Q, not directly
opened): total leverage ratio 1.41x at 2025-09-30 (covenant ceiling
3.75x); interest coverage 12.54x (covenant floor 3.00x); net secured
leverage 1.35x; Term Loan B priced at SOFR + 1.75% (~6.03% all-in as of
that date). [GNRC-C04]

**Dividend policy:** Generac currently pays no regular dividend and states
it does not plan to for the foreseeable future; its credit facilities
currently limit dividend capacity. Historical one-time special dividends
($6.00/share in 2012, $5.00/share in 2013) were debt-refinancing-linked
recapitalization events, not indicative of current policy.

**FY2026 guidance** (as of the Q2 2026 release): net sales growth
mid-to-high teens percent; C&I growth low-30s percent; Residential growth
high-single-digit percent; adjusted EBITDA margin raised to 20.0-21.0%
(from 18.5-19.5% previously); net income margin 9.0-10.0% (from
8.0-9.0%); approximately 1.5 points of full-year benefit from tariff
refunds built into guidance.

## Competition and substitutes

**SECONDARY** (GMInsights market research): top North American residential
standby competitors -- Cummins, Rehlko (Kohler's rebranded engine/generator
business), Kirloskar, Briggs & Stratton -- together with Generac
representing an estimated ~90% of the category, with Generac dominant.

**SECONDARY** (MarketBeat analyst commentary, 2026-06-05): in the newer
C&I/data-center push specifically, Generac "faces stiff competition from
established industrial incumbents such as Caterpillar, Cummins, and
Kohler, all possessing deeper global service networks in data center
power markets" -- i.e., Generac is characterized as a relative newcomer
in hyperscale-grade backup power relative to its dominant residential
position. This session did not research battery-storage-specific
competitors (Tesla Powerwall, Enphase, LG, SolarEdge, etc.) -- an
explicit, disclosed open gap.

## Customer and supplier concentration

**FACT** (WebSearch snippet of the FY2024 Form 10-K, not directly opened):
no single customer accounted for more than 5%, 4%, and 4% of net sales in
FY2024, FY2023, and FY2022 respectively; however, one customer accounted
for approximately 10% and 7% of accounts receivable at 2024-12-31 and
2023-12-31 respectively. **The identity of that customer was not
confirmed by any source found this session** -- a plausible but
**unverified and unstated** guess would be a major retail channel partner
(Generac sells through Home Depot/Lowe's-type retail channels), but this
record does not assert that identification as fact.

**Supplier concentration:** no named single-supplier percentage was
found. What is documented is geographic sourcing exposure to China,
Vietnam, and India, subject to Section 301 and related tariffs (see
Risks).

## Investment thesis

**Concise statement:** Generac is the long-dominant leader in North
American residential standby power, a business with a real and repeatedly
demonstrated boom-bust demand cycle tied to storm/outage activity, now
building a second, evidenced growth leg in data-center/hyperscale backup
power that is still a minority of revenue but growing rapidly and backed
by disclosed, dollar-quantified multi-year supply agreements.

**Expanded narrative:** The residential franchise's demand curve is real
and severe -- 2021's storm/pandemic-driven boom was followed by a 2023
bust that cut operating margin nearly in half and briefly turned free
cash flow negative, and FY2025's Residential softness (explicitly
attributed by management to weak outage activity) confirms this
dependency has not gone away. [GNRC-C04] Against that backdrop, the C&I
segment's pivot into data-center backup power is a genuinely new,
evidenced development: a $1.6 billion backlog, two named multi-year
hyperscale supply agreements, and capacity investment (Enercon, Belvidere,
Sussex/Oshkosh) all point to a real, not merely aspirational, second
demand driver. [GNRC-C03] Whether this second leg is durable depends on
factors this record cannot resolve -- principally, whether hyperscaler
AI-infrastructure capital spending continues at a pace that sustains
Generac's disclosed backlog, and whether Generac can execute successfully
against incumbents with longer-established data-center service networks.

**Conditions required for the thesis to remain valid** (qualitative,
observable, no arbitrary numerical threshold):
- The disclosed data-center backlog converts to recognized C&I revenue
  roughly in line with FY2026 guidance (C&I growth in the low-30s percent)
- No material cancellation, delay, or shrinkage of either disclosed
  hyperscale supply agreement
- Residential segment revenue does not decline for multiple consecutive
  years even during above-average storm/outage years (which would suggest
  secular share loss or category maturity rather than weather noise)
- Total leverage ratio remains well within its covenant ceiling (currently
  ~1.4x against a 3.75x ceiling)
- No recurrence of a large-scale (>$50 million) product-liability charge
  comparable to the 2023 Pennsylvania explosion settlement

**Thesis-weakening / thesis-break conditions** (analytical judgment,
presented for review):
- A reversal or material slowdown in the data-center backlog or either
  named hyperscale supply agreement
- A return to negative free cash flow or a repeat of the FY2022-style
  channel-inventory buildup
- Leverage rising meaningfully toward the 3.75x covenant ceiling from the
  current ~1.4x
- Multi-year Residential revenue decline even during above-average
  storm/outage years
- Gross margin settling durably below the pre-2026 ~38-39% range once the
  ~$71 million tariff-refund benefit laps, without a credible replacement
  driver
- A new large-scale product-liability event beyond the 2023 explosion
  settlement, suggesting a systemic rather than isolated safety issue

## Monitoring signals

- Quarterly data-center backlog disclosure and its conversion rate into
  recognized C&I revenue
- Residential segment year-over-year trend, cross-referenced against
  storm/outage-season activity, to separate weather cyclicality from any
  secular demand shift
- Adjusted EBITDA and gross margin trend **excluding** the tariff-refund
  benefit
- Buyback resumption/pace as a capital-allocation confidence signal (paused
  entirely in H1 2026)
- Leverage ratio and covenant headroom in each 10-Q
- Enercon acquisition close/integration progress and Sussex/Oshkosh/
  Belvidere capacity-expansion progress
- Additional hyperscale customer wins versus order cancellations/push-outs
- Litigation docket for further portable-generator safety claims

## 13. Overlap and diversification versus power_infra (ETN/GEV/PWR) and versus CAT/TSLA

This assessment is deliberately not forced to a clean answer -- the honest
picture is mixed and evolving.

**Historically (pre-2025), GNRC's core demand mechanism was fundamentally
different** from the `power_infra` cluster's shared mechanism (AI
data-center power buildout -- utilities and hyperscalers building new
generation, transmission, and on-site power infrastructure, per this
repository's existing `targets.yaml`/`CLAUDE.md` cluster rationale for
ETN/GEV/PWR). GNRC's historical core -- residential/light-commercial
standby generators, sold reactively through a dealer-installer channel
mostly in response to storm/outage events -- is driven by weather
variability, residential grid-reliability perception, and homeowner
discretionary spending. That is a different mechanism, closer in
character (though not necessarily in measured correlation, which this
record does not compute) to the kind of broad, non-thesis-specific macro
exposure that led CAT and TSLA to be scanned and explicitly *excluded*
from the `power_infra` cluster cap on weak-fundamental-fit grounds
("more likely riding bull-market beta than the specific power-buildout
mechanism," per `CLAUDE.md`'s Decisions Log).

**But the 2025-2026 data materially changes this picture.** GNRC's C&I
segment now supplies large-megawatt backup generators, switchgear, and
enclosures directly to hyperscale data-center operators under disclosed,
dollar-quantified, multi-year supply agreements ($700 million-plus 2027
commitment; a second agreement disclosed as at least as large; a $1.6
billion total backlog; the Enercon acquisition explicitly for data-center
switchgear/enclosures). This is not indirect beta -- it is a direct,
contracted exposure to the same AI-buildout theme ETN (switchgear/power
distribution), GEV (turbines/grid equipment), and PWR
(EPC/interconnection) already represent, and on-site backup generation is
a literal complementary line item in the same data-center power stack.

**However, this data-center exposure remains a minority of total
company revenue.** C&I was ~35% of FY2025 sales ($1.46 billion of $4.21
billion), and even within C&I, data centers are described as the "core
driver" but not the entirety -- telecom, rental, industrial, and
government gensets also sit within C&I. Residential -- genuinely
uncorrelated with the AI-buildout mechanism -- remains the majority of
revenue (~54%, $2.27 billion).

**Net judgment (analytical, not a sourced fact):** GNRC today sits
between the two poles this repository has already established for the
`power_infra` cluster question. It is not a clean "different mechanism"
case the way the CAT/TSLA exclusion rationale would suggest if applied
naively -- GNRC's C&I/data-center leg has a more direct, contractually
evidenced fit to the AI-buildout mechanism than CAT's or TSLA's general
market beta. But it is also not a clean cluster-member case, because the
majority of revenue and the company's historical identity remain in a
genuinely different, weather/housing-driven mechanism. **This is a
blended, actively evolving exposure.** No correlation scan of GNRC
against `power_infra` member returns has been performed by this record
or by any prior repository decision (`PI-0033` §A.2 states plainly that
"unlike CAT, GNRC was never even included in the original `power_infra`
correlation scan") -- performing one is named in `PI-0033`'s own GNRC
reopening trigger and remains a live, unauthorized Milestone-4-adjacent
question this record flags but does not answer. **This record does not
recommend, and is not evidence for, any change to GNRC's cluster
membership, cap treatment, tier, or target** -- any such change requires
its own separate, later, explicit governance decision.

## Next-best use of capital (descriptive framing only, no recommendation)

Factors that could argue for GNRC as a distinctive marginal allocation:
a dual-driver demand profile not otherwise represented in this roster (a
weather/storm-driven residential cycle plus an emerging, contractually
evidenced AI-data-center C&I leg), combined with a conservatively levered
balance sheet (~1.4x total leverage, meaningful covenant headroom) that
gives capacity to fund the disclosed capacity buildout without near-term
financial stress. The position is currently well below its 1.25%
canonical target and is not gated.

Factors arguing for caution on the margin: the company has a recent,
severe, well-documented boom-bust demand history that mechanically
illustrates how quickly either demand driver (storm-based or AI-capex-
based) can reverse; a meaningful share of the most recently reported
margin improvement is a non-recurring tariff refund rather than pure
operating leverage; and the most recently reported full year included a
material, one-off product-liability charge that produced a net loss in
one quarter -- a reminder of manufacturing/safety tail risk that is
idiosyncratic to GNRC rather than macro-driven. No price target,
valuation opinion, or buy/sell recommendation is offered.

## Uncertainty and open items (explicit, not smoothed over)

1. SEC EDGAR could not be directly opened this session (403 on every
   attempt) -- nearly every SEC-filing-sourced fact above is a
   WebSearch-derived snippet/paraphrase, not an independently verified
   primary-document read. Only the Q2 2026 earnings release was directly
   fetched and read in full.
2. Identity of the customer representing ~10%/7% of accounts receivable
   (FY2024/FY2023) -- not named in any source found; not confirmed.
3. Supplier concentration (named supplier, percentage of cost of goods
   sold) -- not found; only general China/Vietnam/India geographic
   exposure confirmed.
4. Current (post-2021) residential market-penetration figure -- only a
   2021-vintage number was found; may be stale, not re-confirmed.
5. Battery-storage/solar-storage competitive landscape (Tesla Powerwall,
   Enphase, LG, SolarEdge, etc.) -- not researched this session.
6. Quantified recurring/subscription/VPP revenue as a percentage of total
   revenue -- not disclosed in any source found.
7. Current dealer-network size -- no sourced figure obtained.
8. No correlation scan of GNRC against `power_infra` cluster-member
   returns has ever been performed by this repository (see Section 13) --
   this record does not perform one and explicitly does not resolve the
   cluster-membership question.

## Review framework

- **Cadence: 90 days**, matching this repository's corpus-wide default.
- **Mandatory unscheduled-review triggers** (qualitative, observable):
  material change to either disclosed hyperscale supply agreement or the
  data-center backlog figure; a Residential-segment multi-quarter decline
  outside a low-outage-activity explanation; a new material
  product-liability event; a dividend initiation or buyback resumption (a
  capital-allocation-posture change); any leverage-ratio move toward the
  covenant ceiling; publication of GNRC's FY2026 Form 10-K.
- **Metrics worth monitoring each review:** data-center backlog and
  conversion rate; Residential segment revenue trend versus storm/outage
  activity; gross margin excluding tariff-refund effects; leverage ratio;
  buyback pace.

## Conviction

**Rating: Medium** -- see `GNRC.yaml`'s `conviction.rationale` for the
full statement. This rating is a PROPOSED rating pending independent
exact-head review and principal acceptance; AI-assisted drafting does not
itself constitute approval.

## Sources

See `GNRC.yaml`'s `sources:` block for the complete, structured source
list with dates and URLs where directly fetched. In summary: one directly
fetched primary-source-content document (Q2 2026 earnings release via
GlobeNewswire); several SEC filings identified but not directly opened
(FY2025 Form 10-K, the March 2026 segment-reorganization 8-K, the Q3 2025
Form 10-Q); and secondary market-research/analyst sources used only for
competitive-context and historical-financial-illustration purposes,
explicitly labeled throughout this record and never conflated with a
primary-source fact.
