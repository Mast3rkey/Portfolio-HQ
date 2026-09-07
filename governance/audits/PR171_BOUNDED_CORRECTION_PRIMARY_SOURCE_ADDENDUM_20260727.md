# PR #171 Bounded-Correction Primary-Source Addendum

**Repository:** `Mast3rkey/Portfolio-HQ`
**Workstream:** WS-0005 Milestone 3, Batch 6
**Authority:** `PI-0028`, applying the bounded correction identified by the independent exact-head
review of PR #171
**Companies:** Visa (`V`), Mastercard (`MA`), JPMorgan Chase (`JPM`)
**Evidence reviewer:** GPT-5.6 Thinking
**Prepared:** 2026-07-27
**Purpose:** close specific mandatory-research gaps and correct overclaims without expanding the
authorized company set or creating portfolio policy.

## 1. Authority and provenance boundary

This addendum supplies primary-source evidence for a correction to the existing V/MA/JPM
implementation. It does not:

- create a fourth company record;
- rank securities mechanically;
- change tiers, targets, holdings, clusters, caps, weights, allocation, or margin;
- authorize a trade, order, Batch 7, Milestone 4, or `OPS-0007` step I;
- approve any conviction rating;
- state that the Claude implementation session directly opened these sources.

The correction author must attribute the facts below to GPT-5.6 Thinking's independent inspection
of the named official filings. Calculated figures must be labeled as arithmetic derived from
issuer-reported inputs, not issuer-defined non-GAAP measures.

## 2. Official source manifest

### Visa

- Visa 2025 Form 10-K, SEC accession `0001403161-25-000089`, fiscal year ended 2025-09-30,
  filed 2025-11-06:
  `https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm`
- Visa Form 10-Q, SEC accession `0001403161-26-000079`, quarter ended 2026-03-31:
  `https://www.sec.gov/Archives/edgar/data/1403161/000140316126000079/v-20260331.htm`
- Visa 2020 Form 10-K, fiscal year ended 2020-09-30, for observed downturn behavior: use the
  corresponding official SEC filing and preserve exact accession/date in the corrected source
  ledger.

### Mastercard

- Mastercard 2025 Form 10-K, SEC accession `0001141391-26-000013`, fiscal year ended 2025-12-31,
  filed 2026-02-11:
  `https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm`
- Mastercard Form 10-Q, SEC accession `0001141391-26-000031`, quarter ended 2026-03-31:
  `https://www.sec.gov/Archives/edgar/data/1141391/000114139126000031/ma-20260331.htm`
- Mastercard 2020 Form 10-K, fiscal year ended 2020-12-31, for observed downturn behavior: use the
  corresponding official SEC filing and preserve exact accession/date in the corrected source
  ledger.

### JPMorgan Chase

- JPMorgan Chase Form 10-Q, SEC accession `0001628280-26-029344`, quarter ended 2026-03-31:
  `https://www.sec.gov/Archives/edgar/data/19617/000162828026029344/jpm-20260331.htm`
- JPMorgan Chase Q2 2026 earnings release, Exhibit 99.1 to 8-K accession
  `0001628280-26-048078`, furnished 2026-07-14:
  `https://www.sec.gov/Archives/edgar/data/19617/000162828026048078/a2q26erfexhibit991narrative.htm`
- JPMorgan Chase Q2 2026 financial supplement, Exhibit 99.2 to the same 8-K:
  `https://www.sec.gov/Archives/edgar/data/19617/000162828026048078/a2q26erfex992supplement.htm`
- JPMorgan Chase 2026 capital-results filing confirming the continuing 11.5% standardized CET1
  requirement:
  `https://www.sec.gov/Archives/edgar/data/19617/000162828026045167/jpmc2026ccarresultsex99.htm`

## 3. Visa correction evidence

### 3.1 Incentive arithmetic

Fiscal-2025 issuer-reported components:

- service revenue: $17.539 billion;
- data-processing revenue: $19.993 billion;
- international-transaction revenue: $14.166 billion;
- other revenue: $4.053 billion;
- client incentives: $15.751 billion reduction;
- net revenue: $40.000 billion.

Correct arithmetic:

- gross revenue before incentives:
  $17.539B + $19.993B + $14.166B + $4.053B = **$55.751B**;
- incentives as a percentage of pre-incentive gross revenue:
  $15.751B / $55.751B = **approximately 28.25%**.

Do not use $71.3 billion or approximately 22%.

### 3.2 Financial quality and capital allocation

For fiscal 2025, Visa reported:

- net revenue: $40.000 billion;
- operating income: $23.994 billion;
- net income: $20.058 billion;
- operating cash flow: $23.059 billion;
- purchases of property, equipment, and technology: $1.482 billion;
- total debt: $25.392 billion; carrying value of debt: $25.171 billion;
- common-stock repurchases: $18.2 billion;
- dividends declared and paid: $4.6 billion;
- remaining repurchase authorization at year-end: $24.9 billion.

Reviewer arithmetic, not an issuer-defined free-cash-flow measure:

- operating cash flow less property/equipment/technology purchases:
  **approximately $21.577 billion**.

Management-history evidence available from the filing:

- Ryan McInerney signed the 2025 Form 10-K as Chief Executive Officer.
- The corrected record should avoid inferring management quality from title or tenure alone.
- Capital-allocation history may be assessed from the multi-year dividend and repurchase record,
  but price discipline and value creation from repurchases remain judgments requiring caution.

### 3.3 Mix, dependencies, substitutes, and cyber risk

The 2025 filing provides source-backed evidence that should replace generic gaps:

- consumer credit, consumer debit, and commercial payment-volume categories are disclosed and
  should be reported with their exact table basis and period;
- Visa depends on financial-institution issuers, acquirers, processors, merchants, and routing
  relationships; incentives, rebates, and support payments are used to maintain and expand those
  relationships;
- competition includes other card networks, domestic networks, closed-loop systems, digital
  wallets, real-time account-to-account systems, bank-led alternatives, and emerging
  blockchain/stablecoin-based rails;
- fraud, cybersecurity, network availability, tokenization, authentication, and data protection
  are operating and thesis risks, not merely generic technology risks.

### 3.4 Demonstrated downturn behavior

Visa's fiscal-2020 filing provides an observed stress case:

- net revenue declined about 5% year over year;
- international-transaction revenue declined materially as cross-border travel contracted;
- net income declined about 10%;
- the company remained profitable.

Use this as historical evidence, not as a forecast of the next recession.

### 3.5 Disconfirming evidence to record explicitly

At minimum, document the active search for evidence that could weaken the high-quality network
thesis:

- incentives rising faster than underlying volume or revenue;
- loss of issuer/acquirer routing relationships;
- alternative-rail substitution;
- regulatory or court outcomes affecting debit routing, interchange, or network practices;
- sustained cross-border weakness;
- major fraud, cyber, or reliability failure;
- capital returns that destroy value or weaken balance-sheet flexibility.

## 4. Mastercard correction evidence

### 4.1 Financial quality and capital allocation

For fiscal 2025, Mastercard reported:

- operating margin: 57.6%;
- net income: $14.968 billion;
- operating cash flow: $17.648 billion;
- purchases of property and equipment: $0.489 billion;
- capitalized software: $0.726 billion;
- total debt: $19.000 billion;
- long-term debt: $18.251 billion;
- share repurchases: $11.727 billion;
- dividends paid: approximately $2.8 billion;
- total capital returned to stockholders: approximately $14.5 billion.

Reviewer arithmetic, not an issuer-defined free-cash-flow measure:

- operating cash flow less property/equipment purchases and capitalized software:
  **approximately $16.433 billion**.

Management-history evidence:

- Michael Miebach has served as President and Chief Executive Officer since January 2021.
- The filing records prior Mastercard operating roles, including President and Chief Product
  Officer.
- Tenure and internal experience are facts; execution quality and acquisition discipline remain
  judgments.

### 4.2 Geography, product mix, dependencies, and cyber risk

The 2025 filing supports a more complete record:

- net revenue is disclosed between the Americas and APEMEA, allowing geographic-mix analysis;
- GDV is disclosed across consumer credit, consumer debit/prepaid, and commercial products;
- Mastercard depends on issuers, acquirers, merchants, processors, settlement banks, and other
  network participants;
- settlement and counterparty exposure must be distinguished from consumer credit risk;
- cyber, operational resilience, fraud, authentication, and data-security risks are material;
- competitors and substitutes include Visa, American Express and other closed-loop systems,
  domestic networks, account-to-account/real-time-payment systems, wallets, fintech platforms, and
  emerging alternative rails.

### 4.3 Demonstrated downturn behavior

Mastercard's fiscal-2020 filing supplies an observed stress case:

- net revenue declined about 9%;
- cross-border volume declined about 29%;
- operating margin fell from 57.2% to 52.8%;
- net income declined about 21%;
- the company remained profitable.

Use this to distinguish revenue-line cyclicality from JPM's balance-sheet and credit transmission.

### 4.4 Disconfirming evidence and conviction discipline

Explicitly document searches for:

- rebates/incentives persistently outgrowing network revenue;
- inability of value-added services to sustain attractive margins or organic growth;
- issuer/acquirer disintermediation;
- alternative-rail substitution;
- multi-jurisdiction regulatory or litigation outcomes;
- cyber, fraud, settlement, or reliability failures;
- acquisition dependence or weak return on acquired assets.

The current record does **not** establish that Visa's comparable incentive trend is better because
a like-for-like Visa quarterly growth rate was not supplied. Do not use missing Visa data as
evidence against Mastercard. Reassess each rating independently.

## 5. JPMorgan Chase correction evidence

### 5.1 Capital headroom

At 2026-03-31, JPMorgan reported:

- standardized CET1 ratio: 14.3%;
- advanced CET1 ratio: 14.1%;
- standardized CET1 requirement including buffers: 11.5%;
- supplementary leverage ratio: 5.6%;
- applicable SLR requirement: 4.3%;
- CET1 capital: $291 billion;
- approximately $1.5 trillion of liquidity sources.

Precise arithmetic:

- standardized CET1 headroom: **2.8 percentage points**;
- advanced CET1 ratio versus the same 11.5% benchmark: **2.6 percentage points**;
- SLR headroom: **1.3 percentage points**.

Use the exact benchmark rather than “wide margin” or “comfortably above” without quantification.
Regulatory headroom is not a guarantee against loss.

### 5.2 Q2 2026 economics by business line

The Q2 2026 release reports:

- managed firmwide net revenue: $58.022 billion;
- net interest income: $25.6 billion;
- net interest income excluding Markets: $23.7 billion, with lower rates partly offsetting higher
  balances;
- Investment Banking revenue: $3.9 billion;
- Investment Banking fees: $3.3 billion;
- Payments revenue: $5.3 billion;
- Markets revenue: $12.1 billion;
- Fixed Income Markets revenue: $6.1 billion;
- Equity Markets revenue: $6.0 billion;
- Securities Services revenue: approximately $1.7 billion;
- Asset & Wealth Management revenue: $6.851 billion;
- AWM assets under management: $5.1 trillion;
- provision for credit losses: $2.515 billion;
- net charge-offs: approximately $2.4 billion;
- net reserve build: $149 million.

Reviewer arithmetic:

- Payments plus Securities Services were approximately $6.96 billion, or roughly **12.0%** of
  Q2 managed firmwide net revenue.

This percentage is only a directional scale comparison. Payments and Securities Services sit in
different disclosed groupings and managed revenue is non-GAAP; do not imply that the arithmetic is
a standalone segment margin or risk measure.

### 5.3 Significant items and Visa-share wording

The release reports:

- Q2 net income: $21.2 billion;
- net income excluding significant items: $16.9 billion;
- a $4.6 billion net gain related to Visa shares;
- $1.0 billion of gains on certain other equity investments.

State only that the quarter included a gain related to Visa shares. Do not claim a continuing
equity stake after the transaction unless another source establishes it. Do not infer that the firm
presented the adjusted measure “precisely because” management believed headline profitability was
overstated.

### 5.4 Capital return and management evidence

The Q2 release reports:

- common dividend: $4.0 billion;
- common-stock net repurchases: $6.2 billion.

Jamie Dimon is identified as Chairman and Chief Executive Officer. The record may discuss long
tenure and capital-management continuity only with the appropriate official source. It must still
separate management claims from demonstrated outcomes and avoid treating “fortress” language as an
independent conclusion.

### 5.5 Disconfirming evidence to record explicitly

Search and disclose evidence that could weaken the diversified-bank thesis:

- deposit outflows or rising deposit costs;
- adverse interest-rate sensitivity and net-interest-income compression;
- reserve inadequacy or acceleration in charge-offs;
- stressed capital depletion beyond current expectations;
- material trading, operational, cyber, conduct, or litigation loss;
- weak returns from business complexity or sustained cost growth;
- investment-banking and markets revenue cyclicality;
- capital distributions that reduce resilience;
- regulatory changes raising capital, liquidity, or resolution costs.

Merchant acquiring should be described only to the extent separately disclosed. When not
quantified, say so rather than treating the Payments line as a pure acquiring business.

## 6. Required provenance and lifecycle language

Use this wording pattern, adapted per file:

> The original Batch 6 recovery audit was supplied externally by GPT-5.6 Thinking. The
> as-delivered file had SHA-256 `c248...`; the repository retained a substantively unchanged copy
> after trailing-whitespace normalization with SHA-256 `ee497...`. The Claude implementation
> session did not directly inspect the cited primary documents.

Do not say “retained verbatim” or “copied byte-for-byte.”

For conviction fields before approval, use this pattern:

> This is a proposed human-judgment rating presented for independent exact-head review and
> principal acceptance. AI-assisted research and drafting do not themselves constitute approval.

## 7. Completion boundary

The corrected implementation may remain a complete Batch 6 candidate only after:

- every mandatory `PI-0028` research field is present or a genuinely unresolvable limitation is
  explicitly justified;
- the arithmetic and overclaims are corrected;
- exact-head validation and CI pass;
- independent delta review approves the corrected head;
- the principal accepts that exact head;
- the PR merges;
- independent post-merge verification confirms byte identity, scope, tests, protected paths, and
  PROVISIONAL status.

This addendum creates no automatic portfolio-policy consequence.
