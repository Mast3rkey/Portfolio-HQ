---
decision_id: PI-0028
date: 2026-07-27
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027]
supporting_artifact: null
---

## Context

`OPS-0006` established WS-0005 and authorized exactly Milestones 1-2 to execute; Milestone 3
(Intelligence completion) proceeds batch-by-batch, each requiring its own separate, later,
explicit principal authorization (`OPS-0006` §5). Five batches are complete: `PI-0023` (ASML,
AMAT, KLAC, LRCX — semis capital equipment), `PI-0024` (MU, SKHY — memory), `PI-0025` (AVGO, AMD,
MRVL, INTC — compute/networking/foundry), `PI-0026` (ETN, VRT, PWR — power infrastructure), and
`PI-0027` (MSFT, GOOGL, META, AMZN — hyperscaler AI infrastructure). `OPS-0008` adopted the
Research Wave Protocol v1, prospectively, for batches authorized from its own merge forward —
`PI-0027` was the first batch filed under it. **No prior batch has covered any financial-sector
holding.**

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ` (remote origin path via the session's
  git proxy).
- **`origin` fetched and pruned.** Local `HEAD` (branch `claude/ws-0005-batch-6-governance-6zi1gn`)
  confirmed identical to `origin/main` at `d16ec07f3c003f7e0ec218773388344a22a18977` — the exact
  baseline this session was given, confirmed live rather than assumed. Working tree confirmed
  clean before any edit.
- **`d16ec07f3c003f7e0ec218773388344a22a18977` is PR #169's merge commit**, confirmed via
  `git log`: parents `86884377d653a3f5413d9c43b0b20142381f629a` (base — `PI-0027`/`OPS-0008`'s own
  merge commit, PR #168) and `a34264eeb1f3894778af03f8219c34aadd98e60c` (second parent — the exact
  head GitHub review `4783082859` (GPT-5.6 Thinking, `APPROVED FOR READINESS AND MERGE`) reviewed
  and the principal (`Mast3rkey`) merged at `2026-07-27T01:30:10Z`). No unreviewed commit sits
  between the reviewed head and the merge.
- **Zero open pull requests exist** in the repository at this filing's preflight — confirmed via
  the GitHub API, not inferred. No branch, open PR, or closed/merged PR (PR #145 through #169
  inspected) references Batch 6, V, MA, JPM, "financial infrastructure," Milestone 4, or
  `OPS-0007` §8 step I — this session's branch is the only one touching this scope.
- **Batch 5 (MSFT, GOOGL, META, AMZN) post-merge verification, performed independently this
  session** (per `OPS-0008` §4(a)'s read-only convention — recorded in this filing's own preflight,
  the same pattern `PI-0024`/`PI-0025`/`PI-0026` already used to confirm the prior batch before
  proceeding): `intelligence_validator.py` run directly against `intelligence/companies/` — 24
  files (20 pre-existing + MSFT/GOOGL/META/AMZN), all valid, exit code 0. `freshness_validator.py`
  — `OK`. Decision filed-versus-indexed reconciliation — 38 files under `governance/decisions/`
  (excluding `README.md`) = 38 entries in `governance/decisions.yaml`, no orphans, `PI-0027` and
  `OPS-0008` present in both. Exactly-one-primary-workstream check — `WS-0005` is the sole
  `priority: primary` entry in `operations/WORKSTREAMS.yaml`. Full pytest suite —
  **1502/1502 passed** (`python3 -m pytest -q`, all environment dependencies from `requirements.txt`
  installed fresh this session). `git diff --check` — clean. Protected-path spot check —
  `targets.yaml`, `holdings.yaml`, `allocate.py`, and `margin_state.py` confirmed unmodified in the
  PR #169 diff per its own body and this session's independent inspection. **All five elements of
  `OPS-0007` §3's PROVISIONAL definition are satisfied for MSFT, GOOGL, META, and AMZN** — eligible
  review (GPT-5.6 Thinking, four rounds culminating in `APPROVED FOR READINESS AND MERGE`), bounded
  corrections and exact-head re-reviews completed for every material finding (I169-1 through I169-6,
  D169-1 through D169-3, F169-1 through F169-3, all resolved per the approval-candidate review),
  explicit principal acceptance and merge at the exact approved head, and this session's own
  post-merge re-verification. **MSFT, GOOGL, META, and AMZN are therefore PROVISIONAL under
  `OPS-0007` §3**, effective as of this filing's preflight.
- **`intelligence/companies/` independently confirmed to hold no V, MA, or JPM record** (24 files,
  none named `V.*`, `MA.*`, or `JPM.*`). `intelligence/freshness_registry.yaml` and
  `intelligence/freshness_checkpoints.yaml` independently confirmed to carry no row for any of the
  three (24 rows each, matching the 24 existing companies exactly).
- **`targets.yaml` independently inspected**: `V` is a `T1` ticker (3.35% target, alongside ASML,
  TSM, MSFT, GOOGL, META, NVDA, GEV, LLY, COST); `MA` is a `T2` ticker (1.65% target, alongside
  AVGO, AMZN, CEG, PWR, ISRG, TMO, DHR, SYK, BRK.B, WMT, EQIX, MLM, AAPL); `JPM` is a `band` ticker
  (0.75% target, 1.25x cap, alongside KLAC, LRCX, AMAT, AMD, MU, MRVL, WDC, VRT, ETN, CAT, GNRC,
  IBM, NOW, CRM, ORCL, NFLX, SHOP, CRWD, PANW, UBER, HOOD, XOM, CVX, RTX, ABBV, MRK, JNJ, GILD, UNH,
  BABA, SKHY, DELL). **None of the three is a member of any `caps.clusters` correlated-cluster cap**
  (`semis`, `power_infra`, `oil`) — confirmed by direct inspection of each cluster's `tickers:` list.
- **`operations/provisional/WS0005_COVERAGE_GAP_REGISTER_20260726.md` independently inspected**: its
  own retained rows for V, MA, and JPM state, verbatim — V: "High materiality because of existing
  portfolio weight; MA (also uncovered, T2) shares the same regulatory exposure with no independent
  verification of either"; MA: "Moderate materiality — same regulatory-exposure category as V
  (uncovered, T1)"; JPM: "Low-moderate — financial-sector holdings carry structurally different risk
  factors (regulatory capital, credit cycle) than the industrial/tech names dominating this
  register." This register — filed before this decision and not authored by it — independently
  supports treating V and MA as one closely linked comparison pair (shared payment-network,
  interchange-fee regulatory exposure) while recognizing JPM as a structurally distinct
  financial-intermediation role, rather than three unrelated names grouped only by GICS sector.
- **`OPS-0007`, `OPS-0008`, and `PI-0023`-`PI-0027` read in full this session** (not relied on from
  memory) to confirm the twelve-point review standard, the Research Wave Protocol's default wave
  size/coherence requirement, the mandatory stop-before-drafting source-readiness gate and its
  standing evidence-recovery pre-authorization, the default two-PR lifecycle, and the PROVISIONAL
  definition, all as they apply to this filing.
- **`PI-0028` confirmed the next unused decision number**, checked live against both
  `governance/decisions/` (highest filed: `PI-0027`; highest `OPS-####`: `OPS-0008`) and
  `governance/decisions.yaml` (same, 38 entries, no `PI-0028` row) — not assumed from the task's own
  suggested numbering.

The principal has directed preparation of a sixth Milestone 3 batch covering **exactly V, MA, and
JPM**, under `OPS-0008`'s Research Wave Protocol v1. This decision records that authorization; it
does not itself perform any research.

### Why three companies, not the default five-to-six

`OPS-0008` §1 sets a default wave size of 5-6 companies but permits a smaller wave when, among
other reasons, "the candidate companies are not, on closer analysis, genuinely coherent" at a
larger size. The retained coverage-gap register's own materiality language (quoted above) already
draws this line: V and MA share one specific, well-defined mechanism (global payment-network
economics, card-scheme interchange regulation, cross-border transaction volume); JPM's economic
role — deposit-taking, lending, credit risk, trading, investment banking, custody, a levered
balance sheet — is a different economic mechanism (financial intermediation, not fee-based network
routing), grouped into this batch only under the broader label "financial infrastructure," not
because it shares V/MA's specific mechanism. Extending this wave to 5-6 names would require adding
either further payment/network names (none remain in `targets.yaml`) or other financial-sector
holdings whose mechanism is different again (e.g., an insurer or asset manager, if one existed in
the roster) — diluting the batch's coherence rather than improving it, the same failure mode
`OPS-0008` §1 already warns against ("not merely the same GICS sector label... or similar
historical price behavior"). Three names, honestly grouped as two sub-mechanisms (network economics;
balance-sheet intermediation) under one demand-side portfolio theme, is the coherent unit here —
matching `PI-0026`'s own three-company precedent (ETN/VRT/PWR) and `PI-0027`'s four-company
precedent (below the 5-6 default for its own documented reason).

## Decision

**PI-0028 authorizes exactly one thing: the sixth bounded WS-0005 Milestone 3 research batch,
covering V, MA, and JPM, and nothing else.** This is **evidence development only** — no research
has been performed, and this filing alone authorizes no research finding, Company Intelligence
record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, trade, or order.
**This filing (its own governance PR) authorizes the creation of the governance-authorization
package only** — this `PI-0028` decision file, `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log entry. It does not
authorize drafting any V, MA, or JPM Company Intelligence record or the comparison artifact — those
become authorized to begin only after this governance decision is independently reviewed,
principal-accepted, and merged, exactly as `PI-0023`-`PI-0027`'s own authorization-precedes-research
separation already established.

**This batch adopts `OPS-0008`'s Research Wave Protocol v1 by reference** for lifecycle, review
standard, and the source-readiness gate — not restated in full here. In particular: the future
implementation PR must apply `OPS-0008` §2's mandatory stop-before-drafting primary-source gate for
each of V, MA, and JPM before drafting substantive economic content, using the standing
evidence-recovery pre-authorization if primary access is blocked; and the future implementation PR
is expected to follow `OPS-0008` §4's default two-PR lifecycle (this authorization PR, then one
implementation PR carrying its full review cycle), with post-merge verification recorded per §4's
read-only default rather than through a dedicated third reconciliation PR, absent a genuine material
discrepancy.

### A. What the later, separate implementation PR may do

Once this decision merges, a later, separate implementation PR (not this filing, and not opened by
this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/
   V.yaml`/`.md`, `MA.yaml`/`.md`, `JPM.yaml`/`.md` — using the existing repository schema frozen
   by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated provisions, with the human
   approvals every prior first-coverage record has required (`portfolio_role_ref` — descriptive
   only; `conviction.rating` from `PI-0004`'s closed four-value vocabulary; conviction rationale;
   review cadence; thesis/risks/catalysts; source-access disclosure).
2. Create exactly **one hand-authored batch comparison artifact**, at `intelligence/
   BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md` (mirroring the existing
   `BATCH<N>_<SUBJECT>_COMPARISON.md` convention), naming this batch's coherent theme — payment-network
   economics (V, MA) contrasted with balance-sheet financial intermediation (JPM), per §C below.
3. Cite required source and evidence references per company, satisfying §D below.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per §E
   below and `OPS-0006` §12 — no universal cadence.
5. Add focused tests or validators, only where required by existing repository convention.
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   **one new enrollment row per company** (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0028`, `company_record_authority:
   PI-0028`).
7. Create a retained, attributable primary-source evidence artifact under `governance/audits/` if
   `OPS-0008` §2's source-readiness gate is blocked for one or more companies and the standing
   evidence-recovery pre-authorization is exercised.
8. Perform the minimum factual `operations/WORKSTREAMS.yaml` synchronization required once that
   implementation PR merges, per `OPS-0008` §4's read-only-by-default post-merge convention — not
   before, and not by this filing.

No other repository change is authorized by this decision for that future implementation PR.

### B. Required research standard (per company)

The implementation PR's research, for each of V, MA, and JPM individually, must establish, at
minimum:

1. Economic function and current governed portfolio role.
2. Business model and revenue economics, by segment where applicable.
3. Durable moat and competitive position.
4. Financial quality — margins, free cash flow, balance-sheet resilience, downturn behavior.
5. Management and capital-allocation history.
6. Major growth drivers.
7. Material regulatory, litigation, credit, cyclicality, and technology risks.
8. Explicit thesis-break conditions.
9. Actively searched disconfirming evidence.
10. Competitors and substitutes.
11. Important dependencies (network partners, issuing/acquiring banks, payment-rail
    counterparties, funding sources, correspondent relationships, as applicable per company).
12. Current evidence freshness and access status.
13. **Current governed tier, target, role, and cluster, clearly labeled as historical policy, not
    research evidence** — per `OPS-0006` §2/§3. (V: T1, 3.35% target. MA: T2, 1.65% target. JPM:
    band, 0.75% target, 1.25x cap.) None of the three is a member of any `targets.yaml`
    correlated-cluster cap.
14. **Margin-relevance evidence, factual and advisory only** — cyclicality; liquidity; leverage
    (including, for JPM specifically, its regulatory-capital and balance-sheet structure as a
    depository institution, distinct from an operating company's ordinary corporate leverage);
    refinancing/funding risk; drawdown and recovery characteristics; correlated-loss behavior —
    with no recommendation to borrow, no safe-leverage calculation, and no deployment-timing or
    margin-ceiling conclusion of any kind.
15. Evidence-driven freshness cadence and refresh triggers per §E below.
16. **External opportunities or replacements only as unauthorized future leads** — advisory
    candidate list only, no holding add, no tier/target assignment, no mechanical ranking, no batch
    expansion, no research on an outside candidate without its own separate future authorization.
17. **Why the company may or may not deserve incremental capital compared with the alternatives**
    (capital-priority comparison, explicitly separated from business quality — same discipline
    `PI-0027` §B.23 established). For each of V, MA, and JPM individually: separate an assessment
    of business quality (items 1-14 above) from a distinct assessment of capital priority (whether
    the next investment dollar is better spent on this company than on a governed alternative);
    compare the company against the next-best use of capital among this repository's other governed
    holdings in `targets.yaml`; state explicitly why the next investment dollar might or might not
    favor this company relative to those alternatives; identify redundancy, substitutes, and
    duplicated exposure with other governed holdings. **This comparison must preserve uncertainty
    and judgment in prose and must not produce a numerical score, a composite index, or an automatic
    ranking of any kind** — consistent with §G's prohibition on any ranking or composite score. It
    remains advisory research evidence only: it recommends no trade, and it does not itself change
    any tier, target, allocation, or policy.
18. **Company-specific requirement — V:** global payment-network economics (transaction/volume
    fees, cross-border economics, value-added services); the Visa/Mastercard duopoly structure and
    its own competitive dynamics with MA; card-network interchange-fee regulation (U.S. and
    international) and current litigation/regulatory status; issuing/acquiring bank-partner
    dependency; fraud and cybersecurity exposure; debit-versus-credit and consumer-versus-commercial
    volume mix.
19. **Company-specific requirement — MA:** the same payment-network economic structure as V,
    directly compared rather than independently re-derived from scratch; MA's own scale,
    geographic mix, and value-added-services (data/analytics/consulting) emphasis relative to V;
    shared interchange-fee regulatory and litigation exposure; issuing/acquiring bank-partner
    dependency; fraud and cybersecurity exposure.
20. **Company-specific requirement — JPM:** deposit-taking and lending economics; credit-cycle and
    loan-loss exposure; investment-banking, trading, and markets revenue; custody and asset/wealth
    management; merchant-acquiring business (where disclosed) and its relationship, if any, to
    V/MA's network economics; balance-sheet size, regulatory capital ratios, and stress-test
    status; interest-rate sensitivity (net interest margin); systemic-importance
    (G-SIB) regulatory status and its implications; distinction from V/MA's fee-based,
    lower-balance-sheet-intensity network model.

### C. Batch comparison requirements

The one hand-authored comparison artifact (`intelligence/
BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md`) must analyze, without scoring or ranking:

1. V versus MA payment-network economics — transaction fees, cross-border and volume exposure,
   debit/credit/commercial/value-added-service revenue mix, directly compared.
2. Network effects and acceptance-footprint scale for both, and how each competes for issuer/
   acquirer/merchant relationships.
3. Shared interchange, merchant-fee, regulatory, litigation, and technological (fraud, real-time
   payments, alternative rails) risk affecting both V and MA.
4. Overlap and redundancy between owning both V and MA — whether the pair represents genuine
   diversification (distinct customer/issuer relationships, geographic mix) or largely duplicated
   exposure to the same regulatory and network-economics risk the coverage-gap register already
   flagged.
5. JPM's distinct deposit, lending, credit, acquiring, investment-banking, markets, custody, and
   balance-sheet role — payment rails (V/MA) versus balance-sheet intermediation (JPM) as two
   structurally different mechanisms, not one "financial sector" category.
6. Sensitivity, across all three, to consumption, credit conditions, interest rates, regulation,
   fraud, cybersecurity, and economic contraction — noting where V/MA and JPM respond to the same
   macro conditions through different transmission channels (transaction volume versus credit
   losses/net interest margin).
7. Portfolio uniqueness and what exposure would be lost if each company were absent.
8. **Qualitative next-dollar (capital-priority) considerations** — same business-quality-versus-
   capital-priority separation required per §B.17 individually, but at the batch level: whether V,
   MA, and JPM compete for capital against each other or against other already-covered governed
   holdings; where redundancy or duplicated capital-priority reasoning exists between V and MA
   specifically; and why the next investment dollar might or might not favor one of the three over
   another or over an already-covered alternative. **Presented as advisory prose and
   uncertainty-preserving judgment only — never as a score, index, or ranking.**
9. Explicit limitations preventing a mechanical capital-priority ordering — differing reporting
   periods, differing disclosure regimes (V/MA as payment networks versus JPM as a regulated
   depository institution with bank-specific capital/liquidity disclosures), and any evidence gaps
   from blocked primary sources.

**The comparison artifact must remain analytical and advisory only.** It must not mechanically score
or rank the three companies, must not declare a preferred holding, must not alter a tier, target,
role, cluster, or cap, must not recommend a trade, must not recommend margin, and must not control
allocator output.

### D. Evidence and source protocol

Require primary-source-first research for changeable facts. The implementation must:

1. Attempt direct inspection of SEC filings (10-K/10-Q/8-K), company investor-relations releases,
   earnings materials, and regulator/court materials where relevant (including, for JPM, banking
   regulator materials — e.g. Federal Reserve stress-test disclosures — where they bear on
   factual, non-predictive claims).
2. Preserve claim-level provenance.
3. Distinguish filed fact; issuer statement; guidance; allegation; preliminary finding; inference;
   uncertainty; judgment.
4. Disclose inaccessible sources rather than representing snippets as inspected evidence — a
   blocked primary source must be labeled "attempted but not directly inspected" and kept separate
   from WebSearch-derived or other secondary evidence, never merged into the same citation as if
   both were equally verified.
5. **`OPS-0008` §2 applies to this batch without modification**: before drafting any company's
   substantive economic content, the implementation PR must attempt direct primary-source
   inspection for each of V, MA, and JPM and produce a source-access manifest. **If access is
   blocked for one or more companies, the implementing session must stop drafting those companies'
   records before writing substantive content** and may engage an eligible independent reviewer's
   primary-source evidence-recovery audit per `OPS-0008` §2's standing pre-authorization before
   resuming. If even that recovery pass cannot establish sufficient primary evidence for any one of
   the three, the implementation must try reasonable official alternatives, then stop, disclose
   exactly what failed, and return for explicit principal direction — it may not silently narrow,
   substitute, or declare the record complete. **The authorized batch is exactly V, MA, and JPM —
   not any two of them.**
6. Retain attributable evidence sufficient for independent review.
7. Preserve unresolved discrepancies and negative findings.
8. Avoid unsupported cross-company comparisons when periods, definitions, or reporting bases
   differ — this applies with particular force between V/MA (payment-network disclosure) and JPM
   (bank regulatory disclosure), which are not directly comparable on most financial metrics.

Do not perform that research in this governance session.

### E. Refresh and monitoring requirements

Each company must receive an evidence-driven refresh plan based on its own rate of business
change, thesis uncertainty, cyclicality, regulatory exposure, and event/gap risk. **No universal
cadence is imposed by this decision, and none may be imposed automatically by the
implementation.** Candidate review triggers, drawn from — but not limited to — `OPS-0006` §12's
list as applied selectively: earnings or guidance changes; interchange-fee or card-network
regulatory/litigation developments (V, MA); bank regulatory-capital, stress-test, or credit-cycle
disclosures (JPM); material M&A; management changes; major macro/rate-cycle developments bearing on
credit or transaction-volume exposure.

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

- Any change to V/MA/JPM's (or any other ticker's) holdings, targets, tiers, roles, clusters, caps,
  or weights.
- Any modification to `allocate.py`, `margin_state.py`, or any allocator formula.
- Any recommendation of a trade, buy, trim, exit, margin deployment, or safe leverage level.
- Any capital-priority ranking or mechanical/composite score of any kind, within the batch or
  against any other holding.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Modifying any existing Company or Theme Intelligence record (the 24 currently covered tickers
  plus `ai_infrastructure` and `life_sciences_tools_medtech`).
- Any research or Company Intelligence record for **EQIX** — EQIX remains explicitly deferred per
  `PI-0027`, and this decision does not authorize it, silently or otherwise.
- Adding a fourth company to Batch 6.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- Beginning Milestone 4 (portfolio relationship mapping) beyond the bounded, batch-internal
  comparison required inside this batch (§C).
- Automatic authorization of a seventh Milestone 3 batch or any Milestone 4-9 work — completing
  Batch 6 does not authorize Batch 7 or Milestone 4.
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

Batch 6 is complete only when:

1. This authorization decision is accepted, merged, and effective.
2. All three Company Intelligence YAML/Markdown pairs (V, MA, JPM) exist.
3. The comparison artifact (`intelligence/BATCH6_FINANCIAL_INFRASTRUCTURE_COMPARISON.md`) exists.
4. One freshness-registry row and one freshness-checkpoint row exist for each of V, MA, JPM.
5. Retained attributable evidence exists wherever `OPS-0008` §2's evidence-recovery method was
   exercised.
6. Validators (`intelligence_validator.py`, `freshness_validator.py`) and the full test suite pass.
7. One implementation PR is independently reviewed at exact head, per `OPS-0007` §1.
8. The principal explicitly accepts that exact head.
9. The exact reviewed head merges.
10. Independent, read-only post-merge verification confirms ancestry, byte identity, scope, tests,
    validators, and protected paths — per `OPS-0008` §4's read-only-by-default convention.
11. V, MA, and JPM are correctly classified under `OPS-0007` §3 (PROVISIONAL only once all of the
    above are satisfied — review and principal acceptance alone are not sufficient).
12. No material discrepancy remains.

**Merge alone is not completion.** Another routine reconciliation PR is not authorized unless
post-merge verification identifies a material discrepancy requiring correction — per `OPS-0008`
§4's no-routine-third-PR default.

### I. Governance package scope (this filing)

This decision's own implementation — the governance PR itself, not the future research PR —
touches exactly:

1. `governance/decisions/PI-0028-ws0005-milestone3-batch6-financial-infrastructure.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0028`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record this batch's authorization,
   Batch 5's independently-verified post-merge/PROVISIONAL status, and minimal preflight facts,
   using only `OPS-0001`'s existing schema and status vocabulary — no new field, no new status
   value. Milestone 3 remains `status: in_progress` for the milestone as a whole; Milestones 4-9
   remain `status: proposed`, unauthorized, unchanged; `next_action` states the next step is
   exactly this governance PR's own independent review, not implementation work, not a seventh
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
- **Completion of this batch does not authorize a seventh Milestone 3 batch or any Milestone 4
  work**, and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself is subject to the same discipline: it must remain in draft state, gain
its own eligible independent review anchored to its exact head per `OPS-0007` §1, and receive
explicit principal acceptance before it may be marked ready or merged. This decision does not mark
itself, or authorize marking itself, ready for merge.

## Rationale

**Why V, MA, and JPM, grouped as "Financial Infrastructure."** These are the only three uncovered
financial-sector holdings in the roster (`targets.yaml`), and the only ones the retained
coverage-gap register flags at High/Moderate/Low-moderate materiality with a shared
"research-coverage urgency only" recommendation. V and MA share one specific, well-evidenced
mechanism (global payment-network economics and interchange-fee regulatory exposure) that the
register itself already identifies as duplicated, unverified risk between the two; JPM is included
in the same batch as a structurally distinct financial-intermediation role (deposit-taking,
lending, credit, trading, investment banking) rather than a second network name, so the batch tests
whether "financial infrastructure" as a portfolio label spans one coherent theme or two related but
distinct mechanisms — the same kind of honest structural question `PI-0026`'s comparison artifact
asked of `power_infra`.

**Why three companies, not the default five-to-six.** See the dedicated Context subsection above —
no further payment-network or comparably coherent financial-sector candidate remains in the roster,
and forcing the wave to 5-6 by adding a less-related financial name would dilute coherence rather
than serve it, exactly the failure mode `OPS-0008` §1 warns against.

**Why `PI-0028`, not a new `OPS-####` or a reuse of `PI-0023`-`PI-0027`.** Same category and
reasoning as every prior batch: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), filed in the `PI-####` series per `governance/decisions/
README.md`'s convention.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical
reasoning to `PI-0023`-`PI-0027`: none of V, MA, or JPM has an existing Company Intelligence
record, so this batch is first-coverage record creation, not a `PI-0016` review of existing
conviction.

**Why the governance authorization is filed separately from, and strictly before, the research
implementation.** `OPS-0006` §5 requires the authorization to precede the research PR; `OPS-0008`
§4 restates this as the default two-PR lifecycle's first step.

**Why Batch 5's PROVISIONAL status and post-merge verification are recorded here rather than in a
dedicated reconciliation PR.** `OPS-0008` §4(a) explicitly directs that read-only post-merge
verification of the prior batch be folded into the next batch's own governance-authorization
preflight — exactly what this filing's Context section does — rather than filed as its own PR,
since no material discrepancy was found.

## Alternatives Considered

- **Include EQIX in this batch as a fourth "financial infrastructure"-adjacent name.** Rejected —
  `PI-0027` already deferred EQIX by name specifically because its REIT legal/disclosure structure
  is untested in this repository's Intelligence coverage; nothing about this batch's scope changes
  that reasoning, and EQIX remains a distinct future candidate, not silently folded in here.
- **Expand to a full 5-6-name wave by adding other financial-adjacent holdings (e.g. BRK.B).**
  Rejected — BRK.B is a diversified insurance/holding-company conglomerate, not a payment-network
  or bank-intermediation name; adding it would dilute this batch's documented coherence rather than
  strengthen it, the exact concern `OPS-0008` §1 raises for forced larger waves.
  Considered and declined; may be its own future batch candidate.
- **Split V/MA and JPM into two separate batches.** Rejected — three names is well within a single
  implementation PR's safe review surface (matching `PI-0026`'s own three-company precedent), and
  the comparison artifact's required payment-rails-versus-balance-sheet-intermediation contrast is
  more useful analyzed together than split across two governance cycles.
- **File under a new `OPS-####` number.** Rejected — same category reasoning as every
  prior Milestone 3 batch authorization.
- **Authorize a seventh Milestone 3 batch, begin Milestone 4, or begin `OPS-0007` §8 step I in this
  same filing.** Rejected — exceeds the principal's authorization, which names exactly V, MA, and
  JPM for Batch 6 only.

## Consequences

**Authorized, effective on this decision's merge:** exactly one sixth Milestone 3 research batch
(V, MA, JPM), scoped and bounded exactly as stated in §§A-J above, to proceed via its own later,
separate, bounded, draft-until-independently-reviewed implementation PR, under `OPS-0008`'s
Research Wave Protocol v1.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 24 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`); `allocate.py`,
`margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness module,
and every existing test; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research
charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
and `constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely
unauthorized, and `OPS-0007` §8 step I is neither begun nor advanced by this filing. **EQIX remains
uncovered and unauthorized.** No seventh Milestone 3 batch is authorized by this filing, and none is
inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future, separately
implemented, draft-until-independently-reviewed research PR may begin exactly the batch scoped
above only after this decision itself merges; any resulting Company Intelligence record, comparison
artifact, freshness-registry update, or later policy consequence remains subject to that PR's own
independent review, principal acceptance, validation, and (for anything beyond Intelligence
content) its own separate future governance decision.
