# Portfolio-HQ Margin Deployment and Target Sizing Research Program — Study Protocol v2 (final, canonical)

**Status:** Final study protocol, filed with the MARGIN-0005 research charter (`governance/decisions/MARGIN-0005-margin-target-research-charter.md`). This document is a research design. It authorizes nothing by itself; all authority derives from the charter, and only once the charter's filing PR merges to `main` and its pinned hashes verify against the committed blobs.
**Date:** 2026-07-23
**Baseline:** `Mast3rkey/Portfolio-HQ` @ `f46d700` (origin/main at design time)
**Governing permission:** Constitution §3/§4 as amended by `GOV-0003`; open research lanes enumerated by `MARGIN-0004` §B.

**Hard scope guards:** no order placement ever; no modification of production files (`allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, Intelligence records, doctrine text) by research code or by virtue of any result; no backtest result is authority to alter production policy — adoption requires its own separate future governance decision. The 1.8x leverage cap and 30% buffer floor are governed constraints and research baselines, not deployment targets; no arm exceeds the cap or models a floor bypass; unused margin capacity is never presumed deployable. No live signal, opportunity map, price target, opaque score, continuous "borrow now" indicator, or precomputed recommendation is produced. Operator discretion is asymmetric throughout: always free to decline, use less, repay more/sooner; never free to exceed a governed limit. No simulation may run before the charter's filing PR is merged and the pinned protocol/pre-registration hashes verify.

---

## 1. Repository Preflight

Executed 2026-07-23 against `f46d700`: clean tree, no open PRs, root commit `3a2fce3` (2026-07-18 — git history does not predate it). Phase 3–7A margin research is closed (`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`, reconciled by `MARGIN-0004`); its engine (`margin_simulation.py` + six lib modules + runners) is the reusable substrate. `margin_state.py`'s CAUTION/RESTRICTED states are inert pending evidence-based thresholds (MARGIN-0003). Research backlog item 5 (real-data logging) is the only open backlog lane and a shadow-phase prerequisite requiring its own separate authorization. Stale-assumption findings recorded: CLAUDE.md's BTC-manual workflow note predates the rebuilt BTC position in `holdings.yaml`; the nominal target sum is **103.25%** at current config (TGT-0001's 101.55% predates the COST promotion). Intelligence corpus fact-check: 7 company records, `last_reviewed` spanning 2026-07-18 → 2026-07-23 only — **no point-in-time Intelligence history predates July 2026**, which fixes Study D's classification (§6). Live account context at design time (context only, not an argument for anything): net equity $6,088.57, gross $7,678.97, debt $1,590.40 (leverage 1.261x), synced buffer 63.12%.

## 2. Authoritative-Policy Map

Precedence per GOV-0002: (1) Constitution + incorporated `docs/MARGIN_DOCTRINE.md` (in full) and `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §20/§24; (2) accepted governance decisions — GOV-0003 (research permission + conditions), MARGIN-0004 (§B open-lane list), TGT-0001 (disclosure template + ex-ante cluster rule), TGT-0002, NUM-0001 (parameter provenance), MARGIN-0003, PI-0001…PI-0022 (Intelligence advisory-only; may not control targets); (3) CLAUDE.md operational synthesis and its closed Decisions-Log questions; (4) `targets.yaml`/`holdings.yaml` config truth; (5) code as implemented.

Derived binding rules:
- **R1** — fixed limits are feasibility constraints in every arm; the buffer-floor blocking behavior is replicated via the maintenance-excess proxy and never relaxed except in labeled §12B diagnostics that measure consequences, never candidate rules.
- **R2** — no valuation-judgment conditioning; all conditioning variables are mechanical account-state or market-state series.
- **R3** — closed Decisions-Log questions (rungs, band/spec trims, tier-weight gradation shapes, regime gate, trend gate, T1/T2 trim) are not re-run as variants; production gate settings are constant except where an arm's definition *is* the tested difference.
- **R4** — Study B never optimizes per-ticker, never produces conviction scores, never lets Intelligence content touch a target.
- **R5** — every new numeric parameter is NUM-0001 provenance-classified at pre-registration.
- **R6** — all output is hypothetical-labeled; the engine's `BANNED_PHRASES` guard extends to every new renderer.
- **R7** — Intelligence remains advisory and may never: increase leverage; **include or exclude individual deployment recipients or redirect margin dollars among securities**; change tiers or targets; alter allocator output; or create an opaque opportunity, conviction, or regime score. The only researchable Intelligence effect is suppression or delay of an otherwise valid mechanical margin action, at whole-cycle or account level only (§6).

## 3. Study Questions

Q1 deploy when-if-ever; Q2 conditional leverage levels (survivability first); Q3 recipient of borrowed capital (mechanical recipient policies only — see R7 for what Intelligence may never do here); Q4 repayment timing; Q5 target-sizing effects on sustainable compounding; Q6 historically-supported vs requires-prospective-shadow classification of every conclusion; Q7 whether dated, point-in-time Intelligence risk flags — at whole-cycle or account level — reduce realized drawdown or forced-risk events at acceptable cost (Study D, prospective shadow only).

## 4. Data Inventory and Gaps

**Exists:** `data/backtest/*.json` — 65 tickers, Alpaca IEX daily OHLCV, split-adjusted (no dividends), longest 2020-07-27 → 2026-07-10, joint window 2021-06-01 start; `performance_log.csv` (2026-07-13 → present); real margin history (7 syncs 2026-07-13→15, then routine syncs; leverage 1.62x→~1.26x, never near cap); git-reconstructable point-in-time state from 2026-07-18 only; the Phase 3–7A engine and libs; `backtest_regime.py` primitives (TWR, MaxDD, calendar, eligibility, $2,000-monthly deposit convention).

**Three separated evidence tracks:** Track 1 — point-in-time Portfolio-HQ replay (historically ~2 weeks deep; its real role is prospective, as the shadow substrate); Track 2 — current-roster counterfactual 2021-06 → 2025-06-30 (development) — **SURVIVORSHIP-BIASED, labeled on every table; arm-relative claims only**; Track 3 — long-history benchmark leverage overlays (SPY from 1993, QQQ from 1999) for leverage mechanics only, never blended with Track 2 in any statistic.

**Gap dispositions:**

| Gap | Disposition |
|---|---|
| Dividends | **Primary accounting path: split-adjusted, non-total-return prices + explicit point-in-time dividend cash ledger** (per-ticker ex-date and per-share amount; credited on ex-date; pay-date +30d lag sensitivity). Total-return series acquired **only** as a reconciliation/validation benchmark, quarantined to the validation namespace, structurally barred from the primary path. Never combine TR prices with explicit dividend cash. Tests §14 T-D1–T-D5 prove no dividend is counted twice |
| Roster history starts 2020/2021 | Accepted; Track 3 covers earlier regimes, mechanics only |
| No historical Robinhood rate series | Constructed: max(floor, Fed Funds effective + calibrated spread), anchored to the ~5% doctrine figure and Phase 7A's ~5.75% ≤$50k tier; flat-5% retained as replication case; stress rates §8.7 |
| No house-maintenance %/displayed-buffer formula | Maintenance-excess proxy (§8.5), calibrated against real synced-buffer pairs accumulating in `holdings.yaml` history; provisional floor until adequacy (≥25 paired observations spanning ≥10pp buffer range); named `maintenance_excess_proxy`, never "buffer" |
| No liquidation sequencing data | Pro-rata (primary) and largest-first variants; conclusions that flip between them → "requires prospective data" |
| Real cash-flow history thin | Backlog item 5 (separate authorization) accumulates it prospectively |
| Earnings-date history | Gate replayed as pass-through (accepted precedent; cost bounded by redirect logic) |
| Crypto | **No cash-like proxy.** Gate-G1 decision, two outcomes only: **(a)** acquire and validate point-in-time BTC/ETH/SOL daily bars 2021-06 → dev boundary (Alpaca `get_crypto_bars`, paged; continuous-coverage gap scan; second-source spot-check; calendar rule: last crypto close at or before each equity close, no future-bar leakage) — then Study B crypto configs run; **(b)** acquisition/validation fails → **crypto target sizing is declared outside Study B's evidentiary scope**, configs cancelled, budget lapses, exclusion stated in the final report |
| Intelligence history | Corpus begins 2026-07-18 → **fails point-in-time historical-replay validity**; Study D is prospective-shadow-only. Escape hatch requires charter amendment upon adequacy (≥12 months of records, ≥20 dated flag events with source dates) |
| G1 data manifest | Every acquired dataset is recorded in `data_manifest.yaml`: source, acquisition timestamp, coverage, transformations applied, content hashes, validation results, known limitations |

## 5. Experiment Matrix — Studies A, B, C

### Study A — Margin overlay, targets fixed (current `targets.yaml` frozen)

**Arms:** A-0a cash-only control / A-0b margin-every-deposit control (Phase 3 Test B replication anchor) / A-1 1.00x; fixed ladder A-2…A-5 (1.10/1.25/1.50/1.80x — A-5 is a **diagnostic ceiling arm only, never a candidate**); A-6 trend-controlled (L_hi ∈ {1.10, 1.25, 1.50} above benchmark 200-SMA, else 1.00); A-7 volatility-targeted (σ_target ∈ {10%, 15%} × L_max ∈ {1.25, 1.50} × source ∈ {account, benchmark}); A-8 staged pullback (fixed tranche schedule −10/−15/−20% → 1.10/1.25/1.40x, repay on recovery); A-9 crash-only (L* ∈ {1.25, 1.50} at ≥ −20% benchmark drawdown, repay-priority at −5% recovery); A-10 market-regime (L_hi ∈ {1.10, 1.25} in risk-on); A-11 trend+vol combined (surviving A-6/A-7 grid points only, ≤4). A-8/A-9 operationalize a mechanism doctrine flags structurally; they are measured under survivability-first scoring rather than excluded by argument.

**Fixed mechanics:** signals computed from close of t−1 only (SMA/EMA, drawdown, realized vol, account leverage, maintenance-excess proxy — nothing valuation-based); execution at close of day t (open-of-day sensitivity on survivors); draws ≤ 1/week, each ≤ 10% of net equity, only on deposit or signal-change days (manual-execution realism); rule-commanded de-levers uncapped, next session; rebalance dead-band |L − L*| ≤ 0.05; deployment recipient = production gap machine (largest-dollar-gap-first, $25 min lot, all gates and caps live); recipient variants on survivors: ETF-sleeve-first, and maintenance-aware eligibility (excluding modeled high-maintenance names — auto-classified "requires prospective broker data"); deposit-cadence sensitivity (12-month pause / halved / one 20% withdrawal) on survivors — the MARGIN-0004 §B cadence lane.

**Buffer/maintenance constraints in every arm:** hard 1.8x clip identical in form to `margin_capacity()`; maintenance-excess-proxy floor breach ⇒ draws blocked + forced de-lever state; FINRA 4210(g)(8) concentration-escalation variant; breach counts are first-class metrics.

#### 5.A.8 Repayment-policy families

Structural invariants above every policy: **(i)** risk-limit cures always execute first (cap or proxy-floor breach → immediate repayment, unlimited size — doctrine, not a variant); **(ii)** no policy ever borrows.

| ID | Policy | Definition |
|---|---|---|
| R1 | Deposits repay first | Each deposit pays debt to the arm's governed target exposure before any purchase |
| R2 | Dividends repay first | All dividend cash pays debt while debt > 0; reinvested only at debt = 0 (control: reinvest) |
| R3 | Governed trims repay first | Production-rule trim proceeds (cluster-cap, T1/T2 ceiling, band/spec RSI) pay debt before re-entering the gap machine |
| R4 | Borrowing-cost hurdle | Effective APR > H ∈ {6%, 8%} → all cash flows divert to repayment until APR ≤ H or debt = 0 (rate-level trigger, observable state) |
| R5 | Trend/vol deterioration | Benchmark < 200-SMA (t−1) or 63-day vol > 1.5× trailing-3-yr median → repay to 1.00x; re-lever only per the arm's own rule after clearing |
| R6 | Maintenance-excess deterioration | Proxy excess < floor + 10pp band → staged repayment (25% of shortfall per week) |
| R7 | Intelligence advisory (freeze/repay) | Study D semantics (§6) — **prospective-shadow only, zero historical configurations** |
| R8 | Restore-to-target only | Repay only leverage above the arm's governed L*; never below it by rule |
| R9 | Full repayment to 1.00x | Any trigger under the paired arm's rule repays to zero debt; re-deployment only via the arm's deployment rule |
| R-B | Model B profit-harvest (reference) | Legacy 10%-of-fresh-HWM-gain harvest; one reference configuration (Phase 3G established the dose-response) |

**Categorical separation (binding on all reporting):** arbitrary percentage-profit harvesting (R-B) and target-restoration trimming (R8) are different kinds of rules, never pooled, averaged, or ranked as one family. **A gain percentage is a path artifact and is never equated with thesis completion**; no repayment family may be justified by valuation language. Category labels: cash-flow-priority (R1–R3), cost-triggered (R4), state-triggered (R5–R6), advisory (R7), posture-defining (R8–R9), profit-path (R-B).

### Study B — Target sizing, leverage fixed 1.00x

B-0 current baseline (nominal sum 103.25%); B-1 tier multipliers ({T1, T2, band} × {0.8, 1.2} — budget levels, not the closed gradation-shape question); B-2 sleeve budgets (ETF {10%, 13%}; crypto {5%, 15%} **only under crypto outcome (a)**); B-3 cluster-cap-constrained reallocation (configured cluster totals to {75%, 50%} of caps; every config passes TGT-0001's ex-ante rule by construction); B-4 concentration reductions (T1-flatten to 2.50 redistributed pro-rata; semis ×0.75 with ETF absorbing); B-5 nominal budgets {110%, 120%} (with the mechanical-honesty note: at 1.00x cash-only this mostly reorders gap priorities — the measured quantity is the path effect); B-6 volatility-aware / equal-risk comparators (quarterly recompute from trailing 252d) — **research comparators only, pre-declared non-adoptable** under current doctrine. Exclusions: no per-ticker optimization, no conviction scores, no Intelligence-controlled targets. Company, tier, sleeve, cluster, and total-budget effects are reported in separate sections and never merged into one "optimal target set." Any target change ever proposed from this evidence is a TGT-0001 proposal, never a backtest output.

### Study C — Interaction study

Runs only after A and B verdicts freeze: ≤2 robust A overlays × ≤2 robust B structures (+ B-0). No combinatorial search, no new parameters, no grid refinement. Question: do overlay and structure effects compose, or does structure change destroy overlay survivability margins (the Phase 4A concentration×margin question with a real maintenance mechanic).

## 6. Study D — Intelligence Advisory-Veto Lane (prospective shadow)

**Classification: PROSPECTIVE SHADOW RESEARCH — zero historical trial budget.** No Intelligence record predates 2026-07-18; a historical replay would require inventing flag dates (lookahead by construction). Historical replay may be proposed only via charter amendment upon the §4 adequacy bar.

**Researchable semantics — exactly three, all retrospective, counterfactual, and non-operational:**

1. **Annotation-only control** — a dated risk flag is attached to an otherwise valid mechanical margin action **without changing it**; the shadow record simply carries the annotation, establishing base rates and flag quality.
2. **Whole-cycle draw freeze** — the flag hypothetically suppresses **the entire new-margin draw for that cycle**. All-or-nothing at cycle level; no per-security effect.
3. **Account-level repayment advisory** — the flag hypothetically recommends repayment to governed target exposure or to 1.00x. Account-level only.

**Removed and prohibited:** any ticker-level recipient veto. Intelligence must not include or exclude individual deployment recipients and must not redirect margin dollars among securities — recipient selection is and remains purely mechanical (gap machine). Any future *operational* use of even the three semantics above requires separate PI-side governance **and** separate margin-policy governance.

**Flag taxonomy** (dated, human-authored, source-pinned; mapped to existing schema surfaces; no new score fields): thesis-break risk; earnings uncertainty; regulatory/competitive deterioration; balance-sheet/funding deterioration; evidence staleness (PI-0011's strict overdue rule — the one flag mechanically computable today).

**Flag event ledger — `research/margin_target_study/intelligence_flag_events.yaml`:** append-only, human-authored, source-pinned research artifact. It **references existing Intelligence records without modifying them**; research code may read it but may never create or modify Intelligence records. Minimum fields per event: `event_id`; `company_or_theme`; `flag_category`; `source_record` and `source_locator` (file + section/key of the existing Intelligence record); `source_publication_date`; `flag_authored_ts`; `effective_ts`; `resolved_ts_or_status`; `materialization_criteria` (pre-stated, for false-positive adjudication); `author`; `provenance`.

**Metrics per veto event and aggregate:** drawdown/loss avoided (with-vs-without counterfactual paths in shadow replay); false-positive vetoes (per pre-stated materialization criteria); foregone return; flag latency (source-event date → authored timestamp); source freshness at effect time; veto frequency per quarter and flag class; effect on financing cost and time under water. Every veto lapses on resolution or a 90-day cap with mandatory re-review; lapsed-unresolved is a latency finding. Evidence bar: §16 event minimums; below minimum → "insufficient evidence," never a pass.

## 7. Objective and Constraints — Defining "Optimal"

Survivability first, return second. Metric suite per arm/track/period: CAGR (TWR, flows subtracted, net of financing); benchmark-relative (SPY, QQQ, A-1); MaxDD; time under water; recovery duration; worst month/quarter/year; Sharpe, Sortino, Calmar; downside deviation; borrowing cost ($ and pp/yr); turnover and cost-adjusted TWR (0/5/15bps); leverage peak, time-weighted mean, % days > 0.9×cap; financing-duration (debt-days); proxy-floor breaches (count/depth/duration); maintenance breaches under stress; forced-liquidation events; concentration-cap breaches; severe-capital-impairment probability P(DD ≥ 40%), P(DD ≥ 60%) with bootstrap expected shortfall. **Output is a Pareto frontier — never an auto-selected winner**; doctrine constraints are infeasible regions; any point is chosen only by the principal via governance. Pre-committed thresholds: ≥ 1.0pp/yr net TWR (incremental cost basis) AND MaxDD ≤ +1.0pp AND zero forced liquidations across §12A AND severe-impairment probability not worse than control; materiality bands ≥ 2.0pp / ≤ 0.5pp; Phase 4A outcome-gate applies to Study C concentration findings.

## 8. Execution Model

1–3: daily bars; fills at close of day t (open sensitivity on survivors); complete fills (disclosed simplification); $25 production min lot. 4: interest — daily accrual on max(0, debt − free tier), capitalized. **5: maintenance-excess proxy** — per-position m_i (baseline 25%; SKHY-class 75% variant; house-stress 30–40%; > 50%-of-equity escalation toward 100%); excess = equity − Σ m_i·V_i; floor calibrated per §4; provisional (NUM-0001: provisional guardrail) until adequacy. **6: forced liquidation** — shortfall × 1.25 cure, next session; pro-rata primary, largest-first variant, no-notice same-day in stress runs only. **7: dividends** — primary path per §4 (split-adjusted prices + explicit PIT dividend cash; TR only in the validation harness); dividend cash follows the active repayment policy. 8: SPY master calendar, UTC→ET session mapping, split-continuity checks; Track 2's frozen-current-roster anachronism is its labeled survivorship bias.

**8.7 Borrowing-cost accounting** (each component NUM-0001-classified): margin interest (constructed rate series — Estimated); first-$1,000 interest-free tier (a Robinhood Gold benefit — Known per doctrine/terms; modeled only when the Gold cost basis is active); Gold subscription ≈ $5/mo ≈ $60/yr (Estimated — **verify against actual billing at G1**; ~1pp/yr at the current ~$6.1k book, potentially decisive); historical rate = max(floor, Fed Funds + calibrated spread) with flat-5% replication case; stress rates (+300bps, 2× spread, +400bps/6-mo path). **Two cost bases, both reported:** incremental (subscription sunk; free tier active) — headline; fully-allocated (subscription attributed; companion no-free-tier unsubscribed counterfactual at the verified unsubscribed rate). Candidates whose incremental edge is smaller than the basis difference are flagged "subscription-sensitive." Cost-basis variants are post-processing on stored paths — zero simulation runs.

## 9. Run-Budget Ledger (exact; enforced at runtime)

Rules: every `simulate()` call — including failed and discarded runs — appends to `trial_ledger.jsonl` (append-only, config-hash per run); survivor-dependent lines state maxima; **unused budget lapses and may not be reallocated**; any configuration beyond this ledger requires a charter amendment **before** the run. Bootstrap, walk-forward windowing, DSR/PSR, and cost-basis analytics are post-processing on stored daily paths and consume no simulation trials.

**All development-phase simulations end at the development boundary: Track 2 = 2025-06-30, Track 3 = 2020-12-31 (§11). Untouched-test simulations are the only runs that touch later data, and only per §9.7.**

### 9.1 Study A — Track 2 (development window; survivorship-labeled)

| Line | Family / grid | Count |
|---|---|---|
| A2-1 | Controls A-0a, A-0b, A-1 | 3 |
| A2-2 | Fixed ladder A-2…A-5 | 4 |
| A2-3 | A-6 trend × L_hi {1.10, 1.25, 1.50} | 3 |
| A2-4 | A-7 vol × σ_target {10%, 15%} × L_max {1.25, 1.50} × source {account, benchmark} | 8 |
| A2-5 | A-8 staged pullback (fixed schedule) | 1 |
| A2-6 | A-9 crash-only × L* {1.25, 1.50} | 2 |
| A2-7 | A-10 regime × L_hi {1.10, 1.25} | 2 |
| A2-8 | A-11 trend+vol (surviving grid points only, max) | ≤4 |
| A2-9 | Repayment sub-study: postures {fixed 1.25x, A-0b} × {R1, R2, R3, R4(6%), R4(8%), R5, R6, R8, R9, R-B} | 20 |
| A2-10 | Top-2 repayment policies × ≤4 surviving overlays | ≤8 |
| A2-11 | Recipient variants {ETF-first, maintenance-aware} × ≤4 survivors | ≤8 |
| | **Subtotal** | **≤63** |

### 9.2 Study A — Track 3 (development window; mechanics only)

| Line | Content | Count |
|---|---|---|
| A3-1 | Base grid (23) × books {SPY, QQQ} | 46 |
| A3-2 | Repayment sub-study (20), SPY book only | 20 |
| | **Subtotal** | **≤66** |

### 9.3 Study A survivor sensitivities (Track 2, development window)

| Line | Sensitivity | Count |
|---|---|---|
| S-1 | Open-of-day fills × (≤4 survivors + 2 controls) | ≤6 |
| S-2 | Borrowing-cost stress {+300bps, 2× spread} × (≤4 survivors + A-1) | ≤10 |
| S-3 | Deposit cadence {pause, halved, withdrawal} × ≤4 survivors | ≤12 |
| S-4 | Dividend pay-date lag (+30d) × (≤4 survivors + A-1) | ≤5 |
| S-5 | Cost bases | 0 (post-processing) |
| | **Subtotal** | **≤33** |

### 9.4 Study B (Track 2, development window)

| Line | Family | Count |
|---|---|---|
| B-1L | B-0 baseline | 1 |
| B-2L | B-1 tier multipliers ({T1, T2, band} × {0.8, 1.2}) | 6 |
| B-3L | B-2 ETF sleeve {10%, 13%} | 2 |
| B-4L | B-2 crypto sleeve {5%, 15%} — conditional on crypto outcome (a); lapses under (b) | ≤2 |
| B-5L | B-3 cluster-constrained reallocation {75%, 50% of caps} | 2 |
| B-6L | B-4 concentration reductions | 2 |
| B-7L | B-5 nominal budgets {110%, 120%} | 2 |
| B-8L | B-6 vol-aware / equal-risk comparators | 2 |
| B-9L | Open-fill sensitivity × ≤3 survivors | ≤3 |
| | **Subtotal** | **≤22** |

### 9.5 Study C (development window)

| Line | Content | Count |
|---|---|---|
| C-1 | ≤2 surviving overlays × (≤2 surviving structures + B-0) | ≤6 |

### 9.6 Stress suite (development-window and synthetic data only; subjects: ≤6 finalists + controls A-1, A-0b = ≤8)

| Line | Category | Scenarios | Count |
|---|---|---|---|
| ST-M | Mandatory survivability (§12A) | 2008, 2018, 2020 Track 3 replays (all ≤ 2020-12-31, inside the Track 3 development window); +400bps/6-mo rate path; conservative maintenance escalation; overnight gaps −7/−13/−20%; slow bear −35%/18mo — 9 scenarios | 9 × ≤8 = **≤72** |
| ST-D | Catastrophic boundary diagnostics (§12B) | synthetic −65%; doubled maintenance; concatenated worst-decile blocks; combined gap+rate+maintenance — 4 scenarios | 4 × ≤6 = **≤24** |
| | **Subtotal** | | **≤96** |

### 9.7 Untouched-test evaluations (the only simulations permitted past the development boundaries; run only after the G3 candidate freeze)

| Line | Content | Count |
|---|---|---|
| U-1 | ≤2 Study A finalists × {Track 2 roster, Track 3 SPY, Track 3 QQQ} | ≤6 |
| U-2 | ≤2 Study B finalists × Track 2 | ≤2 |
| U-3 | ≤2 Study C finalists × Track 2 | ≤2 |
| | **Subtotal (hard)** | **≤10** |

### 9.8 Study D — zero historical simulations (prospective-shadow only; shadow-replay counterfactuals are outside this ledger and so labeled)

### 9.9 Grand total vs ceiling

| Block | Max |
|---|---|
| Enumerated development configurations (9.1–9.6) | **286** |
| Untouched-test simulations (9.7) | **10** |
| Data-correction-only reserve (never for new arms/parameters; every use logged with cause) | **4** |
| **Hard program ceiling (charter-pinned)** | **300** |

Unused untouched-test and correction capacity **lapses and cannot be reallocated**. No silent post-selection flexibility exists: every degree of freedom is a ledger line, and the runtime ledger enforces the ceiling.

## 10. Historical-Data and Bias Controls

Three tracks strictly separated; no pooled statistics. **No same-day lookahead:** signal(t−1) → execute(t), enforced structurally (signal arrays shifted before the loop) and by test. Track 2's frozen-current-targets anachronism disclosed; arm-relative claims only. Benchmarks: SPY/QQQ total-return used *as benchmarks only* (their sanctioned validation role) and A-1; risk-free series for Sharpe/Sortino with a disclosed fallback band. Maintenance-regime-change reruns per §9.6. Cash-flow realism per §9.3. Production gates live except the pass-through earnings gate. Git-reconstructed history only in Track 1 and proxy calibration, horizon disclosed.

## 11. Anti-Overfitting Requirements and Untouched-Test Isolation

`pre_registration.yaml` — frozen before any simulation run, filed and hash-pinned **in the same G0 filing PR as this protocol and the charter** — contains: the exact §5/§6 families (no mid-program additions); the exact §9 grids and ledger; the 300 ceiling; §7 metrics/thresholds; the periods and isolation rules below; walk-forward, plateau, bootstrap, and DSR specifications; rejection criteria; the assumptions registry (Known/Estimated/Hypothetical + NUM-0001 classes).

**Periods:**
- Track 2: train 2021-06-01 → 2024-06-30; validation 2024-07-01 → **2025-06-30 (development boundary)**; untouched test 2025-07-01 → run date.
- Track 3: train 1999-01-01 → 2015-12-31; validation 2016-01-01 → **2020-12-31 (development boundary)**; untouched test 2021-01-01 → run date. 2008 is deliberately in train (crisis mechanics inform design; the untouched period tests generalization, not crisis memory).

**Untouched-test isolation (structural, not procedural):**
1. Development, validation, parameter-stability, bootstrap-selection, and G3 reporting code **cannot read, simulate, store, display, or summarize untouched-period data**. The research data loader serves development mode by default and physically truncates all series at the development boundary; untouched-mode loading requires an explicit flag that is legal only inside the G4 runner, enforced by test (§14 T-U1).
2. Every development-phase `simulate()` call ends at the development boundary — walk-forward folds are evaluation windows over stored *development-period* paths only (valid because no in-simulation parameter fitting occurs; grids are pre-registered).
3. **Candidate freeze:** before any untouched run, finalist identities and their full configuration hashes are frozen in append-only `candidate_freeze.yaml` — at most **2 Study A finalists, 2 Study B finalists, 2 Study C finalists**. The freeze is itself hash-logged in `trial_ledger.jsonl`.
4. Only after the G3 candidate freeze may G4 run the untouched periods. **Each untouched evaluation is an explicit `simulate()` call and counts toward the 300-run ceiling** (ledger §9.7, ≤10 runs).
5. Untouched-period outputs cannot be regenerated with modified candidates: any change to a frozen candidate's configuration after the freeze voids its untouched result and requires a **charter amendment** before any further untouched-period run.
6. The untouched test is spent exactly once; its expenditure is logged.

**Validation requirements (all pre-registered):** expanding-window walk-forward (6-month steps; retention: sign + ≥50% of full-development edge in ≥70% of folds); regime-coverage rule (single-regime edges labeled regime-conditional, not robust); **neighboring-parameter plateau rule — isolated sharp optima without a stable plateau are rejected outright**; stationary block bootstrap (mean block 21 trading days, 1,000 resamples) on arm-vs-control daily differentials; deflated Sharpe using the actual disclosed trial count (DSR ≤ 0 at 95% → statistically unsupported regardless of raw gap); full parameter-trial disclosure including failures. **Rejection criteria (any one suffices):** gate failure; plateau failure; walk-forward failure; DSR ≤ 0; edge vanishes net of financing; edge vanishes on the fully-allocated cost basis while the Gold subscription is not independently justified; edge depends on uninterrupted deposits; any forced liquidation in §12A; liquidation-sequencing-variant flip (→ "requires prospective data").

## 12. Stress Testing

### 12A. Mandatory survivability stresses — adoption criteria apply

Historically plausible crash replays (2008 GFC, 2018 Q4, 2020 pandemic — actual Track 3 paths, all inside the Track 3 development window); conservative rate shock (+400bps over 6 months — within the observed 2022 envelope); conservative maintenance escalation (house 30 → 35%, FINRA 4210(g)(8) on — documented-real mechanisms per Phase 7A); overnight gaps −7/−13/−20% (within observed US single-session history, 1987 inclusive); slow bear (−35% over 18 months, 2000–02-shaped). **Pass requirement (feeds G3/G4): zero forced-liquidation events, no proxy-floor breach lasting > 5 sessions, severe-impairment ceiling respected — in every §12A scenario.**

### 12B. Catastrophic boundary diagnostics — reveal failure boundaries; not automatically disqualifying

Synthetic −65% index decline; doubled maintenance requirements mid-crash; concatenated worst-decile bootstrap blocks; combined beyond-history shock (gap + rate spike + maintenance escalation). Output: failure-boundary maps (the level at which each candidate — and the current posture, and A-1 — fails; impairment depth; liquidation-cascade profile). **These do not automatically disqualify a candidate unless the principal explicitly adopts a §12B scenario as a mandatory standard** (a one-line charter amendment).

### Boundary justification

The mandatory set contains only events inside the historical-plausibility envelope — each magnitude/speed/mechanism has actually occurred in US markets, or (maintenance escalation) is a documented broker/regulatory mechanism confirmed real by Phase 7A. MARGIN_DOCTRINE's survivability definition — hold through a *realistic historical* stress without forced, capital-destroying liquidation — makes exactly this set the adoption bar. The diagnostic set is beyond-history combinations of unknown joint probability; requiring survival there would disqualify essentially every levered configuration *including the currently governed 1.8x posture itself*, converting an unbounded tail standard into a de facto 1.00x mandate — a doctrine change reserved to the principal, made knowingly via the §12B maps, never by a stress-suite default.

## 13. Implementation Architecture, Modules, and Artifacts

Principles: extend, don't fork (no third simulator); additive and output-neutral when unconsumed; zero import coupling with `allocate.py`/`margin_state.py` in either direction; read-only against production files; research writes only under its own directories.

```
margin_simulation.py                       # additive: maintenance proxy + forced liquidation;
                                           #   variable-rate interest; dividend-cash ledger input;
                                           #   generalized pre_trade leverage-target hook
research/margin_target_study/
  PROTOCOL_V2.md                           # this document (hash-pinned in the charter)
  pre_registration.yaml                    # frozen; filed in the same G0 PR; hash-pinned in the charter
  data_manifest.yaml                       # G1 artifact: source, acquisition ts, coverage,
                                           #   transformations, hashes, validation, limitations
  assumptions_ledger.yaml                  # Known/Estimated/Hypothetical + NUM-0001 classes
  trial_ledger.jsonl                       # append-only runtime run ledger (config-hash per run)
  candidate_freeze.yaml                    # append-only G3 finalist freeze (≤2/≤2/≤2 + config hashes)
  intelligence_flag_events.yaml            # append-only, human-authored, source-pinned (§6)
  overlay_lib.py / repayment_lib.py / maintenance_lib.py / dividend_ledger.py
  target_variants.py / data_acquisition.py / validation_lib.py / shadow_replay.py
  run_study_a.py / run_study_b.py / run_study_c.py / run_stress_suite.py
  results/                                 # config-hash-named JSON + reports
```

Of these, **only `PROTOCOL_V2.md` and `pre_registration.yaml` carry substantive content in the G0 filing PR**; every other artifact is authorized-future and is created only during its own stage (G1+), never fabricated to populate the filing. Repository touchpoints beyond the research directory: `margin_simulation.py` additive extensions + tests (S2 PRs); backlog-item-5 logging (separate future authorization); nothing else. Deliverable documents: study reports A/B/C, stress report (12A/12B separated), `FINAL_PARETO_AND_CLASSIFICATION.md` (Q6/Q7 classification + failure-boundary maps), quarterly shadow reports.

## 14. Test Plan

Carried from the existing repo conventions plus program-specific proofs:
- **T-1** engine regression: Phase 3 Test A/B and Model B/C numbers reproduce exactly (legacy configuration) before any new result is accepted.
- **T-2** structural no-lookahead: perturbing day-t data cannot change day-t decisions.
- **T-3** maintenance mechanic: m_i schedules, >50%-of-equity escalation, cure sizing, both sequencing variants; property — liquidation never increases leverage.
- **T-4** overlay purity: pure functions of t−1 state; leverage targets always within [1.0, 1.8].
- **T-5** repayment invariants: cures first; no policy borrows; R2 routing (dividend cash reduces debt XOR reinvests, never both).
- **T-6** Study B: programmatic TGT-0001 ex-ante cluster check on every config; no per-ticker mutation outside the declared transformation.
- **T-7** validation lib: seeded bootstrap reproducibility; DSR worked examples; fold boundaries exact.
- **T-8** isolation: import-graph (research ↔ production barred) and write-path (research writes only under its own dirs).
- **T-9** ledger enforcement: every `simulate()` appends to `trial_ledger.jsonl`; ceiling enforced at runtime; reserve uses require a logged cause.
- **T-D1** dividend uniqueness: each (ticker, ex-date) credits exactly once (duplicate-injection test).
- **T-D2** primary-path purity: primary prices are split-adjusted only (expected TR divergence must exist for known payers).
- **T-D3** reconciliation: buy-and-hold on the primary path (dividends reinvested) matches the TR path within ±0.3pp/yr per ticker-portfolio; failure blocks G1. The only sanctioned TR use.
- **T-D4** structural bar: simulation runners and `dividend_ledger.py` cannot reference the TR namespace; only `validation_lib.py` may. TR-plus-dividend-cash double-counting is impossible by construction.
- **T-D5** repayment routing under R2 (see T-5).
- **T-C1** crypto (conditional on outcome (a)): calendar mapping (last crypto close ≤ equity close; no future-bar leakage); coverage/gap validation.
- **T-U1** untouched isolation: development-mode loader physically truncates at the boundary; untouched-mode flag is rejected outside the G4 runner; G3 report generators fail on any untouched-period timestamp in their inputs.
- **T-U2** candidate freeze: `candidate_freeze.yaml` is append-only (mutation attempts fail); untouched runner refuses any config whose hash is not in the freeze; post-freeze config changes void the candidate (runner refuses reruns absent a charter-amendment marker).
- **T-S1** Study D: no veto path can increase leverage, touch a recipient, or modify a target; flag events with post-dated authorship rejected; research code has no write path to `intelligence/`.

## 15. Computational Requirements

≤ 300 daily-loop simulations over ≤ 1,283 (Track 2 dev) / ~5,500 (Track 3 dev) days ≈ minutes-to-low-hours on a laptop; bootstrap and analytics ≈ tens of minutes; total **< 3 CPU-hours**; no GPU/cloud; no dependencies beyond `requirements.txt`; network only for the one-time cached, manifest-recorded data acquisition (G1).

## 16. Shadow-Mode Design

Batch retrospective replay, never a live indicator: real state accumulates via `performance_log.csv`/`holdings.yaml` syncs, upgraded by backlog-item-5 logging (separate authorization); `shadow_replay.py` runs only at pre-registered quarterly evaluation points (or on principal demand), computes retrospectively what each frozen candidate would have recommended over the logged past, and writes a dated hypothetical-labeled report. Never invoked by `allocate.py`; never daily; never framed as "borrow now"; places no orders; modifies no holdings, targets, tiers, margin policy, or allocator output. Study D joins shadow replay via `intelligence_flag_events.yaml` (§6): each quarterly replay evaluates the three semantics counterfactually.

**Shadow completion gate — both required:**
1. **Minimum elapsed observation:** ≥ 2 quarterly evaluations spanning ≥ 6 months of logged real data (necessary, never sufficient) and proxy-calibration adequacy reached.
2. **Minimum qualifying event counts** per candidate class:

| Class | Qualifying events required |
|---|---|
| Conditional deployment (trend/regime/vol) | ≥5 deploy-or-reduce transitions AND ≥2 complete deploy→reduce cycles |
| Episodic deployment (staged pullback, crash-only) | ≥3 qualifying drawdown-trigger episodes — may take years; the candidate remains "insufficient evidence" indefinitely until they occur (accepted outcome) |
| Repayment rules (R1–R6, R8–R9) | ≥5 rule-trigger events AND ≥10 valid-inaction hold observations |
| Intelligence veto (Study D) | ≥5 veto events with resolved outcomes AND ≥2 non-veto quarters for base rates |

Insufficient events → **"insufficient evidence" — never a pass by elapsed time alone**; the candidate may wait in shadow indefinitely at zero cost. Behavior must also match backtest prediction (no unexplained divergence, no hypothetical breach). Operator behavior is unconstrained during shadow; the fixed posture stays production throughout.

## 17. Limitations

(1) Track 2 survivorship bias — arm-relative claims only. (2) One real bear in the roster development window (2022); Track 3 mitigates mechanics only. (3) Proprietary broker mechanics (buffer formula, house maintenance, liquidation sequencing) → proxy-based; sensitive conclusions classified "requires prospective data." (4) Constructed rate series, two anchors. (5) Dividend/benchmark/rate acquisition may be network-blocked; degraded fallback weakens return accounting and R2 and is a G1 disclosure item. (6) Track 1 historical depth ~2 weeks; genuine point-in-time evidence is prospective. (7) Daily bars only — overnight-gap scenarios bound, not resolve, intraday dynamics. (8) After-tax rankings indicative only (Phase 6A machinery reused as sensitivity; real basis/rates unknown). (9) The behavioral value of the simple fixed posture is real and unquantifiable by TWR; stated, not modeled. (10) Crypto conclusions exist only under validated PIT crypto data, else explicitly out of scope. (11) Study D has no historical evidence by construction; entirely prospective and event-count-gated. (12) Small-book scale effects (Gold subscription, $1,000 free tier are proportionally large at ~$6k net equity); scale sensitivity disclosed.

## 18. Go/No-Go Gates

| Gate | Question | Go criterion | On NO-GO |
|---|---|---|---|
| **G0** | Charter filed with this protocol + frozen `pre_registration.yaml` in one PR, hashes pinned; principal merges | Merged; committed-blob hashes verify | Program does not exist |
| **G1** | Data adequacy: bars verified; dividend ledger acquired, T-D3 passes; benchmarks/risk-free/rate series acquired; crypto (a)/(b) decided and recorded; costs verified; `data_manifest.yaml` complete | All pass, or degraded-mode disclosures explicitly accepted | Pause; report blockers |
| **G2** | Engine extensions merged (own PRs); full suite green; T-1 anchors exact; T-D1–T-D5, T-U1/T-U2 pass | All pass | No simulation runs |
| **G3** | Development-window verdicts: candidate ≥1.0pp net TWR (incremental basis), MaxDD ≤ +1.0pp, zero §12A liquidations, plateau + walk-forward + DSR pass; **finalists (≤2/≤2/≤2) frozen in `candidate_freeze.yaml`** | Freeze recorded → G4 | Honest null: fixed posture stands; skip to G6 |
| **G4** | Untouched-test evaluations (≤10 ledger runs, frozen candidates only): sign + ≥50% edge holds, §12A-grade behavior on the test period | Yes | Candidate reclassified unsupported |
| **G5** | Q6/Q7 classification report (historically-supported vs requires-prospective-shadow; mandatory for proxy-sensitive, asset-eligibility, sequencing-sensitive, all Study D, crypto-conditional) + §12B failure-boundary map | Accepted by principal | Revise; no adoption path opens |
| **G6** | Shadow authorization (backlog-item-5 logging + quarterly replays + Study D flag workflow) — worth authorizing even on a null | Accepted ADR | Program ends at the historical report |
| **G7** | Shadow completion per §16 (elapsed AND event counts AND prediction-consistent) | Candidate may be *proposed*; insufficient events → "insufficient evidence" | Extend or drop |
| **G8** | Adoption: own future governance decision, full evidentiary bar, TGT-0001 disclosure for any target change, inside the unchanged 1.8x/30% limits; Study D additionally needs PI-side governance | — | Fixed posture continues — a valid, pre-legitimized outcome |

## 19. Staged Implementation Plan

S0 charter filing (this PR) → G0. S1 data acquisition + validation + manifest → G1. S2 engine/lib/test PRs (≤3, narrow, individually reviewed) → G2. S3 Studies A/B development-window runs + trial ledger + interim reports → G3 (candidate freeze). S4 Study C + §12A/§12B on finalists + untouched-test evaluations → G4. S5 final Pareto + classification + boundary maps → G5. S6 shadow authorization decision → G6. S7 shadow quarters until §16 minimums → G7. S8 adoption proposals, if any, each its own governance decision → G8. The program can end honestly at G3, G4, G5, or G7 with the fixed posture intact — pre-declared legitimate and useful.

---

*All simulated results produced under this protocol are hypothetical. They do not represent actual trading, are not a recommendation, and authorize no production change.*
