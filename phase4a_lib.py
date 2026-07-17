"""
phase4a_lib.py — Phase 4A concentration-margin research, execution-layer
helpers.

Pure, additive utilities used ONLY by run_phase4a_research.py. Does NOT
modify allocate.py, targets.yaml, holdings.yaml, or margin_state.py.
Implements NO concentration controls, NO new margin rules, NO cluster-cap
changes, NO leverage rules — this module only measures and constructs
scenario inputs; every value it returns is an observation, never a
recommendation or a rule.

Per docs/PHASE4A_ASSUMPTION_RESOLUTION.md §3a/§3b: everything here is
derivable from margin_simulation.py's existing (now, as of this phase,
Phase-4A-extended) SimulationResult output — book_values, gross_series,
leverage_series, events, and the new tracked_values field (the one
genuine engine extension this phase required, since no existing output
exposed per-ticker value over time). Nothing here duplicates
margin_state.py's concentration_risk_score() — that scorer stays
read-only/reference-only per the resolution document, never imported
into a hypothetical simulation loop, preserving margin_simulation.py's
existing isolation boundary from margin_state.py.
"""

from __future__ import annotations

from dataclasses import dataclass


# ── scenario construction (weights / price data) ───────────────────────────

def inflate_weights(weights: dict[str, float], tickers: list[str],
                    multiplier: float) -> dict[str, float]:
    """Synthetic concentration construction (docs/PHASE4A_ASSUMPTION_
    RESOLUTION.md §1, option 1): multiply the named ticker(s)' target
    weight(s) by `multiplier`, leave every other ticker's raw weight
    untouched. Redistribution happens automatically, not as an explicit
    step here: simulate()'s allocation math normalizes every ticker's
    target dollar amount by the SUM of all weights each day
    (`book * weights[s] / w_sum`), so inflating one ticker's raw weight
    increases that sum's denominator, which mechanically shrinks every
    other ticker's proportional share — an explicit proportional-
    redistribution pass would double-count this effect.

    Returns a NEW dict; does not mutate `weights`."""
    if multiplier < 0:
        raise ValueError(f"multiplier must be >= 0, got {multiplier}")
    out = dict(weights)
    for t in tickers:
        if t in out:
            out[t] = out[t] * multiplier
    return out


def apply_synthetic_shock(aligned: dict[str, tuple[list, int | None]], ticker: str,
                          shock_pct: float, start_idx: int, duration_days: int
                          ) -> dict[str, tuple[list, int | None]]:
    """Hypothetical stress construction (docs/PHASE4A_ASSUMPTION_
    RESOLUTION.md §2a, secondary/robustness-testing arm only — historical
    replay, using the real price series unmodified, remains primary).
    Overlays a linear decline of `shock_pct` (negative = decline, e.g.
    -40.0) onto `ticker`'s close-price series over `duration_days`
    trading days starting at `start_idx`, then holds the shocked level
    flat for the remainder of the series (no automatic recovery
    modeled — a disclosed simplification: this constructs a stress
    entry, not a full stress-and-recovery price path).

    Returns a NEW aligned dict; does not mutate the input. Only
    `ticker`'s series is modified; every other ticker's series is
    passed through unchanged (same list objects, not copied, since
    they are not modified)."""
    if not (start_idx >= 0):
        raise ValueError(f"start_idx must be >= 0, got {start_idx}")
    if duration_days <= 0:
        raise ValueError(f"duration_days must be > 0, got {duration_days}")
    out = dict(aligned)
    closes, first_elig = aligned[ticker]
    new_closes = list(closes)
    n = len(new_closes)
    end_idx = min(start_idx + duration_days, n)
    base = new_closes[start_idx] if start_idx < n and new_closes[start_idx] is not None else None
    if base is not None:
        for i in range(start_idx, end_idx):
            if new_closes[i] is None:
                continue
            progress = (i - start_idx + 1) / duration_days
            new_closes[i] = base * (1.0 + (shock_pct / 100.0) * min(1.0, progress))
        shocked_level = new_closes[end_idx - 1] if end_idx > start_idx else base
        for i in range(end_idx, n):
            if new_closes[i] is not None:
                new_closes[i] = shocked_level
    out[ticker] = (new_closes, first_elig)
    return out


def ticker_own_max_drawdown(aligned: dict[str, tuple[list, int | None]], ticker: str) -> float:
    """Real historical max drawdown (%) of one ticker's own price series,
    ignoring None (not-yet-eligible) entries. Used as a calibration
    reference for stress severity and for worst_case_concentration_
    impact()'s position_max_drawdown_pct input — the same reference-
    number role t1t2_trim_backtest.md's NVDA -66.4% figure already
    played for a real, cited decomposition."""
    closes = [c for c in aligned[ticker][0] if c is not None]
    if not closes:
        return 0.0
    peak = closes[0]
    worst = 0.0
    for c in closes:
        peak = max(peak, c)
        if peak > 0:
            worst = min(worst, c / peak - 1.0)
    return worst * 100.0


# ── concentration measurement ───────────────────────────────────────────────

def concentration_series(tracked_values: dict[str, list[float]],
                         book_values: list[float]) -> list[float]:
    """Combined % of book each day for ALL tracked tickers together
    (e.g. every semis-cluster member tracked at once) — sum the tracked
    tickers' dollar values day by day, divide by that day's book value.
    Returns 0.0 for a day with book_value <= 0 rather than raising (a
    degenerate simulation state this harness could in principle produce
    very early in a window before any deposit has landed, not an
    error)."""
    if not tracked_values:
        return [0.0] * len(book_values)
    n = len(book_values)
    out = []
    for i in range(n):
        total = sum(series[i] for series in tracked_values.values())
        book = book_values[i]
        out.append((total / book * 100.0) if book > 0 else 0.0)
    return out


def time_above_threshold_pct(series: list[float | None], threshold: float) -> float:
    """% of valid (non-None) days where `series` exceeds `threshold`.
    Generalizes margin_simulation.time_near_leverage_cap()'s pattern to
    any series/threshold pair (concentration %, leverage ratio, etc.) —
    not reimplementing that function, just applying its same shape to a
    threshold that isn't specifically the leverage cap."""
    valid = [v for v in series if v is not None]
    if not valid:
        return 0.0
    above = sum(1 for v in valid if v > threshold)
    return above / len(valid) * 100.0


# ── forced deleveraging ─────────────────────────────────────────────────────

def forced_deleveraging_events(leverage_series: list[float | None],
                               leverage_cap: float, epsilon: float = 1e-6) -> list[int]:
    """Day indices where simulated leverage exceeds the scenario's own
    leverage_cap — a PASSIVE breach (gross fell while existing debt did
    not, since none of Phase 4A's scenarios run an active repayment
    model per docs/PHASE4A_ASSUMPTION_RESOLUTION.md §4's "leverage fixed"
    design), not something simulate() itself corrects (this harness
    never force-sells to cure a leverage breach outside an active
    repayment policy, which none of Phase 4A's scenarios use). This is a
    pure OBSERVATION of what real doctrine's hard leverage cap would
    require correcting, in the tradition of margin_capacity()'s own
    "would this be allowed" logic — implements no new rule, only
    detects when the existing, real, doctrine-fixed cap would have been
    breached.

    `epsilon` guards against floating-point noise: an "unlevered"
    scenario's margin_debt should be exactly 0.0, but repeated share
    buy/sell arithmetic over a long simulation can leave a residue on
    the order of 1e-12, which makes leverage_ratio (gross/net_equity)
    computed as, e.g., 1.0000000000000002 instead of exactly 1.0 —
    comfortably real but comfortably not a genuine breach. A real
    breach (this account's own leverage passively drifting above its
    cap because gross fell during a stress episode) is orders of
    magnitude larger than this tolerance; discovered and fixed during
    Phase 4A's own first execution run, which produced 214 false
    "events" for a nominally unlevered control before this epsilon was
    added — see test_forced_deleveraging_events_ignores_floating_
    point_noise in test_phase4a_lib.py."""
    return [i for i, lv in enumerate(leverage_series)
           if lv is not None and lv > leverage_cap + epsilon]


def classify_event_repetition(counts_by_case: dict[str, int]) -> bool:
    """docs/PHASE4A_MATERIALITY_THRESHOLDS.md §5: "repeated" = >=3 events
    within a single stress case, OR events (>=1) occurring in >=2 of the
    stress cases. Returns True only if one of those two conditions
    holds — a single isolated event in a single case returns False,
    exactly matching that document's "a single event does not count"
    resolution."""
    if any(n >= 3 for n in counts_by_case.values()):
        return True
    cases_with_events = sum(1 for n in counts_by_case.values() if n > 0)
    return cases_with_events >= 2


# ── recovery time ────────────────────────────────────────────────────────────

@dataclass
class RecoveryInfo:
    peak_index: int | None
    trough_index: int | None
    peak_value: float | None
    trough_value: float | None
    recovery_index: int | None   # None if never recovered within the series
    recovery_days: int | None    # trough_index -> recovery_index, None if never


def worst_drawdown_recovery(values: list[float]) -> RecoveryInfo:
    """Finds the SINGLE worst peak-to-trough episode in `values` (the
    same one max_drawdown() from backtest_regime.py already identifies
    by magnitude, but this function also locates WHERE it happened and
    whether/when the series recovered to a new high after it — a
    measurement max_drawdown() itself does not provide and no existing
    function in this repo computes)."""
    if not values:
        return RecoveryInfo(None, None, None, None, None, None)

    peak_idx = 0
    peak_val = values[0]
    worst_dd = 0.0
    worst_peak_idx = 0
    worst_trough_idx = 0
    worst_peak_val = values[0]
    worst_trough_val = values[0]

    for i, v in enumerate(values):
        if v > peak_val:
            peak_val = v
            peak_idx = i
        if peak_val > 0:
            dd = v / peak_val - 1.0
            if dd < worst_dd:
                worst_dd = dd
                worst_peak_idx = peak_idx
                worst_trough_idx = i
                worst_peak_val = peak_val
                worst_trough_val = v

    if worst_dd == 0.0:
        # series never declined from its running peak at all
        return RecoveryInfo(peak_idx, None, peak_val, None, None, None)

    recovery_idx = None
    for j in range(worst_trough_idx + 1, len(values)):
        if values[j] >= worst_peak_val:
            recovery_idx = j
            break

    recovery_days = (recovery_idx - worst_trough_idx) if recovery_idx is not None else None
    return RecoveryInfo(worst_peak_idx, worst_trough_idx, worst_peak_val,
                        worst_trough_val, recovery_idx, recovery_days)


def is_recovery_material(stressed_days: int | None, baseline_days: int | None,
                         relative_threshold: float = 1.5,
                         absolute_min_days: int = 20) -> bool:
    """docs/PHASE4A_MATERIALITY_THRESHOLDS.md §7: recovery time is
    material only if it exceeds the baseline's own recovery time by
    >=1.5x, OR by an absolute minimum of 20 trading days when the
    baseline has no comparable recovery episode to measure against
    (baseline_days is None) and the stressed scenario does. If the
    stressed scenario also never recovered (stressed_days is None),
    that is reported separately (an unrecovered episode) — this
    function returns False for that case, since "never recovered" is a
    qualitatively different, arguably more severe finding than a slow
    but completed recovery, and should not be silently folded into a
    simple True/False materiality flag."""
    if stressed_days is None:
        return False
    if baseline_days is None or baseline_days == 0:
        return stressed_days >= absolute_min_days
    return stressed_days >= baseline_days * relative_threshold


# ── materiality classification (MaxDD / TWR gaps) ───────────────────────────

def classify_gap(gap_pp: float, material_threshold: float = 2.0,
                 noise_floor: float = 0.5) -> str:
    """docs/PHASE4A_MATERIALITY_THRESHOLDS.md §2/§3: classifies a
    percentage-point gap (MaxDD or TWR) into one of three bands. Uses
    absolute value of the gap — materiality is about magnitude, not
    direction; direction is reported separately wherever this is
    called, not folded into this classification."""
    mag = abs(gap_pp)
    if mag >= material_threshold:
        return "material"
    if mag <= noise_floor:
        return "noise"
    return "suggestive"
