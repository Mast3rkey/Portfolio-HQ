# WS-0005 Preliminary Portfolio Architecture and Target-Scenario Package

**PROVISIONAL. ADVISORY. REVERSIBLE. Not final policy. Not an execution instruction.**
Authorized by `governance/decisions/OPS-0007-capability-based-review-provisional-allocation-bridge.md`
§4 (preliminary portfolio architecture authority). Created 2026-07-26, following
PR #161's merge and post-merge PROVISIONAL-status determination (see Mandatory
provisional metadata below for exact heads/commits).

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
  portfolio's 65 non-ETF holdings currently have any Company Intelligence
  record (see Coverage classification below and the companion Coverage-Gap
  Register).

This document does **not**: change any tier, target, role, cluster, cap, or
holding; create a mechanical score or rank companies from best to worst;
recommend a trade, buy, trim, exit, or margin deployment; claim Milestones 3-8
complete, in whole or in part, beyond what is factually recorded in
`operations/WORKSTREAMS.yaml`; or authorize a fourth Milestone-3 batch or any
Milestone-4-9 execution.

## Coverage classification

Every one of the portfolio's 65 non-ETF share-tracked holdings (per
`holdings.yaml`'s `shares:` block) is classified into exactly one of three
evidence-status categories, determined from retained governance and review
evidence — never inferred from the mere existence of a YAML file.

| Category | Count | Definition |
|---|---|---|
| **ACCEPTED INTELLIGENCE** | 7 | Company Intelligence record that has, in addition to OPS-0007 §3's five elements, undergone `PI-0016`'s standing committee-review methodology or an equivalent explicit, field-by-field human approval recorded in its own `review.log` (not merely a whole-PR acceptance) |
| **PROVISIONAL INTELLIGENCE** | 10 | Company Intelligence record that independently satisfies every one of OPS-0007 §3's five elements — eligible-reviewed, bounded-corrected/re-reviewed if needed, principal-accepted, **merged to `main`**, and post-merge ancestry/scope/validator/test-verified — but has not yet undergone the deeper `PI-0016`-style committee review or WS-0005's own later Milestone-9 review |
| **NOT INDEPENDENTLY RE-DERIVED** | 48 (45 companies + 3 ETFs) | No qualifying Company Intelligence record exists; current governed policy is preserved as an unchanged, temporary baseline only |

### ACCEPTED INTELLIGENCE (7)

COST, XOM, NVDA, GEV, ISRG, TMO, TSM. Each record's own `review.log` documents
an explicit, named human-principal approval event under its own dedicated
`PI-####` authorization (`PI-0003`/`TGT-0002` for COST; `PI-0005` for XOM;
`PI-0007`/`PI-0017`/`PI-0018` for NVDA; `PI-0007`/`PI-0019`/`PI-0020` for GEV;
`PI-0011`-era first-coverage plus later refresh for ISRG; `PI-0009` for TMO;
`PI-0012`/`PI-0013` for TSM) — several (COST, NVDA, GEV) went through `PI-0016`'s
full standing committee-review methodology with an explicit "Keep current
policy" advisory conclusion recorded. These are treated as the strongest
evidentiary tier available in this repository today.

### PROVISIONAL INTELLIGENCE (10)

ASML, AMAT, KLAC, LRCX (Batch 1, `PI-0023`); MU, SKHY (Batch 2, `PI-0024`);
AVGO, AMD, MRVL, INTC (Batch 3, `PI-0025`). Independently verified against
`operations/WORKSTREAMS.yaml` and each batch's own merge/review evidence: all
three batches are merged to `main`, independently reviewed (Fable for
Batches 1-2; an eligible independent reviewer under `OPS-0007` §1 for Batch 3),
principal-accepted, and post-merge validator/test-verified. **None has yet
undergone `PI-0016`'s deeper committee-review methodology or WS-0005's own
Milestone-9 review** — each record's own `review.log` explicitly states its
conviction rating "reflect[s] AI-assisted research pending independent PR
review and human approval" at authoring time, a disclosure this package does
not paper over. PROVISIONAL status here means exactly OPS-0007 §3's five
elements are satisfied — nothing more.

### NOT INDEPENDENTLY RE-DERIVED (48)

Every other roster entry. Full register in the companion
`WS0005_COVERAGE_GAP_REGISTER_20260726.md`. Current role, tier, and target for
each is preserved **exactly**, labeled `temporary current-policy baseline —
not independently re-derived` throughout this package — never treated as
independently confirmed, never treated as evidence the placement is correct.

## Methodology (qualitative, not a composite score)

For each of the 17 ACCEPTED/PROVISIONAL holdings, this pass reasoned — from
each record's own disclosed evidence, before comparing to current policy, per
`OPS-0006` §§2/3's zero-based discipline — through: economic-role uniqueness;
durable competitive position; conviction and its stated rationale; business
and balance-sheet quality; cyclicality; customer/supplier concentration;
capital intensity; geopolitical/export-control exposure; liquidity and
refinancing risk; correlated-loss pathways; thesis-break detectability;
expected recovery duration after impairment; overlap with other holdings; and
evidence quality/unresolved uncertainty. No numeric score was computed or
combined across these factors — each holding's candidate range and point
target reflect a written, falsifiable judgment call, reproduced in full in
`WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`.

**Central finding of this pass: for all 17 covered holdings, the evidence
gathered is consistent with — does not decisively contradict — current
governed tier and target placement.** This is itself a real, disclosed,
zero-based conclusion (an "evidence-consistent" finding), not a default —
three of the seven ACCEPTED-tier holdings (COST, NVDA, GEV) reached this
conclusion through `PI-0016`'s own explicit "Keep current policy" committee
output; the remaining 14 reached it through this pass's own independent
reasoning, documented per-holding in the reconciliation table. **This is
explicitly different from the NOT INDEPENDENTLY RE-DERIVED category**: those
48 holdings' current policy is preserved because no evidence check has
occurred at all; these 17 holdings' current policy is preserved because an
evidence check occurred and did not surface a specific, schema-expressible
reason to differ (see below).

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
recorded here for that future work, not resolved by this pass.

**Net result: zero target-weight change among the 17 covered holdings.**
Production total for these 17: 28.70 percentage points (5×3.35 T1 + 3×1.65 T2
+ 8×0.75 band + 1×1.00 spec). Scenario total: 28.70 percentage points —
reconciles exactly, trivially, because no point target differs from current
policy. Full per-holding candidate role/tier/range/point-target table with
reasoning: `WS0005_CURRENT_POLICY_RECONCILIATION_20260726.md`.

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
per-holding register (45 companies + 3 ETFs): current target/role/tier
baseline, why each is not independently re-derived, material risk of relying
on the temporary baseline, missing research, whether the gap could materially
affect a future provisional allocation result, and an appropriate future
research trigger. No candidate is ranked for capital allocation.

## Assumptions and unresolved evidence

- Every ACCEPTED/PROVISIONAL record's own disclosed unresolved-evidence items
  (e.g. AMD's unresolved >10%-customer claim, INTC's four-value government-
  stake range, MRVL's disputed Amazon-Trainium signal) are preserved exactly
  as each record discloses them — this package does not resolve, smooth over,
  or silently drop any of them.
- This package assumes each of the 17 records' conviction rating and
  disclosed risk picture remain current as of this package's evidence
  cutoff (below); no record was re-researched for this pass.
- Live `holdings.yaml` share counts and market prices will be refreshed
  separately, at run time, before any future Monday allocation-check package
  consumes this scenario file — per `CLAUDE.md` Workflow §2-3 and OPS-0007 §5
  item 4. This package's own holdings reference point is the snapshot
  already on file, not a live re-sync.

## Mandatory provisional metadata

- **Creation date:** 2026-07-26.
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
  four of the ten PROVISIONAL records are less than 48 hours old at creation
  and their evidence is comparatively less battle-tested than the ACCEPTED
  tier's).
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

## Next step

Independent ChatGPT (or any other eligible reviewer under `OPS-0007` §1)
review of this preliminary architecture and target-scenario package, anchored
to its exact PR head. This package's own PR remains in draft and unmerged
throughout. No Monday live allocation check has been run or is authorized to
run by this package alone — that remains OPS-0007 §5's own later, separate,
bounded authorization.
