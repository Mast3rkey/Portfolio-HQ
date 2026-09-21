# Result-free current-architecture evidence and V2 input remediation

**Recorded:** 2026-09-20. **Base:** `c62a98aad8217def4c10a4b021bef198b8a0fcc9`. No historical simulation, sealed-data read, account access, credential use, or production mutation occurred.

## V2 validator and lawful successor chain

`python whole_portfolio_robustness_v2_preregistration_validator.py` exits 1 with `pin drift: issuer_lookthrough.yaml`: frozen predecessor `6cf4e4…`, current PR398 bytes `33d3797…`. This is a substantive predecessor mismatch. A separately accepted pre-execution amendment/successor must preserve the old pin, add current bytes and PHQ-2026-08 authority, require PR398's common-driver rule, admit DFF/SOL evidence, recompute its own digest, pass result-free validation, and receive exact-head review. Changing an expected hash or deleting the error is prohibited. Evidence acquisition is not acceptance.

DFF admission requires both publication and historical vintage/as-of applicability for every required observation. A current schedule/page cannot prove past availability. SOL admission requires one independently authenticated SOL/USD spot-daily provider, predecessor 2021-05-31, complete 2021-06-01–2026-07-31 coverage, provider semantics, retained raw bytes, UTC acquisition time, receipt, and raw/transform hashes. No stitch, fill, proxy, or shorter window.

## Author acquisition log (exact, no receipt invented)

At 2026-09-20 UTC, the author first ran `curl -L --fail --silent --show-error URL -o PATH` for the NY Fed EFFR URL. It failed before origin access: `curl: (56) CONNECT tunnel failed, response 403`; the `set -e` command stopped, so later lines in that command—including every planned SOL API request—did **not** run.

The author then ran the following exact loop form for five pages: `curl -A 'Mozilla/5.0' -L -sS -o /dev/null -w '%{http_code}\n' "$u"`. Each returned curl status 56, displayed HTTP code `000`, and reported proxy CONNECT 403:

- `https://www.newyorkfed.org/markets/reference-rates/effr`
- `https://www.federalreserve.gov/releases/h15/`
- `https://www.finra.org/rules-guidance/rulebooks/finra-rules/2264`
- `https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf`
- `https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductcandles`

No Coinbase candle endpoint was actually contacted; it remained planned after the first command aborted. No bypass, credentials, paid source, partial file, origin bytes, or origin hash is claimed. The independent coordinator reports separately reaching public primary pages through its web tools; that is reviewer-side observation, not author acquisition evidence and does not close DFF vintage or SOL raw-data gates. Both lanes remain unresolved.

## R1 synthetic integration reproduction (result-free)

The focused synthetic test uses X closes `[100,100]`, weight `1`, min lot `1`, dates 2000-01-03/04, and deposits `100` each day. Scenario cap is 1.8, APR/free tier are zero. Day 0 returns `RepaymentDecision(leverage_target=1.8)`; day 1 calls `r1_deposits_first(..., is_deposit_day=True, target_leverage=1.25)`. Observed day-0 gross/debt are 180/80. On day 1 the pre-trade hook computes REPAY 55 and `_fund_repayment` sells 0.55 X **before** the 100 deposit event; ending gross/cash/debt are 200/25/25.

This reproduces a research-engine integration-order gap, not a historical result and not a claim that production R1 is deployed or broken. R1's current formula is trim-funded (`gross - target × opening net equity`), whereas cash-funded deposit-first repayment must be separately defined and limited by cash actually received. A future mandatory integration regression must prove: real broker/maintenance-call cures execute first; otherwise deposit cash is received before cash-funded R1; no repayment uses unavailable cash; only any defined residual trim may sell; and no spurious sell/rebuy occurs on the same deposit cycle. The old isolated `min(contribution,debt)` helper was removed because it neither represented nor proved engine ordering.

## Literature/source ledger

| Source | Relevance | Limitation | Author state |
|---|---|---|---|
| Bailey et al., *Probability of Backtest Overfitting* | Multiple-testing, selection and holdout discipline | Supplies no optimal cap, floor, target, cutoff, or trial budget | Page/PDF blocked before origin; no bytes/hash |
| FINRA Rule 2264 | General official margin-risk/mechanics disclosure | No broker-specific maintenance/buffer formula or optimal limit | Blocked before origin; no bytes/hash |
| NY Fed EFFR / Federal Reserve H.15 | Official publication/vintage leads | Current pages alone do not prove historical as-of vintages | Blocked for author; unresolved |
| Coinbase Exchange candle docs/API | Candidate provider semantics/raw-data route | Must prove single-provider identity, complete daily coverage and hashes | Docs blocked; candles not attempted; unresolved |

## Completed versus planned

Completed: repository hashes; current V2 validator; scoping-checklist tests; exact synthetic R1 reproduction. Planned, not completed: official evidence acquisition, executable successor design, runners, historical trials, and sealed evaluation. The next executable action is **result-blind completion and independent acceptance of a successor specification**; there is no runner command in this draft.
