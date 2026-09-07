---
decision_id: VALUATION-0003
date: 2026-08-08
status: Proposed
category: valuation_archetype_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0005, VALUATION-0001, VALUATION-0002, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/VALUATION-0003-equity-valuation-archetype-assignment-authorization.md
---

## Context

### Authority for this unit

`governance/decisions/VALUATION-0002-equity-valuation-methodology-doctrine-adoption.md` §6.2 states that
real-company archetype-category assignment "is **not performed, sketched, or implied** by this
decision... This remains its own separate, later, explicitly authorized unit, requiring its own
governance filing naming the company or companies in scope, matching the first-coverage-discipline
precedent this repository has applied to every prior Company Intelligence expansion." `governance/
decisions/VALUATION-0001-equity-valuation-research-charter.md` §5 and `research/equity_valuation_study/
PROTOCOL_V1.md` §15 state the same thing in the same terms. This filing is that separate unit.

**This decision does not operate under `PROTOCOL_V1.md`'s own charter authority and does not amend,
extend, reopen, or reinterpret it.** Protocol §12's absolute prohibition on archetype-category
assignment of any real company remains fully binding **on that charter and that study** — the
seven-methodology-family × seven-archetype-category matrix comparison RQ1–RQ4 authorized. This filing
borrows only §5's closed, frozen taxonomy vocabulary **by reference, unedited**, as the classification
vocabulary for a wholly distinct governance unit — precisely the "separate, later, explicitly
authorized" pathway `VALUATION-0001` §5, `VALUATION-0002` §6.2, and protocol §15 all anticipated and
reserved, not an extension of the protocol's own charter.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-0003-archetype-auth-evtwbt` confirmed a fresh checkout of `origin/main` at
  `7640ade92edbb54f86e0c4b6ec123fc75eb7aa0c`, zero divergence (`git diff origin/main` empty), working
  tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit — no competing active
  mutation lane.
- **`VALUATION-0002` (PR #276) independently reconfirmed merged** via the GitHub API, not assumed:
  `merged: true`, `merged_by: Mast3rkey`, head `74840993fd75fff9f5ea53322f341bb109321b59`, base `main` @
  `9640069a0fb2a7b89e5681208664db2331af2860`, 5 changed files (+564/-21), 2 commits, merge SHA
  `7640ade92edbb54f86e0c4b6ec123fc75eb7aa0c` (matches this branch's own base exactly — independently
  confirmed via `git log`, not merely quoted from the authorizing task). `VALUATION-0002`'s own PR body
  independently re-read in full: adopts archetype-differentiated methodology selection and the
  false-precision specification as doctrine; explicitly authorizes neither archetype assignment nor
  valuation execution.
- **Canonical equity roster independently re-derived live from `targets.yaml`**, not assumed:
  `destination:` filtered to `asset_class: equity` yields exactly 27 tickers — `AMZN, ASML, AVGO, CEG,
  COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI,
  TMO, TSLA, TSM, V, WM` — matching the task's stated roster exactly, zero drift.
- **Zero archetype-assignment artifacts exist anywhere in the repository** — confirmed no
  `intelligence/valuation_archetype/` (or similarly named) directory exists at this commit.
- **`operations/WORKSTREAMS.yaml`'s `WS-0015` entry found stale**: `last_verified_main_sha` pointed at
  `5066168b681a0c720a52b61044f220e38d21ffda` (PR #275's own merge, predating `VALUATION-0002`'s later
  merge); `blocker`/`next_action` still described `VALUATION-0002`'s governance PR as unreviewed. This
  filing performs the deferred Lane M synchronization (§K below).
- **Full repository `pytest` baseline independently reproduced before any edit**: 3341 passed, 0 failed
  (one incidental, previously-disclosed, unrelated wall-clock-boundary flake in a review-log test,
  confirmed by isolated and full-suite re-run both green — matching `VALUATION-0002`'s own disclosed
  baseline exactly).
- **Decision catalog independently rebuilt**: 96 decisions, 0 issues, before this filing's own new
  entry.

## Decision

**This decision authorizes exactly one thing: a later, separate, bounded implementation PR that
assigns each of the 27 canonical equities a qualitative valuation-methodology archetype (or a
first-class abstention), under a blind/redacted drafting workflow, strict evidence boundaries, and
mandatory schema/validator coverage. It authorizes no valuation, no fair value, no price target, no
expected return, no RQ4 evidence-category design, and no `TIER-0009` resolution. Implementation does
not begin in this session.**

### A. What is authorized

One future, separate, bounded implementation PR that produces a governed archetype-assignment record
for all 27 canonical equities in one authorized cycle (§G — internally sharded, not separately
gated), plus a dedicated closed-schema validator and its test suite, plus one retained narrative audit.
That future PR requires its own full independent-review/correction/re-review/principal-acceptance/
merge/post-merge-verification lifecycle under `OPS-0007` §1 / `OPS-0009` Lane G before any content is
authoritative — nothing in §§B–J below is itself an assignment; it specifies what a later
implementation must do.

### B. Roster — exactly the 27 canonical equities, zero exclusions, zero additions

The population is fixed to the live `targets.yaml` `asset_class: equity` roster confirmed in Preflight:
`AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR,
RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM`. The future implementation must re-derive this list live
from `targets.yaml` at its own start (never copy this filing's own snapshot) and reconcile any drift
before drafting — matching `TIER-0004`/`TIER-0005`/`PI-0031`'s own population-reconciliation
discipline. Reading `targets.yaml` for this population check is a **structural identity lookup**, not a
judgment input (§D/§E draw that line precisely) — the same distinction `TIER-0004` §B and `REL-0001` §I
already drew for the identical purpose.

### C. Output vocabulary — closed, non-numeric

- **Primary** (`primary_archetype`): exactly one of `A`, `B`, `C`, `D`, `E`, `F`, `G` (protocol §5's
  seven labels, bound by reference — not restated here; a short parenthetical label may be carried in
  the record purely for human readability, e.g. `A (asset-light platform)`, but the seven substantive
  descriptions themselves are never copied into the record or this decision) — **or** the closed
  abstention value `unable_to_determine_archetype`. No eighth category, no numeric code, no blended or
  hyphenated value (matching `PI-0004`'s own closed-vocabulary discipline for `conviction.rating`).
- **Secondary** (`secondary_archetype`, nullable): zero or exactly one of `A`–`G`. `secondary_archetype
  != primary_archetype`, mechanically enforced. **`secondary_archetype` must be `null` whenever
  `primary_archetype == unable_to_determine_archetype`** — a secondary tag on an abstained record would
  assert partial classification exactly where the abstention states none is supportable; this is a
  closed, mechanical rule, not a case-by-case judgment.
- **The archetype-F test, mandatory before any secondary is assigned.** A secondary archetype exists to
  record genuine, evidenced dual-fit — it must never be used as a workaround for skipping a serious
  test of whether `F` (diversified/multi-segment) is the correct **primary** for a company whose
  Company Intelligence record discloses materially different economics across segments. Whenever (a) a
  secondary archetype is assigned, or (b) the ticker's own Company Intelligence record discloses
  multi-segment or materially diversified economics, the record's `rationale` must explicitly state
  whether `F` was considered for primary and why `F` was or was not selected. A record that assigns a
  secondary archetype without this disclosure fails validation.
- **No numeric score, weight, confidence percentage, or ranking of any kind anywhere in the output** —
  the vocabulary is categorical only, matching `TIER-0002`/`XASSET-0002`/`XASSET-0005`'s own
  no-composite-score discipline.

### D. Permitted evidence inputs

Existing repository evidence only, per company, drawn from that company's own already-sealed Company
Intelligence record (`intelligence/companies/<TICKER>.yaml`/`.md`):

- Business-model / thesis narrative.
- `sector`/`industry` — **suggestive context only, never mechanically determinative**; a company's
  sector label does not by itself resolve its archetype (e.g., a "technology" company can be asset-light
  platform, capital-intensive infrastructure, or early-stage/binary depending on its actual economics).
- `competitive_advantages`.
- `risks[]`.
- `catalysts[]`.
- The sealed Milestone 6 `economic_role.role_basis` narrative (`intelligence/classification/
  <TICKER>.yaml`) — **read as contextual evidence only, never as a substitute classification**; Milestone
  6's `economic_role` axis answers a different question (portfolio-relationship economic role) than this
  filing's archetype axis (valuation-methodology fit), and the two must not be conflated or copied
  wholesale from one into the other.
- A **sanitized fact about**, never the literal text of, `gates.yaml`'s `next_gate` entry: exactly
  (a) that a gate exists for the ticker, and (b) whether that gate's `next_gate` text references
  valuation (a single boolean-shaped fact mechanically established by the redaction mechanism, §F —
  never read directly by a blind drafter) — for disclosure as portfolio context in the record's own
  `portfolio_context` metadata only (§H). **The literal `next_gate` text itself — including any named
  peer or comparator, methodology framing, or price/valuation language it contains — must never reach
  a blind drafter and must never appear in any sealed record.** This sanitized fact is **never** an
  input to, or justification for, the primary or secondary archetype determination itself (§E).

### E. Prohibited evidence inputs — binding on the blind drafting workflow

The assignment workflow must not use, and the redaction/isolation mechanism (§F) must prevent a blind
drafter from receiving:

- `portfolio_role_ref`.
- `conviction.rating`.
- Any `targets.yaml` `target_pct` or other allocation weight value.
- `gates.yaml` gate/`allow_add` status **as assignment evidence**, and the literal `next_gate` text in
  any form — the redaction/isolation mechanism (§F) may pass through only the two sanitized facts §D
  specifies (that a gate exists; whether its `next_gate` text references valuation), never the text
  itself and never any peer name, comparator, methodology framing, or price/valuation language the text
  contains. Neither the gate/`allow_add` status nor the sanitized topic-flag may ever determine, or be
  cited as supporting, an archetype choice.
- Any chart, technical-indicator, or screenshot-derived evidence of any kind, including any
  `CHART-0001`/`CHART-0002` record, fresh or historical.
- Any allocator output (`allocate.py`, `--review`/`--health`/`--levels` output).
- Any margin state (`margin_state.py` output, `holdings.yaml` margin fields).
- Any trade or order history.
- Any Milestone 7 (`intelligence/reconciliation/`) or Milestone 8 (`intelligence/recommendations/`)
  finding for the ticker.

### F. Blindness / redaction requirement — proof required, not a prose instruction

The future implementation must build a dedicated redaction mechanism (e.g.
`valuation_archetype_sanitizer.py`, freshly authored, not a copy of `intelligence_classification_
sanitizer.py` — the prohibited-field sets differ, matching this repository's "each Intelligence schema
owns its own validator/sanitizer" convention established at `XASSET-0002`/`crypto_classification_
validator.py`) that:

1. Strips `portfolio_role_ref`, `conviction`, and any `review.log` narrative wholesale from each
   ticker's Company Intelligence `.yaml` before a blind-drafting session ever sees it.
2. Item-level-scans and redacts the retained fields (`risks[].risk`, `competitive_advantages[]`,
   `catalysts[].catalyst`, `sources[].note`) for leaked target/allocation/gate-status/conviction/
   chart-domain language, and scans the retained `.md` narrative for the same, including whole-section
   removal for any section whose *title* names a prohibited topic (a "Conviction," "Governed policy,"
   or "Capital-priority discipline" heading, matching the exact defect classes `TIER-0004`'s own
   BLOCKING/MAJOR corrections found and fixed in the Milestone 6 sanitizer: bare-noun policy leakage
   past an adjective-only pattern list, and dangling references to a stripped section surviving
   elsewhere in the same document).
3. Runs a **mandatory, mechanistically independent** second-stage re-scan of the redacted output — built
   from a materially different check than the strip-decision logic itself (never the same function
   called twice), per `TIER-0004`'s own corrected design and its own disclosed lesson that reusing one
   function for both strip and verify is a false independence claim.
4. The future implementation PR must **prove**, not merely assert, that each blind-drafting session
   received only the sanitized package — e.g., by having each shard's drafting session read exactly one
   sanitized artifact per ticker and nothing else, and by running the independent second-stage scan
   against every sealed record's own free-text fields (`rationale`, any disclosed-conflict text) after
   sealing, rejecting on any prohibited-field or prohibited-language hit. This instructional (not
   filesystem-sandboxed) isolation boundary must be disclosed as such in the implementation's own
   audit, matching `TIER-0004` §9.2's and Milestone 6's own honest disclosure of the identical
   limitation — this filing does not require inventing a stronger isolation guarantee than this
   repository's own established practice already provides.
5. `sector`/`industry` may pass through unredacted (§D) — they are permitted evidence, not prohibited.

### G. Batch / shard structure — one authorized cycle, internally sharded

All 27 companies are authorized for assignment in **one implementation cycle** — no per-batch
governance gating (unlike the Company Intelligence `PI-####` batch series, this archetype axis draws
only on already-sealed, already-reviewed evidence, so the first-coverage risk that justified batching
Company Intelligence research does not apply here). The future implementation must internally divide
the 27 into **shards of approximately 5–6 companies each** (five shards, matching Milestone 6's own
shard size) purely as a drafting- and review-quality unit — **shards carry no independent governance
authority**; they do not require separate authorization, separate PRs, or separate principal
acceptance. One primary session integrates and seals all shard output into one coherent implementation
PR, matching Milestone 6's own single-authoring-session-with-read-only-shard-drafting precedent
(`TIER-0005` §I).

### H. Output contract — governed record schema

The future implementation's governed structure (smallest schema compatible with existing repository
precedent — a single-YAML-per-ticker, filesystem-is-the-index convention, matching `intelligence/
classification/`, `intelligence/etf_classification/`, and `intelligence/crypto_classification/`, not
the paired-YAML+Markdown Company Intelligence convention, since this axis is a structured judgment
record, not a narrative thesis document) must be `intelligence/valuation_archetype/<TICKER>.yaml` plus
one `COHORT_MANIFEST.yaml`, with at minimum:

- `schema_version`, `ticker`.
- `primary_archetype` (§C).
- `secondary_archetype` (nullable, §C).
- `rationale` — cited to specific Company Intelligence evidence (business-model narrative, disclosed
  segments, disclosed competitive dynamics), including the mandatory archetype-F test disclosure where
  applicable (§C).
- `evidence_quality` — reusing this repository's existing `primary_source_coverage` vocabulary
  (`comprehensive`/`partial`/`limited`/`blocked`, matching `TIER-0002`/`XASSET-0002`) plus a required,
  ticker-specific uncertainty statement (structurally comparable to `evidence_quality.thesis_
  uncertainty_statement` elsewhere in this repository).
- `disclosed_evidence_conflicts` (nullable list) — any genuine conflicting evidence found in the
  Company Intelligence record bearing on archetype fit must be disclosed here, never silently resolved
  in one direction without disclosure (matching this repository's established practice, e.g. `VWO`'s
  disclosed China-weight conflict in `XASSET-0003`'s implementation).
- `evidence_gap_statement` (nullable) — **required, non-empty, specific** when `primary_archetype ==
  unable_to_determine_archetype`; **must be absent (`null`)** on every determined record (structurally
  distinguishable, not merely value-distinguishable, matching `TIER-0004` §F's identical rule for
  `economic_role`'s own abstention path).
- `portfolio_context` (optional, disclosure-only sub-object) — may record that a `gates.yaml` gate
  exists and that its `next_gate` text references valuation, **labeled explicitly as portfolio context,
  never as archetype-determining evidence** (§D).
- Lifecycle/provenance fields matching repository precedent: `lifecycle_status: sealed`, `sealed_at`,
  `governing_decision: VALUATION-0003`, `drafting_session_or_shard_id`, `cohort_manifest_entry`,
  `content_sha256`.

No numeric field of any kind (matching `XASSET-0005`'s stricter-than-ETF no-numeric-field design,
appropriate here since even the ETF framework's sole numeric carve-out, `expense_ratio_pct`, has no
analogue in a qualitative archetype-fit judgment).

### I. Validation required of the future implementation

The future implementation PR must include, at minimum:

- A dedicated `valuation_archetype_validator.py` (closed schema, rejects extra keys at every level,
  zero import coupling with `allocate.py`/`margin_state.py`) plus its own focused test suite.
- Primary-vocabulary validation (exactly the eight closed values, §C).
- Secondary-vocabulary and cardinality validation (zero or one of `A`–`G`; `secondary_archetype !=
  primary_archetype`; `secondary_archetype` forced `null` when `primary_archetype ==
  unable_to_determine_archetype`).
- Abstention-requires-`evidence_gap_statement` enforcement, and the converse (a determined record must
  have `evidence_gap_statement == null`).
- The archetype-F-test disclosure check (§C) wherever a secondary is present or segment-diversity
  evidence exists in the source record.
- Complete 27-name roster check against a live `targets.yaml` re-derivation (not a hardcoded list),
  with duplicate- and missing-ticker detection.
- A prohibited-field / prohibited-language scan of every free-text field (`rationale`,
  `disclosed_evidence_conflicts`, `evidence_gap_statement`) for `portfolio_role_ref`, `conviction`,
  numeric target/percent-of-book patterns, gate-policy language, and the full chart-domain term list
  already established by `recommendation_validator.py`/`reconciliation_validator.py` — built as an
  independently-derived scan from the start, not merely a self-declared flag (learning directly from
  `reconciliation_validator.py`'s own disclosed MINOR defense-in-depth gap).
- Proof-of-redacted-input-workflow tests (§F.4) — at minimum, tests demonstrating the sanitizer strips
  every prohibited field/pattern from representative fixtures and that the independent second-stage
  scan uses a materially different code path than the strip logic.
- Repo-wide YAML/YML and JSON parse checks, `git diff --check`, an exact changed-file inventory, and a
  full protected-path scan (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`,
  `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, every existing `intelligence/**` record,
  `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, every other `governance/decisions/*.md` — zero
  diff on all of them).
- Full repository `pytest` and every applicable pre-existing repository validator (`classification_
  validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`, `relationship_
  validator.py`, `intelligence_validator.py`, `freshness_validator.py`, `contender_registry_validator.py`,
  `etf_classification_validator.py`, `crypto_classification_validator.py`) run clean.
- Decision-catalog reconciliation (this filing's own new entry accounted for).
- Exact-head CI green on the implementation PR before it may be marked ready.

### J. Stop conditions — no silent roster contraction

If evidence for one or more of the 27 companies is insufficient or materially conflicting, the future
implementation must record `unable_to_determine_archetype` with a specific `evidence_gap_statement` for
that ticker and **retain it in the authorized 27-name roster** — dropping a ticker from the output,
narrowing the batch, or silently omitting a company is not permitted under any circumstance (matching
`PI-0024`'s own "no license to silently narrow the batch" discipline and `TIER-0004`/`TIER-0005`'s own
population-completeness requirement). A first-class abstention is a complete, valid, and expected
possible outcome for any ticker — not a defect requiring escalation before the implementation PR may be
opened.

### K. Register synchronization (Lane M, this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives, additive only — no existing gate's own text
edited:

1. A new `valuation0002-doctrine-adoption-pr-merged` gate recording this session's independently
   reconfirmed PR #276 facts: merge SHA `7640ade92edbb54f86e0c4b6ec123fc75eb7aa0c`, principal
   acceptance `issuecomment-5226649304`, merge-commit CI run `31263265804` success.
2. A new `valuation0003-archetype-assignment-authorization` gate (`status: in_progress`, `pr: null` —
   this filing does not mark its own unmerged work complete, matching every prior filing's identical
   self-reference discipline in this repository).
3. `status` remains `proposed` (authorizing archetype assignment does not itself complete `WS-0015`'s
   broader charter-and-doctrine objective — a future implementation, and any further future
   application-phase authorization, remain separate later steps). `priority` remains `secondary`.
   `dependencies` remains `[]`.
4. `active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`, `blocker`, and
   `next_action` updated to this filing's own live state; `authorized_by` updated to record this
   filing.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### L. Non-authority — explicit, exhaustive

This decision authorizes no:

- Actual valuation computation, fair value, price target, expected return, or upside/downside
  calculation for any real company.
- DCF input, discount-rate design, peer-multiple selection, or scenario-probability assignment for any
  real company.
- RQ4 evidence-category schema design — remains its own separate, later, explicitly authorized unit
  (`VALUATION-0002` §4/§6.3).
- Resolution, closure, or narrowing of `TIER-0009` §K's `valuation_required` status on any equity.
- Target, tier, holdings, gate, capital-priority, cap, cluster, or allocator change of any kind.
- Margin policy, buy-ladder, chart ingestion, or chart interpretation of any kind.
- Any order or trade.
- Any edit to `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `VALUATION-0001`, or
  `VALUATION-0002`.
- Any actual archetype assignment, valuation, or chart analysis of any real company **by this filing
  itself** — this filing authorizes a future implementation; it performs none of that work.

### M. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0003-equity-valuation-archetype-assignment-authorization.md` (this
   file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0003`).
3. `operations/WORKSTREAMS.yaml` (§K above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 96 → 97).

**No other file is touched.** No production code, no `intelligence/**` record, no `PROTOCOL_V1.md` or
`METHODOLOGY_EVALUATION_REPORT.md`, no `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`.

### N. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (`OPS-0009` Lane G — new authorization, full weight, never reduced),
complete any required bounded correction and exact-head re-review, and receive explicit principal
acceptance before it may be marked ready or merged. **This decision does not mark itself ready and does
not authorize its own merge.** No archetype-assignment implementation PR may open, and §§A–J above are
not effective, until this PR merges to `main`.

## Rationale

**Why archetype assignment can proceed before RQ4 closure while valuation execution cannot.** `RQ4`'s
gap (`VALUATION-0002` §4) is that the Company Intelligence schema lacks financial-statement,
discount-rate, peer-set, or scenario-probability fields — evidence a *valuation computation* requires.
Archetype categorization (protocol §5) is a qualitative business-model classification — asset-light vs.
capital-intensive vs. financial-intermediation vs. commodity/cyclical, etc. — answerable from the
business-model narrative, segment structure, and disclosed competitive dynamics already present in
every sealed Company Intelligence record, the same class of evidence Milestone 6's own `economic_role`
axis already drew on successfully. Requiring RQ4 closure before this qualitative step would conflate
two evidence needs that the report and `VALUATION-0002` §4 already keep distinct.

**Why one authorized cycle rather than per-batch governance gating, unlike Company Intelligence
research.** The Company Intelligence `PI-####` batch series gates each batch separately because each
batch performs genuinely new external research with its own source-access risk. This axis performs no
new research — it classifies already-sealed, already-reviewed Company Intelligence evidence against a
frozen, closed taxonomy. The first-coverage risk that justifies per-batch gating there does not apply
here, matching `TIER-0005`'s own single-authorization-for-all-27 precedent for Milestone 6's
structurally identical situation (also a classification task over already-sealed evidence, also
authorized in one cycle with internal shards only).

**Why a blindness/redaction requirement at all, given no portfolio-policy field appears in protocol
§5's taxonomy.** The risk is not that the taxonomy needs portfolio data — it doesn't — but that an
un-redacted Company Intelligence record carries `portfolio_role_ref`/`conviction.rating` alongside the
permitted business-model evidence in the same file, creating exactly the contamination-without-intent
risk Milestone 6's own three correction rounds demonstrated is real (bare-noun gate-policy leakage,
dangling section references, a catalyst-field leak) rather than hypothetical. Requiring the same
proof-based redaction discipline here, rather than a prose "please ignore these fields" instruction,
directly applies the most expensive lesson this repository's own governance history has already paid
for.

**Why `category: valuation_archetype_governance`, a new category distinct from `VALUATION-0002`'s
`valuation_methodology_governance`.** `VALUATION-0002` adopts *methodology-selection* doctrine (which
family fits which archetype). This filing authorizes *archetype-assignment* work (which archetype fits
which real company) — a structurally distinct governance act, matching the precedent `TIER-0001`
established when it took its own new category (`tier_classification_governance`) distinct from
adjacent categories for a decision playing a structurally different role in the same overall program.

## Alternatives Considered

- **Fold archetype assignment into a combined filing that also performs one illustrative valuation.**
  Rejected outright — protocol §12 bars any valuation of a real company "including as a 'worked
  example'" under the charter, and `VALUATION-0002` §6.3 requires archetype assignment (step 2) to
  complete *before* valuation execution (step 3) may even be proposed; combining them here would violate
  that explicit sequencing the principal has already set.
- **Authorize archetype assignment company-by-company, matching the Company Intelligence `PI-####`
  batch-gating pattern.** Rejected — as the Rationale states, this axis carries no new external-research
  risk per company; batching 27 separate governance filings for a classification task over already-sealed
  evidence would be pure process overhead with no corresponding risk reduction, and the principal's own
  authorization parameters explicitly requested one cycle.
- **Skip the blindness/redaction requirement since the taxonomy itself needs no portfolio data.**
  Rejected — the risk is incidental co-location of prohibited fields in the same source file, not
  taxonomy need; Milestone 6's own three-round correction history is direct, repository-specific evidence
  this risk is real.
- **Allow a secondary archetype without the mandatory archetype-F disclosure test.** Rejected per the
  principal's own explicit instruction — a secondary tag must not become a way to avoid seriously testing
  whether a diversified company's primary should be `F`.

## Bounded Correction (same day, this PR)

An independent exact-head review of the original head (`5929eb6a87fc4ec0fa275181947a759d25134827`)
returned **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE** — 0 BLOCKING / 0 MAJOR / 1 MINOR / 1
non-actionable NOTE. **MINOR, resolved**: §D, §E, and §H described the permitted scope of `gates.yaml`
`next_gate`-text disclosure inconsistently — §D's original wording ("`next_gate` text, read-only, for
disclosure") could be read as permitting the literal text; §E's original wording narrowed this to "mere
existence"; only §H was already correctly narrowed to a fact-about-the-text ("exists" + "references
valuation"). The reviewer independently confirmed this is not academic: live `gates.yaml`'s real SPGI
`next_gate` value — *"Review one clean post-spin quarter and normalized SPGI-versus-MSCI valuation,
leverage, and growth comparison"* — names an external peer comparator (MSCI, not a member of the
27-name governed roster) and carries explicit valuation-methodology framing, exactly the kind of
content a literal reading of §D's original wording could have let leak into a sealed record.

**Resolved by narrowing §D and §E to §H's already-correct formulation**, not by loosening §H: §D now
states the permitted input is "a sanitized fact about, never the literal text of," the `next_gate`
entry — exactly two boolean-shaped facts (a gate exists; whether its `next_gate` text references
valuation) — with the literal text, any named peer/comparator, methodology framing, or price/valuation
language explicitly barred from ever reaching a blind drafter or appearing in any sealed record. §E's
prohibited-evidence entry is symmetrically tightened to state the redaction mechanism (§F) may pass
through only those same two sanitized facts, never the text itself. §H's own wording is unchanged — it
was already the target formulation, confirmed correct by the review.

No other section is touched by this correction: the 27-company roster, the archetype taxonomy, the
secondary-archetype policy and mandatory archetype-F test, the RQ4 boundary, the blindness/redaction
architecture (§F, other than the pre-existing pointers to §D), the batch/shard structure (§G), the
output contract's other fields (§H), and the non-authority/prohibited scope (§L) are all unchanged. The
reviewer's one NOTE (an imprecise citation to `VALUATION-0001` §5 in the Context section) was
independently confirmed non-actionable and is not corrected here, per the review's own explicit
disposition and this correction's own narrow, bounded scope.

Full validation re-run clean at the corrected head: focused decision-catalog tests, full repository
`pytest`, all 9 applicable validators, decision-catalog reconciliation, repo-wide YAML/YML and JSON
parsing, `git diff --check`, exact changed-file inventory (one file: this decision document), and a
full protected-path scan all pass — see the PR's own validation record for exact figures. Requires its
own fresh independent exact-head delta review before this PR may be considered ready.

## Consequences

**What changes.** A future, separate implementation PR may now be opened to assign all 27 canonical
equities a qualitative valuation archetype (or abstention) under this filing's binding schema, evidence
boundary, redaction-proof, and validation requirements — but only after this governance PR itself is
independently reviewed and principal-accepted. `WS-0015`'s register entry reflects `VALUATION-0002`'s
confirmed merge and this filing's own authorization step.

**What does not change.** No real company has been assigned an archetype. No real company has been
valued. `TIER-0009` §K's `valuation_required` status is unchanged on all 27 equities. `PROTOCOL_V1.md`
and `METHODOLOGY_EVALUATION_REPORT.md` are unedited. No target, tier, holdings, gate, cap, cluster,
allocator, margin, or ladder value changes. No Company/Theme/relationship/classification/
reconciliation/recommendation Intelligence record changes. No chart evidence of any kind is consumed.
`WS-0005` and `WS-0014` are unaffected.
