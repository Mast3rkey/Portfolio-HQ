# AMZN ↔ GOOGL — competitor (symmetric)

Last updated: 2026-08-04 — record created through AI-assisted research and
drafting under `governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`
(frozen schema, taxonomy, evidence standard) and
`governance/decisions/REL-0003-ws0005-milestone4-second-relationship-content-batch-remaining-eight-pairs.md`
(this batch's own authorization). Part of WS-0005 Milestone 4's second
relationship-content batch — a reuse-only batch of the eight pairs the
`REL-0001` §I inventory audit's own §9 table already identified as evidence-
ready, following `REL-0002`'s single-pair `CEG_MSFT` precedent. This is one
of three separate pairwise `competitor` records recording the same
batch-level three-way overlap finding — see also `GOOGL_MSFT.md` and
`AMZN_MSFT.md` — per REL-0001 §D's rule that a symmetric relationship type
is recorded once per pair, never once per group.

## Source-access disclosure

This record performs **zero new external research**. Every fact below is
drawn from `intelligence/BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md`
§7 ("Genuine diversification versus duplicated exposure"), an already
existing, already-merged comparison artifact — not from either company's
own individual record. The advisory batch recommendation in
`governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
§9 named the MSFT/GOOGL/AMZN `competitor` triad (as three separate
pairwise records) as an evidence-ready second-batch candidate.

**The specific competitive-overlap claim rests on BATCH5's own comparative
synthesis, not on either company's own named risk disclosure.** This
session directly grepped `intelligence/companies/AMZN.yaml` and
`intelligence/companies/GOOGL.yaml` for cross-references to each other and
found no corroboration in either company's own `.yaml` data.

**Correction (independent review 4856585060, PR #241):** this section's
original text additionally claimed to have found "no independent,
separately-stated competitive-overlap claim in either company's own
words" — that broader claim was inaccurate, because it was drawn only
from the `.yaml` grep above and did not check the `.md` companion files.
`intelligence/companies/AMZN.md`'s own "Capital-priority discipline"
section states "AMZN competes for capital priority against MSFT and
GOOGL, the other two public-cloud sellers in this batch";
`intelligence/companies/GOOGL.md`'s own equivalent section states GOOGL
"compete[s] for T1's overall capital-priority ranking against MSFT... and
against AMZN." Both are genuine, independently-stated cross-references
from each company's own record — but they describe **capital-priority
competition** (a portfolio-capital-allocation concept: which name should
receive the next investment dollar), not the **customer-demand
competitive overlap** REL-0001 §C.10 defines the `competitor` primitive
around ("compete for the same customer demand in a materially overlapping
product or service category"). This record does not treat that
capital-priority language as corroborating the customer-demand
`competitor` claim asserted here — the two are analytically distinct
concepts, and conflating them would overstate this record's evidentiary
basis.

Per the inventory's own §4.6 classification of this exact finding, this
record's evidence entry remains classified `inferred`, not `observed`.

Separately, per REL-0001 §H's existing-evidence-reuse discipline, this
record discloses (without asserting as evidence of the competitor claim
itself) that AMZN and GOOGL are both named, unverified, as customers of
already-covered semis-cluster names in other WS-0005 batches — most
directly, MRVL (non-canonical) is disclosed as supplying AMZN's Trainium
program per `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` §5; no
canonical-pair supplier relationship between AMZN and GOOGL themselves was
located anywhere in the inspected sources.

Neither `intelligence/companies/AMZN.yaml`/`AMZN.md` nor
`intelligence/companies/GOOGL.yaml`/`GOOGL.md` was read for the purpose of
editing them, and neither was modified by this unit in any way.

## The relationship

`BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` §7 states directly:
"MSFT, GOOGL, and AMZN duplicate each other to a real degree as
public-cloud sellers competing for the same enterprise AI-infrastructure
spending — this is the batch's clearest overlap." The same section
immediately qualifies this: within the three cloud sellers, "AWS's
scale/profitability, Azure's enterprise-software-bundled distribution (via
Microsoft 365/Dynamics), and Google Cloud's TPU-based differentiation each
represent a genuinely different competitive approach, not three identical
businesses measured three ways."

Classified under REL-0001 §C's `competitor` primitive, which REL-0001 §D
treats as **symmetric-by-construction**: this record declares
`symmetric: true`, with AMZN and GOOGL as co-equal subjects.

## Why this pair, why this batch

Per the inventory audit's §9 candidate table, the MSFT/GOOGL/AMZN
`competitor` triad was identified as an evidence-ready second-batch
candidate: the claim is fully stated in one already-inspected source
(BATCH5 §7) with no additional sourcing located or required beyond what
that section already cites, and no individual company record needs
editing — three additive pairwise records are required, per REL-0001 §D.

## What this record does and does not establish

**Established, per the evidence above:** BATCH5's own comparative
assessment that AMZN and GOOGL compete directly as public-cloud sellers for
overlapping enterprise AI-infrastructure spending, while retaining a
genuinely different competitive approach each.

**Not established by this record:** any dollar figure, market-share
percentage, or win/loss data quantifying the AMZN-GOOGL competitive overlap
specifically; independent, company-specific risk-disclosure language from
either AMZN or GOOGL's own record restating this competitive finding in
their own words; whether holding both AMZN and GOOGL alongside
already-covered supply-side semis-cluster names constitutes genuine
diversification or a duplicated bet on the same AI-capex cycle from two
value-chain positions — BATCH5 §7 itself names this explicitly as
"squarely a Milestone 4... question, which remains unauthorized," and this
record does not attempt to resolve it; any confirmed named supplier
relationship between AMZN and GOOGL themselves (the disclosed MRVL-Trainium
relationship is a separate, non-canonical, third-party matter, not a
direct AMZN-GOOGL relationship); any measured historical price correlation
between AMZN and GOOGL (REL-0001 §G explicitly separates structural
evidence of this kind from measured price correlation — none was
computed, cited, or implied here); and any conclusion about duplicate
economic exposure, correlated loss, or missing exposure (REL-0001 §C
excludes these as primitive record types).

## Decisions this record serves

Per REL-0001 §F's closed `decision_served` vocabulary, this record names:

- **`duplicate_exposure_detection`** — AMZN and GOOGL are both governed
  canonical holdings competing directly for the same AI-infrastructure
  spending; this record is exactly the kind of structural fact a future
  duplicate-exposure review should account for.
- **`stress_testing`** — a shared demand-side AI-capex-cycle risk across
  two directly competing cloud sellers is a disclosed, structural fact a
  future portfolio-level stress scenario could reference.

This field is explanatory and advisory only, per REL-0001 §F — naming these
values here creates no policy authority and does not itself trigger,
recommend, or imply any monitoring action, tier change, target change, or
trade.

## Non-authority

This record does not authorize, recommend, or imply: any change to AMZN's
or GOOGL's tier, target, role, cluster, cap, or holding; any trade or
order; any margin use or margin-policy recommendation; any ranking, score,
or composite metric; any price-correlation study; any graph or "Eureka"
implementation; or any conclusion about duplicate economic exposure,
correlated loss mechanism, or missing exposure (see "What this record does
and does not establish" above). It is a single, additive, primitive
relationship record under REL-0001's frozen schema — nothing more.
