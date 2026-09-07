---
decision_id: PI-0030
date: 2026-07-28
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027, PI-0028, PI-0029]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1-2 to execute; Milestone 3
(Intelligence completion) proceeds batch-by-batch, each requiring its own separate, later,
explicit principal authorization (`OPS-0006` §5). Seven batches are complete: `PI-0023` (ASML,
AMAT, KLAC, LRCX — semis capital equipment), `PI-0024` (MU, SKHY — memory), `PI-0025` (AVGO, AMD,
MRVL, INTC — compute/networking/foundry), `PI-0026` (ETN, VRT, PWR — power infrastructure),
`PI-0027` (MSFT, GOOGL, META, AMZN — hyperscaler AI infrastructure), `PI-0028` (V, MA, JPM —
financial infrastructure), and `PI-0029` (LLY, ABBV, MRK, JNJ, GILD — biopharmaceuticals).
`OPS-0008` adopted the Research Wave Protocol v1, prospectively, for batches authorized from its
own merge forward — `PI-0027` was the first batch filed under it, `PI-0028` the second, `PI-0029`
the third. **No prior batch has covered any enterprise-software or cybersecurity-platform
holding.**

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin` fetched.** `git fetch origin main` returned `270b471..17ce06e main -> origin/main`;
  `git rev-parse origin/main` confirmed `17ce06e254832fa02681a7220585496cdb21d164`. The session's
  designated branch, `claude/ws-0005-m3-batch-8-to4tz7`, was already created and based exactly at
  that commit (`git merge-base HEAD origin/main` returns the same SHA). Working tree confirmed
  clean before any edit.
- **`17ce06e254832fa02681a7220585496cdb21d164` is PR #174's merge commit** — confirmed via the
  GitHub API this same session (`state: closed`, `merged: true`,
  `merged_at: 2026-07-28T04:03:03Z`, `head.sha: 2010a9e6b538745ee5e85f5beadd3d440654e956`,
  `base.sha: 3848ea695757be4ab324ea25c8aea28288d3691c`, 14 files changed, +2019/-3). PR #174
  implemented Milestone 3 Batch 7 (LLY, ABBV, MRK, JNJ, GILD): final independent exact-head review
  `4793548140` (`APPROVE WITH MINOR NOTES`, F1/F2 closed, three non-blocking NOTE findings only),
  explicit principal acceptance at that exact head, then merge.
- **PR #175 ("WS-0005: reconcile Batch 7 post-merge state") independently confirmed `state: closed`,
  `merged: false`** via the GitHub API this same session — it was opened as a draft to correct four
  stale `operations/WORKSTREAMS.yaml` fields left behind by PR #174's own in-PR sync
  (`active_branch`/`active_pr` pointing at the now-merged PR #174 instead of `null`;
  `last_verified_main_sha`/`last_verified_date` still anchored to PR #173's merge commit instead
  of PR #174's), plus narrative/gate-description updates, but never merged. Per the principal's
  explicit instruction accompanying this batch's authorization, this filing does not merge or
  reuse PR #175's closed branch wholesale — it independently re-derives the WORKSTREAMS delta
  directly from current `main`, described in full below and in §I.
- **Independent re-derivation of the Batch 7 post-merge facts (this session, not copied from PR
  #175's body):** `operations/WORKSTREAMS.yaml`'s `milestone-3-intelligence-completion` gate
  currently carries `active_branch: claude/ws0005-batch7-biopharmaceuticals-impl`,
  `active_pr: 174`, `last_verified_main_sha: 3848ea695757be4ab324ea25c8aea28288d3691c`,
  `last_verified_date: "2026-07-27"` — all four stale against the now-merged, now-closed state
  confirmed above. `intelligence_validator.py` run directly against `intelligence/companies/`
  this session: **32 files, all valid** (ABBV, AMAT, AMD, AMZN, ASML, AVGO, COST, ETN, GEV, GILD,
  GOOGL, INTC, ISRG, JNJ, JPM, KLAC, LLY, LRCX, MA, META, MRK, MRVL, MSFT, MU, NVDA, PWR, SKHY,
  TMO, TSM, V, VRT, XOM — LLY/ABBV/MRK/JNJ/GILD present, confirming Batch 7 landed).
  `validate_themes_directory`: **2/2 valid** (`ai_infrastructure`, `life_sciences_tools_medtech`,
  neither touched by Batch 7). `freshness_validator.py`'s
  `validate_registry_and_checkpoints_files`: **valid, zero errors**. Full pytest suite, this
  session's own `requirements.txt` install: **1502/1502 passed**. `git diff --check`: clean.
  Decision filed-versus-indexed reconciliation: **40 files** under `governance/decisions/`
  (excluding `README.md`) = **40 entries** in `governance/decisions.yaml`, no orphans, `PI-0029`
  present in both. Exactly-one-primary-workstream check: `WS-0005` is the sole
  `priority: primary` entry in `operations/WORKSTREAMS.yaml`. Protected-path spot check:
  `targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py` unmodified since PR #172. **All
  five elements of `OPS-0007` §3's PROVISIONAL definition are satisfied for LLY, ABBV, MRK, JNJ,
  and GILD** (eligible review `4793548140` with F1/F2 independently closed, explicit principal
  acceptance at the exact corrected head, merge, and this session's own independent post-merge
  ancestry/scope/validator/test re-verification, all recorded above). This filing's own
  governance package (§I) corrects the four stale fields and records this reconciliation — the
  smallest accurate delta, not a restatement of PR #175's full narrative.
- **`intelligence/companies/` independently confirmed to hold no IBM, NOW, CRM, ORCL, CRWD, or PANW
  record** (the 32 files enumerated above — none of the six named tickers).
  `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml`
  independently confirmed to carry no row for any of the six (grepped both files for `IBM`, `NOW`,
  `CRM`, `ORCL`, `CRWD`, `PANW` — no match; note `NOW` and `CRM` are grep-checked against the
  ticker-column context specifically, to avoid false positives on the common English words).
- **`targets.yaml` independently inspected**: IBM, NOW, CRM, ORCL, CRWD, and PANW are each a
  **band** ticker (0.75% target, 1.25x cap), alongside KLAC, LRCX, AMAT, AMD, MU, MRVL, WDC, VRT,
  ETN, CAT, GNRC, NFLX, SHOP, UBER, JPM, HOOD, XOM, CVX, RTX, UNH, BABA, SKHY, DELL. **None of the
  six is a member of any `caps.clusters` correlated-cluster cap** (`semis`, `power_infra`, `oil`)
  — confirmed by direct inspection of each cluster's `tickers:` list in `targets.yaml`.
- **`OPS-0007`, `OPS-0008`, and `PI-0023`-`PI-0029` read in full this session** (not relied on from
  memory) to confirm the twelve-point review standard, the Research Wave Protocol's default wave
  size/coherence requirement, the mandatory stop-before-drafting source-readiness gate and its
  standing evidence-recovery pre-authorization, the default two-PR lifecycle with read-only
  post-merge verification, the §12 hard boundaries, and the PROVISIONAL definition, all as they
  apply to this filing.
- **`PI-0030` confirmed the next unused decision number**, checked live against both
  `governance/decisions/` (highest filed: `PI-0029`; highest `OPS-####`: `OPS-0008`) and
  `governance/decisions.yaml` (same, 40 entries, no `PI-0030` row) — not assumed from the task's
  own suggested numbering.

The principal has directed preparation of an eighth Milestone 3 batch covering **exactly IBM,
NOW, CRM, ORCL, CRWD, and PANW**, under `OPS-0008`'s Research Wave Protocol v1, with the common
economic mechanism stated as enterprise software and cybersecurity platform economics: recurring
subscription/support revenue, switching costs, embedded enterprise workflows, cloud and
hybrid-cloud delivery, platform consolidation, AI monetization and infrastructure cost, enterprise
IT/security budgets, renewal durability, sales efficiency, acquisition integration, competitive
bundling, and cyber/data/regulatory risk. This decision records that authorization; it does not
itself perform any research. The principal's authorization also directs this governance PR to
incorporate the Batch 7 post-merge factual synchronization described above, independently
re-derived rather than reused from PR #175's closed branch — addressed in full in §I.

### Why these six companies, at the top of the default wave-size range

`OPS-0008` §1 sets a default wave size of 5-6 companies, with a documented common economic
mechanism required — not merely a shared GICS sector label, tier, or historical price behavior.
IBM, NOW, CRM, ORCL, CRWD, and PANW are six of the roster's uncovered enterprise-software and
cybersecurity holdings (`targets.yaml`), sharing the specific mechanism named above: revenue
concentrated in recurring subscription, support, or consumption contracts sold into enterprise IT
and security budgets; competitive position built on embedded workflows and switching costs rather
than commodity pricing; a common transition arc toward cloud/hybrid-cloud delivery and
platform-consolidation strategies; and AI-feature monetization layered onto existing platforms as
a current, live strategic question for all six. The six companies span a real range within that
shared mechanism — a century-old diversified infrastructure/consulting/hybrid-cloud incumbent in
IBM; three enterprise-application/workflow-platform vendors with materially different growth and
margin profiles (NOW's still-fast-growing single-platform model, CRM's larger and more
acquisition-assembled CRM/data/AI stack, ORCL's database-to-cloud-infrastructure transition
carrying a distinct, much larger balance-sheet/capex profile); and two pure-play cybersecurity
platform vendors (CRWD, PANW) with a shared "platformization" strategy but different incident
histories, product architectures, and competitive postures — coherent as one economic-mechanism
wave, not six unrelated large-cap technology names grouped only by sector label, the same
discipline `PI-0026`'s comparison artifact applied to `power_infra` and `PI-0028`'s to "financial
infrastructure."

## Decision

**PI-0030 authorizes exactly one thing: the eighth bounded WS-0005 Milestone 3 research batch,
covering IBM, NOW, CRM, ORCL, CRWD, and PANW, and nothing else.** This is **evidence development
only** — no research has been performed, and this filing alone authorizes no research finding,
Company Intelligence record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, trade, or order.
**This filing (its own governance PR) authorizes the creation of the governance-authorization
package only** — this `PI-0030` decision file, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml` (including the Batch 7 post-merge reconciliation described in
Context and §I), and the applicable `CLAUDE.md` Decisions Log entry. It does not authorize
drafting any IBM, NOW, CRM, ORCL, CRWD, or PANW Company Intelligence record or the comparison
artifact — those become authorized to begin only after this governance decision is independently
reviewed, principal-accepted, and merged, exactly as `PI-0023`-`PI-0029`'s own
authorization-precedes-research separation already established.

**This batch adopts `OPS-0008`'s Research Wave Protocol v1 by reference** for lifecycle, review
standard, and the source-readiness gate — not restated in full here. In particular: the future
implementation PR must apply `OPS-0008` §2's mandatory stop-before-drafting primary-source gate
for each of IBM, NOW, CRM, ORCL, CRWD, and PANW before drafting substantive economic content,
using the standing evidence-recovery pre-authorization if primary access is blocked; and the
future implementation PR is expected to follow `OPS-0008` §4's default two-PR lifecycle (this
authorization PR, then one implementation PR carrying its full review cycle), with post-merge
verification recorded per §4's read-only default rather than through a dedicated third
reconciliation PR, absent a genuine material discrepancy.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/
   IBM.yaml`/`.md`, `NOW.yaml`/`.md`, `CRM.yaml`/`.md`, `ORCL.yaml`/`.md`, `CRWD.yaml`/`.md`,
   `PANW.yaml`/`.md` — using the existing repository schema frozen by
   `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated provisions, with the human approvals
   every prior first-coverage record has required (`portfolio_role_ref` — descriptive only;
   `conviction.rating` from `PI-0004`'s closed four-value vocabulary; conviction rationale; review
   cadence; thesis/risks/catalysts; source-access disclosure).
2. Create exactly **one hand-authored batch comparison artifact**, at `intelligence/
   BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md` (mirroring the existing
   `BATCH<N>_<SUBJECT>_COMPARISON.md` convention), naming this batch's coherent theme — enterprise
   software and cybersecurity platform economics — per §C below.
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per §E
   below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention.
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0030`, `company_record_authority:
   PI-0030`).
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
      — per `OPS-0008` §4(a)'s exact convention, the same convention this filing itself applies to
      Batch 7's own post-merge state in §I. **A dedicated correction or reconciliation PR is opened
      only if that post-merge verification finds a material discrepancy** — the exact outcome this
      filing avoids repeating by not reopening or reusing PR #175.

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (per company)

The implementation PR's research, for each of IBM, NOW, CRM, ORCL, CRWD, and PANW individually,
must establish, at minimum:

1. Economic function and current governed portfolio role.
2. Business model and revenue economics, by segment where applicable (e.g. subscription vs.
   consulting/services vs. hardware/infrastructure vs. licensing).
3. Durable moat and competitive position (switching costs, platform embedding, ecosystem
   lock-in, brand/channel relationships, technology differentiation).
4. Financial quality — margins, free cash flow, balance-sheet resilience, downturn behavior,
   debt load where material.
5. Management and capital-allocation history, including dividend policy and acquisition strategy
   where applicable.
6. Major growth drivers and current product/platform roadmap, including AI-feature monetization
   strategy specifically.
7. Material regulatory, litigation, competitive, cybersecurity/data-incident, and
   technology-obsolescence risks.
8. Explicit thesis-break conditions.
9. Actively searched disconfirming evidence.
10. Competitors and substitutes, including open-source or in-house-build alternatives where
    applicable.
11. Important dependencies (major customer/partner concentration, cloud-hyperscaler
    infrastructure dependencies, channel-partner relationships, key-personnel dependence,
    acquisition-integration dependence, as applicable per company).
12. Current evidence freshness and access status.
13. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3. (All six: band, 0.75% target, 1.25x cap.) None of
    the six is a member of any `targets.yaml` correlated-cluster cap.
14. **Margin-relevance evidence, factual and advisory only** — cyclicality; liquidity; leverage;
    refinancing/funding risk; drawdown and recovery characteristics; correlated-loss behavior
    (including shared exposure to enterprise-IT/security-budget cycles and cybersecurity-incident
    tail risk as distinct drawdown drivers) — with no recommendation to borrow, no safe-leverage
    calculation, and no deployment-timing or margin-ceiling conclusion of any kind.
15. Evidence-driven freshness cadence and refresh triggers per §E below.
16. **External opportunities or replacements only as unauthorized future leads** — advisory
    candidate list only, no holding add, no tier/target assignment, no mechanical ranking, no
    batch expansion, no research on an outside candidate without its own separate future
    authorization.
17. **Why the company may or may not deserve incremental capital compared with the alternatives**
    (capital-priority comparison, explicitly separated from business quality — same discipline
    `PI-0027` §B.23, `PI-0028` §B.17, and `PI-0029` §B.17 established). For each of the six
    companies individually: separate an assessment of business quality (items 1-14 above) from a
    distinct assessment of capital priority (whether the next investment dollar is better spent on
    this company than on a governed alternative); compare the company against the next-best use of
    capital among this repository's other governed holdings in `targets.yaml`; state explicitly
    why the next investment dollar might or might not favor this company relative to those
    alternatives; identify redundancy, substitutes, and duplicated exposure with other governed
    holdings (including any already-covered enterprise-technology or cybersecurity-adjacent
    names). **This comparison must preserve uncertainty and judgment in prose and must not produce
    a numerical score, a composite index, or an automatic ranking of any kind** — consistent with
    §G's prohibition on any ranking or composite score. It remains advisory research evidence
    only: it recommends no trade, and it does not itself change any tier, target, allocation, or
    policy.
18. **Company-specific requirement — IBM:** hybrid-cloud and Red Hat integration economics;
    consulting-services segment mix and its distinct margin profile relative to software; mainframe
    (zSystems) franchise durability and renewal economics; watsonx/AI monetization strategy and its
    evidenced traction; multi-decade turnaround/transformation context distinguished from
    speculative narrative.
19. **Company-specific requirement — NOW (ServiceNow):** workflow-automation platform breadth
    (IT service management core plus adjacent modules), subscription renewal-rate and net-revenue-
    retention economics, AI (Now Assist / agentic AI) monetization strategy and disclosed adoption,
    and customer/seat-expansion concentration risk.
20. **Company-specific requirement — CRM (Salesforce):** CRM/Data Cloud/Agentforce platform
    economics, the acquisition-assembled nature of its current product stack (e.g. Slack, Tableau,
    MuleSoft) and associated integration risk, margin-expansion and capital-return (buyback/
    dividend) trajectory, and competitive exposure to point-solution and AI-native entrants.
21. **Company-specific requirement — ORCL:** the database-licensing-to-cloud-infrastructure (OCI)
    transition specifically, including capital intensity and debt load associated with AI/cloud
    data-center buildout, enterprise-applications (Fusion, NetSuite) segment economics distinct
    from infrastructure, and customer-concentration/backlog disclosure quality for large cloud
    contracts.
22. **Company-specific requirement — CRWD (CrowdStrike):** Falcon cloud-native endpoint/XDR
    platform economics and subscription ARR growth, the July 2024 global outage incident's
    disclosed financial, contractual, and reputational impact and remediation, competitive dynamics
    against platform and point-solution rivals, and customer-concentration/renewal-rate evidence.
23. **Company-specific requirement — PANW (Palo Alto Networks):** the network-security-to-cloud/
    SASE/XSIAM "platformization" strategy specifically, acquisition-driven product-line expansion
    and associated integration risk, competitive dynamics against CRWD and other security vendors
    (explicitly cross-referenced in the comparison artifact, not merely each company's own record),
    and billings/ARR-based growth-quality evidence distinct from GAAP revenue alone.

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/
BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md`) must analyze, without scoring or ranking:

1. Business-model profile across all six — from IBM's diversified infrastructure/consulting/
   hybrid-cloud mix, to NOW's and CRM's workflow/CRM-platform subscription models, to ORCL's
   database-to-cloud-infrastructure transition, to CRWD's and PANW's cybersecurity-platform
   models — directly compared.
2. Recurring-revenue quality and renewal/retention economics across all six, and how each
   company's disclosed metrics (subscription/ARR/billings, renewal rates, net-revenue-retention
   where disclosed) compare.
3. Shared and distinct AI-monetization strategies across the group — including capital-intensity
   differences (e.g. ORCL's cloud/AI infrastructure capex and debt load versus the others'
   comparatively asset-light software models) — and where the "AI upside" narrative is supported by
   disclosed evidence versus still speculative.
4. Direct competitive overlap between CRWD and PANW specifically (both cybersecurity-platform
   vendors pursuing platform-consolidation strategies), and whether holding both represents
   genuine diversification (distinct product architecture, distinct incident histories, distinct
   customer bases) or materially duplicated cybersecurity-platform exposure.
5. Overlap and redundancy among all six more broadly — whether holding multiple large-cap
   enterprise-software/cybersecurity names represents genuine diversification across the
   value chain (infrastructure vs. applications vs. security) or duplicated exposure to the same
   enterprise-IT-budget cycle.
6. Sensitivity, across all six, to enterprise IT/security budget cycles, macro/interest-rate
   conditions affecting enterprise capital spending, competitive/technology disruption (including
   AI-native entrants), and — for CRWD/PANW specifically — cybersecurity-incident and reputational
   tail risk.
7. Portfolio uniqueness and what exposure would be lost if each company were absent.
8. **Qualitative next-dollar (capital-priority) considerations** — same business-quality-versus-
   capital-priority separation required per §B.17 individually, but at the batch level: whether
   IBM, NOW, CRM, ORCL, CRWD, and PANW compete for capital against each other or against other
   already-covered governed holdings; where redundancy or duplicated capital-priority reasoning
   exists among the six (particularly CRWD versus PANW); and why the next investment dollar might
   or might not favor one of the six over another or over an already-covered alternative.
   **Presented as advisory prose and uncertainty-preserving judgment only — never as a score,
   index, or ranking.**
9. Explicit limitations preventing a mechanical capital-priority ordering — differing reporting
   periods, differing segment-disclosure structures, differing business-model maturity (e.g.
   IBM's century-long history versus CRWD's and PANW's comparatively young public histories), and
   any evidence gaps from blocked primary sources.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically
score or rank the six companies, must not declare a preferred holding, must not alter a tier,
target, role, cluster, or cap, must not recommend a trade, must not recommend margin, and must not
control allocator output.

### D. Evidence and source protocol

Require primary-source-first research for changeable facts. The implementation must:

1. Attempt direct inspection of SEC filings (10-K/10-Q/8-K), company investor-relations releases,
   earnings materials, and relevant regulatory/incident-disclosure materials where they bear on
   factual, non-predictive claims (e.g. renewal-rate figures, the CRWD outage's disclosed
   financial impact, debt issuances).
2. Preserve claim-level provenance.
3. Distinguish filed fact; issuer statement; guidance; allegation; inference; uncertainty;
   judgment.
4. Disclose inaccessible sources rather than representing snippets as inspected evidence — a
   blocked primary source must be labeled "attempted but not directly inspected" and kept separate
   from WebSearch-derived or other secondary evidence, never merged into the same citation as if
   both were equally verified.
5. **`OPS-0008` §2 applies to this batch without modification**: before drafting any company's
   substantive economic content, the implementation PR must attempt direct primary-source
   inspection for each of IBM, NOW, CRM, ORCL, CRWD, and PANW and produce a source-access
   manifest. **If access is blocked for one or more companies, the implementing session must stop
   drafting those companies' records before writing substantive content** and may engage an
   eligible independent reviewer's primary-source evidence-recovery audit per `OPS-0008` §2's
   standing pre-authorization before resuming. If even that recovery pass cannot establish
   sufficient primary evidence for any one of the six, the implementation must try reasonable
   official alternatives, then stop, disclose exactly what failed, and return for explicit
   principal direction — it may not silently narrow, substitute, or declare the record complete.
   **The authorized batch is exactly IBM, NOW, CRM, ORCL, CRWD, and PANW — not any subset of
   them.**
6. Retain attributable evidence sufficient for independent review.
7. Preserve unresolved discrepancies and negative findings.
8. Avoid unsupported cross-company comparisons when periods, segment definitions, or reporting
   bases differ.
9. **The CRWD outage and any comparable disclosed incident require particular care**: distinguish
   company-disclosed financial/contractual impact from third-party estimates or allegations; no
   predictive claim about future incident risk, litigation outcomes, or reputational trajectory may
   be presented as established fact.

Do not perform that research in this governance session.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business
change, thesis uncertainty, cyclicality, competitive/technology-disruption exposure, and
event/gap risk. **No universal cadence is imposed by this decision, and none may be imposed
automatically by the implementation.** Candidate review triggers, drawn from — but not limited to
— `OPS-0006` §12's list as applied selectively: quarterly earnings/guidance changes; material
product launches or AI-monetization disclosures; material M&A or divestiture activity; material
cybersecurity incidents or data breaches (for CRWD and PANW specifically, and for any of the six
as a customer/operator); material debt issuance or credit-rating change (ORCL specifically);
management changes; material competitive or regulatory developments.

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

- Any change to IBM/NOW/CRM/ORCL/CRWD/PANW's (or any other ticker's) holdings, targets, tiers,
  roles, clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or
  against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Modifying any existing Company or Theme Intelligence record (the 32 currently covered tickers
  plus `ai_infrastructure` and `life_sciences_tools_medtech`).
- Any research or Company Intelligence record for **EQIX** or **UNH** — both remain explicitly
  deferred/excluded per `PI-0027`/`PI-0029`, and neither is authorized, silently or otherwise, by
  this decision.
- Adding a seventh company to Batch 8.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C).
- Automatic authorization of a ninth Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 8 does not authorize Batch 9 or Milestone 4.
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

Batch 8 is complete only when:

1. This authorization decision is accepted, merged, and effective.
2. All six Company Intelligence YAML/Markdown pairs (IBM, NOW, CRM, ORCL, CRWD, PANW) exist.
3. The comparison artifact
   (`intelligence/BATCH8_ENTERPRISE_SOFTWARE_CYBERSECURITY_COMPARISON.md`) exists.
4. One freshness-registry row and one freshness-checkpoint row exist for each of IBM, NOW, CRM,
   ORCL, CRWD, PANW.
5. Retained attributable evidence exists wherever `OPS-0008` §2's evidence-recovery method was
   exercised.
6. Validators (`intelligence_validator.py`, `freshness_validator.py`) and the full test suite pass.
7. One implementation PR is independently reviewed at exact head, per `OPS-0007` §1.
8. The principal explicitly accepts that exact head.
9. The exact reviewed head merges.
10. Independent, read-only post-merge verification confirms ancestry, byte identity, scope, tests,
    validators, and protected paths — per `OPS-0008` §4's read-only-by-default convention.
11. IBM, NOW, CRM, ORCL, CRWD, and PANW are correctly classified under `OPS-0007` §3 (PROVISIONAL
    only once all of the above are satisfied — review and principal acceptance alone are not
    sufficient).
12. No material discrepancy remains.

**Merge alone is not completion.** Another routine reconciliation PR is not authorized unless
post-merge verification identifies a material discrepancy requiring correction — per `OPS-0008`
§4's no-routine-third-PR default, the exact discipline this filing itself applies to Batch 7 by
not reopening or merging PR #175.

### I. Governance package scope (this filing)

This decision's own implementation — the governance PR itself, not the future research PR —
touches exactly:

1. `governance/decisions/PI-0030-ws0005-milestone3-batch8-enterprise-software-cybersecurity.md`
   (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0030`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization,
   using only `OPS-0001`'s existing schema and status vocabulary — no new field, no new status
   value; Milestone 3 remains `status: in_progress` for the milestone as a whole; Milestones 4-9
   remain `status: proposed`, unauthorized, unchanged; `next_action` states the next step is
   exactly this governance PR's own independent review, not implementation work, not a ninth
   batch, not Milestone 4, not `OPS-0007` §8 step I). **This filing also performs the Batch 7
   post-merge factual synchronization** left incomplete by PR #175's unmerged closure — per the
   principal's explicit instruction and `OPS-0008` §4(a)'s convention that read-only post-merge
   verification of the prior batch be folded into the next batch's own governance-authorization
   filing rather than a dedicated reconciliation PR. This filing corrects exactly the four stale
   fields identified in Context (`active_branch` → `null`; `active_pr` → `null`;
   `last_verified_main_sha` → `17ce06e254832fa02681a7220585496cdb21d164`; `last_verified_date` →
   `"2026-07-28"`) and records, concisely, the independently re-verified Batch 7 completion facts
   (PR #174 merged, reviewed, principal-accepted; PR #175 closed unmerged and not reused) — the
   smallest accurate delta, not a re-derivation of PR #175's full narrative body.
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
- **Completion of this batch does not authorize a ninth Milestone 3 batch or any Milestone 4
  work**, and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself is subject to the same discipline: it must remain in draft state, gain
its own eligible independent review anchored to its exact head per `OPS-0007` §1, and receive
explicit principal acceptance before it may be marked ready or merged. This decision does not mark
itself, or authorize marking itself, ready for merge.

## Rationale

**Why IBM, NOW, CRM, ORCL, CRWD, and PANW, grouped as "Enterprise Software and Cybersecurity."**
These are six of the roster's uncovered enterprise-software and cybersecurity holdings
(`targets.yaml`), sharing one specific, well-defined economic mechanism — recurring
subscription/support revenue sold into enterprise IT and security budgets, competitive moats built
on switching costs and workflow embedding, a shared strategic pivot toward AI-feature
monetization, and (for the software names) a common cloud/hybrid-cloud delivery transition — while
spanning a real range of business-model maturity and capital intensity, from IBM's diversified
century-old infrastructure/consulting mix to ORCL's capital-intensive cloud-infrastructure buildout
to CRWD's/PANW's asset-light cybersecurity-platform models. No prior batch has covered this
mechanism at all, making it a genuine coverage gap consistent with `OPS-0006`'s zero-based-
completion purpose.

**Why six companies, at the top of the default wave-size range, not a smaller wave.** `OPS-0008`
§1's default of 5-6 companies applies directly here — the six named companies are not, on
analysis, incoherent: each shares the specific recurring-revenue/enterprise-budget/AI-monetization
mechanism stated above, while spanning a genuine range (infrastructure/consulting vs.
application-platform vs. cybersecurity-platform), which is exactly the kind of coherent-but-varied
wave `OPS-0008` §1 favors over a forced, artificially narrow or artificially broad grouping. CRWD
and PANW's direct competitive overlap is handled explicitly as a required comparison point (§C.4),
not treated as grounds to split the wave.

**Why `PI-0030`, not a new `OPS-####` or a reuse of `PI-0023`-`PI-0029`.** Same category and
reasoning as every prior batch: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), filed in the `PI-####` series per `governance/decisions/
README.md`'s convention.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical
reasoning to `PI-0023`-`PI-0029`: none of IBM, NOW, CRM, ORCL, CRWD, or PANW has an existing
Company Intelligence record, so this batch is first-coverage record creation, not a `PI-0016`
review of existing conviction.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR; `OPS-0008`
§4 restates this as the default two-PR lifecycle's first step.

**Why the Batch 7 post-merge reconciliation is folded into this filing rather than a dedicated
PR.** `OPS-0008` §4(a) explicitly directs that read-only post-merge verification of the prior
batch be folded into the next batch's own governance-authorization preflight — exactly what this
filing's Context section and §I do — rather than filed as its own PR. PR #175 attempted the
dedicated-PR path and was closed unmerged; per the principal's explicit instruction, this filing
does not reopen or reuse that closed branch, but instead independently re-derives the same small,
accurate delta directly from current `main`, which this session's own preflight confirms matches
PR #175's intended corrections exactly (same four fields, same target values) without depending on
or inheriting anything from the unmerged branch itself.

## Alternatives Considered

- **Split the batch: software (IBM, NOW, CRM, ORCL) in one wave, cybersecurity (CRWD, PANW) in
  another.** Rejected — both sub-groups share the same enterprise-IT-budget/subscription/
  AI-monetization mechanism, and `OPS-0008` §1's default wave size (5-6) comfortably accommodates
  six coherent names; splitting would create two smaller-than-minimum-coherence waves for no
  documented benefit, and would separate CRWD/PANW from the required direct-competitive-overlap
  comparison that is more useful analyzed within the same wave as the software names' shared
  enterprise-budget-cycle exposure.
- **Reopen or merge PR #175 to close out Batch 7 separately from this authorization.** Rejected —
  the principal's explicit instruction directs against reusing PR #175's closed branch wholesale;
  `OPS-0008` §4(a)'s own convention already favors folding read-only post-merge verification into
  the next batch's governance filing over a dedicated reconciliation PR, which is what this filing
  does instead.
- **File under a new `OPS-####` number.** Rejected — same category reasoning as every prior
  Milestone 3 batch authorization.
- **Authorize a ninth Milestone 3 batch, begin Milestone 4, or begin `OPS-0007` §8 step I in this
  same filing.** Rejected — exceeds the principal's authorization, which names exactly IBM, NOW,
  CRM, ORCL, CRWD, and PANW for Batch 8 only, and which explicitly limits this filing to the
  governance-authorization package (plus the Batch 7 factual synchronization the principal
  separately directed).

## Consequences

**Authorized, effective on this decision's merge:** exactly one eighth Milestone 3 research batch
(IBM, NOW, CRM, ORCL, CRWD, PANW), scoped and bounded exactly as stated in §§A-J above, to proceed
via its own later, separate, bounded, draft-until-independently-reviewed implementation PR, under
`OPS-0008`'s Research Wave Protocol v1. **Also effective on merge:** the corrected, accurate
`operations/WORKSTREAMS.yaml` state for Batch 7 described in Context and §I (four stale fields
corrected; PR #174's merge and PR #175's unmerged closure both accurately recorded).

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 32 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`); `allocate.py`,
`margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness module,
and every existing test; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research
charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely unauthorized,
and `OPS-0007` §8 step I is neither begun nor advanced by this filing. **EQIX and UNH remain
uncovered and unauthorized.** No ninth Milestone 3 batch is authorized by this filing, and none is
inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future, separately
implemented, draft-until-independently-reviewed research PR may begin exactly the batch scoped
above only after this decision itself merges; any resulting Company Intelligence record, comparison
artifact, freshness-registry update, or later policy consequence remains subject to that PR's own
independent review, principal acceptance, validation, and (for anything beyond Intelligence
content) its own separate future governance decision.
