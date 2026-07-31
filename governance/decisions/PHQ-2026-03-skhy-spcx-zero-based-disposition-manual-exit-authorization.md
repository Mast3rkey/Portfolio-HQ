---
decision_id: PHQ-2026-03
date: 2026-07-31
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
---

## Context

`PHQ-2026-02` reconciled `holdings.yaml` from verified post-execution evidence
and recorded, without resolving, two open names: SPCX (`gates.yaml`,
`hold_no_add`, existing 0.502727 sh position held, not exited) and SKHY (no
`targets.yaml` row, no `gates.yaml` entry, reported
`UNRESOLVED — PRINCIPAL POLICY DECISION REQUIRED`). Both remain live holdings
today (see Current State below).

The principal has now reviewed a zero-based disposition recommendation for
both names and given explicit policy approval, quoted verbatim below. This
decision is the repository-native record of that policy approval. It is
**not** an execution record: no trade has occurred, no evidence of a trade
has been supplied, and this filing does not claim otherwise anywhere.

This decision is deliberately narrow, in the same spirit as `PHQ-2026-01`
separating architecture-policy approval from order authorization, and
`PHQ-2026-02` separating actionable-policy implementation from any claim of
executed trades: it records **policy approved now**, distinct from
**positions still currently held**, distinct from **future manual execution
by the principal**, distinct from **a later, separate factual-repository-
synchronization decision after that execution actually happens**.

## Decision

**Accepted, as principal-approved policy, exactly the following, and nothing
beyond it:**

Exact principal approval (2026-07-31):

> "I accept the zero-based SKHY and SPCX disposition recommendation. SKHY and
> SPCX are to receive no canonical target and are authorized for manual exit
> by the principal. Sale proceeds remain cash pending the live Portfolio-HQ
> allocation check. SPCX remains a research candidate only, and SKHY remains
> a watchlist name only. This approval authorizes no automated order, margin
> use, or unrelated target change. Repository holdings and the SPCX gate may
> be changed only after the principal manually executes and supplies
> verified post-trade evidence."

### 1. Current state (unchanged by this decision, verified this session)

- SKHY: 0.278473 sh, present in `holdings.yaml`'s `shares:` block. No row in
  `targets.yaml`. No entry in `gates.yaml`.
- SPCX: 0.502727 sh, present in `holdings.yaml`'s `shares:` block. Carries a
  `target_pct: 0.75` row in `targets.yaml` (annotated "gated hold/no-add —
  see gates.yaml") and a `hold_no_add` entry in `gates.yaml`
  (`holds_existing_shares: true`).
- No execution evidence, sale confirmation, or resulting cash figure for
  either name has been supplied to, or recorded in, this repository. No sale
  of either name is recorded anywhere in this repository.
- This decision does not add, remove, or alter any `holdings.yaml`,
  `targets.yaml`, or `gates.yaml` entry for either name. Both remain held,
  exactly as currently recorded, until later factual synchronization
  (§8 below) occurs from verified post-trade evidence.

### 2. Approved policy

- **SKHY**: receives no canonical `targets.yaml` target (superseding
  `PHQ-2026-02`'s "unresolved, policy decision required" status with an
  actual policy: zero-based, no target). Authorized for manual exit by the
  principal, at the principal's discretion and timing. Until exited, SKHY
  remains a **watchlist name only** — no research, target, or gate
  authority attaches to it beyond that.
- **SPCX**: receives no canonical `targets.yaml` target going forward (this
  decision recommends removing its `target_pct: 0.75` row and its
  `gates.yaml` entry only as part of the future factual-sync unit, §8 below
  — not by this filing). Authorized for manual exit by the principal, at the
  principal's discretion and timing. Until exited, SPCX **remains a research
  candidate only** — its existing `gates.yaml` `hold_no_add` gate remains
  fully binding and is not relaxed, narrowed, or reinterpreted by this
  decision.
- **Sale proceeds** from either name, once and only once a manual exit
  actually occurs, remain in cash pending a live, credentialed
  `python allocate.py --review` run against then-current holdings — no
  redistribution, target reassignment, or reallocation is pre-decided here.

### 3. Execution boundary

- The principal executes any SKHY/SPCX exit manually in Robinhood.
- No order placement, staging, submission, or brokerage-account mutation of
  any kind by software is authorized by this decision. No brokerage account,
  position, or order endpoint may be accessed to prepare, simulate, or
  stage this exit.
- No margin use of any kind is authorized by this decision, for this exit or
  otherwise.

### 4. Repository mutation boundary

- `holdings.yaml` may not be changed to reflect either exit before verified
  post-trade evidence exists. Both positions remain in `holdings.yaml`
  exactly as currently recorded until that evidence is supplied.
- The SPCX `gates.yaml` entry may not be removed or altered before verified
  post-trade evidence exists — it remains fully binding in the interim.
- No target, tier, weight, or unrelated `targets.yaml`/`gates.yaml` entry may
  be changed as a side effect of this decision or its future implementation
  unit. Sale proceeds are not automatically redistributed to any other name.

### 5. Required post-execution evidence

Before any repository mutation reflecting an actual SKHY or SPCX exit, the
following must be supplied and verified, per name as applicable:

- execution date;
- final post-trade quantities for both names (zero, if fully exited);
- transaction confirmation(s) or equivalent verified evidence (the same
  evidentiary bar `PHQ-2026-02` applied to its own v1.35 reconciliation
  package);
- resulting cash balance;
- explicit confirmation that no margin was used in the transaction.

### 6. Required later implementation unit

A **separate, future, factual-synchronization decision and PR** — not this
filing — must:

- update `holdings.yaml` to the actual verified post-trade state for each
  name (a full exit removed per this repository's existing zero-position
  convention, a partial exit reflected at its verified remaining quantity);
- retire the SPCX `gates.yaml` entry and its `targets.yaml` row only if the
  position is actually gone and this decision's authority supports that
  removal — not before, and not speculatively;
- retire or adjust SKHY's status consistent with its actual verified
  post-trade holding;
- preserve any sale proceeds as cash, not pre-assigned to any target;
- run the live `python allocate.py --review` allocation check only after
  both the repository state and market-data prerequisites (live pricing,
  credentials) are satisfied — not as part of this filing, which has neither.

### 7. Reopening conditions

- SKHY may return to `targets.yaml` only through new research and a
  separately approved role and target — this decision's "no canonical
  target" determination is not itself evidence for or against a future
  target; it simply declines to assign one now.
- SPCX may return only after sufficient research, valuation review,
  portfolio-fit analysis, and a separate principal approval — the existing
  `hold_no_add` gate criteria in `gates.yaml` (an accessible investable
  vehicle, reviewed terms, verified financial evidence, liquidity analysis,
  principal approval) are unchanged and remain the operative bar.

### 8. Explicit non-authorizations

This decision authorizes none of the following:

- any automated trade, order, or brokerage mutation of any kind;
- any margin use;
- any unrelated target, tier, weight, cluster-cap, or gate change;
- any dashboard or allocator behavior change;
- any Intelligence-to-policy automation or research-to-target shortcut.

## Rationale

**FACT** — current repository holdings, targets, gate state, and accepted
authority, independently verified this session: SKHY (0.278473 sh) and SPCX
(0.502727 sh) are both present in `holdings.yaml`; SKHY has no
`targets.yaml` row and no `gates.yaml` entry; SPCX has a `target_pct: 0.75`
row and a `hold_no_add` `gates.yaml` entry; `PHQ-2026-01` gated SPCX
(`HOLD TARGET IN CASH`, no directive to sell an existing position) and left
SKHY entirely unaddressed; `PHQ-2026-02` reconciled holdings from the v1.35
evidence package, confirmed both positions as held (not exited) at that
reconciliation, and reported SKHY `UNRESOLVED`. `governance/decisions.yaml`
and the `governance/decisions/` directory each independently reconcile to 50
entries with no orphan and no duplicate `decision_id`, confirming
`PHQ-2026-03` as the next unused identifier in this series, checked live
against both, not assumed.

**INFERENCE** — portfolio overlap, complexity, and next-best-use-of-capital
considerations underlying the "zero-based" characterization of this
recommendation (that neither name currently justifies continued portfolio
complexity relative to the canonical v1.30 architecture's other 37 rows) are
the principal's own basis for the disposition recommendation this decision
records. This repository does not independently re-derive that judgment —
it is recorded here as the stated basis for the approval, not re-litigated
or second-guessed by this filing.

**JUDGMENT** — assigning no canonical target and authorizing manual exit for
both names is the principal's explicit judgment call, exercised through the
verbatim approval above. This decision does not substitute any different
judgment for it, and does not extend it beyond its own stated terms (no
canonical target, manual exit authorized, proceeds to cash, SPCX remains
research-candidate-only, SKHY remains watchlist-only).

**UNCERTAINTY** — future execution price, the resulting cash figure, and the
live allocation-check output that will follow a real exit are all
necessarily unknown at filing time and are not estimated, projected, or
implied anywhere in this decision. `PHQ-2026-02`'s own Limitations section
already discloses that no live Alpaca credentials have been available in any
session to date for a credentialed `--review` run — that constraint is
unchanged here and directly bears on when the future implementation unit
(§8 above) can actually be completed.

No new company-specific or security-specific fact about SKHY or SPCX is
asserted by this decision beyond what is already directly inspected in this
repository's own retained evidence (`holdings.yaml`, `targets.yaml`,
`gates.yaml`, `PHQ-2026-01`, `PHQ-2026-02`, and their retained evidence under
`governance/evidence/`) — no chat summary or external claim is treated as
primary evidence for any changeable fact here.

## Alternatives Considered

- **Fold this policy into `PHQ-2026-02` as a correction.** Rejected —
  `governance/decisions/README.md` prohibits editing a file's substance
  after `status: Accepted`; `PHQ-2026-02` is already Accepted and its own
  SKHY/SPCX determinations (SPCX gated hold/no-add, SKHY unresolved) were
  correct as of its own filing date. A new, separate decision is the correct
  mechanism for a new principal policy input, not a rewrite of settled
  reasoning.
- **Immediately update `holdings.yaml`/`gates.yaml`/`targets.yaml` now, on
  the theory that the disposition is effectively decided.** Rejected — the
  principal's own approval text explicitly reserves repository mutation for
  after manual execution and verified post-trade evidence; mutating now
  would assert a sale that has not happened, exactly the failure mode
  `PHQ-2026-01`/`PHQ-2026-02` already took care to avoid for their own
  execution boundaries.
- **Treat "authorized for manual exit" as authorization to prepare or stage
  an order (e.g., a lot-aware transition packet, per `PHQ-2026-01`'s
  precedent for its own broader transition).** Rejected — the principal's
  approval text here draws a narrower line than `PHQ-2026-01`'s: "no
  automated order... this approval authorizes no... unrelated target
  change," with no parallel "packet preparation" clause. This decision does
  not read one in.
- **Leave SPCX's existing `hold_no_add` gate and target row untouched
  indefinitely, pending exit, with no forward-looking record of the
  approved zero-target policy.** Rejected — the principal's approval is a
  real policy decision (no canonical target, research-candidate-only) that
  the repository should record now, distinct from the mechanical file
  changes that must wait for verified evidence; recording the policy now and
  deferring only the mechanical sync is what this decision actually does.
- **Create a new `operations/WORKSTREAMS.yaml` entry for this disposition.**
  Considered, following the `WS-0006`/`WS-0008` precedent of a workstream
  entry per PHQ-decision. Adopted in a separate, minimal register entry
  (below) — not because convenience favors it, but because this decision
  itself creates a concrete, named future implementation unit (§8) with
  its own governing authority and prohibited scope, which is exactly what
  `OPS-0001`'s register exists to track across the session boundary between
  this filing and whenever the principal actually executes.

## Consequences

- `governance/decisions/PHQ-2026-03-skhy-spcx-zero-based-disposition-manual-exit-authorization.md`
  (this file), `governance/decisions.yaml` (one new entry), `CLAUDE.md` (one
  concise Decisions Log pointer), and `operations/WORKSTREAMS.yaml` (one new
  entry, `WS-0009`, tracking the future factual-sync unit) are the only
  files this decision changes.
- `holdings.yaml`, `targets.yaml`, and `gates.yaml` are **unchanged** by this
  decision — independently confirmed byte-identical against origin/main in
  this PR's validation.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed by this decision.
- SKHY and SPCX remain held, exactly as currently recorded, until a separate
  future factual-synchronization decision and PR records a verified,
  principal-supplied post-trade state for either name.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

The principal's verbatim approval text (quoted in full above) is this
decision's only supporting record — no external evidence package accompanies
this filing, unlike `PHQ-2026-01`/`PHQ-2026-02`'s retained due-diligence and
reconciliation bundles. Current repository state supporting this decision's
Current State section is directly inspected and cited in place
(`holdings.yaml`, `targets.yaml` line 64, `gates.yaml`), not attached as a
separate artifact.

## Limitations

- This decision records policy only. It creates no evidence of, and does not
  imply, any executed trade for either name.
- The future factual-synchronization unit (§8) cannot be completed without
  principal-supplied, verified post-trade evidence — none exists at filing
  time, and none is estimated or approximated here.
- The live `python allocate.py --review` allocation check referenced in the
  principal's approval requires Alpaca credentials that have not been
  available in any session to date (`PHQ-2026-02`'s own disclosed
  limitation, unchanged) — this decision does not resolve that constraint
  and does not attempt to run that check.
- SKHY's and SPCX's reopening conditions (§7) are stated at the level the
  principal's approval and this repository's existing gate criteria support;
  neither name's specific future research bar is expanded or narrowed beyond
  what is already recorded.
