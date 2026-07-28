---
decision_id: PI-0032
date: 2026-07-28
status: Proposed
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0005, PI-0011, PI-0013, PI-0014, PI-0016, PI-0023, PI-0024, PI-0025, PI-0026, PI-0027, PI-0028, PI-0029, PI-0030, PI-0031, PI-0033]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin/main` fetched.** `git fetch origin main` returned `270b471..db43d8b main -> origin/main`;
  `git rev-parse origin/main` confirmed `db43d8b0e71dcf8915f74d81703e5fe260ecd6ce`, matching this
  session's designated branch's starting commit exactly (`git rev-parse HEAD` on
  `claude/portfolio-hq-m3-governance-paxeee` before branching). Working tree confirmed clean before
  any edit.
- **`db43d8b0e71dcf8915f74d81703e5fe260ecd6ce` is PR #184's merge commit** — confirmed via
  `git show --format="%H %P"`, parents `8768bfddd288bd493357b943d076dd12413b7b7f` (base, PR #182's
  merge commit — `OPS-0009`) and `638dbd93dfa7f239ab18ac3c1c24224c1f6492dc` (reviewed head). PR #184
  independently confirmed `merged: true` via the GitHub API. **Zero open pull requests** confirmed
  live via the GitHub API at this filing's preflight.
- **PR #184 retained the independent retrospective review of PR #181** (`PI-0031`/Batch 9, CVX) and
  synchronized `operations/WORKSTREAMS.yaml` to record: CVX Company Intelligence
  (`intelligence/companies/CVX.yaml`/`CVX.md`) now satisfies all five `OPS-0007` §3 PROVISIONAL
  elements — eligible review, no unresolved material finding, principal acceptance, merge to `main`
  at the reviewed head, and post-merge ancestry/scope/validator/test re-verification — and is
  therefore **PROVISIONAL**. Milestone 3 remains `status: in_progress`.
- **`intelligence/companies/` independently confirmed to hold 39 files** (`intelligence_validator.py`
  run directly: 39 companies, all valid) — ABBV, AMAT, AMD, AMZN, ASML, AVGO, COST, CRM, CRWD, CVX,
  ETN, GEV, GILD, GOOGL, IBM, INTC, ISRG, JNJ, JPM, KLAC, LLY, LRCX, MA, META, MRK, MRVL, MSFT, MU,
  NOW, NVDA, ORCL, PANW, PWR, SKHY, TMO, TSM, V, VRT, XOM. `freshness_validator.py` run clean.
- **`targets.yaml` independently re-parsed in full.** T1 (10 tickers): ASML, TSM, MSFT, GOOGL, META,
  NVDA, GEV, LLY, V, COST — **all ten already carry a Company Intelligence record.** T2 (14 tickers):
  AVGO, AMZN, CEG, PWR, ISRG, TMO, DHR, SYK, MA, BRK.B, WMT, EQIX, MLM, AAPL — AVGO, AMZN, PWR, ISRG,
  TMO, MA are covered (6); DHR and SYK are covered by neither a record nor coverage but are
  explicitly deferred per `PI-0014`; EQIX is explicitly deferred per `PI-0027`; **CEG, BRK.B, WMT,
  MLM, and AAPL remain uncovered with no deferral rationale on record** — exactly the five names
  `PI-0031` §K.2 identified as open. `semis` cluster (13 tickers, `caps.clusters`, ≤25% of book):
  ASML, TSM, NVDA, AVGO, AMD, MU, MRVL, KLAC, LRCX, AMAT, WDC, INTC, SKHY — twelve covered, **WDC is
  the sole uncovered member**, exactly as `PI-0024`/`PI-0031` already recorded. `oil` cluster (XOM,
  CVX, ≤20% of book) is now fully covered (XOM per `PI-0005`, CVX per `PI-0031`/PR #181, PROVISIONAL
  per this filing's own preflight above). `power_infra` cluster (GEV, ETN, VRT, PWR, ≤20% of book) is
  fully covered.
- **Six governed-holding Intelligence gaps confirmed live, matching this filing's expected inventory
  exactly**: WDC (`semis` cluster, `band` tier, 0.75% target, 1.25x cap), CEG, BRK.B, WMT, MLM, AAPL
  (all `T2`, 1.65% target). No other governed holding is uncovered and non-deferred.
- **Sandisk independently confirmed absent** from `targets.yaml` (no `SNDK` or `Sandisk` ticker in
  any tier, cluster, or the crypto sleeve), `holdings.yaml` (no `shares:` entry), and
  `intelligence/companies/` (no `SNDK.yaml`/`SNDK.md` or `Sandisk.yaml`/`Sandisk.md`). Sandisk is not
  a Portfolio-HQ holding under any current authority.
- **Sandisk's current legal identity and ticker — identity verification only, not the substantive
  company research this decision authorizes for a later PR.** This session's own `WebFetch` was
  tested against SEC EDGAR (`sec.gov/cgi-bin/browse-edgar`, a Western Digital 8-K filing URL) and
  against Nasdaq's own corporate-actions notice (`nasdaqtrader.com`) — **both returned HTTP 403,
  blocked at this environment's network-policy layer**, the same class of session-wide primary-source
  block `governance/audits/CVX_PRIMARY_SOURCE_EVIDENCE_RECOVERY_AUDIT_20260728.md` already documented
  for SEC EDGAR and issuer investor-relations domains. `WebSearch` (index-based, not a direct fetch of
  either blocked domain) returned converging corroboration from three independent secondary sources —
  a Nasdaq Trader equity corporate-actions alert (title: "Spin-Off/Distribution Information for
  Western Digital Corporation (WDC)"), two Yahoo Finance articles citing Western Digital's own SEC
  8-K filings by exact filename — all stating: Western Digital Corporation completed the separation
  of its flash/NAND business into an independent public company, **Sandisk Corporation**, effective
  **February 21, 2025**, via a pro rata distribution of 80.1% of Sandisk's outstanding shares to
  Western Digital stockholders (Western Digital retaining ~19.9%); Sandisk Corporation trades on the
  **Nasdaq Stock Market under the ticker `SNDK`**. This matches, and does not contradict,
  `operations/WORKSTREAMS.yaml`'s own existing recorded fact ("WDC is explicitly excluded from this
  batch (Sandisk separation, February 2025)," `PI-0024`'s milestone-3 entry). **This identity fact is
  disclosed as attempted-but-not-directly-inspected primary source, corroborated by converging
  secondary reporting of a primary filing** — it authorizes nothing about Sandisk's business quality,
  financials, or portfolio fit, all of which remain for the later implementation PR's own
  primary-source-first research under `OPS-0008` §2.
- **`governance/decisions.yaml` and `governance/decisions/` independently reconciled**: 43 files under
  `governance/decisions/` (excluding `README.md`) = 43 entries in `governance/decisions.yaml`, no
  orphans, highest filed `PI-####` is `PI-0031`, highest `OPS-####` is `OPS-0009`. **`PI-0032`
  confirmed the next unused decision number** in its series, checked live against both the directory
  and the index, not assumed.
- **`operations/WORKSTREAMS.yaml`, `constitution/INVESTMENT_CONSTITUTION.md`, `OPS-0006`, `OPS-0007`,
  `OPS-0008`, `OPS-0009`, and `PI-0031` read in full this session** (not relied on from memory) to
  confirm the zero-based-research-discipline protocol, the twelve-point capability-based review
  standard, the Research Wave Protocol's default wave size and documented smaller-wave exception, the
  mandatory stop-before-drafting source-readiness gate and its standing evidence-recovery
  pre-authorization, the default two-PR lifecycle with read-only post-merge verification, `OPS-0009`'s
  lane discipline (this filing is Lane G throughout — full weight, no reduction), and `PI-0031` §K's
  Milestone 3 completion standard, all as they apply to this filing.
- **No repository truth conflicts with the principal's stated premise.** WDC, CEG, BRK.B, WMT, MLM,
  and AAPL are confirmed still governed holdings, still lacking Company Intelligence records, exactly
  as the principal's directive states. Sandisk is confirmed absent from every governed source, exactly
  as stated.

The principal has directed preparation of the tenth Milestone 3 batch structure, closing every
remaining governed-holding research requirement `PI-0031` §K identified, together with a bounded
Sandisk candidate-research addition explicitly separated from governed-holding authority. This
decision records that authorization; it performs no research itself.

## Decision

**PI-0032 authorizes exactly two things: (1) six independent governed-holding Company Intelligence
research units — WDC, CEG, BRK.B, WMT, MLM, AAPL — and (2) one bounded Sandisk candidate-research
addition, structurally paired with WDC's own research as a coherent storage-architecture comparison,
but explicitly outside the governed-holding denominator.** This is **evidence development only** — no
research has been performed, and this filing alone authorizes no research finding, Company
Intelligence record, comparison artifact, freshness-registry row, policy change,
tier/target/roster/cluster/cap/allocator change, margin-policy recommendation, holding addition,
trade, or order. **This filing (its own governance PR) authorizes the creation of the
governance-authorization package only** — this `PI-0032` decision file, the companion `PI-0033`
decision file (filed in the same PR, its own separate file per this repository's established
two-decisions-in-one-PR convention — `OPS-0008`/`PI-0027` precedent), `governance/decisions.yaml`,
`operations/WORKSTREAMS.yaml`, and the applicable `CLAUDE.md` Decisions Log entries. It does not
authorize drafting any Company Intelligence record, comparison artifact, or freshness row — those
become authorized to begin only after this governance decision is independently reviewed,
principal-accepted, and merged, exactly as `PI-0023`-`PI-0031`'s own authorization-precedes-research
separation already established.

**This filing is Lane G (Governance authorization) under `OPS-0009` §1** — full weight throughout: no
reduced preflight, no reduced review, no reduced principal-acceptance requirement. Nothing in
`OPS-0009`'s lean lifecycle reduces any control this filing or its later implementation PR must
satisfy.

### A. The six governed-holding research units

Authorizes six **independent single-company research units** — WDC, CEG, BRK.B, WMT, MLM, AAPL —
closing every remaining Milestone 3 governed-holding gap `PI-0031` §K.2/§K.3 named as open (excluding
DHR, SYK, and EQIX, which remain deferred per `PI-0014`/`PI-0027` and are not reopened or included
here; see `PI-0033` for their restatement). **This filing does not fabricate a shared economic
mechanism among CEG, BRK.B, WMT, MLM, and AAPL** — a utility/power-generation company, a diversified
insurance-and-holding conglomerate, a discount/grocery retailer, an aggregates/construction-materials
producer, and a consumer-technology hardware/services company share no common economic driver, no
common value chain position, and no common cluster or theme membership. Each is authorized under
`OPS-0008` §1's smaller-wave exception, individually, precisely because forcing them into one
artificial "wave" would violate the same coherence discipline `OPS-0008` §1 exists to protect —
identical reasoning to `PI-0031`'s own single-company CVX wave, applied here to five names at once
rather than one, each remaining its own independent unit rather than a group.

**WDC is the sixth governed-holding unit and is treated separately below (§B)** — not because its own
required research content differs in kind from the other five, but because the principal has directed
that WDC's research proceed alongside a structurally paired, non-governed Sandisk candidate comparison
(§C), which the other five units do not have.

#### A.1 Required research standard — CEG, BRK.B, WMT, MLM, AAPL (each independently)

For each of these five companies, the later implementation PR's research must establish, at minimum:

1. Economic function and current governed portfolio role (T2, 1.65% target, 1.5x `gates.t1t2_trim_mult`
   ceiling — `CLAUDE.md`'s T1/T2 concentration ceiling; no cluster-cap membership for any of the five).
2. Business model and revenue economics, by segment where applicable (e.g. CEG's generation mix and
   contracted/merchant revenue split; BRK.B's insurance float and wholly-owned/equity-stake operating
   businesses; WMT's US/international/Sam's Club/e-commerce segment mix; MLM's aggregates/asphalt/
   ready-mix product mix — noting MLM's existing role absorbing VMC's exposure per CLAUDE.md's "VMC
   consolidated into MLM" decision; AAPL's hardware/Services segment mix and ecosystem economics).
3. Moat, competitive position, and quality assessment — durable competitive advantages, pricing power,
   switching costs, scale economics, brand, or regulatory position, as applicable to each business.
4. Financial quality — margins, free cash flow, balance-sheet resilience, dividend history and
   coverage where applicable, debt load, and cyclical or defensive behavior.
5. Management and capital-allocation history — dividend policy, buybacks, major acquisition or
   divestiture history, and capital-intensity trends.
6. Major growth drivers and secular or cyclical positioning.
7. Key customers, suppliers, partners, and competitors; substitutes and substitution risk.
8. Material regulatory, litigation, geopolitical, and (where applicable — e.g. CEG's
   nuclear/power-generation regulatory exposure) energy-transition or grid-policy risk.
9. Explicit thesis-break conditions.
10. Actively searched disconfirming evidence.
11. Overlap and correlated-loss analysis against other governed holdings — explicitly checking each
    company against every `caps.clusters` member list and every existing Theme Intelligence record,
    even though none of the five is a current cluster or theme member, to confirm (or correct) that
    absence with evidence rather than assumption.
12. **Business quality assessed as a distinct question from capital priority** — same discipline
    `PI-0027` §B.23, `PI-0028` §B.17, `PI-0029` §B.17, `PI-0030` §B.17, and `PI-0031` §B.17 already
    established: a distinct assessment of quality (items 1-11 above) from a distinct assessment of
    whether the next investment dollar is better spent on this holding than on a governed alternative.
    This comparison must preserve uncertainty and judgment in prose and must not produce a numerical
    score, composite index, or automatic ranking of any kind — advisory research evidence only.
13. **Current governed tier, target, and role, clearly labeled as historical policy, not research
    evidence** — per `OPS-0006` §2/§3 (T2, 1.65% target for all five; no cluster membership for any).
14. **Margin-relevance evidence, factual and advisory only** — cyclicality, drawdown behavior,
    liquidity, leverage, refinancing/funding risk, and correlated-loss behavior with any other governed
    holding — with no recommendation to borrow, no safe-leverage calculation, and no deployment-timing
    or margin-ceiling conclusion of any kind.
15. Evidence-driven freshness cadence and refresh triggers, per §E below — no universal cadence.
16. **External opportunities or replacements only as unauthorized future leads** — advisory candidate
    list only, no holding add, no tier/target assignment, no mechanical ranking, no batch expansion.

#### A.2 What may not be assumed shared across the five

The later implementation PR must not construct, imply, or rely on any shared-mechanism narrative,
comparison artifact, or cross-referencing structure treating CEG, BRK.B, WMT, MLM, and AAPL as a
"batch" in the sense `PI-0023`-`PI-0030` used that word. Each of the five companies gets its own
independent Company Intelligence record, evaluated and researched entirely on its own terms; nothing
in this decision authorizes a `BATCH10`-style comparison artifact spanning them.

### B. WDC — the sixth governed-holding unit, researched alongside the Sandisk candidate comparison

WDC (governed `semis`-cluster and `band`-tier holding, the cluster's sole remaining uncovered member)
receives the same required research standard as §A.1 above, items 1-16, adapted to WDC's own
business: current hard-disk-drive (HDD) manufacturing and storage-solutions economics post-separation;
enterprise/cloud/hyperscaler versus consumer/client demand mix; capital intensity and manufacturing
footprint; competitive position against other storage providers; and explicit disclosure of what
economic exposure WDC retains and what it divested in the February 2025 Sandisk separation. WDC's
research is **not** merged into a shared-mechanism narrative with CEG/BRK.B/WMT/MLM/AAPL — its only
structural pairing, authorized specifically by this decision, is with the Sandisk candidate comparison
in §C below.

### C. Sandisk — bounded candidate research, structurally paired with WDC, outside governed authority

**Sandisk is authorized for exactly one purpose: a comparative research artifact examining its
economic relationship to WDC**, the two companies' shared post-separation history, and whether Sandisk
would add genuinely distinct portfolio exposure if ever separately considered for governed status —
**a question this decision explicitly does not answer or pre-judge.**

**Sandisk's classification, binding on this filing and any later implementation PR without
exception:**

1. **Candidate research only** — Sandisk is researched exactly as a prospective external candidate,
   never as a current or presumed-future holding.
2. **Outside the governed 62-company (T1/T2/ETF/band/spec, ex-crypto) coverage denominator** — Sandisk
   is not counted toward, and its coverage or non-coverage does not affect, any Milestone 3 completion
   criterion stated in `PI-0031` §K, including criterion 4's "every remaining uncovered company is
   covered, explicitly deferred, or reassigned" — that criterion is scoped to governed holdings only,
   and Sandisk was never a governed holding to begin with.
3. **Not a Milestone 3 completion prerequisite** — Milestone 3 may reach its future completion
   determination whether or not Sandisk research exists, is complete, or reaches any particular
   conclusion.
4. **Not a holding** — no `holdings.yaml` entry, no `shares:` row, no portfolio value attribution of
   any kind.
5. **Not assigned any governed tier, target, weight, or capital priority** — no `targets.yaml` entry
   under any tier; no cluster or theme membership; no `portfolio_role_ref` value implying governed
   status (a candidate research record, if created, uses a plainly candidate-labeled role reference,
   never one of the seven current governed-tier labels used elsewhere in `intelligence/companies/`).
6. **Not authorized for purchase** — this decision authorizes no trade, no buy, no allocation, and no
   `holdings.yaml`/`targets.yaml` change of any kind arising from Sandisk research, regardless of what
   that research finds.

**Required comparative WDC/Sandisk artifact — the implementation PR must address, at minimum:**

1. Post-separation business boundaries — exactly what each company retained, divested, or continues to
   share (e.g. transitional supply agreements, if any, disclosed in either company's own filings).
2. HDD (WDC) versus NAND/flash (Sandisk) economics — cost structure, capital intensity, manufacturing
   process, and demand-cycle differences.
3. Complementary and substitutive storage use cases — where HDD and flash serve the same demand pool
   versus distinct ones.
4. Cloud, hyperscaler, enterprise, OEM, and consumer demand exposure for each.
5. AI and data-growth sensitivity for each — **without assuming AI demand proves a thesis for either
   company**; the research must state the evidence for and against that sensitivity translating into
   durable economics, not assert it.
6. Pricing cycles and supply discipline in both HDD and NAND/flash markets.
7. Capital intensity and manufacturing dependencies (fabrication facilities, joint ventures, key
   equipment suppliers — noting any overlap with already-covered `semis`-cluster-equipment names from
   `PI-0023`).
8. Customers, competitors, and substitutes for each, including each other where relevant.
9. Correlated-loss and duplicate-exposure risk — whether a downturn in one storage sub-market would be
   expected to move both companies together, separately, or in offsetting directions.
10. **Whether Sandisk would provide a genuinely distinct economic role or simply add another cyclical
    storage exposure** — stated as an open research question with evidence on both sides, never as a
    predetermined conclusion.
11. **Zero-based comparison against WDC and the next-best use of capital** — per `OPS-0006` §2/§3,
    formed on Sandisk's own economic merits before any comparison to WDC's existing governed status,
    and explicitly separating (a) Sandisk's business quality, (b) Sandisk's portfolio fit if it were
    ever considered, (c) capital priority relative to WDC and other governed alternatives, and (d)
    WDC's own current governed policy — the same four-way separation required for every other unit in
    this decision (§A.1 item 12), applied here with the added dimension of Sandisk's non-governed
    status.

**What the Sandisk research may and may not conclude:**

- **May** state, as an advisory research finding, whether Sandisk appears to deserve future policy
  consideration — i.e., whether a future, separately authorized decision naming Sandisk specifically
  should be proposed.
- **May not** add Sandisk to the portfolio, assign it any tier/target/weight, or authorize any trade.
- **May not** automatically create, trigger, or imply a policy-change proposal — any future step
  addressing Sandisk's governed status requires its own separate, later, explicit governance decision,
  naming Sandisk specifically, following exactly the discipline `PI-0016` already established for
  single-company review and `PI-0023`-`PI-0031` already established for first-coverage batches.

### D. Implementation structure

Once this decision merges, **one later, separate, bounded implementation PR** (not opened by this
filing) may include all six governed-holding units (WDC, CEG, BRK.B, WMT, MLM, AAPL) plus the Sandisk
candidate comparison, **provided**:

1. Source readiness (`OPS-0008` §2's mandatory stop-before-drafting gate) is satisfied independently
   for each company — a block on one company's primary sources does not excuse skipping the gate for
   any other.
2. Findings and corrections remain attributable **per company** — no finding about one company may be
   silently generalized to another.
3. **No false shared comparison is created beyond the authorized WDC/Sandisk wave** — CEG, BRK.B, WMT,
   MLM, and AAPL each remain independent units; no comparison artifact spanning any subset of them is
   authorized by this decision.
4. **Any evidence-blocked company may be removed from scope without blocking the other independently
   complete units** — if primary-source access remains blocked for one company even after `OPS-0008`
   §2's standing evidence-recovery pre-authorization is exercised, that company's record is deferred
   (disclosed, not silently dropped) while the remaining companies' independently complete records may
   still proceed to review and merge. This differs from `PI-0031` §D.5's single-company CVX rule only
   in that CVX had no sibling units to preserve — here, partial completion across six-plus-one
   independent units is explicitly permitted rather than forcing an all-or-nothing outcome.
5. The implementation remains reversible and reviewable — each company's YAML/Markdown pair, and the
   Sandisk comparison artifact, must be separable in the diff (distinct files) so that a reviewer or a
   future correction can address one unit without touching another.
6. The PR remains draft until exact-head review, per `OPS-0007` §1 and `OPS-0008` §§2/4.

**This governance filing does not itself authorize drafting.** Drafting begins only after `PI-0032` is
independently reviewed, principal-accepted, and merged.

### E. Evidence, freshness, and review standard (applies to every unit, including Sandisk)

1. Attempt direct inspection of SEC filings (10-K/10-Q/8-K), company investor-relations releases, and
   earnings materials for factual, non-predictive claims, per `OPS-0008` §2's mandatory
   stop-before-drafting gate — for every one of the seven names in this decision (six governed
   holdings plus Sandisk), independently.
2. If primary access is blocked for one or more names, the implementing session must stop before
   drafting substantive economic content for those names and may engage `OPS-0008` §2's standing
   evidence-recovery pre-authorization (an eligible independent reviewer per `OPS-0007` §1) before
   resuming — the same standing method this filing's own preflight used for Sandisk's identity
   verification, at a bounded, narrower scope (identity only, not substantive research).
3. Preserve claim-level provenance; distinguish filed fact, issuer statement, guidance, allegation,
   inference, uncertainty, and judgment throughout.
4. Disclose inaccessible sources rather than representing snippets as inspected evidence — a blocked
   primary source is labeled "attempted but not directly inspected," never merged into the same
   citation as secondary or WebSearch-derived evidence as if both were equally verified.
5. Retain attributable evidence sufficient for independent review; preserve unresolved discrepancies
   and negative findings.
6. Each new record must define an evidence-driven, proportional refresh plan — no universal cadence —
   per `OPS-0006` §12, drawing on candidate triggers (earnings/guidance, 10-K/10-Q/8-K filings, major
   M&A/financing/credit events, management changes, material regulatory/litigation/geopolitical
   developments) selected per company.
7. **`OPS-0007` §1's twelve-point capability-based independent-review standard applies to the future
   implementation PR in full** — exact-head anchoring, retained attribution, bounded correction and
   re-review for any material finding, explicit principal acceptance before merge.
8. New `intelligence/freshness_registry.yaml`/`intelligence/freshness_checkpoints.yaml` rows —
   `checkpoint_status: pending`, `monitoring_enabled: false`, `enrollment_authority`/
   `company_record_authority: PI-0032` — for each of the six governed-holding units. **Sandisk
   receives no freshness-registry or freshness-checkpoint row** unless and until a future, separate
   decision brings it into governed status — a candidate research record, if created, is not enrolled
   in the same monitoring infrastructure as a governed holding's record.

### F. Hard prohibitions

This decision and any later implementation authorize none of the following, under any interpretation:

- Any change to WDC's, CEG's, BRK.B's, WMT's, MLM's, AAPL's, Sandisk's, or any other ticker's
  holdings, targets, tiers, roles, clusters, caps, or weights.
- **Adding Sandisk (`SNDK` or any other ticker) to `holdings.yaml` or `targets.yaml`, under any
  circumstance, by this decision or any later implementation PR it authorizes.**
- Assigning Sandisk any tier, target, weight, cluster, theme, or capital-priority conclusion.
- Any trade, buy, trim, exit, margin deployment, or safe-leverage-level recommendation.
- Any capital-priority ranking or mechanical/composite score of any kind, within any unit or against
  any other holding or candidate.
- Making Intelligence mathematically load-bearing to the allocator in any way.
- Modifying any existing Company or Theme Intelligence record (the 39 currently covered tickers,
  `ai_infrastructure`, `life_sciences_tools_medtech`), **including CVX's or XOM's.**
- Fabricating a shared economic-mechanism comparison among CEG, BRK.B, WMT, MLM, and AAPL, or any
  subset of them.
- Any research or Company Intelligence record for **any ticker not named in this decision or in the
  companion `PI-0033`** — including any name `PI-0033` disposes of, any name already deferred
  (DHR, SYK, EQIX), and any candidate other than Sandisk.
- Any modification to `MARGIN-0005` research, its protocol, or its pre-registration, and any
  consumption of any `MARGIN-0005` trial.
- **Beginning Milestone 4** (portfolio relationship mapping) beyond the bounded, unit-internal overlap
  evidence required inside §A.1 item 11 and §C.
- Automatic authorization of an eleventh Milestone 3 batch, any further candidate research beyond
  Sandisk, or any Milestone 4-9 work.
- Beginning, advancing, or drawing on `OPS-0007` §8 step I in any way.
- Beginning any zero-based unlevered-portfolio redesign or margin-policy study of any kind.
- Any amendment to `constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.
- Any automated scanner, scheduler, notification system, or external-data integration.
- Any generated report replacing an authoritative Company Intelligence record.
- Any investment recommendation of any kind, for any governed holding or for Sandisk.
- **Declaring Milestone 3 complete** — see §G below.

### G. Milestone 3 completion boundary

**Milestone 3 remains in progress after this governance filing.** This decision authorizes research
preparation only — the later implementation PR's drafting, independent review, correction if needed,
principal acceptance, merge, and post-merge verification all remain outstanding steps, for every one
of the six governed-holding units.

- **A later, separate completion-determination decision must evaluate all seven of `PI-0031` §K's
  accepted completion criteria** before Milestone 3 may be marked `complete` — this filing does not
  perform that evaluation and does not itself satisfy any of the seven criteria merely by existing.
- **Sandisk cannot delay Milestone 3 completion because it is not a governed holding** — `PI-0031` §K
  criterion 4 ("every remaining uncovered company is covered, explicitly deferred, or reassigned")
  is scoped to governed holdings; Sandisk was never within that scope, and its research reaching any
  particular state (complete, deferred, inconclusive) has no bearing on that criterion.
- **Completion of the six governed-holding units named in this decision does not authorize Milestone
  4.** Milestone 4 remains unauthorized until a later, separate decision determines `PI-0031` §K's
  criteria have been met and separately authorizes Milestone 4's own scope.
- **No portfolio mutation is authorized** by this decision or by any research it prepares — every
  `holdings.yaml`/`targets.yaml` value, every tier, cluster, cap, and margin parameter remains exactly
  as currently governed throughout and after this filing.

### H. Governance package scope (this filing)

This decision's own implementation — the governance PR itself, not the future research PR — touches
exactly:

1. `governance/decisions/PI-0032-ws0005-milestone3-remaining-governed-holdings-and-sandisk-candidate.md`
   (this file).
2. `governance/decisions/PI-0033-ws0005-milestone3-residual-deferrals.md` (the companion decision,
   filed in this same PR as its own separate file — see `PI-0033` itself).
3. `governance/decisions.yaml` (index regeneration: two new entries, `PI-0032` and `PI-0033`).
4. `operations/WORKSTREAMS.yaml` (WS-0005 Milestone 3 gate: record both decisions' proposed status,
   the six governed-holding research requirements, Sandisk's candidate-only classification, and the
   fourteen-plus-three deferral count — using only `OPS-0001`'s existing schema and status
   vocabulary; no new field, no new status value; Milestone 3 remains `status: in_progress`;
   Milestones 4-9 remain `status: proposed`, unauthorized, unchanged).
5. The applicable `CLAUDE.md` Decisions Log entries recording both decisions as proposed in this draft
   PR, not accepted, merged, or controlling.

**No other file is touched by this governance filing.** No Company Intelligence record, comparison
artifact, freshness-registry or freshness-checkpoint row, and no test or validator file is created,
modified, or authorized to be created by this filing — those belong exclusively to the later, separate
implementation PR authorized in §D.

### I. Effectiveness, review, and merge gates

- **This authorization becomes effective only when this governance PR merges to `main`.** Before that,
  nothing in §§A-F is authorized to begin.
- **The later Company Intelligence implementation must occur in its own separate, bounded PR** — never
  combined with this governance filing, and never opened before this filing merges.
- **That implementation PR must remain in draft state until it has been independently reviewed** —
  applying `OPS-0008` §2's mandatory stop-before-drafting gate first, for every one of the seven names.
- **An eligible independent review must be retained and anchored to the exact implementation PR head**
  that ultimately merges, per `OPS-0007` §1's capability-based standard.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready — per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Principal acceptance is required before merge** — explicit, at the exact head being merged.
- **Post-merge verification is required immediately, by the merging session, as one continuous step
  with the merge itself** — per `OPS-0009` §9 — recorded per `OPS-0008` §4's read-only-by-default
  convention rather than through a routine dedicated reconciliation PR.
- **Completion of this batch does not authorize an eleventh Milestone 3 batch, further candidate
  research, or any Milestone 4 work**, and does not begin or advance `OPS-0007` §8 step I.

This governance PR itself is subject to the same discipline: it must remain in draft state, gain its
own eligible independent review anchored to its exact head per `OPS-0007` §1, and receive explicit
principal acceptance before it may be marked ready or merged. This decision does not mark itself, or
authorize marking itself, ready for merge — consistent with `OPS-0009` §13's rule that a Lane G filing
may not invoke its own lanes to reduce its own review or merge requirements (not directly applicable
here since `OPS-0009` governs itself, but the same discipline is restated for this filing by its own
terms).

## Rationale

**Why six independent units, not a fabricated six-company wave.** `PI-0031` §K.2/§K.3 named exactly
five ungoverned, non-deferred T2 gaps (CEG, BRK.B, WMT, MLM, AAPL) plus WDC as the sole uncovered
`semis`-cluster member — six names with no shared economic mechanism whatsoever. `OPS-0008` §1
requires a documented common economic mechanism for a genuine wave and explicitly permits a smaller
wave, down to one company (`PI-0031`'s own CVX precedent), when no larger coherent group exists.
Treating six unrelated companies as one comparison-artifact "batch" would either force an artificial
narrative (violating §1's coherence requirement in the same way an overly narrow wave violates its
wave-size guidance) or produce a comparison artifact with nothing genuine to compare. Authorizing six
independent units — each still gated by the full `OPS-0008`/`OPS-0007` review discipline — closes the
coverage gap without inventing false coherence.

**Why WDC and Sandisk are structurally paired.** Unlike the other five, WDC has a specific, evidenced,
already-recorded structural relationship to a real economic entity outside the governed roster: its
own February 2025 separation of the Sandisk flash business, already noted in this repository's own
`operations/WORKSTREAMS.yaml` (`PI-0024`'s Batch 2 entry: "WDC is explicitly excluded from this batch
(Sandisk separation, February 2025)"). The principal's request to examine WDC and Sandisk together
is not an artificial pairing — it is the one genuine, already-documented structural relationship in
this batch, and researching WDC's post-separation economics without also examining what it separated
from would be incomplete on its own terms.

**Why Sandisk is bounded so explicitly.** This repository's entire Intelligence architecture (`PI-0001`
onward) governs only companies that are, or are being evaluated for, a Portfolio-HQ holding role.
Sandisk is neither. Without an explicit, repeated classification (candidate-only, outside the governed
denominator, not a Milestone 3 prerequisite, no tier/target/weight, not authorized for purchase), a
future reader could mistake Sandisk research for governed-holding research, or mistake this filing for
an implicit step toward adding Sandisk to the portfolio. Stating the boundary five separate ways in §C
follows the same repetition-for-clarity discipline `OPS-0008` §12 already used for its own hard
boundaries.

**Why `PI-####`, not a new `OPS-####`.** Same category and reasoning as every prior Milestone 3 batch:
this is Company Intelligence research-authorization content (`category: portfolio_intelligence`),
filed in the `PI-####` series per `governance/decisions/README.md`'s convention.

**Why first-coverage discipline, not `PI-0016`'s committee-review framework.** None of the six governed
holdings, and Sandisk, has an existing Company Intelligence record — this is first-coverage record
creation for all seven, identical in kind to `PI-0023`-`PI-0031`.

**Why status: Proposed, not Accepted, in this file's own frontmatter.** This decision has not yet been
independently reviewed or principal-accepted at the time of filing — `governance/decisions/README.md`'s
status vocabulary (`Proposed | Accepted | Superseded | Archived`) names exactly this state. The
decision's own text throughout states it is not yet effective; the frontmatter matches that text
precisely rather than anticipating a review outcome that has not yet occurred.

## Alternatives Considered

- **Force all six governed-holding gaps plus Sandisk into one `OPS-0008`-style 5-6-company wave with a
  fabricated shared narrative.** Rejected — no genuine common economic mechanism exists among a
  utility, an insurance/holding conglomerate, a retailer, a materials producer, and a consumer-tech
  company; `OPS-0008` §1 exists precisely to prevent this kind of forced coherence.
- **Split into six or seven separate governance filings, one per unit.** Rejected — all six
  governed-holding gaps were identified together by `PI-0031` §K and share the same authorization
  logic (closing the last named Milestone 3 gaps); filing them together, as independent units within
  one decision, follows the same efficiency reasoning `OPS-0008`/`OPS-0009` already established without
  sacrificing per-unit independence.
- **Omit Sandisk entirely from this filing, leaving it for a separate future request.** Rejected —
  the principal explicitly requested a bounded Sandisk candidate-research addition now, structurally
  paired with WDC's own research; deferring it to an unspecified future filing would not serve that
  request and the bounding language in §C fully contains the risk of scope creep.
- **Treat Sandisk as a seventh Milestone 3 "batch member," counted toward Milestone 3 completion.**
  Rejected per the principal's explicit instruction — Sandisk is not a governed holding and was never
  part of the 62-company denominator `PI-0031` §K's criteria measure against.
- **Authorize the implementation PR to proceed even if one company's primary sources remain blocked
  after evidence-recovery, forcing an all-or-nothing outcome across all seven names.** Rejected — §D.4
  explicitly permits partial completion so that six-plus-one independent units are not held hostage to
  a single blocked name, while still requiring disclosure rather than silent narrowing.

## Consequences

**Authorized, effective on this decision's merge:** exactly six independent governed-holding Milestone
3 research units (WDC, CEG, BRK.B, WMT, MLM, AAPL) and one bounded Sandisk candidate-research addition
structurally paired with WDC, scoped and bounded exactly as stated in §§A-G above, to proceed via one
later, separate, bounded, draft-until-independently-reviewed implementation PR, under `OPS-0008`'s
Research Wave Protocol v1 (independent-unit application) and `OPS-0009`'s Lane G discipline.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record (the 39 currently
covered tickers, `ai_infrastructure`, `life_sciences_tools_medtech`), **including CVX's and XOM's**;
`allocate.py`, `margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every
freshness module, and every existing test; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s
research charter and trial ceiling; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
and `constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely unauthorized,
and `OPS-0007` §8 step I is neither begun nor advanced by this filing. **No name other than WDC, CEG,
BRK.B, WMT, MLM, AAPL, and Sandisk is authorized for any research by this decision.**

**No research has been conducted, and no research finding, ranking, score, price target, holding
addition, or automatic implementation is authorized or implied by this decision alone.** No investment
recommendation is made or implied, for any governed holding or for Sandisk. A future, separately
implemented, draft-until-independently-reviewed research PR may begin exactly the units scoped above
only after this decision itself merges; any resulting Company Intelligence record, comparison
artifact, freshness-registry update, or later policy consequence — including any future decision on
Sandisk's governed status — remains subject to that PR's own independent review, principal acceptance,
validation, and its own separate future governance decision.
