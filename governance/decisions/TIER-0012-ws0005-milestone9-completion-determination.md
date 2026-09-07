---
decision_id: TIER-0012
date: 2026-08-07
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0016, PI-0031, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0008, TIER-0009, TIER-0010, TIER-0011, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, OPS-0016, CONTENDER-0001, CONTENDER-0002, XASSET-0001]
supporting_artifact: null
file: governance/decisions/TIER-0012-ws0005-milestone9-completion-determination.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1) unit
to determine, on live repository and GitHub evidence independently re-verified this session, whether
WS-0005 Milestone 9 ("Independent review and later adoption," `OPS-0006` §4.9 — the last milestone
`OPS-0006`'s roadmap named) is formally complete now that `TIER-0011`'s authorized review has been
performed and retained (PR #265, merged). This authorization does not authorize any adoption action,
does not perform any Company/Theme/relationship/classification/reconciliation/recommendation content,
does not correct `intelligence/companies/LLY.yaml` or any other sealed artifact, does not introduce
valuation methodology, and does not create any whole-portfolio conclusion.

**No separate Milestone-9-completion-standard document was filed ahead of this one.** `TIER-0011`
§§A-P already fully specifies every control the Milestone 9 review needed — the seven review subjects,
reviewer eligibility, the closed four-value primary-verdict vocabulary, the required output artifact
and metadata, the chart/equity-only boundaries, and — the controlling section — the adoption boundary
(§K). This filing both derives a completion standard from that existing specification and evaluates it
against live evidence in one unit, the same combined pattern `PI-0031`→`PI-0037` (Milestone 3),
`TIER-0007`→`TIER-0008` (Milestone 7), and `TIER-0009`→`TIER-0010` (Milestone 8) used, since no
dedicated standard document preceded any of those either.

### Preflight performed this session, independently verified, not assumed

- Repository path: `/home/user/Portfolio-HQ`. Local branch `claude/milestone-9-completion-bvwxvd`,
  worktree clean (`git status --porcelain=v1` empty).
- `origin/main` fetched and independently confirmed at `e248b878d7a647ed0d3a3d2c6b7f2bc1d88a6cb3`
  — matching local `HEAD` exactly (no drift). This is PR #265's own merge commit
  (`mcp__github__get_commit` confirms commit message "WS-0005 Milestone 9: retain the independent
  review (TIER-0011 authorized) (#265)").
- Zero open pull requests confirmed via `mcp__github__list_pull_requests` (state: open — empty
  result) immediately before this filing's first edit. No competing mutation lane.
- **PR #264 (`TIER-0011`) independently re-confirmed merged**: accepted head
  `d128e51425f3fa1624cd67c0a7a7c80f1ac66785`, merge commit
  `37c1cb45fc05de525752ee74c93fce84a3cfd688`, 5 changed files, 3 commits. One correction round (a
  provenance-citation MAJOR conflating PR #262's and PR #263's own data, resolved via
  `issuecomment-5217726870`); corrected-head delta review `pullrequestreview-4883454274`
  (APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0/1 NOTE); principal acceptance
  `issuecomment-5217994527`; post-merge verification `issuecomment-5218057990`; exact-head CI
  (`31183269036`/`92881495842`) and merge-commit CI (`31185377413`/`92888483593`) both `success`
  — all independently re-fetched via the GitHub API this session, not assumed from any prior
  filing's own citation.
- **PR #265 independently re-confirmed merged**: accepted head
  `729db1c7c620e293bb6aaf3ba034a4c1b67faca2` (base `37c1cb45...`, 2 commits, 3 changed files).
  Independent exact-head review `pullrequestreview-4884030898` — **APPROVED FOR PRINCIPAL
  EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 NOTE (the retained artifact's
  "Reviewing session" field lacks a concrete, independently-checkable identifier for the prior
  Milestone 9 review — the reviewer classified this as "a disclosed epistemic limitation of the
  chosen retention path... not a defect this PR introduced or concealed," explicitly non-blocking,
  no correction round required). Principal acceptance `issuecomment-5218771870` (explicitly
  accepting the NOTE as non-blocking, explicitly restating that Milestone 9 is **not** declared
  complete by PR #265 itself). Post-merge verification `issuecomment-5218826296` — merge SHA
  `e248b878d7a647ed0d3a3d2c6b7f2bc1d88a6cb3`, merge-tree `c2ec533d0845c13e7aa2bfde6a47c8e02cddae8a`
  byte-identical to the accepted head (zero merge drift), merge-commit CI (`31191451730`/
  `92908994540`) `completed`/`success`, exact 3-file changed inventory, all 7 validators clean,
  decision catalog 88/`issues == ()`, full suite 3091/0, `LLY.yaml` confirmed byte-identical to
  base. All of the above independently re-fetched via the GitHub API this session (`pull_request_read`
  method `get`/`get_comments`/`get_reviews`; `get_commit`) — not assumed.
- `governance/decisions/TIER-0011-...md` read in full (§§Context, A-P) this session — not
  summarized from a prior filing's own description.
- `governance/audits/WS0005_M9_INDEPENDENT_REVIEW_20260807.md` read in full this session (197 lines)
  — the retained review artifact itself, not a secondhand citation of it.
- `operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate
  independently re-read: `status: in_progress`, `pr: 265` — matching PR #265's own post-merge
  verification comment's explicit statement that the review has been "performed and retained" but
  Milestone 9 is "still not formally declared complete."
- `WS-0005`'s top-level `status: in_progress`, `priority: primary` independently re-confirmed via
  direct YAML parse (`yaml.safe_load`), not text search.
- **All nine `OPS-0006` §4 milestone gates individually re-read via YAML parse, not assumed**:
  Milestone 1 `complete` (pr 151); Milestone 2 `complete` (pr 151); Milestone 3 `complete` (pr null
  — `PI-0037`, a pure determination filing carrying no implementation PR of its own); Milestone 4
  `complete` (pr null — `REL-0006`, same shape); **Milestone 5
  (`milestone-5-zero-based-classification-and-tier-architecture-review`) `status: proposed`, `pr:
  null`** — its own gate text states explicitly that no prior filing "advance[s]... this gate's own
  `status: proposed`... which remains accurate for the milestone as a whole"; Milestone 6 `complete`
  (pr 253); Milestone 7 `complete` (pr 259); Milestone 8 `complete` (pr 262); Milestone 9
  `in_progress` (pr 265, pre-this-filing). **This finding — Milestone 5's gate was never closed by
  its own dedicated completion-determination filing, unlike Milestones 3, 4, 6, 7, and 8 — is
  independently material to §H below** and was not stated or implied anywhere in this session's own
  task framing; it was discovered by direct inspection.
- Decision catalog independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog`:
  **88 decisions, 12 legacy, `issues == 0`** — confirming `TIER-0012` (this filing) is the next
  unused `TIER-####` identifier (`TIER-0001` through `TIER-0011` all already filed; no gap).
- All seven WS-0005 validators independently re-run against this exact `HEAD`: `classification_
  validator.py` `OK (28 result(s))`; `reconciliation_validator.py` `OK (27 tickers)`;
  `recommendation_validator.py` `OK (27 tickers)`; `relationship_validator.py` `OK (13 record(s))`;
  `intelligence_validator.py` clean; `freshness_validator.py` `OK`; `contender_registry_validator.py`
  `OK (84 entries)`.
- Full repository `pytest`: **3091 passed, 0 failed**, 1 pre-existing warning
  (`intelligence_classification_sanitizer.py`'s cosmetic `\d` docstring `DeprecationWarning`,
  matching the retained review's own Note 1 exactly) — exact match to the post-PR-#265 baseline.
- Repo-wide YAML/YML parsing: 136 files (matching PR #265's own count), 0 errors. JSON: 178 files,
  0 errors. `git diff --check`: clean.
- `intelligence/companies/LLY.yaml` independently re-read: `catalysts[0].expected` still reads
  `"2026-08-31"` — confirmed unedited.
- Exactly one `priority: primary` workstream: `grep -cE "^    priority: primary"` → 1 (`WS-0005`,
  line 543); `^    priority: secondary` → 13.

## Decision

### A. Milestone 9's controlling gate text (quoted, not restated as authority)

> Independent review, by an eligible reviewer per OPS-0007 §1's capability-based standard (Fable
> remains eligible; any other reviewer meeting every §1 requirement is equally eligible), of research
> coverage, relationship methodology, zero-based protocol adherence, candidate tier architecture, the
> policy recommendation package, evidence-versus-judgment separation, and absence of hidden scoring or
> allocator coupling. Any adoption requires its own separate accepted governance decision and a later,
> separately authorized implementation PR. Not authorized to execute.

`TIER-0011` bound a fuller specification to this text (§§A-P); the review PR #265 retained then
performed and recorded, at the reviewed head `37c1cb45fc05de525752ee74c93fce84a3cfd688`.

### B. Derived Milestone 9 completion standard

Combining `TIER-0011` §§C, D, J, K, N with `OPS-0001`, `OPS-0006` §16.1 ("a milestone reaches
`complete` only after every authorized deliverable exists, its PR merges, tests/validators pass, and
`operations/WORKSTREAMS.yaml`/`governance/decisions.yaml` are synchronized — never from discussion,
an edit, a commit, a push, or an open PR alone"), `OPS-0007` §1, and `OPS-0009` §6, sixteen criteria:

1. `TIER-0011`'s own authorization is merged and effective.
2. One reviewer meeting `TIER-0011` §C's sharpened eligibility standard completed the review.
3. The exact reviewed source commit SHA is recorded.
4. All seven `TIER-0011` §A subjects were evaluated, each with `evidence_inspected` (not a restated
   citation to a prior filing's own self-description).
5. Only `TIER-0011` §J's closed four-value primary-verdict vocabulary is used, per subject.
6. The review is retained per §J's either/or standard (a `governance/audits/` artifact was chosen).
7. All findings are classified by severity and preserved, not summarized away.
8. No unresolved BLOCKING or MAJOR finding remains against the review's own subject matter.
9. The LLY MINOR finding is correctly preserved as an open, unfixed, disclosed finding — not
   silently treated as resolved by this filing or by any prior one.
10. The whole-portfolio boundary (§H) is preserved intact in the retained record.
11. The valuation boundary (`target_and_range`/`maximum_position_size` = `valuation_required` for
    all 27, no numeric value invented) is preserved intact.
12. The review-≠-adoption boundary (§K) is preserved intact, including §K.4's explicit statement
    that even a Milestone 9 completion determination does not itself authorize adoption.
13. No unauthorized policy mutation occurred anywhere in the PR #264/#265 lifecycle (protected-path
    isolation holds).
14. The review-recording PR (#265) completed its full lifecycle — independent review, any required
    correction, principal acceptance, merge, post-merge verification, CI success.
15. Every applicable validator and the full test suite pass at the merged head, independently
    re-run by this filing (not merely cited from a prior filing's own report).
16. `operations/WORKSTREAMS.yaml`/`governance/decisions.yaml` register and catalog synchronization
    is correct as of the merged head, independently re-parsed (not text-searched).

### C. Evaluation

| # | Criterion | Evidence | Verdict |
|---|---|---|---|
| 1 | `TIER-0011` merged/effective | PR #264 merge commit `37c1cb45...`, independently re-confirmed via GitHub API this session (Preflight) | **PASS** |
| 2 | Eligible reviewer completed the review | Retained artifact's own metadata reports a "separate, independent, read-only session distinct from every prior WS-0005 Milestones 3-8 authorship/correction/completion-determination session" per §C; PR #265's own independent review (`pullrequestreview-4884030898`) examined this exact claim and found it a disclosed, non-blocking limitation (no independently-checkable session identifier), not a defect — explicitly accepted by the principal (`issuecomment-5218771870`) without requiring a correction round | **PASS**, with the disclosed identifier-limitation carried forward as residual (§I below), not re-litigated here |
| 3 | Exact reviewed SHA recorded | `37c1cb45fc05de525752ee74c93fce84a3cfd688`, recorded in the retained artifact's top-level metadata table and independently confirmed the exact `TIER-0011`/PR #264 merge commit | **PASS** |
| 4 | All seven subjects evaluated with real evidence | Retained artifact §"Per-subject detail" — each of the seven carries a distinct `Evidence inspected` paragraph naming concrete artifacts/commits/command output, not a restated citation | **PASS** |
| 5 | Only the closed 4-value vocabulary used | All seven verdicts read `sound_no_material_finding`; no fifth value, no score, no weighted average, no aggregate readiness figure anywhere in the artifact (independently grepped this session) | **PASS** |
| 6 | Retained per §J's either/or standard | `governance/audits/WS0005_M9_INDEPENDENT_REVIEW_20260807.md`, 197 lines, read in full this session | **PASS** |
| 7 | Findings classified and preserved | 0 BLOCKING / 0 MAJOR / 1 MINOR / 2 NOTE, each with severity, artifact, affected field, description, impact, and required remediation (for the MINOR) | **PASS** |
| 8 | No unresolved BLOCKING/MAJOR | Confirmed 0/0 in the retained artifact; independently re-derivable — no Blocking- or Major-equivalent finding is stated anywhere in the artifact's "Findings" section | **PASS** |
| 9 | LLY MINOR correctly preserved, not silently resolved | `intelligence/companies/LLY.yaml` `catalysts[0].expected` independently re-read this session: still `"2026-08-31"`, unedited; retained artifact and both `operations/WORKSTREAMS.yaml`/CLAUDE.md text explicitly state the finding remains uncorrected pending a future, separate Intelligence-maintenance unit | **PASS** |
| 10 | Whole-portfolio boundary preserved | Retained artifact's own dedicated section lists all eleven non-conclusions (not exhaustive universe; ETF/crypto/GLD/cash/debt/cross-asset not complete; no final holdings/weights/whole-portfolio readiness) verbatim, unedited by this filing | **PASS** |
| 11 | Valuation boundary preserved | Retained artifact: `target_and_range`/`maximum_position_size` = `valuation_required` for all 27, "no numeric target, range, or maximum position size is invented, implied, or backsolved anywhere in this retained record" — independently grepped this session, zero numeric-target token found | **PASS** |
| 12 | Review ≠ adoption boundary preserved, including §K.4 | Retained artifact's "Adoption boundary" section restates the full non-authorization list and explicitly states "A future Milestone 9 completion determination, even if it closes WS-0005's own [gate]... likewise does not itself authorize adoption" | **PASS** |
| 13 | No unauthorized policy mutation | Protected-path scan (this session, `git diff`/direct read against `HEAD`): zero diff on `allocate.py`, `margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, every `intelligence/classification|reconciliation|recommendations|relationships|companies|themes/` file, every WS-0005 validator/sanitizer | **PASS** |
| 14 | PR #265 full lifecycle complete | Review → 0/0/0/1 NOTE, APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE → principal acceptance → merge (`e248b878...`) → post-merge verification → merge-commit CI `success` (`31191451730`/`92908994540`) — all independently re-fetched this session via the GitHub API | **PASS** |
| 15 | Validators/tests clean at merged head | This session independently re-ran all seven validators (all OK/clean) and the full suite (**3091 passed, 0 failed**, 1 pre-existing warning) directly against `HEAD = e248b878...`, not cited from any prior report | **PASS** |
| 16 | Register/catalog synchronization correct | `milestone-9-...` gate `status: in_progress`, `pr: 265` (independently YAML-parsed); decision catalog 88 decisions/`issues == ()` (independently rebuilt); repo-wide YAML/JSON parsing clean; `git diff --check` clean | **PASS** |

All sixteen criteria PASS.

### D. Verdict: MILESTONE 9 COMPLETE

Effective on this decision's own merge, this filing sets the `milestone-9-independent-review-and-
later-adoption` gate's `status` to `complete`, `pr:` unchanged at `265` (the review-recording
implementation PR remains the deliverable of record; this filing's own PR number is recorded
separately per §K below), in `operations/WORKSTREAMS.yaml`.

**What "Milestone 9 complete" means, precisely**: the one review `TIER-0011` authorized was
conducted by an eligible reviewer, evaluated all seven required subjects using only the closed
verdict vocabulary, was retained per §J's standard, and completed its own PR lifecycle (independent
review, principal acceptance, merge, post-merge verification) with zero unresolved BLOCKING or MAJOR
finding. **It does not mean**: any Milestone 8 finding is adopted; the LLY MINOR is fixed; any
numeric target, range, or maximum position size now exists; or — critically, per §H below — that
WS-0005 as a whole is complete.

### E. Whole-portfolio boundary (restated, not narrowed or widened)

Milestone 9 completion means only that the governed 27-equity Milestones 3-8 body has completed its
`TIER-0011`-authorized independent review lifecycle. It does **not** mean:

- the 27 canonical equities are the exhaustive investable universe;
- additional equity contenders (`WS-0014`, `CONTENDER-0001`/`CONTENDER-0002`) are complete;
- ETF work is complete;
- crypto work is complete;
- GLD/defensive-asset work is complete;
- cash/reserve doctrine is complete;
- debt-reduction doctrine is complete;
- valuation is complete;
- cross-asset synthesis (`XASSET-0001`) is complete;
- final holdings are known;
- final target weights are known;
- whole-portfolio readiness exists in any sense.

### F. Valuation boundary (restated, not narrowed or widened)

For all 27 canonical equities, `target_and_range` and `maximum_position_size` remain
`valuation_required` (Milestone 8, `TIER-0009` §G.4/§G.5). **Milestone 9 completion does not convert
that categorical abstention into numeric policy of any kind** — no target percentage, range, or
maximum position size is created, implied, or backsolved by this filing.

### G. Adoption boundary — MILESTONE 9 COMPLETE ≠ ADOPTION

**No adoption is authorized by this filing.** `TIER-0011` §K.4 states this explicitly and in advance
of this filing's own existence: "A future Milestone 9 completion determination... likewise does not
authorize adoption. Closing WS-0005's own nine-milestone roadmap... is a distinct event from adopting
any of the content that roadmap produced." This filing does not narrow, loosen, or reinterpret that
sentence — it operationalizes it exactly. Any future adoption action (editing a `portfolio_role_ref`
or `conviction.rating`; changing a `target_pct`, cluster-cap configuration, issuer-look-through entry,
or a gate's status/`next_gate` text; changing `holdings.yaml`; changing any allocator, margin, or
buy-ladder logic; or acting on any `review_warranted`/`divergence_requires_review`/
`baseline_assumption_stale` finding as if it were an instruction) requires its own separate, future,
explicit governance decision — with its own decision identifier, its own independent Lane G review
under `OPS-0007` §1, and its own explicit principal acceptance — plus its own separate, bounded
implementation PR. No such decision is pre-named, pre-scheduled, or pre-authorized here.

### H. WS-0005 top-level workstream status — remains `in_progress`, not derived automatically from Milestone 9's own closure

`OPS-0006` §4's roadmap names exactly nine milestones and ends at "independent... review before any
adoption" — it never numbered adoption itself as a tenth milestone, treating adoption as a distinct,
indefinitely deferred future action outside the numbered sequence (`TIER-0011` §K.4, restated in §G
above). That structural fact alone would already be sufficient reason not to flip `WS-0005`'s
top-level `status` to `complete` on Milestone 9's closure — "nine milestones closed" and "workstream
objective realized" are different claims, and `WS-0005`'s own `objective` field states the workstream
exists to "design" a framework whose adoption is explicitly out of scope for the roadmap this
decision closes.

**A second, independently sufficient reason was found by direct inspection during this session's
Preflight, not assumed or inherited from any task framing**: of the nine `OPS-0006` §4 milestones,
**Milestone 5 ("zero-based classification and tier-architecture review") never received its own
dedicated completion-determination filing** — unlike Milestones 3 (`PI-0037`), 4 (`REL-0006`), 6
(`TIER-0006`), 7 (`TIER-0008`), and 8 (`TIER-0010`), each closed by exactly this kind of Lane G unit.
`operations/WORKSTREAMS.yaml`'s `milestone-5-zero-based-classification-and-tier-architecture-review`
gate's own `status` field reads literally `proposed`, and its own gate text (added by `TIER-0001`'s
filing) states plainly that no subsequent filing "advance[s]... this gate's own `status: proposed`
above, which remains accurate for the milestone as a whole." `TIER-0001` (classification-question
inventory) and `TIER-0002` (candidate framework design) performed real, substantive Milestone 5
content — and Milestone 6's blind classification demonstrably consumed and validated `TIER-0002`'s
four-axis framework in practice (`classification_validator.py` enforces exactly that framework
against all 27 sealed records) — but consuming a framework downstream is not the same event as a
Lane G determination formally closing Milestone 5's own gate, and no such determination exists in
this repository as of this filing.

**This filing does not attempt to close that gap.** Doing so would require its own separate,
independently-reviewed Lane G completion-determination unit evaluating Milestone 5's own specific
deliverables (`TIER-0001`/`TIER-0002`) against their own specification — new substantive work this
session's authorization does not extend to, and exactly the kind of scope creep the task's own
prohibited-scope list (no unrelated cleanup) rules out. It is disclosed here because it is directly
dispositive of the question this section exists to answer.

**Therefore: `WS-0005`'s top-level `status` remains `in_progress` in this filing** — unchanged, for
two independently sufficient reasons: (1) `OPS-0006`'s own roadmap structure places adoption outside
the nine-milestone sequence, so closing Milestone 9 closes the sequence, not the workstream's broader
objective; and (2) Milestone 5's own gate has never been formally closed by its own dedicated
determination, an independent, live, disclosed gap in the milestone-by-milestone record that this
filing did not create and is not authorized to resolve. Either reason alone would be sufficient;
both hold simultaneously.

### I. Residual findings carried forward, not resolved by this filing

- **LLY MINOR** (`intelligence/companies/LLY.yaml` `catalysts[0].expected`): preserved exactly as
  retained by PR #265; not fixed by this filing; requires a future, separate Intelligence-maintenance
  unit using primary-source confirmation.
- **PR #265's own accepted NOTE** (the retained artifact's "Reviewing session" field lacks a
  concrete, independently-checkable session identifier for the underlying Milestone 9 review):
  preserved exactly as accepted (`issuecomment-5218771870`, "No further correction round is
  authorized or required for this NOTE"); not reopened by this filing.
- **Two Notes already recorded in the retained artifact** (a cosmetic `\d` docstring
  `DeprecationWarning`; the established `in_progress`/paired-post-merge-verification-gate
  convention): non-actionable, unchanged.
- **The Milestone 5 gate gap** (§H): newly disclosed by this filing, not previously recorded as an
  open item anywhere in `CLAUDE.md` or `operations/WORKSTREAMS.yaml`'s own narrative text; requires
  its own future, separate, independently-reviewed Lane G completion-determination filing if and
  when the principal chooses to close it — not authorized, scheduled, or begun here.

None of the above is corrected, resolved, or silently treated as closed by this filing.

### J. Explicit non-authorization

This filing does not, under any circumstance:

- adopt, propose adopting, or take any step toward adopting any Milestone 8 finding (§G);
- edit `intelligence/companies/LLY.yaml` or any other Company/Theme/relationship/classification/
  reconciliation/recommendation record;
- introduce any valuation methodology, numeric target, range, maximum position size, score, or rank;
- create any whole-portfolio conclusion (§E);
- conduct or extend any Milestone 9 review content — the review is already complete and retained;
  this filing evaluates its completion, it does not re-review its substance;
- authorize any tier/target/holdings/gate/cap/cluster/allocator/margin/ladder/chart/order/trade
  change of any kind;
- close the Milestone 5 gate identified in §H, or authorize any future work toward closing it;
- authorize, imply, or schedule any `WS-0014`/`XASSET-0001` cross-asset, ETF, crypto, GLD, cash, or
  debt-reduction work;
- perform any unrelated cleanup beyond the register/catalog synchronization §K requires.

### K. Register and catalog synchronization performed by this filing

- `operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate:
  `status: in_progress` → `status: complete`; `pr:` remains `265` (the review-recording
  implementation's own PR; this filing's PR number is recorded via `WS-0005`'s top-level
  `active_pr` field per `OPS-0001`'s convention — set to `null` in this filing's first commit, then
  updated by a bounded follow-up commit once the PR exists).
- `WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
  `completion_criteria` fields are **unchanged** — per §H, this filing does not close the workstream.
- `WS-0005`'s `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
  self-reference fields are updated to this filing's own live state.
- One short paragraph is appended to `WS-0005`'s `blocker` and `next_action` fields recording this
  filing's own verdict and the §H finding — not rewriting any prior entry.
- `governance/decisions.yaml`: one new index row for `TIER-0012`.
- `CLAUDE.md`: one concise Decisions Log entry pointing to this filing (no restatement of §§A-L).
- `test_portfolio_hq_dashboard_decisions.py`: the two hardcoded decision-count assertions, 88 → 89.

No production code, no `intelligence/classification/`, `intelligence/reconciliation/`,
`intelligence/recommendations/`, `intelligence/relationships/`, `intelligence/companies/`, or
`intelligence/themes/` file, no `governance/audits/` artifact, no other workstream, and no existing
Company/Theme/relationship/classification/reconciliation/recommendation record is touched.

### L. Preserved next roadmap item — not implemented by this filing

The next dedicated governance unit after this filing's own lifecycle completes — whether that is a
future Milestone 5 completion-determination filing (§H) or the first `WS-0014`/`XASSET-0001`
cross-asset unit — must preserve, in the appropriate `WS-0014`/`XASSET-0001` governance architecture,
the following seven-step whole-portfolio sequence (restated here for continuity, not implemented):

1. define governed asset-appropriate frameworks for equities, ETFs, crypto, GLD/defensive assets,
   cash/reserve, and debt reduction;
2. perform asset-appropriate valuation/economic assessment;
3. conduct cross-asset opportunity-cost and overlap synthesis;
4. produce a preliminary portfolio;
5. ingest and interpret governed chart evidence for applicable market-priced instruments as a
   deployment/timing and technical-risk layer, never as a substitute for fundamental/economic
   selection;
6. perform final synthesis;
7. determine holdings, target weights, deployment sequencing, and execution discipline.

This filing does not implement, begin, schedule, or authorize any step of that sequence.

## Rationale

`OPS-0006` §16.1 (echoed by `OPS-0001`) sets a milestone-completion discipline this repository has
applied consistently across Milestones 3, 4, 6, 7, and 8: a milestone reaches `complete` only after
independent verification of its own authorized deliverables, PR lifecycle, and register/catalog
synchronization — never from discussion, a commit, a push, or an open PR alone. Milestone 9 is the
last-numbered milestone in that same roadmap, and `TIER-0011` fully specified what completing it
requires before any review content existed. This filing applies that same discipline: it re-derives
the sixteen applicable criteria directly from `TIER-0011`'s own text rather than inventing a new
standard, and independently re-verifies each against live repository and GitHub state rather than
trusting any prior filing's self-report — consistent with this repository's own standing guardrail
that claims about repository state, even from within the same governance chain, must be verified
before being relied on.

The more consequential judgment this filing makes is §H: refusing to treat "Milestone 9 complete"
as synonymous with "`WS-0005` complete." `TIER-0011` itself anticipated and foreclosed one path to
that conflation (§K.4 — adoption stays outside the roadmap). This filing adds a second, independently
discovered reason — Milestone 5's own gate was never closed by a dedicated determination — found by
direct inspection of `operations/WORKSTREAMS.yaml`'s actual YAML state, not by assuming the
nine-milestone sequence was uniformly closed simply because eight of nine gates currently read
`complete`. Reporting a workstream-wide completion the live register does not actually support would
be exactly the kind of silent, non-evidence-based completion claim `OPS-0006` §16.4 was written to
forbid ("no completion claim may be inferred... from stale wording").

## Alternatives Considered

- **Declare `WS-0005` complete alongside Milestone 9.** Rejected. `OPS-0006`'s own roadmap text
  places adoption outside the nine-milestone sequence regardless of Milestone 9's own state, and —
  independently — Milestone 5's gate remains open. Declaring the workstream complete would
  contradict live, directly-inspectable repository state on at least one, and in fact two, grounds.
- **Silently note the Milestone 5 gap without disclosing it as load-bearing.** Rejected. The gap is
  the actual reason `WS-0005` cannot close on this filing's own terms; treating it as a minor aside
  rather than a stated, evidence-based blocker would understate exactly the kind of finding this
  repository's own precedent (e.g. `PI-0031` §K's own criteria 5-7, left explicitly unverified by
  `PI-0035` rather than silently assumed) requires disclosing plainly.
- **Attempt to close the Milestone 5 gate in this same filing, since the substantive work
  (`TIER-0001`/`TIER-0002`) already exists.** Rejected. This task's own authorization is scoped to
  Milestone 9's completion determination; closing Milestone 5 is new substantive work requiring its
  own independent Lane G review of Milestone 5's own specification and deliverables — exactly the
  unrelated-cleanup and scope-creep this filing's own prohibited-scope list rules out.
- **Treat the reviewing session's undisclosed identifier (the accepted NOTE) as blocking Milestone 9
  completion.** Rejected. `OPS-0007` §1's severity scheme reserves BLOCKING/MAJOR treatment for
  defects that would themselves block a decision from being considered; PR #265's own independent
  review already classified this as a disclosed, non-blocking limitation of the retention path, and
  the principal explicitly accepted it as such without requiring a correction round. Re-litigating an
  already-accepted, non-blocking finding in a downstream completion-determination filing would exceed
  this filing's own scope and would not itself be new evidence.

## Consequences

- `operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate reaches
  `status: complete` — the last milestone in `OPS-0006` §4's nine-milestone roadmap is formally
  closed.
- `WS-0005`'s top-level `status` remains `in_progress`, for the two independently sufficient reasons
  in §H — a future filing may close Milestone 5 and/or a future governance decision may authorize
  adoption, but neither is authorized, scheduled, or implied by this filing.
- The LLY MINOR finding, the PR #265 NOTE, and the two artifact-level Notes remain open, disclosed,
  and unresolved.
- No tier, target, role, gate, holdings, cap, cluster, allocator, margin, ladder, chart, order, or
  trade value changes as a result of this filing.
- The seven-step whole-portfolio sequencing doctrine (§L) remains a preserved, undisclosed-to-code
  design note for the next `WS-0014`/`XASSET-0001` governance unit to carry forward — not itself
  advanced by this filing.
