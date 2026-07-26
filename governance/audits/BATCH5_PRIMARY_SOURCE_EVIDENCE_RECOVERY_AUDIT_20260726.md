# WS-0005 Milestone 3, Batch 5 — Primary-Source Evidence-Recovery Audit

**Companies:** MSFT, GOOGL, META, AMZN
**Deferred:** EQIX
**Authority:** OPS-0008 §2 and PI-0027 §D
**Inspector:** GPT-5.6 Thinking, independent ChatGPT session
**Inspection date:** 2026-07-26
**Purpose:** bounded factual and sourcing recovery only
**Policy authority:** none
**Repository mutation:** none

## 1. Recovery input and scope

This audit responds to `BATCH5_SOURCE_READINESS_MANIFEST.md`, SHA-256:

`8a9e943e0f189ea83d2c89fd34fdb263bd0c23ee49f9b49a2a81e08cc033a211`

That manifest documented that the implementing Claude Code session could directly inspect only limited Microsoft investor material and could not directly inspect the SEC, Alphabet, Meta, or Amazon primary documents required for Batch 5. It correctly stopped before drafting.

This evidence-recovery session directly inspected official issuer, SEC, U.S. Department of Justice, U.S. Federal Trade Commission, and European Commission sources. It did not:

- draft Company Intelligence records;
- produce the Batch 5 comparison artifact;
- make a tier, target, allocation, or trade recommendation;
- rank or score the four companies;
- modify Portfolio-HQ;
- create policy authority.

## 2. Recovery determination

**PASS — the blocked material source categories identified in the manifest now have directly inspected primary evidence sufficient for Batch 5 drafting, subject to the claim envelope and limitations in this audit.**

The implementation session may resume only if it:

1. retains this audit with exact inspector attribution;
2. uses the directly supported facts and source references below;
3. labels management guidance, regulator allegations, preliminary findings, inference, and judgment correctly;
4. excludes any additional material claim not supported by this audit or another directly inspected primary source;
5. stops again if a new material claim requires inaccessible evidence.

This PASS does not declare any company record complete. It clears the source-readiness gate for a bounded drafting pass.

---

# 3. Microsoft (MSFT)

## 3.1 Primary sources directly inspected

### MSFT-P1 — Microsoft 2025 Annual Report

- **Issuer:** Microsoft Corporation
- **Document:** Microsoft 2025 Annual Report / fiscal 2025 Form 10-K content
- **Period:** year ended 2025-06-30
- **Official URL:** https://www.microsoft.com/investor/reports/ar25/index.html
- **Download center:** https://www.microsoft.com/investor/reports/ar25/download-center/
- **Primary-source status:** issuer-filed annual-report content
- **Sections inspected:**
  - Shareholder Letter
  - Business
  - Operating Segments
  - Management’s Discussion and Analysis
  - Summary Results of Operations
  - Cash, Cash Equivalents, and Investments
  - Cash Flows
  - Property and Equipment
  - Segment Information and Geographic Data
  - OpenAI partnership disclosure
- **Inspector:** GPT-5.6 Thinking, this session

### MSFT-P2 — Microsoft FY2026 Q3 earnings release

- **Issuer:** Microsoft Corporation
- **Document:** “Microsoft Cloud and AI Strength Fuels Third Quarter Results”
- **Date:** 2026-04-29
- **Period:** quarter ended 2026-03-31
- **Official URL:** https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/press-release-webcast
- **Primary-source status:** issuer earnings release
- **Sections inspected:** consolidated results, segment results, capital return, OpenAI non-GAAP reconciliation
- **Inspector:** GPT-5.6 Thinking, this session

### MSFT-P3 — Microsoft FY2026 Q3 earnings call transcript

- **Issuer:** Microsoft Corporation
- **Document:** FY2026 Q3 earnings conference call
- **Date:** 2026-04-29
- **Official URL:** https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3
- **Primary-source status:** official issuer transcript; management statements and guidance are unaudited and forward-looking where indicated
- **Sections inspected:** prepared remarks, financial results, capital expenditures, custom silicon, capacity, remaining performance obligations, outlook
- **Inspector:** GPT-5.6 Thinking, this session

### MSFT-R1 — European Commission cloud DMA preliminary position

- **Authority:** European Commission
- **Document:** preliminary position on AWS and Azure gatekeeper designation
- **Date:** 2026-06-25
- **Official URL:** https://digital-markets-act.ec.europa.eu/commission-reaches-preliminary-position-amazons-and-microsofts-market-leading-cloud-services-should-2026-06-25_en
- **Primary-source status:** regulator statement; preliminary, not a final designation
- **Sections inspected:** designation rationale, lock-in, switching costs, ecosystem, AI tools and partnerships
- **Inspector:** GPT-5.6 Thinking, this session

## 3.2 Verified factual extracts

### Business and segment economics

1. Fiscal 2025 revenue was **$281.724 billion**, operating income was **$128.528 billion**, and net income was **$101.832 billion**.
   **Source:** MSFT-P1, “Summary Results of Operations.”

2. Fiscal 2025 segment revenue and operating income were:
   - Productivity and Business Processes: **$120.810 billion revenue**, **$69.773 billion operating income**.
   - Intelligent Cloud: **$106.265 billion revenue**, **$44.589 billion operating income**.
   - More Personal Computing: **$54.649 billion revenue**, **$14.166 billion operating income**.
   **Source:** MSFT-P1, “Segment Results of Operations.”

3. Microsoft reported that Azure and other cloud services revenue grew **34%** in fiscal 2025.
   **Source:** MSFT-P1, Shareholder Letter and Intelligent Cloud MD&A.

4. Microsoft Cloud gross margin was **69%** in fiscal 2025; Microsoft attributed the year-over-year pressure partly to scaling AI infrastructure, partly offset by Azure efficiencies.
   **Source:** MSFT-P1, “Summary Results of Operations.”

### Capital intensity, liquidity, and capital allocation

5. Fiscal 2025 additions to property and equipment were **$64.551 billion**, compared with **$44.477 billion** in fiscal 2024.
   **Source:** MSFT-P1, Consolidated Cash Flows / MD&A.

6. At 2025-06-30, cash, cash equivalents, and short-term investments totaled **$94.6 billion**.
   **Source:** MSFT-P1, “Cash, Cash Equivalents, and Investments.”

7. Fiscal 2025 common-stock repurchases were **$13.0 billion** and cash dividends paid were **$24.082 billion**.
   **Source:** MSFT-P1, “Share Repurchases and Dividends” and Consolidated Cash Flows.

8. At 2025-06-30, Microsoft reported **$32.1 billion** of commitments for construction, building improvements, and leasehold improvements, primarily related to datacenters.
   **Source:** MSFT-P1, Property and Equipment note.

### Current quarter, AI monetization, custom silicon, and capacity

9. FY2026 Q3 revenue was **$82.9 billion**, operating income **$38.4 billion**, and net income **$31.8 billion**.
   **Source:** MSFT-P2, headline consolidated results.

10. FY2026 Q3 Microsoft Cloud revenue was **$54.5 billion**, up **29%** year over year; Azure and other cloud services revenue grew **40%**.
    **Source:** MSFT-P2 and MSFT-P3, segment results.

11. Management stated that Microsoft’s AI business exceeded a **$37 billion annual revenue run rate**, up **123%** year over year. Treat this as an issuer-defined management metric, not a separately audited segment.
    **Source:** MSFT-P3, CEO and CFO prepared remarks.

12. FY2026 Q3 capital expenditures were **$31.9 billion**; management said roughly two-thirds related to short-lived assets, primarily GPUs and CPUs.
    **Source:** MSFT-P3, CFO prepared remarks.

13. Management guided to more than **$40 billion** of Q4 capital expenditures and approximately **$190 billion** for calendar 2026. These are forward-looking management estimates, not realized facts.
    **Source:** MSFT-P3, Q4 outlook.

14. Management stated that Azure demand continued to exceed available capacity and expected capacity constraints through at least 2026. This is management’s operational assessment.
    **Source:** MSFT-P3, Azure results and outlook.

15. Microsoft stated that:
    - Maia 200 was live in Iowa and Arizona datacenters;
    - Cobalt CPUs were deployed in nearly half of its datacenter regions;
    - custom networking, security, and virtualization silicon supported millions of servers.
    These are management claims from the official transcript, not independently benchmarked findings.
    **Source:** MSFT-P3, CEO prepared remarks.

### OpenAI relationship

16. The fiscal 2025 annual report states that Microsoft and OpenAI have a long-term strategic partnership dating to 2019, reciprocal revenue-sharing arrangements, rights to OpenAI intellectual property for integration into Microsoft products, Azure exclusivity for the OpenAI API, and a right of first refusal on new OpenAI capacity needs.
    **Source:** MSFT-P1, business discussion of the OpenAI partnership.

17. FY2026 Q3 GAAP results included Microsoft’s OpenAI investment impact; the earnings release separately presented non-GAAP results excluding that effect.
    **Source:** MSFT-P2, non-GAAP definition and reconciliation.

### Regulatory evidence

18. On 2026-06-25, the European Commission announced a **preliminary** view that Azure and AWS should be designated as DMA gatekeepers for cloud services. The Commission cited gateway importance, user-base entrenchment, lock-in, high switching costs, ecosystem breadth, and AI tools and partnerships.
    **Source:** MSFT-R1.
    **Required label:** regulator preliminary finding, not final adjudication.

## 3.3 Claim limitations and disconfirming evidence

- Do not describe Microsoft as an uncontested cloud or AI monopoly from these materials.
- The $37 billion AI run-rate is management-defined and not a separately audited reportable segment.
- Calendar 2026 capital expenditures and capacity commentary are forward-looking.
- The annual report shows AI infrastructure scaling can pressure cloud gross margin.
- Azure capacity constraints can limit conversion of demand into near-term revenue.
- The Commission’s cloud designation view is preliminary.
- No customer represented more than 10% of Microsoft fiscal 2025 revenue, according to MSFT-P1; do not infer absence of workload, supplier, or partner concentration from that fact.
- Specific supplier shares or dependence on NVDA, AMD, TSM, or other holdings were not quantified in the inspected filings.

---

# 4. Alphabet (GOOGL)

## 4.1 Primary sources directly inspected

### GOOGL-P1 — Alphabet Q1 2026 Form 10-Q

- **Issuer:** Alphabet Inc.
- **Document:** Form 10-Q for quarter ended 2026-03-31
- **Accession:** `0001652044-26-000048`
- **Filed:** 2026-04-30; accepted 2026-04-29
- **Official URL:** https://www.sec.gov/Archives/edgar/data/1652044/000165204426000048/goog-20260331.htm
- **Filing index:** https://www.sec.gov/Archives/edgar/data/1652044/000165204426000048/0001652044-26-000048-index.htm
- **Primary-source status:** SEC-filed quarterly report
- **Sections/pages inspected:**
  - Financial Statements, pp. 6–10
  - Revenue Backlog, p. 10
  - Segment Information, pp. 29–30
  - MD&A — Google Cloud, pp. 35–42
  - Liquidity and Capital Resources, pp. 45–47
  - Commitments and Contingencies / Legal Matters, pp. 25–28
  - Risk Factors
- **Inspector:** GPT-5.6 Thinking, this session

### GOOGL-R1 — DOJ search monopolization case page

- **Authority:** U.S. Department of Justice, Antitrust Division
- **Case:** U.S. and Plaintiff States v. Google LLC [2020]
- **Official URL:** https://www.justice.gov/atr/case/us-and-plaintiff-states-v-google-llc
- **Primary-source status:** official regulator litigation docket/index
- **Sections inspected:** final judgment, remedies materials, 2026 compliance status reports
- **Inspector:** GPT-5.6 Thinking, this session

### GOOGL-R2 — DOJ ad-tech monopolization case page

- **Authority:** U.S. Department of Justice, Antitrust Division
- **Case:** U.S. and Plaintiff States v. Google LLC [2023]
- **Official URL:** https://www.justice.gov/atr/case/us-and-plaintiff-states-v-google-llc-2023
- **Primary-source status:** official regulator litigation docket/index
- **Sections inspected:** April 2025 liability opinion, 2025 remedies materials
- **Inspector:** GPT-5.6 Thinking, this session

## 4.2 Verified factual extracts

### Revenue model and segment economics

1. Q1 2026 revenue was **$109.896 billion**, up **22%** year over year; operating income was **$39.696 billion**.
   **Source:** GOOGL-P1, MD&A executive overview, pp. 38–39.

2. Q1 2026 revenue by type included:
   - Google Search & other: **$60.399 billion**
   - YouTube ads: **$9.883 billion**
   - Google Network: **$6.971 billion**
   - Total Google advertising: **$77.253 billion**
   - Subscriptions, platforms, and devices: **$12.384 billion**
   - Google Cloud: **$20.028 billion**
   **Source:** GOOGL-P1, revenue-by-type table, p. 40.

3. Q1 2026 segment operating income was:
   - Google Services: **$40.589 billion**
   - Google Cloud: **$6.598 billion**
   - Other Bets: **$(2.100) billion**
   **Source:** GOOGL-P1, segment table, pp. 29–30 and 42.

4. Google Cloud revenue grew **63%** year over year, primarily from Google Cloud Platform infrastructure and platform services.
   **Source:** GOOGL-P1, MD&A, pp. 38 and 41.

5. Google Search & other revenue increased **$9.7 billion** year over year; the filing attributes growth to search-query adoption and usage, advertiser spending, and ad-format/delivery improvements.
   **Source:** GOOGL-P1, p. 40.

### Cloud backlog, AI products, and custom silicon

6. At 2026-03-31, Alphabet reported **$467.6 billion** of revenue backlog, of which **$462.3 billion** related to Google Cloud; just over half was expected to be recognized over the next 24 months.
   **Source:** GOOGL-P1, “Revenue Backlog,” p. 10.

7. Google Cloud Platform includes enterprise AI infrastructure, Vertex AI, Gemini Enterprise, cybersecurity, data, and analytics offerings.
   **Source:** GOOGL-P1, “Google Cloud,” p. 36.

8. Alphabet disclosed a limited number of agreements to supply TPU hardware for specialized high-scale on-premises infrastructure. It expected recognition to begin later in 2026, with most revenue in 2027.
   **Source:** GOOGL-P1, “Google Cloud,” p. 36.
   **Required label:** company contract disclosure and forward-looking recognition expectation.

9. Alphabet also disclosed that certain TPU agreements involved credit backstops supporting third-party data centers and power infrastructure.
   **Source:** GOOGL-P1, MD&A “Other Information,” p. 38.

### Capital intensity and liquidity

10. Q1 2026 operating cash flow was **$45.8 billion** and capital expenditures were **$35.7 billion**, primarily for technical infrastructure.
    **Source:** GOOGL-P1, executive overview, pp. 38–39.

11. Q1 capital expenditures increased from **$17.2 billion** in 2025 to **$35.7 billion** in 2026. Alphabet expected a significant 2026 increase in servers, network equipment, and data centers.
    **Source:** GOOGL-P1, “Capital Expenditures and Leases,” pp. 46–47.
    **Required label:** historical capex is fact; future investment is management expectation.

12. At 2026-03-31, cash, cash equivalents, and marketable securities totaled **$126.840 billion**.
    **Source:** GOOGL-P1, balance sheet / liquidity section, pp. 6 and 45.

13. Alphabet reported issuing senior unsecured notes for **$31.1 billion** of net proceeds in Q1 2026.
    **Source:** GOOGL-P1, MD&A “Other Information,” p. 38.

### Regulatory and legal evidence

14. Alphabet’s filing states that a final judgment was entered in December 2025 in the search-distribution case, including restrictions on distribution and requirements involving certain search data and syndication services. Alphabet appealed in January 2026; DOJ and states also appealed in February 2026.
    **Source:** GOOGL-P1, legal proceedings / contingencies, approximately pp. 25–28; corroborated by GOOGL-R1.

15. In the ad-tech case, the April 2025 liability decision and later remedies proceedings remained material; Alphabet stated that proposed structural remedies could materially affect the business and that it intended to appeal adverse rulings after final judgment.
    **Source:** GOOGL-P1, legal proceedings; corroborated by GOOGL-R2.
    **Required label:** litigation status and company assessment, not a forecast of outcome.

## 4.3 Claim limitations and disconfirming evidence

- Advertising remained the largest disclosed revenue source; do not present Cloud as having replaced the core advertising economics.
- The backlog is not realized revenue and depends on contract duration, performance, usage, and cancellations.
- Alphabet changed backlog reporting in Q1 2026 to include certain contracts of one year or less; approximately $7.3 billion of backlog reflected those contracts.
- TPU customer agreements and credit backstops create execution, infrastructure, financing, and counterparty exposure; do not describe custom silicon as pure upside.
- Other Bets remained loss-making in Q1 2026.
- Search and ad-tech remedies remain live legal risks.
- No directly inspected source here quantifies Alphabet’s market share in cloud or AI.
- Supplier exposure to NVDA, TSM, ASML, or other Portfolio-HQ holdings was not quantified in the filing.

---

# 5. Meta Platforms (META)

## 5.1 Primary sources directly inspected

### META-P1 — Meta FY2025 Form 10-K

- **Issuer:** Meta Platforms, Inc.
- **Document:** Form 10-K for year ended 2025-12-31
- **Accession:** `0001628280-26-003942`
- **Filed/accepted:** 2026-01-28
- **Official URL:** https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm
- **Primary-source status:** SEC-filed annual report
- **Sections/pages inspected:**
  - Business
  - Risk Factors
  - Properties
  - Legal Proceedings
  - MD&A
  - Segment profitability
  - Liquidity and capital resources
  - Commitments and contingencies
- **Inspector:** GPT-5.6 Thinking, this session

### META-P2 — Meta Q1 2026 Form 10-Q

- **Issuer:** Meta Platforms, Inc.
- **Document:** Form 10-Q for quarter ended 2026-03-31
- **Accession:** `0001628280-26-028526`
- **Filed:** 2026-04-29
- **Official URL:** https://www.sec.gov/Archives/edgar/data/1326801/000162828026028526/meta-20260331.htm
- **Primary-source status:** SEC-filed quarterly report
- **Sections/pages inspected:**
  - Financial Statements, pp. 6–13
  - Segment Information, pp. 23–24
  - Executive Overview, pp. 31–34
  - Revenue and Segment Profitability, pp. 40–44
  - Liquidity and Capital Resources, pp. 45–47
  - Commitments and Contingencies / Legal Proceedings
  - Risk Factors
- **Inspector:** GPT-5.6 Thinking, this session

### META-R1 — FTC appeal notice

- **Authority:** U.S. Federal Trade Commission
- **Document:** “FTC Appeals Ruling in Meta Monopolization Case”
- **Date:** 2026-01-20
- **Official URL:** https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-appeals-ruling-meta-monopolization-case
- **Primary-source status:** regulator statement
- **Sections inspected:** notice of appeal and FTC allegations
- **Inspector:** GPT-5.6 Thinking, this session

## 5.2 Verified factual extracts

### Revenue concentration and segment economics

1. Q1 2026 total revenue was **$56.311 billion**, up **33%** year over year, and operating income was **$22.872 billion**.
   **Source:** META-P2, executive overview and income statement, pp. 31 and 41.

2. Q1 2026 advertising revenue was **$55.024 billion**; Family of Apps total revenue was **$55.909 billion**.
   **Source:** META-P2, revenue table, p. 42.

3. Q1 2026 Family of Apps operating income was **$26.900 billion**. Reality Labs operating loss was **$4.028 billion**.
   **Source:** META-P2, segment profitability, pp. 23–24 and 44.

4. Q1 2026 ad impressions increased **19%** and average price per ad increased **12%** year over year.
   **Source:** META-P2, executive overview, p. 31.

5. Meta reported average Family daily active people of **3.56 billion** for March 2026, up **4%** year over year.
   **Source:** META-P2, Family of Apps metrics, p. 32.

6. FY2025 Family of Apps operating income was **$102.469 billion** and Reality Labs operating loss was **$19.193 billion**.
   **Source:** META-P1, MD&A “Segment profitability,” approximately pp. 74–76.

### AI investment and capital intensity

7. Q1 2026 capital expenditures, including principal payments on finance leases, were **$19.84 billion**.
   **Source:** META-P2, executive overview and liquidity section, pp. 32 and 45.

8. Meta anticipated approximately **$125 billion to $145 billion** of 2026 capital expenditures to support AI efforts and the core business. This is forward-looking guidance.
   **Source:** META-P2, liquidity and capital resources, p. 46.

9. Meta stated that its AI investment included third-party cloud capacity, servers, data centers, network infrastructure, generative AI, superintelligence, content recommendation, advertising tools, and product development.
   **Source:** META-P2, “Investment Philosophy,” pp. 33–34.

10. Q1 2026 R&D expense was **$17.699 billion**, up **46%** year over year, with the increase partly attributed to employee compensation and AI-related infrastructure.
    **Source:** META-P2, R&D discussion, p. 43.

11. At 2026-03-31, cash, cash equivalents, and marketable securities totaled **$81.18 billion**.
    **Source:** META-P2, executive overview and liquidity section, pp. 32 and 45.

### Business dependencies and disconfirming evidence

12. Meta’s filing identifies advertising as the dominant revenue source and says platform and regulatory changes can impair ad targeting and measurement.
    **Source:** META-P2, advertising trends and risk factors.

13. The filing states that Apple platform-policy changes have negatively affected ad targeting and measurement and may continue to affect marketer budgets.
    **Source:** META-P2, “Developments in Advertising,” approximately pp. 32–33.
    **Required label:** company-described historical and expected impact.

14. Reality Labs revenue declined **2%** in Q1 2026; lower Quest sales were partly offset by higher AI-glasses sales.
    **Source:** META-P2, Reality Labs revenue discussion, p. 42.

15. Meta expected full-year 2026 Reality Labs operating losses to remain similar to 2025. This is forward-looking management guidance.
    **Source:** META-P2, Investment Philosophy, p. 34.

16. Meta’s 2025 Form 10-K reports ownership of **30 data-center locations globally** and the use of some leased data centers.
    **Source:** META-P1, Item 2, “Properties,” approximately p. 50.

### Regulatory evidence

17. Meta states that the district court entered judgment in its favor in November 2025 in the FTC monopolization case and that the FTC filed a notice of appeal on 2026-01-20.
    **Source:** META-P2, legal proceedings; corroborated by META-R1.

18. The FTC continues to allege that Meta maintained a personal-social-networking monopoly through the Instagram and WhatsApp acquisitions. Treat this as the regulator’s allegation on appeal, not an adjudicated fact.
    **Source:** META-R1.

## 5.3 Claim limitations and disconfirming evidence

- Meta’s business remained heavily dependent on advertising.
- AI investment is not separately reported as a segment and does not establish standalone AI profitability.
- The 2026 capex range and Reality Labs loss outlook are forward-looking.
- Reality Labs remained materially loss-making.
- Third-party platform policies, privacy regulation, and access to training data are explicit dependencies.
- No directly inspected source in this audit establishes a quantitative moat, social-network market share, or the economics of Meta’s custom silicon.
- Do not assert MTIA deployment scale or performance without a separate official source.
- FTC allegations must remain clearly attributed to the FTC and distinguished from the district court judgment in Meta’s favor.

---

# 6. Amazon (AMZN)

## 6.1 Primary sources directly inspected

### AMZN-P1 — Amazon Q1 2026 Form 10-Q

- **Issuer:** Amazon.com, Inc.
- **Document:** Form 10-Q for quarter ended 2026-03-31
- **Accession:** `0001018724-26-000014`
- **Filed:** 2026-04-30
- **Official URL:** https://www.sec.gov/Archives/edgar/data/1018724/000101872426000014/amzn-20260331.htm
- **Primary-source status:** SEC-filed quarterly report
- **Sections/pages inspected:**
  - Financial Statements, pp. 3–6
  - Investments and strategic arrangements, pp. 11–13
  - Debt, pp. 16–17
  - Segment Information, pp. 21–22
  - MD&A, pp. 25–34
  - Liquidity and Capital Resources
  - Legal Proceedings and Risk Factors, pp. 36–48
- **Inspector:** GPT-5.6 Thinking, this session

### AMZN-P2 — Amazon Q1 2026 earnings release

- **Issuer:** Amazon.com, Inc.
- **Document:** “Amazon.com Announces First Quarter Results”
- **Date:** 2026-04-29
- **Official SEC exhibit URL:** https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm
- **Related 8-K:** https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260429.htm
- **Primary-source status:** issuer earnings release filed as SEC exhibit
- **Sections inspected:** consolidated and segment results
- **Inspector:** GPT-5.6 Thinking, this session

### AMZN-R1 — FTC Amazon eCommerce case page

- **Authority:** U.S. Federal Trade Commission
- **Case:** Amazon.com, Inc. (Amazon eCommerce)
- **Matter numbers:** 1910129 and 1910130
- **Civil action:** 2:23-cv-01495
- **Official URL:** https://www.ftc.gov/legal-library/browse/cases-proceedings/1910129-1910130-amazoncom-inc-amazon-ecommerce
- **Primary-source status:** regulator case page and pleadings index
- **Sections inspected:** case summary, complaint history, court order history
- **Inspector:** GPT-5.6 Thinking, this session

### AMZN-R2 — European Commission cloud DMA preliminary position

- **Authority:** European Commission
- **Document:** preliminary position on AWS and Azure gatekeeper designation
- **Date:** 2026-06-25
- **Official URL:** https://digital-markets-act.ec.europa.eu/commission-reaches-preliminary-position-amazons-and-microsofts-market-leading-cloud-services-should-2026-06-25_en
- **Primary-source status:** regulator statement; preliminary
- **Inspector:** GPT-5.6 Thinking, this session

## 6.2 Verified factual extracts

### Diversified revenue model and segment economics

1. Q1 2026 net sales were **$181.519 billion**, operating income **$23.852 billion**, and net income **$30.255 billion**.
   **Source:** AMZN-P1, financial statements and segment table, pp. 4 and 21–22.

2. Q1 2026 sales by major category included:
   - Online stores: **$64.254 billion**
   - Third-party seller services: **$41.578 billion**
   - Advertising services: **$17.243 billion**
   - Subscription services: **$13.427 billion**
   - AWS: **$37.587 billion**
   **Source:** AMZN-P1, net-sales-by-group table, p. 22.

3. Q1 2026 segment sales were:
   - North America: **$104.143 billion**
   - International: **$39.789 billion**
   - AWS: **$37.587 billion**
   **Source:** AMZN-P1, segment MD&A, p. 28.

4. Q1 2026 segment operating income was:
   - North America: **$8.267 billion**
   - International: **$1.424 billion**
   - AWS: **$14.161 billion**
   **Source:** AMZN-P1, segment information / MD&A, pp. 21 and 31.

5. AWS sales grew **28%** year over year; Amazon attributed the increase mainly to customer usage, partly offset by long-term-contract pricing changes.
   **Source:** AMZN-P1, p. 28.

### Capital intensity, liquidity, debt, and AI arrangements

6. Q1 2026 cash capital expenditures were **$43.2 billion**, compared with **$24.3 billion** in Q1 2025. Amazon said these primarily reflected technology infrastructure—mostly supporting AWS growth—and fulfillment capacity.
   **Source:** AMZN-P1, liquidity and capital resources, approximately p. 26.

7. Q1 2026 technology and infrastructure expense was **$29.567 billion**, up **29%** year over year.
   **Source:** AMZN-P1, operating-expense table, p. 29.

8. Amazon stated that technology and infrastructure spending was expected to increase as it added infrastructure and employees, including for AI and machine-learning initiatives. This is management expectation.
   **Source:** AMZN-P1, “Technology and Infrastructure,” pp. 29–30.

9. At 2026-03-31, total cash, cash equivalents, and marketable securities were **$143.089 billion**.
   **Source:** AMZN-P1, Financial Instruments note, p. 10.

10. At 2026-03-31, Amazon reported **$121.8 billion** of unsecured senior notes outstanding, including major U.S.-dollar and euro issuances in March 2026.
    **Source:** AMZN-P1, Debt note, pp. 16–17.

11. Amazon disclosed that AWS and OpenAI expanded an existing $38 billion commercial arrangement by **$100 billion over eight years**, including obligations related to AWS-chip performance.
    **Source:** AMZN-P1, commitments / subsequent events, p. 9.
    **Required label:** contractual company disclosure, not realized revenue.

12. Amazon invested **$15 billion** in OpenAI Series C preferred stock in Q1 2026 and entered a conditional commitment for an additional **$35 billion**.
    **Source:** AMZN-P1, Investments note, pp. 12–13.

13. Amazon disclosed a cloud and model collaboration with OpenAI that includes AWS cloud services and AWS chips.
    **Source:** AMZN-P1, Investments note, p. 13.

14. Amazon disclosed:
    - cumulative Anthropic investments through Q4 2025;
    - a subsequent **$5 billion** preferred-stock investment;
    - an amended AWS arrangement with AWS-chip performance obligations;
    - a potential financing facility of up to **$20 billion**;
    - an option for up to **$5 billion** of future equity investment.
    **Source:** AMZN-P1, Investments note, pp. 11–12.
    **Required label:** disclosed commitments and options; do not count all amounts as deployed capital.

### Regulatory evidence

15. The FTC and participating jurisdictions allege that Amazon uses interlocking practices to maintain monopoly power in online superstores and online marketplace services. These remain government allegations in active litigation, not adjudicated facts.
    **Source:** AMZN-R1.

16. Amazon’s 10-Q states that it is litigating matters involving monopolization and consumer-protection claims brought by state attorneys general and the FTC.
    **Source:** AMZN-P1, Risk Factors / legal proceedings, approximately p. 46.

17. The European Commission announced a **preliminary** view that AWS should be designated as a DMA gatekeeper for cloud services, citing gateway importance, entrenchment, switching costs, ecosystem breadth, and AI tools and partnerships.
    **Source:** AMZN-R2.
    **Required label:** preliminary regulator view.

## 6.3 Claim limitations and disconfirming evidence

- AWS is highly profitable, but Amazon’s consolidated economics also depend on retail, third-party marketplace services, advertising, subscriptions, and fulfillment.
- Capital spending and debt expanded materially; do not treat AWS growth as capital-light.
- OpenAI and Anthropic commitments create valuation, counterparty, concentration, delivery, financing, and chip-performance risks.
- Contract amounts are not equivalent to recognized revenue.
- The FTC case contains allegations, not final findings.
- The Commission’s cloud view is preliminary.
- Do not infer AWS market share from the inspected sources except where quoting and attributing the Commission’s preliminary assessment.
- Specific supplier shares or dependence on NVDA, TSM, ASML, or other holdings were not quantified.

---

# 7. Cross-company factual comparison enabled by the recovered evidence

The following comparisons are supported as factual synthesis or clearly labeled inference. They do not establish a ranking or policy recommendation.

## 7.1 Distinct primary economic engines

- **MSFT:** enterprise productivity, cloud infrastructure, developer tooling, security, gaming, search, and AI applications.
- **GOOGL:** search and digital advertising, YouTube, subscriptions/platforms/devices, cloud infrastructure and software, custom TPU supply, and Other Bets.
- **META:** advertising-funded social platforms, messaging/subscription adjacencies, Reality Labs hardware/software, and large AI infrastructure investment.
- **AMZN:** first-party retail, third-party marketplace services, fulfillment, advertising, subscriptions, AWS, and strategic AI investments.

## 7.2 Cloud and AI infrastructure

- MSFT, GOOGL, and AMZN disclose customer-facing cloud businesses.
- META’s disclosed AI infrastructure is primarily directed to its own products, advertising tools, models, wearables, and platform capabilities, although it also uses third-party cloud capacity.
- MSFT disclosed Maia/Cobalt and third-party accelerator use.
- GOOGL disclosed TPU supply agreements and infrastructure credit backstops.
- AMZN disclosed AWS-chip obligations in OpenAI and Anthropic arrangements.
- This audit did not establish equivalent primary evidence for META custom-silicon scale or economics.

## 7.3 Capital deployment

Historical/current disclosed capital expenditure measures are not perfectly comparable because definitions and periods differ:

- MSFT: $64.551 billion additions to property and equipment in fiscal 2025; $31.9 billion FY2026 Q3 capex.
- GOOGL: $35.7 billion Q1 2026 capex.
- META: $19.84 billion Q1 2026 capex including finance-lease principal.
- AMZN: $43.2 billion Q1 2026 cash capex.

Any comparison must retain those definitional differences and avoid treating the figures as directly interchangeable.

## 7.4 Regulatory exposure

- GOOGL faces active search-distribution and ad-tech remedies proceedings.
- META faces an FTC appeal in the personal-social-networking monopolization case.
- AMZN faces active FTC/state marketplace litigation.
- MSFT and AMZN are subject to the European Commission’s preliminary cloud-gatekeeper position.
- Regulatory claims, company descriptions, preliminary findings, final judgments, and appeals must be distinguished.

## 7.5 Shared and differentiated risk mechanisms

Supported shared mechanisms include:

- rapid infrastructure spending and depreciation;
- power, datacenter, server, networking, and advanced-chip availability;
- monetization lag relative to capex;
- AI talent and model-development costs;
- cloud/platform regulatory scrutiny;
- customer switching costs and ecosystem lock-in concerns;
- privacy and data-access constraints;
- contractual and investment exposure to AI labs;
- demand concentration around cloud and digital advertising.

Supported differentiated mechanisms include:

- MSFT’s enterprise productivity and OpenAI integration;
- GOOGL’s search-advertising concentration, TPU commercialization, and search/ad-tech remedies;
- META’s advertising concentration and Reality Labs losses;
- AMZN’s retail/fulfillment economics, AWS profitability, debt issuance, and large OpenAI/Anthropic commitments.

These are research inputs. They do not determine a preferred holding, tier, target, or trade.

---

# 8. Claim envelope for the implementing Claude session

## 8.1 Claims cleared for drafting

The implementation session may use the facts above for:

- business-model and segment descriptions;
- current revenue and operating-income composition;
- cash, liquidity, debt, repurchases, dividends, and capex;
- AI infrastructure and issuer-disclosed custom-silicon initiatives;
- issuer-disclosed partnerships and investment commitments;
- primary regulatory and litigation status;
- evidence-based risks and thesis-break conditions;
- cross-company overlap and dependency analysis;
- explicitly labeled inference about correlated capex, regulatory, and platform risks.

## 8.2 Claims not cleared without additional primary inspection

Do not make the following claims from this audit alone:

- precise market share in cloud, AI, advertising, or social networking;
- “monopoly,” “dominant,” “best,” “irreplaceable,” or similar conclusions except when explicitly attributed to a court or regulator;
- valuation conclusions;
- expected stock returns;
- specific supplier shares or customer-concentration percentages not disclosed;
- exact dependency on NVDA, TSM, ASML, AVGO, AMD, MRVL, or other Portfolio-HQ holdings;
- META custom-silicon deployment scale or unit economics;
- cross-company capex rankings without normalizing definitions;
- realized revenue from backlog or contract commitments;
- certainty about regulatory outcomes;
- any score, mechanical ranking, tier change, target change, or trade instruction.

## 8.3 Required fact labeling

The implementation must distinguish:

- **Filed fact:** audited or unaudited filing data.
- **Issuer statement:** management description or operational claim.
- **Forward-looking guidance:** expectation, target, or outlook.
- **Regulator allegation:** unresolved government claim.
- **Preliminary regulator finding:** not final.
- **Court judgment:** adjudicated result, subject to appeal where applicable.
- **Inference:** analytical connection drawn from multiple facts.
- **Uncertainty:** missing, disputed, or non-comparable information.
- **Judgment:** advisory assessment, with no policy authority.

---

# 9. Provenance and retention instructions

Recommended retained repository path for the implementing session, subject to repository convention and permitted scope:

`governance/audits/BATCH5_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260726.md`

The implementation session should preserve:

- this file unchanged;
- inspector identity: GPT-5.6 Thinking;
- inspection date: 2026-07-26;
- original source-readiness manifest and its checksum;
- exact source URLs;
- any additional directly inspected primary sources;
- a per-claim source reference in each Company Intelligence record;
- a disclosure that Claude Code did not itself directly inspect the blocked primary sources and relied on this retained, attributable recovery audit for those facts.

No claim in this audit should be represented as inspected by Claude Code.

---

# 10. Final determination

**The bounded evidence-recovery requirement is satisfied.**

Batch 5 drafting may resume for exactly MSFT, GOOGL, META, and AMZN, provided the implementation session:

- retains and attributes this audit;
- stays inside the claim envelope;
- performs no policy mutation;
- stops again for unsupported material claims;
- produces the later implementation PR and evidence bundle required by PI-0027 and OPS-0008.

EQIX remains deferred. No Batch 6, Milestone 4, OPS-0007 step I, allocator, margin, or trading authority is created.

**Evidence-recovery verdict: PASS FOR BOUNDED BATCH 5 DRAFTING.**
