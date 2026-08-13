# WS-0014 Level 1 Architecture Amendment Design Audit — 2026-08-13

## Status and authority boundary

This is a non-authoritative supporting audit for `XASSET-0019`. It records the evidence review,
methodology risk register, and preservation analysis. The decision file is the sole operative
authority. This audit creates no percentage, policy target, research authority, portfolio change, or
brokerage authority.

The review began at GitHub/local/origin main
`36a31ebc7a8997d59a427174420cb9b7eb670a82`, the verified merge commit of PR #312. GitHub showed zero
open pull requests. PR #311 and PR #312 were merged; LEVEL2-0001 was present as a 34-instrument
research-cohort freeze only. `XASSET-0019` had no decision file, catalog row, branch, or open PR; its
only repository mentions reserved a contemplated future topic. The primary checkout’s untracked
`AGENTS.md` and `.worktrees/` were preserved by using a clean dedicated worktree.

## Review method

Each requested architecture claim was re-derived from merged repository authority. Classification
means:

- `CONFIRMED`: directly supported or follows necessarily from the governed record set;
- `PARTIALLY_CONFIRMED`: the evidence supports the substance but current accepted methodology uses a
  conflicting historical interpretation or the requested conclusion is a new bounded governance
  judgment; and
- `NOT_SUPPORTED`: no sufficient repository basis. A major `NOT_SUPPORTED` premise would have stopped
  the filing.

No major premise was unsupported.

## Finding classification

| # | Claimed finding | Result | Repository-grounded conclusion |
|---|---|---|---|
| 1 | Current Level 1 objects are heterogeneous | `CONFIRMED` | Profiles and doctrine describe four asset sleeves, an unresolved combined cash/reserve family, and debt reduction as `reduces_liability_not_an_asset` / a margin-policy lever. |
| 2 | Six-way equal baseline was provisional, not empirically validated | `CONFIRMED` | XASSET-0016 and its audit call the outputs provisional class-5 guardrails and disclose that no empirical sweep/backtest calibrated the baseline. |
| 3 | R2/R3 and the fixed increment encode readiness/uncertainty rather than validated economic capital drivers | `CONFIRMED` | R2 reads deferred relationship coverage; R3 reads secondary-condition breadth. Their rationale is governance uncertainty and their increment is explicitly not empirically calibrated. |
| 4 | Current schema-2.0 figures are historical provisional results, not adopted policy | `CONFIRMED` | XASSET-0018 and every record’s authority boundary say `provisional_not_adopted` and prohibit downstream Level 2/configuration authority. |
| 5 | Debt reduction should become a liability/cash-flow control | `PARTIALLY_CONFIRMED` | Functional doctrine proves it reduces a liability and has no market asset/target row. XASSET-0016 nevertheless placed it in the six-member denominator; changing that future interpretation therefore requires the explicit partial supersession made by XASSET-0019. |
| 6 | The residual is unassigned, not cash/debt/deployable | `CONFIRMED` | Schema-2.0 forces `unsized_unassigned_capital`, null sleeve ID, prohibited cash equivalence, prohibited redistribution, and `not_a_target`. |
| 7 | No adopted marginal-capital mechanism answers why the next dollar belongs in one destination | `CONFIRMED` | XASSET-0001 requires opportunity-cost comparison, while current R2/R3 only transform readiness/uncertainty counts. No accepted record completes the destination-level economic comparison. |
| 8 | No complete economic whole-100% reconciliation exists | `CONFIRMED` | A complete computational identity exists, but one-third remains economically unassigned and no separate asset-state/flow ledger reconciles liability actions without double counting. |
| 9 | Empirical risk must challenge provisional sizing before final Level 2 sizing | `PARTIALLY_CONFIRMED` | Existing roadmap requires descriptive risk to challenge/refine provisional sizing, but placed it after provisional sleeve/instrument sizing. Moving the checkpoint before final Level 2 sizing is a justified sequencing amendment, not a claim about prior sequence. |
| 10 | Construction needs bounded preregistered iteration | `PARTIALLY_CONFIRMED` | Preregistration/no-automatic-adoption controls are established, but no closed reopen-class model governed feedback from risk/stress to ontology, membership, and sizing. XASSET-0019 supplies that missing boundary. |
| 11 | Strong governance controls remain valid | `CONFIRMED` | Constitution, OPS-0009, OPS-0014, GOV-0003, MARGIN doctrine, XASSET-0016/18, and LEVEL2-0001 preserve the named controls. |

## Verified architecture findings

### Heterogeneous ontology

The current `sleeve_id` label is a historical schema identifier, not proof that every object is an
economically investable sleeve:

- `equity`, `fund_broad_market`, `fund_gld_defensive`, and `crypto` hold investable assets;
- CASH is characterized as operational liquidity;
- RESERVE’s purpose is explicitly unresolved and must not be inferred;
- `cash_reserve` combines those two without proving one economic function; and
- DEBT_REDUCTION’s capital-preservation character is `reduces_liability_not_an_asset`, its liquidity
  character is `not_applicable`, its profile calls it a margin-policy lever, and no destination row
  exists for it.

The new closed ontology therefore distinguishes asset sleeve, liquidity asset, liquidity constraint,
liability-flow control, and unsized-unassigned capital. It does not decide the future cash split.

### Historical scaffold versus economic method

The equal baseline served a real anti-anchoring purpose: it did not inherit current target weights and
gave a deterministic starting point. R2/R3 then applied symmetrically and reproducibly. That makes the
method computationally coherent. It does not establish that unlike asset, liquidity, and liability
roles deserve equal shares, that deferred-pair counts measure expected capital utility, or that the
chosen increment is an empirically supported economic distance.

The schema-2.0 outputs are preserved exactly as historical results:

| Object | Historical output | Post-amendment downstream authority |
|---|---:|---|
| equity | 18.67% | none for final targets or Level 2 sizing |
| fund_broad_market | 14.67% | none for final targets or Level 2 sizing |
| fund_gld_defensive | 16.67% | none for final targets or Level 2 sizing |
| crypto | 16.67% | none for final targets or Level 2 sizing |
| cash_reserve | null | unresolved; later migration required |
| debt_reduction | null | liability-flow control; no persistent target |
| residual | 33.32% | `UNSIZED_UNASSIGNED_CAPITAL`; no automatic use |

## Verified margin and debt findings

Margin doctrine states that margin is borrowed buying power, a liability and risk-governance concern,
not an asset or alpha source. DEBT_REDUCTION avoids financing cost and changes survival/buffer posture
only when actual debt exists. The functional-doctrine record intentionally separates avoided-cost
analysis from survivability analysis and has no completed economic method for either.

The governing consequence is narrow:

- debt repayment is a flow applied to a liability, outside the asset-allocation denominator;
- it is inactive when there is no debt;
- it may compete for contributions/proceeds only through a later explicit flow rule;
- it cannot own the residual or count simultaneously as cash; and
- no repayment rate, leverage target, trigger, threshold, or priority is supported here.

MARGIN-0001’s existing hard limits, MARGIN-0004’s mixed historical evidence, MARGIN-0005’s bounded
research charter, and the Constitution’s asymmetric risk-reduction discretion remain unchanged.
Unlevered construction remains prior to margin-policy reconsideration.

## Methodology risk register

| Risk | Existing manifestation | Control adopted by XASSET-0019 |
|---|---|---|
| Type error | Asset sleeves, cash concepts, and debt action share one denominator vocabulary | Closed typed ontology; debt excluded; cash migration required |
| Equal-share anchoring | Reproducible seed can be mistaken for economic equality | Historical-only authority and explicit future denominator prohibition |
| Metadata-to-capital leakage | Readiness/uncertainty counts directly change provisional targets | R2/R3 future numeric effect `none` absent later evidence-supported reauthorization |
| False precision | Two-decimal stored outputs look economically exact | Separate computational precision from economic certainty; approximate/provisional human reporting |
| Residual capture | Unassigned capital could be called cash or repayment | Forced independent state; no automatic redistribution or deployment |
| Double counting | One dollar could appear as cash and debt repayment | Separate asset-state and flow ledgers; no dollar counted twice |
| Missing opportunity cost | No rule explains why one alternative receives the marginal dollar | Explicit DRIVERS / CONSTRAINTS / DISCLOSURES comparison requirement |
| One-way pipeline | Later stress evidence has no governed route back to sizing | Preregistered reopen classes and one bounded revision authority |
| Hidden optimization | Risk study could become best-weight search | Explicit early-RISK prohibitions and no composite score |
| Status ambiguity | Merged methodology and adopted portfolio policy can be conflated | Four-status conceptual boundary; future GOV cleanup recommendation |
| Constraint erosion | Iteration could loosen hard limits indirectly | Separate high-authority review for loosening; existing limits preserved |

## Marginal-capital and reconciliation design

A credible capital proposal must compare each destination against credible alternatives using
portfolio function, downside/recovery, diversification, liquidity, valuation/opportunity cost,
evidence uncertainty, and avoided financing cost when debt exists. Drivers explain preference;
constraints bound the feasible set; disclosures communicate uncertainty. They are not blended into a
composite score.

Before full-portfolio stress, a non-adopted candidate asset-state ledger must account for every
asset-side percentage point using an explicitly justified candidate treatment. It may not normalize
an incomplete candidate, use unassigned capital as a balancing plug, or invent a cash, zero-risk,
benchmark, debt-reduction, or other return/risk proxy to complete a portfolio curve. If a complete
lawful candidate cannot be formed, full-portfolio stress remains blocked and the work returns to the
appropriate preregistered checkpoint.

After full-portfolio unlevered stress and any permitted bounded revision, a distinct final
whole-`100%` reconciliation accounts for investable sleeves, separately justified strategic cash,
and any explicitly governed unassigned capital before a separate policy-adoption lifecycle. Both
reconciliations remain non-adopted. The separate flow ledger accounts for contributions/proceeds,
debt repayment, retained liquidity, and asset deployment. The ledgers reconcile but do not collapse
asset states into flow actions. An unexplained residual fails; an explicitly governed residual may
remain only with a status, rationale, review trigger, and no automatic deployment.

## Iteration and downstream sequence

The bounded sequence is:

`roles/constraints → frozen research cohort → early empirical diagnostics → provisional Level 1
sizing/ranges → Level 2 membership/sizing → non-adopted candidate whole-100% reconciliation →
full-portfolio unlevered stress → bounded preregistered revision → final whole-100% reconciliation →
separate portfolio-policy adoption → post-adoption unlevered implementation validation → margin/debt
research and policy → monitoring/deployment`.

Ontology, membership, Level 1 sizing, Level 2 sizing, and constraints are separate reopen classes.
Every later study must declare in advance which class it may reopen. A triggered revision stays within
that class and returns to the next affected checkpoint. Candidate-reconciliation failure returns to
the applicable preregistered class. A stress-triggered revision must reconcile the revised candidate
again before any protocol-permitted stress rerun. Further cycling requires new authority; constraint
loosening requires separate high-authority review.

The next RISK methodology is early evidence, not a ratification step. It must challenge all four
historical magnitudes and whether point targets are warranted; allow ranges, representation
sensitivity, and nulls; and prohibit best-weight search, hidden optimization, final selection/sizing,
debt return series, margin policy, and automatic adoption. It may examine individual sleeve scenarios
without constructing a whole-`100%` portfolio, assigning residual capital, or selecting final Level 2
weights; that early checkpoint is distinct from later full-portfolio stress.

## Supersession and preservation audit

| Item | Result | Preserved substance |
|---|---|---|
| XASSET-0001 | `INTERPRETATION_AMENDED` | Whole-portfolio intent, Level 1/Level 2 separation, opportunity-cost requirement |
| XASSET-0012 | `INTERPRETATION_AMENDED` | Profile/relationship synthesis evidence and abstentions |
| XASSET-0013 | `INTERPRETATION_AMENDED` | Sealed content and provenance |
| XASSET-0014 | `INTERPRETATION_AMENDED` | Axis computation as historical readiness method |
| XASSET-0015 | `INTERPRETATION_AMENDED` | Sealed analytical records |
| XASSET-0016 | `PARTIALLY_SUPERSEDED` | Historical deterministic derivation and reconciliation evidence |
| XASSET-0017 | `UNCHANGED` | Broad-market role evidence |
| XASSET-0018 | `PARTIALLY_SUPERSEDED` | Closed schema, historical figures, reproducibility |
| Functional doctrine | `INTERPRETATION_AMENDED` | CASH evidence, RESERVE abstention, debt/margin evidence |
| Profiles | `INTERPRETATION_AMENDED` | Historical role and evidence summaries |
| Relationships | `INTERPRETATION_AMENDED` | Comparative facts, conditions, abstentions |
| Policy-adoption records | `INTERPRETATION_AMENDED` | Historical axis/readiness results |
| Numeric records/manifest | `PARTIALLY_SUPERSEDED` | Byte-preserved historical outputs and provenance |
| Validators/tests | `UNCHANGED` | Historical computational-conformance checks |
| LEVEL2-0001 | `UNCHANGED` | Frozen research cohort and selection-only boundary |
| Legacy cash_reserve | `REQUIRES_LATER_MIGRATION` | No forced interpretation before evidence/clarification |

Preserved controls: one mutation lane, independent exact-head review, source hashes, abstention,
preregistration, protected scope, no automatic adoption, Level 1/Level 2 separation, chart/policy
separation, manual execution, risk-reducing asymmetric discretion, unlevered-before-margin sequencing,
and existing margin hard limits.

## Source pins

Hashes are SHA-256 of repository file bytes at starting main
`36a31ebc7a8997d59a427174420cb9b7eb670a82`.

| Source | SHA-256 |
|---|---|
| `constitution/INVESTMENT_CONSTITUTION.md` | `f564b0a37946b8ebf2decdda54972af68f2490d4f1717d8844c1008bad2af400` |
| `governance/decisions/GOV-0001-governance-architecture-adopted.md` | `238da85169fddb6ad2808410ac03c09506de26f716bf7cc7f4cff8432754b325` |
| `governance/decisions/GOV-0002-operational-precedence-hierarchy.md` | `1e93490990fbf252c11bf2985892d7efd33fbf142ff2c487da3cde7066491a89` |
| `governance/decisions/GOV-0003-margin-conditional-research-permitted.md` | `599801feaf4f2f200b6175e5c3be7321ba33b10e2bc7bea9ee862549b76538e4` |
| `governance/decisions/OPS-0009-lean-delivery-review-lifecycle-v1.md` | `e0772b1acb63dd3b5669fbc2f7e3a9b32c0e86dfef8df528e5c00a83caf4ed4c` |
| `governance/decisions/OPS-0014-routine-operational-sync.md` | `072c07f101749cd7f1732bd45eb74307195908f47934c0a77dbcb6df5ef6ca82` |
| `governance/decisions/NUM-0001-numeric-parameter-provenance-standards.md` | `33e4b3810405f9bba80adc4be265fcf72fdcf1bf6643cf2114475bc1a060b0ca` |
| `governance/decisions/XASSET-0001-cross-asset-whole-portfolio-allocation-architecture.md` | `0e73d3ab13d15234e2ba23f8eb5a521fc38f9ab4d89748ad445a8387d50a2b12` |
| `governance/decisions/XASSET-0012-ws0014-level1-cross-asset-synthesis-methodology.md` | `4f9ba2676abdc275b7e345a8c4b7e1f97efadd894e11783e12a8a41d840bf3c5` |
| `governance/decisions/XASSET-0013-ws0014-level1-synthesis-content-authorization.md` | `814a8e56a2e22047f421fa56189feb6783be3a747a258cbd05a8d1069d1058c7` |
| `governance/decisions/XASSET-0014-ws0014-level1-policy-adoption-methodology.md` | `122fc0412f9d03522cc0fcf1c89825e93975aa05c54a07e8c362fdec86739b15` |
| `governance/decisions/XASSET-0015-ws0014-level1-policy-adoption-content-authorization.md` | `09d66999eac657e67e428ae3a8d60cf5891bc1bb556e6997e4d5e6e988bdc0fb` |
| `governance/decisions/XASSET-0016-ws0014-level1-numeric-sizing-methodology-and-authorization.md` | `b02d63bb8070e827bec027355a0aa5c4da5958910aba38e1d2f8dba774290c3f` |
| `governance/audits/WS0014_LEVEL1_NUMERIC_SIZING_METHODOLOGY_AND_AUTHORIZATION_20260812.md` | `d1b177443ee84f74a6bd76496d8559b18a824c11f150d516bb00dfd9b23c2284` |
| `governance/decisions/XASSET-0017-fund-broad-market-role-redetermination.md` | `6d2a2539f8458ef9cf2c7a5818560a3d2ac67026bf45622857677a8ba11b9434` |
| `governance/decisions/XASSET-0018-numeric-sizing-structural-authority.md` | `2f98e3be41bcef026e773943aa63e3055a4305585152971c930a8c74d30c6dfc` |
| `governance/decisions/LEVEL2-0001-selection-only-research-cohort-freeze.md` | `3d51441b5da238073fbf2712a35fff669d00d291951b27ef4188bd35db2a57ad` |
| `docs/MARGIN_DOCTRINE.md` | `0883d1fd0ce0f7b9b565c74836691cfa7317b1ac00e5e0b4af3aec81dd819e1f` |
| `governance/decisions/MARGIN-0004-phase3-7a-closure-reconciliation.md` | `96599464ca560c590a7c0c702db5c67c86f69dc2d6fdb533236b0374db6b3c03` |
| `governance/decisions/MARGIN-0005-margin-target-research-charter.md` | `56efb361bd8d25c4fc31eb01d109a964e05cac7b41ac42e8fabc643300df49b9` |
| `intelligence/functional_doctrine/CASH.yaml` | `afdf671b0c4e46aa9c270140cd7414bb2ec08e6903bb62ee302384a6c3ff0356` |
| `intelligence/functional_doctrine/RESERVE.yaml` | `b9660e077a67775f0f8be5161e96f92e4e4b421a447749c8ad345b438d169b42` |
| `intelligence/functional_doctrine/DEBT_REDUCTION.yaml` | `b0d015b8570e9cc6369c43957a2b111f18437d1f45df870fbd9903bed2fe5794` |
| `intelligence/level1_sleeve_synthesis/profiles/COHORT_MANIFEST.yaml` | `3a8890908dd31c94a085bf8c8e68afe0e67120b53c13f6e5279344be1a8e7b15` |
| `intelligence/level1_sleeve_synthesis/relationships/COHORT_MANIFEST.yaml` | `60cb43d3815cb9f35715beadd4b5f6f555a11e50fa5eedd21343ee86eeff8d96` |
| `intelligence/level1_sleeve_synthesis/policy_adoption/COHORT_MANIFEST.yaml` | `08f289ce79481df7e50c1d3f50c1f9402a4c331d2c70b8ef02d99e2efef2b8a8` |
| `intelligence/level1_sleeve_synthesis/numeric_sizing/COHORT_MANIFEST.yaml` | `033ecc3944060ee9811a361a4ee2cbc176bfe2920691507a56cd306cd0226f76` |
| `governance/evidence/LEVEL2-0001/RESEARCH_COHORT_FREEZE.yaml` | `e65699d2e2f627185edcf9006c87b31c7fcd55ffc38dafe26e5c208da3dbafa0` |
| `decision_log.yaml` | `0b383365faa5bf0dc2ab71bd5947e839f28eece0c295e75c23206d84003d77c2` |
| `operations/WORKSTREAMS.yaml` (starting-main blob) | `576ed950b1e169f848b588cf7bf8ea923936b7a1f5cf6120489860cb2dec7c57` |

## Explicit non-authority and next sequence

The old provisional figures are not final GLD, crypto, equity, or broad-market policy; the residual is
not cash; debt reduction is not an investable sleeve; R2/R3 do not remain future capital drivers.

This audit authorizes nothing. After XASSET-0019 becomes effective, the next separately governed work
is the early RISK methodology. Replacement economic sizing follows that evidence. Final Level 2
selection/sizing remains paused; a complete non-adopted candidate reconciliation is mandatory before
full-portfolio stress; final reconciliation remains mandatory after bounded revision and before any
portfolio-policy adoption; and margin numeric policy remains downstream.
