# Phase 2B Review — `margin_state.py`

> **STATUS CORRECTION (2026-07-18, `decision_log.yaml` MARGIN-0003):** Phase 2D has since shipped (see `allocate.py`, commented `# Phase 2D`), contradicting this review's stop point ("Stopping here. Not proceeding to Phase 2D."). Of this review's findings: the `concentration_tightening_coefficient` sign gap (Section 1) is fixed (`margin_state.py` validates `concentration_tightening_coefficient < 0.0`). The four related parameters flagged in "Remaining risks" item 2 (`caution_leverage_fraction`, `caution_buffer_comfort_multiplier`, `restricted_leverage_fraction`, `restricted_buffer_comfort_multiplier`) remain unvalidated as of this correction.

_2026-07-17 · Review-only pass, no production code modified. Every claim below was checked directly against `margin_state.py`'s actual code and, where a claim was non-obvious, against a live Python run — not re-asserted from the implementation summary. One real gap was found (Section 1) and is documented, not fixed, per the explicit "do not modify production code" instruction for this pass._

---

## 1. State severity hierarchy

```
NORMAL → CAUTION → RESTRICTED → FORCED_DELEVER
```

**Leverage cap breach ⇒ `FORCED_DELEVER`: confirmed.** `classify_margin_state()` line ~215: `leverage_breach = leverage_ratio > leverage_cap`; if true, returns `FORCED_DELEVER` regardless of buffer health. Verified live: gross=$200/debt=$100 (leverage 2.0x, cap 1.8x) with a healthy 60% buffer still returns `FORCED_DELEVER` with `violated_constraints == ["leverage_cap_exceeded"]` and no buffer-related entry — the breach is attributed correctly, not conflated with a buffer problem that isn't present. Covered by `test_leverage_cap_breach_forces_delever_even_with_healthy_buffer`.

**Buffer floor breach ⇒ `FORCED_DELEVER`: confirmed.** Same code path, `buffer_breach = buffer_pct is not None and buffer_pct < buffer_floor_pct`. Boundary-tested: exactly at the floor (30.0% vs. a 30.0% floor) does **not** trigger — matches the "hard cutoff, not < vs. ≤ ambiguity" precedent `test_margin.py` already set for `margin_capacity()`. Covered by `test_buffer_floor_breach_forces_delever` and `test_buffer_exactly_at_floor_is_not_forced`.

**Concentration pressure can tighten but never loosen: NOT fully confirmed — a real gap found.** The tightening formula (`_tighten()`, roughly `multiplier = max(min_fraction, 1.0 - k × score)`) is only guaranteed non-loosening when `k ≥ 0`. **`concentration_tightening_coefficient` (`k`) has no validation anywhere in the module** — confirmed by grepping every `raise ValueError` in the file; `k` is absent from that list, alongside `caution_leverage_fraction`, `restricted_leverage_fraction`, and both buffer comfort multipliers, none of which are range-checked either.

Reproduced live, not just inferred: at leverage 1.546x (cap 1.8x, caution threshold 0.85× → raw boundary 1.53x), `k=0.0` correctly returns `CAUTION`. With `k=-1.0` and `concentration_score=1.0`, the identical leverage level returns `NORMAL` — the threshold moved from 1.53x up past 1.546x, i.e. it **loosened**, not tightened, because `1.0 - (-1.0)(1.0) = 2.0`, uncapped on the upper side (`max()` only floors the multiplier, it doesn't ceiling it at 1.0).

**This is a real, reproducible gap in what was claimed as a structural guarantee, not a hypothetical edge case.** It doesn't affect anything today — nothing calls `margin_state.py` yet, and every existing test passes `k` values ≥ 0 (0.0, 0.3, 0.5, 10.0), so the test suite never exercised the sign. `test_concentration_never_loosens_a_threshold` verifies the *intended* behavior correctly for the k-values it uses, but doesn't test that a negative `k` is rejected, because at the time it was written the assumption was that a negative `k` simply wouldn't be passed — an assumption this review found isn't enforced. **Recommended fix for the next approved code pass, not applied now:** add `if concentration_tightening_coefficient < 0: raise ValueError(...)` alongside the existing validation block, and cap the multiplier's upper bound at `1.0` explicitly (`min(1.0, max(min_fraction, 1.0 - k*score))`) as defense-in-depth even after the input is validated, so the guarantee holds structurally, not just by trusting a valid `k`.

**Missing data increases verification requirements but does not create a false emergency state: confirmed.** Verified live: `buffer_pct=None` with healthy leverage (100/20, well under any reasonable cap) returns `NORMAL`, not `FORCED_DELEVER` or `RESTRICTED` — the only effect is `verify_margin_data` appended to `allowed_actions` and an explanatory line in `reasons`. Same for stale-but-present data (`buffer_data_age_days` past the threshold): `violated_constraints` gains `"stale_margin_data"` and `verify_margin_data` is added, but `current_state` stays whatever the leverage/buffer numbers actually support — staleness never forces an escalation on its own. Covered by `test_missing_buffer_data_flags_verify_but_does_not_force_a_state`, `test_stale_buffer_data_flags_verify_and_violated_constraint`, `test_fresh_buffer_data_within_threshold_is_not_stale`, `test_data_age_exactly_at_threshold_is_not_stale`.

---

## 2. Action semantics

**Confirmed: actions are risk-management instructions only, structurally, not by convention.**

`ALLOWED_ACTIONS = frozenset({continue_normal_operations, reduce_risk, prioritize_deleveraging, verify_margin_data})` — verified by direct read, exactly the four requested, no fifth value anywhere in the module. `MarginStateResult.__post_init__` raises `ValueError` if `allowed_actions` ever contains anything outside this set — verified live via `test_margin_state_result_rejects_disallowed_action`, which constructs a result with `"increase_leverage"` and confirms it raises rather than silently accepting it.

**No action implies borrowing more, increasing leverage, timing the market, or deploying margin — confirmed two ways:**
1. **By inspection:** every one of the four allowed strings describes a risk *response* (continue as-is, reduce exposure, prioritize paying down debt, double-check the data) — none describes acquiring exposure, timing a decision, or drawing capital.
2. **By test:** `test_no_state_ever_recommends_increasing_leverage` checks every member of `ALLOWED_ACTIONS` for the substrings `"increase"`, `"borrow"`, `"add_margin"`, `"deploy"` and then re-checks every action actually returned across a 14,175-combination sweep (verified by direct count in this session, not assumed) — both checks pass. **Market timing specifically** isn't a string-matchable property, so it's confirmed differently: no input to `classify_margin_state()` is a price, a regime indicator, or a volatility reading (verified by reading the full parameter list — every parameter is a leverage/buffer/concentration/staleness quantity), so there is no channel through which a market-timing judgment could reach an action even indirectly.

---

## 3. Future repayment compatibility

**Confirmed: the current architecture leaves room for `repayment_policy.py` without requiring a `margin_state.py` rewrite.**

The composition works because `MarginStateResult` is a plain, stable data contract — a future `repayment_policy.py` would consume it (specifically `current_state` and `risk_metrics`) rather than reach into `margin_state.py`'s internals:

```
margin_state.py                    repayment_policy.py (future)          allocation engine
  classify_margin_state()   ──▶      takes MarginStateResult      ──▶      capital deployment
  -> MarginStateResult               + repayment-specific config          (unchanged, out of
     .current_state                  (redirect fractions, waterfall        scope for this review)
     .risk_metrics                   tier settings -- still null in
     .reasons                        targets.yaml, per the Phase 2
                                      plan's Section 3)
                                    -> a repayment recommendation
                                       (separate data contract,
                                       not yet designed)
```

**Checked specifically: does a future repayment calculator need anything `risk_metrics` doesn't already carry?** `risk_metrics` currently holds `net_equity`, `leverage_ratio`, `utilization`, `concentration_score` — not raw `gross`/`margin_debt` directly. But those are algebraically recoverable from what's already there (`gross = net_equity × leverage_ratio`, `margin_debt = gross − net_equity`), so a repayment calculator has two equally valid options: reconstruct them from `MarginStateResult`, or take them directly from the same caller inputs `classify_margin_state()` itself received (which the caller already has, since it's the one supplying them). Either path works without touching `margin_state.py`.

**Checked: does `FORCED_DELEVER`'s lack of a dollar paydown amount block repayment integration?** No — `recommended_paydown()` (the dollar-amount function) was deliberately deferred out of Phase 2B's scope (documented in the Phase 2B completion summary) precisely so it could live in a future module once `emergency_deleveraging.repayment_target_buffer_multiplier` has a backtested value. Adding it later is additive — a new function, not a change to `classify_margin_state()`'s signature or return type.

**One thing worth flagging for whoever designs `repayment_policy.py`:** it will need `concentration_source` (the label of which cap is tightest) if it's going to implement the Phase 2 plan's waterfall tier 2 ("restore acceptable leverage" — a *targeted* paydown, potentially informed by which position/cluster is driving the concentration score). That label is already threaded through into `reasons` as prose text, but not as a structured field on `MarginStateResult`. Not a blocker — `reasons` is human-readable and could be parsed or `concentration_risk_score()` could just be called again directly by the repayment module with the same inputs — but a structured `concentration_source` field on `MarginStateResult` would be a cleaner seam. Noted for the next design pass, not fixed now (out of scope for a review-only pass).

---

## 4. Test coverage summary

**32 tests added** (`test_margin_state.py`), all passing alongside the existing 38 (70 total, confirmed via a combined run).

**Breakdown:**
- `concentration_risk_score()`: 3 (empty input, max-not-average, single entry)
- Normal state: 2
- Leverage cap breach: 2 (breach despite healthy buffer; exactly-at-cap is not a breach)
- Buffer floor breach: 3 (breach; exactly-at-floor; both breaches simultaneously, correctly attributed to both)
- Insolvency (`net_equity ≤ 0`): 2
- Missing/stale data: 4
- Concentration tightening: 4 (escalation happens; monotonicity across a score sweep; floor on the tightening multiplier; unset thresholds never fire)
- Invalid inputs: 11 (9 parametrized `classify_margin_state()` cases + 2 `MarginStateResult` construction cases)
- Property test: 1 (the 14,175-combination sweep)

**Property test scope, precisely:** varies `gross` (5 values), `margin_debt` as a fraction of gross including >1.0 (insolvent) (7 values), `buffer_pct` including `None` (9 values), `concentration_score` (5 values), and `caution`/`restricted` leverage fractions including `None` (3×3 values) — **14,175 combinations, 0 errors, every result's actions inside `ALLOWED_ACTIONS`**, re-verified live in this review. **What it does NOT vary**, stated honestly rather than implied by the large combination count: `leverage_cap` and `buffer_floor_pct` are held fixed at production values (1.8, 30.0) throughout the sweep; buffer comfort multipliers are only ever `None` or one fixed pair (1.5/1.2); `concentration_tightening_coefficient` is fixed at `0.3` throughout, `concentration_min_fraction` at `0.5`; `buffer_data_age_days` is never varied (always `None` in the sweep). The sweep is wide on the account-state dimensions (gross/debt/buffer/concentration/thresholds-on-or-off) but narrow on the policy-coefficient dimensions — which is exactly why Section 1's `k`-sign gap wasn't caught by it.

**Remaining risks, stated plainly:**
1. **The `concentration_tightening_coefficient` sign gap (Section 1).** The one confirmed, reproducible issue this review found. Zero current impact (nothing calls this module yet), but should be fixed before Phase 2D wires real config through, since a misconfigured `targets.yaml` value (even accidental — a typo'd minus sign) would currently silently loosen risk thresholds instead of raising an error.
2. **The other four threshold parameters** (`caution_leverage_fraction`, `restricted_leverage_fraction`, both buffer comfort multipliers) **are also unvalidated** for sign/range. Lower severity than the concentration coefficient specifically (a negative fraction would produce visibly nonsensical thresholds rather than silently inverting a specific guarantee), but the same category of gap, worth closing in the same pass.
3. **No real threshold values have ever been exercised end-to-end**, because none exist yet (`targets.yaml`'s proposed values are all `null`). Every `CAUTION`/`RESTRICTED` test uses fixture values chosen for the test, not the eventual real configuration — this is expected and correct for Phase 2B, but means Phase 2D's integration will be the first time this module runs against numbers nobody has looked at yet, once Phase 3's backtests fill them in. Worth a fresh sanity pass at that point, not assumed to be covered by today's fixture-based tests.
4. **Hysteresis is out of scope** (Option A, no memory, was the Phase 2 plan's recommendation) — not a gap, a deliberate deferral, restated here only so it isn't mistaken for an oversight.

---

## Summary

Three of four review areas confirm the implementation matches its stated guarantees, verified directly rather than assumed. **One area — concentration tightening — does not fully hold**: the code correctly tightens for every `k` value actually exercised by the test suite, but nothing prevents a negative `k` from inverting the guarantee, and this review reproduced that inversion live. Recommending this be fixed (validation + a defensive upper-bound clamp) in the next approved code-touching pass, alongside validating the four related threshold parameters. Not fixed in this pass, per the explicit review-only instruction.

Stopping here. Not proceeding to Phase 2D.
