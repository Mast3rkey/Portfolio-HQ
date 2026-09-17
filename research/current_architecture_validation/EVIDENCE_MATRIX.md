# Current-Architecture Target-Weight and Concentration Evidence Validation

> **⚠️ Dated evidence snapshot. Not policy, not authority, not a recommendation.**
> This artifact classifies the evidence behind parameters that are already in force. It
> changes no target, cap, ceiling, cluster membership, gate, margin parameter, holding, or
> allocator behaviour; executes no study; acquires no data; and makes no buy, sell, trim, or
> hold recommendation. Margin parameters (the 1.8x leverage cap and 30% buffer floor) are
> **out of scope** for this unit. Stage 1 remains **UNARMED AND NOT EXECUTABLE**.

**Artifact ID:** `CURRENT-ARCH-VALIDATION-0001`
**As-of:** 2026-09-17
**Base commit:** `e8b252a5ce82662112cfdbece8a9ee02687d6c66`
**Machine-readable companion:** [`evidence_matrix.json`](evidence_matrix.json)
**Verification:** `test_current_architecture_validation.py` re-derives every load-bearing
number below — against this artifact's **own pinned base commit**, read read-only out of git,
using the production exposure helper. Nothing here should be believed on this document's own
say-so.

**Why the basis is pinned, and what that guarantees.** This is a historical record of what was
true at its stated basis. Reconciling against that basis keeps the check permanently strong
(it still proves the artifact was internally coherent and matched its inputs when created)
while ensuring it never becomes a gate on future policy. A later, legitimate change to live
repository inputs — a refreshed `issuer_lookthrough.yaml`, a defined common-driver inclusion
rule, an executed successor robustness study, updated provenance documentation, an authorized
target or cap change — does **not** make this record false and does **not** by itself turn
repository CI red. Live drift is reported, never fatal. The historical figures here are never
rewritten to current values.

If the pinned base commit is unreachable (a shallow clone), the basis-dependent checks skip
with an explicit reason rather than failing; full-history CI still exercises them.

---

## 1. Headline answer

**No parameter examined in this unit is supported by decision-grade evidence evaluating the
current architecture.** That is a statement about the evidence, not a criticism of the values.
Several are defensible governance choices that were never intended to be empirical; the
problem is that the repository's own provenance documentation no longer describes the
architecture that is actually running.

Three findings are load-bearing:

1. **Every tier-era backtest is architecturally orphaned.** All six read
   `targets.yaml["tiers"]`, directly or through `backtest_regime.universe()`. That key does not
   exist — PHQ-2026-02 removed it. None of them can run against the current configuration, and
   none of them ever tested the current 36 per-name weights.
2. **Both governing provenance documents predate the architecture they describe.**
   `docs/NUMERIC_PARAMETER_PROVENANCE_AUDIT.md` is pinned to 2026-07-21 and
   `docs/PORTFOLIO_POLICY_MANUAL.md` to 2026-07-18; the canonical migration landed 2026-07-31.
   Both still describe tiers, a T1/T2 trim ceiling, and cluster memberships that no longer
   exist. The provenance audit contains **zero occurrences of "issuer", "look-through", or
   "common-driver"** — the entire look-through control family is absent from it, because
   `issuer_lookthrough.yaml` did not yet exist when it was written.
3. **The common-driver "discrepancy" is not configuration drift.** The retained due-diligence
   package's own eleven line items sum to exactly the figure recomputed today. Its *headline*
   number disagrees with its *own table*. Details in §5.

---

## 2. Provenance and evidence matrix

Grades use the vocabulary the unit was given: evidence-derived, robustness-tested, supported
within tested range, governance choice, inherited, unvalidated, unable to determine. Nothing
below is called optimal, because nothing below has earned it.

| Parameter | Current value | Scope now | Scope when set | Evidence actually used | Current arch. tested? | Alternatives tested? | Grade | Status |
|---|---|---|---|---|:--:|:--:|---|---|
| 36 canonical `target_pct` | 36 rows, 99.25% | whole roster | 37 rows, 100.00% | External committee process (PHQ-2026-01); no in-repo study | No | No | **Governance choice** (unvalidated) | Active, binding |
| `semis` cap | 25.0% | ASML, AVGO, KLAC, NVDA, TSM (5) | 13 names incl. AMD, MU, MRVL, LRCX, AMAT, WDC, INTC, SKHY | 0.542 avg pairwise correlation — prose only, no retained dataset | No | No | **Governance choice** (unvalidated) | Active; non-binding at target |
| `power_infra` cap | 20.0% | ETN, GEV, PWR (3) | GEV, ETN, VRT, PWR (4) | 0.560 avg pairwise correlation — prose only | No | No | **Governance choice** (unvalidated) | Active; non-binding at target |
| `oil` cap | 20.0% | **zero members** | XOM, CVX | Drawdown stress arithmetic (input unretained) | No | No | **Unable to determine** | **Dead configuration** |
| Issuer ceiling | 8.0% | 11 mapped issuers | same | None recorded; unclassified by NUM-0001 | No | No | **Governance choice** (unvalidated) | Active; tightest live constraint |
| Common-driver ceiling | 40.0% | same 11 issuers | same | Retained "estimate", basis undefined | No | No | **Unable to determine** | Active; reporting OVER_LIMIT |
| Cluster trim mechanism | floor-at-target, largest-overweight-first, no RSI gate | all clusters | coexisted with 2 now-retired trim rules | Mechanical unit tests only | No | No | **Unvalidated** | Active; latent at target |

Full per-parameter records — origin source, known limitations, policy status, and the specific
next evidence each would need — are in `evidence_matrix.json` under `parameters[]`.

---

## 3. What the existing studies actually prove

| Question | Answer |
|---|---|
| What did `backtest_weights.py` compare? | Four **tier-weight schemes** (current gradation / equal / flatter / steeper) over 63 tickers, holding the band/spec trim constant. |
| Were the current 36 per-name weights tested? | **No.** It varied a tier→weight mapping. The current architecture has no tiers; it sets a weight per name. The question it answered no longer exists. |
| What did `backtest_t1t2_trim.py` test? | Whether a T1/T2 per-name 1.5x ceiling should exist. That rule was **retired** by PHQ-2026-02. |
| Did any test calibrate semis 25% or power_infra 20%? | **No.** No cap-level sweep exists anywhere in the repository. |
| Did any test calibrate issuer 8% or common-driver 40%? | **No.** Neither appears in any backtest or in the provenance audit. |
| Did any test evaluate the **current** cluster-trim algorithm? | **No.** `backtest_t1t2_trim.py`'s Arm D was the cluster-shaped arm and **did not run** (conditional on \|C−B\| > 1.0pp; observed 0.00pp). `trim_backtest.md` tested band/spec RSI-gated trims — a different, now-retired rule. |
| What did RISK-0005 invalidate? | `PORTFOLIO-ROBUSTNESS-0001` → `EVIDENCE_LIMITED_NOT_DECISION_GRADE`, on four defects (23/28 datasets differing from the selected inventory hashes; 17 unresolved corporate-action mismatches; 115 missing SOL sessions; wrongly admitted pre-boundary RTX rows). Citing it as validation of the baseline is an explicitly **barred claim**. |
| What does `whole_portfolio_robustness_v2` contain today? | Protocol, pre-registration, frozen input manifest, engine and validators. **No execution directory. No results.** Its own admission gate records `admitted: false`. |
| Does V2 bind to the current canonical targets? | Yes for inputs — `targets.yaml`, `gates.yaml` and `issuer_lookthrough.yaml` are hash-pinned. But it evaluates **whole-portfolio alternatives**; it calibrates no cap or ceiling level. |
| Do decision-grade current-architecture results exist? | **No.** |

---

## 4. Which controls actually bind

Computed at **canonical target weights** (full deployment), via the production exposure helper.
Current-holdings exposure is `UNAVAILABLE_FROM_REPOSITORY_STATE` and was not estimated.

| Control | Exposure | Limit | Utilisation | Verdict |
|---|---:|---:|---:|---|
| `semis` | 15.75% | 25.00% | 63.0% | Non-binding |
| `power_infra` | 6.50% | 20.00% | 32.5% | Non-binding |
| `oil` | 0.00% | 20.00% | — | **Dead — zero members.** Not a satisfied limit |
| Max effective issuer (NVDA) | 7.1490% | 8.00% | 89.4% | **Tightest constraint**, 0.851pp headroom |
| AI/platform common driver | 41.6454% | 40.00% | 104.1% | **OVER_LIMIT** by 1.6454pp |

Two consequences worth stating plainly:

- **No cluster cap can bind at full deployment**, so the cluster-trim mechanism — the only trim
  rule left in the system — is **latent**. It can fire only on live holdings drift.
- **The oil cap is inert configuration that reads like an active control.** A zero-member cap
  cannot bind on anything. The currentness preflight already refuses to report it `OK`.

---

## 5. Why the common-driver recomputation differs from the retained measurement

This was the unit's sharpest question. The answer is **not** configuration drift.

- Recomputed at target weights today: **41.6454%**
- Retained measurement (2026-07-30): **40.0284%**
- Delta: **+1.6170pp**

The retained due-diligence package contains an itemized eleven-issuer look-through table **and**
a summary block. Summing that table's own `effective_weight` values gives **41.6454%** —
identical to today's recomputation to four decimal places. Every fund allocation it used
(SPY 15%, VEA 7%, VWO 1%) still matches `targets.yaml`, and its NVDA effective weight (7.149%)
reproduces exactly.

**So the discrepancy lives inside the retained evidence: its headline figure is inconsistent
with its own line items in the same file.**

An exhaustive search over all 2,047 non-empty subsets found exactly **one** combination that
reproduces the headline, unique at 1e-9 tolerance:

```
41.6454%  (all eleven effective weights)
−  1.6170pp  (the ETF-embedded components of LLY, TSLA and AAPL)
=  40.0284%  (the retained headline)
```

Corroboration that the *line items* are the reliable part: the package's separate
`effective_mega6_weight` (0.29999) is exactly reproducible from those same line items
(NVDA + MSFT + AMZN + GOOGL + AVGO + META). The headline is the outlier, not the table.

**Intent is unresolved.** The package documents no inclusion rule, calls the number an
"estimate", and gives no reason why LLY, TSLA and AAPL would contribute direct weight but not
embedded weight. This artifact establishes the arithmetic; it does not claim to know the intent,
and it does not decide which figure is correct.

**Consequence.** Whether the canonical target portfolio breaches its own 40% ceiling depends
entirely on an inclusion rule that was never written down. That is a governance gap, not a
measurement error — and it is why this parameter is graded **unable to determine** rather than
simply "over limit".

A second, independent staleness issue affects both ceilings: `issuer_lookthrough.yaml`'s VEA and
VWO constituent weights are as-of 2026-05-31 — **109 days old**, past the one-quarter refresh
condition the file states for itself. Those feed ASML and TSM embedded exposure.

---

## 6. Determination: why no study was run

The unit's decision rule was three-way. This is **Case 3**, and it stops before execution.

- **Case 1 rejected.** No decision-grade current-architecture evidence exists to reconcile.
  The one study that compared this baseline against alternatives is barred from being cited as
  validation of it.
- **Case 2 rejected on the facts, not on judgement.** `PORTFOLIO-ROBUSTNESS-V2-0001` is
  preregistered and hash-pinned to the current config, but it **cannot lawfully execute under its
  own contract**:
  - `validation/input_admission.json` → `admitted: false`, `INPUT_ADMISSION_FAILED`
  - `inputs/input_freeze.json` → SOL provider `UNRESOLVED_SINGLE_USD_SPOT_SOURCE`;
    `dff_availability.status: UNRESOLVED` with `substitution: PROHIBITED`
  - `pre_registration.yaml` → `crypto: NEW_SUCCESSOR_DISPOSITION_REQUIRED_BEFORE_EXECUTION`

  Running it would violate its own halt-before-results rule. Unblocking it requires **external
  data acquisition** (a single-source SOL/USD spot series with complete 2021-06-01→2026-07-31
  coverage, and a DFF/FRED publication-vintage receipt), which is not authorized here.
- **Case 3 applies, and stops.** Designing and executing a new calibration study would be new
  experimental authorization that no accepted decision grants. Per the unit's own instruction,
  this artifact therefore **reports the principal decisions needed instead of inventing a
  parameter sweep**.

**Nothing was executed. No data was acquired. No parameter changed.**

---

## 7. Principal decisions required

| # | Topic | Decision needed | Why it blocks |
|---|---|---|---|
| **PD-1** | Common-driver measurement rule | Define the authoritative common-driver membership and inclusion basis | Without it the repository cannot say whether it is at or over its own 40% ceiling; the two candidate answers straddle the limit |
| **PD-2** | Look-through refresh | Authorize or decline refreshing `issuer_lookthrough.yaml`'s ETF constituents | VEA/VWO are 109 days old, past the file's own refresh rule; they feed both ceilings |
| **PD-3** | Cluster cap membership and level | Authorize a correlation re-scan over current membership, dataset retained | The caps' only empirical input was measured over memberships that no longer exist and was never retained |
| **PD-4** | Oil cap disposition | Retire it or repopulate its membership | Zero-member cap; inert config presenting as an active control |
| **PD-5** | Successor whole-portfolio study | Authorize the external data acquisition V2 needs, or accept that no decision-grade robustness evidence will exist for the current targets | V2 is the only designed vehicle for the target-weight question and is halted at its own input gate |

**Recommended sequence:** PD-1 and PD-2 first — both are cheap, both are prerequisites to
trusting any current concentration number, and PD-1 is the only one that currently changes
whether a live control reads as breached.

---

## 8. Limitations

- This clone is **shallow** (256 commits, oldest reachable 2026-08-20). The SHA that
  `NUMERIC_PARAMETER_PROVENANCE_AUDIT.md` pins (`0b419765…`) is not resolvable here, so that
  audit could not be re-verified against its stated commit. This artifact relies on its audit
  **date** (2026-07-21) relative to PHQ-2026-02 (2026-07-31), which is sufficient for the
  staleness finding.
- The LLY/TSLA/AAPL exclusion is an **arithmetic** reconciliation, unique at 1e-9 tolerance.
  Documented intent remains unresolved and is not inferred here.
- All concentration figures are at **target weights**. Current-holdings exposure is unavailable
  from repository state and was deliberately not estimated.
- The external PHQ-2026-01 committee process is visible only through its retained outputs; its
  method could not be independently re-derived. Its own package discloses that the supporting
  backtest had an approximately 23-month common window "containing look-ahead and survivorship
  limitations".
- Correlation figures (0.542 / 0.560 / 0.819) exist **only as narrative citations**. No dataset,
  script, or reproducible artifact backs them anywhere in the repository.
