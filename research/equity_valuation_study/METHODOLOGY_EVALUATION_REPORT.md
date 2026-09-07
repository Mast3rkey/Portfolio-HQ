# Equity Valuation Methodology Evaluation Report

**Governing charter:** `governance/decisions/VALUATION-0001-equity-valuation-research-charter.md`
**Frozen protocol:** `research/equity_valuation_study/PROTOCOL_V1.md`
**Protocol SHA-256 at study execution:** `2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980`
(independently reproduced via `sha256sum research/equity_valuation_study/PROTOCOL_V1.md` against the
`main` branch at commit `2f47adeafc9703e4074f07951df2a15a407fdc8b` before this report was drafted;
matches the hash pinned in `VALUATION-0001` §3 exactly — no drift since merge)
**Study type:** closed, literature-grounded, 7×7 methodology-comparison matrix (protocol §7) — **not**
a historical backtest, **not** a valuation of any real company, **not** a predictive study of any kind.

---

## 0. Scope statement (read this first)

This report evaluates seven abstract **valuation-methodology families** (protocol §4) against seven
abstract **business-economics archetype categories** (protocol §5) on theoretical-soundness,
data-requirement, and false-precision-risk grounds only. **No real company, holding, ticker, or Company
Intelligence record is named, valued, categorized, or referenced by content anywhere in this document.**
No fair value, price target, expected return, ranking, or buy/sell/hold/trim/exit signal is produced.
No result in this report resolves, closes, or is a substitute for its own separate governance decision
on `TIER-0009` §K's `valuation_required` status for any of the 27 canonical equities (protocol §15).
Every methodology and archetype description below is drawn from established, citable corporate-finance
and equity-valuation literature (standard textbook- and practitioner-level concepts — discounted cash
flow, comparable-company analysis, residual-income/excess-return models, sum-of-the-parts, scenario
analysis — associated in the literature with sources such as Damodaran's applied-valuation texts, the
McKinsey *Valuation* framework (Koller, Goedhart, Wessels), and the CFA Institute equity-valuation
curriculum), cited generically by concept per protocol §6 — not fabricated or attributed to any specific
unverifiable source.

---

## 1. RQ1 — Archetype differentiation finding

**Finding: archetype-differentiated methodology is required. A single valuation methodology is not
defensible across all seven archetype categories.**

**Reasoning.** No candidate family resolves `defensible` (unqualified) against all seven archetypes in
the matrix below (§4). Every family carries at least one `not_defensible` or heavily adjustment-dependent
cell, and several carry outright structural incompatibilities that no disclosed adjustment can cure
within the family's own governing assumptions:

- Family 2 (FCFF DCF) is `defensible` for archetype G and `not_defensible` for archetype C — the
  unlevered-free-cash-flow construct is not coherent when financing activity is the business itself
  (protocol §8's own named example). No adjustment converts a bank's cash flows into a meaningful
  unlevered FCFF without redefining the method into something else (which is exactly what family 3's
  archetype-C variant — dividend-discount / excess-return — already is, as its own separate family).
- Family 4 (earnings/FCF-yield screens) is `defensible` for archetype G and `not_defensible` for
  archetype E — the screen requires a positive, stable earnings or free-cash-flow base that a
  pre-commercial or approval-gated business does not yet have. This is not a matter of degree; the
  numerator the method needs does not exist.
- Family 1 (asset-based/NAV/SOTP) is `not_defensible` for archetype G (book value bears little relation
  to a stable compounder's going-concern earning power — the classical critique of asset-based methods
  applied to earnings-driven businesses) but `defensible` for archetype F (sum-of-the-parts is the
  literature-standard response to genuinely divergent segment economics).
- Family 6 (ROIC/reinvestment economics) is `defensible` for archetype B (named directly in the
  archetype's own description as "a necessary companion") but `not_defensible` for archetype E, where
  invested capital and realized returns are not yet stabilized enough for a return-versus-cost-of-capital
  spread to be a meaningful signal.

This dispersion is not an artifact of matrix design — it follows directly from each family's own
governing theoretical assumption (a going-concern, earnings-producing, single-cash-flow-stream firm for
DCF and yield-screen families; a well-defined non-financial invested-capital base for ROIC; a liquid,
economically meaningful asset base for NAV) being satisfied by some archetypes and violated by others in
ways that are structural, not merely inconvenient. A future implementation applying a fixed, one-size
methodology to the full canonical roster — regardless of which family were chosen — would necessarily
misapply that method to at least one archetype represented among genuinely different business models.
**RQ1 is resolved: methodology selection must be archetype-conditioned**, consistent with how the
protocol's own falsification criteria (§8) are written in terms of family-archetype pairs, not families
in isolation.

A secondary, weaker observation supports the same conclusion: even where a family is `defensible` for
more than one archetype (e.g., family 5 relative valuation for both A and B), the *adjustment content* —
which multiple, which peer set, which normalization — differs by archetype in ways a single fixed
procedure could not encode without archetype-specific branching logic. Differentiation is required not
only at the family-selection level but, for a `defensible_with_adjustment` cell, at the adjustment-design
level too.

---

## 2. Candidate methodology families (recap, unedited from protocol §4)

| # | Short name |
|---|---|
| 1 | Asset-based / balance-sheet-adjusted approaches |
| 2 | Discounted Cash Flow — Free Cash Flow to the Firm (FCFF DCF) |
| 3 | Discounted Cash Flow — Free Cash Flow to Equity (FCFE DCF; DDM/excess-return variant for archetype C) |
| 4 | Earnings yield / free-cash-flow yield screens |
| 5 | Relative valuation / multiples |
| 6 | ROIC / reinvestment economics |
| 7 | Scenario / probability-weighted analysis |

## 3. Candidate archetype categories (recap, unedited from protocol §5)

| Code | Short name |
|---|---|
| A | Asset-light, recurring-revenue platform |
| B | Capital-intensive infrastructure / industrial |
| C | Financial intermediation / network economics |
| D | Commodity / cyclical |
| E | Early-stage / binary-outcome |
| F | Diversified / multi-segment |
| G | Mature, stable, diversified-revenue compounder |

No real company is assigned to any code above or anywhere in this document (protocol §3/§5/§12).

---

## 4. The 49-cell matrix

Closed four-value vocabulary per protocol §7: `defensible` (**D**) · `defensible_with_adjustment`
(**D+A**) · `not_defensible` (**ND**) · `insufficient_evidence_to_determine` (**IE**).

| Family \ Archetype | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1. Asset-based / NAV / SOTP | ND | D+A | D+A | D+A | D+A | **D** | ND |
| 2. FCFF DCF | **D** | D+A | **ND** | D+A | **ND** | D+A | **D** |
| 3. FCFE DCF (DDM/excess-return for C) | **D** | D+A | D+A | D+A | **ND** | D+A | **D** |
| 4. Earnings / FCF-yield screens | D+A | D+A | D+A | D+A | **ND** | D+A | **D** |
| 5. Relative valuation / multiples | **D** | **D** | D+A | D+A | D+A | D+A | **D** |
| 6. ROIC / reinvestment economics | D+A | **D** | D+A | D+A | **ND** | D+A | **D** |
| 7. Scenario / probability-weighted | D+A | D+A | D+A | **D** | **D** | D+A | D+A |

**Zero `insufficient_evidence_to_determine` cells were required.** Every one of the 49 cells resolves to
one of the other three values on citable, disclosed theoretical grounds (§4.1–§4.7 below); the abstention
value (protocol §9) remains available and would be used in preference to a forced guess if a future
charter amendment expanded the family or archetype lists into territory this literature review could not
support — it was not needed for the frozen 7×7 set.

### 4.1 Family 1 — Asset-based / balance-sheet-adjusted (NAV, adjusted book value, SOTP)

- **A — ND.** Governing assumption: the balance sheet captures the economically significant assets.
  Asset-light platforms derive most of their economic value from intangibles that accounting does not
  capitalize (network effects, customer relationships, internally generated software/IP, brand) —
  reported book value is structurally disconnected from the value driver. No adjustment converts a
  thin balance sheet into a meaningful net-asset estimate without effectively re-deriving an
  income-based value, which is a different family. Named incompatibility: book value is not a proxy for
  intangible-driven economic value (protocol §8's non-exhaustive-example standard).
- **B — D+A.** The physical asset base (plant, network, regulated infrastructure) is economically
  significant here, unlike archetype A. Adjustment required: raw historical-cost book value must be
  restated to replacement cost or regulatory asset base, since accumulated depreciation under
  historical-cost accounting diverges from current economic value, particularly for long-lived assets.
  Commonly used as a cross-check alongside DCF (family 2/3), not as the sole method.
- **C — D+A.** Adjusted (tangible) book value is a standard, literature-recognized valuation
  cross-check for financial intermediaries (price-to-tangible-book-value framing), because a bank's
  balance sheet — unlike an industrial company's — is close to its actual economic activity (loans,
  deposits, securities are themselves the business, not merely inputs to it). Adjustment required:
  raw book value must be marked for credit-quality (loan-loss provisioning adequacy) and off-balance
  sheet exposures before it is a meaningful base.
- **D — D+A.** Net-asset/replacement-cost valuation (e.g., proved-reserve or replacement-cost bases in
  extractive/commodity industries) is a recognized standard method. Adjustment required: reserve or
  replacement-cost values must themselves be computed at a normalized, not spot, commodity price
  assumption — otherwise the "asset value" simply re-imports the same cyclicality the method is meant
  to look through.
- **E — D+A.** Not the primary valuation method (it cannot capture pipeline/platform optionality — see
  family 7 below), but net tangible assets (principally cash and near-cash) provide a recognized,
  narrow downside/liquidation-floor cross-check for pre-commercial businesses, a disclosed and
  narrowly-scoped adjustment (explicit floor-value use only, not a primary-value claim).
- **F — D.** This is the archetype the family's own SOTP variant is built for: materially different
  segment economics are exactly the condition under which summing independently-derived segment values
  is standard and literature-preferred over a single blended method. No material adjustment beyond
  correct segment decomposition (which is the method's ordinary execution, not a caveat on top of it).
- **G — ND.** Classical critique of asset-based valuation: for a stable, diversified, earnings-producing
  compounder, net asset value systematically understates going-concern earning power because the
  balance sheet does not capture durable competitive advantage, brand, or accumulated intangible
  capital built through reinvested earnings rather than externally purchased assets. Named
  incompatibility: book value is not a proxy for a mature compounder's earning power.

### 4.2 Family 2 — FCFF DCF

- **A — D.** Canonical application: predictable, scalable unlevered cash-flow generation with a
  definable terminal state is exactly what FCFF DCF is designed to value. Caveat (not a disqualifier):
  terminal-value and long-run growth-durability assumptions carry outsized weight given long explicit
  or implicit forecast horizons — standard, well-documented DCF sensitivity, not an archetype-specific
  incompatibility.
- **B — D+A.** Applicable, but materially more sensitive than archetype A to the reinvestment-rate and
  terminal-growth assumptions, because near-term free cash flow is depressed by heavy ongoing capex
  during a buildout phase — the model must explicitly separate a high-reinvestment forecast period from
  a lower-reinvestment steady state, and get the transition timing right, rather than applying a single
  smoothed growth/reinvestment assumption throughout.
- **C — ND.** Named falsification example (protocol §8): unlevered operating free cash flow is not a
  coherent construct for a business whose financing activity — deposit-taking, loan origination,
  underwriting float — *is* the operating business, not a residual claim funded separately from it.
  There is no disclosed adjustment that preserves the FCFF construct's meaning here; the literature's
  response is a different method entirely (family 3's DDM/excess-return variant), not an adjusted FCFF.
- **D — D+A.** Standard method, but a trailing- or current-year cash-flow figure at a cyclical extreme
  is not representative — the model must be built on a mid-cycle or normalized cash-flow base rather
  than the latest reported figures, a named, disclosed, and structurally necessary adjustment.
- **E — ND (single-path).** Named falsification example (protocol §8): a single deterministic forecast
  path cannot represent a binary or highly bimodal outcome distribution without materially
  understating true uncertainty. A single-path FCFF DCF applied to a pre-commercial, approval-gated, or
  otherwise binary-outcome business systematically misstates the shape of the actual payoff
  distribution — this is a structural incompatibility with the family's single-path construction, not a
  parameter-tuning problem. (A probability-weighted *extension* of DCF — several explicit scenarios
  each individually discounted, then blended — is a different, defensible construction; that is family
  7, evaluated separately below, and is the literature-standard companion or alternative here.)
- **F — D+A.** A single, consolidated FCFF DCF using one blended WACC and one blended growth rate across
  materially different segment economics understates the dispersion between segments and can produce a
  misleading composite discount rate. Adjustment required: apply the method at the segment level (as a
  component of a sum-of-the-parts construction, family 1's archetype-F use) rather than to consolidated
  cash flows directly.
- **G — D.** The literature's stated default case (protocol §5's own archetype-G description): stable,
  diversified revenue, well-covered by comparables, with cash flows predictable enough that standard
  DCF mechanics apply without the archetype-specific adjustments required elsewhere in this row.

### 4.3 Family 3 — FCFE DCF (equity-level; DDM / excess-return variant for archetype C)

- **A — D.** Equity-level analogue of family 2's archetype-A cell; same predictable-cash-flow rationale
  applies, discounting levered free cash flow at a cost of equity rather than unlevered flow at WACC.
  Choice between FCFF and FCFE here is largely a matter of capital-structure stability (FCFE requires an
  assumption about the trajectory of debt issuance/repayment, an added assumption FCFF avoids by
  discounting before financing effects) rather than a difference in defensibility.
- **B — D+A.** Same reinvestment-rate/terminal-growth sensitivity as family 2's archetype-B cell, with
  the added requirement to model the debt-financing trajectory of the infrastructure buildout explicitly
  (since equity-level free cash flow is sensitive to the pace and terms of debt-funded capex, not just
  the capex itself).
- **C — D+A.** This is the archetype and adjustment the protocol's own text names directly (§4 family 3,
  §5 archetype C): plain FCFE is still not well-behaved for a financial intermediary (financing flows
  remain the business), but the family's own dividend-discount or excess-return/residual-income variant
  — built around return on equity versus cost of equity rather than a cash-flow residual — is the
  literature-standard response, precisely because it works at the equity level where deposit/loan flows
  are the natural unit rather than an operating-versus-financing split that doesn't exist cleanly for a
  bank. Disclosed adjustment: DDM or excess-return/residual-income substitution for plain FCFE.
- **D — D+A.** Same normalization requirement as family 2's archetype-D cell, applied to levered cash
  flow: mid-cycle or normalized earnings/cash-flow basis required, not a trailing snapshot.
- **E — ND (single-path).** Same structural incompatibility as family 2's archetype-E cell: a single
  deterministic equity-cash-flow path cannot represent a binary outcome distribution. Same resolution
  (probability-weighted extension = family 7) applies.
- **F — D+A.** Same segment-level-application requirement as family 2's archetype-F cell, at the equity
  level.
- **G — D.** Same default-case rationale as family 2's archetype-G cell; FCFF and FCFE are explicitly
  described in the protocol's own archetype-G text as "typically both applicable and mutually
  corroborating" for a mature, stable compounder — cross-checking one against the other is itself a
  standard practice here.

### 4.4 Family 4 — Earnings yield / free-cash-flow yield screens

- **A — D+A.** Usable as a first-pass sanity check (its stated role per protocol §4), but only once
  earnings or free cash flow are positive and reasonably stable — many asset-light platforms in a
  growth-investment phase report low or negative current earnings/FCF despite strong unit economics, in
  which case a yield screen understates or cannot compute a meaningful figure. Adjustment: apply once a
  stabilized-margin phase is reached, or substitute a forward/normalized-margin estimate rather than the
  trailing figure, with that substitution disclosed.
- **B — D+A.** Same issue as archetype A but driven by capex rather than margin phase: FCF yield is
  mechanically depressed during a heavy-reinvestment buildout period, understating normalized cash
  generation. Adjustment: normalize for the buildout-phase capex intensity before treating the yield as
  representative.
- **C — D+A.** Earnings yield (effectively an inverse P/E) is commonly and reasonably applied to banks;
  free-cash-flow yield specifically is distorted because "free cash flow" for a bank conflates deposit
  and loan-book movements with operating economics. Adjustment: use the earnings-yield form, not the
  FCF-yield form, for this archetype.
- **D — D+A.** A trailing-year earnings or FCF yield at a cyclical extreme materially misprices a
  commodity/cyclical business (the archetype's own protocol text names mid-cycle/normalized bases as
  literature-standard practice). Adjustment: compute the yield on a mid-cycle-normalized earnings/FCF
  base, never the latest reported figure alone.
- **E — ND.** Named falsification example (protocol §8): the screen structurally requires a positive,
  stable earnings or free-cash-flow base as its numerator, and a pre-commercial or approval-gated
  business does not yet have one. There is no adjustment that supplies a numerator the business does not
  yet generate; this is not a normalization problem like archetype D, it is an absence of the required
  input.
- **F — D+A.** A single consolidated yield blends segments with different margin/reinvestment profiles
  into one misleading figure. Adjustment: apply the screen at the segment level as a diagnostic
  component, not to the consolidated figure alone.
- **G — D.** Classic first-pass screen for a stable, mature earner with a representative trailing
  earnings/FCF base — the archetype this simplified method was designed around.

### 4.5 Family 5 — Relative valuation / multiples

- **A — D.** Comparable-company multiples (revenue- or subscription-metric-based multiples where
  earnings are not yet the most informative denominator, or EV/EBITDA once margins mature) are standard
  and widely used, conditional on a genuine peer set existing — a data-availability condition, not a
  theoretical incompatibility.
- **B — D.** EV/EBITDA and related multiples are industry-standard for capital-intensive/infrastructure
  businesses; unlike P/E, they are less distorted by differing depreciation and financing-policy choices
  across otherwise-comparable firms, which is exactly the distortion this archetype is prone to. No
  archetype-specific adjustment required beyond ordinary comparable-set diligence.
- **C — D+A.** Standard non-financial multiples (EV/EBITDA, EV/Sales) are not well-defined for financial
  intermediaries, because enterprise value itself is not a coherent construct when a firm's liabilities
  (deposits) are raw material rather than financing. Adjustment (named directly in the protocol's
  archetype-C text): use sector-specific multiples, principally price-to-book relative to
  return-on-equity, in place of enterprise-value-based multiples.
- **D — D+A.** Multiples computed on trailing, spot-cycle earnings or EBITDA materially mislead at
  cyclical extremes (a low trailing multiple at a cyclical peak looks cheap and is not; a high trailing
  multiple at a trough looks expensive and is not). Adjustment: apply the multiple to a mid-cycle or
  normalized earnings/EBITDA base, or use a through-cycle average multiple.
- **E — D+A.** A conventional earnings-based peer set is often unavailable (comparable companies may
  also be pre-revenue), but relative valuation is still practiced here in an adapted, non-earnings form —
  alternative comparability metrics (e.g., stage-adjusted or pipeline/asset-based multiples among
  similarly-staged peers) are a recognized, if wider-dispersion, adjustment. Not a structural
  incompatibility on the order of family 2/3/4/6's archetype-E cells, since the *comparison* logic
  itself remains valid even when the *metric* must change; disclosed adjustment required: substitute a
  non-earnings comparability metric appropriate to the development stage.
- **F — D+A.** A single blended multiple across materially different segments is a matter of decreasing
  precision, not structural incompatibility (unlike, e.g., family 2's archetype-C cell) — no governing
  assumption of the multiples method is violated by a diversified company, but the resulting figure
  blends divergent segment multiples into a less meaningful composite. Adjustment: apply multiples at
  the segment level as inputs to a sum-of-the-parts construction (family 1's archetype-F use) rather
  than to the consolidated figure alone.
- **G — D.** Classic application: a mature, diversified, well-covered compounder typically has a
  genuine, liquid comparable set, and multiples here are described in the protocol's own archetype-G
  text as typically corroborating DCF output rather than conflicting with it.

### 4.6 Family 6 — ROIC / reinvestment economics

- **A — D+A.** Directionally useful (capital-allocation quality matters for a platform business too),
  but the invested-capital denominator is frequently distorted for asset-light platforms because
  economically significant investments — R&D, customer-acquisition spend, some technology
  development — are expensed under standard accounting rather than capitalized, mechanically inflating
  ROIC by understating the capital base. Adjustment: capitalize and amortize R&D/customer-acquisition-type
  spend before computing invested capital, a disclosed, named, literature-recognized correction.
- **B — D.** Named directly in the protocol's own archetype-B text: ROIC-versus-cost-of-capital framing
  is "often a necessary companion, not merely a nice-to-have" for capital-intensive infrastructure,
  precisely because reinvestment-rate and return-durability assumptions are the dominant driver of
  long-run value here. No archetype-specific adjustment beyond correct capitalization of the (already
  substantial, already-capitalized) physical asset base.
- **C — D+A.** "Invested capital" is not a well-defined non-financial concept for a financial
  intermediary — capital itself is the intermediary's raw material, not an input funding a separate
  operating asset base. Adjustment: substitute the archetype-specific analogue, return on equity versus
  cost of equity, for return on invested capital versus WACC — structurally the same economic-profit
  logic, applied at the equity/regulatory-capital level rather than the enterprise level, consistent
  with family 3's own archetype-C excess-return variant.
- **D — D+A.** ROIC computed on spot-cycle earnings mechanically swings with the commodity cycle exactly
  as the raw yield-screen and multiple metrics do (families 4/5's archetype-D cells) — the same
  normalization requirement applies: compute the return on a mid-cycle or normalized earnings base, not
  the latest reported figure.
- **E — ND.** The framework presumes a stabilized invested-capital base producing a measurable, durable
  return; a pre-revenue or negative-return business has neither a meaningful realized return nor a
  reinvestment rate that reflects durable economics (early capital deployment here is closer to a
  real-option premium than a return-generating investment in the family's sense) — a structural
  precondition failure, the same class of incompatibility as families 2/3/4's archetype-E cells, not a
  parameter-adjustment problem.
- **F — D+A.** Consolidated ROIC blends segments with different capital intensity and return profiles
  into a single, less informative figure. Adjustment: decompose to segment-level ROIC, mirroring the
  sum-of-the-parts logic already required for families 1/2/3/4/5 at this archetype.
- **G — D.** Standard, well-behaved application: a mature compounder with a stabilized, well-defined
  invested-capital base is exactly the setting economic-profit/ROIC-spread analysis is designed for.

### 4.7 Family 7 — Scenario / probability-weighted analysis

- **A — D+A.** Not strictly necessary given archetype A's comparatively predictable economics (a
  well-specified base-case DCF is often already adequate), but useful as a supplementary robustness check
  against terminal-value and growth-durability uncertainty — the same sensitivities family 2/3 already
  flag for this archetype. Adjustment/role: supplementary, not the primary method.
- **B — D+A.** Useful given reinvestment-rate and regulatory/demand-cycle uncertainty during a buildout
  phase, again as a supplement to, not a replacement for, the primary DCF/ROIC combination this archetype
  already calls for.
- **C — D+A.** Scenario framing over credit-cycle and regulatory-capital outcomes (stress-scenario-style
  bands) is a recognized, well-established practice for financial intermediaries specifically, given
  regulatory stress-testing's own use of exactly this technique — useful as a disclosed supplement to the
  DDM/excess-return primary method, not a replacement for it.
- **D — D.** A first-order, standard practice for commodity-linked cyclicals, not merely a supplementary
  check: explicit bull/base/bear commodity-price-path scenarios, each carried through the full valuation
  and blended by disclosed probability weights, is the literature-standard way to represent commodity-
  price uncertainty directly, rather than compressing it into a single "mid-cycle" point assumption. This
  is the named, necessary companion to the normalization adjustment required in families 1/2/3/4/5/6's
  archetype-D cells.
- **E — D.** The archetype and family the protocol's own text points to directly (§5 archetype E, §8's
  falsification logic for families 2/3/4/6): a single-path forecast cannot represent a binary or highly
  bimodal outcome distribution without materially understating uncertainty, and explicit
  probability-weighted scenarios are named as the literature-standard alternative or necessary companion
  for exactly this reason. This is the strongest, least-qualified fit in the entire matrix.
- **F — D+A.** Scenario-weighting each segment's own outcome distribution can supplement a sum-of-the-
  parts construction, but it is not itself the structural solution to multi-segment diversity (that
  remains family 1's SOTP decomposition) — useful as an added-uncertainty layer on top of, not instead
  of, segment-level decomposition.
- **G — D+A.** Useful as a sensitivity/robustness supplement to the "default case" DCF/multiples
  combination, but not load-bearing here — base-case forecasting is generally reliable enough for a
  mature, stable, well-covered compounder that scenario weighting adds robustness rather than resolving a
  structural gap the primary methods leave open.

---

## 5. RQ2 — Methodology defensibility and data-requirement summary

Consolidated from §4.1–§4.7, each family's governing assumption, principal data requirement, and
literature-documented failure mode:

| Family | Governing assumption | Principal data requirement | Documented failure mode when assumption violated |
|---|---|---|---|
| 1. Asset-based/NAV/SOTP | Balance sheet approximates economic value of the relevant assets | Segment/asset-level book or replacement-cost data | Systematically undervalues intangible-/earning-power-driven businesses (archetypes A, G) |
| 2. FCFF DCF | A single, coherent, forecastable unlevered operating cash-flow stream exists | Multi-year cash-flow forecast, WACC components, terminal-value basis | Incoherent construct where financing flows are the business (C); single path cannot represent bimodal outcomes (E) |
| 3. FCFE DCF (DDM/excess-return for C) | A single, coherent, forecastable levered (or equity-return) cash-flow stream exists | Multi-year equity cash-flow or ROE/cost-of-equity forecast | Same single-path limitation as family 2 (E); requires the DDM/excess-return substitution to remain coherent for C |
| 4. Earnings/FCF-yield screens | A positive, stable current earnings or FCF base exists | Trailing or normalized earnings/FCF figure | No numerator exists pre-profitability/pre-revenue (E); misleads at cyclical extremes without normalization (D) |
| 5. Relative valuation/multiples | A genuine, economically comparable peer set exists | Peer-company multiples, comparable metric definitions | Enterprise-value-based multiples ill-defined for intermediaries (C); blended multiples understate segment dispersion (F) |
| 6. ROIC/reinvestment economics | A well-defined, stabilized invested-capital base with a measurable return exists | Invested capital, NOPAT/return figures, cost of capital | Not meaningful pre-stabilization or pre-positive-return (E); "invested capital" ill-defined for intermediaries (C) |
| 7. Scenario/probability-weighted | Multiple discrete, disclosed, probability-weighted outcome paths can be specified | Scenario definitions, per-scenario cash-flow/return paths, disclosed probability weights | Not itself a primary valuation method — depends on an underlying method (DCF, ROIC, etc.) applied per scenario |

No family is disqualified in the abstract; each is disqualified, qualified, or unqualified only in
combination with a specific archetype's governing economics, which is the direct evidentiary basis for
the RQ1 finding above.

---

## 6. RQ3 — False-precision-prevention specification

This section elaborates protocol §10's five requirements into a concrete specification a future,
separately authorized application phase must satisfy. None of this is executed here — no company is
valued under this specification; it defines what a future implementation would be required to do.

1. **Mandatory range output, never a single point.** Any `defensible`/`defensible_with_adjustment`
   application must report a low/base/high range (or, for a scenario-weighted application per family 7,
   the full disclosed scenario set rather than a single blended point) with the specific governing
   assumption(s) driving the width of that range named explicitly — e.g., for a family 2/3 DCF, the
   discount-rate and terminal-growth-rate range that produces the value range; for a family 5 multiple,
   the peer-set dispersion driving the multiple range.

2. **Mandatory, per-input, provenance-labeled assumptions ledger.** Every governing assumption —
   discount rate/WACC derivation, growth rate, terminal-value method, peer-set membership and its
   inclusion/exclusion rationale, cycle-normalization basis, scenario probability weights — must carry
   one of exactly four provenance labels, extending `NUM-0001`'s existing provenance-classification
   discipline (already governing this repository's other consequential numeric parameters, e.g. the 1.8x
   leverage cap and 30% buffer floor) into this new domain:
   - `market_derived` — taken directly from an observable, current market input (e.g., a risk-free rate
     from an observable yield, a peer multiple from observable trading prices).
   - `historically_observed` — taken from a company's or industry's own historical financial record
     (e.g., a historical reinvestment rate, a historical margin trajectory).
   - `analyst_consensus_cited` — taken from a disclosed, named third-party consensus source, cited as
     such and not represented as an independently-derived figure.
   - `assumed_for_illustration` — a judgment input with no market or historical anchor, disclosed
     explicitly as an assumption rather than a fact, with the reasoning behind the chosen value stated.

   An assumption with no label attached is not a valid output under this specification — the label is
   mandatory, not optional metadata.

3. **No fabricated precision.** Output precision (decimal places, percentage-point granularity) must be
   bounded by the precision the underlying evidence and assumptions actually support. A range disclosed
   to the nearest whole percent or the nearest broad dollar band is a complete, correct output; a range
   disclosed to two decimal places on inputs that are themselves order-of-magnitude estimates is a
   defect, not added rigor, per protocol §10's own framing ("a wide, honestly-disclosed range is a
   correct and complete output, not a failure of rigor").

4. **First-class abstention path at the company-application level.** Mirroring §9's family/archetype-level
   abstention rule, a future application phase must carry an equivalent company-level abstention outcome
   (structurally comparable to `TIER-0002`'s `unable_to_determine` axis value and `XASSET-0002`/
   `XASSET-0005`'s forced-abstention readiness fields already in production in this repository) for a
   case where available evidence is insufficient to support even a wide range — never a forced numeric
   output when the honest answer is "cannot be determined from available evidence."

5. **No opaque scoring or composite index, at any point, under any future extension.** No
   machine-learning-derived valuation, weighted composite index, or single blended "score" across
   methodology families is permitted — every output must remain fully inspectable and traceable to a
   named, cited method and its own disclosed assumptions ledger. This is a permanent, not merely
   present-phase, restriction under this charter (protocol §10, §17).

**Archetype-specific elaborations, drawn directly from the §4 matrix, that a future application phase
must additionally observe:**

- For archetype D (commodity/cyclical) applications, the mid-cycle/normalization methodology itself
  (the number of years averaged, the source of the normalized-price assumption) must be disclosed as its
  own named assumption, not folded silently into a "normalized EBITDA" figure presented as if it were an
  observed fact.
- For archetype E (early-stage/binary) applications, every scenario's probability weight must itself
  carry a provenance label under item 2 above — an undisclosed or unlabeled probability weight
  reintroduces exactly the false precision this specification exists to prevent, only relocated from the
  cash-flow forecast into the scenario weighting.
- For archetype C (financial intermediation) applications, regulatory capital and credit-normalization
  assumptions (loan-loss provisioning adequacy, regulatory capital ratio targets) must be disclosed with
  the same rigor as a discount-rate assumption — they are governing assumptions of the method, not
  incidental inputs.
- For archetype F (diversified/multi-segment) applications, a segment-level sum-of-the-parts output must
  disclose each segment's own range and assumptions ledger separately, not only the summed total — an
  aggregate range that hides offsetting segment-level uncertainty is itself a form of false precision.

---

## 7. RQ4 — Evidence-sufficiency finding

**Finding: this repository's existing governed Company Intelligence schema (`docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24) does not structurally capture the quantitative inputs any of
the seven candidate methodology families requires. It does capture several of the qualitative,
narrative-evidence categories a future application phase would still need. A future application phase
requires additional, separately-governed evidence categories not currently collected.**

This finding is based solely on reading the frozen schema's own field list (§9) structurally — it does
not reference, quote, or rely on any individual company's actual field content, consistent with the
protocol §6 evidence boundary.

**What the existing schema structurally provides** (§9 field list): `sector`/`industry` (coarse
classification, potentially informative for archetype triage — e.g., a "Financials" sector tag is
suggestive of archetype C — but not a substitute for a deliberate, disclosed archetype-fit judgment);
`competitive_advantages[]` (freeform narrative, potentially informative for growth-durability and
terminal-value judgment in DCF families, but not structured or quantified); `risks[]` and `catalysts[]`
(narrative, dated, with a severity/status field — potentially informative as qualitative inputs to
scenario construction under family 7, or to a risk-premium judgment, but not a quantitative
scenario-probability input on their own); the freeform thesis Markdown's informally-recommended
"valuation-concerns section" (§10, not enforced by any validator — narrative only, no structured
figures).

**What the existing schema structurally does not provide, for any of the seven families:**

- **No financial-statement or time-series data field of any kind.** The §9 schema has no field for
  revenue, margin, EBITDA, free cash flow, capital expenditure, invested capital, debt, share count, or
  any other quantitative financial figure, current or historical. Every family (1 through 6 directly;
  family 7 indirectly, since it blends per-scenario applications of the others) requires at least one
  such quantitative time series or point figure as its principal data requirement (§5's table above).
- **No discount-rate, cost-of-capital, or peer-set field.** Families 2, 3, 5, and 6 each require an
  explicit discount rate, cost-of-capital estimate, or comparable-peer-set definition; none of these has
  a structural home in the frozen schema.
- **No scenario or probability-weighting field.** Family 7 requires disclosed, named scenario
  definitions and probability weights; the schema's `risks[]`/`catalysts[]` fields are narrative and
  dated but carry no probability-weighting or scenario-blending structure.
- **No archetype-fit field.** The schema's `portfolio_role_ref` (§14 of the spec, cited by the protocol
  as explicitly out of scope for this study) stores a tier/category label for allocation purposes, not
  a valuation-archetype classification — the two are stated in this repository's own governance record
  to be deliberately distinct and non-substitutable (this protocol's own §5 states the archetype
  taxonomy "is deliberately distinct from... `ONTO-0001`," and by the same logic is distinct from
  `portfolio_role_ref`, which the protocol also independently bars from use as a research input, §3).

**Consequence.** A future, separately authorized application phase — which this report does not
authorize, begin, or scope beyond identifying the gap — would need at minimum one new, separately
governed evidence category capturing structured financial-statement and valuation-input data (a
quantitative counterpart to the existing narrative-only Company Intelligence schema), plus a mechanism
for disclosing and provenance-labeling the assumption inputs specified in §6 above. Designing that
evidence category is explicitly out of scope for this protocol (protocol §11.2, §12, §19) and is not
attempted here; this finding only identifies that the gap exists and characterizes its shape.

---

## 8. Limitations

- **This report is a closed-matrix literature comparison, not an empirical study.** It draws on
  established, citable corporate-finance and equity-valuation concepts, cited generically per protocol
  §6, and does not claim the completeness of a full academic literature review; it claims only that each
  cell's disposition follows from a named, standard, citable theoretical principle, per the
  reproducibility standard in protocol §13.
- **The seven-family and seven-archetype taxonomies are closed by charter (protocol §4/§5/§17).** A
  business model that does not cleanly fit one archetype, or a methodology family not among the seven
  listed, is out of scope for this report and would require a charter amendment to address — this is a
  disclosed boundary, not a claim that the taxonomies are exhaustive of all valuation practice.
- **No cell in this matrix is, or should be read as, a claim about any real company.** Even where a
  matrix cell is unqualified `defensible` for an archetype that might describe a familiar kind of
  business in the abstract, no inference back to any actual canonical-roster ticker is licensed by this
  report — that inference (archetype-category assignment of a real company) is explicitly prohibited by
  protocol §12 and is not performed here, in this section or anywhere else in this document.
- **This report does not resolve, close, or shorten `TIER-0009` §K's `valuation_required` status** on
  `target_and_range` or `maximum_position_size` for any of the 27 canonical equities. That determination
  requires its own later, separate, independently reviewed governance decision, informed by but not
  automatically triggered by this report (protocol §11.2, §15).
- **RQ4's evidence-sufficiency finding is structural, not a design proposal.** This report identifies
  that a quantitative evidence category is missing; it does not design, name, or scope that category's
  schema, storage location, or governance path — that remains fully unauthorized future work.
- **This report authorizes no methodology selection or adoption.** Per protocol §15, even a complete,
  well-reasoned matrix with every cell resolved does not itself select or adopt a methodology, family or
  archetype-differentiated set, for use against any real company.

---

## 9. Compliance statement (protocol §11.2 / §12 / §19)

This report contains: no fair value, price target, expected return, ranking, or buy/sell/hold/trim/exit
signal for any company; no new or modified Company Intelligence record; no archetype-category assignment
of any real, named canonical-roster company; no historical backtest of any methodology's output against
subsequent stock-price performance, under any framing; no chart, technical-indicator, or
screenshot-derived input of any kind; no consumption of any Company Intelligence record's actual field
content, `conviction.rating`, `portfolio_role_ref`, or any `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml` field value as a research input; no target, tier, cap, gate, cluster,
allocator, margin, or ladder change or recommendation; no ETF, cryptocurrency, GLD, cash/reserve, or
debt-reduction valuation or economic-assessment methodology content of any kind; no claim that
`TIER-0009`'s `target_and_range`/`maximum_position_size` `valuation_required` status is resolved, closed,
or ready to be revisited. This report requires independent review (per `OPS-0007` §1's twelve-point
capability-based standard, protocol §16) before any of its content may be cited as evidence in a future
governance decision.
