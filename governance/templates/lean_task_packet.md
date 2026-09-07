---
# Lean task packet — Portfolio-HQ, per OPS-0009 (Lean Delivery and Review Lifecycle v1)
# One packet per lifecycle step. Fill every section; write "N/A — <why>" rather than deleting one.
---

## Role

Exactly one of: `author` | `independent reviewer` | `principal / merge coordinator` | `evidence-recovery
session` (per OPS-0008 §2). State which — role-bounded mechanical actions (OPS-0009 §8) depend on it.

## Repository and workstream/decision

- Repository:
- Decision(s) this packet operates under (e.g. `OPS-0009`, `PI-####`, `OPS-####`):
- Workstream, if any (e.g. `WS-0005`), or `none — cross-cutting`:
- Lane (OPS-0009 §1): `G` — governance authorization | `R` — research/Intelligence content |
  `M` — mechanical/factual sync | `C` — bounded correction

## Verified SHAs

- Starting local `HEAD`:
- `origin/<base-branch>` at packet creation:
- Exact head this packet's work targets or reviews (if different from the above):
- Confirmation these were independently checked this session, not assumed:

## Objective

One or two sentences: what this step accomplishes, in this role, on this lane.

## Allowed and prohibited scope

- Allowed files/actions (exact list — no "and related files"):
- Explicitly prohibited (tier/target/holdings/margin/allocator/production-code changes; any file not
  named above; anything reserved to a different role per OPS-0009 §8):

## Evidence identity

- Frozen evidence bundle(s) consumed, if any, and their retained path:
- SHA-256 recomputed and matched? (OPS-0009 §4 — yes/no, value)
- If full count-level re-verification was performed instead of SHA-only reuse, state which of the
  three OPS-0009 §4 exceptions applied (hash mismatch / no retained validation / documented integrity
  concern):

## Required checks

- Validators/tests in scope for this lane's changed files (OPS-0009 §5 — name them; do not list the
  full unrelated suite unless this change actually touches that domain):
- Exact-head CI reliance: run ID / status, or "pending at push":
- Protected-path / scope-diff check performed: yes/no:
- `git diff --check`: pass/fail:

## Completion boundary

- What marks this packet's step SESSION DONE (OPS-0009 §7) — the exact next-role hand-off point:
- What would instead require KEEP (same session continues) or START NEW (a different session must
  act) — name the condition:

## Final-report fields

On completion, produce `governance/templates/lean_final_report.md` with: starting/final SHA, exact
changed files, authority and scope result, evidence identity where relevant, tests and validators,
protected-path result, PR/merge result, unresolved findings, readiness or completion status.
