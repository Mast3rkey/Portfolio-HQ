---
decision_id: PHQ-2026-01
date: 2026-07-30
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, TGT-0001, TGT-0002, MARGIN-0004, MARGIN-0005]
supporting_artifact: governance/evidence/PHQ-2026-01/final_due_diligence/Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json
---

## Context

The principal ran an out-of-repository research process ("Portfolio-HQ committee
session," standalone backtest application `Portfolio_HQ_v1_10_8_repayment_band_backtest_app`,
entirely separate from this repository's own `allocate.py`/`margin_state.py`
engine and its own `research/margin_target_study/` charter) culminating in a
final due-diligence bundle (v1.32) and a bounded unlevered-validation batch
(v1.31.4a). That work produced: a 37-row candidate destination architecture
("canonical v1.30," `Portfolio_HQ_Grand_Master_Architecture_v1_30.csv`), a
narrower "actionable core" transition architecture that holds seven
individually-gated allocations in cash pending further evidence, an 8-case
unlevered backtest comparing both architectures under quarterly/monthly/buy-and-hold
rebalancing and two cash-yield assumptions, an ETF look-through concentration
audit, and a settled finding on margin repayment-band research. None of this
work, nor any of its outputs, previously existed anywhere in this repository,
in any open PR, or in this repository's GitHub history — it was transferred in
as `Portfolio_HQ_PHQ_2026_01_Repository_Sync_Package_v1_0.zip` (SHA-256
`9595bf1af0013770e89fc691bf226d42520b6e134cee7d90a144b1f330216e55`, verified;
see `governance/evidence/PHQ-2026-01/README.md` for the full verification
chain). The principal reviewed that due-diligence package and gave explicit
approval, quoted verbatim below, in the Portfolio-HQ committee session on
2026-07-30. This decision is the repository-native record of that approval —
it is not itself the research, and it does not perform any research.

This is a materially different kind of decision than this repository's other
portfolio-construction filings (`TGT-0001`, `TGT-0002`): those govern
individual future tier/roster changes to the live `targets.yaml`. PHQ-2026-01
approves an entire candidate destination architecture and transition posture
**in principle**, sourced from outside this repository, while explicitly
deferring every actual `targets.yaml`/`holdings.yaml`/allocator change to a
separate future implementation workstream. It is also distinct from `WS-0005`
(`OPS-0006`'s zero-based Portfolio Intelligence / tier-architecture review,
still in progress inside this repository, at Milestone 3): WS-0005 and the
PHQ committee process are two independent tracks that happened to run over the
same period, using different tooling and different evidence. This decision
does not merge, supersede, or accelerate WS-0005 in any way.

## Decision

**Accepted, as principal-approved policy, exactly the following, and nothing
beyond it:**

Exact principal approval (2026-07-30):

> "I approve Principal Resolution PHQ-2026-01 exactly as written. I authorize
> preparation of the lot-aware transition packet, but no trades are authorized
> until I separately approve the final manual order list."

Approved policy scope (12 points, verbatim from the principal approval
record retained at `governance/evidence/PHQ-2026-01/authority/PHQ-2026-01_PRINCIPAL_APPROVAL.txt`):

1. Canonical v1.30 (`Portfolio_HQ_Grand_Master_Architecture_v1_30.csv`, 37
   rows, SHA-256 `09c7d45f2a6fe0820177dde3eb05c22798f5c62443f7df39f42ae479ce7e07d1`)
   is the approved long-term destination architecture.
2. The actionable core — canonical v1.30 with the seven gated allocations'
   target capital held as cash — is the approved current transition
   architecture.
3. SNPS, ICE, SPGI, WM, RKLB, TSLA, and SPCX remain gated; their target
   capital remains cash until each is individually cleared (see
   `governance/evidence/PHQ-2026-01/final_due_diligence/Portfolio_HQ_Gated_Name_Disposition_v1_32.csv`
   for the per-name reason and next gate).
4. Quarterly review with tolerance bands is approved.
5. Monthly forced rebalancing is rejected.
6. No new margin is authorized.
7. Deposits and approved sale proceeds repay inherited debit first.
8. Effective single-issuer exposure may not exceed 8%.
9. AI/platform common-driver exposure may not exceed 40%.
10. Execution remains manual in Robinhood.
11. Research, Intelligence, reports, backtests, or software may not
    automatically change targets or policy.
12. Exact trades remain separately controlled — no order quantity, tax-lot
    selection, or execution instruction is approved by this decision.

**Explicitly stated by this decision, not left implicit:**

- Architecture *policy* is approved. This decision does not itself implement
  the targets — `targets.yaml` is unchanged by this PR and remains the sole
  authoritative live target file, still reflecting its own currently accepted
  configuration.
- This decision does not synchronize current holdings. `holdings.yaml` is
  unchanged by this PR.
- Allocator implementation (translating the approved architecture into
  `targets.yaml`, gating logic, cash/reserve handling, and exposure-ceiling
  monitoring) requires a separate future design/review/implementation
  workstream and its own PR — see
  `docs/PHQ-2026-01_TARGET_ALLOCATOR_IMPLEMENTATION_DESIGN_NOTE.md`, authored
  alongside this decision but authorizing no implementation itself.
- Gated-name activation (SNPS, ICE, SPGI, WM, RKLB, TSLA, SPCX) requires its
  own separate accepted evidence and principal approval per name, per the
  gate criteria already recorded in
  `Portfolio_HQ_Gated_Name_Disposition_v1_32.csv`.
- No order placement or automatic execution is authorized by this decision.
  The principal's own approval text draws this line explicitly: architecture
  approval is granted; preparation of a lot-aware transition packet is
  authorized; the final manual order list itself requires a separate future
  principal approval.

## Rationale

The due-diligence package closes architecture-level diligence on the
candidate destination and transition architectures through a defined,
auditable process: a 7-decision register (DD-001 through DD-007, retained at
`governance/evidence/PHQ-2026-01/final_due_diligence/Portfolio_HQ_Final_Decision_Register_v1_32.csv`),
an 8-case unlevered backtest matrix (all 8 cases `PASS`, common window
2024-08-26 to 2026-07-28, ≈23 months, retained at
`governance/evidence/PHQ-2026-01/unlevered_validation/unlevered_matrix_results.csv`),
an ETF look-through concentration audit against both approved ceilings, and 12
cited primary/secondary sources for the seven gated names' current business
state. The source application's own test suite passed (42/42,
`pytest_full_suite.txt`) and its engine files were confirmed byte-identical
before and after the validation run (`source_hashes_before_after.json`,
`unchanged: true`) — the validation run did not silently modify the tool that
produced it.

**Margin finding.** The package's `settled_margin_finding` states: "Higher
repayment bands and longer payoff capacities did not establish a durable
risk-adjusted advantage. Current authority remains no new margin." This is
consistent with, and does not reopen, this repository's own existing margin
research closure (`MARGIN-0004`) or its own separate, still-open,
pre-registered conditional-margin research charter (`MARGIN-0005`/`GOV-0003`)
— the PHQ committee process's finding is independent evidence reaching the
same "no new margin" conclusion this repository's live doctrine already
holds; it does not supply or substitute for `MARGIN-0005`'s own pending
results, and does not close or amend that charter.

**Concentration ceilings.** The look-through audit
(`Portfolio_HQ_Look_Through_Exposure_v1_32.csv`, summarized in
`Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json`'s
`lookthrough_summary`) found the highest effective single-issuer exposure is
NVDA at 7.149% (under the approved 8% ceiling), and effective AI/platform
common-driver exposure at approximately 40.03% — **at, and marginally over,
the 40% ceiling as measured, not cleanly under it.** The due-diligence
package's own conclusion states this requires monitoring rather than
asserting clean compliance, and this decision records that finding exactly as
measured rather than rounding it into apparent compliance. This is a policy
input for the future implementation workstream (see Limitations below), not
a defect resolved by this decision.

## Alternatives Considered

- **Wait for `WS-0005` (this repository's own zero-based tier-architecture
  review) to reach its Milestone 8 policy-recommendation package before
  recording any new destination-architecture decision.** Rejected by the
  principal's own action: the PHQ committee process is a separate,
  already-completed track with its own due diligence, and nothing in
  `OPS-0006` or `WS-0005` requires all portfolio-architecture questions to
  route through that one workstream. The two tracks remain independent and
  this decision does not fold one into the other.
- **Treat the approved architecture as immediately implemented in
  `targets.yaml`.** Rejected — the principal's own approval text explicitly
  separates architecture approval from order authorization ("no trades are
  authorized until I separately approve the final manual order list"), and
  DD-007 in the package's own decision register is `BLOCKED` ("Execution
  authorization remains withheld... tax-lot, valuation, and wash-sale
  evidence incomplete"). Implementing targets now would exceed the scope the
  principal actually approved.
- **Silently resolve the 40%-AI/platform-ceiling near-miss by rounding or
  omission.** Rejected — Constitution §6 ("verify before acting on external
  review") and this repository's own "honesty over comfort" formatting rule
  require reporting the measured 40.03% as measured.
- **File this as a `TGT-####` decision.** Considered, since
  `portfolio_construction_governance` is an existing category shared with
  `TGT-0001`/`TGT-0002`. Rejected on identity grounds, not subject-matter
  grounds: `TGT-####` decisions execute or govern individual live
  `targets.yaml` changes; this decision approves an external, multi-part,
  principal-named resolution ("PHQ-2026-01") that explicitly does not touch
  `targets.yaml`. The category is shared; the decision-id series is new
  because a genuinely new decision domain — principal resolutions from the
  external PHQ committee process — now exists, consistent with
  `governance/decisions/README.md`'s "a new prefix is chosen only when a
  genuinely new decision domain needs one."

## Consequences

- Architecture *policy* is approved, exactly as stated above.
- Current holdings are **not** synchronized by this record. `holdings.yaml`
  remains at its last sync (`2026-07-22`) and reflects neither the frozen
  v1.31 snapshot (`account_equity: 6162.95`, `margin_used: 963.16`,
  `2026-07-30 15:32 ET`) nor any subsequent Robinhood order activity.
- `targets.yaml` and allocator behavior still require a separate
  design/review/implementation workstream and PR before this approved
  architecture has any live effect. See
  `docs/PHQ-2026-01_TARGET_ALLOCATOR_IMPLEMENTATION_DESIGN_NOTE.md`.
- Intelligence remains advisory; nothing in this decision changes that.
- Gated-name activation (SNPS, ICE, SPGI, WM, RKLB, TSLA, SPCX) requires
  separate accepted evidence and principal approval, per name.
- No order placement or automatic execution is authorized by this decision.
- SPCX is recorded here exactly as the package disposes it: `HOLD TARGET IN
  CASH` (gated, no investable vehicle). Nothing in this decision or its
  evidence directs selling an existing SPCX position.
- SKHY is not addressed by this decision and remains unresolved per
  `CLAUDE.md`'s Open Items — it is not silently brought under PHQ-2026-01.
- `operations/WORKSTREAMS.yaml` records this decision's evidence
  synchronization as `WS-0006`, `status: in_progress`, `priority: secondary`
  — it does not create authority beyond what this record states, and does
  not authorize the next implementation milestone.

## Evidence

All retained verbatim under `governance/evidence/PHQ-2026-01/` — see that
directory's own `README.md` for the full file-by-file index, SHA-256 values,
and provenance chain:

- `final_due_diligence/Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.html`
  and `.json` — the final due-diligence report (human- and machine-readable)
- `final_due_diligence/Portfolio_HQ_Final_Decision_Register_v1_32.csv` — the
  DD-001..DD-007 decision register
- `final_due_diligence/Portfolio_HQ_Look_Through_Exposure_v1_32.csv` — the
  ETF look-through concentration audit
- `final_due_diligence/Portfolio_HQ_Gated_Name_Disposition_v1_32.csv` — the
  seven gated names' per-name reason, next gate, and cited evidence
- `final_due_diligence/Portfolio_HQ_Final_Due_Diligence_Manifest_v1_32.json`
  — the source bundle's own file manifest
- `unlevered_validation/Portfolio_HQ_Master_Research_Log_v1_31_4a_20260730_175519.html`
  and `master_research_report.json` — the master research log/report behind
  the unlevered matrix
- `unlevered_validation/unlevered_matrix_results.csv` — the 8-case result
  matrix
- `unlevered_validation/pytest_full_suite.txt`,
  `source_hashes_before_after.json`, `test_portfolios.json`, `api_health.json`,
  `SHA256SUMS.txt` — the source application's own test/integrity evidence for
  the validation run
- `authority/PHQ-2026-01_PRINCIPAL_APPROVAL.txt`,
  `authority/LIVE_STATE_BOUNDARY.md` — the exact principal approval and the
  post-snapshot live-state warning

## Limitations

- The unlevered backtest's common window is approximately 23 months
  (2024-08-26 to 2026-07-28) and carries look-ahead and survivorship
  limitations, per the package's own disclosed `residual_risks`.
- Current valuations remain a separate execution gate — this decision
  approves architecture, not a purchase price or timing.
- ETF look-through composition (SPY/VEA/VWO holdings) changes over time and
  must be refreshed at each quarterly review; the 8%/40% ceiling figures in
  this record are point-in-time as of the underlying due-diligence date.
- The measured AI/platform common-driver exposure (≈40.03%) is marginally
  over the approved 40% ceiling as measured, not cleanly under it — recorded
  as a monitoring item for the future implementation workstream, not resolved
  here.
- Lot-level tax and wash-sale analysis was waived for this simplified
  transition-architecture process; DD-007 in the source decision register
  remains `BLOCKED` for exactly that reason. A lot-aware transition packet is
  a distinct future work product this decision authorizes *preparing*, not
  *approving* — per the principal's own approval text.
- Current live holdings have changed after partial Robinhood order execution
  (some orders entered after the frozen snapshot filled, others were queued)
  and must be resynchronized later from principal-supplied evidence, not from
  any artifact retained under this decision.
- The two upstream source archives referenced by this evidence
  (`Portfolio_HQ_v1_32_Final_Due_Diligence_Bundle.zip`,
  `Portfolio_HQ_Unlevered_Batch_v1_31_4a_20260730_175519.zip`) were never
  present in this repository's environment — their recorded SHA-256 values
  are asserted by the transfer package's own manifest, not independently
  re-derived here. See `governance/evidence/PHQ-2026-01/README.md`'s
  provenance-chain section.
- `pytest_full_suite.txt`'s 42 passed tests belong to the separate, external
  `Portfolio_HQ_v1_10_8_repayment_band_backtest_app`, not to this
  repository's own test suite. This decision does not claim anything about
  this repository's own tests, which are validated separately (see the PR
  this decision is filed alongside).
