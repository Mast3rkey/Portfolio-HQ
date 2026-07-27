# JPM — JPMorgan Chase & Co.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior JPMorgan Chase Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 6, alongside `V` and `MA`.

**Correction notice (2026-07-27):** this record was corrected in a bounded
pass following GPT-5.6 Thinking's independent exact-head review of PR #171
(verdict CHANGES REQUIRED) and its accompanying primary-source addendum,
retained at
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`.
The correction quantifies capital headroom precisely, adds complete Q2
2026 business-line evidence, corrects Visa-share and management-motive
overclaims, corrects provenance language, and reassesses conviction
independently. See `JPM.yaml`'s `review.log` for the full correction note.

**Analytical note, per `PI-0028` Section B.20:** this record analyzes JPM
using bank-appropriate measures (CET1, liquidity, credit costs, reserves,
deposits, net-interest/fee mix, stress resilience) rather than the
ordinary operating-company metrics (margins, free-cash-flow yield,
net-debt ratios) used for V and MA. JPM is **not** mechanically compared
against V/MA on those operating-company terms anywhere in this record —
see `BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md` for the explicit
discussion of why that comparison is not meaningful.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were
blocked (HTTP 403) on SEC EDGAR, JPMorgan Chase's investor-relations
domain, and a neutral, non-target control domain (`example.com`) --
confirming a session-wide network-policy denial, matching V's and MA's own
disclosed blocks in this same batch. Per `OPS-0008` Section 2's mandatory
stop-before-drafting gate, this session paused before drafting.

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
this Claude session** -- see `JPM.yaml`'s `sources[]` for per-document
attribution.

## Business summary

JPMorgan Chase reported **$4.4 trillion of assets** and **$362.4 billion
of stockholders' equity** at 2025 year-end, operating across three primary
business segments — **Consumer & Community Banking**, **Commercial &
Investment Bank**, and **Asset & Wealth Management** — with **Corporate**
activities reported separately. This is a fundamentally different economic
model from V/MA: deposit-taking, lending, credit risk, trading, investment
banking, custody, and asset/wealth management, rather than a fee-based
transaction-processing network.

## Regulatory-capital headroom (corrected in this pass — precise, not qualitative)

At **2026-03-31**: standardized CET1 ratio **14.3%**, advanced CET1 ratio
**14.1%**, supplementary leverage ratio (SLR) **5.6%**; CET1 capital
**$291 billion**; approximately **$1.5 trillion** of liquidity sources.

The applicable benchmarks, per JPMorgan's 2026 capital-results filing: a
**standardized CET1 requirement including buffers of 11.5%**, and an
**applicable SLR requirement of 4.3%**. **Precise headroom** (reviewer
arithmetic from these disclosed figures):

- standardized CET1 headroom: **2.8 percentage points** (14.3% − 11.5%);
- advanced CET1 headroom versus the same 11.5% benchmark: **2.6
  percentage points** (14.1% − 11.5%);
- SLR headroom: **1.3 percentage points** (5.6% − 4.3%).

**Correction note:** an earlier version of this record described this
headroom only as "comfortably above" regulatory minimums "with a wide
margin," without stating the applicable requirement. That qualitative
language is replaced here with the precise benchmarks and arithmetic
above. **Regulatory headroom is a capacity measure, not a guarantee
against loss.**

## Q2 2026 results — complete business-line evidence (corrected in this pass)

The Q2 2026 release (furnished 2026-07-14) reports **managed firmwide net
revenue of $58.022 billion**, broken out as:

| Line | Q2 2026 |
|---|---|
| Net interest income | $25.6 billion ($23.7 billion excluding Markets) |
| Investment Banking revenue | $3.9 billion (fees $3.3 billion) |
| Markets revenue | $12.1 billion (Fixed Income $6.1B, Equities $6.0B) |
| Payments revenue | $5.3 billion |
| Securities Services revenue | approximately $1.7 billion |
| Asset & Wealth Management revenue | $6.851 billion (AUM $5.1 trillion) |

**Correction note:** an earlier version of this record described JPM's Q2
2026 business-line economics primarily from Payments and Securities
Services data alone. This section adds the full disclosed line-up so the
record does not imply JPM is a Payments-centric business — it is not;
Payments and Securities Services together are a minority of managed
firmwide revenue (see below).

**Reviewer arithmetic (not an issuer-defined segment measure):** Payments
plus Securities Services were approximately **$6.96 billion**, or roughly
**12.0%** of Q2 managed firmwide net revenue. This percentage is a
**directional scale comparison only** — Payments and Securities Services
sit in different disclosed groupings within the Commercial & Investment
Bank, "managed" revenue is itself a non-GAAP measure, and this arithmetic
is not a standalone segment-margin or risk measure.

**Net interest income and rate sensitivity:** Q2 2026 net interest income
was $25.6 billion ($23.7 billion excluding Markets), with lower rates
partly offsetting higher balances per the release's own commentary. This
record does not independently model JPM's forward net-interest-margin
sensitivity to further rate changes.

**Credit costs:** Q2 2026 provision for credit losses was **$2.515
billion**, including approximately **$2.4 billion** of net charge-offs and
a **$149 million** net reserve build.

## Significant items — Q2 2026 results require adjustment to interpret

**This record does not use headline Q2 2026 net income or ROE without
separating the disclosed significant items.** Q2 2026 net income was
**$21.2 billion**, which included a **$4.6 billion gain related to Visa
shares** and **$1.0 billion** of gains on other equity investments.
JPMorgan's own release separately reported **net income excluding
significant items of $16.9 billion**, which this record uses for
assessing ordinary quarterly operating profitability.

**Correction note:** an earlier version of this record described this as
"JPM's equity stake in Visa" and asserted management presented the
adjusted measure "precisely because" the headline figure would overstate
ordinary profitability. Both are corrected here: the release documents a
**gain related to Visa shares**, not a continuing equity stake after the
transaction — no source this record relies on establishes continuing
ownership. And no source establishes management's specific motive for
presenting the adjusted measure, so this record asserts no motive; it
simply notes that the adjusted figure exists and is what this record
relies on.

## Capital return and management (added/corrected in this pass)

Q2 2026 capital return: **common dividend of $4.0 billion** and
**common-stock net repurchases of $6.2 billion** — disclosed facts, not an
assessment of whether this pace is sustainable through a credit-cycle
downturn, and reported in the same quarter the firm also grew deposits
(+7% YoY) and loans.

**Jamie Dimon** is identified as **Chairman and Chief Executive Officer**.
This record discusses tenure and capital-management continuity only with
the appropriate official source, and does not treat "fortress balance
sheet" or similar issuer characterizations as an independent conclusion —
those are issuer framing, not this record's own finding.

## Regulatory and stress-test evidence

The Federal Reserve's **2026 Dodd-Frank Act stress-test** accessibility
tables report a **2.0-percentage-point decline from starting to minimum
CET1** for JPMorgan Chase under the **severely adverse scenario**. **This
is a supervisory stress-test scenario result, not a forecast of an actual
future recession outcome, and it does not by itself establish a safe
leverage level or any margin-deployment conclusion** — treated strictly as
regulatory-scenario evidence in this record.

JPMorgan Chase is designated a **Global Systemically Important Bank
(G-SIB)** per the Financial Stability Board's 2025 G-SIB list, subjecting
it to higher capital buffers, total loss-absorbing capacity (TLAC)
requirements, resolvability requirements, and heightened supervision.
**This record describes G-SIB status as a regulatory constraint and
resilience framework, not a guarantee against loss.**

## Merchant-acquiring exposure (explicit limitation, added in this correction)

Merchant-acquiring exposure is **not separately quantified** in this
record's evidence base. The Payments line (Q2 2026: $5.3 billion) is
disclosed within the Commercial & Investment Bank without a further
merchant-acquiring-specific breakout in the sources inspected. **This
record does not treat Payments as a pure merchant-acquiring business** and
discloses this as an explicit limitation rather than assuming a specific
acquiring-revenue figure.

## Risks — detail

**Significant-items-adjusted earnings interpretation** — headline Q2 2026
net income requires adjustment to assess ordinary operating profitability;
see above.

**Credit costs** — $2.515 billion in Q2 2026, including net charge-offs and
a modest reserve build. This record does not forecast whether credit
costs will rise in a deteriorating credit cycle; it records the current,
disclosed figure only.

**Stress-test sensitivity** — a 2.0-percentage-point stressed CET1 decline
under the Federal Reserve's severely adverse scenario is a real, disclosed
data point this record does not discount to zero, while explicitly not
treating it as a forecast.

**G-SIB regulatory burden** — higher capital/TLAC/resolvability
requirements are both a resilience framework and an ongoing regulatory
cost/complexity factor.

**Net-interest-income and rate sensitivity** — see above; disclosed
current-quarter figure and directional commentary only, no independent
forward model.

**Investment Banking and Markets cyclicality** — both disclosed lines are
historically more cyclical/transaction-dependent than deposit-and-lending
net interest income; no multi-quarter or multi-year trend is established
in this record.

**Merchant-acquiring exposure unquantified** — see above.

**Structural incomparability with V/MA** — JPM's business combines
deposit-and-lending economics with payments, custody, markets, investment
banking, and asset management. This diversification may stabilize
earnings but also creates regulatory, trading, and credit-cycle complexity
with no direct analog in V/MA's fee-based network model. **Ordinary
operating-company metrics are not meaningfully comparable between JPM and
V/MA** — this record does not attempt that comparison; see the comparison
artifact for the explicit limitations discussion required by `PI-0028`
Section C.9.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, JPM currently sits in the **band** tier (0.75% target
weight, 1.25x cap — i.e. up to roughly 0.9375% of book before a mechanical,
RSI-gated opportunistic trim applies). JPM is **not** a member of any
`targets.yaml` correlated-cluster cap. This placement is recorded here as
**existing governed policy, preserved as a historical comparison baseline
only, per `OPS-0006` Sections 2-3's zero-based-research discipline** — it
is not treated as evidence supporting any conclusion in this record, and
this record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality**, per the evidence above, is strong on bank-appropriate
terms: well-capitalized with precisely quantified regulatory headroom
(2.8/2.6/1.3 percentage points across standardized CET1, advanced CET1,
and SLR), highly liquid (~$1.5 trillion of liquidity sources), a growing
deposit and loan franchise, and a genuinely diversified revenue mix
spanning net interest income, Investment Banking, Markets, Payments,
Securities Services, and Asset & Wealth Management.

**Capital priority is a separate question.** JPM carries band's standard
0.75% target — the smallest of this batch's three per-name targets,
reflecting existing governed policy, not a research conclusion this record
independently re-derives. **What would be lost if JPM were absent from the
book:** direct exposure to a diversified, regulated, deposit-and-lending
banking franchise — an economic mechanism entirely distinct from V/MA's
network-fee model, and not duplicated by any other currently governed
holding this record cross-references. **This record does not resolve
whether the next investment dollar favors JPM over V, MA, or another
governed alternative** — JPM's business model is different enough from
V/MA's that a direct next-dollar comparison across all three is explicitly
limited by differing disclosure regimes and economic mechanisms (see the
comparison artifact); this record preserves that uncertainty rather than
resolving it, consistent with `PI-0028` Section B.17's requirement.

## Margin-relevant evidence (factual/advisory only — no leverage recommendation)

- **Regulatory capital position:** precisely quantified headroom (above)
  — 2.8 points standardized CET1, 2.6 points advanced CET1, 1.3 points
  SLR, all versus their applicable requirements — and $590 billion of
  total loss-absorbing capacity disclosed for Q2 2026.
- **Liquidity:** approximately $1.5 trillion of liquidity sources /
  cash and marketable securities disclosed.
- **Credit-cycle exposure:** $2.515 billion of Q2 2026 credit costs
  (including net charge-offs and a reserve build) is the clearest current,
  disclosed indicator of credit-cycle exposure; this record does not
  forecast its trajectory.
- **Revenue-mix cyclicality:** Investment Banking and Markets revenue
  (together $16.0 billion of Q2 2026 managed firmwide revenue) are
  historically more cyclical than net interest income or Payments/
  Securities Services fee revenue; no multi-quarter trend is established
  here.
- **Stress resilience:** the Federal Reserve's 2026 severely-adverse
  scenario shows a 2.0-percentage-point stressed CET1 decline for JPM — a
  supervisory scenario result, explicitly not a safe-leverage or
  deployment-timing conclusion.
- **Correlated-loss relevance:** JPM's Payments/Securities Services
  segment revenue (≈12% of Q2 managed firmwide revenue, reviewer
  arithmetic) provides a partial, disclosed overlap with V/MA's network
  economics (see the comparison artifact), but JPM's dominant risk drivers
  (credit cycle, net interest margin, Investment Banking/Markets
  cyclicality) are structurally distinct from V/MA's network-fee/
  regulatory risk.
- **This record makes no safe-leverage calculation, no deployment-timing
  conclusion, and no margin recommendation of any kind for JPM or any
  other holding**, per `PI-0028` Section B.14.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A material, sustained deterioration in credit quality (rising net
  charge-offs or reserve builds well beyond the Q2 2026 level) signaling a
  credit-cycle downturn.
- A material decline in CET1 ratios toward the 11.5% standardized
  requirement (i.e. materially eroding the current 2.8-point headroom), or
  toward the 4.3% SLR requirement, whether from losses, regulatory
  changes, or balance-sheet growth outpacing capital generation.
- A materially worse-than-disclosed Federal Reserve stress-test result in
  a future cycle, or a regulatory capital-requirement increase specific to
  JPM's G-SIB status.
- Evidence that Q2 2026's significant items (the Visa-share gain and other
  investment gains) mask a deteriorating trend in net income excluding
  significant items over subsequent quarters.
- A material, sustained decline in Investment Banking or Markets revenue
  not evidenced in this record's Q2 2026 baseline.
- A material adverse development in net-interest-income trajectory from
  further rate changes.

## Disconfirming evidence actively searched (added in this correction)

This record's underlying evidence was reviewed specifically for evidence
that would weaken the diversified-bank thesis, recorded whether or not
each item was found:

- **Deposit outflows or rising deposit costs** — not found; Q2 2026
  average deposits grew 7% year over year.
- **Adverse interest-rate sensitivity / NII compression** — found,
  partially: the release notes lower rates partly offsetting higher
  balances in net interest income; this record does not independently
  model the forward trajectory.
- **Reserve inadequacy or accelerating charge-offs** — not established
  either way; Q2 2026 shows a modest net reserve build ($149 million), not
  a drawdown, but this record does not assess reserve adequacy against
  future losses.
- **Stressed capital depletion beyond expectations** — the Federal
  Reserve's 2026 severely-adverse scenario shows a 2.0-point stressed CET1
  decline, already reflected as a risk above; no evidence of depletion
  beyond that disclosed supervisory scenario was found.
- **Material trading, operational, cyber, conduct, or litigation loss** —
  none disclosed in the sources inspected.
- **Weak returns from business complexity or sustained cost growth** — not
  established either way from the sources inspected.
- **Investment Banking/Markets cyclicality** — found and already reflected
  as a risk above; no multi-quarter trend established.
- **Capital distributions reducing resilience** — the Q2 2026 dividend
  ($4.0B) and repurchases ($6.2B) are disclosed alongside a 2.8-point CET1
  headroom; this record does not find evidence the distributions
  materially reduced resilience in this quarter, but does not assess
  multi-year cumulative effect.
- **Regulatory changes raising capital/liquidity/resolution costs** — none
  disclosed beyond the existing G-SIB/TLAC framework already reflected
  above.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

No specific diversified-bank or financial-conglomerate peer is named as a
direct competitor in the sources this record relies on. General industry
knowledge suggests other large diversified U.S. banks occupy an adjacent
competitive space, but none is named specifically here. **This is noted as
a future research lead only, per `PI-0028` Section B.16 — no holding add,
tier assignment, ranking, or further research is authorized by naming this
possibility here.**

## Review framework

- **Cadence: 90 days** — justified independently: JPMorgan reports
  quarterly (a Q2 2026 Form 10-Q filing, if it adds material information
  beyond the already-inspected earnings release and supplement, falls
  within this window), and JPM's credit-cost and stress-test evidence can
  move meaningfully within a single quarter. This matches V's and MA's
  cadence in this same batch for consistency, not because consistency
  alone justifies the choice.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - JPM's Q2 2026 Form 10-Q filing, if it adds material information beyond
    the inspected earnings release/supplement.
  - Any material change in credit costs, net charge-offs, or reserve
    builds relative to the Q2 2026 baseline.
  - Any material Federal Reserve, FSB, or other banking-regulator
    development affecting JPM's capital, stress-test, or G-SIB status
    (internal checkpoint: 2026-10-25, matching this record's next_due
    date).
  - A material change in Investment Banking, Markets, Payments, or
    Securities Services segment growth trends relative to Q2 2026.

## Conviction

**Rating: Medium (PROPOSED).**

This is a **proposed human-judgment rating**, presented for independent
exact-head review and principal acceptance. **AI-assisted research and
drafting do not themselves constitute approval.**

**Rationale (reassessed independently in this correction, not mechanically
carried over):** JPMorgan shows a large, diversified, well-capitalized
banking franchise with precisely quantified regulatory-capital headroom
(2.8 points standardized CET1, 2.6 points advanced CET1, 1.3 points SLR),
substantial liquidity, continued deposit and loan growth, and a genuinely
diversified Q2 2026 revenue mix now evidenced across net interest income,
Investment Banking, Markets, Payments, Securities Services, and Asset &
Wealth Management. Held at Medium — not directly comparable to V's or
MA's ratings, since JPM is analyzed on bank-appropriate terms distinct
from V/MA's network-fee terms. Conviction is not higher because Q2 2026
headline results required significant-items adjustment to interpret
correctly (the Visa-share gain and other investment gains), credit costs
are a disclosed and monitored line item, Investment Banking and Markets
revenue are disclosed but historically cyclical lines without an
established multi-quarter trend here, and the Federal Reserve's 2026
severely-adverse stress scenario shows a real, if modest, stressed CET1
decline that this record does not discount to zero even while treating it
strictly as a supervisory scenario, not a forecast. This rating excludes
valuation, entry-price, allocation, trading, and margin/safe-leverage
judgments.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  JPM, in either the original drafting pass or this correction. All
  primary evidence was inspected by GPT-5.6 Thinking — see Source-access
  disclosure above.
- JPM's Q2 2026 Form 10-Q had not yet been included in the evidence base
  at this record's evidence cutoff; footnote-level JPM claims remain tied
  to the Q1 2026 10-Q or the Q2 earnings release/supplement.
- Merchant-acquiring-specific revenue within the Payments line is not
  separately quantified in this record.
- Multi-quarter or multi-year trend data for Investment Banking, Markets,
  and net-interest-income sensitivity is not established in this record.
- Whether JPM's Q2 2026 capital-return pace is sustainable through a
  credit-cycle downturn is not established in this record.

## Sources

See `JPM.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit and
correction addendum
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`
and
`governance/audits/PR171_BOUNDED_CORRECTION_PRIMARY_SOURCE_ADDENDUM_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
