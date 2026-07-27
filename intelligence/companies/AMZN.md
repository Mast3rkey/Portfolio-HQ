# AMZN — Amazon.com, Inc.

Last updated: 2026-07-26 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0027-ws0005-milestone3-batch5-hyperscaler-ai-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Amazon Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 5, alongside `MSFT`, `GOOGL`, and `META`
(`EQIX` explicitly deferred, not part of this batch).

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-26 were
blocked (HTTP 403) on every Amazon domain tested (`ir.aboutamazon.com`,
`aboutamazon.com`, `press.aboutamazon.com`), on SEC EDGAR, and on Amazon's
own Q4-IR-CDN-hosted PDF earnings release. **Zero primary documents were
opened directly by this session for AMZN.** Per `OPS-0008` Section 2's
mandatory stop-before-drafting gate, this session paused before drafting,
produced `BATCH5_SOURCE_READINESS_MANIFEST.md`, and the principal supplied
an independent evidence-recovery audit performed by **GPT-5.6 Thinking**
(2026-07-26). The original delivered predecessor audit had SHA-256
(`98d00c3c73805177c8301c680dee8dc06eee1b5caff5d4f250d13519051ab909`, the
"as-delivered" hash); this session independently verified that hash against
the two uploaded copies, then normalized trailing Markdown hard-line-break
whitespace only in the retained repository copy (no substantive content
changed) to clear this repository's `git diff --check` CI gate -- following
the same precedent already set by Batch 4's own retained audits. GPT-5.6
Thinking subsequently reissued this CI-clean text as the canonical retained
audit, and the repository contains that **canonical inspector reissue**, SHA-256
(`1ce03813cc3b855d8643708e56063653342476435cebafaf2f4b97ffd0f64ff7`); only
Markdown trailing whitespace differed from the predecessor artifact, and
substantive evidence text did not change; see `MSFT.md`'s own Source-access
disclosure for the full verification detail, not repeated per company here. This session also independently verified the
audit's own cited manifest checksum
(`8a9e943e0f189ea83d2c89fd34fdb263bd0c23ee49f9b49a2a81e08cc033a211`) before
relying on it. **Every fact below was directly inspected by GPT-5.6
Thinking, not by this Claude session** -- see `AMZN.yaml`'s `sources[]` for
per-document attribution.

## Business summary

Q1 2026 (quarter ended 2026-03-31): net sales **$181.519 billion**,
operating income **$23.852 billion**, net income **$30.255 billion**.

| Sales by category | Q1 2026 |
|---|---|
| Online stores | $64.254B |
| Third-party seller services | $41.578B |
| Advertising services | $17.243B |
| Subscription services | $13.427B |
| AWS | $37.587B |

| Segment | Q1 2026 sales | Q1 2026 operating income |
|---|---|---|
| North America | $104.143B | $8.267B |
| International | $39.789B | $1.424B |
| AWS | $37.587B | $14.161B |

**AWS is disproportionately the profit engine**: its Q1 2026 operating
income ($14.161B) **exceeded the combined operating income of the North
America and International retail segments** ($9.691B), even though AWS is
the smallest of the three segments by net sales. AWS sales grew **28%
YoY**, which Amazon attributed mainly to customer usage, partly offset by
long-term-contract pricing changes -- a real, disclosed margin-pressure
mechanism, not merely a growth headline.

## Capital intensity, liquidity, and debt

Q1 2026 cash capital expenditures were **$43.2 billion**, compared with
**$24.3 billion** in Q1 2025 -- nearly double, primarily technology
infrastructure (mostly supporting AWS growth) and fulfillment capacity.
Technology and infrastructure expense was **$29.567 billion, +29% YoY**.
Amazon stated technology/infrastructure spending was expected to increase
further as it adds infrastructure and employees, including for AI and
machine-learning initiatives (**forward-looking management expectation**).

At 2026-03-31, total cash, cash equivalents, and marketable securities
were **$143.089 billion**. At the same date, Amazon reported **$121.8
billion** of unsecured senior notes outstanding, including major
U.S.-dollar and euro issuances in **March 2026** -- new debt issuance
accompanying the capex acceleration in the same period; this record does
not establish use of proceeds, a causal funding relationship, or a change
in total debt, net-debt position, or leverage ratio. **AWS growth is not
capital-light** on this evidence, notwithstanding its high segment margin.

## AI-lab commitments (OpenAI and Anthropic)

Amazon disclosed that AWS and OpenAI **expanded an existing $38 billion
commercial arrangement by $100 billion over eight years**, including
obligations related to AWS-chip performance. **This is a contractual
company disclosure, not realized revenue.** Separately, Amazon invested
**$15 billion** in OpenAI Series C preferred stock in Q1 2026 and entered a
conditional commitment for an additional **$35 billion**. Amazon also
disclosed a cloud and model collaboration with OpenAI that includes AWS
cloud services and AWS chips.

Amazon disclosed cumulative Anthropic investments through Q4 2025, a
subsequent **$5 billion** preferred-stock investment, an amended AWS
arrangement with its own AWS-chip performance obligations, a **potential
financing facility of up to $20 billion**, and an **option for up to $5
billion** of future equity investment. **These are disclosed commitments
and options, not all deployed capital** -- this record does not count
conditional commitments or unexercised options as realized investment.

**These two relationships give Amazon exposure to more than one frontier
AI developer**, a structural difference from Microsoft's single deep
OpenAI relationship (covered in this same batch). The disclosed
arrangements, listed separately rather than summed into one total (the
categories overlap and are not economically interchangeable -- contract
value, equity investments, conditional commitments, financing facilities,
and options are each a different kind of exposure, and none is realized
revenue or fully deployed capital): the $100B, eight-year expanded AWS/
OpenAI commercial arrangement; the $15B OpenAI Series C preferred-stock
investment already made, plus a conditional $35B commitment; cumulative
Anthropic investments through Q4 2025 plus a subsequent $5B
preferred-stock investment; a potential $20B Anthropic financing facility;
and an option for up to $5B of further Anthropic equity investment. No
single additive exposure total is established by this record. This
combination of contractual, investment, and financing exposure is itself a
concentration of counterparty, financing, and delivery
(AWS-chip-performance-obligation) risk that this record does not treat as
pure upside.

## Regulatory evidence

The FTC and participating jurisdictions **allege** that Amazon uses
interlocking practices to maintain monopoly power in online superstores and
online marketplace services (matter numbers 1910129/1910130, civil action
2:23-cv-01495). **These remain government allegations in active
litigation, not adjudicated facts.** Amazon's own 10-Q states it is
litigating monopolization and consumer-protection claims brought by state
attorneys general and the FTC.

On **2026-06-25**, the European Commission announced a **preliminary**
view that AWS (and, separately, Azure) should be designated a Digital
Markets Act gatekeeper for cloud services, citing gateway importance,
entrenchment, switching costs, ecosystem breadth, and AI tools/partnerships.
**This is a regulator preliminary finding, not a final adjudicated
designation.**

## Risks -- detail

**Capex/debt escalation** -- capex nearly doubled YoY and is accompanied by
$121.8B of outstanding unsecured notes with major new March 2026
issuances; AWS growth is not capital-light.

**Profit concentration in AWS** -- AWS generated more Q1 2026 operating
income than the two retail segments combined, a disproportionate reliance
on a single segment for consolidated profitability.

**AI-lab commitment complexity** -- the combined disclosed OpenAI and
Anthropic commitments carry real counterparty, financing, and
chip-performance-delivery risk; contract amounts and options are not
equivalent to recognized revenue or fully deployed capital.

**Active FTC/state antitrust litigation** -- an unresolved, allegation-stage
matter, not an adjudicated fact.

**Preliminary EU cloud-gatekeeper exposure** -- see Regulatory evidence
above.

**Evidence-completeness gap:** this record does not confirm or deny any
specific named supplier relationship between Amazon and NVDA, TSM, AVGO,
AMD, or MRVL (all covered elsewhere in this repository's Company
Intelligence records) -- AMZN was named, unverified, as a hyperscaler
customer of some of those companies in Batch 1/3 records, and this record
establishes AMZN's own economics independently but does not itself resolve
that cross-reference, which was not quantified in any source this record
relies on.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, AMZN currently sits in the **T2** tier (1.65% target
weight per name) -- the only one of this batch's four companies at T2
rather than T1. AMZN is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality** is genuinely strong on the disclosed evidence: a
diversified retail/marketplace/advertising/subscription revenue base
layered with a disproportionately profitable AWS segment, very strong
liquidity ($143.089B), and demonstrated access to multiple frontier AI
developers rather than a single-counterparty bet.

**Capital priority is a separate question, and AMZN's own current T2
placement (1.65%, half of T1's 3.35%) is itself a data point this record
preserves as historical policy, not evidence.** AMZN competes for capital
priority against MSFT and GOOGL, the other two public-cloud sellers in this
batch -- AWS reported more disclosed quarterly segment operating income
than Google Cloud in the compared quarter ($14.161B versus GOOGL's $6.598B
in Q1 2026); the retained Microsoft evidence does not provide a directly
comparable quarterly Azure or Microsoft Cloud operating-income figure, so a
three-company cloud-profitability ordering cannot be established from this
record's evidence base. AMZN's consolidated business also carries the
lowest-margin retail
operations of the batch (North America and International operating margins
of roughly 7.9% and 3.6% respectively, per the segment table above),
diluting AWS's profitability at the consolidated level in a way MSFT's and
GOOGL's more software/services-weighted businesses do not experience to the
same degree. **What would be lost if AMZN were absent:** the specific
combination of the largest disclosed absolute-dollar cloud-segment
operating income in this batch with a genuinely diversified,
non-advertising-dependent consumer retail/marketplace/logistics business no
other company in this batch replicates. **Why the next dollar might not
favor AMZN specifically:** AMZN's own tier placement already reflects half
the per-name conviction weight of MSFT/GOOGL/META, and its combined
AI-lab financial commitments (OpenAI plus Anthropic) are, in aggregate
disclosed scale, the most complex and highest-counterparty-count exposure
in this batch -- a real, evidence-based reason capital priority could
reasonably remain at AMZN's current lower relative weight, without this
record itself making that recommendation. This record preserves that
uncertainty and recommends no tier, target, or allocation change.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Liquidity:** $143.089 billion cash/marketable securities at
  2026-03-31 (figures across this batch's four companies are reported at
  differing dates and instrument definitions and are not presented here as
  a cross-company ranking).
- **Capital intensity:** nearly doubled YoY -- Q1 2026 cash capex $43.2B
  vs. $24.3B Q1 2025, plus $29.567B of technology/infrastructure expense
  (+29% YoY).
- **Debt/leverage:** $121.8 billion of unsecured senior notes outstanding
  at 2026-03-31, including major new March 2026 issuances -- the only one
  of this batch's four companies with a specific, disclosed total
  outstanding-debt figure in this record's evidence base.
- **Cyclicality/drawdown history:** not established by any source this
  record relies on -- a disclosed evidence gap.
- **Correlated-loss relevance:** AMZN's AI-capex trajectory and its large
  OpenAI/Anthropic commitments connect it to the same AI-capex-slowdown
  risk named across MSFT/GOOGL/META in this batch's comparison artifact;
  AMZN's disclosed debt load is a distinct, additional correlated-risk
  channel (interest-rate/refinancing sensitivity) not established with the
  same specificity for the other three companies in this batch's evidence
  base.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- AWS growth decelerating materially or margin compression beyond the
  disclosed long-term-contract-pricing effect, given AWS's
  disproportionate share of consolidated operating income.
- A material adverse development in either the OpenAI or Anthropic
  relationship (a missed chip-performance obligation, a renegotiated or
  unwound commitment, or a disclosed impairment on the equity
  investments).
- A material adverse outcome in the FTC/state marketplace-monopolization
  litigation.
- The EU DMA cloud-gatekeeper matter finalizing with material
  interoperability, data-portability, or structural remedies for AWS.
- Retail-segment margins (North America/International) deteriorating in a
  way that further concentrates consolidated profitability in AWS beyond
  its already-disproportionate Q1 2026 share.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as public-cloud competitors across the sources this record relies on
and general industry knowledge: Microsoft Azure (covered in this same
batch), Google Cloud (covered in this same batch), Oracle Cloud
Infrastructure (not covered in this repository). **These are noted as
future research leads only, per `PI-0027` Section B.18 -- no holding add,
tier assignment, ranking, or further research is authorized by naming them
here.**

## Review framework

- **Cadence: 90 days** -- justified independently by Amazon's own quarterly
  (Form 10-Q) reporting rhythm, the source of the AWS-margin, capex, and
  debt-outstanding figures this record tracks, providing at least one
  re-inspection point before the FTC marketplace litigation's typical
  multi-quarter procedural pace would otherwise leave this record stale.
  This happens to match the cadence used for GEV, COST, XOM, Batch 4's
  ETN/VRT/PWR records, and this batch's MSFT/GOOGL/META records, but that
  consistency is incidental to, not the basis for, this record's own
  cadence choice.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - Quarterly earnings, specifically watching AWS margin trends and
    retail-segment operating-margin trajectory.
  - FTC/state marketplace-litigation developments.
  - The European Commission's final DMA cloud-gatekeeper determination for
    AWS.
  - Material developments (delivery milestones, renegotiation, impairment)
    in the OpenAI or Anthropic commitments.

## Conviction

**Rating: Medium.**

**Rationale:** Amazon shows a genuinely diversified revenue base layered
with a disproportionately profitable cloud segment -- AWS generated more
Q1 2026 operating income than the North America and International retail
segments combined -- and very strong liquidity. Conviction is held at
Medium rather than High because of concrete, current tensions: capital
expenditures nearly doubled year over year in the same period Amazon
carried a growing balance of unsecured notes outstanding -- the evidence
establishes both facts but not a causal funding relationship between them,
which this record treats as an unresolved inference, not an established
fact; Amazon's consolidated profitability is disproportionately
concentrated in a single segment; its multiple, very large AI-lab
commitments carry real counterparty, financing, and chip-performance-delivery
risk and are not equivalent to realized revenue or deployed capital; and
Amazon faces active FTC/state antitrust litigation alongside a preliminary
EU cloud-gatekeeper regulatory exposure. This rating excludes valuation,
entry-price, allocation, trading, and margin judgments, and does not treat
disclosed AI-lab contract amounts or options as realized revenue or capital
already deployed.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** at
  any point for AMZN -- every fact is sourced to GPT-5.6 Thinking's
  independent evidence-recovery audit.
- No specific named supplier relationship between Amazon and NVDA, TSM,
  AVGO, AMD, or MRVL was confirmed or quantified.
- Historical drawdown/cyclicality data was not established.
- Amazon's market share in cloud infrastructure or e-commerce was not
  quantified by any inspected source.
- The precise segment-level breakdown of Amazon's AI capital expenditure
  (as distinct from total technology/infrastructure spend) was not
  extracted from the inspected sources.

## Sources

See `AMZN.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit, with
that provenance stated explicitly -- this Claude session did not itself
open any primary document for AMZN.
