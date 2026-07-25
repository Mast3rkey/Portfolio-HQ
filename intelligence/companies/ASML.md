# ASML — ASML Holding N.V.

Created 2026-07-25 under `governance/decisions/PI-0023-ws0005-milestone3-batch1-semis-equipment.md`
(WS-0005 Milestone 3, Batch 1 — ASML, AMAT, KLAC, LRCX, the semiconductor
capital-equipment sub-segment of `targets.yaml`'s governed `semis` cluster).
Portfolio HQ's eighth Company Intelligence record, and the first of this
four-company batch.

## Source-access disclosure

**Research cutoff for this record: 2026-07-25.** This implementation session
attempted direct WebFetch access to ASML's own investor-relations pages
(`asml.com`), SEC EDGAR, and GlobeNewswire, and every attempt returned an
HTTP 403 — the same network-access-limitation pattern already disclosed in
this repository's NVDA and GEV records. Every figure in this record is
therefore sourced via WebSearch result synthesis of those primary documents
(cross-corroborated across multiple independent secondary outlets where
possible), not independently read from primary filing text by this session.
Where a figure is well-corroborated across multiple independent sources it
is presented with reasonable confidence; where sources genuinely disagree,
that disagreement is stated explicitly below rather than silently resolved
in either direction — per this repository's "no unsupported snippet
presented as inspected primary evidence" discipline (`PI-0023` SSD).

**Unresolved data conflicts found in research, not resolved by this
record:**
- Customer-concentration figures (TSMC ~24% of net sales, top-two ~38%,
  top-ten >80%) appeared consistently across secondary sources but were not
  traced to ASML's own 20-F customer-concentration disclosure.
- ROE/ROIC figures disagreed materially by source and methodology (ROE
  cited variously as ~47% and ~54%; ROIC cited in a ~26-34% range) —
  treat any single point figure as approximate pending primary-statement
  reconciliation.
- A "$130 billion" cumulative US-China trade-war cost figure surfaced in one
  search result with no stated basis or methodology — not carried forward
  as a fact anywhere in this record.
- A 2025 secondary claim of Chinese "operational EUV capability" was found
  in one source only; CSIS and other technical-policy commentary
  characterize such claims as often overstated. Not treated as established
  fact here.
- Exact 2022 ASML stock-price drawdown magnitude/dates (approximate ~30%
  from the late-2021 all-time high, per one secondary source) — not
  precisely pinned down.
- Whether COVID-19-era (2020) disruption materially affected ASML
  specifically was not researched to a confirmed answer this pass —
  flagged as an open gap, not asserted either way.

**Remediation pass (2026-07-25):** a preliminary external primary-source
cross-check identified one imprecision in this record's original draft —
a risk-entry sentence described China's shipment-share decline as
"36% to 14% across two 2026 quarters," which incorrectly implied the 36%
figure itself fell within calendar 2026. This has been corrected
throughout: 36% is ASML's **Q4 2025** net-system-sales China share
(reported alongside FY2025 full-year results, 2026-01-29); 19% is the
**Q1 2026** figure (reported ~2026-04-15); 14% is the **Q2 2026** figure
(reported 2026-07-15) — i.e., the decline from 36% to 14% happened *across*
two 2026 quarters (Q1 and Q2), starting from a Q4 2025 baseline, not
*within* two 2026 quarters. This session's own WebFetch access remained
blocked (HTTP 403) on every primary-source domain re-attempted during this
remediation pass; the correction rests on multiple independent,
mutually-corroborating WebSearch results (ASML's own press-release titles,
the SEC 6-K filing index, and independent news coverage) rather than on
the external cross-check's claim alone or on a single secondary source.
The EUR43-45B FY2026 guidance figure required no correction and is
retained as previously supported. This pass also added ASML's Q1 2026
headline results (EUR8.8B total net sales, EUR2.8B net income, reported
~2026-04-15) and a management color-commentary fact from the Q2 2026 call
(current China demand characterized as domestic/mature-node logic-driven
rather than leading-edge) — both new facts, not corrections.

## Business summary

ASML designs, manufactures, and services photolithography systems — the
single most technologically demanding step in semiconductor
manufacturing — sold to foundries (TSMC, Samsung), IDMs (Intel), and memory
makers. Two revenue streams: **system sales** (new lithography tools, EUV
and DUV, lumpy/large-ticket) and **Installed Base Management** (service,
upgrades, and field options on an installed base of roughly 5,300+ systems,
recurring and higher-margin, smoothing earnings between system-sale
cycles). Q2 2026 (reported 2026-07-15): total net sales EUR9.3B (system
sales EUR6.6B, of which EUV EUR3.8B / 57%; Installed Base Management
EUR2.8B, beating guidance by roughly EUR300M), gross margin 54.0%, net
income EUR2.9B. Q1 2026 (reported ~2026-04-15): total net sales EUR8.8B,
net income EUR2.8B. FY2025 (reported 2026-01-29): total net sales
EUR32.7B, net income EUR9.6B, gross margin 52.8%.

ASML is the **sole commercial supplier of EUV (extreme ultraviolet)
lithography systems worldwide** — required for leading-edge logic below
roughly 7nm and for advancing memory nodes — within a broader ~94% share of
all lithography equipment (DUV+EUV combined; Nikon and Canon split the
remainder, DUV-only). **High-NA EUV** (next-generation, higher numerical
aperture, needed for future nodes such as Intel's 14A) has begun shipping;
confirmed customers to date are Intel and SK Hynix/Samsung for memory.
Capacity is constrained (fewer than 20 High-NA systems/year at current
capacity, per secondary sources); reported backlog extends into 2027.
TSMC's adoption timing for High-NA at its A14 node was reported as
uncertain/possibly delayed in one source — not independently confirmed.

## Investment thesis (business-quality description, not a recommendation)

**Concise statement:** ASML holds a genuine monopoly at the technological
frontier of semiconductor manufacturing (EUV lithography) with a
structurally difficult-to-replicate supplier moat, and FY2026 guidance has
been raised twice during the year on AI-driven demand — but this position
carries the single most concentrated export-control/geopolitical exposure
of any company in this four-company batch, actively escalating within
calendar 2026 itself.

**Expanded narrative:** ASML's moat rests on decades of accumulated
engineering know-how, an exclusive optics relationship with Carl Zeiss SMT,
and a wholly-owned EUV light-source subsidiary (Cymer, acquired 2013) —
components a competitor would need to rebuild an entire ecosystem to
replicate, not merely match ASML's own patents. No commercial EUV
competitor exists; Nikon abandoned EUV commercialization as technically and
financially infeasible. Against that structural strength sits a genuinely
severe and *currently moving* geopolitical risk: China's share of ASML
system shipments fell from 36% (Q4 2025) to 19% (Q1 2026) to 14% (Q2 2026)
in the space of two quarters, and a pending US bill (the "MATCH Act") could
extend restrictions to DUV — ASML's currently-still-sellable China product
line, unlike EUV which has been blocked since 2019. The October 2024
guidance-cut episode (FY2025 guidance cut to EUR30-35B from an implied
~EUR40B, stock down ~16% in a day) is direct evidence that ASML's 12-24
month order-to-delivery lead time smooths but does not eliminate
demand-timing risk to near-term results, despite popular framing of ASML's
backlog as near-total revenue visibility.

**Conditions relevant to monitoring this thesis** (qualitative, observable):
- FY2026 guidance execution against the twice-raised EUR43-45B range
- No further material acceleration in China revenue-share decline beyond
  what is already guided (~20% of FY2026 revenue)
- The MATCH Act's legislative outcome (pending as of this record's evidence
  date)
- High-NA EUV ramp proceeding without a material, disclosed execution
  failure
- No confirmed instance of unauthorized EUV equipment reaching China
  (currently a disputed, unresolved allegation)

**Conditions that would weaken confidence in the above:**
- Enactment of the MATCH Act or a comparable DUV-China restriction
- A confirmed (not disputed) instance of export-control circumvention
- A material, sustained deceleration in order intake inconsistent with the
  "extremely strong" H1 2026 characterization management has given
- Evidence of a credible EUV alternative technology or a materially
  advanced Chinese domestic lithography capability

## Competitive advantages — detail

*(YAML holds concise claims only; fuller evidence lives here.)*

The EUV monopoly and supplier-ecosystem moat (Zeiss optics, owned Cymer
light sources, 5,000+ largely single-sourced suppliers) are treated in this
record as well-corroborated across secondary sources but not independently
verified against ASML's own primary technology or supplier disclosures —
this is a **structural, industry-consensus fact** (no credible source
disputes ASML's EUV exclusivity) rather than a disputed or uncertain claim,
distinguishing it from the customer-concentration and financial-ratio
figures flagged as genuinely unresolved above.

## Risks — detail

Category framing (not a schema field, recorded here only, matching the
existing corpus convention):
- Export control and geopolitical policy: regulatory/geopolitical
  (the dominant risk category for ASML specifically)
- Customer/geographic concentration: structural/commercial
- Capex cyclicality and guidance-timing risk: operational/structural
- Reduced forward visibility (bookings-disclosure discontinuation):
  informational/governance

See YAML `risks[]` for the structured entries. The export-control category
is treated at greater length there than any other risk in this batch's four
records, reflecting that ASML is the only one of the four companies subject
to a *national-government-level* export licensing regime (Dutch, not
solely US) layered on top of the shared US BIS regime the other three
companies face — a batch-level distinction discussed further in the batch
comparison artifact.

## Catalyst

High-NA EUV ramp (Intel 14A target node; SK Hynix/Samsung memory) and
FY2026 guidance execution are the two forward-looking developments with the
clearest evidence base; both are recorded as narrative context above rather
than as dated `catalysts[]` entries, since neither has a single confirmed
date narrower than "within FY2026" — consistent with this corpus's existing
convention of only populating `catalysts[]` with a specific confirmed date
(see NVDA's Q2 FY2027 earnings-date precedent).

## Margin-relevance evidence (factual, advisory only — no leverage recommendation)

Per `PI-0023` SSB.16 and `OPS-0006` SS4's Milestone 3 requirement. This
section is descriptive only: it does not recommend borrowing, estimate a
safe leverage level, recommend deployment timing, or create a margin
signal, and does not change or reference the account's existing 1.8x
leverage cap or 30% buffer floor.

- **Cyclicality**: ASML's *recognized revenue* has shown no outright annual
  decline across the 2022-2025 window found in this research (EUR21.2B
  in 2022 -> EUR27.6B in 2023 (+30%) -> EUR28.3B in 2024 (+2.5%, near-stall)
  -> EUR32.7B in 2025 (+16%)), even though the broader WFE industry and
  ASML's own peers experienced real 2022-2023 downturn conditions. This
  reflects ASML's long order-to-delivery lead time (12-24 months, per
  secondary sources): *orders/bookings* are the leading indicator of the
  broader cycle for ASML, while *recognized revenue* lags and is smoothed
  by backlog. ASML's own stock price fell an estimated ~30% from its late
  2021 all-time high during the 2022 downturn (approximate, not precisely
  dated) even while revenue kept growing — illustrating that equity-price
  cyclicality and revenue cyclicality diverge materially for this specific
  company, a distinction relevant to any future gap-risk assessment.
- **Balance-sheet strength**: cash and equivalents EUR12.9B at year-end
  2025, declining to an estimated ~EUR8.0B by Q1 2026 (secondary,
  partly attributable to buyback/dividend deployment and normal
  working-capital timing around large system-sale collections); total debt
  approximately EUR2.7B (Q1 2026); estimated net cash position roughly
  EUR5.7B. Debt-to-equity trend reported declining (~0.47 in 2021 to ~0.14
  in 2025). No evidence of near-term refinancing stress, covenant issues,
  or credit-rating concerns found in this research pass.
- **Semiconductor-capex sensitivity**: direct and structural — ASML's
  entire revenue base is semiconductor-fab capital expenditure; this is the
  shared demand driver across all four companies in this batch.
- **Export-control/geopolitical exposure**: the most acute of any company
  in this batch (see Risks above) — a national-government-level licensing
  regime, not solely a US regulatory action, and one that has moved
  materially (China shipment share more than halved) within a single
  calendar year.
- **Customer concentration**: reported high (TSMC ~24%, top-10 >80% per
  secondary sources, unresolved against primary 20-F) — a company-specific
  demand shock at a top customer would disproportionately affect ASML
  relative to a more diversified equipment peer.
- **Simultaneous-loss / correlated-risk with the rest of this batch**: see
  the batch comparison artifact (`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`)
  for the cross-company analysis. In short: ASML's order/bookings cycle is
  understood (qualitatively, not from a source directly comparing ASML to
  AMAT/KLAC/LRCX) to move with or ahead of the broader WFE cycle, while its
  *revenue* cycle lags and smooths relative to peers whose revenue
  recognition is tied to shorter-lead-time systems shipments — a real,
  evidence-supported distinction, though no source found in this research
  quantifies the exact lead/lag in months.
- **Drawdown/recovery characteristics**: the clearest single evidenced
  episode is the October 2024 guidance-cut/stock-drop (~16% in a day, ~20%
  over two sessions per secondary sources) — a guidance-driven, not
  fundamentals-realized, drawdown that recovered as subsequent quarters
  beat guidance. No confirmed multi-quarter earnings deterioration episode
  was found for ASML in the 2019-2026 window researched, distinguishing it
  from LRCX's and KLAC's documented FY2023/FY2024 revenue-decline episodes
  (see those records and the batch comparison).
- **Detectability of thesis deterioration**: ASML's discontinuation of
  quarterly bookings disclosure (2026) is itself relevant here — it removes
  a metric that previously gave earlier visibility into demand
  deterioration before it would show up in recognized revenue, meaning a
  future thesis break may now become visible later (via revenue/guidance)
  rather than earlier (via bookings) than it would have under the prior
  disclosure regime. This is a factual observation about disclosure
  practice, not a claim about current demand conditions.

## What exposure would be lost if ASML were absent from the portfolio

ASML is the only company in this batch (and, per this record's evidence,
the only company anywhere) providing direct exposure to the EUV
lithography chokepoint of the semiconductor value chain — a business with
no commercial substitute. Removing ASML from the portfolio would not be
replaceable by increasing exposure to AMAT, KLAC, or LRCX, since none of
the three competes in or substitutes for lithography; the exposure lost
would be specifically to the technological gate that determines whether
leading-edge nodes can be manufactured at all, as distinct from the
process-step (deposition/etch/inspection) exposure the other three provide.

## Current governed tier and target (existing policy, not research evidence)

ASML is currently governed as a **T1** holding at a **3.35%** per-name
target (`targets.yaml`), and is a member of the governed **semis**
correlated-cluster cap (<=25% of book, `targets.yaml` `caps.clusters`).
This placement is recorded here as **existing operating policy**, per
`OPS-0006` SS2/SS3's zero-based-research discipline — it is preserved as
the historical baseline for a future, still-unauthorized Milestone 7
reconciliation, and is explicitly **not** cited as evidence for, or used to
derive, any conclusion in this record. This record's conviction rating
(Medium) was reasoned independently from the business and risk evidence
above, not from ASML's T1 placement.

## Review framework

- **Cadence: 90 days.** Matches the existing corpus convention (COST, XOM,
  NVDA, GEV, ISRG, TMO, TSM all use 90-day cadence).
- **Unscheduled-review triggers** (qualitative, observable, per `OPS-0006`
  SS12's candidate-trigger list applied selectively to what's actually
  relevant to ASML):
  - Enactment or formal defeat of the MATCH Act (or a comparable DUV-China
    export restriction)
  - A material, confirmed (not merely alleged) export-control compliance
    event
  - A quarterly earnings release or guidance revision materially
    inconsistent with the current EUR43-45B FY2026 range
  - A material, disclosed High-NA EUV ramp execution problem
  - Evidence of a credible alternative lithography technology reaching
    commercial viability
  - A significant leadership change
- **Metrics worth monitoring each review:** quarterly net sales and gross
  margin against guidance, EUV vs. DUV system-sale mix, China shipment
  share, High-NA EUV shipment/order pace, and any material regulatory
  development (Dutch, EU, or US).

## Conviction

**Rating: Medium.** See YAML `conviction.rationale` for the full reasoning.
Restated briefly: a genuine, structurally durable technology monopoly
weighed against the batch's most severe and currently-escalating
export-control exposure, extreme customer concentration not yet verified
against primary disclosure, and this record's own source-access
limitations (disclosed above). This rating and rationale reflect
AI-assisted research pending the independent PR review and human approval
this repository's first-coverage discipline (`PI-0003`/`PI-0005`/`PI-0007`/
`PI-0009` precedent, applied here per `PI-0023`) requires before this
record is treated as finalized.

## Batch membership

ASML is one of four companies (ASML, AMAT, KLAC, LRCX) researched together
under `PI-0023` as the semiconductor front-end capital-equipment
sub-segment of `targets.yaml`'s governed `semis` cluster. See
`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` for the batch-level
overlap, dependency, and shared-risk evidence. ASML does not reference a
Theme Intelligence record (`themes:` field intentionally omitted) — no
semiconductor-equipment theme exists in this repository, and creating one
would be a Theme Intelligence expansion decision outside `PI-0023`'s
authorized scope.

## Sources

See YAML `sources[]` for the structured register. All sources in this
record are labeled SECONDARY per the Source-access disclosure above — no
primary document was independently rendered and inspected by this
implementation session. This record requires independent PR review
(primary-source verification, per this repository's "verify before acting
on external review" guardrail) before its figures should be treated as
confirmed.
