# Phase 2 Implementation Plan — Margin Governance Layer

_2026-07-17 · Planning only. `decision_log.yaml` (repo root) was created as part of this pass — it's new, inert data nothing reads yet, not a change to production behavior. **No production code (`allocate.py`, `targets.yaml`, `holdings.yaml`, or any file in the live `--cash`/`--review`/`--margin` path) has been modified.** Everything else below is a proposal. Waiting for approval before any of it is implemented._

---

## 1. Governance-layer enforcement mapping

Before any schema or state design, here is exactly how each doctrine requirement from `docs/MARGIN_DOCTRINE.md`'s "Margin Intelligence Engine Doctrine" section is enforced structurally in what follows — not as a promise, as a design property checkable against Sections 3-5 below.

| Doctrine requirement | Enforcement mechanism |
|---|---|
| Margin is NOT a timing signal | The state machine (Section 4) takes exactly three input categories: leverage ratio, buffer %, concentration score. No price, regime, volatility-as-trigger, or valuation input exists anywhere in the schema (Section 3) or the state criteria (Section 4). There is no field to put a timing signal in even by accident. |
| Margin does NOT create alpha | No component proposed here computes or influences a *buy* decision. Every function in Section 4/5 only ever reduces, blocks, or holds — the type signature of every state's "action" is drawn from `{no_change, reduce_new_draws, block_and_recommend_paydown}`, which structurally excludes "increase." |
| Margin amplifies existing portfolio edge, doesn't create it | Unaffected by this phase — `margin_capacity()`'s leverage-cap/buffer-floor math, which already embodies this (it clips borrowing to a fixed ratio of whatever equity already exists), is untouched. |
| Margin states are risk states only, never opportunity states | Section 4's four states (`NORMAL`/`CAUTION`/`RESTRICTED`/`FORCED_DELEVER`) are explicitly, monotonically risk-ordered — each state is strictly a superset of the prior state's risk conditions. There is no state whose criteria involve anything getting *better* triggering a transition; transitions only fire on leverage/buffer/concentration getting worse (or, for de-escalation, genuinely improving back toward Normal — see Section 4's de-escalation note). |
| No "borrow more because conditions look favorable" logic | Directly tested — Section 5's test plan includes a dedicated property-style test (`test_no_state_ever_recommends_increasing_leverage`) that asserts this for every state, not just checks it by inspection. |

---

## 2. `decision_log.yaml` — done, not a proposal

Created at repo root (config/state layer, alongside `targets.yaml`/`holdings.yaml`, not under `docs/` — it's structured data meant to be read by future tooling, not narrative documentation). Schema exactly as requested: `decision_id`, `date`, `category`, `decision`, `rationale`, `supporting_artifact`, `status`.

**Migrated, this pass, exactly two entries** (per explicit "margin doctrine decisions only" scope):
- `MARGIN-0001` — the 2026-07-13 margin doctrine revision (1.8x cap, 30% floor, margin-timing rejected). `supporting_artifact: null` — stated explicitly as doctrine-driven, not backtest-derived, and `status: pending_evidence` rather than `active`, because Track 2 exists specifically to test whether the numeric level is evidence-supported. This distinction (the *structure* being settled doctrine vs. the *specific number* being open) matters enough that collapsing it into a single "active" status would misrepresent where this decision actually stands.
- `MARGIN-0002` — the 2026-07-15 T1/T2 concentration ceiling. `supporting_artifact: reports/t1t2_trim_backtest.md`, `status: active` (the return question that backtest tested is closed and the rule is live in production; the capital-impairment judgment behind it was a separate doctrine call, noted as such).

**Explicitly not migrated this pass:** every other `CLAUDE.md` Decisions Log entry, including the closely-related "Semis cluster cap: leverage asymmetry" entry (2026-07-14) — it discusses leverage's effect on a cap's denominator but isn't itself a margin-policy decision. Flagged as a reasonable candidate for a broader future migration pass, not started here.

---

## 3. Margin policy schema — proposed `targets.yaml` extension (NOT applied)

```yaml
margin:
  # --- EXISTING, unchanged ---
  leverage_cap: 1.8
  buffer_floor_pct: 30.0

  # --- PROPOSED, not yet added to the real targets.yaml ---
  states:
    caution:
      leverage_fraction_of_cap: null    # e.g. 0.65 -- PLACEHOLDER, not evidence-backed
      buffer_comfort_multiplier: null   # e.g. 1.75 -- PLACEHOLDER
    restricted:
      leverage_fraction_of_cap: null    # e.g. 0.85 -- PLACEHOLDER
      buffer_comfort_multiplier: null   # e.g. 1.25 -- PLACEHOLDER
    # forced_delever has no new parameter -- it reuses buffer_floor_pct directly,
    # exactly as margin_capacity() already does today.

  concentration_adjustment:
    enabled: true
    tightening_coefficient: null   # the "k" in inner_threshold = cap x base x (1 - k x score),
                                     # per MARGIN_INTELLIGENCE_DESIGN.md §3 -- PLACEHOLDER
    min_fraction: null             # floor on how far concentration can tighten a threshold --
                                     # PLACEHOLDER

  repayment:
    redirect_fraction_caution: null     # PLACEHOLDER -- pending the repayment-policy backtest
    redirect_fraction_restricted: null  # PLACEHOLDER -- same
    redirect_fraction_forced: 1.0       # NOT a placeholder -- this matches existing production
                                          # behavior already (Forced state blocks all margin buys;
                                          # 100% of any trim proceeds already redeploy or pay debt,
                                          # nothing new is being invented here)

  debt_reduction_triggers:
    consecutive_syncs_in_elevated_state: null   # PLACEHOLDER -- e.g. "recommend a paydown after
                                                   # N consecutive Caution/Restricted syncs" -- no
                                                   # N is proposed; this needs its own evidence,
                                                   # not a guess

  emergency_deleveraging:
    repayment_target_buffer_multiplier: null   # PLACEHOLDER -- e.g. 1.5, per
                                                  # MARGIN_INTELLIGENCE_DESIGN.md §3's
                                                  # recommended_paydown() formula; restores buffer
                                                  # above the floor by this multiple so a paydown
                                                  # recommendation doesn't immediately re-trigger
```

**Every `null` above is deliberate, not an oversight.** Per the standing discipline this whole project runs on (no parameter gets a default without evidence — the same rule that kept the T1/T2 ceiling's multiplier, the repayment-redirect fraction, and the concentration-adjustment coefficient all unset in the prior design revisions), this schema defines *shape*, not *values*. The example numbers in comments (0.65, 1.75, etc.) are illustrations of what a filled-in value would look like, not proposed defaults — filling any of them in is Phase 3+ work, gated on the corresponding backtest.

**Why this lives in `targets.yaml` and not a new file:** `targets.yaml` is already config-truth for every other gate/cap/threshold in this system (`gates.t1t2_trim_mult`, `caps.clusters`, etc.) — a parallel margin-policy file would fragment config-truth into two places for no structural reason. This proposal extends the existing `margin:` block, consistent with how the T1/T2 ceiling extended the existing `gates:` block rather than inventing a new file.

---

## 4. Margin state machine — design (NOT implemented)

**Four states, exactly as specified, all risk classifications:**

```
NORMAL ──────▶ CAUTION ──────▶ RESTRICTED ──────▶ FORCED_DELEVER
   ▲               │                 │                    │
   └───────────────┴─────────────────┴────────────────────┘
        (de-escalation: re-evaluated fresh every run from
         current leverage/buffer/concentration -- no state
         has "memory" that keeps it stuck once conditions
         genuinely improve; see note below)
```

| State | Objective criteria | Proposed system behavior (Phase 3+, not this phase) |
|---|---:|---|
| `NORMAL` | leverage ≤ `caution.leverage_fraction_of_cap` × cap, AND buffer ≥ floor × `caution.buffer_comfort_multiplier` | No change from current behavior. |
| `CAUTION` | leverage between the Caution and Restricted thresholds, OR buffer between floor×`restricted.buffer_comfort_multiplier` and floor×`caution.buffer_comfort_multiplier` | **Informational only** — displayed, no behavior change. Matches the "Elevated" state from `MARGIN_INTELLIGENCE_DESIGN.md` Rev 1/2, now split into two granular tiers per this revision's explicit 4-state request. |
| `RESTRICTED` | leverage above the Restricted threshold (but still ≤ cap — `margin_capacity()`'s existing clip already prevents exceeding the cap itself), OR buffer between the floor and floor×`restricted.buffer_comfort_multiplier` | New margin-funded buys are reduced (not fully blocked) — the specific mechanism (a tighter effective sub-cap, or a required redirect-to-debt fraction on trim proceeds) is exactly what Section 3's `redirect_fraction_restricted` placeholder is for, and is not decided in this document. |
| `FORCED_DELEVER` | buffer < `buffer_floor_pct` (existing rule, unchanged) | Existing behavior (block all margin-funded buys) — **unchanged in this phase.** A concrete repayment-amount recommendation (per `MARGIN_INTELLIGENCE_DESIGN.md` §3's `recommended_paydown()` formula) is proposed but not built this phase either. |

**Concentration adjustment applies uniformly**: `concentration_risk_score()` (already designed, `MARGIN_INTELLIGENCE_DESIGN.md` §3/§5) tightens every threshold above via the `tightening_coefficient`, never loosens one — a concentrated book reaches `CAUTION`/`RESTRICTED` at a *lower* leverage ratio than a diversified one would, exactly the mechanism the earlier design revision built for Goal 5 of that document.

**Explicitly excluded state names and why, restated from the instruction:** `OPPORTUNISTIC`, `AGGRESSIVE`, `BULLISH`, `VALUATION_OPPORTUNITY` — none of these describe account risk; all of them describe market opportunity, which is exactly the category `MARGIN_DOCTRINE.md`'s doctrine section rules out. There is no version of this state machine, in this phase or any future one, that adds a fifth state along these lines.

**De-escalation note:** every state is computed fresh, every run, from the account's current leverage/buffer/concentration — there is no persisted "we were in Restricted last time so we stay cautious" memory. This is a deliberate simplification worth flagging: it means a single good sync (e.g., a large paydown) can move the account from `FORCED_DELEVER` straight back to `NORMAL` in one step. Whether that's the right behavior (vs. requiring some cooldown/hysteresis before fully de-escalating) is an open design question **not resolved in this document** — flagged here rather than silently decided either way, since hysteresis logic would itself need its own justification and possibly its own test.

---

## 5. Test plan (test cases specified; test code not written this phase)

Every test below is a **pure-function unit test**, no live data, no I/O — same standard as the existing 12 tests in `test_margin.py`. Proposed home: extend `test_margin.py` directly (it already tests the function this extends, `margin_capacity()`) rather than create a parallel file, unless the new module (Section 6) ends up large enough to warrant its own test file — a decision deferred until the module actually exists.

| Test | Cases |
|---|---|
| **Leverage cap enforcement** | Already covered for the hard cap by `test_margin.py`'s existing 7 `margin_capacity()` tests — unchanged, not re-tested here. **New**: state classifier correctly identifies `RESTRICTED` at a leverage level between the Restricted threshold and the cap, and `NORMAL` at a leverage level below the Caution threshold, using placeholder threshold values passed as test fixtures (not the real, still-unset config values). |
| **Buffer floor enforcement** | Already covered for the hard floor (`forced_delever` at exactly-below vs. exactly-at) by existing tests. **New**: `CAUTION` and `RESTRICTED` correctly trigger on buffer values between the floor and the comfort multipliers, boundary-tested at each threshold exactly (same "exactly at floor is not forced" precedent the existing suite already set). |
| **Concentration tightening** | A leverage level that classifies as `NORMAL` at concentration score 0.0 classifies as `CAUTION` or `RESTRICTED` at concentration score 1.0, using the same threshold inputs — directly verifies the tightening mechanism does something, not just that it's wired in. Concentration score itself: all-clusters-under-cap → score < 1.0 and matches the tightest name; one cluster exactly at cap → score == 1.0; empty roster → score == 0.0, not an error. |
| **Forced delever behavior** | Existing coverage (buffer < floor → `allowed == 0.0`, `forced is True`) unchanged. **New**: once `recommended_paydown()` exists (Phase 3+), its own test — a known debt/leverage combination produces the expected leverage-based estimate; `NORMAL`/`CAUTION`/`RESTRICTED` states produce no paydown recommendation (only `FORCED_DELEVER` computes one, per the architecture). |
| **Repayment trigger logic** | `repayment_split()` (Phase 3+): `NORMAL` → 100% of trim proceeds redeploy, 0% to debt. `RESTRICTED` → split matches whatever `redirect_fraction_restricted` is configured as, tested at two different fraction values to prove it's parameterized, not hardcoded. `FORCED_DELEVER` → 100% to debt (matches existing behavior, not new). |
| **No state can recommend increasing leverage** | The one explicitly-requested structural test, treated as a property test rather than a handful of examples: for every `(leverage, buffer, concentration_score)` input combination in a systematic sweep (e.g., leverage from 0 to 2x cap in fine steps, buffer from 0% to 100%, concentration from 0.0 to 1.5), assert the resulting state's associated action is never anything that would increase margin usage — i.e., assert the action is always drawn from the closed set `{no_change, reduce_new_draws, block_and_recommend_paydown}` and never, structurally, `increase`. This test should fail loudly (not silently pass) if a future edit ever adds an `increase` action to the enum at all, regardless of whether any state currently uses it — the test asserts against the full domain of possible inputs, not just currently-reachable states. |

---

## 6. Proposed files (summary)

| File | Status this phase | Purpose |
|---|---|---|
| `decision_log.yaml` | **Created** | Machine-readable decision record, 2 entries, Section 2. |
| `docs/PHASE2_IMPLEMENTATION_PLAN.md` | **Created** (this document) | The plan itself. |
| `targets.yaml` | **Not modified** — Section 3's schema is a proposal only | Would eventually carry the new `margin:` sub-keys, all `null`-valued until backtest evidence fills them in. |
| `margin_state.py` (new) | **Not created** | Proposed home for the pure functions: `concentration_risk_score()`, `classify_margin_state()`, `recommended_paydown()` (Phase 3+), `repayment_split()` (Phase 3+) — mirrors `indicators.py`/`regime_gate.py`'s existing pattern (pure functions, no I/O, importable and testable in isolation). |
| `test_margin_state.py` or an extension of `test_margin.py` | **Not created** | Section 5's test plan, once `margin_state.py` exists to test. |
| `allocate.py` | **Not modified** | Would eventually gain: a new field on `margin_capacity()`'s return contract or a wrapping call to `classify_margin_state()`, and a new display block in `render()`. No behavior change to `plan()`'s buy/trim logic is proposed in this phase — display-only integration, matching `MARGIN_INTELLIGENCE_DESIGN.md`'s Phase 2d ("informational integration only"). |

## 7. Data flow diagram (proposed end state, not current state)

```
targets.yaml (margin: block,          holdings.yaml (margin.debt,
including new null-valued              margin.buffer_pct,
state/concentration/repayment          live-priced holdings for
config -- Section 3)                    concentration inputs)
        │                                        │
        └───────────────┬────────────────────────┘
                          ▼
              margin_state.py (NEW, pure functions)
              ├─ concentration_risk_score()
              ├─ classify_margin_state()  ──────▶  NORMAL/CAUTION/RESTRICTED/FORCED_DELEVER
              ├─ recommended_paydown()     (Phase 3+, only when FORCED_DELEVER)
              └─ repayment_split()          (Phase 3+, only when state != NORMAL)
                          │
                          ▼
              allocate.py's render() -- NEW display block
              (state label + recommendation, informational
               this phase; behavior change is Phase 3+ and
               gated on its own backtest per repayment_split())
                          │
                          ▼
                   stdout + logs/*.md
                   (same as every existing render() output)

decision_log.yaml -- parallel, independent artifact. Nothing in the
flow above reads it yet. Written by a human (or future tooling) when
a decision is made; a future capability (not this phase) could have
render() or a --health report cite it directly ("current 1.8x cap:
see MARGIN-0001") -- flagged as a natural next step, not built here.
```

---

## What this phase deliberately does not do

- Does not add anything to `targets.yaml`. The schema in Section 3 is fully specified but exists only in this document until reviewed.
- Does not write `margin_state.py` or any test code. Section 5 is a test *plan* — the cases are specified precisely enough to write directly from, but nothing is implemented.
- Does not change `allocate.py`'s behavior in any way, including display — even the "informational only" render() integration described in Section 7 is proposed, not built.
- Does not pick any of the placeholder values in Section 3's schema. Every threshold, coefficient, and fraction stays `null` pending its own backtest, exactly as the standing project discipline requires.

Waiting for approval before implementing any part of Sections 3-6.
