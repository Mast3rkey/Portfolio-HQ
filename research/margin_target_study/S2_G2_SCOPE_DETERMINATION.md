# S2/G2 Scope Determination — MARGIN-0005

**Status:** Read-only determination. Authorizes nothing by itself — it recommends a scope
for a later, separate final S2 implementation PR, or an honest stop, or a charter
amendment. It does not open, authorize, or begin that PR; it runs no simulation, executes
no registered study, consumes zero of the 300-run trial ceiling, and creates neither
`trial_ledger.jsonl` nor `candidate_freeze.yaml`.

**Prepared:** 2026-07-24, against `origin/main` at `3c31c2e9d36d55defc95d89c90ab041f31abf251`
(the exact commit this document's own PR is based on), under `governance/decisions/OPS-0003-...md`'s
authorization item 4. Every artifact claim below was verified directly against the live
repository during this session (file existence, line counts, `pytest --collect-only` counts,
`pytest -q` pass/fail) — nothing here is carried over from a prior chat, report, or approximate
recollection.

---

## 1. Exact existing artifacts

**Engine (charter §4 "Engine" area):**

| File | Lines | Tests (pytest-collected) | Status |
|---|---:|---:|---|
| `margin_simulation.py` | 1,488 | — | Merged (PR #139, G2A) |
| `test_margin_simulation.py` | 2,158 | 127 | Merged; all 127 pass |

**Research package (charter §4 "Research package" area) — under `research/margin_target_study/`:**

| File | Status |
|---|---|
| `PROTOCOL_V2.md` | Present, hash-pinned (G0, PR #137) |
| `pre_registration.yaml` | Present, hash-pinned (G0, PR #137) |
| `data_manifest.yaml` | Present (G1, PR #138) |
| `assumptions_ledger.yaml` | Present (G1, PR #138) |
| `data_acquisition.py` | Present (G1, PR #138) — data acquisition/validation script; implements price caching with development-boundary truncation, the sealed untouched archive, the T-D3 dividend-reconciliation `reconcile()` command, and a `validate()` command covering prices, dividend ledger v2, corporate-action ledger, crypto assertions, Track 3 boundaries, ^IRX, DFF, and account-evidence completeness — run as a script, not part of the pytest suite |
| `data/` (cached datasets) | Present (G1) |
| `G1_DATA_VALIDATION_REPORT.md` | Present (G1) — records **G1 DATA GATE PASSED**, including **T-D3 PASS 63/63 tickers + both Track 3 books** |

Also present but **not listed in charter §4** and not part of this determination's scope:
`run_stress_regime_sensitivity.py`, `test_margin.py`, `test_margin_state.py` — these are
pre-existing production/backtest files unrelated to MARGIN-0005 and are unaffected by it.

**Repayment library (charter §4 "Research package" area, per its file list) — actual location
deviates from the table:**

| File | Lines | Tests (pytest-collected) | Status | Location note |
|---|---:|---:|---|---|
| `repayment_lib.py` | 601 | — | Merged (PR #140, G2B) | Lives at **repo root**, not under `research/margin_target_study/` as charter §4's file list and protocol §13's architecture diagram show it |
| `test_repayment_lib.py` | 789 | 93 | Merged; all 93 pass | Repo root |

This root-level placement is not a defect introduced by this document — `operations/WORKSTREAMS.yaml`'s
own G2B milestone `evidence_refs` already records `margin_simulation.py` and `repayment_lib.py`
without a `research/` prefix, meaning the actual accepted implementation location was already root,
not the protocol diagram's nested path. This determination records the fact; it does not attempt to
relocate either file (relocation is itself a change requiring its own review, not a scope-fit question).

**Full test suite (verified this session, clean venv, `requirements.txt` pinned versions):**
`python3 -m pytest -q` → **1,246 passed, 0 failed** — matches PR #143's own recorded count exactly.
`intelligence_validator.py` and `freshness_validator.py` both exit clean (as PR #143 also recorded).

## 2. Exact absent authorized artifacts

Every other file named in charter §4's approved-file table is confirmed **absent** (verified by
`find` across the full repository, not just `research/margin_target_study/`):

- `overlay_lib.py`, `test_overlay_lib.py`
- `maintenance_lib.py`, `test_maintenance_lib.py`
- `dividend_ledger.py` (no dedicated test file is named for it in §4's Tests row)
- `target_variants.py`, `test_target_variants.py`
- `validation_lib.py`, `test_validation_lib.py`
- `shadow_replay.py`, `test_shadow_replay.py`
- `run_study_a.py`, `run_study_b.py`, `run_study_c.py`, `run_stress_suite.py`
- `trial_ledger.jsonl`, `candidate_freeze.yaml`, `intelligence_flag_events.yaml`
- `research/margin_target_study/results/` (any contents)

Zero of these exist anywhere in the repository as of this commit. This is expected — the charter's
§4 table is a **ceiling on what future PRs may create**, not a claim that every listed file already
exists or must eventually exist (see §3 below on `maintenance_lib.py` specifically).

## 3. Classification — required for literal G2 closure vs. permitted vs. later-stage

The protocol's own §18 gate table states the **literal G2 pass criteria** narrowly: *"Engine
extensions merged (own PRs); full suite green; T-1 anchors exact; T-D1–T-D5, T-U1/T-U2 pass."*
This is a materially narrower bar than "every file in §4 exists" or "every test named anywhere in
§14 passes" — most of §14's test IDs (T-2 through T-9, T-C1, T-S1) apply to modules that don't
exist yet and whose properties are therefore not yet even *statable*, let alone required for G2
specifically. Distinguishing by that literal bar:

### Required for literal G2 closure (§18's own text)

| Test | Current state | What's missing |
|---|---|---|
| **T-1** (engine regression, legacy anchors reproduce exactly) | **Already satisfied.** `test_margin_simulation.py` includes the Phase 3 replication anchors; full suite green. | Nothing. |
| **T-D1** (dividend uniqueness: each (ticker, ex-date) credits exactly once, duplicate-injection test) | Partially demonstrated at the *engine-consumption* layer (`test_g2a_dividend_cash_credited_exactly_once` and related G2A tests prove the engine credits an incoming ledger entry exactly once) but **not** at the *ledger-construction* layer — no module owns building the point-in-time per-ticker ledger from `data_acquisition.py`'s validated data into the engine's daily input, so there is nothing yet that could contain a duplicate-injection bug to test against. | `dividend_ledger.py` (construction module) + a dedup test, housed per §4 either as an extension of the already-existing `test_margin_simulation.py` or inside `test_validation_lib.py` (§4 names no dedicated `test_dividend_ledger.py`). |
| **T-D2** (primary-path purity: primary prices are split-adjusted only; TR divergence must exist for known payers) | Not yet testable — no module yet asserts or enforces that the *simulation* primary path never touches the TR namespace (`data_acquisition.py` already quarantines TR for its own G1 reconciliation use, per T-D3, but that is the *data* layer, not a *simulation-input* guarantee). | `dividend_ledger.py` + the same test file as T-D1. |
| **T-D3** (reconciliation ±0.3pp/yr) | **Already satisfied and passed** — `G1_DATA_VALIDATION_REPORT.md` §6 records **PASS, all 63 tickers + both Track 3 books** (worst case 0.157pp/yr), via `data_acquisition.py`'s `reconcile()` command. This is a G1 artifact, already merged. | Nothing. |
| **T-D4** (structural bar: simulation runners and `dividend_ledger.py` cannot reference the TR namespace; only `validation_lib.py` may) | Not yet testable — neither `dividend_ledger.py` nor `validation_lib.py` exists, so there is no import graph to assert a barrier over. | Both files + an import-graph test (naturally `test_validation_lib.py`, extending the existing isolation pattern `test_margin_simulation.py`'s T-8-style checks already use against `allocate.py`/`margin_state.py`). |
| **T-D5** (repayment routing under R2: dividend cash reduces debt XOR reinvests, never both) | **Already satisfied.** The protocol names this "see T-5" — `test_repayment_lib.py` already tests `r2_dividends_first`'s reinvest-XOR-repay routing as part of G2B's T-5 coverage. | Nothing. |
| **T-U1** (untouched isolation: development-mode loader physically truncates at the boundary; untouched-mode flag illegal outside the G4 runner; G3 report generators fail on untouched-period timestamps) | The *data-truncation* half is already built and validated — `data_acquisition.py` truncates at the development boundary and seals the untouched segment in a byte-hash-verified archive that "no G1 or development code opens." The *code-legality* half (asserting an untouched-mode flag is rejected everywhere except an authorized G4-runner context) is not yet test-enforced anywhere, and no G3 report generator exists yet to test against untouched timestamps. | A guard function + test asserting untouched-mode access is illegal from ordinary calling context. This is buildable **now**, without building the real G4 runner (S4 scope) — the test exercises the guard's *legality check*, not an actual future runner. Natural home: `validation_lib.py`. |
| **T-U2** (candidate freeze: `candidate_freeze.yaml` append-only; untouched runner refuses unfrozen configs; post-freeze changes void the candidate) | Not yet built. | A generic append-only-guard function and a hash-membership check, both testable against a **temporary test fixture path** — never the real `candidate_freeze.yaml`, which must not exist yet (it is authorized only at the real G3 freeze). Natural home: `validation_lib.py`. |

**Conclusion: exactly two new files — `dividend_ledger.py` and `validation_lib.py` (plus tests) —
are required to literally close every named G2 gate criterion.** T-1, T-D3, and T-D5 are already
done; nothing further is needed for them.

### Permitted but not strictly required for G2 (needed instead for Study A/B/C to ever execute at S3)

| File | Why it exists in §4 | Why it's not a G2-gate blocker |
|---|---|---|
| `overlay_lib.py` | Study A's overlay decision functions (A-6 trend, A-7 vol-target, A-8 staged pullback, A-9 crash-only, A-10 regime, A-11 combined) — the actual policies that would compute a `leverage_target` value each day | The engine already exposes a generic, tested `leverage_target` pre-trade hook (G2A: clamped to `[1.0, 1.8]`, dead-band suppression, 5 dedicated passing tests) that overlay functions would call *into* — but no G2 gate criterion (T-1, T-D1–T-D5, T-U1/T-U2) requires the overlay functions themselves to exist. Study A simply cannot run without them (S3 concern, not G2). |
| `target_variants.py` | Study B's target-sizing variants (B-0…B-6) and the programmatic TGT-0001 ex-ante cluster check (T-6) | Same reasoning — needed for Study B to ever run, not named in §18's G2 criteria. |

### Later-stage or study-run artifacts (explicitly not needed now, and some explicitly barred)

| File | Stage | Note |
|---|---|---|
| `run_study_a.py`, `run_study_b.py`, `run_study_c.py`, `run_stress_suite.py` | S3 (running the registered studies) | Their entire purpose is to consume trial budget executing `simulate()` calls — that is explicitly S3, gated behind its own future principal authorization to open S3, not S2. |
| `shadow_replay.py`, `test_shadow_replay.py` | S6/S7 (shadow phase) | Charter §4 states plainly: "backlog-item-5 logging changes to `allocate.py` ... required for the shadow phase and authorized, if at all, by its own separate future decision at gate G6." Building `shadow_replay.py` before that G6 authorization exists would create dead code for a phase this charter does not yet permit. |
| `trial_ledger.jsonl` | Runtime, first `simulate()` call | Created only when a real trial runs (S3). Charter forbids fabricating it to populate any filing. |
| `candidate_freeze.yaml` | G3 (candidate freeze) | Created only at the real G3 freeze, after development-window verdicts. Charter forbids fabricating it early. |
| `intelligence_flag_events.yaml` | Study D (prospective shadow) | Human-authored, source-pinned research content — not code, and Study D is prospective-shadow-only (zero historical trial budget); nothing to populate it with yet. |
| `research/margin_target_study/results/**` | S3+ | Populated only once real trials run. |

### `maintenance_lib.py` — a specific, resolvable ambiguity

Charter §4 lists `maintenance_lib.py` / `test_maintenance_lib.py` as approved future artifacts.
However, **G2A's actual implementation already built the maintenance-excess proxy and forced-liquidation
mechanics directly inside `margin_simulation.py`** — the G2A milestone description in
`operations/WORKSTREAMS.yaml` names exactly this ("maintenance-excess proxy, forced liquidation,
leverage-target hook"), and the engine test file already carries 25 dedicated, passing tests
covering per-position `m_i` schedules, escalation, cure sizing, both pro-rata/largest-first
sequencing variants, and the "liquidation never increases leverage" invariant — the substance the
protocol's T-3 describes. The charter's §4 file list is a **ceiling on what a future PR may touch,
never a mandate that every named file must eventually exist**; nothing in MARGIN-0005 requires
`maintenance_lib.py` to be built if its function was already achieved additively elsewhere. This
determination recommends treating `maintenance_lib.py` as **not needed**, but does not itself make
that call final — it should be an explicit, one-line confirmation in the final S2 PR's own
description, checked by that PR's independent reviewer, rather than silently assumed.

## 4. Unresolved test/integration obligations

- T-D1, T-D2, T-D4, T-U1, T-U2 (§3 above) — the concrete, still-open G2-gate obligations.
- The **pre-S3 R2 integration constraint**, recorded in `operations/WORKSTREAMS.yaml`'s WS-0001
  `evidence_refs` from PR #140's independent review: `r2_dividends_first` must never be wired into
  `simulate()`'s pre-trade hook using a same-day dividend amount before that dividend is actually
  credited to cash, because under insufficient idle cash that ordering could fund a repayment by
  selling shares before the dividend lands. **This determination accounts for it explicitly**:
  `dividend_ledger.py`'s output must carry dividend cash keyed to its actual credited date (not its
  declared or ex-date), so that any future consumer — including `repayment_lib.py`'s R2 — can only
  ever observe dividend cash on or after the day it structurally exists. The recommended final S2 PR
  (§5 below) does **not** wire any repayment policy into `simulate()`'s default flow (nothing does
  today, and this determination does not change that) — it only recommends that `dividend_ledger.py`
  be built so that the ordering bug PR #140 flagged is structurally impossible whenever wiring does
  happen at S3, and that a test assert this (an addition to `test_validation_lib.py` or
  `test_margin_simulation.py`, not a new named T-ID the protocol doesn't already define).
- Whether `maintenance_lib.py` is formally in-scope or out-of-scope (§3) — recommended resolution:
  out-of-scope, confirmed explicitly by the final S2 PR's own description and its independent
  reviewer, not silently dropped.

## 5. Recommendation: smallest coherent final S2 implementation scope

**This determination recommends option (a): a smallest coherent final S2 PR scope, for a later,
separate principal authorization.** It does not recommend an honest G2 stop (the remaining gap is
small, concrete, and closable in one narrow additive PR) or a charter amendment (nothing above
requires more than the ≤3 S2 PRs the charter already permits, and this would be exactly the 3rd and
last one — no 4th PR, no ceiling change, no new file outside §4's existing table).

**Recommended scope — exactly:**

1. `dividend_ledger.py` (new) — bridges `data_acquisition.py`'s validated, cached dividend/corporate-
   action data into the per-day input `margin_simulation.py` already accepts; structurally barred
   from importing or referencing the TR (total-return) namespace; dividend cash keyed to actual
   credited date (§4 above, R2 ordering safety).
2. `validation_lib.py` (new) — TR-quarantine namespace + import-graph isolation checks (T-D4, T-8
   extension); untouched-mode loader legality guard (T-U1); candidate-freeze append-only and
   hash-membership guard functions operated only against temporary test fixtures, never the real
   `candidate_freeze.yaml` (T-U2); the bootstrap/DSR/fold-boundary statistical machinery the
   protocol's §11 validation requirements and T-7 describe (needed regardless of when Study A/B
   actually run, and naturally bundled with the isolation work above since both are "validation"
   concerns per the protocol's own module naming).
3. `overlay_lib.py` (new) — Study A's overlay decision functions (A-6, A-7, A-8, A-9, A-10, A-11),
   each a pure function of t−1 state producing a `leverage_target` consumed by the engine's existing,
   already-tested pre-trade hook; leverage targets asserted always within `[1.0, 1.8]` (T-4).
4. `target_variants.py` (new) — Study B's target-sizing variants (B-0…B-6), each passing a
   programmatic TGT-0001 ex-ante cluster-compatibility check by construction (T-6).
5. `test_validation_lib.py`, `test_overlay_lib.py`, `test_target_variants.py` (new) — per §4's Tests
   row. Dividend-ledger dedup/purity tests (T-D1/T-D2) are housed in `test_validation_lib.py` or as
   narrow additions to the already-existing `test_margin_simulation.py`; §4 names no dedicated
   `test_dividend_ledger.py`.

**Explicitly excluded from this recommended scope, with reasons already stated above:**
`maintenance_lib.py` / `test_maintenance_lib.py` (§3 — likely redundant with G2A, final confirmation
left to the PR's own review); `shadow_replay.py` / `test_shadow_replay.py` (G6-gated, not yet
authorized); `run_study_a.py`, `run_study_b.py`, `run_study_c.py`, `run_stress_suite.py` (S3
execution scope); `trial_ledger.jsonl`, `candidate_freeze.yaml`, `intelligence_flag_events.yaml`,
`research/margin_target_study/results/**` (created only at their own later stage; two of them are
this task's own explicit prohibitions).

**One honest caveat on size and reviewability:** this recommended scope (four new modules, three new
test files) is larger than either individual prior S2 PR (G2A: one engine file + one test file;
G2B: one library + one test file). It is sized this way because it is deliberately the **last**
S2 PR available under the charter's ≤3 ceiling — splitting `dividend_ledger.py`/`validation_lib.py`
(G2-gate-closing) from `overlay_lib.py`/`target_variants.py` (S3-enabling) across two more PRs is not
possible without a charter amendment to raise the ≤3 ceiling, which this determination does not
recommend absent evidence that the combined scope is genuinely unreviewable in one pass. If the
final S2 PR's own independent reviewer concludes the combined scope is too large to review safely
as one unit, the correct escalation at that point is a narrow charter amendment adding one additional
S2 PR slot — not silently splitting scope across an unauthorized 4th PR.

## 6. Allowed files for the recommended later PR

Exactly: `dividend_ledger.py`, `validation_lib.py`, `overlay_lib.py`, `target_variants.py`,
`test_validation_lib.py`, `test_overlay_lib.py`, `test_target_variants.py` — all under
charter §4's existing approved-file table; no new path outside that table.
Narrow, reviewable additions to the already-existing `test_margin_simulation.py` (for T-D1/T-D2
dedup/purity tests) are also within the already-approved Engine area.

## 7. Prohibited files and behavior for that later PR

No modification of `holdings.yaml`, `targets.yaml`, `allocate.py`, `margin_state.py`, Intelligence
records, CLAUDE.md doctrine text, or the Constitution. No creation of `trial_ledger.jsonl`,
`candidate_freeze.yaml`, `intelligence_flag_events.yaml`, or `research/margin_target_study/results/**`.
No `shadow_replay.py` or any `run_study_*.py`/`run_stress_suite.py`. No `simulate()` call outside a
test's own fixtures — the recommended PR remains additive and output-neutral when unconsumed, exactly
like G2A and G2B. No wiring of any repayment policy into `simulate()`'s default/automatic pre-trade
flow. No trade, no order, no live signal, no opportunity map, no precomputed recommendation. No
re-running of any closed Decisions-Log question. This recommended PR does not itself authorize S3,
Study A/B/C execution, or any trial consumption — that remains its own separate future principal
authorization exactly as WS-0001's `next_action` already states.

## 8. Required tests and independent-review gate

All existing 1,246 tests must remain green; the new test files must bring the isolation
(import-graph, write-path), T-D1/T-D2/T-D4, T-U1/T-U2, and T-6/T-7 properties under test as described
in §5. The recommended PR requires the same individual review discipline G2A (two remediation
rounds) and G2B (pass-with-non-blocking-observations) already received — not a lighter bar merely
because it is the last authorized S2 PR. The `maintenance_lib.py` exclusion (§3) must be an explicit,
reviewed line item in that PR's own description, not an assumption inherited from this document.

## 9. Zero trials, no registered study

This document consumes zero of the 300-run trial ceiling, appends nothing to a trial ledger that
does not exist, and runs no simulation of any kind — read-only repository inspection and `pytest`/
`git`/`find` verification only, performed during this session.

## 10. This determination does not authorize anything

Recommending the scope in §5 is not authorization to build it. Opening the recommended final S2 PR
requires its own separate, explicit principal authorization, exactly as `operations/WORKSTREAMS.yaml`'s
WS-0001 entry already states and as OPS-0003 preserves unchanged.
