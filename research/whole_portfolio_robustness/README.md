# Whole-portfolio robustness execution

> **Current evidence status (2026-09-07): EVIDENCE LIMITED — NOT DECISION GRADE.**
> A post-execution audit found source-selection, corporate-action, SOL coverage,
> and RTX identity-boundary defects that the original gate did not surface. The
> retained `RETAIN_BASELINE` output is preserved historical evidence and must not
> be cited as empirical validation of the baseline. See
> [`evidence_disposition.json`](evidence_disposition.json) and
> [`RISK-0005`](../../governance/decisions/RISK-0005-whole-portfolio-evidence-disposition.md).

`PORTFOLIO-ROBUSTNESS-0001` is a preregistered, advisory-only comparison of
the accepted portfolio against five bounded alternatives. It does not optimize
weights, use account holdings, change policy, authorize leverage, or execute
trades. Stage 1 remains **UNARMED AND NOT EXECUTABLE**.

## Frozen execution sequence

1. `whole_portfolio_robustness_engine.py` verifies every registered input and
   derives the six reconciled 100% target portfolios without renormalizing the
   accepted baseline.
2. `whole_portfolio_robustness_runner.py validate` truncates market prices at
   the 2023-12-29 confirmation boundary, runs every registered non-holdout
   window at the frozen decision cell, repeats a deterministic path, and emits
   a receipt binding the inputs, implementation files, commit, and seed.
3. `whole_portfolio_robustness_runner.py execute` refuses to run if any byte or
   commit differs from that receipt. It then evaluates the holdout and every
   registered window, portfolio, cadence, cost, and tax cell.
4. `whole_portfolio_robustness_result_validator.py` checks the complete
   Cartesian registry, path alignment, finite values, bootstrap and sensitivity
   registries, output hashes, policy boundaries, and reproduces the disposition
   from the factual outputs.

The post-merge GitHub workflow reacquires the exact hash-pinned, quarantined SOL
bytes, validates non-holdout behavior, and only then exposes the one governed
result artifact from the same immutable commit. Ordinary pull-request CI tests
the implementation but never installs those quarantined bytes or runs the
holdout.

## Decision cell and sensitivities

The sole decision cell is quarterly rebalancing, 10 basis points of one-way
cost, and `TAXABLE_MID`. Annual cadence, 0/25-basis-point costs, and the other
tax profiles are required sensitivities; they cannot replace the decision cell
after results are known. The disposition may only retain the baseline or
recommend a separate policy review. It never adopts a target change.

Machine-readable `metrics.json`, `bootstrap.json`, and
`sensitivity_matrix.json` are facts. `disposition.yaml` and `results.md` contain
the threshold-driven inference. `limitations.md` records the current-roster,
look-through, tax, provider, cash-rate, and non-predictive boundaries.
