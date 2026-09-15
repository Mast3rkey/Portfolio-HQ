# Private ChatGPT allocation adapter

`portfolio_hq.owner.private_allocation` is an offline, recommendation-only
bridge for an authorized private ChatGPT runtime. It reads one exact retained
account submission and its receipt/review chain, validates separately supplied
dated evidence, and calls the existing `allocate.plan()` function. It does not
contact Alpaca, Yahoo, a broker, or an LLM; does not read `holdings.yaml`; and
does not write logs, cache entries, account state, or orders.

## What ChatGPT must supply

First ingest and confirm a schema-version-1 account submission through
`portfolio_hq.owner.account_staging`. The allocation supplement is a UTF-8 JSON
object with **only** these fields:

* `schema_version`: `1`.
* `as_of`: the reproducible, timezone-aware UTC allocation instant. Lifecycle
  timestamps (`submitted_at`, receipt and review times) also remain instants.
* `submission_id`, `receipt_sha256`, `review_id`, `review_sha256`, and `reviewer`: the exact
  expected submission, receipt, and confirmation identities. A missing,
  rejected, conflicting, or superseded identity fails closed. Confirmation is
  version-specific data review, not a freshness finding or authority to trade.
* `buffer`: Robinhood's actually displayed `percentage`, its `currency`, exact
  `observed_at`, and `source_id`. It is never derived. If absent, the adapter
  still returns a real canonical non-actionable result with book, cash, targets,
  gaps, and buys withheld.
* `market`: a row for every eligible non-crypto market member of the identified
  policy roster; gated names need no row. Each row supplies `ticker`, Boolean
  `available`, `price`, `sma200`, `rsi14`, `currency`, exact `observed_at`, and
  `source_id`. An explicitly unavailable row has null metrics and becomes the
  canonical ticker-local no-data result; an available row may use null SMA/RSI
  when those indicators are unavailable.
* `earnings`: exactly one row for each eligible non-crypto ticker, with `ticker`, ISO date
  `next_date` (or `null` for the canonically allowed disclosed unknown), exact
  evidence `observed_at`, and `source_id`.
* `regime`: Boolean `ok` and `known`, exact `observed_at`, and `source_id`.
  Regime remains informational.

Holding, valuation, cash, debt, and displayed-buffer observations must be no
more than two days old at `as_of` and not in its future. Their `observed_at`
may be either a timezone-aware instant or a date-only ISO value. Date-only
values use calendar-day freshness and explicitly carry no intraday precision;
they are never promoted to midnight or a retrieval instant. Old market and
earnings evidence becomes the canonical ticker-local unavailable state, and old
regime evidence becomes informational unknown rather than blocking otherwise
current book evidence. Future or malformed evidence still fails closed.
Original strings are retained in returned provenance: exact-time observations
are not converted to dates and date-only values are not promoted to invented instants.
Only USD evidence is currently actionable; another currency is reported as
unavailable because this adapter has no authorized FX conversion. Every nonzero
holding needs a dated unit valuation. Non-roster holdings remain explicit
orphans in the canonical book and receive no invented target. Submitted
`protected_capital` rows remain evidence only—the canonical target/gate policy,
not an inferred account label, determines protected capital.

The principal must provide facts a read-only connection does not expose:
the displayed maintenance buffer, complete quantities (including dust), debt,
cash, valuations for every nonzero position, and any broker-specific distinction
needed to prevent cash/debt double counting. Crypto is a holding, never USD cash.
Account holdings named `CASH` or `RESERVE` are refused because those identifiers
are canonical synthetic sleeves and accepting them would double count capital.

## Python and private-runtime CLI

```python
from portfolio_hq.owner.private_allocation import run

envelope = run(
    "/private/runtime",
    supplement_bytes,
    source_root="/workspace/Portfolio-HQ",
    expected_source_sha="<exact reviewed commit SHA>",
)
```

```console
python -m portfolio_hq.owner.private_allocation \
  --runtime-root /private/runtime \
  --supplement /private/request.json \
  --source-root /workspace/Portfolio-HQ \
  --expected-source-sha '<exact reviewed commit SHA>'
```

The adapter verifies both working bytes and named-commit blobs for the three
policy files and its executing adapter/allocator dependencies, refuses staged,
dirty, redirected, or mixed-checkout inputs, and parses the already-verified
policy bytes without a second filesystem read.

The envelope contains the actual canonical result, actionability and blocked
reasons, discrepancies, limitations, exact evidence hashes, source commit SHA,
and hashes for `targets.yaml`, `gates.yaml`, and `issuer_lookthrough.yaml`.
It contains recommendations—not orders or executable order payloads. Exit status
is zero only for actionable evidence and two otherwise.
