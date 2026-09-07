---
decision_id: MARGIN-0005
date: 2026-07-23
status: Accepted
category: research_charter
related_decisions: [GOV-0002, GOV-0003, MARGIN-0003, MARGIN-0004, TGT-0001, NUM-0001, PI-0001, PI-0011, PI-0015]
supporting_artifact: research/margin_target_study/PROTOCOL_V2.md
---

## Context

`GOV-0003` (2026-07-21) narrowed Constitution §3/§4: discretionary or predictive margin timing
remains permanently excluded, but whether a rules-based, pre-registered, evidence-gated
conditional deployment or repayment rule outperforms the current fixed posture is an open
empirical question — researchable only under its own separately governed research charter,
adoptable only through its own separate later governance decision. `MARGIN-0004` reconciled the
closed Phase 3–7A program and enumerated (§B) what it deliberately left untested. GOV-0003
explicitly did not create a charter. **This decision is that charter.** It adopts the study
protocol filed alongside it as its complete technical specification and grants research
permission exactly as bounded below. A design-phase protocol and charter draft were prepared
outside the repository and revised under two rounds of principal review before this filing;
this file and the two artifacts pinned below are the entire governance record — nothing outside
the repository carries authority.

## Decision

### 1. Exact research authority granted

This charter authorizes only:

1. Execution of the research program defined in `research/margin_target_study/PROTOCOL_V2.md` —
   Studies A (margin overlays, targets fixed), B (target sizing at 1.00x), C (bounded
   interactions), D (Intelligence advisory research, prospective-shadow only), the split stress
   suite (§12A mandatory / §12B diagnostic), and the statistical-validation plan — strictly
   within the frozen `research/margin_target_study/pre_registration.yaml` and the 300-run hard
   ceiling.
2. The data-acquisition steps named in the protocol's G1 gate (split-adjusted bar verification,
   point-in-time dividend ledger, benchmark/risk-free/rate series, conditional crypto bars),
   cached read-only under the research directory and recorded in the future `data_manifest.yaml`
   (source, acquisition timestamp, coverage, transformations, hashes, validation results, known
   limitations).
3. Future implementation PRs limited to the approved files in §4 below, each individually
   reviewed and merged through the normal PR process.
4. Retrospective, batch, quarterly shadow replays per the protocol's §16 — contingent on a
   separate future authorization for the backlog-item-5 logging infrastructure (gate G6), which
   this charter does not grant.

Everything not listed is not authorized. This charter is not an adoption decision, not a target
change, not a margin-policy change, and not an allocator change. **This filing itself performs no
data acquisition, creates no research implementation code, runs no simulation, operates no
shadow process, mutates no Intelligence record, and places no trade or order.**

### 2. Prohibited production effects (absolute for the charter's entire life)

- No order placement, ever (order methods remain absent from `alpaca_client.py`).
- No modification of `holdings.yaml`, `targets.yaml`, `allocate.py`, `margin_state.py`,
  Intelligence records, CLAUDE.md doctrine text, or the Constitution by research code or by
  virtue of any research result.
- No live signal, opportunity map, price target, opaque score, continuous "borrow now"
  indicator, or precomputed recommendation (GOV-0003 §4 conditions). Shadow evaluation is
  retrospective and batch-only; nothing runs inside or alongside `allocate.py`'s output.
- No arm, run, or shadow computation models exceeding the 1.8x leverage cap as candidate
  behavior, or bypassing the 30%-buffer-floor blocking behavior; both remain unchanged, and this
  charter cannot change them.
- No valuation-judgment conditioning ("borrow because X is cheap") in any rule.
- No re-running of closed Decisions-Log questions as variants.
- Operator discretion remains asymmetric: always free to decline, use less, repay more/sooner;
  never free to exceed a governed limit. Research output never weakens this.

### 3. Hash pinning (same-PR chronology)

The final protocol and the frozen pre-registration were finalized first, their SHA-256 hashes
computed, those exact hashes inserted here, and **all three artifacts (protocol, this charter,
pre-registration) filed together in this single G0 filing PR**:

- `research/margin_target_study/PROTOCOL_V2.md`
  SHA-256: `d794a4c09fa81dbaa147bb830da91b75221a35175f47c8bd979b75e3fc154e21`
- `research/margin_target_study/pre_registration.yaml`
  SHA-256: `e3b101e336f2ff30c013908a4c2b30918e9adf59cbb26499d2774927e472120e`

After merge, the hashes are verified from the committed blobs (`git show <merge>:<path> |
sha256sum`). **No simulation may run before this PR is merged and the pinned hashes verify.**
Any later change to either pinned artifact is a charter amendment: its own governance decision
with a new pinned hash. Silent edits are detectable by hash mismatch and void any result
produced after the edit. The runtime trial ledger (`trial_ledger.jsonl`) records a
configuration hash per run; the final report reconciles every run — including failed and
discarded runs — against the pinned pre-registration.

### 4. Approved files and artifacts for future implementation

Implementation PRs under this charter may create or modify only:

| Area | Files | Constraint |
|---|---|---|
| Engine (additive) | `margin_simulation.py`, `test_margin_simulation.py` | Output-neutral when unconsumed; Phase 3 replication anchors must reproduce exactly before any new result is accepted |
| Research package | `research/margin_target_study/` — `PROTOCOL_V2.md`, `pre_registration.yaml`, `data_manifest.yaml`, `assumptions_ledger.yaml`, `trial_ledger.jsonl`, `candidate_freeze.yaml`, `intelligence_flag_events.yaml`, `overlay_lib.py`, `repayment_lib.py`, `maintenance_lib.py`, `dividend_ledger.py`, `target_variants.py`, `data_acquisition.py`, `run_study_a.py`, `run_study_b.py`, `run_study_c.py`, `run_stress_suite.py`, `validation_lib.py`, `shadow_replay.py`, `results/**` | Zero import relationship with `allocate.py`/`margin_state.py` in either direction (test-enforced); writes only under its own directories; total-return price data quarantined to the validation namespace |
| Tests | `test_overlay_lib.py`, `test_repayment_lib.py`, `test_maintenance_lib.py`, `test_target_variants.py`, `test_validation_lib.py`, `test_shadow_replay.py` | Deterministic; no live network in CI |

Of the research artifacts, **only `PROTOCOL_V2.md` and `pre_registration.yaml` carry substantive
content in this G0 filing PR**. `data_manifest.yaml`, `assumptions_ledger.yaml`,
`trial_ledger.jsonl`, `candidate_freeze.yaml`, and `intelligence_flag_events.yaml` are
authorized future artifacts created only during their own stages — they are not fabricated to
populate this filing. `candidate_freeze.yaml` and `intelligence_flag_events.yaml` are
append-only; `intelligence_flag_events.yaml` is human-authored and source-pinned, references
existing Intelligence records without modifying them, and research code may read it but may
never create or modify Intelligence records.

Explicitly outside this charter: backlog-item-5 logging changes to `allocate.py`
(`update_margin` extension, `margin_log.csv`, cash-flow ledger) — required for the shadow phase
and authorized, if at all, by its own separate future decision at gate G6.

### 5. Trial ceiling

**300 simulated configurations, program-wide, hard**, allocated exactly per the protocol's §9
ledger: **286 enumerated development configurations + 10 untouched-test simulations + 4
data-correction-only reserve runs** (reserve never for new arms/parameters; every use logged
with cause). Survivor-dependent budget, unused untouched-test capacity, and unused reserve all
lapse and may not be reallocated. Post-processing analytics (bootstrap, walk-forward windowing
over stored development-period paths, DSR/PSR, cost-basis variants) are not simulation trials
and are disclosed as compute. Exceeding the ceiling requires a charter amendment **before** the
excess run, never retroactive ratification.

### 6. Untouched-test isolation (binding)

Development boundaries: **Track 2 development data ends 2025-06-30; Track 3 development data
ends 2020-12-31.** Development, validation, parameter-stability, bootstrap-selection, and G3
reporting code cannot read, simulate, store, display, or summarize untouched-period data (loader
truncation, test-enforced). Finalist identities and configuration hashes — at most **2 Study A,
2 Study B, 2 Study C finalists** — are frozen first in append-only `candidate_freeze.yaml`; only
after that G3 freeze may G4 run the untouched periods. Each untouched evaluation is an explicit
`simulate()` call counting toward the 300-run ceiling (≤10 total: 2 Study A finalists × {Track 2
roster, Track 3 SPY, Track 3 QQQ} = 6; 2 Study B finalists × Track 2 = 2; 2 Study C finalists ×
Track 2 = 2). The untouched test is spent exactly once; untouched-period outputs cannot be
regenerated with modified candidates without a charter amendment.

### 7. Required data gates (G1 — no simulation before all are resolved)

- Split-adjusted price cache verified (continuity checks), refreshed through the run date.
- **Dividend accounting:** point-in-time per-ticker dividend ledger acquired; the primary path
  is split-adjusted, non-total-return prices plus explicit dividend cash; total-return series
  are acquired for reconciliation only and are structurally barred from the primary path;
  reconciliation passes within ±0.3pp/yr; the protocol's dividend double-count proofs
  (T-D1–T-D5) pass. Total-return prices are never combined with explicit dividend cash.
- Benchmark (SPY/QQQ total-return, used as benchmarks only), risk-free series, and the
  Fed-funds-anchored borrowing-rate series acquired; Gold subscription cost and the unsubscribed
  counterfactual verified against the account's actual terms.
- **Crypto decision recorded:** outcome (a) validated point-in-time BTC/ETH/SOL bars (then
  Study B crypto configs run) or outcome (b) crypto target sizing declared outside Study B's
  evidentiary scope (configs cancelled, budget lapses). No third option; no cash-like proxy.
- `data_manifest.yaml` completed for every acquired dataset.
- Any degraded mode proceeds only on the principal's explicit, recorded acceptance of the
  pre-registered degraded-mode disclosures.

### 8. Stress-test categories (binding definitions)

- **Mandatory survivability set (protocol §12A)** — historically plausible crash replays (2008,
  2018, 2020 — all inside the Track 3 development window), conservative rate shock
  (+400bps/6mo), conservative maintenance escalation (30→35% + FINRA 4210(g)(8)), overnight gaps
  (−7/−13/−20%), slow bear (−35%/18mo). **Adoption criteria apply here:** zero forced
  liquidations, no proxy-floor breach >5 sessions, severe-impairment ceiling respected. Failing
  any §12A scenario fails G3/G4.
- **Catastrophic boundary diagnostics (protocol §12B)** — synthetic −65% decline, doubled
  maintenance, concatenated worst-decile blocks, combined beyond-history shocks. These produce
  failure-boundary maps and severe-impairment estimates; **they do not automatically disqualify
  a candidate** unless the principal promotes a §12B scenario to the mandatory set by charter
  amendment. Rationale: the mandatory set is the historical-plausibility envelope that
  doctrine's own survivability definition names; requiring survival of beyond-history shocks
  would de facto mandate 1.00x — a doctrine change reserved to the principal, made knowingly via
  the §12B maps, never by a stress-suite default.

### 9. Intelligence advisory-only boundary (Study D)

Intelligence remains advisory under PI-0001 and successors. Under this charter it may never:
increase leverage; **include or exclude individual deployment recipients, or redirect margin
dollars among securities**; change tiers or targets; alter allocator output; or create an
opaque opportunity, conviction, or regime score. Study D researches exactly three retrospective
shadow comparisons, all counterfactual and non-operational: (1) **annotation-only control** — a
dated risk flag attached to an otherwise valid mechanical action without changing it; (2)
**whole-cycle draw freeze** — hypothetical suppression of the entire new-margin draw for that
cycle; (3) **account-level repayment advisory** — hypothetical recommendation to repay to
governed exposure or 1.00x. The ticker-level recipient-veto semantic considered during design
is removed and prohibited. Because no Intelligence record predates 2026-07-18, Study D is
prospective-shadow only, consumes zero historical trial budget, and is event-count-gated; a
historical replay may be proposed only by charter amendment upon the protocol's record-adequacy
bar. Flag events live in append-only, human-authored, source-pinned
`intelligence_flag_events.yaml` (minimum fields per the protocol §6: event_id,
company_or_theme, flag_category, source_record, source_locator, source_publication_date,
flag_authored_ts, effective_ts, resolved_ts_or_status, materialization_criteria, author,
provenance). Any future *operational* use of any Study D semantic requires separate PI-side
governance **and** separate margin-policy governance.

### 10. Stopping conditions

The program stops — reporting what it has, without adoption — upon any of: honest null at G3/G4
(proceeding to the G6 logging authorization remains permitted and encouraged — it closes the
permanent real-data gap); trial-ceiling exhaustion without a charter amendment; unresolved
G1 data-gate failure; engine-integrity failure (replication anchors or dividend proofs
unfixable); **a principal stop order at any time, for any reason, effective immediately**; a
discovered material conflict with a higher-authority source per GOV-0002 (affected work halts
until reconciled); shadow insufficiency without prejudice (candidates below event minimums
remain "insufficient evidence" indefinitely; the shadow phase may be wound down at any
evaluation point).

### 11. Artifact and review requirements

Every stage produces its named artifacts (protocol §13/§19): data-validation report and
manifest; ≤3 narrow implementation PRs, individually reviewed; interim study reports; the trial
ledger; the candidate freeze; the stress report with §12A/§12B separated;
`FINAL_PARETO_AND_CLASSIFICATION.md` (Q6/Q7 two-column historically-supported vs
requires-prospective-shadow classification plus failure-boundary maps); quarterly shadow
reports. All simulated output carries the engine's hypothetical-label guard; banned-phrase
enforcement extends to all new renderers. Every new numeric parameter is NUM-0001
provenance-classified at pre-registration. Each gate (G1–G8) is a recorded review outcome, not
an implicit pass; the untouched test is spent exactly once and its expenditure logged.

### 12. Null results preserve the fixed posture

A null or negative result at any gate preserves the current fixed posture unchanged — the 1.8x
structural cap, the 30% buffer floor, cash-first workflow, recommendation-only manual
execution. This outcome is pre-declared legitimate and valuable: it converts the current
provisional-guardrail posture into an evidence-checked one without changing it. The program is
designed to be endable at G3, G4, G5, or G7 with nothing altered.

### 13. No backtest result changes policy without a later governance decision

No result produced under this charter — however strong — changes any production policy,
parameter, target, tier, cap, floor, workflow, or recommendation. Adoption of any rule
requires: G5 classification, G6/G7 shadow completion with event-count minimums, and its own
separate future governance decision (G8) meeting the repository's full evidentiary bar,
including TGT-0001's mandatory disclosure template and ex-ante cluster-compatibility rule for
any target change, all strictly inside the unchanged 1.8x cap and 30% buffer floor. Neither
this charter nor any report it produces can be cited as authority for any production change.

## Rationale

GOV-0003 opened exactly one research lane and required a separately governed charter before any
research occurs; MARGIN-0004 §B enumerated the questions Phase 3–7A deliberately left untested
(conditional/state-keyed deployment and repayment, deposit-cadence interaction, asset
eligibility, distinct maintenance/liquidation mechanics, financing-duration, dividend cash
flows) — this charter's program targets precisely those lanes and re-runs nothing that is
closed. The pre-registration/hash-pinning/trial-ceiling/untouched-test design applies the same
pre-committed evidentiary discipline every adopted rule in this repository has met (rungs,
trims, weights, regime, trend, t1t2), extended with isolation guarantees proportionate to this
program's larger search space. The stress split follows MARGIN_DOCTRINE's own survivability
definition. The Intelligence boundary preserves PI-0001's advisory-only architecture while
permitting the narrowest observable question (whole-cycle/account-level suppression) to
accumulate prospective evidence.

## Alternatives Considered

- **No charter; keep the fixed posture unexamined.** Rejected: GOV-0003 already judged the
  conditional question open and worth researching; leaving the guardrails provisional forever
  forgoes the chance to make them evidence-checked at near-zero risk (the program's null path
  changes nothing).
- **Fold research authorization into GOV-0003 itself.** Rejected by GOV-0003's own text — it
  explicitly withheld a charter, requiring this separate decision.
- **A broader charter including production integration or margin-state threshold calibration
  (MARGIN-0003's named future enhancements).** Rejected: adoption and threshold-setting are
  separate later decisions; bundling them here would grant authority the research hasn't earned.
- **Ticker-level Intelligence recipient vetoes in Study D.** Rejected on principal review:
  security selection under a flag is stock-picking through the back door and violates the
  advisory-only boundary; only whole-cycle and account-level semantics remain.
- **Elapsed-time-only shadow gate.** Rejected on principal review: rare-event rules could pass
  two quiet quarters without ever firing; event-count minimums replace it.
- **A single stress standard (all scenarios mandatory).** Rejected: beyond-history shocks would
  de facto mandate 1.00x by suite default rather than by the principal's knowing choice.

## Consequences

This filing adds exactly: this decision file; the pinned `PROTOCOL_V2.md` and
`pre_registration.yaml`; one `governance/decisions.yaml` index row; one short CLAUDE.md
Decisions Log pointer entry. Nothing else changes. Confirmed unchanged: the 1.8x leverage cap,
the 30% buffer floor, `targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`,
`margin_simulation.py`, `alpaca_client.py`, every test file, `decision_log.yaml`,
`performance_log.csv`, `intelligence/` (all records), `reports/`, every Phase 3–7A artifact,
and the recommendation-only manual-execution model — this tool still never places orders.
Research execution begins, at the earliest, after this PR merges, the pinned hashes verify from
the committed blobs, and the G1 data gate passes.

This decision becomes effective only when its implementing pull request merges to `main`.
