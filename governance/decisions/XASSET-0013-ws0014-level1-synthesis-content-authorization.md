---
decision_id: XASSET-0013
date: 2026-08-11
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, REL-0001, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0012, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, VALUATION-0007, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/XASSET-0013-ws0014-level1-synthesis-content-authorization.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly **one bounded Stage-2 governance
filing** that names the exact first population of Level 1 `sleeve_profile` and `sleeve_relationship`
records a future implementation PR may populate under `XASSET-0012`'s already-accepted methodology.
This filing is **authorization only** — it populates no `sleeve_profile` record, no
`sleeve_relationship` record, no evidence-coverage state, no comparative finding, no sleeve weight,
no instrument weight, and no portfolio in/out decision of any kind. It is Stage 2 of the four-stage
sequence `XASSET-0012` §10 defines (Stage 1 methodology design — complete; **Stage 2 content
authorization — this unit**; Stage 3 future implementation/population; Stage 4 future portfolio-policy
adoption, separately authorized).

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`,
  branch `claude/xasset-0013-stage-2-auth-8al8kg`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local branch head and `origin/main` both confirmed
  identical at `79a611cf03350e5d0688eb6b0823f7c0f043b2fe` — independently confirmed via the GitHub
  API (`pull_request_read` on `PR #301`) to be `XASSET-0012`'s own merge commit (parents
  `23b858441ffa822467e493f3328649d2475445c5` — the base, `PR #300`'s own merge commit — and
  `bbfd60784a8dfdb7b4ec2e78b6e350d62a74c7aa` — `PR #301`'s own head), matching the directive's own
  stated SHA exactly.
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`PR #301`'s full lifecycle independently re-verified via the GitHub API, not assumed**: `merged:
  true`, `merged_by: Mast3rkey`, one independent exact-head review round
  (`pullrequestreview-4902959254`, CHANGES REQUIRED — 0 BLOCKING / 3 MAJOR / 3 MINOR / 2
  non-actionable NOTE) plus a second delta review (`pullrequestreview-4906063644`, 0 BLOCKING / 0
  MAJOR / 2 MINOR / 1 non-actionable NOTE) resolved by two bounded corrections, both fully
  reconciled inside `XASSET-0012`'s own decision file Correction History section (independently
  re-read in full, not summarized). Merge-commit CI independently re-fetched: check run
  `93778105836`, `status: completed` / `conclusion: success`.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **109 decisions, `issues == ()`**, reconciling exactly against `governance/decisions.yaml`'s own
  109 rows. `XASSET-0001` through `XASSET-0012` and `CONTENDER-0001` through `CONTENDER-0003` all
  present. **`XASSET-0013` independently confirmed the next unused identifier** — zero matches for
  `XASSET-0013` anywhere in `governance/decisions.yaml` or via full-repository grep.
- **`XASSET-0012` read directly, in full — decision file and supporting artifact** (not summarized
  from memory or from the directive's own paraphrase). Its Stage 1 methodology — the six-sleeve
  taxonomy, the two record types (`sleeve_profile`, `sleeve_relationship`), the closed four-value
  `primary_disposition` vocabulary, the closed three-member `secondary_conditions` set, the
  zero-numeric-field posture, the overlap-citation rule, the `sleeve_subject_scope` shared-manifest
  mechanism (§4.1.1), the sub-field-level abstention roll-up rule (§4.2.1), the forbidden-language
  boundaries (§8/§8.1), and the nineteen-point validator/test specification (§9) — is the exact
  controlling text this filing binds to by reference below. `XASSET-0001` §E/§J (the two-level
  architecture and its sequential-dependency rule) and `REL-0001`'s pairwise-record convention were
  independently re-read to confirm `XASSET-0012` operationalizes both correctly; neither is
  redesigned here.
- **`WS-0014`'s full live entry independently re-read**: `status: proposed`, `priority: secondary`,
  `dependencies: [WS-0005]`. The most recent gate, `xasset0012-level1-sleeve-synthesis-
  methodology-design`, reads `status: in_progress`, `pr: null` — stale as of this session's start,
  since `PR #301` is, in fact, fully merged (see above); §L below synchronizes it without editing
  its own historical text. `active_branch: claude/level-1-cross-asset-synthesis-2m35pg`, `active_pr:
  null`, `last_verified_main_sha: 23b858441ffa822467e493f3328649d2475445c5` — one commit behind the
  current tip; also synchronized.
- **Every sealed Intelligence layer `XASSET-0012` §1 inventories independently re-verified live, not
  trusted from the artifact's own text**: 27 `classification`/`valuation_archetype`/
  `valuation_evidence` records; 27 `valuation_results` records, independently re-tallied at
  **18 `completed` / 9 `partial` / 0 `unable_to_determine`** (exact match); 4 `etf_classification`
  records (SPY, VEA, VWO, GLD); 3 `crypto_classification` records (BTC, ETH, SOL); 4
  `functional_doctrine` records (CASH, RESERVE, GLD_DEFENSIVE_ROLE, DEBT_REDUCTION) —
  `DEBT_REDUCTION.yaml`'s own `economic_assessment_readiness` independently re-read and confirmed
  forced `assessment_required` on **both** `avoided_borrowing_cost_readiness` and
  `survivability_and_buffer_benefit_readiness`; 10 `overlap_model` dimension records, independently
  re-tallied at **6 `computed_from_existing_mechanism`** (`issuer_overlap_etf_lookthrough`,
  `economic_role_overlap`, `correlated_loss_mechanisms`, `sleeve_concentration`,
  `etf_direct_equity_duplication`, `leverage_debt_interaction`) **and 4
  `not_yet_computable_interface_only`** (`crypto_correlation_interface`, `defensive_offset_interface`,
  `geographic_currency_exposure`, `whole_portfolio_volatility_drawdown_concentration`); 2
  `economic_assessment` records (GLD, CASH_LIKE_CAPITAL); 6 `instrument_economic_assessment` records
  (SPY, VEA, VWO, BTC, ETH, SOL); 13 `intelligence/relationships/` records; 2
  `contender_evaluation` records (VRT, WMT, non-canonical); 84-entry
  `intelligence/contenders/registry.yaml`. `intelligence/level1_sleeve_synthesis/` independently
  confirmed **absent** — no Stage 2/3 content exists anywhere in the repository prior to this
  filing.
- **`targets.yaml`'s `asset_class` vocabulary independently re-read**: `equity | fund | crypto |
  reserve | cash` — confirming the six-`sleeve_id` Level 1 taxonomy is a functional layer on top of
  `asset_class`, exactly as `XASSET-0012` §1 states, not re-derived differently here.

### Correction history (this filing, same PR)

**Bounded correction, independent exact-head review (posted as a `COMMENT`, same-account platform
restriction, treated with the same weight as a formal review), anchored to the original head
`0158f31c3465d658c89fdffa8a0f9a7840e0d7a5`, zero BLOCKING / zero MAJOR / 1 MINOR / 2 non-actionable
NOTE, CHANGES REQUIRED:**

1. **MINOR — §J's evidence-limitation disclosure checklist required SOL's own sub-field-level
   drawdown abstention be individually disclosed, but did not carry a parallel requirement for a
   real, independently-confirmed divergence on the sleeve's own inflation-narrative sub-field.**
   The `crypto` ↔ `fund_gld_defensive` pair's own stated justification (§D) rests on a "near-identical
   narrative" match between `GLD.yaml` and `BTC.yaml` — independently re-verified accurate for BTC
   specifically (`GLD.yaml`/`BTC.yaml` both carry `historical_inflation_sensitivity`/`historical_
   inflation_sensitivity_narrative: historically_mixed_or_inconsistent`) — but `ETH.yaml`'s and
   `SOL.yaml`'s own `historical_inflation_sensitivity_narrative` sub-fields both independently
   characterize as `historically_weakly_associated`, diverging from BTC's and GLD's own matching
   value. Without an explicit disclosure requirement, a future Stage 3 drafting session could
   generalize BTC's own narrative match to the whole `crypto` sleeve's rationale against
   `fund_gld_defensive`, misrepresenting ETH's and SOL's own divergent evidence. **Resolved**: §D's
   own `crypto`↔`fund_gld_defensive` bullet now states explicitly that the narrative match is
   BTC-specific and requires the future relationship record's `rationale` to disclose ETH's and
   SOL's own divergent `historically_weakly_associated` characterization; §J gains a parallel,
   explicit checklist entry stating the same requirement, mirroring the treatment already given to
   SOL's own drawdown-behavior abstention.

Both non-actionable NOTEs (the unverified-but-hedged "very likely" transitive-redundancy framing for
the four deferred `fund_broad_market` pairs in §E class 1; the disclosed, reasoned five-of-seven
equity-hub batch concentration) are carried forward unresolved, per the review's own explicit
characterization as non-blocking — the first because the filing's own text already treats the
deferral as a disclosed batching choice with an explicit future-revisit escape hatch, never a claim
that the omitted pairs' conclusions are logically settled; the second because batch composition is a
disclosed design choice, not a defect.

Exact correction-delta file inventory: this file only (§D's `crypto`↔`fund_gld_defensive` bullet,
§J's new checklist entry, this section).

## Decision

### A. What this filing authorizes — content population, not implementation

This filing authorizes exactly one future, separate, bounded implementation PR to populate the exact
`sleeve_profile` and `sleeve_relationship` records named below, plus the manifests, validator(s), and
test suite `XASSET-0012` §9 already specifies. It does not itself populate any record, compute any
evidence-coverage state, cite any overlap dimension, or produce any comparative finding. No
methodology field, vocabulary value, or scan design from `XASSET-0012` is redesigned, expanded, or
narrowed by this filing.

### B. Exact `sleeve_profile` population — all six sleeves

The future implementation may populate exactly six `sleeve_profile` records, one per `sleeve_id`
`XASSET-0012` §2 defines: `equity`, `fund_broad_market`, `fund_gld_defensive`, `crypto`,
`cash_reserve`, `debt_reduction`. Live repository state discloses no integrity blocker against any
of the six — every sleeve's own governed layer(s) exist in sealed form (§ Preflight above) — so all
six are authorized in the first population, matching `XASSET-0006`'s own precedent (all four
functional-doctrine capital-use types authorized together under one shared schema) rather than
`XASSET-0002`→`XASSET-0003`/`XASSET-0004`'s split (which reflected two genuinely distinct
frameworks, not a partial population). Where a sleeve's own governed evidence is thin or partially
forced-abstained (`debt_reduction`'s own `functional_doctrine/DEBT_REDUCTION.yaml`, forced
`assessment_required` on both sub-fields; `crypto`'s own `cross_coin_correlation_status: not_yet_
measured`), the future implementation must populate the profile using `XASSET-0012`'s own
abstention/partial-evidence mechanism — `evidence_coverage_profile: forced_abstention` or
`substantially_computed_with_disclosed_gaps` plus the corresponding `abstention_index[]` entries,
per §4.2/§4.2.1 — never omit the sleeve from the first population and never force a stronger
completeness value than the evidence supports.

### C. Exact `sleeve_relationship` population — seven of fifteen pairs, bounded

The future implementation may populate exactly **seven** `sleeve_relationship` records, alphabetically
filed per `REL-0001`'s convention (`<sleeve_a>_<sleeve_b>.yaml`, `sleeve_a` < `sleeve_b`
lexicographically by `sleeve_id`):

| # | Filename | Pair |
|---|---|---|
| 1 | `cash_reserve_debt_reduction.yaml` | `cash_reserve` ↔ `debt_reduction` |
| 2 | `cash_reserve_equity.yaml` | `equity` ↔ `cash_reserve` |
| 3 | `crypto_equity.yaml` | `equity` ↔ `crypto` |
| 4 | `crypto_fund_gld_defensive.yaml` | `crypto` ↔ `fund_gld_defensive` |
| 5 | `debt_reduction_equity.yaml` | `equity` ↔ `debt_reduction` |
| 6 | `equity_fund_broad_market.yaml` | `equity` ↔ `fund_broad_market` |
| 7 | `equity_fund_gld_defensive.yaml` | `equity` ↔ `fund_gld_defensive` |

This is **not** all fifteen `C(6,2)` pairs — a bounded first batch, matching `XASSET-0012` §3's own
explicit permission and `CONTENDER-0003`'s own two-of-nineteen bounded-pilot precedent. It is also
not merely the five equity-anchored pairs the directive floated as a starting example — two
non-equity pairs (rows 1 and 4) are independently determined necessary below, not adopted by
default.

### D. Why each authorized pair is required for a genuinely useful first synthesis

**Equity-anchored pairs (rows 2, 3, 5, 6, 7)** — `equity` is the dominant risk-capital sleeve (27
canonical names, the only sleeve with a full four-layer valuation stack) and the natural pivot for a
first opportunity-cost pass, but each of the five pairs against it tests a *functionally distinct*
capital use, not a repetition:

- **`equity` ↔ `fund_broad_market`** (row 6) — two structurally different vehicles for the same
  broad risk-capital-deployment function (individual-name selection vs. passive index exposure);
  `fund_broad_market`'s own SPY row alone is `targets.yaml`'s single largest position (15.00%
  target). Establishing whether these compete for the same marginal dollar, or occupy genuinely
  distinct roles, is foundational to reading every other pair correctly.
- **`equity` ↔ `fund_gld_defensive`** (row 7) — the portfolio's own explicit growth-versus-ballast
  doctrine (`CLAUDE.md`: "GLD does the ballast job bonds would"). This is the single most load-bearing
  `role_preserving` test case in the batch and must be evaluated directly, not inferred.
- **`equity` ↔ `crypto`** (row 3) — both growth-oriented sleeves, but with a materially different
  evidence-maturity profile: `crypto` carries no `valuation_archetype`/`valuation_evidence`/
  `valuation_results` layer at all, and its own `correlation_and_volatility.cross_coin_correlation_
  status` is structurally forced `not_yet_measured` on all three sealed records. This is the batch's
  clearest candidate for a genuine `stronger_evidence_maturity` finding and must be tested directly.
- **`equity` ↔ `cash_reserve`** (row 2) — the classic deployed-versus-idle-capital question, directly
  underlying the allocator's own "RESERVE/CASH — never a buy candidate, definitionally satisfied"
  gap-filling logic; `cash_reserve`'s own `RESERVE.yaml` carries a sealed `functional_role: unable_to_
  determine` abstention worth surfacing explicitly rather than left buried in a functional-doctrine
  record no synthesis-level reader would otherwise consult.
- **`equity` ↔ `debt_reduction`** (row 5) — the deploy-versus-deleverage question sitting at the heart
  of this portfolio's own margin doctrine (1.8x leverage cap, 30% buffer floor). `debt_reduction`'s
  own `DEBT_REDUCTION.yaml` is forced `assessment_required` on both `economic_assessment_readiness`
  sub-fields — this pair will very likely land at `unable_to_determine` or carry heavy secondary
  flags, and that is itself the valuable, honest disclosure a first synthesis exists to produce, not
  a reason to omit the pair.

**Non-equity pairs, independently determined necessary (rows 1, 4)**:

- **`crypto` ↔ `fund_gld_defensive`** (row 4) — both sleeves carry a real, sourced "alternative/
  inflation-hedge" narrative in their own governed evidence (`GLD.yaml`'s own `historical_
  inflation_sensitivity`/`historical_equity_drawdown_behavior` sub-fields; `BTC.yaml`'s own near-
  identical `historically_mixed` drawdown characterization and matching `historically_mixed_or_
  inconsistent` inflation-narrative characterization). Without a direct comparison, a reader would
  be left to infer a crypto-versus-GLD relationship transitively through two separate equity-anchored
  pairs — exactly the kind of unsupported inference a first synthesis should close directly rather
  than leave open. This is not one of the three pairs the directive floated as an example; it was
  selected independently because it answers a question the equity-anchored batch cannot. **This
  narrative match is BTC-specific, not sleeve-wide, and the future implementation must disclose that
  explicitly**: `ETH.yaml`'s and `SOL.yaml`'s own `historical_inflation_sensitivity_narrative` sub-
  fields both independently characterize as `historically_weakly_associated` — diverging from BTC's
  and GLD's own matching `historically_mixed_or_inconsistent` value — exactly the kind of sub-field-
  level divergence §4.2.1's roll-up rule already requires be individually visible, restated here as
  a binding disclosure requirement on this specific relationship record's own `rationale`, not merely
  left to the general rule (§J below).
- **`cash_reserve` ↔ `debt_reduction`** (row 1) — the one non-equity pair with a directly documented,
  live capital-competition question in this repository's own governed doctrine: un-deployed cash
  could instead pay down margin debt, or margin debt could be preserved specifically to sustain the
  30% buffer floor. Neither equity-anchored pair (`equity`↔`cash_reserve`, `equity`↔`debt_reduction`)
  tests whether cash and debt-reduction compete for the *same* marginal dollar — only this pair does.
  Given `debt_reduction`'s own forced-abstained evidence base, this pair will likely surface a
  meaningful `forced_abstention_present`/`unable_to_determine` finding — a genuine, high-priority gap
  worth disclosing explicitly rather than leaving buried in two separate functional-doctrine records.

### E. Deliberately omitted pairs — three classes, safe to defer

The remaining eight of fifteen pairs are deliberately omitted from the first batch, grouped by why
each class is safe to defer rather than treated as an oversight:

1. **`fund_broad_market` paired with `fund_gld_defensive`, `crypto`, `cash_reserve`, and
   `debt_reduction`** (4 pairs). `fund_broad_market` occupies the same broad-risk-capital-deployment
   functional role `equity` already tests against every other sleeve in rows 2/3/5/7; a direct
   `fund_broad_market` comparison against each non-equity sleeve would very likely reach the same
   disposition class already established transitively (both `equity` and `fund_broad_market` are
   risk-capital-deploying sleeves relative to `crypto`/`debt_reduction`/`fund_gld_defensive`/
   `cash_reserve`, for the same underlying functional reason). Populating near-duplicate findings in
   a *first* batch adds cost without adding a distinct answer; if the equity-anchored batch surfaces
   a genuinely non-obvious divergence between `equity`'s and `fund_broad_market`'s own evidence
   posture, a future batch can add the specific pair that matters — this is the directive's floated
   `fund_broad_market` ↔ `cash_reserve` example, generalized and rejected on the same reasoning
   across all four of `fund_broad_market`'s remaining pairs, not merely the one named.
2. **`fund_gld_defensive` paired with `cash_reserve` and `debt_reduction`** (2 pairs). Both members of
   each pair already occupy a defensive/preservation-oriented functional space relative to the growth
   sleeves — a first-pass comparison strictly among defensive-postured sleeves does not surface a live
   capital-competition question this portfolio's own governed doctrine currently poses, unlike
   `equity`↔`cash_reserve` or `cash_reserve`↔`debt_reduction`, both of which have a directly
   documented, real tension in `CLAUDE.md`'s own margin/allocator doctrine.
3. **`crypto` paired with `cash_reserve` and `debt_reduction`** (2 pairs). `crypto`'s own sleeve is
   populated exclusively through the allocator's own deposit/gap-filling logic and the Standing
   Queue's own crypto-sleeve-rebuild instruction — never by drawing down cash/reserve or as an
   alternative to a margin-paydown decision. No governed doctrine currently frames `crypto` and
   `cash_reserve`/`debt_reduction` as competing for the same marginal dollar the way `equity` and
   `debt_reduction` demonstrably do (margin-funded equity buys are explicit, documented doctrine;
   margin-funded crypto buys are not).

No omitted pair is silently dropped — each is named here, by class, with the specific reason it may
safely wait, matching `XASSET-0012` §3's own "disclosing exactly which pairs are covered and which
are deferred — never silently treating partial coverage as complete" requirement.

### F. First-batch completeness determination

Six profiles plus these seven relationships are sufficient to answer, for a genuinely useful first
synthesis, every question `XASSET-0012`'s own design targets: what role each sleeve currently serves
(the six profiles); which sleeve relationships materially compete for capital (rows 2, 3, 5, 6 test
`equity`'s own competing uses directly; row 1 tests the portfolio's own live cash-versus-debt
tension); where evidence supports relative maturity (rows 3 and 5 are the batch's clearest
`stronger_evidence_maturity` candidates); where role preservation or coexistence is more appropriate
(row 7 is the load-bearing growth-versus-ballast test; row 4 closes the crypto-versus-gold narrative
gap the equity-anchored pairs cannot); where evidence is insufficient (rows 1 and 5 both touch
`debt_reduction`'s own forced-abstained evidence base); and where partial or abstained evidence
constrains confidence (`secondary_conditions` on every row touching `crypto`, `cash_reserve`, or
`debt_reduction`). This batch does not, and is not required to, produce a total ranking of all six
sleeves — `XASSET-0012` §7's own portfolio-selection boundary forecloses that outcome regardless of
batch size.

### G. Structural-reference binding — by reference to `XASSET-0012`, not restated

The future implementation must use exactly the mechanisms `XASSET-0012` already specifies, with no
substitute or shortcut:

- **Layer structural references** — `XASSET-0012` §4.1's aggregate, layer-scoped-by-default design
  (population count, aggregate status tally, one manifest-level or single-record hash pin per input
  layer named in §1's inventory), never a per-instrument reference inside a sleeve profile except
  where §4.1.1 requires it.
- **`sleeve_subject_scope`** (§4.1.1) — required, without exception, on every `sleeve_profile`
  entry referencing `intelligence/etf_classification/` (the one live shared-manifest layer, split
  between `fund_broad_market` {SPY, VEA, VWO} and `fund_gld_defensive` {GLD}) — a hard schema
  failure if omitted, live-cross-checked against both the source manifest's real population and
  §2's fixed sleeve-to-subject mapping table.
- **Live canonical hashes** — every structural, profile, and overlap-dimension reference hash is
  live-recomputed via the cited module's own `canonical_record_hash()` function at validation time,
  never trusted from a stored value, matching every reference in this repository's own established
  discipline.
- **`evidence_coverage_profile`** (§4.2) — mechanically derived from the referenced layer's own
  current aggregate state, never self-declared by a drafting session.
- **`abstention_index[]`** (§4.2.1) — every sub-field-level abstention (e.g. `crypto`'s own
  `cross_coin_correlation_status: not_yet_measured`) independently scanned and echoed, never
  silently absorbed by an otherwise-`sealed` parent record.
- **Existing overlap references** — `overlap_or_duplication_disclosed` may cite only the six
  `overlap_model` dimensions currently `computed_from_existing_mechanism` (§5.3); citing one of the
  four `not_yet_computable_interface_only` dimensions as evidence of overlap is a hard validator
  failure, not a drafting judgment call.
- **Existing evidence-quality/status data** — every judgment field draws only on already-sealed
  Intelligence layers named in §1's inventory; no new primary research, no fabricated evidence, no
  citation of `intelligence/contender_evaluation/` or `intelligence/contenders/registry.yaml` (§7).

### H. Carried-forward review NOTE — mandatory adversarial probe before push

`XASSET-0012`'s own final delta review (`pullrequestreview-4906063644`) carried one non-blocking
NOTE, explicitly deferred rather than resolved: a handful of natural-language eligibility/inclusion
phrase paraphrases (the review's own examples: "crypto is eligible for portfolio inclusion,"
"exclude gold from portfolio") sit just outside §8.1's current literal phrase list and were flagged
as "appropriate to flag for the future implementing session's own mandatory adversarial-test-writing
pass, not a defect in this design-stage filing." **This Stage 2 filing does not redesign or harden
§8.1's scan** — that would exceed this filing's own authority and would itself require its own
future, separate `XASSET-####` amendment if a genuine defect is found. It instead requires, as a
binding condition on the future implementation PR: before any code is pushed, the implementing
session must write adversarial test cases specifically probing this exact vulnerability class
(natural-language eligibility/inclusion paraphrases that avoid §8.1's literal phrase list while
still asserting a portfolio-membership conclusion) against the real §8.1 scan as built, and must
disclose the result — whether the scan catches the paraphrase class, or whether a genuine gap is
found and must be escalated as its own finding rather than silently patched. This is a probe
requirement, not a redesign authorization.

### I. Boundaries restated, unweakened

- **Contender boundary**: `intelligence/contender_evaluation/` (`VRT`, `WMT`) and the remaining 82
  `intelligence/contenders/registry.yaml` entries are excluded from the first synthesis's governed
  evidence base, unchanged from `XASSET-0012` §7. No capital-priority conclusion for `VRT`/`GEV` or
  `WMT`/`COST` is authorized, reopened, or implied by this filing.
- **ETF/QQQ boundary**: `fund_broad_market`'s population remains exactly {SPY, VEA, VWO};
  `fund_gld_defensive`'s remains exactly {GLD}. `QQQ` (`primary_disposition: benchmark_or_index` in
  the contender registry) is not eligible and is not authorized for any future population under this
  filing. No profile or relationship record may assert or imply the current ETF set is globally
  optimal.
- **Output authority**: the future implementation may produce only the closed methodology
  dispositions `XASSET-0012` §5.1 defines (`stronger_evidence_maturity` / `role_preserving` /
  `coexistence_supported` / `unable_to_determine`), never converted into a sleeve weight, an
  allocation percentage, an IN/OUT eligibility verdict, a target allocation, an investment-
  superiority claim, or any instrument-level sizing decision — restating, not narrowing or widening,
  `XASSET-0012` §G's own explicit non-authorization list.

### J. Evidence-limitation disclosure requirements — none may be treated as neutral or complete

The future implementation must explicitly preserve, via the abstention/partial-evidence mechanism
`XASSET-0012` already defines, every known gap already live in the sealed evidence base, never
smoothed over or treated as neutral:

- 9 of 27 equity `valuation_results` records are `partial`, none `unable_to_determine` — the
  `equity` sleeve's own profile must reflect this exact split, not round up to `fully_computed`.
- `discount_rate_evidence` is abstained on all 27 equity records where applicable (per
  `VALUATION-0004`/`VALUATION-0005`'s own disclosed universal gap) — cited as a known limitation
  where it bears on `equity`'s own `evidence_coverage_profile`, never silently ignored.
- `crypto`'s own `cross_coin_correlation_status` is forced `not_yet_measured` on all three sealed
  records — a mandatory `abstention_index[]` entry on the `crypto` profile.
- `crypto`'s own `historical_equity_market_drawdown_behavior` sub-field abstains on SOL specifically
  (`unable_to_determine`, per `XASSET-0011`'s own sealed record) while BTC/ETH reach a determined
  `historically_mixed` finding — this sub-field-level split must remain individually visible per
  §4.2.1, never collapsed into one crypto-wide flag.
- `crypto`'s own `historical_inflation_sensitivity_narrative` sub-field is **not** uniform across the
  sleeve: BTC alone matches `fund_gld_defensive`'s own `GLD.yaml` characterization
  (`historically_mixed_or_inconsistent`), while ETH and SOL both independently characterize as
  `historically_weakly_associated` — the row-4 `crypto`↔`fund_gld_defensive` relationship's own
  `rationale` must disclose this divergence explicitly (per §D's own restated requirement above),
  never generalize BTC's own narrative match to the sleeve as a whole.
- The four `overlap_model` dimensions forced `not_yet_computable_interface_only`
  (`crypto_correlation_interface`, `defensive_offset_interface`, `geographic_currency_exposure`,
  `whole_portfolio_volatility_drawdown_concentration`) may never back an
  `overlap_or_duplication_disclosed` finding on any relationship record — enforced mechanically
  per §5.3, not left to drafting discretion.
- `DEBT_REDUCTION`'s own `economic_assessment_readiness` forced `assessment_required` on both
  sub-fields is the `debt_reduction` sleeve's own governing limitation and must drive its profile
  toward `evidence_coverage_profile: forced_abstention` (or the equivalent disclosed-gap value if a
  future implementing session finds a live evidentiary basis this filing did not — disclosed, not
  assumed) — never presented as equivalent to a fully computed sleeve.
- The unresolved `CASH`/`RESERVE` consolidation question (`XASSET-0008` §N, not reopened here) means
  `cash_reserve`'s own profile must continue treating `CASH` and `RESERVE` as one combined,
  undifferentiated family, exactly as `CASH_LIKE_CAPITAL.yaml`'s own sealed record already does —
  never split, never treated as resolved.

None of the above may be silently treated as neutral, resolved, or complete by the future
implementation; each must surface as a disclosed gap in the relevant profile's or relationship's own
`abstention_index[]`/`secondary_conditions`, per `XASSET-0012` §4.2.1/§5.2.

### K. Implementation shape — exactly one future implementation PR

Exactly one future, separate, bounded implementation PR is authorized, unless live architecture at
implementation time demonstrates a genuine integrity reason to split (none is identified by this
filing). That PR may create:

- the six authorized `sleeve_profile` records (§B) and their `COHORT_MANIFEST.yaml`;
- exactly the seven authorized `sleeve_relationship` records (§C) and their own
  `COHORT_MANIFEST.yaml`;
- the dedicated validator module(s) `XASSET-0012` §9 specifies (one module covering both record
  types, or two — the implementing session's own choice to justify, mirroring `XASSET-0006` §A
  point 3's identical deferral);
- the full nineteen-point focused/adversarial test suite `XASSET-0012` §9 requires, including the
  §H mandatory eligibility-language-paraphrase probe above.

It may not populate an eighth `sleeve_relationship` record, redesign any schema field or vocabulary,
weaken or expand any existing repository validator, or touch any protected path (`allocate.py`,
`margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, or any existing sealed Intelligence record).

### L. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry gains exactly one additive milestone gate,
`xasset0013-level1-synthesis-content-authorization` (`status: in_progress`, `pr: null` — this filing
does not mark its own unmerged work complete), plus one additive Lane M gate,
`xasset0012-post-merge-verification`, recording — without editing the
`xasset0012-level1-sleeve-synthesis-methodology-design` gate's own historical text — that `PR #301`
is fully merged and post-merge CI is green, confirmed above. The workstream's ordinary
self-reference fields (`active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`)
are updated to this filing's own live state. No prior gate's own text is edited. `WS-0014`'s own
`status: proposed`/`priority: secondary`/`dependencies: [WS-0005]` are unedited. `WS-0005` and
`WS-0015` are unaffected by this filing.

### M. Explicit non-authorization

This filing authorizes **content-population targeting only** — exact record identities, nothing
else. It does not authorize:

- population of any `sleeve_profile` or `sleeve_relationship` record by this filing itself;
- any actual comparative finding, evidence-coverage determination, or overlap citation;
- any sleeve weight, sleeve budget, or sleeve allocation percentage;
- any instrument weight or Level 2 sizing decision of any kind;
- any portfolio in/out, eligibility, promotion, or demotion decision for any sleeve or instrument;
- any capital-priority conclusion for `VRT`/`GEV` or `WMT`/`COST`;
- any broader contender-registry sweep beyond `CONTENDER-0003`'s own two-name pilot;
- any `QQQ`/ETF-scope revisit or ETF-population expansion;
- any discount-rate, cross-coin-correlation, `CASH`/`RESERVE`-consolidation, or `DEBT_REDUCTION`
  economic-assessment research;
- any chart evidence, buy-ladder work, backtesting, monitoring, or sell-discipline rule;
- any allocator, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `margin_state.py`, or `levels.py` change;
- any hardening, expansion, or weakening of any existing repository validator beyond building the
  new, dedicated Level 1 synthesis validator(s) `XASSET-0012` §9 already specifies;
- any dashboard change;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind;
- an eighth `sleeve_relationship` pair, or any of the eight deliberately omitted pairs in §E, without
  its own future, separately authorized batch.

## Rationale

`XASSET-0012` designed the methodology but deliberately named "exactly which sleeve profiles and
which relationship pairs the first implementation may populate" as its own future Stage 2 step (§10)
— the same design-then-authorize-content sequence this repository has used for every prior
milestone-scale content step (`TIER-0004`→`TIER-0005` before Milestone 6 population; `REL-0001`→
`REL-0002` before the first relationship batch; `XASSET-0005`→`XASSET-0006`/`XASSET-0007` before
functional-doctrine and overlap-model content; `XASSET-0010`→`XASSET-0011` before the six-instrument
economic-assessment content). Naming the exact scope now, before any record is drafted, prevents the
two failure modes a partially-scoped content PR would otherwise risk: under-scoping (deferring a
pair that materially matters, producing a misleading first synthesis) and over-scoping (forcing full
fifteen-pair coverage before the schema has been proven against real evidence, repeating the
anti-pattern `OPS-0008`'s Research Wave Protocol was created to prevent).

Selecting seven pairs — the five equity-anchored pairs plus two independently-determined non-equity
pairs — rather than mechanically adopting the five example pairs the directive floated, follows the
directive's own explicit instruction not to blindly adopt suggested examples and this repository's
own repeated practice of independently re-deriving scope from live evidence rather than from a
prior session's or an external prompt's own framing (`CONTENDER-0003`'s own independent
re-verification of its authorizing task's assumptions is the most recent precedent). The two
additions were chosen because each answers a question no equity-anchored pair can answer on its own
(crypto-versus-gold's shared alternative-asset narrative; cash-versus-debt-reduction's live
margin-doctrine tension) — not because they were the most obvious or most numerous candidates.

## Alternatives Considered

**Authorize all fifteen `C(6,2)` pairs in the first batch.** Rejected — `XASSET-0012` §3 explicitly
permits bounded first coverage, and forcing full coverage before any pair has been drafted against
real evidence would repeat the exact anti-pattern `OPS-0008`'s Research Wave Protocol and
`CONTENDER-0003`'s own two-of-nineteen precedent were both built to avoid: proving the mechanism
narrowly before scaling.

**Authorize only the five equity-anchored pairs, deferring both non-equity pairs.** Considered and
rejected on the merits, not by default: `crypto`↔`fund_gld_defensive` and `cash_reserve`↔
`debt_reduction` each answer a real question a purely equity-anchored batch cannot — a strictly
five-pair batch would leave a reader to infer crypto-versus-gold and cash-versus-debt-reduction
relationships transitively through equity, exactly the kind of unsupported inference §D above
argues a first synthesis should close directly.

**Authorize a third non-equity pair** (the directive's own third floated example,
`fund_broad_market`↔`cash_reserve`). Rejected — §E class 1 finds this pair, and every other
`fund_broad_market` pairing beyond `equity`, structurally redundant with the equity-anchored batch's
own findings, since `fund_broad_market` occupies the identical broad-risk-capital-deployment
functional role `equity` already tests against every other sleeve.

**Populate fewer than six sleeve profiles**, deferring `debt_reduction`'s own profile given its
forced-abstained evidence base. Rejected — `XASSET-0012` §4.2's `forced_abstention` vocabulary value
exists precisely to represent this case honestly; omitting the profile entirely would produce a less
complete, not a safer, first synthesis, and would leave `debt_reduction` entirely absent from the
sleeve taxonomy a reader sees, rather than present with its own disclosed limitation.

## Consequences

**Changes as a direct result of this decision**: the existence of one retained, exact six-sleeve-
profile population authorization and one retained, exact seven-pair sleeve-relationship population
authorization (with the remaining eight pairs explicitly deferred by class, not silently dropped),
both bound by reference to `XASSET-0012`'s already-accepted methodology with no restatement or
redesign; one binding requirement that the future implementation probe the carried-forward
eligibility-language-paraphrase vulnerability class before push; confirmation, via one additive
`operations/WORKSTREAMS.yaml` gate, that `XASSET-0012`'s own authorized methodology (`PR #301`) is
fully merged and post-merge CI is green.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin
behavior; the 1.8x leverage cap or 30% margin-buffer floor; any Company, Theme, relationship,
classification, valuation-archetype, valuation-evidence, valuation-result, ETF-classification,
crypto-classification, functional-doctrine, overlap-model, economic-assessment,
instrument-economic-assessment, or contender-evaluation record's content; any current cash balance,
reserve level, GLD holding, or margin-debt figure; `WS-0005`'s completed, `status: complete` state;
`WS-0014`'s own `status: proposed`/`priority: secondary`; or any brokerage, trading, or order-related
capability. Completing this unit does not itself populate any sleeve profile or sleeve relationship
record — that remains a separate, future, explicit-review-gated implementation PR — and does not
authorize an eighth relationship pair, Level 2 instrument-level design or sizing, or Stage 4 policy
adoption, per `XASSET-0012` §10's own unedited four-stage sequence.
