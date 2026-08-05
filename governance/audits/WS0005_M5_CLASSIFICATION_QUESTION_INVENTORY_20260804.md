# WS-0005 Milestone 5 — Classification-Question Inventory (TIER-0001 Bounded Unit)

**Implementation output of this session — not an independent review.**

| Field | Value |
|---|---|
| Authority | `governance/decisions/TIER-0001-ws0005-milestone5-classification-question-inventory.md`; `operations/WORKSTREAMS.yaml` WS-0005, `milestone-5-zero-based-classification-and-tier-architecture-review` gate |
| Scope | Read-only inventory of existing repository evidence against nine candidate classification questions. No ticker is classified. No candidate final framework is proposed. No blind classification. No baseline reconciliation. No mechanical score. |
| Repository state audited | `origin/main` @ `09fc72b4671fb18d9b3a4c2f1f1141657660ad35` (PR #244 merge commit — REL-0006/Milestone-4-complete effective), verified clean, working tree clean, zero open PRs |
| Mode | Evidence classification only — every fact below is sourced from an already-existing, already-accepted repository artifact. No new company/theme/relationship research was performed. No `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, allocator, or margin file is touched by this artifact. |

---

## 0. Preflight summary

- `origin` fetched; local `main` confirmed identical to `origin/main` at `09fc72b4671fb18d9b3a4c2f1f1141657660ad35`; working tree clean.
- PR #244 (`REL-0006`, "WS-0005 Milestone 4 completion determination") independently confirmed merged at that exact SHA (direct ancestry check: `git merge-base --is-ancestor` against PR #236's own merge commit `6ea327c7703426521b5a4c53560b77cc2f5e213e` confirms `OPS-0016` is also already folded into this tip).
- Zero open pull requests (`mcp__github__list_pull_requests`, `state: open`, returns `[]`). No active mutation lane.
- `governance/decisions/` carries 71 decision files (excluding `README.md`); `governance/decisions.yaml` carries 71 rows — confirmed 1:1 by direct count. `test_portfolio_hq_dashboard_decisions.py` currently asserts `== 71` in two places, both requiring an update to `72` as part of this filing's own implementation (below).
- `TIER-0001` confirmed unused: zero matches in `governance/decisions.yaml`, zero matches via `mcp__github__search_code` across the repository, and no `TIER-####` prefix exists anywhere in `governance/decisions/README.md`'s prefix history or `decision_log.yaml`.
- `intelligence/companies/` carries 47 records; `intelligence/themes/` carries 2; `intelligence/relationships/` carries 13 pairwise records (confirmed by direct `ls`, not assumed from a prior filing's summary).
- WS-0005's own register entry confirms Milestone 3 `status: complete` (`PI-0037`) and Milestone 4 `status: complete` (`REL-0006`); WS-0005's top-level `status` remains `in_progress`; Milestones 5-9 remain `status: proposed` prior to this filing.

No condition met a stop bar. This unit proceeded.

---

## 1. Methodology

This inventory reuses only already-accepted repository evidence: `targets.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `caps.clusters`, `docs/INVESTMENT_ONTOLOGY.md` (`ONTO-0001`), `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, all 47 Company Intelligence records, both Theme Intelligence records, all 13 relationship records, all nine `intelligence/BATCH*_COMPARISON.md` artifacts, `intelligence/freshness_registry.yaml`, and the CLAUDE.md Decisions Log entries governing tier/cluster/margin doctrine. Every figure below (record counts, field-value distributions) was computed live this session by direct inspection (`grep`/`wc`) of the current checkout — none is copied from a prior audit's stated totals.

Per the authorizing decision, this inventory examines nine candidate classification questions, framed as: does the current flat `destination:` representation (a ticker, a `target_pct`, an `asset_class`) conflate concepts that — if separated — would change a capital-priority decision, a risk interpretation, a monitoring decision, or a review-cadence decision? An axis that is already separately represented elsewhere in the repository, or whose separation would not change any of those four outcomes, is flagged as a candidate for combination or rejection rather than automatically retained.

---

## 2. What OPS-0006 §4 Milestone 5 actually authorizes (governing scope, quoted verbatim)

> **Zero-based classification and tier-architecture review** *(not authorized [by OPS-0006 itself])*. What questions the current tier system answers; where it mixes unrelated concepts; whether one tier label is adequate; the smallest set of candidate frameworks the evidence supports; candidate separation, where useful and not required merely because listed, of economic role, business quality, thesis uncertainty, capital priority, position boundaries, overlap constraints, and review cadence; rejection of unnecessary complexity; no single mechanical conviction score substituting for judgment.

`TIER-0001` is the first explicit, separate principal authorization to begin this milestone (the same pattern `PI-0023` used for Milestone 3 and `REL-0001` used for Milestone 4), bounded to exactly the question-inventory unit below — it does not authorize Milestones 6-9, a candidate framework, or any classification.

---

## 3. What the current flat representation actually is (facts, not inference)

`targets.yaml`'s `destination:` list carries, per row, exactly three fields: `ticker`, `target_pct`, `asset_class` (`equity | fund | crypto | reserve | cash`). Since `PHQ-2026-02` retired the T1/T2/ETF/band/spec tier structure, **no tier, role, or priority label of any kind exists in `targets.yaml` today** — `target_pct` is the sole per-name number, and it is simultaneously the only input `allocate.py`'s gap-filling logic reads to rank buy candidates. Three further mechanisms sit outside `targets.yaml` and touch only a subset of names:

- `gates.yaml` — a binary actionable/non-actionable flag, 6 of 27 canonical equity names (`SNPS`, `ICE`, `SPGI`, `WM`, `RKLB`, `TSLA`), each with its own `next_gate` reopening condition.
- `caps.clusters` — three named correlated-cluster ceilings (`semis` 25%, `power_infra` 20%, `oil` 20%), covering 8 of 27 canonical equity names in total (`ASML, TSM, NVDA, AVGO, KLAC, ETN, GEV, PWR`); 19 canonical names belong to no cluster cap at all.
- `issuer_lookthrough.yaml` — an 8% effective-issuer / 40% AI-platform common-driver ceiling, covering 11 named issuers (a different, overlapping-but-not-identical set from `caps.clusters`' membership).

Separately, and with **zero structural connection to `targets.yaml`**, `intelligence/companies/*.yaml` carries, per covered company: `portfolio_role_ref` (a free-text field literally still populated with the pre-`PHQ-2026-02` tier vocabulary — `T1`/`T2`/`band`/`spec` — a taxonomy `targets.yaml` itself no longer contains anywhere), `conviction.rating` (closed four-value vocabulary, `PI-0004`), `risks[].severity`/`risks[].status` (open vocabulary, `PI-0015`), and `review.cadence_days`/`next_due` (per-record schedule, `PI-0003`). `intelligence/freshness_registry.yaml` separately carries `monitoring_enabled` per enrolled ticker. `intelligence/relationships/*.yaml` separately carries a 12-item closed taxonomy of pairwise dependency/competition/complement primitives (`REL-0001`). None of these four systems (Company Intelligence, freshness registry, relationship records, `docs/INVESTMENT_ONTOLOGY.md`) writes to, reads from, or is referenced by `targets.yaml`, `gates.yaml`, `caps.clusters`, or `issuer_lookthrough.yaml` — each is independently maintained, by design (`PI-0003`: "`portfolio_role_ref` stores only the tier label, never a numeric weight... `targets.yaml` remains sole authority").

**A fifth, largely dormant system exists on top of all of this**: `docs/INVESTMENT_ONTOLOGY.md` (`ONTO-0001`) already freezes a conceptual hierarchy — Economic Systems → Company Roles → Company Quality → Capital Priority → Tier → Target Allocation — and an explicit "Preserved distinctions" list (§F) naming business quality, economic/company role, conviction, capital priority, current tier, and target allocation as concepts that must not collapse into one number. `ONTO-0001` §F states outright that its own "economic/company role" concept "does not correspond to, reinterpret, or substitute for `portfolio_role_ref`" — i.e., **two separate, already-frozen vocabularies exist for overlapping classification concepts, and no accepted decision has ever reconciled them.** `ONTO-0001` is explicitly non-prescriptive ("descriptive, not prescriptive... does not classify any company automatically") and has zero applied instances found anywhere in the 47 Company Intelligence records searched this session.

---

## 4. Classification-question-by-question inventory

For each axis: current representation (fact), evidence source, and whether separating it would change a capital-priority, risk-interpretation, monitoring, or review-cadence outcome.

### 4.1 Economic or portfolio role

**Current representation:** Two disconnected, partial systems. (a) `portfolio_role_ref` in 47 Company Intelligence records, populated with dead tier vocabulary (25 `band`, 11 `T2`, 10 `T1`, 1 `spec`) that `targets.yaml` itself no longer defines — per `PI-0003`/`PI-0022` doctrine this field is "descriptive only," fixed at authoring time, and does not float with allocator changes, so it did not get relabeled when `PHQ-2026-02` removed tiers from `targets.yaml`. It therefore currently answers "what tier was this company originally reviewed under," not "what economic function does it serve." (b) `ONTO-0001` §A/§E's economic-system/company-role vocabulary — zero applied instances. **The 6 gated names (`SNPS/ICE/SPGI/WM/RKLB/TSLA`) and `CASH`/`RESERVE`/`GLD`/`SPY`/`VEA`/`VWO`/`BTC`/`ETH`/`SOL` carry no economic-role characterization anywhere in the repository** — Company Intelligence coverage is zero for all six gated names (confirmed by direct file check this session) and funds/crypto/cash rows were never in Company Intelligence's scope at all.

**Would separation change an outcome?** Potentially yes for *capital-priority interpretation* — a reviewer currently cannot tell, from `targets.yaml` alone, that `GEV` is a power-infrastructure name and `TSM` is a foundry without opening a separate Company Intelligence record (where one exists) or `caps.clusters` (which only covers 8 of 27 names). But `asset_class` already answers the coarsest version of this question (equity/fund/crypto/reserve/cash) for allocator purposes, and the allocator itself has no need for a finer role field — it ranks purely by dollar gap. This axis matters for *human* capital-priority reasoning, not for any existing mechanical decision.

### 4.2 Research conviction

**Current representation:** `conviction.rating`, closed four-value vocabulary (`Low`/`Medium`/`High`/`Very High`, `PI-0004`), present in all 47 Company Intelligence records: 10 `High`, 37 `Medium`, 0 observed `Low` or `Very High` in this corpus. **No established, governed mapping exists anywhere from `conviction.rating` to `target_pct`** — a company's conviction rating has never been shown, by any accepted decision, to determine or even correlate with its destination weight. `TGT-0002` (COST T2→T1 promotion) was made on the principal's own independent determination, not derived from a conviction-rating formula.

**Would separation change an outcome?** Already separated in practice (conviction lives in Company Intelligence, target weight in `targets.yaml`) — but the *relationship* between them is undocumented. This is a genuine open question (§6 below), not a representation gap: conviction already has its own field; what's missing is a stated doctrine on whether/how it should inform `target_pct`, and PI-0004/PI-0016 already explicitly forbid conviction from mechanically determining allocation ("This rating explicitly excludes valuation, entry-price, allocation, trading, and margin judgments" appears verbatim in every record's conviction rationale).

### 4.3 Capital-allocation priority

**Current representation:** `target_pct` in `targets.yaml` — the only field in the entire repository with actual allocator effect. It is a single number that must simultaneously encode "how much conviction," "how large a role this plays in the economic thesis," and "how much risk concentration is acceptable," because no other field carries allocator weight.

**Would separation change an outcome?** This is the axis most directly load-bearing on live decisions — it is not a candidate for combination, it is the thing everything else potentially informs. The open question is whether *other* axes should be allowed to adjust it (they currently do not, by design — `caps.clusters`/`issuer_lookthrough.yaml` only ever clip or trim, never raise, a target).

### 4.4 Risk concentration and overlap

**Current representation:** Three non-unified mechanisms with only partial, non-identical membership: `caps.clusters` (8/27 canonical names, three clusters), `issuer_lookthrough.yaml` (11 issuers, a different set), and `intelligence/relationships/` (13 pairwise records, 12-name closed taxonomy, `REL-0001`, deliberately **not** a price-correlation measure — CLAUDE.md's own Decisions Log records that measured correlation for a proposed T1-AI-infra cluster cap came back at 0.302 (declined) versus `power_infra`'s accepted 0.560 and `oil`'s accepted 0.819, demonstrating the two concepts — structural relationship and measured price correlation — genuinely diverge and are correctly kept separate per `REL-0001` §G).

**Would separation change an outcome?** Yes, materially — this is the one axis where CLAUDE.md's own Decisions Log already documents a live doctrine gap: "T1 and T2 have no trim rule at all... That's a bigger doctrine question" (the "T1 AI-infra cluster cap: scanned and declined" entry), later partly addressed by a T1/T2 ceiling trim whose cost was explicitly recorded as "untested, not tested and cheap" (Open Items). Independently re-derived this session: 8 of 27 canonical names are covered by a cluster cap (`ASML,TSM,NVDA,AVGO,KLAC,ETN,GEV,PWR`); 14 of 27 are covered by a cluster cap and/or a relationship record (the cluster set plus `AMZN,CEG,GNRC,GOOGL,MSFT,META`, each covered only by a relationship record); 13 of 27 are covered by neither mechanism (`COST,ICE,ISRG,LLY,PANW,RKLB,RTX,SNPS,SPGI,TMO,TSLA,V,WM`) — risk concentration for roughly half the roster is currently unmeasured by any mechanism.

### 4.5 Dependency or relationship exposure

**Current representation:** `intelligence/relationships/` — 13 records, closed 12-primitive taxonomy (`REL-0001` §C: `supplier_dependency`, `customer_dependency`, `manufacturing_dependency`, `technology_platform_dependency`, `capital_spending_dependency`, `regulatory_or_reimbursement_dependency`, `commodity_or_energy_dependency`, `financing_or_interest_rate_dependency`, `geographic_or_geopolitical_dependency`, `competitor`, `substitute`, `complement`), directional, evidence-classified (`observed`/`inferred`/`modeled`/`judgmental`). All 13 existing records carry `evidence_classification: inferred` (none reaches `observed` — every counterparty's own record was independently grepped and found to carry zero corroborating disclosure of the relationship from its own side).

**Would separation change an outcome?** Already fully separated from both economic role and risk concentration by explicit design (`REL-0001` §G forbids merging relationship evidence with measured correlation). The open question is coverage, not representation: only 13 pairs exist against a 27-name roster (351 possible unordered pairs) — Milestone 4 was declared complete on an exhaustion-of-recommended-candidates basis (`REL-0006`), not a completeness-of-all-pairs basis, and `REL-0006` itself disclosed two unelevated candidate pairs (`GEV`/`ETN`/`PWR` capital-spending-dependency, `MSFT`/`AMZN` regulatory dependency) as optional, unauthorized future work.

### 4.6 Monitoring intensity

**Current representation:** `intelligence/freshness_registry.yaml`'s `monitoring_enabled` field. **Confirmed this session: all 47 enrolled rows read `monitoring_enabled: false`** — every single one, with zero exceptions, matching `AUTO-0001`'s original design ("all seven initial enrollment rows start `monitoring_enabled: false`") which has never been revisited for any of the 40 records added since.

**Would separation change an outcome?** Not currently — this field exists, is schema-distinct from review cadence (below), but carries zero live differentiation across the entire corpus. It answers a binary "is automated monitoring on" question that has never been turned on for anything. As a classification axis today it is **decorative**: a field that exists in schema but has never varied, so no capital-priority, risk, or review decision has ever depended on its value.

### 4.7 Review cadence

**Current representation:** `review.cadence_days` per Company Intelligence record. **Confirmed this session: all 47 records read `cadence_days: 90`** — uniform, with zero variation by conviction, tier legacy label, sector, or risk severity. This directly contradicts `OPS-0006` §12's own stated future requirement ("an evidence-driven, proportional refresh plan... no universal cadence") — that requirement is written into the *authorized-but-not-yet-executed* Milestone 3 refresh-planning text, and in practice every record shipped under the 90-day default regardless.

**Would separation change an outcome?** Yes, in principle (a company with `severity: high` risks or a thesis dependent on a near-term catalyst arguably warrants a shorter cadence than a stable utility-like holding), but zero evidence currently exists that this has ever been exercised — this is a genuine gap between stated intent and observed practice, not a conflation to resolve. It is schema-distinct from monitoring intensity (§4.6): one is "is a scanner watching," the other is "how often does a human re-review" — they are not redundant with each other even though both are currently undifferentiated in practice.

### 4.8 Implementation readiness

**Current representation:** `OPS-0007` §3's five-part `PROVISIONAL` lifecycle test (eligible independent review, correction if needed, exact-head re-review, principal acceptance, merge, post-merge verification) — applied per-record, not per-ticker-attribute. Every one of the 47 Company Intelligence records and all 13 relationship records has independently been carried through this lifecycle (per the merged PRs' own review/merge/post-merge-verification chains cited throughout CLAUDE.md's Decisions Log).

**Would separation change an outcome?** This is a *process* state (has this record cleared governance review), not an *economic* classification of the ticker itself — it answers "can I trust this record," not "what kind of holding is this." It is already fully tracked (via PR/review metadata, not a company-YAML field) and does not need a new per-ticker field; conflating it with any of the other eight axes would be a mistake, since a `PROVISIONAL` record can describe a `Low`-uncertainty blue-chip or a `High`-uncertainty speculative name equally well.

### 4.9 Uncertainty or evidence quality

**Current representation:** Layered across several places, none unified: `risks[].severity` (open vocabulary — confirmed this session across all 253 risk entries in the corpus: 164 `moderate`, 83 `low`, 6 `high` — `high` now appears, correcting `PI-0015`'s 2026-07 finding that it "never appears," a natural consequence of the corpus growing from 7 to 47 companies since that finding was written); `risks[].status` (confirmed this session: **all 253/253 risk entries read `status: monitoring`** — zero exceptions, meaning this field, like `monitoring_enabled`, exists in schema but has never varied in practice); per-source labeling in `sources[]` (`PRIMARY` vs. secondary, "identified but NOT opened" disclosure language used extensively per `OPS-0008`'s primary-source-readiness discipline); and `evidence_classification` in relationship records (`inferred` in all 13 current pairs).

**Would separation change an outcome?** `severity` is already meaningfully differentiated (three values in active use) and materially informs risk interpretation. `status` is not (100% one value) — the same decorative-field pattern as `monitoring_enabled` in §4.6. Source-quality labeling (`PRIMARY`/secondary/blocked) is the most operationally consequential of the three: it already gates whether a fact can enter a record at all (`OPS-0008`'s stop-before-drafting gate) and whether a batch's implementation session must disclose an access limitation — this is doing real work today, unlike `status`.

---

## 5. Cross-axis conflation actually found in the current representation

Two concrete, evidenced conflations, not hypothetical ones:

1. **`portfolio_role_ref` conflates "economic role at authoring time" with "the tier vocabulary in force at authoring time."** Since `PHQ-2026-02` retired tiers from `targets.yaml`, this field now stores a taxonomy that exists nowhere else in the live system — a real staleness, not a live conflation with `target_pct` (the two were always meant to be independent per `PI-0003`), but a naming/vocabulary drift that makes the field harder to read correctly over time. `AAPL`, `AMD`, `CRM`, and 22 other records carry a `T2`/`band`/`T1`/`spec` label describing a structure that no longer determines anything.
2. **`target_pct` is the sole load-bearing number and must implicitly stand in for capital priority, since no other field is allocator-visible.** This is not a bug — `PI-0003`/`ONTO-0001` both explicitly designed it this way ("`targets.yaml` remains sole authority for tier weights and allocation policy, full stop") — but it means every one of the other eight axes is, by construction, advisory-only to a human, never load-bearing to the allocator. Milestone 5's central question is whether that design should change, not whether it currently holds (it does, verified).

No third conflation was found where two *currently populated* fields disagree or overlap destructively — the repository's layered-but-disconnected design (Company Intelligence, freshness, relationships, ontology, `targets.yaml` each independently maintained) has avoided direct contradiction by avoiding integration entirely. The cost of that avoidance is duplication risk (§3's ONTO-0001/`portfolio_role_ref` overlap) and advisory-only status for every non-`target_pct` axis, not active conflict.

---

## 6. Axes recommended for further consideration vs. combination/rejection

| Axis | Currently differentiated in practice? | Recommendation |
|---|---|---|
| Economic/portfolio role | Partially (`portfolio_role_ref`, stale vocabulary); `ONTO-0001` unused | **Retain for further consideration** — but reconcile with `ONTO-0001` rather than invent a third vocabulary |
| Research conviction | Yes (10 High / 37 Medium) | **Already adequately separated** — no action needed; open question is its *relationship* to priority, not its representation |
| Capital-allocation priority | Yes (`target_pct`, the load-bearing field) | **Retain as-is** — this is the anchor, not a candidate for change |
| Risk concentration/overlap | Partially (8/27 cluster-covered; 14/27 covered by a cluster cap and/or a relationship record; 13/27 covered by neither) | **Retain for further consideration** — the one axis with a documented live doctrine gap (T1/T2 trim history) |
| Dependency/relationship exposure | Yes, for 13 pairs; sparse coverage | **Already adequately separated** (`REL-0001`) — coverage is a Milestone-4-adjacent question, not a Milestone-5 representation question |
| Monitoring intensity | No — 47/47 identical (`false`) | **Candidate for rejection as a distinct Milestone-5 axis** — decorative until actually varied; revisit only if/when `AUTO-0001` monitoring is ever turned on |
| Review cadence | No — 47/47 identical (90 days) | **Candidate for combination with uncertainty/evidence-quality**, or rejection as a standalone axis, until practice actually varies it |
| Implementation readiness | Yes, but as process metadata, not a ticker attribute | **Reject as a classification axis** — this is a record-lifecycle state, not an economic property of the company |
| Uncertainty/evidence quality | Mixed — `severity` yes, `status` no, source-quality yes | **Retain `severity` and source-quality; reject `status` as currently practiced** (100% one value) |

This yields, at most, **four** candidate axes worth a future Milestone-5 framework-design pass (economic role, capital priority [already the anchor], risk concentration, and a merged uncertainty/evidence-quality axis) — materially fewer than the nine originally listed, consistent with the principal's stated preference for the smallest architecture that changes a real decision.

---

## 7. Unresolved questions requiring future human/principal judgment (not resolved here)

1. Should `portfolio_role_ref`'s dead tier vocabulary be migrated to `ONTO-0001`'s vocabulary (economic role, or one of the four capital types), or is the disconnect between the two systems intentional and acceptable indefinitely?
2. Should `conviction.rating` ever inform `target_pct` through an explicit, governed rule — and if so, what evidence would justify that rule (this repository's own backtest discipline, per CLAUDE.md's Decisions Log, would require a pre-registered study before adoption)?
3. Should risk-concentration coverage be extended to the 19 canonical names outside any cluster cap, and if so, through `caps.clusters`' existing correlation-scan mechanism, `intelligence/relationships/`' structural mechanism, or a new instrument — this inventory takes no position.
4. Is `review.cadence_days`' 100% uniformity at 90 days an acceptable default, or should it actually vary per `OPS-0006` §12's own already-accepted (but unexecuted) proportionality requirement — and if so, on what basis?
5. Does the 6-name gated set (`SNPS/ICE/SPGI/WM/RKLB/TSLA`) need any classification at all while gated, given they carry destination weight but zero Company Intelligence coverage and are, by construction, never buy candidates?
6. If a future framework separates economic role from capital priority, does that require a new Company/Theme Intelligence schema field (its own future `PI-####`-style governance decision, per `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s existing change process), a `targets.yaml` schema change (its own future `PHQ-####`-style decision), or neither (a purely descriptive, non-code artifact, matching `ONTO-0001`'s own precedent)?

None of these six questions is answered by this filing. Each requires its own future, separately authorized Milestone-5 unit or principal decision.

---

## 8. What this inventory explicitly does not do

- Does not classify NVDA, GEV, or any other ticker under any framework.
- Does not propose or draft a candidate final tier framework.
- Does not perform blind classification.
- Does not reconcile the Milestone-1 baseline against anything.
- Does not compute a mechanical score of any kind for any axis.
- Does not change `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, or margin policy.
- Does not create, edit, or refresh any Company, Theme, or relationship record.
- Does not authorize Milestone 6 (blind classification), Milestone 7 (baseline reconciliation), Milestone 8 (policy recommendation), or Milestone 9 (independent review and adoption).

---

_Retained per `governance/audits/README.md` convention, alongside `WS0005_MILESTONES1-2_PORTFOLIO_INVENTORY_AUDIT_20260725.md` and `WS0005_M4_RELATIONSHIP_EVIDENCE_INVENTORY_2026-08-04.md` — a self-authored implementation-output inventory artifact, not an independent reviewer's output. Independent review of this artifact and its accompanying PR is the pending next step, per `TIER-0001`._
