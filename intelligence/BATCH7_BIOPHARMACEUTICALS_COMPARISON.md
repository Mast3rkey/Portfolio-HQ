# WS-0005 Milestone 3, Batch 7 — Biopharmaceuticals Comparison

**LLY, ABBV, MRK, JNJ, GILD.** Authorized by
`governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md`
Phase 5 (comparison requirements), applying
`governance/decisions/OPS-0008-research-wave-protocol-v1.md` without
modification. Created 2026-07-27, alongside the five companies' own
Company Intelligence records
(`intelligence/companies/{LLY,ABBV,MRK,JNJ,GILD}.{yaml,md}`).

**What this document is and is not.** This is a hand-authored, one-time
batch comparison artifact — not a generated report, not a Company or Theme
Intelligence record under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema
(it introduces no new schema and is not scanned by `intelligence_validator.py`
or any other validator), and not an authoritative record any allocator or
policy decision may read. It sits at `intelligence/` root, matching
`BATCH1_SEMIS_EQUIPMENT_COMPARISON.md` through
`BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md`'s own placement and scope.
**It does not rank the five companies, does not declare a required
preferred holding, does not recommend a tier/target/cluster change, a
buy/trim/exit, a margin action, or a mechanical capital-priority ranking,
and does not create a composite score of any kind** — per `PI-0029`'s
explicit instruction and the Constitution's standing prohibition on
predictive research or opportunity maps.

**Source-access disclosure (applies to this whole document).** This Claude
Code session's own `WebFetch` attempts on 2026-07-27 were tested and
confirmed blocked (HTTP 403) on SEC EDGAR and on a neutral, non-target
control domain (`example.com`), confirming a session-wide network-policy
denial. The governing implementation authorization supplied the
principal-accepted, independently corrective-validated evidence bundle
`BATCH7_biopharmaceuticals_evidence_bundle_20260727_v2.yaml` (SHA-256
`cff7bc37920e829cd5521128b9fa11019e65a650ce20726f9beea818c8f3a826`; 1227
lines, 5659 words, 56667 bytes; research cutoff 2026-07-27), independently
re-verified byte-for-byte by this session against both uploaded copies
before use. Every fact below is attributed to that bundle's own
directly-inspected primary sources, not to this Claude session's own
document inspection — see each company's `sources[]` for per-claim
attribution.

## Economic role

- **LLY** — concentrated cardiometabolic (incretin/GLP-1) growth franchise
  with a broader multi-therapeutic pipeline.
- **ABBV** — post-Humira immunology franchise (Skyrizi/Rinvoq) with
  neuroscience, oncology, and aesthetics diversification.
- **MRK** — Keytruda-led oncology franchise pursuing lifecycle extension,
  new launches, and acquisition-driven diversification.
- **JNJ** — diversified two-segment platform (Innovative Medicine and
  MedTech) following the 2023 Kenvue separation.
- **GILD** — HIV-centered cash-flow franchise pursuing oncology, cell
  therapy, liver disease, and acquisition-led diversification.

All five share the batch's common mechanism: patented therapeutic
franchises, clinical development, regulatory approval, commercialization,
exclusivity loss, pipeline replenishment, acquisition dependence,
manufacturing capacity, and capital allocation. Concentration takes a
different form in each: Lilly in incretins; AbbVie in Skyrizi/Rinvoq-led
immunology; Merck in Keytruda; J&J across Innovative Medicine plus MedTech;
Gilead in HIV.

## Franchise concentration

| Company | Named concentration | Share of recent quarterly revenue |
|---|---|---|
| LLY | Incretins / key products | 68% of Q1 2026 revenue |
| ABBV | Skyrizi + Rinvoq (immunology) | $6.602B of $15.002B Q1 2026 revenue (~44%) |
| MRK | Keytruda + Keytruda Qlex | ~49% of Q1 2026 sales |
| JNJ | Innovative Medicine (segment-level, not single-product) | 65% of Q2 2026 sales |
| GILD | HIV (Biktarvy-led) | ~72% of Q1 2026 revenue |

GILD and LLY show the highest single-franchise concentration by this
measure; JNJ's concentration is segment-level rather than single-product,
which is a structurally different form of concentration (see the MedTech
boundary discussion below).

## Major replacement burden and exclusivity/biosimilar exposure

- **ABBV** has already substantially executed its replacement burden:
  Skyrizi plus Rinvoq revenue is several times Humira's current residual
  run-rate.
- **JNJ** is mid-replacement: Stelara's biosimilar erosion created an
  ~760-basis-point Q2 2026 operational headwind that a broad set of newer
  products (Darzalex, Carvykti, Tecvayli, Rybrevant/Lazcluze, Tremfya,
  Spravato, Caplyta) is currently offsetting, not yet outrunning.
- **MRK** faces its principal replacement burden ahead, not behind:
  Keytruda's own future exclusivity step-down is not yet reflected in
  current results, and whether launches/acquired assets can offset it in
  time is this record's most consequential unresolved question (B7-U004).
- **LLY** and **GILD** do not show a comparable single-product exclusivity
  cliff already underway in this evidence base, but precise
  product-by-product patent/exclusivity dates are unresolved for all five
  companies (B7-U001, batch-wide) — this comparison does not assert a
  relative exclusivity-timing ranking.

## Pipeline breadth and clinical/regulatory conversion

All five companies show 2026 regulatory approvals converting pipeline
assets into products: LLY (Foundayo), ABBV (Decnupaz), MRK (the Keytruda/
Welireg adjuvant regimen and Lipfendra), JNJ (the teclistamab-combination
approval, among others cited in its growth commentary), and GILD (Hepcludex
and expanded Trodelvy indications). This is evidence that pipeline-to-
product conversion is occurring across the batch, not evidence of relative
pipeline quality or probability of future success, which this record does
not assess.

## Internal research versus acquisition dependence

Business-development intensity is visible across the batch but is not
uniform: LLY announced four separate 2026 acquisitions (Orna, Centessa,
Kelonia, Ajax); MRK recorded a $9.0 billion Cidara charge plus an
anticipated ~$5.8 billion Terns charge; GILD reduced 2026 EPS guidance by
~$9.50 for ~$11.5 billion of anticipated Arcellx/Ouro/Tubulis-related
acquired-IPR&D and financing costs; ABBV carries substantial (unquantified
in this record — see F-2) goodwill and intangible-asset exposure from past
acquisitions. This record does not measure what fraction of each company's
future pipeline value is internally generated versus acquired — that
measure is an unresolved question for ABBV specifically (B7-U003) and is
not established for the others either.

## Manufacturing complexity and capacity

LLY discloses manufacturing capacity as a stated strategic priority
(Pennsylvania site; this record does not assert an exact Wisconsin
production-start date, see LLY.md F-3 disposition). ABBV disclosed a $100
billion decade-long U.S. R&D/capital-investment pledge. JNJ's MedTech
segment adds device-manufacturing and procedure-related capacity
considerations distinct from pharmaceutical manufacturing. This record does
not establish a specific manufacturing-capacity claim for MRK or GILD
beyond their general business-development activity.

## Payer, pricing, reimbursement, and access exposure

Concrete, dated exposure is disclosed for two companies: LLY's Q1 2026
growth was partly offset by lower realized Mounjaro/Zepbound prices, and
ABBV's Botox was selected for Medicare-set pricing beginning 2028. FDA
approval and label/safety requirements (e.g., Foundayo's boxed warning)
apply across the batch as a shared regulatory-access risk category. This
record does not quantify aggregate payer exposure for MRK, JNJ, or GILD
beyond the evidence in each company's own record.

## Regulatory and safety risk

Each company shows at least one 2026 FDA action carrying disclosed
safety/label content (LLY's Foundayo boxed warning is the most explicit in
this evidence base). This is a shared regulatory-risk category across the
batch, not a ranking of relative safety profiles.

## Diversification by product, therapeutic area, and segment

JNJ is structurally the most diversified by segment (Innovative Medicine
plus MedTech, two different economic models under one company). ABBV shows
the most diversification by therapeutic area within pharmaceuticals
(immunology, neuroscience, oncology, aesthetics). GILD's diversification
(oncology, cell therapy, liver disease) is real but currently uneven
(Trodelvy growing, Yescarta declining in the same quarter). MRK's
diversification (Winrevair, Animal Health, Lipfendra) is real but small
relative to Keytruda's scale. LLY's diversification (immunology, oncology,
neuroscience programs, four 2026 acquisitions) is the least far along in
revenue terms relative to its incretin concentration.

## Balance-sheet strength and constraints

Balance-sheet and capital-allocation evidence is disclosed unevenly across
the batch. JNJ discloses the most complete current picture in this evidence
base ($20.8B cash/marketable securities, $49.0B debt, ~$8.7B YTD free cash
flow, $6.4B YTD dividends). GILD discloses $8.6B cash plus concurrent debt
repayment, dividends, and buybacks. ABBV's balance sheet carries
substantial goodwill/intangible exposure whose exact current figure this
record does not state (F-2). This record does not establish a comparable
balance-sheet figure for LLY or MRK beyond their disclosed acquisition
charges.

## Dividends, repurchases, acquisitions, and reinvestment priorities

GILD and JNJ both show concurrent capital return (dividends, buybacks) and
acquisition-driven reinvestment in the same reporting period. LLY and MRK
show acquisition-heavy capital allocation (four 2026 deals for LLY; two
large charges for MRK) without a comparable disclosed capital-return figure
in this record's evidence base. ABBV discloses a decade-long U.S.
investment pledge rather than a near-term capital-return figure in the
sources inspected here.

## Key competitors and substitutes

- LLY: Novo Nordisk and other incretin developers.
- ABBV: other immunology biologics and oral agents.
- MRK: competing oncology regimens and other checkpoint inhibitors.
- JNJ: competing pharmaceutical and medical-device platforms (across its
  two segments separately).
- GILD: competing HIV regimens, oncology antibody-drug conjugates, and
  cell therapies.

## Dependencies and shared external drivers

All five share exposure to: U.S. drug-pricing and reimbursement changes;
patent challenges, biosimilars, and loss of exclusivity; clinical or
regulatory failure in late-stage pipeline assets; manufacturing or
supply-chain disruption; acquisition overpayment, integration failure, or
intangible impairment; and concentration in a small number of high-revenue
products. These are the batch's correlated-loss drivers — a shared
macro/regulatory event (e.g., a broad drug-pricing policy change) could
affect several of these holdings at once, independent of company-specific
execution.

## Duplicated exposure and correlated-loss risk

None of the five companies is a member of any `targets.yaml`
correlated-cluster cap (`semis`, `power_infra`, `oil`) as of this record's
cutoff — this is a structural fact about existing governed policy, not a
finding about whether a correlation-based grouping among these five would
be warranted (that determination is outside this batch's authorized
scope). The shared correlated-loss drivers listed above (regulatory/
pricing policy, exclusivity-cycle timing, and biopharma-sector sentiment)
are a plausible mechanism for correlated moves across the batch, but this
record does not perform or assert a correlation measurement — that would
require its own separate, quantitative analysis outside this batch's
scope.

## JNJ MedTech boundary

**J&J is not a pure pharmaceutical peer within this batch.** Q2 2026 sales
were split $16.384 billion Innovative Medicine / $8.926 billion MedTech
(roughly 65%/35%), with different operational growth rates (6.8% versus
3.6%) and different underlying drivers (pharmaceutical launches and
exclusivity dynamics versus device/procedure volume and hospital
capital-spending dynamics). **This record explicitly does not assume J&J
MedTech is interchangeable with Portfolio-HQ's existing
`intelligence/themes/life_sciences_tools_medtech.yaml` theme** (ISRG, TMO)
— that theme's own members sell devices/tools directly to hospitals, labs,
and biopharma customers as their primary business, a different economic
model from a MedTech segment embedded inside a diversified
pharmaceutical-and-device conglomerate. Comparing JNJ directly against LLY,
ABBV, MRK, or GILD on ordinary pharmaceutical-company terms (pure product
concentration, pipeline-only capital allocation) would understate JNJ's
structural complexity; comparing JNJ's MedTech segment directly against
ISRG or TMO would equally overstate the similarity. This record does not
attempt either comparison as a ranking.

## Company-specific disconfirming evidence

See each company's own `.md` record for its full disconfirming-evidence
list. In brief: LLY's growth is partly offset by realized-price pressure
and carries a materially warned product label; ABBV's diversification is
uneven (Imbruvica decline) atop an unquantified-in-this-record intangible
base; MRK's underlying growth is modest (3% ex-FX) beneath very large
acquisition charges; JNJ's litigation exposure is material and not fully
estimable, and MedTech trails Innovative Medicine's growth; GILD's cell
therapy is contracting even as HIV dominates revenue.

## Unresolved questions (batch-wide and company-specific)

- **B7-U001** (all five): precise product-by-product U.S./ex-U.S. patent
  and exclusivity dates are not established.
- **B7-U002** (LLY): durability of net incretin pricing/access after launch
  normalization.
- **B7-U003** (ABBV): internal-versus-acquired growth-dependency measure.
- **B7-U004** (MRK): probability-weighted Keytruda-replacement timing.
- **B7-U005** (JNJ): financially plausible range of talc/other litigation
  outcomes.
- **B7-U006** (GILD): durability of oncology/cell therapy as a second
  engine relative to HIV.

## Prohibited-output confirmation

No company ranking, tier recommendation, target recommendation, trade
action, or margin recommendation is included in this document or in any of
the five companies' Company Intelligence records created alongside it.
