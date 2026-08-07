---
decision_id: TIER-0009
date: 2026-08-06
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0004, PI-0016, PI-0031, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0008, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, OPS-0016, CONTENDER-0001, XASSET-0001]
supporting_artifact: null
file: governance/decisions/TIER-0009-ws0005-milestone8-policy-recommendation-framework-authorization.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1)
governance filing that **defines and authorizes** the future WS-0005 Milestone 8 ("Policy
recommendation package," `OPS-0006` §4.8) implementation. This filing must not itself produce a
single per-ticker Milestone 8 recommendation. It must define exactly what a future implementation
may and may not conclude, given that Milestone 7 ("Baseline reconciliation") is now formally
complete (`TIER-0008`, PR #260) but no governed valuation architecture, cross-asset synthesis
(`XASSET-0001`), or complete relationship map exists yet.

`operations/WORKSTREAMS.yaml`'s `milestone-8-policy-recommendation-package` gate already carries
controlling description text (quoted in full in §A below) — this filing binds a fuller specification
to that existing gate, the same "define, then later authorize implementation" pattern `REL-0001` used
for Milestone 4, `TIER-0001`/`TIER-0002` used for Milestone 5, and `TIER-0007` used for Milestone 7,
rather than inventing new milestone scope.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/ws-0005-milestone-8-design-h4k9wq` (created from a clean
  `main` tip), working tree clean throughout.
- **`origin/main` fetched and reconciled.** `git fetch origin main` returned
  `6b503b8..aed2599 main -> origin/main`; `git rev-parse origin/main` returned
  `aed259994ea6aa2db08a24a3a1488ebcc39ca985`, matching this session's own starting branch tip exactly
  (`HEAD` confirmed an ancestor of `origin/main` before this filing's first edit).
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open`) —
  empty result. No competing mutation lane exists.
- **PR #260 (`TIER-0008`) independently re-confirmed merged** via the GitHub API: `merged: true`,
  head `c7572aa0f8aa5fd552408bb4920c750a44fd2840`, merge commit
  `aed259994ea6aa2db08a24a3a1488ebcc39ca985`, `merged_at: 2026-08-06T16:35:17Z`, 5 changed files, 2
  commits — matching the session brief exactly.
- **PR #260 merge-commit CI independently re-checked this session, honestly, not assumed clean.**
  `GET /commits/aed2599.../check-runs` returned exactly one check run
  (`92684405269`, workflow run `31120358031`): `status: completed`, `conclusion: cancelled` — an
  infrastructure-layer queue cancellation, not a content-related test failure, matching the session
  brief's disclosure of "repeated infrastructure-layer failures: runner queue timeout/cancellation;
  GitHub action-resolution 'Service Unavailable' before checkout; subsequent prolonged queueing." No
  successful merge-commit CI run for `aed2599` was found as of this preflight. **This filing does not
  treat that gap as resolved** — it is disclosed here as a known, still-open infrastructure condition
  on the merge commit this filing's own base rests on, separate from and not remedied by this
  filing's own independent local re-verification below.
- **Independent local re-verification against the exact merged tree, performed this session in place
  of a clean merge-commit CI run**: `python3 -m pytest -q` — **2939 passed, 0 failed** (one
  pre-existing, unrelated `DeprecationWarning` on `intelligence_classification_sanitizer.py`'s own
  docstring, matching every prior WS-0005 filing's disclosed, unaffected warning). `git diff --check`
  — clean. This matches `TIER-0008`'s own post-merge-verification comment
  (`issuecomment-5207710145`) exactly and confirms the merge tree's content is sound independent of
  the CI infrastructure gap above.
- **`TIER-0008` merged presence and Milestone 7 gate status independently re-read** from live
  `operations/WORKSTREAMS.yaml`: `milestone-7-baseline-reconciliation` reads `status: complete`,
  `pr: 259`, with `TIER-0008`'s own additive paragraph recording PR #260's accepted head, merge SHA,
  independent review (`4876183783`), principal acceptance (`issuecomment-5206850218`), and post-merge
  verification (`issuecomment-5206936450`) in full. **Milestone 7 is confirmed formally complete.**
- **`milestone-8-policy-recommendation-package` gate text independently re-read**, quoted verbatim in
  §A below — unedited by any filing to date; `status: proposed`, `pr: null`.
- **Decision catalog independently reconciled**: `governance/decisions.yaml` — exactly 85
  `decision_id` rows; `ls governance/decisions/*.md` (excluding `README.md`) — exactly 85 files;
  `portfolio_hq.dashboard.decisions.build_catalog('.')` — **85 decisions, `issues == ()`**. No
  `TIER-0009` reference exists anywhere in `governance/`, `operations/`, or `CLAUDE.md` prior to this
  filing (repository-wide grep, zero matches). The highest filed `TIER-####` is `TIER-0008` —
  **`TIER-0009` independently confirmed the next unused identifier.**
- **`XASSET-0001` and `CONTENDER-0001` independently re-read in full** (both `status: Proposed`,
  merged to `main` via PR #256). `XASSET-0001` §H binds three requirements this filing must satisfy
  exactly: (1) Milestone 8 must clearly label any 27-equity-cohort-derived result as equity-scoped in
  every finding it produces; (2) Milestone 8 cannot claim final whole-portfolio target readiness
  before the cross-asset work `XASSET-0001` requires (executed under `WS-0014`) completes; (3)
  Milestone 9 does not silently convert equity-only findings into final whole-portfolio policy.
  `CONTENDER-0001` §B confirms the 27 sealed equity records are "not sufficient alone to determine
  final whole-portfolio targets" and are not the exhaustive contender universe.
- **`TIER-0003`'s chart-evidence boundary independently re-read in full** (§§A–E). Option A
  (fundamentals/business-evidence only) is binding on Milestone 6 blind classification and, per
  `TIER-0007` §E, on Milestone 7 reconciliation as well — neither reopened, narrowed, or
  reinterpreted here.
- **`CHART-0003` independently checked for existence** — confirmed absent from `governance/decisions/`
  and `governance/decisions.yaml` as of this preflight; the highest filed `CHART-####` remains
  `CHART-0002`. Not listed in `related_decisions` above and not cited anywhere in this filing — no
  unfiled decision is cited as authority anywhere in this filing.
- **Current governed authority for valuation, relationship, chart, ETF, crypto, cash/GLD/debt,
  cross-asset, allocation, ladder, and monitoring, independently re-confirmed**:
  - **Valuation**: no governed valuation architecture, methodology, or numeric-target-generation
    framework exists anywhere in this repository. `allocate.py`'s gap-filling logic operates on
    `targets.yaml`'s already-configured `target_pct` values — it does not compute what a target
    *should* be. No workstream, decision, or module produces a valuation output.
  - **Relationship**: `REL-0001` through `REL-0007` (Milestone 4, complete) — 13 sealed
    `intelligence/relationships/*.yaml` records; `REL-0007` independently confirmed 11 of 27 canonical
    equities carry `risk_concentration.unmeasured_flag: true` (SNPS, PANW, ISRG, TMO, ICE, SPGI, V,
    COST, WM, RTX, RKLB) with no further relationship research authorized.
  - **Chart**: `CHART-0001`/`CHART-0002` (Stage 1 image-level evidence, 19 charted equities as of the
    last recorded batch) — advisory, downstream, fundamentals-excluded per `TIER-0003`.
  - **ETF/crypto**: no governed classification framework exists (`XASSET-0001` §C requires one, not
    yet designed).
  - **Cash/GLD/debt**: no governed functional doctrine exists (`XASSET-0001` §D requires one, not yet
    designed).
  - **Cross-asset**: `XASSET-0001` (architecture only, `WS-0014` execution not yet begun).
  - **Allocation**: `allocate.py`/`levels.py` — live, unaffected, out of this filing's scope entirely.
  - **Ladder**: `LADDER-0001` (research charter only, no simulation run yet).
  - **Monitoring**: `intelligence_report.py`/`freshness_*` (existing, unaffected, out of scope).
  None of the above is created, extended, or narrowed by this filing.
- **No competing mutation lane or preserved uncommitted work** — working tree clean at every check
  above; no stash, no untracked file, no other local branch carrying unpushed work found via
  `git branch -vv` and `git status --porcelain`.

No condition on this unit's own stop list was triggered by anything found above except the disclosed,
non-blocking merge-commit CI infrastructure gap on `aed2599`, which does not contradict any review,
acceptance, or content-level fact this filing relies on and is reported rather than concealed.

## Decision

### A. Milestone 8's controlling gate text (quoted, not restated as authority)

`operations/WORKSTREAMS.yaml`'s `milestone-8-policy-recommendation-package` gate, unedited by this
filing beyond the additive record in §L:

> Advisory-only recommendations covering portfolio roles, tier/replacement classification
> architecture, capital-priority rules, targets/target ranges, maximum position sizes,
> economic-system/overlap limits, monitoring frequency, thesis-break review rules, add/hold/trim/
> exit-review discipline. Not authorized to execute.

This filing binds a full specification to that text. Nothing below expands the gate's own subject
matter — it operationalizes exactly the eight areas already named, distinguishing which can be
answered categorically today from which cannot be answered at all without governance this repository
has not yet built.

### B. Purpose

Milestone 8 will produce, for each of the 27 sealed-and-reconciled canonical equities, one advisory
recommendation-package entry addressing the eight areas named in §A. **Milestone 8 is analysis and
advisory categorization only.** It must not itself execute, adopt, or automatically apply any
tier/target/role/gate/holdings/cap/cluster/allocator/margin/ladder/order change. It builds directly on
Milestone 6's sealed classifications (`intelligence/classification/*.yaml`) and Milestone 7's
reconciliation (`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`) — it does not
re-derive either from scratch, and it does not reopen or edit either.

Because no governed valuation, cross-asset, or complete relationship framework exists, this filing
sorts every field a future implementation could produce into six treatment classes:

- **(A) categorical recommendation currently permitted** — a non-numeric, process-level finding
  (`retain_current_baseline` / `review_warranted`) reachable today from Milestone 6/7's own sealed and
  reconciled evidence, with no new research and no invented number;
- **(B) `valuation_required`** — the field is inherently numeric (a target, a range, a maximum size)
  and no governed valuation methodology exists to support one; the future implementation must abstain
  explicitly rather than invent one;
- **(C) `cross_asset_framework_required`** — the field's honest answer depends on whole-portfolio
  architecture `XASSET-0001` requires but has not yet built (sleeve-level or instrument-level
  cross-asset synthesis); out of scope for an equity-only Milestone 8 entirely, not attempted
  per-ticker;
- **(D) `relationship_measurement_required`** — the field's answer is blocked, for a specific ticker,
  by that ticker's own `risk_concentration.unmeasured_flag`/`structural_measurement_gap` carried
  forward from Milestone 6/7;
- **(E) `evidence_refresh_required`-adjacent** — not a separate primary value (see §H) but a secondary
  condition (`unresolved_evidence`) attached alongside whichever primary value the evidence does
  support, never forcing abstention by itself;
- **(F) prohibited until later governance** — any content requiring a new tier-architecture design, a
  new correlated-cluster or issuer-look-through mechanism, a new numeric cap, or any directional
  buy/sell/hold/trim/wait/stage/sizing instruction. None of this is ever produced by Milestone 8, now
  or in its future implementation, without its own separate future governance decision.

This classification does not silently delete Milestone 8's purpose — every one of the eight named
areas (§A, §F) still receives a defined, governed treatment; several simply resolve, by design, to a
governed abstention rather than an invented conclusion.

### C. Permitted inputs

The future implementation may consume, for each of the 27 canonical equities:

1. **Milestone 7's reconciliation artifact** (`intelligence/reconciliation/
   MILESTONE7_BASELINE_RECONCILIATION.yaml`) as its **primary reconciliation input** — the future
   implementation must reuse Milestone 7's own `primary_disposition`, `secondary_conditions`,
   `role_comparison`, `capital_priority_comparison`, `target_context_comparison`, and structural/
   evidence-quality comparison fields directly (quoted or paraphrased faithfully, never
   re-derived from scratch) wherever an area's treatment class is (A);
2. **the 27 sealed Milestone 6 classification records** (`intelligence/classification/*.yaml`) as
   **traceable evidence** — read-only, cited for their `economic_role`, `capital_priority`,
   `risk_concentration`, and `evidence_quality` fields, never edited, never re-sealed, never
   reinterpreted differently than Milestone 7 already interpreted them;
3. current `targets.yaml` (`target_pct`, `caps.clusters` membership) and `gates.yaml` (gate status,
   `next_gate` text) as descriptive current-baseline context only — never a valuation input, never
   mutated;
4. `issuer_lookthrough.yaml` and the 13 sealed `intelligence/relationships/*.yaml` records, as
   structural/relationship evidence for area 6 (§G.6) only;
5. accepted Company and Theme Intelligence (`intelligence/companies/`, `intelligence/themes/`),
   including current `review.last_reviewed`/`next_due`/`log` fields, for area 7 (§G.7);
6. `holdings.yaml`, used only to describe factual current portfolio state (held, gated weight) —
   never to compute a target or size;
7. every controlling governance decision this file's `related_decisions` list cites or that any of
   them cites in turn.

**No new external research, no new Company/Theme Intelligence content, and no new
`intelligence/relationships/` record may be produced by the future implementation.** Every input above
is already-governed, already-accepted repository content as of this filing's own base commit.

### D. Prohibited inputs

The future implementation must not consume or be influenced by, under any circumstance:

- any chart evidence of any kind — raw images, filenames, manifests, coverage status, technical
  indicators, support/resistance levels, momentum or trend descriptions, technical interpretations,
  price-action conclusions, or any `CHART-0001`/`CHART-0002` evidence package
  (`governance/evidence/CHART-0001/`, `governance/evidence/CHART-0002/`) — restating, not narrowing or
  widening, `TIER-0003`'s Option A boundary (§F below);
- any ad hoc valuation calculation invented for this filing (a discounted-cash-flow estimate, a
  multiple, a price target, a technical price level, or any other numeric derivation not backed by a
  separately governed valuation architecture);
- any ungoverned external research (a live web search, a new primary-source fetch, or any fact not
  already present in an accepted repository record);
- any live or scenario `allocate.py`/`levels.py` output;
- any ungoverned ETF, crypto, GLD, reserve, or debt-reduction assumption (none of these five sleeve
  categories has a governed classification or doctrine framework yet — see §K);
- `intelligence/contenders/registry.yaml` (`CONTENDER-0002`) contender status treated as investment,
  research-priority, or policy authority — a registry disposition is inventory, not evidence of merit;
- raw ticker co-occurrence anywhere in repository text treated as relationship evidence — only a
  sealed `intelligence/relationships/*.yaml` record constitutes relationship evidence, per `REL-0001`
  §D, restated here without change.

### E. Equity-only boundary — binding, restated from `XASSET-0001` §H, not narrowed or widened

Every future Milestone 8 output must satisfy, without exception:

1. **All outputs are limited to the sealed 27-equity cohort.** No output addresses, references as
   settled, or implicitly assumes conclusions about any ETF, cryptocurrency, GLD/defensive asset,
   cash/reserve balance, or debt-reduction posture.
2. **No result represents whole-portfolio readiness.** Every artifact, summary, and individual finding
   must carry, verbatim or in substance, the disclosure statement `XASSET-0001` §B already requires of
   Milestone 7 and extends here to Milestone 8:

   > This recommendation package covers the 27 canonical equity destinations only. ETF,
   > cryptocurrency, cash/reserve, GLD/defensive-asset, debt-reduction, and broader
   > contender-universe policy remain governed separately and are not addressed or concluded here.

3. **No ETF, crypto, GLD, reserve, debt, or cross-sleeve recommendation is made** — treatment class
   (C), §B, applies to every such question; none is even attempted per-ticker.
4. **No final whole-portfolio target claim is permitted**, under any label, framing, or aggregation of
   equity-scoped findings.
5. **Later cross-asset work (`WS-0014`) may revise or supersede any equity-scoped Milestone 8
   conclusion** — nothing in a future Milestone 8 package is final or immune from later cross-asset
   reconciliation.
6. **`XASSET-0001` remains controlling** on every point above; this filing narrows or widens none of
   it, and no future Milestone 8 implementation may claim otherwise.

### F. Chart boundary — restated from `TIER-0003`, not reopened

1. **No chart evidence in Milestone 8**, in any form (§D).
2. **No technical-analysis conclusion of any kind** appears anywhere in a Milestone 8 output.
3. **No deployment-timing output** — Milestone 8 addresses portfolio-role, tier, capital-priority,
   overlap, monitoring, and review-discipline *policy*, never *when* to execute a trade.
4. **No chart-derived target or ranking.**
5. **Weekly/daily and any conditional 4H/1H chart work remains a separate, downstream deployment
   system** (`CHART-0001`/`CHART-0002`, and any future chart decision), governed entirely apart from
   Milestone 8 and never an input to it.
6. **Chart evidence may not automatically change membership, role, tier, target, cap, or
   recommendation** — restating, not narrowing or widening, `CHART-0001` §6/`CHART-0002`'s and
   `TIER-0003` §E's existing advisory-only boundary.

### G. The eight policy areas — treatment, permitted vocabulary, and evidence requirements

Each area below states: (1) whether a categorical recommendation is currently permitted; (2) whether
valuation is required; (3) whether cross-asset work is required; (4) whether relationship evidence is
required; (5) the allowed primary-status vocabulary (§H); (6) prohibited output; (7) evidence
requirements; (8) the later-adoption requirement. All eight areas are equity-scoped per §E and exclude
chart evidence per §F without further repetition below.

**G.1 — Portfolio/economic role.**
(1) Categorical permitted: **yes**, reused directly from Milestone 7's own `role_comparison` and
`primary_disposition` for that ticker — never independently re-derived. (2) Valuation: no. (3)
Cross-asset: no. (4) Relationship: no. (5) Allowed: `retain_current_baseline`, `review_warranted`,
`no_policy_conclusion` — mapped 1:1 from Milestone 7's ticker-level `primary_disposition`
(`aligned` → `retain_current_baseline`; `divergence_requires_review`/`baseline_assumption_stale` →
`review_warranted`; `no_policy_conclusion` → `no_policy_conclusion`). (6) Prohibited: any new
`economic_role` judgment not already present in the sealed Milestone 6 record or Milestone 7's
comparison; any numeric score. (7) Evidence: cite the sealed `economic_role` field and Milestone 7's
`role_comparison` field directly. (8) Later adoption: any actual `portfolio_role_ref` edit requires
Milestone 9 review and its own separate future governance decision.

**G.2 — Tier/replacement classification architecture.**
(1) Categorical permitted: **yes, narrowly** — bounded to whether the ticker's *current* tier/gate/
role treatment appears consistent with its reconciled Milestone 7 evidence. **Designing, proposing, or
implying any new tier definition, threshold, category, or replacement architecture is prohibited
outright** (treatment class F) — that is Milestone 5-adjacent architecture work (`TIER-0001`/
`TIER-0002`), already closed, and any future need for it surfaces only as `defer_pending_governance`,
never attempted here. (2) Valuation: no, for the consistency question; any architecture proposal would
require its own future governance regardless of valuation. (3) Cross-asset: no. (4) Relationship: no
directly. (5) Allowed: `retain_current_baseline`, `review_warranted`, `defer_pending_governance` (for
any request beyond consistency-checking), `no_policy_conclusion`. (6) Prohibited: any new tier
schema, threshold, or category of any kind; any content answering "what should the tier structure be"
rather than "is the current tier treatment consistent with reconciled evidence." (7) Evidence:
Milestone 7's `capital_priority_comparison` and `role_comparison`; current `gates.yaml`/
`portfolio_role_ref` state. (8) Later adoption: Milestone 9 review plus its own separate future
governance decision before any tier, gate, or role change; a genuine architecture redesign remains
entirely out of Milestone 8/9's scope.

**G.3 — Capital priority.**
(1) Categorical permitted: **yes**, reused directly from Milestone 6's sealed `capital_priority.status`
and Milestone 7's `capital_priority_comparison` for that ticker — never independently re-derived. (2)
Valuation: no — `capital_priority.status` is itself a non-numeric, closed-vocabulary field by
`TIER-0002`'s own design. (3) Cross-asset: **explicitly out of scope** — any cross-cohort capital-
priority ranking (comparing this ticker's priority against a non-equity sleeve, or against a candidate
outside the 27-name cohort) is prohibited (treatment class C); this area addresses only whether the
ticker's *equity-scoped* priority treatment is internally consistent. (4) Relationship: no directly.
(5) Allowed: `retain_current_baseline`, `review_warranted`, `no_policy_conclusion` — mapped 1:1 from
Milestone 7's ticker-level `primary_disposition`, identically to G.1. (6) Prohibited: any cross-cohort
or cross-sleeve capital-priority ranking; any numeric priority score. (7) Evidence: the sealed
`capital_priority` field and Milestone 7's `capital_priority_comparison` field directly. (8) Later
adoption: Milestone 9 review plus its own separate future governance decision before any actual
reallocation signal is derived from this area.

**G.4 — Targets/target ranges.**
(1) Categorical permitted: **no** — this is the first of two inherently numeric areas. (2) Valuation:
**always required.** (3) Cross-asset: also implicated (a final target requires whole-portfolio budget
context), but the primary status stays a single forced value — no per-ticker branching between (B) and
(C) for this area. (4) Relationship: not the blocking factor. (5) Allowed: **`valuation_required`
only**, for every one of the 27 tickers, with no exception — doctrinally fixed by this filing, not a
per-ticker judgment call for the future implementation to make. (6) Prohibited: any numeric target,
percentage, range, band, or interval of any kind, under any framing, for any ticker — mechanically
enforced by the future validator (§I). (7) Evidence: the rationale field must cite the absence of a
governed valuation methodology (this filing, §K) as the reason for abstention — not a ticker-specific
justification, since the abstention is universal by design. (8) Later adoption: a separately governed
valuation architecture (a named future workstream, §K) must exist before this area can ever produce
anything beyond `valuation_required`.

**G.5 — Maximum position size.**
Identical treatment to G.4 in every respect — (1) no categorical output, (2) valuation always
required, (3) cross-asset risk-budget context also implicated but does not change the forced primary
value, (4) not the blocking factor, (5) `valuation_required` only, (6)/(7)/(8) identical to G.4. Kept
as a separate area (not merged with G.4) because the controlling gate text (§A) and `OPS-0006` §4.8
name them separately, and a future valuation architecture may resolve one before the other.

**G.6 — Economic-system/overlap and concentration limits.**
(1) Categorical permitted: **yes, for the equity-scoped question only** — whether the ticker's current
`caps.clusters`/`issuer_lookthrough.yaml`/`intelligence/relationships/` coverage appears consistent
with Milestone 7's own structural-risk comparison. **The whole-portfolio (cross-sleeve) overlap
question — equity-vs-ETF, equity-vs-crypto, equity-vs-GLD, or any aggregate concentration measure
spanning more than the equity sleeve — is entirely out of scope and not attempted per-ticker**;
`XASSET-0001` §B's disclosure statement (§E.2 above) covers this at the artifact level, once, rather
than a per-ticker `cross_asset_framework_required` entry repeated 27 times for the same universal
gap. (2) Valuation: no. (3) Cross-asset: not attempted per-ticker (see above). (4) Relationship: **yes
— the blocking factor for this area specifically.** Any ticker carrying Milestone 7's
`structural_measurement_gap` secondary flag (the 11 names `REL-0007` and `TIER-0007`/`TIER-0008`
independently confirmed: SNPS, PANW, ISRG, TMO, ICE, SPGI, V, COST, WM, RTX, RKLB) is forced to
primary status `relationship_measurement_required` for this area — there is no governed cluster/
issuer/relationship coverage to compare against, so no categorical finding can responsibly be reached.
The remaining 16 names may receive a categorical finding. (5) Allowed: `retain_current_baseline`,
`review_warranted`, `relationship_measurement_required`, `no_policy_conclusion`. (6) Prohibited: any
cross-sleeve/whole-portfolio overlap claim of any kind; any new numeric cap, cluster, or concentration
limit. (7) Evidence: `targets.yaml` `caps.clusters`, `issuer_lookthrough.yaml`,
`intelligence/relationships/*.yaml`, and Milestone 7's structural-risk comparison fields, cited
directly. (8) Later adoption: whole-portfolio overlap modeling is `WS-0014`/`XASSET-0001` §F scope,
not Milestone 8 or 9; any equity-scoped cluster/cap change requires its own separate future governance
decision regardless.

**G.7 — Monitoring frequency and thesis-break review rules.**
(1) Categorical permitted: **yes**, derived from Milestone 6's `evidence_quality` axis, Milestone 7's
evidence-quality comparison, and each record's existing, already-governed
`review.cadence_days`/`last_reviewed`/`next_due`/`log` fields (Company Intelligence spec, `AUTO-0001`,
`PI-0011`) — this area asks only whether the *existing* monitoring cadence appears adequate given
disclosed evidence quality, never proposes a new cadence number. (2) Valuation: no. (3) Cross-asset:
no. (4) Relationship: no directly (an unresolved-evidence condition is captured as the secondary flag
`unresolved_evidence`, §H, not a separate primary value). (5) Allowed: `retain_current_baseline`,
`review_warranted`, `no_policy_conclusion`. (6) Prohibited: any proposed cadence number (e.g., a
specific day count); any declared thesis-break verdict — Milestone 8 may flag that a thesis-break
condition *appears* to warrant review, never declare a thesis actually broken, since that is a factual
determination this filing does not authorize Milestone 8 to make. (7) Evidence: `review.cadence_days`/
`next_due`/`log`, Milestone 6 `evidence_quality`, and Milestone 7's evidence-quality comparison field,
cited directly. (8) Later adoption: any actual cadence or thesis-status edit to a Company Intelligence
record requires its own separate action under the existing, unmodified Portfolio Intelligence
specification — not authorized by Milestone 8 or 9.

**G.8 — Add/hold/trim/exit-review discipline.**
(1) Categorical permitted: **yes, strictly bounded to whether a review-trigger mechanism exists and
appears adequate** — for the six gated names, whether `gates.yaml`'s own `next_gate` reopening
condition is defined and appears current; for the 21 non-gated names, whether a comparable
thesis-break/review trigger is disclosed in the Company Intelligence record. **This area never
produces an actual add, hold, trim, or exit action or recommendation of any kind, under any framing**
— it evaluates the existence and apparent adequacy of a review *mechanism*, never the position itself.
(2) Valuation: no, for the mechanism question; an actual trim/exit sizing decision would require
valuation and is out of scope entirely, permanently (see §J). (3) Cross-asset: no. (4) Relationship:
no directly. (5) Allowed: `retain_current_baseline` (a review mechanism exists and appears adequate;
no action of any kind is indicated or implied), `review_warranted` (the review-trigger mechanism
itself — not the position — should be examined, e.g., a non-gated name with no disclosed thesis-break
trigger), `no_policy_conclusion`. (6) Prohibited — **the hardest line in this filing**: the words
"buy," "sell," "add," "hold" (as a verb directing an action, distinct from the noun "holdings"),
"trim," "exit" (as a verb directing an action), "wait," "stage," or any sizing instruction must never
appear as an actual directive in this area's output, under any paraphrase; mechanically scanned by the
future validator (§I). (7) Evidence: `gates.yaml` `next_gate` text for the six gated names; Company
Intelligence `risks[]`/`catalysts[]`/thesis-break language already present in the existing record for
the 21 non-gated names. (8) Later adoption: any actual add/hold/trim/exit action requires manual
execution per this repository's permanent CLAUDE.md workflow (deposit-cycle-driven, human-executed on
Robinhood) and is never produced, recommended in directive form, or automated by any part of this
system — Milestone 8 and Milestone 9 do not change this, and no future decision may authorize an order
path without its own separate, explicit, and highly scrutinized governance action outside this
filing's own scope.

### H. Closed recommendation vocabulary — primary status plus secondary condition flags

Mirroring `TIER-0007` §H's already-accepted two-part design, applied per area-entry (§G), per ticker —
because a single flat category cannot honestly represent an area-entry that is evidence-supported on
its main question but still constrained by a disclosed gap.

**Primary status — exactly one per area-entry, closed, seven values:**

1. `retain_current_baseline` — the area-appropriate reconciled evidence supports no material change
   to current treatment. **This does not mean "approved," "optimal," "no future change," or an
   instruction to buy, add, or hold** — it states only that no material disagreement or gap was found
   on the evidence available for this specific area; it carries no policy or execution authority.
2. `review_warranted` — the area-appropriate reconciled evidence supports flagging this area for a
   future, separate policy review. **This is not itself the review, and it is never a directional
   buy/sell/trim/hold/wait/stage instruction** — it names that a closer look is warranted, not what
   the outcome of that look should be.
3. `valuation_required` — this area-entry is inherently numeric and no governed valuation methodology
   exists; doctrinally forced for G.4 and G.5 on every ticker (§G), never a per-ticker discretionary
   choice for those two areas.
4. `cross_asset_framework_required` — this area-entry's honest answer depends on whole-portfolio
   architecture `XASSET-0001` requires but has not built; per §E.3/§G.6, this value is not attempted
   per-ticker inside the 27-equity artifact — the equivalent gap is disclosed once at the artifact
   level instead. Retained in the closed vocabulary for completeness and for any future area
   extension, but **no G.1–G.8 per-ticker entry in this filing's authorized schema uses it** (see
   §I.3).
5. `relationship_measurement_required` — this area-entry's answer is blocked, for this specific
   ticker, by its own `risk_concentration.unmeasured_flag`/`structural_measurement_gap`; applicable
   only to G.6 (§G.6), for the 11 names currently so flagged.
6. `defer_pending_governance` — addressing this area-entry at all requires a specific, named future
   governance step beyond a valuation, cross-asset, or relationship gap (e.g., a genuine
   tier-architecture redesign, §G.2); the `later_governance_action` field (§I) must name that step.
7. `no_policy_conclusion` — use **only** when a specific attempt to apply values 1–6 fails for a
   reason recorded in the entry's `uncertainty` field. Not a default, not a catch-all for
   "insufficient time"; requires the same evidentiary rigor as the other six, applied to the negative
   conclusion that none of them can responsibly be reached.

**Precedence, deterministic, evaluated in this order:** for an area-entry whose treatment class is (A)
per §G (categorical currently permitted), evaluate value 1, then value 2; assign value 7 only if
neither can be responsibly supported. For an area-entry whose treatment class is (B)/(D) per §G
(G.4/G.5 always; G.6 for the 11 structurally-unmeasured names), the forced value (3 or 5
respectively) is assigned directly, with no attempt at 1/2 first — the doctrinal classification in §G
already establishes that no categorical answer is reachable for that area-entry, so attempting one
would not be "reaching a genuine conclusion," it would be inventing content §G already rules out.
Value 6 is used only where §G's own area-level text names it as reachable (currently: G.2 only, for
an architecture-redesign request specifically). Value 4 is reserved and unused in this filing's
authorized schema (§I.3).

**Secondary condition flags — closed, zero to two per area-entry, independent of primary status,
reusing `TIER-0007` §H's own vocabulary without redefinition:**

- `unresolved_evidence` — attach whenever an evidence limitation (per Milestone 6's `evidence_quality`
  axis or Milestone 7's own `unresolved_evidence` secondary flag for that ticker) materially
  constrains this specific area-entry, regardless of primary status. Never assigned in place of a
  reachable primary status; never causes a reachable primary status to be downgraded to
  `no_policy_conclusion`.
- `structural_measurement_gap` — attach whenever the ticker's own `risk_concentration.
  unmeasured_flag`/Milestone 7 `structural_measurement_gap` bears on this area-entry but does not,
  for this specific area, rise to blocking a reachable primary status (e.g., a role-comparison
  area-entry for an unmeasured ticker may still reach `retain_current_baseline` with this flag
  attached, since role is a different axis than structural overlap — contrast with G.6, where the
  identical gap *is* the blocking condition and forces primary status 5 directly).

A ticker's area-entry may carry zero, one, or both flags, in any combination with any of the seven
primary values (subject to §G's per-area restrictions on which primary values are reachable at all).
This vocabulary is closed — no new primary or secondary value without its own future governance
decision, matching `PI-0004`'s conviction-vocabulary and `TIER-0002`'s axis-vocabulary precedent. No
score, rank, or implied action priority is derived from or attached to any primary status, secondary
flag, or combination.

### I. Required per-ticker output schema and artifact architecture

The future implementation must authorize and deliver exactly one retained recommendation-package
artifact covering all 27 canonical equities (or one small set of logically partitioned artifacts —
never one PR per ticker), following the smallest production-quality structure this repository's
precedent already establishes (`TIER-0007`/PR #259's own structure, `TIER-0004`/`TIER-0005`'s sealing
discipline):

1. **One deterministic structured artifact**, `intelligence/recommendations/
   MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`, covering all 27 tickers in strict alphabetical
   order, no duplicate, no missing, no extra.
2. **One retained narrative audit** under `governance/audits/`, documenting methodology and
   area-by-area reasoning at a level a future reviewer can independently reproduce.
3. **One narrow validator**, `recommendation_validator.py`, zero import coupling with `allocate.py`/
   `margin_state.py`, enforcing: (a) a fully **closed schema** at the top level, per-ticker level, and
   per-area-entry level (no unknown key at any level — learning directly from the Milestone 6
   implementation's own corrected MAJOR finding on this exact defect, and from `TIER-0007`'s own
   corrected closed-schema design); (b) the exact seven-value primary vocabulary and two-value
   secondary vocabulary (§H), with deterministic precedence checked, not merely value-membership; (c)
   that G.4 and G.5 carry `primary_status: valuation_required` on **every** one of the 27 tickers,
   with no exception, mechanically verified — not left to per-ticker judgment; (d) that G.6 carries
   `primary_status: relationship_measurement_required` on exactly the 11 currently-flagged tickers and
   a categorical or `no_policy_conclusion` value on the remaining 16, cross-checked live against
   `targets.yaml`/`issuer_lookthrough.yaml`/`intelligence/relationships/` at validation time, not
   merely against the ticket's own Milestone 7 record (defense against silent drift, the same
   discipline `REL-0007` applied when it found `TIER-0002`'s own cached count stale); (e) a
   **forbidden-key/forbidden-phrase scan applied independently to every free-text field on every
   area-entry** — covering, at minimum, numeric-percent-shaped tokens, `proposed_target_pct`/
   `target_range`/`score`/`rank`/`recommendation` keys, the directive words listed in §G.8(6), and
   chart-derived terminology (raw indicator names, "support," "resistance," "breakout," "trend
   line," and equivalents) — **this validator must not repeat `reconciliation_validator.py`'s own
   disclosed MINOR defense-in-depth gap** (`TIER-0007`/`TIER-0008` §B.1: a self-declared
   `chart_evidence_used: false` flag enforced without an independent free-text scan for chart
   terminology) — the chart-terminology scan here is a first-class, independently-tested requirement,
   not deferred to a future correction; (f) the top-level `chart_evidence_used: false` flag, and
   independent verification that it is true; (g) the top-level equity-only disclosure statement (§E.2)
   present verbatim or in substance; (h) a recorded comparison-source `main` SHA (matching `TIER-0007`
   §C.6's discipline) and confirmation that the Milestone 7 artifact and all 27 sealed classification
   records are unchanged since their own respective sealing/acceptance commits.
4. **Focused tests**, `test_recommendation_validator.py`, covering every schema branch, every
   precedence rule, the G.4/G.5 forced-value check, the G.6 live-recomputation check, and the
   forbidden-phrase scan (including explicit negative tests proving each of the §G.8(6) directive
   words is caught).
5. **Minimum `operations/WORKSTREAMS.yaml`/`CLAUDE.md` synchronization** — one additive gate entry
   recording the implementation's own merge, no rewrite of this filing's own gate text, no rewrite of
   any Milestone 1–7 gate.
6. **One coherent implementation PR** — never one PR per ticker, matching every prior WS-0005
   milestone implementation's own precedent.

**Per-ticker top-level fields** (outside the eight area-entries):

- `ticker` (echo, alphabetical-order key);
- `milestone7_reference` — the ticker's own Milestone 7 `primary_disposition` and
  `secondary_conditions`, quoted or faithfully paraphrased, never reinterpreted;
- `policy_areas` — exactly eight keys (`role`, `tier_architecture`, `capital_priority`,
  `target_and_range`, `maximum_position_size`, `overlap_and_concentration`, `monitoring_and_
  thesis_break`, `add_hold_trim_exit_discipline`), each an area-entry object with: `primary_status`
  (§H, one of seven, area-restricted per §G), `secondary_conditions` (§H, zero to two), `rationale`
  (evidence-grounded, non-numeric except where directly quoting an existing `target_pct` as
  descriptive context per §C.3), `supporting_evidence` (citing specific fields/records, not restated
  conclusions), `later_governance_action` (a named future step, required whenever `primary_status` is
  not `retain_current_baseline`);
- `equity_scope_disclosure` — the §E.2 statement, present once per ticker or once at the artifact top
  level (implementation's choice, validator-enforced either way);
- `chart_evidence_used: false` (per-ticker or top-level, validator-enforced);
- `uncertainty` — what the package could not resolve for this ticker as a whole, required whenever any
  area-entry carries `no_policy_conclusion` or a secondary flag.

**Required top-level metadata**: schema version; governing decision (`TIER-0009`); comparison-source
`main` SHA; Milestone 6/7 sealing and completion references (`TIER-0006`, `TIER-0008`); generation
date; cohort size (27); `chart_evidence_used: false`; the §E.2 equity-only disclosure statement.

**Required aggregate reporting**: per-area, per-primary-value counts and ticker identity lists
(never merged across areas, never presented as a single portfolio-wide score); per-area,
per-secondary-flag counts; a cross-tabulation disclaimer stating explicitly that no count, list, or
combination constitutes a score, rank, or implied action priority — matching `TIER-0007` §I's own
disclaimer language, extended to eight areas instead of one disposition axis.

**Prohibited-key scanning**: the validator (§I.3.e) enforces this at the file level; additionally, the
retained narrative audit and the implementation PR's own body must themselves be free of numeric
target/range/score/rank language and of any G.8(6) directive word used as an actual instruction — the
same standard `TIER-0007`/`TIER-0008` applied to their own PR bodies.

**Completion-standard treatment**: this filing does **not** define a Milestone 8 completion standard.
Following the variability this repository's own precedent already establishes — `REL-0001` split
schema-freeze from `REL-0004`'s later completion-standard filing for Milestone 4, while `TIER-0006`/
`TIER-0007`(→`TIER-0008`) combined definition-and-evaluation in one filing per milestone step — a
Milestone 8 completion determination remains its own separate, later, independently-reviewed Lane G
filing, filed only after the future implementation PR this decision authorizes has merged. This filing
does not anticipate which pattern that later filing will follow.

### J. Explicit non-authorization

This filing and the future Milestone 8 implementation it authorizes must not, under any circumstance:

- automatically or otherwise change targets, target ranges, tiers, portfolio roles, gates, holdings,
  caps, clusters, issuer look-through, allocator logic, margin doctrine, or buy ladders;
- use chart evidence (§F);
- issue a buy, sell, hold (as a verb), trim, exit (as a verb), wait, stage, or sizing instruction of
  any kind, in any area, under any framing (§G.8(6));
- place or simulate an order;
- perform Milestone 9 (independent review and later adoption);
- execute a live or scenario allocation check (`allocate.py`/`levels.py` or any wrapper of it);
- edit any sealed Milestone 6 record, `COHORT_MANIFEST.yaml`, the Milestone 7 reconciliation artifact,
  any Company/Theme Intelligence record, or any `intelligence/relationships/` record;
- propose, estimate, imply, or backsolve a numeric target, target range, maximum position size, score,
  or rank of any kind (§G.4, §G.5, §H);
- conduct new external research, or create any new Company/Theme Intelligence or relationship record
  (§C);
- make any ETF, crypto, GLD, reserve, debt-reduction, or whole-portfolio recommendation of any kind
  (§E);
- design, propose, or imply a new tier-architecture, correlated-cluster, or issuer-look-through
  mechanism (§G.2, §G.6).

Milestone 8 may identify that a future policy review is warranted (`review_warranted`, §H); it cannot
decide what the new policy is, and it cannot act on the identification. That remains Milestone 9's
exclusively future, separately authorized scope — and even Milestone 9, per `XASSET-0001` §H, does not
by itself authorize adoption; any adoption requires its own separate accepted governance decision and a
later, separately authorized implementation PR.

### K. Valuation architecture — explicitly not designed here

This filing does **not** design, sketch, or gesture toward a specific future valuation methodology (a
DCF framework, a multiples-based approach, a technical price-target system, or any other). It states
only: (1) no such framework currently exists anywhere in this repository; (2) `G.4`/`G.5` are
doctrinally forced to `valuation_required` until one is separately proposed, researched, and accepted
through its own future governance decision, following the same bounded-charter discipline
`MARGIN-0005`/`LADDER-0001` already established for other numerically-consequential research
questions; (3) that future valuation architecture, whenever proposed, is not created, authorized, or
implied by this filing in any way — it is a distinct, unscoped, future workstream this filing
identifies as a prerequisite (§G.4/§G.5's own `later_governance_action`) without beginning it.

### L. Authorized future implementation unit

Exactly one later, separate, bounded Milestone 8 implementation PR is authorized, effective only after
**this** governance decision is independently reviewed, principal-accepted, merged, and post-merge
verified — matching `TIER-0007`/`REL-0001`/`LADDER-0001`/`CHART-0001`'s "future PR gated on this
governance decision's own merge" convention. That future PR must cover all 27 canonical equities in
one coherent retained recommendation-package artifact (or one small set of logically partitioned
artifacts — never one PR per ticker), following §G–§I's area treatment, closed vocabulary, precedence
design, and output schema exactly — no restatement, no loosening, no reintroduction of a numeric
target/range/size, no attempt at cross-asset content, no chart evidence. Internal read-only shards may
be used for drafting efficiency (matching Milestone 6's and Milestone 7's own shard patterns), but only
one primary authoring session may mutate the repository, and shard use must not be treated as authority
to skip §I.3's validator requirements or §C/§D's input boundary. The future implementation must
receive its own full validation, independent exact-head review under `OPS-0007` §1, any required
bounded correction and delta review, explicit principal exact-head acceptance, merge, and post-merge
verification — the complete lifecycle every prior WS-0005 milestone filing in this log has followed.
This authorization does not itself begin that work; nothing in §§B–K becomes operative for actual
recommendation content until the future PR exists, follows this specification, and completes its own
lifecycle.

`intelligence/classification/*.yaml`, `COHORT_MANIFEST.yaml`, `classification_validator.py`, the
sanitizer, `intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`,
`reconciliation_validator.py`, and `test_reconciliation_validator.py` are **not** touched by this
authorization or by the future implementation — the future PR adds one new recommendation-package
artifact and its own tests/validator/audit only where repository convention requires them; it does not
modify any existing Milestone 6 or Milestone 7 file.

### M. Milestone status and register synchronization performed by this filing

This filing does not itself perform any recommendation-package content and does not claim Milestone 8
work has begun. `operations/WORKSTREAMS.yaml`'s `milestone-8-policy-recommendation-package` gate's own
`status: proposed` is **unchanged** by this filing — matching `TIER-0007` §M's identical treatment of
the `milestone-7-baseline-reconciliation` gate and `REL-0001` §K's/`TIER-0001`'s identical treatment
of the Milestone 4/5 gates: this decision defines doctrine and authorizes one narrow future
implementation step; it does not flip the milestone itself to `in_progress`, since no recommendation
content exists yet. This filing's original commit adds one new, distinctly named, additive gate entry,
`tier0009-milestone8-policy-recommendation-framework-authorization`, `status: in_progress`, recording
exactly this authorization; a bounded follow-up commit sets that gate's own `pr:` field once the PR
exists, matching the `TIER-0003`/`TIER-0005`/`TIER-0007` precedent of recording the real PR number on
the self-tracking gate itself, not only on `WS-0005`'s top-level `active_pr` field.

This filing also folds in the routine Lane M post-merge factual synchronization for `TIER-0008`
(PR #260), disclosed as deferred by that PR's own post-merge-verification comment
(`issuecomment-5207710145`): a new `tier0008-post-merge-verification` gate records the independently
re-verified accepted head (`c7572aa0f8aa5fd552408bb4920c750a44fd2840`), merge commit
(`aed259994ea6aa2db08a24a3a1488ebcc39ca985`), and this filing's own disclosed merge-commit CI
infrastructure gap (§ Preflight) — matching the `tier0006-post-merge-verification`/
`tier0007-post-merge-verification` pattern used by every prior WS-0005 filing in this log. `WS-0005`'s
`active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date` self-reference fields are
updated to this filing's own live state (`active_pr` set to `null` until this filing's own PR number
exists, per `OPS-0001`'s convention — a bounded follow-up commit sets it once the PR is opened).
`WS-0005`'s top-level `status: in_progress`, `priority: primary`, `authorized_scope`, and
`prohibited_scope` are unchanged.

### N. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — two additive gate entries and the
self-reference fields, per §M); (4) `CLAUDE.md` (one concise Decisions Log pointer entry); (5)
`test_portfolio_hq_dashboard_decisions.py` (the two hardcoded decision-count assertions, 85 → 86). No
production code, no `intelligence/classification/`, `intelligence/reconciliation/`, or
`intelligence/relationships/` file, no `governance/audits/` artifact, no other workstream, and no
existing Company/Theme/relationship/classification/reconciliation record is touched.

### O. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (`OPS-0009` Lane G — a new governance authorization, full weight,
never reduced), complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This filing does not review
itself, mark itself ready, merge itself, or post principal acceptance. Nothing in §§A–N above becomes
effective, and the future Milestone 8 implementation unit in §L remains unauthorized to begin, until
this PR merges to `main`.

## Rationale

**Why the eight areas are sorted into treatment classes before any implementation begins.** Milestone
6's own lifecycle (`TIER-0001` through `TIER-0006`) and Milestone 7's own lifecycle (`TIER-0007`
through `TIER-0008`) repeatedly demonstrated that defining a milestone's evidence boundary and output
shape *before* authorizing content work catches defects a combined "define and execute" filing would
not — `TIER-0004`'s redaction specification surfaced a leak before any drafting began; `TIER-0007`'s
own first-round review caught a disposition-precedence gap and a gate-text-fidelity gap before any
comparison content existed. Milestone 8 carries a materially higher risk than either: it is the first
WS-0005 milestone whose own controlling gate text (§A) names outputs — numeric targets, maximum sizes
— that this repository has no governed methodology to produce. Sorting the eight areas into treatment
classes now, rather than leaving that judgment to whichever session drafts the future implementation,
removes the single largest risk in this milestone: a future session inventing a number under time
pressure because the gate text says "targets/target ranges" and no explicit doctrine stops it.

**Why the primary/secondary two-part vocabulary is reused, not redesigned.** `TIER-0007` §H already
solved, and this repository already accepted, the exact problem Milestone 8 also has: a single flat
category cannot honestly represent an entry that is evidence-supported on its main question but still
constrained by a disclosed gap. Reusing the same secondary-flag names (`unresolved_evidence`,
`structural_measurement_gap`) rather than inventing new ones for Milestone 8 keeps the underlying
evidence facts (which tickers are structurally unmeasured, which carry limited evidence) traceable
across Milestone 7 and Milestone 8 outputs without a translation layer that could itself introduce
drift.

**Why `cross_asset_framework_required` is retained in the vocabulary but unused in this filing's
authorized schema.** Removing it entirely would foreclose a future area extension (e.g., if Milestone
8's scope is ever widened by its own future governance decision to attempt a cross-asset-aware
finding for a specific area). Leaving it defined but stating explicitly that no G.1–G.8 entry
currently uses it (§H) avoids two failure modes at once: inventing a value with no defined use, and
silently permitting a future implementation to smuggle a cross-asset claim into a per-ticker entry
under a plausible-sounding label. The single artifact-level disclosure statement (§E.2) is the sole
sanctioned mechanism for surfacing the cross-asset gap.

**Why G.4/G.5 are doctrinally forced, not left to per-ticker judgment.** A per-ticker discretionary
choice between `valuation_required` and a categorical value for an inherently numeric area would
reproduce exactly the risk this filing exists to prevent — a future implementation session, faced with
27 tickers and time pressure, invents a plausible-sounding number for the "easy" cases and abstains
only for the "hard" ones, producing an artifact that looks disciplined but isn't. Fixing the answer for
every ticker, mechanically validator-enforced (§I.3.c), removes that discretion entirely.

**Why the chart-terminology scan is a first-class requirement here rather than deferred.**
`TIER-0007`/`TIER-0008` §B.1 disclosed, honestly and as non-blocking, that
`reconciliation_validator.py` enforces only the self-declared `chart_evidence_used` flag without an
independent free-text scan for chart terminology. That gap was accepted for Milestone 7 because two
independent reviewers separately confirmed the actual merged artifact was clean. Milestone 8 has not
yet been drafted — there is no equivalent independent confirmation available in advance. Building the
scan in from the start, rather than accepting the same disclosed gap a second time, is strictly
cheaper than discovering it after 27 tickers' worth of content exists.

## Alternatives Considered

**Perform the recommendation-package drafting in this same filing.** Rejected per explicit principal
instruction — the principal's own authorization draws the line at "define and authorize," not "define
and execute," mirroring `TIER-0007`'s identical split from its own future implementation. A single
filing that both designs the eight-area schema and populates it for 27 tickers would also make an
eligible independent reviewer's job materially harder, exactly as `TIER-0007`'s own Alternatives
section already reasoned for Milestone 7.

**Adopt the eight-value flat vocabulary suggested in the originating task brief
(`retain_current_baseline` / `review_role_or_priority` / `evidence_refresh_required` /
`relationship_measurement_required` / `valuation_required` / `cross_asset_framework_required` /
`defer_pending_governance` / `no_policy_conclusion`) verbatim, as a single per-ticker disposition.**
Considered, since it closely tracks `TIER-0007`'s own four-value primary/two-value-secondary split at
a glance. Rejected in favor of the per-area-entry design (§G–§I) because Milestone 8's controlling
gate text (§A) names eight *substantively different* policy questions per ticker, not one — collapsing
them into a single ticker-level disposition would either force one area's abstention to mask another
area's reachable categorical finding (exactly the failure mode the brief itself warns against: "prevent
uncertainty flags from replacing reachable primary conclusions") or require eight separate top-level
disposition fields with duplicated precedence logic. The per-area-entry structure reuses one shared
seven-value vocabulary and one shared precedence rule (§H) across all eight areas, while letting each
area's own §G treatment determine which subset of that vocabulary is reachable for it — achieving the
brief's own request for "a closer look at governing logic" over "mechanical adoption" without
multiplying vocabularies.

**Rename `review_warranted` to more closely match the brief's own `review_role_or_priority`
phrasing.** Considered. Rejected because the brief's phrasing is scoped to one area (roles/tier
architecture) but the same categorical "this deserves a closer look" finding is needed generically
across all eight areas (G.1 through G.8) — a name specific to one area's subject matter would read
oddly when reused for, e.g., G.7 (monitoring frequency). `review_warranted` is used uniformly instead,
with each area's own §G text supplying the subject-matter-specific meaning.

**Merge G.4 (targets/target ranges) and G.5 (maximum position size) into one area, since both are
identically treated (always `valuation_required`).** Considered. Rejected because `operations/
WORKSTREAMS.yaml`'s own controlling gate text (§A) and `OPS-0006` §4.8 name them as two distinct
items, and a future valuation architecture may resolve target-setting before position-sizing (or vice
versa) — keeping them as separate area-entries preserves the ability to selectively unlock one before
the other without a schema change.

**Attempt a per-ticker `cross_asset_framework_required` entry for G.6's whole-portfolio overlap
question, rather than a single artifact-level disclosure.** Considered, for symmetry with G.6's
own per-ticker `relationship_measurement_required` treatment. Rejected as redundant and
noise-generating: the whole-portfolio overlap gap applies identically and universally to all 27
tickers (none of them has governed cross-sleeve overlap data), so a per-ticker repetition of an
identical, universal fact adds file size without adding information — `XASSET-0001` §B's own single
artifact-level disclosure statement already exists and is reused here (§E.2) for exactly this purpose.

## Consequences

Once this filing merges, a future, separately authorized Milestone 8 implementation PR may begin,
bound to §§B–L's specification — including the eight-area treatment table (§G), the closed
primary/secondary vocabulary (§H), the doctrinally-forced G.4/G.5 abstention, and the equity-only and
chart boundaries (§E, §F), none of which may be loosened, restated, or replaced without its own future
governance decision. That future PR still requires its own full independent-review and
principal-acceptance lifecycle — this filing does not shorten or bypass any of it. Until that future PR
exists and completes its own lifecycle, no Milestone 8 recommendation-package content exists anywhere
in this repository; the 27 sealed Milestone 6 records and the Milestone 7 reconciliation artifact
remain exactly as `TIER-0006` and `TIER-0008` left them. `milestone-9-independent-review-and-later-
adoption` remains an untouched, unauthorized roadmap item — this filing does not advance it, and
completing a future Milestone 8 implementation would not by itself authorize Milestone 9. No current
portfolio policy or allocator behavior changes as a result of this decision, before or after its merge.
