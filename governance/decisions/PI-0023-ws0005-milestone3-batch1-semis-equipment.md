---
decision_id: PI-0023
date: 2026-07-25
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, PI-0011, PI-0013, PI-0016, AUTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/OPS-0006-portfolio-intelligence-completion-and-zero-based-tier-review.md`
established WS-0005 and authorized exactly Milestones 1 (baseline/inventory) and 2 (Intelligence
coverage/freshness audit) to execute, as one bounded first audit PR. §5 states explicitly:
"Completion of Milestones 1 and 2 does not automatically authorize Milestone 3. Starting
Intelligence-completion batches ... requires its own separate, later, explicit principal
authorization and its own bounded implementation or research PR — following exactly the
discipline `PI-0016` already established for single-company reviews ... informal chat sign-off
does not suffice." PR #151 merged that bounded audit (merge commit `4ff13dfa5ec0a27e55c0eb5f563b4a9c7626c131`),
independently re-verified post-merge by PR #152, which itself merged as commit
`88ac03adac8bd4f0a3bc43b36ce097c84998b27b` — confirmed, at this filing's base commit, to be both
`origin/main`'s current tip and the tip this session's local `main` branch was verified to fast-forward
to cleanly. `operations/WORKSTREAMS.yaml`'s WS-0005 entry records Milestones
1-2 as `status: complete` and Milestone 3 as `status: proposed`, unauthorized.

The retained audit artifact (`governance/audits/WS0005_MILESTONES1-2_PORTFOLIO_INVENTORY_AUDIT_20260725.md`)
independently confirms, from live repository state at audit time: `targets.yaml`'s governed
`semis` correlated-cluster cap (≤25% of book) has 13 members, of which only 2 (NVDA, TSM) carry a
Company Intelligence record — 11 uncovered. The artifact's own §5 "Recommended future research
batches" section lists, first among five advisory groupings, "**semis cluster, uncovered members**
(ASML, AVGO, AMD, MU, MRVL, KLAC, LRCX, AMAT, WDC, INTC, SKHY) — 11 of 13 cluster members
uncovered," explicitly stated as "a grouping suggestion only ... it ranks nothing, authorizes
nothing, and creates no research charter or trial consumption." This decision independently
evaluates a **four-name subset** of that eleven-name grouping — it does not adopt the artifact's
grouping as authority, per `OPS-0006` §3's zero-based discipline (the artifact's own suggestion is
evidence to consider, not a decision this filing is bound to follow in full).

Independently confirmed against `targets.yaml`/`holdings.yaml` at filing time (not restated from
the audit artifact, per `PI-0013`'s reconciliation-gate discipline applied here to selection
rather than to a review conclusion):

- **ASML** — `T1` tier, 3.35% target, `semis` cluster member (`targets.yaml` line 15). No
  Company Intelligence record (`intelligence/companies/` currently holds only COST, GEV, ISRG,
  NVDA, TMO, TSM, XOM).
- **AMAT, KLAC, LRCX** — `band` tier, 0.75% target each (cap 1.25×, RSI-gated trim), `semis`
  cluster members (`targets.yaml` line 33). No Company Intelligence record for any of the three.
- All four are current portfolio holdings (`holdings.yaml` `shares:` block, live-priced).
- `targets.yaml`'s own `semis` cluster comment (authored 2026-07-14, unchanged since) already
  singles out a sub-grouping within the 13-member cluster: "the equipment (KLAC/LRCX/AMAT) and
  memory (MU/WDC) names crash hardest" — an existing doctrine observation, not a new finding of
  this decision, that the equipment names behave as a distinguishable sub-segment of the broader
  correlation-defined cluster. ASML is not named in that specific comment sentence but is, as a
  matter of public industry structure independently verifiable at implementation time, itself a
  semiconductor front-end capital-equipment manufacturer (photolithography), placing it in the
  same equipment sub-segment as AMAT/KLAC/LRCX (deposition/etch, deposition/etch, and process
  control/metrology respectively) — distinct from the cluster's chip designers (NVDA, AVGO, AMD,
  MRVL), the cluster's foundry (TSM), and the cluster's memory makers (MU, WDC).

No other open PR, branch, or accepted decision authorizes research on any of these four tickers.
Preflight for this filing checked: no open pull request exists in the repository (`state: open`
returns empty); no local or remote branch name references ASML, AMAT, KLAC, LRCX, "semis," or
"milestone-3"; `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml`
carry no row for any of the four tickers (both files only gain a row for a ticker "without its own
existing, cited Company Intelligence record" per their own header text, and per `AUTO-0001` a row
is added only through "a human-reviewed incorporation, bootstrap, or correction PR"); `PI-0014`'s
bounded evidence review (INTC/SYK/DHR) does not name any of the four; no PI-#### decision
references ASML, AMAT, KLAC, or LRCX.

## Decision

**PI-0023 authorizes exactly one thing: the first bounded WS-0005 Milestone 3 research batch,
covering ASML, AMAT, KLAC, and LRCX.** This is **evidence development only** — no research has
been performed, and this filing alone authorizes no research finding, Company Intelligence record,
policy change, tier/target/roster/cluster/cap/allocator change, margin-policy recommendation,
trade, or order.

### A. What this decision authorizes

A later, separate implementation PR (not this filing) may:

1. Create exactly **one Company Intelligence record per company** — `intelligence/companies/ASML.yaml`
   / `.md`, `AMAT.yaml` / `.md`, `KLAC.yaml` / `.md`, `LRCX.yaml` / `.md` — using the existing
   repository schema frozen by `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and its incorporated
   provisions, with the human approvals every prior first-coverage record has required
   (`portfolio_role_ref` — descriptive only, `conviction.rating` from `PI-0004`'s closed
   four-value vocabulary, conviction rationale, review cadence, thesis/risks/catalysts, and
   source-access disclosure).
2. Cite required source and evidence references per company, satisfying §D below.
3. Record freshness metadata and a defensible, evidence-driven refresh profile per company, per
   §B.15 below and `OPS-0006` §12.
4. Record relationship evidence among the four companies and their major shared dependencies
   (§B.12/§B.16 below) — structural/economic overlap, not measured price correlation, per `OPS-0006`
   §4 Milestone 4's own distinction, which this batch's evidence must respect even though Milestone
   4 itself remains unauthorized.
5. Add focused tests or validators, only where required by existing repository convention (mirroring
   how `PI-0011`/`AUTO-0002`/`OPS-0006` §5 each added a narrow, single-purpose module with its own
   tests, never a general-purpose framework).
6. Update `intelligence/freshness_registry.yaml` and `intelligence/freshness_checkpoints.yaml` with
   one new enrollment row per company (each `checkpoint_status: pending`, empty `channels: {}`,
   `monitoring_enabled: false`, `enrollment_authority: PI-0023`, `company_record_authority: PI-0023`)
   — matching the existing pattern for COST/XOM/NVDA/GEV/ISRG/TMO/TSM, and matching both files'
   own stated convention that a row requires "its own existing, cited Company Intelligence record"
   and is added only through a human-reviewed PR, never by automation. No `monitoring_enabled` row
   may be set `true` by that PR — enabling monitoring is a distinct future action outside this
   authorization's and `AUTO-0001`'s current scope.
7. Perform **factual** `operations/WORKSTREAMS.yaml` synchronization for WS-0005's Milestone 3 gate
   (status, `pr`, `date`) once that implementation PR merges — not before, and not by this filing.

### B. Required research standard (per company)

The implementation PR's research, for each of ASML, AMAT, KLAC, and LRCX individually, must
establish:

1. Economic function and portfolio-relevant role.
2. Business model and principal revenue/profit drivers.
3. Current primary-source evidence.
4. Competitive moat and realistic erosion mechanisms.
5. Industry structure and technological position.
6. Customers, suppliers, dependencies, competitors, and substitutes.
7. Financial quality and cyclicality.
8. Management and capital-allocation evidence.
9. Key risks and disconfirming evidence.
10. Explicit thesis-break conditions.
11. What exposure would be lost if the company were absent from the portfolio.
12. How it differs from and overlaps with the other three companies in this batch.
13. The next-best capital alternative — descriptive only, **no policy recommendation**.
14. Current governed tier and target, **clearly labeled as historical policy, not research
    evidence** — per `OPS-0006` §2/§3, preserved for later reconciliation, never treated as
    presumptively correct or cited as support for a research conclusion.
15. Freshness: evidence dates; last-reviewed date; next-review date or cadence; event-driven
    refresh triggers (per `OPS-0006` §12's candidate-trigger list, applied selectively — not
    every listed trigger applies to every company); source-review log following the existing
    schema.
16. **Margin-relevance evidence, factual and advisory only** — cyclicality; balance-sheet
    strength and leverage; refinancing sensitivity; semiconductor-capital-expenditure
    sensitivity (the shared demand driver across all four); export-control and geopolitical
    exposure; customer concentration; liquidity and gap risk; drawdown and recovery
    characteristics; shared-loss mechanisms across the batch; whether thesis deterioration would
    be observable before, or only after, a large price decline. This evidence **must not**
    recommend borrowing, leverage, deployment timing, or a margin ceiling of any kind — matching
    `OPS-0006` §4 Milestone 3's own margin-relevant-evidence requirement exactly.
17. **External opportunity and replacement-candidate scan** — identify credible non-owned
    competitors, substitutes, or missing-system candidates revealed by the research; explain the
    economic role each candidate could serve; state which current holding or capital use it would
    compete against; distinguish genuinely new exposure from duplicate exposure; retain no more
    than a small, evidence-supported candidate list; treat all candidates as **advisory
    future-research leads only**.

    **This scan does not authorize:** adding a holding; changing `holdings.yaml`; assigning tiers
    or targets; ranking candidates mechanically; expanding the current four-company research
    batch; or beginning research on an outside candidate without its own separate, future
    authorization. It is a leads list for a possible future, separately-authorized review — not a
    conclusion, a recommendation, or a trigger for any repository or portfolio change.

### C. Zero-based discipline

The later research must, per `OPS-0006` §2/§3: form conclusions from current evidence before
comparing them with current governed tier/role/target/cluster placement; preserve that placement
as the historical baseline for later reconciliation only; never treat it as proof of a research
conclusion; defer formal baseline reconciliation to the still-unauthorized Milestone 7; and record
any disagreement between researched conclusion and governed baseline without changing policy.

### D. Evidence discipline

Require: primary sources for changeable facts; claim-level evidence; explicit separation of fact,
inference, uncertainty, and judgment (the same standard `PI-0016` §D already applies to its
committee-review process, adopted here by reference for its evidentiary discipline only — this
batch is first-coverage record creation, not a `PI-0016` committee review of existing conviction,
since none of the four companies has an existing record or rating to review); active search for
and preservation of disconfirming evidence and null/negative findings; no unsupported snippet
presented as inspected primary evidence; no silent inheritance of an earlier chat conclusion
without independent verification; no mechanical score, ranking, or composite index of any kind.
Historical research or chat conclusions may be used as leads only after independent verification
against a primary or credible current source.

### E. Completion criteria

This batch may be marked complete only when: all four Company Intelligence records exist with the
required evidence and freshness metadata (§B); batch-level relationship/overlap/shared-risk
evidence (§B.12, §B.16) is retained; unresolved gaps are explicitly recorded, not silently
dropped; the producing implementation PR is merged to `main`; `intelligence_validator.py` and
`freshness_validator.py` pass against the merged state; the applicable full test suite passes;
independent review is retained and attributable (a Fable review anchored to the PR's exact head,
per the retained-artifact convention `OPS-0004` established); post-merge verification (ancestry,
merge scope, clean-checkout validation) is complete; and `operations/WORKSTREAMS.yaml` and
`governance/decisions.yaml` are factually synchronized to that state. A draft, a local edit, a
commit, a pushed branch, an open PR, a recommendation, or a pre-merge test run does not, by itself,
constitute completion — mirroring `OPS-0006` §16.1 exactly.

**Completion of this batch does not automatically authorize:** a second Milestone 3 batch;
Milestone 4 (relationship mapping) beyond the batch-internal overlap evidence §B.12/§B.16 already
requires; a tier/target/roster/cluster/cap review; an allocator or holdings change; or any margin
research, `MARGIN-0005` S3 execution, or trial consumption. Each requires its own separate, later,
explicit principal authorization, per `OPS-0006` §5's own restated discipline.

### F. Explicit prohibitions

This decision authorizes none of the following, under any interpretation:

- Any change to ASML/AMAT/KLAC/LRCX's (or any other ticker's) tier, target, role, cluster
  membership, or cap.
- Any holdings change or trade of any kind.
- Any ranking, conviction score, composite score, or automatic capital-priority determination
  across the batch or against any other holding.
- Any allocator or production-code change (`allocate.py`, `margin_state.py`, or any other
  production module).
- Any Intelligence-to-allocator coupling of any kind — Company Intelligence remains advisory-only,
  per the unchanged `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` boundary.
- Any margin use, margin-policy recommendation, safe-leverage calculation, or deployment-ranking
  conclusion. The 1.8x leverage cap and 30% buffer floor are unchanged and out of scope.
- Any `MARGIN-0005` S3 execution or trial consumption of any kind.
- Any automated scanner, scheduler, notification system, or external-data integration — matching
  `OPS-0006` §15's explicit non-grant.
- Any Milestone 4 execution beyond the narrow batch-internal relationship evidence §B.12/§B.16
  already requires as part of this batch's own completeness — no economic-system-wide mapping,
  no portfolio-level margin-preparation register, and no next-best-alternative *ranking* (§B.13
  is descriptive only).
- Automatic authorization of any later Milestone 3 batch.
- Expanding the current four-company batch, or beginning research on any external
  competitor/substitute/candidate identified by §B.17's opportunity scan, without its own
  separate, future authorization — §B.17 is a leads list, not a research trigger.
- Any generated report replacing an authoritative Company Intelligence record — the YAML/Markdown
  pair remains the sole authoritative artifact per company, per the unchanged filesystem-as-index
  doctrine (`PI-0001`).
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.

### G. Workstream synchronization (this filing)

This decision's own implementation (the governance PR itself, not the future research PR) updates
`operations/WORKSTREAMS.yaml`'s WS-0005 entry, using only `OPS-0001`'s existing 21-field schema and
existing status vocabulary — no new field, no new status value:

- Milestones 1-2 remain `status: complete`, unchanged.
- Milestone 3's `gate` entry gains this batch's authorization: it remains `status: proposed` for
  the milestone as a whole (Milestone 3 does not become `authorized` in aggregate — only this
  four-company batch is authorized), with `next_action` stating that this specific batch (ASML,
  AMAT, KLAC, LRCX) is now authorized to proceed to one bounded research implementation PR upon
  this decision's merge, while the milestone's broader scope (any other batch) remains
  unauthorized.
- Milestones 4-9 remain `status: proposed`, unauthorized, unchanged.
- `next_action` states the next step is exactly one bounded research implementation PR for this
  batch — not a second batch, not Milestone 4.
- `evidence_refs` gains a reference to this decision.
- No unrelated workstream priority or authority field changes — WS-0005 remains the sole
  `priority: primary` workstream; WS-0001/WS-0002 priorities are untouched.

## Rationale

**Why a batch, and why these four.** `OPS-0006` §4 Milestone 3 explicitly contemplates "coherent
batches" rather than single-company filings, and this repository already has direct precedent for
a multi-company Intelligence authorization filed as one decision — the historical `PI-0007` (NVDA
+ GEV) and `PI-0009` (ISRG + TMO), both filed under the `PI-####` series before `governance/decisions/`
existed, now succeeded by decisions like this one filed under the same series in its current home.
ASML, AMAT, and KLAC/LRCX are not an arbitrary four-name slice of the eleven uncovered `semis`
names — they are the cluster's semiconductor front-end capital-equipment sub-segment (`targets.yaml`'s
own comment already singles out "the equipment (KLAC/LRCX/AMAT)... names" as behaving distinctly
within the broader cluster; ASML's photolithography role is the same category of business,
independently verifiable, not asserted here as a research conclusion). Their functions are
distinct enough to warrant four separate records (photolithography vs. deposition/etch vs.
process-control/metrology are different, non-substitutable steps in the same fabrication process)
while sharing a genuinely comparable driver set — semiconductor capital-expenditure cycles, a
common customer base of chip fabricators, export-control exposure to the same jurisdictions — that
makes §B.12 (overlap/differentiation) and §B.16 (shared-loss mechanisms) evidence meaningfully
comparable in a way an arbitrary four-name draw from the cluster would not support. This is
narrower, and better justified, than authorizing all eleven uncovered `semis` names in one PR — a
batch that size would be materially harder to implement, validate, and independently review in one
bounded PR, and would blur a coherent equipment sub-segment together with chip designers, a
foundry, and memory makers that do not share the same demand mechanism.

**Why `PI-0023`, not `OPS-0007`.** `OPS-0007` was floated as a session-start candidate and is
rejected here after verification. `governance/decisions/README.md`'s convention reserves `OPS-####`
for `category: operations_coordination` decisions about workstream-register mechanics themselves
(`OPS-0001` through `OPS-0006` — establishing the register, planning/audit gates, priority
transitions, audit-provenance reconciliation, phase reactivation, and WS-0005's own establishment
and Milestone 1-2 authorization). This decision instead authorizes Company Intelligence research
content — squarely `category: portfolio_intelligence`, the same category as every `PI-####`
decision in `governance/decisions/` (`PI-0010` through `PI-0022`), including the closest direct
structural precedents (`PI-0007`/`PI-0009`'s historical multi-company batches; `PI-0017`/`PI-0019`/
`PI-0021`'s single-company authorizations). The retained WS-0005 Milestone-1/2 audit artifact
itself anticipates this: its per-asset completion ledger repeatedly labels a future Milestone-3
first-coverage authorization as "own PI-XXXX filing" for every uncovered ticker, never `OPS-XXXX`.
`PI-0023` is confirmed as the next unused number in the series (`PI-0022` is the highest filed
entry in both `governance/decisions/` and `governance/decisions.yaml` as of this filing's base
commit).

**Why first-coverage discipline, not the `PI-0016` committee-review framework.** `PI-0016`'s
standing methodology (15 narrative dimensions, a 2-5-comparator capital-priority structure, two
independent recommendation outputs) governs review of an *existing* Company Intelligence record's
conviction and capital-priority standing — every company reviewed under it to date (TSM, NVDA,
GEV, COST) already had a record before its `PI-0016` review was authorized. None of ASML, AMAT,
KLAC, or LRCX has an existing record; this batch is first-coverage record *creation*, structurally
identical in kind to `PI-0003` (COST), `PI-0005` (XOM), `PI-0007` (NVDA+GEV), and `PI-0009`
(ISRG+TMO) — not a `PI-0016` review. This decision therefore adopts `PI-0016` §D's evidence
standard by reference (primary-source discipline, fact/inference/judgment separation,
disconfirming-evidence search) because it is directly applicable and already proven, without
importing `PI-0016`'s comparator-set/two-recommendation-output machinery, which presumes an
existing conviction rating to reassess that none of these four companies yet has.

**Why margin-relevance evidence is required now, not deferred to a later refresh.** `OPS-0006` §4
Milestone 3 added this requirement precisely because earlier first-coverage records (COST, XOM,
NVDA, GEV, ISRG, TMO, TSM) were built before that requirement existed. Building it into this
batch's authorization from the start, per `OPS-0006` §4/§16, avoids creating an eighth-through-
eleventh record that would immediately need its own future margin-relevance refresh — the same
smallest-reversible-step discipline `TGT-0001`/`PI-0016`/every backtest closure in `CLAUDE.md`'s
Decisions Log already applies.

## Alternatives Considered

- **Authorize all eleven uncovered `semis` names in one Milestone 3 batch.** Rejected — the audit
  artifact's own grouping is advisory, and a smaller, evidence-coherent, individually-reviewable
  batch is easier to implement, validate, and independently review in one bounded PR, consistent
  with the "smallest reversible next step" discipline this repository applies throughout (`PI-0003`'s
  one-company pilot before any second company; `MARGIN-0005`'s ≤3-PR S2 ceiling; `OPS-0006` §5's
  own Milestones-1-2-as-one-bounded-unit reasoning).
- **Authorize a single company first** (e.g. ASML alone, mirroring `PI-0003`/`PI-0005`'s original
  one-company-at-a-time pattern). Rejected — the objective explicitly requested a four-company
  batch, and unlike `PI-0003`'s original single-company pilot (which was testing whether the
  Company Intelligence *workflow itself* generalized beyond one hand-authored example), this
  batch's whole justification rests on comparative, shared-driver evidence (§B.12, §B.16) that a
  single-company authorization cannot produce — the workflow itself is already proven across seven
  companies and two prior multi-company batches.
- **Include AVGO, AMD, MU, MRVL, WDC, INTC, or SKHY in this batch** (other uncovered `semis`
  members). Rejected — each occupies a materially different value-chain position (chip design,
  foundry-adjacent, memory, or otherwise) than the equipment sub-segment ASML/AMAT/KLAC/LRCX
  share, diluting the batch's coherence and its comparative evidence value without adding a
  compensating benefit; each remains individually eligible for its own future, separately
  authorized batch.
- **File under `OPS-0007`.** Rejected — see Rationale above; wrong category, and inconsistent with
  both the `README.md` convention and the audit artifact's own stated expectation of a `PI-XXXX`
  filing for exactly this kind of authorization.
- **Adopt `PI-0016`'s full committee-review framework for this batch.** Rejected — see Rationale
  above; `PI-0016` presumes an existing record and conviction rating to reassess, which none of
  these four companies has. Adopting only its evidence-standard discipline (§D) by reference is
  the correct-weight fit; importing the comparator/two-recommendation-output machinery designed
  for reviewing existing conviction would be process mismatched to first-coverage creation.
- **Let this filing itself begin the research.** Rejected — `OPS-0006` §5 requires the
  authorization to precede the research PR, not accompany it, the same separation `PI-0013`'s
  rationale already established between authorization and findings as distinct governance events.
- **Update `intelligence/freshness_registry.yaml`/`freshness_checkpoints.yaml` in this governance
  PR.** Rejected — both files state they gain a row only for a ticker with "its own existing,
  cited Company Intelligence record," which does not yet exist for any of the four; adding rows
  belongs in the future implementation PR that creates the records themselves, not in this
  authorization-only filing.

## Consequences

**Authorized, effective on this decision's merge:** exactly one Milestone 3 research batch (ASML,
AMAT, KLAC, LRCX), scoped and bounded exactly as stated in §§A-F above, to proceed via its own
later, separate, bounded implementation PR.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record
(`COST`/`GEV`/`ISRG`/`NVDA`/`TMO`/`TSM`/`XOM`, `ai_infrastructure`, `life_sciences_tools_medtech`);
`allocate.py`, `margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every
freshness module, and every test file; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s
research charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, and `constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4 through
9 of WS-0005 remain entirely unauthorized. No second Milestone 3 batch is authorized by this
filing, and none is inferred from its acceptance.

**No research has been conducted, and no research finding, ranking, score, price target, or
automatic implementation is authorized or implied by this decision alone.** A future,
separately-implemented research PR may now begin exactly the batch scoped above; any resulting
Company Intelligence record, freshness-registry update, or later policy consequence remains
subject to that PR's own review, validation, and (for anything beyond Intelligence content) its
own separate future governance decision.
