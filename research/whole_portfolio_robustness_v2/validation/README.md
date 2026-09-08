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
