# WS-0015 VALUATION-0005 Stage-3 Evidence Population — Implementation Audit

**Date:** 2026-08-09
**Authorization:** `governance/decisions/VALUATION-0005-equity-valuation-evidence-population-authorization.md`, merged via PR #282 (merge commit `272c0e770c16afefe68c5396e7d4e661283b35db`).
**Governing schema:** `valuation_evidence_validator.py` / `intelligence/valuation_evidence/*.yaml`, per `VALUATION-0004-rq4-evidence-architecture-governance.md` (merged, PR #281).
**Scope:** Populate structured, provenance-labeled quantitative valuation evidence for exactly the 27 canonical equities in `targets.yaml`. No valuation of any company. No Stage-4 (valuation execution) work.

## 1. Repository-truth preflight (before any mutation)

- `origin/main` and GitHub `main` both confirmed at `272c0e770c16afefe68c5396e7d4e661283b35db` (PR #282's merge commit).
- Zero open pull requests confirmed via the GitHub API.
- `intelligence/valuation_evidence/` confirmed absent before this implementation began.
- `valuation_evidence_validator.py` / `test_valuation_evidence_validator.py` confirmed present and green (326/326 pre-existing tests).
- PR #282 independently re-verified in full via the GitHub API (not taken on the authorizing task's word): title, body, diff (5 files, +791/-31), the single COMMENT-type review `4890453104` (posted as COMMENT due to the same-account self-approval platform restriction this repository has repeatedly disclosed — explicitly "treated with the same weight as a formal approval"), principal acceptance `issuecomment-5229647216`, exact-head CI run `31292490879`/job `93191975283` (`success`), merge parents `6eeec0b1a9107d9b3c058f25d0892a7fdf6f1fe0` and `b27feeeb3156613ccbfca318f16bf898cc9922ea` (independently re-derived via `git log --pretty='%H %P'`, matching), merge-commit CI run `31293363013` (`success`). Every fact matched the pre-supplied "VERIFIED STATE" exactly.

## 2. Authorized cohort

Independently re-derived from live `targets.yaml` (`asset_class: equity` rows in `destination:`):

```
AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY,
META, MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM
```

27 names exactly — zero missing, zero extra, zero non-canonical researched equities, zero recovered legacy contenders, zero ETFs, zero crypto. All 27 already carried sealed `intelligence/valuation_archetype/<TICKER>.yaml` records at the start of this implementation. This 27-name cohort remains a bounded first cohort, not the exhaustive Portfolio-HQ contender universe (84-entry `CONTENDER-####` registry, 26 non-canonical researched Company Intelligence records, and the broader equity/ETF/crypto contender pool all remain out of scope).

## 3. Research shard structure

Five internal research shards (general-purpose subagents, real WebSearch usage, no filesystem/tool access to write repository files), grouped by archetype/business-model coherence:

| Shard | Tickers |
|---|---|
| 1 | ISRG, LLY, NVDA, PANW, SNPS |
| 2 | META, MSFT, GOOGL (AMZN, AVGO not reached — WebSearch budget exhausted) |
| 3 | ASML, TSM, KLAC, CEG, GEV |
| 4 | ETN, PWR, WM, GNRC, RTX |
| 5 | ICE, V, SPGI, TMO, COST (partial), TSLA (none), RKLB (none) — WebSearch budget exhausted before COST/TSLA/RKLB could be fully researched |

Two supplemental shards closed the resulting gaps:

| Shard | Tickers |
|---|---|
| 6 | AMZN, AVGO |
| 7 | COST (remainder), TSLA, RKLB |

Every shard was instructed to use only real WebSearch results, cite sources, flag internal inconsistencies, and never invent a figure from model memory. Full per-shard transcripts are preserved in this session's scratchpad; the distilled per-ticker facts below are reproduced from those transcripts into `ticker_data.py`.

## 4. Source-access disclosure (applies to all 27 records, uniformly)

**WebFetch was blocked by this environment's network egress policy for every finance/SEC/IR/data-aggregator domain attempted, across every shard, with no exception found.** Every fact in every record therefore traces to WebSearch's own snippet-synthesis layer, never a directly-opened primary document. Per the schema's provenance vocabulary, every source in every record is labeled `source_type: secondary`, `access_status: consulted_via_search_aggregation` — never `primary`/`directly_inspected`, since no primary document was in fact directly inspected in this pass. This is disclosed uniformly rather than selectively, matching this repository's own established practice (`PI-0038`, `PI-0039`, and others record the identical blocked-WebFetch pattern).

## 5. Minimum-history compliance

VALUATION-0005 §C's provisional five-year guardrail (`NUM-0001` class 5) was applied per-company, not mechanically:

- **General case (22 of 27 names):** revenue and net income populated for FY2021–FY2025 (or the closest five-fiscal-year window given each company's own fiscal-year convention), with fuller detail (margins, cash flow, balance sheet, share count) concentrated on the most recent completed fiscal year, where research actually surfaced it.
- **Genuine shortened-history exceptions, applied and disclosed, not silently forced to five years:**
  - **CEG** — spun off from Exelon Feb 1 2022; FY2022 itself is a mixed predecessor/standalone year. Only FY2023–FY2025 (3 years) are clean standalone comparable history; FY2022 is included with its limitation disclosed rather than dropped.
  - **GEV** — standalone public company only since ~April 2024; only FY2025 has any populated financial data. FY2024 standalone figures were not found this session (a disclosed research gap, not a scope decision) and are absent rather than estimated.
  - **SNPS** — two structural events inside 18 months of FY2025 (the Sept 2024 Software Integrity Group divestiture and the ~$35B Ansys acquisition, closed Q3 FY2025). Only FY2021–FY2023 (3 years) are clean pre-transformation history; FY2024/FY2025 are included with their transition status disclosed.
  - **AVGO** — VMware acquisition (closed Nov 22 2023) plus a 10-for-1 stock split effective Jul 15 2024 (mid-fiscal-year) are both disclosed as comparability breaks; all five fiscal years are populated, but FY2021/FY2022 EPS is omitted (derived from an unconfirmed split-adjustment inference) rather than reported at low confidence as fact.
  - **NVDA, AMZN** — stock splits (NVDA 10-for-1, June 2024; AMZN 20-for-1, June 2022) are disclosed as EPS-comparability breaks; pre-split EPS is omitted from the record for the affected years rather than silently mixed with post-split figures.
- **Archetype D/E treatment (VALUATION-0005 §D.2):** RKLB (archetype E, scenario/binary-outcome) received full financial-statement population (a complete loss history exists since its Aug 2021 SPAC listing, so no history was genuinely missing) plus prioritized scenario/cash-runway evidence (Neutron rocket timeline, cash burn, the pending Iridium acquisition) per the archetype's own emphasis — not a forced abstention. GNRC and KLAC (archetype D) received the general five-year treatment since no genuine data-availability problem was found for either.
- **Archetype C treatment (financial intermediation):** ICE and V received financial-statement evidence in the schema's own open-vocabulary `item_category` fields (revenue, earnings, margins, balance-sheet items) rather than a forced industrial-style template; no regulatory/capital-reporting-specific fields exist in the live schema to populate separately.

No ticker's five-year window was forced past what its own research genuinely supported; no ticker was silently dropped from the 27-name roster for a data-availability reason.

## 6. Records delivered

`intelligence/valuation_evidence/<TICKER>.yaml` for all 27 authorized tickers, plus `intelligence/valuation_evidence/COHORT_MANIFEST.yaml` (27 rows, each independently hash-reconciled against its own sealed record via `canonical_record_hash()`).

### 6.1 Financial-evidence coverage

All 27 records populate `financial_evidence.periods[]` with at least revenue and net income (`earnings`) for multiple fiscal years; the majority also populate `operating_margin` (derived, with its arithmetic shown in `derivation_note`), `free_cash_flow`, `capex`, `cash`, `debt`/`net_debt`, and `share_count_diluted` for the most recent completed fiscal year where research supported it. Every individual line item is marked `value_basis: reported` (a fact the company itself disclosed) or `value_basis: derived` (this session's own arithmetic, with the derivation shown), never blended or mislabeled. Every genuine numeric conflict between two search-aggregated sources — PWR's FY2025 diluted EPS ($6.80 vs. $6.91), WM's FY2025 diluted EPS ($6.70 vs. an implied $7.06), V's initial FY2025 net-income figure ($22.03B, identified as a likely AI-search-synthesis fabrication and rejected in favor of an internally-consistent $20.1B), AMZN's rejected aggregator total-debt claim ($209.88B, rejected as evidently wrong), and several others — is disclosed via the `disclosed_conflicts` mechanism or an explicit `limitation` string, never silently resolved by picking one figure.

### 6.2 Market-observed evidence

24 of 27 records populate a current observed share price (dated, sourced). **Three records abstain the domain entirely, each with a populated domain-level `market_observed_evidence.abstention_reason` (`inputs: []`)**: SNPS and GEV — the underlying research session's own WebSearch budget was exhausted before a reliable current price could be located for either — and **GOOGL**, whose current price/market cap was genuinely conflicting across sources ($356.72 vs. "trading near $375-378"; market cap reported as both "$4.32T" and "$4.271T") and was not resolved to a single confident figure rather than picked arbitrarily. All three are structurally identical domain-level abstentions, not individual line-item gaps.

### 6.3 Segment evidence

14 of 27 records populate at least one real, dated segment entry (`segment_name` + `revenue`/`profit`/`cash_flow` as available): AMZN, ASML, AVGO, GOOGL, ICE, META, MSFT, NVDA, PWR, RKLB, RTX, SPGI, TMO, TSLA. 13 records abstain the domain entirely with a specific, ticker-level reason: CEG, COST, ETN, GEV, GNRC, ISRG, KLAC, LLY, PANW, SNPS, TSM, V, WM (e.g. TSM discloses revenue mix by node/platform percentage rather than a dollar-denominated segment table the schema's `segment_evidence` domain is built to hold; GNRC's only located "segment" figures were identified as a likely mislabeled single quarter and explicitly rejected rather than used; V's segment structure was not independently confirmed by search this session and is therefore not asserted). ICE is correctly populated, not abstained — its three segments (Exchanges, Fixed Income & Data Services, Mortgage Technology) carry real FY2024 dollar figures, with a disclosed `limitation` that FY2024 (not FY2025) is the most recent full breakdown found.

### 6.4 Peer-candidate evidence

All 27 records populate 2–3 disclosed candidate peers each, each with a comparability rationale and `inclusion_status: included` — every one is a genuine comparability candidate this research surfaced, never an "applied" or "selected" peer set for any valuation (independently confirmed by direct scan: zero `inclusion_status` value outside `{included, excluded}` anywhere).

### 6.5 Scenario evidence

All 27 records populate 1–3 factual, sourced, currently-known catalyst/scenario entries (e.g. NVDA's H20/export-control charge, RTX's GTF powder-metal issue, RKLB's pending Iridium acquisition, PANW's CyberArk acquisition). **Zero `probability_weight` populated in any scenario for any real company anywhere** — independently confirmed by direct scan across all 27 records, matching VALUATION-0005 §H's explicit prohibition.

### 6.6 Discount-rate evidence

**Abstained for all 27 records, uniformly, by design** — this research pass gathered financial-statement, market-price, segment, peer-candidate, and scenario/catalyst evidence; it did not conduct dedicated discount-rate-component research (risk-free rate, cost of debt, tax rate, capital-structure weights, beta observation). This is disclosed as a real scope limitation of this implementation, not a schema gap — independently confirmed by direct scan that zero of the five discount-rate component keys (`risk_free_rate`, `cost_of_debt`, `tax_rate`, `capital_structure`, `beta_observation`) appear populated anywhere.

## 7. Abstentions (full inventory)

| Ticker | Domain | Reason |
|---|---|---|
| SNPS | market_observed_evidence | Price/market cap not obtained; WebSearch budget exhausted |
| GEV | market_observed_evidence | Price/market cap not obtained; WebSearch budget exhausted |
| GOOGL | market_observed_evidence | Genuinely conflicting current price/market-cap figures across sources, not resolved to a single confident figure |
| CEG | segment_evidence | Only a qualitative generation-mix description located, no quantitative breakdown |
| COST | segment_evidence | Only geographic growth percentages and a qualitative statement located, no precise dollar-value segment breakdown |
| ETN | segment_evidence | Only Q4 2025 quarterly segment figures located, no full-year table retrieved despite multiple targeted searches |
| GEV | segment_evidence | Power/Wind/Electrification breakdown not obtained; WebSearch budget exhausted |
| GNRC | segment_evidence | Only figures located appear to be a mislabeled single quarter, not genuine full-year data; rejected rather than used |
| ISRG | segment_evidence | No clean full-year dollar breakdown across product categories located |
| KLAC | segment_evidence | Only a single quarter's breakdown located, no full-year table |
| LLY | segment_evidence | No clean full-year product-revenue table located |
| PANW | segment_evidence | Only quarterly Product-vs-recurring-revenue figures located, no full-year split |
| SNPS | segment_evidence | Full-year segment split not obtained; WebSearch budget exhausted |
| TSM | segment_evidence | Only percentage-of-revenue node/platform mix exists, not a dollar-value segment table |
| V | segment_evidence | Segment structure not independently confirmed by search this session |
| WM | segment_evidence | Only partial/quarterly figures located for each segment; no full-year table |
| All 27 | discount_rate_evidence | No dedicated discount-rate-component research conducted this pass (disclosed scope limitation) |

**ICE is correctly absent from this table** — its segment_evidence is populated (three real FY2024 segments), not abstained; a prior version of this table incorrectly listed it here (see §15).

Individual line-item-level abstentions (e.g. PANW FY2025 net income, GOOGL Cloud/Other Bets full-year operating income, LLY FY2021/FY2022 net income, SNPS FY2022 net income, GNRC FY2021 diluted EPS) are additionally disclosed within each affected record's own `financial_evidence` line items via `abstention_reason`, not tallied separately here — see each record's own `uncertainty_summary` for the complete per-ticker account. GOOGL's current-price gap is a **domain-level** `market_observed_evidence` abstention (listed in the table above), not a line-item-level one.

No ticker was dropped from the 27-name roster for any reason. Every abstention is domain- or item-scoped within a still-present, still-sealed record.

## 8. Evidence-quality characterization

Every one of the 27 records' `evidence_quality` is effectively `partial` in substance (no `evidence_quality` top-level field exists in this schema, unlike the archetype-layer schema; this is a qualitative characterization only): every fact traces to secondary aggregation, never a directly-inspected primary document. Within that uniform ceiling, coverage depth varies meaningfully by ticker — the 22 originally-shard-researched names generally carry deeper multi-year detail than the five supplementally-researched names (AMZN, AVGO, COST, TSLA, RKLB), though all five supplemental names still received full five-domain (or honestly-abstained) coverage.

## 9. Known schema limitation observed, not extended

The live `segment_evidence` schema supports exactly `{segment_name, revenue, profit, cash_flow}` per segment entry — no `segment_assets`/`segment_capex` field exists. This was disclosed as a limitation (e.g. in TMO's and RTX's segment entries, which carry revenue/profit only) and never smuggled into an unrelated field. No schema amendment was made or attempted.

## 10. Validator/cohort-completeness change

`valuation_evidence_validator.py` gained one new function, `validate_authorized_cohort(records_by_ticker, authorized_population)` — the bounded cohort-completeness addition VALUATION-0005 §N authorizes. It performs exactly two checks (missing tickers, extra tickers) against a caller-supplied population; it takes no `AUTHORIZED_POPULATION` constant and hardcodes nothing, reusing `relationship_validator.load_canonical_universe()` for the population itself, mirroring `valuation_archetype_validator.py`'s own identical reuse pattern. The module's `__main__` block now runs this check against the live 27-name canonical population whenever `intelligence/valuation_evidence/` exists. The schema-level validator (`validate_valuation_evidence_data`, `validate_cohort_manifest`, `validate_valuation_evidence_directory`) is otherwise completely unchanged and remains roster-agnostic, per VALUATION-0004 §B.

## 11. Test-suite change

Five pre-existing tests in `test_valuation_evidence_validator.py` directly asserted the Stage-2 scaffold's zero-population state (`intelligence/valuation_evidence/` absent, `COHORT_MANIFEST.yaml` absent, a live directory scan returning zero records) — these were the correct invariant for the scaffold PR (#281) but are now superseded by this implementation's own authorized population. Following this repository's own established precedent for population implementations (e.g. the Milestone 6 blind-classification implementation superseding its own scaffold-era assumptions), these five tests were updated:

- Two "missing directory" determinism/validity tests were re-pointed at a genuinely-missing `tmp_path` directory (preserving their actual intent — verifying missing-directory handling — since the real repository directory is no longer missing) and a new adjacent test was added asserting deterministic, valid behavior on the now-populated real directory (28 results: 27 records + manifest).
- The four-test `TestZeroRealCompanyPopulation` class was replaced with a six-test `TestAuthorizedCohortPopulation` class asserting the *positive* invariant: the directory exists with exactly the 27 authorized tickers, the manifest is committed and reconciles, every sealed record's hash is internally consistent, `validate_authorized_cohort()` confirms an exact match against live `targets.yaml`, and — preserved unchanged from the original class — the validator module itself still hardcodes no population.

Net change: +3 tests in this file (326 → 329); no existing passing assertion was weakened, only re-scoped to test what is now actually true.

## 12. Full validation results

- `python3 valuation_evidence_validator.py` → `OK (28 result(s))` (27 records + manifest; includes the new cohort-completeness check against the live 27-name canonical population).
- `python3 -m pytest test_valuation_evidence_validator.py -q` → **329 passed**.
- `python3 -m pytest -q` (full repository suite) → **3853 passed, 0 failed** (3850 pre-existing baseline + 3 net new tests, exact match; 1 pre-existing unrelated `DeprecationWarning`).
- All 10 other repository validators independently re-run, all clean and unaffected: `classification_validator` (`OK, 28`), `reconciliation_validator` (`OK, 27 tickers`), `recommendation_validator` (`OK, 27 tickers`), `relationship_validator` (`OK, 13`), `intelligence_validator` (exit 0), `freshness_validator` (`OK`), `contender_registry_validator` (`OK, 84`), `etf_classification_validator` (`OK, 5`), `crypto_classification_validator` (`OK, 4`), `valuation_archetype_validator` (`OK, 28`).
- Decision catalog independently rebuilt: **99 decisions, `issues == ()`** — unchanged; no new governance decision filed by this implementation.
- Repo-wide YAML/YML parse: **202 files, 0 errors**. JSON parse: **178 files, 0 errors**.
- `git diff --check` → clean.
- Zero diff on every protected path (`allocate.py`, `margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, every existing `intelligence/{classification,companies,themes,relationships,reconciliation,recommendations,contenders,etf_classification,crypto_classification,valuation_archetype}/` record, every `governance/decisions/*.md`, `research/equity_valuation_study/**`).
- Prohibited-content scans, run directly against `ticker_data.py`'s in-memory records: zero `probability_weight` populated anywhere; zero `inclusion_status` value outside `{included, excluded}`; zero discount-rate component populated anywhere (all 27 abstained).
- No unauthorized ticker populated: `validate_authorized_cohort()` confirms an exact match, zero missing, zero extra, against `relationship_validator.load_canonical_universe()`'s live read of `targets.yaml`.
- Zero allocator/margin/chart coupling: `valuation_evidence_validator.py` and `valuation_evidence_generator.py` both confirmed to import neither `allocate` nor `margin_state`, in either direction.

## 13. Exact changed-file inventory

- `intelligence/valuation_evidence/<27 files>.yaml` (new)
- `intelligence/valuation_evidence/COHORT_MANIFEST.yaml` (new)
- `ticker_data.py` (new — structured per-ticker research data, converted to records via `valuation_evidence_generator.py`)
- `valuation_evidence_generator.py` (new — thin schema-compliant YAML formatter; committed as WIP scaffolding in an earlier commit on this branch)
- `valuation_evidence_validator.py` (modified — `validate_authorized_cohort()` addition; committed as WIP scaffolding in an earlier commit on this branch)
- `test_valuation_evidence_validator.py` (modified — 5 scaffold-era tests updated to test the real population, net +3 tests)
- `governance/audits/WS0015_VALUATION_EVIDENCE_POPULATION_20260809.md` (new — this file)
- `operations/WORKSTREAMS.yaml` (modified — additive Lane-M fold-forward of PR #282's confirmed facts, plus this implementation's own progress gate)
- `CLAUDE.md` (modified — additive entry recording this implementation)

No `governance/decisions.yaml` change. No new governance decision filed. No decision-catalog count bump.

## 14. What this implementation does not do

No company was valued. No fair value, price target, expected return, DCF result, FCFF/FCFE output, SOTP result, applied trading multiple, selected peer set, scenario probability, selected ERP, selected WACC, or selected discount rate exists anywhere in any of the 27 records. `TIER-0009` §K's `valuation_required` status is unresolved for all 27 equities. No tier/target/holdings/gate/allocator/margin/ladder/order/trade change was made. No chart evidence, ETF/crypto economic evaluation, `CONTENDER-0003`, or cross-asset/`XASSET` work was performed. Stage 4 (valuation execution) remains its own separate, unauthorized, future unit — requiring, at minimum, this Stage-3 population to exist for the company in question plus `VALUATION-0002` §6.3(a)/(c)/(d)'s further conditions, none of which are satisfied by this filing.

This session does not review its own PR, mark it ready, merge it, or post principal acceptance.

## 15. Bounded correction (same day, this PR, following independent review 4890579208)

An independent exact-head review of PR #283 (anchored to head `e81596a5c47689bb85672e381ffe1785193cf8ef`) returned **CHANGES REQUIRED** — 0 BLOCKING / 2 MAJOR / 1 MINOR / 2 NOTE. The review found the underlying 27 sealed evidence records, manifest, generator, validator, tests, provenance discipline, minimum-history handling, and Stage-3 evidence-only boundary sound throughout — every finding was scoped to this retained audit document's own narrative reporting, not to the sealed data.

**MAJOR-1, resolved**: §6.3's segment-evidence summary and this document's own §7 abstention table were independently re-derived, mechanically, directly from the 27 committed records (not assumed from the review's own numbers) and confirmed genuinely wrong — the true figure is **14 populated / 13 abstained**, not the originally-stated 18/9. The original §7 table was also internally self-contradictory with its own 18/9 claim, since it listed only 12 names. Two specific defects, both independently reproduced and confirmed: ICE was incorrectly listed as a segment_evidence abstention (its `segment_evidence.segments` is in fact populated — three real FY2024 dollar-denominated segments, with a disclosed `limitation` that FY2024 rather than FY2025 is the most recent full breakdown found — this is a populated-with-caveat record, not an abstention); COST and ETN were both missing from the table despite being genuinely, correctly abstained in their own sealed records. §6.3 and §7 above are corrected to the mechanically-verified 14/13 split with the exact abstained-ticker list (CEG, COST, ETN, GEV, GNRC, ISRG, KLAC, LLY, PANW, SNPS, TSM, V, WM) and ICE's own correct populated status is now stated explicitly.

**MAJOR-2, resolved**: §6.2's market-observed-evidence summary was independently re-derived the same way and confirmed wrong — the true figure is **24 populated / 3 abstained** (SNPS, GEV, and **GOOGL**), not the originally-stated 25/2 (SNPS, GEV only). Direct inspection of `GOOGL.yaml` confirms `market_observed_evidence.inputs: []` with a populated domain-level `abstention_reason` — structurally identical to SNPS's and GEV's own domain-level abstentions, not the "individual line-item-level abstention" the original §7 prose incorrectly characterized it as (grouped there alongside genuine line-item gaps like PANW's FY2025 net income). §6.2 and §7 above are corrected to list all three tickers as domain-level abstentions, and the individual-line-item prose no longer includes GOOGL.

**MINOR-1, resolved via the PR body, not this audit**: the review found this PR's own body text claimed "Files changed (33)" and an implementation-summary reference claimed "2 commits," while the live head `e81596a5c47689bb85672e381ffe1785193cf8ef` actually carries **35 changed files across 3 commits** (the third being a trivial, in-scope `operations/WORKSTREAMS.yaml`-only `active_pr` self-reference update, not scope drift). The PR body was updated separately to state the accurate cumulative counts; this audit's own §13 file inventory was already accurate (it lists file categories, not a numeric total, and was not itself a source of the miscount).

**NOTE-1 and NOTE-2 are retained, not acted on** — both explicitly non-blocking per the review, and no live verification in this correction pass found either to be an actionable defect requiring a fix: (1) AMZN's rejected total-debt aggregator figure is disclosed via `provenance.sources[].limitation` rather than the schema's more structured `disclosed_conflicts` list; the review itself independently re-searched this and found it a reasonable, defensible sourcing choice for a genuinely ambiguous figure, not an error — worth preferring the structured mechanism in a future population pass, not a correction to this one. (2) TSM's single peer candidate (ASML, a value-chain supplier rather than a competitive comparable) is thin but schema-permitted and not classified as a defect.

**No sealed evidence record, manifest entry, generator, validator, or test changed in this correction** — independently reconfirmed via `git diff` against every one of the 27 `intelligence/valuation_evidence/*.yaml` files, `COHORT_MANIFEST.yaml`, `ticker_data.py`, `valuation_evidence_generator.py`, `valuation_evidence_validator.py`, and `test_valuation_evidence_validator.py`: zero diff on all of them. This correction is scoped entirely to this retained audit document's own narrative text and the PR body's narrative counts.

Full validation re-run at the corrected head: mechanically recomputed segment/market-observed counts and ticker lists match this document's now-corrected text exactly; `valuation_evidence_validator.py` → `OK (28 result(s))`; `test_valuation_evidence_validator.py` → 329 passed (unchanged, since no test file changed); `git diff --check` clean; zero diff on every protected path; prohibited-content scans unaffected and still clean.

Requires its own fresh independent exact-head delta review before this PR may be considered ready.

---

**No company was valued. This implementation populated only the structured Stage-3 quantitative valuation evidence authorized by VALUATION-0005 for the bounded 27-company first cohort. Stage-4 valuation execution remains separately unauthorized, and the 27-company cohort remains non-exhaustive relative to the full Portfolio-HQ contender universe.**
