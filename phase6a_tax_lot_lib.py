"""
phase6a_tax_lot_lib.py — Phase 6A tax-lot analysis, execution-layer
helpers only. Per docs/PHASE6A_TAX_LOT_MODELING_PLAN.md and
docs/PHASE6A_IMPLEMENTATION_APPROVAL.md.

Does NOT modify margin_simulation.py, allocate.py, targets.yaml,
holdings.yaml, or margin_state.py. Operates entirely on an
already-completed SimulationResult's `tax_lot_events` list (produced by
the Phase 6A FIFO lot ledger inside margin_simulation.py) — pure
post-processing of already-computed per-lot disposal records, no new
simulation logic, no new trading behavior.

Reuses tax_treatment_lib.net_twr_after_tax() (itself a thin wrapper
around transaction_cost_lib.cost_adjusted_twr()) for the net-TWR
computation — identical mechanics whether the deducted amount is the
Phase 3G upper-bound tax drag or this module's FIFO-realistic one.
"""

from __future__ import annotations

from datetime import date

HOLDING_PERIODS = ("short_term", "long_term")


def _holding_period_days(ev: dict) -> int:
    """Elapsed real calendar days between a tax-lot event's acquisition
    and sale dates. Computed here, not read from a pre-existing field —
    margin_simulation.py's tax_lot_events records the short_term/
    long_term classification directly (it needed the day count
    internally to derive that), but does not itself expose the raw day
    count as a separate field; deriving it here from the same two
    already-recorded date strings is a pure read, not a new simulation
    computation, and keeps this analysis pass from requiring any further
    change to the already-implemented and already-verified engine."""
    d0 = date.fromisoformat(ev["acquisition_date"])
    d1 = date.fromisoformat(ev["sale_date"])
    return (d1 - d0).days


def realized_gain_summary(tax_lot_events: list[dict]) -> dict:
    """Aggregates a SimulationResult.tax_lot_events list into the
    disposal-level metrics required by docs/PHASE6A_TAX_LOT_MODELING_
    PLAN.md's research question: total proceeds, realized gains,
    realized losses, event count, proceeds-weighted average holding
    period, and the short-term/long-term split of GAINS specifically
    (losses are not split by holding period — the requested split is
    "percentage of gains classified short-term/long-term", not of all
    disposals)."""
    n_events = len(tax_lot_events)
    total_proceeds = sum(ev["proceeds"] for ev in tax_lot_events)
    total_cost_basis = sum(ev["cost_basis"] for ev in tax_lot_events)
    total_realized_gain_net = sum(ev["realized_gain"] for ev in tax_lot_events)

    gain_events = [ev for ev in tax_lot_events if ev["realized_gain"] > 0]
    loss_events = [ev for ev in tax_lot_events if ev["realized_gain"] < 0]
    total_realized_gains = sum(ev["realized_gain"] for ev in gain_events)
    total_realized_losses = sum(ev["realized_gain"] for ev in loss_events)  # <= 0

    if total_proceeds > 0:
        avg_holding_period_days = sum(
            _holding_period_days(ev) * ev["proceeds"] for ev in tax_lot_events
        ) / total_proceeds
    else:
        avg_holding_period_days = 0.0

    st_gain_dollars = sum(ev["realized_gain"] for ev in gain_events
                          if ev["holding_period"] == "short_term")
    lt_gain_dollars = sum(ev["realized_gain"] for ev in gain_events
                          if ev["holding_period"] == "long_term")
    total_gain_dollars = st_gain_dollars + lt_gain_dollars
    st_gain_pct = (st_gain_dollars / total_gain_dollars * 100.0) if total_gain_dollars > 0 else 0.0
    lt_gain_pct = (lt_gain_dollars / total_gain_dollars * 100.0) if total_gain_dollars > 0 else 0.0

    return {
        "n_disposal_events": n_events,
        "n_gain_events": len(gain_events),
        "n_loss_events": len(loss_events),
        "total_proceeds": total_proceeds,
        "total_cost_basis": total_cost_basis,
        "total_realized_gain_net": total_realized_gain_net,
        "total_realized_gains": total_realized_gains,
        "total_realized_losses": total_realized_losses,
        "avg_holding_period_days_proceeds_weighted": avg_holding_period_days,
        "short_term_gain_dollars": st_gain_dollars,
        "long_term_gain_dollars": lt_gain_dollars,
        "short_term_gain_pct_of_gains": st_gain_pct,
        "long_term_gain_pct_of_gains": lt_gain_pct,
    }


def net_taxable_base(tax_lot_events: list[dict], floor_at_zero: bool = True) -> float:
    """The FIFO-realistic taxable base: net realized gain across every
    disposal event (proceeds minus cost basis, summed — losses offset
    gains directly, no per-lot separation). `floor_at_zero=True`
    (default) means a net realized LOSS produces zero taxable base, not
    a negative one — this harness does not model any loss-carryforward
    or ordinary-income-offset benefit (explicitly out of scope, see
    docs/PHASE6A_TAX_LOT_MODELING_PLAN.md §5/§9's wash-sale/AMT/NIIT
    exclusion, extended here to loss-deduction mechanics for the same
    reason: modeling the benefit side of losses would require tax-code
    detail this phase deliberately does not implement). This is a
    disclosed simplification, not a claim that a net loss has zero real
    tax consequence — only that this harness does not compute one."""
    total = sum(ev["realized_gain"] for ev in tax_lot_events)
    return max(0.0, total) if floor_at_zero else total
