# POST-REVIEW ADDITIVE DISCLOSURE SUPPLEMENT

This supplement addresses the two `MAJOR` reporting findings in independent full RESULTS review
`4941983592` under effective `RISK-0004`. It is additive disclosure of already-frozen evidence for
`RISK-0001-EXECUTION-ATTEMPT-002`. It does **not** replace, revise, or modify the frozen historical
`RESULTS.md` or `LIMITATIONS_AND_SURVIVORSHIP.md`.

This supplement introduces no new economic result, trial, metric, threshold, provider,
interpretation, sizing, recommendation, or policy. All four family dispositions remain
`unable_to_determine`. Attempt-2 authorization remains `CONSUMED`; rerun, retry, recomputation, and a
third attempt remain prohibited. The results remain research evidence only and have no sizing or
portfolio-policy effect.

## Frozen accounting and recovery censoring

The frozen ordered inventory contains 777 registered cells: 609 executed eligible cells and 168
governed null/ineligible cells. Reserve cells are zero, and duplicate, missing, and extra trial IDs
are each zero. The null/ineligible accounting and affected representations are:

| Frozen state | Cells | Affected representations |
|---|---:|---|
| `NOT_APPLICABLE_PRE_INCEPTION` | 93 | AVGO 3; BTC 9; CEG 12; ETH 9; GEV 15; GNRC 3; META 3; PANW 3; RKLB 9; RTX 9; SOL 9; TSLA 3; V 3; VEA 3 |
| `MISSING_SOURCE_DATA` | 3 | SOL 3 |
| `KNOWN_DATA_GAP` | 24 | ETN 6; GNRC 6; VWO 6; WM 6 |
| `CORPORATE_ACTION_UNRESOLVED` | 6 | SPGI 6 |
| `CONDITIONAL_ASSET_NOT_ACQUIRED` | 42 | GLDM 21; SGOL 21 |
| `QUALITY_GATE_FAILED` | 0 | None |

The frozen diagnostics record 133 censored recovery observations. Censoring means the affected path
had not recovered by its governed window end; it is a right-censored recovery observation, not a
zero-duration recovery, an imputed recovery, or evidence that recovery occurred. It therefore limits
recovery-direction evidence without changing any recorded cell or disposition. The scenario-expanded
cell file contains the same scenario-independent path censoring on each registered scenario; the
governed diagnostic count is the 133 unique recovery observations.

Trace: `cell_results.json` fields `registered_cell_count`, `execution_count`,
`ineligible_or_null_count`, `state_counts`, and ordered `records`; `diagnostics.json` field
`censored_recovery_count`; Protocol V1 §§10, 15, and 19.

## Selection conditioning, missingness, and truncation

The cohort is frozen and selection-conditioned. In particular, the 27 current evidence-ready equity
constituents are not the historical opportunity set. These results therefore do not establish
universe-wide performance, an exhaustive opportunity set, final membership, or what a historical
investor could have selected from at each date.

Pre-inception observations were kept as `NOT_APPLICABLE_PRE_INCEPTION`; no predecessor history was
stitched and no observation was fabricated or zero-filled. SOL specifically has 9 pre-inception
cells and 3 `MISSING_SOURCE_DATA` cells. Its shorter, history-limited coverage makes the CRYPTO result
sensitive to representation availability across the mandatory asset-available and family-common
paths.

The frozen known-gap states affect VWO, ETN, GNRC, and WM, with 6 cells for each representation.
VWO's gap matters directly because SPY, VEA, and VWO are all mandatory, separate broad-market
representations. The frozen corporate-action truncation affects SPGI in 6
`CORPORATE_ACTION_UNRESOLVED` cells. Those periods remain null rather than being guessed, stitched,
or repaired.

Trace: `cell_results.json` ordered `records` and `state_counts`; `diagnostics.json` fields
`selection_conditioned_cohort_warning`, `equity`, and `limitations_are_preserved_not_imputed`;
Protocol V1 §§4, 9–11, 16, and 17.

## Actual provider/fallback reliance

The frozen registry actually binds 630 registered cells to `YAHOO_FINANCE_CHART` and 21 registered
cells to `COINBASE_EXCHANGE`. These are actual registered-cell source bindings, not hypothetical
“if used” fallbacks. Their payloads remain quarantined and hash-pinned under the frozen licensing and
receipt treatment. This actual reliance does not itself imply provider invalidity; it limits source
provenance to the frozen provider coverage, receipts, gaps, and no-stitching rules.

Trace: `eligibility_matrix.json` field `records[].source_provider`; Protocol V1 §§7–8.

DFF remains the analytical opportunity-cost comparator only, using the registered actual/360
convention and one-Federal-Reserve-business-day lawful-availability lag. It is not cash, a residual
destination, or a fifth sleeve. Missing required DFF evidence would make the affected
opportunity-cost metric unavailable rather than invite a substitute or forward fill.

Trace: Protocol V1 §§8, 12–13 and the frozen preregistration comparator contract.

## Gold-peer admission and representation sensitivity

IAU was admitted and is the only admitted conditional gold peer. SGOL failed the zero-unresolved-gap
admission requirement because its frozen evidence records one unresolved required-session gap. GLDM
failed the governed correlation gate: its stored overlap total-return correlation is
`0.9943199988624067` (rounded to `0.9943199989` in review), below the preregistered `0.995` minimum.
The failed peers remain excluded as `CONDITIONAL_ASSET_NOT_ACQUIRED`; neither was silently promoted,
ranked, or substituted.

Trace: `diagnostics.json` fields `gold_peer_admission_evidence` and `admitted_gold_peers`; Protocol
V1 §§4, 10, 16, and 17.

## Family-result traces

The traces below explain the frozen evaluator outcomes; they do not select LOWER, the historical
reference, or HIGHER and do not create recommendations.

- **EQUITY — `unable_to_determine`.** LOWER improves governed path-risk and recovery direction but
  worsens opportunity cost. HIGHER worsens path risk and recovery while improving opportunity cost.
  The mandatory voting-family directions are mixed, so neither adjacent direction can determine a
  policy-review direction.
- **FUND_BROAD_MARKET — `unable_to_determine`.** VWO's frozen known-gap state prevents complete
  mandatory representation consistency across SPY, VEA, and VWO. HIGHER path risk worsens while
  recovery and opportunity-cost evidence is unavailable or otherwise non-determinative. The
  required separate-representation evidence therefore cannot determine a direction.
- **FUND_GLD_DEFENSIVE — `unable_to_determine`.** GLD and admitted IAU evidence reconcile where
  applicable, but path-risk/recovery direction and opportunity-cost direction conflict. Only IAU
  passed admission; SGOL and GLDM remain excluded under the frozen gates. The conflicting path and
  admitted-representation limits prevent a determined direction.
- **CRYPTO — `unable_to_determine`.** SOL's shorter history, 9 pre-inception cells, and 3 missing
  family-common cells leave required path/recovery evidence unavailable. BTC and ETH disagree where
  applicable, and SOL unavailability prevents the mandatory BTC/ETH/SOL representation-consistency
  gate from determining a direction.

These traces expose representation and path sensitivity rather than average it away. Under Protocol
V1, missing mandatory evidence, representation conflict, and mixed voting-family directions fail
closed to `unable_to_determine`. The final dispositions therefore remain exactly:

| Family | Frozen disposition |
|---|---|
| `EQUITY` | `unable_to_determine` |
| `FUND_BROAD_MARKET` | `unable_to_determine` |
| `FUND_GLD_DEFENSIVE` | `unable_to_determine` |
| `CRYPTO` | `unable_to_determine` |

Trace: `raw_evidence.json` fields `families.*.directions`; `disposition.json` fields
`families.*.directional_states`, `families.*.point_states`, and `families.*.result`;
`diagnostics.json` representation and gold-peer evidence; Protocol V1 §§6, 16–18; and the bounded
family traces accepted by `RISK-0004` §5.

## Immutable lifecycle and policy boundary

Attempt 2 began its first eligible registered cell at `2026-08-14T19:42:17Z` and completed at
`2026-08-14T19:44:02Z`. Its status remains
`COMPLETED_RESULTS_OBSERVED_NO_RERUN_PERMITTED`. The one RISK-0002 authorization was consumed at the
first-cell boundary. There is no retry or third attempt, and this supplement authorizes no execution,
recomputation, regeneration, reacquisition, provider substitution, or result mutation.

No family result is a recommendation. No Level-1 or Level-2 sizing, membership, holding, target,
cash, margin, leverage, allocator, ladder, chart, brokerage, or other portfolio policy is adopted or
changed. A new independent full exact-head RESULTS review is required before results acceptance or
merge.

Trace: `results/execution_receipt.json`; `disposition.json` fields `no_policy_effect`,
`automatic_adoption`, `replacement_level1_method_created`, `level2_membership_or_sizing_created`,
`whole_portfolio_constructed`, and `residual_cash_debt_margin_or_leverage_analyzed`; RISK-0004 §§2–7.
