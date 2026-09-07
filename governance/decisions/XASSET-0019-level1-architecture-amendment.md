---
decision_id: XASSET-0019
date: 2026-08-13
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, MARGIN-0001, MARGIN-0004, MARGIN-0005, XASSET-0001, XASSET-0012, XASSET-0013, XASSET-0014, XASSET-0015, XASSET-0016, XASSET-0017, XASSET-0018, LEVEL2-0001]
supporting_artifact: governance/audits/WS0014_LEVEL1_ARCHITECTURE_AMENDMENT_DESIGN_20260813.md
file: governance/decisions/XASSET-0019-level1-architecture-amendment.md
---

## Context

The accepted Level 1 sequence created a reproducible provisional sizing scaffold: six named
capital-use objects shared an equal starting baseline, two closed comparative rules could adjust
eligible sleeves, blocked objects remained null, and the remainder reconciled arithmetically as
unsized unassigned capital. XASSET-0018 then made the resulting schema-2.0 authority recursively
closed. The implementation is mechanically sound and remains useful as historical evidence.

A direct architecture review, retained in the supporting audit, found that the six objects are not
economically homogeneous. Four are investable asset sleeves; `cash_reserve` combines unresolved
liquidity concepts; and `debt_reduction` reduces a liability rather than owning an asset. It also
confirmed that the equal-share baseline and R2/R3 adjustment increment were deliberately
provisional governance choices, not empirically calibrated economic capital drivers. The current
records therefore answer “what did the historical method produce?” but not “why should the next
marginal dollar go to one destination instead of another?” or “how does the economically governed
whole portfolio reconcile?”

This is one connected Level 1 architecture amendment. It does not invalidate historical arithmetic,
select a replacement percentage, run a backtest, select or size Level 2 instruments, or change
portfolio configuration.

## Decision

### A. Effective boundary and status

This file is a **proposed decision** while its pull request is open. Principal exact-head acceptance
is required before merge. Only after that accepted head merges does this amendment become
**effective merged methodology**. Effective methodology is not an **adopted portfolio policy**:
portfolio adoption remains a separate later decision after the sequence in §J is complete.

The existing schema-2.0 outputs remain **provisional analytical results**. “Computationally derived,”
“economically validated,” “empirically diagnosed,” and “policy adopted” are separate statuses; none
implies another. A superseded method may remain historically valid and reproducible.

### B. Closed Level 1 ontology

Future Level 1 work must use exactly these architecture types unless a later accepted amendment
changes the ontology:

| Architecture type | Meaning | Current classification |
|---|---|---|
| `INVESTABLE_ASSET_SLEEVE` | An asset-holding capital destination eligible for future asset-allocation sizing | `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto` |
| `LIQUIDITY_ASSET` | An actually held liquidity asset with a defined portfolio function | No single current `cash_reserve` classification; later migration required |
| `LIQUIDITY_CONSTRAINT` | A minimum or other boundary on available liquidity; a constraint, not an asset sleeve | Later methodology required |
| `LIABILITY_FLOW_CONTROL` | A state-dependent rule governing cash flows applied to a liability | `debt_reduction` |
| `UNSIZED_UNASSIGNED_CAPITAL` | Capital not yet economically assigned; neither an asset sleeve nor a flow action | The historical schema-2.0 residual, subject to §I |

An object may not silently perform more than one of these roles. A future implementation that needs
a new role must amend the closed ontology rather than overloading an existing identifier.

### C. `debt_reduction` reclassification

For every future Level 1 sizing or adoption decision, `debt_reduction` is a
`LIABILITY_FLOW_CONTROL`, not an investable asset sleeve. It:

- is excluded from the asset-allocation sizing denominator;
- has no persistent portfolio target weight;
- is state-dependent on actual debt and is inactive/not applicable when debt is zero;
- may govern future contributions or proceeds only under a separately accepted rule;
- never owns residual or unassigned capital by default;
- cannot count the same dollar as a liquidity asset or reserve; and
- receives no contribution fraction, repayment fraction, leverage target, debt threshold, margin
  trigger, or waterfall priority from this amendment.

This classification supersedes XASSET-0016’s future treatment of `debt_reduction` as one
percentage-bearing denominator member. It does not rewrite or invalidate the historical six-member
calculation and does not alter any current margin rule.

### D. Cash and liquidity boundary

The legacy `cash_reserve` family may not silently continue as one undifferentiated bucket. Before any
cash percentage or policy is proposed, future work must distinguish, as applicable:

1. operational and settlement liquidity (`LIQUIDITY_ASSET`);
2. any required liquidity boundary (`LIQUIDITY_CONSTRAINT`);
3. strategic cash or dry powder, only if separately justified and adopted as an asset role; and
4. margin-related liquidity constraints, downstream of unlevered portfolio construction.

The sealed CASH evidence remains evidence for an operational-liquidity function. The sealed RESERVE
abstention remains unresolved. This decision adopts no cash percentage, does not infer a RESERVE
purpose, and requires a later explicit migration before `cash_reserve` may participate in economic
sizing.

### E. Historical baseline and R2/R3

The six-way `100 / 6 = 16.67%` baseline remains a reproducible historical anti-anchoring seed and
provisional scaffold. For work after this amendment it is **partially superseded** and may not be
treated as:

- final economic sizing or adopted policy;
- evidence that unlike capital-use types deserve equal capital;
- the denominator for a future Level 1 allocation; or
- an input authority for final Level 1 targets or Level 2 sizing.

R2 (relative relationship-coverage state), R3 (relative secondary-condition breadth), and the fixed
`±2.00` percentage-point increment retain their historical derivation. For future economic sizing,
R2/R3 are readiness, uncertainty, and diagnostic metadata only. Their numeric effect is `none` unless
a later accepted method separately reauthorizes a capital effect with evidence appropriate to that
effect. This decision creates no replacement increment or score.

### F. Current schema-2.0 numeric records

The six records and manifest under
`intelligence/level1_sleeve_synthesis/numeric_sizing/` remain byte-unchanged. Their current historical
outputs are:

- `equity`: `18.67%`;
- `fund_broad_market`: `14.67%`;
- `fund_gld_defensive`: `16.67%`;
- `crypto`: `16.67%`;
- `cash_reserve`: null;
- `debt_reduction`: null; and
- residual: `33.32%`.

These are historically valid, computationally derived, provisional, economically unvalidated, and
not policy adopted. After this amendment they are prohibited as input authority for final Level 1
targets, final Level 2 membership or sizing, portfolio configuration, deployment, or brokerage
action. The historical validator may continue validating the method that produced them; validator
success proves computational conformance, not economic validity.

Two-decimal storage remains appropriate for reproducing and reconciling the historical computation.
It does not imply `0.01%` economic certainty. Future human-facing reporting must label provisional or
approximate status conspicuously and must not present historical precision as confidence.

### G. Marginal-capital requirement

Every future proposal to assign or change capital must answer:

> Why should the next marginal dollar go to this destination instead of each credible alternative?

The comparison must keep three categories separate:

- **DRIVERS** — portfolio function, downside and recovery behavior, diversification contribution,
  liquidity, valuation/opportunity cost, evidence uncertainty, and avoided financing cost where
  actual debt exists, as applicable;
- **CONSTRAINTS** — constitutional and accepted policy limits, liquidity requirements, concentration
  boundaries, abstentions, evidence gates, and margin hard limits; and
- **DISCLOSURES** — limitations, representation sensitivity, freshness, unresolved evidence, and
  decision uncertainty that inform interpretation without becoming hidden arithmetic.

No composite score is authorized. No proportional or automatic redistribution is the default. An
abstention or explicit unassigned-capital state remains valid when evidence does not justify a
destination.

### H. Asset-state and flow ledgers

Two distinct whole-`100%` reconciliations are required. Neither one adopts portfolio policy.

**Non-adopted candidate whole-100% reconciliation.** After provisional Level 1 sizing/ranges and
Level 2 membership/sizing, but before full-portfolio stress, a research/policy candidate must provide
a complete, internally reconciled asset-state representation. It is not adopted policy and has no
production authority. Every asset-side percentage point must have an explicitly modeled candidate
treatment supported by the marginal-capital comparison in §G. No amount may be assigned merely as a
balancing plug, automatically redistributed, or anchored to a historical target. Any strategic-cash
candidate treatment must itself be separately justified under this architecture. Liability-flow
controls remain outside the asset denominator.

Full-portfolio stress may run only on that fully specified, internally reconciled, non-adopted
candidate asset-state representation. It may not normalize incomplete assigned sleeves to `100%`,
silently allocate a residual, assume a residual is cash, reserve, or debt reduction, apply a
synthetic zero-return series, use a benchmark or other proxy as filler, or assign capital merely to
make a portfolio curve possible. Unresolved or unassigned capital receives no invented cash,
zero-risk, benchmark, or other return/risk proxy. If no complete lawful candidate can be formed,
full-portfolio stress must abstain and remain blocked while the work returns to the appropriate
preregistered checkpoint in §I.

**Final whole-100% reconciliation.** After full-portfolio unlevered stress and any permitted bounded,
preregistered revision, a final economically reconciled candidate must cover the whole `100%`
asset state before it may proceed to a separate portfolio-policy-adoption lifecycle. It incorporates
only lawful bounded revisions, remains non-adopted until that later lifecycle completes, and must
separately identify:

- investable asset sleeves;
- governed strategic cash, if any is later adopted; and
- explicitly governed `UNSIZED_UNASSIGNED_CAPITAL`, if any remains.

Liability-flow controls do not enter the asset-allocation denominator. A separate flow ledger must
reconcile contributions and proceeds, debt repayment, retained liquidity, and asset deployment. No
dollar may appear in both ledgers as two simultaneous uses. An unexplained residual is rejected.

A nonzero `UNSIZED_UNASSIGNED_CAPITAL` balance may persist only when its rationale, status, review
trigger, and prohibition on automatic deployment are explicit. It is not cash, reserve, debt
repayment, deployable capital, or an automatic redistribution pool.

### I. Bounded iterative construction and reopen gates

Future portfolio construction follows this sequence:

`roles/constraints → frozen research cohort → early empirical diagnostics → provisional Level 1
sizing/ranges → Level 2 membership/sizing → non-adopted candidate whole-100% reconciliation →
full-portfolio unlevered stress → bounded preregistered revision → final whole-100% reconciliation →
separate portfolio-policy adoption → post-adoption unlevered implementation validation → margin/debt
research and policy → monitoring/deployment`.

Every authorized study or construction filing must preregister which of these reopen classes its
evidence may affect:

| Reopen class | Permitted trigger | Boundary |
|---|---|---|
| `ONTOLOGY` | Evidence that a governed object is mis-typed or a required role is absent | Separate architecture amendment |
| `MEMBERSHIP` | Governed cohort/evidence-parity or representation failure | Selection-only decision; no implicit sizing change |
| `LEVEL1_SIZING` | Material diagnostic or reconciliation failure at sleeve level | Only preregistered sleeves/assumptions may be revised |
| `LEVEL2_SIZING` | Instrument-level or full-portfolio stress failure | Only preregistered instruments/assumptions may be revised |
| `CONSTRAINTS` | Evidence that a constraint is insufficient, contradictory, or infeasible | Tightening may be proposed separately; loosening requires separate high-authority review |

Failure to form the non-adopted candidate reconciliation returns the work to the appropriate
preregistered `ONTOLOGY`, `MEMBERSHIP`, `LEVEL1_SIZING`, `LEVEL2_SIZING`, or `CONSTRAINTS` checkpoint;
it does not authorize a plug or proxy. A stress finding may reopen only its preregistered class. Any
revised candidate must complete the non-adopted candidate reconciliation again before stress may be
rerun, and only to the extent that the preregistered protocol permits that rerun. Each revision must
cite the triggering evidence, remain inside the preregistered class and protected scope, and return
to the next affected checkpoint. Repeated cycling, retrospective objective changes, and a post-hoc
best-weight optimizer are prohibited. Further iteration after the preregistered bounded revision
requires a new explicit authorization.

### J. Early empirical-risk checkpoint

The next separately authorized RISK study must challenge rather than ratify the provisional magnitude
or point-target premise for equity, broad-market funds, GLD, and crypto before final Level 2 sizing.
It may examine ranges, representation sensitivity, honest null/inconclusive results, drawdown,
recovery, diversification, and liquidity evidence.

This early empirical checkpoint may challenge individual investable-sleeve scenarios without first
constructing a whole-`100%` portfolio. It does not assign residual capital, perform the non-adopted
candidate reconciliation, or select final Level 2 weights. Later full-portfolio unlevered stress is a
different checkpoint and requires the complete candidate representation in §H.

It may not search for the best historical weight, hide optimization inside a score or sweep, select
final membership, assign final Level 2 weights, manufacture a debt return series, change margin
policy, or cause automatic adoption. Any backtest or empirical computation requires its own bounded,
preregistered authority. The already frozen LEVEL2-0001 population remains a research cohort only.

### K. Supersession map

This map is exhaustive for the affected Level 1 chain; unaffected evidence is not broadly
superseded.

| Authority or artifact | Classification | Effect |
|---|---|---|
| `XASSET-0001` | `INTERPRETATION_AMENDED` | Preserve two-level separation and opportunity-cost requirement; retype debt and require explicit reconciliation/iteration. |
| `XASSET-0012` | `INTERPRETATION_AMENDED` | Preserve synthesis evidence; the six identifiers are no longer presumed homogeneous economic sleeves. |
| `XASSET-0013` | `INTERPRETATION_AMENDED` | Preserve profiles/relationships as evidence; debt comparisons become liability-flow diagnostics. |
| `XASSET-0014` | `INTERPRETATION_AMENDED` | Preserve Axis methodology as historical readiness analysis; Axis status is not economic capital authority. |
| `XASSET-0015` | `INTERPRETATION_AMENDED` | Preserve sealed policy-adoption records as historical analytical dispositions, not adopted portfolio policy. |
| `XASSET-0016` | `PARTIALLY_SUPERSEDED` | Retain historical derivation; retire six-way denominator, R2/R3 numeric effect, and outputs as future economic authority. |
| `XASSET-0017` | `UNCHANGED` | Broad-market role redetermination remains historical evidence; it grants no final sizing authority. |
| `XASSET-0018` | `PARTIALLY_SUPERSEDED` | Preserve schema-2.0 closure and historical computation; prohibit its outputs as downstream final sizing authority. |
| functional doctrine | `INTERPRETATION_AMENDED` | Preserve sealed evidence; debt is a liability-flow control and CASH/RESERVE need later separation. |
| Level 1 profiles | `INTERPRETATION_AMENDED` | Preserve evidence; legacy `sleeve_id` does not override this typed ontology. |
| Level 1 relationships | `INTERPRETATION_AMENDED` | Preserve comparative evidence; readiness/uncertainty does not itself allocate capital. |
| policy-adoption records | `INTERPRETATION_AMENDED` | Preserve analytical statuses; the directory name is not proof of adopted portfolio policy. |
| numeric-sizing records and manifest | `PARTIALLY_SUPERSEDED` | Historical/reproducible only; no final Level 1 or Level 2 downstream authority. |
| numeric-sizing validator/tests | `UNCHANGED` | May validate historical conformance; cannot establish economic validity or policy adoption. |
| `LEVEL2-0001` | `UNCHANGED` | Research-cohort freeze only; final membership and sizing remain unauthorized. |
| legacy `cash_reserve` representation | `REQUIRES_LATER_MIGRATION` | Must be separated into adopted liquidity roles/constraints before economic sizing. |

No historical record is rewritten by this map.

### L. Preserved controls and non-authorization

Unchanged and binding: one mutation lane; OPS-0009 independent exact-head review and principal
acceptance; source hashes; abstention; preregistration; protected scope; no automatic adoption;
Level 1/Level 2 separation; chart/policy separation; recommendation-only manual execution;
risk-reducing asymmetric discretion; unlevered-before-margin sequencing; and every existing margin
hard limit until a separate higher-authority amendment changes one.

This amendment authorizes no percentage, target, range, score, backtest, robustness calculation,
final Level 2 member, instrument weight, cash target, debt repayment rate, leverage change, trade,
allocation check, or portfolio-configuration change. It does not edit any sealed Intelligence or
numeric-sizing record. Early RISK work, a replacement numeric method, final Level 2 work, margin
numeric policy, and portfolio adoption each require separate later authority.

### M. Status-vocabulary maintenance

This decision does not migrate repository-wide frontmatter. The existing
`Proposed | Accepted | Superseded | Archived` decision-file vocabulary and historical structured-ledger
vocabularies remain as documented. Because several merged decisions retain `status: Proposed`, a
future separate GOV maintenance unit should reconcile filing status, principal acceptance, merged
methodology effectiveness, analytical-result status, portfolio-policy adoption, and supersession
without rewriting substantive history. Until then, this decision’s §A boundary governs its own
interpretation.

## Rationale

Equal treatment was useful for avoiding inherited-target anchoring, but equality among unlike
objects is not an economic conclusion. Relationship completeness and disclosed uncertainty are
important governance signals, but they do not explain the opportunity cost of allocating the next
dollar. Separating asset states from liability flows prevents denominator distortion and double
counting. Requiring early empirical challenge, a complete non-adopted candidate before stress,
bounded revisions, and final whole-portfolio reconciliation closes those gaps while preserving every
strong control and every reproducible historical artifact.

## Alternatives Considered

**Keep schema-2.0 as future target authority because it validates cleanly.** Rejected: validation
proves exact implementation of the historical method, not the method’s economic sufficiency.

**Delete or rewrite the historical numeric records.** Rejected: they are valid provenance and their
preservation makes the supersession auditable.

**Give the residual to cash or debt reduction.** Rejected: either move would silently adopt an
economic destination and could double count asset state and liability flow.

**Choose replacement weights or optimize them here.** Rejected: the architecture review supplies no
authority for new numbers, and doing so would bypass the empirical checkpoint and preregistration.

**Split debt, cash, numeric authority, and iteration into separate decisions.** Rejected: they are
one denominator-and-reconciliation defect; splitting them would leave internally conflicting Level 1
authority during the transition.

## Consequences

After this decision’s independent exact-head review, principal acceptance, merge, and post-merge
verification, future work must use the typed ontology and revised sequence above. The next eligible
unit is a separately governed early RISK methodology; it must not ratify or optimize the old figures.
A replacement economic sizing method follows evidence, then final Level 2 work, non-adopted candidate
whole-100% reconciliation, and full-portfolio unlevered stress, then bounded revision and final
whole-100% reconciliation before any separate portfolio-policy adoption.

The historical files, current portfolio configuration, allocator, holdings, gates, margin settings,
and execution model do not change.
