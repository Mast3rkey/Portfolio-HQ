"""
margin_state.py — pure margin risk classification. Phase 2B of the Margin
Intelligence Engine (see docs/MARGIN_DOCTRINE.md, docs/PHASE2_IMPLEMENTATION_PLAN.md).

This module is a risk-governance calculator, not a decision-maker. It answers
"how much risk is this account carrying right now" from numbers the caller
supplies — it never fetches data, never places or recommends an order, never
reads a price/regime/volatility signal, and structurally cannot recommend
increasing leverage: ALLOWED_ACTIONS contains no such action, by construction.

Four states, all risk classifications (see docs/MARGIN_DOCTRINE.md's Margin
Intelligence Engine Doctrine section for the full ✅/❌ boundary this module
is built to hold):
    NORMAL          — leverage and buffer comfortably clear of every threshold.
    CAUTION         — approaching a threshold; informational only.
    RESTRICTED      — past the inner threshold; new margin draws should be
                      reduced (the specific mechanism is not decided by this
                      module — see the repayment waterfall design).
    FORCED_DELEVER  — buffer below the floor, or leverage above the cap
                      (the account's own state has breached a hard,
                      pre-existing structural rule). Existing behavior in
                      allocate.py's margin_capacity() already blocks margin
                      buys here; this module adds the descriptive layer.

Every threshold this module can escalate on (caution/restricted leverage
fractions, buffer comfort multipliers, concentration tightening) is an
explicit parameter with no built-in default beyond None/0 — if a caller
passes None for a threshold, that escalation path simply never fires. This
mirrors targets.yaml's proposed margin: schema (docs/PHASE2_IMPLEMENTATION_PLAN.md
§3), where every such threshold is still null pending backtest evidence:
this module does not invent a number the project's own discipline says
shouldn't exist yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ── the closed action vocabulary ─────────────────────────────────────────────
# This set is the structural enforcement of "no state may recommend increasing
# leverage" (docs/PHASE2_IMPLEMENTATION_PLAN.md §4): every action this module
# can ever return is a member of this set, and the set contains no action that
# increases margin usage, recommends borrowing, or suggests a buy. There is no
# code path anywhere in this module that returns a string outside this set.
CONTINUE_NORMAL_OPERATIONS = "continue_normal_operations"
REDUCE_RISK = "reduce_risk"
PRIORITIZE_DELEVERAGING = "prioritize_deleveraging"
VERIFY_MARGIN_DATA = "verify_margin_data"

ALLOWED_ACTIONS = frozenset({
    CONTINUE_NORMAL_OPERATIONS,
    REDUCE_RISK,
    PRIORITIZE_DELEVERAGING,
    VERIFY_MARGIN_DATA,
})

STATES = ("NORMAL", "CAUTION", "RESTRICTED", "FORCED_DELEVER")


@dataclass
class MarginStateResult:
    """The output contract. Every field is plain data — no method on this
    class computes anything or triggers any action; it is a report, not an
    agent."""
    current_state: str
    reasons: list[str] = field(default_factory=list)
    violated_constraints: list[str] = field(default_factory=list)
    risk_metrics: dict[str, float | None] = field(default_factory=dict)
    allowed_actions: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.current_state not in STATES:
            raise ValueError(f"current_state must be one of {STATES}, got {self.current_state!r}")
        bad = set(self.allowed_actions) - ALLOWED_ACTIONS
        if bad:
            raise ValueError(f"allowed_actions contains disallowed action(s): {bad} "
                              f"— only {ALLOWED_ACTIONS} may ever appear")


# ── concentration: portfolio-level pressure only, never per-ticker leverage ──

def concentration_risk_score(proximities: dict[str, float]) -> tuple[float, str | None]:
    """Portfolio-level concentration pressure: how close is the TIGHTEST
    currently-active risk cap (a cluster cap or the T1/T2 ceiling) to
    breaching. Takes the max, not an average, because portfolio risk is
    dominated by its worst concentration, not its typical one.

    `proximities` is {label: value/cap_ratio} for every cluster and T1/T2
    name the CALLER has already computed (e.g. "cluster:semis" -> 0.93,
    "t1t2:NVDA" -> 1.05) — this function does no I/O and does not compute
    cluster values itself; it only aggregates numbers already produced by
    allocate.py's existing cluster-cap/T1T2-ceiling logic for an unrelated
    purpose (deciding what to trim).

    This answers "how much does concentration reduce margin safety" (one
    portfolio-level number) — it does NOT answer "how much leverage does
    NVDA have" (margin debt is an account-wide liability with no real
    per-position allocation; the returned label identifies which existing
    CAP is under the most pressure, for explainability, not a leverage
    figure assigned to that name).

    Returns (score, source_label). Empty input -> (0.0, None), not an error.
    """
    if not proximities:
        return 0.0, None
    label = max(proximities, key=proximities.get)
    return float(proximities[label]), label


# ── the classifier ────────────────────────────────────────────────────────────

def classify_margin_state(
    *,
    gross: float,
    margin_debt: float,
    buffer_pct: float | None,
    leverage_cap: float,
    buffer_floor_pct: float,
    concentration_score: float = 0.0,
    concentration_source: str | None = None,
    caution_leverage_fraction: float | None = None,
    caution_buffer_comfort_multiplier: float | None = None,
    restricted_leverage_fraction: float | None = None,
    restricted_buffer_comfort_multiplier: float | None = None,
    concentration_tightening_coefficient: float = 0.0,
    concentration_min_fraction: float = 0.5,
    buffer_data_age_days: float | None = None,
    stale_threshold_days: float = 2.0,
) -> MarginStateResult:
    """Classify current margin risk. Pure function: every input is a number
    or None: no fetch, no clock read beyond what the caller supplies via
    buffer_data_age_days, no market data of any kind.

    Inputs map directly to docs/PHASE2_IMPLEMENTATION_PLAN.md §2's required
    list: gross portfolio value, margin debt, Robinhood buffer %, leverage
    cap, buffer floor, concentration score (optional), and configuration
    values for the CAUTION/RESTRICTED thresholds (all optional — None means
    "not yet configured, this escalation path does not fire," never a
    guessed default; see targets.yaml's proposed margin: schema, every one
    of these is still null pending backtest evidence).

    Net equity and leverage ratio are DERIVED here (net_equity = gross -
    margin_debt; leverage = gross / net_equity) rather than accepted as
    separate inputs, so a caller can never pass an internally-inconsistent
    pair (e.g. a net_equity that doesn't match gross - debt).
    """
    # ---- input validation: fail fast on malformed data, not on extreme-but-
    # real account states (see the net_equity <= 0 handling below, which is
    # NOT a validation error -- it's a real, if catastrophic, account state
    # this classifier must be able to describe rather than crash on). ------
    if gross < 0:
        raise ValueError(f"gross must be >= 0, got {gross}")
    if margin_debt < 0:
        raise ValueError(f"margin_debt must be >= 0, got {margin_debt}")
    if leverage_cap < 1.0:
        raise ValueError(f"leverage_cap must be >= 1.0, got {leverage_cap}")
    if not (0.0 <= buffer_floor_pct <= 100.0):
        raise ValueError(f"buffer_floor_pct must be in [0, 100], got {buffer_floor_pct}")
    if buffer_pct is not None and not (0.0 <= buffer_pct <= 100.0):
        raise ValueError(f"buffer_pct must be in [0, 100] or None, got {buffer_pct}")
    if concentration_score < 0.0:
        raise ValueError(f"concentration_score must be >= 0, got {concentration_score}")
    if not (0.0 <= concentration_min_fraction <= 1.0):
        raise ValueError(f"concentration_min_fraction must be in [0, 1], got {concentration_min_fraction}")
    if buffer_data_age_days is not None and buffer_data_age_days < 0:
        raise ValueError(f"buffer_data_age_days must be >= 0 or None, got {buffer_data_age_days}")

    reasons: list[str] = []
    violated: list[str] = []
    metrics: dict[str, float | None] = {}

    net_equity = gross - margin_debt
    metrics["net_equity"] = net_equity

    # ---- insolvency: a real, extreme account state, not a data error -------
    if net_equity <= 0:
        reasons.append(f"net equity is non-positive (${net_equity:,.2f}) — "
                        "gross holdings no longer cover margin debt")
        violated.append("net_equity_non_positive")
        metrics["leverage_ratio"] = None
        metrics["utilization"] = None
        return MarginStateResult(
            current_state="FORCED_DELEVER",
            reasons=reasons,
            violated_constraints=violated,
            risk_metrics=metrics,
            allowed_actions=[PRIORITIZE_DELEVERAGING],
        )

    leverage_ratio = gross / net_equity
    metrics["leverage_ratio"] = leverage_ratio

    # utilization = how much of the leverage-cap ceiling is actually drawn.
    # Guarded: leverage_cap == 1.0 means "no leverage allowed at all," so the
    # denominator (net_equity * (cap - 1)) is zero -- undefined, not an error.
    if leverage_cap > 1.0:
        max_allowed_debt = net_equity * (leverage_cap - 1.0)
        metrics["utilization"] = (margin_debt / max_allowed_debt) if max_allowed_debt > 0 else None
    else:
        metrics["utilization"] = 0.0 if margin_debt == 0 else None
        if margin_debt > 0:
            reasons.append("leverage_cap is 1.0 (no leverage permitted) but margin_debt > 0 — "
                            "utilization is undefined")

    metrics["concentration_score"] = concentration_score
    if concentration_source:
        reasons.append(f"tightest concentration pressure: {concentration_source} "
                        f"at {concentration_score:.2f}")

    # ---- staleness / missing data: informational, never forces a state ----
    stale = False
    verify_data = False
    if buffer_pct is None:
        reasons.append("buffer_pct unavailable (never synced) — buffer-based "
                        "checks skipped, classification uses leverage only")
        verify_data = True
    elif buffer_data_age_days is not None and buffer_data_age_days > stale_threshold_days:
        stale = True
        verify_data = True
        reasons.append(f"margin data is {buffer_data_age_days:.1f} day(s) old "
                        f"(stale threshold {stale_threshold_days:.1f}) — "
                        "buffer-based classification is unverified")
        violated.append("stale_margin_data")

    # ---- hard breaches: same severity as each other, both force FORCED_DELEVER,
    # per doctrine's "1.8x cap / 30% floor" both being fixed, no-exception rules ----
    buffer_breach = buffer_pct is not None and buffer_pct < buffer_floor_pct
    leverage_breach = leverage_ratio > leverage_cap

    if buffer_breach:
        violated.append("buffer_floor_breach")
        reasons.append(f"buffer {buffer_pct:.1f}% < {buffer_floor_pct:.1f}% floor")
    if leverage_breach:
        violated.append("leverage_cap_exceeded")
        reasons.append(f"leverage {leverage_ratio:.3f}x > {leverage_cap:.3f}x cap")

    if buffer_breach or leverage_breach:
        actions = [PRIORITIZE_DELEVERAGING]
        if verify_data:
            actions.append(VERIFY_MARGIN_DATA)
        return MarginStateResult(
            current_state="FORCED_DELEVER",
            reasons=reasons,
            violated_constraints=violated,
            risk_metrics=metrics,
            allowed_actions=actions,
        )

    # ---- concentration tightening: only ever makes a threshold TIGHTER,
    # never looser -- concentration_score >= 0 by validation above, so the
    # multiplier below is always <= 1.0. -------------------------------------
    def _tighten(fraction: float | None) -> float | None:
        if fraction is None:
            return None
        multiplier = max(concentration_min_fraction,
                          1.0 - concentration_tightening_coefficient * concentration_score)
        return fraction * multiplier

    caution_lev = _tighten(caution_leverage_fraction)
    restricted_lev = _tighten(restricted_leverage_fraction)

    restricted_lev_hit = (restricted_lev is not None and leverage_ratio > restricted_lev * leverage_cap)
    restricted_buf_hit = (
        buffer_pct is not None and restricted_buffer_comfort_multiplier is not None
        and buffer_pct < buffer_floor_pct * restricted_buffer_comfort_multiplier
    )
    caution_lev_hit = (caution_lev is not None and leverage_ratio > caution_lev * leverage_cap)
    caution_buf_hit = (
        buffer_pct is not None and caution_buffer_comfort_multiplier is not None
        and buffer_pct < buffer_floor_pct * caution_buffer_comfort_multiplier
    )

    if restricted_lev_hit or restricted_buf_hit:
        if restricted_lev_hit:
            reasons.append(f"leverage {leverage_ratio:.3f}x above the RESTRICTED threshold")
        if restricted_buf_hit:
            reasons.append(f"buffer {buffer_pct:.1f}% below the RESTRICTED comfort band")
        actions = [REDUCE_RISK, PRIORITIZE_DELEVERAGING]
        if verify_data:
            actions.append(VERIFY_MARGIN_DATA)
        return MarginStateResult(
            current_state="RESTRICTED",
            reasons=reasons,
            violated_constraints=violated,
            risk_metrics=metrics,
            allowed_actions=actions,
        )

    if caution_lev_hit or caution_buf_hit:
        if caution_lev_hit:
            reasons.append(f"leverage {leverage_ratio:.3f}x above the CAUTION threshold")
        if caution_buf_hit:
            reasons.append(f"buffer {buffer_pct:.1f}% below the CAUTION comfort band")
        actions = [CONTINUE_NORMAL_OPERATIONS, REDUCE_RISK]
        if verify_data:
            actions.append(VERIFY_MARGIN_DATA)
        return MarginStateResult(
            current_state="CAUTION",
            reasons=reasons,
            violated_constraints=violated,
            risk_metrics=metrics,
            allowed_actions=actions,
        )

    reasons.append("leverage and buffer within normal range")
    actions = [CONTINUE_NORMAL_OPERATIONS]
    if verify_data:
        actions.append(VERIFY_MARGIN_DATA)
    return MarginStateResult(
        current_state="NORMAL",
        reasons=reasons,
        violated_constraints=violated,
        risk_metrics=metrics,
        allowed_actions=actions,
    )
