# MA — Mastercard Incorporated

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Mastercard Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 6, alongside `V` and `JPM`.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were
blocked (HTTP 403) on SEC EDGAR, Mastercard's investor-relations domain,
and a neutral, non-target control domain (`example.com`) -- confirming a
session-wide network-policy denial rather than a domain-specific failure,
matching V's and JPM's own disclosed blocks in this same batch. Per
`OPS-0008` Section 2's mandatory stop-before-drafting gate, this session
paused before drafting, and the principal supplied an independent
primary-source evidence-recovery audit performed by **GPT-5.6 Thinking**
(2026-07-27). This session independently verified the uploaded audit's
identity before relying on it: size 17,693 bytes, 225 lines, SHA-256
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a` --
matching the expected values exactly. The repository retains this audit
verbatim at
`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`.
**Every fact below was directly inspected by GPT-5.6 Thinking, not by this
Claude session** -- see `MA.yaml`'s `sources[]` for per-document
attribution (source IDs MA-1 through MA-4 in the audit's own manifest).

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

Note: this record's underlying 10-K source establishes the fiscal-year
period (ended 2025-12-31) and SEC accession number but this record does
not independently establish the exact 10-K filing date beyond the period
end; treat the 10-K's `date` field in `MA.yaml` as the period-end date, not
a confirmed filing date.

## Rebates and incentives -- a growing competitive cost

**Q1 2026 payment-network rebates and incentives rose 23%** (**19%** on a
currency-neutral basis) -- **faster than payment-network revenue growth
(12%)** in the same quarter. This is Mastercard's equivalent of Visa's
client incentives, and this record treats it the same way: a real,
disclosed competitive cost of sustaining and renewing customer
relationships, and one whose growth rate outpacing revenue growth in the
most recent quarter is a specific, current margin-pressure signal, not a
generic risk.

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
concentrated in the United States. This record does not aggregate these
distinct matters into a single unsupported liability estimate -- each
remains a separate, jurisdiction-specific disclosed matter of uncertain
magnitude.

## Risks -- detail

**Rebates/incentives outpacing network-segment revenue growth** -- a
current, quarter-specific margin-pressure signal.

**Multi-jurisdiction regulatory/litigation exposure** -- broader in
disclosed geographic spread than Visa's, though this record does not
establish which company's aggregate exposure is larger in dollar terms
(neither company's aggregate litigation exposure is quantified in this
record).

**Shared network-economics risk with Visa** -- Mastercard's core
payment-network revenue depends on the same fee-based, GDV-and-switching
mechanism as Visa's service/data-processing revenue. Any regulatory,
litigation, or alternative-payment-rail development that pressures network
economics broadly is likely to affect both companies together -- a
duplicated-exposure consideration this record does not attempt to resolve
independently of the comparison artifact.

**Evidence-completeness gap** -- this record's balance-sheet, leverage,
cash-flow, and capital-allocation detail is not established from the
sources inspected, matching the same disclosed gap for Visa.

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
for Visa, and value-added services growing faster than the core network
segment.

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
  transactions all grew through Q1 2026, but this record does not
  establish how MA's revenue behaved during a prior broad economic
  contraction -- no historical drawdown or recession-period data was
  inspected.
- **Balance-sheet/leverage:** not established by any source this record
  relies on -- a genuine, disclosed evidence gap, matching Visa's.
- **Rebate/incentive-driven margin pressure:** the Q1 2026
  rebates-outpacing-revenue signal is a disclosed, current margin
  consideration distinct from an external shock.
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
  switched-transaction growth relative to the Q1 2026 trend.
- Rebates and incentives continuing to grow structurally faster than
  payment-network revenue over multiple consecutive quarters (confirming,
  rather than a one-quarter signal, a durable margin-compression trend).
- A material competitive displacement by an alternative payment rail, the
  same industry-level risk named in V's own thesis-break conditions.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as a direct payment-network peer in the sources this record relies
on and general industry knowledge: Visa (`V`, covered in this same batch).
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

**Rating: Medium.**

**Rationale:** Mastercard shows the same durable network-toll-road
economics as Visa, a larger disclosed value-added-services revenue share,
and continued double-digit revenue growth into Q1 2026 with value-added
services outgrowing the core network segment. Conviction is held at
Medium, one notch below Visa's High in this same batch, for two concrete,
current, evidence-based reasons rather than a generic "second name in the
pair" discount: rebates and incentives grew faster than payment-network
revenue in the most recently reported quarter (a specific, disclosed
margin-pressure signal), and Mastercard's disclosed regulatory/litigation
footprint is broader and more jurisdictionally dispersed than this record
establishes for Visa's more concentrated U.S. exposure. This rating
excludes valuation, entry-price, allocation, trading, and margin
judgments, and does not treat this quarter's rebate/incentive trend as
necessarily durable.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  MA. All primary evidence was inspected by GPT-5.6 Thinking during the
  2026-07-27 evidence-recovery audit -- see Source-access disclosure
  above.
- Mastercard's balance-sheet, leverage, cash-flow, and capital-allocation
  detail (buybacks, dividends, total debt) is not established in this
  record.
- The dollar magnitude of Mastercard's aggregate regulatory/litigation
  exposure across its disclosed multi-jurisdiction matters is not
  established in this record.
- The exact Form 10-K filing date (beyond period end 2025-12-31 and its
  SEC accession number) was not established by this record.
- Q2 2026 results (scheduled 2026-07-30) were not yet available at this
  record's evidence cutoff and are not reflected here.

## Sources

See `MA.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
