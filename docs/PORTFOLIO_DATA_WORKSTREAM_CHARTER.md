# Portfolio Data Integrity Workstream — Charter

> **Planning document. No code written, no production file touched.** This charter defines what this new workstream is and is not, before any implementation begins — the same "define the boundary, then work inside it" discipline that governed every phase of the margin research program (`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`).

_Written 2026-07-17. Sources reviewed: `CLAUDE.md` (in full — Identity & Role, Portfolio Doctrine, Workflow, Decisions Log, Guardrails), `docs/PHASE5B_GOVERNANCE_DECISION.md`, `docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`, and `allocate.py`/`targets.yaml`/`holdings.yaml` read directly to confirm the allocator's actual current responsibilities (§2 below)._

---

## 1. Relationship to the completed margin research

The Phase 3–7A margin research program (`docs/PHASE7_RESEARCH_PROGRAM_CLOSURE.md`) is closed and is not reopened by this charter or by anything in this new workstream. That program's one open item (historical data collection infrastructure) is a margin-specific logging gap, distinct from this workstream's scope, and remains tracked in `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`, not here. If this workstream's own work ever touches margin-adjacent data (e.g., `holdings.yaml`'s margin block), it does so only as a factual-input concern (is the synced debt/buffer accurate and current), never as a re-opening of any margin *research* question.

## 2. Current allocator's responsibilities and boundaries

Confirmed by direct reading of `allocate.py`/`targets.yaml`/`holdings.yaml`/`CLAUDE.md`, not assumed:

**What the allocator (`allocate.py`) does:**
- Computes gross/net-equity book value from `holdings.yaml`'s `shares:`/`crypto_shares:`/manual-value entries, live-repriced via Alpaca on every run (`resolve_holdings()`).
- Computes each roster ticker's tier target in dollars from `targets.yaml`'s `tiers:`/`crypto:` weight percentages applied against the current book (`build_roster()`, `plan()`).
- Ranks dollar gaps (target minus current position value) largest-first and fills them from available cash/margin, gated in a fixed order: 200-SMA trend → 7-day earnings blackout → correlated-cluster caps (`caps.clusters` in `targets.yaml`) → band cap (1.25× target) → spec fixed-at-target (`plan()`).
- Applies mechanical, no-RSI-gated trims for cluster-cap and T1/T2-concentration-ceiling breaches, and opportunistic RSI-gated trims for band/spec overweight.
- Computes and displays margin capacity against the 1.8x leverage cap and 30% buffer floor (`margin_capacity()`), using the buffer % synced from Robinhood's own displayed value, never derived.
- Presents a recommendation table (`render()`); places no orders.
- Provides sync commands (`update_holdings`, `update_shares`, `update_crypto_shares`, `update_margin`) that update `holdings.yaml` from data the user supplies.

**What the allocator explicitly does not do, per `CLAUDE.md`'s standing rules:**
- Never places an order — order-placement code is deliberately absent from `alpaca_client.py`.
- Never performs predictive research, sets a price target, or produces an "opportunity map" — `CLAUDE.md`'s Guardrails section states this explicitly; every opportunity is computed at runtime, on deposit day, from the current gap between actual and target weight, never from a forecast.
- Never scores, ranks, or weights a ticker by conviction, thesis, or attractiveness — every ticker's target weight is a fixed, config-editable percentage set in `targets.yaml` by the account holder, not computed by the tool from any analytical judgment.
- Never treats a rising margin buffer as a timing signal, and never runs a margin-timing model — margin capacity is a fixed structural ceiling, not a discretionary lever (`CLAUDE.md`'s Portfolio Doctrine section, and the entire Phase 3–7A research program's own governing constraint).

**The allocator's decision logic is therefore entirely mechanical**, in the specific sense this charter cares about: every buy/trim decision follows deterministically from (a) config values in `targets.yaml` that the account holder sets directly, and (b) computed facts (current prices, current holdings, current gaps, current gate states) — never from a value this tool itself judges, predicts, or scores.

## 3. Mission

**Objective: Improve the factual inputs consumed by the existing allocation engine without creating any new investment decision-maker.**

This workstream exists to make the allocator's *inputs* more accurate, complete, and timely — never to add a new layer that decides, ranks, scores, or recommends anything the allocator's existing mechanical rules don't already determine.

## 4. Scope

In scope, as a general category: any change that improves the accuracy, completeness, timeliness, or reliability of a *fact* the allocator already consumes or needs to consume correctly, where the allocator's own decision rules (tier weights, gates, caps, trim thresholds) are unchanged by the improvement.

## 5. Explicit non-goals

This workstream does **not**:
- Build a conviction score, attractiveness rating, or any per-ticker judgment metric.
- Build an investment thesis system, company dossier, or qualitative research repository intended to influence allocation.
- Build a predictive model, price target, or forward-looking "opportunity" ranking of any kind.
- Change any tier weight, cap, gate, or trim rule in `targets.yaml`'s policy — those remain the account holder's direct, manual configuration choices, per `CLAUDE.md`'s "CONFIG-EDITABLE" framing.
- Reopen the band-overlay backtest's already-closed verdict (227% vs. 422% buy-and-hold, NO-GO on automated/analytical trading layers) or any other closed backtest in `CLAUDE.md`'s Decisions Log.
- Reopen any Phase 3–7A margin research conclusion.

## 6. The governing test

Every proposed task in this workstream, before any implementation begins, must be run through one question:

> **Does this improve the accuracy of an existing input, or does it introduce a new judgment?**

- **Improves an input** (more accurate ticker metadata, more complete universe coverage, more reliable price/earnings/margin data, better data-source redundancy, operational tooling around the allocator) → **potentially in scope.**
- **Introduces a judgment** (any score, conviction level, attractiveness ranking, thesis weighting, prediction, or recommendation not already produced by the allocator's existing fixed rules) → **out of scope**, and requires its own separate governance review with the same evidentiary bar as any other doctrine change — it is not "just another feature."

## 7. Allowed work (examples, not a commitment to build any of them)

- Auditing `targets.yaml`'s roster for completeness/accuracy against each ticker's actual current tier-appropriate classification (a factual correction, not a re-scoring — c.f. the AAPL band→T2 and AVGO-stays-T2 tier-fit scan already performed and recorded in `CLAUDE.md`'s Decisions Log, which this workstream would extend in kind, not in method).
- Improving `earnings.py`'s data reliability (the `finance.yahoo.com` network-policy gap already identified and left open in `CLAUDE.md`'s Guardrails section).
- Improving `holdings.yaml`/`margin_state.py` sync accuracy, timeliness, or automation (without changing what either represents).
- Building the historical margin/cashflow logging infrastructure named in `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`'s one open item, if and when that work is separately picked up (margin-specific, tracked there, not owned by this workstream, but consistent with this workstream's input-fidelity spirit if it is ever folded in).
- Operational tooling: better error handling for data-feed failures, clearer sync-state diagnostics, automated staleness checks on `holdings.yaml`.

## 8. Disallowed work (examples)

- A "which of these 65 tickers looks most attractive right now" ranking of any kind.
- A qualitative or quantitative thesis document per ticker intended to feed sizing or selection decisions.
- Any model that outputs a number this project would then use to override, supplement, or justify deviating from `targets.yaml`'s fixed tier weights.
- Any feature that reads as "the tool now tells you what to buy based on its own analysis" rather than "the tool now has more accurate facts to compute an already-fixed rule against."

## 9. Success criteria

- Every task undertaken under this charter can be described, without qualification, as "the allocator's output is unchanged in *kind*, only in *accuracy*" — i.e., re-running `allocate.py` unchanged, with only the improved input in place, produces the same category of recommendation table it always has, just computed from better facts.
- No task under this charter ever requires a materiality-threshold backtest of the kind Phase 3–7A required, because no task under this charter changes a decision rule — it only changes a fact the existing rule consumes. (A task that *would* require such a backtest is, by definition, out of scope per §6.)
- Every task's completion is verifiable by comparing the allocator's decision logic before and after: identical logic, different (better) inputs.

## 10. Assumption registry

| # | Assumption | Label | Basis |
|---|---|---|---|
| 1 | The allocator's current decision rules (tier weights, gates, caps, trims) are fixed and not open for revision by this workstream | **Known** | `targets.yaml`'s own "CONFIG-EDITABLE" framing places rule changes in the account holder's direct hands, not this workstream's; confirmed by direct read of `allocate.py`'s `plan()` |
| 2 | "Predictive research, price targets, opportunity maps" are prohibited tool behavior | **Known** | `CLAUDE.md` Guardrails section, stated directly |
| 3 | Any new judgment/scoring/ranking layer would need to overcome the band-overlay backtest's NO-GO verdict | **Known** | `CLAUDE.md` Decisions Log, June 2026 entry, stated directly |
| 4 | The margin research program's open item (data collection infrastructure) is margin-specific and separate from this workstream's scope | **Known** | `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`'s final status table, item 5 |
| 5 | "Improving an input" and "introducing a judgment" are the correct, sufficient dividing line for every future task in this workstream | **Hypothetical** — a governance design choice adopted for this charter, not itself derived from a backtest; if a future proposal's category is genuinely ambiguous, that ambiguity itself is a reason to pause and seek explicit clarification before proceeding, not a reason to default to "in scope" |

## 11. Decision boundaries

- **No code is written under this charter alone.** This document authorizes nothing beyond its own existence.
- **No production file (`allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, `CLAUDE.md`) is modified by this charter.**
- **Any task classified "in scope" under §6 still requires its own separate implementation approval** before code is written — this charter establishes the filter, not a standing authorization to build anything that passes it.
- **Any task whose classification under §6 is contested or unclear is treated as out of scope by default** until explicitly resolved — the burden of proof is on demonstrating a proposed task is input-improvement, not on demonstrating it might be a judgment layer.
- **No backlog is created by this charter.** Per explicit instruction, backlog creation is a separate, later step.

---

## What this document deliberately does not do

- Does not write any code or modify any production file.
- Does not create a backlog of candidate tasks.
- Does not authorize any specific future task, even one that would clearly pass the §6 test.
- Does not reopen the margin research program or any of its conclusions.
- Does not propose or endorse any scoring, ranking, thesis, or predictive system.

Stopping here. Awaiting direction on the next step (inventorying the allocator's current inputs, per the suggested sequence).
