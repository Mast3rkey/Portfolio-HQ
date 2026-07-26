# WS-0005 Preliminary Portfolio Architecture and Target-Scenario Package

**PROVISIONAL. ADVISORY. REVERSIBLE. Not final policy. Not an execution instruction.**
Authorized by `governance/decisions/OPS-0007-capability-based-review-provisional-allocation-bridge.md`
§4 (preliminary portfolio architecture authority). Created 2026-07-26, following
PR #161's merge and post-merge PROVISIONAL-status determination (see Mandatory
provisional metadata below for exact heads/commits).

**Bounded correction note (this revision):** an independent ChatGPT review
(review `4781581139`, verdict CHANGES REQUIRED, session identifier
`chatgpt-pr163-review-20260726-01`) found three Major findings in the prior
revision: (1) the evidence-status classification (7 ACCEPTED / 10
PROVISIONAL) conflicted with `OPS-0007` §4's own literal text, which treats
"the thirteen existing records" collectively as currently accepted
Intelligence; (2) the 17-holding reconciliation used global narrative
paragraphs instead of a per-holding decision trail, making the zero-change
conclusion unauditable; (3) the coverage-gap register grouped multiple
tickers per row and omitted required fields. This revision corrects all
three, plus two Minor findings (a misstated roster count, and ambiguous
research-priority wording) — see each section below for the specific fix.

## What this document is and is not

This is a **preliminary, evidence-based organization** of the current portfolio's
already-researched holdings, prepared to support a later, separate, scenario-only,
cash-only, zero-margin Monday allocation-check package (OPS-0007 §5 — not yet
authorized to run, not performed here). It is:

- **provisional** — subject to revision as more Intelligence coverage accumulates
  and as WS-0005's later, deeper milestones (4-9, all still unauthorized) proceed;
- **advisory** — informs judgment, recommends no trade, order, or margin action;
- **reversible** — changes nothing in `targets.yaml`, `holdings.yaml`, `allocate.py`,
  or `margin_state.py`; a future decision may adopt, revise, or discard any
  conclusion here without cost, per OPS-0007 §6's sunset discipline;
- **not a claim that portfolio-wide research is complete** — only 17 of the
  portfolio's 62 company holdings currently have any Company Intelligence
  record (see Coverage classification below and the companion Coverage-Gap
  Register).

This document does **not**: change any tier, target, role, cluster, cap, or
holding; create a mechanical score or rank companies from best to worst;
recommend a trade, buy, trim, exit, or margin deployment; claim Milestones 3-8
complete, in whole or in part, beyond what is factually recorded in
`operations/WORKSTREAMS.yaml`; or authorize a fourth Milestone-3 batch or any
Milestone-4-9 execution.

## Roster counts (corrected)

`holdings.yaml`'s `shares:` block contains **65 total share-target roster
entries**. Of those:

- **62 are company holdings**, of which:
  - **17 carry a qualifying Company Intelligence record** (13 ACCEPTED + 4
    PROVISIONAL — see Coverage classification below);
  - **45 are NOT INDEPENDENTLY RE-DERIVED** (full register in
    `WS0005_COVERAGE_GAP_REGISTER_20260726.md`).
- **3 are ETFs** (SPY, QQQ, GLD) — a structurally separate category, not
  "uncovered companies"; see that register's own ETF-baseline section.

(The prior revision's "65 non-ETF holdings" phrasing was incorrect and is
retracted — the roster is 65 total entries, of which 62 are companies and 3
are ETFs, not 65 non-ETF entries.)

## Coverage classification

Every one of the 62 company holdings is classified into exactly one of two
evidence-status categories defined by `OPS-0007` §4 itself, plus the
structurally separate ETF category — determined from retained governance and
review evidence, never inferred from the mere existence of a YAML file.

| Category | Count | Definition (per `OPS-0007` §4) |
|---|---|---|
| **ACCEPTED INTELLIGENCE** | 13 | `OPS-0007` §4's own "the thirteen existing records" — every Company Intelligence record that existed and was merged to `main` before PR #161, regardless of which prior process (a `PI-0016`-style committee review, or a first-coverage `PI-####` batch authorization) produced it |
| **PROVISIONAL INTELLIGENCE** | 4 | PR #161's four records (AVGO, AMD, MRVL, INTC) — the only batch that has ever been required to satisfy, and has now independently satisfied, `OPS-0007` §3's five-part PROVISIONAL definition, because it is the first batch to merge after `OPS-0007` itself existed |
| **NOT INDEPENDENTLY RE-DERIVED** | 45 companies (+ 3 ETFs, separate category) | No qualifying Company Intelligence record exists; current governed policy is preserved as an unchanged, temporary baseline only |

### ACCEPTED INTELLIGENCE (13)

COST, XOM, NVDA, GEV, ISRG, TMO, TSM, ASML, AMAT, KLAC, LRCX, MU, SKHY —
exactly `OPS-0007` §4's own enumerated "thirteen existing records," quoted
verbatim: *"currently accepted Intelligence (the thirteen existing records,
plus any batch — including PR #161's AVGO/AMD/MRVL/INTC records — only once
it meets every element of §3's five-part PROVISIONAL definition...)."*
`OPS-0007` §2 separately confirms that "every existing retained Fable review
on this repository's merged history remains valid exactly as recorded; this
decision changes no past review's status" — meaning all 13 records' prior
review/merge history (each under its own `PI-####` authorization, predating
`OPS-0007`) is unaffected and treated as already-accepted.

**Correction retracted from the prior revision:** the prior revision split
this group into a narrower 7-record "ACCEPTED" set (requiring a `PI-0016`
committee review) and moved the other 6 (ASML, AMAT, KLAC, LRCX, MU, SKHY)
into "PROVISIONAL." `OPS-0007` §4's text does not draw that line — it treats
all 13 pre-PR-#161 records as one accepted set. This revision follows that
literal structure. Governance authority to redefine the ACCEPTED/PROVISIONAL
boundary itself was not sought and is out of scope for this bounded
correction.

**Distinguishing accepted standing from deeper review depth (a non-
reclassifying annotation).** All 13 are ACCEPTED under `OPS-0007` §4. Within
that single category, this pass separately notes — for transparency, not as
a reclassification — that seven of the thirteen (COST, XOM, NVDA, GEV, ISRG,
TMO, TSM) additionally underwent `PI-0016`'s standing committee-review
methodology or an equivalent explicit, field-by-field human-approval process
recorded in their own `review.log`, while six (ASML, AMAT, KLAC, LRCX, MU,
SKHY) were accepted via first-coverage `PI-0023`/`PI-0024` batch review and
principal acceptance without that deeper committee-review layer. Both groups
are equally ACCEPTED for `OPS-0007` §4 purposes; the underlying evidence
quality and review depth genuinely differ and are recorded per-holding in
`WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`'s own evidence-quality
field, not smoothed into a single label.

### PROVISIONAL INTELLIGENCE (4)

AVGO, AMD, MRVL, INTC (Batch 3, `PI-0025`, PR #161). Independently verified
against `operations/WORKSTREAMS.yaml` and PR #161's own merge/review
evidence: eligible-reviewed under `OPS-0007` §1 (reviews `4781479573`,
`4781536364`), bounded-corrected for the one material finding, principal-
accepted, merged to `main` at `270b47163bde6999dd336ff327965bbc7b5fd031`,
and post-merge ancestry/scope/validator/test-verified — all five elements of
`OPS-0007` §3 independently confirmed satisfied. **None has yet undergone
`PI-0016`'s deeper committee-review methodology or WS-0005's own Milestone-9
review** — each record's own `review.log` explicitly states its conviction
rating "reflect[s] AI-assisted research pending independent PR review and
human approval" at authoring time, a disclosure this package does not paper
over. PROVISIONAL status here means exactly `OPS-0007` §3's five elements
are satisfied — nothing more.

### NOT INDEPENDENTLY RE-DERIVED (45 companies)

Every other company roster entry. Full register, one explicit row per
ticker (no grouping), in the companion
`WS0005_COVERAGE_GAP_REGISTER_20260726.md`. Current role, tier, and target
for each is preserved **exactly**, labeled `temporary current-policy
baseline — not independently re-derived` throughout this package — never
treated as independently confirmed, never treated as evidence the placement
is correct.

### ETF BASELINE (3) — a separate structural category

SPY, QQQ, GLD. These are **not** "uncovered companies" — they are index/
commodity-tracking funds, a structurally different category the Company
Intelligence schema does not apply to (see the coverage-gap register's own
ETF-baseline section for each fund's full disposition). Current target
preserved exactly for all three.

## Methodology (qualitative, not a composite score)

For each of the 17 ACCEPTED/PROVISIONAL holdings, this pass reasoned — from
each record's own disclosed evidence, before comparing to current policy, per
`OPS-0006` §§2/3's zero-based discipline — through the full 20-field decision
trail now given per holding in `WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`:
economic role, evidence-derived candidate role, conviction, evidence
quality, confidence, distinct portfolio function, meaningful overlap/
redundancy, major risk amplifiers, thesis-deterioration detectability,
candidate tier, candidate target range, point target, target change, a
zero-based reason for preserving or changing the candidate tier/point target
(never citing the current target itself as evidence), unresolved evidence,
and possible later allocator-output difference. No numeric score was
computed or combined across these factors.

**Central finding of this pass: for all 17 covered holdings, the evidence
gathered is consistent with — does not decisively contradict — current
governed tier and target placement.** This is itself a real, disclosed,
zero-based conclusion, not a default — several of the 13 ACCEPTED holdings
(COST, NVDA, GEV) reached this conclusion through `PI-0016`'s own explicit
"Keep current policy" committee output; the remaining 14 reached it through
this pass's own independent, now fully per-holding-documented reasoning in
the reconciliation artifact. **This is explicitly different from the NOT
INDEPENDENTLY RE-DERIVED category**: those 45 companies' current policy is
preserved because no evidence check has occurred at all; these 17 holdings'
current policy is preserved because an evidence check occurred, per holding,
and did not surface a specific, schema-expressible reason to differ.

**One directional observation, not implemented as a target change.** AVGO's
evidence (rapidly accelerating AI-semiconductor revenue, an improving credit
profile, and a defensive recurring-software segment none of its immediate T2
peers carry) trends toward the stronger end of a plausible T2 range; TMO's
evidence (positive but comparatively muted segment growth) trends toward the
more moderate end. **This directional difference is not reflected in the
machine-readable scenario file**, because `targets.yaml`'s tier structure
applies one uniform `weight_pct` to every ticker within a tier — expressing a
single-ticker differentiated weight would require either a full tier
reassignment (a materially larger claim than this preliminary pass makes) or
a schema change to support per-ticker overrides (out of scope, not
authorized, and not necessary on the evidence gathered so far). This
structural limitation is itself a relevant finding for the still-unauthorized
Milestone 5 (zero-based classification/tier-architecture review) and is
recorded here for that future work, not resolved by this pass. A second,
more clearly unresolved tension (ASML's Medium conviction sitting at T1
without a `PI-0016`-style deeper review, unlike GEV's equivalent, already-
examined tension) is recorded per-holding in the reconciliation artifact and
similarly not resolved here.

**Net result: zero target-weight change among the 17 covered holdings.**
Production total for these 17: 28.70 percentage points (5×3.35 T1 + 3×1.65 T2
+ 8×0.75 band + 1×1.00 spec). Scenario total: 28.70 percentage points —
reconciles exactly, because no point target differs from current
policy. Full per-holding candidate role/tier/range/point-target table with
20-field reasoning per ticker: `WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`.

## Proof unsupported holdings are unchanged

Independently verified (see Validation below): `operations/provisional/ws0005_provisional_target_scenario_20260726.yaml`
loaded via `allocate.py`'s own `build_roster()` produces a roster
**identical** to production `targets.yaml`'s roster — same 65 tickers, same
per-ticker `{tier, weight_pct, fixed, cap_multiple}` for every single entry,
zero difference in aggregate weight (93.25 percentage points, both files).
This is not merely claimed; it was computed and compared programmatically
against both files as they exist on disk.

## Coverage gaps

See the companion `WS0005_COVERAGE_GAP_REGISTER_20260726.md` for the full
register: **one explicit row per each of the 45 uncovered company holdings**
(current target/role/tier baseline, why not independently re-derived,
missing research, material risk of relying on the temporary baseline,
whether the gap could materially affect a future provisional allocation
result, and a future research trigger), plus a **separate, fully-disposed
ETF-baseline section** for SPY/QQQ/GLD. No candidate is ranked for capital
allocation. Any discussion of a gap's materiality reflects
**research-coverage urgency only** — never a capital ranking, and never a
batch selection or authorization. (The prior revision's "highest-priority
gap"/"higher-priority gap" phrasing has been replaced throughout the
register with neutral materiality language, per the independent review's
Minor 2 finding.)

## Assumptions and unresolved evidence

- Every ACCEPTED/PROVISIONAL record's own disclosed unresolved-evidence items
  (e.g. AMD's unresolved >10%-customer claim, INTC's four-value government-
  stake range, MRVL's disputed Amazon-Trainium signal, MU's entirely-missing
  customer-concentration figure, SKHY's never-opened F-1/424B4 section) are
  preserved exactly as each record discloses them, now indexed per-holding in
  the reconciliation artifact's own item 19 for each ticker — this package
  does not resolve, smooth over, or silently drop any of them.
- This package assumes each of the 17 records' conviction rating and
  disclosed risk picture remain current as of this package's evidence
  cutoff (below); no record was re-researched for this pass.
- Live `holdings.yaml` share counts and market prices will be refreshed
  separately, at run time, before any future Monday allocation-check package
  consumes this scenario file — per `CLAUDE.md` Workflow §2-3 and OPS-0007 §5
  item 4. This package's own holdings reference point is the snapshot
  already on file, not a live re-sync.

## Mandatory provisional metadata

- **Creation date:** 2026-07-26 (this revision: bounded correction pass
  following independent review `4781581139`).
- **Evidence cutoff:** 2026-07-26 (matches every ACCEPTED/PROVISIONAL
  record's own `review.last_reviewed` date for records reviewed this
  session's batch cycle; earlier for the pre-existing ACCEPTED records —
  see each record's own `review.log` for its specific date).
- **Exact authoritative `main` SHA at package creation:** `270b47163bde6999dd336ff327965bbc7b5fd031`
  (PR #161's merge commit).
- **PR #161 merge commit:** `270b47163bde6999dd336ff327965bbc7b5fd031`, parents
  `80bccbaebca1a7fcfa8069643cdb83355426ddb2` (base, `OPS-0007`'s own merge
  commit) and `c6fe6b0b3725c4fdba50c8b787123f09faf90805` (the reviewed,
  principal-accepted head).
- **Source Intelligence commit heads:** all 17 ACCEPTED/PROVISIONAL records
  as they exist at `270b47163bde6999dd336ff327965bbc7b5fd031` on `main` — no
  earlier or later head used for any record.
- **Holdings snapshot date already on file:** `holdings.yaml`'s `margin.synced_at: 2026-07-22`;
  share counts as currently committed. **Live holdings and market data will
  be refreshed separately before any future Monday allocation-check run
  consumes this package** — this package's own figures are not re-synced
  live.
- **Expiration date:** 2026-08-10 (15 calendar days from creation — shorter
  than the 30-day maximum this package's own authorization permits, given
  four of the thirteen ACCEPTED records now carry a PROVISIONAL sibling
  batch created same-day, and PROVISIONAL records' evidence is comparatively
  less battle-tested than the deeper-reviewed ACCEPTED subset's).
- **Mandatory earlier re-review triggers** (per OPS-0007 §6): a deeper Fable
  or other eligible-reviewer audit becomes available; any underlying
  ACCEPTED/PROVISIONAL record materially changes; research coverage
  materially expands (a fourth Milestone-3 batch, once separately
  authorized, merges); a material earnings/guidance/regulatory/customer/
  liquidity/thesis-break event affects any of the 17 covered holdings; this
  package's own expiration date arrives.
- **Supersession rule:** this package is superseded by (a) any future,
  separately authorized WS-0005 Milestone 4-9 work reaching its own
  reconciled conclusion for any of these 17 holdings, or (b) a later,
  separately authorized preliminary-architecture package with a newer
  evidence cutoff. A superseded package remains a dated, disclosed snapshot
  of what the evidence supported at the time — not treated as wasted work,
  per OPS-0007 §6.

## Validation performed

- All new/modified YAML parses clean.
- `operations/provisional/ws0005_provisional_target_scenario_20260726.yaml`
  independently confirmed loadable via `allocate.py`'s own `load_yaml()` and
  `build_roster()`; roster and aggregate weight confirmed **identical** to
  production `targets.yaml` (65 tickers, 93.25pp total, zero diff).
- `targets.yaml` confirmed byte-untouched (`git diff` against this branch's
  base shows zero changes to the file).
- `intelligence_validator.py`, `freshness_validator.py`, full pytest suite,
  `git diff --check`, decision-index reconciliation, and the exactly-one-
  primary-workstream invariant all re-run clean — see this package's PR
  description for exact results.
- Roster-count reconciliation independently re-verified: 65 total = 62
  companies (17 covered + 45 uncovered) + 3 ETFs.

## Next step

A fresh, exact-head independent ChatGPT re-review of this bounded correction
pass, anchored to its new exact head — the same reviewing session that
returned review `4781581139` (session identifier
`chatgpt-pr163-review-20260726-01`). This package's own PR remains in draft
and unmerged throughout. No Monday live allocation check has been run or is
authorized to run by this package alone — that remains OPS-0007 §5's own
later, separate, bounded authorization.
