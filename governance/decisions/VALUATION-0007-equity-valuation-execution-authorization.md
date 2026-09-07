---
decision_id: VALUATION-0007
date: 2026-08-09
status: Proposed
category: valuation_execution_authorization
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0002, XASSET-0005, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, VALUATION-0005, VALUATION-0006, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/VALUATION-0007-equity-valuation-execution-authorization.md
---

## Context

### Authority for this unit

`VALUATION-0006` §T states four distinct closure states for the Stage-4 valuation domain and reaches
only the first: (1) methodology-application policy and result architecture governed; (2) result
schema/validator/test implementation merged; (3) discount-rate-evidence population and any other
real-company evidence-population extension a future execution unit finds it needs; (4) real-company
valuation execution authorized, "requiring states 2 and 3 for the company/family in question, plus
`VALUATION-0002` §6.3(a)/(c)/(d), plus its own independent review and principal acceptance before any
output is produced." `VALUATION-0006` §T names this filing by its provisional identifier verbatim:
"a separate future decision — provisionally identified as `VALUATION-0007`, or whichever
`VALUATION-####` identifier is next unused at the time it is actually filed — must authorize the
real-company execution population after this decision (`VALUATION-0006`) is merged and independently
accepted, and after state 2 (schema/validator/test implementation) is itself merged and independently
accepted." Both conditions are independently reconfirmed satisfied below (Preflight). This filing is
that separate, later, explicitly authorized execution-authorization unit — for the authorization step
only. **It does not itself populate a single real-company result record, and it does not itself reach
`VALUATION-0002` §6.3(d)'s "independent review and principal acceptance before any output is
produced" for any company — that review/acceptance step belongs to the future execution
implementation this filing authorizes, not to this filing.**

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-0007-authorization-4ukhkj` confirmed identical to `origin/main` at
  `3efc055882ae38ad68283d7ad1c2a63c6bbb82c7` (the merge commit of PR #289, the `VALUATION-0006`-authorized
  Stage-4 result-scaffold implementation), zero divergence, working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit — no competing active
  mutation lane.
- **PR #289 (`VALUATION-0006`-authorized Stage-4 result-scaffold implementation) independently
  reconfirmed merged**, full lifecycle re-verified from the GitHub API, not taken on any prior summary's
  word — see §M below for the complete, independently-reconstructed record, including two resolved
  bounded-correction rounds (both narrowing validator over-blocking/under-coverage defects the
  independent reviews found in `_domains_bearing_on_family`/`_FAMILY_RELEVANT_ITEM_CATEGORIES`; zero
  sealed record affected, since zero sealed records existed at either correction).
- **`VALUATION-0006` read in full this session** — its seventeen governed conventions (§C), discount-rate
  policy (§D), terminal-growth discipline (§E), peer-selection discipline (§F), scenario-probability
  discipline (§G), predictive-research boundary (§H), evidence-quality treatment (§I), sensitivity/
  conflict/abstention rules (§J), result schema (§K), validator contract (§L), archetype/methodology
  compatibility enforcement (§M), execution-batching evaluation (§N, "evaluated, not authorized"),
  blindness/isolation decision (§O), and disclosed segment/SOTP non-blocking finding (§P) are all bound
  **by reference** below, not redesigned or restated in full.
- **`VALUATION-0002` §2's per-family governed-role table read in full and independently cross-checked
  against `valuation_result_validator.py`'s own live `_GOVERNED_ROLE_TABLE` constant** — byte-for-byte
  match for every one of the 7×7 = 49 cells, confirmed by direct source inspection (§E below).
- **`valuation_archetype_validator.py`, `valuation_evidence_validator.py`, and
  `valuation_result_validator.py` (all three, in full) read this session** — the shared
  `canonical_record_hash()` pattern, the closed-schema/extra-key-rejection discipline, the
  `_FAMILY_REQUIRED_EVIDENCE_DOMAINS`/`_FAMILY_RELEVANT_ITEM_CATEGORIES`/`_domains_bearing_on_family`
  conflict-propagation design (including both PR #289 bounded corrections), and the `result_status`
  triggering logic (`_validate_result_status`, requiring at least one family whose `governed_role` is
  `primary_candidate` or `secondary_corroborative` — never `adjustment_required` — to reach `completed`)
  are all independently traced and bound by reference below (§E–§G). Neither `valuation_result_validator.py`
  nor its two upstream validators imports `allocate.py` or `margin_state.py` in either direction —
  independently reconfirmed.
- **`intelligence/valuation_archetype/` independently re-derived and inspected this session, not
  assumed from any prior filing's own summary**: 27 sealed records plus `COHORT_MANIFEST.yaml`. Primary
  archetype distribution independently recomputed from the live files: **A:6 (ISRG, LLY, META, NVDA,
  PANW, SNPS) · B:6 (ASML, CEG, GEV, PWR, TSM, WM) · C:2 (ICE, V) · D:2 (GNRC, KLAC) · E:1 (RKLB) · F:8
  (AMZN, AVGO, ETN, GOOGL, MSFT, RTX, SPGI, TSLA) · G:2 (COST, TMO)** — exact match to `VALUATION-0006`
  §N's own independently re-derived distribution, zero drift.
- **`intelligence/valuation_evidence/` independently re-derived and inspected this session**: 27 sealed
  records plus `COHORT_MANIFEST.yaml`. `discount_rate_evidence` independently reconfirmed abstained
  (non-empty `abstention_reason`, no populated components) on all 27 of 27 records — zero exception.
  Specific, individually-inspected evidence gaps this session (§F below): ETN's `segment_evidence` carries
  a domain-level `abstention_reason` ("Only Q4 2025 quarterly segment figures were located... a full-year
  segment revenue/operating-profit table was not retrieved"); TSM's `peer_set_evidence` carries exactly one
  `included` candidate (ASML), independently re-read as a value-chain-supplier comparability rationale, not
  a competitive/valuation comparable; PWR's `financial_evidence` carries one `disclosed_conflicts` entry on
  a line item with `item_category: earnings` (two irreconcilable FY2025 diluted-EPS figures, $6.80 vs.
  $6.91); GNRC/KLAC/RKLB's `scenario_evidence` each carry named scenarios with zero populated
  `probability_weight` values anywhere.
- **`targets.yaml` independently re-derived this session, not assumed from the archetype directory
  listing**: `[row['ticker'] for row in destination if row['asset_class'] == 'equity']`, sorted, produces
  exactly the same 27-name list the archetype and evidence directories carry — `AMZN, ASML, AVGO, CEG,
  COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI,
  TMO, TSLA, TSM, V, WM` — cross-validated three independent ways (targets.yaml, the sealed archetype
  cohort, the sealed evidence cohort), zero discrepancy.
- **`TIER-0009` §K read and independently reconfirmed unedited** — still the controlling statement that
  no valuation framework exists in production and that `target_and_range`/`maximum_position_size` stay
  doctrinally forced to `valuation_required` pending a future, separately accepted governance decision
  this filing does not attempt to be.
- **`NUM-0001` and `governance/decisions/README.md` read and reconfirmed this session** — this filing
  introduces zero new numeric parameters of any kind (every convention it operates under was already
  classified by `VALUATION-0006` §C); the category-minting discipline (`governance/decisions/README.md`,
  the `TIER-0001`/`VALUATION-0002`/`VALUATION-0004`/`VALUATION-0005` precedent) is applied below (§O).
- **`OPS-0007` §1 and `OPS-0009` read and reconfirmed this session** — the twelve-point capability-based
  independent-review standard and Lane G's "always full weight, never reduced" rule bind this filing
  exactly as they bound every prior `VALUATION-####` filing.
- **`OPS-0008`'s Research Wave Protocol reviewed for applicability** — this filing is execution-batching
  design over an already-fully-sealed, already-fully-evidenced 27-name cohort (no first-coverage research
  risk of the kind `OPS-0008` governs), matching `VALUATION-0003` §G's and `VALUATION-0005` §K's own
  identical reasoning for why their comparable-scale content-population work used internally sharded batch
  cycles rather than `OPS-0008`'s research-wave apparatus.
- **Decision catalog independently rebuilt before this filing's own new entry**: 103 decisions, 0 issues.
- **`test_portfolio_hq_dashboard_decisions.py` independently inspected**: two hardcoded assertions
  currently assert `== 103`; both require bumping to `104` (§O below).
- **Full repository `pytest` baseline independently reproduced before any edit**: 4215 passed, 0 failed,
  1 pre-existing unrelated `DeprecationWarning`.
- **`valuation_result_validator.py` run standalone before any edit**: `OK (0 result(s))`. `intelligence/
  valuation_results/` independently confirmed absent from the repository at this commit.

## Decision

**This decision authorizes exactly one future, separate, bounded implementation PR to populate real
`intelligence/valuation_results/<TICKER>.yaml` records for the 27-name canonical equity cohort already
sealed under `valuation_archetype`/`valuation_evidence`, applying `VALUATION-0006`'s already-governed
methodology-application policy and result schema. It does not itself value any company, does not itself
compute a fair value, price target, expected return, discount rate, WACC, beta, ERP, terminal growth
rate, applied peer set, or scenario probability for any real company, and does not itself create,
populate, review, or accept a single result record. Real-company execution begins only in a future,
separately reviewed implementation PR, not in this session.**

### A. What is authorized

One future, separate, bounded implementation PR that:

1. Populates `intelligence/valuation_results/<TICKER>.yaml` for the 27-name cohort in §B, applying
   `VALUATION-0006` §§C–M exactly (bound by reference, not redesigned) — every governed convention, the
   result schema, the validator's existing compatibility/conflict/abstention enforcement, and the
   targeted isolation rule (§O below, restated from `VALUATION-0006` §O).
2. Is internally organized into the four method-homogeneous execution batches `VALUATION-0006` §N
   evaluated and this filing now adopts (§G below) — one primary authoring session per batch mutating
   the repository, internally sharded for drafting efficiency, matching `VALUATION-0003` §G's and
   `VALUATION-0005` §K's own established shard-review architecture — packaged as **one** implementation
   PR covering all four batches (§G's own reasoning), not four separate PRs.
3. Uses the already-merged `valuation_result_validator.py` as-is — this filing authorizes **no** change
   to that validator's schema, closed-key sets, compatibility table, or free-text scan design. If the
   future implementation session discovers a genuine defect in the validator while populating real
   records (as PR #289's own two bounded corrections discovered while building the scaffold against
   synthetic fixtures), it must disclose that finding and, if a fix is warranted, treat it as its own
   bounded correction within that implementation PR's own review cycle — not as license to redesign the
   schema or the governed conventions this filing and `VALUATION-0006` both bind.
4. Produces, for every one of the 27 tickers, exactly one of the three `result_status` values already
   governed by `VALUATION-0006` §J: `completed`, `partial`, or `unable_to_determine` — **never a promise,
   implicit or explicit, that every ticker reaches `completed`** (§F/§H below).
5. Requires its own full independent-review/correction/re-review/principal-acceptance/merge/
   post-merge-verification lifecycle under `OPS-0007` §1 / `OPS-0009` Lane G before any populated record
   is authoritative.

**Nothing in §§B–L below is itself a populated record.** This filing specifies the bounded population
scope and disclosed constraints a future implementation must operate within — it performs none of that
population itself.

### B. Exact cohort — the bounded first equity-valuation execution population

Independently re-derived this session from live `targets.yaml` (Preflight), cross-validated against the
sealed `valuation_archetype` and `valuation_evidence` cohorts (identical population, zero drift):

`AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR,
RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM` — 27 names, zero exclusion, zero addition.

**This authorization is bounded to exactly this population.** It does not extend, automatically or by
implication, to the 26 researched non-canonical Company Intelligence contenders, the broader
`CONTENDER-####` registry (84 entries), any future ETF/QQQ candidate, or any name added to `targets.yaml`
after this filing — a future roster addition requires its own separate archetype assignment, evidence
population, and execution authorization, following this program's own established first-coverage
discipline (`PI-0003`/`PI-0005`/`PI-0007`/`VALUATION-0003`'s own identical population-boundary language).

### C. Archetype distribution and batch composition — re-derived, not assumed

Independently recomputed this session directly from the sealed `intelligence/valuation_archetype/*.yaml`
records (Preflight): **A:6 · B:6 · C:2 · D:2 · E:1 · F:8 · G:2** — exact match to `VALUATION-0006` §N's
own corrected distribution.

Per `VALUATION-0006` §N's recommended (there, not-yet-authorized) method-homogeneous batching, now
**adopted** by this filing with exact per-ticker membership (§G below resolves why this shape, not a
27-name cycle or per-archetype/per-ticker fragmentation, is authorized):

| Batch | Archetypes | Primary family | Tickers (8/8/8/3 = 27) |
|---|---|---|---|
| 1 — DCF/compounder | A + G | Families 2/3 (FCFF/FCFE DCF) | ISRG, LLY, META, NVDA, PANW, SNPS, COST, TMO |
| 2 — SOTP/diversified | F | Family 1 (Asset-based/SOTP) | AMZN, AVGO, ETN, GOOGL, MSFT, RTX, SPGI, TSLA |
| 3 — Relative-valuation/adjustment | B + C | Family 5 (B); no Primary for C | ASML, CEG, GEV, PWR, TSM, WM, ICE, V |
| 4 — Scenario/cyclical-binary | D + E | Family 7 (Scenario) | GNRC, KLAC, RKLB |

Batch labels name the archetype's own **Primary** family per `VALUATION-0002` §2's table (§E below) —
they are drafting/review-organization labels only, never a promise that the named family is the only
family a ticker's result may apply, nor that it will reach `completed` (§F/§H).

### D. Stage-4 closure-state resolution — state 3 is company/family-specific, never a blanket 27-ticker
prerequisite

`VALUATION-0006` §T's state 4 requires states 2 and 3 "for the company/family in question" — a
deliberately narrow, per-pairing formulation, not "state 3 must be satisfied for every evidence domain,
for every company, before any execution may begin." This filing resolves what that means mechanically,
using the already-sealed Stage-3 evidence and the already-merged validator's own required-domain mapping
(`_FAMILY_REQUIRED_EVIDENCE_DOMAINS`, independently traced this session):

1. **State 2 is satisfied** — PR #289 merged (§M), `valuation_result_validator.py`/
   `test_valuation_result_validator.py` exist and run clean.
2. **State 3 is satisfied today for families 1, 4, 5, 6, and 7** — every evidence domain those families
   require (`financial_evidence`, `segment_evidence`, `peer_set_evidence`, `scenario_evidence`) is already
   populated by the sealed Stage-3 corpus (PR #283). "Satisfied" here means the evidence **exists and is
   readable** — it does not mean every company/family pairing's evidence is *sufficient* for a `completed`
   result; sufficiency is an honest, per-pairing, execution-time determination (§F/§H), never predicted or
   guaranteed by this filing.
3. **State 3 is NOT satisfied today for families 2 and 3** — both require `discount_rate_evidence`
   (`_FAMILY_REQUIRED_EVIDENCE_DOMAINS`), independently reconfirmed abstained on all 27 of 27 sealed
   records (Preflight). This is the one universal, currently-open state-3 gap this filing identifies. It
   is not closed by this filing, and this filing does not authorize a future execution unit to close it —
   discount-rate-evidence population, if ever pursued, is its own further, separately authorized,
   evidence-population extension (`VALUATION-0004`'s domain, not this filing's), not folded into the
   execution authorization granted here.
4. **A future execution unit does not need to separately request a "state-3 extension" merely to attempt
   family 1, 4, 5, 6, or 7 for any of the 27 tickers** — the evidence prerequisite for those families is
   already met at the population level. It needs a state-3 extension only for family 2/3 (discount-rate
   evidence), which this filing does not authorize requesting or performing.
5. **Consequence for the batching in §C**: Batch 1's own two named "Primary" families (2 and 3) are
   structurally blocked from `completed` for every one of its 8 tickers by item 3 above — but this does
   **not** mean Batch 1 tickers are blocked from `completed` altogether. Six of the eight (the A-archetype
   tickers: ISRG, LLY, META, NVDA, PANW, SNPS) also carry family 5 (relative valuation) as an
   **independent Primary candidate** per `VALUATION-0002` §2's own table (§E), not gated on discount-rate
   evidence — only on peer-set sufficiency. The two G-archetype tickers (COST, TMO) carry families 4, 5,
   and 6 as Secondary/corroborative alternatives, any one of which, if clean, can independently support a
   company-level `completed` result under `VALUATION-0006` §J's own definition ("at least one methodology
   family whose governed role... is Primary candidate or Secondary/corroborative... reached a populated
   range... Other applied families may remain partial or unapplied without preventing an overall completed
   status"). **This filing does not predict which of the 27 tickers will actually reach `completed`** —
   it only establishes that the discount-rate gap alone does not doctrinally foreclose Batch 1's own
   company-level outcomes, given the alternative families each archetype's own governed-role table already
   makes available.

### E. Family/methodology readiness boundary — bound by reference to `VALUATION-0002` §2, independently
re-verified against the live validator, not redesigned

`VALUATION-0002` §2's per-family governed-role table (bound by reference, quoted below only to ground
§C/§D/§F, not restated as new authority) and `valuation_result_validator.py`'s own live
`_GOVERNED_ROLE_TABLE` constant are independently confirmed, this session, to match cell-for-cell across
all 7 families × 7 archetypes = 49 cells:

| Family | Primary | Secondary | Adjustment-required | Prohibited |
|---|---|---|---|---|
| 1 — Asset-based/SOTP | F | — | B, C, D, E | A, G |
| 2 — FCFF DCF | A, G | — | B, D, F | C, E |
| 3 — FCFE DCF | A, G | — | B, C, D, F | E |
| 4 — Earnings/FCF-yield | — | G | A, B, C, D, F | E |
| 5 — Relative valuation | A, B | G | C, D, E, F | — |
| 6 — ROIC/reinvestment | — | B, G | A, C, D, F | E |
| 7 — Scenario/probability-weighted | D, E | — | A, B, C, F, G | — |

This filing designs, redefines, or re-derives none of this table — it is `VALUATION-0002` §2's own
already-accepted mapping, cited here only so a future execution session and its independent reviewer do
not have to reconstruct it from the underlying report. **A family whose governed role for a ticker's own
sealed `primary_archetype` is Prohibited or Insufficient basis for adoption may never appear in that
ticker's `methodology_families_applied` — mechanically enforced by the already-merged validator (§M),
never merely discouraged by prose.**

### F. Known cohort limitations — disclosed constraints on the existing evidence base, not defects this
filing authorizes "fixing"

The following are **facts about the current sealed cohort**, independently verified this session against
live data (Preflight), that a future execution session must work within honestly — never silently routed
around, never treated as license to invent missing evidence, and never grounds for a promised `completed`
outcome this filing does not make:

1. **Universal discount-rate gap (families 2/3, all 27 tickers).** §D item 3. DCF-family output for any
   ticker is structurally forced to `partial`/`unable_to_determine` for that family specifically, until a
   separately authorized evidence-population extension closes the gap.
2. **Terminal-growth/discount-rate numeric-unit convention — a second, independent, currently-dormant gap
   layered on top of item 1.** `valuation_result_validator.py`'s own `_check_terminal_growth_hard_rule`
   docstring (added by PR #289's own bounded correction, review 4892431010 MINOR-3) discloses, verbatim,
   that no merged authority defines whether `terminal_growth` and `applicable_discount_rate` share a
   common numeric-unit convention (e.g., both decimal fractions such as `0.02` for "2%") — the comparison
   "has no way to detect a unit mismatch... and would either incorrectly reject a validly-paired assumption
   or incorrectly accept an invalidly-paired one." Because item 1 already forces every family-2/3 output to
   `partial`/`unable_to_determine` for all 27 tickers today, this second gap is presently **dormant** — it
   cannot be exercised while discount-rate evidence itself is universally absent. **This filing does not
   invent a unit convention.** It instead binds the future implementation: no real family-2/3 execution
   that would populate a paired `terminal_growth`/`applicable_discount_rate` `assumptions_ledger` entry
   requiring the validator's strict `g < r` comparison may proceed until either (a) a future, separately
   governed decision settles the unit convention, or (b) the values are represented under a convention
   already clearly authorized by existing text (none is identified today). Non-DCF families (1, 4, 5, 6, 7)
   are entirely unaffected by this gap and may proceed independently under this authorization.
3. **ETN — segment-evidence abstention blocks its own SOTP-primary path from `completed`.** ETN's
   `segment_evidence` carries a domain-level `abstention_reason` (only Q4 2025 quarterly figures were
   located; no full-year segment table). Per `VALUATION-0006` §I ("where a Stage-3... domain-level
   abstention bears materially on an applied family's own required inputs, that family may not reach
   `completed`"), independently confirmed mechanically enforced by `_domains_bearing_on_family`, family 1
   — F's **only** Primary-or-Secondary-eligible family under §E's table — cannot reach `completed` for
   ETN under current evidence. Since archetype F carries no Secondary alternative (every other family is
   Adjustment-required for F), ETN's company-level result is structurally constrained to `partial` or
   `unable_to_determine` unless and until additional segment evidence is separately populated — this
   filing does not authorize that population.
4. **TSM — thin peer-candidate set constrains, but does not foreclose, family 5.** TSM's
   `peer_set_evidence` carries exactly one `included` candidate (ASML), independently re-read this session
   as a value-chain-supplier relationship, not a competitive/valuation comparable — the exact real finding
   `VALUATION-0006` §F cites as the direct motivation for the two-peer minimum (item 11). Family 5 (TSM's
   Primary family under archetype B) may therefore be reported only as a disclosed corroborative data
   point inside a `partial` result, never as sole support for `completed`, per that mechanically-enforced
   rule. **TSM is not thereby foreclosed from `completed`** — family 6 (ROIC/reinvestment), Secondary for
   archetype B, requires no peer evidence at all and is not affected by the peer-thinness finding; whether
   TSM's `financial_evidence` is otherwise sufficient for a clean family-6 result is an execution-time
   determination this filing does not make or predict.
5. **PWR — a disclosed earnings conflict bears mechanically on its Primary family, but not its Secondary
   one.** PWR's `financial_evidence` carries one `disclosed_conflicts` entry on an `item_category:
   "earnings"` line item (two irreconcilable FY2025 diluted-EPS figures). Independently traced through
   `valuation_result_validator.py`'s own `_FAMILY_RELEVANT_ITEM_CATEGORIES` mapping this session: `earnings`
   is a relevant category for family 5 (PWR's own Primary family under archetype B) — so family 5 may not
   reach `completed` for PWR while that conflict stands, per §I's rule. `earnings` is **not** a relevant
   category for family 6 (Secondary for B) — the conflict does not mechanically bear on that family, so a
   PWR family-6 result is not blocked by this specific conflict (though it remains subject to its own,
   independently-evaluated evidence sufficiency). This is a demonstrated, code-verified example of the
   item-category-scoped conflict-propagation design PR #289's own bounded correction built — not a
   hypothetical.
6. **ICE, V (archetype C) — structurally capped at `partial`, by doctrine, not by an evidence gap.**
   Independently re-verified against §E's table: for archetype C, family 2 is Prohibited and every one of
   the remaining six families (1, 3, 4, 5, 6, 7) is Adjustment-required — **zero families reach Primary or
   Secondary/corroborative for archetype C anywhere in the governed table.** `VALUATION-0006` §J's
   `completed` bar requires at least one Primary-or-Secondary family; ICE and V therefore cannot reach
   `completed` under the current, already-accepted doctrine, **regardless of how strong their evidence
   is**. This is not a defect this filing authorizes correcting — `VALUATION-0002` §2 itself already
   anticipated exactly this outcome for financial-intermediation archetypes and did not invent a Primary
   family that the underlying report's own literature review does not support. A future execution session
   must report ICE and V as `partial` (or `unable_to_determine`, if even an Adjustment-required family
   cannot produce a clean disclosed range), never force a `completed` status by mischaracterizing an
   Adjustment-required family's governed role.
7. **GNRC, KLAC, RKLB (archetypes D/E) — evidence exists, but probability assignment is an unresolved
   execution-time judgment.** All three carry named scenarios in `scenario_evidence` with zero populated
   `probability_weight` values (Preflight). Family 7 (Primary for both D and E) does not depend on
   discount-rate evidence and is not blocked by any disclosed conflict in the current corpus for these
   three tickers — but assigning a real probability weight to a named scenario is itself a governed,
   execution-time policy judgment (`VALUATION-0006` §G), subject to the targeted isolation rule (§I below).
   This batch's own evidence base is, on the facts independently verified this session, the least
   constrained of the four — but this filing does not predict a `completed` outcome for any of the three.

**These seven items are the specific, individually-verified gaps this session found. They are not
represented as exhaustive of every possible evidence limitation across all 27 records and all seven
families** — a future execution session must independently re-inspect the live evidence for each
ticker/family pairing it actually attempts, at execution time, and disclose honestly whatever it finds,
using `partial`/`unable_to_determine` as the legitimate, expected outcome wherever evidence does not
support `completed`'s own bar.

### G. Implementation packaging — one PR, four internally-sharded batches, adopted from `VALUATION-0006`
§N's evaluation

`VALUATION-0006` §N evaluated four packaging options and recommended, without authorizing, the
method-homogeneous four-batch shape in §C. This filing adopts that recommendation as binding, for the
same reasons §N already gave (restated only in summary, not re-derived): a single 27-name cycle collapses
five structurally different judgment/failure modes into one review unit; per-archetype fragmentation
(seven batches) produces two under-sized 1–2-ticker units with no coherence benefit; per-ticker execution
(27 PRs) multiplies governance overhead 27-fold with no corresponding review-quality gain, directly
contrary to `OPS-0008`'s own rejection of exactly that overhead pattern.

**This filing packages the four batches as one implementation PR**, not four separate PRs, because: (1)
all four batches share the identical, already-merged result schema and validator — there is no
schema/validator boundary a PR split would meaningfully separate; (2) the 27-name population is itself one
closed, already-bounded cohort (§B) — splitting it across PRs would not narrow authority, only add review
overhead; (3) internal batch sharding (one primary authoring session per batch, drafting in parallel or in
sequence at the implementing session's own discretion) already preserves the per-batch review-quality
benefit §N's own reasoning is built on, without paying a second governance cycle per batch; (4) this
mirrors `VALUATION-0003` §G's own established precedent exactly — that filing's 27-name archetype-
assignment implementation used five internal shards inside **one** implementation PR, not five. A future
implementation session remains free to split into more than one PR if it finds, in practice, that
combining all four batches into a single review unit is unwieldy — but that is a judgment for that
session's own PR, not a fragmentation this filing pre-authorizes or requires.

**No per-ticker PR fragmentation is authorized.**

### H. Result-status/abstention contract — restated, not redesigned

Bound by reference to `VALUATION-0006` §J/§K/§L, mechanically enforced by the already-merged
`valuation_result_validator.py` (§M): `completed`, `partial`, and `unable_to_determine` are the closed,
exhaustive `result_status` vocabulary. **`completed` is never an objective requirement for every ticker in
the 27-name cohort** — §F above already identifies at least two tickers (ICE, V) doctrinally incapable of
reaching it under the current governed-role table, and at least two more (ETN, TSM) whose current evidence
base constrains their own Primary path specifically. `partial` and `unable_to_determine` are legitimate,
fully governed outputs, not failure states requiring correction. Absence of sufficient evidence must never
be papered over by an invented assumption, a fabricated peer, an invented scenario, or a forced family
application the validator's own compatibility check would otherwise reject. A ticker's company-level
`result_status` may be `completed` on the strength of one clean qualifying family while other applied
families for the same ticker remain `partial` or unapplied (§D item 5) — `VALUATION-0006` §J's own
definition, restated, not amended. No family may bypass `valuation_result_validator.py`'s own evidence,
conflict, compatibility, or terminal-growth checks under any circumstance; this filing grants no exception
to any of them.

The disclosed family-level/record-level `partial`-shape distinction PR #289's own scaffold already
supports (`family_status` distinct from record-level `result_status`) is not redesigned or amended by this
filing — a future implementation applies it exactly as the merged validator already enforces it.

### I. Targeted isolation — restated from `VALUATION-0006` §O, not redesigned or widened

Bound by reference, restated only in summary: the future execution session must apply `VALUATION-0006`
§O's targeted isolation rule for exactly three sub-judgments and no others — (a) applied-peer-set
selection (§F above, e.g. TSM's peer-exclusion/inclusion decisions), (b) scenario-probability assignment
(§F item 7 above, e.g. GNRC/KLAC/RKLB), and (c) terminal-growth-rate selection within the disclosed softer
ceiling (dormant today per §F item 2). While making any of these three specific calls, the session must
not have `portfolio_role_ref`, `conviction.rating`, `target_pct` or any other current allocation/
target-weight figure, current holding status or size, `intelligence/recommendations/` (Milestone 8)
disposition, or `gates.yaml` status open, cited, or referenced — and the written rationale must
independently justify the choice from Stage-3/Stage-2 evidence and market/peer/discount-rate facts alone,
mechanically scannable per §L's free-text-scan discipline. **No full Milestone-6-style blind-drafting/
sanitizer architecture is required or authorized for this population** — `VALUATION-0006` §O's own
analysis (Stage-4 inputs are already-sealed, already-redacted-of-policy evidence plus external market
data, materially unlike archetype assignment's own single-anchor vulnerability) is independently
reconfirmed sound by this filing and is not reopened. Underlying Stage-2/Stage-3 economic evidence remains
fully visible throughout every judgment, including the three isolated ones — the isolation rule blinds a
session to portfolio-policy anchors specifically, never to the economic evidence its own judgment must be
grounded in.

### J. Zero automatic portfolio authority — restated, exhaustive

**A populated valuation-result record, however complete, creates zero allocation, target, tier, cap,
cluster, gate, or trade authority on its own.** The governed flow is, and remains, exactly:

real valuation results (this filing's future implementation)
→ independent review + principal acceptance (that implementation's own required lifecycle)
→ a future, separate, still-unauthorized recommendation/adoption decision reviewing the results
→ a future, separate, still-unauthorized cross-asset synthesis/sizing decision
→ a future, separate, still-unauthorized execution-planning decision.

**Never**: valuation result → automatic target/trade. This filing authorizes no `TIER-0009` §K
resolution (§K below), no target/range change, no maximum-position-size change, no tier change, no
holding inclusion/removal, no gate change, no allocator change, no capital-priority change, no sleeve
sizing, no cross-asset rank, no buy/sell/add/hold/trim/exit recommendation, no margin deployment, no
ladder creation, no chart-informed execution, and no trade of any kind — by this filing, or by the future
implementation it authorizes.

### K. `TIER-0009` §K — restated, not resolved

Even a fully populated, independently reviewed, and principal-accepted set of real-company valuation
results does not automatically resolve `TIER-0009` §K's `valuation_required` status for
`target_and_range`/`maximum_position_size` on any of the 27 equities. A later, separate recommendation/
adoption decision must review the results and explicitly determine whether, and how, they revise those two
fields — following the same bounded-charter, "define, then implement, then execute, then adopt" discipline
this program has applied at every prior layer. This filing does not perform, begin, or imply that
recommendation/adoption decision.

### L. Non-canonical / whole-universe boundary — restated

The 27-name cohort in §B is a bounded first equity-valuation execution population, not Portfolio-HQ's
final security selection, and this filing draws no incumbent-bias inference from it. Explicitly, still
outside this filing's scope: the 19 evidence-ready non-canonical equities and 7 freshness-review equities
`WS-0014`'s own contender registry names; `CONTENDER-0003` or any further contender-registry work; any
broader ETF/QQQ candidate beyond the four already-classified funds; ETF, cryptocurrency, GLD, cash/reserve,
and debt-reduction economic-assessment methodology (`WS-0014`/`XASSET-0001` §C/§D, unaffected); the
overlap-concentration model (`XASSET-0005`/`XASSET-0007`, unaffected); cross-asset opportunity-cost
synthesis; Level 1/Level 2 sleeve/instrument sizing; chart evidence of any kind (`CHART-0001`/`CHART-0002`,
unaffected); buy-ladder/deployment integration (`LADDER-0001`, unaffected); unlevered-versus-levered
testing; margin/leverage-policy review; monitoring/sell discipline; and final portfolio integration/audit.

### M. Lane M — PR #289 (`VALUATION-0006`-authorized Stage-4 result-scaffold implementation) lifecycle,
independently re-verified and recorded

Independently re-verified via the GitHub API this session, not assumed:

- PR #289, base `main` @ `03dc2a044390a4944257f4027a480ef955b3a6d7`, accepted head
  `af0e8fa67e5d204dc50da1d7bd11d4c57290c474`.
- Review chain: `pullrequestreview-4892431010` (first review — CHANGES REQUIRED, findings including the
  `_domains_bearing_on_family` MAJOR-2 over-blocking defect and the terminal-growth unit-convention
  MINOR-3 disclosure), resolved by a bounded correction (`_ITEM_CATEGORY_SCOPED_CONFLICT_DOMAINS`/
  `_FAMILY_RELEVANT_ITEM_CATEGORIES` narrowing, independently traced this session at §F item 5 above);
  `pullrequestreview-4892545747` (delta review — a further MINOR under-inclusion gap in the item-category
  mapping, seven of 21 governed categories left unreachable by any family), resolved by a second bounded
  correction extending the mapping with each addition traced to specific `PROTOCOL_V1.md` §4 language;
  `pullrequestreview-4892667088` (final delta review). **Zero sealed `intelligence/valuation_results/`
  record existed at either correction** — both corrections touched only `valuation_result_validator.py`'s
  own internal mapping constants and their test coverage, never a populated record, since none existed.
- Principal acceptance: `issuecomment-5234132129`, at the accepted head.
- Exact-head CI: run `31336183418`, job `93302308154`, `status: completed`/`conclusion: success`.
- Merge: `3efc055882ae38ad68283d7ad1c2a63c6bbb82c7`, parents `03dc2a044390a4944257f4027a480ef955b3a6d7`
  and `af0e8fa67e5d204dc50da1d7bd11d4c57290c474` (independently re-confirmed via `git log --pretty`).
- Merge-commit CI: run `31339074586`, job `93309736882`, `status: completed`/`conclusion: success`.
- **Post-merge validation independently reproduced this session**: `valuation_result_validator.py` →
  `OK (0 result(s))`; standalone-module run confirms `intelligence/valuation_results/` still absent;
  `test_valuation_result_validator.py` → 173 focused tests, all passing (up from PR #289's own originally
  reported 110, reflecting the tests both bounded corrections added); full repository `pytest` → 4215
  passed, 0 failed; decision catalog → 103 decisions, 0 issues; all twelve pre-existing repository
  validators clean and unaffected (`classification_validator` 28, `reconciliation_validator` 27,
  `recommendation_validator` 27, `relationship_validator` 13, `intelligence_validator` clean,
  `freshness_validator` OK, `contender_registry_validator` 84, `etf_classification_validator` 5,
  `crypto_classification_validator` 4, `valuation_archetype_validator` 28, `valuation_evidence_validator`
  28, `functional_doctrine_validator` 5).

### N. Register synchronization (Lane M, this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives, additive only — no existing gate's own text
edited:

1. A new `valuation0006-stage4-result-scaffold-implementation-post-merge-verification` gate recording
   §M's independently reconfirmed PR #289 facts in full, including both bounded-correction rounds and the
   corrected final test count (173) — this corrects the drafting-session's own necessarily-incomplete,
   in-progress description without editing the existing
   `valuation0006-stage4-result-scaffold-implementation` gate's own text.
2. A new `valuation0007-equity-valuation-execution-authorization` gate (`status: in_progress`, `pr: null`
   — this filing does not mark its own unmerged work complete, matching every prior filing's identical
   self-reference discipline in this repository).
3. `status` remains `proposed`. `priority` remains `secondary`. `dependencies` remains `[]`.
4. `active_branch`, `active_pr`, `last_verified_main_sha`, `last_verified_date`, `blocker`, `next_action`,
   `completion_criteria`, and `authorized_by` updated to this filing's own live state.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### O. Non-authority — explicit, exhaustive

This decision authorizes no:

- Fair value, price target, expected return, or upside/downside calculation for any real company.
- Actual DCF computation, actual peer selection applied to a computation, actual discount-rate value,
  actual WACC, actual beta, actual ERP value, actual terminal growth rate, or actual scenario probability
  for any real company.
- Real-company valuation-result **population** of any kind, in this session — that population is what a
  future, separate implementation PR performs, gated on its own full independent-review/correction/
  re-review/principal-acceptance/merge/post-merge-verification lifecycle.
- Any `valuation_result_validator.py` schema, closed-key set, compatibility-table, or free-text-scan
  redesign (§A item 3).
- Discount-rate-evidence population for any real company (§D item 3/§F item 1's disclosed gap remains
  unclosed by this filing).
- Any settling of the terminal-growth/discount-rate numeric-unit convention (§F item 2's disclosed gap
  remains unclosed and dormant).
- Resolution, closure, or narrowing of `TIER-0009` §K's `valuation_required` status on any equity (§K).
- Any amendment to `VALUATION-0004`/`VALUATION-0005`'s Stage-3 evidence schema or `VALUATION-0006`'s
  Stage-4 result schema.
- Target, tier, holdings, gate, capital-priority, cap, cluster, or allocator change of any kind.
- Margin policy, buy-ladder, chart ingestion, or chart interpretation of any kind.
- `CONTENDER-0003` or any further contender-registry regeneration/legacy-recovery work.
- Any ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content.
- Any overlap/concentration modeling, cross-asset synthesis, or unlevered-versus-levered allocation
  testing.
- Any order or trade.
- Any historical backtest of a discount rate, terminal-growth assumption, peer multiple, or scenario
  probability against subsequent stock-price performance, under any framing (`VALUATION-0006` §H, restated
  not reopened).
- Any edit to `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
  or `VALUATION-0001` through `VALUATION-0006`.

**Category note**: `valuation_execution_authorization` is a new category, distinct from
`VALUATION-0006`'s `valuation_application_governance`, `VALUATION-0005`'s
`valuation_evidence_population_authorization`, `VALUATION-0004`'s `valuation_evidence_governance`, and
`VALUATION-0003`'s `valuation_archetype_governance` — the same "structurally distinct governance act, new
category" precedent `TIER-0001` established, and the exact model `VALUATION-0005`'s own Rationale applied
one layer earlier for the identical governance-design-versus-population-authorization distinction
(`VALUATION-0004` governs evidence architecture; `VALUATION-0005` authorizes evidence population — a
structurally analogous pair to `VALUATION-0006` governing application policy/result architecture and this
filing authorizing execution population).

### P. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0007-equity-valuation-execution-authorization.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0007`).
3. `operations/WORKSTREAMS.yaml` (§N above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 103 → 104).

**No other file is touched.** No production code, no `intelligence/**` record, no `PROTOCOL_V1.md`,
`METHODOLOGY_EVALUATION_REPORT.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` change, no `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml` change, no `valuation_result_validator.py` change.

### Q. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (`OPS-0009` Lane G — new authorization, full weight, never reduced), complete
any required bounded correction and exact-head re-review, and receive explicit principal acceptance before
it may be marked ready or merged. **This decision does not mark itself ready and does not authorize its own
merge.** No real-company execution implementation PR may open, and §§A–O above are not effective, until
this PR merges to `main`.

## Rationale

**Why authorize execution now, in a dedicated filing separate from `VALUATION-0006`.**
`VALUATION-0002` §6.3's own explicit sequencing (archetype assignment, then RQ4 closure, then evidence
population, then application-policy design, then execution) and `VALUATION-0006` §T's own four-state
staging both require this as its own, later, separate step — collapsing it into `VALUATION-0006` itself
would have violated the sequencing `VALUATION-0006` §T explicitly named this filing to satisfy, and would
have asked one governance PR to carry both "what convention governs" and "is real execution now
authorized," the same combination `VALUATION-0006`'s own Alternatives Considered section already rejected.

**Why resolve `VALUATION-0006` §T's state-3 "for the company/family in question" language explicitly,
rather than leave it to the future implementation to interpret.** A literal, unresolved reading could be
misapplied two ways — either as "state 3 requires every evidence domain fully populated for every ticker
before any execution begins" (which would make this authorization vacuous, since discount-rate evidence is
universally absent) or as "state 3 is automatically satisfied everywhere because *some* evidence exists"
(which would license family 2/3 execution the discount-rate gap should still block). §D's mechanical,
family-by-family resolution — grounded directly in the already-merged validator's own
`_FAMILY_REQUIRED_EVIDENCE_DOMAINS` mapping, not invented — avoids both misreadings and gives the future
implementation session an unambiguous, code-traceable starting point.

**Why disclose seven specific cohort limitations (§F) rather than leave them for the implementation session
to discover independently.** Every one of the seven was independently verified this session against live
data and, in several cases, against the actual validator logic that would enforce or reject a given
output — disclosing them now prevents the future implementation session from re-deriving the same findings
from scratch, and prevents an independent reviewer from having to determine, mid-review, whether a
`partial` result for ICE/V/ETN/TSM reflects a real doctrine/evidence constraint or an implementation
defect. This mirrors `VALUATION-0006` §D's own identical practice of disclosing the discount-rate gap
explicitly "so a future reader does not discover it by surprise mid-execution."

**Why package all four batches as one implementation PR (§G), departing from a literal reading of
`VALUATION-0006` §N's own four-cohort framing as four separate governance/review units.** `VALUATION-0006`
§N evaluated the *batching shape*, not the *PR-packaging* question — nothing in §N requires four separate
PRs, and `VALUATION-0003` §G's own precedent (27-name population, five internal shards, one PR) is directly
on point for a population of this exact scale under one already-fixed schema. Splitting into four
governance-and-review cycles would multiply overhead without narrowing what any single cycle authorizes,
since all four batches share the identical schema, validator, and cohort boundary.

**Why `valuation_execution_authorization`, a new category.** Restated in §O — matches the identical
precedent this program has applied at every prior governance-design-to-population-authorization transition
(`VALUATION-0004`→`VALUATION-0005`; `TIER-0001` itself).

## Alternatives Considered

- **Authorize execution for only the batches with no currently-disclosed evidence limitation (e.g., Batch
  4), deferring the rest.** Rejected — every batch has at least one ticker with a real alternative
  Primary/Secondary family not gated on the disclosed limitation (§D item 5, §F items 4/5), so a
  batch-level exclusion would be both under-inclusive (denying tickers a legitimate `partial`-or-better
  attempt) and would not actually track where the real constraints lie, which are family-specific, not
  batch-specific.
- **Require the future implementation to first close the discount-rate-evidence gap, so all seven families
  are available for every ticker before execution begins.** Rejected — this would fold a Stage-3
  evidence-population extension into a Stage-4 execution authorization, blurring exactly the evidence/
  execution separation `VALUATION-0006` §F/§G were built to preserve, and would delay execution on the six
  non-DCF-dependent families indefinitely for no evidence-quality reason.
- **Invent a terminal-growth/discount-rate numeric-unit convention now, so §F item 2's dormant gap cannot
  ever resurface.** Rejected — no existing repository authority supports a specific convention, and
  `NUM-0001`'s own discipline (already applied at every layer of `VALUATION-0006`) treats an unsupported
  numeric or structural convention invented without evidence as its own defect class; the gap is dormant
  today specifically because item 1 already blocks family 2/3, so there is no live case forcing a decision
  now.
- **Package the four batches as four separate implementation PRs, one per batch, each with its own
  governance-authorization filing.** Rejected — restated in Rationale; would multiply review overhead
  eightfold (four governance cycles plus four implementation cycles) relative to this filing's single
  authorization plus one implementation PR, with no corresponding narrowing of authority or improvement in
  review quality that `VALUATION-0003`'s own comparable-scale precedent didn't already achieve with a
  single PR.
- **Declare ICE/V's archetype-C ceiling and ETN's segment gap "blocking defects" requiring a schema or
  doctrine amendment before execution may proceed.** Rejected — `VALUATION-0002` §2's table already
  anticipated financial-intermediation archetypes reaching no Primary/Secondary family, and `VALUATION-0006`
  §P already found the segment-evidence gap non-blocking at the schema level; treating either as requiring
  a fix here would exceed this filing's own bounded execution-authorization scope and would relitigate
  already-accepted doctrine without new evidence.

## Consequences

**What changes.** A future, separate implementation PR may now be opened to populate real
`intelligence/valuation_results/<TICKER>.yaml` records for the 27-name cohort — but only after this
governance PR itself is independently reviewed and principal-accepted. Once that future implementation
merges (after its own full independent-review/correction/re-review/principal-acceptance/merge/post-merge-
verification lifecycle), `VALUATION-0006`'s methodology-application-policy conventions, result schema, and
validator contract become the binding, exercised specification against real company data for the first
time. `WS-0015`'s register entry reflects PR #289's confirmed merge (with the corrected final test count
and both bounded-correction rounds) and this filing's own execution-authorization step.

**What does not change.** No real company's valuation-result record exists or is populated in this
session. No real company is valued. No fair value, price target, expected return, discount rate, WACC,
beta, ERP, terminal growth rate, applied peer set, or scenario probability is assigned to any real
company. `discount_rate_evidence` remains abstained for all 27 canonical equities' Stage-3 records — this
filing does not populate it. The terminal-growth/discount-rate unit-convention gap remains open and
dormant. `TIER-0009` §K's `target_and_range`/`maximum_position_size` `valuation_required` status is
unchanged on all 27 canonical equities. `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `docs/
PORTFOLIO_INTELLIGENCE_SPEC.md`, and `VALUATION-0001` through `VALUATION-0006` are all unedited. No
target, tier, holdings, gate, cap, cluster, allocator, margin, or ladder value changes. No Company/Theme/
relationship/classification/reconciliation/recommendation/archetype/evidence Intelligence record changes.
No chart evidence of any kind is consumed. `CONTENDER-0003`, ETF/crypto evaluation, and cross-asset
synthesis remain unaddressed. `WS-0005` and `WS-0014` are unaffected.

---

**No company was valued.** `VALUATION-0007` authorizes only a future, separate Stage-4 real-company
equity valuation-result population implementation under the already-governed `VALUATION-0002`/
`VALUATION-0006` methodology and validator contracts. No target, tier, holding, gate, allocation, or trade
decision was changed or authorized. The 27-company cohort remains a bounded first equity-valuation
population, not the exhaustive Portfolio-HQ contender universe.
