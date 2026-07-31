---
decision_id: PHQ-2026-05
date: 2026-07-31
status: Proposed
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04]
supporting_artifact: governance/evidence/PHQ-2026-05/v1_37/Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json
---

## Context

`PHQ-2026-02` reconciled `holdings.yaml` from the v1.35 evidence package.
Separately, `PHQ-2026-04` (this repository's other currently-open governance
PR, #205) records the principal's manual SKHY/SPCX exit, evidenced by
execution-fill facts (submitted 2026-07-31 15:10:57–15:11:27 ET, both filled,
both confirmed absent from the post-trade Positions screenshot, resulting
cash $2,675.05).

The principal has now supplied a further, later "Final Confirmed Account
State v1.37" package — a `MANIFEST.json` (with per-file SHA-256), a JSON
account-state export, a CSV holdings export, and a README — described as
"the final post-buy quantities shown in the principal-supplied mobile
holdings screenshots" after "all seven buy fills," with an `effective_time`
of "2026-07-31 approximately 16:13 ET." All three data files' SHA-256 hashes
were independently recomputed this session and matched the manifest exactly.

**Direct comparison against `holdings.yaml` as reconciled through
`PHQ-2026-04`** (i.e., after SKHY/SPCX removal) found exactly seven changed
or added `shares:` quantities and zero other equity/fund/crypto changes:

| Ticker | Pre-v1.37 | v1.37 confirmed | Change |
|---|---|---|---|
| AMZN | 0.423377 | 1.146551 | increased |
| NVDA | 0.986492 | 1.858992 | increased |
| TMO | 0.2038 | 0.325606 | increased |
| SPY | 0.25105 | 1.250856 | increased |
| PWR | (none) | 0.116807 | new |
| VEA | (none) | 6.186296 | new |
| VWO | (none) | 0.476555 | new |

All other tracked equities/funds (ASML, AVGO, CEG, COST, ETN, GEV, GLD,
GNRC, GOOGL, ISRG, KLAC, LLY, META, MSFT, PANW, RTX, TSM, V) and all crypto
(BTC, ETH, SOL) are identical between the pre-v1.37 state and the v1.37
package — independently confirmed by a full field-by-field diff, not
assumed. PWR, VEA, and VWO each already carry an existing canonical
`targets.yaml` destination row (1.25%, 7.00%, and 1.00% respectively) — this
filing introduces no new ticker, target, cap, or gate; it only updates share
counts for names the canonical architecture already governs.

**A material, unresolved conflict was found and escalated to the principal
before any file was edited**: the v1.37 package's own `positions` list still
includes SKHY (0.278473 sh) and SPCX (0.502727 sh) at their exact pre-exit
quantities, and its README/JSON both instruct to "preserve SPCX hold/no-add"
and "leave SKHY unresolved" — i.e., treats them as continuing holdings, not
exited. This directly contradicts `PHQ-2026-04`'s independently-evidenced
sale-fill facts. The v1.37 package's reported cash ($845.84) also does not
reconcile against `PHQ-2026-04`'s post-sale-only cash ($2,675.05), even after
accounting for the cost of the seven buy fills above. The principal was
asked directly and confirmed: **`PHQ-2026-04`'s SKHY/SPCX exit facts control;
v1.37's SKHY/SPCX rows and cash figure are treated as stale for those two
data points specifically.**

## Decision

**Accepted, bounded to exactly the seven-quantity reconciliation above:**

1. Updates `holdings.yaml`'s `shares:` block: AMZN, NVDA, TMO, SPY quantities
   updated to their v1.37-confirmed values; PWR, VEA, VWO added at their
   v1.37-confirmed quantities (new share-tracked positions, not new
   tickers to the canonical architecture — see table above).
2. Makes **no** change to SKHY or SPCX. Both remain exactly as `PHQ-2026-04`
   left them (removed from `holdings.yaml`/`targets.yaml`/`gates.yaml`, zero
   position, not restored). This filing does not reopen, edit, or
   second-guess `PHQ-2026-04`.
3. Makes **no** change to `targets.yaml`, `gates.yaml`, or
   `issuer_lookthrough.yaml` — every changed/added ticker already has an
   existing canonical row; no target, cap, or gate is added, removed, or
   resized.
4. Discloses, but does not resolve, the cash discrepancy between v1.37
   ($845.84) and `PHQ-2026-04`'s post-sale cash ($2,675.05) — `holdings.yaml`
   has no persisted cash field (unchanged since `PHQ-2026-02`), so this
   filing has nothing to mutate on that point. Flagged as an open item
   requiring principal re-verification before the confirmed cash balance is
   relied on for any future cash-funded `allocate.py --cash` run.
5. Retains the full v1.37 evidence package verbatim under
   `governance/evidence/PHQ-2026-05/v1_37/` (`MANIFEST.json`, the JSON
   account-state export, the CSV holdings export, `README.md`) — SHA-256
   independently reconfirmed against the manifest at filing time.

## Rationale

**FACT** — the seven-ticker delta table above was derived by a direct,
field-by-field comparison between `holdings.yaml`'s state after `PHQ-2026-04`
and the v1.37 package's `positions` list (JSON), cross-checked against the
CSV export (identical quantities in both v1.37 files). All three v1.37 data
files' SHA-256 hashes were independently recomputed and matched
`MANIFEST.json` exactly before any repository file was edited.

**INFERENCE** — none of the seven quantity changes required inference; each
is a directly-stated `quantity` field in the v1.37 JSON/CSV, both internally
consistent with each other.

**JUDGMENT** — resolving the SKHY/SPCX conflict between v1.37 and
`PHQ-2026-04` is a judgment this repository's evidence alone cannot make
(this session was explicitly instructed not to query Robinhood or infer tax
lots). The principal was asked directly and made the call: `PHQ-2026-04`'s
independently-evidenced, timestamped sale-fill record controls over v1.37's
apparently-stale SKHY/SPCX rows. This filing implements that principal
judgment; it does not make the call itself.

**UNCERTAINTY** — the root cause of v1.37's stale SKHY/SPCX rows and
non-reconciling cash figure is not established by this filing (e.g., whether
v1.37's screenshots were captured before the `PHQ-2026-04` sale despite a
later-stamped `effective_time`, or some other explanation). This filing does
not speculate further and treats the principal's direction as controlling
without asserting a mechanism for the discrepancy.

## Alternatives Considered

- **Apply v1.37 verbatim, including its SKHY/SPCX rows.** Rejected — would
  silently re-introduce two positions `PHQ-2026-04` independently evidenced
  as sold, and was explicitly rejected by the principal when the conflict
  was escalated.
- **Wait for `PHQ-2026-04` (PR #205) to merge before filing this
  reconciliation.** Rejected — `PHQ-2026-04`'s exact commits were adopted
  directly onto this filing's branch (a clean fast-forward from the same
  base) rather than duplicated or re-derived, so this filing's diff against
  `main` is self-consistent and correctly sequenced; no conflicting branch
  was created. This filing does not alter, and is not itself, `PHQ-2026-04`.
- **Resolve the cash discrepancy by picking one of the two reported figures
  as authoritative.** Rejected — `holdings.yaml` has no persisted cash
  field to update, and picking a number without principal-supplied
  reconciling evidence would fabricate a fact this session cannot verify.
  Disclosed as an open item instead.
- **Add new `targets.yaml` rows for PWR/VEA/VWO.** Rejected — unnecessary;
  all three already have canonical destination rows from `PHQ-2026-02`'s
  migration. This is a quantity update only.

## Consequences

- `holdings.yaml` changed exactly as described (seven `shares:` quantities);
  `governance/decisions/PHQ-2026-05-post-buy-quantity-reconciliation-v1-37.md`
  (this file), `governance/decisions.yaml` (one new entry),
  `governance/evidence/PHQ-2026-05/v1_37/` (new, retained verbatim), and
  `CLAUDE.md` (one concise Decisions Log pointer) are the only other files
  this decision changes. No `targets.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, or
  `operations/WORKSTREAMS.yaml` change.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed by this decision — it records buy fills the
  principal already executed manually.
- No allocator behavior, tier, target, cluster, cap, or gate is changed.
  SKHY and SPCX remain exactly as `PHQ-2026-04` left them.
- Per this repository's Lean Delivery and Review Lifecycle (`OPS-0009`),
  this filing is classified **Lane M** (mechanical/factual synchronization)
  — it records already-true, principal-confirmed post-buy quantities and
  introduces no new tier/target/cluster/cap/gate/allocator authority. Per
  `OPS-0009` §2, Lane M may omit a separate independent-review round of the
  recording itself, but every other control still applies in full,
  including explicit principal acceptance of the underlying facts before
  merge, protected-path verification, and applicable test/validator
  re-confirmation. This decision does not mark itself ready and does not
  authorize its own merge.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

`governance/evidence/PHQ-2026-05/v1_37/` — the principal-supplied v1.37
package retained verbatim (`MANIFEST.json`, `Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json`,
`Portfolio_HQ_Final_Confirmed_Holdings_v1_37.csv`, `README.md`). SHA-256 of
each file independently recomputed and matched against `MANIFEST.json` at
filing time:

- `Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json`:
  `782f68284b92377ed396584a63c112f7835900ac18a2d117d85f62239da85ebd`
- `Portfolio_HQ_Final_Confirmed_Holdings_v1_37.csv`:
  `c091ef39994829a2ebfd71baa419983a820cd43fbcd23d13ba18e845a6a4636b`
- `README.md`: `ab17dfe6314c549d74bd8edf4a2b4ad2a9d43f104e1940115038106d4b1bf38c`

## Limitations

- The cash discrepancy between v1.37 ($845.84) and `PHQ-2026-04`'s post-sale
  cash ($2,675.05) is disclosed, not resolved. It should be re-verified
  against a fresh Robinhood screen before being relied on for any future
  `allocate.py --cash`-funded run; this filing's own allocation check (see
  the implementing PR) uses `--review` (no new cash) specifically to avoid
  depending on either disputed figure.
- The root cause of v1.37's stale SKHY/SPCX rows is not established (see
  Rationale, Uncertainty).
- This filing does not evaluate, re-open, or resolve SPCX's or SKHY's
  reopening conditions (`PHQ-2026-03` §7) — unchanged.
