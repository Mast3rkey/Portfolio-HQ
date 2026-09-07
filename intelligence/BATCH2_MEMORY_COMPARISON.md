# WS-0005 Milestone 3, Batch 2 — DRAM/NAND/HBM Memory-Manufacturer Comparison

**MU, SKHY.** Authorized by `governance/decisions/PI-0024-ws0005-milestone3-batch2-memory.md`
§C (batch comparison requirements) and §I (completion criteria requiring
this evidence be retained). Created 2026-07-26, alongside the two companies'
own Company Intelligence records
(`intelligence/companies/{MU,SKHY}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema (it
introduces no new schema and is not scanned by `intelligence_validator.py`
or any other validator), and not an authoritative record any allocator or
policy decision may read. It sits at `intelligence/` root rather than inside
`companies/` (reserved for `<TICKER>.yaml`/`.md` pairs per spec §7) or
`governance/audits/` (reserved for independently-authored audits per
`OPS-0004` — this document is authored by the same implementation session as
the two company records, not an independent review of them), matching
`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`'s own placement and
scope. It does **not** rank the two companies, does not recommend a tier/
target/cluster change, and does not create a composite score of any kind —
per `PI-0024` §C's own instruction ("must not create a numerical score,
weighted ranking, composite conviction measure, or automatic capital-
priority output of any kind") and the Constitution's standing prohibition on
predictive research or opportunity maps.

**Source-access disclosure (applies to this whole document):** every fact
below is inherited from the two companies' own Company Intelligence records,
each of which discloses that WebFetch was blocked throughout the research
pass (a network/proxy-level 403 for MU's research session; a tool-level
403, including on a non-target control domain, for SKHY's research session)
and that this synthesizing/implementing session independently re-attempted
WebFetch against the specific primary-source URLs each research pass
identified and received the identical failure both times — no primary
document was independently rendered and inspected by any session at any
point. Each underlying record distinguishes document type (PRIMARY — an
issuer- or regulator-authored filing/press release; SECONDARY — journalism
or analyst commentary about one) from access status (every primary document
is labeled "identified but NOT opened by this session"); this document
inherits that same distinction rather than re-stating it in full. This
document adds no new primary research of its own — it only compares and
cross-references what the two company records already established, plus
this synthesizing session's own independent WebSearch cross-checks
(documented in each company record's own Source-access disclosure) of the
most load-bearing or previously-conflicting figures. Where a company record
flags a figure as unresolved or internally conflicting, this document
repeats that flag rather than resolving it.

## 1. Distinct competitive positions within the same product category (unlike Batch 1's distinct value-chain steps)

Unlike Batch 1 (ASML, AMAT, KLAC, LRCX), where each company performs a
genuinely distinct, largely non-substitutable step in the semiconductor
fabrication process, MU and SKHY are **direct competitors selling
substantially the same product categories** — DRAM (including HBM) and
NAND flash — into overlapping customer bases. The batch-defining question is
therefore not "what distinct function does each perform" (Batch 1's
framing) but **"what distinct competitive position does each hold within
the same function, and does owning both add exposure or mostly duplicate
one memory-cycle bet"** — the specific question `PI-0024` §C.10 requires
this document to address, taken up directly in §10 below.

| Company | Reported HBM position | Reported overall DRAM position | NAND position |
|---|---|---|---|
| MU | Fast-growing #2/#3 challenger, ~2% (2023) growing to ~18-21% (2025-2026 cuts) | #3 by most cuts found (~22% DRAM revenue share, one Q1 2026 source) | Mid-pack (~13%, one Q1 2026 source; trails Kioxia in at least one recent quarterly cut) |
| SKHY | Reported market leader, ~53-62% across sources/periods/metrics | #2 by most cuts found (~29% DRAM revenue share, one Q1 2026 source, versus Samsung's ~39%) | Reported second-largest (~21% of NAND, 2025, one source), behind Samsung |

**Both companies' own records flag the same evidentiary limitation on these
figures**: percentages vary meaningfully by source, reporting period
(quarterly vs. full-year), and metric (shipment share vs. revenue share),
and neither record found a single, internally consistent, primary-sourced
table covering both companies on an identical basis. This document does not
attempt to reconcile the two companies' figures into one unified table
beyond what is shown above — doing so would risk manufacturing false
precision from source material that both underlying records already
disclose as imprecise.

## 2. HBM versus conventional DRAM/NAND exposure (PI-0024 §C.1)

Both companies derive a material and growing share of their DRAM business
from HBM specifically, driven by the same AI-compute demand mechanism:
- **MU**: ships HBM3E (up to 36GB, 1.2TB/s peak bandwidth) and is targeting
  HBM4 mass production in 2026, claiming a hybrid-bonding advanced-packaging
  differentiation that industry reporting (semiengineering.com, cited in
  MU's own record) suggests is ahead of where the HBM4 standard has actually
  landed industry-wide (still largely microbump-based) — a claim treated in
  MU's record as a company differentiation assertion, not an established
  industry fact.
- **SKHY**: reported first to reach HBM4 mass production (February 2026, at
  its new M15X fab in Cheongju), and reportedly supplies the large majority
  of NVIDIA's current HBM (~90%, one source) and a majority of NVIDIA's
  forward HBM4 allocation (~70%, a UBS-cited forward estimate for the
  "Vera Rubin" platform, not a confirmed contract).

**Conventional (non-HBM) DRAM and NAND remain a larger share of total
revenue for both companies** (SKHY's own record estimates DRAM overall at
~70-75% of revenue, of which HBM is a growing but not dominant sub-
component; MU's record does not state an equivalent overall DRAM-vs-NAND-
vs-HBM revenue split with comparable precision — a gap this document
flags rather than fills with an unsupported estimate). Both companies'
conventional DRAM/NAND businesses are therefore still the larger revenue
base today, even though HBM is the primary driver of each company's recent
re-rating and of the batch's own AI-infrastructure investment thesis.

## 3. Product, technology, and packaging differentiation (PI-0024 §C.2)

- **Process technology**: SKHY's own record cites a "1c DRAM" (6th-
  generation, 10nm-class) node claimed as first-to-market on 1c DDR5, with
  "mature yield" per company-relayed language. MU's own record does not cite
  an equivalent specific process-node claim — a genuine information gap
  between the two records, not evidence that MU lacks a comparable node.
- **Packaging**: MU's record specifically claims a hybrid-bonding
  (direct copper-to-copper) advanced-packaging approach as a differentiator,
  flagged in MU's own record as running ahead of where the HBM4 industry
  standard has broadly settled (microbumps). SKHY's own record does not
  describe an equivalent packaging-technology claim — again, a gap in what
  was found, not a stated absence.
- **Patent claims**: a single, unverified secondary source cited in MU's
  research (not adopted as fact in MU's own record) claimed Micron holds
  621 HBM-related patents versus SK hynix's 315 — this document does not
  adopt this figure either, consistent with MU's own record's treatment of
  it, and notes it only to disclose that it was found and explicitly
  rejected as insufficiently supported.

**Overall differentiation assessment**: both companies compete in the same
HBM/DRAM/NAND product categories with genuinely different competitive
standing (SKHY currently leading by most measures, MU growing faster from a
smaller base) rather than differentiated non-competing product lines. This
is a materially different differentiation shape than Batch 1's four
companies, which occupied largely non-overlapping value-chain steps.

## 4. Manufacturing footprint and equipment dependencies (PI-0024 §C.4)

| Company | Primary manufacturing geography | China exposure | Notable equipment/expansion facts |
|---|---|---|---|
| MU | Taiwan (Taichung x3 buildings + new Tongluo site, Tainan, Taoyuan), expanding to Japan (Hiroshima), Singapore, US (Idaho, New York, Virginia), Malaysia (assembly/test) | Xi'an packaging/test facility only (no wafer fab); explicitly exiting China server/data-center sales market | US CHIPS Act funding (~$6.1-6.4B) across Idaho/New York/Virginia sites, with a 10-year "countries of concern" expansion guardrail carrying full clawback risk |
| SKHY | Korea (Icheon R&D/back-end; Cheongju NAND + new M15X HBM fab; future Yongin cluster) | Wuxi DRAM fab (~40% of DRAM output, single-source estimate) and Dalian NAND fab (~25% of NAND output, single-source estimate, acquired from Intel) — both under a renewable 2026 US site-license system following VEU revocation | Yongin Y1 phase secured KRW31T investment, start date moved up to February 2027; M15X funded partly by ADR-offering proceeds |

**Neither company's own record identifies a specific named equipment
supplier** (e.g., a direct citation naming ASML, AMAT, KLAC, or LRCX — all
four already covered in this repository's Batch 1 records — as a confirmed
supplier to MU or SKHY specifically). Given that advanced DRAM/HBM
manufacturing at the process nodes both companies describe (MU's advanced
nodes; SKHY's 1c DRAM) is understood industry-wide to require EUV
lithography and advanced deposition/etch/process-control tools of the kind
Batch 1's four companies produce, **a shared equipment-supplier dependency
across the two batches is a reasonable structural inference**, but it is
recorded here explicitly as an inference this batch's own research did not
confirm with a named-supplier citation for either MU or SKHY — an open
evidentiary gap per `PI-0024` §C.5's requirement to address "relationships
to NVDA, TSM, ASML, AMAT, KLAC, and LRCX," addressed honestly as an
unconfirmed structural relationship rather than a fabricated specific
citation.

**China exposure is structurally different in kind between the two
companies**: MU has already exited its China server/data-center *sales*
market while retaining only a packaging/test *facility*; SKHY continues to
*operate* two China wafer fabs (Wuxi, Dalian) under a renewable annual
license — meaning SKHY's China manufacturing exposure is presently larger
and more operationally active than MU's, even though MU's realized
regulatory loss (the 2023 CAC ban) was, at the time, a more severe single
adverse event than anything SKHY has yet experienced from US export-control
action specifically (SKHY's VEU revocation was resolved into continued,
capped operation rather than a market-access ban).

## 5. Relationships to NVDA, TSM, ASML, AMAT, KLAC, and LRCX (PI-0024 §C.5)

- **NVDA**: both companies are reported NVIDIA suppliers. SKHY's
  relationship is far more prominent and quantified in the evidence found
  (reportedly ~90% of NVIDIA's current HBM supply, ~70% of HBM4 "Vera
  Rubin" allocation, and disclosed revenue-concentration percentages
  reaching ~27% in 1H 2025). MU's own record found no equivalent named-
  customer concentration disclosure for NVIDIA specifically — MU is
  understood generally to sell HBM to AI-accelerator makers including
  NVIDIA, but no comparable percentage or allocation-share figure was
  located in this research pass. This is the batch's most significant
  cross-company evidentiary asymmetry: SKHY's NVIDIA relationship is
  well-quantified; MU's is not, in the evidence gathered.
- **TSM**: no direct relationship (customer, supplier, or competitor) was
  identified between either MU or SKHY and TSM in this research pass — TSM
  is a logic foundry, a different value-chain function from memory
  manufacturing, consistent with Batch 1's own finding that ASML's function
  had no direct overlap with the other three equipment names.
- **ASML, AMAT, KLAC, LRCX**: no named, sourced supplier relationship was
  found for either MU or SKHY specifically (see §4 above) — recorded as an
  open evidentiary gap, not a finding of absence, consistent with Batch 1's
  own treatment of its equipment-supplier research gaps.

## 6. Shared customers and customer overlap (PI-0024 §C.3)

Both companies' primary disclosed/reported customer overlap is
**NVIDIA and, more broadly, the same set of AI-infrastructure hyperscalers
and AI-accelerator makers** driving HBM demand. Neither company's own record
provides a customer-by-customer breakdown precise enough to determine
whether the same hyperscaler dollar is being split competitively between MU
and SKHY for the same capacity build-out (competitive substitution) versus
representing additive demand across suppliers (a hyperscaler diversifying
its HBM supply base across both) — the same evidentiary limit Batch 1's own
comparison document identified for its four companies' shared customers
(§3 of that document), preserved here rather than resolved. What can be
stated with reasonable confidence: NVIDIA's own stated strategy of
diversifying its HBM supplier base (SKHY's own record cites NVIDIA's
reported ~90%-toward-~50% SK hynix supply-share moderation as *evidence of*
active diversification) implies NVIDIA specifically treats MU and SKHY as
at least partially substitutable suppliers for a share of its HBM
purchasing — a customer-side view distinct from, and more concrete than,
the general "shared customer base" finding in Batch 1.

## 7. Shared memory-pricing and capital-expenditure cycles (PI-0024 §C.6)

Both companies are exposed to the same underlying commodity-memory-pricing
cycle, and both companies' own records document the same historical
downturn window (2022-2023) with directly comparable severity, though
measured on different financial-statement lines:

| Company | 2022-2023 downturn evidence | Current (2025-2026) upcycle evidence |
|---|---|---|
| MU | FY2023 Q2 revenue -53% YoY; full-year FY2023 GAAP net loss ~$1.6B; $1.83B inventory write-downs; ~70% peak-to-trough pricing decline (industry-wide) | Q3 FY2026 revenue +345.7% YoY, GAAP net income $28.24B, 81.2% operating margin |
| SKHY | Q4 2022 operating loss KRW1.7T (first quarterly operating loss since Q3 2012); full-year 2023 operating loss KRW7.73T; DRAM revenue -54% YoY (Q4 2022) | Q1 2026 revenue KRW52.58T (record), operating profit KRW37.61T (72% margin), net profit margin 77% |

**Both companies moved from loss/near-loss conditions to record profitability
within the same roughly three-year window, driven by the same underlying
memory-pricing and AI-demand cycle** — this is the batch's clearest,
best-evidenced simultaneous-loss (and simultaneous-recovery) mechanism, a
direct memory-sector analog to Batch 1's own semiconductor-capex-cycle
finding, but arguably sharper and faster-moving given both companies swung
between an outright annual loss and record annual profit within roughly
three years, versus the equipment names' comparatively smoother
(backlog-buffered, per ASML's own record) revenue cycles.

**Capex behavior differs somewhat in emphasis**: MU's own record documents
an explicit ~4x capex swing (FY2023 trough $7B to FY2026 guided ~$27B)
alongside a stated intent to "return 100% of excess cash... over time" that
press coverage has characterized as not yet matched by actual capital
return (the dividend/buyback "payout-ratio anomaly" in MU's own record).
SKHY's own record documents a stated "Value Up" capital-discipline framework
targeting total annual investment at a mid-30s-percent-of-revenue ceiling,
alongside an already-executed 25% dividend increase and an active,
recurring buyback-and-cancel program — a more advanced, already-implemented
capital-return posture than MU's own record describes as still emerging.
This document does not judge which posture is preferable — only that they
differ, and that the difference is evidenced in each company's own record.

## 8. China/export-control and geopolitical exposure — comparative summary (PI-0024 §C.7)

| Company | Regime | Current status | Most severe disclosed/estimated impact found |
|---|---|---|---|
| MU | US-adjacent (China's own CAC cybersecurity-review authority, not a US export-control action) | **Realized and largely resolved via exit** — 2023 CAC ban led to a 2025 complete exit from China's server/data-center memory market; retains only a packaging/test facility in Xi'an | ~11% of 2022 revenue in the affected segment (CSIS characterization); FY2025 mainland-China revenue now ~7.1% of total ($2.64B), independently cross-checked by this synthesizing session |
| SKHY | US export-control (BIS Validated End-User authorization) | **Ongoing, recently narrowed but not resolved** — VEU revoked effective 2025-12-31, replaced by a renewable annual site-license system for 2026 permitting continued fab operation but not expansion/technology upgrades | Wuxi (~40% of DRAM output) and Dalian (~25% of NAND output) figures, both single-source and not independently corroborated in this research pass — if accurate, a structurally larger share of current output than MU's remaining China exposure |

**This is a materially different risk shape between the two companies, not
merely a difference in severity**: MU's China risk is a completed,
already-absorbed loss with a now-smaller, more contained remaining
footprint (packaging only, no wafer fab); SKHY's China risk is an ongoing,
operationally larger exposure (two active wafer fabs) currently under a
license structure that must be renewed, not a one-time resolved event. A
future China or US regulatory escalation would therefore likely affect the
two companies asymmetrically — SKHY has more currently-operating China
capacity exposed to a potential further tightening than MU does.

## 9. Customer concentration — comparative summary (PI-0024 §C.3, expanded)

The batch's clearest evidentiary asymmetry, restated from §5 above: **SKHY's
NVIDIA concentration is well-quantified and trending (27% 1H 2025 -> 24%
FY2025, with a second customer newly crossing 10% at 12.4% in 2026); MU's
comparable customer/hyperscaler concentration was not found in this research
pass at all** — MU discloses only volume-commitment metrics (16 Strategic
Customer Agreements covering ~20% of DRAM volume, up to a third of NAND
volume), not a customer-identity or revenue-percentage figure. **This
document does not conclude MU therefore has lower customer concentration
than SKHY** — the honest state of the evidence is that MU's concentration
level is simply unknown from what this research pass could access, not
that it is known to be lower. This is flagged explicitly as a priority item
for the primary-source verification (MU's 10-K customer-concentration
disclosure) that both companies' own records already identify as
outstanding.

## 10. Differentiated portfolio exposure and duplication assessment (PI-0024 §C.9, §C.10)

**Genuinely differentiated exposure between MU and SKHY:**
- **Competitive position**: SKHY is the reported HBM share leader and
  primary NVIDIA HBM supplier; MU is a fast-growing challenger from a
  smaller base. These are different points on the same competitive curve,
  not the same position twice.
- **Geographic/regulatory risk profile**: MU's realized-and-largely-resolved
  China risk (exit, retained packaging only) versus SKHY's ongoing,
  larger, renewable-license China fab exposure (§8) is a genuine
  differentiation in geopolitical risk shape, not merely magnitude.
  MU's Taiwan concentration (three-plus fab sites) and active
  diversification into Japan/Singapore/US versus SKHY's Korea-concentrated
  footprint (with China fabs as the secondary site) is a distinct
  geographic-concentration profile for each company.
- **Security-structure risk**: SKHY carries the ADR conversion-cap/premium
  structural risk documented in its own record — a risk category MU (a
  domestic US issuer, not an ADR) does not carry at all. This is a genuine,
  non-duplicative risk-exposure difference between the two holdings,
  independent of their underlying businesses' competitive overlap.
- **Currency/reporting basis**: SKHY reports in KRW as a Korea-domiciled
  foreign private issuer; MU reports in USD as a US domestic issuer — a
  structural difference in currency and disclosure-regime exposure that
  this research pass did not develop in quantitative detail for SKHY (see
  Source-access disclosure), but which is a real, non-duplicative
  difference in kind.

**Where the two companies mostly duplicate one memory-cycle bet:**
- Both are exposed to the same underlying DRAM/NAND/HBM commodity-pricing
  cycle (§7), documented in both records as having moved through the same
  loss-to-record-profit swing within the same roughly three-year window.
  A broad memory-cycle downturn is very likely to affect both companies
  simultaneously and in the same direction, even if the magnitude differs
  by company.
- Both are exposed, at least partially, to the same AI-compute/HBM demand
  driver and, per NVIDIA's own reported multi-supplier strategy (§6), at
  least partly to the same customer dollar.
- Both companies' own records independently flag the same *forward* risk,
  sourced separately but converging on the same 2027-2028 timeframe:
  outside analysts in MU's research flagged HBM oversupply risk for 2028 as
  all three major DRAM makers expand capacity in parallel; SKHY's own
  research separately flagged the identical concern (SemiWiki/Silicon
  Analysts-style commentary on FY2028 estimate risk) — this convergence,
  reached independently for each company rather than copied from one
  record to the other, is treated in this document as meaningfully
  strengthening the shared-cycle-risk finding rather than as a
  coincidence.

**Overall assessment (descriptive, not a recommendation, per PI-0024 §C's
explicit prohibition on ranking or scoring):** owning both MU and SKHY adds
real, evidenced differentiated exposure — different competitive standing
within HBM, different and asymmetric geopolitical/China risk shapes, and a
security-structure risk (the ADR mechanic) unique to SKHY — layered on top
of a shared, and likely dominant, memory-pricing-cycle bet that a holder of
either company alone would also be exposed to. Whether that differentiated
layer is "worth" holding both names, at what size, or relative to any other
capital use is a capital-priority and policy question this document is
explicitly prohibited from answering (`PI-0024` §C, §H) and defers entirely
to any future, separately authorized policy process.

## 11. Common correlated-loss mechanisms — consolidated (PI-0024 §C.8)

Consolidated from both company records' own disclosed risk evidence:
1. **Broad memory-cycle price contraction** (§7, §10) — the batch's
   clearest, best-evidenced simultaneous-loss mechanism, affecting both
   companies' revenue/earnings in the same direction, historically with
   comparable severity (both moved to a full-year loss or near-loss in
   2022-2023).
2. **A shared customer-concentration shock** — if NVIDIA (or the broader
   AI-hyperscaler buyer base both companies depend on) were to
   materially reduce HBM/DRAM purchasing, both companies would likely be
   affected, though SKHY's disclosed concentration to NVIDIA specifically
   is higher and better-quantified than MU's (§5, §9), so the *magnitude*
   of this shared mechanism is asymmetric even though the *direction* is
   shared.
3. **A parallel-capacity-expansion oversupply event** (§10) — both
   companies' own research independently surfaced the same 2027-2028
   oversupply concern as all three major DRAM makers (MU, SKHY, Samsung)
   expand HBM/DRAM capacity simultaneously into a currently tight market —
   the classic memory-industry boom-bust pattern, evidenced historically by
   the 2021-2023 cycle documented in both records.
4. **A China/export-control escalation** — though, per §8, this would likely
   hit the two companies asymmetrically (SKHY's larger, currently-operating
   China fab footprint versus MU's smaller, already-reduced exposure)
   rather than identically.

## 12. Where evidence is insufficient to compare confidently — consolidated (PI-0024 §C, evidentiary-gap discipline)

Per the same discipline `PI-0023`'s own comparison document applied
(§11 of `BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`), consolidated from both
company records' own disclosed gaps:
- **MU's customer/hyperscaler revenue concentration** — not found at all in
  this research pass (§9), the batch's single most consequential
  evidentiary asymmetry between the two companies.
- **Exact reconciled HBM/DRAM/NAND market-share figures for either
  company** — genuinely variable by source, period, and metric; neither
  company's own record, nor this document, resolves this into a single
  precise number (§1, §2).
- **A confirmed, named equipment-supplier relationship for either company**
  to any of Batch 1's four covered names (ASML/AMAT/KLAC/LRCX) — an
  inference this batch's research did not confirm (§4, §5).
- **Whether shared customers represent additive demand or competitive
  substitution for the same capex dollar** — not disclosed at that level of
  granularity for either company (§6), the same limit Batch 1's own
  comparison found for its four companies.
- **SKHY's F-1/424B4 risk-factors section** — never opened by any session in
  this research (China/currency/FPI-disclosure/customer-concentration
  language as SK hynix itself discloses it, not as journalism paraphrases
  it) — the single highest-priority primary-source verification item
  carried forward from SKHY's own record.
- **Precise, reconciled Wuxi/Dalian output-share percentages** for SKHY —
  each traces to a single, uncorroborated source (§4, §8).
- **Cycle-timing (lead/lag) between MU and SKHY specifically** — no source
  found in either company's research directly and quantitatively compares
  the two companies' cycle timing, the same kind of gap Batch 1's own
  comparison document found for its four companies' cycle-timing question.

## 13. External opportunity and replacement-candidate scan — batch-level consolidation (PI-0024 §B.18)

Per `PI-0024` §B.18. Each company's own record and this research pass
surfaced named non-owned competitors; consolidated here as a small,
evidence-supported leads list. **All items below are future-research leads
only** — none is researched as a full company, none is added to holdings,
none is assigned a tier or target, none is ranked, and none authorizes
expanding this batch or beginning research on any of them without its own
separate future authorization, per `PI-0024` §B.18 and §H's explicit
prohibitions.

| Candidate | Possible economic role | Competes against |
|---|---|---|
| Samsung Electronics | The third major global DRAM/NAND/HBM maker, named as a direct competitor in both MU's and SKHY's own records (and already the primary competitive reference point in most of the market-share figures cited throughout this document) | Would represent duplicate, not new, exposure to the same DRAM/NAND/HBM memory-cycle driver MU and SKHY already provide — not a diversifying candidate by economic function, though its listing venue/structure (a Korean conglomerate affiliate with a different ownership and disclosure profile than either MU or SKHY) was not assessed here |
| Kioxia (Japan) | Named in MU's own record as a NAND competitor that, in at least one recent quarterly cut, held greater NAND share than MU | Duplicate exposure to the NAND sub-segment of the same memory-cycle driver; not independently assessed for accessibility (listing venue, ADR/ordinary-share considerations) in this pass |
| ChangXin Memory Technologies (China) | Referenced in SKHY's own record as an emerging Chinese domestic DRAM competitor | Not assessed as a portfolio-exposure candidate in the conventional sense — a Chinese-domiciled competitor with its own distinct regulatory and accessibility considerations, recorded only as a competitive-erosion risk to the two companies' existing thesis, not as an investable lead, consistent with how Batch 1's own comparison document treated Naura/AMEC |

No candidate above is recommended for purchase, tier assignment, or further
research by this document. Any future research on any of them requires its
own separate authorization, per `PI-0024` §B.18.

## 14. Zero-based discipline note

Per `OPS-0006` §§2/3 and `PI-0024` §G, this comparison was constructed from
the two companies' own independently-researched records, each of which
reasoned its conviction rating from disclosed business/risk evidence before
— not by way of — the companies' existing governed tier/target/cluster
placement (both MU and SKHY: `band` tier, 0.75% target, `semis` cluster,
capped at 25% of book). Both companies received the same **Medium**
conviction rating despite occupying different competitive positions within
their shared product category — this document does not treat that
similarity in rating as evidence the two companies are more alike than the
evidence above shows; each company's own record reasoned its rating from
distinct evidence (SKHY's rating weighs its NVIDIA concentration and
ADR-structural risk most heavily; MU's weighs its #2/#3 HBM competitive
position and realized China risk most heavily), and this document's own
§10 differentiation analysis stands independent of the fact that both
ratings landed on the same ordinal value. This batch's evidence is broadly
consistent with `targets.yaml`'s own existing `semis` cluster comment
grouping MU together with WDC as "memory" names — though `PI-0024` §E
separately identifies that specific WDC characterization as stale following
Western Digital's February 2025 Sandisk separation, a correction this batch
does not make (see each company's own "Current governed tier and target"
section). Any apparent tension between this batch's evidence and current
policy (for example, either company's Medium conviction rating alongside
its existing `band`/0.75% placement, or the batch's own finding that MU's
customer-concentration profile is simply unknown rather than known-low) is
recorded as a future reconciliation question for the still-unauthorized
Milestone 7, not resolved or implemented here.
