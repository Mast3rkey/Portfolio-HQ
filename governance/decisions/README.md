# Decision Records

One file per decision, append-only, ADR-style. Adopted as part of the governance architecture (`GOV-0001-governance-architecture-adopted.md`, this directory).

## Convention

- **Filename**: `<ID>-<kebab-slug>.md`, e.g. `GOV-0002-example-decision.md`.
- **ID prefixes**: `PI-####` and `MARGIN-####` continue to exist as historical series in `decision_log.yaml` (repo root) — they are not migrated here and not reused for new decisions of a different kind. `GOV-####` is used for decisions about this documentation/governance architecture itself, starting with `GOV-0001`. A new prefix is chosen only when a genuinely new decision domain needs one — not pre-declared in advance.
- **Same-date ordering**: when decision records share the same calendar date — whether within `governance/decisions/`, within `decision_log.yaml`, or across both — repository history may be used to establish filing order; the date field alone does not encode intra-day sequence.
- **Never edit a file's substance after `status: Accepted`.** Correct with a dated note appended to the same file for narrow factual corrections (the pattern this repo already used for the Phase 2 margin docs' "STATUS CORRECTION" banners), or supersede it with a new decision file that sets `status: Superseded` on the old one and links back via `related_decisions`. Never silently rewrite the original reasoning.
- **Template**: `governance/templates/decision_template.md`.
- **Status vocabulary is intentionally distinct from `decision_log.yaml`'s** (`Proposed | Accepted | Superseded | Archived` here vs. `pending_evidence | active | accepted` there) — `governance/decisions/` is authoritative for every decision from GOV-0001 forward, while `decision_log.yaml` remains the unchanged historical ledger for everything decided before it.

## Why no historical backfill

`decision_log.yaml`'s existing 12 entries (`MARGIN-0001` through `MARGIN-0003`, `PI-0001` through `PI-0009`) are not converted into files here. Reformatting already-settled decisions into a new structure is mechanical work with no decision-quality upside, and `decision_log.yaml` continues to serve its stated purpose — a queryable structured record for the margin and Portfolio Intelligence domains specifically. If a future need justifies migrating them (e.g., extending `governance/decisions.yaml`'s generation to cover the full historical set), that migration is its own decision, not an assumed default.

## `governance/decisions.yaml`

A generated index of every file in this directory's frontmatter (`decision_id`, `date`, `status`, `category`, `related_decisions`, `supporting_artifact`). Regenerate it — by hand or script — whenever a decision file is added; it is never the primary record, the `.md` files are.
