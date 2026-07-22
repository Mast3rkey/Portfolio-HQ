---
decision_id: PI-0017
date: 2026-07-22
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, AUTO-0001, PI-0004, PI-0006, PI-0007, PI-0009, PI-0012, PI-0013, PI-0016, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0016-standing-company-review-framework.md` froze a
standing, reusable Investment Committee review methodology (15 narrative
dimensions in §A, a reusable evidence standard in §D, a bounded 2-5-comparator
capital-priority structure in §E, two independent recommendation outputs in
§F, and `PI-0013`'s repository-fact reconciliation gate applying by default
in §C) but authorized no company-specific use of it. PI-0016 §B requires that
"before research begins on a specific company, a separate, narrow,
repository-filed governance decision ... must name exactly one ticker, state
and justify why that company was selected, adopt PI-0016's methodology and
evidence standard by explicit reference, define the bounded research scope,
identify the comparator set ..., state the evidence limitations already known
at authorization time, authorize research only, and explicitly prohibit any
Company Intelligence, policy, target, tier, roster, cluster, cap, allocator,
code, or implementation change." This decision is that separate,
company-specific authorization, naming NVDA.

NVDA already carries a Company Intelligence record
(`intelligence/companies/NVDA.yaml`/`.md`), created and human-approved under
`PI-0007` as part of the `ai_infrastructure` Theme Intelligence pilot. NVDA is
also one of the seven tickers enrolled, but currently dormant
(`monitoring_enabled: false`), in `AUTO-0001`'s freshness registry. Neither
fact by itself authorizes a PI-0016 committee review — `PI-0007` authorized
only the existence of the current record, and `AUTO-0001` authorizes no
research or review activity of any kind. This decision supplies the review
authorization those two records do not.

Repository facts, reported here as background only: `PI-0013` permits tier,
target weight, raw share count, ownership, and cluster membership to be
reported as context, but not treated as evidence of company quality,
conviction, theme eligibility, or automatic entitlement to become the next
review subject. Relevant company-side theme references are factual inputs
to the repository-fact reconciliation required by `PI-0016` §C and
`PI-0013`; they do not independently establish capital priority. Confirmed
directly against `targets.yaml` and `holdings.yaml` at filing time: NVDA is
a T1 holding at a 3.35% per-name target, held at 0.917642 shares, and is a
member of the `semis` correlated-cluster cap (25% of book) alongside TSM,
ASML, and AVGO; `NVDA.yaml` references the `ai_infrastructure` theme. These
facts are recorded for the reconciliation this decision requires of the
future review — they are not themselves review findings and do not
prejudge one.

## Decision

**PI-0017 authorizes exactly one thing: bounded, research-only committee
review activity on NVDA, conducted under PI-0016's standing methodology.** It
authorizes no research conclusion, no Company or Theme Intelligence change,
and no policy, tier, target, roster, cluster, cap, or allocator change. Each
of those remains gated behind its own separate authorization, exactly as
PI-0016 requires.

### A. Subject and methodology adopted by reference

Exactly one subject ticker: **NVDA**. No other company is named or implied by
this decision.

This review adopts, by explicit reference and without restatement or
redesign:

- **PI-0016 §A** — the 15 standing narrative review dimensions (economic
  role, investment thesis, moat, bottleneck power, financial quality,
  capital allocation, secular tailwinds, execution risk, portfolio
  uniqueness, replacement candidate, capital priority, risks/thesis-break
  conditions, current governed tier/target context reported not decided,
  and the two recommendation outputs below);
- **PI-0016 §D** — the reusable primary-source-first evidence standard,
  including explicit labeling of established fact / management claim /
  third-party claim / committee inference / unresolved uncertainty, and an
  active search for disconfirming evidence;
- **PI-0016 §C** — the `PI-0013` repository-fact reconciliation gate,
  applying by default before final human approval of this review's Portfolio
  Uniqueness finding, Replacement Candidate finding, capital-priority
  comparison, and any resulting draft YAML/Markdown update.

None of these are redefined here. This decision selects and scopes NVDA
only; it does not re-derive the methodology PI-0016 already supplies.

### B. Selection rationale (neutral — no research conclusion prejudged)

NVDA is selected because it is the corpus's most-established Company
Intelligence subject with an existing record, an existing theme reference,
and dormant freshness-registry enrollment, making it a natural first
application of PI-0016's newly standing methodology on a company the
repository already has the most context for reconciling against. This
mirrors `PI-0012`'s own selection precedent (choosing TSM as a
process-testing subject rather than a claim about TSM's economic role): this
decision does not conclude, assume, or imply anything about NVDA's moat,
bottleneck power, financial quality, portfolio uniqueness, or capital
priority. Those are exactly the questions the future review must determine,
not answers this governance decision supplies in advance. NVDA's existing
`High` conviction rating and its existing record stand exactly as `PI-0007`
left them, unaffected by this filing, unless and until a future, separate
Intelligence-record-update authorization changes them.

### C. Bounded research scope

The review may: (1) apply PI-0016 §A's 15 dimensions narratively to NVDA,
drawing on NVDA's existing Company Intelligence record as background context
that itself requires no re-approval, and on new primary-source research
where the existing record is silent, dated, or insufficient; (2) apply the
§D evidence standard to any new source considered; (3) apply the §C/`PI-0013`
reconciliation gate against current `targets.yaml`, `holdings.yaml`, the
current `intelligence/companies/` inventory, and NVDA's own `themes:`
reference; (4) produce the two independent recommendation outputs required
by §F (below). The review may not create, modify, or propose text for any
tracked repository file other than its own eventual review packet /
implementation-PR narrative — no file under `intelligence/`, `targets.yaml`,
or `holdings.yaml` is authorized to change as part of this research.

### D. Comparator set — named exactly, per PI-0016 §E option 1

The review's bounded capital-priority comparison (PI-0016 §E) uses exactly
this four-company comparator set, named here rather than left to a
qualifying method: **TSM, ASML, AVGO, MSFT.** The review packet may not
narrow, expand, order, rank, substitute, or otherwise modify this set.

Neutral relevance basis for each comparator (process justification only —
no comparator conclusion is stated or implied):

- **TSM** — already a Company Intelligence subject (`PI-0012`), a `semis`
  cluster co-member, and NVDA's own foundry/manufacturing counterparty;
  raises the bottleneck-power and supply-chain-position question from the
  opposite end of NVDA's own supply chain.
- **ASML** — a `semis` cluster co-member with no existing Company
  Intelligence record; sits further upstream (lithography equipment) than
  either NVDA or TSM, raising a distinct moat/bottleneck comparison at a
  different supply-chain layer.
- **AVGO** — a `semis` cluster co-member, previously the subject of a
  tier-fit governance review (kept at T2; see CLAUDE.md Decisions Log) that
  explicitly cited its own semis-correlation as a reason not to promote it
  further — a direct within-cluster capital-allocation alternative.
- **MSFT** — a T1 co-holding, not a `semis` cluster member, and one of the
  names in the previously-flagged 7-of-9 T1 AI-infrastructure subset
  (CLAUDE.md's "T1 AI-infra cluster cap: scanned and declined" entry); raises
  a demand-side (hyperscaler customer) versus supply-side (compute-hardware
  vendor) comparison within the same broad AI-infrastructure narrative,
  deliberately outside NVDA's own correlated cluster.

Each of these is a neutral hypothesis for the review to test, not a
predetermined finding — the review must independently state, for each
comparator actually used, its substantive relevance, distinct economic role,
overlap/complementarity with NVDA, and the opportunity-cost case, per PI-0016
§E's own requirements.

### E. Known evidence limitations, disclosed at authorization time

- NVDA's own existing Company Intelligence record already discloses a
  narrower evidentiary basis than COST's or XOM's: its five risk categories
  were understood from general secondary coverage, not independently
  verified word-for-word against NVIDIA's own filed FY2026 Form 10-K
  risk-factor language, and no 10-K URL is asserted in the record.
- Direct rendering of primary documents (SEC EDGAR, issuer investor-relations
  domains) has previously returned HTTP 403 in this research environment for
  NVDA, COST, and XOM; TSM's record shows this was not universal (TSM's
  sources were directly opened). The review should expect, but cannot
  assume, this limitation will recur for NVDA, ASML, AVGO, or MSFT sourcing.
- ASML, AVGO, and MSFT have no existing Company Intelligence record of any
  kind — their comparator-relevant sourcing starts from zero within this
  repository and must be built during the review itself, at the standard set
  by PI-0016 §D.
- NVDA's record is dated 2026-07-18 (`next_due: 2026-10-16`); any review
  conducted under this authorization should independently confirm whether
  the record's underlying figures remain current rather than assuming they
  do.

### F. Two required recommendation outputs (PI-0016 §F, adopted by reference)

The review must state exactly one value from each of the following two
independent vocabularies. Neither grants implementation authority; both are
advisory only, for the principal's separate decision:

1. **Advisory policy recommendation** — exactly one of: Keep current policy;
   Recommend promotion; Recommend demotion; Recommend target increase;
   Recommend target reduction; Hold pending specified evidence.
2. **Intelligence-maintenance recommendation** — exactly one of: No
   Intelligence update needed; Intelligence refresh recommended; Intelligence
   update held pending specified evidence.

These stay independent per PI-0016's own rationale: NVDA's governed tier and
target may remain entirely correct while its Company Intelligence record
independently needs newer evidence, or the reverse may hold. This decision
states the requirement; it produces neither value itself.

### G. Lifecycle

```
PI-0017 (this decision, filed once, names NVDA and TSM/ASML/AVGO/MSFT)
  -> bounded research under PI-0016 Sec A/D
  -> repository-fact reconciliation (PI-0016 Sec C, PI-0013's gate)
  -> human review
  -> advisory policy recommendation (Sec F.1) and Intelligence-maintenance
     recommendation (Sec F.2)
  -> principal decision
  -> [optional, conditional on findings] separate Intelligence-record
     update authorization
  -> [optional, conditional on findings] separate tier/target/roster/
     cluster/cap/other policy governance
  -> [optional, conditional on findings] implementation, validation,
     merge/effectiveness
```

Every step after "principal decision" is conditional on what the review
actually finds and is optional, not mandatory. A review that concludes "Keep
current policy" and "No Intelligence update needed" is a valid, complete
outcome on its own — it requires no further Intelligence, tier, target, or
other governance filing, and no standalone closure decision is required to
retire this authorization. Conversely, findings are not self-executing: any
downstream Intelligence, tier, target, roster, cluster, cap, or allocator
change still requires its own separate, later, filed governance decision,
exactly as PI-0016 §B/§I require. An unfiled conversational finding under
this authorization is context only, not repository authority, per PI-0016
§H's own convention.

### H. Explicit prohibitions

This decision authorizes none of the following, under any interpretation:

- any research conclusion about NVDA, TSM, ASML, AVGO, or MSFT — none is
  stated by this filing, and none may be treated as pre-decided by it;
- creating or modifying `intelligence/companies/NVDA.yaml`, `NVDA.md`, or any
  other Company or Theme Intelligence record, including TSM's;
- any second company beyond NVDA becoming a review subject under this
  decision — TSM, ASML, AVGO, and MSFT appear here only as named comparators,
  not as authorized review subjects in their own right;
- any ontology, schema, or vocabulary change beyond what `ONTO-0001` already
  froze;
- any numeric score, ranking, league table, or weighted comparison of any
  kind;
- any change to any target, tier, roster, cluster, cap, or `holdings.yaml`
  value;
- any allocator or margin integration, code, or production-module change
  (`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
  `intelligence_report.py`, or any other module);
- any trade or order of any kind;
- any price target, return forecast, valuation conclusion without a
  disclosed methodology, or automatic implementation of any finding;
- any amendment to `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/INVESTMENT_ONTOLOGY.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`;
- any report generator, validator, or test change;
- extending PI-0016's methodology or evidence standard to any company beyond
  NVDA — this authorization is NVDA-only, exactly as PI-0012 was TSM-only.

## Rationale

Same discipline `PI-0012`/`PI-0013` applied to TSM and `PI-0016` itself
requires of every future company-specific authorization: a standing
methodology is authorized once, separately from any authority to apply it to
a specific subject, and the second question — which company, if any, is
reviewed, and under what bounded scope — is answered only by its own new,
separately justified, repository-filed decision. This is that decision for
NVDA.

Naming the exact four-company comparator set (§D) rather than defining a
qualifying method follows PI-0016 §E's own instruction: a "same correlated
cluster" qualifying rule would yield TSM, ASML, and AVGO but not MSFT, and
MSFT's demand-side contrast is deliberately wanted here — a set that mixes a
within-cluster and an outside-cluster comparator cannot be produced by a
single deterministic membership rule without either narrowing or discretionary
ordering, which §E prohibits. Naming the set directly is therefore the
correct path under §E's own decision rule, not a preference.

Listing `related_decisions` as corrected: `GOV-0001` (the governance-record
layer this file is filed under); `AUTO-0001` (NVDA's existing, dormant
freshness-registry enrollment, reported here as background only, not as
research authority); `PI-0004` (the two-recommendation split's closest
precedent and the closed conviction vocabulary this review must respect if
it touches NVDA's rating); `PI-0006`/`PI-0007` (the Theme Intelligence
authority behind NVDA's existing `ai_infrastructure` reference); `PI-0009`
(the corpus precedent for a second theme-referencing pair of company
records, relevant background for how theme references have been handled
elsewhere in the corpus); `PI-0012` (the eleven-question method this
review's dimensions generalize from, and the TSM record this review names as
a comparator); `PI-0013` (the reconciliation gate this decision applies by
default, and the selection-justification requirement this decision satisfies
for NVDA); `PI-0016` (the standing methodology, evidence standard, and
comparator-set rule this decision adopts by reference); `ONTO-0001` (the
vocabulary PI-0016's dimensions operate under, unchanged and unextended
here).

## Alternatives Considered

- **Authorize a qualifying method (e.g., "all `semis` cluster co-members")
  instead of naming the comparator set.** Rejected: yields only TSM/ASML/AVGO,
  excludes the demand-side MSFT contrast the review should test, and PI-0016
  §E requires naming the exact set whenever a single deterministic rule
  cannot unambiguously produce it without discretionary narrowing.
- **Fold this authorization and NVDA's future review findings into one
  combined decision.** Rejected: exactly the blurring PI-0013's own
  rationale (echoing PI-0004's COST/XOM sequencing) warns against —
  authorization and findings are different governance events with different
  evidentiary maturity, and PI-0016 §B requires the authorization precede
  research, not accompany or follow it.
- **Treat NVDA's existing Company Intelligence record and `AUTO-0001`
  enrollment as sufficient authorization on their own.** Rejected: `PI-0007`
  authorized only the existing record's creation, and `AUTO-0001` authorizes
  no review or research activity of any kind — neither satisfies PI-0016
  §B's explicit requirement for a separate, filed, company-specific research
  authorization.
- **Select a different or larger comparator set (e.g., the full `semis`
  roster, or a five-company set).** Rejected: PI-0016 §E bounds the set to
  two-to-five names and requires each to be independently justified; four
  named, distinctly-justified comparators (one same-supply-chain, one
  upstream-equipment, one within-cluster-allocation, one demand-side) covers
  the intended range of contrasts without inflating the set past what can be
  individually justified.
- **State a substantive conclusion about NVDA, TSM, ASML, AVGO, or MSFT in
  this filing to give the future review a head start.** Rejected: governance
  decisions in this repository authorize process and scope; they do not
  pre-decide the substantive findings a human-reviewed record is supposed to
  independently establish, the same restraint `PI-0012` applied to TSM.

## Consequences

`intelligence/companies/NVDA.yaml`, `NVDA.md`, every other existing Company
or Theme Intelligence record (including `TSM.yaml`/`.md`), `intelligence/
freshness_registry.yaml`, `intelligence/freshness_checkpoints.yaml`,
`intelligence_validator.py`, `intelligence_report.py`, every test file,
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
`constitution/INVESTMENT_CONSTITUTION.md`, `allocate.py`, `margin_state.py`,
`targets.yaml`, and `holdings.yaml` all remain unchanged. `governance/
decisions.yaml` gains one new row for this entry. `CLAUDE.md`'s Decisions Log
gains one short pointer entry.

**No research has been conducted, and no research finding, ranking, score,
price target, or automatic implementation is authorized or implied by this
decision alone.** A future NVDA committee review may now begin under the
scope and comparator set stated above; any resulting Intelligence-record
update, or any tier/target/roster/cluster/cap/allocator change, remains its
own separate, future, separately-approved governance decision, exactly as
PI-0016 §B/§I require.
