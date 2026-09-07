---
decision_id: PI-0029
date: 2026-07-27
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027, PI-0028]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1-2 to execute; Milestone 3
(Intelligence completion) proceeds batch-by-batch, each requiring its own separate, later,
explicit principal authorization (`OPS-0006` §5). Six batches are complete: `PI-0023` (ASML, AMAT,
KLAC, LRCX — semis capital equipment), `PI-0024` (MU, SKHY — memory), `PI-0025` (AVGO, AMD, MRVL,
INTC — compute/networking/foundry), `PI-0026` (ETN, VRT, PWR — power infrastructure), `PI-0027`
(MSFT, GOOGL, META, AMZN — hyperscaler AI infrastructure), and `PI-0028` (V, MA, JPM — financial
infrastructure). `OPS-0008` adopted the Research Wave Protocol v1, prospectively, for batches
authorized from its own merge forward — `PI-0027` was the first batch filed under it, `PI-0028` the
second. **No prior batch has covered any pharmaceutical or biopharmaceutical holding.**

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin` fetched.** Local branch `claude/ws0005-batch7-pharma-auth-orient` created from
  `origin/main` at `2185d80d81e011b340ffdedd4ded26fd2cc9364d` — confirmed live via `git fetch` and
  `git rev-parse origin/main` immediately before branching, not assumed from a prior report.
  Working tree confirmed clean before any edit.
- **`2185d80d81e011b340ffdedd4ded26fd2cc9364d` is PR #172's merge commit** (parents `5f08ad3f...`
  base, `d0420aa0...` reviewed head) — a narrow, two-file WS-0005 register-reconciliation PR
  (`operations/WORKSTREAMS.yaml` wording correction plus retention of
  `governance/audits/PR171_INDEPENDENT_POST_MERGE_VERIFICATION.md`), independently confirmed via
  the GitHub API this same session to carry no policy, tier, target, holdings, allocator, or margin
  change.
- **Zero open pull requests exist** in the repository at this filing's preflight — confirmed via
  the GitHub API this same session. No branch, open PR, or recently merged PR references Batch 7,
  LLY/ABBV/MRK/JNJ/GILD, "biopharmaceutical," Milestone 4, or `OPS-0007` §8 step I.
- **Batch 6 (V, MA, JPM) post-merge state, independently re-confirmed this same session** (per
  `OPS-0008` §4(a)'s read-only convention): `intelligence_validator.py` run directly against
  `intelligence/companies/` — **27 files, all valid** (exit code 0, no errors, confirmed by direct
  function call since the module exposes no CLI). `freshness_validator.py` — `OK`. Full pytest
  suite — **1502/1502 passed** (`python3 -m pytest -q`, this session's own dependency installation
  from `requirements.txt`). `git diff --check` — clean. Decision filed-versus-indexed
  reconciliation — **39 files** under `governance/decisions/` (excluding `README.md`) = **39
  entries** in `governance/decisions.yaml`, no orphans, `PI-0028` present in both. Exactly-one-
  primary-workstream check — `WS-0005` is the sole `priority: primary` entry in
  `operations/WORKSTREAMS.yaml`. Protected-path spot check — `targets.yaml`, `holdings.yaml`,
  `allocate.py`, `margin_state.py` unmodified since PR #171/#172. **All five elements of
  `OPS-0007` §3's PROVISIONAL definition remain satisfied for V, MA, and JPM** (eligible review
  `4789515179`, no correction required, principal merge, and this reconciliation's own independent
  post-merge verification, consistent with `operations/WORKSTREAMS.yaml`'s own recorded state).
- **`intelligence/companies/` independently confirmed to hold no LLY, ABBV, MRK, JNJ, or GILD
  record** (27 files: AMAT, AMD, AMZN, ASML, AVGO, COST, ETN, GEV, GOOGL, INTC, ISRG, JPM, KLAC,
  LRCX, MA, META, MRVL, MSFT, MU, NVDA, PWR, SKHY, TMO, TSM, V, VRT, XOM — none of the five named
  tickers). `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml`
  independently confirmed to carry no row for any of the five (grep against both files returned no
  match for `LLY`, `ABBV`, `MRK`, `JNJ`, or `GILD`).
- **`targets.yaml` independently inspected**: `LLY` is a **T1** ticker (3.35% target, alongside
  ASML, TSM, MSFT, GOOGL, META, NVDA, GEV, V, COST); `ABBV`, `MRK`, `JNJ`, and `GILD` are each
  **band** tickers (0.75% target, 1.25x cap, alongside KLAC, LRCX, AMAT, AMD, MU, MRVL, WDC, VRT,
  ETN, CAT, GNRC, IBM, NOW, CRM, ORCL, NFLX, SHOP, CRWD, PANW, UBER, HOOD, XOM, CVX, RTX, UNH, BABA,
  SKHY, DELL, JPM). **None of the five is a member of any `caps.clusters` correlated-cluster cap**
  (`semis`, `power_infra`, `oil`) — confirmed by direct inspection of each cluster's `tickers:`
  list in `targets.yaml`. **UNH, also a band-tier pharmaceutical/healthcare-adjacent holding, is
  explicitly not part of this batch** — the principal's authorization names exactly LLY, ABBV, MRK,
  JNJ, and GILD; UNH (a managed-care/health-insurance company, a structurally different economic
  mechanism from branded-pharmaceutical-franchise economics) remains uncovered and unauthorized.
- **`intelligence/themes/life_sciences_tools_medtech.yaml` independently inspected**: its
  membership (ISRG, TMO; SYK and DHR deferred) is medical-device and life-sciences-tools/diagnostics
  economics — explicitly *not* the same economic mechanism as branded-pharmaceutical franchise and
  pipeline economics. No overlap or duplication risk between this batch and that existing theme.
- **`OPS-0007`, `OPS-0008`, and `PI-0023`-`PI-0028` read in full this session** (not relied on from
  memory) to confirm the twelve-point review standard, the Research Wave Protocol's default wave
  size/coherence requirement, the mandatory stop-before-drafting source-readiness gate and its
  standing evidence-recovery pre-authorization, the default two-PR lifecycle, the §12 hard
  boundaries, and the PROVISIONAL definition, all as they apply to this filing.
- **`PI-0029` confirmed the next unused decision number**, checked live against both
  `governance/decisions/` (highest filed: `PI-0028`; highest `OPS-####`: `OPS-0008`) and
  `governance/decisions.yaml` (same, 39 entries, no `PI-0029` row) — not assumed from the task's
  own suggested numbering.

The principal has directed preparation of a seventh Milestone 3 batch covering **exactly LLY,
ABBV, MRK, JNJ, and GILD**, under `OPS-0008`'s Research Wave Protocol v1, with the common economic
mechanism stated as biopharmaceutical franchise and pipeline economics: patented therapeutic
franchises, clinical development, regulatory approval, commercialization, exclusivity loss,
pipeline replenishment, acquisition dependence, and capital allocation. This decision records that
authorization; it does not itself perform any research.

### Why these five companies, at the default wave size

`OPS-0008` §1 sets a default wave size of 5-6 companies, with a documented common economic
mechanism required — not merely a shared GICS sector label, tier, or historical price behavior.
LLY, ABBV, MRK, JNJ, and GILD are five of the roster's uncovered pharmaceutical/biopharmaceutical
holdings (`targets.yaml`), sharing the specific mechanism named above: revenue concentrated in
patent-protected therapeutic franchises, R&D-and-clinical-trial-dependent pipeline replenishment,
regulatory approval risk (FDA and non-U.S. equivalents), a structurally recurring
loss-of-exclusivity/patent-cliff cycle, and business-development/M&A as a standing mechanism for
franchise replacement — distinct from `life_sciences_tools_medtech`'s tools/diagnostics/device
economics and distinct from UNH's managed-care/insurance economics. The five companies span a real
range within that shared mechanism (a single-franchise-concentrated innovator in LLY; multiple
diversified large-cap innovators with differing pipeline/patent-cliff profiles in ABBV, MRK, JNJ,
and GILD's own antiviral/oncology concentration) — coherent as one economic-mechanism wave, not
five unrelated large-cap healthcare names grouped only by sector label, the same discipline
`PI-0026`'s comparison artifact applied to `power_infra` and `PI-0028`'s to "financial
infrastructure."

## Decision

**PI-0029 authorizes exactly one thing: the seventh bounded WS-0005 Milestone 3 research batch,
covering LLY, ABBV, MRK, JNJ, and GILD, and nothing else.** This is **evidence development only**
— no research has been performed, and this filing alone authorizes no research finding, Company
Intelligence record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, trade, or order.
**This filing (its own governance PR) authorizes the creation of the governance-authorization
package only** — this `PI-0029` decision file, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log entry. It does not
authorize drafting any LLY, ABBV, MRK, JNJ, or GILD Company Intelligence record or the comparison
artifact — those become authorized to begin only after this governance decision is independently
reviewed, principal-accepted, and merged, exactly as `PI-0023`-`PI-0028`'s own
authorization-precedes-research separation already established.

**This batch adopts `OPS-0008`'s Research Wave Protocol v1 by reference** for lifecycle, review
standard, and the source-readiness gate — not restated in full here. In particular: the future
implementation PR must apply `OPS-0008` §2's mandatory stop-before-drafting primary-source gate for
each of LLY, ABBV, MRK, JNJ, and GILD before drafting substantive economic content, using the
standing evidence-recovery pre-authorization if primary access is blocked; and the future
implementation PR is expected to follow `OPS-0008` §4's default two-PR lifecycle (this
authorization PR, then one implementation PR carrying its full review cycle), with post-merge
verification recorded per §4's read-only default rather than through a dedicated third
reconciliation PR, absent a genuine material discrepancy.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/
   LLY.yaml`/`.md`, `ABBV.yaml`/`.md`, `MRK.yaml`/`.md`, `JNJ.yaml`/`.md`, `GILD.yaml`/`.md` — using
   the existing repository schema frozen by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its
   incorporated provisions, with the human approvals every prior first-coverage record has required
   (`portfolio_role_ref` — descriptive only; `conviction.rating` from `PI-0004`'s closed four-value
   vocabulary; conviction rationale; review cadence; thesis/risks/catalysts; source-access
   disclosure).
2. Create exactly **one hand-authored batch comparison artifact**, at `intelligence/
   BATCH7_BIOPHARMACEUTICALS_COMPARISON.md` (mirroring the existing `BATCH<N>_<SUBJECT>_
   COMPARISON.md` convention), naming this batch's coherent theme — biopharmaceutical franchise and
   pipeline economics — per §C below.
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per §E
   below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention.
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0029`, `company_record_authority:
   PI-0029`).
7. Create a retained, attributable primary-source evidence artifact under `governance/audits/` if
   `OPS-0008` §2's source-readiness gate is blocked for one or more companies and the standing
   evidence-recovery pre-authorization is exercised.
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

### B. Required research standard (per company)

The implementation PR's research, for each of LLY, ABBV, MRK, JNJ, and GILD individually, must
establish, at minimum:

1. Economic function and current governed portfolio role.
2. Business model and revenue economics, by segment/franchise where applicable.
3. Durable moat and competitive position (patent estate, regulatory exclusivity, manufacturing
   scale, physician/payer relationships).
4. Financial quality — margins, free cash flow, balance-sheet resilience, downturn behavior.
5. Management and capital-allocation history, including dividend policy where applicable.
6. Major growth drivers and current pipeline/franchise composition.
7. Material regulatory (FDA and non-U.S. equivalents), litigation, patent-cliff/exclusivity-loss,
   pricing-policy (e.g. U.S. drug-pricing legislation and negotiation programs where applicable),
   and technology/scientific risks.
8. Explicit thesis-break conditions.
9. Actively searched disconfirming evidence.
10. Competitors and substitutes, including biosimilar/generic competition where applicable.
11. Important dependencies (key franchise/product concentration, manufacturing and supply-chain
    dependencies, licensing/partnership relationships, major customer/payer-mix concentration, as
    applicable per company).
12. Current evidence freshness and access status.
13. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3. (LLY: T1, 3.35% target. ABBV, MRK, JNJ, GILD: each
    band, 0.75% target, 1.25x cap.) None of the five is a member of any `targets.yaml`
    correlated-cluster cap.
14. **Margin-relevance evidence, factual and advisory only** — cyclicality; liquidity; leverage;
    refinancing/funding risk; drawdown and recovery characteristics (including patent-cliff-driven
    revenue-cliff risk as a distinct drawdown driver from ordinary market cyclicality);
    correlated-loss behavior — with no recommendation to borrow, no safe-leverage calculation, and
    no deployment-timing or margin-ceiling conclusion of any kind.
15. Evidence-driven freshness cadence and refresh triggers per §E below.
16. **External opportunities or replacements only as unauthorized future leads** — advisory
    candidate list only, no holding add, no tier/target assignment, no mechanical ranking, no batch
    expansion, no research on an outside candidate without its own separate future authorization.
17. **Why the company may or may not deserve incremental capital compared with the alternatives**
    (capital-priority comparison, explicitly separated from business quality — same discipline
    `PI-0027` §B.23 and `PI-0028` §B.17 established). For each of the five companies individually:
    separate an assessment of business quality (items 1-14 above) from a distinct assessment of
    capital priority (whether the next investment dollar is better spent on this company than on a
    governed alternative); compare the company against the next-best use of capital among this
    repository's other governed holdings in `targets.yaml`; state explicitly why the next
    investment dollar might or might not favor this company relative to those alternatives;
    identify redundancy, substitutes, and duplicated exposure with other governed holdings
    (including UNH, though UNH itself remains outside this batch's own research scope). **This
    comparison must preserve uncertainty and judgment in prose and must not produce a numerical
    score, a composite index, or an automatic ranking of any kind** — consistent with §G's
    prohibition on any ranking or composite score. It remains advisory research evidence only: it
    recommends no trade, and it does not itself change any tier, target, allocation, or policy.
18. **Company-specific requirement — LLY:** GLP-1/incretin (obesity and diabetes) franchise
    concentration and its share of current and projected revenue; manufacturing-capacity buildout
    and supply constraints; competitive dynamics against other incretin-class entrants; pipeline
    beyond the incretin franchise; patent/exclusivity timeline for key products.
19. **Company-specific requirement — ABBV:** post-Humira biosimilar-erosion trajectory and the
    specific replacement franchises (e.g. immunology successor products) funding that transition;
    oncology and neuroscience pipeline; acquisition-driven pipeline strategy and associated
    integration/debt considerations.
20. **Company-specific requirement — MRK:** key oncology franchise concentration (including
    patent-cliff timing for its largest product) and pipeline/business-development strategy to
    diversify beyond it; animal-health segment economics as a distinct, separately-disclosed
    business line where applicable.
21. **Company-specific requirement — JNJ:** post-consumer-health-separation segment structure
    (pharmaceutical and MedTech segments specifically); pharmaceutical pipeline and patent-cliff
    exposure across its multi-franchise portfolio; MedTech segment's overlap, if any, with
    `life_sciences_tools_medtech`'s existing membership (ISRG, TMO) — explicitly distinguishing
    JNJ's MedTech business from that theme's device/tools economics rather than assuming identity;
    litigation exposure specific to JNJ's disclosed matters.
22. **Company-specific requirement — GILD:** antiviral (HIV and viral hepatitis) franchise
    concentration and durability; oncology and cell-therapy pipeline diversification; competitive
    and pricing dynamics specific to its core franchise.

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/BATCH7_BIOPHARMACEUTICALS_COMPARISON.md`)
must analyze, without scoring or ranking:

1. Franchise-concentration profile across all five — from LLY's comparatively concentrated
   incretin-driven growth to ABBV's, MRK's, JNJ's, and GILD's differing degrees of
   multi-franchise/multi-segment diversification — directly compared.
2. Patent-cliff and loss-of-exclusivity timing across all five, and how each company's disclosed
   pipeline or business-development strategy is positioned to replace at-risk revenue.
3. Shared regulatory, pricing-policy (e.g. U.S. drug-pricing legislation/negotiation exposure where
   applicable), litigation, and biosimilar/generic-competition risk affecting the group, and where
   exposure differs materially by company or franchise.
4. Overlap and redundancy among the five — whether holding multiple large-cap biopharmaceutical
   names represents genuine diversification (distinct franchises, distinct patent-cliff timing,
   distinct pipeline bets) or materially duplicated exposure to the same macro/regulatory/pricing
   risk.
5. JNJ's distinct multi-segment (pharmaceutical plus MedTech) structure relative to the other four's
   pure-play (or near-pure-play) pharmaceutical structure, and explicit non-overlap with
   `life_sciences_tools_medtech`'s existing ISRG/TMO membership.
6. Sensitivity, across all five, to clinical-trial outcomes, regulatory-approval timing,
   drug-pricing policy, patent litigation, and biosimilar/generic entry — noting where the
   companies respond to the same macro/regulatory conditions through different franchise-specific
   transmission channels.
7. Portfolio uniqueness and what exposure would be lost if each company were absent.
8. **Qualitative next-dollar (capital-priority) considerations** — same business-quality-versus-
   capital-priority separation required per §B.17 individually, but at the batch level: whether
   LLY, ABBV, MRK, JNJ, and GILD compete for capital against each other or against other
   already-covered governed holdings; where redundancy or duplicated capital-priority reasoning
   exists among the five; and why the next investment dollar might or might not favor one of the
   five over another or over an already-covered alternative. **Presented as advisory prose and
   uncertainty-preserving judgment only — never as a score, index, or ranking.**
9. Explicit limitations preventing a mechanical capital-priority ordering — differing reporting
   periods, differing franchise/segment disclosure structures, and any evidence gaps from blocked
   primary sources.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically
score or rank the five companies, must not declare a preferred holding, must not alter a tier,
target, role, cluster, or cap, must not recommend a trade, must not recommend margin, and must not
control allocator output.

### D. Evidence and source protocol

Require primary-source-first research for changeable facts. The implementation must:

1. Attempt direct inspection of SEC filings (10-K/10-Q/8-K), company investor-relations releases,
   earnings materials, and FDA or other relevant regulatory materials where they bear on factual,
   non-predictive claims (e.g. approval dates, label changes, patent-litigation docket status).
2. Preserve claim-level provenance.
3. Distinguish filed fact; issuer statement; guidance; allegation; preliminary clinical finding;
   inference; uncertainty; judgment.
4. Disclose inaccessible sources rather than representing snippets as inspected evidence — a
   blocked primary source must be labeled "attempted but not directly inspected" and kept separate
   from WebSearch-derived or other secondary evidence, never merged into the same citation as if
   both were equally verified.
5. **`OPS-0008` §2 applies to this batch without modification**: before drafting any company's
   substantive economic content, the implementation PR must attempt direct primary-source
   inspection for each of LLY, ABBV, MRK, JNJ, and GILD and produce a source-access manifest. **If
   access is blocked for one or more companies, the implementing session must stop drafting those
   companies' records before writing substantive content** and may engage an eligible independent
   reviewer's primary-source evidence-recovery audit per `OPS-0008` §2's standing pre-authorization
   before resuming. If even that recovery pass cannot establish sufficient primary evidence for any
   one of the five, the implementation must try reasonable official alternatives, then stop,
   disclose exactly what failed, and return for explicit principal direction — it may not silently
   narrow, substitute, or declare the record complete. **The authorized batch is exactly LLY, ABBV,
   MRK, JNJ, and GILD — not any subset of them.**
6. Retain attributable evidence sufficient for independent review.
7. Preserve unresolved discrepancies and negative findings.
8. Avoid unsupported cross-company comparisons when periods, franchise definitions, or reporting
   bases differ.
9. **Clinical and scientific claims require particular care**: preliminary or early-stage clinical
   findings must be labeled as such, distinct from regulatory-approved label claims; no predictive
   claim about trial outcomes, approval likelihood, or future revenue may be presented as
   established fact.

Do not perform that research in this governance session.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business change,
thesis uncertainty, cyclicality, regulatory exposure, and event/gap risk. **No universal cadence is
imposed by this decision, and none may be imposed automatically by the implementation.** Candidate
review triggers, drawn from — but not limited to — `OPS-0006` §12's list as applied selectively:
earnings or guidance changes; FDA (or non-U.S. equivalent) approval/rejection/label decisions;
patent-litigation or exclusivity-loss developments; material clinical-trial readouts; material M&A
or licensing transactions; drug-pricing-policy or legislative developments; management changes.

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

- Any change to LLY/ABBV/MRK/JNJ/GILD's (or any other ticker's, including UNH's) holdings, targets,
  tiers, roles, clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or
  against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Modifying any existing Company or Theme Intelligence record (the 27 currently covered tickers
  plus `ai_infrastructure` and `life_sciences_tools_medtech`).
- Any research or Company Intelligence record for **EQIX** or **UNH** — EQIX remains explicitly
  deferred per `PI-0027`; UNH is not part of this batch's authorized scope; neither is authorized,
  silently or otherwise, by this decision.
- Adding a sixth company to Batch 7.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C).
- Automatic authorization of an eighth Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 7 does not authorize Batch 8 or Milestone 4.
- Beginning, advancing, or drawing on `OPS-0007` §8 step I (the official-and-provisional Monday
  allocation-check package) in any way.
- Beginning any zero-based unlevered-portfolio redesign or margin-policy study of any kind.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.

Capital-priority discussion must remain qualitative and advisory throughout. Current governed
tiers and targets remain binding until separately superseded.

### H. Lifecycle and completion conditions

Batch 7 is complete only when:

1. This authorization decision is accepted, merged, and effective.
2. All five Company Intelligence YAML/Markdown pairs (LLY, ABBV, MRK, JNJ, GILD) exist.
3. The comparison artifact (`intelligence/BATCH7_BIOPHARMACEUTICALS_COMPARISON.md`) exists.
4. One freshness-registry row and one freshness-checkpoint row exist for each of LLY, ABBV, MRK,
   JNJ, GILD.
5. Retained attributable evidence exists wherever `OPS-0008` §2's evidence-recovery method was
   exercised.
6. Validators (`intelligence_validator.py`, `freshness_validator.py`) and the full test suite pass.
7. One implementation PR is independently reviewed at exact head, per `OPS-0007` §1.
8. The principal explicitly accepts that exact head.
9. The exact reviewed head merges.
10. Independent, read-only post-merge verification confirms ancestry, byte identity, scope, tests,
    validators, and protected paths — per `OPS-0008` §4's read-only-by-default convention.
11. LLY, ABBV, MRK, JNJ, and GILD are correctly classified under `OPS-0007` §3 (PROVISIONAL only
    once all of the above are satisfied — review and principal acceptance alone are not
    sufficient).
12. No material discrepancy remains.

**Merge alone is not completion.** Another routine reconciliation PR is not authorized unless
post-merge verification identifies a material discrepancy requiring correction — per `OPS-0008`
§4's no-routine-third-PR default.

### I. Governance package scope (this filing)

This decision's own implementation — the governance PR itself, not the future research PR —
touches exactly:

1. `governance/decisions/PI-0029-ws0005-milestone3-batch7-biopharmaceuticals.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0029`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization,
   Batch 6's independently-verified post-merge/PROVISIONAL status, and minimal preflight facts,
   using only `OPS-0001`'s existing schema and status vocabulary — no new field, no new status
   value. Milestone 3 remains `status: in_progress` for the milestone as a whole; Milestones 4-9
   remain `status: proposed`, unauthorized, unchanged; `next_action` states the next step is
   exactly this governance PR's own independent review, not implementation work, not an eighth
   batch, not Milestone 4, not `OPS-0007` §8 step I).
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
- **Completion of this batch does not authorize an eighth Milestone 3 batch or any Milestone 4
  work**, and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself is subject to the same discipline: it must remain in draft state, gain
its own eligible independent review anchored to its exact head per `OPS-0007` §1, and receive
explicit principal acceptance before it may be marked ready or merged. This decision does not mark
itself, or authorize marking itself, ready for merge.

## Rationale

**Why LLY, ABBV, MRK, JNJ, and GILD, grouped as "Biopharmaceuticals."** These are five of the
roster's uncovered pharmaceutical/biopharmaceutical holdings (`targets.yaml`), sharing one specific,
well-defined economic mechanism — branded-pharmaceutical franchise concentration, clinical-pipeline
dependence, regulatory-approval risk, the patent-cliff/loss-of-exclusivity cycle, and
business-development-driven franchise replacement — distinct from the existing
`life_sciences_tools_medtech` theme's device/tools/diagnostics economics and from UNH's managed-care
economics. No prior batch has covered this mechanism at all, making it a genuine coverage gap
consistent with `OPS-0006`'s zero-based-completion purpose.

**Why five companies, at the default wave size, not a smaller wave.** `OPS-0008` §1's default of
5-6 companies applies directly here — the five named companies are not, on analysis, incoherent:
each shares the specific franchise/pipeline/patent-cliff mechanism stated above, while spanning a
real range of franchise-concentration profiles (from LLY's comparatively concentrated
incretin-driven growth to ABBV's, MRK's, JNJ's, and GILD's differing diversification), which is
exactly the kind of coherent-but-varied wave `OPS-0008` §1 favors over a forced, artificially
narrow or artificially broad grouping.

**Why `PI-0029`, not a new `OPS-####` or a reuse of `PI-0023`-`PI-0028`.** Same category and
reasoning as every prior batch: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), filed in the `PI-####` series per `governance/decisions/
README.md`'s convention.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical
reasoning to `PI-0023`-`PI-0028`: none of LLY, ABBV, MRK, JNJ, or GILD has an existing Company
Intelligence record, so this batch is first-coverage record creation, not a `PI-0016` review of
existing conviction.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR; `OPS-0008`
§4 restates this as the default two-PR lifecycle's first step.

**Why Batch 6's PROVISIONAL status and post-merge verification are recorded here rather than in a
dedicated reconciliation PR.** `OPS-0008` §4(a) explicitly directs that read-only post-merge
verification of the prior batch be folded into the next batch's own governance-authorization
preflight — exactly what this filing's Context section does — rather than filed as its own PR,
since no material discrepancy was found (this session independently re-confirmed Batch 6's
PROVISIONAL status, matching `operations/WORKSTREAMS.yaml`'s own already-recorded state).

## Alternatives Considered

- **Include UNH in this batch as a sixth "healthcare" name.** Rejected — the principal's
  authorization names exactly five companies, and UNH's managed-care/health-insurance economics is
  a structurally different mechanism (payer economics, not branded-franchise/pipeline economics)
  from the other five; including it would dilute the batch's documented coherence rather than
  strengthen it, the same concern `OPS-0008` §1 raises for forced or loosely-grouped waves.
- **Split the batch by franchise-concentration profile (e.g. LLY alone vs. the other four).**
  Rejected — five names is well within a single implementation PR's safe review surface (matching
  `PI-0027`'s own four-company and `OPS-0008`'s default 5-6-company precedent), and the comparison
  artifact's required cross-franchise, cross-patent-cliff contrast is more useful analyzed together
  than split across two governance cycles.
- **File under a new `OPS-####` number.** Rejected — same category reasoning as every prior
  Milestone 3 batch authorization.
- **Authorize an eighth Milestone 3 batch, begin Milestone 4, or begin `OPS-0007` §8 step I in this
  same filing.** Rejected — exceeds the principal's authorization, which names exactly LLY, ABBV,
  MRK, JNJ, and GILD for Batch 7 only, and which explicitly limits this filing to the
  governance-authorization package.

## Consequences

**Authorized, effective on this decision's merge:** exactly one seventh Milestone 3 research batch
(LLY, ABBV, MRK, JNJ, GILD), scoped and bounded exactly as stated in §§A-J above, to proceed via its
own later, separate, bounded, draft-until-independently-reviewed implementation PR, under
`OPS-0008`'s Research Wave Protocol v1.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 27 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`); `allocate.py`,
`margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness module,
and every existing test; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research
charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely unauthorized,
and `OPS-0007` §8 step I is neither begun nor advanced by this filing. **EQIX and UNH remain
uncovered and unauthorized.** No eighth Milestone 3 batch is authorized by this filing, and none is
inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future, separately
implemented, draft-until-independently-reviewed research PR may begin exactly the batch scoped
above only after this decision itself merges; any resulting Company Intelligence record, comparison
artifact, freshness-registry update, or later policy consequence remains subject to that PR's own
independent review, principal acceptance, validation, and (for anything beyond Intelligence
content) its own separate future governance decision.
