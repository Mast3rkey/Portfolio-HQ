# Equity Valuation and Economic-Assessment Methodology Research — Protocol V1 (frozen pre-registration)

_Companion protocol for `governance/decisions/VALUATION-0001-equity-valuation-research-charter.md`.
This document is the complete technical specification of the study `VALUATION-0001` authorizes.
Nothing in this document is executed by the governance filing that adopts it — no methodology
comparison, no archetype-fit evaluation, and no company-level application of any kind may begin
before that filing's PR merges and this file's pinned SHA-256 verifies from the committed blob._

## 0. Why this study exists

`TIER-0009` §K (WS-0005 Milestone 8 policy-recommendation-framework authorization, `governance/
decisions/TIER-0009-ws0005-milestone8-policy-recommendation-framework-authorization.md`) forces the
`target_and_range` and `maximum_position_size` policy areas to `primary_status: valuation_required`
on all 27 canonical equities, with zero exception, because — independently reconfirmed this session
by a full-repository search — **no governed valuation or economic-assessment methodology exists
anywhere in this repository**. `TIER-0009` §K states explicitly that this gap is "a distinct,
unscoped, future workstream this filing identifies as a prerequisite... without beginning it,"
naming `MARGIN-0005`/`LADDER-0001`'s bounded-charter discipline as the model to follow for closing
it. `XASSET-0001` §J's fourteen-item `WS-0014` scope list does not include equity valuation
methodology design anywhere in its enumeration (independently re-read in full this session) — that
list is scoped to contender normalization, additional-equity classification cohorts, ETF/crypto
framework design and classification, functional cash/reserve/GLD/debt doctrine, cross-asset overlap
modeling, and sleeve/instrument sizing, none of which is "how do we estimate what an equity is
economically worth." This protocol is the first filing to take up that specific, previously-
unclaimed gap, scoped to equities only — ETF, crypto, GLD, cash/reserve, and debt-reduction
valuation/economic-assessment methodology remain separately governed and unaddressed here, per
`XASSET-0001` §C/§D's own asset-appropriate-framework requirement.

## 1. What kind of study this is (and is not)

This is **not** a historical price-return backtest in the shape of `MARGIN-0005`/`LADDER-0001` —
neither of those charters computes what an asset is *worth*; both test whether a mechanical
deployment/repayment or entry-timing *rule* would have produced a better risk-adjusted outcome than
an alternative rule, using historical price series as the input. Testing "would a valuation
methodology's output have predicted subsequent stock returns" is a materially different question —
it is **predictive research** in the exact sense CLAUDE.md's Guardrails permanently prohibit ("No
predictive research, price targets, or 'opportunity maps'") and the Decisions Log has rejected every
time it has surfaced (the June 2026 band-overlay backtest, the permanently-excluded chart-pattern-
reading exclusion, the explicit rejection of "market-view-driven lever-up" margin timing). **This
protocol authorizes no such test, now or under any future amendment of it.**

What this protocol authorizes instead is a bounded, closed, literature-grounded **methodology-
selection and methodology-design study**: which valuation/economic-assessment methodology family
(or families) are theoretically defensible, under what evidence conditions, for what kinds of
business economics — evaluated on data-availability, theoretical-soundness, and false-precision-risk
grounds, never on whether a method's output would have forecast a stock's subsequent price. This is
structurally closer to `TIER-0001`/`TIER-0002`'s "define, then later authorize implementation"
classification-framework design than to a numeric backtest — but this protocol adopts `MARGIN-0005`/
`LADDER-0001`'s **charter mechanics** (hash-pinned freeze, bounded approved-file list, explicit
non-adoption rule, workstream creation) per `TIER-0009` §K's own explicit instruction to follow that
discipline, because the underlying risk this repository is managing — a research output being read
as more conclusive or more actionable than its own scope — is identical regardless of whether the
research is numeric or a fixed literature-comparison matrix.

## 2. Research questions (pre-committed, closed set, no expansion without a charter amendment)

- **RQ1 — Archetype differentiation.** Given the canonical equity roster's genuinely differing
  business economics (asset-light recurring-revenue platforms, capital-intensive infrastructure,
  financial intermediation, commodity-linked cyclicals, early-stage/binary-outcome businesses,
  multi-segment diversified operations, and mature stable compounders — §5), is a single valuation
  methodology defensible across all of them, or does defensible valuation require
  archetype-differentiated methodology? This question is preserved as open research — this protocol
  does not pre-answer it, and CLAUDE.md's own Guardrails require the same discipline already applied
  to every other closed backtest in this repository: no forcing a single mechanism where the
  evidence does not support one.
- **RQ2 — Methodology defensibility and data requirements.** For each candidate methodology family
  (§4), what are its data requirements, governing theoretical assumptions, and known,
  literature-documented failure modes, and under what archetype/evidence conditions is it
  defensible, defensible-with-adjustment, or not defensible?
- **RQ3 — False-precision prevention.** What evidence-quality gates, output-range requirements, and
  abstention rules are structurally necessary to prevent a future application of any methodology
  from producing false precision — a single confident-looking number the underlying evidence cannot
  actually support?
- **RQ4 — Evidence sufficiency.** Does this repository's existing governed evidence base (Company
  Intelligence records under `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9 — `sector`, `industry`,
  `risks[]`, `catalysts[]`, `competitive_advantages[]`, financial-quality narrative, `evidence_
  quality`) supply sufficient structured inputs for the candidate methodology families, or does a
  future application phase require additional, separately-governed evidence categories not
  currently collected?

No fifth research question, no methodology-family or archetype-category addition, and no
reformulation of RQ1–RQ4 without a charter amendment (its own governance decision, with a newly
pinned protocol hash, per §17/§18).

## 3. Governing boundaries (restated here, binding on the entire life of this charter)

- **Fundamentals/economics only — no chart evidence.** Matching `TIER-0003`'s permanent
  fundamentals-only blind-classification boundary, restated and not reopened: no chart pattern,
  technical indicator, support/resistance level, or price-action reading of any kind is a permitted
  input to any part of this study, now or under any future methodology-application phase this
  protocol identifies as a prerequisite step but does not itself authorize.
- **No predictive claim of any kind.** No part of this study computes, estimates, or characterizes a
  future stock return, a future price movement, or a methodology's historical "accuracy" against
  subsequent price action. §1 above is the controlling statement; this bullet restates it as a hard
  boundary, not merely a framing choice.
- **No valuation of any actual company.** This study evaluates methodology **families** and
  **archetype categories** in the abstract — it does not compute, estimate, bound, or illustrate a
  fair value, price target, or expected return for any real ticker, holding, or company, sealed
  Company Intelligence record, or canonical destination-roster name, at any point in its authorized
  scope. Any future illustrative or applied use of a methodology against a real company is its own,
  separate, later, explicitly authorized unit — not performed, sketched, or implied here.
- **No adoption, no policy change.** Restated per §14 below — no result produced under this charter,
  however well-supported, automatically changes any target, tier, cap, gate, cluster, allocator,
  margin, ladder, or Intelligence-record field.
- **Zero-based discipline (`OPS-0006` §2/§3).** Any existing `portfolio_role_ref`, tier, conviction
  rating, or target weight is never read as evidence of a company's economic merit or valuation
  during this study — this protocol does not consume `targets.yaml` weights, `holdings.yaml` share
  counts, or Company Intelligence `conviction.rating`/`portfolio_role_ref` fields as research inputs
  anywhere in §4–§10.

## 4. Candidate methodology families (closed list, no pre-selected winner)

Seven families, drawn from established corporate-finance and equity-valuation literature (discounted
cash flow, comparable-company/precedent-transaction analysis, income-yield screens, economic-profit/
capital-efficiency frameworks, scenario analysis, and asset-based approaches are all standard,
independently-documented categories in that literature — not invented for this repository). Listed
alphabetically by short name, not by any implied preference or ranking:

1. **Asset-based / balance-sheet-adjusted approaches** — net asset value, adjusted book value,
   sum-of-the-parts for multi-segment structures. Standard alternative when segment or asset values
   diverge materially from a single-entity earnings or cash-flow multiple.
2. **Discounted Cash Flow — Free Cash Flow to the Firm (FCFF DCF)** — enterprise-level intrinsic
   valuation discounting unlevered free cash flow at a weighted-average cost of capital.
3. **Discounted Cash Flow — Free Cash Flow to Equity (FCFE DCF)** — equity-level intrinsic valuation
   discounting levered free cash flow (or, for financial intermediaries, a dividend-discount or
   excess-return/residual-income variant — see §5 archetype C) at a cost of equity.
4. **Earnings yield / free-cash-flow yield screens** — simplified income-based relative-value
   screens (E/P, FCF/EV) used as a first-pass sanity check, not a substitute for a full intrinsic or
   relative valuation.
5. **Relative valuation / multiples** — comparable-company and, where applicable, precedent-
   transaction multiples (P/E, EV/EBITDA, EV/Sales, P/FCF, P/B where asset-based comparison is more
   appropriate than earnings-based comparison).
6. **ROIC / reinvestment economics** — return-on-invested-capital versus cost-of-capital spread,
   reinvestment-rate and growth-durability framing (economic-profit / residual-income lens), used to
   assess capital-allocation quality as an input to, not a replacement for, an intrinsic-value method.
7. **Scenario / probability-weighted analysis** — multiple explicit scenarios (not a single base
   case) blended by disclosed, evidence-linked probability weights, used where a single-path forecast
   is not defensible (see §5 archetype E).

No eighth family, and no methodology-family addition or removal without a charter amendment (§17).
This protocol does not select a winner among these seven — RQ1/RQ2 (§2) are the open questions a
future implementation answers, per family and per archetype category, using the closed vocabulary in
§7.

## 5. Candidate valuation-methodology archetype categories (closed list, distinct from `ONTO-0001`)

A narrow, closed, seven-category taxonomy describing business economics **as they bear on
valuation-methodology fit only** — deliberately distinct from, and not a replacement, extension, or
reinterpretation of, `docs/INVESTMENT_ONTOLOGY.md` (`ONTO-0001`)'s economic-systems/company-roles/
capital-types vocabulary, which serves a different analytical purpose (thematic and qualitative
committee-review discussion, not methodology-selection criteria) and remains completely unedited and
unreferenced as an input here. This taxonomy assigns **no real company to any category** — every
example below is a generic business-model description, not a claim about any specific canonical
roster ticker, and no future step this protocol identifies performs that assignment without its own
separate authorization:

- **A — Asset-light, recurring-revenue platform.** Subscription or platform-network economics, high
  incremental margin, low reinvestment intensity relative to revenue. Classic DCF/FCFF and multiples
  are typically well-suited, subject to the usual terminal-value and growth-durability sensitivity.
- **B — Capital-intensive infrastructure / industrial.** High reinvestment intensity, long asset
  lives, revenue tied to a multi-year buildout or utility-like demand curve. DCF is applicable but
  materially more sensitive to reinvestment-rate and terminal-growth assumptions than archetype A;
  ROIC/reinvestment framing (family 6) is often a necessary companion, not merely a nice-to-have.
- **C — Financial intermediation / network economics.** Banks, payment networks, insurers, and
  similar businesses whose capital structure and regulatory capital requirements make a standard
  FCFF-DCF calculation theoretically inappropriate (financing flows are the business, not a residual
  claim on operating cash flow) — established literature instead favors dividend-discount or
  excess-return/residual-income models (family 3's stated variant) and financial-sector-specific
  multiples (e.g., price-to-book relative to return-on-equity).
- **D — Commodity / cyclical.** Earnings and cash flow highly sensitive to a commodity price or
  demand cycle; a trailing- or current-year figure is not representative of normalized economics —
  literature-standard practice uses mid-cycle or normalized earnings/cash-flow bases rather than a
  single-year snapshot.
- **E — Early-stage / binary-outcome.** Cash flow not yet stable, predictable, or positive (e.g.,
  pipeline-dependent, pre-commercial, or approval-gated economics); a single-path DCF is not
  defensible on its own — scenario/probability-weighted analysis (family 7) is the literature-
  standard alternative or necessary companion.
- **F — Diversified / multi-segment.** Materially different economics across reportable segments;
  sum-of-the-parts (family 1) is typically more defensible than a single blended multiple or
  single-entity DCF.
- **G — Mature, stable, diversified-revenue compounder.** The literature's "default case" — stable,
  diversified, well-covered by public comparables; classic DCF/FCFF and multiples are typically both
  applicable and mutually corroborating.

No eighth category, and no category addition, removal, or redefinition without a charter amendment
(§17). A future implementation may find that a given canonical roster company does not cleanly fit
one category, or fits more than one — that finding is itself a valid, disclosed research result
under §11's abstention rule, not a defect requiring the taxonomy to be forced to fit.

## 6. Evidence sources and evidence boundary

Permitted evidence sources for the future implementation this protocol authorizes: established,
citable corporate-finance and equity-valuation literature and methodology descriptions (textbook- and
practitioner-standard concepts — discounted cash flow, comparable-company analysis, residual-income/
excess-return models, sum-of-the-parts, scenario analysis — cited generically by concept, not
fabricated or attributed to a specific unverifiable source); this repository's own already-frozen
Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24) **read only to
determine what evidence categories it does and does not already structurally capture** (RQ4), never
to extract or reference any individual company's actual field values; and this protocol document
itself. **Explicitly not a permitted evidence source for this study**: any individual company's
actual financial statements, disclosures, share price, market capitalization, analyst estimate, or
Company Intelligence record content; `targets.yaml`, `holdings.yaml`, `gates.yaml`, or
`issuer_lookthrough.yaml` field values (structure may be read for the RQ4 evidence-category question
only, per above); any chart, screenshot, or technical-analysis source (§3); any brokerage, Alpaca, or
live-market-data feed.

## 7. Evaluation design — bounded, closed matrix (the "trial" mechanism for this study)

Unlike `MARGIN-0005`/`LADDER-0001`, this study has no repeated-sampling or Monte-Carlo trial
mechanism to bound with a numeric run ceiling (§14 explains why a NUM-0001-style numeric threshold is
not invented here) — its evaluation unit is a **fixed, closed 7×7 = 49-cell matrix**: each of the
seven methodology families (§4) evaluated against each of the seven archetype categories (§5), no
more, no fewer, no expansion without a charter amendment (§17). Each cell is resolved to exactly one
value from a closed four-value vocabulary — mirroring this repository's own established closed-
vocabulary, no-composite-score discipline (`TIER-0002`, `XASSET-0002`, `XASSET-0005`):

- `defensible` — the methodology family is directly applicable to the archetype category on
  standard literature grounds, no material adjustment required.
- `defensible_with_adjustment` — applicable only with a disclosed, named adjustment (e.g., a
  dividend-discount variant of family 3 for archetype C; a mid-cycle earnings base for family 5
  applied to archetype D).
- `not_defensible` — the methodology family's governing theoretical assumptions are structurally
  incompatible with the archetype category's economics (e.g., family 2's unlevered-FCFF assumption
  against archetype C's financing-flows-are-the-business structure), citing the specific
  incompatibility.
- `insufficient_evidence_to_determine` — the literature does not provide a clear, citable basis to
  resolve the cell either way; disclosed as open, never forced to one of the other three values.

No numeric score, weighted average, or composite "best methodology" ranking is computed from the
matrix at any point — each cell's disposition, and its cited reasoning, is the complete unit of
research output (§11).

## 8. Falsification / rejection criteria

A methodology family is resolved `not_defensible` for a given archetype category only when a
specific, named, citable theoretical or structural incompatibility exists — never merely because a
family is unfamiliar, complex, or produces a wide range. Named examples of a genuine incompatibility
(illustrative, not exhaustive): family 2 (FCFF DCF) against archetype C (financial intermediation) —
unlevered operating free cash flow is not a coherent construct when financing activity is the
business itself; family 4 (earnings/FCF-yield screens) against archetype E (early-stage/binary) —
the screen requires a positive, stable earnings or free-cash-flow base that does not yet exist; a
single-path family 2/3 DCF against archetype E generally — a single forecast path cannot represent a
binary or highly bimodal outcome distribution without materially understating uncertainty. A cell is
never resolved `not_defensible` on the basis of "this repository has not used it before" or any
similar non-theoretical ground.

## 9. Abstention rule

`insufficient_evidence_to_determine` (§7) is a first-class, complete, and equally legitimate research
outcome for any of the 49 cells — never a placeholder to be revisited under pressure to produce a
complete-looking matrix. A future implementation that cannot cite a defensible basis for a cell's
disposition must resolve it to `insufficient_evidence_to_determine` and disclose exactly what
additional evidence or literature review would be required to resolve it, rather than forcing a
plausible-sounding but uncited conclusion. This mirrors the abstention discipline already governing
`TIER-0002`'s `unable_to_determine` axis value and `XASSET-0002`/`XASSET-0005`'s forced-abstention
readiness fields.

## 10. False-precision protections

Independent of, and binding on, any future methodology-application phase this protocol identifies as
a downstream prerequisite step (§15) but does not itself authorize:

- **No single-point output.** Any eventual application of a `defensible`/`defensible_with_adjustment`
  methodology family to a real company must produce a **range**, with disclosed sensitivity to its
  governing assumptions (discount rate, growth rate, terminal-value method, peer-set composition, as
  applicable) — never a single number presented without its sensitivity band.
- **Mandatory assumptions ledger.** Every governing assumption (discount rate/WACC derivation, growth
  rate, terminal-value method, peer-set membership, normalization basis) must be logged with an
  explicit provenance label — `market_derived`, `historically_observed`, `analyst_consensus_cited`,
  or `assumed_for_illustration` — never presented without a label, matching `NUM-0001`'s existing
  provenance-classification discipline extended to this domain.
- **No fabricated precision.** No output may carry more decimal or percentage precision than its
  underlying evidence and assumptions actually support; a wide, honestly-disclosed range is a correct
  and complete output, not a failure of rigor.
- **Abstention is always available.** Per §9, `insufficient_evidence_to_determine` is available at
  the family/archetype level; an eventual company-level application (not authorized here) must carry
  an equivalent abstention path, never a forced output when evidence is insufficient.
- **No opaque scoring.** No composite index, weighted blend, or machine-learning-derived valuation
  output is permitted at any point under this charter or any methodology it eventually finds
  defensible — every output must remain fully inspectable and attributable to a named, cited method,
  matching this repository's blanket prohibition on opaque scores (`CHART-0001`/`CHART-0002`,
  `TIER-0002`, `XASSET-0002`).

## 11. Required output shape (the sole deliverable this protocol authorizes)

The one later, separate implementation PR this protocol authorizes (§16) produces exactly:

1. **One retained methodology-evaluation report** (`research/equity_valuation_study/
   METHODOLOGY_EVALUATION_REPORT.md` or `reports/equity_valuation_methodology.md`, implementation
   PR's choice, matching this repository's existing `reports/*.md` convention) containing: the
   complete 49-cell matrix (§7) with cited reasoning per cell; RQ1's disclosed finding (archetype
   differentiation required, not required, or inconclusive — with reasoning, never asserted without
   it); RQ3's false-precision-protection specification, elaborated for a future application phase;
   RQ4's evidence-sufficiency finding (including any disclosed structural evidence-category gap in
   the existing Company Intelligence schema); and a limitations section.
2. **Nothing else.** No fair value, price target, expected return, ranking, or buy/sell/hold/trim/
   exit signal for any company. No new or modified Company Intelligence record. No target, tier,
   cap, gate, cluster, allocator, margin, or ladder change or recommendation. No claim that Milestone
   8's `target_and_range`/`maximum_position_size` `valuation_required` status (`TIER-0009` §H/§K) is
   resolved, closed, or ready to be revisited — that determination requires its own later, separate
   governance decision, informed by but not automatically triggered by this report (§14).

## 12. Prohibited research activities (absolute for this charter's entire life)

- No computation, estimate, bound, or illustration of any real company's fair value, price target,
  or expected return, at any point, for any purpose (including as a "worked example" or "illustrative
  application" of a methodology family) — an illustrative single-company application, if ever wanted,
  requires its own separate, later, explicitly authorized unit, not performed under this protocol.
- No historical backtest of a valuation methodology's output against subsequent stock-price
  performance, under any framing (§1).
- No chart, technical-indicator, or screenshot-derived input (§3).
- No consumption of any Company Intelligence record's actual field content, `conviction.rating`,
  `portfolio_role_ref`, or any `targets.yaml`/`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`
  field value as a research input (§3/§6).
- No archetype-category (§5) assignment of any real, named canonical-roster company.
- No modification of `allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, dashboard code, the Constitution, or any existing
  `intelligence/**` record.
- No ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content of any kind — equity only, per `XASSET-0001` §C/§D's own asset-appropriate-
  framework requirement, unaffected and unaddressed here.

## 13. Data period and reproducibility

This study consumes no market-data time series and no company-specific financial-statement data of
any kind (§6) — it is a literature-grounded, closed-matrix methodology-comparison study, not an
empirical backtest over a data window. There is accordingly no data-acquisition step, no data
manifest, and no minimum-history rule analogous to `LADDER-0001` §5/§9/§21 — this is a disclosed,
deliberate structural difference from the `MARGIN-0005`/`LADDER-0001` template, not an omission.
Reproducibility instead means: every §7 matrix cell's disposition must cite the specific theoretical
or structural reasoning behind it, in enough detail that an independent reviewer could reach the same
disposition from the same reasoning without relying on the implementing session's own unstated
judgment — matching this repository's blanket "no opaque score, everything inspectable" doctrine.

## 14. Why no numeric materiality threshold is invented (NUM-0001 provenance)

`MARGIN-0005`/`LADDER-0001` each pre-commit a numeric materiality threshold (1.0 percentage point
TWR/MaxDD) because each is a comparison of empirically-measured historical outcomes, where a
threshold is needed to separate a material result from noise. This study produces no empirically-
measured numeric outcome of any kind (§13) — its output is a closed set of categorical dispositions
(§7's four-value vocabulary) with cited reasoning, not a number to be compared against a materiality
bar. Inventing a numeric threshold here would be false precision of exactly the kind §10 prohibits —
manufacturing a quantitative-looking gate for a fundamentally qualitative, literature-grounded
comparison. Per `NUM-0001`'s own provenance-classification discipline, no NUM-0001 §1 binding-value
class or §2 contextual class applies to this study, because no consequential number is produced by
it; this section documents that absence as a deliberate design choice, not an oversight.

## 15. Relationship to `TIER-0009` §K and any future application phase

This protocol's output (§11) is a **prerequisite research input** to, never itself, a resolution of
`TIER-0009` §K's identified gap. Even a complete, well-reasoned 49-cell matrix with every cell
resolved does not itself: select or adopt a methodology (family or archetype-differentiated set);
authorize a future application of any methodology to any real company; resolve `target_and_range`/
`maximum_position_size`'s forced `valuation_required` status on any of the 27 canonical equities; or
begin any later WS-0005 Milestone 8 recommendation-package revision. Each of those remains its own,
separate, later, explicitly authorized governance decision and implementation unit — following the
identical "no result automatically changes production behavior" discipline every closed backtest and
every prior research charter in this repository's Decisions Log already applies (§18/§20 below).

## 16. Data, reproducibility, and evidence-retention requirements for the future implementation

A later, separate implementation PR (not opened by the governance filing this protocol supports)
must, before it is considered complete: populate the 49-cell matrix (§7) with cited reasoning for
every cell, never leaving a cell silently blank; disclose any cell resolved
`insufficient_evidence_to_determine` together with what would be needed to resolve it (§9); disclose
RQ1's archetype-differentiation finding explicitly, with reasoning, never asserted without it;
disclose RQ4's evidence-sufficiency finding, including any Company Intelligence schema gap found;
include a limitations section restating this protocol's own structural boundaries (§3/§12); avoid any
company-specific, ticker-named application of any kind (§12); and undergo independent review (per
`OPS-0007` §1's twelve-point capability-based standard) of both methodology and findings before any
of its content is cited as evidence in a future governance decision.

## 17. Prohibited post-hoc changes

Once this protocol's governance PR merges, none of the following may change without a charter
amendment (its own governance decision, with a newly pinned protocol hash, per this document's own
§18 hash-pinning discipline): the four research questions (§2), the governing boundaries (§3), the
seven methodology families (§4), the seven archetype categories (§5), the evidence-source boundary
(§6), the 49-cell closed matrix design and its four-value vocabulary (§7), the falsification/
abstention rules (§8/§9), the false-precision protections (§10), the required output shape (§11), the
prohibited-activities list (§12), or the no-numeric-threshold determination (§14). Silent edits are
detectable by hash mismatch and void any result produced after the edit — the same discipline
`MARGIN-0005` §3 and `LADDER-0001` §20/§22 already establish.

## 18. Hash pinning

This protocol's SHA-256 is computed and pinned in `governance/decisions/VALUATION-0001-equity-
valuation-research-charter.md` §3, exactly as `MARGIN-0005` §3 pins `PROTOCOL_V2.md` and `LADDER-0001`
§3 pins `PROTOCOL_V1.md` — both this decision and this protocol are filed together in this single
governance PR. **No methodology-comparison research, archetype-fit evaluation, or any other work
under this charter may begin before this PR is merged and the pinned hash verifies from the committed
blob** (`git show <merge>:research/equity_valuation_study/PROTOCOL_V1.md | sha256sum`). Any later
change to this file is a charter amendment: its own governance decision with a newly pinned hash, per
§17.

## 19. What this protocol does not authorize

Restated here, not only in the governance filing, so this document is self-contained: no production-
code change (`allocate.py`, `levels.py`, `margin_state.py`); no dashboard integration; no live price
or financial-statement fetch; no brokerage or Alpaca-account access of any kind; no order of any
kind; no fair value, price target, or expected return for any company; no methodology adoption; no
archetype-category assignment of any real company; no Company Intelligence record creation or edit;
no target/tier/holdings/gate/cap/cluster/allocator/margin/ladder change; no ETF, crypto, GLD, cash/
reserve, or debt-reduction valuation methodology content; no chart-evidence use of any kind; no
Constitution change; no Intelligence-to-allocator coupling; no automated scoring or ranking. This
protocol authorizes exactly: four frozen research questions, a frozen closed-matrix method, and —
once a later, separate implementation PR executes it — one methodology-evaluation report. Nothing
else.
