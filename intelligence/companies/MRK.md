# MRK — Merck & Co., Inc.

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Merck Company Intelligence record existed). Portfolio
HQ's WS-0005 Milestone 3 Batch 7, alongside `LLY`, `ABBV`, `JNJ`, and `GILD`
("Biopharmaceuticals"). `UNH` and `EQIX` are not part of this batch and
remain uncovered and unauthorized.

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
session** -- see `MRK.yaml`'s `sources[]`.

## Business summary

Merck is an oncology-led pharmaceutical company whose current revenue is
dominated by its Keytruda franchise, pursuing lifecycle extension,
non-oncology launches, and acquisition-driven diversification.

**Q1 2026** worldwide sales were **$16.286 billion**, up **5%** reported and
**3%** excluding foreign exchange. **Keytruda and Keytruda Qlex** sales were
**$8.0 billion**, approximately **49%** of total company sales. Q1 2026 also
included **$525 million** of Winrevair sales and **$1.8 billion** of Animal
Health sales.

## Keytruda concentration and lifecycle extension

Keytruda's share of Q1 2026 sales (~49%) means the company's near-term
results are still tightly linked to one franchise. Merck is actively
extending that franchise's lifecycle rather than treating it as static: the
FDA approved a **Keytruda/Keytruda Qlex plus Welireg** adjuvant regimen in
renal-cell carcinoma in **June 2026**, based on the LITESPARK-022 trial.
This is concrete evidence of combination-strategy execution, not merely a
restated concentration risk.

## Regulatory and pipeline diversification

The FDA approved Merck's oral PCSK9 inhibitor **Lipfendra** — the first
oral PCSK9 inhibitor approved to lower LDL cholesterol — in **July 2026**.
This is a genuinely new diversification asset outside oncology and outside
Merck's existing Winrevair/Animal Health franchises, evidence of pipeline
conversion beyond the core oncology business.

## Internal research versus acquisition dependence

Merck recorded a **$9.0 billion charge for the Cidara acquisition** and
announced a **Terns transaction expected to produce an additional
approximately $5.8 billion one-time charge** — very large, disclosed
one-time costs tied to business-development-driven diversification. This
record does not establish the eventual return on capital from either
transaction; the charges are disclosed as evidence of capital-allocation
scale and risk, not as a verdict on whether the acquisitions will succeed.

## Clinical, manufacturing, and regulatory risks

Beyond the Keytruda/Welireg and Lipfendra approvals described above, this
record's evidence base does not establish a specific manufacturing-capacity
or regulatory-risk claim for Merck distinct from the general patent/
exclusivity question below (unresolved question B7-U001).

## Patent, exclusivity, and replacement-cycle risk

Whether launches and acquired pipeline assets (Winrevair, Animal Health,
Lipfendra, and Cidara/Terns-derived programs) can offset Keytruda
concentration **before its principal exclusivity step-downs** is not
established by a probability-weighted replacement curve in this record's
evidence base (unresolved question B7-U004). Precise product-by-product
patent and exclusivity dates are also not established (B7-U001,
batch-wide).

## Payer, pricing, and regulatory-access exposure

This record's evidence base does not establish a Merck-specific payer- or
pricing-pressure claim distinct from the general regulatory-approval and
lifecycle-extension evidence above; this is a disclosed evidence gap, not a
finding of no payer risk.

## Competitors, substitutes, and shared drivers

Competing oncology regimens and other checkpoint inhibitors are the primary
named competitive set for Keytruda (see
`BATCH7_BIOPHARMACEUTICALS_COMPARISON.md`). This record does not quantify
Merck's relative competitive position from the evidence inspected.

## Disconfirming evidence

- Keytruda represented roughly half of Q1 2026 company sales.
- Underlying Q1 2026 growth was only 3% excluding foreign exchange.
- Merck incurred very large one-time acquisition charges ($9.0 billion
  Cidara, ~$5.8 billion expected Terns) in pursuit of diversification.
- The replacement thesis remains dependent on clinical, regulatory, and
  commercial execution that has not fully played out.

## Thesis-break conditions

A thesis-break condition would include failure to replace Keytruda
economics before material exclusivity erosion, poor returns on the large
Cidara/Terns acquisitions, or repeated clinical/regulatory failure in the
franchises meant to replace Keytruda's eventual decline. This is an
analytical condition, not a forecast.

## Unresolved questions

- **B7-U001** (batch-wide): precise product-by-product patent and
  exclusivity dates, including for Keytruda, are not established.
- **B7-U004** (MRK-specific): whether launches and acquired pipeline assets
  can offset Keytruda concentration before the principal exclusivity
  step-downs is not established by a probability-weighted replacement
  curve. Required follow-up: build a dated franchise-replacement bridge
  using patent tables, launch forecasts, and phase-adjusted pipeline
  evidence in a future review.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, MRK currently sits in the **band** tier (0.75% target
weight, 1.25x cap). MRK is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Freshness and next-review requirements

Research cutoff: **2026-07-27**. Known unavailable material: Merck's Q2
2026 results were scheduled for 2026-08-04 and were not available by the
cutoff. Next review due **2026-10-25** (90-day cadence), or sooner on
publication of Q2 2026 results or any material Keytruda exclusivity or
Cidara/Terns integration development.
