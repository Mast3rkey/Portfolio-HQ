---
decision_id: OPS-0014
date: 2026-08-03
status: Accepted
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, OPS-0011, OPS-0012, OPS-0013, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04, PHQ-2026-05, PHQ-2026-06]
supporting_artifact: null
---

## Context

Three completed, read-only audits — a Routine Operational Sync Governance Design review, a Portfolio-HQ Completion Roadmap Audit, and a Portfolio-HQ Research Coverage Audit — independently converged on the same governance gap: CLAUDE.md's "Git sync — automatic, not a request" section (`## Git sync`, the paragraph beginning "After any commit-worthy change") instructs a session to `git add`, commit, and `git push` **directly to `main`**, unprompted, for any tracked-file change, including factual portfolio updates (share counts, margin debt, cash, deposits, trade confirmations). That instruction predates this repository's governance architecture (`GOV-0001`, 2026-07-18) and its lean delivery/review lifecycle (`OPS-0009`, merged via PR #182) — both of which require every mutation to classify into a lane, move through a branch and (for anything beyond Lane M's narrow mechanical-sync exemption) an independent review round, and never write directly to `main`. In practice, every routine factual-sync decision filed since `OPS-0009` (`PHQ-2026-04`, `PHQ-2026-05`, `PHQ-2026-06`) has already operated as Lane M — branch, draft PR, principal acceptance of the underlying fact, merge — in direct tension with CLAUDE.md's still-unamended literal text. No decision until now has named this precisely as a standing classification-and-lifecycle rule for *conversational* factual-update requests (as opposed to authorizing one specific sync event), leaving every session to informally reconstruct the same reasoning from precedent rather than from controlling text.

Separately, the Completion Roadmap and Research Coverage audits found `operations/WORKSTREAMS.yaml`'s `WS-0005` and `WS-0012` entries carrying stale `active_branch`/`active_pr` self-references (PR #210 and PR #230, both already merged with no open PR remaining — confirmed live via GitHub this session), and found no `WS-0013` entry recording the dependency-ordered path from the workstreams already in flight (`WS-0005` Intelligence completion, `WS-0012` chart evidence) to an eventual governed final allocation check. Both are recording gaps, not authority gaps — `OPS-0001` already establishes that this register creates no authority and that live repository/GitHub state always controls over a stale cached field.

## Decision

OPS-0014 becomes standing procedural authority, effective on this decision's own acceptance, for classifying and handling routine conversational Portfolio-HQ operational requests — read-only inspection, ephemeral output, durable generated records, routine factual synchronization, material correction, governance/policy change, and (as an absolute prohibition) brokerage execution. It narrowly corrects CLAUDE.md's Git-sync wording so it no longer instructs a direct commit/push for factual portfolio mutations, without reopening or narrowing `OPS-0009`'s own lane definitions, `OPS-0001`'s register semantics, or any accepted decision's specific factual content.

### A. Mutation taxonomy

**Class 0 — Read-only inspection.** Status, explanation, `--review --no-log`, why a ticker was gated or blocked, confirming an already-recorded value is unchanged. No tracked write, no branch, no commit, no PR, no authority creation.

**Class 1A — Ephemeral generated output.** A local allocation transcript, a temporary diagnostic, a regenerable preview or report. Not committed, not pushed, non-authoritative, freely regenerable, and never permitted to mutate repository truth.

**Class 1B — Durable governed generated record.** Applies only where an existing accepted decision explicitly requires durable retention of a generated artifact (e.g., a canonical `performance_log.csv` row under the existing performance-logging convention, or another artifact a future decision specifically names). Never written directly to `main`; requires a narrow branch, a reproducibility/duplicate-event check, and a draft PR (or another future explicitly accepted lightweight merge mechanism — none exists yet, so a draft PR is the only current path) before merge. The output being *generated* is never by itself grounds for filing a new governance decision, and a generated file's mere current existence does not retroactively make it canonical — see §F below for the narrow-default rule this class runs under.

**Class 2 — Routine factual synchronization.** Exact equity/crypto share quantities, exact margin debt, exact broker-displayed margin buffer where directly evidenced, a confirmed deposit/withdrawal, a confirmed trade execution or non-execution, or another exact current factual field an accepted decision explicitly permits. This decision is the standing procedural authority for this class going forward — no new governance decision is required for each qualifying event. Requirements: the principal supplies or confirms the underlying fact; evidence meets §B's matrix; the exact delta is previewed before any mutation; a narrow branch is used; nothing is ever written directly to `main`; a draft PR is required under the repository's current lifecycle; focused validation runs before merge; the principal gives exact-head acceptance before merge; independent review may be waived only where `OPS-0009` §2's Lane M exemption legitimately applies (mechanical, non-authority-bearing, records an already-true, already-verified fact, introduces no new claim or interpretation) — principal acceptance of the underlying fact is never waived by that exemption, only the second independent-review round; post-merge verification is required; only the approved factual field(s) change; and a routine sync never changes policy. This mirrors, and does not alter, the pattern `PHQ-2026-04`/`PHQ-2026-05`/`PHQ-2026-06` already established in practice: hashed or directly-evidenced facts, disclosed rather than silently resolved conflicts, no renormalization of freed target weight without separate authorization, and an explicit statement of what each sync does not authorize.

**Class 3 — Material factual correction.** A conflict with a prior recorded fact, correction of misleading historical evidence, a confirmed event that retires or alters a gate or another authority-bearing object, materially contradictory screenshots or attestations, or disputed holdings/quantities. Requires the full branch-and-draft-PR lifecycle with independent review and principal exact-head acceptance; must preserve historical truth (never silently overwritten, same discipline `PHQ-2026-05`'s v1.37/v1.38 reconciliation already applied); may never be downgraded to Class 2 for convenience.

**Class 4 — Governance or investment-policy change.** Any change to tier, target, gate, cluster, cap, margin doctrine, allocator rule, the Intelligence-to-policy relationship, chart-policy use, or execution authority. Requires the full Lane G lifecycle (`OPS-0009` §1), an accepted decision, independent review, principal exact-head acceptance, and its own separate implementation authority — none of which OPS-0014 grants for any specific change.

**Class 5 — Prohibited brokerage or order execution.** Placing, routing, submitting, automating, scheduling, or implying execution of any brokerage order. Prohibited absolutely, with no exception this or any decision may carve out without amending the Constitution itself (§1-2). The principal executes manually in Robinhood.

### B. Evidence rules

**Settled cash** — distinct from buying power; the repository currently has no persisted `cash` field in `holdings.yaml` (confirmed this session — unchanged since `PHQ-2026-02`/`PHQ-2026-05`/`PHQ-2026-06`); it may be supplied as a runtime input to `allocate.py --cash`. A durable deposit/withdrawal fact may be recorded only under Class 2's accepted procedure. Principal attestation with an exact amount and date may suffice when consistent with prior state; a screenshot is preferred; any conflict requires abstention, not silent reconciliation (`PHQ-2026-06`'s disclosed, unresolved $0.18 gap is the precedent).

**Buying power** — context only; never treated as settled cash; never authorizes deployment; qualitative "ready to use" language is not a numeric buffer.

**Margin debt** — distinct from margin availability; a changed numeric value normally requires direct broker evidence; "still zero" may be recorded as a no-op factual confirmation (Class 0 or a trivial Class 2 no-op) rather than a mutation.

**Margin buffer** — persisted only as the exact broker-displayed value where `holdings.yaml`'s schema supports it (`margin.buffer_pct`); never derived from qualitative text (per CLAUDE.md's existing Margin doctrine, unchanged by this decision); stale or unavailable buffer data must be disclosed, not silently treated as current.

**Equity and crypto quantities** — require ticker/asset, exact quantity, direction, and confirmation the execution occurred; a screenshot or direct broker evidence is normally required where the fact is material, conflicting, gated, cap-relevant, or otherwise high-risk.

**Confirmed execution** — a recommendation is never an execution; principal confirmation must identify the exact ticker, quantity, and event; uncertainty in price/date is preserved rather than invented.

**Confirmed non-execution** — principal attestation suffices; share quantities are never mutated on this basis alone; recorded only when a governed durable record actually requires it.

**Screenshots** — establish only what they visibly show; margin debt, buying power, fills, or quantities not visible must never be inferred from one; provenance is preserved where retained (per the evidence-retention pattern PHQ-2026-02 established at `governance/evidence/<decision-id>/`, and per `PHQ-2026-04`'s narrower, non-retained choice where a decision explicitly makes that tradeoff).

**Conflicting, stale, or incomplete evidence** — mandatory abstention; stop and ask the principal; never silently reconcile (this is not a new rule — it restates the discipline `PHQ-2026-05`'s v1.37 conflict and `PHQ-2026-06`'s $0.18 gap already demonstrated in practice, as the standing rule it was always implicitly following).

### C. File boundaries

Class 2 may never touch `targets.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator production logic (`allocate.py`'s `plan()`/gating code), tests unrelated to the specific factual field being synced, Intelligence records, chart evidence, governance policy text, or margin-policy limits (the 1.8x leverage cap / 30% buffer floor). Any request that would necessarily touch one of those surfaces is not a Class 2 request — it escalates to Class 3 or Class 4 as applicable.

### D. Active-lane rule

At most one active mutation lane (branch/PR) runs against Portfolio-HQ at a time — no concurrent branch/PR mutations. Multiple read-only audits may run separately in clean, isolated clones without contending for the lane, since Class 0 work creates no branch or PR.

### E. Supersession of CLAUDE.md's Git-sync wording

This decision narrowly supersedes only the portion of CLAUDE.md's `## Git sync — automatic, not a request` section that instructs an immediate, direct `git commit`/`git push` to `main` for a factual portfolio mutation. It does not reopen or broadly rewrite `OPS-0009` — `OPS-0009` continues to govern Lane M's review-waiver treatment and every other lane exactly as filed. No direct-`main` write is permitted under any class this decision defines above Class 0/1A, and neither CLAUDE.md nor any future conversational instruction may, by itself, create an accepted decision or an accepted procedure — only a filed and accepted (or, for Class 2 events, this decision's own already-accepted procedural authority) governance record can do that. CLAUDE.md's session-start `git pull` and cross-session-honesty discipline (the rest of the Git-sync section) are unaffected — the correction is scoped to the commit/push instruction alone. See CLAUDE.md's own corrected text for the operative replacement language.

### F. Open Class-1B question — narrow, source-faithful resolution

Default generated output is Class 1A and is not committed. Only a specifically governed canonical record is Class 1B. A generated file merely existing in the repository today does not by itself make it canonical. This decision names one currently recognized durable generated record meeting that bar: `performance_log.csv`, written by `allocate.py`'s existing `log-performance`/`--review` (absent `--no-log`) paths under the pre-existing convention that record is a canonical, append-only performance ledger, not a regenerable transcript. Every other generated artifact this repository currently produces (dashboard HTML under `OPS-0011`/`OPS-0012`, retained audit artifacts under `governance/audits/`, Intelligence staleness reports under `intelligence/reports/`, chart-evidence packages under `governance/evidence/CHART-0002/`) is governed by its own already-accepted decision's specific retention rule and is unaffected by this section — this section does not reclassify any of them. Any other unresolved generated-artifact category remains Class 1A until a future decision specifically governs it as Class 1B; this decision does not pre-authorize that reclassification for anything not named above.

## Rationale

`OPS-0009`'s lean delivery lifecycle and the branch/draft-PR/review/merge discipline it and `GOV-0001`/`GOV-0002` require are already, in practice, exactly how every Portfolio-HQ factual-sync decision since `PHQ-2026-04` has actually been handled — CLAUDE.md's literal Git-sync text is the one piece of controlling-looking prose that still contradicts observed, already-accepted practice. Leaving that contradiction unresolved risks a future session following CLAUDE.md's literal instruction (direct push to `main`) precisely because it reads as the current operative rule, undoing the discipline `OPS-0009` established. Naming the taxonomy explicitly, rather than leaving each session to re-derive Lane M eligibility informally from PHQ precedent, reduces the chance of either an under-cautious silent-write error or an over-cautious escalation of a genuinely mechanical fact to a full governance filing.

## Alternatives Considered

**Do nothing, rely on `OPS-0009` alone.** Rejected — `OPS-0009` defines lanes for *changes already in a PR*, not the upstream question of when a conversational request should become a branch/PR at all instead of a direct commit; CLAUDE.md's text is the thing a session actually reads first, and it currently answers that question wrongly.

**Broadly rewrite CLAUDE.md's workflow section.** Rejected per the principal's explicit bounding of this unit — a broad rewrite risks touching investment doctrine or workflow text this audit did not review, and the smallest correction that removes the direct-push instruction is sufficient to close the gap.

**Fold this into a new `OPS-0009` amendment instead of a new decision.** Rejected — `OPS-0009` is a cross-cutting lifecycle decision already carrying its own scope; a routine-sync-specific classification taxonomy is a distinct decision domain (matching this repository's existing pattern of narrow, single-purpose `OPS-####` filings — `OPS-0011`/`OPS-0012`/`OPS-0013` each added one bounded capability rather than amending an earlier one), and narrow supersession (§E) is the established mechanism for correcting exactly the parts of prior text that need it.

**Make every Class 1B artifact require its own new decision.** Rejected — this would require re-litigating `performance_log.csv`'s already-settled status; naming it once and leaving everything else Class 1A by default is the narrower, source-faithful rule the principal specified.

## Consequences

Going forward, a session handling a conversational Portfolio-HQ request classifies it under this taxonomy before acting. Read-only requests make no mutation. Routine facts (Class 2) use the branch/draft-PR procedure this decision makes standing authority for, without requiring a new governance filing per event. Material corrections and any governance/policy change continue to require their own full lifecycle exactly as before. No direct write to `main` is permitted for any class above Class 0/1A. No order is ever placed by any repository code, under any class. This decision changes no tier, target, gate, cluster, cap, margin parameter, allocator rule, or holding, and authorizes no research, no chart interpretation, and no allocation check — it is a classification and lifecycle decision only.
