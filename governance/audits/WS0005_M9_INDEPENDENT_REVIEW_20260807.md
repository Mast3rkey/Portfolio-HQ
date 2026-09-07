# WS-0005 Milestone 9 — Independent Review (retained record)

**Retained:** 2026-08-07
**Authority for this review's specification:** `governance/decisions/TIER-0011-ws0005-milestone9-independent-review-and-adoption-authorization.md` (merged, PR #264, merge commit `37c1cb45fc05de525752ee74c93fce84a3cfd688`).
**This artifact is retention only.** It is not itself a review — it is the verbatim-in-substance record of a completed independent review, transcribed here per `TIER-0011` §J's either/or retention standard (a verbatim `governance/audits/` artifact, in lieu of a GitHub review thread). No finding below was reached, re-derived, upgraded, downgraded, or newly judged by the session that authored this recording — see "Retention provenance and scope" below for exactly what that means and does not mean.

## Top-level metadata (TIER-0011 §J)

| Field | Value |
|---|---|
| Reviewing session | WS-0005 Milestone 9 Independent Review — a separate, independent, read-only session distinct from the session that authored this retention artifact and distinct from every prior WS-0005 Milestones 3-8 authorship/correction/completion-determination session, per `TIER-0011` §C's sharpened eligibility standard (see "Reviewer eligibility" below) |
| Exact commit head reviewed | `37c1cb45fc05de525752ee74c93fce84a3cfd688` |
| Date | 2026-08-07 |
| Review made repository mutations? | No — zero repository mutations, confirmed read-only |
| Diagnostic-only / no-adoption statement (`TIER-0011` §K) | **This review is diagnostic only. It performs no adoption action. A favorable verdict on any or all of the seven subjects below does not change, and must not be read as authorizing a change to, any `portfolio_role_ref`, `conviction.rating`, `target_pct`, gate, cap, cluster, `holdings.yaml`, allocator, margin, or ladder value. Any adoption of any finding below requires its own separate, future, explicit governance decision and implementation PR, per `TIER-0011` §K in full.** |
| Equity-only / cross-asset disclosure (`TIER-0011` §H.2, quoted verbatim) | "This review covers the 27 canonical equity destinations' Company/Theme/relationship Intelligence, blind classification, baseline reconciliation, and policy recommendation package only. ETF, cryptocurrency, cash/reserve, GLD/defensive-asset, debt-reduction, and broader contender-universe coverage remain governed separately under `WS-0014`/`XASSET-0001` and are not addressed or concluded here." |
| Overall conclusion | **EQUITY PACKAGE INTERNALLY SOUND FOR LATER ADOPTION CONSIDERATION** |

### Reviewer eligibility (`TIER-0011` §C)

The reviewing session is reported, by the review itself, as a fresh, read-only session that made zero repository mutations — satisfying `TIER-0011` §C's sharpened standard that "the reviewed work" for Milestone 9 purposes means the complete cumulative WS-0005 Milestones 3-8 output (not merely the most recent PR), and that a session which authored, edited, corrected, or filed a completion determination for any one of that cumulative output is ineligible. This retention artifact records that eligibility exactly as reported and does not independently re-derive or re-audit it — re-deriving reviewer eligibility from scratch would itself be new judgment, which this retention filing is scoped not to perform.

### Artifacts and scope in evidence (`TIER-0011` §D / §Preflight population, independently confirmed current by this retention session as of the reviewed head)

- 53 Company Intelligence records (`intelligence/companies/*.yaml`)
- 2 Theme Intelligence records (`intelligence/themes/*.yaml`)
- 13 sealed relationship records (`intelligence/relationships/*.yaml`; Milestone 4, complete per `REL-0006`)
- 27 sealed blind-classification records plus `COHORT_MANIFEST.yaml` (`intelligence/classification/`; Milestone 6, complete per `TIER-0006`)
- 1 reconciliation artifact covering 27 tickers (`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`; Milestone 7, complete per `TIER-0008`)
- 1 recommendation-package artifact covering 27 tickers across 8 policy areas (`intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`; Milestone 8, complete per `TIER-0010`)
- The governing decisions authorizing or determining completion of each of the above (`PI-0023`-`PI-0039`, `REL-0001`-`REL-0007`, `TIER-0001`-`TIER-0011`)
- `classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`, `relationship_validator.py`, `intelligence_validator.py`, `freshness_validator.py`, and the full repository test suite

`intelligence/contenders/registry.yaml` (`CONTENDER-0002`, `WS-0014`) is cited by the review as context only, per `TIER-0011` §D.1 — not itself a Milestone 9 review subject and not treated as investment or research-priority evidence.

## Seven subject verdicts (`TIER-0011` §A / §D / §J)

| # | Subject (`TIER-0011` §A) | Primary verdict (`TIER-0011` §J, closed 4-value) |
|---|---|---|
| 1 | Research coverage and provenance | `sound_no_material_finding` |
| 2 | Relationship methodology | `sound_no_material_finding` |
| 3 | Zero-based protocol adherence | `sound_no_material_finding` |
| 4 | Candidate tier architecture | `sound_no_material_finding` |
| 5 | Policy recommendation package | `sound_no_material_finding` |
| 6 | Evidence-versus-judgment separation | `sound_no_material_finding` |
| 7 | Absence of hidden scoring or allocator coupling | `sound_no_material_finding` |

No subject reached `material_finding_corrected`, `material_finding_unresolved`, or `not_evaluable_scope_limitation`. Per `TIER-0011` §J point 1, `sound_no_material_finding` "does not mean 'adopt,' 'approved,' or 'optimal'" — it states only that the subject presents no reviewed Blocking- or Major-equivalent defect that would itself block a future, separate adoption decision from being considered; it carries no adoption authority of its own. `sound_no_material_finding` explicitly permits recorded sub-Major findings (Minor, Note) — see "Findings" below.

### Per-subject detail

**1. Research coverage and provenance** — `sound_no_material_finding`.
Evidence inspected: the 53 Company Intelligence records and 2 Theme Intelligence records against the 27-name canonical population (`targets.yaml`); freshness fields (`review.last_reviewed`/`next_due`) cross-checked against `PI-0039`'s prior freshness-verification findings; the six formerly-gated names' and LLY's disclosed `limited`/`partial` evidence-access constraints (`PI-0038`'s disclosed WebFetch blockage). One Minor finding recorded here — see "Findings" — that does not change the primary verdict.
Required remediation: n/a (verdict is `sound_no_material_finding`; the one Minor finding's own remediation is recorded in "Findings").

**2. Relationship methodology** — `sound_no_material_finding`.
Evidence inspected: `REL-0001`'s frozen twelve-primitive taxonomy, directionality rules, claim-level evidence/abstention standard, and closed `decision_served` vocabulary, applied across the 13 sealed relationship records (`REL-0002`, `REL-0003`, `REL-0005`); the corpus-wide `evidence_classification: inferred` pattern (no record claims `observed`, since no counterparty record independently corroborates any relationship); the 11-name `structural_measurement_gap` set (SNPS, PANW, ISRG, TMO, ICE, SPGI, V, COST, WM, RTX, RKLB), independently re-derivable from `targets.yaml`/`issuer_lookthrough.yaml`/`intelligence/relationships/`; `REL-0006`'s own Milestone 4 completion-determination lifecycle (independent review, principal acceptance, merge, post-merge verification).
Required remediation: n/a.

**3. Zero-based protocol adherence** — `sound_no_material_finding`.
Evidence inspected: `OPS-0006` §§2-3's zero-based-research-discipline protocol applied to Milestones 5-8; Milestone 6's blind-drafting shard isolation and PR #253's own three-round correction history (bare-noun-"gate" leakage, the tautological-verifier finding, the dangling-section-title-reference gap), each independently traced to confirm root-cause resolution rather than a surface patch; Milestone 7's sealing-before-comparison sequencing and no-retroactive-rewrite discipline (`TIER-0007` §C/§J); Milestone 8's reuse of Milestone 7's own comparison fields rather than independent re-derivation, except where `TIER-0009` §G.2's bounded consistency-check design explicitly permits narrow additional reasoning (the `PI-0038` gated-six correction round).
Required remediation: n/a.

**4. Candidate tier architecture** — `sound_no_material_finding`.
Evidence inspected: `TIER-0001`/`TIER-0002`'s four-axis framework (`economic_role`, `capital_priority`, `risk_concentration`, `evidence_quality`) evaluated as a design, including its rejected alternative (extending the frozen Company Intelligence schema directly) and stated reasoning; whether the closed per-axis vocabularies remain adequate given everything observed since, including the corrected 17/9/1 `capital_priority` distribution from Milestone 6's own second bounded correction; the non-cascading abstention rule (one axis's uncertainty is never automatic grounds for abstention on another) held across all 27 records, including SPGI's own `no_policy_conclusion` abstention.
Required remediation: n/a.

**5. Policy recommendation package** — `sound_no_material_finding`.
Evidence inspected: the Milestone 8 artifact directly, all 27 tickers × 8 policy areas, against `TIER-0009` §§G-I — the eight-area treatment-class sorting; the closed seven-value primary/two-value secondary vocabulary and its deterministic precedence; the doctrinally forced `valuation_required` on `target_and_range`/`maximum_position_size` for all 27 tickers with zero exception; the live-recomputed (not cached) 11-name structural-gap set on `overlap_and_concentration`; complete absence of any numeric target, range, maximum size, score, or rank anywhere in the artifact; complete absence of directive add/hold/trim/exit/wait/stage language under any framing; independent re-run of `recommendation_validator.py` and an independent free-text scan for chart terminology and directive language.
Required remediation: n/a.

**6. Evidence-versus-judgment separation** — `sound_no_material_finding`.
Evidence inspected: whether every claim across the Milestones 3-8 output is labeled by its actual evidentiary status (primary source, secondary source, inference, estimate, unresolved) rather than presented uniformly as settled fact; `TIER-0007` §D's six-category labeling requirement as applied in the Milestone 7 artifact; `TIER-0009`'s equivalent evidence/rationale separation in the Milestone 8 artifact; whether the six formerly-gated names' and LLY's disclosed access limitations were preserved through Milestones 6-8 rather than silently dropped as evidence moved further from its original source — confirmed preserved (LLY and the six formerly-gated names remain consistently carried as `limited`/`partial` evidence and `unresolved_evidence`/`structural_measurement_gap` throughout the chain, which is itself part of why the Finding below does not invalidate any downstream M6/M7/M8 conclusion).
Required remediation: n/a.

**7. Absence of hidden scoring or allocator coupling** — `sound_no_material_finding`.
Evidence inspected, independently reproduced rather than accepted on a prior filing's self-report: no numeric score, weighted composite, or rank exists anywhere in `intelligence/classification/`, `intelligence/reconciliation/`, or `intelligence/recommendations/`; zero import coupling between any WS-0005 validator (`classification_validator.py`, `reconciliation_validator.py`, `recommendation_validator.py`, `relationship_validator.py`, `intelligence_validator.py`) and `allocate.py`/`margin_state.py`, in either direction; `allocate.py`, `margin_state.py`, and `levels.py` read none of `intelligence/classification/`, `intelligence/reconciliation/`, `intelligence/recommendations/`, or `intelligence/relationships/`; no live or scenario allocation check anywhere in the Milestones 3-8 history consumed WS-0005 output as an input.
Required remediation: n/a.

## Findings

### BLOCKING
None.

### MAJOR
None.

### MINOR

**Finding:** LLY Company Intelligence catalyst-date staleness.
**Artifact:** `intelligence/companies/LLY.yaml`
**Affected field:** `catalysts[0].expected`
**Description:** `PI-0039` had already identified that the stated Q2 2026 report date does not match the actual confirmed report date, but left the field unchanged because `PI-0039`'s own authorized scope did not extend to that Intelligence edit. The field remains uncorrected as of the reviewed head.
**Impact:** No Milestone 6, 7, or 8 conclusion is invalidated — LLY is already consistently carried as `partial` evidence coverage / `unresolved_evidence` through the classification, reconciliation, and recommendation chain, so this staleness was already priced into every downstream finding rather than silently assumed away.
**Severity:** Minor (per `OPS-0007` §1 point 8's severity scheme) — does not change subject 1's or subject 6's primary verdict.
**Required remediation:** A separately authorized Company Intelligence maintenance/refresh unit for LLY using primary-source confirmation. Not performed by this review, and not performed by this retention filing — this retention artifact records the finding; it does not correct `LLY.yaml`.

### NOTE (non-actionable, disclosed for completeness)

**Note 1.** `intelligence_classification_sanitizer.py` contains a cosmetic `\d` `DeprecationWarning` in its module docstring (confirmed present at the reviewed head; independently reproduced by this retention session's own full-suite run — see "Independent mechanical reconfirmation" below). Pre-existing, non-actionable under this scope.

**Note 2.** Several historical WS-0005 authorization gates in `operations/WORKSTREAMS.yaml` remain `status: in_progress` while their paired post-merge-verification gates record completion (e.g. the implementation-PR gate stays `in_progress` while a later completion-determination filing's own gate records the merge/review/acceptance chain). This is established repository convention (matching the `PI-0031`→`PI-0037`/`REL-0001`→`REL-0006`/`TIER-0007`→`TIER-0008`/`TIER-0009`→`TIER-0010` pattern) — non-actionable.

## Whole-portfolio boundary (preserved, not narrowed or widened)

The review covers only the governed 27-equity Milestones 3-8 body. It does **not** conclude that:

- the 27 are the exhaustive equity universe;
- additional equity contenders are rejected;
- ETF work is complete;
- crypto work is complete;
- GLD/defensive work is complete;
- cash/reserve doctrine is complete;
- debt-reduction doctrine is complete;
- cross-asset synthesis is complete;
- final holdings are known;
- final target weights are known;
- whole-portfolio readiness exists.

Broader contender/`XASSET-0001`/`WS-0014` work remains downstream and unauthorized by this review or this retention filing.

## Valuation boundary (preserved, not narrowed or widened)

For all 27 canonical equities:

- `target_and_range` remains `valuation_required`.
- `maximum_position_size` remains `valuation_required`.

This is confirmed as a correct categorical abstention — no valuation methodology exists anywhere in this repository. No numeric target, range, or maximum position size is invented, implied, or backsolved anywhere in this retained record.

## Eight-area policy-adoption-readiness matrix (preserved, not upgraded)

| Area | Adoption-readiness characterization |
|---|---|
| `role` | Internally sound; suitable for later adoption consideration as diagnostic input; evidence limitations remain where `unresolved_evidence` is carried. |
| `tier_architecture` | Internally sound as bounded consistency-check content; not itself a new architecture proposal; any actual tier redesign requires separate governance. |
| `capital_priority` | Internally sound; suitable for later adoption consideration as diagnostic input; unresolved evidence remains for affected names. |
| `target_and_range` | Internally sound only as a `valuation_required` abstention; not adoptable as numeric policy; requires a future valuation architecture. |
| `maximum_position_size` | Same as `target_and_range`. |
| `overlap_and_concentration` | Internally sound; later-adoption consideration available for measured names; the 11-name structural-measurement gap remains unresolved; any new relationship content requires separate governance. |
| `monitoring_and_thesis_break` | Internally sound; suitable for later adoption consideration where findings exist; no implementation authorized here. |
| `add_hold_trim_exit_discipline` | Internally sound as a mechanism-adequacy finding only; no directive trading instruction is created. |

## Adoption boundary — the controlling constraint (`TIER-0011` §K, restated verbatim in substance)

**Review ≠ adoption.**

This review, and this retention filing, do **not** authorize:

- `portfolio_role_ref` changes
- `conviction.rating` changes
- `target_pct` changes
- `holdings.yaml` changes
- gate changes
- caps/clusters changes
- allocator changes
- margin changes
- buy-ladder changes
- chart/deployment changes
- any buy/sell/add/hold/trim/exit instruction
- any order or trade

A later adoption action requires its own separate, explicit governance decision — with its own decision identifier, its own independent Lane G review under `OPS-0007` §1, and its own explicit principal acceptance — plus its own separate, future, bounded implementation PR. No such decision is pre-named, pre-scheduled, or pre-authorized by this review or by this retention filing. A future Milestone 9 completion determination, even if it closes WS-0005's own `milestone-9-independent-review-and-later-adoption` gate, likewise does not itself authorize adoption (`TIER-0011` §K.4).

## What this retained record does not mean

- It does not mean Milestone 9 is formally complete — that determination, if and when made, is a separate, later, independently-reviewed Lane G filing (matching the `PI-0031`→`PI-0037`/`REL-0001`→`REL-0006`/`TIER-0007`→`TIER-0008`/`TIER-0009`→`TIER-0010` precedent), not this retention filing.
- It does not mean any Milestone 8 finding is adopted, approved for adoption, scheduled for adoption, or presumptively correct.
- It does not mean the LLY finding, or any Note, has been corrected — none has been, by this filing or by the review itself.
- It does not mean whole-portfolio, ETF, crypto, GLD, cash/reserve, or debt-reduction work has advanced in any way.
- It does not mean any numeric target, range, maximum position size, score, or rank now exists for any of the 27 tickers.
- It does not mean any tier, target, role, gate, holdings, cap, cluster, allocator, margin, or ladder value has changed, or that any order or trade is authorized.

## Retention provenance and scope

This artifact was authored by a session tasked with retaining an already-completed, independently-conducted Milestone 9 review — not with conducting, re-conducting, extending, or second-guessing that review. The retaining session:

- performed no new external research, no new relationship research, no valuation-architecture work, no additional-equity classification, no ETF/crypto/cash/GLD/debt-reduction work, and no chart-evidence work;
- made no edit to `intelligence/companies/LLY.yaml` or to any other Company/Theme/relationship/classification/reconciliation/recommendation record;
- did not upgrade, downgrade, or reinterpret any verdict, finding, or boundary reported by the review — every verdict, finding, and boundary above is transcribed as reported;
- independently reconfirmed, through its own live, deterministic, non-judgmental command execution (not a repetition of the review's own analytical judgment), that the repository's mechanical state at the reviewed head is consistent with the review's own reported findings — see "Independent mechanical reconfirmation" below. This reconfirmation is a factual cross-check on reproducible tool output, not a re-review of the seven subjects' substance, and does not alter any verdict above.

### Independent mechanical reconfirmation (performed by the retaining session, at the reviewed head `37c1cb45fc05de525752ee74c93fce84a3cfd688`)

- `classification_validator.py`: `OK (28 result(s))`
- `reconciliation_validator.py`: `OK (27 tickers)`
- `recommendation_validator.py`: `OK (27 tickers)`
- `relationship_validator.py`: `OK (13 record(s))`
- `intelligence_validator.py`: clean (no output on success)
- `freshness_validator.py`: `OK`
- `contender_registry_validator.py`: `OK (84 entries)`
- Full repository test suite: **3091 passed, 0 failed**, 1 pre-existing warning (`intelligence_classification_sanitizer.py`'s cosmetic `\d` docstring `DeprecationWarning` — matching Note 1 exactly)
- Decision catalog: 88 decisions, `issues == ()`
- `git diff --check`: clean
- `intelligence/companies/LLY.yaml` `catalysts[0].expected` independently read and confirmed to still read `2026-08-31` (unedited), corroborating the Minor finding's own "remains uncorrected as of the reviewed head" description

No protected path (`allocate.py`, `margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, any existing `intelligence/classification|companies|themes|relationships/` record, `COHORT_MANIFEST.yaml`, `intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`, `intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`) is touched by this retention filing.
