"""Tests for target_variants.py (MARGIN-0005 S2, third/final authorized S2
PR). All fixtures are a small, synthetic, hand-computable roster/cluster
set -- never the real 65-ticker roster or targets.yaml, never a registered
Study B configuration. Nothing here writes any file or touches
trial_ledger.jsonl/candidate_freeze.yaml.

Import-graph isolation (T-8) for target_variants.py is tested centrally in
test_validation_lib.py; this file focuses on target_variants.py's own
T-6 cluster-check and variant-builder behavior.
"""

import math

import pytest

from target_variants import (
    ClusterDef,
    TieredWeight,
    assert_ex_ante_cluster_compatible,
    build_b0_baseline,
    build_b1_tier_multiplier,
    build_b2_etf_sleeve_budget,
    build_b3_cluster_constrained,
    build_b4_semis_reduction,
    build_b4_t1_flatten,
    build_b5_nominal_budget,
    build_b6_equal_risk_contribution_uncorrelated,
    build_b6_inverse_vol,
    check_cluster_compatibility,
    cluster_totals,
)


def _roster():
    return [
        TieredWeight("A", "T1", 3.0),
        TieredWeight("B", "T1", 3.0),
        TieredWeight("C", "T2", 2.0),
        TieredWeight("D", "band", 1.0),
        TieredWeight("E", "ETF", 2.0),
        TieredWeight("F", "ETF", 2.0),
    ]


def _clusters():
    # Loose caps -- the baseline roster is compliant under these.
    return [ClusterDef("semis", 10.0, ("A", "C")), ClusterDef("power", 10.0, ("B", "D"))]


def _weights(roster=None):
    return {r.ticker: r.weight_pct for r in (roster or _roster())}


# ═════════════════════════════════════════════════════════════════════════
# T-6 — ex-ante cluster-compatibility check
# ═════════════════════════════════════════════════════════════════════════

def test_cluster_totals_hand_computed():
    totals = cluster_totals(_weights(), _clusters())
    assert totals == {"semis": 5.0, "power": 4.0}  # A(3)+C(2)=5; B(3)+D(1)=4


def test_cluster_totals_missing_ticker_contributes_zero():
    totals = cluster_totals({"A": 3.0}, _clusters())
    assert totals["semis"] == 3.0  # C absent from weights -> contributes 0


def test_check_cluster_compatibility_reports_compliance():
    report = check_cluster_compatibility(_weights(), _clusters())
    assert report["semis"] == {"total_pct": 5.0, "cap_pct": 10.0, "compliant": True}
    assert report["power"] == {"total_pct": 4.0, "cap_pct": 10.0, "compliant": True}


def test_assert_ex_ante_cluster_compatible_passes_when_compliant():
    report = assert_ex_ante_cluster_compatible(_weights(), _clusters())
    assert all(r["compliant"] for r in report.values())


def test_assert_ex_ante_cluster_compatible_raises_naming_the_breaching_cluster():
    tight = [ClusterDef("semis", 4.0, ("A", "C"))]  # total 5.0 > cap 4.0
    with pytest.raises(ValueError, match="semis"):
        assert_ex_ante_cluster_compatible(_weights(), tight)


def test_cluster_check_never_raises_by_itself():
    tight = [ClusterDef("semis", 4.0, ("A", "C"))]
    report = check_cluster_compatibility(_weights(), tight)  # never raises
    assert report["semis"]["compliant"] is False


# ═════════════════════════════════════════════════════════════════════════
# B-0 baseline
# ═════════════════════════════════════════════════════════════════════════

def test_b0_baseline_returns_unmodified_weights():
    result = build_b0_baseline(_roster(), _clusters())
    assert result["weights"] == _weights()
    assert result["variant_id"] == "B0_baseline"


# ═════════════════════════════════════════════════════════════════════════
# B-1 tier multipliers
# ═════════════════════════════════════════════════════════════════════════

def test_b1_tier_multiplier_only_scales_declared_tiers():
    result = build_b1_tier_multiplier(_roster(), tiers=("T1",), multiplier=1.2,
                                      clusters=_clusters())
    w = result["weights"]
    assert math.isclose(w["A"], 3.6) and math.isclose(w["B"], 3.6)
    # every non-T1 ticker's weight is exactly unchanged -- no mutation
    # outside the declared transformation.
    base = _weights()
    for t in ("C", "D", "E", "F"):
        assert w[t] == base[t]


def test_b1_tier_multiplier_rejects_nonpositive_multiplier():
    with pytest.raises(ValueError):
        build_b1_tier_multiplier(_roster(), tiers=("T1",), multiplier=0.0, clusters=_clusters())


# ═════════════════════════════════════════════════════════════════════════
# B-2 ETF sleeve budget (crypto half excluded -- G1 outcome (b), see module docstring)
# ═════════════════════════════════════════════════════════════════════════

def test_b2_etf_sleeve_rescales_proportionally():
    result = build_b2_etf_sleeve_budget(_roster(), etf_tickers=("E", "F"),
                                       new_sleeve_pct=3.0, clusters=_clusters())
    w = result["weights"]
    assert math.isclose(w["E"] + w["F"], 3.0)
    assert math.isclose(w["E"], w["F"])  # equal proportions preserved (both started at 2.0)
    base = _weights()
    for t in ("A", "B", "C", "D"):
        assert w[t] == base[t]


def test_b2_etf_sleeve_rejects_zero_current_weight():
    roster = [TieredWeight("E", "ETF", 0.0)]
    with pytest.raises(ValueError):
        build_b2_etf_sleeve_budget(roster, etf_tickers=("E",), new_sleeve_pct=1.0, clusters=[])


# ═════════════════════════════════════════════════════════════════════════
# B-3 cluster-constrained (enforced by construction)
# ═════════════════════════════════════════════════════════════════════════

def test_b3_cluster_constrained_shrinks_over_target_clusters_exactly():
    tight = [ClusterDef("semis", 4.0, ("A", "C")), ClusterDef("power", 5.0, ("B", "D"))]
    result = build_b3_cluster_constrained(_roster(), clusters=tight, fraction_of_cap=0.5)
    w = result["weights"]
    assert math.isclose(w["A"] + w["C"], 2.0)     # 0.5 * 4.0
    assert math.isclose(w["B"] + w["D"], 2.5)     # 0.5 * 5.0
    for name, r in result["cluster_check"].items():
        assert r["compliant"]


def test_b3_never_scales_up_an_already_under_target_cluster():
    loose = [ClusterDef("semis", 100.0, ("A", "C"))]  # 0.5*100=50, current total 5 well under
    result = build_b3_cluster_constrained(_roster(), clusters=loose, fraction_of_cap=0.5)
    assert result["weights"]["A"] == 3.0 and result["weights"]["C"] == 2.0  # unchanged


def test_b3_rejects_bad_fraction():
    with pytest.raises(ValueError):
        build_b3_cluster_constrained(_roster(), clusters=_clusters(), fraction_of_cap=0.0)
    with pytest.raises(ValueError):
        build_b3_cluster_constrained(_roster(), clusters=_clusters(), fraction_of_cap=1.5)


# ═════════════════════════════════════════════════════════════════════════
# B-4 concentration reductions
# ═════════════════════════════════════════════════════════════════════════

def test_b4_t1_flatten_caps_t1_and_redistributes_pro_rata():
    result = build_b4_t1_flatten(_roster(), ceiling_pct=2.5, clusters=_clusters())
    w = result["weights"]
    assert w["A"] == 2.5 and w["B"] == 2.5   # both T1 entries flattened to the ceiling
    base = _weights()
    for t in ("C", "D", "E", "F"):
        assert w[t] > base[t]                # every non-T1 entry grew
    assert math.isclose(sum(w.values()), sum(base.values()))  # total nominal sum conserved


def test_b4_t1_flatten_leaves_already_compliant_names_untouched():
    result = build_b4_t1_flatten(_roster(), ceiling_pct=10.0, clusters=_clusters())
    assert result["weights"] == _weights()  # nothing above a 10.0 ceiling


def test_b4_semis_reduction_etf_absorbs_exact():
    semis = ClusterDef("semis", 10.0, ("A", "C"))
    result = build_b4_semis_reduction(_roster(), semis_cluster=semis, etf_tickers=("E", "F"),
                                      factor=0.75, clusters=_clusters())
    w = result["weights"]
    assert math.isclose(w["A"], 2.25) and math.isclose(w["C"], 1.5)
    # removed = (3.0-2.25) + (2.0-1.5) = 1.25, split evenly across E, F
    assert math.isclose(w["E"], 2.0 + 0.625) and math.isclose(w["F"], 2.0 + 0.625)
    assert w["B"] == 3.0 and w["D"] == 1.0  # untouched (not semis, not ETF)
    assert math.isclose(sum(w.values()), sum(_weights().values()))  # conserved


def test_b4_semis_reduction_rejects_bad_factor():
    semis = ClusterDef("semis", 10.0, ("A", "C"))
    with pytest.raises(ValueError):
        build_b4_semis_reduction(_roster(), semis_cluster=semis, etf_tickers=("E",),
                                 factor=1.0, clusters=_clusters())
    with pytest.raises(ValueError):
        build_b4_semis_reduction(_roster(), semis_cluster=semis, etf_tickers=(),
                                 factor=0.5, clusters=_clusters())


# ═════════════════════════════════════════════════════════════════════════
# B-5 nominal budgets
# ═════════════════════════════════════════════════════════════════════════

def test_b5_nominal_budget_scales_every_ticker_uniformly():
    result = build_b5_nominal_budget(_roster(), factor=1.1, clusters=_clusters())
    w = result["weights"]
    base = _weights()
    for t, v in base.items():
        assert math.isclose(w[t], v * 1.1)


def test_b5_rejects_nonpositive_factor():
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), factor=0.0, clusters=_clusters())


# ═════════════════════════════════════════════════════════════════════════
# B-6 comparators (pre-declared non-adoptable)
# ═════════════════════════════════════════════════════════════════════════

def test_b6_inverse_vol_conserves_total_and_favors_lower_vol():
    vol = {"A": 0.2, "B": 0.1, "C": 0.4, "D": 0.1, "E": 0.2, "F": 0.2}
    result = build_b6_inverse_vol(_roster(), volatility=vol, clusters=_clusters())
    w = result["weights"]
    base = _weights()
    assert math.isclose(sum(w.values()), sum(base.values()))
    assert w["B"] > w["A"] > w["C"]  # lower vol (B) -> higher weight than higher vol (A, C)


def test_b6_inverse_vol_rejects_missing_or_nonpositive_volatility():
    with pytest.raises(ValueError):
        build_b6_inverse_vol(_roster(), volatility={"A": 0.2}, clusters=_clusters())
    vol_bad = {t: 0.2 for t in _weights()}
    vol_bad["A"] = 0.0
    with pytest.raises(ValueError):
        build_b6_inverse_vol(_roster(), volatility=vol_bad, clusters=_clusters())


def test_b6_equal_risk_contribution_uncorrelated_matches_inverse_vol_numerically():
    vol = {t: 0.1 + i * 0.05 for i, t in enumerate(_weights())}
    inv = build_b6_inverse_vol(_roster(), volatility=vol, clusters=_clusters())
    erc = build_b6_equal_risk_contribution_uncorrelated(_roster(), volatility=vol, clusters=_clusters())
    assert erc["weights"] == inv["weights"]
    assert erc["variant_id"] != inv["variant_id"]  # distinct label, same numbers, disclosed simplification


# ═════════════════════════════════════════════════════════════════════════
# No scoring/ranking/pooling function exists (mirrors repayment_lib.py's own check)
# ═════════════════════════════════════════════════════════════════════════

def test_no_scoring_ranking_or_pooling_function_exists():
    import target_variants
    public = [n for n in dir(target_variants) if not n.startswith("_")]
    banned = ("rank", "score", "aggregate", "pool")
    offending = [n for n in public if any(b in n.lower() for b in banned)]
    assert offending == []
