---
decision_id: OPS-0016
date: 2026-08-04
status: Proposed
category: operations_coordination
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0009, OPS-0011, OPS-0012, OPS-0013, OPS-0014, OPS-0015, PI-0037, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
---

## Context

`OPS-0015` recorded that Portfolio-HQ is first being built as a personal, repository-native application and set out a seven-phase future-application roadmap (A–G), a parallel-work protocol, a discovered-work reconciliation discipline, and a deferred commercialization posture. It named no application, gave the future application no identity distinct from "Portfolio-HQ" itself, and did not address mobile or cloud execution, screenshot/evidence ingestion boundaries, chart evidence beyond what `CHART-0001`/`CHART-0002` already govern, a broader buy-ladder/trim/sell-review research program beyond `LADDER-0001`'s frozen three-arm buy-ladder charter, Portfolio Intelligence's eventual opportunity-cost comparison function, a slate of future governance-mechanism candidates (too-hard register, pre-registered falsifiers, base-rate evidence, and related concepts), or the explicit separation between accepted policy and research/analysis that may recommend changing it.

Since `OPS-0015`'s merge, `PI-0037` determined `WS-0005` Milestone 3 complete (Company Intelligence coverage of the canonical roster), leaving Milestone 4 (relationship mapping) as the next, still-unauthorized `WS-0005` step. The human repository principal has now explicitly authorized exactly one further, bounded governance-and-roadmap-reconciliation unit: to name the future application ("Eureka"), record its mobile/cloud-execution architecture and operating lanes, record screenshot-evidence-ingestion boundaries, situate the already-accepted chart-evidence (`CHART-0001`/`CHART-0002`) and buy-ladder (`LADDER-0001`) charters within that architecture without re-authorizing or duplicating them, record a broader future chart-package design candidate and a trim/sell-review research dimension `LADDER-0001` does not cover, record Portfolio Intelligence's eventual opportunity-cost comparison function and its advisory-only boundary, record ten future governance-mechanism candidates as candidates only, restate the policy/analysis/software/visualization separation, and record a seventeen-step future sequencing order — all without authorizing any implementation, research, or repository/policy mutation. No architecture or roadmap-reconciliation audit artifact is retained anywhere in this repository supporting this filing — as with `OPS-0015` §H, this decision records the principal's explicit direction given in this session's own prompt, not an inspected audit.

## Decision

`OPS-0016` records, as durable governance authority: the name "Eureka" for Portfolio-HQ's future unified user-facing application; the authoritative-repository, cloud-executable, mobile-operable execution architecture and its four conceptual operating lanes; screenshot/evidence-ingestion boundaries; the chart-evidence framework's relationship to already-accepted `CHART-0001`/`CHART-0002` authority; a future chart-package design candidate; a buy-ladder/trim/sell-review research program restating `LADDER-0001`'s existing charter and adding trim/sell-review candidates it does not cover; four governed visual zones as a future presentation/policy-research concept; Portfolio Intelligence's eventual opportunity-cost comparison function and its advisory-only limits; ten future governance-mechanism candidates; the policy/analysis/software/visualization separation; and a seventeen-step future sequencing order. **This decision authorizes no application implementation, no mobile or cloud workflow implementation, no screenshot-ingestion code, no chart construction or interpretation, no backtesting, no `WS-0005` Milestone 4 or relationship mapping, no target/tier/cap/cluster/gate/ladder/trim/sell/margin/holdings/allocator change, no brokerage integration, no order, no commercialization step, no repository rename, and no new workstream.** It is naming, architecture, and roadmap-recording only.

### A. Eureka identity

The project's and user-facing application's name is **Eureka**, one word. The current GitHub repository remains `Mast3rkey/Portfolio-HQ` — this decision renames no repository, package, path, module, branch, URL, or historical artifact. Any future repository rename requires its own separate migration decision, impact review, implementation, tests, redirects, and principal approval; none of that is authorized here. Eureka remains personal-first per `OPS-0015` §A/§F — commercialization stays deferred and non-blocking.

**Mission** (restates and extends `OPS-0015` §B, does not narrow it): Eureka is the human principal's personal, repository-native, recommendation-only investment operating system — a unified visual and interactive projection of repository truth that integrates research, portfolio analysis, governance, risk, and advisory allocation while preserving manual execution. `OPS-0015`'s Phase A–G application roadmap is Eureka's roadmap under its new name; naming it here does not add, remove, reorder, or re-gate any phase.

### B. Authoritative and execution architecture

- GitHub and the governed repository remain the source of truth (`OPS-0001`, `GOV-0002`). A laptop is not the source of truth and must not become a permanent runtime dependency.
- Eureka should ultimately be cloud-executable and mobile-operable; the phone is intended to become the ordinary control surface. A laptop may remain useful as an optional high-volume screenshot and evidence-ingestion station (see §C) — an optional convenience, never a requirement.
- Local-machine state must not silently affect governed outputs. Cloud execution must begin from a clean checkout of an exact repository SHA.
- Every Eureka output must disclose: repository, branch, exact SHA, run ID, time, input freshness, validation state, and abstention reasons — the same disclosure discipline `OPS-0011` already requires of the dashboard, restated here as a whole-application requirement, not narrowed or widened.
- Secrets remain in protected secret storage. Eureka requires no brokerage-order credentials — order methods remain stripped from `alpaca_client.py` per the repository's founding rule (CLAUDE.md, Identity & Role).
- Recommendation output and factual repository mutation remain separate workflows. Manual Robinhood execution remains absolute.

**Four conceptual operating lanes** (naming and organizing principle only — no lane is implemented by this decision):

1. **Read lane** — inspect repository truth: research, holdings, policy, governance, workstreams, system health. Corresponds to `OPS-0015` Phases A–C and the dashboard/explorer work already delivered under `WS-0007` (`OPS-0011`/`OPS-0012`/`OPS-0013`).
2. **Advisory allocation lane** — collect explicitly confirmed fresh external facts; validate readiness; invoke existing `allocate.py`; return a recommendation artifact; make no commit, push, order, or silent state update. Corresponds to `OPS-0015` Phase E, which itself overlaps `OPS-0007` §5's already-authorized scenario-display bridge — this decision does not narrow, widen, or duplicate either.
3. **Evidence-sync lane** — ingest screenshots and other factual evidence; extract proposed facts; show existing value, observed value, proposed delta, provenance, and uncertainty; require human factual confirmation; update repository truth only through the governed branch/PR lifecycle already required by `OPS-0014`. Corresponds to `OPS-0015` Phase F.
4. **Engineering lane** — perform repository work in an isolated local or cloud execution environment; preserve branch, tests, exact-head review, human acceptance, merge, and post-merge verification per `OPS-0007`/`OPS-0009`.

### C. Screenshot and evidence ingestion

- Screenshots are evidence, not policy.
- Screenshots may support factual synchronization of: holdings, shares, cash, equity, margin state, confirmed transactions, timestamps, and other observable account facts — the same class of fact `OPS-0014` Class 2 already governs and `PHQ-2026-04`/`PHQ-2026-05`/`PHQ-2026-06` already exemplify.
- Screenshot ingestion may not silently modify: targets, tiers, gates, ladders, trims, sell rules, research conclusions, allocator behavior, margin policy, or brokerage behavior.
- Bulk screenshot ingestion may be performed from a laptop for convenience, but ordinary Eureka operation must not depend on that laptop (§B).
- Illegible, conflicting, incomplete, or stale evidence must produce disclosure or abstention rather than guessed facts — the same discipline `PHQ-2026-06` already applied when this repository declined to fabricate a hash for an unopenable upload path.

No dedicated, ongoing "screenshot ingestion" workstream currently exists in `operations/WORKSTREAMS.yaml`; this discipline is currently carried directly by `OPS-0014`'s Class 0–4 classification, not by a workstream register entry. This decision records the evidence-sync lane as a roadmap-level restatement of that existing discipline and creates no new workstream to hold it.

### D. Chart evidence framework

Charts are governed evidence and explanation tools. They may inform recommendations concerning: business fundamentals; valuation; cyclicality; balance-sheet risk; price history; drawdown and recovery; volatility; customer or product concentration; portfolio weight; targets and maximums; theme and economic-system exposure; dependency and correlated-loss risk; buy-ladder design; trim reviews; thesis-break and sell reviews.

Charts may not independently: create policy; assign tiers or targets; change ladders; trigger buys, trims, or permanent sells; duplicate allocator logic; write repository state; place or imply orders.

Chart authority depends on: source; methodology; date; freshness; limitations; whether the evidence is observed, derived, modeled, tested, untested, or analogy-based — the same evidentiary-provenance discipline §I.6 below generalizes.

Historical HTML reports remain evidence artifacts, not the living Eureka application, per `OPS-0011` §2's existing treatment.

**This section restates and situates, without re-authorizing or duplicating, already-accepted chart-evidence authority.** `CHART-0001` (Accepted; `WS-0011`, status: complete) and `CHART-0002` (Accepted; `WS-0012`, status: in_progress) already govern: the Chart Evidence Record schema (fact/observation/inference/uncertainty separation); the privacy standard; provenance/hash controls; the Stage 1 (image-level) / Stage 2 (ticker-level cross-timeframe synthesis) architecture; the repository-native, LFS-free evidence-package storage model; and the currently-authorized 19-name first-cohort scope. This decision changes nothing in either file and grants no chart-evidence authority beyond what they already establish — it records only that Eureka's future chart-evidence surface is the same governed framework, not a second one.

### E. Future chart package (design candidate only, no implementation authority)

Recorded as a future design candidate for what a company or holding's chart-evidence package might eventually contain — broader than `CHART-0001`/`CHART-0002`'s current TradingView-price-chart-only scope, and not authorized by recording it:

- **Fundamentals** — revenue; margins; free cash flow; debt; dilution; return on capital; capital expenditure; business-specific operating measures.
- **Valuation** — relevant valuation measures; free-cash-flow yield; historical ranges; realistic peer comparisons; valuation at possible buy and trim levels.
- **Price and risk** — drawdowns; volatility; recovery periods; important event reactions; governed buy, hold, trim-review, and exit-review zones (§G).
- **Portfolio fit** — current weight; approved target and maximum; theme and cluster exposure; ETF overlap; dependency exposure; correlated-loss contribution.
- **Evidence** — provenance; source; date; methodology; freshness; limitations.

Any future implementation of this package — including any fundamentals/valuation data source beyond the price-chart images `CHART-0001`/`CHART-0002` already cover — requires its own separate future authorization, schema design, and evidence standard, following the same discipline `PI-0006` applied before Theme Intelligence and `CHART-0001` applied before the first chart pilot.

### F. Buy-ladder, trim, and sell-review research program

**Buy deployment** is already governed by `LADDER-0001`'s accepted, bounded, hash-pinned research charter (`WS-0010`, status: proposed pending its own governance PR's independent review and merge — unaffected by this filing) — the current ATR ladder vs. a fixed-percentage pullback ladder vs. immediate/scheduled deployment, run against the current canonical non-gated equity/fund/GLD roster. This decision does not reopen, widen, or re-authorize that charter. Recorded here only as future candidates, each requiring its own separate future charter before any research begins — not implied to be in scope for `LADDER-0001`'s already-frozen three arms: volatility-aware spacing; valuation-aware spacing; event-aware staging; drawdown-plus-stabilization; simple trend or 200-day overlays as eligibility or sizing hypotheses.

**Trim methods** — recorded as future research candidates only, no charter exists yet for any of them: target-band trim; staged overweight trim; valuation-review trim; theme or correlated-risk trim; winner-preserving trim of excess above approved maximum.

**Sell methods** — recorded as future research candidates only: no automatic technical permanent sell; moving-average exit; drawdown stop; partial risk reduction; fundamental-deterioration proxy; thesis-review trigger followed by human decision.

Any future study in this program should, at minimum, compare: return; maximum drawdown; recovery time; missed upside; cash drag; rung utilization; turnover; taxes and spreads where supportable; event losses; concentration; correlated-loss exposure; false signals; parameter sensitivity; complexity and governance cost — matching the standard the repository's own closed backtests (`reports/trim_backtest.md`, `reports/rung_backtest.md`, `reports/regime_backtest.md`, `reports/trend_backtest.md`, `reports/weight_backtest.md`, `reports/t1t2_trim_backtest.md`) already applied, and preserving negative results per that same precedent. A method that depends on one fragile parameter or one favorable period should be rejected, matching `trim_backtest.md`'s own explicit rejection of per-ticker tailored parameters as overfitting.

**Permanent sells should remain primarily governed by**: thesis break; permanent competitive deterioration; governance or accounting failure; destructive capital allocation; unacceptable portfolio risk; redundancy (the VMC→MLM consolidation precedent); a clearly superior replacement; an approved decision that the holding no longer belongs. A price decline, moving-average crossover, or visual pattern alone is not sufficient permanent-sell authority — consistent with the Constitution's existing prohibition on chart-pattern-based rules (CLAUDE.md Decisions Log, July 2026, "Chart-pattern reading... permanently excluded").

### G. Four governed visual zones (future presentation and policy-research concept only)

Recorded as a future concept, not current policy or implementation authority:

- **Buy zone** — below an approved target, valuation acceptable, thesis current, and all gates pass.
- **Hold zone** — within the approved range and no action required.
- **Trim-review zone** — above an approved target or maximum, valuation materially stretched, or concentration risk elevated.
- **Exit-review zone** — thesis-break, governance, redundancy, unacceptable-risk, or replacement evidence requires human-principal review.

These zones may only ever visualize approved repository policy (`targets.yaml`, `gates.yaml`, `caps.clusters`) — a future Eureka UI may not invent them ad hoc or derive them from anything other than governed configuration and accepted decisions.

### H. Portfolio Intelligence and opportunity cost

Company Intelligence (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `PI-0001` onward) explains the business. Theme Intelligence (`PI-0006` onward) explains how holdings relate through a shared driver. Relationship analysis — `WS-0005` Milestone 4, unauthorized, not begun — will eventually explain how holdings fit together (dependency, supplier/customer, substitute, duplicate-exposure, correlated-loss mapping), explicitly distinct from measured price correlation per `OPS-0006`.

**Portfolio Intelligence should eventually compare**, as a future, separately authorized function: the next dollar across eligible uses; business quality; reinvestment runway; valuation; thesis risk; evidence freshness; portfolio role; target gap; concentration; dependency and overlap; correlated-loss risk; differentiated exposure; the next-best alternative — the same "next dollar vs. next-best alternative" comparison `PI-0016`'s standing committee-review methodology already applies at the single-company level (its bounded 2–5-comparator capital-priority comparison), generalized here as a future portfolio-wide function, not authorized by recording it.

**Portfolio Intelligence is advisory only.** It may recommend policy review but may not automatically change: tiers; targets; caps; clusters; gates; buy ladders; trims; sells; margin; allocator output — the same boundary `OPS-0006` §§10–15 and `PI-0016` already established for Company/Theme Intelligence, restated here for the portfolio-comparison function specifically.

Relationship and knowledge-graph artifacts must identify the specific investment, allocation, or risk decision they improve. They must not exist merely as decorative complexity — matching `OPS-0006`'s own explicit decline of "track correlation across everything continuously" as a standing-analysis-layer proposal.

### I. Future governance candidates (proposed, unauthorized — each requires its own separate evaluation)

Recorded as candidates only. This decision does not adopt any of the following mechanisms; each requires its own future benefit/complexity/authority/implementation review before any part of it exists in this repository:

1. **Too-Hard Register** — names or questions deliberately excluded; reason; reopening evidence; no automatic evaluation while excluded. (`PI-0033`'s per-name deferral-with-reopening-trigger pattern is an existing precedent for the shape this could take, not itself this register.)
2. **Pre-registered falsifiers** — thesis-break observations stated before capital moves.
3. **Base-rate evidence** — outside-view evidence alongside company-specific analysis.
4. **Roads-not-taken ledger** — sufficiently documented rejected opportunities for later process review.
5. **Friction ledger** — turnover, spread, tax drag, and cash drag.
6. **Evidentiary provenance types** — observed; derived; modeled; independently tested; untested; analogy-derived; principal judgment. (`NUM-0001`'s six-class provenance standard for numeric parameters is an existing, narrower precedent; this candidate would generalize the concept to evidence generally, not extend `NUM-0001` itself.)
7. **Red-team requirement** — explicit disconfirming argument or independent challenge before material policy changes.
8. **Doctrine-amendment cooling-off** — future evaluation of whether changes proposed under position or market pressure require a waiting period and position-agnostic rationale.
9. **Dashboard cadence governance** — future evaluation of whether display frequency should be deliberately limited to reduce unnecessary action.
10. **Conviction versus confidence** — conviction reflects judgment; confidence reflects the strength, freshness, and completeness of supporting evidence. (Distinct from, and not a proposal to reopen, `PI-0004`'s already-frozen `conviction.rating` four-value vocabulary.)

### J. Policy and analysis relationship

- Current accepted policy remains binding until superseded.
- Research and portfolio analysis may evaluate whether current policy remains optimal.
- Research and analysis may recommend a policy change.
- Only the human repository principal may approve that change.
- Software implements accepted policy and must not invent it.
- Visualization explains evidence and governed outputs and must not directly control implementation or execution.

This restates, as one explicit conceptual statement, the separation already practiced throughout this repository's governance record (e.g., `OPS-0006` §§13–15's "no automated scanner... rewriting Intelligence, changing tier/role/target/cap/holding" and `PI-0016`'s "advisory policy recommendation, separate from any Intelligence-maintenance recommendation") — it creates no new authority and narrows nothing already in force.

### K. Future sequencing (preferred dependency order — recorded, not authorized)

1. This PR's own lifecycle completes (independent review, principal acceptance, merge, post-merge verification).
2. Verify and reconcile any material factual or lifecycle gaps found in the process.
3. Prepare and authorize `WS-0005` Milestone 4.
4. Relationship, dependency, overlap, and correlated-risk mapping.
5. Chart and ladder research design (building on §D/§F above, each still requiring its own future charter).
6. Zero-based role, tier, target, cap, ladder, trim, and sell review (`WS-0005` Milestones 5–7).
7. Human-principal policy decisions (`WS-0005` Milestones 8–9).
8. Encode and validate approved policy.
9. Test the unlevered portfolio and monitoring discipline.
10. Implement mobile/cloud read and advisory allocation workflows (§B lanes 1–2).
11. Develop the unified Eureka application (§A/§B, `OPS-0015` Phases A–G).
12. Perform final live account synchronization.
13. Run the final governed allocation check.
14. Manually execute or deliberately decline.
15. Reconcile confirmed facts.
16. Consider margin studies only under separate authority (`MARGIN-0005`, `GOV-0003`).
17. Consider commercialization only after the personal system is stable and validated (`OPS-0015` §F).

Steps 12–15 restate, without altering, `OPS-0015` §G's and `WS-0013`'s existing final-allocation-readiness convergence sequence — this is the same destination, named here as Eureka's own roadmap terminus, not a second or competing sequence.

## Non-authority

This decision explicitly does not authorize: `WS-0005` Milestone 4; relationship mapping; chart construction or interpretation; backtesting of any kind; Eureka application implementation; cloud workflow implementation; screenshot-ingestion code; allocation-check workflow implementation; any target, tier, cap, cluster, gate, ladder, trim, sell, margin, holdings, or allocator change; brokerage integration; orders; commercialization; repository renaming; or a new workstream. `operations/WORKSTREAMS.yaml` remains non-authoritative — a recording register, not a source of authority, per `OPS-0001`. This decision does not edit, narrow, widen, or supersede `CHART-0001`, `CHART-0002`, `LADDER-0001`, `OPS-0006`, `OPS-0007`, `OPS-0009`, `OPS-0011`, `OPS-0012`, `OPS-0013`, `OPS-0014`, or `OPS-0015` — each is cross-referenced by name and left otherwise unedited.

## Rationale

`OPS-0015` established the personal-first mission and a phased roadmap but left the future application unnamed and several architectural questions unrecorded: how it runs (laptop-independent, cloud-executable, mobile-operable), how evidence enters the repository (screenshot boundaries), how the already-accepted chart-evidence and buy-ladder charters relate to the broader application, what a fuller future chart package might contain, what trim/sell-review research remains uncharted alongside `LADDER-0001`'s buy-only scope, what Portfolio Intelligence's eventual opportunity-cost function should compare and where its advisory limit sits, what governance mechanisms might further reduce process risk, and in what order the many currently-authorized-but-unstarted and future-unauthorized pieces should eventually connect. Recording all of this now, at the roadmap level only, lets a future bounded authorization request cite a specific named piece (an identity, a lane, a candidate) rather than re-litigating the whole shape of the application each time — the same reasoning `OPS-0015` §77 gave for its own phase map, applied to the additional ground the principal has now specified.

## Alternatives Considered

**Do nothing; let each future concept (naming, mobile/cloud, a fuller chart package, trim/sell research, opportunity cost, the ten governance candidates) surface only when someone proposes it.** Rejected — this is the status quo `OPS-0015` already partially corrected for the application mission itself; the additional ground here (identity, execution architecture, evidence boundaries, the chart/ladder/trim/sell relationship to already-accepted charters, opportunity cost, governance candidates, and sequencing) remains unrecorded without this filing, and the principal has explicitly authorized recording it now.

**Fold this into `OPS-0015` as an amendment.** Rejected — `OPS-0015` is `status: Accepted` and, per `governance/decisions/README.md`, its substance may not be edited after acceptance; a dated note appended to it could record a narrow factual correction but not this much new roadmap content. A new decision, cross-referencing `OPS-0015` by `related_decisions`, is the correct instrument, matching how `OPS-0012`/`OPS-0013` each extended `OPS-0011`'s dashboard grant with their own new filings rather than editing `OPS-0011` after acceptance.

**Re-author or expand `CHART-0001`/`CHART-0002`/`LADDER-0001` to add the new chart-package and trim/sell-research material directly.** Rejected — each is `status: Accepted` and substantively closed on its own bounded scope; re-opening any of them for unrelated roadmap content would violate the same never-edit-after-acceptance convention and would blur their own tightly bounded authorizations. Cross-referencing them and recording the new material as separate future candidates preserves their existing scope exactly.

**Create a new workstream for Eureka itself.** Rejected — the controlling principal authorization for this unit explicitly prohibits creating a new workstream, and this decision's pieces already have homes: `WS-0002` (status/report layer), `WS-0003` (daily-check UX, conversational operator), `WS-0005` (Intelligence completion, relationship mapping, opportunity-cost-adjacent zero-based review), `WS-0007` (dashboard), `WS-0012` (chart evidence), `WS-0013` (final allocation readiness) — matching `OPS-0015`'s own identical reasoning for the same question.

**Authorize any implementation slice now (mobile app scaffold, screenshot-ingestion prototype, chart-package data source, a trim/sell backtest) since the architecture is being recorded anyway.** Rejected — the controlling principal authorization for this unit is explicitly naming, architecture, and roadmap-recording only; any implementation, however small, requires its own separate future authorization exactly as `OPS-0011`/`OPS-0012`/`OPS-0013`/`CHART-0001`/`CHART-0002`/`LADDER-0001` each required their own.

## Consequences

Going forward, a session working on Portfolio-HQ can call the future unified application "Eureka" and cite this decision's architecture (§B), evidence boundaries (§C), chart-framework situating (§D/§E), ladder/trim/sell research candidates (§F), visual-zone concept (§G), opportunity-cost boundary (§H), governance candidates (§I), policy/analysis separation (§J), and sequencing (§K) when scoping a future bounded authorization request. `WS-0002`, `WS-0003`, `WS-0005`, `WS-0007`, `WS-0012`, and `WS-0013` each receive one additive cross-reference to this decision (see `operations/WORKSTREAMS.yaml`) recording how they relate to Eureka's roadmap, without any change to their status, priority, authorized_scope, prohibited_scope, or completion criteria. `CHART-0001`, `CHART-0002`, and `LADDER-0001` are cross-referenced, not edited, narrowed, or widened. **Nothing about this decision authorizes writing application, mobile, cloud, screenshot-ingestion, or chart code; beginning research or backtesting; mapping relationships; changing holdings, allocation, margin, tiers, targets, caps, clusters, gates, ladders, trims, or sells; placing or preparing brokerage orders; renaming the repository; or creating a new workstream** — each remains gated behind its own separate future authorization exactly as before this filing.
