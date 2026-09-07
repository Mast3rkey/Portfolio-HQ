# Retained Evidence — PHQ-2026-01

Evidence supporting `governance/decisions/PHQ-2026-01-canonical-architecture-and-transition-policy-approval.md`,
retained verbatim from the source materials the principal supplied for that
decision. Established following the `governance/audits/` convention (one
retained-evidence area per governing decision, files copied in as-is, never
edited after retention) — this is an evidence-retention area, not a second
audit-artifact convention.

## Status labels (apply to every file in this directory)

- **Approved-policy evidence, not current live state.** These files document
  the architecture research and unlevered-validation work behind PHQ-2026-01's
  approved policy. None of them reflects current `holdings.yaml`, current
  Robinhood account state, or current market prices.
- **Not trade or order authority.** Nothing here authorizes, recommends
  quantities for, or executes any purchase or sale.
- **Historical snapshot where dated.** The `frozen_state` block inside
  `unlevered_validation/master_research_report.json` (account equity $6,162.95,
  margin used $963.16, snapshot "2026-07-30 15:32 ET") is historical evidence
  only — `holdings.yaml` was last synced 2026-07-22 and neither figure updates
  the other. See `authority/LIVE_STATE_BOUNDARY.md`.
- **SPCX:** `final_due_diligence/Portfolio_HQ_Gated_Name_Disposition_v1_32.csv`
  disposes SPCX as `HOLD TARGET IN CASH` (gated — no investable vehicle), not
  sell-all. No file in this directory or elsewhere in this repository directs
  selling an existing SPCX position.
- **SKHY:** not referenced by any file in this directory. PHQ-2026-01 does not
  govern SKHY; it remains unresolved per `CLAUDE.md`'s Open Items.

## Provenance chain

Supplied to this repository as `Portfolio_HQ_PHQ_2026_01_Repository_Sync_Package_v1_0.zip`
(SHA-256 `9595bf1af0013770e89fc691bf226d42520b6e134cee7d90a144b1f330216e55`,
verified against the transfer package as received). That package's own internal
manifest (`manifests/PACKAGE_MANIFEST.json` / `manifests/SHA256SUMS_PACKAGE.txt`)
was verified file-by-file (`sha256sum -c`, 21/21 OK) before any file below was
copied into the repository — the hashes recorded per file below are unchanged
from that verification.

The transfer package's own manifest records two upstream source archives:

| Source archive | Recorded SHA-256 |
|---|---|
| `Portfolio_HQ_v1_32_Final_Due_Diligence_Bundle.zip` | `8308a0dc1522ecc413f58c63a2ad4b21460e4b0cde1047b8431be51566e45092` |
| `Portfolio_HQ_Unlevered_Batch_v1_31_4a_20260730_175519.zip` | `c0a4a6b33b4ff9362d0159ea069e5e3eb397bc1c867174ea33f6d51c450b962a` |

**Neither source archive was included in the transfer package** (`manifests/SOURCE_BUNDLE_HASHES.txt`
states this explicitly — only files already extracted from them were transferred).
These two hashes are therefore *recorded*, matching the values independently
supplied for this task, but were **not independently re-derived against the
original archive bytes** in this repository — no session with access to this
repository has ever held either archive. Treat them as asserted provenance, not
as a cryptographic proof chain back to original generation.

## Bounded correction (2026-07-31): CSV line-ending normalization

The transfer package's original CSV files used CRLF line endings, which fail
this repository's `git diff --check` / CI whitespace check. Four retained CSV
files were normalized from CRLF to LF in a bounded, content-preserving
correction — **line endings only; every field, row, column, delimiter,
quotation mark, and value is byte-for-byte identical** to the originally
transferred content with carriage returns stripped (verified: normalized
content = original content piped through carriage-return removal, diffed
byte-for-byte, zero difference, for all four files).

**Distinguish the two hash sets below.** The "originally supplied (CRLF)"
hash is the file exactly as the transfer package delivered it — this matches
what `final_due_diligence/Portfolio_HQ_Final_Due_Diligence_Manifest_v1_32.json`
itself records internally for the three files it covers, since that manifest
is retained verbatim as originally supplied and was **not** edited by this
correction. The "repository-retained (LF)" hash is what is actually committed
in this directory today, and is what the per-file tables below now show.

| File | Originally supplied (CRLF) SHA-256 / bytes | Repository-retained (LF) SHA-256 / bytes |
|---|---|---|
| `final_due_diligence/Portfolio_HQ_Final_Decision_Register_v1_32.csv` | `5797fda14b2cfceeb10a721957caee96a5b85050f9755e9433997c81e762d013` / 1654 | `1e9b0db7e2f76bef6b4cced43163ba582d9e54d71a36b8ae8d9c4d0e589c2569` / 1646 |
| `final_due_diligence/Portfolio_HQ_Gated_Name_Disposition_v1_32.csv` | `03990e4d6d904a37c28b20617f46b1299616421c87e59adec747c9f15698a41d` / 2688 | `e531ba8f0ed53230d1bc28953fa814620a30ded48cf38138ad97c8840f9291a2` / 2680 |
| `final_due_diligence/Portfolio_HQ_Look_Through_Exposure_v1_32.csv` | `7aa617cdd6628cab667909945760a9bd96d5341e0ddf3fa4a59e608701829bb3` / 651 | `403f022a4c037de26916e210ceedd40e93103826ef71f456db1a94ae010b7e3d` / 639 |
| `unlevered_validation/unlevered_matrix_results.csv` | `85a3b9aeeff497c2cae6f89b42caff2c84c8ad21965d0a8da7446e7602159d8e` / 2580 | `1eee0c99dfca8d1bc9fffbb71a5193dcf657f1775f8603768dead1775fb5aa4d` / 2571 |

**Scope note:** the independent reviewer's finding named the three
`final_due_diligence/` CSVs. This repository's own `git diff --check` run
against the PR's merge-base additionally found the same CRLF condition in
`unlevered_validation/unlevered_matrix_results.csv` — left uncorrected, that
file alone would still fail the same CI check this correction exists to fix.
It was normalized identically (same mechanism, same verification) and is
included in this table and the per-file listing below for exactly that
reason. `manifests/PACKAGE_MANIFEST.json`/`manifests/SHA256SUMS_PACKAGE.txt`
(the transfer package's own manifests, never retained in this repository —
see "Explicitly omitted" below) are the only place that file's original hash
was otherwise recorded; no retained repository file needed correcting for it
beyond this README's own table.

Unaffected by this correction — no other retained file's hash or byte count
changed: `authority/PHQ-2026-01_PRINCIPAL_APPROVAL.txt`,
`authority/LIVE_STATE_BOUNDARY.md`, both HTML files, both JSON files under
`final_due_diligence/`, `final_due_diligence/Portfolio_HQ_Final_Due_Diligence_Manifest_v1_32.json`
(retained verbatim as originally supplied — see above), and every other file
under `unlevered_validation/`.

## Retained files

### `authority/`

| File | SHA-256 | Content |
|---|---|---|
| `PHQ-2026-01_PRINCIPAL_APPROVAL.txt` | `a4947fa7690e923eb5cd72271b8f734ba7239013b35fdca5b0dcf267e66f30d6` | Exact principal approval statement and approved policy scope (12 points) |
| `LIVE_STATE_BOUNDARY.md` | `9d8ab8261cf31b9bc5a0ab11ad3df4aff27b14951f1426f75c9e18567fde816d` | Post-snapshot Robinhood order-entry warning; required repository treatment |

### `final_due_diligence/` — v1.32 final due-diligence bundle

| File | SHA-256 | Content |
|---|---|---|
| `Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.html` | `fbcd6b07b61efd38b89ab81920a8e411f8cb8247f32a3d7262628efdbce9952d` | Human-readable final due-diligence report |
| `Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json` | `2748892c2c1c93397d049fe9888ec39ed149d7debe79136ec91fa194a2bc074d` | Machine-readable version: 7 decisions (DD-001..DD-007), 37 architecture rows, gated dispositions, look-through exposure, sources, residual risks |
| `Portfolio_HQ_Final_Decision_Register_v1_32.csv` | `1e9b0db7e2f76bef6b4cced43163ba582d9e54d71a36b8ae8d9c4d0e589c2569` (LF-normalized; see "Bounded correction" above) | The 7 DD-### decisions in tabular form |
| `Portfolio_HQ_Look_Through_Exposure_v1_32.csv` | `403f022a4c037de26916e210ceedd40e93103826ef71f456db1a94ae010b7e3d` (LF-normalized; see "Bounded correction" above) | Per-issuer effective exposure through SPY/VEA/VWO ETF look-through |
| `Portfolio_HQ_Gated_Name_Disposition_v1_32.csv` | `e531ba8f0ed53230d1bc28953fa814620a30ded48cf38138ad97c8840f9291a2` (LF-normalized; see "Bounded correction" above) | Per-name disposition for the 7 gated tickers (SNPS, ICE, SPGI, WM, RKLB, TSLA, SPCX) |
| `Portfolio_HQ_Final_Due_Diligence_Manifest_v1_32.json` | `71c0f30e174e10cc7828da61c131ffe209b3d65ced0263372daa4452489fff6b` | Bundle's own internal file manifest (byte counts + hashes for the 7 files above plus the two files retained once under `unlevered_validation/` below), retained verbatim as originally supplied and unedited by this repository — **its own recorded hashes/byte counts for the 3 CSVs it covers are the pre-normalization (CRLF) values**, not the LF values those CSVs carry in this repository today; see "Bounded correction" above |

### `unlevered_validation/` — v1.31.4a bounded unlevered backtest validation

| File | SHA-256 | Content |
|---|---|---|
| `Portfolio_HQ_Master_Research_Log_v1_31_4a_20260730_175519.html` | `57fb37da834741172e743d9c5f986314477e5dd249a0d20da89c123517a13757` | Human-readable research log for the 8-case unlevered matrix run. **Also part of the `final_due_diligence` bundle's own manifest** — retained once here rather than duplicated. |
| `master_research_report.json` | `fadc2636e178af3fe49faf5df5af1f8b10e3c796b0706fb3c1ba59b0f3d41d96` | Machine-readable research report: frozen state snapshot, canonical architecture, discovery runs, unlevered matrix, transition map, settled margin finding. **Same file `final_due_diligence`'s own manifest references as `master_report_source_sha256`** — retained once here rather than duplicated. |
| `unlevered_matrix_results.csv` | `1eee0c99dfca8d1bc9fffbb71a5193dcf657f1775f8603768dead1775fb5aa4d` (LF-normalized; see "Bounded correction" above) | 8-case result matrix (canonical/actionable-core × quarterly/monthly/buy-and-hold × cash-yield 0%/3%), common window 2024-08-26 to 2026-07-28 (~23 months), all 8 cases PASS |
| `pytest_full_suite.txt` | `f5aa966e27c44a10c118bcd14a5adb65e0f7f0ad012337204deedcd86b8c416c` | Full test-suite output from the source backtest application (42 passed) — a separate, standalone application (`Portfolio_HQ_v1_10_8_repayment_band_backtest_app`), not this repository's own test suite |
| `source_hashes_before_after.json` | `637d6325fc7352d01ebbb1b0a2afe6ad15650bcaec60c1071d1b6f9b1523f290` | Confirms the source backtest application's own engine files were unchanged before/after the validation run |
| `test_portfolios.json` | `5dd533ad073125f2b3fafa137929cab3a0cb2244525f81ecd69db8f4fc0b394c` | The two portfolios tested: `canonical_proposed` (37 rows, includes gated names at target weight) and `actionable_core` (gated names' target capital held as cash) |
| `api_health.json` | `9217ca8167caa792706f22f40f3187b2cf668b4b4fefab523fd9a0cc88dbff17` | Source application's market-data API health check at run time |
| `SHA256SUMS.txt` | `31fa4c3f6e107c4cdabca70d41b5f8961536cb22b30337c65fe0e5ca7f7d76e7` | Source backtest application's own full internal source-tree hash inventory (180 entries) at run time, for provenance only — not this repository's code |

## Explicitly omitted (not retained)

- The transfer package's own meta-manifests (`README_SYNC_PACKAGE.md`,
  `manifests/PACKAGE_MANIFEST.json`, `manifests/SHA256SUMS_PACKAGE.txt`,
  `manifests/SOURCE_BUNDLE_HASHES.txt`) — these describe the *transfer
  package*, not the underlying evidence; their content is folded into this
  README and the decision record instead of duplicating a second manifest set.
- The transfer ZIP itself.
- The two upstream source archives (`Portfolio_HQ_v1_32_Final_Due_Diligence_Bundle.zip`,
  `Portfolio_HQ_Unlevered_Batch_v1_31_4a_20260730_175519.zip`) — never present
  in this repository's environment; only already-extracted files were
  transferred.
- The frozen v1.31 portfolio snapshot, the provisional transition map, and the
  simplified v1.34/v1.34a allocation outputs — per `authority/LIVE_STATE_BOUNDARY.md`,
  these are stale as live-state evidence (Robinhood orders were entered, some
  filled, some queued, after the frozen snapshot) and were intentionally
  excluded from the transfer package itself; none is retained here.
