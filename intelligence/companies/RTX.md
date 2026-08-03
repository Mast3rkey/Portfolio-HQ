# RTX — RTX Corporation

Last updated: 2026-08-03 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0036-gnrc-rtx-company-intelligence-wave.md`
(`status: Accepted` at this record's base commit
`71ac5d759b4f7adc5b8f2237f00e6d6a407f5d00`), which narrowly supersedes
`governance/decisions/PI-0033-ws0005-milestone3-residual-deferrals.md` solely
for research-authorization purposes as to RTX -- `PI-0033`'s own text is
otherwise unedited and remains fully controlling for the other sixteen names
it addresses. First Company Intelligence coverage for RTX (no prior record
existed). **Filed as an administrative pairing with GNRC** -- identical
portfolio-governance status (held, targeted, ungated, uncovered) and
execution efficiency only. RTX and GNRC share no genuine economic mechanism;
see Section 19 below and `PI-0036` for the explicit administrative-wave-versus-
economic-coherence distinction.

## Source-access disclosure

This session directly opened and parsed three primary documents via a
working SEC EDGAR access path (a User-Agent-identified fetch, and the
`data.sec.gov` JSON API for supplementary lookups -- standard `WebFetch`
calls to `sec.gov` returned HTTP 403, a tooling note, not a content-
confidence issue, since the workaround succeeded): the **FY2025 Form 10-K**
(filed 2026-02-06), the **Q2 2026 Form 10-Q** (filed 2026-07-23), and the
**Q2 2026 earnings press release** (Exhibit 99 to the Form 8-K filed
2026-07-23). This is a materially stronger access posture than the
same-day `GNRC.md` record, which could not directly open any SEC-hosted
document. `investors.rtx.com` timed out on every attempt, so no standalone
investor-relations presentation deck was reviewed -- every fact below is
sourced to the three SEC filings above. Two explicit gaps: RTX does not
disclose a specific aftermarket-margin percentage in these filings (the
aftermarket-driven-margin-growth statements below are qualitative company
commentary, not a disclosed number), and this session did not
independently verify the January 7, 2026 Executive Order's own text
against a White House/Federal Register primary source -- it is reported
here exactly as RTX's own 10-K describes it.

## Business summary

RTX Corporation is an aerospace/defense conglomerate operating through
three segments: **Collins Aerospace**, **Pratt & Whitney**, and
**Raytheon** (defense systems). FY2025 segment net sales: Collins $30,196
million, Pratt & Whitney $32,916 million, Raytheon $28,043 million;
consolidated net sales $88,603 million (net of intersegment
eliminations). FY2025 segment operating margins: Collins 16.3%, Pratt &
Whitney 7.9%, Raytheon 11.5%; total segment margin 11.8%; consolidated
GAAP operating margin 10.5%. [RTX-C01, source: FY2025 Form 10-K, Note 20]

**Revenue mix by customer type** (FY2025, 10-K): U.S. government direct
sales $33,279 million (38% of total, down from 40% in FY2024 and 46% in
FY2023 -- the FY2023 percentage was inflated by the GTF powder-metal
revenue reduction shrinking that year's denominator); foreign military
sales through the U.S. government $6,702 million (7.6%); foreign
government direct commercial sales $6,123 million (6.9%); commercial
aerospace and other commercial $42,499 million (48.0%). Combined
government-related revenue is approximately 52% of the total; commercial,
approximately 48%. Airbus alone represented 14% of total RTX net sales in
2025.

## Segment detail

**Collins Aerospace** makes avionics, power/electric systems,
environmental control, flight controls, landing systems (wheels/brakes),
cabin interiors, communications/navigation systems, space life-support
systems, and defense command-and-control/battlespace systems. Boeing and
Airbus combined represented 16% of Collins segment sales in 2025 (16% in
2024, 19% in 2023). 2025 organic growth by driver (MD&A): aftermarket
+$1.4 billion, defense +$0.7 billion, commercial OEM +$0.5 billion.

**Pratt & Whitney** is a leading commercial and military engine
manufacturer. Commercially, the GTF (Geared Turbofan, PW1000G family)
powers more than 2,600 aircraft across 90-plus operators on three
platforms (A320neo family, A220, E-Jets E2); the GTF Advantage variant
received FAA and EASA certification in 2025. Militarily, the **F135
engine has exclusive, sole-source status powering all three F-35
variants**, surpassed one million flight hours in 2025, and received a
$2.8 billion undefinitized contract action for Lot 18/19 production in
2025. Airbus is Pratt & Whitney's largest commercial customer: 29% of
segment sales in 2025 (31% in 2024; 48% in 2023, the elevated 2023 figure
again reflecting the powder-metal charge's effect on that year's
denominator).

**Raytheon** (defense systems) makes missiles, air- and missile-defense
systems, sensors/radar, defense electronics, space systems, and
hypersonics. Named major programs in the 10-K include Patriot, LTAMDS,
AMRAAM, SM-3/SM-6, Tomahawk, AIM-9X Sidewinder, NASAMS, Javelin, Stinger,
StormBreaker, SPY-6 radar, Next Generation Jammer, and Coyote
counter-unmanned-aircraft systems. FY2025 segment operating margin was
11.5%, up from 9.7% in FY2024.

## The Pratt & Whitney GTF powder-metal matter (full detail)

This is the single most consequential, best-documented company-specific
risk in this record, and remains open, not closed:

- In July/August 2023, Pratt & Whitney determined that a rare powder-metal
  contamination requires accelerated inspection of the PW1100G-JM engine
  fleet (which powers the A320neo family). A Special Instruction was
  issued August 4, 2023; an expanded fleet management plan followed in
  November 2023, subsequently reflected in FAA airworthiness directives.
- **Q3 2023 pre-tax operating-profit charge: $2.9 billion**, reflecting
  RTX/Pratt & Whitney's net 51% program share (partners -- MTU, JAEC, and
  others -- hold the remaining 49% under the IAE international
  collaboration). The gross (100%) impact was a **$5.4 billion** reduction
  to net sales in Q3 2023, offset by a **$2.5 billion** reduction to cost
  of sales reflecting the partners' own share.
- This produced a **$2.8 billion** net increase to Other accrued
  liabilities (the customer-compensation accrual) at inception.
- **Accrual balance trajectory, directly confirmed across the two
  directly-opened filings: $2.8 billion (Q3 2023 inception) -> $1.7
  billion (2024-12-31) -> $0.7 billion (2025-12-31) -> $0.4 billion
  (2026-06-30).** Utilization (cash paid plus credits issued): $1.0
  billion in 2024, $1.0 billion in 2025. The company's own FY2026
  cash-impact estimate is approximately $0.7 billion.
- **Aircraft-on-ground (AOG) levels for the affected PW1100-powered
  A320neo fleet are expected to remain elevated through 2026**, per the
  company's own current disclosure as of the Q2 2026 10-Q -- not yet
  revised to an earlier resolution date as of this record.
- **Litigation and regulatory tail:** securities class actions were
  dismissed by the District of Connecticut on September 12, 2025;
  plaintiffs appealed to the Second Circuit on October 14, 2025.
  Shareholder derivative suits are pending in the District of Delaware. An
  **SEC investigation remains ongoing** (subpoenas received; outcome and
  timing explicitly described by the company as unable to be predicted).
- The company states it does not currently believe other affected engine
  models will have a material financial impact, but explicitly flags this
  as an assumption subject to change -- not a resolved conclusion.

## Backlog, aftermarket, and commercial/defense mix

**Backlog (FY2025 year-end, 10-K):** total $268 billion (up from $218
billion in FY2024) -- Collins $42B, Pratt & Whitney $151B, Raytheon $75B.
Split: commercial $161B / defense $107B. Defense bookings were
approximately $61 billion in both 2025 and 2024, and $51 billion in 2023.

**Backlog (Q2 2026, most recent, 10-Q):** total **$289 billion** --
commercial $170B / defense $119B. Raytheon's own defense backlog reached
$86 billion at 2026-06-30 (up from $75 billion at 2025-12-31), driven in
part by **$3.7 billion of Patriot GEM-T interceptor bookings for Ukraine**
in Q2 2026 alone, plus $988 million of GEM-T bookings for Poland via NATO
NSPA. RTX's CEO, in the Q2 2026 earnings release (2026-07-23), stated
backlog was "up 22 percent year over year."

**Aftermarket economics:** RTX does not disclose a single consolidated
aftermarket-margin percentage in these filings. Qualitatively, MD&A
commentary repeatedly attributes margin expansion to aftermarket
volume/mix -- e.g., Collins' 2025 organic profit growth citing "higher
commercial aerospace aftermarket sales of $1.4 billion," and Pratt &
Whitney's Q2 2026 commentary citing a "25 percent increase in commercial
aftermarket" alongside military volume as profit-growth drivers. This is
consistent with (but not independently proof of, beyond company
commentary) the industry-standard pattern that aftermarket carries higher
margins than original equipment.

## Defense-budget, export-control, and geopolitical exposure

**Budget/procurement:** the 10-K's risk factors explicitly flag U.S.
government budget and appropriations volatility, including reliance on
continuing resolutions and shutdown risk. The FY2025 10-K discloses, as a
subsequent event, that **a government shutdown was actually resolved on
February 3, 2026** when Congress passed and the President signed a
spending package -- with the Department of Homeland Security remaining on
a continuing resolution at that time. This confirms appropriations
disruption is a realized, recurring risk for this filing period, not
merely theoretical. Separately, the filing consistently refers to the
U.S. Department of Defense as the **"Department of War (DoW)"** throughout
-- a real nomenclature fact from the primary source, noted here since it
is non-obvious. RTX's own defense-bookings momentum ($61 billion
company-wide defense bookings in both FY2025 and FY2024; Raytheon backlog
growing to $86 billion) suggests the company is currently a beneficiary of
an elevated-threat-environment budget cycle -- though this is a two-year
snapshot, not a structural guarantee.

**China:** China announced sanctions in February 2023 against the former
Raytheon Missiles & Defense business over Taiwan arms sales (a stated fine
equal to twice the value of arms sold to Taiwan since September 2020);
additional sanctions have since been announced against Raytheon and a
Collins joint venture. The company states future impact is "uncertain";
ongoing Taiwan foreign military sales are expected to continue "in
alignment with U.S. government policy."

**Russia/Ukraine:** broad U.S. and allied sanctions on Russia apply since
the invasion; Russian counter-sanctions target certain RTX management and
board members personally. Canadian sanctions (February 2024) on
Russian-owned titanium suppliers forced RTX to source alternate titanium,
causing a **$175 million charge in Q1 2024 within Collins** (unfavorable
purchase commitments plus contract-fulfillment impairment) -- a realized,
not hypothetical, supply-chain cost. At the same time, the war is a direct
current demand driver: $3.7 billion of Patriot GEM-T bookings "for
Ukraine" in Q2 2026 alone.

**Legacy compliance overhang:** in October 2024, Raytheon entered two
Deferred Prosecution Agreements (one FCPA/AECA-related, concerning Middle
East payments through the Thales-Raytheon joint venture since 2012;
another combined with a False Claims Act settlement, concerning defective
pricing on legacy 2011-2017 contracts) plus an SEC Administrative Order,
with a single independent compliance monitor covering all three. Separately,
an August 2024 Consent Agreement with the State Department (a three-year
term) resolved ITAR/AECA export-control violations tied mainly to the
Rockwell Collins integration, requiring an externally appointed Special
Compliance Officer (appointed September 27, 2024) and an external
ITAR-compliance audit. None of these is individually deemed material by
RTX, but collectively they represent sustained government compliance
scrutiny.

**A genuinely new, disclosed political risk:** a **January 7, 2026
Executive Order**, as described in RTX's own FY2025 Form 10-K, empowers
the "Secretary of War" to potentially restrict RTX's ability to pay
dividends or repurchase stock if the government determines RTX has
"underperformed or lacked sufficient prioritization of, investment in or
production speed in" its U.S. government contract performance. This is an
unusual, recently disclosed (within roughly seven months of this record)
capital-allocation risk specific to defense primes under the current
administration -- flagged here as high-salience for governance purposes,
and not independently verified against the Executive Order's own primary
text by this session (see Source-access disclosure).

## Customer, supplier, and competitive structure

**Customer concentration:** U.S. government (direct) is 38% of FY2025
revenue; total government-related revenue (direct plus foreign military
sales plus foreign government direct) is approximately 52%. Airbus is 14%
of total company revenue, 29% of Pratt & Whitney segment revenue, and is
explicitly named as a segment-level concentration risk. Boeing and Airbus
combined are 16% of Collins segment revenue. No single commercial-airline
customer concentration is separately broken out in the 10-K.

**Supplier dependencies:** the 10-K explicitly names dependency on foreign
sources for cobalt, tantalum, chromium, rhenium, nickel, and titanium,
with single-source foreign suppliers for some components. The titanium
risk crystallized concretely via the $175 million Q1 2024 charge described
above -- a realized, not hypothetical, event. Broader supply-chain
disruption commentary (rare earths, microelectronics) is qualitative and
not further quantified in the filings reviewed.

**Competitive structure:** the 10-K's Competition section is deliberately
generic, in keeping with standard practice for large defense primes -- it
does not name specific competitors. It does note that competitors
increasingly include non-traditional/commercial entrants and startups
favored by the Department of War's Other Transaction Authority contracting
approach, foreign-government-subsidized competitors, and an increasing
government appetite for IP-sharing terms that could erode
differentiation. As general industry background (not sourced to this
filing, flagged as such): in commercial narrowbody engines, the GTF's only
direct competitor is CFM International's LEAP (a GE Aerospace-Safran
joint venture); in missiles/air-defense, RTX's principal U.S. peers are
Lockheed Martin (also RTX's own F135 customer via the F-35 program),
Northrop Grumman, and L3Harris.

## Capital allocation and financial quality

**Dividends and buybacks:** dividends declared per share rose from $2.320
(2023) to $2.480 (2024) to $2.670 (2025) -- a steadily rising payout. Cash
dividends paid were $3,574 million in 2025 versus $3,217 million in 2024.
Buybacks, by contrast, have been modest and sharply reduced: only **$50
million repurchased in all of FY2025** (396,000 shares), versus $186
million in FY2024. The Board authorized an $11 billion repurchase program
in October 2023; only approximately $0.6 billion of that authority
remained at 2025-12-31 -- meaning roughly $10.4 billion was executed
earlier in the program, with the pace now near zero.

**Debt and credit quality:** total debt fell from $41,261 million
(FY2024) to $37,904 million (FY2025); total debt to total capitalization
improved from 40% to 36%. Credit outlooks improved during 2025: Moody's
Baa1/negative moved to Baa1/stable (March 2025); S&P affirmed BBB+ with
outlook improved from negative to stable (June 2025).

**Financial trend summary** (10-K and 10-Q, directly sourced):

| Metric | FY2023 | FY2024 | FY2025 | Q2 2025 | Q2 2026 |
|---|---|---|---|---|---|
| Net sales | $68,920M | $80,738M | $88,603M | $21,581M | $24,708M |
| GAAP operating margin | 5.2% | 8.1% | 10.5% | 9.9% | 11.4% |
| Operating cash flow | $7,883M | $7,159M | $10,567M | $458M | $3,547M |
| Free cash flow | ~$5,468M | ~$4,534M | ~$7,940M | $(72)M | $2,878M |

FY2023's depressed operating margin reflects the $2.9 billion powder-metal
charge; Q2 2025's depressed operating cash flow/free cash flow reflects a
roughly $100 million Pratt & Whitney customer-bankruptcy charge and
working-capital timing. **FY2026 guidance was raised in the Q2 2026
release (2026-07-23):** adjusted sales $95.0-96.0 billion (from
$92.5-93.5 billion previously), organic growth 8-9% (from 5-6%), adjusted
EPS $7.10-7.25 (from $6.70-6.90), free cash flow $8.50-8.75 billion (from
$8.25-8.75 billion). All three segments showed adjusted-margin expansion
in Q2 2026 versus Q2 2025: Collins 16.7% versus 16.4%; Pratt & Whitney
8.3% versus 8.0%; Raytheon 12.6% versus 11.6%.

## Investment thesis

**Concise statement:** RTX is a diversified aerospace/defense
conglomerate showing genuine, primary-source-confirmed operating
momentum -- rising backlog, raised guidance, expanding segment margins,
and an improving credit profile -- while still carrying a real, unresolved
engine-remediation liability and a newly disclosed political risk
targeting its own capital-return capacity.

**Expanded narrative:** The three-segment structure gives RTX exposure to
commercial aerospace OEM and aftermarket cycles (Collins, Pratt &
Whitney), a durable sole-source military-engine franchise (Pratt &
Whitney's F135/F-35), and defense-electronics/missile programs benefiting
from an elevated-threat-environment procurement cycle (Raytheon) --
evidenced concretely by 22% year-over-year backlog growth to $289 billion
and $3.7 billion of single-quarter Ukraine-driven Patriot bookings. Set
against that momentum, the GTF powder-metal matter is not a closed
chapter: the compensation accrual continues shrinking on schedule ($2.8B
-> $1.7B -> $0.7B -> $0.4B) but affected-fleet aircraft-on-ground levels
are still expected to remain elevated through 2026, and an open SEC
investigation plus appealed litigation mean the matter's full resolution
timeline and total cost remain genuinely uncertain. The January 2026
Executive Order disclosure is a new, filing-confirmed fact this record
treats as material context rather than speculation -- it did not exist as
a risk a year earlier, and its practical significance (has it been
invoked, clarified, or left dormant) is presently unknown.

**Conditions required for the thesis to remain valid** (qualitative,
observable):
- The GTF customer-compensation accrual continues declining and
  aircraft-on-ground levels begin improving from "elevated" as FY2026
  progresses, without a new charge
- Defense and commercial backlog both continue growing or at minimum do
  not reverse into net cancellations
- No SEC enforcement action, restatement, or material adverse ruling
  emerges from the ongoing GTF-related investigation
- The January 2026 Executive Order is not actually invoked to restrict
  RTX's dividend or buyback capacity
- Credit ratings/outlook do not reverse back toward negative

**Thesis-weakening / thesis-break conditions** (analytical judgment,
presented for review):
- GTF accrual utilization stalls or reverses, or a new powder-metal-related
  charge is taken in a future filing
- The SEC investigation results in an enforcement action, penalty, or
  restatement
- The January 2026 Executive Order (or a successor policy) is actually
  invoked against RTX
- A full-year decline (not merely a growth-rate slowdown) in defense
  backlog, signaling a budget-cycle turn
- A material adverse ruling on the roughly $2.1 billion-plus DCMA Cost
  Accounting Standards claims, or a DPA breach determination
- A credit-rating downgrade back to negative outlook or below BBB+/Baa1

## Monitoring signals

Quarterly: Pratt & Whitney segment margin trajectory and the GTF
customer-compensation accrual balance in each new 10-Q; commercial-versus-
defense backlog mix shift; buyback resumption as a capital-allocation
confidence signal; SEC-investigation status updates; DPA/Consent
Agreement compliance-monitor findings (the 10-K described the monitor
engagement as pending "by end of first quarter" -- worth confirming this
has actually occurred); status of the January 2026 Executive Order (has it
been invoked, clarified, or left dormant); Ukraine/NATO booking cadence as
a proxy for allied-demand durability; China-Taiwan sanctions escalation.

## 19. Diversification versus existing roster holdings

Per this repository's current roster, **no other aerospace/defense name is
currently held** -- RTX's revenue drivers (commercial-aftermarket cycle,
Department of War appropriations, GTF-specific engineering/regulatory
risk, ITAR/export-control regime, Airbus/Boeing OE cycle) do not overlap
with this roster's industrial, technology, or financial holdings in any
mechanism this record has identified. This is a portfolio-structure
observation drawn from the roster context supplied for this research wave,
not an independently re-verified scan of every other holding's own
Company Intelligence record. **RTX and GNRC, the two companies covered by
this same governance wave (`PI-0036`), also share no genuine economic
mechanism** -- see `PI-0036`'s "Administrative wave, not economic
coherence" section; their joint filing reflects identical
portfolio-governance status (held, targeted, ungated, uncovered) and
execution efficiency only, never a claimed business relationship.

## Next-best use of capital (descriptive framing only, no recommendation)

RTX sits at a 0.240403-share position against a 0.75%-of-book, not-gated
canonical target -- structurally a build-toward-target position under the
current architecture, not a trim candidate (restating the repository's own
existing governed state, not new research). Descriptively: the company is
currently directing incremental free cash flow disproportionately toward
debt reduction and rising dividends over buybacks, and its backlog and
guidance trajectory (22% year-over-year backlog growth, raised FY2026
guidance across sales/EPS/free cash flow) is currently more constructive
than the disconfirming risks above would suggest in isolation --
genuinely two-sided evidence that a future capital-priority comparison,
not this record, would need to weigh. No price target, valuation opinion,
or buy/sell recommendation is offered.

## Uncertainty and open items (explicit, not smoothed over)

1. RTX does not disclose a specific aftermarket-margin percentage in
   these filings -- the aftermarket-driven-profit-growth statements above
   are qualitative company commentary, not a disclosed number.
2. `investors.rtx.com` timed out on every attempt -- no standalone
   investor-relations presentation deck was reviewed; every fact above is
   sourced to the three SEC filings directly opened.
3. Named-competitor claims (CFM/GE Aerospace-Safran, Lockheed Martin,
   Northrop Grumman, L3Harris) are general industry background, not
   sourced to any RTX filing -- flagged inline above.
4. The January 7, 2026 Executive Order's own text was not independently
   verified against a White House/Federal Register primary source -- it is
   reported here exactly as RTX's own 10-K describes it.
5. Deeper FY2023-versus-FY2024 Pratt & Whitney and Raytheon segment MD&A
   narrative detail (analogous to the Collins detail captured above) was
   not exhaustively extracted line-by-line for all years -- the
   FY2025-versus-FY2024 comparison is fully sourced; earlier-year detail
   for those two segments specifically is comparatively thinner in this
   record.
6. This record does not independently verify whether the external
   compliance monitor and Special Compliance Officer engagements described
   in the FY2025 10-K have proceeded on the schedule that filing
   described -- worth confirming at the next scheduled review.

## Review framework

- **Cadence: 90 days**, matching this repository's corpus-wide default.
- **Mandatory unscheduled-review triggers** (qualitative, observable): any
  new GTF-related charge or accrual reversal; any SEC enforcement action,
  penalty, or restatement tied to the powder-metal investigation; actual
  invocation, clarification, or rescission of the January 2026 Executive
  Order; a full-year defense-backlog decline; a material adverse CAS-claim
  ruling or DPA breach determination; a credit-rating downgrade;
  publication of RTX's FY2026 Form 10-K.
- **Metrics worth monitoring each review:** GTF accrual balance and AOG
  trend; defense-versus-commercial backlog mix and growth rate; segment
  operating margins (especially Pratt & Whitney); buyback pace; total
  debt and leverage ratios; dividend growth rate.

## Conviction

**Rating: Medium** -- see `RTX.yaml`'s `conviction.rationale` for the full
statement. This rating is a PROPOSED rating pending independent exact-head
review and principal acceptance; AI-assisted drafting does not itself
constitute approval.

## Sources

See `RTX.yaml`'s `sources:` block for the complete, structured source list
with dates and URLs. All three sources (FY2025 Form 10-K, Q2 2026 Form
10-Q, Q2 2026 earnings press release) were directly opened and parsed by
this session via SEC EDGAR. No secondary/aggregator source was relied upon
for any factual claim in this record; the small number of general
industry-background statements not sourced to an RTX filing (named
competitors) are explicitly flagged inline where they appear.
