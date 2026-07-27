# WS-0005 Milestone 3, Batch 6 — Financial Infrastructure Comparison

**V, MA, JPM.** Authorized by
`governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
Section C (comparison requirements) and Section H (completion criteria
requiring this evidence be retained), applying
`governance/decisions/OPS-0008-research-wave-protocol-v1.md` without
modification. Created 2026-07-27, alongside the three companies' own
Company Intelligence records
(`intelligence/companies/{V,MA,JPM}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema
(it introduces no new schema and is not scanned by
`intelligence_validator.py` or any other validator), and not an
authoritative record any allocator or policy decision may read. It sits at
`intelligence/` root, matching `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`
through `BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md`'s own
placement and scope. **It does not rank the three companies, does not
declare a required preferred holding, does not recommend a tier/target/
cluster change, a buy/trim/exit, a margin action, or a mechanical
capital-priority ranking, and does not create a composite score of any
kind** — per `PI-0028` Section C's explicit instruction and the
Constitution's standing prohibition on predictive research or opportunity
maps.

**Source-access disclosure (applies to this whole document).** This Claude
Code session's own direct `WebFetch` attempts on 2026-07-27 were blocked
(HTTP 403) on SEC EDGAR and on every V/MA/JPM investor-relations domain
tested, and on a neutral, non-target control domain (`example.com`) used
specifically to confirm the block was session-wide rather than
domain-specific. Per `OPS-0008` Section 2's mandatory stop-before-drafting
gate, drafting paused and the principal supplied an independent
evidence-recovery audit performed by **GPT-5.6 Thinking** (2026-07-27),
independently identity-verified by this session as-delivered (17,693
bytes, 225 lines, SHA-256
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a`).
Following the same precedent already established for Batch 4's and Batch
5's own retained audits, this session then normalized trailing Markdown
hard-line-break whitespace (six lines in the header block only) in the
**retained repository copy only** — no substantive content changed — to
clear this repository's `git diff --check` CI gate; the retained copy
therefore carries SHA-256
`ee497ac6323e25df5e0aa5cc3473e692c8566a84f0f2150a424d25d3a95bf9d8`
(17,681 bytes, 225 lines, unchanged), intentionally different from the
as-delivered hash because of the whitespace normalization only. Retained
at
`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`.
**Every fact below is inherited from the three companies' own Company
Intelligence records**, each of which discloses its own per-source
attribution — this document adds no new primary research of its own.
Consistent with `OPS-0006` Section 4's distinction between structural/
economic overlap and measured historical price correlation, **no
price-correlation coefficient was computed for this document** — every
correlation-relevant statement below is about shared economic drivers, not
measured historical return correlation.

## 1. V versus MA — network economics, directly compared

| Metric | V | MA |
|---|---|---|
| Core revenue mechanism | Fee-based (service, data-processing, international-transaction) | Fee-based (payment-network, tied to GDV and switching) |
| Latest full fiscal year | FY2025 (ended 2025-09-30): net revenue $40.0B | FY2025 (ended 2025-12-31): payment-network net revenue $19.476B + VAS $13.315B = $32.791B |
| Value-added services (latest FY) | $10.9B | $13.315B |
| Latest quarterly revenue growth | Fiscal Q2 2026: net revenue +17% YoY | Q1 2026: net revenue +16% YoY |
| Latest quarterly cross-border volume growth | +12% (+11% ex-intra-Europe) | +13% |
| Latest quarterly customer-incentive/rebate growth | Not separately reported as a growth rate in this batch's evidence base | Rebates/incentives +23% (+19% currency-neutral) — **outpacing** payment-network revenue growth (+12%) |

**Both companies run the same fundamental network-toll-road mechanism**:
fees earned on transaction/dollar volume processed over their respective
networks, netted against a real, disclosed customer-incentive cost (Visa's
"client incentives," Mastercard's "rebates and incentives"). **Neither
company issues cards, extends credit, or sets account-holder rates** — the
economic risk both carry is network-volume and network-relationship risk,
not credit risk.

**The one directly quantifiable divergence in this batch's evidence base**:
Mastercard's Q1 2026 rebates/incentives grew faster (23%) than its
payment-network revenue (12%), a specific, disclosed margin-pressure
signal. This record's evidence base does not establish the equivalent
year-over-year growth rate for Visa's client incentives in the same
period, so **this is not evidence that Visa's incentive structure is
better-behaved — only that Mastercard's is the one this batch's evidence
base can specifically quantify as currently outpacing revenue.**

Mastercard's value-added-services revenue ($13.315B FY2025) is both larger
in absolute terms and a larger share of total net revenue than the $10.9B
this batch's evidence establishes for Visa — though the two companies'
total net-revenue bases differ enough (Visa $40.0B vs. Mastercard's
$32.791B combined) that this record does not compute or assert a directly
comparable VAS-as-percent-of-revenue figure for both without flagging that
the underlying revenue-recognition and category definitions may not be
perfectly aligned between the two 10-Ks.

## 2. Network effects, acceptance scale, and issuer/acquirer/merchant relationships

Both V and MA compete for the same three-sided relationships: **card
issuers** (banks that issue Visa- or Mastercard-branded cards), **acquirers**
(banks/processors that sign up merchants), and **merchants** (who accept
the cards). Neither company's own disclosed evidence in this batch
provides a directly comparable acceptance-footprint or issuer-count metric
for the other — this record does not assert a market-share ordering
between the two from the evidence gathered. Client incentives (V) and
rebates/incentives (MA) are each company's disclosed mechanism for
competing for and retaining these same issuer/acquirer relationships — the
same competitive dynamic, expressed through the same economic lever, for
both.

## 3. Shared interchange, merchant-fee, regulatory, litigation, and technological risk

| Risk category | V | MA |
|---|---|---|
| Interchange/merchant-fee litigation | U.S. interchange litigation, disclosed escrow structure | U.S. interchange opt-outs; U.K./pan-European merchant claims; Portuguese and Dutch proceedings |
| Antitrust/monopolization | DOJ debit-network monopolization complaint (2024-09-24), motion to dismiss denied 2025-06-23 | Not disclosed as a distinct antitrust matter in this batch's evidence base |
| Geographic dispersion of disclosed matters | Primarily U.S.-concentrated in this batch's evidence base | Multi-jurisdiction: U.S., U.K., pan-European, Portuguese, Dutch |
| Fraud / cybersecurity / alternative-rail risk | Named qualitatively as a standing industry risk in V.md; not separately quantified | Named qualitatively as a standing industry risk in MA.md; not separately quantified |

**Both companies face the same category of risk — regulatory and legal
challenge to interchange/network economics — but the specific matters
disclosed in this batch's evidence base differ in kind and geography.**
Visa's most acute currently-disclosed matter (the DOJ debit-network
monopolization case) is a U.S. antitrust action with a denied motion to
dismiss; Mastercard's disclosed exposure is broader in geographic spread
but, on the evidence gathered, does not include an equivalent
U.S. antitrust monopolization complaint. **This record does not aggregate
these into a single "payment network regulatory risk" score** — the
matters are legally and factually distinct, and their eventual financial
consequences, if any, are not established by any source in this batch's
evidence base.

## 4. Overlap and redundancy between owning both V and MA

**A real, disclosed, structural overlap exists.** Both companies earn fees
from the same fundamental mechanism (fee-based network tolls on payment
volume), both compete for the same issuer/acquirer/merchant
relationships, and both are exposed to the same category of interchange-
fee regulatory and litigation risk, even where the specific matters
differ. An investor holding meaningful exposure to one is, to a real
degree, already exposed to the core economics the other also captures.

**Distinct exposure does exist, but this batch's evidence base does not
establish that it is large.** The clearest quantifiable distinctions are:
Mastercard's larger disclosed value-added-services revenue share, a
faster-growing rebates/incentives cost line for Mastercard in the latest
quarter, and a broader, differently-shaped disclosed litigation/regulatory
footprint for each company. **Whether these distinctions amount to
genuine diversification or largely duplicated exposure to the same
regulatory and network-economics risk is not resolved by this document**
— this record states the evidence on both sides without collapsing it
into a conclusion, consistent with `PI-0028` Section C.4's explicit
instruction.

## 5. JPM's distinct deposit, lending, credit, acquiring, investment-banking, markets, custody, and balance-sheet role

JPMorgan Chase's economic model is **not a variant of V/MA's network
model** — it is regulated balance-sheet intermediation: deposit-taking,
lending with associated credit risk, trading and markets activity,
investment banking, custody, and asset/wealth management, across $4.4
trillion of assets. JPM's revenue depends on **net interest income** (the
spread between what it pays depositors and earns on loans/investments),
**credit performance** (net charge-offs and reserve builds, $2.5 billion
of Q2 2026 credit costs), and **fee income** across a wide range of
businesses (investment banking, markets, custody, asset/wealth
management, and — the point of partial overlap with V/MA — Payments and
Securities Services, $5.3 billion and $1.7 billion of Q2 2026 revenue
respectively).

**The one direct, disclosed financial link between JPM and V in this
batch's evidence base**: JPM's Q2 2026 results included a $4.6 billion
gain related to Visa shares. This is a real, disclosed connection, but
this record does not treat it as evidence that JPM and V are economically
substitutable, nor that JPM's equity stake materially changes either
company's own investment thesis — it is recorded as a factual point of
overlap, not a synthesis.

## 6. Payment rails (V/MA) versus balance-sheet intermediation (JPM) — two structurally different mechanisms

**This is the batch's central structural finding, and it is not merely a
"financial sector" label.** V and MA earn fees on transaction volume they
do not fund with their own balance sheets — they carry network,
regulatory, and litigation risk, not credit risk. JPM's core business is
the opposite: it takes deposits, extends credit, and bears the resulting
credit and interest-rate risk directly on a $4.4 trillion balance sheet,
subject to bank-specific regulatory capital requirements (CET1, TLAC,
G-SIB status) that have no analog in V/MA's disclosed evidence. **JPM's
Payments and Securities Services segments provide a partial, real point of
overlap with V/MA's network economics, but they are a minority of JPM's
overall business and do not make JPM a third payment network** — the vast
majority of JPM's revenue, risk, and regulatory capital structure is
balance-sheet-intermediation-specific.

## 7. Sensitivity to consumption, credit conditions, interest rates, regulation, fraud, cybersecurity, and economic contraction

| Factor | V / MA transmission channel | JPM transmission channel |
|---|---|---|
| Consumer spending | Directly, via payments/transaction volume | Indirectly, via deposit growth, loan demand, and card-related fee/interest income within JPM's own consumer business |
| Credit conditions | Largely indirect — V/MA do not extend credit themselves | Direct — credit costs (net charge-offs, reserve builds) are a core, disclosed JPM metric ($2.5B Q2 2026) |
| Interest rates | Indirect, mainly through consumer spending and cross-border/currency effects | Direct — net interest income and margin are core to JPM's earnings, not established as a specific figure in this batch's evidence base |
| Regulation | Interchange-fee and antitrust-specific (V's DOJ case; MA's multi-jurisdiction matters) | Bank-capital and systemic-risk-specific (CET1 requirements, stress testing, G-SIB status) — a different regulatory regime entirely |
| Fraud / cybersecurity | Named as a standing industry risk for both V and MA | Not specifically evidenced in this batch's JPM research; general industry knowledge suggests banks also carry this risk, but it is not established in this record |
| Economic contraction | Transaction-volume decline (a revenue-line effect) | Credit losses, potential CET1 pressure per the Fed's severely-adverse stress scenario (a balance-sheet and capital effect) — a structurally more severe transmission channel in a downturn |

**All three companies respond to the same macro environment, but through
different, largely non-overlapping channels.** A downturn that reduces V/MA's transaction volume (a revenue-line effect) is a different order of
severity from one that produces credit losses and CET1 pressure at JPM (a
balance-sheet and regulatory-capital effect) — the Federal Reserve's own
severely-adverse stress-test scenario exists specifically because bank
balance-sheet risk requires a different analytical and regulatory
framework than a payment network's revenue-line risk.

## 8. Portfolio uniqueness and what exposure would be lost if each were absent

- **If V were absent:** loss of direct network-toll-road exposure to
  global card-payment volume growth — partially, but not fully,
  substitutable by MA given their shared mechanism (Section 4).
- **If MA were absent:** the same category of loss as above, in reverse —
  MA's specific value-added-services emphasis and its distinct (broader,
  more multi-jurisdictional) regulatory-exposure profile would not be
  replicated by V alone.
- **If JPM were absent:** loss of the book's only direct exposure to
  regulated deposit-and-lending banking economics, credit-cycle risk, and
  bank-specific capital/liquidity dynamics — **not substitutable by either
  V or MA**, whose businesses do not carry credit risk or bank regulatory
  capital requirements at all.

## 9. Explicit limitations preventing a mechanical capital-priority ordering

**This record does not, and cannot from its own evidence base, produce a
mechanical capital-priority ordering across all three companies**, for
reasons distinct from a simple unwillingness to rank:

1. **Differing reporting periods.** V's fiscal year ends 2025-09-30; MA's
   and JPM's calendar fiscal years end 2025-12-31 — direct year-over-year
   comparisons across all three require period-adjustment this record does
   not perform.
2. **Differing disclosure regimes.** V and MA disclose under ordinary
   SEC operating-company requirements; JPM discloses under bank-specific
   regulatory-capital and stress-test frameworks (CET1, TLAC, Federal
   Reserve stress-test accessibility tables) that have no V/MA analog, and
   V/MA disclose no equivalent bank-regulatory-capital metric.
3. **Non-comparable core metrics.** Ordinary operating metrics (net
   revenue, operating margin) are meaningful for V and MA but are not the
   primary lens for evaluating a bank like JPM, whose core health measures
   (CET1 ratio, credit costs, net interest margin, stress resilience) have
   no direct V/MA analog.
4. **Evidence gaps.** This batch's evidence base does not establish V's or
   MA's balance-sheet, leverage, or capital-allocation detail (see each
   company's own record), which would be needed for even a partial
   V/MA-versus-JPM capital-structure comparison.

## 10. Qualitative next-dollar (capital-priority) considerations (advisory prose only, per `PI-0028` Sections B.17/C.8)

**This section separates business quality from capital priority for all
three companies and compares them against each other and against the
next-best use of capital among this repository's other governed holdings —
it produces no score, index, or ranking, consistent with Section G's
prohibition.**

All three companies show real business-quality strength on the evidence
gathered: V and MA both run durable, growing, fee-based network
businesses; JPM runs a well-capitalized, diversified, growing banking
franchise. **The three do not compete for capital priority in a uniform
way** — V (T1, 3.35%) and MA (T2, 1.65%) already carry different governed
tier weights reflecting different historical conviction levels (existing
policy, not this batch's own conclusion), while JPM's band placement
(0.75%, 1.25x cap) reflects the smallest governed conviction of the three
as existing policy. **This batch's research does not independently
re-derive whether those existing weight differentials are
evidence-supported** — per `OPS-0006` Sections 2-3, current tiers and
targets are preserved as historical comparison baselines only, not
treated as evidence for this batch's own conclusions.

**Where redundancy exists:** V and MA duplicate each other most directly
(Sections 1, 4 above) as fee-based payment networks sharing the same core
mechanism — an investor already holding meaningful exposure to one is, to
a real degree, already exposed to the other's core economics, even where
company-specific distinctions (value-added-services mix, specific
litigation/regulatory matters) remain genuine. **JPM is the least
redundant of the three** with either V or MA — its balance-sheet-
intermediation model, credit-cycle exposure, and bank-regulatory-capital
structure have no analog in either payment network's disclosed business.

**Why the next investment dollar might, or might not, favor one of the
three over another or over an already-covered alternative:** V's evidence
base shows the most acute currently-disclosed U.S. antitrust exposure (the
DOJ debit-network case, motion to dismiss denied); MA's evidence base
shows the broadest multi-jurisdiction regulatory footprint and a
currently-disclosed rebates/incentives growth rate outpacing its core
network-segment revenue growth; JPM's evidence base shows the most
complete capital/liquidity picture of the three (CET1 ratios, liquidity
sources, stress-test results) but requires significant-items adjustment to
interpret its most recent quarter's headline earnings correctly, and
carries a structurally different (credit-cycle, balance-sheet) risk
profile that a stress-test scenario — not a forecast — flags as
non-trivial in a severe downturn. **None of these observations resolves
into a preferred holding** — each is a real, evidence-based distinction
preserved here as uncertainty and judgment, not collapsed into a ranking.
Any actual capital-priority decision among these three, or between any of
them and another governed holding, remains a human judgment exercised
through the existing tier/target framework, not an output of this
document.

## Summary (advisory, not a ranking)

V, MA, and JPM complete first-coverage Company Intelligence research for
this repository's only three uncovered financial-sector holdings,
grouped as "Financial Infrastructure" to test — honestly, per this same
comparison approach `PI-0026`'s own `power_infra` comparison used — whether
that label spans one coherent theme or two related but distinct
mechanisms. **The answer this batch's evidence supports is two distinct
mechanisms, not one**: V and MA are directly comparable, largely
overlapping fee-based payment networks (Sections 1-4); JPM is a
structurally distinct, regulated balance-sheet-intermediation business
whose only real point of overlap with V/MA is a minority Payments/
Securities Services segment and one disclosed financial link (JPM's Q2
2026 Visa-share gain) (Sections 5-6). Each company carries its own,
company-specific disclosed risks and evidence gaps, documented
individually in `V.yaml`/`.md`, `MA.yaml`/`.md`, and `JPM.yaml`/`.md`.
**This document does not rank the three companies, does not recommend any
tier, target, cluster, cap, holding, allocator, trade, or margin action,
and does not alter any existing Intelligence record.** Any future use of
this evidence — for Milestone 4 relationship mapping, for a policy
reconsideration, or for any other purpose — requires its own separate,
later, explicit governance authorization. `EQIX` remains deferred and
uncovered by this batch, and no Goldman Sachs or other outside-company
research was performed or is authorized by this document.
