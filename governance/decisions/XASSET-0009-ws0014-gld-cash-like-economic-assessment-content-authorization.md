---
decision_id: XASSET-0009
date: 2026-08-10
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, VALUATION-0001, VALUATION-0002, VALUATION-0004, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002]
supporting_artifact: null
file: governance/decisions/XASSET-0009-ws0014-gld-cash-like-economic-assessment-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0008` designed, as text only, a closed economic-assessment methodology for exactly two analytical
subjects — `GLD` and `CASH_LIKE_CAPITAL` — closing part of `XASSET-0005` §5 step 2's own restated sequence
("perform asset-appropriate valuation/economic assessment — future, separate, undesigned") for those two
subjects. `XASSET-0008` §A names five stages and states plainly that it authorizes stage 1 (methodology
design) only: stage 2 ("future, separate content authorization — not performed here; requires its own
future, explicit principal authorization, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0006`'s own
role for the ETF, crypto, and functional-doctrine content steps") is exactly this filing. This filing is
the direct analogue of `XASSET-0003`, `XASSET-0004`, and `XASSET-0006` for the economic-assessment content
step — authorization only, binding by reference to `XASSET-0008`'s already-accepted design, no
restatement, no redesign.

**Batching determination — one filing, both analytical subjects, no split required.** Unlike `XASSET-0005`
(which designed two *separate* content domains — functional doctrine and the overlap model — in one
batched filing, requiring two separate content authorizations, `XASSET-0006` and `XASSET-0007`, never
combined), `XASSET-0008` designed **one schema** covering **two population members within it**
(`GLD`, `CASH_LIKE_CAPITAL`), explicitly requiring "one dedicated validator module
(`economic_assessment_validator.py`...)" (`XASSET-0008` supporting artifact §11). This is structurally the
same shape as `XASSET-0006`, which authorized one implementation PR covering all four functional-doctrine
capital-use types under one shared schema — not the `XASSET-0002`→`XASSET-0003`+`XASSET-0004` shape, which
split two genuinely separate frameworks. This filing accordingly authorizes **exactly one** future
implementation PR covering **both** `GLD` and `CASH_LIKE_CAPITAL` — splitting them into two separate
authorization filings would fragment one already-unified schema for no review benefit, the same reasoning
`XASSET-0006` §A point 4 already applied to the functional-doctrine sleeve's four-record population, here
applied to an even smaller two-record population.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0009-gld-authorization-s7qao5`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `47851f8042c65989e3b9ed606943089fec47b23e` — the `XASSET-0007`-authorized overlap-model content
  implementation's own merge commit (PR #292).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #292`'s full lifecycle independently re-verified via the GitHub API, not assumed**: merged
  (`merged: true`, `merged_by: Mast3rkey`), head `3a36e831d7f7f958649150e5508ead187f5f7d0e`, base `main` @
  `957d14b7d3ac8e299b3c966d7aeed00f85c03ae0`, 17 changed files, 2 commits; independent exact-head review
  `pullrequestreview-4893474500` (**APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR /
  0 MINOR / 2 non-blocking NOTE), cited verbatim in the merge-commit message itself; merge (merge commit
  `47851f8042c65989e3b9ed606943089fec47b23e`, parents `957d14b7d3ac8e299b3c966d7aeed00f85c03ae0` and
  `3a36e831d7f7f958649150e5508ead187f5f7d0e`, both independently re-confirmed via `git log --pretty`);
  merge-commit CI independently re-fetched — workflow run `31352460106`, `status: completed`,
  `conclusion: success`. `WS-0014` step 7's own content half (all ten overlap-model dimension records) is
  therefore fully implemented and merged.
- **A genuine, disclosed stale-state finding, independently discovered this session, not assumed from any
  prior filing's own summary**: `operations/WORKSTREAMS.yaml`'s own
  `xasset0008-gld-cash-reserve-economic-assessment-methodology-design` gate — as last written by the
  `PR #292` authoring session — describes `XASSET-0008` as "this session, unmerged," "draft, unmerged."
  Independently verified via `git log --graph` and the GitHub API that this is **stale**: `XASSET-0008`
  (`PR #287`) in fact merged to `main` **before** `PR #292` was even branched — `PR #292`'s own base
  (`957d14b7...`) is a descendant of `PR #287`'s merge commit (`b3fb5325...`). `PR #292`'s authoring
  session branched from a state that already contained `XASSET-0008`, but its own copy of
  `operations/WORKSTREAMS.yaml` (inherited, unedited on this point, from before `PR #287` merged into that
  session's own lineage) still carried the pre-merge description, and `PR #292`'s own scope (overlap-model
  content only) gave it no reason to touch that unrelated gate. **`PR #287`'s full lifecycle independently
  re-verified via the GitHub API, not assumed** (§H fold-forward below gives the complete chain): accepted
  head `ed117baba90e537a97292675dd19138d8c4eb72e`; three independent review rounds (original
  `pullrequestreview-4891713650`, CHANGES REQUIRED 0/0/2/0; delta `pullrequestreview-4891924618`, CHANGES
  REQUIRED 0/0/2/0; final delta `pullrequestreview-4891981315`, **APPROVED FOR PRINCIPAL EXACT-HEAD
  ACCEPTANCE**, 0/0/0/0); principal acceptance posted as review `pullrequestreview-4891991832`; merge
  (merge commit `b3fb5325cac5736daf59a109ebc5e1daa1704297`, parents `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`
  and `ed117baba90e537a97292675dd19138d8c4eb72e`); merge-commit CI — workflow run `31326626381`,
  `status: completed`, `conclusion: success`. **`XASSET-0008` is therefore merged and effective** —
  independently confirmed by the presence, on this session's own `main`-identical `HEAD`, of the decision
  file, its supporting artifact, and every commit in `PR #287`'s own history (`bb938ec`, `1323307`,
  `252622b`, `ed117ba`, all confirmed ancestors of `HEAD`). Per this repository's established
  never-silently-rewrite-a-prior-gate's-own-text convention, this stale description is **not edited in
  place** — §H below adds a new, additive `xasset0008-post-merge-verification` gate recording the accurate,
  independently re-verified state, exactly mirroring how `xasset0007-post-merge-verification` was added
  (by `XASSET-0008` itself) to record `PR #286`'s merge without rewriting the
  `xasset0007-overlap-model-content-authorization` gate's own historical text.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `active_branch:
  claude/xasset-0007-overlap-model-mqov2k`, `active_pr: 292`, `last_verified_main_sha:
  957d14b7d3ac8e299b3c966d7aeed00f85c03ae0`, `last_verified_date: "2026-08-10"` — the `active_pr`/
  `last_verified_main_sha` fields are themselves stale relative to `PR #292`'s own now-confirmed merge (the
  same self-referential pattern this repository's convention explicitly defers to "the next filing that
  substantively touches the workstream," per the identical precedent `XASSET-0003`'s own post-merge
  comment established for `WS-0014`) — this filing performs that deferred synchronization (§H).
- **`WS-0015`'s live state independently read and left untouched** — no established fold-forward reason or
  authority for this filing, an unrelated `WS-0014` unit, to edit it.
- **`XASSET-0001` (§A, §D, §E, §F, §J, §M), `XASSET-0005` (decision file and supporting artifact),
  `XASSET-0006` (in full), `XASSET-0007` (in full), and `XASSET-0008` (decision file and supporting
  artifact, in full) read directly this session**, not summarized from memory.
- **`OPS-0007` (capability-based review standard, §1) and `OPS-0009` (Lean Delivery lifecycle, Lane G) read
  directly this session** for the applicable review-eligibility and lifecycle-lane discipline — this filing
  is classified Lane G (governance authorization) throughout, matching every prior `XASSET-####` content
  authorization.
- **`intelligence/functional_doctrine/{CASH,RESERVE,GLD_DEFENSIVE_ROLE,DEBT_REDUCTION}.yaml` and
  `functional_doctrine_validator.py` independently read directly**: all four confirmed sealed,
  byte-unedited. `CASH.yaml`'s `functional_role.role_category: operational_liquidity_float` and
  `RESERVE.yaml`'s `functional_role.role_category: unable_to_determine` confirmed exactly as `XASSET-0008`
  describes them. `functional_doctrine_validator.py`'s `canonical_record_hash(data: dict) -> str` function
  confirmed present at line 355, unchanged since `XASSET-0008`'s own citation.
- **`intelligence/etf_classification/GLD.yaml` and `etf_classification_validator.py` independently read
  directly**: confirmed sealed, unaffected by any intervening filing. `structure_and_methodology.
  benchmark_type: spot_commodity_price` and `cost_and_tracking_quality.expense_ratio_pct: 0.4` confirmed
  exactly as `XASSET-0008` cites them. `etf_classification_validator.py`'s `canonical_record_hash(data:
  dict) -> str` function confirmed present at line 322, unchanged since `XASSET-0008`'s own citation.
- **`intelligence/overlap_model/defensive_offset_interface.yaml` independently read directly**: confirmed
  `computation_status: not_yet_computable_interface_only`, unconditional — `XASSET-0007`'s implementation
  did not loosen this value despite `GLD_DEFENSIVE_ROLE.yaml` now existing, exactly as `XASSET-0007` §A
  point 2/§D require. This filing's own §E below restates, unweakened, the boundary `XASSET-0008` §E
  already drew between GLD's own single-asset historical characterization (this filing's future scope) and
  `defensive_offset_interface`'s own portfolio-level, still-forced-abstention computation (out of scope
  here, unaffected).
- **`intelligence/economic_assessment/` confirmed absent** — no directory, no file, anywhere in the
  repository, at this session's own starting head.
- **Decision catalog independently rebuilt**: **104 decisions, `issues == ()`** at the starting head, 104
  non-`README.md` files in `governance/decisions/` reconciling 1:1. `XASSET-0009` confirmed unused: zero
  matches in `governance/decisions.yaml`, zero matches via full-repository grep for the literal string
  `XASSET-0009` across every `.md`/`.yaml`/`.py` file. `governance/decisions/README.md`'s own rule ("a new
  prefix is chosen only when a genuinely new decision domain needs one") is satisfied by continuing the
  existing `XASSET-####` series — this filing is the direct continuation of `XASSET-0008` §A stage 2, not a
  genuinely new decision domain, mirroring `XASSET-0003`'s, `XASSET-0004`'s, `XASSET-0006`'s, and
  `XASSET-0007`'s identical continuation.
- **Full repository `pytest` independently re-run this session**, matching the expected post-`PR #292`
  baseline, before any edit in this filing.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does three things, in one bounded PR:

1. **Performs the ordinary `WS-0014` self-reference synchronization** (`active_branch`, `active_pr`,
   `last_verified_main_sha`, `last_verified_date`) reflecting this session's own live-state verification.
2. **Adds two additive Lane M fold-forward gates** — one recording `PR #292`'s own confirmed merge/review/
   acceptance/CI state (the `xasset0007-overlap-model-content-implementation` gate's own historical text is
   left unedited), and one recording `PR #287`'s (`XASSET-0008`'s own governance filing) confirmed merge/
   review/acceptance/CI state, correcting the stale-description finding disclosed in the Preflight above
   without editing the `xasset0008-gld-cash-reserve-economic-assessment-methodology-design` gate's own
   historical text.
3. **Authorizes exactly one future, separate, bounded economic-assessment (content) implementation pull
   request**, covering both analytical subjects `GLD` and `CASH_LIKE_CAPITAL` under the exact schema,
   evidence, sequencing, abstention, structural-reference, and validator/test controls already specified
   and accepted through `XASSET-0008`. It performs no population itself, creates no economic-assessment
   record or validator, and implements no `intelligence/economic_assessment/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1), any
required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle every prior filing in this chain has followed — may proceed to:

1. Draft and seal one `economic_assessment` record for each of the two fixed analytical subjects named in
   `XASSET-0008` §B — `GLD` and `CASH_LIKE_CAPITAL` — zero exclusions, zero additions. No `CASH` or
   `RESERVE` as a standalone `analytical_subject` value, and no `DEBT_REDUCTION` value of any kind, may be
   introduced without its own separate, future, explicit authorization (`XASSET-0008` supporting artifact
   §11 point 1's own closed-population rule).
2. Create the appropriate `COHORT_MANIFEST.yaml` for the two sealed records, matching every prior
   classification framework's own manifest convention (`XASSET-0008` supporting artifact §7 point 5's
   `record_status` sealing discipline; §11 point 16's determinism requirement).
3. Build `economic_assessment_validator.py` — the one dedicated validator module `XASSET-0008` supporting
   artifact §11 already names — and its dedicated test file.
4. Use a single implementation pass covering both analytical subjects (no per-subject PR structure; no
   multi-shard isolation apparatus of any kind) — the population is fixed and smaller than the
   functional-doctrine sleeve's own four-record population, which `XASSET-0006` §A point 4 already
   determined needs no shard isolation; this filing makes the identical determination binding here, a
   fortiori, for a two-record population.
5. Stop after the first record, without a separate pilot authorization, if a systemic schema, evidence, or
   contamination defect is discovered — an internal stop-and-fix condition within the one authorized
   implementation PR, not a license to split into a second governance filing or a per-subject PR structure.

**No `CASH`/`RESERVE` distinct-purpose content of any kind is authorized by this filing** — the future
implementation must never assert, in any field or free-text rationale, that `CASH` and `RESERVE`
individually warrant different treatment (§B below, `XASSET-0008` §D.4/§F/§J's own binding rule, supporting
artifact §11 point 15's dedicated validator scan). **No overlap-model content and no `DEBT_REDUCTION`
economic-assessment content of any kind is authorized by this filing** — both remain separately, wholly
unauthorized (`XASSET-0007`'s own future overlap-model content step is already separately authorized and
implemented via `PR #292`, unaffected and untouched here; `DEBT_REDUCTION`'s economic-assessment gap
belongs to the separately governed margin/leverage-policy track, `XASSET-0008` §B).

### B. Binding specification — by reference, not restatement

The implementation PR must follow `XASSET-0008`'s specification exactly, as accepted and merged at
`ed117baba90e537a97292675dd19138d8c4eb72e` (`PR #287`). This filing does not redesign, loosen, tighten, or
restate that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section (`XASSET-0008 §N` citations refer to the decision file; `AA §N` citations refer to the supporting artifact, `governance/audits/WS0014_GLD_CASH_RESERVE_ECONOMIC_ASSESSMENT_METHODOLOGY_DESIGN_20260809.md`) |
|---|---|
| Exactly two `analytical_subject` values (`GLD`, `CASH_LIKE_CAPITAL`); no `CASH`/`RESERVE` as a standalone value; no `DEBT_REDUCTION` | `XASSET-0008` §B; `AA` §3, §11 point 1 |
| One shared substantive axis (`deployability_and_optionality`, computed once per subject) plus one GLD-only compound axis (`instrument_specific_economic_characterization`, `not_applicable: true` on `CASH_LIKE_CAPITAL`) plus `evidence_quality` on both — no third substantive axis, no numeric field of any kind, no score, no ranking formula, no target percentage, no expected-return or hurdle-rate figure | `XASSET-0008` §F, §G; `AA` §4.1–§4.4 |
| `deployability_and_optionality`: closed vocabulary `high_optionality_low_friction` \| `moderate_optionality` \| `low_optionality_or_structurally_constrained` \| `unable_to_determine` (required `abstention_reason`); no `not_applicable` path; computed for `CASH_LIKE_CAPITAL` **once**, never split by legacy identifier | `AA` §4.2 |
| `instrument_specific_economic_characterization` (`GLD` only): a closed, structurally required compound object with three independently-abstainable sub-fields — `cost_and_tracking_economic_significance`, `historical_inflation_sensitivity`, `historical_equity_drawdown_behavior` — each with its own closed vocabulary and prohibited-inference rules; `not_applicable: true` (literal, structural) on `CASH_LIKE_CAPITAL` | `AA` §4.3 |
| Structural references — `GLD`: two independent content-hash pins (`structural_reference_etf_classification` via `etf_classification_validator.canonical_record_hash()`, `etf_classification_validator.py:322`; `structural_reference_functional_doctrine` via `functional_doctrine_validator.canonical_record_hash()`, `functional_doctrine_validator.py:355`), both live-recomputed on every validator run, forbidden on `CASH_LIKE_CAPITAL`. `CASH_LIKE_CAPITAL`: a `legacy_structural_references` list of **exactly two** entries (one `source_capital_use_type: "CASH"`, one `"RESERVE"`), each via `functional_doctrine_validator.canonical_record_hash()`, cited as provenance context only — never content to copy or restate — forbidden on `GLD` | `XASSET-0008` §H; `AA` §5 |
| Zero numeric field anywhere, no carve-out of any kind (stricter than the ETF framework's own scoped `expense_ratio_pct` exception); the two legacy `target_pct` values (4.00%/1.00%) read only as structural identity context for the `legacy_structural_references` pins, never as a numeric input to any judgment axis | `XASSET-0008` §G |
| Evidence/contamination boundary — no live `holdings.yaml` value, no `targets.yaml` `target_pct`, no live `margin_state.py` output, no current dollar balance as evidence for any judgment axis; existing mechanisms may be cited structurally (e.g., the existence of the 30% buffer floor, the existence of the deposit/allocation workflow) | `XASSET-0008` §I |
| `CASH`/`RESERVE` as legacy structural identifiers, provenance only — no distinct-interpretation of any kind; `RESERVE.yaml`'s own sealed abstention preserved exactly as sealed, never resolved, inferred around, or bypassed by proxy; `CASH.yaml`'s own `operational_liquidity_float` characterization not treated as settled ground; no finding may cite the different labels or `target_pct` values as evidence of distinct purpose | `XASSET-0008` §D; `AA` §7 |
| Abstention discipline — non-cascading; `unable_to_determine` with required `abstention_reason` on every substantive axis and sub-field; a fully-abstained record for either subject is a fully valid, complete, sealed outcome — never force a value merely to fill the record | `XASSET-0008` §J; `AA` §4.2, §4.3, §7 point 5 |
| GLD/overlap-model boundary — this design may characterize GLD's own single-asset, historically-grounded drawdown behavior; it may never compute, duplicate, or preempt `defensive_offset_interface`'s own portfolio-level, still-forced `not_yet_computable_interface_only` finding; every future `historical_equity_drawdown_behavior` record must carry an explicit single-asset, non-portfolio-level disclosure | `XASSET-0008` §E; `AA` §6 |
| Future research interface — three named, unanswered GLD research questions (historical equity-drawdown behavior; realized tracking quality vs. the LBMA Gold Price PM benchmark, named in `GLD.yaml`'s own sealed narrative/provenance text, distinct from the categorical `benchmark_type: spot_commodity_price` field; a sourced, long-horizon gold/inflation characterization) — this filing conducts no research toward any of them and does not authorize the future implementation to treat any as already answered | `XASSET-0008` §K; `AA` §8 |
| Synthesis handoff — `cross_asset_handoff` envelope may carry only categorical findings, assessment/completeness status, evidence quality, freshness, uncertainty, abstentions, and structural references; never a target weight, rank, IN/OUT signal, buy/sell/hold signal, sleeve percentage, trade-timing recommendation, leverage amount, or any `CASH`-versus-`RESERVE`-distinction claim | `XASSET-0008` §L; `AA` §9 |
| Portfolio-selection boundary — evidence → cross-asset opportunity-cost synthesis → explicit human-approved adoption decision → only then, governed IN/OUT membership; completing both records, however completely, does not select the portfolio | `XASSET-0008` §M; `AA` §10 |
| Validator specification (16 points, `AA` §11: exact 2-subject population enforcement; closed schema at every level rejecting extra keys, not just missing ones; `analytical_subject`-conditional shape enforcement; `legacy_structural_references` exact-two-entry shape enforcement; no cross-schema field-name leakage — equity/ETF/crypto/functional-doctrine/overlap-model key names forbidden; zero numeric field with no carve-out; both GLD structural-reference pins' live hash recompute; `legacy_structural_references`' live hash recompute against both `CASH.yaml`/`RESERVE.yaml`; no chart-evidence leakage; no directive/trading-language leakage — the shared eight words, word-boundary matched; no predictive-language leakage, scoped to the two GLD historical sub-fields; overlap-model non-duplication check; evidence/provenance validation; allocator/margin import decoupling; **no `CASH`-versus-`RESERVE`-distinction leakage — a materially independent free-text scan, not a byproduct of the hash-reconciliation check**; deterministic generation and protected-path isolation) plus §11.1's five explicitly carried-forward lessons | `AA` §11, §11.1 |
| Test specification (`AA` §12's full item list: happy-path per subject; malformed/extra/missing keys at every level; wrong `analytical_subject`; `legacy_structural_references`/single-pin shape-mismatch rejection in both directions; `instrument_specific_economic_characterization` `not_applicable`-conditional rejection in both directions; every structural-reference hash independently verified via a live recompute, including a synthetic stale-hash test for each; cross-schema field-name leakage per source schema; numeric-field leakage per named term with no positive-acceptance test; chart-terminology leakage per term; directive/trading-language leakage per word including a false-positive guard; predictive-language leakage per term, scoped correctly; overlap-model non-duplication; **`CASH`-versus-`RESERVE`-distinction leakage per named pattern, individually, plus a positive test confirming neutral dual-citation is accepted**; abstention behavior including non-cascading; deterministic output; protected-path isolation including `CASH.yaml`/`RESERVE.yaml` themselves referenced-never-modified; allocator/margin import-coupling isolation) | `AA` §12 |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a
genuine ambiguity or gap in `XASSET-0008`'s specification must return for its own separate governance
correction — not resolve it unilaterally inside the implementation PR.

### C. Evidence standard (binding on the future implementation) — the RESERVE-non-blocking abstention preserved, not resolved

The implementing session must use only the evidence `XASSET-0008` §I authorizes. Where evidence is
insufficient for a given axis or sub-field on either subject, the implementation must use the framework's
own abstention path (§B above) rather than filling the gap — an axis abstaining on `GLD`, on
`CASH_LIKE_CAPITAL`, or on both is an honest, complete, sealed outcome, not a defect requiring correction.
This filing preserves, exactly as `XASSET-0008` §J/§D.6 and `AA` §7 point 5 already established, that:

1. `RESERVE.yaml`'s own sealed `functional_role.role_category: unable_to_determine` abstention is
   **structurally non-blocking** by design — no `CASH_LIKE_CAPITAL`-level axis is ever asked "on behalf of
   `RESERVE` specifically," so there is nothing for that abstention to cascade into or out of. The future
   implementation must not resolve, narrow, or work around `RESERVE.yaml`'s own abstention by proxy through
   any `economic_assessment` field.
2. `CASH.yaml`'s own sealed `functional_role.role_category: operational_liquidity_float` — independently
   confirmed, per `XASSET-0008`'s own bounded-correction investigation (§0), to be an AI-derived
   characterization, not a principal-sourced fact — must not be treated as settled ground for
   `CASH_LIKE_CAPITAL`'s own `deployability_and_optionality` determination. The implementation must reason
   from `XASSET-0008` §I's own permitted evidence sources (`CLAUDE.md`'s Workflow section and Portfolio
   Doctrine, cited as a shared mechanical fact about the combined family), never from either legacy
   record's own prior characterization as authority.
3. Three named GLD research questions (§B above) remain genuinely open — if the implementing session cannot
   source citable, dated, defensible evidence for `historical_inflation_sensitivity` or
   `historical_equity_drawdown_behavior`, `unable_to_determine` with a specific `abstention_reason` is the
   required, complete outcome; **this filing does not authorize any research toward answering them, and does
   not pre-decide whether the implementing session should attempt to.**

If the implementing session determines that gathering adequate evidence for any axis on either subject
requires research authority beyond what this filing and `XASSET-0008` already grant, it must stop and
disclose that as a genuine blocker rather than substitute an invented value or a forced determination
without disclosure.

### D. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: population drift (a
third `analytical_subject` value appearing to be needed, or either of the two ceasing to apply); any
equity-, ETF-, crypto-, functional-doctrine-, or overlap-model-shaped field leakage; any numeric
score/rank/target/expected-return/hurdle-rate leakage of any kind; any chart-domain leakage; any predictive/
forecast-language leakage inside the two GLD historical sub-fields; any attempt to compute, duplicate, or
preempt `defensive_offset_interface`'s own portfolio-level finding; any attempt to assert, in any field or
under any framing, that `CASH` and `RESERVE` individually warrant different treatment or that their
different `target_pct` values are meaningful as evidence; any attempt to resolve `RESERVE.yaml`'s own
sealed abstention, or to edit `CASH.yaml`/`RESERVE.yaml`/`GLD_DEFENSIVE_ROLE.yaml`/`GLD.yaml`; any
duplication or re-derivation of a sealed field from any referenced record rather than citing it by hash;
any consolidation of the `CASH`/`RESERVE` `targets.yaml` rows; any attempt to answer `XASSET-0008` §N's own
disclosed-but-unanswered consolidation question; any protected-path mutation; or any unexpected target,
holdings, gate, cap, cluster, allocator, margin, ladder, order, or trade change.

### E. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact two-subject
population; the exact changed-file inventory; schema conformance for both records, including the correct
`analytical_subject`-conditional shape of `instrument_specific_economic_characterization` and the
structural-reference mechanism; abstention validity and non-cascading behavior, including whether
`RESERVE.yaml`'s own abstention was correctly treated as non-blocking (§C.1) and whether `CASH.yaml`'s own
characterization was correctly withheld from authority (§C.2); both GLD structural-reference pins' live
hash recompute and absence of every ETF/functional-doctrine axis key name inside a `GLD` record;
`CASH_LIKE_CAPITAL`'s `legacy_structural_references` exact-two-entry shape and live hash recompute against
both `CASH.yaml` and `RESERVE.yaml`; the dedicated, materially independent `CASH`-versus-`RESERVE`-
distinction free-text scan and at least one positive neutral-citation test; the GLD/`defensive_offset_
interface` boundary disclosure on any `historical_equity_drawdown_behavior` finding; the validator and its
tests against `XASSET-0008` supporting artifact §11/§12's full specification, including §11.1's five
explicitly carried-forward lessons; CI; protected-path isolation; absence of any `DEBT_REDUCTION` or
overlap-model content of any kind; absence of any cross-asset synthesis, sleeve target, or instrument
target; and absence of any policy mutation. Any correction requires its own fresh exact-head delta review
before principal acceptance.

### F. GLD / overlap-model / DEBT_REDUCTION boundaries — restated, unweakened

**GLD**: the future implementation may characterize GLD's own single-asset, historically-grounded economic
characteristics (§B above) exactly as `XASSET-0008` §E/§K designed. It may not compute, duplicate, or
preempt `defensive_offset_interface`'s own portfolio-level diversification-benefit finding, which remains
forced `not_yet_computable_interface_only` under `intelligence/overlap_model/defensive_offset_
interface.yaml`'s own sealed value (independently reconfirmed this session, unaffected by `PR #292`'s own
merge) — this filing does not loosen that value and does not authorize the future implementation to loosen
it either.

**`DEBT_REDUCTION`**: remains entirely outside this filing's scope, exactly as `XASSET-0008` §B excludes
it. Its own economic-assessment gap (`avoided_borrowing_cost_readiness` /
`survivability_and_buffer_benefit_readiness`) belongs to the separately governed margin/leverage-policy
track — the 1.8x leverage cap, the 30% buffer floor, `MARGIN-0005`'s own bounded research charter — none of
which is touched, reopened, or weakened by this filing or the implementation it authorizes.

**Overlap model**: `XASSET-0007`'s own future content step is already separately authorized and fully
implemented (`PR #292`, §H below) — unaffected, untouched, and not reopened by this filing.

### G. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **`active_branch` set to this filing's own branch, `active_pr` set to this filing's own PR number,
   `last_verified_main_sha` updated** `957d14b7d3ac8e299b3c966d7aeed00f85c03ae0` →
   `47851f8042c65989e3b9ed606943089fec47b23e`, and **`last_verified_date` updated** to this filing's own
   date.
2. **One new additive gate, `xasset0007-overlap-model-content-implementation-post-merge-verification`**,
   recording — without editing the `xasset0007-overlap-model-content-implementation` gate's own historical
   text — that `PR #292` is fully merged, reviewed, principal-accepted, and post-merge verified (Preflight
   above gives the full independently re-verified chain).
3. **One new additive gate, `xasset0008-post-merge-verification`**, recording — without editing the
   `xasset0008-gld-cash-reserve-economic-assessment-methodology-design` gate's own historical text — that
   `PR #287` (`XASSET-0008`) is in fact fully merged, reviewed, principal-accepted, and post-merge verified
   (Preflight above gives the full independently re-verified chain), correcting the stale
   "unmerged"/"draft" description disclosed in this filing's own Preflight without rewriting it.
4. **One additive gate, `xasset0009-gld-cash-like-economic-assessment-content-authorization`**, recording
   this filing's own branch and PR number — `status: in_progress`, **not** `status: complete`, since this
   filing's own governance PR is itself unmerged, unreviewed, and unaccepted, matching every prior filing's
   identical discipline in this chain.
5. **`blocker` and `next_action` updated** to state plainly: `XASSET-0007`'s own overlap-model content
   implementation is complete and merged (`PR #292`); `XASSET-0008` is merged and effective; this filing,
   once merged, authorizes exactly one future economic-assessment content implementation PR covering `GLD`
   and `CASH_LIKE_CAPITAL`; `DEBT_REDUCTION` economic assessment, the `CASH`/`RESERVE` consolidation
   question, and every other remaining `WS-0014` item (steps 2, 8–13 per `XASSET-0001` §J's own numbering)
   remain wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`) is
changed. `WS-0005` and `WS-0015` are not touched by this filing.

### H. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder
change; any trade or order; any chart use of any kind; any buy/sell/hold/trim/exit/wait/stage recommendation
or directive of any kind; population of any `economic_assessment` record by this filing itself; creation of
`intelligence/economic_assessment/` or any file inside it; any validator or test implementation; any
economic finding, categorical or otherwise, for `GLD` or `CASH_LIKE_CAPITAL`; any claim of distinct
`CASH`-versus-`RESERVE` economic purpose; resolution of `RESERVE.yaml`'s own `functional_role` abstention;
any edit to `CASH.yaml`, `RESERVE.yaml`, `GLD_DEFENSIVE_ROLE.yaml`, or `GLD.yaml`; any consolidation of the
`CASH`/`RESERVE` `targets.yaml` rows; any `DEBT_REDUCTION` economic-assessment methodology or content; any
resolution of any sealed functional-doctrine record's forced `economic_assessment_readiness.status`; any
overlap-model dimension computation or edit of any kind; any cross-asset opportunity-cost synthesis; any
Level 1 sleeve or Level 2 instrument sizing; and any edit to `XASSET-0001`, `XASSET-0005`, `XASSET-0006`,
`XASSET-0007`, or `XASSET-0008`'s own text.

### I. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index row);
(3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §G updates); (4) `CLAUDE.md` (one concise Decisions
Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count
assertions, 104→105, made stale by this filing's own new row). No supporting audit artifact is created —
`XASSET-0008` and its supporting artifact already contain the complete accepted process specification for
the economic-assessment schema, and restating it in a second retained document would duplicate content
rather than add evidence, matching `XASSET-0003`'s, `XASSET-0004`'s, and `XASSET-0006`'s own identical
determination. No `intelligence/` company, theme, relationship, classification, reconciliation,
recommendation, contender, ETF-classification, crypto-classification, functional-doctrine, overlap-model,
valuation-archetype, valuation-evidence, or valuation-results file; no `targets.yaml`/`holdings.yaml`/
`gates.yaml`/`issuer_lookthrough.yaml`; and no production allocator/margin code is touched.

### J. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This session does not review its own
work, mark it ready, merge it, or post principal acceptance. Nothing in this decision becomes effective
until this governance PR merges to `main` — including the authorization in §A, which the future
implementation session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0008` already carries a complete,
independently reviewed (three review rounds across two correction cycles), principal-accepted, merged, and
post-merge-verified specification for every schema, evidence, sequencing, and validator control the
economic-assessment methodology needs. Re-deriving or rephrasing that content here would introduce exactly
the kind of drift risk this repository's own review history has repeatedly demonstrated is not
hypothetical — the smaller and more reliable move is to bind the future implementation to `XASSET-0008`'s
own text by reference, unchanged.

**Why this filing authorizes both `GLD` and `CASH_LIKE_CAPITAL` content in one filing, not two.**
`XASSET-0008` designed one shared schema (one validator module, `XASSET-0008` supporting artifact §11)
covering two population members, not two separate frameworks that happen to share a filing — the structural
shape `XASSET-0006` already used for the functional-doctrine sleeve's own four-type population, not the
shape `XASSET-0002`→`XASSET-0003`+`XASSET-0004` used for two genuinely independent frameworks (ETF, crypto).
Splitting this filing into a `GLD`-only and a `CASH_LIKE_CAPITAL`-only authorization would fragment one
already-unified schema and duplicate the same binding table twice for no review benefit.

**Why the stale `WS-0014` gate is disclosed and additively corrected, not silently rewritten.** This
repository's own established convention (`OPS-0009`, and every prior additive-fold-forward gate in this
chain) treats a prior filing's own historical gate text as an append-only record, never edited after the
fact — even when that text is later found stale, as `XASSET-0008`'s own gate description was here, because
`PR #292`'s authoring session branched from a lineage that had already merged `XASSET-0008` but had no
occasion to update the unrelated gate describing it. Disclosing this plainly and adding a new, accurately
dated gate — rather than quietly editing the old one — preserves the audit trail exactly as this
repository's own convention requires.

**Why the two evidence-sufficiency preservations (`RESERVE`'s non-blocking abstention, the three unanswered
GLD research questions) are restated rather than resolved by this filing.** Resolving either here would
exceed this filing's own authorization-only scope — `XASSET-0008` §J/§D.6 and supporting artifact §7 point
5 already reserve those determinations to the drafting session under independent review, not to a
governance-authorization filing that performs no drafting of its own. Restating them plainly here (§C)
ensures the future implementation session inherits the constraint without having to re-derive it from
`XASSET-0008`'s own longer text.

## Alternatives Considered

- **Split into two separate authorization filings, one for `GLD` and one for `CASH_LIKE_CAPITAL`.**
  Rejected — see Rationale; `XASSET-0008` designed one shared schema, not two independent frameworks;
  splitting would fragment it for no review benefit, unlike the genuine `XASSET-0002`→`XASSET-0003`+
  `XASSET-0004` split, which separated two structurally distinct frameworks.
- **Combine this authorization with economic-assessment content in one PR**, matching several smaller
  Company Intelligence batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected —
  `XASSET-0008`'s own stage-separation rule (§A) and `XASSET-0001` §J's separation rule both require content
  to follow its own separate authorization and implementation lifecycle, matching `XASSET-0003`'s,
  `XASSET-0004`'s, and `XASSET-0006`'s own identical treatment, not the smaller-batch pattern used for an
  already-proven equity framework.
- **Silently edit the stale `xasset0008-gld-cash-reserve-economic-assessment-methodology-design` gate's own
  text in place**, since it is now known to be inaccurate. Rejected — this repository's own established
  never-silently-rewrite convention requires an additive correction gate instead (§G), preserving the
  original text as an accurate record of what the `PR #292` authoring session actually knew at the time.
- **Resolve `RESERVE`'s abstention or answer one of the three GLD research questions in this filing**,
  since both are already disclosed as open. Rejected — this filing performs no drafting and has no
  evidence-gathering authority of its own; forcing either here would itself be the "force a value merely to
  fill the record" failure mode `XASSET-0008`'s own design exists to prevent.
- **Create a retained audit artifact restating `XASSET-0008`'s process specification.** Rejected —
  `XASSET-0008` and its supporting artifact are themselves the retained, accepted specification; a second
  document repeating it would be redundant, not additive, matching `XASSET-0003`'s, `XASSET-0004`'s, and
  `XASSET-0006`'s own identical determination.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded economic-assessment
content implementation PR covering both analytical subjects (`GLD`, `CASH_LIKE_CAPITAL`), bound exactly to
`XASSET-0008`'s specification per §A–F above, gated on its own full independent-review/correction/re-review/
principal-acceptance/merge/post-merge-verification lifecycle; two additive Lane M fold-forward gates
(`PR #292`'s and `PR #287`'s own confirmed post-merge state); the
`xasset0009-gld-cash-like-economic-assessment-content-authorization` gate transitioning to
`status: in_progress` recording this filing as underway; `WS-0014`'s ordinary self-reference
synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** population of any
`economic_assessment` record; any economic finding, categorical or otherwise, for `GLD` or
`CASH_LIKE_CAPITAL`; any claim of distinct `CASH`-versus-`RESERVE` economic purpose; resolution of
`RESERVE.yaml`'s own `functional_role` abstention; any edit to `CASH.yaml`, `RESERVE.yaml`,
`GLD_DEFENSIVE_ROLE.yaml`, or `GLD.yaml`; any consolidation of the `CASH`/`RESERVE` `targets.yaml` rows; any
`DEBT_REDUCTION` economic-assessment methodology or content; any resolution of any sealed functional-
doctrine record's forced `economic_assessment_readiness.status`; any overlap-model dimension computation or
edit of any kind; any cross-asset opportunity-cost synthesis; any Level 1 sleeve or Level 2 instrument
sizing; any validator or test implementation; any edit to `XASSET-0001`, `XASSET-0005`, `XASSET-0006`,
`XASSET-0007`, or `XASSET-0008`'s own text; and any tier/target/holdings/role/cluster/cap/gate/allocator/
margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine/overlap-model/
valuation-archetype/valuation-evidence/valuation-results record, byte-for-byte, including all four sealed
functional-doctrine records (`CASH.yaml`/`RESERVE.yaml` included) and GLD's own sealed ETF classification;
all ten sealed overlap-model dimension records, including `defensive_offset_interface`'s own forced
`not_yet_computable_interface_only` value; `XASSET-0001` through `XASSET-0008`'s own accepted text and
scope, in full, unedited; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `levels.py`, `margin_state.py`; the 1.8x leverage cap and 30% margin-buffer floor; `WS-0005`'s
completed, `status: complete` state; `WS-0015`'s own live state; `WS-0014`'s own `status: proposed`/
`priority: secondary`.

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded two-subject content authorization does not narrow
that fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery; QQQ and any other future ETF candidate
expansion; ETF and crypto economic/valuation methodology; equity Stage-4 valuation execution beyond the
sealed 27-company cohort; `DEBT_REDUCTION` economic assessment; whether `CASH`/`RESERVE` should ultimately
be consolidated (`XASSET-0008` §N); cross-asset opportunity-cost synthesis; Level 1 sleeve allocation;
Level 2 instrument allocation; `CHART-0003` and any remaining governed chart ingestion; ladder/deployment
integration; unlevered testing; margin/leverage-policy review; monitoring/sell discipline; final
integration and audit; and any true whole-universe allocation test.
