---
decision_id: PHQ-2026-07
date: 2026-08-03
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04, PHQ-2026-05, PHQ-2026-06]
supporting_artifact: governance/evidence/PHQ-2026-07/MANIFEST.json
---

## Context

Earlier in this session, a live `python allocate.py --cash 1041.23` check
(the repository's then-current synced cash, per `PHQ-2026-06`) recommended
two buys — AVGO ($40) and ETN ($34) — against the reconciled book. The
principal then supplied two new Robinhood screenshots (Investing home tab;
Buying power detail screen) showing cash of **$1,279.23**, a ~$238 increase
over the prior synced figure with no explanation on the screen alone for
what changed.

Rather than infer a cause, the session asked the principal directly (two
targeted questions) whether the AVGO/ETN buys had executed and whether
margin debt had changed. The principal confirmed: **neither buy executed —
the change is a new deposit only** — and **margin debt is still $0.00,
unchanged since 2026-07-31**. The arithmetic confirms the deposit amount
exactly: $1,041.23 + $238.00 = $1,279.23, matching the new screenshot to
the penny.

The buying-power detail screen also differs from prior evidence in this
repository: it shows margin buffer only as a qualitative status ("Ready to
use"), not the numeric percentage this repository's margin-sync convention
is built around (`holdings.yaml`'s own comment; `allocate.py`'s
`write_state()`). No numeric buffer % is available from this evidence.

## Decision

**Bounded to exactly the cash fact below — nothing else:**

1. Records the new, retained-screenshot-supported cash figure:
   **$1,279.23**, evidence date 2026-08-03.
2. Makes **no** change to any `shares:` or `crypto_shares:` quantity in
   `holdings.yaml` — the principal explicitly confirmed the prior
   allocation check's recommended AVGO/ETN buys did not execute, so no
   position change is evidenced.
3. Makes **no** change to `holdings.yaml`'s `margin:` block — the principal
   explicitly confirmed margin debt is still $0.00, unchanged since the
   2026-07-31 sync. `margin.buffer_pct` (currently `100.0`, a zero-margin
   placeholder, not a Robinhood-displayed screen) is also left unchanged —
   this evidence shows only a qualitative "Ready to use" status, not a
   numeric buffer %, so there is nothing to sync into that field.
4. Makes **no** change to `targets.yaml`, `gates.yaml`, or
   `issuer_lookthrough.yaml`.
5. Records `buying_power` ($7,920.11) and `margin_total_available`
   ($6,641.06) as evidence-only context, explicitly **not** cash and **not**
   deployment authority of any kind.
6. `holdings.yaml` has no persisted cash schema field (unchanged since
   `PHQ-2026-02`) — this decision updates only `holdings.yaml`'s
   explanatory comment/header, recording the new figure as evidence to be
   supplied through `allocate.py`'s existing `--cash` runtime input at the
   next allocation-check run.
7. Retains both supporting screenshots verbatim, hashed, under
   `governance/evidence/PHQ-2026-07/`.
8. Authorizes a fresh, live `python allocate.py --cash 1279.23` run against
   the unchanged share/margin state as this session's own next action —
   the prior $1,041.23-based check is superseded by this new cash figure,
   not re-used.

## Rationale

**FACT** — both retained screenshots' displayed cash ($1,279.23), buying
power ($7,920.11), margin total available ($6,641.06), and pending orders
(-$0.18) were read directly from the two image files this session copied
and hashed from real, filesystem-accessible upload paths (SHA-256
`3724e4d2b3d1a20047dca3837cf78535667b911801c4d173de1b0b5263737d84` and
`8f5f264f979bea803686505be80239fafb21cec8d4cc5c3e2fb7540563a4bc0f`) — no
transcript-extraction workaround was needed this time, unlike `PHQ-2026-06`.

**INFERENCE** — none required for the cash figure itself, which is read
directly off the retained images and reconciles exactly against the prior
figure plus a confirmed deposit amount.

**JUDGMENT** — this session declined to assume that AVGO/ETN had filled
just because cash moved by roughly the right order of magnitude, and
declined to assume margin was unchanged just because the qualitative
"Ready to use" status reads positively. Per this repository's standing
"never hallucinate... verify before acting" guardrail, both facts were
obtained by asking the principal directly (`AskUserQuestion`) rather than
inferred from ambiguous evidence, following the same discipline
`PHQ-2026-05`/`PHQ-2026-06` applied to their own open discrepancies.

**UNCERTAINTY** — none disclosed as unresolved in this filing (contrast
`PHQ-2026-06`'s disclosed $0.18 gap). The deposit arithmetic reconciles
exactly, and both open questions (buy execution, margin debt) were closed
by explicit principal confirmation rather than left open.

## Alternatives Considered

- **Assume the AVGO/ETN buys filled and treat the remaining ~$238 as the
  deposit.** Rejected — this would have silently changed two `shares:`
  quantities in `holdings.yaml` on an inference alone, contrary to this
  repository's verification guardrail; the principal's direct answer
  confirmed this assumption would have been wrong.
- **Derive a numeric margin buffer % from the qualitative "Ready to use"
  status or from `margin_total_available`.** Rejected — `holdings.yaml`'s
  own comment and `allocate.py`'s `write_state()` explicitly require
  Robinhood's own *displayed* buffer %, not a derived value; deriving one
  here would repeat a mistake this repository has already documented as
  unreliable (CLAUDE.md's margin doctrine note: a simple subtraction
  "doesn't reconcile" against Robinhood's real formula).
- **Treat this screenshot pair as a full holdings reconciliation.**
  Rejected — neither screen shows a per-ticker share list; this remains a
  cash-only synchronization, consistent with `PHQ-2026-04`'s/`PHQ-2026-06`'s
  precedent for aggregate-only evidence.

## Consequences

- `holdings.yaml`'s explanatory comment/header is updated to record the new
  cash figure and evidence date — no `shares:`, `crypto_shares:`, or
  `margin:` data field is changed. `governance/decisions/PHQ-2026-07-cash-synchronization-238-deposit.md`
  (this file), `governance/decisions.yaml` (one new entry),
  `governance/evidence/PHQ-2026-07/` (both screenshots retained verbatim
  plus `MANIFEST.json` and `README.md`), `operations/WORKSTREAMS.yaml`
  (`WS-0009`'s stale cash-figure pointer updated to this decision), and
  `CLAUDE.md` (one concise Decisions Log pointer) are the only other files
  this decision changes.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed by this decision itself.
- A fresh, live allocation check using this new cash figure is this
  session's own next, separate action — not part of this decision's file
  changes.
- No allocator behavior, tier, target, cluster, cap, gate, or
  `issuer_lookthrough.yaml` weight is changed.
- Per this repository's Lean Delivery and Review Lifecycle (`OPS-0009`),
  this filing is classified **Lane M** (mechanical/factual synchronization)
  — it records an already-true, screenshot-evidenced cash figure, confirmed
  by direct principal answers on the two points a screenshot alone could
  not resolve, and introduces no new tier/target/cluster/cap/gate/allocator
  authority.

## Evidence

`governance/evidence/PHQ-2026-07/` — this decision's own retained evidence:

- `robinhood_investing_home_20260803.png` — Investing tab home screen.
  SHA-256 `3724e4d2b3d1a20047dca3837cf78535667b911801c4d173de1b0b5263737d84`,
  741690 bytes, `image/png`.
- `robinhood_buying_power_detail_20260803.png` — Buying power detail
  screen. SHA-256
  `8f5f264f979bea803686505be80239fafb21cec8d4cc5c3e2fb7540563a4bc0f`,
  358939 bytes, `image/png`.
- `MANIFEST.json` — full displayed-figure record and provenance.
- `README.md` — evidence-directory summary.

## Limitations

- No numeric margin buffer % was available from this evidence (the
  buying-power screen shows only a qualitative "Ready to use" status) —
  `holdings.yaml`'s `margin.buffer_pct` remains the pre-existing `100.0`
  zero-margin placeholder, not a Robinhood-displayed screen. A real
  numeric buffer % should still be synced before any future margin-funded
  decision.
- This screenshot pair supports a cash-only synchronization. It does not
  support, and this decision does not attempt, a full share-by-share
  holdings reconciliation.
