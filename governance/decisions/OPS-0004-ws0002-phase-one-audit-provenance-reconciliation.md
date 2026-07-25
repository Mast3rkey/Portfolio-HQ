---
decision_id: OPS-0004
date: 2026-07-25
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, GOV-0002]
supporting_artifact: governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md
---

## Context

`OPS-0002` item 4 required an independent high-capability audit of the WS-0002 planning
baseline before that baseline could be accepted, and named two further checkpoints (after
material architecture implementation; before final end-to-end acceptance) as future
completion conditions. `OPS-0003`'s Context section records, as settled fact, that this
first checkpoint was satisfied: "an independent Fable audit (disposition: REMEDIATION
REQUIRED, no Blocking finding...), a confirming Fable delta re-review against that exact
head, and explicit principal acceptance of both conclusions."

A separate, later reviewing session (`session_01H9bxWHpdadjhooQ4EjYZVk`, distinct from every
session that authored PR #143, PR #144, or OPS-0003) was explicitly authorized by the
principal to independently audit the merged Phase One baseline at `085f5560bc87d98a0a9f3e0bffb99958e401163d`,
read-only. Its output — `governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md`
("WS-0002 Phase One Independent Audit — Fable," Version 1.1) — independently verified the
F1–F4 disposition corrections on the merits and found them genuine, verified PR #143/#144's
diffs matched their authorizations exactly, independently re-executed the full test suite
(1,246 passed, 0 failed) and re-derived the `MARGIN-0005` charter-pinned hashes, and returned
disposition **PASS WITH FINDINGS — no Blocking finding**. Its own Finding FA-1 identified a
provenance gap that this decision exists to close: PR #143 carries zero GitHub reviews and
zero comments (API-verified); the "independent Fable audit" `OPS-0003`'s Context section
describes exists only as prose in the PR body and commit messages of the same committer
identity as the audited work, with no independently retained, attributable artifact behind
it. FA-1 states plainly that nothing it found *contradicts* that claim — the F1–F4
dispositions are real, coherent, and substantively sound — but the closure record could not,
until now, substantiate the audit claim from retained evidence rather than self-reported
narrative.

A separate incidental discrepancy surfaced during this reconciliation's own preflight
verification (distinct from the audit's own findings): a `wc -w` count of the retained
artifact returns 2,216 words, not the 2,267 previously reported in an earlier read-only pass
over the same file. The file's SHA-256 (`7077d5ba59b3f9f2372e321bf2cf3cecde5da40415f7960ae29ba874e5222db8`),
byte size (17,526), and line count (82) all match exactly across both passes — this decision
treats the matching hash as the authoritative identity check for the artifact and records the
word-count discrepancy transparently rather than silently adopting either figure. The
discrepancy does not affect the artifact's content, which is retained verbatim and
independently confirmed byte-identical to the reviewing session's original output.

This decision is the "narrow governance reconciliation filing" FA-1 itself recommends.

## Decision

1. **Audit artifact retained.** `governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md`
   is added to the repository verbatim, byte-identical to the reviewing session's output
   (SHA-256 `7077d5ba59b3f9f2372e321bf2cf3cecde5da40415f7960ae29ba874e5222db8`, confirmed by
   independent `sha256sum` in this reconciliation session both before and after copying it
   into the repository). It is retained as the durable, independently-authored audit record
   for the WS-0002 Phase One planning baseline, evaluated at the merged state `085f556…`,
   per `governance/audits/README.md`'s new convention (also added by this decision).

2. **FA-1's provenance finding is recorded, not disputed and not resolved retroactively.**
   `OPS-0003`'s Context-section claim that an "independent Fable audit" and a "confirming
   Fable delta re-review" occurred against PR #143 is **not** rewritten, disputed, or found
   false by this decision — FA-1 itself found the F1–F4 dispositions genuine and the
   underlying reasoning sound. What this decision records as fact is narrower: that claim's
   *evidentiary provenance* — a standalone, independently attributable artifact — was not
   retained anywhere in the repository or on PR #143 itself, and cannot be reconstructed after
   the fact. This decision does not manufacture that missing retroactive evidence; it cannot.
   What it does instead is supply, from this point forward, an independently-authored artifact
   (item 1) that itself verifies the same dispositions on the merits from a separate session
   with no authorship stake — closing the evidentiary gap prospectively, exactly as FA-1's own
   recommended disposition describes, without claiming to authenticate the original prose
   retroactively.

3. **A narrow, dated factual note is appended to `OPS-0003`** (below, in this same decision's
   Consequences and via a note added directly to the bottom of `OPS-0003-post-acceptance-workstream-priority-transition.md`,
   per `governance/decisions/README.md`'s narrow-correction convention — its substance is not
   otherwise edited) clarifying the provenance gap described in item 2 and pointing readers to
   this decision and the retained artifact for the full reconciliation.

4. **FA-2, FA-3, and FA-4 are recorded, requiring no independent action beyond what is already
   in place.**
   - **FA-2** (PR #143's merged body overstates a since-resolved branch-cleanup item): no
     action — merged PR bodies are frozen history; the live record (PR #144's preflight, and
     the confirmed absence of `docs/ops-0002-unified-core-blueprint` on `origin`) is already
     correct.
   - **FA-3** (the BTC `holdings.yaml`/`targets.yaml`/CLAUDE.md conflict): remains open,
     unresolved, and out of scope for this decision, exactly as it was for `OPS-0002` and
     `OPS-0003`. It continues to require its own separately verified factual-reconciliation
     change before any crypto-sleeve rebuild logic or Standing Queue wording is next touched —
     restated here, not newly imposed.
   - **FA-4** (test-suite re-execution): resolved within the retained artifact itself
     (1,246 passed, 0 failed, independently re-executed) — no further action.

5. **Forward evidentiary rule for the two remaining `OPS-0002` item 4 checkpoints.** Going
   forward, an audit satisfying either of `OPS-0002` item 4's two remaining checkpoints (after
   material architecture implementation; before final end-to-end acceptance) is complete only
   when a retained, independently attributable artifact is filed under `governance/audits/` per
   its README convention — a claim made only in a PR body, commit message, or other unretained
   prose, authored by the same identity as the work under review, does not by itself satisfy
   either checkpoint from this decision forward. This is an evidentiary completion-condition
   addition to `OPS-0002` item 4, not a reopening of item 4's substance or of the checkpoint
   already treated as satisfied under `OPS-0003` (item 2 above).

6. **Scope withheld, restated.** This decision authorizes no WS-0002 architecture
   implementation, no reactivation of WS-0002 beyond its existing `status: complete`
   (planning-and-audit phase only), no change to WS-0001/`MARGIN-0005`'s authority, milestones,
   or sequencing, no action on PR #145 (confirmed still open, draft, unmerged, base `main` at
   `085f556…`, mergeable_state `clean`, untouched by this decision), no allocator/`targets.yaml`/
   `holdings.yaml`/`margin_state.py`/Intelligence/BTC/production-code change, no trade, and no
   order. It does not supersede `OPS-0002` or `OPS-0003`'s substance — only appends the narrow
   factual note described in item 3 and adds the forward-looking evidentiary rule in item 5.

7. **Register updated to reflect this filing.** `operations/WORKSTREAMS.yaml`'s WS-0002 entry's
   `evidence_refs` gains the retained artifact and this decision file. No other field of the
   WS-0002 or WS-0001 entries changes — `status`, `priority`, `authorized_scope`,
   `prohibited_scope`, milestones, `next_action`, `completion_criteria`, and `blocker` are all
   unchanged from `OPS-0003`.

## Rationale

FA-1 is precise about what it can and cannot supply: "This artifact closes that gap
prospectively for this audit; it cannot close it retroactively for the prior one." The correct
response is exactly that narrow — retain the new evidence, record what it can and cannot prove,
and add a forward rule so the same gap cannot recur silently, without overreaching into either
disputing work that independent verification found sound (item 2) or expanding this filing's
authority beyond the evidentiary question FA-1 actually raised (item 6). This mirrors the
discipline `NUM-0001` applied to numeric-parameter provenance: distinguishing a well-founded
claim from an unsubstantiated one is itself valuable even when the claim turns out, on
independent check, to be correct — and the fix is a provenance standard, not a retraction.
Appending a dated note to `OPS-0003` rather than rewriting it follows `governance/decisions/
README.md`'s own convention (the same pattern `OPS-0002` used for its own same-day correction),
preserving the original reasoning while keeping the record accurate for a future reader who
finds `OPS-0003` alone.

## Alternatives Considered

- **Take no action, since FA-1 found no Blocking finding and the underlying dispositions
  genuine.** Rejected — FA-1's own recommended disposition explicitly asks for this narrow
  filing; leaving "independently audited" resting on unretained prose when a documented gap
  exists and a fix is available is the kind of unaddressed finding this repository's governance
  process exists to close, not defer.
- **Rewrite or supersede `OPS-0003`'s Context section outright.** Rejected — `OPS-0003` is
  `status: Accepted`; per `governance/decisions/README.md`, substance is not edited after
  acceptance, and FA-1 does not find the underlying claim false, only its provenance
  unretained. A dated note is the correct, proportionate instrument.
- **Treat this as resolving FA-3 (the BTC conflict) as well, since a reconciliation filing is
  already open.** Rejected — FA-3 requires its own separately verified factual reconciliation
  against live `holdings.yaml`/`targets.yaml` state; bundling it here would exceed this
  decision's narrow evidentiary scope and risks a less careful reconciliation than that open
  item deserves on its own.
- **Reopen `OPS-0002` item 4's already-satisfied first checkpoint and require retroactive
  re-audit-with-artifact.** Rejected — the retained artifact (item 1) itself independently
  verifies that checkpoint's substance on the merits from a separate, non-authoring session;
  demanding a second, formal re-audit of already-independently-reconfirmed work has no
  decision-quality upside and is exactly the kind of disproportionate process the blueprint's
  own efficiency principles (`OPS-0002` item 4's routine-edit exemption; blueprint §7/§8) warn
  against.
- **Apply the forward evidentiary rule (item 5) only to future workstreams, leaving `OPS-0002`
  item 4's two remaining checkpoints unaffected.** Rejected — those two checkpoints are the
  exact future case FA-1's recommendation names ("future audit gates... should require a
  retained, attributable artifact"); leaving them unaffected would repeat the same gap this
  decision exists to close.

## Consequences

Going forward: the WS-0002 Phase One planning-and-audit record now rests on a retained,
independently-authored, byte-verified artifact (`governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md`)
in addition to the narrative already in `OPS-0003` and PR #143/#144 — the evidentiary gap FA-1
identified is closed prospectively, not retroactively erased. `OPS-0003` carries an added
dated factual note (below) but is otherwise unchanged; `OPS-0002` is otherwise unchanged. Any
future audit satisfying one of `OPS-0002` item 4's two remaining checkpoints must file a
retained artifact under `governance/audits/` as part of that checkpoint's completion. No
WS-0002 implementation, no WS-0001/`MARGIN-0005` change, no action on PR #145, and no
allocator/`targets.yaml`/`holdings.yaml`/margin/Intelligence/production-code/trade/order change
results from this decision. This decision, the retained artifact, the `governance/audits/`
README, and the `OPS-0003` note become effective once this exact implementing commit is pushed
to the designated branch and, per the principal's standing instructions for this repository, a
pull request is opened only if and when the principal asks for one.

---

_**2026-07-25 dated note, appended to `OPS-0003-post-acceptance-workstream-priority-transition.md`
by this decision (narrow factual correction, substance otherwise unchanged, per
`governance/decisions/README.md`'s convention):** this decision's Context section describes an
"independent Fable audit" and a "confirming Fable delta re-review" against PR #143. A later,
separately-authorized independent audit (`governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md`,
Finding FA-1) found that claim's evidentiary provenance unretained: PR #143 carries zero GitHub
reviews and zero comments, and the audit narrative exists only as prose in the PR body and
commit messages of the same committer identity as the audited work. FA-1 does not find the
underlying F1–F4 dispositions false — it independently re-verified them as genuine — only that
this Context section's claim could not, until `OPS-0004`, be substantiated from retained,
independently-attributable evidence. See `OPS-0004-ws0002-phase-one-audit-provenance-reconciliation.md`
for the full reconciliation. Nothing else in this decision changes._
