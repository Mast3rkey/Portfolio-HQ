---
decision_id: PI-0021
date: 2026-07-23
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0003, PI-0004, PI-0006, PI-0009, PI-0012, PI-0013, PI-0016, PI-0017, PI-0019, TGT-0002, ONTO-0001]
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
code, or implementation change." `governance/decisions/
PI-0017-nvda-committee-review-authorization.md` and `governance/decisions/
PI-0019-gev-committee-review-authorization.md` were the first two such
filings, naming NVDA and GEV respectively. This decision is the third,
naming **COST**.

COST already carries a Company Intelligence record
(`intelligence/companies/COST.yaml`/`.md`). Confirmed directly against
`targets.yaml`, `holdings.yaml`, and `intelligence/companies/COST.yaml` at
filing time:

- COST is a **T1** holding at the standard **3.35%** per-name target
  (`targets.yaml`), held at 0.227127 shares (`holdings.yaml`).
- `COST.yaml`'s `portfolio_role_ref` is **T1**; `conviction.rating` is
  **High**.
- The record originated as Portfolio HQ's **first** Company Intelligence
  pilot (`governance/decisions/PI-0003...` per `decision_log.yaml`; record's
  own header: "Portfolio HQ's first Portfolio Intelligence pilot record"),
  created 2026-07-17 through AI-assisted research and human approval at a
  time when COST's `portfolio_role_ref` was **T2**. `review.log`'s
  2026-07-20 entry records that a later human portfolio-role review,
  following `governance/decisions/TGT-0002-cost-promotion-t2-to-t1.md`'s
  separate T2→T1 promotion decision, updated `portfolio_role_ref` from T2 to
  T1 — explicitly noted in the record itself as "an advisory Company
  Intelligence characterization only" that does not itself authorize, derive,
  or alter allocation policy, conviction, thesis, risks, catalysts, or review
  cadence.
- COST's record discloses a material source-access limitation: direct
  rendering of Costco's and SEC's primary documents returned HTTP 403 across
  seven distinct access attempts in the original research environment. Every
  cited figure was corroborated across at least two independent search
  results and cites an exact primary document (title, date, SEC accession
  number, URL), but — per the record's own "Source-access disclosure"
  section — "was not directly verified against rendered primary text." No
  secondary-only content was retained; content that depended solely on
  secondary corroboration (specific wage figures, a speculative fee-increase
  catalyst, unconfirmed e-commerce growth figures) was removed or
  generalized rather than kept with a secondary citation.
- COST's record is dated `last_reviewed: 2026-07-17`, `next_due:
  2026-10-15` — its evidentiary base is FY2025 (fiscal year ended
  2025-08-31) results and Q3 FY2026 (quarter ended 2026-05-10) results; no
  later reporting period is reflected.

These facts establish an observation this decision is careful not to
overstate: COST carries Portfolio HQ's **oldest** Company Intelligence
record, produced under a materially narrower source-access environment than
some later records, subsequently reconciled to a new tier through a separate
governance decision (`TGT-0002`) rather than through any Company Intelligence
review of its own, and has never been the subject of a `PI-0016`-style
committee review. Recording this is not a claim that COST's tier is wrong,
that its `High` conviction rating is wrong, or that either must change; it is
the selection rationale for why a review is warranted now, exactly as
`PI-0016` §B requires this filing to state — the same restraint `PI-0017`
and `PI-0019` applied to NVDA and GEV.

## Decision

**PI-0021 authorizes exactly one thing: bounded, research-only committee
review activity on COST, conducted under PI-0016's standing methodology.** It
authorizes no research conclusion, no Company or Theme Intelligence change,
and no policy, tier, target, roster, cluster, cap, or allocator change. Each
of those remains gated behind its own separate authorization, exactly as
PI-0016 requires.

### A. Subject and methodology adopted by reference

Exactly one subject ticker: **COST**. No other company is named or implied
as a review subject by this decision — WMT, AMZN, BRK.B, and V appear below
solely as named comparators under §D, not as review subjects in their own
right.

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

None of these are redefined here. This decision selects and scopes COST
only; it does not re-derive the methodology PI-0016 already supplies.

### B. Selection rationale (neutral — no research conclusion prejudged)

COST is selected because its existing repository record presents a
meaningful, unresolved review question: it is Portfolio HQ's oldest Company
Intelligence record, drafted under a materially constrained source-access
environment (primary-document rendering blocked across seven attempts,
corroborated only through search results), and its tier was subsequently
changed by a separate governance decision (`TGT-0002`) without any
accompanying committee-style review of COST's own business-quality thesis or
capital priority. This decision does not conclude, assume, or imply that
COST's T1 tier is too high, too low, or otherwise incorrect; that its `High`
conviction rating should change; or that its Intelligence record is stale or
inadequate. Those are exactly the questions the future review must
determine, not answers this governance decision supplies in advance. COST's
existing `High` conviction rating, its T1 tier, and its 3.35% target all
stand exactly as previously established, unaffected by this filing, unless
and until their own separate, future, separately-approved governance
decisions change them. This mirrors `PI-0017`'s and `PI-0019`'s own
selection precedent — a repository-fact-grounded rationale for *why a
review is warranted now*, not a conclusion the review itself is meant to
reach.

### C. Bounded research scope

The review may examine, narratively, under PI-0016 §A's 15 dimensions:
portfolio role and economic function; membership economics and renewal
quality; price leadership and customer value proposition; purchasing scale
and the limited-SKU operating model; warehouse expansion and international
runway; e-commerce and omnichannel execution; operating margins and
membership-fee economics; labor economics and wage pressure; capital
allocation; competitive durability; tariff, currency, and merchandise-cost
exposure; management execution; valuation only insofar as PI-0016 §D and §E
permit it within the bounded capital-priority comparison (no standalone
valuation conclusion, no price target); thesis-break conditions; overlap and
opportunity cost versus the four comparators named in §D below; and whether
current governed policy should be maintained or separately reconsidered, and
whether the existing COST Intelligence record requires maintenance. This
list is illustrative of the scope PI-0016 §A already authorizes, not an
additional or narrower scope of its own.

The review may: (1) apply PI-0016 §A's 15 dimensions narratively to COST,
drawing on COST's existing Company Intelligence record as background context
that itself requires no re-approval, and on new primary-source research
where the existing record is silent, dated, blocked by the disclosed
source-access limitation, or insufficient — including, specifically, any
Costco reporting more recent than the record's cited FY2025/Q3 FY2026
evidence base; (2) apply the §D evidence standard to any new source
considered, for COST and for each named comparator; (3) apply the
§C/`PI-0013` reconciliation gate against current `targets.yaml`,
`holdings.yaml`, the current `intelligence/companies/` inventory, and (COST's
record carries no `themes:` reference, so this reconciliation element is
inapplicable to COST but still applies to any theme references a comparator
record may carry); (4) produce the two independent recommendation outputs
required by §F (below). The review may not create, modify, or propose text
for any tracked repository file other than its own eventual review packet /
implementation-PR narrative — no file under `intelligence/`, `targets.yaml`,
or `holdings.yaml` is authorized to change as part of this research.

### D. Comparator set — named exactly, per PI-0016 §E option 1

The review's bounded capital-priority comparison (PI-0016 §E) uses exactly
this four-company comparator set, named here rather than left to a
qualifying method: **WMT, AMZN, BRK.B, V.** The review packet may not
narrow, expand, order, rank, substitute, or otherwise modify this set.

COST is not a member of any `targets.yaml` correlated cluster (`semis`,
`power_infra`, `oil`), so no deterministic cluster-membership rule (PI-0016
§E option 2, the path `PI-0019` used for GEV/ETN/VRT/PWR) is available here.
The set is instead named directly, the same path `PI-0017` used for NVDA,
because a single membership rule cannot reach a deliberately mixed
consumer/commerce-overlap and durable-compounder-alternative comparator set
without discretionary narrowing — exactly the condition under which PI-0016
§E requires naming the exact set rather than defining a method.

Neutral relevance basis for each comparator (process justification only —
no comparator conclusion is stated or implied):

- **WMT** (Walmart, `T2` tier, confirmed `targets.yaml`, held per
  `holdings.yaml`) — the closest current portfolio alternative in scaled,
  defensive retail and consumer distribution, including its own warehouse-
  club format (Sam's Club). Raises a direct comparison on purchasing power,
  logistics, membership-adjacent economics, digital execution, resilience,
  and governed capital priority against a name held one tier below COST.
- **AMZN** (Amazon, `T2` tier, confirmed `targets.yaml`, held per
  `holdings.yaml`) — the major current portfolio alternative in commerce,
  logistics, membership economics (Prime), digital retail, and customer
  ecosystem strength. The future review must not reduce Amazon to a retail
  comparison alone; it must account for AWS and advertising as material,
  economically distinct differentiators from COST's single-segment retail
  model.
- **BRK.B** (Berkshire Hathaway, `T2` tier, confirmed `targets.yaml`, held
  per `holdings.yaml`) — relevant as a current-portfolio alternative for
  durable compounding, defensive resilience, capital stewardship, and
  opportunity cost, not as a direct operating peer. Its purpose in this
  comparison is bounded capital-priority contrast, not business-model
  equivalence.
- **V** (Visa, `T1` tier, confirmed `targets.yaml`, held per
  `holdings.yaml`) — another governed **T1** compounder competing for the
  same scarce core-capital allocation as COST, with durable network
  economics, high business quality, and a distinct economic function
  (payments infrastructure, not retail). Tests whether COST deserves the
  same governed capital-priority tier relative to a non-retail
  infrastructure compounder, rather than only against retail/commerce
  alternatives.

These four are intentionally mixed — two (WMT, AMZN) with meaningful
consumer/commerce overlap, and two (BRK.B, V) representing next-best
durable-compounder uses of core capital rather than operating peers. Each of
these is a neutral hypothesis for the review to test, not a predetermined
finding — the review must independently state, for each comparator actually
used, its substantive relevance, distinct economic role, overlap/
complementarity with COST, and the opportunity-cost case, per PI-0016 §E's
own requirements. **This is not a ranking.** No score, league table, or
weighted comparison of the four comparators against COST or against each
other is authorized; comparators need not be, and are not required to be,
identical operating peers to COST or to one another; the review is limited
strictly to role, quality, overlap, opportunity cost, and capital priority
as PI-0016 §E defines them; and no persistent cross-company comparison
structure, index, or table of any kind — inside or outside `intelligence/`
— may be created as part of, or as a byproduct of, this comparison.

### E. Known evidence limitations, disclosed at authorization time

- COST's own existing Company Intelligence record already discloses that
  direct rendering of Costco's and SEC's primary documents returned HTTP 403
  across seven distinct access attempts in the original research
  environment, and that every cited figure, while corroborated across at
  least two independent search results and citing an exact primary
  document, "was not directly verified against rendered primary text." The
  review should expect, but cannot assume, this limitation will recur for
  COST or for WMT, AMZN, BRK.B, or V sourcing.
- COST's record's own evidentiary base ends at FY2025 full-year (ended
  2025-08-31) and Q3 FY2026 (quarter ended 2026-05-10) reporting; any review
  conducted under this authorization should independently confirm whether
  more recent Costco reporting exists and is material, rather than assuming
  the record's cited figures remain the latest available.
- WMT, AMZN, BRK.B, and V have no existing Company Intelligence record of
  any kind — their comparator-relevant sourcing starts from zero within this
  repository and must be built during the review itself, at the standard
  set by PI-0016 §D.
- COST's `portfolio_role_ref` was changed (T2 → T1) by `TGT-0002`, a
  separate tier-governance decision, without any accompanying Company
  Intelligence review of COST's underlying business-quality thesis or
  capital priority at the time of that promotion. The future review should
  treat this as part of the repository-fact reconciliation required by
  PI-0016 §C, not as a finding this authorization pre-supplies.
- COST's record is dated `last_reviewed: 2026-07-17` (`next_due:
  2026-10-15`); this authorization does not itself determine whether the
  record is stale — that determination is the review's own
  Intelligence-maintenance recommendation (§F.2).

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

These stay independent per PI-0016's own rationale: COST's governed tier and
target may remain entirely correct while its Company Intelligence record
independently needs newer evidence, or the reverse may hold — precisely the
distinction §Context above observes but does not resolve. This decision
states the requirement; it produces neither value itself. **Neither
recommendation is self-executing** — the review's advisory policy
recommendation and Intelligence-maintenance recommendation each require
their own separate, future, principal-approved governance decision before
any repository state changes as a result.

### G. Lifecycle — states kept distinct

```
PI-0021 (this decision, filed once, names COST and WMT/AMZN/BRK.B/V)
  -> discussed (conversational scoping, this session)
  -> authorized (this decision, on merge — see below)
  -> [not yet reached] bounded research under PI-0016 Sec A/D
  -> [not yet reached] repository-fact reconciliation (PI-0016 Sec C,
     PI-0013's gate)
  -> [not yet reached] researched (review packet produced)
  -> [not yet reached] recommended (Sec F.1 advisory policy recommendation
     and Sec F.2 Intelligence-maintenance recommendation stated)
  -> [not yet reached] approved (principal decision on each recommendation)
  -> [optional, conditional on findings, not yet reached] separate
     Intelligence-record update authorization
  -> [optional, conditional on findings, not yet reached] separate
     tier/target/roster/cluster/cap/other policy governance
  -> [optional, conditional on findings, not yet reached] implemented,
     validated, merged / effective
```

**Merging this authorization makes only the research authority described in
§C effective — nothing more.** It does not itself constitute research,
does not produce a review packet, does not state or imply either §F
recommendation, and does not approve, imply, or pre-commit to any outcome of
a future review. Every step after "authorized" above is a separate,
future, distinct event with its own evidentiary maturity; none is
retroactively satisfied by this filing, and none of these states may be
collapsed into another or treated as already reached because an earlier one
was.

Every step after "authorized" is conditional on what the review actually
finds and is optional, not mandatory. A review that concludes "Keep current
policy" and "No Intelligence update needed" is a valid, complete outcome on
its own — it requires no further Intelligence, tier, target, or other
governance filing, and no standalone closure decision is required to retire
this authorization. Conversely, findings are not self-executing: any
downstream Intelligence, tier, target, roster, cluster, cap, or allocator
change still requires its own separate, later, filed governance decision,
exactly as PI-0016 §B/§I require. An unfiled conversational finding under
this authorization is context only, not repository authority, per PI-0016
§H's own convention.

### H. Explicit prohibitions

This decision authorizes none of the following, under any interpretation:

- any research conclusion about COST, WMT, AMZN, BRK.B, or V — none is
  stated by this filing, and none may be treated as pre-decided by it;
- conducting the actual external COST, WMT, AMZN, BRK.B, or V research, or
  producing the review packet, in this governance-only filing;
- creating or modifying `intelligence/companies/COST.yaml`, `COST.md`, or
  any comparator's Intelligence record — none exists for WMT/AMZN/BRK.B/V,
  and none is created here — or any other Company or Theme Intelligence
  record;
- any second company beyond COST becoming a review subject under this
  decision — WMT, AMZN, BRK.B, and V appear here only as named comparators,
  not as authorized review subjects in their own right;
- any ontology, schema, or vocabulary change beyond what `ONTO-0001` already
  froze; any amendment to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`;
- any numeric score, ranking, league table, or weighted comparison of any
  kind; any computed or derived conviction value;
- any change to COST's T1 tier, its 3.35% target, or any other target,
  tier, roster, cluster, cap, or `holdings.yaml` value;
- any allocator or margin integration, code, or production-module change
  (`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
  `intelligence_report.py`, or any other module), and no test change;
- any standing review queue, automatic cadence, or entitlement for COST or
  any other company to be reviewed next;
- any trade or order of any kind, and no recommendation that any trade or
  order be placed;
- any price target, return forecast, valuation conclusion without a
  disclosed methodology, or automatic implementation of any finding;
- any amendment to `constitution/INVESTMENT_CONSTITUTION.md` or
  `docs/INVESTMENT_ONTOLOGY.md`;
- any report generator, validator, or test change;
- treating either future §F recommendation, once stated, as automatically
  authoritative or self-executing;
- extending PI-0016's methodology or evidence standard to any company beyond
  COST — this authorization is COST-only, exactly as PI-0017 was NVDA-only
  and PI-0019 was GEV-only.

## Rationale

Same discipline `PI-0012`/`PI-0013` applied to TSM, `PI-0017` applied to
NVDA, `PI-0019` applied to GEV, and `PI-0016` itself requires of every
future company-specific authorization: a standing methodology is authorized
once, separately from any authority to apply it to a specific subject, and
the second question — which company, if any, is reviewed, and under what
bounded scope — is answered only by its own new, separately justified,
repository-filed decision. This is that decision for COST.

Naming the exact four-company comparator set (§D) directly, rather than
defining a qualifying method, follows `PI-0017`'s NVDA precedent rather than
`PI-0019`'s GEV precedent: COST carries no `targets.yaml` correlated-cluster
membership, so no deterministic cluster-based rule is available to produce a
comparator set at all, and the desired mix — two consumer/commerce-overlap
names plus two durable-compounder alternatives at different governed tiers
— could not be produced by any single membership rule without discretionary
narrowing, which PI-0016 §E prohibits for a rule-based path. Naming the set
directly is therefore the correct path under §E's own decision rule, not a
preference, exactly as it was for `PI-0017`.

Selecting COST now, as the third `PI-0016` company-specific authorization,
follows directly from a fact the record itself discloses: it is Portfolio
HQ's oldest Company Intelligence record, produced under a materially
constrained evidence environment, subsequently reconciled to a new tier by
a separate governance decision (`TGT-0002`) without any accompanying
committee-style review of its own thesis — a distinction of the same shape
`PI-0019` identified for GEV (governed tier versus independent
Intelligence-record conviction), applied here to governed tier versus
Intelligence-record provenance and evidentiary vintage instead.

Listing `related_decisions`: `GOV-0001` (the governance-record layer this
file is filed under); `PI-0003` (the pilot authorization that created
COST's original record); `PI-0004` (the two-recommendation split's closest
precedent and the closed conviction vocabulary this review must respect if
it touches COST's rating); `PI-0006` (the Theme Intelligence freeze,
relevant background though COST's record carries no theme reference);
`PI-0009` (the corpus precedent for how theme references have been handled
elsewhere, relevant only as background since COST has none); `PI-0012` (the
eleven-question method this review's dimensions generalize from); `PI-0013`
(the reconciliation gate this decision applies by default, and the
selection-justification requirement this decision satisfies for COST);
`PI-0016` (the standing methodology, evidence standard, and comparator-set
rule this decision adopts by reference); `PI-0017` (the first
company-specific authorization filed under PI-0016, whose named-comparator-
set structure this decision follows); `PI-0019` (the second, whose overall
filing structure this decision also follows); `TGT-0002` (the separate
tier-promotion decision this filing's selection rationale is grounded in,
without re-litigating or reopening it); `ONTO-0001` (the vocabulary
PI-0016's dimensions operate under, unchanged and unextended here).

## Alternatives Considered

- **Select a different company for this third PI-0016 review.** Rejected in
  favor of COST: no other current Company Intelligence record combines
  COST's specific combination of oldest-record provenance, a materially
  constrained original evidence environment, and a tier subsequently changed
  by a separate governance decision without any accompanying committee-style
  review — a distinct, previously-unexamined gap from the one `PI-0017`
  (governed tier vs. `High` conviction, dormant freshness enrollment) and
  `PI-0019` (governed tier vs. `Medium` conviction) each identified for
  their own subjects.
- **Define a qualifying method rather than naming WMT/AMZN/BRK.B/V
  directly.** Rejected: COST has no correlated-cluster membership in
  `targets.yaml`, so no deterministic membership rule is available, and the
  desired mixed comparator set (commerce-overlap plus durable-compounder
  alternatives at two different governed tiers) cannot be produced by any
  single non-discretionary rule — PI-0016 §E requires naming the exact set
  under exactly this condition.
- **Include a fifth comparator (e.g., Target, BJ's Wholesale, or Costco's
  closest pure warehouse-club peer) to sharpen the retail-format
  comparison.** Rejected at this stage: PI-0016 §E bounds the set to
  two-to-five names and requires each to be independently justified; four
  named, distinctly-justified comparators (two commerce-overlap, two
  durable-compounder-alternative) covers the intended range of contrasts
  the task description specifies without inflating the set past what can be
  individually justified in this filing. A future, separate authorization
  could name a different or larger set for a different review; this
  decision does not foreclose that.
- **Fold this authorization and COST's future review findings into one
  combined decision.** Rejected: exactly the blurring `PI-0013`'s own
  rationale warns against — authorization and findings are different
  governance events with different evidentiary maturity, and PI-0016 §B
  requires the authorization precede research, not accompany or follow it.
- **Treat COST's existing Company Intelligence record and `TGT-0002`'s tier
  promotion as sufficient authorization on their own.** Rejected: `PI-0003`
  authorized only the existing record's creation, and `TGT-0002` authorized
  only the tier change to `portfolio_role_ref` — neither satisfies PI-0016
  §B's explicit requirement for a separate, filed, company-specific research
  authorization.
- **State a substantive conclusion about COST, WMT, AMZN, BRK.B, or V in
  this filing to give the future review a head start.** Rejected: governance
  decisions in this repository authorize process and scope; they do not
  pre-decide the substantive findings a human-reviewed record is supposed to
  independently establish, the same restraint `PI-0012`, `PI-0017`, and
  `PI-0019` applied to their own subjects.
- **File this decision as `Proposed` pending a further principal-approval
  step.** Considered and rejected: this workstream was itself commissioned
  directly by the principal as "the next bounded Portfolio-HQ Investment
  Committee workstream," matching the same direct-principal-authorization
  posture under which `PI-0017` and `PI-0019` were each filed `Accepted`
  without an intermediate `Proposed` stage. No repository precedent in this
  series uses a `Proposed` status for a §B company-specific research
  authorization; adopting one here without precedent would be an invented
  step, not a discovered requirement.

## Consequences

`intelligence/companies/COST.yaml`, `COST.md`, every other existing Company
or Theme Intelligence record (none of which exists yet for WMT, AMZN,
BRK.B, or V), `intelligence/freshness_registry.yaml`, `intelligence/
freshness_checkpoints.yaml`, `intelligence_validator.py`,
`intelligence_report.py`, every test file, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `constitution/INVESTMENT_CONSTITUTION.md`,
`allocate.py`, `margin_state.py`, `targets.yaml`, and `holdings.yaml` all
remain unchanged. `governance/decisions.yaml` gains one new row for this
entry. `CLAUDE.md`'s Decisions Log gains one short pointer entry.

**No research has been conducted, and no research finding, ranking, score,
price target, or automatic implementation is authorized or implied by this
decision alone.** A future COST committee review may now begin under the
scope and comparator set stated above; any resulting Intelligence-record
update, or any tier/target/roster/cluster/cap/allocator change, remains its
own separate, future, separately-approved governance decision, exactly as
PI-0016 §B/§I require.
