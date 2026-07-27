# MA — Mastercard Incorporated

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Mastercard Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 6, alongside `V` and `JPM`.

**Correction notice (2026-07-27):** this record was corrected in a bounded
pass following GPT-5.6 Thinking's independent exact-head review of PR #171
(verdict CHANGES REQUIRED) and its accompanying primary-source addendum,
retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`.
The correction adds several previously-missing `PI-0028`-mandatory
research fields, removes an unsupported relative-to-Visa conviction
rationale, corrects provenance language, and reassesses conviction
independently. See `MA.yaml`'s `review.log` for the full correction note.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were
blocked (HTTP 403) on SEC EDGAR, Mastercard's investor-relations domain,
and a neutral, non-target control domain (`example.com`) -- confirming a
session-wide network-policy denial rather than a domain-specific failure,
matching V's and JPM's own disclosed blocks in this same batch. Per
`OPS-0008` Section 2's mandatory stop-before-drafting gate, this session
paused before drafting.

The principal supplied an independent primary-source evidence-recovery
audit performed by **GPT-5.6 Thinking** (2026-07-27). The as-delivered
audit file had SHA-256
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a`
(17,693 bytes, 225 lines), independently verified by this session before
use. **The repository retained a substantively unchanged copy after
trailing-whitespace normalization** (six lines, header block only --
required to clear this repository's `git diff --check` CI gate), which
carries SHA-256
`ee497ac6323e25df5e0aa5cc3473e692c8566a84f0f2150a424d25d3a95bf9d8`
(17,681 bytes, 225 lines). Both hashes are disclosed together because the
files are not byte-identical; no content beyond trailing whitespace
differs. The Claude implementation session did not directly inspect the
cited primary documents in either the original audit or this correction's
addendum.

A second, bounded correction addendum, also authored by **GPT-5.6
Thinking**, was supplied for this pass and is retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`
(this Claude session verified its as-delivered SHA-256,
`5b8e89ad4f207b87b07c344d0e28e2338f2551965a929a6e540410fd2782b59c`
(15,090 bytes, 351 lines), before use, then normalized trailing Markdown
whitespace in the retained repository copy only -- no substantive content
changed -- to clear this repository's `git diff --check` CI gate; the
retained copy carries SHA-256
`4922290196e273f964003537b92a64f21cdc1cc88a5bc4fb4c87ce8265db9b6e`
(15,062 bytes, 351 lines)). **Every fact below was directly inspected by GPT-5.6 Thinking, not by
this Claude session** -- see `MA.yaml`'s `sources[]` for per-document
attribution.

## Business summary

Mastercard classifies its net revenue into two categories: **payment
network** and **value-added services and solutions**. Payment-network
revenue is generated primarily from fees based on gross dollar volume
(GDV) and from switching and network services -- **the same fundamental
network-toll-road mechanism Visa uses** (see V.md and the comparison
artifact for the direct comparison `PI-0028` Section B.19 requires).

**Fiscal 2025** payment-network net revenue was **$19.476 billion** and
value-added-services-and-solutions net revenue was **$13.315 billion**.
Value-added services span security, digital and authentication solutions,
consumer acquisition and engagement, business and market insights,
processing and gateway services, account-based payments, real-time
payments, and open finance -- a broader disclosed product set than this
record independently verifies for Visa.

**Q1 2026** (furnished 2026-04-30): total net revenue **$8.398 billion, up
16%**; payment-network revenue **+12%**; value-added-services-and-solutions
revenue **+22%** -- growing faster than the core network segment. On a
local-currency basis, GDV grew **7% to $2.7 trillion**, cross-border volume
grew **13%**, and switched transactions grew **9%**.

## Financial quality and capital allocation (added in this correction)

For fiscal 2025, per Mastercard's Form 10-K: **operating margin 57.6%**;
**net income $14.968 billion**; **operating cash flow $17.648 billion**;
purchases of property and equipment of **$0.489 billion** plus capitalized
software of **$0.726 billion**. Reviewer arithmetic (operating cash flow
less those two items -- not an issuer-defined free-cash-flow measure):
**approximately $16.433 billion** available before capital return.

**Debt:** total debt **$19.000 billion**; long-term debt **$18.251
billion** (FY2025).

**Capital return:** FY2025 share repurchases of **$11.727 billion** and
dividends paid of **approximately $2.8 billion**, for **total capital
returned to stockholders of approximately $14.5 billion** -- on the
evidence inspected, funded from operating cash flow.

**Management:** Michael Miebach has served as President and Chief
Executive Officer since January 2021; the filing records prior Mastercard
operating roles including President and Chief Product Officer. **Tenure
and internal experience are facts; execution quality and acquisition
discipline remain judgments** this record does not resolve from the
filing alone.

## Rebates and incentives -- a growing competitive cost

**Q1 2026 payment-network rebates and incentives rose 23%** (**19%** on a
currency-neutral basis) -- **faster than payment-network revenue growth
(12%)** in the same quarter. This is Mastercard's equivalent of Visa's
client incentives, and this record treats it the same way: a real,
disclosed competitive cost of sustaining and renewing customer
relationships, and one whose growth rate outpacing revenue growth in the
most recent quarter is a specific, current margin-pressure signal.

**This record does not have a directly comparable current Visa
incentive-growth-rate figure.** V.md's own client-incentive discussion
(corrected in this same pass) establishes a FY2025 *level* (≈28.25% of
pre-incentive gross revenue) but not a comparable *growth rate*. This
record therefore treats the Q1 2026 rebates/incentives-outpacing-revenue
signal as **Mastercard-specific evidence**, not as proof that Visa's
comparable trend is better -- absence of a comparable Visa figure is not
evidence of a better Visa trend.

## Geography, product mix, and dependencies (added in this correction)

Mastercard's FY2025 Form 10-K discloses net revenue split between the
**Americas** and **APEMEA** (Asia Pacific, Europe, Middle East, and
Africa) regions, and GDV disclosed across **consumer credit, consumer
debit/prepaid, and commercial** products. This record preserves that
these disclosures exist in the 10-K without restating the exact
percentage splits here, since the correction addendum did not itself
extract those specific figures -- a narrower, disclosed limitation than
the original record's blanket "not established" statement.

**Dependencies:** Mastercard depends on **issuers**, **acquirers**,
**merchants**, **processors**, **settlement banks**, and other network
participants. **Settlement and counterparty exposure is a distinct
dependency from ordinary consumer credit risk** -- Mastercard, like Visa,
does not extend consumer credit itself.

## Competitors, substitutes, and cyber/operational risk (added in this correction)

Disclosed competitors and substitutes: **Visa**, **American Express** and
other closed-loop systems, domestic (in-country) payment networks,
account-to-account/real-time-payment systems, digital wallets, fintech
platforms, and emerging alternative rails. This record does not quantify
market-share movement to any of these categories.

**Cyber, operational resilience, fraud, authentication, and
data-security** risks are disclosed as material per the 10-K's own
risk-factor discussion -- a standing structural risk category for a
network and settlement business of Mastercard's scale, not evidence of an
active incident.

## Regulatory and litigation evidence

Mastercard's Form 10-Q for the quarter ended 2026-03-31 states that
interchange fees and acceptance practices face regulatory and legal
challenges in multiple jurisdictions and may materially affect growth and
results. Current disclosed matters include:

- U.S. interchange opt-outs;
- U.K. and pan-European merchant claims;
- Portuguese and Dutch proceedings;
- other, unspecified regulatory matters.

**This is a broader, more jurisdictionally dispersed litigation/regulatory
footprint than this record establishes for Visa**, whose disclosed matters
(the DOJ debit-network case and U.S. interchange litigation) are more
concentrated in the United States. **This record does not quantify the
aggregate dollar exposure of either company's litigation footprint and
does not treat greater jurisdictional dispersion alone as proof of
greater expected liability** -- it is recorded as a distinct, disclosed
risk-profile shape, not a ranking.

## Demonstrated downturn behavior (added in this correction)

Mastercard's fiscal-2020 Form 10-K (fiscal year ended 2020-12-31) provides
an observed stress case, used here as **historical evidence, not a
forecast**: fiscal-2020 net revenue declined **approximately 9%**;
cross-border volume declined **approximately 29%**; operating margin fell
from **57.2% to 52.8%**; net income declined **approximately 21%**; **the
company remained profitable** throughout. **This is a materially sharper
decline than Visa's own disclosed fiscal-2020 figures** (net revenue -5%,
net income -10%, per V.md) in the same downturn -- one company-specific
data point suggesting greater cyclicality for Mastercard in at least this
one observed stress episode, not an assumption that the two companies are
equally cyclical.

## Risks -- detail

**Rebates/incentives outpacing network-segment revenue growth** -- a
current, quarter-specific margin-pressure signal, evaluated on its own
terms (see above), not as comparative proof against Visa.

**Multi-jurisdiction regulatory/litigation exposure** -- broader in
disclosed geographic spread than Visa's; aggregate dollar exposure not
established for either company.

**Shared network-economics risk with Visa** -- see the comparison
artifact for the shared-mechanism risk discussion.

**Issuer/acquirer/settlement dependency and cyber/operational risk** --
see above.

**Competitive/substitution risk** -- see above; disclosed categories, not
quantified market-share movement.

**Cross-border and downturn sensitivity** -- Mastercard's own fiscal-2020
downturn (above) was materially sharper than Visa's in the same period.

**Narrowed but not eliminated evidence-completeness gap** -- exact
geographic and GDV-mix percentages, and multi-year
capital-allocation/acquisition-integration execution quality, remain
unestablished from the sources inspected.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, MA currently sits in the **T2** tier (1.65% target
weight per name) -- half V's T1 per-name weight. MA is **not** a member of
any `targets.yaml` correlated-cluster cap. This placement is recorded here
as **existing governed policy, preserved as a historical comparison
baseline only, per `OPS-0006` Sections 2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion in
this record, and this record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality**, per the evidence above, is strong and closely
parallels Visa's: a durable, growing network-toll-road business with a
larger disclosed value-added-services share than this record establishes
for Visa, value-added services growing faster than the core network
segment, and now-established financial quality (large operating cash flow
relative to capex, an own-cash-flow-funded capital-return program of
approximately $14.5 billion in FY2025).

**Capital priority is a separate question.** MA carries T2's standard
1.65% per-name target, historically half V's T1 weight -- **this record
does not independently re-derive whether that differential is
evidence-supported**; it is recorded as existing governed policy per
`OPS-0006` Sections 2-3. **What would be lost if MA were absent from the
book:** to a real degree, not much that V does not already provide -- both
are payment-network businesses sharing the same fee-based GDV/switching
mechanism (see the comparison artifact Section 1 for the direct
comparison). MA's own scale, geographic mix, and larger disclosed
value-added-services emphasis are the primary sources of distinct exposure
this record can identify; whether that distinction is sufficient to
justify holding both V and MA, versus one alone, **is not resolved by this
record** -- it is preserved as an open, evidence-based question in the
comparison artifact, consistent with `PI-0028` Section B.17's requirement
to separate business quality from capital priority without producing a
ranking.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Revenue/volume cyclicality:** GDV, cross-border volume, and switched
  transactions all grew through Q1 2026; Mastercard's fiscal-2020 downturn
  (above) is the best available historical evidence of behavior in a
  broad contraction, and it was materially sharper than Visa's in the same
  period.
- **Balance-sheet/leverage:** total debt $19.000B / long-term debt
  $18.251B (FY2025) is now established; a complete liquidity/current-ratio
  picture and any post-FY2025 issuance are not established by any source
  this record relies on.
- **Rebate/incentive-driven margin pressure:** the Q1 2026
  rebates-outpacing-revenue signal is a disclosed, current, Mastercard-
  specific margin consideration.
- **Correlated-loss relevance:** MA shares its core network-toll-road
  mechanism with V, covered in the same batch -- see the comparison
  artifact for the shared-mechanism risk discussion (interchange
  regulation, fraud/cybersecurity exposure, alternative-payment-rail
  competition).

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A material adverse ruling, settlement, or structural remedy in any of
  the disclosed multi-jurisdiction interchange/regulatory matters (U.S.,
  U.K., pan-European, Portuguese, Dutch).
- Sustained deceleration in GDV, cross-border-volume, or
  switched-transaction growth relative to the Q1 2026 trend, or a
  fiscal-2020-scale contraction recurring.
- Rebates and incentives continuing to grow structurally faster than
  payment-network revenue over multiple consecutive quarters (confirming,
  rather than a one-quarter signal, a durable margin-compression trend).
- A material competitive displacement by an alternative payment rail, the
  same industry-level risk named in V's own thesis-break conditions.
- A material cyber, fraud, or settlement/operational-resilience failure.

## Disconfirming evidence actively searched (added in this correction)

This record's underlying evidence was reviewed specifically for evidence
that would weaken the network-quality thesis, recorded whether or not
each item was found:

- **Rebates/incentives persistently outgrowing network revenue** -- found:
  Q1 2026 shows exactly this (23% vs. 12%); recorded as a live risk above,
  not yet established as a multi-quarter trend.
- **Value-added services failing to sustain margins or organic growth** --
  not found; Q1 2026 shows value-added-services revenue growing faster
  (22%) than the network segment (12%).
- **Issuer/acquirer disintermediation** -- no specific instance disclosed
  in the sources inspected.
- **Alternative-rail substitution at scale** -- disclosed as a competitive
  category; no quantified market-share loss found.
- **Multi-jurisdiction regulatory or litigation adverse outcomes** --
  found: the disclosed U.S./U.K./pan-European/Portuguese/Dutch matters are
  the concrete instances of this risk category, magnitude unquantified.
- **Cyber, fraud, settlement, or reliability failures** -- none disclosed
  in the sources inspected.
- **Acquisition dependence or weak return on acquired assets** -- not
  established either way from the sources inspected; a genuine open item.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as a direct payment-network peer in the sources this record relies
on and general industry knowledge: Visa (`V`, covered in this same batch).
Other disclosed competitive categories (American Express and other
closed-loop systems, domestic networks, account-to-account/real-time
systems, digital wallets, fintech platforms, emerging alternative rails)
are referenced qualitatively above but not named as specific companies.
**These are noted as future research leads only, per `PI-0028` Section
B.16 -- no holding add, tier assignment, ranking, or further research is
authorized by naming them here.**

## Review framework

- **Cadence: 90 days** -- justified independently: Mastercard reports
  quarterly (the next release, Q2 2026, falls within this window and is
  itself this record's nearest mandatory refresh trigger), and Mastercard's
  multi-jurisdiction regulatory exposure is live and can move on a
  comparable timeframe. This matches V's cadence in this same batch for
  direct comparability, not because consistency alone justifies the
  choice.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - Q2 2026 earnings release, scheduled 2026-07-30 -- **mandatory
    near-term refresh trigger**, per the recovery audit's own instruction;
    this record must not present those results as known before they are
    released.
  - Any material development in the disclosed U.S., U.K., pan-European,
    Portuguese, or Dutch regulatory/litigation matters.
  - A material shift in the rebates-and-incentives-versus-revenue growth
    relationship relative to Q1 2026.

## Conviction

**Rating: Medium (PROPOSED).**

This is a **proposed human-judgment rating**, presented for independent
exact-head review and principal acceptance. **AI-assisted research and
drafting do not themselves constitute approval.**

**Rationale (reassessed independently in this correction, not mechanically
carried over, and independently from Visa's own rating):** Mastercard
shows the same durable network-toll-road economics as Visa, a larger
disclosed value-added-services revenue share, continued double-digit
revenue growth into Q1 2026 with value-added services outgrowing the core
network segment, and now-established financial quality (FY2025 operating
cash flow $17.648B, ~$14.5B of total FY2025 capital returned to
stockholders). Held at Medium on the basis of **Mastercard's own
evidence**, not a relative discount to Visa: Q1 2026 rebates/incentives
growing faster (23%) than payment-network revenue (12%); a disclosed
multi-jurisdiction regulatory/litigation footprint whose aggregate dollar
exposure is not established in this record; and Mastercard's own
materially sharper fiscal-2020 downturn (net revenue -9%, net income
-21%) than Visa's fiscal-2020 figures -- evidence of greater
company-specific cyclicality in at least one observed stress episode.
**This record does not infer that Mastercard's rebate/incentive trend is
worse than Visa's merely because a comparable current Visa figure was
unavailable** -- the absence of a comparable Visa figure is not evidence
of a better Visa trend, and this rating's reasoning rests on Mastercard's
own disclosed evidence, not a comparative inference. This rating excludes
valuation, entry-price, allocation, trading, and margin judgments, and
does not treat this quarter's rebate/incentive trend as necessarily
durable.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  MA, in either the original drafting pass or this correction. All
  primary evidence was inspected by GPT-5.6 Thinking -- see Source-access
  disclosure above.
- Exact geographic (Americas/APEMEA) and GDV-mix (consumer credit/debit/
  commercial) percentage splits are not established in this record.
- The dollar magnitude of Mastercard's aggregate regulatory/litigation
  exposure across its disclosed multi-jurisdiction matters is not
  established in this record.
- Multi-year capital-allocation and acquisition-integration execution
  quality are not established in this record.
- Q2 2026 results (scheduled 2026-07-30) were not yet available at this
  record's evidence cutoff and are not reflected here.

## Sources

See `MA.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit and
correction addendum
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`
and
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
