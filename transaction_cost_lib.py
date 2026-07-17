"""
transaction_cost_lib.py — Transaction cost sensitivity analysis,
execution-layer helpers only.

Per docs/TRANSACTION_COST_SENSITIVITY_PLAN.md. Does NOT modify
margin_simulation.py, allocate.py, targets.yaml, holdings.yaml, or
margin_state.py. No engine change was needed for this analysis:
SimulationResult.events already carries every repayment event's exact
day and dollar amount (confirmed by reading margin_simulation.py's
_fund_repayment() and simulate() before writing this module) — nothing
here required extending output capture.

Implements NO new margin rule, NO cost-aware trading behavior, and does
NOT change how simulate() executes trades. Every function here only
POST-PROCESSES an already-completed SimulationResult with a disclosed,
hypothetical cost assumption — a lump-sum approximation, not a
re-simulated cost-aware backtest (docs/TRANSACTION_COST_SENSITIVITY_
PLAN.md §6's explicitly disclosed simplification).
"""

from __future__ import annotations

from backtest_regime import twr_annualized


def event_costs(events: list[dict], bps: float, kind: str = "repayment") -> list[float]:
    """Cost (in dollars) for each event of the given `kind`, as
    `bps` basis points of that event's dollar amount. 100 bps = 1%, so
    a 5 bps assumption is `bps=5.0` (this function divides by 10,000
    internally, not by 100 -- 5 bps is 0.05%, not 5%)."""
    if bps < 0:
        raise ValueError(f"bps must be >= 0, got {bps}")
    rate = bps / 10_000.0
    return [e["amount"] * rate for e in events if e.get("kind") == kind]


def total_transaction_cost(events: list[dict], bps: float, kind: str = "repayment") -> float:
    """Sum of event_costs() -- the total hypothetical dollar cost across
    every event of the given kind."""
    return sum(event_costs(events, bps, kind))


def cost_adjusted_twr(book_values: list[float], flows: dict[int, float],
                      total_cost: float) -> float:
    """Annualized TWR after subtracting `total_cost` as a single lump
    sum from the FINAL day's book value only (docs/TRANSACTION_COST_
    SENSITIVITY_PLAN.md §6's disclosed first-order approximation --
    does not compound the cost drag forward, does not model reduced
    reinvestment capacity after each trim). Reuses backtest_regime.py's
    already-tested twr_annualized() unmodified -- the only new logic
    here is constructing the cost-adjusted value series to feed it.

    Returns 0.0 for an empty book_values series (nothing to compute),
    matching twr_annualized()'s own no-returns convention rather than
    raising."""
    if not book_values:
        return 0.0
    adjusted = list(book_values)
    adjusted[-1] = adjusted[-1] - total_cost
    return twr_annualized(adjusted, flows)
