---
decision_id: PHQ-2026-04
date: 2026-07-31
status: Proposed
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02, PHQ-2026-03]
supporting_artifact: governance/evidence/PHQ-2026-04/execution_facts.json
---

## Context

`PHQ-2026-03` recorded the principal's policy approval for a zero-based
SKHY/SPCX disposition (no canonical target, manual exit authorized) but was
explicitly **not** an execution record — no trade had occurred and none was
claimed. It required "a separate, future, factual-synchronization decision
and PR" (§6) before any repository mutation reflecting an actual exit, gated
on principal-supplied, verified post-trade evidence (§5): execution date,
final post-trade quantities, transaction confirmation, resulting cash
balance, and explicit confirmation that no margin was used.

The principal has now manually executed both exits in Robinhood and supplied
that evidence directly in this session as screenshots (a "Recent orders"
view and a combined "Positions + Account" view). Per this session's explicit
evidence-handling instructions, those screenshots are treated as temporary
source evidence only — inspected directly, extracted facts reported before
any file was edited, and **not retained or committed to this repository in
any form** (no image file, no byte-for-byte extraction package, unlike
`PHQ-2026-02`'s retained v1.35 evidence bundle). This is a deliberate,
narrower evidentiary-retention choice for this decision specifically, not a
correction of `PHQ-2026-02`'s own retention convention.

## Decision

**Accepted, as the factual-synchronization unit `PHQ-2026-03` §6 required,
and nothing beyond it:**

Both extracted trade records were independently read directly from the
supplied screenshots (not assumed, not inferred from any prior chat
summary):

| | SKHY | SPCX |
|---|---|---|
| Status | Filled | Filled |
| Side | Sell | Sell |
| Type | Market | Market |
| Quantity | 0.278473 | 0.502727 |
| Qty filled | 0.278473 | 0.502727 |
| Avg fill price | $147.02 | $107.94 |
| Filled notional | $40.94 | $54.27 |
| Submitted | Jul 31 15:11:27 | Jul 31 15:10:57 |
| Post-trade quantity | 0 (absent from positions list) | 0 (absent from positions list) |

Both orders show `Quantity == Qty filled` — a full fill, no partial
remainder — and both symbols are confirmed absent from the "Positions"
screenshot's Equities list, independently corroborating a full exit for
each. Post-trade account state, read directly from the same "Positions +
Account" screenshot: **cash $2,675.05**; **margin Used $0.00**.

Per `PHQ-2026-03` §6, this decision:

1. Updates `holdings.yaml` to remove SKHY and SPCX from the `shares:` block
   entirely (this repository's existing zero-position removal convention,
   not zeroing) — both fully exited, verified above.
2. Retires SPCX's `targets.yaml` destination row (0.75%) and its
   `gates.yaml` `hold_no_add` entry — the governed position is confirmed
   gone, satisfying `PHQ-2026-03` §6's "only if the position is actually
   gone" condition. **No renormalization**: the removed 0.75% target is not
   redistributed to any other row; `targets.yaml`'s `destination:` list now
   sums to 99.25%, not 100%, by design (see `targets.yaml`'s own updated
   comment).
3. Assigns no canonical target to SKHY (per `PHQ-2026-03`'s existing
   "no canonical target" determination) — no `targets.yaml` row is added.
4. Preserves sale proceeds as ordinary cash — no `targets.yaml`,
   `gates.yaml`, or `allocate.py` change allocates, recommends, or
   pre-assigns the proceeds to any name. `holdings.yaml` has no persisted
   `cash` field in its schema (unchanged since `PHQ-2026-02`); the verified
   $2,675.05 figure is recorded as evidence here, to be supplied through
   `allocate.py`'s existing `--cash` runtime input at whatever future
   session runs a live, credentialed allocation check.
5. Confirms margin debt remains `$0.00` in `holdings.yaml` — unchanged from
   its existing value, consistent with the verified $0.00 margin-used
   evidence above.

## Rationale

**FACT** — both trade records and the post-trade account state above were
read directly from principal-supplied Robinhood screenshots in this session,
not inferred, not carried forward from any prior chat summary, and cross-
checked internally (Quantity == Qty filled; both symbols absent from the
Positions list) before any repository file was edited, per this session's
evidence-handling rules. `PHQ-2026-03`'s own required evidence checklist
(§5: execution date, final quantities, transaction confirmation, resulting
cash, no-margin confirmation) is satisfied by this record in full.

**INFERENCE** — none beyond the trade/account facts themselves. This
decision does not infer a value that was obscured, cropped, or ambiguous in
the supplied screenshots; every figure above was clearly legible.

**JUDGMENT** — the principal's own PHQ-2026-03 approval already made every
policy judgment this decision executes (no canonical target for either name,
proceeds to cash, SPCX remains research-candidate-only, SKHY remains
watchlist-only); this decision makes no new judgment call, only the
mechanical repository synchronization PHQ-2026-03 §6 reserved for this
future filing.

**UNCERTAINTY** — a connected investment/holdings feed, if consulted
separately from this session's own screenshot evidence, may still lag and
display pre-trade positions for some period after execution; that potential
lag is disclosed here as a known limitation of any *other*, unconsulted data
source and is not treated as contradicting the screenshot evidence above,
which is this decision's sole and controlling execution evidence. No
connected-data corroboration is fabricated or asserted here. A later,
separate reconciliation check against connected-data state, once it has
caught up, is recorded as a follow-up (see Limitations), not a blocker to
this filing.

## Alternatives Considered

- **Retain the screenshots (or an extracted, byte-verified package) under
  `governance/evidence/`, matching `PHQ-2026-02`'s v1.35 precedent.**
  Rejected for this decision specifically — this session's explicit
  governing instructions required screenshots to be treated as temporary
  source evidence only, not saved, exported, or copied into the repository.
  This is a deliberate scope difference from `PHQ-2026-02`'s own retention
  choice, not a claim that `PHQ-2026-02`'s convention was wrong.
- **Wait for connected-data corroboration before synchronizing
  `holdings.yaml`.** Rejected — `PHQ-2026-03` §6 names principal-supplied,
  verified post-trade evidence as the controlling standard, the same
  evidentiary bar `PHQ-2026-02` itself applied to its own reconciliation;
  a connected feed's independent lag does not defeat directly-inspected,
  internally-cross-checked screenshot evidence of a completed, filled,
  zero-quantity-remaining trade.
- **Renormalize the removed SPCX 0.75% target across the remaining 36 rows.**
  Rejected — `PHQ-2026-03` explicitly authorizes no unrelated target change
  and no automatic redistribution; the gap is recorded as unallocated
  (ordinary cash), not reassigned.
- **Assign SKHY a `targets.yaml` row now that it is confirmed exited.**
  Rejected — `PHQ-2026-03` already declined a canonical target for SKHY
  independent of exit status; exiting a position does not by itself create
  a case for (re-)targeting it, and `PHQ-2026-03` §7 requires new research
  and a separate approval before that could happen.
- **Run a live `python allocate.py --review` allocation check as part of
  this filing.** Rejected — `PHQ-2026-03` §6 gates that check on both
  repository state *and* market-data prerequisites (live pricing,
  credentials) being satisfied; this session has neither the credentials
  nor a principal instruction to run one. This filing performs no
  allocation run of any kind.

## Consequences

- `holdings.yaml`, `targets.yaml`, `gates.yaml` changed exactly as described
  above; `governance/decisions/PHQ-2026-04-skhy-spcx-post-execution-factual-synchronization.md`
  (this file), `governance/decisions.yaml` (one new entry),
  `governance/evidence/PHQ-2026-04/execution_facts.json` and its `README.md`
  (new, screenshot-derived facts only, no image retained), `CLAUDE.md` (one
  concise Decisions Log pointer), and `operations/WORKSTREAMS.yaml`
  (`WS-0009` synchronized to its actual post-merge-of-PR-#204 and
  factual-sync state) are the only other files this decision changes.
  `test_phq_2026_02.py` required a small number of assertion updates where
  it had hard-coded SPCX/SKHY's pre-exit `holdings.yaml`/`targets.yaml`/
  `gates.yaml` state as a currently-true fact — disclosed in the
  implementing PR, not silently changed.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed by this decision — it records a trade the
  principal already executed manually; it does not execute one.
- No allocator behavior, unrelated target, tier, cluster, cap, or gate is
  changed. Sale proceeds remain cash, not pre-assigned to any target.
- SPCX remains a research candidate only (its `hold_no_add` gate criteria's
  underlying bar — an accessible investable vehicle, reviewed terms,
  verified financial evidence, liquidity analysis, principal approval —
  still governs any future re-entry, even though the mechanical gate entry
  itself is retired since there is no longer a held position for it to
  govern). SKHY remains a watchlist name only. Re-entry for either requires
  separate research and principal approval per `PHQ-2026-03` §7, unchanged
  by this filing.
- Per this repository's Lean Delivery and Review Lifecycle (`OPS-0009`),
  this filing is classified **Lane G** (governance authorization) — it
  narrows repository authority (retiring SPCX's gate) — and therefore
  requires the full, unreduced lifecycle: independent exact-head review,
  retained attribution, and explicit principal acceptance before merge.
  This decision does not mark itself ready and does not authorize its own
  merge.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

`governance/evidence/PHQ-2026-04/` — this decision's own smallest
repository-conforming evidence record (`execution_facts.json` plus
`README.md`), containing exactly the extracted trade and post-trade account
facts recorded above. Provenance: **principal-supplied Robinhood screenshots
reviewed during the factual-sync session; screenshots not retained in the
repository.** No account number, unrelated holding, P&L figure, buying
power, or other unnecessary private information from the supplied
screenshots is included.

## Limitations

- No connected investment/holdings feed was consulted in this session to
  corroborate the screenshot evidence; if such a feed is checked later and
  still shows pre-trade positions, that reflects ordinary provider lag, not
  a contradiction of the evidence this decision relies on. A future
  reconciliation against connected-data state, once current, is a follow-up
  check, not a blocker to this filing.
- No live, credentialed `python allocate.py --review` run was performed —
  `PHQ-2026-03` §6's own market-data/credential prerequisite for that check
  remains unresolved, unchanged from `PHQ-2026-02`'s and `PHQ-2026-03`'s own
  disclosed limitation on this point.
- This filing does not evaluate, re-open, or resolve SPCX's or SKHY's
  reopening conditions (`PHQ-2026-03` §7) — both remain exactly as
  restrictive as `PHQ-2026-03` left them.
