---
decision_id: PI-0015
date: 2026-07-21
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0001, PI-0002, PI-0003, PI-0004, PI-0005, PI-0006, PI-0007, PI-0009, PI-0011, PI-0012, PI-0013, ONTO-0001]
supporting_artifact: null
---

## Context

`decision_log.yaml`'s `PI-0004` closed the COST pilot-review gate and, in
the same decision, deliberately deferred `risks[].severity` and
`risks[].status`: "one company record is insufficient evidence to justify
a closed vocabulary for either field; revisit once 3-5 company records
exist and real usage patterns are observable." Seven Company Intelligence
records now exist — COST, GEV, ISRG, NVDA, TMO, TSM, XOM — exceeding
`PI-0004`'s own stated revisit threshold. This decision is that revisit,
performed as a bounded, read-only evidence review (conversational
analysis this session; `supporting_artifact: null` above, same disclosure
convention `PI-0004`/`PI-0005`/`PI-0006`/`PI-0007`/`PI-0009` already used).

The review inventoried every risk entry across all seven records: **34**
total. `severity` has exactly **two** observed values — `moderate` (25
occurrences: COST 3, GEV 3, ISRG 4, NVDA 3, TMO 2, TSM 7, XOM 3) and `low`
(9 occurrences: COST 2, GEV 1, NVDA 2, TMO 2, XOM 2) — both lowercase, no
casing drift, no numeric substitute, no hybrid. `high` never appears, in
any of the 34 entries, despite several risks whose own text reads as
severe (TSM's Taiwan/cross-strait and Nanjing export-license exposure;
NVDA's export-control/geopolitical exposure; XOM's Guyana territorial
dispute). `status` has exactly **one** observed value — `monitoring`,
34/34, every entry in every record, no exception. Notably,
`test_intelligence_validator.py`'s Phase 1 synthetic fixture (predating
any real record) illustrated `status: "open"` — a value no real record has
ever used; real usage converged entirely on a word the schema-design
fixture did not anticipate.

Within this corpus, `severity` shows no internal discrimination where it
would matter most: TSM rates all seven of its own risks `moderate`,
including both a routine node-transition margin-dilution item and its
Taiwan cross-strait geopolitical/Nanjing export-license exposure, without
distinguishing them. Neither the frozen specification
(`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9, which declares `severity:
<string>` / `status: <string>` with no enumerated values) nor
`intelligence_validator.py` (which checks only that both keys are present,
with no value-level constraint) defines what axis `severity` measures —
business impact, likelihood, urgency, and portfolio-relative impact are
all plausible reads, and observed entries mix framings without the field
distinguishing them.

`governance/decisions/PI-0011-intelligence-operations-v1.md` independently
applied the identical anti-overfitting reasoning to the sibling field
`catalyst.status` the same week, declining to close it on one company's
worth of `pending`-status evidence and citing `PI-0004`'s own "3-5
records" bar as the reason. `docs/INVESTMENT_ONTOLOGY.md`
(`ONTO-0001`) governs a separate company-role/capital-type vocabulary and
does not reach Company Intelligence's `risks[]` fields at all.

## Decision

**Closes `PI-0004`'s deferred risk-vocabulary review question. Neither
`risks[].severity` nor `risks[].status` is frozen by this decision.** No
closed vocabulary is created for either field; both remain open,
free-text strings exactly as `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9
already specifies.

Seven records produced **less** differentiated usage than `PI-0004`'s own
3-5-record bar anticipated, not more: two `severity` values (never the
plausible third, `high`) and one `status` value. Freezing either field on
this evidence would encode the absence of observed variation as if it
were a discovered vocabulary — the identical overfitting risk `PI-0004`
itself warned against, and the same reasoning `PI-0011` already applied
to `catalyst.status`.

**`PI-0004`'s numeric "3-5 records" trigger is retired outright and is not
replaced by any other record-count threshold.** A bare record count
already proved to be a weak signal in this instance — seven records
crossed `PI-0004`'s own bar and produced no new information (fewer
distinct values than the bar was set to detect). In its place, both
fields get exact, evidence-driven triggers, keyed to what would actually
constitute new information, not to how many files exist:

- **`risks[].severity`** must be revisited when any one of the following
  occurs:
  - a future author proposes a `severity` value outside the currently
    observed lowercase set (`moderate`, `low`);
  - reviewers materially disagree about what `severity` measures (e.g.,
    business impact vs. likelihood vs. urgency vs. portfolio-relative
    impact);
  - reviewers materially disagree about how a specific risk should be
    labeled;
  - a future amendment to the `risks[]` schema is proposed.
- **`risks[].status`** must be revisited when any one of the following
  occurs:
  - an actual risk-state transition away from `monitoring` occurs on any
    real record;
  - a future author proposes any alternative `status` value;
  - a future amendment to the `risks[]` schema is proposed.

For both fields: a trigger opens a new governance evidence review only —
it does not automatically freeze a vocabulary. No proposed value becomes
controlled doctrine merely by triggering a review. Any later freeze still
requires its own separately accepted governance decision, applying the
same evidentiary discipline this one did.

**No schema, validator, or test change is authorized by this decision.**
`intelligence_validator.py` gains no new enforcement for either field.
**No existing record is migrated or modified** — COST.yaml, GEV.yaml,
ISRG.yaml, NVDA.yaml, TMO.yaml, TSM.yaml, and XOM.yaml all remain exactly
as currently committed.

**This decision authorizes exactly three file changes, and nothing
else:**

1. `governance/decisions/PI-0015-risk-vocabulary-review-closure.md` —
   this file.
2. `governance/decisions.yaml` — new `PI-0015` index row.
3. `CLAUDE.md` — one short Decisions Log pointer entry, same pattern as
   `PI-0010`/`PI-0011`/`PI-0012`/`PI-0013`/`PI-0014`.

No implementation PR, no validator change, no company or theme selection,
no schema amendment, and no second review is authorized by this decision.

## Rationale

`PI-0004` set an explicit, falsifiable revisit condition rather than
leaving the deferral open-ended, and named the specific anti-overfitting
concern it was guarding against: "freezing a vocabulary against a single
data point risks standardizing the wrong thing prematurely." That concern
is fully vindicated by what seven records actually show — two `severity`
values with the intuitively expected third (`high`) entirely unobserved,
and a single `status` value used without exception. A record-count-only
trigger already misled expectations once here: crossing `PI-0004`'s own
3-5-record bar produced no new variation at all, so a bare count is
demonstrated on this evidence not to track the thing that actually
matters. Retaining any numeric record-count trigger — at the original
threshold or a higher one — would repeat exactly the mechanism just shown
to fail; the replacement triggers above are evidence-driven instead,
keyed to an actual new value, an actual disagreement, an actual status
transition, or an actual schema-amendment proposal, so that the next
review is triggered by real information rather than by file count alone.

`TSM`'s own internal usage — seven risks spanning routine execution items
and existential geopolitical/export-control exposure, all rated
`moderate` — demonstrates the field is not yet discriminating in the one
company record where discrimination would matter most, reinforcing that
closure now would standardize an under-exercised concept, not codify a
demonstrated one. Retaining `status` fully open follows the same logic
`PI-0011` already used for `catalyst.status`: a single repeated value
provides no evidence of a working lifecycle vocabulary, only evidence
that no record has yet needed anything else.

## Alternatives Considered

- **Freeze both `severity` and `status` (Option A).** Rejected: `status`
  has exactly one observed value across 34 entries; freezing it now would
  be indistinguishable from freezing whatever word happened to get
  written first, with zero evidence of any actual lifecycle distinction.
- **Freeze `severity` only, leave `status` open (Option B).** Considered
  as the closer case — two observed values is thin but not zero.
  Rejected as the primary outcome because the plausible third value,
  `high`, has never once appeared despite several risks (TSM's Taiwan/
  export exposure, NVDA's export-control exposure, XOM's Guyana
  territorial dispute) that plausibly warrant it; freezing a two-of-three
  scale now risks encoding an incomplete vocabulary and reopening the
  question almost immediately upon the first genuinely severe entry. Also
  rejected: the field's semantic axis (impact vs. likelihood vs. urgency
  vs. portfolio-relative impact) is undefined anywhere in the frozen
  specification or the validator, and TSM's own undifferentiated
  seven-for-seven `moderate` usage shows the field is not yet
  discriminating even within a single record — freezing an unexercised
  axis compounds rather than resolves that gap.
- **Freeze `status` only, leave `severity` open (Option C).** Rejected:
  the weakest possible evidence basis of the four options — a single
  observed value across the entire corpus is definitionally insufficient
  to justify any closed vocabulary.
- **Leave both open with no new review trigger, i.e. simply extend
  `PI-0004`'s deferral unchanged.** Rejected: `PI-0004`'s own "3-5
  records" trigger has now been met and shown to be a weak signal (seven
  records produced no new variation); restating the same numeric trigger
  without correction would repeat a condition already demonstrated not to
  track the thing that actually matters. A field-specific, value-based
  trigger is a strictly more informative replacement, not a mere
  restatement.

## Consequences

`intelligence_validator.py`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `constitution/INVESTMENT_CONSTITUTION.md`,
`decision_log.yaml`, `allocate.py`, `margin_state.py`, `targets.yaml`,
`holdings.yaml`, and every existing Company/Theme Intelligence record
(`COST`, `GEV`, `ISRG`, `NVDA`, `TMO`, `TSM`, `XOM`,
`ai_infrastructure`, `life_sciences_tools_medtech`) are unchanged.
`governance/decisions.yaml` gains one new row for this entry. `CLAUDE.md`'s
Decisions Log gains one short pointer entry. **This decision does not
select or authorize any company or theme, does not enumerate a candidate
vocabulary for either field, and does not itself constitute or schedule
any future implementation.** A future closure of either vocabulary — upon
either stated trigger being met — requires its own separate governance
decision, applying the same evidentiary review discipline this one did.
