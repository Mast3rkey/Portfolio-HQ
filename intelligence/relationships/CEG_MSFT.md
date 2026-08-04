# CEG ↔ MSFT — customer_dependency (CEG depends on MSFT)

Last updated: 2026-08-04 — record created through AI-assisted research and
drafting under `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
(frozen schema, taxonomy, evidence standard) and
`governance/decisions/REL-0002-ws0005-milestone4-first-relationship-content-batch-ceg-msft.md`
(this specific batch's authorization). First WS-0005 Milestone 4
relationship-content record of any kind — no prior `intelligence/relationships/`
record existed anywhere in this repository before this unit.

## Source-access disclosure

This record performs **zero new external research**. Every fact below is
drawn from evidence already present in the repository at this unit's own
preflight: `intelligence/companies/CEG.yaml`'s claim `CEG-C05` (itself
sourced to Constellation Energy Corporation's 2025 Form 10-K, SEC accession
0001868275-26-000032, Item 1, page 14, as directly inspected by that
record's own external evidence-recovery researcher — not by this session),
and the advisory batch recommendation in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§9, which named `CEG_MSFT` as the smallest coherent first Milestone 4
relationship-content candidate.

**This relationship is disclosed from CEG's side only.** This session
directly grepped `intelligence/companies/MSFT.yaml` and
`intelligence/companies/MSFT.md` for any mention of "Constellation," "CEG,"
"nuclear," or "power purchase"/"PPA" and found zero matches — Microsoft's
own Company Intelligence record does not independently name Constellation
Energy, the Crane Clean Energy Center, or this PPA anywhere. No attempt was
made to locate independent MSFT-side primary-source confirmation (an SEC
filing, an investor-relations statement, a press release) — that would
constitute new external research, which this unit is not authorized to
perform. Per the inventory's own §9 stopping condition for this exact
candidate ("if MSFT-side confirmation cannot be found without new
primary-source research beyond what CEG.md already cites, the record should
carry `evidence_classification: inferred` from CEG's side only and disclose
the one-sided sourcing explicitly, not silently upgrade to `observed`"),
this record's evidence entry is classified `inferred`, not `observed` — see
`CEG_MSFT.yaml`'s `evidence[0].evidence_classification` and
`evidence[0].uncertainty`.

Neither `intelligence/companies/CEG.yaml`/`CEG.md` nor
`intelligence/companies/MSFT.yaml`/`MSFT.md` was read for the purpose of
editing them, and neither was modified by this unit in any way.

## The relationship

Constellation Energy Corporation (CEG) is disclosed, in its own Company
Intelligence record, as party to a **20-year Power Purchase Agreement (PPA)
with Microsoft Corporation (MSFT)**. Microsoft is named as the offtake
counterparty supporting the planned restart of CEG's **835 MW Crane Clean
Energy Center** nuclear generating asset. CEG's own record describes this as
"long-duration, investment-grade offtake demand tied specifically to
data-center/AI electricity demand," explicitly subject to regulatory and
execution conditions — the restart is a planned project, not an operating
asset, at this evidence cutoff.

Classified under REL-0001 §C's `customer_dependency` primitive:
**CEG (subject) depends on MSFT (object)** as a named, contracted,
long-duration source of demand for CEG's own generation output. Directional
per REL-0001 §D — `customer_dependency` is directional-by-construction, and
this record declares `symmetric: false` accordingly. No claim is made in
the reverse direction (Microsoft depending on Constellation) — this is a
single-direction relationship, not a mutual one, and Microsoft's own energy
procurement almost certainly spans far more counterparties than this single
PPA, none of which this record addresses.

## Why this batch, why this pair first

Per the inventory audit's §9 candidate table, `CEG_MSFT` was identified as
the smallest coherent first Milestone 4 relationship-content candidate:
CEG's own record already fully documents the PPA, counterparty, and asset;
no new external research was judged likely to be required to establish the
relationship's existence (only to strengthen it beyond one-sided sourcing);
neither company's existing Intelligence record needed editing (this record
is purely additive); and the evidentiary strength — a named, dollar-relevant
(though the specific dollar figure is not disclosed in the current evidence
base), long-duration, primary-source-corroborated (on CEG's side)
relationship — was described by the inventory as "the single best-documented
canonical-pair relationship found anywhere in this inventory."

## What this record does and does not establish

**Established, per the evidence above:** CEG's own disclosure of a named,
long-duration PPA with Microsoft as counterparty, tied to a specific named
asset (Crane Clean Energy Center) and a specific named capacity figure
(835 MW).

**Not established by this record:** the PPA's dollar value or its
percentage of CEG's total or segment revenue (not located anywhere in the
current evidence base); independent MSFT-side confirmation of the PPA's
existence or terms; whether the Crane restart has since progressed, stalled,
or been confirmed complete (this record's evidence cutoff is CEG.yaml's own
2026-07-28 review, itself drawn from a 2025 Form 10-K filed 2026-02-24 and a
Q1 2026 earnings presentation dated 2026-05-11); any measured historical
price correlation between CEG and MSFT (REL-0001 §G explicitly separates
structural evidence of this kind from measured price correlation — none was
computed, cited, or implied here); and any conclusion about duplicate
economic exposure, correlated loss, or missing exposure (REL-0001 §C
excludes these as primitive record types — they are derived conclusions a
future, separately authorized artifact may draw *from* records like this
one, never asserted directly by a primitive record itself).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`thesis_monitoring`** — a material, disclosed customer relationship
  tied to a specific pending asset restart is exactly the kind of fact a
  future thesis-monitoring pass over CEG (or, if MSFT's own energy strategy
  is later reviewed, over MSFT) should track for status changes.
- **`stress_testing`** — if the Crane restart is delayed, cancelled, or the
  PPA terms are renegotiated, this is a disclosed, name-specific event a
  future portfolio-level stress scenario could reference, distinct from any
  generic utility-sector or nuclear-sector stress assumption.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, stress-test execution, tier
change, target change, or trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to CEG's or
MSFT's tier, target, role, cluster, cap, or holding; any trade or order; any
margin use or margin-policy recommendation; any ranking, score, or composite
metric; any price-correlation study; any graph or "Eureka" implementation;
or any conclusion about duplicate economic exposure, correlated loss
mechanism, or missing exposure (see "What this record does and does not
establish" above). It is a single, additive, primitive relationship record
under REL-0001's frozen schema — nothing more.
