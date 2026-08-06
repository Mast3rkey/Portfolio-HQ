---
decision_id: TIER-0007
date: 2026-08-05
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0004, PI-0016, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, REL-0001, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, OPS-0016]
supporting_artifact: null
file: governance/decisions/TIER-0007-ws0005-milestone7-baseline-reconciliation-authorization.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1)
governance filing that **defines and authorizes** the future WS-0005 Milestone 7 ("Baseline
reconciliation," `OPS-0006` §4.7) implementation. This filing must not perform the reconciliation
itself. It must define exactly how the 27 sealed Milestone 6 blind classifications
(`intelligence/classification/*.yaml`, sealed under `TIER-0002`/`TIER-0003`/`TIER-0004`/`TIER-0005`,
implemented by PR #253, completion determined by `TIER-0006`) may later be unblinded and compared
with the current governed portfolio baseline while preserving the blind records unchanged.

`OPS-0006` §4.7 already names Milestone 7's subject ("Baseline reconciliation") and `operations/
WORKSTREAMS.yaml`'s `milestone-7-baseline-reconciliation` gate already carries controlling
description text (quoted in full in §A below) — this filing binds a fuller specification to that
existing gate, the same "define, then later authorize implementation" pattern `REL-0001` used for
Milestone 4 and `TIER-0001`/`TIER-0002` used for Milestone 5, rather than inventing new milestone
scope.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/milestone-7-baseline-reconciliation-auth-dmtyr6`,
  working tree clean at session start.
- **`origin` fetched and reconciled.** Local branch tip and `origin/claude/milestone-7-baseline-
  reconciliation-auth-dmtyr6` both confirmed at `eac680ef8ba3e11592181b6e7063b7d90566e6f0` — the
  exact previously-reviewed head. Base `main` unchanged at `1107c5b70801ff5e7027efddf6a2aa916030dce2`.
- **PR #255 independently reconfirmed via the GitHub API:** `state: open`, `draft: true`,
  `merged: false`, `mergeable_state: clean`, `commits: 2`, `changed_files: 5` — all matching the
  expected values supplied for this correction. Exact-head CI (check run `92468496446`, workflow run
  `31054341293`) independently reconfirmed `completed`/`success`, anchored to head
  `eac680ef8ba3e11592181b6e7063b7d90566e6f0`.
- **Independent review `4869718735` retrieved and read directly from GitHub, not assumed from any
  summary.** Anchored to the same head. Verdict `CHANGES REQUIRED` — 0 BLOCKING / 2 MAJOR / 1 MINOR /
  0 NOTE. Every other section of the prior filing (sealed-record integrity, permitted-input
  labeling, chart boundary, non-retroactive-rewrite rule, non-authorization boundary, protected-path
  isolation, TIER-0006 lifecycle synchronization) was independently confirmed sound by that review —
  this correction is scoped to exactly the three findings below and touches nothing else.

### Correction history (this filing, same PR)

**Bounded correction, review `4869718735`, three findings, 0 BLOCKING / 2 MAJOR / 1 MINOR:**

1. **MAJOR** — the original §G (disposition vocabulary) required "exactly one" of six flat values
   with no precedence or tie-break rule for a ticker that qualifies for more than one simultaneously
   (a real, not hypothetical, risk: 11 of 27 tickers already carry `risk_concentration.
   unmeasured_flag: true`, several of which will also independently support a substantive role/
   capital-priority comparison result). **Resolved** by replacing the flat six-value vocabulary with
   a **primary disposition (exactly one, deterministic precedence, four values)** plus a **closed
   secondary-condition flag set (zero to two, independent of the primary value)** — see §H.
2. **MAJOR** — the controlling gate text (§A) names "target-vs-evidence-supported range," but the
   sealed Milestone 6 schema (`TIER-0002`'s four-axis framework) contains no numeric range, band, or
   interval anywhere — confirmed by direct inspection of a live sealed record (`intelligence/
   classification/COST.yaml`) and by grepping `TIER-0001`/`TIER-0002` for "range" (zero hits). The
   original filing never operationalized this specific gate-text phrase. **Resolved** by adding a
   new §G, "Target-context comparison," defining a categorical-only comparison
   (`target_context_comparison`) that never proposes, estimates, or backsolves a numeric target —
   see §G. This renumbers the original §G ("Disposition vocabulary") to §H, and every subsequent
   section (§H–§N) to §I–§O.
3. **MINOR** — the bounded follow-up commit that recorded this PR's own number in `WS-0005`'s
   `active_pr` field left the new `tier0007-milestone7-baseline-reconciliation-authorization` gate's
   own `pr:` field at `null`, deviating from the `TIER-0003`/`TIER-0005` precedent of setting both.
   **Resolved** in `operations/WORKSTREAMS.yaml` directly (§M) — see the accompanying commit.

This correction performs no reconciliation, unblinds no ticker, inspects no ticker-level baseline
comparison, and edits no sealed Milestone 6 record or manifest — confirmed by the exact changed-file
inventory in §N, unchanged from the original filing (this decision file and `operations/
WORKSTREAMS.yaml`; `CLAUDE.md` receives one further factual-synchronization update after this PR's
own re-review, per §O, not as part of this correction commit).

## Decision

### A. Milestone 7's controlling gate text (quoted, not restated as authority)

`operations/WORKSTREAMS.yaml`'s `milestone-7-baseline-reconciliation` gate, unedited by this filing
beyond the additive record in §M:

> Unblind the sealed baseline and compare current-vs-researched role, tier-vs-proposed capital
> priority, target-vs-evidence-supported range, cluster-vs-relationship-map, caps-vs-portfolio risk,
> review cadence-vs-thesis uncertainty; every difference states evidence, reasoning, uncertainty,
> opportunity cost, controlling policy, and required governance action. Not authorized to execute.

This filing binds a full specification to that text. Nothing below expands the gate's own subject
matter — it operationalizes exactly what the gate already names, including the "target-vs-evidence-
supported range" phrase (§G), which the sealed evidence can support only categorically, not
numerically.

### B. Purpose

Milestone 7 will unblind the sealed 27-company Milestone 6 classifications
(`intelligence/classification/*.yaml`) and compare each against the current governed portfolio
baseline. For each of the 27 canonical equities, the comparison must identify, per ticker:

- **agreement** — the sealed judgment and current governed baseline point the same direction;
- **divergence** — they point in different directions or reach different weight;
- **stale baseline assumption** — the current baseline appears to rest on a fact the sealed record's
  (or a more current) evidence contradicts;
- **an evidence limitation** — either an unresolved-evidence condition (neither side settles the
  comparison) or a structural-measurement gap (`risk_concentration.unmeasured_flag`, or no current
  cluster/issuer-look-through/relationship coverage). Under this filing's design (§H), an evidence
  limitation is reported as a **secondary condition alongside whichever primary finding the
  available evidence does support** — it never stands alone in place of a substantive agreement,
  divergence, or staleness finding when one is reachable, and it never silently erases one;
- **governance action required later** — a specific, named future governance step the divergence
  would require, without taking that step here.

**Milestone 7 is analysis only.** It must not itself recommend or adopt new portfolio policy. It
identifies that a future policy review may be warranted; it does not decide what that policy should
be.

### C. Sealed-record integrity — required before any future unblinding

Before any future implementation may unblind a sealed record, it must:

1. re-run `classification_validator.py` against the current repository state and confirm `OK`;
2. recompute all 27 `content_sha256` values via `classification_validator.canonical_record_hash()`
   and confirm zero mismatches against `COHORT_MANIFEST.yaml`;
3. reconcile `COHORT_MANIFEST.yaml` bidirectionally against the 27 sealed records and the 27-name
   canonical universe;
4. confirm every record's `lifecycle_status` remains `sealed`;
5. confirm, via `git diff` against the `TIER-0006`/PR #253 merge state, that no sealed record has
   changed since Milestone 6 acceptance;
6. record the exact `main` merge SHA used as the comparison source (a specific, dated commit, not
   "current main" as a moving target).

`intelligence/classification/*.yaml` and `COHORT_MANIFEST.yaml` are **immutable evidence inputs** to
Milestone 7 — the future implementation must not edit or rewrite them. If a defect in a sealed
record is discovered during reconciliation (a factual error, an internal inconsistency, evidence that
has since changed), it must be **disclosed as a Milestone 7 finding**, not silently corrected in the
sealed record. Any proposed correction to a sealed Milestone 6 record requires its own separate
governed process (matching this repository's `governance/decisions/README.md` "never edit a file's
substance after `status: Accepted`" convention, applied here to sealed advisory records by the same
logic) and cannot be performed inside a Milestone 7 reconciliation unit.

### D. Permitted reconciliation inputs

After the §C integrity checks pass, the future implementation may compare the sealed records against
current governed baseline sources, including — where applicable per ticker:

- `targets.yaml` (current `target_pct` values, `caps.clusters` membership);
- `gates.yaml` (gate status, `next_gate` reopening condition, for the six formerly-gated names);
- current `portfolio_role_ref` fields and any current tier/band assignment recorded in Company
  Intelligence records;
- `holdings.yaml` or other current portfolio-state evidence, used only to describe factual baseline
  state (e.g., "currently held," "gated no-add") — never to compute a new target;
- `issuer_lookthrough.yaml`;
- `intelligence/relationships/*.yaml` (the 13 sealed-as-of-`REL-0006` relationship records);
- accepted Company and Theme Intelligence (`intelligence/companies/`, `intelligence/themes/`);
- current `review.last_reviewed`/`next_due`/evidence-quality state for each record;
- controlling governance decisions (this file's `related_decisions` list and any decision either
  cites).

The future implementation must clearly and separately label, for every claim in its output:

- **blind-classification conclusion** (from the sealed Milestone 6 record — quoted, not
  paraphrased into a different meaning);
- **current baseline policy** (`targets.yaml`/`gates.yaml`/`portfolio_role_ref` as they stand today);
- **factual current portfolio state** (`holdings.yaml` — held, gated, weight — descriptive only);
- **governing constraint** (a cluster cap, the 8%/40% no-add ceiling, the leverage cap, or any other
  binding rule that bears on the comparison);
- **reconciliation analysis** (the future implementation's own comparison reasoning);
- **unresolved evidence** (what neither side settles).

### E. Chart-evidence boundary

Milestone 7 remains **fundamentals-and-structure reconciliation only**. Chart evidence under
`CHART-0001`, `CHART-0002`, or any later chart decision must not be included in Milestone 7 unless a
separate future decision explicitly authorizes it. `TIER-0003`'s exclusion of chart evidence from
blind classification is not reopened, narrowed, or reinterpreted by this filing — Milestone 7
compares the same fundamentals-only sealed judgment `TIER-0003` produced against a fundamentals-only
current baseline. Charts remain a separate, downstream, advisory layer, preserved under `WS-0012` and
referenced only as future sequencing context in `WS-0013` — not an input to Milestone 7's
comparison.

### F. Required per-ticker output

The future implementation must authorize and deliver exactly one retained reconciliation artifact
covering all 27 canonical equities. For each ticker it must record, at minimum, the following
**eighteen fields**:

1. sealed `economic_role`;
2. current `portfolio_role_ref` or equivalent baseline role description;
3. role comparison result;
4. sealed `capital_priority` (status and rationale);
5. current target/tier/baseline capital-priority context (`target_pct`, gate status if applicable);
6. capital-priority comparison result — compares the sealed `capital_priority.status` to the
   baseline's priority/tier treatment; never a numeric range (see §G for the separate, categorical
   target-context comparison);
7. `target_context_comparison` (§G) — a categorical-only evaluation of whether the current numeric
   target context is consistent with the sealed evidence, kept distinct from item 6;
8. sealed `risk_concentration` (including `unmeasured_flag`);
9. current `caps.clusters`/`issuer_lookthrough.yaml`/`intelligence/relationships/` representation for
   that ticker;
10. structural-risk comparison result;
11. sealed `evidence_quality` (`primary_source_coverage`, disclosed uncertainty);
12. current evidence posture (freshness state, any material change since the seal date);
13. evidence-quality comparison;
14. `primary_disposition` (§H) — exactly one, closed four-value vocabulary, deterministic
    precedence;
15. `secondary_conditions` (§H) — closed flag set, zero to two values, independent of item 14;
16. supporting evidence (citing specific fields/records, not restated conclusions);
17. uncertainty (what the comparison could not resolve — and, when `primary_disposition:
    no_policy_conclusion`, specifically why none of the other three primary values could be
    responsibly supported);
18. later governance action required, if any (a named future step — e.g., "would require a future
    Milestone 8 policy-recommendation review of X" — never a decision made here).

The future implementation must **not** require or produce a new target percentage, target range,
valuation band, allocation interval, score, or ranking for any ticker. This applies to every field
above, including item 7 (§G) and items 14–15 (§H).

### G. Target-context comparison — operationalizing "target-vs-evidence-supported range"

The controlling gate text (§A) names "target-vs-evidence-supported range" as one of six required
comparisons. Independently confirmed against the sealed evidence itself: Milestone 6's four-axis
framework (`TIER-0002`) supplies only a closed-vocabulary `capital_priority.status`
(`maintain_current_weight` / `case_for_review` / `no_assessment`) plus free-text `rationale` — no
numeric target range, valuation band, or allocation interval exists anywhere in the sealed schema or
in any of the 27 sealed records. **There is no "evidence-supported range" to compare a target
against, and Milestone 7 must not invent one, infer one, or retrofit numeric policy content into the
sealed classification.**

This section operationalizes the gate-text phrase as a **categorical target-consistency comparison**,
kept distinct from item 6's capital-priority comparison (§F):

- item 6 (capital-priority comparison) compares the sealed `capital_priority.status` to how the
  baseline currently treats this name's priority/tier — i.e., does the sealed judgment about whether
  this name deserves additional capital-deployment consideration match current treatment;
- `target_context_comparison` (item 7, this section) separately evaluates whether the **existing
  numeric target context** (`target_pct`, and gate status where applicable) is categorically
  consistent with the sealed evidence — without generating, proposing, estimating, implying, or
  backsolving any replacement percentage, range, or interval.

Required shape:

```
target_context_comparison:
  status: categorically_consistent | categorically_divergent | unable_to_determine
  rationale: <evidence-grounded, non-numeric explanation>
```

- `categorically_consistent` — the current `target_pct`/gate context and the sealed categorical
  evidence point the same direction (e.g., sealed `maintain_current_weight` alongside an unchanged,
  non-gated target that has been reviewed recently);
- `categorically_divergent` — they point in different directions (e.g., sealed `case_for_review`
  alongside a target that has not been reviewed since, or a gated name whose sealed evidence no
  longer plainly supports the gate's own stated reopening condition);
- `unable_to_determine` — the evidence available is insufficient to reach either of the above.

`rationale` must explain, in evidence-grounded, non-numeric prose, why the status was reached.
`target_context_comparison` must never contain a `proposed_target_pct`, a target range, a desired
weight, buy or sizing advice, or a direction to increase or decrease allocation, and must never be
used to derive a ranking or score. This field is analysis only, matching every other Milestone 7
output (§B, §K).

### H. Disposition vocabulary (closed) — primary disposition plus secondary condition flags

Each ticker's reconciliation output carries exactly one **primary disposition** plus a closed set of
zero, one, or two **secondary condition flags**. This two-part design exists because a single flat
category cannot honestly represent a ticker that qualifies for more than one finding simultaneously —
a documented, not hypothetical, risk: `TIER-0006`'s own confirmed distribution shows 11 of 27 tickers
(SNPS, PANW, ISRG, TMO, ICE, SPGI, V, COST, WM, RTX, RKLB) carry `risk_concentration.
unmeasured_flag: true`, and several of those same names independently support a substantive role or
capital-priority comparison result on the evidence available. A flat enum with no precedence rule
would either force an arbitrary single-category choice or silently erase one of the two findings;
this design does neither.

**Primary disposition — exactly one, closed, evaluated in this deterministic order:**

1. `baseline_assumption_stale` — use when the current baseline rests on a factual or policy
   assumption that the reconciled evidence shows is no longer current or supportable. Takes
   precedence over `divergence_requires_review` and `aligned` whenever it applies — a stale
   assumption is a more specific and more directly actionable finding than a general divergence.
2. `divergence_requires_review` — use when the sealed classification and current baseline
   materially disagree, but the baseline is not demonstrably stale. Takes precedence over `aligned`.
3. `aligned` — use when the sealed classification and current baseline materially agree. **This does
   not mean "maintain current policy," "approved," or "no future change"** — it states only that the
   comparison found no material disagreement on the evidence available; it carries no policy
   authority of its own.
4. `no_policy_conclusion` — use **only** when the comparison cannot responsibly determine alignment,
   divergence, or staleness — i.e., a specific attempt to apply values 1–3 fails for a reason that
   must be recorded in the ticker's `uncertainty` field (§F item 17). This value is not a default and
   must not become a catch-all for "insufficient time to analyze" — it requires the same evidentiary
   rigor as the other three, applied to the negative conclusion that none of them can be reached.

Selection is mandatory and deterministic: evaluate value 1, then value 2, then value 3; assign value
4 only if none of 1–3 can be responsibly supported by the available evidence.

**Secondary condition flags — closed, zero to two, independent of the primary disposition:**

- `unresolved_evidence` — attach whenever an evidence limitation materially constrains any part of
  the comparison, regardless of primary disposition. An evidence limitation is reported alongside
  whatever primary disposition the available evidence *does* support — it is never assigned in place
  of a primary disposition, and it never causes a reachable primary disposition to be downgraded to
  `no_policy_conclusion`.
- `structural_measurement_gap` — attach whenever the sealed or current structural representation
  carries the governed measurement gap (sealed `unmeasured_flag: true` and/or no current
  `caps.clusters`/`issuer_lookthrough.yaml`/`intelligence/relationships/` coverage), regardless of
  primary disposition.

A ticker may carry zero, one, or both secondary flags, in any combination with any primary
disposition. Secondary flags must never replace a material primary divergence or stale-baseline
finding — a ticker that is structurally unmeasured but otherwise aligned remains `primary_
disposition: aligned` with `secondary_conditions: [structural_measurement_gap]`, never `primary_
disposition: structural_measurement_gap`. No value outside these two flags may appear in
`secondary_conditions` — the set is closed, not a free-text list.

**Examples of required behavior:**

- `primary_disposition: divergence_requires_review`, `secondary_conditions: [structural_measurement_gap]`
- `primary_disposition: no_policy_conclusion`, `secondary_conditions: [unresolved_evidence, structural_measurement_gap]`
- `primary_disposition: aligned`, `secondary_conditions: [structural_measurement_gap]` (structurally
  unmeasured but otherwise aligned)
- `primary_disposition: aligned`, `secondary_conditions: []` (no qualifying secondary condition)

This vocabulary is closed — no new primary or secondary value without its own future governance
decision, matching `PI-0004`'s conviction-vocabulary and `TIER-0002`'s axis-vocabulary precedent. No
score, rank, or implied action priority is derived from or attached to any primary disposition,
secondary flag, or combination of the two.

### I. Aggregate outputs

Beyond the per-ticker table, the future implementation should summarize, as analytical findings only
(never recommendations), with primary dispositions and secondary condition flags counted and listed
**separately — never merged, and never double-counted as if they were the same kind of thing**:

- count and identity of `aligned` names;
- count and identity of `divergence_requires_review` names;
- count and identity of `baseline_assumption_stale` names;
- count and identity of `no_policy_conclusion` names;
- count and identity of names carrying the `unresolved_evidence` secondary flag (regardless of
  primary disposition);
- count and identity of names carrying the `structural_measurement_gap` secondary flag (regardless
  of primary disposition), cross-referenced against `REL-0007`'s own 11-name `unmeasured_flag`
  finding for currency;
- count and identity of names carrying **both** secondary flags;
- recurring `economic_role` mismatches (a pattern across multiple tickers, not a single-name
  observation restated);
- recurring `capital_priority`/`target_context_comparison` mismatches;
- evidence-quality limitations (the `limited`/`partial` `primary_source_coverage` set — the six
  formerly-gated names and LLY, per `TIER-0006`'s own confirmed distribution, cross-checked against
  current state);
- portfolio-level patterns (observations that span multiple tickers or the whole 27-name set);
- unresolved questions;
- potential future policy topics (named, not decided).

A name may legitimately appear in more than one list at once (e.g., one primary-disposition list and
one or both secondary-flag lists) — this is expected under §H's design and must not be flattened
into a single number. No list, count, or cross-tabulation may be presented as, or used to derive, a
score, rank, or implied action priority.

### J. No retroactive rewrite

Milestone 7 must never edit `intelligence/classification/*.yaml` or `COHORT_MANIFEST.yaml`. It may
quote or reference sealed records. It may identify disagreement, incomplete evidence, a possible
classification defect, or facts that changed after the seal date (`TIER-0005`-governed, sealed under
PR #253, completion-determined by `TIER-0006` at merge commit `1107c5b70801ff5e7027efddf6a2aa916030dce2`).
Any proposed correction to a sealed record requires a separate governed process, per §C, and cannot
be performed inside a Milestone 7 unit.

### K. Explicit non-authorization

This filing and the future Milestone 7 implementation it authorizes must not, under any
circumstance:

- automatically or otherwise change targets, tiers, portfolio roles, gates, holdings, caps, clusters,
  issuer look-through, allocator logic, margin doctrine, or buy ladders;
- use chart evidence (§E);
- issue a buy, sell, hold, trim, wait, stage, or sizing instruction of any kind;
- place or simulate an order;
- perform Milestone 8 (policy recommendation) or Milestone 9 (independent review and adoption);
- execute a live or scenario allocation check (`allocate.py` or any wrapper of it);
- edit any sealed Milestone 6 record, `COHORT_MANIFEST.yaml`, any Company/Theme Intelligence record,
  or any `intelligence/relationships/` record;
- propose, estimate, imply, or backsolve a replacement target percentage or range of any kind (§G).

Milestone 7 may identify that a future policy review is warranted (`divergence_requires_review` or
`baseline_assumption_stale`, §H); it cannot decide what the new policy is. That remains Milestone 8's
exclusively future, separately authorized scope.

### L. Authorized future implementation unit

Exactly one later, separate, bounded Milestone 7 implementation PR is authorized, effective only
after **this** governance decision is independently reviewed, principal-accepted, merged, and
post-merge verified — matching `REL-0001`/`LADDER-0001`/`CHART-0001`'s "future PR gated on this
governance decision's own merge" convention. That future PR must cover all 27 canonical equities in
one coherent retained reconciliation artifact (or one small set of logically partitioned artifacts —
never one PR per ticker), following §F–§I's schema, primary/secondary disposition design, and
target-context design exactly — no restatement, no loosening, no reintroduction of a flat single-
value disposition or a numeric target range. Internal read-only shards may be used for research/
drafting efficiency (matching the Milestone 6 implementation's own shard pattern), but only one
primary authoring session may mutate the repository, and the shard boundary must not be treated as
authority to skip §C's integrity checks or §D's evidence-source labeling. The future implementation
must receive its own full validation, independent exact-head review under `OPS-0007` §1, any required
bounded correction and delta review, explicit principal exact-head acceptance, merge, and post-merge
verification — the complete lifecycle every prior WS-0005 milestone filing in this log has followed.
This authorization does not itself begin that work; nothing in §§B–K becomes operative for actual
reconciliation content until the future PR exists, follows this specification, and completes its own
lifecycle.

`intelligence/classification/*.yaml`, `COHORT_MANIFEST.yaml`, `classification_validator.py`, and the
sanitizer are **not** touched by this authorization or by the future implementation — the future PR
adds one new reconciliation artifact and its own tests/validator only where repository convention
requires them; it does not modify any existing Milestone 6 file.

### M. Milestone status and register synchronization performed by this filing

This filing does not itself perform any reconciliation and does not claim Milestone 7 work has begun.
`operations/WORKSTREAMS.yaml`'s `milestone-7-baseline-reconciliation` gate's own `status: proposed`
is **unchanged** by this filing — matching `REL-0001` §K's identical treatment of the
`milestone-4-portfolio-relationship-mapping` gate and `TIER-0001`'s identical treatment of the
`milestone-5-...` gate: this decision defines doctrine and authorizes one narrow future
implementation step; it does not flip the milestone itself to `in_progress`, since no reconciliation
content exists yet. This filing's original commit added one new, distinctly named, additive gate
entry, `tier0007-milestone7-baseline-reconciliation-authorization`, `status: in_progress`, recording
exactly this authorization; a second, same-day commit set that gate's `pr:` field to `255` once the
PR existed, matching the `TIER-0003`/`TIER-0005` precedent of recording the real PR number on the
self-tracking gate itself (not only on `WS-0005`'s top-level `active_pr` field) — this bounded
correction (§ "Correction history" above) closes that gap directly in `operations/WORKSTREAMS.yaml`,
the same PR, no separate follow-up filing required. `status` remains `in_progress` throughout —
following `TIER-0001`'s own corrected precedent, a filing may not mark its own unmerged work
`complete`.

This filing also folds in the routine Lane M post-merge factual synchronization for `TIER-0006`
(PR #254), disclosed as deferred by that PR's own post-merge-verification comment: a new
`tier0006-post-merge-verification` gate records the independently re-verified accepted head
(`306e1a0f716d2fd8d515f1d0496b81ca30af93f4`), merge commit
(`1107c5b70801ff5e7027efddf6a2aa916030dce2`), independent review (`4869309702`), principal acceptance
(`issuecomment-5198112358`), and merge-commit CI (`31052845524`, `completed`/`success`) — matching
the `tier0001-post-merge-verification` / `rel0002-post-merge-verification` pattern used by every
prior WS-0005 filing in this log. `WS-0005`'s `active_branch`/`active_pr`/`last_verified_main_sha`/
`last_verified_date` self-reference fields are updated to this filing's own live state
(`active_pr: 255`, recorded by the bounded follow-up commit within this same PR). `WS-0005`'s
top-level `status: in_progress`, `priority: primary`, `authorized_scope`, and `prohibited_scope` are
unchanged.

### N. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — two additive gate entries and the
self-reference fields, per §M); (4) `CLAUDE.md` (one concise Decisions Log pointer entry, updated
after this bounded correction to reflect the corrected specification); (5) `test_portfolio_hq_
dashboard_decisions.py` (the two hardcoded decision-count assertions, 80 → 81). This bounded
correction round touches only this decision file and `operations/WORKSTREAMS.yaml` (the `pr:` field
fix, §M) — no new file, no `governance/decisions.yaml` change (no metadata field changed), no
`test_portfolio_hq_dashboard_decisions.py` change (no count changed). No production code, no
`intelligence/classification/` or `intelligence/relationships/` file, no `governance/audits/`
artifact, no other workstream, and no existing Company/Theme Intelligence or classification record
is touched, in either the original filing or this correction.

### O. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (`OPS-0009` Lane G — a new governance authorization, full weight,
never reduced), complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This filing does not review
itself, mark itself ready, merge itself, or post principal acceptance. Nothing in §§A–N above becomes
effective, and the future Milestone 7 implementation unit in §L remains unauthorized to begin, until
this PR merges to `main`.

## Rationale

Milestone 6's own lifecycle (`TIER-0001` through `TIER-0006`) repeatedly demonstrated that defining a
milestone's evidence boundary, output shape, and integrity controls *before* authorizing content work
catches defects a combined "define and execute" filing would not: `TIER-0004`'s population/redaction
specification surfaced (and fixed, before any drafting began) the exact `.md` whole-section-header
redaction gap that would otherwise have leaked forbidden conclusions into all 27 blind-drafting
shards. This filing's own first-round independent review demonstrated the same value in the opposite
direction — it caught a disposition-precedence gap (§H) and a gate-text-fidelity gap (§G) before any
comparison content existed, exactly the kind of underspecified-threshold defect that required a
bounded correction during the Milestone 6 implementation itself (`TIER-0002`'s `capital_priority`
threshold, corrected in PR #253's second review round). Fixing both now, before the future
implementation drafts against this specification, is strictly cheaper than discovering either defect
across 27 tickers' worth of already-written comparison content.

Binding to the existing `milestone-7-baseline-reconciliation` gate text (§A) rather than restating
Milestone 7's subject in new words follows `TIER-0005`'s own explicit reasoning for citing `TIER-
0004` "by reference, not restatement": restatement is exactly the risk a prior BLOCKING finding
(`TIER-0004`'s own redaction gap) demonstrated is live, not hypothetical, when a specification is
paraphrased rather than quoted. This correction reinforces that discipline rather than abandoning it:
§G does not restate the gate text in looser words — it explains precisely why the sealed evidence can
satisfy the "range" phrase only categorically, and defines exactly what that categorical comparison
must contain and must never contain.

Leaving the parent `milestone-7-baseline-reconciliation` gate at `status: proposed` (§M) rather than
advancing it to `in_progress` matches the identical, twice-established precedent of `REL-0001` §K
(Milestone 4) and `TIER-0001` (Milestone 5): a schema/definition/authorization filing that performs
no substantive milestone content is not itself "the milestone beginning." Tracking this filing's own
progress via a new, distinctly named gate (`tier0007-milestone7-baseline-reconciliation-
authorization`, `status: in_progress`) rather than marking the parent gate or this filing's own unit
`complete` follows `TIER-0001`'s own corrected precedent — that correction (review `4859945925`)
found a filing marking its own still-open PR's gate `complete` a MAJOR defect; the fix has held
without recurrence across five subsequent filings (`TIER-0002` through `TIER-0006`), and this
filing's own Finding 3 (a narrower `pr:`-field synchronization gap, not a premature-`complete` defect)
does not disturb that record.

## Alternatives Considered

**Perform the reconciliation in this same filing.** Rejected per explicit principal instruction — the
principal's own authorization draws the line at "define and authorize," not "define and execute,"
mirroring `REL-0001`'s split from `REL-0002`/`REL-0003` and `TIER-0001`'s split from the later
Milestone 6 implementation. A single filing that both designs the comparison schema and populates it
for 27 tickers would also make an eligible independent reviewer's job materially harder — reviewing
schema soundness and reviewing 27 tickers' worth of factual comparison content are different review
tasks, and Milestone 6's own four-round review history shows how much surface area 27-ticker content
review already carries on its own.

**Advance `milestone-7-baseline-reconciliation` to `status: in_progress` directly, rather than adding
a new gate.** Considered, since this filing is unambiguously the first work on Milestone 7. Rejected
because `REL-0001` and `TIER-0001` already established, and no later WS-0005 filing reversed, that a
milestone's own top-level gate is reserved for actual milestone-content progress, not for a preceding
schema/authorization filing — the same distinction §M states explicitly. Using the new-gate pattern
instead keeps that convention unbroken and keeps the parent gate's status meaningful (it will now
mean, unambiguously, "content work has started" whenever it does move past `proposed`).

**Fold the `TIER-0006` post-merge synchronization into a separate, later filing instead of this
one.** Rejected as unnecessary process overhead — `OPS-0008` §4(a)'s read-only post-merge convention
and every `tier0001-post-merge-verification`/`rel0002-post-merge-verification`-style prior entry in
this log already establish that the very next authorized filing folds in the prior filing's routine
post-merge confirmation rather than spawning a dedicated reconciliation PR for it.

**Authorize the six comparison axes (role, capital priority, target range, cluster, risk, review
cadence) named in the original `milestone-7-baseline-reconciliation` gate text as six independent
future sub-units, matching Milestone 6's own `milestone6-prereq1` through `prereq6` sequencing.**
Considered, since Milestone 6 needed six sequenced prerequisite steps before its own fresh
authorization. Rejected: Milestone 6's prerequisites existed because population, freshness,
relationship-gap, and chart-scope questions each had to be resolved *before* a defensible blind-
classification specification could be written, and each had genuinely separate evidence
requirements. Milestone 7's six comparison axes are not sequentially dependent on each other in the
same way — they are columns of one per-ticker comparison table (§F), not six separate research
questions — so splitting them into six separate authorization filings would multiply governance
overhead without a corresponding evidence-quality benefit. This filing's own §F, §G, and §H, taken
together, now genuinely operationalize all six named comparisons — role (§F items 1–3), capital
priority (§F items 4–6), the target-context phrase specifically (§F item 7, §G), cluster/relationship
representation (§F items 8–10), evidence quality (§F items 11–13, serving as the closest available
proxy for the gate text's "review cadence-vs-thesis uncertainty," since Milestone 6 sealed no
separate cadence judgment), and disposition (§F items 14–15, §H) — a claim the original filing made
prematurely for the target-range comparison specifically before this correction actually built it.

**Merge the target-context comparison (§G) into the capital-priority comparison (§F item 6) rather
than adding it as a separate field.** Considered, since both ultimately compare the sealed
`capital_priority` judgment against current policy. Rejected: the gate text (§A) names "tier-vs-
proposed capital priority" and "target-vs-evidence-supported range" as two distinct comparisons, and
conflating them into one field would re-introduce exactly the ambiguity Finding 2 identified — a
future implementer or reviewer would not be able to tell whether a single comparison result was
addressing the priority-treatment question or the target-consistency question. Keeping them as
separate, cross-referenced fields (§F items 6 and 7) preserves the gate text's own distinction while
being explicit that both draw on the same underlying sealed evidence.

## Consequences

Once this filing merges, a future, separately authorized Milestone 7 implementation PR may begin,
bound to §§B–L's specification — including the primary/secondary disposition design (§H) and the
categorical target-context comparison (§G), neither of which may be loosened, restated, or replaced
with a numeric range without its own future governance decision. That future PR still requires its
own full independent-review and principal-acceptance lifecycle — this filing does not shorten or
bypass any of it. Until that future PR exists and completes its own lifecycle, the 27 sealed
Milestone 6 records remain exactly as `TIER-0006` left them: sealed advisory evidence, unblinded by
nothing, compared against nothing, carrying no portfolio-policy authority. `milestone-8-policy-
recommendation-package` and `milestone-9-independent-review-and-later-adoption` remain untouched,
unauthorized roadmap items — this filing does not advance either, and completing a future Milestone 7
implementation would not by itself authorize Milestone 8.
