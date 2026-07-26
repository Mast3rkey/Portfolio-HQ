# PR #166 Primary-Source Audit

**Reviewer:** GPT-5.6 Thinking  
**Review type:** independent primary-source recovery audit  
**PR:** #166  
**Base:** `92ea06705b1707d8b7644e311e4f086f462e9573`  
**Audited head:** `246fa1c8f4436608640b4a3dfbac58393e209b65`  
**Evidence bundle SHA-256:** `0fddf2eadd6e15ed25c3e34b8f64337e0550473c001faf2bc740bf7ce8c4f44b`  
**Verdict:** **CHANGES REQUIRED**

## Independence and method

GPT-5.6 Thinking did not author or edit PR #166. The audit used the complete exact-head evidence bundle prepared by the implementation session and independently inspected official issuer and SEC materials that the Claude environment could not access.

The implementation session remained access-blocked. Any corrected repository provenance must say that primary sources were **independently inspected during this external GPT audit**, not that Claude opened them.

## Controlling process finding

### C1 — Blocking — PI-0026 primary-evidence stop condition was not followed

The implementation continued to completed Company Intelligence records, Medium conviction ratings, a comparison artifact, freshness enrollment, commits, and draft PR creation after determining that no primary source could be opened. PI-0026 required the implementation to try reasonable official alternatives and then stop and return for explicit principal direction if sufficient primary evidence remained unavailable.

The draft is therefore not review-ready at the audited head. The defect can be recovered without changing the authorized ticker scope if the principal explicitly authorizes the independently inspected GPT primary-source audit as the bounded evidence-recovery method.

## Company findings

### M1 — Major — ETN contains stale and unresolved claims that official sources resolve

Required corrections:

1. **Boyd Thermal close date**
   - Current draft: treats the close date as unresolved.
   - Official source: Eaton announced completion on **March 12, 2026**.
   - Replace every unresolved-close-date statement in ETN YAML, ETN Markdown, comparison, catalysts, risks, conviction rationale, and unresolved-items sections.

2. **Mobility transaction**
   - Current draft: describes a planned standalone Mobility Group spin-off.
   - Official source dated June 11, 2026: Eaton entered a definitive Reverse Morris Trust agreement to combine Mobility Group with Dana. The transaction values Mobility Group at approximately $5.1 billion, provides Eaton an approximately $1.1 billion cash distribution, leaves Eaton shareholders owning at least 50.1% of the combined company, and is expected to close in Q1 2027.
   - Replace stale standalone-spin framing with the current definitive transaction and its actual execution risks.

3. **Q1 2026 financials**
   - Official release supports sales of $7.5 billion, adjusted EPS of $2.81, segment margin of 22.7%, Electrical-sector backlog growth of 48%, and FY2026 guidance of 9–11% organic growth, 24.1–24.5% segment margin, and adjusted EPS of $13.05–$13.50.
   - Cite the exact official release rather than a generic newsroom URL.

4. **Claims not located in the inspected official release**
   - The 240% data-center-order growth, 32 GW, 228 GW, and “12 years of backlog” statements require an exact official presentation or call source.
   - Until that source is inspected, retain only with explicit secondary/management-commentary classification or remove them from decision-bearing conviction and comparison language.

Official sources inspected:

- Eaton Q1 2026 results:  
  https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html
- Boyd Thermal completion:  
  https://www.eaton.com/sg/en-us/company/news-insights/news-releases/2026/eaton-completes-acquisition-of-leading-liquid-cooling-solutions-provider-boyd-thermal.html
- Eaton Mobility Group / Dana definitive transaction:  
  https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-mobility-group-enters-agreement-to-combine-with-dana.html

### M2 — Major — VRT leverage and financial-evidence statements are materially wrong or unnecessarily unresolved

Required corrections:

1. **Net leverage**
   - Current draft: repeatedly states approximately 0.8x–1.0x “currently.”
   - Official Q1 2026 release: net leverage was approximately **0.2x** at quarter-end.
   - Correct VRT YAML, Markdown, conviction rationale, comparison, and margin-relevant evidence.

2. **Product/service mix**
   - Current draft: calls the approximately 81%/19% split a single unverified secondary estimate.
   - Official Q1 2026 Form 10-Q reports $2,091.2 million product sales and $558.3 million services-and-spares sales, approximately 78.9%/21.1%.
   - Replace the secondary estimate with the filing figures and classification.

3. **Gross margin**
   - Current draft: says no gross-margin figure was found.
   - Official Q1 Form 10-Q reports $999.7 million gross profit on $2,649.5 million net sales, approximately **37.7%**.
   - Remove the “not found” gap and use the primary figure.

4. **Backlog discrepancy**
   - Current draft makes a $15.0 billion-to-$12.45 billion backlog decline a central moderate risk, catalyst, thesis-break condition, comparison finding, and conviction limiter.
   - The inspected official Q1 release and Form 10-Q did not substantiate the $12.45 billion claim. The official Q4 release supports strong orders and approximately 0.5x net leverage but the audited materials did not establish the alleged Q1 backlog figure.
   - Remove this as a settled company-reported discrepancy unless an exact official document and passage are identified and inspected. It may remain only as a clearly labeled unresolved secondary claim with no decision-bearing weight.

5. **Guidance**
   - Reconcile the official Q1 2026 full-year adjusted operating-margin guidance to **22.8%–23.8%**, rather than preserving an unresolved secondary-source conflict.

Official sources inspected:

- Vertiv Q1 2026 results:  
  https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx
- Vertiv Q1 2026 Form 10-Q:  
  https://www.sec.gov/Archives/edgar/data/1674101/000162828026026556/vrt-20260331.htm
- Vertiv Q4/FY2025 results:  
  https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/
- Vertiv refinancing and ratings:  
  https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Completion-of-2-1-Billion-Senior-Unsecured-Bond-Offering-and-2-5-Billion-Senior-Unsecured-Revolving-Credit-Facility/

### M3 — Major — PWR’s business model and current disclosure are misstated

Required corrections:

1. **Manufacturing**
   - Current draft says PWR “does not manufacture equipment at all.”
   - Official 2025 Form 10-K states Quanta manufactures power transformers and related electrical components and owns manufacturing facilities associated with those businesses.
   - Reframe PWR as **primarily a labor-intensive infrastructure-services contractor with a growing, still-secondary manufacturing capability**.
   - Correct the company record and every comparison statement that relies on a services-only characterization.

2. **Employees**
   - Current draft reports 51,306 employees and unresolved estimates.
   - Official 2025 Form 10-K: approximately **69,500 employees** at December 31, 2025.

3. **Collective bargaining**
   - Current draft says no union-membership percentage was found.
   - Official 2025 Form 10-K: approximately **36%** of employees were covered by collective-bargaining agreements.

4. **Customer concentration**
   - Current draft treats FY2023 figures of 6% largest customer / 31% top ten as the latest available.
   - Official 2025 Form 10-K: largest customer **8%**, ten largest customers **30%** of consolidated revenue.
   - The same filing gives directional customer mix of 70% Utility and Power, 17% Energy and Other, and 13% Technology, Manufacturing and Communications.

5. **Legacy legal matters**
   - Maurepas and PRONATEL were not located in the inspected 2025 Form 10-K.
   - Do not treat omission alone as proof of resolution, but remove them from current conviction/risk weighting unless a current exact primary source establishes continuing materiality. They may be retained only as historical matters with present status unresolved and no current decision-bearing weight.

6. **Q1 2026**
   - Official release supports $7.87 billion revenue, adjusted EPS $2.68, adjusted EBITDA $686.4 million, RPO $26.2 billion, and backlog $48.5 billion.

Official sources inspected:

- Quanta 2025 Form 10-K:  
  https://www.sec.gov/Archives/edgar/data/1050915/000105091526000006/pwr-20251231.htm
- Quanta Q1 2026 results:  
  https://investors.quantaservices.com/news-events/press-releases/detail/396/quanta-services-reports-first-quarter-2026-results

### M4 — Major — The comparison artifact inherits material company errors

The comparison must be updated wherever it:

- characterizes PWR as having no manufacturing activity;
- uses the unsupported VRT $15.0B-to-$12.45B backlog claim as the batch’s “most specific evidence gap”;
- uses VRT’s wrong 0.8x–1.0x current leverage;
- treats ETN Boyd timing as unresolved;
- describes the Mobility transaction as a simple standalone spin;
- draws conviction, correlation, diversification, or margin-risk conclusions from those incorrect premises.

The high-level conclusion that the companies occupy distinct positions may remain only after the corrected factual foundation is re-read and the comparison is revised. No cluster, cap, tier, target, or capital-priority conclusion is authorized.

## Provenance and lifecycle findings

### m1 — Minor — PR body is stale

The PR body says 9 files and 1,834 insertions with zero deletions. The exact-head cumulative state is 10 files, 1,911 insertions, and 5 deletions. Update the PR body after the bounded correction.

### m2 — Minor — External-audit provenance must be explicit

Every corrected record and WORKSTREAMS statement must preserve this split:

- Claude implementation session: access-blocked; did not inspect the primary documents.
- GPT-5.6 Thinking external audit: independently inspected the named official sources.
- Correction author: revised repository content from the retained audit; must not claim personal inspection unless it actually performed it.

Do not replace the original access disclosure with a false statement that Claude opened primary materials.

## Scope that remains acceptable

No issue was found with:

- authorized company set: ETN, VRT, PWR;
- GEV remaining comparison-only and untouched;
- freshness rows being monitoring-disabled and pending;
- no changes to holdings, targets, allocator, margin policy, or trade execution;
- PR remaining draft and unmerged;
- exact-head CI and the 1,502-test result for the audited head.

These points do not cure the research-evidence and factual errors above.

## Required recovery sequence

1. Principal explicitly authorizes use of this independently inspected GPT audit as the bounded evidence-recovery method under PI-0026.
2. The current PR #166 implementation session applies one bounded correction pass on the same branch.
3. Correct only the three records, comparison, source ledgers, WORKSTREAMS factual provenance, and PR body as required.
4. Re-run validators, 1,502-test suite, `git diff --check`, protected-path checks, and exact-head CI.
5. Keep PR draft and unmerged.
6. Collect a fresh exact-head delta evidence bundle in a new independent session.
7. GPT-5.6 Thinking performs the final exact-head review.

No Batch 5, Milestone 4, allocation package, margin work, policy change, readiness transition, or merge is authorized by this audit.
