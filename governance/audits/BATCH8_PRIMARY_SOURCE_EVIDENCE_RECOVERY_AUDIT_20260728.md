# Batch 8 Primary-Source Evidence Recovery Audit

**Repository:** `Mast3rkey/Portfolio-HQ`
**Workstream:** `WS-0005` Milestone 3, Batch 8
**Authority:** `PI-0030`, applying `OPS-0008` §2 and `OPS-0007` §1
**Companies:** International Business Machines (`IBM`), ServiceNow (`NOW`), Salesforce (`CRM`), Oracle (`ORCL`), CrowdStrike (`CRWD`), Palo Alto Networks (`PANW`)
**Recovery artifact:** `BATCH8_enterprise_software_cybersecurity_evidence_bundle_20260728_v1.yaml`, supplied by the principal, authored outside this repository by an independent primary-source evidence-recovery researcher
**Audit date:** 2026-07-28
**Purpose:** Retained, attributable record of primary-source evidence recovery after this Claude implementation session's own `WebFetch` access was confirmed blocked session-wide (HTTP 403 on SEC EDGAR, multiple issuer investor-relations domains, and a neutral non-target control domain, `en.wikipedia.org`), per `OPS-0008` §2's standing evidence-recovery pre-authorization.

## 1. Independence and authority boundary

The frozen evidence bundle's creator is disclosed in its own `artifact_metadata` as an "independent primary-source evidence-recovery researcher" — a role distinct from, and external to, this Claude Code implementation session, this session's own blocked gate report, and `PI-0030`'s authoring session. This audit exercises only the standing evidence-recovery authority in `OPS-0008` §2. It:

- recovers and inspects primary evidence (performed by the bundle's external author, not by this session);
- records claim-level provenance and access limitations;
- determines whether the `OPS-0008` §2 source-readiness gate can pass;
- supplies attributable evidence for this session's implementation of the six Company Intelligence records and the comparison artifact.

It does **not**:

- create Company Intelligence records itself (that is this session's own separate implementation work, performed after this audit and cited from it);
- change holdings, tiers, targets, roles, clusters, caps, weights, allocation, or margin policy;
- rank companies mechanically or declare a preferred holding;
- recommend or execute trades;
- authorize a seventh company, Batch 9, Milestone 4 beyond the batch's own required comparison, or `OPS-0007` §8 step I.

## 2. Independent verification of the frozen artifact (this session)

Before relying on the bundle, this session independently recomputed, from the raw uploaded bytes, and confirmed exact matches against the external `.sha256` manifest supplied alongside it:

| Check | External manifest | Independently recomputed | Match |
|---|---|---|---|
| SHA-256 | `4ee63b1f5eb8cfaf64d404fde6fd8cb52f806ebe091f7b911e4b871e48b2b61c` | `4ee63b1f5eb8cfaf64d404fde6fd8cb52f806ebe091f7b911e4b871e48b2b61c` | Yes |
| Lines (`LC_ALL=C.UTF-8 wc -l`) | 1612 | 1612 | Yes |
| Words (`wc -w`) | 8139 | 8139 | Yes |
| Bytes (`wc -c`) | 78577 | 78577 | Yes |

This session additionally parsed the YAML and independently confirmed, by direct enumeration (not by trusting the bundle's own self-description):

- Exactly **6** governed companies present in `authority_and_governed_boundaries.governed_scope` and in `company_evidence`: IBM, NOW, CRM, ORCL, CRWD, PANW — no seventh company, no EQIX, no UNH.
- Exactly **19** unique `source_id` values in `source_manifest` (IBM: 3, NOW: 3, CRM: 3, ORCL: 3, CRWD: 4, PANW: 3), matching `source_readiness.total_directly_inspected_primary_source_count: 19`.
- Exactly **38** unique `claim_id` values in `claim_level_evidence` (30 per-company claims, 5 each × 6 companies, plus 8 batch-level `BATCH-C1`–`BATCH-C8` claims).
- **Every** claim's `source_ids` resolves to an existing `source_id` in `source_manifest` — zero unresolved references, checked programmatically across all 38 claims.
- **Every** claim's `exact_locators` list and every source's `precise_locators` list is non-empty — checked programmatically, zero empty lists.
- **Every** one of the six companies has a non-empty `disconfirming_evidence_summary` and exactly 3 `thesis_break_conditions` in `company_evidence` — checked programmatically.
- **No** forbidden score, ranking, or preferred-holding declaration — the only occurrences of "preferred holding" and "ranking" in the full text are negation/prohibition statements (`implementation_handoff.facts_not_to_assert`, `batch_comparison_evidence.required_cautions`, `scope_and_policy_compliance_checks`), confirmed by direct text inspection of every match, not merely by trusting the bundle's own `scope_and_policy_compliance_checks` block.
- **No** embedded final digest or measurements inside the YAML itself (`artifact_metadata.self_digest_or_final_measurements_embedded: false`, confirmed true by inspection — the hash/line/word/byte figures live only in the external `.sha256` manifest).

**Known, disclosed, non-blocking artifact characteristic — reverse-index reciprocity.** This session independently checked full bidirectional reciprocity between each claim's `source_ids` and each cited source's own `claims_supported` list. **26 one-directional gaps were found** (e.g. `IBM-C5` cites `IBM-S1` in its `source_ids`, but `IBM-S1`'s own `claims_supported` list does not include `IBM-C5`; several `BATCH-C*` claims cite per-company sources whose `claims_supported` lists were not backfilled with the batch-level claim ID). No case of the reverse — a source's `claims_supported` naming a claim that does not itself cite that source back — was found. This is exactly the artifact characteristic the implementing instructions disclosed in advance as non-blocking, with **claim-level `source_ids` controlling** or the two overlapping conventions this repository already uses for CRWD, and does not reproduce PANW's platformization claims verbatim provenance. This audit does not repair the bundle's `claims_supported` index; every Company Intelligence record produced from this bundle cites its evidence from each claim's own `source_ids` and `exact_locators`, not from the source-side reverse index.

## 3. Source-readiness determination

**READY for the complete six-company batch**, per the bundle's own `source_readiness.full_batch_verdict` and this session's independent structural verification above. No subset implementation is used or permitted — `methodology.batch_scope_rule` ("All six companies must be ready; no subset implementation is permitted") is satisfied for all six.

## 4. Source-access manifest

All 19 sources below are SEC-filed primary documents or SEC-furnished issuer exhibits, reported by the bundle's author as directly opened and inspected (`direct_inspection_status: directly_inspected` on every entry) at `retrieval_timestamp_utc: 2026-07-28T10:04:58+00:00`, research cutoff **2026-07-28**. This Claude Code session did not itself independently re-open these URLs (its own `WebFetch` access to `sec.gov` and every tested company IR domain, and to a neutral control domain, was confirmed blocked) — attribution below is to the bundle's external author, consistent with the disclosure required in every resulting Company Intelligence record.

### 4.1 IBM

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| IBM-S1 | Form 10-K, year ended 2025-12-31 | Form 10-K | filed 2026-02-24 | 0000051143-26-000010 |
| IBM-S2 | Form 10-Q, quarter ended 2026-03-31 | Form 10-Q | filed 2026-04-23 | 0000051143-26-000038 |
| IBM-S3 | Arvind Krishna's Letter to IBM Investors — preliminary Q2 2026 results | Form 8-K Ex. 99.1 | furnished 2026-07-14 | 0000051143-26-000070 |

### 4.2 NOW

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| NOW-S1 | Form 10-K, year ended 2025-12-31 | Form 10-K | filed 2026-01-29 | 0001373715-26-000007 |
| NOW-S2 | Form 10-Q, quarter ended 2026-03-31 | Form 10-Q | filed 2026-04-23 | 0001373715-26-000056 |
| NOW-S3 | Q1 2026 earnings release | Form 8-K Ex. 99.1 | furnished 2026-04-22 | 0001373715-26-000054 |

### 4.3 CRM

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| CRM-S1 | Form 10-K, fiscal year ended 2026-01-31 | Form 10-K | filed 2026-03-02 | 0001108524-26-000060 |
| CRM-S2 | Form 10-Q, quarter ended 2026-04-30 | Form 10-Q | filed 2026-05-28 | 0001108524-26-000127 |
| CRM-S3 | Q1 FY2027 results | Form 8-K Item 2.02 / Ex. 99.1 | furnished 2026-05-27 | 0001108524-26-000125 |

### 4.4 ORCL

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| ORCL-S1 | Form 10-K, fiscal year ended 2026-05-31 | Form 10-K | filed 2026-06-26 | 0001193125-26-277521 |
| ORCL-S2 | Form 10-Q, quarter ended 2026-02-28 | Form 10-Q | filed 2026-03-11 | 0001193125-26-101045 |
| ORCL-S3 | Fiscal Q4 / full-year 2026 results | Form 8-K Item 2.02 / Ex. 99.1 | furnished 2026-06-10 | 0001193125-26-265848 |

### 4.5 CRWD

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| CRWD-S1 | Form 10-K, fiscal year ended 2026-01-31 | Form 10-K | filed 2026-03-05 | 0001535527-26-000010 |
| CRWD-S2 | Form 10-Q, quarter ended 2026-04-30 | Form 10-Q | filed 2026-06-04 | 0001535527-26-000025 |
| CRWD-S3 | Q1 FY2027 results | Form 8-K Item 2.02 / Ex. 99.1 | furnished 2026-06-03 | 0001535527-26-000022 |
| CRWD-S4 | July 19, 2024 Falcon sensor incident disclosure | Form 8-K Item 8.01 | filed 2024-07-22 | 0001104659-24-081571 |

### 4.6 PANW

| ID | Document | Type | Date / period | SEC accession |
|---|---|---|---|---|
| PANW-S1 | Form 10-K, fiscal year ended 2025-07-31 | Form 10-K | filed 2025-08-29 | 0001327567-25-000027 |
| PANW-S2 | Form 10-Q, quarter ended 2026-04-30 | Form 10-Q | filed 2026-06-03 | 0001327567-26-000015 |
| PANW-S3 | Fiscal Q3 2026 results | Form 8-K Item 2.02 / Ex. 99.1 | furnished 2026-06-02 | 0001327567-26-000012 |

Official SEC EDGAR URLs for all 19 sources are preserved verbatim in each company's own `intelligence/companies/<TICKER>.yaml` `sources[]` block, carried through from the bundle's `source_manifest`.

## 5. Recovered factual baseline per company

The following is a drafting baseline distilled from the bundle's `claim_level_evidence`, not a restatement of every claim verbatim (see each company's own Company Intelligence record for full claim-grounded prose) and not a complete investment conclusion.

### 5.1 IBM

**Filed facts.** Four segments (Software, Consulting, Infrastructure, Financing); hybrid-cloud/AI strategy stated alongside extensive named competition and open-source dependence (IBM-C1, IBM-C2). Preliminary Q2 2026 (furnished, not final): total revenue +1%, Software +5%, Consulting flat, Infrastructure -7% (IBM-C3). Buyback program suspended at the 2019 Red Hat closing; unused authorization remained as of the 2025 10-K, with dividends/debt management/acquisitions prioritized (IBM-C4).

**Disconfirming evidence / cautions.** Mixed preliminary segment execution; final Q2 10-Q not yet available at cutoff; segment mix conceals materially different economics; do not present IBM as a pure SaaS peer.

### 5.2 NOW

**Filed facts.** Unified workflow platform (ITSM/ITOM/security/CRM/creator) with Now Assist/AI agents embedded across modules (NOW-C1). 98% ACV-based renewal rate (2023–2025); year-end 2025 RPO $28.2B, 46% expected within 12 months (NOW-C2). Q1 2026: subscription revenue $3.671B, cRPO $12.64B, RPO $27.7B, >130% YoY growth in customers spending >$1M ACV on Now Assist (NOW-C3). Moveworks acquired for ~$2.4B with substantial goodwill/intangibles (NOW-C4).

**Disconfirming evidence / cautions.** Renewal metric is definition-limited and excludes several expansion/contraction effects; Now Assist total revenue/margin not separately disclosed; Moveworks integration and goodwill risk; do not compare 98% renewal directly with CRM attrition, CRWD retention, or PANW NGS ARR.

### 5.3 CRM

**Filed facts.** Platform integrates CRM applications with Slack, Data Cloud, MuleSoft, Tableau, and Agentforce (CRM-C1). FY2026 year-end RPO $72.4B, ~$2.2B tied to Informatica, explicitly not indicative of future revenue growth (CRM-C2). ~8% attrition rate at 2026-01-31, excluding Slack self-service and current-year acquisitions (CRM-C3). FY2026 repurchases ~$12.7B, dividends ~$1.6B, followed by a $25B accelerated share repurchase in March 2026 (CRM-C4).

**Disconfirming evidence / cautions.** Agentforce economics only partly disclosed; RPO acquisition- and timing-sensitive; attrition metric not directly comparable across issuers; large capital returns compete with acquisitions/debt reduction/reinvestment.

### 5.4 ORCL

**Filed facts.** Database licensing/support, enterprise applications, and OCI infrastructure combined; OCI buildout changes the historical asset-light profile (ORCL-C1). RPO $552.6B at 2026-02-28, ~12% expected within 12 months, driven by significant cloud contracts (ORCL-C2). First-nine-months fiscal 2026 capex $39.2B vs. $12.1B a year earlier, primarily data-center expansion, management expects the upward trend to continue (ORCL-C3). Financed with substantial senior-note issuance and mandatory convertible preferred stock while continuing dividends (ORCL-C4).

**Disconfirming evidence / cautions.** RPO is long-dated and contract-concentrated, not near-term revenue/profit/cash; capital expenditures and financing risk have risen sharply; do not compare Oracle RPO mechanically with shorter-duration RPO elsewhere in the batch.

### 5.5 CRWD

**Filed facts.** Cloud-native Falcon platform, common sensor, 32 modules at year-end/33 at filing (CRWD-C1). FY2026 year-end ARR ~$5.253B, +24%; ARR assumes expiring contracts renew on existing terms and can include active post-expiration renewal negotiations (CRWD-C2). July 19, 2024 Falcon sensor update caused Windows-system outages; later filings state harm to sales/reputation/partner relationships, customer commitment packages, longer sales cycles, and contraction (CRWD-C3). Company states it cannot estimate the loss range from outage-related proceedings and that insurance is not expected to cover all possible costs/claims/liabilities (CRWD-C4).

**Disconfirming evidence / cautions.** Outage-related concessions, sales delays, litigation, and uncertain liabilities challenge the otherwise strong ARR/platform narrative; do not quantify an ultimate liability; do not compare ARR directly with PANW's NGS ARR or any issuer's RPO.

### 5.6 PANW

**Filed facts.** Platformization strategy integrates network security, SASE, cloud security, and security operations (Cortex/XSIAM) to displace point products (PANW-C1). FY2025 year-end NGS ARR $5.6B, RPO $15.8B; NGS ARR expressly an operating metric, not GAAP revenue, with scope that can expand (PANW-C2). Mixed revenue recognition timing: product revenue at shipment/delivery, subscription/support over time (PANW-C3). Acquisition-led expansion creates contingent-consideration/integration risk; the IBM QRadar asset transaction produced a material contingent-liability estimate and a critical audit matter (PANW-C4).

**Disconfirming evidence / cautions.** Platformization can require sales concessions and complex integration; NGS ARR scope can expand, reducing comparability; do not present PANW as a pure subscription SaaS company; do not mechanically rank against CRWD.

## 6. Required batch comparison discipline (BATCH-C1 through BATCH-C8)

The bundle's batch-level claims establish, and this audit confirms are available for the comparison artifact: (1) shared enterprise IT/security budget exposure alongside real economic heterogeneity (IBM's consulting/infrastructure mix, ORCL's OCI buildout); (2) ARR/NGS ARR/RPO/cRPO/renewal/attrition are not definitionally interchangeable across the five recurring-metric issuers; (3) uneven AI-monetization disclosure across all six; (4) a wide capital-intensity range (ORCL's data-center buildout at one extreme, asset-light workflow/cybersecurity vendors at the other); (5) material acquisition dependence across the batch (Red Hat, Moveworks, Informatica, Cerner, PANW's product-expansion acquisitions); (6) CRWD/PANW as the batch's most direct overlap, with distinct architectures, incident histories, and metric definitions; (7) a common correlated-loss driver (enterprise technology budget pressure) plus AI-infrastructure cost, acquisition integration, and cyber/reputational events; (8) the evidence supports qualitative business-quality analysis, not a mechanical next-dollar ordering.

## 7. Evidence limitations and refresh triggers

**Current limitations (per-company, from `source_readiness.per_company.*.material_unresolved_questions`):** IBM's final Q2 2026 10-Q, watsonx revenue/margin/retention, zSystems cycle economics, and post-Q2 debt/pension position; NOW's direct Now Assist revenue/margin, post-Moveworks retention, seat-vs-module mix, and stock-comp/repurchase per-share offset; CRM's Agentforce standalone economics, Informatica integration/ROI, product-level retention, and final ASR share count/price; ORCL's customer concentration within large cloud contracts, OCI capacity/unit economics, Cerner integration economics, and post-year-end financing/capex commitments; CRWD's ultimate outage loss range/insurance recovery, post-outage renewal cohorts, government inquiry outcomes, and product-level win rates; PANW's current platformization concession economics, CRWD overlap/displacement evidence, acquisition-integration milestones, and any NGS ARR definition change.

**Mandatory refresh triggers** (evidence-driven, no universal cadence, per company, carried into each `freshness_registry.yaml`/`freshness_checkpoints.yaml` enrollment row and each record's own review cadence): final quarterly/annual filings superseding a preliminary or interim source; material AI-monetization disclosure; material acquisition, debt, or capital-return update; for CRWD/PANW specifically, any material legal settlement, inquiry outcome, or cybersecurity incident; any material RPO/ARR/NGS ARR definitional change.

## 8. Source-readiness conclusion

**READY.** This session's own implementation may resume Batch 8 using this audit, and the frozen evidence bundle it synthesizes, as retained, attributable primary-source-recovery evidence under `OPS-0008` §2.

Conditions:

1. This audit is retained under the repository's established `governance/audits/` convention.
2. This Claude Code session's own blocked `WebFetch` attempts are never represented as successful direct inspection — every fact is attributed to the bundle's external author.
3. The bundle's `claims_supported` reverse-index non-reciprocity (§2 above) is disclosed wherever cited, with claim-level `source_ids` controlling.
4. Every Company Intelligence record preserves the source dates, definitional limitations, and disconfirming evidence recorded here and in the underlying bundle.
5. This implementation PR is submitted as a draft, gated on its own separate independent exact-head review, principal acceptance, merge, and post-merge verification — none of which this audit itself performs or grants.

**No portfolio-policy, tier, target, cluster, cap, holdings, allocator, margin, or trading authority is created by this audit.**
