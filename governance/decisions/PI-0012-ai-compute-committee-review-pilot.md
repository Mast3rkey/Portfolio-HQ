---
decision_id: PI-0012
date: 2026-07-19
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0001, PI-0002, PI-0003, PI-0004, PI-0006, PI-0007, PI-0010, PI-0011, ONTO-0001]
supporting_artifact: null
---

## Context

A design-only architecture/governance session (this repository, 2026-07-19)
was asked to design a bounded committee-review pilot capable of later
producing a sourced, human-approved Company Intelligence record, using
`docs/INVESTMENT_ONTOLOGY.md`'s standardized company-review vocabulary
(`ONTO-0001`). That session performed no implementation, no external
research, and no repository writes — it is the source of this proposal.

Two separate authority gaps make this decision necessary before any such
pilot may proceed:

1. `ONTO-0001` authorizes only the existence of
   `docs/INVESTMENT_ONTOLOGY.md`. Its own text states: "A future use of this
   vocabulary in a Company Intelligence record, a Theme Intelligence record,
   **a committee review**, a report, or a policy decision requires its own
   separate proposal and its own separate governance decision." A
   committee-review process built on that vocabulary — even purely
   qualitative, non-scoring, advisory-only — is exactly the case ONTO-0001
   names and does not pre-approve.
2. `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §§20/24 state that freezing the
   specification never authorizes implementation. Every prior addition to
   `intelligence/companies/` or `intelligence/themes/` required its own
   bounded decision (`PI-0002`→`PI-0003` for COST, `PI-0005` for XOM,
   `PI-0006`→`PI-0007` for the `ai_infrastructure` theme pilot). A future
   company record needs the same authorization this decision supplies.

A repository review of ten candidate tickers (NVDA, TSM, ASML, AVGO, AMD,
AMAT, KLAC, LRCX, MRVL, INTC) against `targets.yaml`, `holdings.yaml`, and
`intelligence/companies/` found: all ten are currently held and are members
of `targets.yaml`'s `semis` correlated-cluster cap; NVDA already has a
Company Intelligence record and already references the `ai_infrastructure`
theme (`PI-0007`); **the remaining nine have no Company Intelligence
coverage of any kind.** AVGO was separately the subject of a tier-fit
governance/policy review (kept at T2, semis-correlation-flagged) — that is
governance and policy history, not a Company Intelligence record, and does
not count as coverage.

`ai_infrastructure`'s conceptual identity (`PI-0006`) is compute hardware
plus the electrical-power infrastructure supporting large-scale AI
workloads. Its own narrative deliberately permits later company-side
expansion without changing that identity, and the theme record itself
stores no reverse company membership (authority runs one way only, company
→ theme, per PI-0006). `PI-0007` authorized implementation of exactly the
NVDA and GEV company-side references to that theme.

This decision does not change that theme's conceptual scope and does not
modify `ai_infrastructure.yaml` or `.md`. It does, however, conditionally
authorize exactly one possible new company-side reference: see the Decision
section below for the precise conditional TSM→`ai_infrastructure` authority
this decision grants, and the boundary that authority does not cross. No
company other than TSM may reference the theme under this decision.

"AI Compute" is only the non-authoritative name of this bounded committee
review initiative. It is not a new Theme Intelligence record, an ontology
classification, an economic-system assignment, a schema value, a portfolio
sleeve, a target, or a cluster. No file called `ai_compute.yaml` or
`ai_compute.md` is authorized by this decision, and none is created by it.

## Decision

**Authorizes exactly six things, and nothing else:**

1. **Operational use of `docs/INVESTMENT_ONTOLOGY.md`'s Section E
   standardized company-review vocabulary** (Economic Role, Moat,
   Bottleneck Power, Secular Tailwinds, Financial Quality, Capital
   Allocation, Execution Risk, Portfolio Uniqueness, Replacement Candidate,
   Capital Priority) **strictly for the bounded, one-company TSM
   committee-review pilot** — as descriptive committee notes and future
   thesis-Markdown narrative only. This is the separate governance decision
   `ONTO-0001` itself requires before any committee review may use its
   vocabulary. It does **not** add any ontology-referencing field to
   `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s Company or Theme YAML schema,
   does **not** connect any ontology term to `portfolio_role_ref`, and
   grants no authority to apply this vocabulary to any company other than
   TSM. Later governance decisions may adopt this template or evidence
   standard by explicit reference, but PI-0012 itself grants no authority
   to apply it to another company.
2. **The eleven-question qualitative review template** (Economic role,
   Investment thesis, Moat, Bottleneck power, Financial quality, Capital
   allocation, Secular tailwinds, Execution risk, Portfolio uniqueness,
   Replacement candidate, Capital Priority — bounded to `ONTO-0001`'s own
   definition, never a score), documented here as the **approved
   methodology for the TSM pilot only** — not as a standing operational
   process for the rest of the roster. Explicitly prohibited in any
   application of this template: numeric company scores, weighted
   scorecards, league tables, automatic rankings, "best company"
   declarations, next-dollar recommendations, mechanical
   promotion/demotion, automatic tier or target changes.
3. **The TSM-specific research-evidence standard**: primary-source priority
   order (official filings/IR materials; regulatory filings; official
   customer/supplier disclosures; government/industry-primary sources;
   high-quality secondary sources for corroboration/context only); per
   material claim, a recorded exact source, publication date, the specific
   claim supported, primary-vs-secondary classification, confidence
   limitation, unresolved contradictions, and any information that could
   not be independently verified; and explicit separation of established
   facts, management claims, analyst interpretation, and committee
   inference. This standard governs TSM's future draft only.
4. **Future creation, after all required human approvals below, of exactly**
   `intelligence/companies/TSM.yaml` and `intelligence/companies/TSM.md`,
   through a later, separately reviewed implementation PR. This decision
   creates neither file itself.
5. **Conditional TSM → `ai_infrastructure` theme reference.** PI-0012
   conditionally authorizes exactly one possible new company-side theme
   reference: TSM may reference `ai_infrastructure` in its future Company
   Intelligence YAML only if the TSM research review demonstrates that the
   company meets the existing theme record's Non-membership standard **and**
   the human principal explicitly approves both that conclusion and the
   exact `themes: [ai_infrastructure]` value. If either condition is not
   satisfied, the TSM record must omit the theme reference. This conditional
   authority applies only to TSM: it does not authorize a reference for any
   other company, does not modify the theme's conceptual identity, does not
   modify `ai_infrastructure.yaml` or `.md`, does not store reverse
   membership, and does not treat theme membership as a tier, sizing, or
   allocation conclusion.
6. **The governance-index entry and `CLAUDE.md` pointer entry associated
   with this decision** — modifications to the existing
   `governance/decisions.yaml` and `CLAUDE.md` files, not new files, filed
   in this same PR.

### Selection rationale (neutral — no research conclusion prejudged)

TSM has a materially different business model from NVDA's existing Company
Intelligence subject, making it a useful one-company test of whether the
review framework works across different business models without expanding
the pilot beyond one company. This decision does not conclude, assume, or
imply that TSM holds a chokepoint, a bottleneck, an irreplaceable
manufacturing role, or any other substantive review finding — those are
exactly the questions the future committee review is meant to test, not
answers this governance decision supplies in advance. The future research
must independently determine TSM's economic role, moat, bottleneck power,
financial quality, portfolio uniqueness, and every other substantive review
conclusion listed in the template above.

### Authorized TSM pilot review questions

This subsection is the authoritative record of the eleven-question
methodology referenced in Decision item 2, so the full methodology survives
in the repository independent of any external conversation. It applies only
to the TSM pilot (see "Applies only to TSM" below).

1. **Economic/company role**
   - What function does TSM serve within the relevant economic system or
     supply chain?
   - Is this descriptive role distinct from its `portfolio_role_ref`, which
     remains only a human-authored tier/category reference?

2. **Investment thesis**
   - What is the durable, long-term reason to own or monitor TSM?
   - Which secular demand drivers support that thesis?
   - Which claims are established facts versus committee inference?

3. **Moat**
   - What makes TSM difficult to displace?
   - Is the advantage technological, structural, regulatory, ecosystem-based,
     scale-based, customer-embedded, or some evidenced combination?
   - What could realistically weaken it?

4. **Bottleneck power**
   - Does TSM control a real chokepoint?
   - Can customers route around it?
   - What substitutes or alternative suppliers exist?
   - The review must be permitted to conclude that no durable bottleneck is
     established.

5. **Financial quality**
   - What does the evidence show about balance-sheet strength?
   - Margin and cash-generation quality?
   - Reinvestment requirements?
   - Capital intensity and cyclicality?

6. **Capital allocation**
   - How has management deployed cash among reinvestment, acquisitions,
     buybacks, dividends, and balance-sheet priorities?
   - What evidence supports value creation or destruction?
   - Do not use stock-price performance alone as proof.

7. **Secular tailwinds**
   - Which multi-year structural demand drivers are evidenced?
   - Which apparent strengths may instead reflect a temporary semiconductor
     cycle?

8. **Execution risk**
   - What must management successfully execute in the future?
   - Which parts of the thesis are already established versus dependent on
     future delivery?

9. **Portfolio uniqueness**
   - What distinct exposure would TSM add to the documented portfolio
     reasoning?
   - Which current holdings overlap with that exposure?
   - What economically important exposure, if any, would be absent without
     TSM?

10. **Replacement candidate**
    - Which current holding or outside alternative could perform a similar
      economic function?
    - This is descriptive comparison only and is not a recommendation to
      replace, sell, trim, buy, or add anything.

11. **Capital Priority**
    - Apply only `ONTO-0001`'s bounded definition: the human-reviewed case
      for whether additional capital deserves consideration relative to
      current policy and available alternatives.
    - Do not produce a score, ranking, league table, next-dollar list, buy
      recommendation, target-weight instruction, promotion, or demotion.

**Output-mapping rule:**

- These eleven dimensions belong in the human review packet and future TSM
  Markdown narrative.
- They do not create eleven new YAML fields.
- `TSM.yaml` must remain within the existing frozen Company Intelligence
  schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9).
- No ontology field, scorecard field, or connection to `portfolio_role_ref`
  is authorized.

**Applies only to TSM:** this methodology is documented here as the
approved TSM-pilot review process. It has no standing authority over any
other company. A future decision may adopt it by explicit reference for a
different company; PI-0012 itself grants no such authority.

### Required human approvals before any implementation PR opens (TSM)

Research scope; sources; economic-role description; risks and catalysts;
`portfolio_role_ref` (descriptive only, per `PI-0003`'s unchanged doctrine,
fixed at authoring time, not derived from `targets.yaml`); the conditional
theme-reference decision described in Decision item 5 above — explicit human
approval of both (a) the conclusion that TSM's evidence meets
`ai_infrastructure.yaml`'s own Non-membership standard, and (b) the exact
`themes: [ai_infrastructure]` value, or, failing either, the record must
omit the theme reference entirely; final YAML; final Markdown narrative.

**Conviction rating**, specifically: either (a) human approval of
`conviction.rating` where a rating is included, and any included value must
be exactly one of `PI-0004`'s four frozen values — Low, Medium, High, Very
High, never computed or inferred — or (b) explicit human approval that
`conviction.rating` is omitted because the evidence does not support
selecting one. A decision to omit the rating does not itself authorize or
require the TSM record to be created; the complete final YAML and Markdown
still require their own separate human approval regardless of how the
conviction question is resolved.

**No draft automatically becomes an accepted Intelligence record.**

### No presumed second company

All nine uncovered non-NVDA candidates (TSM, ASML, AVGO, AMD, AMAT, KLAC,
LRCX, MRVL, INTC) remain deferred, not rejected, except that this decision
authorizes TSM as the one pilot subject. PI-0012 establishes no sequence or
presumption for a second company. Any second company — including but not
limited to ASML — requires its own later proposal and its own separate
governance decision, made after the TSM pilot is evaluated, following the
same review-gate discipline `PI-0004` applied to close the COST pilot
before `PI-0005` authorized XOM.

### Prohibited — explicit authority boundary

This decision explicitly prohibits, and none of the following is authorized
under any interpretation:

- any research conclusion about TSM (economic role, moat, bottleneck power,
  financial quality, portfolio uniqueness, or any other substantive
  finding) — those remain for the future committee review to determine;
- any Company Intelligence, Theme Intelligence, research, schema,
  implementation, report, or AI Compute artifact creation in this
  governance-only PR, including no `TSM.yaml`, `TSM.md`, `ai_compute.yaml`,
  or `ai_compute.md`. This governance-only PR changes exactly three files.
  It creates exactly one new file — this governance decision file
  (`governance/decisions/PI-0012-ai-compute-committee-review-pilot.md`) —
  and modifies exactly two existing files: `governance/decisions.yaml`, by
  adding the PI-0012 index entry, and `CLAUDE.md`, by adding the PI-0012
  Decisions Log pointer. It creates no investment-research or Intelligence
  artifact;
- any second AI Compute company beyond TSM (ASML, AVGO, AMD, AMAT, KLAC,
  LRCX, MRVL, INTC, and any re-review of NVDA all remain unauthorized, with
  no presumed sequence);
- any company-side theme reference for TSM other than `ai_infrastructure`;
  PI-0012 conditionally authorizes only the exact TSM → `ai_infrastructure`
  reference described in Decision item 5, and only when both required
  evidence and human-approval conditions are satisfied;
- any new company-side theme reference for any company other than TSM under
  this decision. The existing NVDA and GEV references remain unchanged and
  continue to derive their authority solely from `PI-0007`;
- any new Theme Intelligence record;
- any change to `ai_infrastructure.yaml`/`.md`, `COST.yaml`/`.md`,
  `GEV.yaml`/`.md`, `ISRG.yaml`/`.md`, `TMO.yaml`/`.md`, or `XOM.yaml`/`.md`;
- any change to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s schema, including no
  ontology-referencing field of any kind;
- any change to `docs/INVESTMENT_ONTOLOGY.md` itself;
- any change to `intelligence_validator.py`, `intelligence_report.py`, or
  either module's tests;
- any numeric company score, weighted scorecard, league table, automatic
  ranking, or "best company" declaration;
- any next-dollar, buy, sell, trim, promotion, or demotion recommendation;
- any change to `allocate.py`, `margin_state.py`, `targets.yaml`,
  `holdings.yaml`, any tier, target, cap, cluster, or weight;
- any classification of the full roster, or any ticker beyond TSM, against
  the ontology vocabulary;
- extending the eleven-question template or the research-evidence standard
  to any company beyond TSM without a further governance decision adopting
  them by explicit reference.

## Rationale

Same discipline `PI-0002`/`PI-0003` applied to Company Intelligence,
`PI-0006`/`PI-0007` applied to Theme Intelligence, and `PI-0011` applied to
Intelligence Operations: a frozen specification or reference artifact
describing intended future use is not itself authorization to build or
operationally use it. `ONTO-0001` explicitly names "a committee review" as
requiring its own separate decision before its vocabulary may be used —
this decision supplies exactly that, scoped as narrowly as every prior
bounded pilot in this repository's history, and no more broadly than one
company.

Filed under the `PI-####` series rather than a new `ONTO-0002`, following
`PI-0010`'s own precedent reasoning: the substantive domain of this
decision is a Portfolio-Intelligence-producing process (a committee review
whose output is a future Company Intelligence record), not a change to the
ontology reference document itself. `ONTO-0001` is listed in
`related_decisions` and this decision's own text states plainly that it
satisfies `ONTO-0001`'s "separate governance decision" requirement — a
second, `ONTO`-prefixed file would add no additional authorization, only
duplicate paperwork for one bounded scope. `PI-0004` is listed in
`related_decisions` in place of `PI-0005` because this decision's
conviction-handling correction (optional rating, exact frozen vocabulary,
or explicit human approval of omission) directly extends `PI-0004`'s own
closed four-value vocabulary and "reviewed pilot" completion-criterion
precedent; `PI-0005`'s XOM-specific selection reasoning is not relied upon
here.

TSM-only, not a batch: matches the smallest-reversible-step discipline this
repository has applied to every prior gate (rungs, trims, weights, the
T1/T2 ceiling, and every Company/Theme Intelligence pilot to date) — one
company lets the eleven-question template and the ontology-vocabulary-in-a-
committee-review approach get reviewed before any roster-wide pattern is
set. The selection rationale is deliberately limited to a neutral,
process-testing justification (a materially different business model from
NVDA's existing record) rather than any claim about TSM's economic role,
moat, or bottleneck position — those are the review's own open questions,
not inputs this governance decision is positioned to answer.

## Alternatives Considered

- **Authorize all ten candidates, or a multi-company batch, simultaneously.**
  Rejected: violates the smallest-reversible-step discipline `PI-0003`
  established and invites exactly the research sprawl and inconsistent-
  standards risk a one-company pilot is designed to avoid.
- **File as `ONTO-0002` instead of `PI-0012`.** Considered: `ONTO-0001` is
  literally the decision whose authorization requirement this satisfies.
  Rejected on the same domain-substance basis `PI-0010` already used to
  choose `PI-####` over `GOV-####` for a Portfolio-Intelligence-substantive
  decision: this decision's output is a company-review pipeline feeding
  Portfolio Intelligence, not a change to the ontology document.
  Two separate decisions (`ONTO-0002` + `PI-0012`) were also considered and
  rejected as unnecessary ceremony for one coherent, bounded scope.
- **Create a narrower `ai_compute` Theme Intelligence record instead of a
  committee-review process.** Rejected: `ai_infrastructure`'s own narrative
  already anticipates covering more compute-hardware companies without
  changing its identity; a second theme would fragment one demand
  narrative for no stated benefit, the same reasoning `PI-0010` used to
  reject a second Portfolio-Intelligence-adjacent spec document.
- **Name ASML, or any other ticker, as the presumed next candidate.**
  Rejected: prejudging a sequence beyond the one authorized pilot subject
  is exactly the kind of premature commitment `PI-0003`'s one-company-first
  discipline exists to prevent. All nine uncovered non-NVDA candidates are
  left equally deferred.
- **Require `conviction.rating` on the future TSM record.** Rejected in
  favor of allowing explicit, human-approved omission — the evidence for a
  single, freshly-reviewed company may not support a confident rating, and
  forcing one would risk exactly the vocabulary misuse `PI-0004` was
  designed to prevent (a rating chosen to fit the field rather than the
  evidence).
- **State a substantive conclusion about TSM's economic role or moat in
  this governance decision, to give the future implementation a head
  start.** Rejected: governance decisions in this repository authorize
  process and scope, they do not pre-decide the substantive research
  findings a human-reviewed record is supposed to independently establish.

## Consequences

`docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`intelligence_validator.py`, `intelligence_report.py`, `allocate.py`,
`margin_state.py`, `targets.yaml`, `holdings.yaml`, `README.md`, and every
existing `intelligence/companies/*`/`intelligence/themes/*` record remain
unchanged. `governance/decisions.yaml` gains one new row for this entry.
`CLAUDE.md`'s Decisions Log gains one short pointer entry, consistent with
the `GOV-0001`/`PI-0010`/`ONTO-0001`/`PI-0011` pattern. No company file,
theme file, schema change, or allocator-visible behavior exists as a result
of adopting this decision alone — a future, separately-reviewed
implementation PR is required to create `TSM.yaml`/`TSM.md`, gated behind
the human approvals listed above. No second company, no new theme, and no
extension of the template or evidence standard beyond TSM is authorized;
each would require its own future, separately-approved governance decision.
TSM's own future record may or may not reference `ai_infrastructure`,
exactly as conditioned under Decision item 5 — this decision does not
itself add, default-authorize, or guarantee that reference; it becomes real
only if both required approvals are separately obtained.
