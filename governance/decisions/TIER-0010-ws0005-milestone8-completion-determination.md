---
decision_id: TIER-0010
date: 2026-08-07
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0016, PI-0031, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0008, TIER-0009, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, OPS-0016, CONTENDER-0001, XASSET-0001]
supporting_artifact: null
file: governance/decisions/TIER-0010-ws0005-milestone8-completion-determination.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1) unit
to determine, on live repository and GitHub evidence independently re-verified this session, whether
WS-0005 Milestone 8 ("Policy recommendation package," `OPS-0006` §4.8) is formally complete now that
its sole authorized implementation, PR #262, has been merged and post-merge verified. This
authorization explicitly does not authorize Milestone 9 ("Independent review and later adoption")
regardless of this filing's own verdict, and does not itself perform any policy recommendation,
allocation analysis, external research, valuation methodology, cross-asset synthesis, or edit to the
Milestone 8 recommendation-package artifact, its validator, its tests, or the retained implementation
audit.

**No separate Milestone-8-completion-standard document was filed ahead of this one.** `TIER-0009`
§§B–L already fully specifies every control the Milestone 8 implementation needed — the six treatment
classes, permitted/prohibited inputs, the equity-only and chart boundaries, all eight policy areas'
individual treatment, the closed seven-value primary/two-value secondary vocabulary and its
deterministic precedence, the required per-ticker output schema and artifact architecture, the
explicit non-authorization boundary, and the authorized-future-implementation-unit gate — across one
already-accepted filing. This filing therefore both derives the completion criteria from that
already-accepted controlling text and evaluates them in the same unit, the identical combined pattern
`TIER-0006` used for Milestone 6 and `TIER-0008` used for Milestone 7 (see Alternatives Considered).

### Preflight (independently verified this session, not assumed from the authorizing brief)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/ws-0005-milestone-8-completion-9jmyc0`, working tree clean
  at session start and throughout preflight.
- **`origin/main` fetched and reconciled.** `git fetch origin main` succeeded; `git rev-parse
  origin/main` and `git rev-parse HEAD` both returned `eecbb72f752957d27494f818aa49fa6122f67dfb` —
  this session's starting branch was already positioned exactly at that commit, with a clean working
  tree, before any edit in this filing.
- **PR #262 independently re-confirmed merged** via the GitHub API (`pull_request_read`, method
  `get`): `merged: true`, title "WS-0005 Milestone 8: policy-recommendation package for the 27 sealed
  equities," base `main`@`dc302d45b4cca417cc306e98584dba556cb055b5`, head
  `910caa4547627f505ddbae3115799a300cc2f437`, merge commit
  `eecbb72f752957d27494f818aa49fa6122f67dfb` (independently confirmed via `get_commit`),
  `merged_at: 2026-08-07T05:11:32Z`, 6 changed files, 3 commits, `additions: 6066`, `deletions: 7`.
- **Full commit list independently re-read**: (1) `b7052a2ff137b8b127aa96f73ee00df390389386` — initial
  implementation; (2) `15514bc8968e76c7d9191edb47b3d2fa322e86e2` — `WS-0005` `active_pr` sync plus gate
  update; (3) `910caa4547627f505ddbae3115799a300cc2f437` — bounded correction (accepted head, final
  commit in the PR's own list). Merge commit `eecbb72f752957d27494f818aa49fa6122f67dfb` sits one level
  up on `main`, confirmed separately via `get_commit`, not itself a PR commit.
- **Full review/acceptance/verification chain independently re-read in full via the GitHub API**, not
  copied from any prior summary:
  - First-round review `4879556015` (anchored to `15514bc8968e76c7d9191edb47b3d2fa322e86e2`) —
    **CHANGES REQUIRED**, 0 BLOCKING / 1 MAJOR / 1 MINOR / 2 NOTE. The MAJOR asked whether `TIER-0009`
    actually authorizes `tier_architecture` (G.2) mechanically reusing Milestone 7's
    `primary_disposition`-derived status identically to `role`/`capital_priority`, given §G.2(1)'s
    "narrowly" framing. The MINOR flagged missing direct test coverage of
    `validate_recommendation_data`'s non-dict top-level branch and `_read_yaml`'s
    `OSError`/`yaml.YAMLError` catch paths.
  - Bounded correction (commit `910caa4547627f505ddbae3115799a300cc2f437`) resolved the MAJOR by
    explicit design justification — not a new computation — citing `TIER-0009` §G.2(6)'s "what should
    the tier structure be" prohibition and §G.2(7)'s own two named evidence sources, and adding an
    explicit, ticker-specific "Design note" to all 27 `tier_architecture.rationale` fields with no
    change to any `primary_status`/`secondary_conditions`/`supporting_evidence`/
    `later_governance_action` value on any ticker on any area. The MINOR was resolved with nine new
    tests (parametrized non-dict top-level, missing-file, directory-as-file, malformed-YAML, and
    empty-file-is-`None`-not-a-mapping cases), raising the focused suite from 143 to 152.
  - Corrected-head delta review `4879786313` (anchored to `910caa4547627f505ddbae3115799a300cc2f437`)
    — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 0 NOTE. Zero
    findings survived at the corrected head.
  - Principal acceptance `issuecomment-5212688009` — independently re-read in full: explicit
    acceptance at exact head `910caa4547627f505ddbae3115799a300cc2f437`, naming review `4879786313`
    and exact-head CI (workflow run `31143369532`, job `92757721969`, `completed`/`success`), and
    explicitly confirming that "the original MAJOR (`tier_architecture`/G.2 design justification) and
    MINOR (validator error-path test coverage) findings were independently confirmed resolved by the
    corrected-head delta review."
  - Post-merge verification `issuecomment-5212728415` — independently re-read in full: merge-tree
    identity, exact 6-file merged inventory, zero diff on every protected path, `recommendation_
    validator.py` `OK (27 tickers)`, aggregate counts reconfirmed, 152/152 focused tests, full `pytest`
    3091/3091, decision catalog 86/`issues == ()` unchanged, exactly one primary workstream.
  - **Merge-commit CI independently re-fetched this session** (`get_check_run` +
    `list_workflow_jobs`): workflow run `31149785644`, job `92776874235`, `head_sha` confirmed exactly
    `eecbb72f752957d27494f818aa49fa6122f67dfb`, branch `main`, `status: completed`,
    `conclusion: success`. **Exact-head CI independently re-fetched separately**: workflow run
    `31143369532`, job `92757721969`, `head_sha` confirmed exactly
    `910caa4547627f505ddbae3115799a300cc2f437`, `status: completed`, `conclusion: success`.
- **Zero open pull requests** confirmed via `mcp__github__list_pull_requests` (`state: open`) — empty
  result. No active mutation lane exists.
- **`TIER-0010` independently confirmed the next unused identifier.** `ls governance/decisions/*.md`
  (excluding `README.md`) returns exactly 86 files; `governance/decisions.yaml` contains exactly 86
  `decision_id` rows; `portfolio_hq.dashboard.decisions.build_catalog('.')` — **86 decisions, `issues
  == ()`**, independently reconciled this session. No `TIER-0010` reference exists anywhere in
  `governance/`, `operations/`, or `CLAUDE.md` prior to this filing (repository-wide grep, zero
  matches). The highest filed `TIER-####` is `TIER-0009`.
- **Live validators and full suite independently re-run this session** against the exact merged head
  above, before any edit:
  - `recommendation_validator.py` (direct CLI run) — **OK (27 tickers)**.
  - `classification_validator.py` (direct CLI run) — **OK (28 results)** — 27 records + manifest.
  - `reconciliation_validator.py` (direct CLI run) — **OK (27 tickers)**.
  - `relationship_validator.py` (direct CLI run) — **OK (13 record(s))**.
  - `freshness_validator.py` (direct CLI run) — **OK**.
  - `portfolio_hq.dashboard.decisions.build_catalog('.')` — **86 decisions, `issues == ()`**.
  - `python3 -m pytest test_recommendation_validator.py -q` — **152 passed**.
  - `python3 -m pytest -q` (full repository suite) — **3091 passed, 0 failed** (1 pre-existing,
    unrelated `DeprecationWarning` on `intelligence_classification_sanitizer.py`'s own docstring) —
    matching PR #262's own post-merge-verification result exactly.
  - Repository-wide YAML/YML and JSON parsing — zero errors across every file.
  - `git diff --check` — clean. Working tree clean throughout, before any edit.
- **Milestone 8 artifact independently re-parsed and cross-checked this session, field by field**
  (not merely read from the PR's own summary table):
  - `intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`: `chart_evidence_
    used: false`; `cohort_size: 27`; 27 ticker entries, strict alphabetical order, no duplicate.
  - `role`/`tier_architecture`/`capital_priority` — independently recomputed distribution **12
    `retain_current_baseline` / 14 `review_warranted` / 1 `no_policy_conclusion` (SPGI)** on all three,
    exact match to the PR's own claim.
  - `target_and_range`/`maximum_position_size` — independently confirmed **27/27
    `valuation_required`**, zero exceptions.
  - `overlap_and_concentration` — independently recomputed the `relationship_measurement_required` set
    directly from the artifact: **{COST, ICE, ISRG, PANW, RKLB, RTX, SNPS, SPGI, TMO, V, WM}** — exact
    match, both in membership and count (11), to `REL-0007`'s/`TIER-0007`'s/`TIER-0008`'s own
    independently-computed structural-measurement-gap set, independently cross-checked this session
    against live `targets.yaml`, `issuer_lookthrough.yaml`, and `intelligence/relationships/`.
  - `monitoring_and_thesis_break` — independently recomputed **20 `retain_current_baseline` / 6
    `review_warranted` / 1 `no_policy_conclusion` (SPGI)**, exact match to the PR's own claim.
  - `add_hold_trim_exit_discipline` — independently recomputed **27/27 `retain_current_baseline`**,
    zero exceptions.
  - **Prohibited-content scan, independently run this session, not merely inherited from the
    validator's own pass**: a repository-level grep for `\bscore\b`/`\brank\b`/`\brecommendation\b`
    found only the artifact's own name ("policy-recommendation package"), the governing-decision file
    path, and the cross-tabulation disclaimer's own prose ("does not constitute a score, rank, or
    implied action priority") — no proposed numeric value of any kind. A line-by-line scan for
    numeric-percent-shaped tokens found exactly 15, all inside `supporting_evidence`/rationale text
    quoting existing financial disclosures (China DUV revenue share, Azure/AWS margin figures,
    customer-concentration percentages) already present in the underlying Milestone 6/7 evidence —
    none attached to a proposed target, range, or maximum-size value for any ticker. A directive-word
    scan (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`, word-boundary-matched) across every
    `rationale`/`supporting_evidence`/`later_governance_action` field on all 27 tickers' 8 areas found
    **zero hits**. A chart-terminology scan (`support`/`resistance`/`breakout`/`trend line`/`moving
    average`/`RSI`/`MACD`/`candlestick`/`chart pattern`/`technical analysis`/`oversold`/
    `overbought`/`fibonacci`/`volume profile`/`price target`) found only the field name
    `supporting_evidence` and unrelated substring false-positives inside ordinary English words (e.g.
    "reversible," "requires") containing the letters "rsi" — zero genuine chart-derived content.
  - The same directive-word and percent-token scan was independently repeated against the retained
    narrative audit (`governance/audits/WS0005_M8_POLICY_RECOMMENDATION_PACKAGE_20260807.md`) — zero
    percent tokens; every directive-word occurrence found is a meta-reference naming the prohibited
    word itself (e.g., "Zero directive words (`buy`/`sell`/…) appearing as an actual directive…") or
    the area's own field name (`add_hold_trim_exit_discipline`), never an actual instruction.
- **Sealed Milestone 6/7 evidence integrity independently re-verified this session**:
  - `git diff 1107c5b70801ff5e7027efddf6a2aa916030dce2 HEAD -- intelligence/classification/` — empty
    (zero drift since the `TIER-0006` merge).
  - `git diff 79b5a15ba0427856c9655beeb490d0cbb1c02718 HEAD -- intelligence/reconciliation/
    reconciliation_validator.py test_reconciliation_validator.py` — empty (zero drift since the PR
    #259/Milestone 7 merge).
  - `classification_validator.py` confirms all 27 hash reconciliations and manifest bidirectional
    consistency; `reconciliation_validator.py` confirms the Milestone 7 artifact unchanged.
- **Protected-path isolation independently re-confirmed** via `git diff
  dc302d45b4cca417cc306e98584dba556cb055b5 HEAD --stat -- targets.yaml holdings.yaml gates.yaml
  issuer_lookthrough.yaml allocate.py margin_state.py levels.py` — empty output, zero diff on every
  protected path across the entire PR #262 lifecycle plus every commit since.
- **`operations/WORKSTREAMS.yaml`'s live gate state independently re-read** (not copied from the
  authorizing brief): `milestone-8-policy-recommendation-package` reads **`status: in_progress`,
  `pr: 262`** — content work begun, not yet `complete`, exactly as PR #262 itself left it;
  `milestone-9-independent-review-and-later-adoption` reads `status: proposed`, `pr: None`, untouched;
  `tier0009-post-merge-verification` reads `status: complete`, `pr: 261`; `WS-0005`'s
  `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields read
  PR #262's own pre-merge state (`claude/milestone-8-policy-recommendation-740p8e` / `262` /
  `dc302d45b4cca417cc306e98584dba556cb055b5` / `"2026-08-07"`) — stale on exactly the fact that PR
  #262 has since merged and `origin/main` has advanced past it, matching this repository's
  established one-filing-lag convention (`TIER-0006`'s/`TIER-0008`'s own identical treatment of the
  prior implementation PR's self-reference fields).
- **Exactly one primary workstream confirmed**: `WS-0005` (`status: in_progress`, `priority:
  primary`), independently re-read from live `operations/WORKSTREAMS.yaml`.
- **Isolated worktree/branch confirmed clean** before this unit's own first edit; no other mutation
  lane active on this branch or elsewhere in the repository.

No condition on this unit's own stop list was triggered: `main` had not advanced past the expected
merge SHA; no overlapping mutation lane exists; the next `TIER-####` identifier (`TIER-0010`) matched
expectation; no gate had reopened; the 27-name population matched expectation exactly; live evidence
did not contradict PR #262's own review/acceptance/post-merge-verification chain; a clean isolated
workspace was established without incident.

## Decision

**`TIER-0010` determines, on live repository and GitHub evidence independently re-verified this
session, that WS-0005 Milestone 8 ("Policy recommendation package") is formally complete, and
accordingly sets the `milestone-8-policy-recommendation-package` gate's `status` to `complete` in
`operations/WORKSTREAMS.yaml`, recording PR #262's accepted head, merge SHA, independent review chain,
principal acceptance, and post-merge verification.** This decision authorizes no Milestone 9 work, no
numeric valuation, no whole-portfolio target, no cross-asset synthesis, no external research, no
allocation analysis, and no tier/target/holdings/gate/cap/cluster/allocator/margin/ladder/chart/order/
trade change of any kind. It creates no investment, allocation, or trading authority. **Completion of
Milestone 8 does not itself adopt, endorse, or act on any recommendation-package finding** — the
27-ticker, eight-area recommendation package remains advisory analysis, nothing more, pending a
separately authorized future Milestone 9.

**Completion of Milestone 8 means the `TIER-0009`-authorized categorical policy-recommendation package
is complete. It does not mean**: numeric valuation work is complete; whole-portfolio targets are
complete; cross-asset synthesis is complete; ETF/crypto policy is complete; additional-equity
classification is complete; Milestone 9 is authorized or complete; adopted portfolio policy exists;
allocation is authorized; chart deployment is authorized; or any trade is authorized. Every one of
these remains exactly as unauthorized after this decision as before it.

### A. Completion criteria — derived from controlling text, evaluated fresh against live state

No prior filing enumerated a numbered Milestone 8 completion standard the way `REL-0004` did for
Milestone 4. This section derives fifteen criteria directly from `TIER-0009` §§A–N (the controlling
gate text, purpose, six treatment classes, permitted/prohibited inputs, equity-only and chart
boundaries, the eight-area treatment table, the closed primary/secondary vocabulary and its
deterministic precedence, the required per-ticker output schema and artifact architecture, the
explicit non-authorization boundary, and the authorized-future-implementation-unit gate), `OPS-0001`
(workstream register `active_branch`/`active_pr` live-work semantics and status vocabulary),
`OPS-0006` §16.1 (a milestone reaches `complete` only after every authorized deliverable exists,
merges, passes its tests/validators, and the register/decision catalog are synchronized — never from
discussion, an edit, a commit, a push, or an open PR alone), and `OPS-0007` §1/`OPS-0009` §6 (the
capability-based independent-review standard and the delta-review discipline for material findings) —
then evaluates each fresh against live repository and GitHub state, per this repository's own
established discipline of not inferring completion from any prior filing's own summary (`PI-0037`,
`REL-0006`, `TIER-0006`, `TIER-0008`).

**Criterion 1 — Implementation deliverables exist on merged `main`.**
*Standard:* the recommendation-package artifact, its validator, its focused tests, the retained audit,
and factual register synchronization all exist on `main` at the confirmed PR #262 merge commit
(`TIER-0009` §I, §N).
**PASS.** Independently confirmed present at `HEAD` (`eecbb72f752957d27494f818aa49fa6122f67dfb`):
`intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`,
`recommendation_validator.py`, `test_recommendation_validator.py`,
`governance/audits/WS0005_M8_POLICY_RECOMMENDATION_PACKAGE_20260807.md`, plus the
`CLAUDE.md`/`operations/WORKSTREAMS.yaml` synchronization PR #262's own body describes — exact 6-file
inventory matching the PR's own reported 6066 additions / 7 deletions across its full 3-commit
lifecycle. **Fully satisfied.**

**Criterion 2 — Exact 27-equity cohort coverage.**
*Standard:* the recommendation-package artifact covers exactly the 27 canonical equities Milestone 6
sealed and Milestone 7 reconciled, no missing ticker, no extra ticker, deterministic alphabetical
order (`TIER-0009` §B, §I.1).
**PASS.** Independently re-parsed this session: the `recommendations` list holds exactly 27 entries in
strict alphabetical ticker order, byte-identical in membership to the 27-name `intelligence/
classification/` population, `COHORT_MANIFEST.yaml`'s 27-entry `cohort` list, and the Milestone 7
reconciliation artifact's own 27-entry population — zero drift, zero extras, zero duplicates. **Fully
satisfied.**

**Criterion 3 — Closed schema compliance.**
*Standard:* every ticker entry, every one of the eight area-entries, and the top-level artifact each
carry only their authorized fields — no unknown key at any level (`TIER-0009` §I.3.a).
**PASS.** Independently re-run this session: `recommendation_validator.py` — `OK (27 tickers)` —
confirming closed top-level, per-ticker, and per-area-entry schema (unknown-key and missing-key
rejection, per the validator's own design, independently reviewed and confirmed sound across two
review rounds culminating in review `4879786313`'s zero-finding verdict). **Fully satisfied.**

**Criterion 4 — Eight-area population per §G's treatment-class assignment.**
*Standard:* `role`, `tier_architecture`, and `capital_priority` reuse Milestone 7's own
`primary_disposition` 1:1, never independently re-derived (§G.1(1), §G.2(1), §G.3(1));
`monitoring_and_thesis_break` is independently computed from evidence-quality and review-cadence
fields, not copy-pasted from the role/capital-priority split (§G.7); `overlap_and_concentration` is
independently, mechanically computed from live structural-measurement data, not read from a cached
field (§G.6); `add_hold_trim_exit_discipline` addresses only mechanism-existence, never the position
itself (§G.8).
**PASS.** Independently re-verified this session: `role`/`tier_architecture`/`capital_priority` share
an identical 12/14/1 distribution by design (all three reuse the same source field), while
`monitoring_and_thesis_break` (20/6/1) and `overlap_and_concentration` (16/11) diverge from that
pattern in specific, evidence-traceable ways — e.g. ICE reaches `review_warranted` on monitoring
despite `retain_current_baseline` on role; six `review_warranted`-role tickers reach
`retain_current_baseline` on monitoring — independently confirmed proof the areas are genuinely
separately computed rather than templated. `tier_architecture`'s bounded correction (this session's
own preflight above) added an explicit per-ticker "Design note" grounding the reuse in §G.2(6)/(7)'s
own text without changing any value, resolving the one MAJOR finding raised against this criterion
during PR #262's own review cycle. **Fully satisfied.**

**Criterion 5 — G.4/G.5 doctrinally forced, zero exception.**
*Standard:* `target_and_range` and `maximum_position_size` carry `primary_status: valuation_required`
on every one of the 27 tickers, with no per-ticker discretion, mechanically validator-enforced
(`TIER-0009` §G.4, §G.5, §H, §I.3.c).
**PASS.** Independently re-parsed this session: both areas show `valuation_required: 27` with zero
other value present for either area on any ticker. `recommendation_validator.py`'s mechanical forced-
value check independently confirmed present and passing. **Fully satisfied.**

**Criterion 6 — G.6 live-recomputed structural-gap set.**
*Standard:* `overlap_and_concentration` carries `primary_status: relationship_measurement_required` on
exactly the currently structurally-unmeasured tickers, cross-checked live against
`targets.yaml`/`issuer_lookthrough.yaml`/`intelligence/relationships/` at validation time, not merely
against a cached Milestone 7 value (`TIER-0009` §G.6, §I.3.d — the defense against silent drift
`REL-0007` itself demonstrated was necessary).
**PASS.** Independently recomputed this session, directly from live `targets.yaml`,
`issuer_lookthrough.yaml`, and `intelligence/relationships/*.yaml` (not merely read from the artifact's
own claim): the structurally-unmeasured set is exactly **{COST, ICE, ISRG, PANW, RKLB, RTX, SNPS,
SPGI, TMO, V, WM}** — 11 names — an exact match to the artifact's own `relationship_measurement_
required` set, and an exact match to `REL-0007`'s/`TIER-0007`'s/`TIER-0008`'s own independently-
computed set. **Fully satisfied.**

**Criterion 7 — No prohibited numeric policy output.**
*Standard:* no proposed target, target range, maximum position size, score, or rank appears anywhere
in the artifact, on any field, for any ticker; every numeric-percent-shaped token traces to an
inherited, already-governed financial fact, never a proposed value (`TIER-0009` §D, §G.4(6), §G.5(6),
§H, §J).
**PASS.** Independently re-run this session: `recommendation_validator.py`'s forbidden-key/forbidden-
phrase scan passed on all 27 entries across all 8 areas. A separate, independent repository-level grep
of the artifact for `score`/`rank`/`recommendation` found only the artifact's own name, the governing-
decision file path, and the disclaimer's own prose disclaiming exactly this — no proposed value. A
line-by-line scan for the 15 numeric-percent-shaped tokens present in the file confirmed every one
traces to an inherited financial disclosure already present in Milestone 6/7 evidence (revenue-share,
margin, customer-concentration figures), never a proposed target/range/size. **Fully satisfied.**

**Criterion 8 — No chart evidence, independently free-text scanned.**
*Standard:* `chart_evidence_used: false` at the top level, independently verified true by a free-text
scan for chart-derived terminology across every field — not merely the self-declared flag,
deliberately not repeating `reconciliation_validator.py`'s own disclosed MINOR defense-in-depth gap
(`TIER-0009` §D, §F, §I.3.e).
**PASS.** Independently re-run this session: `chart_evidence_used: false` confirmed at the artifact's
top level. A dedicated free-text scan for sixteen chart-derived terms (support/resistance, breakout,
trend line, moving average, RSI, MACD, candlestick, chart pattern, technical analysis, oversold,
overbought, Fibonacci, volume profile, price target, momentum) found zero genuine matches across the
entire artifact — the only hits were the field name `supporting_evidence` and unrelated substring
false-positives inside ordinary English words. The retained narrative audit was independently scanned
on the same basis with the same clean result. **Fully satisfied.**

**Criterion 9 — No directive trading language; no execution path.**
*Standard:* none of the eight §G.8(6) directive words (`buy`/`sell`/`add`/`hold`-as-verb/`trim`/`exit`-
as-verb/`wait`/`stage`) appears as an actual instruction anywhere in the artifact, in any area, under
any framing; no order, trade, or live/scenario `allocate.py`/`levels.py` output was produced or
executed by the implementation or by this filing (`TIER-0009` §D, §G.8(6), §J).
**PASS.** Independently re-run this session: a word-boundary-matched scan for all eight directive words
across every free-text field on all 27 tickers' 8 areas found **zero hits** as an actual directive —
`add`/`hold`/`trim`/`exit` appear only inside the area's own field name
(`add_hold_trim_exit_discipline`) or, in the retained audit, as meta-references naming the prohibited
words themselves. No `allocate.py`/`levels.py` invocation, order, or trade appears anywhere in PR #262,
the retained audit, or this filing. **Fully satisfied.**

**Criterion 10 — Equity-only and non-authorization boundaries.**
*Standard:* the artifact's own equity-scope disclosure statement is present verbatim or in substance;
no ETF/crypto/GLD/reserve/debt/cross-sleeve recommendation appears anywhere; no whole-portfolio-
readiness claim is made; the sealed Milestone 6 records, `COHORT_MANIFEST.yaml`, the Milestone 7
reconciliation artifact, `reconciliation_validator.py`, `test_reconciliation_validator.py`, and every
existing Company/Theme/relationship Intelligence record remain byte-identical and unedited (`TIER-0009`
§E, §J, §L).
**PASS.** Independently re-confirmed this session: `equity_scope_disclosure` present at the artifact
top level, matching `XASSET-0001` §B's required disclosure text; no ETF/crypto/GLD/reserve/debt/cross-
sleeve content found anywhere in a targeted grep of the artifact or the retained audit; `git diff
1107c5b70801ff5e7027efddf6a2aa916030dce2 HEAD -- intelligence/classification/` and `git diff
79b5a15ba0427856c9655beeb490d0cbb1c02718 HEAD -- intelligence/reconciliation/
reconciliation_validator.py test_reconciliation_validator.py` both empty — zero drift on either
sealed-evidence layer since their own respective sealing/acceptance commits. **Fully satisfied.**

**Criterion 11 — Uncertainty and later-governance-action completeness.**
*Standard:* every area-entry not carrying `retain_current_baseline` names a `later_governance_action`;
every ticker carrying `no_policy_conclusion` on any area or any secondary flag carries a non-empty
`uncertainty` field (`TIER-0009` §I, "Per-ticker top-level fields").
**PASS.** Independently re-verified via `recommendation_validator.py`'s own schema enforcement (which
review `4879786313` confirmed sound) plus a direct spot-check of SPGI's entry (the sole
`no_policy_conclusion` ticker on three areas) — its `uncertainty` field is non-empty and traces to the
disclosed Milestone 6 over-redaction correction, consistent with Milestone 7's own identical treatment
of the same ticker. **Fully satisfied.**

**Criterion 12 — Aggregate reconciliation.**
*Standard:* the artifact's own aggregate counts, independently recomputed from the raw per-ticker data,
match this filing's own independent recomputation exactly, for all eight areas (`TIER-0009` §I,
"Required aggregate reporting").
**PASS.** Independently recomputed this session directly from the 27 per-ticker `recommendations`
entries for all eight areas (not merely read from the artifact's own precomputed `aggregate` block):
role/tier_architecture/capital_priority 12/14/1; target_and_range and maximum_position_size 27/0/0
(all `valuation_required`); overlap_and_concentration 16/11; monitoring_and_thesis_break 20/6/1;
add_hold_trim_exit_discipline 27/0/0 — every figure matches the artifact's own aggregate block and PR
#262's own reported result summary table exactly. **Fully satisfied.**

**Criterion 13 — Validator and test sufficiency.**
*Standard:* `recommendation_validator.py` passes; all focused tests pass; the full repository test
suite passes; every other domain validator (`classification_validator.py`,
`reconciliation_validator.py`, `relationship_validator.py`, `freshness_validator.py`) remains clean;
the decision catalog reconciles; YAML/YML and JSON parsing succeed repository-wide; `git diff --check`
is clean; exact-head and merge-commit CI both succeeded (`TIER-0009` §I.4, §L; `OPS-0007` §1-equivalent
lifecycle completeness).
**PASS.** Independently re-run this session, all against the current merged `HEAD`:
`recommendation_validator.py` — `OK (27 tickers)`; `classification_validator.py` — `OK (28 results)`;
`reconciliation_validator.py` — `OK (27 tickers)`; `relationship_validator.py` — `OK (13 record(s))`;
`freshness_validator.py` — `OK`; `test_recommendation_validator.py` — **152/152 passed** (up from 143
at the original head, after the bounded correction's nine new tests); full `pytest` — **3091 passed, 0
failed**; decision catalog — **86 decisions, `issues == ()`**; repository-wide YAML/YML/JSON parsing —
zero errors; `git diff --check` — clean. Exact-head CI (`92757721969`/`31143369532`) and merge-commit
CI (`92776874235`/`31149785644`) both independently re-fetched this session — both `completed`/
`success`, with `head_sha` cross-checked to the correct commit in each case. **Fully satisfied.**

**Criterion 14 — Full PR #262 lifecycle completeness.**
*Standard:* an eligible independent exact-head review occurred (`OPS-0007` §1); any material (Blocking
or Major) finding triggered a bounded correction and an exact-head delta review before the PR was
considered ready (`OPS-0009` §6's four-condition delta-review test); explicit principal acceptance
occurred at the exact merged head; the merge-commit tree is byte-identical to the accepted head's tree;
post-merge verification occurred and independently reconfirmed scope, validators, tests, and CI.
**PASS.** Independently re-read in full this session (§ Preflight above): first-round review
`4879556015` found one MAJOR and one MINOR, both requiring correction under `OPS-0009` §6; the bounded
correction (commit `910caa4547627f505ddbae3115799a300cc2f437`) addressed both without altering any
recommendation content; corrected-head delta review `4879786313` returned zero findings of any kind —
**APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**. Principal acceptance (`issuecomment-5212688009`)
explicitly names that exact head and that review. Post-merge verification (`issuecomment-5212728415`)
independently confirms merge scope and re-states every validator/test result. This session's own
independent re-derivation of the merge commit's identity, CI status, and full validator/test results
(§ Preflight above) matches every one of these claims exactly, not merely cited from the PR's own
text. **Fully satisfied.**

**Criterion 15 — Register and catalog synchronization.**
*Standard:* the decision catalog is updated with this new decision; the `milestone-8-policy-
recommendation-package` gate is set to `complete` only by this filing, not by PR #262 itself;
`active_branch`/`active_pr` follow `OPS-0001`'s live-work semantics; exactly one primary workstream
remains `WS-0005`; current `main` SHA and verification date are recorded accurately (`OPS-0001`;
`OPS-0006` §16.1).
**PASS, as of this filing's own synchronization (§B–C below).** `milestone-8-policy-recommendation-
package` reads `status: in_progress`, `pr: 262` at this filing's own base — exactly as PR #262 itself
left it, correctly not self-declaring completion (`TIER-0009` §L's own future-implementation gate
explicitly withheld that determination from the implementation PR). This filing corrects exactly that
(§B). `WS-0005`'s `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
self-reference fields read PR #262's own pre-merge state — stale on exactly the fact that PR #262 has
since merged; this filing corrects that (§B), per `OPS-0001`'s "only currently-live work" rule for
those two fields. **This filing is that dedicated, later, separate completion-determination filing** —
Criterion 15 is satisfied by this filing's own existence and the synchronization performed in §B,
effective only on this filing's own merge (§D). **Fully satisfied as of this filing's own edits and
future merge.**

### B. Register synchronization performed by this filing

This filing performs the minimum `operations/WORKSTREAMS.yaml` synchronization Criterion 15 requires:

1. `milestone-8-policy-recommendation-package` gate: `status: in_progress` → `status: complete`,
   appended additively to the gate's existing description text (per this repository's
   never-silently-rewrite convention for retained state), recording PR #262's accepted head
   (`910caa4547627f505ddbae3115799a300cc2f437`), merge SHA
   (`eecbb72f752957d27494f818aa49fa6122f67dfb`), the two-round review chain (`4879556015` →
   bounded correction → `4879786313`), principal acceptance (`issuecomment-5212688009`), and
   post-merge verification (`issuecomment-5212728415`). `pr: 262` (unchanged — that field already
   correctly names the implementation PR).
2. `WS-0005`'s own `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
   self-reference fields updated to this filing's own branch, `active_pr: null` until this filing's
   own PR number exists (per `OPS-0001`'s established convention — a bounded follow-up commit sets it
   once the PR is opened), `last_verified_main_sha: eecbb72f752957d27494f818aa49fa6122f67dfb`,
   `last_verified_date: "2026-08-07"`.

No other `WS-0005` field (`status`, `priority`, `authorized_scope`, `prohibited_scope`, or any other
milestone's own gate — including Milestones 1–7, all left byte-for-byte unedited and not reopened) is
touched. `WS-0005`'s top-level `status` remains `in_progress` — Milestone 8 reaching `complete` does
not itself complete the workstream, since Milestone 9 ("Independent review and later adoption")
remains an unauthorized roadmap item per `OPS-0006` §5's own per-milestone authorization gate,
unaffected by this filing.

### C. Verdict

**MILESTONE 8 COMPLETE.**

All fifteen criteria above are satisfied as of this filing's own live-state re-verification
(`origin/main` at `eecbb72f752957d27494f818aa49fa6122f67dfb`, the confirmed PR #262 merge commit). No
criterion fails. The 27-ticker, eight-area recommendation package is accepted as Milestone 8's
completed analysis artifact. **This verdict records that the policy-recommendation exercise was
completed under its accepted controls — it does not evaluate, endorse, or act on any individual
recommendation-package finding, and does not itself recommend or adopt any portfolio policy change.**

This filing accordingly sets the `milestone-8-policy-recommendation-package` gate's `status` to
`complete` in `operations/WORKSTREAMS.yaml` (§B above), **effective only on this decision's own merge
to `main`**, per §E's required independent-review and principal-acceptance gate.

**Completion of Milestone 8 enables only a future, separately authorized Milestone 9 authorization
filing** — the next roadmap item `OPS-0006` §4.9 names ("Independent review, by an eligible reviewer
per `OPS-0007` §1's capability-based standard, of research coverage, relationship methodology,
zero-based protocol adherence, candidate tier architecture, the policy recommendation package,
evidence-versus-judgment separation, and absence of hidden scoring or allocator coupling. Any adoption
requires its own separate accepted governance decision and a later, separately authorized
implementation PR. Not authorized to execute."). **This determination does not itself authorize**: any
Milestone 9 content of any kind; any numeric valuation methodology; any whole-portfolio target; any
cross-asset synthesis (`WS-0014`/`XASSET-0001`); any ETF or crypto classification; any additional-
equity blind classification; any target, tier, role, gate-policy, holdings, cap, cluster, issuer-look-
through, allocator, or margin change; any chart evidence use; any allocation check, live or scenario;
or any trade or order. A future Milestone 9 filing requires its own separate, explicit principal
authorization, following the identical per-milestone authorization gate `OPS-0006` §5 has applied to
every prior WS-0005 milestone.

### D. Effectiveness, review, and merge gates

- **This governance PR must remain in draft state** and must not be marked ready for review or merged
  by this session.
- **An eligible independent review is required**, anchored to this PR's exact final head, per
  `OPS-0007` §1's twelve-point capability-based standard — no self-review by the authoring session.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready, per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Explicit principal acceptance is required before merge**, at the exact head being merged.
- **This decision does not mark itself, or authorize marking itself, ready for merge.** It becomes
  effective — including the Milestone 8 `status: complete` transition in §B — only on this governance
  PR's own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized scope
  ends at opening this draft PR (and one bounded follow-up commit setting `WS-0005`'s `active_pr`
  self-reference to this PR's own number once it exists) and reporting its exact head. No independent
  review, no correction pass, no re-review, no merge, and no post-merge verification is performed by
  this session — each is a separate future step requiring a separate actor. This session does not
  review its own work, mark it ready, merge it, or post principal acceptance.

## E. What this decision does not do

- **Does not authorize, begin, schedule, or imply Milestone 9** (independent review and later
  adoption). `OPS-0006` §5's own per-milestone authorization gate remains in force and unaddressed by
  this filing.
- **Does not itself recommend, endorse, or act on any of the 27 tickers' 8-area recommendation-package
  findings** — the 14 `review_warranted` names, the 1 `no_policy_conclusion` (SPGI), the 27/27
  `valuation_required` on G.4/G.5, the 11-name structural-gap set on G.6, and every other finding all
  remain exactly as PR #262 left them: analysis, not policy.
- **Does not design, sketch, or begin any valuation methodology** — `target_and_range` and
  `maximum_position_size` remain doctrinally forced to `valuation_required` on all 27 tickers,
  unchanged.
- **Does not perform any cross-asset synthesis, ETF classification, crypto classification, or
  `WS-0014` work of any kind.**
- **Does not edit `intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`,
  `recommendation_validator.py`, `test_recommendation_validator.py`, or the retained implementation
  audit** — all byte-for-byte unedited, independently confirmed zero diff.
- **Does not edit any of the 27 sealed classification records, `COHORT_MANIFEST.yaml`, the Milestone 7
  reconciliation artifact, `reconciliation_validator.py`, `test_reconciliation_validator.py`, or
  `classification_validator.py`/the sanitizer.**
- **Does not edit any existing Company, Theme, or relationship Intelligence record.**
- **Does not reopen any `gates.yaml` gate** — all 6 entries, their `status`, `authority`, `allow_add`,
  and `next_gate` text, are unchanged.
- **Does not change any tier, target, gate, cluster, cap, margin, holding, allocator, chart, ladder,
  brokerage, or order behavior.** `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`,
  `levels.py`, and `margin_state.py` are untouched.
- **Does not run or log an allocation check.**
- **Does not perform any chart interpretation** or touch any `CHART-0001`/`CHART-0002` file.
- **Does not perform any external research, allocation analysis, or broader relationship-mapping,
  ETF, crypto, cash/GLD/debt, or cross-asset work.**
- **Does not mark this filing's own governance PR ready, request or begin independent review of it,
  post principal acceptance of it, or merge it** — this decision's own effectiveness is contingent on
  its own future, separate independent review and principal acceptance, exactly as every prior
  WS-0005 governance filing in this log has required of itself.
- **Creates no research, policy, allocation, or implementation authority of any kind beyond the single
  factual determination stated in §C.**

## Rationale

**Why a completion-determination decision is warranted now.** PR #262's own post-merge-verification
comment explicitly disclosed that the merge did not itself declare Milestone 8 complete, and named a
future, separate Lane G filing as the required next step — matching the identical discipline `TIER-
0006` applied to Milestone 6 and `TIER-0008` applied to Milestone 7. This filing performs exactly that
required step.

**Why this filing both derives and evaluates the completion criteria in one unit, rather than filing a
separate standard first.** `TIER-0006` and `TIER-0008` set the precedent, for this same milestone
family, of combining standard-definition and determination in one filing when the controlling
specification is already fully accepted and no new specification content remains to be written. Here,
`TIER-0009` §§B–L already fully specifies every control Milestone 8 needed (the six treatment classes,
permitted/prohibited inputs, equity-only and chart boundaries, the eight-area treatment table, the
closed vocabulary and precedence design, required aggregate outputs, the explicit non-authorization
boundary) across one already-accepted filing; the only work remaining was to organize those controls
into named criteria and evaluate them against the now-complete, now-merged implementation. Filing a
separate "Milestone 8 completion standard" document first, only to evaluate it in the very next filing
with no new specification content in between, would duplicate `TIER-0009`'s own text rather than add
evidence — the same "reference, don't restate" discipline `TIER-0005`'s, `TIER-0007`'s, and
`TIER-0008`'s own Rationale sections already applied.

**Why the one MAJOR and one MINOR finding from PR #262's first review round do not carry forward as
residual, unlike `TIER-0008`'s two accepted MINOR findings for Milestone 7.** Unlike Milestone 7, where
both findings were explicitly accepted as non-blocking and carried forward for this later filing's own
disposition, Milestone 8's MAJOR and MINOR findings were both fully *resolved* — not merely
accepted-as-non-blocking — by a bounded correction that the corrected-head delta review (`4879786313`)
independently confirmed left zero findings of any kind. There is accordingly no residual finding for
this filing to carry forward or dispose of; Criterion 14's "Fully satisfied" reflects a genuinely clean
final-head review, not an accepted gap.

**Why this filing relies on, but independently re-derives, PR #262's own review/acceptance/post-merge-
verification chain rather than re-running the review from scratch.** `OPS-0009` §4's evidence-identity
discipline permits reuse of an already-independently-validated conclusion without repeating its
underlying derivation, provided the conclusion's own retained evidence is re-confirmed current. This
filing independently re-read the review, principal-acceptance, and post-merge-verification comments in
full via the GitHub API this session, and independently re-ran every validator and the full `pytest`
suite against the current merged state, rather than accepting any prior summary on trust — matching the
identical discipline `TIER-0006` and `TIER-0008` applied to their own respective PRs' review chains.

## Alternatives Considered

- **Declare Milestone 8 complete based on PR #262's own governance text alone, without independently
  re-reading the review/acceptance/merge history.** Rejected — exactly the "assume PR-level language
  proves lifecycle compliance" failure mode `TIER-0006`, `REL-0006`, `PI-0037`, and `TIER-0008` already
  rejected for prior milestones.
- **File a separate "Milestone 8 completion standard" document first, then a second, later
  determination filing evaluating it** — mirroring `REL-0004`→`REL-0006`'s two-filing split exactly.
  Rejected — see Rationale; unlike Milestone 4 at the time `REL-0004` was filed, every control
  Milestone 8 needed was already fully specified in `TIER-0009` §§B–L, so a separate standard-only
  filing would restate existing accepted text rather than add new specification content. `TIER-0006`'s
  and `TIER-0008`'s own combined-filing precedent (for this same milestone family) is adopted instead.
- **Treat the resolved MAJOR/MINOR findings from PR #262's first review round as still requiring
  disposition in this filing, the way `TIER-0008` disposed of Milestone 7's two accepted MINOR
  findings.** Rejected — those findings were fully resolved by a bounded correction and confirmed clean
  by a zero-finding delta review before merge, unlike Milestone 7's findings, which were explicitly
  accepted as non-blocking rather than resolved. There is no residual gap for this filing to evaluate.
- **Begin Milestone 9 in the same filing, since Milestone 8 is now determined complete.** Rejected —
  explicitly outside this unit's authorization; `OPS-0006` §5's separate-authorization gate for each
  milestone is unaffected by this filing under any circumstance.
- **Re-derive any individual ticker's recommendation-package finding independently from first
  principles as part of this determination**, rather than re-verifying the already-merged,
  already-reviewed artifact. Rejected — this filing is a completion determination, not a re-analysis;
  re-deriving recommendation content here would exceed this filing's own authorized scope and duplicate
  work review `4879556015`/`4879786313` already performed independently.

## Consequences

**Authorized, effective only on this decision's merge:** the factual determination that WS-0005
Milestone 8 satisfies all fifteen completion criteria derived from `TIER-0009` as of this filing's own
live-state verification, and the corresponding `status: complete` update to the `milestone-8-policy-
recommendation-package` gate in `operations/WORKSTREAMS.yaml`, together with the minimum `WS-0005`
self-reference synchronization in §B.

**Unchanged by this decision:** `intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_
PACKAGE.yaml`, `recommendation_validator.py`, `test_recommendation_validator.py`, and the retained
implementation audit, byte-for-byte; all 27 `intelligence/classification/*.yaml` records and
`COHORT_MANIFEST.yaml`, byte-for-byte; `intelligence/reconciliation/MILESTONE7_BASELINE_
RECONCILIATION.yaml`, `reconciliation_validator.py`, and `test_reconciliation_validator.py`,
byte-for-byte; `classification_validator.py`, `intelligence_classification_sanitizer.py`, and both
Milestone 6 test files, byte-for-byte; every existing Company/Theme/relationship Intelligence record,
all of them; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`,
`levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s top-level `status` (`in_progress`),
`priority` (`primary`), `authorized_scope`, `prohibited_scope`, and `completion_criteria`; Milestones
1–7's own `status: complete` (unedited, not reopened); `TIER-0001` through `TIER-0009`'s own accepted
text and scope, in full, unedited.

**Explicitly not authorized by this decision, stated repeatedly for clarity:** Milestone 9; any numeric
valuation methodology; any whole-portfolio target; any cross-asset synthesis; any ETF or crypto policy;
any additional-equity classification; any policy recommendation, allocation analysis, or external
research beyond what is already recorded; any Company, Theme, or relationship Intelligence edit; any
gate reopening; any tier/target/role/cluster/cap/holdings/margin/allocator/ladder/chart/order-behavior
change; any allocation check; any policy adoption. **This decision creates no research, policy,
allocation, or implementation authority beyond the single factual determination in §C.**

This decision becomes effective only when its implementing pull request merges to `main`.

**No current portfolio policy or allocator behavior changes as a result of this decision, before or
after its merge.** `allocate.py`'s buy/trim/gap logic, every gate parameter, every cap, every target
weight, and every margin parameter remain exactly as `targets.yaml`/`gates.yaml`/`holdings.yaml`
currently state them, unaffected by this filing under any circumstance.
