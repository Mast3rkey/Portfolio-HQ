# CVX Primary-Source Evidence Recovery Audit

**Repository:** `Mast3rkey/Portfolio-HQ`
**Workstream:** `WS-0005` Milestone 3, Batch 9
**Authority:** `PI-0031`, applying `OPS-0008` §2 and `OPS-0007` §1
**Company:** Chevron Corporation (`CVX`) -- CVX only; `XOM` (the `oil` cluster's other member) is existing comparison context only and is not modified by this batch
**Recovery artifact:** `CVX_PRIMARY_SOURCE_EVIDENCE_RECOVERY_20260728_v3.yaml`, supplied by the principal, authored outside this repository by an independent primary-source evidence-recovery researcher via a web-enabled research backend
**Audit date:** 2026-07-28
**Purpose:** Retained, attributable record of primary-source evidence recovery after this Claude implementation session's own `WebFetch` access was confirmed blocked session-wide (HTTP 403 on SEC EDGAR, a Chevron investor-relations URL, and two neutral non-target control domains, `example.com` and `google.com`), per `OPS-0008` §2's standing evidence-recovery pre-authorization.

## 1. Independence and authority boundary

The frozen evidence bundle's creator is disclosed in its own `bundle_metadata.retrieval_disclosure` as inspecting "official SEC and Chevron pages... through ChatGPT's hosted web research backend" -- a role distinct from, and external to, this Claude Code implementation session, this session's own prior blocked-gate report, and `PI-0031`'s authoring session. This audit exercises only the standing evidence-recovery authority in `OPS-0008` §2. It:

- recovers and inspects primary evidence (performed by the bundle's external author, not by this session);
- records claim-level provenance and access limitations;
- determines whether the `OPS-0008` §2 source-readiness gate can pass;
- supplies attributable evidence for this session's implementation of the CVX Company Intelligence record and the bounded XOM/CVX comparison artifact.

It does **not**:

- create the CVX Company Intelligence record itself (that is this session's own separate implementation work, performed after this audit and cited from it);
- change holdings, tiers, targets, roles, clusters, caps, weights, allocation, or margin policy;
- rank CVX and XOM mechanically or declare a preferred holding;
- recommend or execute trades;
- modify XOM's existing record in any way;
- authorize a tenth Milestone 3 batch, Milestone 4 beyond this batch's own required comparison, or `OPS-0007` §8 step I.

## 2. Independent verification of the frozen artifact (this session)

Before relying on the bundle, this session independently recomputed, from the raw uploaded bytes, and confirmed exact matches against the externally supplied `.sha256` manifest:

| Check | External manifest | Independently recomputed | Match |
|---|---|---|---|
| SHA-256 | `8256231340142d35289a5336bc2162c575164fe1df3db39ee4ecb6a20fb75203` | `8256231340142d35289a5336bc2162c575164fe1df3db39ee4ecb6a20fb75203` | Yes |
| Lines | 758 | 758 | Yes |
| Words (Python whitespace split) | 3,765 | 3,765 | Yes |
| Bytes | 31,612 | 31,612 | Yes |

This session additionally parsed the YAML with `yaml.safe_load` and independently confirmed, by direct enumeration and programmatic reciprocity checking (not by trusting the bundle's own self-description):

- Exactly **7** unique `source_id` values in `source_manifest` (CVX-S1 through CVX-S7), matching the bundle's own `provenance_integrity.source_count: 7`.
- Exactly **39** unique `claim_id` values in `claims` (CVX-C01 through CVX-C39), matching `provenance_integrity.claim_count: 39`.
- Exactly **53** unique claim-declared `(claim_id, source_id)` pairs, and **53** unique source-declared `(claim_id, source_id)` pairs from each source's own `claim_ids` list -- **the two sets are identical (symmetric difference empty in both directions)**, confirming full reciprocity, not merely the one-directional check the bundle's own `provenance_integrity` block reports.
- **Zero** orphan sources (every source is cited by at least one claim) and **zero** claims with empty `source_ids` -- checked programmatically.
- **Every** claim's `locators` list and every source's `locators` list is non-empty -- checked programmatically, zero empty lists.
- **Every** source is marked `directly_inspected: true` -- checked programmatically, zero exceptions.
- **Zero** duplicate `claim_id` or `source_id` values -- checked programmatically.
- **No** forbidden score, ranking, or preferred-holding declaration: `rank`/`score`-family substrings appear exactly 4 times in the full text, and every occurrence is a negation/prohibition statement (`bundle_metadata.research_boundary`; `claims[].qualification` for `CVX-C37`, explicitly stating the bundle "does not rank" CVX and XOM; `prohibited_conclusions`) -- confirmed by direct text inspection of every match, not merely by trusting the bundle's own `prohibited_conclusions` block.
- Claim `fact_inference_judgment` distribution: 35 `fact`, 2 `inference`, 2 `judgment` -- the two `judgment`-labeled claims (`CVX-C35`, `CVX-C36`) are the bundle's two thesis-break candidates, and the two `inference`-labeled claims (`CVX-C34`, `CVX-C37`) are the disconfirming-evidence synthesis and the XOM/CVX comparison input -- consistent with the bundle's own category labels for those four claims, checked by direct inspection rather than assumed.

**Bounded correction from v2, independently confirmed.** The audit accompanying v3 states that `CVX-S4` (the Form 8-K furnishing the Q1 2026 earnings release under Item 2.02) was a real official source in v2 with no linked claim, and that v3 adds `CVX-C39`, a narrow filing-identity claim, to resolve the orphan. This session independently confirmed against the v3 file itself: `CVX-S4`'s `claim_ids` lists exactly `[CVX-C39]`, and `CVX-C39`'s `source_ids` lists exactly `[CVX-S4]` -- the correction is present, reciprocal, and narrow (filing-identity only: that the 8-K was furnished 2026-05-01 under Item 2.02/9.01, not a new financial, operating, or policy claim).

## 3. Source-readiness determination

**READY for the single-company CVX batch**, per the bundle's own `verdict: EVIDENCE BUNDLE READY FOR INDEPENDENT VALIDATION` and this session's independent structural verification above. This batch is a deliberate single-company wave under `OPS-0008` §1's smaller-wave exception (`PI-0031`), so no multi-company batch-scope rule applies -- only CVX's own readiness is at issue, and it is satisfied.

## 4. Source-access manifest

All 7 sources below are SEC-filed primary documents, an SEC-furnished issuer exhibit/current report, or Chevron's own official investor-relations page, reported by the bundle's author as directly opened and inspected (`directly_inspected: true` on every entry) through a hosted web research backend, research cutoff **2026-07-28**. This Claude Code session did not itself independently re-open these URLs (its own `WebFetch` access to `sec.gov`, a Chevron investor-relations URL, and two neutral control domains was confirmed blocked) -- attribution below is to the bundle's external author, consistent with the disclosure required in the resulting Company Intelligence record.

| ID | Document | Type | Filed / furnished | Reporting period | SEC accession |
|---|---|---|---|---|---|
| CVX-S1 | Form 10-K filing index | 10-K (index) | 2026-02-24 | 2025-12-31 | 0000093410-26-000078 |
| CVX-S2 | Form 10-K, official inline-XBRL document | 10-K | 2026-02-24 | 2025-12-31 | 0000093410-26-000078 |
| CVX-S3 | Form 10-Q | 10-Q | 2026-05-07 | 2026-03-31 | 0000093410-26-000113 |
| CVX-S4 | Form 8-K (Q1 2026 earnings, Item 2.02/9.01) | 8-K | 2026-05-01 | 2026-05-01 | 0000093410-26-000110 |
| CVX-S5 | Q1 2026 earnings release, Exhibit 99.1 | 8-K Ex. 99.1 | 2026-05-01 | 2026-03-31 | 0000093410-26-000110 |
| CVX-S6 | Form 8-K, Q1 2026 pre-announcement guidance update | 8-K | 2026-04-09 | 2026-04-09 | 0000093410-26-000108 |
| CVX-S7 | Official Chevron investor-relations page | IR page | n/a (inspected as of cutoff) | 2026-07-28 cutoff | n/a |

Official SEC EDGAR URLs (and the Chevron IR URL) for all 7 sources are preserved verbatim in `intelligence/companies/CVX.yaml`'s `sources[]` block, carried through from the bundle's `source_manifest`.

## 5. Recovered factual baseline

The following is a drafting baseline distilled from the bundle's `claims`, not a restatement of every claim verbatim (see `CVX.yaml`/`CVX.md` for full claim-grounded prose) and not a complete investment conclusion.

**Filed facts.** Two reportable segments (Upstream, Downstream) plus an All Other category (CVX-C02); earnings depend mostly on Upstream profitability (CVX-C03). FY2025: revenue $184.432B, net income attributable $12.299B (CVX-C05); operating cash flow $33.939B, capex $17.347B (CVX-C06); company-defined free cash flow $16.592B (CVX-C07); ROCE 6.6%, down from 10.1% in 2024 (CVX-C09); production 3.7 MMBOED (+12% YoY, largely Hess-driven) (CVX-C10); reserves ~10.591B BOE (+8% YoY) (CVX-C11). Hess acquisition closed 2025-07-18, ~$48B aggregate price, $8.8B assumed debt, 301.25M shares issued (CVX-C16); Hess's principal upstream operations were in the US, Guyana, and Malaysia, plus a ~38% Hess Midstream LP interest (CVX-C17); integration is a stated, unresolved risk (CVX-C18). Q1 2026: revenue $48.607B (CVX-C19); net income $2.293B, attributable $2.210B, adjusted (non-GAAP) $2.8B (CVX-C20/C21); operating cash flow $2.514B including a $4.625B working-capital use (CVX-C22); capex $4.063B, company-defined free cash flow **negative** $1.549B (CVX-C23); cash $5.323B, short-term debt $5.828B, long-term debt $39.600B, total debt $45.428B up from $40.758B at 2025-12-31 (CVX-C24); commercial paper $10.1B, $11.4B of near-term debt reclassified to long-term on stated refinancing intent/ability (CVX-C25); dividends $3.526B, repurchases $2.5B, $6.0B total shareholder distributions (CVX-C26); $75B repurchase authorization, $41.0B cumulative through Q1 2026 (CVX-C27); US/International Upstream $2.112B/$1.797B, US Downstream $196M, **International Downstream loss $1.013B** (CVX-C29/C30); Q2 2026 earnings call officially scheduled 2026-07-31 (CVX-C38).

**Disconfirming evidence / cautions (bundle's own synthesis, labeled `inference`/`judgment`, not `fact`).** Lower 2025 ROCE than 2024; negative Q1 2026 free cash flow; higher post-Hess debt; a large International Downstream loss in the same quarter Upstream was strong (CVX-C34). Two thesis-break candidates: sustained inability to cover capex and distributions from operating cash flow across a normalized period while debt keeps rising (CVX-C35); and failure to realize Hess-integration benefits while debt/capital intensity stay elevated and performance underdelivers (CVX-C36) -- both explicitly require persistence across a normalized period, not one working-capital-distorted quarter.

## 6. Required XOM/CVX comparison discipline

The bundle's `CVX-C37` (labeled `inference`) establishes the comparison input this batch requires: structural shared exposure to crude-oil, natural-gas, and refining cycles between XOM and CVX, with CVX-specific divergence drivers including Hess/Guyana integration, Tengiz/CPC exposure, Permian and Gulf of America growth, and International Downstream performance. The bundle explicitly qualifies that "the XOM side must be grounded in Portfolio-HQ's existing XOM record and sources" and that the bundle itself "does not rank the companies or prove price correlation" -- both constraints are carried into `intelligence/BATCH9_OIL_CLUSTER_COMPARISON.md` unchanged. **Gap disclosed, not resolved:** the bundle does not establish, and this audit does not assert, any specific relationship between Hess's acquired Guyana asset and XOM's own separately-disclosed Guyana operations (e.g., whether they are the same offshore block or field) -- this is recorded as an explicit unresolved cross-reference question in the comparison artifact, not asserted as fact from either party's currently cited sources.

## 7. Evidence limitations and refresh triggers

**Current limitations** (per `unresolved_evidence_gaps` CVX-G01 through CVX-G05): governed tier/target/role must come from repository truth, not this bundle (CVX-G01); the XOM side of the comparison must come from XOM's own existing record (CVX-G02); Q2 2026 results were unavailable at the 2026-07-28 cutoff (CVX-G03); the July 31 earnings release will precede, and is not a substitute for, the Q2 2026 Form 10-Q (CVX-G04); no CVX/XOM price correlation was computed (CVX-G05).

**Mandatory refresh trigger** (per `july_31_refresh_manifest`, carried into `CVX.yaml`'s `freshness`/review fields and `intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml`): the Q2 2026 earnings release and Form 10-Q, both required, neither substituting for the other, refreshing earnings, segment results, production, operating cash flow, capital expenditures, free cash flow, cash, debt, shareholder distributions, Hess integration, guidance, risks, disconfirming evidence, thesis-break conditions, and freshness metadata. The manifest's own `implementation_rule` -- that a refresh must not move an already-exact-head-approved reviewed head without a fresh review -- is carried forward unchanged into this record's review framework.

## 8. Source-readiness conclusion

**READY.** This session's own implementation may resume Batch 9 (CVX) using this audit, and the frozen evidence bundle it synthesizes, as retained, attributable primary-source-recovery evidence under `OPS-0008` §2.

Conditions:

1. This audit is retained under the repository's established `governance/audits/` convention.
2. This Claude Code session's own blocked `WebFetch` attempts are never represented as successful direct inspection -- every fact is attributed to the bundle's external author.
3. Every Company Intelligence and comparison-artifact claim preserves the source dates, definitional limitations (GAAP vs. adjusted, consolidated vs. attributable, operating cash flow vs. company-defined free cash flow, gross vs. net debt, quarterly vs. annual), and disconfirming evidence recorded here and in the underlying bundle.
4. This implementation PR is submitted as a draft, gated on its own separate independent exact-head review, principal acceptance, merge, and post-merge verification -- none of which this audit itself performs or grants.
5. XOM's existing Company Intelligence record is read only as comparison context and is not modified, refreshed, or reassessed by this batch under any circumstance.

**No portfolio-policy, tier, target, cluster, cap, holdings, allocator, margin, or trading authority is created by this audit.**
