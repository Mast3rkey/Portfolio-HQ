---
decision_id: TGT-0002
date: 2026-07-20
status: Accepted
category: portfolio_construction_governance
related_decisions: [TGT-0001, GOV-0001, PI-0003, PI-0004]
supporting_artifact: null
---

## Context

COST has been held at T2 (`weight_pct` 1.65%) since the current tier
structure was established. No prior accepted decision addresses a T2→T1
promotion question for COST specifically. The one prior mention of COST in
`CLAUDE.md`'s Decisions Log is incidental: the AAPL band→T2 promotion entry
("Tier-fit scan: AAPL promoted band → T2; AVGO stays at T2," PR #58) cites
COST only as an example of T2's existing "quality compounder" character
alongside WMT/MA/BRK.B — that entry evaluated AAPL and AVGO, not COST, and
reached no verdict on COST's own tier placement. `TGT-0001`'s
Prior-Decision Supersession list (AMZN, AVGO, AAPL) accordingly does not
include COST, and this filing supersedes no prior COST-specific reasoning
because none exists.

This filing follows `TGT-0001` (accepted the same day,
`governance/decisions/TGT-0001-additive-target-budget-policy.md`), which
requires every future roster/tier-change proposal to satisfy a Mandatory
Disclosure Template and an Ex-Ante Cluster-Compatibility Rule before
approval. This is the first proposal filed under that policy.

Recomputed directly from `targets.yaml` at filing time, prior to this
change: T1 (9 tickers × 3.35%) = 30.15%; T2 (15 tickers × 1.65%) = 24.75%,
including COST. `targets.yaml`'s `caps.clusters` list (semis, power_infra,
oil) does not include COST in any cluster's `tickers:` array. `targets.yaml`'s
`gates.t1t2_trim_mult` (1.5) is unchanged and applies to both tiers.

Current-book snapshot (evidence only, not governing authority):
`performance_log.csv`, row dated 2026-07-20 — net_equity (book) $6,150.00,
gross $7,405.64, margin_debt $1,255.64. This snapshot is cited only for the
Mandatory Disclosure Template's theoretical-gross-exposure calculation
below; it establishes nothing about COST's live holdings value, trim
status, or any other runtime allocator state, and this decision does not
run or rely on a live `allocate.py` check.

## Decision

**COST is promoted from T2 to T1**, effective in `targets.yaml`: appended
to `tiers.T1.tickers`, removed from `tiers.T2.tickers`. COST's per-name
target weight changes from 1.65% (T2) to 3.35% (T1).

This decision rests on the principal's own qualitative judgment that COST
independently possesses the qualities the principal associates with T1
placement. It is not derived from a mechanical test, a scoring model, a
ranking exercise, or any comparison against other T2 or band names — no
such ranking is imported into or relied upon by this decision.

This decision is scoped narrowly. It does not:

1. **Adopt a general T1 admission standard.** No mechanical test,
   checklist, or scoring threshold for T1 admission is established by this
   decision. A future proposal to promote a different name to T1 requires
   its own separate justification and its own separate governance filing.
2. **Re-rank or reconsider existing T1 holdings.** ASML, TSM, MSFT, GOOGL,
   META, NVDA, GEV, LLY, and V are unaffected — their placement, weighting,
   and standing rationale are untouched.
3. **Authorize another promotion.** This decision authorizes exactly one
   change: COST, T2 to T1. It does not open, pre-approve, or create a
   presumption in favor of any other roster or tier change.
4. **Touch MA.** MA remains at T2, unchanged. Any future change to MA's
   placement requires its own new decision.
5. **Bring ISRG into scope.** ISRG is not addressed by this decision in any
   way — no Company Intelligence work, no tier review, nothing.
6. **Treat Company Intelligence as authoritative.** COST's existing Company
   Intelligence record (`intelligence/companies/COST.yaml`/`COST.md`,
   `PI-0003`) remains exactly what `PI-0001` defined it to be: advisory,
   descriptive-only, and without authority over allocator behavior or tier
   placement. This decision does not read from, write to, or rely on that
   record, and does not modify it.
7. **Authorize margin, a trade, or a live allocation action.** This
   decision changes declarative target configuration only. It does not
   request, recommend, authorize, or size any margin use; does not
   instruct or authorize any trade; and does not run or constitute a live
   allocation check.

### Mandatory disclosure (per TGT-0001)

- **Ticker:** COST
- **Current sleeve / proposed sleeve:** T2 → T1
- **Current target % / proposed target %:** 1.65% → 3.35% (+1.70pp)
- **Total nominal target percentage before / after:** 101.55% → 103.25%
- **Amount above 100% before / after:** +1.55pp → +3.25pp
- **Implied fully-filled gross-exposure multiple before / after:** 1.0155x
  → 1.0325x
- **Theoretical additional gross exposure above book at snapshot:** +1.70pp
  × $6,150.00 (net equity, 2026-07-20 snapshot) ≈ **+$104.55** — a
  hypothetical figure assuming every target is simultaneously filled to
  100% of weight, not how the allocator behaves in debt-free cash-only
  operation (`TGT-0001`'s Cash-Only Behavior section), and not itself a
  margin request.
- **Source and freshness of book snapshot:** `performance_log.csv`, row
  dated 2026-07-20 (net_equity 6150.00, gross 7405.64, margin_debt
  1255.64) — filed same-day.
- **Margin statement:** This disclosure does not request or authorize
  margin. Margin remains a separate human input per `TGT-0001`'s Margin
  Separation section.
- **Debt-free cash-only gap:** widens by 1.70pp (101.55% → 103.25% nominal
  target sum, both already above 100%).
- **Combined cumulative consequences:** none — this is the only roster/tier
  change under consideration in this filing.
- **Trim-regime consequences:** COST moves from T2's mechanical, no-RSI-gate
  T1/T2 concentration-ceiling coverage to T1's — the same mechanism
  (`gates.t1t2_trim_mult`, 1.5x, floored at target), now applied at COST's
  new 3.35% target instead of its former 1.65% target. Band/spec RSI-gated
  trims never applied to COST and continue not to. No cluster-cap trim
  applies — see below.
- **Cluster-target totals before/after:** unaffected. COST is not a member
  of `semis`, `power_infra`, or `oil` in `targets.yaml`'s `caps.clusters`,
  before or after this change. No cluster's configured target total
  changes as a result of this decision.

### Ex-ante cluster-compatibility (per TGT-0001)

COST is not listed in any cluster's `tickers:` array. This decision changes
no cluster's membership or configured target total. The Ex-Ante
Cluster-Compatibility Rule is satisfied trivially — there is nothing to
check.

## Consequences

`targets.yaml`: COST appended to `tiers.T1.tickers`, removed from
`tiers.T2.tickers`. No other line in `targets.yaml` changes — cluster
definitions, gate parameters, ETF/band/spec tiers, and the crypto sleeve
are all unaffected.

T1 becomes 10 names (33.50% nominal); T2 becomes 14 names (23.10% nominal).
The configured nominal target sum rises from 101.55% to 103.25% of book,
per the disclosure above.

`CLAUDE.md`'s Decisions Log gains one short pointer entry.
`governance/decisions.yaml` gains one new row for this entry.

This decision changes no allocator code, no cluster cap, no margin
parameter, no other ticker's tier or weight, and no Company or Theme
Intelligence record. It does not run, and is not informed by, a live
`allocate.py` check — the recomputed figures above come from `targets.yaml`
and `performance_log.csv` directly, not from a live allocation run.
