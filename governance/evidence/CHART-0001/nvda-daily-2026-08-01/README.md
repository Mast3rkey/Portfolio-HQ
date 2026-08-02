# CHART-0001 NVDA daily pilot evidence

This is the single, bounded evidence package for the CHART-0001 Section 8
one-asset/one-screenshot pilot: **NVDA, daily timeframe, captured
2026-08-01**.

## Why this package exists

`governance/decisions/CHART-0001-chart-evidence-pilot-governance-proposal.md`
defines an advisory Chart Evidence Record type and, once accepted, authorizes
exactly one future implementation PR for a bounded one-asset/one-screenshot
pilot. The principal's dated acceptance note and the further principal
authorization quoted in this PR's description activate that pilot's
*preparation* — this package is that preparation. It is not itself accepted,
merged, or effective as chart-evidence policy until its own independent
`OPS-0007` §1 review and explicit principal acceptance, per CHART-0001 §§8-9
and §14.

## Exact scope: one image, one asset, one timeframe

- **Asset:** NVDA (NVIDIA Corporation), equity.
- **Timeframe:** daily (1D).
- **Source:** the sole canonical NVDA daily screenshot in the read-only,
  externally governed Chart-Automation library
  (`Chart-Automation/library/governed/2026-08-01/NVDA/NVDA__2026-08-01__1D.png`,
  project-relative reference only — no absolute user path is committed here
  or anywhere in this package).
- No second image, no other ticker, no other timeframe, and no batch of any
  kind is included. This mirrors CHART-0001 §4/§8's own "exactly one" scope.

## Files in this package

- `NVDA__2026-08-01__1D.png` — the retained chart image. **Not** byte-for-byte
  identical to the governed source (see Privacy below); it is a
  privacy-redacted derivative. SHA-256 `7afb06217c762a3d31f20e9cf92339dfa4bc0ea73870fd2f3817f3e5452c220b`,
  656,463 bytes, PNG, 3624x2336.
- `record.yaml` — the structured advisory Chart Evidence Record: identity and
  capture metadata, the privacy/redaction disposition, content split cleanly
  into `visible_facts` / `observations` / `inferences` / `uncertainties`,
  thesis-relationship and advisory-boundary fields, provenance, and lifecycle.
- `MANIFEST.json` — hash reconciliation, the full source-provenance chain
  (governed library → this package), the privacy result and transformation
  detail, and the verifiability boundary.
- This `README.md`.

No second screenshot, thumbnail, OCR-extracted text file, or derivative chart
is present. No `chart_evidence/` directory, index file, or validator is
created — this package reuses the existing `governance/evidence/<decision-id>/`
pattern already established by `PHQ-2026-01` through `PHQ-2026-06`, per
CHART-0001 §4.

## Source and provenance boundary

The governed Chart-Automation library establishes, independently of this
session, that `NVDA__2026-08-01__1D.png` is the sole canonical NVDA daily
screenshot for the 2026-08-01 governed batch (`chart_inventory.json`'s NVDA/1D
record shows `duplicate_group: null`) and that its SHA-256
(`0ddc0eb0aded012618c368343f657f983d5bb9db7d130f58965f4bb542c4055f`) is
identical across the library file itself, the copy manifest's
source/destination hash pair, and the separate chart inventory record. This
session independently recomputed that hash directly against the file on disk
and confirmed the three-way match, rather than trusting any single record. See
`MANIFEST.json`'s `source_provenance_chain` for the full chain and its
disclosed, unavoidable trust boundary (identical in kind to every prior
`PHQ-####` screenshot-evidenced decision in this repository — see
`governance/evidence/PHQ-2026-06/README.md` for the closest precedent).

The Chart-Automation project itself was read-only for this session: nothing
under `~/Projects/Chart-Automation` was modified, renamed, copied within,
reorganized, regenerated, or deleted, and `~/Downloads` was never accessed
directly.

## Privacy result

**Redacted, not passed clean.** The governed source image's top-left capture
watermark visibly showed a TradingView platform username ahead of "created
with TradingView.com, Aug 01, 2026 14:16 UTC-4". CHART-0001 §5 permits a
narrow, principal-approved, per-image username exception, but the principal
authorization governing this specific pilot implementation states explicitly
that **no username exception is authorized for this exact image**. The
username was therefore covered with a solid black rectangle before the file
was ever written into this repository; the date/time/platform text beside it
remains fully legible, and no other part of the chart was altered. Full
transformation detail, including the exact pixel region, is in
`MANIFEST.json`. No other private, account-level, or brokerage-identifying
information (balances, account numbers, positions, order history,
buying-power/margin figures, email, real name, or watchlist contents) is
present anywhere in the image.

## Fact vs. interpretation boundary

`record.yaml`'s `content` block keeps four lists strictly separate, per
CHART-0001 §3/§9:

- `visible_facts` — only what is literally legible in the image (labels,
  values, line positions, colors, panel structure).
- `observations` — descriptive statements grounded directly in those facts,
  still non-interpretive.
- `inferences` — explicitly labeled interpretive judgments, hedged, never
  presented as fact, and never a prediction, score, or recommendation.
- `uncertainties` — everything not legible, not confirmed, or ambiguous,
  including indicator names/parameters that are not shown anywhere in the
  image and are recorded as unknown rather than guessed.

No indicator setting, date, or price level anywhere in this package was
invented. No live market data or external research was used to fill any gap
in what the image itself shows, per CHART-0001's own prohibition.

## Advisory-only status — what this package does and does not do

This package is **secondary observational evidence only** — a single, dated,
point-in-time chart capture. It:

- does **not** change `intelligence/companies/NVDA.yaml` or any other
  Company/Theme Intelligence record;
- does **not** change NVDA's tier, target, or canonical destination weight in
  `targets.yaml`;
- does **not** change `holdings.yaml`, any share count, or any margin
  parameter;
- does **not** affect `allocate.py`'s output, any allocator computation, or
  any live-priced holding value;
- does **not** create, feed, or in any way touch `LADDER-0001`'s research
  charter or protocol (which independently excludes chart/screenshot input
  from its own study);
- does **not** create an order, a trade recommendation, a technical score, or
  a ranking of any kind.

`record.yaml`'s `thesis_relationship.governed_consequence` is explicitly
`none`.

## Freshness limitation

This is a **daily-timeframe** capture, which per CHART-0001 §7 goes stale
faster than a weekly one. `record.yaml`'s `lifecycle.review_or_expiration_date`
records an analyst-chosen advisory heuristic (roughly five trading sessions
after capture) — not a governed cadence, and not equivalent to Company
Intelligence's `review.cadence_days`/`next_due` fields, which this package
does not use or extend. Staleness past that date requires disclosure or
analyst abstention from relying on this record, never an automatic policy
change of any kind.

## Outstanding review and acceptance gates

This package, and the PR that introduces it, are **not** effective chart-
evidence policy on their own. Per CHART-0001 §§8-9 and §14, still required
before this pilot may be considered complete:

1. Independent, exact-head review under `OPS-0007` §1 (this is `OPS-0009`
   Lane G in full, per CHART-0001 §8 — never reduced weight).
2. Any bounded correction such review finds necessary, plus exact-head
   re-review.
3. Explicit principal acceptance at the exact final head.
4. Merge to `main`, followed by post-merge verification per `OPS-0009` §4(a).

This PR is opened as a **draft** and stays draft through this session. No
merge, no "ready for review" transition, and no independent review are
performed by this authoring session.

## No scaling authority

This package authorizes nothing beyond itself. It does not authorize a second
image, a second asset, a second timeframe, bulk ingestion, a recurring or
scheduled capture process, a `chart_evidence/` index, a dashboard surface, or
any research/backtest use (including as `LADDER-0001` input) — all of which
CHART-0001 §§2/11 already independently prohibit without their own separate,
later, principal-accepted governance decision.
