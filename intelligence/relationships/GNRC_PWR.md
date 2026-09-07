# GNRC ↔ PWR — complement (symmetric)

Last updated: 2026-08-04 — record created through AI-assisted research and
drafting under `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
(frozen schema, taxonomy, evidence standard) and
`governance/decisions/REL-0003-ws0005-milestone4-second-relationship-content-batch-remaining-eight-pairs.md`
(this batch's own authorization). Part of WS-0005 Milestone 4's second
relationship-content batch — a reuse-only batch of the eight pairs the
`REL-0001` §I inventory audit's own §9 table already identified as evidence-
ready, following `REL-0002`'s single-pair `CEG_MSFT` precedent.

## Source-access disclosure

This record performs **zero new external research**. Every fact below is
drawn from evidence already present in the repository at this unit's own
preflight: `intelligence/companies/GNRC.yaml`'s claim `GNRC-C03`, itself
citing Generac's own Q2 2026 earnings release (directly fetched and read by
that record's own research session), and `intelligence/companies/GNRC.md`
§13 ("Overlap and diversification versus power_infra (ETN/GEV/PWR) and
versus CAT/TSLA") — the analytical section that itself draws the
`complement` framing this record adopts. The advisory batch recommendation
in `governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§9 named `GNRC_GEV`, `GNRC_ETN`, and `GNRC_PWR` as evidence-ready
second-batch candidates.

**This relationship is disclosed from GNRC's side only.** This session
directly grepped `intelligence/companies/PWR.yaml` and
`intelligence/companies/PWR.md` for "GNRC" and "Generac" and found zero
matches — Quanta Services' own Company Intelligence record does not
independently name Generac, a shared customer, or a shared project
anywhere. No attempt was made to locate independent PWR-side primary-source
confirmation of a named joint relationship — that would constitute new
external research, which this unit is not authorized to perform.

Neither `intelligence/companies/GNRC.yaml`/`GNRC.md` nor
`intelligence/companies/PWR.yaml`/`PWR.md` was read for the purpose of
editing them, and neither was modified by this unit in any way.

## The relationship

Generac Holdings (GNRC)'s 2025-2026 pivot into commercial & industrial
(C&I) data-center backup power is disclosed, dollar-quantified, in GNRC's
own Company Intelligence record: two disclosed multi-year hyperscale supply
agreements (approximately $700 million of committed 2027 volume; a second,
disclosed as expected to be at least as large) and a Q2 2026-disclosed
**$1.6 billion data-center order backlog**.

GNRC's own record's analytical section (§13) frames this directly against
the governed `power_infra` correlated-cluster cap: on-site backup
generation (GNRC) is described as "a literal complementary line item in the
same data-center power stack" alongside Quanta Services (PWR)'s
EPC/interconnection services, Eaton (ETN)'s switchgear and power-
distribution equipment, and GE Vernova (GEV)'s turbines and grid equipment —
four functionally distinct, non-substitutable equipment/service categories
within the same overall AI-data-center electrical buildout, not a
supplier/customer or competitive relationship among any of them.

Classified under REL-0001 §C's `complement` primitive, which REL-0001 §D
treats as **symmetric-by-construction**: this record declares
`symmetric: true`, with GNRC and PWR as co-equal subjects, per REL-0001 §D's
rule that a symmetric type is recorded once per pair with no directional
subject/object.

## Why this pair, why this batch

Per the inventory audit's §9 candidate table, `GNRC_PWR` (alongside
`GNRC_GEV` and `GNRC_ETN`) was identified as an evidence-ready second-batch
candidate: GNRC's own record's §13 analysis is dollar-quantified and
already documents the mechanism; neither company's existing Intelligence
record needs editing — this record is purely additive; and the inventory's
own stopping condition specified exactly this record's resolution if a
named shared customer could not be confirmed from either side (it could
not): record as `complement`/`inferred` with the materiality caveat GNRC's
own record already discloses.

## What this record does and does not establish

**Established, per the evidence above:** GNRC's own disclosure of a
dollar-quantified, contracted pivot into hyperscale data-center backup
power, and GNRC's own record's analytical framing of that pivot as
complementary to PWR's (and ETN's and GEV's) role in the same data-center
electrical buildout.

**Not established by this record:** any named joint contract, shared
hyperscaler customer, or shared project specifically linking GNRC and PWR
(no source located names both companies together in a single disclosed
transaction — PWR's own role is EPC/interconnection construction services,
a different function from either a supplier or a customer relationship to
GNRC's generator manufacturing); any dollar figure or percentage
attributable to the GNRC-PWR overlap specifically, as distinct from GNRC's
total data-center backlog; whether GNRC's data-center pivot will continue
to grow relative to its majority-residential revenue base (GNRC.md §13
explicitly frames this as "a blended, actively evolving exposure," not
settled); any measured historical price correlation between GNRC and PWR
or any `power_infra` member — GNRC.md §13 states explicitly that no such
correlation scan has ever been performed by this record or by any prior
repository decision; and any conclusion about duplicate economic exposure,
correlated loss, or missing exposure (REL-0001 §C excludes these as
primitive record types).

**Materiality caveat, carried forward from GNRC's own record and not
smoothed over here:** GNRC's C&I segment was only ~35% of FY2025 total
company revenue ($1.46B of $4.21B), and even within C&I, data centers are
described as the "core driver" but not the entirety — telecom, rental,
industrial, and government gensets also sit within C&I. Residential demand,
genuinely unrelated to the AI-buildout mechanism, remains the majority of
GNRC's revenue (~54%, $2.27B). GNRC.md §13's own "net judgment" states this
is not a clean cluster-member case the way a naive reading might suggest —
GNRC sits between two poles this repository has already established for
the `power_infra` question, with the majority of its revenue and
historical identity still in a genuinely different, weather/housing-driven
mechanism (the same category CAT and TSLA were scanned and excluded from
on weak-fundamental-fit grounds).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — GNRC's C&I/data-center leg and PWR's
  power_infra role serve overlapping demand within the same buildout theme;
  a future duplicate-exposure review should be aware of this even though
  GNRC itself is not a `power_infra` cluster member.
- **`missing_exposure_review`** — the reverse question (whether the
  existing `power_infra` cluster construction is missing GNRC's own
  distinct on-site-generation exposure, or whether GNRC's inclusion would
  be double-counting) is exactly the kind of question this record's
  disclosed evidence should inform, without this record itself answering
  it.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, tier change, target change,
cluster-membership change, or trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to GNRC's
or PWR's tier, target, role, cluster, cap, or holding — GNRC's cluster
membership question is explicitly named in `PI-0033`'s own GNRC disposition
as a separate, unauthorized, future Milestone-4-adjacent question this
record flags but does not answer; any trade or order; any margin use or
margin-policy recommendation; any ranking, score, or composite metric; any
price-correlation study; any graph or "Eureka" implementation; or any
conclusion about duplicate economic exposure, correlated loss mechanism, or
missing exposure (see "What this record does and does not establish"
above). It is a single, additive, primitive relationship record under
REL-0001's frozen schema — nothing more.
