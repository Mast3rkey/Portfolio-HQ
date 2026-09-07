---
decision_id: CONTENDER-0001
date: 2026-08-06
status: Proposed
category: contender_universe_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, OPS-0015, OPS-0016, PI-0016, PI-0031, PI-0035, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, REL-0001, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, XASSET-0001]
supporting_artifact: null
file: governance/decisions/CONTENDER-0001-universal-contender-universe-principle.md
---

## Context

### Authority for this unit

The human repository principal authorized exactly one small, coherent Lane G (`OPS-0009` §1)
governance PR containing two separate but coordinated decision records: this one (the universal
contender-universe principle) and `XASSET-0001` (the cross-asset whole-portfolio allocation
architecture). This filing authorizes architecture and sequencing only. It does not authorize
building a contender registry, normalizing any ticker, researching any ticker, reviving any
historical candidate, or classifying any additional equity, ETF, or cryptocurrency.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. Working directory
  `/home/user/Portfolio-HQ`, branch `claude/cross-asset-contender-architecture-trqpks`, working tree
  clean at session start.
- **`origin/main` fetched and reconciled.** Local branch and `origin/main` both confirmed identical
  at `f71ea3bb1428445023c4fa582ed953ae409ba070` — the merge commit of PR #255 (`TIER-0007`).
- **Zero open pull requests** confirmed live via the GitHub API (`state: open` returned an empty
  list) — no competing mutation lane.
- **PR #255's full lifecycle independently re-verified**, not assumed from the task brief: three
  independent review rounds (`4869718735` CHANGES REQUIRED 0/2/1/0; `4869945654` CHANGES REQUIRED
  0/1/1/0; `4870096664` DELTA APPROVED — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0/0),
  explicit principal acceptance at exact head `4a4408ab133b8ebb58309d607f397f37853bfaa6`
  (`issuecomment-5199184589`), merged (`merged: true`, `merged_at: 2026-08-06T01:00:24Z`), exact-head
  CI `completed`/`success` (check run `92485616796`, workflow run `31059983036`). Current `main`
  confirmed to be exactly that merge commit.
- **Decision catalog** independently rebuilt via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **81 decisions, `issues == ()`**. `governance/decisions/` independently confirmed to hold 81 `.md`
  files besides `README.md`, reconciling 1:1 against `governance/decisions.yaml`'s 81 rows.
  Full-repository grep confirms `TIER-0007` is the highest filed decision of any prefix touched by
  this session.
- **Next unused workstream identifier** independently derived from `operations/WORKSTREAMS.yaml`:
  `WS-0001` through `WS-0013` all exist; **`WS-0014` is the next unused identifier**, confirmed by a
  full-file grep for `WS-00\d{2}` returning no `WS-0014` hit anywhere in the repository.
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new
  decision domain needs one — not pre-declared in advance") was independently applied, not assumed:
  a repository-wide, case-insensitive grep for `CONTENDER-[0-9]` and `XASSET-[0-9]` across
  `governance/decisions.yaml`, every file under `governance/decisions/`, `operations/WORKSTREAMS.yaml`,
  and `CLAUDE.md` returned **zero hits for either string**, confirming both as genuinely new decision
  domains rather than a fit for any existing prefix (`PI-####` is frozen, one-way, non-relational
  Company/Theme Intelligence per `PI-0006` and does not fit a cross-cutting universe-eligibility
  principle spanning every asset type in the repository, not just companies; `TIER-####` is
  WS-0005-Milestone-5/6/7-specific and scoped to the 27-equity cohort by `TIER-0004`/`TIER-0005`'s own
  text; `REL-####` is the closed twelve-item relationship-primitive taxonomy under `REL-0001`, a
  different subject entirely; `OPS-####` is reserved for workstream-register mechanics and
  cross-cutting process protocol, not asset-eligibility doctrine; `PHQ-####` is reserved, per
  `PHQ-2026-01`'s own text, for the separate out-of-repository Portfolio-HQ committee process).
- **`WS-0005` and `WS-0013`'s live text independently re-read in full** (not summarized) — see §D and
  `XASSET-0001` §J for the exact quoted gate text each decision binds to.
- **Exactly one `priority: primary` workstream** confirmed at the YAML-field level: `WS-0005`
  (`operations/WORKSTREAMS.yaml` line 543). Every other workstream (`WS-0001`–`WS-0004`,
  `WS-0006`–`WS-0013`) carries `priority: secondary`.
- **Live `targets.yaml`** independently re-read: 36 `destination:` rows — 27 equities, SPY/VEA/VWO,
  GLD, BTC/ETH/SOL, RESERVE/CASH — confirming the task brief's described state exactly.
- **Live Company Intelligence and classification state** independently re-verified:
  `intelligence/companies/` holds 53 records; `intelligence/classification/` holds exactly 27 sealed
  ticker records plus `COHORT_MANIFEST.yaml`; `classification_validator.py` reports `OK (28 result(s))`
  (27 records + 1 manifest); `relationship_validator.py` reports `OK (13 record(s))`. No ETF-, crypto-,
  reserve-, GLD-, or debt-specific Intelligence or classification framework exists anywhere in the
  repository (confirmed by grep — no schema, validator, or record of that shape exists). No
  `intelligence/contenders/` or equivalent open contender registry exists anywhere in the repository.

## Decision

### A. The universal contender principle

The 27 sealed Milestone 6 equity classifications (`intelligence/classification/*.yaml`, sealed under
`TIER-0002`/`TIER-0003`/`TIER-0004`/`TIER-0005`, implemented by PR #253, completion determined by
`TIER-0006`) are **Portfolio-HQ's first completed blind-classification cohort — not the permanent or
exhaustive contender universe.**

**Every genuine, valid investable ticker represented anywhere in Portfolio-HQ is eligible for governed
contender screening**, whether it appears as:

- a current holding (`holdings.yaml`);
- a current target (`targets.yaml`);
- a gated name (`gates.yaml`);
- a retained or historical Company Intelligence record (including the 26 non-canonical retained
  records `PI-0035` classified "retained/historical-advisory/non-current for Milestone 3 accounting");
- a capital-priority comparator named in any committee review, batch comparison artifact, or
  `intelligence/relationships/` record;
- a relationship or theme reference (`intelligence/relationships/`, `intelligence/themes/`);
- a chart-covered ticker (`CHART-0001`/`CHART-0002`'s governed chart library);
- a prior holding no longer tracked in `holdings.yaml`;
- a disclosed external-opportunity lead (e.g., a batch comparison artifact's advisory "external
  opportunity/replacement-candidate scan," per `PI-0023`'s own authorized shape);
- another genuine governed Portfolio-HQ project reference (a decision file, a workstream register
  entry, a retained audit artifact, a research protocol).

**Current holdings, targets, tiers, gates, classifications, or canonical-population membership do not
by themselves determine inclusion or exclusion** from future contender screening. A ticker's absence
from the current 27-name canonical equity roster, its gated status, or its "retained/historical"
Company Intelligence classification is not, by itself, a disqualification from future evaluation —
just as presence in that roster or in a sealed classification is not, by itself, a guarantee of
continued inclusion. Both directions require evidence-based screening, not status inheritance.

### B. Contender status creates evaluation eligibility only

**Contender status creates evaluation eligibility only. It creates no holding, target, tier, role,
allocation, gate change, trade, or policy authority.** Identifying a ticker as a genuine contender —
whether through this principle's own future normalization work or through any prior or future
Portfolio-HQ research artifact — does the following and nothing more:

- it makes the ticker eligible for future, separately authorized research-readiness screening and,
  eventually, asset-appropriate blind classification (`XASSET-0001` §C);
- it does **not** add the ticker to `holdings.yaml` or `targets.yaml`;
- it does **not** assign a tier, role, weight, target percentage, or gate status;
- it does **not** authorize a trade, an order, or a margin-funded purchase;
- it does **not** by itself change any allocator output, cluster cap, or issuer-look-through
  measurement;
- it does **not** constitute investment advice, a buy/sell/hold recommendation, or a price target.

A future contender registry (not authorized by this filing — see §F) records eligibility and
disposition, not investment merit or priority. Merit and priority remain the separately governed,
asset-appropriate blind-classification and capital-priority-comparison work `XASSET-0001` bounds.

### C. Raw ticker occurrence is not proof of investability — normalization is required

Raw ticker-string occurrence anywhere in this repository is **not sufficient proof of investability**.
A future contender-normalization unit (not authorized by this filing — see §F) must classify every
raw ticker-shaped string it finds into one of at least the following categories before treating it as
a genuine candidate:

1. **genuine investable ticker** — a real, currently tradeable equity, ETF, or cryptocurrency,
   confirmed against a live or authoritative reference, not merely present as a string;
2. **test/fixture symbol** — a ticker-shaped string used only in test code, synthetic data, or
   documentation examples (e.g., `test_classification_validator.py`'s synthetic records), never a
   candidate;
3. **benchmark or index reference** — a symbol used only as a comparison benchmark or index proxy,
   not itself a position candidate unless independently also a genuine holding-eligible instrument
   (e.g., an index ticker cited in prose but never purchasable directly);
4. **alias or brokerage-convention variant** — the same underlying instrument under a different
   symbol convention (the repository's own confirmed precedent: `BRK.B` vs. Yahoo's `BRK-B`,
   corrected in `earnings.py`'s `_YAHOO_SYMBOL` map) — normalized to one canonical symbol, not
   double-counted as two candidates;
5. **malformed or incomplete symbol** — a string that is not a valid ticker at all (a typo, a
   truncated reference, a placeholder);
6. **obsolete, acquired, or delisted issuer** — a ticker that once traded but no longer does (the
   repository's own confirmed precedent: `PI-0032`'s WDC/Sandisk separation, where Sandisk (SNDK)
   was explicitly classified "candidate research only... not a holding, not assigned any tier/target/
   weight/capital priority, and not authorized for purchase under any circumstance" pending its own
   separate future authorization);
7. **synthetic or placeholder row** — a row that exists in a schema, template, or generated report
   for structural reasons, not because it names a real instrument.

Only category 1 (and, after normalization, category 4's resolved canonical form) may ever become a
genuine contender under §A. Categories 2, 3, 5, 6, and 7 must be **normalized and dispositioned** —
explicitly recorded as non-candidates with a stated reason — never silently treated as investment
candidates by omission or by accidental inclusion in a future scan.

### D. Relationship to the sealed 27-equity cohort and Milestone 7

`operations/WORKSTREAMS.yaml`'s `WS-0005` objective (unedited by this filing beyond the additive
record in §F) states its purpose as understanding "every asset from first principles" — this
principle formalizes what "every asset" means at the universe-eligibility level, distinct from and
prior to the classification-framework question `XASSET-0001` addresses. The 27 sealed equity records
remain exactly as `TIER-0006` left them: valid, complete for their authorized cohort, immutable
evidence inputs, not reopened by this filing. They are not the exhaustive equity universe, not the
entire opportunity universe, and not sufficient alone to determine final whole-portfolio targets — see
`XASSET-0001` §B/§H for the full Milestone 7–9 boundary this principle requires.

### E. Who owns future contender-normalization execution

Future contender-registry creation, ticker normalization execution, research-readiness screening, and
additional blind-classification cohorts are the responsibility of `WS-0014` (authorized by
`XASSET-0001` §I, not by this filing) — not `WS-0005` (whose Milestone 3–7 scope remains the sealed
27-equity cohort and its own future baseline reconciliation) and not `WS-0013` (final allocation-
readiness orchestration, non-authorizing). This filing establishes the principle `WS-0014`'s future
work must follow; it does not itself perform any of that work.

### F. Explicit non-authorization

This filing authorizes the **principle** stated in §§A–C. It does not authorize, and no future action
may treat it as having authorized:

- creation of a contender registry (`intelligence/contenders/` or any equivalent structure) of any
  kind;
- ticker normalization execution against any real data source;
- research on any new ticker, of any asset type;
- additional blind classification of any equity beyond the sealed 27;
- ETF or cryptocurrency classification of any kind;
- reviving, re-evaluating, or re-scoring any historical candidate (including any of the ~41
  previously-tracked, currently-untracked `holdings.yaml` tickers referenced in `PHQ-2026-02`'s own
  reconciliation history, or Sandisk/SNDK per `PI-0032`);
- any target, tier, holding, gate, cap, cluster, allocator, margin, ladder, chart, order, or trade
  change;
- any allocation check, live or scenario.

## Rationale

Milestone 6's completion (`TIER-0006`) closed Portfolio-HQ's first blind-classification cohort, and
`PI-0037`'s Milestone 3 completion determination, `PI-0035`'s roster reconciliation, and `PI-0031`
§K's own seven-criterion standard all independently establish that the 27-name canonical equity
roster is itself a *policy-defined* subset (`targets.yaml`'s current `destination:` list), not a
claim about the full universe of tickers that appear, in some form, across this repository's Company
Intelligence, relationship, theme, chart, and governance-decision corpus. Without an explicit
principle, a future session could reasonably — but wrongly — read "27 covered, Milestone 6 complete"
as "the equity opportunity set is now known." This filing forecloses that reading before any future
Milestone 7/8/9 or `WS-0014` work begins, matching this repository's own repeated practice of
defining doctrine before authorizing content work (`TIER-0001`/`TIER-0002` before Milestone 6;
`REL-0001` before Milestone 4's content batches; `TIER-0007` before Milestone 7's content).

The normalization requirement in §C responds directly to a real, disclosed risk this repository's own
history demonstrates: `PI-0032` found WDC's own February 2025 Sandisk separation created exactly the
kind of ambiguous-ticker problem this principle generalizes (a real corporate action producing two
tickers where one previously existed, one of which — SNDK — was carefully kept out of any
authoritative denominator); `PI-0024` similarly excluded WDC from a memory-sector batch on
economic-mechanism grounds even though the ticker string appears throughout the repository's
`caps.clusters` "semis" comment. A universal principle with no normalization discipline would treat
every string occurrence — test fixtures, benchmark tickers, aliases, delisted issuers — as an
undifferentiated pool of "eligible" candidates, which is neither true nor useful. Requiring explicit
disposition (§C) before any string counts as a genuine contender preserves this repository's
demonstrated evidence discipline (`OPS-0008`'s stop-before-drafting gate, `TIER-0004`'s fail-closed
sanitizer design) at the universe-definition layer, before it reaches any classification pipeline.

Assigning future execution to a new workstream (`WS-0014`, authorized in `XASSET-0001` §I) rather than
folding it into `WS-0005` follows the same reasoning `WS-0012`'s filing gave for not folding
`CHART-0002` into `WS-0011`: `WS-0005`'s own milestone sequence (1–9) is specific to the equity
zero-based tier review and its own sealed 27-cohort artifacts; contender normalization and
cross-asset synthesis span every asset type the portfolio holds or could hold, a genuinely broader
scope that deserves its own dependency-tracked register entry rather than an implicit widening of
`WS-0005`'s already-defined roadmap.

## Alternatives Considered

**Fold this principle into `WS-0005`'s existing Milestone 3–7 text instead of a standalone
decision.** Rejected: `WS-0005`'s milestones are specifically scoped to the 27-name canonical equity
roster (`PI-0031` §K, `PI-0035` §C) and its own sealed classification cohort; a universe-eligibility
principle spanning ETFs, cryptocurrency, and every historical/retained ticker in the repository is a
genuinely broader subject that would either dilute `WS-0005`'s own scope discipline or require the
same kind of scope-creep disclaimer every `WS-0005` filing already carries in abundance. A standalone
decision, cross-referenced from `WS-0005`, keeps both scopes legible.

**Automatically treat every ticker string found anywhere in the repository as a contender, with no
normalization step.** Rejected per §C's own reasoning — this would silently promote test fixtures,
benchmarks, and delisted issuers to candidate status, a real and disclosed failure mode this
repository has already encountered once (Sandisk/SNDK) and generalized rather than treated as a
one-off.

**Define a numeric contender-eligibility score or ranking as part of this principle.** Rejected as
exactly the kind of "standing analysis layer" this repository's own Decisions Log has repeatedly
declined (the band-overlay backtest NO-GO, the T1 AI-infra correlation-scan declines, `PI-0016`'s
explicit "no automated cadence, monitoring queue, or full-roster sweep" restriction). Contender status
is binary evaluation-eligibility (§B), never a score.

## Consequences

Once this filing merges, alongside `XASSET-0001`, a future `WS-0014` implementation unit may begin
contender-registry design and normalization work bounded by this principle — but only after its own
separate, future, explicit principal authorization and its own full independent-review/principal-
acceptance/merge/post-merge-verification lifecycle. Until then, this principle changes nothing about
current repository state: no registry exists, no ticker is newly researched, and the 27 sealed equity
records, `holdings.yaml`, `targets.yaml`, `gates.yaml`, and every existing Intelligence/relationship/
classification record remain byte-identical to their `TIER-0006`/PR #255 state. Every future
Milestone 7 (and later Milestone 8/9) filing must henceforth disclose, per `XASSET-0001` §B, that its
own scope is bounded to the 27-equity cohort and does not represent the full contender universe this
filing defines.
