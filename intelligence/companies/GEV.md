# GEV — GE Vernova Inc.

Last updated: 2026-07-23 -- bounded corrective pass on draft PR #132,
addressing an independent review of the 2026-07-22 evidence-only
refresh (itself implemented under
`governance/decisions/PI-0020-gev-intelligence-refresh-authorization.md`,
following the `PI-0019` committee review's principal-approved
"Intelligence refresh recommended" conclusion). Original record created
2026-07-18 through AI-assisted research and drafting, finalized through
explicit human review and approval under `PI-0007` -- Portfolio HQ's
fourth Portfolio Intelligence record, and the second of two records
created under the `ai_infrastructure` Theme Intelligence pilot
(`decision_log.yaml` PI-0006/PI-0007). This corrective pass is
evidence-accuracy-only: it does not change `review.last_reviewed` or
`review.next_due` (both still represent the 2026-07-22 evidence-refresh
cycle, per `review.log`), and it does not change `conviction.rating`.

## Source-access disclosure

Direct rendering of GE Vernova's primary documents has not been
achieved in this research environment across any pass on this record
(2026-07-18 original, 2026-07-22 refresh, or this 2026-07-23 corrective
pass). This section names exactly what was attempted rather than making
an undifferentiated blanket claim, per this pass's own reassessment:

- **SEC EDGAR** -- retested 2026-07-23: `www.sec.gov` root, the
  `data.sec.gov/submissions/...` filing-index API, and the specific Q1
  2026 and Q2 2026 8-K/10-Q exhibit URLs cited in `sources[]` below (both
  the PDF and, where available, the HTML exhibit form). All returned
  HTTP 403.
- **`gevernova.com`** -- retested 2026-07-23: site root, the investor-
  relations landing page, and the specific press-release URLs cited in
  `sources[]` below. All returned HTTP 403.
- **A reader-proxy workaround** (routing a primary SEC URL through a
  third-party text-extraction relay, attempted only in this
  2026-07-23 pass as an additional avenue) -- also returned HTTP 403.
- **Representative secondary syndication outlets** (Benzinga,
  MarketScreener, TradingView, StockTitan, Yahoo Finance, BusinessWire,
  Morningstar, BNN Bloomberg) -- retried in the 2026-07-22 pass and
  spot-retested in this 2026-07-23 pass. All returned HTTP 403 to this
  repository's direct-fetch tooling.

This is a genuine, repeatedly retested limitation of this session's
direct-fetch tooling against these specific hosts, not a narrowed
description standing in for a broader one -- every host actually
attempted, across all three passes, failed identically. It is the same
access pattern already disclosed in COST's and XOM's records. **What
does succeed, and is the actual evidentiary basis for every factual
claim in this record:** a separate search-and-synthesis capability that
retrieves and quotes source content server-side even when this
repository's own direct-fetch tooling cannot render the page. Every
material figure below is corroborated across **multiple independent
secondary outlets per claim** (cross-checked, not single-sourced) via
that capability, including, where the underlying primary document's own
exact wording could be located through it (e.g. the Q1 2026 Wind
segment-EBITDA guidance language, the FY2025 orders description, and
the December 2025 dividend/buyback figures), direct quotation of that
primary wording -- see the per-entry notes in `sources[]` for which
claims reach that standard. This caveat applies once, to the whole
record, and is not repeated per figure below. An earlier draft of the
underlying research also asserted a specific Power-segment-only backlog
figure (~$94.4 billion) that could not be independently reconfirmed and
was withdrawn prior to the 2026-07-18 approval -- it does not appear
anywhere in this record.

**Explicit correction from the 2026-07-22 refresh, unchanged by this
pass:** the prior (2026-07-18) version of this record stated that
management's ~$200 billion total-backlog target "predates, and was not
accelerated by, the Q1 2026 results." That statement was incorrect.
Multiple independent secondary sources describing the Q1 2026 earnings
call (reported 2026-04-22) confirm management accelerated the target
from year-end 2028 to year-end 2027 at that call, reaffirmed at the Q2
2026 call. The 2026-07-22 refresh corrected the record rather than
silently editing over the error -- see the Catalyst section below and
the corresponding `sources[]` entry.

**Corrections made in this 2026-07-23 pass** (full detail in each
affected section below and in `GEV.yaml`'s `review.log`): (1) the
FY2025 $59.3 billion orders figure, mislabeled since the original
2026-07-18 record as "Power/Electrification orders," is corrected to
total-company orders, led by equipment at Power and Electrification and
services in each segment; (2) an independent reviewer's proposed
EBIT/EBITDA relabeling of the Wind segment loss figures was
investigated against primary-source-quoted language and **rejected** --
the metric is segment EBITDA, as this record already stated throughout,
and no basis-mismatch caveat has been added; (3) the Wind/European
Electrification margin-softness risk's `identified` date, incorrectly
moved to 2026-07-22 by the prior refresh, is restored to its true
original value of 2026-07-18; (4) two literal "SS" encoding artifacts
(intended as the section symbol, §) are corrected.

## Business summary

GE Vernova supplies power-generation and electrification equipment (gas
turbines, grid/electrification products) into a demand environment that
includes, but is not limited to, AI data-center power buildout. Fiscal
year 2025: total-company orders of $59.3 billion (up 34% organically,
led by equipment at Power and Electrification and services in each
segment -- corrected 2026-07-23; an earlier version of this record
inaccurately described this figure as "Power/Electrification orders"),
total backlog $150 billion (+$31.2 billion year-over-year), revenue
$38.1 billion, net
income $4.9 billion (including a $2.9 billion tax benefit). Q1 2026: the
Electrification segment booked $2.4 billion in equipment orders
supporting data centers alone -- more than all of 2025 combined -- and
total company backlog grew more than $13 billion quarter-over-quarter,
to $163 billion.

**Q2 2026 (reported 2026-07-22):** revenue $11.1 billion (+22% total,
+12% organic), orders $24.2 billion (+88% organic), total backlog $176
billion (+$13 billion sequentially from Q1's $163 billion), GAAP net
income $649 million, GAAP diluted EPS $2.47, adjusted EBITDA $1.25
billion (11.3% margin, up from $770 million/8.5% margin in Q2 2025),
free cash flow $5.1 billion (up from $194 million in Q2 2025), and a
cash balance of $13.1 billion at quarter-end (+$4.3 billion
year-to-date). Management raised FY2026 guidance to revenue $45.5-46.5
billion (from $44.5-45.5 billion guided at Q1) and free cash flow
$11.5-12.5 billion (from $6.5-7.5 billion guided at Q1).

Segment detail, Q2 2026:
- **Electrification:** revenue $3,637 million, 18.4% EBITDA margin;
  orders $6.3 billion, book-to-bill approximately 1.7; equipment backlog
  $40.6 billion, +69% year-over-year, including $5 billion from the
  Prolec GE acquisition; more than $5 billion of first-half 2026
  data-center orders (Q1 $2.4B + Q2 $2.7B).
- **Power:** revenue $5,477 million, 18.8% EBITDA margin; orders $16.7
  billion, +134% organic, driven by gas power equipment; gas equipment
  backlog and slot-reservation agreements grew from 100 GW (Q1 2026) to
  116 GW (Q2 2026), with management targeting at least 125 GW under
  contract by year-end 2026.
- **Wind:** orders $1.2 billion, -40% organic (lower Onshore Wind
  equipment orders, primarily North America); EBITDA loss $275 million,
  -13.6% margin (vs. -7.3% a year earlier). See Risks below for the
  full Wind detail, including the Q1 2026 comparison and Q3 2026
  outlook.

## Investment thesis (business-quality description, not a
recommendation)

**Concise statement:** GE Vernova is a large-scale power and
electrification equipment supplier with reported, growing order and
backlog exposure to AI data-center power demand, operating in a
business whose execution risk centers on large, long-cycle,
fixed/competitively-bid contracts, with a distinct and continuing Wind
segment drag.

**Expanded narrative:** the Electrification segment's data-center order
figures ($2.4 billion in Q1 2026, a further $2.7 billion in Q2 2026,
more than $5 billion combined for H1 2026) are concrete, dated, sourced
growth signals distinct from the company's broader backlog growth. The
FY2025 total backlog figure ($150 billion, +$31.2 billion year-over-year)
grew to $163 billion by Q1 2026 and $176 billion by Q2 2026 -- a company
converting demand into booked orders at an accelerating scale, reflected
in management's own decision to pull forward its ~$200 billion
total-backlog target by a full year (year-end 2028 to year-end 2027).
Backlog is not revenue, though, and conversion pace carries its own
disclosed execution risk (see Risks below). The Power segment's gas
equipment backlog and slot-reservation growth (100 GW to 116 GW in one
quarter, against a 125 GW year-end target) is a second, distinct demand
signal, largely independent of the Electrification segment's
data-center narrative. Set against this demand strength, the Wind
segment's EBITDA losses widened in dollar terms through H1 2026 (Q1
-$382 million, Q2 -$275 million) even as its margin improved
sequentially (-26.7% to -13.6%) -- management's own framing, reported
through secondary sources, is that H1 2026 Wind orders shipped with
weaker tariff protection than H2 2026 orders will carry, and that Q3
2026 Wind EBITDA is expected to be approximately break-even. This is a
real, disclosed, ongoing drag on the business's overall profitability,
not a resolved issue.

**Conditions relevant to monitoring this thesis** (qualitative,
observable -- no arbitrary numerical threshold, consistent with
PI-0004's precedent for COST/XOM):
- Electrification segment data-center order flow continues at or
  above recently reported levels, without a material, sustained
  reversal
- Total backlog continues growing or is converted to revenue at a
  pace consistent with recent disclosure, including progress toward the
  accelerated ~$200 billion by year-end 2027 target
- No material, disclosed deterioration in Wind or European
  Electrification margins beyond what is already flagged -- the Q3 2026
  "approximately break-even" Wind EBITDA outlook (secondary-reported)
  is itself a condition to watch for confirmation or reversal
- Progress toward the Power segment's stated 125 GW year-end-2026
  gas-equipment-backlog-and-slot-reservation target continues to be
  disclosed on pace

**Conditions that would weaken confidence in the above** (analytical
judgment, qualitative and observable, no numerical trigger):
- A material, sustained decline in Electrification segment
  data-center order flow
- Evidence of material backlog-to-revenue conversion failure (orders
  booked but not converting to delivered revenue on a reasonable
  timeline)
- A material, disclosed supply-chain-driven project delay
- A material further deterioration in Wind or European Electrification
  margins, including a failure of the guided Q3 2026 approximately
  break-even Wind EBITDA outlook to materialize
- A material, disclosed integration setback in the Prolec GE
  acquisition

## Capital allocation

Two capital-allocation actions and one acquisition, none previously
captured in this record, are added by this refresh (PI-0020 §C):

- **Dividend and buyback (December 2025).** At its December 9, 2025
  investor update, GE Vernova's Board declared a quarterly dividend
  increase to $0.50/share (from $0.25/share), payable 2026-02-02 to
  holders of record 2026-01-05, and increased the share-repurchase
  authorization to $10 billion (from $6 billion) -- approximately $3.3
  billion of the prior authorization had been spent as of 2025-12-03.
- **Prolec GE acquisition (closed 2026-02-02).** GE Vernova completed
  the acquisition of the remaining 50% stake of Prolec GE, an
  electrical-equipment manufacturer previously held as a 30-year,
  50/50 joint venture, for $5.275 billion, funded with an equal mix of
  cash and debt. This was GE Vernova's first major acquisition since
  becoming a standalone public company. Prolec GE now operates within
  the Electrification segment and contributed $5 billion to that
  segment's Q2 2026 equipment backlog.
- **Senior notes offering (closed 2026-02-04).** GE Vernova closed a
  $2.6 billion, three-tranche public senior-notes offering ($600
  million 4.250% due 2031; $1.0 billion 4.875% due 2036; $1.0 billion
  5.500% due 2056), used in part to fund the Prolec GE acquisition.

**Balance-sheet note, disclosed limitation:** this refresh could not
directly render GE Vernova's Q2 2026 10-Q (HTTP 403). Secondary sources
corroborate total long-term borrowings excluding finance leases of
approximately $2.6 billion following the February 2026 notes issuance;
the Q1 2026 10-Q separately disclosed total long-term borrowings of
$2,806 million (including $314 million of other long-term borrowings
and finance leases). This record does not claim independent primary
verification of the exact Q2 2026 balance-sheet debt line item -- it is
presented as secondary-corroborated, consistent with this record's
access-limitation disclosure above.

## Competitive advantages — detail

*(YAML holds concise claims only, per the frozen schema; fuller
evidence lives here.)*

1. **Large, reported backlog scale, growing and accelerating.**
   Evidence: FY2025 total backlog of $150 billion (+$31.2 billion
   year-over-year), $163 billion by Q1 2026, $176 billion by Q2 2026
   (+$13 billion sequentially). Management's own ~$200 billion
   total-backlog target moved a full year earlier (year-end 2028 to
   year-end 2027) between the December 2025 investor update and the
   Q1 2026 call, reaffirmed at Q2. Limitation: backlog is a
   booked-order figure, not revenue; conversion pace and timing carry
   their own disclosed execution risk (see Risks).
2. **Reported data-center-specific demand concentration.** Evidence:
   $2.4 billion in Electrification-segment equipment orders supporting
   data centers in Q1 2026 alone (more than all of 2025 combined), and
   a further $2.7 billion in Q2 2026 alone -- more than $5 billion for
   H1 2026 combined. Limitation: these figures are corroborated across
   multiple independent secondary outlets, not directly rendered by
   this repository's tooling in this pass; two strong quarters are
   stronger evidence of a trend than the original record's single
   quarter, but still not a multi-year track record.
3. **Power segment gas-equipment contracting momentum.** Evidence: gas
   equipment backlog and slot-reservation agreements grew from 100 GW
   (Q1 2026) to 116 GW (Q2 2026), against a management target of at
   least 125 GW under contract by year-end 2026. Limitation: a slot
   reservation is not an equipment order; conversion of reservations to
   firm orders and eventual revenue carries its own timing risk, not
   separately quantified here.
4. **Raised FY2026 financial guidance.** Evidence: revenue guidance
   raised to $45.5-46.5 billion (from $44.5-45.5 billion guided at Q1,
   itself raised from a December 2025 baseline) and free cash flow
   guidance raised to $11.5-12.5 billion (from $6.5-7.5 billion guided
   at Q1). Limitation: guidance is management's own forward estimate,
   not a certainty, and this record does not treat a guidance raise as
   validated performance.

## Risks — detail

Category framing (not a schema field, recorded here only, same
convention COST's and XOM's records established):
- Large-project execution risk: operational/structural -- the defining
  risk of a long-cycle, fixed/competitively-bid equipment business
- Supply-chain dependency: operational/structural
- Wind/European Electrification margin softness: operational,
  currently reported as a continuing headwind distinct from stronger
  segment performance elsewhere
- Data-center order-flow reliance: commercial/structural
- Tariff exposure: commercial/regulatory, newly added by this refresh

**Important limitation, disclosed explicitly, unchanged from the
original record:** the specific enumerated risk-factor text of GE
Vernova's own Form 10-K was not independently inspected in either
research pass. The five risk categories above are understood from
general secondary coverage of GE Vernova's disclosed condition, not
confirmed word-for-word against GE Vernova's own filed risk-factor
language. This limitation is carried forward, not resolved, by this
refresh.

**Wind segment detail (this refresh's most substantive addition).**
Wind EBITDA losses widened in dollar terms through H1 2026: $382
million in Q1 2026 (-26.7% margin, vs. -$146 million/-7.9% margin a
year earlier) and $275 million in Q2 2026 (-13.6% margin, vs. -7.3% a
year earlier) -- so the loss narrowed sequentially quarter-over-quarter
even as it remains larger, in both quarters, than the prior-year
comparable period. Management maintained FY2026 Wind EBITDA-loss
guidance of approximately $400 million at both the Q1 and Q2 2026
calls. Reported through secondary sources (official transcript,
prepared remarks, and webcast replay were not directly inspected in
this research pass -- HTTP 403 on every attempted primary fetch): CFO
Ken Parks guided Q3 2026 Wind revenue to decline at a low-double-digit
rate year-over-year with segment EBITDA approximately break-even, and
characterized H1 2026's weaker results as reflecting equipment shipped
under contracts signed before current tariff conditions, with H2 2026
shipments carrying better tariff protection.

**Committee arithmetic, explicitly labeled (not company guidance):**
summing the two separately company-reported quarterly losses ($382M +
$275M) gives a cumulative H1 2026 Wind EBITDA loss of approximately
$657 million. If the approximately $400 million FY2026 loss guidance
holds, that implies approximately $257 million of positive H2 2026 Wind
EBITDA ($657M H1 loss less $400M FY loss). **GE Vernova did not guide
to, and this record does not assert, any specific positive-dollar-amount
H2 2026 Wind EBITDA figure** -- the $257 million figure is this
repository's own arithmetic on company-reported inputs, presented here
once, clearly labeled, per PI-0020 §D.2, and must not be read or cited
elsewhere as management guidance.

**Tariff exposure (newly added by this refresh).** Management's net
2026 tariff-impact estimate was $100-200 million as of the Q2 2026
call, down from a $250-350 million estimate given at Q1 2026. The
current, lower estimate is the operative figure; the Q1 estimate is
retained here as history, consistent with PI-0020 §C's instruction to
retain the superseded estimate rather than silently drop it.

Observable indicators worth monitoring: quarterly Electrification
segment data-center order flow, total backlog level and growth rate,
backlog-to-revenue conversion pace, Wind segment quarterly EBITDA
dollar loss and margin against the Q3 2026 approximately-break-even
outlook and the ~$400M FY2026 guide, and the realized 2026 tariff
impact against the current $100-200M estimate.

## Catalyst

Management's total-backlog target of approximately $200 billion,
**accelerated from year-end 2028 to year-end 2027.** The original
year-end-2028 target was set at the December 2025 investor update and
was described in this record's original (2026-07-18) version as
unaffected by the Q1 2026 results -- that description is now known to
be incorrect. Multiple independent secondary sources describing the Q1
2026 earnings call (reported 2026-04-22) report management moving the
target a full year earlier, to year-end 2027, citing accelerating
backlog growth; the Q2 2026 call reaffirmed the 2027 target against a
$176 billion backlog already on hand. Expected: 2027-12-31, genuinely
tied to management's own restated target date, reported through
secondary sources (primary transcript not directly inspected in this
research pass). No other catalyst is included in this record; continued
quarterly order/backlog disclosure is directionally relevant but
carries no confirmed forward date of its own.

## Review framework

- **Cadence: 90 days**, unchanged by this refresh. Matches COST's and
  XOM's cadence, and the `ai_infrastructure` theme's own cadence.
- **Unscheduled-review triggers** (qualitative, observable, same
  pattern COST's and XOM's records established) -- unchanged by this
  refresh, though the Q2 2026 Wind margin deterioration is itself an
  instance of the second trigger below, which is the reason this
  refresh exists:
  - A material, sustained decline in Electrification segment
    data-center order flow
  - A material backlog-to-revenue conversion failure
  - A material, disclosed supply-chain-driven project delay
  - A material further deterioration in Wind or European
    Electrification margins
  - A significant leadership change
- **Metrics worth monitoring each review:** quarterly Electrification
  segment data-center orders, total backlog level and growth (against
  the accelerated ~$200B-by-2027 target), backlog-to-revenue conversion
  pace, Wind/European Electrification margin trend (against the Q3 2026
  approximately-break-even guide and ~$400M FY2026 guide), and realized
  2026 tariff impact (against the current $100-200M estimate).

## Conviction

**Rating: Medium** -- unchanged from the original 2026-07-18 record.
This refresh does not change, and was not authorized to change, this
rating. `PI-0020`'s approved advisory-policy conclusion for GEV is "Keep
current policy," and any future rating change requires its own separate
human approval per `PI-0004`'s closed four-value vocabulary.

**Rationale:** GE Vernova's demand signal has continued to build through
Q2 2026: FY2025 total-company orders ($59.3B, +34% organic), total backlog reaching
$176B by Q2 2026 (from $150B at FY2025), Q2 2026 orders of $24.2B (+88%
organic), and cumulative H1 2026 Electrification data-center orders
exceeding $5B all reflect real, demonstrated demand tied to the
AI-infrastructure power buildout, reinforced by a Q2 2026 guidance raise
(FY2026 revenue to $45.5-46.5B, free cash flow to $11.5-12.5B).
Conviction is Medium rather than High because the company's own
disclosed risk profile centers on execution across large, long-cycle,
fixed/competitively-bid contracts, with margin softness specifically
flagged in Wind and European Electrification -- Wind's EBITDA losses
widened further in H1 2026 (Q1 -$382M, Q2 -$275M) even as management
maintained its ~$400M FY2026 Wind loss guidance, and 2026 tariff
exposure, while reduced from the Q1 2026 estimate, remains a live,
disclosed cost. This rating explicitly excludes valuation, entry-price,
allocation, trading, and margin judgments.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and
drafting process does not itself constitute the human judgment this
record requires; the approval decision does. The 2026-07-22 refresh
updates the rationale's supporting evidence only, under `PI-0020`'s
explicit authorization to preserve `conviction.rating: Medium` as
baseline; it does not itself constitute a new conviction judgment. The
2026-07-23 corrective pass changes only the orders-description wording
above (total-company orders, not "Power/Electrification orders") and
does not touch the rating or otherwise alter this rationale's
substance.

## Theme membership

References the `ai_infrastructure` Theme Intelligence record
(`intelligence/themes/ai_infrastructure.yaml`/`.md`). GEV is
independently a member of `targets.yaml`'s `power_infra` correlation
cluster -- a different cluster than NVDA's `semis`, and a different
kind of information than this narrative theme reference. Per PI-0006's
frozen one-way-authority model, this file references the theme; the
theme file does not reference GEV back. Theme membership does not
imply anything about GEV's allocator treatment, tier weight, or
cluster-cap status, all of which remain governed exclusively by
`targets.yaml`. Unchanged by this refresh.

## Unresolved items and access limitations (this refresh, and the
2026-07-23 corrective pass)

- Direct primary-source rendering (SEC EDGAR, `gevernova.com`, and
  every secondary outlet URL cited above) remained HTTP 403-blocked
  throughout the 2026-07-22 refresh and was retested and reconfirmed
  blocked in the 2026-07-23 corrective pass -- see the Source-access
  disclosure section at the top of this file for the exact hosts and
  methods retested. Every claim in this record is corroborated across
  multiple independent secondary outlets rather than independently
  primary-read, though several claims reach direct quotation of the
  primary document's own language via a search-and-synthesis capability
  that succeeds even when this repository's direct-fetch tooling does
  not -- see `sources[]` for which entries reach that standard.
- Two items raised by an independent review and investigated in the
  2026-07-23 corrective pass are now resolved, not open: whether the
  FY2025 $59.3B figure is "Power/Electrification orders" or
  total-company orders (resolved: total-company orders, corrected
  throughout this record); and whether the Wind segment loss figures
  should be relabeled from EBITDA to EBIT (resolved: EBITDA is correct,
  confirmed against the primary filing's own quoted language -- no
  relabeling made).
- The exact Q2 2026 10-Q total-long-term-borrowings-excluding-finance-
  leases figure (~$2.6B) is secondary-corroborated only, not
  independently confirmed against the primary balance sheet line item
  in this pass -- see the Capital allocation section's balance-sheet
  note above.
- The Q2 2026 earnings-call Wind commentary (Q3 outlook, H1/H2
  framing) is reported through secondary sources only; the official
  transcript, prepared remarks, or webcast replay were not directly
  inspected, per this record's mandatory secondary-reported provenance
  labeling for that content (`PI-0020` §D.1).
- This implementation was not supplied with, and does not rely on, the
  `PI-0019`/`PI-0020` committee review packet's own text or its
  specific numbered unresolved-evidence items (UNRES-01, -02, -04,
  -07, -08, -10 per `PI-0020`'s Context section). Consistent with
  `PI-0020` §D.3's instruction not to silently resolve or discard
  unresolved evidence, this implementation makes no claim about their
  status, content, or resolution one way or the other -- they remain
  wherever the packet itself left them, outside this repository.
  Nothing in this refresh should be read as confirming, resolving, or
  superseding any packet-level unresolved item this record does not
  itself discuss.
- Per `PI-0020` §D.3's binding exclusion list, this refresh does not
  include: any Barclays/Siemens Energy peak-cycle argument; any
  GAAP-EPS-versus-consensus comparison (several secondary outlets
  characterized Q2 2026 results as a "profit miss" against estimates --
  that framing is deliberately excluded here); insider-selling reports;
  the May 2026 permitting commentary; unverified customer-concentration
  percentages; turbine-market-share figures; or any share-price-reaction
  observation (several secondary outlets described post-earnings share
  price moves -- deliberately excluded here as well).

## Sources

See YAML `sources[]` for the structured register -- two primary-
document citations carried forward from the original record (GE
Vernova's Q4/FY2025 and Q1 2026 results releases; both had their notes
amended, not their underlying claims changed, in the 2026-07-23
corrective pass -- the Q4/FY2025 note's orders description was
corrected from "Power/Electrification orders" to total-company orders,
and the Q1 2026 note gained the Wind segment-EBITDA primary-language
citation), plus six new entries added by the 2026-07-22 refresh (the Q1
2026 earnings-call backlog-acceleration correction, the December 2025
investor-update capital-allocation press release, the Prolec GE
acquisition/senior-notes closing press release, the Q2 2026 Form 8-K
results, the Q2 2026 Form 10-Q balance-sheet/tariff citation, and the
Q2 2026 earnings-call Wind commentary with its mandatory
secondary-reported provenance labeling). Every entry discloses that
direct rendering was blocked in the research environment, per the
disclosure above, which also names the specific hosts and methods
retested in the 2026-07-23 pass.
