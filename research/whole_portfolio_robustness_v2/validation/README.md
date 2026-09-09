# Validation boundary

Only synthetic ledgers are permitted before independent input-freeze acceptance. The result validator
recomputes NAV, TWR primitives and disposition from ledger records rather than trusting hashes or a
simulation summary. Historical invocation remains fail-closed while `input_freeze.json` is incomplete.

## Deterministic units and formulas

Monetary fields are decimal US dollars; shares are split-normalized decimal units. Rates and returns
are decimals except source DFF and decision deltas explicitly named `_pp`. NAV is settled cash plus
unsettled net receivables plus close-valued securities. TWR is the chain product of consecutive NAV
ratios minus one; external flows are prohibited. One-way cost is traded notional times bps/10,000.
Positive realized HIFO gains use frozen holding-period/asset tax character; losses receive no credit.
The bootstrap samples paired baseline, alternative and lawful risk-free observations with one stationary
index path, mean block 21, 2,000 draws and seed 20260907. `correction_replication` alone supplies the
exact 15-of-18 vote and decision bootstrap; context supplies only its separate direction/link gate.

Whole-study fixtures must use the byte-pinned 1,298-session XNYS sequence and each retained UTC close,
including DST and early closes. Each path carries its immediately preceding NAV and the compounded gross
lagged-DFF return for that valuation interval; `$100,000` is used only at inception. The full registry
shares immutable synthetic primitives and retains compact paths plus event/lot audit rows to bound memory;
the independent validator replays all 1,887 calendar transitions from those primitives and binds every
compact path back to its exact case/cell/variant simulation. Fixed regimes, expanding-origin metrics,
both registered bootstraps, pathwise concentration, standalone named gates, foreign vetoes and the
ordered passing set are regenerated rather than accepted as caller assertions.

Operational fields are cumulative primitive counters on each session row. Window metrics subtract the
replayed predecessor counters: turnover is traded notional divided by the window anchor NAV; cost and tax
drag are dollars; taxable realized gain is dollars without loss credit; cash drag is all calendar-day cash
interest credits; and rebalance count counts scheduled rebalance events. Missing counters are not zero.

`recovery_days` is the calendar-day distance from the peak preceding the deepest drawdown to its first
subsequent full recovery (equality qualifies); it is `null` when that drawdown remains unrecovered and zero
when no drawdown occurs. Window anchors carry the actual predecessor XNYS date. Synthetic crypto prices
are independently rebuilt from complete, ordered UTC daily bars against each pinned XNYS close; aligned
price dictionaries are comparison claims, not replay inputs.
