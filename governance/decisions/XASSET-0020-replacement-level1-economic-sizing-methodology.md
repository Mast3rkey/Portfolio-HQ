---
decision_id: XASSET-0020
date: 2026-08-14
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, GOV-0003, OPS-0009, OPS-0014, NUM-0001, XASSET-0001, XASSET-0005, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, XASSET-0013, XASSET-0014, XASSET-0015, XASSET-0016, XASSET-0017, XASSET-0018, XASSET-0019, LEVEL2-0001, VALUATION-0002, VALUATION-0005, VALUATION-0006, VALUATION-0007, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0020-replacement-level1-economic-sizing-methodology.md
---

## Context

XASSET-0019 made the historical Level-1 sizing scaffold ineligible for future economic sizing and
required a replacement method to answer a different question: why the next marginal dollar belongs
in one investable sleeve rather than another or should remain unassigned. RISK-0001 attempt 2 has now
completed its one authorized lifecycle. Its accepted result package is admissible research evidence,
but all four family dispositions are `unable_to_determine`; the result is not a target, anchor,
adjustment, recommendation, or policy.

This decision supplies the replacement methodology only. It deliberately does not apply the method,
create a point or range, choose a sleeve weight, select Level-2 members, reconcile a real candidate
portfolio, or adopt portfolio policy.

## Decision

### A. Authority, effectivity, and lifecycle boundary

This is an `OPS-0009` Lane G filing. While its pull request is open it is proposed methodology only.
It becomes effective only after all four events occur against one exact head: independent full
exact-head review, principal exact-head acceptance, merge, and immediate post-merge verification.
Filing, CI, or review alone is insufficient. The author may commit, push, and open the draft PR but
may not self-review, principal-accept, mark ready, or merge.

The stale `status: Proposed` vocabulary on several merged predecessor files does not defeat their
actual accepted/effective history. In particular, XASSET-0019 is effective from PR #313's accepted
head `df2cb58c38a87888c476af0743884b8377b354e5`, final review `4929869313`, principal acceptance
`5284252049`, merge `0962385bf6b1b72cebe8b326da49927977db2912`, and post-merge verification
`5284447082`.

### B. Closed object model and scope

The only `INVESTABLE_ASSET_SLEEVE` values this method may size are, in canonical order:

1. `equity`;
2. `fund_broad_market`;
3. `fund_gld_defensive`; and
4. `crypto`.

The following are separate and may not be promoted into a fifth sleeve:

- `LIQUIDITY_ASSET` / liquidity state — unresolved by this decision;
- `LIQUIDITY_CONSTRAINT` — a constraint only;
- `LIABILITY_FLOW_CONTROL` / `debt_reduction` — outside asset sizing; and
- `UNSIZED_UNASSIGNED_CAPITAL` — an explicit abstention state, not an asset or flow action.

This method governs how a later, separately authorized application may produce a provisional point,
range, or abstention for each of the four sleeves. It creates no actual output.

### C. Normalized unlevered asset-state denominator

The canonical denominator is one exact normalized unit of prospective, unlevered asset-side capital,
equivalently the whole `100%` asset state. It is a mathematical normalization, not a target and not a
claim about current holdings.

The denominator:

- contains asset-side capital only;
- excludes debt, debt reduction, margin buying power, leverage, and buffer state;
- never uses current holdings, current weights, or current targets as priors;
- does not silently treat cash as a balancing plug;
- does not require the four sleeve outputs alone to exhaust the unit; and
- preserves every unsupported portion as `UNSIZED_UNASSIGNED_CAPITAL` until a separate lawful
  liquidity or allocation decision exists.

A separately governed `LIQUIDITY_ASSET` may later occupy part of the same asset state, but this
decision neither defines nor sizes it. Liability-flow controls remain in a separate flow ledger.

### D. Central marginal-capital question

Every later application must answer, for every sleeve and every direct comparison:

> Given accepted, question-matched evidence, why should the next marginal dollar be assigned to this
> sleeve rather than each credible alternative or remain unassigned?

The answer must be traceable to admitted evidence and categorical rules below. Existing ownership,
target membership, research volume, evidence maturity, or a need to make totals balance is never an
answer.

### E. Strict separation of DRIVERS, CONSTRAINTS, and DISCLOSURES

#### E.1 DRIVERS

Only these closed driver classes may support positive or negative economic allocation preference:

1. `portfolio_function` — the sleeve's directly evidenced job in the prospective portfolio;
2. `valuation_opportunity_cost` — question-matched evidence of the cost of assigning the marginal
   dollar here rather than to the direct alternative;
3. `downside_path_risk` — directly comparable loss shape, depth, or path evidence;
4. `recovery` — directly comparable recovery or time-underwater evidence;
5. `diversification_cobehavior` — direct pair evidence about duplication, shared loss mechanisms, or
   offset behavior; and
6. `sleeve_deployability` — sleeve-level convertibility, lockup, or implementation friction.

Representation sensitivity and uncertainty do not create positive preference in methodology v1.0.
They are precision gates and disclosures. A later amendment would be required to change that rule.

#### E.2 CONSTRAINTS

Constraints may block, cap, or clip a candidate. They never create preference and never redirect the
clipped amount to another sleeve. The closed classes are:

- constitutional or effective-governance limits;
- evidence admission, identity, and freshness requirements;
- accepted concentration boundaries where directly applicable;
- unresolved liquidity constraints;
- abstentions and required missingness propagation;
- the Level-2 boundary;
- the no-margin/no-debt-input rule; and
- exact-reconciliation feasibility.

Constraint clipping sends the unsupported or prohibited portion to `UNSIZED_UNASSIGNED_CAPITAL`.
It does not increase any other sleeve.

#### E.3 DISCLOSURES

Disclosures must stay visible and must not enter arithmetic or decide a direction. They include:

- source and evidence quality;
- partial evidence and selection-conditioned cohorts;
- representation disagreement and sensitivity;
- stale or unavailable evidence;
- uncomputed overlap interfaces;
- valuation partials and incompatible company-level aggregation;
- survivorship, inception, provider, and licensing limits; and
- every accepted `unable_to_determine` result and its causal trace.

### F. Closed evidence-admission contract

#### F.1 Per-item admission fields

Every evidence item in a future application must record exactly:

- `evidence_id`, exact path/source class, and exact content/file SHA-256;
- the accepted/effective governing authority and lifecycle identity;
- the exact question the item may answer;
- its `DRIVER`, `CONSTRAINT`, or `DISCLOSURE` classification;
- source-owned freshness/currentness requirement and observed state;
- representation and cohort scope;
- conflict behavior and missing-data behavior; and
- an explicit `forbidden_implications` list.

An item is admitted only when its hash matches, its governing authority is effective, its own
validator passes where one exists, its question matches the current comparison, and every governed
freshness condition passes. Historical RISK evidence remains valid as historical evidence but does
not thereby become a current market observation. If a source supplies no governed currentness rule,
it may remain a disclosure but may not become a current positive driver unless a later authorization
governs currentness. No universal age threshold or freshness penalty is invented here.

Higher-authority conflicts follow GOV-0002. Material conflict among same-level admitted drivers, or
between representations that a source requires to agree, yields `unable_to_determine`; it is never
averaged. Missing required direct evidence also yields `unable_to_determine`. `not_applicable` is
permitted only when the object model makes the driver structurally irrelevant, never as a synonym for
missing.

#### F.2 Current admissible source classes and exact snapshot

The following table freezes the current source identities for methodology review. It does not apply
them or pre-assign any driver direction. `Accepted/effective` in this table means effective through
the cited merged lifecycle despite stale catalog vocabulary. Unless a row states otherwise, a
hash/authority/currentness failure excludes the item; required missingness or same-level conflict
propagates `unable_to_determine` under §F.1.

| Evidence class and exact question it may answer | Exact source identity | Accepted/effective authority and currentness | Classification, conflict/missing behavior, and forbidden implication |
|---|---|---|---|
| Sleeve function and governed gaps: what directly evidenced portfolio job or unresolved functional gap does this sleeve have? | Profile content hashes: `equity` `1f44f44369a4c1fe9ea824d99e82539d96f9ccf6407a740ef93d182a8b64bedc`; `fund_broad_market` `2ed99d67847a9aea644be6867c53cac15b5870eff84ea759ab87a7a3a2d49de1`; `fund_gld_defensive` `255c74fc9b3d901de1aa1418765aabcac6f995e62270cdc306dd1c07373a23e1`; `crypto` `3c0cfcd1e7fd61357e5507e23b460a3d63137b6b678815f194982588df683e31` under `intelligence/level1_sleeve_synthesis/profiles/` | XASSET-0012 (effective through PR #301) and XASSET-0013 (effective through PR #302); content merged through PR #303. Sealed historical synthesis, validated by `level1_sleeve_synthesis_validator.py`; no current-market inference unless separately refreshed. | `portfolio_function` DRIVER fields plus DISCLOSURES. Missing required function evidence yields `unable_to_determine`. Conflicting fields are not counted or reconciled. Evidence coverage, maturity, `sizing_readiness`, and capital eligibility may not imply size or preference. |
| Direct sleeve relationships: for this exact unordered pair, what function difference, duplication, or directly stated co-behavior is evidenced? | `equity_fund_broad_market` `8667974b8e08926173ffb9819e4418a06fe2731b0983883fab062e8a272ed0f8`; `equity_fund_gld_defensive` `5f5daa85f6aea16354fb8a6202df23747c39b57147a201debffdc37b67dbabed`; `crypto_equity` `54fa83d59e761536fa332ef3eb23f8a995a5f2ce3a99acb2034fb90042aa7e9e`; `crypto_fund_gld_defensive` `d939157d59d4d59fdab81d3d1a51900551dd6a69588c7198864c7608c33b8312` under `intelligence/level1_sleeve_synthesis/relationships/` | Same XASSET-0012/XASSET-0013 and PR #303 lifecycle as the profiles. Sealed direct-pair evidence only; a future application must revalidate the exact hash and may not treat it as a current market observation. | Direct function/duplication fields may be DRIVER input. A missing direct pair is handled only by §I; conflict yields `unable_to_determine`. `stronger_evidence_maturity`, `favored_sleeve_id`, readiness counts, and coverage counts are DISCLOSURE-only and may not imply preference. |
| Broad-market instrument economics: for a named fund, what directly evidenced cost and tracking characteristics apply? | SPY `3bd02ff4028830439573a78f2b2cbe6d92070615ca1907f5530de72dfec57cda`; VEA `b8c90454d98bbc445360f92562ff01bfee40e25e7c5f6bb004b5c95d259cc42c`; VWO `4f9986fb7eae9758b558d5f9d76325eb6469e82912ed0c2457d6c491ca10ac00` under `intelligence/instrument_economic_assessment/` | XASSET-0010 (effective through PR #295) and XASSET-0011 (effective through PR #296), with merged validated content on current main. Source-record freshness fields govern; stale or unavailable fields are excluded. | Instrument-specific DRIVER evidence only after a separately accepted sleeve-representation rule. Until then it is DISCLOSURE at Level 1; disagreement/missingness defeats aggregation. It may not be averaged, counted, or treated as sleeve valuation. |
| Crypto instrument economics: for a named coin, what directly evidenced historical path or inflation-sensitivity characterization applies? | BTC `99a2e2dabc40aa6cf8004b17807495390e1d65523efa9bd4d48fe9329f72d3c0`; ETH `830953dc1da2f74f30f77fc7ab6e518e59c77cc6612454554ba133010c6ba4b4`; SOL `b94b5785a661479ba6a9a8539dded3c180cf36703797263785e878e49f089734` under `intelligence/instrument_economic_assessment/` | Same XASSET-0010/XASSET-0011 lifecycle and source-owned freshness contract as the fund records. Historical observations do not become current forecasts. | Instrument-specific path/recovery DRIVER evidence only after an accepted representation rule; otherwise DISCLOSURE. Cross-coin disagreement or unavailability is preserved; no equal, market-cap, conviction, current-weight, or other aggregation is implied. |
| GLD function and economics: what directly evidenced defensive function, historical path, cost, or deployability applies to the GLD representation? | `intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml` `52dd76614fab7e3a6ac33b9da6486ea2d485b935a8ab633cef88ba323c9a9b5e`; `intelligence/economic_assessment/GLD.yaml` `055d3e9abd270122c7120bbfd474b61a2282d7c0fd7803b82fe8ec1edfce5406` | XASSET-0005 (effective through PR #273), XASSET-0008 (effective through PR #287), and XASSET-0009 (effective through PR #293), with content merged through PR #294. Source-owned status/freshness fields govern. | Direct function/path/cost/deployability fields may be DRIVER evidence; partial or conflicted fields propagate disclosure/`unable_to_determine`. They do not prove portfolio-level offset magnitude, a relationship to an untested pair, or a sleeve weight. |
| Overlap and co-behavior: what directly computed duplication or explicitly uncomputed relationship interface exists? | `etf_direct_equity_duplication` `aae8dcc80b9a55741910abacad90dbbb6c7e27f0cacbd339d17b49d7c34c7b77`; `issuer_overlap_etf_lookthrough` `246bc77aaf831db1478884eb3eea831d3a1731ecf281b0ca20e0616643f81c12`; `crypto_correlation_interface` `90553348b0f23f2f20caab718e10db5da979b2e86b36a144a666ca6831646108`; `defensive_offset_interface` `cf9cd500f2710c7280effde328a5b414e3620c7dcb213049b5ebd0c99a5b2316` | XASSET-0005 (PR #273) and XASSET-0007 (effective through PR #286), with content merged through PR #292. Exact snapshot status controls; an interface marked uncomputed is not evidence. | Computed direct duplication may be `diversification_cobehavior` DRIVER evidence. Point-in-time current weights are forbidden. Uncomputed interfaces are DISCLOSURES and cause missingness where their direct question is required; no proxy or transitive fill is allowed. |
| Equity valuation: what accepted company-level valuation evidence or partial exists, without answering a Level-1 aggregation question? | `intelligence/valuation_results/COHORT_MANIFEST.yaml` canonical content hash `5956a37d0de87def2e94a62a80c87956bb0fc7e6bcc674812a556d0eabc89d11` | VALUATION-0002/0005/0006/0007 (merged through PRs #276/#282/#288/#290) and their validators. Each company record's own freshness/partial state governs; stale or partial evidence stays visible. | DISCLOSURE at Level 1 until a separately accepted, non-current-weight, non-counting sleeve-aggregation rule exists. Missing or conflicting company evidence cannot be filled, averaged, or weighted into a sleeve signal. |
| RISK attempt-2: what does the accepted historical study say about uncertainty, representation sensitivity, path/recovery, and opportunity-cost robustness? | Exact identities in §G | RISK-0001/0002/0003/0004 and the exact accepted PR #316 lifecycle in §G. Its historical window is fixed; it is not refreshed into current market evidence. | Historical DRIVER evidence only for its directly measured questions and DISCLOSURE/precision gating otherwise. Any required governed null or family `unable_to_determine` propagates without reinterpretation. It may not become a target anchor, increment, weight, or automatic preference. |

This registry is closed for methodology v1.0. A future application authorization must freeze the exact
subset it will consume and may not silently add a source class.

### G. Accepted RISK lifecycle and evidence freeze

The exact admissible RISK lifecycle identity is:

- repository/PR: `Mast3rkey/Portfolio-HQ` PR #316;
- accepted RESULTS head: `1bf550c5ca5278ff0cbedc498decbf760bb4c8a0`;
- independent full RESULTS review: `4942378204`;
- principal exact-head acceptance: `5299933404`;
- merge: `a13d9b5053ab3fce74e577ab6efcd930ee3910fd`;
- post-merge verification: `5299981108`;
- merge-commit CI: `31857856905`, successful;
- attempt: `RISK-0001-EXECUTION-ATTEMPT-002`, authority `CONSUMED`, no retry or third attempt;
- accounting: 777 registered / 609 executed / 168 governed null-ineligible; and
- family dispositions: `EQUITY`, `FUND_BROAD_MARKET`, `FUND_GLD_DEFENSIVE`, and `CRYPTO` each exactly
  `unable_to_determine`.

The exact protocol and preregistration identities are:

| Artifact | SHA-256 |
|---|---|
| `research/level1_sleeve_robustness/PROTOCOL_V1.md` | `90277ad4767e4766d7a38c1199affde66f44e55ff16fd7f73e0894380cf8a425` |
| `research/level1_sleeve_robustness/pre_registration.yaml` | `8da1697456e8a8f4a168c99ae8387c77cd023e0e615cf51c78110165223d3c5a` |
| `research/level1_sleeve_robustness/implementation_config.yaml` | `9f97162260ca97ef340b56811d8d91009235922cddf478ff39be7270614301de` |
| `research/level1_sleeve_robustness/eligibility_matrix.json` | `3854e9203c6b282e3d7c398b19a8f35de6cdad1c291b06456af19fa4d47ed680` |
| `research/level1_sleeve_robustness/trial_registry.json` | `8942227dfba3a4fff6b1b94067ad252f0890cfa0959e2939e25ef98036904f51` |

The accepted result/report package is frozen at:

| Artifact | SHA-256 |
|---|---|
| attempt-2 independent approval receipt | `ec9dd6aeb4b8f5751ea8679c700723203b20777e89623b52882508a0a144b2cd` |
| `results/execution_receipt.json` | `9d72f2b461e7834d24b3cadac0ebd5572e10c89519ae863b4ec7cc241158ac24` |
| `results/raw_evidence.json` | `eae2f5e54950efbe5fe97016d688b09529507c915658fed020e94568171c1cbc` |
| `results/cell_results.json` | `c5f6d8b0f24dee69ca0c398a42071ddbec04eddb0baeef014f6fb89932111b61` |
| `results/disposition.json` | `364a324c6dad68d84ee5126600e2caef6ac6d3253c739e6ed55773325107e5d5` |
| `results/diagnostics.json` | `f1c5d08fdebb368472c5e07a4c485d3c8356ed3c7116737dc6ba348d17ce5b04` |
| `results/RESULTS.md` | `2a6b814e8df578bbc30c4bf2c40e05815df48cf0d1c2308630b7f7042ff207bc` |
| `results/LIMITATIONS_AND_SURVIVORSHIP.md` | `28eb4796d371ffb527845b8539b5cbb14493a191452b2f37bca4956a21971deb` |
| `results/RESULTS_DISCLOSURE_SUPPLEMENT.md` | `8013f376a0ad08bbbdffe7e6481d8d3e40b993b98515f6f3a9b7c445d49ded45` |

`unable_to_determine` remains exactly that. The family traces may constrain precision or require
abstention; they may not be recoded as neutral, non-rejection, a directional lean, or an anchor.

### H. Six-pair marginal-capital contract

Exactly six unordered pair records exist, in this canonical order:

1. `equity__fund_broad_market`;
2. `equity__fund_gld_defensive`;
3. `equity__crypto`;
4. `fund_broad_market__fund_gld_defensive`;
5. `fund_broad_market__crypto`; and
6. `fund_gld_defensive__crypto`.

The first named sleeve is `self`; the second is `counterpart`. Reversed or duplicate records are
invalid. A sleeve-centric view mechanically inverts direction when the sleeve is the counterpart; it
does not create a seventh record.

Every pair record must explicitly contain:

- direct evidence available, by exact hash;
- all six driver categories considered, each with `applicable`, `not_applicable`, or missing state;
- direction per applicable driver: `self_preferred`, `counterpart_preferred`, `indistinguishable`, or
  `unable_to_determine`;
- missing, conflicting, stale, and representation-sensitive evidence;
- every applicable constraint and its clipping/blocking effect; and
- one pair conclusion using the same four-value vocabulary.

The pair conclusion is deterministic:

| Condition | Conclusion |
|---|---|
| At least one applicable determinate driver favors self; every other applicable driver favors self or is indistinguishable; no driver is missing, stale, conflicted, or unable; no representation gate fails | `self_preferred` |
| Mirror image of the prior row | `counterpart_preferred` |
| At least one driver is applicable; every applicable driver is `indistinguishable`; none is missing, stale, conflicted, or unable | `indistinguishable` |
| Any contrary directions, required missingness, staleness, conflict, failed representation gate, or other unclosed state | `unable_to_determine` |

This is a unanimity/no-veto table, not a win count. Driver quantity, source count, evidence maturity,
or the number of favorable statements never decides the conclusion.

Each of the four sleeves must also be compared directly with `UNSIZED_UNASSIGNED_CAPITAL`. The closed
conclusions are `sleeve_preferred`, `unassigned_preserved`, `indistinguishable`, and
`unable_to_determine`. `sleeve_preferred` requires a lawful, positive, evidence-bounded exposure and
no blocking constraint. If assignment needs a missing parameter, proxy, plug, or unsupported pair
inference, the result is `unassigned_preserved` or `unable_to_determine`, never automatic deployment.

### I. Missing-direct-pair and non-transitivity rule

The current accepted non-RISK relationship corpus contains no direct
`fund_broad_market` ↔ `fund_gld_defensive` record and no direct
`fund_broad_market` ↔ `crypto` record. Their absence is not neutral evidence and may not be filled by
transitivity through equity or another sleeve.

For any missing direct pair, a future application must record the pair conclusion as
`unable_to_determine`. A sleeve range may still survive that missing pair only when both endpoints are
independently and directly governed and remain valid under every possible direction of the unresolved
pair. That is a non-inferential intersection of already-authorized bounds, not a derived relationship.
If this condition is not met, the affected sleeve outcome is abstention. A missing pair never blocks
filing this methodology and never licenses a proxy relationship.

### J. Point, range, and abstention contract

#### J.1 POINT

A provisional point is permitted only when all of the following hold:

1. every required item is admitted and current enough under its own authority;
2. every consequential conflict resolves under GOV-0002 and the closed tables here;
3. all pairwise comparisons bearing on the sleeve are determinate and none leaves unresolved precision;
4. representation sensitivity does not defeat point precision;
5. the sleeve-versus-unassigned comparison is `sleeve_preferred`;
6. one exact numeric value is uniquely stated by admitted authority or uniquely mathematically derived
   with complete NUM-0001 coverage;
7. no current-weight, midpoint, historical target, proxy, or plug enters the derivation; and
8. exact portfolio reconciliation holds.

If more than one lawful value remains, a point is prohibited.

#### J.2 RANGE

A provisional range is permitted only when:

- admitted evidence supports nonzero but bounded exposure and does not uniquely support a point;
- both endpoints are separately traceable to exact accepted evidence or an exact mathematical
  consequence of such evidence;
- unresolved pair evidence cannot invalidate either endpoint under §I;
- representation sensitivity is contained within, rather than concealed by, the bounds;
- every endpoint parameter has complete NUM-0001 authority; and
- exact set-valued reconciliation under §K is feasible.

No historical target, old midpoint, current weight, minimum range width, symmetry convention, or
default midpoint may create an endpoint. A range stays a range; no midpoint is selected automatically.

#### J.3 ABSTENTION

Abstention is mandatory when any of the following applies:

- required evidence is missing, unaccepted, hash-mismatched, or stale beyond its own rule;
- direct evidence is materially conflicted;
- representation sensitivity defeats lawful point or range bounds;
- a required pair remains unsupported and §I cannot preserve independently governed bounds;
- a consequential parameter lacks NUM-0001 authority;
- reconciliation would require a hidden plug, proxy, prior, or redistribution;
- a constraint or Level-2 dependency cannot be applied without substantive discretion; or
- repeated derivation from the same frozen inputs is not byte-identical.

Abstention is a complete governed outcome, not a defect to be patched with an assumption.

### K. Unassigned capital and exact reconciliation

For an exact point vector, reconciliation is the identity:

`UNSIZED_UNASSIGNED_CAPITAL = normalized_asset_unit - separately_governed_liquidity_asset - sum(admitted_sleeve_points)`.

For ranges, the authoritative output is the exact feasible set of sleeve vectors inside the admitted
endpoints. For every vector `x` in that set, unassigned capital is the exact complement
`1 - separately_governed_liquidity_asset - sum(x)`. The method does not choose a vector, midpoint, or
optimized combination. A negative complement invalidates the candidate and forces abstention.

If no separate liquidity-asset value has been lawfully resolved, none is invented; unsupported capital
remains unassigned. Constraint clipping increases unassigned capital by the exact clipped amount. It
does not alter any other sleeve.

`UNSIZED_UNASSIGNED_CAPITAL` may not automatically flow to cash, reserve, debt reduction, a benchmark,
a broad-market fund, pro-rata redistribution, another sleeve, or any zero-return/risk proxy. It carries
its own rationale, review trigger, and `deployment_status: prohibited_without_future_governance`.

### L. NUM-0001 inventory and parameter-elimination decisions

| Item | NUM-0001 treatment | Canonical source / basis | Binding and stale/unavailable behavior |
|---|---|---|---|
| One normalized asset unit / whole 100% state | Mathematically derived normalization; contextual representation, not an economic parameter | XASSET-0019 asset-state reconciliation and §C | Binding denominator convention; never a target. |
| Four sleeves | Mathematical count from the closed ontology | XASSET-0019 and §B | Binding until ontology amendment. |
| Six unordered pairs | Mathematical derivation `4 choose 2` | §H | Binding; any missing/duplicate/reversed pair invalidates application. |
| Canonical pair and sleeve orders | Engineering/procedural constant over the closed ontology | §§B/H | Binding for determinism; no economic effect. |
| Pair-winner threshold | Eliminated | Unanimity/no-veto table in §H | No numeric threshold exists. |
| Evidence-conflict score or confidence percentage | Eliminated | Fail-closed categorical conflict rule | Conflict yields `unable_to_determine`. |
| Minimum range width / midpoint rule | Eliminated | Direct endpoint provenance in §J | No width or midpoint parameter exists. |
| Evidence-maturity weight / freshness penalty | Eliminated | E/F prohibitions | Maturity is disclosure-only; stale evidence is excluded, not discounted. |
| Endpoint value | Not chosen here; must be externally imposed, mathematically derived, empirically calibrated, evidence-bounded governance selection, or provisional guardrail under a later exact record | Exact future application authority | If no justified number exists, abstain. |
| Output precision and rounding | No new precision selected | Preserve exact source precision or exact rational derivation | If arithmetic would require an ungoverned rounding choice, abstain and seek separate authority. Human display rounding is non-authoritative and may not change canonical values. |
| Reconciliation mechanics | Mathematically derived exact identity | §K | Binding; any mismatch invalidates output. |
| Freshness/currentness threshold | Source-owned; no universal number | Each admitted source's effective authority | Missing source-owned rule makes the item disclosure-only unless separately governed. |

No consequential numeric parameter is introduced for convenience. Any future numeric endpoint or
precision rule must state class, canonical source, evidence basis, scope, binding status, precision,
stale/unavailable behavior, and reopen trigger exactly as NUM-0001 requires.

### M. Formula, score, optimizer, and legacy-anchor prohibitions

The only authorized arithmetic is exact normalization, direct source-prescribed derivation,
constraint clipping, bound intersection, and reconciliation. Explicitly prohibited:

- weighted or composite scores;
- confidence percentages;
- pairwise win tallies;
- hidden utilities or preference functions;
- optimizer, solver, grid search, sweep, or best-weight selection;
- averaging incomparable metrics or representations;
- evidence-maturity weights, source-count advantage, or freshness penalties;
- current-weight or incumbency priors; and
- post-hoc rounding or plugs that alter economic meaning.

The following are contamination evidence only and mechanically barred from future input authority:
the old six-way equal baseline; historical `18.67 / 14.67 / 16.67 / 16.67` sleeve outputs; historical
`33.32` residual; R2/R3 counts or directions; the fixed adjustment increment; XASSET-0016's formula
or outputs; XASSET-0018's historical sizing outputs and `numeric_sizing/` records; policy-adoption
`sizing_readiness` or capital-eligibility states as economic evidence; current targets, holdings,
weights, tiers, gates, margin buying power, leverage, buffer, charts, technicals, validation maturity,
evidence counts, and residual-as-cash logic.

Historical records may be read solely to identify and reject contamination. Their validator success
proves historical computational conformance, not current economic validity.

### N. Level-2, liquidity, and debt boundaries

LEVEL2-0001 is a research-cohort freeze only. This method does not choose final members, treat cohort
inclusion as membership, size instruments, or assign internal sleeve weights. Instrument-level evidence
may be admitted only through an accepted sleeve-representation rule; absent that rule it remains
disclosure or causes abstention.

This decision does not determine operational cash, strategic cash, a reserve target, a liquidity amount,
debt reduction, margin deployment, repayment, leverage, or buffer policy. Liquidity may enter only as a
separately accepted constraint/disclosure or later governed `LIQUIDITY_ASSET`. Debt reduction remains a
separate liability-flow control and never enters the denominator.

### O. Closed future application schema

A future application record must use a recursively closed structured schema containing at least:

```
methodology_identity:
  decision_id
  accepted_head
  decision_file_sha256
  schema_version
application_identity:
  authorization_decision
  exact_head
  frozen_at
normalized_asset_state:
  denominator_identity
  separately_governed_liquidity_state
  debt_excluded
evidence_snapshot[]:
  evidence_id
  path
  sha256
  governing_authority
  authority_lifecycle
  permitted_question
  classification
  freshness_state
  representation_scope
  forbidden_implications[]
sleeves[exactly_four]:
  sleeve_id
  admitted_drivers[]
  applicable_constraints[]
  disclosures[]
  representation_sensitivity
  uncertainty_state
  sleeve_vs_unassigned
  conflict_missingness_state
  outcome_type
  point_or_range_or_null
  deterministic_derivation_trace[]
pairs[exactly_six]:
  canonical_pair_id
  self_sleeve
  counterpart_sleeve
  direct_evidence[]
  driver_ledger[exactly_six_driver_classes]
  missing_conflicting_stale_evidence[]
  constraint_effects[]
  conclusion
portfolio_reconciliation:
  exact_feasible_set_or_point
  unsized_unassigned_capital
  constraint_clipping_to_unassigned
  reconciliation_identity
reopen_triggers[]
authority_boundary:
  provisional_not_adopted
  no_policy_effect
  no_level2_effect
  no_liquidity_or_debt_effect
```

No real record is populated by this filing. Natural-language explanation may accompany the closed
record only as derived, non-authoritative material pinned to the authoritative record hash.

### P. Later application authorization is not bundled

This decision does **not** authorize a later application PR. Bundling would be lawful only if source
population, exact hashes, question-to-driver mappings, pair evidence, conflict/missingness handling,
endpoint derivation, every consequential parameter, precision/rounding, reconciliation, and the closed
application schema left no substantive application-time judgment.

That bar is not met. Current evidence contains two missing direct pairs, uncomputed co-behavior
interfaces, representation disagreement, all four accepted RISK dispositions at
`unable_to_determine`, no accepted Level-1 aggregation rule for company valuations, and no governed
numeric endpoint/precision authority. A later application would therefore need substantive judgments
about its refreshed source population and any new direct evidence before it could do more than record
abstention. A separate future Lane G authorization must freeze those choices. Speed is not a basis for
bundling them here.

### Q. Validator and adversarial contract

Any future authorized implementation/application must mechanically enforce:

1. exactly four sleeves and exactly six unordered pairs;
2. no duplicate, reversed, missing, or extra pair;
3. exact evidence paths, hashes, governing authorities, and source-owned freshness states;
4. the exact accepted RISK lifecycle and all frozen package hashes in §G;
5. no legacy anchor, current target, current holding, current weight, or incumbency prior;
6. no composite score, confidence percentage, tally, utility, optimizer, or hidden weighting;
7. no automatic midpoint, proxy, plug, or redistribution;
8. preservation of `UNSIZED_UNASSIGNED_CAPITAL`;
9. no liquidity fifth-sleeve or debt-denominator leakage;
10. no Level-2 membership, instrument sizing, or research-cohort-to-membership leakage;
11. no policy-adoption, allocation-check, deployment, chart, ladder, margin, trade, or order language;
12. complete NUM-0001 coverage for every consequential numeric/procedural parameter;
13. byte-identical repeated derivation from the same frozen inputs and exact reconciliation;
14. partial, conflict, missingness, staleness, abstention, and representation-sensitivity propagation;
15. missing direct-pair behavior and zero transitive inference;
16. constraint clipping to unassigned without positive preference or redistribution; and
17. protected-path byte identity.

Required adversarial fixtures must include: a hidden current-weight prior; midpoint default; residual
as cash; pro-rata redistribution; “confidence” used as a score; transitive pair inference; missing
evidence treated as neutral; a constraint treated as preference; stale evidence silently admitted;
Level-2 member leakage; cash or debt as a fifth sleeve; policy language; a reversed pair; duplicate
pair; hash drift; RISK identity drift; unsupported precision; and nondeterministic repeated output.

### R. Reopen triggers

Methodology review is required when any of these occurs:

- controlling constitutional or accepted governance authority changes;
- a new accepted evidence class materially changes an admissible question;
- liquidity architecture changes denominator or reconciliation mechanics;
- the Level-2 architecture changes a boundary relied on here;
- a required parameter proves unsupported or a source-owned freshness rule is unavailable;
- a validator exposes nondeterminism, incomplete closure, or hidden arithmetic;
- application requires discretion not closed by this decision;
- a direct-pair source is added, removed, materially changed, or contradicted; or
- the closed ontology changes.

Reopening methodology does not automatically change a point, range, target, membership, policy, or
portfolio configuration.

### S. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files:

1. this decision;
2. `governance/decisions.yaml` — one catalog row;
3. `operations/WORKSTREAMS.yaml` — additive WS-0014 lifecycle facts and active-lane fields; and
4. `test_portfolio_hq_dashboard_decisions.py` — the two mechanical catalog-count assertions.

No supporting audit is necessary because this decision contains the complete methodology and exact
RISK/source freeze. No `CLAUDE.md`, Intelligence, research result, production, configuration, allocator,
or protected portfolio file belongs in this PR.

WS-0014 must record additively that PR #316 is accepted and merged, the RISK results lifecycle is
complete, results are research evidence only, XASSET-0020 is the active next unit, and actual Level-1
sizing/application remains downstream and unperformed. Liquidity, Level 2, whole-portfolio stress,
charts, ladders, and margin remain downstream. Historical gate text remains byte-unchanged.

### T. Absolute non-authorization

This decision produces and authorizes no real sleeve point, range, weight, target, membership,
allocation, Level-2 selection or sizing, current-portfolio analysis, liquidity target, cash target,
debt target, margin/leverage rule, chart, ladder, deployment, trade, order, backtest, optimizer, policy
adoption, `targets.yaml`/`holdings.yaml`/`gates.yaml` mutation, allocator change, or brokerage action.

## Rationale

A deterministic economic sizing method cannot begin from inherited percentages or research-count
advantage. It must compare each marginal use of capital directly, preserve conflicts and missingness,
and refuse precision the evidence cannot support. Separating drivers, constraints, and disclosures
prevents a safety boundary or evidence-quality label from secretly becoming return preference.
Preserving unassigned capital makes abstention operationally honest without disguising it as cash.

## Alternatives Considered

**Reuse the historical schema-2.0 method with new labels.** Rejected: XASSET-0019 removed its future
economic authority, and relabeling the same baseline/increment would not answer the marginal-capital
question.

**Aggregate evidence into one confidence or utility score.** Rejected: incomparable evidence would be
silently weighted, missingness could look neutral, and the result would be unauditable.

**Infer the two missing broad-market pairs through equity.** Rejected: transitivity is not direct
evidence and could conceal vehicle-specific function, cost, or co-behavior differences.

**Bundle one application authorization.** Rejected for the reasons in §P: substantive source,
representation, pair, endpoint, and precision judgment remains.

**Force four sleeves to exhaust the denominator.** Rejected: unresolved liquidity and unsupported
capital would be silently assigned, recreating the plug defect XASSET-0019 prohibited.

## Consequences

After this decision becomes effective, a future governance unit may propose a bounded application only
by freezing question-matched evidence and closing every remaining application-time judgment. The method
can lawfully return points, ranges, or abstentions, but it creates none here. Existing portfolio policy,
configuration, Level-2 research cohort, RISK results, liquidity/debt architecture, and manual execution
model remain unchanged.
