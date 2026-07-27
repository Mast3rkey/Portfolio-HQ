# MSFT — Microsoft Corporation

Last updated: 2026-07-26 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0027-ws0005-milestone3-batch5-hyperscaler-ai-infrastructure.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Microsoft Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 5, alongside `GOOGL`, `META`, and `AMZN`
(`EQIX` explicitly deferred, not part of this batch).

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-26 were blocked
(HTTP 403) on SEC EDGAR (every endpoint tested: `browse-edgar`,
`data.sec.gov`, `efts.sec.gov`, and direct `/Archives/edgar/data/...`
document paths) and on a non-target control domain (`example.com`), matching
the pattern already disclosed in Batches 1-4's own records. **Two**
`microsoft.com/investor` pages were the exception -- they rendered directly
for this session (the FY2026 Q3 earnings-release page and the general
investor-relations landing page) -- but Microsoft's FY2025 Form 10-K itself,
any Form 10-Q, any 8-K, and any antitrust-specific primary document were not
reached directly by this session. Per `OPS-0008` Section 2's mandatory
stop-before-drafting gate, this session paused before drafting, produced
`BATCH5_SOURCE_READINESS_MANIFEST.md`, and the principal supplied an
independent evidence-recovery audit performed by **GPT-5.6 Thinking**
(2026-07-26). The original delivered predecessor audit had SHA-256
`98d00c3c73805177c8301c680dee8dc06eee1b5caff5d4f250d13519051ab909` (the
"as-delivered" hash); this session first independently verified that hash
against the two uploaded copies, then, following the precedent already
established for Batch 4's own retained audits
(`governance/audits/PR166_PRIMARY_SOURCE_AUDIT_20260726.md` and
`PR166_CORRECTED_HEAD_REVIEW_20260726.md`), normalized trailing Markdown
hard-line-break whitespace in the retained repository copy only (no
substantive content changed -- confirmed by a whitespace-collapsed diff
against the as-delivered file) to clear this repository's `git diff --check`
CI gate. GPT-5.6 Thinking subsequently reissued this CI-clean text as the
canonical retained audit, and the repository contains that **canonical
inspector reissue** at
`governance/audits/BATCH5_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260726.md`,
SHA-256 (`1ce03813cc3b855d8643708e56063653342476435cebafaf2f4b97ffd0f64ff7`)
-- intentionally different from the as-delivered hash because of the
whitespace normalization, not a discrepancy; only Markdown trailing
whitespace differed from the predecessor artifact, and substantive evidence
text did not change. This session
also independently verified the audit's own cited checksum of
`BATCH5_SOURCE_READINESS_MANIFEST.md`
(`8a9e943e0f189ea83d2c89fd34fdb263bd0c23ee49f9b49a2a81e08cc033a211`) matches
this session's own manifest file, before relying on the audit's content.
**Every fact below not explicitly attributed to this session's own two
successful `microsoft.com` fetches was directly inspected by GPT-5.6
Thinking, not by this Claude session** -- see `MSFT.yaml`'s `sources[]` for
per-document attribution.

## Business summary

Microsoft reports in three segments. Fiscal 2025 (year ended 2025-06-30):
total revenue **$281.724 billion**, operating income **$128.528 billion**,
net income **$101.832 billion**.

| Segment | FY2025 revenue | FY2025 operating income |
|---|---|---|
| Productivity and Business Processes | $120.810B | $69.773B |
| Intelligent Cloud | $106.265B | $44.589B |
| More Personal Computing | $54.649B | $14.166B |

**Productivity and Business Processes** covers Microsoft 365, LinkedIn, and
Dynamics. **Intelligent Cloud** covers Azure and other cloud services --
Azure grew **34%** in FY2025 and accelerated to **40% YoY (GAAP)** in FY2026
Q3 (quarter ended 2026-03-31); FY2026 Q3 Microsoft Cloud revenue was **$54.5
billion, +29% YoY**. **More Personal Computing** covers Windows, gaming
(Xbox), and devices/search advertising.

**FY2026 Q3** (per Microsoft's own earnings release, directly fetched by
this session): revenue **$82.9 billion**, operating income **$38.4
billion**, net income **$31.8 billion**.

## AI monetization and infrastructure

Management stated on the FY2026 Q3 call that Microsoft's AI business
exceeded a **$37 billion annual revenue run rate, up 123% YoY**. **This is
an issuer-defined management metric, not a separately audited reportable
segment** -- treated here as a real, disclosed, growing signal, not as
GAAP-equivalent disclosure comparable to segment revenue.

FY2026 Q3 capital expenditures were **$31.9 billion**; management stated
roughly two-thirds related to short-lived assets, primarily GPUs and CPUs.
Management guided to **more than $40 billion** of Q4 FY2026 capex and
**approximately $190 billion** for calendar 2026 -- **forward-looking
management estimates, not realized facts**.

Management stated Azure demand continued to **exceed available capacity**
and expected capacity constraints to persist **through at least 2026** --
this is management's own operational assessment, and it cuts two ways: it
signals real, unmet demand, but it also means already-signed demand cannot
be fully converted into near-term recognized revenue.

**Custom silicon** (issuer transcript claims, not independently benchmarked
by this record): Maia 200 AI accelerators live in Iowa and Arizona
datacenters; Cobalt CPUs deployed in nearly half of Microsoft's datacenter
regions; custom networking, security, and virtualization silicon supporting
millions of servers.

## OpenAI relationship

Microsoft's FY2025 Annual Report states Microsoft and OpenAI have a
long-term strategic partnership dating to 2019, with **reciprocal
revenue-sharing arrangements**, **rights to OpenAI intellectual property**
for integration into Microsoft products, **Azure exclusivity for the OpenAI
API**, and a **right of first refusal on new OpenAI capacity needs**. This
is simultaneously a structural competitive advantage (a contractually
secured, deeply integrated AI-model relationship most competitors lack) and
a concentration/complexity risk (a single, unusually deep counterparty
dependency). FY2026 Q3 GAAP results included the impact of Microsoft's
OpenAI investment; the earnings release separately presented non-GAAP
results excluding that effect -- the accounting impact is large enough to
warrant its own standing non-GAAP carve-out, which this record treats as
evidence of real financial entanglement, not merely a footnote.

## Capital allocation and balance sheet

At 2025-06-30: cash, cash equivalents, and short-term investments totaled
**$94.6 billion**. FY2025 property-and-equipment additions were **$64.551
billion** (up from $44.477 billion in FY2024). FY2025 common-stock
repurchases were **$13.0 billion** and cash dividends paid were **$24.082
billion**. At 2025-06-30, Microsoft had **$32.1 billion** of commitments for
construction, building improvements, and leasehold improvements, primarily
related to datacenters. **This record could not independently establish
Microsoft's total debt or net-debt position** -- the inspected sources cover
cash/investments and capex/commitments but not a full balance-sheet debt
figure; treated as an open evidence item, not assumed zero or immaterial.

## Regulatory evidence

On **2026-06-25**, the European Commission announced a **preliminary**
view that Azure (and, separately, AWS) should be designated Digital Markets
Act gatekeepers for cloud services, citing gateway importance, user-base
entrenchment, lock-in, high switching costs, ecosystem breadth, and AI
tools/partnerships. **This is a regulator preliminary finding, not a final
adjudicated designation** -- its eventual scope and any remedies, if
finalized, are not established by any source this record relies on. **No
U.S. antitrust primary document specific to Microsoft was inspected by
either this session or the evidence-recovery audit** -- this is a disclosed
evidence gap, not an assertion that no such exposure exists.

## Risks -- detail

**AI-capex-driven cloud-margin pressure**, already disclosed, not merely
feared: Microsoft Cloud gross margin was **69% in FY2025**, with
year-over-year pressure attributed partly to scaling AI infrastructure
(partly offset by Azure efficiencies) -- and management is guiding to an
even larger calendar-2026 capex figure (~$190B) funded predominantly from a
business whose own cloud margin is already under disclosed pressure from
the same buildout.

**Azure capacity constraint** -- demand exceeding available capacity,
expected to persist through at least 2026, can delay revenue realization
independent of underlying demand durability.

**OpenAI concentration/complexity** -- see above; a single AI-model
relationship this deep is unusual among Microsoft's peers and creates a
counterparty dependency this record cannot fully evaluate the downside of
without more evidence than the audit provides.

**EU DMA cloud-gatekeeper exposure** -- preliminary, not final; a real,
current, but unresolved regulatory matter.

**Evidence-completeness gap** -- no standalone Form 10-K/10-Q as filed with
the SEC and no U.S. antitrust primary document specific to Microsoft was
directly inspected by either this session or the evidence-recovery audit.
No customer represented more than 10% of Microsoft's FY2025 revenue per the
inspected annual-report disclosure, but specific supplier concentration
(e.g., dependence on NVDA, AMD, or TSM capacity) was not quantified in any
source this record relies on -- do not infer the absence of supplier
concentration from the customer-concentration disclosure, which is a
different fact.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, MSFT currently sits in the **T1** tier (3.35% target
weight per name). MSFT is **not** a member of any `targets.yaml`
correlated-cluster cap (`semis`, `power_infra`, or `oil`). This placement is
recorded here as **existing governed policy, preserved as a historical
comparison baseline only, per `OPS-0006` Sections 2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion in
this record, and this record does not recommend any change to it.

## Capital-priority discipline (business quality vs. capital priority)

**Business quality**, per the evidence above, is strong: diversified,
already-profitable growth across three segments; a real, growing, disclosed
AI monetization signal; balance-sheet strength sufficient to fund a large
capex buildout without acute financial strain evident in the record; and a
structurally secured (if concentrated) AI-model relationship.

**Capital priority is a separate question.** MSFT already carries the
largest single-name weight of any T1 holding by tier design (3.35%, same as
every other T1 name). As a structural, unconfirmed relationship
hypothesis relevant to future portfolio mapping -- not an established
fact -- Microsoft's own AI-infrastructure buildout is plausibly connected to
other already-covered governed holdings: NVDA/TSM/AMD (general-industry-
knowledge GPU/CPU supply for AI infrastructure and accelerator use),
AVGO/MRVL (networking-adjacent infrastructure demand), and GEV (electrical
power-generation demand growth partly driven by hyperscaler datacenter
buildout, a mechanism also named in Microsoft's own capex disclosures). **The
retained evidence does not quantify or confirm any specific Microsoft
supplier share or dependence on NVDA, TSM, AMD, AVGO, MRVL, or GEV, and this
record does not present these as verified bilateral relationships.**
**What would be lost if MSFT were absent from the book:** the specific
combination of enterprise-productivity-software economics (Microsoft 365,
LinkedIn, Dynamics -- a subscription-revenue base none of GOOGL/META/AMZN
directly replicates) plus a public-cloud business with a uniquely deep,
contractually formalized frontier-AI-lab partnership. GOOGL and AMZN both
offer public-cloud exposure as a substitute in kind, but neither carries
Microsoft's specific enterprise-productivity-software franchise or its
specific OpenAI relationship structure. **Whether the next investment
dollar favors MSFT over GOOGL or AMZN (the two other public-cloud sellers
in this batch) is not resolved by this record** -- MSFT shows the most
complete evidence base of the four (an annual report, a quarterly earnings
release this session independently corroborated, and a call transcript) and
the most diversified segment mix, but GOOGL's Google Cloud segment is
already profitable at the segment-operating-income level with faster
disclosed growth (63% YoY vs. Microsoft Cloud's 29% YoY), a genuinely
different comparison than a simple business-quality ranking would suggest.
This record preserves that uncertainty rather than resolving it, and
recommends no tier, target, or allocation change.

## Margin-relevant evidence (factual/advisory only -- no leverage recommendation)

- **Liquidity:** $94.6 billion cash/short-term investments at 2025-06-30 --
  a large liquidity buffer relative to disclosed near-term capex
  commitments ($32.1 billion of construction/leasehold commitments).
- **Capital intensity:** rapidly rising -- FY2025 capex $64.551B (+45% YoY
  from $44.477B), FY2026 Q3 capex $31.9B, with $40B+ guided for Q4 and
  ~$190B guided for full calendar 2026. This record could not confirm
  whether that spending is funded entirely from operating cash flow or
  partly from incremental debt.
- **Debt/leverage:** not established by any source this record relies on --
  a genuine, disclosed evidence gap, not an assumption of low leverage.
- **Cyclicality/drawdown history:** not established by any source this
  record relies on -- no historical drawdown data was inspected or
  reproduced here (contrast with Batch 4's ETN/GEV/VRT/PWR records, which
  did include documented historical drawdown figures from prior research
  passes; this batch's evidence-recovery audit did not cover that ground
  for any of the four companies).
- **Correlated-loss relevance:** MSFT's AI-capex trajectory is one of the
  shared mechanisms named in the Batch 5 comparison artifact as a common
  risk across MSFT/GOOGL/META/AMZN, and indirectly connects to the
  already-governed `semis` cluster (NVDA/TSM/AVGO/AMD/MRVL and others) via
  shared exposure to an AI-capex slowdown.

## Thesis-break conditions (this record's own synthesis, labeled as inference)

- Azure/Microsoft Cloud growth decelerating materially, especially if
  accompanied by evidence that the AI-capex buildout is not converting into
  proportional revenue growth.
- Cloud gross margin compression proving structural rather than a
  temporary function of capacity-ramp costs.
- A material adverse development in the OpenAI relationship (renegotiated
  exclusivity, a dispute over IP rights or revenue-sharing terms, or a
  competing hyperscaler securing a comparable frontier-lab relationship).
- The EU DMA cloud-gatekeeper matter finalizing with material
  interoperability, data-portability, or structural remedies for Azure.
- Evidence that the $37B AI annual-revenue-run-rate metric was materially
  overstated relative to how it converts into GAAP segment revenue over
  subsequent quarters.

## Non-owned competitor/replacement candidates (unauthorized future research leads only)

Named as public-cloud and enterprise-software competitors across the
sources this record relies on and general industry knowledge: AWS (Amazon,
covered in this same batch), Google Cloud (Alphabet, covered in this same
batch), Oracle Cloud Infrastructure, Salesforce (enterprise
software/productivity adjacency). **These are noted as future research
leads only, per `PI-0027` Section B.18 -- no holding add, tier assignment,
ranking, or further research is authorized by naming them here.**

## Review framework

- **Cadence: 90 days** -- justified independently by Microsoft's own
  evidence-refresh triggers, not adopted solely because other records use
  the same interval: Microsoft reports quarterly (the next FY2026 Q4 release
  falls within this window), the EU DMA cloud-gatekeeper matter is a live
  preliminary proceeding that can move on a comparable timeframe, and the
  OpenAI relationship's standing non-GAAP carve-out is large enough to
  warrant at least quarterly re-inspection. This happens to match the
  cadence used for GEV, COST, XOM, and Batch 4's ETN/VRT/PWR records, but
  that consistency is incidental to, not the basis for, this record's own
  cadence choice.
- **Named review triggers**, drawn selectively from `OPS-0006` Section 12's
  candidate-trigger list:
  - Quarterly earnings releases, specifically watching whether Azure
    capacity constraints ease and whether Cloud gross margin stabilizes or
    continues compressing.
  - The European Commission's final DMA cloud-gatekeeper determination.
  - Any material change to the OpenAI partnership terms (exclusivity,
    revenue-sharing, IP rights) or to Microsoft's own disclosed AI
    annual-revenue-run-rate metric's growth trajectory.
  - Full calendar-2026 capex realization against the ~$190B guide.

## Conviction

**Rating: High.**

**Rationale:** Microsoft shows diversified, already-profitable growth
across all three reporting segments, a real (not purely narrative) AI
monetization signal, and balance-sheet strength sufficient to fund a large
capex buildout without financial strain evident in the record. Conviction
is held at High rather than Very High because of concrete, current,
evidence-based tensions: disclosed cloud-gross-margin compression
specifically attributed to AI-infrastructure scaling; an Azure capacity
constraint that can delay revenue realization independent of underlying
demand; an unusually deep, complex, and financially entangled OpenAI
relationship large enough to require its own non-GAAP carve-out; and a
live, though still preliminary, EU DMA cloud-gatekeeper regulatory
exposure. This rating excludes valuation, entry-price, allocation, trading,
and margin judgments, and does not treat forward-looking capex or AI-run-rate
guidance as realized fact.

This rating and rationale reflect human judgment, approved after
independent review of AI-assisted research -- the research and drafting
process does not itself constitute the human judgment this record
requires; the approval decision does.

## Unresolved items and access limitations

- No primary document was directly opened by **this Claude session** except
  two `microsoft.com/investor` pages (the FY2026 Q3 earnings-release page
  and the general investor-relations landing page). The FY2025 Annual
  Report, the FY2026 Q3 call transcript, and the EU Commission statement
  were inspected by GPT-5.6 Thinking during an independent evidence-recovery
  audit, not by this session -- see Source-access disclosure above.
- No standalone Form 10-K/10-Q as filed with the SEC was inspected by
  either this session or the audit.
- No U.S. antitrust primary document specific to Microsoft was inspected.
- Microsoft's total debt/net-debt position was not established.
- Historical drawdown/cyclicality data was not established.
- Specific supplier concentration (dependence on NVDA, AMD, or TSM
  capacity) was not quantified in any inspected source.
- The precise economics of the OpenAI non-GAAP carve-out (its dollar
  magnitude) were not extracted from the inspected sources.

## Sources

See `MSFT.yaml`'s `sources[]` for the structured register. All entries
except the FY2026 Q3 earnings-release page (directly fetched by this
Claude session) are sourced to GPT-5.6 Thinking's independent
evidence-recovery audit, with that provenance stated explicitly.
