# WS-0005 Milestone 5 — Candidate Classification Framework Design (TIER-0002 Bounded Unit)

**Implementation output of this session — not an independent review.**

| Field | Value |
|---|---|
| Authority | `governance/decisions/TIER-0002-ws0005-milestone5-candidate-classification-framework-design.md`; `operations/WORKSTREAMS.yaml` WS-0005, `milestone-5-zero-based-classification-and-tier-architecture-review` gate |
| Scope | Structural design of a candidate classification framework, using only the four axes `TIER-0001` recommended for further consideration (economic role, capital priority, risk concentration, uncertainty/evidence quality). No ticker is classified. No file of the proposed new type is created. No existing file (`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, any Company/Theme/relationship record, `docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `allocate.py`, `margin_state.py`, `levels.py`) is modified. |
| Repository state audited | `origin/main` @ `96020e55b5317aa6191733e22d2df84bea4a6574` (PR #245 merge commit — `TIER-0001` effective), verified clean, working tree clean, zero open PRs |
| Mode | Design only. Every field, vocabulary, and structural choice below is a proposal for future, separately authorized use — nothing here is created, applied, or made operative by this artifact. |

---

## 0. Preflight summary

- `origin` fetched; local `main` confirmed identical to `origin/main` at `96020e55b5317aa6191733e22d2df84bea4a6574`; working tree clean.
- Zero open pull requests (`mcp__github__list_pull_requests`, `state: open` → `[]`). No active mutation lane.
- `TIER-0002` confirmed unused: zero matches in `governance/decisions.yaml`, zero matches via full-repository grep, `TIER-0001` is the only existing `TIER-####` entry.
- PR #245 (`TIER-0001`) independently confirmed via the GitHub API: `merged: true`, merge commit `96020e55b5317aa6191733e22d2df84bea4a6574` (matching `origin/main`'s current tip exactly), independent exact-head review `4859945925` (CHANGES REQUIRED — 2 MAJOR, 1 MINOR, 1 NOTE), a correction commit (`eed05c07`), an independent delta review `4860022747` ("DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"), a retained principal-acceptance comment (`issuecomment-5186141437`, quoting explicit acceptance at exact head `eed05c07c2604a18466f345a1bb9c8877705f5a2`), and a retained post-merge-verification comment (`issuecomment-5186176928`) already confirming decision-catalog/YAML/validator/test/protected-path/primary-workstream state clean at the merge commit. `TIER-0001`'s own decision-file and `governance/decisions.yaml` frontmatter still read `status: Proposed` — a known, pre-existing, out-of-scope state matching the `CHART-0001`/`CHART-0002`/`REL-0002`-`REL-0005` two-step acceptance-recording pattern already documented in CLAUDE.md's Decisions Log; not corrected here.
- The `tier0001-classification-question-inventory-bounded-unit` gate in `operations/WORKSTREAMS.yaml` (as merged) reads `status: in_progress`, `pr: null` — accurate as of the PR's own text (matching the `rel0002`-`rel0005` precedent of never self-declaring completion on a still-open PR), but stale now that the PR has since merged, been reviewed, and been accepted. Per the PR's own post-merge-verification comment, this synchronization is deferred to "a future WS-0005 session's own preflight/governance filing" — this filing performs that synchronization (§7 below), per `OPS-0008` §4(a)'s read-only-by-default fold-in convention, matching the `REL-0002`→`REL-0003`, `REL-0003`→`REL-0004`, `REL-0004`→`REL-0005`, `REL-0005`→`REL-0006` chain's own established pattern.
- `governance/decisions/` carries 72 decision files (excluding `README.md`); `governance/decisions.yaml` carries 72 rows — confirmed 1:1 by direct count this session. `test_portfolio_hq_dashboard_decisions.py` currently asserts `== 72` in two places, both requiring an update to `73` as part of this filing's own implementation.
- WS-0005's own register entry confirms Milestones 1-4 `status: complete`; Milestone 5 (`milestone-5-zero-based-classification-and-tier-architecture-review` gate) remains `status: proposed`; Milestones 6-9 remain `status: proposed`.

No condition met a stop bar. This unit proceeded.

---

## 1. Authorizing scope (restated, not expanded)

The principal authorized exactly one bounded Milestone 5 candidate-framework design unit, using only the four axes `TIER-0001` retained (economic role, capital priority, risk concentration, uncertainty/evidence quality), producing the smallest structure that materially improves portfolio decisions. Explicitly excluded: classifying any ticker; applied examples assigning a real holding to a category; any change to `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, caps, clusters, allocator logic, `levels.py`, `margin_state.py`, `allocate.py`, charts, ladder files, or trades; new external research; a mechanical score or weighted ranking; an adoption decision; Milestones 6-9.

This artifact is the retained design record; `governance/decisions/TIER-0002-*.md` is the governing decision that authorizes and frames it.

---

## 2. Design standard applied

Per the authorizing instruction, every proposed field is tested against exactly one question: **does separating this concept change a capital-prioritization decision, a risk interpretation, a monitoring decision, or a review-cadence decision?** A field that does not is rejected. No field may answer the same question a different field, or an existing repository mechanism, already answers.

---

## 3. Recommended framework: a new, optional, non-coupled classification namespace

### 3.1 Structural choice

A new, separate, optional record type — `intelligence/classification/<TICKER>.yaml`, one file per ticker, single-file (not YAML+Markdown pair) — is the recommended structure. **Not created by this filing.** No ticker has, or is authorized to have, a file of this type as a result of this design.

Reasoning for each structural choice:

- **New namespace, not an extension of `intelligence/companies/<TICKER>.yaml`.** Extending the frozen Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9) requires its own separate governance decision under §19/§20's own change process, and would create pressure to backfill all 47 existing records for a still-unadopted Milestone 5 experiment. A separate namespace can be discarded in full (`rm -rf intelligence/classification/`) without touching a single one of the 47 already-governed, already-`OPS-0007`-§3-PROVISIONAL Company Intelligence records, preserving `OPS-0006` §2's zero-based reversibility guarantee at maximum strength.
- **Filesystem is the index.** No `intelligence/classification/index.yaml` — the same doctrine already tested and re-affirmed by `PI-0001`, `PI-0006`, and `REL-0001` §B, applied here without re-litigation.
- **One file per ticker, YAML only, no Markdown pair.** Company Intelligence pairs YAML with Markdown because the thesis narrative needs freeform prose (§10 of the frozen spec). This framework's only prose fields — `capital_priority.rationale` and `evidence_quality.thesis_uncertainty_statement` — are each deliberately bounded to a few sentences, not a business-summary-length narrative, so a second file would add structure without adding capability. If a future Milestone 6/7 unit finds the prose fields outgrowing that bound, splitting to a YAML+MD pair is a small, later, separately authorized change — not pre-built here on spec.
- **Coverage is opt-in**, mirroring §16 of the frozen Company Intelligence spec exactly: absence of a classification file for any ticker, gated or not, is normal and not an error.

### 3.2 Rejected alternative: extend the Company YAML schema (§9) directly

Considered and rejected. A fifth top-level block (`classification:`) inside `intelligence/companies/<TICKER>.yaml` was the most obvious alternative. Rejected because:

1. It requires reopening `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s frozen §9 schema — its own separate governance decision (§19/§20), not something this filing is authorized to do or should smuggle in via a design proposal.
2. A schema addition typically implies uniform application; the pressure to backfill all 47 existing records the moment the field exists is real and would front-run Milestones 6-9's own adoption question.
3. `risk_concentration`'s cross-reference fields (§3.5 below) are inherently **portfolio-level** facts about a company (which cluster, which relationship records), not **company-level** facts — the same reasoning `REL-0001` used to justify a new `intelligence/relationships/` namespace rather than folding pairwise data into the single-company schema applies here with equal force.
4. It is the larger, less reversible change for no incremental capability — violating the "smallest structure that materially improves decisions" instruction directly.

No other alternative was found materially useful enough to record; per the authorizing instruction, only one rejected alternative is presented.

### 3.3 Axis 1 — Economic Role (`economic_role`)

| Sub-field | Type | Allowed values | Fact or judgment |
|---|---|---|---|
| `economic_system_ref` | string | One of `docs/INVESTMENT_ONTOLOGY.md` §D's five named systems (AI & Compute Infrastructure / Energy & Electrification / Healthcare & Life Sciences / Financial Infrastructure / Digital Platforms & Enterprise Software), or `other: <label>` for a system not yet named there | Factual (a categorization of disclosed business activity) |
| `company_role` | short string | Free text, reusing `docs/INVESTMENT_ONTOLOGY.md` §A/§E's illustrative role vocabulary where it fits (e.g. "power," "equipment," "compute," "networking," "cloud platform") | Factual |
| `role_basis` | one sentence + citation | Free text, must cite a primary disclosure (10-K/10-Q/IR material segment description) or an existing Company Intelligence record's `sector`/`industry`/thesis content | Factual, source-cited |

**What this answers:** "what function does this holding serve, and in which broader economic system?" — distinct from *how much I believe in it* (conviction) and distinct from *what tier vocabulary was in force when its Company Intelligence record was authored* (`portfolio_role_ref`).

**Why retained despite TIER-0001 finding it has no direct mechanical effect on any existing decision.** `TIER-0001` §4.1 found this axis "matters for human capital-priority reasoning, not for any existing mechanical decision." That is the justification for retaining it here, not against it: `capital_priority`'s `comparator_set` (§3.4) cannot be chosen defensibly without knowing which economic system and role a ticker occupies — every existing PI-0016-style committee review already performs this reasoning informally, in prose, before naming its 2-5 comparators (e.g. `PI-0019`'s GEV review named ETN/VRT/PWR specifically because they are the other `power_infra` members). This axis is a structured place to record that reasoning once, reusably, rather than re-deriving it from scratch in every future review's prose. It therefore materially changes the capital-prioritization decision indirectly, by making the comparator selection auditable and consistent — the test the authorizing instruction requires.

**Reconciliation with `ONTO-0001` and `portfolio_role_ref` (TIER-0001 open question #1).** This field is explicitly **not** a replacement for `portfolio_role_ref`, does not migrate it, and does not resolve TIER-0001's open question about whether `portfolio_role_ref`'s stale tier vocabulary should ever be updated — that stays open, for a future Milestone 7 reconciliation step. `company_role`/`economic_system_ref` are proposed as the **first candidate structured location where `ONTO-0001` §A/§E's already-frozen, currently-unapplied vocabulary could actually be used** — `ONTO-0001` itself already states its terms have "zero allocator, tier, target, or portfolio-policy consequence" and require "its own separate proposal and governance decision" before any use; this design proposes exactly that future use, without performing it.

### 3.4 Axis 2 — Capital Priority (`capital_priority`)

| Sub-field | Type | Allowed values | Fact or judgment |
|---|---|---|---|
| `status` | closed enum | `maintain_current_weight` \| `case_for_review` \| `no_assessment` (default) | Judgment |
| `comparator_set` | list of 2-5 tickers | Bounded, matching `PI-0016`'s already-governed comparator convention | Judgment (selection), factual (membership, once selected) |
| `rationale` | short narrative, required when `status != no_assessment` | Free text; must not contain a numeric target, a suggested `target_pct`, or a buy/sell/trim instruction | Judgment |
| `assessed_date` / `assessing_record` | date / pointer | ISO date; pointer to the governing committee-review decision (e.g. `PI-0017`/`PI-0018`), if one exists | Factual |

**What this answers:** "does additional-capital-deployment consideration exist for this holding relative to current policy and available alternatives?" — the descriptive term `docs/INVESTMENT_ONTOLOGY.md` §E already defines precisely ("not a standing ranking, score, target-allocation instruction, or buy recommendation").

**How this stays distinct from `target_pct` (never a number, never allocator-visible).** `capital_priority.status` is a three-value closed enum, never a number, never read by `allocate.py`, and never automatically changes `target_pct`. Any resulting weight change remains a fully separate, manual `targets.yaml` edit under its own governance path — exactly `TGT-0001`/`TGT-0002`'s existing precedent (COST's T2→T1 promotion was "the principal's own independent determination," never a formula), and exactly the loosest-coupled, lowest-risk integration tier `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §19 point 2 already names ("a conviction rating could *suggest* a tier-weight review is warranted, but any actual change is still a human hand-editing `targets.yaml`").

**Why this does not create the conviction-to-target_pct rule TIER-0001 flagged as open (question #2).** No formula exists anywhere in this design connecting `conviction.rating` (Company Intelligence, already governed by `PI-0004`) to `capital_priority.status`, or `capital_priority.status` to any target weight. The two remain related only through human narrative cross-reference. Whether a future, separately pre-registered, evidence-gated rule should ever connect conviction to weight is explicitly left open, matching the discipline `GOV-0003` already applies to margin-timing research: research into a conditional rule is one thing, adopting one is a separate, later, evidence-gated decision this filing does not make or shortcut.

**Why this is not decorative.** Unlike `monitoring_enabled`/`risks[].status` (100% uniform, TIER-0001 found decorative), this axis reuses a conclusion committee reviews **already reach in prose today** (`PI-0018`, `PI-0020`, `PI-0022` each concluded "Keep current policy," an advisory statement functionally identical to `status: maintain_current_weight`) — this design merely gives that already-occurring judgment a structured, queryable location. It adds zero new analysis requirement.

### 3.5 Axis 3 — Risk Concentration & Overlap Exposure (`risk_concentration`)

| Sub-field | Type | Allowed values | Fact or judgment |
|---|---|---|---|
| `cluster_cap_membership` | computed list | Zero or more of `semis` \| `power_infra` \| `oil` (`targets.yaml` `caps.clusters` keys) | Factual, computed |
| `issuer_lookthrough_membership` | computed boolean | `true` \| `false` | Factual, computed |
| `relationship_record_coverage` | computed list | Zero or more `intelligence/relationships/<A>_<B>` filenames including this ticker | Factual, computed |
| `unmeasured_flag` | computed boolean | `true` exactly when all three above are empty/`false` | Factual, computed |
| `notes` | optional free text | Free text | Judgment |

**What this answers:** "what portfolio-level concentration or dependency risk mechanism, if any, already covers this holding — and is it currently measured by nothing at all?"

**How this stays distinct from `caps.clusters`/`issuer_lookthrough.yaml` (no new ceiling, no new number).** This axis creates **no new percentage, no new cluster, and no new gate** — `allocate.py` never reads it, and no field here duplicates a cap's own threshold value. It is purely a **cross-reference rollup**: the first four sub-fields are mechanically computed from three files that already exist and are already authoritative (`targets.yaml`'s `caps.clusters`, `issuer_lookthrough.yaml`, `intelligence/relationships/*.yaml`'s `tickers` fields) — nothing here could disagree with those files, because nothing here asserts anything independently of them.

**Why this is the one axis TIER-0001 found "materially" changes an outcome today.** `TIER-0001` §4.4 (independently reviewed and corrected during that PR's own review cycle) found exactly 13 of 27 canonical names are covered by neither a cluster cap nor a relationship record (`COST, ICE, ISRG, LLY, PANW, RKLB, RTX, SNPS, SPGI, TMO, TSLA, V, WM`) — a real, evidenced, currently-invisible-without-manual-cross-referencing gap. `unmeasured_flag` operationalizes that finding as a standing, always-current, per-ticker fact rather than a one-time count that goes stale the moment a new relationship record or cluster changes membership. This directly changes risk interpretation — a reviewer can now read one field instead of manually cross-referencing three files, exactly the "materially changes an outcome" bar the design standard requires.

**What this explicitly does not authorize.** Neither `unmeasured_flag` nor `notes` implies, recommends, or triggers a new cluster cap, a new correlation scan, or any extension of `caps.clusters`/`issuer_lookthrough.yaml` membership. Any such extension remains its own separate, future, evidence-based governance decision — exactly `REL-0001` §G/§L's existing discipline (structural evidence and measured correlation stay separate, and no correlation study is authorized by naming a gap).

### 3.6 Axis 4 — Uncertainty & Evidence Quality (`evidence_quality`)

| Sub-field | Type | Allowed values | Fact or judgment |
|---|---|---|---|
| `primary_source_coverage` | closed enum, computed | `comprehensive` \| `partial` \| `limited` \| `blocked` | Factual, computed |
| `highest_disclosed_risk_severity` | computed rollup | Reuses the ticker's own `risks[].severity` values (existing, already-differentiated vocabulary — `moderate`/`low`/`high`) | Factual, computed |
| `thesis_uncertainty_statement` | required short narrative | One sentence: the single disclosed fact or event that would most undermine this ticker's `economic_role`/`capital_priority` assessment | Judgment |
| `review_trigger_notes` | optional short narrative | Free text naming an event-driven re-review condition | Judgment |

**What this answers:** "how strong and complete is the evidence behind this ticker's classification, and what would most invalidate it?"

**Fields explicitly excluded, and why (matching TIER-0001's own rejections, not re-litigated).** `risks[].status` (100% uniform across all 253 risk entries, per `TIER-0001` §4.9) and `monitoring_enabled` (100% uniform across all 47 enrolled rows, per `TIER-0001` §4.6) are **not** reused or re-surfaced anywhere in this axis. Both stay exactly as they are in their existing owning schemas (Company Intelligence, `intelligence/freshness_registry.yaml`), unrevisited until they actually vary in practice — repeating a decorative field inside a second schema would not make it less decorative.

**How review cadence is handled without duplicating `review.cadence_days`.** `review_trigger_notes` names a **condition** ("re-review on the next 10-Q" / "re-review if the PPA is amended"), never a **schedule**. `AUTO-0001`/`PI-0003` remain the sole owner of `review.cadence_days`/`last_reviewed`/`next_due` — this field is advisory input a human could use when manually editing those existing fields, exactly mirroring `OPS-0006` §13's own already-accepted, already-unexecuted preference for event-driven over universal cadence. No new scheduling mechanism is created.

**Distinct from conviction.** Conviction (`PI-0004`) answers "how much do I believe in this"; this axis answers "how well-supported, and how fragile, is what I believe" — a `High`-conviction thesis can carry `limited` primary-source coverage (e.g. a foreign private issuer with restricted disclosure access), and the two must not collapse into one number, matching `ONTO-0001` §F's own "preserved distinctions" discipline applied to a new pair of concepts.

---

## 4. Cross-axis non-duplication check

| Axis | Answers | Does NOT answer (owned elsewhere) |
|---|---|---|
| `economic_role` | What does this holding do, and in what system? | How much conviction (Company Intelligence `conviction.rating`); what tier (`targets.yaml`); what cap applies (`caps.clusters`) |
| `capital_priority` | Does a case exist to reconsider current weight? | The weight itself (`target_pct`, `targets.yaml`, sole authority); the conviction rating |
| `risk_concentration` | What concentration/dependency mechanism, if any, covers this ticker? | The cap threshold itself (`caps.clusters`); the relationship claim's own evidence (`intelligence/relationships/`) |
| `evidence_quality` | How strong is the evidence, what would break the thesis? | The risk list itself (`risks[]`); the review schedule (`review.cadence_days`) |

No two axes, and no axis and an existing repository field, answer the same question. Each axis's factual sub-fields are either newly-authored citations (`economic_role.role_basis`) or pure cross-reference computations from already-authoritative files (`risk_concentration`'s four computed sub-fields, `evidence_quality`'s two computed sub-fields) — nothing here could disagree with an existing source of truth, because nothing here restates one independently.

---

## 5. Design-standard test, applied per field (per the authorizing instruction)

| Field | Changes capital prioritization? | Changes risk interpretation? | Changes monitoring? | Changes review cadence? | Retained? |
|---|---|---|---|---|---|
| `economic_role.*` | Indirectly — supplies the comparator-selection context `capital_priority` needs | No | No | No | Yes (via capital prioritization) |
| `capital_priority.*` | Directly — its entire purpose | No | No | No | Yes |
| `risk_concentration.*` | No | Directly — surfaces coverage gaps invisible today without manual cross-referencing | No | No | Yes |
| `evidence_quality.*` | No | Yes — severity rollup and uncertainty statement inform risk reading | No | Indirectly — `review_trigger_notes` informs (never automates) a human's cadence edit | Yes |

Every retained field changes at least one of the four named decisions, directly or by supplying context another retained field needs to change one. No field was found that changes none of the four; consequently no field is dropped from the four axes at this design stage (a stricter within-axis trim, if warranted, is a Milestone 6/7 question once real drafts exist, not decidable in the abstract here).

---

## 6. Future blind-classification method (Milestone 6 — described, not performed, not begun)

Per `OPS-0006` §2/§3's already-frozen zero-based-research-discipline protocol, applied unmodified: a future, separately authorized Milestone 6 unit would, for each ticker in turn —

1. Open a fresh, blank `intelligence/classification/<TICKER>.yaml` template (the schema in §3 above).
2. Populate all four axes from primary/existing evidence only. The reviewer must not consult that ticker's current `target_pct`, `portfolio_role_ref`, gate status, or cluster membership while drafting `economic_role` or `capital_priority` — exactly `OPS-0006` §2's "conclusions formed independently before formal comparison" rule, applied per-ticker rather than portfolio-wide.
3. Record the draft as sealed and timestamped **before** any comparison to current policy — matching `MARGIN-0005`'s own untouched-test-set sealing precedent, applied here to a classification draft rather than a simulation trial.
4. Only at a dedicated future Milestone 7 reconciliation step, compare the blind draft against current `target_pct`/`portfolio_role_ref`/cap membership, and record agreement or disagreement explicitly — never silently, matching `OPS-0006` §2's "no silent inheritance of an old classification" rule.

This description is not an authorization to begin, does not classify any ticker, and does not create the template file named above.

---

## 7. Lane M factual synchronization: TIER-0001 (PR #245) post-merge state

Folded into this filing per `OPS-0008` §4(a)'s read-only-by-default post-merge convention, matching the `REL-0002`→`REL-0003` chain's own established pattern, rather than a dedicated reconciliation PR.

Independently re-confirmed this session via the GitHub API (not assumed from the PR's own post-merge-verification comment, though that comment's claims were cross-checked and found accurate):

- **State**: `MERGED`, merge commit `96020e55b5317aa6191733e22d2df84bea4a6574` (base `09fc72b4671fb18d9b3a4c2f1f1141657660ad35`, accepted head `eed05c07c2604a18466f345a1bb9c8877705f5a2`), merged 2026-08-05T00:32:52Z, merged by `Mast3rkey`.
- **Independent review**: `4859945925` (CHANGES REQUIRED — 2 MAJOR: overstated 19/27 vs. actual 13/27 coverage-gap arithmetic in the retained artifact; premature `status: complete`/`pr: 245` on the gate's own still-open PR — plus 1 MINOR, 1 NOTE).
- **Correction**: commit `eed05c07`, resolving all three actionable findings.
- **Delta review**: `4860022747` — "DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE," all corrections independently re-verified, zero new issues.
- **Principal acceptance**: `issuecomment-5186141437`, explicit acceptance quoted verbatim at exact head `eed05c07c2604a18466f345a1bb9c8877705f5a2`.
- **Post-merge verification**: `issuecomment-5186176928` (posted the same session, before this filing began) — 72 decisions/`issues == ()`, YAML clean, three validators clean, 183/183 focused + 2581/2581 full suite passing, `git diff --check` clean, protected paths byte-identical to base, exactly one `priority: primary` workstream, merge-commit CI `success`.

**Conclusion.** `TIER-0001` is fully merged, reviewed, corrected, delta-approved, principal-accepted, and post-merge verified. This filing's own `operations/WORKSTREAMS.yaml` change (§L of the governing decision) adds a `tier0001-post-merge-verification` gate recording this state — the pre-existing `tier0001-classification-question-inventory-bounded-unit` gate entry is left unedited, matching this repository's convention of never rewriting a gate's own historical text, exactly the `rel0002-post-merge-verification` / `rel0003-post-merge-verification` pattern already established. This synchronization creates no new tier/target/holdings/cluster/cap/allocator/margin authority and does not itself advance the `milestone-5-zero-based-classification-and-tier-architecture-review` gate's own `status: proposed` beyond what this filing's own new gate entry (§8 of the governing decision) separately records.

---

## 8. What this design explicitly does not do

- Does not classify NVDA, GEV, or any other ticker under this or any framework.
- Does not create `intelligence/classification/` or any file inside it.
- Does not modify `docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, or any existing Company/Theme/relationship record.
- Does not modify `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, or `margin_state.py`.
- Does not perform blind classification or baseline reconciliation.
- Does not compute a mechanical score or ranking of any kind.
- Does not authorize Milestone 6 (blind classification), Milestone 7 (baseline reconciliation), Milestone 8 (policy recommendation package), or Milestone 9 (independent review and adoption).
- Does not resolve TIER-0001's six unresolved questions — §3.3-§3.6 above narrow two of them (question #6, where framework output would live; and partially question #2, by declining to build a conviction→target_pct formula) but the remaining questions (portfolio_role_ref migration timing, risk-concentration coverage extension, review-cadence proportionality execution, gated-name classification necessity) stay open for future principal judgment.

---

_Retained per `governance/audits/README.md` convention, alongside `WS0005_M5_CLASSIFICATION_QUESTION_INVENTORY_20260804.md` and its predecessors — a self-authored implementation-output design artifact, not an independent reviewer's output. Independent review of this artifact and its accompanying PR is the pending next step, per `TIER-0002`._
