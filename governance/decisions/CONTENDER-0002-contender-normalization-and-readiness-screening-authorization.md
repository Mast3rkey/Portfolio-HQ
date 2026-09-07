---
decision_id: CONTENDER-0002
date: 2026-08-06
status: Proposed
category: contender_universe_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0011, PI-0016, PI-0023, PI-0024, PI-0027, PI-0029, PI-0032, PI-0033, PI-0035, PI-0036, PI-0038, TIER-0002, TIER-0004, TIER-0007, REL-0001, CHART-0001, CHART-0002, MARGIN-0005, PHQ-2026-02, CONTENDER-0001, XASSET-0001]
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

### A. Scope — one combined execution unit; numbering authority stated explicitly

This filing authorizes exactly one future, separate implementation PR, covering exactly
`XASSET-0001` §J's dependency-order step 1: **contender normalization plus research-readiness
screening**, described there as "genuinely one evidence-gathering pass." It authorizes nothing else
in `WS-0014`'s scope.

**Two different, already-live numbering schemes both describe this same scope, and this filing states
which governs "item N" references going forward.** `XASSET-0001` §J's own roadmap numbers steps
`0`–`13` (14 entries), where step `0` is the architecture filing itself and step `1` is the
**combined** pair this filing authorizes. `WS-0014`'s own live `objective` field (unedited by this
filing) instead enumerates 14 conceptually distinct components with normalization as `(1)` and
research-readiness screening as `(2)` — two separate list entries for the same combined step. Read
literally against the register's own count, "item 1" alone would name normalization only, leaving it
ambiguous whether screening is covered.

**`XASSET-0001` §J's step numbering (`0`–`13`) is authoritative for what a `WS-0014` authorization
filing has covered.** `WS-0014`'s own `objective` field's `(1)`–`(14)` list is a **descriptive
component enumeration**, not a second independent authorization-tracking sequence — its `(1)` and
`(2)` are the same combined `XASSET-0001` §J step `1` this filing authorizes, not two separately
authorizable units. Concretely: **this filing's "item 1" covers both `WS-0014` objective items `(1)`
and `(2)`; no second authorization is required between normalization and screening; both occur in the
same future implementation PR.**

**No general index formula is asserted beyond this one step, and none should be assumed.** The two
lists' internal structure diverges past step 2: `XASSET-0001` §J step `2` ("additional-equity blind
cohorts") does correspond to `WS-0014` objective item `(3)` — both name the same next unit — but
`XASSET-0001` §J step `3` ("ETF and crypto framework design," one combined step) does **not** map
cleanly to any single `WS-0014` objective item; the register's own list instead splits that
combined step across items `(4)` ETF framework design and `(6)` crypto framework design, with item
`(5)` (ETF blind classification) interleaved between them, while `XASSET-0001` §J keeps framework
design as one step (`3`) followed by ETF classification (`4`) and crypto classification (`5`)
separately. **A future authorization filing for any step beyond this one must state its own explicit
correspondence between the two numbering schemes rather than assume a fixed offset** — the mismatch
documented here is a disclosed fact about the two already-merged lists, not something this filing
attempts to reconcile or renumber (`CONTENDER-0001`/`XASSET-0001` are not edited by this correction).
Every `WS-0014` objective item `(3)` through `(14)`, and every `XASSET-0001` §J step `2` through
`13`, remains exactly as unauthorized as before this filing.

### B. Source locations the future implementation must scan

The future implementation PR must mechanically inventory ticker-shaped references from, at minimum,
the following sixteen categories. Each is tagged with its **role** — `discovery` (a source that may
introduce a symbol not found anywhere else), `corroboration` (a source that confirms or adds
provenance to a symbol discovery expects to find elsewhere too, but must still be scanned rather than
assumed empty), or `context` (a source read for disposition-relevant facts about a symbol, not itself
treated as an independent discovery site) — matching `CONTENDER-0001` §A's own list of what counts as
eligible-for-screening provenance, which this list operationalizes:

1. `targets.yaml`'s `destination:` list (canonical population, `asset_class` field) — `discovery`;
2. `gates.yaml` (gated names, their `status`/`next_gate` disposition) — `discovery`;
3. `holdings.yaml`'s `shares:` and `crypto_shares:` blocks (current positions) — `discovery`;
4. `issuer_lookthrough.yaml` (ETF constituent symbols — tickers appearing only as fund constituents,
   never independently held) — `discovery`;
5. `intelligence/companies/*.yaml` and `*.md` (53 records — both the 27 covering a current canonical
   name and the 26 `PI-0035` classified "retained/historical-advisory/non-current") — `discovery`;
6. `intelligence/themes/*.yaml` and `*.md` (2 records) — `corroboration`;
7. `intelligence/relationships/*.yaml` and `*.md` (13 records — pairwise, likely no new symbols
   beyond items 1/5, but must be scanned for completeness, not assumed empty) — `corroboration`;
8. `intelligence/classification/*.yaml` and `COHORT_MANIFEST.yaml` — read-only reference only (§D) —
   `context`, never rescanned as a new-discovery source;
9. `governance/decisions/*.md` (comparator sets named in committee-review authorizations —
   `PI-0016`-methodology filings and their comparator lists — plus explicit deferrals: `PI-0014`'s
   INTC/SYK/DHR, `PI-0027`'s deferred EQIX, `PI-0029`'s excluded UNH, `PI-0032`'s Sandisk/SNDK
   candidate, `PI-0033`'s fourteen dispositioned names, and any later decision that narrowly
   supersedes a deferral for specific names — e.g. `PI-0036` for GNRC/RTX, `PI-0038` for RKLB/TSLA,
   see §E) — `discovery` for comparator names, `context` for disposition history;
10. `operations/WORKSTREAMS.yaml` (workstream register entries — `CONTENDER-0001` §A itself names "a
    workstream register entry" as eligible provenance; this file's own `evidence_refs`/`objective`/
    `next_action` prose may name a candidate ticker not otherwise enumerated) — `discovery`;
11. `intelligence/BATCH*_COMPARISON.md` artifacts (external-opportunity/replacement-candidate leads,
    per `PI-0023`'s own authorized shape) — `discovery`;
12. `governance/audits/*.md` (retained audit artifacts that may name additional comparator or
    candidate tickers, e.g. coverage-gap registers) — `discovery`;
13. `decision_log.yaml` (the pre-`governance/decisions/` historical ledger, `PI-0001`–`PI-0009`,
    `MARGIN-0001`–`MARGIN-0003`) — `discovery`;
14. `research/**/*.md` governed research protocols (e.g. `research/margin_target_study/PROTOCOL_V2.md`,
    `research/buy_ladder_backtest/PROTOCOL_V1.md` — `CONTENDER-0001` §A itself names "a research
    protocol" as eligible provenance; these name their own study universes, which may reference a
    ticker not otherwise enumerated; `research/margin_target_study/data/untouched_sealed/` is
    excluded from any scan, matching `MARGIN-0005`'s own sealed-data isolation requirement) —
    `discovery`;
15. `earnings.py`'s `_YAHOO_SYMBOL` map (known-alias precedent, §C) — `context`, resolves identity,
    does not itself introduce a new candidate;
16. `governance/evidence/CHART-0002/` package manifests (chart-covered tickers, per `CHART-0001`/
    `CHART-0002`'s governed library) — `discovery`.

`test_*.py` files are explicitly **excluded** as a source of candidates — they exist only to confirm,
where a symbol also appears in an authoritative source above, that it is real, or, where a
symbol appears *only* in test code, to classify it `synthetic_or_test_fixture` (§E).

**Deduplication is per canonical identity, not per source.** A symbol discovered in more than one
`discovery`-role source (e.g. a current holding also named in a batch-comparison artifact) is one
inventory entry, not one per source — every source that mentioned it is recorded as a provenance
location on that single entry (§E), never as separate rows counted toward source-occurrence totals.

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

### E. Disposition model — exactly one primary disposition, deterministic precedence, orthogonal secondary flags

A single canonical identity can genuinely satisfy more than one of the twelve dispositions'
descriptions at once (§E.4 below works a real, already-live example). Assigning "exactly one of
twelve, no rule for overlap" — this filing's own original text — leaves that overlap to be invented
ad hoc by a future implementation under time pressure. This repository's own immediately-preceding
precedent, `TIER-0007`, hit the identical defect in its own closed-disposition design and resolved it
by splitting a flat vocabulary into one required **primary disposition** plus a small set of optional
**secondary condition flags** — this filing adopts the same structure.

**E.1 — Model.** Every normalized ticker-shaped identity receives:

- **exactly one primary disposition**, chosen from the twelve-value closed vocabulary below by
  mechanically applying the precedence order in §E.2 — never chosen by discretion, never left
  unset, never assigned more than one;
- **zero or more secondary factual-state flags** (§E.3) — orthogonal metadata that must not be lost
  just because the primary disposition took precedence over the fact that flag represents.

**E.2 — Closed twelve-value vocabulary, in mandatory precedence order.** Evaluate top to bottom;
assign the primary disposition at the first value whose condition is mechanically true; each
definition below is the corrected, disambiguated text (superseding the original, ambiguous
definitions in this filing's first commit — no other filing is edited):

1. `synthetic_or_test_fixture` — a ticker-shaped string appearing only in test code, synthetic data,
   or documentation examples, **or** a structural, non-ticker destination row that names an
   accounting construct rather than a tradeable instrument (`targets.yaml`'s `CASH`/`RESERVE` rows,
   `asset_class: cash`/`reserve` — per `CONTENDER-0001` §C.7's "synthetic or placeholder row"
   category). Checked first because a fixture or structural row can otherwise superficially match
   several later conditions (e.g. "appears in `targets.yaml`" looks like evidence of investability).
2. `benchmark_or_index` — used only as a comparison benchmark or index proxy in repository text or
   configuration, never represented anywhere as a `destination:` row, holding, or position candidate
   (e.g. `QQQ` — present in `targets.yaml`'s own `regime_ticker: QQQ` config field, "informational"
   per that field's own comment, and in the regime-gate/trend-gate backtest entries of CLAUDE.md's
   Decisions Log, but absent from `targets.yaml`'s `destination:` list, `holdings.yaml`, `gates.yaml`,
   and every Company Intelligence record). If the same symbol is *also* a genuine current
   `destination:` target/holding (this repository's SPY is the concrete counter-example — a real fund
   with its own `destination:` row, not merely a benchmark proxy), it does not qualify here; it
   proceeds to the dispositions below on its own merits.
3. `non_investable` — a malformed, truncated, placeholder, or otherwise not-a-real-ticker string.
4. `duplicate_or_alias` — resolved, per §C's alias rule, as the same underlying instrument as another
   canonical entry already inventoried under its own canonical symbol — carries a `duplicate_of`
   link, never inventoried as a second independent candidate.
5. `stale_or_superseded` — reserved **strictly** for a case where the *old* symbol itself no longer
   refers to any live, tradeable security — a true identity supersession (an acquisition, a delisting,
   a ticker change that leaves the prior symbol dead), never merely "this company's most recent
   corporate action produced a new, related instrument." **Corrected worked example** (the original
   filing's WDC → Sandisk/SNDK citation was wrong and is withdrawn): WDC's own February 2025 Sandisk
   spinoff created a *new* instrument (SNDK) — WDC itself kept trading under its own unchanged
   ticker, with its own unchanged Company Intelligence record (`PI-0035`'s "retained/historical-
   advisory/non-current" classification refers to *portfolio-roster* status, not identity death). A
   spinoff is therefore **not** `stale_or_superseded` for the pre-existing name — WDC's own
   disposition depends on its own governed-record state (§E's lower tiers), while the *new* entity
   (SNDK) with no prior identity of its own is `requires_research` (tier 9), never `stale_or_
   superseded`. A future implementation must not apply this tier to any symbol whose old form still
   resolves to a live security merely because a related new symbol now also exists.
6. `requires_identity_resolution` — the canonical security identity cannot be resolved mechanically
   (an alias mapping to more than one live security, ambiguity between a true `stale_or_superseded`
   case and a spinoff per tier 5's own distinction, or any other identity conflict a documented alias
   rule (§C) does not settle).
7. `explicitly_deferred_or_excluded` — a genuine investable instrument the repository has already,
   separately, and specifically dispositioned as deferred or excluded, **and that deferral is
   currently live and unsuperseded as of the scan** (`PI-0014`, `PI-0027`'s EQIX, `PI-0029`'s UNH,
   the surviving members of `PI-0033`'s fourteen names) — the future implementation must cite the
   existing decision and reason verbatim, never re-derive or re-litigate it. **Mandatory
   supersession check before applying this tier**: a name's deferral must be checked against any
   later decision that narrowly supersedes it for that specific name before being cited at face
   value — this repository has done this twice already (`PI-0036` narrowly superseded `PI-0033`'s
   deferral for GNRC/RTX "solely and exactly to the extent needed to authorize Company Intelligence
   research... and no further"; `PI-0038` did the identical thing for RKLB/TSLA). A name whose
   research-block has been narrowly superseded is **not** currently deferred from evaluation for
   purposes of this registry, even though its underlying gate/tier/target consequences (unchanged by
   either supersession) may still apply — see §E.4's worked example. This is a mechanical check: the
   superseding decision's own text states its exact scope, nothing is inferred.
8. `abstain_pending_human_decision` — mechanical facts are available, but assigning any of the
   dispositions above, or distinguishing between tiers 9–12 below, would require a new research or
   policy judgment the future implementation is not authorized to make (§H) — e.g. a genuinely
   ambiguous read of whether an existing record's own text discloses "insufficient" evidence (tier
   11) versus merely "not yet fresh" evidence (tier 10).
9. `requires_research` — genuine investable instrument, **no** governed evidence record of any kind
   exists yet (no Company/Theme Intelligence record, no asset-appropriate equivalent).
10. `requires_freshness_review` — genuine investable instrument **with** a governed record, and that
    record's own mechanical freshness fields (owned by `PI-0011`/`AUTO-0001`, read not recomputed —
    §F) report the evidence as stale or due, **and** the record's own text does not separately
    disclose an evidence-sufficiency problem (that is tier 11, checked first).
11. `insufficient_evidence` — genuine investable instrument with a governed record that exists and
    was substantively drafted, but that record's own text explicitly discloses evidence access
    failures or gaps too material to support the next evaluation step (matching this repository's
    own disclosed-access-failure precedent — `PI-0038`'s six gated-name records, all of which
    explicitly "disclose their own research session's source-access failure in full"). Distinct from
    tier 10: this is about the record's own *content* disclosing a gap, not merely its `next_due`
    date having passed.
12. `evaluation_ready` — genuine investable instrument, has an adequate, sufficiently current governed
    evidence base, with none of tiers 1–11 applying — ready for a future, separately authorized
    research-readiness-consuming step (e.g., an additional blind-classification cohort under
    `XASSET-0001` §C item 1).

**E.3 — Secondary factual-state flags (optional, orthogonal, never a disposition substitute).** The
registry schema must support recording, independent of the primary disposition, whichever of the
following are mechanically true for an identity: `has_current_gate` (present in `gates.yaml`);
`has_historical_intelligence` (a Company/Theme Intelligence record exists but the ticker is not in
the current canonical roster, per `PI-0035`'s "retained/historical-advisory/non-current"
classification); `has_prior_deferral_superseded` (a `PI-0033`-style deferral exists but was narrowly
superseded for this name per §E.2 tier 7's check); `freshness_due` (the record's own freshness field
reads stale/due, read regardless of which primary tier it landed on); `classification_exists` (a
sealed Milestone 6 record exists, §D); `chart_evidence_exists` (covered in the governed chart
library); `current_holding` (present in `holdings.yaml`); `current_target` (present in `targets.yaml`
`destination:`, including while gated). A flag is metadata only — it never adds a second primary
disposition, never changes which precedence tier governs, and must never be omitted from the
registry merely because a higher-precedence primary disposition applied instead.

**E.4 — Worked example: RKLB and TSLA (resolves the review's own concrete overlap case).**
Mechanical facts: both are current canonical, gated equities (`gates.yaml`, `has_current_gate: true`,
`current_target: true`); both are named among `PI-0033`'s fourteen deferred names; both had that
deferral narrowly superseded by `PI-0038` "solely and exactly to the extent needed to authorize
Company Intelligence research... and no further" (leaving the deferral's gate/tier/target
consequences fully in force, per `PI-0038`'s own text — only the research-block was lifted); both now
have real, substantively drafted `intelligence/companies/{RKLB,TSLA}.yaml` records that themselves
disclose primary-source access failures. Applying §E.2 top to bottom: tier 7
(`explicitly_deferred_or_excluded`) does **not** apply — the mandatory supersession check finds the
research-block superseded, so the deferral is not currently live for evaluation purposes. Tier 11
(`insufficient_evidence`) applies — a governed record exists, was substantively drafted, and
explicitly discloses an access-failure gap. **Primary disposition: `insufficient_evidence`** for
both, with secondary flags `has_current_gate: true`, `has_prior_deferral_superseded: true`,
`current_target: true` preserved on each entry so no fact is lost. `PI-0036`'s GNRC/RTX pair applies
the identical *primary-disposition reasoning* (a `PI-0033` deferral narrowly superseded for research
purposes only, landing on `insufficient_evidence` via tier 11) — but their secondary flags differ:
GNRC and RTX are **not** gated (`PI-0035` independently confirms both as "non-gated, already-
dispositioned canonical-roster names"), so their entries carry `has_current_gate: false`,
`has_prior_deferral_superseded: true`, `current_target: true` — a future implementation must read
each identity's own facts rather than assume all four names share one flag profile. This is the
concrete case this correction exists to make unambiguous; a future implementation must not need to
re-derive this reasoning from first principles.

**E.5 — Further stress cases, briefly (illustrative only — no research performed by this filing).**
A current canonical *ungated* equity with a sealed classification and a governed record: tier 10 or
12, depending only on the record's own live freshness field. A retained/historical Company
Intelligence name (e.g. one of the 26 `PI-0035` "retained" records): eligible under `CONTENDER-0001`
§A regardless of roster absence — same tier-10/12 evaluation, `has_historical_intelligence: true`,
`current_target: false`. `QQQ` (referenced only as a regime-gate benchmark, no target/holding/record
anywhere): tier 2. `CASH`/`RESERVE` (`targets.yaml`'s structural rows): tier 1. A `BRK.B`/`BRK-B`-
style alias pair, if both raw forms are found as separate occurrences: tier 4, one entry, `duplicate_
of` recorded. A symbol named only once in decision prose as a considered-but-excluded comparator
with no other coverage (e.g. a name mentioned only in a cluster-correlation discussion): tier 9,
`requires_research` — its identity is not ambiguous, only its evidence base is absent.

**E.6 — Required per-entry fields.** Each registry entry must retain: canonical symbol/identity;
primary disposition (§E.2, exactly one); applicable secondary flags (§E.3); asset type
(`equity`/`fund`/`crypto`/`benchmark`/`fixture`/other, matching `targets.yaml`'s existing
`asset_class` vocabulary where applicable, extended only as needed for non-investable categories);
every provenance location found, with each source's role (§B); investability status; research
status; evidence-freshness status (mechanically read, never recomputed); Milestone-6 classification
status where applicable (§D); current-policy status (mechanically read from
`targets.yaml`/`holdings.yaml`/`gates.yaml`); existing gate or prior-decision disposition where one
exists, including the supersession check's own result (§E.2 tier 7); duplicate/supersession link
where applicable (tiers 4/5); a plain-text reason; a review trigger where applicable; and the exact
next required governed action (which is never itself authorized by that record's own presence in the
inventory).

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
source. If, after step 1–3 above, the 41 legacy tickers remain unrecovered, the retained audit
artifact (§I) must record an explicit gap entry rather than omit the topic silently:

```
known_unenumerated_legacy_gap: true
reported_count: approximately 41
source_authority: PHQ-2026-02
recovery_status: unavailable_in_current_clone   # or: recovered_n_of_41 / recovery_ambiguous
registry_entries_created: 0
next_action: separately_authorized_history_recovery_sub_unit
```

No placeholder or invented ticker row may be created for any unrecovered legacy symbol — the gap is
recorded once, at this granularity, never as 41 individual `abstain_pending_human_decision` rows for
symbols nobody has actually seen.

### H. Mechanical-versus-judgment boundary and conflict-resolution procedure

**H.1 — Permitted, mechanical facts.** Symbol occurrence and its exact file/line provenance; current
`targets.yaml`/`holdings.yaml`/`gates.yaml` membership and field values; `issuer_lookthrough.yaml`
constituent membership; the known alias map (§C); each governed record's own existing
freshness/staleness/review-status fields (read, not recomputed content-wise); Milestone 6
classification-status presence (§D); an existing governed disposition's own recorded text, including
whether a later decision narrowly supersedes it for a specific name (§E.2 tier 7).

**H.2 — Prohibited.** Any new investment-merit judgment; any new freshness determination beyond what
an existing owning system already computes; any new identity resolution beyond §C's documented-alias
rule; any research beyond reading already-committed repository text; any reopening or reinterpretation
of a closed deferral's, evidence-quality's, or classification's own stated conclusion. Where a
symbol's disposition cannot be resolved by a mechanical rule above, it is
`abstain_pending_human_decision` (§E.2 tier 8) — never forced into a more definite-sounding category.

**H.3 — Conflict-resolution procedure.** Real cases exist (§E.4) where more than one governed fact
about the same identity points toward a different disposition — a live deferral and an existing
Intelligence record; stale-and-also-insufficient evidence; a gate with a research-ready record; a
chart-covered ticker absent from canonical policy; a name named only in decision prose with no other
coverage; a current-policy presence alongside superseded-identity evidence. The future implementation
must, for every such case:

1. collect every mechanically-observable factual state for the identity first, before assigning
   anything (§H.1);
2. apply §E.2's precedence order mechanically to select the one primary disposition — the order
   itself is the conflict-resolution rule; no case-by-case discretion is exercised at this step;
3. preserve every orthogonal fact not captured by the winning tier as a secondary flag (§E.3) — a
   fact is never dropped merely because a higher-precedence tier governed the primary disposition;
4. never overwrite, edit, or reinterpret any existing governed decision's own text or conclusion —
   only cite it;
5. never reinterpret an existing evidence-quality conclusion (e.g. a record's own disclosed
   "insufficient evidence" finding is read as-is, never second-guessed as "actually sufficient" or
   vice versa);
6. if applying §E.2's order still leaves genuine ambiguity — the mechanical facts collected in step 1
   do not cleanly satisfy any single tier's condition — assign `abstain_pending_human_decision`
   (§E.2 tier 8) rather than force a resolution;
7. disclose every case where more than one tier's condition was mechanically true before precedence
   resolved it, in the retained audit artifact (§I) — the registry itself records only the winning
   primary disposition and its secondary flags, but the audit preserves the reasoning trail so a
   human reviewer can see what the precedence rule actually did.

The registry reports existing governed facts through the disposition/flag model; it never harmonizes
conflicting facts into a new investment conclusion of its own.

### I. Output design — hybrid, matching repository precedent

The future implementation must produce two artifacts, not one, matching this repository's own
established split between narrative audit evidence and machine-checkable structured record (the same
split `TIER-0001`'s inventory audit and `TIER-0002`'s framework design established before Milestone
6's execution, and the split `REL-0001`'s inventory audit established before `REL-0002`'s content):

1. **One retained narrative audit artifact** under `governance/audits/` documenting the full scan
   methodology, source-by-source findings, every §H.3.7 overlap disclosure, the legacy-gap record
   (§G), and any other stop-condition disclosures (§K) — the human-readable record of how the
   inventory was built and what was found ambiguous.
2. **One small, structured, committed registry** (e.g. `intelligence/contenders/registry.yaml`, one
   row per normalized identity, schema matching §E.6's required fields) plus a **new, narrowly-scoped
   validator** (e.g. `contender_registry_validator.py`) enforcing the closed primary-disposition
   vocabulary, the secondary-flag schema, required fields, and internal consistency (no duplicate
   canonical symbol, every `duplicate_of`/`explicitly_deferred_or_excluded` citation resolving to a
   real target, exactly one primary disposition per entry) — matching `classification_validator.py`'s
   and `relationship_validator.py`'s own precedent of a committed, validated record rather than an
   uncommitted, regenerated-on-demand report. A structured registry is preferred over a purely
   regenerated report (the `PI-0011` staleness-report pattern) because this unit's own output — unlike
   freshness, which is a pure function of already-owned fields — includes abstentions and identity-
   resolution calls (§E.2 tiers 6/8) that are themselves point-in-time editorial findings worth a
   stable, citable record for `WS-0014`'s later items to build on.

**The registry is a governed snapshot, not investment-policy truth.** `targets.yaml`, `holdings.yaml`,
`gates.yaml`, and every existing Intelligence/relationship/classification record remain sole
authority for their own facts — the registry only reports what those sources already say, per §H's
procedure. Regeneration must be deterministic from the same source commit — running the scan twice
against an unchanged `main` must produce byte-identical entries (excluding the run timestamp field
below); the registry's own header must record the exact source commit SHA it was generated from and a
generation timestamp, so a later session can mechanically detect staleness by comparing the recorded
source SHA against current `main` rather than re-deriving whether anything changed. No hand edit to a
generated entry is permitted outside a new, explicitly governed regeneration or correction — an entry
that needs to change requires re-running the deterministic process, not a manual patch.

The registry must carry zero import coupling with `allocate.py`/`margin_state.py` in either direction
and must never be read by, or coupled to, any allocator or production decision path — it is inventory,
not policy.

### J. Validator, test, and CI requirements

The future implementation must, at minimum: parse-validate every new/changed YAML and Markdown file;
run the new `contender_registry_validator.py` clean against its own registry; add focused tests
covering the closed primary-disposition vocabulary and its precedence order (§E.2), the secondary-flag
schema (§E.3), duplicate/alias resolution, and abstention-path behavior; **require bidirectional
reconciliation** between the §B scan's discovered references and the registry — (a) every accepted
discovered identity from the authorized source set (§B) is represented in the registry by exactly one
entry, or explicitly recorded in the retained audit as excluded/ambiguous with a stated reason (a
false-positive prose match, a resolved fixture, or an unresolved token pending §K containment); (b)
every registry entry cites at least one valid provenance location from an authorized §B source — no
registry-only invented identity. The validator must fail if a discovered reference from the scan
disappears from both the registry and the audit's own exclusion record without disposition, and must
fail if a registry entry cites no real §B provenance. The retained audit must include a reconciliation
summary (counts: discovered, registered, excluded-with-reason, legacy-gap per §G) so the two
directions can be checked by a human reviewer without re-running the scan; re-run and report the full
existing suite (`classification_validator.py`, `relationship_validator.py`, `intelligence_validator.py`,
`freshness_validator.py`, the decision-catalog reconciliation, and full `pytest`) to confirm zero
regression; confirm zero diff on every existing protected path listed in §B item 8's own read-only
boundary and every path `CONTENDER-0001`/`XASSET-0001` already named; confirm exactly one
`priority: primary` workstream; and pass `git diff --check` clean.

### K. Stop conditions — per-entry containment versus whole-unit halt

Not every stop condition has the same severity, and conflating them risks either halting an entire
scan over one ambiguous ticker or failing to halt on a genuine structural blocker. The future
implementation must distinguish the two:

**K.1 — Per-entry containment (continue processing every other identity).** Applies when the problem
is scoped to one identity: a symbol indistinguishable between a genuine reference and a fixture; an
alias mapping to more than one live security; investability that cannot be confirmed from repository
text or a documented alias rule; conflicting repository sources for the same symbol; any point at
which that one identity's disposition would require a new research or policy judgment (§H). Required
behavior: assign `requires_identity_resolution` (§E.2 tier 6) or `abstain_pending_human_decision`
(tier 8), whichever fits per §H.3; preserve every provenance location found for that identity; record
the reason in the registry entry and the audit; continue processing every other identity in the same
run; never silently omit the entry from the registry.

**K.2 — Whole-unit halt (stop the entire implementation unit).** Applies when the problem is not
scoped to one identity: the §B source-set definition proves materially incomplete against live
repository state; canonicalization logic (§C) produces a nondeterministic result across the cohort
(the same raw input yields different canonical forms on repeated runs); the registry schema cannot
represent a required fact from §E.6; §J's bidirectional reconciliation fails at the whole-scan level
(not one entry); a git-history recovery attempt (§G) unexpectedly expands scope or ambiguity beyond
§G's own bound; a protected path (`targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`,
`intelligence/classification/`, any existing Company/Theme/Relationship Intelligence record,
`governance/evidence/`) would need to be mutated; another concurrent mutation lane appears; or the
validator/test architecture itself proves defective (not just a failing individual test). Required
behavior: stop the implementation unit entirely; preserve all work completed so far in a safe,
clearly-labeled partial state; report the exact partial state (what was scanned, what was not) in the
PR/audit; **never publish a registry or audit that reads as complete when it is not**.

### L. `operations/WORKSTREAMS.yaml` update performed by this filing

`WS-0014` receives exactly one additive milestone entry, `contender0002-normalization-and-readiness-
screening-authorization`, recording this filing's own bounded scope (§A–§K), including the numbering
cross-reference from §A (this filing's authorized unit is `XASSET-0001` §J step 1, covering `WS-0014`
objective items `(1)` and `(2)` together), without editing `WS-0014`'s own `status` (`proposed`),
`priority` (`secondary`), `dependencies` (`[WS-0005]`), or `prohibited_scope` fields. `WS-0014`'s
`authorized_scope` and `next_action` fields are updated, additively, to state that this filing (once
merged) authorizes exactly one future, separate, combined implementation PR for `XASSET-0001` §J step
1 only — every remaining step/item remains exactly as unauthorized as before. The new milestone gate
is recorded `status: in_progress`, `pr: 257` (this filing's own PR, recorded once opened — this
filing's own bounded correction runs inside that same PR, so no chicken-and-egg gap arises this
round), consistent with `TIER-0004`/`TIER-0005`'s own established precedent that a filing may not mark
its own still-unmerged work `complete` — a later Lane M synchronization, once this PR's own
independent review, correction if needed, principal acceptance, merge, and post-merge verification
occur, is the appropriate place to close it. No `WS-0013` field is touched by this filing — `WS-0014`'s
own dependency relationship to `WS-0013` (recorded by PR #256) is unaffected.

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
- `XASSET-0001` §J steps 2 through 13 (equivalently, `WS-0014` objective items `(3)` through `(14)`,
  per §A's own stated correspondence).

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

**The primary-disposition/secondary-flag split (§E) is not a novel design — it directly reapplies this
repository's own immediately-preceding precedent.** `TIER-0007`'s own independent review
(`4869718735`, Finding A) found its closed-disposition vocabulary required "exactly one" value with no
precedence rule for a ticker qualifying for more than one category, and resolved it by superseding a
flat vocabulary with a primary disposition plus a closed secondary-condition flag set. This filing's
own first commit repeated the identical defect one filing later, in a different domain — this
correction closes it the same way, rather than inventing a new resolution shape, and the RKLB/TSLA
worked example (§E.4) demonstrates the fix against a real, already-live case rather than a
hypothetical one, matching `TIER-0007`'s own use of a concrete case to validate its precedence rule.

## Alternatives Considered

**Authorize the full fourteen-item `WS-0014` scope in one filing.** Rejected — `XASSET-0001` §J
already requires separate lifecycle units for framework design versus execution, ETF versus crypto
work, every completion determination, and sleeve- versus instrument-level targets; batching item 1
with any later item would violate that already-accepted discipline and this repository's own
bounded-unit-per-authorization pattern throughout `WS-0005`/`WS-0012`.

**Skip the structured registry and rely on a regenerated report only, matching the `PI-0011`
freshness-report precedent.** Rejected per §I's own reasoning — this unit's output includes point-in-
time editorial abstentions (§E.2 tiers 6/8), unlike pure freshness facts, which are a stable function of
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

**Allow an identity to carry more than one primary disposition simultaneously, instead of a strict
precedence order.** Rejected — a multi-valued primary field reintroduces exactly the "which one wins"
ambiguity §E exists to close, just moved one layer down (a future consumer of the registry would still
need its own precedence rule to pick one). A single ordered precedence list, with orthogonal facts
captured separately as secondary flags (§E.3), keeps the registry's primary field simple and
deterministic while losing no information.

**Renumber or edit `XASSET-0001` §J or `WS-0014`'s live `objective` field to eliminate the two-list
mismatch (§A) at the source.** Rejected — the task authorizing this correction explicitly bars
redesigning `CONTENDER-0001`/`XASSET-0001`, and this repository's own narrow-supersession convention
never edits a merged decision's substance after acceptance. An additive clarification in this filing
(and the mirrored `operations/WORKSTREAMS.yaml` text) that states which numbering governs and
discloses exactly where the two lists diverge resolves the live ambiguity without touching either
merged document.

## Consequences

Once this filing merges, a future, separate `WS-0014` implementation PR may begin exactly the scope
§A–§K bound — gated on its own full independent-review/correction/principal-acceptance/merge/post-
merge-verification lifecycle, matching every other bounded unit in this repository's history. Until
then, nothing in current repository state changes: no registry exists, no ticker is newly researched,
no symbol's disposition is assigned, and `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, every existing Company/Theme/Relationship Intelligence record, and the 27
sealed classification records remain byte-identical to their pre-filing state. `WS-0014`'s remaining
thirteen scope items stay exactly as unauthorized as `XASSET-0001` left them.
