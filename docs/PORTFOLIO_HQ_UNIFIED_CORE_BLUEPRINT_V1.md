# Portfolio-HQ Unified Core Blueprint V1

_Draft planning baseline for WS-0002 (`operations/WORKSTREAMS.yaml`), filed under
`governance/decisions/OPS-0002-unified-core-planning-and-audit-gate.md`. Status:
**draft, unaudited, unmerged.** This document is planning and architecture material
only — it authorizes no implementation, no allocator/policy/target/holdings/margin
change, no research execution, no Intelligence expansion, and no trade or order. It
does not itself become effective; see OPS-0002 for the governance action that
scopes what this planning package authorizes and what it does not._

_**2026-07-24 architecture correction:** the original draft of this document
incorrectly cast Company/Theme Intelligence as permanently display-only —
annotation and explanation beside the allocator's output, with no path to
influence targets, tiers, clusters, or policy at all. That was a material error,
corrected in this revision throughout §§3–7, §10, and §12: Intelligence is the
intended primary analytical and organizational basis for **recommending** how
target allocation is set — retain, promote, or demote a tier; raise, lower, or
retain a target; introduce, remove, or redefine a cluster; adjust capital
priority — but no such recommendation becomes effective merely because it
exists. It reaches the allocator only after principal review, any required
governance approval, and a separate bounded update to `targets.yaml` or another
governing source. The allocator itself still never imports or interprets raw
Intelligence at runtime. This correction changes planning architecture only —
see OPS-0002's own changelog note for the corresponding governance-record
correction._

---

## 0. Provenance and a note on source material

This blueprint was commissioned as a conversion of a prior Sonnet planning review
into a durable, repository-native artifact. **That prior report's content was not
available to the session that authored this document** — no attachment, file, or
inline text corresponding to it was present anywhere in this session's context or
in the repository. Rather than reconstruct or infer what such a report might have
said, this blueprint is built entirely from a fresh, independent re-verification of
the live repository (`origin/main` at `69723a69bb863cc792ac3f09818be64fe628ffd4`) —
the CLAUDE.md Decisions Log, the Constitution, `governance/decisions/`,
`operations/WORKSTREAMS.yaml`, `targets.yaml`/`holdings.yaml`, the Intelligence
corpus, and the MARGIN-0005 research program's actual on-disk state. Every factual
claim below was checked directly against the repository during this session, per
Constitution §6 ("verify before acting on external review") — none is copied from,
or attributed to, a document this session never saw. Where the principal's task
description specified required corrections and principles (§§2–8 below), those are
followed as authorized instructions, not as claims re-derived from an unseen report.

## 1. Purpose and scope of this document

Defines the smallest coherent architecture, priority ordering, and terminal
acceptance target needed to answer one question honestly and reproducibly: **given
current governed policy, portfolio state, risk constraints, and available
evidence, what is the best governed use of available capital now, what are the
next-best alternatives, and what uncertainty could change that conclusion?**

This is a planning artifact. It:

- proposes the WS-0002 planning baseline (definitions, boundaries, milestone);
- does **not** design, build, or authorize any code, allocator change, target/
  tier/cluster/policy change, research execution, or Intelligence expansion;
- is scoped by, and subordinate to, OPS-0002, which is the actual governance
  action authorizing anything about this planning package's review and audit.

## 2. Current priority (as authorized by OPS-0002)

The principal has made full planning, architecture, scope, sequencing, and
independent audit the immediate priority, ahead of further WS-0001 implementation.

- **WS-0002** (this planning package): `status: review`, `priority: primary`.
  Authorized only for completing this planning package, its independent audit,
  reconciliation of audit findings, and principal acceptance. No implementation
  authority.
- **WS-0001** (MARGIN-0005 research program): remains `status: in_progress` with
  every existing authority, milestone, completion criterion, and its exact
  next action (the read-only S2/G2 scope determination described in
  `operations/WORKSTREAMS.yaml`) fully intact and unchanged. `priority: secondary`.
  A principal sequencing hold applies to further WS-0001 *implementation* until
  the WS-0002 planning package and its first independent audit are complete,
  unless the principal separately authorizes otherwise. **This is a sequencing
  preference, not a finding that MARGIN-0005 is cancelled, technically blocked,
  or complete** — none of those is true, and this document does not claim
  otherwise. Verified directly: `research/margin_target_study/` contains
  `PROTOCOL_V2.md`, `pre_registration.yaml`, `G1_DATA_VALIDATION_REPORT.md`,
  `assumptions_ledger.yaml`, and `data_manifest.yaml`; `margin_simulation.py`,
  `repayment_lib.py`, and their test files exist at repository root (G2A/G2B, per
  the register); `trial_ledger.jsonl` and `candidate_freeze.yaml` are confirmed
  **absent** — no simulation has run, and zero of the charter's 300-run ceiling
  has been consumed, as of this document.

Only one workstream carries `priority: primary` at a time, per the rule
`governance/decisions/OPS-0001-portfolio-hq-workstream-register.md` already
established.

## 3. Three-layer architecture

The smallest coherent architecture Portfolio-HQ needs is three layers, strictly
separated by what may cross between them **at runtime** — which is a narrower
boundary than "Intelligence has no influence on policy at all." Intelligence is
intended to be the primary analytical and organizational basis for recommending
*how governed policy itself should be set*; it is not intended to remain
permanently confined to annotation beside an unchangeable allocator.

### Layer 1 — Authoritative deterministic allocation core

Current holdings (`holdings.yaml`), accepted targets and tiers (`targets.yaml`),
accepted concentration and margin policy (correlated-cluster caps, the T1/T2
concentration ceiling, the 1.8x leverage cap, the 30% buffer floor —
`margin_state.py`), live market data (`alpaca_client.py`, read-only), and the
allocator (`allocate.py`). At runtime, this layer consumes **only accepted,
governed policy and verified account/market state** — never raw Intelligence.
Output is a reproducible numeric recommendation: buys, trims, and blocks, computed
deterministically from current state and currently accepted policy. This layer is
**recommendation-only** — no order-placement path exists or is to be reintroduced
(Constitution §1). `allocate.py` must not import, read, or interpret any file
under `intelligence/` (or any future portfolio-level Intelligence output) to
recalculate gaps, buys, trims, weights, tiers, targets, or margin — that
prohibition is unchanged by this correction and is exactly what keeps the
allocator deterministic.

### Layer 2 — Intelligence, portfolio organization, and policy-recommendation layer

Company and Theme Intelligence (`intelligence/companies/`, `intelligence/themes/`),
research evidence, freshness state, uncertainty, thesis-break conditions, overlap,
correlation, and opportunity-cost context, and evidence conflicts/gaps. Verified
current coverage: 7 company records (COST, GEV, ISRG, NVDA, TMO, TSM, XOM) and 2
theme records (`ai_infrastructure`, `life_sciences_tools_medtech`).

This layer is responsible for organizing and evaluating, per holding and per
theme:

- each holding's economic function and portfolio role;
- company quality, moat, durability, and financial strength;
- thesis, evidence, uncertainty, risks, and thesis-break conditions;
- current business quality versus present capital priority;
- comparison with next-best capital uses;
- theme, sector, industry, customer, supplier, geographic, regulatory,
  commodity, factor, and macro exposure;
- structural and economic overlap among holdings;
- measured return correlation where evidence and methodology support it (see
  "Correlation and organizational understanding" below);
- concentration and hidden cluster risk;
- evidence freshness and conflicts;
- implications for tiers, per-holding targets, target weights, cluster
  membership, concentration policy, and portfolio organization generally.

From this evaluation, Layer 2 **may produce explicit governed recommendations**,
for example: retain, promote, or demote a holding's tier; raise, lower, or retain
a per-holding target; introduce, remove, or redefine a concentration cluster;
recommend reducing exposure where several individually attractive holdings create
excessive combined dependence; increase or decrease capital priority based on
portfolio role and opportunity cost; or retain a high-quality company while
recommending a lower present target because its opportunity cost or overlap has
changed. Every such recommendation must carry evidence, reasoning, uncertainty,
alternatives considered, expected portfolio benefit, and thesis-break conditions
where relevant — the same evidentiary bar the PI-series Company Intelligence
reviews (PI-0012, PI-0016 forward) already hold themselves to.

**A recommendation under this layer remains advisory until accepted through
governance** (see "The essential distinction" and "Governed policy-development
flow" below). Nothing in this layer computes a numeric score, a conviction
value, or a ranking that any code path consumes automatically.

### Layer 3 — Principal decision, policy adoption, and manual execution

1. The principal reviews Layer 2's recommendation and evidence.
2. The principal accepts, rejects, narrows, or defers it.
3. The principal authorizes any governance decision the change requires (a new
   or amended entry under `governance/decisions/`, following existing precedent
   such as TGT-0001/TGT-0002 for target/tier changes).
4. The principal authorizes a bounded policy/configuration PR implementing
   exactly the accepted change.
5. Once merged, the deterministic allocator applies the newly accepted policy —
   an ordinary `targets.yaml` (or equivalent governing-source) input, computed
   through the same mechanism as every existing target.
6. The principal manually executes any resulting recommendation in Robinhood.
7. Fills and account state (share counts, margin debt/buffer) are synced back
   into `holdings.yaml` afterward.

No layer above Layer 1 ever places an order, and no step above short-circuits
step 3/4's governance and implementation requirement.

### The essential distinction (runtime control vs. policy recommendation)

- Raw Intelligence must not be imported by `allocate.py` or used at runtime to
  recalculate gaps, buys, trims, weights, tiers, targets, or margin.
- Intelligence may, and is intended to, recommend changes to the policy inputs
  the allocator later uses.
- No Intelligence recommendation becomes effective merely because it exists.
- A principal decision, and any required governance filing, must explicitly
  accept it before it has any effect.
- The accepted change is then implemented through a separate, bounded update to
  `targets.yaml` or the applicable governing source — never by the Intelligence
  record or its authoring process directly.
- The allocator remains deterministic because it consumes **accepted policy**,
  never raw advisory conclusions, opaque scores, or unaccepted recommendations.

### Governed policy-development flow

```
Evidence
  → Intelligence synthesis (Company/Theme records)
  → portfolio-level organization and comparison
  → target/tier/cluster/policy recommendation
  → principal review and required governance approval
  → governed policy update (targets.yaml or another governing source)
  → deterministic allocation (allocate.py applies accepted policy)
  → manual execution (Robinhood)
  → state reconciliation (holdings.yaml/margin sync)
```

This is a **governed policy-development loop** — periodic, human-gated, and
recorded — never a runtime Intelligence-to-allocator coupling. Nothing in this
flow lets Layer 2 output reach Layer 1 without passing through principal review,
governance acceptance, and a bounded implementation PR.

### Correlation and organizational understanding

Two distinct kinds of evidence inform Layer 2's cluster/overlap/target
recommendations, and this blueprint deliberately keeps them separate rather than
collapsing them into one opaque score:

**Economic or structural overlap** — shared exposure through demand drivers,
technology cycles, customers, suppliers, financing conditions, regulation,
geography, commodities, macroeconomic dependencies, or common portfolio function.
This is a qualitative, evidence-based judgment (the same kind already made for
the `semis`, `power_infra`, and `oil` clusters' mechanism tests in the CLAUDE.md
Decisions Log).

**Measured return correlation** — an observed security-return relationship over
a defined time window, a documented data source, a stated sampling frequency, an
explicit methodology, and known regime/sample limitations (the same kind of
evidence the semis/power_infra/oil/T1-AI-infra correlation scans already produced
and recorded).

Neither substitutes for the other, and neither alone is dispositive:

- low recent price correlation does not prove economic independence;
- high price correlation does not by itself prove identical economic roles;
- both forms of evidence may inform a governed cluster or target recommendation
  produced by Layer 2;
- **neither automatically changes policy** — both still route through "The
  essential distinction" and the governed policy-development flow above.

### What remains explicitly prohibited

A scoring engine, a computed conviction number, a theme-ranking mechanism, an
opaque aggregation of Layer 2 content into a number, or automatic/silent
adoption of any Layer 2 recommendation are all still explicitly **not**
authorized by this blueprint. What has changed from the original draft is
narrower and precise: Layer 2 output may, through principal review and
governance acceptance, become a new Layer 1 policy input (a target, tier,
cluster definition, or capital-priority weighting) — it may never become a
runtime input that `allocate.py` reads, interprets, or is silently adjusted by.
Every prior rejection of a standing analysis/scoring/opportunity-map layer in
the CLAUDE.md Decisions Log and the Constitution (§§2, 4) applies here
without exception.

## 4. Intelligence value and policy-recommendation role

Company/Theme Intelligence is the intended primary analytical and organizational
basis for recommending how target allocation is set across holdings — not merely
a passive annotation layer. Its value is assessed, and its further expansion
prioritized, on:

- contribution to thesis understanding and risk/thesis-break recognition;
- evidence freshness (the freshness/staleness reporting already built under
  PI-0011/AUTO-0001 through AUTO-0003);
- comparative business quality across capital-priority comparators (the method
  PI-0016 already generalizes);
- opportunity-cost judgment support (Layer 2 presenting the next-best eligible
  uses of capital and the business-quality/risk differences between them);
- **quality and actionability of the policy recommendations it produces** — does
  a tier/target/cluster recommendation carry the evidence, reasoning,
  alternatives, and thesis-break conditions §3 requires; and
- demonstrated improvement in the principal's actual decision quality over time.

Further Intelligence expansion (new companies, new themes, validator hardening,
or a future portfolio-level Intelligence capability that aggregates across
existing company/theme records) may still be paused, deferred, or prioritized
selectively — but only on evidence, expected decision value, workload, and
opportunity cost. **No portfolio-level Intelligence engine, computed conviction
system, or opaque scoring mechanism is designed, scoped, or authorized by this
blueprint** — only the recommendation *role* described in §3 is defined here;
building any such capability is its own future, separately authorized
implementation.

## 5. Opportunity cost

Two distinct questions must stay visibly separate:

1. **Runtime allocation under currently accepted policy** — largest-dollar-gap-
   first (`allocate.py`'s `plan()`) is the governed, deterministic, policy-driven
   mechanical capital-priority rule inside the allocation core, applied to
   whatever targets/tiers/clusters are currently accepted. It remains exactly
   that: deterministic and policy-driven, gated by trend/earnings/caps as already
   documented in CLAUDE.md. Layer 2 may not secretly nudge or override any given
   run of this computation.
2. **Periodic governed review of whether that policy should change** — Layer 2
   may evaluate whether the currently accepted targets/tiers/clusters still
   represent the best portfolio policy, and may recommend a different target,
   tier, or cluster treatment based on business quality, portfolio role,
   overlap, risk, and next-best capital use (§3's Layer 2 responsibilities and
   recommendation types). Such a recommendation is presented **as a
   recommendation**, with its own evidence and reasoning, alongside — never
   inside — any current allocator run. Once, and only once, the principal
   accepts it and it is implemented as a bounded update to `targets.yaml` or
   another governing source (§3's Layer 3 steps 3–5), it becomes a normal
   deterministic allocator input for every subsequent run.

A comparator table in a Company Intelligence review (e.g. the
PI-0016/PI-0017/PI-0019/PI-0021 methodology's 2–5-comparator capital-priority
comparison) is advisory narrative supporting question 2 above — it is never a
second allocator, and it never substitutes for, or is blended into, question 1's
Layer 1 numeric recommendation for the run currently being presented.

## 6. Terminal acceptance milestone — the end-to-end allocation check

Defines the terminal, reproducible acceptance target this architecture is meant
to serve (tracked under WS-0003; **no UX design or implementation is authorized
here or by that workstream's entry** — this is a target definition only). A
qualifying run must draw on, and make explicit:

- current holdings and available capital (cash or margin buying power, per the
  existing CLAUDE.md workflow distinction between the two);
- live prices and their explicit freshness/staleness (including the known
  regular-session-only pricing gap already logged in CLAUDE.md's Open Items);
- governed targets and tiers (`targets.yaml`, unchanged authority);
- margin debt, leverage, and maintenance constraints (the 1.8x cap, 30% buffer
  floor, and `margin_state.py`'s risk-state classification, unchanged authority);
- concentration and overlap controls (correlated-cluster caps, the T1/T2
  concentration ceiling);
- **the Layer 1 allocator recommendation under currently accepted policy** —
  presented as the executable action;
- relevant Layer 2 Intelligence/portfolio-organization context and next-best
  governed alternatives, presented alongside the recommendation, never blended
  into it;
- any separately identified candidate policy change Layer 2 has surfaced (a
  tier/target/cluster recommendation not yet accepted) — presented explicitly
  as **advisory and requiring its own separate governance approval**, never as
  part of the current run's executable output;
- explicit uncertainty and degraded-data handling (e.g. `earnings:unavailable`,
  stale margin sync, illiquid/staked crypto);
- reproducible logs (the same run, same inputs, same output);
- clear abstention when inputs are insufficient, rather than a guess presented
  as confident output;
- concise, user-facing output (bold headers, tables, zero preamble, per
  CLAUDE.md's Formatting section), **visibly distinguishing (a) actions valid
  under current accepted policy from (b) advisory policy-review recommendations
  that require separate approval**; and
- manual Robinhood execution only — this milestone does not authorize, imply, or
  move toward automated order placement.

No unapproved Intelligence recommendation may ever be presented as an executable
allocation instruction under this milestone.

This blueprint states the target; it does not design its presentation, schedule
its implementation, or authorize building it. That remains WS-0003's own future,
separately authorized scope.

## 7. Efficiency and return-contribution principles

Adopted as explicit operating principles for all future Portfolio-HQ planning and
implementation work, not just this package:

- Use the largest safe, coherent unit of work that can be fully reviewed and
  validated in one pass — avoid unnecessary prompt/session/PR fragmentation.
- Preserve separate authorization, independent review, and post-merge validation
  exactly where they materially reduce risk (as this package itself does for
  WS-0002, and as §3's Layer 3 does for every future accepted policy change) —
  not as ceremony applied uniformly regardless of stakes.
- Every material phase of work must have a credible, statable benefit to
  sustainable returns, capital protection, decision quality, reliability, or
  usability.
- Reject work whose complexity, delay, maintenance cost, or review burden
  exceeds its expected value — this is the same standard the trim/rung/weight/
  regime/trend backtests already apply to allocator rules, generalized to
  planning and architecture work itself.
- More files, more governance records, more tests, or more architecture layers
  are not, by themselves, evidence of a better outcome. Each addition is judged
  on demonstrated value, the same bar Intelligence expansion is held to in §4.

## 8. Independent audit gates

Uses model-neutral language throughout: **"independent high-capability audit,
currently intended to be performed by Fable, or another explicitly authorized
high-capability reviewer."** No specific audit prompt is included in this
document or in OPS-0002.

Three gates are recorded as material, and only these three:

1. **After this coherent architecture/roadmap package is complete** — the exact
   audit this PR requires, against this PR's exact head commit, before the
   WS-0002 planning package may be accepted or any WS-0002 implementation may
   begin. This is the gate this filing exists to establish.
2. **After material architecture implementation, before it becomes the default
   workflow** — recorded as a future checkpoint; not triggered by this filing.
3. **Before final end-to-end acceptance** (§6's milestone) — recorded as a
   future checkpoint; not triggered by this filing.

Routine edits, mechanical register updates, small bug fixes, and ordinary
test-only corrections do not require this audit — requiring it uniformly would
violate §7's own proportionality principle.

## 9. Known factual conflicts — recorded, not corrected here

Verified directly against the repository during this session:
`holdings.yaml`'s `crypto_shares:` block currently contains a live `BTC:
0.00460473` entry, while `CLAUDE.md`'s Standing Queue/Open Items and
`targets.yaml`'s `crypto:` block comment both still read as if BTC were fully
sold and absent pending a rebuild ("BTC has no entry in holdings.yaml's
crypto_shares — fully sold 2026-07-13"). This is a real, present wording/data
conflict between `holdings.yaml` (live share-tracked source of truth) and the
narrative/config comments in `CLAUDE.md`/`targets.yaml`. **This blueprint
records the conflict and does not resolve it** — per the explicit authorization
boundary of this filing, `CLAUDE.md` and `targets.yaml` are not modified here.
It requires its own separately verified factual-reconciliation change before the
next relevant allocation workflow change touches crypto-sleeve rebuild logic or
Standing Queue wording.

## 10. Explicit exclusions from this planning package

None of the following is created, proposed, authorized, or implied by this
blueprint or by OPS-0002:

- any target, tier, cluster, cap, holding, margin, allocator, Intelligence
  record, or production-code change;
- implementation of a portfolio-level Intelligence engine (an aggregation
  capability spanning multiple company/theme records into a single view or
  score);
- computed conviction of any kind;
- opaque scoring of any kind;
- automatic target mutation;
- automatic policy adoption (every policy change still requires the full §3
  Layer 3 sequence: principal review, governance approval, bounded PR);
- research execution;
- trades or orders;
- a separate branch-cleanup workstream;
- a standalone Fable workstream;
- a separate end-to-end-allocation workstream (the milestone in §6 is tracked
  under the existing WS-0003, not a new workstream);
- a standalone SHA-refresh PR;
- an Intelligence-expansion workstream without demonstrated need;
- a new scoring, ranking, or conviction system of any kind.

## 11. Relationship to WS-0001, WS-0003, WS-0004

- **WS-0001** — unaffected in substance; only priority and sequencing change
  (§2). All MARGIN-0005 governing authority, milestones, and completion
  criteria stand exactly as recorded in `operations/WORKSTREAMS.yaml`.
- **WS-0003** — gains a terminal-milestone definition (§6) inside its existing
  entry; still `status: proposed`; no UX implementation authorized.
- **WS-0004** — unaffected; remains `status: proposed`, contingent on its own
  separate future research charter, exactly as already recorded.

## 12. What this document does not authorize

Restated plainly, in case any section above is read in isolation: this document
authorizes no implementation, no allocator/`targets.yaml`/`holdings.yaml`/
`margin_state.py` change, no target/tier/cluster/capital-priority policy change,
no portfolio-level Intelligence engine, no computed conviction or opaque
scoring, no automatic target mutation or automatic policy adoption, no research
execution, no Intelligence-record expansion, no trade, and no order. Its only
effect, subject to OPS-0002 and this exact PR remaining in draft and unmerged
until the independent audit in §8(1) completes, is to serve as the proposed
WS-0002 planning baseline — including the corrected architecture in §3–§7 under
which Intelligence is the intended recommending basis for governed policy
changes, reaching the allocator only through principal review, governance
acceptance, and a separate bounded implementation.
