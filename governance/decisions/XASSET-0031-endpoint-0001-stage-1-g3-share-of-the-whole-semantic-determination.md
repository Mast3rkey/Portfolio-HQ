---
decision_id: XASSET-0031
date: 2026-08-16
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_g3_share_of_the_whole.py
---

## Context

### Live preflight

Verified independently before any mutation, against live GitHub and git state rather than inherited
narrative:

| Fact | Verified |
|---|---|
| GitHub `main` / `origin/main` / local `HEAD` | all three `3bcb137981d7dea5362ebca05deba60830076bee` |
| PR #329 (`XASSET-0030`) | merged/closed; merge parents `3cc15d58…` + accepted head `0a7e0216…` |
| Merge-commit CI | run `31970647289` / job `95222489853`, completed/success, `head_sha` matching |
| Open pull requests | **0**; working tree clean; stash empty; sole worktree |
| `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` |
| `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` |
| Construction universe | regenerated live: **680** constructions, **48** cells, `73c0965e…5224` |
| All six `LOAD_BEARING_RELPATHS` | re-hashed against `HEAD`: **all `MATCH`** |
| `new_execution_is_authorized()` | `False` — "no attestation present" |
| Lane / attestation / claim / completion / ledger / `stage1_results.yaml` | **all absent** |
| `XASSET-0031` | unused across every tracked file |

**`ATTEMPT_1` is intact, unclaimed, and unconsumed, and remains so after this filing.**

### The question this unit answers

`XASSET-0030` determined `GATE_EVALUATION_METHOD_NOT_CLOSABLE` — six of twelve gates closable under
current authority, six not — and recorded that **`G3` alone is independently sufficient** for that
negative. `G3` is therefore the critical-path semantic prerequisite, and `XASSET-0030` §G.A named it
first.

> **What exact semantic condition permits evidence about a Level-1 sleeve or comparison to support a
> LOWER or UPPER share of one normalized unit of prospective unlevered asset-side capital, rather than
> merely supporting direction, preference, function, risk, recovery, diversification, or
> deployability?**

The canonical gate states the same question mechanically (`pre_registration.yaml` line 790):

> "Would the candidate state the `XASSET-0024` §C quantity — a share of one normalized unit of
> prospective unlevered asset-side capital — rather than a quantity in the sleeve's own,
> within-instrument, market, per-share, or leverage-bearing denominator?"

`controlling_authority: XASSET-0024_SECTION_C_AND_SECTION_F_LIMB_1`; `failure_disposition:
BLOCKED_CATEGORICALLY`.

### Correction history

**Correction 1** — after independent FULL exact-head review `4947565573` (`CHANGES REQUIRED` —
0 BLOCKING / 2 MAJOR / 1 MINOR / 1 NOTE) at head `209e5d33c119c236b977e27bb44b640dceda3417`, whose
exact-head CI run `31978535243` / job `95241592673` was completed/success. Both MAJOR findings were
reproduced against controlling text before any edit.

**MAJOR 1** — §C.1/§C.2 and the §E R1/R2 table over-narrowed lawful **R2** by conflating *where a
derivation is authored* with *where it is executed*. `XASSET-0024` §D's R2 row invalidates a derivation
that is "composed, selected, or invented" or carries "any tunable coefficient, ordering, tolerance,
cutoff, or selection", and §J.6 requires it be "source-prescribed, not composed by the application" —
every invalidator is authorship or choice, none is the act of computing. The prior text ("no downstream
normalization is lawful, by any mechanism, ever"; "under both R1 and R2 the normalization has already
occurred upstream") would have permanently forbidden constructions accepted authority leaves
conditionally lawful. Corrected: §C.1 now turns on **who fixes the denominator**; §C.2 splits limb A
(downstream-authored — barred) from limb B (mechanical execution of a complete, choice-free
source-prescribed derivation — not categorically barred), with §H.3 item 7 as the operative control;
the §E table gains a "where the arithmetic may run" column.

**MAJOR 2** — §D's capability table recorded "Direction = **YES**" class-wide and the prose asserted
"Every one of the four values is a direction." `XASSET-0020` §E.1 says only that the six classes "**may
support**" preference — an admission rule, not a realization finding — and §H reaches `indistinguishable`
on a determinate tie and `unable_to_determine` on missingness/conflict/staleness, neither of which is a
positive or negative direction. Corrected: the column reads **PERMITTED (source/result-dependent)**,
and a per-value table records which two of the four are directional and which two are not. What the
vocabulary does establish — that **none of the four carries a magnitude** — is preserved, and is all
this unit relies on.

**MINOR 1** — `operations/WORKSTREAMS.yaml` carried `pr: null` / `active_pr: null` after PR #330 was
opened. Corrected factually; no historical gate text rewritten.

**Neither correction changes the `SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE` determination, the
`XASSET-0030` 6/6 gate map, §K.1's unresolved state, §E.1's unamended state, R1/R2 route authority, or
any canonical semantics.** No R2 construction is found to clear `G3`.

**Correction 2** — after independent DELTA review `4947665744` (`CHANGES REQUIRED` — 0 BLOCKING /
1 MAJOR / 0 MINOR / 1 NOTE) at head `f19dde2cd121f9e8801fc028ee600b0860cbedc7`, whose exact-head CI run
`31980541182` / job `95246422723` was completed/success. That review recorded correction 1's two
findings as substantially corrected and raised one **stale mirror** of MAJOR 1 surviving in §D.

**MAJOR 1** — §D's five-class bullet still read: "Their native denominators are the sleeve's own
position, the pair, or the alternative. **Reaching the whole from any of them would require precisely
the mapping §C.2 bars.**" After correction 1 that is false: §C.2 limb B and the §E R2 row expressly
leave a complete, zero-free-choice, source-prescribed R2 derivation **not categorically barred**. The
sentence would have let a successor cite §D for a **class-wide negative** against
`valuation_opportunity_cost`, `downside_path_risk`, `recovery`, `diversification_cobehavior`, and
`sleeve_deployability` — converting a reserved per-source question into a settled impossibility for
five of six classes. Corrected: the bullet now records native scope as **an observation only**, states
that a source in one of the five reaches the §C quantity by satisfying §C.1 on its own terms (R1's
direct statement, or a complete source-prescribed R2 derivation), keeps §C.2 limb A's bar on any
application-composed conversion, and states that **neither satisfaction nor impossibility is determined
here for any class**. The valid native-scope facts (`SELF`/`PAIR`/`ALT`, no class whole-scoped) are
preserved unchanged.

**Sweep.** The decision, the `WORKSTREAMS` `xasset0031` mirror, the PR body, and the focused tests were
each searched for equivalent claims. **No other live stale mirror exists.** The `WORKSTREAMS` mirror
states only "no class carries a whole-portfolio scope" — a native-scope fact with no barred-mapping
inference — and was therefore left unchanged. Two residual matches in the decision and PR body are the
**correction-1 history quoting the prior head**, which is intentional documentation rather than a live
claim.

**Correction 2 changes no determination either**: the core NEGATIVE, the 6/6 gate map, §K.1, §E.1,
R1/R2 route authority, and canonical semantics are all untouched, and `G3` remains source-dependent and
RESERVED for every class.

## Decision

### A. Determination — `SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE`

The outcome vocabulary is closed to three values and exactly one is selected:

- `SHARE_OF_THE_WHOLE_CONDITION_CLOSABLE` — a deterministic rule exists that two independent conforming
  executors must apply identically to all 680 constructions;
- **`SHARE_OF_THE_WHOLE_CONDITION_NOT_CLOSABLE`** — the semantic condition is statable, but its
  *satisfiability* is expressly reserved by accepted authority and cannot be closed by this unit;
- `UNABLE_TO_DETERMINE` — accepted authority cannot resolve even what the condition is.

**The answer is NEGATIVE, and it is a bounded negative rather than a blank one.** The semantic
condition **is** exactly statable from accepted authority, and §C states it. What cannot be closed is
whether any construction satisfies it — which is precisely what `XASSET-0027` §J.3 and §M.3 reserve to
per-candidate study findings.

This unit therefore delivers three positive sub-determinations (§C), a per-class capability analysis
(§D), and the exact named prerequisite (§G) — and stops at the reservation rather than legislating
through it.

**`G3` remains NOT CLOSABLE. The `XASSET-0030` 6/6 snapshot is unchanged. Stage 1 remains UNARMED and
NOT EXECUTABLE.** This filing changes no canonical byte, no universe, no hash pin, and no authorization
state.

### B. What this unit reproduced before determining anything

All reproductions used the real modules against the live frozen universe. No results document, lane
state, or Stage-1 output was created, and no gate was evaluated for any construction.

**B.1 — Whole-denomination is *stipulated* in all 680 constructions.** Every registered construction's
frozen `hypothetical_source_requirements` carries requirement **R5** verbatim: "The bound must be
intrinsic to the source's own statement rather than derived by the application, **and must be expressed
against the normalized asset unit**." Counted mechanically: **680 / 680**.

**B.2 — All 680 constructions are hypothetical.** `source_architecture` is
`HYPOTHETICAL_SOURCE_ARCHITECTURE` for every entry, without exception. **No source exists anywhere whose
declared denominator could be inspected.**

**B.3 — Each DRIVER class has exactly one native scope, and none of the six is the whole.** Read from
each construction's own frozen **R3** subject-matter clause and its construction-id scope tag:

| Native scope | Driver classes | Constructions |
|---|---|---|
| `SELF` — "the sleeve's own … evidence" | `portfolio_function`, `sleeve_deployability` | 80 |
| `PAIR` — "direct … pair evidence for the unordered pair …" | `diversification_cobehavior` | 120 |
| `ALT` — "evidence directly comparing the sleeve with …" | `downside_path_risk`, `recovery`, `valuation_opportunity_cost` | 480 |

No class carries a whole-portfolio scope tag. This is the mechanical form of `XASSET-0025` §J's finding
that "**There is no sleeve-independent DRIVER class**" and of `XASSET-0027` §J.1's "Every one of
`XASSET-0020` §E.1's six DRIVER classes is defined on a sleeve or on a comparison; the endpoint is a
share **of the whole**."

**B.4 — Nothing anywhere produces a `G3` result.** The 680 universe entries carry exactly ten identity
fields, none of which is a gate outcome; no derivation function in the preregistration validator emits
one. `G3` is decided by a human analytical act under the charter — the validator says so of itself.

**B.5 — The ambiguity, stated exactly.** A construction simultaneously requires **R3** (subject matter
scoped to a sleeve, a pair, or a comparison) and **R5** (a bound denominated in the whole). `G3` asks
whether that conjunction is lawfully satisfiable. Deriving `PASS` from R5's own presence is
by-construction inference, which `XASSET-0030` §E's Standard 1 rejects in terms: "**(a) a specification
requiring property P** is never by itself **(b) proof that P is lawfully satisfiable.**"

### C. What this unit *does* close — three positive sub-determinations

Each is a restatement of accepted authority assembled in one place. None adds a rule.

**C.1 — The semantic condition, stated exactly.**

> Evidence supports a LOWER or UPPER share of the whole **if and only if the `XASSET-0024` §C
> denominator — one normalized unit of prospective, unlevered, asset-side capital — is fixed by the
> source's own governed content**: either **stated** by the source itself at exact source precision
> (R1), or produced by the source's **own complete prescribed derivation** (R2), in each case as the
> denominator that content is measured against. A denominator that is **supplied, chosen, composed,
> selected, or invented by a downstream reader** is not the §C denominator, however arithmetically
> faithful the conversion.

Grounded in: `XASSET-0025` §D criterion **T1** — "**Right quantity** — **states or source-prescribes** a
value for the §C quantity", whose disqualifier is "**Any other quantity, however expressed as a
percentage**"; `XASSET-0025` §F, which fails the RISK scenario magnitudes at T1 because "the denominator
is unspecified **by the source itself**"; and the canonical gate question and `PROTOCOL_V1.md` §3.3,
whose named wrong denominators are "sleeve-internal, within-fund, market-share, per-share, or
leverage-bearing."

**T1's own disjunction is load-bearing and is preserved here.** "States **or source-prescribes**"
admits both routes. The condition therefore turns on **who fixes the denominator**, not on where any
arithmetic physically runs — see §C.2.

**C.2 — No downstream-*authored* normalization is lawful. The boundary is authorship, not execution
locus.** `XASSET-0023` §H fixes that "There is no third route", and `XASSET-0024` §D's closed table
admits only **R1** (uniquely stated by the source) and **R2** (uniquely derived by a derivation *the
admitted source itself prescribes*), barring **N1–N8** by name. Both are preserved exactly.

`XASSET-0024` §D's R2 row states what invalidates the route: "**Any composed, selected, or invented
derivation** (that is authorship, §H.3 item 3); **any tunable coefficient, ordering, tolerance, cutoff,
or selection** (§H.3 item 7); ungoverned rounding; >1 lawful result." §J.6 puts it the same way: "For
R2, the derivation must be **source-prescribed**, not composed by the application." **Every one of
those invalidators is an act of authorship or choice. None of them is the physical act of computing.**
The two cases must therefore be kept apart:

> **A — BARRED: downstream-authored or downstream-selected normalization.** No transformation of
> `portfolio_function`, `valuation_opportunity_cost`, `downside_path_risk`, `recovery`,
> `diversification_cobehavior`, or `sleeve_deployability` content into a portfolio percentage may be
> **composed, selected, invented, tuned, or completed** at application or Stage-1 time — by any
> coefficient, ratio, integration, scaling, budgeting, allocation, or normalization step the
> application itself supplies. Any such step is a new portfolio model and fails `XASSET-0023` §H.3
> item 7's free-choice test, `XASSET-0020` §M's prohibitions, or both.
>
> **B — NOT CATEGORICALLY BARRED: mechanical execution of a source-prescribed R2 derivation.** Where
> the admitted source prescribes the **complete** derivation — its inputs, its operations, its
> ordering, and the §C quantity and denominator it yields — leaving the executor **zero free choice**,
> the application may **execute** that derivation. Execution is not authorship. That the arithmetic
> physically runs downstream does not convert a lawful R2 into a third route, and does not by itself
> make the result "normalized by a downstream reader."

**The operative test is `XASSET-0023` §H.3 item 7**, quoted by `XASSET-0024` §D as "the control": *if
any step could have been chosen differently without violating the source's own prescription, it is a
model parameter and the derivation fails.* A derivation that survives that test has had every choice
already made upstream; a derivation that does not is authorship no matter where it runs.

`XASSET-0027` §J.1 names every mapping "anyone would reach for" as barred — an optimizer or grid
search, a composite score, a symmetry or equal-division convention, a midpoint, a default range width,
or a residual plug. **Each is barred because the application would be choosing it**, which is exactly
limb A. None of them is a source-prescribed complete derivation, so §J.1's list is not evidence against
limb B.

**This does not establish that any R2 construction actually satisfies `G3`.** Whether an admitted
source could prescribe a complete, choice-free derivation whose output is the §C quantity is precisely
the reserved question (§A, §D). Limb B states that such a construction is not barred *by the execution
locus*; it is still subject to `G3`'s own reservation, and to `G2`, `G6`, `G7`, and every other gate.

**C.3 — `G3` is a property of what the evidence measures, not of who certifies it.** `XASSET-0025` §H
states that T1 and T2 are "**properties of what the evidence measures, not of who may certify it**" —
competent authority is T5, closed separately by `XASSET-0027` §F. **Competent Level-1 endpoint authority
therefore does not, and cannot, satisfy `G3`.** A future filing that attempted to close `G3` by
constituting an authority competent for Level-1 shares would be answering T5 and leaving T1 exactly
where it is. This is recorded because it is the most plausible way a successor could believe it had
closed `G3` without having done so.

### D. The six DRIVER classes, analyzed separately

Four capability levels are assessed per class. **Capability is not assumed uniform across the six**, and
where it is source-dependent rather than class-wide that is recorded instead of a class-wide answer
being invented.

| # | DRIVER class | 1. Subject matter | 2. Direction | 3. Intrinsic magnitude | 4. Intrinsic share-of-whole |
|---|---|---|---|---|---|
| 1 | `portfolio_function` | **YES** — `SELF` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §J.3 names this class specifically** |
| 2 | `valuation_opportunity_cost` | **YES** — `ALT` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §M.3; source-dependent** |
| 3 | `downside_path_risk` | **YES** — `ALT` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §M.3; source-dependent** |
| 4 | `recovery` | **YES** — `ALT` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §M.3; source-dependent** |
| 5 | `diversification_cobehavior` | **YES** — `PAIR` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §M.3; source-dependent** |
| 6 | `sleeve_deployability` | **YES** — `SELF` | **PERMITTED** (source/result-dependent) | **OPEN (§K.1)** | **RESERVED — §M.3; source-dependent, and additionally contested at `G5`** |

**Level 1 (subject matter) is class-wide YES** and is not this gate's question: `XASSET-0024` §D
determines the six are subject-matter classes, and `XASSET-0030` closed `G1` on that basis.

**Level 2 (direction) is class-wide PERMITTED — not class-wide realized.** `XASSET-0020` §E.1's
operative sentence is "Only these closed driver classes **may support** positive or negative economic
**allocation preference**." That is an **admission rule**: it closes *which* classes are eligible to
carry a direction, and bars every other class from doing so. **It does not determine that every class,
every source, or every admitted item actually carries one.** Whether a determinate direction exists is
a property of the particular source and the particular comparison — a result, not a class attribute.

§H's own four-value vocabulary confirms that reading rather than contradicting it, and the four values
are **not** four directions:

| §H value | What it is |
|---|---|
| `self_preferred` | a **direction** — positive preference toward `self` |
| `counterpart_preferred` | a **direction** — positive preference toward `counterpart` |
| `indistinguishable` | **not a direction** — a determinate **tie**; §H reaches it only when "every applicable driver is `indistinguishable`" |
| `unable_to_determine` | **not a direction** — preserved **uncertainty**; §H reaches it on "any contrary directions, required missingness, staleness, conflict, failed representation gate, or other unclosed state" |

**Two of the four are therefore non-directional outcomes**, and `unable_to_determine` is expressly the
uncertainty/disclosure result `XASSET-0020` §F.1 requires rather than a weak preference. What the
vocabulary *does* establish, and all this unit relies on, is that **none of the four carries a
magnitude** — every value is qualitative. That is the structural point: §H's machinery, when it
succeeds, yields at most a direction or a tie, never a quantity, and never a share of the whole.

**Level 3 (intrinsic magnitude) is `XASSET-0024` §K.1's open question, class-wide, and is routed
through `G2` and only `G2`** (`XASSET-0027` §M.1). This unit neither resolves nor relies on it.

**Level 4 (intrinsic share-of-whole) is `G3`, and is RESERVED for every class** — but not for identical
reasons, and the difference is recorded rather than flattened:

- **`portfolio_function` is textually distinguished.** It is the only class whose §E.1 scope language
  refers to the prospective **portfolio** — "the sleeve's directly evidenced job in the prospective
  portfolio." `XASSET-0027` §J.3 records exactly this, and then reserves the consequence in the same
  breath: "**Whether that suffices to carry a share-of-the-whole statement is what `G3` tests.**"
  Determining here that it suffices would decide the precise question §J.3 assigns to the study;
  determining that it does not would contradict §M.3. **The observation is carried forward unchanged as
  a fact and not as a prediction**, exactly as §J.3 framed it.
- **The other five carry no portfolio-framed scope language at all.** Their native subject matter is
  `SELF`, `PAIR`, or `ALT` — the sleeve's own position, the pair, or the alternative — not the whole.
  **That observation is about native scope only, and does not by itself decide `G3` for any of them.**
  A source in one of the five reaches the §C quantity only by satisfying §C.1 on its own terms — R1's
  direct statement, or a complete, zero-free-choice, source-prescribed R2 derivation that yields it —
  and any conversion the application would compose, select, invent, or tune remains barred by §C.2
  limb A. **Neither satisfaction nor impossibility is determined here for any class.**

**Why the reserved answer is source-dependent and not class-wide.** `G3` tests the denominator a source
*declares*, and `XASSET-0025` §H fixes that as a property of the evidence itself. Two sources in the
same class may declare different denominators; a class label does not fix one. Recording a class-wide
`G3` disposition would therefore assert something about sources that the class does not determine —
and, for all 680 constructions, about sources that do not exist (§B.2).

### E. R1 and R2, and the preservation of "no third route"

`XASSET-0023` §H's "There is no third route" is preserved exactly and is **not** narrowed, widened, or
reinterpreted by anything above.

| Route | Who fixes the §C denominator | Where the arithmetic may run | What this unit adds |
|---|---|---|---|
| **R1** — uniquely stated | The source's own governed content **states** one exact value **for the §C quantity**. | Nowhere — there is no arithmetic to run. | §C.1 states the condition the statement must satisfy; §C.3 records that competent authority does not substitute for it |
| **R2** — uniquely derived | The source itself **prescribes** the complete derivation, its inputs, its ordering, and the quantity it yields. | **Downstream execution is permitted**, provided the executor makes no choice: it executes, never composes, selects, tunes, or completes. | §C.2 limb B records that execution locus is not the authority boundary; §C.2 limb A records that a derivation composed, selected, or invented downstream is authorship and fails `XASSET-0023` §H.3 items 3 and 7 |

**Neither route is a "bridge" in `XASSET-0027` §J.1's sense**, and that is the substantive point: §J.1's
difficulty arises only where a *conversion is chosen*, and under both lawful routes every choice has
already been made upstream, inside the source — under R1 because the value is simply stated, under R2
because the prescription fixes every step and §H.3 item 7 disqualifies any step that could have been
chosen otherwise. **Nothing about R2 requires the arithmetic itself to have been performed upstream**,
and reading it that way would forbid constructions `XASSET-0024` §D expressly leaves conditionally
lawful.

**This does not establish that any qualifying source can exist, by either route** — that is `G3`, and
it is reserved (§A). In particular, no finding here is that any of the 136 registered `R2_C2`
constructions clears `G3`, or would clear it.

### F. `XASSET-0024` §K.1 — preserved, not resolved, and shown not to be dispositive of `G3`

**This filing adopts neither §K.1 reading**, asserts no `g2_outcome_under_*` value for any construction,
and creates no results document. It has no authority to resolve §K.1 and does not purport to.

`G3`'s disposition is stated under **both** readings, because a successor must know that resolving §K.1
does not discharge `G3`:

| §K.1 reading | Effect on `G2` | Effect on `G3` |
|---|---|---|
| **Subject-matter** (operative for `XASSET-0024` Outcome A) | Classes can house a magnitude; `G2` reading-dependent → `UNABLE_TO_DETERMINE` per §M.1 | **`G3` remains open.** Whether a housed magnitude is *whole-denominated* is a distinct property, reserved by §J.3 / §M.3 |
| **Preference-only** (contrary, preserved) | If established, "all cells abstain" (§M.1) | **`G3` is never reached as an independent question.** The program abstains at `G2` before denomination matters |

**Therefore §K.1 is not dispositive of `G3` in either direction**, and the two questions are genuinely
distinct: §K.1/`G2` asks whether a number can be *intrinsic* to §E.1 evidence; `G3` asks whether a
number is *denominated in the whole*. A source can satisfy one and fail the other — an expense ratio is
intrinsic to fund-cost evidence and denominated in fund assets; a bare governance figure may be
whole-denominated and wholly appended.

**A narrow but load-bearing reconciliation with `XASSET-0030` §G.A.** That section named `G3` as "the
`T1`/`T2` share-of-the-whole question" and cited §K.1's "narrowly scoped clarification of
`XASSET-0020` §E.1 alone" as "the shape of the smallest corrective." Read against `XASSET-0025` §D,
**T1 and T2 are separate criteria** — T1 is right quantity (`G3`), T2 is subject matter plus intrinsic
statement (`G1` + `G2`) — and §K.1's own text addresses only whether the classes "house a magnitude
statement," which is T2. `XASSET-0030` identified the correct **vehicle**; this filing records that the
vehicle must carry **two** properties rather than one (§G). Nothing in `XASSET-0030` is contradicted:
its §G.A named a shape, not a sufficient text, and its `G3` disposition is unchanged.

### G. `XASSET-0020` §E.1 — not amended, and what a future clarification would have to contain

**This filing amends, clarifies, narrows, widens, or supersedes nothing in `XASSET-0020` §E.1.** §B.3's
scope findings and §D's capability table restate `XASSET-0025` §J and `XASSET-0027` §J.1 / §J.3, each of
which is accepted and effective; no new scope rule is created. `XASSET-0020` is byte-unchanged.

Recorded for the successor, and authorizing nothing: a future §E.1 clarification intended to unblock
`G3` would have to close **both** of the following, and closing only the first leaves `G3` exactly where
it is:

1. **Magnitude housing (T2 / `G2`, §K.1's question)** — whether §E.1's six classes may house a
   quantitative statement at all, or are preference classes only.
2. **Denominator scope (T1 / `G3`, this unit's question)** — whether a class whose subject matter is
   scoped to a sleeve, a pair, or a comparison may carry a statement denominated in the **whole**,
   and if so under exactly what condition.

A successor must additionally confront a structural difficulty this unit surfaces rather than solves:
for `HYPOTHETICAL_SOURCE_ARCHITECTURE` constructions there is no source whose declared denominator can
be inspected (§B.2), so `G3` can be answered only by stipulation — barred as by-construction inference
— or by a judgment about possibility, which is what §M.3 reserves. **Whether that difficulty is
soluble by clarification alone, or requires a stage at which an actual candidate source exists, is not
determined here.** Recording the difficulty is this unit's remit; resolving it is not.

### H. `G1` and `G2` re-derivation — the trigger did not fire

`XASSET-0030` §E.1 makes `G1` and `G2` re-derivable when "§E.1's classes or scope are amended", when
"§D's subject-matter determination is amended or superseded", when "§M.1's routing changes", when "a
reading slot is added to `G1`", when "§K.1 is resolved or amended in either direction", when "§E.1 is
clarified in a way that settles magnitude capability", or when "the reading map or its
`required_g2_gate_result` coupling changes".

Each was checked against this filing's actual diff rather than assumed:

| Trigger | Fired? | Basis |
|---|---|---|
| §E.1's classes or scope amended | **No** | `XASSET-0020` byte-unchanged; §G states no amendment is made |
| §D's subject-matter determination amended or superseded | **No** | `XASSET-0024` byte-unchanged; §D relied on unchanged |
| §M.1's routing changed / reading slot added to `G1` | **No** | `XASSET-0027` byte-unchanged; §F asserts no reading for `G1` |
| §K.1 resolved or amended | **No** | §F adopts neither reading and resolves nothing |
| §E.1 clarified so as to settle magnitude capability | **No** | Level 3 recorded **OPEN** for all six classes (§D) |
| Reading map or `required_g2_gate_result` coupling changed | **No** | Canonical `pre_registration.yaml` byte-unchanged |
| Either pinned canonical hash changed | **No** | Both re-verified identical in preflight |
| `XASSET-0019`–`XASSET-0026` effective identity changed | **No** | None edited |

**No trigger fires, so `G1` and `G2` are not re-derived and their `XASSET-0030` §E dispositions carry
forward unchanged.** This is a deliberate design property of the filing, not an omission: the unit was
scoped to state the `G3` condition and its reservation *without* amending §E.1, precisely so that the
coupling `XASSET-0030` §E.1 warned about would not fire and a successor would not inherit two stale
results.

### I. Resulting gate map — unchanged

The `CURRENT_AUTHORITY_GATE_EVALUATION_SNAPSHOT` stands exactly as `XASSET-0030` §E left it:

| Closable under current authority (6) | Not closable (6) |
|---|---|
| `G1` → `PASS`, `G2` → `UNABLE_TO_DETERMINE`, `G4` → `PASS`, `G6` → `PASS`, `G7` → `PASS`, `G11` → `PASS` | **`G3`**, `G5`, `G8`, `G9`, `G10`, `G12` |

`G3` remains not closable, and remains independently sufficient for `XASSET-0030`'s
`GATE_EVALUATION_METHOD_NOT_CLOSABLE`. Every §E.1 invalidation trigger remains as recorded. `G5`, `G8`,
`G9`, `G10`, and `G12` are **untouched** — this unit examined none of them and determines nothing about
any of them.

### J. Successor model

`XASSET-0030` §G's two-class model — semantic prerequisites (§G.A) first, then one coherent
canonical / enforcement / outcome-producing-code / reauthorization pass (§G.B) — is adopted unchanged
and is **not** re-sequenced. This filing discharges no §G.A item: `G3` remains open, now with its
condition stated and its prerequisite named.

The remaining §G.A items — `G5`, `G8`, `G9`, `G10`, `G12` — are expected to be handled by a later
semantic unit and are deliberately not pulled into this filing. Nothing here schedules, packages, or
pre-decides them.

**No part of §G.A or §G.B is authorized by this decision, and none is performed.**

### K. Recorded rather than resolved

**K.1 — The hypothetical-source difficulty is disclosed, not converted into a finding about Stage 1's
viability.** §B.2 and §G record that no construction has an inspectable source. This bears on `G3` and
is stated for `G3`. **It is not determined here whether the same difficulty affects any other gate**,
and no claim is made that Stage 1 is unexecutable in principle — `XASSET-0028` §F puts Stage 1's
question at lawful satisfiability, and judging satisfiability is the designed task.

**K.2 — The `G5` overlap is named and not entered.** `sleeve_deployability` is flagged at §D as
additionally contested at `G5` because `XASSET-0027` §M.4 reserves constraint-shape per candidate.
**This filing takes no position on `G5` for that class or any other**, and §M.4 is untouched.

**K.3 — Not reopened here.** `XASSET-0030` §C's validator enforcement-conformance defect; §D's
load-bearing reauthorization dependency; `XASSET-0027` §K.2's deferred §J.12; `XASSET-0023` §G's
Level-2 subset question; `XASSET-0021` §O's strict-conjunction tension; `XASSET-0024` §K.2's
circularity discussion; `XASSET-0025` §O.5's unresolved ordering and packaging. None bears on any
determination above, and none is resolved.

### L. Governance package and WORKSTREAMS synchronization

This filing touches exactly five tracked files:

1. this decision;
2. `test_level1_stage1_g3_share_of_the_whole.py` — the focused adversarial module;
3. `governance/decisions.yaml` — one catalog row;
4. `operations/WORKSTREAMS.yaml` — additive `XASSET-0030` post-merge closeout and `XASSET-0031` lane
   facts, every prior gate's own text byte-unchanged; and
5. `test_portfolio_hq_dashboard_decisions.py` — the two mechanical catalog-count assertions.

**No canonical file, no validator, no authorization module, no runner, and no `CLAUDE.md` entry is
touched.** The `XASSET-0030` adversarial module is left byte-unchanged: its 6/6 partition and every
reservation it pins remain true at this head, so amending it would be a change without a finding.

### M. Reopen triggers

Reopen `XASSET-0031` if: `XASSET-0019` through `XASSET-0030`'s effective identity changes;
`XASSET-0020` §E.1's driver classes or scope language is amended; `XASSET-0024` §C's endpoint quantity
or §D's route table changes; `XASSET-0024` §K.1 is resolved or amended in either direction, including a
reviewer establishing the contrary reading; `XASSET-0025` §D's T1 or T2 criteria change;
`XASSET-0027` §J.1, §J.3, §M.1, or §M.3 is amended, or `G3`'s express reservation is lifted; either
pinned canonical hash changes; the construction universe's cardinality, identity, `source_architecture`,
or frozen `hypothetical_source_requirements` change; a candidate endpoint source with an inspectable
declared denominator is proposed; or `NUM-0001`'s classes or §§6–8 change.

### N. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner and no `stage1_results.yaml`;
consumes nothing of `ATTEMPT_1`; evaluates `G3` or any other gate for no construction and asserts no
per-construction outcome; closes, re-derives, or reclassifies no gate, and leaves the `XASSET-0030` 6/6
snapshot exactly as accepted; amends `XASSET-0020` §E.1 or any other accepted decision in no respect;
resolves `XASSET-0024` §K.1 neither way; determines nothing about `G5`, `G8`, `G9`, `G10`, or `G12`;
corrects no validator, changes no `LOAD_BEARING_RELPATHS`, and performs no load-bearing
reauthorization; amends no canonical file and changes no hash pin, universe, cardinality, or
construction identity; acquires no market, fundamental, economic, or Stage-2 data; resolves no §J.12,
grants no Stage 2, and grants no application authority; invents no Level-1 representation aggregation
or selection rule and designates no CM-14–CM-17 membership; selects no sleeve and creates no endpoint,
bound, point, range, percentage, weight, rank, target, or allocation; introduces no consequential
numeric parameter; reuses no RISK scenario, value, parameter, window, result, or private artifact, and
accesses no protected RISK results path; weakens no validator or test; changes no `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap, or margin
state; authorizes no chart, ladder, deployment, trade, order, or brokerage action; and rewrites no
accepted history.

## Rationale

The standard is `XASSET-0030`'s and is unchanged: not "a competent analyst could answer `G3`", but that
two independent conforming executors, given identical frozen inputs, must not be able to select
different lawful results. `G3` fails that standard, and it fails it for a reason worth stating
precisely rather than restating as "reserved."

**The reservation is real, and it is doubly express.** `XASSET-0027` §J.3 reserves the one class whose
scope language would most plausibly carry a share-of-the-whole — "Whether that suffices … is what `G3`
tests" — and §M.3 reserves the general case, assigning it to "a finding of the study rather than an
assumption of the charter." A governance unit that determined either way would be deciding the exact
question two accepted decisions assign elsewhere.

**Both available closures were tested and both fail.** Closing `G3` affirmatively would have to rest on
R5's own stipulation, since R5 is present in all 680 constructions and no source exists to inspect
instead — the by-construction inference `XASSET-0030` §E rejects and its Alternatives Considered
declined by name. Closing it negatively would have to determine that no bridge exists, which §M.3
forbids as a premise and which would additionally contradict `XASSET-0024` §D's standing determination
that R1 is lawful in principle for a source stating the §C quantity.

**What was worth doing instead is the part that is closable.** Three things were genuinely unstated
before this filing and are now fixed: the condition itself (§C.1), the bar on downstream-**authored**
normalization together with the authorship-versus-execution boundary that limits it (§C.2), and — the
finding least likely to be anticipated — that competent Level-1 endpoint authority does **not** satisfy
`G3` (§C.3). The third matters most.
`XASSET-0025` §G found T5 failing universally and `XASSET-0027` §F closed it; a successor that read
those together could reasonably believe constituting endpoint authority moves `G3`. It does not:
`XASSET-0025` §H fixes T1 as a property of what the evidence measures, not of who certifies it, and
`G3` is T1.

**The §K.1 separation is the second finding a successor would otherwise pay for.** `XASSET-0030` §G.A
cited §K.1's "narrowly scoped clarification of `XASSET-0020` §E.1 alone" as `G3`'s corrective shape.
Read against `XASSET-0025` §D, §K.1's own text addresses T2 — whether the classes house a magnitude —
while `G3` is T1, whether a magnitude is whole-denominated. The vehicle is right and the payload is
incomplete. A successor drafting the §E.1 clarification from §K.1's wording alone would close `G2`,
re-derive `G1` and `G2` under §E.1's invalidation trigger, and discover `G3` still open — having spent
the amendment.

**Declining to amend §E.1 was a design choice with a mechanical consequence.** `XASSET-0030` §E.1 warns
that the §E.1 clarification is `G1`'s and `G2`'s invalidation trigger. By stating the `G3` condition
from `XASSET-0025` §J and `XASSET-0027` §J.1 — both accepted, both effective, neither amended — this
unit leaves `G1` and `G2` standing on their original basis. §H verifies trigger-by-trigger that none
fires. A filing that had reached the same substantive conclusions by editing §E.1 would have cost two
re-derivations for no additional finding.

## Alternatives Considered

**Close `G3` affirmatively from R5 and competent authority.** Rejected on two independent grounds: R5
is a frozen specification requirement present in all 680 constructions, so inferring satisfiability
from it is `XASSET-0030` §E Standard 1's rejected inference; and `XASSET-0025` §H fixes T1 as a
property of the evidence, so authority competence (T5) cannot supply it.

**Close `G3` negatively — determine no bridge exists.** Rejected: `XASSET-0027` §M.3 states in terms
that §J.1 "does not determine that no bridge exists," and `XASSET-0024` §D's route table — accepted and
unedited — marks R1 lawful in principle for a source stating the §C quantity. A categorical negative
would contradict both.

**Determine that `portfolio_function` alone clears `G3`, on §J.3's textual observation.** Rejected, and
it was the most tempting option. §J.3 makes the observation and reserves its consequence in the same
sentence; converting a fact recorded "not as a prediction" into a class-wide gate disposition is
exactly the overreach §J.3's own wording guards against. The observation is carried forward at §D
unchanged.

**Amend `XASSET-0020` §E.1 in this filing to settle denominator scope.** Rejected. The amendment is a
methodology change requiring its own authorization, it would fire `G1`'s and `G2`'s invalidation
triggers for a question this unit cannot close anyway, and — per §G — a clarification that closed only
§K.1's magnitude question would leave `G3` open regardless. §G states what such an amendment must
contain and leaves its drafting to a unit scoped for it.

**Resolve `XASSET-0024` §K.1 as the route to `G3`.** Rejected on authority and on merit: this unit has
no authority to resolve §K.1, and §F shows resolution is not dispositive of `G3` in either direction.

**Batch `G5`, `G8`, `G9`, `G10`, and `G12` into this filing.** Rejected. `XASSET-0030` §G.A states the
semantic prerequisites "need not be one filing," `G3` is independently sufficient for the standing
negative and is the named critical path, and the remaining five turn on materially different
authorities — constraint shape, uniqueness over an empty set, representation, pair independence, and an
undefined governed term. Bundling would have produced one filing whose review surface spanned six
unrelated questions.

**Record `UNABLE_TO_DETERMINE`.** Rejected. Accepted authority determines the condition precisely
enough to state it (§C.1) and to bar every downstream-authored mapping (§C.2); abstaining on the whole
question would have discarded three closable sub-determinations to avoid one reserved one.

**State §C.2 as an absolute bar on all downstream normalization, including execution.** Rejected: that
was this filing's own first formulation and it was wrong. `XASSET-0024` §D's R2 row invalidates a
derivation that is "composed, selected, or invented," or that carries "any tunable coefficient,
ordering, tolerance, cutoff, or selection" — every invalidator is an act of authorship or choice, and
§J.6 fixes the requirement as "source-prescribed, not composed by the application." An absolute bar
keyed on execution locus would permanently forbid constructions accepted authority expressly leaves
conditionally lawful, while claiming to preserve "no third route" unchanged. The corrected §C.2 bars
the authorship and leaves the execution question where `XASSET-0024` left it. **It grants nothing:
`G3` is unchanged, and no R2 construction is found to clear it.**

**State direction as class-wide realized rather than class-wide permitted.** Rejected for the same
class of error, in the opposite direction. `XASSET-0020` §E.1 says the six classes "**may support**"
preference — an admission rule fixing eligibility, not a finding that every source carries a direction
— and §H's own condition table reaches `indistinguishable` only on a determinate tie and
`unable_to_determine` on missingness, conflict, or staleness. Calling all four values "directions"
would manufacture a class-wide semantic capability accepted authority does not establish, and could
contaminate later `G3`/`G5` reasoning. The corrected §D records direction as permitted and
source/result-dependent, and preserves the two non-directional outcomes by name.

**File nothing, on the ground that `XASSET-0030` already recorded `G3` as reserved.** Rejected. "Not
closable" without a stated condition leaves a successor unable to tell a qualifying source from a
disqualified one, or to know that the §E.1 clarification it is drafting is incomplete.

## Consequences

`G3` stays open and Stage 1 stays unarmed, but the successor's task is now bounded rather than
open-ended. It knows the exact condition a qualifying source must satisfy, that no
downstream-**authored** normalization will ever supply it — while mechanical execution of a complete,
choice-free source-prescribed R2 derivation is not barred by execution locus and remains subject to
`G3` like everything else — that constituting competent Level-1 endpoint authority will not close it,
that resolving §K.1 will not close it either, and that an §E.1 clarification aimed at `G3` must carry
two properties rather than the one §K.1 names.

It also inherits `G1` and `G2` on their original, unamended basis, because this unit deliberately
reached its conclusions without touching §E.1.

What remains genuinely unresolved is disclosed rather than smoothed: whether any construction can
satisfy the §C.1 condition is reserved by `XASSET-0027` §J.3 and §M.3, and for hypothetical-source
constructions there is no declared denominator to inspect. Whether that is soluble by clarification, or
requires a stage at which a real candidate source exists, is the next question — and it is not answered
here.

Nothing about the portfolio changes. The construction universe stands at 680 / 48 / `73c0965e…5224`,
both canonical hashes are unchanged, all six load-bearing paths are byte-identical, the authorization
lane is absent, `new_execution_is_authorized()` remains `False`, and `ATTEMPT_1` remains intact,
unclaimed, and unconsumed.
