---
decision_id: XASSET-0024
date: 2026-08-15
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, LEVEL2-0001, RISK-0001, RISK-0002, RISK-0003, RISK-0004]
supporting_artifact: null
file: governance/decisions/XASSET-0024-level1-endpoint-basis-feasibility-determination.md
---

## Context

XASSET-0023 is effective (PR #322, merge `3050bcb72738da76dbfcb8f00a1935a83e9a85d2`). Its §H fixed the
*admissibility test* an endpoint must clear, and its §H.8 applied that test to the frozen XASSET-0021 §C
snapshot and found it unsatisfied for every sleeve by every route. Its §L then recorded what "becomes
scopeable": a future unit "now knows the exact admissibility bar its evidence must clear."

Knowing the bar is not the same as knowing the bar is clearable. XASSET-0023 deliberately did not
determine whether any source could *in principle* satisfy §H — only that nothing in the current snapshot
does. That leaves the next economic unit unable to answer the only question that determines whether it is
worth commissioning at all:

> Is there any lawful route by which a Level-1 sleeve-share LOWER or UPPER endpoint could ever come to
> exist under the methodology as accepted — and if so, what exactly must a source be?

Commissioning expensive endpoint research before answering that is the failure mode this repository has
already paid for once: PR #309's numeric-sizing implementation attempt was closed without merge after
repeated reviews established that the approach could not be made lawful, at the cost of the whole
implementation cycle. A feasibility determination is the cheap step that belongs before, not after.

This filing is that step. It is governance-only. It reads accepted authority and determines what that
authority already permits and forbids. It creates no endpoint, chooses no percentage, runs no research,
authorizes no application, amends no methodology, and adopts no portfolio policy.

**Preflight, independently re-verified this session, not inherited.** `origin/main` and local `HEAD` both
at `3050bcb72738da76dbfcb8f00a1935a83e9a85d2`; PR #322 confirmed merged via the GitHub API (head
`4e6c97cbefe5a5cf305bbd878276552d2e206f7b`, base `8f4da01cb2dfe020bb56335db7858c3c97ff0fdf`, 4 files, 4
commits); zero open pull requests; decision catalog 125 rows with `issues == ()`; `XASSET-0024` unused;
`APPLICATION_AUTHORIZATION_REGISTRY` empty; no `intelligence/level1_application/` artifact; the
XASSET-0021 §N matrix unchanged at 14 / 14 / 2. Every substantive premise below was re-read from the
merged accepted sources themselves rather than from any prior session's summary. A preflight report
described to this session was treated as search leads only; where its characterizations and the accepted
text diverge, §F records the divergence rather than repeating it.

## Decision

### A. Lifecycle, authority, and controlling identity

`OPS-0009` Lane G, governance-only. Effective on merge of this filing after its own independent
exact-head review, principal exact-head acceptance, and immediate post-merge verification. Until then it
determines nothing.

Controlling upstream identity, unedited by this filing: XASSET-0019 (Level-1 architecture), XASSET-0020
(methodology), XASSET-0021 (prerequisite closure and frozen snapshot), XASSET-0022 (application schema),
XASSET-0023 (feasibility and admissibility), NUM-0001 (numeric provenance), LEVEL2-0001, and the accepted
RISK corpus. Where this filing and any of them appear to differ, they control and this filing is wrong.

### B. Scope

In scope: determining, from accepted authority alone, (i) the exact quantity a Level-1 endpoint must
state, (ii) whether any lawful origin route for such an endpoint is constructible in principle, (iii)
what a qualifying source must be, (iv) which NUM-0001 classes may support a bound, (v) what makes an
evidence-bounded selection non-discretionary, (vi) why numerically plausible values in the corpus cannot
become endpoints, (vii) what a future source must do about representations, and (viii) whether RANGE or
POINT is the shorter critical path.

Out of scope and not performed: any endpoint, percentage, or range; any research, data acquisition, or
backtest; any representation rule; any direct-pair work; any RISK rerun, parameter reuse, or family
re-question; any application authorization or registry population; any snapshot or schema successor; any
Level-2 work; any liquidity determination; any sleeve-specific analysis. **No sleeve is selected,
preferred, or examined ahead of any other by this filing** — endpoint-basis feasibility is common to all
four sleeves and is settled here at that level.

### C. Determination A — the exact Level-1 endpoint quantity

Composed from XASSET-0020 §C, §K, and §L, XASSET-0021 §G, and XASSET-0023 §H's own definitional sentence.
No element is new.

**The quantity.** The share of one exact normalized unit of prospective, unlevered, asset-side capital
attributable to one named investable sleeve — the same quantity XASSET-0020 §K's reconciliation identity
sums as `sum(admitted_sleeve_points)`.

**Denominator.** Exactly one normalized unit, equivalently the whole `100%` asset state, per XASSET-0020
§C. It is a mathematical normalization, not a target and not a claim about current holdings. It contains
asset-side capital only and **excludes** debt, debt reduction, margin buying power, leverage, and buffer
state. It never uses current holdings, current weights, or current targets as priors.

**Units.** A dimensionless fraction of that unit — equivalently a percentage *of that unit* — carried at
exact source precision or as an exact rational derivation under XASSET-0021 §G. Never rounded before
comparison, intersection, constraint application, or reconciliation. Human display rounding is
non-authoritative.

**Relationship to `UNSIZED_UNASSIGNED_CAPITAL`.** XASSET-0020 §C provides that the four sleeve outputs are
**not** required to exhaust the unit, and §K makes the complement `UNSIZED_UNASSIGNED_CAPITAL`. An
endpoint therefore never derives from what other sleeves leave over: a bound obtained as a residual is a
plug, barred by §J.1 item 7, §J.2, and §M. Constraint clipping increases unassigned capital by exactly
the clipped amount and increases no sleeve.

**Debt and liquidity separation.** Debt reduction is a liability-flow control and never enters the
denominator (XASSET-0020 §N). A separately governed `LIQUIDITY_ASSET` may later occupy part of the same
asset state but is neither defined nor sized by any accepted decision, so no endpoint may assume, reserve
for, or net against one.

**What kind of object a bound is.** A LOWER or UPPER endpoint is **a governed bound on a normalized
share** — not a target, not an allocation, not a recommendation, and not a §E.2 CONSTRAINT. Under
XASSET-0020 §J.2 and §K the authoritative output of a range is the exact feasible *set* of sleeve vectors
lying inside the admitted endpoints; the method chooses no vector, midpoint, or combination from that set.
The distinction from a constraint is load-bearing and is fixed by XASSET-0023 §H.1 item 5 and XASSET-0021
§F: a constraint may clip or intersect a bound that already exists and can never originate one.

### D. Determination B — closed endpoint-origin-route feasibility table

XASSET-0023 §H states, of the two origination routes, "There is no third route." The table below is
therefore closed by accepted authority, not by this filing's judgment. Routes R1–R2 are the origination
routes; N1–N8 are the non-routes accepted authority already recognizes and bars, enumerated so that
"closed" is verifiable rather than asserted.

| # | Route | Lawful in principle? | What the source would have to be | NUM-0001 class | What invalidates it | Originate or clip? | Hidden-model risk |
|---|---|---|---|---|---|---|---|
| R1 | **Uniquely stated** by admitted DRIVER authority (XASSET-0020 §J.1 item 6; XASSET-0021 §F; XASSET-0023 §H.2) | **YES, conditionally** — every §H.2 item 1–6 condition and every §J condition below must hold | An item admitted under XASSET-0020 §F.1, inside the governed snapshot or a lawfully extended one, classified DRIVER under one of §E.1's six closed classes, whose own governed content states one exact value **for the §C quantity**, from an authority competent to fix a Level-1 sleeve share | 1, 3, 4, or 5 (§H.4 item 3) | Wrong quantity; DISCLOSURE or CONSTRAINT classification; incompetent authority scope; barred origin; a second lawful value; failed hash/effectivity/freshness | **Originate** | Low if the value is genuinely stated; the risk migrates upstream into how the stating authority chose it — see §E |
| R2 | **Uniquely mathematically derived** from admitted DRIVER inputs (XASSET-0023 §H.3) | **YES, conditionally** — narrowly, and narrower than it first appears | Admitted DRIVER inputs plus a derivation **the admitted source itself prescribes**, using only XASSET-0020 §M's closed arithmetic, exact, single-valued, byte-identically reproducible | 2 | Any composed, selected, or invented derivation (that is authorship, §H.3 item 3); any tunable coefficient, ordering, tolerance, cutoff, or selection (§H.3 item 7); ungoverned rounding; >1 lawful result | **Originate** | **High** — §H.3 item 7's test is the control: if any step could have been chosen differently without violating a source's own prescription, it is a model parameter and the derivation fails |
| N1 | Constraint application or bound intersection | **NO** | — | — | XASSET-0020 §E.2 ("never create preference"); XASSET-0021 §F ("may narrow already-authorized endpoints but may not create one") | **Clip only** | — |
| N2 | DISCLOSURE-classified content, however strong | **NO** | — | — | XASSET-0020 §E.3 (disclosures "must not enter arithmetic or decide a direction"); XASSET-0023 §H.1 item 3 | Neither | — |
| N3 | Selecting or combining across representations absent an accepted rule | **NO** | — | — | XASSET-0021 §E.3 (no majority, average, weighting, representative or "most conservative" selection) | Neither | — |
| N4 | Midpoint, symmetry convention, default, or minimum range width | **NO** | — | — | XASSET-0020 §L (parameter **eliminated**, does not exist); §J.2; §M | Neither | — |
| N5 | Residual, plug, or complement of the other sleeves | **NO** | — | — | XASSET-0020 §C, §J.1 item 7, §K, §M (`33.32` residual named) | Neither | — |
| N6 | Reusing a study-internal governed threshold or its derivation pattern | **NO** | — | — | XASSET-0023 §H.4 item 5, with the gold-parity gate as the worked counter-example — "**not a template, precedent, or permitted derivation pattern**" | Neither | — |
| N7 | Historical target, XASSET-0016/0018 output, current allocation, weight, tier, or gate | **NO** | — | — | XASSET-0020 §M contamination list; XASSET-0021 §F; XASSET-0022 §R mechanical scan | Neither | — |
| N8 | Application-author or reviewer selection, or a value stated in a task brief or decision prose | **NO** | — | — | XASSET-0021 §F ("analyst or reviewer preference," "undocumented judgment"); XASSET-0023 §H.2 item 2 — expressly including *this decision's own prose* | Neither | — |

**No route is invented here because the existing ones are difficult.** R1 and R2 are the accepted set;
N1–N8 are barred by name.

**One condition on R1 and R2 that deserves separate statement, because it is easy to miss.** XASSET-0023
§H.1 item 3 requires the endpoint-supporting item to be **classified DRIVER for the endpoint question**,
and XASSET-0020 §E.1 closes DRIVER to six named classes — `portfolio_function`,
`valuation_opportunity_cost`, `downside_path_risk`, `recovery`, `diversification_cobehavior`,
`sleeve_deployability`. Those six are *subject-matter* classes describing what evidence is about; none is
"sleeve share," and none excludes quantitative content either. A qualifying source must therefore be
admissible as a DRIVER under at least one of the six **on its own subject matter**, with its quantitative
statement intrinsic to that evidence rather than a number appended to it. A source whose only claim to
DRIVER status is that it contains a share figure does not satisfy §E.1. See §K.1 for the residual
question a reviewer may reasonably press here, recorded rather than assumed away.

### E. Determination C — evidence-bounded governance selection, and the anti-discretion test

This is the highest-value question in this filing, and the answer has a shape that is easy to get wrong
in a way that would quietly reintroduce discretion.

**E.1 — It is a lawful route, and it is not a third route.** NUM-0001 §1 class 4 is expressly named as a
permitted endpoint provenance class by XASSET-0020 §L's endpoint row and by XASSET-0023 §H.4 item 2. But
§H.4 item 3 fixes its structural position precisely: "A §H.3 derivation is NUM-0001 class 2. A §H.2
statement may carry class 1, 3, 4, or 5." **Class 4 is a provenance class carried by a route-R1 statement
— never an independent origination route, and never an application-time act.**

**E.2 — The consequence, stated plainly.** For class 4 to produce a lawful bound, the governance selection
must **already have happened, upstream, and be stated in the admitted source's own governed content**
before any application reads it. §H.4 item 3 requires the value to "have been selected by an effective
governance authority competent for Level-1 endpoints, never by the application author or a reviewer,"
and grounds that on XASSET-0021 §F's unconditional bar, calling it "the whole basis for this item."

So class 4 is **not** a licence for an application author to pick a value inside a range that evidence
established. It is a rule that relocates the choice out of the application and into a separately filed,
separately reviewed, separately accepted governance act. The application transcribes; it never selects.

**E.3 — The anti-discretion test.** A candidate class-4 bound is lawful only if all eight hold. The test is
constructed so that two independent application authors given the same admitted evidence cannot reach
different bounds — in the success branch because nothing is left to choose, and in the failure branch
because both must abstain identically.

1. **Upstream selection.** The selection was made and recorded by an effective governance authority
   competent for Level-1 endpoints, outside and before the application. (§H.4 item 3.)
2. **Question identity.** The range or constraint the evidence established is a range **of the §C
   quantity** — not of any other quantity that happens to be expressed as a percentage. (§H.2 item 1.)
3. **NUM-0001 §7 triple, complete.** The record states the defensible range or constraint the evidence
   established; **which specific value** within it governance chose; and the **stated economic — not
   statistical — reason** for that specific choice. A sweep that merely fails to disprove a value
   establishes at most this class and never calibration. (NUM-0001 §7, §8; §H.4 item 4.)
4. **Closed statement.** The authority's governed content fixes exactly one value for the bound, or a
   closed finite set together with a stated rule that fixes exactly one member of it. **If the authority
   leaves an open interval and states no rule fixing a member, no lawful bound exists** — the interval is
   evidence, not an endpoint, and any narrowing of it by the application is the barred selection.
5. **No interpolation and no tunable step.** §H.3 item 7's operational test applies to class 4 as well as
   to derivations: if any coefficient, weighting, ordering, tolerance, cutoff, or selection could have
   been chosen differently without violating the authority's own prescription, the value is a model
   parameter, and no NUM-0001 label rehabilitates it.
6. **Exactness.** Exact source precision; never rounded, inferred, reconstructed, or normalized into
   existence. (XASSET-0021 §G; §H.2 item 4.)
7. **Uniqueness and conflict.** No second lawful value for the same endpoint quantity exists anywhere in
   the admitted set. Two candidate values defeat uniqueness and yield `unable_to_determine`; no midpoint,
   average, mean, mode, "most conservative" selection, or precedence-by-recency may resolve them.
   (§H.2 item 5; §H.6 item 5.)
8. **Freshness and unavailability.** The source-owned currentness rule is applied exactly as written and
   its observed state recorded. A source with no governed currentness rule remains historical/disclosure
   evidence and may not become a current positive driver. No universal age threshold, freshness score, or
   penalty is invented. (XASSET-0020 §F.1; XASSET-0021 §H.)

**E.4 — What makes a bound evidence-bounded rather than discretionary.** Precisely items 1, 3, and 4
together. Discretion is not eliminated by calling a value "evidence-bounded"; it is eliminated by
requiring that the act of choosing be (i) performed by a competent authority rather than an author,
(ii) accompanied by a stated economic reason for *that* value rather than a neighbouring one, and
(iii) already closed in the source, so that reading it involves no choice. A record that states a range
and a value but no economic reason for the value fails item 3 and is class 6 in substance regardless of
its label — and class 6 is disqualifying under §H.4 item 2.

**E.5 — Class 5 carries the same relocation requirement, and one addition.** §H.4 item 3 treats class 5
identically to class 4 on who may select. NUM-0001 §6 adds that a provisional guardrail must carry an
explicit "provisional, not empirically calibrated" label and a stated review condition, which may be
calendar-based, event-driven, or evidence-driven. A provisional Level-1 bound is therefore lawful in
principle, and is honest only if it is labelled as provisional rather than presented as an economic
finding.

### F. Determination D — the contamination and wrong-denominator firewall

A firewall built only on "wrong denominator" would fail. This session verified, from committed sources,
that the corpus contains at least one barred value that has **exactly the right denominator and the right
units**. The firewall therefore has four limbs, and a candidate must clear all four.

**Limb 1 — wrong quantity or wrong question.** Numerically plausible, but not the §C quantity. Fails
§H.2 item 1 (same quantity) and XASSET-0020 §D's question-matching requirement.

| Candidate | What it actually measures | Verified this session |
|---|---|---|
| ETF `expense_ratio_pct` — GLD `0.4`, SPY `0.0945`, VEA `0.03`, VWO `0.06` | Annual fund cost as a percentage **of assets invested in that fund**. A different denominator entirely. | Read directly from `intelligence/etf_classification/{GLD,SPY,VEA,VWO}.yaml` |
| `GOLD_PARITY_CORRELATION_MIN` `0.995`, `GOLD_PARITY_RETURN_MAX_PP` `0.50`, `GOLD_PARITY_DRAWDOWN_MAX_PP` `2.00` | A correlation and two parity tolerances governing **conditional gold-peer admission**, not a share of anything | Read from `research/level1_sleeve_robustness/pre_registration.yaml`; each records `binding_scope: CONDITIONAL_GOLD_PEER_ADMISSION`, `valid_for_study_id: RISK-0001`, `evidence_status: NOT_CALIBRATED_NOT_EVIDENCE_BOUNDED`, `calibrated: false`, `evidence_bounded: false` |
| RISK provisional LOWER/HIGHER scenario magnitudes; R2/R3 values, directions, counts | Historical study reduction units under a single preregistered question whose accepted outcome is `unable_to_determine` at every level | XASSET-0023 §D.6; XASSET-0020 §M names R2/R3 explicitly |
| RISK materiality and representation-admission thresholds | Study-internal gates answering admission, not share | XASSET-0023 §H.4 item 5 |
| ETF internal country/sector weights; crypto dominance, staking, supply, or venue percentages | Shares **of a fund's or a market's own composition** — a within-instrument or market denominator | XASSET-0020 §F.2 marks these DISCLOSURE at Level 1 absent a representation rule |
| Equity valuation outputs | Per-share ranges with no accepted Level-1 aggregation rule | XASSET-0020 §F.2; XASSET-0021 §C.2 |

**Limb 2 — right quantity, barred origin. This is the limb a units test would miss.** Verified directly:
`intelligence/level1_sleeve_synthesis/numeric_sizing/equity.yaml` carries `provisional_target_pct: '18.67'`,
and the sibling records carry `14.67`, `16.67`, and the `33.32` residual. These are **not**
wrong-denominator quantities — they are sleeve shares of the normalized whole, in the right units, at the
right level. They are barred for an entirely different reason: XASSET-0020 §M names them as contamination
"mechanically barred from future input authority," XASSET-0021 §F bars any endpoint created from a
historical target or XASSET-0016/0018 output, and XASSET-0022 §R scans for the literal strings. The same
limb bars the six-way equal baseline, the fixed adjustment increment, and every current target, holding,
weight, tier, and gate.

The limb is not exhausted by the values that already exist. XASSET-0021 §F also bars **equal division**
as an endpoint origin, and that bar reaches constructions no scanner will ever match on a literal string —
a freshly computed one-quarter share across the four sleeves is barred exactly as the historical six-way
baseline is, not because the number appears on a list but because dividing the unit evenly is a
symmetry convention rather than admitted evidence about the §C quantity. The same is true of residual
balancing (§F Limb 2 read with N5) and of any bound reconstructed to match a value that once existed.
**A candidate that passes Limb 1 has proved nothing about Limb 2, and clearing XASSET-0022 §R's literal
scan is a floor rather than the boundary** — XASSET-0023 §H.2 item 6 says so in terms.

**Limb 3 — right quantity, right class, incompetent authority scope.** A source whose accepted authority
is effective for some other purpose "does not become Level-1 endpoint authority because it happens to
contain a number" (§H.2 item 3). The gold-parity gate is the worked case: real, committed, NUM-0001-classed,
and still failing three separate ways — its class forbids calling it calibrated, its scope answers an
admission question, and its `reuse_rule: NEW_GOVERNANCE_AUTHORITY_REQUIRED` with an already-met
`lapse_condition` defeats competent authority (§H.4 item 5; XASSET-0023 §D.6). It fixes the boundary and
is not a template.

**Limb 4 — constraint-only content.** A cap, ceiling, floor-as-limit, or concentration boundary that only
blocks, caps, or clips cannot originate a bound however precisely it is expressed (§E.2; §H.1 item 5;
XASSET-0021 §F).

**Why "it is numeric" is never itself an argument.** Every limb above describes a real, committed,
sometimes governed, sometimes NUM-0001-classed number. Numeric existence, provenance labelling, validator
success, and even correct units are each insufficient. Only question-identity, unbarred origin, competent
authority, and DRIVER classification together admit a value to consideration — and admission is still not
uniqueness.

### G. Determination E — the representation interface

This filing does **not** resolve CM-14, CM-15, CM-16, or CM-17, and invents no equity aggregation, no
SPY/VEA/VWO aggregation, no gold-peer selection, and no crypto composite rule. It determines only what
future endpoint-supporting evidence must do with representations.

A candidate endpoint survives the representation gate only by one of two paths, and otherwise abstains:

1. **Self-contained.** The endpoint-stating or endpoint-prescribing source's own governed content directly
   governs **every** representation its own authority requires, so no cross-representation combination is
   performed at all; or
2. **Separately ruled.** A separately accepted representation aggregation or selection rule, competent at
   Level 1, exists and lawfully maps the required representations — a rule that XASSET-0023 §H.5 records
   "does not exist anywhere at Level 1" today.
3. **Otherwise — mandatory abstention.** Any missing, unavailable, conflicted, or directionally
   disagreeing required representation makes the point or range ineligible. No majority, average,
   weighting, representative selection, or "most conservative" selection is permitted, and representation
   disagreement may never become a directional score. (XASSET-0021 §E.3.)

For a **range** specifically, XASSET-0021 §E.2 and XASSET-0023 §H.5 item 2 add that **every endpoint must
be separately governed for every required representation**, and their exact intersection must be non-empty
and valid under every representation. An endpoint governed for some representations and silent on others
does not satisfy this by inheriting the other endpoint's coverage.

**The gap is a rule, not evidence.** XASSET-0023 §H.5 is explicit that executed representation-sensitivity
evidence exists inside the accepted RISK corpus and that what is absent is an accepted combining rule.
A successor unit must therefore be scoped to **supply the missing rule under its own authority**, not to
re-discover evidence that already exists. That rule is not authorized here.

### H. Determination F — RANGE-first critical path

Sequencing only. No range, no value, no research.

**H.1 — A RANGE is structurally reachable without determinate RISK pair outcomes.** XASSET-0023 §D.2
determined that XASSET-0020 §J.2 omits any pair-determinacy condition, and that §I preserves a range
through unresolved pair evidence where both endpoints are independently and directly governed and remain
valid under every possible direction of the unresolved pair.

**H.2 — A POINT is materially harder, and the additional obstacle is not endpoint-shaped.** XASSET-0023
§D.1 determined that RISK independently bars a point: §J.1 item 3 requires every bearing pair determinate;
XASSET-0021 §D maps `downside_path_risk` and `recovery` to the accepted RISK dispositions and forbids
`not_applicable`; the accepted dispositions are `unable_to_determine`. That bar holds "even if every other
driver class became determinate and a lawful endpoint existed." Removing it requires determinate RISK
outcomes, which the consumed RISK-0001 authority cannot supply — all twenty of its consequential
parameters have lapsed and each requires new governance authority in its own recorded form (§D.6), and no
authority exists to re-question an individual family.

**H.3 — Therefore.** Future economic work seeking a non-abstaining Level-1 outcome should establish RANGE
feasibility **before** POINT feasibility, unless the evidence itself uniquely supplies a point — in which
case the point route is available on its own terms and this sequencing preference does not bar it. This is
a recommendation about the order in which questions are asked, not a preference for ranges over points as
outputs, and it authorizes neither.

**H.4 — What "valid under every possible direction" actually requires.** XASSET-0020 §I calls the
surviving construct "a non-inferential intersection of already-authorized bounds, not a derived
relationship." The operative requirement is therefore stronger and simpler than case-testing: an endpoint
qualifies only if the unresolved pair **is not an input to it at all**. An endpoint whose value would move
under some direction of that pair is pair-dependent by construction and fails; showing that it happens to
survive each enumerated direction is not the same as showing it never consumed the pair. Direction-
invariance by independence is the test; direction-robustness by inspection is not.

### I. Determination G — outcome

The outcome vocabulary is closed to exactly three values, and exactly one is selected:

- `ENDPOINT_BASIS_EXISTS_UNDER_CURRENT_METHODOLOGY` — a lawful endpoint-origin route is constructible in
  principle under accepted authority as it stands, and the next unit's task is evidence and authority;
- `ENDPOINT_BASIS_REQUIRES_METHODOLOGY_AMENDMENT` — accepted authority cannot support endpoint creation,
  and a named clause must be amended before endpoint research could lawfully be commissioned;
- `UNABLE_TO_DETERMINE` — accepted authority genuinely cannot resolve whether a route exists.

**Outcome: A — `ENDPOINT_BASIS_EXISTS_UNDER_CURRENT_METHODOLOGY`.**

At least one lawful endpoint-origin route is constructible in principle under the methodology exactly as
accepted, with no amendment required. The determination rests on four express provisions, not on the
absence of a prohibition:

1. **XASSET-0020 §L's endpoint row** states the endpoint value is "Not chosen here; must be externally
   imposed, mathematically derived, empirically calibrated, evidence-bounded governance selection, or
   provisional guardrail **under a later exact record**," with basis "Exact future application authority."
   That is an express contemplation of a future record supplying the value, not merely silence.
2. **XASSET-0023 §H.4 items 2–3** map the five permitted classes onto the two routes and expressly permit
   class 4 and class 5 values "selected by an effective governance authority competent for Level-1
   endpoints."
3. **XASSET-0023 §H.1 item 2** expressly contemplates evidence in "a snapshot lawfully replaced or
   extended by a separate future authorization," so the frozen snapshot's current contents are not a
   permanent ceiling.
4. **XASSET-0021 §O** names "endpoint authority" as one of the things separate governance "would
   additionally have to admit," i.e. a reopen path — describing an evidence-and-authority gap, not a
   methodological impossibility.

**What is missing is therefore a qualifying source and a competent authority, not a permission.** No
clause needs amending to allow an endpoint to exist; what does not yet exist is (i) admitted,
DRIVER-classified, question-matched evidence that states or source-prescribes the §C quantity, and (ii)
for a class 4 or class 5 bound, a filed governance act competent for Level-1 endpoints that has made and
recorded the selection with NUM-0001 §7's complete triple.

This outcome is deliberately **not** a prediction that such a source can be produced, cheaply or at all.
Feasibility in principle is a much weaker claim than availability in fact, and §F shows how many
plausible-looking candidates fail. The value of Outcome A is precisely that it tells the next unit its
work is *sourcing and authority*, not methodology reform — and that a proposal to amend the methodology in
order to make endpoint creation easier would be solving the wrong problem.

### J. Minimum evidence properties for the next research or authority unit

A future unit seeking a lawful Level-1 bound must produce a source satisfying **all** of the following.
This list is a restatement of accepted requirements assembled in one place; it adds none.

**J.1 Admission.** Exact path and content/file SHA-256 match; accepted/effective governing authority; own
validator passes where one exists; question matches; every governed freshness condition passes.
(XASSET-0020 §F.1.)

**J.2 Snapshot position.** Present in XASSET-0021 §§C.2–C.3, or in a snapshot **lawfully replaced or
extended by a separate future authorization**. An application may never silently add a later file,
refreshed observation, or new source class. (XASSET-0021 §C.1; XASSET-0023 §H.1 item 2.)

**J.3 DRIVER classification on subject matter.** Classified DRIVER under at least one of XASSET-0020
§E.1's six closed classes, on the source's own subject matter, with the quantitative statement intrinsic
to that evidence. Not DISCLOSURE. Not CONSTRAINT. (§E.1–§E.3; §H.1 items 3 and 5.)

**J.4 Question identity.** States or source-prescribes a value for **the §C quantity** — the share of one
normalized unit of prospective unlevered asset-side capital attributable to one named sleeve — and clears
all four §F limbs.

**J.5 Competent authority.** The stating authority's accepted/effective scope extends to fixing a Level-1
sleeve share. (§H.2 item 3.)

**J.6 Route compliance.** Either R1 in full (§H.2 items 1–6) or R2 in full (§H.3 items 1–7). For R2, the
derivation must be **source-prescribed**, not composed by the application.

**J.7 Provenance.** Complete NUM-0001 §4 field set; a class from NUM-0001 §1 items 1–5 (class 6
disqualifying); route-class coherence per §H.4 item 3; honest labelling per NUM-0001 §8 and §11. For class
4, the full §E.3 eight-item anti-discretion test. For class 5, additionally NUM-0001 §6's explicit
provisional label and stated review condition.

**J.8 Uniqueness.** No second lawful value for the same endpoint quantity anywhere in the admitted set.

**J.9 Representation closure.** §G path 1 or path 2; otherwise abstain. For a range, every endpoint
separately governed for every required representation, with a non-empty valid intersection.

**J.10 Pair independence.** For any unresolved pair, the endpoint does not consume that pair as an input
at all (§H.4 above).

**J.11 Exactness and determinism.** Exact source precision or exact rational derivation; no ungoverned
rounding; byte-identical reproduction from the same frozen inputs.

**J.12 Reconciliation feasibility.** Exact set-valued reconciliation under XASSET-0020 §K remains feasible
with no negative complement, no plug, no proxy, and no redistribution.

**Answering the two structural questions the next unit will ask.** *Must LOWER and UPPER share an evidence
class or source?* **No — and independence is affirmatively required.** XASSET-0020 §J.2 requires both
endpoints "separately traceable"; XASSET-0021 §F applies the endpoint rule "independently for each bound";
XASSET-0021 §E.2 requires each "separately governed"; XASSET-0023 §H.5 item 4 requires both "independently
and directly governed." Two bounds may therefore come from different sources carrying different NUM-0001
classes — for example an externally imposed upper bound and an evidence-bounded governance-selected lower
bound — provided each independently satisfies J.1–J.12 and their exact intersection is non-empty and valid
under every required representation and every possible direction of every unresolved pair. What is **not**
permitted is deriving one bound from the other, or letting one bound's representation coverage stand in
for the other's. *And which NUM-0001 classes may support a bound?* Classes 1, 2, 3, 4, and 5 — class 2 via
R2 and classes 1, 3, 4, 5 via R1. Class 6 is disqualifying.

### K. Recorded rather than resolved

**K.1 — Whether §E.1's six DRIVER classes house a magnitude statement.** §D above determines that they do,
reading the six as subject-matter classes none of which excludes quantitative content, so that a source
about (for instance) a sleeve's evidenced portfolio function or its deployability may state a quantitative
consequence of that function or friction. A reviewer could reasonably press the contrary reading: that
§E.1's six are all phrased as *preference* classes and that a share magnitude is a different kind of claim,
in which case no admitted item could ever be "classified DRIVER for the endpoint question" and both R1 and
R2 would collapse — making the correct outcome **B**, with the smallest corrective a narrowly scoped
clarification of XASSET-0020 §E.1 alone. **This filing does not make that amendment and does not presume
it unnecessary.** It records the dependency plainly: Outcome A is conditional on the subject-matter
reading of §E.1, and §D states the requirement strictly enough that a source cannot qualify merely by
containing a share figure.

**K.2 — Circularity, addressed rather than elided.** §E.2 requires a class-4 or class-5 bound to have been
selected by a competent governance authority before the application reads it, and §J.2 requires that
authority's record to enter an admitted snapshot. A reviewer may ask whether that is a real route or a
relocation of the same discretion into a different file. It is a real route, for one reason: the relocated
act is subject to independent exact-head review, principal acceptance, and merge, and must carry
NUM-0001 §7's economic reason for *that specific value*, whereas an application-time selection is subject
to none of those and is barred outright. The discipline is not that discretion vanishes; it is that
discretion becomes reviewable, attributable, and refusable. Nothing here makes such a future record easier
to justify — §F applies to it in full.

**K.3 — The preflight described to this session was not retained as repository authority.** Its
characterizations were treated as search leads and independently re-verified. Two divergences are recorded
for accuracy: the historical `18.67 / 14.67 / 16.67 / 33.32` values are **not** a wrong-denominator
failure, as §F Limb 2 establishes — they are the right quantity barred by origin, a materially different
failure mode; and the RISK gold-parity gate's disqualification is not primarily a denominator problem
either, but a three-way failure of class labelling, binding scope, and lapsed competent authority. A
firewall built on the preflight's framing alone would have admitted `18.67`.

**K.4 — Not reopened here.** XASSET-0023 §G's Level-2 subset question; §J.1's XASSET-0021 §O
strict-conjunction tension; §J.2's gold-representation labelling difference. None bears on any
determination above, and none is resolved.

### L. Effect on the closure matrix, and application authority

No XASSET-0021 §N row is reclassified. The matrix stands exactly as accepted at 14
`CLOSED_DETERMINISTICALLY` / 14 `APPLICATION_MUST_ABSTAIN` / 2 `SEPARATE_PREREQUISITE_REQUIRED`, with
`application_time_author_or_reviewer_judgment_remaining: 2`. CM-18, CM-19, CM-25, and CM-26 remain
`APPLICATION_MUST_ABSTAIN`; this filing supplies no endpoint and therefore changes nothing about them.

**Application authority remains WITHHELD.** XASSET-0021 §O's double gate is untouched, XASSET-0022 §P's
mechanical enforcement is untouched, `APPLICATION_AUTHORIZATION_REGISTRY` remains empty, and no
`intelligence/level1_application/` artifact exists or is authorized. Nothing in §§C–K may be read as
granting, implying, scheduling, or partially granting application authority. **No all-abstention
application is authorized either** — it would exercise the mechanism without closing CM-19 or CM-26 and
without advancing Level-1 sizing.

### M. Governance package and WORKSTREAMS synchronization

This filing touches exactly four tracked files: this decision; `governance/decisions.yaml` (one catalog
row); `operations/WORKSTREAMS.yaml` (additive XASSET-0023 post-merge closeout and XASSET-0024 lane facts,
every prior gate's own text byte-unchanged); and `test_portfolio_hq_dashboard_decisions.py` (the two
mechanical decision-count assertions).

No supporting artifact is created. This is a governance determination, not a research result, and its
complete reasoning and citations are contained here. No Intelligence, research, schema, generator,
validator, allocator, target, holding, gate, margin, chart, ladder, or protected portfolio file is
changed.

### N. Reopen triggers

Reopen XASSET-0024 if: XASSET-0019's, XASSET-0020's, XASSET-0021's, XASSET-0022's, or XASSET-0023's
effective identity changes; XASSET-0020 §E.1's driver classes or §L's endpoint row is amended; any
XASSET-0021 §C path or hash changes, or the snapshot is lawfully replaced or extended; a candidate
endpoint source is proposed and its §J compliance must be assessed; a Level-1 cross-representation
aggregation or selection rule becomes accepted; separate governance grants reuse authority over any
lapsed RISK parameter, or a new RISK study is chartered; NUM-0001's classes, §7 requirements, or §8
standards change; a reviewer establishes the contrary reading of §E.1 recorded at §K.1, or the
strict-conjunction reading of XASSET-0021 §O; or the liquidity or Level-2 architecture changes a boundary
relied on here.

### O. Absolute non-authorization

This decision creates no endpoint, bound, point, range, percentage, weight, target, or allocation, and
selects no sleeve; performs and authorizes no research, endpoint research, data acquisition, backtest,
evidence admission, direct-pair study, representation study, or RISK study; produces no evidence
conclusion or historical anchor; commissions no research charter and defines no research question beyond
identifying the exact future question a later unit must answer; grants no application authority, including
for an abstention-only application, and populates no authorization registry; creates no application
artifact or directory; amends no methodology and supplies no representation rule; performs no Level-1
sizing and no Level-2 membership or sizing; makes no liquidity determination; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin state;
authorizes no chart, ladder, optimizer, deployment, trade, order, or brokerage action; adopts no portfolio
policy; creates no XASSET-0021 snapshot successor and no XASSET-0022 schema or version successor; grants
no reuse authority over any lapsed RISK parameter or result and no authority to re-question any RISK
family; edits no accepted decision; and rewrites no accepted history.

## Rationale

The next unit in this program is expensive. It must either commission economic research aimed at
producing a Level-1 bound, or amend the methodology so that bounds can be produced. Choosing between those
two without first determining which one the accepted corpus actually calls for is how PR #309's cycle was
lost — an implementation pursued to completion before establishing that it could be made lawful.

The determination separates two things that had been running together. XASSET-0023 fixed the
*admissibility test* and applied it to the current snapshot, finding nothing passes. That is a statement
about the snapshot. It is silent on whether anything *could* pass, and a reader could reasonably infer
from §H.8's flatness that the methodology is closed against endpoints altogether — which would make
amendment the necessary next step. It is not closed. XASSET-0020 §L's endpoint row, XASSET-0023 §H.4's
class mapping, §H.1 item 2's extendable snapshot, and XASSET-0021 §O's reopen-path language each
affirmatively contemplate a future endpoint arriving through a later exact record. Recording that
explicitly redirects the next unit from methodology reform, which is not needed, to sourcing and
authority, which is.

The evidence-bounded-governance-selection analysis is the part most likely to be misused if left
unstated. Class 4 is the only class that sounds like it authorizes judgment, and the natural misreading —
that an application author may pick a value inside an evidence-established range — would reintroduce
exactly the discretion this program has spent several decisions eliminating. XASSET-0023 §H.4 item 3
already forecloses it, but tersely, in a clause about route-class coherence. Stating the relocation
requirement plainly, and giving it a test whose failure branch is as deterministic as its success branch,
makes the boundary usable rather than merely present.

The firewall's two-limb structure is the one finding here that is not a restatement. Verifying the barred
values directly rather than accepting a summary showed that `provisional_target_pct: '18.67'` and its
siblings are not wrong-denominator quantities at all — they are sleeve shares of the normalized whole, in
the right units, at the right level, barred purely by origin. A future author testing candidates only for
denominator correctness would admit them. Recording that a candidate can pass every units check and still
be categorically barred is worth more than another restatement of the prohibition list.

Finally, the RANGE-first sequencing determination follows from XASSET-0023 §D's asymmetry, but its
practical consequence had not been drawn: the point route's blocker is not endpoint-shaped at all. It is
RISK pair determinacy, which no endpoint work can address and which the consumed RISK-0001 authority
cannot supply. A unit that pursued a point first would spend its effort on the endpoint problem and then
discover an independent bar it never had authority to remove.

## Alternatives Considered

- **Determine Outcome B and specify an amendment.** Rejected. It would have required finding that accepted
  authority forbids endpoint creation, and four express provisions say the opposite. Recommending an
  amendment where none is needed would loosen a methodology that is working as designed, and would invite
  the loosening to go further than the diagnosis warranted. The one genuine route by which B could be
  correct is recorded at §K.1 rather than suppressed.
- **Determine Outcome C, `UNABLE_TO_DETERMINE`.** Rejected. The question is answerable from accepted text;
  the four provisions in §I are express, not inferred. Abstaining would have been abstention as a
  substitute for reading, which XASSET-0020 §J.3's own framing of abstention as "a complete governed
  outcome, not a defect to be patched" does not license in the opposite direction.
- **Force Outcome A by weakening the DRIVER-classification requirement.** Rejected explicitly. §D states
  the requirement strictly — DRIVER status on subject matter, quantitative statement intrinsic to the
  evidence — precisely so that Outcome A cannot be cashed out by a source that merely contains a share
  figure. A permissive reading would have made the outcome easy and useless.
- **Also specify the missing cross-representation aggregation rule.** Rejected. XASSET-0023 §H.5 identifies
  it as the missing piece, and supplying it here would be an amendment to Level-1 methodology performed
  inside a feasibility determination, without its own authorization or review. §G states what a rule must
  achieve and leaves its creation to a unit scoped for it.
- **Commission the endpoint research charter in the same filing.** Rejected. The principal's authorization
  is expressly bounded against running research or issuing a charter, and the two acts have different
  evidentiary bases: this one reads accepted text, the other would have to justify a research design.
  §J identifies the exact future question; it does not commission it.
- **Begin with a single sleeve, or with GLD as the narrowest representation case.** Rejected. Endpoint-basis
  feasibility is common to all four sleeves and is prior to any sleeve-specific work; starting with a
  sleeve would have produced a sleeve-shaped answer to a structural question and would have been
  sleeve selection without authority.
- **Authorize an abstention-only application to exercise the mechanism.** Rejected, and expressly barred at
  §L. It would demonstrate XASSET-0022's machinery while closing neither CM-19 nor CM-26 and advancing no
  Level-1 sizing.
- **Create a supporting audit artifact.** Rejected. Repository convention creates one where a filing's
  substance is research output or a large enumeration; here the determinations and their citations are the
  decision, and XASSET-0021, XASSET-0022, and XASSET-0023 each carried comparable analytical weight with
  `supporting_artifact: null`.

## Consequences

A future unit seeking a lawful Level-1 bound now knows, before spending anything, that the methodology
permits one, that no amendment is required to allow it, and that its work is to obtain a qualifying source
and — for a class 4 or class 5 bound — a competent governance authority willing to make and record the
selection with an economic reason for that specific value. It knows the twelve properties that source must
satisfy (§J), the eight-item test a class-4 selection must pass (§E.3), the four limbs any candidate value
must clear (§F), the two representation paths available (§G), and that RANGE feasibility is the shorter
critical path because the point route's additional blocker is RISK determinacy rather than anything
endpoint-shaped (§H).

It also knows what will not work, by name: constraints, disclosures, midpoints, residuals, study-internal
thresholds, historical and current anchors, author or reviewer selection, and — the finding least likely
to be anticipated — values that are already sleeve shares of the normalized whole in exactly the right
units, which are barred by origin rather than by arithmetic.

Nothing about the portfolio changes. Application authority remains withheld, the closure matrix stands at
14 / 14 / 2, the authorization registry remains empty, no application artifact exists, and no endpoint,
range, percentage, weight, target, allocation, or trade is created, recommended, or authorized by this
filing. XASSET-0019 through XASSET-0023, NUM-0001, LEVEL2-0001, the RISK corpus, `intelligence/`,
`research/`, and every protected portfolio file are byte-unchanged.
