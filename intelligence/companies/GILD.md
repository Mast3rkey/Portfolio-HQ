# GILD — Gilead Sciences, Inc.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Gilead Sciences Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 7, alongside `LLY`, `ABBV`, `MRK`,
and `JNJ` ("Biopharmaceuticals"). `UNH` and `EQIX` are not part of this
batch and remain uncovered and unauthorized.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were tested
and confirmed blocked (HTTP 403) on SEC EDGAR and on a neutral, non-target
control domain (`example.com`), confirming a session-wide network-policy
denial, matching the pattern already disclosed in this repository's Batch
1-6 records.

The governing implementation authorization supplied
`BATCH7_biopharmaceuticals_evidence_bundle_20260727_v2.yaml`, authored by an
independent evidence-recovery researcher. This session independently
verified the bundle's SHA-256
(`cff7bc37920e829cd5521128b9fa11019e65a650ce20726f9beea818c8f3a826`) against
both uploaded copies, and its measurements (1227 lines, 5659 words, 56667
bytes) before use. The bundle is a frozen, principal-custodied
implementation input, not committed to this repository. **Every fact below
was directly inspected by the bundle's author, not by this Claude
session** -- see `GILD.yaml`'s `sources[]`.

## Business summary

Gilead is an HIV-centered pharmaceutical company pursuing oncology, cell
therapy, and liver-disease diversification, partly through acquisition.

**Q1 2026** revenue was **$7.0 billion**; product sales excluding Veklury
were **$6.8 billion, up 8%**. **HIV product sales were $5.0 billion**,
including **$3.4 billion from Biktarvy** -- roughly **72%** of total
quarterly revenue.

## HIV franchise concentration

HIV's ~72% share of Q1 2026 revenue means Gilead's near-term results remain
tightly linked to that franchise's continued durability. This record does
not independently assess future HIV competitive dynamics beyond noting the
concentration as a structural fact.

## Oncology and cell-therapy performance -- mixed, not uniform

Q1 2026 **cell-therapy sales declined 12% to $407 million**, including a
**14% decline in Yescarta**, while **Trodelvy grew 37% to $402 million**.
This is a genuinely mixed picture: one named oncology diversification
engine (cell therapy) contracted while another (Trodelvy) grew in the same
quarter. Neither trend alone supports a conclusion that oncology
diversification is succeeding or failing overall.

## Pipeline execution and regulatory conversion (F-5 disposition)

The FDA approved **Hepcludex** for chronic hepatitis delta, per an FDA
announcement titled "FDA Approves First Treatment for Chronic Hepatitis
Delta Virus (HDV) Infection." **This record scopes that approval as the
first U.S.-approved treatment for chronic hepatitis delta** -- it does not
state or imply Hepcludex was the first approval worldwide, since the FDA's
own announcement establishes only a U.S. regulatory-approval claim. The
FDA also approved expanded **Trodelvy** indications (monotherapy and in
combination with pembrolizumab) for first-line triple-negative breast
cancer in 2026 -- further evidence of pipeline assets converting into
approved, revenue-relevant indications.

## Acquired-asset dependence and impairment risk

Gilead reduced 2026 EPS guidance by approximately **$9.50** for anticipated
**$11.5 billion** of acquired IPR&D and financing costs related to
**Arcellx, Ouro, and Tubulis** -- a very large, disclosed near-term earnings
and capital burden. This record does not establish the eventual clinical
or economic return on these acquisitions; the guidance reduction is
disclosed as evidence of capital-allocation scale and near-term earnings
impact, not as a verdict on the acquisitions' eventual success.

## Capital returns and balance-sheet use

At Q1 2026 end, Gilead reported **$8.6 billion** of cash, equivalents, and
marketable securities. During the quarter it **repaid $2.8 billion of
debt, paid $1.0 billion of dividends, and repurchased $419 million of
stock** -- disclosed evidence of active balance-sheet management and
capital return occurring in the same period as the large acquired-IPR&D
charges above.

## Pricing and exclusivity exposure

This record's evidence base does not establish a Gilead-specific payer- or
net-pricing claim for the HIV franchise beyond the 8% product-sales growth
figure above; precise patent and exclusivity dates for Biktarvy and other
HIV products are not established (unresolved question B7-U001,
batch-wide).

## Manufacturing and capacity requirements

This record's evidence base does not establish a specific manufacturing-
capacity claim for Gilead; this is a disclosed evidence gap, not a finding
of no capacity constraint.

## Competitors, substitutes, and shared drivers

Competing HIV regimens, oncology antibody-drug conjugates, and cell
therapies are the primary named competitive set for Gilead (see
`BATCH7_BIOPHARMACEUTICALS_COMPARISON.md`). This record does not quantify
Gilead's relative competitive position from the evidence inspected.

## Disconfirming evidence

- HIV remains the dominant source of revenue (~72% of Q1 2026 total).
- Cell-therapy sales and Yescarta specifically declined in Q1 2026 amid
  competitive headwinds.
- The acquisition program creates large acquired-IPR&D charges (~$11.5
  billion anticipated) and real execution risk.
- Oncology diversification remains uneven -- Trodelvy growth alongside
  cell-therapy contraction -- despite new approvals.

## Thesis-break conditions

A thesis-break condition would include loss of HIV franchise durability
without offsetting launches, continued cell-therapy contraction, or poor
clinical and economic returns from the large acquired pipeline assets
(Arcellx, Ouro, Tubulis). This is an analytical condition, not a forecast.

## Unresolved questions

- **B7-U001** (batch-wide): precise product-by-product patent and
  exclusivity dates, including for Biktarvy, are not established.
- **B7-U006** (GILD-specific): whether oncology and cell therapy will
  become durable second engines relative to HIV is not established.
  Required follow-up: track launch uptake, competitive share, Phase 3
  readouts, and acquired-asset milestones in future reviews.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, GILD currently sits in the **band** tier (0.75% target
weight, 1.25x cap). GILD is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Capital priority and next-dollar considerations

**Business quality**, per the evidence above, shows a large, currently
growing HIV franchise (product sales excluding Veklury +8% in Q1 2026),
meaningful balance-sheet strength with active concurrent capital return
(debt repayment, dividends, and buybacks in the same quarter as large
acquisition spending), and real 2026 regulatory conversion (Hepcludex,
expanded Trodelvy indications).

**Capital priority is a separate question, and GILD's own current band
placement (0.75% target, 1.25x cap) -- the same tier as ABBV, MRK, JNJ,
and the uncovered UNH -- is itself a data point this record preserves as
historical policy, not evidence.** GILD's distinct exposure within this
batch is the only antiviral/HIV-concentrated franchise -- a different
mechanism from ABBV's immunology transition, MRK's oncology concentration,
and JNJ's multi-segment structure. **What would be lost if GILD were
absent:** exposure to the batch's most singularly concentrated (~72% of
Q1 2026 revenue) base franchise, which on this record's evidence is also
currently growing (+8% ex-Veklury), plus its demonstrated capacity to
fund both capital return and acquisition-driven diversification
concurrently.

**Factors that could support greater capital priority** include the HIV
franchise's demonstrated durability and current growth, the concurrent
capital-return-and-acquisition-investment capacity, and real regulatory
conversion in two separate therapeutic areas (liver disease and oncology)
in the same year. **Factors favoring an alternative use of capital**
include GILD's own disclosed concentration -- the highest single-franchise
revenue share among this batch's five companies -- a real, current
contraction in one named diversification engine (cell therapy, Yescarta
-14%), the largest near-term earnings and capital burden of the five
(~$9.50 EPS reduction for ~$11.5 billion of anticipated Arcellx/Ouro/
Tubulis-related costs) whose eventual clinical and economic return this
record's evidence base does not establish, and the unresolved question of
whether oncology/cell therapy will become a durable second engine
(B7-U006). A holding with a demonstrated, rather than still-emerging,
second engine -- or with lower single-franchise concentration -- could
reasonably be favored by a reviewer weighting diversification more heavily
than current cash-generation strength.

**UNH redundancy/mechanism check (required by `PI-0029`):** UNH is a
band-tier (0.75%), currently uncovered holding whose economic mechanism is
managed-care/payer economics -- fundamentally different from GILD's
branded-pharmaceutical-franchise-and-pipeline economics. This record does
not create new UNH research, does not assign UNH any conviction, quality,
tier, target, or capital-priority judgment, and does not claim GILD is
better or worse than UNH. A fully evidenced capital comparison between
GILD and UNH must abstain until UNH receives its own governed Company
Intelligence coverage.

Business quality and portfolio capital priority are separate judgments.
This record does not determine the governed target: GILD's current band
tier and 0.75% target remain binding, this Intelligence record does not
change them, and a final next-dollar decision requires portfolio-wide
comparison and principal approval.

## Freshness and next-review requirements

Research cutoff: **2026-07-27**. Known unavailable material: Gilead's Q2
2026 full results were not available by the cutoff per the governing
evidence bundle. Next review due **2026-10-25** (90-day cadence), or sooner
on publication of Q2 2026 results or any material HIV, cell-therapy, or
Arcellx/Ouro/Tubulis integration development.
