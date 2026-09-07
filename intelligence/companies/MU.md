# MU — Micron Technology, Inc.

Created 2026-07-26 under `governance/decisions/PI-0024-ws0005-milestone3-batch2-memory.md`
(WS-0005 Milestone 3, Batch 2 — MU, SKHY, the DRAM/NAND/HBM memory-manufacturer
sub-segment of `targets.yaml`'s governed `semis` cluster, the value-chain
counterpart one level down from `PI-0023`'s Batch 1 equipment sub-segment).
Portfolio HQ's twelfth Company Intelligence record, and the first of this
two-company batch.

## Source-access disclosure

**Research cutoff for this record: 2026-07-26.** Research was conducted by a
dedicated research session using WebSearch; WebFetch (direct primary-document
retrieval) was **blocked at the network/proxy egress level for the entire
session** — every attempt against SEC EDGAR, `investors.micron.com`,
`micron.com`, and a long list of secondary-news domains returned HTTP 403,
confirmed mechanically via the proxy's own `recentRelayFailures` log showing
`"kind": "connect_rejected"` / `"gateway answered 403 to CONNECT (policy
denial or upstream failure)"` for each host — only `github.com` succeeded as
a control, indicating a broad environment-level access gap rather than a
Micron- or SEC-specific block. **This synthesizing/implementing session
independently re-attempted WebFetch** against the exact SEC EDGAR URLs
identified by the research pass (the FY2025 10-K and the Q3 FY2026 8-K
earnings exhibit) and received the identical HTTP 403 result; a further
control fetch against `micron.com` and `en.wikipedia.org` (a non-target,
generally-unrestricted site) also returned 403, confirming this is a
persistent, session-wide condition rather than a stale or single-attempt
failure — the same access-limitation pattern already disclosed in this
repository's ASML/AMAT/KLAC/LRCX (`PI-0023`, Batch 1) records from the
immediately preceding batch (2026-07-25).

Given that constraint, **no primary document (10-K, 10-Q, 8-K, earnings
release, investor presentation) was directly opened and read by either the
research session or this synthesizing session.** Every figure in this record
is therefore sourced via WebSearch result synthesis — either citing a named
primary document by its exact title/URL/date (labeled "PRIMARY, identified
but NOT opened/inspected" in the YAML `sources[]` and below) or via
secondary journalism/analyst commentary (labeled "SECONDARY"). Where a figure
is well-corroborated across multiple independent sources it is presented
with reasonable confidence; where sources genuinely disagree, that
disagreement is stated explicitly rather than silently resolved, per this
repository's "no unsupported snippet presented as inspected primary
evidence" discipline (`PI-0024` §D).

**This synthesizing session additionally performed independent WebSearch
cross-checks (2026-07-26, separate from the original research pass) on the
three most load-bearing or internally-conflicting figures the research pass
flagged**, specifically to satisfy this task's "independently assess the
research results for source quality, factual accuracy, freshness" step:
1. **FY2025 mainland-China revenue share** — the original research flagged
   two conflicting figures (7.1%/$2.64B versus 12%/$3.4B). An independent
   re-search returned only the 7.1%/$2.64B figure consistently across
   multiple sources; the 12% figure did not resurface and is **not adopted**
   as a confirmed second data point.
2. **Credit ratings** — independently confirmed Moody's Baa2 (upgraded from
   Baa3, 2026-01-08, stable outlook) and S&P BBB (affirmed 2026-05-26,
   positive outlook) directly against rating-agency-adjacent press coverage.
   A separately-reported "BBB+ from all three major agencies" claim was
   searched for and **not corroborated** — not adopted.
3. **HBM market-share range** — confirmed this is genuinely variable across
   sources by period and metric (shipment vs. revenue share), not a single
   reconcilable number; presented in this record as a range (~18-21%) with
   that caveat stated explicitly rather than resolved to a false-precision
   point estimate.

**Unresolved data gaps and conflicts found in research, not resolved by this
record:**
- No named-customer or hyperscaler revenue-concentration percentage was
  located for Micron specifically (the 16 Strategic Customer Agreements /
  ~20% DRAM volume / ~1/3 NAND volume figures are volume-commitment metrics,
  not customer-identity or revenue-share disclosures) — flagged as a genuine
  gap requiring primary 10-K verification, not evidence of low concentration
  either way.
- No named equipment-supplier relationship (e.g., to ASML/AMAT/KLAC/LRCX,
  all already covered in this repository's Batch 1 records) was found
  specific to Micron in this research pass — an evidentiary gap, not
  evidence of absence.
- HBM patent-count claim (621 Micron vs. 315 SK hynix, per one secondary
  source) is a single-source, unverified claim — not adopted as fact, noted
  here only as a data point requiring primary verification if cited.
- Exact date and cost/production impact of the reported Taichung, Taiwan
  fab gas-leak fire were not established — reporting described it as
  contained with no injuries and normal operations resuming, but the
  specific date and any disclosed financial impact were not found.
- Whether Micron's continued China packaging/assembly presence (Xi'an) and
  any residual China-facing legacy-node manufacturing interact with the
  CHIPS Act's 10-year "countries of concern" expansion guardrail (which
  carries a full clawback-plus-interest penalty for violation) was not
  established — a real research gap, not confirmed compliant or
  non-compliant either way.
- A reported "$5.4 billion debt buyback" (single source, FinancialContent/
  MarketMinute) was not independently corroborated against a primary filing
  and is not restated as a confirmed figure in the YAML.

## Business summary

Micron designs, manufactures, and sells memory and storage semiconductors
under the Micron and Crucial brands, reporting across four segments: Cloud
Memory Business Unit, Core Data Center Business Unit, Mobile and Client
Business Unit, and Automotive and Embedded Business Unit. Two product
families dominate: **DRAM** (including HBM, server DDR5/DDR4, mobile
LPDDR5X, and graphics memory) and **NAND** flash storage. Q3 FY2026 (period
ended 2026-05-28, reported 2026-06-24): revenue $41.46B — a fifth
consecutive quarterly record, up 345.7% year-over-year — GAAP net income
$28.24B ($24.67 diluted EPS), operating margin 81.2%, operating cash flow
$25.39B. Data-center revenue exceeded $25B (an annualized run-rate above
$100B); data-center SSD revenue exceeded $5B, more than doubling
sequentially. FY2025 (period ended 2025-08-28) total revenue grew 49%
year-over-year (DRAM +62%, NAND +18%), with consolidated gross margin
improving to 40% from 22% in FY2024. Guidance for Q4 FY2026: revenue $50B
+/- $1B, gross margin approximately 86%, non-GAAP EPS $31 +/- $1.

## Investment thesis (business-quality description, not a recommendation)

**Concise statement:** Micron is the fastest-growing HBM-share challenger
among the three global merchant DRAM makers, riding an AI-memory demand
supercycle to record results and a rapidly deleveraging balance sheet — but
it remains a distant #2/#3 in the specific HBM product line driving that
re-rating, has already absorbed one of the most severe documented
semiconductor down-cycles (2022-2023) at roughly a quarter of its current
capital base, and carries realized, not hypothetical, China regulatory risk.

**Expanded narrative:** Micron's growth story is concentrated in AI-driven
demand for HBM and high-capacity server DRAM/SSDs: its HBM share has grown
from an estimated ~2% in 2023 to a range of roughly 18-21% across
late-2025/2026 cuts, and data-center revenue now runs at an annualized rate
above $100B. This growth has funded rapid balance-sheet repair — total debt
fell from $14,577M to $5,722M over the nine months to Q3 FY2026, alongside
two credit-rating upgrades (Moody's Baa2, S&P BBB) within the past six
months. Set against this strength: Micron's FY2022-2023 downturn is a
concrete, severe precedent for what a memory-cycle turn can do to this
specific business — a 53% single-quarter revenue collapse, a full-year GAAP
net loss, $1.83B in inventory write-downs, and a roughly 70% peak-to-trough
price decline across the industry. FY2026 capex guidance of approximately
$27B (rising further into FY2027) means the capital base now exposed to a
comparable future downturn is on the order of 4x the FY2023 trough spending
level. Micron's China exposure is not a tail-risk hypothetical: the 2023 CAC
cybersecurity ruling already cost the company access to China's
critical-infrastructure procurement (an affected segment reported at ~11% of
2022 revenue), and as of late-2025 reporting Micron has concluded that
business will not recover, exiting China's server/data-center memory market
entirely while retaining only a packaging/test facility in Xi'an. Within its
core competitive set, Micron is a fast-growing challenger, not yet the
category leader — SK hynix holds a persistently larger HBM share across most
cuts found in this research (see the batch comparison artifact), and in
conventional NAND, Micron sits mid-pack, trailing Kioxia in at least one
recent quarterly cut.

**Conditions relevant to monitoring this thesis** (qualitative, observable):
- Continued HBM share gains (or at minimum, no reversal) against SK hynix
  and Samsung through the HBM4 transition
- FY2026/FY2027 capex execution and whether memory pricing sustains at a
  level that supports it
- No further material deterioration in China market access beyond the
  already-completed server/data-center exit
- Whether the capital-return posture (dividend, buybacks) begins to move
  more in line with the current earnings level, or whether the current
  restrained posture persists

**Conditions that would weaken confidence in the above:**
- A confirmed reversal or stalling of Micron's HBM share-gain trajectory
- Memory pricing rolling over sharply while FY2026/FY2027 capex remains
  committed at current elevated levels, reproducing the FY2023 loss dynamic
  at a materially larger capital base
- A new China, Taiwan, or broader export-control escalation affecting
  Micron's remaining China operations or its Taiwan manufacturing base
- A sustained shift of analyst sentiment toward the minority Sell case
  currently held by at least one covering analyst

## Competitive advantages — detail

*(YAML holds concise claims only; fuller evidence lives here.)*

Micron's position as one of only three global-scale merchant DRAM
manufacturers is a structural, industry-consensus fact (no credible source
disputes this three-way market structure). Its HBM share-growth trajectory
(~2% in 2023 to ~18-21% across recent cuts) is well-corroborated directionally
across multiple sources, though the exact point-in-time percentage varies by
source, period, and metric — treated in this record as a range, not a false-
precision single figure. The deleveraging balance sheet (debt down ~60%
within FY2026 to date) and the two-agency credit upgrade are independently
cross-checked facts (see Source-access disclosure above), among the highest-
confidence figures in this record.

## Risks — detail

Category framing (not a schema field, recorded here only, matching the
existing corpus convention):
- Memory-cycle cyclicality and capital-base scaling: structural/operational
  (the dominant risk category for Micron specifically, given the FY2023
  precedent)
- China regulatory/geopolitical exposure: regulatory/geopolitical (realized,
  not hypothetical — see the 2023 CAC ruling and 2025 China exit)
- Taiwan manufacturing concentration: geopolitical/operational
- Competitive position within HBM/NAND: structural/commercial
- Capital-allocation posture: governance/informational (a debated, not
  resolved, signal)

See YAML `risks[]` for the structured entries. Unlike ASML's export-control
risk (the batch-1 precedent for this category framing), Micron's China risk
is *already realized* — a completed market exit, not an escalating but
still-open exposure — which is a materially different risk shape worth
distinguishing explicitly: the open question for Micron is whether a
comparable future action could hit its remaining, smaller China footprint or
its Taiwan manufacturing base, not whether the already-lost China
server/data-center business might further deteriorate.

## Catalyst

No single dated catalyst with a specific confirmed date narrower than
"within FY2026/FY2027" was identified with sufficient confidence to populate
a `catalysts[]` entry in this pass — HBM4 mass production timing, the
Idaho/Japan/Singapore capacity ramps, and FY2027 capex execution are all
recorded as narrative context above (Investment thesis, Manufacturing
footprint) rather than as dated `catalysts[]` entries, consistent with this
corpus's existing convention (see NVDA's dated-earnings-only precedent,
restated in ASML's own record) of only populating `catalysts[]` with a
specific confirmed date. Micron's next quarterly earnings date was not
independently confirmed in this research pass (the FY2026 fiscal year end
is approximately August/September, historically followed by a report in
late September; this is an inference from cadence, not a confirmed date, and
should be verified before being relied upon).

## Margin-relevance evidence (factual, advisory only — no leverage recommendation)

Per `PI-0024` §B.16 and `OPS-0006` §4's Milestone 3 requirement. This
section is descriptive only: it does not recommend borrowing, estimate a
safe leverage level, recommend deployment timing, or create a margin
signal, and does not change or reference the account's existing 1.8x
leverage cap or 30% buffer floor.

- **Cyclicality**: among the most severe of any name plausibly held in this
  portfolio. FY2023 Q2 revenue fell 53% YoY; the company posted a full-year
  FY2023 GAAP net loss of approximately $1.6B following FY2022
  profitability; the current up-cycle has since produced a swing to $28.24B
  of *quarterly* GAAP net income (Q3 FY2026) — a swing of a magnitude few
  other holdings in this repository's Intelligence corpus exhibit.
- **Capex cyclicality**: capex itself swings roughly 4x trough-to-peak
  within a single multi-year cycle ($7B FY2023 trough to ~$27B FY2026
  guided), meaning free cash flow (revenue minus capex) is even more
  volatile than revenue alone — a directly relevant fact for any future
  gap-risk or drawdown assessment.
- **Balance-sheet strength, current**: cash and marketable investments of
  approximately $30.1-30.2B against total debt of $5,722M (net cash
  position ~$24.4B) as of Q3 FY2026, with total debt down from $14,577M
  nine months earlier — the company is currently *de-levering* sharply, not
  adding leverage, even as its underlying business cyclicality remains
  structurally high. Two independent credit-rating upgrades (Moody's Baa2,
  S&P BBB positive) corroborate this improving trajectory.
- **Drawdown/recovery characteristics**: the FY2022-2023 downturn is the
  clearest evidenced episode — a full-year net loss and $1.83B of inventory
  write-downs, with recovery driven by the subsequent AI/HBM demand cycle
  rather than a quick mean-reversion; no confirmed multi-year recovery
  timeline (as distinct from the eventual recovery itself) was established
  in this research pass.
- **Realized regulatory-loss precedent**: the 2023 China CAC ruling and 2025
  server/data-center China exit is a real, dollar-quantifiable (~11% of 2022
  revenue in the affected segment) example of a geopolitical action
  producing a sustained, not merely temporary, revenue impairment — a
  distinct loss mechanism from ordinary price-cycle cyclicality.
- **Simultaneous-loss / correlated-risk with the rest of the semis
  cluster**: see the batch comparison artifact
  (`intelligence/BATCH2_MEMORY_COMPARISON.md`) for the cross-company
  analysis with SKHY, and the existing `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`
  for this cluster's equipment sub-segment. In short: Micron shares the
  broader semiconductor-capex-cycle exposure documented for the equipment
  names, but its own revenue/earnings cyclicality (driven by commodity
  memory pricing, not equipment order timing) has historically been
  sharper and faster-moving than the equipment sub-segment's own documented
  downturns.

## What exposure would be lost if MU were absent from the portfolio

Micron is this portfolio's only US-headquartered exposure to DRAM/NAND/HBM
memory manufacturing as a distinct AI-infrastructure sub-vertical, separate
from the logic (NVDA), foundry (TSM), and front-end-equipment (ASML, AMAT,
KLAC, LRCX) exposure already covered elsewhere in this repository's
Intelligence corpus and in the `semis` cluster generally. Removing MU would
not be replaceable by increasing exposure to those names, since none of them
manufactures memory; the exposure lost would be specifically to
commodity-memory-pricing upside (and downside) and the AI-driven HBM
transition, a risk/return profile with materially higher revenue and
earnings cyclicality than the logic/foundry/equipment names, as documented
in the FY2022-2023 downturn comparison above. Distinct from SKHY (the
batch's other memory holding), MU offers memory exposure without the
ADR-specific structural risk (conversion-cap-driven valuation premium)
documented in SKHY's own record and the batch comparison artifact.

## Current governed tier and target (existing policy, not research evidence)

MU is currently governed as a **band** holding at a **0.75%** per-name
target with a 1.25x cap (`targets.yaml`), and is a member of the governed
**semis** correlated-cluster cap (<=25% of book, `targets.yaml`
`caps.clusters`). `targets.yaml`'s own `semis` cluster comment groups MU
together with WDC as "memory" names — a grouping this batch's authorizing
decision (`PI-0024`) identifies as stale following Western Digital's
February 2025 separation of its Flash business into Sandisk (SNDK), but does
not correct in this implementation, consistent with `PI-0024` §E. This
placement is recorded here as **existing operating policy**, per `OPS-0006`
§§2/3's zero-based-research discipline — it is preserved as the historical
baseline for a future, still-unauthorized Milestone 7 reconciliation, and is
explicitly **not** cited as evidence for, or used to derive, any conclusion
in this record. This record's conviction rating (Medium) was reasoned
independently from the business and risk evidence above, not from MU's
`band` tier placement.

## Review framework

- **Cadence: 90 days.** Matches the existing corpus convention (COST, XOM,
  NVDA, GEV, ISRG, TMO, TSM, ASML, AMAT, KLAC, LRCX all use 90-day cadence).
- **Unscheduled-review triggers** (qualitative, observable, per `OPS-0006`
  §12's candidate-trigger list applied selectively to what's actually
  relevant to Micron):
  - A quarterly earnings release or guidance revision materially
    inconsistent with the current cycle-strength narrative (particularly
    any sign of memory-pricing rollover)
  - A material, confirmed change in HBM market-share standing relative to
    SK hynix or Samsung
  - A new China, Taiwan, or broader export-control action affecting
    Micron's remaining operations
  - A material capital-return policy change (dividend, buyback cadence)
  - A significant leadership change
  - Confirmation or resolution of the reported Taichung fab fire's
    operational/financial impact
- **Metrics worth monitoring each review:** quarterly revenue and gross
  margin against guidance, HBM/DRAM/NAND segment mix and share trend, capex
  trajectory against guidance, credit-rating actions, and any material
  regulatory development (US CHIPS Act guardrails, China, Taiwan).

## Conviction

**Rating: Medium.** See YAML `conviction.rationale` for the full reasoning.
Restated briefly: genuine, fast-growing HBM-share momentum and a rapidly
strengthening balance sheet, weighed against the severest documented
memory-cycle downturn precedent found anywhere in this repository's
Intelligence corpus to date, a #2/#3 (not leading) competitive position in
the specific HBM product line driving the current re-rating, realized China
regulatory risk, and this record's own source-access limitations (disclosed
above). This rating and rationale reflect AI-assisted research pending the
independent PR review and human approval this repository's first-coverage
discipline (`PI-0003`/`PI-0005`/`PI-0007`/`PI-0009`/`PI-0023` precedent,
applied here per `PI-0024`) requires before this record is treated as
finalized.

## Batch membership

MU is one of two companies (MU, SKHY) researched together under `PI-0024` as
the DRAM/NAND/HBM memory-manufacturer sub-segment of `targets.yaml`'s
governed `semis` cluster — the value-chain counterpart, one level down, to
`PI-0023`'s Batch 1 (ASML, AMAT, KLAC, LRCX) semiconductor capital-equipment
sub-segment. See `intelligence/BATCH2_MEMORY_COMPARISON.md` for the
batch-level overlap, dependency, and shared-risk evidence between MU and
SKHY. MU does not reference a Theme Intelligence record (`themes:` field
intentionally omitted) — no semiconductor-memory theme exists in this
repository, and creating one would be a Theme Intelligence expansion
decision outside `PI-0024`'s authorized scope, matching the reasoning
already applied to ASML's own record in Batch 1.

## Sources

See YAML `sources[]` for the structured register, which distinguishes
**document type** (PRIMARY — Micron's own SEC filings and press releases;
SECONDARY — news-outlet/analyst coverage of an underlying primary action)
from **access status** (every primary document is labeled "identified but
NOT opened by this session" — no primary document was independently
rendered and inspected by either the research session or this synthesizing
session at any point, confirmed via a fresh WebFetch re-attempt by this
session against the exact identified URLs). This record requires
independent PR review (full primary-source verification, per this
repository's "verify before acting on external review" guardrail) before
its figures should be treated as confirmed — named-customer/hyperscaler
concentration disclosure and the CHIPS Act guardrail interaction with
Micron's remaining China footprint remain the priority open items for that
verification.
