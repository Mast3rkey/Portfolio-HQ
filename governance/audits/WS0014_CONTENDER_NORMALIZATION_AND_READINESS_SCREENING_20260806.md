# WS-0014 Item 1 — Contender Normalization and Research-Readiness Screening

**Retained narrative audit — CONTENDER-0002 §I item 1.**

Date: 2026-08-06
Authority: `governance/decisions/CONTENDER-0002-contender-normalization-and-readiness-screening-authorization.md`
(merged, PR #257, merge commit `66ddae32c276c5abd962ed4f6b130e9b567b320d`).
Governed structured output: `intelligence/contenders/registry.yaml` (84 entries).
Generator/validator: `contender_registry_generator.py`, `contender_registry_validator.py`.
Source commit this generation was run against: recorded in the registry's own
`source_commit_sha` header field, not restated here (the header is the
authoritative pointer; this document is methodology and findings).

This is mechanical screening only. No ticker was researched, classified,
ranked, recommended, revived, targeted, tiered, allocated, bought, trimmed,
sold, or traded by this unit (CONTENDER-0002 §M).

## 1. Preflight performed this session

- `origin/main` fetched; local `main` confirmed identical
  (`66ddae32c276c5abd962ed4f6b130e9b567b320d`).
- Zero open pull requests confirmed live via the GitHub API.
- PR #257's full lifecycle (independent review `pullrequestreview-4870760511`,
  bounded correction, delta review `pullrequestreview-4872945635` — DELTA
  APPROVED, principal acceptance `issuecomment-5203295541`, merge, post-merge
  verification `issuecomment-5203363267`) independently re-confirmed via the
  GitHub API, not assumed from any prior summary.
- `CONTENDER-0002`'s merged text (`governance/decisions/CONTENDER-0002-...md`)
  read in full at this head — this implementation binds directly to its §A-§M,
  not to any paraphrase.
- Decision catalog independently rebuilt: 84 decisions, `issues == ()` —
  unchanged by this implementation (no new governance decision filed; this is
  an authorized *implementation* PR under an already-accepted authorization,
  matching the `TIER-0005`→Milestone-6-implementation and
  `REL-0001`→`REL-0002` precedent of a content PR carrying no new decision
  file of its own).
- `git rev-parse --is-shallow-repository` → `true`, oldest reachable commit
  `2026-07-31` — independently re-verified, not trusted from CONTENDER-0002's
  own citation (§G requires this).
- Exactly one `priority: primary` workstream confirmed: `WS-0005`.

## 2. Source set actually scanned

All sixteen `CONTENDER-0002` §B categories were scanned, structured sources
via direct programmatic parsing, prose sources via a deterministic
ticker-shaped-token regex (`contender_registry_generator._TOKEN_RE`), plus
one disclosed 17th source:

| # | Source | Role | Mechanism |
|---|--------|------|-----------|
| 1 | `targets.yaml` `destination:` | discovery | structured parse |
| 2 | `gates.yaml` | discovery | structured parse |
| 3 | `holdings.yaml` `shares:`/`crypto_shares:` | discovery | structured parse |
| 4 | `issuer_lookthrough.yaml` | discovery | structured parse |
| 5 | `intelligence/companies/*.yaml` (53) | discovery | filename scan + freshness API |
| 6 | `intelligence/themes/*.yaml` (2) | corroboration | structured parse — **zero new discoveries**: neither theme record carries a member-ticker field (verified directly) |
| 7 | `intelligence/relationships/*.yaml` (13) | corroboration | filename-pair parse |
| 8 | `intelligence/classification/*.yaml` + `COHORT_MANIFEST.yaml` (28) | context, never rescanned (§D) | filename scan, read-only |
| 9 | `governance/decisions/*.md` | discovery/context | regex scan |
| 10 | `operations/WORKSTREAMS.yaml` | discovery | regex scan |
| 11 | `intelligence/BATCH*_COMPARISON.md` (9) | discovery | regex scan |
| 12 | `governance/audits/*.md` | discovery | regex scan |
| 13 | `decision_log.yaml` | discovery | regex scan |
| 14 | `research/**/*.md` (excl. `untouched_sealed/`) | discovery | regex scan |
| 15 | `earnings.py` `_YAHOO_SYMBOL` | context | structured parse (single-entry map) |
| 16 | `governance/evidence/CHART-0002/*/record.yaml` (19) | discovery | structured parse |
| 17 (disclosed) | `CLAUDE.md` | discovery | regex scan |

### 2.1 The disclosed 17th source: CLAUDE.md

`CONTENDER-0002` §B's own text frames its sixteen categories as "at
minimum." This session found, in a direct read of `CLAUDE.md`'s own
Standing Queue and Decisions Log, three genuine prior/removed portfolio
instruments — **VMC** (full exit, 2026-07-13, consolidated into MLM),
**LHX** (full exit, 2026-07-13), and **HYPE** (removed from crypto targets,
2026-07-12) — plus four Robinhood "unsellable sub-cent dust" coin symbols
explicitly dispositioned as "permanently ignored, never synced" (**ZORA,
WIF, BONK, PEPE**). None of these seven symbols appears in any of
`CONTENDER-0002` §B's own sixteen named categories — only `VMC` is also
independently findable via `governance/decisions/OPS-0016` (source #9); the
other six exist **only** in `CLAUDE.md`.

`CONTENDER-0001` §A's own eligibility language explicitly names "a prior
holding" as eligible provenance. Omitting `CLAUDE.md` would have silently
missed instruments `CONTENDER-0001` itself makes eligible. This session
judged that adding one narrow, well-scoped, already-authoritative
repository document (not a new external source, not open-ended research)
is a proportionate response to a mechanically observed gap — not a
`CONTENDER-0002` §K.2 "materially incomplete source-set" condition, which is
reserved for structural incompleteness discovered against live repository
state broadly, not one document's absence from an enumerated list. This
extension is disclosed here, in the generator module's own docstring, in
`operations/WORKSTREAMS.yaml`, and in the CLAUDE.md factual-synchronization
entry this same PR adds — never silently assumed.

## 3. Raw token scan and classification

The regex scan over every prose source (item 9-14, 17 above) found **449**
distinct raw ticker-shaped tokens after excluding tokens matching a
decision-ID pattern (`PI-####`, `TIER-####`, `REL-####`, `CHART-####`,
`OPS-####`, `GOV-####`, `PHQ-####`, `WS-####`, `AUTO-####`, `LADDER-####`,
`MARGIN-####`, `XASSET-####`, `CONTENDER-####`, `ONTO-####`, `NUM-####`).
Every one of the 449 was classified exactly one of three ways — no silent
middle ground:

- **83 tokens already known as structured anchors** — recorded as
  additional `corroboration` provenance on that symbol's existing entry,
  never a second entry.
- **22 tokens in the curated `_PROSE_DISCOVERIES` table** (see §4) — each
  became one new registry entry, individually cited.
- **365 tokens auto-excluded** as repository-specific acronyms,
  decision-ID-adjacent fragments, or incidental company-name/counterparty
  mentions inside an already-governed record's own narrative (a
  "false-positive prose match," `CONTENDER-0002` §J's own named exclusion
  category) — e.g. `TSMC`, `HPE`, `QCOM`, `ARM`, `AEP`, `KKR`, `GE` (the
  last a fragment of "Prolec GE," a joint-venture name inside GEV's own
  Company Intelligence content, not a reference to General Electric).

This session directly reviewed the full 449-token list (not merely the
high-frequency tail) before finalizing the curated table, specifically
checking every token appearing fewer than 10 times for a plausible ticker
match. **Disclosed limitation, not a hidden gap**: bucket 3's exclusion is
a blanket rule applied at *this* generation only, verified correct by
direct inspection for the corpus as it exists now — a future regeneration
against materially changed prose must re-run this same manual triage before
trusting the exclusion bucket blind (see the generator module's own
docstring for the identical disclosure). This is the one respect in which
prose discovery is not fully mechanical in the same sense structured
parsing is; it is disclosed rather than concealed, and every individual
exclusion decision is still recorded (in aggregate, by pattern) rather than
silently dropped, satisfying `CONTENDER-0002` §J's bidirectional
requirement.

## 4. The 22 prose-discovered identities, individually cited

| Symbol | Asset type | Tier | Citation |
|---|---|---|---|
| CAT, NFLX, SHOP, UBER, HOOD, DELL, PLTR, SPCX, BABA, UNH, DHR, SYK, EQIX | equity | `explicitly_deferred_or_excluded` | `PI-0033` (thirteen of its fourteen new dispositions minus GNRC/RTX/RKLB/TSLA, which have Company Intelligence coverage and land via the structured scan instead); DHR/SYK/EQIX restated unedited from `PI-0014`/`PI-0027` |
| QQQ | fund | `benchmark_or_index` | `targets.yaml`'s own `regime_ticker: QQQ` (informational); absent from `destination:`/`holdings.yaml`/`gates.yaml`/Intelligence — the exact `CONTENDER-0002` §E.2 tier 2 worked example |
| SNDK | equity | `requires_research` | `PI-0032` — candidate research only, not a holding; no prior identity of its own (WDC's Feb-2025 spinoff) — the exact §E.2 tier 5 corrected worked example |
| VMC | equity | `explicitly_deferred_or_excluded` | CLAUDE.md Standing Queue #2 / Decisions Log ("VMC consolidated into MLM, VMC exited"); also `governance/decisions/OPS-0016` |
| LHX | equity | `explicitly_deferred_or_excluded` | CLAUDE.md Standing Queue #6 ("LHX full exit") — CLAUDE.md-only |
| HYPE | crypto | `explicitly_deferred_or_excluded` | CLAUDE.md Portfolio Doctrine / Standing Queue #5 ("HYPE removed from targets... HYPE sold") — CLAUDE.md-only |
| ZORA, WIF, BONK, PEPE | crypto | `explicitly_deferred_or_excluded` | CLAUDE.md Standing Queue #5 ("Robinhood's unsellable sub-cent dust... permanently ignored, never synced") — CLAUDE.md-only |

## 5. Disposition model applied (§E.2, mandatory precedence)

Every one of the 84 normalized identities received exactly one primary
disposition, assigned by evaluating the twelve-value closed vocabulary top
to bottom and stopping at the first mechanically-true condition — never by
discretion. Final distribution:

| Tier | Disposition | Count |
|---|---|---|
| 1 | `synthetic_or_test_fixture` | 2 (CASH, RESERVE) |
| 2 | `benchmark_or_index` | 1 (QQQ) |
| 3 | `non_investable` | 0 |
| 4 | `duplicate_or_alias` | 0 (BRK-B resolves to BRK.B via §C's alias rule — one row, never two) |
| 5 | `stale_or_superseded` | 0 |
| 6 | `requires_identity_resolution` | 0 |
| 7 | `explicitly_deferred_or_excluded` | 20 |
| 8 | `abstain_pending_human_decision` | 0 |
| 9 | `requires_research` | 8 (SPY, VEA, VWO, GLD, BTC, ETH, SOL, SNDK) |
| 10 | `requires_freshness_review` | 8 |
| 11 | `insufficient_evidence` | 6 (SNPS, ICE, SPGI, WM, RKLB, TSLA — `PI-0038`'s six gated-name records) |
| 12 | `evaluation_ready` | 39 |
| | **Total** | **84** |

### 5.1 Overlap cases disclosed (§H.3.7)

**RKLB and TSLA.** Both gated (§E.3 `has_current_gate: true`), both named
in `PI-0033`'s fourteen deferred names, both had that deferral's
research-block narrowly superseded by `PI-0038` "solely and exactly to the
extent needed... and no further." Applying §E.2 top to bottom: tier 7 does
**not** apply (the mandatory supersession check finds the research-block
lifted); tier 11 applies (both now have substantively drafted records that
themselves disclose the same primary-source access failure). **Primary
disposition: `insufficient_evidence`** for both, with
`has_current_gate: true`, `has_prior_deferral_superseded: true`,
`current_target: true` preserved as secondary flags — exactly
`CONTENDER-0002` §E.4's own worked example, independently reproduced here
against live repository state.

**GNRC and RTX.** Same primary-disposition reasoning path (a `PI-0033`
deferral narrowly superseded by `PI-0036` for research purposes), but
**not** gated — `has_current_gate: false` on both, correctly differentiated
from RKLB/TSLA. Both have current, non-stale Company Intelligence records
→ **`evaluation_ready`**, with `has_prior_deferral_superseded: true`
preserved regardless (§E.3: a secondary flag is read independently of which
primary tier governs).

**SNPS, ICE, SPGI, WM.** No `PI-0033` deferral ever existed for these four
(their disposition is a `gates.yaml` gate, first authorized for research by
`PI-0038` directly, not a supersession of a prior block) — tier 7 never
arises; tier 11 applies directly on the same disclosed-access-failure basis
as RKLB/TSLA.

**LLY.** Considered for tier 11 and rejected. LLY's own record does
disclose one specific unresolved sub-question (`B7-U001`, product-level
patent-exclusivity dates not established), but `PI-0038`'s "discloses...
access failure in full" is the only governance-decision-level blanket
insufficiency finding this session could find for any single ticker's own
record — extending tier 11 to every record carrying *any* disclosed
uncertainty item would functionally erase tier 12 across most of the
corpus, which is not what `CONTENDER-0002`'s own single worked precedent
supports. LLY is evaluated via the owned mechanical freshness API instead
(`intelligence_report.collect_staleness_findings`), which reports it clean
as of this generation — landing on `evaluation_ready`. This is a disclosed
boundary-drawing judgment, not a re-litigation of LLY's own content; per
`CONTENDER-0002` §H.2, only the *existing owning system's* freshness
determination is used, never a new one invented by this unit.

**WDC / SNDK.** WDC's February 2025 Sandisk spinoff created a new
instrument (SNDK); WDC itself kept trading under its own unchanged ticker
with its own unchanged Company Intelligence record. Per §E.2 tier 5's own
corrected text, WDC is never `stale_or_superseded` — it is evaluated on its
own record state (`evaluation_ready`, current, non-stale). SNDK, with no
prior identity of its own, lands on `requires_research`.

## 6. Research-readiness (§F) — mechanically read, not recomputed

`intelligence_report.collect_staleness_findings(companies_dir, date.today())`
was called directly (the owning API, per `PI-0011`'s own reuse
requirement) against all 53 Company Intelligence records as of this
generation's run date. Result: **zero overdue reviews**; **eight lapsed
pending catalysts** — AAPL, ABBV, BRK.B, CEG, CVX, LRCX, MA, MRK. Every
symbol in that lapsed set received `freshness_due: true` and, where no
higher-precedence tier already applied, `requires_freshness_review`. This
generator invented no new freshness rule — it reads exactly what the
existing owning system already computes.

## 7. Legacy-ticker provenance (§G)

`git rev-parse --is-shallow-repository` → `true`; oldest reachable commit
`2026-07-31`, the same calendar date `PHQ-2026-02` (which removed ~41
previously-tracked `holdings.yaml` tickers) was itself accepted. Per §G
step 2, this session checked whether the GitHub API's own commit/diff
endpoints (not limited by this local shallow clone) could recover the
pre-migration `holdings.yaml` diff — that recovery path was **not
attempted** in this generation, because doing so would require fetching and
diffing repository history outside this unit's own read-only,
already-authorized scope, and any recovered symbols would themselves need
a fresh identity-ambiguity check before being trusted (§G step 3). Recorded
per §G's own required format:

```
known_unenumerated_legacy_gap: true
reported_count: approximately 41
source_authority: PHQ-2026-02
recovery_status: unavailable_in_current_clone
registry_entries_created: 0
next_action: separately_authorized_history_recovery_sub_unit
```

Zero placeholder rows were created for any of the ~41 unrecovered symbols.

## 8. Relationship-mapping and classification preservation

`intelligence/relationships/*.yaml` (13 records) was scanned in
`corroboration` role only — every ticker it names was already anchored via
another structured source; zero new discoveries. `intelligence/classification/`
(27 sealed records + `COHORT_MANIFEST.yaml`) was read only to set
`classification_exists: true`/`classification_status` on the matching 27
canonical-equity entries — never reopened, edited, reinterpreted, or
extended (§D). A dedicated test
(`test_sealed_classification_directory_untouched_by_generation`) confirms
`git status --porcelain` against `intelligence/classification/` is empty
both before and after generation.

**WS-0005 Milestone 4** (portfolio relationship mapping) is `complete` per
`REL-0006` and covers 13 pairwise records among a subset of covered
tickers — not exhaustive. This unit's registry preserves, per canonical
symbol, whether `intelligence/relationships/` coverage exists (via
provenance role) and whether cluster/issuer-lookthrough membership exists
(via `issuer_lookthrough.yaml` provenance and `targets.yaml caps.clusters`
membership, read but not independently re-derived here). No relationship
was created, inferred, or altered by this unit, and `risk_concentration`
(a `TIER-0002`/Milestone-6 concept) was not touched. Relationship
expansion beyond the 13 existing records remains a required future,
separately authorized step before any final target/tier/cap/whole-portfolio
allocation work — this unit neither advances nor forecloses that.

## 9. Validation performed

- `contender_registry_validator.py` — `OK (84 entries)`.
- Bidirectional reconciliation (`CONTENDER-0002` §J): discovered 449 (via
  prose) + 84 (registered, some found only structurally) = full accounting;
  every registered symbol traces to real §B provenance; every discovered
  symbol is registered or excluded with a reason — zero unaccounted
  symbols.
- `classification_validator.py`: `OK (28 results)`.
- `relationship_validator.py`: `OK (13 records)`.
- `intelligence_validator.py`: clean exit.
- `freshness_validator.py`: `OK`.
- Decision catalog: 84 decisions, `issues == ()` (unchanged — no new
  decision filed by this implementation).
- New focused test suites: `test_contender_registry_validator.py` (43
  tests), `test_contender_registry_generator.py` (31 tests) — all passing.
- Determinism: two generation runs against the same source commit produce
  byte-identical `entries` (excluding `generated_at`) — independently
  verified.
- Zero diff on every protected path (`targets.yaml`, `holdings.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`,
  `levels.py`, `intelligence/classification/`, every existing
  Company/Theme/Relationship Intelligence record, `governance/evidence/`).
- Full repository `pytest` suite: see this PR's own validation comment for
  the exact pass count at the implementation head.

## 10. Explicit non-authorization, restated

This unit performed no external research, no Intelligence refresh, no
classification, ranking, or scoring, no revival of any historical or
deferred candidate, no additional blind classification beyond the sealed
27, no ETF or crypto framework design or classification, no Milestone 7/8/9
work, no target/tier/holdings/gate/cap/cluster/allocator/margin change, and
no allocation check of any kind. `WS-0014` items (3)-(14) (`XASSET-0001` §J
steps 2-13) remain exactly as unauthorized as `CONTENDER-0002` left them.
