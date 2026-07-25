# WS-0005 Milestones 1–2 — Portfolio Asset Inventory & Intelligence/Freshness Audit

**Retained advisory audit artifact — implementation output, not an independent review.**

| Field | Value |
|---|---|
| Authority | `governance/decisions/OPS-0006-portfolio-intelligence-completion-and-zero-based-tier-review.md` §5 (2026-07-25 amendment); `operations/WORKSTREAMS.yaml` WS-0005, Milestones 1–2, `status: authorized` |
| Author | This implementation session, `session_01HJiL9QvHfrPfPFDHbv1dk8` — **not** an independent reviewer. An independent Fable review of this artifact is the pending next step, per OPS-0006 §16.1's own completion discipline. |
| Scope | Exactly Milestone 1 (governed-asset baseline inventory) and Milestone 2 (Intelligence coverage / freshness audit), per OPS-0006 §5. Milestones 3–9 are not begun and are not authorized by this artifact. |
| Repository state audited | `origin/main` @ `05cd6f0782936b670f738da0d447567e000a13d7` (PR #150 merge commit; parents `536e71f5…` (prior main) and `6da4f0d1…` (exact reviewed OPS-0006 head)), verified clean fast-forward, working tree clean |
| Mode | Read-only inventory and cross-reference. No `holdings.yaml`, `targets.yaml`, `allocate.py`, `margin_state.py`, or company/theme Intelligence record modified. No tier, target, role, cluster, cap, or allocator behavior changed. |
| Margin state referenced (context only, unchanged) | debt $1,590.40, buffer 63.12% (synced 2026-07-22, `holdings.yaml`); 1.8x leverage cap / 30% buffer floor (`targets.yaml` `margin:` block) — both unchanged by this artifact |

---

## 0. Post-merge preflight summary (performed before this artifact was drafted)

- `origin/main` fetched and pruned; local branch fast-forwarded to `05cd6f0782936b670f738da0d447567e000a13d7`, matching `origin/main` exactly. Working tree clean throughout.
- PR #150 confirmed: `merged: true`, `merged_by: Mast3rkey`, head `6da4f0d19f384b60d428a33ec82016899880f9ee` (confirmed ancestor of `origin/main`), base `536e71f58857f2e55d98169b2e829e392c27a016`. Merge commit `05cd6f0…` has exactly those two parents.
- Exactly 4 files changed by PR #150 (`CLAUDE.md`, `governance/decisions.yaml`, `governance/decisions/OPS-0006-…md`, `operations/WORKSTREAMS.yaml`) — matches the PR body's own claim, independently re-verified via `pull_request_read(get_files)`, not merely cited.
- Both retained reviews present and correctly anchored: full review `4779333484` (head `acc82a5…`, APPROVED WITH NON-BLOCKING FINDINGS) and delta review `4779344234` (head `6da4f0d…`, same verdict, confirms NB-1/NB-2 resolved). No open PRs on the repository at the time of this audit.
- Deleted source branch `claude/phase-two-governance-draft-c173n1` confirmed fully contained in `origin/main` (its head `6da4f0d…` is an ancestor).
- **NB-1 fix independently re-verified**: OPS-0006's frontmatter `related_decisions` (22 IDs) now matches `governance/decisions.yaml`'s index row for OPS-0006 field-for-field.
- **Full validation re-run on merged main** (this session, fresh environment — `pytest`/`PyYAML`/etc. installed from `requirements.txt`, no repository file touched):
  - `pytest -q` → **1502 passed, 0 failed** (matches the PR's own claimed count).
  - `intelligence_validator.py` → exit 0.
  - `freshness_validator.py` → `OK`, exit 0.
  - YAML parse clean: `operations/WORKSTREAMS.yaml`, `governance/decisions.yaml`, `holdings.yaml`, `targets.yaml`, `decision_log.yaml`.
  - Decision-frontmatter parse: **31 decision files ⇄ 31 `governance/decisions.yaml` index rows**, 1:1 by `decision_id`, zero mismatches.
  - `git diff --check` clean; working tree clean before and after (one incidental run of `intelligence_report.py --all` to read current staleness/role-drift state was reverted via `git checkout --` before any branch work began, since regenerating that generated artifact is outside this artifact's authorized scope).
- **Governance/authority state confirmed**: WS-0005 is the sole `priority: primary` workstream (exactly one match for the literal YAML field, verified by parsing, not `grep` prose-text collision); Milestones 1–2 `status: authorized`; Milestones 3–9 `status: proposed`. WS-0001 `in_progress`/`secondary`, S3 unauthorized in both directions (unchanged). WS-0002 `authorized`/`secondary`, OPS-0005's Phase Two grant intact (unchanged). `targets.yaml`'s `margin.leverage_cap: 1.8` and `margin.buffer_floor_pct: 30.0` unchanged; CLAUDE.md's own 1.8x/30% doctrine text unchanged (confirmed no diff in the PR #150 delta, which touched none of these files).

No condition met the "Stop with ACTION REQUIRED" bar in the assigning instructions — the merge, authority state, repository state, and validation all matched the expected state exactly. Execution of Milestones 1–2 proceeded.

---

## 1. Methodology — how the governed-asset population was reconciled

The **governed-asset population** is defined as every ticker/coin appearing in `holdings.yaml`'s `shares:` or `crypto_shares:` blocks (the repository's own source of truth for currently-held positions), cross-checked against `targets.yaml`'s tier ticker lists, cluster ticker lists, and crypto coin list. This is a mechanical, programmatic reconciliation — not a re-derivation from any external source — performed as follows:

1. Parsed `holdings.yaml`: 65 tickers under `shares:`, 3 coins under `crypto_shares:` (`BTC`, `ETH`, `SOL`), `holdings:` (manual-fallback dict) empty.
2. Parsed `targets.yaml`: summed tier ticker lists (`T1`=10, `T2`=14, `ETF`=3, `band`=33, `spec`=5 → 65 total), cluster ticker lists (`semis`=13, `power_infra`=4, `oil`=2), crypto coin list (`BTC`, `ETH`, `SOL`).
3. Set-differenced `shares:` tickers against the union of all tier ticker lists: **zero** tickers held but untiered, **zero** tickers tiered but not held. **Zero** tickers appear in more than one tier.
4. Verified every cluster's tickers are a subset of held tickers: **zero** cluster members not held.
5. Set-differenced `crypto_shares:` against `crypto.coins`: exact match, both directions.

**Result: 65 equity assets + 3 crypto assets = 68 governed assets**, with **zero** missing, duplicated, or tier-inconsistent records at the tier/cluster/holdings level. This matches the population size CLAUDE.md's own Decisions Log has referenced throughout (the "65 tickers," "63 T1-spec tickers (no crypto)" backtests, etc.), providing an independent confirmation that the long-referenced population figure is still accurate as of this audit.

One **pre-existing, independently-flagged data inconsistency** was found in this pass and is *not* new — see the BTC row in §4 and the portfolio-level note in §6.

**Intelligence/freshness cross-reference** (Milestone 2) was built by parsing all 7 `intelligence/companies/*.yaml` records, both `intelligence/themes/*.yaml` records, `intelligence/freshness_registry.yaml`, and `intelligence/freshness_checkpoints.yaml`, then joining each on ticker against the Milestone-1 population. `intelligence_report.py --all --as-of 2026-07-25` was run once, read-only, to cross-check this session's manual parse against the existing reporting tool's own output (role-drift and staleness); its generated-artifact side effect (`intelligence/reports/staleness_report.md`) was reverted before any branch work began, per this artifact's read-only-until-branch-creation posture.

---

## 2. Governed asset population — summary

| Tier / group | Count | Per-name target | Notes |
|---|---|---|---|
| T1 | 10 | 3.35% | ASML, TSM, MSFT, GOOGL, META, NVDA, GEV, LLY, V, COST |
| T2 | 14 | 1.65% | AVGO, AMZN, CEG, PWR, ISRG, TMO, DHR, SYK, MA, BRK.B, WMT, EQIX, MLM, AAPL |
| ETF | 3 | 2.30% | SPY, QQQ, GLD |
| band | 33 | 0.75% (cap 1.25×) | KLAC, LRCX, AMAT, AMD, MU, MRVL, WDC, VRT, ETN, CAT, GNRC, IBM, NOW, CRM, ORCL, NFLX, SHOP, CRWD, PANW, UBER, JPM, HOOD, XOM, CVX, RTX, ABBV, MRK, JNJ, GILD, UNH, BABA, SKHY, DELL |
| spec | 5 | 1.00% (fixed) | INTC, SPCX, RKLB, TSLA, PLTR |
| crypto sleeve | 3 | 10.0% (sleeve aggregate) | BTC, ETH, SOL |
| **Total** | **68** | — | 65 equities + 3 crypto |

**Cluster membership (cross-cutting, not exclusive of tier):** semis 13 members (≤25% of book), power_infra 4 members (≤20%), oil 2 members (≤20%). **T1/T2 concentration ceiling** (`gates.t1t2_trim_mult: 1.5`) applies to all 24 T1+T2 names uniformly. **Band cap_multiple** (1.25×, RSI-gated trim) applies to all 33 band names. **Spec** is fixed-at-target for all 5 spec names, never above.

---

## 3. Milestone 1 — Governed-Asset Baseline Inventory

Historical comparison baseline only — **not treated as presumptively correct**, per OPS-0006 §2/§3. No tier, target, role, cluster, or cap value below is changed by this artifact.

| Ticker | Type | Tier | Target % | Cluster(s) | Applicable Policy | Source |
|---|---|---|---|---|---|---|
| AAPL | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| ABBV | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| AMAT | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| AMD | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| AMZN | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| ASML | equity | T1 | 3.35 | semis (≤25%) | T1 weight 3.35%; semis cluster cap ≤25.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| AVGO | equity | T2 | 1.65 | semis (≤25%) | T2 weight 1.65%; semis cluster cap ≤25.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| BABA | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| BRK.B | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| CAT | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| CEG | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| COST | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| CRM | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| CRWD | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| CVX | equity | band | 0.75 | oil (≤20%) | band weight 0.75%; oil cluster cap ≤20.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| DELL | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| DHR | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| EQIX | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| ETN | equity | band | 0.75 | power_infra (≤20%) | band weight 0.75%; power_infra cluster cap ≤20.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| GEV | equity | T1 | 3.35 | power_infra (≤20%) | T1 weight 3.35%; power_infra cluster cap ≤20.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| GILD | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| GLD | equity | ETF | 2.3 | — | ETF weight 2.3% | `targets.yaml` |
| GNRC | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| GOOGL | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| HOOD | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| IBM | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| INTC | equity | spec | 1.0 | semis (≤25%) | spec weight 1.0%; semis cluster cap ≤25.0% of book; spec fixed at target, no overweight permitted | `targets.yaml` |
| ISRG | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| JNJ | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| JPM | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| KLAC | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| LLY | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| LRCX | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| MA | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| META | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| MLM | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| MRK | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| MRVL | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| MSFT | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| MU | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| NFLX | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| NOW | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| NVDA | equity | T1 | 3.35 | semis (≤25%) | T1 weight 3.35%; semis cluster cap ≤25.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| ORCL | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| PANW | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| PLTR | equity | spec | 1.0 | — | spec weight 1.0%; spec fixed at target, no overweight permitted | `targets.yaml` |
| PWR | equity | T2 | 1.65 | power_infra (≤20%) | T2 weight 1.65%; power_infra cluster cap ≤20.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| QQQ | equity | ETF | 2.3 | — | ETF weight 2.3% | `targets.yaml` |
| RKLB | equity | spec | 1.0 | — | spec weight 1.0%; spec fixed at target, no overweight permitted | `targets.yaml` |
| RTX | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| SHOP | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| SKHY | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| SPCX | equity | spec | 1.0 | — | spec weight 1.0%; spec fixed at target, no overweight permitted | `targets.yaml` |
| SPY | equity | ETF | 2.3 | — | ETF weight 2.3% | `targets.yaml` |
| SYK | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| TMO | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| TSLA | equity | spec | 1.0 | — | spec weight 1.0%; spec fixed at target, no overweight permitted | `targets.yaml` |
| TSM | equity | T1 | 3.35 | semis (≤25%) | T1 weight 3.35%; semis cluster cap ≤25.0% of book; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| UBER | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| UNH | equity | band | 0.75 | — | band weight 0.75%; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| V | equity | T1 | 3.35 | — | T1 weight 3.35%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| VRT | equity | band | 0.75 | power_infra (≤20%) | band weight 0.75%; power_infra cluster cap ≤20.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| WDC | equity | band | 0.75 | semis (≤25%) | band weight 0.75%; semis cluster cap ≤25.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| WMT | equity | T2 | 1.65 | — | T2 weight 1.65%; T1/T2 ceiling 1.5x (gates.t1t2_trim_mult) | `targets.yaml` |
| XOM | equity | band | 0.75 | oil (≤20%) | band weight 0.75%; oil cluster cap ≤20.0% of book; band cap_multiple 1.25x, RSI-gated trim >60 | `targets.yaml` |
| BTC | crypto | crypto sleeve | 10.0 (sleeve aggregate, no per-coin target) | — | crypto sleeve 10% of book (`targets.yaml` crypto.sleeve_pct); no cluster cap applies | `targets.yaml` / `holdings.yaml` — **holdings.yaml shows crypto_shares.BTC=0.00460473, inconsistent with targets.yaml's own comment claiming BTC was fully sold 2026-07-13 (=FA-3, see §6)** |
| ETH | crypto | crypto sleeve | 10.0 (sleeve aggregate, no per-coin target) | — | crypto sleeve 10% of book (`targets.yaml` crypto.sleeve_pct); no cluster cap applies | `targets.yaml` / `holdings.yaml` |
| SOL | crypto | crypto sleeve | 10.0 (sleeve aggregate, no per-coin target) | — | crypto sleeve 10% of book (`targets.yaml` crypto.sleeve_pct); no cluster cap applies | `targets.yaml` / `holdings.yaml` |

**Gap note (portfolio-level, applies to all 68 rows):** neither `holdings.yaml` nor `targets.yaml` records a per-ticker "last verified/synced" timestamp for share counts or tier placement — only `holdings.yaml`'s `margin:` block carries a `synced_at` date. Individual tier-change dates are recoverable only from `targets.yaml`'s free-form comments (present for some tickers, e.g. AAPL's 2026-07-14 promotion, SKHY's 2026-07-10 listing) or the CLAUDE.md Decisions Log — not a structured, queryable field. This is a **pre-existing schema gap, not something this artifact changes or is authorized to fix** (adding such a field would be a `holdings.yaml`/`targets.yaml` schema change, out of scope).

---

## 4. Milestone 2 — Intelligence Coverage & Freshness Audit

**Coverage is opt-in** (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §16) — absence of a record is not itself an error. Company Intelligence's own scope is explicitly **per-company only** (spec §1); ETF and crypto asset types fall structurally outside that scope, not by omission.

| Ticker | Intelligence Record | Coverage Status | Last Reviewed | Next Due | Freshness (as of 2026-07-25) | Registry / Checkpoint | Theme Ref |
|---|---|---|---|---|---|---|---|
| AAPL | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| ABBV | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| AMAT | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| AMD | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| AMZN | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| ASML | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| AVGO | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| BABA | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| BRK.B | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| CAT | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| CEG | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **COST** | **present** (`intelligence/companies/COST.yaml`+`.md`) | current, not overdue | 2026-07-23 | 2026-10-21 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | — |
| CRM | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| CRWD | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| CVX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| DELL | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| DHR | absent (deferred, not rejected — see below) | no record; named in `life_sciences_tools_medtech.yaml` as "deferred, not rejected" (PI-0009); PI-0014 authorized a bounded, conversation-only evidence review (no repository artifact) | n/a | n/a | n/a | not enrolled; no checkpoint row | theme references DHR in evidence text only, not as a member |
| EQIX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| ETN | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **GEV** | **present** (`intelligence/companies/GEV.yaml`+`.md`) | current, not overdue | 2026-07-22 | 2026-10-20 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | ai_infrastructure |
| GILD | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| GLD | not applicable | out of spec scope (ETF, not a company) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| GNRC | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| GOOGL | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| HOOD | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| IBM | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| INTC | absent (bounded review, no artifact) | no record; PI-0014 authorized a bounded, conversation-only evidence review on the TSM.md-documented TSM/INTC overlap question — no repository artifact | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **ISRG** | **present** (`intelligence/companies/ISRG.yaml`+`.md`) | current, not overdue | 2026-07-20 | 2026-10-18 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | life_sciences_tools_medtech |
| JNJ | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| JPM | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| KLAC | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| LLY | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| LRCX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MA | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| META | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MLM | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MRK | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MRVL | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MSFT | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| MU | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| NFLX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| NOW | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **NVDA** | **present** (`intelligence/companies/NVDA.yaml`+`.md`) | current, not overdue | 2026-07-22 | 2026-10-20 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | ai_infrastructure |
| ORCL | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| PANW | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| PLTR | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| PWR | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| QQQ | not applicable | out of spec scope (ETF, not a company) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| RKLB | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| RTX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SHOP | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SKHY | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SPCX | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SPY | not applicable | out of spec scope (ETF, not a company) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SYK | absent (deferred, not rejected — see below) | no record; named in `life_sciences_tools_medtech.yaml` as "deferred, not rejected" (PI-0009); PI-0014 authorized a bounded, conversation-only evidence review (no repository artifact) | n/a | n/a | n/a | not enrolled; no checkpoint row | theme references SYK in evidence text only, not as a member |
| **TMO** | **present** (`intelligence/companies/TMO.yaml`+`.md`) | current, not overdue | 2026-07-18 | 2026-10-16 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | life_sciences_tools_medtech |
| TSLA | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **TSM** | **present** (`intelligence/companies/TSM.yaml`+`.md`) | current, not overdue | 2026-07-19 | 2026-10-17 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | ai_infrastructure |
| UBER | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| UNH | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| V | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| VRT | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| WDC | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| WMT | absent | no record (opt-in, spec §16) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| **XOM** | **present** (`intelligence/companies/XOM.yaml`+`.md`) | current, not overdue | 2026-07-18 | 2026-10-16 | current (90-day cadence) | enrolled (`monitoring_enabled: false`); checkpoint `pending`, no channels established | — |
| BTC | not applicable | out of spec scope (per-company only, §1) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| ETH | not applicable | out of spec scope (per-company only, §1) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |
| SOL | not applicable | out of spec scope (per-company only, §1) | n/a | n/a | n/a | not enrolled; no checkpoint row | — |

**Evidence quality / primary-source coverage, 7 covered companies (summary — full detail lives in each company's own record, not restated here):** COST 15 sources / 6 risks; GEV 8 sources / 5 risks; ISRG 6 sources / 4 risks; NVDA 8 sources / 5 risks; TMO **1 source** / 4 risks; TSM 7 sources / 7 risks; XOM 5 sources / 5 risks. **TMO's single-source count is the weakest evidence base of the seven** — structurally valid (schema-passes, has a conviction rating, has a review date) but thin on independently-corroborating sources relative to the other six. This is a factual observation, not a conclusion about TMO's investment merit, and is not a finding requiring any record change under this artifact's scope.

**Portfolio-role-drift check** (re-run this session via `intelligence_report.py --role-drift`, cross-checked against each company record's own `portfolio_role_ref` field manually): **7 checked, 7 MATCH, 0 MISMATCH** — every existing company record's descriptive `portfolio_role_ref` (COST/GEV/NVDA/TSM: T1; ISRG/TMO: T2; XOM: band) currently matches that ticker's live tier in `targets.yaml`. Per PI-0003/PI-0018/PI-0020/PI-0022 doctrine, `portfolio_role_ref` is descriptive-only and fixed at authoring time — a future match is not guaranteed and a future mismatch would not itself require either side to change; it is recorded here as the current factual state, not as a standing property.

**Margin-relevance evidence status (all 68 assets):** **none captured for any asset.** OPS-0006 §4 assigns capturing per-asset margin-relevant evidence (cyclicality, leverage, balance-sheet strength, refinancing risk, drawdown drivers, etc.) to the future, still-unauthorized **Milestone 3**. No such evidence exists in any of the 7 current company records today, and this artifact does not create any. This is a uniform, portfolio-wide gap — not itemized per-ticker in the tables above, since the answer is identical (none) for all 68 assets.

**Refresh-profile status (all 68 assets):** **not yet defined for any asset.** OPS-0006 §10 names a future governed refresh-profile concept (evidence date, cadence, stale-reason, event triggers, etc.) as a principle and future extension-candidate only — explicitly not implemented, and explicitly preserving `AUTO-0001`'s and the Company Intelligence spec's existing field ownership (`review.cadence_days`/`last_reviewed`/`next_due`/`log`, which the 7 covered companies do already have — see table above). No record has a distinct "refresh profile" beyond its existing `review:` block.

**Event-trigger coverage:** none of the 7 covered companies' `freshness_checkpoints.yaml` rows has any established channel (`checkpoint_status: pending`, `channels: {}` for all 7) — per AUTO-0002's own design, this is the correct, disclosed starting state (checkpoint establishment is separate, per-company reviewed work belonging to a future bootstrap PR, not this filing or any prior one). This is **not** a defect; it is documented, intentional, unactioned infrastructure.

---

## 5. Portfolio-level findings

- **Total governed assets: 68** (65 equity + 3 crypto), reconciled programmatically from `holdings.yaml` against `targets.yaml` with zero missing/duplicated/tier-inconsistent records (§1, §3).
- **Intelligence coverage by asset type:** 7 of 65 equities (10.8%) have a Company Intelligence record; 0 of 3 crypto assets and 0 of 3 ETF assets are in scope for one at all (structural, per spec §1 — not a coverage gap). Of the 7 covered, all 7 are current (not overdue) as of 2026-07-25, matching `intelligence_report.py --staleness`'s own live output re-run this session.
- **Freshness / next-review-date coverage:** all 7 covered companies carry `review.last_reviewed`/`next_due` on a 90-day cadence; earliest `next_due` is TMO/XOM at 2026-10-16, latest is COST at 2026-10-21 — none overdue, none due within the next 30 days as of this audit date.
- **Missing/inconsistent schema usage:** none found — all 7 company records and both theme records parse cleanly against `intelligence_validator.py`/`freshness_validator.py`; all 31 governance decision files parse cleanly against `governance/decisions.yaml`.
- **Duplicate or ambiguous records:** none among the 68 governed assets' tier/cluster placement. One **pre-existing, already-documented** inconsistency: `holdings.yaml`'s `crypto_shares.BTC = 0.00460473` contradicts `targets.yaml`'s own comment text ("BTC has no entry... fully sold 2026-07-13") — this is the same conflict independently identified as **FA-3** in the retained `governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md` (dated 2026-07-24, one day before this artifact), confirmed still present and unresolved. This artifact does not resolve it — FA-3 itself specifies the fix needs "its own separately verified factual-reconciliation change," which is a data-correction action outside Milestones 1–2's inventory/audit scope.
- **Assets lacking primary evidence:** among the 7 covered, TMO's single-source evidence base is comparatively thin (see §4); among the 58 uncovered equities, all lack primary evidence by definition of having no record. INTC, SYK, and DHR specifically have had bounded, conversation-only evidence review under PI-0014, but that review produced no retained repository artifact — from a repository-truth standpoint their coverage status is identical to any other uncovered name.
- **Assets lacking margin-relevance evidence:** all 68 (uniform gap; deferred to future Milestone 3/4, see §4).
- **Assets lacking a usable refresh plan:** all 68 in the OPS-0006 §10 "refresh-profile" sense (not yet defined for anyone); the 7 covered companies do have the pre-existing `review:` cadence/next-due mechanism, which is a materially weaker but real freshness signal already in active use.
- **Shared evidence gaps across economic systems:** the `semis` cluster (13 members) has Company Intelligence coverage for exactly 2 (NVDA, TSM); `power_infra` (4 members) covers 2 (GEV, and PWR is uncovered); `oil` (2 members) covers 1 (XOM, CVX uncovered); the `ai_infrastructure` theme covers 3 (NVDA, GEV, TSM — all already-covered companies, no new gap); the `life_sciences_tools_medtech` theme covers 2 (ISRG, TMO) with 2 deferred candidates (SYK, DHR) already named in its own text.

### Recommended future research batches (advisory only — not authorized, ranked, or requested by this artifact)

Grouped by shared economic system / evidence overlap, to reduce duplication if and when a future, separately authorized Milestone 3 batch is proposed:

1. **semis cluster, uncovered members** (ASML, AVGO, AMD, MU, MRVL, KLAC, LRCX, AMAT, WDC, INTC, SKHY) — 11 of 13 cluster members uncovered; INTC already has PI-0014's conversational groundwork (uncaptured in any file) that a future record could draw on.
2. **power_infra cluster, uncovered members** (ETN, VRT, PWR) — 3 of 4 cluster members uncovered; GEV's existing record already documents the cluster's shared driver.
3. **oil cluster, uncovered member** (CVX) — 1 of 2; XOM's existing record already documents the shared crude-oil mechanism, likely directly reusable context.
4. **life_sciences_tools_medtech theme, deferred candidates** (SYK, DHR) — both already named and reasoned about in the existing theme file and PI-0014's conversational review; a future record for either would extend, not originate, existing analysis.
5. **T1/T2 names with no coverage and no cluster overlap** (AVGO already listed under semis; remaining: ASML listed under semis; MSFT, GOOGL, META, LLY, V, AMZN, CEG, MA, BRK.B, WMT, EQIX, MLM, AAPL) — no shared mechanism identified in this audit; would be independent, single-company batches if ever pursued.

This batching is a grouping suggestion only, based on already-existing shared evidence and cluster/theme structure — it ranks nothing, authorizes nothing, and creates no research charter or trial consumption.

---

## 6. Confirmations

- No tier, target, role, cluster, cap, holding, or allocator-formula value was changed by this artifact.
- No company or theme Intelligence record was completed, rewritten, or refreshed.
- No new external company research was performed; all facts above come from files already in the repository (`holdings.yaml`, `targets.yaml`, `intelligence/`, `governance/`, `operations/WORKSTREAMS.yaml`) plus this session's own re-execution of existing, already-authorized tooling (`pytest`, `intelligence_validator.py`, `freshness_validator.py`, `intelligence_report.py` read-only).
- No scanner, scheduler, notification system, or external integration was built.
- No margin recommendation was made; the 1.8x leverage cap and 30% buffer floor are unchanged and untouched.
- No `MARGIN-0005` S3 authority was created or consumed; zero trials consumed.
- Milestones 3–9 remain `status: proposed`, unauthorized, and unstarted.

---

## 7. Completion Ledger (OPS-0006 §16.2)

Every one of the 68 governed assets has an explicit factual status and next action below — this table **is** the per-asset completion ledger required by §16.2, kept inside this retained artifact rather than in `operations/WORKSTREAMS.yaml` (per §16.2's own instruction that the ledger stay out of the register).

| Ticker | Milestone-1 Status | Milestone-2 Status | Next Action |
|---|---|---|---|
| AAPL | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| ABBV | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| AMAT | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| AMD | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| AMZN | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| ASML | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| AVGO | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| BABA | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| BRK.B | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| CAT | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| CEG | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| COST | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-21); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| CRM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| CRWD | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| CVX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| DELL | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| DHR | current — role/tier/target/cluster/cap consistent | no Company Intelligence record; named in `life_sciences_tools_medtech.yaml` evidence text as "deferred, not rejected" (PI-0009); PI-0014 separately authorized a bounded, conversation-only evidence review on whether DHR's FY2025 mixed segment picture changed in later reporting — no repository artifact produced, and PI-0014 explicitly excluded revisiting the existing TMO-redundancy finding | No Milestone-1/2 action required. Deferred-membership status and PI-0014's conversational findings are not a substitute for a filed record; any future DHR coverage or theme-membership decision needs its own separate authorization. Not requested by this artifact. |
| EQIX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| ETN | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| GEV | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-20); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| GILD | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| GLD | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | No action. ETF asset type is structurally out of spec scope; not requested to be brought into scope by this artifact. |
| GNRC | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| GOOGL | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| HOOD | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| IBM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| INTC | current — role/tier/target/cluster/cap consistent | no Company Intelligence record; PI-0014 authorized a bounded, conversation-only, read-only evidence review on INTC's TSM.md-documented TSM/INTC overlap question — that review produced no repository artifact and selects/authorizes no company record | No Milestone-1/2 action required. PI-0014's conversational findings are not a substitute for a filed record; any future INTC coverage decision needs its own separate PI-XXXX authorization per PI-0016. Not requested by this artifact. |
| ISRG | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-18); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| JNJ | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| JPM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| KLAC | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| LLY | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| LRCX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MA | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| META | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MLM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MRK | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MRVL | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MSFT | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| MU | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| NFLX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| NOW | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| NVDA | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-20); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| ORCL | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| PANW | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| PLTR | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| PWR | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| QQQ | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | No action. ETF asset type is structurally out of spec scope; not requested to be brought into scope by this artifact. |
| RKLB | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| RTX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| SHOP | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| SKHY | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| SPCX | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| SPY | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | No action. ETF asset type is structurally out of spec scope; not requested to be brought into scope by this artifact. |
| SYK | current — role/tier/target/cluster/cap consistent | no Company Intelligence record; named in `life_sciences_tools_medtech.yaml` evidence text as "deferred, not rejected" (PI-0009); PI-0014 separately authorized a bounded, conversation-only evidence review on the theme file's segment-reorganization timing question — no repository artifact produced | No Milestone-1/2 action required. Deferred-membership status and PI-0014's conversational findings are not a substitute for a filed record; any future SYK coverage or theme-membership decision needs its own separate authorization. Not requested by this artifact. |
| TMO | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-16); 90-day cadence; **weakest evidence base of the 7 covered (1 source)** | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016-style authorization, which could specifically target evidence breadth; not requested by this artifact. |
| TSLA | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| TSM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-17); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| UBER | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| UNH | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| V | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| VRT | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| WDC | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| WMT | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | no Intelligence record (opt-in coverage; absence is not itself an error per PORTFOLIO_INTELLIGENCE_SPEC.md §16) | No Milestone-1/2 action required. Candidate for a future, separately authorized Milestone-3 first-coverage decision (own PI-XXXX filing, own selection rationale, per PI-0016); not requested, ranked, or authorized by this artifact. |
| XOM | current — role/tier/target/cluster/cap consistent, no duplicate/ambiguous record found | current record; not overdue (next_due 2026-10-16); 90-day cadence | No Milestone-1/2 action required. Eligible for a future, separately authorized Milestone-3 refresh per PI-0016/PI-0018/PI-0020/PI-0022-style authorization; not requested by this artifact. |
| BTC | **inconsistent record (pre-existing, not newly created here)** — `holdings.yaml` `crypto_shares.BTC` = 0.00460473 (nonzero), but `targets.yaml`'s crypto comment states "BTC has no entry in holdings.yaml's crypto_shares — fully sold 2026-07-13." This is the same conflict independently identified as FA-3 in `governance/audits/WS0002_PHASE_ONE_FABLE_AUDIT_20260724.md` (audited 2026-07-24) and is still present, unresolved, unchanged by PR #150 or this artifact | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | **Not a Milestone-1/2 action, but flagged for the record**: FA-3 already requires "its own separately verified factual-reconciliation change before any crypto-sleeve rebuild logic or Standing Queue wording is next touched." That reconciliation is outside this artifact's authorized scope (data correction, not inventory/Intelligence audit) and is not performed here. |
| ETH | current — tracked via `holdings.yaml` `crypto_shares`; sleeve aggregate target only, no per-coin target | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | No action. Whether Theme/Portfolio Intelligence should ever extend to non-company asset types is unaddressed and explicitly out of scope for this artifact. |
| SOL | current — tracked via `holdings.yaml` `crypto_shares`; sleeve aggregate target only, no per-coin target | not applicable — Company Intelligence spec is per-company only (§1); no schema gap implied | No action. Whether Theme/Portfolio Intelligence should ever extend to non-company asset types is unaddressed and explicitly out of scope for this artifact. |

**Ledger completeness check:** 68 rows above = 68 governed assets identified in §1/§2. No asset omitted; no asset duplicated.

---

## 8. Explicit scope confirmation (re-stated per assigning instructions)

This artifact does **not**: perform Milestone 3 research completion; rewrite any existing Intelligence record; change holdings or targets; change tiers, roles, clusters, or caps; change allocator behavior; add scoring, ranking, aggregation, or computed conviction; connect Intelligence directly to allocation; recommend or implement margin; modify the 1.8x cap or 30% floor; authorize or consume `MARGIN-0005` S3; create scanners, schedules, notifications, or external integrations; generate trading instructions; or perform unrelated cleanup.

**Independent Fable review of this artifact is the pending next step** — this artifact does not mark itself, or WS-0005 Milestones 1–2, `complete`; per OPS-0006 §16.1, that requires this PR to merge, tests/validators to pass, post-merge verification, and register/index synchronization, which is recorded as `status: in_progress` (not `complete`) in `operations/WORKSTREAMS.yaml` alongside this PR while it remains open.
