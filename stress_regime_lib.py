"""
stress_regime_lib.py — Stress-regime execution assumptions analysis,
execution-layer helpers only.

Per docs/STRESS_REGIME_EXECUTION_ASSUMPTIONS_PLAN.md. Does NOT modify
margin_simulation.py, allocate.py, targets.yaml, holdings.yaml, or
margin_state.py. No engine change was needed or made: every function
here operates either on the raw cached OHLCV bars in data/backtest/
*.json (never previously read beyond their 'c' close field by any
Phase 3/4 script) or on an already-completed SimulationResult's
existing output (events, book_values, leverage_series).

Implements NO liquidity model, NO execution-failure model, and NO
invented historical event. Stress-window detection uses ONLY real,
already-cached high/low/volume data as a volatility/liquidity PROXY —
never presented as measured bid-ask spread or market depth (see
detect_stress_days()'s docstring). The hypothetical-secondary friction
overlay (regime_conditional_cost()) is a disclosed, bounded multiplier
applied only to already-known repayment events falling inside
real, historically-detected stress windows — it does not construct or
assume any price movement that didn't actually occur.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "data" / "backtest"


# ── OHLCV loading (external to the simulation engine) ───────────────────────

def load_aligned_ohlcv(ticker: str, calendar: list[str]) -> dict[str, list[float]]:
    """Reads `ticker`'s real cached daily bars (data/backtest/{ticker}.json)
    and aligns high/low/close/volume to `calendar` (the same simulation-day
    calendar load_real_aligned_data() already produces), forward-filling
    any date not present in the raw bars from the last known value — the
    same forward-fill convention backtest_regime.py's setup() already uses
    for its own regime-ticker alignment. Returns {'h': [...], 'l': [...],
    'c': [...], 'v': [...]}, one list per field, each len(calendar) long.

    Reads ONLY 'h' (high), 'l' (low), 'c' (close), and 'v' (volume) —
    real, already-cached fields on every bar, confirmed present by direct
    inspection before this module was written. No field is invented or
    estimated; a date with no bar at all is forward-filled from the prior
    real value, never fabricated."""
    bars = json.loads((CACHE / f"{ticker}.json").read_text())
    by_date = {b["t"][:10]: b for b in bars}
    out = {"h": [], "l": [], "c": [], "v": []}
    last = None
    for dt in calendar:
        bar = by_date.get(dt, last)
        last = bar
        for field in out:
            out[field].append(float(bar[field]) if bar is not None else None)
    return out


# ── stress-day / stress-window detection ────────────────────────────────────

def detect_stress_days(highs: list[float], lows: list[float], closes: list[float],
                       volumes: list[float], trailing_window: int = 60,
                       volatility_multiplier: float = 1.5,
                       liquidity_fraction: float = 0.7) -> list[bool]:
    """Flags each day as a stress-proxy day if EITHER:
      - intraday range (high-low)/close exceeds `volatility_multiplier`
        times its own trailing `trailing_window`-day average (a realized-
        volatility PROXY, not a measured volatility index), OR
      - volume falls below `liquidity_fraction` times its own trailing
        `trailing_window`-day average (a liquidity-pressure PROXY, not
        measured spread or market depth).

    Both proxies are computed entirely from real, already-cached OHLCV
    data (see load_aligned_ohlcv()) — this function detects when real
    historical conditions plausibly indicate stress, using real
    historical facts, never an invented or assumed event.

    The first `trailing_window` days always return False (insufficient
    trailing history to compute a baseline) -- not stress-flagged by
    default, not treated as an error."""
    n = len(closes)
    range_pct = [None] * n
    for i in range(n):
        if highs[i] is not None and lows[i] is not None and closes[i]:
            range_pct[i] = (highs[i] - lows[i]) / closes[i]

    flags = [False] * n
    for i in range(trailing_window, n):
        window_range = [r for r in range_pct[i - trailing_window:i] if r is not None]
        window_vol = [v for v in volumes[i - trailing_window:i] if v is not None]
        if not window_range or not window_vol or range_pct[i] is None or volumes[i] is None:
            continue
        avg_range = sum(window_range) / len(window_range)
        avg_vol = sum(window_vol) / len(window_vol)
        volatility_flag = avg_range > 0 and range_pct[i] > volatility_multiplier * avg_range
        liquidity_flag = avg_vol > 0 and volumes[i] < liquidity_fraction * avg_vol
        flags[i] = volatility_flag or liquidity_flag
    return flags


def stress_windows_from_days(stress_flags: list[bool], min_window_days: int = 3,
                             merge_gap_days: int = 5) -> list[tuple[int, int]]:
    """Converts a per-day stress flag series into contiguous windows
    (inclusive start_idx, end_idx pairs). Runs shorter than
    `min_window_days` are discarded (single-day noise, not a sustained
    stress period). Windows separated by a gap of `merge_gap_days` or
    fewer non-stress days are merged into one — a brief calm interruption
    inside an otherwise stressed stretch is treated as one episode, not
    several artificially split ones."""
    raw_runs = []
    start = None
    for i, flag in enumerate(stress_flags):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            raw_runs.append((start, i - 1))
            start = None
    if start is not None:
        raw_runs.append((start, len(stress_flags) - 1))

    runs = [(s, e) for s, e in raw_runs if (e - s + 1) >= min_window_days]
    if not runs:
        return []

    merged = [runs[0]]
    for s, e in runs[1:]:
        last_s, last_e = merged[-1]
        if s - last_e - 1 <= merge_gap_days:
            merged[-1] = (last_s, e)
        else:
            merged.append((s, e))
    return merged


def day_in_any_window(day_idx: int, windows: list[tuple[int, int]]) -> bool:
    return any(s <= day_idx <= e for s, e in windows)


def nearest_window_distance(day_idx: int, windows: list[tuple[int, int]]) -> int:
    """Distance in days from `day_idx` to the nearest stress window --
    0 if inside a window. Returns a large sentinel (10**9) if `windows`
    is empty, rather than raising or returning None -- a real possible
    input (no stress windows detected at all in this parameter setting),
    treated as "arbitrarily far," not an error."""
    if not windows:
        return 10**9
    best = 10**9
    for s, e in windows:
        if s <= day_idx <= e:
            return 0
        best = min(best, abs(day_idx - s), abs(day_idx - e))
    return best


# ── event classification against stress windows ─────────────────────────────

@dataclass
class EventStressSplit:
    in_window: list[dict]
    outside_window: list[dict]
    total_amount: float
    in_window_amount: float
    outside_window_amount: float

    @property
    def in_window_dollar_fraction(self) -> float:
        return (self.in_window_amount / self.total_amount) if self.total_amount > 0 else 0.0


def split_events_by_stress_window(events: list[dict], windows: list[tuple[int, int]],
                                  kind: str = "repayment") -> EventStressSplit:
    """Classifies every event of `kind` as inside or outside the given
    stress windows. This is the historical-primary analysis's core
    output: does repayment activity cluster inside real, detected stress
    periods, measured directly, not assumed."""
    matching = [e for e in events if e.get("kind") == kind]
    in_win = [e for e in matching if day_in_any_window(e["day"], windows)]
    out_win = [e for e in matching if not day_in_any_window(e["day"], windows)]
    total = sum(e["amount"] for e in matching)
    in_amt = sum(e["amount"] for e in in_win)
    out_amt = sum(e["amount"] for e in out_win)
    return EventStressSplit(in_win, out_win, total, in_amt, out_amt)


def base_rate_days_in_stress(windows: list[tuple[int, int]], n_days: int) -> float:
    """% of the whole simulated window's trading days that fall inside a
    detected stress window -- the "base rate" to compare
    in_window_dollar_fraction against (are repayment events over- or
    under-represented in stress periods relative to how much of the
    calendar stress periods occupy at all)."""
    if n_days <= 0:
        return 0.0
    covered = sum(min(e, n_days - 1) - s + 1 for s, e in windows if s < n_days)
    return covered / n_days * 100.0


# ── hypothetical-secondary: regime-conditional friction overlay ─────────────

def regime_conditional_cost(events: list[dict], windows: list[tuple[int, int]],
                            base_bps: float, stress_multiplier: float,
                            kind: str = "repayment") -> float:
    """Disclosed, bounded hypothetical-secondary overlay: applies
    `base_bps` to every matching event OUTSIDE a detected stress window,
    and `base_bps * stress_multiplier` to every matching event INSIDE
    one. Both the base rate and the multiplier are explicit, disclosed
    Hypothetical assumptions (the base rate reuses docs/TRANSACTION_
    COST_SENSITIVITY_PLAN.md's already-approved tiers; the multiplier is
    new to this analysis and must be labeled as such wherever reported).
    Does not model execution failure, does not assume any trade fails to
    fill -- only that its cost, if it fills, may be higher during
    detected stress."""
    if base_bps < 0 or stress_multiplier < 0:
        raise ValueError("base_bps and stress_multiplier must be >= 0")
    total = 0.0
    for e in events:
        if e.get("kind") != kind:
            continue
        rate = (base_bps * stress_multiplier if day_in_any_window(e["day"], windows)
               else base_bps) / 10_000.0
        total += e["amount"] * rate
    return total
