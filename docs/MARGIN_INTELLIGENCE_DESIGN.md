# Margin Intelligence Engine — Design Document

_2026-07-17 · Planning/design pass only. No code changed. Written after inspecting `CLAUDE.md` (doctrine + Decisions Log), `allocate.py`'s `margin_capacity()`, `targets.yaml`'s `margin:` block, `holdings.yaml`'s live margin state, the six `backtest_*.py` scripts, and `test_margin.py` (12 tests, all passing)._

---

## 0. What already exists (inspection summary)

**`margin_capacity()`** (`allocate.py:144-157`) is the entire current margin engine — 14 lines:
```python
def margin_capacity(gross, margin_debt, cash, leverage_cap, buffer_pct, buffer_floor_pct, margin_requested):
    net_equity = gross - margin_debt
    if buffer_pct is not None and buffer_pct < buffer_floor_pct:
        return net_equity, 0.0, True, "buffer < floor — forced de-lever"
    max_by_leverage = max(0.0, leverage_cap * (net_equity + cash) - gross - cash)
    allowed = min(margin_requested, max_by_leverage)
    ...
```
Two rules, both hard cutoffs, no taper, no discretion: (1) buffer below floor → zero margin allowed, full stop; (2) otherwise, clip the requested margin to whatever keeps gross/net-equity at or under `leverage_cap`. That's the entire "intelligence" today — a static ceiling and a static floor.

**`targets.yaml`'s `margin:` block:**
```yaml
margin:
  leverage_cap: 1.8
  buffer_floor_pct: 30.0
```
Two numbers. No repayment logic, no state machine, no history-aware behavior.

**`holdings.yaml`'s live margin state** (current, synced 2026-07-15): `debt: 1628.64`, `buffer_pct: 61.77`, `synced_at: 2026-07-15`. Current leverage ≈1.27x against the 1.8x cap — well inside every existing threshold.

**`test_margin.py`**: 12 tests. 7 cover `margin_capacity()` directly (leverage clipping, buffer-floor hard cutoff at/below the exact boundary, unsynced-buffer behavior, cash growing headroom, already-over-cap). 5 cover cluster-cap and the T1/T2 ceiling's mechanical trim inside `plan()`. Zero tests exist for repayment — there is no repayment logic to test.

**The backtest framework** (`backtest_regime.py`, `backtest_trend.py`, `backtest_trims.py`, `backtest_weights.py`, `backtest_rungs.py`, `backtest_t1t2_trim.py`) has a consistent, load-bearing discipline this design must inherit exactly:
- A **pre-committed decision rule**, fixed and stated in the file *before* any result is computed (usually "adopt only if it beats current by >1.0pp annualized TWR").
- A **MaxDD tolerance** alongside the TWR threshold where the question has a leverage/concentration dimension (`t1t2_trim_backtest.md` set this precedent: "a TWR win bought with a materially deeper drawdown doesn't count").
- **One test, one verdict, no variant mining.** Closed questions carry "no re-runs without a new regime in the data."
- Verdicts are **never auto-applied** — a human reads the report, hand-edits `targets.yaml`, writes a Decisions Log entry.

**The Decisions Log entry that governs everything below** (2026-07-13, "Margin doctrine revised"):
> "Formally allowed going forward within a fixed 1.8x structural leverage cap and 30% buffer floor... **Explicitly rejected: any margin-timing model** ('borrow more when conditions look good') — same category as the band-overlay backtest and the multi-timeframe/Fable-5 research proposals... **Leverage amplifies whatever edge already exists (or doesn't); it is not itself a source of edge, and is not backtestable as one.**"

This is the single most important fact this design has to work within. Section 2 below addresses it directly and repeatedly, because several items in the requested task brief conflict with it.

---

## 1. Margin utilization framework

### When should margin be allowed?
Unchanged from current doctrine, because current doctrine is already correct on this question: margin is allowed as **fuel within a fixed structural ceiling**, whenever a deposit/opportunity cycle calls for more buying power than cash alone provides, *and* the projected post-trade leverage stays at or under `leverage_cap`, *and* the projected post-trade buffer stays at or above `buffer_floor_pct`. No new "should we allow it" logic is needed here — `margin_capacity()`'s existing two checks already answer this correctly and are staying as-is.

### When should margin be reduced?
This is a genuinely new question the current system doesn't answer — today, margin is reduced only when the buffer floor is *already* breached (reactive, forced). The Margin Intelligence Engine's real job is answering this *before* it's forced:
- **Mechanically, on a schedule tied to leverage relative to the cap**, not on a market view. E.g., "if leverage exceeds some fraction of the cap for N consecutive syncs, recommend a paydown" — a structural rule, same shape as the buffer floor, not a timing call.
- **Never** in response to "the market looks risky" or "I have a bad feeling" — that's a discretionary/emotional judgment the doctrine (and the task's own "no emotional deployment" instruction) explicitly excludes.

### When should margin be paid down?
Two legitimate, non-timing triggers:
1. **Forced** — buffer below floor. Already exists (`forced_delever` in `margin_capacity()`); Section 4 proposes making the recommendation concrete (a specific dollar amount) rather than just a red flag.
2. **Opportunistic-in-the-mechanical-sense** — when trim proceeds exist anyway (band/spec RSI trims, cluster-cap trims, T1/T2 ceiling trims), a *mechanical* rule can route a portion of those proceeds to debt paydown before redeployment, if leverage is elevated. This is not "pay down margin because the market looks bad" — it's "when cash exists from an already-triggered, already-doctrine-approved trim, and leverage is running hot, prefer debt reduction over redeployment for that dollar." The trigger is trims that already happen for other reasons, not a new market read.

### What signals matter?
Only structural/mechanical account-state signals:
- **Leverage ratio** (gross/net-equity) vs. the fixed cap.
- **Buffer %** (Robinhood-displayed, never derived) vs. the fixed floor.
- **Concentration** (cluster caps, T1/T2 ceiling) — already-existing risk signals that interact with leverage (a concentrated position under leverage is exactly the capital-impairment risk `t1t2_trim_backtest.md` surfaced).
- **Available cash** — mechanical inputs to the deployment math, not a market judgment.
- **Margin debt trend over time** (is leverage drifting up across syncs) — descriptive, feeds the "when to reduce" schedule above.

### What signals are forbidden?
Explicitly, per the standing Decisions Log rejection and the task's own doctrine constraints:
- **Volatility regime** as a "good time to lever up" or "bad time to lever up" signal. (Volatility as an input to a *risk* calculation — e.g., translating a drawdown into an equity-impact estimate the way `t1t2_trim_backtest.md` did for NVDA — is fine; volatility as a *timing trigger for changing leverage* is not.)
- **Market drawdown** as a "buy the dip with borrowed money" trigger. This is literally averaging down, explicitly forbidden by the task brief and structurally identical to the rejected margin-timing model.
- **Valuation opportunities** ("this looks cheap, lever up") — pure predictive/thesis judgment, already excluded system-wide by the Guardrails' "no predictive research, price targets, or opportunity maps."
- **Unrealized gains/losses on existing positions** as a lever-up trigger. Doctrine is explicit on the adjacent case (buffer): "never read a high/rising buffer as a signal to add more leverage: buffer rises mechanically when positions gain value, which is exactly when pro-cyclically levering up... is most dangerous." The same logic applies directly to using unrealized gains themselves as a signal.
- **Regime status** (QQQ vs. 200-EMA) as a margin-draw gate. The existing regime gate was already tested and removed *for cash deployment* on cost grounds; using it to gate margin specifically would be building the same rejected timing mechanism back in through a side door, without even the "it was tested" cover the cash version had — the margin-timing rejection was explicit and never backtested precisely *because* the doctrine holds it isn't a backtestable question (leverage isn't a source of edge to time).

---

## 2. Margin states — redesigned to be risk-only, not opportunity-seeking

The task brief's example states were **Normal / Opportunistic / Defensive / Forced deleveraging**. I'm not implementing this as given — "Opportunistic" as a state name implies a state where the system recommends *increasing* leverage because conditions look favorable, which is precisely the margin-timing model the Decisions Log rejects by name. Renaming or redefining it away from opportunity-seeking is not a cosmetic change; the whole point of a state machine here is that state transitions must only ever point in the risk-reducing direction in response to risk signals, never in the opportunity-seeking direction in response to opportunity signals.

**Proposed replacement — three states, ceiling-and-floor shaped like everything else in this doctrine:**

| State | Objective criteria | System behavior |
|---|---|---|
| **Normal** | Leverage ≤ some inner threshold of the cap (e.g. 80% of `leverage_cap`, i.e. ≤1.44x at the current 1.8x cap) AND buffer comfortably above floor (e.g. ≥1.5× `buffer_floor_pct`, i.e. ≥45%) | No change from current behavior. Margin available up to the cap, buys/trims proceed as normal. |
| **Elevated** | Leverage between the inner threshold and the cap, OR buffer between the floor and the comfort margin above | **Informational only** — shown in every `--review`/`--cash` run, same as the existing margin table, with an explicit note that leverage/buffer is trending toward its limit. No behavior change, no forced action. This is the "watch, don't act" state — consistent with "margin is not a timing tool." |
| **Forced deleveraging** | Buffer < floor (existing `forced_delever` condition, unchanged) | Existing behavior (block all margin-funded buys) **plus** a concrete repayment recommendation (Section 3) instead of just a block message. |

Three states, not four — I deliberately dropped "Defensive" as a fourth distinct state because on inspection it would either (a) duplicate "Elevated" (both are "getting close to a limit, do nothing but watch") or (b) smuggle in exactly the discretionary judgment call ("conditions look risky, reduce proactively before you're forced to") the doctrine excludes. If you want a genuine fourth state, it needs an *objective, mechanical* trigger distinct from leverage/buffer proximity — I don't have one to propose without inventing a new signal, and per the forbidden-signals list above, most of the obvious candidates (volatility, drawdown) are exactly what's excluded.

---

## 3. Margin deployment rules — evaluated against the requested signal list

Going through every signal the task brief asked me to consider:

| Signal | Verdict | Reasoning |
|---|---|---|
| Leverage ratio | **Use** | Already the core mechanism; unchanged. |
| Robinhood buffer % | **Use** | Already the core mechanism; unchanged, never derived. |
| Volatility regime | **Do not use as a deployment trigger.** May use as a *risk-sizing input* (e.g., translating a drawdown into a levered-equity-impact estimate, informational only) — never as a "lever up/down because volatility is low/high" rule. | Forbidden-signal list, Section 1. |
| Market drawdown | **Do not use as a deployment trigger.** | Averaging-down territory; forbidden-signal list. |
| Portfolio concentration | **Use — but only in the risk-reducing direction.** Already partially wired (cluster caps, T1/T2 ceiling); the new piece is letting elevated concentration nudge the *repayment* schedule (Section 4), never the deployment ceiling upward. | Consistent with existing cap mechanics. |
| Available cash | **Use** | Already a mechanical input (`deployable = cash + margin_allowed`); unchanged. |
| Valuation opportunities | **Do not use.** | Forbidden-signal list; also excluded system-wide by the Guardrails. |
| Existing unrealized gains/losses | **Do not use as a lever-up trigger.** May inform which specific positions a mechanical trim touches (already true — trims are per-ticker, not portfolio-wide) — never as a portfolio-level "we're up, lever up" signal. | Forbidden-signal list; direct extension of the existing buffer-rising warning. |

**Net effect:** the deployment *ceiling* logic doesn't change at all from what `margin_capacity()` already does. What's new is entirely on the reduction/repayment side (Section 4) and the informational state display (Section 2). This is a deliberate, doctrine-driven scope narrowing from what the task brief's signal list implied — flagged explicitly here rather than silently narrowed.

---

## 4. Margin repayment framework

This is the genuinely new, doctrine-compatible core of the engine — nothing here conflicts with existing rules, because no repayment logic exists today to conflict with.

**When should profits repay debt?**
Never based on "profits" as a standalone concept (that would be a market-timing/emotional judgment — "we're up, let's delever"). Instead: **when a mechanical trim that was already going to happen for an unrelated reason (RSI overweight, cluster cap, T1/T2 ceiling) generates cash, and leverage is in the Elevated state (Section 2), route a portion of that specific trim's proceeds to debt paydown before the normal gap-fill redeployment.** The trigger is "a trim happened" (already doctrine-approved), not "the market is favorable."

**Should trims automatically prioritize debt reduction?**
Proposed rule: **yes, but only proportionally, and only above the Normal/Elevated boundary.** E.g., if leverage is in the Elevated band, some fraction of trim proceeds (a config value, not derived from a market view) goes to debt paydown before the remainder competes in the normal gap-fill allocation. At leverage in the Normal band, 0% is redirected — full proceeds redeploy as today. This needs backtesting (Section 5, arm 5) before a specific fraction is chosen; do not pick a number without evidence, same standard as every other parameter in this system.

**Should cash flows restore margin capacity?**
Yes, mechanically: a cash deposit already does this today as a side effect (`margin_capacity()`'s `max_by_leverage` grows with `net_equity + cash`) — no new logic needed, just worth stating explicitly as intentional in the doctrine write-up so a future session doesn't "discover" it as an inconsistency the way the T1/T2 ceiling's floor-vs-ceiling gap was discovered.

**How to avoid permanently carrying expensive leverage?**
The real structural fix here isn't a new signal — it's making the "Forced deleveraging" state's response *specific* instead of just a block. Today, `render()` shows "⚠️ FORCED DE-LEVER" with a reason string but no dollar amount. Proposed: compute and display an explicit **recommended paydown amount** — the dollar figure that would restore buffer to some target above the floor (not just barely at it, to avoid immediately re-triggering on the next price wiggle). This is arithmetic on numbers the system already has (gross, debt, buffer), not a new judgment call.

---

## 5. Backtesting requirements — redesigned against doctrine, arm by arm

The task brief requested five backtest arms. Going through each against the margin-timing rejection:

**1. Fixed leverage vs. adaptive leverage — buildable, but "adaptive" must mean mechanical, not discretionary.**
"Adaptive" cannot mean "leverage that changes based on a market read" (rejected). It *can* mean "leverage that changes based on the account's own mechanical state" — e.g., does tapering the effective leverage target as concentration risk rises (informed by the Elevated state in Section 2) perform differently than a flat 1.8x cap regardless of concentration. This is testable without violating doctrine because the input is the account's own risk state, not a market view.
- **Arms:** A (current, flat 1.8x cap) vs. B (cap tapers linearly from 1.8x to some floor as the largest cluster's %-of-book rises toward its cap).
- **Metric bar:** TWR + MaxDD, same 1.0pp/1.0pp precedent as `t1t2_trim_backtest.md`.

**2. No margin vs. controlled margin — buildable, directly answers "does margin help at all."**
- **Arms:** A (no margin ever, cash-only) vs. B (current production: 1.8x cap, 30% floor).
- This is the most fundamental question and hasn't actually been tested — the 2026-07-13 doctrine revision *allowed* margin based on it already existing (post-hoc legitimization, per this session's own external-review discussion), not based on a backtest showing margin helps. Worth running for real evidence, whichever way it comes out.
- **Metric bar:** TWR + MaxDD + worst-case single-position levered-drawdown decomposition (the `t1t2_trim_backtest.md` NVDA-style analysis) — a margin backtest without a tail-risk view is exactly the mistake the trim backtest's leverage override was designed to catch.

**3. Margin only during drawdowns — NOT buildable as specified. Direct conflict.**
This is, by definition, "borrow more when conditions look good [i.e., after a drop, expecting reversion]" — the exact model the Decisions Log names and rejects, and it is functionally indistinguishable from averaging down with borrowed money, which the task's own doctrine constraints separately forbid. **I'm not designing this arm.** If there's a legitimate risk-management question hiding inside this idea (e.g., "does letting margin capacity mechanically restore as prices fall, rather than staying flat, change outcomes" — a structural question, not a timing one), that would need to be posed as its own, differently-shaped question, and should come back as an explicit conversation the way the "investment thesis management" item did in the Phase 1 audit — not built because it appeared on this list.

**4. Margin deployment based on regime — NOT buildable as specified. Direct conflict.**
Same rejection as #3, and additionally: the *cash* version of this exact idea (deploy or hold based on QQQ's 200-EMA) was already tested (`regime_backtest.md`) and dropped for costing 2.56pp/yr. Re-running the identical mechanism on the margin axis wouldn't be new evidence — the doctrine's position on margin timing is that it isn't a backtestable question in the first place (leverage doesn't have its own edge to time), so there's no version of this arm that both (a) tests what's being asked and (b) doesn't just rebuild the rejected mechanism. **Not designing this arm.**

**5. Margin repayment strategies — buildable, and the most valuable arm on the list.**
This is the one item in the original five that's unambiguously in-scope and unambiguously new (Section 4 has no backtested basis for its proposed proportional-redirect rule yet).
- **Arms:** A (current: 100% of trim proceeds redeploy, no debt priority) vs. B (proportional redirect to debt paydown when leverage is Elevated, per Section 4 — test 2-3 fractions, e.g. 25%/50%/75%, as a pre-committed parameter sweep, same style as `trim_backtest.md`'s band-cap/RSI sweep) vs. C (100% of trim proceeds to debt paydown whenever Elevated, the aggressive end).
- **Metric bar:** TWR + MaxDD + a new metric — **time spent in the Elevated/Forced states** (does a repayment rule actually reduce time-at-risk, not just move dollars around) + **interest cost avoided** (debt × ~5% APR × time, a real, quantifiable savings this system hasn't measured before).

**Metrics, across all buildable arms** (per the task brief's request, mapped to what's genuinely computable from this system's data):
- **CAGR / annualized TWR** — existing `twr_annualized()`, reused unchanged.
- **Max drawdown** — existing `max_drawdown()`, reused unchanged.
- **Volatility** — **new**: standard deviation of daily returns, annualized (√252 scaling). Nothing in the repo computes this today (confirmed via grep — no existing Sharpe/volatility helper anywhere in the codebase); this would be a genuinely new, small, pure function alongside `twr_annualized`/`max_drawdown` in `backtest_regime.py`, with its own unit test before use (per the task's "all new financial logic requires tests before integration" instruction).
- **Sharpe ratio** — **new**, built directly on the new volatility function: `(annualized_return − risk_free_rate) / annualized_volatility`. Needs a risk-free-rate constant decided explicitly (not defaulted silently) — propose using 0% for simplicity and disclosing that choice in the report header, the same way every other backtest states its held-constant parameters up front, rather than picking a real T-bill rate that itself becomes an unexamined assumption.
- **Worst-case loss** — the single-name/single-position levered-drawdown decomposition already built for `t1t2_trim_backtest.md` (NVDA's 2.14x/-66.4% analysis), generalized into a reusable function rather than one-off script code.
- **Time underwater** — **new**: count of days the account's value sits below its prior peak, as a fraction of total days. Straightforward given the existing daily-value series every backtest already produces.
- **Leverage exposure** — **new**: the leverage ratio's own time series (not just its max), so a report can show *how often* an arm ran hot vs. just *how hot it got once*.

---

## 6. Integration plan

**Files that will change:**
- `allocate.py` — `margin_capacity()` extended to also return a margin *state* (Section 2) and, when Forced, a concrete repayment dollar amount (Section 4). `plan()`'s trim logic extended to optionally redirect a fraction of trim proceeds to debt paydown, gated by the new state (only if Section 5's backtest supports a specific fraction — do not hardcode one pre-emptively). `render()` extended to show the state and (if Forced) the repayment recommendation.
- `targets.yaml` — new `margin:` sub-keys: state thresholds (the "80% of cap" / "1.5× floor" boundaries from Section 2 — these need their own explicit values, not left implicit in code) and, if Section 5's backtest adopts one, the repayment-redirect fraction.
- `CLAUDE.md` — new Decisions Log entries for every backtest verdict (arms 1, 2, 5), and explicit doctrine lines for the state definitions and repayment rule, in the same style as the T1/T2 ceiling's entry (including, if applicable, the same "this is a doctrine decision, here's exactly what was and wasn't tested" precision that entry required after review).

**New files needed:**
- `backtest_margin_leverage.py` — arms 1 and 2 (adaptive-vs-fixed leverage, no-margin-vs-controlled). Two related questions, one file, matching how `backtest_regime.py` and `backtest_trend.py` are split by *question* not by mechanism.
- `backtest_margin_repayment.py` — arm 5.
- New shared metrics added to `backtest_regime.py` (volatility, Sharpe, time-underwater, leverage-exposure-series) so every backtest script — margin and non-margin alike — can adopt them the same way they already share `twr_annualized`/`max_drawdown`, rather than creating a second parallel metrics module.
- `test_margin_intelligence.py` (or extend `test_margin.py` directly, given it already covers the exact function this extends) — unit tests for the new state-classification logic and the repayment-amount calculation, at the same rigor as the existing 7 `margin_capacity()` tests, before any of this touches `plan()`.

**Test strategy:**
1. Pure-function unit tests first (state classification given leverage/buffer inputs; repayment-amount arithmetic given gross/debt/buffer/target inputs) — deterministic, fast, no live data, same pattern as existing `test_margin.py`.
2. New backtest metric functions (volatility, Sharpe, time-underwater) get their own unit tests against hand-computed small examples *before* being trusted in a real backtest run — this is exactly the class of thing `test_indicators.py`'s RSI-of-flat-series case exists to catch (an intuitive-but-wrong assumption baked into a formula).
3. Backtests run and reviewed (human-in-the-loop, per the framework's standing practice) before any `targets.yaml`/`allocate.py` change is made.
4. `plan()` changes (if any survive the backtests) get integration coverage the same way the T1/T2 ceiling did — a live `--review` run checked against hand-computed expected output before commit.

**Migration steps:**
1. Add new pure functions (state classifier, repayment calculator, new metrics) with tests. No behavior change yet — nothing calls them from `plan()`.
2. Add the two new backtest scripts, run them, get verdicts, write Decisions Log entries.
3. Only then wire adopted verdicts into `plan()`/`render()`/`targets.yaml`, one at a time, each its own commit (matching the Phase 1 cleanup's "small, logically grouped commits" pattern) — repayment logic and state display are independent enough to ship separately rather than as one large change.
4. Update `README.md`'s margin section to describe the new states/repayment behavior once it's live — do not let this drift the way the old README did.

---

## 7. Conflicts with existing doctrine — consolidated

Restating everything flagged inline above in one place, as requested:

1. **The task brief's "Opportunistic" margin state directly contradicts the 2026-07-13 Decisions Log entry rejecting any margin-timing model.** Not implementing it; replaced with a risk-only three-state model (Section 2).
2. **"Volatility regime" and "market drawdown" as deployment signals are forbidden** — both are margin-timing-by-another-name and/or averaging down, which the task's own doctrine constraints separately prohibit. Redirected to risk-sizing-only use (Section 1, Section 3).
3. **"Valuation opportunities" and "existing unrealized gains/losses" as deployment signals are forbidden** — the first is excluded system-wide by the Guardrails' no-predictive-research rule; the second is a direct extension of the existing "never read a rising buffer as a lever-up signal" doctrine line.
4. **Backtest arm 3 ("margin only during drawdowns") is not being designed** — it's definitionally averaging down with borrowed money.
5. **Backtest arm 4 ("margin deployment based on regime") is not being designed** — it would rebuild, on the margin axis, the exact mechanism the Decisions Log calls "not backtestable as one" for leverage generally, and whose cash-axis analog was already tested and rejected on cost grounds (`regime_backtest.md`).
6. **No conflict, but a related discipline point**: the task brief asks for a "rigorous" engine — rigor here specifically means resisting the temptation to reintroduce timing logic under a different name (a "risk regime," a "smart deployment score," etc.). Every mechanical rule in this system that has survived scrutiny (leverage cap, buffer floor, cluster caps, T1/T2 ceiling) shares one property: it responds to the account's own state, never to a market read. This design holds that line throughout.

---

## 8. Recommended implementation order

1. **Repayment framework's pure functions + tests** (Section 4, Section 6 step 1) — no conflicts, most concretely useful, builds on `margin_capacity()`'s existing tested math.
2. **New backtest metrics (volatility, Sharpe, time-underwater, leverage-exposure) + their own unit tests** — needed before arm 2 or arm 5 can be evaluated properly; useful to every future backtest, not just margin ones.
3. **Backtest arm 2 (no margin vs. controlled margin)** — the most fundamental open question, currently answered only by "it already existed when discovered," not by evidence. Do this before arm 5, since arm 5's repayment rules only matter if arm 2 confirms margin is worth carrying at all.
4. **Backtest arm 5 (repayment strategies)** — depends on arm 2's verdict and the new metrics from step 2.
5. **State classification (Section 2) as a pure, informational function** — display-only integration into `render()`, no behavior change, low risk, can ship independent of the backtests above.
6. **Backtest arm 1 (mechanical adaptive vs. fixed leverage)** — lowest priority of the buildable arms; the current fixed cap already has a doctrine rationale (same posture as crypto-sleeve conviction-sizing) that doesn't strictly require backtest validation the way a *new* mechanism would, but it's cheap to test given the framework already exists.
7. **Wire adopted verdicts into `plan()`/`targets.yaml`**, one change at a time, only after every relevant backtest has a verdict and every relevant pure function has tests.

## 9. What should NOT be built yet

- **Arms 3 and 4 as originally specified** — not a sequencing question, a scope question. These would need to come back as their own explicit conversation with a reframed premise, the same way "investment thesis management" was flagged and deferred in the Phase 1 audit, not built because they were on a list.
- **Any "Opportunistic" or lever-up-on-signal state** — same reasoning.
- **Any automatic `plan()`/`targets.yaml` change before a backtest verdict exists for it.** The repayment-redirect *fraction* specifically must come from Section 5's backtest, not be picked and shipped first.
- **A fourth margin state beyond the three proposed** — I don't have an objective, mechanical trigger to justify one; inventing a state without a clean criterion would just be a slower path to reintroducing discretion.
- **A real risk-free rate for the Sharpe calculation** — using 0% and disclosing it is the right default for now; picking an actual rate is a small but real assumption that deserves its own explicit decision, not a default buried in code.

---

Nothing in this document has been implemented. Awaiting approval before any code, test, or config change.
