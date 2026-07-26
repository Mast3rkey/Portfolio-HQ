# META — Meta Platforms, Inc.

Last updated: 2026-07-26 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0027-ws0005-milestone3-batch5-hyperscaler-ai-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Meta Company Intelligence record existed). Portfolio HQ's
WS-0005 Milestone 3 Batch 5, alongside `MSFT`, `GOOGL`, and `AMZN` (`EQIX`
explicitly deferred, not part of this batch).

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-26 were
blocked (HTTP 403) on every Meta domain tested (`investor.fb.com`,
`investor.atmeta.com`, `about.fb.com`, `about.meta.com`) and on SEC EDGAR.
**Zero primary documents were opened directly by this session for META.**
Per `OPS-0008` Section 2's mandatory stop-before-drafting gate, this session
paused before drafting, produced `BATCH5_SOURCE_READINESS_MANIFEST.md`, and
the principal supplied an independent evidence-recovery audit performed by
**GPT-5.6 Thinking** (2026-07-26), retained verbatim at
`governance/audits/BATCH5_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260726.md`.
This session independently verified the delivered file's SHA-256
(`98d00c3c73805177c8301c680dee8dc06eee1b5caff5d4f250d13519051ab909`, the
"as-delivered" hash) against the two uploaded copies, then normalized
trailing Markdown hard-line-break whitespace only in the retained repository
copy (no substantive content changed) to clear this repository's
`git diff --check` CI gate -- following the same precedent already set by
Batch 4's own retained audits -- yielding a different, "as-retained" SHA-256
(`1ce03813cc3b855d8643708e56063653342476435cebafaf2f4b97ffd0f64ff7`); see
`MSFT.md`'s own Source-access disclosure for the full verification detail,
not repeated per company here. This session also independently verified the
audit's own cited manifest checksum
(`8a9e943e0f189ea83d2c89fd34fdb263bd0c23ee49f9b49a2a81e08cc033a211`) before
relying on it. **Every fact below was directly inspected by GPT-5.6
Thinking, not by this Claude session** -- see `META.yaml`'s `sources[]` for
per-document attribution.

## Business summary

Q1 2026 (quarter ended 2026-03-31): total revenue **$56.311 billion, +33%
YoY**; operating income **$22.872 billion**. Advertising revenue was
**$55.024 billion**; Family of Apps total revenue was **$55.909 billion**
-- advertising is essentially the entire disclosed revenue base, roughly
**98%** of total revenue.

| Segment | Q1 2026 |
|---|---|
| Family of Apps operating income | $26.900B |
| Reality Labs operating loss | $(4.028)B |

Growth came from both volume and pricing: ad impressions **+19% YoY**,
average price per ad **+12% YoY**. Average Family daily active people were
**3.56 billion** in March 2026, **+4% YoY**. FY2025 (per Meta's own Form
10-K): Family of Apps operating income **$102.469 billion**; Reality Labs
operating loss **$19.193 billion**.

## AI investment and infrastructure

**Meta discloses no customer-facing public-cloud business** -- a structural
difference from MSFT, GOOGL, and AMZN in this same batch. Meta's AI
investment, per its own Q1 2026 filing, includes third-party cloud
capacity, servers, data centers, network infrastructure, generative AI,
"superintelligence," content recommendation, advertising tools, and product
development -- entirely directed at Meta's own products and operations,
with no disclosed avenue to resell excess AI infrastructure capacity to
third parties.

Meta anticipated approximately **$125 billion to $145 billion** of 2026
capital expenditures to support AI efforts and the core business --
**forward-looking guidance**, not a realized figure. Q1 2026 capital
expenditures, including principal payments on finance leases, were
**$19.84 billion**. Q1 2026 R&D expense was **$17.699 billion, +46% YoY**,
partly attributed to employee compensation and AI-related infrastructure --
an expense-growth rate outpacing the quarter's own +33% revenue growth,
worth monitoring though not yet evidence of margin deterioration (operating
income also grew).

Meta's FY2025 Form 10-K reports ownership of **30 data-center locations
globally**, alongside use of some leased data centers -- a disclosed,
tangible infrastructure footprint.

**This record's evidence base could not establish the scale or economics
of Meta's own custom-silicon (MTIA) program.** This is a genuine,
disclosed evidentiary gap relative to MSFT (Maia/Cobalt), GOOGL (TPU), and
AMZN (AWS-chip obligations in its OpenAI/Anthropic arrangements) in this
same batch -- this record does not assert MTIA deployment scale or
performance without a separate official source.

## Reality Labs

Reality Labs revenue declined **2%** in Q1 2026 -- lower Quest sales
partly offset by higher AI-glasses sales. The segment's operating loss was
**$4.028 billion** in Q1 2026 alone, against a **$19.193 billion** FY2025
full-year loss. Meta expects full-year 2026 Reality Labs operating losses
to remain **similar to 2025** -- **forward-looking management guidance**,
not a resolved trajectory toward profitability. This record treats Reality
Labs as a large, persistent capital allocation to a loss-making segment
with no disclosed near-term profitability path in any source it relies on.

## Business dependencies

Meta's own filing identifies advertising as its primary revenue source and
states that platform and regulatory changes can impair ad targeting and
measurement. **Apple's platform-policy changes have already negatively
affected ad targeting and measurement** and may continue to affect
marketer budgets, per Meta's own disclosure -- this is an **already-realized
impact**, not a hypothetical risk, and it is the single most concrete,
company-disclosed dependency this record identifies for META.

## Regulatory evidence

The district court entered judgment **in Meta's favor** in **November
2025** in the FTC personal-social-networking monopolization case. **The
FTC filed a notice of appeal on 2026-01-20**, and continues to allege Meta
maintained a personal-social-networking monopoly through the Instagram and
WhatsApp acquisitions. **This is the regulator's allegation on appeal, not
an adjudicated fact** -- Meta currently holds the trial-level win, a
materially different current posture than GOOGL's or AMZN's still-pending
matters in this batch, though the appeal itself remains a live, unresolved
risk.

## Risks -- detail

**Extreme single-revenue-stream concentration** -- advertising is roughly
98% of disclosed revenue, with an already-realized negative platform-policy
impact (Apple) disclosed by the company itself, not merely a hypothetical
risk.

**No public-cloud offset for AI capex** -- Meta's very large guided 2026
capex ($125B-$145B) must be recovered entirely through Meta's own product,
advertising, and Reality Labs improvements; MSFT, GOOGL, and AMZN can, at
least in principle, monetize excess AI infrastructure capacity through
their public-cloud businesses, an option this record found no evidence
Meta has.

**Reality Labs persistent, large, guided-to-continue loss** -- see above.

**Custom-silicon evidence gap** -- MTIA's scale and economics were not
established by any source this record relies on.

**R&D expense growth outpacing revenue growth** -- +46% YoY vs. +33%
revenue growth in Q1 2026, worth monitoring.

**FTC appeal remains live** -- see Regulatory evidence above.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, META currently sits in the **T1** tier (3.35% target
weight per name). META is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality**, on disclosed growth metrics, is the strongest of
this batch's four companies: +33% revenue growth, +19% ad impressions,
+12% price per ad, and a very large, high-margin Family of Apps segment
(FY2025 operating income $102.469B) funding Meta's own large discretionary
AI and Reality Labs investment without external financing evident in this
record.

**Capital priority is a separate, and here materially different, question.**
META carries the same 3.35% T1 target weight as MSFT and GOOGL, but its
risk concentration is structurally different: a single revenue stream
(~98% advertising) with an already-realized platform-dependency impact, no
public-cloud business to offset its very large AI capex commitment, a
persistent nine-figure-billion-dollar Reality Labs loss with no disclosed
profitability path, and this record's own inability to establish its
custom-silicon program's economics. **What would be lost if META were
absent:** the specific combination of the largest disclosed social/messaging
platform reach in this batch (3.56 billion average Family daily active
people) with an advertising-technology franchise that does not overlap in
kind with MSFT's/GOOGL's/AMZN's public-cloud businesses -- this is
genuinely distinct exposure, not duplicative of the other three. **Why the
next dollar might not favor META specifically:** unlike MSFT, GOOGL, and
AMZN, META has no disclosed avenue to monetize its AI infrastructure
buildout beyond its own advertising and product improvements, meaning its
very large capex commitment carries more concentrated execution risk with
fewer disclosed fallback monetization paths if internal AI-driven ad
improvements underperform expectations -- a real, evidence-based
distinction from its three cloud-selling peers in this batch, not a
prediction of outcome. This record preserves that uncertainty and
recommends no tier, target, or allocation change.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Liquidity:** $81.18 billion cash/marketable securities at 2026-03-31 --
  the smallest liquidity figure disclosed among this batch's four
  companies, though still very large in absolute terms.
- **Capital intensity:** Q1 2026 capex (including finance-lease principal)
  $19.84B, with a guided 2026 full-year range of $125B-$145B -- the
  broadest guided range of the four companies in this batch, reflecting
  greater disclosed uncertainty in Meta's own capex planning.
- **Debt/leverage:** not established by any source this record relies on
  -- a disclosed evidence gap.
- **Cyclicality/drawdown history:** not established by any source this
  record relies on -- a disclosed evidence gap.
- **Correlated-loss relevance:** META's AI-capex trajectory is one of the
  shared mechanisms named in the Batch 5 comparison artifact as a common
  risk across MSFT/GOOGL/META/AMZN; unlike the other three, META's capex
  has no public-cloud revenue to offset it if the AI-capex cycle slows,
  which this record treats as a materially different correlated-loss
  exposure, not merely the same risk restated.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A material deterioration in advertising demand or pricing, given the
  ~98% revenue concentration in that single stream.
- Further Apple (or another major platform) policy changes materially
  impairing ad targeting/measurement beyond what is already disclosed.
- Reality Labs losses widening materially beyond the "similar to 2025"
  guidance, or a disclosed strategic reassessment of Reality Labs' role.
- 2026 AI capex realizing at or above the top of the guided $125B-$145B
  range without a corresponding, evidence-based improvement in disclosed
  ad-revenue growth or efficiency.
- An adverse outcome in the FTC's appeal reversing Meta's current
  trial-level win.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as digital-advertising and social-platform competitors across the
sources this record relies on and general industry knowledge: Alphabet
(Google/YouTube advertising, covered in this same batch), TikTok/ByteDance
(not covered in this repository), Snap Inc. (not covered in this
repository). **These are noted as future research leads only, per
`PI-0027` Section B.18 -- no holding add, tier assignment, ranking, or
further research is authorized by naming them here.**

## Review framework

- **Cadence: 90 days** -- matches the existing cadence used for GEV, COST,
  XOM, Batch 4's ETN/VRT/PWR records, and this batch's MSFT/GOOGL records.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - Quarterly earnings, specifically watching advertising growth
    durability and Reality Labs' loss trajectory against guidance.
  - The FTC's appeal of the November 2025 district-court judgment.
  - Full-year 2026 capex realization against the guided $125B-$145B range.
  - Any disclosed development on Meta's own custom-silicon (MTIA) program
    that would close this record's current evidence gap.

## Conviction

**Rating: Medium.**

**Rationale:** Meta shows the strongest recent growth momentum of this
batch on disclosed metrics and a very large, high-margin core Family of
Apps segment funding its own large AI/Reality Labs investment without
external financing evident in this record. Conviction is held at Medium,
not High, because Meta carries the most concentrated risk profile of the
four companies in this batch on the evidence available: advertising is
roughly 98% of disclosed revenue with an already-realized negative impact
from Apple's platform-policy changes; Meta has no public-cloud-resale
business to offset its very large guided AI capex, unlike MSFT, GOOGL, and
AMZN; Reality Labs is a large, persistent loss guided to continue at a
similar scale in 2026; and this record's evidence base could not establish
Meta's own custom-silicon program's scale or economics. This rating
excludes valuation, entry-price, allocation, trading, and margin
judgments, and treats the FTC's continuing appeal as an unresolved
allegation, not a settled matter, notwithstanding Meta's current
trial-level win.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** at
  any point for META -- every fact is sourced to GPT-5.6 Thinking's
  independent evidence-recovery audit.
- Meta's custom-silicon (MTIA) program's scale and economics were not
  established.
- Meta's debt/net-debt position and historical drawdown/cyclicality data
  were not established.
- The precise revenue attributable to AI-glasses versus Quest within
  Reality Labs was not extracted from the inspected sources.
- Meta's market share in digital advertising or social networking was not
  quantified by any inspected source.

## Sources

See `META.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit, with
that provenance stated explicitly -- this Claude session did not itself
open any primary document for META.
