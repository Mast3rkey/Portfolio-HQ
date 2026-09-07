---
decision_id: XASSET-0021
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0005, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, XASSET-0013, XASSET-0019, XASSET-0020, LEVEL2-0001, VALUATION-0002, VALUATION-0005, VALUATION-0006, VALUATION-0007, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0021-level1-economic-sizing-application-prerequisite-closure.md
---

## Context

Effective XASSET-0020 supplies a replacement Level-1 economic sizing methodology but deliberately
withholds application authority. It identifies open application-time choices involving evidence
population, the two absent direct pairs, representation sensitivity, endpoint provenance,
precision, conflict handling, freshness, liquidity, unassigned capital, and the accepted RISK
uncertainty states. Leaving any of those choices to an application author would permit the author to
create allocation meaning that the methodology itself did not authorize.

This decision classifies every such choice. It closes the economic choices deterministically or by
mandatory abstention, and it identifies the application artifact schema and deterministic generation
contract as two unresolved mechanical prerequisites that may not be originated during application.
It does not apply XASSET-0020, populate an application record, produce a sleeve point or range, choose
any target or weight, resolve liquidity, select a Level-2 instrument, or adopt portfolio policy.

## Decision

### A. Lifecycle, controlling identity, and scope

This is an OPS-0009 Lane G filing. While its pull request is open it is proposed prerequisite
governance only. It becomes effective only after independent full exact-head review, principal
exact-head acceptance, merge, immediate post-merge verification, and successful exact-head CI.
The author may commit, push, and open the draft PR but may not self-review, principal-accept, mark
ready, or merge.

The prerequisite methodology is exactly:

- decision: `XASSET-0020`;
- accepted methodology head: `d2c0ce84f1922bc606c3de6983eb47266dbe4d72`;
- decision-file SHA-256:
  `f04ee116b7ed93165f621f65d91594557c5e4e3d0744d5f87ddfea5ccba999d2`;
- independent full exact-head review: `4943427551`;
- principal exact-head acceptance: `5301699393`;
- merge commit: `e7d66d93b5f7ab2ecd985a7a4bf680a118df6b0e`;
- post-merge verification: `5301728726`; and
- merge-commit CI: run `31878188273`, successful.

Any mismatch in that identity makes the future application ineligible. No other methodology, old
Level-1 output, or historical numeric record may be substituted.

The only investable sleeves remain, in canonical order, `equity`, `fund_broad_market`,
`fund_gld_defensive`, and `crypto`. `LIQUIDITY_ASSET`, `LIQUIDITY_CONSTRAINT`,
`LIABILITY_FLOW_CONTROL`, and `UNSIZED_UNASSIGNED_CAPITAL` retain XASSET-0019/XASSET-0020's separate
types and may not become additional sleeves.

### B. Closure vocabulary and authorization test

Every substantive application-time issue is classified as exactly one of:

- `CLOSED_DETERMINISTICALLY` — the application has one mechanical treatment;
- `APPLICATION_MUST_ABSTAIN` — the issue is unresolved economically, but the application has one
  mechanical response: preserve the governed uncertainty and abstain; or
- `SEPARATE_PREREQUISITE_REQUIRED` — no application is authorized until the named prerequisite is
  separately accepted.

Application authority exists only when every substantive row in §N is either
`CLOSED_DETERMINISTICALLY` or `APPLICATION_MUST_ABSTAIN`. A single
`SEPARATE_PREREQUISITE_REQUIRED` row withholds authority. Speed, portfolio need, reviewer preference,
or a desire to avoid an all-abstention result cannot change this test.

### C. Exact evidence snapshot

#### C.1 Snapshot rules

The future application may consume only the rows in §§C.2-C.3. Each identity is the exact canonical
repository path and whole-file SHA-256 at XASSET-0020's accepted/effective main tree. The source-owned
`content_sha256` is additionally recorded where the schema supplies it. A whole-file hash mismatch,
content-hash mismatch, missing path, governing-authority failure, or validator failure is not corrected
inside the application: the item is excluded and any required question propagates
`unable_to_determine`.

The snapshot is historical and immutable. Its freezing does not make a historical observation
current. The future application may not silently add a later file, refreshed observation, new source
class, current holding, current target, or current weight. A changed source requires a separate future
authorization to replace or extend this snapshot.

Accepted/effective lifecycle identity is fixed by source class exactly as XASSET-0020 §F.2 records:

- profiles and direct relationships: XASSET-0012 effective through PR #301, XASSET-0013 effective
  through PR #302, content merged through PR #303;
- broad-market and crypto instrument economics: XASSET-0010 effective through PR #295 and
  XASSET-0011 effective through PR #296, with their validated content merged on the frozen tree;
- GLD function/economics: XASSET-0005 through PR #273, XASSET-0008 through PR #287,
  XASSET-0009 through PR #293, content through PR #294;
- overlap/co-behavior: XASSET-0005 through PR #273, XASSET-0007 through PR #286, content through
  PR #292;
- equity valuation: VALUATION-0002/0005/0006/0007 through PRs #276/#282/#288/#290; and
- RISK: the exact PR #316 lifecycle in §C.3.

No stale frontmatter vocabulary defeats those accepted/effective lifecycles. A future application
must store the applicable lifecycle identity on every item rather than merely naming a decision ID.

#### C.2 Non-RISK snapshot

| Evidence ID | Canonical path | Whole-file SHA-256 | Source content SHA-256 / deterministic identity | Application classification and currentness state |
|---|---|---|---|---|
| `PROFILE_EQUITY` | `intelligence/level1_sleeve_synthesis/profiles/equity.yaml` | `edf3cce04b2f63bed97975ba8dd04313d5bd0a6e4c06b165987580e3f47f4796` | `1f44f44369a4c1fe9ea824d99e82539d96f9ccf6407a740ef93d182a8b64bedc` | Accepted sealed historical profile under XASSET-0012/0013; no source-owned current-market rule; DISCLOSURE only for current preference. |
| `PROFILE_FUND_BROAD_MARKET` | `intelligence/level1_sleeve_synthesis/profiles/fund_broad_market.yaml` | `a2657187141f4dbeaa9f1a583192c74071eb530985a194fedb9c69a72d10f194` | `2ed99d67847a9aea644be6867c53cac15b5870eff84ea759ab87a7a3a2d49de1` | Same treatment; disclosed partial evidence preserved. |
| `PROFILE_FUND_GLD_DEFENSIVE` | `intelligence/level1_sleeve_synthesis/profiles/fund_gld_defensive.yaml` | `f7474115e8e9303fa07c2b7b0db589a855c4a386c50bf4a06dec8e57b3aada01` | `255c74fc9b3d901de1aa1418765aabcac6f995e62270cdc306dd1c07373a23e1` | Same treatment; forced assessment gap preserved. |
| `PROFILE_CRYPTO` | `intelligence/level1_sleeve_synthesis/profiles/crypto.yaml` | `3677dacfc0956450cd83da8537d85cc3e03c0860156c59b557d0bbbe10dad4a1` | `3c0cfcd1e7fd61357e5507e23b460a3d63137b6b678815f194982588df683e31` | Same treatment; cross-coin missingness and SOL abstention preserved. |
| `REL_EQUITY_FUND_BROAD_MARKET` | `intelligence/level1_sleeve_synthesis/relationships/equity_fund_broad_market.yaml` | `c54b24f4f8cf793043df0b76628a55905a2e63949f70a02578573183b3ba331c` | `8667974b8e08926173ffb9819e4418a06fe2731b0983883fab062e8a272ed0f8` | Accepted sealed direct-pair historical evidence. `primary_disposition`, `favored_sleeve_id`, maturity, and coverage are DISCLOSURE-only and never direction. Current direct holdings/weights are forbidden. |
| `REL_EQUITY_FUND_GLD_DEFENSIVE` | `intelligence/level1_sleeve_synthesis/relationships/equity_fund_gld_defensive.yaml` | `7af1e3f98d81cf86e70fbd175df615f700a019fa3f27fd70c969d417e0abf390` | `5f5daa85f6aea16354fb8a6202df23747c39b57147a201debffdc37b67dbabed` | Accepted historical role disclosure; it supplies no marginal-dollar endpoint or preference. |
| `REL_CRYPTO_EQUITY` | `intelligence/level1_sleeve_synthesis/relationships/crypto_equity.yaml` | `673d45e6c60ee1f133a8c006975be62ce8f5a73d9d241be9391c2c6f4332c70e` | `54fa83d59e761536fa332ef3eb23f8a995a5f2ce3a99acb2034fb90042aa7e9e` | Accepted historical evidence; maturity preference is forbidden and no remaining current directional driver is supplied. |
| `REL_CRYPTO_FUND_GLD_DEFENSIVE` | `intelligence/level1_sleeve_synthesis/relationships/crypto_fund_gld_defensive.yaml` | `bbe09701f46211007d5574efc93fb70a8c7d0f83bd6c29cecc51d4721d0f447b` | `d939157d59d4d59fdab81d3d1a51900551dd6a69588c7198864c7608c33b8312` | Accepted historical coexistence/mixed-representation disclosure; not a current preference or endpoint. |
| `ETF_ECON_SPY` | `intelligence/instrument_economic_assessment/SPY.yaml` | `b5ce51c220d6b16d67efa6253dbd2d53108f9c522899ef63316a93388b4a5221` | `3bd02ff4028830439573a78f2b2cbe6d92070615ca1907f5530de72dfec57cda` | Accepted sealed instrument evidence under XASSET-0010/0011; no accepted sleeve-representation aggregation and no governed currentness rule; DISCLOSURE only at Level 1. |
| `ETF_ECON_VEA` | `intelligence/instrument_economic_assessment/VEA.yaml` | `d4f9bb5a1b103c51b3ddda2e533c0ea3e4d16e1e5c83a075894b9e19e9750da1` | `b8c90454d98bbc445360f92562ff01bfee40e25e7c5f6bb004b5c95d259cc42c` | Same treatment. |
| `ETF_ECON_VWO` | `intelligence/instrument_economic_assessment/VWO.yaml` | `470234f9a0e68c59cb873ad87ada902763f3460663853559a1bb1edd5fd4fb03` | `4f9986fb7eae9758b558d5f9d76325eb6469e82912ed0c2457d6c491ca10ac00` | Same treatment; accepted RISK known-gap state remains visible. |
| `CRYPTO_ECON_BTC` | `intelligence/instrument_economic_assessment/BTC.yaml` | `617924326be8c1f5459174fd2b81ce2eff89d45d87e7315ce2651f9c9a42ca0b` | `99a2e2dabc40aa6cf8004b17807495390e1d65523efa9bd4d48fe9329f72d3c0` | Accepted sealed single-instrument historical evidence; no accepted cross-coin aggregation/currentness rule; DISCLOSURE only at Level 1. |
| `CRYPTO_ECON_ETH` | `intelligence/instrument_economic_assessment/ETH.yaml` | `2261fb6c0c8684226950d0b13c152373068c326434050f06963e4736765fe0d2` | `830953dc1da2f74f30f77fc7ab6e518e59c77cc6612454554ba133010c6ba4b4` | Same treatment. |
| `CRYPTO_ECON_SOL` | `intelligence/instrument_economic_assessment/SOL.yaml` | `74d423e3e3626f80fd2c8a5684fb6836ec610967251854eb9040b8f36d51c309` | `b94b5785a661479ba6a9a8539dded3c180cf36703797263785e878e49f089734` | Same treatment; its own drawdown abstention remains binding. |
| `GLD_FUNCTION` | `intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml` | `cf391b226c8d08bca55216bdb094bcf99d57f8ad6b8f4b4d55e3c7797f2f483d` | `52dd76614fab7e3a6ac33b9da6486ea2d485b935a8ab633cef88ba323c9a9b5e` | Accepted sealed function evidence. Its source-owned hash-pin currentness is `current` at the snapshot; it may establish the existence of a defensive function but cannot establish relative preference or an endpoint. |
| `GLD_ECON` | `intelligence/economic_assessment/GLD.yaml` | `e75577cd546bb906cddf49a24d80c2e48637ab6939c86a2002c95f1931121991` | `055d3e9abd270122c7120bbfd474b61a2282d7c0fd7803b82fe8ec1edfce5406` | Accepted sealed historical, partial evidence under XASSET-0008/0009; no governed currentness rule; DISCLOSURE only for current preference. |
| `OVERLAP_ETF_DIRECT` | `intelligence/overlap_model/etf_direct_equity_duplication.yaml` | `79de4b36224301befe86a24664604ed72f9a11e810714e6e06faffb099b13a9f` | `aae8dcc80b9a55741910abacad90dbbb6c7e27f0cacbd339d17b49d7c34c7b77` | Accepted historical categorical rollup. Because application may not read current holdings/weights and the source requires drift re-check, it is DISCLOSURE only. |
| `OVERLAP_ISSUER_LOOKTHROUGH` | `intelligence/overlap_model/issuer_overlap_etf_lookthrough.yaml` | `e0255956d0bdb4e4704a8c007d2435a08bd4f093ecf95a8fec17f485afdcd1fc` | `246bc77aaf831db1478884eb3eea831d3a1731ecf281b0ca20e0616643f81c12` | Accepted point-in-time rollup with source-owned quarterly review requirement. Current weights are prohibited; the retained snapshot and freshness warning are DISCLOSURE only. |
| `OVERLAP_CRYPTO_INTERFACE` | `intelligence/overlap_model/crypto_correlation_interface.yaml` | `d55527be57f7d8ba4641d578aeecb69b383219171e7199e01b33c635f8535591` | `90553348b0f23f2f20caab718e10db5da979b2e86b36a144a666ca6831646108` | Accepted interface whose state is `not_yet_computable_interface_only`; it is missing evidence, not a driver. |
| `OVERLAP_DEFENSIVE_INTERFACE` | `intelligence/overlap_model/defensive_offset_interface.yaml` | `55992b329ef5617be374ccf873c85f2338ce9355b249b26a3a1522a65c1e0ad4` | `cf9cd500f2710c7280effde328a5b414e3620c7dcb213049b5ebd0c99a5b2316` | Same treatment; no portfolio-level defensive offset may be inferred. |
| `EQUITY_VALUATION_MANIFEST` | `intelligence/valuation_results/COHORT_MANIFEST.yaml` | `2f402e3c20b4ecc83d30cae2eb389c82ccba4c2a5ebf1a0d00e8cb15cf8be85f` | Manifest content identity `5956a37d0de87def2e94a62a80c87956bb0fc7e6bcc674812a556d0eabc89d11` | Accepted company-level results. Per-record freshness/partial states remain source-owned, but no accepted Level-1 aggregation rule exists; DISCLOSURE only. |

The two absent relationship files are not snapshot omissions. No accepted direct record exists for
`fund_broad_market__fund_gld_defensive` or `fund_broad_market__crypto`; their absence is the governed
missingness state in §D.

#### C.3 Accepted RISK snapshot

The only RISK evidence is `RISK-0001-EXECUTION-ATTEMPT-002`, accepted through RISK-0001/0002/0003/0004
and PR #316. Its accepted RESULTS head is
`1bf550c5ca5278ff0cbedc498decbf760bb4c8a0`; independent full RESULTS review `4942378204`;
principal exact-head acceptance `5299933404`; merge
`a13d9b5053ab3fce74e577ab6efcd930ee3910fd`; post-merge verification `5299981108`; and successful
merge-commit CI run `31857856905`. Attempt authority is `CONSUMED`; no retry or third attempt exists.

The exact admitted files and SHA-256 identities are:

| Canonical path | SHA-256 |
|---|---|
| `research/level1_sleeve_robustness/PROTOCOL_V1.md` | `90277ad4767e4766d7a38c1199affde66f44e55ff16fd7f73e0894380cf8a425` |
| `research/level1_sleeve_robustness/pre_registration.yaml` | `8da1697456e8a8f4a168c99ae8387c77cd023e0e615cf51c78110165223d3c5a` |
| `research/level1_sleeve_robustness/implementation_config.yaml` | `9f97162260ca97ef340b56811d8d91009235922cddf478ff39be7270614301de` |
| `research/level1_sleeve_robustness/eligibility_matrix.json` | `3854e9203c6b282e3d7c398b19a8f35de6cdad1c291b06456af19fa4d47ed680` |
| `research/level1_sleeve_robustness/trial_registry.json` | `8942227dfba3a4fff6b1b94067ad252f0890cfa0959e2939e25ef98036904f51` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/independent_preexecution_review.json` | `ec9dd6aeb4b8f5751ea8679c700723203b20777e89623b52882508a0a144b2cd` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/execution_receipt.json` | `9d72f2b461e7834d24b3cadac0ebd5572e10c89519ae863b4ec7cc241158ac24` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/raw_evidence.json` | `eae2f5e54950efbe5fe97016d688b09529507c915658fed020e94568171c1cbc` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/cell_results.json` | `c5f6d8b0f24dee69ca0c398a42071ddbec04eddb0baeef014f6fb89932111b61` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/disposition.json` | `364a324c6dad68d84ee5126600e2caef6ac6d3253c739e6ed55773325107e5d5` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/diagnostics.json` | `f1c5d08fdebb368472c5e07a4c485d3c8356ed3c7116737dc6ba348d17ce5b04` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/RESULTS.md` | `2a6b814e8df578bbc30c4bf2c40e05815df48cf0d1c2308630b7f7042ff207bc` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/LIMITATIONS_AND_SURVIVORSHIP.md` | `28eb4796d371ffb527845b8539b5cbb14493a191452b2f37bca4956a21971deb` |
| `research/level1_sleeve_robustness/attempts/RISK-0001-EXECUTION-ATTEMPT-002/results/RESULTS_DISCLOSURE_SUPPLEMENT.md` | `8013f376a0ad08bbbdffe7e6481d8d3e40b993b98515f6f3a9b7c445d49ded45` |

The historical window is fixed and is not a current-market observation. It is admitted only for the
questions it directly measured and as a precision/abstention gate. Its accounting and limitations
remain part of the evidence; no family result may be detached from them.

### D. Missing direct pairs and non-transitivity

All six driver classes are applicable to every investable-sleeve marginal-capital pair. They may not
be marked `not_applicable` merely because evidence is missing. The frozen mapping is:

| Driver class | Exact frozen treatment for every pair |
|---|---|
| `portfolio_function` | A source may disclose an individual function, but no admitted current direct-comparative source determines marginal preference. State is missing/`unable_to_determine`. |
| `valuation_opportunity_cost` | No accepted Level-1 comparative endpoint or aggregation exists. State is missing/`unable_to_determine`. |
| `downside_path_risk` | RISK is admitted historical evidence, but every family disposition is `unable_to_determine`; preserve that state. |
| `recovery` | Same RISK treatment; no unavailable/censored observation is imputed. |
| `diversification_cobehavior` | Current-weight overlap is forbidden and both correlation/defensive interfaces are uncomputed. State is missing/`unable_to_determine`. |
| `sleeve_deployability` | No admitted current, directly comparable sleeve-level evidence exists across both members of any pair. State is missing/`unable_to_determine`. |

The legacy relationship fields `primary_disposition`, `favored_sleeve_id`, evidence maturity,
coverage, and coexistence/readiness language are disclosure-only under XASSET-0020 and may not fill
any ledger cell. Consequently the four pairs with historical relationship records—
`equity__fund_broad_market`, `equity__fund_gld_defensive`, `equity__crypto`, and
`fund_gld_defensive__crypto`—each have the deterministic pair conclusion
`unable_to_determine` under this snapshot. This is an application rule, not a populated pair record.

For `fund_broad_market__fund_gld_defensive` and `fund_broad_market__crypto`, XASSET-0020 §I already
closes the application rule: the pair conclusion is `unable_to_determine`. Missingness is neither
neutral nor indistinguishable. No equity-mediated, GLD-mediated, benchmark, category, economic-role,
or other transitive/proxy inference is permitted.

XASSET-0020 permits an affected sleeve range to survive only if both endpoints are independently
governed and remain valid under every possible direction of the unresolved pair. This snapshot has no
lawful endpoints under §F. Therefore the missing-pair rows are `APPLICATION_MUST_ABSTAIN`, not
`SEPARATE_PREREQUISITE_REQUIRED`. New direct-pair evidence would be required only to seek a later
non-abstaining result; it is not one of the prerequisites preventing an abstention-capable application.
That application nevertheless remains unauthorized until the separate mechanical prerequisite in §O
becomes effective.

### E. Representation sensitivity

Representation handling is a precision gate only:

1. A point is eligible only if every representation required by its source authority is admitted and
   gives the same determinate direction for every driver bearing on the point.
2. A range is eligible only if every endpoint is separately governed for every required
   representation and their exact intersection is non-empty and valid under every representation.
3. A missing, unavailable, conflicted, or directionally disagreeing required representation makes the
   affected point/range ineligible. No majority, average, weighting, representative selection, or
   “most conservative” selection is permitted.
4. Representation disagreement is recorded in disclosures and cannot become a directional score.

Applied as an eligibility rule to the frozen snapshot—not as a populated application result:

- `equity`: the company-level valuation corpus has no accepted Level-1 aggregation rule and the RISK
  family is `unable_to_determine`;
- `fund_broad_market`: SPY/VEA/VWO remain separate, VWO carries governed gaps in RISK, and the family
  is `unable_to_determine`;
- `fund_gld_defensive`: the accepted RISK evidence preserves mixed path/opportunity-cost direction and
  admitted-representation limitations, yielding `unable_to_determine`; and
- `crypto`: BTC/ETH disagreement and SOL unavailable/missing observations remain preserved, yielding
  `unable_to_determine`.

Each row is `APPLICATION_MUST_ABSTAIN` for point/range precision under this snapshot. No separate
representation study is a prerequisite to record that abstention.

### F. Endpoint derivation

A future point endpoint may originate only from one exact numeric value uniquely stated by admitted
effective authority or uniquely mathematically derived from admitted authoritative inputs with complete
NUM-0001 provenance. A future range endpoint has the same rule independently for each bound. Bound
intersection may narrow already-authorized endpoints but may not create one.

The frozen snapshot contains no such Level-1 endpoint authority for any sleeve. No endpoint may be
created from a historical target, XASSET-0016 or XASSET-0018 output, midpoint, current allocation,
analyst or reviewer preference, evidence count, relative maturity, residual balancing, equal division,
or undocumented judgment. Therefore:

- point eligibility is `APPLICATION_MUST_ABSTAIN` for every sleeve;
- range eligibility is `APPLICATION_MUST_ABSTAIN` for every sleeve; and
- `point_or_range_or_null` must remain null in the future sleeve ledgers.

This is an eligibility closure, not an application or a populated outcome record.

### G. Precision, rounding, and NUM-0001

No economic rounding parameter exists or is needed. Canonical arithmetic is exact:

- the normalized asset unit is XASSET-0020's mathematically derived symbolic unit;
- counts and canonical ordering are exact procedural/mathematical constants;
- any later lawful numeric value must be represented at exact source precision or as an exact rational
  derivation with full NUM-0001 provenance;
- canonical values may never be rounded before comparison, intersection, constraint application, or
  reconciliation; and
- human display rounding is non-authoritative, must be labeled `display_only`, must retain a pointer to
  the exact canonical value, and may not alter any outcome.

Under this snapshot no endpoint exists, so endpoint storage/display precision is not applicable. If a
future application encounters arithmetic requiring a rounding choice, it must abstain; it may not inherit
a historical decimal convention. Exact symbolic reconciliation is required and a display mismatch must
be resolved by redisplaying the exact canonical value, never by changing the ledger.

### H. Conflict, materiality, and freshness

No unquantified materiality judgment exists. For the exact same question and scope:

- any two admitted same-authority drivers with contrary directions produce
  `unable_to_determine`;
- an admitted determinate direction plus an admitted `unable_to_determine`, missing, stale, or
  conflicted required state produces `unable_to_determine`;
- different scopes are disclosed separately and never averaged; and
- higher-authority conflicts follow GOV-0002 and block the affected item.

Words such as “material,” “significant,” “sufficient,” “meaningful,” or “reasonable” in source prose
do not create thresholds or application discretion. Only closed structured states and exact source
identities control.

Freshness behavior is likewise exact:

- a source-owned rule is applied exactly as written and its observed state is recorded;
- a source with no governed currentness rule remains historical/disclosure evidence and is excluded
  from current positive preference;
- the GLD functional-doctrine hash pin is current at the snapshot but establishes function only;
- issuer-lookthrough/ETF-direct overlap remains point-in-time disclosure because current holdings and
  weights are prohibited from the application;
- company-level valuation freshness remains per-record disclosure because no Level-1 aggregation rule
  exists; and
- RISK remains fixed historical evidence and never becomes a current forecast.

No universal age threshold, freshness score, penalty, or author assessment is introduced.

### I. Liquidity boundary

XASSET-0019 requires a later explicit migration before legacy `cash_reserve` may participate in
economic sizing. XASSET-0020, the later accepted methodology, expressly permits a four-sleeve
provisional application while liquidity remains unresolved: it says no liquidity value is invented
and unsupported capital remains `UNSIZED_UNASSIGNED_CAPITAL`.

Therefore liquidity is `CLOSED_DETERMINISTICALLY` for this application boundary:

- `separately_governed_liquidity_state.status` is
  `unresolved_not_entered_into_application_ledger`;
- its numeric value is null, not zero;
- no liquidity term is subtracted or imputed;
- no cash target, reserve target, fifth sleeve, liquidity amount, or cash proxy is created; and
- the unresolved state remains a reopen trigger and blocks the later complete candidate/stress/adoption
  sequence where XASSET-0019 requires a fully specified asset state.

Liquidity resolution is not one of the prerequisites preventing a bounded four-sleeve
abstention-capable application. The application remains unauthorized for the separate mechanical
reason in §O. Liquidity remains a separate prerequisite for later work that requires an economically
complete candidate.

### J. Unassigned-capital reconciliation

The future application must preserve the exact symbolic ledger identity:

`NORMALIZED_ASSET_UNIT = SUM(ADMITTED_SLEEVE_ASSIGNMENTS) + UNSIZED_UNASSIGNED_CAPITAL`

while liquidity is in §I's unresolved/non-entered state. An abstaining sleeve contributes no admitted
assignment; it is not treated as an assigned zero-weight sleeve. Every unsupported or constraint-clipped
portion remains on the right-hand side as `UNSIZED_UNASSIGNED_CAPITAL` with
`deployment_status: prohibited_without_future_governance`.

No unassigned amount may become cash, reserve, SPY, any other sleeve, pro-rata redistribution, debt
repayment, margin reduction, or a zero-return/risk proxy. The four sleeves are not forced to exhaust the
unit. A negative complement or a reconciliation requiring a plug invalidates the application.

### K. Accepted RISK treatment

The four accepted family states remain exactly:

- `EQUITY = unable_to_determine`;
- `FUND_BROAD_MARKET = unable_to_determine`;
- `FUND_GLD_DEFENSIVE = unable_to_determine`; and
- `CRYPTO = unable_to_determine`.

They are historical evidence and precision/abstention gates only. They may not be recoded as neutral,
indistinguishable, non-rejection, a directional lean, a target anchor, a range anchor, or an adjustment.
Because no independent endpoint survives, each state makes the affected sleeve's point/range eligibility
`APPLICATION_MUST_ABSTAIN` under this snapshot.

### L. Application contract remains a separate prerequisite

This decision does not define or authorize an application artifact schema, generator, serializer,
validator, fixture, or populated record. The prior application-contract sketch was not an exact schema:
it did not close the field set, types, vocabularies, ordering, metadata derivation, canonical bytes, or
trace content, and therefore cannot support application authority.

The smallest required future unit is one separate Lane G governance unit titled, by scope,
`Level-1 Application Artifact Schema and Deterministic Generation Authority`. It must remain purely
mechanical and must not add economic evidence, parameters, endpoints, portfolio rules, or policy. To
close CM-27 and CM-28, that unit must define all of the following as one reviewable contract:

1. one exact schema name and version, canonical artifact path, file format, and encoding;
2. one canonical serialization, including newline, key/field order, whitespace, numeric, null, list,
   duplicate-field, and extra-field rules sufficient for byte-identical reproduction;
3. the complete allowed top-level and nested field set, with every field's required/forbidden/nullable
   status, exact type, enum vocabulary, canonical order, and fixed or mechanical value derivation;
4. closed vocabularies for every evidence, freshness, missingness, conflict, representation, driver,
   constraint, pair, sleeve, endpoint, reconciliation, provisional/adoption, and reopen-trigger state;
5. fixed or mechanically derived schema, methodology, prerequisite, snapshot, source-tree, and
   application identities, with no wall-clock or author-chosen metadata in canonical bytes;
6. one exact deterministic derivation-trace structure, required step identifiers, contents, and order;
7. one exact reopen-trigger identifier set, contents, and order;
8. a non-self-referential lifecycle binding: the committed artifact must not contain the SHA of the
   commit that contains itself; exact application PR/head identity must instead be external Git/GitHub
   lifecycle metadata verified by independent review and later acceptance records, and must not alter
   the canonical artifact bytes;
9. the smallest generator/validator/fixture mechanism necessary to prove that identical frozen inputs
   necessarily produce identical canonical bytes; and
10. exact rejection fixtures covering every adversarial case in §M.

Until that separate unit becomes effective, no application author may choose a record shape, field,
value vocabulary, metadata value, trace, reopen-trigger list, serialization, or lifecycle binding.
The economic population consequences already closed by §§C-K remain unchanged, but they do not by
themselves define lawful artifact bytes.

### M. Required static and adversarial proof for the separate prerequisite

The separate unit named in §L must supply a closed validator/generator/fixture contract that rejects
each of the following before any application may be authorized:

1. methodology, lifecycle, path, file-hash, content-hash, or RISK identity drift;
2. any evidence class not frozen in §C;
3. missing, extra, reversed, or duplicate sleeve/pair records;
4. missing direct evidence treated as neutral or indistinguishable;
5. transitive or proxy pair inference;
6. any RISK `unable_to_determine` state treated as direction, anchor, or neutral evidence;
7. historical/current target, holding, weight, XASSET-0016/0018 output, or midpoint used as endpoint;
8. any automatic midpoint or vector selection from a range;
9. rounding that changes comparison, eligibility, intersection, constraint, or reconciliation;
10. any unclosed “material,” “significant,” “sufficient,” “meaningful,” or “reasonable” judgment;
11. historical evidence silently treated as a current positive driver;
12. unassigned capital treated as cash, reserve, fund, redistribution, debt repayment, or proxy;
13. forced four-sleeve exhaustion;
14. liquidity treated as a fifth sleeve or as numeric zero;
15. any point/range despite absent endpoint authority;
16. current holdings/targets used as priors;
17. score, confidence percentage, tally, utility, optimizer, solver, grid, sweep, or hidden weighting;
18. Level-2 membership/refreeze or instrument sizing;
19. policy/adoption/deployment/trading language; or
20. any extra field or omitted required field;
21. any wrong field type, invalid enum, or free-text substitution for a governed enum;
22. any alternate canonical semantic-list or field ordering;
23. any alternate encoding, newline, whitespace, key ordering, or other serialization;
24. any noncanonical null or numeric representation;
25. any altered, omitted, added, reordered, or free-text deterministic-trace step;
26. any altered, omitted, added, reordered, or free-text reopen trigger;
27. any schema-name or schema-version drift;
28. any committed artifact field that purports to contain the SHA of its own containing commit; or
29. non-byte-identical repeated output from identical frozen inputs.

This section requires future mechanical proof; it does not authorize that subsystem or an application
inside this filing. This filing's own validation must instead prove the §N reclassification, failed
authorization gate, unchanged 35-source snapshot, and unchanged economic closures.

### N. Complete machine-reviewable closure matrix

```yaml
closure_matrix_schema: XASSET-0021.v1
allowed_states:
  - CLOSED_DETERMINISTICALLY
  - APPLICATION_MUST_ABSTAIN
  - SEPARATE_PREREQUISITE_REQUIRED
rows:
  - {id: CM-01, issue: methodology_identity, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-02, issue: evidence_population_and_hashes, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-03, issue: evidence_authority_and_effectivity, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-04, issue: evidence_question_classification_and_forbidden_implications, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-05, issue: source_owned_freshness_behavior, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-06, issue: same_level_conflict_and_missingness_behavior, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-07, issue: missing_pair_fund_broad_market__fund_gld_defensive, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-08, issue: missing_pair_fund_broad_market__crypto, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-09, issue: transitive_or_proxy_pair_inference, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-10, issue: existing_pair_equity__fund_broad_market, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-11, issue: existing_pair_equity__fund_gld_defensive, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-12, issue: existing_pair_equity__crypto, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-13, issue: existing_pair_fund_gld_defensive__crypto, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-14, issue: equity_representation_and_level1_valuation_aggregation, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-15, issue: fund_broad_market_representation_sensitivity, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-16, issue: fund_gld_defensive_representation_sensitivity, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-17, issue: crypto_representation_sensitivity, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-18, issue: point_endpoint_derivation, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-19, issue: range_endpoint_derivation, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-20, issue: midpoint_or_vector_selection, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-21, issue: precision_rounding_and_num_0001, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-22, issue: conflict_materiality_threshold, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-23, issue: liquidity_boundary_for_four_sleeve_application, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-24, issue: unassigned_capital_reconciliation, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-25, issue: accepted_risk_uncertainty_treatment, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-26, issue: sleeve_vs_unassigned_positive_endpoint_requirement, state: APPLICATION_MUST_ABSTAIN}
  - {id: CM-27, issue: application_schema, state: SEPARATE_PREREQUISITE_REQUIRED}
  - {id: CM-28, issue: deterministic_trace_and_repeatability, state: SEPARATE_PREREQUISITE_REQUIRED}
  - {id: CM-29, issue: legacy_and_current_allocation_anchor_exclusion, state: CLOSED_DETERMINISTICALLY}
  - {id: CM-30, issue: provisional_nonadopted_authority_boundary, state: CLOSED_DETERMINISTICALLY}
summary:
  substantive_row_count: 30
  closed_deterministically: 14
  application_must_abstain: 14
  separate_prerequisite_required: 2
  application_time_author_or_reviewer_judgment_remaining: 2
```

The matrix is normative. If the structured counts do not reconcile, application authority is withheld.
Any `SEPARATE_PREREQUISITE_REQUIRED` row withholds authority until a new accepted governance decision
resolves it.
`application_time_author_or_reviewer_judgment_remaining` counts unresolved substantive rows, not the
individual design choices inside them; application is prohibited from resolving either row.

### O. Application-authority determination

The §N gate fails because CM-27 and CM-28 are `SEPARATE_PREREQUISITE_REQUIRED`. XASSET-0021 therefore
authorizes no XASSET-0020 methodology application, including an abstention-only application.
XASSET-0020 remains methodology authority only.

The smallest prerequisite is the one mechanical Lane G unit named in §L. It must become effective
through its own independent exact-head review, principal exact-head acceptance, merge, immediate
post-merge verification, and successful exact-head CI before any application may start. Only after
that effectivity may a later governance decision determine whether one application PR can be
authorized. Neither this decision nor the future prerequisite may silently treat application authority
as automatic.

To seek any future non-abstaining result, separate governance would additionally have to admit
question-matched evidence that actually closes the affected missing direct pair(s), representation
rule(s), and endpoint authority. Those are later reopen paths, not part of the mechanical prerequisite.
Liquidity migration remains separately required before later complete-candidate/stress/adoption work.

### P. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files:

1. this decision;
2. `governance/decisions.yaml` — one catalog row;
3. `operations/WORKSTREAMS.yaml` — additive XASSET-0020 lifecycle and XASSET-0021 active-lane facts;
4. `test_portfolio_hq_dashboard_decisions.py` — the two mechanical decision-count assertions.

No supporting audit is needed because the exact snapshot, rules, application contract, and complete
closure matrix are contained here. No Intelligence, research-result, production, configuration,
allocator, target, holding, gate, margin, chart, ladder, or protected portfolio file is changed.

WORKSTREAMS records that XASSET-0020 is effective, XASSET-0020 withheld application authority,
XASSET-0021 prerequisite classification is active, CM-27/CM-28 remain separate prerequisites, no
sizing/application has occurred, and liquidity/Level-2 boundaries remain unchanged. No later
application may begin until the separate mechanical unit in §L becomes effective and new application
authority is granted.

### Q. Reopen triggers

Reopen XASSET-0021 before application if any of these occurs:

- XASSET-0020's effective identity changes;
- any §C path or exact hash changes;
- a new evidence class, direct pair, representation rule, endpoint authority, or freshness rule is
  proposed for use;
- liquidity or Level-2 architecture changes a boundary relied on here;
- an accepted RISK identity or disposition changes;
- a validator reveals incomplete closure, nondeterminism, hidden arithmetic, or schema ambiguity; or
- an application would require any author/reviewer judgment not represented in §N.

A reopen decision does not itself create a point, range, weight, target, liquidity amount, membership,
or policy.

### R. Absolute non-authorization

This decision does not apply the methodology and produces no actual sleeve point, range, weight,
target, allocation, example portfolio, application record, Level-2 membership or sizing, liquidity or
cash amount, reserve amount, debt-reduction amount, margin/leverage rule, chart, ladder, deployment,
optimizer, backtest, trade, order, brokerage action, or portfolio-policy adoption. It changes no current
portfolio configuration.

## Rationale

XASSET-0020 is deliberately abstention-capable. The honest way to close economic discretion is not to
manufacture the missing evidence or endpoints, but to make their consequence mechanical. Freezing the
exact evidence, excluding historical or unaggregated sources from current positive preference,
propagating every accepted uncertainty state, eliminating rounding and materiality judgment, and keeping
unassigned capital explicit leaves no economic choice. It does not, however, supply the exact artifact
and deterministic-generation authority needed to produce one lawful application record.

Liquidity does not need to be mislabeled as a prerequisite to this bounded step. XASSET-0020 expressly
permits unresolved liquidity to remain outside the application ledger while unsupported capital stays
unassigned; XASSET-0019's complete-candidate requirement still blocks later stress/adoption work until
the liquidity architecture is separately resolved.

## Alternatives Considered

**Require new direct-pair research before any application.** Rejected: XASSET-0020 already supplies the
deterministic missing-pair result, and an abstention application needs no proxy or new evidence.

**Select one representative instrument per sleeve.** Rejected: no accepted representation-selection
authority exists, and selection would create the directional judgment this filing must eliminate.

**Use historical outputs or current allocations as endpoints.** Rejected: XASSET-0019/0020 explicitly
bar them, and NUM-0001 would not convert historical precision into economic authority.

**Resolve disagreement with a threshold or majority.** Rejected: no governed threshold exists; the
categorical fail-closed rule is deterministic and does not disguise conflict as confidence.

**Treat unresolved liquidity as numeric zero.** Rejected: that would silently size liquidity. The exact
state is null and not entered; unsupported capital remains unassigned.

**Close the exact schema and deterministic generator inside this correction.** Rejected: doing so would
originate a new schema, canonical serializer, generator/validator, and fixture subsystem rather than
correct the two false matrix classifications. That work is mechanical rather than economic, but still
requires its own bounded authority and exact-head review.

## Consequences

If this decision completes its full lifecycle, application authority remains withheld. One separate
mechanical Lane G prerequisite must close the exact artifact schema and deterministic generation
contract before a later governance decision may consider authorizing an application. Under the current
evidence boundary, any eventual compliant application still could not lawfully create a point or range
and would have to preserve abstention and unassigned capital. Any non-abstaining result requires later,
separately accepted evidence/parameter authority and a reopen of this prerequisite closure. Portfolio
policy, liquidity, Level 2, targets, holdings, and execution remain unchanged.
