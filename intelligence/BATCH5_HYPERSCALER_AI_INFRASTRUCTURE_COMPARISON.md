# WS-0005 Milestone 3, Batch 5 — Hyperscaler AI Infrastructure Comparison

**MSFT, GOOGL, META, AMZN.** Authorized by
`governance/decisions/PI-0027-ws0005-milestone3-batch5-hyperscaler-ai-infrastructure.md`
Section C (comparison requirements) and Section I (completion criteria
requiring this evidence be retained), applying
`governance/decisions/OPS-0008-research-wave-protocol-v1.md` without
modification. Created 2026-07-26, alongside the four companies' own Company
Intelligence records (`intelligence/companies/{MSFT,GOOGL,META,AMZN}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema (it
introduces no new schema and is not scanned by `intelligence_validator.py`
or any other validator), and not an authoritative record any allocator or
policy decision may read. It sits at `intelligence/` root, matching
`BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`, `BATCH2_MEMORY_COMPARISON.md`,
`BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`, and
`BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md`'s own placement and scope.
**It does not rank the four companies, does not recommend a tier/target/
cluster change, a buy/trim/exit, a margin action, or a next-best-alternative
ranking, and does not create a composite score of any kind** — per `PI-0027`
Section C's explicit instruction and the Constitution's standing prohibition
on predictive research or opportunity maps.

**Source-access disclosure (applies to this whole document).** This Claude
Code session's own direct `WebFetch` attempts on 2026-07-26 were blocked
(HTTP 403) on SEC EDGAR and on every GOOGL/META/AMZN investor-relations
domain tested; two `microsoft.com/investor` pages were the one exception.
Per `OPS-0008` Section 2's mandatory stop-before-drafting gate, drafting
paused and an independent evidence-recovery audit performed by **GPT-5.6
Thinking** (2026-07-26) was supplied by the principal. The original
delivered predecessor audit had SHA-256
`98d00c3c73805177c8301c680dee8dc06eee1b5caff5d4f250d13519051ab909`,
independently checksum-verified by this session before use; GPT-5.6
Thinking subsequently reissued a canonical CI-clean copy (only Markdown
trailing whitespace differed from the predecessor artifact -- substantive
evidence text did not change), and the repository contains that canonical
inspector reissue at
`governance/audits/BATCH5_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260726.md`,
SHA-256 `1ce03813cc3b855d8643708e56063653342476435cebafaf2f4b97ffd0f64ff7`. **Every
fact below is inherited from the four companies' own Company Intelligence
records**, each of which discloses its own per-source attribution — this
document adds no new primary research of its own. Consistent with `OPS-0006`
Section 4's distinction between structural/economic overlap and measured
historical price correlation, **no price-correlation coefficient was
computed for this document** — every correlation-relevant statement below is
about shared economic drivers, not measured historical return correlation.

## 1. Common economic mechanism

All four companies share direct, disclosed exposure to the current AI
capital-expenditure supercycle — each is either building AI infrastructure
to sell to third parties (MSFT, GOOGL, AMZN) or to power its own products
(META, and secondarily all four for internal use), and each has disclosed
large infrastructure capital-expenditure commitments, though not on a
uniformly comparable basis: GOOGL and AMZN each disclose an explicit
quarter-over-quarter-year capex comparison showing roughly a doubling;
MSFT discloses a FY2025-vs-FY2024 property-and-equipment-additions increase
(a different period and definition) alongside large separate forward
guidance; META discloses a large guided full-year 2026 range without a
directly comparable prior-year actual in this batch's evidence base (see
Section 3 below for the full figures and caveats). This is the
batch's own governing rationale, matching `PI-0027`'s selection of these
four as the companies closing the remaining Company Intelligence coverage
gap in CLAUDE.md's documented "7-of-9 T1 AI-infrastructure names" finding
(ASML/TSM/NVDA/GEV already covered; MSFT/GOOGL/META now covered by this
batch, completing that finding's own Company Intelligence coverage — see
Section 8 below).

## 2. Public-cloud sellers versus no disclosed cloud-resale business — a real structural split, not a labeling exercise

| Company | Public-cloud business? | Q1 2026 (or FY2026 Q3 for MSFT) cloud/relevant segment revenue | Segment operating income |
|---|---|---|---|
| MSFT | Yes — Azure/Intelligent Cloud | Microsoft Cloud $54.5B (FY2026 Q3), +29% YoY; Azure +40% YoY | Intelligent Cloud FY2025 $44.589B (full-year; Q3-specific segment OI not separately extracted) |
| GOOGL | Yes — Google Cloud | $20.028B (Q1 2026), +63% YoY | $6.598B |
| AMZN | Yes — AWS | $37.587B (Q1 2026), +28% YoY | $14.161B |
| META | **No public-cloud-resale business disclosed** | N/A | N/A — no public-cloud-resale business was disclosed in the inspected evidence; the currently evidenced recovery path depends primarily on Meta's own advertising, applications, devices, and platform economics |

**This is the single clearest structural finding in this batch, matching
`PI-0027`'s own framing.** MSFT, GOOGL, and AMZN disclose customer-facing
cloud businesses that can, at least in principle, recover their
AI-infrastructure capital expenditure by selling compute capacity to
third-party customers; no public-cloud-resale business was disclosed in
the inspected evidence for META. The currently evidenced recovery path for
META's entire AI capex guide ($125B–$145B for 2026, per META.yaml)
depends primarily on Meta's own advertising, applications, devices, and
platform economics; this document does not claim that every possible
Meta external-monetization path is permanently closed, only that none was
disclosed in the sources it relies on. On the facts disclosed, this is not
a matter of degree — it is a different business model, and this document
does not flatten the four into a single "Big Tech" category.

Among the three public-cloud sellers, **AWS reported more disclosed
quarterly segment operating income than Google Cloud in the compared
quarter** ($14.161B Q1 2026 AWS versus $6.598B Q1 2026 Google Cloud). **The
retained Microsoft evidence does not provide a directly comparable
quarterly Azure or Microsoft Cloud operating-income figure** (only a
FY2025 full-year Intelligent Cloud segment operating-income figure and a
Q3 revenue figure without a separately extracted Q3 segment operating
income) — so a three-company cloud-profitability ordering cannot be
established from this batch's evidence base. Separately, **Google Cloud is
growing fastest** on disclosed revenue (+63% YoY vs. Azure's +40% YoY and
AWS's +28% YoY) from a smaller base. No company in this batch discloses a
directly comparable, apples-to-apples cloud segment margin percentage
across all three in this record's evidence base.

## 3. AI-capital-expenditure funding source and trajectory versus revenue growth

| Company | Most recent disclosed capex | YoY change / composition note | Guided/forward figure |
|---|---|---|---|
| MSFT | $31.9B (FY2026 Q3) | not established in comparable quarterly form (see composition note below) | >$40B guided Q4 FY2026; ~$190B guided calendar 2026 |
| GOOGL | $35.7B (Q1 2026) | up from $17.2B (Q1 2025) — more than doubled | significant further 2026 increase expected (not quantified) |
| META | $19.84B (Q1 2026, incl. finance-lease principal) | — | $125B–$145B guided full-year 2026 |
| AMZN | $43.2B (Q1 2026 cash capex) | up from $24.3B (Q1 2025) — nearly doubled | technology/infrastructure spend expected to keep rising (not quantified) |

*Composition note on MSFT: management stated approximately two-thirds of
this capex is short-lived (GPUs/CPUs), per the FY2026 Q3 earnings call —
an asset-mix disclosure, not a year-over-year change figure.*

**These figures are not directly comparable without normalization** — they
cover different periods (a fiscal quarter for MSFT/GOOGL/META/AMZN, but
MSFT's fiscal year ends in June, so "Q3" spans a different calendar window
than the others' Q1), different definitions (META's includes finance-lease
principal payments; AMZN's is specifically "cash" capex; MSFT's FY2025
figure is "property and equipment additions"), and this document does not
rank the four by capex size. **The retained evidence does not establish a
uniform "AI-specific portion" capex-growth-versus-revenue-growth
relationship for all four companies** — no company in this batch isolates
an AI-specific capex figure or growth rate distinct from total capex, so
this document does not claim that comparison as proven. What the evidence
does support, stated separately per company: **GOOGL and AMZN each have an
explicit Q1 year-over-year capex comparison in the retained evidence**, and
both roughly doubled quarterly capex year over year; **MSFT's and META's
year-over-year or forward-guided figures are not established in directly
comparable form** in this batch's evidence base (MSFT's own FY2025-vs-FY2024
comparison uses a different period/definition than a quarterly figure, and
META's evidence gives a current-quarter actual plus a full-year guidance
range without a comparable prior-year actual). Across all four, the
better-supported characterization of the shared risk is: **large and
accelerating, or guided-large, infrastructure capital commitments with
uncertain monetization timing** — not a proven capex-growth-exceeds-
revenue-growth relationship. META's guided range is the widest (a $20B
spread), reflecting the greatest disclosed planning uncertainty of the
four.

## 4. Custom-silicon strategy and dependency on external chip suppliers

| Company | Disclosed custom-silicon program | External chip-supplier disclosure |
|---|---|---|
| MSFT | Maia 200 (AI accelerator, live in Iowa/Arizona datacenters), Cobalt (CPU, ~half of datacenter regions) — issuer transcript claims, not independently benchmarked | Not quantified in this batch's evidence base |
| GOOGL | TPU — limited external-supply agreements disclosed, revenue recognition expected late 2026/2027; some agreements include credit backstops for third-party datacenter/power infrastructure | Not quantified |
| META | **No equivalent primary evidence established** — MTIA's scale/economics could not be confirmed by this batch's evidence-recovery audit; not asserted here | Not quantified |
| AMZN | Trainium/Inferentia not named explicitly in this batch's evidence base — AWS-chip performance obligations are disclosed within the OpenAI and Anthropic commercial arrangements, without further product-line specificity in the sources this batch relies on | Not quantified |

**Cross-reference against already-covered semis-cluster companies (NVDA,
TSM, AVGO, AMD, MRVL, ASML, AMAT, KLAC, LRCX, MU, SKHY).** This batch's
evidence base does **not** independently confirm or quantify any specific
supplier relationship between any of MSFT/GOOGL/META/AMZN and any of those
already-covered names — Batch 1 and Batch 3's own records previously named
MSFT/GOOGL/META/AMZN as hyperscaler *customers* of those semis-cluster
companies without independent verification from the customer side; **this
batch's own research does not resolve that cross-reference either.** This
remains a disclosed, unresolved evidence gap on both sides of the
relationship, consistent with `OPS-0006` Section 4's distinction between
structural/economic overlap (plausible, and consistent with general
industry knowledge that hyperscalers are large GPU/AI-accelerator
purchasers) and independently measured or confirmed evidence (not
established here).

## 5. Advertising, cloud, retail, and enterprise-software revenue concentration

| Company | Largest revenue driver | Approximate concentration |
|---|---|---|
| MSFT | Diversified across three segments (Productivity/Business Processes, Intelligent Cloud, More Personal Computing) | No single segment exceeds ~43% of FY2025 revenue (Productivity and Business Processes $120.810B of $281.724B) |
| GOOGL | Advertising | ~70% of Q1 2026 revenue ($77.253B of $109.896B) |
| META | Advertising | ~98% of Q1 2026 revenue ($55.024B of $56.311B) — the most concentrated of the four |
| AMZN | Diversified (retail, marketplace, advertising, subscriptions, AWS) | Online stores are the largest single line (~35% of Q1 2026 net sales) but no line dominates as heavily as META's advertising share |

**META's concentration is a structural outlier in this batch** — no other
company approaches its ~98% single-revenue-stream share. MSFT and AMZN are
both genuinely diversified across multiple large, distinct revenue drivers;
GOOGL sits between the two, with advertising still the largest revenue driver but Cloud now a
material and growing secondary driver.

## 6. Antitrust and regulatory exposure — correlated or company-specific?

| Company | Matter(s) | Current status |
|---|---|---|
| MSFT | EU DMA cloud-gatekeeper preliminary position (Azure) | Preliminary, not final (2026-06-25) |
| GOOGL | Search-distribution case (DOJ, 2020) + ad-tech case (DOJ, 2023) | Search: final judgment Dec 2025, under appeal by both sides. Ad-tech: adverse liability finding (Apr 2025), remedies proceedings ongoing, possible structural remedy |
| META | FTC personal-social-networking monopolization case | District court ruled **in Meta's favor** Nov 2025; FTC appealed Jan 2026 — allegation continues on appeal |
| AMZN | FTC/state marketplace-monopolization litigation + EU DMA cloud-gatekeeper preliminary position (AWS) | Litigation active, allegation stage; DMA preliminary, not final |

**This exposure is partly correlated (a shared U.S./EU regulatory
environment increasingly scrutinizing large technology platforms) and
partly company-specific in severity and posture.** GOOGL currently carries
the most severe disclosed exposure — an adverse liability finding with a
possible structural remedy still pending, on top of a separate final
judgment under active cross-appeal. AMZN's litigation remains at the
allegation stage. META currently holds a favorable trial-level result,
notwithstanding the FTC's appeal. MSFT and AMZN share the same specific EU
DMA cloud-gatekeeper preliminary matter (GOOGL and META do not appear in
that specific EU proceeding in this batch's evidence base — this record
does not assert GOOGL or META are exempt from EU platform regulation
generally, only that this specific DMA cloud-gatekeeper preliminary
position, as sourced, names Azure and AWS, not Google Cloud). **No source
in this batch's evidence base quantifies the probability or dollar
magnitude of any eventual remedy for any of the four matters.**

## 7. Genuine diversification versus duplicated exposure

**Among the batch's four companies:** MSFT, GOOGL, and AMZN duplicate each
other to a real degree as public-cloud sellers competing for the same
enterprise AI-infrastructure spending — this is the batch's clearest
overlap. META is the outlier: no public-cloud-resale business was
disclosed in the inspected evidence, so on the facts gathered it does not
directly compete with the other three for cloud-infrastructure customers,
even though all four compete for the same underlying AI-capex
supercycle's benefits in different ways (selling capacity vs. using it
internally). Within the three cloud sellers, AWS's scale/profitability, Azure's
enterprise-software-bundled distribution (via Microsoft 365/Dynamics), and
Google Cloud's TPU-based differentiation each represent a genuinely
different competitive approach, not three identical businesses measured
three ways.

**Against already-covered supply-side semis-cluster names:** this batch's
evidence base does not establish enough specific, confirmed supplier
detail to state whether holding all four hyperscalers alongside the
existing semis-cluster names (NVDA, TSM, AVGO, AMD, MRVL, ASML, AMAT, KLAC,
LRCX, MU, SKHY) constitutes genuine diversification (demand-side vs.
supply-side exposure to the same AI-capex cycle) or a duplicated bet on the
same underlying cycle viewed from two different value-chain positions.
Structurally, demand-side (hyperscaler) and supply-side (chip/equipment
maker) exposure to the same capex cycle are economically distinct
positions — a hyperscaler slowing its own capex is a different event than a
chip supplier losing a specific customer contract — but both would be
expected to respond, to some degree, to the same underlying AI-capex-cycle
health. This record does not attempt to resolve that question further; it
is squarely a Milestone 4 (portfolio relationship mapping) question, which
remains unauthorized.

## 8. Coverage-completion observation (advisory only, per PI-0027 Section C.8)

Completing MSFT, GOOGL, and META's coverage in this batch closes the
Company Intelligence coverage gap CLAUDE.md's own Decisions Log entry
"T1 AI-infra cluster cap: scanned and declined" identified: of the 7-name
AI-infrastructure subset that entry scanned (ASML, TSM, NVDA, MSFT, GOOGL,
META, GEV), 4 already carried coverage before this batch (ASML, TSM, NVDA,
GEV); this batch adds the remaining 3 (MSFT, GOOGL, META), bringing that
specific 7-name group to full Company Intelligence coverage. **This is an
advisory research observation only, with no automatic effect on any tier,
target, or cluster** — the original CLAUDE.md entry declined a
correlation-based cluster cap for that group on evidentiary grounds
(0.302–0.373 average pairwise correlation, well below the semis/power_infra/
oil caps' thresholds), and nothing in this batch re-tests that correlation
finding or reopens that decision. Any actual policy consequence of full
coverage now existing requires its own separate, later, explicit governance
decision.

## 9. Common correlated-loss mechanisms across the batch and against already-covered semis-cluster names

The single most consistently named, cross-company thesis-break condition in
this batch's four company records is a **sustained AI-capital-expenditure
slowdown or pause** — each of MSFT, GOOGL, META, and AMZN names a version of
this condition independently in its own record. Beyond that shared macro
driver, this batch's evidence base did not establish a second,
independent, confirmed correlated-loss mechanism binding all four together
— e.g., no shared customer relationship, no shared supplier relationship,
and no shared financing counterparty was confirmed across all four records
(the OpenAI and Anthropic relationships are shared between MSFT/AMZN and
AMZN respectively, not all four). Company-specific amplifiers differ
materially in kind: GOOGL's and AMZN's are principally regulatory/legal
(active antitrust litigation); META's is principally structural
(concentration + no cloud-resale offset); MSFT's is principally
relationship-specific (OpenAI concentration).

## 10. Capital-priority comparison across all four companies (advisory prose only, per PI-0027 Sections B.23/C.10)

**This section separates business quality from capital priority and
compares the four against each other and against the next-best use of
capital among this repository's other governed holdings — it produces no
score, index, or ranking, consistent with Section G's prohibition.**

All four companies show real business-quality strength on the evidence
gathered: profitable, growing core franchises and large, disclosed
AI-infrastructure commitments. GOOGL disclosed a $31.1B senior-notes
issuance in Q1 2026 and AMZN disclosed $121.8B of unsecured senior notes
outstanding at 2026-03-31, including major U.S.-dollar and euro issuances
in March 2026 -- both occurring in the same reporting period as elevated
capex, but this record does not establish use of proceeds or a causal
funding relationship between the debt and the AI-infrastructure spending
for either company. **The four do not compete for capital priority in a
uniform way** — MSFT, GOOGL, and META share the same 3.35% T1 target
weight and so compete for T1's overall capital-priority ranking on equal
per-name terms by tier design, while AMZN's existing T2 placement (1.65%)
already reflects half that per-name conviction weight as governed
historical policy, not a research conclusion this batch draws independently.

**Where redundancy exists:** MSFT, GOOGL, and AMZN duplicate each other
most directly as public-cloud sellers (Section 2, 7 above) — an investor
already holding meaningful exposure to one of the three public-cloud
businesses is, to a real degree, already exposed to the same
AI-infrastructure-demand economics the other two also capture, even though
each company's non-cloud business (MSFT's enterprise software, AMZN's
retail/logistics, GOOGL's advertising) remains genuinely distinct. **META
is the least redundant with the other three** on a business-model basis
(no public-cloud-resale business disclosed in the inspected evidence, no
comparable retail/logistics or enterprise-software franchise), even
though it shares the same underlying AI-capex-cycle risk.

**Why the next investment dollar might, or might not, favor one of the
four over another or over an already-covered alternative:** GOOGL's
evidence base shows the most severe currently-disclosed regulatory
exposure (an adverse ad-tech liability finding with a possible structural
remedy); META's shows the most concentrated business-model risk (~98%
single revenue stream, no public-cloud-resale business disclosed to
offset its AI capex); AMZN's shows the
most complex AI-lab financial-commitment structure (OpenAI plus Anthropic
disclosed arrangements spanning a $100B expanded commercial arrangement, a
$15B equity investment plus a conditional $35B commitment, a $5B Anthropic
preferred-stock investment, a potential $20B financing facility, and an
option for up to $5B more equity — listed separately rather than summed,
since these categories overlap and are not economically interchangeable,
and no single additive total is established) alongside the most specific
disclosed total-debt figure of the four; MSFT's evidence base is the most
complete (an annual report, an
earnings release this session's own research independently corroborated,
and a call transcript) and shows the most segment diversification, but
carries its own concrete tension in the depth and complexity of its OpenAI
relationship. **None of these observations resolves into a preferred
holding** — each is a real, evidence-based distinction preserved here as
uncertainty and judgment, not collapsed into a ranking. Any actual
capital-priority decision among these four, or between any of them and
another governed holding, remains a human judgment exercised through the
existing tier/target framework, not an output of this document.

## Summary (advisory, not a ranking)

MSFT, GOOGL, META, and AMZN complete first-coverage Company Intelligence
research for the entire remaining CLAUDE.md-documented 7-name AI-infrastructure
concentration group (Section 8) and add the fourth major hyperscaler (AMZN)
already cited, unverified, across three prior batches' own records. The
batch's clearest structural finding is the public-cloud-seller /
no-disclosed-cloud-resale split (Section 2): MSFT, GOOGL, and AMZN
disclose customer-facing cloud businesses that can in principle recover
AI-infrastructure capex by selling capacity to third parties; no
public-cloud-resale business was disclosed in the inspected evidence for
META, whose currently evidenced recovery path for its entire, very large
capex guide depends on internal product and advertising improvements.
This document does not claim that every possible Meta external-monetization
path is permanently closed, only that none was disclosed in the sources it
relies on. Each
company carries its own, company-specific set of disclosed risks and
evidence gaps, documented individually in `MSFT.yaml`/`.md`,
`GOOGL.yaml`/`.md`, `META.yaml`/`.md`, and `AMZN.yaml`/`.md`. **This
document does not rank the four companies, does not recommend any tier,
target, cluster, cap, holding, allocator, trade, or margin action, and does
not alter any existing Intelligence record.** Any future use of this
evidence — for Milestone 4 relationship mapping, for a policy
reconsideration, or for any other purpose — requires its own separate,
later, explicit governance authorization. `EQIX` remains deferred and
uncovered by this batch.
