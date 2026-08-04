---
decision_id: REL-0006
date: 2026-08-04
status: Proposed
category: relationship_mapping_governance
related_decisions: [REL-0001, REL-0002, REL-0003, REL-0004, REL-0005, GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0031, PI-0033, PI-0035, PI-0036, PI-0037, LADDER-0001, CHART-0001, CHART-0002, OPS-0016]
supporting_artifact: null
---

## Context

### Authority for this unit

The human repository principal authorized exactly one bounded Lane G (`OPS-0009` §1) unit to
determine, on live repository and GitHub evidence independently re-verified this session, whether
WS-0005 Milestone 4 ("Portfolio Relationship Mapping") satisfies the eight-criterion completion
standard `REL-0004` defined. This authorization explicitly does not predetermine the outcome — the
conclusion may be COMPLETE, INCOMPLETE, or ABSTAIN/INSUFFICIENT EVIDENCE. This is a
completion-**determination** only: it performs no new relationship research, creates no
`intelligence/relationships/` record, computes no price correlation, edits no Company or Theme
Intelligence record, reopens no gate, and does not itself begin Milestone 5 regardless of its own
verdict.

### Preflight (independently verified this session, not assumed from the authorizing brief)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/ws0005-m4-completion-s91zpx`, working tree clean at
  session start.
- **`origin/main` fetched.** `git rev-parse origin/main` returned
  `7562c49fe0a2a52db42c7f40e5609c452d78af0e`, identical to this branch's own starting head — no
  drift, no rebase required.
- **PR #243 (`REL-0005`) independently re-confirmed merged** via the GitHub API: `state: MERGED`,
  `merged: true`, head `6612c62a59302d80a7c3e2449ccb2ab0512e0d9e`, base `main`@`29761b6a...`, merge
  commit `7562c49fe0a2a52db42c7f40e5609c452d78af0e` (matches `origin/main`'s tip above exactly).
  Independent delta review `4857969070` (verdict **DELTA APPROVED — APPROVED FOR PRINCIPAL
  EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 2 non-blocking NOTEs, both process/
  provenance disclosures) independently re-read in full. Principal acceptance comment
  `issuecomment-5184081674` independently re-read, naming exact head `6612c62a...` and that review.
  Post-merge verification comment `issuecomment-5184148213` independently re-read: merge-tree
  identity confirmed byte-identical to the accepted head's tree, exact 14-file scope confirmed,
  protected paths confirmed untouched, full validator/test suite confirmed clean, merge-commit CI
  confirmed `completed`/`success`.
- **Zero open pull requests** confirmed via `mcp__github__list_pull_requests` (`state: open`) —
  empty result. No active mutation lane exists.
- **`REL-0006` independently confirmed the next unused identifier**: `ls governance/decisions/*.md`
  (excluding `README.md`) returns exactly 70 files; `governance/decisions.yaml` contains exactly 70
  `decision_id` rows; both reconciled 1:1 by direct comparison. The highest filed `REL-####` is
  `REL-0005`. `REL-0006` does not exist in either the directory or the index prior to this filing.
- **Governing decisions read in full this session, not relied on from memory or summary**:
  `REL-0001` (schema/taxonomy/evidence standard/inventory authorization), `REL-0002` (`CEG_MSFT`),
  `REL-0003` (eight-pair batch), `REL-0004` (the eight-criterion completion standard this filing
  evaluates), `REL-0005` (four-pair TSM batch), `OPS-0007` (capability-based review standard),
  `OPS-0008` (Research Wave Protocol v1), `OPS-0009` (Lean Delivery and Review Lifecycle v1), and the
  retained supporting artifact `governance/audits/WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md`
  (all 261 lines).
- **Live validators and full suite independently re-run this session**, against the exact base SHA
  above, before any edit:
  - `relationship_validator.py` (direct run) — **`OK (13 record(s))`**.
  - `intelligence_validator.validate_directory('intelligence/companies')` — **47/47 valid**.
  - `freshness_validator.py` — **OK**.
  - `portfolio_hq.dashboard.decisions.build_catalog('.')` — **70 decisions, 12 legacy, `issues == ()`**.
  - `python3 -m pytest -q` — **2581 passed, 0 failed** (82.3s) — matching PR #243's own post-merge
    verification result exactly (this session's checkout directory is itself named `Portfolio-HQ`,
    so `test_real_repository_model_builds`'s checkout-directory-basename dependency resolves to a
    pass here, the same disclosed, pre-existing, environment-only artifact every prior REL-#### PR
    has independently reconciled — not a regression).
  - `git diff --check` — clean. Working tree clean throughout, before any edit.
- **Canonical governed roster independently re-derived from live `targets.yaml`**: exactly 27
  `destination:` rows outside `{BTC, ETH, SOL, CASH, RESERVE, GLD, SPY, VEA, VWO}`. **`gates.yaml`
  independently re-parsed**: exactly 6 gated tickers (SNPS, ICE, SPGI, WM, RKLB, TSLA), each
  `allow_add: false`, each carrying an unsatisfied `next_gate` condition — unchanged from `PI-0037`'s
  own last independent count. 27 = 21 non-gated + 6 gated. **Zero commits touch
  `intelligence/companies/`, `intelligence/themes/`, `targets.yaml`, `gates.yaml`, or
  `issuer_lookthrough.yaml` between the inventory audit's own authoring commit
  (`52bb3c6`) and this filing's own base (`7562c49f`)** — independently confirmed via
  `git log 52bb3c6..HEAD --oneline -- intelligence/companies/ intelligence/themes/ targets.yaml
  gates.yaml issuer_lookthrough.yaml`, which returns no results. The governing inventory's own
  evidence base has zero drift as of this filing's own live-state re-verification.
- **`intelligence/relationships/` independently confirmed to hold exactly 13 `.yaml`/`.md` pairs**:
  `AMZN_GOOGL`, `AMZN_MSFT`, `ASML_TSM`, `AVGO_GOOGL`, `AVGO_META`, `AVGO_TSM`, `CEG_MSFT`,
  `ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`, `GOOGL_MSFT`, `KLAC_TSM`, `NVDA_TSM` — `CEG_MSFT` from
  `REL-0002` (PR #240), eight from `REL-0003` (PR #241), four from `REL-0005` (PR #243).
- **Isolated worktree/branch confirmed clean** before this unit's own first edit; no other mutation
  lane active on this branch or elsewhere in the repository.

No condition in this unit's own stop list was triggered: `main` had not advanced past the expected
base; no overlapping mutation lane exists; the next `REL-####` identifier (`REL-0006`) matched
expectation; no gate has reopened; the canonical roster count (27) matched expectation; live evidence
did not contradict the retained inventory artifact; a clean isolated workspace was established
without incident.

## Decision

**`REL-0006` determines, on live repository and GitHub evidence independently re-verified this
session, that WS-0005 Milestone 4 satisfies all eight of `REL-0004` §C's completion criteria as of
this filing's own live-state re-verification, and accordingly sets the
`milestone-4-portfolio-relationship-mapping` gate's `status` to `complete` in
`operations/WORKSTREAMS.yaml`.** This decision authorizes no research, no relationship record, no
price-correlation study, no Company or Theme Intelligence edit, no gate reopening, no
tier/target/role/cluster/cap/holdings/margin/allocator change, and — repeatedly, explicitly — **does
not authorize, begin, schedule, or imply Milestone 5** (zero-based classification and tier-
architecture review) or any later WS-0005 milestone, or "Eureka" (`OPS-0016`). It creates no
investment, allocation, or trading authority of any kind.

### A. Criterion-by-criterion determination

Each criterion below is evaluated fresh against live repository and GitHub state, per `REL-0004` §C's
own instruction not to infer from any prior filing's summary.

**Criterion 1 — Full-roster inventory-pass currency.**
*Text:* every non-gated, non-deferred canonical equity name has been evaluated at least once by a
systematic full-roster relationship-evidence inventory, and that inventory's own coverage is
confirmed current as of the determination.
**PASS.** The retained `WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` artifact
systematically evaluated all 27 canonical names (§2 of that artifact) against `REL-0001` §C's twelve
primitive types. This filing independently re-confirmed, via direct `git log` inspection (§ Preflight
above), that zero commits have touched `intelligence/companies/`, `intelligence/themes/`,
`targets.yaml`, `gates.yaml`, or `issuer_lookthrough.yaml` since that artifact's own authoring commit
— its coverage is unchanged since `2026-08-04`, not merely re-asserted. No reconciliation delta is
required. **Fully satisfied now.**

**Criterion 2 — Candidate-set exhaustion.**
*Text:* every relationship candidate the governing inventory identified as evidence-ready in a
recommendation table comparable to its own §9 has either a filed, validator-passing record, or an
explicit, reasoned abstention.
**PASS.** The inventory's §9 table named exactly four candidate groupings (nine pairwise records):
`CEG_MSFT`; `AVGO_GOOGL`/`AVGO_META`; `GNRC_GEV`/`GNRC_ETN`/`GNRC_PWR` (filed as `GEV_GNRC`/
`ETN_GNRC`/`GNRC_PWR` per `REL-0001` §B's alphabetical rule); `MSFT_GOOGL`/`AMZN_GOOGL`/`AMZN_MSFT`
(filed as `GOOGL_MSFT`/`AMZN_GOOGL`/`AMZN_MSFT`). All nine are filed, merged, and
`relationship_validator.py`-passing (independently re-run this session: `OK (13 record(s))`, which
includes all nine). No further §9-comparable recommendation table has been produced since — only one
`governance/audits/` artifact of this kind exists in the repository, independently confirmed by
directory listing. **Fully satisfied now.**

**Criterion 3 — Explicit disposition for every canonical name.**
*Text:* every canonical, non-gated, non-deferred equity name is either covered by a filed
relationship record, or explicitly determined, in a retained artifact, to carry no canonical-pair
relationship evidence meeting `REL-0001` §E's materiality bar.
**PASS.** Cross-referencing the 21 non-gated canonical names against the 13 filed records' own
`subject`/`object` tickers: **14 of 21** appear in at least one filed record (AMZN, ASML, AVGO, CEG,
ETN, GEV, GNRC, GOOGL, KLAC, META, MSFT, NVDA, PWR, TSM).
The remaining **7 of 21** (COST, ISRG, LLY, PANW, RTX, TMO, V) carry an explicit,
disclosed, no-canonical-pair-evidence disposition in the inventory's §6 table and §7 (RTX/GNRC
explicit mutual disclaimer) — a valid, complete disposition under `REL-0004` §C.3's own text ("a name
with zero evidenced canonical-pair relationships is a valid, complete disposition... provided the
absence is itself disclosed"). **One factual correction to the governing inventory's own §6 table,
disclosed here and not silently inherited**: §6 listed **GNRC** as carrying no canonical-pair
evidence — this is now stale, superseded by `REL-0003`'s later filing of three GNRC-anchored
`complement` records (`ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`), exactly as `REL-0004` §B itself already
flagged ("GNRC's own entry is now stale, since `REL-0003` filed three GNRC-anchored `complement`
records the original audit's §6 table predates"). This is a positive drift — GNRC moved from
"no evidence" to "covered" — and does not create a gap; it is recorded here as the reconciliation
`REL-0004` §B anticipated, not as a defect in the original artifact (which was accurate as of its own
`2026-08-04` authoring date, before `REL-0003` existed). The governing artifact's own file is not
edited, per `governance/decisions/README.md`'s never-silently-rewrite convention for retained
artifacts. **Fully satisfied now**, with the correction above disclosed rather than silently
inherited.

**Criterion 4 — Per-record PROVISIONAL status.**
*Text:* every `intelligence/relationships/` record existing at determination time individually
satisfies an `OPS-0007` §3-equivalent standard, applied per record: eligible independent review at
its exact implementation head, any required bounded correction and exact-head re-review, explicit
principal acceptance at that exact head, merge to `main`, and post-merge verification.
**PASS**, independently re-verified per originating PR, not inferred from any batch's own narrative:
- **`CEG_MSFT`** (PR #240): independent review `4856012228` (APPROVED FOR PRINCIPAL EXACT-HEAD
  ACCEPTANCE, 0 BLOCKING/MAJOR/MINOR, 2 NOTEs) → principal acceptance `issuecomment-5180959007`
  (naming exact head `8403a4f8...`) → merged → post-merge facts independently re-verified by
  `REL-0003`'s own preflight and re-confirmed again by this session (`relationship_validator.py`
  currently reports this record present and valid).
- **8 `REL-0003` records** (`AVGO_GOOGL`, `AVGO_META`, `ETN_GNRC`, `GEV_GNRC`, `GNRC_PWR`,
  `GOOGL_MSFT`, `AMZN_MSFT`, `AMZN_GOOGL`, PR #241): independent review `4856585060` (CHANGES
  REQUIRED — one MINOR, competitor-triad sourcing disclosure) → bounded correction commit `fe81561`
  → exact-head delta review `4856745242` (APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0
  BLOCKING/MAJOR/MINOR remaining) → principal acceptance `issuecomment-5181876227` (naming exact head
  `fe815617...`) → merged → post-merge facts independently re-verified by `REL-0004`'s own preflight
  and re-confirmed again by this session.
- **4 `REL-0005` records** (`ASML_TSM`, `AVGO_TSM`, `KLAC_TSM`, `NVDA_TSM`, PR #243): independent
  delta review `4857969070` (DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0
  BLOCKING/MAJOR/MINOR, 2 NOTEs) → principal acceptance `issuecomment-5184081674` (naming exact head
  `6612c62a...`) → merged (`7562c49f...`) → post-merge verification `issuecomment-5184148213`
  (independently re-read this session, confirming merge-tree identity, exact scope, protected-path
  isolation, and clean validators/tests at the merge commit).

All three PR review/comment threads were independently re-read in full by this session via the
GitHub API (not cited from any prior filing's own summary), and this session's own fresh
`relationship_validator.py`/`pytest` run (§ Preflight above) independently re-confirms all 13 records
currently parse, validate, and pass their tests at the present `origin/main` head. **All 13 of 13
currently-existing `intelligence/relationships/` records are independently confirmed PROVISIONAL, 0
held back. Fully satisfied now.**

**Criterion 5 — No unresolved MATERIAL finding.**
*Text:* no open BLOCKING or MAJOR finding remains against any filed record's evidence, sourcing,
classification, or taxonomy compliance, or against the governing inventory's own methodology.
**PASS.** Independently re-tallied from the three review threads read in full above: PR #240 — 0
BLOCKING, 0 MAJOR, 0 MINOR (2 NOTEs). PR #241 — 0 BLOCKING, 0 MAJOR at either review pass; 1 MINOR at
the first pass (competitor-triad sourcing disclosure), independently confirmed resolved by the
bounded correction and re-verified 0 remaining at the delta review. PR #243 — 0 BLOCKING, 0 MAJOR, 0
MINOR (2 NOTEs) at its own delta review. **Zero open BLOCKING or MAJOR findings against any of the 13
records or against the governing inventory's methodology, independently confirmed. Fully satisfied
now.**

**Criterion 6 — New-research gaps disclosed, not required.**
*Text:* every relationship gap the governing inventory identified as requiring genuinely new external
research is explicitly disclosed, together with an explicit statement that it does not block
completion; new external relationship research is not itself a prerequisite of this standard.
**PASS**, with three items independently re-confirmed and disclosed, none blocking:
1. **§5.1 — Hyperscaler-to-semis capital/customer chain** (MSFT/GOOGL/AMZN/META ↔ NVDA/AVGO). This
   session independently re-grepped `intelligence/companies/MSFT.{yaml,md}`,
   `GOOGL.{yaml,md}`, `AMZN.{yaml,md}` for `NVDA`/`AVGO` references and confirmed each record's own
   text explicitly states it does **not** confirm or quantify a specific named supplier relationship
   with those semis-cluster names (e.g. `AMZN.md`: "No specific named supplier relationship between
   Amazon and NVDA, TSM, AVGO, AMD, or MRVL was confirmed or quantified"; `MSFT.md`/`GOOGL.md` carry
   materially identical disclaimers). **Remains a disclosed, unresolved evidence gap on both sides**,
   independently reconfirmed, not merely cited from `REL-0004`'s or `REL-0005`'s own text. Per
   `REL-0004` §C.6 and Milestone 3's own `DHR`/`SYK`/`EQIX`/`UNH` precedent, this gap does not block
   completion.
2. **Newly disclosed by this filing — two evidence-ready-but-never-recommended items from the
   inventory's own §4 tables, distinct from the §9 recommendation table Criterion 2 governs.** The
   inventory's §4.2 records a `GEV`/`ETN`/`PWR` shared `capital_spending_dependency` on the same
   hyperscaler/utility capex class ("observed for the mechanism's existence... inferred for the
   shared-class framing"), and its §4.4 records an `MSFT`/`AMZN` `regulatory_or_reimbursement_
   dependency` (both named in the same EU DMA cloud-gatekeeper proceeding, "observed"). Neither was
   ever placed in the §9 recommendation table (§9 covered only the `complement`/`customer_dependency`/
   `competitor` angles for these same names, not these two), and neither is required by Criterion 2's
   text, which scopes strictly to "recommended in an advisory table comparable to the existing audit's
   §9." **Disclosed here as a residual, non-blocking, already-evidenced (not requiring new external
   research) candidate a future optional batch could act on — not evaluated, filed, or required by
   this determination.**
3. **New external relationship research is not itself a prerequisite of this standard**, per
   `REL-0004` §C.6's own text — no research-wave protocol for relationship content exists, and this
   filing does not create one. **Fully satisfied now**, all three items disclosed, none blocking.

**Criterion 7 — Register and validator synchronization.**
*Text:* the `intelligence/relationships/` directory, `relationship_validator.py`'s clean pass,
`governance/decisions.yaml`, and `operations/WORKSTREAMS.yaml`'s `WS-0005` entry are mutually
consistent and current as of the determination filing's own live-state re-verification.
**PASS, as of this filing's own synchronization (performed in §B below).** At the start of this
session, `WS-0005`'s `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
self-reference fields read `claude/rel0004-milestone4-semis-relationship-batch` / `243` /
`29761b6a...` (the pre-`REL-0005`-merge base SHA) / `"2026-08-04"` — stale on exactly the fact that
`REL-0005`'s own PR has since merged and `origin/main` has advanced past it, the identical mechanical
staleness pattern every prior WS-0005 filing in this log has recorded and corrected after its own
predecessor's merge. This filing corrects exactly that fact (§B) and performs no other
`operations/WORKSTREAMS.yaml` change beyond the additive gate entries this filing itself requires.
The `intelligence/relationships/` directory (13 records), `relationship_validator.py` (`OK (13
record(s))`), and `governance/decisions.yaml` (70 rows, 1:1 with 70 files, independently reconciled
this session) are already mutually consistent and current, with no other correction required.
**Fully satisfied as of this filing's own edits.**

**Criterion 8 — Independent completion-determination filing.**
*Text:* a dedicated, later, separate Lane G filing freshly re-verifies Criteria 1-7 together against
live state, states an explicit verdict, and is itself subject to the full independent-review/
correction/re-review/principal-acceptance/merge/post-merge-verification lifecycle before the gate's
`status` may be set to `complete`.
**This filing is that filing.** It performs no new relationship research, creates no relationship
record, and computes no correlation. §A above freshly re-verifies Criteria 1 through 7 together
against live repository and GitHub state, independently re-derived in this session rather than
inferred from `REL-0004`'s, `REL-0005`'s, or any prior filing's own summary. This filing's own
governance PR must remain in draft, receive its own independent exact-head review under `OPS-0007`
§1, complete any required bounded correction and re-review, and receive explicit principal acceptance
before merge — per §D below. **The `milestone-4-portfolio-relationship-mapping` gate's `status:
complete` transition below is not effective until this filing's own governance PR merges to `main`.**

### B. Verdict

**MILESTONE 4 COMPLETE.**

All eight of `REL-0004` §C's completion criteria are satisfied as of this filing's own live-state
re-verification (`origin/main` at `7562c49fe0a2a52db42c7f40e5609c452d78af0e`). No criterion fails. No
corrective unit is required to reach this verdict. Two residual, disclosed, non-blocking items are
recorded above (Criterion 6, item 2) as discovered work for a future, separately authorized, optional
batch — neither is required by any of the eight criteria as written, and neither is acted on by this
filing.

This filing accordingly sets the `milestone-4-portfolio-relationship-mapping` gate's `status` to
`complete` in `operations/WORKSTREAMS.yaml` (§C below), **effective only on this decision's own
merge to `main`**, per §D's required independent-review and principal-acceptance gate.

### C. Register synchronization performed by this filing

This filing performs the minimum `operations/WORKSTREAMS.yaml` synchronization Criterion 7 requires:
one additive gate-status entry recording this determination and setting
`milestone-4-portfolio-relationship-mapping`'s `status` to `complete`; and an update to `WS-0005`'s
own `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields
(`active_pr` remains `null` until this filing's own PR number exists, per `OPS-0001`'s established
convention — a bounded follow-up commit sets it once the PR is opened). No other `WS-0005` field
(`status`, `priority`, `authorized_scope`, `prohibited_scope`, `completion_criteria`, or any other
milestone's own gate) is touched. `WS-0005`'s top-level `status` remains `in_progress` — Milestone 4
reaching `complete` does not itself complete the workstream, since Milestones 5-9 remain unauthorized
roadmap items per `OPS-0006` §5's own per-milestone authorization gate, unaffected by this filing.

### D. Required independent review, principal-acceptance gate, and stopping condition

- **This governance PR must remain in draft state** and must not be marked ready for review or
  merged by this session.
- **An eligible independent review is required**, anchored to this PR's exact final head, per
  `OPS-0007` §1's twelve-point capability-based standard — no self-review by the authoring session.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready, per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Explicit principal acceptance is required before merge**, at the exact head being merged.
- **This decision does not mark itself, or authorize marking itself, ready for merge.** It becomes
  effective — including the Milestone 4 `status: complete` transition in §C — only on this governance
  PR's own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized
  scope ends at opening this draft PR (and one bounded follow-up commit setting `WS-0005`'s
  `active_pr` self-reference to this PR's own number once it exists) and reporting its exact head. No
  independent review, no correction pass, no re-review, no merge, and no post-merge verification is
  performed by this session — each is a separate future step requiring a separate actor. This session
  does not review its own work, mark it ready, merge it, or post principal acceptance.

## E. What this decision does not do

- **Does not authorize, begin, schedule, or imply Milestone 5** (zero-based classification and
  tier-architecture review) or any later WS-0005 milestone. `OPS-0006` §5's own per-milestone
  authorization gate remains in force and unaddressed by this filing.
- **Does not perform, authorize, or imply any new relationship research**, external or otherwise.
- **Does not create any `intelligence/relationships/*.yaml` or `.md` record.**
- **Does not compute, authorize, or substitute for any price-correlation study.** `REL-0001` §G's
  structural-versus-measured separation is preserved unmodified.
- **Does not edit any existing `intelligence/relationships/`, Company Intelligence, or Theme
  Intelligence record's substance.**
- **Does not reopen any `gates.yaml` gate** — all 6 entries, their `status`, `authority`,
  `allow_add`, and `next_gate` text, are unchanged.
- **Does not change any tier, target, gate, cluster, cap, margin, holding, allocator, chart,
  brokerage, or order behavior.** `targets.yaml`, `holdings.yaml`, `gates.yaml`, `allocate.py`,
  `levels.py`, and `margin_state.py` are untouched.
- **Does not run or log an allocation check.**
- **Does not act on either residual item disclosed under Criterion 6** (the unfiled
  `GEV`/`ETN`/`PWR` capex-dependency or `MSFT`/`AMZN` regulatory-dependency evidence) — both remain
  unauthorized, undecided, optional future work.
- **Does not correct, edit, or silently rewrite** the retained
  `WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` artifact's own §6 table — Criterion 3's
  GNRC-staleness reconciliation is recorded in this filing's own text only (§A, Criterion 3), per this
  repository's never-silently-rewrite convention for retained artifacts.
- **Does not mark this filing's own governance PR ready, request or begin independent review of it,
  post principal acceptance of it, or merge it** — this decision's own effectiveness is contingent on
  its own future, separate independent review and principal acceptance, exactly as every prior
  WS-0005 governance filing in this log has required of itself.
- **Creates no research, policy, allocation, or implementation authority of any kind beyond the
  single factual determination stated in §B.**

## Rationale

**Why a completion-determination decision is warranted now.** `REL-0004` §A stated explicitly that
nine filed records, by themselves, satisfy none of §C's eight criteria in full — each requires fresh,
independent re-verification, not batch-level citation. This filing performs exactly that fresh
re-verification, now that `REL-0005`'s four additional records have also merged and completed their
own full review/acceptance/post-merge-verification lifecycle, closing the last gap `REL-0004`'s own
Preflight left open (per-record PROVISIONAL status for the four `REL-0005` records, which post-dated
`REL-0004`'s own filing).

**Why Criterion 3's GNRC correction is disclosed rather than silently inherited or silently
corrected.** `REL-0004` §B already flagged that the governing inventory's own §6 table would go stale
the moment `REL-0003`'s GNRC-anchored records merged, and explicitly declined to correct the retained
artifact itself, consistent with `governance/decisions/README.md`'s convention against silently
rewriting a retained artifact's original text. This filing follows that same discipline: the
correction lives in this filing's own text, not as an edit to the original audit.

**Why the two Criterion-6 residual items are disclosed but not converted into a blocking finding.**
Both (`GEV`/`ETN`/`PWR` capex dependency; `MSFT`/`AMZN` regulatory dependency) are genuinely
`REL-0001`-taxonomy-eligible evidence already present in the governing inventory's own §4 tables —
but neither was ever elevated to a recommendation in a §9-comparable table, and `REL-0004`'s own
Criterion 2 text scopes exhaustion strictly to recommended candidates, not to every raw evidence
entry the inventory happens to classify. Treating every §4 entry as an implicit completion
requirement would silently expand Criterion 2 beyond its own written text — exactly the "record count
alone" or "exhaustive pairwise mapping" failure modes `REL-0004`'s own Rationale explicitly rejected.
Disclosure without a requirement to act matches this repository's own established convention
(`PI-0037`'s own "Discovered work" section; `OPS-0004`'s Finding FA-1) for exactly this situation.

**Why this filing relies on, but independently re-reads, the three prior review threads rather than
re-running each review from scratch.** `OPS-0009` §4's evidence-identity discipline permits reuse of
an already-independently-validated conclusion without repeating its underlying derivation, provided
the conclusion's own retained evidence is re-confirmed current. This filing independently re-read
all three review threads (`4856012228`, `4856585060`+`4856745242`, `4857969070`) and all three
principal-acceptance comments in full via the GitHub API this session, and independently re-ran
`relationship_validator.py` and the full `pytest` suite against the current merged state, rather than
accepting any prior filing's summary of those facts on trust.

## Alternatives Considered

- **Declare Milestone 4 complete based on `REL-0005`'s own governance text alone, without
  independently re-reading the three PRs' review/acceptance/merge history.** Rejected — exactly the
  "assume batch-level language proves per-record lifecycle compliance" failure mode `REL-0004`
  Criterion 4 explicitly warns against and `PI-0037`'s own Milestone 3 precedent already rejected for
  GNRC/RTX.
- **Treat the `GEV`/`ETN`/`PWR` and `MSFT`/`AMZN` §4-table entries as blocking, requiring a further
  relationship-content batch before completion.** Rejected — `REL-0004` Criterion 2's own text scopes
  candidate-set exhaustion strictly to §9-comparable recommendation tables, not to every raw §4
  evidence entry; forcing coverage of every entry the inventory happens to classify would exceed the
  written standard and reintroduce the "exhaustive pairwise mapping" failure mode `REL-0004`'s
  Rationale explicitly rejected. Disclosed as discovered work instead (§A, Criterion 6, item 2).
- **Correct the governing inventory artifact's own §6 table in place**, since GNRC's entry is now
  factually stale. Rejected — `governance/decisions/README.md`'s convention treats a retained
  artifact's original text as a historical record, corrected via disclosure in a later filing, not by
  silent in-place rewriting; this filing follows that same discipline (§A, Criterion 3).
- **Defer this determination further, pending a new relationship-content batch closing the §5.1
  hyperscaler-to-semis gap.** Rejected — `REL-0004` Criterion 6 explicitly states new external
  relationship research is not a prerequisite of the standard, mirroring Milestone 3's own
  `DHR`/`SYK`/`EQIX`/`UNH` precedent, where disclosed deferral did not block `PI-0037`'s own
  `MILESTONE 3 COMPLETE` verdict.
- **Begin Milestone 5 in the same filing, since Milestone 4 is now determined complete.** Rejected —
  explicitly outside this unit's authorization; `OPS-0006` §5's separate-authorization gate for each
  milestone is unaffected by this filing under any circumstance.

## Consequences

**Authorized, effective only on this decision's merge:** the factual determination that WS-0005
Milestone 4 satisfies all eight `REL-0004` §C completion criteria as of this filing's own live-state
verification, and the corresponding `status: complete` update to the
`milestone-4-portfolio-relationship-mapping` gate in `operations/WORKSTREAMS.yaml`, together with the
minimum `WS-0005` self-reference synchronization in §C.

**Unchanged by this decision:** every existing `intelligence/relationships/` record, all 13 of them,
byte-for-byte; every existing Company/Theme Intelligence record, all 47 of them; every existing
comparison artifact; `issuer_lookthrough.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`allocate.py`, `levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s top-level `status`
(`in_progress`), `priority` (`primary`), `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; Milestone 3's own `status: complete` (`PI-0037`, unedited, not reopened);
`REL-0001`'s, `REL-0002`'s, `REL-0003`'s, `REL-0004`'s, and `REL-0005`'s own accepted/proposed text
and scope, in full, unedited; the retained
`WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` artifact, unedited.

**Explicitly not authorized by this decision, stated repeatedly for clarity:** Milestone 5 or any
later WS-0005 milestone; any relationship, Company, or Theme Intelligence research of any kind; any
new `intelligence/relationships/` record; any price-correlation study; any gate reopening; any
tier/target/role/cluster/cap/holdings/margin/allocator/order-behavior change; any allocation check;
action on either residual item disclosed under Criterion 6. **This decision creates no research,
policy, allocation, or implementation authority beyond the single factual determination in §B.**

This decision becomes effective only when its implementing pull request merges to `main`.

**No current portfolio policy or allocator behavior changes as a result of this decision, before or
after its merge.** `allocate.py`'s buy/trim/gap logic, every gate parameter, every cap, every target
weight, and every margin parameter remain exactly as `targets.yaml`/`gates.yaml`/`holdings.yaml`
currently state them, unaffected by this filing under any circumstance.
