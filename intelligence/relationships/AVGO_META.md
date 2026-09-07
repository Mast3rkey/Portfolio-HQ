# AVGO ↔ META — customer_dependency (AVGO depends on META)

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
preflight: `intelligence/companies/AVGO.yaml`'s `competitive_advantages[1]`
and `risks[0]` entries, themselves citing `AVGO.yaml`'s own `sources[2]`
entry (labeled "SECONDARY (aggregated custom-AI-accelerator industry
coverage, multiple partially-overlapping outlets)"), and the advisory batch
recommendation in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§9, which named `AVGO_GOOGL` and `AVGO_META` as evidence-ready second-batch
candidates alongside `CEG_MSFT`.

**This relationship is disclosed from AVGO's side only.** This session
directly grepped `intelligence/companies/META.yaml` and
`intelligence/companies/META.md` for "AVGO" and "Broadcom" and found zero
matches — Meta's own Company Intelligence record does not independently
name Broadcom or any custom-silicon supplier relationship anywhere. No
attempt was made to locate independent META-side primary-source
confirmation — that would constitute new external research, which this
unit is not authorized to perform. Per the inventory's own §9 stopping
condition for this candidate ("same one-sided-sourcing disclosure
discipline as CEG_MSFT"), this record's evidence entry is classified
`inferred`, not `observed`.

Neither `intelligence/companies/AVGO.yaml`/`AVGO.md` nor
`intelligence/companies/META.yaml`/`META.md` was read for the purpose of
editing them, and neither was modified by this unit in any way.

## The relationship

Broadcom Inc. (AVGO)'s custom AI accelerator (XPU) design-services and
AI-networking business is disclosed, in AVGO's own Company Intelligence
record, as reporting a small, named hyperscaler/frontier-lab customer
roster: **Google, Meta, OpenAI, Anthropic, and Apple**, with at least one
source characterizing the roster as "six major customers" without naming a
sixth (this record does not adopt an unnamed sixth customer as confirmed).
Unlike the parallel `AVGO_GOOGL` record, no Meta-specific contract
structure, dollar value, or supply-agreement detail comparable to AVGO's
disclosed Google TPU supply agreement was located in the current evidence
base — Meta is named in the customer roster only.

Classified under REL-0001 §C's `customer_dependency` primitive: **AVGO
(subject) depends on META (object)** as a named source of AI-segment
customer demand and design-services revenue. Directional per REL-0001
§D — `customer_dependency` is directional-by-construction, and this record
declares `symmetric: false` accordingly. No claim is made in the reverse
direction (Meta depending on Broadcom) — Meta's own compute-supply strategy
spans far more than this one design-services relationship, none of which
this record addresses.

## Why this pair, why this batch

Per the inventory audit's §9 candidate table, `AVGO_META` (alongside
`AVGO_GOOGL`) was identified as an evidence-ready second-batch candidate on
the same grounds as `CEG_MSFT`: AVGO's own record already documents the
named customer roster; no new external research was judged likely to be
required to establish the relationship's existence; and neither company's
existing Intelligence record needs editing — this record is purely
additive.

## What this record does and does not establish

**Established, per the evidence above:** AVGO's own disclosure of a named,
concentrated AI-segment customer roster including Meta.

**Not established by this record:** any Meta-specific dollar figure,
contract structure, or percent-of-AVGO-AI-segment-revenue attributable to
Meta alone (not located anywhere in the current evidence base — the
disclosed ~40% top-five-customer figure is company-wide, not
Meta-specific); independent META-side confirmation of a supply, design, or
contract relationship of any kind; whether AVGO's own reported customer
roster or backlog figures have since changed (this record's evidence
cutoff is AVGO.yaml's own 2026-07-26 review); any measured historical price
correlation between AVGO and META (REL-0001 §G explicitly separates
structural evidence of this kind from measured price correlation — none
was computed, cited, or implied here); and any conclusion about duplicate
economic exposure, correlated loss, or missing exposure (REL-0001 §C
excludes these as primitive record types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — AVGO and META are both governed
  canonical holdings; a disclosed customer relationship between them is
  exactly the kind of structural fact a future duplicate-exposure review
  should account for.
- **`thesis_monitoring`** — a concentrated, named AI-segment customer
  roster is a fact a future thesis-monitoring pass over AVGO should track
  for status changes (e.g., a customer's own AI-capex pullback).

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, tier change, target change, or
trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to AVGO's
or META's tier, target, role, cluster, cap, or holding; any trade or
order; any margin use or margin-policy recommendation; any ranking, score,
or composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
