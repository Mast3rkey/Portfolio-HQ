# LLY — Eli Lilly and Company

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Eli Lilly Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 7, alongside `ABBV`, `MRK`, `JNJ`, and `GILD`
("Biopharmaceuticals"). `UNH` and `EQIX` are not part of this batch and remain
uncovered and unauthorized.

## Source-access disclosure

This Claude Code session's own `WebFetch` attempts on 2026-07-27 were tested
and confirmed blocked (HTTP 403) on SEC EDGAR and on a neutral, non-target
control domain (`example.com`) used specifically to test whether the block
was domain-specific or session-wide -- the control domain failed identically,
confirming a session-wide network-policy denial. This matches the pattern
already disclosed in this repository's Batch 1-6 records.

The governing implementation authorization (a principal-issued, corrective-
validated evidence bundle) supplied `BATCH7_biopharmaceuticals_evidence_bundle_20260727_v2.yaml`,
authored by an independent evidence-recovery researcher. This session
independently verified the bundle's SHA-256
(`cff7bc37920e829cd5521128b9fa11019e65a650ce20726f9beea818c8f3a826`) against
both uploaded copies, and its `LC_ALL=C.UTF-8 wc -l -w -c` measurements
(1227 lines, 5659 words, 56667 bytes) before use. The bundle is a frozen,
principal-custodied implementation input -- it is not committed to this
repository, per the authorizing instruction. **Every fact below was directly
inspected by the bundle's author, not by this Claude session** -- see
`LLY.yaml`'s `sources[]` for per-document attribution.

## Business summary

Eli Lilly is a pharmaceutical company whose current growth is concentrated
in its cardiometabolic incretin (GLP-1) franchise, alongside a broader
multi-therapeutic pipeline in immunology, oncology, and neuroscience.

**Q1 2026** revenue was **$19.8 billion, up 56%** year over year -- primarily
volume-driven, and *partly offset by lower realized prices* for Mounjaro and
Zepbound. Incretin revenue grew **90%** in the quarter, and Lilly's defined
key products generated **$13.4 billion, or 68%** of quarterly revenue.
Zepbound alone was **$4.2 billion**, up 80%, with a management-reported
**60.1%** U.S. incretin prescription share (IQVIA data -- management-
presented third-party data, cited as such, not independently verified by
this record).

## Pipeline conversion and regulatory approval

The FDA approved **Foundayo**, an oral GLP-1, for chronic weight management
on **2026-04-01** -- the first new molecular entity approved under the FDA's
National Priority Voucher Program. The label carries a boxed warning and
material gastrointestinal, pancreatitis, kidney, gallbladder, aspiration,
and thyroid C-cell tumor precautions. This is real evidence of pipeline
conversion into an approved, commercially relevant product, paired with a
real, disclosed safety and monitoring burden.

## Manufacturing capacity (F-3 disposition)

Lilly's Q1 2026 earnings-call presentation referenced manufacturing-capacity
expansion, including a newly announced Pennsylvania site. **This record does
not assert an exact Wisconsin production-start date.** The underlying bundle
claim (LLY-C005) stated that Lilly "began production at a Wisconsin site
during Q1 2026"; this Claude session's own attempt to independently
re-verify that clause against the primary source (LLY-S04) was blocked by
the network-policy denial described above. Per the bundle's own bounded-
abstention instruction for this finding, this record retains only the
directly supportable fact -- manufacturing capacity is a stated strategic
priority, evidenced concretely by the Pennsylvania site announcement -- and
omits the specific Wisconsin timing assertion. This is a disclosed
evidence-precision limitation, not a claim that no Wisconsin capacity work
is occurring.

## Internal research versus acquisition dependence

Lilly announced agreements during Q1 2026 to acquire **Orna, Centessa,
Kelonia, and Ajax**, while also advancing internal, non-incretin programs in
immunology, oncology, and neuroscience. This shows a pipeline strategy that
combines internal development with active external business development --
this record does not establish what fraction of Lilly's future pipeline
value will originate internally versus through acquisition (see unresolved
questions below).

## Payer, pricing, and regulatory-access exposure

Q1 2026 revenue growth was **partly offset by lower realized prices** for
Mounjaro and Zepbound -- concrete, current evidence of payer/net-price
pressure on the franchise driving most of the company's growth, not a
hypothetical future risk.

## Patent, exclusivity, and replacement-cycle risk

Precise product-by-product U.S. and ex-U.S. patent and regulatory-exclusivity
dates are **not established** in this record's evidence base (unresolved
question B7-U001, batch-wide -- see below). This record does not assert an
exclusivity timeline for the incretin franchise or any other Lilly product.

## Balance-sheet and capital-allocation evidence

The evidence bundle's LLY-series sources did not include a dedicated
balance-sheet/capital-allocation claim beyond the acquisition and
manufacturing-investment evidence above. This record does not assert a
specific cash, debt, or capital-return figure for Lilly and discloses this
as an evidence gap rather than inferring one.

## Competitors, substitutes, and shared drivers

Novo Nordisk and other incretin developers are the primary named competitive
set for Lilly's cardiometabolic franchise (see
`BATCH7_BIOPHARMACEUTICALS_COMPARISON.md` for the batch-wide competitive
and shared-driver mapping). This record does not quantify Lilly's relative
market-share position against Novo Nordisk from the evidence inspected.

## Disconfirming evidence

- Q1 2026 revenue growth was partly offset by lower realized prices for
  Mounjaro and Zepbound.
- The franchise is highly concentrated in incretins and a small number of
  other key products (68% of Q1 2026 revenue).
- Foundayo's label includes a boxed warning and multiple clinically
  significant precautions.
- The growth strategy requires large, concurrent manufacturing investment
  and execution across four separately announced 2026 acquisitions.

## Thesis-break conditions

A thesis-break condition would include sustained erosion of incretin
prescription share or net pricing, a demonstrated manufacturing inability to
meet demand, or a material safety/regulatory setback in the cardiometabolic
franchise. This is an analytical condition derived from the disclosed risk
factors and pricing commentary above, not a forecast that any of these will
occur.

## Unresolved questions

- **B7-U001** (batch-wide): precise product-by-product U.S. and ex-U.S.
  patent and regulatory-exclusivity dates are not established. Required
  follow-up: inspect Lilly's own patent tables directly before stating an
  exact loss-of-exclusivity date for any product.
- **B7-U002** (LLY-specific): how durable are net realized prices and payer
  access for Mounjaro, Zepbound, and Foundayo after launch normalization?
  Current materials disclose pricing pressure and access milestones, but
  long-duration net pricing is not yet observable. Required follow-up:
  track quarterly net-price commentary, rebate accruals, payer coverage,
  and channel inventory in future reviews.
- Wisconsin manufacturing production-start timing (F-3): not independently
  re-verified by this session; omitted from this record's factual claims
  pending direct primary-source access.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, LLY currently sits in the **T1** tier (3.35% target
weight per name). LLY is **not** a member of any `targets.yaml`
correlated-cluster cap (`semis`, `power_infra`, or `oil`). This placement is
recorded here as **existing governed policy, preserved as a historical
comparison baseline only, per `OPS-0006` Sections 2-3's zero-based-research
discipline** -- it is not treated as evidence supporting any conclusion in
this record, and this record does not recommend any change to it.

## Capital priority and next-dollar considerations

**Business quality**, per the evidence above, is genuinely strong on several
dimensions: a fast-growing, still-expanding incretin franchise (Q1 2026
revenue +56%, incretin revenue +90%), a real regulatory conversion into an
approved product (Foundayo) rather than a pipeline promise, and deliberate
pipeline diversification beyond incretins (four announced 2026
acquisitions plus internal immunology/oncology/neuroscience programs).

**Capital priority is a separate question, and LLY's own current T1
placement (3.35%, the book's largest per-name tier weight) is itself a
data point this record preserves as historical policy, not evidence.**
LLY's cardiometabolic/incretin growth exposure is not duplicated by any
other Batch 7 company (ABBV, MRK, JNJ, and GILD each concentrate in a
different franchise -- immunology, oncology, multi-segment, and antiviral
respectively) or by the book's other governed healthcare holdings, ISRG
and TMO (T2, 1.65% each; device/tools economics, not branded-franchise
pipeline economics). **What would be lost if LLY were absent:** the book's
only direct exposure to incretin-class commercial growth at this scale --
the named competitive set (Novo Nordisk and other incretin developers,
see the comparison artifact) is not itself a governed holding, so this
record does not identify a governed substitute for this specific exposure.

**Factors that could support greater capital priority** include LLY's
demonstrated growth rate relative to the rest of the batch, the Foundayo
approval as evidence of pipeline execution, and the four 2026 acquisitions
as evidence of deliberate diversification beyond a single franchise.
**Factors favoring an alternative use of capital** include LLY's own
disclosed concentration (68% of Q1 2026 revenue in a narrow key-product
set that is simultaneously the source of both the growth and the realized-
pricing pressure), Foundayo's boxed-warning safety burden, the simultaneous
execution risk of large manufacturing investment alongside four separate
acquisition integrations in one quarter, and the unresolved batch-wide
patent/exclusivity-timeline question (B7-U001) this record has not
independently verified. A less-concentrated holding -- within this batch
(e.g. JNJ's two-segment structure) or elsewhere in the governed book --
could reasonably be favored by a reviewer weighting concentration risk
more heavily than growth momentum.

**UNH redundancy/mechanism check (required by `PI-0029`):** UNH is a
band-tier (0.75%), currently uncovered holding whose economic mechanism is
managed-care/payer economics -- fundamentally different from LLY's
branded-pharmaceutical-franchise-and-pipeline economics. This record does
not create new UNH research, does not assign UNH any conviction, quality,
tier, target, or capital-priority judgment, and does not claim LLY is
better or worse than UNH. A fully evidenced capital comparison between LLY
and UNH must abstain until UNH receives its own governed Company
Intelligence coverage.

Business quality and portfolio capital priority are separate judgments.
This record does not determine the governed target: LLY's current T1
tier and 3.35% target remain binding, this Intelligence record does not
change them, and a final next-dollar decision requires portfolio-wide
comparison and principal approval.

## Freshness and next-review requirements

Research cutoff: **2026-07-27**. Known unavailable material: Lilly's Q2 2026
full results were not available by the cutoff per the governing evidence
bundle. Next review due **2026-10-25** (90-day cadence), or sooner on
publication of Q2 2026 results, any material safety/label action on
Foundayo or the incretin franchise, or resolution of the Wisconsin
manufacturing-timing question (F-3) via direct primary-source access.
