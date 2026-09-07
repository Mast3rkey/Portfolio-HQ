---
decision_id: PI-0016
date: 2026-07-21
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0004, PI-0006, PI-0007, PI-0009, PI-0010, PI-0011, PI-0012, PI-0013, PI-0014, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0012-ai-compute-committee-review-pilot.md` authorized
an eleven-question qualitative review methodology and a research-evidence
standard **strictly for the bounded, one-company TSM pilot** — not "as a
standing operational process for the rest of the roster." `governance/
decisions/PI-0013-tsm-pilot-review-closure.md` closed that pilot's gate,
reaffirmed the method and evidence standard remain "TSM-only," and required
that **any future decision that explicitly adopts PI-0012's method for another
company must also require, before final human approval, a repository-fact
reconciliation** against `targets.yaml`, `holdings.yaml`, the current
`intelligence/companies/` inventory, and relevant company-side theme
references. PI-0013 also declined to define, rank, or freeze next-company
selection criteria, leaving that to "a future, separate proposal."

A same-session, read-only design review (this repository, 2026-07-21)
produced a governance-design report recommending a standing, reusable version
of PI-0012's methodology, reviewed by the human principal, who approved it
**with three corrections**:

1. Per-company selection must be its own durable, repository-filed governance
   record — not an informal chat sign-off — stating and justifying its own
   selection criteria, per PI-0013's own requirement.
2. A review must produce two independent conclusions, not one: an advisory
   policy recommendation, and a separate Intelligence-maintenance
   recommendation — because a company's governed tier and target can remain
   correct while its Company Intelligence record independently needs newer
   evidence (or vice versa).
3. The bounded capital-priority comparison must be tightened to a named,
   justified two-to-five-company comparator set, scoped to specific
   dimensions, with no scoring, ranking, or persistent comparison structure of
   any kind.

The same review also corrected a factual misstatement in its own prior
report: `supporting_artifact: null` (used by `PI-0004`-lineage decisions,
including `PI-0012` through `PI-0015`) means only that no *separate* backing
artifact was preserved — it does not mean the governance decision itself
went unfiled. The accepted ADR file and its `governance/decisions.yaml` index
row are themselves the durable repository record regardless of whether a
supporting artifact exists. This decision's own Lifecycle section (H) states
that distinction explicitly so it is not misread again.

This decision is the standing framework the principal approved, incorporating
all three corrections.

## Decision

**PI-0016 authorizes exactly one thing: a standing, reusable methodology for
future, bounded, one-company-at-a-time Investment Committee reviews.** It
authorizes no specific company, no research, no Intelligence-record change,
and no policy, tier, target, roster, cluster, cap, or allocator change. Every
one of those remains gated behind its own separate authorization, exactly as
before this decision.

### A. Standing review dimensions

A future review conducted under PI-0016 addresses, narratively:

1. Economic role
2. Investment thesis
3. Moat
4. Bottleneck power
5. Financial quality
6. Capital allocation
7. Secular tailwinds
8. Execution risk
9. Portfolio uniqueness
10. Replacement candidate
11. Capital priority (see §E for the bounded comparison rule)
12. Risks and observable thesis-break conditions
13. Current governed tier and target context (reported, not decided, here)
14. Advisory policy recommendation (see §F)
15. Intelligence-maintenance recommendation (see §F)

These are review-packet narrative dimensions only. **They create no YAML
field, scorecard field, schema change, computed value, or allocator input.**
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s Company YAML schema (§9) is unchanged
by this decision; a future record produced after a review still must fit that
existing schema without modification, or its own separate schema-change
decision is required.

### B. Separate, durable, per-company research authorization — required

**PI-0016 does not itself select or authorize research on any company.**
Before research begins on a specific company, a separate, narrow,
repository-filed governance decision (its own `.md` file under
`governance/decisions/`, its own `governance/decisions.yaml` row, its own
`CLAUDE.md` pointer) must:

- name exactly one ticker;
- state and justify why that company was selected;
- adopt PI-0016's methodology (§A) and evidence standard (§D) by explicit
  reference, rather than restating or redesigning them;
- define the bounded research scope;
- identify the comparator set or the comparator-selection method to be used
  under §E;
- state the evidence limitations already known at authorization time;
- authorize **research only**;
- explicitly prohibit, in its own text, any Company Intelligence, policy,
  target, tier, roster, cluster, cap, allocator, code, or implementation
  change.

That later authorization should be concise — its job is to select and scope
one company, not to re-derive a methodology PI-0016 already supplies.
**An informal conversational or chat-only sign-off is not sufficient** to
authorize a company-specific review; the authorization must be a filed
repository governance record before research begins, consistent with
`PI-0013`'s own requirement that a future selection proposal "state and
justify its own selection criteria."

### C. Repository-fact reconciliation — applies by default

Every review conducted under PI-0016 must apply `PI-0013`'s reconciliation
gate before final human approval of that review's Portfolio Uniqueness
finding, Replacement Candidate finding, capital-priority comparison, and any
resulting draft YAML/Markdown: verify the review's factual claims against
current `targets.yaml`, `holdings.yaml`, the current `intelligence/
companies/` inventory, relevant company-side `themes:` references, and
current tier/target/cluster policy. This may remain a manual, read-only
review step, documented in the review packet or implementation-PR narrative,
exactly as `PI-0013` already permits — no new script, validator, or test is
required or authorized by this requirement. A discovered mismatch is
advisory: it does not itself determine which source is wrong or require
either source to change.

### D. Evidence standard

Every review conducted under PI-0016 uses one reusable evidence standard,
generalized from `PI-0012`'s TSM-specific standard:

- primary sources first: SEC or applicable regulatory filings; issuer
  investor-relations materials; official customer, supplier, and competitor
  disclosures; government and industry-primary sources;
- reputable secondary sources used only for corroboration or for facts
  unavailable from a primary source;
- for every material claim: exact source, publication date, the specific
  claim it supports, and a primary-vs-secondary classification;
- explicit, separate labeling of established fact, management claim,
  third-party claim, committee inference, and unresolved uncertainty;
- an active search for disconfirming evidence, not merely confirming
  evidence;
- disclosure of inaccessible evidence and unresolved contradictions, rather
  than silent omission;
- no valuation conclusion without a disclosed methodology, date, and source
  basis;
- no false precision.

### E. Bounded capital-priority comparison

A review conducted under PI-0016 may answer, for its one subject company
only: *"if one new dollar were available, why should it go to this company
instead of the next-best available portfolio alternative?"* — as a bounded,
human-reviewed qualitative comparison against **exactly two to five named
alternatives**. The comparator set is not free to be invented once research
has already begun. Every company-specific filed authorization under §B must
do exactly one of the following:

1. **name the exact two-to-five comparator set** the review will use; or
2. **define and justify a deterministic, relevance-based qualifying rule**
   that produces a complete set of two to five companies **without ranking,
   ordering, or scoring them.** An acceptable method states a criterion for
   *membership* in the comparator set, not a criterion for *ordering*
   candidates against each other — for example: "all other currently held
   companies that share the subject company's governed correlated-cluster
   membership, but only when that complete qualifying set contains between
   two and five companies." A method must never rely on company ranking,
   portfolio-weight ranking, target-gap ranking, conviction ranking, quality
   ranking, numeric scoring, or any other ordered league-table logic — a
   method answers only "does this candidate qualify," never "which
   qualifying candidates rank highest."

**When a proposed method would produce fewer than two companies, more than
five companies, or an ambiguous set that would require discretionary
ordering, ranking, or selection to narrow down to two-to-five, the
company-specific filed authorization must instead name the exact
two-to-five comparator set** — a method is only usable when it is precise
enough, on its own, to yield a complete, unambiguous two-to-five-company set
with no further judgment call.

When the authorization names the exact set, the review packet uses that set
and no other. When the authorization instead defines a qualifying method,
the review packet may name its final two-to-five comparators only by
applying that pre-authorized method exactly as stated. **The review packet
may not narrow, expand, order, rank, substitute, or otherwise modify the
pre-authorized set** — there is no review-packet-only, post-hoc comparator
selection.

For each comparator actually used, the review must state **all** of the
following:

- why that comparator is **substantively relevant** to this subject
  company's capital-priority review (satisfying a pre-authorized method is
  not itself a substitute for this explanation — the review must still
  explain the comparator's relevance in its own terms);
- when a qualifying method was used, why this specific comparator satisfies
  that pre-authorized method;
- its own distinct economic role;
- its principal overlap or complementarity with the subject company;
- the opportunity-cost reason capital might instead go to it.

The comparison is written entirely inside the one subject company's review
packet. **Explicitly prohibited, without exception:**

- a standing ranking of any companies against each other;
- a league table;
- numeric or weighted scoring of any kind, including any comparator-set
  qualifying method that ranks, orders, or scores candidates rather than
  merely testing membership;
- a computed or derived conviction value;
- an automated or recurring next-dollar list;
- a live or stored opportunity map;
- a price target;
- a recurring buy/sell signal;
- allocator coupling of any kind;
- an automatic promotion, demotion, or target change;
- a persistent cross-company comparison database, index, or table of any
  kind, inside or outside `intelligence/`.

### F. Two independent recommendations

A review conducted under PI-0016 must state exactly one value from **each**
of the following two independent vocabularies. Neither recommendation grants
implementation authority; both are advisory only, for the principal's
separate decision.

**1. Advisory policy recommendation** — exactly one of:
- Keep current policy
- Recommend promotion
- Recommend demotion
- Recommend target increase
- Recommend target reduction
- Hold pending specified evidence

**2. Intelligence-maintenance recommendation** — exactly one of:
- No Intelligence update needed
- Intelligence refresh recommended
- Intelligence update held pending specified evidence

These two vocabularies are deliberately independent: a company's governed
tier and target may remain entirely correct while its Company Intelligence
record independently needs newer evidence (stale sources, a materially
changed factual picture since the record's `review.last_reviewed` date), or
the reverse may hold. Collapsing the two into one conclusion would obscure
which of two different problems — a policy question or a record-maintenance
question — a review actually found.

### G. No automatic program

**PI-0016 authorizes no automatic review cadence, no recurring company-review
process, no monitoring queue, no full-roster sweep, no company-review
sequence, no entitlement for any company to be reviewed, no mandatory
ontology classification, no mandatory economic-system membership, and no
research automation.** Every review begins only after its own separate,
company-specific research authorization under §B. Adoption of this standing
methodology does not itself schedule, queue, or imply that any particular
company — including but not limited to NVDA, or any of the eight `PI-0012`
pool members still deferred, or INTC/SYK/DHR under `PI-0014` — will be
reviewed next, or ever.

### H. Lifecycle

```
PI-0016 standing methodology (this decision, filed once)
  → separate, company-specific, repository-filed research authorization (§B)
  → bounded research
  → repository-fact reconciliation (§C, PI-0013's gate)
  → human review
  → advisory policy recommendation (§F.1) and Intelligence-maintenance
    recommendation (§F.2)
  → principal decision
  → separate Intelligence-record creation/update authorization, if needed
  → separate tier/target/roster/cluster/cap/other policy governance, if
    needed
  → implementation
  → validation
  → merge / effectiveness
```

An unfiled conversational review — research or analysis discussed in a
session but not carried through a filed governance decision — is context
only. It is not repository authority, must not later be cited as repository
truth, and may end without any repository mutation if no durable record or
policy change is warranted; that is a valid, complete outcome, not an
incomplete one. If such conversational findings are later relied on for any
further step, they must first be independently re-verified and carried
through their own authorized filing.

**Factual clarification:** `supporting_artifact: null`, as used on this and
prior `PI-####` decisions, means only that no separate backing artifact
(e.g. a backtest report) was preserved alongside the decision. It does not
mean the decision itself is unfiled or informal — the accepted `.md` file
under `governance/decisions/` and its `governance/decisions.yaml` index row
are themselves the durable, repository-authoritative record, exactly as for
every other decision using that same convention (`PI-0012` through
`PI-0015`).

### I. Explicit prohibitions

This decision authorizes none of the following, under any interpretation:

- selecting any company for review;
- conducting research on any company;
- creating or modifying any Company or Theme Intelligence record;
- any ontology field, schema field, or vocabulary freeze beyond what
  `ONTO-0001` already froze;
- any numeric score or ranking, standing or otherwise;
- any change to any target, tier, roster, cluster, cap, or `holdings.yaml`
  value;
- any allocator or margin integration;
- any report generator, validator, or test change;
- any change to production code (`allocate.py`, `margin_state.py`,
  `intelligence_validator.py`, `intelligence_report.py`, or any other module);
- any trade or order of any kind;
- any amendment to `constitution/INVESTMENT_CONSTITUTION.md`;
- any amendment to `docs/INVESTMENT_ONTOLOGY.md`;
- any amendment to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.

## Rationale

Same discipline `PI-0002`/`PI-0003` applied to Company Intelligence,
`PI-0006`/`PI-0007` applied to Theme Intelligence, and `PI-0012`/`PI-0013`
applied to the TSM pilot: a reusable methodology is authorized once, narrowly,
and separately from any authority to use it on a specific subject. `PI-0012`
itself limited its method to TSM "not as a standing operational process for
the rest of the roster" — precisely because generalizing a review method and
generalizing authority to apply it to any company are two different
questions. This decision answers only the first question. The second
question — which company, if any, is reviewed next — remains exactly as
open as `PI-0013` left it, and is answered, every time, by its own new,
separately justified, repository-filed decision (§B) — never by this one.

Splitting the capital-priority comparison into a bounded, named,
two-to-five-comparator structure (§E) rather than an open-ended qualitative
comparison follows directly from `ONTO-0001`'s own boundary: "Capital
Priority" is a descriptive, human-reviewed input, not a ranking or score, and
bounding the comparator set in both count and required content is what keeps
a single-company review from silently becoming a portfolio-wide ranking
exercise no governance decision has authorized.

Splitting the review's conclusion into two independent recommendations (§F)
reflects a real, previously-uncaptured distinction: a company's tier and
target are `targets.yaml`'s domain, while its Company Intelligence record's
currency is a separate, `review.next_due`-driven concern (`docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §13, §18; `PI-0011`'s staleness reporting).
A single review that only ever produced one policy-shaped conclusion would
have no way to say "the tier is still right, but the record needs new
sources." This distinction was identified during the principal's later
review of the standing-framework design, using the prior NVIDIA discussion
as the concrete example: current policy may remain appropriate while the
supporting Company Intelligence record independently needs refreshed
evidence. `PI-0013` itself made no such finding — its actual authority is
the repository-fact reconciliation gate, the holdings/targets/Intelligence/
theme verification it requires, and its deliberate refusal to freeze a
standing candidate-selection doctrine, all unchanged and unextended by this
paragraph.

Requiring per-company selection to be its own filed decision (§B), rather
than an informal sign-off, follows `PI-0013`'s own text precisely: "a future,
separate candidate-selection proposal must state and justify its own
selection criteria." A standing methodology reduces the cost of that future
decision (it no longer needs to redesign the review method itself) without
reducing its status as a real, auditable, repository-filed governance record.

`related_decisions` lists `GOV-0001` (the governance-decision-record layer
this file is filed under); `PI-0004` (the two-recommendation split's closest
precedent — its own closed conviction vocabulary and five-part pilot-review
test, referenced here for the same "don't blur two questions into one"
discipline); `PI-0006`/`PI-0007`/`PI-0009` (the Theme Intelligence precedent
for freezing a reusable data model separately from authorizing its use);
`PI-0010` (the `PI-####`-over-`GOV-####`/`ONTO-####` domain-substance
reasoning this decision follows in choosing its own prefix); `PI-0011` (the
reconciliation-adjacent staleness/role-drift precedent, and the "freeze is
not authorization to build" discipline applied a third time here); `PI-0012`
(the TSM-only method and evidence standard this decision generalizes);
`PI-0013` (the reconciliation gate this decision applies by default, and the
selection-criteria requirement §B directly implements); `PI-0014` (the most
recent bounded, per-candidate evidence-review precedent, itself narrower than
a full committee review); and `ONTO-0001` (the vocabulary this decision's §A
and §E operate under, without reopening or extending it).

## Alternatives Considered

- **Adopt Option A (NVDA-specific second pilot only).** Rejected: solves
  nothing for any company besides NVDA and would require re-deriving the
  whole methodology again for the next company after that — the exact
  repeated cost this decision exists to remove.
- **Adopt Option B (an AI-compute-company-specific framework).** Rejected:
  risks `ai_compute` being read as a de facto theme, sleeve, or system despite
  `PI-0012`'s explicit disclaimer that it is not one, and still requires a
  wholly separate framework for every other sector of the roster.
- **Adopt Option D (continue one full governance decision, methodology and
  all, per company).** Rejected: this is the status quo the principal asked
  to move past — every future company would re-litigate the reusable review
  methodology, evidence standard, and capital-priority boundary `PI-0012`
  already worked out once.
- **Let per-company selection be an informal chat approval instead of a
  filed decision.** Rejected per the principal's explicit correction:
  `PI-0013` requires a future selection proposal to state and justify its own
  criteria, and an unfiled approval is not repository truth or institutional
  memory — it cannot be audited, cited, or relied on by a future session the
  way a filed `.md` file and index row can.
- **Allow an unbounded qualitative capital-priority comparison against "the
  rest of the portfolio."** Rejected per the principal's explicit correction:
  an unbounded comparison drifts toward an implicit full-roster ranking with
  no stated boundary on count or content; naming exactly two to five
  comparators, each independently justified, keeps the comparison inside one
  company's review without creating a portfolio-wide ranking artifact.
- **Produce one combined recommendation instead of two independent ones.**
  Rejected per the principal's explicit correction: a single recommendation
  cannot distinguish a policy question from a record-maintenance question,
  and the NVIDIA-review discussion earlier this session is a concrete
  example of exactly that ambiguity arising in practice.
- **Treat `supporting_artifact: null` as meaning "this review was never
  really filed."** Rejected: this was an identified factual error in the
  prior report, corrected explicitly in §H — the field describes only the
  absence of a *separate* backing artifact, not the status of the ADR itself.

## Consequences

`docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`constitution/INVESTMENT_CONSTITUTION.md`, `intelligence_validator.py`,
`intelligence_report.py`, every test file, `allocate.py`, `margin_state.py`,
`targets.yaml`, `holdings.yaml`, and every existing `intelligence/companies/*`
and `intelligence/themes/*` record are unchanged. `governance/decisions.yaml`
gains one new row for this entry. `CLAUDE.md`'s Decisions Log gains one short
pointer entry, consistent with the `GOV-0001`/`PI-0010`/`ONTO-0001`/`PI-0011`
pattern.

**No company is selected, authorized for research, or implied to be next by
this decision.** A future review of any company — NVDA included — requires
its own separate, filed research authorization under §B, adopting this
decision's methodology and evidence standard by reference, before any
research may begin. No Intelligence record, tier, target, roster, cluster,
cap, or allocator change is authorized by this decision alone; each remains
its own separate, future, separately-approved governance decision.
