---
decision_id: TIER-0011
date: 2026-08-07
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0004, PI-0011, PI-0016, PI-0031, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0008, TIER-0009, TIER-0010, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, OPS-0016, CONTENDER-0001, CONTENDER-0002, XASSET-0001]
supporting_artifact: null
file: governance/decisions/TIER-0011-ws0005-milestone9-independent-review-and-adoption-authorization.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1)
governance filing that **defines and authorizes** the future WS-0005 Milestone 9 ("Independent review
and later adoption," `OPS-0006` §4.9) implementation. This filing must not itself perform the
Milestone 9 review. It must define exactly what a future independent review may and must evaluate,
who is eligible to conduct it, what a review verdict may and may not conclude, and — critically — what
"later adoption" does and does not mean, given that Milestone 8 ("Policy recommendation package") is
now formally complete (`TIER-0010`, PR #263) and Milestone 9 is the last milestone `OPS-0006` §4 named.

`operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate already
carries controlling description text (quoted in full in §A below) — this filing binds a fuller
specification to that existing gate, the same "define, then later authorize implementation" pattern
`REL-0001` used for Milestone 4, `TIER-0001`/`TIER-0002` used for Milestone 5, `TIER-0007` used for
Milestone 7, and `TIER-0009` used for Milestone 8, rather than inventing new milestone scope.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/milestone-9-authorization-design-fqriuq`, working tree
  clean at session start and throughout.
- **`origin/main` fetched and reconciled.** `git fetch origin main` returned `up to date`;
  `git rev-parse origin/main` returned `64dbbee1a16768704169e8f1d8df49b4370d6eb3`, confirmed identical
  to this branch's own starting tip (`git merge-base --is-ancestor origin/main HEAD` succeeded) — this
  branch was created from a clean, current `main`, not a stale base.
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open`) —
  empty result. No competing mutation lane exists.
- **PR #263 (`TIER-0010`) independently re-confirmed merged** via the GitHub API: `merged: true`,
  `state: closed`, head `910caa4547627f505ddbae3115799a300cc2f437`, merge commit
  `64dbbee1a16768704169e8f1d8df49b4370d6eb3`, `merged_at: 2026-08-07`, 5 changed files, 2 commits —
  matching the session brief exactly. `main`'s current tip is exactly this merge commit.
- **`milestone-8-policy-recommendation-package` gate independently re-read** from live
  `operations/WORKSTREAMS.yaml`: `status: complete`, `pr: 262`, carrying `TIER-0010`'s own additive
  paragraph recording PR #262's accepted head, both review rounds, the bounded correction, principal
  acceptance (`issuecomment-5212688009`), post-merge verification (`issuecomment-5212728415`), and
  both exact-head and merge-commit CI success. **Milestone 8 is confirmed formally complete.**
- **`milestone-9-independent-review-and-later-adoption` gate text independently re-read**, quoted
  verbatim in §A below — unedited by any filing to date; `status: proposed`, `pr: null`, `date:
  "2026-07-25"` (the original `OPS-0006` roadmap date, predating any WS-0005 content work).
- **Decision catalog independently reconciled**: `governance/decisions.yaml` — exactly 87
  `decision_id` rows; `ls governance/decisions/*.md` (excluding `README.md`) — exactly 87 files;
  `portfolio_hq.dashboard.decisions.build_catalog('.')` — **87 decisions, `issues == ()`**. No
  `TIER-0011` reference exists anywhere in `governance/`, `operations/`, or `CLAUDE.md` prior to this
  filing (repository-wide grep, zero matches). The highest filed `TIER-####` is `TIER-0010` —
  **`TIER-0011` independently confirmed the next unused identifier**, continuing the same
  Milestone-5-through-9 `TIER-####` series `TIER-0001` began (Milestone 9 is the tier-architecture-
  review workstream's own final roadmap step, not a new decision domain — no new prefix is warranted).
- **Cumulative WS-0005 output this filing's future review will cover, independently counted live, not
  assumed**: 53 Company Intelligence records (`intelligence/companies/*.yaml`); 2 Theme Intelligence
  records (`intelligence/themes/*.yaml`); 13 sealed relationship records (`intelligence/
  relationships/*.yaml`, `REL-0002`/`REL-0003`/`REL-0005`, Milestone 4 complete per `REL-0006`); 27
  sealed blind-classification records (`intelligence/classification/*.yaml` excluding
  `COHORT_MANIFEST.yaml`, Milestone 6 complete per `TIER-0006`); one reconciliation artifact covering
  27 tickers (`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`, Milestone 7
  complete per `TIER-0008`); one recommendation-package artifact covering 27 tickers across 8 policy
  areas (`intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`, Milestone 8
  complete per `TIER-0010`); 84 contender-registry entries (`intelligence/contenders/registry.yaml`,
  `CONTENDER-0002`, a related but distinct WS-0014 deliverable, not itself a WS-0005 output — see §D.1
  for why it is cited as context only).
- **Zero allocator/margin coupling independently re-verified this session**, not merely cited from a
  prior filing: `grep -rn "import allocate\|from allocate\|import margin_state\|from margin_state"`
  across `classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
  `relationship_validator.py`, `intelligence_validator.py`, and `contender_registry_validator.py` —
  zero matches. `grep -n "intelligence/classification\|intelligence/reconciliation\|intelligence/
  recommendations\|intelligence/relationships"` across `allocate.py`, `margin_state.py`, and
  `levels.py` — zero matches. No WS-0005 output of any kind is read by, or coupled to, live allocator
  or margin logic as of this preflight.
- **`OPS-0007` §1 independently re-read in full** (the twelve-point capability-based independent-review
  standard). Point 4 records that `OPS-0006` §4 Milestone 9 originally named "Fable" specifically and
  that this was superseded — `milestone-9-independent-review-and-later-adoption`'s own current gate
  text (quoted §A) already reflects that supersession ("by an eligible reviewer per `OPS-0007` §1's
  capability-based standard").
- **`XASSET-0001` §H independently re-read in full.** It already binds three requirements this filing
  must not weaken: Milestone 7 is a bounded 27-equity reconciliation, not whole-portfolio optimality;
  Milestone 8 must label every finding equity-scoped and cannot claim whole-portfolio target readiness
  before `WS-0014`'s cross-asset work completes; and — directly on point for this filing —
  **"Milestone 9 does not silently convert equity-only findings into final whole-portfolio policy,"**
  and "an equity-scoped Milestone 8 package, even if independently reviewed and found sound under
  Milestone 9's standard, does not by itself constitute or authorize whole-portfolio policy adoption."
- **`OPS-0006` §§2-3 independently re-read in full** (the zero-based-research-discipline protocol this
  filing's §D.3 binds the future review to evaluating for adherence): baseline preserved for
  comparison only, never as evidence; research from first principles; conclusions formed independently
  before formal comparison; explicit comparison only at a dedicated reconciliation milestone; explicit
  agreement/disagreement record; no silent inheritance of an old classification; accepted history never
  erased.
- **`TIER-0003`'s chart-evidence boundary independently re-read in full.** Option A
  (fundamentals/business-evidence only) is binding on Milestone 6 blind classification and, per
  `TIER-0007` §E and `TIER-0009` §F, on Milestones 7 and 8 as well — neither reopened, narrowed, nor
  reinterpreted here.
- **No competing mutation lane or preserved uncommitted work** — working tree clean throughout; no
  stash, no untracked file, no other local branch carrying unpushed work found via `git branch -vv`
  and `git status --porcelain`.

No condition on this unit's own stop list was triggered by anything found above.

## Decision

### A. Milestone 9's controlling gate text (quoted, not restated as authority)

`operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate, unedited by
this filing beyond the additive record in §N:

> Independent review, by an eligible reviewer per OPS-0007 §1's capability-based standard (Fable
> remains eligible; any other reviewer meeting every §1 requirement is equally eligible), of research
> coverage, relationship methodology, zero-based protocol adherence, candidate tier architecture, the
> policy recommendation package, evidence-versus-judgment separation, and absence of hidden scoring or
> allocator coupling. Any adoption requires its own separate accepted governance decision and a later,
> separately authorized implementation PR. Not authorized to execute.

This filing binds a full specification to that text. Nothing below expands the gate's own subject
matter — it operationalizes exactly the seven review subjects already named, and takes at face value
the gate's own explicit, load-bearing sentence that adoption is not part of the review and requires its
own separate future authorization (§K).

### B. Purpose

Milestone 9 will produce exactly one thing: **one independent review of the cumulative WS-0005
Milestones 3-8 output**, evaluating it against the seven subjects named in §A. Milestone 9 is
**diagnostic, not adoptive.** It determines whether the underlying research, methodology, and
recommendation content are sound enough that a future, separate adoption decision could reasonably be
considered — it does not itself adopt anything, and a favorable verdict on every subject does not
change any tier, target, role, gate, holdings, cap, cluster, allocator, margin, or ladder value.

This is a structurally different milestone from every prior WS-0005 milestone this repository has
authorized. Milestones 3 through 8 each **produced new content** (Company Intelligence records,
relationship records, sealed classifications, a reconciliation artifact, a recommendation package).
Milestone 9 **produces no new investment-facing content of that kind** — it produces a review verdict
about content that already exists and is already complete. This filing's own structure follows that
difference: §D defines evaluation methodology per subject rather than a per-ticker output schema,
and §J defines a verdict vocabulary rather than a classification/disposition vocabulary.

### C. Reviewer eligibility

The future Milestone 9 review must be conducted by a reviewer satisfying `OPS-0007` §1's twelve-point
capability-based standard **in full, unweakened, cited by reference and not restated here.** This
filing adds exactly one Milestone-9-specific sharpening of `OPS-0007` §1 point 1 ("did not author or
edit the reviewed work"):

- **"The reviewed work," for Milestone 9 purposes, means the complete cumulative WS-0005 Milestones
  3-8 output** — every Company/Theme Intelligence record, every relationship record, all 27 sealed
  classification records, the reconciliation artifact, and the recommendation package, together with
  every governance decision that authorized or determined completion of any of them
  (`PI-0023`-`PI-0039`, `REL-0001`-`REL-0007`, `TIER-0001`-`TIER-0010`, and this filing itself once
  merged). A reviewer who authored, edited, corrected, or filed a completion determination for **any
  one** of these — not merely the single most recent PR — is not eligible, even if that reviewer did
  not touch the specific artifact under closest scrutiny in a given review pass. This closes a
  specific, non-hypothetical loophole: because dozens of prior WS-0005 filings were authored by Claude
  Code (Sonnet) sessions, a session that happens not to have authored the *most recent* PR could
  otherwise claim technical eligibility while having authored, e.g., the Milestone 6 sanitizer or the
  Milestone 7 disposition-precedence design under review. `OPS-0007` §1's own explicit restatement —
  "a Sonnet session may not independently approve work that the same Sonnet session authored" — is
  the operative principle; this filing applies it at the scope Milestone 9 actually requires: the
  whole reviewed body of work, not one PR.
- Fable remains eligible (unchanged from `OPS-0007` §1). Any other reviewer — a different model, a
  different session, a different platform — is equally eligible provided it independently satisfies
  every one of `OPS-0007` §1's twelve points, including retained attribution (point 9), severity
  classification (point 8), and explicit principal acceptance at the exact reviewed head (point 12).

### D. Evaluation methodology — the seven review subjects, mapped to concrete artifacts

Each of the seven subjects the controlling gate text (§A) names is operationalized below: what it
means, which artifacts constitute its evidence base, and what a reviewer must actually inspect —
never accept a prior filing's own self-description as a substitute for direct inspection.

**D.1 — Research coverage.**
Evaluate whether the 53 Company Intelligence records and 2 Theme Intelligence records provide adequate,
current, primary-source-grounded evidence for the 27 canonical equities Milestones 6-8 classified,
reconciled, and produced recommendations for. Required inspection: cross-check the 27-name canonical
population (`targets.yaml`) against Company Intelligence coverage (already independently confirmed
27/27 at Milestone 6/7/8 sealing — the reviewer must re-derive this, not merely cite it); spot-check
freshness (`review.last_reviewed`/`next_due`, `PI-0039`'s freshness-verification findings) for
material staleness since the last verification pass; confirm the six formerly-gated names' and LLY's
disclosed `limited`/`partial` evidence-access constraints (`PI-0038` §-disclosed WebFetch blockage)
are still accurately reflected, not silently upgraded. **`CONTENDER-0002`'s 84-entry registry is
context only, not a Milestone 9 review subject** — it inventories tickers system-wide (`WS-0014`
scope) and is explicitly barred from being treated as investment or research-priority evidence
(`TIER-0009` §D); the reviewer may cite it to confirm no covered ticker's disposition contradicts
Milestone 9's own scope, but must not extend the review into `WS-0014` territory.

**D.2 — Relationship methodology.**
Evaluate `REL-0001`'s frozen taxonomy (twelve primitive relationship types, directionality rules, the
claim-level evidence/abstention standard, the closed `decision_served` vocabulary) and its application
across the 13 sealed relationship records (`REL-0002`, `REL-0003`, `REL-0005`). Required inspection:
confirm every record's `evidence_classification` is honestly assigned (the corpus's own disclosed
pattern — every one of the 13 records carries `inferred`, never `observed`, because no counterparty
record independently corroborates the relationship — must be reproduced, not merely trusted);
independently re-derive the 11-name `structural_measurement_gap` set (SNPS, PANW, ISRG, TMO, ICE,
SPGI, V, COST, WM, RTX, RKLB) directly from `targets.yaml`/`issuer_lookthrough.yaml`/
`intelligence/relationships/` rather than copying it from a prior filing (matching the discipline
`REL-0007`, `TIER-0007`, `TIER-0008`, and this filing's own preflight already applied); confirm
`REL-0006`'s completion determination for Milestone 4 was itself independently reviewed and
principal-accepted, not merely asserted complete.

**D.3 — Zero-based protocol adherence.**
Evaluate whether Milestones 5-8 actually followed `OPS-0006` §§2-3's zero-based-research-discipline
protocol (independently re-read in full this session, §Preflight) rather than merely stating adherence.
Required inspection, at minimum: for Milestone 6, confirm the blind-drafting shard isolation actually
withheld `portfolio_role_ref`/`conviction`/`review.log` narrative and every policy-signaling term from
every drafting session — the concrete evidence trail is PR #253's own three-round correction history
(the original bare-noun-"gate" leakage, the tautological-verifier finding, and the dangling-
section-title-reference gap), which the reviewer must independently trace to confirm each defect was
genuinely root-cause-fixed and not merely patched around; for Milestone 7, confirm the sealed
classifications were compared against current baseline only *after* sealing (never the reverse) and
that no sealed record was edited during reconciliation (`TIER-0007` §C's integrity checks, §J's
no-retroactive-rewrite rule); for Milestone 8, confirm recommendation content reused Milestone 7's own
comparison fields rather than independently re-deriving a different conclusion from the same evidence
(`TIER-0009` §C.1's reuse requirement) except where §G.2's bounded consistency-check design explicitly
permits narrow additional reasoning, itself independently justified in the record (the `PI-0038`
gated-six correction round, §Preflight).

**D.4 — Candidate tier architecture.**
Evaluate `TIER-0001`/`TIER-0002`'s four-axis candidate classification framework (`economic_role`,
`capital_priority`, `risk_concentration`, `evidence_quality`) as a *design*, not only its application.
Required inspection: whether the four axes are the right axes (the framework design's own rejected
alternative — extending the frozen Company Intelligence schema directly — and its stated reasoning);
whether the closed vocabularies within each axis remain adequate given everything since observed
(e.g., whether the 17/9/1 `capital_priority` distribution corrected under Milestone 6's second bounded
correction reveals a vocabulary gap, or whether it is simply the corpus's honest shape); whether the
non-cascading abstention rule (`TIER-0004` §"one axis's uncertainty is never automatic grounds for
abstention on another") held in practice across all 27 records, including SPGI's own
`no_policy_conclusion` abstention.

**D.5 — The policy recommendation package.**
Evaluate the Milestone 8 artifact directly — all 27 tickers × 8 policy areas — against `TIER-0009`'s
own specification (§§G-I): the eight-area treatment-class sorting; the closed seven-value primary/
two-value secondary vocabulary and its deterministic precedence; the doctrinally-forced
`valuation_required` on G.4/G.5 for every one of the 27 tickers with zero exception; the live-
recomputed (not merely cached) 11-name structural-gap set on G.6; the complete absence of any numeric
target, range, maximum size, score, or rank anywhere in the artifact; the complete absence of any
directive add/hold/trim/exit/wait/stage language (`TIER-0009` §G.8(6)) under any framing. The reviewer
must independently re-run `recommendation_validator.py` and independently re-scan the artifact's own
free text for chart terminology and directive language — not rely on the validator's or a prior
filing's self-report alone.

**D.6 — Evidence-versus-judgment separation.**
Evaluate whether every claim across the full Milestones 3-8 output is labeled by its actual evidentiary
status — primary source, secondary source, inference, estimate, unresolved — rather than presented
uniformly as settled fact. Required inspection: `TIER-0007` §D's six-category labeling requirement
(blind-classification conclusion / current baseline policy / factual current portfolio state /
governing constraint / reconciliation analysis / unresolved evidence) as applied in the Milestone 7
artifact; `TIER-0009`'s equivalent evidence/rationale separation in the Milestone 8 artifact; whether
any Company Intelligence record's disclosed access limitation (the six formerly-gated names' and
LLY's WebFetch-blockage disclosures) was preserved through Milestones 6-8 rather than silently dropped
as the evidence moved further from its original source.

**D.7 — Absence of hidden scoring or allocator coupling.**
Evaluate, independently — not by trusting §Preflight's own findings above, which the reviewer must
reproduce rather than accept on faith — that: (a) no numeric score, weighted composite, or rank exists
anywhere in `intelligence/classification/`, `intelligence/reconciliation/`, or
`intelligence/recommendations/`; (b) zero import coupling exists between any WS-0005 validator
(`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`,
`relationship_validator.py`, `intelligence_validator.py`) and `allocate.py`/`margin_state.py`, in
either direction; (c) `allocate.py`, `margin_state.py`, and `levels.py` read none of
`intelligence/classification/`, `intelligence/reconciliation/`, `intelligence/recommendations/`, or
`intelligence/relationships/`; (d) no live or scenario allocation check anywhere in the Milestones 3-8
history consumed WS-0005 output as an input.

### E. Permitted review inputs

The future implementation may consume, read-only:

1. every artifact and record named in §D, in full;
2. every governing decision this file's `related_decisions` list cites or that any of them cites in
   turn;
3. `targets.yaml`, `gates.yaml`, `holdings.yaml`, `issuer_lookthrough.yaml`, and `caps.clusters`, as
   descriptive current-baseline context — the same permitted-input class `TIER-0007` §D and `TIER-0009`
   §C already establish, never a valuation or adoption input;
4. verification research — the reviewer may independently attempt to re-verify a load-bearing external
   factual claim already made somewhere in the reviewed corpus (`OPS-0007` §1 point 5), disclosing any
   source-access limitation encountered exactly as every prior review in this repository has;
5. the full repository test suite and every existing validator, run directly, not merely cited.

### F. Prohibited review inputs and actions

The future implementation must not, under any circumstance:

- create any new Company/Theme Intelligence record, relationship record, classification record,
  reconciliation entry, or recommendation-package entry — Milestones 3-8 are complete and sealed; a
  gap the review finds is a *finding*, named and disclosed, never silently filled by the review itself;
- edit any sealed Milestone 6 record, `COHORT_MANIFEST.yaml`, the Milestone 7 reconciliation artifact,
  the Milestone 8 recommendation-package artifact, any Company/Theme Intelligence record, or any
  relationship record — matching `TIER-0007` §J's no-retroactive-rewrite rule, extended here to every
  sealed WS-0005 artifact, not only Milestone 6's;
- use chart evidence of any kind — restating, not narrowing or widening, `TIER-0003`'s Option A
  boundary (§G below);
- conduct any ETF, crypto, GLD, reserve, or debt-reduction research, or any `WS-0014`/`XASSET-0001`
  cross-asset work — entirely out of scope (§H below);
- execute, simulate, or scenario-run `allocate.py`/`levels.py` or any wrapper of it;
- propose, estimate, imply, or backsolve any numeric target, target range, maximum position size,
  score, or rank of its own — the review evaluates whether the reviewed content avoided doing this; it
  must not itself do it while evaluating;
- issue a buy, sell, hold (as a verb), trim, exit (as a verb), wait, stage, or sizing instruction of
  any kind, in any finding, under any framing;
- perform, begin, or imply any adoption action of any kind (§K) — including editing
  `portfolio_role_ref`, `conviction.rating`, `target_pct`, any gate, any cap, any cluster, `holdings.yaml`,
  or any margin/allocator/ladder value, even where the review's own verdict is favorable;
- compute or publish a single aggregate "readiness score" across the seven subjects (§D) or across the
  27 tickers — the closed per-subject verdict vocabulary (§J) is the only sanctioned output shape,
  chosen specifically to prevent the kind of hidden scoring subject D.7 itself requires the review to
  rule out.

### G. Chart-evidence boundary — restated from `TIER-0003`, not reopened

No chart evidence in Milestone 9, in any form. No technical-analysis conclusion of any kind appears
anywhere in a Milestone 9 output. This restates, and does not narrow or widen, `TIER-0003`'s Option A
boundary and its extension through `TIER-0007` §E and `TIER-0009` §F.

### H. Equity-only and cross-asset boundary — restated from `XASSET-0001` §H, not narrowed or widened

The reviewed content (Milestones 3-8) covers the 27 canonical equity destinations only. The future
Milestone 9 review must:

1. evaluate the reviewed content strictly on its own equity-scoped terms — it does not, and cannot,
   certify whole-portfolio readiness, since no ETF, cryptocurrency, GLD/defensive-asset, cash/reserve,
   or debt-reduction classification or recommendation exists anywhere in the reviewed corpus;
2. carry, verbatim or in substance, in its own retained output: *"This review covers the 27 canonical
   equity destinations' Company/Theme/relationship Intelligence, blind classification, baseline
   reconciliation, and policy recommendation package only. ETF, cryptocurrency, cash/reserve, GLD/
   defensive-asset, debt-reduction, and broader contender-universe coverage remain governed separately
   under `WS-0014`/`XASSET-0001` and are not addressed or concluded here."*;
3. never state or imply that a favorable verdict on the equity-scoped review constitutes or authorizes
   whole-portfolio policy adoption — `XASSET-0001` §H's own text is controlling and is not reopened:
   "an equity-scoped Milestone 8 package, even if independently reviewed and found sound under
   Milestone 9's standard, does not by itself constitute or authorize whole-portfolio policy adoption."

### I. Reviewer disagreement with a prior WS-0005 finding

If the Milestone 9 reviewer disagrees with a conclusion reached inside any prior WS-0005 filing (a
Milestone 6 classification, a Milestone 7 comparison, a Milestone 8 recommendation), that disagreement
is itself a review finding (§J) — the reviewer states it, classifies its severity per `OPS-0007` §1
point 8, and names the required remediation. **The reviewer does not silently overrule, does not edit
the disputed record, and does not substitute its own judgment for the sealed record's judgment inside
the review artifact itself** — the sealed records are immutable evidence (§F), and any actual
correction to one of them requires its own separate governed process, per `TIER-0007` §C/§J's
already-established convention, extended here to every sealed WS-0005 artifact.

### J. Required review-output artifact and closed verdict vocabulary

The future implementation must authorize and deliver exactly one retained review artifact — either a
GitHub review/comment thread anchored to a specific commit head, or a verbatim `governance/audits/`
artifact, per `OPS-0007` §1 point 9's existing either/or standard — covering all seven subjects named
in §A/§D. For each subject, the review must record exactly one **primary verdict**, closed, four
values:

1. `sound_no_material_finding` — the subject was directly inspected per §D's methodology and no
   Blocking- or Major-equivalent finding (`OPS-0007` §1 point 8's severity scheme) was identified.
   **This does not mean "adopt," "approved," or "optimal"** — it states only that this subject
   presents no reviewed defect that would itself block a future, separate adoption decision from being
   considered; it carries no adoption authority of its own.
2. `material_finding_corrected` — a Blocking- or Major-equivalent finding was identified and resolved
   through a bounded correction within this same review cycle (`OPS-0007` §1 point 11), confirmed
   clean by an exact-head delta re-review. Use only when the correction is complete and re-verified,
   not merely proposed.
3. `material_finding_unresolved` — a Blocking- or Major-equivalent finding was identified that cannot
   be resolved by a bounded correction inside this review (a structural gap requiring new content
   generation, a new governance decision, or work outside Milestone 9's own scope). The review must
   name the specific required remediation and which future governance step it belongs to (e.g., "a
   new company batch," "a `WS-0014` cross-asset unit," "a future valuation-architecture charter") —
   without performing that remediation itself.
4. `not_evaluable_scope_limitation` — the reviewer could not reach a verdict on this subject because of
   a disclosed access, evidence, or scope limitation (`OPS-0007` §1 point 5) — an honest abstention,
   not a default, and not interchangeable with either of the other three values.

No fifth value, no numeric score, no weighted average across the seven subjects, and no single
aggregate "readiness" figure of any kind — the seven per-subject verdicts, together with their
supporting findings, are the complete and only sanctioned output. This vocabulary is closed — no new
value without its own future governance decision, matching `PI-0004`'s conviction-vocabulary,
`TIER-0002`'s axis-vocabulary, and `TIER-0007` §H's disposition-vocabulary precedent.

Required per-subject fields: `subject` (one of the seven named in §A); `primary_verdict` (§J, one of
four); `findings` (zero or more, each carrying a severity classification per `OPS-0007` §1 point 8, a
description, the specific artifact/field it concerns, and — for `material_finding_corrected` — the
correction applied and the re-review confirming it); `evidence_inspected` (the specific artifacts,
commits, or live command output the reviewer actually ran or read — not a restated citation to a prior
filing's own self-description); `required_remediation` (named, non-empty, whenever `primary_verdict`
is `material_finding_unresolved`).

Required top-level metadata: reviewing model/session identifier and eligibility confirmation (§C);
exact commit head reviewed; date; the §H equity-only/cross-asset disclosure statement; an explicit
statement that this review is diagnostic only and performs no adoption action (§K); a list of every
artifact and commit actually inspected.

### K. Adoption boundary — the controlling constraint of this entire filing

**Milestone 9's review, however favorable, is not adoption and does not authorize adoption.** This is
not a discretionary design choice this filing is making — it is the controlling gate text's (§A) own
explicit, load-bearing sentence: "Any adoption requires its own separate accepted governance decision
and a later, separately authorized implementation PR." This filing operationalizes that sentence
without narrowing or loosening it in any way:

1. **The future Milestone 9 review implementation authorized by this filing produces a review verdict
   only (§J).** It does not itself constitute, propose, draft, or pre-approve any adoption decision,
   even where every one of the seven subjects reaches `sound_no_material_finding`.
2. **"Adoption" means any action that changes live portfolio-governing state on the strength of
   Milestone 8's recommendation content** — including, without limitation: editing a
   `portfolio_role_ref` or `conviction.rating` field; changing a `target_pct`, a cluster-cap
   configuration, an issuer-look-through entry, a gate's status or `next_gate` text; changing
   `holdings.yaml`; changing any allocator, margin, or buy-ladder logic or parameter; or acting on any
   `review_warranted`/`divergence_requires_review`/`baseline_assumption_stale` finding as if it were
   itself an instruction.
3. **Every such adoption action requires its own separate, future, explicit governance decision —
   with its own decision identifier, its own independent Lane G review under `OPS-0007` §1, and its
   own explicit principal acceptance — plus its own separate, future, bounded implementation PR.** No
   such decision is pre-named, pre-numbered, pre-scoped, or pre-authorized by this filing. A future
   adoption decision may address one finding, several, or none, at the principal's own discretion; this
   filing creates no obligation, expectation, or schedule for when or whether adoption occurs.
4. **A future Milestone 9 completion determination (§N) — confirming the review itself was properly
   conducted and closing WS-0005's own `milestone-9-independent-review-and-later-adoption` gate,
   matching the `PI-0031`→`PI-0037`/`REL-0001`→`REL-0006`/`TIER-0007`→`TIER-0008`/`TIER-0009`→
   `TIER-0010` precedent — likewise does not authorize adoption.** Closing WS-0005's own nine-milestone
   roadmap (`OPS-0006` §4) is a distinct event from adopting any of the content that roadmap produced.
   `OPS-0006`'s own original roadmap text never numbered adoption as a milestone at all — it ended at
   "independent... review before any adoption," treating adoption as a distinct, indefinitely deferred
   future action outside the numbered sequence. This filing preserves that structure exactly.
5. **This filing itself authorizes no adoption action of any kind** — neither directly nor through any
   future implementation it authorizes.

### L. Explicit non-authorization

This filing and the future Milestone 9 review implementation it authorizes must not, under any
circumstance:

- adopt, propose adopting, or take any step toward adopting any Milestone 8 finding (§K);
- automatically or otherwise change targets, target ranges, tiers, portfolio roles, gates, holdings,
  caps, clusters, issuer look-through, allocator logic, margin doctrine, or buy ladders;
- use chart evidence (§G);
- conduct ETF, crypto, GLD, reserve, debt-reduction, or cross-asset research or classification of any
  kind (§H);
- create any new Company/Theme Intelligence record, relationship record, classification record, or
  recommendation-package entry (§F);
- edit any sealed Milestone 6, 7, or 8 artifact, or any Company/Theme/relationship Intelligence record
  (§F, §I);
- issue a buy, sell, hold (as a verb), trim, exit (as a verb), wait, stage, or sizing instruction of
  any kind, in any finding, under any framing;
- place or simulate an order;
- execute a live or scenario allocation check (`allocate.py`/`levels.py` or any wrapper of it);
- compute or publish a single aggregate readiness score across the seven subjects or across the 27
  tickers (§J);
- authorize, imply, or schedule a tenth WS-0005 milestone — `OPS-0006` §4 named exactly nine, and this
  filing neither adds a tenth nor treats Milestone 9's own completion as automatically producing one.

### M. Authorized future implementation unit

Exactly one later, separate, bounded Milestone 9 review is authorized, effective only after **this**
governance decision is independently reviewed, principal-accepted, merged, and post-merge verified —
matching `TIER-0007`/`TIER-0009`/`REL-0001`/`LADDER-0001`/`CHART-0001`'s "future work gated on this
governance decision's own merge" convention. That future review must satisfy §C's reviewer-eligibility
standard, cover all seven subjects per §D's methodology, respect §E-§I's input and boundary
constraints, and deliver §J's required review-output artifact using §J's closed verdict vocabulary —
no restatement, no loosening, no invented eighth subject, no numeric scoring. The future review must
receive its own full validation (re-running every applicable validator and the full test suite,
independently, not merely citing a prior filing's results), its own retained attribution per §J, and
explicit principal acceptance at its own exact head, per `OPS-0007` §1's twelve points in full. This
authorization does not itself begin that work; nothing in §§B-L becomes operative for actual review
content until the future review exists, follows this specification, and completes its own lifecycle.

No sealed Milestone 6, 7, or 8 artifact, `COHORT_MANIFEST.yaml`, `classification_validator.py`,
`reconciliation_validator.py`, `recommendation_validator.py`, the sanitizer, or any Company/Theme/
relationship Intelligence record is touched by this authorization or by the future review — the
future review adds one new review artifact only, under `governance/audits/` or as a retained GitHub
review, and does not modify any existing WS-0005 file.

### N. Milestone status and register synchronization performed by this filing

This filing does not itself perform any review and does not claim Milestone 9 work has begun.
`operations/WORKSTREAMS.yaml`'s `milestone-9-independent-review-and-later-adoption` gate's own
`status: proposed` is **unchanged** by this filing — matching `TIER-0007` §M's and `TIER-0009` §M's
identical treatment of the `milestone-7-baseline-reconciliation` and `milestone-8-policy-
recommendation-package` gates: this decision defines doctrine and authorizes one narrow future
implementation step; it does not flip the milestone itself to `in_progress`, since no review content
exists yet. This filing's original commit adds one new, distinctly named, additive gate entry,
`tier0011-milestone9-independent-review-and-adoption-authorization`, `status: in_progress`, recording
exactly this authorization; a bounded follow-up commit sets that gate's own `pr:` field once the PR
exists, matching the `TIER-0003`/`TIER-0005`/`TIER-0007`/`TIER-0009` precedent of recording the real
PR number on the self-tracking gate itself, not only on `WS-0005`'s top-level `active_pr` field.

This filing also folds in the routine Lane M post-merge factual synchronization for `TIER-0010`
(PR #263), matching the `tier0006-post-merge-verification`/`tier0007-post-merge-verification`/
`tier0008-post-merge-verification` pattern used by every prior WS-0005 filing in this log: a new
`tier0010-post-merge-verification` gate records the independently re-verified accepted head
(`910caa4547627f505ddbae3115799a300cc2f437`), merge commit
(`64dbbee1a16768704169e8f1d8df49b4370d6eb3`), independent review (`4879786313`, APPROVED FOR PRINCIPAL
EXACT-HEAD ACCEPTANCE, 0/0/0/0), principal acceptance (`issuecomment-5212688009`), post-merge
verification (`issuecomment-5212728415`), and both exact-head and merge-commit CI success
(`92757721969`/`31143369532`, `92776874235`/`31149785644`). `WS-0005`'s `active_branch`/`active_pr`/
`last_verified_main_sha`/`last_verified_date` self-reference fields are updated to this filing's own
live state (`active_pr` set to `null` until this filing's own PR number exists, per `OPS-0001`'s
convention — a bounded follow-up commit sets it once the PR is opened). `WS-0005`'s top-level `status:
in_progress`, `priority: primary`, `authorized_scope`, and `prohibited_scope` are unchanged.

### O. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) `governance/decisions.yaml` (one new index
row); (3) `operations/WORKSTREAMS.yaml` (`WS-0005` only — two additive gate entries and the
self-reference fields, per §N); (4) `CLAUDE.md` (one concise Decisions Log pointer entry); (5)
`test_portfolio_hq_dashboard_decisions.py` (the two hardcoded decision-count assertions, 87 → 88). No
production code, no `intelligence/classification/`, `intelligence/reconciliation/`,
`intelligence/recommendations/`, `intelligence/relationships/`, or `intelligence/companies/`/
`intelligence/themes/` file, no `governance/audits/` artifact, no other workstream, and no existing
Company/Theme/relationship/classification/reconciliation/recommendation record is touched.

### P. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (`OPS-0009` Lane G — a new governance authorization, full weight,
never reduced), complete any required bounded correction and exact-head re-review, and receive
explicit principal acceptance before it may be marked ready or merged. This filing does not review
itself, mark itself ready, merge itself, or post principal acceptance. Nothing in §§A-O above becomes
effective, and the future Milestone 9 review unit in §M remains unauthorized to begin, until this PR
merges to `main`.

## Rationale

**Why Milestone 9 needs a structurally different specification than Milestones 5-8.** Every prior
WS-0005 milestone authorization in this log (`TIER-0001`/`TIER-0002` for Milestone 5, `TIER-0005` for
Milestone 6, `TIER-0007` for Milestone 7, `TIER-0009` for Milestone 8) defined a per-ticker output
schema for new content the milestone would generate. Milestone 9 generates no new investment-facing
content — its own controlling gate text (§A) describes a review of content that already exists. Reusing
the per-ticker-schema pattern here would misfit the actual task and risk smuggling in exactly the kind
of hidden scoring subject D.7 requires the review to rule out (a per-ticker "verdict" across 27 tickers
would read uncomfortably like the numeric ranking this entire governance architecture has repeatedly
declined to build). The per-subject verdict design (§J) fits the actual shape of the gate text's seven
named subjects instead.

**Why the adoption boundary (§K) is this filing's controlling section, not an afterthought.** The
controlling gate text's own sentence — "Any adoption requires its own separate accepted governance
decision and a later, separately authorized implementation PR" — is doing real work: without it,
Milestone 9's own completion could be misread as sufficient authority to act on Milestone 8's
`review_warranted` findings. `XASSET-0001` §H already anticipated exactly this risk for the
equity-vs-whole-portfolio dimension ("Milestone 9 does not silently convert equity-only findings into
final whole-portfolio policy"); this filing generalizes the same discipline to the review-vs-adoption
dimension for the equity-scoped findings themselves, closing both directions of the same risk rather
than only the one `XASSET-0001` already named.

**Why reviewer eligibility is sharpened beyond `OPS-0007` §1's literal text (§C).** `OPS-0007` §1
point 1 was written and has been applied, in every prior WS-0005 filing, at single-PR scope — did the
reviewer author *this* PR. Milestone 9 is the first review whose subject is not one PR but an entire
multi-month, multi-filing body of work. Applying the literal single-PR reading would let a reviewer who
authored, say, the Milestone 6 sanitizer but not the Milestone 8 recommendation package claim
eligibility to review the whole corpus including the sanitizer's own design soundness (subject D.4/
D.3) — precisely the self-review risk `OPS-0007` §1 exists to prevent, just missed by a literal
single-PR reading. Naming the reviewed work's actual scope explicitly closes this before any future
review session could exploit the ambiguity, the same anticipatory-defect-catching discipline
`TIER-0004`'s redaction specification and `TIER-0009`'s chart-terminology scan already demonstrated is
cheaper than discovering the gap after review content exists.

**Why the verdict vocabulary is four values, not the eight-area/seven-value shape `TIER-0009` used.**
Milestone 8's eight areas each needed a value expressing *why* a categorical answer wasn't reachable
(valuation-required, cross-asset-required, relationship-required, and so on) because those reasons
were structurally different from each other and each pointed to a different future prerequisite.
Milestone 9's seven subjects don't have that structure — a review finding is either sound, correctable
now, correctable only later, or not evaluable given a disclosed limitation. Reusing `TIER-0009`'s
richer vocabulary here would import distinctions Milestone 9 doesn't need and risks obscuring the
review's own central finding (is this subject actually sound) behind machinery built for a different
problem.

## Alternatives Considered

**Perform the Milestone 9 review in this same filing.** Rejected per explicit principal instruction —
the task brief draws the line at "authorization/design filing... Do NOT perform the Milestone 9 review
itself," mirroring `TIER-0007`'s and `TIER-0009`'s identical split from their own future
implementations. A single filing that both designs the review methodology and performs it would also
make an eligible independent reviewer's job of reviewing *this* filing materially harder, since it
would need to evaluate both the specification's soundness and 3-8 milestones' worth of review content
at once.

**Treat Milestone 9's completion as itself authorizing adoption of every `sound_no_material_finding`
subject.** Considered, since it would shorten the roadmap by one governance cycle. Rejected outright —
this directly contradicts the controlling gate text's own explicit sentence (§A, §K) and would
convert a diagnostic milestone into an adoption milestone without the principal ever having separately
authorized that conversion. `OPS-0006`'s own original roadmap deliberately stopped at "independent
review... before any adoption" and never numbered adoption as a step — collapsing the two would erase
a distinction the roadmap's own author drew on purpose.

**Number a "Milestone 10: Adoption" now, to give the eventual adoption work a home in the existing
roadmap.** Considered. Rejected: `OPS-0006` §4 named exactly nine milestones, and adding a tenth is
itself a scope expansion this filing's own principal authorization does not cover ("define and
authorize... Milestone 9... only"). Leaving adoption unnumbered and indefinitely deferred, gated behind
"its own separate accepted governance decision" exactly as the controlling text already states,
preserves the existing roadmap's own boundary rather than quietly extending it.

**Adopt a five- or six-value verdict vocabulary, adding e.g. `finding_advisory_only` (a non-blocking
observation not rising to Major) as a fifth value.** Considered, since `OPS-0007` §1 point 8's own
severity scheme includes an "Advisory" tier below Minor. Rejected as unnecessary: `findings` (§J) is
already a list, and an advisory-level observation can be recorded there under a primary verdict of
`sound_no_material_finding` (which explicitly permits recorded findings — only Blocking/Major-
equivalent findings drive the vocabulary's other three values) without needing its own primary-verdict
value. Keeping the primary-verdict vocabulary at four values matches the corresponding severity
threshold every prior WS-0005 filing's own correction history has actually used to trigger a bounded
correction (Blocking/Major only) and avoids proliferating values for a distinction the `findings` list
already carries.

## Consequences

Once this filing merges, a future, separately authorized Milestone 9 review may begin, bound to
§§B-M's specification — including the seven-subject evaluation methodology (§D), the sharpened
reviewer-eligibility standard (§C), the closed four-value verdict vocabulary (§J), and, above all, the
adoption boundary (§K), none of which may be loosened, restated, or bypassed without its own future
governance decision. That future review still requires its own full independent-review and
principal-acceptance lifecycle under `OPS-0007` §1 — this filing does not shorten or bypass any of it.
Until that future review exists and completes its own lifecycle, no Milestone 9 review content exists
anywhere in this repository; the 27 sealed Milestone 6 records, the Milestone 7 reconciliation
artifact, and the Milestone 8 recommendation package remain exactly as `TIER-0006`, `TIER-0008`, and
`TIER-0010` left them. Even after a future Milestone 9 review completes and a future, separate
completion-determination filing closes WS-0005's own `milestone-9-independent-review-and-later-
adoption` gate, **no adoption of any Milestone 8 finding occurs automatically** — every such adoption
remains its own separate, future, explicitly authorized governance decision and implementation PR,
with no schedule, obligation, or presumption created by this filing, by the future Milestone 9 review,
or by that future completion determination. No current portfolio policy or allocator behavior changes
as a result of this decision, before or after its merge.
