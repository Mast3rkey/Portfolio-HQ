---
decision_id: VALUATION-0005
date: 2026-08-09
status: Proposed
category: valuation_evidence_population_authorization
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0002, XASSET-0005, VALUATION-0001, VALUATION-0002, VALUATION-0003, VALUATION-0004, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
file: governance/decisions/VALUATION-0005-equity-valuation-evidence-population-authorization.md
---

## Context

### Authority for this unit

`governance/decisions/VALUATION-0004-rq4-evidence-architecture-governance.md` §O sets out four
distinct states in this domain and reaches only the first: (1) evidence architecture governed
(`VALUATION-0004` itself); (2) schema/validator/test implementation merged (PR #281, independently
reconfirmed below); (3) **real-company evidence population — "a further, separately authorized, later
unit — not authorized by this filing or by the implementation it authorizes... matching this
repository's own first-coverage-discipline precedent"**; (4) valuation execution, requiring states 2
and 3 plus `VALUATION-0002` §6.3(a)/(c)/(d). `VALUATION-0004` §P restates the same boundary from the
implementation side: "Real-company population requires its own separate, later, explicitly authorized
unit (§O.3)." `VALUATION-0004` §H separately, explicitly reserves minimum-historical-period-length
policy to "the future population authorization" rather than inventing one itself, "because no existing
repository authority sets one for this domain, and inventing one here would itself be exactly the kind
of unsupported numeric parameter `NUM-0001`'s provenance-classification discipline exists to prevent."
This filing is that state-3 population authorization, and the filing `VALUATION-0004` §H names as the
correct place to set the minimum-history rule.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` independently fetched and
  confirmed at `6eeec0b1a9107d9b3c058f25d0892a7fdf6f1fe0` — exact match to the task's own stated
  expectation, not merely copied from it. Local branch `claude/valuation-0005-authorization-xh7fxo`
  confirmed identical to that SHA, working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API before any edit — no competing active
  mutation lane.
- **PR #281 (`VALUATION-0004`-authorized Stage-2 schema/validator/test implementation) independently
  reconfirmed merged**, full lifecycle re-verified from the GitHub API, not taken on the task brief's
  word — see §P below for the complete, independently-reconstructed record, including two review-chain
  reads that were pulled directly from the PR's own review list rather than assumed from the task
  brief's summary.
- **`valuation_evidence_validator.py` and `test_valuation_evidence_validator.py` confirmed present on
  `main`** at this session's starting head; `intelligence/valuation_evidence/` confirmed **absent** —
  no `COHORT_MANIFEST.yaml` and no per-ticker record exists anywhere in the repository.
- **The 27-name canonical equity cohort independently re-derived from live `targets.yaml`** (`asset_class:
  equity` rows in the `destination:` list, not assumed from the task brief's own list): `AMZN, ASML,
  AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, RKLB, RTX,
  SNPS, SPGI, TMO, TSLA, TSM, V, WM` — exact match to the task brief's expected roster, confirmed by
  independent derivation, not by trusting the brief.
- **`operations/WORKSTREAMS.yaml`'s `WS-0015` entry found stale**: `active_branch`/`active_pr` still
  point at PR #281's own branch/number, and `last_verified_main_sha` still points at PR #281's own base
  commit rather than its merge commit. This filing performs the deferred Lane M synchronization (§P/§Q),
  additively, without editing any existing gate's own text.
- **Full repository `pytest` baseline independently reproduced before any edit**: 3850 passed, 0
  failed, 1 pre-existing unrelated `DeprecationWarning` (`intelligence_classification_sanitizer.py`'s
  own `\d` docstring escape) — exact match to PR #281's own final claim.
- **`test_portfolio_hq_dashboard_decisions.py` independently re-run**: 95 passed.
- **Decision catalog independently rebuilt**: 98 decisions, 0 issues, before this filing's own new
  entry.
- **All eleven repository validators independently re-run directly, clean**: `classification_validator.py`
  (`OK (28 result(s))`), `reconciliation_validator.py` (`OK (27 tickers)`), `recommendation_validator.py`
  (`OK (27 tickers)`), `relationship_validator.py` (`OK (13 record(s))`), `intelligence_validator.py`,
  `freshness_validator.py` (`OK`), `contender_registry_validator.py` (`OK (84 entries)`),
  `etf_classification_validator.py` (`OK (5 result(s))`), `crypto_classification_validator.py`
  (`OK (4 result(s))`), `valuation_archetype_validator.py` (`OK (28 result(s))`), and
  `valuation_evidence_validator.py` itself (`OK (0 result(s))`).
- **`intelligence/valuation_archetype/COHORT_MANIFEST.yaml` read** to confirm the precedent this filing
  follows for cohort structure: 27 entries, `governing_decision: VALUATION-0003`, one row per ticker
  with `content_sha256`/`shard_id`/`sealed_at`/`record_path`.
- **`valuation_evidence_validator.py`'s live Stage-2 schema read in full** to ground every evidence-
  authority section below in the schema's own actual field names, not invented ones: `financial_evidence`
  (`periods[]` with `period_type` ∈ {`annual`,`quarterly`,`ttm`}, `restated`/`restated_from_note`,
  `line_items[]` with `item_category`, `value_basis` ∈ {`reported`,`derived`}, `derivation_note`,
  `disclosed_conflicts`, `abstention_reason`), `segment_evidence` (`segments[]` with `segment_name`,
  `revenue`, `profit`, `cash_flow` only — **no `segment_assets` or `segment_capex` field**, confirmed by
  direct inspection, see §I), `market_observed_evidence` (`inputs[]`, including `value_basis`/
  `derivation_note` support added in PR #281's own bounded correction), `discount_rate_evidence`
  (exactly five components — `risk_free_rate`, `cost_of_debt`, `tax_rate`, `capital_structure`,
  `beta_observation` — with `discount_rate`/`wacc`/`equity_risk_premium`/`erp`/`cost_of_capital`
  structurally absent from every allowed-key set and separately forbidden-key-scanned),
  `peer_set_evidence` (`candidates[]` with `identity`, `comparability_rationale`, `provenance`,
  `as_of_date`, `inclusion_status` ∈ {`included`,`excluded`}, `inclusion_rationale`), `scenario_evidence`
  (`scenarios[]` with `scenario_name`, `variables[]`, and a structurally-present but SS K-restricted
  `probability_weight`/`probability_weight_provenance_label` pair), `freshness_state` (computed, not
  merely trusted), and `abstention_index` reconciled against exactly six abstainable domains
  (`financial_evidence`, `segment_evidence`, `market_observed_evidence`, `discount_rate_evidence`,
  `peer_set_evidence`, `scenario_evidence` — `freshness_state` is not itself abstainable). `record_status`
  ∈ {`draft`,`sealed`}. Confirmed `validate_cohort_manifest()` performs no closed-population check today
  (`VALUATION-0004` §B's deliberate roster-agnostic design) — the mechanism §N below authorizes closes
  that gap for this cohort specifically, without narrowing the schema's own roster-agnostic design.
- **`valuation_archetype_validator.py` read** to confirm its own closed-27-name reconciliation reuses
  `relationship_validator.load_canonical_universe()` rather than a hand-maintained list — the precedent
  §N below directs the future implementation to follow.

## Decision

**This decision authorizes exactly one future, separate, bounded Stage-3 implementation PR to populate
structured quantitative valuation evidence, under the `VALUATION-0004`-governed schema, for the 27
canonical equities currently carrying a sealed `valuation_archetype` record. It sets a provisional
minimum-history data-sufficiency guardrail for that population (§D), and specifies the evidence,
provenance, abstention, and validation rules the future implementation must follow. It authorizes no
population, evidence, or valuation itself — implementation does not begin in this session.**

### A. What is authorized

One future, separate, bounded implementation PR that creates, for each of the 27 names in §B: exactly
one `intelligence/valuation_evidence/<TICKER>.yaml` record conforming to the live Stage-2 schema, plus
one `COHORT_MANIFEST.yaml` (mirroring `intelligence/valuation_archetype/COHORT_MANIFEST.yaml`'s own
shape — one row per ticker, `content_sha256`, `shard_id`, `sealed_at`, `governing_decision:
VALUATION-0005`, `record_path`), plus the smallest cohort-specific validator addition and focused tests
described in §N. That future PR requires its own full independent-review/correction/re-review/
principal-acceptance/merge/post-merge-verification lifecycle under `OPS-0007` §1 / `OPS-0009` Lane G
before any of it is authoritative. Nothing in §§B–O below is itself a populated record — this filing
specifies what a later implementation must build and how.

### B. Cohort — exactly the 27 canonical equities, one bounded first evidence cohort

The cohort is exactly the 27 names independently re-derived from live `targets.yaml` in the Preflight
above: `AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META, MSFT, NVDA,
PANW, PWR, RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM` — zero exclusions, zero additions. Every one of
the 27 already carries a sealed `intelligence/valuation_archetype/<TICKER>.yaml` record (`VALUATION-0003`/
`TIER-0006`-adjacent precedent, `PI-0037`/`REL-0006`-adjacent Milestone coverage), so this authorization
targets an already-defined, already-covered roster rather than opening new first-coverage research.

**This cohort is explicitly, repeatedly not the exhaustive researched equity universe and not the
exhaustive Portfolio-HQ contender universe** — matching `VALUATION-0004` §S's own restated boundary,
unedited and unnarrowed here:

- The 26 already-researched non-canonical Company Intelligence contenders (`PI-0032`/`PI-0033`'s own
  roster) remain outside this authorization. None of them carries a `valuation_archetype` record, and
  none is authorized for `valuation_evidence` population by this filing.
- The `CONTENDER-####` registry (`WS-0014` item 1, `intelligence/contenders/registry.yaml`, 84 entries)
  identifies a broader universe of ticker mentions across this repository — none of it is authorized for
  population here.
- **Any future equity contender may reuse the `VALUATION-0004`-governed schema without amendment**
  (`VALUATION-0004` §B's roster-agnostic design is preserved, not narrowed, by this filing) — but
  population of any name outside the 27 listed above requires its own separate, later, explicitly
  authorized population unit, matching this repository's own first-coverage-discipline precedent for
  every prior Intelligence-adjacent content expansion (`PI-0003`, `PI-0005`, `PI-0007`,
  `PI-0023`–`PI-0031`, `PI-0036`, `VALUATION-0003` §B's own identical restatement for the archetype
  layer).

### C. Batching / shard structure — one authorized cycle, internally sharded, no per-shard gating

All 27 names are authorized for population in **one implementation cycle**, internally sharded into
approximately five shards of approximately five to six names each for research and review quality —
directly mirroring `VALUATION-0003` §G's own precedent, already applied to this identical 27-name
cohort one layer earlier (archetype assignment). No shard carries independent governance authority; no
per-shard or per-archetype governance filing is required or permitted. This is a content-population
cycle over an already-fully-covered, already-classified roster — not a first-coverage research wave in
`OPS-0008`'s sense (which governs opening coverage on genuinely new companies) — so `OPS-0008`'s
default 5–6-company wave-size and stop-before-drafting gate are cited as a compatible sizing precedent,
not as controlling authority for this unit.

**No silent contraction, under any circumstance** — matching `VALUATION-0003` §J's identical stop-
condition discipline: if evidence access proves materially inadequate for part of the authorized cohort
(a blocked primary source, an unreconcilable numeric conflict, or a company whose economics genuinely
resist the evidence domains in §E–§I), the future implementation must (1) disclose the specific problem
per company and domain, (2) seal that company's record with a first-class `abstention_reason` on the
affected domain(s) rather than a fabricated or force-fit figure (§K), and (3) stop and escalate for
principal direction only if the entire authorized unit cannot be completed honestly — never silently
drop an authorized ticker from the cohort or from `COHORT_MANIFEST.yaml`.

### D. Minimum-history data-sufficiency guardrail — provisional governance guardrail, `NUM-0001` class 5

The future implementation must apply the following minimum-history convention. **This is a provisional,
data-sufficiency guardrail adopted under incomplete evidence, not an empirically calibrated or
evidence-bounded-selected parameter** (see the `NUM-0001` classification below).

1. **DCF/ROIC/trend-relevant evidence (the general case).** Target **five completed fiscal years of
   annual history** (`financial_evidence.periods[]` with `period_type: annual`). Where a company has
   less available history because of an IPO, spin-off, restructuring, or a comparable genuine
   limitation, the future implementation must collect **all available comparable history instead** —
   never fabricate or backfill periods that do not exist — and must explicitly disclose the shortened
   history (via the affected period range plus a note in `uncertainty_summary` or the relevant
   `abstention_reason`, never silently presented as though five years were available).
2. **Scenario-heavy / cyclical archetypes (report archetype D — commodity/cyclical — and archetype E —
   early-stage/binary-outcome, per protocol §5, bound by reference).** The five-year annual target is
   **not forced merely for symmetry** where the evidence problem is scenario- or cycle-specific. The
   future implementation must instead collect the available historical record plus the evidence
   relevant to normalized-cycle or scenario analysis (e.g., a commodity-price-cycle reference period for
   D, a milestone/catalyst timeline for E), and must disclose where the available history cannot support
   the archetype's own governed methodology family (§2 of `VALUATION-0002`, bound by reference).
3. **Financial-intermediation economics (report archetype C, per protocol §5).** The future
   implementation must collect the available comparable regulatory/capital-reporting history
   appropriate to the specific institution's business model, and must **not force irrelevant
   industrial-style history fields** (e.g., a `capex`/`reinvestment` line item that does not map
   cleanly onto a bank's or insurer's actual disclosed financials) merely to satisfy a generic
   five-year-annual template. Structural limitations specific to the business model must be disclosed,
   not smoothed over.
4. **Quarterly / TTM supplementation.** Quarterly or trailing-twelve-month evidence may supplement
   annual history where sourced and relevant, but every such fact must carry its own explicit
   `period_type` and must **never silently substitute** for missing annual history — a quarter is not
   interchangeable with a fiscal year in this schema or in this guardrail.
5. **Restatements.** The existing `restated`/`restated_from_note` distinction (`VALUATION-0004` §C.13,
   already structurally present in the live schema) must be preserved exactly — a restated period's
   prior reported figures are never silently overwritten; both the original and the restated value, with
   their own provenance, are the honest record.

**`NUM-0001` classification: class 5, "Provisional governance guardrail"** — "a deliberately
conservative interim value adopted under incomplete evidence, explicitly labeled as such, with a stated
review condition" (`NUM-0001` §1.5). This is the accurate class, not class 4 ("evidence-bounded
governance selection"): class 4 requires that "evidence establishes a defensible range, constraint, or
trade-off" from which governance then selects a specific value within that supported space
(`NUM-0001` §7) — no such range-establishing evidence exists here. `VALUATION-0004` §H already found,
independently and explicitly, that "no existing repository authority (protocol, `VALUATION-0001`/
`0002`/`0003`, `NUM-0001`) sets one for this domain," and declined to invent one for exactly that
reason. Nor is it class 3 ("empirically calibrated" — no evidence "directly and uniquely favors this
specific number over real, tested alternatives," `NUM-0001` §8; five years is a widely-used convention
in equity-research practice, not a number this repository's own evidence has tested against
alternatives). **Provisional label**: "provisional, not empirically calibrated — a data-sufficiency
convention adopted for population-cycle consistency, not a tested optimum." **Review condition
(evidence-driven, per `NUM-0001` §6's own explicit allowance for non-calendar conditions)**: revisit if
real Stage-3 population evidence across the 27-name cohort shows this default is systematically
inadequate for a given archetype or company (e.g., forcing an unnatural fit, producing materially
misleading shortened-history disclosures at scale), or if a future, separately authorized evidence-
sufficiency study is proposed and produces range-establishing evidence — either of which would support
reclassifying a revised value under `NUM-0001` class 4, not merely re-asserting class 5 with a different
number.

### E. Evidence population authority — financial evidence

The future implementation may populate, for each of the 27 names, only the structured evidence the live
schema's `financial_evidence`/`segment_evidence` domains already support (§ Preflight), where relevant
and sourced: revenue history, operating income, operating margins, net income/earnings, EPS-relevant
figures where the schema's `item_category` vocabulary accommodates them, operating cash flow, free cash
flow, capex, D&A-relevant evidence where needed, cash, debt, net debt/cash, basic and diluted share
counts, dilution evidence, segment-level financials via `segment_evidence` where structurally supported
(§I), the available comparable regulatory/capital evidence for archetype-C names (§D.3), and
ROIC/invested-capital ingredients and cyclicality/normalization evidence via the existing
`invested_capital`/`roic_related` and disclosed-conflict/uncertainty mechanisms.

**Reported vs. derived, exactly as the schema already enforces**: every populated fact must carry
`value_basis` — `reported` for a figure taken directly from a source, `derived` (with a non-empty
`derivation_note` stating the method and inputs) for a figure computed from sourced facts. A derived
value must never be presented as directly reported, and a methodology or policy assumption must never be
disguised as a fact — this governs, for example, that a computed free-cash-flow figure derived from
reported operating cash flow and reported capex is `derived` with its derivation disclosed, never
silently entered as though it were itself a reported line item.

### F. Market-observed evidence authority

The future implementation may record, in `market_observed_evidence.inputs[]`, sourced and dated raw
observations only: an observed market price, raw market-capitalization ingredients, a risk-free-rate
observation, an observable bond-yield or cost-of-debt observation, a beta observation (recorded only as
an observation with its own disclosed observation/estimation metadata — never as a chosen policy input),
and peer-market observations. **Prohibited at Stage 3, structurally enforced by the live schema's own
forbidden-key set and the future cohort-completeness addition's own scan (§N):** a selected equity-risk
premium, a chosen WACC, a chosen discount rate, a chosen beta methodology/estimation window/reference-
index policy, and any valuation output — fair value, expected return, or price target of any kind.

### G. Peer-set boundary

The future implementation may record, per `peer_set_evidence.candidates[]` as the live schema already
supports: candidate peer identity, a comparability rationale, source provenance and an as-of date, and
an `inclusion_status` (`included`/`excluded`) with its own `inclusion_rationale` — or a first-class
`abstention_reason` where no defensible candidate set exists. Recording a candidate's comparability
evidence and inclusion/exclusion disposition is **evidence-layer disposition only**, per `VALUATION-0004`
§J's own text ("this decision selects no peer for any company — the structure exists so a future,
separately authorized population phase can record peer-set evidence and its reasoning transparently").
**Stage 3 does not decide, and this filing does not authorize deciding, the peer set actually applied to
compute a relative-valuation multiple for any company** — that application-level selection remains part
of valuation execution (§O.4 in `VALUATION-0004`'s framing), not evidence population.

### H. Scenario boundary

The future implementation may record, per `scenario_evidence.scenarios[]` as the live schema already
supports: named scenario variables and their evidence basis, a `provenance_label` from the closed
`market_derived`/`historically_observed`/`analyst_consensus_cited`/`assumed_for_illustration` vocabulary
for every scenario input, and a first-class abstention where no defensible scenario set exists. **The
schema's `probability_weight`/`probability_weight_provenance_label` fields remain structurally present
but must not be populated with any value for any real company by this filing or by the implementation it
authorizes** — assigning an actual probability weight to an actual scenario for an actual company is
valuation-relevant judgment, not evidence-layer content, and remains outside this authorization exactly
as `VALUATION-0004` §K already established.

### I. Segment / SOTP boundary, and a known schema limit disclosed, not extended

The future implementation may record, per `segment_evidence.segments[]` as the live schema already
supports: segment-level revenue, profit, and cash-flow evidence where disclosed, `shared_
unallocated_costs`, `intersegment_eliminations`, and a segment-level abstention where a company's
disclosure is not adequately granular. **No sum-of-the-parts valuation of any kind may be performed.**

**Known schema limit, disclosed, not extended by this filing.** The live Stage-2 schema's
`_SEGMENT_ENTRY_ALLOWED_KEYS` is exactly `{segment_name, revenue, profit, cash_flow}` — there is no
`segment_assets` or `segment_capex` field. This filing does **not** authorize a schema amendment to add
either field: no live evidence gathered this session demonstrates that population cannot proceed
honestly without them (a company's segment-level asset or capex facts, where genuinely load-bearing for
an archetype-F evidence picture, can be disclosed as unavailable via the segment's own `abstention_reason`
or the record's `uncertainty_summary`, rather than forced). The future implementation must **never**
smuggle a segment-asset or segment-capex fact into an unrelated allowed field (e.g., padding
`cash_flow` with capex data) to work around this gap. If a future implementing session finds, from real
population work, that this limitation is genuinely blocking rather than merely inconvenient, that
finding must be disclosed as its own recommendation for a future, separately authorized schema
amendment — not resolved unilaterally inside this population-authorization's own scope.

### J. Source / provenance rule — reused, not invented

The future implementation must reuse, exactly and without amendment, the live schema's two existing
provenance vocabularies: **source provenance** (`source_type` ∈ {`primary`,`secondary`}; `access_status`
∈ {`directly_inspected`,`consulted_via_search_aggregation`,`attempted_not_directly_inspected`}) on every
raw financial-statement or market-observed fact; and **assumption/scenario provenance** (`market_derived`,
`historically_observed`, `analyst_consensus_cited`, `assumed_for_illustration`) on every discount-rate
component, peer-set entry, and scenario variable — matching `VALUATION-0004` §F exactly. The source
hierarchy is bound by reference to `VALUATION-0004` §G, unedited: company/regulatory primary filings,
then earnings releases/investor presentations, then market/regulatory data, then secondary aggregators,
then analyst/consensus data with explicit labeling — descending reliability, honest fallback disclosure
required at every step. **Primary sources must be attempted where applicable; a primary-access failure
must never cause invented data or silent omission** — a fallback to a lower-reliability source class is
permitted only with its own honest, explicit `access_status` disclosure, matching this repository's own
extensively disclosed history of primary-source access failures across every prior Intelligence layer.
This is not a "primary-only-forever" rule, matching `VALUATION-0004` §G's own explicit rejection of one.

### K. Abstention / conflict policy

First-class abstention (`abstention_reason`, non-empty) is required on any of the six abstainable
domains (`financial_evidence`, `segment_evidence`, `market_observed_evidence`, `discount_rate_evidence`,
`peer_set_evidence`, `scenario_evidence`) wherever evidence is unavailable or structurally insufficient,
reconciled against `abstention_index` exactly as the live schema already enforces. The future
implementation must never: fabricate a figure, silently estimate a missing value, silently average or
choose between conflicting sourced values, or silently omit an authorized ticker from the cohort.
Conflicting sourced values for the same fact must be retained and disclosed using the schema's own
`disclosed_conflicts` mechanism (for financial line items) or the market-observed input's equivalent —
never resolved by guess, matching this repository's own established precedent (e.g. `VWO`'s disclosed
China-weight conflict in the ETF classification layer). Stale facts must follow the schema's own
computed `freshness_state` mechanism (`most_recent_evidence_date`/`next_review_due_date`/`stale`,
independently recomputed by the validator, not merely trusted).

### L. Partial-record sealing policy

A record may be sealed (`record_status: sealed`) with disclosed gaps if: every populated fact carries
its required provenance; every materially unavailable domain carries an explicit abstention disclosed
per §K; hash and manifest validation pass; and the future implementation's own independent review accepts
the disclosed evidence quality as honest and complete in its disclosure, even where the underlying
evidence itself is incomplete. **Artificial completeness is never required merely to achieve sealing** —
a well-disclosed gap is a correct output under this policy, not a defect to be papered over.

### M. Implementation architecture — the smallest sufficient build

The one future implementation PR authorized by §A may build: manual/hybrid researched structured YAML
population for the 27 names, internally sharded per §C; one integrating/sealing session that assembles
and hash-reconciles the shard outputs into sealed records and `COHORT_MANIFEST.yaml`; and the validator
addition and tests described in §N. **It may not build**: a new scraping/data-ingestion framework or
automated feed integration (population is manually/hybrid researched, matching every prior Intelligence-
adjacent content layer in this repository); or a sanitizer/redaction pipeline **by default** — Stage 3
evidence is objective, dated, sourced financial and market fact, structurally distinct from the
archetype layer's own judgment-call risk of `portfolio_role_ref`/`conviction`/target-weight
contamination that motivated `TIER-0004`'s and `VALUATION-0003`'s own blind-drafting/redaction
machinery. No sanitizer is authorized here; if the future implementing session finds live evidence of a
real prohibited-input boundary during population that a sanitizer would be needed to enforce, it must
disclose that finding explicitly before building one, rather than assuming its absence is settled by
this filing.

### N. Validation authority for the future implementation

The future implementation must **reuse** `valuation_evidence_validator.py` — it may not create a
duplicate schema validator. It is authorized to make exactly the smallest cohort-specific addition
needed for this population unit, preferably: a thin closed-cohort completeness/reconciliation function
inside the existing module (mirroring `valuation_archetype_validator.py`'s own reuse of
`relationship_validator.load_canonical_universe()` for its identical 27-name reconciliation, rather than
a hand-maintained list) proving, for this cohort specifically: exactly the 27 authorized tickers are
present in `COHORT_MANIFEST.yaml`, with zero missing and zero extra; a ticker with every domain
abstained still counts as present (abstention is not absence); and manifest/hash reconciliation is
exact. **This addition must not narrow `validate_cohort_manifest()`'s own existing roster-agnostic
design** (`VALUATION-0004` §B) — it is a cohort-specific check layered alongside the roster-agnostic
validator, not a replacement of it, so the same schema and validator remain usable, unmodified, for any
future contender population authorized separately. If the live validator already supports this
reconciliation without modification by the time implementation begins, no redundant code should be
added.

Before that future PR may be marked ready, it must independently pass, at minimum: its own new Stage-3-
cohort-specific focused tests; `valuation_evidence_validator.py` run directly; the full repository
`pytest` suite; every applicable pre-existing repository validator; exact 27-name cohort reconciliation
(zero missing, zero extra, abstained records counted as present); manifest/hash reconciliation; repo-wide
YAML/YML parsing; repo-wide JSON parsing; `git diff --check`; an exact changed-file inventory; a full
protected-path scan (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, every existing `intelligence/**` record outside
`intelligence/valuation_evidence/` itself, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `PROTOCOL_V1.md`,
`METHODOLOGY_EVALUATION_REPORT.md`, every other `governance/decisions/*.md`); the existing prohibited-
output scan (fair-value/price-target/expected-return/opaque-discount-rate/directive-trading-language/
chart-domain-terminology — reusing `valuation_evidence_validator.py`'s own independent free-text and
key-name scans, never a new, separately-drifting copy of them); confirmation that zero tickers outside
the authorized 27 were populated; zero coupling of any kind to `allocate.py`/`margin_state.py`/
`targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`; decision-catalog reconciliation;
and exact-head CI green.

### O. Non-authority — explicit, exhaustive

This decision, and the future implementation it authorizes, create no:

- Fair value, price target, expected return, or upside/downside calculation for any real company.
- Actual DCF, FCFF, or FCFE valuation output for any real company.
- Sum-of-the-parts (SOTP) valuation of any kind.
- Application of any relative-valuation multiple to any real company.
- Chosen weighted-average cost of capital, chosen equity risk premium, chosen discount rate, or chosen
  beta estimation methodology/window/reference-index policy for any real company.
- Real-company scenario probability of any kind — the schema's `probability_weight` field remains
  structurally present but unpopulated for every real company under this authorization.
- A selected, applied valuation peer set for any real company — only comparability evidence and
  inclusion/exclusion disposition per §G.
- Resolution, closure, or narrowing of `TIER-0009` §K's `target_and_range`/`maximum_position_size`
  `valuation_required` status on any equity.
- Target, tier, holdings, gate, cap, cluster, or allocator change of any kind.
- Margin-policy change of any kind.
- Buy-ladder (`LADDER-0001`) change of any kind.
- Chart ingestion, chart interpretation, or any chart-derived input of any kind (`TIER-0003`'s
  fundamentals-only boundary is restated, not reopened).
- Order or trade of any kind.
- Any `CONTENDER-0003` work, contender-registry regeneration, or legacy-history recovery.
- Any ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content — remains `WS-0014`/`XASSET-0001` §C/§D's own separate, unaffected scope.
- Any overlap/concentration modeling, cross-asset synthesis, or unlevered-versus-levered allocation
  testing — remains `XASSET-0005`'s own separate, unaffected scope.
- Any Company/Theme/relationship/classification/reconciliation/recommendation/archetype Intelligence
  record creation or edit — this filing and its authorized implementation touch only the new
  `intelligence/valuation_evidence/` layer.
- Any edit to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`,
  `VALUATION-0001`, `VALUATION-0002`, `VALUATION-0003`, or `VALUATION-0004`.
- Any schema amendment to `valuation_evidence_validator.py` beyond the bounded cohort-completeness
  addition §N authorizes.
- Any actual population code or populated evidence record — this filing authorizes a future
  implementation; it performs none of that work itself.

### P. Lane M — PR #281 (`VALUATION-0004`-authorized Stage-2 implementation) lifecycle, independently
reconfirmed

Independently re-verified via the GitHub API this session, not assumed:

- PR #281, "WS-0015: VALUATION-0004 Stage-2 — RQ4 evidence-architecture scaffold (schema + validator +
  tests)," base `main` @ `6f70e7d2de0ad202a1386d1e6fb20bb34b2d0b6b`, head
  `350d825dcbb5972350a6fab504831be328ae0b5a`, 4 changed files, 5 commits.
- Review chain, independently re-read in full from the PR's own review list (4 reviews, all `COMMENTED`
  due to the same-account self-review platform restriction this repository has repeatedly disclosed,
  each explicit that its verdict carries the same weight as a formal review):
  1. `4889789139` — **CHANGES REQUIRED**, 0 BLOCKING / 1 MAJOR / 1 MINOR / 1 NOTE (a free-text valuation-
     language scan gap and a market-observed reported/derived-marker gap).
  2. `4889931092` — **CHANGES REQUIRED** (prior findings resolved, one narrower MINOR surfaced).
  3. `4890158953` — **CHANGES REQUIRED** (prior MINOR resolved, one false-positive MINOR surfaced).
  4. `4890356660` — **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 2
     non-actionable NOTE, anchored to the accepted head.
- Bounded corrections resolving the review chain's findings: `c025882` (strengthened the free-text
  valuation-language scan; added market-observed `value_basis`/`derivation_note` support),
  `17c917e` (closed residual free-text adjacency gaps), `350d825` (required a numeric conclusion before
  the generic "is" branch) — all independently confirmed present in this session's own `git log` on
  `origin/main`.
- Principal acceptance: `issuecomment-5229426613`, at exact head
  `350d825dcbb5972350a6fab504831be328ae0b5a` — independently re-read in full, confirming all four
  review-chain findings resolved and zero surviving BLOCKING/MAJOR/MINOR findings.
- Exact-head CI: run `31287230269`, job `93178159217`, `status: completed`/`conclusion: success` —
  independently re-fetched and confirmed.
- Merge: `6eeec0b1a9107d9b3c058f25d0892a7fdf6f1fe0`, parents `6f70e7d2de0ad202a1386d1e6fb20bb34b2d0b6b`
  and `350d825dcbb5972350a6fab504831be328ae0b5a` — independently re-confirmed via `git log --pretty='%H
  %P'`, not merely quoted from the task brief.
- Merge-commit CI: run `31290891267`, job `93187702806` — independently re-fetched via the GitHub
  Actions API, `status: completed`/`conclusion: success`, head SHA confirmed matching the merge commit
  exactly.
- **Post-merge validation independently reproduced this session, not taken on any prior claim's word**:
  `valuation_evidence_validator.py` run directly — `OK (0 result(s))`; `test_valuation_evidence_
  validator.py` — 326 passed; `test_portfolio_hq_dashboard_decisions.py` — 95 passed; full repository
  `pytest` — **3850 passed, 0 failed**, 1 pre-existing unrelated `DeprecationWarning`; decision catalog —
  **98 decisions, 0 issues**; all eleven repository validators clean (§ Preflight); zero
  `intelligence/valuation_evidence/` content of any kind confirmed still absent, consistent with
  `VALUATION-0004` §P's absolute zero-real-company-population bar for the Stage-2 unit.

`VALUATION-0002` §6.3(b)'s RQ4-closure precondition is therefore satisfied for the first time as of this
merge, per `VALUATION-0004` §O's own state 1→2 transition — a schema, a closed-schema validator, and
passing tests now exist on `main`. This does not itself authorize population (state 3); this filing is
that separate authorization.

### Q. Register synchronization (Lane M, this filing)

`operations/WORKSTREAMS.yaml`'s `WS-0015` entry receives, additive only — no existing gate's own text
edited:

1. A new `valuation0004-rq4-evidence-architecture-implementation-post-merge-verification` gate recording
   §P's independently reconfirmed PR #281 facts in full — the existing `valuation0004-rq4-evidence-
   architecture-implementation` gate's own text (`status: in_progress`, `pr: 281`) is left byte-unedited;
   this new gate is where the confirmed-merged, confirmed-clean state is recorded.
2. A new `valuation0005-evidence-population-authorization` gate (`status: in_progress`, `pr: null` —
   this filing does not mark its own unmerged work complete, matching every prior filing's identical
   self-reference discipline in this repository).
3. `status` remains `proposed` (authorizing population does not itself complete `WS-0015`'s own broader
   charter-and-doctrine objective — the future Stage-3 implementation, and any further future Stage-4
   application-phase authorization, remain separate later steps). `priority` remains `secondary`.
   `dependencies` remains `[]`.
4. `active_branch`, `active_pr` (nulled — no implementation PR is opened by this filing),
   `last_verified_main_sha`, `last_verified_date`, `blocker`, `next_action`, `completion_criteria`, and
   `authorized_by` updated to this filing's own live state, reflecting: Stage 1 (charter + methodology-
   evaluation report) complete; Stage 2 (RQ4 evidence-architecture schema/validator/test) complete,
   merged via PR #281; Stage 3 (real-company evidence population) — **authorization filed in this PR,
   implementation not yet begun**; Stage 4 (valuation execution) remains separately, wholly unauthorized.

No other workstream entry is touched. `WS-0005` and `WS-0014` are unaffected.

### R. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0005-equity-valuation-evidence-population-authorization.md` (this
   file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0005`).
3. `operations/WORKSTREAMS.yaml` (§Q above).
4. `CLAUDE.md` (one Decisions Log pointer entry).
5. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 98 → 99).

**No other file is touched.** No production validator, no production data file, no `intelligence/**`
record, no `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
change, no `targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml` change.

### S. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to its
exact head per `OPS-0007` §1 (`OPS-0009` Lane G — new authorization, full weight, never reduced),
complete any required bounded correction and exact-head re-review, and receive explicit principal
acceptance before it may be marked ready or merged. **This decision does not mark itself ready and does
not authorize its own merge.** No Stage-3 evidence-population implementation PR may open, and §§A–P
above are not effective, until this PR merges to `main`.

## Rationale

**Why authorize population now, in a filing separate from the Stage-2 implementation and from any
future Stage-3 implementation.** Matches this repository's own established "define, then later
authorize implementation" discipline at every layer of the Portfolio/Theme/relationship/classification/
reconciliation/recommendation/archetype/evidence Intelligence programs (`REL-0001` before `REL-0002`;
`TIER-0001`/`TIER-0002` before `TIER-0005` before the Milestone 6 implementation; `XASSET-0002` before
`XASSET-0003`; `VALUATION-0002` before `VALUATION-0003`; `VALUATION-0004` before this filing, one layer
deeper still). `VALUATION-0004` §O and §P already anticipated this exact filing as the next required
unit — authorizing it now, cleanly bounded to authorization-plus-rules rather than folding in
implementation, avoids collapsing a population-policy decision (what minimum-history standard applies,
what evidence domains are in scope, what the abstention/sealing discipline is) into an implementation
decision (the exact research and YAML-writing work) before either has been independently reviewed on its
own terms.

**Why set the minimum-history rule in this filing, not leave it to the future implementation.**
`VALUATION-0004` §H explicitly reserved this decision to "the future population authorization," naming
this filing by role before it existed. Leaving it unset would risk five internal shards each inventing
their own inconsistent standard for what "sufficient" history means — exactly the kind of drift this
repository's governance history has repeatedly corrected after the fact (e.g. `TIER-0004`'s BLOCKING
finding on restated content). Setting it now, explicitly labeled provisional under `NUM-0001` class 5,
gives the future implementation one consistent, disclosed standard while leaving room for it to be
revised once real population evidence exists.

**Why `NUM-0001` class 5, not class 4 or class 3.** `NUM-0001` §7's class-4 test requires evidence that
"establishes a defensible range" from which a specific value is selected with a stated economic reason;
no such range-establishing evidence exists for a minimum-history convention in this repository — no
sweep, no backtest, no prior sizing study. `NUM-0001` §8's class-3 test requires evidence that "directly
and uniquely favors" the specific number over tested alternatives; "five years" is an ordinary equity-
research convention, not a number this repository has itself tested. Class 5 — "a deliberately
conservative interim value adopted under incomplete evidence" with "a stated review condition" — is the
precise, honest classification, and using it here extends `NUM-0001`'s discipline into a new domain
rather than inventing an ad hoc alternative.

**Why all 27 in one authorized cycle, internally sharded, rather than smaller sequential population-
authorization filings.** Unlike a first-coverage Company Intelligence research wave (`OPS-0008`'s own
governing domain — genuinely new companies with no prior repository evidence), all 27 names here already
carry sealed Company Intelligence and sealed archetype-classification coverage. The risk this
authorization bounds is evidence-collection and provenance discipline over an already-covered roster, not
first-coverage research risk. `VALUATION-0003` §G's own precedent — authorizing this identical 27-name
cohort in one cycle, internally sharded, for archetype assignment one layer earlier — is the closer,
directly on-point analog, and this filing follows it rather than importing a smaller batch size from a
structurally different situation.

**Why no sanitizer/blind-drafting requirement by default.** `TIER-0004`'s and `VALUATION-0003`'s own
redaction machinery exists because their evidence sources (Company Intelligence records) embed
policy-adjacent content (`portfolio_role_ref`, `conviction.rating`) in the same file a blind drafter
would otherwise read, contaminating an independence-sensitive judgment call. Stage-3 evidence — dated,
sourced financial and market fact — carries no comparable contamination risk by its own nature; imposing
that machinery here without a demonstrated need would be process overhead unjustified by any actual risk
finding. The future implementation retains the authority, and the obligation, to build one if it
discovers a real prohibited-input boundary during population.

**Why `category: valuation_evidence_population_authorization`, a new category distinct from
`VALUATION-0004`'s `valuation_evidence_governance`.** `VALUATION-0004` governs the evidence architecture's
structure and rules; this filing authorizes the act of populating real-company content under that
architecture — a structurally distinct governance act, matching the precedent `TIER-0001` established
when it took its own new category for a decision playing a structurally different role in the same
overall program, and that `VALUATION-0002`'s and `VALUATION-0004`'s own Rationale sections each cite as
the model for exactly this kind of situation.

## Alternatives Considered

- **Combine this population authorization with the Stage-3 implementation itself in one filing.**
  Rejected — repeats the "define, then later authorize implementation" discipline this program has
  followed at every prior layer (see Rationale); population is real, external, per-company research work,
  a materially different risk class from an authorization-and-rules filing.
- **Leave the minimum-history-length policy unset, deferring it entirely to the future implementing
  session's own judgment.** Rejected — `VALUATION-0004` §H explicitly named this filing as the correct
  place to set it, and leaving it unset invites inconsistent per-shard standards with no disclosed
  governing rule to audit against.
- **Batch the 27 names into multiple smaller population-authorization filings (e.g., 5–6 at a time,
  mirroring `OPS-0008`'s first-coverage research-wave default).** Rejected — this is not first-coverage
  research; all 27 names already carry sealed Company Intelligence and archetype coverage, and
  `VALUATION-0003` §G's own one-cycle/internally-sharded precedent for this identical cohort is the
  closer, directly on-point analog.
- **Classify the minimum-history rule as `NUM-0001` class 4 (evidence-bounded governance selection).**
  Rejected — class 4 requires range-establishing evidence that does not exist here; using it would
  overstate the rule's evidentiary basis exactly as `NUM-0001` itself warns against.
- **Extend the Stage-2 schema now to add `segment_assets`/`segment_capex` fields.** Rejected — no live
  evidence gathered this session demonstrates population cannot proceed honestly without them (the
  disclosed-abstention path covers the gap), and a schema amendment is its own bounded implementation
  act deserving its own independent review, not something to fold speculatively into a population-
  authorization filing.
- **Require a sanitizer/blind-drafting workflow for Stage 3, mirroring the archetype layer's Milestone-6-
  style redaction, as a precaution.** Rejected as an unjustified default — Stage-3 evidence is objective
  financial fact, not a judgment call carrying the same contamination risk the archetype layer's own
  redaction machinery was built to prevent; the future implementation retains authority to build one if
  it finds a genuine need.
- **Authorize the Stage-3 implementation to design and add `segment_assets`/`segment_capex` fields
  ad hoc if it finds them useful during population.** Rejected — silently expanding the schema mid-
  population, without its own independent review, would repeat exactly the "combine schema design with
  content work" risk `VALUATION-0004`'s own Rationale already rejected for the schema's original
  construction; any such need must be disclosed as a recommendation for a future, separately authorized
  amendment instead.

## Consequences

**What changes.** A future, separate Stage-3 implementation PR may now be opened — but only after this
governance PR itself is independently reviewed and principal-accepted — to populate structured
quantitative valuation evidence for the 27 canonical equities under `VALUATION-0004`'s schema, following
this filing's minimum-history guardrail, evidence-authority boundaries, provenance rules, abstention/
conflict policy, and validation contract. `WS-0015`'s register entry reflects PR #281's confirmed merge
and this filing's own population-authorization step.

**What does not change.** No real company's quantitative evidence exists or is populated by this filing.
No real company is valued. No fair value, price target, expected return, discount rate, applied peer set,
or scenario probability is assigned to any real company. No SOTP valuation is performed. `TIER-0009` §K's
`target_and_range`/`maximum_position_size` `valuation_required` status is unchanged on all 27 canonical
equities. `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`,
and `VALUATION-0001`–`VALUATION-0004` are all unedited. `valuation_evidence_validator.py`'s live schema is
unedited by this filing — only a future implementation's own bounded addition, under §N, may extend it.
No target, tier, holdings, gate, cap, cluster, allocator, margin, or ladder value changes. No Company/
Theme/relationship/classification/reconciliation/recommendation/archetype Intelligence record changes. No
chart evidence of any kind is consumed. `CONTENDER-0003`, ETF/crypto evaluation, and cross-asset synthesis
remain unaddressed. `WS-0005` and `WS-0014` are unaffected. The 27-company cohort remains a bounded first
equity-valuation cohort, not the exhaustive Portfolio-HQ contender universe.

---

No real-company quantitative valuation evidence was populated and no company was valued.
`VALUATION-0005` authorizes only the future bounded Stage-3 evidence-population implementation for the
named 27-company first cohort. Stage 4 valuation execution remains separately unauthorized, and the
27-company cohort remains non-exhaustive relative to the full Portfolio-HQ contender universe.
