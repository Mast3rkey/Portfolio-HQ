# JNJ — Johnson & Johnson

Last updated: 2026-07-27 -- record created through AI-assisted research and
drafting under `governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md`
and `governance/decisions/OPS-0008-research-wave-protocol-v1.md`, first-coverage
discipline (no prior Johnson & Johnson Company Intelligence record existed).
Portfolio HQ's WS-0005 Milestone 3 Batch 7, alongside `LLY`, `ABBV`, `MRK`,
and `GILD` ("Biopharmaceuticals"). `UNH` and `EQIX` are not part of this
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
session** -- see `JNJ.yaml`'s `sources[]`.

## Business summary and post-Kenvue structure (F-1 resolution)

Johnson & Johnson operates **two reportable segments: Innovative Medicine
and MedTech.** This structure follows the **August 2023 separation of
Kenvue** (the former Consumer Health business): following completion of
that separation, Johnson & Johnson presented Consumer Health as
discontinued operations and described the continuing company as focused on
**Pharmaceutical** (the company's own then-current term) and **MedTech**.
Current company reporting uses **Innovative Medicine** for the same
continuing pharmaceutical segment -- the source's terminology changed, the
separation structure did not. This record relies on that 2023 corporate-
action release (JNJ-S06) to substantiate why current J&J analysis centers
on Innovative Medicine and MedTech rather than Consumer Health. The source
does not establish any subsequent change in J&J's retained Kenvue stake, if
any, and this record does not assert one.

**Q2 2026** sales were **$16.384 billion** in Innovative Medicine and
**$8.926 billion** in MedTech -- roughly **65%** and **35%** of company
sales -- with operational growth of **6.8%** in Innovative Medicine and
**3.6%** in MedTech.

## JNJ MedTech boundary -- explicit distinction from `life_sciences_tools_medtech`

Portfolio-HQ's existing `intelligence/themes/life_sciences_tools_medtech.yaml`
theme covers **ISRG** (medical/surgical devices) and **TMO** (life-sciences
research tools, diagnostics instrumentation, reagents, and consumables) --
two device/tools businesses selling directly to hospitals, surgeons, labs,
and biopharma companies as their primary economic model.

**J&J MedTech is not assumed interchangeable with that theme.** J&J MedTech
is one segment of a diversified pharmaceutical-and-device conglomerate,
reported alongside and cross-subsidized within the same corporate structure
as Innovative Medicine, with its own distinct Q2 2026 growth rate (3.6%
operational) separate from Innovative Medicine's (6.8%). This record does
not assert that J&J MedTech's customers, revenue model, competitive set, or
risk profile match ISRG's or TMO's, and does not add JNJ to the
`life_sciences_tools_medtech` theme or any theme -- that would require its
own separate governance authorization, outside PI-0029's scope. See
`BATCH7_BIOPHARMACEUTICALS_COMPARISON.md` for the batch-level discussion of
this boundary.

## Innovative Medicine pipeline replacement

Q2 2026 Innovative Medicine growth included **Darzalex, Carvykti, Tecvayli,
Rybrevant/Lazcluze, Tremfya, Spravato, and Caplyta**, while **Stelara**
biosimilar competition created an approximately **760-basis-point**
operational headwind in the same period. This shows pipeline replacement
actively occurring alongside real, large, currently-realized exclusivity
erosion -- not replacement that has already outrun the erosion it is meant
to offset.

## Litigation and regulatory risk (F-4 disposition)

J&J's filings disclose **material product-liability and other litigation**,
including limits on estimating losses beyond amounts accrued. **This record
does not quote or reproduce the filings' specific accrual or
loss-estimation language.** This Claude session's own attempt to
independently re-verify that language against the primary sources (JNJ-S01,
JNJ-S02) was blocked by the network-policy denial described above. Per the
bundle's own bounded-abstention instruction for this finding, this record
preserves only the general, disclosed fact that material product-liability
litigation -- including talc-related matters -- is a real, current risk not
fully estimable beyond disclosed accruals, without overstating or quoting
the specific estimation wording.

## Balance-sheet and capital-allocation evidence

The Q2 2026 earnings presentation reported **$20.8 billion** of cash and
marketable securities, **$49.0 billion** of debt, approximately **$8.7
billion** of year-to-date free cash flow (a non-GAAP measure, estimated as
of 2026-07-15), and **$6.4 billion** of year-to-date dividends -- a
disclosed balance sheet with meaningful liquidity and capital-return
capacity alongside meaningful debt.

## Manufacturing and MedTech capacity needs

This record's evidence base does not establish a specific MedTech
manufacturing-capacity claim beyond the segment revenue and growth-rate
figures above; this is a disclosed evidence gap, not a finding of no
capacity constraint.

## Payer, pricing, and regulatory-access exposure

This record's evidence base does not establish a specific payer- or
pricing-pressure claim for J&J beyond the Stelara biosimilar-erosion
evidence above and the general litigation risk discussed above.

## Patent, exclusivity, and replacement-cycle risk

Stelara's biosimilar erosion (~760 basis points of Q2 2026 operational
headwind) is the clearest currently-realized exclusivity event in this
record's evidence base. Precise product-by-product patent and exclusivity
dates for J&J's other Innovative Medicine products are not established
(unresolved question B7-U001, batch-wide).

## Internal research versus acquisition dependence

This record's evidence base documents internally-driven pipeline
replacement (the named Innovative Medicine products above) but does not
establish a specific acquisition-dependency measure for J&J distinct from
that evidence.

## Competitors, substitutes, and shared drivers

Competing pharmaceutical and medical-device platforms are the primary named
competitive set for J&J across its two segments (see
`BATCH7_BIOPHARMACEUTICALS_COMPARISON.md`). This record does not quantify
J&J's relative competitive position in either segment from the evidence
inspected.

## Disconfirming evidence

- Stelara biosimilar competition created a large reported growth headwind
  (~760 basis points) in Innovative Medicine.
- MedTech's Q2 2026 operational growth (3.6%) trailed Innovative Medicine's
  (6.8%), consistent with the bundle's disclosed note that some MedTech
  categories faced competitive pressure, procedure softness, and China
  volume-based procurement effects.
- Product-liability litigation remains material and, per the filings
  themselves, not fully estimable beyond disclosed accruals.
- The company's diversified two-segment structure can obscure different
  risk and return drivers between Innovative Medicine and MedTech.

## Thesis-break conditions

A thesis-break condition would include inability of new Innovative Medicine
franchises to offset Stelara or other erosion, persistent MedTech
underperformance, an adverse litigation outcome beyond manageable capital
capacity, or poor returns on acquisitions. This is an analytical condition,
not a forecast.

## Unresolved questions

- **B7-U001** (batch-wide): precise product-by-product patent and
  exclusivity dates beyond the disclosed Stelara erosion are not
  established.
- **B7-U005** (JNJ-specific): the financially plausible range of talc and
  other product-liability outcomes is not established from a reliable
  bounded total-outcome figure. Required follow-up: use subsequent 10-Qs,
  court developments, and legal-accrual disclosures in future reviews; do
  not manufacture a range.
- Exact litigation/accrual estimation language (F-4): not independently
  re-verified by this session; not quoted in this record pending direct
  primary-source access.
- Whether J&J's Q2 2026 Form 10-Q (not located as filed by the 2026-07-27
  cutoff) contains material information beyond the inspected Q2 2026
  release and presentation is unresolved until that filing is located and
  inspected.

## Governed policy (existing, not a research conclusion)

Per `targets.yaml`, JNJ currently sits in the **band** tier (0.75% target
weight, 1.25x cap). JNJ is **not** a member of any `targets.yaml`
correlated-cluster cap. This placement is recorded here as **existing
governed policy, preserved as a historical comparison baseline only, per
`OPS-0006` Sections 2-3's zero-based-research discipline** -- it is not
treated as evidence supporting any conclusion in this record, and this
record does not recommend any change to it.

## Freshness and next-review requirements

Research cutoff: **2026-07-27**. Known unavailable material: J&J's Q2 2026
Form 10-Q was not located as filed by the cutoff (latest filed 10-Q
inspected: Q1 2026, supplemented by the directly inspected Q2 2026 release
and presentation). Next review due **2026-10-25** (90-day cadence), or
sooner on filing of the Q2 2026 10-Q, resolution of the F-4 litigation-
language verification question via direct primary-source access, or any
material talc-litigation development.
