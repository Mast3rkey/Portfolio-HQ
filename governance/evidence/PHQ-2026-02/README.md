# PHQ-2026-02 evidence

## v1.35 post-execution holdings-reconciliation package

- Retained verbatim under `v1_35/` (original filenames preserved except the
  upstream `README.md`, renamed `UPSTREAM_README.md` to avoid colliding with
  this directory's own README). **The source zip itself is not retained in
  Git** — only its extracted contents (the six files under `v1_35/`) are.
- Source archive: `Portfolio_HQ_Post_Execution_Reconciliation_v1_35.zip`.
- Top-level archive SHA-256 (verified against the principal-supplied expected
  value before any file inside it was read):
  `fb8eb811df29eb560bfaed16e8d0e89c6cbcf44bc42e1f1ae2ccfca4cddd889e`. **This
  is transfer/source provenance, not independently reconstructable from the
  retained extracted files** — a zip's own digest is a property of its exact
  byte stream (compression, ordering, metadata), which six standalone files on
  disk cannot reproduce. Treat it as asserted provenance, matching the value
  the principal supplied, the same way `governance/evidence/PHQ-2026-01/README.md`
  treats its own two un-retained upstream source archives.
- **Independently, and separately verified**: every one of the six retained
  extracted files' own SHA-256 and byte count were re-derived from the actual
  bytes on disk and matched exactly against the archive's own internal
  `MANIFEST.json` (which itself was extracted and is retained) — this is the
  cryptographic proof chain that actually holds here, distinct from the
  top-level zip digest above.
- Evidence received at 2026-07-31 09:40 ET per the package's own
  `evidence_received_at` field; two screenshots captured seconds apart during
  live markets — quantities are the controlling reconciliation evidence,
  market values are reasonableness checks only (see `UPSTREAM_README.md`).

## Controlling determination: complete post-transition equity/crypto list

The v1.35 package captures 24 total equity/fund positions (SPCX included
within that 24, not additional to it) + 7 crypto entries (31 total) — far
fewer than the 65 equity/fund tickers `holdings.yaml` tracked before this
reconciliation. The package's own README states the later
screenshot supplies "the complete equity list," and the two account-summary
cross-checks corroborate this internally without any external assumption:
sum of the 24 listed equity rows ($3,325.88) matches the screenshot's own
displayed equities total ($3,325.86) to two cents; sum of the 7 crypto rows
($317.79) matches the displayed crypto total ($317.90) closely; margin used
is $0.00 against a previously-synced $1,590.40 debt, consistent with sale
proceeds repaying inherited debit first per `PHQ-2026-01` point 7.

**This determination — that the 41 previously-tracked tickers absent from
v1.35 were fully exited by the manual transition trades, not omitted from a
partial screenshot — was confirmed directly by the principal** before
`holdings.yaml` was reconciled, rather than inferred silently from the
internal arithmetic alone.

## Reconciliation check

`reconciliation_check.json` — machine-readable, generated from this
directory's own retained evidence JSON and the reconciled `holdings.yaml`:
every non-dust captured quantity (24 total equity/fund, SPCX included, plus
BTC/ETH/SOL — 27 rows) maps exactly to the corresponding `holdings.yaml` entry
(`all_captured_quantities_match: true`). BONK/PEPE/WIF/ZORA are excluded per
this repository's existing permanent dust-ignore convention (`$0.00` mark,
CLAUDE.md, established 2026-07-12) — not a new decision made here.

## Ticker-symbol normalization

None required. Every non-dust symbol in the v1.35 evidence matches an
existing repository ticker convention exactly (no `.`/`-` variant, no
renamed issuer).

## Fields not populated

No tax-lot, cost-basis, or acquisition-date field was populated anywhere in
this reconciliation — none was supplied by the evidence and none was
inferred.

## Margin buffer note

`holdings.yaml`'s `margin.buffer_pct: 100.0` reflects zero margin drawn per
this evidence (`margin_used: $0.00`), not a Robinhood-displayed buffer
screen — the v1.35 package did not capture a displayed buffer percentage.
Re-sync a real displayed buffer % before any future margin-funded decision.
