# SKHY — SK hynix Inc. (Nasdaq ADR)

Created 2026-07-26 under `governance/decisions/PI-0024-ws0005-milestone3-batch2-memory.md`
(WS-0005 Milestone 3, Batch 2 — MU, SKHY, the DRAM/NAND/HBM memory-manufacturer
sub-segment of `targets.yaml`'s governed `semis` cluster). Portfolio HQ's
thirteenth Company Intelligence record, and the second of this two-company
batch. **SK hynix is not a newly formed company** — it is the long-established
Korean memory chipmaker (formerly Hynix Semiconductor, part of the SK Group);
what is new is specifically the Nasdaq ADR listing (2026-07-10), a distinction
this record treats carefully throughout, since several risks below (the ADR
conversion-cap mechanic in particular) are specific to holding the ADR rather
than the underlying, much longer-established operating business.

## Source-access disclosure

**Research cutoff for this record: 2026-07-26**, three days before SK hynix's
first quarterly earnings call as a Nasdaq-listed company (Q2 2026 results,
scheduled 2026-07-29 at 9:00am Seoul time) — that report is **not** reflected
anywhere in this record and is recorded as a near-term review trigger below.

WebFetch (direct primary-document retrieval) was **non-functional for the
entire research session** — every attempted fetch returned HTTP 403,
including a control test against `example.com` (a non-target, generally
unrestricted site), which also failed identically to SEC EDGAR, SK hynix's
own investor-relations pages, and Bloomberg. This indicates a tool/
infrastructure-level condition for that session, not a domain-specific
block. **This synthesizing/implementing session independently re-attempted
WebFetch** against the exact SEC EDGAR 424B4 URL identified by the research
pass and received the identical HTTP 403 result, confirming the condition
persisted rather than being a stale, single-attempt failure — the same
access-limitation pattern already disclosed in this repository's ASML/AMAT/
KLAC/LRCX (`PI-0023`, Batch 1) records and in this batch's own MU record.

Given that constraint, **no primary document (Form F-1/F-1A, 424B4
prospectus, 6-K, any future 20-F) was directly opened and read by either the
research session or this synthesizing session.** Every figure in this record
is therefore sourced via WebSearch result synthesis, labeled "PRIMARY,
identified but NOT opened/inspected" (where a specific SEC filing or SK
hynix release is named as the underlying source) or "SECONDARY" (journalism/
analyst commentary) in the YAML `sources[]` and below.

**This synthesizing session additionally performed independent WebSearch
cross-checks (2026-07-26, separate from the original research pass)** on the
two most load-bearing or previously-imprecise figures the research pass
flagged, specifically to satisfy this task's "independently assess the
research results for source quality, factual accuracy, freshness" step:
1. **NVIDIA revenue-concentration trajectory** — independently confirmed the
   ~27% (1H 2025) moderating to ~24% (full-year 2025) figures as consistent
   across multiple independent sources (TechSciResearch, TrendForce, AJU
   Press), resolving what the original research flagged as two
   possibly-inconsistent figures (24% vs. 25%) into a coherent trajectory:
   the FY2025 full-year average (~24%) is lower than the 1H 2025 figure
   (~27%), i.e. H2 2025 concentration moderated rather than the two figures
   representing an unreconciled conflict.
2. **ADR conversion-cap mechanics** — independently confirmed the core
   2.5%-exhausted-cap fact, and found an important additional nuance the
   original research pass did not fully capture: a further 25% depositary
   capacity is technically registered with the SEC, but reopening it beyond
   the exhausted 2.5% operational cap would reportedly require a process
   akin to a secondary public offering — meaning this is not simply an
   administrative limit likely to be raised routinely, but a structural
   condition requiring a further deliberate corporate action by SK hynix
   itself.

**Bounded remediation pass (2026-07-26), same day, following an independent
Fable review of the initial draft PR (#158):** the review found this
record's ADR-premium figures ("up to 51%, narrowing to roughly 30-33%")
were already materially stale relative to accessible evidence, and that the
record omitted pre-cutoff reporting of a 2026-07-29 two-way-conversion
event. An independent WebSearch re-check in this pass found: (a) a more
granular, lower premium trajectory — peak ~52.5% (2026-07-14), ~26% at the
2026-07-15 close, ~25% through the following week, ~22% as of
~2026-07-24-25 — now reflected throughout this record in place of the
earlier 30-33% figure; and (b) Korea Securities Depository reporting (via
Korean local-media sources, not independently verified against a KSD
primary statement) that 2026-07-29 is the date applications for two-way
conversion become possible, with an important asymmetry preserved rather
than resolved into a prediction: cancelling an ADS for an ordinary share is
reported to carry no separate KSD limit, while the capped
ordinary-share-to-ADS direction is unaffected by that date. At least one
source found in this pass explicitly cautions that primary material does
not support a definitive "the premium resolves on July 29" reading — this
record states the event and its reported mechanics without adopting that
prediction. The `conviction.rating` (Medium) was reassessed against this
correction and left unchanged — see `conviction.rationale` in the YAML and
the review-log entry for the same date for the reasoning. No other section
of this record was changed in this pass.

**Unresolved data gaps and conflicts found in research, not resolved by this
record:**
- Whether NVIDIA is named directly as a customer in SK hynix's own
  regulatory disclosure, or whether the concentration percentages above are
  analyst/press inference from a company reference to "a single major
  client," was not resolved — search snippets were inconsistent on this
  distinction, and it matters for how much weight to place on the exact
  percentages.
- The Wuxi (~40% of DRAM output) and Dalian (~25% of NAND output) figures
  each trace to only one distinct outlet in this research pass — not
  independently corroborated across multiple sources, unlike most other
  figures in this record.
- Whether any Form 20-F exists yet for SK hynix — as a brand-new 2026 ADR
  listing, no evidence of an existing 20-F was found, and this record does
  not assert one exists.
- Exact depositary-bank confirmation (Citibank) traces to a single source
  (GraniteShares) — not independently corroborated elsewhere in this pass.
- Supplier relationships (e.g., a lithography-equipment dependency on ASML,
  already covered in this repository's Batch 1 records) were not directly
  sourced this session — an inference, not a finding, and not stated as fact
  anywhere in this record.
- A single-source, unverified claim of a CEO-bonus-dispute lawsuit
  (approximately KRW700M) was found and is explicitly not adopted as
  confirmed fact.
- KRW currency/FX risk was not independently quantified or traced to a
  specific disclosed hedging policy in this research pass — a general,
  structural fact for any Korea-domiciled, KRW-reporting issuer, but not
  developed further here.
- Foreign-private-issuer-specific disclosure or governance provisions (e.g.,
  proxy-rule exemptions, reduced reporting frequency relative to a domestic
  filer) were not independently confirmed for SK hynix specifically in this
  pass — standard for FPI/20-F filers generically, but not verified against
  SK hynix's own elections.

## Business summary

SK hynix is a Korean memory-semiconductor manufacturer with two primary
product segments: **DRAM** (approximately 70-75% of revenue, including HBM,
server DDR5/DDR4, mobile LPDDR5X, and graphics GDDR7) and **NAND flash**
(approximately 25-30%). FY2025 (full year): revenue KRW97.1 trillion,
operating profit KRW47.2 trillion — record results. Q4 2025: NAND revenue
+59% YoY to KRW7.6T; DRAM revenue +70.6% YoY to KRW24.9T; HBM revenue "more
than doubled" YoY. Q1 2026: revenue KRW52.5763 trillion (the first quarter
exceeding KRW50 trillion), operating profit KRW37.6103 trillion (72%
operating margin, a record), net profit KRW40.3459 trillion (77% net
margin). Q2 2026 results are not yet reported as of this record's evidence
cutoff (call scheduled 2026-07-29); pre-earnings analyst estimates found in
this research (Korea Investment & Securities: revenue KRW80.9T, operating
profit KRW60.4T) are explicitly labeled as estimates, not actuals, and are
not adopted as fact anywhere in this record.

SK hynix is widely reported as the current **HBM market leader** and
**NVIDIA's primary HBM supplier** — reported share figures vary by source,
period, and metric (53-62% depending on the specific cut) but are
directionally consistent in describing a dominant, not merely leading,
position. The company reportedly overtook Samsung in operating profit for
the first time in its history during 2025, attributed to HBM's premium
pricing/margin mix, despite Samsung retaining a larger overall DRAM revenue
share.

## Investment thesis (business-quality description, not a recommendation)

**Concise statement:** SK hynix holds the strongest disclosed financial
performance and the most dominant single-product-line market position (HBM)
of any company in this repository's Intelligence corpus to date — but that
strength sits on top of severe, escalating single-customer (NVIDIA)
concentration, a structural ADR-specific valuation-mechanism risk unique to
holding SKHY rather than the Seoul-listed shares, and a documented capacity
for the entire business to swing from record profit to a full-year operating
loss within about a year, as it did in 2022-2023.

**Expanded narrative:** SK hynix's current position rests on being first to
scale HBM3/HBM3E and, as of February 2026, first to begin HBM4 mass
production, feeding an AI-compute buildout in which NVIDIA is reportedly
both the dominant customer (up to 27% of revenue in 1H 2025, moderating to
~24% for full-year 2025) and the primary near-term beneficiary of continued
allocation (reportedly ~70% of NVIDIA's HBM4 "Vera Rubin" allocation, a
forward-looking analyst estimate, not a confirmed contract). This
concentration compounds, rather than offsets, a documented history of severe
cyclicality: the company's Q4 2022 operating loss (KRW1.7 trillion, its
first quarterly operating loss since Q3 2012) and full-year 2023 operating
loss (KRW7.73 trillion) demonstrate that even the current dominant HBM
position does not exempt the business from a demand-driven collapse if AI
compute demand or memory pricing were to turn — the current 77% net-margin
quarter (Q1 2026) and the 2023 full-year operating loss are the two extremes
of the same underlying cycle, separated by roughly three years. Distinct
from the underlying operating business, holding **SKHY specifically**
(rather than the Seoul-listed ordinary shares) carries an additional,
structural risk: the 2.5% ADS conversion cap on **new** ADS creation
(ordinary shares -> ADS) was fully exhausted by the offering itself,
breaking the normal cross-listing arbitrage mechanism and producing a
valuation premium over the ordinary shares that peaked near 52.5% on
2026-07-14, narrowed sharply to roughly 26% at the 2026-07-15 close,
persisted around 25% through the following week, and was reported at
roughly 22% as of ~2026-07-24-25 — still material, though narrower than an
earlier draft of this record stated, corrected in a 2026-07-26 remediation
pass. Reopening meaningful additional *new-ADS* conversion capacity would
likely require a process akin to a secondary offering, not routine
administrative action. Separately, per Korea Securities Depository (KSD)
reporting, 2026-07-29 is the date applications for two-way conversion
become possible, coinciding with the domestic listing of the offering's
newly issued underlying Korean shares — but the reported mechanism is
asymmetric: cancelling an ADS to receive an ordinary share is reported to
carry no separate KSD limit, while the capped ordinary-share-to-ADS
direction is unaffected by this date. As of this record's 2026-07-26
cutoff, the event had not yet occurred; whether it meaningfully compresses
the premium is unassessed here, and at least one source found in this
research explicitly cautions that primary material does not support a
definitive "premium resolves" reading of that date — a caution this record
preserves rather than resolves. The stock's own post-listing trading
history illustrates this is not a purely theoretical risk: the Seoul-listed
shares fell more than 15% in a single session on 2026-07-13, described as
the worst single-day performance on record, amid reported elevated retail
and margin-financed positioning in the Korean market.

**Conditions relevant to monitoring this thesis** (qualitative, observable):
- Continued HBM leadership (or at minimum no confirmed, material share loss)
  through the HBM4 transition against Samsung and Micron
- NVIDIA concentration continuing to moderate as a percentage (as it did
  from 1H 2025 to full-year 2025) without a proportional loss of absolute
  dollar demand
- Continued operation (even if capped) of the Wuxi/Dalian China fabs under
  the 2026 site-license system, without further license-renewal
  deterioration
- Whether the reported 2026-07-29 two-way-conversion opening produces any
  observable further compression in the ADR premium (already ~22% as of
  ~2026-07-24-25, down from a ~52.5% peak), or whether the premium persists
  or re-expands given the capped direction (ordinary shares -> ADS) is
  unaffected by that date
- Q2 2026 results (2026-07-29, not yet reported as of this record) and
  whether they continue the current run-rate or show signs of deceleration

**Conditions that would weaken confidence in the above:**
- A confirmed, sustained drop in NVIDIA's HBM allocation share materially
  below current levels without an offsetting new large customer
- Confirmed HBM price/margin compression starting materially earlier than
  the 2028-and-beyond window flagged by outside analysts as the likely
  oversupply risk (see the batch comparison artifact for the cross-company
  framing of this risk, shared with MU)
- A binding tightening of the China export-control/site-license regime that
  meaningfully impairs (not merely caps) Wuxi/Dalian output
- A disorderly ADR premium correction driven by the conversion-cap mechanic
  itself, independent of the underlying business's performance

## Competitive advantages — detail

*(YAML holds concise claims only; fuller evidence lives here.)*

SK hynix's HBM leadership is treated in this record as well-corroborated
directionally across multiple independent sources — no source found in this
research pass disputes that SK hynix holds the largest HBM share of the
three major DRAM makers — but the *exact* percentage genuinely varies by
source, period, and metric (shipment share vs. revenue share; a single
quarter vs. a full-year figure), consistent with how this repository's
Batch 1 records (see ASML's China-shipment-share handling) treat similarly
variable figures: presented as a range with the variability stated
explicitly, not resolved to a single false-precision number. The FY2025/Q1
2026 financial results are the highest-confidence figures in this record,
independently cross-corroborated across SK hynix's own company release
language (as relayed via search-result synthesis) and multiple analyst
outlets.

## Risks — detail

Category framing (not a schema field, recorded here only, matching the
existing corpus convention):
- Customer/hyperscaler concentration: structural/commercial (the single
  most consequential risk category for SK hynix specifically, given both
  the concentration level and its rapid absolute-dollar growth)
- ADR-specific structural/valuation risk: unique to this security, not the
  underlying operating business — a risk category this repository's
  existing Intelligence corpus (TSM's own ADR, which does not carry a
  comparable conversion-cap constraint) does not otherwise document
- China export-control/geopolitical exposure: regulatory/geopolitical
  (recently shifted from an acute VEU-revocation event to a recurring,
  renewable license-review exposure — a different risk shape than either a
  fully resolved or a fully unresolved regulatory action)
- Memory-cycle cyclicality: operational/structural (comparable in kind, if
  measured differently, to MU's own documented FY2022-2023 downturn)
- Post-listing volatility and governance friction: informational/governance

See YAML `risks[]` for the structured entries. The ADR-specific risk is
discussed at materially greater length here than any comparable risk in
MU's record, reflecting that MU carries no equivalent structural mechanism —
a batch-level distinction discussed further in the comparison artifact.

## Catalyst

SK hynix's Q2 2026 earnings call, scheduled **2026-07-29**, is the clearest
near-term dated event with a confirmed date, but falls three days after this
record's evidence cutoff and is therefore recorded here as context (and as
an explicit review trigger below) rather than populated as a `catalysts[]`
entry with a status this record cannot yet assess. No other single
forward-looking development (Yongin Y1 fab start, HBM4 ramp pacing) carries
a specific confirmed date narrower than a quarter or year in the evidence
gathered, consistent with this corpus's existing convention of only
populating `catalysts[]` with a specific confirmed date.

## Margin-relevance evidence (factual, advisory only — no leverage recommendation)

Per `PI-0024` §B.16 and `OPS-0006` §4's Milestone 3 requirement. This
section is descriptive only: it does not recommend borrowing, estimate a
safe leverage level, recommend deployment timing, or create a margin
signal, and does not change or reference the account's existing 1.8x
leverage cap or 30% buffer floor.

- **Cyclicality**: extreme, and directly evidenced — full-year operating
  profit swung from a run-rate of +KRW4.2T-per-quarter-level profitability
  to a KRW7.73T full-year *loss* within roughly one year (2022 to 2023),
  the sharpest documented cyclical swing found across either company in
  this batch, and comparable in kind (though measured in operating profit
  rather than net income) to MU's own FY2023 downturn.
- **Company-level balance-sheet leverage**: aggregator-sourced figures
  (not independently primary-verified — flagged explicitly) show debt/
  equity of roughly 24%, with cash and short-term investments (~KRW28.0T)
  exceeding total debt (~KRW24.1T), and an improving S&P rating (BBB+,
  positive outlook, February 2026) — directionally consistent with a
  currently strong, investment-grade balance sheet at this point in the
  up-cycle, though this reflects the currently-elevated point in the memory
  cycle, not a stress-tested figure.
- **Stock-price drawdown history, 2026 (security-level, not company
  financial performance)**: an approximately 36.8% peak-to-trough
  correction in the run-up to the Nasdaq listing, separate from the >15%
  single-session Seoul-listed decline on 2026-07-13 and further declines of
  roughly 6-9% by 2026-07-24 — i.e., multiple double-digit-percentage
  drawdowns within a single month surrounding the listing event alone,
  independent of the underlying business's own (currently strong)
  financial trajectory.
- **ADR-specific structural volatility source**: the conversion-cap/
  arbitrage-block mechanic documented above means SKHY's price can diverge
  from, and move independently of, the underlying Seoul-listed shares'
  fundamental value — a volatility source specific to holding the ADR
  rather than the ordinary shares, and not present in any other name in
  this repository's Intelligence corpus researched to date. This has
  already produced a large, rapidly-moving premium (peak ~52.5% on
  2026-07-14, ~22% by ~2026-07-24-25) independent of the underlying
  business's own performance; a reported 2026-07-29 partial opening of the
  conversion mechanism (see Investment thesis above) is a further
  observable data point for this volatility source, not a resolution of it.
- **Simultaneous-loss / correlated-risk with MU and the rest of the semis
  cluster**: see the batch comparison artifact
  (`intelligence/BATCH2_MEMORY_COMPARISON.md`) for the cross-company
  analysis. In short: SKHY and MU share direct exposure to the same
  memory-pricing cycle (a genuine simultaneous-loss mechanism), while SKHY
  additionally carries the ADR-structural risk layer MU does not have.
- **Detectability of thesis deterioration**: SK hynix's disclosed second-
  customer emergence (12.4% in 2026) is a data point that, if it continues,
  would give somewhat *more* forward visibility into customer
  diversification than a business with a single disclosed customer above
  10% would offer — a factual observation about disclosure trajectory, not
  a claim about current concentration risk being resolved.

## What exposure would be lost if SKHY were absent from the portfolio

SK hynix is this portfolio's only exposure to the reported #1-by-share HBM
producer and NVIDIA's reported primary HBM supplier — a distinct position
from MU (the batch's other memory holding, a fast-growing but currently
smaller-share HBM challenger) and from the `semis` cluster's equipment names
(ASML, AMAT, KLAC, LRCX), which are toolmakers rather than chip producers.
Removing SKHY would not be replaceable by increasing exposure to MU, since
the two companies occupy different competitive positions within the same
product category (see the batch comparison artifact for the detailed
overlap/differentiation analysis) — MU does not currently hold SK hynix's
reported HBM share or its reported NVIDIA-primary-supplier position. Holding
SKHY specifically (rather than not holding SK hynix exposure at all) is also
the only way this portfolio gains exposure to SK hynix's operating business,
since no other SK hynix security is held.

## Current governed tier and target (existing policy, not research evidence)

SKHY is currently governed as a **band** holding at a **0.75%** per-name
target with a 1.25x cap (`targets.yaml`), and is a member of the governed
**semis** correlated-cluster cap (<=25% of book, `targets.yaml`
`caps.clusters`). This placement is recorded here as **existing operating
policy**, per `OPS-0006` §§2/3's zero-based-research discipline — it is
preserved as the historical baseline for a future, still-unauthorized
Milestone 7 reconciliation, and is explicitly **not** cited as evidence for,
or used to derive, any conclusion in this record. This record's conviction
rating (Medium) was reasoned independently from the business and risk
evidence above, not from SKHY's `band` tier placement.

## Review framework

- **Cadence: 90 days.** Matches the existing corpus convention (COST, XOM,
  NVDA, GEV, ISRG, TMO, TSM, ASML, AMAT, KLAC, LRCX, MU all use 90-day
  cadence).
- **Unscheduled-review triggers** (qualitative, observable, per `OPS-0006`
  §12's candidate-trigger list applied selectively to what's actually
  relevant to SK hynix):
  - **SK hynix's Q2 2026 earnings call, 2026-07-29** — the first earnings
    report as a Nasdaq-listed company, falling just three days after this
    record's evidence cutoff; this is the single nearest-term, highest-
    priority review trigger for this record
  - A material, confirmed change in HBM market-share standing relative to
    Samsung or Micron
  - A material, confirmed change in NVIDIA revenue concentration (either
    direction)
  - Any change to the China Wuxi/Dalian site-license status (renewal,
    tightening, or further relaxation)
  - **The reported 2026-07-29 two-way-conversion opening**: a dedicated,
    dated trigger to reassess (1) whether it actually occurred as reported,
    (2) whether the ADS-to-ordinary-share conversion path remains
    operational, (3) whether the ADR premium compressed further, held
    (~22% as of ~2026-07-24-25), persisted, or re-expanded, and (4) whether
    the 2.5% cap or broader depositary-capacity mechanics changed — none of
    which this record concludes in advance
  - A significant leadership change
- **Metrics worth monitoring each review:** quarterly revenue and operating
  margin against the current run-rate, HBM/DRAM/NAND segment mix, NVIDIA
  and second-customer concentration percentages, the SKHY-vs-000660 ADR
  premium, and any material regulatory development (Korea, US, China).

## Conviction

**Rating: Medium.** See YAML `conviction.rationale` for the full reasoning.
Restated briefly: the strongest disclosed financial performance and market
position of any company in this repository's Intelligence corpus to date,
weighed against severe and only recently, partially diversifying customer
concentration, a structural ADR-specific valuation risk unique to this
security, recurring (not resolved) China export-control exposure, and this
record's own source-access limitations (disclosed above, including the
F-1/424B4 risk-factors section never being opened). This rating and
rationale reflect AI-assisted research pending the independent PR review and
human approval this repository's first-coverage discipline (`PI-0003`/
`PI-0005`/`PI-0007`/`PI-0009`/`PI-0023` precedent, applied here per
`PI-0024`) requires before this record is treated as finalized.

## Batch membership

SKHY is one of two companies (MU, SKHY) researched together under `PI-0024`
as the DRAM/NAND/HBM memory-manufacturer sub-segment of `targets.yaml`'s
governed `semis` cluster. See `intelligence/BATCH2_MEMORY_COMPARISON.md` for
the batch-level overlap, dependency, and shared-risk evidence between SKHY
and MU. SKHY does not reference a Theme Intelligence record (`themes:`
field intentionally omitted) — no semiconductor-memory theme exists in this
repository, and creating one would be a Theme Intelligence expansion
decision outside `PI-0024`'s authorized scope, matching the reasoning
already applied to ASML's own record in Batch 1 and to MU's own record in
this batch.

## Sources

See YAML `sources[]` for the structured register, which distinguishes
**document type** (PRIMARY — SK hynix's own SEC registration filings;
SECONDARY — news-outlet/analyst coverage of an underlying primary action)
from **access status** (every primary document is labeled "identified but
NOT opened by this session" — no primary document was independently
rendered and inspected by either the research session or this synthesizing
session at any point, confirmed via a fresh WebFetch re-attempt by this
session against the exact identified 424B4 URL). This record requires
independent PR review (full primary-source verification, per this
repository's "verify before acting on external review" guardrail) before
its figures should be treated as confirmed — the F-1/424B4 risk-factors
section (China export-control, currency, foreign-private-issuer disclosure,
and SK hynix's own customer-concentration language) remains the single
highest-priority open item for that verification, followed by the Wuxi/
Dalian output-share percentages and the depositary-bank confirmation.
