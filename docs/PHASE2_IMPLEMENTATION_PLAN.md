# Phase 2 Implementation Plan — Margin Governance Layer

_2026-07-17, Rev 2 · Planning only. `decision_log.yaml` (repo root) was created in Rev 1 — it's new, inert data nothing reads yet, not a change to production behavior. **No production code (`allocate.py`, `targets.yaml`, `holdings.yaml`, or any file in the live `--cash`/`--review`/`--margin` path) has been modified.** Everything else below is a proposal. Rev 2 adds: an explicit risk-only confirmation for the state machine, a hysteresis design comparison (Option A vs. B, with a recommendation — not implemented), a full margin repayment framework (the deleveraging-necessity/strategic-repayment split and the four-tier waterfall), a consolidated future-backtest-requirements section, and explicit Phase 2A-2D sequencing with a hard gate before any `allocate.py` change. Waiting for approval before any of it is implemented._

---

## 1. Governance-layer enforcement mapping

Before any schema or state design, here is exactly how each doctrine requirement from `docs/MARGIN_DOCTRINE.md`'s "Margin Intelligence Engine Doctrine" section is enforced structurally in what follows — not as a promise, as a design property checkable against Sections 3-4 below.

| Doctrine requirement | Enforcement mechanism |
|---|---|
| Margin is NOT a timing signal | The state machine (Section 4) takes exactly three input categories: leverage ratio, buffer %, concentration score. No price, regime, volatility-as-trigger, or valuation input exists anywhere in the schema (Section 3) or the state criteria (Section 4). There is no field to put a timing signal in even by accident. |
| Margin does NOT create alpha | No component proposed here computes or influences a *buy* decision. Every function in Section 4/6 only ever reduces, blocks, or holds — the type signature of every state's "action" is drawn from `{no_change, reduce_new_draws, block_and_recommend_paydown}`, which structurally excludes "increase." |
| Margin amplifies existing portfolio edge, doesn't create it | Unaffected by this phase — `margin_capacity()`'s leverage-cap/buffer-floor math, which already embodies this (it clips borrowing to a fixed ratio of whatever equity already exists), is untouched. |
| Margin states are risk states only, never opportunity states | Section 4's four states (`NORMAL`/`CAUTION`/`RESTRICTED`/`FORCED_DELEVER`) are explicitly, monotonically risk-ordered — each state is strictly a superset of the prior state's risk conditions. There is no state whose criteria involve anything getting *better* triggering an escalation; escalation only fires on leverage/buffer/concentration getting worse. |
| No "borrow more because conditions look favorable" logic | Directly tested — Section 7's test plan includes a dedicated property-style test (`test_no_state_ever_recommends_increasing_leverage`) that asserts this for every state, not just checks it by inspection. |

---

## 2. `decision_log.yaml` — done, not a proposal

Created at repo root (config/state layer, alongside `targets.yaml`/`holdings.yaml`, not under `docs/` — it's structured data meant to be read by future tooling, not narrative documentation). Schema exactly as requested: `decision_id`, `date`, `category`, `decision`, `rationale`, `supporting_artifact`, `status`.

**Migrated, this pass, exactly two entries** (per explicit "margin doctrine decisions only" scope):
- `MARGIN-0001` — the 2026-07-13 margin doctrine revision (1.8x cap, 30% floor, margin-timing rejected). `supporting_artifact: null` — stated explicitly as doctrine-driven, not backtest-derived, and `status: pending_evidence` rather than `active`, because Track 2 exists specifically to test whether the numeric level is evidence-supported.
- `MARGIN-0002` — the 2026-07-15 T1/T2 concentration ceiling. `supporting_artifact: reports/t1t2_trim_backtest.md`, `status: active`.

**Explicitly not migrated this pass:** every other `CLAUDE.md` Decisions Log entry, including the closely-related "Semis cluster cap: leverage asymmetry" entry (2026-07-14). Flagged as a candidate for a broader future migration pass, not started here.

---

## 3. Margin policy schema — proposed `targets.yaml` extension (NOT applied)

```yaml
margin:
  # --- EXISTING, unchanged ---
  leverage_cap: 1.8
  buffer_floor_pct: 30.0

  # --- PROPOSED, not yet added to the real targets.yaml ---
  states:
    caution:
      leverage_fraction_of_cap: null    # e.g. 0.65 -- PLACEHOLDER, not evidence-backed
      buffer_comfort_multiplier: null   # e.g. 1.75 -- PLACEHOLDER
    restricted:
      leverage_fraction_of_cap: null    # e.g. 0.85 -- PLACEHOLDER
      buffer_comfort_multiplier: null   # e.g. 1.25 -- PLACEHOLDER
    # forced_delever has no new parameter -- it reuses buffer_floor_pct directly,
    # exactly as margin_capacity() already does today.
    hysteresis:                          # see Section 5 -- NOT implemented, schema
                                           # shape only, included so the eventual
                                           # decision doesn't require a second
                                           # schema revision
      enabled: null                       # PLACEHOLDER -- true/false, pending Section 5's decision
      deescalation_persistence_syncs: null  # PLACEHOLDER -- "N" in Section 5's Option B

  concentration_adjustment:
    enabled: true
    tightening_coefficient: null   # the "k" in inner_threshold = cap x base x (1 - k x score),
                                     # per MARGIN_INTELLIGENCE_DESIGN.md §3 -- PLACEHOLDER
    min_fraction: null             # floor on how far concentration can tighten a threshold --
                                     # PLACEHOLDER

  repayment:
    # See Section 6 for the full waterfall this section parameterizes.
    redirect_fraction_caution: null     # PLACEHOLDER -- pending the repayment-policy backtest
    redirect_fraction_restricted: null  # PLACEHOLDER -- same
    redirect_fraction_forced: 1.0       # NOT a placeholder -- matches existing production
                                          # behavior already (Forced state blocks all margin buys)
    strategic_repayment_enabled: null   # PLACEHOLDER -- whether tier 4 of the waterfall
                                          # (Section 6) is active at all; explicitly NOT
                                          # defaulted to true -- "always repay margin
                                          # immediately" is not assumed

  debt_reduction_triggers:
    consecutive_syncs_in_elevated_state: null   # PLACEHOLDER

  emergency_deleveraging:
    repayment_target_buffer_multiplier: null   # PLACEHOLDER -- e.g. 1.5
```

**Every `null` above is deliberate, not an oversight.** This schema defines *shape*, not *values*. Filling any of them in is Phase 3+ work, gated on the corresponding backtest (Section 8).

---

## 4. Margin state machine — design (NOT implemented)

**Four states, exactly as specified. Confirmed: risk classifications only.**

| State | Objective criteria | Proposed system behavior (Phase 3+, not this phase) |
|---|---:|---|
| `NORMAL` | leverage ≤ `caution.leverage_fraction_of_cap` × cap, AND buffer ≥ floor × `caution.buffer_comfort_multiplier` | No change from current behavior. |
| `CAUTION` | leverage between the Caution and Restricted thresholds, OR buffer between floor×`restricted.buffer_comfort_multiplier` and floor×`caution.buffer_comfort_multiplier` | Informational only — displayed, no behavior change. |
| `RESTRICTED` | leverage above the Restricted threshold (still ≤ cap — `margin_capacity()`'s existing clip already prevents exceeding the cap itself), OR buffer between the floor and floor×`restricted.buffer_comfort_multiplier` | New margin-funded buys reduced (not fully blocked) — mechanism is Section 6's waterfall tier 2, not decided in this document. |
| `FORCED_DELEVER` | buffer < `buffer_floor_pct` (existing rule, unchanged) | Existing behavior (block all margin-funded buys), unchanged this phase. Section 6's waterfall tier 1. |

### Explicit confirmation: no state may

Stated directly, one line per prohibition, each tied to why it structurally can't happen rather than just asserted:

1. **No state may increase leverage.** Every state's action is drawn from a closed set — `{no_change, reduce_new_draws, block_and_recommend_paydown}` — that contains no "increase" member. This isn't a runtime check; there is no code path that could produce that output because the type doesn't allow it.
2. **No state may recommend borrowing.** The only margin-quantity outputs any state produces are a *reduction* target (`repayment_split()`, Section 6) or a *paydown* amount (`recommended_paydown()`, Section 6, `FORCED_DELEVER` only). Nothing computes a "draw more" amount anywhere in this design.
3. **No state may use valuation.** The state classifier's only inputs are leverage ratio, buffer %, and `concentration_risk_score()` (itself computed purely from existing cluster-cap/T1T2-ceiling proximity, not price target or fair-value judgment). No price-vs-fair-value comparison exists in the input set.
4. **No state may use volatility as an entry signal.** Volatility doesn't appear in the state classifier's inputs at all in this design (it's a candidate input for the *separate*, already-speced tail-risk decomposition in `MARGIN_INTELLIGENCE_DESIGN.md`, which describes *outcomes* under stress — it never triggers a state transition).
5. **No state may time the market.** Regime status (QQQ vs. 200-EMA) is not an input anywhere in Section 3's schema or Section 4's criteria — consistent with `regime_backtest.md`'s standing verdict and the Margin Doctrine's explicit rejection of regime-gated margin.

**Explicitly excluded state names, restated:** `OPPORTUNISTIC`, `AGGRESSIVE`, `BULLISH`, `VALUATION_OPPORTUNITY` — none describe account risk. No future phase adds a fifth state along these lines.

**Concentration adjustment applies uniformly**: `concentration_risk_score()` tightens every threshold above, never loosens one.

---

## 5. Hysteresis analysis (design comparison — NOT implemented)

The prior revision flagged, but didn't resolve, whether state transitions should have memory. Formalized here as a real comparison with a recommendation, per instruction — implementation stays separate and gated until approved on its own.

### Option A — pure recalculation every run

Every state is computed fresh from current leverage/buffer/concentration on every `allocate.py` run. No persisted state.

- **Pros:** Simple. Transparent — the state shown is always a direct, auditable function of the current numbers, nothing else. No hidden memory to reason about, debug, or explain. Architecturally consistent with every other rule in this system (the leverage cap, buffer floor, cluster caps, T1/T2 ceiling are all stateless, recomputed fresh every run — no exceptions exist today).
- **Cons:** Possible oscillation — an account sitting right at a threshold boundary could flip between `CAUTION` and `RESTRICTED` (or `RESTRICTED` and `FORCED_DELEVER`) on small, ordinary day-to-day value changes, producing a noisy, flapping display.

### Option B — cooldown / de-escalation persistence

Escalating to a higher-risk state happens immediately (no delay — risk should never be under-reported). De-escalating to a lower-risk state requires the account to have qualified for the lower state for N consecutive observations (syncs) before the display actually moves down.

- **Pros:** Avoids whipsaw — a single good sync right after a bad one doesn't erase the display of recent risk, which may itself be informative (e.g., "this account was in Forced Deleveraging 2 syncs ago" is a fact worth a beat before declaring "all clear").
- **Cons:** Introduces genuine state memory — a new concept nothing else in this codebase's architecture has. Requires a new persisted field (where does "how many consecutive qualifying syncs" live — `holdings.yaml`? a new file?) and a new parameter (`N`) that itself needs justification, joining the list of not-yet-evidence-backed numbers (Section 3's `deescalation_persistence_syncs: null`). Asymmetric by design (escalation instant, de-escalation delayed) — asymmetry is usually the right call for a risk system, but it's one more thing to get right, not free.

### Recommendation: Option A, for this phase — with a named condition for revisiting it

**Recommend Option A (pure recalculation)** for the informational-only integration this phase's Section 4 behavior column describes (`NORMAL`/`CAUTION` don't change behavior at all; `RESTRICTED`/`FORCED_DELEVER`'s behavior changes are display + a passive redirect rule, not a hard block that would be jarring to flip on and off). Reasoning:
- It's the only option consistent with this codebase's existing architecture without a new justification burden.
- Oscillation's actual cost, at this phase, is cosmetic (a flapping display line), not financial — no real dollars move differently depending on which side of a boundary the account flaps across on a given day, since `RESTRICTED`'s behavior is a redirect *fraction*, not a hard gate.
- Introducing hysteresis now would mean choosing `N` without evidence, which is exactly the pattern this whole project has been careful to avoid (see every `null` in Section 3).

**Named condition to revisit:** if a future phase makes `RESTRICTED`'s behavior a hard gate (fully blocking margin buys, not just redirecting a fraction) rather than a soft one, oscillation's cost stops being cosmetic — flapping between "blocked" and "allowed" every sync would be a real usability and possibly a real-dollar problem (missing a genuine gap-fill opportunity because the display flapped down for one sync). **That specific change should trigger a fresh look at Option B**, not an assumption that Option A still holds. Flagged here so it isn't forgotten when that decision comes up.

---

## 6. Margin repayment framework (design — NOT implemented)

### The necessary distinction

**A) Deleveraging necessity** — objective, mechanical, non-optional triggers:
- Forced delever (buffer < `buffer_floor_pct`) — the existing hard rule.
- Buffer breach warning zone (`RESTRICTED`/`CAUTION` states) — not yet a breach, but the account is closer to one than `NORMAL`.
- Leverage cap violation — shouldn't occur given `margin_capacity()`'s existing clip (it structurally prevents new draws from exceeding the cap), but included as a named trigger category for defense-in-depth, in case a future change to the clipping logic ever introduces a gap.

**B) Strategic repayment** — optional, evidence-gated, never assumed:
- Excess cash beyond what a deposit cycle's gap-fill needs.
- Realized profits from trims that would otherwise fully redeploy.
- Portfolio growth that mechanically restores leverage headroom (already happens today as a side effect — Section 7 of `MARGIN_INTELLIGENCE_DESIGN.md`'s Rev 1 noted this, no new logic needed for the mechanical effect itself).

**The distinction matters because the two categories have different urgency and different evidentiary bars.** Category A is a survival question — the system should act on it every time, no cost-benefit debate, exactly like the existing forced-delever rule. Category B is a return/risk-tradeoff question — whether to prioritize debt reduction over redeployment when nothing is actually at risk — and that tradeoff needs its own evidence (Section 8's repayment-policy backtest) before any rule fires by default. **Conflating the two would mean treating an optional, unproven optimization with the same mandatory urgency as an actual survival response** — exactly the "always repay margin immediately" assumption this section is designed not to make.

### The repayment waterfall

Four tiers, strictly ordered — a lower-numbered tier's condition, if triggered, takes priority over every higher-numbered tier:

1. **Protect against forced liquidation.** `FORCED_DELEVER` state: 100% of available cash and trim proceeds directed to debt paydown until buffer clears the floor by `emergency_deleveraging.repayment_target_buffer_multiplier`. Non-negotiable, matches existing behavior (margin buys already fully blocked here), just adds a concrete recommended amount rather than a bare block message. **This is Category A — always fires, no evidence gate.**
2. **Restore acceptable leverage.** `RESTRICTED` state: a portion of trim proceeds (`repayment.redirect_fraction_restricted`, currently `null`) redirected to debt to bring leverage back toward the `CAUTION`/`NORMAL` boundary specifically — a targeted, partial paydown, not a full one. **Category A in spirit (responding to an elevated-but-not-emergency risk state) but the specific *fraction* redirected is Category B in evidentiary standard — it needs Section 8's repayment-policy backtest before any non-zero default ships.**
3. **Maintain strategic allocation.** Once tiers 1-2's conditions aren't active (i.e., the account is in `NORMAL` or `CAUTION`), **normal deployment resumes** — gap-fill buys toward tier targets proceed exactly as today, and the system does **not** keep prioritizing debt reduction just because debt exists. This tier is the explicit answer to "do not assume always repay margin immediately": once risk is under control, restoring/maintaining the target allocation outranks continuing to chase debt reduction. This is the tier most likely to be skipped by an implementation that defaults to "pay down whenever possible" — named explicitly here so it isn't.
4. **Repay remaining excess debt.** Only below tiers 1-3, and only if `repayment.strategic_repayment_enabled` is explicitly `true` (currently `null` — not assumed on): a lower-priority, genuinely optional paydown using cash that isn't needed for tier 3's allocation maintenance. **Purely Category B** — this tier doesn't exist in production until its own backtest (Section 8) supports it, and even then it's explicitly the *lowest* priority tier, not the default behavior of extra cash.

**This waterfall is a design, not running code.** Sections 3's `null` placeholders are exactly the parameters this waterfall needs filled in before any tier beyond 1 (which already matches existing forced-delever behavior) can activate.

---

## 7. Test plan (test cases specified; test code not written this phase)

Every test below is a **pure-function unit test**, no live data, no I/O — same standard as the existing 12 tests in `test_margin.py`.

| Test | Cases |
|---|---|
| **Leverage cap enforcement** | Existing `margin_capacity()` coverage unchanged. New: state classifier correctly identifies `RESTRICTED` between the Restricted threshold and the cap, `NORMAL` below the Caution threshold, using fixture threshold values (not real, still-unset config). |
| **Buffer floor enforcement** | Existing hard-floor coverage unchanged. New: `CAUTION`/`RESTRICTED` trigger correctly on buffer values between the floor and the comfort multipliers, boundary-tested exactly at each threshold. |
| **Concentration tightening** | A leverage level classifying `NORMAL` at concentration 0.0 classifies `CAUTION`/`RESTRICTED` at concentration 1.0. `concentration_risk_score()` itself: under-cap clusters → score < 1.0, matches tightest name; exactly-at-cap → score == 1.0; empty roster → score == 0.0, not an error. |
| **Forced delever behavior** | Existing coverage (`allowed == 0.0`, `forced is True`) unchanged. New: `recommended_paydown()` — known debt/leverage → expected leverage-based estimate; non-Forced states → no recommendation. |
| **Repayment trigger logic** | `repayment_split()` per waterfall tier: tier 3 conditions (`NORMAL`/`CAUTION`) → 100% redeploy, 0% to debt (directly tests that "always repay" is NOT what happens). Tier 2 (`RESTRICTED`) → split matches `redirect_fraction_restricted` at ≥2 different configured values. Tier 1 (`FORCED_DELEVER`) → 100% to debt. Tier 4 → 0% redirected whenever `strategic_repayment_enabled` is `null`/`false` (proves the "not assumed on" default holds), non-zero only when explicitly enabled and configured. |
| **No state can recommend increasing leverage** | Property test over a systematic `(leverage, buffer, concentration_score)` sweep (leverage 0-2x cap, buffer 0-100%, concentration 0.0-1.5): every resulting action is drawn from `{no_change, reduce_new_draws, block_and_recommend_paydown}`, never `increase`. Built to fail loudly if `increase` is ever added to the action enum at all, regardless of whether any state currently uses it. |
| **Hysteresis (only if Option B is ever approved — not this phase)** | Not written now, since Option A is recommended and Option B isn't being built. If revisited per Section 5's named condition: escalation fires on the first qualifying observation; de-escalation requires exactly `N` consecutive qualifying observations, boundary-tested at `N-1` (should not de-escalate) and `N` (should). |

---

## 8. Future backtest requirements (documented for later validation — none run this phase)

Consolidated from `MARGIN_INTELLIGENCE_DESIGN.md` §5 and `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md`, restated here as the explicit gate list for filling in Section 3's placeholders. None of these run in Phase 2 — they're prerequisites for Phase 3+.

1. **Unlevered baseline comparison** — Track 2's own core question (margin vs. no margin, hypothetical, labeled as such). Gates whether *any* of this framework's non-emergency tiers (waterfall tiers 2-4) are worth building at all.
2. **Fixed leverage comparison** — a sweep across leverage levels (e.g. 1.2x-2.0x, per the earlier "sustainable leverage" framing), gating `targets.yaml`'s `leverage_cap` itself and Section 3's `states.*.leverage_fraction_of_cap` thresholds.
3. **Repayment policy comparison** — the Model A (permanent leverage, never repay unless forced) / Model B (profit harvesting — maintain target leverage, excess pays debt) / Model C (risk reset — reduce debt after gains/volatility spikes/concentration increases) comparison. Gates Section 6's waterfall tier 2 and tier 4 fractions directly — this is the single backtest every `redirect_fraction_*` placeholder in Section 3 is waiting on.
4. **Concentration-adjusted leverage comparison** — does `concentration_risk_score()` tightening the effective cap (not just the display threshold) improve MaxDD without materially costing TWR. Gates whether Section 3's `concentration_adjustment` block should ever affect real deployment capacity, versus staying display-only indefinitely.

Each, when run, follows the standing framework discipline: pre-committed threshold stated before results, MaxDD tolerance alongside TWR, one test one verdict, written up in `CLAUDE.md`'s Decisions Log and cross-referenced into `decision_log.yaml`.

---

## 9. Implementation sequencing

**Phase 2A — Documentation/schema only.** *(This document, Rev 2, plus `decision_log.yaml` from Rev 1 — complete as of this revision, pending your approval.)* No code.

**Phase 2B — Pure `margin_state.py` calculations.** New file, mirroring `indicators.py`/`regime_gate.py`'s existing pattern: `concentration_risk_score()`, `classify_margin_state()`, `recommended_paydown()`, `repayment_split()`. Pure functions only — no I/O, no imports from `allocate.py`, fully unit-testable in isolation. **Not started until Phase 2A is approved.**

**Phase 2C — Tests.** Section 7's full test plan, written against Phase 2B's actual function signatures. **Not started until Phase 2B exists**, and per the standing "tests before integration" rule already governing every prior phase of this project, these tests must all pass before Phase 2D begins.

**Phase 2D — Integration into `allocate.py`.** Display-only (state label + recommendation in `render()`), no change to `plan()`'s buy/trim logic. **Hard gate, stated explicitly: no `allocate.py` change of any kind happens until `margin_state.py` has full, passing, independently-reviewable test coverage from Phase 2C.** This is not a soft preference — it's the same discipline that kept the T1/T2 ceiling's tests (`test_margin.py`) written and passing before that rule touched `plan()`, applied here with an even harder line since margin code carries more consequence than a single trim rule.

Sections 3, 4, 5, and 6's `null` placeholders are **not filled in by any of Phase 2A-2D** — that's Phase 3+, gated on Section 8's backtests, a distinct and later effort from getting the governance *machinery* built and tested.

---

## What this phase deliberately does not do

- Does not add anything to `targets.yaml`. Section 3's schema is fully specified but exists only in this document until reviewed.
- Does not write `margin_state.py` or any test code (Phase 2B/2C, not started).
- Does not change `allocate.py`'s behavior in any way, including display (Phase 2D, not started, hard-gated on 2C).
- Does not pick any of the placeholder values in Section 3's schema, or decide the hysteresis question (Section 5 recommends Option A but doesn't implement it).
- Does not run any of Section 8's backtests.
- Does not assume strategic repayment (waterfall tier 4) is ever on by default — `strategic_repayment_enabled` stays `null`, not `true`.

Waiting for approval before starting Phase 2B.
