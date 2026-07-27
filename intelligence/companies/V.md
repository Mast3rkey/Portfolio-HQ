# V — Visa Inc.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Visa Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 6, alongside `MA` and `JPM` ("Financial
Infrastructure"). `EQIX` is not part of this batch and remains deferred per
`PI-0027`.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were
blocked (HTTP 403) on SEC EDGAR (every path attempted), on Visa's own
investor-relations domain, and on a neutral, non-target control domain
(`example.com`) used specifically to test whether the block was
domain-specific or session-wide -- the control domain failed identically,
confirming a session-wide organizational network-policy denial (the local
proxy's own diagnostic guidance states plainly: "403/407 from the proxy:
the destination host is not allowed by your organization's egress policy
for this session -- do not retry or route around it"). This matches the
pattern already disclosed in this repository's Batch 1-5 records. Per
`OPS-0008` Section 2's mandatory stop-before-drafting gate, this session
paused before drafting, produced `BATCH6_SOURCE_READINESS_MANIFEST.md`
(documenting the blocked state for V, MA, and JPM), and the principal
supplied an independent primary-source evidence-recovery audit performed
by **GPT-5.6 Thinking** (2026-07-27). This session independently verified
the uploaded audit's identity before relying on it: size 17,693 bytes, 225
lines, SHA-256 `c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a`
-- matching the expected values exactly. The repository retains this audit
verbatim at
`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`.
**Every fact below was directly inspected by GPT-5.6 Thinking, not by this
Claude session** -- see `V.yaml`'s `sources[]` for per-document
attribution (source IDs V-1 through V-6 in the audit's own manifest).

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

## Client incentives -- a material competitive cost, not a rounding item

Fiscal 2025 client incentives of $15.751 billion reduced gross
revenue-before-incentives (service + data-processing + international +
other + incentives, approximately $71.3 billion) by roughly 22 percentage
points to reach $40.0 billion of net revenue. **This record treats client
incentives as a real, disclosed competitive cost of sustaining and
renewing issuer/acquirer network relationships** -- not an accounting
footnote to be ignored because it is netted against revenue. Its trend
over time is a direct, disclosed read on competitive intensity for those
relationships.

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

## Risks -- detail

**DOJ debit-network monopolization litigation** -- live, unresolved,
motion to dismiss denied; a real and current legal exposure, not
speculative, but not an adjudicated liability either.

**Disclosed U.S. interchange litigation and escrow** -- an ongoing legal
matter with a dedicated reserve structure, magnitude not established in
this record.

**Client incentives as competitive cost** -- see above; a large,
disclosed, and real reduction of gross revenue that reflects competitive
intensity for network relationships, not merely an accounting item.

**Cross-border sensitivity** -- cross-border revenue is disproportionately
exposed to travel volume, macroeconomic conditions, currency movements,
and cross-border-specific regulatory intervention, a distinct sensitivity
from Visa's domestic transaction-processing business. This record cannot
separately quantify cross-border revenue as a share of the total from the
evidence inspected.

**Evidence-completeness gap** -- this record's balance-sheet, leverage,
cash-flow, and capital-allocation (buybacks/dividends) detail is **not
established** from the sources GPT-5.6 Thinking's audit directly
inspected. The audit's recovered baseline covers business model, revenue
composition, current-quarter volume growth, and litigation status, but not
a balance-sheet or cash-flow figure for Visa. This is a disclosed evidence
gap, not an assumption of low leverage or ample liquidity -- do not infer
balance-sheet strength from the absence of a stated weakness.

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
growth continuing into the most recent reported quarter, and a structural
distinction from bank-model credit/deposit risk (Visa does not extend
credit or take deposits).

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
  cross-border volume +12%), but this record does not establish how V's
  revenue behaved during a prior broad economic contraction -- no
  historical drawdown or recession-period data was inspected.
- **Balance-sheet/leverage:** not established by any source this record
  relies on -- a genuine, disclosed evidence gap.
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
  processed-transaction growth relative to the fiscal Q2 2026 trend.
- Evidence that client incentives are rising at a rate structurally
  outpacing gross revenue growth (margin compression via the incentive
  line, not merely a level).
- A material competitive displacement by an alternative payment rail
  (real-time payments, account-to-account transfer schemes) not
  independently evidenced in this record but named as a standing industry
  risk in the comparison artifact.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as a direct payment-network peer in the sources this record relies
on and general industry knowledge: Mastercard (`MA`, covered in this same
batch). Other alternative-payment-rail participants (e.g. real-time
payment schemes, account-to-account networks) are referenced qualitatively
in the comparison artifact but are not named as specific companies in this
record's evidence base. **These are noted as future research leads only,
per `PI-0028` Section B.16 -- no holding add, tier assignment, ranking, or
further research is authorized by naming them here.**

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

**Rating: High.**

**Rationale:** Visa shows a durable, network-scale payments-technology
business with diversified, growing revenue and continued double-digit
growth in its most recently reported quarter. Conviction is held at High
rather than Very High because of two concrete, current tensions: an active
DOJ monopolization complaint concerning debit-network services with a
denied motion to dismiss (unresolved, not yet a liability finding, but
real and live), and a disclosed evidence gap in this record's
balance-sheet, leverage, and capital-allocation detail. This rating
excludes valuation, entry-price, allocation, trading, and margin
judgments, and does not treat the pending DOJ litigation's outcome as
predictable from the evidence in this record.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  V. All primary evidence was inspected by GPT-5.6 Thinking during the
  2026-07-27 evidence-recovery audit -- see Source-access disclosure
  above.
- Visa's balance-sheet, leverage, cash-flow, and capital-allocation detail
  (buybacks, dividends, total debt) is not established in this record.
- The dollar magnitude of Visa's potential interchange-litigation and
  DOJ-litigation exposure is not established in this record.
- Cross-border revenue's specific share of total revenue is not separately
  quantified in this record.
- Fiscal Q3 2026 results (scheduled 2026-07-28) were not yet available at
  this record's evidence cutoff and are not reflected here.

## Sources

See `V.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
