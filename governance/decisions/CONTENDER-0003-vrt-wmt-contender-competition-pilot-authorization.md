---
decision_id: CONTENDER-0003
date: 2026-08-10
status: Proposed
category: contender_universe_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, CONTENDER-0001, CONTENDER-0002, XASSET-0001, TIER-0001, TIER-0002, TIER-0009, PI-0016, PI-0019, PI-0020, PI-0021, PI-0022, PI-0026, PI-0032, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0006, VALUATION-0007, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/CONTENDER-0003-vrt-wmt-contender-competition-pilot-authorization.md
---

## Context

### Authority for this unit

The human repository principal explicitly authorized exactly one bounded governance/design filing for
a **two-name broader-equity contender-competition pilot**, covering exactly `VRT` and `WMT`, to
establish the minimum safe mechanism needed to compare non-canonical equities against their canonical
incumbents using existing Portfolio-HQ evidence and valuation doctrine. This filing is **design and
pilot authorization only** — it performs no contender-evaluation content, no research conclusion, no
promotion/demotion, no portfolio selection, and no capital-allocation decision.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory `/home/user/
  Portfolio-HQ`, branch `claude/vrt-wmt-contender-pilot-fakayi`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local branch head and `origin/main` both confirmed
  identical at `a79c2a8b65e2220e08b5471fc5d30f019db86872` — independently confirmed (via
  `mcp__github__pull_request_read`) to be the merge commit of **PR #297** (`head` = corrected
  `580ecd1d730d459bb1d4eafb74086d76ab795b3e`, `base` = `5e7e6c07ddae8494e2eda4be7808e62376a82751`),
  the `XASSET-0011`-authorized implementation delivering the six sealed `intelligence/
  instrument_economic_assessment/{SPY,VEA,VWO,BTC,ETH,SOL}.yaml` records. PR #297's own full
  lifecycle independently re-verified via the GitHub API: original independent exact-head review
  (`pullrequestreview-4900226400`, CHANGES REQUIRED — 0 BLOCKING / 0 MAJOR / 2 MINOR — a `SPY.yaml`
  spelled-out numeric-magnitude leak and a manifest `record_path` presence-only check), a bounded
  correction (`issuecomment-5244985609`, corrected head `580ecd1d...`), a delta review
  (`pullrequestreview-4900345645`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0/0/0/0),
  explicit principal acceptance at that exact head (`issuecomment-5245186740`), and merge-commit CI
  independently re-fetched (workflow run `31426005526`, `status: completed`, `conclusion: success`).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **107 decisions, `issues == ()`**. `governance/decisions/` independently confirmed to hold 107 `.md`
  files besides `README.md`, reconciling 1:1 against `governance/decisions.yaml`'s 107 rows.
- **Next unused `CONTENDER-####` identifier** independently reconciled: a full-catalog scan found
  exactly `CONTENDER-0001` and `CONTENDER-0002` filed; **`CONTENDER-0003` is the next unused
  identifier**, matching the task's own stated identifier.
- **Contender registry** (`intelligence/contenders/registry.yaml`, `CONTENDER-0002`'s own output, 84
  entries) independently re-read: `VRT` and `WMT` both carry `primary_disposition: evaluation_ready`,
  `secondary_flags.has_historical_intelligence: true`, `classification_exists: false`,
  `current_holding: false`, `current_target: false`, `has_current_gate: false`, and
  `next_required_action: "eligible for a future, separately authorized research-readiness-consuming
  step (e.g. an additional blind-classification cohort)"` — matching the task's own stated preflight
  finding exactly.
- **Canonical 27-name equity population** independently re-derived live via
  `relationship_validator.load_canonical_universe('.')`: exactly 27 names, `VRT` and `WMT` both
  confirmed absent. `GEV` and `COST` both confirmed present, each already carrying a sealed
  `intelligence/valuation_archetype/<TICKER>.yaml` record (`GEV`: primary archetype `B`, secondary
  `F`, evidence quality `limited`; `COST`: primary archetype `G`, secondary `A`, evidence quality
  `comprehensive`) and a sealed Milestone 6 `intelligence/classification/<TICKER>.yaml` record.
- **`VRT`/`WMT` Company Intelligence** confirmed to already exist at `intelligence/companies/
  {VRT,WMT}.{yaml,md}` — `VRT` filed under `PI-0026` (Batch 4, power infrastructure — `conviction.
  rating: Medium`, `last_reviewed: 2026-07-26`, `next_due: 2026-10-24`); `WMT` filed under `PI-0032`
  (`conviction.rating: Medium`, `last_reviewed: 2026-07-28`, `next_due: 2026-10-26`). Neither has a
  `valuation_archetype`, `valuation_evidence`, `valuation_result`, or Milestone 6 `classification`
  record — confirmed by direct filesystem check (absent from all four sealed directories).
- **Existing comparator evidence** independently confirmed live: `VRT` was already named as one of
  exactly three comparators (`ETN`, `VRT`, `PWR`) in `PI-0019`/`PI-0020`'s `GEV` committee review
  under the `PI-0016` standing methodology; `WMT` was already named as one of exactly four comparators
  (`WMT`, `AMZN`, `BRK.B`, `V`) in `PI-0021`/`PI-0022`'s `COST` committee review under the same
  methodology. Both committee reviews are prose governance findings, not sealed, validated Intelligence
  records — confirmed by direct inspection of `governance/decisions/PI-0019*.md` and
  `PI-0021*.md`.
- **Canonical validator population-closure mechanism** independently confirmed by direct source
  inspection: `classification_validator.py` (Milestone 6), `valuation_archetype_validator.py`, and
  `valuation_evidence_validator.py` all import and enforce `relationship_validator.
  load_canonical_universe()` — a live, 27-name population derived from `targets.yaml`'s
  `destination:` list, `asset_class == equity` only — as their hard population ceiling.
  `valuation_result_validator.py` does **not** import `relationship_validator` or call
  `load_canonical_universe()` at all — independently confirmed by direct grep (zero matches) and by
  its own module docstring, which states explicitly it is "**roster-agnostic by design (`VALUATION-
  0006` §B): no closed/authorized population is enforced here**," a deliberate accepted design choice
  distinct from the other three validators, not an oversight. This does not change this filing's own
  conclusion: three of the four canonical validators genuinely hard-enforce the 27-name population,
  and none of the four validators — including the roster-agnostic one — defines any schema field
  this pilot's own `contender_evaluation` records could populate, so a dedicated non-canonical
  domain remains necessary regardless of `valuation_result_validator.py`'s own population posture.
  Neither `VRT` nor `WMT` can pass either of the three hard-enforced validators' population checks
  without either adding them to `targets.yaml` (out of scope, prohibited) or weakening the validators
  themselves (explicitly prohibited by this filing's own authorizing instruction).
- **No existing decision authorizes contender-evaluation content of any kind.** `CONTENDER-0001` §F
  and `CONTENDER-0002` §M both explicitly withhold authorization for "additional blind classification
  of any equity beyond the sealed 27"; `XASSET-0001` §I item 3 / §J step 2 name this work as its own
  future, separately authorized `WS-0014` step, not begun by any prior filing.

## Decision

### A. The smallest useful pilot: exactly `VRT` and `WMT`, no third ticker

This filing authorizes a **two-name pilot**, exactly `VRT` and `WMT` — no third ticker, no sweep of
the contender registry's other 17 fresh `evaluation_ready` names, no refresh of its 7 stale entries,
no `SNDK`/excluded/deferred-name research, no `QQQ`/ETF-scope revisit. `VRT` and `WMT` are the
strongest-supported pair currently available for exactly the reason the preflight above establishes:
each already has (1) a real Company Intelligence record with a determined `Medium` conviction and
current review cadence, and (2) prior, principal-approved committee-review comparator evidence
directly against its intended canonical incumbent — `VRT` against `GEV` (`PI-0019`/`PI-0020`), `WMT`
against `COST` (`PI-0021`/`PI-0022`). No other contender-registry `evaluation_ready` name has both
properties simultaneously. Proving the mechanism on this pair — the two names requiring the least new
evidence-gathering — is the fastest, lowest-risk path to a working contender-comparison capability;
sweeping a larger set before the mechanism itself is proven would repeat this repository's own
disclosed anti-pattern (`OPS-0008`'s finding that earlier batches proceeded to drafting before
confirming evidence readiness).

### B. Canonical comparators — read-only reference, never modified

`GEV` (for `VRT`) and `COST` (for `WMT`) are referenced **structurally, read-only** — via a
content-hash pin into each comparator's own already-sealed `intelligence/valuation_archetype/
<TICKER>.yaml` record, reusing `valuation_archetype_validator.canonical_record_hash()` exactly as
every prior cross-schema structural-reference in this repository has (`GLD_DEFENSIVE_ROLE.yaml`'s pin
into `GLD.yaml`; `CASH_LIKE_CAPITAL.yaml`'s pin into `CASH.yaml`/`RESERVE.yaml`; the six `intelligence/
instrument_economic_assessment/` records' pins into their own ETF/crypto classification records). No
future implementation under this authorization may edit, restate, duplicate, or reclassify any field
of `GEV.yaml`, `COST.yaml`, or either ticker's own sealed Milestone 6 classification, archetype,
evidence, or result record. A hash mismatch (live-recomputed, never trusted from a stored value) is a
hard validator failure, matching every prior structural-reference mechanism in this repository.

### C. Reused doctrine — cited by reference, not redesigned

The future implementation this filing authorizes must reuse, unmodified, by reference:

1. **Valuation-methodology archetype taxonomy** — the closed A–G taxonomy frozen in `research/
   equity_valuation_study/PROTOCOL_V1.md` §5 and its abstention value `unable_to_determine_archetype`,
   exactly as `VALUATION-0003` already applied it to the canonical 27. No new archetype value, no new
   taxonomy.
2. **Evidence-quality doctrine** — the `primary_source_coverage`/`uncertainty_statement` shape and the
   provenance vocabulary (`source_type`: `primary`/`secondary`; `access_status`: `directly_inspected`/
   `consulted_via_search_aggregation`/`attempted_not_directly_inspected`) established by `VALUATION-
   0004` and reused unmodified by every subsequent `VALUATION-####`/`XASSET-####` schema in this
   repository (most recently `XASSET-0010`/`XASSET-0011`).
3. **Abstention discipline** — a first-class, non-cascading `unable_to_determine`-shaped abstention
   path on every substantive field, matching `TIER-0002`/`VALUATION-0003`/`VALUATION-0007`'s own
   established convention: an abstention on one field never forces or implies a value on another.
4. **False-precision controls** — `VALUATION-0002` §3's zero-fabricated-precision doctrine and, more
   specifically, the **zero-numeric-field rule with no carve-out**, matching `XASSET-0005`'s (`GLD`/
   `CASH_LIKE_CAPITAL`/functional-doctrine/overlap-model), `XASSET-0010`'s (ETF/crypto instrument),
   and `VALUATION-0003`'s (equity `valuation_archetype`, itself already "no numeric field of any
   kind" — this pilot shares that identical posture, not a stricter one) own zero-numeric-field
   design. This pilot's own posture is genuinely stricter only relative to `valuation_evidence`'s
   and `valuation_result`'s schemas — the two layers that do carry governed numeric content (sourced
   financial figures; low/base/high ranges) — never relative to `valuation_archetype`, since this
   pilot's own purpose is a bounded comparability finding, not a quantitative valuation exercise.
5. **Methodology-application/result conventions** — `VALUATION-0002` §2's already-accepted, closed
   per-family governed-role table (mapping each of the seven methodology families to a governed role
   — Primary candidate / Secondary-corroborative / Adjustment-required / Prohibited / Insufficient
   basis — per archetype letter) is reused **as a mechanical lookup only**, keyed off whichever
   archetype letter the contender's own evidence supports. This produces a **methodology-
   applicability reference**, not a valuation. No discount rate, WACC, beta, terminal-growth rate,
   applied peer multiple, scenario probability, or numeric range of any kind is computed, estimated,
   or authorized for either ticker under this filing — the actual valuation-execution machinery
   `VALUATION-0006`/`VALUATION-0007` built for the canonical 27 is explicitly not reopened, extended,
   or reused for `VRT`/`WMT` by this filing (§H).
6. **Existing Company Intelligence and comparator evidence** — `VRT.yaml`/`VRT.md`, `WMT.yaml`/
   `WMT.md`, and the two committee-review comparator findings (`PI-0019`/`PI-0020`; `PI-0021`/
   `PI-0022`) are the primary permitted evidence base for the future implementation's archetype and
   evidence-quality assessments — no new primary research is required or authorized to prove the
   mechanism on this pair, though a future implementing session may perform bounded, disclosed
   supplementary sourcing consistent with §H's boundary if the existing record proves genuinely
   insufficient on a specific field (abstaining, per §C.3, rather than fabricating, if it cannot).

None of the six conventions above is redesigned, extended, or amended by this filing. Every one is
bound by reference to its own already-accepted governing text.

### D. A separate, non-canonical content domain — new directory, dedicated validator

Because `classification_validator.py`, `valuation_archetype_validator.py`, and `valuation_evidence_
validator.py` each hard-enforce the live 27-name canonical population (§ preflight) and must not be
weakened or expanded to admit `VRT`/`WMT` (an explicit instruction of this authorization) —
`valuation_result_validator.py` is roster-agnostic by its own accepted `VALUATION-0006` §B design and
enforces no population at all, but defines no field this pilot's schema could populate either, so its
different posture does not change the conclusion below — the future implementation must define a
**new, separate, non-canonical directory and a dedicated validator module** — matching this
repository's own repeated, settled pattern of "different population/schema → different directory,
different validator" (`etf_classification_validator.py`, `crypto_classification_validator.py`,
`functional_doctrine_validator.py`, `overlap_model_validator.py`, `economic_assessment_validator.py`,
`instrument_economic_assessment_validator.py` — none shares a population-closure mechanism with any
sealed-27 validator, and none has ever needed to). This is the smallest structure capable of
producing like-for-like evidence-parity outputs without touching a single line of any canonical-27
validator.

- **Directory**: `intelligence/contender_evaluation/` — a new, roster-agnostic-in-shape-but-fixed-
  population-in-practice directory, one record per contender ticker (`VRT.yaml`, `WMT.yaml`) plus
  `COHORT_MANIFEST.yaml`, matching the shape of every prior sealed-cohort directory in this
  repository.
- **Validator**: a new, dedicated `contender_evaluation_validator.py` module — zero import coupling
  with `allocate.py` or `margin_state.py` in either direction (independently testable via AST
  inspection, matching every prior validator's own established discipline); a hard-coded, closed
  two-name population constant (`AUTHORIZED_POPULATION = frozenset({"VRT", "WMT"})`), analogous to
  `etf_classification_validator.py`'s and `crypto_classification_validator.py`'s own hard-coded
  fixed-population constants rather than a live-derived roster (no `targets.yaml` row exists for
  either ticker to derive a population from); read-only structural-reference hash recomputation
  against `GEV.yaml`/`COST.yaml`'s own sealed `valuation_archetype` records via `valuation_archetype_
  validator.canonical_record_hash()`.

### E. Schema — the smallest structure producing like-for-like evidence-parity outputs

Each `intelligence/contender_evaluation/<TICKER>.yaml` record must carry exactly:

1. **Envelope** — `contender_symbol`, `canonical_comparator_symbol`, `schema_version`, `provenance`
   (reusing §C.2's vocabulary), lifecycle/seal fields (`lifecycle_status`, `sealed_at`,
   `governing_decisions`, `content_sha256`), matching every prior sealed-cohort record's own shape.
2. **`comparator_structural_reference`** — exactly one hash pin per record, into the named canonical
   comparator's own sealed `valuation_archetype` record (`referenced_content_sha256`, live-
   recomputed, never trusted from a stored value — §B).
3. **`archetype_assessment`** — `primary_archetype` (the closed A–G taxonomy or
   `unable_to_determine_archetype`), an optional `secondary_archetype` (`!= primary`, forced `null` on
   abstention, matching `TIER-0004`'s established non-cascading-abstention shape), and a `rationale`
   citing only the permitted evidence in §C.6.
4. **`evidence_quality_assessment`** — `primary_source_coverage` and `uncertainty_statement`, reusing
   §C.2's schema exactly.
5. **`methodology_applicability_reference`** — a read-only lookup of `VALUATION-0002` §2's own
   per-family governed-role table for the ticker's own determined `primary_archetype`, never a new
   judgment (§C.5) — explicitly **not** a valuation-result field, never carrying a range, a discount
   rate, a peer set, or a scenario probability.
6. **`evidence_parity_finding`** — a **closed, purely descriptive vocabulary** comparing the
   contender's own evidence completeness/maturity (not investment merit, not business quality) against
   the canonical comparator's own sealed `evidence_quality` state: `comparable_evidence_depth` /
   `contender_evidence_gap` / `comparator_evidence_richer` / `insufficient_evidence_for_parity_
   determination`, plus a `rationale`. This field answers only "is there enough comparable evidence to
   support a future capital-priority comparison" — it never answers "which one is better" or "should
   either be added, removed, or resized."
7. **`abstention_index`** — reconciling every `unable_to_determine`-shaped value present, matching
   §C.3.
8. **Zero numeric fields anywhere** — no carve-out of any kind (§C.4), independently enforced by both
   a forbidden-key-name scan and a free-text numeric-pattern scan.

No field in this schema computes, implies, or outputs a score, rank, composite index, capital-
priority conclusion, or promotion/demotion recommendation. The schema is deliberately narrower than
the canonical 27's own four-layer pipeline (`classification` → `valuation_archetype` → `valuation_
evidence` → `valuation_result`) — it produces one bounded comparability finding per contender, not a
parallel valuation pipeline.

### F. Validator/test requirements for the future implementation

The future, separate, bounded implementation PR this filing authorizes must build, at minimum:

- closed schema at every nesting level (envelope, structural-reference, archetype-assessment,
  evidence-quality, methodology-applicability-reference, evidence-parity-finding, abstention-index,
  provenance source, manifest row) with **extra-key rejection**, not merely missing-key checks
  (learning directly from `contender_registry_validator.py`'s own disclosed MAJOR finding);
- live, independent recomputation of every structural-reference hash, never trusting a stored value
  (§B), with a dedicated stale-hash rejection test;
- a hard-coded, closed two-name population check (`VRT`, `WMT`, zero exception, zero silent
  contraction or expansion);
- an independent free-text scan rejecting: any numeric token of any kind (percent, currency, ratio,
  written-out magnitude comparison — learning directly from `instrument_economic_assessment_
  validator.py`'s own disclosed MINOR-1 finding on `SPY.yaml`, which caught only digit+`%`-shaped
  tokens and missed a spelled-out "three times lower" magnitude claim); chart-domain terminology; and
  word-boundary-matched directive/trading language (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/
  `stage`, matching the established citation-field-exemption pattern where genuinely needed);
- a **new, dedicated forbidden-promotion-language scan** — this pilot's own specific prohibition
  (§H) — rejecting any assertion that a contender should be added to, promoted into, or should
  replace/supersede/displace its canonical comparator within `targets.yaml`/`holdings.yaml`/the
  canonical 27, and any composite-score- or ranking-shaped key name (`score`, `rank`, `priority_
  index`, `composite`, and equivalents);
- a further, **materially separate, dedicated comparative-investment-superiority scan** on
  `evidence_parity_finding.rationale` and `archetype_assessment.rationale` specifically — the
  forbidden-promotion-language scan above catches only an explicit add/promote/replace/supersede/
  displace/score/rank assertion, and would not by itself catch a generic comparative-quality claim
  (e.g. "VRT's business is a stronger investment than GEV," "WMT is the superior compounder,"
  "better positioned," "preferable investment," "outperform," "underperform," or equivalents) that
  converts §E.6's own descriptive evidence-completeness/archetype finding into an implied investment
  preference or expected-relative-performance judgment without ever naming a score, rank, or
  add/promote/replace action. This scan must remain a bounded, closed term/phrase list — matching
  every prior pattern-based free-text scan already accepted throughout this repository's validator
  history — never a generic sentiment/NLP classifier, and must be independently tested with
  adversarial false positives proving it does **not** reject legitimate descriptive language about
  evidence completeness, evidence maturity, archetype classification, uncertainty, or abstention
  (e.g. "the contender's evidence base is materially less mature than the comparator's," "both
  records share the same primary archetype," "insufficient evidence exists to support a parity
  determination" must all still validate cleanly);
- manifest bidirectional reconciliation (hash, duplicate, missing, extra, orphan — every check the
  independent review history of prior manifests in this repository has required);
- zero import coupling with `allocate.py`/`margin_state.py`, independently AST-verified;
- a dedicated test confirming `GEV.yaml`/`COST.yaml` and their sealed `valuation_archetype`/
  Milestone 6 `classification` records remain byte-identical before and after the future
  implementation, matching `economic_assessment_validator.py`'s and `functional_doctrine_validator.
  py`'s own established `test_protected_intelligence_records_untouched` precedent — a live
  `git status --porcelain` check against those exact paths, not merely the structural-reference
  hash-pin's own indirect, next-run-only detection;
- a focused test suite covering every check above, both directions of every conditional/closed
  vocabulary, and a real-corpus validation pass against the two real sealed records once populated.

### G. Pilot output boundary — explicit prohibitions restated as this filing's own operative text

The future implementation this filing authorizes may produce **only** the evidence-parity contender
outputs described in §E for `VRT` and `WMT`. It must not, under any framing:

- rank, score, or compare the full equity universe or any subset of the contender registry beyond
  `VRT`/`WMT`;
- create a composite score of any kind;
- promote `VRT` or `WMT` into the canonical 27-equity cohort, or add either to `targets.yaml`/
  `holdings.yaml`;
- remove, demote, or reclassify `GEV` or `COST`;
- modify any target, tier, holding, gate, cap, cluster, or allocator behavior;
- make, state, or imply an IN/OUT portfolio decision for any ticker;
- make, state, or imply a cross-asset or Level 1/Level 2 sizing decision;
- perform any valuation execution (no discount rate, WACC, beta, terminal-growth rate, applied peer
  multiple, scenario probability, or numeric range for either ticker — §C.5);
- perform additional-equity blind classification under `TIER-0002`'s own Milestone-6-style multi-shard
  sanitizer/isolation machinery — that mechanism remains a separate, heavier, still-unauthorized future
  option under `XASSET-0001` §I item 3, not exercised or foreclosed by this filing, which deliberately
  reuses the lighter `VALUATION-####` archetype/evidence-quality conventions instead (a design choice,
  explained further in Alternatives Considered below, not a redesign of `TIER-0002` itself);
- any capital-priority conclusion of any kind. `CONTENDER-0001` §B is unambiguous that contender
  status "creates evaluation eligibility only," and no controlling doctrine currently authorizes a
  capital-priority conclusion for a non-canonical ticker outside a `PI-0016`-style, separately
  authorized committee review — this filing does not newly authorize one. `PI-0019`/`PI-0020`'s and
  `PI-0021`/`PI-0022`'s own comparator findings for `VRT`/`WMT` remain exactly what they always were:
  process-only, non-scoring evidence-gathering context for `GEV`'s and `COST`'s own reviews, never a
  capital-priority finding about `VRT` or `WMT` themselves, and this filing does not convert them into
  one.

Any actual capital-priority, promotion, or portfolio-selection conclusion — for `VRT`, `WMT`, or any
other contender — remains a separate, later, explicitly authorized decision, matching every prior
`WS-0014` content-authorization filing's own identical restatement of this boundary.

### H. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry gains exactly one additive milestone gate,
`contender0003-vrt-wmt-competition-pilot-authorization` (`status: in_progress`, `pr: null` — this
filing does not mark its own unmerged work complete), plus the ordinary self-reference synchronization
(`active_branch`, `active_pr`, `last_verified_main_sha` updated to `a79c2a8b65e2220e08b5471fc5d30f01
9db86872`, `last_verified_date`) folding forward PR #297's confirmed merge. No prior gate's own text
is edited. `WS-0014`'s own `status: proposed`/`priority: secondary`/`dependencies: [WS-0005]` are
unedited. `WS-0005` and `WS-0015` are unaffected by this filing.

### I. Explicit non-authorization

This filing authorizes **exactly one** future, separate, bounded implementation PR to build:
`intelligence/contender_evaluation/{VRT,WMT}.yaml` (sealed, per §E), `COHORT_MANIFEST.yaml`, a new
dedicated `contender_evaluation_validator.py` (per §D/§F), and its focused test suite — nothing more.
That future PR requires its own full independent exact-head review under `OPS-0007` §1, any required
bounded correction and re-review, explicit principal acceptance, merge, and post-merge verification
before it may be considered complete. It does not itself authorize:

- research or evaluation of any contender other than `VRT`/`WMT` (including the other 17 fresh
  `evaluation_ready` contender-registry entries, the 7 stale entries, `SNDK`, or any deferred/excluded
  name);
- any `QQQ`/ETF-scope revisit;
- any cross-asset synthesis, overlap/concentration modeling, or Level 1/Level 2 sizing;
- any chart evidence, buy-ladder work, backtesting, margin/debt research, or monitoring/sell-discipline
  rule;
- any allocator change of any kind;
- any hardening, expansion, or weakening of `classification_validator.py`, `valuation_archetype_
  validator.py`, `valuation_evidence_validator.py`, `valuation_result_validator.py`, or any other
  existing repository validator;
- any dashboard change;
- any tier/target/holdings/gate/cap/cluster/order/trade change of any kind.

## Rationale

`CONTENDER-0001` established that every genuine investable ticker in this repository is eligible for
future contender screening, and that contender status "creates evaluation eligibility only." `XASSET-
0001` §I item 3 named "additional-equity blind-classification cohorts" as its own future `WS-0014`
step, dependent on `WS-0005`'s equity-cohort evidence and on `CONTENDER-0002`'s own contender-
normalization/readiness-screening step (already complete, `PR #258`). Neither filing performed or
authorized any actual contender content — this is the first filing in `WS-0014`'s history to move from
architecture/normalization into an actual contender-comparison mechanism, and it does so at the
smallest possible scale: two names, both already evidence-ready, both already carrying prior
principal-approved comparator context against their intended canonical incumbent. Proving the
mechanism here — rather than designing a generic, universe-wide ranking system first — matches this
repository's own repeated, settled discipline of building the smallest reversible unit before scaling
(`PI-0003`'s single-company pilot before any batch; `TIER-0001`'s classification-question inventory
before any framework design; `XASSET-0002`'s five-instrument scope before `XASSET-0002`'s own later
scale-up amendment). Reusing the `VALUATION-####` series' already-accepted archetype/evidence-quality/
false-precision doctrine — rather than either inventing a new evaluation framework or invoking `TIER-
0002`'s heavier Milestone-6 blind-classification machinery — keeps this pilot's own implementation
bounded to exactly what is needed to answer one question: can a non-canonical equity's evidence base
be compared, like-for-like, against a canonical incumbent's, without touching any canonical validator
or drawing any capital-priority conclusion. That is the mechanism this filing authorizes proving.

## Alternatives Considered

- **Reuse `TIER-0002`'s Milestone-6 four-axis framework directly** (economic_role/capital_priority/
  risk_concentration/evidence_quality), matching `XASSET-0001` §I item 3's own literal text. Rejected
  for this pilot as disproportionate to a two-name proof-of-mechanism: that framework's own accepted
  implementation required a dedicated sanitizer, multi-shard blind-drafting isolation, and a 27-ticker
  cohort's worth of process overhead (`TIER-0004`/`TIER-0005`/the Milestone 6 implementation) — sound
  for a 27-name canonical cohort whose evidence directly feeds `targets.yaml`-adjacent policy, but
  more machinery than a bounded, advisory, two-name evidence-parity comparison needs. The lighter
  `VALUATION-####` archetype/evidence-quality doctrine produces a comparably rigorous, still fully
  reused-by-reference mechanism at a fraction of the implementation cost, and remains available as a
  future upgrade path if a larger contender cohort later justifies the heavier machinery — not
  foreclosed by this filing.
- **Sweep the full 19-name evaluation-ready contender pool in one batch.** Rejected as directly
  contrary to the authorizing instruction's own efficiency directive and to `OPS-0008`'s Research Wave
  Protocol discipline (prove the mechanism narrowly before scaling a batch).
- **Extend the canonical `classification_validator.py`/`valuation_archetype_validator.py`/etc. to
  accept a 29-name population (27 + `VRT` + `WMT`).** Rejected outright: those validators' hard
  27-name closure is load-bearing doctrine (`relationship_validator.load_canonical_universe()`, sourced
  live from `targets.yaml`), and weakening it to admit non-targeted, non-held tickers would silently
  blur the canonical/non-canonical evidence boundary this repository has maintained deliberately
  through every prior `XASSET-####`/`VALUATION-####` filing's own separate-directory-per-domain
  convention.
- **Draw a capital-priority conclusion for `VRT` vs. `GEV` and `WMT` vs. `COST` directly in this
  filing**, using the existing `PI-0019`/`PI-0020`/`PI-0021`/`PI-0022` comparator text. Rejected: those
  comparator findings were filed as process-only, non-scoring context for `GEV`'s/`COST`'s own reviews
  under `PI-0016`'s standing methodology, not as capital-priority findings about `VRT`/`WMT`
  themselves, and no controlling doctrine currently authorizes converting them into one outside a
  fresh, separately authorized committee review naming `VRT`/`WMT` as the review subject.

## Consequences

Once this filing merges, exactly one future, separate implementation PR may proceed to build the two
sealed `intelligence/contender_evaluation/` records, `COHORT_MANIFEST.yaml`, `contender_evaluation_
validator.py`, and its test suite, per §E/§F — nothing beyond that. `GEV`, `COST`, every existing
sealed record, `targets.yaml`, `holdings.yaml`, `gates.yaml`, and every canonical validator remain
exactly as they are today. No target, tier, holding, gate, allocation, or trade changes as a result of
this filing. `WS-0014`'s remaining thirteen roadmap items (ETF/crypto economic-assessment content,
`DEBT_REDUCTION` economic assessment, overlap-model content — already independently complete under
prior filings — cross-asset synthesis, Level 1/Level 2 sizing, chart-informed deployment, and the
final independent audit) remain wholly unauthorized and unaffected by this filing. A future,
separately authorized decision is required before any capital-priority, promotion, or portfolio-
selection conclusion may be drawn for `VRT`, `WMT`, or any other contender.
