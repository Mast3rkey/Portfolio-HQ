---
decision_id: PI-0020
date: 2026-07-22
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0003, PI-0004, PI-0006, PI-0007, PI-0009, PI-0016, PI-0018, PI-0019, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0019-gev-committee-review-authorization.md`
authorized bounded, research-only Investment Committee review activity on
GEV under `PI-0016`'s standing methodology, naming ETN/VRT/PWR — the other
current-holding members of the governed `power_infra` cluster — as the
fixed comparator set. That review has now been conducted and produced a
review packet stating both of `PI-0016`'s required, independent
recommendations: an **advisory policy recommendation of "Keep current
policy"** and an **Intelligence-maintenance recommendation of
"Intelligence refresh recommended."** Per `PI-0016`/`PI-0019`'s own
lifecycle, a review packet's findings are not self-executing — acting on
the Intelligence-maintenance recommendation requires its own separate,
later, filed governance authorization before any implementation may
begin. This decision is that separate authorization.

**Provenance of the evidentiary basis, stated precisely.** The human
principal supplied exactly one external artifact directly to this session
as a local file attachment:

- `GEV_committee_review_packet_20260722_principal_ready_v4.md` — the
  canonical, corrected (v4) GEV committee-review packet, SHA256
  `e3d3325e8ccbc507f304e1ef834bcc176f1d2d7291276ab2c40c95fba9280a00`,
  independently computed in full by this session and matching the
  principal-identified expected value exactly.

This session then performed the packet's **final independent acceptance
audit itself, from first principles, in this same session** — not relying
on any prior session's verdict or the packet's self-certifications —
covering: artifact identity; repository authority (origin/main and local
HEAD both at `cfb39b516a6ebc0e2f2ed8e7e040775d22e00a1a`, clean tree, no
open PRs, no overlapping GEV/power_infra workstream); PI-0016/PI-0019
`Accepted` status; all 13 repository-fact reconciliation rows re-verified
directly against `targets.yaml`, `holdings.yaml`, and
`intelligence/companies/`; the full mechanical ledger recount (51
detailed blocks, 13 REPO IDs, 11 UNRES IDs, 75 unique IDs, 6 open / 4
resolved / 1 retired, zero duplicates, zero unresolved citations, no
comparator rank-ordering language); and fresh, independent external
corroboration of the packet's corrected Q2 2026 Wind-commentary treatment
(the approximately $400M FY2026 Wind EBITDA-loss guide maintained at the
Q2 call; the $275M Q2 loss described by CFO Ken Parks as in line with
expectations; Q3 Wind EBITDA guided approximately break-even; first-half
losses expected to be partially offset by second-half profitability; no
specific positive-H2 dollar amount guided — all located again through
multiple independent secondary outlets in this session, with direct
primary-transcript access still HTTP 403-blocked, consistent with the
packet's ACCESS-01 record and its secondary-reported classification).
The audit returned **READY FOR PRINCIPAL REVIEW** with zero findings.

The human principal then explicitly approved both of the packet's
conclusions in this session: **"Keep current policy"** (advisory) and
**"Intelligence refresh recommended"** (Intelligence-maintenance). The
first conclusion requires no change and none is made — GEV remains T1 at
its 3.35% per-name target with its existing `power_infra` cluster
membership, exactly as `targets.yaml` already encodes. This decision acts
on the second conclusion only.

The packet's seven prior superseded artifacts (v0 through principal-ready
v3) were not supplied to this session and are not relied on; the v4
packet attests their preservation at reported hashes in its §13, and the
v4 artifact alone — audited as above — is the evidentiary basis here. No
copy of any packet artifact is added to this repository by this decision,
consistent with `PI-0018`'s convention that a review packet's narrative
lives outside `intelligence/` while its authorized recommendations are
what a downstream governance filing acts on.

## Decision

**PI-0020 authorizes exactly one thing: a later, separate, bounded
implementation refresh of `intelligence/companies/GEV.yaml` and `GEV.md`,
evidence-content only, on its own future branch and PR.** This decision
itself changes neither file. It does not authorize any change to GEV's
tier, target, holdings, roster, cluster, cap, allocator, or margin
behavior, and it does not authorize a conviction-rating change.

### A. Why a refresh is authorized

The packet, reconciled against the existing record per `PI-0016`/
`PI-0013`'s gate and re-verified by this session's own audit, identifies
specific, dated gaps between `GEV.yaml`/`GEV.md` (evidence base ending at
Q1 2026) and the company's current disclosed state, on the packet's §9
three-track split:

1. **Genuinely new Q2 2026 evidence is absent.** Q2 2026 results
   (reported 2026-07-22): revenue $11.1B (+22% YoY), orders $24.2B (+88%
   organic), total backlog $176B, GAAP diluted EPS $2.47, adjusted EBITDA
   $1.25B (11.3% margin), free cash flow $5.107B; raised FY2026 guidance
   (revenue $45.5–46.5B, FCF $11.5–12.5B); segment actuals
   (Electrification orders $6.3B/+66% organic, book-to-bill ~1.7,
   equipment backlog $40.6B; Power orders $16.7B/+134% organic, gas
   backlog+slot reservations 100GW→116GW); the Q2 10-Q's total-debt
   ($2.6B excluding finance leases) and current tariff ($100M–$200M net
   for 2026) disclosures; and the Q2 earnings-call Wind commentary (the
   ~$400M FY2026 Wind-loss guide maintained; $275M Q2 loss in line with
   expectations; Q3 Wind EBITDA ~break-even; H1 losses expected partially
   offset by H2 profitability; no positive-H2 dollar amount guided).
2. **Older established facts were never captured by the record.** The
   dividend doubling to $0.50/share quarterly and the buyback-
   authorization increase from $6B to $10B (announced 2025-12-09); the
   Prolec GE acquisition closing (remaining 50%, $5.275B, 2026-02-02)
   and its $2.6B senior-notes financing (closed 2026-02-04); the Q1-set
   ~$400M FY2026 Wind-loss guide and the Q1 tariff estimate
   ($250M–$350M, now superseded) as record history. This session
   confirmed directly that the existing record contains no mention of
   Prolec, the dividend action, or the buyback action.
3. **The Q2 Wind development is consistent with one of the record's own
   enumerated unscheduled-review triggers** — "a material further
   deterioration in Wind or European Electrification margins" (Q2 Wind
   margin -13.6% vs. -7.3% a year earlier) — verified by this session
   against `GEV.md`'s five-trigger list. The capital-allocation
   developments are material omitted evidence supporting record currency
   but are not themselves a listed trigger, exactly as the packet's
   corrected §10b states. The record's `next_due` (2026-10-16) has not
   lapsed; this is a material-content trigger, not a staleness one.

### B. Distinguishing the stages (do not conflate)

Per the same lifecycle discipline as `PI-0018` §B:

1. **Committee review completion** — done: the v4 packet.
2. **Independent acceptance audit** — done, in this session: READY FOR
   PRINCIPAL REVIEW, zero findings.
3. **Principal approval of both conclusions** — done, in this session.
4. **Governance authorization** — this decision (`PI-0020`), filed now.
   Authorizes the refresh scope below; performs no refresh itself.
5. **Later implementation** — not yet begun. Requires its own branch and
   PR per §G below.
6. **Validation and merge** — not yet reached. Requires the §F validation
   suite before merge; this filing does not itself authorize merging that
   future PR.

### C. Authorized refresh scope

A later, separate implementation PR may refresh, within
`intelligence/companies/GEV.yaml` and `GEV.md` only, evidence-based
content limited to:

- the newly reported financial period (Q2 2026 and any subsequent
  reporting cycle current at implementation time);
- financial-quality and balance-sheet evidence (revenue, orders, backlog,
  segment results, margins, EPS, adjusted EBITDA, free cash flow, cash,
  total debt, raised guidance);
- capital-allocation evidence (the December 2025 dividend and buyback
  actions; the Prolec GE closing and its senior-notes financing);
- Wind-segment evidence, including the Q2 call's maintained ~$400M
  FY2026 loss guide and quarterly Wind outlook, subject to the mandatory
  provenance labeling in §D;
- tariff-exposure evidence (the current $100M–$200M net estimate,
  superseding the Q1 $250M–$350M estimate, retained as history);
- observable thesis-break conditions (updated factual status only, not a
  redefinition of the existing qualitative framework);
- the source ledger and disclosed access limitations;
- review dates and provenance (`review.last_reviewed`, `review.next_due`,
  `review.log`, consistent with the existing Company Intelligence
  schema).

No other section of the schema, and no other file, is in scope.

### D. Evidence-standard requirement for implementation

The later implementation must use **current primary sources wherever
accessible** (GE Vernova investor-relations materials; SEC filings and
exhibits; official earnings materials or transcripts; repository-
authoritative files for any governed portfolio fact restated in the
refreshed record), with secondary sources retained only when clearly
classified as secondary and only when primary access remains unavailable
at implementation time. Every material claim carried into the refreshed
record must retain (or newly assign) an explicit classification —
established fact, management claim, third-party claim, committee
inference, or unresolved uncertainty — per `PI-0016` and the packet's own
§11 ledger discipline. Three packet-specific obligations bind the
implementation:

1. **The Q2 earnings-call Wind commentary must carry secondary-reported
   provenance labeling** ("management commentary reported through
   secondary sources") unless the official transcript, webcast replay, or
   prepared remarks are directly inspected first — the exact condition
   the packet's GEV-Q2-10 entry sets. If primary access is available at
   implementation time where it was not during research, the
   implementation must prefer it.
2. **Committee arithmetic must stay labeled as such.** The approximately
   $657M cumulative H1 2026 Wind losses and approximately $257M implied
   positive H2 Wind EBITDA are committee arithmetic from company-reported
   inputs, not company guidance; the Q4-concentration reading is
   committee inference. If carried into the record, these labels carry
   with them. The record must not state or imply that the company guided
   to any dollar amount of positive H2 Wind EBITDA.
3. **The packet's §9.C exclusion list is binding.** The following must
   not enter the refreshed record: the Barclays/Siemens Energy peak-cycle
   argument (date conflict, methodology never inspected); any
   GAAP-EPS-versus-consensus comparison (basis compatibility unproven);
   insider-selling reports (no primary confirmation); the May 2026
   permitting commentary (unresolved secondary paraphrase, until its
   primary wording is inspected); unverified customer-concentration
   percentages; turbine-market-share figures (methodology uninspected);
   any share-price-reaction observation. Unresolved items disclosed in
   the packet (UNRES-01, -02, -04, -07, -08, -10) must not be silently
   resolved or silently dropped — either confirm them against a primary
   source or retain their unresolved status.

### E. Explicit prohibitions

The later implementation must not, under any interpretation:

- change GEV's T1 tier or its 3.35% per-name target in `targets.yaml`;
- change `holdings.yaml`, the portfolio roster, any cluster membership,
  or any cluster cap (including the `power_infra` cluster GEV belongs
  to);
- change `allocate.py`, `margin_state.py`, or any margin or allocator
  behavior;
- change any other company's or theme's Company/Theme Intelligence record
  (including the `ai_infrastructure` theme record GEV references, and any
  ETN/VRT/PWR material — no comparator record exists and none is
  authorized);
- propose, imply, or execute any trade or execution instruction;
- change `intelligence_validator.py`, `intelligence_report.py`, or any
  other production module beyond the two named content files;
- amend `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/INVESTMENT_ONTOLOGY.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.

**`conviction.rating: Medium` is the authorized baseline and must be
preserved as-is by the refresh.** A conviction-rating change is not
authorized by this decision and must never be inferred merely from
refreshing evidence — the packet's own advisory policy recommendation,
approved by the principal, is "Keep current policy," and `PI-0004`'s
closed four-value vocabulary governs any future rating regardless. If a
future human reviewer separately concludes that the rating itself should
change, that change requires its own separate, explicit human approval —
it may not be made silently inside the refresh this decision authorizes.

No computed or derived conviction value, ranking, score, portfolio
aggregation, or allocator coupling of any kind is authorized by this
decision, consistent with `PI-0016` and `ONTO-0001`'s unchanged boundary.

### F. Required implementation validation (before merge)

The later implementation PR must pass, and its description must record
the exact results of:

1. **`intelligence_validator.py`** run against the refreshed `GEV.yaml` —
   must pass with zero errors.
2. **Focused, relevant tests** covering Company-Intelligence validation
   paths in the existing test suite.
3. **The full applicable test suite** — must pass in full, not merely the
   focused subset.
4. **YAML parse validation** of the refreshed `GEV.yaml` (a clean
   `yaml.safe_load` or equivalent, independent of the validator's own
   schema checks).
5. **`git diff --check`** against the implementation branch, confirming
   no whitespace errors.
6. **An exact protected-path and scope review** — a diff enumeration
   confirming the only files changed are
   `intelligence/companies/GEV.yaml` and `intelligence/companies/GEV.md`,
   and confirming, by name, that `targets.yaml`, `holdings.yaml`,
   `allocate.py`, `margin_state.py`, every other Company/Theme
   Intelligence record, `intelligence_validator.py`, and
   `intelligence_report.py` are unchanged.

### G. Branch and PR

The later implementation must occur on its **own narrow branch**, separate
from this governance decision's branch, and must open its **own PR** —
this decision's PR does not carry the refresh's implementation.

### H. This decision performs no Intelligence refresh

Filing and accepting `PI-0020` changes no byte of
`intelligence/companies/GEV.yaml` or `GEV.md`. It authorizes scope,
sourcing standard, and validation requirements for a future, separate
implementation only.

### I. Append-only governance history

This decision adds one new file and one new `governance/decisions.yaml`
row. No existing decision file, index row, or `CLAUDE.md` Decisions Log
entry is edited or removed by this filing.

## Rationale

Same discipline `PI-0017`→`PI-0018` established for the first review
filed under `PI-0016`: a completed, audited review is one governance
event, and authority to implement what it recommends is a separate,
later, filed decision. `PI-0016`/`PI-0019` deliberately split "Keep
current policy" from "Intelligence refresh recommended" as two
independent conclusions precisely so a correct tier/target can coexist
with a record that independently needs newer evidence — this decision is
the authorization that lets the second conclusion be acted on without
touching the first.

The three packet-specific §D obligations (secondary-reported labeling for
the Q2 call commentary, committee-arithmetic labeling, and the §9.C
exclusion list) exist because they were the substance of the packet's own
final correction cycle — the v4 revision's whole point was getting the
provenance and arithmetic-attribution boundaries exactly right, and an
implementation that dropped those labels while copying the content would
undo the correction the audit process paid for.

Preserving `conviction.rating: Medium` as an explicit baseline follows
`PI-0018`'s precedent and `PI-0004`'s closed-vocabulary discipline:
refreshing evidence is not evidence of a conviction change, and the
packet's approved advisory recommendation is "Keep current policy," not a
rating change.

## Alternatives Considered

- **Treat the packet's recommendation plus the principal's chat approval
  as sufficient authorization to implement the refresh directly.**
  Rejected: `PI-0016`/`PI-0019` are explicit that review findings are not
  self-executing; the `PI-0018` pattern requires a filed,
  repository-auditable authorization, which is what this decision
  supplies — the chat approval is its basis, this filing is its record.
- **Fold conviction-rating reconsideration into this authorization.**
  Rejected: the approved advisory recommendation is "Keep current
  policy"; a rating change needs its own explicit human approval.
- **Authorize a broader refresh scope** (wholesale thesis-narrative
  revision). Rejected: the packet's findings are evidence-and-currency
  gaps, not a thesis reversal — the authorization stays proportional to
  what was actually found.
- **Commit the review packet (or its supersession chain) into the
  repository as a supporting artifact.** Rejected: `PI-0018` established
  the convention that review-packet narratives remain external; the
  packet's identity is pinned here by its independently computed SHA256
  instead.
- **Skip re-verifying the packet's mechanical counts and Wind-commentary
  corroboration and rely on its self-reported validation summary.**
  Rejected: this repository's standing "verify before acting on external
  review" guardrail required this session to recount the ledger,
  re-verify the repository facts, and independently re-locate the Q2 call
  commentary — all of which it did before the verdict this decision
  rests on.

## Consequences

**Changes:** `governance/decisions.yaml` gains one new row for `PI-0020`.
`CLAUDE.md`'s Decisions Log gains one short pointer entry.

**Does not change:** `intelligence/companies/GEV.yaml`, `GEV.md`, any
other Company or Theme Intelligence record, `targets.yaml`,
`holdings.yaml`, any tier, target, roster, cluster, or cap,
`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, `constitution/INVESTMENT_CONSTITUTION.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, any
existing governance decision file, or any trade/execution state.

**Enables:** a future, separate, narrowly-scoped implementation PR,
subject to the sourcing standard and packet-specific obligations (§D),
prohibitions (§E), and validation requirements (§F) above, and its own
separate merge decision.
