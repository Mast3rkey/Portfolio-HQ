---
decision_id: TIER-0005
date: 2026-08-05
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0004, PI-0016, PI-0038, PI-0039, TIER-0001, TIER-0002, TIER-0003, TIER-0004, REL-0001, REL-0007, CHART-0001, CHART-0002]
supporting_artifact: null
file: governance/decisions/TIER-0005-ws0005-milestone6-fresh-authorization.md
---

## Context

### Authority for this unit

`PI-0038`'s pre-Milestone-6 roadmap (`operations/WORKSTREAMS.yaml`, `WS-0005`) records six ordered
prerequisites required before a fresh Milestone 6 (blind classification) implementation may be
authorized. Prerequisites 1-5 are now complete in substance (§ Preflight below). The principal has
explicitly authorized exactly one Step 6 filing (`milestone6-prereq6-fresh-authorization-required`):
the fresh, explicit authorization that gate's own text has required since `PI-0038` created it. This
filing performs that authorization and no other work — it classifies no ticker and implements no
Milestone 6 output.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local branch confirmed identical to `origin/main` at
`d42988f2dae167c484d0b8a07bdb3ac2676a975c` — the exact SHA reported in the authorizing task,
independently re-derived, not trusted. Working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no competing mutation lane.

`PR #251` (`TIER-0004`) independently re-confirmed via the GitHub API in full, not taken from the
task's own summary: `merged: true`, merge commit `d42988f2dae167c484d0b8a07bdb3ac2676a975c` (matching
`origin/main`'s current tip exactly, parents `ecd1e89d1278432874dab0d5440a9a8eecbc57d1` and
`87891c9b720c14d7a37521136fe4d4248a155445`); three review rounds independently re-read in full
(`4865967653` CHANGES REQUIRED — 1 BLOCKING/1 MINOR/2 NOTE; `4866171285` delta CHANGES REQUIRED — the
BLOCKING resolved, 1 MINOR partially resolved; `4866305616` delta **DELTA APPROVED — APPROVED FOR
PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0/0/0/0 at exact head `87891c9b720c14d7a37521136fe4d4248a155445`);
retained principal-acceptance comment `issuecomment-5194141626` (explicit acceptance quoted verbatim
at that exact head, bound to review `4866305616` and exact-head CI run `31022188426`); retained
post-merge-verification comment `issuecomment-5194217647` (merge-tree identity confirmed byte-
identical, exact 6-file scope, 78 decisions/`issues == ()`, 2581/2581 full suite, merge-commit CI run
`31023085469`). Merge-commit CI independently re-fetched this session (`actions_get`,
`get_workflow_run`, resource `31023085469`): `status: completed`, `conclusion: success`, `head_sha`
matches `d42988f2...` exactly, on branch `main`.

`governance/decisions.yaml` and `portfolio_hq.dashboard.decisions.build_catalog('.')` both
independently re-derived: **78 decisions, `issues == ()`**, before this filing's own new row.
`TIER-0005` independently confirmed the next unused identifier (`TIER-0001`-`TIER-0004` are the only
prior entries; `TIER` remains the correct, already-established prefix — no new prefix minted).

`targets.yaml`'s `destination:` list independently re-derived: exactly the same 27 canonical equity
rows `TIER-0004` reconciled (`NVDA, TSM, ASML, AVGO, SNPS, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY,
ISRG, TMO, ICE, SPGI, V, COST, WM, CEG, ETN, GEV, GNRC, PWR, RTX, RKLB, TSLA`), zero drift. All 27
independently reconfirmed to carry governed Company Intelligence (`intelligence/companies/*.yaml`,
53 total records repository-wide, 0 missing among the 27). The two untracked local
`classification_validator.py`/`test_classification_validator.py` drafts reported from the prior,
separate, stopped Milestone 6 session are independently reconfirmed absent from this session's own
working tree (`git status --porcelain` clean; a repository-wide filename search finds zero matches);
`intelligence/classification/` does not exist anywhere in the repository.

`operations/WORKSTREAMS.yaml`'s live gate state, independently re-read (not copied from the
authorizing task): `milestone6-prereq1` through `milestone6-prereq4` all `status: complete`;
`milestone6-prereq5-population-reconciliation` reads **`status: in_progress`, `pr: null`** — stale
relative to `TIER-0004`'s now-confirmed merge, exactly the deferred synchronization `TIER-0004`'s own
post-merge-verification comment assigned to "the next WS-0005 filing"; `milestone6-prereq6-fresh-
authorization-required` reads `status: blocked`; `milestone-6-blind-classification` reads
`status: proposed`, "Not authorized to execute." All four independently confirmed live, matching the
task's expected state exactly.

No condition met a Stop bar. This unit proceeded.

## Decision

**This filing authorizes exactly one future, separate, bounded Milestone 6 (blind classification)
implementation pull request**, covering all 27 canonical equities under the exact population,
redaction, blindness, sequencing, abstention, sealing, contamination, and validator controls already
specified and accepted through `TIER-0004`. It performs no classification, creates no sanitized
evidence package, and implements no validator itself.

### A. What is authorized

One future implementation PR, gated on its own separate independent exact-head review (`OPS-0007`
§1), any required bounded correction and re-review, explicit principal acceptance, merge, and
post-merge verification — the same lifecycle every prior filing in this chain has followed — may
proceed to:

1. Draft and seal one classification record for each of the 27 canonical equities named in
   `TIER-0004` §A, zero exclusions, zero additions.
2. Use approximately five isolated blind-drafting shards of five to six tickers each (`TIER-0004`
   §I), with one deterministic sanitized-evidence-generation process, one integration and sealing
   pass, one cohort manifest, one fresh `classification_validator.py`, one dedicated validator test
   file, and one independent exact-head review of the fully integrated batch.
3. Stop after any single shard, without a separate pilot authorization, if a systemic leakage,
   schema, sanitizer, or contamination defect is discovered — an internal stop-and-fix condition
   within the one authorized implementation PR, not a license to split into a second governance
   filing or a per-ticker PR structure.

**No one-PR-per-ticker design. No separate pilot unless a genuine architectural defect surfaces
before drafting completes**, per the authorizing instruction.

### B. Binding specification — by reference, not restatement

The implementation PR must follow `TIER-0004`'s specification exactly, as accepted and merged at
`d42988f2dae167c484d0b8a07bdb3ac2676a975c`. This filing does not redesign, loosen, tighten, or restate
that specification in its own words beyond the index below — the implementation session has no
discretion to depart from it:

| Control | Governing section |
|---|---|
| 27-name population, zero exclusions | `TIER-0004` §A |
| Four-axis framework (`economic_role`, `capital_priority`, `risk_concentration`, `evidence_quality`) — no fifth axis, no score, no ranking formula, no target percentage, no weighting formula, no buy/sell signal | `TIER-0002` §3 (frozen), restated by `TIER-0004` throughout |
| Permitted inputs / forbidden answer-key inputs (`targets.yaml`, `target_pct`, `holdings.yaml` weights, `portfolio_role_ref`, `conviction`, `gates.yaml`, prior tier/policy conclusions, `caps.clusters`/`issuer_lookthrough.yaml` during judgment-axis drafting, chart-domain content in any form) | `TIER-0004` §B |
| Redaction mechanics — separate `.yaml` and `.md` sanitization, fail-closed mandatory re-scan treating any surviving marker as a hard failure, assembly from sanitized outputs only | `TIER-0004` §C (as bounded-corrected — the `.md` file is **not** exempt from redaction) |
| Sequencing — judgment axes sealed before `risk_concentration` is computed | `TIER-0004` §D |
| Sealing and contamination controls (`lifecycle_status`, `sealed_at`, `governing_decision`, `drafting_session_or_shard_id`, `schema_version`, `content_sha256`, cohort-manifest entry; shard isolation; sealed-before-comparison) | `TIER-0004` §E |
| `economic_role.economic_system_ref: unable_to_determine` abstention (requires `abstention_reason` + `evidence_gap_statement`; non-cascading to `capital_priority`/`evidence_quality`) | `TIER-0004` §F |
| Fresh `classification_validator.py` + test file, authored from `main` at implementation time | `TIER-0004` §G |
| Prior-stopped-session contamination exclusion — the untracked drafts must not be read, copied, adapted, moved, staged, or reused; both files authored fresh | `TIER-0004` §H, reconfirmed live this session (§ Preflight) |
| Batch/shard recommendation, now binding | `TIER-0004` §I |

Nothing in this table is amended, expanded, or narrowed by this filing. Any future session finding a
genuine ambiguity or gap in `TIER-0004`'s specification must return for its own separate governance
correction — not resolve it unilaterally inside the implementation PR.

### C. Stop conditions (binding on the future implementation)

The implementation PR must stop immediately and disclose, never silently work around: sanitizer
leakage; any surviving forbidden marker after the mandatory re-scan; unauthorized access to an
unsanitized source file by a drafting shard; schema ambiguity; an invalid or cascading abstention;
shard cross-contamination; population drift (extra or missing ticker against the 27-name list);
content-hash or cohort-manifest mismatch; chart-domain leakage; any protected-path mutation; or any
unexpected target, holdings, gate, cap, cluster, allocator, margin, ladder, order, or trade change.

### D. Independent review requirement (binding on the future implementation)

The implementation PR's independent exact-head review must verify, at minimum: the exact 27-name
population; the exact changed-file inventory; sanitizer and fail-closed controls for both `.yaml` and
`.md`; absence of answer-key leakage; shard isolation; four-axis schema conformance; abstention
validity and non-cascading behavior; sequencing; sealing metadata and hash/manifest consistency;
`classification_validator.py` and its tests; CI; protected-path isolation; absence of any Milestone 7
comparison; and absence of any policy mutation. Any correction requires its own fresh exact-head delta
review before principal acceptance.

### E. Register synchronization (this filing)

`operations/WORKSTREAMS.yaml`'s `milestone6-prereq5-population-reconciliation` gate is updated
`status: in_progress` → `status: complete`, `pr: null` → `pr: 251`, recording `TIER-0004`'s
independently reconfirmed merge (`d42988f2dae167c484d0b8a07bdb3ac2676a975c`), review chain (delta
approval `4866305616`), principal acceptance (`issuecomment-5194141626`), post-merge verification
(`issuecomment-5194217647`), and merge-commit CI (`31023085469`, `success`) — the deferred
synchronization `TIER-0004`'s own post-merge-verification comment assigned to this filing.
`milestone6-prereq6-fresh-authorization-required` is updated `status: blocked` → `status: in_progress`,
recording this filing's own branch and (once it exists) PR number — **not** `status: complete`, since
this filing's own governance PR is itself unmerged, unreviewed, and unaccepted, matching every prior
WS-0005 filing's identical discipline. `milestone-6-blind-classification` is left exactly as it
stands, `status: proposed`, "Not authorized to execute" — this filing's own authorization does not
make that gate executable while this filing's own PR remains unmerged; a later, separate filing
performs that transition once this PR merges and is post-merge verified, per the same discipline
applied to every prior gate in this chain (including `milestone6-prereq5` itself, left `in_progress`
by `TIER-0004` pending this filing).

### F. Non-authority

This decision does not authorize: any tier/target/holdings/role/cluster/cap/gate/allocator/margin/
ladder change; any trade or order; any chart use of any kind; any buy or sell recommendation; any
deployment recommendation; any comparison of a future classification record against current portfolio
policy; Milestone 7 baseline reconciliation; any policy recommendation; classification of any ticker
by this filing itself; creation of `intelligence/classification/` or any file inside it; any sanitized
evidence package; any validator implementation; or any edit to `CHART-0001`, `CHART-0002`,
`TIER-0001`, `TIER-0002`, `TIER-0003`, or `TIER-0004`'s own text. Milestone 6, once authorized to
execute and implemented under §A-D above, produces sealed classification evidence only — no score,
no ranking, no target, no policy conclusion.

### G. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — the §E gate updates plus the
`active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields per
`OPS-0001`'s existing convention); (4) `CLAUDE.md` (one concise Decisions Log pointer entry);
(5) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-count assertions,
78→79, made stale by this filing's own new row). No supporting audit artifact is created — `TIER-0004`
already contains the complete accepted process specification, and restating it in a second retained
document would duplicate content rather than add evidence. No chart file, no `intelligence/` company/
theme/relationship/classification record, no `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`, and no production allocator/margin code is touched.

### H. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review,
and receive explicit principal acceptance before it may be marked ready or merged. This session does
not review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this
decision becomes effective until this governance PR merges to `main` — including the authorization in
§A, which the future implementation session may not rely on before that merge.

## Rationale

**Why this filing authorizes rather than redesigns.** `TIER-0004` already carries a complete,
independently reviewed (three rounds, one BLOCKING and one MINOR finding both resolved), principal-
accepted, merged, and post-merge-verified specification for every mechanical and evidentiary control
Milestone 6 needs. Re-deriving or rephrasing that content here would introduce exactly the kind of
drift risk `TIER-0004`'s own BLOCKING finding demonstrated a plausible-sounding restatement can carry
— the smaller and more reliable move is to bind the future implementation to `TIER-0004`'s own text by
reference, unchanged.

**Why one implementation PR for all 27 tickers, not a per-ticker or partial-batch structure.**
`TIER-0004` §I already recommended this shape after weighing it against the alternative; this filing
makes that recommendation binding rather than re-litigating it. A per-ticker PR structure would
multiply review overhead 27-fold for a single coherent population with a single shared specification
— the same proportionality reasoning `OPS-0008`'s Research Wave Protocol applied to Company
Intelligence batches.

**Why implementation is not folded into this same filing.** The authorizing instruction is explicit
that this filing "must not itself classify any company or implement any Milestone 6 output." Unlike
several smaller Company Intelligence batches in this repository's history that combined governance
authorization and delivery in one PR, Milestone 6 is the first unit in this chain to touch all 27
canonical names at once under a brand-new record type with untested sanitization mechanics — the
higher blast radius of a mechanical leakage or contamination defect (as `TIER-0004`'s own BLOCKING
finding demonstrated is a live risk, not a hypothetical one) favors keeping authorization and
execution as separately reviewable units, matching `REL-0001`'s own precedent of freezing a schema in
one filing and authorizing content separately.

**Why `milestone-6-blind-classification` is not flipped to an executable status by this filing.** The
authorizing instruction is explicit that the gate stays `proposed` and non-executable "while this
authorization PR remains unmerged." This filing's own text becomes binding only on its own merge (§H)
— transitioning the gate before that would assert an authorization this filing cannot yet actually
provide, the same discipline `TIER-0004` applied to leaving `milestone6-prereq5` at `in_progress`
rather than `complete` while its own PR was still open.

**Why no new supporting audit artifact.** Every fact this filing needs — the accepted redaction,
sequencing, sealing, abstention, and validator specification — already exists in `TIER-0004`'s merged,
reviewed text. Creating a second retained document that restates the same content would violate this
repository's own "reference, don't restate" discipline (`REL-0001`, `PI-0016`) without adding
verifiable evidence.

## Alternatives Considered

- **Redesign or restate `TIER-0004`'s specification in this filing's own words**, on the theory that a
  Step 6 authorization should be self-contained. Rejected — see Rationale; the authorizing instruction
  explicitly directs citing `TIER-0004` precisely rather than duplicating it, and restatement itself
  introduces drift risk the binding-by-reference table (§B) avoids.
- **Authorize a smaller first batch (e.g. 5-6 tickers) rather than all 27 at once**, mirroring earlier
  Company Intelligence research waves. Rejected — Milestone 6 is not new-evidence research; it applies
  one already-frozen framework to an already-fully-covered population under one already-specified
  mechanism, so the proportionality concern that justified smaller research waves does not carry over
  the same way; `TIER-0004` §I's own recommendation (all 27 in one PR, internally sharded) already
  weighed this and is adopted as binding here.
- **Combine this authorization with implementation in one PR**, matching several prior batches'
  combined-filing precedent. Rejected — the authorizing instruction explicitly prohibits it for this
  filing, and the higher blast radius of a first-of-its-kind sanitization mechanism across the full
  population favors a separate, independently reviewable implementation lifecycle.
- **Flip `milestone-6-blind-classification` to `status: in_progress` now, since authorization text
  exists in this filing.** Rejected — the authorizing instruction is explicit that the gate stays
  `proposed`/non-executable until this filing's own PR merges; authorization is not effective before
  merge (§H).
- **Create a retained audit artifact restating `TIER-0004`'s process specification for this filing's
  own supporting evidence.** Rejected — `TIER-0004` is itself the retained, accepted specification;
  a second document repeating it would be redundant, not additive, matching the authorizing
  instruction's own expectation that none should be needed here.

## Consequences

**Authorized, effective only on this decision's merge:** one future, separate, bounded Milestone 6
implementation PR covering all 27 canonical equities, bound exactly to `TIER-0004`'s specification per
§A-D above, gated on its own full independent-review/correction/re-review/principal-acceptance/merge/
post-merge-verification lifecycle; the `milestone6-prereq5` gate transition to `status: complete`,
`pr: 251`; the `milestone6-prereq6` gate transition to `status: in_progress` recording this filing as
underway.

**Not authorized by this filing, now or ever without a further separate decision:** classification of
any ticker; any sanitized evidence package; any validator implementation; any edit to `CHART-0001`,
`CHART-0002`, `TIER-0001`, `TIER-0002`, `TIER-0003`, or `TIER-0004`'s own text; Milestone 7 baseline
reconciliation; any tier/target/holdings/role/cluster/cap/gate/allocator/margin/ladder/trade/
brokerage/order change; and execution of the `milestone-6-blind-classification` gate itself, which
remains `status: proposed` until a later, separate, post-merge synchronization filing transitions it.

**Unchanged by this decision:** every existing Company/Theme/relationship Intelligence record, byte-
for-byte; `CHART-0001`'s, `CHART-0002`'s, `TIER-0001`'s, `TIER-0002`'s, `TIER-0003`'s, and
`TIER-0004`'s own accepted text and scope, in full, unedited; `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the
Constitution; `WS-0005`'s top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and
`completion_criteria`; Milestones 1-4's own `status: complete` (unedited, not reopened); the
`milestone-6-blind-classification` gate's own `status: proposed` (unedited by this filing).

This decision becomes effective only when its implementing pull request merges to `main`.
