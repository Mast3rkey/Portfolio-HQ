# CHART-0002 Batch 1 -- COST daily chart evidence

This is one of 19 bounded evidence packages in CHART-0002 Stage 1 Batch 1
(the first 19-name eligible cohort, daily `1D` timeframe only), authorized by
the controlling principal directive for this implementation session and
governed by `governance/decisions/CHART-0002-bounded-multi-chart-evidence-framework-proposal.md`.

## Why this package exists

CHART-0002 (`status: Accepted`) authorizes preparation of a bounded,
multi-image extension of CHART-0001's closed one-image NVDA pilot. This
package is COST's share of the first 19-ticker batch: `AMZN, ASML, AVGO,
CEG, COST, ETN, GEV, GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, TMO,
TSM, V`, daily timeframe only, Stage 1 only (no Stage 2 cross-timeframe
synthesis).

## Exact scope: one image, one asset, one timeframe

- **Asset:** COST (Costco Wholesale Corporation), equity.
- **Timeframe:** daily (1D).
- **Source:** the sole canonical COST daily screenshot in the read-only,
  externally governed Chart-Automation library
  (`Chart-Automation/library/governed/2026-08-01/COST/COST__2026-08-01__1D.png`,
  project-relative reference only -- no absolute user path is committed here
  or anywhere in this package).
- No second image, no other ticker, no other timeframe is included in this
  package.

## Files in this package

- `COST__2026-08-01__1D.png` -- the retained chart image. **Byte-for-byte
  identical** to the governed source (no redaction applied -- see Privacy
  below). SHA-256 `9c5ccfdc71033e67475d369f5635210a717b85427fd9d3d5f3262743537e0be9`, 1,784,040 bytes, PNG, 3624x2336.
- `record.yaml` -- the structured advisory Chart Evidence Record: identity
  and capture metadata, the privacy disposition, content split cleanly into
  `visible_facts` / `observations` / `inferences` / `uncertainties`,
  thesis-relationship and advisory-boundary fields, provenance, and
  lifecycle.
- `MANIFEST.json` -- hash reconciliation, the full source-provenance chain
  (governed library -> this package), the privacy result and disclosure
  detail, and the verifiability boundary.
- This `README.md`.

No second screenshot, thumbnail, OCR-extracted text file, or derivative
chart is present. No `chart_evidence/` directory, index file, or validator
is created here -- this package reuses the existing
`governance/evidence/<decision-id>/` pattern already established by
`PHQ-2026-01` through `PHQ-2026-06` and `CHART-0001`.

## Source and provenance boundary

The governed Chart-Automation library establishes, independently of this
session, that `COST__2026-08-01__1D.png` is the canonical COST daily
screenshot for the 2026-08-01 governed batch, and its SHA-256 is identical
across the library file itself and `chart_inventory.json`'s matching record.
This session independently recomputed that hash directly against the file on
disk. See `MANIFEST.json`'s `source_provenance_chain` for the full chain and
its disclosed, unavoidable trust boundary (identical in kind to every prior
`PHQ-####` and `CHART-0001` screenshot-evidenced package in this repository).

The Chart-Automation project itself was read-only for this session: nothing
under `~/Projects/Chart-Automation` was modified, renamed, copied within,
reorganized, regenerated, or deleted, and `~/Downloads` was never accessed
directly.

## Privacy result

**Passed, with a formally invoked, per-image username exception -- not
redacted.** The governed source image's top-left capture watermark visibly
shows a TradingView platform username ahead of "created with
TradingView.com, Aug 01, 2026 16:43 UTC-4". CHART-0001 Section 5
permits a narrow, principal-approved, per-image username exception, reused
by reference in CHART-0002 Section 6 (which requires a *fresh* explicit
approval for each new image, since the prior CHART-0001 NVDA grant does not
carry over). The principal formally, explicitly, and individually invoked
that exception for this image (and the other 18 images in this same batch)
in this authorizing implementation session -- the full verbatim text is
recorded in `MANIFEST.json`'s `privacy_result_detail` and
`record.yaml`'s `privacy_and_redaction.username_exception_note`. No other
private, account-level, or brokerage-identifying information (balances,
account numbers, positions, order history, buying-power/margin figures,
email, real name, or watchlist contents) is present anywhere in the image.
`governed_source_sha256 == retained_sha256` confirms no pixel of any kind
was modified.

## Fact vs. interpretation boundary

`record.yaml`'s `content` block keeps four lists strictly separate, per
CHART-0001 Section 3/Section 9:

- `visible_facts` -- only what is literally legible (labels, values, line
  positions, colors, panel structure).
- `observations` -- descriptive statements grounded directly in those
  facts, still non-interpretive.
- `inferences` -- explicitly labeled interpretive judgments, hedged, never
  presented as fact, and never a prediction, score, or recommendation.
- `uncertainties` -- everything not legible, not confirmed, or ambiguous,
  including indicator names/parameters that are not shown anywhere in the
  image and are recorded as unknown rather than guessed.

No indicator setting, date, or price level anywhere in this package was
invented. No live market data or external research was used to fill any gap
in what the image itself shows, per CHART-0001's own prohibition.

## Advisory-only status -- what this package does and does not do

This package is **secondary observational evidence only** -- a single,
dated, point-in-time chart capture. It:

- does **not** change `intelligence/companies/COST.yaml` or any other
  Company/Theme Intelligence record;
- does **not** change COST's tier, target, or canonical destination
  weight in `targets.yaml`;
- does **not** change `holdings.yaml`, any share count, or any margin
  parameter;
- does **not** affect `allocate.py`'s output, any allocator computation, or
  any live-priced holding value;
- does **not** create, feed, or in any way touch `LADDER-0001`'s research
  charter or protocol (which independently excludes chart/screenshot input
  from its own study);
- does **not** create an order, a trade recommendation, a technical score,
  or a ranking of any kind.

`record.yaml`'s `thesis_relationship.governed_consequence` is explicitly
`none`.

## Freshness limitation

This is a **daily-timeframe** capture, which per CHART-0001 Section 7 goes
stale faster than a weekly one. `record.yaml`'s
`lifecycle.review_or_expiration_date` records an analyst-chosen advisory
heuristic (roughly five trading sessions after capture) -- not a governed
cadence, and not equivalent to Company Intelligence's
`review.cadence_days`/`next_due` fields, which this package does not use or
extend. Staleness past that date requires disclosure or analyst abstention
from relying on this record, never an automatic policy change of any kind.

## Review, acceptance, and merge -- not yet complete

This package is part of a **draft** implementation PR. Per CHART-0002 and
`OPS-0007` Section 1, it requires independent shard review, a mandatory
final exact-head integration review, explicit principal approval at that
exact head, and post-merge verification before it may be treated as
accepted evidence. None of those steps has occurred yet.

## No scaling authority

This package authorizes nothing beyond itself. It does not authorize a
second batch, a second timeframe for COST, Stage 2 cross-timeframe
synthesis, bulk ingestion beyond this named 19-ticker cohort, a recurring or
scheduled capture process, a dashboard surface, or any research/backtest use
(including as `LADDER-0001` input) -- all of which CHART-0001
Sections 2/11 and CHART-0002 already independently prohibit without their
own separate, later, principal-accepted governance decision.
