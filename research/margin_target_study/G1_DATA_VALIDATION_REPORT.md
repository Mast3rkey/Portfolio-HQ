# G1_DATA_VALIDATION_REPORT.md — MARGIN-0005 gate G1 (data acquisition, validation, provenance, adequacy verdict)

**Program:** margin_deployment_and_target_sizing_v1
**Authority:** `governance/decisions/MARGIN-0005-margin-target-research-charter.md` (§1.2 data acquisition; §7 required data gates)
**Protocol:** `research/margin_target_study/PROTOCOL_V2.md` (§4 gap dispositions, §11 isolation, §14 T-D3, §18 G1)
**Executed:** 2026-07-24 (run date for refresh purposes: 2026-07-23, last complete session)
**Base commit:** `f984665936203c0505e8603de7c870beb64f7f21` (origin/main, matching the task's last-known merged SHA)

All content in this report is data validation. **No `simulate()` call was made, no registered trial was
consumed, no candidate, ranking, margin signal, target recommendation, trade, or order was produced.**
`trial_ledger.jsonl` and `candidate_freeze.yaml` do not exist and were not fabricated.

---

## 1. Preflight and pinned-hash verification

- Repository: `Mast3rkey/Portfolio-HQ`; branch `claude/margin-g1-data-validation-dhsm6f` created from verified `origin/main` = `f984665` (exact match to the task authority). Working tree clean at start. Open PRs at preflight: **none** — no overlapping margin/research/data/allocator/target/holdings/Intelligence/governance work in flight.
- Pinned-hash recomputation from committed blobs (`git cat-file blob origin/main:<path> | sha256sum`):
  - `PROTOCOL_V2.md` → `d794a4c09fa81dbaa147bb830da91b75221a35175f47c8bd979b75e3fc154e21` — **exact match**.
  - `pre_registration.yaml` → `e3b101e336f2ff30c013908a4c2b30918e9adf59cbb26499d2774927e472120e` — **exact match**.
- Neither pinned artifact, nor the charter, nor any production or governance file is modified by this PR.

## 2. Source plan (as executed)

| Need | Source used | Status |
|---|---|---|
| 63-ticker split-adjusted roster prices | Alpaca v2 bars, `adjustment=split`, `feed=iex` (repository-established vendor) — fresh research-side cache, refreshed through run date per charter §7 | ACQUIRED |
| PIT dividend ledger (ex-date, amount, pay date) | Alpaca v1 corporate-actions `cash_dividend` (+ split records for adjustment consistency) | ACQUIRED |
| SPY/QQQ benchmark + TR validation series | Yahoo v8 chart (quarantined namespace); Track 3 long history 1993/1999→2020-12-31 | ACQUIRED (quarantined, not committed) |
| Risk-free series | Yahoo `^IRX` fallback (protocol §10 disclosed-fallback provision) — primary Treasury/FRED sources network-blocked | ACQUIRED (fallback, disclosed) |
| Fed Funds effective | FRED / Fed H.15 / NY Fed EFFR / Treasury — **all denied by environment network policy (CONNECT 403)** | **BLOCKED (B2)** |
| Robinhood margin-rate evidence | Issuer newsroom + repository Phase-7A/doctrine anchors + flagged secondary aggregation | ACQUIRED (`data/rates/robinhood_margin_rate_evidence.yaml`) |
| Gold account-specific terms | Gmail connector (token expired), repository (no account billing evidence) | **UNVERIFIED (B3)** |
| BTC/ETH/SOL PIT daily bars 2021-06→dev boundary | Alpaca v1beta3 crypto (protocol-named method) | ACQUIRED; SOL coverage FAILS (§8) |

No source was silently substituted: every deviation from a primary source is recorded here and in
`data_manifest.yaml` with its cause (network-policy denial) and its disclosure obligation.

## 3. Untouched-test isolation (boundary implementation and proof)

Governing text: pre_registration `untouched_test_isolation` (loader truncation; development code may not
read/simulate/store/display/summarize untouched-period data) and charter §7 ("Split-adjusted price cache
verified (continuity checks), **refreshed through the run date**"). These are consistent under exactly one
reading, which G1 implements: **acquisition may cover the charter-directed range; consumption is what is
barred.** The committed repository already stores untouched-period rows (`data/backtest/*.json` ends
2026-07-10 on `main`), confirming storage-level presence with loader-level quarantine is the intended design.
The physical-truncation loader itself is gate-G2 work (test T-U1) and is **not claimed here**.

Boundary status of every G1 dataset (validator output, `data_acquisition.py validate`):

- dividend ledger max ex_date: **2025-06-30** ≤ 2025-06-30 — OK
- crypto BTC/ETH/SOL max bar: **2025-06-30** ≤ 2025-06-30 — OK (Track 2 dev boundary; nothing later acquired)
- Track 3 SPY/QQQ max session: **2020-12-31** ≤ 2020-12-31 — OK (Track 3 untouched period **not even acquired**)
- TR validation series max date: **2025-06-30** ≤ 2025-06-30 — OK
- research price cache: extends to 2026-07-23 **by charter direction**; every return-derived computation in
  G1 (discontinuity scans, T-D3, cross-checks) is hard-filtered to ≤ 2025-06-30 in code
  (`data_acquisition.py`, `validate()`/`reconcile()`); the untouched segment appears in no G1 statistic,
  table, chart, or summary.

Reproduction commands: `python3 research/margin_target_study/data_acquisition.py validate` (boundary
section at end of output) and `python3 research/margin_target_study/data_acquisition.py reconcile`.

## 4. Roster price validation (charter §7 bullet 1)

Research-side cache `research/margin_target_study/data/prices/` (63 files, 9,950,851 bytes; per-file SHA-256
in `data_manifest.yaml`):

- Ticker identity: 63/63 files match their queried symbol.
- Duplicates: **0** across all tickers. Nonpositive OHLC: **0**.
- Missing sessions vs the SPY master calendar (dev window, post-listing): 0 for 60 tickers; TSM 3
  (2021-04-19, 2021-10-25, 2022-03-08 — IEX thin-tape days, each ≤3 total), within the ≤3 acceptance line.
- Stale end dates: **none** — all 63 end 2026-07-23 (run date).
- Split discontinuities (dev window): one flag, HOOD 2021-08-04 +50.4% — a real price move (verified
  meme-rally session), not an adjustment error.
- Adjustment-mode cross-check vs the production cache `data/backtest/` on the full overlap ≤ 2025-06-30:
  **0 differing closes across all 63 tickers** — the research cache is bit-consistent with the repository's
  established split-adjusted source.
- Legacy cache inventory (65 files incl. exited TM/VMC, excluded SPCX/SKHY): coverage ends 2026-07-10;
  per-file SHA-256 recorded in `data_manifest.yaml` (`legacy_backtest_cache`). Not modified by this PR.

**Price gate: PASS.**

## 5. Point-in-time dividend ledger (charter §7 bullet 2)

`data/dividends/dividend_ledger.json`: **822 events, 47 payers**, ex-dates 2020-07-31 → 2025-06-30, from
Alpaca corporate actions with split adjustment (factors from `data/dividends/splits.json`, 19 split records
queried through the run date because as-of-now split-adjusted prices embed all splits to date).

Two acquisition-semantics defects were found and fixed during G1 (both documented in the module):
vendor duplicate rows (2, deduped on economic key) and the vendor window filtering on payable/process
rather than ex date (fixed by +120d buffered query with local ex-date filter; recovers 10 late-June-2025
events that a naive query silently drops).

Validation results:
- Uniqueness (symbol, ex_date, special): **0 duplicates**. Nonpositive amounts: **0**.
- Chronology: **0** payable_date < ex_date. Payment-date availability: **822/822 (100%)**.
- Future-date leakage: **0** events past 2025-06-30.
- Split consistency: NVDA (4:1 2021, 10:1 2024), WMT, AVGO, AMZN, GOOGL, TSLA-era splits all reconcile —
  the split-adjustment transformation agrees with Yahoo's independently split-adjusted amounts everywhere
  the sources agree on gross-vs-net convention (below).
- Full-roster cross-source comparison (not just a sample) vs quarantined Yahoo events:
  **agree 637 / disagree 55 / Alpaca-only 1 / Yahoo-only 0.** Every disagreement is cause-classified:
  - **TSM (17 events, ratio ≈0.78)** — Alpaca records net of ~21% Taiwan withholding; Yahoo gross.
  - **ASML (15 events, ratio 0.85)** — net of 15% Dutch withholding vs gross.
  - **ETN (9 events, ratio 0.75)** — Irish-DWT-net convention vs gross (US holders typically receive gross).
  - **BABA (2 events, −$0.02)** — ADS depositary fee.
  - **DHR (9) / IBM (1) / MRK (2)** — Yahoo scales pre-spinoff dividend history by its spinoff pseudo-split
    factor; Alpaca records the actual declared amounts (Alpaca is correct for these).
  - **Alpaca-only:** ASML 2024-12-02 $0.5938 — uncorroborated by the issuer's published dividend calendar;
    retained as acquired, flagged as a suspected vendor artifact (~0.02pp/yr impact, ASML passes T-D3).
- No dividend is double-counted anywhere: the primary path never touches TR-adjusted prices (T-D2/T-D4
  proofs are engine tests at G2; the *data* prerequisites they need are in place and validated).

**Ledger integrity: PASS.** One open accounting-convention decision (net-vs-gross for foreign issuers) is
escalated as **D-2**, and the structural spinoff exclusion as **D-1** (§6).

## 6. T-D3 reconciliation (charter §7 bullet 2; tolerance ±0.3pp/yr)

Method: buy-and-hold with dividends reinvested on ex-date at close, primary path (research split-adjusted
prices + PIT ledger) vs quarantined Yahoo TR (adjclose), Track 2 dev window 2021-06-01 → 2025-06-30;
Track 3 books same-source check over 1999→2020. Computed by `data_acquisition.py reconcile` — a data-
validation path, not the production simulator, consuming zero registered trials.

**Result: 57/63 tickers PASS; both Track 3 books PASS (SPY 0.003, QQQ 0.001pp/yr). 6 FAIL, all
cause-attributed; none is a ledger or double-count error:**

| Ticker | Diff pp/yr | Attribution (alpaca-leg vs yahoo-raw-leg isolation) |
|---|---|---|
| WDC | 6.813 | Sandisk spinoff 2025-02-24 (factor 1.323): price-leg structural; yahoo-raw leg passes at 0.001 |
| DHR | 2.850 | Veralto spinoff 2023-10-02 (1.128): price-leg structural; yahoo-raw leg 0.024 |
| IBM | 1.358 | Kyndryl spinoff 2021-11-04 (1.046): price-leg structural; yahoo-raw leg 0.056 |
| MRK | 1.249 | Organon spinoff 2021-06-03 (1.048): price-leg structural; yahoo-raw leg 0.013 |
| GEV | 0.665 | IEX-vs-consolidated endpoint noise on a 1.24y window (start close 139.60 vs 140.00); yahoo-raw leg 0.003 — ledger clean |
| TSM | 0.457 | Withholding convention: ledger carries net-of-21% actual US-holder cash; TR benchmark is gross. Yahoo-raw leg 0.468 confirms it is not price-sourced |

Near-tolerance disclosures (passing): ETN 0.256 (same withholding-convention divergence), ASML 0.091,
BRK.B 0.033. Median absolute diff across the 57 passers: ~0.02pp/yr.

Full 63-ticker + Track 3 table:

| ticker | window | yrs | primary CAGR | TR CAGR | diff pp/yr | verdict |
| AAPL | 2021-06-01->2025-06-30 | 4.08 | 13.691% | 13.676% | 0.015 | PASS |
| ABBV | 2021-06-01->2025-06-30 | 4.08 | 17.551% | 17.526% | 0.025 | PASS |
| AMAT | 2021-06-01->2025-06-30 | 4.08 | 8.060% | 8.052% | 0.008 | PASS |
| AMD | 2021-06-01->2025-06-30 | 4.08 | 14.804% | 14.799% | 0.005 | PASS |
| AMZN | 2021-06-01->2025-06-30 | 4.08 | 7.883% | 7.892% | 0.008 | PASS |
| ASML | 2021-06-01->2025-06-30 | 4.08 | 5.303% | 5.394% | 0.091 | PASS |
| AVGO | 2021-06-01->2025-06-30 | 4.08 | 58.050% | 58.037% | 0.013 | PASS |
| BABA | 2021-06-01->2025-06-30 | 4.08 | -13.855% | -13.860% | 0.005 | PASS |
| BRK.B | 2021-06-01->2025-06-30 | 4.08 | 13.462% | 13.495% | 0.033 | PASS |
| CAT | 2021-06-01->2025-06-30 | 4.08 | 14.387% | 14.383% | 0.004 | PASS |
| CEG | 2022-02-02->2025-06-30 | 3.41 | 71.602% | 71.529% | 0.073 | PASS |
| COST | 2021-06-01->2025-06-30 | 4.08 | 28.096% | 28.110% | 0.015 | PASS |
| CRM | 2021-06-01->2025-06-30 | 4.08 | 3.810% | 3.806% | 0.004 | PASS |
| CRWD | 2021-06-01->2025-06-30 | 4.08 | 22.549% | 22.566% | 0.016 | PASS |
| CVX | 2021-06-01->2025-06-30 | 4.08 | 11.895% | 11.902% | 0.007 | PASS |
| DELL | 2021-06-01->2025-06-30 | 4.08 | 25.731% | 25.745% | 0.014 | PASS |
| DHR | 2021-06-01->2025-06-30 | 4.08 | -4.741% | -1.891% | 2.850 | FAIL |
| EQIX | 2021-06-01->2025-06-30 | 4.08 | 3.728% | 3.717% | 0.010 | PASS |
| ETN | 2021-06-01->2025-06-30 | 4.08 | 26.284% | 26.540% | 0.256 | PASS |
| GEV | 2024-04-02->2025-06-30 | 1.24 | 192.473% | 191.808% | 0.665 | FAIL |
| GILD | 2021-06-01->2025-06-30 | 4.08 | 18.587% | 18.609% | 0.023 | PASS |
| GLD | 2021-06-01->2025-06-30 | 4.08 | 14.115% | 14.112% | 0.003 | PASS |
| GNRC | 2021-06-01->2025-06-30 | 4.08 | -17.996% | -17.998% | 0.002 | PASS |
| GOOGL | 2021-06-01->2025-06-30 | 4.08 | 10.254% | 10.252% | 0.002 | PASS |
| HOOD | 2021-07-29->2025-06-30 | 3.92 | 28.784% | 28.698% | 0.086 | PASS |
| IBM | 2021-06-01->2025-06-30 | 4.08 | 24.260% | 25.619% | 1.358 | FAIL |
| INTC | 2021-06-01->2025-06-30 | 4.08 | -18.675% | -18.676% | 0.002 | PASS |
| ISRG | 2021-06-01->2025-06-30 | 4.08 | 17.785% | 17.786% | 0.001 | PASS |
| JNJ | 2021-06-01->2025-06-30 | 4.08 | 0.874% | 0.877% | 0.003 | PASS |
| JPM | 2021-06-01->2025-06-30 | 4.08 | 17.719% | 17.687% | 0.032 | PASS |
| KLAC | 2021-06-01->2025-06-30 | 4.08 | 30.532% | 30.535% | 0.002 | PASS |
| LLY | 2021-06-01->2025-06-30 | 4.08 | 41.225% | 41.235% | 0.010 | PASS |
| LRCX | 2021-06-01->2025-06-30 | 4.08 | 11.776% | 11.767% | 0.009 | PASS |
| MA | 2021-06-01->2025-06-30 | 4.08 | 12.182% | 12.186% | 0.003 | PASS |
| META | 2021-06-01->2025-06-30 | 4.08 | 22.079% | 22.057% | 0.023 | PASS |
| MLM | 2021-06-01->2025-06-30 | 4.08 | 11.339% | 11.309% | 0.030 | PASS |
| MRK | 2021-06-01->2025-06-30 | 4.08 | 4.555% | 5.803% | 1.249 | FAIL |
| MRVL | 2021-06-01->2025-06-30 | 4.08 | 13.017% | 13.031% | 0.014 | PASS |
| MSFT | 2021-06-01->2025-06-30 | 4.08 | 19.664% | 19.642% | 0.022 | PASS |
| MU | 2021-06-01->2025-06-30 | 4.08 | 10.421% | 10.417% | 0.004 | PASS |
| NFLX | 2021-06-01->2025-06-30 | 4.08 | 27.392% | 27.373% | 0.019 | PASS |
| NOW | 2021-06-01->2025-06-30 | 4.08 | 21.212% | 21.204% | 0.008 | PASS |
| NVDA | 2021-06-01->2025-06-30 | 4.08 | 74.735% | 74.700% | 0.035 | PASS |
| ORCL | 2021-06-01->2025-06-30 | 4.08 | 29.936% | 29.939% | 0.003 | PASS |
| PANW | 2021-06-01->2025-06-30 | 4.08 | 35.049% | 35.056% | 0.007 | PASS |
| PLTR | 2021-06-01->2025-06-30 | 4.08 | 54.572% | 54.586% | 0.014 | PASS |
| PWR | 2021-06-01->2025-06-30 | 4.08 | 40.040% | 40.032% | 0.008 | PASS |
| QQQ | 2021-06-01->2025-06-30 | 4.08 | 13.918% | 13.919% | 0.000 | PASS |
| RKLB | 2021-06-01->2025-06-30 | 4.08 | 36.526% | 36.540% | 0.014 | PASS |
| RTX | 2021-06-01->2025-06-30 | 4.08 | 15.549% | 15.546% | 0.003 | PASS |
| SHOP | 2021-06-01->2025-06-30 | 4.08 | -1.993% | -1.980% | 0.013 | PASS |
| SPY | 2021-06-01->2025-06-30 | 4.08 | 11.579% | 11.570% | 0.009 | PASS |
| SYK | 2021-06-01->2025-06-30 | 4.08 | 12.473% | 12.496% | 0.023 | PASS |
| TMO | 2021-06-01->2025-06-30 | 4.08 | -2.115% | -2.102% | 0.014 | PASS |
| TSLA | 2021-06-01->2025-06-30 | 4.08 | 10.960% | 10.942% | 0.017 | PASS |
| TSM | 2021-06-01->2025-06-30 | 4.08 | 18.903% | 19.360% | 0.457 | FAIL |
| UBER | 2021-06-01->2025-06-30 | 4.08 | 15.974% | 15.969% | 0.005 | PASS |
| UNH | 2021-06-01->2025-06-30 | 4.08 | -4.787% | -4.791% | 0.004 | PASS |
| V | 2021-06-01->2025-06-30 | 4.08 | 12.453% | 12.444% | 0.008 | PASS |
| VRT | 2021-06-01->2025-06-30 | 4.08 | 49.583% | 49.602% | 0.019 | PASS |
| WDC | 2021-06-01->2025-06-30 | 4.08 | -3.937% | 2.877% | 6.813 | FAIL |
| WMT | 2021-06-01->2025-06-30 | 4.08 | 21.164% | 21.172% | 0.008 | PASS |
| XOM | 2021-06-01->2025-06-30 | 4.08 | 19.625% | 19.618% | 0.006 | PASS |
| SPY | 1999-01-04->2020-12-31 | 21.99y | 7.137% | 7.135% | 0.003 | PASS |
| QQQ | 1999-03-10->2020-12-31 | 21.81y | 9.374% | 9.373% | 0.001 | PASS |

**Interpretation.** The dividend ledger itself reconciles cleanly — wherever the price legs are consistent,
diffs collapse to ≤0.06pp/yr. The failures isolate two pre-existing structural properties (spinoff value
outside the pre-registered primary path; IEX endpoint noise) and one accounting-convention divergence
(withholding). Per protocol §14 T-D3, **failure blocks G1** absent the principal's explicit acceptance of
degraded-mode disclosures — escalated as **B1** with decision items **D-1/D-2/D-3** (§10).

T-D1–T-D5 are engine tests: **not claimed complete** — G1 establishes the data adequacy they require; G2
implements and tests the governed engine boundaries.

## 7. Rates and borrowing-cost evidence (charter §7 bullet 3)

- **Risk-free:** `^IRX` 13-week T-bill discount yield, 6,655 rows 1999-01-04 → 2025-06-30, 0 out-of-range
  values. This is a **fallback source** (all primary Treasury/FRED/H.15/NY-Fed hosts are network-policy
  blocked) used under protocol §10's disclosed-fallback-band provision; Sharpe/Sortino use only.
- **Fed Funds effective: NOT ACQUIRED — BLOCKER B2.** Exact evidence: CONNECT-tunnel 403 (proxy policy
  denial) on `fred.stlouisfed.org`, `api.stlouisfed.org`, `www.federalreserve.gov` (H.15 datadownload),
  `markets.newyorkfed.org` (EFFR API), `api.fiscaldata.treasury.gov`, `home.treasury.gov`. Remediation
  options: (i) allowlist one primary host in the environment network policy (the repository has precedent:
  the Yahoo-host allowlist fix of 2026-07-15); (ii) principal-accepted alternative construction from the
  FOMC target-range decision record (see D-4); (iii) principal-accepted degraded mode.
- **Margin-rate observations:** recorded source-pinned in `data/rates/robinhood_margin_rate_evidence.yaml`
  (2020-12 primary announcement; 2022-11 rate change with the explicit target-upper+spread mechanism;
  Phase 7A Dec-2025 tier evidence; current Jul-2026 published schedule). Internal consistency: the Gold
  lowest-tier spread is ~+2.5pp over the Fed target upper bound in every dated observation — supporting,
  not yet calibrating, the pre-registered construction.
- **Cost separation recorded** (assumptions A-05, A-07, A-08, A-09): margin interest (Estimated,
  constructed series pending B2); first-$1,000 Gold free tier (Known per terms; account applicability
  pending B3); Gold subscription $5/mo (Estimated; **billing unverified — B3**); subscribed rate
  (unverified — B3); unsubscribed counterfactual (historical +4pp evidence only; current terms
  unverified — B3); incremental vs fully-allocated bases (pre-registered post-processing, no trials).
- **Account-specific verification:** attempted via the user's Gmail connector — token expired,
  non-interactive session cannot re-authorize. No account billing evidence exists in the repository.
  Per the task rule ("Do not infer account-specific terms from generic marketing pages"), these remain
  **unverified**, and G1 therefore cannot pass (consolidated request in §10).

Every numeric assumption is NUM-0001-classified in `assumptions_ledger.yaml` (A-01…A-16).

## 8. Crypto outcome (charter §7 bullet 4) — **formally recorded**

Protocol-named method executed: Alpaca `get_crypto_bars`, paged, 2021-06-01 → 2025-06-30.

- **BTC/USD: 1491/1491 days** — 0 duplicates, 0 nonpositive, 0 gaps, UTC-midnight buckets verified,
  equity-session mapping (t−1 rule, last crypto close ≤ each equity close, no future-bar leakage) complete.
- **ETH/USD: 1491/1491 days** — identical clean profile.
- **SOL/USD: FAIL — 1073/1491 days.** A **416-day coverage hole 2023-07-06 → 2024-08-26** (the vendor's
  SOL suspension/relisting era) plus a 2-day gap 2023-06-23→26; 289 dev-window equity sessions have no
  qualifying SOL close. Full permitted coverage and pagination-completeness validations fail.
- Independent spot-checks (BTC/ETH sample closes vs public UTC-midnight references) were consistent;
  immaterial given the outcome below.

Per the protocol's two-outcome rule (no third option, no cash-like proxy, no partial-sleeve variant, and
outcome A only if **every** required validation passes):

> **B. CRYPTO TARGET SIZING OUT OF SCOPE** — SOL acquisition/validation failed; the two Study B crypto
> configurations (ledger line B-4L, ≤2 runs) **lapse and their budget lapses with them**; no crypto-sizing
> conclusion may be produced by this program; the exclusion must be restated in the final report.

## 9. Artifacts created (exact file list of this PR)

| File | Role |
|---|---|
| `research/margin_target_study/data_acquisition.py` | Charter-§4-approved module: reproducible acquisition + deterministic validators + T-D3 |
| `research/margin_target_study/data_manifest.yaml` | Charter §7 manifest — 9 datasets, 199 per-file hash entries, sources, coverage, transformations, validation, limitations, licensing, isolation status |
| `research/margin_target_study/assumptions_ledger.yaml` | A-01…A-16, Known/Estimated/Hypothetical + NUM-0001 classes |
| `research/margin_target_study/G1_DATA_VALIDATION_REPORT.md` | this report |
| `research/margin_target_study/data/prices/*.json` (63) | committed primary-path price cache (Alpaca; repository-policy precedent) |
| `research/margin_target_study/data/dividends/dividend_ledger.json`, `splits.json` | committed PIT ledger + split records |
| `research/margin_target_study/data/crypto/{BTCUSD,ETHUSD,SOLUSD}.json` | committed crypto bars (evidence for the recorded outcome) |
| `research/margin_target_study/data/rates/robinhood_margin_rate_evidence.yaml` | committed hand-authored, source-pinned rate evidence |

**Not committed** (Yahoo redistribution caution; reproducible via `data_acquisition.py yahoo`; SHA-256 and
byte counts recorded in the manifest): `data/quarantine_yahoo/tr/*` (63), `data/quarantine_yahoo/track3/*`
(2), `data/quarantine_yahoo/rates/irx_13w_tbill.json`. Not created (later-stage artifacts, not fabricated):
`trial_ledger.jsonl`, `candidate_freeze.yaml`, `intelligence_flag_events.yaml`, any results/**.

## 10. Blockers and decisions required (consolidated — principal input needed)

**B1 — T-D3 tolerance breaches (6 tickers, §6).** Decisions:
- **D-1 (spinoffs):** choose one for DHR/IBM/MRK/WDC — (a) accept as a disclosed structural limitation of
  the pre-registered primary path (arm-relative claims unaffected; absolute levels understated for these 4);
  (b) authorize adding in-kind distribution cash-equivalents to the ledger from corporate-action spin_off
  records (a primary-path accounting extension — needs its own validation round); (c) exclude the 4 tickers
  from dividend-sensitive analyses. G1 recommends none — the choice is an accounting-policy call.
- **D-2 (withholding convention):** ledger currently carries vendor amounts (net for TSM/ASML/BABA-fee,
  0.75x-gross for ETN, gross elsewhere). Options: keep as-acquired (disclosed, most conservative for TSM);
  normalize to gross; or normalize to modeled US-retail net. Affects TSM's T-D3 verdict and the R2 family.
- **D-3 (GEV):** accept 0.665pp/yr as disclosed IEX endpoint noise on a 1.24-year window (no data fix
  exists at the free tier), or exclude GEV from T-D3 scope on window-length grounds.

**B2 — Fed Funds series unacquirable** (§7): allowlist a primary host (preferred; one-line network-policy
change, repository precedent 2026-07-15), or approve an alternative construction (D-4), or accept degraded
mode explicitly.
- **D-4:** the protocol pre-registers Fed Funds *effective* + spread; Robinhood's published mechanism uses
  the *target upper bound* + spread. Once B2 unblocks, choose the construction input (or run both, one as
  sensitivity — no extra simulation trials, §8.7 post-processing).

**B3 — Gold/account-specific terms unverified.** Needed from the principal (or a re-authorized Gmail /
uploaded statement): (1) Gold subscription status; (2) actual billed cost ($5/mo assumed); (3) the margin
rate currently shown in the app; (4) the unsubscribed counterfactual rate/terms if displayed. The Gmail
connector needs re-authorization in claude.ai connector settings if email evidence should be used.

**Recorded outcome (not a blocker): crypto outcome B** (§8) — no principal action required; noted for the
final report.

## 11. G1 verdict

Pass-criteria checklist: pinned hashes exact **✓**; price data **PASS**; dividend ledger **PASS** (with D-2
open); T-D3 **FAIL for 6/63 with full cause attribution** → principal acceptance required; benchmarks **PASS**;
risk-free **fallback acquired, disclosed**; Fed Funds **BLOCKED**; Gold/account terms **UNVERIFIED**;
crypto outcome **B formally recorded ✓**; untouched isolation **proven for G1's scope ✓**; manifests and
assumptions **complete ✓**; prohibited files/activities **none ✓**.

Degraded-mode acceptance is reserved to the principal (charter §7: "Any degraded mode proceeds only on the
principal's explicit, recorded acceptance"). This session does not self-approve it. Therefore:

> ## **G1 DATA GATE BLOCKED**
>
> Bounded, fully-enumerated blockers: **B1** (T-D3 disclosures/decisions D-1–D-3), **B2** (Fed Funds
> acquisition path / D-4), **B3** (account-terms verification). Everything else required of G1 is complete,
> validated, manifest-recorded, and reproducible. On resolution of B1–B3 the gate can be re-verdicted
> without re-doing the acquisition work (data-correction paths are documented per item).

**G2 was not begun**: no engine, overlay, repayment, maintenance, shadow, or loader code exists in this PR;
`margin_simulation.py` and its tests are untouched.

---

*All figures above are data-validation measurements, not simulated trading results. Nothing in this report
is a recommendation, a margin signal, or authority for any production change.*
