---
decision_id: PI-0010
date: 2026-07-18
status: Accepted
category: architecture_governance
related_decisions: [PI-0001, PI-0006, PI-0007, PI-0009, GOV-0001]
supporting_artifact: null   # doctrine/documentation-reconciliation decision; no
                            # backtest or external evidence file — grounded in
                            # repository state itself (see Context).
---

## Context

`decision_log.yaml` PI-0006 froze the Theme Intelligence data model. PI-0007
authorized, and PI-0009 retroactively recorded, two implemented pilots:
`ai_infrastructure` (referencing NVDA, GEV) and `life_sciences_tools_medtech`
(referencing ISRG, TMO). Both are live on `main`: `intelligence/themes/`
holds both themes' YAML and Markdown pairs, and four company records under
`intelligence/companies/` carry a `themes:` field, all validated by
`intelligence_validator.py`'s theme-specific functions
(`_validate_themes_field`, `_validate_theme_references`,
`validate_theme_data`, `validate_theme_file`, `validate_themes_directory`).

`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` — status "canonical, frozen" — contains
no reference to themes anywhere: its Directory structure section enumerates
only `intelligence/companies/` and `intelligence/reports/` and states "No
other top-level directories," which is no longer accurate; its Company YAML
schema section has no `themes:` field though the validator enforces one; no
theme schema section exists despite PI-0006 freezing one. PI-0007 itself
anticipated this gap and gated it explicitly: "No change to
docs/PORTFOLIO_INTELLIGENCE_SPEC.md is authorized under this decision,
including no new section — any future spec change requires its own separate
governance decision." This decision is that separate governance decision.

Independently, two other governed documents already assume the spec covers
themes: `governance/README.md` calls `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
the frozen spec for company/theme thesis content in the same breath it names
the `PI-####` decision series, and `constitution/INVESTMENT_CONSTITUTION.md`
refers to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` outright as covering
"Company/Theme Intelligence's non-negotiables." The constitution's own
citation is currently inaccurate against the spec as written — a second,
independent symptom of the same gap this decision closes.

## Decision

Authorizes exactly one action: amending `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
to document the Theme Intelligence architecture already frozen by PI-0006 and
already implemented by PI-0007/PI-0009. Specifically, and only:

1. Purpose and scope section — append one paragraph noting Theme Intelligence
   exists as a related, separately-governed record type, pointing to the new
   addendum section (item 4 below) for the schema.
2. Directory structure section — add `intelligence/themes/<THEME_ID>.{yaml,md}`
   to the directory listing; correct the "No other top-level directories"
   sentence to reflect the actual top-level set.
3. Company YAML schema section — add the optional
   `themes: [<theme_id>, ...]` field, codifying PI-0006's company-side
   schema addition without changing its substance.
4. New §25, "Theme Intelligence (addendum — PI-0006 / PI-0007 / PI-0009)" —
   faithfully codifies PI-0006's frozen theme YAML schema (`theme_id`,
   `description`, `evidence`, `risks`, `catalysts`, `lifecycle` closed
   vocabulary, `review` block) and governing rules, including one-way
   company→theme authority, no stored sibling index, no theme-level
   conviction or numeric score, and a closing restatement of the
   specification's already-existing non-coupling posture (§4, §20) and the
   already-governed deferral of Portfolio Intelligence aggregation and
   allocator integration (PI-0006, PI-0007). This restatement creates no
   new prohibition, architecture, or authority. Added as a new trailing
   section rather than interleaved into the existing numbered sections, to
   avoid disturbing the cross-reference numbering those sections use
   internally among themselves.

No other section of the specification changes. No company file, theme file,
validator, report, or allocator-visible behavior is created, modified, or
authorized by this decision.

## Rationale

Single-source-of-truth discipline (the same principle GOV-0001 generalized
from PI-0001): a document titled "canonical, frozen" should not omit a
record type that is live, governed, and already assumed-covered by two other
documents in the same repository. Documenting already-frozen, already-shipped
architecture is not a design decision — the actual design choices were made
and closed by PI-0006 (data model) and PI-0007/PI-0009 (implementation
scope); this decision performs no new evaluation of alternatives on those
questions and reopens none of them.

`architecture_governance` is retained as this decision's category because it
is the category every prior `PI-####` entry in `decision_log.yaml` uses
(`PI-0001` through `PI-0009`), as well as `MARGIN-0003` and `GOV-0001` — the
established category for freezes, specifications, and governance-process
decisions, as distinct from `margin_doctrine` or `concentration_risk`, which
are used for decisions setting specific numeric parameters. This decision
sets no numeric parameter; it reconciles documentation with already-accepted
governance, matching the established pattern exactly.

This decision is filed with `status: Accepted` directly, following
`GOV-0001`'s own precedent (filed directly as `Accepted`, with no
intermediate `Proposed`-status file in the repository's history). Neither
`governance/README.md` nor `governance/decisions/README.md` requires an
intermediate `Proposed` state before a decision may be filed as `Accepted`;
the `Proposed` value in `governance/templates/decision_template.md` is a
template default, not a mandated workflow gate.

## Alternatives Considered

- **Leave the spec unchanged.** Rejected: the drift is active, not
  hypothetical — a reader of the "canonical, frozen" spec today cannot learn
  Theme Intelligence exists, and two other governed documents already
  contradict the spec's own silence on the topic.
- **A second, separate spec document for Theme Intelligence.** Rejected:
  fragments a single domain (Portfolio Intelligence, of which Theme
  Intelligence is an explicitly-scoped extension per PI-0006's own roadmap
  language) across two canonical documents for no stated benefit, and
  contradicts the spec's own framing of future work as incremental
  implementation against a single fixed specification.
- **Wait for a third theme before updating.** Rejected: two pilots are
  already merged and live; deferral has no evidentiary upside (this isn't a
  backtest-style question where more data changes the answer) and only
  extends the period during which the canonical spec misdescribes
  production.
- **Renumber the existing sections to insert the theme schema in
  schema-adjacent position, shifting later sections down.** Rejected as
  higher-risk-for-no-benefit: numerous existing sections cross-reference
  each other by section number; renumbering is a larger, more error-prone
  diff for a purely organizational preference, not required by anything
  this decision needs to accomplish.
- **`GOV-####` instead of `PI-####` as the identifier prefix.** Considered:
  `governance/decisions/README.md` states `GOV-####` is "used for decisions
  about this documentation/governance architecture itself." This decision's
  substantive domain is Portfolio Intelligence — it reconciles
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, the exact document the `PI-####`
  series already governs — not the four-layer documentation architecture
  `GOV-0001` adopted. `GOV-0001` governs *where* this decision is filed
  (`governance/decisions/`, per its own Consequences section: "a new
  decision in any domain gets a file under `governance/decisions/`"), not
  *which domain prefix* it uses. `PI-0010` was selected as the domain-correct
  identifier on that basis.

## Consequences

`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` remains "canonical, frozen" — this
decision documents already-frozen (PI-0006) and already-implemented
(PI-0007, PI-0009) architecture; it freezes nothing new and reopens no
closed question. Explicitly out of scope, not authorized by this decision:
theme aggregation, theme-level scoring/ranking/weighting, any allocator or
execution-visible integration, any new theme or company record, any change
to `intelligence_validator.py`, `allocate.py`, `targets.yaml`, or
`holdings.yaml`, and any change to PI-0004's conviction vocabulary or
PI-0006's lifecycle vocabulary. `governance/decisions.yaml` requires one new
row for this entry, added alongside this file. `decision_log.yaml` is not
touched — per `GOV-0001`, it remains the unchanged historical ledger for
decisions predating the governance-decision-record layer, and this is not
one of those. A short pointer entry is added to `CLAUDE.md`'s Decisions Log,
consistent with the pattern `GOV-0001`'s own entry there already set; the
full rationale stays in this file and is not duplicated in `CLAUDE.md`.
