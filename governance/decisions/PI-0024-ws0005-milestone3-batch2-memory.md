---
decision_id: PI-0024
date: 2026-07-25
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, PI-0011, PI-0013, PI-0016, PI-0023, AUTO-0001]
supporting_artifact: null
---

## Context

`PI-0023` authorized WS-0005 Milestone 3's first batch (ASML, AMAT, KLAC, LRCX — the `semis`
cluster's capital-equipment sub-segment) and recorded, in its Alternatives Considered section,
that of the cluster's other uncovered members — including MU and SKHY — "each remains
individually eligible for its own future, separately authorized batch." `PI-0023`'s
implementation (PR #154) is merged and complete; `operations/WORKSTREAMS.yaml`'s WS-0005 entry
records Milestone 3 as `status: in_progress` (Batch 1 complete, milestone as a whole not complete)
and its `next_action` names, without selecting or authorizing, "candidate uncovered semis-cluster
members: AVGO, AMD, MU, MRVL, WDC, INTC, SKHY" for a future batch decision.

The principal has explicitly authorized preparation of a second Milestone 3 batch covering
**exactly MU and SKHY**, on the following stated rationale: both are current DRAM/NAND memory
manufacturers; the batch must examine their HBM exposure and differentiation; both occupy the
same memory-cycle and AI-memory economic function; SKHY is the Nasdaq ADR for the established SK
hynix business, not a newly formed operating company; and WDC is excluded because Western Digital
separated its Flash business into Sandisk in February 2025, leaving the remaining WDC business
centered on HDD storage rather than the DRAM/NAND/HBM memory-cycle function this batch examines.
This decision records that authorization; it does not itself perform any research.

Independently confirmed against live repository state at filing time (not restated from the
`PI-0023`-era audit artifact, per the same reconciliation-gate discipline `PI-0023` applied to its
own selection):

- **MU** — `holdings.yaml` `shares.MU: 0.048267` (a governed, live-priced holding); `targets.yaml`
  places it in the `band` tier (0.75% target, cap 1.25x, RSI-gated trim) and in the `semis`
  correlated-cluster cap (≤25% of book). No Company Intelligence record exists
  (`intelligence/companies/` currently holds only AMAT, ASML, COST, GEV, ISRG, KLAC, LRCX, NVDA,
  TMO, TSM, XOM). No row for MU exists in `intelligence/freshness_registry.yaml` or
  `intelligence/freshness_checkpoints.yaml`.
- **SKHY** — `holdings.yaml` `shares.SKHY: 0.278473` (a governed, live-priced holding since
  2026-07-14); `targets.yaml` places it in the `band` tier (0.75% target) and in the `semis`
  cluster. No Company Intelligence record exists; no freshness_registry/checkpoints row exists.
- **WDC** — `holdings.yaml` `shares.WDC: 0.15222` (a governed holding, unaffected by this
  decision); `targets.yaml` places it in `band` and in `semis`. `targets.yaml`'s `semis` cluster
  comment (dated 2026-07-14 in repository content, unchanged since) reads: "the equipment
  (KLAC/LRCX/AMAT) and memory (MU/WDC) names crash hardest" — grouping MU and WDC together as
  "memory" names. The comment itself is dated July 2026, but its treatment of WDC as a
  flash-memory peer of MU reflects Western Digital's business composition before its February 2025
  separation of the Flash (NAND) business into the independent, publicly traded Sandisk
  Corporation (SNDK), and appears stale after that separation; the WDC business remaining after it
  is centered on HDD (hard-disk-drive) storage, not DRAM/NAND/HBM memory manufacturing.
  This decision finds that comment stale as a factual description of WDC's current business — see
  §"WDC / Sandisk boundary" below — but does not correct it here; correction is recorded as a
  separate, unauthorized, future factual-reconciliation item.
- No open PR, branch, or accepted decision authorizes or implements a second Milestone 3 batch.
  Preflight for this filing confirmed: `state: open` pull requests return empty; no local or
  remote branch references MU, SKHY, "batch2," "batch-2," or "milestone-3" beyond this filing's
  own branch; `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml`
  carry no row for MU or SKHY; no `PI-####` decision references either ticker; `PI-0023` (highest
  filed entry in `governance/decisions/` and `governance/decisions.yaml` at this filing's base
  commit) does not authorize a second batch.
- `PI-0024` is confirmed as the next unused decision number in the series — checked live against
  both `governance/decisions/` (highest filed: `PI-0023`) and `governance/decisions.yaml` (highest
  indexed: `PI-0023`) at this filing's base commit, not assumed.

## Decision

**PI-0024 authorizes exactly one thing: the second bounded WS-0005 Milestone 3 research batch,
covering MU and SKHY, and nothing else.** This is **evidence development only** — no research has
been performed, and this filing alone authorizes no research finding, Company Intelligence record,
policy change, tier/target/roster/cluster/cap/allocator change, margin-policy recommendation,
trade, or order. **The authorized batch is exactly MU + SKHY — not MU alone.** No clause in this
decision permits a future implementation session to automatically contract this batch to MU only,
under any circumstance, including source-access difficulty (see "No automatic contraction" below).

### A. What this decision authorizes

A later, separate implementation PR (not this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/MU.yaml`
   / `MU.md` and `intelligence/companies/SKHY.yaml` / `SKHY.md` — using the existing repository
   schema frozen by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated provisions, with the
   human approvals every prior first-coverage record has required (`portfolio_role_ref` —
   descriptive only, `conviction.rating` from `PI-0004`'s closed four-value vocabulary, conviction
   rationale, review cadence, thesis/risks/catalysts, and source-access disclosure).
2. Create exactly **one hand-authored batch comparison artifact** examining MU and SKHY together,
   per §"Batch comparison requirements" below.
3. Cite required source and evidence references per company, satisfying §D below and the
   primary-source standard stated there.
4. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per
   §B.17 below and `OPS-0006` §12.
5. Record relationship evidence between MU and SKHY and their major shared dependencies (§B.12,
   comparison artifact) — structural/economic overlap, not measured price correlation, per
   `OPS-0006` §4 Milestone 4's own distinction, which this batch's evidence must respect even
   though Milestone 4 itself remains unauthorized.
6. Add focused tests or validators, only where required by existing repository convention
   (mirroring `PI-0011`/`AUTO-0002`/`PI-0023`'s own narrow, single-purpose additions).
7. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   one new enrollment row per company (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0024`, `company_record_authority:
   PI-0024`) — matching the existing pattern for COST/XOM/NVDA/GEV/ISRG/TMO/TSM/ASML/AMAT/KLAC/
   LRCX, and matching both files' own stated convention that a row requires "its own existing,
   cited Company Intelligence record" and is added only through a human-reviewed PR, never by
   automation. No `monitoring_enabled` row may be set `true` by that PR.
8. Perform **factual** `operations/WORKSTREAMS.yaml` synchronization for WS-0005's Milestone 3
   gate (status, `pr`, `date`) once that implementation PR merges — not before, and not by this
   filing.

### B. Required research standard (per company)

The implementation PR's research, for each of MU and SKHY individually, must establish:

1. Economic function and governed portfolio role.
2. Business model and revenue drivers.
3. DRAM, NAND, HBM, packaging, and other relevant product exposure.
4. Manufacturing footprint and process/technology position.
5. Customers, suppliers, competitors, and substitutes.
6. Financial quality and memory-cycle sensitivity.
7. Capital expenditure and supply-discipline behavior.
8. Management and capital allocation.
9. Customer and hyperscaler concentration.
10. China, Korea, Taiwan, United States, currency, export-control, trade, and geopolitical
    exposure.
11. Balance-sheet resilience and downturn behavior.
12. Risks and actively searched disconfirming evidence.
13. Explicit thesis-break conditions.
14. What portfolio exposure would be lost if the company were absent.
15. Current governed tier and target, **clearly labeled as historical policy, not research
    evidence** — per `OPS-0006` §2/§3, preserved for later reconciliation, never treated as
    presumptively correct or cited as support for a research conclusion.
16. **Margin-relevance evidence, factual and advisory only** — no borrowing, leverage, deployment-
    timing, or margin-ceiling recommendation of any kind, matching `OPS-0006` §4 Milestone 3's own
    margin-relevant-evidence requirement and `PI-0023` §B.16 exactly.
17. Evidence-driven freshness and refresh profile — evidence dates; last-reviewed date; next-review
    date or cadence; event-driven refresh triggers (per `OPS-0006` §12's candidate-trigger list,
    applied selectively); source-review log following the existing schema.
18. **Unauthorized external opportunity or replacement leads** — identify credible non-owned
    competitors, substitutes, or missing-system candidates revealed by the research, recorded only
    as **future leads**, matching `PI-0023` §B.17 exactly: no holding add, no `holdings.yaml`
    change, no tier/target assignment, no mechanical ranking, no batch expansion, and no research
    on an outside candidate without its own separate future authorization.

### C. Batch comparison requirements

The one hand-authored comparison artifact must examine, for MU and SKHY together:

1. HBM versus conventional DRAM/NAND exposure for each company.
2. Product, technology, and packaging differentiation between the two.
3. Customer overlap and concentration.
4. Manufacturing and equipment dependencies (including any shared dependency on the `PI-0023`
   batch's equipment makers).
5. Relationships to NVDA, TSM, ASML, AMAT, KLAC, and LRCX.
6. Shared memory-pricing and capital-expenditure cycles.
7. China/export-control and geopolitical exposure.
8. Common correlated-loss mechanisms.
9. Genuinely differentiated portfolio exposure between the two companies.
10. Whether owning both adds distinct economic value or mostly duplicates one memory-cycle bet.

**The comparison artifact must not create a numerical score, weighted ranking, composite
conviction measure, or automatic capital-priority output of any kind.**

### D. Evidence discipline and primary-source standard

Require: primary sources for changeable facts; claim-level evidence; explicit separation of fact,
inference, uncertainty, judgment, source type, and actual inspection/access status (the same
standard `PI-0016` §D and `PI-0023` §D already apply, adopted here by reference for its
evidentiary discipline only — this batch is first-coverage record creation, not a `PI-0016`
committee review of existing conviction, since neither company has an existing record or rating to
review); active search for and preservation of disconfirming evidence and null/negative findings;
no unsupported search-result snippet presented as inspected primary evidence — a snippet may
identify a document but may not be represented as inspected primary evidence; no silent inheritance
of an earlier chat conclusion without independent verification.

**Required direct-inspection attempts:**

- **For MU**: SEC 10-K, 10-Q, and 8-K filings; official earnings releases; official investor
  presentations and product materials; relevant government and regulatory documents.
- **For SKHY / SK hynix**: the SEC registration statement and 424B4 prospectus; subsequent 20-F and
  6-K filings where available; official SK hynix English-language investor-relations materials;
  official Korean-market filings and financial materials where usable; relevant government and
  regulatory documents.

A later implementation session must independently attempt source access at implementation time.
**Earlier WebFetch failures (including those recorded against the `PI-0023` batch) do not prove
that primary documents are generally unavailable** and must not be relied upon as a substitute for
a fresh attempt.

### E. WDC / Sandisk boundary

This decision states explicitly:

- **WDC and SNDK are outside this batch.** Neither is authorized for research, a Company
  Intelligence record, or any other action by this decision.
- **Western Digital separated its Flash (NAND) business into Sandisk Corporation (SNDK) in
  February 2025.** The remaining WDC business is centered on HDD (hard-disk-drive) storage, not
  DRAM/NAND/HBM memory manufacturing — the economic function this batch examines.
- **`targets.yaml`'s existing `semis` cluster comment — "the equipment (KLAC/LRCX/AMAT) and memory
  (MU/WDC) names crash hardest" — groups MU and WDC together as equivalent "memory" names and
  appears stale** as a factual description of WDC's current business following the February 2025
  separation. This decision identifies that staleness; it does not correct it.
- **This decision does not alter WDC's role, cluster, tier, target, or holding status in any way.**
  WDC remains exactly as governed today: `band` tier, 0.75% target, `semis` cluster member.
- **This decision does not authorize WDC or SNDK research of any kind**, under this batch or any
  other authority.
- **No correction to `targets.yaml` occurs in this filing or its implementing PR.** The stale
  MU/WDC comment is recorded here as a separately governed factual-reconciliation item — a future,
  narrow, comment-only correction to `targets.yaml` reflecting the February 2025 Sandisk
  separation — that this decision does not resolve, authorize, schedule, or perform. It requires
  its own future action, exactly as WS-0005's own prior BTC-comment staleness finding
  (`operations/WORKSTREAMS.yaml`'s WS-0005 `next_action`) was recorded without being corrected in
  the filing that found it.

### F. No automatic contraction

**The authorized batch is exactly MU and SKHY.** No provision of this decision, and no future
implementation session's own judgment, may contract this authorization to MU alone (or to SKHY
alone) merely because primary evidence for one company proves harder to obtain than the other.

If a future implementation session cannot obtain sufficient primary evidence for either company
under §D's standard, **it must stop, disclose the specific evidence-access problem encountered,
and return to the principal for explicit amendment** — it may not silently narrow scope, complete
only one company's record and call the batch done, or treat tool failure, inaccessible sources, or
stale evidence as a license to change what this decision authorizes. Abstaining from a conclusion
for one company under §D's evidence standard is permitted and consistent with `OPS-0006` §14's
evidence-validity boundary; **redefining the batch's scope is not.**

### G. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before
comparing them with current governed tier/role/target/cluster placement; preserve that placement
as the historical baseline for later reconciliation only (§B.15); never treat it as proof of a
research conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7;
and record any disagreement between researched conclusion and governed baseline without changing
policy.

### H. Explicit prohibitions

This decision authorizes none of the following, under any interpretation:

- Any change to MU/SKHY's (or WDC's, or any other ticker's) tier, target, role, cluster
  membership, or cap.
- Any holdings change or trade of any kind.
- Any ranking, conviction score, composite score, or automatic capital-priority determination
  across the batch or against any other holding.
- Any allocator or production-code change (`allocate.py`, `margin_state.py`, or any other
  production module).
- Any Intelligence-to-allocator coupling of any kind.
- Any margin use, margin-policy recommendation, safe-leverage calculation, or deployment-ranking
  conclusion. The 1.8x leverage cap and 30% buffer floor are unchanged and out of scope.
- Any `MARGIN-0005` S3 execution or trial consumption of any kind.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any Milestone 4 execution beyond the narrow batch-internal relationship evidence this batch's
  own completeness already requires (§B.12, comparison artifact) — no economic-system-wide
  mapping, no portfolio-level margin-preparation register, and no next-best-alternative ranking.
- Automatic authorization of any later Milestone 3 batch (Samsung, or any other candidate, remains
  unauthorized).
- Automatic contraction of this batch to MU alone, to SKHY alone, or expansion beyond MU and SKHY,
  under any circumstance — see §F.
- Beginning research on WDC, SNDK, or any external opportunity/replacement lead identified by
  §B.18 without its own separate, future authorization.
- Any generated report replacing an authoritative Company Intelligence record.
- Any policy conclusion drawn from the research itself — the research remains advisory only; it
  may recommend a future policy review but cannot itself change governed policy.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any correction to `targets.yaml`'s stale MU/WDC comment — see §E.

### I. Completion and review gates

This batch may be marked complete only when: both Company Intelligence records exist with the
required evidence and freshness metadata (§B); the batch comparison artifact exists (§C);
`intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml` gain one enrollment row per
company; unresolved evidence gaps are explicitly retained, not silently dropped; the producing
implementation PR is merged to `main`; `intelligence_validator.py` and `freshness_validator.py`
pass against the merged state; `git diff --check` is clean; the full applicable test suite passes;
CI succeeds at the PR's exact head; independent, attributable Fable review is retained, anchored to
that unchanged exact head (a Fable review anchored to an intermediate commit does not satisfy this
gate — the review must be re-run, or a delta review obtained, against the literal head that
merges); at most one bounded correction pass follows if the review requires changes; the principal
explicitly accepts the implementation; post-merge ancestry, merge scope, and validator/test
re-verification are complete; and `operations/WORKSTREAMS.yaml` and `governance/decisions.yaml` are
factually synchronized to that state. A draft, a local edit, a commit, a pushed branch, an open PR,
a recommendation, or a pre-merge test run does not, by itself, constitute completion — mirroring
`OPS-0006` §16.1 and `PI-0023` §E exactly.

**Completion of this batch does not automatically authorize:** a third Milestone 3 batch;
Milestone 4 beyond the batch-internal overlap evidence already required; a tier/target/roster/
cluster/cap review; a `targets.yaml` correction (including the MU/WDC comment identified in §E);
an allocator or holdings change; or any margin research, `MARGIN-0005` S3 execution, or trial
consumption. Each requires its own separate, later, explicit principal authorization.

### J. Workstream synchronization (this filing)

This decision's own implementation (the governance PR itself, not the future research PR) updates
`operations/WORKSTREAMS.yaml`'s WS-0005 entry, using only `OPS-0001`'s existing 21-field schema and
existing status vocabulary — no new field, no new status value:

- Milestones 1-2 remain `status: complete`, unchanged. Milestone 3, Batch 1 (ASML/AMAT/KLAC/LRCX)
  remains recorded exactly as `PI-0023`/PR #154 left it, unchanged.
- Milestone 3's `gate` entry gains this second batch's authorization: it remains `status:
  in_progress` for the milestone as a whole (Milestone 3 does not become `complete` in aggregate —
  only this second, MU + SKHY batch is authorized to proceed), with `next_action` stating that this
  specific batch is now authorized to proceed to one bounded research implementation PR upon this
  decision's merge, while the milestone's broader scope (any third batch) remains unauthorized.
- Milestones 4-9 remain `status: proposed`, unauthorized, unchanged.
- `next_action` states the next step is exactly one bounded research implementation PR for this
  batch — not a third batch, not Milestone 4, and not the `targets.yaml` MU/WDC comment
  correction identified in §E.
- `evidence_refs` gains a reference to this decision.
- No unrelated workstream priority or authority field changes — WS-0005 remains the sole
  `priority: primary` workstream; WS-0001/WS-0002 priorities are untouched.

## Rationale

**Why MU and SKHY, and why together.** Both are current DRAM/NAND memory manufacturers occupying
the same memory-cycle and AI-memory economic function within the `semis` cluster — the batch
counterpart, one level down the value chain, to `PI-0023`'s capital-equipment sub-segment. SKHY is
the Nasdaq-listed vehicle for the established SK hynix operating business (not a newly formed
company), making it a comparable, evidence-bearing peer to MU rather than a speculative or
early-stage name requiring a different evidentiary posture. Requiring HBM exposure and
differentiation to be examined for both, together, reflects that HBM (high-bandwidth memory) is a
current, material differentiator within DRAM manufacturing specifically relevant to AI-compute
demand — the same category of shared, comparable driver that justified batching ASML with
AMAT/KLAC/LRCX in `PI-0023` rather than authorizing single-company filings.

**Why WDC is excluded.** `targets.yaml`'s existing cluster comment groups MU and WDC as "memory"
names, but that characterization reflects Western Digital's business composition before its
February 2025 separation of the Flash business into Sandisk (SNDK), and appears stale after that
separation — the WDC that remains is an HDD storage company, a different technology and
economic function from DRAM/NAND/HBM memory manufacturing. Including WDC in a "memory cycle"
batch after that separation would misclassify its current business on the same stale-grouping
basis this decision independently identifies as needing future correction, not perpetuate it here.

**Why the stale `targets.yaml` comment is flagged but not corrected in this filing.** This is a
governance-authorization filing, not a factual-reconciliation filing — mirroring `PI-0023`'s own
discipline of authorizing exactly one thing and no more, and the precedent WS-0005's own register
already set for the BTC-comment staleness finding (identified in `operations/WORKSTREAMS.yaml`'s
WS-0005 `next_action` without being corrected in the same entry). Correcting the comment now would
add an unauthorized, unrelated `targets.yaml` touch to a decision the principal scoped narrowly to
MU/SKHY batch authorization.

**Why no automatic contraction to MU alone.** The principal's authorization is explicit that the
batch is MU + SKHY, not MU with SKHY as an optional extension, and that a future implementation
session's inability to access sufficient primary evidence for one company is a reason to stop and
seek amendment, not a license to silently narrow what was authorized. This mirrors `OPS-0006` §14's
existing evidence-validity boundary (materially stale or incomplete evidence may require abstention
from a conclusion, but staleness alone must not automatically change what is authorized) applied
here to batch scope rather than to a policy recommendation.

**Why `PI-0024`, not a new `OPS-####` or a reuse of `PI-0023`.** Same category and reasoning as
`PI-0023` itself: this is Company Intelligence research-authorization content
(`category: portfolio_intelligence`), not workstream-register mechanics, so it is filed in the
`PI-####` series per `governance/decisions/README.md`'s convention. `PI-0023`'s own text is
`status: Accepted` and, per that same README convention, is never edited after acceptance for
anything beyond a narrow dated correction — a second batch requires its own new decision file, not
an amendment to `PI-0023`. `PI-0024` is confirmed as the next unused number, checked live against
both `governance/decisions/` and `governance/decisions.yaml` at this filing's base commit, not
assumed.

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** Identical
reasoning to `PI-0023`: `PI-0016`'s standing methodology governs review of an *existing* Company
Intelligence record's conviction and capital-priority standing; neither MU nor SKHY has an existing
record, so this batch is first-coverage record creation, structurally identical in kind to
`PI-0003`, `PI-0005`, `PI-0007`, `PI-0009`, and `PI-0023` — not a `PI-0016` review. This decision
adopts `PI-0016` §D's evidence standard by reference for its evidentiary discipline only, exactly
as `PI-0023` did.

## Alternatives Considered

- **Authorize MU alone, deferring SKHY to its own future batch.** Rejected — the principal's
  authorization is explicit that the batch is exactly MU + SKHY, and the batch's own justification
  (HBM exposure/differentiation, shared memory-cycle and AI-memory economic function) rests on
  comparative evidence a single-company authorization cannot produce, the same reasoning `PI-0023`
  applied when rejecting a single-company ASML-only batch.
- **Include WDC in this batch, preserving `targets.yaml`'s existing MU/WDC grouping.** Rejected —
  WDC's current business (HDD storage, post-February-2025 Sandisk separation) is a different
  technology and economic function from the DRAM/NAND/HBM memory-cycle bet this batch examines;
  including it would misclassify its current business on the same stale-grouping basis this
  decision identifies as needing future correction.
- **Correct `targets.yaml`'s stale MU/WDC comment in this same filing.** Rejected — out of this
  decision's authorized scope (governance authorization only, per the principal's explicit
  instruction), and inconsistent with the narrow-single-purpose discipline `PI-0023` and this
  decision both otherwise follow; recorded as a separate, unauthorized, future factual-
  reconciliation item instead.
- **Permit automatic contraction to MU alone if SKHY's primary sources prove inaccessible.**
  Rejected — explicitly foreclosed by the principal's instruction; tool failure or inaccessible
  sources are grounds for disclosed abstention or a return for amendment, never for a future
  session's unilateral scope change.
- **Adopt `PI-0016`'s full committee-review framework for this batch.** Rejected — same reasoning
  as `PI-0023`: `PI-0016` presumes an existing record and conviction rating to reassess, which
  neither MU nor SKHY has.
- **File under a new `OPS-####` number.** Rejected — same reasoning as `PI-0023`: this is Company
  Intelligence research-authorization content, not workstream-register mechanics.
- **Let this filing itself begin the research.** Rejected — `OPS-0006` §5 requires the
  authorization to precede the research PR, not accompany it, the same separation `PI-0013`'s and
  `PI-0023`'s own rationale already established.
- **Update `intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml` in this governance
  PR.** Rejected — both files gain a row only for a ticker with "its own existing, cited Company
  Intelligence record," which does not yet exist for MU or SKHY; adding rows belongs in the future
  implementation PR, exactly as `PI-0023` reasoned for its own batch.
- **Authorize a third Milestone 3 batch (e.g. AVGO, AMD, MRVL, INTC) in the same filing, since the
  candidate list is already named in `operations/WORKSTREAMS.yaml`.** Rejected — exceeds the
  principal's authorization, which names exactly MU and SKHY; each remaining candidate stays
  individually eligible for its own future, separately authorized batch, exactly as `PI-0023`
  reasoned for MU and SKHY themselves.

## Consequences

**Authorized, effective on this decision's merge:** exactly one second Milestone 3 research batch
(MU, SKHY), scoped and bounded exactly as stated in §§A-J above, to proceed via its own later,
separate, bounded implementation PR.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml` — including WDC's — remains exactly as governed today; every
existing Company/Theme Intelligence record (`AMAT`/`ASML`/`COST`/`GEV`/`ISRG`/`KLAC`/`LRCX`/`NVDA`/
`TMO`/`TSM`/`XOM`, `ai_infrastructure`, `life_sciences_tools_medtech`); `allocate.py`,
`margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness module,
and every test file; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research charter
and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. `targets.yaml`'s stale MU/WDC cluster comment is
identified as requiring future correction but is not corrected here. Milestones 4 through 9 of
WS-0005 remain entirely unauthorized. No third Milestone 3 batch is authorized by this filing, and
none is inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future,
separately-implemented research PR may now begin exactly the batch scoped above; any resulting
Company Intelligence record, comparison artifact, freshness-registry update, or later policy
consequence remains subject to that PR's own review, validation, and (for anything beyond
Intelligence content) its own separate future governance decision. If that future session cannot
obtain sufficient primary evidence for either company, it must stop, disclose the evidence-access
problem, and return for explicit principal amendment — it may not narrow this batch on its own
authority.
