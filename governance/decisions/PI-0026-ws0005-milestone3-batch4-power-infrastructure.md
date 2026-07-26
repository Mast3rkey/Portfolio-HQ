---
decision_id: PI-0026
date: 2026-07-26
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, PI-0007, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, AUTO-0001]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1 (baseline/inventory) and 2
(Intelligence coverage/freshness audit) to execute, as one bounded first audit PR. §5 states
explicitly: "Completion of Milestones 1 and 2 does not automatically authorize Milestone 3.
Starting Intelligence-completion batches ... requires its own separate, later, explicit principal
authorization and its own bounded implementation or research PR." Three Milestone 3 research
batches have since been authorized and completed under that discipline: `PI-0023` (ASML, AMAT,
KLAC, LRCX — the `semis` cluster's capital-equipment sub-segment; PR #154, merged and complete),
`PI-0024` (MU, SKHY — the `semis` cluster's memory sub-segment, WDC explicitly excluded; PR #158,
merged and complete), and `PI-0025` (AVGO, AMD, MRVL, INTC — the `semis` cluster's remaining
compute/networking/foundry sub-segment; PR #161, merged, independently confirmed PROVISIONAL per
`OPS-0007` §3). All three batches covered members of the governed `semis` correlated-cluster cap.
No prior batch has covered any member of the governed `power_infra` correlated-cluster cap.

`targets.yaml`'s `power_infra` cluster (≤20% of book) has exactly four members: `GEV, ETN, VRT,
PWR`. Of these, only **GEV** carries an existing Company Intelligence record — created under
`PI-0007` (the historical NVDA + GEV batch, filed before `governance/decisions/` existed),
independently reviewed and refreshed twice since (`PI-0019`/`PI-0020`'s bounded GEV
committee-review and Intelligence-refresh authorizations). **ETN, VRT, and PWR have no Company
Intelligence record.** This is independently confirmed against live repository state at this
filing's base commit, not restated from any prior artifact:

- **ETN (Eaton Corporation)** — `holdings.yaml` `shares.ETN: 0.262049` (a governed, live-priced
  holding); `targets.yaml` places it in the `band` tier (0.75% target, cap 1.25×, RSI-gated trim)
  and in the `power_infra` correlated-cluster cap (≤20% of book, `targets.yaml` line 86). No
  Company Intelligence record exists (`intelligence/companies/` currently holds AMAT, AMD, ASML,
  AVGO, COST, GEV, INTC, ISRG, KLAC, LRCX, MRVL, MU, NVDA, SKHY, TMO, TSM, XOM — 17 records, 13
  ACCEPTED and 4 PROVISIONAL per `OPS-0007` §3). No row for ETN exists in
  `intelligence/freshness_registry.yaml` or `intelligence/freshness_checkpoints.yaml`.
- **VRT (Vertiv Holdings)** — `holdings.yaml` `shares.VRT: 0.332404` (a governed, live-priced
  holding); `targets.yaml` places it in the `band` tier (0.75% target) and in the `power_infra`
  cluster. No Company Intelligence record or freshness row exists.
- **PWR (Quanta Services)** — `holdings.yaml` `shares.PWR: 0.160774` (a governed, live-priced
  holding); `targets.yaml` places it in the **`T2`** tier (1.65% target, subject to the T1/T2
  mechanical concentration ceiling — `gates.t1t2_trim_mult`, 1.5×, no RSI gate — not the `band`
  tier's 1.25× cap or RSI-gated trim, neither of which applies to PWR) and in the `power_infra`
  cluster. No Company Intelligence record or freshness row exists.
- **GEV (GE Vernova)** — `holdings.yaml` `shares.GEV: 0.208382`; `targets.yaml` places it in `T1`
  (3.35% target) and in `power_infra`. Existing Company Intelligence record (`portfolio_role_ref:
  T1`, `conviction.rating: Medium`, `last_reviewed: 2026-07-22`, per `PI-0020`'s refresh). **GEV is
  not part of this batch** — its record is not authorized to be created, edited, or refreshed by
  this decision or by any later implementation PR this decision authorizes; it is comparison-only
  existing context, exactly as `PI-0025` treated `NVDA`/`TSM`/`ASML`/`AMAT`/`KLAC`/`LRCX` as
  existing comparison context for its own batch's overlap section.

Preflight for this filing independently confirmed: no open pull request exists in the repository
(`state: open` returns empty — PR #164 is confirmed merged, closed at `2026-07-26T13:43:14Z`, an
ancestor of `origin/main`'s current tip `f16796ce02cd9a8dd36341ee30e65e1d165d9f06`); no local or
remote branch references ETN, VRT, PWR, "batch4," "batch-4," or "power_infra" beyond this filing's
own branch; `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml`
carry no row for ETN, VRT, or PWR; no `PI-####` decision authorizes Company Intelligence research
on any of the three. `operations/WORKSTREAMS.yaml`'s WS-0005 entry, checked live at this filing's
base commit: Milestone 3's `status` is `in_progress` for the milestone as a whole (Batches 1-3
complete/merged; no fourth batch recorded as authorized anywhere in the entry); `OPS-0007` §8 step
H (creation of the preliminary architecture/target-scenario package, PR #163) is recorded merged
and independently post-merge verified by PR #164 (merge commit
`f16796ce02cd9a8dd36341ee30e65e1d165d9f06`, confirmed the current `origin/main` tip); `OPS-0007` §8
step I (the official-and-provisional Monday allocation-check package, §5) remains gated, unbegun,
and is not touched by, drawn on, or advanced by this filing in any way. **PI-0026** is confirmed as
the next unused decision number in the series — checked live against both
`governance/decisions/` (highest filed: `PI-0025`, and `OPS-0007`, the highest-numbered decision of
any prefix) and `governance/decisions.yaml` (same, 35 filed ↔ 35 indexed, no orphans) at this
filing's base commit, not assumed. Working tree confirmed clean at this filing's base commit.

The principal has explicitly authorized preparation of a fourth Milestone 3 batch covering
**exactly ETN, VRT, and PWR**, intended to complete first-coverage research for the three currently
uncovered members of the governed `power_infra` cluster. GEV, already researched under `PI-0007`
and refreshed under `PI-0019`/`PI-0020`, may be used as existing comparison context but its record
must not be edited by this filing or by the later Batch 4 implementation unless separately
authorized. This decision records that authorization; it does not itself perform any research.

## Decision

**PI-0026 authorizes exactly one thing: the fourth bounded WS-0005 Milestone 3 research batch,
covering ETN, VRT, and PWR, and nothing else.** This is **evidence development only** — no
research has been performed, and this filing alone authorizes no research finding, Company
Intelligence record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, trade, or order.
**This filing (its own governance PR) authorizes the creation of the governance-authorization
package only — this PI-0026 decision file, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log entry. It does not
authorize drafting any ETN, VRT, or PWR Company Intelligence record or the comparison artifact —
those become authorized to begin only after this governance decision is independently reviewed,
principal-accepted, and merged**, exactly as `PI-0023`/`PI-0024`/`PI-0025`'s own
authorization-precedes-research separation already established.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/ETN.yaml`
   / `.md`, `VRT.yaml` / `.md`, `PWR.yaml` / `.md` — using the existing repository schema frozen by
   `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated provisions, with the human approvals
   every prior first-coverage record has required (`portfolio_role_ref` — descriptive only,
   `conviction.rating` from `PI-0004`'s closed four-value vocabulary, conviction rationale, review
   cadence, thesis/risks/catalysts, and source-access disclosure).
2. Create exactly **one hand-authored batch comparison artifact**, at
   `intelligence/BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md` — the filename chosen to mirror this
   repository's existing convention (`BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`,
   `BATCH2_MEMORY_COMPARISON.md`, `BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`:
   `BATCH<N>_<SUBJECT>_COMPARISON.md`, uppercase, underscore-separated, directly under
   `intelligence/`), naming this batch's coherent theme — the power and electrification value
   chain — per §C below. **GEV may appear in this artifact as existing researched comparison
   context; the artifact must not edit, restate as new, or silently supersede any content of
   `intelligence/companies/GEV.yaml` or `GEV.md`.**
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per
   §B.21 below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention
   (mirroring `PI-0011`/`AUTO-0002`/`PI-0023`/`PI-0024`/`PI-0025`'s own narrow, single-purpose
   additions).
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0026`, `company_record_authority:
   PI-0026`) — matching the existing pattern for the seventeen currently-enrolled tickers, and
   matching both files' own stated convention that a row requires "its own existing, cited Company
   Intelligence record" and is added only through a human-reviewed PR, never by automation. No
   `monitoring_enabled` row may be set `true` by that PR. **GEV's existing row is unaffected.**
7. Perform **only the minimum factual** `operations/WORKSTREAMS.yaml` synchronization required by
   repository convention for WS-0005's Milestone 3 gate (status, `pr`, `date`) once that
   implementation PR merges — not before, and not by this filing.

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (per company)

The implementation PR's research, for each of ETN, VRT, and PWR individually, must establish, at
minimum:

1. Economic function and current governed portfolio role.
2. Business model and material revenue drivers.
3. Segment and end-market composition.
4. Data-center, utility, grid, industrial, commercial-building, and other relevant demand exposure.
5. Products, services, technology, engineering, construction, and aftermarket exposure as
   applicable.
6. Customers, suppliers, competitors, and substitutes.
7. Customer and project concentration.
8. Backlog quality, cancellation risk, and revenue-conversion characteristics.
9. Competitive moat and barriers to entry.
10. Financial quality, margins, working capital, free cash flow, and cyclicality.
11. Capital expenditure, acquisitions, and capital allocation.
12. Balance-sheet resilience and downturn behavior.
13. Labor, materials, supply-chain, execution, and fixed-price-contract risk.
14. Interest-rate, utility-spending, hyperscaler-capex, regulatory, and geopolitical exposure.
15. Management claims versus independently supported facts.
16. Actively searched disconfirming evidence.
17. Explicit thesis-break conditions.
18. What portfolio exposure would be lost if the company were absent.
19. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3, preserved for later reconciliation, never treated
    as presumptively correct or cited as support for a research conclusion. (PWR: `T2`, 1.65%
    target, T1/T2 concentration ceiling, `power_infra` cluster. ETN, VRT: `band`, 0.75% target,
    1.25× cap with RSI-gated trim, `power_infra` cluster.)
20. **Margin-relevance evidence, factual and advisory only** — cyclicality; liquidity; leverage;
    balance-sheet sensitivity; refinancing/funding risk; drawdown and recovery characteristics;
    correlated-loss behavior — with no recommendation to borrow, no safe-leverage calculation, and
    no deployment-timing or margin-ceiling conclusion of any kind, matching `OPS-0006` §4
    Milestone 3's own margin-relevant-evidence requirement and `PI-0023` §B.16 / `PI-0024` §B.16 /
    `PI-0025` §B.10 exactly.
21. Evidence-driven freshness cadence and refresh triggers per §"Refresh and monitoring
    requirements" below.
22. **External opportunities or replacements only as unauthorized future leads** — identify
    credible non-owned competitors, substitutes, or missing-system candidates revealed by the
    research; explain the economic role each candidate could serve; distinguish genuinely new
    exposure from duplicate exposure; retain no more than a small, evidence-supported candidate
    list; treat all candidates as advisory future-research leads only, matching `PI-0023` §B.17 /
    `PI-0024` §B.18 / `PI-0025` §B.11 exactly: no holding add, no `holdings.yaml` change, no
    tier/target assignment, no mechanical ranking, no batch expansion, and no research on an
    outside candidate without its own separate future authorization.

In addition to the above, the research must specifically cover, per company:

**ETN (Eaton Corporation):**
- Electrical segment disclosures and end-market composition (data center, utility, industrial,
  commercial/institutional, residential, aerospace, vehicle).
- Data-center and utility end-market materials, including any disclosed data-center-specific
  order or backlog figures.
- Acquisition and capital-allocation disclosures, and integration risk from any material
  acquisitions.
- Margin-relevant balance-sheet, gap-risk, and correlated-loss evidence.

**VRT (Vertiv Holdings):**
- Thermal-management and power-system disclosures (cooling, power distribution, IT infrastructure
  for data centers specifically).
- Data-center demand and backlog materials, including AI/hyperscaler-driven demand signals.
- Customer-concentration and supply-chain disclosures.
- Margin-relevant liquidity, gap-risk, and correlated-loss evidence.

**PWR (Quanta Services):**
- Electric-power, utility, communications, and infrastructure segment disclosures.
- Backlog and project-risk disclosures, including cancellation and rescheduling risk.
- Fixed-price-contract, labor, safety, regulatory, and acquisition disclosures.
- Margin-relevant liquidity, working-capital, and correlated-loss evidence specific to a
  labor-intensive, contract-services business model (distinct from ETN's and VRT's
  equipment-manufacturing economics).

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/BATCH4_POWER_INFRASTRUCTURE_COMPARISON.md`)
must explicitly distinguish, across ETN, VRT, PWR, and existing GEV context:

1. Each company's distinct function in the power/electrification value chain — electrical
   equipment (ETN) versus thermal/power-management-for-data-centers (VRT) versus
   engineering/construction/infrastructure services (PWR) versus power-generation-and-grid
   equipment (GEV, existing context only).
2. Direct and indirect data-center exposure — per company, distinguishing directly-sold
   data-center equipment/services from broader electrification/grid exposure that only partially
   overlaps with data-center demand.
3. Utility and grid-capital-spending exposure — per company.
4. Customer and supplier overlap — per company, and against GEV where evidence supports it.
5. Backlog composition and execution risk — per company (equipment backlog for ETN/VRT versus
   project backlog for PWR's contract-services model).
6. Recurring versus project-based economics — per company.
7. Capital intensity and working-capital behavior — per company.
8. Acquisitions and integration risk — per company.
9. Common macro and spending-cycle dependencies across the four (AI-data-center buildout,
   utility-capex cycles, interest-rate sensitivity).
10. Raw-material, labor, regulatory, and interest-rate sensitivities — per company.
11. Common correlated-loss mechanisms across the batch, and against GEV where evidence supports
    it — the same shared-driver evidence that originally justified the `power_infra` cluster cap
    (`targets.yaml`'s own comment: "real shared driver is AI data-center power/electricity demand
    buildout, not just market beta").
12. Genuine diversification versus duplicated exposure among ETN, VRT, PWR, and GEV.
13. **Whether the existing `power_infra` grouping describes one coherent risk cluster or several
    meaningfully distinct economic functions, and what evidence supports or challenges the
    cluster's present rationale** — structural/economic overlap kept explicitly distinct from
    measured historical price correlation, per `OPS-0006` §4 Milestone 4's own distinction, which
    this batch's evidence must respect even though Milestone 4 itself remains unauthorized.
14. Company-specific and common margin-risk amplifiers across the batch.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically
score or rank the four companies, must not declare a preferred holding, must not alter a tier,
target, role, cluster, or cap, must not recommend a trade, must not recommend margin, and must not
control allocator output — matching `PI-0024` §C's and `PI-0025` §C's no-ranking rule exactly.
**The comparison may recommend future review of the cluster's composition or cap as an advisory
research conclusion, but that recommendation carries no automatic policy effect** — any actual
change to `targets.yaml`'s `power_infra` cluster requires its own separate, later, explicit
governance decision, exactly as every other WS-0005 finding in this repository's history has been
treated (e.g. the "T1 AI-infra cluster cap: scanned and declined" precedent, and the still-open
capital-impairment question the T1/T2 concentration ceiling entry left for future, separate
judgment).

### D. Evidence and access discipline

Require: primary sources for changeable facts; claim-level evidence; explicit separation of fact,
inference, uncertainty, judgment, source type, and actual inspection/access status (the same
standard `PI-0016` §D, `PI-0023` §D, `PI-0024` §D, and `PI-0025` §D already apply, adopted here by
reference for its evidentiary discipline only — this batch is first-coverage record creation for
ETN, VRT, and PWR, not a `PI-0016` committee review of existing conviction, since none of the three
has an existing record or rating to review; GEV's own existing conviction rating is not reviewed,
revisited, or reassessed by this batch under any framework); active search for and preservation of
disconfirming evidence and null/negative findings; no unsupported search-result snippet presented
as inspected primary evidence; no silent inheritance of an earlier chat conclusion without
independent verification.

**Required direct-inspection attempts, per company, where applicable:**

- SEC Form 10-K, 10-Q, and relevant 8-K filings.
- Official earnings releases and official earnings-call materials (transcripts or webcast
  materials).
- Official investor presentations and annual reports.
- Official product, end-market, backlog, and strategy materials.
- Relevant government, utility, regulatory, and industry documents.

**Additional expected source areas, per company:**

- **ETN**: electrical segment disclosures; data-center and utility end-market materials;
  acquisition and capital-allocation disclosures.
- **VRT**: thermal-management and power-system disclosures; data-center demand and backlog
  materials; customer-concentration and supply-chain disclosures.
- **PWR**: electric-power, utility, communications, and infrastructure segment disclosures;
  backlog and project-risk disclosures; fixed-price, labor, safety, regulatory, and acquisition
  disclosures.

**A blocked primary source must be:**

- Identified precisely (the specific document and URL or filing reference attempted).
- Labeled explicitly as "attempted but not directly inspected."
- Kept separate from WebSearch-derived or other secondary evidence, never merged into the same
  citation as if both were equally verified — search-result snippets may identify documents but
  may not be represented as inspected evidence.
- Never described as directly verified.

**No silent scope contraction is permitted because a source is blocked.** If sufficient primary
evidence cannot be accessed for any one of the three companies under this standard, the future
implementation must try reasonable official alternatives, then stop, disclose exactly what failed,
and return for explicit principal direction — it may not silently narrow, substitute, or declare
the record complete. This mirrors `PI-0024` §F's and `PI-0025` §D's "no automatic contraction"
rule exactly: the authorized batch is exactly ETN, VRT, and PWR — not any two of them, not any one.

Every material claim must distinguish fact, inference, uncertainty, judgment, source type, and
actual access/inspection status.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business
change, thesis uncertainty, cyclicality, customer/project concentration, backlog-execution risk,
capital intensity, regulatory sensitivity, acquisition or integration state, and event/gap risk.
**No universal cadence is imposed by this decision, and none may be imposed automatically by the
implementation.**

Each record should define named review triggers where supported by evidence, drawn from — but not
limited to — `OPS-0006` §12's candidate-trigger list as applied selectively (not every listed
trigger applies to every company): earnings or guidance changes; data-center or hyperscaler
customer-concentration disclosures; major backlog, order, or project awards/cancellations;
acquisition or integration developments; credit-rating, debt, liquidity, or capital-spending
changes; utility-capex or regulatory developments; and major market-share or competitive changes.

### F. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before
comparing them with current governed tier/role/target/cluster placement; preserve that placement
as the historical baseline for later reconciliation only (§B.19 above); never treat it as proof of
a research conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7;
and record any disagreement between researched conclusion and governed baseline — including any
disagreement about the `power_infra` cluster's own coherence (§C.13) — without changing policy.

### G. Hard prohibitions

This decision and any later implementation authorize none of the following, under any
interpretation:

- Any change to ETN/VRT/PWR's (or GEV's, or any other ticker's) holdings, targets, tiers, roles,
  clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch, against
  GEV, or against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way — Company
  Intelligence remains advisory-only, per the unchanged `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
  boundary.
- **Any edit, refresh, or reassessment of `intelligence/companies/GEV.yaml` or `GEV.md`** — GEV's
  existing record, conviction rating, and freshness metadata are untouched by this decision and by
  any implementation it authorizes.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C), including §C.13's cluster-coherence discussion —
  which remains advisory research output, not a Milestone 4 conclusion.
- Any research or Company Intelligence record for a fifth company, or for any ticker not named
  ETN, VRT, or PWR.
- Modifying any existing Company or Theme Intelligence record (AMAT, AMD, ASML, AVGO, COST, GEV,
  INTC, ISRG, KLAC, LRCX, MRVL, MU, NVDA, SKHY, TMO, TSM, XOM, `ai_infrastructure`,
  `life_sciences_tools_medtech`).
- Silently importing existing tiers or targets as research conclusions.
- **Automatically validating, rejecting, or otherwise changing the effective status of the
  `power_infra` cluster cap** — §C.13's advisory research finding is not, by itself, a policy
  action; any actual cap change requires its own separate, later, explicit governance decision.
- Automatic authorization of a fifth Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 4 does not authorize Batch 5 or Milestone 4.
- Beginning, advancing, or drawing on `OPS-0007` §8 step I (the official-and-provisional Monday
  allocation-check package) in any way.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.

### H. Governance package (this filing)

This decision's own implementation — the governance PR itself, not the future research PR —
touches exactly:

1. This decision file,
   `governance/decisions/PI-0026-ws0005-milestone3-batch4-power-infrastructure.md`.
2. `governance/decisions.yaml` (index regeneration: one new entry for `PI-0026`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization,
   using only `OPS-0001`'s existing 21-field schema and existing status vocabulary — no new field,
   no new status value). Milestones 1-2 and Milestone 3 Batches 1-3 entries remain exactly as
   prior filings left them; Milestone 3 remains `status: in_progress` for the milestone as a whole
   (this batch's authorization does not make Milestone 3 `complete` in aggregate); Milestones 4-9
   remain `status: proposed`, unauthorized, unchanged; `next_action` states the next step is
   exactly one bounded research implementation PR for this batch — not a fifth batch, not
   Milestone 4, not `OPS-0007` §8 step I; `evidence_refs` gains a reference to this decision; no
   unrelated workstream priority or authority field changes — WS-0005 remains the sole
   `priority: primary` workstream, WS-0001/WS-0002/WS-0003/WS-0004 priorities untouched;
   `active_branch`/`active_pr` are left exactly as this filing's base commit recorded them,
   matching `PI-0023`/`PI-0024`/`PI-0025`'s own precedent of leaving those fields to a later
   post-merge synchronization PR, not to the batch-authorization filing itself.
4. The applicable `CLAUDE.md` Decisions Log entry recording this acceptance.

**No other file is touched by this governance filing.** No Company Intelligence record, no
comparison artifact, no freshness-registry or freshness-checkpoint row, and no test or validator
file is created, modified, or authorized to be created by this filing — those belong exclusively
to the later, separate implementation PR authorized in §A.

### I. Effectiveness, review, and merge gates

- **This authorization becomes effective only when this governance PR merges to `main`.** Before
  that, nothing in §A is authorized to begin.
- **The later Company Intelligence implementation must occur in its own separate, bounded PR** —
  never combined with this governance filing, and never opened before this filing merges.
- **That implementation PR must remain in draft state until it has been independently reviewed** —
  it may not be marked ready for review, and must not be merged, before an eligible independent
  review is retained.
- **An eligible independent review must be retained and anchored to the exact implementation PR
  head** that ultimately merges, per the capability-based standard `OPS-0007` §1 established
  (Fable remains eligible; any reviewer meeting every §1 requirement is equally eligible; the
  authoring session may never review its own work) — a review anchored only to an intermediate
  commit does not satisfy this gate.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready — following `OPS-0007` §1.11's
  single-bounded-correction-pass mechanism.
- **Principal acceptance is required before merge** — explicit, at the exact head being merged, not
  inferred from silence or from an earlier round's acceptance of a different head.
- **Post-merge verification and factual `operations/WORKSTREAMS.yaml` synchronization are
  required** after that implementation PR merges — ancestry, merge scope, validator, and test
  re-verification on a clean checkout of the merged state, followed by a factual (not aspirational)
  register update, matching the discipline `PI-0023`/`PI-0024`/`PI-0025`'s own implementations and
  post-merge syncs already established.
- **Completion of this batch does not authorize a fifth Milestone 3 batch or any Milestone 4
  work**, and does not begin or advance `OPS-0007` §8 step I. Each requires its own separate,
  later, explicit principal authorization, exactly as `PI-0023` §E, `PI-0024` §I, and `PI-0025` §I
  already state for their own batches.

This governance PR itself (the one implementing this decision) is subject to the same discipline:
it must remain in draft state, gain its own eligible independent review anchored to its exact head
per `OPS-0007` §1, and receive explicit principal acceptance before it may be marked ready or
merged. This decision does not mark itself, or authorize marking itself, ready for merge.

## Rationale

**Why a batch, and why these three, with GEV as comparison-only.** `OPS-0006` §4 Milestone 3
explicitly contemplates "coherent batches" rather than single-company filings, and this repository
has direct precedent for multi-company Intelligence authorizations (`PI-0007`, `PI-0009`,
`PI-0023`, `PI-0024`, `PI-0025`). ETN, VRT, and PWR are not an arbitrary slice of the roster — they
are the entire remaining uncovered membership of the governed `power_infra` correlated-cluster cap,
whose fourth and only-covered member (GEV) already has an existing, twice-refreshed Company
Intelligence record. Completing first-coverage for the other three closes exactly the same kind of
coverage gap `PI-0023`/`PI-0024`/`PI-0025` closed for the `semis` cluster, one cluster over. The
three share a genuinely comparable driver set — the `power_infra` cluster's own governing rationale
(`targets.yaml`: "real shared driver is AI data-center power/electricity demand buildout") — while
their business models are deliberately preserved as materially distinct (ETN: diversified
electrical-equipment manufacturer; VRT: data-center-specific thermal/power-management equipment
manufacturer; PWR: labor-intensive engineering/construction/infrastructure-services provider),
which is exactly the kind of comparative, non-duplicative evidence §C requires. GEV's inclusion as
comparison-only context, without touching its existing record, mirrors exactly how `PI-0025`
referenced Batch 1's ASML/AMAT/KLAC/LRCX as existing comparison context for its own cross-batch
overlap section, without re-authorizing or editing those records.

**Why `PI-0026`, not a new `OPS-####` or a reuse of `PI-0023`/`PI-0024`/`PI-0025`.** Same category
and reasoning as `PI-0023`/`PI-0024`/`PI-0025`: this is Company Intelligence research-authorization
content (`category: portfolio_intelligence`), not workstream-register mechanics, so it is filed in
the `PI-####` series per `governance/decisions/README.md`'s convention. `PI-0023`, `PI-0024`, and
`PI-0025` are all `status: Accepted` and, per that same convention, are never edited after
acceptance for anything beyond a narrow dated correction — a fourth batch requires its own new
decision file. `PI-0026` is confirmed as the next unused number, checked live against both
`governance/decisions/` and `governance/decisions.yaml` at this filing's base commit, not assumed.

**Why first-coverage discipline, not the `PI-0016` committee-review framework, for ETN/VRT/PWR —
and why GEV's existing review is untouched.** Identical reasoning to `PI-0023`/`PI-0024`/`PI-0025`:
`PI-0016`'s standing methodology governs review of an *existing* Company Intelligence record's
conviction and capital-priority standing; none of ETN, VRT, or PWR has an existing record, so this
batch is first-coverage record creation, structurally identical in kind to `PI-0003`, `PI-0005`,
`PI-0007`, `PI-0009`, `PI-0023`, `PI-0024`, and `PI-0025` — not a `PI-0016` review. GEV already
underwent its own dedicated `PI-0016`-methodology committee review (`PI-0019`, closed by `PI-0020`
with an Intelligence refresh) — this batch does not reopen, duplicate, or supersede that review;
GEV's role here is strictly as existing comparison context, per §A.2's explicit prohibition on
editing its record.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR, not
accompany it — the same separation `PI-0013`'s, `PI-0023`'s, `PI-0024`'s, and `PI-0025`'s own
rationale already established, and the principal's own explicit instruction for this filing:
authorize the package now, gate the research implementation on this decision's independent review,
principal acceptance, and merge.

## Alternatives Considered

- **Authorize fewer than three companies now, deferring the rest to later batches.** Rejected —
  the principal's authorization is explicit that the batch is exactly ETN, VRT, and PWR together,
  and the batch's own justification (completing the `power_infra` cluster's coverage as one
  coherent unit) rests on comparative evidence a smaller grouping would weaken, the same reasoning
  `PI-0024`/`PI-0025` applied when rejecting a narrower authorization.
- **Include GEV as a fourth researched company in this batch, refreshing or re-reviewing its
  record.** Rejected — GEV already has a current, twice-refreshed Company Intelligence record
  (`PI-0007` original, `PI-0019`/`PI-0020` committee review and refresh, `last_reviewed:
  2026-07-22`); re-researching it here would duplicate completed work and exceed the principal's
  explicit instruction that GEV's record "must not be edited by this filing or by the later Batch 4
  implementation unless separately authorized."
- **Adopt `PI-0016`'s full committee-review framework for this batch.** Rejected — same reasoning
  as `PI-0023`/`PI-0024`/`PI-0025`: `PI-0016` presumes an existing record and conviction rating to
  reassess, which none of ETN, VRT, or PWR has.
- **File under a new `OPS-####` number.** Rejected — same reasoning as `PI-0023`/`PI-0024`/
  `PI-0025`: this is Company Intelligence research-authorization content, not workstream-register
  mechanics.
- **Let this filing itself begin the research, or authorize the implementation PR to open
  immediately (non-draft) on this decision's merge.** Rejected — the principal's explicit
  instruction, and `OPS-0006` §5's existing discipline, requires the authorization to be
  independently reviewed and merged first, and requires the later implementation PR to remain
  draft until its own independent review and principal acceptance — mirroring the gate structure
  `PI-0023`/`PI-0024`/`PI-0025` each already used.
- **Update `intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml` in this governance
  PR.** Rejected — both files gain a row only for a ticker with "its own existing, cited Company
  Intelligence record," which does not yet exist for any of the three; adding rows belongs in the
  future implementation PR, exactly as `PI-0023`/`PI-0024`/`PI-0025` reasoned for their own batches.
- **Authorize a fifth Milestone 3 batch, begin Milestone 4 relationship mapping, or begin `OPS-0007`
  §8 step I in this same filing.** Rejected — exceeds the principal's authorization, which names
  exactly ETN, VRT, and PWR for Batch 4 only; each requires its own future, separate authorization.
- **Have this batch's comparison artifact resolve the `power_infra` cluster-coherence question
  (§C.13) as a binding conclusion.** Rejected — a Milestone 3 batch comparison is advisory research
  output, not a Milestone 4/5 policy conclusion; any actual cluster or cap change requires its own
  separate, later, explicit governance decision, per `OPS-0006` §6's explicit prohibition on this
  workstream directly changing clusters or caps.

## Consequences

**Authorized, effective on this decision's merge:** exactly one fourth Milestone 3 research batch
(ETN, VRT, PWR), scoped and bounded exactly as stated in §§A-I above, to proceed via its own later,
separate, bounded, draft-until-independently-reviewed implementation PR.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (AMAT, AMD, ASML,
AVGO, COST, GEV, INTC, ISRG, KLAC, LRCX, MRVL, MU, NVDA, SKHY, TMO, TSM, XOM, `ai_infrastructure`,
`life_sciences_tools_medtech`) — GEV's included, in full; `allocate.py`, `margin_state.py`,
`intelligence_validator.py`, `intelligence_report.py`, every freshness module, and every test file;
the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research charter and trial ceiling;
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4 through 9 of WS-0005 remain entirely
unauthorized, and `OPS-0007` §8 step I remains gated and unbegun. No fifth Milestone 3 batch is
authorized by this filing, and none is inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, cluster
conclusion, or automatic implementation is authorized or implied by this decision alone.** A
future, separately implemented, draft-until-independently-reviewed research PR may begin exactly
the batch scoped above only after this decision itself merges; any resulting Company Intelligence
record, comparison artifact, freshness-registry update, or later policy consequence remains subject
to that PR's own independent review, principal acceptance, validation, and (for anything beyond
Intelligence content) its own separate future governance decision. If that future session cannot
obtain sufficient primary evidence for any one of the three companies, it must try reasonable
official alternatives, then stop, disclose the evidence-access problem, and return for explicit
principal amendment — it may not narrow this batch on its own authority.
