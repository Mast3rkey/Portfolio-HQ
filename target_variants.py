"""
target_variants.py — MARGIN-0005 research-only Study B target-sizing
variant library (S2, third and final authorized S2 PR under the charter's
<=3 ceiling; scope per `research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md`
§5, item 4 — "permitted but not strictly required for G2," needed instead
for Study B to ever execute at S3).

Authorized by `governance/decisions/MARGIN-0005-margin-target-research-charter.md`
(charter §4, "Research package" row) and `PROTOCOL_V2.md` §5 (Study B arms
B-0 through B-6) / §13.

## Scope

Pure, deterministic functions building the Study B target-sizing variant
configurations (`pre_registration.yaml` `studies.study_b.arms`), each
operating on a CALLER-SUPPLIED roster (this module reads no YAML, no
`targets.yaml`, no live holdings — a future `run_study_b.py`, S3 scope,
supplies the real roster derived from `targets.yaml`, keeping this module's
isolation as clean as `repayment_lib.py`'s own zero-file-I/O design).

## T-6 — the TGT-0001 ex-ante cluster-compatibility check

`assert_ex_ante_cluster_compatible()` below is the programmatic form of the
rule `governance/decisions/TGT-0001-additive-target-budget-policy.md`
already states in prose: "a proposal that would place a configured cluster
target total above that cluster's existing cap... is not approvable as
written." Every Study B variant builder in this module calls it before
returning, and **B-3 is constructed so its output always passes** ("every
config passes TGT-0001's ex-ante rule by construction," per
`pre_registration.yaml` B3_cluster_constrained) — the other builders (B-1,
B-2, B-4, B-5, B-6) are still CHECKED against the rule on every call (T-6:
"programmatic... check on every config"), but are not guaranteed to pass
it; their `cluster_check` result is returned alongside the weights so a
future S3 runner can exclude an over-cap variant rather than this module
silently rejecting or silently permitting one.

## Crypto (B-2)

`pre_registration.yaml` `B2_sleeves.crypto` is `conditional_on:
crypto_outcome_a`. `data_acquisition.py`'s own G1 `validate()` already
recorded the actual outcome: **"(b) CRYPTO TARGET SIZING OUT OF SCOPE"**
(SOL's 416-day coverage hole) — the crypto-sleeve configurations
accordingly lapse and are NOT built here; `build_b2_etf_sleeve_budget()`
covers only the ETF-sleeve half of B-2, which carries no such condition.

## No per-ticker optimization, no scoring

Every function here operates on an explicit, caller-supplied roster and a
declared, named transformation (a tier multiplier, a sleeve rescale, a
cluster-cap-relative shrink, a flat nominal scale) — never a per-ticker
optimization, conviction score, or Intelligence-derived weight
(`pre_registration.yaml` `study_b.exclusions`). `REPAYMENT`-style scoring/
ranking/pooling functions do not exist anywhere in this module (same
absence `repayment_lib.py`'s own `test_no_scoring_ranking_or_pooling_
function_exists` enforces there).

Zero import relationship with `allocate.py`/`margin_state.py` in either
direction. No file or network I/O anywhere in this module. Never calls
`margin_simulation.simulate()`; never touches `trial_ledger.jsonl` or
`candidate_freeze.yaml`; consumes zero of the 300-run trial ceiling.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TieredWeight:
    """One roster entry: a ticker, its tier label, and its target weight
    (percent of book). The caller builds the initial list from
    `targets.yaml` (or a synthetic test fixture) — this module never reads
    it directly."""
    ticker: str
    tier: str
    weight_pct: float


@dataclass(frozen=True)
class ClusterDef:
    """One correlated-cluster cap definition (`targets.yaml`
    `caps.clusters[]`), caller-supplied."""
    name: str
    pct: float
    tickers: tuple[str, ...]


# ═════════════════════════════════════════════════════════════════════════
# T-6 — programmatic TGT-0001 ex-ante cluster-compatibility check
# ═════════════════════════════════════════════════════════════════════════

def cluster_totals(weights: dict[str, float], clusters: list[ClusterDef]) -> dict[str, float]:
    """Configured target-weight TOTAL for each cluster under `weights` —
    the sum of every member ticker's configured weight that's present in
    `weights` (a ticker not in `weights` at all contributes 0, not an
    error — a variant may legitimately omit a ticker)."""
    return {c.name: sum(weights.get(t, 0.0) for t in c.tickers) for c in clusters}


def check_cluster_compatibility(weights: dict[str, float],
                                clusters: list[ClusterDef]) -> dict[str, dict]:
    """Per-cluster `{"total_pct", "cap_pct", "compliant"}` report — the
    read-only form of the TGT-0001 ex-ante check."""
    totals = cluster_totals(weights, clusters)
    return {c.name: {"total_pct": totals[c.name], "cap_pct": c.pct,
                     "compliant": totals[c.name] <= c.pct + 1e-9}
           for c in clusters}


def assert_ex_ante_cluster_compatible(weights: dict[str, float],
                                      clusters: list[ClusterDef]) -> dict[str, dict]:
    """Raises `ValueError` naming every cluster whose configured target-
    weight total under `weights` would exceed its cap — the programmatic
    form of TGT-0001's "not approvable as written" rule. Returns the full
    compatibility report on success (every builder below can pass this
    report straight through as its own `cluster_check` output)."""
    report = check_cluster_compatibility(weights, clusters)
    bad = {name: r for name, r in report.items() if not r["compliant"]}
    if bad:
        raise ValueError(f"cluster cap(s) exceeded by construction: {bad}")
    return report


def _weights_of(roster: list[TieredWeight]) -> dict[str, float]:
    return {r.ticker: r.weight_pct for r in roster}


# ═════════════════════════════════════════════════════════════════════════
# Study B variant builders
# ═════════════════════════════════════════════════════════════════════════

def build_b0_baseline(roster: list[TieredWeight],
                      clusters: list[ClusterDef]) -> dict:
    """B-0 — current baseline: the roster's own configured weights,
    unmodified. Still checked (not asserted) against the ex-ante rule,
    since a real current-book baseline is expected to already comply, and
    this is exactly the kind of "check on every config" T-6 requires."""
    weights = _weights_of(roster)
    return {"variant_id": "B0_baseline", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b1_tier_multiplier(roster: list[TieredWeight], *, tiers: tuple[str, ...],
                             multiplier: float, clusters: list[ClusterDef]) -> dict:
    """B-1 — tier multipliers: every roster entry whose `tier` is in
    `tiers` (`pre_registration.yaml` B1_tier_multipliers: `tiers: [T1, T2,
    band]`, `multipliers: [0.8, 1.2]`) has its weight scaled by
    `multiplier`; every other entry's weight is unchanged (no per-ticker
    mutation outside the declared transformation)."""
    if multiplier <= 0:
        raise ValueError(f"multiplier must be > 0, got {multiplier}")
    weights = {r.ticker: (r.weight_pct * multiplier if r.tier in tiers else r.weight_pct)
              for r in roster}
    return {"variant_id": f"B1_tier_multiplier_{multiplier}", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b2_etf_sleeve_budget(roster: list[TieredWeight], *, etf_tickers: tuple[str, ...],
                               new_sleeve_pct: float, clusters: list[ClusterDef]) -> dict:
    """B-2 (ETF half only — see module docstring on crypto's G1 outcome
    (b) exclusion): rescales the ETF-sleeve tickers so their weights sum to
    exactly `new_sleeve_pct` (`pre_registration.yaml` B2_sleeves.etf:
    `[0.10, 0.13]`), preserving their RELATIVE proportions to each other;
    every non-ETF ticker's weight is unchanged."""
    if new_sleeve_pct <= 0:
        raise ValueError(f"new_sleeve_pct must be > 0, got {new_sleeve_pct}")
    base = _weights_of(roster)
    current_total = sum(base.get(t, 0.0) for t in etf_tickers)
    if current_total <= 0:
        raise ValueError("ETF sleeve has zero current configured weight — cannot rescale proportionally")
    scale = new_sleeve_pct / current_total
    weights = {t: (w * scale if t in etf_tickers else w) for t, w in base.items()}
    return {"variant_id": f"B2_etf_sleeve_{new_sleeve_pct}", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b3_cluster_constrained(roster: list[TieredWeight], *, clusters: list[ClusterDef],
                                 fraction_of_cap: float) -> dict:
    """B-3 — cluster-constrained reallocation (`pre_registration.yaml`
    B3_cluster_constrained: `configured_cluster_totals_as_fraction_of_caps:
    [0.75, 0.50]`, `tgt0001_exante_rule: enforced_by_construction`). For
    every cluster whose current configured total exceeds
    `fraction_of_cap * cap`, every member ticker's weight is scaled down
    proportionally so the cluster's total lands exactly at that target
    (never scaled UP — a cluster already under the target fraction is left
    unchanged). Because the post-condition is `total <= fraction_of_cap *
    cap <= cap` for every cluster by construction, this is the one builder
    whose output is ASSERTED (not merely checked) against the ex-ante
    rule — a violation here would indicate a bug in this function itself,
    not a legitimately over-cap research variant."""
    if not (0.0 < fraction_of_cap <= 1.0):
        raise ValueError(f"fraction_of_cap must be in (0, 1], got {fraction_of_cap}")
    weights = _weights_of(roster)
    for c in clusters:
        total = sum(weights.get(t, 0.0) for t in c.tickers)
        target_total = fraction_of_cap * c.pct
        if total > target_total and total > 0:
            scale = target_total / total
            for t in c.tickers:
                if t in weights:
                    weights[t] *= scale
    report = assert_ex_ante_cluster_compatible(weights, clusters)
    return {"variant_id": f"B3_cluster_constrained_{fraction_of_cap}", "weights": weights,
           "cluster_check": report}


def build_b4_t1_flatten(roster: list[TieredWeight], *, ceiling_pct: float,
                        clusters: list[ClusterDef]) -> dict:
    """B-4a — "T1-flatten to `ceiling_pct` redistributed pro-rata"
    (`pre_registration.yaml` B4_concentration_reductions:
    `t1_flatten_to_2.50_redistribute_pro_rata`). Every T1 entry above
    `ceiling_pct` is capped at it; the total excess removed is added back,
    distributed proportionally to every NON-T1 entry's existing weight
    (the total nominal sum is conserved)."""
    if ceiling_pct <= 0:
        raise ValueError(f"ceiling_pct must be > 0, got {ceiling_pct}")
    weights = _weights_of(roster)
    excess = 0.0
    for r in roster:
        if r.tier == "T1" and weights[r.ticker] > ceiling_pct:
            excess += weights[r.ticker] - ceiling_pct
            weights[r.ticker] = ceiling_pct
    non_t1_total = sum(w for r, w in ((r, weights[r.ticker]) for r in roster) if r.tier != "T1")
    if excess > 0 and non_t1_total > 0:
        for r in roster:
            if r.tier != "T1":
                weights[r.ticker] += excess * (weights[r.ticker] / non_t1_total)
    return {"variant_id": f"B4_t1_flatten_{ceiling_pct}", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b4_semis_reduction(roster: list[TieredWeight], *, semis_cluster: ClusterDef,
                             etf_tickers: tuple[str, ...], factor: float,
                             clusters: list[ClusterDef]) -> dict:
    """B-4b — "semis x0.75, ETF absorbs" (`pre_registration.yaml`
    B4_concentration_reductions: `semis_x0.75_etf_absorbs`). Every semis-
    cluster member's weight is scaled by `factor` (e.g. 0.75); the total
    dollars removed are added to the ETF-sleeve tickers, split evenly
    across them."""
    if not (0.0 < factor < 1.0):
        raise ValueError(f"factor must be in (0, 1), got {factor}")
    if not etf_tickers:
        raise ValueError("etf_tickers must be non-empty for the ETF-absorbs step")
    weights = _weights_of(roster)
    removed = 0.0
    for t in semis_cluster.tickers:
        if t in weights:
            reduction = weights[t] * (1.0 - factor)
            removed += reduction
            weights[t] -= reduction
    if removed > 0:
        share = removed / len(etf_tickers)
        for t in etf_tickers:
            weights[t] = weights.get(t, 0.0) + share
    return {"variant_id": f"B4_semis_x{factor}_etf_absorbs", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b5_nominal_budget(roster: list[TieredWeight], *, factor: float,
                            clusters: list[ClusterDef]) -> dict:
    """B-5 — nominal budgets (`pre_registration.yaml` B5_nominal_budgets:
    `[1.10, 1.20]`): every ticker's weight scaled uniformly by `factor`,
    preserving all relative proportions exactly."""
    if factor <= 0:
        raise ValueError(f"factor must be > 0, got {factor}")
    weights = {r.ticker: r.weight_pct * factor for r in roster}
    return {"variant_id": f"B5_nominal_{factor}", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b6_inverse_vol(roster: list[TieredWeight], *, volatility: dict[str, float],
                         clusters: list[ClusterDef]) -> dict:
    """B-6 — inverse-volatility comparator (`pre_registration.yaml`
    B6_comparators_non_adoptable: `inverse_vol`; PRE-DECLARED
    NON-ADOPTABLE under current doctrine — a research comparator only).
    `volatility` is a caller-supplied `{ticker: annualized realized vol}`
    map (computed elsewhere, e.g. by `overlay_lib.realized_vol_series` on
    real price history — this module does no price-data I/O itself).
    Weight_i is proportional to `1/vol_i`, rescaled so the total nominal
    sum equals the roster's own current total (conserved, not re-targeted)."""
    base = _weights_of(roster)
    total_nominal = sum(base.values())
    missing = [t for t in base if t not in volatility]
    if missing:
        raise ValueError(f"volatility missing for ticker(s): {sorted(missing)}")
    if any(v <= 0 for v in volatility.values()):
        raise ValueError("every volatility value must be > 0")
    inv = {t: 1.0 / volatility[t] for t in base}
    inv_total = sum(inv.values())
    weights = {t: inv[t] / inv_total * total_nominal for t in base}
    return {"variant_id": "B6_inverse_vol", "weights": weights,
           "cluster_check": check_cluster_compatibility(weights, clusters)}


def build_b6_equal_risk_contribution_uncorrelated(roster: list[TieredWeight], *,
                                                  volatility: dict[str, float],
                                                  clusters: list[ClusterDef]) -> dict:
    """B-6 — equal-risk-contribution comparator, ZERO-CORRELATION
    simplification (`pre_registration.yaml` B6_comparators_non_adoptable:
    `equal_risk_contribution`; PRE-DECLARED NON-ADOPTABLE). A true
    covariance-based ERC solve requires the full pairwise correlation
    matrix and an iterative numerical solver — data and machinery this
    module does not have and, for a pre-declared non-adoptable comparator,
    is not worth introducing the risk of an unreviewed numerical optimizer
    for. Under the explicit simplifying assumption of ZERO pairwise
    correlation (a diagonal covariance matrix), equal-risk-contribution
    reduces to a well-known closed form that IS exactly inverse-volatility
    weighting — so this function is mathematically identical to
    `build_b6_inverse_vol()` above, kept as its own named, separately
    tested entry point because it is a conceptually distinct comparator
    (and a different pre-registered arm) whose simplifying assumption is
    disclosed here, not silently reused from the other function."""
    result = build_b6_inverse_vol(roster, volatility=volatility, clusters=clusters)
    return {**result, "variant_id": "B6_equal_risk_contribution_uncorrelated"}
