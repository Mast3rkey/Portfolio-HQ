---
decision_id: PI-0025
date: 2026-07-26
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, AUTO-0001]
supporting_artifact: null
---

## Context

`PI-0023` authorized WS-0005 Milestone 3's first batch (ASML, AMAT, KLAC, LRCX — the `semis`
cluster's capital-equipment sub-segment); its implementation (PR #154) is merged and complete.
`PI-0024` authorized the second batch (MU, SKHY — the cluster's DRAM/NAND memory sub-segment,
WDC explicitly excluded); its implementation (PR #158) is merged and principal-accepted. Its own
post-merge synchronization PR (#159) has itself now been independently reviewed (Fable review
anchored to exact head `d9a52f1f70f9571d53c9ec474fb79d0ddf74ca81`, verdict "APPROVED FOR READINESS
AND MERGE," stating explicitly that upon merge Batch 2 "may properly be described as fully complete
per PI-0024 §I and OPS-0006 §16.1") and merged — the merge commit,
`7c11d90fc8e68670f814ac35d32de693ab166a21`, is this filing's own verified base. **Batch 2 is
therefore fully complete, not merely merged.** Milestone 3 overall remains `status: in_progress` —
completing Batch 2 did not complete Milestone 3 as a whole, and Batch 3 still requires its own
separate authorization, which this decision provides only upon its own merge. Neither `PI-0023` nor
`PI-0024` authorized a third batch; both
decisions' Alternatives Considered sections name AVGO, AMD, MRVL, and INTC among the cluster's
still-uncovered members, explicitly without selecting or authorizing any of them. WS-0005's
`next_action` field at this filing's base commit names, without selecting or authorizing,
"Remaining candidate uncovered semis-cluster members for a possible future batch: AVGO, AMD, MRVL,
INTC."

The principal has explicitly authorized preparation of a third Milestone 3 batch covering **exactly
AVGO, AMD, MRVL, and INTC**, justified as a coherent semiconductor compute, accelerated-computing,
networking, custom-silicon, and integrated-device/foundry comparison set — distinct in kind from
Batch 1's equipment sub-segment and Batch 2's memory sub-segment — while preserving each company's
materially different business model (AVGO: diversified semiconductor plus infrastructure-software
conglomerate; AMD: fabless CPU/GPU/accelerator designer; MRVL: fabless networking/custom-silicon
specialist; INTC: integrated device manufacturer pursuing an external foundry strategy). This
decision records that authorization; it does not itself perform any research.

Independently confirmed against live repository and GitHub state at filing time (not restated from
either prior batch's decision or audit artifact, per the same reconciliation-gate discipline
`PI-0023`/`PI-0024` each applied to their own selection):

- **Repository identity** confirmed exactly `Mast3rkey/Portfolio-HQ`.
- **Authoritative `origin/main`** fetched and pruned successfully; local `main` reset to match
  `origin/main` exactly at merge commit `7c11d90fc8e68670f814ac35d32de693ab166a21` — confirmed the
  merge commit for PR #159 (WS-0005 Milestone 3 Batch 2 post-merge synchronization), with parents
  `d9a52f1f70f9571d53c9ec474fb79d0ddf74ca81` (the reviewed head) and PR #158's own merge commit
  `6740f9eca95303e97368f3d010bf99fba1cb404b` as its ancestor. PR #158 independently confirmed merged
  at reviewed/principal-accepted head `957a223278e154a9bdd20033911cec79f0696c37`. This matches the
  expected authoritative starting state stated for this filing exactly — no divergence to
  investigate.
- **AVGO** — `holdings.yaml` `shares.AVGO` present (a governed, live-priced holding); `targets.yaml`
  places it in the `T2` tier (1.65% target), subject to the T1/T2 mechanical concentration ceiling
  (`gates.t1t2_trim_mult`, 1.5×, no RSI gate — not the `band` tier's 1.25× cap or RSI-gated trim,
  neither of which applies to AVGO), and in the `semis` correlated-cluster cap (≤25% of book). This
  is the current historical/governed baseline only, preserved per `OPS-0006` §2/§3 for later
  reconciliation — it is not evidence supporting any future conviction rating, role, or capital
  priority for AVGO. No Company Intelligence record exists
  (`intelligence/companies/` currently holds AMAT, ASML, COST, GEV, ISRG, KLAC, LRCX, MU, NVDA,
  SKHY, TMO, TSM, XOM — 13 records). No row for AVGO exists in
  `intelligence/freshness_registry.yaml` or `intelligence/freshness_checkpoints.yaml`.
- **AMD** — `holdings.yaml` `shares.AMD` present (a governed, live-priced holding); `targets.yaml`
  places it in `band` (0.75% target) and in the `semis` cluster. No Company Intelligence record or
  freshness row exists.
- **MRVL** — `holdings.yaml` `shares.MRVL` present (a governed, live-priced holding); `targets.yaml`
  places it in `band` (0.75% target) and in the `semis` cluster. No Company Intelligence record or
  freshness row exists.
- **INTC** — `holdings.yaml` `shares.INTC` present (a governed, live-priced holding); `targets.yaml`
  places it in the `spec` tier (1.0% fixed target, no RSI-gated trim) and in the `semis` cluster.
  No Company Intelligence record or freshness row exists. `PI-0014` (bounded, conversation-only,
  read-only evidence review of INTC's committed TSM/INTC-overlap open question, no repository
  artifact) is the only prior governance touchpoint naming INTC — it produced no Company
  Intelligence record and does not substitute for one; this decision treats it strictly as
  conversational context, never as a source a future implementation may cite as if it were a filed
  record.
- No open pull request exists in the repository (`state: open` returns empty, independently
  confirmed via the GitHub API at filing time). No local or remote branch references AVGO, AMD,
  MRVL, INTC, "batch3," "batch-3," or "milestone-3" beyond this filing's own branch
  (`claude/portfolio-hq-batch-3-auth-9pw2hs`) and the unrelated, already-closed-in-spirit
  `gov/pi-0014-intc-syk-dhr-bounded-evidence-review` branch (a stale remote ref from `PI-0014`'s
  own, separate, already-filed evidence review — it does not authorize or implement any part of
  this batch and is not touched by this filing). `intelligence/freshness_registry.yaml` and
  `intelligence/freshness_checkpoints.yaml` carry no row for AVGO, AMD, MRVL, or INTC. No `PI-####`
  decision authorizes Company Intelligence research on any of the four.
- `operations/WORKSTREAMS.yaml`'s WS-0005 entry, checked live at this filing's base commit: Milestone
  3's `status` is `in_progress` for the milestone as a whole (Batch 1 complete, Batch 2 merged and
  pending its own post-merge-sync review); no third batch is recorded as authorized anywhere in the
  entry.
- **PI-0025** is confirmed as the next unused decision number in the series — checked live against
  both `governance/decisions/` (highest filed: `PI-0024`) and `governance/decisions.yaml` (highest
  indexed: `PI-0024`) at this filing's base commit, not assumed.
- Working tree confirmed clean at this filing's base commit.

## Decision

**PI-0025 authorizes exactly one thing: the third bounded WS-0005 Milestone 3 research batch,
covering AVGO, AMD, MRVL, and INTC, and nothing else.** This is **evidence development only** — no
research has been performed, and this filing alone authorizes no research finding, Company
Intelligence record, policy change, tier/target/roster/cluster/cap/allocator change,
margin-policy recommendation, trade, or order. **This filing (its own governance PR) authorizes the
creation of the governance-authorization package only — this PI-0025 decision file,
`governance/decisions.yaml`, `operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions
Log entry. It does not authorize drafting any AVGO, AMD, MRVL, or INTC Company Intelligence
record or the comparison artifact — those become authorized to begin only after this governance
decision is independently reviewed, principal-accepted, and merged**, exactly as `PI-0013`'s and
every subsequent `PI-####` authorization's own authorization-precedes-research separation already
established.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/AVGO.yaml`
   / `.md`, `AMD.yaml` / `.md`, `MRVL.yaml` / `.md`, `INTC.yaml` / `.md` — using the existing
   repository schema frozen by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated
   provisions, with the human approvals every prior first-coverage record has required
   (`portfolio_role_ref` — descriptive only, `conviction.rating` from `PI-0004`'s closed
   four-value vocabulary, conviction rationale, review cadence, thesis/risks/catalysts, and
   source-access disclosure).
2. Create exactly **one hand-authored four-company batch comparison artifact**, at
   `intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md` — the filename chosen to mirror
   this repository's existing convention (`intelligence/BATCH1_SEMIS_EQUIPMENT_COMPARISON.md`,
   `intelligence/BATCH2_MEMORY_COMPARISON.md`: `BATCH<N>_<SUBJECT>_COMPARISON.md`, uppercase,
   underscore-separated, directly under `intelligence/`), naming this batch's coherent theme —
   semiconductor compute, accelerated computing, networking, and connectivity — per §C below.
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per
   §B.17 below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention
   (mirroring `PI-0011`/`AUTO-0002`/`PI-0023`/`PI-0024`'s own narrow, single-purpose additions).
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0025`, `company_record_authority:
   PI-0025`) — matching the existing pattern for the thirteen currently-enrolled tickers, and
   matching both files' own stated convention that a row requires "its own existing, cited Company
   Intelligence record" and is added only through a human-reviewed PR, never by automation. No
   `monitoring_enabled` row may be set `true` by that PR.
7. Perform **only the minimum factual** `operations/WORKSTREAMS.yaml` synchronization required by
   repository convention for WS-0005's Milestone 3 gate (status, `pr`, `date`) once that
   implementation PR merges — not before, and not by this filing.

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (per company)

The implementation PR's research, for each of AVGO, AMD, MRVL, and INTC individually, must
establish, at minimum:

1. Economic function and governed portfolio role.
2. Business model and principal revenue/profit drivers.
3. Current governed tier and target, **clearly labeled as historical policy, not research
   evidence** — per `OPS-0006` §2/§3, preserved for later reconciliation, never treated as
   presumptively correct or cited as support for a research conclusion.
4. Financial quality and semiconductor-cycle sensitivity.
5. Management and capital allocation.
6. Key risks and actively searched disconfirming evidence.
7. Explicit thesis-break conditions.
8. What portfolio exposure would be lost if the company were absent.
9. How the company differs from and overlaps with the other three companies in this batch.
10. **Margin-relevance evidence, factual and advisory only** — no borrowing, leverage,
    deployment-timing, or margin-ceiling recommendation of any kind, matching `OPS-0006` §4
    Milestone 3's own margin-relevant-evidence requirement and `PI-0023` §B.16 / `PI-0024` §B.16
    exactly.
11. **Unauthorized external opportunity or replacement leads** — identify credible non-owned
    competitors, substitutes, or missing-system candidates revealed by the research, recorded only
    as future leads, matching `PI-0023` §B.17 / `PI-0024` §B.18 exactly: no holding add, no
    `holdings.yaml` change, no tier/target assignment, no mechanical ranking, no batch expansion,
    and no research on an outside candidate without its own separate future authorization.
12. Evidence-driven freshness and refresh profile per §"Refresh and monitoring requirements" below.

In addition to the above, the research must specifically cover, per company:

**AVGO (Broadcom):**
- Semiconductor versus infrastructure-software segment economics.
- Custom AI accelerators (XPU/ASIC programs) and AI networking-silicon exposure.
- Hyperscaler and customer concentration.
- VMware integration, acquisition-related debt, deleveraging trajectory, and recurring-software
  economics.
- Acquisition dependence and integration risk (VMware and prior acquisitions).
- Semiconductor cyclicality and export-control exposure.
- Foundry and advanced-packaging dependencies.
- Margin-relevant balance-sheet, gap-risk, and correlated-loss evidence.

**AMD (Advanced Micro Devices):**
- Data-center CPU and accelerator (GPU/AI) positioning.
- Competition with NVIDIA and Intel across CPU and accelerator lines.
- Hyperscaler and enterprise demand drivers.
- Product-roadmap execution track record.
- TSMC and advanced-packaging dependence.
- Gaming and embedded-segment cyclicality.
- Export controls and China exposure.
- Margin-relevant drawdown, concentration, funding, and execution risks.

**MRVL (Marvell Technology):**
- Data-center networking, optical, interconnect, switching, and custom-silicon exposure.
- Hyperscaler and customer concentration.
- Dependence on AI-infrastructure buildout demand.
- Legacy carrier, enterprise, storage, and consumer-segment cyclicality.
- Foundry, packaging, and supplier dependencies.
- Design-win timing and revenue-conversion uncertainty.
- Balance-sheet condition and acquisition history.
- Margin-relevant liquidity, gap-risk, and correlated-loss evidence.

**INTC (Intel):**
- Client and server CPU competitive position.
- Intel Foundry strategy and external-customer credibility.
- Manufacturing roadmap and process-node execution.
- Capital intensity, government subsidies, restructuring, liquidity, and funding needs.
- Competitive pressure from AMD, ARM-based architectures, and TSMC-manufactured competitor
  products.
- Geopolitical and domestic-manufacturing relevance.
- `PI-0014`'s prior conversational overlap work as **context only** — it is not a filed Company
  Intelligence record and must never be treated as, cited as, or substituted for one.
- Margin-relevant turnaround, execution, refinancing, gap-risk, and prolonged-recovery evidence.

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/BATCH3_SEMIS_COMPUTE_CONNECTIVITY_COMPARISON.md`)
must explicitly distinguish, across AVGO, AMD, MRVL, and INTC:

1. CPU, GPU/accelerator, networking, custom-silicon, software, and foundry exposure — per company.
2. Fabless versus IDM (integrated device manufacturer) economics.
3. Recurring-software versus semiconductor-cycle economics (AVGO's infrastructure-software segment
   versus the other three's pure-semiconductor economics).
4. TSMC and advanced-packaging dependence — per company, including INTC's dual role as both an
   external-foundry customer (for some products) and an aspiring foundry competitor.
5. Hyperscaler and customer concentration — per company.
6. Acquisition and integration dependence (AVGO/VMware most directly; noted for the others where
   applicable).
7. AI-infrastructure opportunity exposure versus shared AI-capex-cycle risk (the risk that all four
   are exposed to the same AI-capex cycle turning, not merely to its upside).
8. China/export-control and broader geopolitical exposure — per company.
9. Capital intensity and balance-sheet resilience — per company, with particular attention to
   INTC's capital-intensive foundry buildout versus the fabless economics of AMD/MRVL and AVGO's
   semiconductor segment.
10. Duplicated portfolio exposure among the four (and, where evidence supports it, against the
    Batch 1/Batch 2 companies already covered in the `semis` cluster).
11. Structural/economic overlap kept explicitly distinct from measured historical price
    correlation — per `OPS-0006` §4 Milestone 4's own distinction, which this batch's evidence must
    respect even though Milestone 4 itself remains unauthorized.
12. Company-specific and common margin-risk amplifiers across the batch.

**The comparison artifact must remain analytical and advisory only. It must not rank the four
companies for capital deployment, and must not recommend a buy, trim, target, tier, margin use, or
portfolio weight of any kind — matching `PI-0024` §C, whose comparison-artifact section states this
same no-ranking rule; `PI-0023` does not have a directly corresponding §C (its §C is "Zero-based
discipline"), but carries the same no-ranking prohibition in §F ("no next-best-alternative
*ranking*") and the same relationship-evidence requirement in §B.12.**

### D. Evidence and access discipline

Require: primary sources for changeable facts; claim-level evidence; explicit separation of fact,
inference, uncertainty, judgment, source type, and actual inspection/access status (the same
standard `PI-0016` §D, `PI-0023` §D, and `PI-0024` §D already apply, adopted here by reference for
its evidentiary discipline only — this batch is first-coverage record creation, not a `PI-0016`
committee review of existing conviction, since none of the four companies has an existing record or
rating to review); active search for and preservation of disconfirming evidence and null/negative
findings; no unsupported search-result snippet presented as inspected primary evidence; no silent
inheritance of an earlier chat conclusion (including `PI-0014`'s INTC conversational context, see
§B) without independent verification.

**Required direct-inspection attempts, per company, where applicable:**

- Annual reports (Form 10-K) and quarterly reports (Form 10-Q).
- Earnings releases and official earnings-call materials (transcripts or webcast materials).
- Investor presentations and investor-day materials.
- Debt and credit-rating disclosures (AVGO's VMware-related debt load and deleveraging in
  particular; INTC's liquidity and funding disclosures in particular).
- Acquisition-related filings (AVGO/VMware in particular; MRVL's acquisition history).
- Export-control or other regulatory documents.
- Official manufacturing/foundry disclosures (INTC's Intel Foundry disclosures in particular; TSMC
  dependence disclosures for AMD/MRVL/AVGO).

**A blocked primary source must be:**

- Identified precisely (the specific document and URL or filing reference attempted).
- Labeled explicitly as "attempted but not directly inspected."
- Kept separate from WebSearch-derived or other secondary evidence, never merged into the same
  citation as if both were equally verified.
- Never described as directly verified.

**No silent scope contraction is permitted because a source is blocked.** If evidence is
insufficient for any one of the four companies under this standard, the future implementation must
stop, disclose the specific evidence-access problem, and return for explicit principal direction —
it may not silently drop that company, complete only a subset of the batch and call the batch done,
or treat tool failure as license to change what this decision authorizes. This mirrors `PI-0024`
§F's "no automatic contraction" rule exactly, extended here from a two-company to a four-company
batch: the authorized batch is exactly AVGO, AMD, MRVL, and INTC — not any three of them, not any
two, not any one.

Require explicit separation, throughout every record and the comparison artifact, between:
directly inspected primary evidence; primary evidence identified but not opened; secondary
evidence; conflicting or single-source claims; AI-reasoned interpretation; and unresolved evidence
gaps.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business change,
thesis uncertainty, cyclicality, customer concentration, product-roadmap risk, capital intensity,
regulatory/export sensitivity, acquisition or restructuring state, and event/gap risk. **No
universal cadence is imposed by this decision, and none may be imposed automatically by the
implementation.**

Each record should define named review triggers where supported by evidence, drawn from — but not
limited to — `OPS-0006` §12's candidate-trigger list as applied selectively (not every listed
trigger applies to every company): earnings or guidance changes; customer-concentration
disclosures; major custom-silicon or accelerator awards or losses; product-roadmap delays;
foundry-node or yield changes; material acquisition or integration developments (AVGO's VMware
integration in particular); credit-rating, debt, liquidity, or capital-spending changes (INTC's
funding and subsidy status in particular); export-control or subsidy developments; and major
market-share changes.

### F. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before
comparing them with current governed tier/role/target/cluster placement; preserve that placement as
the historical baseline for later reconciliation only (§B.3 above); never treat it as proof of a
research conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7; and
record any disagreement between researched conclusion and governed baseline without changing
policy.

### G. Hard prohibitions

This decision and any later implementation authorize none of the following, under any
interpretation:

- Any change to AVGO/AMD/MRVL/INTC's (or any other ticker's) holdings, targets, tiers, roles,
  clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or
  against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way — Company Intelligence
  remains advisory-only, per the unchanged `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` boundary.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C).
- Any research or Company Intelligence record for a fifth company, or for WDC, SNDK, or any other
  ticker not named AVGO, AMD, MRVL, or INTC.
- Correcting `targets.yaml`'s stale MU/WDC `semis`-cluster comment or the stale BTC comment
  identified elsewhere in `operations/WORKSTREAMS.yaml`'s WS-0005 entry.
- Modifying any existing Company or Theme Intelligence record (AMAT, ASML, COST, GEV, ISRG, KLAC,
  LRCX, MU, NVDA, SKHY, TMO, TSM, XOM, `ai_infrastructure`, `life_sciences_tools_medtech`).
- Silently importing existing tiers or targets as research conclusions.
- Automatic authorization of a fourth Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 3 does not authorize Batch 4 or Milestone 4.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.

### H. Governance package (this filing)

This decision's own implementation — the governance PR itself, not the future research PR — touches
exactly:

1. This decision file, `governance/decisions/PI-0025-ws0005-milestone3-batch3-compute-networking.md`.
2. `governance/decisions.yaml` (index regeneration: one new entry for `PI-0025`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization,
   using only `OPS-0001`'s existing 21-field schema and existing status vocabulary — no new field,
   no new status value). Milestones 1-2 and Milestone 3 Batch 1/Batch 2 entries remain exactly as
   prior filings left them; Milestone 3 remains `status: in_progress` for the milestone as a whole
   (this batch's authorization does not make Milestone 3 `complete` in aggregate); Milestones 4-9
   remain `status: proposed`, unauthorized, unchanged; `next_action` states the next step is exactly
   one bounded research implementation PR for this batch — not a fourth batch, not Milestone 4;
   `evidence_refs` gains a reference to this decision; no unrelated workstream priority or authority
   field changes — WS-0005 remains the sole `priority: primary` workstream, WS-0001/WS-0002/WS-0003/
   WS-0004 priorities untouched.
4. The applicable `CLAUDE.md` Decisions Log entry recording this acceptance.

**No other file is touched by this governance filing.** No Company Intelligence record, no
comparison artifact, no freshness-registry or freshness-checkpoint row, and no test or validator
file is created, modified, or authorized to be created by this filing — those belong exclusively to
the later, separate implementation PR authorized in §A.

### I. Effectiveness, review, and merge gates

- **This authorization becomes effective only when this governance PR merges to `main`.** Before
  that, nothing in §A is authorized to begin.
- **The later Company Intelligence implementation must occur in its own separate, bounded PR** —
  never combined with this governance filing, and never opened before this filing merges.
- **That implementation PR must remain in draft state until it has been independently reviewed** —
  it may not be marked ready for review, and must not be merged, before an independent Fable review
  is retained.
- **An independent Fable review must be retained and anchored to the exact implementation PR head**
  that ultimately merges — per the retained-artifact convention `OPS-0004` established and every
  subsequent `PI-####` batch has followed; a review anchored only to an intermediate commit does not
  satisfy this gate.
- **Any material finding from that review requires a bounded correction and an exact-head
  re-review** before the PR may be considered ready — following `PI-0024` §I, which states this
  exact mechanism (at most one bounded correction pass per round, followed by re-verification at
  the corrected exact head). `PI-0023` §E does not itself state this specific correction-pass
  mechanism; it is cited elsewhere in this decision only for its broader independent-review-and-
  completion discipline, not for this mechanism.
- **Principal acceptance is required before merge** — explicit, at the exact head being merged, not
  inferred from silence or from an earlier round's acceptance of a different head.
- **Post-merge verification and factual `operations/WORKSTREAMS.yaml` synchronization are required**
  after that implementation PR merges — ancestry, merge scope, validator, and test re-verification
  on a clean checkout of the merged state, followed by a factual (not aspirational) register update,
  matching the discipline `PI-0023`/`PI-0024`'s own implementations and post-merge syncs already
  established.
- **Completion of this batch does not authorize a fourth Milestone 3 batch or any Milestone 4
  work.** Each requires its own separate, later, explicit principal authorization, exactly as
  `PI-0023` §E and `PI-0024` §I already state for their own batches.

This governance PR itself (the one implementing this decision) is subject to the same discipline:
it must remain in draft state, gain its own independent Fable review anchored to its exact head, and
receive explicit principal acceptance before it may be marked ready or merged. This decision does
not mark itself, or authorize marking itself, ready for merge.

## Rationale

**Why a batch, and why these four.** `OPS-0006` §4 Milestone 3 explicitly contemplates "coherent
batches" rather than single-company filings, and this repository has direct precedent for
multi-company Intelligence authorizations (`PI-0007`, `PI-0009`, `PI-0023`, `PI-0024`). AVGO, AMD,
MRVL, and INTC are not an arbitrary four-name slice of the `semis` cluster's remaining uncovered
members — `PI-0023`'s own Alternatives Considered section already distinguished "chip design[ers]"
(AVGO, AMD as accelerator/CPU designers, MRVL as networking/custom-silicon designer) and INTC's
foundry-adjacent role from the equipment sub-segment (ASML/AMAT/KLAC/LRCX, Batch 1) and the memory
sub-segment (MU/SKHY, Batch 2) it authorized instead. This batch completes that third natural
sub-segment: compute (CPU/GPU/accelerator design and, for INTC, integrated manufacture),
accelerated computing and custom silicon, data-center networking/connectivity, and (for AVGO and
INTC specifically) infrastructure-software and foundry economics that sit outside pure fabless chip
design. The four share a genuinely comparable driver set — exposure to the AI-infrastructure capex
cycle, TSMC/advanced-packaging dependence (INTC as a partial exception, pursuing its own foundry),
hyperscaler customer concentration, and export-control exposure — while their business models are
deliberately preserved as materially distinct (fabless designer vs. IDM-with-foundry-ambitions vs.
diversified semiconductor-plus-software conglomerate), which is exactly the kind of comparative,
non-duplicative evidence §B.9/§C requires and a single-company or randomly-grouped authorization
could not produce as coherently.

**Why `PI-0025`, not a new `OPS-####` or a reuse of `PI-0023`/`PI-0024`.** Same category and
reasoning as `PI-0023`/`PI-0024`: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), not workstream-register mechanics, so it is filed in the
`PI-####` series per `governance/decisions/README.md`'s convention. `PI-0023` and `PI-0024` are both
`status: Accepted` and, per that same convention, are never edited after acceptance for anything
beyond a narrow dated correction — a third batch requires its own new decision file. `PI-0025` is
confirmed as the next unused number, checked live against both `governance/decisions/` and
`governance/decisions.yaml` at this filing's base commit, not assumed.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical reasoning
to `PI-0023`/`PI-0024`: `PI-0016`'s standing methodology governs review of an *existing* Company
Intelligence record's conviction and capital-priority standing; none of AVGO, AMD, MRVL, or INTC has
an existing record, so this batch is first-coverage record creation, structurally identical in kind
to `PI-0003`, `PI-0005`, `PI-0007`, `PI-0009`, `PI-0023`, and `PI-0024` — not a `PI-0016` review.
This decision adopts `PI-0016` §D's evidence standard by reference for its evidentiary discipline
only, exactly as `PI-0023`/`PI-0024` did. `PI-0014`'s prior bounded, conversation-only INTC evidence
review is explicitly not a substitute for a filed record — see §B and §D.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR, not
accompany it — the same separation `PI-0013`'s, `PI-0023`'s, and `PI-0024`'s own rationale already
established, and the principal's own explicit instruction for this filing: authorize the package
now, gate the research implementation on this decision's independent review, principal acceptance,
and merge.

## Alternatives Considered

- **Authorize fewer than four companies now, deferring the rest to later batches** (e.g. AVGO+AMD
  only, or AVGO+AMD+MRVL only). Rejected — the principal's authorization is explicit that the batch
  is exactly AVGO, AMD, MRVL, and INTC together, and the batch's own justification (a coherent
  compute/accelerated-computing/networking/custom-silicon/foundry comparison set with deliberately
  distinct business models) rests on comparative evidence a smaller grouping would weaken, the same
  reasoning `PI-0024` applied when rejecting an MU-alone authorization.
- **Include additional uncovered `semis` members (e.g. WDC, SNDK) in this batch.** Rejected — WDC's
  current HDD-storage business is outside this batch's compute/networking/accelerated-computing
  theme entirely (and was already excluded from Batch 2 on separate, still-valid grounds); adding it
  or any other name would exceed the principal's explicit four-company authorization.
- **Adopt `PI-0016`'s full committee-review framework for this batch.** Rejected — same reasoning as
  `PI-0023`/`PI-0024`: `PI-0016` presumes an existing record and conviction rating to reassess, which
  none of these four companies has.
- **File under a new `OPS-####` number.** Rejected — same reasoning as `PI-0023`/`PI-0024`: this is
  Company Intelligence research-authorization content, not workstream-register mechanics.
- **Let this filing itself begin the research, or authorize the implementation PR to open
  immediately (non-draft) on this decision's merge.** Rejected — the principal's explicit
  instruction, and `OPS-0006` §5's existing discipline, requires the authorization to be
  independently reviewed and merged first, and requires the later implementation PR to remain draft
  until its own independent review and principal acceptance — mirroring the gate structure
  `PI-0023`/`PI-0024` each already used for their own implementation PRs.
- **Update `intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml` in this governance
  PR.** Rejected — both files gain a row only for a ticker with "its own existing, cited Company
  Intelligence record," which does not yet exist for any of the four; adding rows belongs in the
  future implementation PR, exactly as `PI-0023`/`PI-0024` reasoned for their own batches.
- **Authorize a fourth Milestone 3 batch or begin Milestone 4 relationship mapping in this same
  filing**, since candidate names and relationship questions are already visible in
  `operations/WORKSTREAMS.yaml`. Rejected — exceeds the principal's authorization, which names
  exactly AVGO, AMD, MRVL, and INTC for Batch 3 only; any further batch or Milestone 4 work requires
  its own future, separate authorization.
- **Correct `targets.yaml`'s stale MU/WDC or BTC comments in this same filing.** Rejected — outside
  this decision's authorized scope, and the principal's instruction is explicit that no such
  correction is authorized here; it remains a separate, unauthorized, future factual-reconciliation
  item, exactly as `PI-0024` §E left it.

## Consequences

**Authorized, effective on this decision's merge:** exactly one third Milestone 3 research batch
(AVGO, AMD, MRVL, INTC), scoped and bounded exactly as stated in §§A-I above, to proceed via its own
later, separate, bounded, draft-until-independently-reviewed implementation PR.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (AMAT, ASML, COST,
GEV, ISRG, KLAC, LRCX, MU, NVDA, SKHY, TMO, TSM, XOM, `ai_infrastructure`,
`life_sciences_tools_medtech`); `allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, every freshness module, and every test file; the 1.8x leverage cap and 30%
buffer floor; `MARGIN-0005`'s research charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, and `constitution/INVESTMENT_CONSTITUTION.md`. `targets.yaml`'s stale
MU/WDC cluster comment and the stale BTC comment remain identified but uncorrected. Milestones 4
through 9 of WS-0005 remain entirely unauthorized. No fourth Milestone 3 batch is authorized by this
filing, and none is inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future, separately
implemented, draft-until-independently-reviewed research PR may begin exactly the batch scoped
above only after this decision itself merges; any resulting Company Intelligence record, comparison
artifact, freshness-registry update, or later policy consequence remains subject to that PR's own
independent review, principal acceptance, validation, and (for anything beyond Intelligence content)
its own separate future governance decision. If that future session cannot obtain sufficient primary
evidence for any one of the four companies, it must stop, disclose the evidence-access problem, and
return for explicit principal amendment — it may not narrow this batch on its own authority.
