"""
tax_treatment_lib.py — Tax treatment sensitivity analysis, execution-
layer helpers only.

Per docs/TAX_TREATMENT_SENSITIVITY_PLAN.md. Does NOT modify
margin_simulation.py, allocate.py, targets.yaml, holdings.yaml, or
margin_state.py. No engine change was needed or made: SimulationResult
.events already carries every repayment event's exact dollar amount --
nothing here required extending output capture or adding cost-basis
tracking (explicitly out of scope per the plan's §3/§5).

Implements NO tax-aware trading behavior, NO cost-basis tracking, and
does NOT change how simulate() executes trades. Every function here
only POST-PROCESSES an already-completed SimulationResult's repayment
events with a disclosed, hypothetical, UPPER-BOUND tax assumption --
100% of each repayment event's dollar amount is treated as realized
gain (docs/TAX_TREATMENT_SENSITIVITY_PLAN.md §5's directionally-
justified-but-not-accurate ceiling, not an estimate of actual realized
gain or actual tax owed).

Reuses transaction_cost_lib.cost_adjusted_twr() for the net-TWR
computation -- the mechanics (deduct a lump-sum dollar amount from the
final day's book value, then reuse backtest_regime.twr_annualized())
are identical whether the deducted amount represents a transaction
cost or a tax drag; no duplicate implementation was written.
"""

from __future__ import annotations

from transaction_cost_lib import cost_adjusted_twr

HOLDING_PERIODS = ("all_long_term", "all_short_term")


def taxable_realization_upper_bound(events: list[dict], kind: str = "repayment") -> float:
    """Upper-bound taxable base: sum of every event of the given kind's
    dollar amount, treating 100% of it as realized gain (zero return of
    basis). This is a disclosed ceiling, not an estimate of actual
    realized gain -- per docs/TAX_TREATMENT_SENSITIVITY_PLAN.md §5, this
    harness has no cost-basis tracking (deliberately not added, per the
    plan's explicit "do not add cost-basis tracking" constraint) and
    therefore cannot compute an accurate, non-upper-bound figure.

    Only events of `kind` (default "repayment") are included --
    deposits, interest accrual, and margin draws are explicitly
    excluded, per the plan's requirement to apply tax sensitivity only
    to repayment-generated realized amounts, never to deposits,
    unrealized gains, or other non-repayment portfolio movement."""
    return sum(e["amount"] for e in events if e.get("kind") == kind)


def tax_drag(taxable_base: float, rate: float) -> float:
    """Dollar tax drag: `rate` (a fraction, e.g. 0.15 for 15%, not a
    percentage or basis-point value) applied to the upper-bound taxable
    base. Never scales the base itself -- this function does not
    convert the upper-bound assumption into an estimate; it only
    applies a disclosed rate to the disclosed ceiling, and the result
    must be labeled the same way (upper bound, not estimate) wherever
    it is used."""
    if rate < 0:
        raise ValueError(f"rate must be >= 0, got {rate}")
    return taxable_base * rate


def net_twr_after_tax(book_values: list[float], flows: dict[int, float],
                      drag: float) -> float:
    """Thin, explicitly-named wrapper around transaction_cost_lib.
    cost_adjusted_twr() -- reused, not reimplemented, since the
    mechanics (lump-sum deduction from the final book value, then
    backtest_regime.twr_annualized()) are identical for a tax drag as
    for a transaction cost. Named separately here purely for call-site
    clarity in tax-specific code, not because the computation differs."""
    return cost_adjusted_twr(book_values, flows, drag)
