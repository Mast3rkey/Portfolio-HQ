---
decision_id: PI-0031
date: 2026-07-28
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, PI-0005, PI-0011, PI-0013, PI-0014, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027, PI-0028, PI-0029, PI-0030]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1-2 to execute; Milestone 3
(Intelligence completion) proceeds batch-by-batch, each requiring its own separate, later,
explicit principal authorization (`OPS-0006` §5). Eight batches are complete: `PI-0023` (ASML,
AMAT, KLAC, LRCX — semis capital equipment), `PI-0024` (MU, SKHY — memory), `PI-0025` (AVGO, AMD,
MRVL, INTC — compute/networking/foundry), `PI-0026` (ETN, VRT, PWR — power infrastructure),
`PI-0027` (MSFT, GOOGL, META, AMZN — hyperscaler AI infrastructure), `PI-0028` (V, MA, JPM —
financial infrastructure), `PI-0029` (LLY, ABBV, MRK, JNJ, GILD — biopharmaceuticals), and
`PI-0030` (IBM, NOW, CRM, ORCL, CRWD, PANW — enterprise software and cybersecurity). 38 companies
now carry a Company Intelligence record. `OPS-0008`'s Research Wave Protocol v1 governs batches
authorized from its own merge forward (`PI-0027` was the first, `PI-0028`/`PI-0029`/`PI-0030` the
second through fourth).

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin` fetched.** `git fetch origin main` returned `270b471..aa55a43 main -> origin/main`;
  `git rev-parse origin/main` confirmed `aa55a43bec154b0c7778e5cd6c8c1eaf69cfba87`, matching the
  session's verified starting `main` exactly. The session's designated branch,
  `claude/pi-0031-governance-auth-iiv2go`, was already present locally at that same commit
  (`git rev-parse HEAD` = `git rev-parse origin/main`). Working tree confirmed clean before any
  edit (`git status` — nothing to commit).
- **`aa55a43bec154b0c7778e5cd6c8c1eaf69cfba87` is PR #178's merge commit** — the register-sync
  reconciliation that recorded PR #177's (Batch 8 implementation) merge, independent reviews, and
  post-merge verification into `operations/WORKSTREAMS.yaml`. Batch 8 (IBM, NOW, CRM, ORCL, CRWD,
  PANW) is fully merged and independently post-merge verified complete as of this commit.
- **Zero open pull requests** confirmed via the GitHub API this session. **31 branches** listed,
  none named for a CVX or "batch 9" / "batch9" effort, and none overlapping this filing's scope.
- **`intelligence/companies/` independently confirmed to hold 38 files, no `CVX` record** —
  ABBV, AMAT, AMD, AMZN, ASML, AVGO, COST, CRM, CRWD, ETN, GEV, GILD, GOOGL, IBM, INTC, ISRG, JNJ,
  JPM, KLAC, LLY, LRCX, MA, META, MRK, MRVL, MSFT, MU, NOW, NVDA, ORCL, PANW, PWR, SKHY, TMO, TSM,
  V, VRT, XOM. **XOM is present; CVX is not.**
- **`targets.yaml` independently inspected**: the `oil` correlated-cluster cap (`caps.clusters`)
  lists exactly `tickers: [XOM, CVX]`, `pct: 20.0`. XOM already carries a Company Intelligence
  record; **CVX is the sole remaining uncovered member of this cluster.** CVX is a `band`-tier
  holding (0.75% target, 1.25x cap), not a member of the `semis` or `power_infra` clusters. The
  `semis` cluster (`ASML, TSM, NVDA, AVGO, AMD, MU, MRVL, KLAC, LRCX, AMAT, WDC, INTC, SKHY`) has
  exactly one uncovered member, **WDC** — confirmed independently; WDC is not a member of the
  `oil` cluster and is not touched or bundled by this filing.
- **`governance/decisions.yaml` and `governance/decisions/` independently reconciled**: 41 files
  under `governance/decisions/` (excluding `README.md`) = 41 entries in `governance/decisions.yaml`
  (parsed via `yaml.safe_load`), no orphans, highest filed `PI-0030` / highest `OPS-####` is
  `OPS-0008`. **`PI-0031` confirmed the next unused decision number** — not assumed from this
  filing's own suggested numbering.
- **`operations/WORKSTREAMS.yaml` read in full** (2636 lines). WS-0005 is the sole
  `priority: primary` entry. The `milestone-3-intelligence-completion` gate's `next_action` field
  is stale (still describes `PI-0030` as "filed, not yet merged"), superseded by its own `blocker`
  field, which correctly records Batch 8's full merge and post-merge verification
  (`intelligence_validator.py` 38/38 valid, `freshness_validator.py` clean, full pytest suite
  1502/1502, `git diff --check` clean, decision index 41 = 41, protected-path diff empty) at
  `last_verified_main_sha: 12c93234badca7231d02a9cf085a0d1099573474` (PR #177's merge commit, one
  commit behind this session's verified `aa55a43` — PR #178 itself). CRM's and IBM's two residual
  MINOR findings (debt quantification; Financing-segment elaboration) and the universal 90-day
  freshness-cadence NOTE (unbroken since Batch 1) remain recorded there as open, non-blocking, and
  untouched.
- **`CLAUDE.md`, `constitution/INVESTMENT_CONSTITUTION.md`, `OPS-0006`, `OPS-0007`, `OPS-0008`, and
  `PI-0023`-`PI-0030` read in full this session** (not relied on from memory) to confirm the
  zero-based-research-discipline protocol, the twelve-point capability-based review standard, the
  Research Wave Protocol's default wave size and its documented smaller-wave exception, the
  mandatory stop-before-drafting source-readiness gate and its standing evidence-recovery
  pre-authorization, the default two-PR lifecycle with read-only post-merge verification, and the
  `OPS-0007` §3 PROVISIONAL definition, all as they apply to this filing.
- **No repository truth conflicts with the scope directed by the principal.** CVX is confirmed the
  sole uncovered `oil`-cluster member; WDC is confirmed the sole uncovered `semis`-cluster member
  and is not part of the `oil` cluster; both facts match the principal's stated premise exactly.

The principal has directed preparation of a ninth Milestone 3 batch covering **exactly CVX, and
nothing else** — explicitly not bundled with WDC — under `OPS-0008`'s Research Wave Protocol v1,
using its §1 smaller-wave exception (no larger coherent economic-mechanism group currently
supports a 5-6-company wave for this coverage gap), together with a Milestone 3 completion
standard stated in full below. This decision records that authorization and defines that standard;
it does not itself perform any research.

### Why CVX alone, and why now

CVX is the sole remaining uncovered member of the governed `oil` correlated-cluster cap. XOM,
the cluster's other member, already carries a Company Intelligence record whose own drawdown-
history evidence partly informed the cluster cap's 20% derivation (`CLAUDE.md` Decisions Log,
"Third concentration cap added: oil"). Completing CVX closes the only remaining Intelligence gap
in an actively enforced correlated-cluster cap, directly serving `OPS-0006`'s Milestone 3 purpose
and materially improving the evidence base required for the still-unauthorized Milestone 4
(portfolio relationship mapping and correlated-loss analysis). No other currently uncovered
holding shares CVX's specific integrated-oil-and-gas economic mechanism and cluster-cap
membership — WDC's uncovered status is a `semis`-cluster gap, a wholly different mechanism and
cluster, and bundling the two would violate `OPS-0008` §1's common-economic-mechanism requirement
the same way splitting a genuinely coherent wave would violate its wave-size guidance in the other
direction. A single-company wave is smaller than `OPS-0008` §1's 5-6-company default, but §1
itself contemplates a smaller wave where no larger coherent group exists — exactly this case, and
the same "smaller than default, justified on coherence grounds" reasoning `PI-0028` already applied
to its own three-company wave.

## Decision

**PI-0031 authorizes exactly two things: (1) the ninth bounded WS-0005 Milestone 3 research batch,
covering CVX only, and (2) the Milestone 3 completion standard stated in full in §K below.** This
is **evidence development only** — no research has been performed, and this filing alone
authorizes no research finding, Company Intelligence record, comparison artifact, freshness-
registry row, policy change, tier/target/roster/cluster/cap/allocator change, margin-policy
recommendation, trade, or order. **This filing (its own governance PR) authorizes the creation of
the governance-authorization package only** — this `PI-0031` decision file, `governance/
decisions.yaml`, `operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log
entry. It does not authorize drafting `intelligence/companies/CVX.yaml` or `CVX.md`, or the
XOM/CVX comparison artifact — those become authorized to begin only after this governance decision
is independently reviewed, principal-accepted, and merged, exactly as `PI-0023`-`PI-0030`'s own
authorization-precedes-research separation already established.

**This batch adopts `OPS-0008`'s Research Wave Protocol v1 by reference** for lifecycle, review
standard, and the source-readiness gate — not restated in full here, with one explicit
application: **this is a deliberate use of `OPS-0008` §1's smaller-wave exception**, a
single-company wave rather than the protocol's 5-6-company default, because no larger coherent
economic-mechanism group currently exists for this specific coverage gap (§ "Why CVX alone,"
above). In particular: the future implementation PR must apply `OPS-0008` §2's mandatory
stop-before-drafting primary-source gate for CVX before drafting substantive economic content,
using the standing evidence-recovery pre-authorization if primary access is blocked; and the
future implementation PR is expected to follow `OPS-0008` §4's default two-PR lifecycle (this
authorization PR, then one implementation PR carrying its full review cycle), with post-merge
verification recorded per §4's read-only default rather than through a dedicated third
reconciliation PR, absent a genuine material discrepancy.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record** — `intelligence/companies/CVX.yaml` and
   `intelligence/companies/CVX.md` — using the existing repository schema frozen by
   `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated provisions, with the human approvals
   every prior first-coverage record has required (`portfolio_role_ref` — descriptive only;
   `conviction.rating` from `PI-0004`'s closed four-value vocabulary; conviction rationale; review
   cadence; thesis/risks/catalysts; source-access disclosure).
2. Create exactly **one hand-authored, bounded XOM/CVX comparison artifact**, only to the extent
   required by current Intelligence conventions (mirroring the existing `BATCH<N>_<SUBJECT>_
   COMPARISON.md` convention, e.g. `intelligence/BATCH9_OIL_CLUSTER_COMPARISON.md`), naming the
   shared integrated-oil-and-gas/commodity-price mechanism per §C below. **XOM's existing record
   must not be modified, refreshed, or reassessed by this batch under any circumstance** — it may
   be read and cited as existing comparison context only.
3. Cite required source and evidence references for CVX, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile for CVX, per §E
   below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention.
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row for CVX** (`checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0031`, `company_record_authority:
   PI-0031`).
7. Create a retained, attributable primary-source evidence artifact under `governance/audits/` if
   `OPS-0008` §2's source-readiness gate is blocked for CVX and the standing evidence-recovery
   pre-authorization is exercised.
8. `operations/WORKSTREAMS.yaml` synchronization happens in two distinct steps, neither performed
   by this filing:
   1. **Pre-merge, inside the implementation PR itself**: the implementation PR may update
      `operations/WORKSTREAMS.yaml` only to record its own actual, current state — that it is
      open/draft/in-review, which gates (source-readiness, independent review, any required
      correction, principal acceptance, merge) remain pending, and that completion and PROVISIONAL
      status under `OPS-0007` §3 are not yet reached. It must not describe itself as merged,
      complete, or PROVISIONAL before that is true.
   2. **Post-merge, read-only, per `OPS-0008` §4's default**: ancestry, byte identity, scope,
      validator/test re-run, protected-path confirmation, completion, and PROVISIONAL status are
      determined only *after* the implementation PR merges. This verification is folded into the
      Preflight/Context section of the next batch's own separately authorized governance filing, or
      into another already-authorized factual-synchronization surface if no next batch is imminent
      — per `OPS-0008` §4(a)'s exact convention. **A dedicated correction or reconciliation PR is
      opened only if that post-merge verification finds a material discrepancy.**

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (CVX)

The implementation PR's research must establish, at minimum, for CVX:

1. Economic function and current governed portfolio role (`band` tier, 0.75% target, 1.25x cap,
   `oil` correlated-cluster-cap member alongside XOM).
2. Business model and revenue economics by segment (upstream exploration/production, downstream
   refining/marketing, midstream, chemicals, where applicable).
3. Shared commodity-price exposure with XOM specifically — the same driver the `oil` cluster cap
   is built on — and how CVX's own segment mix, geographic exposure, and cost structure compare.
4. Financial quality — margins, free cash flow, balance-sheet resilience, dividend history and
   coverage, debt load, and behavior across historical commodity-price cycles.
5. Management and capital-allocation history, including dividend policy, buyback activity, and
   major acquisition/divestiture history.
6. Major growth drivers, reserve replacement, and capital-expenditure discipline.
7. Material regulatory, environmental, litigation, geopolitical, and energy-transition risks.
8. Explicit thesis-break conditions.
9. Actively searched disconfirming evidence.
10. Competitors and substitutes, including other integrated majors and alternative-energy
    substitution risk.
11. Important dependencies (major joint-venture partners, refining/midstream counterparties,
    geopolitical/regulatory jurisdictions material to production).
12. Current evidence freshness and access status.
13. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3. (`band`, 0.75% target, 1.25x cap; `oil`
    cluster-cap member.)
14. **Margin-relevance evidence, factual and advisory only** — cyclicality; commodity-price-driven
    drawdown behavior; liquidity; leverage; refinancing/funding risk; correlated-loss behavior with
    XOM specifically (the shared driver the cluster cap already assumes) — with no recommendation
    to borrow, no safe-leverage calculation, and no deployment-timing or margin-ceiling conclusion
    of any kind.
15. Evidence-driven freshness cadence and refresh triggers per §E below.
16. **External opportunities or replacements only as unauthorized future leads** — advisory
    candidate list only, no holding add, no tier/target assignment, no mechanical ranking, no batch
    expansion, no research on an outside candidate without its own separate future authorization.
17. **Why CVX may or may not deserve incremental capital compared with the alternatives**
    (capital-priority comparison, explicitly separated from business quality — same discipline
    `PI-0027` §B.23, `PI-0028` §B.17, `PI-0029` §B.17, and `PI-0030` §B.17 established): a distinct
    assessment of business quality (items 1-14 above) from a distinct assessment of capital
    priority (whether the next investment dollar is better spent on CVX than on a governed
    alternative, including XOM specifically); state explicitly why the next investment dollar
    might or might not favor CVX relative to XOM or other governed holdings; identify redundancy,
    substitutes, and duplicated exposure. **This comparison must preserve uncertainty and judgment
    in prose and must not produce a numerical score, a composite index, or an automatic ranking of
    any kind** — consistent with §G's prohibition on any ranking or composite score. It remains
    advisory research evidence only.

### C. Batch comparison requirements

The one hand-authored comparison artifact must analyze, without scoring or ranking:

1. Business-model and segment-mix comparison between XOM and CVX — upstream/downstream/midstream/
   chemicals weighting, geographic exposure, cost structure.
2. The shared commodity-price mechanism the `oil` cluster cap is built on, and whether CVX's own
   evidence confirms, refines, or complicates the cluster cap's existing 0.819 avg-pairwise-
   correlation and ~30% historical-max-drawdown derivation (`CLAUDE.md` Decisions Log) — as an
   advisory research observation only, with **no automatic effect on the cluster or cap** (any
   actual `oil` cluster/cap change requires its own separate, later, explicit governance decision).
3. Dividend policy, balance-sheet resilience, and capital-allocation-history comparison between the
   two.
4. Whether holding both XOM and CVX represents genuine diversification (distinct segment mix,
   distinct geographic/regulatory exposure) or largely duplicated commodity-price exposure.
5. Portfolio uniqueness and what exposure would be lost if either company were absent.
6. **Qualitative next-dollar (capital-priority) considerations** — same business-quality-versus-
   capital-priority separation required per §B.17, presented as advisory prose and
   uncertainty-preserving judgment only — never as a score, index, or ranking.
7. Explicit limitations preventing a mechanical capital-priority ordering — differing reporting
   periods, evidence-access gaps, and the fact that XOM's own record was authored under an earlier
   evidence standard than any later batch.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically
score or rank XOM and CVX, must not declare a preferred holding, must not alter a tier, target,
role, cluster, or cap, must not recommend a trade, must not recommend margin, and must not control
allocator output.

### D. Evidence and source protocol

1. Attempt direct inspection of SEC filings (10-K/10-Q/8-K), company investor-relations releases,
   and earnings materials for factual, non-predictive claims.
2. Preserve claim-level provenance.
3. Distinguish filed fact; issuer statement; guidance; allegation; inference; uncertainty;
   judgment.
4. Disclose inaccessible sources rather than representing snippets as inspected evidence — a
   blocked primary source must be labeled "attempted but not directly inspected" and kept separate
   from WebSearch-derived or other secondary evidence, never merged into the same citation as if
   both were equally verified.
5. **`OPS-0008` §2 applies to this batch without modification**: before drafting CVX's substantive
   economic content, the implementation PR must attempt direct primary-source inspection and
   produce a source-access manifest. **If access is blocked, the implementing session must stop
   drafting before writing substantive content** and may engage an eligible independent reviewer's
   primary-source evidence-recovery audit per `OPS-0008` §2's standing pre-authorization before
   resuming. If even that recovery pass cannot establish sufficient primary evidence, the
   implementation must try reasonable official alternatives, then stop, disclose exactly what
   failed, and return for explicit principal direction — it may not silently declare the record
   complete or substitute secondary summaries as if inspected.
6. Retain attributable evidence sufficient for independent review.
7. Preserve unresolved discrepancies and negative findings.
8. Avoid unsupported comparisons with XOM when periods, segment definitions, or reporting bases
   differ.
9. **No reliance on snippets or secondary summaries as inspected primary evidence, throughout.**

Do not perform that research in this governance session.

### E. Refresh and monitoring requirements

CVX must receive an evidence-driven refresh plan based on its own rate of business change, thesis
uncertainty, commodity-price cyclicality, and event/gap risk. **No universal cadence is imposed by
this decision, and none may be imposed automatically by the implementation.** Candidate review
triggers, drawn from `OPS-0006` §12's list as applied selectively: quarterly earnings/guidance
changes; material commodity-price regime shifts; material M&A or divestiture activity; material
debt issuance or credit-rating change; management changes; material regulatory or
energy-transition-policy developments; material geopolitical events affecting production
jurisdictions.

### F. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before
comparing them with current governed tier/role/target placement; preserve that placement as the
historical baseline for later reconciliation only (§B.13 above); never treat it as proof of a
research conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7;
and record any disagreement between researched conclusion and governed baseline without changing
policy.

### G. Hard prohibitions

This decision and any later implementation authorize none of the following, under any
interpretation:

- Any change to CVX's, WDC's, XOM's, or any other ticker's holdings, targets, tiers, roles,
  clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or
  against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Modifying any existing Company or Theme Intelligence record, **including XOM's** (the 38
  currently covered tickers plus `ai_infrastructure` and `life_sciences_tools_medtech`).
- **Bundling WDC with CVX in this or any future batch under this authorization** — WDC remains the
  `semis` cluster's sole uncovered member, a wholly separate coverage gap, untouched by this
  filing.
- Any research or Company Intelligence record for **AAPL, CEG, DHR, SYK, BRK.B, WMT, MLM, EQIX,
  UNH, or any other currently uncovered ticker** — all remain unauthorized by this decision.
- Reopening or resolving CRM's and IBM's residual MINOR findings, or the universal 90-day
  freshness-cadence NOTE — all three remain open, non-blocking, and outside this batch's scope.
- Adding a second company to Batch 9.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- **Beginning Milestone 4** (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C).
- Automatic authorization of a tenth Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 9, or this decision's Milestone 3 completion standard existing, does not authorize Batch
  10 or Milestone 4. **§K below states this explicitly.**
- Beginning, advancing, or drawing on `OPS-0007` §8 step I (the official-and-provisional Monday
  allocation-check package) in any way.
- Beginning any zero-based unlevered-portfolio redesign or margin-policy study of any kind.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.
- Any investment recommendation of any kind.

Capital-priority discussion must remain qualitative and advisory throughout. Current governed
tiers and targets remain binding until separately superseded.

### H. Lifecycle and completion conditions (Batch 9 itself)

Batch 9 is complete only when:

1. This authorization decision is accepted, merged, and effective.
2. The CVX Company Intelligence YAML/Markdown pair exists.
3. The comparison artifact exists.
4. One freshness-registry row and one freshness-checkpoint row exist for CVX.
5. Retained attributable evidence exists wherever `OPS-0008` §2's evidence-recovery method was
   exercised.
6. Validators (`intelligence_validator.py`, `freshness_validator.py`) and the full test suite pass.
7. One implementation PR is independently reviewed at exact head, per `OPS-0007` §1.
8. The principal explicitly accepts that exact head.
9. The exact reviewed head merges.
10. Independent, read-only post-merge verification confirms ancestry, byte identity, scope, tests,
    validators, and protected paths — per `OPS-0008` §4's read-only-by-default convention.
11. CVX is correctly classified under `OPS-0007` §3 (PROVISIONAL only once all of the above are
    satisfied — review and principal acceptance alone are not sufficient).
12. No material discrepancy remains.

**Merge alone is not completion.** A dedicated reconciliation PR is not authorized unless
post-merge verification identifies a material discrepancy requiring correction — per `OPS-0008`
§4's no-routine-third-PR default.

### I. Governance package scope (this filing)

This decision's own implementation — the governance PR itself, not the future research PR —
touches exactly:

1. `governance/decisions/PI-0031-ws0005-milestone3-batch9-cvx-completion-standard.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0031`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate's `next_action`, `blocker`, and
   `authorized_by` fields: record this batch's authorization and this decision's Milestone 3
   completion standard, using only `OPS-0001`'s existing schema and status vocabulary — no new
   field, no new status value; Milestone 3 remains `status: in_progress` for the milestone as a
   whole; Milestones 4-9 remain `status: proposed`, unauthorized, unchanged; also refreshes
   `last_verified_main_sha`/`last_verified_date` to this session's independently confirmed
   `origin/main` state).
4. The applicable `CLAUDE.md` Decisions Log entry recording this acceptance.

**No other file is touched by this governance filing.** No Company Intelligence record, comparison
artifact, freshness-registry or freshness-checkpoint row, and no test or validator file is created,
modified, or authorized to be created by this filing — those belong exclusively to the later,
separate implementation PR authorized in §A.

### J. Effectiveness, review, and merge gates

- **This authorization becomes effective only when this governance PR merges to `main`.** Before
  that, nothing in §A is authorized to begin.
- **The later Company Intelligence implementation must occur in its own separate, bounded PR** —
  never combined with this governance filing, and never opened before this filing merges.
- **That implementation PR must remain in draft state until it has been independently reviewed** —
  applying `OPS-0008` §2's mandatory stop-before-drafting gate first.
- **An eligible independent review must be retained and anchored to the exact implementation PR
  head** that ultimately merges, per `OPS-0007` §1's capability-based standard.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready.
- **Principal acceptance is required before merge** — explicit, at the exact head being merged.
- **Post-merge verification is required**, recorded per `OPS-0008` §4's read-only-by-default
  convention rather than through a routine dedicated reconciliation PR.
- **Completion of this batch does not authorize a tenth Milestone 3 batch or any Milestone 4
  work**, and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself is subject to the same discipline: it must remain in draft state, gain
its own eligible independent review anchored to its exact head per `OPS-0007` §1, and receive
explicit principal acceptance before it may be marked ready or merged. This decision does not mark
itself, or authorize marking itself, ready for merge.

### K. Milestone 3 completion standard

**This decision defines, but does not itself satisfy, the standard under which Milestone 3 as a
whole (not any single batch) becomes eligible for a future completion determination.** Milestone 3
reaches `status: complete` only when all seven of the following are true, verified together, not
individually inferred from any one batch's own completion:

1. **Every T1 company has a current Company Intelligence record.** (As of this filing, all ten
   T1 holdings — ASML, TSM, MSFT, GOOGL, META, NVDA, GEV, LLY, V, COST — already carry one;
   this criterion is stated as a standing requirement, not newly satisfied by this filing.)
2. **Every non-deferred T2 company has a current Company Intelligence record.** (As of this
   filing, AVGO, AMZN, PWR, ISRG, TMO, and MA are covered; **CEG, BRK.B, WMT, MLM, and AAPL remain
   uncovered with no deferral decision on record — genuine open gaps**; DHR and SYK remain
   uncovered but were considered and explicitly deferred, not rejected, per `PI-0014`; EQIX
   remains uncovered and explicitly deferred per `PI-0027`.)
3. **Every member of every active correlated-cluster cap has a current Company Intelligence
   record.** (As of this filing: `power_infra` — GEV, ETN, VRT, PWR — fully covered. `oil` — XOM
   covered, CVX authorized by this decision, not yet implemented. `semis` — twelve of thirteen
   members covered; **WDC remains the sole uncovered member, unaffected by this decision.**)
4. **Every remaining uncovered company is covered, explicitly deferred by accepted authority with
   rationale, or assigned to an approved alternative research architecture.**
5. **No unresolved MATERIAL research-coverage finding remains.** (CRM's and IBM's two residual
   findings are recorded as MINOR, not MATERIAL, and the universal 90-day freshness-cadence
   observation is recorded as a NOTE, not a finding of any severity — both are explicitly preserved
   as open and non-blocking, and this criterion does not require resolving either; it requires only
   that no *MATERIAL* finding remain outstanding at the time Milestone 3 completion is evaluated.)
6. **Coverage indexes, freshness records, and `operations/WORKSTREAMS.yaml` are synchronized.**
7. **Every completed record has passed the required independent review, merge, and post-merge
   verification lifecycle** — per `OPS-0007` §3's PROVISIONAL definition, applied per record, not
   merely per batch filing.

**Explicit statements, controlling over any contrary inference:**

- **These seven criteria do not authorize research for any ticker other than CVX.** They are a
  completion test for a future determination, not a research authorization for any company,
  cluster, or T2 gap they describe.
- **Satisfying Batch 9 (CVX) does not itself complete Milestone 3.** Criterion 2 (non-deferred T2
  coverage) and criterion 4 (every remaining company covered/deferred/reassigned) remain unmet
  regardless of Batch 9's outcome — CEG, BRK.B, WMT, MLM, and AAPL remain uncovered T2 gaps with no
  deferral rationale on record, and WDC remains an uncovered `semis`-cluster gap.
- **WDC and the remaining non-deferred T2 gaps (CEG, BRK.B, WMT, MLM, AAPL) remain open** — none is
  covered, deferred, or reassigned by this decision, and none is authorized for research by this
  decision.
- **Milestone 4 remains unauthorized until a later decision determines these completion criteria
  have been met** — this decision states the standard; it does not evaluate Milestone 3 against
  it, and does not itself trigger or schedule that evaluation.

## Rationale

**Why CVX alone, invoking `OPS-0008` §1's smaller-wave exception.** CVX is the sole remaining
uncovered member of the actively enforced `oil` correlated-cluster cap; XOM is already covered; no
other currently uncovered holding shares CVX's specific integrated-oil-and-gas/commodity-price
mechanism and cluster-cap membership in a way that would support a coherent 5-6-company wave under
`OPS-0008` §1's own common-mechanism requirement. Forcing a larger wave by adding unrelated names
(or WDC, from a wholly different cluster and mechanism) would violate the same coherence
discipline `OPS-0008` §1 exists to protect, in the opposite direction from an artificially narrow
wave.

**Why the Milestone 3 completion standard is defined now, in this filing.** Nine batches into
Milestone 3, no accepted decision has yet stated what "Milestone 3 complete" actually means as a
verifiable, cross-batch standard — each batch's own `§H`/lifecycle section defines only that
batch's own completion. Defining the standard once, referencing the concrete current-state facts
this filing's own preflight independently verified (T1 fully covered; specific named T2 gaps;
WDC as the sole `semis` gap; CVX as the sole `oil` gap; CRM/IBM's residual findings and the 90-day
NOTE at MINOR/NOTE severity, not MATERIAL), gives future sessions and future batch authors a fixed
reference point rather than requiring each to re-derive or informally assume one.

**Why `PI-0031`, not a new `OPS-####` or a reuse of `PI-0023`-`PI-0030`.** Same category and
reasoning as every prior batch: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), filed in the `PI-####` series per `governance/decisions/
README.md`'s convention. The Milestone 3 completion standard, while cross-cutting, is defined here
rather than as a separate `OPS-####` filing because it is stated as an integral qualifying
condition on Milestone 3's Intelligence-completion research program specifically, not as a change
to WS-0005's operational-coordination register mechanics.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical
reasoning to `PI-0023`-`PI-0030`: CVX has no existing Company Intelligence record, so this batch is
first-coverage record creation, not a `PI-0016` review of existing conviction.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR; `OPS-0008`
§4 restates this as the default two-PR lifecycle's first step.

## Alternatives Considered

- **Bundle WDC with CVX into one batch to close both remaining cluster-coverage gaps at once.**
  Rejected — the principal explicitly directed against this; WDC (`semis`) and CVX (`oil`) share no
  common economic mechanism, and `OPS-0008` §1's coherence requirement governs wave composition
  regardless of the operational convenience of clearing two gaps in one filing.
- **Defer CVX until a larger coherent wave can be assembled (e.g., alongside other energy-adjacent
  or industrial names).** Rejected — no currently uncovered holding shares CVX's specific
  commodity-price/cluster-cap mechanism in a way that would produce a genuinely coherent wave;
  `OPS-0008` §1 explicitly contemplates a smaller wave when no larger coherent group exists, which
  is exactly this case, rather than manufacturing artificial coherence to hit a wave-size target.
- **Omit the Milestone 3 completion standard from this filing and leave it for a dedicated future
  decision.** Rejected per the principal's explicit direction — stating the standard now, anchored
  to this filing's own independently verified current-state facts, is more useful than deferring it
  indefinitely, and doing so here does not expand this batch's own narrow CVX-only research
  authorization.
- **File under a new `OPS-####` number.** Rejected — same category reasoning as every prior
  Milestone 3 batch authorization.
- **Authorize a tenth Milestone 3 batch, begin Milestone 4, or begin `OPS-0007` §8 step I in this
  same filing.** Rejected — exceeds the principal's authorization, which names exactly CVX for
  Batch 9 only and limits this filing to the governance-authorization package plus the completion
  standard.

## Consequences

**Authorized, effective on this decision's merge:** exactly one ninth Milestone 3 research batch
(CVX only), scoped and bounded exactly as stated in §§A-J above, to proceed via its own later,
separate, bounded, draft-until-independently-reviewed implementation PR, under `OPS-0008`'s
Research Wave Protocol v1 and its §1 smaller-wave exception. **Also effective on merge:** the
Milestone 3 completion standard stated in §K, as a defined future test — not itself an evaluation
that Milestone 3 has met it.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 38 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`), **including XOM's**;
`allocate.py`, `margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every
freshness module, and every existing test; the 1.8x leverage cap and 30% buffer floor;
`MARGIN-0005`'s research charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, and `constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of
WS-0005 remain entirely unauthorized, and `OPS-0007` §8 step I is neither begun nor advanced by
this filing. **WDC, CEG, BRK.B, WMT, MLM, AAPL, DHR, SYK, EQIX, UNH, and every other currently
uncovered ticker remain uncovered and unauthorized.** CRM's and IBM's residual MINOR findings and
the universal 90-day freshness-cadence NOTE remain open, non-blocking, and untouched. No tenth
Milestone 3 batch is authorized by this filing, and none is inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** No investment
recommendation is made or implied. A future, separately implemented, draft-until-independently-
reviewed research PR may begin exactly the batch scoped above only after this decision itself
merges; any resulting Company Intelligence record, comparison artifact, freshness-registry update,
or later policy consequence remains subject to that PR's own independent review, principal
acceptance, validation, and (for anything beyond Intelligence content) its own separate future
governance decision.
