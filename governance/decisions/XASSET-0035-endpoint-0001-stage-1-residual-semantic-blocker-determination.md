---
decision_id: XASSET-0035
date: 2026-08-17
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0009, OPS-0014, NUM-0001, XASSET-0019, XASSET-0020, XASSET-0021, XASSET-0022, XASSET-0023, XASSET-0024, XASSET-0025, XASSET-0026, XASSET-0027, XASSET-0028, XASSET-0029, XASSET-0030, XASSET-0031, XASSET-0032, XASSET-0033, XASSET-0034, LEVEL2-0001, RISK-0001]
supporting_artifact: test_level1_stage1_residual_semantic_blockers.py
---

## Context

### Live preflight

Verified against live repository and GitHub state before any mutation, not inherited from any prior
filing's summary:

| Check | Observed |
|---|---|
| GitHub `main` / `origin/main` / local `HEAD` | all `a39f8e1322ba321b70a89be781ee9463047b8882` |
| `PR #333` (`XASSET-0034`) | merged, closed; parents `cd126f0e…` + accepted head `97326cc6…` |
| Merge-commit CI | workflow run `32023425300`, `head_sha` `a39f8e13…`, `completed` / `success` |
| Open pull requests | **0** |
| Working tree / stash / worktrees | clean / empty / sole worktree |
| Local `main` branch | stale at `3cc15d58…`; **not** reset, rebased, or touched |
| `XASSET-0035` | unused (zero matches repository-wide) |
| Canonical `PROTOCOL_V1.md` | `6c34cbbc4ed28807354f9468b225771341c6cdd40190fad06722e0cfd0ae64cb` **MATCH** |
| Canonical `pre_registration.yaml` | `6e0c07a8e3279f8100a41df489921720f7f3125346f977e64fb5deca2f34337c` **MATCH** |
| Construction universe | regenerated live: **680** constructions / **48** cells / `73c0965e…5224` **MATCH** |
| `LOAD_BEARING_RELPATHS` | all **6** present, unchanged |
| `AUTHORIZATION_ROOT` | **absent** |
| `new_execution_is_authorized()` | `False` — "no attestation present … There is no merge-to-execution gap" |
| Runner / result writer / attestation / claim / completion / ledger / `stage1_results.yaml` | **absent** |

**Stage 1 is UNARMED and NOT EXECUTABLE. `ATTEMPT_1` is intact, unclaimed, unconsumed.**

### The question this unit answers

`XASSET-0034` determined `SEMANTIC_CLOSURE_PARTIAL_THREE_RESIDUAL_BLOCKERS` — five §G.A items are
execution-ready governed satisfaction residues that do **not** block `XASSET-0030` §G.B, and three
genuine residual **semantic** blockers do. Its §G tabled all three as decidable from committed text,
requiring no candidate source, snapshot successor, market data, or protected `RISK` access, and left
their packaging open.

This unit takes exactly those three:

> **B1** — the tense of `G12`'s "could admit". **B2** — `XASSET-0024` §H.4 consumption semantics for the
> 360 `DIRECT_ALTERNATIVE` constructions carrying a sleeve counterpart. **B3** — the shared *recording
> posture* for reserved-satisfiability gates evaluated against a frozen
> `HYPOTHETICAL_SOURCE_ARCHITECTURE` specification.
>
> For each: can the semantic degree of freedom be eliminated, such that two independent conforming
> executors handed byte-identical frozen inputs can no longer lawfully choose different semantics?

The bar is `XASSET-0030`'s and is unchanged: not "a competent analyst could answer this", but that two
conforming executors cannot lawfully diverge — because `ATTEMPT_1` is one-shot and
`execution.rerun_rule.after_outcomes_observed` is `PROHIBITED`.

## Decision

### A. Determination — `ALL_THREE_RESIDUAL_SEMANTIC_BLOCKERS_RESOLVED`

**All three are resolved. `XASSET-0030` §G.A's semantic prerequisites are complete.**

| Blocker | Route | Determination |
|---|---|---|
| **B1** `G12` modal | **CONSTITUTIVE** — a governed `G12`-scoped modal statement | "Could admit" is evaluated against **lawful satisfiability of the frozen construction specification**, not execution-time world state (§E) |
| **B2** `G10` §H.4 consumption | **INTERPRETIVE** — accepted authority selects | A construction consumes a canonical §H unordered pair **iff both of its own two frozen named comparison endpoints are sleeves**. Determined by frozen comparison identity, never by the `unordered_pair_id` label (§F) |
| **B3** reserved-gate recording posture | **INTERPRETIVE** — by elimination over the closed vocabulary | `UNABLE_TO_DETERMINE`, for exactly `G3`, `G5`, and `G9` path 1 **when undetermined** (§G) |

**§G.B is therefore unlocked — but only on this decision's own accepted lifecycle closure**, not on
this PR being opened or merged. Independent full exact-head review, any bounded correction and
exact-head re-review, explicit principal exact-head acceptance, merge, and post-merge verification are
each required first (§I).

**Nothing else moves.** The `XASSET-0030` 6/6 gate map is **unchanged** and no §E.1 invalidation trigger
fires (§H.1). `XASSET-0024` §K.1 stays unresolved; `XASSET-0020` §E.1 stays unamended; `XASSET-0031`'s
`G3` determination is neither reopened nor used as a premise. **No gate is closed on satisfaction**, and
the five execution-ready residues `XASSET-0034` §D identified remain exactly as it left them (§H.2).
**No gate is evaluated for any construction and no per-construction outcome is asserted.** Stage 1
remains UNARMED and NOT EXECUTABLE.

### B. What this unit reproduced before determining anything

All reproductions used the live committed bytes and the real modules. Where a derivation function was
exercised it was fed **isolated synthetic gate-result dictionaries**, never a real construction — the
same method `XASSET-0030` §B used. **No gate was evaluated for any of the 680**, and no results
document, lane state, or Stage-1 output was created.

**B.1 — The closed gate-result vocabulary is exactly four values.**
`result_vocabulary.gate_result_vocabulary` is `['PASS', 'FAIL', 'UNABLE_TO_DETERMINE',
'NOT_APPLICABLE']`. No fifth value exists and none may be added at results time.

**B.2 — Gate classes, read from canonical bytes.** `failure_disposition` is `BLOCKED_CATEGORICALLY` for
`G1`–`G8`, `G10`, `G11`, and `BLOCKED_PENDING_SEPARATE_PREREQUISITE` for exactly `G9` and `G12`. **The
canonical prerequisite set is exactly two gates.** `G3`, `G5`, and `G10` are categorical-class.

**B.3 — The two class definitions turn on closeability, not on face-unlawfulness.** Verbatim:

> `categorical_definition.means`: `NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY`
>
> `prerequisite_definition.means`: `CLOSEABLE_BY_A_NAMED_SEPARATELY_AUTHORIZED_PREREQUISITE_WITHOUT_METHODOLOGY_AMENDMENT`, with `requires_named_dependency: true`

This pair is load-bearing for §G and, so far as this unit can determine, has not previously been cited
for the recording-posture question.

**B.4 — Nine of the twelve canonical gate *questions* are counterfactual.** Read from
`gate_sequence.gates[*].question`: `G2`, `G3`, `G5`, `G6`, `G7`, `G8`, `G9`, `G10`, and `G11` each begin
"**Would** the candidate …". `G1` asks "**Can** evidence … **be** admissible"; `G4` asks "**Is** every
input free of barred origin"; `G12` asks "**Is** a lawful … successor identifiable that **could** admit
the candidate". **A gate-level counterfactual register is therefore canonically instantiated, not
inferred.** This is new to this filing and is §E's principal ground.

**B.5 — The canonical gate-level abstention conditions are likewise counterfactual.** Of the eight
`mandatory_abstention_conditions`, each keyed to a specific gate's controlling authority, four use a
counterfactual modal — `AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT` (§H.4 → `G10`),
`A_CANDIDATE_WOULD_REQUIRE_INVENTING_A_LEVEL_1_AGGREGATION_OR_REPRESENTATION_RULE` (§H.5 → `G9`),
`ANY_STEP_COULD_HAVE_BEEN_CHOSEN_DIFFERENTLY` (§H.3 item 7), and
`REPRESENTATION_PATH_1_FAILS_AND_NO_ACCEPTED_RULE_EXISTS`'s own note "a candidate whose construction
**would require** cross-representation combination". `abstention_is_a_complete_outcome` is `true`.

**B.6 — The comparison architecture, counted mechanically from the frozen universe.**

| Group | `comparison_subject_kind` | Count | Driver classes |
|---|---|---|---|
| `PAIR__<sleeve>` | `UNORDERED_PAIR` | **120** | `diversification_cobehavior` (120) |
| `ALT__<sleeve>` | `DIRECT_ALTERNATIVE` | **360** | `valuation_opportunity_cost` (120), `downside_path_risk` (120), `recovery` (120) |
| `ALT__UNSIZED_UNASSIGNED_CAPITAL` | `DIRECT_ALTERNATIVE` | **120** | same three (40 each) |
| `SELF` | `SLEEVE_SELF` | **80** | `portfolio_function` (40), `sleeve_deployability` (40) |

`120 + 360 + 120 + 80 = 680`, reproducing `XASSET-0032` §B.2 exactly.

**B.7 — All 360 map onto the six canonical pairs, uniformly, with no exceptions.** For every one of the
360, both named endpoints are members of the four-sleeve set, so `{self, counterpart}` is one of
`XASSET-0020` §H's six unordered pairs. Counted: **60 per pair**, all six pairs, **zero unmapped, zero
degenerate** (`self == counterpart` never occurs). The 120 `UNORDERED_PAIR` constructions distribute
**20 per pair**. Each canonical pair is therefore implicated by 20 + 60 = **80** constructions.

**B.8 — Every construction is hypothetical.** `source_architecture` is
`HYPOTHETICAL_SOURCE_ARCHITECTURE` for all 680, without exception — the shared root of B3.

**B.9 — Recording is mandatory for every applicable gate.**
`gate_sequence.evaluation_requirement` is `EVALUATE_EVERY_APPLICABLE_GATE_BEFORE_CLASSIFYING`;
`record_first_failing_gate_only` is `false`; `first_failing_gate_is_diagnostic_only` is `true`. A gate
result that is disposition-inert today must still be recorded.

**B.10 — Gate reinterpretation is barred only *after* an outcome is observed.** Canonical
`gates_may_not_be_added_removed_reordered_or_reinterpreted_after_any_outcome_observed` is `true`. **No
outcome has been observed**: Stage 1 is unarmed and `ATTEMPT_1` unclaimed. Fixing gate semantics **now**
is therefore expressly the lawful window, and doing it later would not be. This is affirmative authority
for §E's constitutive act, and it is the reason this work belongs before §G.B rather than inside it.

### C. Batchability — one coherent unit, with one disclosed scope guard

`XASSET-0032` §C's five-question test is the available method and this unit applies it.

1. **One shared methodology and authority surface?** **Yes.** All three are Stage-1 **gate-semantics**
   questions — the exact class `XASSET-0034` §C determined is required for §G.B entry. All three are
   decidable from committed text with no candidate source, no snapshot successor, no market data, and no
   protected `RISK` access (`XASSET-0034` §G says so of each). All three sit on one surface:
   `XASSET-0024` §§F/G/H.4/J, `XASSET-0020` §§E.1/H/I, `XASSET-0030` §E's two Standards, `XASSET-0028`
   §F, and the two canonical artifacts. `OPS-0009` Lane G throughout.
2. **Would batching create accidental cross-gate policy?** **Only if B3 were stated broadly — and it is
   not.** This is the one real risk in this filing and it is handled explicitly. Stated as "any
   reserved or source-dependent gate records `UNABLE_TO_DETERMINE`", B3 would swallow `G10` (defeating
   B2's categorical consequence) and `G12` (defeating B1). **B3 is therefore scoped to exactly `G3`,
   `G5`, and `G9` path 1**, on the express-reservation ground those three share and `G8`/`G10`/`G12` do
   not (§G.4). Each of B1, B2, B3 addresses a disjoint gate set — `{G12}`, `{G10}`, `{G3, G5, G9}` — and
   **no determination below is used as a premise for any other**; §H.4 records the interactions as
   observations.
3. **Would any require amending a different controlling decision?** **No.** None requires the
   `XASSET-0020` §E.1 clarification, and so none fires `G1`'s or `G2`'s invalidation trigger (§H.1).
   B1 is constituted forward as a new `G12`-scoped statement rather than by editing `XASSET-0033`; B2
   and B3 are readings of accepted text.
4. **Would any require protected evidence or a real future candidate?** **No.** B2 is decidable from the
   frozen universe and committed text; `XASSET-0032` §G.2 already dissolved the `risk_lane_boundary`
   concern for pair status, and **`risk_lane_boundary.protected_result_path` was not read, listed,
   opened, or referenced by this filing**. B1 and B3 are pure readings. The *satisfaction* residues do
   require a candidate — which is exactly why they are not touched.
5. **Independently reviewable without hiding separate judgments?** **Yes, and the disclosure is
   sharpened rather than blurred.** §§E–G are separate sections, each with its own authority,
   reproduction, determination, rejected alternatives, and triggers, and each separately pinned by
   tests. **B1's constitutive character is stated in its own heading and again at §E.1**, so a reviewer
   is never left to infer that a governed choice was presented as a reading.

**Choice: ALL-THREE COHERENT UNIT.** Three separate lifecycles would change no conclusion and would
fragment one §G.B entry condition across three reviews — and resolving two of three leaves §G.B locked
regardless, so partial filing purchases nothing.

### D. The two routes, distinguished before either is used

This filing does two different kinds of work and says which is which, because conflating them is how a
governance unit legislates while appearing to read.

> **INTERPRETIVE closure** — accepted authority already selects; the unit assembles it and the competing
> reading is shown **unlawful**. This is `XASSET-0031` §C's method: "a restatement of accepted authority
> assembled in one place. None adds a rule." **B2 and B3 are interpretive.**
>
> **CONSTITUTIVE closure** — accepted authority does *not* select, and competent Lane-G governance
> **states the rule**, prospectively. The competing reading does not *become* unlawful until the
> statement is accepted. **B1 is constitutive**, and is authorized as such by `XASSET-0030` §G.A, which
> lists as the prerequisite "**`G12`'s 'identifiable'** — **a governed definition**, including the tense
> of 'could admit the candidate' for a source that does not yet exist."

`XASSET-0034` §C's guard is preserved exactly: an executor may **apply an already-fixed rule to an
already-frozen object**; an executor may never **choose what the rule is**. Everything below fixes
rules before execution, which is precisely what B.10 makes the lawful window.

### E. B1 — `G12`'s modal register, constituted

#### E.1 — Route and authority for the act

**This is a constitutive governed statement, not a reading.** `XASSET-0033` returned
`G12_COULD_ADMIT_TENSE_NOT_CLOSABLE` and that negative **stands as correct on its own bar**: it required
the competing reading to be shown *unlawful*, and its §F.3 obstacles 2 and 3 survive this filing
untouched. `XASSET-0033` did not leave the question open for a better reader — its §I named the
corrective:

> "**Smallest sufficient corrective — a `G12`-scoped modal statement.** One governed sentence fixing
> whether `G12`'s 'could admit' is evaluated against execution-time world state or against lawful
> satisfiability of the frozen construction specification. It requires **no new evidence**, no
> methodology amendment, no change to `G12`'s wording, and no snapshot successor. It touches one gate."

Competence to make it is established by three independent texts: `XASSET-0030` §G.A's "**a governed
definition**"; `XASSET-0034` §G's B1 row, "Requires new evidence? **No**"; and canonical B.10, which
bars gate reinterpretation only *after* an outcome is observed.

**It must be constituted rather than deferred, because a tense can never be settled by evidence.**
`XASSET-0034` §E.1 records this in terms: "No property of any source, snapshot, or specification could
settle a tense." Abstaining is therefore not caution — it is permanent termination of the program on an
undefined modal, which `XASSET-0034`'s own Alternatives rejected as ending the program "on a
construction rather than on evidence."

#### E.2 — The statement

> **`G12`'s embedded modal "could admit" is evaluated against the lawful satisfiability of the frozen
> construction specification, not against execution-time world state.** A lawful `XASSET-0021` snapshot
> successor "could admit the candidate" if, under accepted authority and the ordering that authority
> fixes, that successor would be capable of admitting a source conforming to the construction's own
> frozen specification. **The present nonexistence of a conforming source is not, by itself, a ground
> for concluding that no such successor could admit it.**

#### E.3 — Why this register and not the other

The direction is chosen on coherence with the canonical register, **not** because it blocks fewer
constructions. That consideration is expressly excluded, and §E.5 records what the direction does *not*
purchase.

1. **The canonical gate-question register is counterfactual, at gate level (B.4).** Nine of twelve gate
   questions ask "**Would** the candidate …" — a register only coherent about a source that does not yet
   exist. `G3`'s "Would the candidate **state** the §C quantity", `G5`'s "Would the candidate
   **originate** a bound", `G8`'s "Would **exactly one lawful value exist**", `G10`'s "Would the
   candidate **avoid consuming** any unresolved pair" are each unanswerable in a world-state register,
   because no candidate exists to inspect. **This closes `XASSET-0033` §F.3 obstacle 1 as stated** —
   that the register statements "describe Stage 1, not a gate-level modal rule." The register is in the
   gate questions themselves.
2. **The canonical gate-level abstention conditions are counterfactual too (B.5)** — including §H.4's
   own `AN_UNRESOLVED_PAIR_WOULD_BE_CONSUMED_AS_AN_INPUT` and the `representation` block's "would
   require".
3. **`XASSET-0028` §F binds one evaluand for all twelve gates**, verbatim: "Stage 1 evaluates whether a
   **frozen specification** is lawfully satisfiable **under the twelve gates** — it does not search the
   world. Two executors handed the same `construction_id` receive the same requirement set byte for
   byte, so a negative means *the registered specification was evaluated and blocked*, never 'no source
   this executor happened to find.'" A world-state register for `G12` alone would give one gate of
   twelve a different evaluand than the other eleven.
4. **The named dependency is already identified.** `XASSET-0032` §H.3 closed this on `XASSET-0024` §J.2,
   `XASSET-0026` §G.2 constraint 3, `XASSET-0027` §P.2, and `PROTOCOL_V1.md`'s dependency order. §H.1
   binds that successor nonexistence may never by itself be `G12` `FAIL`.
5. **Coherence.** Under a world-state register, `G12`'s result is readable directly off the frozen
   `source_architecture` identity field for all 680 — the gate becomes a restatement of the generator.
   `XASSET-0030` rejects that inference in the `PASS` direction (Standard 1, and its "Close the method
   by adopting by-construction inference" alternative) and Standard 2 bars it in the `FAIL` direction.

#### E.4 — Why the competing reading *becomes* unlawful

Before this statement, the world-state reading was lawful — `XASSET-0033` §G says so, and this filing
does not pretend otherwise. **After it, that reading contradicts an accepted governed `G12`-scoped
rule**, and an executor adopting it would be reinterpreting a gate against accepted authority. That is
the constitutive mechanism, and it is prospective by construction. **`XASSET-0033`'s text is not
edited**, and its verdict is not recorded as having been wrong.

#### E.5 — Scope, and what is preserved

- **`G12` only.** This is expressly **not** a program-wide gate-modal register rule. `XASSET-0033` §I
  records that a program-wide statement "would bear on **every** gate, including the six the
  `XASSET-0030` snapshot records as closable, and would therefore be an invalidation trigger for that
  partition", and flags it as a **caution**. That caution is honoured: §H.1 verifies no trigger fires.
- **Identifiability only.** `XASSET-0032` §H.2 is preserved in full — `G12` may not absorb §J.1's
  hash-match, validator-pass, or governed-freshness conditions. `stage_1_testable_subset` keeps
  `J_2_SNAPSHOT_POSITION` at `G12_IDENTIFIABILITY_ONLY_NO_SUCCESSOR_CREATED`.
- **The clause stays operative.** `XASSET-0033` §C's dissolution bar is preserved: "that could admit the
  candidate" may not be dropped as a conjunct on the strength of `PROTOCOL_V1.md` §6/§6.1's shorter
  restatements.
- **§H.1's floor stays.** Successor nonexistence is still never by itself a `FAIL` ground.
- **No gate result is asserted.** This statement fixes the register; it records no `PASS`, `FAIL`, or
  `UNABLE_TO_DETERMINE` for `G12` for any construction. Applying the fixed register to the frozen object
  is the executor's act under `XASSET-0034` §C guard 1.
- **No snapshot successor** is created, extended, replaced, identified as existing, or authorized.
- **Disposition-inert today, and that is not a licence.** Verified by synthetic composition through the
  real `derive_candidate_disposition`: with `G2` at `UNABLE_TO_DETERMINE` for all 680, either `G12`
  result yields the same candidate disposition. `XASSET-0032` §H.5 and B.9 both bind — the gate result
  must still be recorded, and becomes outcome-determining the moment §K.1 resolves.

### F. B2 — `G10` §H.4 consumption semantics, determined

#### F.1 — The rule

> **A construction consumes a canonical `XASSET-0020` §H unordered pair if and only if both of its own
> two frozen named comparison endpoints are members of the four-sleeve set** — that is, its
> `comparison_subject_kind` is `UNORDERED_PAIR`, or it is `DIRECT_ALTERNATIVE` whose `counterpart` is
> another sleeve. The pair consumed is the single unordered pair those two endpoints form.
> **Consumption is determined by the construction's own frozen comparison identity, and never by the
> presence or absence of the `unordered_pair_id` label.**

#### F.2 — The four terms, given their exact accepted meanings

- **Pair.** `XASSET-0020` §H: "Exactly six unordered pair records exist, in this canonical order" over
  the four sleeves. Six is `C(4,2)` — the set is **exhaustive** over sleeve-to-sleeve comparison.
- **`UNORDERED_PAIR`.** §H fixes that "The first named sleeve is `self`; the second is `counterpart`.
  Reversed or duplicate records are invalid. **A sleeve-centric view mechanically inverts direction when
  the sleeve is the counterpart; it does not create a seventh record.**"
- **`DIRECT_ALTERNATIVE`.** A sleeve compared against a named counterpart. Where that counterpart is a
  sleeve, §H's sentence above governs: the comparison is that pair viewed directionally — **the same
  object, not a distinct one**.
- **Consumption / use / reference.** `XASSET-0024` §H.4, verbatim: "an endpoint qualifies only if the
  unresolved pair **is not an input to it at all**. An endpoint whose value **would move under some
  direction of that pair** is pair-dependent by construction and fails; showing that it happens to
  survive each enumerated direction is not the same as showing it never consumed the pair.
  **Direction-invariance by independence is the test; direction-robustness by inspection is not.**" The
  test is **counterfactual dependence on the pair's direction** — a matter of substance.
- **Unresolved-pair protection.** `XASSET-0020` §I: an endpoint survives a missing pair only where "both
  endpoints are **independently and directly governed** and remain valid under every possible direction
  of the unresolved pair. That is a **non-inferential intersection** of already-authorized bounds, **not
  a derived relationship**." §I also bars filling a missing pair "by transitivity through equity or
  another sleeve."

#### F.3 — Why accepted authority selects, rather than merely favouring

Four grounds, of which the second and third were not before the question when `XASSET-0032` §G.4
recorded that "nothing selects":

1. **The canonical test is counterfactual and substance-based.** `G10`'s own question asks "**Would** the
   candidate **avoid consuming** any unresolved pair as an input at all", and the matching canonical
   abstention condition is `AN_UNRESOLVED_PAIR_**WOULD_BE**_CONSUMED_AS_AN_INPUT` (B.5). A label check
   is not that test.
2. **`XASSET-0020` §H's no-seventh-record rule.** A sleeve-versus-sleeve comparison *is* the unordered
   pair, viewed directionally. Treating the 360 as consuming no pair requires them to be comparisons of
   something other than a pair — which §H forecloses in terms.
3. **§H requires each pair record to carry a direction for every driver class.** "all six driver
   categories considered, each with `applicable`, `not_applicable`, or missing state" and "direction per
   applicable driver". The 360 carry exactly `valuation_opportunity_cost`, `downside_path_risk`, and
   `recovery` (B.6) — three of those six categories. Each of the 360 therefore occupies a specific
   driver row of a specific canonical pair record. Its endpoint and that row's direction are functions
   of the same comparative fact, so the endpoint's value **would move under some direction of that
   pair** — §H.4's test, met.
4. **§I's independence requirement.** An endpoint whose subject matter *is* the comparative relationship
   between two sleeves is a **derived relationship**, and is not "independently and directly governed"
   of that pair.

#### F.4 — Why the competing reading is unlawful, not merely less attractive

Reading B's only remaining ground, once §H.4's substance test is applied, is that the 360 do not carry
`unordered_pair_id` — inferring **non-consumption from specification silence**. `XASSET-0032` §G.5
already rejected exactly that inference, for the 200-construction group, on exactly this authority:

> "A specification's silence about pair consumption is not proof that an eventual source consumes no
> pair — `XASSET-0030` §E Standard 1 again. The table records a specification fact, nothing more."

An accepted decision cannot bar that inference for 200 constructions and permit it for 360. Reading B
is therefore foreclosed by authority already in force.

#### F.5 — Mechanical effect, proved without evaluating any economic outcome

| Group | Count | Consumes a canonical §H pair? | Which |
|---|---|---|---|
| `UNORDERED_PAIR` | **120** | **Yes** — already established by `XASSET-0032` §G.3 | its own `unordered_pair_id`; 20 per pair |
| `DIRECT_ALTERNATIVE`, sleeve counterpart | **360** | **Yes** — by F.1 | the pair its two endpoints form; **60 per pair**, all six, zero unmapped, zero degenerate |
| `DIRECT_ALTERNATIVE`, `ALT__UNSIZED_UNASSIGNED_CAPITAL` | **120** | **No** | `UNSIZED_UNASSIGNED_CAPITAL` is a separate §H comparison family with its own closed conclusions (`sleeve_preferred`, `unassigned_preserved`, `indistinguishable`, `unable_to_determine`), not one of the six |
| `SLEEVE_SELF` | **80** | **No** | no comparison endpoint at all |

Consuming population **480**; non-consuming **200**. No sleeve, bound, driver class, family, or economic
property was consulted, and **no construction's `G10` result is recorded**.

#### F.6 — The four abuses this rule is built to prevent

- **No hidden pair inference.** Consumption is read from the construction's own two frozen named
  endpoints. No inference from driver class, family, route, bound, or what a future source might turn
  out to consult.
- **No transitive consumption.** Only the single pair the construction's own two endpoints form. Never a
  pair reachable through a chain — `XASSET-0020` §I bars transitivity expressly.
- **No relabelling.** `comparison_subject_kind` and `unordered_pair_id` are **not changed for any
  construction**. The 360 remain `DIRECT_ALTERNATIVE` with `unordered_pair_id` absent. **Consumption is
  not identity**, and this rule creates no `UNORDERED_PAIR` construction, no seventh pair, and no change
  to the frozen universe or its hash.
- **No ignoring genuine consumption.** The 360 are held to consume, on F.3's grounds.

#### F.7 — What this does *not* determine

**It does not determine `G10`'s result for any construction.** `G10` turns on whether the consumed pair
is **unresolved at evaluation time**, which is `XASSET-0032` §G.4 blocker 1 and `XASSET-0034` §D.5's
execution-ready successor-snapshot **satisfaction** residue — untouched, not closed, and expressly not a
§G.B entry condition. `XASSET-0021` §D's all-six-unresolved determination remains scoped "**under this
snapshot**" and does not travel. The 200 are **not** recorded `G10` `PASS`: `XASSET-0032` §G.5 stands.

#### F.8 — Consequence a successor must carry, recorded not corrected

Verified by synthetic composition through the real `derive_candidate_disposition`: a `G10` `FAIL`
alongside `G2` at `UNABLE_TO_DETERMINE` derives `BLOCKED_CATEGORICALLY`, because categorical dominates
uncertainty. **So if the consumed pair is unresolved at evaluation time, up to 480 constructions dispose
categorically** — and every one of them meets the validator branch `XASSET-0030` §C recorded as an
enforcement conformance defect, which rejects a `BLOCKED_CATEGORICALLY` disposition while `G2` is
reading-dependent.

**That defect is therefore no longer hypothetical**; B2's resolution makes it load-bearing for up to 480
of 680. **This unit does not correct it** — it is a load-bearing implementation path (`XASSET-0030` §D)
and belongs to §G.B step 3. It is recorded here so the successor scopes it up front. `XASSET-0030` §C's
defect is neither re-derived, expanded, narrowed, nor corrected.

### G. B3 — the reserved-gate recording posture, determined by elimination

#### G.1 — The rule

> **Where a gate's *satisfaction* is expressly reserved by accepted authority, and the frozen
> construction is `HYPOTHETICAL_SOURCE_ARCHITECTURE` so the reserved question cannot be answered from
> the specification, the executor records `UNABLE_TO_DETERMINE` for that gate.**
>
> This applies to exactly three items: **`G3`**, **`G5`**, and **`G9` path 1 when self-containment is
> undetermined**. It applies to no other gate (§G.4).

The outcome is shared; the **route** differs per gate and is stated per gate, because `G3`/`G5` and `G9`
sit in different classes and a single shared derivation would paper over that.

#### G.2 — Per-gate derivation

Standard 2 requires absence to be "classified as **categorical, prerequisite, or uncertainty** on
governed grounds — never inferred from nonexistence alone." That trichotomy is the elimination frame.

**`G3` (categorical class).**

| Value | Status |
|---|---|
| `PASS` | **Barred** — Standard 1: "a specification requiring property P is never by itself proof that P is lawfully satisfiable." `XASSET-0031` §B.5 applies it to `G3` by name. |
| `NOT_APPLICABLE` | **Unavailable** — `G3` is applicable to all 680; no canonical rule makes it inapplicable. |
| `FAIL` | **Barred.** It maps to `BLOCKED_CATEGORICALLY`, whose canonical meaning (B.3) is `NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY`. Recording it **asserts** non-closeability — which `XASSET-0027` §M.3 expressly declines: "§J.1 identifies the difficulty; **it does not determine that no bridge exists**." |
| *prerequisite limb* | **Structurally unavailable** — `G3`'s `failure_disposition` is `BLOCKED_CATEGORICALLY` and the canonical prerequisite set is exactly `{G9, G12}` (B.2). |
| **`UNABLE_TO_DETERMINE`** | **The only remainder** — and it names the actual state: accepted authority has reserved the answer and the executor cannot determine it. |

**`G5` (categorical class).** Identical route, with `XASSET-0027` §M.4 supplying the reservation:
constraint-shape "is exactly what `G5` decides, per candidate, on the candidate's own terms. **No
prejudgment is recorded here.**" A `FAIL` would be the prejudgment §M.4 withholds.

**`G9` path 1, undetermined (prerequisite class).**

| Value | Status |
|---|---|
| `PASS` | **Barred** — `XASSET-0032` §F.3: "Deriving `PASS` from `R8`'s presence would be the by-construction inference `XASSET-0030` §E Standard 1 rejects." |
| `NOT_APPLICABLE` | **Unavailable** — `G9` applies to all 680. |
| `FAIL` | **Barred here.** It maps to `BLOCKED_PENDING_SEPARATE_PREREQUISITE`, which requires `requires_named_dependency: true` (B.3). Naming the dependency asserts a **determined** path-1 failure — precisely what is undetermined — so it is a failure inferred from source nonexistence, which Standard 2 bars. |
| **`UNABLE_TO_DETERMINE`** | **The only remainder.** |

#### G.3 — What is expressly preserved, not overridden

- **`G9`'s determined path-1 failure remains prerequisite-blocked.** Where a candidate's construction
  *would* require cross-representation combination, canonical `non_self_contained_handling` —
  `NAME_THE_EXACT_DEPENDENCY_AND_BLOCK_PENDING_SEPARATE_PREREQUISITE` — and `XASSET-0032` §F.2's
  reconciliation govern unchanged: it records the exact dependency and **fails `G9` as a prerequisite**,
  with the endpoint-level outcome being abstention. **B3 applies only to the undetermined case** and
  does not convert that determined case into `UNABLE_TO_DETERMINE`.
- **No gate changes class.** No categorical gate becomes a prerequisite gate; no prerequisite gate
  becomes categorical. No gate's class, index, question, controlling authority, or `failure_disposition`
  is changed by this filing.
- **Abstention remains a complete outcome.** `abstention_is_a_complete_outcome: true` and all eight
  `mandatory_abstention_conditions` are untouched. `UNABLE_TO_DETERMINE` maps to a candidate disposition
  of the same name under canonical precedence.
- **Neither Standard is weakened.** Standard 1 still bars a by-construction `PASS`; Standard 2 still
  bars a nonexistence-`FAIL`. This rule is the value that survives both, not an exception to either.
- **Not a negative portfolio judgment.** `UNABLE_TO_DETERMINE` is neither `FAIL` nor
  `BLOCKED_CATEGORICALLY`. It records that a reserved question was not answerable at Stage 1 — not that
  a candidate failed a requirement, and not any statement about any sleeve, target, weight, or holding.
- **Not a pass by specification-satisfaction.** A hypothetical construction does not clear these gates
  by conforming to its own frozen specification.

#### G.4 — Scope limit: the three gates this rule does *not* reach

Stated as an operative limit, because a broader B3 would silently decide B1 and B2.

- **`G8`** — its residue is a **future snapshot successor's composition** (`XASSET-0034` §D.4), not an
  express reservation of the §M.3/§M.4 kind. Not reached.
- **`G10`** — its residue is pair status under a successor snapshot (`XASSET-0034` §D.5), and its
  consumption semantics are governed by §F. **B3 does not give `G10` an `UNABLE_TO_DETERMINE` posture**
  and does not soften §F.8's categorical consequence.
- **`G12`** — governed by §E's register, §H.1's floor, and §H.2's scope. Not reached.
- **`G2` is untouched.** `g2_reading_mapping` is **not** generalized, extended, or applied to any other
  gate; `open_reading_handling` keeps `resolved_by_this_program: false` and
  `relied_upon_by_this_program: false`. `XASSET-0032`'s refusal to add reading slots stands.

#### G.5 — Disposition effect, stated honestly

Verified by synthetic composition through the real `derive_candidate_disposition`: with `G2` already
`UNABLE_TO_DETERMINE` for all 680, recording `G3`/`G5`/`G9` as `UNABLE_TO_DETERMINE` yields a candidate
disposition of `UNABLE_TO_DETERMINE` — **the same value `G2` alone already yields. B3 is
disposition-inert today.**

**That is not a licence, for the reason `XASSET-0032` §H.5 gives.** Every applicable gate must still be
evaluated and recorded (B.9), and a disposition-inert gate result becomes outcome-determining the moment
§K.1 is resolved. B3 is required for §G.B not because it changes today's dispositions but because §G.B
step 2 must transcribe a determinate rule and steps 3–4 must encode and compute it.

### H. Interactions, preservation, and triggers

#### H.1 — No `XASSET-0030` §E.1 invalidation trigger fires; the 6/6 map is unchanged

Checked per gate against §E.1's own trigger rows:

| Gate | Its triggers | Fired? |
|---|---|---|
| `G1` | `XASSET-0020` §E.1 classes/scope amended; `XASSET-0024` §D subject-matter determination amended; §M.1 routing changed; a reading slot added to `G1` | **No** — none touched |
| `G2` | §K.1 resolved or amended; §E.1 clarified so as to settle magnitude capability; the reading map or its `required_g2_gate_result` coupling changed | **No** — §K.1 expressly unresolved, reading map untouched |
| `G4`, `G6`, `G7`, `G11` | route table / §F origin limbs / §H.2–§H.3 / `NUM-0001` classes / §C units regime / §J.11 / `XASSET-0021` §G | **No** — none touched |

`XASSET-0032` §M's rows are likewise unfired: `XASSET-0020` §H and §I are **read, not amended**;
`PROTOCOL_V1.md` §6.1/§8.1, the canonical `J.2` mapping, `XASSET-0026` §G.2 constraint 3 and
`XASSET-0027` §P.2 are untouched. Both canonical hash pins are unchanged, so no general trigger fires.

#### H.2 — The five execution-ready residues stay exactly as `XASSET-0034` §D left them

**None is closed, narrowed, or converted by this filing.** `G3` and `G5` satisfaction remain reserved to
per-candidate study findings (`XASSET-0027` §M.3, §M.4); `G9` path 1's self-containment remains
irreducibly source-dependent under frozen `R8`; `G8`'s uniqueness remains successor-snapshot-dependent;
`G10` blocker 1 remains successor-snapshot-dependent. §G gives the three reserved gates a **recording
posture** for the undetermined case; it does not answer what any source exhibits. §F gives `G10` a
**consumption rule**; it does not answer whether any pair is unresolved at evaluation time.

#### H.3 — Corrections to prior basis statements, classifications unchanged

Recorded in this unit's own text. **No prior decision's text is edited**, per the repository's
never-silently-rewrite convention — the pattern `XASSET-0032` §J and `XASSET-0033` §H each followed.

| # | Prior statement | Correction | Effect on its classification |
|---|---|---|---|
| H.3.1 | `XASSET-0033` §F.3 obstacle 1: the canonical register statements "describe Stage 1, not a gate-level modal rule" | A gate-level counterfactual register **is** canonically instantiated — nine of twelve gate questions and four gate-level abstention conditions (B.4, B.5) | `G12` **NOT CLOSABLE** stands as correct on `XASSET-0033`'s own bar; obstacles 2 and 3 survive. This filing **constitutes** rather than claiming the reading was available |
| H.3.2 | `XASSET-0032` §G.4 blocker 2: "Both readings are defensible and **nothing selects**" | `XASSET-0020` §H's no-seventh-record rule and six-driver requirement, §I's independence clause, and the canonical counterfactual §H.4 condition select; §G.5's own Standard-1 reasoning forecloses the label reading (§F.3, §F.4) | `G10` unchanged — still **NOT CLOSABLE** on blocker 1, successor-snapshot status |
| H.3.3 | `XASSET-0034` §E.3: "**no accepted authority states which of the four closed values** the executor records" | Canonical `categorical_definition.means`, the two-member canonical prerequisite set, and Standard 1 leave exactly one lawful value by elimination (§G.2) | B3 resolved; no gate's classification changes |

#### H.4 — Cross-blocker interactions, as observations only

**No determination above is used as a premise for any other.** §E does not rely on §F or §G; §F does not
rely on §E or §G; §G is scoped so as not to reach §E's or §F's gates (§G.4). Two proximities worth
recording: §E and §G both concern how a hypothetical specification is evaluated, but §E fixes a *modal
register* for one gate while §G fixes a *recorded value* for three others; and §F and §G both bear on
categorical gates, but §F's consequence is a categorical `FAIL` and §G's is expressly not.

#### H.5 — Invalidation and re-derivation triggers

| Determination | Re-derive if |
|---|---|
| §E `G12` modal register | `PROTOCOL_V1.md` §6/§6.1/§8.1 changes; the canonical `J.2` mapping changes; `XASSET-0032` §H.1/§H.2/§H.3 is reopened; `XASSET-0028` §F is amended; a program-wide gate-modal register rule is later accepted |
| §F consumption rule | `XASSET-0024` §H.4 is amended; `XASSET-0020` §H's six-pair contract, its no-seventh-record sentence, or §I's independence clause changes; the universe's `comparison_subject_kind` decomposition or `unordered_pair_id` population changes; `mandatory_abstention_conditions` changes |
| §G recording posture | `XASSET-0030` §E Standard 1 or 2 changes; `XASSET-0028` §F changes; `result_vocabulary.gate_result_vocabulary`, `categorical_definition`, or `prerequisite_definition` changes; `XASSET-0027` §M.3 or §M.4's reservations are lifted; `XASSET-0026` §H's disposition changes; any gate's `failure_disposition` changes |
| §A §G.B entry | Any of the three is reopened, or any `XASSET-0034` §D item is reclassified |

**A general trigger applies to every row**, matching `XASSET-0030` §E.1, `XASSET-0032` §M, and
`XASSET-0034` §H: if either pinned canonical hash changes, or `XASSET-0019` through `XASSET-0026`'s
effective identity changes, the whole set is re-derived rather than inherited.

### I. Effect on `XASSET-0030` §G.B — unlocked on lifecycle closure, not on merge

**§G.B step 1 is now satisfied.** Its six §G.A items divide as `XASSET-0034` §A determined: five are
execution-ready satisfaction residues that were never entry conditions, and the three semantic blockers
are resolved by §§E–G.

**§G.B is not unlocked by this PR being opened, nor by its merge alone.** It becomes lawful to begin only
after this decision has completed independent full exact-head review under `OPS-0007` §1, any bounded
correction and exact-head re-review, explicit principal exact-head acceptance, merge, and post-merge
verification — the same lifecycle every filing in this program has carried.

**What the next unit may then do — recorded as scope, not authorization, and performed nowhere here.**
`XASSET-0030` §G.B steps 2–11, as one coherent pass: reconcile the final accepted semantics into the
canonical artifacts; correct the §C enforcement conformance defect (now load-bearing for up to 480
constructions per §F.8) and any other the final semantics require; implement and fully validate the
deterministic runner and result writer; extend the successor trust boundary so those exact
outcome-producing paths are load-bearing; recompute identities and pins only after all bytes stabilize;
independently review, principal-accept, merge, and post-merge verify that exact package; perform **one**
successor operational-authorization rebinding against those merged bytes; treat post-rebinding readiness
as read-only verification; fail closed on any drift; and only then produce the external one-shot
attestation and arm. **§G.B's invariant is restated unchanged: no outcome-producing executable code may
be created, changed, or left outside the bound execution identity after the final rebinding and before
`ATTEMPT_1`.**

**This decision authorizes none of §G.B and performs no part of it.**

### J. Work deliberately *not* created

Applying `XASSET-0034` §E.4's discipline, so this filing removes successor work rather than adding it:

| Candidate successor requirement | Why not created |
|---|---|
| Close `G3` / `G5` satisfaction | `XASSET-0027` §M.3 / §M.4 assign these to per-candidate study findings; §G gives a recording posture, not an answer |
| Close `G8` snapshot composition, `G9` path-1 source satisfaction, `G10` blocker-1 snapshot status | Each requires a candidate source or a snapshot successor; `XASSET-0034` §D classified all three execution-ready |
| A program-wide gate-modal register rule | `XASSET-0033` §I records its reach over **every** gate as a caution; §E is `G12`-scoped precisely to avoid it |
| Extend `g2_reading_mapping` to any other gate | `XASSET-0032` rejected it; §M.1 routes §K.1 through `G2` alone |
| Resolve `XASSET-0024` §K.1 | Not required by any of the three; expressly left unresolved |
| Amend `XASSET-0020` §E.1 | Not required; and it is `G1`'s and `G2`'s invalidation trigger |
| Correct the `XASSET-0030` §C enforcement defect | A load-bearing implementation path; §G.B step 3's work, recorded at §F.8 |
| Relabel the 360 as `UNORDERED_PAIR` constructions | §F.6 — consumption is not identity; the universe and its hash are untouched |
| A separate filing per blocker | §C's five-question test returned one coherent unit |

### K. Absolute non-authorization

This decision generates no `XASSET-0029` attestation and creates no `READY`, `CLAIMED`, or `COMPLETED`
lane state; arms and executes no Stage 1; creates no Stage-1 runner, result writer, serializer, or
`stage1_results.yaml`; creates no `AUTHORIZATION_ROOT`; consumes nothing of `ATTEMPT_1`; **evaluates no
gate for any construction and asserts no per-construction outcome**; closes no gate on satisfaction and
changes no gate's class, index, question, controlling authority, or failure disposition; adds, removes,
or reorders no gate; corrects no validator, extends no `LOAD_BEARING_RELPATHS`, and performs no
load-bearing reauthorization or rebinding; amends no canonical file and changes no hash pin, universe,
cardinality, `comparison_subject_kind`, `unordered_pair_id`, or construction identity; enters no part of
§G.B; acquires no market, fundamental, economic, or Stage-2 data; resolves `XASSET-0024` §K.1 neither
way and leaves `XASSET-0020` §E.1 unamended; leaves `XASSET-0031`'s `G3` determination untouched and
unused as a premise; grants no Stage 2 and no application authority; creates no representation
aggregation or selection rule and designates no CM-14–CM-17 membership; creates no snapshot successor;
selects no sleeve and creates no endpoint, bound, point, range, percentage, weight, rank, target, or
allocation; weakens no validator or test; **reads, lists, opens, or references no `risk_lane_boundary`
protected result path** and reuses no `RISK` scenario, value, parameter, window, or result; changes no
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, tier, cluster, cap,
or margin state; authorizes no chart, ladder, deployment, trade, order, or brokerage action; and
rewrites no accepted history.

## Rationale

Four consecutive filings asked *is this gate closable?* and answered no six times. `XASSET-0034` then
asked a different question — *which of those openings actually defeats determinism?* — and found that
five were satisfaction residues that never blocked §G.B, while three were semantic choices that did. It
declined to resolve them, correctly: it was chartered to decide sequencing, and a recording-posture rule
binding every gate result in an irreversible 680-construction run "deserves its own independent review
anchored to its own head."

This unit is that review's subject, and the useful finding was that the three blockers are not the same
kind of problem.

**Two are readings that accepted authority already settles, and the settling texts were sitting
unexamined.** `XASSET-0032` §G.4 recorded that "nothing selects" between the two `G10` consumption
readings — but `XASSET-0020` §H, in the same section that defines the six pairs, states that a
sleeve-centric view of a pair "does not create a seventh record", and requires every pair record to
carry a direction for each of the six driver classes. The 360 `DIRECT_ALTERNATIVE` constructions carry
three of those six and name two sleeves; they are pair views, and §H says so. §I adds that surviving a
missing pair requires endpoints "independently and directly governed" and "not a derived relationship",
which comparative evidence is not. And the competing reading turns out to rest on an inference
`XASSET-0032` itself already barred one page earlier, for a different group, on `XASSET-0030` Standard 1
— specification silence is not proof of non-consumption. That is not a preference between defensible
readings; it is one reading foreclosed by authority in force.

`XASSET-0034` §E.3 said no accepted authority states which of the four values a reserved gate records.
The canonical `categorical_definition` states what `BLOCKED_CATEGORICALLY` *means* —
`NOT_CLOSEABLE_BY_A_NAMED_PREREQUISITE_UNDER_THE_CURRENTLY_ACCEPTED_METHODOLOGY` — and that is the
missing hinge. Recording `FAIL` on `G3` asserts non-closeability, which `XASSET-0027` §M.3 expressly
declines to determine; Standard 1 bars `PASS`; the prerequisite limb is closed to a categorical-class
gate; `NOT_APPLICABLE` is false. One value remains, and it is the one that describes the state honestly.
The vocabulary was never the gap, as `XASSET-0034` §B.3 said — but neither was the answer absent. It was
recoverable by elimination, which is why §G adds no rule.

**One is a genuine gap that no evidence can ever fill, and governance had already been told to fill
it.** A tense is not a fact about a source. `XASSET-0033` was right to refuse to close `G12` by reading —
its bar was that the competing reading be shown *unlawful*, and reading a gate on its face is not
unlawful. But its §I did not leave the matter open; it named the corrective as a governed `G12`-scoped
modal statement, and `XASSET-0030` §G.A had listed "a governed **definition**" as the prerequisite from
the start. Deferring again would not have been caution. It would have terminated the program on an
undefined modal, which is the outcome `XASSET-0034` rejected as ending on a construction rather than on
evidence.

The direction was chosen on the canonical register, not on the count of blocked constructions — and the
strongest ground is one no prior filing had put on the table. **Nine of the twelve canonical gate
questions are phrased "Would the candidate …"**, a register only coherent about a source that does not
yet exist; the gate-level abstention conditions are counterfactual too. `XASSET-0033` §F.3's first
obstacle was that the satisfiability register lived at Stage-1 level rather than gate level. It lives at
gate level, in the gate questions themselves. Reading `G12` alone against world state would give one
gate of twelve a different evaluand than the other eleven, against `XASSET-0028` §F's binding rule that
Stage 1 evaluates one frozen specification "under the twelve gates". And it would make `G12`'s result
readable off a frozen identity field — the by-construction inference this program rejects in both
directions.

Two disciplines mattered more than the conclusions. The first is that constitutive and interpretive acts
are labelled as such, per blocker and in the headings, so a reviewer is never invited to mistake a
governed choice for a discovered reading. The second is B3's scope. Stated broadly — "reserved gates
record `UNABLE_TO_DETERMINE`" — B3 would have swallowed `G10` and `G12`, quietly deciding B1 and B2 by
side effect and destroying the categorical consequence §F identifies. Batching three questions in one
filing is safe only because the third is fenced, and the fence is operative text rather than an
intention.

Finally, this filing does not report unqualified progress. §F.8 records that resolving B2 converts
`XASSET-0030` §C's enforcement defect from a hypothetical into a live obstruction for up to 480 of 680
constructions, and §E.5 and §G.5 record that B1 and B3 are disposition-inert today and would be easy to
wave through on that basis — which `XASSET-0032` §H.5 forecloses. The §G.B pass is now reachable, and it
is larger than it looked.

## Alternatives Considered

**File three separate governance PRs.** Rejected. One shared authority surface, one method, disjoint
gate sets, no cross-gate policy once B3 is fenced, and each judgment separately sectioned and separately
tested. Resolving two of three leaves §G.B locked anyway, so partial filing buys nothing but lifecycle.

**Isolate B1 because it is constitutive.** Seriously considered — it is the only governed choice here and
the one `XASSET-0033` just declined. Rejected because splitting weakens rather than strengthens review:
a reviewer must verify all three to confirm §G.B unlocks, and B1's constitutive character is disclosed
in its own heading, at §D, and at §E.1 rather than being smuggled in by adjacency. `XASSET-0032` §C
question 5 asks whether batching hides separate judgments; labelling makes it harder to hide, not
easier.

**Close B1 interpretively on the strength of B.4's nine-of-twelve register finding.** Rejected, and this
was the closest call. The finding is strong enough to close `XASSET-0033` §F.3 obstacle 1, but obstacles
2 and 3 survive: `G12` is one of the three gates *not* phrased "Would", an executor reading its embedded
modal on its face is reading the canonical artifact, and `XASSET-0025` §D already establishes that a
universal structural negative is not absurd. Claiming interpretive closure would have overstated the
authority and mislabelled a governed choice — the precise failure `XASSET-0030`'s corrections were
about.

**Adopt the present-tense / world-state register for `G12`.** Rejected on §E.3, not on outcome. After
`XASSET-0033` §E stripped both of its cited supports, its affirmative ground reduces to an undefined
modal plus a frozen identity field — and selecting a register because the modal is in that register is
circular. It would also isolate one gate's evaluand from the other eleven.

**Fold B3 into B1 as one modal/recording question.** Rejected, following `XASSET-0034`'s own reasoning:
a program-wide modal rule reaches every gate including the six recorded closable, and `XASSET-0033` §I
flags that reach as a caution. B3 is narrower and stays narrower.

**State B3 as a general rule for all source-dependent gates.** Rejected as the most dangerous available
shortcut. It would give `G10` an uncertainty posture, silently nullifying §F's categorical consequence
for up to 480 constructions, and would give `G12` one, silently nullifying §E. §G.4 fences it to the
three gates that share the express-reservation ground.

**Record `G10` `FAIL` for the 480 consuming constructions.** Rejected. `G10` turns on the pair's status
at **evaluation time**, and `XASSET-0021` §D's all-six-unresolved determination is expressly scoped
"under this snapshot". Recording a result would close `XASSET-0034` §D.5's satisfaction residue, which
requires a snapshot successor this program may not create.

**Record `G10` `PASS` for the 200 non-consuming constructions.** Rejected — `XASSET-0032` §G.5 stands.
A specification's silence about pair consumption is not proof an eventual source consumes no pair.

**Resolve B2 by relabelling the 360 as `UNORDERED_PAIR` constructions.** Rejected outright. It would
change frozen construction identity, the universe, and its hash, and would convert a substance finding
into a specification edit. §F.6 makes the separation operative: consumption is not identity.

**Leave B2 to the Stage-1 executor, since it concerns 360 enumerable constructions.** Rejected.
`XASSET-0032` rejected run-time semantics outright on `ATTEMPT_1`'s one-shot character, and
`XASSET-0034` §C preserved that rejection in full. Enumerability makes a question answerable now; it
does not make it an executor's to answer.

**Correct `XASSET-0032`'s, `XASSET-0033`'s, or `XASSET-0034`'s text in place.** Rejected. All are
accepted; none has its classification changed by this filing; §H.3 records the three corrections
forward, the convention `XASSET-0032` §J and `XASSET-0033` §H each followed.

**Correct the `XASSET-0030` §C enforcement defect here, now that §F.8 makes it load-bearing.** Rejected.
It is a load-bearing implementation path, its correction deliberately creates enforcement drift
(`XASSET-0030` §D), and it belongs to §G.B step 3 where the final semantics determine what the corrected
enforcement must encode. Recording the raised stakes is this unit's remit; discharging them is not.

**Declare §G.B unlocked on merge of this PR.** Rejected. §I ties it to accepted lifecycle closure.

**Abstain on all three and file the analysis only.** Rejected. B2 and B3 are settled by authority in
force, so abstaining would misreport them as open; and B1 can never be settled by evidence, so
abstaining there is not deferral but termination.

## Consequences

`XASSET-0030` §G.A is **closed**. Its six items are now five execution-ready satisfaction residues that
were never entry conditions and one — `G12` — resolved by a governed `G12`-scoped modal statement, with
`G10`'s consumption semantics and the reserved-gate recording posture resolved alongside it. §G.B may
begin once this decision completes its own lifecycle, and not before.

Two of the three resolutions cost nothing to carry forward, because they add no rule: §F assembles
`XASSET-0020` §H and §I with `XASSET-0024` §H.4 and the canonical abstention conditions, and §G
eliminates over a closed four-value vocabulary using the canonical class definitions. The third, §E, is
a governed statement and is scoped to one gate precisely so that the `XASSET-0030` 6/6 partition
survives it — verified trigger by trigger at §H.1.

The countervailing result is that the §G.B pass is now **larger** than `XASSET-0034` left it. §F.8
establishes that `XASSET-0030` §C's enforcement conformance defect is load-bearing for up to 480 of 680
constructions rather than hypothetical: a lawfully-reached categorical disposition is currently
unpublishable, and B2's resolution is what makes that reachable. A successor scoped against
`XASSET-0034` alone would have met that at implementation time. It is recorded now, unfixed and
deliberately so.

Three gate results are disposition-inert today — `G3`, `G5`, `G9` under §G, and `G12` under §E — because
`G2` already carries `UNABLE_TO_DETERMINE` for all 680. That is stated rather than relied on. Every
applicable gate must still be evaluated and recorded, and each becomes outcome-determining the moment
`XASSET-0024` §K.1 resolves, which no filing in this program has done.

What remains before an irreversible run is now implementation rather than interpretation: canonical
reconciliation, one enforcement correction, a runner and result writer bound inside the execution
identity, and one rebinding lifecycle. **Stage 1 stays UNARMED, `ATTEMPT_1` stays intact and unclaimed,
and no portfolio, allocation, target, holding, gate, margin, ladder, chart, order, or trade state is
changed or authorized by this filing.**
