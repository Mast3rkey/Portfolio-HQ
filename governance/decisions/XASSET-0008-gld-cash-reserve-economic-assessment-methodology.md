---
decision_id: XASSET-0008
date: 2026-08-09
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, TIER-0002, TIER-0009, REL-0001, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0005, XASSET-0006, XASSET-0007, VALUATION-0001, VALUATION-0002, VALUATION-0004]
supporting_artifact: governance/audits/WS0014_GLD_CASH_RESERVE_ECONOMIC_ASSESSMENT_METHODOLOGY_DESIGN_20260809.md
file: governance/decisions/XASSET-0008-gld-cash-reserve-economic-assessment-methodology.md
---

## Context

### Authority for this unit

`XASSET-0005` §5 restates a seven-step whole-portfolio sequence and names step 2 — "perform
asset-appropriate valuation/economic assessment" — as "future, separate, undesigned." Every sealed
functional-doctrine record (`CASH.yaml`, `RESERVE.yaml`, `GLD_DEFENSIVE_ROLE.yaml`) carries the identical
forced value `economic_assessment_readiness.status: assessment_required`, stating plainly that no
governed methodology exists to compare that capital-use type's opportunity cost against anything else.
This filing is the first step toward closing that gap for `GLD` and, in bounded, non-interpretive form,
the legacy `CASH`/`RESERVE` identifiers — it designs a closed, categorical economic-assessment methodology
for **two analytical subjects**: `GLD` and `CASH_LIKE_CAPITAL` (§B). It does not populate any record and
does not itself resolve any sealed record's forced `economic_assessment_readiness` value.

### Bounded correction (same day, this PR): CASH/RESERVE provenance investigation and redesign

**This filing's original submission** (first commit, this same branch/PR) designed the methodology around
**three** independent population members — `CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE` — each getting its own
separately sealed record under a shared schema, with `RESERVE`'s abstention preserved via a "non-cascading
worked example" and `CASH`'s own sealed `functional_role.role_category: operational_liquidity_float`
implicitly treated as settled ground to reason from.

**Before any further work, the controlling principal directed a read-only, repository-wide provenance
investigation** into whether `CASH` and `RESERVE` were ever established as genuinely distinct economic
concepts, or whether that three-member population design was quietly presupposing a distinction the
repository does not actually support. That investigation (performed this same session, zero mutations,
full unshallowed history — 844 commits back to the repository's actual root commit) found:

- `CASH` and `RESERVE` first appear together, simultaneously, in commit `b3afa70` ("feat: implement
  PHQ-2026-02 canonical allocator," 2026-07-31) — the migration to the canonical v1.30 destination
  architecture. **No earlier commit, in the full unshallowed history, mentions either as a portfolio
  category.** The prior five-tier (T1/T2/ETF/band/spec) structure had no cash-allocation row of any kind.
- Both rows' weights (`RESERVE` 4.00%, `CASH` 1.00%) are sourced verbatim from an external,
  out-of-repository committee process (`Portfolio_HQ_Grand_Master_Architecture_v1_30.csv`, cited only by
  SHA-256 — **the source file itself is not retained in this repository**, so whatever rationale (if any)
  that external process had for the split is not inspectable here.
- The only textual distinction anywhere in the retained external evidence is two one-line, purely
  data-plumbing labels (`RESERVE`: "Portfolio-level reserve designation, not a market symbol"; `CASH`:
  "Engine-native cash sleeve; no market-data request required") — explaining why neither needs a
  market-data lookup, not articulating an economic or portfolio-construction rationale for treating them
  differently. The same evidence package's own backtest-modeling data (`test_portfolios.json`) uses a
  **single combined `CASH` key** to represent reserve-plus-gated-target-absorption-plus-`SPCX` cash across
  different scenarios — the external committee's own modeling treated them as fungible, not analytically
  distinct.
- **Zero principal-authorized text anywhere** (`CLAUDE.md`, `decision_log.yaml`, any governance decision,
  the `PHQ-2026-01` principal-approval record) establishes a substantive CASH-vs-RESERVE distinction.
- **Zero mechanical distinction anywhere in code.** `allocate.py` and `levels.py` group
  `("reserve", "cash")` as one identical tuple in every conditional branch (buy-candidate exclusion,
  trim-eligibility exclusion, market-data-fetch exclusion). `margin_state.py` has no `RESERVE` reference at
  all. `gates.yaml` and `issuer_lookthrough.yaml` have zero mentions. `holdings.yaml` persists neither as a
  tracked balance. The **only** difference anywhere in this repository is the bare `target_pct` number.
- The functional-doctrine records' own later characterizations (`CASH.yaml`'s determined
  `operational_liquidity_float`; `XASSET-0005`'s supporting artifact asserting they differ in "intended
  functional purpose") are themselves **AI-authored inferences from this same sparse evidence base**, not
  principal-sourced facts — `RESERVE.yaml`'s own abstention is, by contrast, the epistemically honest
  position.

**The controlling principal's explicit decision, based on this investigation**: Portfolio-HQ does **not**
currently recognize a deliberate policy distinction between `CASH` and `RESERVE`. They are to be treated,
for present analytical/governance purposes, as semantically equivalent, unresolved members of one
cash-like capital family, unless and until a future, separately authorized, principal-approved decision
establishes a genuine distinction. Neither the different labels nor the different `target_pct` values
(4.00% vs. 1.00%) may be read as evidence of a distinct economic purpose. No analysis under this
methodology may bootstrap a later AI-authored description into evidence that `CASH` and `RESERVE` have
distinct functions.

**Resulting redesign, applied throughout this filing and its supporting artifact**: the population
collapses from three independent members to **two analytical subjects** — `GLD` (unchanged) and
`CASH_LIKE_CAPITAL` (new — an analytical family/projection over the unresolved, combined treatment of the
legacy `CASH`/`RESERVE` identifiers, never a new target row, investable symbol, or production concept).
`CASH`'s and `RESERVE`'s own already-sealed functional-doctrine records are **not edited by this
filing** — `XASSET-0006`'s implementation is out of this filing's scope, and any correction to those sealed
records' own content is a separate, future governance question (§D below) — but this methodology no
longer inherits or amplifies their prior characterizations as though settled. This correction changes the
population, the structural-reference mechanism (§H), the abstention treatment (§D, §J), and adds an
explicit downstream governance question (§N) that this filing does not answer. It does **not** change the
GLD-specific methodology (§E), the zero-numeric posture (§G), the evidence/contamination rules (§I), the
future-research interface (§K), the synthesis-handoff boundary (§L), the portfolio-selection boundary
(§M), or this filing's own stage-1-only authorization class (§A) — all of that is preserved unchanged.
This correction was made before any independent review occurred on this PR (confirmed: zero reviews
posted as of this correction) — it is a same-session, pre-review redesign, not a post-review defect fix.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/xasset-0008-economic-assessment-b5078s`, working tree clean at session start (both the original
  drafting session and this correction session).
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c` — `XASSET-0007`'s own merge commit (PR #286) — unchanged
  since this filing's original draft.
- **Zero open pull requests other than this one** confirmed live via the GitHub API at correction time —
  no competing mutation lane. This filing's own PR (**#287**) confirmed `open`/`draft: true`/
  `merged: false`, `mergeable_state: clean`, head `bb938ecdf58a23b6441cf2256b35059bfaa8dd66`, base `main` @
  `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, 6 changed files, 1 commit, **zero reviews posted**
  (`get_reviews` returns `[]`) — confirming this correction lands before any independent review, not as a
  post-review delta.
- **`PR #286`'s full lifecycle independently re-verified via the GitHub API, not assumed**: accepted head
  `cf478cdbcf10fd930d337e74ada9f72a42e09a92` (base `main` @ `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e`);
  single independent exact-head review (`pullrequestreview-4891559425`, **APPROVED FOR PRINCIPAL
  EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE); principal acceptance
  (`issuecomment-5231939730`); merge (merge commit `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, parents
  `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e` and `cf478cdbcf10fd930d337e74ada9f72a42e09a92`); merge-commit
  CI — workflow run `31317721215`, `status: completed`, `conclusion: success`. `WS-0014` step 7's own
  content half remains authorized and awaiting its own separate implementation — this filing does not
  touch it.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`) —
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`. This filing performs the ordinary
  self-reference synchronization (§O below) plus the required Lane M addition confirming `PR #286`'s own
  post-merge state — the `xasset0007-overlap-model-content-authorization` gate's own historical text is
  left unedited.
- **`XASSET-0001` (§A, §D, §E, §F, §J, §M, in full), `XASSET-0005` (decision file plus supporting
  artifact, in full), `XASSET-0006` (in full), and `XASSET-0007` (in full) read directly this session**,
  not summarized from memory.
- **`intelligence/functional_doctrine/{CASH,RESERVE,GLD_DEFENSIVE_ROLE,DEBT_REDUCTION}.yaml` and
  `functional_doctrine_validator.py` independently read directly** — all four confirmed sealed,
  byte-unedited by this filing. `RESERVE.yaml`'s own `functional_role.role_category: unable_to_determine`,
  `abstention_reason` text, and `later_governance_action` were each read verbatim — the provenance
  investigation independently confirmed no repository evidence anywhere else establishes a
  RESERVE-specific functional purpose. `CASH.yaml`'s own `functional_role.role_category:
  operational_liquidity_float` was likewise read verbatim and independently confirmed to be an AI-derived
  determination (its own sealed rationale: "a near-tautological label requiring no interpretive leap"),
  not a principal-sourced fact — carried forward accurately, not silently elevated to authority, in this
  filing's own text (§D below).
- **`intelligence/etf_classification/GLD.yaml` independently read directly** — confirmed sealed,
  unaffected by this correction.
- **`functional_doctrine_validator.py`'s own `canonical_record_hash(data: dict) -> str` function
  independently confirmed present** (`functional_doctrine_validator.py:355`) — load-bearing for both
  `GLD`'s own structural reference (unchanged) and `CASH_LIKE_CAPITAL`'s own revised, two-entry legacy
  structural-reference list (§H below).
- **`VALUATION-0001`, `VALUATION-0002`, and `VALUATION-0004` read directly this session** for the
  design-then-authorize-content separation pattern and false-precision-prevention discipline — unaffected
  by this correction; still not imported wholesale (supporting artifact §1).
- **Decision catalog independently rebuilt**: **102 decisions, `issues == ()`** — `XASSET-0008` already
  present as its own row (this correction does not add a second decision or change the catalog count).
- **Full repository `pytest` independently re-run this session: 4042 passed, 0 failed**, matching the
  expected post-`XASSET-0007` baseline exactly, unaffected by this correction (governance-text-only).

No condition met a Stop bar for the correction itself. The in-place redesign proceeded because it does not
change this filing's authorization class (still stage-1-only methodology design, still no population, no
content, no schema-amendment authority beyond what this filing itself specifies) and does not touch
`GLD`'s own methodology, which required no change.

## Decision

This filing designs, as text only — not an authorization, not an adoption, not applied to any real GLD
holding, cash balance, or reserve level — **a closed economic-assessment methodology for exactly two
analytical subjects: `GLD` and `CASH_LIKE_CAPITAL`**. `DEBT_REDUCTION` is explicitly excluded (§B). It
performs no population, computes no economic finding, resolves no sealed functional-doctrine record's
forced `economic_assessment_readiness.status: assessment_required` value, and asserts no distinct economic
purpose for `CASH` versus `RESERVE`. Full field-by-field detail, closed vocabularies, abstention
discipline, structural-reference mechanics, and the validator/test specification are in the supporting
artifact.

### A. Stage separation — five stages, this filing is stage 1 only

1. **Methodology/schema design** — this filing. Designs the closed question set, evidence rules,
   abstention discipline, and structural-reference mechanics. Performs no content.
2. **Future, separate content authorization** — not performed here; requires its own future, explicit
   principal authorization, mirroring `XASSET-0003`'s/`XASSET-0004`'s/`XASSET-0006`'s own role for the
   ETF, crypto, and functional-doctrine content steps.
3. **Future, separate content implementation** — not performed here; the actual drafting and sealing of
   up to two `economic_assessment` records, gated on stage 2's own authorization and its own full
   independent-review/correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle.
4. **Later cross-asset synthesis** — `XASSET-0001` §E/§F, wholly undesigned, wholly unauthorized by this
   filing or by any future stage-3 content this filing's methodology would produce.
5. **Later explicit policy adoption** — a still-separate, human-approved governance decision, required
   before any evidence this methodology eventually produces may affect any tier, target, holdings, gate,
   cap, cluster, allocator, or margin behavior.

**This filing authorizes stage 1 only.** It does not authorize, begin, schedule, or imply stages 2–5.

### B. Population — exactly two analytical subjects, `DEBT_REDUCTION` explicitly excluded

**`GLD`** — unchanged from this filing's original design; a single-instrument economic-assessment subject
referencing GLD's own sealed ETF structural record and functional-doctrine record by hash pin (§H).

**`CASH_LIKE_CAPITAL`** — an **analytical family/projection**, not a new target row, not a new investable
symbol, and not created in `targets.yaml`, `holdings.yaml`, allocator code, or any production
configuration. It represents the unresolved, combined analytical treatment of the two legacy structural
identifiers `CASH` and `RESERVE` — reused as provenance/reference sources only (§D, §H), never
independently interpreted as two separate economic subjects. This filing does not merge, rename, or delete
either legacy `targets.yaml` row, either sealed functional-doctrine record, or any allocator behavior —
`CASH_LIKE_CAPITAL` exists exclusively inside this future economic-assessment methodology's own schema.

**`DEBT_REDUCTION` is out of scope**: its own economic-assessment gap (`avoided_borrowing_cost_readiness` /
`survivability_and_buffer_benefit_readiness`, `XASSET-0005` §3.5) belongs to the separately governed
margin/leverage-policy track (the 1.8x leverage cap, the 30% buffer floor, `MARGIN-0005`'s own bounded
research charter) — not touched, not reopened, not weakened by this filing. No equity, ETF beyond `GLD`
(referenced only, §E below), or cryptocurrency economic assessment is addressed.

### C. Batching — one filing, two analytical subjects, no new prefix

Both population members are designed in one filing because they share one schema shape (§E, §H) and the
same classification-hygiene discipline this repository has now applied four times (equity, ETF/crypto,
functional-doctrine, this design) — separating them would duplicate the shared abstention/evidence-
quality/structural-reference discipline for no review benefit, the same reasoning `XASSET-0002`'s
ETF+crypto batching and `XASSET-0005`'s functional-doctrine+overlap-model batching both already applied.
This filing continues the existing `XASSET-####` series rather than minting a new prefix — see the
Preflight's decision-catalog reconciliation above; `governance/decisions/README.md`'s own rule is
satisfied because this is a direct continuation of `XASSET-0005` §5's own restated sequence, not a
genuinely new decision domain.

### D. `CASH`/`RESERVE` as legacy structural identifiers — provenance only, no distinct interpretation

`RESERVE.yaml`'s sealed `functional_role.role_category: unable_to_determine` is unchanged by this filing —
not resolved, not inferred around, not silently answered by proxy. This design:

1. Does **not** interpret `CASH` and `RESERVE` as economically or functionally distinct. No repository
   evidence supports such a distinction (Bounded correction, above) — confirmed by a repository-wide,
   full-history provenance investigation, not assumed.
2. Does **not** infer or assume a RESERVE-specific functional purpose (emergency reserve, margin reserve,
   permanent safety buffer, dry powder, deployment reserve, or any other) anywhere, and does **not** treat
   `CASH`'s own already-sealed `functional_role.role_category: operational_liquidity_float` — an
   AI-derived characterization, not a principal-sourced fact (Bounded correction, above) — as settled
   ground for `CASH_LIKE_CAPITAL`'s own analysis. This filing neither edits `CASH.yaml`/`RESERVE.yaml`
   (out of this filing's own scope; either is a separate, future, explicit correction question under
   `XASSET-0006`'s own governance, not decided here) nor inherits their prior characterizations as
   authoritative going forward.
3. Treats `CASH_LIKE_CAPITAL`'s own analytical questions (§F, supporting artifact §3) as questions about
   the **combined, undifferentiated family** — never split into a per-legacy-identifier answer. Because no
   question is asked separately of `RESERVE`, `RESERVE.yaml`'s own abstention is never itself resolved,
   never bypassed, and never made to block `CASH_LIKE_CAPITAL`'s own assessment — the family-level question
   is structurally independent of whichever legacy identifier's own internal composition remains
   unresolved.
4. States explicitly, as a binding methodological rule, that no finding under this methodology may cite
   the different `CASH`/`RESERVE` labels or their different `target_pct` values (4.00% vs. 1.00%) as
   evidence of a distinct economic purpose — mechanically enforced by a dedicated future validator scan
   (supporting artifact §10) that rejects any free-text claim asserting a `CASH`-versus-`RESERVE`
   distinction anywhere in a future `economic_assessment` record.
5. Records that both legacy rows are **historical/configuration facts only** under this methodology —
   their continued existence as two separate `targets.yaml` rows is preserved for backward compatibility,
   historical auditability, and to avoid an unauthorized target/schema migration; it is not itself evidence
   that a distinction was, or should be, established (§N records the separate, future question of whether
   they should ultimately be consolidated).
6. Does **not** create a policy answer merely to make the population complete — a `CASH_LIKE_CAPITAL`
   `economic_assessment` record with one or more genuine `unable_to_determine` axes is a fully valid,
   complete, sealed record under this methodology, exactly as much as a fully determined one.

### E. GLD / overlap-model boundary — no duplicate ownership (unchanged by this correction)

This methodology may address GLD-specific, single-instrument economic characteristics: cost/tracking-
quality economic significance; historically-grounded inflation-sensitivity characterization, if sourced;
historically-grounded, single-asset crisis/drawdown-behavior characterization, if properly scoped;
deployability/optionality; evidence quality and uncertainty (supporting artifact §3). It does **not**
address, duplicate, or preempt: whole-portfolio volatility/drawdown concentration; quantitative or
portfolio-wide diversification-contribution computation; GLD's measured correlation with Portfolio-HQ's
own current holdings; or `defensive_offset_interface`'s own computation, which remains forced
`not_yet_computable_interface_only` under `XASSET-0005` §6.2's unconditional rule, unchanged by this
filing. Supporting artifact §5 makes this boundary structural, not merely documentary — every future
record populating `historical_equity_drawdown_behavior` must carry an explicit single-asset,
non-portfolio-level disclosure, mechanically enforced by a dedicated future validator scan (supporting
artifact §10 point 11).

GLD's existing sealed functional-doctrine finding (`functional_role.role_category:
defensive_offset_or_ballast`) is evidence this methodology may cite by structural reference; it is not an
adopted portfolio-policy conclusion, and this filing does not treat it as proof of any quantitative
diversification benefit.

### F. `CASH_LIKE_CAPITAL` analytical scope — capital-use characterization, not security valuation

`CASH_LIKE_CAPITAL` is treated as a capital-use family, never as an ordinary security requiring a
DCF-style valuation. The methodology may characterize, categorically, for the **combined family as a
whole**: immediate deployability/optionality; economic-assessment-readiness disclosure; uncertainty. It
does not invent, and the supporting artifact's validator specification mechanically forbids: a hurdle
rate; a cash expected-return forecast; a target cash percentage; a rank or score of any kind; **any
claim, categorical or otherwise, that `CASH` and `RESERVE` individually warrant different treatment**
(supporting artifact §10).

### G. Zero-numeric default (unchanged by this correction)

No new numeric assessment field is authorized anywhere in this schema — stricter than the ETF framework's
own single disclosed-fact carve-out (`expense_ratio_pct`), matching the functional-doctrine and overlap-
model schemas' own zero-numeric-field posture instead. GLD's own sealed `expense_ratio_pct` (and any
other existing sealed numeric structural fact) may be referenced by structural hash/source pin under this
design; it does not become precedent for opening a general numeric assessment schema, and any necessary
future numeric carve-out requires its own explicit, separate authorization. The two legacy `target_pct`
values (4.00%/1.00%) are read only as structural identity context for the `structural_reference` pins
(§H) — never as a numeric input to any judgment axis.

### H. Structural references — reuse, never duplicate; revised for the two-subject population

**`GLD` (unchanged)**: a future implementation must use live structural-reference/hash-pin semantics,
reusing `etf_classification_validator.canonical_record_hash()` and
`functional_doctrine_validator.canonical_record_hash()` — both independently confirmed present and already
relied upon by an existing sealed record — rather than duplicating any sealed field. Supporting artifact §4
gives the full mechanism, including why a direct pin into `GLD.yaml` (not only a two-hop pin through
`GLD_DEFENSIVE_ROLE.yaml`) is required.

**`CASH_LIKE_CAPITAL` (revised by this correction)**: rather than a single required pin into one sealed
functional-doctrine record (the original design's per-member mechanism, which presupposed `CASH` and
`RESERVE` were separately meaningful subjects), a future `CASH_LIKE_CAPITAL` record must carry a **list of
exactly two legacy structural references** — one pinning to `intelligence/functional_doctrine/CASH.yaml`,
one pinning to `intelligence/functional_doctrine/RESERVE.yaml`, both via
`functional_doctrine_validator.canonical_record_hash()` — cited as **provenance context only**. Neither
pinned record's own content (including `CASH.yaml`'s own `functional_role.role_category:
operational_liquidity_float`) may be copied, restated, or treated as a `CASH_LIKE_CAPITAL`-level finding;
the pins exist solely so a future reader can trace which legacy identifiers this analytical family
combines, not to import either record's own characterization as authority. Supporting artifact §4 gives
the full revised mechanism.

### I. Evidence / contamination boundary (unchanged by this correction)

No live account-specific value from `holdings.yaml`, no `target_pct` from `targets.yaml`, no live
`margin_state.py` output, and no current dollar balance may be used as evidence for any judgment axis —
the identical contamination rule `XASSET-0005` §3.6 already established for functional doctrine, applied
here without modification. Existing mechanisms may be cited structurally (e.g., the existence of the 30%
buffer floor, the existence of the deposit/allocation workflow) where genuinely relevant; their current
live outputs create no investment-policy authority under this schema.

### J. Abstention — non-cascading, honestly disclosed; RESERVE treatment revised

Every substantive axis supports `unable_to_determine` with a required `abstention_reason`; `not_
applicable` is reserved for structurally absent concepts. One axis's abstention never automatically forces
another axis to abstain — this applies to GLD's own three-sub-field compound axis (each sub-field
independently abstainable, supporting artifact §3.3) exactly as before. **`CASH_LIKE_CAPITAL`'s own
abstention treatment is revised by this correction**: because the family-level question is never split
into a per-legacy-identifier answer (§D.3), `RESERVE.yaml`'s own sealed abstention is structurally
**non-blocking** by design, not resolved via a worked non-cascading example as the original draft
described — there is no `CASH_LIKE_CAPITAL`-level "RESERVE's own share of the answer" for that abstention
to cascade into or out of. Missing GLD macro evidence (the three named future research questions, §K
below) never forces an invented conclusion — an honest, specific `unable_to_determine` is a complete,
valid, sealed outcome for either analytical subject.

### K. Future research interface — three named, unanswered questions (unchanged by this correction)

Supporting artifact §7 identifies, without answering: GLD's own historical behavior during major
equity-market drawdown periods; GLD's realized tracking quality against its own benchmark; a defensible,
sourced, long-horizon characterization of gold's relationship to inflation regimes. This filing conducts
no research toward any of the three and treats none as already answered. None of these three questions
concerns `CASH_LIKE_CAPITAL` — that family's own future research needs, if any, are a separate matter this
filing does not address.

### L. Synthesis handoff — categorical evidence only

A future `economic_assessment` record's `cross_asset_handoff` envelope may carry only: categorical
economic findings; assessment/completeness status; evidence quality; freshness; uncertainty; abstentions;
structural references. It may never carry: a target weight; a rank; an IN/OUT selection; a buy/sell/hold
signal of any kind; a sleeve percentage; a trade-timing recommendation; a leverage amount; or any claim of
distinct `CASH`-versus-`RESERVE` purpose. The future synthesis, not this design, compares competing uses of
capital (supporting artifact §8).

### M. Portfolio-selection boundary

Completing economic assessment for `GLD` and `CASH_LIKE_CAPITAL` — however complete — does not select the
portfolio. It creates evidence for a later selection mechanism that does not yet exist:

> evidence → cross-asset opportunity-cost synthesis → explicit human-approved adoption decision → only
> then, governed IN/OUT portfolio membership.

### N. Future consolidation review — a disclosed downstream governance question, not decided here

This filing records, as a disclosed future question and **not as implementation authority of any kind**:

> Should the legacy `CASH` and `RESERVE` `targets.yaml` configuration rows ultimately be consolidated
> into one canonical capital-use row?

Answering that question — in either direction — requires its own future, separate, explicit governance
decision covering, at minimum: an authority/provenance review (building on, not merely repeating, this
filing's own Bounded-correction findings); a target-policy determination (what combined weight, if any,
would replace 4.00%/1.00%, and on what basis); a schema-migration analysis (`targets.yaml`,
`intelligence/functional_doctrine/`, this methodology's own `CASH_LIKE_CAPITAL` design, and any other
affected schema); a full protected-path review; its own independent exact-head review; and explicit
principal acceptance. **This filing does not answer this question, does not recommend an answer, and does
not authorize any future session to treat this disclosure as a standing authorization to begin that work.**

### O. Register updates performed by this filing

`operations/WORKSTREAMS.yaml`'s `WS-0014` entry receives:

1. **One new additive gate, `xasset0007-post-merge-verification`**, recording — without editing the
   `xasset0007-overlap-model-content-authorization` gate's own historical text — that `PR #286` is fully
   merged, reviewed, principal-accepted, and post-merge verified (Preflight above gives the full
   independently re-verified chain). `WS-0014` step 7's own content half is therefore authorized and
   awaiting its own future, separate implementation PR — not begun by this filing.
2. **`active_branch` set to this filing's own branch, `last_verified_main_sha` updated**
   `c90eb6fcf6fc7c2b5a77a6a8d79bc73c0506c50e` → `67c62d363fc2a5c5e627b8c1b0449ca8d0bb8e6c`, and
   **`last_verified_date` updated** to this filing's own date.
3. **One additive gate, `xasset0008-gld-cash-reserve-economic-assessment-methodology-design`** (same gate
   name as this filing's original draft — not renamed, since it still tracks this same filing's own
   progress; its description text is updated by this correction to reflect the revised two-subject
   design), recording this filing's own branch and PR number — `status: in_progress`, **not**
   `status: complete`, matching every prior filing's identical discipline in this chain.
4. **`blocker` and `next_action` updated** to state plainly: `XASSET-0007`'s own authorization is merged;
   this filing, once merged, designs but does not authorize a future `GLD`/`CASH_LIKE_CAPITAL`
   economic-assessment content step, and does not resolve the `CASH`-versus-`RESERVE` provenance question
   beyond recording it as a disclosed future governance question (§N); `DEBT_REDUCTION` economic
   assessment, the overlap-model content implementation itself, the `CASH`/`RESERVE` consolidation
   question, and every other remaining `WS-0014` item (steps 2, 8–13 per `XASSET-0001` §J's own numbering)
   remain wholly unauthorized.

No other `WS-0014` field (`status`, `priority`, `dependencies`, `authorized_scope`, `prohibited_scope`) is
changed. `WS-0005` and `WS-0015` are not touched by this filing.

## Rationale

**Why the population changed from three independent members to two analytical subjects.** The provenance
investigation found no repository evidence — mechanical, textual, or governance — supporting `CASH` and
`RESERVE` as distinct economic subjects, and the controlling principal explicitly declined to adopt such a
distinction (Bounded correction, above). Continuing to design a methodology around three independently
assessed members would have presupposed exactly the fact now found unsupported — the same "force a value
merely to fill the record" failure mode `XASSET-0006` §C already forecloses for content records, applied
here to a governance decision's own population design.

**Why `CASH_LIKE_CAPITAL` is an analytical projection, not a production concept.** Creating a third
`targets.yaml` row, a new `capital_use_type` enum value, or any allocator-visible construct would be an
unauthorized target/schema migration this filing has no authority to perform (explicitly barred by the
controlling principal directive). Confining `CASH_LIKE_CAPITAL` to this future methodology's own schema —
never touching `targets.yaml`, `holdings.yaml`, `allocate.py`, or any sealed functional-doctrine record —
preserves every legacy row and every existing sealed record exactly as-is while still allowing a coherent,
honest economic-assessment question to be asked about the combined, unresolved family.

**Why `CASH.yaml`'s own `operational_liquidity_float` characterization is disclosed but not treated as
authority.** The provenance investigation found that determination is itself an AI-authored inference from
the same sparse evidence base RESERVE's own abstention already discloses as insufficient — not a
principal-sourced fact. Silently continuing to build on it (as this filing's own original draft implicitly
did) would be exactly the "later AI-authored descriptions bootstrap[ping] themselves into policy
authority" failure the controlling principal directive explicitly prohibits. This filing does not rewrite
`CASH.yaml` itself (out of scope, a separate future correction question under `XASSET-0006`'s own
governance) but does not build `CASH_LIKE_CAPITAL`'s own prospective methodology on that characterization
either.

**Why `RESERVE`'s abstention becomes structurally non-blocking rather than needing a "non-cascading"
worked example.** The original design's own worked example existed because `RESERVE` was a separate
population member with its own record and its own axes, one of which (`functional_role`) was abstained
while another (`deployability_and_optionality`) might still be determinable — requiring an explicit
demonstration that the abstention did not automatically cascade. Under the corrected design, no
`CASH_LIKE_CAPITAL`-level axis is ever asked "on behalf of RESERVE specifically" — the family-level
question and `RESERVE.yaml`'s own internal-composition question are now different questions entirely, so
there is nothing for the abstention to cascade into.

**Why this remains a bounded, in-place correction rather than a replacement filing.** This filing's own
stage-1-only authorization class (§A), its `XASSET-####` continuation (§C), and its zero-numeric/
evidence-contamination/abstention/future-research/synthesis-handoff/portfolio-selection design discipline
(§G–§M) are all unaffected by this correction — only the population's shape and the `CASH`/`RESERVE`-
specific sections change. `GLD`'s own methodology (§E) required no change at all. A genuinely different
governance architecture would have been required only if this correction had needed to abandon the
stage-separation discipline, the `XASSET-####` continuation, or GLD's own design — none of which occurred.

## Alternatives Considered

**Keep the original three-member population (`CASH`, `RESERVE`, `GLD_DEFENSIVE_ROLE`), each independently
assessed.** Rejected — this is precisely the presupposition the provenance investigation found unsupported
and the controlling principal explicitly declined to adopt.

**Consolidate `CASH` and `RESERVE` into one `targets.yaml` row within this filing.** Rejected outright,
per the controlling principal directive — mechanical consolidation is a separate, future, bounded
governance decision (§N), not something this design-only filing may perform or presuppose.

**Silently drop `RESERVE` from the methodology's scope entirely, addressing only `CASH`.** Rejected — this
would itself assert an unsupported distinction (that `CASH` alone is the "real" cash-like capital use and
`RESERVE` is not), the opposite error from treating them as separately meaningful; `CASH_LIKE_CAPITAL`'s
combined, non-interpretive treatment is the design that takes no position either way.

**Rewrite `CASH.yaml` and/or `RESERVE.yaml` in this same PR to reflect the corrected understanding.**
Rejected — those are separately sealed records under `XASSET-0006`'s own governance; editing sealed
records is a distinct, future, bounded correction question outside this design-only filing's own scope,
and the controlling principal directive explicitly instructed prospective clarification here instead.

**Design `DEBT_REDUCTION`'s economic-assessment methodology in the same filing, for full step-2
coverage.** Rejected, unchanged from the original design — see Rationale; `DEBT_REDUCTION`'s own gap
belongs to the margin/leverage-policy track, a deliberately separately governed domain this filing does
not open.

**Adopt `VALUATION-0001`'s 7×7 methodology-family-by-archetype matrix, scaled down.** Rejected, unchanged
from the original design — see supporting artifact §1; a matrix built for a methodology-selection-across-
archetypes problem does not fit this design's fixed, small population with no archetype-differentiation
question.

## Consequences

**Authorized, effective only on this decision's merge:** the closed `GLD`/`CASH_LIKE_CAPITAL`
economic-assessment methodology design in the supporting artifact (two-subject population,
`deployability_and_optionality` and `instrument_specific_economic_characterization` axes, two structural-
reference mechanisms — GLD's own single pin, `CASH_LIKE_CAPITAL`'s own two-entry legacy-reference list —
combined validator/test specification, including a dedicated forbidden-distinct-purpose-claim scan);
confirmation, via one additive `operations/WORKSTREAMS.yaml` gate entry, that `XASSET-0007`'s own
authorization (PR #286) is fully merged, reviewed, principal-accepted, and post-merge verified; `WS-0014`'s
ordinary self-reference synchronization; the disclosed, unanswered future `CASH`/`RESERVE` consolidation
question (§N).

**Not authorized by this filing, now or ever without a further separate decision:** population of any
`economic_assessment` record; any economic finding, categorical or otherwise, for `GLD` or
`CASH_LIKE_CAPITAL`; any claim of distinct `CASH`-versus-`RESERVE` economic purpose; resolution of
`RESERVE.yaml`'s own `functional_role` abstention; any edit to `CASH.yaml` or `RESERVE.yaml`; any
consolidation of the `CASH`/`RESERVE` `targets.yaml` rows; any `DEBT_REDUCTION` economic-assessment
methodology; any resolution of any sealed functional-doctrine record's forced
`economic_assessment_readiness.status`; any overlap-model dimension computation (`XASSET-0007`'s own
future, separate content implementation, untouched here); any cross-asset opportunity-cost synthesis; any
Level 1 sleeve or Level 2 instrument sizing; any validator or test implementation; any edit to
`XASSET-0001`, `XASSET-0005`, `XASSET-0006`, or `XASSET-0007`'s own text; and any tier/target/holdings/
role/cluster/cap/gate/allocator/margin/ladder/chart/order/trade change.

**Unchanged by this decision:** every existing Company/Theme/relationship/classification/reconciliation/
recommendation/ETF-classification/crypto-classification/functional-doctrine record, byte-for-byte,
including all four sealed functional-doctrine records (`CASH.yaml`/`RESERVE.yaml` included, unedited) and
GLD's own sealed ETF classification; `XASSET-0001` through `XASSET-0007`'s own accepted text and scope, in
full, unedited; `targets.yaml` (both the `CASH` and `RESERVE` rows, their `target_pct` values, and every
other row, untouched), `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
`levels.py`, `margin_state.py`; the 1.8x leverage cap and 30% margin-buffer floor; `WS-0005`'s completed,
`status: complete` state; `WS-0015`'s own live state; `WS-0014`'s own `status: proposed`/
`priority: secondary`.

This decision becomes effective only when its implementing pull request merges to `main`.

**Whole-universe boundary, restated (unchanged by this or any prior filing in this chain).** Portfolio-HQ
is not a 27-stock system, and this filing's own bounded two-subject methodology design does not narrow
that fact. Still unfinished, still unauthorized by this filing: the 26 researched non-canonical equities;
contender-registry regeneration and legacy-history recovery; QQQ and any other future ETF candidate
expansion; ETF and crypto economic/valuation methodology; equity Stage-4 valuation execution;
`DEBT_REDUCTION` economic assessment; the overlap-model content implementation itself (`XASSET-0007`'s own
authorized, still-unbegun next step); whether `CASH`/`RESERVE` should ultimately be consolidated (§N);
cross-asset opportunity-cost synthesis; Level 1 sleeve allocation; Level 2 instrument allocation;
`CHART-0003` and any remaining governed chart ingestion; ladder/deployment integration; unlevered testing;
margin/leverage-policy review; monitoring/sell discipline; final integration and audit; and any true
whole-universe allocation test.
