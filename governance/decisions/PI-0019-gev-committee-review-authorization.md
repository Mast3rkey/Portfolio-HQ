---
decision_id: PI-0019
date: 2026-07-22
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0004, PI-0006, PI-0007, PI-0009, PI-0012, PI-0013, PI-0016, PI-0017, ONTO-0001]
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
code, or implementation change." `governance/decisions/PI-0017-nvda-committee-
review-authorization.md` was the first such filing, naming NVDA. This
decision is the second, naming GEV.

GEV already carries a Company Intelligence record
(`intelligence/companies/GEV.yaml`/`.md`), created and human-approved under
`PI-0007` as part of the same `ai_infrastructure` Theme Intelligence pilot
that produced NVDA's record — Portfolio HQ's fourth company record overall,
the second of that pilot's two. Neither that fact, nor GEV's governed tier,
nor its cluster membership by itself authorizes a PI-0016 committee review —
`PI-0007` authorized only the existence of the current record. This decision
supplies the review authorization that record does not.

Repository facts, reported here as background only, per `PI-0013`'s
guardrail that tier, target weight, share count, and cluster membership may
be reported as context but never treated as evidence of quality, conviction,
or entitlement to review: confirmed directly against `targets.yaml`,
`holdings.yaml`, and `intelligence/companies/GEV.yaml` at filing time —

- GEV is a **T1** holding at the standard **3.35%** per-name target, held at
  0.196239 shares (`holdings.yaml`), the same governed tier and target as
  NVDA, ASML, TSM, MSFT, and every other T1 name.
- GEV is a member of `targets.yaml`'s `power_infra` correlated-cluster cap
  (GEV, ETN, VRT, PWR; ≤ 20% of book) — a different cluster than NVDA's
  `semis`.
- `intelligence/companies/GEV.yaml`'s `conviction.rating` is **Medium**, not
  `High` (NVDA's rating). This is a plain reading of the existing record's own
  field, not a new finding by this decision.
- GEV's record is dated `last_reviewed: 2026-07-18`, `next_due: 2026-10-16`,
  and its cited evidence base is FY2025 full-year results and Q1 2026
  (calendar-Q1) results — no later reporting period is reflected.
- `GEV.yaml` references the `ai_infrastructure` theme, the same reference
  NVDA's record carries.

These facts establish an observation this decision is careful not to
overstate: GEV carries the *same* governed capital-priority tier and target
as the repository's `High`-conviction names, while its own Company
Intelligence record independently rates it `Medium` — a distinction between
governed capital priority and current business-quality conviction that has
not, to date, been the subject of any committee-style review. Recording this
distinction is not a claim that the tier is wrong, that the conviction rating
is wrong, or that either must change; it is the selection rationale for why a
review is warranted, exactly as `PI-0016` §B requires this filing to state.

## Decision

**PI-0019 authorizes exactly one thing: bounded, research-only committee
review activity on GEV, conducted under PI-0016's standing methodology.** It
authorizes no research conclusion, no Company or Theme Intelligence change,
and no policy, tier, target, roster, cluster, cap, or allocator change. Each
of those remains gated behind its own separate authorization, exactly as
PI-0016 requires.

### A. Subject and methodology adopted by reference

Exactly one subject ticker: **GEV**. No other company is named or implied as
a review subject by this decision — ETN, VRT, and PWR appear below solely as
named comparators under §D, not as review subjects in their own right.

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

None of these are redefined here. This decision selects and scopes GEV only;
it does not re-derive the methodology PI-0016 already supplies.

### B. Selection rationale (neutral — no research conclusion prejudged)

GEV is selected because its existing repository record presents a
meaningful, unresolved distinction this framework is well-suited to examine:
GEV holds the same governed **T1 / 3.35%** capital-priority standing as the
repository's `High`-conviction names, yet its own Company Intelligence
record independently rates it **Medium**, and that record's evidentiary base
is limited to FY2025 and Q1 2026 disclosure. This decision does not conclude,
assume, or imply that GEV's tier is too high, too low, or otherwise
incorrect; that its conviction rating should change; or that its Intelligence
record is stale or inadequate. Those are exactly the questions the future
review must determine, not answers this governance decision supplies in
advance. GEV's existing `Medium` conviction rating, its T1 tier, and its
3.35% target all stand exactly as previously established, unaffected by this
filing, unless and until their own separate, future, separately-approved
governance decisions change them. This mirrors `PI-0017`'s own selection
precedent for NVDA — a repository-fact-grounded rationale for *why a review
is warranted now*, not a conclusion the review itself is meant to reach.

### C. Bounded research scope

The review may: (1) apply PI-0016 §A's 15 dimensions narratively to GEV,
drawing on GEV's existing Company Intelligence record as background context
that itself requires no re-approval, and on new primary-source research
where the existing record is silent, dated, or insufficient — including,
specifically, any GE Vernova reporting more recent than the record's cited
FY2025/Q1 2026 evidence base; (2) apply the §D evidence standard to any new
source considered, for GEV and for each named comparator; (3) apply the
§C/`PI-0013` reconciliation gate against current `targets.yaml`,
`holdings.yaml`, the current `intelligence/companies/` inventory, and GEV's
own `themes:` reference; (4) produce the two independent recommendation
outputs required by §F (below). The review may not create, modify, or
propose text for any tracked repository file other than its own eventual
review packet / implementation-PR narrative — no file under `intelligence/`,
`targets.yaml`, or `holdings.yaml` is authorized to change as part of this
research.

### D. Comparator set — named exactly, per PI-0016 §E

The review's bounded capital-priority comparison (PI-0016 §E) uses exactly
this three-company comparator set: **ETN, VRT, PWR.** The review packet may
not narrow, expand, order, rank, substitute, or otherwise modify this set.

**Shared basis for the set:** all three are current portfolio holdings
(confirmed in `holdings.yaml`) and are the other, and only other, members of
`targets.yaml`'s governed `power_infra` correlated-cluster cap alongside GEV
— a deterministic, membership-only qualifying rule ("all other current
holdings sharing GEV's own governed correlated-cluster membership") that
produces exactly three names, within PI-0016 §E's required two-to-five
range, with no discretionary ordering, ranking, or narrowing required to
reach that count. This is the same qualifying-method path PI-0016 §E
describes as option 2, stated here as the exact resulting set per §E's own
instruction that a precise, unambiguous method may be named directly once it
yields a complete two-to-five set.

Neutral relevance basis for each comparator (process justification only —
no comparator conclusion is stated or implied):

- **ETN** (Eaton Corporation) — a `band`-tier holding and `power_infra`
  cluster co-member; an electrical-equipment and power-management supplier
  whose product categories (grid, electrical distribution, power quality)
  sit adjacent to GEV's own grid/electrification equipment lines, raising a
  direct within-cluster overlap/complementarity and capital-allocation
  question between two power-equipment suppliers held at different governed
  tiers (T1 vs. band).
- **VRT** (Vertiv Holdings) — a `band`-tier holding and `power_infra` cluster
  co-member; a data-center-specific power and thermal-management equipment
  supplier, raising a narrower overlap question than ETN's — both GEV and
  VRT have reported data-center-driven demand, so this comparator tests
  whether GEV's own data-center order growth is distinct from, or redundant
  with, exposure already held through VRT.
- **PWR** (Quanta Services) — a **T2**-tier holding and `power_infra`
  cluster co-member; a power-infrastructure engineering, construction, and
  maintenance services provider rather than an equipment manufacturer,
  raising a distinct value-chain-position question (equipment supplier vs.
  construction/EPC services) within the same cluster, at yet another
  governed tier than GEV or ETN/VRT.

Each of these is a neutral hypothesis for the review to test, not a
predetermined finding — the review must independently state, for each
comparator actually used, its substantive relevance, distinct economic role,
overlap/complementarity with GEV, and the opportunity-cost case, per PI-0016
§E's own requirements.

### E. Known evidence limitations, disclosed at authorization time

- GEV's own existing Company Intelligence record already discloses that
  direct rendering of primary documents (SEC EDGAR, `gevernova.com`) returned
  HTTP 403 in the research environment, and that its four risk categories
  are understood from general secondary coverage rather than confirmed
  word-for-word against GE Vernova's own filed Form 10-K risk-factor
  language. The review should expect, but cannot assume, this limitation
  will recur.
- GEV's record's own evidentiary base ends at Q1 2026 (calendar) reporting;
  any review conducted under this authorization should independently
  confirm whether more recent GE Vernova reporting exists and is material,
  rather than assuming the record's cited figures remain the latest
  available.
- ETN, VRT, and PWR have no existing Company Intelligence record of any
  kind — their comparator-relevant sourcing starts from zero within this
  repository and must be built during the review itself, at the standard
  set by PI-0016 §D.
- GEV's record is dated `last_reviewed: 2026-07-18` (`next_due:
  2026-10-16`); this authorization does not itself determine whether the
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

These stay independent per PI-0016's own rationale: GEV's governed tier and
target may remain entirely correct while its Company Intelligence record
independently needs newer evidence, or the reverse may hold — precisely the
distinction §Context above observes but does not resolve. This decision
states the requirement; it produces neither value itself.

### G. Lifecycle

```
PI-0019 (this decision, filed once, names GEV and ETN/VRT/PWR)
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

- any research conclusion about GEV, ETN, VRT, or PWR — none is stated by
  this filing, and none may be treated as pre-decided by it;
- creating or modifying `intelligence/companies/GEV.yaml`, `GEV.md`, or any
  other Company or Theme Intelligence record, including the
  `ai_infrastructure` theme file or NVDA's record;
- any second company beyond GEV becoming a review subject under this
  decision — ETN, VRT, and PWR appear here only as named comparators, not as
  authorized review subjects in their own right;
- any ontology, schema, or vocabulary change beyond what `ONTO-0001` already
  froze;
- any numeric score, ranking, league table, or weighted comparison of any
  kind;
- any change to GEV's T1 tier, its 3.35% target, or any other target, tier,
  roster, cluster, cap, or `holdings.yaml` value;
- any allocator or margin integration, code, or production-module change
  (`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
  `intelligence_report.py`, or any other module), and no test change;
- any trade or order of any kind;
- any price target, return forecast, valuation conclusion without a
  disclosed methodology, or automatic implementation of any finding;
- any amendment to `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/INVESTMENT_ONTOLOGY.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`;
- any report generator, validator, or test change;
- extending PI-0016's methodology or evidence standard to any company beyond
  GEV — this authorization is GEV-only, exactly as PI-0017 was NVDA-only and
  PI-0012 was TSM-only.

## Rationale

Same discipline `PI-0012`/`PI-0013` applied to TSM, `PI-0017` applied to
NVDA, and `PI-0016` itself requires of every future company-specific
authorization: a standing methodology is authorized once, separately from
any authority to apply it to a specific subject, and the second question —
which company, if any, is reviewed, and under what bounded scope — is
answered only by its own new, separately justified, repository-filed
decision. This is that decision for GEV.

Naming the exact three-company comparator set (§D) as the direct output of a
deterministic "other current holdings in GEV's own governed cluster" rule
follows PI-0016 §E's own instruction: unlike `PI-0017`'s NVDA authorization
— where a single cluster-membership rule could not reach the desired
demand-side contrast without discretionary narrowing, requiring the set to
be named independently of any rule — GEV's `power_infra` cluster has exactly
three other current-holding members, so the qualifying rule and the named
set coincide exactly, with no ranking, ordering, or discretionary step
between them.

Listing `related_decisions`: `GOV-0001` (the governance-record layer this
file is filed under); `PI-0004` (the two-recommendation split's closest
precedent and the closed conviction vocabulary this review must respect if
it touches GEV's rating); `PI-0006`/`PI-0007` (the Theme Intelligence
authority behind GEV's existing `ai_infrastructure` reference and the pilot
that produced GEV's record alongside NVDA's); `PI-0009` (the corpus
precedent for how theme references have been handled elsewhere); `PI-0012`
(the eleven-question method this review's dimensions generalize from);
`PI-0013` (the reconciliation gate this decision applies by default, and the
selection-justification requirement this decision satisfies for GEV);
`PI-0016` (the standing methodology, evidence standard, and comparator-set
rule this decision adopts by reference); `PI-0017` (the first company-
specific authorization filed under PI-0016, whose structure this decision
follows for consistency); `ONTO-0001` (the vocabulary PI-0016's dimensions
operate under, unchanged and unextended here).

## Alternatives Considered

- **Select a different company for this second PI-0016 review.** Rejected
  in favor of GEV: no other current Company Intelligence record presents as
  direct a tier/conviction distinction — GEV is the only record whose
  `conviction.rating` (`Medium`) diverges from its governed tier's typical
  company profile in a way that has never been examined under any
  committee-style review, while carrying a comparator cluster (`power_infra`)
  small enough to name exactly and completely.
- **Define a qualifying method rather than naming ETN/VRT/PWR directly.**
  Effectively the same outcome here: `power_infra`'s full membership minus
  GEV is exactly ETN, VRT, and PWR, so a qualifying-method authorization and
  a named-set authorization coincide. Named directly for clarity and to
  match `PI-0017`'s own presentation convention.
- **Include CAT or TSLA as additional comparators**, since both were scanned
  as correlated with the `power_infra` group when the cluster cap was built.
  Not selected: CAT and TSLA were not selected. Neither is a member of the
  governed `power_infra` cluster, so neither satisfies this authorization's
  selected deterministic rule: all other current holdings that share GEV's
  actual governed cluster membership. The repository's historical
  explanation for excluding CAT and TSLA from that cluster — weaker
  fundamental fit to the specific power-infrastructure mechanism — supports
  their lower relevance here, but does not create a governance prohibition
  against their use as comparators in some other separately authorized
  review. Including them here would also have pushed the set to five names
  under a different, unauthorized selection basis than the one this decision
  actually adopts.
- **Fold this authorization and GEV's future review findings into one
  combined decision.** Rejected: exactly the blurring `PI-0013`'s own
  rationale warns against — authorization and findings are different
  governance events with different evidentiary maturity, and PI-0016 §B
  requires the authorization precede research, not accompany or follow it.
- **Treat GEV's existing Company Intelligence record and theme reference as
  sufficient authorization on their own.** Rejected: `PI-0007` authorized
  only the existing record's creation; neither it nor the theme reference
  satisfies PI-0016 §B's explicit requirement for a separate, filed,
  company-specific research authorization.
- **State a substantive conclusion about GEV, ETN, VRT, or PWR in this
  filing to give the future review a head start.** Rejected: governance
  decisions in this repository authorize process and scope; they do not
  pre-decide the substantive findings a human-reviewed record is supposed to
  independently establish, the same restraint `PI-0012` and `PI-0017`
  applied to their own subjects.

## Consequences

`intelligence/companies/GEV.yaml`, `GEV.md`, every other existing Company or
Theme Intelligence record (including `NVDA.yaml`/`.md` and the
`ai_infrastructure` theme file), `intelligence/freshness_registry.yaml`,
`intelligence/freshness_checkpoints.yaml`, `intelligence_validator.py`,
`intelligence_report.py`, every test file, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `constitution/INVESTMENT_CONSTITUTION.md`,
`allocate.py`, `margin_state.py`, `targets.yaml`, and `holdings.yaml` all
remain unchanged. `governance/decisions.yaml` gains one new row for this
entry. `CLAUDE.md`'s Decisions Log gains one short pointer entry.

**No research has been conducted, and no research finding, ranking, score,
price target, or automatic implementation is authorized or implied by this
decision alone.** A future GEV committee review may now begin under the
scope and comparator set stated above; any resulting Intelligence-record
update, or any tier/target/roster/cluster/cap/allocator change, remains its
own separate, future, separately-approved governance decision, exactly as
PI-0016 §B/§I require.
