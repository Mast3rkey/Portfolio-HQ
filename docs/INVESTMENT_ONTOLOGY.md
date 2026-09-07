# Investment Ontology (Reference Vocabulary)

Status: **frozen reference artifact** (`governance/decisions/ONTO-0001-investment-ontology-freeze.md`).
Date of adoption: 2026-07-19.

## Authority boundary — read this first

This document supplies a shared vocabulary for human research, discussion, and
governance. It is descriptive, not prescriptive. Specifically, this document:

- does not originate investment policy;
- does not classify any company automatically;
- does not assign or change any company's tier;
- does not assign or change any target weight;
- does not authorize a trade;
- does not modify or influence `allocate.py` or any other production code's
  behavior;
- does not override `CLAUDE.md`, `targets.yaml`, `holdings.yaml`,
  `constitution/INVESTMENT_CONSTITUTION.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.

Where any term below might someday inform a Company Intelligence record, a
Theme Intelligence record, a committee review, a report, or a policy change,
that use requires its own separate proposal and governance decision — nothing
here is self-executing. A company or theme having no ontology classification
at all is normal and is not an error or a gap to fill.

## A. Economic systems as an analytical lens

The idea that reasoning should examine the economic system a company
participates in, not just the company in isolation, originated in prior
investment-committee discussion. An economic-system lens allows a human
reviewer to examine a shared demand driver, supply chain, or structural
theme and the distinct functions companies may serve within it.

Example: an **AI & Compute Infrastructure** system can contain distinct
company roles, including:

- power
- equipment
- manufacturing
- compute
- networking
- cloud platforms

This lens describes the different functions companies may serve inside a
broader economic system. It does **not** mean:

- the portfolio is required to own every layer of a system, or any
  particular company;
- a system carries its own allocation sleeve, target, floor, or cap;
- a system functions as a new correlated-cluster cap under `targets.yaml`'s
  `caps.clusters` (that mechanism is unchanged and unrelated).

## B. Four capital types

Four descriptive categories for the purpose capital serves in the portfolio.
These are analytical labels, not tiers, not weights, and not executable
instructions. Sizing is controlled exclusively by approved tiers and targets
in `targets.yaml`; none of these four labels sets or implies a position size.

1. **Foundational Capital** — deep moats, critical infrastructure,
   resilience; purpose is long-term compounding.
2. **Growth Capital** — above-average growth supported by secular trends;
   purpose is to increase long-term portfolio growth.
3. **Optionality Capital** — meaningful upside with materially higher
   uncertainty; purpose is bounded asymmetric exposure.
4. **Tactical Capital** — capital whose thesis depends more heavily on
   valuation, cycle, or a specific temporary condition and therefore may
   warrant more frequent human review.

None of these four labels maps one-to-one onto `targets.yaml`'s tiers
(T1/T2/ETF/band/spec/crypto). A capital type is a reason a position might
exist; a tier is the config-encoded, already-governed mechanism that actually
sizes it. Restating a company's capital type is not a proposal to change its
tier.

## C. Portfolio reasoning hierarchy

```
Investment Constitution
    ↓
Economic Systems
    ↓
Company Roles
    ↓
Company Quality
    ↓
Capital Priority
    ↓
Tier
    ↓
Target Allocation
    ↓
Portfolio-HQ executes approved policy
```

This hierarchy describes how human reasoning can proceed toward an approved
policy decision. **It does not authorize any automated transition between
layers.** Each downward step — Company Quality to Capital Priority, Capital
Priority to Tier, Tier to Target Allocation — remains a distinct, manual,
separately-governed judgment. Nothing in this document, or in any future
record that references it, causes one layer to mechanically produce the
next.

## D. Initial enduring-system vocabulary

Reference examples only, not a mandatory, exhaustive, scored, weighted, or
allocator-consumed classification of the portfolio:

- AI & Compute Infrastructure
- Energy & Electrification
- Healthcare & Life Sciences
- Financial Infrastructure
- Digital Platforms & Enterprise Software

A company is not required to belong to any of these, or to exactly one. This
list may be amended only through a later, separately approved governance
decision. Whether these examples are used or left unused has no allocator,
tier, target, or portfolio-policy consequence.

## E. Standardized company-review vocabulary

A shared, descriptive checklist for discussing a company in committee-style
review. None of these terms compute a score, and none is a tier, weight, or
trade instruction.

- **Economic Role** — what function the company serves within a broader
  economic system (see A).
- **Moat** — the durability of the company's competitive advantage.
- **Bottleneck Power** — how structurally hard the company is to route
  around within its role.
- **Secular Tailwinds** — the multi-year demand trend the company benefits
  from, if any.
- **Financial Quality** — balance sheet strength, margin structure, cash
  generation.
- **Capital Allocation** — how management has historically deployed capital
  (buybacks, M&A, reinvestment, dividends).
- **Execution Risk** — the risk that management fails to convert opportunity
  into results.
- **Portfolio Uniqueness** — how much distinct exposure the company adds
  versus what's already held.
- **Replacement Candidate** — whether another holding could serve the same
  economic role, for discussion purposes only; naming a replacement
  candidate is not a recommendation to trim, add, or swap anything.
- **Capital Priority** — the human-reviewed case for whether additional
  capital deserves consideration relative to current policy and available
  alternatives; not a standing ranking, score, target-allocation
  instruction, or buy recommendation.

## F. Preserved distinctions

This vocabulary depends on keeping the following concepts separate.
Collapsing any two of them into one number or one instruction is exactly the
failure mode this document exists to prevent:

- **business quality** — the company's underlying fundamentals, independent
  of the portfolio;
- **economic/company role** — the descriptive ontology concept from
  Sections A and E; it does not correspond to, reinterpret, or substitute
  for `portfolio_role_ref` or any other Portfolio Intelligence field
  (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§14);
- **conviction** — the ordinal, human-set rating already governed by
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §12 and PI-0004's closed four-value
  vocabulary (`Low`/`Medium`/`High`/`Very High`), where a Portfolio
  Intelligence record exists;
- **capital priority** — the descriptive term in Section E, a qualitative
  review input, not a ranking, score, or instruction;
- **current tier** — the actual, config-encoded tier in `targets.yaml`;
- **target allocation** — the actual, config-encoded numeric weight in
  `targets.yaml`.

A high-quality business is not automatically the highest capital priority.
None of these concepts may be converted into an automatic numeric score or
allocation instruction by this document, or by any use of this document's
vocabulary, absent its own separate governance decision. Any future proposal
to add an ontology-referencing field to the Company or Theme YAML schema, or
to otherwise connect this vocabulary to `portfolio_role_ref` or any other
Portfolio Intelligence field, requires its own separate governance decision
under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s own change process — this
document does not propose, imply, or pre-approve one.

## G. What this document is not

- Not a scorecard. No field here produces a number.
- Not a roster classification requirement. No company or theme is required
  to have any ontology terms applied to it. Classification is optional; its
  absence is normal.
- Not a research program. No new standing analysis, monitoring, or scoring
  layer is created, requested, or implied by this document (see
  `constitution/INVESTMENT_CONSTITUTION.md` Principle 4 and CLAUDE.md's
  Decisions Log entries on the band-overlay and regime-gate backtests).
- Not an amendment to `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `targets.yaml`, or `holdings.yaml`.
- Not read by `allocate.py`, `margin_state.py`, or any other production code
  path, and no such read path is authorized by this document.

---

_Adopted by `governance/decisions/ONTO-0001-investment-ontology-freeze.md`.
Any future use of this vocabulary — in a Company Intelligence record, a
Theme Intelligence record, a committee review process, a report, or a
policy change — requires its own separate proposal and governance decision.
Terms in this document remain purely descriptive until such a decision
explicitly grants them a specific use._
