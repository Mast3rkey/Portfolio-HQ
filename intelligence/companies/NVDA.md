# NVDA — NVIDIA Corporation

Last updated: 2026-07-22 — evidence refresh authorized by
`governance/decisions/PI-0018-nvda-intelligence-refresh-authorization.md`,
following the PI-0017 committee review's Intelligence-maintenance
recommendation, with factual corrections applied following independent PR
review of the implementation PR (#126). Originally created 2026-07-18
through AI-assisted research and drafting, finalized through explicit
human review and approval under PI-0007. Portfolio HQ's third Portfolio
Intelligence record, and the first of two records created under the
`ai_infrastructure` Theme Intelligence pilot (`decision_log.yaml`
PI-0006/PI-0007).

## Source-access disclosure

**Research cutoff for this refresh: 2026-07-22.** This implementation
session directly tested `www.sec.gov`, `investor.nvidia.com`,
`nvidianews.nvidia.com`, `www.bis.gov`, `efts.sec.gov`, and
`www.congress.gov` and every one returned a network-policy
CONNECT-tunnel 403, confirmed against this environment's own proxy
relay-failure log (a policy denial at the gateway, not a site-side
rejection). This is the same access pattern already disclosed in the
original 2026-07-18 record for COST, XOM, and NVDA itself.

**Independent PR review subsequently rendered the primary sources this
session could not.** Across two rounds of independent review of
implementation PR #126, an independent reviewer directly rendered and
inspected NVIDIA's Q1 FY2027 press release and Form 10-Q, the BIS January
2026 licensing-policy announcement, the White House January 2026 tariff
proclamation, BIS's own May 31, 2026 guidance document (its full
substantive text, not merely its date), and NVIDIA's investor-relations
event-details page confirming the Q2 FY2027 results date — and supplied
the verified facts incorporated into this corrected version. Wherever
this record states a fact as primary-source-verified below, that
verification was performed during PR review, not by this implementation
session directly — this session's own attempts to render those same URLs
remained blocked throughout. As of this final correction pass, no
material claim in this record remains classified as unresolved; any fact
this record could not obtain to a confident, specific standard even with
that review's input would be retained as explicitly unresolved rather
than asserted, per the same discipline applied throughout this refresh.

## Business summary

NVIDIA supplies accelerated-compute hardware and networking platforms used
for AI training and inference at scale. For fiscal year 2026 (ended
2026-01-25): total revenue was $215.938 billion, up 65% year-over-year;
Data Center segment revenue was $193.7 billion, up 68% year-over-year.

**Q1 FY2027 (quarter ended 2026-04-26, reported 2026-05-20)** — the newest
reporting cycle since the original record — showed acceleration rather
than deceleration: total revenue $81.6 billion, up 85% year-over-year;
Data Center segment revenue a record $75.2 billion, up 92% year-over-year
and 21% sequentially (Data Center compute revenue $60.4 billion; Data
Center networking revenue $14.8 billion). GAAP gross margin was 74.9%;
GAAP operating income was $53.536 billion (+147% YoY) on GAAP operating
expenses of $7.6 billion (+52% YoY); GAAP net income was $58.321 billion
(+211% YoY) on **GAAP diluted EPS of $2.39** (non-GAAP diluted EPS $1.87
— the two are distinct figures and are not interchangeable). Operating
cash flow was $50.3 billion against capital expenditure of approximately
$1.8 billion, yielding free cash flow of $48.6 billion — NVIDIA returned
approximately $20.0 billion to shareholders in the quarter through
buybacks and dividends. NVIDIA's Q2 FY2027 financial-results event is
officially scheduled for **2026-08-26**, per NVIDIA's own investor-relations
event-details page, independently rendered and inspected during PR review
(this implementation session's own attempt to access `investor.nvidia.com`
remained blocked) — no longer treated as an unconfirmed estimate.

**Operating-income-to-net-income bridge (Q1 FY2027, per the Form 10-Q,
independently inspected during PR review):** operating income $53.536B;
interest income $0.540B; interest expense $0.102B; other income, net
$15.929B; total other income, net $16.367B; income before tax $69.903B;
income-tax expense $11.582B; net income $58.321B. The increase in other
income was primarily driven by $13.4 billion in unrealized gains on
publicly-held equity securities and $2.6 billion in unrealized gains on
non-marketable equity securities.

**Cash and investment position (Q1 FY2027, per the Form 10-Q):** cash and
cash equivalents $13.237 billion; marketable debt securities $37.098
billion (cash, cash equivalents, and marketable debt securities combined:
$50.335 billion); current marketable equity securities $30.237 billion;
long-term publicly-held equity securities of $8.864 billion reported
separately in Other assets. These categories are kept distinct rather
than collapsed into a single ambiguous total, per the filing's own
presentation.

**R&D expense (Q1 FY2027, per the Form 10-Q):** $6.321 billion.

**Corrected from the prior version of this refresh:** the prior version
of this record mislabeled non-GAAP diluted EPS ($1.87) as the GAAP figure;
the correct GAAP diluted EPS is $2.39. The prior version also left R&D
expense, the cash/marketable-securities position, and the
operating-income-to-net-income bridge as unresolved — all three are now
resolved above using the Form 10-Q's own figures, confirmed via
independent PR review.

**Corrected in this final pass:** the prior version also asserted that
Blackwell-class (B200) and Rubin-class products remain "strictly
restricted from China export" — an unsupported overstatement, now removed
and replaced in the Risks section below with the narrower facts the Form
10-Q itself supports. The 2026-05-31 BIS guidance, previously confirmed
only as to its date, is now fully primary-source-verified (see Risks
below), and the Q2 FY2027 earnings date is now an officially confirmed
fact rather than a secondary estimate (see above).

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
  now confirmed against the Q1 FY2027 Form 10-Q's own text as three
  direct customers at 21%/17%/16% of revenue and 30%/18%/16% of accounts
  receivable (see Risks below)
- Export-control or geopolitical policy does not materially restrict
  addressable market beyond what is currently disclosed — two distinct
  regulatory developments (a January 2026 BIS licensing-policy change and
  separate tariff proclamation, and further BIS guidance dated
  2026-05-31) predated but were not fully captured in the original
  2026-07-18 record
- Each new compute-architecture-generation transition executes without a
  material, disclosed ramp or yield problem
- NVIDIA's own disclosed risk that some customers are developing their
  own ASICs and workload-optimized products does not materially displace
  NVIDIA's position with those same customers

**Conditions that would weaken confidence in the above** (analytical
judgment, qualitative and observable, no numerical trigger):
- A material, sustained deceleration or reversal in Data Center segment
  revenue
- Evidence of material customer concentration risk materializing (a large
  customer meaningfully reducing orders)
- A material new export-control or geopolitical restriction, or evidence
  that the 2026-05-31 BIS guidance is not effectively enforced
- A disclosed, material execution failure in a new architecture
  generation's ramp
- Evidence that customer-developed ASICs are materially displacing
  NVIDIA's position faster than new architecture generations can offset

## Competitive advantages — detail

*(YAML holds concise claims only, per the frozen schema; fuller evidence
lives here.)*

1. **AI accelerated-compute hardware leadership, now with an accelerating
   growth rate.** Evidence: FY2026 Data Center segment revenue of $193.7
   billion (+68% YoY), followed by Q1 FY2027 Data Center segment revenue
   of $75.2 billion in a single quarter (+92% YoY, +21% sequentially),
   split $60.4 billion compute and $14.8 billion networking. These Q1
   FY2027 figures were independently inspected against NVIDIA's own press
   release and Form 10-Q during PR review; this implementation session's
   own attempt to render those documents directly remained blocked (see
   Source-access disclosure). The specific competitive-moat mechanisms
   (e.g., software ecosystem lock-in) were not independently verified
   against NVIDIA's own filed disclosures in this pass, same limitation as
   the original record.
2. **Materially expanded shareholder capital return.** Evidence: board
   approval on 2026-05-18 of a quarterly dividend increase from $0.01 to
   $0.25 per share and an additional $80.0 billion share-repurchase
   authorization (no expiration), against Q1 FY2027 free cash flow of
   $48.6 billion. Primary-source-verified via NVIDIA's own Q1 FY2027 press
   release, independently inspected during PR review; also corroborated
   across multiple secondary sources (StreetInsider, TipRanks, The Motley
   Fool, Yahoo Finance).

## Risks — detail

Category framing (not a schema field, recorded here only, same convention
COST's, XOM's, and the original NVDA record established):
- Customer/hyperscaler concentration: structural/commercial
- Export control and geopolitical policy: regulatory/geopolitical
- Competition in AI accelerator hardware: competitive/structural
- Supply-chain and manufacturing-capacity concentration: operational/structural
- Architecture-generation transition execution: operational

**Customer/hyperscaler concentration — now an established, primary-source-
verified fact, not a secondary estimate.** NVIDIA's Q1 FY2027 Form 10-Q
discloses that three direct customers represented 21%, 17%, and 16% of
total revenue, and three direct customers represented 30%, 18%, and 16%
of accounts receivable as of 2026-04-26 — customer identities are not
disclosed, and this record does not speculate about them. NVIDIA also
discloses indirect-customer revenue concentration arising from a limited
number of cloud-service-provider relationships. These figures were
independently inspected against the 10-Q's own text during PR review of
this implementation PR; this record no longer classifies them as a
third-party or secondary claim.

**Export-control and geopolitical policy — two distinct developments,
correctly dated, that predated but were not fully captured in the
original record.** (1) The Bureau of Industry and Security announced a
licensing-policy revision on 2026-01-13; the final rule took effect
2026-01-15, moving China export-license review for H200/MI325X-class and
similar qualifying chips from presumption-of-denial to case-by-case when
specified conditions are met: U.S. supply availability, no diversion of
foundry capacity from U.S. customers, purchaser compliance/customer
screening, and independent U.S. testing. Separately, a White House
proclamation dated 2026-01-14 imposed a 25% tariff on certain imported
advanced-computing chips, subject to stated exclusions — **this tariff is
a distinct action, not a condition of the BIS licensing rule**, and this
record does not conflate the two. Per NVIDIA's own Q1 FY2027 Form 10-Q
(independently inspected during PR review): licensing requirements
established in October 2023 covered B200 and other products exceeding
specified performance thresholds; beginning in February 2026 the U.S.
government granted licenses allowing small amounts of H200 products to be
shipped to specific China-based customers, though NVIDIA had generated no
revenue under this H200 licensing program as of the filing and did not
know whether imports would ultimately be allowed into China; licensed
H200 units require U.S. inspection before shipment; and NVIDIA stated
that, as of the end of Q1 FY2027, it was effectively foreclosed from
competing in China's data-center compute market. **No Rubin-specific
China-export restriction is asserted here** — the original record's
"Rubin-class products remain strictly restricted" claim was removed as
unsupported by any dedicated primary source. (2) BIS issued further
guidance on export-restriction scope for advanced-computing items dated
**2026-05-31**, independently rendered and inspected during PR review:
the official one-page guidance states, in BIS's own language, that a
license is required to export advanced-computing items to entities
headquartered in Country Group D:5 or Macau, or to entities whose
ultimate parent is headquartered in Country Group D:5 or Macau, even
where the entity itself is located outside those destinations. This is
now a primary-source-verified fact, not a secondary characterization —
the prior version's "beneficial-ownership loophole" framing and its
dependency on a secondary news article are both removed in favor of the
guidance's own stated language.

**Competition in AI accelerator hardware — now grounded in NVIDIA's own
risk-factor language rather than unsourced market-share precision.** Per
NVIDIA's Q1 FY2027 Form 10-Q (independently inspected during PR review):
some customers are developing their own ASICs and other
workload-optimized products, and competition may adversely affect
NVIDIA's market share and financial results. This record does not assert
a specific market-share percentage (e.g., an "~80%" figure), a
"faster-growing" comparative claim, or an inference-workload-concentration
claim for competing custom silicon — each was removed because it lacked a
specific, fully classified source entry (issuer, title, date, URL,
classification, and exact claim supported) sufficient to state it as
fact.

**Supply-chain and manufacturing-capacity concentration — now grounded in
NVIDIA's own risk-factor language.** Per NVIDIA's Q1 FY2027 Form 10-Q
(independently inspected during PR review): competitors and customers may
constrain NVIDIA's ability to procure foundry capacity and scarce inputs;
NVIDIA has experienced manufacturing lead times exceeding 12 months; and
foundry partners and contract manufacturers may be unable to provide
sufficient capacity. This record no longer asserts a specific named
foundry-partner capacity-allocation percentage or a "sold out through
2026" characterization, since neither was backed by a specific, fully
classified source at the standard this record now applies.

**Architecture-generation transition execution.** Unchanged in kind from
the original record: each new compute-architecture generation (most
recently Blackwell, referenced in the Q1 FY2027 results above) carries ramp
timing and yield execution risk. No specific disclosed execution failure
was identified in this pass.

**Important limitation carried forward from the original record:** the
specific enumerated risk-factor text of NVIDIA's own Form 10-K was not
independently inspected in the original 2026-07-18 pass; this refresh's
independent PR review did directly inspect the Q1 FY2027 Form 10-Q's own
risk-factor and financial-statement text (see entries above), narrowing
but not fully closing that original gap — the FY2026 Form 10-K's own text
remains uninspected.

Observable indicators worth monitoring: quarterly Data Center segment
revenue trend and its compute/networking split, any further disclosed
customer-concentration commentary, any material export-control policy
development (particularly enforcement of the 2026-05-31 BIS guidance),
competitive product announcements from customers developing their own
silicon, and architecture-generation ramp commentary.

## Catalyst

NVIDIA's Q2 FY2027 financial-results event is officially scheduled for
**2026-08-26**, confirmed via NVIDIA's own investor-relations event-details
page, independently rendered and inspected during PR review (see YAML
`sources[]`) — this is now a company-confirmed fact, not a secondary
estimate. No `catalysts[]` entry is added to this record's structured
schema for it, consistent with the existing corpus convention (no company
record in this corpus currently populates `catalysts[]` with a dated
entry); the confirmed date is instead recorded here and in the source
register, the same treatment already applied to every other confirmed-date
development in this record.

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
    material enforcement development on the 2026-05-31 BIS guidance
  - A disclosed material execution failure in a new architecture
    generation's ramp
  - Evidence of material displacement by customer-developed ASICs
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
High because customer/hyperscaler concentration (now confirmed against the
Q1 FY2027 Form 10-Q's own text: three direct customers at 21%/17%/16% of
revenue and 30%/18%/16% of accounts receivable), export-control and
geopolitical exposure (a January 2026 BIS licensing-policy change and
separate tariff proclamation, both predating but not fully captured in
the original 2026-07-18 record, plus further BIS guidance dated
2026-05-31), and competition from customers developing their own ASICs
(per NVIDIA's own risk-factor disclosure) are all real, disclosed risk
categories. This rating explicitly excludes valuation, entry-price,
allocation, trading, and margin judgments.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research — the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does. The PI-0017 committee review's own
advisory policy recommendation was "Keep current policy," not a rating
change, and this refresh does not treat that recommendation, nor the
independent PR review's factual corrections, as license to change the
rating either.

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
2026-07-22 refresh adds further entries: NVIDIA's Q1 FY2027 press release
and Form 10-Q, a BIS licensing-policy announcement, a White House tariff
proclamation, BIS's own May 31, 2026 guidance, and NVIDIA's
investor-relations event-details page confirming the Q2 FY2027 results
date — each labeled `PRIMARY` in the YAML `note` field, reflecting that
these documents were independently rendered and inspected during PR
review of this implementation PR, even though this implementation
session's own direct-access attempts against every one of them remained
blocked (see Source-access disclosure). Following the final correction
pass, the May 31 BIS guidance entry is fully primary-source-verified as
to both its date and its own substantive text — the guidance's own
language, not a secondary characterization, is what this record now
states. One remaining secondary-only entry (a filing mirror of the
2026-05-18 board actions) is retained as corroboration, not as the sole
basis for facts that are otherwise primary-source-verified.
