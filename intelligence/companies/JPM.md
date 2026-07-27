# JPM — JPMorgan Chase & Co.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior JPMorgan Chase Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 6, alongside `V` and `MA`.

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
stop-before-drafting gate, this session paused before drafting, and the
principal supplied an independent primary-source evidence-recovery audit
performed by **GPT-5.6 Thinking** (2026-07-27). This session independently
verified the as-delivered uploaded audit's identity before relying on it:
size 17,693 bytes, 225 lines, SHA-256
`c248f74f07708c9c61a57169e7a7b234c0d6238b484ffa92c52dcb1f295bb73a` --
matching the expected values exactly. Following the same precedent already
established for Batch 4's and Batch 5's own retained audits, this session
then normalized trailing Markdown hard-line-break whitespace (six lines in
the header block only) in the **retained repository copy only** -- no
substantive content changed -- to clear this repository's `git diff
--check` CI gate. The repository's retained copy therefore carries SHA-256
`ee497ac6323e25df5e0aa5cc3473e692c8566a84f0f2150a424d25d3a95bf9d8`
(17,681 bytes, 225 lines, unchanged) -- intentionally different from the
as-delivered hash because of the whitespace normalization, not a
discrepancy. Retained at
`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`.
**Every fact below was directly inspected by GPT-5.6 Thinking, not by this
Claude session** -- see `JPM.yaml`'s `sources[]` for per-document
attribution (source IDs JPM-1 through JPM-6 in the audit's own manifest).

## Business summary

JPMorgan Chase reported **$4.4 trillion of assets** and **$362.4 billion
of stockholders' equity** at 2025 year-end, operating across three primary
business segments — **Consumer & Community Banking**, **Commercial &
Investment Bank**, and **Asset & Wealth Management** — with **Corporate**
activities reported separately. This is a fundamentally different economic
model from V/MA: deposit-taking, lending, credit risk, trading, investment
banking, custody, and asset/wealth management, rather than a fee-based
transaction-processing network.

**Capital and liquidity (at 2026-03-31):** $291 billion of CET1 capital;
standardized and advanced CET1 ratios of **14.3%** and **14.1%**; a
**5.6%** supplementary leverage ratio; approximately **$1.5 trillion** of
liquidity sources.

**Q2 2026 results (furnished 2026-07-14):** JPMorgan reported **$21.2
billion** of net income, which **included a $4.6 billion gain related to
Visa shares and $1.0 billion of gains on other equity investments** — the
release separately reported **net income excluding significant items of
$16.9 billion**. Q2 2026 firmwide metrics: standardized and advanced CET1
ratios of **14.1%** and **14.2%**; **$590 billion** of total loss-absorbing
capacity; **$1.5 trillion** of cash and marketable securities; average
loans of **$1.5 trillion**; average deposits **up 7% year over year**.
Q2 2026 credit costs were **$2.5 billion**, including **$2.4 billion** of
net charge-offs and a **$149 million** net reserve build.

**Segment detail relevant to this batch:** in the Commercial & Investment
Bank, Q2 2026 **Payments** revenue was **$5.3 billion, up 12%**, and
**Securities Services** revenue was **$1.7 billion, up 17%**. Combined
**Banking & Payments** revenue was **$11.2 billion**. This gives JPM a
partial, though structurally distinct, point of overlap with V/MA's
network economics — see the comparison artifact.

## Significant items — Q2 2026 results require adjustment to interpret

**This record does not use headline Q2 2026 net income or ROE without
separating the disclosed significant items.** The $4.6 billion Visa-share
gain and $1.0 billion of other equity-investment gains are one-time or
episodic in nature relative to JPM's ordinary operating profitability;
JPMorgan's own release separately disclosed net income excluding
significant items ($16.9 billion) precisely because the headline figure
would otherwise overstate ordinary quarterly earnings power. Notably, the
Visa-share gain is a direct, disclosed financial linkage between JPM and V
within this same batch — a fact worth flagging structurally, though this
record does not treat it as evidence that JPM and V are economically
substitutable or that JPM's equity stake in Visa materially changes either
company's own thesis.

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

## Risks — detail

**Significant-items-adjusted earnings interpretation** — headline Q2 2026
net income requires adjustment to assess ordinary operating profitability;
see above.

**Credit costs** — $2.5 billion in Q2 2026, including net charge-offs and
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
terms: well-capitalized (CET1 ratios comfortably above regulatory
minimums), highly liquid (~$1.5 trillion of liquidity sources), a growing
deposit and loan franchise, and diversified fee/net-interest revenue
spanning consumer banking, investment banking, markets, and asset/wealth
management.

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

- **Regulatory capital position:** CET1 ratios (14.1%-14.3% standardized/
  advanced as of 2026-03-31 and Q2 2026) sit comfortably above regulatory
  minimums, and $590 billion of total loss-absorbing capacity is disclosed
  for Q2 2026.
- **Liquidity:** approximately $1.5 trillion of liquidity sources /
  cash and marketable securities disclosed.
- **Credit-cycle exposure:** $2.5 billion of Q2 2026 credit costs
  (including net charge-offs and a reserve build) is the clearest current,
  disclosed indicator of credit-cycle exposure; this record does not
  forecast its trajectory.
- **Stress resilience:** the Federal Reserve's 2026 severely-adverse
  scenario shows a 2.0-percentage-point stressed CET1 decline for JPM — a
  supervisory scenario result, explicitly not a safe-leverage or
  deployment-timing conclusion.
- **Correlated-loss relevance:** JPM's Payments/Securities Services
  segment revenue provides a partial, disclosed overlap with V/MA's
  network economics (see the comparison artifact), but JPM's dominant risk
  drivers (credit cycle, net interest margin, trading/markets exposure)
  are structurally distinct from V/MA's network-fee/regulatory risk.
- **This record makes no safe-leverage calculation, no deployment-timing
  conclusion, and no margin recommendation of any kind for JPM or any
  other holding**, per `PI-0028` Section B.14 and the recovery audit's own
  explicit instruction to treat the Federal Reserve stress result strictly
  as a supervisory scenario.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- A material, sustained deterioration in credit quality (rising net
  charge-offs or reserve builds well beyond the Q2 2026 level) signaling a
  credit-cycle downturn.
- A material decline in CET1 ratios toward regulatory minimums, whether
  from losses, regulatory changes, or balance-sheet growth outpacing
  capital generation.
- A materially worse-than-disclosed Federal Reserve stress-test result in
  a future cycle, or a regulatory capital-requirement increase specific to
  JPM's G-SIB status.
- Evidence that Q2 2026's significant items (Visa-share and other
  investment gains) mask a deteriorating trend in net income excluding
  significant items over subsequent quarters.
- A material adverse development in JPM's trading, markets, or investment-
  banking revenue lines not evidenced in this record's Q2 2026 baseline.

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
    development affecting JPM's capital, stress-test, or G-SIB status.
  - A material change in the Payments/Securities Services segment growth
    trend relative to Q2 2026.

## Conviction

**Rating: Medium.**

**Rationale:** JPMorgan shows a large, diversified, well-capitalized
banking franchise with CET1 ratios comfortably above regulatory minimums,
substantial liquidity, continued deposit and loan growth, and a
diversified fee/net-interest revenue mix. Conviction is held at Medium —
not directly comparable to V's High or MA's Medium ratings in this same
batch, since JPM is analyzed on bank-appropriate terms distinct from
V/MA's network-fee terms. Conviction is not higher because Q2 2026's
headline results require significant-items adjustment to interpret
correctly, credit costs — while currently moderate — are a disclosed and
monitored line item, and the Federal Reserve's 2026 severely-adverse
stress scenario shows a real, if modest, stressed CET1 decline that this
record does not discount to zero even while treating it strictly as a
supervisory scenario, not a forecast. This rating excludes valuation,
entry-price, allocation, trading, and margin/safe-leverage judgments.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research — the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** for
  JPM. All primary evidence was inspected by GPT-5.6 Thinking during the
  2026-07-27 evidence-recovery audit — see Source-access disclosure above.
- JPM's Q2 2026 Form 10-Q had not yet been included in the evidence-recovery
  audit's inspected source set at this record's evidence cutoff — claims
  requiring full quarter-end footnote detail beyond the earnings
  release/supplement remain tied to the Q1 2026 10-Q or are flagged as
  pending refresh once the Q2 10-Q is filed.
- The specific composition and duration of JPM's disclosed credit-cost and
  reserve figures (e.g. by loan category) is not established in this
  record.
- Segment-level detail beyond Payments/Securities Services within the
  Commercial & Investment Bank (e.g. detailed markets/investment-banking
  revenue breakdown) is not established in this record.

## Sources

See `JPM.yaml`'s `sources[]` for the structured register. All entries are
sourced to GPT-5.6 Thinking's independent evidence-recovery audit
(`governance/audits/BATCH6_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260727.md`),
with that provenance stated explicitly; no source in this record was
directly opened by this Claude session.
