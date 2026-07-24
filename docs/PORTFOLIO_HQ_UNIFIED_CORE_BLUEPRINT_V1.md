# Portfolio-HQ Unified-Core Blueprint — Version 1

**Status:** Draft planning baseline for WS-0002, filed under
`governance/decisions/OPS-0002-unified-core-planning-and-audit-gate.md`.
**Not yet audited.** Pending an independent, high-capability audit (currently
intended to be performed by Fable) against the exact commit that introduces
this document, before this planning package may be accepted or any WS-0002
implementation is authorized.
**Authority level:** Level 8 (generated/derivative synthesis) under the
`GOV-0002` operational-precedence hierarchy — non-authoritative. This
document cannot override the Constitution, an accepted governance decision,
`targets.yaml`, `holdings.yaml`, or production code/tests. Where anything
below conflicts with a higher-authority source, the higher source controls
and this document is wrong until corrected.
**Supersession:** future revisions require their own version (V2, V3, …) or
an explicit superseding decision — this file is not silently edited after
acceptance, per the same discipline `governance/decisions/README.md` applies
to accepted decision records.
**Base commit verified at authoring time:** `69723a69bb863cc792ac3f09818be64fe628ffd4`.

---

## 1. Purpose and scope

This document converts a completed read-only Sonnet planning review into a
durable, repository-native architecture and sequencing baseline for WS-0002
(“Unified Portfolio-HQ core architecture and optimization audit”). It is a
**planning artifact, not an implementation**. Nothing in this document
changes `holdings.yaml`, `targets.yaml`, `allocate.py`, `margin_state.py`,
the Constitution, any accepted governance decision, any Intelligence record
or schema, or any MARGIN-0005 research file. Recording this blueprint
authorizes its own review and independent audit — it does not authorize
building any of the architecture it describes.

## 2. Relationship to the prior Sonnet planning review

A prior read-only planning session produced a comprehensive system map,
gap register, and phased roadmap. That report is source material for this
blueprint, not an authority this document defers to uncritically — every
material fact below was independently reverified against the live repository
at the commit stated above before being restated here. Three corrections
were made to the prior report's framing, at the principal's explicit
direction:

1. **Intelligence is not "no demonstrated value" merely because it has zero
   allocator coupling.** The prior report's anti-complexity audit filed
   Company/Theme Intelligence under "optional convenience / no demonstrated
   value yet" on the strength of its coupling-free architecture alone. That
   was a category error: the coupling-free boundary is a **required design
   property** (§20 of `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, incorporated
   into the Constitution), not evidence of low value. §5 below restates
   Intelligence's evaluation criteria correctly — thesis understanding, risk
   and thesis-break recognition, evidence freshness, comparative business
   quality, opportunity-cost judgment, and human decision quality — and
   further expansion is a pace/evidence/workload question, never a
   "why bother, it doesn't move the allocator" question.
2. **Opportunity cost is not something to invent a new engine for.** The
   prior report correctly rejected a new scoring/conviction/ranking system,
   but this blueprint states the reasoning more precisely in §6: the
   allocator's existing largest-dollar-gap-first rule already *is* the
   governed opportunity-cost mechanism; the advisory layer's job is to add
   context to that number, never to compute a second one.
3. **Priority sequencing is now explicit, not inferred.** The prior report
   left WS-0001 and WS-0002 as non-competing lanes without a principal
   decision forcing a choice. The principal has now explicitly reprioritized
   planning as primary (§9, and `operations/WORKSTREAMS.yaml`) — this
   blueprint and its governing decision record that choice precisely,
   including what does and does not change for WS-0001 as a result.

Everything else material in the prior report — the system map, the
authority hierarchy, the gap register, the MARGIN-0005 gate-state findings,
the Intelligence coverage/coupling findings, the branch-hygiene findings —
was reverified at this session's base commit and found unchanged (see §3).

## 3. Verified repository facts (reverified this session)

- `origin/main` and local HEAD both equal `69723a69bb863cc792ac3f09818be64fe628ffd4`; working tree clean at authoring time.
- Zero open pull requests at authoring time.
- `governance/decisions.yaml` carries 26 accepted decisions, `OPS-0001` the most recent, none superseded.
- `operations/WORKSTREAMS.yaml` carries exactly four workstreams (WS-0001–WS-0004), consistent with `OPS-0001`.
- MARGIN-0005 (WS-0001): G0/G1 closed and merged (PRs #137, #138); G2A/G2B merged (PRs #139, #140); **gate G2 itself is not yet formally closed** — the protocol's literal G2 text requires T-D1–T-D5 and T-U1/T-U2 proofs, which `G1_DATA_VALIDATION_REPORT.md` itself states "remain G2 work and are not claimed." One of the ≤3 authorized S2 implementation PRs remains. `research/margin_target_study/trial_ledger.jsonl` and `candidate_freeze.yaml` are both confirmed absent — zero of the 300 registered trials consumed — reverified directly this session.
- Company/Theme Intelligence: 7 of 65 roster tickers covered (COST, GEV, ISRG, NVDA, TMO, TSM, XOM); coverage is opt-in by design and absence is not an error. Zero import coupling in either direction between `intelligence_validator.py`/`intelligence_report.py`/`freshness_*.py` and `allocate.py`/`margin_state.py` — reverified directly this session via source grep, confirmed empty both directions.
- `docs/INVESTMENT_ONTOLOGY.md` (ONTO-0001) has zero code references anywhere in `allocate.py`, `margin_state.py`, or `intelligence_validator.py` — reverified directly this session, confirmed empty.
- **Factual conflict on record, not corrected here:** `holdings.yaml`'s `crypto_shares` block contains a live `BTC: 0.00460473` entry, while `CLAUDE.md`'s Standing Queue and `targets.yaml`'s own comment both state BTC has no `crypto_shares` entry ("fully sold 2026-07-13"). This blueprint records the conflict; it does not resolve it. Per this session's explicit authorization boundary, `CLAUDE.md` and `targets.yaml` are not touched here. Resolving this requires its own separately verified factual reconciliation (confirming whether a BTC rebuild buy has actually executed) before the next relevant allocation workflow change touches either file.
- Full test suite status at this commit: reverified as part of this session's validation pass (§ Validation, reported in the governing decision and the PR description) — no production file is touched by this change, so no test-suite behavior change is possible or claimed.

## 4. Three-layer architecture

The smallest coherent architecture that lets Portfolio-HQ reach a governed
allocation conclusion is three layers, cleanly separated by authority, not
by file location:

### Layer 1 — Authoritative deterministic allocation core

**Owns:** current holdings and available capital (`holdings.yaml`,
`resolve_holdings()`); targets and tier policy (`targets.yaml`); market data
(Alpaca prices, RSI/regime/earnings via `indicators.py`/`regime_gate.py`/
`earnings.py`); the allocator itself (`allocate.py`); hard margin and
concentration constraints (`margin_capacity()`, cluster caps, the T1/T2
ceiling, the buffer floor, the leverage cap); the reproducible numeric
recommendation and its log (`logs/allocation-*.md`, `performance_log.csv`).

**Property:** fully deterministic given its inputs. Every hard constraint in
this system already lives here and stays here. This layer is complete today
— no gap was found in it during this or the prior review.

### Layer 2 — Advisory decision-context layer

**Owns:** Company and Theme Intelligence (`intelligence/`); research
evidence (MARGIN-0005 and the closed Phase 3–7A backtests); freshness and
staleness signals (`freshness_*.py`, `intelligence_report.py`); uncertainty
and thesis-break conditions; overlap and opportunity-cost *context* (as
distinct from the opportunity-cost *rule*, which lives in Layer 1 — see §6);
evidence gaps and conflicts (including the BTC conflict recorded in §3).

**Property:** may annotate, explain, compare, or warn. **May not** change a
target, tier, weight, gap, buy, trim, margin figure, or any allocator output
— this boundary is a required system property, verified this session to be
currently unbroken in both directions (§3), and must remain unbroken by
construction, not by convention alone.

### Layer 3 — Human decision and manual-execution layer

**Owns:** the principal's review of the governed recommendation and any
advisory context; the principal's discretion to decline a recommendation or
use less capital than the recommendation allows (never more, never bypassing
a hard constraint); manual execution on Robinhood; post-trade sync of fills,
share counts, and margin state back into `holdings.yaml`.

**Property:** the only layer where a trade is ever actually placed. No code
path anywhere in this repository places an order — confirmed unchanged.

### Prohibited coupling (by construction)

- Layer 2 → Layer 1 in any form that changes a number: **prohibited**, no
  exception path.
- A new scoring engine, computed conviction score, theme ranking, or opaque
  aggregation that feeds Layer 1: **prohibited** — this would recreate
  exactly the "opportunity map" / "standing predictive layer" Constitution
  §4 excludes.
- Any future Layer 2 → Layer 1 integration must be **display-only** (an
  annotation appended to an existing recommendation line, e.g. "(Company
  Intelligence: High conviction, reviewed 2026-XX-XX)"), and must itself be
  separately researched, justified, tested, and approved — the same bar
  every existing gate in `allocate.py` was held to (`PORTFOLIO_INTELLIGENCE_SPEC.md`
  §20, Constitution-incorporated).
- Governance is consulted at proposal/commit time (a decision precedes and
  is cited by the commit that changes `targets.yaml`/`allocate.py`), never
  at run time — there is no runtime governance lookup anywhere in this
  system, and none should be added.

## 5. Intelligence's evaluated contribution (corrected framing)

Company and Theme Intelligence should be assessed on its own terms, not on
whether it moves the allocator — moving the allocator is exactly what it is
designed never to do. Its demonstrated and expected contributions are:

- **Thesis understanding** — a durable, human-authored record of why a
  position is held, reviewed on a cadence, rather than reconstructed from
  memory each time.
- **Risk and thesis-break recognition** — explicit `risks[]`/catalyst
  tracking per company, so a change in the underlying business case is
  noticed rather than silently absorbed into a price move.
- **Evidence freshness** — the staleness-reporting mechanism (`PI-0011`)
  surfaces when a record's evidence has gone stale relative to its own
  review cadence.
- **Comparative business quality** — the PI-0016 standing review
  methodology's capital-priority comparator sets (e.g. NVDA vs. TSM/ASML/
  AVGO/MSFT) give the principal a structured, repeatable way to compare
  names within a cluster or tier.
- **Opportunity-cost judgment** — not a computed number, but qualitative
  context: which of several eligible uses of capital has a fresher, higher-
  conviction thesis behind it right now.
- **Human decision quality** — the actual, intended consumer of all of the
  above is the principal reading it before executing a recommendation, not
  any piece of code.

**Consequence for pacing, not value:** further Intelligence expansion (a new
company or theme record, activating freshness monitoring) may still be
paused, deferred, or prioritized selectively — but only on evidence of
workload, actual review value, or opportunity cost of the reviewing time
itself, exactly the standard `PI-0016` already applies per company. It is
not paused because the layer "doesn't count" — it does count, on its own
axis, and this blueprint records that explicitly so a future session does
not repeat the prior report's category error.

## 6. Opportunity-cost doctrine

- The allocator's existing **largest-dollar-gap-first** rule, applied across
  every eligible sleeve (T1/T2/ETF/band/spec/crypto) simultaneously, **is**
  the governed, mechanical, policy-driven capital-priority rule. It must
  remain deterministic and config-driven exactly as it is today.
- The advisory layer (Layer 2) may present, alongside a recommendation: the
  next-best eligible uses of capital by gap size; business-quality
  differences already captured in Intelligence records; open risks,
  uncertainties, or thesis-break flags; and freshness/staleness of the
  evidence behind a name.
- The advisory layer **cannot** recalculate, re-rank, or override the
  allocator's gap-based ordering — doing so, even implicitly (e.g. a
  "suggested reorder" derived from conviction ratings), would be exactly the
  computed-conviction/opportunity-map system Constitution §4 and this
  blueprint's §4 both exclude.

## 7. End-to-end allocation-check acceptance milestone (terminal, not yet reached)

This is the future acceptance milestone WS-0003 records as its terminal
item, and the point at which WS-0002's architecture work is judged
"complete, current, integrated, tested, and operating as designed."

**The milestone must answer, honestly and reproducibly:**

> Given current governed policy, portfolio state, risk constraints, and
> available evidence, what is the best governed use of available capital
> now, what are the next-best alternatives, and what uncertainty could
> change that conclusion?

**Required inputs, all freshness-checked and explicitly flagged if stale:**
current holdings and available capital (Layer 1); live prices and pricing
freshness (regular-session-only limitation surfaced, not silently ignored);
governed targets and tier policy; margin debt, leverage ratio, and
maintenance/buffer state; concentration, cluster, and T1/T2-ceiling
proximity; the allocator's deterministic recommendation; relevant advisory
Intelligence and research context for any flagged name (Layer 2, display-only);
explicit uncertainty and degraded-data handling (stale margin sync, a
`earnings:unavailable` flag, a session-hours pricing gap, an overdue
Intelligence review) — each must produce a visible flag, never a silent
best-effort guess.

**Reproducibility:** identical inputs must produce an identical
recommendation and an identical log entry, exactly as today.

**Abstention:** where a required input is missing or too stale to trust
(e.g. margin not synced recently enough for a margin-funded buy), the
milestone's output must say so plainly and recommend inaction or a sync
step — never proceed on a guess.

**User-facing output:** one concise, action-first table, consistent with
CLAUDE.md's existing Formatting doctrine — not a new dashboard, not a second
rendering surface.

**What must remain manual, always:** order placement and fill confirmation
on Robinhood, and the post-trade sync back into `holdings.yaml`. This
milestone never promises certainty or automated trading, and no version of
it ever will under this architecture.

**Not yet reached.** Nothing in this document or its governing decision
authorizes building toward it — this section defines the target so that
future, separately authorized implementation phases have a fixed
destination to build toward and be judged against.

## 8. Efficiency and return-contribution operating principles

- Use the largest safe, coherent unit of work that can be fully reviewed and
  validated in one pass — this blueprint itself is sized that way, covering
  the full planning package in one PR rather than fragmenting it across
  several.
- Avoid unnecessary prompt/session/PR fragmentation. Not every field change,
  finding, or clarification needs its own PR — bundle what belongs together,
  split only when independent review genuinely benefits from it.
- Preserve separate authorization, independent review, and post-merge
  validation exactly where they materially reduce risk (a margin-funded
  decision, a research-adoption decision, an architecture-implementation
  decision) — and nowhere else.
- Every material phase in the roadmap this blueprint supports must have a
  credible, statable benefit to sustainable risk-adjusted returns, capital
  protection, decision quality, reliability, or usability. A phase without
  one of these does not get built.
- Reject work whose complexity, delay, maintenance cost, or review burden
  exceeds its expected value. This is not a new rule — it restates the
  standard this repository already applies to every closed backtest and
  every declined "standing analysis layer" proposal in CLAUDE.md's Decisions
  Log.
- More files, more governance decisions, more tests, or more architecture
  are not themselves progress. The correct measure is whether a change
  demonstrably improves a real decision the principal will actually make.

## 9. Priority and sequencing (recorded here, authorized in OPS-0002)

The principal has explicitly made full planning, architecture, scope,
sequencing, and independent audit the immediate priority. Concretely:

- **WS-0002** (this workstream) becomes `priority: primary`, `status:
  review` — authorized for planning-package review, independent audit, and
  finding reconciliation only. No implementation authority is granted.
- **WS-0001** (MARGIN-0005) remains `status: in_progress`, becomes
  `priority: secondary`, and keeps every existing element of its research
  authority, milestones, completion criteria, and its exact S2/G2
  `next_action` text unchanged. A principal sequencing hold is recorded: the
  final authorized S2 implementation PR is held pending the WS-0002
  planning package's completion and its first independent audit, unless the
  principal separately authorizes proceeding sooner. **MARGIN-0005 is not
  cancelled, not blocked by any technical defect, and not complete** — it is
  sequenced behind the planning/audit phase by explicit principal choice,
  recorded exactly as such in `operations/WORKSTREAMS.yaml`.
- Only one workstream carries `priority: primary` at a time, per `OPS-0001`'s
  own rule — verified true after this change.

## 10. Independent audit-gate plan (model-neutral)

Portfolio-HQ's review practice for architecture-level work: Sonnet performs
the detailed groundwork (this document and its governing decision); an
independent, high-capability audit — currently intended to be performed by
Fable, but named generically here so the practice survives a future model
change — reviews a coherent, completed package, read-only and findings-only;
findings are reconciled (accepted, corrected, or explicitly declined with
stated reasoning) before anything proceeds; only approved corrections are
implemented; and this gate is not repeated for routine or mechanical work.

**Gate 1 (this package):** required now, against the exact commit that
introduces this blueprint and `OPS-0002`, before this planning package may
be accepted or any WS-0002 implementation begins.

**Gate 2 (future, conditional):** after material architecture is actually
implemented per this blueprint (e.g. the consolidated read-only status
layer described in the prior Sonnet report's roadmap), before it becomes the
default daily workflow.

**Gate 3 (future, conditional):** before the end-to-end allocation-check
milestone (§7) is formally accepted.

**Not required for:** routine edits, mechanical register field updates
(e.g. a `last_verified_main_sha` refresh), small bug fixes, or ordinary
test-only corrections. Requiring an audit for these would be exactly the
"repeated ceremonial review" this practice is designed to avoid.

## 11. Explicitly not created by this blueprint or its governing decision

To keep this package narrow and proportionate to demonstrated need:

- No separate branch-cleanup workstream (a one-off git hygiene action, not
  a standing concern).
- No standalone "Fable audit" workstream (modeled as milestones under
  WS-0002 instead, §10).
- No standalone "end-to-end allocation check" workstream (modeled as
  WS-0003's terminal milestone instead, §7).
- No standalone SHA-refresh PR (folded into this session's verified-fact
  update to `operations/WORKSTREAMS.yaml`).
- No Intelligence-expansion workstream or authorization (§5 restates why
  expansion is a pace/evidence question, not something this document
  greenlights).
- No new scoring, ranking, or conviction system of any kind (§4, §6).

## 12. Authority statement

This document is a non-authoritative synthesis (GOV-0002 level 8). It
carries no authority beyond what `governance/decisions/OPS-0002-unified-core-planning-and-audit-gate.md`
grants it: recording a planning baseline for review and independent audit.
It does not amend the Constitution, `docs/MARGIN_DOCTRINE.md`,
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, any accepted governance decision,
`targets.yaml`, or `holdings.yaml`. Any future revision to the architecture
described here requires either a new, explicitly superseding version of
this document or a new governance decision that supersedes `OPS-0002` —
never a silent edit to this file after it is accepted.
