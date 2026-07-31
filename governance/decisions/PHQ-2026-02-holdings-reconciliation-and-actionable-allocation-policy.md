---
decision_id: PHQ-2026-02
date: 2026-07-31
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, PHQ-2026-01]
supporting_artifact: governance/evidence/PHQ-2026-02/reconciliation_check.json
---

## Context

`PHQ-2026-01` approved canonical v1.30 (the 37-row destination architecture)
and the actionable-core transition posture as policy, but explicitly deferred
three things to a separate future workstream: implementing `targets.yaml`
against that architecture, reconciling `holdings.yaml` from post-execution
evidence, and resolving the open representation questions in
`docs/PHQ-2026-01_TARGET_ALLOCATOR_IMPLEMENTATION_DESIGN_NOTE.md` §10. This
decision is that separate workstream's governance record.

The principal supplied two inputs that resolve those open items: (1)
principal-supplied post-execution Robinhood screenshots, packaged and
verified as `Portfolio_HQ_Post_Execution_Reconciliation_v1_35.zip` (SHA-256
`fb8eb811df29eb560bfaed16e8d0e89c6cbcf44bc42e1f1ae2ccfca4cddd889e`, retained
verbatim under `governance/evidence/PHQ-2026-02/v1_35/`); and (2) an explicit
principal policy approval resolving design-note §10's representation-shape,
ceiling-monitoring, and 40.03%-measurement questions, quoted verbatim below.

## Decision

**Accepted, as principal-approved policy:**

> "I approve PHQ-2026-02 as recommended: targets.yaml remains the canonical
> destination source; actionable gates are represented separately; gated
> capital remains cash without renormalization; the 8% issuer and 40%
> common-driver ceilings are no-add controls rather than automatic sell
> rules; the existing measured 40.0284% exposure is recorded as above the
> ceiling and may not be increased without separate approval; holdings.yaml
> may be reconciled only from post-execution evidence; SPCX remains hold/no
> add and SKHY remains unresolved; implementation remains advisory-only with
> manual Robinhood execution."

This resolves design-note §10 as follows:

1. **Representation shape (§1/§2)**: single-source — `targets.yaml`'s
   `destination:` list is the canonical v1.30 architecture directly (37
   rows, weights transcribed verbatim from the retained PHQ-2026-01
   evidence, `governance/evidence/PHQ-2026-01/final_due_diligence/Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json`
   `architecture_rows`). Actionable gates are represented **separately**, in
   a new `gates.yaml` — not as an inline `gate:` block per the design note's
   original candidate shape.
2. **Ceiling monitoring (§5/§6)**: neither deferred to manual quarterly
   review nor a live ETF-constituent fetch — a hand-maintained,
   point-in-time look-through config (`issuer_lookthrough.yaml`, transcribed
   verbatim from `Portfolio_HQ_Look_Through_Exposure_v1_32.csv`) backs a
   mechanical **no-add control** in `allocate.py`'s `plan()`: blocks/clips a
   buy that would push effective issuer exposure to/above 8% or common-driver
   exposure to/above 40%. Never a trim/sell rule.
3. **The 40.0284% figure**: retained exactly as measured (not rounded),
   labeled above-ceiling, and recorded as a point-in-time policy fact that
   may not be increased without separate approval — alongside a live,
   separately-labeled current calculation from reconciled holdings.
4. **`holdings.yaml` reconciliation**: performed from the v1.35 evidence
   package only (see below) — quantities are the controlling evidence.

## Holdings reconciliation

The v1.35 package's later screenshot is the complete post-transition
equity/fund list — 24 total rows, SPCX and SKHY included within that 24, not
additional to it — and the earlier screenshot the complete crypto list (7
rows, including permanently-ignored dust) — confirmed by two internal
cross-checks (sum of listed equity rows vs. the screenshot's own displayed
equities total, within $0.02; margin used $0.00 vs. a previously synced
$1,590.40 debt, consistent with sale proceeds repaying inherited debit per
`PHQ-2026-01` point 7) **and explicitly confirmed by the principal** before
any file was changed — not inferred from the arithmetic alone. The 41
previously-tracked tickers absent from the v1.35 evidence were removed from
`holdings.yaml`'s `shares:` block entirely (not zeroed), consistent with this
repository's existing zero-position convention (BTC, 2026-07-13). Full
detail, the machine-readable reconciliation check, and every retained
evidence file: `governance/evidence/PHQ-2026-02/`.

`holdings.yaml`'s `shares:` block now holds 24 total equity/fund positions
(including SPCX, gated hold/no-add, and SKHY, unresolved) plus BTC/ETH/SOL in
`crypto_shares:`, margin debt `$0.00`. **`holdings.yaml` has no `cash` field
in its current schema** — the verified post-execution cash figure,
`$2,579.84`, is retained as evidence and recorded here and in
`governance/evidence/PHQ-2026-02/`, and is supplied to the allocator through
its existing runtime input (`allocate.py --cash`), not persisted in
`holdings.yaml` itself.

## Implemented policy

- **`targets.yaml`**: migrated from the prior five-tier (T1/T2/ETF/band/spec)
  structure to canonical v1.30's flat 37-row `destination:` list. Retired by
  this migration: the tier structure itself, the correlated-cluster
  membership no longer present in the canonical roster (clusters remain
  configured, now binding on only their surviving members), and the T1/T2
  1.5x concentration-ceiling trim rule (`gates.t1t2_trim_mult`) — that rule
  was defined in terms of tiers this migration removes, and no equivalent
  rule is invented in its place (no numeric tolerance-band trim rule is
  specified in any retained PHQ-2026-01 evidence).
- **`gates.yaml`**: the seven gated names (SNPS, ICE, SPGI, WM, RKLB, TSLA,
  SPCX) transcribed verbatim from `Portfolio_HQ_Gated_Name_Disposition_v1_32.csv`.
  A gated name's `targets.yaml` weight is untouched; `allocate.py`'s `plan()`
  simply never proposes a buy for it — its target dollars are never
  redistributed to any other name (verified by regression test:
  `test_canonical_targets_unchanged_by_gates`,
  `test_gating_several_names_does_not_renormalize`). SPCX's existing
  position (0.502727 sh) is held, not exited.
- **`issuer_lookthrough.yaml`**: 8%/40% no-add controls per above.
- SKHY carries no row in `targets.yaml` and no entry in `gates.yaml` —
  reported `UNRESOLVED — PRINCIPAL POLICY DECISION REQUIRED`, counted in book,
  never assigned a buy/trim/exit instruction.

## Rationale

The design note's own recommended shapes (§1's "single-source shape... is
likely preferable," §5's config-table approach as "the smaller, lower-risk
first step" once monitoring becomes mechanical) are exactly what the
principal approved. No new estimate was invented anywhere: canonical
weights, gate criteria, and look-through constituent weights are all
transcribed verbatim from evidence already retained and SHA-256-verified
under `governance/evidence/PHQ-2026-01/`.

## Alternatives Considered

- **Two-document shape** (a second `targets_destination.yaml`, design note
  §1's alternative). Rejected — "targets.yaml remains the canonical
  destination source" reads most literally as targets.yaml's own content
  representing the destination, and a second target file would itself risk
  becoming "a second canonical target table," which this decision's own
  approval text and the implementation task explicitly prohibit.
- **Defer 8%/40% monitoring to manual quarterly review** (design note §5's
  smaller alternative). Rejected — the principal's approval text explicitly
  calls these "no-add controls," which only has mechanical meaning if
  `plan()` itself enforces them.
- **Leave the tiered structure in place and add canonical v1.30 as a
  secondary reference block.** Considered as a smaller, lower-risk diff.
  Rejected after explicit principal direction: a monitored-only reference
  block does not actually make canonical v1.30 the destination that governs
  live buy/hold/gated recommendations, which is what "canonical destination
  source" requires in operative, not just descriptive, terms.

## Consequences

- `targets.yaml`, `holdings.yaml`, `allocate.py`, `levels.py` changed; two
  new config files (`gates.yaml`, `issuer_lookthrough.yaml`) added.
- **Test migration status (corrected after the initial filing).** The three
  pytest files whose fixtures constructed the retired tiered/cluster/
  crypto-sleeve/T1T2 schema and whose tests actually failed in CI
  (`test_allocate_integration.py`, `test_margin.py`, `test_plan_gates.py`)
  have been migrated to the canonical `destination:` schema in this PR.
  Still-governed behavior (gap ordering, trend/earnings gates, cluster-cap
  clip/trim) was migrated in place; tests that exercised retired policy
  (the aggregate crypto sleeve, T1/T2 proximity reporting, the T1/T2 1.5x
  ceiling trim, the band/spec RSI-hot opportunistic trim) were replaced with
  explicit tests proving that policy no longer fires, not carried forward as
  passing tests of dead code paths. The full pytest suite passes with zero
  failures at this PR's final head — see the implementing PR's validation
  section for the exact count. The standalone backtest scripts
  (`backtest_regime.py`/`backtest_rungs.py`/`backtest_trims.py`/
  `backtest_t1t2_trim.py`/`backtest_weights.py`) are not part of the pytest
  suite or CI and remain genuinely out of this PR's scope — they are
  one-time historical-study tools (per CLAUDE.md's Decisions Log, each
  already closed "no re-runs without a new regime in the data") that would
  need their own separate schema-migration effort only if someone chose to
  re-run one, which is not anticipated.
- No trade or order is authorized. No margin increase is authorized. Manual
  Robinhood execution remains controlling.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

`governance/evidence/PHQ-2026-02/` — v1.35 package retained verbatim
(manifest- and SHA-256-verified), machine-readable quantity reconciliation
check, README documenting the complete-list determination and its principal
confirmation.

## Limitations

- The 8%/40% look-through config is a point-in-time snapshot (PHQ-2026-01
  due-diligence date, 2026-07-30) — not live-fetched. Must be refreshed at
  each quarterly review, per `PHQ-2026-01`'s own Limitations section; this
  decision does not change that.
- No live Alpaca credentials were available in the implementing session's
  environment — the authoritative allocation check (`python allocate.py
  --review`) could not be run against live current prices in this session.
  Verified instead via synthetic-price focused tests and the existing full
  suite; a live run with real credentials is required before treating any
  specific dollar recommendation as current.
- The pytest-suite migration is complete as of this PR's final head (see
  Consequences). The standalone backtest scripts noted there remain
  unmigrated, disclosed, and genuinely out of scope.
