# WS-0005 Milestone 4 — Relationship Evidence Inventory (REL-0001 §I Bounded Unit)

**Retained advisory audit artifact — implementation output, not an independent review.**

| Field | Value |
|---|---|
| Authority | `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md` §I; `operations/WORKSTREAMS.yaml` WS-0005, `rel0001-inventory-only-unit-active` gate |
| Author | This implementation session — **not** an independent reviewer. An independent review of this artifact and the accompanying PR is the pending next step. |
| Scope | Exactly REL-0001 §I items 1-8: `relationship_validator.py`, `test_relationship_validator.py`, exactly this one retained audit artifact, and this inventory itself — classification of already-existing evidence only, against the current 27-name canonical roster, with no new research and no relationship record. |
| Repository state audited | `origin/main` @ `cd95a8fd21793f5d2a2383f69d6907ea6788d251` (PR #237 merge commit — REL-0001 effective), verified clean, working tree clean |
| Mode | Read-only inventory and classification. No `holdings.yaml`, `targets.yaml`, `allocate.py`, `margin_state.py`, or Company/Theme Intelligence record modified. No `intelligence/relationships/*.yaml` or `.md` record created. No score, ranking, or correlation computed. |

---

## 0. Preflight summary (performed before this artifact was drafted)

- Fresh isolated clone established; repository identity confirmed `Mast3rkey/Portfolio-HQ`; authenticated GitHub identity confirmed `Mast3rkey`. `origin` fetched and pruned; `main` confirmed at `cd95a8fd21793f5d2a2383f69d6907ea6788d251`, working tree clean.
- PR #237 ("Freeze WS-0005 Milestone 4 relationship schema and authorize inventory audit") independently confirmed `MERGED`, merge commit `cd95a8fd21793f5d2a2383f69d6907ea6788d251` (the current `origin/main` tip), merged 2026-08-04T05:33:12Z; its post-merge `test` check confirmed `completed`/`success`.
- Zero open pull requests (`gh pr list --state open` returns empty). No branch or open PR overlaps `governance/audits/`, `relationship_validator.py`, `test_relationship_validator.py`, `operations/WORKSTREAMS.yaml`, or `CLAUDE.md`.
- `REL-0001` read in full: status `Accepted`, effective on `cd95a8f`'s merge. No decision filed after `REL-0001` in `governance/decisions.yaml` (`REL-0001` is the last of 66 indexed rows) supersedes or expands it. `governance/decisions/` (66 `.md` files, excluding `README.md`) and `governance/decisions.yaml` (66 rows) confirmed 1:1; `portfolio_hq.dashboard.decisions.build_catalog('.').issues == ()` confirmed this session.
- `intelligence/relationships/` confirmed absent from the repository, both before and after this unit's own work — no prior relationship record exists anywhere.
- Canonical roster independently re-derived from `targets.yaml`'s `destination:` list, `asset_class: equity` rows only: exactly 27 names. Gate/disposition split independently re-derived from `gates.yaml`: 6 gated (`SNPS`, `ICE`, `SPGI`, `WM`, `RKLB`, `TSLA`, all `status: cash_pending_clearance`, `authority: PHQ-2026-01`), 21 not gated. Matches REL-0001's own recorded facts exactly.
- The ten `intelligence/*COMPARISON*.md` artifacts, both Theme Intelligence records (`ai_infrastructure`, `life_sciences_tools_medtech`, 4 files), and `issuer_lookthrough.yaml` all independently confirmed present and — after this unit's work — byte-identical to their pre-unit state (this unit reads only; see §9 of the implementing PR's own validation for the diff confirmation).
- Full pytest baseline on a fresh checkout of `cd95a8f` (before this unit's own files were added): **2440 passed, 1 failed** — the sole failure, `test_portfolio_hq_dashboard.py::test_real_repository_model_builds`, asserts `provenance.repo_name == "Portfolio-HQ"`, a value the production code derives from the checkout directory's own basename (`portfolio_hq/dashboard/provenance.py`: `repo_name=repo_root.name`). This session's mandated workspace directory is named `portfolio-hq-ws0005`, not `Portfolio-HQ` — the failure is a pre-existing artifact of this session's required workspace naming, not of any repository content, and is independent of every file this unit touches. Not treated as a Stop condition; disclosed here as discovered, pre-existing, environment-caused, non-blocking.

No condition met the Phase 1 "Stop" bar — the merge, authority state, repository state, and roster all matched REL-0001's own recorded facts exactly. This unit proceeded.

---

## 1. Methodology

Per REL-0001 §H/§I(5)/§J, this inventory inspects and reuses, before any new research (none was performed): all ten `intelligence/*COMPARISON*.md` artifacts; both Theme Intelligence records; `issuer_lookthrough.yaml`; existing cluster/cap decisions and their retained correlation rationale (`semis`, `power_infra`, `oil`, plus the declined T1-AI-infra and enterprise-software cluster-cap scans, all in `CLAUDE.md`'s Decisions Log); `gates.yaml`'s six gate dispositions; and each covered canonical company's own Company Intelligence record where a comparison artifact's own text pointed there. Every source below was opened and read directly by this session — no claim in this inventory rests on an unopened source or an uninspected search snippet.

**Scope discipline (REL-0001 §J).** The first inventory is frozen to the current 27-name canonical equity roster. Several comparison artifacts' companies are **not** canonical (e.g. `AMAT`, `LRCX`, `AMD`, `MRVL`, `INTC`, `MU`, `SKHY`, `MA`, `JPM`, `ABBV`, `MRK`, `JNJ`, `GILD`, `IBM`, `NOW`, `CRM`, `ORCL`, `CRWD`, `CVX`, `XOM`, `WDC`, `VRT` — all retained/historical-advisory records per `PI-0035`). Evidence naming those tickers is read and reported below **only** where it establishes a relationship, gap, or explicit disclaimer touching a canonical-roster ticker; a non-canonical-to-non-canonical relationship (e.g. `CRWD`/`PANW` is canonical-to-non-canonical, in scope for `PANW`'s side; `MA`/`JPM` internal comparisons are out of scope entirely) is noted only where it materially affects a canonical name's own gap/coverage picture, per §J's own instruction not to silently drop discovered work.

**Classification discipline.** Every classification below states its own `evidence_classification` read (`observed`/`inferred`/`modeled`/`judgmental`), its `relationship_status` read (`current`/`historical`/`potential`/`hypothetical`), and a `decision_served` candidate from REL-0001 §F's closed vocabulary. Per REL-0001 §E, absence of a sourced relationship is reported as an evidentiary gap, never as evidence that no relationship exists. Per §G, no measured price correlation is used, computed, or cited as if it were structural evidence anywhere below — correlation figures already on record (`CLAUDE.md`'s cluster-cap scans) are cited only as portfolio-policy context, kept in their own paragraph, never merged into a relationship classification.

---

## 2. Canonical roster accounting — all 27 names

| # | Ticker | Gate status | Company Intelligence coverage | Comparison-artifact / theme source |
|---|---|---|---|---|
| 1 | NVDA | not gated | present (T1) | Batch1(cross-ref §16), Batch2 §5, Batch3, Batch5 §4, `ai_infrastructure` theme |
| 2 | TSM | not gated | present (T1) | Batch1 §5, Batch2 §5, Batch3 §5/§16, `ai_infrastructure` theme |
| 3 | ASML | not gated | present (T1) | Batch1, Batch2, Batch3 §16 |
| 4 | AVGO | not gated | present (T2) | Batch3 §5/§6/§9/§16, Batch5 §4 |
| 5 | KLAC | not gated | present (band) | Batch1, Batch2, Batch3 §16 |
| 6 | MSFT | not gated | present (T1) | Batch5, `ai_infrastructure` theme (capex evidence), CEG.md |
| 7 | GOOGL | not gated | present (T1) | Batch3 §6 (AVGO customer), Batch5 |
| 8 | AMZN | not gated | present (T2) | Batch3 §6 (MRVL customer, non-canon), Batch5 |
| 9 | META | not gated | present (T1) | Batch3 §6 (AVGO/AMD customer), Batch5 |
| 10 | PANW | not gated | present (band) | Batch8 (CRWD overlap, CRWD non-canon) |
| 11 | LLY | not gated | present (T1) | Batch7 |
| 12 | ISRG | not gated | present (T2) | `life_sciences_tools_medtech` theme |
| 13 | TMO | not gated | present (T2) | `life_sciences_tools_medtech` theme |
| 14 | V | not gated | present (T1) | Batch6 §1-§4 (MA/JPM comparison, both non-canon) |
| 15 | COST | not gated | present (T1) | none (no comparison artifact; no cross-reference found in any other record) |
| 16 | CEG | not gated | present (T2) | WDC_SANDISK (incidental only); own record's Microsoft PPA (§4 below) |
| 17 | ETN | not gated | present (band) | Batch4 |
| 18 | GEV | not gated | present (T1) | Batch4, Batch9 (incidental), `ai_infrastructure` theme |
| 19 | PWR | not gated | present (T2) | Batch4 |
| 20 | GNRC | not gated | present (band) | GNRC.md §13 (own record; no dedicated comparison artifact) |
| 21 | RTX | not gated | present (band) | RTX.md (own record; administrative GNRC pairing only, §7 below) |
| 22 | SNPS | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |
| 23 | ICE | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |
| 24 | SPGI | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |
| 25 | WM | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |
| 26 | RKLB | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |
| 27 | TSLA | **gated** (`cash_pending_clearance`) | absent | n/a — no record exists |

**21 not-gated + 6 gated = 27, all 27 accounted for.** Every gate/disposition above is transcribed verbatim from `gates.yaml`, unedited and unchanged by this artifact. No gated name's real-world reopening-trigger event was investigated (explicitly out of this unit's scope per REL-0001 §J) — each `next_gate` condition is reported below exactly as filed, with no assessment of whether it has since been satisfied.

**Gated-name disposition, verbatim `next_gate` text (unchanged by this artifact):**

| Ticker | `next_gate` |
|---|---|
| SNPS | "Review after September 30, 2026 Investor Day and a fresh normalized valuation model." |
| ICE | "Review official Q2 package and transaction financing/integration assumptions before initiation." |
| SPGI | "Review one clean post-spin quarter and normalized SPGI-versus-MSCI valuation, leverage, and growth comparison." |
| WM | "Retrieve and model the complete Q2 2026 earnings package and update valuation." |
| RKLB | "Require Q2 results plus a defined Neutron technical milestone before activation." |
| TSLA | "Activate only under the accepted milestone framework and a fresh valuation review." |

**All 6 gated names have zero relationship evidence of any kind**, by direct consequence of having no Company Intelligence record at all (confirmed: none of `SNPS`/`ICE`/`SPGI`/`WM`/`RKLB`/`TSLA` appears anywhere under `intelligence/companies/`). This is not a finding requiring action — it is the mechanical, expected consequence of their gated/uncovered status, reported per §J's "account for all 27 canonical names" instruction.

---

## 3. Sources inspected (§H reuse requirement)

- `intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` (ASML/AMAT/KLAC/LRCX; AMAT/LRCX non-canonical)
- `intelligence/BATCH2_MEMORY_COMPARISON.md` (MU/SKHY/WDC/SanDisk-adjacent; none canonical — read for its own §5 cross-references to NVDA/TSM/ASML/KLAC)
- `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` (AVGO/AMD/MRVL/INTC; AMD/MRVL/INTC non-canonical)
- `intelligence/BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md` (GEV/ETN/VRT/PWR; VRT non-canonical)
- `intelligence/BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` (MSFT/GOOGL/AMZN/META — all four canonical)
- `intelligence/BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md` (V/MA/JPM; MA/JPM non-canonical)
- `intelligence/BATCH7_BIOPHARMACEUTICALS_COMPARISON.md` (LLY/ABBV/MRK/JNJ/GILD; ABBV/MRK/JNJ/GILD non-canonical)
- `intelligence/BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` (IBM/NOW/CRM/ORCL/CRWD/PANW; only PANW canonical)
- `intelligence/BATCH9_OIL_CLUSTER_COMPARISON.md` (CVX/XOM; neither canonical — read for completeness, no canonical-pair evidence found)
- `intelligence/WDC_SANDISK_COMPARISON.md` (WDC/SanDisk; neither canonical — read for completeness, no canonical-pair evidence found)
- `intelligence/themes/ai_infrastructure.md`/`.yaml` (NVDA, GEV)
- `intelligence/themes/life_sciences_tools_medtech.md`/`.yaml` (ISRG, TMO; SYK/DHR deferred, non-canonical)
- `issuer_lookthrough.yaml` (AI/platform common-driver look-through membership)
- `targets.yaml` `caps:` section (`semis`/`power_infra`/`oil` cluster membership and cap percentages)
- `CLAUDE.md` Decisions Log: power_infra cap addition (0.560 avg correlation), T1 AI-infra cluster-cap decline (0.302/0.373 avg correlation), enterprise-software cluster-cap decline (0.650 avg correlation) — cited as portfolio-policy context only, never merged into a structural-relationship classification (REL-0001 §G)
- `gates.yaml` (6 gated names' verbatim disposition text)
- Individual Company Intelligence records cross-referenced by the above where their own text supplied a relationship claim not otherwise captured: `intelligence/companies/CEG.md`, `RTX.md`, `GNRC.md`, `V.md`

No `intelligence/relationships/` file exists to inspect (confirmed absent). No external web/company research of any kind was performed.

---

## 4. Existing evidence, classified by REL-0001 §C primitive type

Every entry below is evidence **already present** in the sources at §3 — this unit authored none of the underlying facts, only the classification against REL-0001's taxonomy. Both tickers named in each row are canonical unless marked "(non-canon)".

### 4.1 `manufacturing_dependency`

| Pair | Claim (paraphrased from source) | Source | Classification | Status |
|---|---|---|---|---|
| NVDA → TSM | NVDA is fabless; TSM record and industry-wide reporting place TSM as the dominant advanced-node manufacturing partner for NVDA-class fabless designers. No NVDA-specific named-percentage TSM dependence figure was located by Batch3's own research pass. | `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §5, §16 | inferred (structural inference from fabless status + industry concentration, not a company-specific disclosed %) | current |
| AVGO → TSM | Same structural inference as above, extended explicitly to AVGO by Batch3 §5: "AVGO, AMD, and MRVL all depend on external foundry capacity... TSMC as the dominant advanced-node/advanced-packaging supplier." No AVGO-specific named-percentage figure found. | `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §5 | inferred | current |

### 4.2 `capital_spending_dependency`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| ASML → TSM (fab capex class) | ASML's revenue is dependent on foundry/IDM (TSMC-class) capital-expenditure cycles for lithography equipment purchases — Batch1's own "shared semiconductor-capex drivers" finding, cross-referenced against Batch3 §16's explicit statement that "AVGO/AMD/MRVL fabless growth indirectly drives TSMC... capacity expansion, which in turn drives foundry purchases of ASML/AMAT/KLAC/LRCX equipment." | `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §5; `BATCH3...` §16 | inferred (batch-level structural mechanism; no ASML-TSM-specific dollar figure) | current |
| KLAC → TSM (fab capex class) | Same mechanism as ASML, per the same two sources — KLAC's equipment demand depends on the same foundry-capex class TSM anchors. | `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §5; `BATCH3...` §16 | inferred | current |
| GEV / ETN / PWR — shared capex dependency on hyperscaler/utility capex class | "All four share genuine, disclosed exposure to the AI-data-center-capex buildout... the transmission mechanism differs by company" — GEV's Power/Electrification, ETN's Electrical, and PWR's utility/grid work are each, by their own disclosed evidence, dependent on the same named hyperscaler-and-utility capex cycle (a "named class of companies," per REL-0001 §C.5's own definition). | `BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md` §9 | observed for the mechanism's existence (each company's own disclosed order/backlog growth figures), inferred for the shared-class framing | current |
| MSFT/GOOGL/AMZN/META (hyperscaler capex) → semis-cluster names (NVDA/AVGO) | **Explicitly unresolved gap, not established evidence** — see §5.1 below. Batch5's own text: "This batch's evidence base does **not** independently confirm or quantify any specific supplier relationship between any of MSFT/GOOGL/META/AMZN and any of those already-covered [semis] names... this remains a disclosed, unresolved evidence gap on both sides." | `BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` §4 | **not classified** — explicit gap, reported as such, not converted into an inferred claim (REL-0001 §E: absence of evidence is not evidence of relationship) | n/a |

### 4.3 `customer_dependency`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| AVGO → GOOGL | AVGO's AI-segment customer roster names Google (Alphabet/GOOGL) specifically among a small named group (Google, Meta, OpenAI, Anthropic, Apple), contributing to AVGO's disclosed ~40% top-5-customer concentration. | `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §6 | observed (named in AVGO's own disclosed customer roster) | current |
| AVGO → META | Same source, Meta named in the same AI-segment customer roster. | `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §6 | observed | current |
| **CEG → MSFT** | Constellation Energy (CEG) has a disclosed **20-year Power Purchase Agreement with Microsoft**, supporting the Crane Clean Energy Center nuclear-plant restart — a named, dollar-relevant, long-duration, primary-source-corroborated customer relationship. This is, by evidentiary strength, the single best-documented canonical-pair relationship found anywhere in this inventory. | `intelligence/companies/CEG.md` (own record, §"20-year Microsoft PPA... Crane Clean Energy Center restart") | **observed** (named counterparty, named contract structure, primary-source-referenced in CEG's own record) | current |

### 4.4 `regulatory_or_reimbursement_dependency`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| MSFT / AMZN | Both companies are named, specifically, in the **same** EU DMA cloud-gatekeeper preliminary regulatory matter (Azure and AWS both named; GOOGL/META do not appear in this specific proceeding per the batch's own evidence). This is a same-specific-regime match, not merely generic tech-sector regulatory exposure. | `BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` §6 | observed (both named in the same disclosed proceeding) | current |
| ISRG / TMO — **explicitly NOT established** | The `life_sciences_tools_medtech` theme record itself states these are "two distinct sub-industries linked by a shared secular driver, not one industry described two ways," and explicitly separates device-company reimbursement exposure (ISRG) from tools/diagnostics biopharma-funding-cycle exposure (TMO) as "not the same regulatory process." A `regulatory_or_reimbursement_dependency` classification between ISRG and TMO would **over-claim** what the source supports. | `intelligence/themes/life_sciences_tools_medtech.md`/`.yaml` | **abstained** — explicit source-level disclaimer against treating this as a shared-regime relationship | n/a |

### 4.5 `geographic_or_geopolitical_dependency`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| ASML / KLAC — **partial, not a full match** | Both carry material China/export-control exposure, but via **structurally different regimes**: ASML under Dutch/EU national licensing (EUV/DUV) plus a separate pending US legislative track; KLAC under the US BIS regime only. Batch1's own text: "the *regime* differs meaningfully... ASML is structurally distinct from the other three." A same-specific-regime claim (REL-0001 §C.9's own bar) is **not supported** between ASML and KLAC — only a shared general theme (China exposure), not a shared specific mechanism. | `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` §8 | **abstained** as a primitive `geographic_or_geopolitical_dependency` claim between this specific pair — the source itself draws the distinction this inventory preserves | n/a |
| AVGO — China export-control exposure (~20% of revenue) | Disclosed, quantified, but this batch's evidence does not name a second canonical-roster company sharing the identical regime/action — reported as a single-company data point, not a pair. | `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §9 | observed (single-company only; no in-scope pair to classify) | current |

### 4.6 `competitor`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| PANW / CRWD (non-canon) | "CrowdStrike and Palo Alto Networks are the batch's most directly overlapping pair... both are named in each other's own risk disclosures as direct competitors." Strong, named, primary-source-adjacent evidence — but CRWD is non-canonical (retained), so this pair is **out of the current inventory's scope** as a recordable primitive under §J, even though the evidence quality is the strongest `competitor` example found anywhere in the roster. Reported here as a disclosed gap: PANW has no *canonical-pair* competitor evidence. | `BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` §"Direct CRWD/PANW overlap" | observed (for the PANW/CRWD pair itself, out-of-scope for recording) | current |
| ETN / VRT (non-canon) | ETN and VRT are named, in their own records, as competitors to each other in overlapping data-center electrical/power-management categories. VRT is non-canonical — same out-of-scope treatment as PANW/CRWD above. | `BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md` §4 | observed (out-of-scope pair) | current |
| MSFT / GOOGL / AMZN (canonical) | "MSFT, GOOGL, and AMZN duplicate each other to a real degree as public-cloud sellers competing for the same enterprise AI-infrastructure spending — this is the batch's clearest overlap." All three are canonical roster names — this is the one canonical-to-canonical `competitor` match located in this inventory, a three-way mutual overlap from a single source, in-scope under §J (unlike the two non-canonical pairs above). | `BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` §7 ("Genuine diversification versus duplicated exposure") | inferred (the batch's own synthesized comparative assessment of overlapping public-cloud businesses, not a company's own named risk-disclosure statement of direct competition — a lower evidentiary tier than the PANW/CRWD entry above, which is itself out of scope) | current |

**Correction (this artifact's own retained-review bounded correction, see repository governance record):** an earlier version of this section stated "No canonical-to-canonical `competitor` pair was found anywhere in the ten comparison artifacts or any individual company record inspected." That statement was false — it overlooked the MSFT/GOOGL/AMZN row above, present in a source (`BATCH5...`) this artifact's own §3 methodology certifies as fully inspected. The corrected finding: exactly one canonical-to-canonical `competitor` match was located, per the row above; no *other* canonical-to-canonical `competitor` pair beyond MSFT/GOOGL/AMZN was found.

### 4.7 `complement`

| Pair | Claim | Source | Classification | Status |
|---|---|---|---|---|
| GNRC / (ETN, GEV, PWR) | GNRC's C&I segment now supplies large-megawatt backup generators, switchgear, and enclosures directly to hyperscale data-center operators under disclosed, dollar-quantified multi-year agreements. GNRC's own record states this is "a literal complementary line item in the same data-center power stack" alongside ETN (switchgear/power distribution), GEV (turbines/grid equipment), and PWR (EPC/interconnection) — a textual match to REL-0001 §C.12's `complement` definition (GNRC's product increases the completeness/viability of the same data-center power buildout ETN/GEV/PWR also serve). | `intelligence/companies/GNRC.md` §13 | inferred (the source's own framing is judgmental/synthesized from GNRC's disclosed contracts, not a single named joint claim between GNRC and any one of the three) | current, though GNRC's own record notes this data-center exposure is still a minority (~35% of FY2025 sales in C&I, and data centers are only the "core driver" within that ~35%, not its entirety) — a materiality caveat any future record would need to carry explicitly |

### 4.8 `supplier_dependency`, `technology_platform_dependency`, `commodity_or_energy_dependency`, `financing_or_interest_rate_dependency`, `substitute`

**No canonical-to-canonical evidence meeting REL-0001 §E's materiality/specificity bar was found for any of these five primitive types.** Specific gaps and near-misses, reported per §E's abstention discipline rather than forced into a classification:

- `supplier_dependency`: Batch1 explicitly found **no shared-supplier concentration** among its four companies (a disclosed research gap, not a finding of absence, per the source's own words) — no canonical pair qualifies.
- `technology_platform_dependency`: no canonical-pair claim located (Batch3's MSFT/GOOGL custom-silicon material is single-company, not a dependency *on* another canonical company's platform).
- `commodity_or_energy_dependency`: GEV/ETN/VRT/PWR's shared "copper/aluminum commodity exposure" is disclosed only in general market terms, "not company-quantified" (`BATCH4...` §10) — too generic to meet §E's materiality-as-gating-question bar as a named, specific commodity dependency between any two canonical names.
- `financing_or_interest_rate_dependency`: GEV/ETN/VRT/PWR's shared capex-financing rate sensitivity is disclosed only in general terms ("none of the four companies' own records discloses a company-specific quantified rate-sensitivity figure," `BATCH4...` §9) — REL-0001 §C.8 requires a dependency "beyond generic market-wide rate exposure"; this evidence does not clear that bar.
- `substitute`: no canonical-pair substitute claim located in any source inspected.

---

## 5. Cross-batch relationship gaps (REL-0001 §I item 7)

Evidence a comparison artifact already implies but no primitive record currently captures, and which no single existing artifact resolves on its own:

### 5.1 Hyperscaler-to-semis capital/customer chain (highest-value gap)

Batch3 (semis) and Batch5 (hyperscalers) each assume the other side would confirm a NVDA/AVGO ↔ MSFT/GOOGL/AMZN/META customer or capital-spending dependency — general industry knowledge makes this highly plausible, but **neither batch's own research independently verifies it from the counterparty side**. Batch5's own text states this explicitly: "this batch's own research does not resolve that cross-reference either... a disclosed, unresolved evidence gap on both sides." This is the single largest, best-identified, most decision-relevant gap in the current evidence base — it would plausibly serve `duplicate_exposure_detection` (T1's AI-infrastructure concentration, already flagged by `CLAUDE.md`'s own declined cluster-cap scan, runs through exactly this unconfirmed chain) and `stress_testing`.

### 5.2 CEG as an under-recognized AI-infrastructure-adjacent name

CEG's own Microsoft PPA (§4.3 above) is disclosed in CEG's individual record but is **not cross-referenced by the `ai_infrastructure` theme record**, which currently names only NVDA and GEV as members. CEG's power-supply relationship to the same hyperscaler AI-buildout theme is structurally comparable in kind (if not scale) to GEV's — a gap in the theme's own membership completeness, noted here as discovered work, not acted on (extending theme membership is outside this unit's scope and would itself require its own separate authorization under PI-0007's human-approval-gated theme-membership process).

### 5.3 GNRC's data-center pivot is undocumented anywhere except GNRC's own record

GNRC's 2025-2026 shift toward hyperscale data-center backup power (§4.7) is disclosed only in `GNRC.md` — it appears in no comparison artifact (Batch4 predates GNRC's coverage and was never amended) and is not cross-referenced from ETN's, GEV's, or PWR's own records. A future Batch4-adjacent reconciliation (not authorized by this unit) could close this gap.

### 5.4 issuer_lookthrough.yaml's AI/platform grouping is a different mechanism than any REL-0001 primitive

`issuer_lookthrough.yaml`'s 11-issuer "AI/platform common-driver" list (NVDA, MSFT, AMZN, GOOGL, AVGO, META, LLY, TSLA, AAPL, TSM, ASML) measures **ETF constituent-weight overlap** (ownership-structure duplication via `SPY`/`VWO`/`VEA`), not a structural business dependency between any two of those issuers. It is retained here as existing, authoritative infrastructure for a *different* question (effective-issuer concentration, `PHQ-2026-02`) — **not itself relationship evidence in REL-0001's sense**, and a future relationship record must not conflate the two mechanisms. Flagged per REL-0001 §I item 7/§H as a place where an existing artifact already provides the appropriate authoritative mechanism for its own (adjacent, non-relationship) question.

---

## 6. Canonical names with no meaningful cross-canonical relationship evidence

The following covered (not-gated) canonical names carry **no relationship evidence meeting REL-0001 §E's materiality bar with any other canonical-roster name**, based on the sources inspected — each has either no comparison artifact, or a comparison/individual-record explicitly disclaiming a shared mechanism with its nearest portfolio neighbor:

| Ticker | Why no canonical-pair evidence exists | Nearest evidenced relationship (out of scope or too weak) |
|---|---|---|
| COST | No comparison artifact; no cross-reference located in any other inspected record | none found |
| V | Batch6's only canonical member; MA/JPM (its comparison peers) are both non-canonical | V/MA competitor evidence exists but MA is non-canonical |
| PANW | Its strongest, best-evidenced relationship (CRWD, `competitor`) is non-canonical | PANW/CRWD, out of scope |
| LLY | Its shared regulatory/reimbursement drivers are with ABBV/MRK/JNJ/GILD, all non-canonical; its named competitor (Novo Nordisk) is not a portfolio holding at all | none in-roster |
| ISRG / TMO | Share theme membership, but the theme record itself explicitly disclaims a shared regulatory mechanism (§4.4) | abstained, see §4.4 |
| RTX | RTX's own record explicitly states "RTX and GNRC share no genuine economic mechanism" (§7 below) — the one other canonical name it was administratively researched alongside | GNRC pairing explicitly disclaimed |
| GNRC | Same explicit disclaimer from GNRC's own record, re: RTX; GNRC's real evidenced connection (§4.7) is to ETN/GEV/PWR, not RTX | RTX pairing explicitly disclaimed; ETN/GEV/PWR connection is `complement`/`inferred`, see §4.7 |

**KLAC** carries evidence but only under an abstained (not classified) `geographic_or_geopolitical_dependency` reading against ASML (§4.5) — its only clearly *established* canonical-pair evidence is the `capital_spending_dependency` reading in §4.2 (via TSM as the shared-class anchor).

---

## 7. Explicit conflicts / disconfirming statements found

- **RTX / GNRC**: both companies' own individual records state, in near-identical language, that they were "filed as an administrative pairing" for research-execution efficiency only, and that "RTX and GNRC share no genuine economic mechanism." This is retained negative evidence, not a gap — a future relationship record must not treat RTX/GNRC's shared research wave (`PI-0036`) as itself implying an economic relationship. No conflict between the two records; both agree.
- **ASML / KLAC China exposure**: no direct conflict, but a real risk of over-classification if read carelessly — Batch1's own text is explicit that the *regime* differs (Dutch/EU vs. US BIS), even though both companies share the general theme of China/export-control exposure. Reported in §4.5 as an abstention, not a conflict between sources.
- **ISRG / TMO shared theme, disclaimed shared regulatory mechanism**: not a conflict between two sources, but a single source (the theme record) actively working against a naive same-theme-implies-same-regulatory-mechanism reading. Reported in §4.4.
- No instance was found anywhere in the inspected sources of two different artifacts making factually inconsistent claims about the same canonical-pair relationship (the pre-existing `BTC` share-count inconsistency documented by the Milestones 1-2 audit and `FA-3` is unrelated to relationship evidence and is not re-litigated here).

---

## 8. Where existing infrastructure already provides the appropriate mechanism

- **`ai_infrastructure` and `life_sciences_tools_medtech` Theme Intelligence records** already serve as the authoritative narrative/evidence layer for their member companies' shared secular driver — a future relationship record for NVDA/GEV or ISRG/TMO should reference, not duplicate, the theme record's own evidence list.
- **`issuer_lookthrough.yaml`** already serves as the authoritative mechanism for ETF-embedded ownership-overlap questions (§5.4) — a future relationship record must not re-derive or restate this from a structural-dependency angle; it answers a different question (effective-issuer concentration), not a REL-0001 primitive-relationship question.
- **`targets.yaml`'s `caps:` cluster definitions and `CLAUDE.md`'s retained correlation-scan narrative** already serve as the authoritative mechanism for the *measured-price-correlation* side of REL-0001 §G's structural-versus-measured separation — a future relationship record's own `evidence` entries must cite these only as separate-provenance context, never merge them into a structural claim's own evidence classification.

---

## 9. First future relationship-content batch — advisory recommendation only

Per REL-0001 §I/§L and Phase 6 of this unit's own task authorization: **this section recommends, and does not authorize, select, implement, or begin, a future relationship-content batch.** Any future batch requires its own separate, explicit principal authorization before any `intelligence/relationships/*.yaml` record is created.

Based solely on the inventory above, the smallest coherent first candidate batch is:

| Candidate pair | Common mechanism | Existing evidence available | Missing evidence | Likely `decision_served` | External research required? | Shared-file risk | Stopping condition |
|---|---|---|---|---|---|---|---|
| `CEG_MSFT` | `customer_dependency` — 20-year nuclear PPA | CEG's own record fully documents the PPA, counterparty, and asset (Crane Clean Energy Center) | Contract dollar value/percent-of-CEG-revenue not located in the existing record; MSFT's own record does not independently confirm the PPA from its side | `thesis_monitoring`, `stress_testing` | Possibly none — CEG's existing sourcing may be sufficient; MSFT-side confirmation would strengthen but is not certain to be required | Neither company's existing Intelligence record would need editing — a relationship record is additive only | If MSFT-side confirmation cannot be found without new primary-source research beyond what CEG.md already cites, the record should carry `evidence_classification: inferred` from CEG's side only and disclose the one-sided sourcing explicitly, not silently upgrade to `observed` |
| `AVGO_GOOGL` and `AVGO_META` | `customer_dependency` — named AI-segment customer roster | AVGO's own disclosed top-5-customer concentration and named roster (Batch3 §6) | GOOGL's/META's own records do not independently confirm AVGO as a supplier from their side (neither currently discloses semiconductor-supplier-level detail) | `duplicate_exposure_detection`, `thesis_monitoring` | Likely none beyond what Batch3 already cites, unless one-sided sourcing is judged insufficient | Additive only | Same one-sided-sourcing disclosure discipline as CEG_MSFT |
| `GNRC_GEV`, `GNRC_ETN`, `GNRC_PWR` | `complement` — same data-center power stack | GNRC's own record's §13 analysis (dollar-quantified C&I contracts, Enercon acquisition rationale) | ETN/GEV/PWR's own records do not cross-reference GNRC; no named shared customer confirmed from either side | `duplicate_exposure_detection`, `missing_exposure_review` | Possibly, to locate a named shared hyperscaler customer if the batch wants to strengthen beyond GNRC's one-sided framing | Additive only | If a named shared customer cannot be confirmed, record as `complement`/`inferred` with the materiality caveat GNRC's own record already discloses (data-center revenue still a minority of GNRC's total) |
| `MSFT_GOOGL`, `AMZN_GOOGL`, `AMZN_MSFT` (three pairwise `competitor` records — §D records a symmetric type once per pair, not once per group) | `competitor` — public-cloud sellers overlapping on the same enterprise AI-infrastructure spending (§4.6) | Fully stated in one already-inspected source (`BATCH5...` §7); no additional sourcing located or required beyond what §4.6 already cites | MSFT's/GOOGL's/AMZN's own individual records do not separately, independently restate this overlap in their own words — the claim currently rests on BATCH5's own comparative synthesis only | `duplicate_exposure_detection` (this is the same T1 AI-infrastructure concentration `CLAUDE.md`'s own declined cluster-cap scan already flagged), `stress_testing` | None identified — existing evidence appears sufficient on its face | Additive only; three separate pairwise records required, each independently satisfying §D's symmetric-pair form | Evidence should carry `evidence_classification: inferred` (per §4.6's own classification, not `observed`) unless a future batch locates a more directly-sourced statement from one of the three companies' own records |

**Not recommended as a near-term batch**: the ASML/KLAC China-exposure question (§4.5) and the ISRG/TMO regulatory question (§4.4) — both were evaluated and found, on the existing evidence, to fail the "same specific mechanism" bar REL-0001 §C requires; either would need new primary research to clear that bar, which this unit does not authorize and does not recommend prioritizing over the three higher-confidence candidates above.

This recommendation ranks nothing beyond "smallest coherent first step," creates no score, and does not itself authorize any research, drafting, or file creation.

---

## 10. Explicit non-findings and boundaries (REL-0001 §I/§L compliance)

This artifact creates zero `intelligence/relationships/*.yaml` or `.md` records; performed no external company research; computed no price correlation; created no score, ranking, or composite/aggregate metric; altered no existing Company or Theme Intelligence record; recommends no tier/target/holdings/cluster/cap/gate/ladder/trim/sell/margin/allocator/brokerage/order change; does not implement any part of "Eureka" (`OPS-0016`); does not begin Milestone 5 or any later WS-0005 milestone; and does not create a new workstream. Every classification above is drawn from evidence already present in the sources listed in §3 as of `cd95a8fd21793f5d2a2383f69d6907ea6788d251`. The `milestone-4-portfolio-relationship-mapping` gate's own `status: proposed` (`operations/WORKSTREAMS.yaml`) is unchanged by this artifact. Relationship-content research remains unauthorized; the batch candidates in §9 are advisory only and require their own separate, future, explicit principal authorization before any work on them may begin.
