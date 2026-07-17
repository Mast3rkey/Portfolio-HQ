"""
phase3g_lib.py — Phase 3G sensitivity-testing execution-layer helpers.

Pure, additive utilities used ONLY by run_phase3g_sensitivity.py. Does
NOT modify margin_simulation.py, allocate.py, targets.yaml, or
holdings.yaml — everything here wraps or post-processes objects
margin_simulation.py already produces (SimulationResult, ModelCRiskReset)
without changing their behavior.

Two capabilities not exposed by margin_simulation.py's own SimulationResult
.metrics() and needed by docs/PHASE3_SENSITIVITY_PLAN.md's Model C
dimension:

1. `ModelCTriggerLogger` — a thin wrapper around a real `ModelCRiskReset`
   instance that logs every False->True transition of `.reset_active`.
   This matters because simulate() only appends a "repayment" event to
   SimulationResult.events when repay_amount > 0 -- a trigger that fires
   but finds leverage already at/below the reset target (see
   test_model_c_no_repay_needed_if_already_under_target_after_crash in
   test_margin_simulation.py) activates reset_active with NO logged
   event at all. Counting logged repayment events alone would silently
   undercount true trigger activations. The wrapper still delegates
   every call to the real policy unchanged -- it only observes.

2. `estimate_turnover()` -- same upper-bound methodology
   docs/results/PHASE3_MODEL_B_ANALYSIS.md §4 already used and disclosed
   (total repaid via trim-funded events, as a share of total deposited
   capital), extracted into a reusable, testable function instead of
   being computed ad hoc in a probe script.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from margin_simulation import ModelCRiskReset, PortfolioState, RepaymentDecision


@dataclass
class ModelCTriggerLogger:
    """Wraps a ModelCRiskReset instance. Delegates every call unchanged;
    additionally records the day_index of every reset ACTIVATION (the
    False->True transition of the wrapped policy's `.reset_active`) in
    `activation_days`. Does not alter the wrapped policy's decisions in
    any way -- purely an observer, so wrapping a policy and using the
    wrapper in place of the bare policy in simulate() cannot change
    simulation results, only add visibility into them."""
    inner: ModelCRiskReset
    activation_days: list[int] = field(default_factory=list)

    def __call__(self, state: PortfolioState, prior_gross: float | None) -> RepaymentDecision:
        was_active = self.inner.reset_active
        decision = self.inner(state, prior_gross)
        if (not was_active) and self.inner.reset_active:
            self.activation_days.append(state.day_index)
        return decision

    @property
    def n_activations(self) -> int:
        return len(self.activation_days)


def estimate_turnover(total_repaid: float, total_deposited: float) -> float:
    """Upper-bound estimate of repayment-driven turnover as a fraction of
    total deposited capital -- exact only when repayments are funded
    entirely via trim (no idle cash), which docs/results/
    PHASE3_MODEL_B_ANALYSIS.md §4 already established is the common case
    in this harness (min_lot keeps idle cash near zero after allocation).
    Returns 0.0 for total_deposited <= 0 rather than raising -- a
    defensive guard for a degenerate input, not a real simulation state
    this harness ever produces."""
    if total_deposited <= 0:
        return 0.0
    return total_repaid / total_deposited


def event_amount_stats(events: list[dict], kind: str) -> dict:
    """Count/sum/mean/median/max for a given event kind (e.g.
    'repayment') from a SimulationResult.events list. Returns zeros for
    an empty match rather than raising -- an arm where nothing of this
    kind happened (e.g. Model C not triggering) is a real, expected
    result to report, not an error."""
    amounts = sorted(e["amount"] for e in events if e.get("kind") == kind)
    n = len(amounts)
    if n == 0:
        return {"count": 0, "total": 0.0, "mean": 0.0, "median": 0.0, "max": 0.0}
    total = sum(amounts)
    median = amounts[n // 2] if n % 2 == 1 else (amounts[n // 2 - 1] + amounts[n // 2]) / 2.0
    return {"count": n, "total": total, "mean": total / n, "median": median, "max": amounts[-1]}


def twr_maxdd_ratio(ann_twr_pct: float, max_drawdown_pct: float) -> float | None:
    """Same simple TWR/|MaxDD| lens docs/results/PHASE3_MODEL_B_ANALYSIS.md
    §7 used, explicitly labeled there (and here) as one descriptive lens,
    not a verdict or a ranking criterion. Returns None (not a number) for
    a zero-drawdown arm rather than dividing by zero -- a real possible
    input (e.g. an arm with no debt ever drawn), not an error."""
    if max_drawdown_pct == 0:
        return None
    return ann_twr_pct / abs(max_drawdown_pct)


def gap_vs_baseline(value: float, baseline: float) -> float:
    """Simple percentage-point gap, value minus baseline -- extracted
    only so every table in the sensitivity report computes this
    identically rather than by ad hoc subtraction scattered through the
    report-generation script."""
    return value - baseline
