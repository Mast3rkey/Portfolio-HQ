# Retained Audit Artifacts

Independent audit reports retained verbatim, for permanent reference by the governance
decisions that rely on them. Established by `governance/decisions/OPS-0004-ws0002-phase-one-audit-provenance-reconciliation.md`,
which found that an "independently audited" claim resting solely on PR-body/commit-message
prose (no retained review, comment, or standalone artifact) cannot be verified after the
fact — a repository-wide search finds only the claim itself, authored by the same identity
as the work it describes.

## Convention

- One file per audit, named `<WORKSTREAM>_<SCOPE>_<REVIEWER>_AUDIT_<YYYYMMDD>.md`, copied in
  verbatim from the reviewing session's output — never edited after retention. A reviewer's
  own in-document revision (e.g. a dated "Version 1.1" amendment) is part of the artifact,
  not a repository edit.
- Referenced by the governance decision(s) that rely on it via `supporting_artifact` in that
  decision's frontmatter, and by SHA-256 in the decision's own text where identity matters.
- Any future audit gate that a governance decision names as a completion condition (e.g.
  `OPS-0002` item 4's two remaining checkpoints) is satisfied only by a retained, attributable
  artifact filed here — narrative-only claims in a PR body or commit message no longer suffice
  as of `OPS-0004`.
