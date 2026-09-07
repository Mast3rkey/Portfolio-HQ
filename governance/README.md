# Governance

This directory is the decision-record layer of Portfolio-HQ's documentation architecture, adopted 2026-07-18 (`governance/decisions/GOV-0001-governance-architecture-adopted.md`). It sits between the Constitution and Portfolio Policy in the decision flow:

```
constitution/INVESTMENT_CONSTITUTION.md   (why — rarely amended)
        │
        ▼
governance/decisions/                     (what was decided, and why — this layer)
        │
        ▼
intelligence/companies/, intelligence/themes/   (how it applies to one name/theme)
        │
        ▼
CLAUDE.md Portfolio Doctrine / Guardrails (the standing rule)
        │
        ▼
targets.yaml                              (config, encoded)
        │
        ▼
allocate.py                               (execution)
```

## What's here

- **`decisions/`** — one file per decision (ADR-style), append-only. See `decisions/README.md` for the convention.
- **`decisions.yaml`** — a generated index of `decisions/*.md` frontmatter, for quick lookup. Never hand-edited; regenerate by re-reading the ADR files' frontmatter when a new one is added.
- **`templates/`** — authoring scaffolding, currently just the decision-record template.

## What's deliberately not here

- **Company and theme intelligence** (`intelligence/companies/`, `intelligence/themes/`) is unchanged and stays exactly where it is. This governance layer records *decisions about the system*; it does not duplicate or relocate per-company thesis content, which already has its own frozen spec (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`) and its own decision series (`PI-####` in `decision_log.yaml`).
- **Historical decisions are not backfilled here.** `decision_log.yaml` (repo root) remains the historical record for the `MARGIN-####` and `PI-####` series exactly as it stands — untouched by this governance layer's creation. New decisions from this point forward, in any domain, get a file under `decisions/`; existing ones are not retroactively migrated. See `decisions/README.md` for why.
- **No investment methodology, scoring system, or capital-allocation philosophy.** This layer is documentation governance only — see `constitution/INVESTMENT_CONSTITUTION.md` for the boundary this repository already draws around "no new analysis/research/thesis systems."

## Enforcement of "every `targets.yaml` change has a documented decision"

Convention only, by default: a commit that touches `targets.yaml` should cite the relevant decision ID in its commit message. No script or CI gate enforces this yet — escalate to one only if drift is actually observed (same evidence-before-tooling standard this repo applies everywhere else).
