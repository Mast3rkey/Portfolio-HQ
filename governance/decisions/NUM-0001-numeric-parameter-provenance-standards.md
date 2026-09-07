---
decision_id: NUM-0001
date: 2026-07-21
status: Accepted
category: numeric_governance
related_decisions: [GOV-0001, GOV-0002, GOV-0003, MARGIN-0004, TGT-0001, PI-0004]
supporting_artifact: docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md
---

## Context

A repository-wide read-only Numeric Parameter Provenance Audit (`docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md`, dated 2026-07-21, audited against `main` SHA `0b419765301128223c2f277bd162f38a6e50750c`) found consequential numeric parameters across every domain of this system — portfolio construction, margin, allocator mechanics, technical gates, and research methodology — described with inconsistent, sometimes overclaiming provenance language. Concretely: the audit found parameters previously informally treated as "backtested" or "calibrated" that evidence had, at most, bracketed or failed to disprove, not uniquely selected; at least one stated governance review trigger (`PI-0004`'s "3-5 records" condition for revisiting `risk.severity`/`risk.status`) met and never re-examined; and several code-level fallback/duplication patterns currently masked by matching configuration, with no standing convention for disclosing that distinction. No existing decision category's stated scope — `architecture_governance` (documentation architecture), `margin_doctrine`, `portfolio_construction_governance`, `concentration_risk`, `research_automation`, `portfolio_intelligence`, `analytical_vocabulary` — covers a cross-cutting evidentiary standard for numeric parameters generally.

## Decision

Establishes a Numeric Parameter Provenance and Calibration Standards framework governing how every future **consequential numeric parameter** in this repository is classified, sourced, labeled, and reviewed. This decision does not itself classify, validate, change, or supersede any existing parameter — the supporting audit's classifications are non-binding observations at one audited SHA, not this decision's operative content.

**Consequential**, for the purposes of this framework, means: a value where changing it can materially alter an allocation, recommendation, trim, leverage or survivability outcome, risk classification, research verdict, governance gate, or the validity of an investment-facing output. This definition deliberately excludes incidental formatting values, identifiers, dates, and immaterial engineering literals — this framework's provenance requirements apply only to consequential parameters, not to every numeric literal in the codebase.

### 1. Parameter classes

Every consequential numeric parameter is classified into one or more of six classes (a parameter may have multiple contributing components; its record must state which component actually selected the binding value):

1. **Externally imposed** — a broker/regulatory/contractual/market-convention constraint the system did not choose.
2. **Mathematically derived** — a reproducible formula over authoritative inputs, with no judgment call in the number itself.
3. **Empirically calibrated** — evidence directly and uniquely selected this specific number as superior to real, tested alternatives.
4. **Evidence-bounded governance selection** — evidence establishes a defensible range, constraint, or trade-off, but does not uniquely select one number; governance selected the exact binding value within that supported space and records the economic reason for that specific selection.
5. **Provisional governance guardrail** — a deliberately conservative interim value adopted under incomplete evidence, explicitly labeled as such, with a stated review condition.
6. **Unsupported/unclassified** — fits none of the above. Distinguishes "not yet reviewed under this framework" from "reviewed and found provisional."

### 2. Contextual classes (kept separate, never conflated with the six above)

Observed state; calculated output; research assumption; engineering constant; test fixture; dates/identifiers/formatting values.

### 3. Source-of-truth ownership

Every consequential parameter has exactly one canonical source-of-truth location. Where a value is consumed in more than one file — a hardcoded fallback, a duplicated literal, a redundant computation — the record names the single canonical location and flags every other site as a duplicate requiring reconciliation. This decision does not itself reconcile any duplicate; identifying one is a provenance-recording act, not an implementation authorization.

### 4. Required provenance fields

Per consequential parameter: canonical source location; every duplicate/fallback location; provenance class(es) and which component selected the binding value; supporting evidence artifact, or an explicit "none — doctrine" statement; current binding status; whether config-editable or hardcoded; and, where applicable, its review condition.

### 5. Duplicate and fallback disclosure

A hardcoded fallback that currently matches its canonical config value is disclosed as **masked**, not silently treated as equivalent to the absence of a divergence risk. A parameter's record states explicitly whether a divergence between a fallback and its canonical source has been demonstrated, or is latent/masked under current configuration.

### 6. Provisional-value labeling

Every parameter classified as a provisional governance guardrail carries, at its source location or governing decision, an explicit "provisional, not empirically calibrated" label and a stated review condition. Review conditions are **not required to share one universal calendar cadence** — a condition may be calendar-based, event-driven (e.g., "revisit if a new leverage regime appears in the data," "revisit once N records exist"), or evidence-driven (e.g., "revisit if a future sweep narrows the supported range"). The appropriate condition type is chosen per parameter, never mandated uniformly.

### 7. Evidence-bounded governance-selection requirements

Must record: the defensible range or constraint the evidence established; which specific value within that range governance chose; and the stated economic (not statistical) reason for that specific choice. A sensitivity sweep finding "no statistically significant difference from the current value" does **not**, by itself, constitute empirical calibration — it establishes, at most, an evidence-bounded range.

### 8. Empirical-calibration standards

A parameter may be labeled "empirically calibrated" only when evidence directly and uniquely favors that specific number over real, tested alternatives — not merely fails to disprove it. Where feasible, calibration evidence should include a stated pre-committed threshold, sensitivity/robustness variants, and out-of-sample or walk-forward evaluation; where infeasible (declared explicitly, with reason), in-sample evidence may still ground an evidence-bounded governance selection, but must not be mislabeled as calibration.

### 9. Supported ranges and uncertainty disclosure

Where a sweep exists but is flat or inconclusive across part of its range, the record states the actual empirically-distinguishable range, not an implied single-point precision the evidence doesn't support.

### 10. External-term freshness ownership

Every parameter classed "externally imposed" records: source; observed/verified date; account applicability; whether the term is point-in-time or durable; an owner responsible for refresh; a refresh condition or cadence; and defined behavior when stale or unavailable. No single universal freshness interval is mandated by this framework — the cadence or stale-threshold itself is a consequential parameter and requires its own rationale or authority, per parameter.

### 11. False-precision prohibitions

A source, configured value, observation, or calculation may be described as verified when the proposition being verified is stated precisely — e.g., "this config key is verified to contain value X," "this branch's behavior was verified against a test," or "this count was verified by direct enumeration." That kind of factual verification is not restricted by this section and remains ordinary practice throughout this repository's documentation.

No parameter may be described, without qualification, as economically validated, empirically verified, optimal, or derived in a way implying economic correctness, unless its recorded evidence class under §1 actually supports that specific claim. Confirming that a source contains a value, that an observation was made, or that a calculation was performed correctly is not, by itself, a claim about whether the underlying number is economically right — those are different propositions, and a record must not blur them by reusing "verified" to mean both without qualification.

### 12. Review-trigger handling

A documented review trigger being met (a stated record-count, book-size, or other threshold) requires an explicit future governance decision addressing it. It does **not**, by itself, automatically change, invalidate, or supersede the parameter. A met trigger that has not yet been addressed is itself flagged as a governance gap requiring attention, not treated as implicit re-affirmation by silence.

### 13. Supersession rules

Unchanged from existing convention (`governance/decisions/README.md`): a filed decision's substance is never edited after acceptance; correct narrowly via a dated appended note, or supersede via a new decision that explicitly marks the prior one Superseded.

### 14. Implementation and validator boundaries

This decision authorizes **no code, no validator, no provenance-checking tool**, and no change to `allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, any backtest script or report, or any Company/Theme Intelligence file. Any future validator enforcing this framework's required fields requires its own separate, later governance authorization — the same doctrine-then-implementation split already used for Portfolio Intelligence (`PI-0001`→`PI-0002`) and the Freshness framework (`AUTO-0001`→`AUTO-0002`).

### 15. Backward treatment of existing parameters

This decision classifies no existing parameter as operative policy. The supporting audit's classifications of existing parameters are non-binding observations at one audited SHA — informative context, not this decision's binding content. Existing parameters are not retroactively invalidated, re-labeled, or required to be reclassified as a precondition of this decision taking effect.

### 16. Transition rules

Every current safeguard remains exactly as binding as it was before this decision: the 1.8x leverage cap, the 30% buffer floor, every cluster cap, every gate, every tier weight, and every trim rule. Nothing suspends, loosens, or pauses an existing safeguard merely because a supporting audit describes its provenance, or because a future governed review classifies it under this framework.

## Explicit statements

- **Current parameters remain binding until separately superseded.**
- **Adoption validates no existing number.**
- **Adoption changes no existing number.**
- **Adoption classifies no existing parameter as operative policy** — the supporting audit's classifications are non-binding observations at one audited SHA.
- **Adoption authorizes no calibration research** of any kind — leverage, margin deployment, margin repayment, T1/T2 trim, or otherwise. Any such research remains gated exactly as `GOV-0003`/`MARGIN-0004` already require, under its own separate charter.
- **Adoption authorizes no code or validator.**
- **Adoption chooses no holding, tier, target, cap, weight, leverage level, margin deployment rule, repayment rule, or allocator output.**
- **A met review trigger requires explicit governance attention, not an automatic parameter change.**
- **Tests proving software behavior do not prove economic validity** — a passing test confirms the code does what it was written to do, not that the underlying number is the right one.
- **No universal review cadence is imposed** — calendar, event-driven, and evidence-driven conditions are each valid depending on the parameter.
- **Any freshness cadence or stale threshold is itself consequential and requires its own provenance record**, not an assumed default.

## Audit preservation

The supporting audit (`docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md`) is a dated evidence snapshot. Future repository states require a new dated audit or explicitly governed addendum rather than silently rewriting this snapshot's substantive findings. The audit does not become operational authority by virtue of this decision citing it as a supporting artifact — the authority disclaimer stated in the audit document itself governs its status, unchanged by this ADR.

## Rationale

The audit demonstrated concrete, real classification errors under the repository's prior informal approach. Most notably, the 1.8x leverage cap and 30% buffer floor sit in two evidentially distinct — and previously blurred-together — situations that this decision keeps separate: a later leverage-level sweep (1.2x–2.0x) exists and bears specifically on the 1.8x leverage cap, but it failed to distinguish 1.8x from its adjacent tested levels (flat/identical from 1.6x–2.0x) and neither validated, optimized, nor invalidated it; no equivalent sweep of alternative floor levels exists at all for the 30% buffer floor — its evidentiary situation is "never tested," not "tested but non-selecting." Both remain provisional governance guardrails under `MARGIN-0004`'s unedited authority, but for two different reasons, and this decision does not imply the leverage sweep bears on the buffer floor's validity in any way. Similarly, `band.cap_multiple` and `trim_rsi` had been informally described in ways that blurred "evidence bracketed a range without disqualifying the current value" with "evidence calibrated this specific number." Without a named, shared standard, this conflation will keep recurring across future backtests, decisions, and reviews. This decision does not resolve any specific instance found by the audit — it establishes the vocabulary and required-fields discipline so future work can state its evidentiary basis precisely, and gives the repository a place to record when a stated review trigger (e.g., `PI-0004`'s) has been met but not yet acted on, rather than letting that fact go unrecorded.

## Alternatives Considered

- **Fold this into `GOV-####` under `architecture_governance`.** Rejected — `governance/decisions/README.md` scopes `GOV-` to decisions about this repository's documentation/governance architecture itself; a numeric-evidence-standards framework is a different kind of thing and would stretch that prefix's stated scope.
- **File this as a constitutional amendment.** Rejected — for the same reason `GOV-0002` itself rejected folding its own authority-hierarchy work into the Constitution: "a hierarchy that must accommodate new specification and decision types over time belongs in an amendable governance decision, not the document hardest to amend" (Constitution §7 — amendment "rarely, and only through its own... process"). This framework will need ordinary iteration as new parameter classes and domains appear.
- **Do nothing; rely on informal Decisions Log discipline.** Rejected — the audit demonstrated concrete conflation errors under exactly that informal approach.
- **Have this decision itself reclassify every existing parameter.** Rejected — conflates a standard-setting decision with a parameter-by-parameter audit; the audit document already performs the latter as a dated, separately-updatable snapshot, without reopening this decision each time.
- **A genuinely new `PARAM-####` or `PROV-####` prefix instead of `NUM-####`.** Considered and not adopted for this filing per the principal-approved governance identity (`NUM-0001`, category `numeric_governance`) — `PARAM-` risked reading as "decisions that set a specific parameter's value," which collides conceptually with `TGT-####`'s existing scope, and `PROV-` risked ambiguity with "provisional," "provider," or "province" outside context.

## Consequences

Going forward, any new numeric parameter, backtest report, or governance decision touching a consequential number is expected to state its provenance class(es) and which component selected the binding value, using this framework's vocabulary. Explicitly, and restated for emphasis given the sensitivity of the domains this framework touches:

Nothing about the 1.8x leverage cap, the 30% buffer floor, any cluster cap, any tier weight, any trim rule, or any allocator gate changes as a result of this decision. No research charter of any kind is opened. No code or validator is authorized. No holding, tier, target, or margin behavior is chosen or altered. The supporting audit remains exactly what it says it is — a dated, non-binding evidence snapshot — and does not acquire operational authority by being cited here.

Explicitly unchanged: `allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, every backtest script/report, every Company/Theme Intelligence record, `decision_log.yaml`, and every existing governance decision's status.
