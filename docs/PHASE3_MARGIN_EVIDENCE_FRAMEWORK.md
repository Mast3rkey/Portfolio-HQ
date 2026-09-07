# Phase 3: Margin Evidence Framework — Specification

_2026-07-17 · Documentation only. No production code changes. No backtests run. This document specifies what evidence Phase 3 will gather and how, so that when each backtest is actually run it follows the same pre-committed discipline as every prior backtest in this repo (`rung_backtest.md`, `regime_backtest.md`, `trend_backtest.md`, `weight_backtest.md`, `trim_backtest.md`, `t1t2_trim_backtest.md`) instead of being designed after the fact to fit a result._

## Why this document exists

Phase 2 built the margin risk-governance machinery (`margin_state.py`, integrated into `allocate.py` in Phase 2D) with every tunable threshold left `null` — `CLAUDE.md`'s standing rule is "never guess/default a numeric parameter without backtest evidence." `docs/PHASE2_IMPLEMENTATION_PLAN.md` §8 named four future backtests in one paragraph each as placeholders. This document is the full specification for those four, upgraded to the same rigor as the repo's existing backtest reports, plus the data-availability and output-language constraints that keep the results honest given this account's real, short, largely-undocumented margin history (`docs/MARGIN_DATA_INVENTORY.md`, `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`).

Nothing here is implemented. This is the spec Phase 3A+ implementation work will be built against, and the bar each backtest must clear before its verdict is written into `CLAUDE.md`'s Decisions Log.

---

## 1. The four questions

Each question below states: the question, why it matters, what a verdict would gate, and the pre-committed decision rule that will apply before any test runs (per the repo's standing backtest discipline — the threshold is fixed now, not after seeing results).

### A. Margin drag test

**Question:** Would this account's actual strategy (current tier weights, gates, trims) have performed better, on a risk-adjusted basis, unlevered versus at its current/allowed leverage?

**Why it matters:** This is the foundational question the entire Margin Intelligence Engine exists to eventually answer with evidence instead of doctrine alone. `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md` already established that this account's *real* leverage history (3 recorded days, 1.622x falling to 1.273x, never near the 1.8x cap) is too short and too monotonic to answer this from real data — this test is necessarily a **hypothetical simulation** (Track 2 pattern: real historical prices, 2021-2026, `data/backtest/*.json`, simulated account, simulated deposit cadence, simulated leverage policy), not a claim about what this account's real history would have shown.

**What it gates:** Whether margin is worth carrying at all as a structural policy (waterfall tiers 2-4 in the repayment framework), separate from the already-settled question of whether the *cap* is safe (that's Test B).

**Pre-committed decision rule:** State the TWR and MaxDD threshold (e.g. the repo's standing 1.0pp TWR / 1.0pp MaxDD-tolerance pattern from `trim_backtest.md` and `t1t2_trim_backtest.md`) *before* running any arm. A leverage arm that wins TWR but breaches the MaxDD tolerance is treated the same way `trim_backtest.md` treated its never-trim control: a real number, honestly reported, but disqualified from being adopted as policy on leverage-under-forced-liquidation grounds — same reasoning already applied to the account's real ~1.44x-1.62x range in `t1t2_trim_backtest.md`'s NVDA decomposition.

### B. Sustainability test

**Question:** At what leverage levels does the strategy survive its own worst historical drawdowns without breaching the 30% buffer floor or being forced into liquidation at the bottom?

**Why it matters:** The 1.8x leverage cap is a **doctrine decision, not a backtest verdict** (`CLAUDE.md` Decisions Log, "Margin doctrine revised") — explicitly stated as fixed and not up for backtest-driven relitigation on its own. This test does not re-litigate the cap. It answers a narrower, legitimate question: given the cap is fixed at 1.8x, what is the actual survival margin at that level versus lower levels, using the worst real drawdowns available in the historical price data (2021-2022 bear stretch, per every prior backtest's stated sample-size caveat)?

**What it gates:** `targets.yaml`'s future `states.caution.leverage_fraction_of_cap` and `states.restricted.leverage_fraction_of_cap` thresholds (currently `null` in the Phase 2 schema) — i.e., how far below the hard 1.8x ceiling the CAUTION/RESTRICTED soft-warning states should sit. Does **not** gate the 1.8x cap itself.

**Pre-committed decision rule:** Sweep leverage 1.2x-2.0x (the range already named in `PHASE2_IMPLEMENTATION_PLAN.md` §8) against the account's own known worst-case single-name decomposition pattern (`t1t2_trim_backtest.md`'s NVDA -66.4% peak-to-trough at 2.14x target is the existing precedent for "how bad can a real position's own drawdown get") rather than only portfolio-level MaxDD, because portfolio-level MaxDD already proved (in that same document) too smooth to surface a leverage-critical single-name event.

### C. Repayment policy test

**Question:** When does paying down margin debt improve risk-adjusted outcomes versus maintaining current exposure?

**Why it matters:** The repayment waterfall framework (`PHASE2_IMPLEMENTATION_PLAN.md` §6, four tiers: protect against forced liquidation → restore acceptable leverage → maintain strategic allocation → repay remaining excess debt) has tiers 2 and 4 gated on this test by name. Tier 1 (protect against forced liquidation) is not gated — it's the same doctrine-level hard rule as the buffer floor itself, non-negotiable regardless of this test's outcome.

**What it gates:** Whether tiers 2 and 4 of the waterfall are ever implemented as automatic recommendations, and their specific `redirect_fraction_*` values (currently `null`).

**Pre-committed decision rule:** Three named repayment models to compare (already specified in `PHASE2_IMPLEMENTATION_PLAN.md` §8 item 3): **Model A** (permanent leverage, never repay unless forced by a hard breach), **Model B** (profit harvesting — hold leverage at a target ratio, any excess above it pays down debt), **Model C** (risk reset — proactively reduce debt after gains, volatility spikes, or concentration increases, not waiting for a breach). Compare on TWR + MaxDD + a new metric this test must define precisely before running: **time spent within X% of the buffer floor** (a proxy for "how close to forced liquidation did this policy run, independent of whether it actually breached").

### D. Concentration interaction test

**Question:** Does `concentration_risk_score()` tightening the *effective* leverage capacity (not just the CAUTION/RESTRICTED display threshold) improve MaxDD without materially costing TWR?

**Why it matters:** `margin_state.py`'s concentration-tightening mechanism currently only ever affects which risk *state* is displayed (`docs/PHASE2B_REVIEW.md`; Phase 2D integration is display-only, confirmed in the just-completed integration). This test asks whether concentration should ever be allowed to affect *real deployable margin capacity* — a materially bigger change than a display label, and explicitly not yet decided.

**What it gates:** Whether `concentration_adjustment` ever moves from a display-only signal to something `margin_capacity()` itself consults. This is the single biggest-blast-radius decision in the whole framework, since `margin_capacity()` is the one function in `allocate.py` this entire project has treated as untouchable throughout Phase 2 (explicitly named "sole authority," never modified). A GO verdict here would be the first time any of this work proposes touching it.

**Pre-committed decision rule:** Given the blast radius, this test needs a *stricter* bar than the standard 1.0pp threshold — propose 2.0pp TWR improvement minimum (double the standard threshold) before even considering a `margin_capacity()` change, on the reasoning that a function this consequential shouldn't move for a marginal win. This number is a proposal in this spec, not yet a committed threshold — confirm before Test D actually runs.

---

## 2. Data requirements

Classified using the same A/B/C scheme `docs/MARGIN_DATA_INVENTORY.md` already established — reproduced and applied specifically to what these four tests need, not re-deriving the inventory itself.

### Available (usable directly)

| Data | Source | Used by |
|---|---|---|
| Historical daily prices, 2021-2026, current 65-ticker roster | `data/backtest/*.json` | A, B, C, D — the simulation substrate for every hypothetical arm |
| Current tier weights, gates, cluster caps, T1/T2 ceiling | `targets.yaml` | A, B, C, D — the strategy being simulated is today's production rules, not a hypothetical strategy |
| 7 real margin debt/buffer sync points | `holdings.yaml` git history, tabulated in `MARGIN_DATA_INVENTORY.md` Table A | Anchors any simulated debt trajectory to the account's real *current* state as the simulation's starting point — does not extend backward |
| Net equity / gross / QQQ / VOO snapshots | `performance_log.csv` | Sanity-checks simulated portfolio value against the account's real, current trajectory where the two overlap (3 real dates) |
| Stated interest rate term (~5% APR, first $1,000 free) | `CLAUDE.md` doctrine | A, C — cost-of-carry assumption for every leveraged arm; the "~" is preserved as an explicit disclosed simplification, not treated as exact |
| Existing backtest infrastructure and discipline pattern | `backtest_common.py` (per the earlier repo audit's dedup work), `reports/*.md` | All four — reuse the existing engine rather than building a parallel one |

### Missing (per `MARGIN_DATA_INVENTORY.md` Category C — reaffirmed here, not re-derived)

| Missing data | Impact on this framework |
|---|---|
| Historical interest expense (no ledger exists) | A, C cannot use *actual* interest paid — must use the disclosed fixed-rate assumption throughout, flagged in every output per §3 below |
| Complete margin timeline (draws/paydowns between the 7 sync points) | Confirms, again, that Test A/B/C cannot be run as a "real historical account" backtest — must be the same hypothetical-forward-simulation pattern as Track 2, not a Track-1-style reality audit |
| Deposits/withdrawals history (only 1 of unknown-many events recorded) | A, C's simulated deposit cadence must be a disclosed, stated assumption (e.g. "$X/month, starting from $0") — cannot reconstruct the account's real deposit pattern |
| Pre-2026-07-13 margin state (~$4,423 figure is prose-only, not data — see `MARGIN_DATA_INVENTORY.md`'s explicit caveat) | No test in this framework may use the ~$4,423 figure as an input; it is unverifiable and excluded per that document's existing ruling |
| Buffer time series between syncs | B's "survives its own worst drawdown" claim about buffer-floor proximity is necessarily about the *simulated* trajectory, not verified against any real intra-period buffer reading |

No new data collection is proposed by this document — `MARGIN_DATA_INVENTORY.md`'s "required future data collection plan" (§ margin_log.csv, cashflow_log.csv, interest-charge log, buffer time series) already covers this and is out of scope for Phase 3 planning specifically.

---

## 3. Acceptable output language

Every one of the four tests, when eventually run, is a **hypothetical simulation using real historical prices**, per the Missing-data findings above — none can be an audit of this account's real margin history, because that history doesn't exist in recoverable form. This section makes the language requirement mechanical, not a style preference, so a future implementation (or a future reviewing session) cannot accidentally overstate a result.

**Prohibited, in any report, log entry, or `CLAUDE.md` Decisions Log write-up produced by this framework:**
- "Margin would have made X%."
- "Leverage improved returns by X%." (stated as fact about this account)
- Any sentence whose grammatical subject is the real account's real history for a period this framework has no data for.

**Required framing, in every result:**
> "Under these assumptions [list them: leverage level, interest rate, deposit cadence, starting capital, repayment rule], a simulated investor following this policy through [date range] historical prices would have experienced [outcome]."

This mirrors, verbatim in spirit, `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md`'s existing "Required output language" section — this framework does not invent a new rule, it extends the one already established for Track 2 to cover Tests A-D specifically, since all four are Track-2-shaped (hypothetical, assumption-driven) rather than Track-1-shaped (real-data audit).

Every report produced under this framework carries an opening banner, matching Track 2's existing pattern:
> **⚠️ Hypothetical, simulated.** This report does not describe this account's real margin history. See §2 for what real data exists and what doesn't.

---

## 4. Benchmark framework

All four tests share one benchmark set, run against the same historical price data and the same current-production tier weights/gates, so results are comparable across tests without re-deriving benchmarks each time.

1. **Unlevered baseline** — the current strategy (weights, gates, trims, cluster caps, T1/T2 ceiling) with margin permanently unavailable (`leverage_cap = 1.0`, equivalent to `margin_capacity()` always returning 0 allowed). This is the same-shape control as every prior backtest's "current production" baseline arm.
2. **Current allocation** — the strategy exactly as configured today: `leverage_cap = 1.8`, `buffer_floor_pct = 30.0`, margin used opportunistically wherever `plan()`'s existing gap-driven logic would draw it, no explicit repayment policy (matches production's actual current behavior — margin is drawn to fund allocation gaps, never proactively repaid beyond what real Robinhood trims already did).
3. **Fixed leverage variants** — the 1.2x-2.0x sweep named in Test B, each held constant as a hard ceiling substituted for 1.8x, otherwise identical to benchmark 2.
4. **Repayment variants** — Models A/B/C from Test C, each run at the current 1.8x cap, varying only the repayment behavior once debt exists.

Every benchmark, including "current allocation," is itself a simulated hypothetical run through historical price data per §3 — "current allocation" here does *not* mean this account's real historical performance (that data doesn't exist for a comparable period), it means today's production ruleset run forward through the same historical window as every other benchmark, so the comparison is apples-to-apples.

---

## 5. What cannot be tested honestly

Named explicitly, per this session's standing practice of stating hard walls rather than letting a future session quietly attempt to work around them (matching `MARGIN_DATA_INVENTORY.md` Category C's own framing):

- **Whether margin has *actually* helped or hurt this specific account, historically.** Already answered by `docs/TRACK1_HISTORICAL_REALITY_AUDIT.md`: the real borrowing path doesn't exist to evaluate. Tests A-D cannot change this — they answer "what would a policy have done to a simulated account," never "what did margin do to *this* account."
- **Real interest cost sensitivity.** Because no interest ledger exists (Category C), every test's interest assumption is a single disclosed constant (~5% APR). A "how sensitive is the verdict to the actual rate this account paid" question is unanswerable — there is no actual-rate data to check the assumption against, only the doctrine-stated term.
- **Real deposit-cadence sensitivity.** Same shape of gap — deposits are simulated on a disclosed, invented schedule (e.g. "$2,000/month" per the Track 2 assumptions table), not this account's real, irregular, unlogged deposit history. A test cannot claim its verdict would hold under "this account's actual deposit pattern," because that pattern isn't recorded.
- **Any conclusion about whether *this account's specific past margin draws* (the ~$4,423 pre-2026-07-13 debt, or any of the 7 recorded sync-point deltas) were good or bad decisions at the time.** The framework explicitly cannot reconstruct what alternative was available at each of those moments (buying power, prices, targets in force at the time) with enough fidelity to grade a real historical decision. This is a permanent gap, not a "needs more data collection" gap — those decisions are in the past and cannot be re-observed.
- **Behavioral effects.** Same caveat every prior backtest in this repo has carried forward (`regime_backtest.md`'s "forced pause reduces panic-sell risk" note, `t1t2_trim_backtest.md`'s framing) — a TWR/MaxDD backtest cannot price the psychological effect of carrying leverage through a drawdown, only the numerical outcome. Tests A-D will report numbers; they will not claim those numbers capture the full decision-relevant picture.

---

## 6. Sequencing and gating

Consistent with every implementation phase so far in this project:

- **This document (Phase 3A)** — specification only. No code, no data pulled, no arms run. Requires approval before Phase 3B.
- **Phase 3B** — build/extend the simulation harness (likely extending `backtest_common.py`, matching the existing dedup work from the earlier repo cleanup) to support a leverage-and-repayment-aware simulated account. No verdicts, no threshold decisions — infrastructure only.
- **Phase 3C** — run Test A only, first, since B/C/D's thresholds and scope depend on A's outcome in each test's own "what it gates" section above (e.g., if A concludes margin isn't worth carrying as policy, B's leverage sweep still matters for the cap's existing safety margin, but C's repayment tiers 2/4 become moot). Each subsequent test gets its own explicit go/no-go check against this dependency chain before running, not a batch of four run simultaneously.
- Each test, when run, produces its own `reports/margin_*.md` (matching the existing `rung_backtest.md`/`regime_backtest.md`/etc. naming convention), a `decision_log.yaml` entry, and a `CLAUDE.md` Decisions Log entry — same three-artifact pattern as every closed backtest question in this repo.
- **Hard gate, stated explicitly, matching Phase 2's pattern:** no `targets.yaml` schema value currently `null` (leverage_cap and buffer_floor_pct stay as they are — they're doctrine, not gated by this framework) gets filled in until its specific gating test (named in §1 above) has run and produced a verdict under this document's discipline.

## What this document deliberately does not do

- Does not run any test. No arms, no numbers, no verdicts.
- Does not modify `backtest_common.py`, `targets.yaml`, `margin_state.py`, or `allocate.py`.
- Does not pick the final decision-rule thresholds for Tests A-C (states the repo's standing 1.0pp/1.0pp pattern as the default to carry forward) or finalize Test D's proposed 2.0pp bar — both need explicit confirmation before Phase 3C, not implicit adoption by this spec.
- Does not decide whether Test D ever proceeds — flagged as the framework's highest-blast-radius question, deliberately sequenced last and gated hardest.
- Does not begin the `margin_log.csv`/`cashflow_log.csv`/interest-log/buffer-time-series data collection plan `MARGIN_DATA_INVENTORY.md` already specified — that plan exists independently and isn't re-scoped here.

Stopping here. No code, no data pulled, no backtests run. Awaiting approval before Phase 3B.
