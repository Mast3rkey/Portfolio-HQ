# V — Visa Inc.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Visa Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 6, alongside `MA` and `JPM` ("Financial
Infrastructure"). `EQIX` is not part of this batch and remains deferred per
`PI-0027`.

**Correction notice (2026-07-27):** this record was corrected in a bounded
pass following GPT-5.6 Thinking's independent exact-head review of PR #171
(`PR171_EXACT_HEAD_IMPLEMENTATION_REVIEW_20260727.md`, verdict CHANGES
REQUIRED) and its accompanying primary-source addendum
(`PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`, retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`).
The correction fixes a material client-incentive arithmetic error, adds
several previously-missing `PI-0028`-mandatory research fields, corrects
premature approval and provenance language, and reassesses conviction
independently. **A second, final bounded micro-correction pass**
(2026-07-27) then applied GPT-5.6 Thinking's corrected-head delta review
(`PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`, retained at
`governance/audits/PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`): it
completed the payment-volume-mix figures, corrected the fiscal-2020
source citation to an exact filing identity, and removed an unsupported
capital-return funding-source claim. See `V.yaml`'s `review.log` for both
full correction notes.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were
blocked (HTTP 403) on SEC EDGAR (every path attempted), on Visa's own
investor-relations domain, and on a neutral, non-target control domain
(`example.com`) used specifically to test whether the block was
domain-specific or session-wide -- the control domain failed identically,
confirming a session-wide organizational network-policy denial. This
matches the pattern already disclosed in this repository's Batch 1-5
records. Per `OPS-0008` Section 2's mandatory stop-before-drafting gate,
this session paused before drafting and produced
`BATCH6_SOURCE_READINESS_MANIFEST.md`.

The principal supplied an independent primary-source evidence-recovery
audit performed by **GPT-5.6 Thinking** (2026-07-27). The as-delivered
audit file had SHA-256
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a`
(17,693 bytes, 225 lines) -- independently verified by this session
against the uploaded file before use. **The repository retained a
substantively unchanged copy after trailing-whitespace normalization**
(six lines, header block only -- required to clear this repository's
`git diff --check` CI gate), which carries SHA-256
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
this Claude session** -- see `V.yaml`'s `sources[]` for per-document
attribution.

## Business summary

Visa describes itself as a global payments-technology company that
facilitates secure, reliable, and efficient global commerce and money
movement, providing transaction-processing services -- primarily
authorization, clearing, and settlement -- among consumers, issuing and
acquiring financial institutions, and sellers, through its electronic
payments network, **VisaNet**. Visa states plainly that it is **not a
financial institution**: it does not issue cards, does not extend credit,
and does not set account-holder interest rates or fees. This is a
structural distinction from a bank's credit and deposit-taking business,
relevant directly to this batch's comparison with JPM (see
`BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md`).

**Fiscal 2025** (year ended 2025-09-30) revenue by category: service
revenue **$17.539 billion**, data-processing revenue **$19.993 billion**,
international-transaction revenue **$14.166 billion**, other revenue
**$4.053 billion**, less **$15.751 billion** of client incentives
(a contra-revenue deduction), for **net revenue of $40.0 billion**.
Value-added-services revenue within this total was **$10.9 billion**.

Service revenue is tied principally to payments volume; data-processing
revenue is tied principally to processed transactions; international-
transaction revenue is earned on cross-border processing and currency
conversion -- three related but economically distinct volume drivers.

**Fiscal Q2 2026** (quarter ended 2026-03-31, furnished 2026-04-28): net
revenue **$11.2 billion, up 17% year over year**; constant-dollar payments
volume grew **9%**; total cross-border volume grew **12%** (**11%**
excluding intra-Europe); processed transactions grew **9% to 66.1
billion**. This is recent evidence of continued growth, not solely a
historical franchise argument.

## Client incentives -- corrected arithmetic

**Corrected in this pass.** Fiscal-2025 issuer-reported components:
service revenue $17.539B, data-processing revenue $19.993B,
international-transaction revenue $14.166B, and other revenue $4.053B sum
to **gross revenue before incentives of $55.751 billion**. Client
incentives of **$15.751 billion** are therefore **$15.751B / $55.751B ≈
28.25%** of that pre-incentive gross amount -- not the previously stated
~22% (which incorrectly used $71.3 billion, a figure that double-counted
incentives in the denominator, as the base). **This 28.25% figure is
reviewer arithmetic derived from issuer-reported components, not an
issuer-defined metric.**

The underlying economic conclusion is unchanged and, if anything,
strengthened by the correction: client incentives are a large, disclosed,
and real competitive cost of sustaining and renewing issuer/acquirer
network relationships -- not an accounting footnote to be ignored because
it is netted against revenue. At roughly 28% of pre-incentive gross
revenue, this is a materially larger share than the original (incorrect)
~22% figure suggested. Its trend over time is a direct, disclosed read on
competitive intensity for those relationships.

## Financial quality and capital allocation (added in this correction)

For fiscal 2025, per Visa's Form 10-K: **operating income $23.994
billion**; **net income $20.058 billion**; **operating cash flow $23.059
billion**; purchases of property, equipment, and technology of only
**$1.482 billion**. Reviewer arithmetic (operating cash flow less those
purchases -- not an issuer-defined free-cash-flow measure): **approximately
$21.577 billion** available before capital return and other uses.

**Debt:** total debt $25.392 billion; carrying value of debt $25.171
billion (FY2025). This record does not establish a complete
liquidity/current-ratio picture or any post-FY2025 debt issuance beyond
this total-debt figure.

**Capital return:** FY2025 common-stock repurchases of **$18.2 billion**
and dividends declared/paid of **$4.6 billion**, with **$24.9 billion** of
repurchase authorization remaining at fiscal year-end. **Correction note:**
an earlier version of this section asserted the capital-return program was
"funded from the company's own operating cash flow, not from a disclosed
external-debt build" — that causal source-of-funds claim is removed here,
since the evidence inspected does not trace which specific dollars funded
the repurchases/dividends, does not establish that no opening cash was
used, and does not establish a year-over-year debt change. The facts are
reported in parallel instead: FY2025 operating cash flow was $23.059
billion; disclosed capex was $1.482 billion; total debt was $25.392
billion (carrying value $25.171 billion) at fiscal year-end. Operating
cash flow was large relative to the disclosed capex and capital-return
figures in the same period — this record states that relative size, not a
funding-source conclusion.

**Management:** Ryan McInerney signed the FY2025 Form 10-K as Chief
Executive Officer. **This record does not infer management quality from
title or tenure alone.** Multi-year capital-allocation execution quality
-- specifically, whether repurchases were made at prices that created
value -- remains a judgment this record does not resolve from a single
fiscal year's disclosure.

## Payment-volume mix and dependencies (added in this correction; figures completed in the final micro-correction)

Visa's FY2025 Form 10-K discloses **nominal payments volume** (twelve
months ended 2025-06-30) broken out by category: **consumer credit $5.604
trillion**; **consumer debit, including prepaid/Interlink as defined in
the filing, $6.551 trillion**; **commercial $1.739 trillion**; **total
nominal payments volume $13.894 trillion**. Reviewer arithmetic from these
issuer-reported components (not an issuer-defined mix metric, and subject
to filing rounding): consumer credit **≈40.33%**, consumer debit
**≈47.15%**, commercial **≈12.52%** of total nominal payments volume.
**Correction note:** an earlier version of this section stated only that
the disclosure existed without reporting the figures; this was a genuinely
available primary-source fact, not an unresolvable limitation, and has
been completed here per GPT-5.6 Thinking's independent inspection of the
FY2025 10-K's volume-and-transaction-statistics table (SEC accession
0001403161-25-000089).

**Dependencies:** Visa depends on financial-institution **issuers**,
**acquirers**, **processors**, **merchants**, and **routing**
relationships to generate volume across VisaNet. Client incentives,
rebates, and support payments (see above) are the primary disclosed
mechanism Visa uses to maintain and expand those relationships -- meaning
Visa's own revenue growth is partly a function of a real, ongoing
competitive-payment relationship with the same issuers and acquirers whose
business it needs to retain.

## Competitors, substitutes, and alternative rails (added in this correction)

Per the FY2025 10-K's own disclosed competitive-landscape discussion:
other card networks, domestic (in-country) payment networks, closed-loop
payment systems, digital wallets, real-time account-to-account payment
systems, bank-led payment alternatives, and emerging blockchain- or
stablecoin-based payment rails. **These are disclosed competitive
categories, not evidence that any specific substitution is currently
occurring at scale against Visa** -- this record does not quantify
market-share erosion to any of these categories from the evidence
inspected.

## Fraud, cybersecurity, and network-reliability risk (added in this correction)

Fraud, cybersecurity, network availability/reliability, tokenization,
authentication, and data-protection risk are disclosed, material operating
and thesis risks for a network business of VisaNet's scale -- not merely
generic technology-sector boilerplate. A material failure in any of these
areas could damage issuer/acquirer/merchant trust and network volume. This
record does not identify a specific past incident affecting Visa and
treats this as a standing structural risk category per the FY2025 10-K's
own risk-factor disclosure, not as evidence of an ongoing or imminent
failure.

## Litigation and regulatory evidence

- **U.S. v. Visa, Inc. [2024]** (U.S. Department of Justice): a
  monopolization complaint concerning debit-network services, filed
  **2024-09-24**. Visa's motion to dismiss was **denied by court order on
  2025-06-23**. **This is an active, unresolved allegation with a denied
  motion to dismiss -- a procedural status, not an adjudicated finding of
  liability.** This record does not state or imply that Visa has been
  found liable of anything in this matter.
- Visa's FY2025 10-K discloses **U.S. interchange litigation**, including a
  **litigation-escrow structure**, DOJ debit-network litigation (the same
  matter above), related private class actions, and other merchant and
  ATM-related matters. The existence of a litigation escrow indicates Visa
  itself treats potential interchange-related liability as material enough
  to reserve against, though **this record does not establish a specific
  dollar exposure estimate** from the sources inspected.

## Demonstrated downturn behavior (added in this correction)

Visa's fiscal-2020 Form 10-K (fiscal year ended 2020-09-30, SEC accession
`0001403161-20-000070`, filed 2020-11-19) provides an
observed stress case, used here as **historical evidence, not a forecast
of the next downturn**: fiscal-2020 net revenue declined **approximately
5%** year over year; international-transaction revenue declined
materially as cross-border travel contracted during that period; net
income declined **approximately 10%**; **the company remained profitable**
throughout. This demonstrates Visa's revenue-line (not balance-sheet or
credit) sensitivity to a broad travel/consumption contraction -- a
different transmission channel than JPM's credit-cycle exposure (see the
comparison artifact).

## Risks -- detail

**DOJ debit-network monopolization litigation** -- live, unresolved,
motion to dismiss denied; a real and current legal exposure, not
speculative, but not an adjudicated liability either.

**Disclosed U.S. interchange litigation and escrow** -- an ongoing legal
matter with a dedicated reserve structure, magnitude not established in
this record.

**Client incentives as competitive cost (corrected)** -- see above; a
large, disclosed reduction of gross revenue (≈28.25% of the pre-incentive
base, corrected from an erroneous ~22%) that reflects real competitive
intensity for network relationships.

**Cross-border sensitivity** -- cross-border revenue is disproportionately
exposed to travel volume, macroeconomic conditions, currency movements,
and cross-border-specific regulatory intervention; the fiscal-2020
downturn (above) is this record's best available evidence of that
sensitivity in practice.

**Payment-volume mix, issuer/acquirer dependency, and substitution risk**
-- see above; a disclosed but only partially quantified risk category.

**Fraud/cybersecurity/network-reliability risk** -- see above; a standing
structural risk, not evidence of an active incident.

**Narrowed but not eliminated evidence-completeness gap** -- this record
now establishes FY2025 operating cash flow, capex, total debt, and capital
return (above), but a complete liquidity/current-ratio picture, any
post-FY2025 debt issuance, exact payment-volume-mix percentages, and
multi-year capital-allocation execution quality remain unestablished from
the sources inspected. This is a disclosed evidence gap, not an assumption
of strength or weakness.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, V currently sits in the **T1** tier (3.35% target
weight per name). V is **not** a member of any `targets.yaml`
correlated-cluster cap (`semis`, `power_infra`, or `oil`). This placement
is recorded here as **existing governed policy, preserved as a historical
comparison baseline only, per `OPS-0006` Sections 2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion in
this record, and this record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality**, per the evidence above, is strong: a diversified,
growing, network-scale payments-technology business with disclosed volume
growth continuing into the most recent reported quarter, now-demonstrated
financial quality (large operating cash flow relative to capex, an
own-cash-flow-funded capital-return program), and a structural distinction
from bank-model credit/deposit risk.

**Capital priority is a separate question.** V carries T1's standard 3.35%
per-name target, tied with the other T1 names. **What would be lost if V
were absent from the book:** direct exposure to global card-network
transaction-processing economics -- a distinct economic mechanism from
every other currently governed holding, including MA (see the comparison
artifact for the V-versus-MA overlap discussion) and JPM (a
balance-sheet-intermediation model, not a network-toll-road model). **The
retained evidence does not resolve whether the next investment dollar
favors V over MA** -- both are payment networks sharing largely the same
core economic mechanism (see `BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md`
Section 1); this record preserves that uncertainty rather than resolving
it, consistent with `PI-0028` Section B.17's requirement to separate
business quality from capital priority and to preserve judgment and
uncertainty rather than produce a ranking.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Revenue/volume cyclicality:** payments and cross-border volume are
  disclosed to have grown through fiscal Q2 2026 (payments volume +9%,
  cross-border volume +12%); the fiscal-2020 downturn (above) is the best
  available historical evidence of Visa's behavior in a broad contraction
  -- a revenue-line effect, not a balance-sheet or credit event.
- **Balance-sheet/leverage:** total debt $25.392B / carrying value
  $25.171B (FY2025) is now established; a complete liquidity/current-ratio
  picture and any post-FY2025 issuance are not established by any source
  this record relies on.
- **Litigation-driven liability risk:** the DOJ debit-network case and the
  disclosed interchange-litigation escrow represent a potential, currently
  unquantified financial liability distinct from ordinary business-cycle
  risk.
- **Correlated-loss relevance:** V shares its core network-toll-road
  economic mechanism with MA, covered in the same batch (see the
  comparison artifact) -- a shared-mechanism risk (interchange regulation,
  network-security/fraud exposure, alternative-payment-rail competition)
  distinct from JPM's balance-sheet-intermediation risk.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- An adverse final ruling or a structural/behavioral remedy in the DOJ
  debit-network monopolization case that materially constrains Visa's
  network economics or pricing.
- A material adverse development in the disclosed U.S. interchange
  litigation exceeding the escrow's apparent adequacy (not independently
  quantified in this record).
- Sustained deceleration in payments volume, cross-border volume, or
  processed-transaction growth relative to the fiscal Q2 2026 trend, or a
  fiscal-2020-scale contraction recurring.
- Evidence that client incentives are rising at a rate structurally
  outpacing gross revenue growth (margin compression via the incentive
  line, not merely a level) -- this record does not currently have a
  comparable Visa incentive-growth-rate figure to test this against.
- A material competitive displacement by an alternative payment rail
  (real-time payments, account-to-account transfer schemes, or a
  blockchain/stablecoin-based rail) not independently evidenced in this
  record but named as a disclosed competitive category above.
- A material cybersecurity, fraud, or network-reliability failure.

## Disconfirming evidence actively searched (added in this correction)

This record's underlying evidence (Visa's FY2025 10-K and Q2 2026
materials, plus the fiscal-2020 10-K) was reviewed specifically for
evidence that would weaken the "durable, high-quality network" thesis
above. The following categories were searched and are recorded here
whether or not each was found:

- **Incentives rising faster than volume/revenue** -- the FY2025 level
  (≈28.25% of pre-incentive gross revenue) is disclosed and material, but
  this record does not have a directly comparable prior-year or
  multi-year growth-rate figure to establish a trend, so this item remains
  an open question, not a confirmed finding either way.
- **Loss of issuer/acquirer routing relationships** -- no specific loss
  disclosed in the sources inspected.
- **Alternative-rail substitution at scale** -- disclosed as a competitive
  category (above); no quantified market-share loss found in the sources
  inspected.
- **Adverse regulatory/court outcomes on debit routing or interchange** --
  found: the DOJ case (unresolved) and the disclosed interchange
  litigation/escrow (magnitude unquantified) are the concrete instances of
  this risk category already reflected in the Risks section above.
- **Sustained cross-border weakness** -- the fiscal-2020 downturn is the
  one historical instance found; no current sustained weakness is
  disclosed in the fiscal Q2 2026 evidence (cross-border volume +12%).
- **Major fraud, cyber, or reliability failure** -- none disclosed in the
  sources inspected.
- **Value-destructive capital returns** -- not established either way;
  this record's evidence does not include repurchase-price detail needed
  to assess whether the $18.2B FY2025 buyback program was value-accretive.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as a direct payment-network peer in the sources this record relies
on and general industry knowledge: Mastercard (`MA`, covered in this same
batch). Other named disclosed competitive categories (other card
networks, domestic networks, closed-loop systems, digital wallets,
real-time account-to-account systems, bank-led alternatives, and emerging
blockchain/stablecoin-based rails) are referenced qualitatively above but
are not named as specific companies in this record's evidence base.
**These are noted as future research leads only, per `PI-0028` Section
B.16 -- no holding add, tier assignment, ranking, or further research is
authorized by naming them here.**

## Review framework

- **Cadence: 90 days** -- justified independently: Visa reports quarterly
  (the next release, fiscal Q3 2026, falls within this window and is
  itself this record's nearest mandatory refresh trigger), and the DOJ
  debit-network litigation is a live matter that can move on a comparable
  timeframe. This happens to match the cadence used for other T1 records
  (e.g. `MSFT`, `GEV`), but that consistency is incidental to, not the
  basis for, this record's own cadence choice.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - Fiscal Q3 2026 earnings release, scheduled 2026-07-28 -- **mandatory
    near-term refresh trigger**, per the recovery audit's own instruction;
    this record must not present those results as known before they are
    released.
  - Any material ruling, remedy proposal, or settlement in U.S. v. Visa,
    Inc. [2024].
  - Any material development in the disclosed U.S. interchange litigation
    or its escrow structure.
  - A material shift in payments-volume or cross-border-volume growth
    trend relative to fiscal Q2 2026.

## Conviction

**Rating: High (PROPOSED).**

This is a **proposed human-judgment rating**, presented for independent
exact-head review and principal acceptance. **AI-assisted research and
drafting do not themselves constitute approval** -- that requires the
review and acceptance steps `PI-0028` and `OPS-0007` describe.

**Rationale (reassessed independently in this correction, not mechanically
carried over):** Visa shows a durable, network-scale payments-technology
business with diversified, growing revenue, continued double-digit growth
in its most recently reported quarter, and now-established financial
quality (large operating cash flow relative to disclosed capex, alongside
a disclosed capital-return program and total-debt figure, reported in
parallel without a source-of-funds conclusion). Held at High rather than
Very High because of concrete, current tensions: an active DOJ
monopolization complaint concerning debit-network services with a denied
motion to dismiss; the corrected, material client-incentive cost (≈28.25%
of pre-incentive gross revenue); and a still-incomplete liquidity and
multi-year capital-allocation picture. This rating excludes valuation,
entry-price, allocation, trading, and margin judgments, and does not treat
the pending DOJ litigation's outcome as predictable from the evidence in
this record.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  V, in either the original drafting pass or this correction. All primary
  evidence was inspected by GPT-5.6 Thinking -- see Source-access
  disclosure above.
- A complete liquidity/current-ratio picture beyond total debt, and any
  post-FY2025 debt issuance, are not established in this record.
- Which specific source (operating cash flow, existing cash, or other)
  funded Visa's FY2025 capital-return program is not established in this
  record — a source-of-funds conclusion was removed in this correction as
  unsupported by the evidence inspected.
- The dollar magnitude of Visa's potential interchange-litigation and
  DOJ-litigation exposure is not established in this record.
- Whether the FY2025 $18.2B buyback program was value-accretive (price
  discipline) is not established in this record.
- Fiscal Q3 2026 results (scheduled 2026-07-28) were not yet available at
  this record's evidence cutoff and are not reflected here.

## Sources

See `V.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit,
correction addendum, and (for the payment-volume-mix figures and the
exact fiscal-2020 filing identity added in the final micro-correction)
Appendix A of the corrected-head delta review
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`,
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`,
and
`governance/audits/PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
