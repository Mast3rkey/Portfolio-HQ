---
decision_id: XASSET-0023
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, LEVEL2-0001, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0023-level1-non-abstention-feasibility-and-level2-prerequisite-determination.md
---

## Context

XASSET-0022 is effective. It closed `CM-27 application_schema` and `CM-28
deterministic_trace_and_repeatability` mechanically while expressly withholding application authority:
its `APPLICATION_AUTHORIZATION_REGISTRY` is empty, no `intelligence/level1_application/` artifact
exists, and XASSET-0021 §O's double gate stands unweakened.

The next question is therefore not mechanical but interpretive. Before any expensive economic-evidence
unit can be scoped, three controlling ambiguities have to be read out of already-accepted text:

1. whether `CM-25 accepted_risk_uncertainty_treatment` blocks a non-abstaining Level-1 outcome
   independently, or only because no lawful endpoint currently survives;
2. what Level-1 result accepted authority actually requires before final Level-2 membership or sizing
   work may lawfully begin; and
3. what a future body of evidence would have to prove to constitute a lawful Level-1 point or range
   endpoint under XASSET-0020's "uniquely stated or uniquely mathematically derived" test.

Each of the three is currently answerable in more than one way from the filed text, and each reading
would scope a materially different — and materially more expensive — successor unit. Resolving them
is interpretation of accepted authority, not new economics.

This decision resolves those three questions and nothing else. It performs no research, admits no new
evidence, creates no endpoint, sizes nothing, authorizes no application, and adopts no policy.

**Disclosure — no retained audit artifact.** The session authorizing this filing described a
completed read-only "L1-SIZING Non-Abstention Economic Sufficiency Audit." A direct search of
`governance/audits/` and the wider repository at this filing's base found no such retained artifact.
Every determination below is therefore grounded in this decision's own reading of accepted decision
text, cited section by section, and on no unverified audit. Where accepted text does not resolve a
question, this decision says so rather than closing the gap by assertion.

## Decision

### A. Lifecycle, authority, and controlling identity

This is an `OPS-0009` Lane G filing. While its pull request is open it is a proposed determination
only. It becomes effective only after independent full exact-head review, principal exact-head
acceptance, merge, immediate post-merge verification, and successful exact-head CI against one exact
head. The author may commit, push, and open the draft PR but may not self-review, principal-accept,
mark ready, or merge.

The controlling chain this decision interprets, and does not edit, is:

- `XASSET-0019`, effective from PR #313 accepted head `df2cb58c38a87888c476af0743884b8377b354e5`,
  merge `0962385bf6b1b72cebe8b326da49927977db2912`;
- `XASSET-0020`, effective from PR #319 accepted head `d2c0ce84f1922bc606c3de6983eb47266dbe4d72`,
  merge `e7d66d93b5f7ab2ecd985a7a4bf680a118df6b0e`;
- `XASSET-0021`, effective from PR #320 accepted head `afc3eef410dd3748c209053bdb8de7dd09c273bf`,
  merge `5f94634bdfd0ff8ab603b8dd6ece2921033191df`;
- `XASSET-0022`, effective from PR #321 accepted head `85a39e2dadb4fce27c285dc978bf648fef21c9df`,
  merge `8f4da01cb2dfe020bb56335db7858c3c97ff0fdf`; and
- `LEVEL2-0001`, `NUM-0001`, and the accepted `RISK-0001` attempt-2 lifecycle frozen at
  XASSET-0021 §C.3.

Stale `status: Proposed` frontmatter on merged predecessors does not defeat those accepted/effective
histories, exactly as XASSET-0020 §A and XASSET-0021 §C.1 already record.

### B. Scope

This decision determines only what future evidence or authority would have to prove. It supplies no
part of the economic answer.

It resolves exactly three questions — §§D–E, §§F–G, and §H. It does not amend XASSET-0019,
XASSET-0020, XASSET-0021, or XASSET-0022; it does not reclassify any XASSET-0021 §N closure-matrix
row; it does not populate `APPLICATION_AUTHORIZATION_REGISTRY`; and it does not grant, imply, or
schedule application authority.

`operations/WORKSTREAMS.yaml` is synchronized additively by this filing as an operational record. It
is not an authority source, and nothing in it is relied on for any determination below.

### C. The three ambiguities, reproduced from accepted text

**C.1 — CM-25.** XASSET-0021 §K closes with: "Because no independent endpoint survives, each state
makes the affected sleeve's point/range eligibility `APPLICATION_MUST_ABSTAIN` under this snapshot."
The subordinate clause "Because no independent endpoint survives" and the qualifier "under this
snapshot" read as conditioning the abstention on endpoint absence. But the same section states the
four RISK family dispositions are "precision/abstention gates," which reads as an independent bar.
Whether a future lawful endpoint would be defeated by RISK's `unable_to_determine` states alone is
therefore unresolved on the face of XASSET-0021 §K.

**C.2 — Level-2 prerequisite.** XASSET-0019 §I fixes the order "provisional Level 1 sizing/ranges →
Level 2 membership/sizing," but nowhere states a completion criterion for the Level-1 step.
XASSET-0019 §H places the "complete, internally reconciled asset-state representation" requirement
*after* Level-2 membership/sizing. XASSET-0019 §G says an abstention "remains valid." LEVEL2-0001 §K
withholds Level-2 authority entirely. It is therefore unresolved on the face of the text whether
Level-2 work requires non-null Level-1 outcomes for all four sleeves, for some, or for none.

**C.3 — Endpoint admissibility.** XASSET-0020 §J.1 item 6 and XASSET-0021 §F both require an endpoint
to be "uniquely stated by admitted effective authority or uniquely mathematically derived from
admitted authoritative inputs with complete NUM-0001 provenance." Neither section defines what
"uniquely stated" or "uniquely mathematically derived" mean operationally, so neither a future
evidence unit nor its reviewer can currently tell what would satisfy the test.

### D. Determination 1 — CM-25 / RISK coupling

**The coupling is asymmetric between the two non-abstaining outcome types. It is independent for a
POINT and conditional for a RANGE.**

**D.1 — RISK independently bars a POINT.** XASSET-0020 §J.1 item 3 requires, for a point, that "all
pairwise comparisons bearing on the sleeve are determinate and none leaves unresolved precision."
XASSET-0021 §D fixes that "All six driver classes are applicable to every investable-sleeve
marginal-capital pair. They may not be marked `not_applicable` merely because evidence is missing,"
and maps both `downside_path_risk` and `recovery` to the accepted RISK dispositions with the
instruction to "preserve that state." XASSET-0020 §H's conclusion table sends any "required
missingness ... or other unclosed state" to `unable_to_determine`.

Composing those three: while any RISK family disposition remains `unable_to_determine`, the
`downside_path_risk` and `recovery` ledger cells of every pair bearing on that sleeve remain
unclosed, so no such pair can reach a determinate conclusion, so XASSET-0020 §J.1 item 3 cannot be
satisfied. This holds **even if every other driver class became determinate and a lawful endpoint
existed**.
For a point, therefore, CM-25 is an independent bar, not merely an endpoint-conditioned one.

**D.2 — RISK does not independently bar a RANGE.** XASSET-0020 §J.2 deliberately omits any
pair-determinacy condition. Its third bullet instead requires only that "unresolved pair evidence
cannot invalidate either endpoint under §I." XASSET-0020 §I supplies the survival rule: "A sleeve range
may still survive that missing pair only when both endpoints are independently and directly governed
and remain valid under every possible direction of the unresolved pair. That is a non-inferential
intersection of already-authorized bounds, not a derived relationship."

XASSET-0020 §J.2's phrase is "unresolved pair evidence," which is broader than XASSET-0020 §I's own
heading case of a structurally absent record and reaches a pair left `unable_to_determine` for any
reason, RISK included. A range is therefore eligible notwithstanding RISK's `unable_to_determine`
states, provided
both endpoints independently satisfy §H below and remain valid under every possible direction of each
unresolved pair.

**D.3 — This is not neutrality, and may never be read as neutrality.** XASSET-0020 §I's survival
test is strictly stronger than treating an unresolved pair as neutral. Neutrality would let an
unresolved pair contribute nothing and leave a candidate bound standing by default; XASSET-0020 §I
instead requires each endpoint to hold under *every* possible direction the unresolved pair could
take, so an endpoint that survives only under some directions is defeated. XASSET-0021 §K's
prohibition is preserved in full and restated here as operative text: no RISK `unable_to_determine` state may be recoded as neutral,
indistinguishable, non-rejection, a directional lean, a target anchor, a range anchor, or an
adjustment, and none may contribute positive preference to any sleeve under any framing.

**D.4 — CM-25's classification does not change.** `CM-25` remains `APPLICATION_MUST_ABSTAIN` on the
XASSET-0021 §C snapshot, because XASSET-0021 §F's endpoint finding independently forces abstention
for every sleeve regardless of D.2. This determination states the *reason* CM-25 abstains and therefore what
would have to change for it not to; it reclassifies nothing and leaves XASSET-0021 §N's counts —
14 / 14 / 2 — exactly as accepted.

**D.5 — Consequence for successor scoping.** A successor evidence unit seeking a non-abstaining
Level-1 *range* need not obtain determinate RISK outcomes. A successor unit seeking a Level-1 *point*
must, and RISK-0001's attempt authority is `CONSUMED` with no retry or third attempt, so any such
evidence would require a new separately chartered study. This decision authorizes neither.

### E. XASSET-0019 §J is a different requirement from CM-25, and is already satisfied

XASSET-0019 §J requires that "The next separately authorized RISK study must challenge rather than
ratify the provisional magnitude or point-target premise for equity, broad-market funds, GLD, and
crypto before final Level 2 sizing."

That is an **occurrence-and-posture** requirement on a study, gated to *final Level-2 sizing*. It is
not a requirement that the study return determinate results: §J expressly lists "honest
null/inconclusive results" among what the study may examine, and requires only that it challenge
rather than ratify. RISK-0001 is that study — its own charter states, in its Context section under
"Controlling architecture," that it "is the separate early-RISK authority `XASSET-0019` requires. It challenges
rather than ratifies those historical scenarios, before replacement Level-1 sizing or final Level-2
work" — and its attempt-2 lifecycle is accepted and frozen at XASSET-0021 §C.3 with all four families
at `unable_to_determine`.

Accordingly:

- XASSET-0019 §J is **satisfied**. An all-`unable_to_determine` outcome discharges it rather than
  reopening it, because challenging the point-target premise and failing to sustain it is the posture
  §J demanded.
- §J gates **final Level-2 sizing**, not provisional Level-1 sizing. XASSET-0019 §I's own sequence
  places "early empirical diagnostics" *before* "provisional Level 1 sizing/ranges," so the RISK
  checkpoint is upstream of Level-1 sizing and cannot be a gate on it.
- Satisfying §J creates **no** endpoint authority, no driver direction, and no preference. The two
  questions are disjoint: §J asks whether a qualifying study happened; CM-25 asks how that study's
  result propagates into XASSET-0020 §J.1/§J.2 eligibility.
- Conversely, CM-25's abstention does **not** mean §J is unmet, and no future unit may cite CM-25 as
  grounds for asserting that a further RISK study is required by §J.

### F. Determination 2 — the Level-2 prerequisite threshold

**F.1 — There is no accepted whole-Level-1 completeness precondition for entering Level-2 work.**
The only "complete" requirement in the chain is XASSET-0019 §H's non-adopted candidate whole-100%
reconciliation, and §H positions it expressly "After provisional Level 1 sizing/ranges and Level 2
membership/sizing, but before full-portfolio stress." XASSET-0021 §I independently confirms that
placement, recording that unresolved liquidity "blocks the later complete candidate/stress/adoption
sequence where XASSET-0019 requires a fully specified asset state" — a gate on the candidate, stress,
and adoption steps, not on Level-2 entry. Option (a) of the framing question — non-null point or
range for all four sleeves before any Level-2 work — has no textual basis and is rejected.

**F.2 — What accepted authority does require is an ordering, and it is binding.** XASSET-0019 §I
fixes "provisional Level 1 sizing/ranges → Level 2 membership/sizing." A lawful, completed Level-1
application record — whatever its outcome — is therefore a sequencing precondition to Level-2
membership or sizing work. No such record exists, can exist, or may be generated today: application
authority is withheld and `APPLICATION_AUTHORIZATION_REGISTRY` is empty.

**F.3 — Per sleeve, Level-2 sizing requires that sleeve's Level-1 outcome to be non-null. This is
arithmetic, not a new threshold.** Under the two-level architecture XASSET-0019 §K preserves and
XASSET-0020 §N restates ("size instruments, or assign internal sleeve weights"), an instrument's
share of the normalized asset unit is the product of its sleeve's Level-1 share and its within-sleeve
share. Where a sleeve's `point_or_range_or_null` is null, that product is undefined and no
portfolio-level instrument quantity can be expressed for any instrument inside it. This constrains
portfolio-level instrument *quantities* only; it says nothing about whether within-sleeve relative
work of any other kind is permissible, which remains separately unauthorized under LEVEL2-0001 §K.

**F.4 — Level-2 membership carries no Level-1 magnitude precondition, and is unauthorized anyway.**
Choosing which instruments represent a sleeve does not require the sleeve's magnitude, and no accepted
text conditions it on one. LEVEL2-0001 §K nevertheless withholds authority for final membership
outright, and §J makes "a future final Level 2 membership decision is undertaken" a mandatory refreeze
trigger. Membership therefore requires its own authorization and a refreeze regardless of any Level-1
outcome.

**F.5 — XASSET-0019 §J's RISK precondition on final Level-2 sizing is satisfied** per §E and is not
reopened by its `unable_to_determine` outcome.

**F.6 — Composite answer.** Before final Level-2 membership or sizing work may lawfully begin,
accepted authority requires: (i) a lawful completed Level-1 application record, under an application
authority that does not yet exist (§F.2); (ii) for *sizing* of any given sleeve, a non-null Level-1
outcome for that sleeve (§F.3); (iii) for *membership*, its own separate authorization plus a
LEVEL2-0001 §J refreeze (§F.4); and (iv) the already-satisfied XASSET-0019 §J RISK checkpoint
(§F.5). It does **not** require non-null outcomes for all four sleeves as a condition of entry, and it does **not**
relocate XASSET-0019 §H's whole-100% completeness gate, which remains exactly where §H puts it and
remains independently blocked by unresolved liquidity under XASSET-0021 §I.

Because the current snapshot yields abstention for every sleeve, the practical consequence today is
that zero sleeves are eligible for Level-2 sizing, and an all-abstaining Level-1 record would satisfy
the §F.2 ordering while supplying no sleeve for §F.3 to act on.

### G. Residual Level-2 ambiguity that accepted authority does not resolve

If a future Level-1 record ever returned a non-null outcome for **some but not all** sleeves, whether
Level-2 sizing may proceed for that subset while the remainder abstain is **not resolved by accepted
text**. XASSET-0019 §I permits the ordering, §H's completeness gate sits downstream and contemplates
governed `UNSIZED_UNASSIGNED_CAPITAL` as an explicit treatment, and §H simultaneously directs that
"If no complete lawful candidate can be formed, full-portfolio stress must abstain and remain blocked
while the work returns to the appropriate preregistered checkpoint in §I." Those provisions can be
read either to permit bounded subset work that may later fail at §H, or to withhold it until the
subset question is governed.

This decision deliberately does **not** invent a sequencing rule to close that gap. The question is
not currently reachable — no sleeve is non-abstaining, and no application authority exists — and
resolving it now would create Level-2 sequencing policy on a hypothetical. It is recorded here as an
identified, deferred ambiguity that requires its own separate governance decision **if and when** a
partially non-abstaining Level-1 record is ever lawfully produced. Until then no unit may assume
either reading.

### H. Determination 3 — the endpoint feasibility and admissibility test

This section states what future evidence must satisfy to constitute a lawful Level-1 point or range
endpoint. It creates no endpoint, no formula for portfolio weights, no scoring model, no optimizer, no
evidence conclusion, no historical anchor, and no sleeve percentage or range.

The governing rule is XASSET-0020 §J.1 item 6 and §J.2 bullet 2, restated at XASSET-0021 §F: an
endpoint may originate **only** from one exact numeric value **uniquely stated** by admitted effective
authority, **or uniquely mathematically derived** from admitted authoritative inputs, in either case
with complete NUM-0001 provenance. There is no third route.

Throughout this section, "the endpoint quantity" means the share of XASSET-0020 §C's one normalized
unit of prospective unlevered asset-side capital attributable to one named investable sleeve — the
same quantity XASSET-0020 §K's reconciliation identity sums as `sum(admitted_sleeve_points)`.

#### H.1 What may constitute endpoint-supporting evidence

An item may support an endpoint only if all of the following hold.

1. **Admitted.** It satisfies XASSET-0020 §F.1 in full: exact path and content/file SHA-256 match;
   its governing authority is accepted/effective; its own validator passes where one exists; its
   question matches the current comparison; and every governed freshness condition passes.
2. **In the governed snapshot.** It appears in XASSET-0021 §§C.2–C.3, or in a snapshot lawfully
   replaced or extended by a separate future authorization — XASSET-0021 §C.1 forbids an application
   from silently adding a later file, refreshed observation, or new source class.
3. **Classified DRIVER for the endpoint question.** XASSET-0020 §E.3 provides that disclosures "must
   not enter arithmetic or decide a direction." A DISCLOSURE-classified item therefore may neither
   state nor enter an endpoint. This is decisive under the present snapshot, where XASSET-0021 §C.2
   marks essentially every row DISCLOSURE-only for current preference.
4. **Not barred by its own `forbidden_implications`** under XASSET-0020 §F.1.
5. **Not a constraint.** XASSET-0020 §E.2 provides that constraints "never create preference," and
   XASSET-0021 §F that "Bound intersection may narrow already-authorized endpoints but may not create
   one." A constraint may clip or intersect an endpoint that already exists; it can never originate
   one.

#### H.2 "Uniquely stated," operationally

An endpoint is uniquely stated when, and only when, all of the following hold.

1. **Same quantity.** An admitted DRIVER item's own governed content states an exact numeric value
   *for the endpoint quantity as defined above* — not a numerically similar figure answering a
   different question. XASSET-0020 §D requires "question-matched evidence" and XASSET-0020 §F.1
   requires the item's question to match the current comparison.
2. **Stated by the source.** The value appears in the admitted source's governed content. A value
   supplied by an application author, a reviewer, a task brief, this decision, or any decision's
   narrative prose is not stated by an admitted source and is barred as "undocumented judgment" under
   XASSET-0021 §F.
3. **Competent authority.** The stating source's accepted/effective authority must extend to fixing a
   Level-1 sleeve share. An authority effective for some other purpose does not become Level-1
   endpoint authority because it happens to contain a number.
4. **Exact.** The value is taken at exact source precision under XASSET-0021 §G. It may not be
   rounded, inferred, reconstructed, or normalized into existence.
5. **Exactly one.** No second lawful value for the same endpoint quantity exists anywhere in the
   admitted set. Two admitted items stating different values for the same quantity is a same-level
   conflict yielding `unable_to_determine` under XASSET-0021 §H, and under XASSET-0020 §J.1, "If more
   than one lawful value remains, a point is prohibited."
6. **Not from a barred origin.** XASSET-0021 §F bars a historical target, XASSET-0016 or XASSET-0018
   output, midpoint, current allocation, analyst or reviewer preference, evidence count, relative
   maturity, residual balancing, equal division, or undocumented judgment. XASSET-0020 §M's
   contamination list is barred identically and in full, including the legacy `18.67 / 14.67 / 16.67 /
   16.67` outputs, the `33.32` residual, the six-way equal baseline, the fixed adjustment increment,
   R2/R3, and every current target, holding, weight, tier, or gate. XASSET-0022 §R already scans for
   several of these mechanically; that scan is a floor, not the full boundary.

#### H.3 "Uniquely mathematically derived," operationally

A derivation qualifies when, and only when, all of the following hold.

1. **Admitted DRIVER inputs only**, each satisfying §H.1.
2. **Closed arithmetic only.** XASSET-0020 §M provides that "The only authorized arithmetic is exact
   normalization, direct source-prescribed derivation, constraint clipping, bound intersection, and
   reconciliation." No other operation may appear anywhere in the derivation.
3. **Source-prescribed.** "Direct source-prescribed derivation" means the admitted source itself
   prescribes the derivation. An application may not compose, select among, or invent a derivation the
   sources do not prescribe; composing one is authorship, not derivation.
4. **Exact.** Exact source precision or an exact rational derivation, per XASSET-0021 §G. Canonical
   values are never rounded before comparison, intersection, constraint application, or
   reconciliation, and arithmetic that would require an ungoverned rounding choice forces abstention
   rather than a chosen convention.
5. **Exactly one value.** A derivation admitting more than one lawful result is not unique, and
   XASSET-0020 §J.1 prohibits a point on that basis.
6. **Byte-identically reproducible** from the same frozen inputs, per XASSET-0020 §J.3 and §Q item 13.
7. **Not a model in disguise.** XASSET-0020 §M bars weighted or composite scores, confidence
   percentages, pairwise win tallies, hidden utilities or preference functions, optimizers, solvers,
   grid searches, sweeps, best-weight selection, averaging of incomparable metrics or representations,
   evidence-maturity weights, source-count advantage, freshness penalties, current-weight or incumbency
   priors, and post-hoc rounding or plugs. Operationally: if any step's coefficient, weighting,
   ordering, tolerance, cutoff, or selection could have been chosen differently without violating an
   admitted source's own prescription, the step is a model parameter and the derivation fails item 3.
   A "derivation" whose output moves when such a step is varied is a hidden model, and no NUM-0001
   label rehabilitates it.

#### H.4 Provenance that must exist

For the endpoint value itself:

1. **Complete NUM-0001 §4 field set** — canonical source location; every duplicate or fallback
   location; provenance class or classes and which component actually selected the binding value;
   supporting evidence artifact, or an explicit "none — doctrine" statement; current binding status;
   whether config-editable or hardcoded; and its review condition where applicable.
2. **A class from NUM-0001 §1 items 1–5**, per XASSET-0020 §L's endpoint row: externally imposed,
   mathematically derived, empirically calibrated, evidence-bounded governance selection, or
   provisional governance guardrail. Class 6, unsupported/unclassified, is disqualifying.
3. **Route-class coherence.** A §H.3 derivation is NUM-0001 class 2. A §H.2 statement may carry class
   1, 3, 4, or 5 — but a class 4 or class 5 value must have been selected by an effective governance
   authority competent for Level-1 endpoints, never by the application author, since XASSET-0021 §L
   forbids an application author from choosing a value and XASSET-0021 §F bars undocumented
   judgment.
4. **Honest labeling.** NUM-0001 §8 permits "empirically calibrated" only where evidence directly and
   uniquely favors that number over real tested alternatives; a sweep that merely fails to disprove a
   value establishes at most §7's evidence-bounded governance selection. NUM-0001 §11's false-precision
   prohibition applies in full.

#### H.5 Representation closure that must exist

Per XASSET-0021 §E:

1. **Point** — every representation required by its source authority is admitted and gives the same
   determinate direction for every driver bearing on the point.
2. **Range** — every endpoint is separately governed for every required representation, and their
   exact intersection is non-empty and valid under every representation.
3. **Failure** — any missing, unavailable, conflicted, or directionally disagreeing required
   representation makes the affected point or range ineligible. No majority, average, weighting,
   representative selection, or "most conservative" selection is permitted, and representation
   disagreement may never become a directional score.
4. **Additionally, for a range under any unresolved pair** — both endpoints independently and directly
   governed, and valid under *every possible direction* of that pair, per XASSET-0020 §I and §D.3
   above.

#### H.6 How conflicting admissible evidence is handled

Per XASSET-0021 §H, and never by averaging:

1. Two admitted same-authority drivers with contrary directions for the same question and scope yield
   `unable_to_determine`.
2. An admitted determinate direction combined with any admitted `unable_to_determine`, missing, stale,
   or conflicted required state yields `unable_to_determine`.
3. Different scopes are disclosed separately and never averaged.
4. Higher-authority conflicts follow GOV-0002 and block the affected item.
5. Two candidate endpoint values for the same endpoint quantity defeat uniqueness: a point is
   prohibited under XASSET-0020 §J.1, and no midpoint, average, mean, mode, "most conservative"
   selection, or precedence-by-recency may resolve them.
6. Bound intersection may narrow already-authorized endpoints; an empty intersection forces
   abstention.
7. Words such as "material," "significant," "sufficient," "meaningful," or "reasonable" in source
   prose create no threshold and no discretion, per XASSET-0021 §H.

#### H.7 When abstention remains mandatory

XASSET-0020 §J.3's triggers apply unchanged and in full: missing, unaccepted, hash-mismatched, or
stale-beyond-its-own-rule evidence; materially conflicted direct evidence; representation sensitivity
defeating lawful bounds; an unsupported required pair that XASSET-0020 §I cannot preserve bounds through; a
consequential parameter lacking NUM-0001 authority; reconciliation requiring a hidden plug, proxy,
prior, or redistribution; a constraint or Level-2 dependency inapplicable without substantive
discretion; or non-byte-identical repeated derivation.

To those, this determination adds only clarifications already implied above: abstention is mandatory
where no admitted DRIVER-classified, question-matched item states or prescribes the endpoint quantity
(§§H.1–H.3); where arithmetic would require an ungoverned rounding choice (§H.4 item 1 and
XASSET-0021 §G); and where a bound intersection is empty (§H.6 item 6).

Abstention remains "a complete governed outcome, not a defect to be patched with an assumption," per
XASSET-0020 §J.3.

#### H.8 Application of the test to the current snapshot

Applied to the XASSET-0021 §C snapshot, the test is not satisfied for any sleeve, by any route. That
is not a new finding: XASSET-0021 §F already determined that "The frozen snapshot contains no such
Level-1 endpoint authority for any sleeve," and §H.1 item 3 above explains mechanically why —
essentially every snapshot row is DISCLOSURE-only for current preference and so may not enter an
endpoint at all. This decision changes nothing about that state and creates no path around it.

### I. Clarification, not amendment

Every element of §§D, F, and H traces to already-accepted text: the two origination routes to
XASSET-0020 §J.1 item 6 and XASSET-0021 §F; DRIVER-only entry to XASSET-0020 §E.3; admission to
XASSET-0020 §F.1; snapshot limitation to XASSET-0021 §C.1; the closed arithmetic list and
contamination bar to
XASSET-0020 §M; exactness and rounding to XASSET-0021 §G; uniqueness to XASSET-0020 §J.1;
NUM-0001 coverage to XASSET-0020 §J.1 item 6 and XASSET-0020 §L; representation closure to
XASSET-0021 §E; conflict handling
to XASSET-0021 §H; constraint non-creation to XASSET-0020 §E.2 and XASSET-0021 §F; determinism to
XASSET-0020 §J.3 and §Q item 13; the range survival rule to XASSET-0020 §I and §J.2; the sequence and
completeness placement to XASSET-0019 §§H–I; and the RISK checkpoint to XASSET-0019 §J with RISK-0001's
own charter statement of its role.

No element loosens a bound, creates an origination route, admits a source class, relaxes a
prohibition, or supplies a value. Where this decision could not clarify without amending, it stopped
and recorded the gap instead — see §G and §J.

### J. One interpretive tension recorded rather than resolved by assertion

XASSET-0021 §O states that "To seek any future non-abstaining result, separate governance would
additionally have to admit question-matched evidence that actually closes the affected missing direct
pair(s), representation rule(s), and endpoint authority." Read as a strict conjunction, that would
require closing a missing pair even for a range, which would contradict XASSET-0020 §I's express
range-survival path and §J.2's omission of any pair-determinacy condition.

This decision resolves the tension the narrow way: XASSET-0021 §O is a general summary of the routes
to a
non-abstaining result, subordinate to the specific rules in XASSET-0020 §I and §J.2, and its own
qualifier "the *affected*" is read to exclude a pair that a §I-compliant range lawfully survives.
That reading is what §D.2 relies on.

Recorded honestly: this is the one place where a reviewer could reasonably reach the opposite reading.
If the strict-conjunction reading is preferred, the smallest corrective is a narrowly scoped amendment
to **XASSET-0021 §O's wording alone** — not to XASSET-0020 §I or §J.2, which are unambiguous. This
decision does not make that amendment and does not presume it unnecessary.

### K. Effect on the closure matrix, and application authority

No XASSET-0021 §N row is reclassified. The accepted matrix stands at 14 `CLOSED_DETERMINISTICALLY` /
14 `APPLICATION_MUST_ABSTAIN` / 2 `SEPARATE_PREREQUISITE_REQUIRED`, with
`application_time_author_or_reviewer_judgment_remaining: 2`, exactly as accepted. That CM-27 and CM-28
became substantively satisfied through XASSET-0022's effectivity is recorded in XASSET-0022 §§N–O; this
decision neither performs nor pre-empts their formal reclassification, which remains for whichever
future decision addresses application authority.

**Application authority remains WITHHELD.** XASSET-0021 §O's double gate is untouched, XASSET-0022
§P's mechanical enforcement is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, no
registered decision id or bound head is added by this filing, and no `intelligence/level1_application/`
artifact exists or is authorized. Nothing in §§D–H may be read as granting, implying, scheduling, or
partially granting application authority.

### L. What becomes scopeable

After this decision becomes effective, a future governance unit may be scoped with a known target for
the first time:

- A unit seeking a non-abstaining Level-1 **range** now knows it must supply, per sleeve, two
  independently governed endpoints meeting §H in full, each valid under every possible direction of
  every unresolved pair — and that it need not first obtain determinate RISK outcomes (§D.2).
- A unit seeking a Level-1 **point** now knows it must additionally close `downside_path_risk` and
  `recovery` to determinacy for every bearing pair, which the consumed RISK-0001 authority cannot
  supply (§D.1, §D.5).
- Either unit now knows the exact admissibility bar its evidence must clear (§H), including that a
  DISCLOSURE-classified source cannot support an endpoint however strong its content (§H.1 item 3).
- A future Level-2 unit now knows the ordering and per-sleeve conditions it faces (§F), and that the
  subset question is undecided (§G).

None of that is authorized by this decision. Each remains a separate future Lane G filing with its own
review, acceptance, merge, and post-merge verification.

### M. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files:

1. this decision;
2. `governance/decisions.yaml` — one catalog row;
3. `operations/WORKSTREAMS.yaml` — additive XASSET-0022 post-merge closeout and XASSET-0023 lane
   facts, with every prior gate's own text byte-unchanged; and
4. `test_portfolio_hq_dashboard_decisions.py` — the two mechanical decision-count assertions.

No supporting audit is created: the complete determinations and their citations are contained here.
No Intelligence, research-result, schema, generator, validator, allocator, target, holding, gate,
margin, chart, ladder, or protected portfolio file is changed.

### N. Reopen triggers

Reopen XASSET-0023 if: XASSET-0019's, XASSET-0020's, XASSET-0021's, or XASSET-0022's effective
identity changes; any XASSET-0021 §C path or hash changes, or the snapshot is lawfully replaced or
extended; a new evidence class, direct pair, representation rule, endpoint authority, or freshness
rule is proposed for use; an accepted RISK identity or disposition changes, or a new RISK study is
separately chartered; the liquidity or Level-2 architecture changes a boundary relied on here; a
partially non-abstaining Level-1 record becomes lawfully possible, making §G's deferred question
reachable; or a reviewer establishes the strict-conjunction reading of XASSET-0021 §O discussed in §J.

### O. Absolute non-authorization

This decision creates no endpoint, point, range, percentage, weight, target, or allocation; performs
and authorizes no research, evidence admission, direct-pair study, representation study, or RISK
study; produces no evidence conclusion or historical anchor; grants no application authority and
populates no authorization registry; creates no application artifact or directory; performs no Level-1
sizing and no Level-2 membership or sizing; makes no liquidity determination; changes no
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster,
cap, or margin state; authorizes no chart, ladder, backtest, optimizer, deployment, trade, order, or
brokerage action; adopts no portfolio policy; creates no XASSET-0021 snapshot successor and no
XASSET-0022 schema or version successor; and rewrites no accepted history.

## Rationale

The three questions this decision answers were each already answerable from filed text, but each was
answerable in more than one way — and the readings differ in what they would cost. Under one reading
of CM-25, a non-abstaining Level-1 range is unreachable without a new RISK study that RISK-0001's
consumed authority cannot supply; under the other, a range is reachable through endpoint evidence
alone. Under one reading of the Level-2 threshold, four non-null sleeve outcomes are prerequisite;
under another, an ordering is all that binds. Under no reading at all was "uniquely stated or uniquely
mathematically derived" operational enough for a future unit to know what to gather, or for a reviewer
to know what to reject.

Answering them by interpretation is cheaper and safer than answering them by expensive research aimed
at an undefined target. The asymmetry the text actually encodes — pair determinacy required for a
point, endpoint robustness required for a range — is not a loophole; XASSET-0020 §I's "valid under
every possible direction" is a stronger demand than determinacy would be for the narrow purpose it serves, because it
requires an endpoint to survive every resolution of the unknown rather than assuming one.

Defining endpoint admissibility carried the real risk in this filing: an operational test is exactly
where a sizing methodology could be amended while appearing to be explained. That risk is managed by
deriving every element from an existing sentence, by barring disclosures from arithmetic rather than
inventing a new admission tier, by closing "derivation" against XASSET-0020 §M's own list rather than
a new one, and by adding a single operational test for hidden models — whether any step could have
been chosen differently without violating a source's own prescription — that tightens nothing beyond
what XASSET-0020 §M already prohibits.

## Alternatives Considered

**Read CM-25 as an independent bar on both points and ranges.** Rejected: it would require reading
XASSET-0021 §K's "Because no independent endpoint survives" as surplusage and would contradict
XASSET-0020 §J.2, which omits pair determinacy, and XASSET-0020 §I, which expressly preserves ranges
through unresolved pairs.

**Read CM-25 as purely conditional for both outcome types.** Rejected: XASSET-0020 §J.1 item 3
independently requires determinate bearing pairs for a point, and XASSET-0021 §D forecloses marking
the RISK-driven driver classes `not_applicable`.

**Require all four sleeves non-null before any Level-2 work.** Rejected: no text supports it, and it
would relocate XASSET-0019 §H's completeness gate upstream of where §H expressly places it.

**Permit Level-2 sizing on any subset of non-abstaining sleeves.** Rejected as premature: §G shows the
text supports two readings, the question is unreachable today, and answering it now would create
sequencing policy on a hypothetical.

**Define endpoint admissibility by enumerating acceptable source types or a qualifying evidence
standard.** Rejected: enumerating what would qualify comes far closer to selecting the answer than
stating the structural test, and would have amended XASSET-0020 §F's closed admission contract rather
than clarifying it.

**Resolve XASSET-0021 §O's conjunction tension by amending it here.** Rejected: this filing's
authority is interpretive, the specific rules in XASSET-0020 §I and §J.2 already control, and §J
records the tension and the smallest corrective instead of performing it.

## Consequences

After this decision's own independent exact-head review, principal acceptance, merge, and post-merge
verification, the three ambiguities are closed for scoping purposes and a successor economic-evidence
unit can be specified against a known target. Application authority remains withheld; the closure
matrix is unchanged; no endpoint, sizing, membership, liquidity value, or policy exists or is
authorized; and the §G subset question and the §J wording tension remain open and recorded. Portfolio
configuration, allocator behavior, targets, holdings, gates, margin state, Level-2 work, and the
manual execution model are entirely unchanged.
