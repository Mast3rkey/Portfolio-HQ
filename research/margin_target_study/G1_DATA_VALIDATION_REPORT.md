# G1_DATA_VALIDATION_REPORT.md — MARGIN-0005 gate G1 (v2, blocker remediation)

**Program:** margin_deployment_and_target_sizing_v1
**Authority:** `governance/decisions/MARGIN-0005-margin-target-research-charter.md` §1.2, §7
**Protocol:** `research/margin_target_study/PROTOCOL_V2.md` §4, §11, §14, §18
**Executed:** initial G1 2026-07-24 (commit `6efd716`); remediation same day (this revision)
**Base:** `origin/main` = `f984665936203c0505e8603de7c870beb64f7f21`

**No `simulate()` call was made in either round, zero of the 300 registered trials were consumed, no
candidate, ranking, margin signal, target recommendation, trade, or order was produced.** `trial_ledger.jsonl`,
`candidate_freeze.yaml`, `intelligence_flag_events.yaml`, and results artifacts do not exist. G2 was not begun.
Pinned hashes recomputed from `origin/main` blobs at remediation preflight — both **exact**.

---

## 1. Remediation preflight

PR #138: open, draft, head `6efd716` (unmoved since the initial round), base `f984665`, 74 files, no
comments/reviews/threads, no CI checks configured, `mergeable_state: clean`. No other open PRs — no
overlapping work. Working tree clean before remediation. The initial commit was **not amended or
force-pushed**; remediation is one additional narrow commit so the audit trail (v1 → v2) stays visible.

## 2. Untouched-test compliance audit (pre-work, as directed)

### 2.1 Authoritative wording

- Charter §7 (G1 gate): *"Split-adjusted price cache verified (continuity checks), **refreshed through the
  run date**."*
- Charter §6: *"Development, validation, parameter-stability, bootstrap-selection, and G3 reporting code
  **cannot read, simulate, store, display, or summarize untouched-period data** (loader truncation,
  test-enforced)."*
- Protocol §11.1: *"The research data loader serves development mode by default and **physically truncates
  all series at the development boundary**; untouched-mode loading requires an explicit flag that is legal
  only inside the G4 runner, enforced by test (§14 T-U1)."*
- `pre_registration.yaml` `untouched_test_isolation`: `loader: development_mode_truncates_at_boundary`;
  `development_code_may_not: [read, simulate, store, display, summarize]`.

Determination: **acquisition** of post-development-boundary raw prices is permitted — charter §7 expressly
directs the run-date refresh at G1, and the loader-truncation design presupposes that stored series extend
past the boundary (the pre-existing `data/backtest` cache on `main` already does). **Storage in a
sealed/quarantined cache** is therefore permitted and is the intended shape. **Structural-integrity
inspection** at acquisition time is within §7's own "verified (continuity checks)" direction. What the
accepted rules bar is *development* code reading/summarizing untouched-period data — the consumption side.

### 2.2 Exact read audit of the initial G1 round (commit `6efd716`)

| Action | Code path | Post-2025-06-30 (T2) | Post-2020-12-31 (T3) |
|---|---|---|---|
| Acquisition (fetch+store) | `acquire_prices` (v1) | yes — charter-directed refresh | **never acquired** |
| Hash / byte integrity | manifest generation | bytes only | n/a |
| Date/coverage inspection | v1 `validate()` duplicate-date, stale-end checks | yes (dates only) | none |
| Price-value inspection | v1 `validate()` nonpositive check | yes — values compared to 0 in memory; boolean counts output only | none |
| Return calculation | v1 discontinuity scan, cross-check, `reconcile()` | **no — hard-filtered ≤ 2025-06-30** | **no** |
| Reporting/display/summary | report, manifest, PR | coverage endpoint dates only; **no untouched value or return anywhere** | none |

Track 3: untouched-period data (2021-01-01 →) was never acquired, read, or stored in any form.

**Verdict: NO BREACH.** No development/validation/reporting code computed, displayed, stored (outside the
acquisition cache), or summarized any untouched-period value or return. The single gray-zone action — the
v1 structural nonpositive check touching post-boundary price values in memory — was acquisition-verification
under charter §7's own wording, produced only boolean counts, and is preserved un-rewritten in git history
(commit `6efd716`).

### 2.3 Mechanical quarantine (implemented this round)

Ambiguity removed structurally: `acquire_prices` v2 splits at the boundary — development-visible files
(`data/prices/*.json`) now contain **no bar after 2025-06-30** (validator-asserted per file), and the
post-boundary segment (2025-07-01 → 2026-07-23, 63 members, 16,821 rows) lives only in
`data/untouched_sealed/untouched_prices.tar.gz` (deterministic archive, SHA-256
`c18fdd9f1db896ea5c91ea674f12de7728c4812f9d47f1700c72f795b14de618` recorded in `SEALED_INDEX.json`). Seal-time integrity (duplicates 0, nonpositive 0
per member) was computed once during acquisition; only counts persist outside the archive. After sealing,
**no G1 code opens the archive** — `validate()` verifies it byte-level (hash) only; proof:
`grep -n "tarfile\|SEALED_ARCHIVE" research/margin_target_study/data_acquisition.py` shows archive opening
only inside `acquire_prices` (seal creation). Unsealing is a G4-runner act after the candidate freeze.
G2 strategy loaders were **not** implemented; loader-level T-U1 enforcement remains G2 work.

## 3. D-1 — Corporate-action resolution (spin-offs)

New PIT dataset `data/corporate_actions/spinoffs.json`. Vendor `spin_off` records exist for DHR→VLTO and
WDC→SNDK; the 2021 events predate the vendor feed's coverage and are hand-authored from issuer documents
(per-event `source_classification` distinguishes them). GEV was investigated as directed: it is itself the
distributed child of GE's 2024-04-02 spin-off (GE not in roster) — no parent-side event exists for roster
holders; GEV's divergence was a price-feed issue (D-3), not a corporate action.

| Parent → Child | Announced | Record | Ex/parent session | Ratio | Child close (SIP, ex session) | Source |
|---|---|---|---|---|---|---|
| MRK → OGN | 2020-02-05 | 2021-05-17 | 2021-06-03 | 0.1 | $37.00 | Merck 2021-05-07 release (hand-recorded) |
| IBM → KD | 2020-10-08 | 2021-10-25 | 2021-11-04 | 0.2 | $26.38 | IBM 8-K ex-99.1 / Kyndryl IR (hand-recorded) |
| DHR → VLTO | 2022-09-14 | — (vendor) | 2023-10-02 | 1/3 | $85.12 | Alpaca CA spin_off record |
| WDC → SNDK | 2023-10-30 | 2025-02-12 | 2025-02-24 | 1/3 | $48.60 | Alpaca CA spin_off record |

All four carry cash-in-lieu treatment for fractions, acquisition timestamps, and per-event classification.
The primary accounting path is now: **split-adjusted non-TR prices + explicit gross cash dividends +
explicit PIT non-cash corporate actions** (valuation rule A-17: ratio × child consolidated close on the
parent's ex session, credited as reinvestable cash). No holding was excluded; no approximate cash
substitution beyond the stated, validated valuation rule; total-return prices remain barred from the
primary path.

## 4. D-2 — Dividend convention (gross declared primary)

`dividend_ledger.json` rebuilt as **schema v2_gross_declared**: primary amount = gross declared pre-tax
cash per share (split-adjusted); the vendor's net-convention amounts are retained per row (`vendor_net`),
never silently netted. Gross determination runs at (symbol, ex-date) **aggregate** level — necessary
because issuers declare regular + special dividends on one ex-date as separate vendor rows while the gross
reference reports one combined event (BABA 2024-06-13: vendor 0.98 + 0.66 vs combined gross 1.66; per-row
matching would double-count — caught by T-D3 during remediation, fixed, documented in the module).

Results: 822 events — 596 corroborated (vendor = gross), 46 gross-from-Yahoo across TSM/ASML/ETN/BABA
(net-convention vendor rows), 63 vendor-declared on the spinoff-scaled tickers (Yahoo unusable as gross
reference there), 116 pre-cross-source-window rows (all before 2021-05-01, outside the simulation window),
1 uncorroborated flagged row (ASML 2024-12-02, retained + flagged, ~0.02pp/yr). Integrity: 0 duplicates,
0 nonpositive gross, 0 payable<ex, 0 net>gross, 0 future leakage, payable dates 822/822.

ADR/withholding documentation (separate, source-backed): `data/dividends/withholding_register.yaml` —
TSM (1 ADR = 5 ordinary; TW 21%; measured vendor ratio ~0.78), ASML (1:1; NL 15%; measured 0.850 exactly),
ETN (US-listed Irish plc; vendor models full 25% DWT; US holders typically exempt — account treatment
UNRESOLVED pending B3), BABA (1 ADS = 8 ordinary; ~$0.02/ADS depositary fee). These are sensitivities;
the primary ledger stays gross. T-D3 now compares gross-convention primary vs gross-convention TR — both
sides shown in §6.

## 5. D-3 — GEV resolution (outcome A)

Root cause established with dated, same-vendor comparisons — not waived as "noise": Alpaca SIP
(consolidated) vs Alpaca IEX daily closes for GEV over its full 312-session dev window: 7 sessions differ
by >0.15%, worst **2024-12-23: 344.92 vs 339.34 (1.618%)**, also 2024-09-17 (0.573%) and the listing
session 2024-04-02 (140.00 vs 139.60, 0.286%); mean |diff| 0.05%. No corporate action is involved (§3).
The IEX prints on those dated sessions deviate from the consolidated tape; over GEV's short 1.24-year
window this breached the T-D3 tolerance.

**Resolution (outcome A):** documented ticker-specific source exception — GEV's primary series uses Alpaca
**SIP** (same vendor, same API, same split-adjustment mode), constant `GEV_FEED_EXCEPTION` in
`data_acquisition.py`, provenance in the manifest, dated evidence above. GEV T-D3: **0.003pp/yr PASS**.
GEV was not excluded; the tolerance was not widened; the series is the vendor's consolidated tape, not an
unexplained adjustment. (Roster-wide SIP migration is noted as a possible future improvement requiring its
own decision — not adopted here.)

## 6. T-D3 reconciliation v2 — **PASS, all 63 tickers + both Track 3 books**

Primary path (split-adjusted prices + gross PIT dividends + spin-off cash-equivalents) vs quarantined
Yahoo TR, dev window, tolerance ±0.3pp/yr:

- Former failures, now: WDC **0.157**, DHR **0.105**, IBM **0.050**, MRK **0.011**, TSM **0.016**,
  GEV **0.003**, plus BABA **0.020** and ETN **0.004** after the aggregate-level gross rule.
- Track 3 same-source construction check: SPY **0.003**, QQQ **0.001**.
- Worst diff across the entire roster: WDC 0.157pp/yr; median ≈ 0.02pp/yr.

Full table:

| ticker | window | yrs | primary CAGR | TR CAGR | diff pp/yr | verdict |
| AAPL | 2021-06-01->2025-06-30 | 4.08 | 13.691% | 13.676% | 0.015 | PASS |
| ABBV | 2021-06-01->2025-06-30 | 4.08 | 17.551% | 17.526% | 0.025 | PASS |
| AMAT | 2021-06-01->2025-06-30 | 4.08 | 8.060% | 8.052% | 0.008 | PASS |
| AMD | 2021-06-01->2025-06-30 | 4.08 | 14.804% | 14.799% | 0.005 | PASS |
| AMZN | 2021-06-01->2025-06-30 | 4.08 | 7.883% | 7.892% | 0.008 | PASS |
| ASML | 2021-06-01->2025-06-30 | 4.08 | 5.449% | 5.394% | 0.055 | PASS |
| AVGO | 2021-06-01->2025-06-30 | 4.08 | 58.050% | 58.037% | 0.013 | PASS |
| BABA | 2021-06-01->2025-06-30 | 4.08 | -13.840% | -13.860% | 0.020 | PASS |
| BRK.B | 2021-06-01->2025-06-30 | 4.08 | 13.462% | 13.495% | 0.033 | PASS |
| CAT | 2021-06-01->2025-06-30 | 4.08 | 14.387% | 14.383% | 0.004 | PASS |
| CEG | 2022-02-02->2025-06-30 | 3.41 | 71.602% | 71.529% | 0.073 | PASS |
| COST | 2021-06-01->2025-06-30 | 4.08 | 28.096% | 28.110% | 0.015 | PASS |
| CRM | 2021-06-01->2025-06-30 | 4.08 | 3.810% | 3.806% | 0.004 | PASS |
| CRWD | 2021-06-01->2025-06-30 | 4.08 | 22.549% | 22.566% | 0.016 | PASS |
| CVX | 2021-06-01->2025-06-30 | 4.08 | 11.895% | 11.902% | 0.007 | PASS |
| DELL | 2021-06-01->2025-06-30 | 4.08 | 25.731% | 25.745% | 0.014 | PASS |
| DHR | 2021-06-01->2025-06-30 | 4.08 | -1.786% | -1.891% | 0.105 | PASS |
| EQIX | 2021-06-01->2025-06-30 | 4.08 | 3.728% | 3.717% | 0.010 | PASS |
| ETN | 2021-06-01->2025-06-30 | 4.08 | 26.536% | 26.540% | 0.004 | PASS |
| GEV | 2024-04-02->2025-06-30 | 1.24 | 191.805% | 191.808% | 0.003 | PASS |
| GILD | 2021-06-01->2025-06-30 | 4.08 | 18.587% | 18.609% | 0.023 | PASS |
| GLD | 2021-06-01->2025-06-30 | 4.08 | 14.115% | 14.112% | 0.003 | PASS |
| GNRC | 2021-06-01->2025-06-30 | 4.08 | -17.996% | -17.998% | 0.002 | PASS |
| GOOGL | 2021-06-01->2025-06-30 | 4.08 | 10.254% | 10.252% | 0.002 | PASS |
| HOOD | 2021-07-29->2025-06-30 | 3.92 | 28.784% | 28.698% | 0.086 | PASS |
| IBM | 2021-06-01->2025-06-30 | 4.08 | 25.569% | 25.619% | 0.050 | PASS |
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
| MRK | 2021-06-01->2025-06-30 | 4.08 | 5.814% | 5.803% | 0.011 | PASS |
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
| TSM | 2021-06-01->2025-06-30 | 4.08 | 19.376% | 19.360% | 0.016 | PASS |
| UBER | 2021-06-01->2025-06-30 | 4.08 | 15.974% | 15.969% | 0.005 | PASS |
| UNH | 2021-06-01->2025-06-30 | 4.08 | -4.787% | -4.791% | 0.004 | PASS |
| V | 2021-06-01->2025-06-30 | 4.08 | 12.453% | 12.444% | 0.008 | PASS |
| VRT | 2021-06-01->2025-06-30 | 4.08 | 49.583% | 49.602% | 0.019 | PASS |
| WDC | 2021-06-01->2025-06-30 | 4.08 | 3.033% | 2.877% | 0.157 | PASS |
| WMT | 2021-06-01->2025-06-30 | 4.08 | 21.164% | 21.172% | 0.008 | PASS |
| XOM | 2021-06-01->2025-06-30 | 4.08 | 19.625% | 19.618% | 0.006 | PASS |
| SPY | 1999-01-04->2020-12-31 | 21.99y | 7.137% | 7.135% | 0.003 | PASS |
| QQQ | 1999-03-10->2020-12-31 | 21.81y | 9.374% | 9.373% | 0.001 | PASS |

T-D1–T-D5 engine proofs remain G2 work and are not claimed.

## 7. D-4 — Federal Funds (DFF) acquisition and reconstruction

The pinned construction is unchanged: **DFF + pre-registered calibrated spread** (per
`pre_registration.yaml` `costs.interest`); the target-range upper bound does **not** replace DFF. Direct
acquisition remains blocked — re-verified this round: CONNECT-tunnel 403 on `fred.stlouisfed.org` (and all
alternate primary hosts in the v1 evidence). The principal has verified DFF exists through 2026-07-22.

Manual-supply path implemented and documented (`data_acquisition.py dff <csv>` + `DFF_EXPECTED_SCHEMA`):
expected file = FRED fredgraph CSV for DFF (`header DATE,DFF` or `observation_date,DFF`; rows
`YYYY-MM-DD,<percent>`; missing "."), coverage 1999-01-01 → ≥2025-06-30. The ingestion validator checks
header, duplicates, coverage span, value range [0,25], gaps >4 days; on pass it stores dev-bounded
`data/rates/dff.json` (FRED data is US-government public domain — committable), records the supplied file's
SHA-256, and emits the reconstruction comparison: implied spread (observed Robinhood Gold lowest-tier rate
− DFF) on each recorded observation date vs the issuer's published target-upper + 2.5pp mechanism (recorded
as cross-check and limitation). **If the DFF-based and target-upper-based constructions diverge materially
enough to alter costs or a future candidate classification, a MARGIN-0005 charter amendment is required
before simulations** — no model choice is made silently.

## 8. Crypto outcome — principal acceptance recorded

> **CRYPTO TARGET SIZING OUT OF SCOPE** (outcome b) — **accepted by the principal 2026-07-24.**

Confirmed consequences: the two Study B crypto configurations (ledger line B-4L) **lapse**; their trial
capacity **cannot be reallocated**; BTC/ETH data (1491/1491 days each, fully validated) remain documented
but **cannot support any crypto target-sizing conclusion under this charter**; **no cash-like proxy** is
introduced. Basis: SOL/USD 416-day coverage hole (2023-07-06 → 2024-08-26) in the protocol-named source.
This acceptance is **not** degraded-mode approval for any other dataset.

## 9. Gold account evidence — placeholders (nothing verified, nothing invented)

Public Robinhood terms are recorded as **generic provider evidence only** (`robinhood_margin_rate_evidence.yaml`).
Account-specific fields, all **[PENDING PRINCIPAL EVIDENCE]** (assumption A-21):

| Field | Status |
|---|---|
| Active Gold subscription status | [PENDING] |
| Monthly vs annual plan | [PENDING] |
| Actual billed cost | [PENDING] |
| App-displayed margin rate | [PENDING] |
| First-$1,000 treatment on this account | [PENDING] |
| Non-Gold / downgrade terms | [PENDING] |

Intake procedure on supply: inspect the artifact; record evidence date, account-specific value, source
artifact, locator, hash where applicable, and a privacy-preserving description. **No unredacted personal
screenshot will be committed without explicit principal authorization** — a redacted extract or recorded
facts with provenance is preferred.

## 10. Validation results (remediation round)

- YAML parse: all new/updated YAML + config YAML clean.
- Deterministic validators (`data_acquisition.py validate`): every section passes — prices (0 dup/nonpos/
  beyond-boundary; missing sim-window sessions ≤3; RKLB's 13 gaps are pre-2021-06-01 warm-up only), sealed
  archive hash match with zero seal-time anomalies, dividend ledger v2 clean, corporate-action ledger clean,
  crypto assertions, Track 3 boundaries, ^IRX — **except the single open DFF item**, which the validator
  correctly reports as a blocker (overall FAIL by design until DFF is ingested).
- T-D3 v2: **PASS 63/63 + 2/2** (§6).
- Manifest hashes: regenerated (11 datasets, 202 per-file entries) and spot-verified.
- Untouched-boundary checks: all OK (§2.3); Track 3 untouched never acquired.
- `python -m pytest -q`: full suite green (see PR).
- `git diff --check`: clean; protected paths untouched (every changed file inside
  `research/margin_target_study/`); `simulate()` never called; zero trials consumed; pinned hashes exact.

## 11. Remaining blockers and verdict

Resolved this round: **B1** (T-D3 — D-1/D-2/D-3 implemented, full pass), crypto outcome acceptance
recorded. Remaining:

- **B2′ (DFF):** awaiting the principal-supplied FRED DFF CSV (or a network-policy allowlist addition);
  ingestion + validation + reconstruction comparison are implemented and one command away.
- **B3 (Gold/account evidence):** the six [PENDING] fields in §9.

Because charter §7 requires the borrowing-rate series acquired and costs verified against the account's
actual terms, and no degraded mode is self-approvable:

> ## **G1 DATA GATE BLOCKED**
>
> Narrowed to exactly two bounded items: **B2′** (supply DFF CSV → `python3
> research/margin_target_study/data_acquisition.py dff <file>`) and **B3** (six account-evidence fields).
> All other G1 requirements pass. On resolution, the gate can be re-verdicted without re-doing any
> acquisition or reconciliation work.

**G2 was not begun.**

---

*All figures above are data-validation measurements, not simulated trading results. Nothing in this report
is a recommendation, a margin signal, or authority for any production change.*
