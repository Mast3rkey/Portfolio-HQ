---
decision_id: GOV-0001
date: 2026-07-18
status: Accepted
category: architecture_governance
related_decisions: [PI-0001, MARGIN-0003]
supporting_artifact: null
---

## Context

A repository-wide documentation review (this session) found real, demonstrated drift: four Phase 2 margin-design docs contradicted live code for a period before a 2026-07-18 correction pass (`decision_log.yaml` MARGIN-0003); `decision_log.yaml` reads as the authoritative structured decision ledger but by its own header only covers the margin and Portfolio Intelligence domains, leaving ~30 other CLAUDE.md Decisions Log entries (rung/regime/trend/weight/trim backtests, cluster-cap additions, tier-fit scans) with no structured counterpart; and margin doctrine's constitutional content (`docs/MARGIN_DOCTRINE.md`) sat outside any formal constitution despite self-describing as one. Separately, `docs/` had accumulated 62 files, roughly 35 of which are a closed margin-research program (Phase 2 through Phase 7A) whose own closure document states it produced exactly one decision ("maintain current doctrine") and zero production changes.

A parallel proposal ("Project B" — economic-systems reorganization, capital-type taxonomy, company scorecards) was raised in the same conversation and explicitly separated out and excluded from this decision's scope at the requester's direction; it runs into this system's existing no-predictive-research and no-new-analysis-layer guardrails and is not addressed here.

## Decision

Adopts a four-layer documentation architecture: **Constitution** (`constitution/INVESTMENT_CONSTITUTION.md`, immutable philosophy, rarely amended), **Governance decisions** (`governance/decisions/`, one file per decision going forward, ADR-style), **Company/Theme Intelligence** (`intelligence/`, unchanged), and **Portfolio Policy** (CLAUDE.md, unchanged in content, narrows over time as new entries become pointers). `targets.yaml`/`allocate.py` remain the executable floor, unchanged, per PI-0001's existing precedent that Knowledge and Policy never write to Implementation directly.

Scope actually implemented under this decision: `constitution/INVESTMENT_CONSTITUTION.md` (new); `governance/README.md`, `governance/decisions/README.md`, `governance/templates/decision_template.md`, `governance/decisions.yaml` (new); this file. One pointer note added to CLAUDE.md's Identity & Role section; one header comment added to `decision_log.yaml`. No existing file was moved, merged, or deleted.

## Rationale

Single-source-of-truth discipline: each concept (constitution, decision record, company thesis, policy, config) gets exactly one authoritative home, everything else references rather than duplicates. This generalizes PI-0001's already-adopted rule (Intelligence layer cannot write to `targets.yaml`/`allocate.py`) to the whole pipeline, rather than inventing a new principle. Proportionality: this is a solo operator's tool, not a multi-person institution — no committee-meeting ceremony, no template files that would restate schema already owned by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and risk drifting from it.

## Alternatives Considered

- **Merge `docs/MARGIN_DOCTRINE.md` into the constitution wholesale**, per the original proposal. Rejected during implementation: `margin_state.py` (live production code) references this file by path in three places, `allocate.py` and `margin_simulation.py` reference it once each, and five other `docs/` files cite it directly. Moving or deleting it would strand those references for no single-source-of-truth gain worth the risk to production code accuracy. The constitution references it instead (Principle 3); the file itself stays exactly where it is.
- **Archive the closed Phase 2–7A margin research program into `docs/archive/` now**, per the original proposal's highest-priority cleanup item. Deferred, not rejected: the same reference-scan found these docs cross-referenced from four live `.py` files' comments/docstrings (`margin_state.py`, `allocate.py`, `margin_simulation.py`, `test_margin_state.py`) and roughly a dozen other `docs/` files reference each other and `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md` (itself cited from the protected `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, which this decision does not touch). A correct move requires updating every one of those paths, not just `git mv`-ing the files — a larger, separate, careful pass, not a minimum-viable governance layer. Left as the top item in this session's remaining recommendations.
- **Backfill `decision_log.yaml`'s 12 existing entries into `governance/decisions/`.** Rejected as low-value mechanical work with no decision-quality upside — see `governance/decisions/README.md`.
- **Create `company_review_template.md` and `theme_review_template.md` under `governance/templates/`**, per the original proposal's folder tree. Not created: their schemas are already governed by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and enforced by `intelligence_validator.py`, and a parallel template would restate that schema in a second, unenforced place with nothing keeping the two in sync — exactly the documentation-drift risk this governance layer exists to prevent, not a gap in it.
- **Fold Project B (economic systems, capital types, company scorecards) into this architecture.** Out of scope by explicit instruction; separately, it runs into this system's existing no-predictive-research and no-new-analysis-layer guardrails and the closed AMZN/AVGO tier decisions, and was not evaluated here.

## Consequences

Going forward, a new decision in any domain gets a file under `governance/decisions/`; CLAUDE.md's Decisions Log entries for genuinely new decisions become short pointers to those files rather than full prose (existing ~30 entries are unchanged). `decision_log.yaml` stays exactly as it is — the historical record for the `MARGIN-####`/`PI-####` series, not superseded or replaced. The `docs/` archive reorganization, and the eventual retirement of `docs/MARGIN_DOCTRINE.md` as a standalone file in favor of full constitution merge, remain open, explicitly out-of-scope-for-now items — not silently abandoned, not assumed done.
