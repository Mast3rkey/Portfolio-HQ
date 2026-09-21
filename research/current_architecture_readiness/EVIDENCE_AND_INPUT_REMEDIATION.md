# Result-free current-architecture evidence and V2 input remediation

**Recorded:** 2026-09-21. **Base:** `c62a98aad8217def4c10a4b021bef198b8a0fcc9`. No historical simulation, sealed-data read, account access, credential use, or production mutation occurred.

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

## Current-roster coverage and provenance ledger (metadata only)

This ledger was derived without opening price outcomes. The canonical population is the 36 rows at `targets.yaml::destination`. “Available” means retained metadata/receipt bytes exist; it is weaker than “admissible for a successor.”

| Current population | Existing evidence available | Admissibility / consequence |
|---|---|---|
| 25 ladder-admitted identities: `AMZN ASML AVGO CEG COST ETN GEV GLD GNRC GOOGL ISRG KLAC LLY META MSFT NVDA PANW PWR RTX SPY TMO TSM V VEA VWO` | LADDER-0003 `input_disposition.json::price_files` records provider, dates, transform hash, and raw/receipt paths and hashes for its 2021-06-01–2026-07-31 scope. | Admission is limited to LADDER-0003. CEG begins 2022-02-02 and GEV 2024-04-02; predecessor stitching is prohibited, disproving a complete 2021-06-01 common current-roster window. |
| Gated equities `SNPS ICE SPGI WM RKLB TSLA` | RISK-0001 inventory records successful raw receipts and candidate transforms. LADDER kept their capital in cash, so they are absent from its selected 25. | Availability is not successor admission. RKLB's lawful inception is 2021-08-25. SPGI has an unresolved 2026 distribution valuation convention; affected cells must abstain under existing gates. |
| `BTC ETH SOL` | RISK-0001 inventory records successful BTC/ETH/SOL receipts/candidates; selected BTC/ETH transforms exist. | RISK-0005 limits inherited evidence. SOL has no independently accepted successor anchor/receipt proving the required predecessor and complete window; this ledger cannot promote existing bytes. |
| `RESERVE CASH` | Canonical rows and cash-accounting rules exist; no price series is appropriate. | A successor must use declared cash/rate accounting with admissible DFF evidence, never drop these rows or use a security proxy. |

The exposed PHQ-2026-01 matrix does not cure these gaps. **Result-blind conclusion:** some-scope receipts exist for every priced identity, but no common admissible window for all current rows is demonstrated. Identified bottlenecks are GEV/CEG/RKLB lawful inceptions, SPGI action treatment, SOL successor evidence, and DFF vintage/release-clock evidence. No asset is dropped and no earlier history is imputed.

## Reviewer-verified official methodological leads (not acquired records)

The independent coordinator verified on 2026-09-21 that FRED's official `series_vintagedates` documentation describes revision/new-release dates, excludes unchanged releases, and requires a registered API key; `series_observations` supports `vintage_dates` and real-time periods. These are reviewer-side methodological leads, not author-acquired DFF records:

- `https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html`
- `https://fred.stlouisfed.org/docs/api/fred/series_observations.html`

A lawful DFF reconciliation must retain, for every required observation: the exact observations request with explicit real-time/vintage parameters; the vintagedates response; separate official dated release-clock evidence because unchanged releases are excluded; credential-free request parameters, status, acquisition UTC, semantics, byte counts and raw hashes; a no-forward-lookup transform and hash; and a mechanical raw-to-transform reconciliation. Missing dates, inaccessible key routes, or ambiguous release clocks fail the affected input rather than using today's series.

The coordinator also verified that Alpha Vantage documents `DIGITAL_CURRENCY_DAILY` as daily cryptocurrency history refreshed midnight UTC with USD quotes and an API-key requirement: `https://www.alphavantage.co/documentation/`. SOL coverage, exchange identity, predecessor day, complete window, and raw response remain unverified, so it is not admitted. This PR registers no account, extracts no secret, purchases nothing, and bypasses no access control.

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
| FRED vintagedates/observations docs | Reviewer-verified real-time/vintage query methods | Key required; unchanged releases excluded, requiring separate release-clock proof | Method lead only; no DFF records acquired |
| Alpha Vantage digital-currency docs | Reviewer-verified daily/midnight-UTC/USD method description | Key required; SOL coverage and exchange identity unverified | Method lead only; not admitted |

## Completed versus planned

Completed: repository hashes; current V2 validator; scoping-checklist tests; exact synthetic R1 reproduction; metadata reconciliation of all 36 current rows; and a DFF vintage/release-clock acquisition recipe. Planned, not completed: official observations, executable successor design, runners, historical trials, and sealed evaluation. The next action is result-blind successor-specification completion under MARGIN-0005's existing gates; this artifact adds no personal-approval condition and provides no runner command.
