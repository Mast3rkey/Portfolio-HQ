---
decision_id: PHQ-2026-08
date: 2026-09-18
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, NUM-0001, PHQ-2026-01, PHQ-2026-02, PHQ-2026-07]
supporting_artifact: issuer_lookthrough.yaml
---

## Context

The current-architecture validation filed in PR #397 established, from the
committed configuration alone, that the retained common-driver measurement in
`issuer_lookthrough.yaml` is **internally inconsistent with its own source
table**. The retained headline reads `40.0284%`. Recomputing the same
look-through over the same eleven governed issuers, on the same canonical
target-weight basis, through the same production helper (`allocate._issuer_exposure`)
produced `41.6454%` at that snapshot's configuration — a `+1.6170pp` gap.

That gap is **not** configuration drift. The retained evidence package's own
per-issuer line items sum to the recomputation exactly. What does not
reconcile is the retained *headline* against the retained *table*. The headline
is arithmetically consistent with having summed only a subset of the governed
issuers' effective exposure — specifically, with the ETF-embedded components of
`LLY`, `TSLA` and `AAPL` omitted. `AAPL` is the decisive case: it carries no
direct canonical target at all, so its entire governed exposure is
ETF-embedded. Omitting embedded components silently removes `AAPL` from the
measurement in full while leaving it nominally "a governed issuer."

Two questions therefore stood open, and both were unanswerable from the
committed record alone:

1. **Which measurement is the rule?** No accepted decision stated whether the
   common-driver ceiling is measured over full effective exposure or over some
   narrower quantity. `allocate.py` implements one answer; the retained headline
   is consistent with a different one. The 40% ceiling was being enforced
   against a figure whose definition was undetermined.

2. **Are the constituent weights current?** Every `fund_holding_weight` in
   `issuer_lookthrough.yaml` was inherited from the `PHQ-2026-01` due-diligence
   package (measured 2026-07-30) at two-decimal-percent precision, with no
   recorded publisher, as-of date, or evidence hash. The file's own header
   already required refresh "at each quarterly review," and that window had
   passed.

This decision is the principal's authority for both, granted explicitly and
recorded here.

## Decision

The principal authorizes the following, and nothing beyond it.

### PD-1 — Authoritative common-driver measurement rule

**1. The rule.** Common-driver exposure is measured as:

    COMMON_DRIVER_EXPOSURE = SUM over all governed common-driver issuers
                             of (DIRECT_EXPOSURE + ALL GOVERNED ETF-EMBEDDED EXPOSURE)

This is the **authoritative** definition of the quantity the 40% ceiling is
measured against. It is recorded machine-readably in `issuer_lookthrough.yaml`
under `common_driver_measurement_rule`, `basis: FULL_EFFECTIVE_ALL_ISSUERS`.

**2. No selective omission.** No governed issuer's ETF-embedded component may
be omitted from the measurement, **specifically including `LLY`, `TSLA` and
`AAPL`**. A measurement that omits any governed issuer's embedded exposure is
not a valid common-driver measurement under this decision, regardless of how it
is labelled.

**3. Economic-issuer aggregation.** Where one economic issuer appears in a
governed fund under more than one line — multiple share classes, or a
depositary receipt alongside the local line — those lines aggregate into that
single governed issuer. **SEDOL identifies a security, not necessarily an
economic issuer.** Aggregation requires evidenced mapping of each distinct
security identifier to the same economic issuer; name similarity alone is
never sufficient.

**4. The retained figure is historical evidence, not the rule.** The retained
`40.0284%` value, its `measured_at: 2026-07-30`, its methodology string and its
`PHQ-2026-01` evidence pointer are **preserved unchanged and unrewritten** in
`issuer_lookthrough.yaml`. They remain an accurate record of what was measured
on that date under the process then in use. They are now explicitly annotated
as **historical evidence only**. The retained figure may not be cited as the
measurement rule, and this decision does not retroactively revise it, restate
it, or claim it was computed under PD-1.

**5. Implementation.** `allocate._issuer_exposure` already computes
`direct_pct + Σ(fund_pct_of_book × fund_holding_weight)` for every governed
issuer and sums across all of them. PD-1 therefore **ratifies existing
production behaviour**. `allocate.py` is **not modified** by this decision.
This is a durable statement of what the code already does, not a change to what
it does.

**6. What PD-1 does not change.** Common-driver issuer membership remains the
same eleven issuers. The 8% effective-issuer ceiling remains `8.0`. The 40%
common-driver ceiling remains `40.0`. No cluster cap, cluster membership,
`target_pct`, gate, margin parameter, or allocator decision rule is changed.

### PD-2 — Primary-source look-through refresh

**7. Authority.** The principal authorizes refreshing every governed
`fund_holding_weight` in `issuer_lookthrough.yaml` from **official primary-source
issuer holdings data**, with auditable provenance.

**8. Governing sources, and only these.** `SPY` from State Street Global
Advisors; `VEA` and `VWO` from Vanguard. Blogs, third-party ETF data sites,
search-engine snippets, cached summaries, and model recall are **not**
governing sources and were not used. Where an official source could not be
obtained, the correct action is to stop and report for that fund, never to
substitute an unofficial provider.

**9. Acquisition, recorded honestly.** Network egress from this execution
environment to the official publisher endpoints is denied by policy (the
gateway refuses `CONNECT`). The official files were therefore **supplied
directly by the principal** rather than fetched here. Each fund's
`fund_sources` block records `acquisition: PRINCIPAL_SUPPLIED_OFFICIAL_FILE`
together with an `acquisition_note` stating the egress block. The provenance
record does not claim a fetch that did not happen.

**10. Evidence retention.** The three official files are retained verbatim and
SHA-256-pinned under `governance/evidence/PHQ-2026-08/`:

| Fund | File | Published as of | SHA-256 |
|---|---|---|---|
| SPY | `holdings-daily-us-en-spy.xlsx` | 2026-09-17 | `19bb37597955bc83ea8b2163a2f06898334afa2f5d6eda66c52c4d6f9ae2cee3` |
| VEA | `Holdings_details_FTSE_Developed_Markets_ETF.csv` | 2026-08-31 | `cb6603835fef54b99ddaefc6b349306daea3e3929461f95c03a98fd4256119aa` |
| VWO | `Holdings_details_FTSE_Emerging_Markets_ETF.csv` | 2026-08-31 | `e0fdfda925ebddf036c73d60ea655ec220b7e7f0481593a660e985797634ef1d` |

**11. Machine-readable provenance.** `issuer_lookthrough.yaml` carries a
`fund_sources` block recording, per fund: publisher, source identity,
`holdings_as_of`, `received_at`, acquisition mode and note, evidence path,
evidence SHA-256, and — per governed issuer — the exact source security rows
(name, ticker, SEDOL, raw weight) the refreshed weight was built from. The
`holdings_as_of` field makes staleness machine-readable rather than opaque.

**12. Alphabet.** `SPY` carries Alphabet under two lines: `ALPHABET INC CL A`
(`GOOGL`, SEDOL `BYVY8G0`, 3.092270%) and `ALPHABET INC CL C` (`GOOG`, SEDOL
`BYY88Y7`, 2.466308%). Per PD-1 §3 these aggregate into the single governed
Alphabet economic issuer: `0.05558578`.

**13. TSMC identity.** `VWO` carries Taiwan Semiconductor Manufacturing Company
under two lines: the Taiwan local line `2330` (SEDOL `6889106`, 14.67%) and the
sponsored ADR `TSM` (SEDOL `2113382`, 0.02%). These are the same economic
issuer and aggregate to `0.1469` per PD-1 §3. `VWO` separately carries **Taiwan
Semiconductor Co Ltd**, ticker `5425`, SEDOL `6222972` — a **different economic
issuer** despite the similar name. It is **excluded**, and that exclusion is
recorded explicitly in `fund_sources.VWO.excluded_similar_identities` so the
decision not to include it is auditable rather than invisible.

**14. Refreshed weights.** All eleven governed `fund_holding_weight` values are
replaced with the primary-source-derived values. Membership is unchanged.

**15. What PD-2 does not change.** No ceiling, cluster cap, cluster membership,
`target_pct`, gate, holding, or margin parameter is changed. No automatic
network fetching is added to the production allocator; this remains a
point-in-time snapshot refreshed under governance, as
`PHQ-2026-01_TARGET_ALLOCATOR_IMPLEMENTATION_DESIGN_NOTE.md` §5/§6 requires.

### Measured effect, reported not acted on

**16.** Recomputing on the canonical target-weight basis through the unchanged
production helper, against the refreshed configuration:

- **Maximum effective issuer exposure: `NVDA` at `7.2099%`** against the
  unchanged `8.00%` ceiling — headroom `0.7901pp`, status `APPROACHING`. No
  governed issuer exceeds the 8% ceiling.
- **Common-driver exposure: `41.7646%`** against the unchanged `40.00%` ceiling
  — headroom `−1.7646pp`, `limit_status: OVER_LIMIT`.
- Cluster caps unchanged and unaffected: `semis` 15.75% / 25% `OK`;
  `power_infra` 6.50% / 20% `OK`; `oil` 0.00% / 20% `UNAVAILABLE` (no canonical
  members).

**17. This is measurement, not action.** The over-ceiling common-driver reading
is **reported**, exactly as `PHQ-2026-01` point 9 and `PHQ-2026-02` already
required of the retained figure — recorded as measured, not rounded into
compliance. This decision authorizes **no** trim, sale, purchase, target
change, ceiling change, or order of any kind in response to it. The
common-driver ceiling's existing operational effect in `allocate.py` — a
no-add clip-or-block on buys, never a trim or sell rule — is unchanged.

**18. The measurement basis is target weights, not holdings.** Every figure in
§16 is computed on the canonical full-deployment target-weight basis (a unit
book of 100.0 with each row's own `target_pct` as its value), the same basis the
retained figure used. It is **not** a measurement of the current portfolio and
must not be read as one.

### Not authorized

**19.** This decision authorizes nothing beyond §§1–18. It specifically does
**not** authorize: any change to `targets.yaml`, `gates.yaml`, `holdings.yaml`,
`margin_state.py`, `levels.py`, or `allocate.py`; any change to the 8% or 40%
ceiling; any change to cluster caps, cluster membership, or common-driver
membership; any margin-policy change, and the 1.8x leverage cap and 30% buffer
floor are untouched; execution of `PORTFOLIO-ROBUSTNESS-V2` or `MARGIN-0005`
Stage 3; any `ENDPOINT-0001` Stage-1 arming, attestation, or lane claim; any
trade, order, or brokerage capability; any allocation check run for execution;
or PD-3, PD-4, PD-5, or any successor.

## Rationale

The 40% ceiling was being enforced against an undefined quantity. Two
defensible readings of "common-driver exposure" existed in the committed record
simultaneously — the production helper's full-effective sum and the retained
headline's narrower figure — and nothing chose between them. That is not a
tolerable state for a hard limit: a limit whose measurement basis is ambiguous
is a limit that can be satisfied or breached by reading choice rather than by
portfolio fact.

Full effective exposure is the reading that matches the ceiling's stated
purpose. The control exists because these eleven issuers share a common return
driver, and a share of that driver reaching the book through an ETF wrapper is
economically identical to the same share held directly. `AAPL` makes this
concrete: under the narrower reading a governed issuer with no direct target
contributes zero to a ceiling explicitly created to capture it. Selective
omission also has no stopping rule — nothing in the narrower reading explains
why `LLY`, `TSLA` and `AAPL` specifically, which is itself evidence that the
omission was an artifact rather than a policy.

Resolving PD-1 in favour of what `allocate.py` already does means the
production system needs no behavioural change. This matters: the alternative —
ratifying the narrower reading — would have required editing the allocator to
implement selective omission, introducing a new rule with no principled
membership test, on the strength of reverse-engineering a single retained
number.

PD-2 follows from PD-1 rather than standing alone. Having fixed what is
measured, the inputs to that measurement must be current and attributable. The
prior weights were two-decimal-percent figures with no publisher, no as-of
date, and no hash — unattributable, and by the file's own quarterly standard,
stale. Primary-source data with retained bytes, published as-of dates and
SHA-256 pins makes every refreshed weight independently re-derivable from
evidence in the repository.

The refreshed measurement reads further over the ceiling, not less. That is
reported plainly. It is the expected consequence of measuring more completely
and from more current data, and it is recorded as measured — not adjusted,
rounded, or accompanied by a recommendation.

## Alternatives considered

**Ratify the narrower reading and edit `allocate.py` to match.** Rejected. It
would have required inventing a membership rule for which issuers' embedded
exposure counts, with no principled basis, derived by reverse-engineering one
retained figure. It also weakens the control precisely where the control is
most needed.

**Rewrite the retained `40.0284%` to the recomputed figure.** Rejected. The
retained value is an accurate record of a measurement made on 2026-07-30 under
the process then in use. Overwriting it would destroy the evidence trail that
exposed the ambiguity in the first place. It is preserved verbatim and
annotated instead.

**Leave the weights stale and file PD-1 alone.** Rejected as creating a
half-valid state: an authoritative rule fed by unattributable inputs. The
principal approved both together, and they were implemented together.

**Substitute a third-party ETF data provider when official egress failed.**
Rejected outright — excluded by the authorizing scope and by the evidence
standard. The correct behaviour on blocked official access is to stop and
report, which is what happened; the principal then supplied the official files
directly, and the acquisition path is recorded honestly rather than described
as a fetch.

**Add live constituent fetching to the allocator.** Rejected. Explicitly out of
scope, and `PHQ-2026-01_TARGET_ALLOCATOR_IMPLEMENTATION_DESIGN_NOTE.md` §5/§6
warns against exactly this. The file remains a governed point-in-time snapshot.

**Aggregate TSMC by name.** Rejected. `VWO` contains a differently-identified
company with a near-identical name. Identity is resolved by SEDOL, and the
excluded identity is recorded so the exclusion is auditable.

## Consequences

The common-driver measurement basis is now stated, machine-readable, and
enforced by tests. `allocate.py`'s existing behaviour is the governed rule
rather than one of two unreconciled candidates.

Every governed constituent weight is traceable to a retained, hashed, official
publisher file with a published as-of date, and to the specific source security
rows it was built from.

The recomputed common-driver figure now reads `41.7646%` against an unchanged
`40.00%` ceiling. The gap versus the retained `40.0284%` is `+1.7362pp`, and
the existing `RETAINED_MEASUREMENT_DISCREPANCY` reporting path continues to
surface it. The ceiling is a no-add control; it is not, and does not become, a
trim or sell trigger.

`holdings_as_of` dates become the staleness signal for the next quarterly
review. Refreshing them again is a future, separately authorized unit.

Nothing in the live portfolio, the targets, the gates, the caps, the margin
policy, or the order path changes as a result of this decision.
