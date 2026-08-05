# TSLA — Tesla, Inc.

Last updated: 2026-08-05 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0038-ws0005-gated-six-company-
intelligence-completion.md` (status: Proposed at authoring time -- not yet
independently reviewed or principal-accepted). First Company Intelligence
coverage for TSLA (no prior record existed). **Filed as one of a
six-company administrative batch** (SNPS, ICE, SPGI, WM, RKLB, TSLA) --
identical portfolio-governance status (gated under `PHQ-2026-01`,
`cash_pending_clearance`, no prior Intelligence coverage) and execution
efficiency only. The six companies share no genuine economic mechanism
and this record makes no such claim.

## Source-access disclosure

This session's `WebFetch` was attempted against nine domains (SEC EDGAR,
Tesla IR, Electrek, StockTitan, Teslarati, EVwire, CNBC, Yahoo Finance,
and en.wikipedia.org as a neutral control) and **every single attempt
returned HTTP 403**, confirming a wholesale WebFetch outage in this
environment rather than domain-specific filtering. **No primary source
document was directly read this session.** Every fact below is
`WebSearch`-tool-synthesized from secondary reporting about primary
sources, not this session's own direct reading of the 10-Q, 8-K, or IR
materials. Specific cross-source inconsistencies are flagged inline
rather than silently resolved.

## Business summary

Tesla operates three segments: **Automotive** (vehicle sales, regulatory
credits, leasing), **Energy Generation & Storage** (Megapack/Powerwall),
and **Services & Other**. [TSLA-C05] Q2 2026 (quarter ended 2026-06-30)
segment revenue: Automotive $20.52B (+23% YoY, of which regulatory
credits were $146M, -67% YoY -- see Material risks); Energy Generation &
Storage $3.14B (+13% YoY); Services & Other $4.58B (+50% YoY, described
in company materials as record profitability and margin for the
segment). Total revenue $28.24B (sources cite $28.236B-$28.24B, +26%
YoY), a record quarter beating consensus (~$28.2B).

## Recent financial results and operating detail

**Q2 2026** (reported 2026-07-22): deliveries **480,126** vehicles (Q2
record, versus an analyst estimate of ~406,600 -- this record confirms
and slightly refines this gate's own cited ">480,000" figure); energy
storage deployments **13.5 GWh** (confirms the gate's cited figure), up
53% sequentially from Q1 2026, described as the second-best quarterly
deployment and a trailing-twelve-month record. H1 2026 cumulative
(YTD): ~860K vehicles produced, ~838K delivered; 22.3 GWh storage
deployed.

**Margins**: automotive gross margin ex-credits 16.3%, down from 19.2%
in Q1 2026; energy gross margin 20.4%, down sharply from 39.5% in Q1
2026 -- attributed in secondary commentary to a vendor cell warranty
issue, non-recurring tariff benefits rolling off, and lower industrial-
storage pricing. Operating income $398M, down 57% YoY, operating margin
1.4%. Net income $1.114B; GAAP EPS ~$0.32, non-GAAP EPS $0.33, versus a
~$0.53 consensus estimate -- a miss.

**Cash flow / capex**: Q2-specific capex $5.79B (+142% YoY); free cash
flow -$1.09B (deficit) in Q2 2026 versus +$1.44B surplus in Q1 2026. A
separately-surfaced snippet citing "operating cash flow $8.634B, capex
$8.282B" appears to be an H1/YTD-cumulative figure rather than Q2-only,
given surrounding context -- **this session could not reconcile it with
confidence against the Q2-only $5.79B capex figure**, flagged as an
unresolved internal inconsistency. Cash plus short-term investments at
2026-06-30: $43.524B ($15.219B cash, $28.305B short-term investments).

**Regulatory-credit revenue collapse**: $146M in Q2 2026, down 67% YoY
from $439M and down 62% sequentially from $380M in Q1 2026 -- the lowest
quarterly credit revenue since 2020, just 0.6% of total revenue.
Full-year credit revenue fell from a 2024 peak of $2.76B to $1.99B in
2025 (-28%); the Q2 2026 figure continues and steepens that decline,
linked in secondary commentary to the expiration of the federal EV tax
credit (2025-09-30) and relaxed federal fuel-economy-penalty enforcement
reducing other automakers' need to buy Tesla's credits.

## Autonomy -- FSD and robotaxi

FSD **v14 "Lite"** began wide release to Hardware 3 (HW3) vehicles around
2026-07-21/23 -- still Level 2 supervised, not unsupervised. Tesla
confirmed (secondary reporting, April 2026) that **HW3 vehicles cannot
run unsupervised FSD** due to memory-bandwidth hardware constraints and
will remain Level 2 permanently regardless of future software -- roughly
4 million HW3 vehicles were reportedly frozen on an older FSD version
until this v14 Lite rollout. HW4 vehicles run FSD v14.3.x (Supervised) as
of June-July 2026, with some owner-reported regressions in a late-July
point release.

**Robotaxi commercial status**: operating in Austin and California, and
as of **2026-07-03** expanded to Miami -- the first driverless-service
market outside Texas/California. **Update, 2026-08-05 (SECONDARY only,
no primary source opened -- WFLA, FOX13 Tampa, Not a Tesla App, Tesla
Oracle):** Tesla reportedly launched unsupervised/driverless robotaxi
service in both **Orlando and Tampa on 2026-07-21**, 18 days after
Miami -- correcting this record's prior "softened from firm H1 2026
timelines to preparations underway" framing for those two markets,
which is now stale; the live footprint is reportedly 5 markets (Austin,
Bay Area/California, Miami, Orlando, Tampa), not 3. Separately, one
secondary source (Electrek, 2026-07-22) reports Tesla's own Q2 chart
shows paid robotaxi miles roughly flat quarter-over-quarter (~900K Q1
and Q2 alike) despite the geographic expansion -- a relevant nuance on
service scale versus geographic reach that this record does not
resolve either way. Stated company ambition: unsupervised
FSD/Robotaxi in roughly a dozen U.S. states by end of 2026 (Phoenix and
Las Vegas launches remain "preparations underway" per secondary
reporting as of this update). Safety
data (Austin, July 2025-March 2026, NHTSA data via secondary synthesis):
17 total reported incidents (13 property-damage-only, 2 no-injury, 1
minor injury without hospitalization, 1 minor injury with
hospitalization), zero "major" crashes, 6 minor contact events with the
Tesla system at-fault or partial-fault. A separate, unverified secondary
claim that robotaxis crash "4x worse than humans" on a per-mile basis is
noted but not adopted as fact -- methodology unclear.

**Regulatory/investigation status -- the largest disclosed near-term
risk cluster**: **NHTSA EA26002**, opened 2026-03-18, an engineering
analysis (the step preceding a potential recall) covering approximately
3.2 million Tesla vehicles, model years 2016-2026, examining whether
camera-only FSD fails to detect/warn the driver appropriately under
degraded-visibility conditions (glare, airborne obscurants). Secondary
reporting references "three simultaneous federal investigations into
FSD" as of mid-2026; this session could independently identify and
detail only EA26002 by name. Separately: a Cybertruck recall (wheel-
separation risk on the RWD 18" steel-wheel configuration, with the 173
affected units reportedly representing that configuration's entire
production volume); an open Model Y door-handle-failure investigation
(~174,000 units) and an open Model 3 door-release probe, both referenced
as running in parallel/unresolved, current status unconfirmed this
session; and in August 2026, NHTSA denied a petition to open a defect
investigation into 2022 Model 3 mechanical door releases but granted a
related petition to consider new federal rulemaking on industry-wide
emergency-egress systems.

## Robotics -- Optimus

A single secondary source (TechTimes, dated 2026-07-20, not
independently corroborated) reported disclosed unit production remained
essentially zero as the Q2 2026 earnings call approached -- **this
"zero" claim could not be verified against a second source and is
flagged as unconfirmed, not adopted as settled fact.** The Fremont
factory line conversion (former Model S/X production, which ended in
early May 2026) was targeted for completion in late July/August 2026, a
roughly four-month production gap. Musk (secondary-quoted, ~2026-07-01):
"Optimus production will be extremely slow at first, as everything is
new. This is not like making a car" -- and separately called the 2026
production rate "literally impossible to predict" given roughly 10,000
unique parts on an entirely new line. 2026 production targets were
reported inconsistently (50,000-100,000 units in one source; a
longer-term 1 million units/year design capacity for the converted
Fremont line and an "aspirationally 10 million units/year" target for a
planned Optimus 4 line at Gigafactory Texas, targeted for ~summer 2027
start, in another). The Optimus V3/Gen 3 reveal has been pushed back
multiple times through 2026 per contemporaneous reporting (Electrek,
2026-04-22).

**Assessment**: Optimus remains pre-commercial with a documented pattern
of schedule slippage and near-zero disclosed current output as of the
most recent reporting found -- a significant unresolved execution risk
for a program embedded directly in the CEO's own compensation-package
milestones (1 million units) and in the stock's forward narrative.

## Energy business trajectory

Storage deployments 13.5 GWh in Q2 2026 (see above), up 53% sequentially.
CFO Vaibhav Taneja is quoted (secondary) describing the 2026 backlog as
"strong, well-diversified globally," with expected growth from Megapack 3
and Mega Block launches. Shanghai Megafactory annualized run-rate ~40
GWh as of mid-2026 (its designed capacity); a new Brookshire, Texas
Megafactory under construction targets Megapack 3/Megablock production
beginning late 2026, aiming for 50 GWh/year capacity once fully ramped.
Energy segment gross margin fell to 20.4% in Q2 2026 from 39.5% in Q1
(see above) -- a material, recent, same-quarter margin swing worth
tracking rather than a settled trend.

## Capital allocation

2026 capex guidance raised to **over $25 billion** (from an earlier
~$20B figure discussed in April 2026), versus $8.5B (2025), $11.3B
(2024), $8.9B (2023) -- a large step-change in capital intensity, spread
across AI-training compute, the Austin/Giga Texas semiconductor fab,
battery/materials capacity, new solar manufacturing, and facilities
tied to a lithium refinery, LFP batteries, CyberCab, Semi, a new
megafactory, and Optimus. AI compute capacity is reported to be roughly
doubling in about six months (from ~120,000 Nvidia H100-equivalent GPUs
at end-2025 to ~280,000 by end-June 2026, secondary-sourced estimate,
not confirmed against a primary disclosure). Dojo's current operational
status is unclear from sources found this session (one source describes
it as "restarted" for "space-based AI compute"; this conflicts with
widely-reported prior deprioritization in 2025 that this session did not
re-confirm either way).

**No dividend and, per the most recent reporting found (as late as
2026-01-23), no disclosed formal company-funded share-buyback program**
at scale. Musk made ~$1B of personal open-market TSLA purchases (reported
September 2025) -- explicitly a personal transaction, not corporate
capital return.

**CEO compensation package -- material, large, and directly relevant to
the gate's "milestone framework" language**: shareholders approved a
roughly $1 trillion, 10-year compensation package for Musk (vote dated
2025-11-06 per the most reliably dated source found; some secondary
sources' date labeling was ambiguous), structured as 12 tranches of
35.3 million shares each, vesting on both market-capitalization
milestones ($2 trillion through $8.5 trillion, in $500B/then $1T
increments) and operational milestones: **20 million cumulative
vehicles delivered, 10 million paid FSD subscriptions, 1 million
Optimus robots produced, 1 million commercial robotaxis operating for
3+ consecutive months, and a cumulative adjusted-EBITDA target scaling
from $50 billion to $400 billion annually.** Could raise Musk's
ownership stake to as much as 29%. Norway's Norges Bank and proxy
advisors Glass Lewis/ISS opposed the package citing dilution, size, and
insufficient mitigation of key-person risk; a shareholder derivative
suit alleging fiduciary breach (diversion of AI resources to Musk's
other ventures, e.g. xAI/SpaceX) is reported as pending, current status
unconfirmed. **This is the closest identified analog to this gate's own
"accepted milestone framework" language** -- but this record explicitly
flags that identifying it as the specific framework the gate's author
had in mind is an inference, not a verified fact; no verbatim Tesla-
stated "milestone framework" phrase matching the gate's own wording was
found.

## Competitive position

**US**: Tesla's US EV market share reportedly jumped from 41% (Q3 2025)
to 59% (Q4 2025/early 2026), attributed to the federal tax credit's
expiration disproportionately hurting smaller/less-scaled competitors
rather than necessarily reflecting Tesla-specific demand strength.
**[UNVERIFIED-CONFLICT, flagged 2026-08-05 following independent
review]**: this quarter-over-quarter swing was originally stated with
more confidence than the underlying single-aggregator sourcing supports,
unlike comparably-sourced claims elsewhere in this record (China,
Optimus) which are already flagged. A targeted re-check this session
found additional, seemingly conflicting figures from other secondary
sources: Tesla held **~46% of the full-year 2025** US EV market (down
from ~49% in 2024, per one source), and **~54.2%** in Q1 2026 (per
another) -- readings that, taken together with the 41%/59% quarterly
swing, are not necessarily contradictory (full-year averages smooth over
quarter-specific spikes/troughs) but were not reconciled into one
consistent trend line this session. The directional takeaway -- a real
Q4 2025 spike plausibly tied to the tax-credit-expiration timing effect,
sitting within a longer-run full-year share that appears to be
gradually declining (49%→46%) rather than straightforwardly rising --
should be treated as this session's own inference from partial,
unreconciled secondary data, not a verified fact. Rivian's R2 SUV (2026
launch) is flagged in secondary commentary as "the biggest near-term
threat to Model Y." **Update, 2026-08-05 (WS-0005 Milestone-6-prerequisite-2
freshness check, SECONDARY only, no primary source opened):** one
further data point was found and added to the trend line -- Tesla's
**Q2 2026 US EV share reportedly 50.5%** (CleanTechnica, 2026-07-22),
sitting between the FY2025 figure (46%) and the Q1 2026 figure (54.2%)
above. This fills in the quarterly trend (FY2025 46% -> Q1 2026 54.2%
-> Q2 2026 50.5%) but does **not** reconcile against the original,
still-uncorroborated 41%-to-59% Q3/Q4 2025 claim, whose sourcing/
methodology remains unidentified -- this conflict is confirmed still
open, not resolved, after this session's own re-check (no primary
source, e.g. Cox Automotive or EIA, was reachable).

**Global/China**: global EV-leadership figures were inconsistent across
sources and could not be reconciled from search snippets alone (unit
counts versus share percentages, measured over different windows,
possibly BEV-only versus all-NEV). China-specific figures showed a
similar tension: "wholesale EV sales rise 38% in July 2026" versus a
separately reported "fifth successive quarterly [delivery] retreat"
pulling China's share of Tesla's global volume below 30% for the first
time since Q4 2020 -- **these two figures could not both describe the
same metric/period and were not reconciled this session**, likely
reflecting a wholesale/export-versus-domestic-delivery distinction.
Local competition intensified regardless of which figure is emphasized:
BYD July 2026 wholesale NEVs 419,211 units (+21.76% YoY); Leapmotor
crossed 100,000 units/month in July 2026, surpassing Tesla China's
monthly tally for a second consecutive month; Geely's Xingyuan reportedly
outsold both Tesla and BYD models in February 2026.

**Europe**: 13-plus consecutive months of year-over-year registration
declines through January 2026 (-17% YoY that month), full-year 2025
EU+EFTA+UK registrations down 27% to 238,656 units -- occurring while
the broader European BEV market grew (+13.9% YoY in January 2026), i.e.,
Tesla-specific share loss rather than a market-wide slowdown. BYD Europe
registrations +165% YoY over the same period, off a small base
(0.7%→1.9% share).

**Moat characteristics**: the Supercharger network (see Business
summary/Competitive-advantages) is the most concretely evidenced moat
element found this session; vertical integration and an FSD/fleet-data
advantage are commonly cited in secondary commentary but this session
found no new, dated, primary evidence quantifying either.

## Material risks

1. **Regulatory-credit revenue collapse** -- structural tailwind
   reversal, not a one-quarter blip (see Recent financial results).
2. **Automotive and energy margin compression** in the most recent
   quarter, alongside a swing to negative free cash flow against sharply
   rising capex.
3. **Autonomy regulatory/safety risk** -- NHTSA EA26002 (~3.2M vehicles)
   is the single largest disclosed overhang; multiple additional open
   recalls/investigations (Cybertruck wheels, Model Y/Model 3 door
   handles).
4. **HW3 fleet obsolescence for unsupervised autonomy** -- a real,
   structural technical/customer-promise gap for roughly 4 million
   vehicles.
5. **Optimus execution risk** -- near-zero (unconfirmed single-source)
   disclosed production, repeated reveal delays, management's own
   "impossible to predict" framing, embedded directly in CEO
   compensation milestones.
6. **Regional demand pressure** -- Europe (sustained decline into a
   growing category) and China (declining domestic share amid
   intensifying local competition), even as the US shows apparent
   tax-credit-timing-driven share gains.
7. **Extreme valuation dependence on unproven businesses** -- made
   explicit by the CEO pay package's own milestone structure (robotaxi,
   Optimus, FSD subscriptions) rather than current auto/energy earnings.
8. **Dilution** -- up to ~29% potential Musk ownership stake and 12
   tranches of 35.3M shares each under the pay package if fully vested.
9. **Key-person/governance risk** -- Musk simultaneously runs Tesla,
   SpaceX, xAI, X, Boring Company, and Neuralink; a pending shareholder
   derivative suit alleges fiduciary breach via diversion of AI
   resources to his other ventures, current status unconfirmed.
10. **This session's own weak source access** -- no primary document
    directly opened; several figures internally inconsistent across
    sources (see disclosure above).

## Relationship to the gate

`gates.yaml`'s stated rationale: "Vehicle and storage scale are
substantial, but the small target depends on autonomy, energy, robotics,
capital allocation, and valuation milestones rather than current
deliveries alone." `next_gate`: "Activate only under the accepted
milestone framework and a fresh valuation review." This record confirms
and slightly refines the gate's own cited Q2 2026 figures (480,126
deliveries, 13.5 GWh storage). It independently supports the gate's
central framing: current-quarter operating margin (1.4%) and negative
free cash flow (-$1.09B) sit well below a scale that would obviously
justify a large target weight on present earnings alone, and every named
forward driver (autonomy, energy margin durability, Optimus, capital
allocation) carries live, currently-unresolved uncertainty documented
above. This record could not identify a verbatim Tesla-stated "milestone
framework" matching the gate's own phrase -- the CEO compensation
package's own operational-milestone structure is the closest identified
analog, offered explicitly as an inference, not a confirmed match. This
record does not resolve when the gate's `next_gate` condition will be
satisfied.

## Investment thesis (descriptive, no recommendation)

**Concise statement:** Tesla's current-period vehicle and energy-storage
scale is genuinely large and, on some metrics, record-setting, but
current-period profitability is thin and under fresh pressure (margin
compression, negative free cash flow, collapsing regulatory-credit
revenue), while the forward valuation case rests heavily -- by the
company's own governance structure -- on autonomy, robotics, and energy
milestones that remain substantially unproven as of this record's
authoring date.

**Conditions that would support initiation**: sustained automotive/
energy margin recovery; positive resolution (or at least de-risking) of
the NHTSA EA26002 investigation; visible, verified Optimus production
ramp; continued robotaxi geographic expansion without a material safety
incident; a valuation re-rating consistent with actual (not merely
promised) milestone progress.

**Conditions that would argue for continued caution**: an adverse NHTSA
EA26002 finding or recall; a material Optimus or robotaxi safety
incident; continued regional (Europe/China) share loss; further margin
compression without a clear recovery path; continued near-zero Optimus
production well past the Fremont line's targeted completion.

## Uncertainty and open items (explicit, not smoothed over)

1. No primary source was directly opened this session.
2. Q2-only versus H1-cumulative capex/operating-cash-flow figures could
   not be reconciled.
3. Segment-level gross profit in dollar terms (not just margin
   percentages) was not found.
4. The exact number and names of "three simultaneous federal FSD
   investigations" -- only EA26002 was concretely identified.
5. Current status (open/closed/resolved) of the Model Y and Model 3
   door-handle-related probes -- not confirmed.
6. Dojo's current operational status -- conflicting/unclear signal.
7. The China wholesale-sales-growth versus delivery-decline contradiction
   -- not resolved.
8. The CEO pay-package vote date -- treated as 2025-11-06 based on the
   most reliably dated source, but some secondary references were
   ambiguous.
9. Exact Q3 2026 earnings date -- unconfirmed by Tesla.
10. The single-source "Optimus production remains zero" claim -- not
    independently corroborated.

## Review framework

- **Cadence: 90 days**, matching this repository's corpus-wide default.
- **Mandatory unscheduled-review triggers**: any NHTSA EA26002
  development or recall determination; a confirmed Optimus production
  figure (positive or negative surprise); any material robotaxi safety
  incident; a material change to automotive or energy gross margin
  trend; any CEO pay-package milestone achievement or reversal.
- **Metrics worth monitoring each review**: automotive/energy gross
  margin trend; free cash flow; regulatory-credit revenue run rate;
  Optimus production figures once available; robotaxi state-by-state
  expansion progress; Europe/China delivery trend.

## Conviction

**Rating: Medium** -- see `TSLA.yaml`'s `conviction.rationale` for the
full statement. This is a PROPOSED rating pending independent exact-head
review and principal acceptance; AI-assisted drafting does not itself
constitute approval.

## Sources

See `TSLA.yaml`'s `sources:` block for the complete, structured source
list. In summary: Tesla's own Q2 2026 shareholder deck/earnings release
and the CEO compensation-package vote disclosure, all identified via
WebSearch snippets and not directly opened this session; NHTSA
investigation coverage; secondary/aggregator and trade-press sources
(Electrek, Teslarati, InsideEVs, regional registration-data aggregators)
used for autonomy, robotics, and regional-competitive context, explicitly
labeled secondary throughout and never conflated with a primary-source
fact.
