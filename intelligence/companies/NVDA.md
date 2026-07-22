# NVDA — NVIDIA Corporation

Last updated: 2026-07-22 — evidence refresh authorized by
`governance/decisions/PI-0018-nvda-intelligence-refresh-authorization.md`,
following the PI-0017 committee review's Intelligence-maintenance
recommendation. Originally created 2026-07-18 through AI-assisted research
and drafting, finalized through explicit human review and approval under
PI-0007. Portfolio HQ's third Portfolio Intelligence record, and the first
of two records created under the `ai_infrastructure` Theme Intelligence
pilot (`decision_log.yaml` PI-0006/PI-0007).

## Source-access disclosure

**Research cutoff for this refresh: 2026-07-22.** Direct rendering of
NVIDIA's and the U.S. government's primary documents was attempted and
confirmed unavailable in this research environment, not merely assumed:
this session directly tested `www.sec.gov`, `investor.nvidia.com`,
`nvidianews.nvidia.com`, `www.bis.gov`, `efts.sec.gov`, and
`www.congress.gov` and every one returned a network-policy CONNECT-tunnel
403, confirmed against this environment's own proxy relay-failure log (a
policy denial at the gateway, not a site-side rejection). This is the same
access pattern already disclosed in the original 2026-07-18 record for
COST, XOM, and NVDA itself, now independently re-confirmed rather than
re-assumed. Every new figure and claim added by this refresh is therefore
sourced to secondary aggregation (financial news outlets, filing mirrors,
and trade press), explicitly labeled as such, and corroborated across
multiple independent secondary sources converging on the same values where
possible, per `PI-0018` Sec D's evidence standard and fallback provision.
Where a figure could not be corroborated to this session's confidence
standard, it is recorded below as an unresolved item rather than asserted.
No NVIDIA Form 10-K or 10-Q filing URL is asserted as directly rendered by
this record — the identified URLs in the YAML `sources[]` block are cited
as the primary document's location, with their access-blocked status
disclosed alongside each.

## Business summary

NVIDIA supplies accelerated-compute hardware and networking platforms used
for AI training and inference at scale. For fiscal year 2026 (ended
2026-01-25): total revenue was $215.938 billion, up 65% year-over-year;
Data Center segment revenue was $193.7 billion, up 68% year-over-year.

**Q1 FY2027 (quarter ended 2026-04-26, reported 2026-05-20)** — the newest
reporting cycle since the original record — showed acceleration rather
than deceleration: total revenue $81.6 billion, up 85% year-over-year;
Data Center segment revenue a record $75.2 billion, up 92% year-over-year
and 21% sequentially (Data Center computing revenue $60 billion, +77% YoY;
Data Center networking revenue $15 billion, nearly tripling YoY). GAAP
gross margin was 74.9%; GAAP operating income was $53.5 billion (+147%
YoY) on GAAP operating expenses of $7.6 billion (+52% YoY); GAAP net
income was $58.3 billion (+211% YoY) on GAAP diluted EPS of $1.87.
Operating cash flow was $50.3 billion against capital expenditure of
approximately $1.8 billion, yielding free cash flow of $48.6 billion —
NVIDIA returned approximately $20.0 billion to shareholders in the quarter
through buybacks and dividends. A second reporting cycle, Q2 FY2027, is
expected around 2026-08-26 per secondary calendar aggregators — this date
is not independently confirmed against a NVIDIA-issued announcement in
this pass and is treated as an estimate, not a scheduled fact.

**Unresolved from this refresh, disclosed rather than silently omitted:**
(1) the precise Q1 FY2027 R&D expense figure — secondary sources suggested
a range but did not converge with sufficient consistency for this record
to assert a specific dollar figure with confidence; (2) NVIDIA's total
cash-and-marketable-securities balance at quarter-end — sources found
disclosed a $13.2 billion cash-and-equivalents figure and a separate $27.4
billion lock-up-restricted-investment component without a clearly
reconciled combined total; (3) the exact operating-income-to-net-income
bridge — Q1 FY2027 net income ($58.3B) exceeds operating income ($53.5B),
which secondary sources attribute directionally to a large "other income,
net" line (including unrealized gains of $13.4 billion on marketable
equity securities held at period end) net of an income-tax provision, but
the precise other-income and tax-provision split was not resolved to this
session's confidence standard. All three remain open, not converted to
fact and not dropped.

## Investment thesis (business-quality description, not a
recommendation)

**Concise statement:** NVIDIA is the reported leading supplier of
accelerated-compute hardware for AI training and inference; its Data
Center segment grew to $193.7 billion in FY2026 and then to a record $75.2
billion in the single quarter of Q1 FY2027 (+92% YoY), an acceleration
from FY2026's own growth rate rather than the deceleration a maturing
buildout might otherwise show.

**Expanded narrative:** the thesis rests on continued demand for
accelerated compute from the AI-infrastructure buildout described in the
`ai_infrastructure` theme record — reported here as the current disclosed
condition, not a prediction that this demand pattern continues. The Q1
FY2027 acceleration (92% YoY Data Center growth vs. FY2026's 68% YoY) is a
reported fact, not an inference, and directly updates the original
record's growth trajectory rather than merely restating it. Management's
own May 2026 capital-allocation decision — a 25x quarterly dividend
increase and an additional $80.0 billion buyback authorization — is a
disclosed, dated fact that speaks to confidence in sustained free-cash-flow
generation, not itself a forecast this record independently verifies.

**Conditions relevant to monitoring this thesis** (qualitative, observable
— no arbitrary numerical threshold, consistent with PI-0004's precedent
for COST/XOM):
- Data Center segment revenue continues at or above recently reported
  growth rates, without a material, sustained reversal
- No material loss of position among the largest hyperscaler customers,
  now more concretely disclosed as three direct customers at
  approximately 21%/17%/16% of Q1 FY2027 revenue (secondary-sourced, see
  Risks below)
- Export-control or geopolitical policy does not materially restrict
  addressable market beyond what is currently disclosed — now a more
  active area than at the original record's writing, with a January 2026
  licensing-policy change and a June 2026 loophole-closing guidance
  update both reported since
- Each new compute-architecture-generation transition executes without a
  material, disclosed ramp or yield problem
- Hyperscaler custom-silicon competitors (Google TPU, AWS Trainium,
  Microsoft Maia, Meta MTIA) do not materially displace NVIDIA's share of
  inference workloads specifically, reported as the segment where
  custom-ASIC competition is most concentrated

**Conditions that would weaken confidence in the above** (analytical
judgment, qualitative and observable, no numerical trigger):
- A material, sustained deceleration or reversal in Data Center segment
  revenue
- Evidence of material customer concentration risk materializing (a large
  customer meaningfully reducing orders)
- A material new export-control or geopolitical restriction, or evidence
  that the June 2026 loophole-closing guidance is not effectively enforced
- A disclosed, material execution failure in a new architecture
  generation's ramp
- Evidence that hyperscaler custom-ASIC adoption is materially eroding
  NVIDIA's inference-workload position faster than new architecture
  generations can offset

## Competitive advantages — detail

*(YAML holds concise claims only, per the frozen schema; fuller evidence
lives here.)*

1. **AI accelerated-compute hardware leadership, now with an accelerating
   growth rate.** Evidence: FY2026 Data Center segment revenue of $193.7
   billion (+68% YoY), followed by Q1 FY2027 Data Center segment revenue
   of $75.2 billion in a single quarter (+92% YoY, +21% sequentially),
   split $60 billion compute (+77% YoY) and $15 billion networking (nearly
   tripling YoY). Limitation: these figures are corroborated across
   multiple independent secondary aggregators, not directly rendered by
   this repository's tooling in this pass (see Source-access disclosure);
   the specific competitive-moat mechanisms (e.g., software ecosystem
   lock-in) were not independently verified against NVIDIA's own filed
   disclosures in this pass, same limitation as the original record.
2. **Materially expanded shareholder capital return.** Evidence: board
   approval on 2026-05-18 of a quarterly dividend increase from $0.01 to
   $0.25 per share and an additional $80.0 billion share-repurchase
   authorization (no expiration), against Q1 FY2027 free cash flow of
   $48.6 billion. Limitation: corroborated across multiple secondary
   sources (StreetInsider, TipRanks, The Motley Fool, Yahoo Finance), not
   directly rendered against NVIDIA's own 8-K in this pass.

## Risks — detail

Category framing (not a schema field, recorded here only, same convention
COST's, XOM's, and the original NVDA record established):
- Customer/hyperscaler concentration: structural/commercial
- Export control and geopolitical policy: regulatory/geopolitical
- Competition in AI accelerator hardware: competitive/structural
- Semiconductor manufacturing and advanced-packaging supply-chain
  concentration: operational/structural
- Architecture-generation transition execution: operational

**Customer/hyperscaler concentration — now more specifically quantified,
still not primary-source-verified.** Secondary synthesis of NVIDIA's Q1
FY2027 Form 10-Q describes three direct customers at approximately 21%,
17%, and 16% of total revenue (attributed primarily to the Compute &
Networking segment), plus separately disclosed indirect-customer
concentration arising from a limited number of cloud-service-provider
relationships. This is recorded as a third-party claim, not an established
fact — this record does not independently confirm these percentages
against the filed document itself, and does not name or speculate about
the identity of any specific customer beyond what is quantified above.

**Export-control and geopolitical policy — materially more active since
the original record.** Two distinct developments since 2026-07-18:
(1) a 2026-01-15 BIS final rule reported to shift H200/MI325X-class China
export-license review from presumption-of-denial to case-by-case,
conditioned on a 25% tariff, a 50% volume cap, third-party testing, and
KYC requirements, following a 2025-12-08 presidential announcement
permitting the change; Blackwell-class (B200) and Rubin-class products are
reported as remaining strictly restricted from China export. (2) A
2026-06-01 BIS guidance update reported to close a beneficial-ownership
loophole — extending export restrictions to any entity headquartered in,
or with an ultimate parent headquartered in, Country Group D:5 or Macau,
regardless of the entity's own physical location, closing a reported route
through Malaysia/Singapore/UAE-incorporated subsidiaries that may have
allowed some advanced-chip flow to Chinese-linked entities. Both
developments are sourced to secondary/trade-press reporting; this record
did not independently access BIS's own primary text (blocked, see
Source-access disclosure) and does not assert a specific revenue impact
figure for either development.

**Competition in AI accelerator hardware — a growing hyperscaler
custom-silicon dimension, not previously detailed.** NVIDIA is reported to
hold approximately 80% of the AI-accelerator market in 2026, but custom
ASICs from Google (TPU), Amazon (Trainium), Microsoft (Maia), and Meta
(MTIA) — largely co-designed with and fabricated via Broadcom/Marvell —
are reported as the faster-growing competitive threat, concentrated in
inference workloads specifically, alongside AMD's competing Instinct/MI400
line. This record does not adopt any specific future market-share
projection found in secondary sources as a fact; it records the reported
current competitive landscape only.

**Semiconductor manufacturing and advanced-packaging supply-chain
concentration.** NVIDIA is reported as TSMC's largest single allocation of
CoWoS-L advanced-packaging capacity (secondary industry estimates cite a
majority share of 2025-2026 CoWoS capacity), with industry-wide CoWoS
capacity reported as sold out into 2026 — a bottleneck this record treats
as a supply-side operational risk to NVIDIA's own shipment volumes, not a
demand-side concern.

**Architecture-generation transition execution.** Unchanged in kind from
the original record: each new compute-architecture generation (most
recently Blackwell, referenced in the Q1 FY2027 results above) carries ramp
timing and yield execution risk. No specific disclosed execution failure
was identified in this pass.

**Important limitation carried forward from the original record:** the
specific enumerated risk-factor text of NVIDIA's own Form 10-K/10-Q was
not independently inspected in this refresh pass either — the five risk
categories above remain understood from secondary coverage of NVIDIA's
disclosed condition, not confirmed word-for-word against NVIDIA's own
filed risk-factor language. This refresh adds more specific, dated
secondary evidence within each category; it does not close this
underlying evidentiary gap.

Observable indicators worth monitoring: quarterly Data Center segment
revenue trend and its compute/networking split, any further disclosed
customer-concentration commentary, any material export-control policy
development (particularly enforcement of the June 2026 guidance),
competitive product announcements from hyperscaler custom-silicon programs
and AMD, and architecture-generation ramp commentary.

## Catalyst

No catalyst entry is included in this record's structured schema, per the
existing convention — no specific future date is confirmed by this record
to the standard that would justify a dated `catalysts[]` entry. Q2 FY2027
results are expected around 2026-08-26 per secondary calendar aggregators;
this record explicitly treats that date as an unconfirmed estimate, not a
company-announced fact, consistent with the correction already applied to
COST's and XOM's own catalyst sections.

## Review framework

- **Cadence: 90 days.** Unchanged — matches COST's, XOM's, TSM's, ISRG's,
  TMO's, and GEV's cadence, and the `ai_infrastructure` theme's own
  cadence, for consistency across the corpus.
- **Unscheduled-review triggers** (qualitative, observable, same pattern
  the original record established):
  - A material, sustained deceleration or reversal in Data Center segment
    revenue
  - A disclosed material customer-concentration event
  - A material new export-control or geopolitical restriction, or a
    material enforcement development on the June 2026 guidance
  - A disclosed material execution failure in a new architecture
    generation's ramp
  - Evidence of material hyperscaler custom-silicon share erosion in
    inference workloads
  - A significant leadership change
- **Metrics worth monitoring each review:** quarterly Data Center segment
  revenue and its compute/networking split and growth rate, total company
  revenue, any disclosed customer-concentration commentary, free cash flow
  relative to the new capital-return posture (dividend and buyback pace),
  and any material regulatory or competitive development.

## Conviction

**Rating: High** (unchanged from the original record — this refresh does
not alter the rating; a rating change requires its own separate human
approval per PI-0018 Sec E).

**Rationale:** NVIDIA's Data Center segment revenue reached $75.2 billion
in Q1 FY2027 alone, up 92% year-over-year — an acceleration from FY2026's
own 68% YoY growth rate, and a continued demonstrated position in the
AI-infrastructure compute buildout. Conviction is High rather than Very
High because customer/hyperscaler concentration (now reported with
specific, if not yet primary-source-verified, percentages), export-control
and geopolitical exposure (more active since the original record, with a
January 2026 licensing change and a June 2026 loophole-closing guidance
update both reported since), and a growing hyperscaler custom-silicon
competitive threat concentrated in inference workloads are all real,
disclosed risk categories. This rating explicitly excludes valuation,
entry-price, allocation, trading, and margin judgments.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research — the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does. The PI-0017 committee review's own
advisory policy recommendation was "Keep current policy," not a rating
change, and this refresh does not treat that recommendation as license to
change the rating either.

## Theme membership

References the `ai_infrastructure` Theme Intelligence record
(`intelligence/themes/ai_infrastructure.yaml`/`.md`). NVDA is independently
a member of `targets.yaml`'s `semis` correlation cluster — a different
kind of information than this narrative theme reference. Per PI-0006's
frozen one-way-authority model, this file references the theme; the theme
file does not reference NVDA back. Theme membership does not imply
anything about NVDA's allocator treatment, tier weight, or cluster-cap
status, all of which remain governed exclusively by `targets.yaml`. This
refresh makes no change to theme membership or the theme record itself.

## Sources

See YAML `sources[]` for the structured register. The original record's
single primary-document citation (NVIDIA's Q4/FY2026 results press
release, disclosed as access-blocked) is preserved unchanged. This
2026-07-22 refresh adds five further entries, all explicitly labeled
SECONDARY in their `note` field, each identifying the primary document's
URL where one exists (NVIDIA's Q1 FY2027 press release and Form 10-Q, a
filing-mirror report of the 2026-05-18 board actions, and the two BIS
policy developments) while disclosing that direct rendering of every one
of them was blocked by this environment's network policy in this pass, not
merely assumed blocked. No source added by this refresh is treated as an
established fact independent of that disclosed limitation.
