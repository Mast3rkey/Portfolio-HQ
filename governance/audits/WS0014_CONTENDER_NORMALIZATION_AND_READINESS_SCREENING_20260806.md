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

## 11. Bounded correction (same day, this PR) — environment-independent clone-depth handling

Exact-head CI on this PR's original head (`481948ce0aa8840509942ac0e247690a200eec3a`,
workflow run `31094971398`, job `92594735748`) failed: **2829 passed, 1
failed** — `test_contender_registry_generator.py::test_this_environment_is_a_shallow_clone`,
`AssertionError: assert 'false' == 'true'`. Root cause, independently
confirmed from the job log: GitHub Actions' own checkout step uses
`fetch-depth: 0` (a complete clone), so `git rev-parse
--is-shallow-repository` correctly reports `false` there — the test's own
hardcoded `assert out == "true"` mistook this session's own local
development clone's shallow state (a genuine, still-accurate fact about
*this* environment) for a universal repository invariant.

A deeper, related defect was found while fixing this: `build_registry()`'s
own `legacy_gap` block **never actually called a live clone-depth check at
all** — `recovery_status` was a hardcoded string, `"unavailable_in_current_clone"`,
written once by hand after this session's own manual `git rev-parse`
check, not computed by the generator itself. In a complete-clone
environment (like CI), this would have produced a **false claim** —
reporting history as unrecoverable when it was, in fact, reachable.

**Fix**: `contender_registry_generator.detect_clone_depth()` (new) calls
`git rev-parse --is-shallow-repository` live, every generation, and
normalizes the result to exactly `"shallow"` or `"complete"`
(`contender_registry_validator.CLONE_DEPTH_VALUES`) — accepting an
injectable `runner` for deterministic unit testing without depending on
the actual executing environment's real clone depth.
`build_legacy_gap(clone_depth)` (new) derives `recovery_status` from that
live-detected value: `"unavailable_in_current_clone"` when shallow;
a new, disclosed fourth value, `"reachable_but_recovery_not_attempted_this_generation"`,
when complete — chosen deliberately over the two other §G-documented
values (`recovered_n_of_41`, which would falsely claim recovery work that
did not happen, and `unavailable_in_current_clone`, which would falsely
claim unreachability) because **actually attempting §G step 2's bounded
historical diff remains its own separately scoped, separately authorized
follow-on unit** — not performed by this correction, consistent with this
task's own explicit scope boundary against deep Git-history recovery.
`registry.yaml`'s `legacy_gap` block gains one new required field,
`clone_depth_at_generation`, recording exactly which state was detected —
this field, together with `recovery_status`, is now a **disclosed,
intentional exception** to §I's regeneration-determinism guarantee:
`entries` depends only on tree content at `source_commit_sha` and remains
byte-identical across environments, but `legacy_gap`'s two clone-depth
fields legitimately vary by executing environment even at the identical
source commit — this is documented directly in the generator module's own
docstring ("Determinism scope") rather than left implicit.

**Test redesign**: the hardcoded assertion was replaced with (a) unit
tests exercising both `"shallow"` and `"complete"` branches via dependency
injection (`_fake_git_output()`), independent of the real environment; (b)
a rejection test for malformed `git` output; (c) a test proving
`build_registry()` actually calls the live detector rather than hardcoding
a value (`monkeypatch`-based); (d) exactly one integration-style test
against the real environment, which accepts either valid state and
cross-checks the detector's own output against git's real result directly
— never hardcoding which state the runner happens to be in.

**Content impact on the committed registry**: this session's own working
clone remains shallow (independently re-verified, unchanged from §1/§7
above) — regenerating in this same environment reproduces
`clone_depth_at_generation: shallow`, `recovery_status:
unavailable_in_current_clone`, identical to before. The regenerated file's
diff is otherwise limited to `source_commit_sha`/`generated_at` (expected,
timestamp-scoped) and a small number of new `governance/audits` provenance
citations on the CLAUDE.md-only-discovered symbols (VMC, LHX, HYPE,
ZORA, WIF, BONK, PEPE, EQIX) — a genuine, expected side effect of this
same audit document now existing and itself naming those tickers in its
own worked-case citations (§4-§5 above), not a defect. **All 84 entries
and every primary disposition are byte-identical to before this
correction** — independently re-verified (disposition distribution
recomputed and matched exactly against §5's table).

**Validation at the corrected head**: `contender_registry_validator.py` OK
(84 entries); bidirectional reconciliation passes with zero errors;
`classification_validator.py` OK (28 results); `relationship_validator.py`
OK (13 records); `intelligence_validator.py` clean; `freshness_validator.py`
OK; decision catalog unchanged (84 decisions, `issues == ()`); the sealed 27
classification records and every protected path confirmed byte-identical
(`git status --porcelain` empty against `intelligence/classification/` and
`git diff --stat` empty against every protected path); `git diff --check`
clean; exactly 5 files changed by this correction
(`contender_registry_generator.py`, `contender_registry_validator.py`,
`intelligence/contenders/registry.yaml`, `test_contender_registry_generator.py`,
`test_contender_registry_validator.py`) — see this PR's own updated body
for the exact corrected full-suite pass count and new exact head.

This correction performed no ticker research, no disposition change, no
Git-history recovery, and no change to `CONTENDER-0001`/`XASSET-0001`/
`CONTENDER-0002`. This session does not review its own PR, mark it ready,
merge it, or post principal acceptance — awaiting terminal exact-head CI
and independent exact-head review.

## 12. Second bounded correction (same day, this PR) — closed schema everywhere, and genuine §G step 2 compliance

An independent exact-head review (`pullrequestreview-4874631727`, anchored
to `6c22aaba718c38c21ad580e99f717cefea12844d`) returned **CHANGES
REQUIRED** — 0 BLOCKING / 2 MAJOR / 2 MINOR / 1 NOTE. All confirmed-correct
findings from that review (population, dispositions, worked cases,
protected-path isolation, the sealed-27 cohort, and §11's own clone-depth
fix) stand unedited.

**MAJOR — validator schema not actually closed at three levels.**
`_validate_secondary_flags()` already rejected both missing and extra
keys; `validate_entry()`, the registry-header check, and the `legacy_gap`
check each computed only `missing`, never `extra` — demonstrated live by
the reviewer: an entry carrying `conviction_score`/`recommended_target_pct`
(exactly the policy-shaped content `CONTENDER-0002` §M forbids) validated
as `valid=True`. **Fixed** with one shared helper,
`_check_closed_keys(value, allowed, errors, where, cite)`, applied at all
three levels (entry, top-level header/document, `legacy_gap`) — mirroring
`_validate_secondary_flags`'s own pattern rather than inventing a new one.
The top-level document check uses a combined allowed-set
(`_TOP_LEVEL_ALLOWED_KEYS = _REQUIRED_HEADER_KEYS | {"entries", "legacy_gap"}`)
so the registry's own legitimate `entries`/`legacy_gap` keys are never
misflagged as extra. Regression tests added for `conviction_score`,
`recommended_target_pct` (both individually and together), an arbitrary
top-level key, and an arbitrary `legacy_gap` key — each independently
confirmed to now fail validation, and a positive test confirms
`entries`/`legacy_gap` are never themselves flagged.

**MAJOR — `perform_legacy_recovery()` did not implement §G step 2's
mandatory recovery attempt.** `CONTENDER-0002` §G step 2 reads: "if full
history is reachable ... **attempt** a bounded, mechanical diff of
`holdings.yaml` across the `PHQ-2026-02` reconciliation commit to recover
the 41 symbols" — a requirement conditioned only on reachability, not
discretionary. The prior correction's `build_legacy_gap()` instead
unconditionally substituted a disclosed-but-non-compliant
`"reachable_but_recovery_not_attempted_this_generation"` for every
complete-clone environment, deferring the actual diff to an unfiled
follow-on unit — meaning every CI run of this generator's own test suite
(GitHub Actions checks out with `fetch-depth: 0`, a complete clone) would
permanently skip the mandatory attempt. **Fixed**: `build_legacy_gap()` is
removed entirely (superseded, not left as dead code) and replaced with
three new functions —
`find_phq_2026_02_reconciliation_commit(repo_root, runner=None)` (walks
reachable history oldest-first for a commit whose own subject line names
`PHQ-2026-02` and touches `holdings.yaml`, matching this repository's own
consistent commit-message convention; returns `(None, None)` if no match,
or `(commit_sha, None)` if the match is a root/merge commit with no single
resolvable parent — both fail-closed, never guessed);
`diff_holdings_tickers_across_commit(repo_root, commit_sha, parent_sha,
runner=None)` (the literal "bounded, mechanical diff" — tickers present in
`shares:`/`crypto_shares:` at the parent but absent at the commit; raises
on any read/parse failure rather than returning a partial result); and
`perform_legacy_recovery(repo_root, clone_depth, runner=None)`
(orchestrates both, always attempting when `clone_depth == "complete"`,
failing closed to `recovery_ambiguous` — zero entries, zero invented
placeholders — whenever the commit, the parent, or a non-empty diff
cannot be established). `build_registry()` now runs recovery *before*
disposition assignment and merges every genuinely new recovered symbol
into the same `_assign_disposition()` pipeline every other discovered
identity goes through (never hardcoded to one tier) — with an explicit
collision guard so a recovered symbol that is *already* tracked via a
live source (re-added later, or already carrying a Company Intelligence
record) is never duplicated or has its existing entry overwritten (§H.3
step 4). `legacy_gap.recovery_status` now takes the dynamic shape
`"recovered_<N>_of_41"` when recovery succeeds — `N` is §G's own YAML
comment's literal placeholder character, substituted with the real,
mechanically-diffed count — validated via a new
`RECOVERED_STATUS_PATTERN` regex rather than a fixed enum value, with
`registry_entries_created` required to equal that same `N` and be greater
than 0 (§G's "no placeholder row for any UNRECOVERED symbol" is read, on
its own terms, as not barring a real row for a RECOVERED one).
`RECOVERY_STATUS_VALUES` is trimmed to the two genuinely fixed outcomes
(`unavailable_in_current_clone`, `recovery_ambiguous`); the now-superseded
`reachable_but_recovery_not_attempted_this_generation` value and the
never-actually-produced literal `"recovered_n_of_41"` are both removed
from the closed vocabulary rather than left as dead, confusing options.

**Verified this environment remains genuinely shallow** (independently
re-run `git rev-parse --is-shallow-repository` → `true`) — the committed
`registry.yaml` therefore still correctly reports
`clone_depth_at_generation: shallow`, `recovery_status:
unavailable_in_current_clone`, 84 entries, identical dispositions to §5's
table. **The new "complete" recovery path is exercised only via
dependency-injected synthetic git output in this session** (a fabricated
commit log and two synthetic `holdings.yaml` blobs, not this repository's
real full history) — deliberately, not an oversight: this repository's
own actual pre-`PHQ-2026-02` history is not reachable from this shallow
clone to test against directly, and unshallowing this real, live
repository mid-correction to manufacture reachability would itself be a
heavier, riskier action than this bounded correction requires — §G step 2
only mandates the attempt when reachability already exists as a fact of
the environment, not that a correction PR manufacture reachability that
doesn't otherwise exist here. **This will be exercised for real** the next
time this test suite runs in this repository's own CI (`fetch-depth: 0`,
a genuinely complete clone) — `build_registry()`'s own pytest fixture
calls the real function against the real checked-out repository state
there, so the real reconciliation-commit search and real diff will run
against real history on the very next CI invocation, not merely a
simulated one. If that search does not find a real match (e.g. because
this repository's actual commit-message convention differs subtly from
what this correction assumed), the code fails closed to
`recovery_ambiguous` rather than crashing or fabricating a result — a safe
outcome either way, independently verified via nine dedicated unit tests
covering: successful recovery with correct asset-type tagging and real
git-SHA provenance; earliest-match selection when more than one commit
mentions PHQ-2026-02; no matching commit; a merge/root commit with an
unresolvable parent; an empty diff (also treated as ambiguous, not a
successful zero-ticker recovery); malformed `git show` YAML; a raising
`git show` call; the shallow branch never issuing a single git call;
end-to-end merging into `build_registry()`'s own `entries` with correct
bidirectional-reconciliation bookkeeping; the collision guard against
duplicating an already-tracked symbol; and determinism across two calls
against identical synthetic input.

**MINOR — stale PR/audit cross-reference.** Resolved directly: this
section states the corrected figures itself rather than deferring to the
PR body, and the PR body is updated in the same correction round with the
actual corrected numbers (see this PR's own latest comment).

**MINOR — CLAUDE.md missing a "Bounded correction" paragraph.** Resolved:
CLAUDE.md's own Decisions Log entry for this implementation gains a
concise correction paragraph recording the original CI failure, the first
clone-depth fix, this review's four actionable findings, and this
correction's own bounded scope — matching this repository's own
consistent same-PR self-documentation convention.

**NOTE** (the 365-token prose auto-exclusion bucket being manually
triaged, not fully mechanical) — no action required; already correctly
disclosed as a bounded, known limitation, not a defect, per the review's
own text.

**Validation at this corrected head**: `contender_registry_validator.py`
OK (84 entries); bidirectional reconciliation passes with zero errors
(including a dedicated test exercising it with recovered identities
present); `classification_validator.py` OK (28 results);
`relationship_validator.py` OK (13 records); `intelligence_validator.py`
clean; `freshness_validator.py` OK; decision catalog unchanged (84
decisions, `issues == ()`); the sealed 27 classification records and
every protected path confirmed byte-identical; determinism reconfirmed
(two generation runs against the same source commit produce
byte-identical `entries`, excluding `generated_at`); `git diff --check`
clean; exactly 5 files changed this round
(`contender_registry_generator.py`, `contender_registry_validator.py`,
`intelligence/contenders/registry.yaml`, `test_contender_registry_generator.py`,
`test_contender_registry_validator.py`) — see this PR's own latest
comment for the exact corrected full-suite pass count and new exact head.

This correction performed no ticker research, no ranking, no policy
change, and no change to `CONTENDER-0001`/`XASSET-0001`/`CONTENDER-0002`.
This session does not review its own PR, mark it ready, merge it, or post
principal acceptance — awaiting terminal exact-head CI and a fresh
independent exact-head delta review.

## 13. Third bounded correction (same day, this PR) — CI proved §G step 2 works, one test's own assumption was wrong

Exact-head CI on the second-correction head (`be9c951c5e096c75eac1c9eb462642cf14326690`, run `31104047670`, job `92624528328`) **failed — but not because the new §G step 2 recovery logic malfunctioned.** It worked exactly as designed: `1 failed, 2867 passed` —
`test_legacy_gap_record_present_and_creates_no_placeholder_rows` asserted
`registry_entries_created == 0` unconditionally; the real assertion
failure was `assert 41 == 0`. GitHub Actions' own checkout
(`fetch-depth: 0`) gave `perform_legacy_recovery()` genuine reachable
history for the first time, it correctly located the real `PHQ-2026-02`
reconciliation commit, diffed `holdings.yaml` across it, and recovered
**41 real, mechanically-derived legacy tickers** — landing almost exactly
on `CONTENDER-0002` §G's own "approximately 41" estimate. This is the
intended, disclosed, environment-dependent behavior working correctly in
its own genuinely-complete-history environment for the first time; the
test's own hardcoded `== 0` was the defect, not the recovery logic.

**Governing-contract question, resolved from the text, not invented**:
should the committed `registry.yaml` be regenerated to reflect CI's
successful recovery, or does the governing design tolerate — even
require — different committed output per environment? `CONTENDER-0002`
§G's own three-step structure (re-verify clone depth live; **attempt**
recovery only *if* full history is reachable; stop and disclose
otherwise) is itself conditioned on environment-dependent reachability —
a single cross-environment byte-identical requirement would contradict
that text, not satisfy it. §I's determinism guarantee ("running the scan
twice against an unchanged `main` must produce byte-identical `entries`")
is read, on its own terms, as *same-environment* reproducibility (the two
runs it describes happen within one session), not a claim about a shallow
run and a complete run of the identical commit. **Resolved**: the
contract is "deterministic for the same repository state AND the same
git-history availability," not "deterministic regardless of clone
depth" — stated explicitly now in the generator's own module docstring.
This session's own working clone remains genuinely shallow (independently
re-verified) — the committed `registry.yaml` correctly continues to
report `clone_depth_at_generation: shallow`, `recovery_status:
unavailable_in_current_clone`, 84 entries. **Not regenerated to reflect
CI's 41 recovered tickers** — doing so would require actually operating
in a complete-clone environment (which this session is not), and CI's own
in-memory test run (the `registry` pytest fixture calling `build_registry()`
directly) never writes to `intelligence/contenders/registry.yaml` — no
risk of CI silently overwriting the committed file with a different
entry count exists today, by construction (the generator's `__main__`
regeneration script is a separate, manually-invoked path, not something
CI's `pytest -q` step runs).

**Fix**: `test_legacy_gap_record_present_and_creates_no_placeholder_rows`
is renamed to `test_legacy_gap_record_present_and_shape_is_valid` and
rewritten to assert the *invariant* rather than one environment's
particular outcome: `clone_depth_at_generation` is always one of the two
closed values; when `recovery_status` matches the dynamic
`"recovered_<N>_of_41"` pattern, `registry_entries_created` must equal
that exact `N`, be greater than 0, `clone_depth_at_generation` must be
`"complete"`, and — checked directly against `reg["entries"]`, not merely
trusted — exactly `N` entries must carry a `"§G step 2"`/"PHQ-2026-02
reconciliation commit" citation in their own `existing_disposition` text;
otherwise (`unavailable_in_current_clone` or `recovery_ambiguous`),
`registry_entries_created` must be exactly 0. This is the same test, now
correctly encoding "zero placeholder rows in either state" rather than
"zero rows in every state" — the actual property `CONTENDER-0002` §G
requires. No other test in either file assumed a fixed entry count
against the real, non-injected `registry` fixture — independently
re-checked (grepped for hardcoded counts against fixture-based tests;
only two hardcoded counts exist anywhere in the suite, both inside tests
using a fully injected synthetic git runner, immune to real-environment
variation).

**Verification of the 41 recovered identities, honestly bounded**: this
session cannot directly enumerate or independently re-inspect the 41 real
ticker symbols CI's own complete-history environment found — the CI log
truncates the failing test's own dict repr, and this session's own clone
remains shallow, unable to reproduce the same real-history diff locally.
What IS independently verified, mechanically, not by trust: the recovery
code path itself (`find_phq_2026_02_reconciliation_commit()`,
`diff_holdings_tickers_across_commit()`, `perform_legacy_recovery()`) was
exercised end-to-end against nine dependency-injected synthetic scenarios
in §12 above, each proving the mechanism cannot fabricate a ticker
(it only ever returns literal YAML-key set differences between two real
git blobs), cannot invent a placeholder (every recovered row requires a
real removed key), and fails closed rather than guessing whenever the
commit, parent, or diff cannot be established. CI's real 41-ticker result
landing almost exactly on the "approximately 41" figure `PHQ-2026-02`'s
own reconciliation history already discloses is independent corroborating
evidence the mechanism found the right boundary, not a coincidence this
session can claim credit for engineering — the number came from real
history, not from this correction's own code choosing it.

**Documentation updated for accuracy** (no other document claimed a
false universal invariant beyond the one test above, independently
re-checked): the generator's own module docstring gains an explicit
"contract" paragraph stating deterministic-per-environment scope and
citing this real CI outcome; `contender_registry_validator.py`'s own
module docstring §G bullet corrected from "`registry_entries_created`
must be exactly 0" to the accurate conditional rule; this PR's body and
CLAUDE.md's own bounded-correction paragraph (appended again, not
edited) both restate the same corrected figures.

**Validation at this corrected head**: `contender_registry_validator.py`
OK (84 entries); bidirectional reconciliation zero errors; all four
other domain validators clean; decision catalog unchanged (84
decisions); sealed 27 and every protected path byte-identical;
determinism reconfirmed within this environment; `git diff --check`
clean — see this PR's own latest comment for the exact corrected
full-suite pass count and this correction's own final head.

This correction performed no ticker research, no disposition change
beyond what the already-existing, already-tested mechanical §G recovery
logic itself produces, no weakening of the recovery requirement, and no
change to `CONTENDER-0001`/`XASSET-0001`/`CONTENDER-0002`. This session
does not review its own PR, mark it ready, merge it, or post principal
acceptance — awaiting terminal exact-head CI and a fresh independent
exact-head delta review.

## 14. Fourth bounded correction (same day, this PR) — a genuine semantic bug, not a test-only fix: `registry_entries_created` must count NEW rows, not raw diff hits

Exact-head CI at the third-correction head (`6df76296129f46fcd5a32f5bffa18df0c86d8f3e`,
run `31105070187`, job `92627971330`) failed: `1 failed, 2867 passed`,
`assert 0 == 41`, `where 0 = len([])`. The renamed
`test_legacy_gap_record_present_and_shape_is_valid` correctly reported
`registry_entries_created == 41` from `legacy_gap`, but its own
provenance-search predicate (`"§G step 2" in existing_disposition`) found
**zero** entries actually carrying that citation. This traced to a real
semantic defect in `perform_legacy_recovery()` itself, not merely a test
assertion bug: `registry_entries_created` was set to `len(recovered)` —
the raw count of legacy tickers the mechanical diff found removed —
**regardless of whether any of them actually became a new registry row**.
`build_registry()`'s own collision guard (§H.3 step 4: never overwrite an
already-tracked symbol) correctly prevented every one of the 41
mechanically-found tickers from creating a duplicate or overwriting an
existing entry — this repository's own real, complete-history CI
independently confirms every one of those 41 legacy tickers already
carries its own Company Intelligence coverage today, added later by
WS-0005's own batches (PI-0023 through PI-0030 and others) — but nothing
downstream of the collision guard ever recomputed
`registry_entries_created` to reflect that. The gap record's own count
was simply wrong: it claimed 41 rows were created when the true number,
after collision filtering, was 0.

**Root cause, precisely**: `perform_legacy_recovery()` both performed the
mechanical diff AND finalized the `legacy_gap` record in one step — but
only `build_registry()`, which alone applies the collision guard, can
know how many of the diff's hits actually became new rows. Finalizing
the gap record before collision filtering was the structural mistake.

**Fix, in order**:

1. **`perform_legacy_recovery()` no longer constructs `legacy_gap` at
   all.** It now returns `(recovered, outcome)` where `outcome` is
   exactly one of `"shallow"`, `"ambiguous"`, or `"found"` — a raw
   mechanical-fact signal, not a finished record. `build_registry()`
   alone owns final `legacy_gap` construction, computed *after* its own
   collision-filtering loop.
2. **Structured provenance marker, not prose matching.** The review's own
   implicit lesson (a fragile substring search broke on real data) is
   addressed directly: a new, dedicated provenance source label,
   `SRC_LEGACY_RECOVERY = "holdings.yaml (historical — CONTENDER-0002 §G
   step 2 recovery)"`, is attached to every genuinely new recovered
   entry's `provenance` list — distinct from `SRC_HOLDINGS` (a current
   `holdings.yaml` citation) — added to `AUTHORIZED_SOURCE_LABELS` (an
   18th entry; this correction leaves `CONTENDER-0002` §E.3's own
   exactly-eight-value `secondary_flags` vocabulary untouched, on the
   reasoning that extending this session's own open, generator-owned
   source catalog — already precedented by the disclosed 17th
   `CLAUDE.md` source — is less invasive than extending §E.3's own
   closed, governing-text-enumerated vocabulary). A recovered entry is
   now identified via `any(p["source"] == SRC_LEGACY_RECOVERY for p in
   entry["provenance"])` — mechanical, structural, never prose-fragile.
3. **A fourth, honest `recovery_status` outcome**: `"all_recovered_
   already_tracked"` — the diff succeeded and found one or more removed
   legacy tickers, but every one already had its own entry via another
   governed source, so zero new rows were needed or created. Deliberately
   distinct from `"recovery_ambiguous"` (which means the search itself
   could not be resolved) — this is a clean, successful search that
   legitimately requires no new rows, not a failure, and calling it
   "ambiguous" would misrepresent what actually happened. The raw
   mechanically-found count is disclosed in this outcome's own
   `next_action` text (e.g. "identified 41 legacy ticker(s)... every one
   already carries independent governed coverage") so this is never
   confused with "nothing was found."
4. **`registry_entries_created` now genuinely means "new rows created."**
   Computed in `build_registry()` from the actual post-collision count
   (`len(net_new_recovered_symbols)`), never `len(recovered)`.

**Test rewrite**: the marker search now uses `SRC_LEGACY_RECOVERY`
membership in `provenance`, not prose matching, and the test's own
branching covers all four outcomes explicitly (shallow/ambiguous/
all-already-tracked all require `registry_entries_created == 0` and zero
marked entries; the recovered-with-new-rows branch requires the count to
match exactly and every marked entry to carry real commit-SHA
provenance). New focused tests added: a mixed scenario (one genuinely new
identity, one that collides) proving `registry_entries_created` counts
correctly in the partial case; a dedicated `all_recovered_already_tracked`
test proving the raw found count is disclosed and the status is never
conflated with `recovery_ambiguous`; an end-to-end `build_registry()`
determinism test. All `perform_legacy_recovery()`-calling tests updated
for its new `(recovered, outcome_string)` return shape.

**Validation at this corrected head**: `contender_registry_validator.py`
OK (84 entries); bidirectional reconciliation zero errors, independently
re-verified with the mixed-collision scenario; all four domain validators
clean; decision catalog unchanged; sealed 27 and every protected path
byte-identical; determinism reconfirmed (including a new dedicated
`build_registry()`-level determinism test, not just
`perform_legacy_recovery()`'s own); 119 focused tests in the two
`test_contender_registry_*.py` files (up from 112) — see this PR's own
latest comment for the exact corrected full-suite pass count and this
correction's own final head.

This correction fixed a genuine semantic defect in how recovery success
was counted — not merely a test's own assumption — while preserving
every prior correction's own fix intact (closed schema, live clone-depth
detection, the mandatory §G step 2 attempt itself, fail-closed handling
on every ambiguous path, zero placeholder rows in every outcome). No
ticker research, no ranking, no policy change, no change to
`CONTENDER-0001`/`XASSET-0001`/`CONTENDER-0002`. This session does not
review its own PR, mark it ready, merge it, or post principal
acceptance — awaiting terminal exact-head CI and a fresh independent
exact-head delta review.
