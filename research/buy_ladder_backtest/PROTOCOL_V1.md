# Buy-Ladder and Trim-Level Backtest — Protocol V1 (frozen pre-registration)

_Companion protocol for `governance/decisions/LADDER-0001-canonical-buy-ladder-backtest-authorization.md`.
This document is the complete technical specification of the study `LADDER-0001` authorizes.
Nothing in this document is executed by the governance filing that adopts it — no simulation may
run before that filing's PR merges and this file's pinned SHA-256 verifies from the committed
blob._

## 0. Why this study exists

`reports/rung_backtest.md` (2026-07-12) tested the current ATR-based buy-ladder methodology
(`levels.py`) against a support/resistance alternative and a market-buy baseline, on the **65-ticker
retired T1/T2/ETF/band/spec tier universe** (`backtest_rungs.py`'s `roster_tickers()` reads
`targets.yaml`'s old `tiers:` block, confirmed by direct inspection this session — that key no
longer exists in `targets.yaml` since `PHQ-2026-02`'s migration to the canonical `destination:`
list). The verdict (NO CHANGE, all arms within the pre-committed 1.0pp threshold) is closed and not
reopened by this study. What has never been tested is whether that same verdict — or the ladder
mechanism itself — still holds on the **current canonical 27-name equity/fund roster**
(`targets.yaml`, `PHQ-2026-02`), which has different membership, different per-name weights, and a
materially different actionable-gate structure (6 gated names, `gates.yaml`) than the retired
universe. This protocol re-runs the same class of question, narrowly, against current truth.

## 1. Research question

Does the current ATR-based buy-ladder methodology (`levels.py`: L1/L2/L3 = 50SMA − {1.0, 2.0,
3.0}×ATR14, L3 floored at 200SMA, 25% practicality cap, 60-session swing-low flag) remain
reasonable — i.e., not worse than clearly-defined simpler alternatives by more than a
pre-committed materiality threshold — for the current canonical destination roster, compared with
(B) a simple fixed-percentage pullback ladder and (C) immediate/scheduled deployment?

This study evaluates **methodology** (does the ladder mechanism earn its complexity), not current
trade recommendations. It produces no buy list, no current ticker signal, and no live price
computation.

## 2. Hypotheses (pre-committed, one test, one verdict)

- **H0 (retain current methodology):** Arm A's annualized TWR is within ±`ADOPT_THRESHOLD_PP`
  (1.0pp) of both Arm B and Arm C, **and** Arm A's MaxDD is within ±1.0pp of both — matching the
  original `rung_backtest.md` finding's shape. Verdict: NO CHANGE.
- **H1 (simplify):** Arm C beats Arm A by more than 1.0pp TWR without a MaxDD deterioration of more
  than 1.0pp in Arm C's favor — waiting for rungs is net cash drag on the current roster. Verdict:
  recommend simplification (subject to §17 adoption rule — this study cannot itself change
  `levels.py`).
- **H2 (retain/reinforce):** Arm A beats both B and C by more than 1.0pp TWR without failing the
  MaxDD tolerance. Verdict: recommend retaining current methodology with stronger evidence behind
  it.
- No fourth hypothesis, no variant mining. One pre-committed threshold, checked once, per §14.

## 3. Current-policy baseline — Arm A (independently verified against production code this session)

Verified directly against `levels.py` and `targets.yaml` (`levels:` block) at authorization time,
not assumed from the audit lead that prompted this study:

- `rung_atr_multipliers: [1.0, 2.0, 3.0]` — L1 = 50SMA − 1.0×ATR14; L2 = 50SMA − 2.0×ATR14;
  L3 = max(50SMA − 3.0×ATR14, 200SMA) ("trend-floor" — L3 is never modeled below the 200SMA).
- `practicality_cap_pct: 25` — a rung more than 25% below current price is tagged "unlikely
  near-term"; for simulation purposes such a rung is treated as **unlikely to fill within the cycle
  it was staged** (see §10 reset rule), not deleted from the ladder.
  named the same way `levels.py` reports it — the crash-level tag does not remove the rung.
- `swing_low_sessions: 60` — L3 below the 60-session swing low is flagged "below recent support"
  (informational; does not change fill logic in this study — no discretionary override is modeled).
- Trend gate: adds blocked below 200-SMA unless RSI(14) < `trend_rsi_override` (30) (`gates.yaml`);
  applied identically across all three arms (§12) — it is not the experimental variable.
- Earnings gate: adds blocked within `earnings_blackout_days` (7) calendar days of an earnings date
  (`gates.yaml`); applied identically across all three arms (§12).
- Sizing/ticker-selection: production `levels.py` is an advisory staging report — it does not
  itself execute or size a purchase. To simulate a ladder at all, this study reuses, unchanged,
  `allocate.py`'s existing gap-fill ranking (largest target-gap-dollar first, `min_lot_dollars`
  $25 floor, cluster-cap and 8%/40% no-add ceilings applied identically across arms per §12/§13) to
  decide **which** ticker(s) a cycle's deposit is directed to; the three arms differ only in
  **when** that ticker's allocated dollars are deployed (immediately, or staged across ladder
  rungs). This is the same "identical deposits, identical tickers, entry timing is the ONLY
  difference" design `backtest_rungs.py`'s own docstring already used for the 2026-07-12 study —
  reused here for methodological comparability, not invented new.
- Per-rung sizing: equal-dollar across the 3 rungs (each rung gets 1/3 of the ticker's allocated
  cycle dollars) — matching `backtest_rungs.py`'s `N_RUNGS = 3` convention.

## 4. Alternative arms

**Arm B — simple fixed-percentage pullback ladder.** Three rungs at fixed **−5% / −10% / −15%**
off the ticker's 50-SMA (same reference point as Arm A, isolating "how levels are computed" as the
only difference from Arm A). Equal-dollar per rung. No ATR, no 200SMA floor, no swing-low check.
These three percentages are the entire parameterization — fixed before any simulation runs, not
swept, not tuned after seeing a result (§20).

**NUM-0001 provenance (`governance/decisions/NUM-0001-numeric-parameter-provenance-standards.md`):**
these three percentages are a **research assumption** — one of NUM-0001 §2's contextual classes,
kept separate from and never conflated with its six binding-value provenance classes (§1). They do
not govern any live allocation, margin, or trim outcome; they are pre-registered design inputs to
this bounded comparison arm only. They are explicitly **not** empirically calibrated (NUM-0001 §8 —
no evidence directly and uniquely favors −5/−10/−15% over any other simple percentage set) and
**not** an evidence-bounded governance selection (NUM-0001 §7 — no prior evidence establishes a
defensible range for a fixed-percentage pullback ladder on this roster; that is exactly the open
question this study exists to inform, not a premise it already rests on). They are a governance
judgment, selected only to instantiate one clearly-defined, simple, non-ATR alternative worth
testing against Arm A — not current portfolio policy, not a production ladder setting, and not a
ticker-specific recommendation. **This classification does not imply, and must not be read to
imply, that −5%/−10%/−15% are optimal, superior, or better-sized than any other fixed-percentage
set** — per §4's own "No Arm D" discussion above, a percentage-grid sweep to find a "better" Arm B
is explicitly declined as parameter-fishing, precisely because this arm's role is a bounded,
one-shot comparison point, not an optimization target.

**Arm C — immediate/scheduled deployment baseline.** The cycle's full ticker-allocated deposit is
deployed at the deposit-day close, no waiting for any level. This is the same "market-buy" baseline
concept as the original study's Arm C, applied to the canonical roster's gap-ranked ticker
selection.

**No Arm D.** Two candidates were considered and explicitly declined, not silently omitted:

1. **Reopening the previously-rejected support/resistance pivot-based ladder**
   (`rung_backtest.md`'s Arm B: pivot swing lows, 29.05% vs. current 29.35% — REJECTED, losing to
   both other arms). The audit that produced this filing's lead specifically warned against
   reopening this arm merely because TradingView screenshots are now available for manual chart
   reading. No new hypothesis and no new evidence regime is documented here — chart-pattern
   reading remains permanently excluded from this repository's backtestable methodology (CLAUDE.md
   Decisions Log, July 2026) and screenshots are not a reproducible numerical input (§8). Declined.
2. **An ATR-multiplier or percentage-grid sweep** (e.g., testing {0.5,1.5,2.5}, {1.5,2.5,3.5}, ±2pp
   variants of Arm B's percentages, alternative practicality caps). Declined as parameter-fishing —
   exactly the per-ticker-tailored-parameter overfitting `trim_backtest.md` already rejected for a
   different gate, and the "avoid optimization fishing" instruction this study is chartered under.
   One bounded parameterization per arm, fixed before simulation, full stop.

## 5. Canonical universe (frozen at authorization time — `targets.yaml` as of this filing)

Verified directly against `targets.yaml`'s `destination:` list and `gates.yaml` this session, not
assumed:

| Class | Members | Treatment |
|---|---|---|
| Individual equities (non-gated, primary study) | NVDA, TSM, ASML, AVGO, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG, TMO, V, COST, CEG, ETN, GEV, GNRC, PWR, RTX (21 names) | Included, Arms A/B/C, all metrics |
| Individual equities (gated) | SNPS, ICE, SPGI, WM, RKLB, TSLA (6 names) | **Excluded from the primary study entirely** — see §6 |
| Broad ETFs | SPY, VEA, VWO | Included, Arms A/B/C — same three arms as equities, mechanically unmodified `levels.py`/`allocate.py` logic already treats them identically — but reported as **its own segment**, never pooled into the equity-only figures (§15, §18) |
| GLD | GLD | Included, Arms A/B/C, reported as its **own segment**, never pooled with equities or broad ETFs (§15, §18) — its ballast/commodity return profile differs materially from growth equities and from diversified broad-market ETFs |
| Crypto | BTC, ETH, SOL | **Excluded from this study entirely** — see §19 |
| Reserve / cash | RESERVE, CASH | **Excluded** — `asset_class: reserve`/`cash` rows are never buy candidates in production (`targets.yaml` comment, `allocate.py plan()`); no price series exists for them and none is modeled |

31 equity/fund/GLD rows named in this study's scope discussion (21 non-gated equities + 6 gated,
excluded per §6, + 3 broad ETFs [SPY, VEA, VWO] + 1 GLD row: 21 + 6 + 3 + 1 = 31); **25 rows are
actually simulated** across the three segments once the 6 gated names are excluded (21 non-gated
equities + 3 broad ETFs + 1 GLD row: 21 + 3 + 1 = 25).

**Minimum-history rule:** a ticker with fewer than 210 trading sessions of split-adjusted history
at the earlier of (its first date in the data window) or (the point it would first become
gap-eligible) is excluded from the simulation and named explicitly in the data manifest — matching
`backtest_rungs.py`'s own `MIN_HISTORY = 210` convention. This is a data-sufficiency rule, not a
roster judgment; an excluded name is disclosed, never silently dropped.

## 6. Gated names — not buy-eligible, not simulated

`gates.yaml` (authority `PHQ-2026-01`) currently gates SNPS, ICE, SPGI, WM, RKLB, and TSLA —
`allow_add: false` for each, their destination weight held in cash, never redistributed. This study
**excludes all six from every arm and every simulated cycle** — they are never buy candidates in
production today, and simulating a purchase of any of them would misstate current authorization.
No labeled counterfactual arm is added for gated names in this first study (a bounded choice,
consistent with "keep the study bounded" — a gated-name counterfactual, even labeled, is deferred
to a future, separately authorized study if ever pursued). **This study does not authorize, and
must not be read to authorize, a purchase of SNPS, ICE, SPGI, WM, RKLB, or TSLA under any
circumstance.**

## 7. Fundamental / Intelligence boundary

No Company or Theme Intelligence field (conviction rating, thesis, risk severity, catalyst,
freshness status) is read, referenced, or used as a simulation input anywhere in this study. Ticker
selection each cycle is driven exclusively by `allocate.py`'s existing mechanical
target-gap-dollar ranking (§3) — the same rule production already uses, holding Intelligence
fully advisory and uninvolved, per `PI-0001`/`OPS-0008` §12's unbroken doctrine.

## 8. Chart-analysis boundary

TradingView screenshots and manual technical chart reading are **not a study input under this
protocol**. Every level, rung, and fill decision in Arms A/B/C is computed from the same
reproducible numerical series (split-adjusted daily OHLC, SMA/ATR/RSI derived from it) already used
by `levels.py`/`indicators.py` in production. Screenshots cannot create portfolio eligibility,
cannot override a gate or a target, are not current investment authority, and this study does not
authorize screenshot-based recommendations of any kind, now or after results are produced.

## 9. Data period

**2021-06-01 through the last complete trading day before the G1 data-acquisition step begins** (to
be recorded, once known, in `data_manifest.yaml` — not invented in this frozen protocol). The start
date matches `rung_backtest.md`/`trend_backtest.md`/`weight_backtest.md`/`regime_backtest.md`'s
own window, preserving rough comparability to this repository's other closed backtests and
preserving the one real (2022) bear stretch already established in this data (§16 sub-period
check). The end date is **not** extended after G1 freezes it without a charter amendment (§20).

## 10. Deposit schedule, position sizing, cash handling, reset/expiry

- **Deposit schedule:** synthetic $2,000 on the first trading session of each calendar month —
  matching `backtest_rungs.py`'s `DEPOSIT = 2000.0` convention exactly, for direct methodological
  comparability to the 2026-07-12 study. This is a modeling assumption for comparability, not a
  claim about the account's actual current deposit cadence or size, and does not authorize any
  actual cash or margin deployment (this protocol touches no live account state — see §21).
- **Position sizing / ticker selection:** each cycle's deposit is ranked against then-current
  simulated target gaps using the same largest-dollar-gap-first rule `allocate.py` already applies
  in production, subject to the same cluster-cap and 8%/40% no-add constraints (§12/§13) — held
  identical across all three arms so that entry timing (A vs. B vs. C) is the only experimental
  variable, exactly `backtest_rungs.py`'s original design.
- **Cash handling:** dollars allocated to a ticker but not yet deployed (an unfilled Arm A/B rung)
  sit as idle simulated cash — never redirected to another ticker mid-cycle, never treated as
  deployed for TWR purposes until an actual fill is simulated. Idle time is the "cash drag" and
  "unfilled-capital duration" metrics (§14).
- **Reset / expiry rule:** an Arm A/B rung unfilled by the end of the deposit cycle it was staged
  in is **abandoned, not carried forward** — the next cycle's deposit is evaluated fresh against
  then-current gaps and levels. This matches the real advisory tool's own behavior: `levels.py`
  recomputes every level fresh on every run, with no persisted order book or queued limit order
  (the human decides manually, per CLAUDE.md's Identity & Role — this tool places no orders). No
  alternative reset rule (e.g., indefinite carry-forward, partial-fill rollover) is tested in this
  study.

## 11. Corporate-action handling

Split-adjusted daily OHLC price series only (same source convention as every existing backtest
script in this repository). **Price-return only — dividends excluded from every return
calculation.** This is a disclosed simplification, matching every one of this repository's prior
closed backtests (`rung_backtest.md`, `trend_backtest.md`, `weight_backtest.md`,
`regime_backtest.md`, `trim_backtest.md`, `t1t2_trim_backtest.md`), none of which built a
dividend ledger. `MARGIN-0005`'s heavier point-in-time dividend-ledger machinery is a deliberately
larger research program for a different question (margin/target sizing, 300-run ceiling) and is
**not** replicated here — building one would not match this study's "smallest reversible next
step" framing. The limitations section (§21) must restate this simplification; it is not silently
assumed.

## 12. Gate treatment (held constant, not the tested variable)

Trend gate (RSI-override-below-200SMA), earnings blackout gate, and the gated-name exclusion (§6)
apply **identically across Arms A, B, and C** — exactly as `t1t2_trim_backtest.md` and
`trend_backtest.md` each held every non-tested rule at production values so only the one variable
under test could explain a result. No arm gets a looser or stricter gate than production.

## 13. Target-room, cluster, and issuer-constraint treatment (held constant)

`caps.clusters` (semis ≤25% of book: ASML/TSM/NVDA/AVGO/KLAC; power_infra ≤20%: ETN/GEV/PWR) and
the 8% effective-issuer / 40% AI-platform common-driver no-add ceilings (`issuer_lookthrough.yaml`)
apply identically across all three arms, exactly as `allocate.py plan()` already applies them in
production — clip or block a buy, never trim, unchanged from current doctrine. A name's own
`target_pct` in `targets.yaml` is the same room ceiling in every arm. None of this is the
experimental variable; it is held constant so a cluster-cap bind can be measured as its own metric
(§14) without being confused with a ladder-timing effect.

## 14. Metrics

Reported per arm, per asset-class segment (§5/§15), for the full window and the 2022 sub-period
(§16) separately:

- **Return:** annualized time-weighted return (TWR, primary); money-weighted/IRR return if
  methodologically supportable given the fixed monthly-deposit schedule (secondary — disclosed as
  omitted if not computable cleanly, never approximated silently).
- **Risk:** maximum drawdown (MaxDD).
- **Execution friction:** cash drag ($ and % of cumulative deposits sitting idle, time-weighted
  average), deployment speed (median calendar days from a cycle's deposit to that cycle's dollars
  being fully deployed), unfilled-capital duration (days an individual rung's dollars remain
  unfilled before filling or expiring per §10), turnover (count of simulated buy transactions ÷
  total dollars deployed), number of transactions.
- **Portfolio-shape outcomes:** concentration drift (maximum single-name weight deviation from its
  `target_pct` observed during the run), cluster-cap interactions (count of cycles where a
  cluster-cap or 8%/40% ceiling actually clipped or blocked a candidate buy), target-gap closure
  (% of the roster's cumulative starting target gap closed by the end of the window).
- **Regime participation:** downside participation (arm return during the 2022 sub-period relative
  to Arm C) and upside participation (arm return during the remaining, rising portion of the window
  relative to Arm C) — reported, not separately thresholded (§17 applies to the full-window
  headline numbers only).

Return outcomes, risk-control outcomes, and execution-friction outcomes are reported as three
visually distinct groups in the output report — never blended into one composite score. No
composite, weighted, or opaque index of these metrics is computed at any point.

## 15. Asset-class-segmented reporting (robustness check 1)

Every headline metric in §14 is reported **separately** for (a) individual equities, (b) broad
ETFs (SPY/VEA/VWO), and (c) GLD. A pooled, blended figure across all three segments may be shown
as a supplementary total but is never the primary reported number and never the number the §17
adoption threshold is checked against in isolation — the threshold check (§17) is applied
per-segment; a study that passes on a blended number while failing on the equity segment alone is
not a clean H0/H1/H2 result and must be disclosed as segment-divergent, not summarized away.

## 16. 2022 bear sub-period check (robustness check 2)

Every prior closed backtest in this repository's Decisions Log discloses the same honest caveat:
the 2021-06-01 window contains exactly one real bear stretch (2022), not a large or diverse sample
of adverse regimes. This study reports every §14 metric for the 2022 calendar-year sub-period
separately from the full-window figure, using the same disclosure discipline, rather than letting
a mostly-rising full window mask what happened during the one adverse stretch it actually contains.

## 17. Success threshold and adoption rule (NUM-0001 provenance)

**Threshold: 1.0 percentage point annualized TWR**, pre-committed before simulation, identical to
every closed backtest in this repository (`rung_backtest.md`, `regime_backtest.md`,
`trend_backtest.md`, `weight_backtest.md`, `trim_backtest.md`, `t1t2_trim_backtest.md`). NUM-0001
provenance class: **evidence-bounded governance selection** — this value is not independently
derived from a statistical-power calculation for this specific study; it is a governance-selected
consistency threshold matching this repository's own established practice, disclosed as such, not
presented as empirically derived.

**MaxDD tolerance: 1.0 percentage point**, mirroring `t1t2_trim_backtest.md`'s own precedent that
a TWR win bought with a materially deeper MaxDD does not count as a clean win. Same NUM-0001
provenance class.

(Arm B's fixed −5%/−10%/−15% pullback percentages carry their own, separate NUM-0001
classification — **research assumption**, a §2 contextual class, not a §1 binding-value class —
recorded in §4 above, not repeated here.)

**Adoption rule:** No result produced under this study — however strong, on any segment —
automatically changes `levels.py`, `targets.yaml`'s `levels:` block, or any production behavior.
A result meeting or exceeding the threshold on a per-segment basis (§15), with the MaxDD tolerance
also met, is reported as an evidence-based **recommendation only** — retain, simplify, adopt, no
change, or insufficient evidence (§18) — requiring its own separate, later governance decision
(its own new decision-record filing, independently reviewed and principal-accepted, meeting this
repository's full evidentiary bar) before any production file is touched. This mirrors
`MARGIN-0005` §13 exactly, restated for this domain.

**Non-adoption rule:** a result inside both the TWR and MaxDD thresholds on a segment is NO CHANGE
for that segment, closed under the same "no re-runs without a new regime in the data" discipline
every other closed backtest in this repository's Decisions Log already carries.

## 18. Valid outcomes

The study is not required to produce a change. Valid, equally legitimate outcomes: retain current
methodology; simplify to a less complex methodology (per segment); adopt Arm B's approach (per
segment); no change because differences are immaterial; evidence insufficient (§9's minimum-history
exclusions removed too much of a segment to draw a conclusion, disclosed by name). A null or
inside-threshold result is a complete, valuable answer, not a failed study.

## 19. Crypto decision (pre-registered, mirroring MARGIN-0005 §7's explicit crypto gate)

**Outcome (b): crypto (BTC, ETH, SOL) is excluded from this study's evidentiary scope entirely.**
No equity/fund/GLD finding from Arms A/B/C may be applied to BTC/ETH/SOL by inference or
extrapolation — the audit that produced this filing's lead found no retained evidence supporting
that transfer, and crypto rows already carry materially different production doctrine (no
trend/RSI/earnings timing gate applies to crypto, per `targets.yaml`'s own comment and the July
2026 Decisions Log "conviction-sizing, not a timing call" entry). A separate future crypto-specific
ladder study, if ever pursued, requires its own charter naming its own hypotheses, data source, and
threshold — not silently inherited from this one.

## 20. Prohibited post-hoc changes

Once G1 data acquisition begins (a later, separate implementation step this filing does not
perform), none of the following may change without a charter amendment (its own governance
decision, with a newly pinned protocol hash, per this document's own §22 hash-pinning discipline):
the canonical universe (§5), the gated-name exclusion (§6), the three arms and their fixed
parameterizations (§4), the data period (§9), the deposit schedule and sizing rule (§10), the
corporate-action handling (§11), the gate/cluster/issuer treatment (§12/§13), the metrics list
(§14), the success threshold or MaxDD tolerance (§17), or the crypto exclusion (§19). Silent edits
are detectable by hash mismatch and void any result produced after the edit — the same discipline
`MARGIN-0005` §3 already established for its own protocol.

## 21. Data, reproducibility, and evidence-retention requirements

A later, separate implementation PR (not opened by the governance filing this protocol supports)
must, before any simulation trial: acquire and cache split-adjusted daily bars for the frozen
universe under `research/buy_ladder_backtest/data/` (git-ignored, same convention as
`research/margin_target_study/data/.gitignore`); write `research/buy_ladder_backtest/
data_manifest.yaml` naming exact source, acquisition timestamp, coverage per ticker, any
minimum-history exclusions (§5), and known limitations; use a deterministic, committed simulation
script (no live network calls at simulation time); use historical market data only, never live
brokerage or Alpaca-account data; avoid look-ahead bias (a rung fill or gate decision on day N may
use only data available through day N); retain the frozen universe snapshot and the frozen
`targets.yaml`/`gates.yaml` snapshot used, by commit SHA; retain the full output report under
`research/buy_ladder_backtest/` or `reports/`; include a limitations section restating §11's
price-return simplification, §9's data-period boundary, and any §5 minimum-history exclusions; and
undergo independent review (per `OPS-0007` §1's twelve-point capability-based standard) of both
methodology and results before any adoption-rule outcome (§17) is acted on.

## 22. Hash pinning

This protocol's SHA-256 is computed and pinned in
`governance/decisions/LADDER-0001-canonical-buy-ladder-backtest-authorization.md` §3, exactly as
`MARGIN-0005` §3 pins `PROTOCOL_V2.md`. **No simulation may run before the authorizing PR merges
and the pinned hash verifies against the committed blob** (`git show <merge>:<path> | sha256sum`).
Any later change to this file is a charter amendment: its own governance decision, with a newly
pinned hash.

**Bounded correction (same day, this PR, pre-merge, pre-principal-acceptance):** an independent
exact-head review of PR #214 (reviewed head `0f8c8d795687409cec866ac6b8a77a41a247e76f`) returned
APPROVE with two MINOR findings, both corrected in this pass before any further review: (1) §5's
descriptive universe totals were arithmetically wrong given the already-frozen named lists — fixed
to state 31 total named equity/fund/GLD rows (21 non-gated equities + 6 gated + 3 broad ETFs + 1
GLD row) and 25 rows actually simulated (21 + 3 + 1), with no ticker added, removed, or
reclassified; (2) Arm B's fixed −5%/−10%/−15% pullback percentages (§4) had no NUM-0001 provenance
classification — added, classified as a **research assumption** (NUM-0001 §2 contextual class, not
one of §1's six binding-value classes), explicitly not empirically calibrated and not an
evidence-bounded governance selection, with no implication that these percentages are optimal.
Neither correction changes the frozen universe, arms, materiality standard, or adoption rules (§20
still governs any further change as a charter amendment). This edit changes the file's SHA-256 —
see the corrected hash in `LADDER-0001` §3, superseding the value originally pinned at PR #214's
first commit (`96f686e2dbdb10459e34a8c031d6071add59940c`).

## 23. What this protocol does not authorize

Restated here, not only in the governance filing, so this document is self-contained: no
production-code change (`allocate.py`, `levels.py`, `margin_state.py`); no dashboard integration;
no live price fetch; no brokerage or Alpaca-account access beyond the read-only historical-bar
client already used by every existing `backtest_*.py` script; no order of any kind; no executable
buy ladder; no current ticker recommendation; no trim rule; no SOL reduction; no ICE purchase; no
cash or margin deployment; no Constitution change; no Intelligence-to-allocator coupling; no
automated scoring or ranking. This protocol authorizes exactly: a frozen research question, a
frozen method, and — once a later, separate implementation PR executes it — a report. Nothing
else.
