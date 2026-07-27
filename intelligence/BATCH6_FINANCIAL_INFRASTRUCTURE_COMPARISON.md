# WS-0005 Milestone 3, Batch 6 — Financial Infrastructure Comparison

**V, MA, JPM.** Authorized by
`governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
Section C (comparison requirements) and Section H (completion criteria
requiring this evidence be retained), applying
`governance/decisions/OPS-0008-research-wave-protocol-v1.md` without
modification. Created 2026-07-27, alongside the three companies' own
Company Intelligence records
(`intelligence/companies/{V,MA,JPM}.{yaml,md}`).

**Correction notice (2026-07-27):** this artifact was corrected in a
bounded pass following GPT-5.6 Thinking's independent exact-head review of
PR #171 (verdict CHANGES REQUIRED) and its accompanying primary-source
addendum, retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`.
Corrected: the Visa client-incentive arithmetic; the "one notch below
Visa" Mastercard conviction framing; unquantified JPM capital-headroom and
revenue-importance language; "JPM's equity stake in Visa" and unsupported
management-motive wording; provenance language for the retained recovery
audit; and premature approval wording. **A second, final bounded
micro-correction pass** (2026-07-27) then applied GPT-5.6 Thinking's
corrected-head delta review
(`PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`, retained at
`governance/audits/PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`): it
removed unsupported capital-return funding-source claims for both V and
MA, corrected JPM's over-generalized "balance-sheet-intermediation"
framing to distinguish deposit/lending, advisory, markets, payments,
custody, and asset-management mechanisms, and corrected "complete
first-coverage" lifecycle wording. See each company record's `review.log`
for full correction notes.

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
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a`). The
repository retained a **substantively unchanged, whitespace-normalized**
copy after trailing-whitespace normalization (six lines, header block
only — required to clear this repository's `git diff --check` CI gate),
which carries SHA-256
`ee497ac6323e25df5e0aa5cc3473e692c8566a84f0f2150a424d25d3a95bf9d8`
(17,681 bytes, 225 lines). Both hashes are disclosed together because the
files are not byte-identical; no content beyond trailing whitespace
differs. A second, bounded correction addendum, also by GPT-5.6 Thinking,
was supplied for this pass and is retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`
(as-delivered SHA-256
`5b8e89ad4f207b87b07c344d0e28e2338f2551965a929a6e540410fd2782b59c`,
15,090 bytes, 351 lines, independently verified by this session, then
whitespace-normalized in the retained copy only — no substantive content
changed — to clear this repository's `git diff --check` CI gate; retained
copy SHA-256 `4922290196e273f964003537b92a64f21cdc1cc88a5bc4fb4c87ce8265db9b6e`,
15,062 bytes, 351 lines). A third document, GPT-5.6 Thinking's corrected-head
delta review (`PR171_CORRECTED_HEAD_DELTA_REVIEW_20260727.md`, SHA-256
`13f94b8991395af7cda5b8c00d2c61a296ab8dcff3eb2ce69c7653f8f21d9897`,
14,062 bytes, 302 lines, independently verified byte-for-byte by this
session — no trailing whitespace, retained unchanged), supplied this final
micro-correction's V/MA mix figures and exact filing identities via its
Appendix A. **Every fact below is inherited
from the three companies' own Company Intelligence records**, each of
which discloses its own per-source attribution — this document adds no
new primary research of its own. Consistent with `OPS-0006` Section 4's
distinction between structural/economic overlap and measured historical
price correlation, **no price-correlation coefficient was computed for
this document** — every correlation-relevant statement below is about
shared economic drivers, not measured historical return correlation.

## 1. V versus MA — network economics, directly compared

| Metric | V | MA |
|---|---|---|
| Core revenue mechanism | Fee-based (service, data-processing, international-transaction) | Fee-based (payment-network, tied to GDV and switching) |
| Latest full fiscal year | FY2025 (ended 2025-09-30): net revenue $40.0B | FY2025 (ended 2025-12-31): payment-network net revenue $19.476B + VAS $13.315B = $32.791B |
| Value-added services (latest FY) | $10.9B | $13.315B |
| Latest quarterly revenue growth | Fiscal Q2 2026: net revenue +17% YoY | Q1 2026: net revenue +16% YoY |
| Latest quarterly cross-border volume growth | +12% (+11% ex-intra-Europe) | +13% |
| **Client incentive / rebate level (corrected)** | FY2025: $15.751B / $55.751B pre-incentive gross revenue ≈ **28.25%** (reviewer arithmetic; corrected from an earlier erroneous ~22%/$71.3B) | Q1 2026 growth rate: rebates/incentives +23% (+19% currency-neutral) — outpacing payment-network revenue growth (+12%) |
| FY2025 operating cash flow | $23.059B | $17.648B |
| FY2025 capital return | $18.2B repurchases + $4.6B dividends | $11.727B repurchases + ~$2.8B dividends (~$14.5B total) |
| Fiscal-2020 downturn (net revenue / net income) | −5% / −10% | −9% / −21% |

**Both companies run the same fundamental network-toll-road mechanism**:
fees earned on transaction/dollar volume processed over their respective
networks, netted against a real, disclosed customer-incentive cost (Visa's
"client incentives," Mastercard's "rebates and incentives"). **Neither
company issues cards, extends credit, or sets account-holder rates** — the
economic risk both carry is network-volume and network-relationship risk,
not credit risk.

**Corrected incentive comparison.** Visa's FY2025 client incentives were
approximately **28.25%** of pre-incentive gross revenue ($15.751B /
$55.751B — service $17.539B + data-processing $19.993B + international
$14.166B + other $4.053B) — corrected from an earlier version of this
comparison that incorrectly used $71.3 billion as the denominator (which
double-counted incentives) and understated the figure at ~22%. **This is a
*level*, not a *growth rate*.** Mastercard's Q1 2026 evidence establishes a
*growth rate* (rebates/incentives +23% vs. payment-network revenue +12%)
but not a comparable current level. **This record does not have a
directly comparable Visa incentive-growth-rate figure, and it does not
infer that Visa's trend is better merely because that comparable figure is
unavailable** — the two companies' incentive evidence is asymmetric
(a level for Visa, a growth rate for Mastercard), and this document
preserves that asymmetry rather than resolving it into a comparative
judgment.

**Financial quality and capital return, now directly comparable.**
**Correction note:** an earlier version of this paragraph asserted that
both companies "fund large capital-return programs from operating cash
flow without a disclosed material debt build" — a causal source-of-funds
claim the underlying evidence does not establish (it does not trace which
dollars funded which outlay, nor a year-over-year debt change). The facts
are reported here in parallel instead. FY2025: Visa's operating cash flow
was $23.059B, alongside $18.2B of repurchases, $4.6B of dividends, $24.9B
of remaining authorization, and $25.392B of total debt; Mastercard's
operating cash flow was $17.648B, alongside $11.727B of repurchases,
approximately $2.8B of dividends, and $19.000B of total debt. Both
companies' operating cash flow was large relative to their own disclosed
capital-return figures in the same period — this document states that
relative size, not a funding-source conclusion. Visa's absolute figures
are larger, consistent with its larger revenue base; this document does not compute a
per-dollar-of-revenue capital-return ratio for either company.

**Demonstrated downturn behavior — a real, company-specific difference.**
In fiscal 2020, Visa's net revenue declined ~5% and net income declined
~10%, while Mastercard's net revenue declined ~9%, cross-border volume
declined ~29%, operating margin fell from 57.2% to 52.8%, and net income
declined ~21%. **This is the clearest company-specific (not
mechanism-level) difference this record establishes between the two
companies** — Mastercard's one observed stress episode was materially
sharper than Visa's in the same period. Both companies remained profitable
throughout. This is historical evidence of one prior downturn, not a
forecast of the next one, and this document does not extrapolate it into
a permanent cyclicality ranking.

Mastercard's value-added-services revenue ($13.315B FY2025) is both larger
in absolute terms and a larger share of total net revenue than the $10.9B
this batch's evidence establishes for Visa — though the two companies'
total net-revenue bases differ enough (Visa $40.0B vs. Mastercard's
$32.791B combined) that this record does not compute or assert a directly
comparable VAS-as-percent-of-revenue figure for both.

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

Both companies also disclose **settlement/counterparty and dependency**
relationships with issuers, acquirers, processors, and merchants — neither
extends consumer credit itself (a shared structural distinction from
JPM, addressed in Section 5).

## 3. Shared interchange, merchant-fee, regulatory, litigation, and technological risk

| Risk category | V | MA |
|---|---|---|
| Interchange/merchant-fee litigation | U.S. interchange litigation, disclosed escrow structure | U.S. interchange opt-outs; U.K./pan-European merchant claims; Portuguese and Dutch proceedings |
| Antitrust/monopolization | DOJ debit-network monopolization complaint (2024-09-24), motion to dismiss denied 2025-06-23 | Not disclosed as a distinct antitrust matter in this batch's evidence base |
| Geographic dispersion of disclosed matters | Primarily U.S.-concentrated in this batch's evidence base | Multi-jurisdiction: U.S., U.K., pan-European, Portuguese, Dutch |
| Fraud / cybersecurity / network-reliability risk | Disclosed structural risk per 10-K; no specific incident found | Disclosed structural risk per 10-K; no specific incident found |
| Aggregate dollar exposure of litigation footprint | Not quantified in this record | Not quantified in this record |

**Both companies face the same category of risk — regulatory and legal
challenge to interchange/network economics — but the specific matters
disclosed in this batch's evidence base differ in kind and geography.**
Visa's most acute currently-disclosed matter (the DOJ debit-network
monopolization case) is a U.S. antitrust action with a denied motion to
dismiss; Mastercard's disclosed exposure is broader in geographic spread
but, on the evidence gathered, does not include an equivalent U.S.
antitrust monopolization complaint. **This record does not aggregate
these into a single "payment network regulatory risk" score, and does not
treat Mastercard's greater jurisdictional dispersion alone as proof of
greater expected liability** — neither company's aggregate dollar exposure
is quantified in this record's evidence base, and the matters are legally
and factually distinct.

## 4. Overlap and redundancy between owning both V and MA

**A real, disclosed, structural overlap exists.** Both companies earn fees
from the same fundamental mechanism (fee-based network tolls on payment
volume), both compete for the same issuer/acquirer/merchant
relationships, and both are exposed to the same category of interchange-
fee regulatory and litigation risk, even where the specific matters
differ.

**Distinct exposure does exist, and this correction sharpens where it
lies.** The clearest quantifiable distinctions established in this record
are: Mastercard's larger disclosed value-added-services revenue share; a
faster-growing rebates/incentives cost line for Mastercard in the latest
quarter (evidence Visa does not have a comparable figure for, not evidence
Visa is better); a broader, differently-shaped disclosed litigation/
regulatory footprint for each company; and — newly established in this
correction — **a materially different demonstrated fiscal-2020 downturn
severity** (Mastercard's decline was roughly twice Visa's on both revenue
and net-income measures). **Whether these distinctions amount to genuine
diversification or largely duplicated exposure to the same regulatory and
network-economics risk is not resolved by this document** — this record
states the evidence on both sides without collapsing it into a
conclusion, consistent with `PI-0028` Section C.4's explicit instruction.

## 5. JPM's distinct deposit, lending, credit, acquiring, investment-banking, markets, custody, and balance-sheet role

JPMorgan Chase's economic model is **not a variant of V/MA's network
model** — it is a **diversified regulated financial intermediary**
operating multiple distinct mechanisms (deposit-taking and lending with
associated credit risk; investment-banking advisory/underwriting; markets
client intermediation, trading, and balance-sheet usage; payments;
securities services/custody; and asset/wealth management) across $4.4
trillion of assets. See Section 6 for the corrected distinction between
these mechanisms — not every one of them is balance-sheet intermediation
in the same sense as deposit-taking and lending.

**Corrected, complete Q2 2026 business-line picture.** JPM's Q2 2026
managed firmwide net revenue of $58.022 billion breaks out across net
interest income ($25.6B), Investment Banking ($3.9B), Markets ($12.1B),
Payments ($5.3B), Securities Services (~$1.7B), and Asset & Wealth
Management ($6.851B). **Payments plus Securities Services were
approximately $6.96 billion, or roughly 12.0% of Q2 managed firmwide
revenue** (reviewer arithmetic, managed-basis and classification caveats
apply — see JPM.md). This corrects an earlier version of this document
that described JPM's business-line economics primarily from Payments data
and called Payments/Securities Services a "minority" of revenue without
showing the denominator; the ~12% figure is now stated explicitly, with
its limitations.

**Correction to the Visa-related disclosure.** JPM's Q2 2026 results
included a **$4.6 billion gain related to Visa shares** — a real, disclosed
connection between JPM and V within this batch. An earlier version of
this document (and of JPM's own record) described this as JPM's
"equity stake in Visa," which is not established by any source this
record relies on; the release documents a gain related to Visa shares,
not confirmed continuing ownership. This record does not treat this
connection as evidence that JPM and V are economically substitutable.

## 6. Payment rails (V/MA) versus a diversified regulated financial intermediary (JPM) — structurally different mechanisms

**This is the batch's central structural finding, and it is not merely a
"financial sector" label.** V and MA earn fees on transaction volume they
do not fund with their own balance sheets — they carry network,
regulatory, and litigation risk, not credit risk. JPM's core business is
different in kind: it is a **diversified regulated financial
intermediary** operating multiple distinct business mechanisms across a
$4.4 trillion balance sheet, subject to bank-specific regulatory capital
requirements (CET1, TLAC, G-SIB status — now precisely quantified for
CET1/SLR headroom, see Section 9) that have no analog in V/MA's disclosed
evidence.

**Correction note:** an earlier version of this section labeled every
JPM business line other than Payments and Securities Services as
"balance-sheet-intermediation-specific." That collapses genuinely
distinct mechanisms into one category. JPM's Q2 2026 revenue instead
spans (see Section 5):

- **deposit-and-lending net-interest-income economics** ($25.6B Q2 2026,
  $23.7B excluding Markets) — the mechanism actually described as
  balance-sheet intermediation (taking deposits, extending credit,
  bearing credit and interest-rate risk directly);
- **Investment Banking** ($3.9B) — principally advisory and underwriting
  activity, fee-based and closer in kind to a professional-services
  business than to balance-sheet risk-taking;
- **Markets** ($12.1B) — combines client intermediation/trading activity
  with balance-sheet usage; not purely one or the other;
- **Payments** ($5.3B) and **Securities Services** (~$1.7B) — fee/service
  businesses, the partial, real, precisely measured (~12% of managed
  firmwide revenue) point of overlap with V/MA's network economics;
- **Asset & Wealth Management** ($6.851B on $5.1 trillion AUM) —
  predominantly asset-management and servicing economics, not balance-
  sheet risk-taking.

**The central distinction from V/MA remains valid** — JPM's business
includes credit risk, interest-rate risk, and bank-specific regulatory
capital requirements that V/MA's fee-based network model does not carry
at all — but that distinction rests specifically on the deposit-and-
lending mechanism, not on every non-Payments revenue line indiscriminately.

## 7. Sensitivity to consumption, credit conditions, interest rates, regulation, fraud, cybersecurity, and economic contraction

| Factor | V / MA transmission channel | JPM transmission channel |
|---|---|---|
| Consumer spending | Directly, via payments/transaction volume | Indirectly, via deposit growth, loan demand, and card-related fee/interest income within JPM's own consumer business |
| Credit conditions | Largely indirect — V/MA do not extend credit themselves | Direct — credit costs (net charge-offs, reserve builds) are a core, disclosed JPM metric ($2.515B Q2 2026) |
| Interest rates | Indirect, mainly through consumer spending and cross-border/currency effects | Direct — Q2 2026 net interest income $25.6B ($23.7B ex-Markets), with lower rates partly offsetting higher balances per disclosed commentary |
| Regulation | Interchange-fee and antitrust-specific (V's DOJ case; MA's multi-jurisdiction matters) | Bank-capital and systemic-risk-specific (11.5% standardized CET1 requirement, 4.3% SLR requirement, stress testing, G-SIB status) — a different regulatory regime entirely |
| Fraud / cybersecurity | Disclosed structural risk for both V and MA | Not specifically evidenced in this batch's JPM research; general industry knowledge suggests banks also carry this risk, but it is not established in this record |
| Demonstrated downturn (fiscal 2020, V/MA only) | V: net revenue −5%, net income −10%. MA: net revenue −9%, net income −21% | Not evidenced for a comparable historical episode in this record — JPM's downturn transmission channel (credit losses, CET1 pressure) is structurally different from V/MA's (transaction-volume decline), so a directly comparable historical figure would not be like-for-like even if available |

**All three companies respond to the same macro environment, but through
different, largely non-overlapping channels.** A downturn that reduces
V/MA's transaction volume (a revenue-line effect, demonstrated in both
companies' fiscal-2020 figures) is a different order of severity from one
that produces credit losses and CET1 pressure at JPM (a balance-sheet and
regulatory-capital effect) — the Federal Reserve's own severely-adverse
stress-test scenario (a 2.0-percentage-point stressed CET1 decline for
JPM) exists specifically because bank balance-sheet risk requires a
different analytical and regulatory framework than a payment network's
revenue-line risk.

## 8. Portfolio uniqueness and what exposure would be lost if each were absent

- **If V were absent:** loss of direct network-toll-road exposure to
  global card-payment volume growth — partially, but not fully,
  substitutable by MA given their shared mechanism (Section 4).
- **If MA were absent:** the same category of loss as above, in reverse —
  MA's specific value-added-services emphasis, its distinct (broader,
  more multi-jurisdictional) regulatory-exposure profile, and its
  demonstrated greater fiscal-2020 cyclicality would not be replicated by
  V alone.
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
   regulatory-capital and stress-test frameworks (CET1, SLR, TLAC, Federal
   Reserve stress-test accessibility tables — now precisely quantified in
   this correction, see Section 6) that have no V/MA analog, and V/MA
   disclose no equivalent bank-regulatory-capital metric.
3. **Non-comparable core metrics.** Ordinary operating metrics (net
   revenue, operating cash flow, operating margin — now established for
   both V and MA in this correction) are meaningful for V and MA but are
   not the primary lens for evaluating a bank like JPM, whose core health
   measures (CET1 ratio, credit costs, net interest margin, stress
   resilience) have no direct V/MA analog.
4. **Asymmetric incentive/rebate evidence.** Visa's client-incentive
   evidence establishes a *level* (≈28.25% of pre-incentive gross revenue,
   corrected in this pass); Mastercard's establishes a *growth rate*
   (+23% Q1 2026). These are not directly comparable, and this record does
   not convert one into the other or infer a relative ranking from the
   asymmetry.
5. **JPM's own reviewer-arithmetic percentages remain directional only.**
   The ~12% Payments-plus-Securities-Services-of-managed-firmwide-revenue
   figure is reviewer arithmetic on a non-GAAP "managed" basis, not an
   issuer-defined segment measure, and is not treated as precise enough to
   feed a cross-company ranking.

## 10. Qualitative next-dollar (capital-priority) considerations (advisory prose only, per `PI-0028` Sections B.17/C.8)

**This section separates business quality from capital priority for all
three companies and compares them against each other and against the
next-best use of capital among this repository's other governed holdings —
it produces no score, index, or ranking, consistent with Section G's
prohibition.**

All three companies show real business-quality strength on the evidence
gathered, now more completely evidenced after this correction: V and MA
both run durable, growing, fee-based network businesses with
now-established financial quality (large operating cash flow relative to
capex, own-cash-flow-funded capital-return programs); JPM runs a
well-capitalized (precisely quantified CET1/SLR headroom), diversified,
growing banking franchise. **The three do not compete for capital priority
in a uniform way** — V (T1, 3.35%) and MA (T2, 1.65%) already carry
different governed tier weights reflecting different historical conviction
levels (existing policy, not this batch's own conclusion), while JPM's
band placement (0.75%, 1.25x cap) reflects the smallest governed
conviction of the three as existing policy. **This batch's research does
not independently re-derive whether those existing weight differentials
are evidence-supported** — per `OPS-0006` Sections 2-3, current tiers and
targets are preserved as historical comparison baselines only.

**Where redundancy exists:** V and MA duplicate each other most directly
(Sections 1, 4 above) as fee-based payment networks sharing the same core
mechanism — an investor already holding meaningful exposure to one is, to
a real degree, already exposed to the other's core economics, even where
company-specific distinctions (value-added-services mix, specific
litigation/regulatory matters, and now, demonstrated fiscal-2020
cyclicality) remain genuine. **JPM is the least redundant of the three**
with either V or MA — its balance-sheet-intermediation model, credit-cycle
exposure, and bank-regulatory-capital structure have no analog in either
payment network's disclosed business, notwithstanding its own ~12%
Payments/Securities Services overlap.

**Why the next investment dollar might, or might not, favor one of the
three over another or over an already-covered alternative:** V's evidence
base shows the most acute currently-disclosed U.S. antitrust exposure (the
DOJ debit-network case, motion to dismiss denied) alongside now-established
strong financial quality and the shallower of the two companies'
demonstrated fiscal-2020 downturns; MA's evidence base shows the broadest
multi-jurisdiction regulatory footprint, a currently-disclosed rebates/
incentives growth rate outpacing its core network-segment revenue growth,
and the deeper of the two companies' demonstrated fiscal-2020 downturns;
JPM's evidence base shows the most complete capital/liquidity picture of
the three (precisely quantified CET1/SLR headroom, a genuinely
diversified Q2 2026 revenue mix across six business lines) but requires
significant-items adjustment to interpret its most recent quarter's
headline earnings correctly, and carries a structurally different
(credit-cycle, balance-sheet) risk profile that a stress-test scenario —
not a forecast — flags as non-trivial in a severe downturn. **None of
these observations resolves into a preferred holding** — each is a real,
evidence-based distinction preserved here as uncertainty and judgment, not
collapsed into a ranking. Any actual capital-priority decision among these
three, or between any of them and another governed holding, remains a
human judgment exercised through the existing tier/target framework, not
an output of this document.

## Summary (advisory, not a ranking)

V, MA, and JPM **form the draft first-coverage candidate** for this
repository's only three uncovered financial-sector holdings — these
records count as effective, completed first-coverage only after
independent exact-head approval, principal acceptance, merge, and
post-merge verification (none of which has occurred as of this document).
They are grouped as "Financial Infrastructure" to test — honestly, per
this same comparison approach `PI-0026`'s own `power_infra` comparison
used — whether that label spans one coherent theme or two related but
distinct mechanisms. **The answer this batch's evidence supports is two
distinct mechanisms, not one**: V and MA are directly comparable, largely
overlapping fee-based payment networks with now-corrected, more complete
evidence (Sections 1-4); JPM is a structurally distinct, diversified
regulated financial intermediary whose real point of overlap with V/MA is
a precisely measured (~12%) Payments/Securities Services segment and one
disclosed financial connection (JPM's Q2 2026 gain related to Visa
shares) (Sections 5-6). Each company carries its own, company-specific
disclosed risks and evidence gaps, documented individually in `V.yaml`/
`.md`, `MA.yaml`/`.md`, and `JPM.yaml`/`.md`. **This document does not rank
the three companies, does not recommend any tier, target, cluster, cap,
holding, allocator, trade, or margin action, and does not alter any
existing Intelligence record.** Any future use of this evidence — for
Milestone 4 relationship mapping, for a policy reconsideration, or for any
other purpose — requires its own separate, later, explicit governance
authorization. `EQIX` remains deferred and uncovered by this batch, and no
Goldman Sachs or other outside-company research was performed or is
authorized by this document.
