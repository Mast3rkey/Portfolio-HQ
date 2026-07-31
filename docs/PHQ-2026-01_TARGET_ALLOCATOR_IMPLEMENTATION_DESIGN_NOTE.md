# PHQ-2026-01 target/allocator implementation — design note

**Design only. Authorizes no implementation.** Filed alongside
`governance/decisions/PHQ-2026-01-canonical-architecture-and-transition-policy-approval.md`,
which approved the canonical v1.30 destination architecture and the
actionable-core transition architecture as *policy*. This note answers the
questions a future implementation PR must resolve before touching
`targets.yaml`, `allocate.py`, `margin_state.py`, or any test — it does not
answer them by writing code, and it does not authorize a future session to
proceed without its own separate principal approval (see §10).

Status: **proposed, unauthorized.** No branch, PR, or code exists for this
work as of this note.

---

## 1. Controlling source for canonical destination targets

`targets.yaml` remains the sole file the allocator (`build_roster()`,
`plan()`) reads at runtime — that does not change. The open design question
is how `targets.yaml` itself should represent the *approved destination*
(canonical v1.30, 37 rows) versus the *current operating* configuration,
given PHQ-2026-01 approved the former as policy without making it effective.

Two shapes were considered, neither implemented here:

- **Single-source shape**: `targets.yaml` is edited directly to the canonical
  v1.30 weights, with gated names' rows carrying a `gated: true` flag (see
  §2) instead of being omitted or zeroed silently.
- **Two-document shape**: a new `targets_destination.yaml` (or a `destination:`
  block inside `targets.yaml`) holds the approved canonical v1.30 figures for
  reference/drift-monitoring, while the existing `targets.yaml` top-level
  structure remains the only thing `build_roster()`/`plan()` read, edited
  only when a specific implementation PR is authorized to move a specific
  name.

The single-source shape is likely preferable — it avoids a second file
`allocate.py` must decide whether to read, keeps `targets.yaml` config-is-truth
(per `CLAUDE.md`), and lets `--health` or a future report diff "current" vs
"gated-but-approved-destination" from one file. This preference is not a
decision; the actual choice is deferred to the authorized implementation PR.

## 2. Actionable-core gating alongside approved destination targets

A gated name's row must carry both its approved destination weight (for
future activation) and its current cash-holding status, without deleting the
destination figure. Candidate representation: extend each `targets.yaml` tier
entry with an optional `gate:` block —

```yaml
- ticker: SNPS
  target_pct: 2.5
  tier: T1              # or whichever tier v1.30 assigns
  gate:
    status: cash_pending_clearance
    authority: PHQ-2026-01
    next_gate: "Review after 2026-09-30 Investor Day and a fresh normalized valuation model"
```

`build_roster()`/`plan()` would need a new rule: a gated ticker's target
capital is not renormalized into other names (§3) and the allocator never
proposes a buy for it, regardless of gap size, until `gate.status` changes.
This is additive to the existing gate order (200-SMA trend → earnings
blackout → caps) — it would need to run *before* those, as a hard exclusion,
not a timing gate.

## 3. Gated allocations remain cash without renormalizing

This is the sharpest design risk. The allocator's existing gap-filling logic
computes each name's dollar gap against its target weight of the *whole
book*; if gated names are simply dropped from the roster, their target
percentage points don't disappear — they get silently redistributed pro rata
across every remaining name's gap, inflating everyone else's target beyond
what canonical v1.30 or the actionable core actually specifies. That is
exactly the "gated allocation renormalizes into other companies" failure mode
this decision must not produce.

The correct shape: gated names stay **in** the roster and **in** the target
total (so the book's target percentages still sum against 100%), but their
own gap is permanently treated as satisfied by cash — i.e., a synthetic
`RESERVE`/`CASH` sleeve absorbs their target weight (see §4) rather than the
allocator either buying them or spreading their weight elsewhere. This needs
a new roster field (e.g. `gate.absorbed_by: RESERVE`) and a new `plan()`
branch that recognizes a gated name's "gap" as already-filled-by-cash rather
than computing a real buy gap for it.

## 4. Representing RESERVE, CASH, SPCX, and gated public names

- **RESERVE / CASH**: the actionable-core `test_portfolios.json` already
  models this as a `CASH` line (12.5% in `actionable_core_all_uncleared_allocations_as_cash`,
  5.75% in `canonical_proposed_spcx_and_reserve_as_cash`). `targets.yaml`
  would need an explicit `CASH`/`RESERVE` roster entry that the allocator
  recognizes as "never buy, holds the reserve," distinct from an
  ordinary target gap.
- **SPCX**: gated, `HOLD TARGET IN CASH` per
  `governance/evidence/PHQ-2026-01/final_due_diligence/Portfolio_HQ_Gated_Name_Disposition_v1_32.csv`
  — not sell-all. If SPCX is already a live holding (current
  `holdings.yaml` state, not yet reconciled — see §8), its target-capital
  treatment under this design is "hold what exists, don't add more," which
  is a *different* rule from "target capital sits in cash because nothing is
  held yet." The implementation PR must determine SPCX's actual current
  holding status from reconciled `holdings.yaml` before choosing between
  these two gate behaviors — this note does not resolve it.
- **Other gated public names** (SNPS, ICE, SPGI, WM, RKLB, TSLA): target
  capital absorbed by RESERVE per §3, individually re-evaluated at each
  ticker's own `next_gate` criterion (already recorded per-name in the
  Gated Name Disposition evidence).

## 5. Monitoring the 8% effective-issuer ceiling

Requires an ETF look-through computation the allocator does not currently
have — `allocate.py` has no concept of "this ETF's holding of that
ticker contributes embedded weight." The `Portfolio_HQ_Look_Through_Exposure_v1_32.csv`
evidence shows the shape (`direct_target + fund_allocation × fund_holding_weight
= effective_weight`) but was computed externally, from ETF constituent data
this repository's Alpaca client does not fetch. A future implementation would
need either (a) a periodically-refreshed, hand-maintained ETF constituent
table (config, not live-fetched — consistent with `targets.yaml`'s
config-is-truth pattern and this repository's general reluctance to add new
live external dependencies), or (b) explicit deferral of live 8%-ceiling
monitoring to the quarterly review process (manual, using the same due-diligence
methodology) rather than a runtime allocator check. This note recommends (b)
as the smaller, lower-risk first step, with (a) as a possible later
enhancement — not decided here.

## 6. Monitoring the 40% AI/platform common-driver ceiling

Same data dependency as §5, plus a second undefined input: which tickers
count toward "AI/platform common driver" is a judgment call the due-diligence
package made once (evidently: the "mega6" plus look-through AI-exposed names)
but that grouping is not the same as `targets.yaml`'s existing `semis` cluster
or the declined T1-AI-infra cluster cap (`CLAUDE.md` Decisions Log,
"T1 AI-infra cluster cap: scanned and declined"). A future implementation
must not silently reuse the `semis` cluster definition for this — it would
need its own explicit membership list, sourced from the PHQ-2026-01 evidence
or a fresh review, and its own governance decision if it is ever to become a
mechanical allocator cap rather than a monitored figure. Given the measured
figure is already ≈40.03% (marginally over, per the accepted decision's own
Limitations section), this ceiling arguably needs resolving *before* any
implementation PR proceeds — see §10.

## 7. Required allocator behavior changes

None are authorized by this note. If a future implementation PR is
separately authorized, the likely change surface (not a commitment) is:

- `build_roster()`: read gate/RESERVE fields from `targets.yaml`; exclude
  gated names from ordinary gap-buy candidates.
- `plan()`: new gated-absorption branch (§3); no change to existing 200-SMA
  trend, earnings blackout, cluster-cap, or T1/T2-ceiling gates, which
  continue to apply to every non-gated name exactly as today.
- `--health`: extend to show effective-issuer/common-driver monitoring
  figures if §5/§6 land on the config-table approach; otherwise no change,
  and monitoring stays a manual quarterly-review step.
- No change to `margin_state.py` — PHQ-2026-01 authorizes no new margin and
  the existing 1.8x cap / 30% buffer floor are untouched by this whole
  effort.

## 8. Reconciling `holdings.yaml` after pending Robinhood orders

Out of scope for the implementation PR itself, and a hard prerequisite before
it can run meaningfully: some Robinhood orders were entered after the frozen
v1.31 snapshot, some filled, some were queued. `holdings.yaml` must be
resynchronized from principal-supplied post-execution evidence (screenshots
or `TICKER qty` lines via the existing `update-shares`/`update-crypto-shares`/
`update-holdings`/`update-margin` workflow in `CLAUDE.md`) **before** any
gap/buy computation under the new architecture would be meaningful — running
the new gating logic against stale `holdings.yaml` would manufacture false
signals the same way a stale margin sync already has once before (see
`CLAUDE.md`'s T1/T2 ceiling Open Item, "a mechanical trim rule interacting
with a stale book will manufacture false signals mechanically"). This
reconciliation is principal-driven, not something a Claude session can infer
or reconstruct from the PHQ-2026-01 evidence, which is itself explicitly
historical (see the accepted decision's Limitations).

## 9. Keeping historical snapshots separate from live state

Already enforced by convention this PR follows: the frozen v1.31 snapshot,
the account-equity/margin figures inside `master_research_report.json`'s
`frozen_state` block, and the provisional transition map are retained only
under `governance/evidence/PHQ-2026-01/`, clearly labeled historical (see
that directory's `README.md`), and never written into `holdings.yaml`. A
future implementation PR must preserve this separation — no script or report
under the new work may read `governance/evidence/PHQ-2026-01/` as if it were
current state. If the implementation PR wants a "current vs. approved
destination" comparison view, it should compute "current" fresh from
reconciled `holdings.yaml` (§8) and "approved destination" from `targets.yaml`
post-implementation (§1) — never from the frozen evidence files.

## 10. What requires a new principal approval before implementation

This note identifies at least four items that are not resolved by
PHQ-2026-01 and need explicit principal direction before an implementation PR
can be authorized to start:

1. **Which representation shape** for destination-vs-actionable targets
   (§1), gating (§2), and RESERVE/CASH (§4) — these are structural choices
   with real behavioral consequences, not mechanical translation.
2. **How the 8%/40% ceilings get monitored** (§5/§6) — config table vs.
   manual quarterly review vs. a new mechanical cap, and, if a config table,
   who maintains the ETF-constituent and AI/platform-membership data and how
   often.
3. **The measured ≈40.03% AI/platform figure** — already at/over the
   approved ceiling as measured. Whether this blocks starting the
   implementation PR, is accepted as a monitoring flag to resolve during
   implementation, or requires a fresh look-through recompute first is a
   principal call, not an engineering one.
4. **`holdings.yaml` reconciliation** (§8) — the principal must supply
   post-execution evidence; no session can proceed without it.

No implementation PR should begin against `targets.yaml`, `allocate.py`,
`margin_state.py`, or their tests until the principal has separately approved
answers to at least these four items, consistent with `PHQ-2026-01`'s own
explicit reservation of "targets.yaml and allocator behavior still require a
separate design/review/implementation workstream."
