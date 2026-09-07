# WS-0005 Milestone 7 — Baseline Reconciliation (retained audit)

**Date:** 2026-08-06
**Authority:** `governance/decisions/TIER-0007-ws0005-milestone7-baseline-reconciliation-authorization.md` (merged, PR #255, merge commit `f71ea3bb1428445023c4fa582ed953ae409ba070`, independently reviewed across three rounds, principal-accepted at exact head `4a4408ab133b8ebb58309d607f397f37853bfaa6`, post-merge verified).
**Comparison-source main SHA:** `1d5d93f94bbc39a0b9d99178a7b477e6f0f27928` (PR #258's merge commit — the exact `origin/main` head this implementation branched from and verified against).
**Sealed cohort reference:** `intelligence/classification/*.yaml` + `COHORT_MANIFEST.yaml`, sealed under `TIER-0002`/`TIER-0003`/`TIER-0004`/`TIER-0005`, implemented by PR #253, Milestone 6 completion determined by `TIER-0006` at merge commit `1107c5b70801ff5e7027efddf6a2aa916030dce2`.
**Produced artifact:** `intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml` (27 tickers, alphabetical, 18-field schema per TIER-0007 §F).

This is the single implementation unit TIER-0007 §L authorized: exactly one later, separate, bounded Milestone 7 PR unblinding and comparing the 27 sealed Milestone 6 records against current governed baseline context. **Analysis only.** It recommends, authorizes, and executes no target/tier/role/gate/holdings/cap/cluster/allocator/margin/ladder/chart/order/trade change of any kind.

## §C pre-unblinding integrity checks (all performed and passed before any comparison content was drafted)

1. `classification_validator.py`: `OK (28 result(s))` — 27 sealed records + `COHORT_MANIFEST.yaml`, independently re-run this session.
2. `content_sha256` recomputed for all 27 records via direct comparison against `COHORT_MANIFEST.yaml`'s own recorded hashes: **zero mismatches**.
3. Manifest bidirectional reconciliation: 27 manifest entries ↔ 27 sealed record files, zero orphans in either direction (mechanical Python cross-check, not `classification_validator.py`'s own internal check alone — independently re-derived).
4. `lifecycle_status: sealed` confirmed on all 27 records, zero exceptions.
5. `git diff 1107c5b70801ff5e7027efddf6a2aa916030dce2 HEAD -- intelligence/classification/` (base = `origin/main` at implementation start, `1d5d93f9...`): **empty diff** — zero drift in any sealed record or the manifest since the `TIER-0006` merge.
6. Comparison-source `main` SHA recorded as `1d5d93f94bbc39a0b9d99178a7b477e6f0f27928` — a specific, dated commit (PR #258's merge), not "current main" as a moving target, per TIER-0007 §C step 6.

`intelligence/classification/*.yaml` and `COHORT_MANIFEST.yaml` were opened read-only throughout this implementation. Neither file, nor `classification_validator.py`, nor the sanitizer, was edited.

## Methodology

For each of the 27 sealed tickers, current baseline context was gathered from exactly the sources TIER-0007 §D permits: `targets.yaml` (`target_pct`, `caps.clusters` membership), `gates.yaml` (status, `next_gate`, for the six formerly-gated names), `issuer_lookthrough.yaml` membership, `intelligence/relationships/*.yaml` coverage, each ticker's `intelligence/companies/<TICKER>.yaml` (`portfolio_role_ref`, `conviction.rating`, `review.last_reviewed`/`next_due`), and this filing's own governance context. No chart evidence was consulted or used anywhere (`chart_evidence_used: false` in the artifact's own top-level metadata, mechanically enforced by `reconciliation_validator.py`).

Structural-risk comparison (item 10 of the 18-field schema) was computed mechanically: cluster-cap membership, issuer-look-through membership, and relationship-record coverage were independently re-derived live from `targets.yaml`/`issuer_lookthrough.yaml`/`intelligence/relationships/` and cross-checked against each sealed record's own `risk_concentration.unmeasured_flag`. **Result: 27/27 exact match, zero drift** — the sealed 11-name `unmeasured_flag: true` set (COST, ICE, ISRG, PANW, RKLB, RTX, SNPS, SPGI, TMO, V, WM) exactly reproduces `REL-0007`'s own independently-computed finding.

Role comparison (items 2–3) found the same structural pattern on all 27 records without exception: `portfolio_role_ref` still carries the pre-`PHQ-2026-02` T1/T2/band/gated tier vocabulary that `targets.yaml`'s canonical destination architecture no longer defines anywhere — a corpus-wide finding `TIER-0001`'s Milestone 5 audit already disclosed, reconfirmed here rather than newly discovered. Because this label carries no economic-function content, it cannot conflict with the sealed `economic_role` finding for any ticker; role comparison is therefore uniformly "no conflict possible; sealed record is the corpus's only economic-role description" across all 27 — this is a genuine structural finding, not templated prose.

**Primary-disposition determination** (TIER-0007 §H, deterministic precedence — `baseline_assumption_stale` > `divergence_requires_review` > `aligned` > `no_policy_conclusion`) applied the following reasoning, disclosed here for reproducibility:

- **Non-gated tickers:** sealed `capital_priority.status: maintain_current_weight` was read as `aligned` (current baseline is an unflagged, steady target with no active reconsideration signal — the sealed finding independently confirms nothing distinctive is happening). Sealed `case_for_review` was read as `divergence_requires_review` (current allocator policy carries no standing monitor-elevation mechanism for T1/T2/band positions, so a sealed finding that a name "warrants explicit reviewer reconsideration" is not reflected anywhere in current baseline treatment).
- **Gated tickers (SNPS, ICE, SPGI, WM, RKLB, TSLA):** the current baseline for a gated name is already "no new capital, awaiting a named reopening condition" — structurally similar to what a sealed `case_for_review` finding calls for. Four of six (SNPS, ICE, RKLB, TSLA) carry sealed `case_for_review` and were read as `aligned` on this basis — the gate's own withholding posture and the sealed finding point the same direction. **WM is the one exception**: its sealed status is `maintain_current_weight` — an "ordinary, ratified, nothing-distinctive" finding — read directly against evidence (the Q2 2026 earnings package, Stericycle integration friction "substantially resolved") that is exactly what WM's own `next_gate` text names as its reopening condition. This is read as `divergence_requires_review`, not `aligned`: the sealed evidence, on its own terms, does not support continued withholding on the specific grounds the gate names, though this reconciliation does not itself decide whether the gate should reopen (§K explicit non-authorization). **SPGI** carries sealed `capital_priority.status: no_assessment` — the sealed record itself abstained because a majority of its disclosed risk/catalyst/source evidence was excluded from the drafting shard's sanitized package (a disclosed Milestone 6 correction-round finding, not new to this unit). No substantive primary value (1–3) could responsibly be reached from an abstained judgment; SPGI is `no_policy_conclusion`, per TIER-0007 §H item 4's own text.
- **Zero tickers reached `baseline_assumption_stale`.** This reconciliation found no case where the current baseline's *founding assumption* was shown factually superseded (as opposed to "warrants review because something changed") — disclosed as a finding, not omitted.

**Secondary conditions** were assigned mechanically: `structural_measurement_gap` exactly where the sealed `unmeasured_flag` is `true` (the same 11-name set reconfirmed above); `unresolved_evidence` where `evidence_quality.primary_source_coverage` is `limited`/`partial` (ICE, LLY, RKLB, SNPS, SPGI, TSLA, WM), extended to `AVGO, GOOGL, ISRG, META, NVDA, TMO` where the sealed record's own rationale explicitly flags a load-bearing supporting fact as "secondary-sourced," "reportedly," or "pending primary-source confirmation" (disclosed methodology, not a hidden judgment call). Real-world open matters disclosed without a sourcing-confidence caveat (e.g., ASML's unresolved export-control allegation, CEG's Calpine integration) were **not** flagged `unresolved_evidence` — that distinction (evidentiary confidence vs. an open real-world matter) is stated explicitly so a future reviewer can check it.

## Aggregate result

| Primary disposition | Count | Tickers |
|---|---|---|
| `baseline_assumption_stale` | 0 | — |
| `divergence_requires_review` | 14 | ASML, AVGO, CEG, ETN, GEV, GNRC, GOOGL, ISRG, LLY, META, NVDA, RTX, TMO, WM |
| `aligned` | 12 | AMZN, COST, ICE, KLAC, MSFT, PANW, PWR, RKLB, SNPS, TSLA, TSM, V |
| `no_policy_conclusion` | 1 | SPGI |

| Secondary condition | Count | Tickers |
|---|---|---|
| `unresolved_evidence` | 13 | AVGO, GOOGL, ICE, ISRG, LLY, META, NVDA, RKLB, SNPS, SPGI, TMO, TSLA, WM |
| `structural_measurement_gap` | 11 | COST, ICE, ISRG, PANW, RKLB, RTX, SNPS, SPGI, TMO, V, WM |
| Both | 7 | ICE, ISRG, RKLB, SNPS, SPGI, TMO, WM |

14 + 12 + 1 = 27. Full per-ticker detail, citations, and 18-field content live only in the artifact itself — not restated here.

## Scope discipline

This artifact and this audit cover **exactly the 27 sealed canonical equity classifications** and nothing else. Broader contender-universe screening (`WS-0014`), ETF and cryptocurrency classification frameworks, cash/reserve/GLD/debt-reduction doctrine, cross-asset opportunity-cost synthesis, and final whole-portfolio allocation-readiness (`XASSET-0001`) all remain separate, unconcluded, unauthorized-by-this-unit future work. No numeric target, range, score, or ranking appears anywhere in the artifact — mechanically enforced by `reconciliation_validator.py`'s forbidden-key and forbidden-phrase scan.

## Validation performed

- `classification_validator.py`: `OK (28 result(s))`
- `relationship_validator.py`: `OK (13 record(s))`
- `reconciliation_validator.py` (new): `OK (27 tickers)`
- `intelligence_validator.py`: companies 53/53 valid, themes 2/2 valid
- `freshness_validator.py`: `OK`
- Decision catalog: 84 decisions, `issues == ()` — **unchanged**, since `TIER-0007` already authorized this implementation and no new governance decision file is filed by this unit
- `test_reconciliation_validator.py` (new): 64/64 passed
- Full repository `pytest`: see PR body / commit message for the exact count at this exact head
- `git diff --check`: clean
- Zero diff on every protected path (`allocate.py`, `margin_state.py`, `levels.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, every existing `intelligence/classification|companies|themes|relationships/` file, `COHORT_MANIFEST.yaml`, `classification_validator.py`, `intelligence_classification_sanitizer.py`)
- Exactly one `priority: primary` workstream (`WS-0005`)

## Completion-standard disclosure

`TIER-0007` authorizes and specifies this one implementation unit; it does **not** itself define a separate Milestone 7 completion-determination standard, unlike `REL-0004` (which explicitly defined the Milestone 4 completion standard ahead of `REL-0006`'s determination) or `PI-0031` §K (which defined the Milestone 3 standard). Following the identical pattern those two milestones established — a completion determination is its own separate, later, independently-reviewed governance filing, never self-declared by the implementation PR that does the content work — **this implementation does not claim Milestone 7 complete**, and `operations/WORKSTREAMS.yaml`'s `milestone-7-baseline-reconciliation` gate is updated to `status: in_progress` (recording that content work has now begun) but not to `complete`. A future, separate Lane G filing (matching `TIER-0006`'s and `REL-0006`'s own precedent) would be required to: (a) define Milestone 7's completion criteria if none exist yet, or reuse this filing's own methodology section as a basis, and (b) independently re-verify this artifact, its validator, its tests, and this session's own review/merge/post-merge lifecycle before declaring Milestone 7 complete. This unit does not perform that determination and does not authorize Milestone 8.

This implementation does not authorize, begin, schedule, or imply Milestone 8 (policy recommendation) or Milestone 9 (independent review and adoption).
