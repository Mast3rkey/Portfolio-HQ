# WS-0005 Milestone 3 — WDC/Sandisk Comparison

**WDC (governed, new coverage) paired with Sandisk (candidate-only, not
governed).** Authorized by
`governance/decisions/PI-0032-ws0005-milestone3-remaining-governed-holdings-and-sandisk-candidate.md`
Section B (WDC research) and Section C (the required WDC/Sandisk
comparative artifact). Created 2026-07-28, alongside WDC's own Company
Intelligence record (`intelligence/companies/WDC.yaml`,
`intelligence/companies/WDC.md`).

## What this document is and is not

This is a hand-authored, one-time comparison artifact — not a generated
report, not a Company or Theme Intelligence record under
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema (it introduces no new
schema and is not scanned by `intelligence_validator.py` or any other
validator), and not an authoritative record any allocator or policy
decision may read. It sits at `intelligence/` root, matching
`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` through
`intelligence/BATCH9_OIL_CLUSTER_COMPARISON.md`'s own placement and scope,
though it is deliberately **not** named `BATCH10` — `PI-0032` itself
distinguishes this genuine, structurally-evidenced WDC/Sandisk pairing
from the "no fabricated shared comparison" prohibition it applies to the
five unrelated CEG/BRK.B/WMT/MLM/AAPL units. **It does not rank WDC and
Sandisk, does not recommend a tier/target/cluster/cap change, a
buy/trim/exit, a margin action, or a next-best-alternative ranking, and
does not create a composite score of any kind** — per `PI-0032` Section C's
explicit instruction and the Constitution's standing prohibition on
predictive research or opportunity maps.

## Sandisk classification — restated exactly as `PI-0032` Section C binds it

This entire document treats Sandisk under six explicit, repeated
constraints, matching `PI-0032` Section C's own five-way repetition
discipline:

1. **Candidate research only** — Sandisk is examined exactly as a
   prospective external candidate, never as a current or presumed-future
   holding.
2. **Outside the governed 62-company (T1/T2/ETF/band/spec, ex-crypto)
   coverage denominator** — Sandisk's coverage or non-coverage does not
   affect any Milestone 3 completion criterion (`PI-0031` Section K),
   including criterion 4 — that criterion is scoped to governed holdings
   only, and Sandisk was never a governed holding.
3. **Not a Milestone 3 completion prerequisite** — Milestone 3 may reach
   its future completion determination whether or not this comparison, or
   any Sandisk research, exists or reaches any particular conclusion.
4. **Not a holding** — confirmed absent from `holdings.yaml` (no `shares:`
   row) and `targets.yaml` (no tier, cluster, or crypto-sleeve entry) this
   session, independently re-verified before drafting.
5. **Not assigned any governed tier, target, weight, or capital
   priority** — no `portfolio_role_ref` value implying governed status is
   used anywhere for Sandisk in this document or in any file this
   implementation creates; Sandisk receives no Company Intelligence YAML
   or Markdown record, and no freshness-registry or freshness-checkpoint
   row, under this authorization.
6. **Not authorized for purchase** — nothing in this document authorizes a
   trade, buy, allocation, or `holdings.yaml`/`targets.yaml` change of any
   kind, regardless of what this comparison finds.

## Source-access disclosure (applies to this whole document)

WDC facts below are drawn from `intelligence/companies/WDC.yaml`/`WDC.md`,
themselves built from a principal-supplied, checksum-verified
primary-source evidence bundle
(`WDC_SANDISK_PRIMARY_SOURCE_EVIDENCE_RECOVERY_20260728_v2.yaml`, SHA-256
`f4093c9b78d7260ba78ff7c64e7a98b6e26cbb4f3ae955e59feef7f729ce8ef5`,
independently re-verified this session by hash recomputation and direct
YAML re-parse) after this Claude session's own `WebFetch` was confirmed
blocked session-wide (HTTP 403 on SEC EDGAR and a neutral control domain,
`example.com`). Sandisk facts below are drawn from the **same** evidence
bundle's `SNDK-S1` through `SNDK-S4` sources and `SNDK-C##`/`CMP-C##`
claims — both companies' evidence in this document share one bundle and
one evidence-recovery standard, unlike the `BATCH9_OIL_CLUSTER_COMPARISON.md`
precedent, whose two companies' records were built to different,
non-contemporaneous evidence standards. The bundle's own disclosed
limitation applies throughout: raw source documents were not embedded in
the bundle (URLs, accessions, dates, sections, and claim reciprocity were
retained and independently re-verified; underlying filing text was not
re-read by this session). No price-correlation coefficient was computed
for this document — WDC and Sandisk are not members of any existing
`targets.yaml` correlated-cluster cap together (Sandisk is not a governed
holding at all; WDC's own `semis` cluster does not include Sandisk),
so unlike `BATCH9`'s XOM/CVX comparison, there is no existing cluster
correlation figure this document could even reference.

## 1. Post-separation business boundaries

On 2025-02-21, Western Digital completed the separation of its Flash/NAND
business into Sandisk Corporation, which began independent Nasdaq trading
under ticker `SNDK` on 2025-02-24 via a pro rata distribution. [WDC-C01,
SNDK-C01] **WDC retained the HDD business in full; Sandisk retained the
Flash/NAND business in full** — the evidence bundle's claim set does not
disclose any continuing transitional supply agreement, revenue-sharing
arrangement, or cross-ownership stake between the two companies following
separation. This is recorded as an evidence gap, not asserted as an
absence of any relationship — the bundle simply does not address whether
transitional agreements exist.

## 2. HDD (WDC) versus NAND/flash (Sandisk) economics

WDC emphasizes HDD cost-per-capacity and total-cost-of-ownership for
mass, high-capacity storage; Sandisk emphasizes NAND/SSD performance,
power efficiency, form factor, and latency-sensitive applications. [CMP-C01]
WDC manufactures substantially all recording heads and magnetic media
in-house, sourcing remaining HDD components externally. [WDC-C04] Sandisk's
manufacturing model is structurally different and more constrained: it
obtains **substantially all** flash-memory wafers through Flash Ventures
(its 49.9%-owned joint ventures with Kioxia), pays half of Flash Ventures'
fixed costs **regardless of purchased output**, and can be required to
fund roughly half of approved joint-venture capital investments. [SNDK-C05,
SNDK-C06] **This is a materially different capital-intensity and
fixed-cost-exposure profile than WDC's own disclosed model** — WDC's
evidence base states no comparable joint-venture cost-sharing obligation.

## 3. Complementary and substitutive storage use cases

The two technologies can be complementary in tiered storage
architectures (HDD for capacity/cost-optimized tiers, flash for
performance-optimized tiers), but they are also substitutes in some
workloads and compete for portions of the same customer storage budgets.
[CMP-C02] WDC's own 10-K names NAND-flash suppliers as indirect
competitors — including, notably, its own former Flash business, now an
independently operated competitor. [WDC-C05]

## 4. Cloud, hyperscaler, enterprise, OEM, and consumer demand exposure

| | WDC | Sandisk |
|---|---|---|
| End markets served | Cloud, Client, Consumer [WDC-C02] | Cloud, Client, Consumer [SNDK-C03] |
| FY2025 Cloud/Datacenter share | 88% of revenue [WDC-C06] | $960M of $7.355B total revenue (~13%) [SNDK-C08] |
| Most recent inspected quarter Cloud/Datacenter growth | +48% YoY (36% higher exabytes, 9% higher ASP/exabyte) [WDC-C07] | Datacenter +645% YoY (160% higher exabytes, 186% higher ASP/gigabyte) [SNDK-C13] |
| FY2025 top-customer concentration | Top ten 68%; three customers 17/12/10% [WDC-C06] | No customer >10%; top ten 40% [SNDK-C10] |
| Most recent quarter top-customer concentration | Top ten 71%; three customers 17/15/11% [WDC-C08] | Not stated in the evidence bundle for the most recent quarter |

**WDC's Cloud business is a much larger share of its total revenue than
Sandisk's Datacenter business is of Sandisk's total revenue, but Sandisk's
Datacenter growth rate is far more explosive off a smaller base, and
Sandisk's customer concentration (by the FY2025 figures available for
both) is meaningfully lower than WDC's.** [CMP-C04] This is a real,
evidenced structural difference, not a matter of degree only.

## 5. AI and data-growth sensitivity — evidence for and against, not assumed

Both companies are exposed to cloud and AI-related data growth, but
**neither company's own filings, nor the evidence bundle's synthesis,
treats that demand driver as eliminating pricing, qualification,
competition, or technology risk.** [CMP-C03] For WDC: Cloud revenue growth
and margin expansion are real and evidenced, but the bundle's own
uncertainty claim states this strength remains exposed to concentration,
pricing, qualification-cycle, and demand-volatility risk. [WDC-C14] For
Sandisk: Datacenter revenue growth is even more dramatic (+645% YoY), but
Sandisk's own filings disclose material NAND-cycle risk — excess supply
can drive price declines, underutilization, inventory write-downs, and
investment impairment — and the bundle's own uncertainty claim states
Sandisk's current earnings strength is highly sensitive to NAND pricing,
customer mix, long-term-agreement economics, capacity investment, and
Kioxia alignment. [SNDK-C11, SNDK-C19] **Neither company's AI/data-growth
exposure is evidence that either company's current growth rate is a new
durable state** — this document does not draw that inference for either.

## 6. Pricing and supply cycles

WDC's most recent quarter shows a 9% higher average selling price per
exabyte alongside 36% higher exabyte volume — both price and volume moved
favorably together. [WDC-C07] Sandisk's most recent quarter shows a far
larger ASP move (186% higher ASP per gigabyte) alongside 160% higher
exabyte volume in Datacenter specifically — an even larger simultaneous
price-and-volume expansion. [SNDK-C13] Sandisk's own filings separately
disclose that this level of pricing strength is not guaranteed to persist:
the FY2026 Q3 release's own $5.95B revenue and 78.4% GAAP gross margin was
attributed by management to mix shift and pricing, with the evidence
bundle's own caveat that "one quarter's unusually strong pricing and mix
should not be treated as normalized earnings power." [SNDK-C18] **The same
caution applies, by the same logic, to WDC's own recent margin expansion**
— this document extends Sandisk's own disclosed caveat to WDC symmetrically,
since WDC's evidence base does not itself state an equivalent caveat but
the underlying risk (a single strong pricing quarter is not necessarily a
new baseline) is structurally the same for both companies.

## 7. Capital intensity and manufacturing dependencies

WDC's capital model: substantially self-manufactured recording heads and
magnetic media, externally sourced remaining components, and capital
expenditures generally expected at 4%-6% of revenue. [WDC-C04, WDC-C12]
Sandisk's capital model is structurally different and more
joint-venture-dependent: 49.9% ownership of each Flash Ventures entity
with Kioxia, entitlement to roughly half of joint-venture output,
responsibility for half of Flash Ventures' fixed costs regardless of
purchased output, potential obligation to fund roughly half of approved
Flash Ventures capital investments, and — as of the most recently
inspected quarter — an extension of all three Flash Ventures through 2034
alongside a new $1.2 billion commitment to Kioxia for manufacturing
services and continued supply availability during 2026-2029. [SNDK-C05,
SNDK-C06, SNDK-C16] **This is a materially larger and more specific
forward capital commitment than anything disclosed in WDC's own evidence
base.** No overlap with this portfolio's already-covered `semis`-cluster
equipment names (ASML, AMAT, KLAC, LRCX, per `PI-0023`) was identified in
either company's evidence base — neither WDC nor Sandisk names any of
those four equipment makers as a supplier or dependency in the sources
inspected for this comparison.

## 8. Customers, competitors, and substitutes

WDC competes directly with Seagate and Toshiba (HDD) and indirectly with
NAND-flash suppliers, including Sandisk itself. [WDC-C05] Sandisk competes
with vertically integrated NAND suppliers: Kioxia (also its Flash Ventures
partner), Micron, Samsung, SK hynix, and YMTC. [SNDK-C04] **Sandisk names
five direct competitors, one of which (Kioxia) is simultaneously its
essential manufacturing joint-venture partner — a dual
competitor/dependency relationship that has no analog in WDC's own
disclosed competitive structure**, where WDC's direct competitors
(Seagate, Toshiba) are not also disclosed manufacturing partners.

## 9. Correlated-loss and duplicate-exposure risk

Both companies' earnings show recent strength tied to the same broad
demand driver (cloud/hyperscale storage buildout, plausibly AI-adjacent),
but through economically distinct mechanisms — WDC through HDD
capacity/cost economics, Sandisk through NAND/SSD performance economics
and a joint-venture-dependent supply structure. [CMP-C01, CMP-C05] Owning
both would diversify storage-technology exposure but would **not**
eliminate correlated-loss risk from cloud capital spending, storage
pricing cycles, inventory corrections, and technology transitions — both
companies' filings independently name cyclicality/demand-volatility and
technology-transition risk as material. [CMP-C05, WDC-C14, SNDK-C11,
SNDK-C12] **A broad cloud-capex slowdown would be expected to pressure
both companies' Cloud/Datacenter revenue simultaneously, even though the
underlying products (HDD versus NAND) are technically distinct** — this is
the correlated-loss mechanism most clearly supported by the evidence, more
significant than any shared-customer or shared-supplier relationship
identified in this comparison (none was identified).

## 10. Whether Sandisk would provide a distinct role or duplicate cyclical storage exposure — open question, evidence on both sides

**Evidence favoring "genuinely distinct":** Sandisk's product category
(NAND/SSD) and demand drivers (latency-sensitive, performance-oriented
workloads) are technically different from WDC's HDD capacity/cost
economics [CMP-C01]; Sandisk's FY2025 customer concentration (no customer
above 10%) is materially lower than WDC's own most recent concentration
figures (top three customers at 43% combined) [SNDK-C10, WDC-C08]; and
Sandisk's Flash Ventures/Kioxia structure is a distinct risk and
dependency profile not present anywhere in WDC's own evidence base
[SNDK-C05 through SNDK-C07, SNDK-C16].

**Evidence favoring "duplicated cyclical storage exposure":** both
companies' most recent quarters show extraordinary, likely
not-fully-normalized pricing and volume strength in the same
cloud/hyperscale demand environment [WDC-C07, WDC-C09, SNDK-C13,
SNDK-C18]; both disclose structural cyclicality and technology-transition
risk as material [WDC-C14, SNDK-C11, SNDK-C12]; and a severe, broad
cloud-capex pullback would plausibly compress both companies'
highest-growth segment simultaneously, even without a direct product
substitution mechanism (§9).

**This document does not resolve this question and is not authorized to.**
[CMP-C06] Per the evidence bundle's own judgment claim: Sandisk research
may justify future policy consideration only if its NAND/SSD role improves
portfolio function after accounting for cycle risk, Kioxia dependence, and
overlap with existing semiconductor exposure — **the evidence assembled
here does not itself justify opening a position, and this document does
not recommend one.** [CMP-C06]

## 11. Zero-based comparison against WDC and the next-best use of capital

Per `OPS-0006` Sections 2-3 and `PI-0032` Section C.11, four distinct
questions are separated here, none of which this document resolves with a
ranking or score:

**(a) Sandisk's business quality on its own economic merits:** Sandisk
shows a focused NAND/flash manufacturer with dramatic recent Datacenter
revenue growth, materially expanding gross margin, low FY2025 customer
concentration, real liquidity ($3.735B cash, $4.545B nine-month operating
cash flow), and a large, actively-funded $6.0B repurchase authorization.
[SNDK-C13, SNDK-C14, SNDK-C17, SNDK-C18] It also carries a structurally
more constrained, joint-venture-dependent manufacturing model with
material, name-specific counterparty risk (Kioxia) that WDC's own model
does not share. [SNDK-C05 through SNDK-C07, SNDK-C16]

**(b) Sandisk's portfolio fit if it were ever considered:** would add
NAND/flash-specific exposure and a materially lower disclosed customer
concentration than WDC, but would also add joint-venture/counterparty
concentration risk (Kioxia) that has no current analog anywhere in this
portfolio's evidence base, including within the governed `semis` cluster.

**(c) Capital priority relative to WDC and other governed alternatives:**
**not resolved by this document.** A reviewer weighting Sandisk's lower
customer concentration and higher current growth rate more heavily could
reasonably view it as attractive on business-quality grounds alone; a
reviewer weighting the Flash Ventures/Kioxia dependency, the single-quarter
nature of both companies' current pricing strength (§6), and Sandisk's
complete absence of any current governed-portfolio role could reasonably
conclude no capital-priority comparison is even appropriate yet. **Both
views are evidence-supported; neither is declared here**, and per
`CMP-C07`, current strong results for both companies should be normalized
across a full storage cycle before any future capital-priority comparison
is attempted. [CMP-C07]

**(d) WDC's own current governed policy:** unchanged by this document —
WDC remains **band** tier, 0.75% target, member of the governed `semis`
cluster, exactly as `WDC.yaml`/`WDC.md` record as existing policy, not a
research conclusion.

## Summary (advisory, not a ranking)

This document completes the WDC/Sandisk pairing `PI-0032` Section C
authorized: WDC (newly covered, governed `semis`-cluster holding) and
Sandisk (candidate-only, non-governed) share a genuine, disclosed
structural relationship — a February 2025 corporate separation — but now
operate economically distinct businesses (HDD capacity/cost economics
versus NAND/SSD performance economics with a joint-venture-dependent
manufacturing structure) that are neither fully complementary nor fully
substitutive, and that currently both show strong, likely
not-fully-normalized, cloud/hyperscale-driven growth. **This document does
not rank WDC and Sandisk, does not recommend any tier, target, cluster,
cap, holding, allocator, trade, or margin action for either company, and
does not conclude whether Sandisk deserves future policy consideration** —
that remains an open question the evidence here presents both sides of, per
§10 and §11(c) above, and Sandisk remains, throughout, exactly as bounded
above: candidate-only, outside the governed coverage denominator, not a
Milestone 3 prerequisite, not a holding, not assigned any tier/target/
weight, and not authorized for purchase. Any future step addressing
Sandisk's governed status requires its own separate, later, explicit
governance decision naming Sandisk specifically.
