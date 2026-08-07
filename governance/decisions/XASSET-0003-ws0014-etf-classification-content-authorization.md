---
decision_id: XASSET-0003
date: 2026-08-07
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0004, TIER-0005, TIER-0007, TIER-0009, REL-0001, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002]
supporting_artifact: null
file: governance/decisions/XASSET-0003-ws0014-etf-classification-content-authorization.md
---

## Context

### Authority for this unit

`XASSET-0002`'s own unlettered "Numbering note" paragraph, within its `## Decision` section (`XASSET-0002`
uses no lettered `§A`–`§M` sections anywhere — only unlettered `##`/`###` Markdown headers; only its
supporting artifact uses numbered `§1`–`§11` sections, cited as such throughout this filing), states,
verbatim: "ETF classification (§I item 5 / §J step 4)... require[s] its own
separate, future, explicit principal authorization and independent-review lifecycle, and this filing
does not combine, foreshadow, or pre-stage either." The supporting artifact's §7 restates this as a
binding future-lifecycle rule: "ETF classification content is its own future, separate implementation
PR — never combined with this design filing, never combined with crypto classification content." This
filing is that separate, future, explicit authorization for ETF classification content specifically. It
authorizes; it does not classify.

This mirrors this repository's own established design-then-authorize-content sequencing for the
adjacent equity pipeline: `TIER-0001`/`TIER-0002` designed the four-axis equity framework; `TIER-0004`
specified the population/redaction/sequencing/sealing mechanics; `TIER-0005` then authorized — as its
own separate filing, with zero classification content — the Milestone 6 implementation PR that actually
classified the 27 equities. `XASSET-0002` plays the combined role of `TIER-0002`+`TIER-0004` for the ETF
framework (it already specifies population-scale mechanics, contamination analysis, a validator
specification, and a test specification in one filing — see `XASSET-0002`'s own Rationale for why one
filing sufficed at this population scale). This filing plays `TIER-0005`'s role: authorization only,
binding by reference to the already-accepted design, no restatement, no redesign.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/etf-classification-content-izagzk`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `f06dc014dd61ee00d68155b196642bbb40dc87ee` — `XASSET-0002`'s own merge commit (PR #268).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #268` independently re-confirmed in full** via the GitHub API, not taken from any prior
  summary: `merged: true`, merge commit `f06dc014dd61ee00d68155b196642bbb40dc87ee` (parents
  `bb909532b9329e22d509180b2f308103f3594fa0` and `9fe25c2ae61eb495f15ca067b6f6a16e4a622225`,
  merge-commit tree confirmed byte-identical to the accepted head's own tree per the retained
  post-merge-verification comment); two independent review rounds (`pullrequestreview-4885506171`
  CHANGES REQUIRED — 0 BLOCKING / 2 MAJOR / 0 MINOR; `pullrequestreview-4885709287` delta —
  **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 1 non-blocking MINOR at
  corrected head `9fe25c2ae61eb495f15ca067b6f6a16e4a622225`); one bounded correction
  (`issuecomment-5220693309`, resolving a phantom numeric "tracking-difference companion" field claim
  and a WS-0014 §I/§J roadmap-numbering self-contradiction across three files — both independently
  reconfirmed genuinely resolved by the delta review); one PR-description synchronization
  (`issuecomment-5220870934`); principal acceptance (`issuecomment-5220923953`, accepted head
  `9fe25c2ae61eb495f15ca067b6f6a16e4a622225`); post-merge verification (`issuecomment-5220989275`,
  6-file scope, all seven pre-existing validators clean, full suite 3091/0, decision catalog
  91/`issues == ()`, zero protected-path diff, merge-commit CI run `31209335772` `success`). All
  independently re-fetched and re-read this session, not inferred from any prior summary.
- **`PR #268`'s own post-merge-verification comment explicitly deferred two field updates**:
  `WS-0014`'s `active_pr`/`last_verified_main_sha` fields were left pointing at PR #268's own pre-merge
  state, "deferring that specific factual sync to the next filing that substantively touches
  `WS-0014`." This filing is that next filing — §I performs the deferred synchronization.
- **`XASSET-0001` and `XASSET-0002` (plus its supporting artifact) read in full this session** — not
  summarized from memory. `XASSET-0002`'s supporting artifact §7 point 2 ("ETF classification content
  is its own future, separate implementation PR"), §8 (13-point validator specification), and §9 (test
  specification) are the controlling text this filing binds to (§B below).
- **`targets.yaml` independently re-read**: exactly four `asset_class: fund` rows in `destination:` —
  `SPY` (15.00%), `VEA` (7.00%), `VWO` (1.00%), `GLD` (4.00%) — zero drift from `XASSET-0002`'s own
  stated population. No fifth fund row exists.
- **`issuer_lookthrough.yaml` independently re-read**: `funds:` entries across every issuer row name
  only `SPY`, `VEA`, `VWO` — `GLD` is confirmed absent from every constituent-bearing fund reference,
  consistent with `XASSET-0002`'s supporting artifact §5's own GLD determination.
- **`intelligence/contenders/registry.yaml` independently re-read**: `SPY`, `VEA`, `VWO`, `GLD` each
  carry `asset_type: fund`, `primary_disposition: requires_research`, `classification_exists: false`,
  `current_holding: true`, `current_target: true` — set before `XASSET-0002`'s framework existed
  (`CONTENDER-0002`'s own screening predates it), correctly recording that no fund-specific evidence
  or classification currently exists, not a blocker to this authorization (a screening disposition
  records evidence state, not permission — `CONTENDER-0001` §L: "Contender status creates evaluation
  eligibility only... no... policy... authority"). `QQQ` carries `primary_disposition:
  benchmark_or_index` and `current_target: false` — independently confirmed absent from
  `targets.yaml`'s `destination:` list (referenced only as `regime_ticker`, an informational trend
  indicator, not a holding or target) — correctly excluded from the authorized population (§A).
- **No `intelligence/etf_classification/` directory, no ETF classification content of any kind,**
  independently reconfirmed absent from the repository — this filing is the first to name that future
  path.
- **Decision catalog independently rebuilt**: **91 decisions, `issues == ()`** at the starting head,
  91 `.md` files in `governance/decisions/` (excluding `README.md`) reconciling 1:1. `XASSET-0003`
  confirmed the next unused identifier in the `XASSET-####` series (only `XASSET-0001`/`XASSET-0002`
  exist) — the direct continuation of `XASSET-0002`'s own roadmap step, not a genuinely new decision
  domain, matching the `CONTENDER-0001`→`CONTENDER-0002` and `TIER-0004`→`TIER-0005` continuation
  precedent.

No condition met a Stop bar. This unit proceeded.

## Decision

This filing does two things, in one bounded PR:

1. **Reconfirms (Lane M) that `XASSET-0002`'s own implementation PR (#268) is fully merged, reviewed,
   corrected, principal-accepted, and post-merge verified**, and performs the two field updates that
   PR's own post-merge-verification comment explicitly deferred (`active_pr`, `last_verified_main_sha`)
   plus one new additive gate entry recording the confirmed state — no edit to any existing gate's own
   historical text (§I).
2. **Authorizes exactly one future, separate, bounded ETF classification (blind-classification content)
   implementation pull request**, covering all four canonical fund destinations under the exact
   population, evidence, sequencing, abstention, GLD-scope, contamination, and validator/test controls
   already specified and accepted through `XASSET-0002`. It performs no classification itself, creates
   no classification record or validator, and implements no `intelligence/etf_classification/` content.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007` §1),
any required bounded correction and re-review, explicit principal acceptance, merge, and post-merge
verification — the same lifecycle every prior filing in this chain has followed — may proceed to:

1. Draft and seal one ETF classification record for each of the four canonical fund destinations named
   in `targets.yaml`'s `destination:` list — `SPY`, `VEA`, `VWO`, `GLD` — zero exclusions, zero
   additions. `QQQ` is explicitly excluded (§ Preflight): it is not a `targets.yaml` destination row, is
   not a current holding or target, and carries `primary_disposition: benchmark_or_index` in the
   contender registry.
2. Use a single implementation pass covering all four instruments (no per-fund PR structure; no
   multi-shard isolation apparatus of any kind) — `XASSET-0002`'s own Rationale independently
   determined shard isolation unnecessary at this population scale (ETF ≤ 4), and this filing makes that
   determination binding rather than re-litigating it. If the eligible fund population grows before this
   authorization is exercised, the implementing session must reconfirm that determination still holds
   before proceeding (`XASSET-0002`'s own disclosed NOTE) — and disclose the reconfirmation in the
   implementation PR rather than silently assuming it.
3. Build exactly one ETF classification validator (or one shared-envelope-helper module plus one
   ETF-specific validator, if the future crypto content authorization reuses the shared helpers — that
   determination belongs to whichever authorization is filed second, not to this filing) and its
   dedicated test file, per `XASSET-0002`'s supporting artifact §8/§9.
4. Stop after the first instrument, without a separate pilot authorization, if a systemic schema,
   evidence, or contamination defect is discovered — an internal stop-and-fix condition within the one
   authorized implementation PR, not a license to split into a second governance filing or a
   per-instrument PR structure.

**No crypto classification content of any kind is authorized by this filing.** Crypto classification
requires its own separate, future, explicit authorization and its own separate implementation PR,
per `XASSET-0002`'s supporting artifact §7 point 3/point 5 — this filing does not combine, foreshadow, or pre-stage it, and
an ETF-classification implementation PR authorized here must not classify BTC, ETH, or SOL under any
circumstance.

### B. Binding specification — by reference, not restatement

The implementation PR must follow `XASSET-0002`'s specification exactly, as accepted and merged at
`f06dc014dd61ee00d68155b196642bbb40dc87ee`. This filing does not redesign, loosen, tighten, or restate
that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section (all `XASSET-0002 §N` citations below refer to `XASSET-0002`'s supporting artifact, `governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_DESIGN_20260807.md` — `XASSET-0002`'s own decision file uses no numbered or lettered sections) |
|---|---|
| 4-instrument population, zero exclusions, `QQQ` explicitly out | This filing §A, cross-checked against `targets.yaml`'s live `destination:` list at implementation time |
| Seven-field ETF schema (`structural_role`, `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`, `evidence_quality`) — no fifth substantive axis beyond the six named, no score, no ranking formula, no target percentage, no weighting formula, no buy/sell/hold/trim/exit signal | `XASSET-0002` supporting artifact §3 (frozen by that filing's own acceptance) |
| Method: narrative-judgment axes kept separate from mechanically-computed axes; no standalone "uncertainty axis" — `evidence_quality` is the one axis that summarizes uncertainty | `XASSET-0002` supporting artifact §2 |
| Permitted inputs / forbidden answer-key inputs — the fund's own prospectus/fact-sheet/index-methodology/cost-and-tracking disclosures; `issuer_lookthrough.yaml`'s `fund_holding_weight` entries for the mechanical `overlap_and_concentration` rollup only; `targets.yaml`'s existing row permitted only for symbol identity, **never** for `target_pct`; no chart-domain content in any form; no `conviction`/`portfolio_role_ref`-style policy language of any kind (no such field exists for a fund today, but the prohibition is explicit regardless) | `XASSET-0002` supporting artifact §3.2 (per-axis evidence-input and prohibited-inference statements), §6.2 |
| GLD structural-only treatment — `structural_role`, `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology` must reach a real determination or a genuine `unable_to_determine`; `constituent_exposure` and `overlap_and_concentration` are expected to resolve `not_applicable` as a genuine structural fact, not a schema failure. **No functional/defensive/ballast role determination for GLD is authorized by this filing or by any implementation it authorizes** — that remains reserved to a fully separate, future, functional-doctrine unit under `XASSET-0001` §D | `XASSET-0002` supporting artifact §5 |
| Judgment-before-mechanical-rollup sequencing — `structural_role`/`constituent_exposure`/`cost_and_tracking_quality`/`liquidity`/`structure_and_methodology` (narrative/evidence-sourced) drafted before `overlap_and_concentration` (mechanical rollup of `issuer_lookthrough.yaml`) is computed, mirroring `TIER-0002`'s judgment-before-`risk_concentration` sequencing | `XASSET-0002` supporting artifact §2, §3.2 |
| Abstention discipline — two genuinely distinct semantics (`not_applicable` for a structurally absent axis; `unable_to_determine`, always with a required `abstention_reason`, for a genuine evidence gap); abstention does not cascade between axes | `XASSET-0002` supporting artifact §3.3 |
| Shared cross-asset-handoff envelope (`instrument_id`, `asset_type: etf`, `schema_version`, `provenance`, `evidence_quality_status`, `uncertainty_summary`, `structural_risk_flags`, `record_status`, `valuation_and_economic_assessment_readiness`, `cross_asset_handoff`, `abstention_index`) — every summary field a read-only copy of an already-computed axis value, never independently computed | `XASSET-0002` supporting artifact §6.1, §6.2, §6.4 |
| `valuation_and_economic_assessment_readiness.status` forced to exactly one value, `valuation_required`, on all four records, zero exception — no fair value, target price, `target_pct`, target range, maximum position size, score, or rank anywhere | `XASSET-0002` supporting artifact §6.3 |
| Numeric-field boundary — `cost_and_tracking_quality.expense_ratio_pct` is the **sole** numeric field either framework defines; `tracking_quality_category` is categorical, not numeric (as corrected in `XASSET-0002`'s own bounded-correction round — no "tracking-difference companion" numeric field exists) | `XASSET-0002` supporting artifact §3.2, §6.1 (post-correction text) |
| Validator specification (13 points: exact population enforcement, closed schema at every level with extra-key rejection, asset-type separation, no ETF/crypto schema cross-contamination, no equity-field leakage, no numeric score/rank/target leakage with a scoped exception for `expense_ratio_pct`, independent chart-terminology scan, evidence/provenance validation, abstention requirements, deterministic generation, protected-path isolation, allocator/margin import decoupling, cross-asset policy non-implication) | `XASSET-0002` supporting artifact §8 |
| Test specification (~24-item inventory: happy-path, malformed top-level/instrument, extra/missing keys at every level, wrong `asset_type`, cross-contamination in both directions, forbidden equity-field leakage, invalid evidence citation, abstention behavior including the two-semantics distinction, duplicate/missing/extra instrument against the named population, numeric/score/rank leakage, the `expense_ratio_pct` scoped-acceptance test, chart-terminology leakage per term, directive-language leakage, forced-`valuation_required` violation, envelope-projection-mismatch rejection, determinism, protected-path isolation, allocator/margin import-coupling isolation) | `XASSET-0002` supporting artifact §9, including §9.1's three explicitly carried-forward lessons (extra-key rejection, independent-mechanism verification, no self-declared-flag-without-independent-scan) |
| Batching/future-lifecycle rules — design never recombined with content; ETF and crypto content never share one filing; a schema revision, if ever needed, is its own future, separately authorized design-amendment unit | `XASSET-0002` supporting artifact §7 |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a
genuine ambiguity or gap in `XASSET-0002`'s specification must return for its own separate governance
correction — not resolve it unilaterally inside the implementation PR.

### C. Evidence standard (binding on the future implementation)

The implementing session must use only appropriate fund-classification evidence — official fund
prospectus/fact-sheet material, issuer/index methodology documentation, the fund's own disclosed expense
ratio, holdings/exposure breakdowns, tracking-quality information, liquidity/structure disclosures, and
`issuer_lookthrough.yaml` where actually applicable (SPY/VEA/VWO only, per §B). No evidence may be
invented, assumed by analogy from another fund, or backfilled from a company's own Company Intelligence
record. Where evidence is insufficient for a given axis, the implementation must use the framework's own
abstention path (§B) rather than filling the gap — an axis abstaining on all four instruments is an
honest outcome, not a defect requiring correction. If the implementing session determines that gathering
adequate primary evidence requires research authority beyond what this filing and `XASSET-0002` already
grant (e.g., a live data feed this repository does not have access to), it must stop and disclose that
as a genuine blocker rather than substitute secondary inference for a primary source without disclosure.

### D. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: population drift
(a fifth fund appearing in `targets.yaml`, or one of the four disappearing, since the implementation may
begin some time after this filing merges); any equity-field leakage (`economic_role`, `capital_priority`,
`risk_concentration`, or any `TIER-0002`-shaped field name); any crypto-field leakage on an ETF record;
any numeric score/rank/target leakage beyond the one permitted `expense_ratio_pct` field; any chart-domain
leakage; any attempt to determine GLD's functional/defensive role; any attempt to depart from the forced
`valuation_required` state; any protected-path mutation; or any unexpected target, holdings, gate, cap,
cluster, allocator, margin, ladder, order, or trade change.

### E. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact four-instrument
population (including confirming `QQQ` was correctly excluded and no fifth fund had appeared in
`targets.yaml` since this filing); the exact changed-file inventory; seven-field schema conformance for
every record; abstention validity and non-cascading behavior, including the `not_applicable`-versus-
`unable_to_determine` distinction; sequencing (judgment axes before the mechanical `overlap_and_
concentration` rollup); GLD's structural-only treatment with no functional-role content; the forced
`valuation_and_economic_assessment_readiness: valuation_required` state on all four records; the
envelope's read-only-projection consistency (§6.2's rule); the validator and its tests against `XASSET-
0002` §8/§9's full specification, including the three explicitly carried-forward lessons (§9.1); CI;
protected-path isolation; absence of any crypto content; absence of any cross-asset synthesis, sleeve
target, or instrument target; and absence of any policy mutation. Any correction requires its own fresh
exact-head delta review before principal acceptance.

### F. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **`active_pr` updated `268` → this filing's own PR number**, and **`last_verified_main_sha` updated**
   `bb909532b9329e22d509180b2f308103f3594fa0` → `f06dc014dd61ee00d68155b196642bbb40dc87ee` —
   the exact two fields `PR #268`'s own post-merge-verification comment explicitly deferred to "the
   next filing that substantively touches `WS-0014`." `last_verified_date` updated to this filing's own
   date.
2. **One new additive gate, `xasset0002-post-merge-verification`**, recording `XASSET-0002`'s (PR #268)
   confirmed merge (`f06dc014dd61ee00d68155b196642bbb40dc87ee`), two-round review chain, one bounded
   correction, principal acceptance (`issuecomment-5220923953`), and post-merge verification
   (`issuecomment-5220989275`) — matching the identical Lane M pattern `XASSET-0002` itself applied to
   `CONTENDER-0002`'s stale gate, and the `TIER-0002`/`REL-0002`-`REL-0006`/`PI-0039`/`REL-0007`/
   `TIER-0007`/`TIER-0009`/`TIER-0011` chain before it. The `xasset0002-etf-crypto-framework-design`
   gate's own historical text is left unedited.
3. **One new additive gate, `xasset0003-etf-classification-content-authorization`**, recording this
   filing's own branch and (once it exists) PR number — `status: in_progress`, **not** `status:
   complete`, since this filing's own governance PR is itself unmerged, unreviewed, and unaccepted,
   matching every prior filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: step 3 (ETF + crypto framework design) is
   complete and merged (PR #268); this filing, once merged, authorizes exactly one future ETF
   classification content implementation PR (step 4 of the `§J` roadmap / item 5 of the `§I` list);
   crypto classification content (step 5 / item 7) remains separately, wholly unauthorized; steps 6
   through 12 remain wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`)
is changed — this filing does not begin execution and does not alter the workstream's own standing.

### G. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/
ladder change; any trade or order; any chart use of any kind; any buy or sell recommendation; any
deployment recommendation; crypto classification content of any kind (BTC, ETH, SOL); GLD's functional/
defensive-role determination; any valuation or economic-assessment methodology; any cash/reserve/GLD/
debt functional doctrine; any cross-asset overlap, concentration, or opportunity-cost synthesis; any
sleeve-level or instrument-level sizing; classification of any fund by this filing itself; creation of
`intelligence/etf_classification/` or any file inside it; any sanitized evidence package (none is
required or authorized — `XASSET-0002`'s supporting artifact §7's Rationale determined the equity pipeline's redaction
apparatus does not transfer, since no ETF evidence source embeds portfolio-policy content); any validator
implementation; or any edit to `XASSET-0001`, `XASSET-0002`, or its supporting artifact's own text.

### H. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0014` only — the §F updates); (4) `CLAUDE.md` (one concise
Decisions Log pointer entry); (5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded
decision-catalog-count assertions, 91→92, made stale by this filing's own new row). No supporting audit
artifact is created — `XASSET-0002`'s own supporting artifact already contains the complete accepted
process specification (population-scale contamination analysis, validator specification, test
specification), and restating it in a second retained document would duplicate content rather than add
evidence, matching `TIER-0005`'s own identical determination. No `intelligence/` company, theme,
relationship, classification, reconciliation, recommendation, or contender file; no `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; and no production allocator/margin code is
touched.

### I. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. This session does not
review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this decision
becomes effective until this governance PR merges to `main` — including the authorization in §A, which
the future implementation session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `XASSET-0002` already carries a complete,
independently reviewed (two rounds, two MAJOR findings both resolved), principal-accepted, merged, and
post-merge-verified specification for every schema, evidence, sequencing, and validator control ETF
classification needs. Re-deriving or rephrasing that content here would introduce exactly the kind of
drift risk `XASSET-0002`'s own two MAJOR findings demonstrated a plausible-sounding restatement can
carry (a phantom numeric field claimed in four locations; a roadmap-numbering inconsistency replicated
across three files) — the smaller and more reliable move is to bind the future implementation to
`XASSET-0002`'s own text by reference, unchanged.

**Why implementation is not folded into this same filing.** `XASSET-0002`'s own unlettered "Numbering
note" paragraph and its supporting artifact's §7 are both explicit and unambiguous that ETF classification content requires its own
separate authorization and its own separate implementation lifecycle — this is controlling text this
filing has no discretion to reinterpret. This also matches this repository's own general pattern for a
framework's first-ever content application (`TIER-0004`→`TIER-0005`→separate Milestone 6 implementation)
over the smaller combined-filing pattern used for incremental, already-precedented content batches
(`REL-0002`, `PI-0036`) — ETF classification is the first-ever application of a brand-new framework, not
an incremental batch under an already-proven one.

**Why the population is bounded to exactly four instruments with no per-instrument PR structure.**
`targets.yaml`'s `destination:` list names exactly four fund rows today; `XASSET-0002`'s own Rationale
already determined multi-shard isolation unnecessary at this scale (ETF ≤ 4, contrasted explicitly with
equity Milestone 6's 27-name/five-shard design). This filing makes that determination binding rather
than re-litigating it, while requiring the implementing session to reconfirm it if the population has
grown by the time implementation begins (§A point 2) — the same forward-looking discipline `TIER-0005`
applied to its own binding-by-reference table.

**Why no new supporting audit artifact.** Every fact this filing needs — the accepted ETF schema,
evidence standard, sequencing, GLD treatment, envelope design, and validator/test specification —
already exists in `XASSET-0002`'s merged, reviewed text and its supporting artifact. Creating a second
retained document that restates the same content would violate this repository's own "reference, don't
restate" discipline (`REL-0001`, `PI-0016`, `TIER-0005`) without adding verifiable evidence.

**Why crypto classification is explicitly excluded rather than silently out of scope.** `XASSET-0002`
§7 point 5 requires that ETF and crypto content "never share a filing" — this filing names that
exclusion explicitly (§A, §G) rather than relying on the reader to infer it from the filing's title
alone, matching this repository's own repeated correction history around ambiguous or under-stated
scope boundaries (`XASSET-0002`'s own MAJOR finding on roadmap-numbering ambiguity is the most recent
direct precedent for why an explicit statement is worth the extra sentence).

## Alternatives Considered

- **Combine this authorization with ETF classification content in one PR**, matching several smaller
  Company Intelligence batches' combined-filing precedent (`REL-0002`, `PI-0036`, `PI-0038`). Rejected —
  `XASSET-0002`'s own unlettered "Numbering note" paragraph and its supporting artifact §7 explicitly
  prohibit combining design/authorization with content for either asset type; this is controlling text,
  not a discretionary style choice.
- **Authorize both ETF and crypto classification content in this same filing**, since both frameworks
  were designed together in `XASSET-0002`. Rejected outright — `XASSET-0002`'s supporting artifact §7
  point 5 is explicit that "ETF and crypto content must never share a filing," restated as binding by
  this filing's own §A/§G.
- **Redesign or restate `XASSET-0002`'s specification in this filing's own words**, on the theory that a
  content authorization should be self-contained. Rejected — see Rationale; restatement itself
  introduces drift risk the binding-by-reference table (§B) avoids, and `XASSET-0002`'s own review
  history demonstrates this is not a hypothetical risk.
- **Authorize a partial ETF population first (e.g., SPY only) as a smaller first batch**, mirroring
  early Company Intelligence research waves. Rejected — ETF classification is not open-ended new-ticker
  research; it applies one already-frozen framework to an already-fully-covered, already-small
  population (four instruments) under one already-specified mechanism, so the proportionality concern
  that justified smaller research waves for open-ended ticker discovery does not carry over the same
  way; `XASSET-0002`'s own Rationale already determined a single pass across all four is appropriate at
  this scale.
- **Create a retained audit artifact restating `XASSET-0002`'s process specification for this filing's
  own supporting evidence.** Rejected — `XASSET-0002` and its supporting artifact are themselves the
  retained, accepted specification; a second document repeating it would be redundant, not additive.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded ETF
classification implementation PR covering all four canonical fund destinations (`SPY`, `VEA`, `VWO`,
`GLD`), bound exactly to `XASSET-0002`'s specification per §A-E above, gated on its own full
independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle;
the `xasset0002-post-merge-verification` gate recording `XASSET-0002`'s (PR #268) confirmed state; the
`xasset0003-etf-classification-content-authorization` gate transitioning to `status: in_progress`
recording this filing as underway; `WS-0014`'s deferred `active_pr`/`last_verified_main_sha`
synchronization.

**Not authorized by this filing, now or ever without a further separate decision:** crypto
classification content of any kind; GLD's functional/defensive-role determination; classification of
any fund by this filing itself; any sanitized evidence package; any validator implementation; any edit
to `XASSET-0001`, `XASSET-0002`, or its supporting artifact's own text; any valuation or economic-
assessment methodology; any cash/reserve/GLD/debt functional doctrine; any cross-asset overlap,
concentration, or opportunity-cost synthesis; any sleeve-level or instrument-level sizing; and any
tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation Intelligence record, byte-for-byte; the contender registry; `XASSET-0001`'s and
`XASSET-0002`'s own accepted text and scope, in full, unedited; `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution;
`WS-0005`'s completed, `status: complete` state; `WS-0014`'s own `status: proposed`/`priority:
secondary` (unedited by this filing).

This decision becomes effective only when its implementing pull request merges to `main`.
