---
decision_id: TIER-0013
date: 2026-08-07
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0037, REL-0001, REL-0004, REL-0006, REL-0007, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0008, TIER-0009, TIER-0010, TIER-0011, TIER-0012, CHART-0001, CHART-0002, LADDER-0001, OPS-0016, CONTENDER-0001, XASSET-0001]
supporting_artifact: null
file: governance/decisions/TIER-0013-ws0005-milestone5-completion-determination.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1) unit
to determine, on live repository and GitHub evidence independently re-verified this session,
whether WS-0005 Milestone 5 ("Zero-based classification and tier-architecture review," `OPS-0006`
§4.5) is formally complete — the one remaining formally-open WS-0005 roadmap gate `TIER-0012`
disclosed but was not authorized to resolve — and, only if so, whether WS-0005's own top-level
`status` may now transition from `in_progress` to `complete`. This authorization does not authorize
any redesign of `TIER-0002`'s framework, any new classification content, any correction to
`intelligence/companies/LLY.yaml`, any new research, any tier/target/holdings/gate/cap/cluster/
allocator/margin/ladder/chart change, or any trade or order.

### Preflight (independently verified this session, not assumed from the authorizing brief)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, starting branch `claude/ws-0005-milestone-5-completion-5dk36x`,
  working tree clean at session start. This filing itself was authored on a fresh branch,
  `claude/ws0005-milestone5-completion-9fq2la`, cut from that verified starting point.
- **`origin/main` fetched and reconciled.** `git fetch origin main` succeeded; `git rev-parse
  origin/main` and the starting branch's own `git rev-parse HEAD` both returned
  `31b2674be7024662b696352e80c0079e7d0744ca` — `TIER-0012`'s own merge commit (PR #266) — confirmed
  identical, clean working tree, before any edit in this filing.
- **PR #266 (`TIER-0012`) independently re-confirmed merged** via the GitHub API: merge commit
  `31b2674be7024662b696352e80c0079e7d0744ca`, title "TIER-0012: WS-0005 Milestone 9 completion
  determination — MILESTONE 9 COMPLETE," `merged: true`.
- **Zero open pull requests** confirmed via `mcp__github__list_pull_requests` (`state: open`) —
  empty result both before drafting and immediately before pushing this branch. No active mutation
  lane exists.
- **`TIER-0013` independently confirmed the next unused identifier.** `governance/decisions.yaml`
  contains exactly 89 `decision_id` rows (`TIER-0012` the highest-numbered `TIER-####` entry);
  `portfolio_hq.dashboard.decisions.build_catalog('.')` → **89 decisions, `issues == ()`**,
  independently reconciled this session. `mcp__github__search_code` for `"TIER-0013"` across the
  full repository returns zero results; a full-repository grep for the literal string `TIER-0013`
  (excluding `.git/`) also returns zero results.
- **All nine `OPS-0006` §4 milestone gates individually re-read** via direct line inspection of
  `operations/WORKSTREAMS.yaml` (not text search, not inference from CLAUDE.md's own prose), before
  any edit:

  | Gate | `status` | `pr` | `date` |
  |---|---|---|---|
  | `milestone-1-baseline-and-inventory` | `complete` | 151 | 2026-07-25 |
  | `milestone-2-intelligence-coverage-and-freshness-audit` | `complete` | 151 | 2026-07-25 |
  | `milestone-3-intelligence-completion` | `complete` | null | 2026-08-03 |
  | `milestone-4-portfolio-relationship-mapping` | `complete` | null | 2026-08-04 |
  | `milestone-5-zero-based-classification-and-tier-architecture-review` | **`proposed`** | null | 2026-07-25 |
  | `milestone-6-blind-classification` | `complete` | 253 | 2026-08-05 |
  | `milestone-7-baseline-reconciliation` | `complete` | 259 | 2026-08-06 |
  | `milestone-8-policy-recommendation-package` | `complete` | 262 | 2026-08-07 |
  | `milestone-9-independent-review-and-later-adoption` | `complete` | 265 | 2026-08-07 |

  **Milestone 5 is the sole remaining `status: proposed` gate**, unedited since `TIER-0001` first
  added it on 2026-07-25 — every later Milestone-5-adjacent filing (`TIER-0001` itself,
  `tier0001-post-merge-verification`, `TIER-0002`) explicitly declined to advance it, each stating
  in its own text that it "remains accurate for the milestone as a whole" and that closing it
  requires its own separate, later, dedicated filing. This filing is that filing.
- **`operations/WORKSTREAMS.yaml`'s `tier000#` sub-gate inventory independently re-read in full**
  (`grep -n "gate: tier000"`): exactly four exist — `tier0001-classification-question-inventory-
  bounded-unit`, `tier0001-post-merge-verification`, `tier0002-candidate-framework-design`, and
  `tier0006-post-merge-verification`. **No `tier0002-post-merge-verification` gate exists anywhere
  in the file** — confirming, by direct inspection rather than by trusting `TIER-0012`'s own
  disclosure, that `TIER-0002`'s post-merge state was never synchronized into the register, exactly
  the gap `TIER-0012` found and could not close within its own authorized scope.
- **`TIER-0001` (PR #245) independently re-confirmed via the GitHub API**, not taken on faith from
  any prior filing's summary: `merged: true`, merge commit
  `96020e55b5317aa6191733e22d2df84bea4a6574`. Review chain independently re-read: exact-head review
  `4859945925` (CHANGES REQUIRED — 2 MAJOR: overstated 19/27-vs-actual-13/27 risk-concentration
  coverage-gap arithmetic in the retained artifact; a premature `status: complete`/`pr: 245` on this
  workstream's own still-open gate — plus 1 MINOR, 1 NOTE), correction commit `eed05c07`, delta
  review `4860022747` ("DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE," zero
  remaining findings), retained principal-acceptance comment `issuecomment-5186141437` (exact head
  `eed05c07c2604a18466f345a1bb9c8877705f5a2`), retained post-merge-verification comment
  `issuecomment-5186176928`.
- **`TIER-0002` (PR #246) independently re-confirmed via the GitHub API this session** — read in
  full, not merely cited: `merged: true`, base `96020e55b5317aa6191733e22d2df84bea4a6574`, head
  `bc63a03c05e7dc8736fdd0078ece805c152dbe42`, merge commit
  `24be14552b0e5caed8052e07497855cde6a37085` (parents the base and the accepted head; merge-commit
  tree independently confirmed byte-identical to the accepted head's own tree per the retained
  post-merge comment). `merged_at: 2026-08-05T01:29:19Z`, exactly 6 changed files (503 insertions,
  6 deletions). Full review/acceptance/verification chain independently re-fetched and read in full
  this session:
  - Exact-head review `4860208858` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING /
    0 MAJOR / 0 MINOR / 1 NOTE (a pre-existing, clone-path-sensitive test assertion unrelated to
    this PR's content, independently diagnosed and disclosed as not actionable). Fourteen numbered
    verification points, each independently checked against file content by that reviewer (not the
    PR's own narrative): the four-axis match to `TIER-0001` §6 exactly; zero ticker classified; zero
    `intelligence/classification/` file created; byte-identical protected paths; explicit fact/
    judgment labeling on every field; the rejected-alternative reasoning; correct non-destructive
    register synchronization; validators and CI all green at the exact reviewed head. **No
    correction round was required** — a single-round, zero-finding approval, unlike `TIER-0001`'s
    two-round chain.
  - Principal acceptance `issuecomment-5186480372` — independently re-read in full: explicit
    acceptance at exact head `bc63a03c05e7dc8736fdd0078ece805c152dbe42`, naming review
    `4860208858` and exact-head CI (workflow run `30964877971`, job `92176578867`,
    `completed`/`success`).
  - Post-merge verification `issuecomment-5186508964` — independently re-read in full: merge-commit
    tree identity confirmed, exact 6-file merged inventory, decision catalog 73/`issues == ()`,
    `intelligence_validator.py`/`freshness_validator.py`/`relationship_validator.py` all clean,
    183/183 focused and 2581/2581 full-suite tests, `git diff --check` clean, every protected path
    byte-identical to base, exactly one `priority: primary` workstream, merge-commit CI (workflow
    run `30966516781`, `completed`/`success`). **This comment is the one that explicitly disclosed
    the gap this filing closes**: "No separate factual-synchronization filing is required right
    now — this comment itself is the retained post-merge verification record, and the next WS-0005
    session's own preflight is the correct, precedented place to add the
    `tier0002-post-merge-verification` gate entry... The pre-existing
    `milestone-5-zero-based-classification-and-tier-architecture-review` gate stays
    `status: proposed`."
- **The candidate classification framework's persistence, independently verified by direct source
  inspection, not inferred from any narrative summary**: `classification_validator.py`'s live
  `_FOUR_AXES` constant, at this session's starting `HEAD`, reads exactly
  `("economic_role", "capital_priority", "risk_concentration", "evidence_quality")` — the identical
  four axes, in the identical order, that `TIER-0002` §2 designed and that `TIER-0001` §6
  independently narrowed to from nine candidates. No fifth axis, no renamed axis, no dropped axis,
  anywhere in the currently-merged validator that Milestone 6, 7, and 8 all actually executed
  against.
- **Live validators and full suite independently re-run this session** against the exact starting
  `HEAD` above, before any edit:
  - `classification_validator.py` (direct CLI run) — **OK (28 result(s))**.
  - `reconciliation_validator.py` — **OK (27 tickers)**.
  - `recommendation_validator.py` — **OK (27 tickers)**.
  - `relationship_validator.py` — **OK (13 record(s))**.
  - `intelligence_validator.py` — exit 0 (clean, 53 companies, 2 themes).
  - `freshness_validator.py` — **OK**.
  - `contender_registry_validator.py` — **OK (84 entries)**.
  - `python3 -m pytest -q` (full repository suite, after installing `requirements.txt`'s pinned
    dependencies into this session's own environment, which lacked them at session start) — **3091
    passed, 0 failed** in 203.86s — matching every immediately-prior WS-0005 filing's own reported
    baseline exactly.
  - Repository-wide YAML/YML parsing (all `.yaml`/`.yml` files, `.git/` excluded) — zero errors.
    Repository-wide JSON parsing — zero errors.
  - `git diff --check` — clean. `git status --porcelain` — empty throughout preflight.
- **`intelligence/companies/LLY.yaml` independently confirmed unedited**: `catalysts[0].expected`
  still reads `"2026-08-31"` — the `PI-0039`-identified, `TIER-0011`/PR #265-carried-forward MINOR
  finding remains exactly as every prior filing left it, not touched by this filing.
- **`WS-0005`'s live top-level state independently re-read**: `status: in_progress`,
  `priority: primary`, `dependencies: []` — confirmed via direct line inspection, not copied from
  any prior filing's summary.
- **Protected-path isolation confirmed for this session's own preflight** (before any edit):
  `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
  `margin_state.py`, `levels.py`, every existing `intelligence/classification|companies|themes|
  relationships/` record, `COHORT_MANIFEST.yaml`, `intelligence/reconciliation/
  MILESTONE7_BASELINE_RECONCILIATION.yaml`, and `intelligence/recommendations/
  MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml` all confirmed present and unmodified from the
  starting `HEAD` — `git status --porcelain` empty confirms no stray local change exists to
  accidentally carry into this filing's diff.

No condition on this unit's own stop list was triggered: `main` had not advanced past the expected
merge SHA; no overlapping mutation lane exists; the next `TIER-####` identifier (`TIER-0013`)
matched expectation; no gate had reopened; live evidence did not contradict `TIER-0001`'s or
`TIER-0002`'s own review/acceptance/post-merge-verification chains; a clean isolated workspace was
established without incident.

## Decision

**`TIER-0013` determines, on live repository and GitHub evidence independently re-verified this
session, that WS-0005 Milestone 5 ("Zero-based classification and tier-architecture review") is
formally complete, and accordingly sets the
`milestone-5-zero-based-classification-and-tier-architecture-review` gate's `status` to `complete`
in `operations/WORKSTREAMS.yaml`.** Because this is the last of the nine `OPS-0006` §4 roadmap
gates to reach `complete`, this filing additionally determines, from `OPS-0006`'s own controlling
text, that WS-0005's top-level `status` transitions from `in_progress` to `complete` — **the
roadmap's own nine-milestone scope is fully executed** — while explicitly, repeatedly stating what
that closure does and does not mean (§D, §E below). This decision authorizes no Milestone 10 of any
kind (none exists), no adoption action, no numeric valuation, no whole-portfolio target, no
cross-asset synthesis, no ETF/crypto work, no chart deployment, no external research, and no tier/
target/holdings/gate/cap/cluster/allocator/margin/ladder/order/trade change of any kind. It creates
no investment, allocation, or trading authority.

### A. Milestone 5 completion criteria — derived from controlling text, evaluated fresh against live state

No prior filing enumerated a numbered Milestone 5 completion standard the way `REL-0004` did for
Milestone 4 or `PI-0031` did for Milestone 3. `OPS-0006` §4.5's own controlling text (quoted in
full, not restated, per the reference-not-restate discipline `TIER-0005`/`TIER-0007`/`TIER-0008`/
`TIER-0010` all applied — **corrected by bounded correction, independent review: the version
originally presented here was a compressed paraphrase, omitting the seven-concept candidate-
separation clause below, and is now replaced with the actual full text**) is: *"What questions the
current tier system answers; where it mixes unrelated concepts; whether one tier label is adequate;
the smallest set of candidate frameworks the evidence supports; candidate separation, where useful
and not required merely because listed, of economic role, business quality, thesis uncertainty,
capital priority, position boundaries, overlap constraints, and review cadence; rejection of
unnecessary complexity; no single mechanical conviction score substituting for judgment."*
`TIER-0001`'s own nine-question inventory independently corroborates that this fuller canvassing —
covering business quality, position boundaries, and review cadence alongside the four axes
`TIER-0002` ultimately retained — actually took place: `TIER-0001` §6 explicitly found position
boundaries already served by `target_pct`, review cadence already served by Company Intelligence's
own `review.cadence_days` field, and business quality folded into the retained axes' evidence
sources, rather than silently narrowing scope without addressing them. Unlike Milestones 3/4/6/7/8,
Milestone 5 is a design
milestone, not a content-production milestone — it has no artifact of its own analogous to a
Company Intelligence record, a relationship record, a sealed classification, a reconciliation, or a
recommendation package. Its "deliverable" is the framework itself, and the only evidence capable of
confirming that framework is genuinely "the smallest structure that materially improves portfolio
decisions" (`TIER-0002`'s own authorizing instruction, quoted at Context) is whether later
milestones could actually execute against it without requiring a redesign — evidence that did not
exist at `TIER-0002`'s own merge time (2026-08-05) but exists now, after Milestones 6, 7, and 8 have
each independently consumed the same four-axis framework to completion.

This filing therefore derives ten criteria directly from `OPS-0006` §4.5, `TIER-0001`, `TIER-0002`,
`OPS-0001` (register semantics), `OPS-0006` §16.1 (a milestone reaches `complete` only after every
authorized deliverable exists, merges, passes its tests/validators, and the register/decision
catalog are synchronized — never from discussion, an edit, a commit, a push, or an open PR alone),
and `OPS-0007` §1 / `OPS-0009` §6 (the capability-based independent-review standard and the
delta-review discipline for material findings) — then evaluates each fresh against live repository
and GitHub state, per this repository's own established discipline of not inferring completion from
any prior filing's own summary (`PI-0037`, `REL-0006`, `TIER-0006`, `TIER-0008`, `TIER-0010`,
`TIER-0012`).

**Criterion 1 — Governing Milestone 5 units exist and are merged.**
*Standard:* `TIER-0001` (classification-question inventory) and `TIER-0002` (candidate framework
design) both merged to `main` (`OPS-0006` §16.1).
**PASS.** Independently reconfirmed via the GitHub API this session (§ Preflight above): `TIER-0001`
merged at `96020e55b5317aa6191733e22d2df84bea4a6574`; `TIER-0002` merged at
`24be14552b0e5caed8052e07497855cde6a37085`. Both confirmed ancestors of the current `origin/main`
tip. **Fully satisfied.**

**Criterion 2 — Classification-question inventory performed against `OPS-0006` §4.5's full scope.**
*Standard:* the nine candidate classification questions are mapped against existing repository
evidence, distinguishing load-bearing fields from decorative or duplicative ones, with an explicit,
evidence-grounded narrowing recommendation (`TIER-0001` §Decision).
**PASS.** `TIER-0001`'s retained artifact (`governance/audits/WS0005_M5_CLASSIFICATION_QUESTION_
INVENTORY_20260804.md`) independently re-confirmed present and unedited at this session's starting
`HEAD`. Key findings independently spot-checked against live state this session: `target_pct`
remains the sole allocator-visible field (confirmed — `allocate.py` reads no other `targets.yaml`
field for gap-sizing); `_FOUR_AXES` in the now-merged `classification_validator.py` matches
`TIER-0001` §6's narrowed four-axis recommendation exactly. **Fully satisfied.**

**Criterion 3 — Candidate framework designed for exactly the four retained axes.**
*Standard:* a field-by-field design for `economic_role`, `capital_priority`, `risk_concentration`,
and `evidence_quality`, with fact-versus-judgment labeling on every field, named evidence sources,
and an explicit non-duplication check against `caps.clusters`/`issuer_lookthrough.yaml`/
`intelligence/relationships/` (`TIER-0002` §Decision, §Rationale).
**PASS.** `TIER-0002`'s retained artifact (`governance/audits/WS0005_M5_CANDIDATE_CLASSIFICATION_
FRAMEWORK_DESIGN_20260805.md`) independently re-confirmed present and unedited. Independently
cross-checked this session against the actually-merged `classification_validator.py`: all four axis
names, the `capital_priority` three-value closed vocabulary
(`maintain_current_weight`/`case_for_review`/`no_assessment`), and `risk_concentration`'s
cross-reference-only design (no new ceiling) all match the design document exactly, at the exact
code that Milestone 6 executed. **Fully satisfied.**

**Criterion 4 — No mechanical or composite score created.**
*Standard:* neither filing computes, proposes, or authorizes a weighted, numeric, or composite
classification score (`TIER-0002` §Alternatives Considered, explicitly rejecting this).
**PASS.** Independently re-confirmed via source inspection: `classification_validator.py` enforces
closed, non-numeric enum values on every axis; no numeric or weighted field exists anywhere in the
schema. **Fully satisfied.**

**Criterion 5 — No ticker classified; no `intelligence/classification/` content created by either
Milestone 5 filing.**
*Standard:* both filings are structural/inventory only — no real ticker is assigned to any category
by `TIER-0001` or `TIER-0002` themselves (`TIER-0002` §Decision, explicit non-authorization list).
**PASS.** Independently reconfirmed this session: `intelligence/classification/` did not exist as a
directory until Milestone 6's own implementation (PR #253, well after both Milestone 5 filings
merged) — confirmed via `git log --diff-filter=A -- intelligence/classification/` showing the
directory's first files were added in a commit that post-dates `TIER-0002`'s merge commit. **Fully
satisfied.**

**Criterion 6 — No adoption or production-policy change from either Milestone 5 filing.**
*Standard:* zero diff on `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `margin_state.py`, `levels.py`, `docs/INVESTMENT_ONTOLOGY.md`,
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, and every pre-existing Intelligence record, across both
filings' own merge diffs.
**PASS.** Independently re-derived this session via `git diff --stat` across each filing's own
base-to-merge-commit range for both PRs — empty output in every case, confirming byte-identical
protected paths, matching each filing's own independent reviewer's identical finding (review
`4859945925`/`4860022747` for `TIER-0001`; review `4860208858` for `TIER-0002`). **Fully
satisfied.**

**Criterion 7 — Framework proven implementation-ready by Milestone 6's actual, unmodified use of
it.**
*Standard:* this is the criterion specific to a design milestone, distinguishing "a plausible
paper design" from "a framework that survived contact with real execution." The framework
Milestone 6 actually classified all 27 canonical equities against must be the same framework
Milestone 5 designed — no axis added, renamed, or dropped mid-execution — and any correction
Milestone 6 required must be attributable to implementation defects (evidence-redaction bugs,
drafting-instruction calibration) rather than to a structural deficiency in the four-axis design
itself.
**PASS**, independently traced through the full Milestone 6 correction history recorded in CLAUDE.md
and cross-checked against the actually-merged `classification_validator.py` and
`intelligence_classification_sanitizer.py`:
  - The **BLOCKING** finding (a bare-noun "gate" leak past the sanitizer) and the later **MAJOR**
    finding (a dangling section-title cross-reference surviving redaction) were both defects in
    `intelligence_classification_sanitizer.py`'s evidence-redaction implementation — a component
    `TIER-0002` never specified in the first place (redaction mechanics are downstream of the
    framework, not part of it). Neither finding touched an axis name, an axis vocabulary, or a
    field definition.
  - The one **MAJOR** finding that did touch axis content — `capital_priority`'s `case_for_review`
    threshold producing a near-uniform 25-of-27 result — was resolved by re-grounding the
    *drafting instruction* directly in `TIER-0002` §3.4's own already-accepted text ("does
    additional-capital-deployment consideration exist... relative to current policy and available
    alternatives?"), not by adding a new value, removing a value, or renaming the axis. The
    corrected 17/9/1 distribution uses the identical three-value vocabulary `TIER-0002` designed.
  - **No correction round, across all three bounded-correction cycles Milestone 6 required, ever
    added a fifth axis, removed one of the four, or changed a field's fact-versus-judgment
    classification.** `classification_validator.py`'s `_FOUR_AXES` constant, independently
    confirmed identical at this session's starting `HEAD` and at every intermediate Milestone 6
    correction commit inspectable via `git log -p -- classification_validator.py` (the axis tuple
    was written once, at the framework's implementation, and never subsequently edited).
  - Milestones 7 and 8 then each independently consumed the same sealed four-axis output — Milestone
    7's `role_comparison`/`capital_priority_comparison` fields map 1:1 from the sealed
    `economic_role`/`capital_priority` values; Milestone 8's `role`/`tier_architecture`/
    `capital_priority` recommendation areas reuse Milestone 7's `primary_disposition` 1:1 — with
    zero framework redesign requested or performed at either downstream milestone.
  **Fully satisfied** — the framework survived three independent milestones' worth of real
  execution with its structural design (four axes, their names, their vocabularies) completely
  unchanged; every correction required was at the implementation or instruction-calibration layer,
  never the framework-design layer this milestone is responsible for.

**Criterion 8 — Full lifecycle completeness for both Milestone 5 filings.**
*Standard:* an eligible independent exact-head review occurred for each filing (`OPS-0007` §1); any
material (Blocking or Major) finding triggered a bounded correction and an exact-head delta review
before the PR was considered ready (`OPS-0009` §6's four-condition delta-review test); explicit
principal acceptance occurred at the exact merged head for each; each merge-commit tree is
byte-identical to its own accepted head's tree; post-merge verification occurred for each and
independently reconfirmed scope, validators, tests, and CI.
**PASS.** Independently re-read in full this session (§ Preflight above): `TIER-0001`'s two-round
chain (review → 2 MAJOR/1 MINOR found → bounded correction → delta review, zero remaining findings)
and `TIER-0002`'s single-round chain (review, zero findings, no correction required) both terminate
in an explicit principal-acceptance comment naming the exact accepted head and an independent
post-merge-verification comment. Zero unresolved BLOCKING or MAJOR finding remains against either
filing at its own final accepted head. **Fully satisfied.**

**Criterion 9 — Validators, tests, and decision catalog remain coherent at the current head.**
*Standard:* all seven WS-0005 validators pass; the full repository test suite passes; the decision
catalog reconciles with zero issues; repository-wide YAML/YML and JSON parsing succeed; `git diff
--check` is clean.
**PASS.** Independently re-run this session against the exact starting `HEAD`
(`31b2674be7024662b696352e80c0079e7d0744ca`), before any edit (§ Preflight above):
`classification_validator.py` OK (28 results); `reconciliation_validator.py` OK (27 tickers);
`recommendation_validator.py` OK (27 tickers); `relationship_validator.py` OK (13 records);
`intelligence_validator.py` clean; `freshness_validator.py` OK; `contender_registry_validator.py`
OK (84 entries); full `pytest` **3091 passed, 0 failed**; decision catalog **89 decisions,
`issues == ()`**; repo-wide YAML/YML/JSON parsing zero errors; `git diff --check` clean. **Fully
satisfied.**

**Criterion 10 — Register and catalog synchronization can now be performed honestly.**
*Standard:* the two disclosed, previously-unresolved gaps — `TIER-0002`'s own missing
`tier0002-post-merge-verification` gate, and the `milestone-5-...` gate's own stale
`status: proposed` — can now both be closed accurately, without asserting anything beyond what
Criteria 1-9 above actually established.
**PASS, as of this filing's own synchronization (§B below).** Both gaps independently reconfirmed
still open at this session's starting `HEAD` (§ Preflight above); this filing is the dedicated,
later, separate completion-determination filing each prior filing named as the required next step.
**Fully satisfied as of this filing's own edits and future merge.**

### B. Historical validation — Milestone 5 output versus Milestone 6's actual use of it

Addressing directly what a design milestone's completion determination must show that a
content-production milestone's does not:

**What Milestone 5 actually delivered.** (1) A nine-question inventory of what the pre-existing flat
`targets.yaml destination:` representation does and does not capture, narrowed by direct evidence
(two 100%-uniform decorative fields, one stale-vocabulary field, two axes already adequately served
by existing mechanisms) to four candidate axes (`TIER-0001`). (2) A field-by-field structural design
for exactly those four axes — `economic_role`, `capital_priority`, `risk_concentration`,
`evidence_quality` — with allowed values, fact-versus-judgment labeling, named evidence sources, a
non-duplication check against `caps.clusters`/`issuer_lookthrough.yaml`/
`intelligence/relationships/`, and one rejected alternative recorded with its reasons (`TIER-0002`).

**Whether Milestone 6's own correction rounds corrected implementation defects only, or exposed a
framework deficiency.** Traced above at Criterion 7: every Milestone 6 correction was either (a) a
sanitizer/redaction-mechanics bug — a component outside the framework's own scope — or (b) a
drafting-instruction recalibration for one axis's threshold, resolved by grounding more precisely in
`TIER-0002`'s *already-accepted* text rather than by changing that text. No correction added,
removed, renamed, or redefined an axis.

**Whether any unresolved finding remains that belongs specifically to Milestone 5.** None found.
Every finding against `TIER-0001` was resolved by its own bounded correction and confirmed at zero
by its own delta review. Every finding against `TIER-0002` — there were none at any point in its
single-round review. Every finding against the framework's *use* (Milestone 6's sanitizer bugs and
threshold recalibration) was disclosed, corrected, and confirmed resolved within Milestone 6's own
completion determination (`TIER-0006`), not carried forward as a Milestone 5 defect, because it was
never a Milestone 5 defect in the first place.

**Whether the framework Milestone 6 used is materially the same framework Milestone 5 authorized.**
Yes, confirmed by direct source inspection: `classification_validator.py`'s `_FOUR_AXES` constant is
identical, in name and in order, to `TIER-0002` §2's four retained axes, and remained unedited across
every one of Milestone 6's three correction commits.

**Whether Milestone 5 can be declared complete retrospectively without rewriting history.** Yes — no
finding, correction, or later milestone's own text is edited, reinterpreted, or reclassified by this
determination. `TIER-0001` and `TIER-0002`'s own decision-file text, `governance/decisions.yaml`
entries, and retained artifacts are all left byte-for-byte unedited by this filing (§D). This filing
adds a completion verdict grounded in evidence that did not yet exist when either filing merged — the
downstream milestones' own successful, unmodified use of the framework — without altering the record
of what happened at the time.

**Conclusion: Milestone 6 did not require a substantive Milestone 5 framework redesign.** Every
correction the milestone required was attributable to implementation mechanics or instruction
calibration, never to the four-axis structural design itself.

### C. Milestone 5 verdict

**MILESTONE 5 COMPLETE.**

All ten criteria above are satisfied as of this filing's own live-state re-verification
(`origin/main` at `31b2674be7024662b696352e80c0079e7d0744ca`). No criterion fails. This filing
accordingly sets the `milestone-5-zero-based-classification-and-tier-architecture-review` gate's
`status` to `complete` in `operations/WORKSTREAMS.yaml` (§F below), **effective only on this
decision's own merge to `main`**, per §H's required independent-review and principal-acceptance
gate.

### D. WS-0005 top-level status — all nine roadmap milestones now complete

With Milestone 5 determined complete (§C), all nine `OPS-0006` §4 milestone gates now read
`status: complete` (see the table in § Preflight, updated per this filing at §F). This is the first
point at which that has been true.

**`OPS-0006` §4 item 9's own controlling text is explicit that adoption sits outside the
nine-milestone sequence**: *"Any adoption requires its own separate accepted governance decision and
a later, separately authorized implementation PR."* Adoption is never numbered as a tenth milestone
anywhere in `OPS-0006`'s own text, and `TIER-0011` §K.4 (independently re-read this session)
restates the same boundary for Milestone 9 specifically: *"Even a future Milestone 9 completion
determination does not itself authorize adoption."* `WS-0005`'s own `governing_authority` field
names `OPS-0006` as the authority for "the complete zero-based/blinded-review protocol and
nine-milestone roadmap" — the roadmap itself, not a broader or open-ended mandate, is what
`OPS-0006` actually authorized this workstream to execute.

**`TIER-0012` disclosed, but explicitly did not resolve, a second consideration**: that WS-0005's own
register `objective` text ("...design the simplest defensible portfolio-role, capital-priority,
tier, target, and review framework") reads more broadly than the nine-milestone roadmap's own
numbered scope, and that "closing Milestone 9 closes the sequence, not WS-0005's broader ...
objective." This filing independently evaluated that consideration and finds it does not, on
inspection of the actually-controlling text, constitute a binding requirement to keep WS-0005 open
now that all nine gates are complete:

1. No accepted governance decision anywhere in `governance/decisions.yaml` states that WS-0005's
   top-level `status` must remain `in_progress` until adoption occurs, or until any milestone beyond
   the nine `OPS-0006` §4 names. A full-repository grep for this specific claim, run independently
   this session, returns zero matches.
2. `OPS-0006` §4 item 9's own text draws the adoption boundary in the same breath it defines
   Milestone 9 — deliberately, not by omission — precisely to keep the research/design/review
   roadmap (which this workstream's `governing_authority` names as its scope) separate from the
   distinct, later, separately-gated act of changing live portfolio policy on the strength of that
   roadmap's output. Reading WS-0005's own prose `objective` as silently expanding that deliberately
   drawn boundary would make the boundary meaningless — `OPS-0006` §4 item 9 would have said so
   directly if adoption were meant to be WS-0005's own tenth, unstated milestone.
3. `TIER-0012` itself did not, and could not, resolve this question with the evidence available to
   it, because Milestone 5 was still open at that time — it had two independently sufficient reasons
   to keep WS-0005 open, one of which (the Milestone 5 gap) is now resolved by this filing, and the
   other of which (this adoption-scope question) it explicitly flagged rather than settled. This
   filing is the first to reach the point where that second consideration must actually be decided,
   not merely disclosed.

Accordingly, this filing determines that **WS-0005's top-level `status` transitions from
`in_progress` to `complete`**, meaning precisely and only: the nine-milestone research, design, and
review roadmap `OPS-0006` §4 defined is fully executed, reviewed, and register-synchronized. This
transition creates no adoption authority, no policy change, and no new workstream — it records that
this workstream's own bounded charter has been fulfilled.

**`WS-0005`'s `priority` transitions from `primary` to `secondary` in this same filing** (bounded
correction, following an independent exact-head review of this PR). The original text left
`priority: primary` unedited, citing `OPS-0003` as precedent for treating any reassignment as "its
own governance act... not a byproduct of a routine completion filing" — the review found this
mischaracterizes `OPS-0003` item 1, the directly on-point precedent, which performed exactly this
reassignment inside the same filing that recorded WS-0002's own scope completion, for the identical
stated reason: *"its authorized planning work is done; nothing further is pending on it that would
justify holding `priority: primary`."* That reasoning transfers here without modification — WS-0005's
authorized nine-milestone roadmap is done; nothing further is pending on it that would justify
holding `priority: primary`. Accordingly, `WS-0005`'s `priority` field is set to `secondary`, matching
`OPS-0003` item 1 exactly. No schema, validator, or test in this repository ties `priority` to
`status` (confirmed by direct inspection of `render.py`'s `n_ws_primary` computation, a plain count
independent of `status`), and `OPS-0001`'s register rules permit zero `priority: primary`
workstreams — this filing accordingly names no successor primary workstream; identifying one is its
own separate judgment, left to a future, separate decision (matching `OPS-0003` item 2's own treatment
of WS-0001's priority as a distinct action from item 1's WS-0002 downgrade, not a single combined
act).

### E. Whole-portfolio, valuation, and adoption boundaries — preserved unchanged

**Closing Milestone 5 and WS-0005 does NOT mean**: the final portfolio is complete; final holdings
are known; final target weights are known; valuation is complete; an ETF framework is complete; a
crypto framework is complete; GLD/cash/debt doctrine is complete; cross-asset synthesis is complete;
chart deployment is complete; or adoption is complete. WS-0005 closure is **equity-workstream
roadmap closure only** — the same equity-scoped, 27-canonical-name boundary `XASSET-0001` §H and
every one of `TIER-0007`/`TIER-0008`/`TIER-0009`/`TIER-0010`/`TIER-0011`/`TIER-0012` already
restated, unweakened here.

**Valuation boundary, unchanged**: `target_and_range` and `maximum_position_size` remain
`primary_status: valuation_required` for all 27 sealed equities in the Milestone 8 recommendation
package — no numeric target, range, or maximum-position-size value is authorized, proposed, or
implied by this filing. No governed valuation methodology exists anywhere in this repository, and
none is created here.

**Adoption boundary, unchanged**: review and completion are not adoption. `TIER-0011` §K's controlling
text — that Milestone 9's review, however favorable, does not authorize adoption, and that every
adoption action requires its own separate, future, explicit governance decision and implementation
PR — remains fully in force. This filing's own determination that all nine milestones (including
Milestone 9) and WS-0005 itself are complete does not itself adopt, endorse, apply, or act on any
individual finding from Milestones 6, 7, or 8. No `portfolio_role_ref`, `conviction.rating`,
`target_pct`, gate, cap, cluster, `holdings.yaml`, allocator, margin, or ladder value is authorized,
proposed, or changed by this filing.

### F. Register synchronization performed by this filing

This filing performs the minimum `operations/WORKSTREAMS.yaml` synchronization Criterion 10 and §D
require:

1. `milestone-5-zero-based-classification-and-tier-architecture-review` gate: `status: proposed` →
   `status: complete`, appended additively to the gate's existing description text (per this
   repository's never-silently-rewrite convention for retained state), recording `TIER-0001`'s and
   `TIER-0002`'s accepted heads, merge SHAs, review chains, principal acceptances, and post-merge
   verifications, and this filing's own Criterion 7/§B historical-validation finding that Milestone
   6 required no framework redesign.
2. A new, additive `tier0002-post-merge-verification` gate entry (Lane M, `OPS-0009` §1),
   synchronizing `TIER-0002`'s already-confirmed merge/review/acceptance/post-merge-verification
   state — the gap `TIER-0002`'s own post-merge comment explicitly deferred to "a future WS-0005
   session's own preflight." The pre-existing `tier0002-candidate-framework-design` gate entry is
   left byte-unedited.
3. `WS-0005`'s top-level `status`: `in_progress` → `complete`, and `priority`: `primary` →
   `secondary`, with an appended note recording this filing's own §D reasoning and explicitly
   restating the whole-portfolio/valuation/adoption boundaries from §E.
4. `WS-0005`'s own `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
   self-reference fields updated to this filing's own branch, `active_pr: null` until this filing's
   own PR number exists (per `OPS-0001`'s established convention — a bounded follow-up commit sets
   it once the PR is opened), `last_verified_main_sha:
   31b2674be7024662b696352e80c0079e7d0744ca`, `last_verified_date: "2026-08-07"`.
5. **A new, additive `tier0013-ws0005-roadmap-completion` gate entry**, self-tracking this filing's
   own progress. Following `tier0002-candidate-framework-design`'s, `tier0007-milestone7-baseline-
   reconciliation-authorization`'s, `tier0009-milestone8-policy-recommendation-framework-
   authorization`'s, and `tier0011-milestone9-independent-review-and-adoption-authorization`'s own
   established convention exactly, this gate is left at `status: in_progress`, `pr: null` — not
   marked `complete` — since this filing's own governance PR is itself still draft, unreviewed, and
   unmerged. This gate's eventual `status: complete` transition, if warranted, belongs to a later,
   separate `tier0013-post-merge-verification` filing once independent review, correction if needed,
   principal acceptance, merge, and post-merge verification have actually occurred — exactly the
   pattern this filing itself applies to the `tier0002-post-merge-verification` gate at item 2 above.
   (**Bounded correction, independent review**: this gate was originally, mistakenly, filed at
   `status: complete` while PR #267 remained draft — the identical defect class `TIER-0001`'s own
   independent review classified MAJOR for `TIER-0001`'s own self-referencing gate. Corrected to
   `status: in_progress` per the convention stated above.)

No other `WS-0005` field (`objective`, `governing_authority`, `dependencies`, `authorized_scope`,
`prohibited_scope`) or any other milestone's own gate (Milestones 1-4 and 6-9, all left byte-for-byte
unedited and not reopened) is touched. `TIER-0001`'s and `TIER-0002`'s own decision-file text and
`governance/decisions.yaml` frontmatter (both still reading `status: Proposed`, per this
repository's established two-step acceptance-recording pattern) are left unedited by this filing —
not corrected here, matching every prior filing's identical treatment of this known, pre-existing,
out-of-scope state.

### G. What this decision does not do

- **Does not redesign `TIER-0002`'s framework** — no axis added, removed, renamed, or redefined; no
  new field; no numeric or weighted score.
- **Does not create any new classification content** — `intelligence/classification/`, all 27 sealed
  records, and `COHORT_MANIFEST.yaml` remain byte-for-byte unedited, independently confirmed zero
  diff.
- **Does not correct `intelligence/companies/LLY.yaml`** — the `PI-0039`-identified,
  `TIER-0011`/PR #265-carried-forward MINOR finding remains exactly as found, byte-for-byte
  unedited.
- **Does not perform any new research** of any kind.
- **Does not change any tier, target, holdings, gate, cap, cluster, allocator, margin, or ladder
  value** — `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`,
  `levels.py`, and `margin_state.py` are untouched.
- **Does not perform any ETF or crypto work, valuation architecture, or cross-asset synthesis** —
  `WS-0014`/`XASSET-0001` remain exactly as their own governing decisions left them.
- **Does not perform any chart interpretation** or touch any `CHART-0001`/`CHART-0002` file.
- **Does not run or log an allocation check** — no order, trade, or live/scenario `allocate.py`/
  `levels.py` output is produced or executed by this filing.
- **Does not adopt, endorse, or act on any Milestone 6/7/8 finding** — see §E.
- **Does not name a new primary workstream** — see §D.
- **Does not reopen `TIER-0001` or `TIER-0002`'s own accepted text, decision-file frontmatter, or
  retained artifacts.**
- **Does not mark this filing's own governance PR ready, request or begin independent review of it,
  post principal acceptance of it, or merge it** — this decision's own effectiveness is contingent
  on its own future, separate independent review and principal acceptance, exactly as every prior
  WS-0005 governance filing in this log has required of itself.
- **Creates no research, policy, allocation, or implementation authority of any kind beyond the two
  factual determinations stated in §C and §D.**

### H. Effectiveness, review, and merge gates

- **This governance PR must remain in draft state** and must not be marked ready for review or
  merged by this session.
- **An eligible independent review is required**, anchored to this PR's exact final head, per
  `OPS-0007` §1's twelve-point capability-based standard — no self-review by the authoring session.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready, per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Explicit principal acceptance is required before merge**, at the exact head being merged.
- **This decision does not mark itself, or authorize marking itself, ready for merge.** It becomes
  effective — including the Milestone 5 `status: complete` transition (§F.1) and the WS-0005
  top-level `status: complete` transition (§F.3) — only on this governance PR's own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized
  scope ends at opening this draft PR (and one bounded follow-up commit setting `WS-0005`'s
  `active_pr` self-reference to this PR's own number once it exists) and reporting its exact head.
  No independent review, no correction pass, no re-review, no merge, and no post-merge verification
  is performed by this session — each is a separate future step requiring a separate actor. This
  session does not review its own work, mark it ready, merge it, or post principal acceptance.

### I. Bounded correction (same PR, independent review)

An independent exact-head review of this PR's original head (`8deda40ddd3fb8ff413a9aa2ed59636d07204cf4`)
returned CHANGES REQUIRED — 0 BLOCKING / 2 MAJOR / 1 MINOR / 1 NOTE. All ten Milestone 5 completion
criteria (§A), the Criterion-7 framework-identity finding (§B), and the WS-0005 top-level closure
reasoning against `TIER-0011` §K.4 and `OPS-0006` §4 item 9/§7 item 5 were all independently
re-derived and confirmed sound by that review — none of the findings below touch the substantive
Milestone 5 or WS-0005-closure verdicts.

**MAJOR 1, resolved**: the new `tier0013-ws0005-roadmap-completion` self-tracking gate was originally
filed at `status: complete`/`pr: null` while this PR remained draft, unreviewed, and unmerged —
contradicting this repository's own established convention for a filing's self-tracking gate
(`tier0002-candidate-framework-design`, `tier0007-milestone7-baseline-reconciliation-authorization`,
`tier0009-milestone8-policy-recommendation-framework-authorization`, `tier0011-milestone9-
independent-review-and-adoption-authorization` — all stay `status: in_progress` until a later,
separate post-merge-verification filing closes them) and reproducing the identical defect class
`TIER-0001`'s own independent review classified MAJOR. Corrected to `status: in_progress`, `pr: null`
(§F.5); the gate's real completion recording is deferred to a future `tier0013-post-merge-
verification` filing.

**MAJOR 2, resolved**: the original text left `WS-0005`'s `priority: primary` unedited, citing
`OPS-0003` as precedent for treating any reassignment as its own separate, later governance act. The
review found this mischaracterizes `OPS-0003` item 1, the directly on-point precedent, which
performed exactly this reassignment inside the same filing that recorded WS-0002's own scope
completion, for the identical "authorized work is done" reasoning. Corrected: `WS-0005`'s `priority`
now transitions `primary` → `secondary` in this same filing (§D, §F.3), matching `OPS-0003` item 1
exactly, without naming a successor primary workstream (a materially different, still-rejected
alternative — Alternatives Considered).

**MINOR, resolved**: `OPS-0006` §4.5's gate text was presented as "quoted in full" but was in fact a
compressed paraphrase omitting the seven-concept candidate-separation clause. Corrected to the actual
full controlling text, with `TIER-0001`'s own inventory cited as corroborating that the omitted
concepts (business quality, position boundaries, review cadence) were genuinely canvassed, not
silently dropped (§A).

**NOTE, no correction required**: the reviewing session's own local `pytest` run showed one failure
(`test_real_repository_model_builds`), independently diagnosed by that review as a pre-existing,
clone-path-sensitive assertion tied to the reviewing worktree's own directory name — not a defect in
this PR's content, and the same artifact class `TIER-0002`'s own review chain already disclosed. This
session's own local runs (worktree named `Portfolio-HQ`) show the full **3091 passed, 0 failed** at
both the original and this corrected head.

No Milestone 5 completion criterion, no Criterion 7 finding, no WS-0005-closure reasoning, no
whole-portfolio/valuation/adoption boundary, and no protected-path scope changed as a result of this
correction. Requires its own fresh independent exact-head delta review before this PR may be
considered ready.

## Rationale

**Why a completion-determination decision is warranted now.** `TIER-0012` explicitly disclosed, as a
live, previously-undisclosed gap found by direct YAML inspection, that the Milestone 5 gate's own
`status` had never been flipped to `complete` by a dedicated completion-determination filing, unlike
every other milestone — and named this as one of two reasons WS-0005 itself could not yet close.
This filing performs exactly that required, disclosed-but-unauthorized-for-`TIER-0012`-itself step.

**Why this filing both derives and evaluates the completion criteria in one unit, rather than filing
a separate standard first.** `TIER-0006`, `TIER-0008`, and `TIER-0010` set the precedent, across the
same milestone family, of combining standard-definition and determination in one filing when the
controlling specification is already fully accepted and no new specification content remains to be
written. Here, `OPS-0006` §4.5's own gate text, together with `TIER-0001`'s and `TIER-0002`'s own
already-accepted content, fully specifies what Milestone 5 required; the only work remaining was to
organize those controls into named criteria — including one criterion (§A.7) unique to a design
milestone, evaluating the framework's proven use rather than merely its existence — and evaluate
them against live state.

**Why Criterion 7 and §B (historical validation) are the load-bearing sections of this filing.** A
design milestone's completion cannot be judged on the same terms as a content-production milestone —
"the framework exists and was reviewed" is necessary but not sufficient, because a plausible-looking
design can still fail on contact with real classification work. This filing's distinguishing
contribution is tracing, through the full Milestone 6 correction history, that every defect Milestone
6 actually surfaced was at the implementation (sanitizer) or instruction-calibration (threshold
wording) layer, never at the four-axis structural-design layer — the evidence that was not yet
available when `TIER-0002` merged and that only a filing written after Milestones 6-8 completed
could actually verify.

**Why the WS-0005 top-level closure determination (§D) is decided now rather than deferred again.**
`TIER-0012` explicitly flagged this as an open question rather than a settled one, and the task
authorizing this filing explicitly instructed evaluating it once all nine milestones are complete —
this is now the first filing positioned to actually decide it, since Milestone 5 (the last open gate)
is resolved within this same filing. Deferring the question a second time, with no new fact
expected to change the analysis, would not serve `OPS-0006` §16.4's standing rule against inferring
completion claims beyond what was actually authorized and delivered — nor would it serve the
opposite failure mode of leaving a fully-executed roadmap's workstream register entry permanently
`in_progress` for a reason ("adoption") that `OPS-0006` §4 item 9's own text already, deliberately,
separates from the roadmap.

## Alternatives Considered

- **Declare Milestone 5 complete based on `TIER-0001`'s or `TIER-0002`'s own governance text alone,
  without independently re-reading the review/acceptance/merge history for both.** Rejected — exactly
  the "assume PR-level language proves lifecycle compliance" failure mode `TIER-0006`, `REL-0006`,
  `PI-0037`, `TIER-0008`, `TIER-0010`, and `TIER-0012` already rejected for prior milestones.
- **File a separate "Milestone 5 completion standard" document first, then a second, later
  determination filing evaluating it** — mirroring `REL-0004`→`REL-0006`'s two-filing split.
  Rejected — see Rationale; `TIER-0006`'s, `TIER-0008`'s, and `TIER-0010`'s own combined-filing
  precedent for this same milestone family is adopted instead, since no new specification content
  remained to write.
- **Treat Milestone 6's correction rounds as evidence Milestone 5 was incomplete, and decline to
  close Milestone 5 without a redesign.** Rejected on direct evidence — see Criterion 7 and §B: every
  correction was implementation- or instruction-layer, never framework-design-layer; the axis names,
  order, and vocabularies are unedited across all three Milestone 6 correction commits.
- **Determine WS-0005's top-level status complete without addressing `TIER-0012`'s disclosed
  "broader objective" consideration.** Rejected — silently ignoring a disclosed open question would
  repeat the exact failure mode this repository's own conventions exist to prevent; §D addresses it
  directly rather than assuming it away.
- **Keep WS-0005 `in_progress` indefinitely, treating adoption as an implicit tenth milestone.**
  Rejected — no accepted governance decision states this, `OPS-0006` §4 item 9's own text draws the
  adoption boundary deliberately, and the controlling authorization for this filing explicitly
  instructs against keeping WS-0005 open "solely because adoption is unauthorized unless live
  governance explicitly requires that."
- **Name a different workstream (e.g. `WS-0014`) as the new `priority: primary` in this same
  filing.** Rejected — distinct from downgrading `WS-0005`'s own priority (performed, see §D and the
  correction below): identifying which workstream should next hold `priority: primary` is its own
  separate judgment this filing is not positioned to make, and `OPS-0001`'s register rules permit
  zero `priority: primary` workstreams in the meantime.
- **Leave `WS-0005`'s `priority: primary` unedited, treating a primary-workstream reassignment as
  always requiring its own separate, later, dedicated decision.** This was this filing's original
  position, citing `OPS-0003` as precedent — rejected on correction (independent review) once direct
  inspection of `OPS-0003` item 1's own text showed it is not a separate-decision precedent but a
  same-filing one: `OPS-0003` downgraded WS-0002's priority in the very filing that recorded its
  scope completion, for the same "authorized work is done" reasoning that applies to `WS-0005` here.
  Corrected to perform the downgrade (`priority: primary` → `secondary`) in this same filing, per §D,
  without naming a successor (a materially different, still-rejected alternative — see above).
- **Begin any Milestone-10-equivalent, adoption, or `WS-0014`/`XASSET-0001` content in the same
  filing, since all nine milestones are now complete.** Rejected — explicitly outside this unit's
  authorization; nothing in `OPS-0006`, `TIER-0011`, or `XASSET-0001` treats roadmap completion as
  self-authorizing any next step.

## Consequences

**Authorized, effective only on this decision's merge:** the factual determination that WS-0005
Milestone 5 satisfies all ten completion criteria derived above, the corresponding
`status: complete` update to the `milestone-5-zero-based-classification-and-tier-architecture-review`
gate, the new `tier0002-post-merge-verification` gate entry, the new self-tracking
`tier0013-ws0005-roadmap-completion` gate (left `status: in_progress` per §F.5), the factual
determination that all nine `OPS-0006` §4 milestone gates are now complete, the corresponding
`status: complete` update to `WS-0005`'s own top-level entry, the `priority: primary` → `secondary`
transition (§D), and the minimum `WS-0005` self-reference synchronization in §F.

**Unchanged by this decision:** `TIER-0001`'s and `TIER-0002`'s own decision-file text and
`governance/decisions.yaml` frontmatter, byte-for-byte; both filings' retained artifacts, byte-for-
byte; `classification_validator.py`, `intelligence_classification_sanitizer.py`, and all 27
`intelligence/classification/*.yaml` records plus `COHORT_MANIFEST.yaml`, byte-for-byte;
`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml` and
`intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`, byte-for-byte; every
existing Company/Theme/relationship Intelligence record, all of them, including
`intelligence/companies/LLY.yaml`; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s own
`objective`, `governing_authority`, `dependencies`, `authorized_scope`, and `prohibited_scope`
fields (`priority` is changed by this decision — `primary` → `secondary`, per §D and the bounded
correction above, with no successor primary workstream named); Milestones 1-4 and 6-9's own
`status: complete` gates (unedited, not reopened);
`TIER-0001` through `TIER-0012`'s own accepted text and scope, in full, unedited.

**Explicitly not authorized by this decision, stated repeatedly for clarity:** any framework
redesign; any new classification, relationship, reconciliation, or recommendation content; any
correction to `intelligence/companies/LLY.yaml` or any other existing record; any numeric valuation
methodology; any whole-portfolio target; any cross-asset synthesis; any ETF or crypto policy; any
new primary-workstream designation; any adoption action of any kind; any external research; any
gate reopening; any tier/target/role/cluster/cap/holdings/margin/allocator/ladder/chart/order-
behavior change; any allocation check. **This decision creates no research, policy, allocation, or
implementation authority beyond the two factual determinations in §C and §D.**

This decision becomes effective only when its implementing pull request merges to `main`.

**No current portfolio policy or allocator behavior changes as a result of this decision, before or
after its merge.** `allocate.py`'s buy/trim/gap logic, every gate parameter, every cap, every target
weight, and every margin parameter remain exactly as `targets.yaml`/`gates.yaml`/`holdings.yaml`
currently state them, unaffected by this filing under any circumstance.
