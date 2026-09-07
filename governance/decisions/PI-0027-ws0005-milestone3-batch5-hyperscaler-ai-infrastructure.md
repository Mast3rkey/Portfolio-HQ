---
decision_id: PI-0027
date: 2026-07-26
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, PI-0007, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, AUTO-0001]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1-2 to execute; Milestone 3
proceeds batch-by-batch, each requiring its own separate, later, explicit principal authorization
(`OPS-0006` §5). Four batches are complete: `PI-0023` (ASML, AMAT, KLAC, LRCX — semis capital
equipment), `PI-0024` (MU, SKHY — memory), `PI-0025` (AVGO, AMD, MRVL, INTC — compute/networking/
foundry), and `PI-0026` (ETN, VRT, PWR — power infrastructure). All four covered members of the
governed `semis` or `power_infra` correlated-cluster caps. **No prior batch has covered any T1 or T2
holding outside those two clusters.**

A separate, explicitly bounded proposal-only session (this repository's WS-0005 Research Wave
Protocol design and zero-based Batch 5 scope review) independently re-derived the current coverage
state directly from `targets.yaml`, `holdings.yaml`, and `intelligence/companies/`, cross-checked
against the retained `operations/provisional/WS0005_COVERAGE_GAP_REGISTER_20260726.md`: of 62
governed operating companies, 20 carry a qualifying record (13 ACCEPTED, 7 PROVISIONAL — the Batch 3
and Batch 4 additions), 42 do not. Of the 5 uncovered T1 holdings (MSFT, GOOGL, META, LLY, V), the
retained coverage-gap register itself independently flags MSFT, GOOGL, and META with the register's
own highest disclosed materiality rating — each is named, by ticker, as a "Yes — could materially
affect a future scenario result" row, and each is separately cited as a still-unverified named
counterparty inside the Batch 1/2/3 comparison artifacts and company records already merged to
`main` (Batch 1/3 records cite MSFT/GOOGL/META/AMZN as hyperscaler customers of the covered
semis-cluster names without any of the four's own economics having been independently researched).

CLAUDE.md's own Decisions Log records, under "T1 AI-infra cluster cap: scanned and declined," that a
one-time correlation scan of a 7-name AI-infrastructure subset (ASML, TSM, NVDA, MSFT, GOOGL, META,
GEV) found only 0.302-0.373 average pairwise correlation — too diffuse for a correlation-based
cluster cap, and explicitly declined on that basis — but that entry also states the underlying T1
concentration (42.1% of book against a 30.15% target at scan time) was real, just not
cluster-cap-shaped, and separately identifies that T1/T2 had no trim rule at all at the time (later
addressed by the T1/T2 concentration ceiling, a separate doctrine decision). Of that 7-name group,
**4 already carry Company Intelligence coverage (ASML, TSM, NVDA, GEV); MSFT, GOOGL, and META do
not.** No governance decision has ever authorized research on any of the three.

The principal reviewed a five-candidate Batch 5 comparison (pharma; the three uncovered
AI-infra names alone; the three plus AMZN and EQIX; enterprise software; the three-name safety
fallback) and, following GPT-5.6 Thinking's independent review, approved a fourth variant: **exactly
MSFT, GOOGL, META, and AMZN — deferring EQIX.** EQIX's REIT legal and disclosure structure (a
different SEC filing shape, different economics — funds from operations, tenant/lease
concentration, dividend-distribution mechanics — than an operating company) is untested anywhere in
this repository's Intelligence coverage; deferring it keeps this batch to four companies sharing a
single, already-proven-workable operating-company disclosure shape, while preserving EQIX as a
named, explicit candidate for its own future batch rather than silently dropping it.

**Preflight for this filing** (independently verified, not assumed): `origin/main` fetched and
pruned; local and remote `main` identical at `1aba3e74d3847aa278b774f3b0956c786b6ee480` (PR #167's
merge commit, confirmed merged via the GitHub API, `merged_at: 2026-07-26T18:42:15Z`); zero open
pull requests exist; working tree clean; `governance/decisions.yaml` carries exactly 36 entries
before this filing, highest `PI-####` is `PI-0026` — confirming `PI-0027` as the next unused number
in its series. `intelligence/companies/` independently confirmed to hold no MSFT, GOOGL, META, or
AMZN record (17 non-batch-5 tickers plus AMAT, AMD, ASML, AVGO, COST, ETN, GEV, INTC, ISRG, KLAC,
LRCX, MRVL, MU, PWR, SKHY, TMO, TSM, VRT, XOM = 20 files, `intelligence_validator.py` confirms all 20
valid). `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` carry no
row for any of the four. No branch or open PR references MSFT, GOOGL, META, AMZN, "batch5," or
"batch-5" beyond this filing's own branch.

The principal has explicitly authorized preparation of a fifth Milestone 3 batch covering **exactly
MSFT, GOOGL, META, and AMZN**, under the Research Wave Protocol v1 adopted in `OPS-0008` (filed in
the same governance PR as this decision). This decision records that authorization; it does not
itself perform any research.

## Decision

**PI-0027 authorizes exactly one thing: the fifth bounded WS-0005 Milestone 3 research batch,
covering MSFT, GOOGL, META, and AMZN, and nothing else.** This is **evidence development only** — no
research has been performed, and this filing alone authorizes no research finding, Company
Intelligence record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, trade, or order.
**This filing (its own governance PR) authorizes the creation of the governance-authorization
package only** — this `PI-0027` decision file, `OPS-0008` (filed alongside it), `governance/
decisions.yaml`, `operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log entries.
It does not authorize drafting any MSFT, GOOGL, META, or AMZN Company Intelligence record or the
comparison artifact — those become authorized to begin only after this governance decision is
independently reviewed, principal-accepted, and merged, exactly as `PI-0023`-`PI-0026`'s own
authorization-precedes-research separation already established.

**This batch adopts `OPS-0008`'s Research Wave Protocol v1 by reference for lifecycle, review
standard, and the source-readiness gate** — not restated in full here. In particular: the future
implementation PR must apply `OPS-0008` §2's mandatory stop-before-drafting primary-source gate for
each of the four companies before drafting substantive economic content, using the standing
evidence-recovery pre-authorization if primary access is blocked; and the future implementation PR is
expected to follow `OPS-0008` §4's default two-PR lifecycle (this authorization PR, then one
implementation PR carrying its full review cycle), with post-merge verification recorded per §4's
read-only default rather than through a dedicated third reconciliation PR, absent a genuine material
discrepancy.

**EQIX is explicitly deferred, not included, and not silently folded into a future batch by this
decision** — any future EQIX research requires its own separate, later, explicit authorization
naming it.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/
   MSFT.yaml`/`.md`, `GOOGL.yaml`/`.md`, `META.yaml`/`.md`, `AMZN.yaml`/`.md` — using the existing
   repository schema frozen by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated
   provisions, with the human approvals every prior first-coverage record has required
   (`portfolio_role_ref` — descriptive only; `conviction.rating` from `PI-0004`'s closed four-value
   vocabulary; conviction rationale; review cadence; thesis/risks/catalysts; source-access
   disclosure).
2. Create exactly **one hand-authored batch comparison artifact**, at `intelligence/
   BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md` (mirroring the existing
   `BATCH<N>_<SUBJECT>_COMPARISON.md` convention), naming this batch's coherent theme — the
   hyperscale AI/cloud-infrastructure demand chain — per §C below.
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per §E
   below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention.
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0027`, `company_record_authority:
   PI-0027`).
7. Perform the minimum factual `operations/WORKSTREAMS.yaml` synchronization required once that
   implementation PR merges, per `OPS-0008` §4's read-only-by-default post-merge convention — not
   before, and not by this filing.

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (per company)

The implementation PR's research, for each of MSFT, GOOGL, META, and AMZN individually, must
establish, at minimum:

1. Economic function and current governed portfolio role.
2. Business model and material revenue drivers, by segment.
3. Cloud-infrastructure economics specifically (Azure for MSFT, Google Cloud/GCP for GOOGL, AWS for
   AMZN) — margin contribution, growth trajectory, capital intensity — and, for META, the absence of
   a public cloud-resale business alongside its own hyperscale AI/data-center capital expenditure for
   internal use (ad-ranking, Llama/AI-model training, Reality Labs).
4. AI-capital-expenditure trajectory and funding source (operating cash flow versus debt-financed
   capex) for each company.
5. Custom AI-silicon strategy where applicable (GOOGL's TPU program, AMZN's Trainium/Inferentia
   programs) and dependency on external chip suppliers.
6. Advertising, retail, subscription, and enterprise-software revenue concentration as applicable.
7. Customers, suppliers, competitors, and substitutes, including the four companies' competitive and
   customer relationships with each other.
8. Antitrust and regulatory exposure — each of the four carries live or recent antitrust, ad-tech, or
   platform-regulation matters; these must be researched as current fact, not assumed or omitted.
9. Financial quality, margins, free cash flow, and capital-allocation history.
10. Balance-sheet resilience and downturn behavior.
11. Management claims versus independently supported facts.
12. Actively searched disconfirming evidence.
13. Explicit thesis-break conditions.
14. What portfolio exposure would be lost if the company were absent.
15. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3. (MSFT, GOOGL, META: T1, 3.35% target each. AMZN: T2,
    1.65% target.) None of the four is a member of any `targets.yaml` correlated-cluster cap.
16. **Margin-relevance evidence, factual and advisory only** — cyclicality; liquidity; leverage;
    balance-sheet sensitivity; refinancing/funding risk; drawdown and recovery characteristics;
    correlated-loss behavior — with no recommendation to borrow, no safe-leverage calculation, and no
    deployment-timing or margin-ceiling conclusion of any kind.
17. Evidence-driven freshness cadence and refresh triggers per §E below.
18. **External opportunities or replacements only as unauthorized future leads** — advisory candidate
    list only, no holding add, no tier/target assignment, no mechanical ranking, no batch expansion,
    no research on an outside candidate without its own separate future authorization.
19. **Company-specific requirement — MSFT:** Azure growth and margin disclosures; the OpenAI
    partnership and investment structure (equity stake, compute-purchase commitments, revenue-sharing
    terms as disclosed); enterprise-software (Microsoft 365, Dynamics) concentration; antitrust
    history and current exposure.
20. **Company-specific requirement — GOOGL:** Google Cloud/GCP segment disclosures; TPU and custom-
    silicon strategy; advertising-revenue concentration and dependency; the DOJ/state antitrust
    litigation history and current status; Gemini/AI-model investment and monetization.
21. **Company-specific requirement — META:** the absence of a public-cloud-resale business,
    contrasted explicitly with MSFT/GOOGL/AMZN; advertising-revenue concentration; AI-infrastructure
    capital-expenditure trajectory for internal model training and ad-ranking; Reality Labs
    investment and losses; antitrust and platform-regulation exposure.
22. **Company-specific requirement — AMZN:** AWS segment economics (margin contribution versus the
    retail/logistics segments); Trainium/Inferentia custom-silicon strategy; named, in Batch 1/3
    records, as a hyperscaler customer of already-covered semis-cluster companies without AMZN's own
    economics ever having been independently verified — that specific cross-reference must be
    addressed; antitrust exposure (FTC litigation and related matters).
23. **Capital-priority comparison, explicitly separated from business quality** (added following an
    independent exact-head review that found this requirement ambiguous in the original text). For
    each of MSFT, GOOGL, META, and AMZN individually, the research must: separate an assessment of
    business quality (competitive position, moat, financial strength — items 1-16 above) from a
    distinct assessment of capital priority (whether the next investment dollar is better spent on
    this company than on a governed alternative); compare the company against the next-best use of
    capital among this repository's other governed holdings in `targets.yaml`; state explicitly, in
    addition to item 14's exposure-if-absent requirement, why the next investment dollar might or
    might not favor this company relative to those alternatives; and identify redundancy,
    substitutes, and duplicated exposure with other governed holdings, extending item 7's
    customer/supplier/competitor/substitute analysis to a capital-priority lens specifically. **This
    comparison must preserve uncertainty and judgment in prose and must not produce a numerical
    score, a composite index, or an automatic ranking of any kind** — consistent with §G's existing
    prohibition on any ranking or composite score. It remains advisory research evidence only: it
    recommends no trade, and it does not itself change any tier, target, allocation, or policy.

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/
BATCH5_HYPERSCALER_AI_INFRASTRUCTURE_COMPARISON.md`) must explicitly distinguish, across MSFT, GOOGL,
META, and AMZN:

1. Public-cloud sellers (MSFT/GOOGL/AMZN) versus AI-capex-only buyer with no public-cloud-resale
   business (META) — a materially different economic structure that must not be flattened into "Big
   Tech" as a single category.
2. Each company's AI-capital-expenditure funding source and trajectory, and whether that spending is
   growing faster than, in line with, or slower than disclosed revenue growth in the relevant segment.
3. Custom-silicon strategy and dependency on external chip suppliers, per company, and cross-reference
   against the already-covered semis-cluster companies (NVDA, TSM, AVGO, AMD, MRVL, ASML, AMAT, KLAC,
   LRCX, MU, SKHY) as customers/counterparties, distinguishing structural overlap from measured price
   correlation, per `OPS-0006` §4 Milestone 4's own distinction (which this batch's evidence must
   respect even though Milestone 4 itself remains unauthorized).
4. Antitrust and regulatory exposure, per company, and whether that exposure is correlated across the
   four (a shared regulatory-environment risk) or company-specific.
5. Advertising-revenue, cloud-revenue, retail-revenue, and enterprise-software-revenue concentration,
   per company.
6. Common macro and spending-cycle dependencies across the four (AI-capex supercycle, interest-rate
   sensitivity, hyperscaler capital-spending guidance revisions).
7. Genuine diversification versus duplicated exposure among the four, and against every already-
   covered supply-side semis-cluster name.
8. Whether completing MSFT/GOOGL/META closes the CLAUDE.md-documented "7-of-9 T1 AI-infra names"
   concentration finding's own Company Intelligence coverage gap (4 of 7 covered pre-batch: ASML, TSM,
   NVDA, GEV; +3 T1 names here = 7 of 7 covered) — **an advisory research observation only, with no
   automatic effect on any tier, target, or cluster.** Any actual policy consequence of that
   observation requires its own separate, later, explicit governance decision.
9. Common correlated-loss mechanisms across the batch and against the already-covered semis-cluster
   names.
10. **A capital-priority comparison across all four companies** (added following an independent
    exact-head review), addressing the same business-quality-versus-capital-priority separation and
    next-best-use-of-capital discussion required per §B.23 individually, but at the batch level:
    whether the four companies, taken together, compete for capital against each other or against
    other already-covered governed holdings; where redundancy or duplicated capital-priority
    reasoning exists among them; and why the next investment dollar might or might not favor one of
    the four over another or over an already-covered alternative. **Presented as advisory prose and
    uncertainty-preserving judgment only — never as a score, index, or ranking**, consistent with
    §B.23 and §G.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically score
or rank the four companies, must not declare a preferred holding, must not alter a tier, target, role,
cluster, or cap, must not recommend a trade, must not recommend margin, and must not control
allocator output.

### D. Evidence and access discipline

Require: primary sources for changeable facts; claim-level evidence; explicit separation of fact,
inference, uncertainty, judgment, source type, and actual inspection/access status; active search for
and preservation of disconfirming evidence and null/negative findings; no unsupported search-result
snippet presented as inspected primary evidence; no silent inheritance of an earlier chat conclusion
without independent verification.

**`OPS-0008` §2 applies to this batch without modification**: before drafting any company's
substantive economic content, the implementation PR must attempt direct primary-source inspection
(SEC Form 10-K/10-Q/8-K; official earnings releases and call materials; official investor
presentations) for each of the four companies and produce a source-access manifest. **If access is
blocked for one or more companies, the implementing session must stop drafting those companies'
records before writing substantive content** and may engage an eligible independent reviewer's
primary-source evidence-recovery audit per `OPS-0008` §2's standing pre-authorization before resuming.
If even that recovery pass cannot establish sufficient primary evidence for any one of the four, the
implementation must try reasonable official alternatives, then stop, disclose exactly what failed, and
return for explicit principal direction — it may not silently narrow, substitute, or declare the
record complete. The authorized batch is exactly MSFT, GOOGL, META, and AMZN — not any three of them.

**A blocked primary source must be** identified precisely, labeled explicitly as "attempted but not
directly inspected," and kept separate from WebSearch-derived or other secondary evidence — never
merged into the same citation as if both were equally verified.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business change,
thesis uncertainty, cyclicality, regulatory exposure, and event/gap risk. **No universal cadence is
imposed by this decision, and none may be imposed automatically by the implementation.** Candidate
review triggers, drawn from — but not limited to — `OPS-0006` §12's list as applied selectively:
earnings or guidance changes; antitrust rulings, settlements, or major litigation developments;
material AI-capex guidance revisions; major cloud-segment disclosures; custom-silicon program
milestones; major M&A.

### F. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before comparing
them with current governed tier/role/target placement; preserve that placement as the historical
baseline for later reconciliation only (§B.15 above); never treat it as proof of a research
conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7; and record any
disagreement between researched conclusion and governed baseline without changing policy.

### G. Hard prohibitions

This decision and any later implementation authorize none of the following, under any interpretation:

- Any change to MSFT/GOOGL/META/AMZN's (or any other ticker's) holdings, targets, tiers, roles,
  clusters, caps, or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or against
  any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Any research or Company Intelligence record for **EQIX** or any fifth company — EQIX is explicitly
  deferred, not authorized, and not silently includable by a future implementation session under this
  decision.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C), including §C.8's coverage-completion observation —
  which remains advisory research output, not a Milestone 4 conclusion.
- Modifying any existing Company or Theme Intelligence record (the 20 currently covered tickers plus
  `ai_infrastructure` and `life_sciences_tools_medtech`).
- Silently importing existing tiers or targets as research conclusions.
- Automatic authorization of a sixth Milestone 3 batch or any Milestone 4-9 work — completing Batch 5
  does not authorize Batch 6 or Milestone 4.
- Beginning, advancing, or drawing on `OPS-0007` §8 step I (the official-and-provisional Monday
  allocation-check package) in any way.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.

### H. Governance package (this filing)

This decision's own implementation — the governance PR itself, carrying this file and `OPS-0008`
together, not the future research PR — touches exactly:

1. This decision file, `governance/decisions/PI-0027-ws0005-milestone3-batch5-hyperscaler-ai-
   infrastructure.md`.
2. `governance/decisions/OPS-0008-research-wave-protocol-v1.md` (filed alongside this decision, its
   own separate file, per the principal's amendment).
3. `governance/decisions.yaml` (index regeneration: two new entries, `OPS-0008` and `PI-0027`).
4. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization and the
   protocol's adoption, using only `OPS-0001`'s existing schema and status vocabulary — no new field,
   no new status value. Milestones 1-2 and Milestone 3 Batches 1-4 entries remain exactly as prior
   filings left them; Milestone 3 remains `status: in_progress` for the milestone as a whole;
   Milestones 4-9 remain `status: proposed`, unauthorized, unchanged; `next_action` states the next
   step is exactly one bounded research implementation PR for this batch, following `OPS-0008`'s
   protocol — not a sixth batch, not Milestone 4, not `OPS-0007` §8 step I).
5. The applicable `CLAUDE.md` Decisions Log entries (one for `OPS-0008`, one for this decision)
   recording this acceptance.

**No other file is touched by this governance filing.** No Company Intelligence record, comparison
artifact, freshness-registry or freshness-checkpoint row, and no test or validator file is created,
modified, or authorized to be created by this filing — those belong exclusively to the later,
separate implementation PR authorized in §A.

### I. Effectiveness, review, and merge gates

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
- **Completion of this batch does not authorize a sixth Milestone 3 batch or any Milestone 4 work**,
  and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself (carrying this decision and `OPS-0008` together) is subject to the same
discipline: it must remain in draft state, gain its own eligible independent review anchored to its
exact head per `OPS-0007` §1, and receive explicit principal acceptance before it may be marked ready
or merged. This decision does not mark itself, or authorize marking itself, ready for merge.

## Rationale

**Why MSFT, GOOGL, META, and AMZN, and why EQIX is deferred rather than included.** These four close
the entire remaining Company Intelligence coverage gap in the CLAUDE.md-documented 7-name AI-
infrastructure concentration finding (ASML/TSM/NVDA/GEV already covered) and add the fourth major
hyperscaler (AMZN) already cited, unverified, across three completed batches' own records. The
retained coverage-gap register independently flags MSFT/GOOGL/META with its own highest disclosed
materiality rating. EQIX was seriously considered — as a data-center-REIT counterpart to this
demand-side wave — but the principal's approved amendment defers it: EQIX's REIT legal and disclosure
structure is untested anywhere in this repository's Intelligence coverage, and proving out the newly-
adopted two-PR lifecycle and stop-before-drafting gate on four companies sharing a single, already-
proven operating-company disclosure shape is the more conservative first application of `OPS-0008`.
Deferring EQIX by name, rather than omitting it silently, preserves it as an explicit future
candidate.

**Why `PI-0027`, not a new `OPS-####` or a reuse of `PI-0023`-`PI-0026`.** Same category and
reasoning as `PI-0023`-`PI-0026`: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), filed in the `PI-####` series per `governance/decisions/
README.md`'s convention, as its own file per the principal's explicit amendment (separate from
`OPS-0008`, though filed in the same governance PR).

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical reasoning
to `PI-0023`-`PI-0026`: none of MSFT, GOOGL, META, or AMZN has an existing Company Intelligence
record, so this batch is first-coverage record creation, not a `PI-0016` review of existing
conviction.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR; `OPS-0008` §4
restates this as the default two-PR lifecycle's first step.

## Alternatives Considered

- **Include EQIX as a fifth company in this batch.** Rejected per the principal's explicit amendment
  — EQIX's REIT structure introduces an untested disclosure shape; deferred to its own future batch
  rather than diluting this batch's first application of the new protocol.
- **Select a pharma-focused batch (LLY, ABBV, MRK, JNJ, GILD) instead.** Considered as an alternative
  candidate in the proposal-only session's Phase 5 comparison; rejected by the principal in favor of
  the higher-documented-materiality hyperscaler wave, which the retained coverage-gap register
  independently flags as the highest-priority remaining gap.
- **Select an enterprise-software batch (CRM, NOW, ORCL, IBM, DELL) instead.** Rejected — lowest
  materiality of the candidates considered per the retained coverage-gap register; a legitimate future
  "quick win" candidate, not selected as this batch.
- **Limit this batch to MSFT, GOOGL, and META alone (3 companies), deferring AMZN as well.**
  Considered as the safety-fallback candidate; rejected — AMZN's inclusion is well-supported by its own
  repeated, unverified citation across three completed batches' records, and four companies sharing a
  single disclosure shape does not present the same evidence-burden concern EQIX's REIT structure
  would have.
- **File under a new `OPS-####` number, or combine with `OPS-0008` into one filing.** Rejected per the
  principal's explicit amendment and the same category reasoning `PI-0023`-`PI-0026` already
  established for filing Company Intelligence research authorizations as `PI-####`.
- **Authorize a sixth Milestone 3 batch, begin Milestone 4 relationship mapping, or begin `OPS-0007`
  §8 step I in this same filing.** Rejected — exceeds the principal's authorization, which names
  exactly MSFT, GOOGL, META, and AMZN for Batch 5 only.

## Consequences

**Authorized, effective on this decision's merge:** exactly one fifth Milestone 3 research batch
(MSFT, GOOGL, META, AMZN), scoped and bounded exactly as stated in §§A-I above, to proceed via its own
later, separate, bounded, draft-until-independently-reviewed implementation PR, under `OPS-0008`'s
Research Wave Protocol v1.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 20 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`); `allocate.py`,
`margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness module, and
every existing test; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research charter and
trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely unauthorized, and
`OPS-0007` §8 step I is neither begun nor advanced by this filing. **EQIX remains uncovered and
unauthorized.** No sixth Milestone 3 batch is authorized by this filing, and none is inferred from its
acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or automatic
implementation is authorized or implied by this decision alone.** A future, separately implemented,
draft-until-independently-reviewed research PR may begin exactly the batch scoped above only after
this decision itself merges; any resulting Company Intelligence record, comparison artifact,
freshness-registry update, or later policy consequence remains subject to that PR's own independent
review, principal acceptance, validation, and (for anything beyond Intelligence content) its own
separate future governance decision.
