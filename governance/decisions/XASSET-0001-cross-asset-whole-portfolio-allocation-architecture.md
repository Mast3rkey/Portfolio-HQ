---
decision_id: XASSET-0001
date: 2026-08-06
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, OPS-0011, OPS-0012, OPS-0013, OPS-0014, OPS-0015, OPS-0016, PI-0016, PI-0031, PI-0035, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, MARGIN-0005, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001]
supporting_artifact: null
file: governance/decisions/XASSET-0001-cross-asset-whole-portfolio-allocation-architecture.md
---

## Context

### Authority for this unit

The human repository principal authorized this filing alongside `CONTENDER-0001` in the same Lane G
(`OPS-0009` §1) governance PR. `CONTENDER-0001` establishes that the 27 sealed equity classifications
are Portfolio-HQ's first completed blind-classification cohort, not the exhaustive universe, and that
every genuine ticker anywhere in the repository is eligible for future contender screening. This
filing addresses the companion question that principle leaves open: **what governed architecture is
required before any final, controlling whole-portfolio target policy may be adopted**, given that
Portfolio-HQ's actual holdings span individual equities, ETFs, cryptocurrency, GLD, cash/reserve, and
margin debt — not equities alone. This filing authorizes architecture and sequencing only.

### Preflight performed this session, independently verified, not assumed

Repository identity, `origin/main` state (`f71ea3bb1428445023c4fa582ed953ae409ba070`), zero open PRs,
PR #255's full lifecycle, the 81-decision catalog, `WS-0014` as the next unused workstream identifier,
`XASSET-####`/`CONTENDER-####` as genuinely new, unused decision prefixes, live `targets.yaml`'s 36
destination rows, and the sole `priority: primary` workstream (`WS-0005`) were all independently
re-verified this session — see `CONTENDER-0001`'s Context section for the full preflight record,
performed once and shared by both filings in this PR. Additionally for this filing:

- **`WS-0005`'s Milestone 7–9 gate text independently re-read in full** from live
  `operations/WORKSTREAMS.yaml` (lines 2043–2077) — quoted verbatim in §H below, not restated from
  memory.
- **`WS-0013`'s complete live entry independently re-read in full** (`operations/WORKSTREAMS.yaml`
  lines 7498–7637) — `status: proposed`, `priority: secondary`, `authorized_scope: "none — durable
  planning intent only"`, `dependencies: [WS-0005, WS-0012]`, `active_branch:
  claude/eureka-architecture-reconciliation-93det0`, `active_pr: 236`, `last_verified_main_sha:
  2a934549f5d6383e795cfd312dc2b443dc347c63`, `last_verified_date: "2026-08-04"` — all confirmed live
  and unchanged since `OPS-0016`'s own last touch. `completion_criteria` step (5), quoted verbatim:
  "the zero-based portfolio review (WS-0005 Milestones 5-7) complete" — this is the exact phrase this
  filing's §J clarifies (WS-0005 Milestones 5-7 are equity-only; a separate cross-asset dependency is
  required and was previously unrecorded).
- **No ETF-, crypto-, reserve-, GLD-, or debt-specific Intelligence or classification framework**
  independently reconfirmed absent from the repository — a full grep for schema/validator/record
  shapes matching any of those asset types beyond `targets.yaml`'s own `destination:` rows and
  `holdings.yaml`'s `crypto_shares:` block returns nothing resembling `TIER-0002`'s four-axis company
  framework or any analogous ETF/crypto equivalent.

## Decision

### A. Portfolio objective (preserved, not newly invented)

This filing records, and does not alter, Portfolio-HQ's governing objective:

> Maximize long-term portfolio compounding and capital appreciation within approved risk, liquidity,
> concentration, leverage, and survival constraints.

Expected capital gains are central to this objective but do not silently override reserve
requirements, concentration limits, liquidity, drawdown survivability, the leverage cap, the
margin-buffer floor, or evidence uncertainty. This restates CLAUDE.md's existing Portfolio Doctrine
(margin cap/buffer floor) and Guardrails (margin-buffer-below-30%-forces-de-lever, no predictive
research, cash-tight recommends inaction) in objective form — it changes no existing guardrail,
margin parameter, or allocator rule. This objective governs both the future contender-screening work
`CONTENDER-0001` authorizes in principle and the cross-asset architecture this filing defines; it does
not itself authorize either.

### B. The current 27-cohort boundary, as it bears on Milestone 7

The 27 sealed Milestone 6 equity records remain valid, complete for their authorized cohort, immutable
evidence inputs, and are **not reopened by this filing** — matching `CONTENDER-0001` §D exactly. They
are not the exhaustive equity universe, not the entire opportunity universe, and **not sufficient
alone to determine final whole-portfolio targets**, because they say nothing about ETFs,
cryptocurrency, cash/reserve, GLD, or debt reduction — five of the eleven `targets.yaml` sleeve
categories a whole-portfolio decision must weigh.

Every future Milestone 7 implementation artifact and PR must therefore disclose, verbatim or in
substance, the following boundary statement — added here as a durable requirement on all future
Milestone 7 work, not merely a suggestion:

> This reconciliation covers the 27 canonical equity destinations only. ETF, cryptocurrency,
> cash/reserve, GLD/defensive-asset, debt-reduction, and broader contender-universe allocation remain
> governed separately and are not represented as concluded here.

This requirement supplements, and does not narrow or loosen, `TIER-0007`'s existing Milestone 7
specification (§§A–O of that filing) — every sealed-record-integrity check, permitted-input list,
disposition vocabulary, and non-authorization boundary `TIER-0007` already defines remains fully
controlling. This filing adds exactly one new disclosure requirement on top of it.

### C. Asset-appropriate blind classification — no forcing a single schema across asset types

`TIER-0002`'s four-axis equity framework (`economic_role`, `capital_priority`, `risk_concentration`,
`evidence_quality`) and the Company Intelligence schema it builds on (`docs/PORTFOLIO_INTELLIGENCE_
SPEC.md` §9/§20/§24, frozen under `PI-0001`) are **equity-shaped by design** — built around a
company's own economic role, competitive position, and financial disclosures. Neither fits an ETF (a
basket with no independent "economic role" of its own — its role is a function of its constituents
and its look-through exposure, already partially captured by `issuer_lookthrough.yaml`) or a
cryptocurrency (no issuer, no financial statements, no earnings, no "capital priority" comparable to a
company's).

This filing therefore requires, as future doctrine, three distinct treatments:

1. **Additional research-ready equities** use the existing, already-frozen equity Company
   Intelligence schema and, once evidence-ready, the existing `TIER-0002` four-axis blind-
   classification framework — no new equity framework is required; only new cohorts of it, under
   their own future `WS-0014` authorization.
2. **ETFs require a separately governed, ETF-specific blind framework**, not authorized or designed
   by this filing. It must be designed from ETF-appropriate evidence: constituent look-through
   overlap with individually held equities (extending `issuer_lookthrough.yaml`'s existing point-in-
   time constituent-weight mechanism), expense ratio, tracking quality, geographic/currency exposure,
   and the fund's structural role in the portfolio (broad-market beta, developed-ex-US, emerging
   markets — matching `targets.yaml`'s current SPY/VEA/VWO members) — never forced into
   `TIER-0002`'s company-shaped fields.
3. **Cryptocurrencies require a separately governed, crypto-specific blind framework**, not
   authorized or designed by this filing. It must be designed from crypto-appropriate evidence:
   network/protocol fundamentals, liquidity and market-structure characteristics, custody/
   counterparty risk, cross-asset and cross-coin correlation, and volatility/drawdown behavior
   distinct from equity risk — never forced into a company-shaped economic-role or capital-priority
   field, and explicitly preserving CLAUDE.md's existing crypto-sleeve doctrine (conviction-sizing,
   no timing gates) as unchanged, unless and until a future, separately authorized decision revisits
   it.

Forcing ETF or cryptocurrency evidence into the Company Intelligence or `TIER-0002` equity schema is
**explicitly prohibited** by this filing — a future implementation must design new, asset-appropriate
schemas rather than stretch the existing one, matching this repository's own precedent of designing a
new data model when an existing one's shape genuinely does not fit (`PI-0006`'s Theme Intelligence
freeze, explicitly distinct from Company Intelligence; `REL-0001`'s new pairwise relationship
namespace, explicitly not a Company Intelligence schema extension).

### D. Cash, reserve, GLD, and debt reduction — functional doctrine, not company-style classification

Cash/reserve, GLD/defensive assets, and debt reduction are not investable "companies" or
"instruments" whose economic merit can be blind-classified the way an equity, ETF, or cryptocurrency
can. They require **governed functional doctrine as competing uses of capital**, not classification:
a future, separately authorized decision must define the criteria under which incremental capital is
directed toward reserve/cash buffer, GLD/defensive ballast, or debt (margin) paydown versus toward an
equity/ETF/crypto sleeve — as an explicit Level 1 sleeve-allocation input (§E), governed by the same
opportunity-cost discipline as every other sleeve, not treated as a residual or an afterthought. This
filing does not itself define that doctrine; it records that it is required and assigns its future
authorship to `WS-0014` (§I).

### E. Whole-portfolio allocation architecture — two levels

Final portfolio allocation requires two distinct, sequenced decision layers, neither of which the 27
sealed equity records alone can settle:

**Level 1 — sleeve allocation.** How much of the whole portfolio should be directed toward each of:

- individual equities;
- ETFs;
- cryptocurrency;
- GLD/defensive assets;
- cash/reserve;
- debt reduction or leverage reduction (paying down margin versus deploying incremental capital
  elsewhere).

**Level 2 — instrument allocation inside each approved sleeve.** Given a Level 1 sleeve allocation,
which specific equities, which specific ETFs, which specific cryptocurrencies receive capital within
that sleeve's budget — this is the layer `targets.yaml`'s current `destination:` rows already operate
at, and the layer the sealed 27-equity Milestone 6/7 work addresses for the equity sleeve specifically.

**Final portfolio allocation must compare opportunity cost across all governed sleeves** — a dollar's
best use is never determined by comparing it only against other equities; it must be weighed against
the ETF sleeve, the crypto sleeve, GLD, cash/reserve, and debt reduction, using the objective in §A.
**Final instrument targets cannot be declared globally optimal merely by allocating among the existing
27 equities** — that would silently answer a Level 2 (equity-instrument) question while leaving every
Level 1 (sleeve) question unaddressed. This is the precise failure mode `CONTENDER-0001` §D and this
filing's own §H exist to foreclose.

This filing defines the two-level architecture. It does not perform Level 1 or Level 2 sizing of any
kind, and it does not authorize any future filing to perform either without its own separate,
explicit authorization.

### F. Overlap, concentration, and risk — required future accounting, not implemented here

A future cross-asset architecture must account for, at minimum:

- ETF look-through overlap with individually held equities (extending, not duplicating,
  `issuer_lookthrough.yaml`'s existing point-in-time constituent-weight mechanism);
- sector and correlated-cluster duplication across sleeves (extending, not duplicating,
  `targets.yaml`'s existing `caps.clusters` mechanism and the `intelligence/relationships/` corpus
  `REL-0001`–`REL-0006` established);
- issuer concentration (extending, not duplicating, the existing 8% effective-issuer / 40%
  AI-platform-common-driver no-add ceilings in `issuer_lookthrough.yaml`);
- geographic and currency exposure (relevant to VEA/VWO and any future international or
  currency-denominated instrument);
- crypto cross-correlation (BTC/ETH/SOL's own correlation with each other and, separately, with
  risk-on equity beta);
- volatility and drawdown concentration across the whole portfolio, not sleeve-by-sleeve in isolation;
- liquidity (how quickly each sleeve can be converted to cash without material value loss, distinct
  from margin-buffer capacity);
- duplicated exposure across sleeves (e.g., an ETF whose constituents already include a directly held
  equity, or a crypto position whose economic driver overlaps an equity's own thesis);
- margin and debt interaction (how each sleeve's own volatility and liquidity characteristics
  interact with the existing 1.8x leverage cap and 30% buffer floor — unchanged, unweakened, and
  explicitly not reopened by this filing).

**This filing does not implement any of these models.** It records them as required future work,
assigned to `WS-0014` (§I), to be designed, reviewed, and authorized on the same bounded,
one-authorization-per-unit discipline every prior WS-0005 milestone in this repository has followed.

### G. Chart boundary — unchanged, restated

Fundamentals, classification, contender screening, and cross-asset policy determine what deserves
capital and its approved limits. Chart evidence remains strictly downstream: it may later inform
timing, staging, monitoring, and technical-risk review **within already-approved policy**, but it
**never automatically changes membership, tier, sleeve target, instrument target, cap, or trade** —
matching `TIER-0003`'s existing fundamentals-only blind-classification boundary and `CHART-0001`/
`CHART-0002`'s own explicit "advisory only, never automatically changes a technical signal, score,
rank, or trigger a transaction" restrictions. **`TIER-0003` is not reopened, narrowed, or
reinterpreted by this filing.** This applies identically across every sleeve this filing defines —
chart evidence is no more authoritative for an ETF, a cryptocurrency, or a cash/GLD/debt decision than
it already is, per `TIER-0003`, for an equity.

### H. Milestones 7–9 boundary

`operations/WORKSTREAMS.yaml`'s Milestone 7–9 gate text, unedited by this filing, quoted verbatim:

> **Milestone 7 (`milestone-7-baseline-reconciliation`):** Unblind the sealed baseline and compare
> current-vs-researched role, tier-vs-proposed capital priority, target-vs-evidence-supported range,
> cluster-vs-relationship-map, caps-vs-portfolio risk, review cadence-vs-thesis uncertainty; every
> difference states evidence, reasoning, uncertainty, opportunity cost, controlling policy, and
> required governance action. Not authorized to execute.
>
> **Milestone 8 (`milestone-8-policy-recommendation-package`):** Advisory-only recommendations
> covering portfolio roles, tier/replacement classification architecture, capital-priority rules,
> targets/target ranges, maximum position sizes, economic-system/overlap limits, monitoring
> frequency, thesis-break review rules, add/hold/trim/exit-review discipline. Not authorized to
> execute.
>
> **Milestone 9 (`milestone-9-independent-review-and-later-adoption`):** Independent review... of
> research coverage, relationship methodology, zero-based protocol adherence, candidate tier
> architecture, the policy recommendation package, evidence-versus-judgment separation, and absence
> of hidden scoring or allocator coupling. Any adoption requires its own separate accepted governance
> decision and a later, separately authorized implementation PR. Not authorized to execute.

This filing binds the following requirements to that existing text, without editing it:

- **Milestone 7 is a bounded 27-equity reconciliation.** It does not, and must not be represented as,
  establishing global opportunity optimality across the whole portfolio — see §B's disclosure
  requirement, binding on every future Milestone 7 artifact.
- **Milestone 8 must clearly label any 27-equity-cohort-derived result as equity-scoped** in every
  finding, recommendation, and summary it produces. It must not present an equity-only conclusion in
  language that reads as a whole-portfolio conclusion.
- **Milestone 8 cannot claim final whole-portfolio target readiness before the cross-asset work this
  filing requires (§C–§F, executed under `WS-0014`) completes.** A Milestone 8 policy-recommendation
  package that addresses only the equity sleeve is permitted to exist and be reviewed on its own
  equity-scoped terms, but it cannot itself be the basis for a final, controlling whole-portfolio
  target adoption — that requires the normalized contender coverage (`CONTENDER-0001`) and the
  cross-asset sleeve/instrument synthesis this filing defines to also be complete.
- **Final controlling whole-portfolio target adoption must wait** for: normalized contender coverage
  under `CONTENDER-0001`; asset-appropriate blind-classification frameworks and their execution for
  ETFs and cryptocurrency (§C); functional cash/reserve/GLD/debt doctrine (§D); the overlap and
  concentration modeling required by §F; and Level 1 sleeve-allocation and Level 2 instrument-
  allocation synthesis (§E) — each its own separately authorized future unit under `WS-0014`.
- **Milestone 9 does not silently convert equity-only findings into final whole-portfolio policy.**
  Its own text already requires "absence of hidden scoring or allocator coupling" and states "any
  adoption requires its own separate accepted governance decision" — this filing makes explicit that
  an equity-scoped Milestone 8 package, even if independently reviewed and found sound under
  Milestone 9's standard, does not by itself constitute or authorize whole-portfolio policy adoption.

This filing does not modify `TIER-0007` (Milestone 7's own detailed specification — eighteen-field
schema, primary/secondary disposition, categorical target-context comparison) beyond the additive
disclosure requirement in §B, and does not modify the Milestone 7/8/9 gate text quoted above. The
factual, additive cross-reference this filing adds is recorded in `operations/WORKSTREAMS.yaml` (§K)
— no `governing_authority`, `authorized_scope`, `prohibited_scope`, or `completion_criteria` field on
any existing `WS-0005` gate is changed.

### I. New workstream — `WS-0014`

This filing authorizes creation of **`WS-0014`**, a new, dedicated workstream to own future:

1. contender normalization (per `CONTENDER-0001` §C);
2. research-readiness screening;
3. additional-equity blind-classification cohorts (using the existing `TIER-0002` framework, per §C
   item 1);
4. ETF framework design (§C item 2);
5. ETF blind classification;
6. crypto framework design (§C item 3);
7. crypto blind classification;
8. cash/reserve/GLD/debt functional doctrine (§D);
9. cross-asset overlap and concentration modeling (§F);
10. cross-asset synthesis (§E);
11. sleeve-level candidate targets (§E, Level 1);
12. instrument-level candidate targets (§E, Level 2);
13. chart-informed deployment integration (§G, within already-approved policy only);
14. final independent audit.

`WS-0014` begins, and this filing authorizes nothing beyond:

- `status: proposed`;
- `priority: secondary` (`WS-0005` remains the sole `priority: primary` workstream — unchanged by
  this filing);
- `authorized_scope: "none — architecture and sequencing planning only, recorded by this filing;
  no execution unit authorized"`;
- no active implementation PR beyond this governance filing itself;
- `dependencies: [WS-0005, CONTENDER-0001 (governance record, not a workstream)]` — `WS-0014`'s
  contender-normalization work (item 1) depends on `CONTENDER-0001`'s principle; its equity-cohort
  work (items 2–3) depends on `WS-0005`'s Milestone 3–7 evidence.

No item in the fourteen-item list above is itself authorized to begin by this filing — each requires
its own separate, future, explicit principal authorization and its own bounded implementation or
research PR, matching the discipline `WS-0005` and `WS-0013` already apply to their own future
milestones. The exact `operations/WORKSTREAMS.yaml` entry is added in §K.

### J. Dependency order and batching

The recommended dependency order for `WS-0014`'s future work, none of it authorized to begin by this
filing:

0. this architecture filing (`CONTENDER-0001` + `XASSET-0001`);
1. contender normalization plus research-readiness screening;
2. additional-equity blind cohorts;
3. ETF and crypto framework design;
4. ETF classification;
5. crypto classification;
6. cash/reserve/GLD/debt doctrine;
7. overlap and concentration modeling;
8. cross-asset synthesis;
9. sleeve-level candidate targets;
10. instrument-level candidate targets;
11. chart-informed deployment;
12. final independent audit;
13. convergence into `WS-0013`'s final allocation-readiness sequence.

**Future safe batching is permitted only where explicitly coherent**, matching `OPS-0008`'s Research
Wave Protocol discipline (a genuine common mechanism, not a shared label, justifies one unit):

- contender normalization + research-readiness screening (step 1) — genuinely one evidence-gathering
  pass;
- structural ETF + crypto framework **design** (step 3) — both are schema-design exercises, not
  content research, and may reasonably batch as one architecture unit even though the two frameworks
  differ in content;
- cash/GLD/debt doctrine + overlap-model **architecture** (steps 6–7) — permitted to batch only where
  no asset-specific judgment occurs (i.e., defining the doctrine's shape and the overlap model's
  shape, not applying either to a specific instrument or sleeve).

**Separate lifecycle units are required, never batched, for:**

- framework design versus blind-classification execution (step 3 must never be combined with step 4
  or step 5 — a schema must exist and be reviewed before it is applied to real evidence, matching
  `TIER-0001`/`TIER-0002`'s design-then-authorize-content precedent for the equity sleeve);
- ETF versus crypto classification (steps 4 and 5 — different asset types, different evidence
  standards, never one filing);
- every completion determination (each future milestone-equivalent gate under `WS-0014` requires its
  own separate completion-determination filing, matching `PI-0037`/`REL-0006`/`TIER-0006`'s precedent
  — a batch's own narrative "this is done" is never sufficient by itself);
- sleeve-level versus instrument-level targets (steps 9 and 10 — Level 1 and Level 2 of §E are
  sequentially dependent and must not be decided in the same filing, since a Level 2 instrument
  target inside a sleeve is only meaningful once that sleeve's own Level 1 budget is set);
- the final independent audit (step 12) — its own standalone unit, never folded into step 8, 9, 10,
  or 11's own filing.

### K. Register updates performed by this filing

`operations/WORKSTREAMS.yaml` receives exactly two changes:

1. **A new `WS-0014` entry** (full text in the accompanying commit), `status: proposed`, `priority:
   secondary`, `authorized_scope` and `prohibited_scope` matching §I exactly, `milestones: []` (no
   gate has yet been authorized to begin), `dependencies: [WS-0005]`, `governing_authority:
   [CONTENDER-0001, XASSET-0001, OPS-0001, OPS-0006 (equity precedent, dependency reference only),
   OPS-0007, OPS-0009]`, `evidence_refs: [CONTENDER-0001, XASSET-0001]`, `next_action: "None
   authorized. WS-0014's first step (contender normalization, item 1 of the fourteen-item list) may
   not begin without its own separate, future, explicit principal authorization."`,
   `completion_criteria: "Not applicable — no execution is authorized under this workstream by this
   filing. §J's dependency-ordered roadmap records what a future completion-determination decision
   would need to verify, in order, once execution begins."`, `blocker: "Every item in the
   fourteen-item scope list is blocked on its own future, separate, explicit principal authorization
   — none is authorized to begin by this entry."`
2. **One additive `WS-0013` milestone entry**, `gate: xasset0001-cross-asset-dependency-cross-
   reference-recorded`, recording — without editing any existing `WS-0013` field — that: `WS-0005`
   Milestones 5–7 are equity-only, per `CONTENDER-0001`/`XASSET-0001`; `WS-0014` is a required future
   dependency before any final allocation-readiness claim, alongside `WS-0005` and `WS-0012`; and
   `WS-0013` remains non-authorizing throughout — this addition changes no `WS-0013` `status`,
   `priority`, `authorized_scope`, `prohibited_scope`, `dependencies`, or `completion_criteria` field,
   matching every prior additive `WS-0013` cross-reference gate (`ops0015-...`,
   `ops0016-eureka-sequencing-...`) exactly.

No existing `WS-0005` field, gate, or self-reference value is touched by this filing.

### L. Durable language

The following statements, restated here for the record (the first three appear verbatim in
`CONTENDER-0001`; the last two are this filing's own):

> "The 27 sealed equity classifications are Portfolio-HQ's first completed blind-classification
> cohort; they are not the permanent or exhaustive contender universe."

> "Every genuine, valid investable ticker represented anywhere in Portfolio-HQ is eligible for
> governed contender screening. Current holdings, targets, tiers, gates, classifications, or
> canonical-population membership do not by themselves determine inclusion or exclusion."

> "Contender status creates evaluation eligibility only. It creates no holding, target, tier,
> allocation, policy, order, or trade authority."

> "Final whole-portfolio targets require governed treatment of equities, ETFs, cryptocurrency,
> cash/reserve, GLD or defensive assets, debt reduction, cross-asset overlap, concentration,
> opportunity cost, and portfolio-level risk."

> "No final allocation-readiness claim may be made from the 27-equity cohort alone."

### M. Explicit non-authorization

This filing authorizes architecture and sequencing only. It does not authorize:

- creation of the contender registry (`CONTENDER-0001` §F);
- ticker normalization execution;
- new ticker research of any kind;
- additional blind classification of any equity beyond the sealed 27;
- ETF or crypto classification, or design work on either framework beyond this filing's own
  architecture-level description (§C);
- Milestone 7 implementation (governed exclusively by `TIER-0007`, unedited beyond §B's additive
  disclosure requirement);
- Milestone 8 recommendations;
- any target, tier, holding, gate, cap, cluster, allocator, margin, ladder, chart, order, or trade
  change;
- any allocation check, live or scenario;
- any cash/reserve/GLD/debt doctrine content (§D describes what is required, not what it is);
- any overlap, concentration, or correlation model implementation (§F describes what is required,
  not an implementation);
- any sleeve-level or instrument-level sizing of any kind (§E defines the two-level architecture, not
  its content).

## Rationale

`TIER-0006`'s completion of Milestone 6 and the imminent authorization of Milestone 7 content
(`TIER-0007`, merged as PR #255) created a real, near-term risk that this repository's own history
shows it has hit before: a completed, well-reviewed unit of work being read — by a future session, not
maliciously, simply by proximity — as more conclusive than its own actual scope. `PI-0031` §K
explicitly anticipated this for Milestone 3 ("these seven criteria authorize no research for any
other ticker; satisfying Batch 9 does not itself complete Milestone 3"); `REL-0004`/`REL-0006` did the
same for Milestone 4. This filing applies the identical discipline one layer up: at the
whole-portfolio level, where the stakes of a premature "final target" claim are highest, because
`targets.yaml`'s actual `destination:` list already spans eleven sleeve categories (27 equities, 3
funds, GLD, 3 cryptocurrencies, RESERVE, CASH) that no purely-equity milestone sequence could ever
settle on its own.

Defining the two-level sleeve/instrument architecture (§E) before any sizing work begins follows the
same "define, then later authorize implementation" pattern this repository has used for every prior
milestone-scale undertaking (`TIER-0001`/`TIER-0002` before Milestone 6; `REL-0001` before Milestone
4's content; `TIER-0007` before Milestone 7's content) — and the same reasoning `TIER-0007`'s own
Rationale gives: fixing an underspecified boundary before content work begins is strictly cheaper than
discovering the gap after dollars' worth of research or classification work already exists on the
wrong shape.

Assigning execution to a new workstream (`WS-0014`) rather than expanding `WS-0005`'s own milestone
sequence preserves `WS-0005`'s demonstrated scope discipline (its own repeated "does not authorize a
tenth/eleventh Milestone 3 batch," "does not begin Milestone 4," "does not imply Milestone 5" pattern
across dozens of filings) and avoids retroactively redefining what "WS-0005 complete" would mean —
`WS-0005`'s nine milestones remain exactly the equity zero-based tier review `OPS-0006` originally
scoped them to be. `WS-0013` is deliberately left as the final orchestration layer, not the execution
layer, per the principal's own explicit instruction — its `completion_criteria` step (5) already named
"WS-0005 Milestones 5-7" as a dependency; this filing's §K addition makes explicit, for the first
time, that a second, previously-unrecorded dependency (`WS-0014`) also gates final allocation
readiness, without granting `WS-0013` any new authority.

## Alternatives Considered

**Expand `WS-0005`'s own milestone sequence (a "Milestone 10," cross-asset) rather than create a new
workstream.** Rejected: `WS-0005`'s objective, `governing_authority`, and nine-milestone roadmap
(`OPS-0006` §4) are specifically an equity zero-based tier review; ETF/crypto/cash/GLD/debt
architecture spans instruments `OPS-0006` never named and a decision-record family (`TIER-####`) built
specifically for the equity classification pipeline. A tenth equity-workstream milestone would either
force cross-asset work through an equity-shaped schema (exactly what §C prohibits) or require its own
extensive disclaimer language distinguishing it from the other nine — the same overhead a dedicated
workstream avoids more cleanly, directly precedented by `WS-0010`(`LADDER-0001`)/`WS-0011`
(`CHART-0001`)/`WS-0012` (`CHART-0002`), each spun out as its own workstream rather than folded into
`WS-0005`.

**Make `WS-0013` the execution workstream instead of creating `WS-0014`.** Rejected per the
principal's own explicit instruction: "`WS-0013` remains the final allocation-readiness orchestration
and dependency ledger. It does not become the execution workstream." `WS-0013`'s own existing
`authorized_scope: "none — durable planning intent only"` and its fifteen-step roadmap already
describe it as a sequencing record, not an execution owner — repurposing it would contradict its own
accepted design.

**Design the ETF and crypto blind-classification frameworks in this filing, rather than deferring
them to `WS-0014`.** Rejected: this filing's own explicit non-authorization boundary (§M) states
architecture and sequencing only. Designing a full framework (field schema, evidence standard,
disposition vocabulary — the ETF/crypto equivalent of `TIER-0001`–`TIER-0005`'s multi-filing equity
design sequence) is substantive content work requiring its own dedicated authorization and its own
independent review cycle, not a byproduct of a filing whose stated purpose is establishing that such
frameworks are needed.

**Attempt to quantify or pre-size the Level 1 sleeve allocation (e.g., "equities should be X%, crypto
Y%") in this filing.** Rejected as exactly the "final controlling whole-portfolio target adoption"
this filing itself states must wait for the full cross-asset prerequisite chain (§H) — proposing even
an illustrative number here would contradict the filing's own stated architecture-only scope and risk
being read as an implicit recommendation.

## Consequences

Once this filing merges, alongside `CONTENDER-0001`, `WS-0014` exists as a proposed, secondary,
non-executing workstream recording the future cross-asset roadmap — no execution begins. Every future
Milestone 7 artifact must carry §B's disclosure statement. Every future Milestone 8 filing must
comply with §H's equity-scoped labeling requirement and may not claim final whole-portfolio target
readiness. `WS-0013`'s completion criteria now correctly reflect a previously-unrecorded dependency
(`WS-0014`) alongside `WS-0005` and `WS-0012`, without gaining any new authority itself. No target,
tier, holding, gate, cap, cluster, allocator, margin, ladder, chart, order, or trade changes as a
result of this filing; `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
`allocate.py`, `margin_state.py`, `levels.py`, every existing Company/Theme/Relationship Intelligence
record, and all 27 sealed classification records remain byte-identical to their pre-filing state.
