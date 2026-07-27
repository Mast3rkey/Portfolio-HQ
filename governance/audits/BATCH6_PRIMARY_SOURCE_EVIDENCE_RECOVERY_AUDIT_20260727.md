# Batch 6 Primary-Source Evidence Recovery Audit

**Repository:** `Mast3rkey/Portfolio-HQ`  
**Workstream:** `WS-0005` Milestone 3, Batch 6  
**Authority:** `PI-0028`, applying `OPS-0008` §2  
**Companies:** Visa (`V`), Mastercard (`MA`), JPMorgan Chase (`JPM`)  
**Recovery reviewer:** GPT-5.6 Thinking  
**Audit date:** 2026-07-27  
**Purpose:** Independent primary-source recovery after the Claude implementation environment reported a session-wide HTTP 403 network-policy block.

## 1. Independence and authority boundary

GPT-5.6 Thinking did not author PR #170, PI-0028, or the blocked Claude implementation session.

This audit exercises only the standing evidence-recovery authority in `OPS-0008` §2. It:

- recovers and inspects primary evidence;
- records claim-level provenance and access limitations;
- determines whether the source-readiness gate can pass;
- supplies attributable evidence for the later implementation author.

It does **not**:

- create Company Intelligence records;
- change holdings, tiers, targets, roles, clusters, caps, weights, allocation, or margin policy;
- rank companies mechanically;
- recommend or execute trades;
- authorize another company, Batch 7, Milestone 4, or `OPS-0007` step I.

## 2. Source-readiness determination

**PASS for V, MA, and JPM using the latest publicly available primary sources as of 2026-07-27.**

Sufficient directly inspected primary evidence exists to begin drafting all three records and the required comparison artifact.

Two near-term refresh events are explicitly pending:

- Visa fiscal Q3 2026 results are scheduled for 2026-07-28.
- Mastercard Q2 2026 results are scheduled for 2026-07-30.

Those pending releases do not invalidate the current source-readiness pass. They create a mandatory near-term refresh trigger. The initial records must state the evidence cutoff dates below and must not present the forthcoming results as already known.

## 3. Source-access manifest

### 3.1 Visa (`V`)

| ID | Primary source | Date / period | Directly inspected | Drafting use |
|---|---|---:|---|---|
| V-1 | Visa 2025 Form 10-K, SEC accession `0001403161-25-000089` | FY ended 2025-09-30; filed 2025-11-06 | Yes, full parsed filing inspected | Business model, revenue categories, network economics, risk factors, capital allocation, legal matters |
| V-2 | Visa Form 10-Q, SEC accession `0001403161-26-000079` | Quarter ended 2026-03-31 | Yes, full parsed filing inspected | Current revenue, volume drivers, balance-sheet and litigation updates |
| V-3 | Visa fiscal Q2 2026 earnings release, Exhibit 99.1 to 8-K accession `0001403161-26-000077` | 2026-04-28 | Yes, filed exhibit inspected | Current operating metrics, revenue growth, repurchases, acquisitions |
| V-4 | U.S. Department of Justice, `U.S. v. Visa, Inc. [2024]` case page | Updated through DOJ page dated 2025-07-07 | Yes | Complaint, market definition, monopolization allegation, June 23, 2025 dismissal order |
| V-5 | DOJ Memorandum Opinion and Order page for `U.S. v. Visa, Inc. [2024]` | 2025-06-23 | Yes | Procedural status: Visa's motion to dismiss was denied |
| V-6 | Visa investor-relations notice for fiscal Q3 2026 results | 2026-07-07 | Yes | Confirms 2026-07-28 release date and creates refresh trigger |

Official locations:

- https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm
- https://www.sec.gov/Archives/edgar/data/1403161/000140316126000079/v-20260331.htm
- https://www.sec.gov/Archives/edgar/data/1403161/000140316126000077/q22026earningsrelease.htm
- https://www.justice.gov/atr/case/us-v-visa-inc-2024
- https://www.justice.gov/atr/case-document/visa-memorandum-opinion-and-order
- https://investor.visa.com/news/news-details/2026/Visa-to-Announce-Fiscal-Third-Quarter-2026-Financial-Results-on-July-28-2026/default.aspx

### 3.2 Mastercard (`MA`)

| ID | Primary source | Date / period | Directly inspected | Drafting use |
|---|---|---:|---|---|
| MA-1 | Mastercard 2025 Form 10-K, SEC accession `0001141391-26-000013` | FY ended 2025-12-31 | Yes, full parsed filing inspected | Business model, payment network and value-added services, economics, risks, legal matters |
| MA-2 | Mastercard Form 10-Q, SEC accession `0001141391-26-000031` | Quarter ended 2026-03-31 | Yes, full parsed filing inspected | Current revenue mix, rebates and incentives, regulatory and litigation developments |
| MA-3 | Mastercard Q1 2026 earnings release, Exhibit 99.1 to 8-K accession `0001141391-26-000029` | 2026-04-30 | Yes, filed exhibit inspected | Current GDV, cross-border and switched-transaction growth, revenue growth |
| MA-4 | Mastercard investor-relations notice for Q2 2026 results | 2026-07-08 | Yes | Confirms 2026-07-30 release date and creates refresh trigger |

Official locations:

- https://www.sec.gov/Archives/edgar/data/1141391/000114139126000013/ma-20251231.htm
- https://www.sec.gov/Archives/edgar/data/1141391/000114139126000031/ma-20260331.htm
- https://www.sec.gov/Archives/edgar/data/1141391/000114139126000029/ma03312026-exx991xearnings.htm
- https://investor.mastercard.com/investor-news/investor-news-details/2026/Mastercard-Incorporated-to-Host-Conference-Call-on-Second-Quarter-2026-Financial-Results/default.aspx

### 3.3 JPMorgan Chase (`JPM`)

| ID | Primary source | Date / period | Directly inspected | Drafting use |
|---|---|---:|---|---|
| JPM-1 | JPMorgan Chase 2025 Form 10-K, SEC accession `0001628280-26-008131` | FY ended 2025-12-31 | Yes, full parsed filing inspected | Business lines, assets, deposits, loans, risk, capital, regulation |
| JPM-2 | JPMorgan Chase Form 10-Q, SEC accession `0001628280-26-029344` | Quarter ended 2026-03-31 | Yes, full parsed filing inspected | Current balance sheet, CET1, liquidity, credit, segment metrics |
| JPM-3 | JPMorgan Chase Q2 2026 earnings release, Exhibit 99.1 to 8-K accession `0001628280-26-048078` | 2026-07-14 | Yes, filed exhibit inspected | Current firmwide and segment results, Payments, Securities Services, capital and credit |
| JPM-4 | JPMorgan Chase Q2 2026 financial supplement, Exhibit 99.2 to the same 8-K | 2026-07-14 | Yes, filed exhibit inspected | Detailed segment and regulatory-capital support |
| JPM-5 | Federal Reserve 2026 Dodd-Frank Act stress-test results and accessibility tables | 2026-06-24 through 2026-06-30 updates | Yes | Bank-specific stressed CET1 decline and system-wide scenario context |
| JPM-6 | Financial Stability Board 2025 G-SIB list | 2025-11-27 | Yes | Current G-SIB designation framework and higher-loss-absorbency consequences |

Official locations:

- https://www.sec.gov/Archives/edgar/data/19617/000162828026008131/jpm-20251231.htm
- https://www.sec.gov/Archives/edgar/data/19617/000162828026029344/jpm-20260331.htm
- https://www.sec.gov/Archives/edgar/data/19617/000162828026048078/a2q26erfexhibit991narrative.htm
- https://www.sec.gov/Archives/edgar/data/19617/000162828026048078/a2q26erfex992supplement.htm
- https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2026.htm
- https://www.federalreserve.gov/publications/2026-june-stress-test-results-accessibility-tables.htm
- https://www.fsb.org/2025/11/2025-list-of-global-systemically-important-banks-g-sibs/

## 4. Recovered factual baseline

The following is a drafting baseline, not a complete investment conclusion.

### 4.1 Visa

**Filed facts**

- Visa describes itself as a global payments technology company providing authorization, clearing and settlement through VisaNet. It states that it is not a financial institution, does not issue cards, does not extend credit, and does not set account-holder rates or fees.
- Fiscal 2025 revenue categories included service revenue of $17.539 billion, data-processing revenue of $19.993 billion, international-transaction revenue of $14.166 billion, other revenue of $4.053 billion, and client incentives of $15.751 billion as a reduction of revenue, producing net revenue of $40.0 billion.
- Fiscal 2025 value-added-services revenue was $10.9 billion.
- Visa's service revenue is tied principally to payments volume; data-processing revenue is tied principally to processed transactions; international-transaction revenue is earned from cross-border processing and currency conversion.
- For fiscal Q2 2026, Visa reported $11.2 billion of net revenue, up 17% year over year; constant-dollar payments volume grew 9%, total cross-border volume grew 12%, cross-border volume excluding intra-Europe grew 11%, and processed transactions grew 9% to 66.1 billion.
- The 2025 10-K discloses continuing U.S. interchange litigation, a litigation-escrow structure, DOJ debit-network litigation, related private class actions, and other merchant and ATM matters.
- The DOJ case page records a September 24, 2024 monopolization complaint concerning debit-network services and a June 23, 2025 order denying Visa's motion to dismiss.

**Drafting judgments that remain judgments**

- Visa's moat should be analyzed through network acceptance, issuer/acquirer integration, reliability, tokenization and security, and the cost and friction of replacing the network. Do not present "duopoly" alone as proof of durability.
- Client incentives are economically important and should be treated as a competitive cost of sustaining and renewing network relationships, not ignored because they are netted against revenue.
- Cross-border economics are attractive but more exposed to travel, macroeconomic conditions, currency movements, and regulatory intervention.
- The DOJ and interchange matters are live thesis risks. Describe allegations and procedural status precisely; do not state that liability has been established.

### 4.2 Mastercard

**Filed facts**

- Mastercard classifies net revenue into payment network and value-added services and solutions.
- Payment-network revenue is generated primarily from fees based on gross dollar volume and from switching and network services.
- Fiscal 2025 payment-network net revenue was $19.476 billion and value-added-services-and-solutions net revenue was $13.315 billion.
- Fiscal 2025 payment-network revenue included $20.522 billion of customer rebates and incentives.
- Value-added services include security, digital and authentication solutions, consumer acquisition and engagement, business and market insights, processing and gateway services, account-based payments, real-time payments and open finance.
- In Q1 2026, total net revenue was $8.398 billion, up 16%; payment-network revenue rose 12% and value-added-services-and-solutions revenue rose 22%. On a local-currency basis, GDV grew 7% to $2.7 trillion, cross-border volume grew 13%, and switched transactions grew 9%.
- Q1 2026 payment-network rebates and incentives rose 23%, or 19% on a currency-neutral basis.
- Mastercard's 10-Q states that interchange fees and acceptance practices face regulatory and legal challenges in multiple jurisdictions and may materially affect growth and results.
- Current disclosed matters include U.S. interchange opt-outs, U.K. and pan-European merchant claims, Portuguese and Dutch proceedings, and other regulatory matters.

**Drafting judgments that remain judgments**

- Mastercard's comparison with Visa should separate the shared network mechanism from company-specific mix, geography, customer relationships, service attach, and execution.
- Value-added services may deepen relationships and diversify revenue, but their moat, margins, acquisition dependence and stand-alone competitiveness must be evaluated rather than assumed.
- Rebates and incentives are a material competitive cost and a source of estimation uncertainty.
- Regulatory and litigation claims must be labeled by jurisdiction, allegation, procedural status and disclosed exposure; do not aggregate unlike matters into one unsupported liability estimate.

### 4.3 JPMorgan Chase

**Filed and regulator facts**

- JPMorgan Chase reported $4.4 trillion of assets and $362.4 billion of stockholders' equity at 2025 year-end and operates across consumer and community banking, commercial and investment banking, and asset and wealth management, with Corporate activities reported separately.
- At March 31, 2026, the firm reported $291 billion of CET1 capital, standardized and advanced CET1 ratios of 14.3% and 14.1%, a 5.6% supplementary leverage ratio, and approximately $1.5 trillion of liquidity sources.
- For Q2 2026, JPMorgan reported $21.2 billion of net income, including a $4.6 billion gain related to Visa shares and $1.0 billion of gains on other equity investments. The release separately reported net income excluding significant items of $16.9 billion.
- Q2 2026 firmwide metrics included standardized and advanced CET1 ratios of 14.1% and 14.2%, $590 billion of total loss-absorbing capacity, $1.5 trillion of cash and marketable securities, average loans of $1.5 trillion, and average deposits up 7% year over year.
- Q2 2026 credit costs were $2.5 billion, including $2.4 billion of net charge-offs and a $149 million net reserve build.
- In the Commercial & Investment Bank, Q2 2026 Payments revenue was $5.3 billion, up 12%, and Securities Services revenue was $1.7 billion, up 17%. Banking & Payments revenue was $11.2 billion.
- The Federal Reserve's 2026 stress-test accessibility tables report a 2.0-percentage-point decline from starting to minimum CET1 for JPMorgan Chase under the severely adverse scenario. The result is a supervisory scenario, not a forecast.
- The FSB's 2025 G-SIB framework confirms that listed G-SIBs are subject to higher capital buffers, TLAC, resolvability requirements and heightened supervision. JPMorgan's record must describe G-SIB status as a constraint and resilience framework, not as a guarantee against loss.

**Drafting judgments that remain judgments**

- JPMorgan is not directly comparable with V or MA using ordinary operating margins, free-cash-flow yield, or net-debt metrics. Use bank-appropriate measures: CET1, risk-weighted assets, liquidity, credit costs, charge-offs, reserves, deposit franchise, net interest income, fee mix and stress resilience.
- The firm combines deposit and lending economics with payments, custody, markets, investment banking and asset management. Diversification may stabilize earnings but also creates complexity, regulatory burden, trading and credit exposure.
- Q2 2026 results contain material significant items. Do not use reported net income or ROE without separating the Visa-share and other investment gains.
- Stress-test results support scenario analysis but do not establish a safe leverage level, predict an actual recession outcome or justify portfolio margin.

## 5. Required V-versus-MA-versus-JPM comparison discipline

The implementation may use this recovered evidence to compare:

- network toll-road economics versus regulated balance-sheet intermediation;
- volume and cross-border sensitivity versus credit and rate sensitivity;
- customer incentives and partner dependencies;
- regulatory and litigation exposure;
- cybersecurity, fraud and alternative-rail risk;
- recurring and transaction-sensitive revenue;
- overlap between V and MA;
- the distinct exposure added by JPM;
- qualitative next-best use of capital.

It must not:

- normalize incompatible metrics into one score;
- compare JPM's bank leverage with Visa/Mastercard corporate debt as though they were the same;
- state a preferred security mechanically;
- change governed policy;
- treat current tiers and targets as evidence of investment quality.

## 6. Evidence limitations and refresh triggers

### Current limitations

- Visa's latest available operating quarter at this audit date is the quarter ended 2026-03-31. Fiscal Q3 results had not yet been released.
- Mastercard's latest available operating quarter at this audit date is the quarter ended 2026-03-31. Q2 results had not yet been released.
- JPMorgan's Q2 earnings release and supplement were available, but the June 30, 2026 Form 10-Q had not yet been included in the inspected source set. Claims requiring full quarter-end footnote detail should remain tied to the Q1 10-Q or be refreshed when the Q2 10-Q is filed.
- Court and regulator matters can change quickly. Every record must carry an `as_of` date and preserve procedural qualifiers.
- Earnings releases include management-selected and non-GAAP measures. Filed GAAP figures and reconciliations control.

### Mandatory near-term refresh

Refresh the records and comparison artifact after:

1. Visa furnishes fiscal Q3 2026 results on 2026-07-28.
2. Mastercard furnishes Q2 2026 results on 2026-07-30.
3. JPMorgan files its Q2 2026 Form 10-Q, if it adds material information beyond the inspected earnings package.
4. Any material DOJ, court, Federal Reserve, FSB or interchange-regulatory development.

The initial implementation does not need to wait for these events. It must label the current evidence cutoff and keep the refresh status explicit.

## 7. Source-readiness conclusion

**PASS.**

The blocked Claude session may resume Batch 6 implementation using this audit as retained,
attributable primary-source recovery evidence under `OPS-0008` §2.

Conditions:

1. Include or retain this audit under the repository's established `governance/audits/` convention.
2. Do not represent Claude's blocked WebFetch attempts as successful direct inspection.
3. Attribute recovered primary evidence to GPT-5.6 Thinking.
4. Preserve the source dates and limitations in each record.
5. Complete the scheduled post-July-30 refresh through a bounded update; do not automatically change policy.
6. Submit the implementation PR to a separate independent exact-head reviewer.

**No portfolio-policy or trading authority is created by this audit.**
