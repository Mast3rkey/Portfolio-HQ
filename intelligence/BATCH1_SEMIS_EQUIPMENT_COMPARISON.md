# WS-0005 Milestone 3, Batch 1 — Semiconductor Capital-Equipment Comparison

**ASML, AMAT, KLAC, LRCX.** Authorized by `governance/decisions/PI-0023-ws0005-milestone3-batch1-semis-equipment.md`
SSB.12/SSB.16 (batch-level overlap/dependency/shared-risk evidence) and SSE
(completion criteria requiring this evidence be retained). Created
2026-07-25, alongside the four companies' own Company Intelligence records
(`intelligence/companies/{ASML,AMAT,KLAC,LRCX}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema
(it introduces no new schema and is not scanned by `intelligence_validator.py`
or any other validator), and not an authoritative record any allocator or
policy decision may read. It sits at `intelligence/` root rather than inside
`companies/` (reserved for `<TICKER>.yaml`/`.md` pairs per spec SS7) or
`governance/audits/` (reserved for independently-authored audits per
`OPS-0004` — this document is authored by the same implementation session
as the four company records, not an independent review of them). It does
**not** rank the four companies, does not recommend a tier/target/cluster
change, and does not create a composite score of any kind — per `PI-0023`
SSB.12's own instruction ("how it differs from and overlaps with the other
three companies... descriptive only") and the Constitution's standing
prohibition on predictive research or opportunity maps.

**Remediation pass (2026-07-25):** following a preliminary external
primary-source cross-check on the underlying company records, this
document was updated to match: the China-exposure comparison table (§9)
now reflects KLAC's reconciled by-fiscal-year figures (43% FY2024 ->
33% FY2025, not an unresolved conflict) and drops the claim that AMAT
carries the batch's highest China exposure (LRCX's 43% Q1 FY2026 peak and
KLAC's FY2024 43% figure both exceed AMAT's range); the cyclicality
table (§6) now cites LRCX's precisely-sequenced 31.4% YoY decline
(Q1 FY2024 vs. Q1 FY2023) rather than an unqualified "~31%" figure; and
§8's export-control table notes AMAT's additional, distinct February 2026
BIS settlement (a confirmed compliance violation, not merely a shared
regulatory-environment risk). See each company's own record for the full
correction detail and citations.

**Second remediation pass (2026-07-25), source-accounting
micro-remediation:** further corrected to match each company's own
second-pass corrections: AMAT's BIS settlement date is now stated as two
distinct dates (AMAT's own press release 2026-02-11; BIS's own press
release 2026-02-12), and the "56 violations to SMIC" characterization is
now narrowed as unverified against the primary charging document (§8);
KLAC's China-revenue figures are now stated as KLA's own reported
whole-percentage figures (43%/33%/27% for FY2024/FY2025/FY2023) rather
than a third-party-calculated decimal, with FY2023's 27% flagged as
lower-confidence (not independently re-corroborated) than FY2024/FY2025
(§9); ASML's geographic-sales figures are now cited to the exact official
investor-relations presentation containing the table, with a conflicting
29.1%-China figure found once and explicitly not adopted (§8-9); and
LRCX's downturn-quarter citations now include the exact per-quarter 8-K
exhibit URL for each of the five quarters in the sequence (§6). See each
company's own record for full detail.

**Source-access disclosure (applies to this whole document):** every fact
below is inherited from the four companies' own Company Intelligence
records, each of which discloses that WebFetch was blocked (HTTP 403) on
every primary-source domain attempted throughout this research pass and
both remediation passes — no primary document was independently rendered
and inspected by this session at any point. Each underlying record now
distinguishes document type (PRIMARY — an issuer- or regulator-authored
filing/press release; SECONDARY — journalism or analysis about one) from
this session's access status (every primary document is labeled
"identified but NOT opened by this session"); this document inherits that
same distinction rather than re-stating it. This document adds no new
primary research of its own — it only compares and cross-references what
the four company records already established. Where a company record
flags a figure as unresolved or internally conflicting, this document
repeats that flag rather than resolving it.

## 1. Distinct economic function (no overlap in what each company sells)

| Company | Function | Value-chain step |
|---|---|---|
| ASML | Photolithography systems (EUV/DUV) | Patterning — printing the circuit onto the wafer |
| AMAT | Deposition, etch, ion implantation, CMP, metrology/inspection | Materials engineering — building/shaping the wafer's physical structure, broadest single-company step coverage in the batch |
| KLAC | Process control: inspection, defect review, metrology | Measurement — verifying the wafer at each step, does not process it |
| LRCX | Plasma etch, thin-film deposition (memory-concentrated) | Materials engineering — etch/deposition, overlapping AMAT most directly |

All four sell into the same customer base (chip fabricators) for the same
ultimate reason (semiconductor-capacity capital expenditure), but each
performs a genuinely distinct, largely non-substitutable step in the same
fabrication process. ASML's function (patterning) has no substitute
provider anywhere; KLAC's function (measurement) is categorically distinct
from AMAT's/LRCX's (processing); AMAT and LRCX are the batch's one genuine
product-overlap pair (see SS3 below).

## 2. Product and process exposure / overlap

- **ASML vs. the other three:** essentially no direct product overlap.
  ASML's KLAC-adjacent exposure runs through KLAC's competitor relationship
  with ASML's own metrology/inspection business (HMI/YieldStar), not
  through ASML's core lithography business — recorded in KLAC's own record
  as a competitive relationship, not recorded from ASML's side as a direct
  competitive threat (ASML's record does not name KLAC as a competitor).
- **AMAT vs. LRCX — the batch's one direct, two-sided competitive
  relationship.** Both companies' own records independently name the
  other: AMAT's record states Lam is "described as etch market leader,
  especially high-aspect-ratio" and "clear second in deposition" after
  AMAT; LRCX's record states "Applied Materials (deposition/etch overlap —
  the most direct competitor of the four companies in this batch)."
  Secondary sources cited in both records put the top-5 WFE vendors
  (ASML, AMAT, Tokyo Electron, LRCX, KLA) at roughly 75% of industry
  sales combined — a market-structure fact, not something either company
  record treats as precisely apportioned between AMAT and LRCX
  specifically.
- **AMAT vs. KLAC:** AMAT's own record states KLAC's process-control
  competition is understood as "exerting indirect pressure via fab
  capex-allocation competition rather than direct product overlap" — i.e.
  they compete for the same customer capex dollar, not for the same
  physical tool sale, except that AMAT is separately reported (in KLAC's
  record) to hold some process-control tools of its own and to have lost
  share in that specific sub-segment (reportedly ~13% to under 8%,
  secondary, unverified exact figures) — a narrow area of genuine, if
  small, product overlap.
- **KLAC vs. LRCX:** minimal direct overlap — LRCX's record describes KLA
  as "more a customer-side WFE-cycle correlate than a competitor."

## 3. Shared customers

All four companies' records independently name overlapping customers:
TSMC, Samsung, and Intel appear in some combination across all four
records; SK Hynix and Micron appear specifically in LRCX's and, to a lesser
extent, KLAC's records (memory exposure). No record in this batch disclosed
a customer-by-customer revenue breakdown precise enough to state whether
the same *dollar* of a shared customer's capex is being fought over by
multiple companies in this batch versus representing genuinely additive
demand (e.g. TSMC buying lithography from ASML and etch from LRCX in the
same capacity build-out is additive demand, not competitive substitution).
This distinction — shared customer versus competitive substitution for the
same customer dollar — is preserved here as a real evidentiary limit, not
resolved.

## 4. Shared suppliers

No source in any of the four company records identified a supplier shared
across two or more of the four companies. ASML's record names specific,
largely exclusive suppliers (Carl Zeiss SMT for optics, its own wholly-
owned Cymer subsidiary for light sources) that are specific to
lithography and not shared with the other three. AMAT's, KLAC's, and
LRCX's records each disclose this as a genuine research gap (no specific
named suppliers found for any of the three). **No shared-supplier
concentration risk can be stated as a finding from this batch's evidence**
— this is an absence of evidence, not evidence of absence, and is recorded
as an open gap rather than a conclusion either way.

## 5. Shared semiconductor-capex drivers (the batch's actual common thread)

All four companies are exposed to the same underlying demand driver:
semiconductor fabrication-capacity capital expenditure ("WFE," wafer-fab
equipment spending), currently characterized across all four records as
being driven by AI/leading-edge-logic capex, advanced-packaging growth,
and (for LRCX/AMAT specifically) memory-technology transitions. This is
the mechanism `targets.yaml`'s own `semis` cluster-cap comment already
identifies generally for the wider 13-name cluster ("these names crash
together... the equipment (KLAC/LRCX/AMAT)... names crash hardest") and
this batch's evidence is broadly consistent with that existing doctrine
observation — recorded here as a consistency check against existing
policy per `OPS-0006` SS2/SS3's zero-based discipline, not as this
record's own independent re-derivation of the cluster-cap's correlation
finding (no new correlation scan was run by this batch; that would be
outside `PI-0023`'s authorized scope).

## 6. Common loss mechanisms and cyclicality — comparative summary

| Company | Documented downturn evidence | Severity/amplitude found |
|---|---|---|
| ASML | Revenue never fell YoY in the 2022-2025 window researched (backlog-smoothed); stock fell ~30% from its 2021 ATH during the 2022 downturn (approximate); a guidance-cut-driven ~16-20% two-day stock drop in October 2024 (fundamentals-timing, not a realized multi-quarter earnings decline) | Revenue: low/smoothed. Order/stock: high, but distinctly guidance-cut-driven rather than realized-earnings-driven in the one clear recent episode found |
| AMAT | FY2019 revenue guided down ~16% (2019 memory downturn); one third-party source (Trefis, unverified) cites an average 23% peak-to-trough stock decline across 15 historical shocks and a ~55% deepest historical drawdown | Moderate-to-high by the one third-party framing found, not independently corroborated to a second source |
| KLAC | FY2024 confirmed revenue decline of ~6.5% (the only company in the batch with a directly confirmed, primary-adjacent recent annual revenue decline figure); no comparable-quality drawdown or 2022-2023-specific figure found | Lowest confirmed magnitude of the four by this measure, though see SS9 below — KLAC also carries a genuine, reconciled China-revenue decline (43% FY2024 to 33% FY2025) not reflected in this row's revenue-decline metric |
| LRCX | Q1 FY2024 revenue -31.4% YoY (vs. Q1 FY2023 specifically — distinct from two separate sequential 26.7% and 17.1% QoQ declines in the two preceding quarters), adjusted EPS -34% YoY (2022-2023 memory downturn) — the single sharpest, best-quantified quarterly decline found anywhere in this batch; a ~7%-workforce layoff in the same episode, officially filed 2023-01-23 | Highest confirmed magnitude of the four |

**This table should not be read as a ranking of investment quality** — it
reflects only which downturn episodes happened to be best-documented in
the sources found during this research pass, filtered through each
company's own disclosure practices and this record's own source-access
limitations. KLAC's apparently "mild" cyclicality by the revenue-decline
metric above is a real, confirmed FY2024 fact, but KLAC also carries a
real, reconciled China-revenue exposure (SS9 below) that this narrow
revenue-decline table does not capture — stated explicitly to avoid
reading this table as a comprehensive risk ranking.

**Simultaneous-loss mechanism:** all four companies share exposure to the
same WFE-spending cycle, meaning a broad semiconductor-capex contraction is
a genuine simultaneous-loss risk across the batch (and, per `targets.yaml`'s
own cluster-cap doctrine, across the wider 13-name `semis` cluster). None
of the four company records found a source that quantifies precise
lead/lag timing between the four companies within a single cycle (see SS7
below) — the *magnitude* differs (LRCX's memory concentration produces
sharper swings; ASML's backlog smooths revenue relative to orders), but no
record establishes a confident *phase* relationship (who moves first).

## 7. Cycle-timing (lead/lag) — an explicit, batch-wide evidentiary gap

Each of the four company records independently searched for and reported
on this question, and each independently found the same result: **no
source located in this research directly and quantitatively compares
cycle timing across two or more of these four companies.** What each
record found instead:
- ASML's order/backlog cycle (12-24 month lead time) is understood, from
  ASML-specific commentary only, to run ahead of ASML's own revenue
  recognition — not compared directly to AMAT/KLAC/LRCX in any source
  found.
- LRCX's record found amplitude evidence (Lam's cycle swings appear
  sharper than KLA's in at least one same-period growth-rate comparison
  cited) but explicitly not phase/timing evidence.
- KLAC's record found only qualitative claims that process-control spend
  may be "stickier" than raw capacity-expansion spend, with no quantified
  lead/lag figure.
- AMAT's record found generic industry commentary that all major WFE
  vendors move with the same capacity-planning driver, which is
  consistent with (but does not establish) simultaneous rather than
  staggered exposure.

**This is recorded as an open batch-level research gap**, not resolved by
this document, consistent with `PI-0023` SSB.12's instruction to "state
where evidence is insufficient to compare confidently."

## 8. Export-control exposure — comparative summary

All four companies are exposed to export-control risk, but the *regime*
differs meaningfully:

| Company | Regime | Most severe disclosed/estimated impact found |
|---|---|---|
| ASML | Dutch/EU export licensing (EUV blocked since 2019, DUV licensing since Sept 2023), layered under a separate US pressure/legislative track (the pending, not-yet-enacted "MATCH Act") | China net-system-sales share, per ASML's own Q2 2026 investor presentation (identified but not opened this session): 36% (Q4 2025) -> 19% (Q1 2026) -> 14% (Q2 2026) — a decline across two 2026 quarters starting from a Q4 2025 baseline. A conflicting 29.1% figure for Q2 2026 surfaced once in this batch's second remediation pass and was explicitly not adopted (single, unattributed appearance vs. 14%'s repeated cross-corroboration — see ASML's own record). October 2024 guidance-cut episode (~16-20% two-day stock decline) was demand-timing-driven, not directly an export-control event |
| AMAT | US BIS regime only (Oct 2022, Oct 2023, Sept 2025 actions), plus a reported-but-unofficial Chinese domestic-content mandate, **plus AMAT's own confirmed compliance violation** — a BIS settlement (AMAT's own press release dated 2026-02-11; BIS's own press release dated 2026-02-12) distinct from the shared regulatory-environment risk the other three companies also face | ~$400M disclosed Oct 2022 impact; ~$110M+$600M disclosed Sept 2025 impact ($710M combined is the sum of these two, not a separate figure); $252.5M BIS settlement penalty, well-corroborated as to amount — the specific "56 violations"/"SMIC" characterization is reported across multiple secondary/legal-advisory sources but is NOT verified against the primary charging document, and one newer source describes the violation period and named recipient differently (see AMAT's own record for the full discrepancy) |
| KLAC | US BIS regime only (Oct 2022, Apr 2026) | $600-900M estimated Oct 2022 impact; Apr 2026 Hua Hong-related impact magnitude undisclosed as of this record's evidence date; China revenue itself declined from 43% (FY2024) to 33% (FY2025) of total revenue, reconciled in this record's remediation pass |
| LRCX | US BIS regime only (Oct 2022, a 2023 servicing-restriction episode, a 2026 "affiliate rule") | ~$2.5B (~13% of FY2022 revenue) estimated Oct 2022 impact — the largest single disclosed percentage-of-revenue impact found in the batch; ~$600M disclosed calendar-2026 impact from the newer rule |

**ASML is structurally distinct from the other three** — it is the only
company in the batch subject to a *national-government-level* (Dutch)
licensing regime independent of, though coordinated with, US policy, and
the only one with a pending legislative threat (the MATCH Act) that would
extend restrictions to a currently-still-sellable product line (DUV). The
other three share an identical regulatory mechanism (US BIS rules) applied
independently to each company, meaning a single US regulatory action is
capable of hitting AMAT, KLAC, and LRCX simultaneously (as the April 2026
Hua Hong shipment-halt order reportedly did, per KLAC's record, to KLAC,
LRCX, and AMAT together) — a genuine, evidenced simultaneous-loss
mechanism distinct from, and in addition to, the shared WFE-cycle
mechanism in SS6 above. **AMAT is additionally distinct from KLAC and
LRCX** in carrying a confirmed historical export-compliance *violation* of
its own (the February 2026 BIS settlement) — a company-specific
compliance-conduct data point, not merely exposure to the shared
regulatory environment; no comparable confirmed violation was found for
any other company in this batch.

## 9. Customer concentration — comparative summary, normalized by period where possible

**Remediation pass (2026-07-25):** this table was corrected to reconcile
KLAC's China-revenue figures by fiscal year rather than presenting them as
an internally inconsistent range, and to remove an unsupported claim
(previously stated in an earlier draft of AMAT's own record) that AMAT
carries the batch's highest China exposure — on the figures actually
found, LRCX's single-quarter peak (43%) and KLAC's FY2024 figure (43%)
both exceed anything found for AMAT.

| Company | China revenue (most recent/best-available figures, by period) | Confidence |
|---|---|---|
| ASML | 36% (Q4 2025) -> 19% (Q1 2026) -> 14% (Q2 2026) of net system sales; FY2026 guided toward ~20% full-year average | Moderate-to-high — company-guided figures, quarterly shipment mix corroborated across multiple independent sources |
| AMAT | 24-30% range across FY2022-Q2 FY2026 periods, moving unevenly (not the batch's highest — see below) | Moderate — multiple sources roughly agree on the range, though exact-period figures/bases differ (systems+services vs. total revenue) |
| KLAC | 27% (FY2023) -> 43% (FY2024) -> 33% (FY2025) of total revenue, per KLA's own reported whole-percentage figures ("Revenue from customers in China was 33% of revenue in 2025 (43% in 2024)," per the 10-K's own stated language) | Moderate-to-high for FY2024/FY2025 (independently re-confirmed via direct WebSearch match to a filing-summary source this pass); lower confidence for FY2023's 27% specifically (not independently re-corroborated by a second search) |
| LRCX | 34% (FY2025 full year) -> 43% peak (Q1 FY2026) -> guided below 30% (calendar 2026) — the batch's single largest disclosed percentage-of-revenue peak | Moderate-to-high — the clearest, most consistently sourced China-percentage trajectory in the batch |

**On a peak-percentage basis, LRCX (43%) and KLAC (43%) both exceed
AMAT's range (24-30%)** — this record does not claim AMAT carries the
batch's highest China exposure, correcting an earlier draft of AMAT's own
record that made that comparative claim without a consistent, same-period,
same-basis comparison across all four companies. All four companies
disclose or are guided toward China representing a smaller share of
revenue going forward (ASML ~20% FY2026 guide; KLAC reportedly guided
toward the mid-20s; LRCX guided below 30% for calendar 2026); AMAT's own
record did not find a forward-looking company guidance figure for its
China percentage specifically. KLAC's FY2024/FY2025 figures are now
independently re-confirmed at higher confidence than the FY2023 27%
figure, which was not re-corroborated by a second search in this pass —
the 27% figure is retained per the external cross-check's instruction but
treated as the one remaining lower-confidence data point in this table.

## 10. Differentiation and substitution risk

- **ASML has no substitution risk from within this batch** — none of
  AMAT/KLAC/LRCX competes in or could substitute for lithography.
- **AMAT and LRCX are each other's most direct within-batch substitution
  risk** for deposition/etch business specifically, per SS2 above — a
  customer choosing between the two for a given process step is the
  batch's one real head-to-head competitive dynamic.
- **KLAC has limited within-batch substitution risk** — AMAT holds some
  process-control tools (reportedly declining share in that specific
  sub-segment) but this is a minor overlap relative to KLAC's core
  business, per KLAC's own record.
- Each company's record separately names external (non-batch) competitors
  with more direct substitution relevance: Nikon/Canon for ASML (DUV-only,
  no EUV competitor); Tokyo Electron for AMAT and LRCX (etch/deposition,
  also strong in coater/developer tracks neither AMAT nor LRCX
  competes in directly); Onto Innovation and ASML's own HMI/YieldStar
  business for KLAC.

## 11. Where evidence is insufficient to compare confidently (consolidated)

Per `PI-0023` SSB.12's explicit instruction, consolidated from all four
company records' own disclosed gaps:
- Cycle-timing (lead/lag) across the four companies — no source found (SS7).
- Whether shared customers represent additive demand or competitive
  substitution for the same capex dollar — not disclosed at that level of
  granularity anywhere in the batch's sources (SS3).
- Shared-supplier concentration — absence of evidence found for AMAT/
  KLAC/LRCX (only ASML's suppliers are specifically named), not evidence
  of absence (SS4).
- KLAC's true China-revenue exposure — internally inconsistent sources,
  the batch's single largest data-quality gap (SS9).
- Precise apportionment of the reported ~75% top-5-WFE-vendor combined
  market share among AMAT, LRCX, and the other listed vendors specifically
  (SS2).
- COVID-19-era (2020) company-specific impact — not researched to a
  confirmed answer for any of the four companies.

## 12. Margin-relevance evidence — batch-level synthesis (factual, advisory only)

Per `PI-0023` SSB.16 and `OPS-0006` SS4's Milestone 3 requirement. This
section is descriptive only: it does not recommend borrowing, estimate a
safe leverage level, recommend deployment timing, or create a margin
signal, and does not change or reference the account's existing 1.8x
leverage cap or 30% buffer floor. Company-level detail lives in each
company's own record; this section states only what is genuinely
batch-level (i.e., about the interaction of the four companies together,
not restatable from any single company's own record).

- **Simultaneous-loss mechanisms, batch-level**: two distinct, evidenced
  mechanisms exist — (1) a broad WFE-spending contraction (all four
  exposed, per SS6), and (2) a single US BIS regulatory action capable of
  hitting AMAT, KLAC, and LRCX simultaneously (the April 2026 Hua Hong
  order reportedly affected all three; ASML sits partly outside this
  specific mechanism as it answers to Dutch/EU authority first, per SS8).
  These two mechanisms can compound: a WFE downturn and a regulatory
  action are not mutually exclusive and have occurred in overlapping
  windows historically (the October 2022 export-control action landed
  during the same broad 2022-2023 cyclical downturn all four companies
  were independently exposed to).
- **Recovery uncertainty, batch-level**: the batch's evidence shows
  differing recovery patterns — ASML's revenue was never observed to
  decline outright in the window researched (backlog-smoothed); KLAC's one
  confirmed down year (FY2024) recovered within a single subsequent fiscal
  year (+24% FY2025); LRCX's 2022-2023 downturn's precise stock-price
  recovery timeline was not established in this research (only the
  revenue-recovery pattern via subsequent quarters). No batch-wide recovery
  timeline can be stated with confidence.
- **Gap risk / detectability**: the batch's four companies differ in how
  early thesis deterioration would likely become visible — ASML's 2026
  discontinuation of bookings disclosure specifically *reduces* early
  visibility for that one company going forward (a fact disclosed in
  ASML's own record); KLAC's backlog-conversion disclosure (71-76% within
  12 months, if reliable) would give somewhat *more* forward visibility
  than a company without any such disclosure. This creates a genuine,
  evidenced batch-level asymmetry in detectability, not merely a
  company-level one.
- **Correlated historical-loss magnitude**: LRCX's 2022-2023 episode
  (-31.4% YoY revenue, Q1 FY2024 vs. Q1 FY2023 specifically) is the
  batch's most severe confirmed figure; this does not by itself establish
  that LRCX would fall furthest in a *future* downturn, only that it did
  in the one well-documented past
  episode found — stated as historical evidence, not a forward
  projection, per this task's explicit instruction to use historical
  evidence only to describe risk, not to create a timing or trading
  signal.

## 13. External opportunity and replacement-candidate scan — batch-level consolidation

Per `PI-0023` SSB.17. Each company's own record and this research pass
surfaced named non-owned competitors; consolidated here as a small,
evidence-supported leads list. **All items below are future-research leads
only** — none is researched as a full company, none is added to holdings,
none is assigned a tier or target, none is ranked, and none authorizes
expanding this batch or beginning research on any of them without its own
separate future authorization, per `PI-0023` SSB.17 and SSF's explicit
prohibitions.

| Candidate | Possible economic role | Competes against |
|---|---|---|
| Tokyo Electron (TEL) | Etch/deposition/coater-developer-track equipment maker, named as a direct competitor to both AMAT and LRCX (and holding some track-related business neither AMAT nor LRCX directly competes in) | Would represent duplicate, not new, exposure to the same WFE-cycle driver AMAT/LRCX already provide — the clearest candidate for "duplicate exposure," per PI-0023's own instruction to distinguish genuinely new from duplicate exposure |
| Onto Innovation | Named in KLAC's record as KLA's "closest direct competitor," particularly in packaging-related inspection | Duplicate exposure to KLAC's process-control/inspection role, with a possible narrower differentiation in advanced-packaging-specific inspection — not independently assessed |
| Naura / AMEC (Chinese domestic equipment makers) | Named across AMAT's and LRCX's records as rising competitive threats gaining share in China specifically | Not a portfolio-exposure candidate in the conventional sense (Chinese A-share/red-chip listings with their own distinct regulatory and accessibility considerations, not assessed here) — recorded only as a competitive-erosion risk to AMAT/LRCX's existing thesis, not as an investable lead |

No candidate above is recommended for purchase, tier assignment, or
further research by this document. Any future research on any of them
requires its own separate authorization, per `PI-0023` SSB.17.

## 14. Zero-based discipline note

Per `OPS-0006` SS2/SS3 and `PI-0023` SSC, this comparison was constructed
from the four companies' own independently-researched records, each of
which reasoned its conviction rating from disclosed business/risk evidence
before — not by way of — the companies' existing governed tier/target/
cluster placement (ASML T1 3.35%; AMAT/KLAC/LRCX band 0.75% each; all four
in the `semis` cluster, capped at 25% of book). This document's SS6
comparison table is broadly consistent with `targets.yaml`'s own existing
comment singling out "the equipment (KLAC/LRCX/AMAT)... names crash
hardest" within the wider cluster — recorded here as a consistency
observation against existing doctrine, not as this batch's own independent
re-derivation of that finding (no new correlation scan was run). Any
apparent tension between this batch's evidence and current policy (for
example, ASML's Medium conviction rating alongside its existing T1/3.35%
placement, the batch's highest tier) is recorded as a future reconciliation
question for the still-unauthorized Milestone 7, not resolved or
implemented here.
