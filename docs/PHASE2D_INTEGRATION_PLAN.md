# Phase 2D Integration Plan — Wiring `margin_state.py` into `allocate.py`

_2026-07-17 · Planning only. `allocate.py` has not been modified — every line number and code excerpt below was read directly from the file as it exists right now, not recalled from memory. No code is written in this pass. Stop point: this document, awaiting approval._

---

## 1. Current allocation flow — exact mapping

```
holdings.yaml (margin: debt, buffer_pct, synced_at)
        │
        ▼
main(), line 871-874:
  margin_state = holdings_yaml.get("margin", {}) or {}   ◀── local dict, NAME COLLISION, see §3
  margin_debt = float(margin_state.get("debt", 0.0))
  margin_buffer_pct = margin_state.get("buffer_pct")  (float or None)
        │
        ▼
main(), line 896-898:
  result = plan(targets, holdings, roster, metrics, regime_ok, regime_known,
                args.cash, margin_debt=margin_debt,
                margin_buffer_pct=margin_buffer_pct, margin_requested=args.margin)
        │
        ▼
plan(), line 180-182 (margin_capacity() call):
  gross = sum(float(v) for v in holdings.values())          [line 179]
  net_equity, margin_allowed, forced_delever, margin_block_reason =
      margin_capacity(gross, margin_debt, cash, leverage_cap,
                       margin_buffer_pct, buffer_floor_pct, margin_requested)
        │
        ▼
plan(), line 384-391 (return dict):
  result["margin"] = {
      "gross", "net_equity", "debt", "buffer_pct", "buffer_floor_pct",
      "leverage_current", "leverage_cap", "requested", "allowed",
      "used", "forced_delever", "block_reason"
  }
  result["clusters"] = [{"name", "value", "pct"} for each cluster]   ◀── cluster
                                                                          proximities
                                                                          derivable
                                                                          from here
        │
        ▼
main(), line 899: result["margin"]["synced_at"] = margin_state.get("synced_at")
        │
        ▼
main(), line 911: out = render(result, review=args.review)
        │
        ▼
render(), line 499-537 ("## Margin" section):
  mg = result["margin"]
  if mg["debt"] > 0 or mg["requested"] > 0:      ◀── EXISTING GATE, see §4
      ... renders gross/equity, debt, leverage vs cap, buffer vs floor,
          forced-delever warning, staleness warning ...
```

**Where margin data is currently loaded:** `main()`, lines 871-874 (from `holdings.yaml`) and line 897-898 (`args.margin`, from the CLI).

**Where `margin_capacity()` currently operates:** `plan()`, lines 180-182 — the sole place leverage-cap clipping and the buffer-floor hard cutoff actually happen. This is the function that determines `deployable` (line 184) and therefore every dollar amount in `buys`/`trims`. **Nothing in this integration plan touches this function or this call.**

**Where the rendered margin section is generated:** `render()`, lines 499-537, gated by `mg["debt"] > 0 or mg["requested"] > 0` (line 500).

**T1/T2 and cluster-cap trims** happen inside `plan()`'s main per-ticker loop (between the `margin_capacity()` call and the return statement) — `cluster_value` is fully populated by the time `plan()` returns (used to build `result["clusters"]`), but **individual T1/T2 proximity ratios (current/target vs. the 1.5x ceiling) are computed inline during the loop and are not retained anywhere in `plan()`'s return dict.** This is a real, concrete finding, not a hypothetical concern — flagged precisely in §3.

---

## 2. Integration philosophy — confirmed compatible, not just asserted

The required boundary (risk overlay, not a trading signal) is checked against what `margin_state.py` actually does, per the Phase 2B review already on record:

| Requirement | Status |
|---|---|
| May block unsafe leverage | Already true — `margin_capacity()` does this today, unchanged by this integration. `classify_margin_state()` adds a *descriptive* layer (state label), it doesn't add a second blocking mechanism. |
| May warn about risk | New capability this integration adds — the `CAUTION`/`RESTRICTED` states, informational only. |
| May reduce permitted margin usage | **Not built in this integration.** `RESTRICTED`'s proposed behavior change (reducing new draws) is Phase 3+ per the Phase 2 plan — this pass is display-only. |
| May NOT create buy signals | Confirmed structurally — `ALLOWED_ACTIONS` has no buy-adjacent member (Phase 2B review, Section 2). |
| May NOT identify opportunities | Confirmed — no valuation/price-target input exists anywhere in `margin_state.py`'s parameter list. |
| May NOT override allocation doctrine | Confirmed by construction in §3 below — the integration point is chosen specifically so `classify_margin_state()`'s output cannot reach any allocation-math variable. |
| May NOT recommend timing | Confirmed — no regime/volatility/drawdown-as-trigger input exists in `margin_state.py`. |

---

## 3. Smallest integration surface

**One import, in `allocate.py`'s import block:**
```python
from margin_state import classify_margin_state, concentration_risk_score
```
**Not** `import margin_state` as a bare module import. This is not a style preference — `main()` already has a local variable literally named `margin_state` (line 871: `margin_state = holdings_yaml.get("margin", {}) or {}`, read again at lines 872-874 and 899). Because Python resolves a name as local to the whole function the moment it's assigned anywhere in that function, `import margin_state` followed by any later reference like `margin_state.classify_margin_state(...)` inside `main()` would resolve to the **local dict**, not the module — either an `AttributeError` or, worse, a silent wrong-value bug depending on exact placement. Importing the specific functions by name sidesteps this collision entirely; no reference to the bare name `margin_state` is ever needed in the integration code.

**One calculation call, in `main()`, placed after `result = plan(...)` returns (line 898) and before `render()` is called (line 911) — not inside `plan()`:**

```python
cluster_proximities = {f"cluster:{c['name']}": c["value"] / (result["book"] * c["pct"] / 100.0)
                        for c in result["clusters"] if c["pct"] > 0}
concentration_score, concentration_source = concentration_risk_score(cluster_proximities)

margin_cfg = targets.get("margin", {})
result["margin_state"] = classify_margin_state(
    gross=result["margin"]["gross"],
    margin_debt=result["margin"]["debt"],
    buffer_pct=result["margin"]["buffer_pct"],
    leverage_cap=result["margin"]["leverage_cap"],
    buffer_floor_pct=result["margin"]["buffer_floor_pct"],
    concentration_score=concentration_score,
    concentration_source=concentration_source,
    caution_leverage_fraction=margin_cfg.get("states", {}).get("caution", {}).get("leverage_fraction_of_cap"),
    restricted_leverage_fraction=margin_cfg.get("states", {}).get("restricted", {}).get("leverage_fraction_of_cap"),
    caution_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("caution", {}).get("buffer_comfort_multiplier"),
    restricted_buffer_comfort_multiplier=margin_cfg.get("states", {}).get("restricted", {}).get("buffer_comfort_multiplier"),
    concentration_tightening_coefficient=margin_cfg.get("concentration_adjustment", {}).get("tightening_coefficient") or 0.0,
    concentration_min_fraction=margin_cfg.get("concentration_adjustment", {}).get("min_fraction") or 0.5,
)
```

This is attached to `result` (a plain dict already threaded through to `render()`), not passed as a new `render()` parameter — `render()`'s signature (`render(result, review)`) does not change.

**Named limitation, stated honestly rather than worked around:** the cluster-proximity dict above is derivable cleanly from `result["clusters"]` (already present, no `plan()` change needed). **T1/T2 proximities are not** — per §1's finding, they're computed inline during `plan()`'s loop and never retained. This integration pass **omits T1/T2 names from the concentration score** rather than reaching into `plan()` to extract them (which would violate "avoid rewriting `plan()`"). The concentration score is therefore *cluster-cap-only* in this first integration, not the full picture the Phase 2 design originally envisioned. Two honest options for closing this gap, **neither exercised in this pass**: (a) a small, separate `targets.yaml`-driven recomputation of T1/T2 ratios in `main()` (a few lines, duplicating logic that already exists in `plan()` — some risk of drift between the two copies), or (b) a minimal, explicitly-scoped future change to `plan()`'s return dict adding a `t1t2_proximities` key (touches `plan()`, needs its own review). Recommend deferring this decision to a future, explicitly-scoped pass rather than deciding it here.

**Given real config today:** `targets.yaml`'s `margin:` block has none of Section 3's proposed sub-keys yet (only `leverage_cap`/`buffer_floor_pct` exist) — every `.get(...)` chain above resolves to `{}` and then `None`, meaning **`classify_margin_state()` will only ever return `NORMAL` or `FORCED_DELEVER` in production today**, exactly as intended (`CAUTION`/`RESTRICTED` require thresholds that don't exist yet). This is the correct, honest behavior for this integration — not a bug to fix before shipping it.

**One render addition, in `render()`, nested inside the existing gate (line 500), not a new top-level conditional:**

```python
if mg["debt"] > 0 or mg["requested"] > 0:
    ... existing lines 501-537, completely unchanged ...
    ms = result.get("margin_state")
    if ms is not None:
        L.append("")
        L.append(f"**Margin risk state: {ms.current_state}**"
                  + (f" — {'; '.join(ms.reasons)}" if ms.reasons else ""))
```

Placed inside the existing `if mg["debt"] > 0 or mg["requested"] > 0:` block, not a new one — this is the specific design choice that makes §4's "unchanged when debt = 0" compatibility check true by construction, not by a separate check. `result.get("margin_state")` (not `result["margin_state"]`) so `render()` degrades gracefully if ever called directly with a `result` dict that predates this integration (e.g., a future test that constructs a minimal fixture) rather than raising `KeyError`.

**What is explicitly avoided, per instruction:**
- `plan()` is not modified — not its signature, not its internals, not its return dict.
- No existing render() line changes — only new lines are added, nested in the existing gate.
- No allocation mathematics changes — `deployable`, `buys`, `trims`, `cash_left` are computed identically before and after this integration; the new call happens strictly after `plan()` has already returned, so there is no code path by which its output could feed back into allocation math even by accident.

---

## 4. Compatibility checks

**Margin debt = 0:** `render()`'s existing gate (`mg["debt"] > 0 or mg["requested"] > 0`) is `False`, so the entire "## Margin" section — including the new state line, which is nested inside it — does not render. Output is **byte-identical** to today's behavior. (The `classify_margin_state()` call in `main()` still runs and computes a result, harmlessly — it's just never displayed. This is fine and cheap; no need to skip the calculation itself, only the display.)

**Margin data missing** (`buffer_pct is None`, e.g. never synced): `margin_capacity()`'s existing behavior is unchanged (leverage cap still applies, buffer gate skipped — `test_unsynced_buffer_skips_buffer_gate_applies_leverage_only` already covers this and is untouched). `classify_margin_state()` handles `buffer_pct=None` gracefully per Phase 2B (`verify_margin_data` action, no forced state) — confirmed already tested in `test_margin_state.py`. The new render line would show `NORMAL` (or `FORCED_DELEVER` if leverage alone breaches the cap) with a reason noting buffer is unavailable — informational only, no crash, no behavior change to buys/trims.

**Normal leverage:** No change to `margin_capacity()`, no change to `deployable`/`buys`/`trims`. The only new output is a `NORMAL` state line inside the existing Margin section (only shown when debt > 0, per the gate above).

**Existing hard constraints remain exactly as they are:**
- **Leverage cap** — enforced solely by `margin_capacity()` (line 153: `max_by_leverage = max(0.0, leverage_cap * (net_equity + cash) - gross - cash)`), untouched by this integration.
- **Buffer floor** — enforced solely by `margin_capacity()` (line 150-152, hard cutoff), untouched by this integration.

`classify_margin_state()` reads the *outcome* of these two mechanisms (via `result["margin"]`, already computed by the time it's called) — it cannot influence them, because it's called after they've already run and its output is never fed back into `plan()`.

---

## 5. Testing plan (before implementation)

1. **Existing 80 tests must remain passing, unmodified.** No test file changes are needed to satisfy this — none of `test_margin.py`'s `plan()`-calling tests construct or inspect a `result["margin_state"]` key, and `plan()` itself isn't touched, so they're unaffected by construction, not by careful avoidance.

2. **New integration tests** (proposed home: a new `test_allocate_margin_state.py`, or a new section in `test_margin.py` — decide at implementation time based on size):
   - A `plan()` result with `debt=0` → after the proposed `main()`-equivalent logic runs, `render()`'s output contains no `"Margin risk state"` text at all (not just "state is NORMAL" — the line must be **absent**, matching the existing gate).
   - A `plan()` result with `debt>0`, healthy leverage/buffer, no config thresholds set → rendered state text says `NORMAL`.
   - A `plan()` result with `forced_delever=True` (buffer below floor) → rendered state text says `FORCED_DELEVER`, and — this is the important cross-check — the *existing* "⚠️ FORCED DE-LEVER" warning (line 520-523) still appears unchanged, so the report shows both the existing block-reason message and the new state line, consistently agreeing with each other (both should indicate an emergency, from two independently-computed sources: `margin_capacity()`'s `forced_delever` flag and `classify_margin_state()`'s independent buffer/leverage check).
   - A missing-buffer case (`buffer_pct=None`) → renders `NORMAL` (or `FORCED_DELEVER` if leverage alone breaches) with no crash, and the existing "unsynced" buffer display (line 502) is unaffected.

3. **Snapshot comparison of rendered reports, before vs. after — a concrete procedure, not just a description:** capture `render(result, review=...)`'s output for a small, fixed set of synthetic `result` dicts (e.g., the exact fixtures `test_margin.py` already builds for its `plan()` tests) **before** the integration code is written, save as reference text; re-run the identical fixtures **after** the integration lands; diff the two. The diff must show **only** the new `"**Margin risk state: ...**"` line(s) added inside the existing Margin section, and **zero** difference anywhere else in the report (buy/trim tables, summary line, cluster lines, crypto section, everything). This is the same before/after diff discipline already used for the Phase 1 backtest-helper dedup (`git stash`, run, compare, restore) — same rigor, applied to `render()`'s output instead of a backtest script's.

4. **Test that `margin_state` cannot increase allocation** — the specific regression test requested: assert that `plan()`'s return dict (`buys`, `trims`, `cash_left`, `deployable`-derived figures) is **identical** whether or not the proposed `main()` integration code runs afterward. Concretely: call `plan()` once, capture its return dict verbatim; separately run the full proposed integration snippet (concentration score + `classify_margin_state()` + attaching `result["margin_state"]`); assert every key in the original `plan()` return dict except the newly-added `"margin_state"` key is unchanged (same object identity or equal value) after the integration code runs. This is true by construction given §3's design (the call happens strictly after `plan()` returns, and nothing about it can reach backward into `plan()`'s already-computed values) — the test exists to make that structural guarantee an enforced regression check, not just an architectural claim, the same way the Phase 2B property test made "no action recommends increasing leverage" a checked fact rather than an assertion in a docstring.

---

## Open items for approval, not decided in this document

- Whether to close the T1/T2-proximity gap (§3) now, later, or not at all for the concentration score — flagged, not resolved.
- Exact test file placement (new file vs. extending `test_margin.py`) — a implementation-time call, not a design blocker.

Stopping here. No code written. Awaiting approval before implementing this plan.
