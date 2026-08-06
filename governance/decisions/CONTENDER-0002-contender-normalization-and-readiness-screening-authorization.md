---
decision_id: CONTENDER-0002
date: 2026-08-06
status: Proposed
category: contender_universe_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0011, PI-0016, PI-0023, PI-0024, PI-0027, PI-0029, PI-0032, PI-0033, PI-0035, TIER-0002, TIER-0004, REL-0001, CHART-0001, CHART-0002, PHQ-2026-02, CONTENDER-0001, XASSET-0001]
supporting_artifact: null
file: governance/decisions/CONTENDER-0002-contender-normalization-and-readiness-screening-authorization.md
---

## Context

### Authority for this unit

The human principal authorized exactly one bounded Lane G (`OPS-0009` §1) governance filing that
authorizes `WS-0014`'s first execution unit: contender normalization plus research-readiness
screening — dependency-order step 1 of `XASSET-0001` §J's fourteen-item roadmap, the item both
`CONTENDER-0001` §E and `XASSET-0001` §I assign to `WS-0014` and neither authorizes to begin. This
filing authorizes a later, separate implementation PR only. It performs no scan, produces no
inventory, classifies nothing, and researches nothing itself.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`, branch
  `claude/ws-0014-contender-normalization-jsdxi8`, working tree clean at session start.
- **`origin/main` fetched and reconciled.** Local branch base and `origin/main` both confirmed
  identical at `42949907558afe1577a74e3562e777ba62469d66` — the merge commit of PR #256
  (`CONTENDER-0001` + `XASSET-0001`).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **PR #256's full lifecycle independently re-verified**, not assumed: `merged: true`,
  `merged_at: 2026-08-06T02:51:03Z`, both governance decisions merged. The PR's own principal-
  acceptance comment (`issuecomment-5199829133`, exact head `7279f1e31046c8a00c07c38b51ff42b5a406e6d1`)
  and post-merge-verification comment (`issuecomment-5199866504`) were both independently read in
  full — merge-commit tree confirmed byte-identical to the accepted head's own tree (zero drift at
  merge), decision catalog confirmed **83 decisions, `issues == ()`**, 754/754 focused and 2756/2756
  full `pytest` at merge, exactly one `priority: primary` workstream (`WS-0005`), zero diff on every
  protected path (`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `allocate.py`, `margin_state.py`, `levels.py`, `intelligence/classification/`,
  `intelligence/companies/`, `intelligence/themes/`, `intelligence/relationships/`,
  `governance/evidence/`), and merge-commit CI `completed`/`success`.
- **`CONTENDER-0001` and `XASSET-0001` independently re-read in full** at their merged text (not
  summarized from the PR description) — see §A–§K below, which bind directly to their quoted text.
- **`WS-0014`'s live register entry independently re-read in full**: `status: proposed`,
  `priority: secondary`, `dependencies: [WS-0005]`, `milestones: []` (empty — no prior execution
  unit), `authorized_scope: "None — architecture and sequencing planning only... no execution unit
  authorized"`, `next_action` naming exactly this item ("This workstream's first possible future
  step (contender normalization plus research-readiness screening, item 1...) may not begin without
  its own separate, future, explicit principal authorization") — confirming no prior decision
  already authorizes this unit's execution.
- **Decision catalog independently rebuilt** via `portfolio_hq.dashboard.decisions.build_catalog('.')`:
  **83 decisions, `issues == ()`**, matching PR #256's own post-merge figure exactly (no new decision
  merged since).
- **Next unused decision identifier independently derived.** A full-repository, case-insensitive grep
  for `CONTENDER-0002` across `governance/decisions.yaml`, every file under `governance/decisions/`,
  `operations/WORKSTREAMS.yaml`, and `CLAUDE.md` returned zero hits before this filing. Per
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new
  decision domain needs one"), this filing extends the already-established `CONTENDER-####` domain
  rather than minting a new prefix — this repository's own repeated precedent for a domain's second
  filing (`REL-0001`→`REL-0002`, `TIER-0001`→`TIER-0002`, `CHART-0001`→`CHART-0002`), not a fit for
  `TIER-####` (WS-0005-Milestone-5/6/7-specific, scoped to the 27-equity cohort), `REL-####` (the
  closed relationship-primitive taxonomy), or `PI-####` (frozen, one-way Company/Theme Intelligence).
- **Exactly one `priority: primary` workstream** confirmed at the YAML-field level: `WS-0005`.
- **Live repository composition independently counted**, not assumed: `targets.yaml`'s
  `destination:` list holds 36 rows (27 `asset_class: equity`, 4 `fund` — SPY/VEA/VWO/GLD, 3
  `crypto` — BTC/ETH/SOL, 1 `reserve`, 1 `cash`); `gates.yaml` holds 6 gated names (none currently
  holding shares); `holdings.yaml` holds 25 `shares:` entries and 3 `crypto_shares:` entries;
  `intelligence/companies/` holds 53 `.yaml`/`.md` record pairs; `intelligence/themes/` holds 2;
  `intelligence/relationships/` holds 13; `intelligence/classification/` holds exactly 27 sealed
  ticker records plus `COHORT_MANIFEST.yaml` (28 total), `classification_validator.py` reporting
  `OK (28 results)`; `issuer_lookthrough.yaml` exists as a separate point-in-time ETF-constituent
  snapshot (never a live fetch, per its own header comment); `earnings.py` carries exactly one known
  alias mapping, `_YAHOO_SYMBOL = {"BRK.B": "BRK-B"}`.
- **Local git history depth independently checked and found materially limited.** This session's
  working clone is a **shallow clone** (`git rev-parse --is-shallow-repository` → `true`), with its
  oldest reachable commit dated 2026-07-31 (the same calendar date `PHQ-2026-02`, which removed 41
  previously-tracked `holdings.yaml` tickers, was itself accepted). This is a genuine, verified
  finding, not an assumption — see §G.

## Decision

### A. Scope — item 1 only

This filing authorizes exactly `XASSET-0001` §J's dependency-order step 1: **contender normalization
plus research-readiness screening**, described there as "genuinely one evidence-gathering pass." It
authorizes nothing else in the fourteen-item `WS-0014` scope list — no additional-equity blind
cohort, no ETF/crypto framework design, no cash/reserve/GLD/debt doctrine, no overlap modeling, no
synthesis, no sleeve- or instrument-level sizing, no chart-informed deployment, no final audit.

### B. Source locations the future implementation must scan

The future implementation PR must mechanically inventory ticker-shaped references from, at minimum:

1. `targets.yaml`'s `destination:` list (canonical population, `asset_class` field);
2. `gates.yaml` (gated names, their `status`/`next_gate` disposition);
3. `holdings.yaml`'s `shares:` and `crypto_shares:` blocks (current positions);
4. `issuer_lookthrough.yaml` (ETF constituent symbols — tickers appearing only as fund constituents,
   never independently held);
5. `intelligence/companies/*.yaml` and `*.md` (53 records — both the 27 covering a current canonical
   name and the 26 `PI-0035` classified "retained/historical-advisory/non-current");
6. `intelligence/themes/*.yaml` and `*.md` (2 records);
7. `intelligence/relationships/*.yaml` and `*.md` (13 records — pairwise, likely no new symbols
   beyond items 1/5, but must be scanned for completeness, not assumed empty);
8. `intelligence/classification/*.yaml` and `COHORT_MANIFEST.yaml` — read-only reference only (§D);
9. `governance/decisions/*.md` (comparator sets named in committee-review authorizations —
   `PI-0016`-methodology filings and their comparator lists — plus explicit deferrals: `PI-0014`'s
   INTC/SYK/DHR, `PI-0027`'s deferred EQIX, `PI-0029`'s excluded UNH, `PI-0032`'s Sandisk/SNDK
   candidate, `PI-0033`'s fourteen dispositioned names);
10. `intelligence/BATCH*_COMPARISON.md` artifacts (external-opportunity/replacement-candidate leads,
    per `PI-0023`'s own authorized shape);
11. `governance/audits/*.md` (retained audit artifacts that may name additional comparator or
    candidate tickers, e.g. coverage-gap registers);
12. `decision_log.yaml` (the pre-`governance/decisions/` historical ledger, `PI-0001`–`PI-0009`,
    `MARGIN-0001`–`MARGIN-0003`);
13. `earnings.py`'s `_YAHOO_SYMBOL` map (known-alias precedent, §C);
14. `governance/evidence/CHART-0002/` package manifests (chart-covered tickers, per `CHART-0001`/
    `CHART-0002`'s governed library).

`test_*.py` files are explicitly **excluded** as a source of candidates — they exist only to confirm,
where a symbol also appears in an authoritative source above, that it is real, or, where a
symbol appears *only* in test code, to classify it `synthetic_or_test_fixture` (§E).

### C. Canonicalization precedence and alias handling

`targets.yaml`'s `destination:` ticker is the canonical symbol for any instrument with a current
destination row. Where a source above uses a different convention for the same underlying instrument
(this repository's own confirmed precedent: `BRK.B` vs. Yahoo's `BRK-B`), the future implementation
must resolve to one canonical entry and record the alias, never double-count it as two candidates.
`earnings.py`'s `_YAHOO_SYMBOL` map is the only currently-known alias and must be reused, not
reinvented; any newly discovered alias must be recorded with its source and mapped, never guessed. A
symbol that cannot be mechanically resolved to a known canonical form or a documented alias is
`requires_identity_resolution` (§E), never silently assumed.

### D. The 27 sealed equities are read-only reference, not rescanned content

`intelligence/classification/*.yaml` and `COHORT_MANIFEST.yaml` remain exactly as `TIER-0006` left
them — sealed, immutable evidence inputs. The future implementation may read them only to record the
mechanical fact that a given canonical ticker already has a completed Milestone 6 blind classification
(informing, not replacing, its research-readiness status, §F) — it must not reopen, edit, reinterpret,
or extend any sealed record, and must not treat "already classified" as itself a contender-screening
disposition (the 27 are equities with an existing canonical destination row; contender screening is
about the wider, currently-uninventoried set `CONTENDER-0001` §A defines as eligible).

### E. Closed screening-disposition vocabulary

The future implementation must assign, to every normalized ticker-shaped reference it finds, exactly
one of the following twelve closed dispositions — no thirteenth value, no free-text substitute:

1. `evaluation_ready` — genuine investable instrument, has an adequate, sufficiently current governed
   evidence base (Company Intelligence, Theme Intelligence, or equivalent asset-appropriate record),
   ready for a future, separately authorized research-readiness-consuming step (e.g., an additional
   blind-classification cohort under `XASSET-0001` §C item 1);
2. `requires_research` — genuine investable instrument, no adequate governed evidence base exists yet;
3. `requires_freshness_review` — genuine investable instrument with a governed record, but its
   evidence currency is stale or unverified against the record's own `review.next_due`/freshness
   fields (owned by `PI-0011`/`AUTO-0001`, never duplicated here — see §F);
4. `requires_identity_resolution` — symbol or asset identity is ambiguous and cannot be mechanically
   resolved (an alias mapping to more than one live security, a corporate-action successor that is
   unclear from repository text alone, or any other identity conflict);
5. `insufficient_evidence` — genuine investable instrument with some governed record, but that
   record's own text discloses evidence access failures or gaps too material to support even a
   readiness call (matching this repository's own disclosed-access-failure precedent, e.g.
   `PI-0038`'s six gated-name records);
6. `duplicate_or_alias` — resolved as the same underlying instrument as another canonical entry
   already inventoried under its own canonical symbol (§C) — carries a `duplicate_of` link, never
   inventoried as a second independent candidate;
7. `benchmark_or_index` — used only as a comparison benchmark or index proxy in repository text, not
   itself represented as a position candidate;
8. `synthetic_or_test_fixture` — a ticker-shaped string appearing only in test code, synthetic data,
   or documentation examples;
9. `stale_or_superseded` — an identity genuinely superseded by a corporate action (this repository's
   own confirmed precedent: `PI-0032`'s WDC → Sandisk/SNDK separation) — distinct from
   `requires_freshness_review` (evidence currency) because the underlying *identity*, not just its
   evidence, has changed;
10. `non_investable` — a malformed, truncated, placeholder, or otherwise not-a-real-ticker string;
11. `explicitly_deferred_or_excluded` — a genuine investable instrument the repository has already,
    separately, and specifically dispositioned as deferred or excluded (`PI-0014`, `PI-0027`'s EQIX,
    `PI-0029`'s UNH, `PI-0033`'s fourteen names) — the future implementation must cite the existing
    decision and reason verbatim, never re-derive or re-litigate it;
12. `abstain_pending_human_decision` — none of the above can be mechanically assigned without a new
    research or policy judgment the future implementation is not authorized to make (§H).

Each entry must retain: canonical symbol/identity; asset type (`equity`/`fund`/`crypto`/`benchmark`/
`fixture`/other, matching `targets.yaml`'s existing `asset_class` vocabulary where applicable, extended
only as needed for non-investable categories); every provenance location found (§B); investability
status; research status; evidence-freshness status (mechanically read, never recomputed); Milestone-6
classification status where applicable (§D); current-policy status (current holding/target/gate,
mechanically read from `targets.yaml`/`holdings.yaml`/`gates.yaml`); existing gate or prior-decision
disposition where one exists (§E.11); duplicate/supersession link where applicable (§E.6/§E.9); a
plain-text reason; a review trigger where applicable; and the exact next required governed action
(which is never itself authorized by that record's own presence in the inventory).

### F. Research-readiness screening rules — mechanical only, no new evaluation

"Research-readiness" in this unit means only: does a mechanically-observable governed evidence
record already exist and does its own freshness metadata (owned by `PI-0011`/`AUTO-0001`/each Company
Intelligence record's own `review.*` fields, per `OPS-0006` §10's explicit non-duplication rule) read
as current, per that owning system's own existing rules? The future implementation must call or
reproduce those existing checks (e.g., `intelligence_report.py`'s public staleness API, per `PI-0011`'s
own reuse requirement) rather than invent a second freshness computation. It must not itself judge
whether a record's *content* is good enough, correct, or investment-worthy — that is research and
classification judgment, out of scope here and everywhere in `WS-0014`'s still-unauthorized items 2+.

### G. Legacy-ticker provenance — conditional, bounded

`PHQ-2026-02`'s own reconciliation history discloses that 41 previously-tracked `holdings.yaml`
tickers were removed (not zeroed) when holdings were reconciled to the verified v1.35 evidence
package, without individually enumerating those 41 symbols in this repository's own committed text.
This session verified, live, that its own working clone is a **shallow git clone** — oldest reachable
commit dated 2026-07-31, the same calendar date `PHQ-2026-02` was accepted — meaning the pre-migration
`holdings.yaml` history that would name those 41 tickers is **not reachable from this clone** as
verified. The future implementation must, before attempting any recovery:

1. independently re-verify its own execution environment's git clone depth (`git rev-parse
   --is-shallow-repository` and the oldest reachable commit date) rather than trust this filing's own
   finding as still current;
2. if full history is reachable (e.g., via an unshallowed clone or the GitHub API's own commit/diff
   endpoints, which are not limited by a local shallow clone), attempt a bounded, mechanical diff of
   `holdings.yaml` across the `PHQ-2026-02` reconciliation commit to recover the 41 symbols;
3. if recovery is not reachable, or if recovered symbols raise identity ambiguity beyond what §C's
   mechanical rules resolve (a materially expanded or ambiguous scope), **stop and disclose** — per
   this filing's own instruction, legacy-ticker recovery becomes its own later, separately authorized
   sub-unit, not silently folded into or dropped from this one.

No legacy ticker may be guessed, reconstructed from memory, or asserted without a directly inspected
source.

### H. Mechanical-versus-judgment boundary

Permitted, mechanical facts: symbol occurrence and its exact file/line provenance; current
`targets.yaml`/`holdings.yaml`/`gates.yaml` membership and field values; `issuer_lookthrough.yaml`
constituent membership; the known alias map (§C); each governed record's own existing
freshness/staleness/review-status fields (read, not recomputed content-wise); Milestone 6
classification-status presence (§D); an existing governed disposition's own recorded text (§E.11).

Prohibited: any new investment-merit judgment; any new freshness determination beyond what an
existing owning system already computes; any new identity resolution beyond §C's documented-alias
rule; any research beyond reading already-committed repository text; any reopening of a closed
deferral's own reasoning. Where a symbol's disposition cannot be resolved by a mechanical rule above,
it is `abstain_pending_human_decision` (§E.12) — never forced into a more definite-sounding category.

### I. Output design — hybrid, matching repository precedent

The future implementation must produce two artifacts, not one, matching this repository's own
established split between narrative audit evidence and machine-checkable structured record (the same
split `TIER-0001`'s inventory audit and `TIER-0002`'s framework design established before Milestone
6's execution, and the split `REL-0001`'s inventory audit established before `REL-0002`'s content):

1. **One retained narrative audit artifact** under `governance/audits/` documenting the full scan
   methodology, source-by-source findings, and any stop-condition disclosures (§G, §K) — the human-
   readable record of how the inventory was built and what was found ambiguous.
2. **One small, structured, committed registry** (e.g. `intelligence/contenders/registry.yaml`, one
   row per normalized ticker, schema matching §E's required fields) plus a **new, narrowly-scoped
   validator** (e.g. `contender_registry_validator.py`) enforcing the closed disposition vocabulary,
   required fields, and internal consistency (no duplicate canonical symbol, every `duplicate_of`/
   `explicitly_deferred_or_excluded` citation resolving to a real target) — matching
   `classification_validator.py`'s and `relationship_validator.py`'s own precedent of a committed,
   validated record rather than an uncommitted, regenerated-on-demand report. A structured registry is
   preferred over a purely regenerated report (the `PI-0011` staleness-report pattern) because this
   unit's own output — unlike freshness, which is a pure function of already-owned fields — includes
   abstentions and identity-resolution calls (§E.4/§E.12) that are themselves point-in-time editorial
   findings worth a stable, citable record for `WS-0014`'s later items to build on, not a value that
   silently changes on every regeneration.

The registry must carry zero import coupling with `allocate.py`/`margin_state.py` in either direction
and must never be read by, or coupled to, any allocator or production decision path — it is inventory,
not policy.

### J. Validator, test, and CI requirements

The future implementation must, at minimum: parse-validate every new/changed YAML and Markdown file;
run the new `contender_registry_validator.py` clean against its own registry; add focused tests
covering the closed-vocabulary enforcement, duplicate/alias resolution, and abstention-path behavior;
re-run and report the full existing suite (`classification_validator.py`, `relationship_validator.py`,
`intelligence_validator.py`, `freshness_validator.py`, the decision-catalog reconciliation, and full
`pytest`) to confirm zero regression; confirm zero diff on every existing protected path listed in
§B item 8's own read-only boundary and every path `CONTENDER-0001`/`XASSET-0001` already named;
confirm exactly one `priority: primary` workstream; and pass `git diff --check` clean.

### K. Stop conditions

The future implementation must stop and disclose, rather than guess past, any of: a symbol
indistinguishable between a genuine reference and a fixture; an alias mapping to more than one live
security; investability that cannot be confirmed from repository text or a documented alias rule;
conflicting repository sources for the same symbol; a git-history recovery attempt that expands scope
or ambiguity beyond §G's bound; any point at which assigning a disposition would require a new
research or policy judgment (§H); any need to mutate a protected path (`targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`,
`intelligence/classification/`, any existing Company/Theme/Relationship Intelligence record,
`governance/evidence/`); or the appearance of another concurrent mutation lane.

### L. `operations/WORKSTREAMS.yaml` update performed by this filing

`WS-0014` receives exactly one additive milestone entry, `contender0002-normalization-and-readiness-
screening-authorization`, recording this filing's own bounded scope (§A–§K) without editing
`WS-0014`'s own `status` (`proposed`), `priority` (`secondary`), `dependencies` (`[WS-0005]`), or
`prohibited_scope` fields. `WS-0014`'s `authorized_scope` and `next_action` fields are updated,
additively, to state that this filing (once merged) authorizes exactly one future, separate,
implementation PR for item 1 only — every other item in the fourteen-item list remains exactly as
unauthorized as before. The new milestone gate is recorded `status: in_progress`, `pr: null` at this
filing's own first commit, consistent with `TIER-0004`/`TIER-0005`'s own established precedent that a
filing may not mark its own still-unmerged work `complete` — a later Lane M synchronization, once this
PR's own independent review, correction if needed, principal acceptance, merge, and post-merge
verification occur, is the appropriate place to close it. No `WS-0013` field is touched by this
filing — `WS-0014`'s own dependency relationship to `WS-0013` (recorded by PR #256) is unaffected.

### M. Explicit non-authorization

This filing authorizes definition and future-implementation authorization only. It does not
authorize, and no future action may treat it as having authorized:

- any actual scan, inventory build, registry file, or audit artifact — those are the future
  implementation PR's own deliverables, gated on this filing's own merge and that PR's own full
  independent-review/correction/principal-acceptance/merge/post-merge-verification lifecycle;
- research on any ticker, of any asset type;
- classification, ranking, scoring, or capital-priority comparison of any ticker;
- revival, re-evaluation, or re-scoring of any historical, deferred, or delisted candidate (Sandisk/
  SNDK per `PI-0032`, any recovered legacy ticker per §G, or any `PI-0033`/`PI-0027`/`PI-0014` name);
- additional blind classification of any equity beyond the sealed 27;
- ETF or cryptocurrency research, framework design, or classification;
- any target, tier, holding, gate, cap, cluster, allocator, margin, ladder, chart, order, or trade
  change;
- any allocation check, live or scenario;
- Milestone 7 implementation or any Milestone 8/9 work;
- any item 2 through 14 of `WS-0014`'s fourteen-item scope list.

## Rationale

`CONTENDER-0001` and `XASSET-0001` both explicitly assign contender normalization and research-
readiness screening to `WS-0014` as its first future step, and both explicitly withhold authorization
to begin it. `XASSET-0001` §J's own dependency-order roadmap names this exact pairing — normalization
plus readiness screening — as "genuinely one evidence-gathering pass," the correct batching unit per
`OPS-0008`'s Research Wave Protocol discipline (a genuine common mechanism, not a shared label,
justifies one unit): both tasks operate over the same source corpus (§B), both are mechanical-fact
questions (§H), and splitting them into two filings would produce no scope-discipline benefit while
doubling the review/correction/acceptance overhead `OPS-0008` was itself adopted to reduce.

Defining the disposition vocabulary, canonicalization rule, and mechanical-versus-judgment boundary
before authorizing execution follows this repository's own repeated "doctrine before content" pattern
(`TIER-0001`/`TIER-0002` before Milestone 6's execution; `REL-0001` before Milestone 4's content
batches). A twelve-value closed vocabulary, rather than free text, matches this repository's own
established schema discipline (`TIER-0002`'s four-axis framework, `REL-0001`'s twelve-item
relationship taxonomy, `PI-0004`'s closed conviction vocabulary) — an open-ended disposition field
would recreate exactly the ambiguity this filing exists to close.

The hybrid audit-artifact-plus-structured-registry output design (§I) follows this repository's own
demonstrated pattern of pairing a narrative retained audit (for methodology and disclosed ambiguity)
with a machine-checkable committed record (for anything later work needs to cite or validate against)
— never one alone where the content includes both narrative judgment calls and structured facts.

The legacy-ticker provenance finding (§G) is not speculative: this session directly ran
`git rev-parse --is-shallow-repository` and inspected the oldest reachable commit, confirming a real,
disclosed limitation on what this specific working environment can mechanically recover — exactly the
kind of "verify before acting" discipline CLAUDE.md's own Guardrails section requires, applied here to
an environment fact rather than an external claim.

## Alternatives Considered

**Authorize the full fourteen-item `WS-0014` scope in one filing.** Rejected — `XASSET-0001` §J
already requires separate lifecycle units for framework design versus execution, ETF versus crypto
work, every completion determination, and sleeve- versus instrument-level targets; batching item 1
with any later item would violate that already-accepted discipline and this repository's own
bounded-unit-per-authorization pattern throughout `WS-0005`/`WS-0012`.

**Skip the structured registry and rely on a regenerated report only, matching the `PI-0011`
freshness-report precedent.** Rejected per §I's own reasoning — this unit's output includes point-in-
time editorial abstentions (§E.4/§E.12), unlike pure freshness facts, which are a stable function of
already-owned fields and regenerate identically every time.

**Leave the disposition vocabulary open-ended, to be defined by the future implementation session
itself.** Rejected as exactly the kind of under-specified authorization this repository's own
`TIER-0001`→`TIER-0002` sequencing was built to avoid — a closed vocabulary, defined here and bound by
reference in the future implementation, prevents that session from inventing ad hoc categories under
time pressure.

**Attempt legacy-ticker git-history recovery in this same filing.** Rejected — this filing authorizes
architecture only and performs no implementation; §G instead specifies the exact verification a future
implementation session must perform and the exact condition under which recovery becomes its own
separate sub-unit, rather than guessing at scope now.

## Consequences

Once this filing merges, a future, separate `WS-0014` implementation PR may begin exactly the scope
§A–§K bound — gated on its own full independent-review/correction/principal-acceptance/merge/post-
merge-verification lifecycle, matching every other bounded unit in this repository's history. Until
then, nothing in current repository state changes: no registry exists, no ticker is newly researched,
no symbol's disposition is assigned, and `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, every existing Company/Theme/Relationship Intelligence record, and the 27
sealed classification records remain byte-identical to their pre-filing state. `WS-0014`'s remaining
thirteen scope items stay exactly as unauthorized as `XASSET-0001` left them.
