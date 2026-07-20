# Portfolio Policy Manual v1.0

**Document status:** Non-authoritative synthesis of existing, adopted investment policy, at the lowest derived level of the operational precedence hierarchy (`governance/decisions/GOV-0002-operational-precedence-hierarchy.md`). This manual originates no new policy, changes no doctrine, and recommends no code. **Principal governing sources, in descending authority:** the Investment Constitution (`constitution/INVESTMENT_CONSTITUTION.md`, including material it expressly incorporates — `docs/MARGIN_DOCTRINE.md` in full, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §20/§24 only); accepted governance decisions (`governance/decisions/`, indexed by `governance/decisions.yaml`, with `decision_log.yaml` as historical evidence of the pre-GOV-0001 `MARGIN-####`/`PI-####` ledger within its original scope); current accepted or frozen specifications and doctrine not incorporated into the Constitution (including the balance of `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` outside §20/§24); `CLAUDE.md` (operational synthesis); `targets.yaml`; `holdings.yaml`; executable code and tests. See GOV-0002 for the complete hierarchy and its conflict-resolution rules. If those sources change, this manual must be updated to match; it is not itself an amendment mechanism.

**Authoritative repository sources were last verified against `main` at commit `38394ddab127583c61549a3f5361df0b3cfd472c`.** This manual also documents the read-only `--health` behavior introduced by PR #89. The cited SHA records the authoritative-source verification baseline; it is not intended to identify the commit containing every sentence in this document. Later authoritative-source changes supersede this synthesis.

**As of:** 2026-07-18. Net equity ~$5,545 (gross ~$8,994 less margin debt ~$3,450) and margin buffer 61.08% are retained as a **2026-07-13/07-14 doctrine-revision baseline** for historical context. They are no longer stated in `CLAUDE.md`, which now points to `holdings.yaml` for the repository's most recently synced margin state. These are not live figures and are not policy — policy is the rules below, which apply regardless of where these numbers sit on any given day.

---

## 1. Portfolio Mission

This is a **decision-support system, not an execution system.** It never places orders — order-placement methods were deliberately stripped from `alpaca_client.py` and must not be re-added. All trades are executed manually on Robinhood by the account holder. The system's job is to combine live portfolio data with mechanical policy rules and present a recommendation; the human's job is to apply judgment on top of that and execute. The system is explicitly expected to **push back when the human's own instructions conflict with the human's own adopted rules.**

**Book** is defined as **net equity**: the gross total of `holdings.yaml` minus current margin debt, both recomputed from source on every run — never assumed or carried forward from a prior session.

## 2. Capital Allocation Philosophy

- **Fuel for allocation is deposits and margin** (margin only within the leverage cap in §6). Cash deposits and margin-funded buying power are gated differently: margin does not grow the book/target baseline the way a cash deposit does, and must be identified as cash vs. margin before an allocation run.
- **Mechanism: a "largest dollar gap" allocator, not a forecaster.** Every run computes each ticker's dollar distance below its own target weight and fills the **largest gaps first**, in **$25 minimum lots**, until the deposit is exhausted. There is no separate return-prediction, price-target, or "opportunity map" layer — the system computes opportunities at runtime, on deposit day, from current gaps only.
- **No market-timing overlays.** Every timing/regime layer proposed or tested has been rejected or removed:
  - A band-overlay signal-trading backtest returned 227% vs. 422% buy-and-hold → **NO-GO**, never implemented.
  - A QQQ 200-EMA regime gate that blocked/zeroed deployment when QQQ was below its 200-day EMA was backtested (25.49% vs. 28.05% annualized TWR, a 2.56pp/yr cost) and **removed from `allocate.py`**. Regime status is still computed and displayed every run, purely informational — it no longer blocks or delays any deployment.
  - A per-ticker 200-SMA/RSI trend gate on the *buy* side was tested (27.64% vs. 28.05%, +0.41pp, inside noise) and **kept unchanged** — it still gates individual buys (see §7), just wasn't found to justify removal.
- **Tier weighting exists to express conviction, not to chase return.** A four-arm backtest (current vs. equal-weight vs. flatter vs. steeper gradation) found every variant within 0.75pp of current — no measurable performance difference from tier-weight structure in either direction. Weights are a conviction ladder, not a performance lever.
- **Buy-level staging (`--levels`) kept unchanged.** A three-arm rung backtest (current SMA−ATR rungs vs. S/R rungs vs. market-buy, pre-committed 1.0pp threshold) found all arms within the noise threshold — S/R rungs rejected (lost to both other arms), current rungs kept as a non-gating staging aid, not a buy gate. Question closed (`reports/rung_backtest.md`).
- **Crypto sleeve sizing is conviction-based, not timing-based** — it competes in the same gap-ranking as every other line, with no directional or valuation view driving size (see §4).

## 3. Tier Philosophy

Per-ticker target weights (`targets.yaml`, config truth):

| Tier | Weight/name | Trim ceiling | Roster |
|---|---|---|---|
| **T1** | 3.35% | 1.5× target (mechanical, §6) | ASML, TSM, MSFT, GOOGL, META, NVDA, GEV, LLY, V |
| **T2** | 1.65% | 1.5× target (mechanical, §6) | AVGO, AMZN, CEG, PWR, ISRG, TMO, DHR, SYK, MA, BRK.B, WMT, COST, EQIX, MLM, AAPL |
| **ETF** | 2.30% | none | SPY, QQQ, GLD |
| **band** | 0.75% | 1.25× target (RSI-gated, §8) | KLAC, LRCX, AMAT, AMD, MU, MRVL, WDC, VRT, ETN, CAT, GNRC, IBM, NOW, CRM, ORCL, NFLX, SHOP, CRWD, PANW, UBER, JPM, HOOD, XOM, CVX, RTX, ABBV, MRK, JNJ, GILD, UNH, BABA, SKHY, DELL |
| **spec** | 1.00% fixed | never above target | INTC, SPCX, RKLB, TSLA, PLTR |

**Tier is a conviction statement, reviewed only through explicit, one-time scans — not a standing research process:**
- **AMZN kept at T2, not promoted to T1** — T1 is already 7-of-9 names one AI-infrastructure trade; sizing up another mega-cap there compounds a flagged concentration rather than fixing it.
- **AVGO stays at T2, not promoted to T1** — same reasoning as AMZN, and AVGO is itself a `semis` cluster member, so promotion would compound that concentration more directly.
- **AAPL promoted band → T2** (2026-07-14) — fits T2's "quality compounder" character (alongside COST/WMT/MA/BRK.B) better than band's cyclical/smaller-cap character, and doesn't touch the T1 concentration question.
- **VMC exited, consolidated into MLM** (2026-07-13) — both were direct aggregates-industry peers; holding both was redundant sector exposure, not diversification.
- A full 65-name tier-fit scan found the rest of the roster reasonably placed; no other promotions/demotions flagged.

## 4. Sleeve Philosophy

Six sleeves total: T1, T2, ETF, band, spec (all above), plus:

- **Crypto sleeve — 10% of book, ETH/SOL/BTC only.** HYPE was removed from targets (July 2026). Reaffirmed doctrine: **conviction-sizing, not a timing call** — the sleeve rebuilds only through the standard gap machine, competing like any other underweight, with **no trend/RSI/earnings gates and no "cheap vs. expensive" market view** sizing it up or down.
- **BTC is the sleeve's designated liquid reserve**, not a third coequal coin. It was fully sold 2026-07-13 to correct a sleeve overage (see §11), leaving the sleeve ETH/SOL-only until rebuilt. Robinhood's unsellable sub-cent dust (ZORA/WIF/BONK/PEPE, $0.00) is permanently ignored, never synced — display noise, not a holding.
- Sector/asset-class completeness was audited once: three single-name "sectors" (Materials/MLM, Utilities/CEG, Real Estate/EQIX) were found thin but immaterial (no new tier warranted), and zero fixed-income exposure was found **correct, not a gap** — GLD serves the ballast role a bond allocation would, and bonds would compete poorly against a ~5% margin cost.

## 5. Cluster Philosophy

Correlated-cluster caps sit **above** individual tier weights — a name can be within its own tier target and still be blocked or trimmed by its cluster. Caps are **ceiling-only by design: no cluster target or floor.** A cluster target would mean buying *toward* a thematic exposure goal, a different (and here, wrong-direction) decision from "these move together, cap the downside." A ticker in more than one cluster needs headroom in **every** cluster it belongs to before it can be bought.

| Cluster | Cap (% of book) | Roster | Basis |
|---|---|---|---|
| **semis** | 25.0% | ASML, TSM, NVDA, AVGO, AMD, MU, MRVL, KLAC, LRCX, AMAT, WDC, INTC, SKHY | 0.542 avg pairwise correlation — chip names crash together |
| **power_infra** | 20.0% | GEV, ETN, VRT, PWR | 0.560 avg pairwise correlation — AI data-center power/electricity buildout demand |
| **oil** | 20.0% | XOM, CVX | 0.819 avg pairwise correlation (strongest scanned) — same commodity driver; cap level *derived* from a stress test (historical max drawdown × cap ceiling ≈ 6% of book impact, matched to power_infra's risk budget), not picked |

**Deliberately declined clusters** (same bar applied, different verdict):
- **CAT/TSLA**, correlated with the power_infra group in the same scan, were excluded — weaker fundamental fit (general industrials / EV-storage), more likely bull-market beta than the specific power-buildout mechanism.
- **Enterprise software (CRM/MSFT/NOW)**, 0.650 correlation, declined — generic "software sector" beta, not a narrow shared driver, and immaterial in size ex-MSFT.
- **T1 AI-infrastructure (ASML/TSM/NVDA/MSFT/GOOGL/META/GEV)**, scanned directly: 0.302 avg correlation (0.373 ex-MSFT) — below every adopted cap and below the already-declined enterprise-software bar. **Declined as a cluster cap.** (The underlying concentration this scan surfaced was real and is instead addressed by the T1/T2 concentration ceiling — §6, §11.)

**Known structural property, left as-is, not a bug:** cap denominator is net equity (book), not gross. Under leverage, a broad decline can nudge a cluster over cap with zero real cluster-specific dispersion (fixed margin debt shrinks the denominator faster than assets fall), and a broad rally quietly loosens every cap. Switching to a gross denominator would remove the decline-side asymmetry but understate true leverage-adjusted concentration risk during rallies — judged the worse trade-off.

## 6. Risk Management Policy

**Margin.**
- Fixed **1.8× structural leverage cap** on gross-position-value ÷ net-equity — the level in place when the doctrine was formalized (2026-07-13), not derived from a target and not a lever to move opportunistically.
- **30% margin-buffer floor, hard cutoff.** Before any margin-funded buy, the system checks the *most recently synced*, Robinhood-displayed buffer against the 30% floor; if that synced buffer is already below 30%, the buy is blocked outright — **no partial taper** — and it's treated as a forced de-lever signal (trim or pay down margin), same severity as a cash-tight guardrail. Independently, requested margin is clipped to the 1.8× leverage cap. **The system cannot calculate Robinhood's exact projected post-trade buffer from the data available to it** — no such formula exists in this codebase; only the currently-synced buffer is ever checked, never a post-trade estimate. Margin data must therefore be freshly synced from Robinhood before it's relied on for a margin-funded decision, and synced again immediately after execution.
- **Buffer is a capacity ceiling, not a timing throttle.** It states how much more can safely be borrowed right now, not whether now is a good time to. A high or rising buffer must never be read as license to lever up — buffer rises mechanically as positions gain value, which is exactly when pro-cyclical levering (buying high, taking the worst of a reversal) is most dangerous.
- **No margin-timing model of any kind** — no "borrow more when conditions look good," no market-view-driven lever up/down. The cap is fixed and mechanical, same posture as crypto's conviction-sizing rule.
- Margin interest (~5% APR, first $1,000 free) is a **guaranteed cost / hurdle rate**, not something to optimize around.

**T1/T2 concentration ceiling.** Any T1 or T2 name above **1.5× its own tier target** trims mechanically to target, no RSI gate — the same treatment as a cluster-cap breach, applied per-name instead of per-cluster. This is a **doctrine decision, not a backtest verdict** — same category as the 1.8× leverage cap and 30% buffer floor: a single core-conviction position at 2×+ target under leverage is judged a tail/forced-liquidation risk that a total-return backtest cannot price, so it is stated and applied without further relitigation absent a new leverage regime.

**Margin risk-state display.** Every run other than `--levels`/`--performance` computes and displays a margin risk state (NORMAL / CAUTION / RESTRICTED / FORCED_DELEVER). Only NORMAL and FORCED_DELEVER are reachable today — CAUTION/RESTRICTED thresholds are unconfigured in `targets.yaml`. This classifier is informational only and runs strictly after the allocation plan is computed; it cannot alter a buy/trim/block decision. The only decision-altering margin check is the pre-existing hard buffer-floor block above.

**Standing guardrails, enforced on the human:**
- Buffer below 30% → recommend immediate de-lever; never propose increasing leverage as a response to a drawdown.
- Trades proposed outside a deposit cycle → remind of the workflow before helping.
- Any proposal to build new analysis/research/thesis layers → cite the Decisions Log first (added layers have measured negatively in this system's own backtests).
- Cash tight (recent withdrawals, sub-$500 buffer) → recommend inaction. **Pausing is the system working, not a failure to act.**
- No predictive research, price targets, or forward-looking "opportunity maps."
- Never hallucinate prices, dates, or holdings — live data or `holdings.yaml` only.
- Claims from external review (outside this system, without live data/file access) must be **verified against the actual code/files before being acted on** — demonstrated necessary twice in-session (a stale price, an incorrect assumed RSI value).

## 7. Buy Policy

Buys are allocated to the **largest dollar gap first**, in **$25 minimum lots**, gated in this fixed order:

1. **200-day SMA trend gate** — a new add is blocked unless the name is above its 200-SMA, *or* RSI(14) is below 30 (oversold override).
2. **7-day earnings blackout** — no new add within 7 calendar days of an earnings date.
3. **Caps** — correlated-cluster caps (§5), band's 1.25× ceiling, spec's fixed-at-target ceiling. A name in more than one cluster needs room in all of them.

**Removed from the buy path:** the QQQ 200-EMA regime gate (§2) — dropped entirely after backtest; regime status still displays but never blocks or delays a deposit.

**Crypto sleeve buys** are computed as one aggregate sleeve gap only — the allocator does not split across ETH/SOL/BTC. The coin split is a manual, human decision; the current standing instruction (§11) is to route new crypto buys to BTC specifically until the reserve is rebuilt.

**Untestable, accepted as-is:** the earnings blackout's cost cannot be backtested (no historical earnings-date feed for 63 tickers over 5 years on the free tier); its mechanism (redirecting money to the next gap, not holding cash) is the same as the trend gate's, so its cost is accepted as bounded by the same measured-small logic.

## 8. Trim Policy

Two distinct trim mechanisms, deliberately different in trigger and rigor:

**Opportunistic, RSI-gated (band/spec only).** A band or spec position above its cap (band: 1.25× target; spec: any amount above its fixed target) trims **only when RSI(14) > 60** — waits for strength, a return-timing choice for overweight positions with no other risk-limit reason to force a sale.

**Mechanical, no RSI gate (risk-limit breaches).** Two cases, both floored at the name's own tier target, both triggering regardless of RSI:
- A **correlated-cluster cap breach** (§5) — trims largest-own-target-overweight-first within the breaching cluster.
- A **T1/T2 name above 1.5× its own tier target** (§6) — trims to target.

These are risk-limit breaches, not timing calls, so — unlike band/spec's opportunistic trim — they do not wait for a "good" price.

**Backtest discipline on trims:**
- A five-arm trim-parameter backtest (1.25×/RSI 60 current, tighter/looser variants, mechanical no-gate, never-trim) found all parameter variants within ±0.26pp of current — **kept unchanged**, no re-tuning, per-ticker tailoring rejected as overfitting.
- **Never-trim won the raw-TWR backtest by +6.65pp/yr** but did so by letting a single spec position balloon to ~3.6× its intended size with a materially worse drawdown that, at the account's leverage, threatens the buffer floor and forces selling at the bottom. **Trims are the enforcement mechanism of tier sizing (risk control) — the 6.65pp gap is the insurance premium, priced honestly as a real cost, not a return leak to be closed.**
- **Important precision, carried forward exactly as recorded:** the T1/T2 ceiling *tested* in `t1t2_trim_backtest.md` trimmed excess back down to 1.5× (ceiling-style, ~0.02pp cost). The rule actually running trims all the way **down to 1.0× target** (floor-at-target), matching the cluster-cap mechanism — removing materially more per breach than what was tested. **This rule's true cost is untested**, not "tested and cheap"; it stands on doctrine grounds only (§6), not on the 0.02pp backtest number.

## 9. Human Responsibilities

- Report deposits and buying power, or margin draws/paydowns — and specify whether new capacity is cash or margin, since the two are gated differently.
- Execute every recommended trade manually on Robinhood; confirm fills back to the system.
- After any real share/coin/BTC/margin change, paste the update and run the corresponding sync (share counts, crypto shares, BTC value, margin debt/buffer) — margin buffer must be the brokerage's own **displayed** figure, never derived.
- Proactively report deposits, withdrawals, margin draws/paydowns, or buffer changes — absent an explicit report, the system assumes nothing moved.
- Hold final judgment and override authority — the system is expected to combine its output with human judgment, and the human is expected to hear it when it pushes back on a rule violation.
- Any change to a cap, gate, tier weight, or doctrine line requires the human's own decision, recorded in the Decisions Log — the system does not originate policy changes on its own.

## 10. System Responsibilities

- Never place an order, under any circumstance — recommendations only.
- Recompute the book (gross and net equity) from source on every run; live-price every synced share/coin position automatically; hold BTC and margin at their last manually-synced value until the human updates them.
- Enforce every gate and cap exactly as coded, mechanically and without discretion — no ad hoc timing overrides invented at runtime.
- Compute buy/trim opportunities only at the moment of a run, from current gaps and current data — never maintain or surface a standing forward-looking research layer.
- Sync repository state automatically: pull before reading any state at the start of a session; commit and push immediately after any commit-worthy change, never batched or deferred; never silently overwrite another session's unpushed state.
- Display informational-only signals (regime status, margin risk state) without letting them silently gate a decision the doctrine has not assigned them to gate.
- A separate, advisory-only Portfolio/Theme Intelligence layer (per-company and per-theme thesis records under `intelligence/`) may exist alongside this policy. By its own governing specification it **cannot modify `holdings.yaml` or `targets.yaml`, cannot alter any allocator recommendation, and no production code reads it** — it is a human research record, not a component of the allocation or risk mechanism described in this manual.
- `python allocate.py --health` exposes a read-only snapshot of metrics `plan()` and `margin_state.py` already compute — leverage, last-synced buffer, margin risk state, cluster-cap proximity, crypto-sleeve drift, and T1/T2 target/ceiling proximity. It is non-authoritative in the same sense as this manual itself: it introduces no new policy, threshold, or investment doctrine, and it does not change any buy, trim, block, or delever outcome — each metric it displays continues to defer to the same canonical source (`plan()`, `margin_state.py`, `targets.yaml`) described elsewhere in this manual. There is no overall portfolio-health score or categorical healthy/unhealthy verdict — every figure is shown individually, labeled with its own source and comparison point.

## 11. Open Investment Policy Questions

- **Crypto sleeve rebuild in progress.** BTC was fully drained 2026-07-13 to correct a sleeve overage; the standing instruction is to route future crypto buys to BTC until it returns to ~25% of the sleeve (~2.5% of book). ETH/SOL remain staked/illiquid, so no further trim is available without unstaking — passive correction via other sleeves' deposits is the accepted default path unless the overage keeps drifting further.
- **T1/T2 concentration ceiling's true cost is an open evidentiary question, not a closed one** (see §8 precision note). The *decision to trim* is settled doctrine (capital-impairment risk, same category as the leverage cap); the *magnitude actually implemented* (floor-at-target, not the tested ceiling-style version) has never itself been backtested. This is flagged, not resolved.
- **`min_lot_dollars` ($25) does not scale with book size.** Adequate today (~0.45% of book); flagged to revisit once the book crosses roughly $25,000, where it would drop under ~0.1% and stop functioning as a meaningful floor.
- **Live-priced valuation only reflects the regular trading session (9:30am–4:00pm ET)**, frozen outside it on both sides (confirmed pre-market and post-close). This is a structural limitation of the free daily-bar data feed, not a settling-in issue, and has no fix without a paid real-time feed.
- **Earnings-gate data source is still on a weaker fallback than intended.** `finance.yahoo.com` (the primary lookup host) was never added to the network allowlist alongside the query-subdomain hosts that were fixed — every earnings-date lookup has been running on a thinner single-date fallback instead of the intended full-history source. The gate still functions, on weaker data than designed.
- **The 1.8× leverage-cap structure is fixed doctrine; the specific numeric level is recorded as an open evidentiary question in the structured decision record** (`decision_log.yaml`, MARGIN-0001: status `pending_evidence`) — the cap formalized the debt level already in place in 2026-07-13 rather than deriving 1.8× from evidence. Stated plainly, without resolving it here: the *mechanism* (fixed, mechanical, no discretion) is settled doctrine on the same footing as the buffer floor; the *number* 1.8× itself has not been separately justified by a backtest the way the trim/rung/weight/regime/trend rules have been.
