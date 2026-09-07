# PHQ-2026-04 evidence

## Provenance

Principal-supplied Robinhood screenshots reviewed during the factual-sync
session; **screenshots not retained in the repository.** Unlike
`governance/evidence/PHQ-2026-02/`'s retained v1.35 package (a zip archive
with independently-verified SHA-256s for its extracted contents), this
decision's evidence-handling instructions required screenshots to be treated
as temporary source evidence only — inspected directly in-session, facts
extracted and reported before any repository file was edited, then
discarded. No image file, extracted screenshot fragment, or byte-verified
package of either screenshot exists anywhere in this repository.

## What was inspected

Two screenshots, supplied directly in the factual-sync session:

1. A "Recent orders" table showing, among other rows out of this decision's
   scope, two `Filled` `Sell` `Market` orders for SKHY and SPCX.
2. A combined "Positions + Account" view showing the post-trade Equities
   positions list (SKHY and SPCX absent) and the account's cash/margin
   summary panel.

## Extracted facts

See `execution_facts.json` (this directory) for the complete machine-readable
record: per-symbol status/side/type/quantity/qty-filled/avg-fill-price/
filled-notional/submitted-timestamp/post-trade-quantity, plus the post-trade
account's cash and margin-used figures. Every value there was read directly
and was clearly legible — no obscured, cropped, or ambiguous value was
inferred or guessed.

## Deliberately excluded

Per this session's evidence-handling rules, the following were visible in
the supplied screenshots but are deliberately **not** included anywhere in
this evidence record: account number, unrelated equity/crypto holdings and
their individual mark/quantity/P&L figures, today's/YTD P&L, buying power
(equities/options/futures/crypto), margin available/maintenance-requirement
figures beyond the single `margin_used_usd: 0.0` fact, and the ~28 unrelated
Jul 30 sell orders visible in the same "Recent orders" screenshot (out of
this decision's SKHY/SPCX-only scope; those trades pre-date and are already
reflected in the `PHQ-2026-02` v1.35 reconciliation baseline this decision
builds on, not a separate open item this filing addresses).

## Connected-data reconciliation

Not performed this session — no connected investment/holdings feed was
consulted. If checked later and still showing pre-trade positions, that
reflects ordinary provider lag, not a contradiction of this evidence. See
the parent decision's Limitations section.
