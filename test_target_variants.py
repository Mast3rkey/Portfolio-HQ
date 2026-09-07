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


def test_b2_etf_sleeve_pct_is_percent_of_book_not_a_fraction():
    # F-4: new_sleeve_pct is on the roster's own 0-100 weight_pct scale
    # (e.g. 10.0 means "10% of book"), matching TieredWeight.weight_pct --
    # NOT a 0-1 fraction. pre_registration.yaml's B2_sleeves.etf: [0.10,
    # 0.13] registers these budgets as fractions (10%, 13%); a correct S3
    # caller converts 0.10 -> 10.0 before calling this function.
    correct = build_b2_etf_sleeve_budget(_roster(), etf_tickers=("E", "F"),
                                        new_sleeve_pct=10.0, clusters=_clusters())
    assert math.isclose(correct["weights"]["E"] + correct["weights"]["F"], 10.0)

    # Passing the RAW registered fraction (0.10) directly, without
    # converting to this module's percent-of-book scale, targets a sleeve
    # roughly 100x smaller than the registered 10%-of-book arm actually
    # intends -- pinning the exact unit mistake the docstring warns about,
    # not merely asserting the two calls differ.
    naive_fraction = build_b2_etf_sleeve_budget(_roster(), etf_tickers=("E", "F"),
                                               new_sleeve_pct=0.10, clusters=_clusters())
    naive_total = naive_fraction["weights"]["E"] + naive_fraction["weights"]["F"]
    assert math.isclose(naive_total, 0.10)
    assert math.isclose(naive_total * 100.0, correct["weights"]["E"] + correct["weights"]["F"])


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

def test_b5_nominal_budget_sums_to_exact_target_1_10():
    # F-2: target_nominal_total is the TARGET TOTAL itself (matching
    # pre_registration.yaml's literal registered B5_nominal_budgets value
    # of 1.10 = "110%"), NOT a multiplier applied to the roster's own
    # current total -- pins the corrected semantics directly.
    result = build_b5_nominal_budget(_roster(), target_nominal_total=1.10, clusters=_clusters())
    assert math.isclose(sum(result["weights"].values()), 1.10)


def test_b5_nominal_budget_sums_to_exact_target_1_20():
    result = build_b5_nominal_budget(_roster(), target_nominal_total=1.20, clusters=_clusters())
    assert math.isclose(sum(result["weights"].values()), 1.20)


def test_b5_nominal_budget_preserves_relative_proportions():
    result = build_b5_nominal_budget(_roster(), target_nominal_total=1.10, clusters=_clusters())
    w = result["weights"]
    base = _weights()
    base_total = sum(base.values())
    new_total = sum(w.values())
    for t, v in base.items():
        # every ticker's SHARE of the new total equals its share of the old total
        assert math.isclose(w[t] / new_total, v / base_total, rel_tol=1e-9)
    # pairwise ratios between any two tickers are exactly unchanged
    assert math.isclose(w["A"] / w["B"], base["A"] / base["B"], rel_tol=1e-9)
    assert math.isclose(w["E"] / w["F"], base["E"] / base["F"], rel_tol=1e-9)


def test_b5_nominal_budget_does_not_multiply_current_total_by_target():
    # F-2 regression guard: the pre-F-2 (buggy) behavior would have produced
    # sum == current_total * target_nominal_total (13.0 * 1.10 = 14.3 for
    # this fixture roster) -- explicitly assert the corrected output is NOT
    # that, on top of the positive sum==1.10 assertion above.
    result = build_b5_nominal_budget(_roster(), target_nominal_total=1.10, clusters=_clusters())
    buggy_multiplier_total = sum(_weights().values()) * 1.10
    assert not math.isclose(sum(result["weights"].values()), buggy_multiplier_total)


def _percent_of_book_roster():
    # NEW-3: a small roster already on this repository's REAL 0-100
    # percent-of-book weight convention (targets.yaml / TieredWeight
    # everywhere else in this module), current total 103.25 -- matching
    # pre_registration.yaml's own B0_baseline label
    # ("current_targets_yaml_nominal_sum_103.25pct") rather than the
    # fixture roster's smaller, scale-arbitrary total of 13.0.
    return [
        TieredWeight("T1A", "T1", 40.0),
        TieredWeight("T2A", "T2", 30.0),
        TieredWeight("BANDA", "band", 20.0),
        TieredWeight("ETFA", "ETF", 13.25),
    ]


def test_b5_nominal_budget_percent_of_book_scale_sums_to_110_and_120():
    # NEW-3: on a roster using the repository's real percent-of-book scale,
    # the correct target_nominal_total for the registered "110%"/"120%" B-5
    # arms is 110.0/120.0 -- NOT pre_registration.yaml's raw fractional
    # values 1.10/1.20, which on THIS scale would target a total of
    # roughly 1.1%/1.2% of book (a ~100x-too-small mistake in the opposite
    # direction from the original F-2 multiplier bug).
    roster = _percent_of_book_roster()
    result_110 = build_b5_nominal_budget(roster, target_nominal_total=110.0, clusters=[])
    result_120 = build_b5_nominal_budget(roster, target_nominal_total=120.0, clusters=[])
    assert math.isclose(sum(result_110["weights"].values()), 110.0)
    assert math.isclose(sum(result_120["weights"].values()), 120.0)

    base = _weights(roster)
    base_total = sum(base.values())
    assert math.isclose(base_total, 103.25)
    for t, v in base.items():
        # relative proportions preserved on the percent-of-book scale too
        assert math.isclose(result_110["weights"][t] / 110.0, v / base_total, rel_tol=1e-9)
        assert math.isclose(result_120["weights"][t] / 120.0, v / base_total, rel_tol=1e-9)


def test_b5_nominal_budget_fractional_scale_mistake_on_percent_roster_is_off_by_100x():
    # Pins the exact unit mistake the corrected docstring warns about: on a
    # percent-of-book roster, passing pre_registration.yaml's raw
    # fractional value (1.10) instead of the converted percent-of-book
    # value (110.0) produces a total off by a factor of 100.
    roster = _percent_of_book_roster()
    correct = build_b5_nominal_budget(roster, target_nominal_total=110.0, clusters=[])
    mistaken = build_b5_nominal_budget(roster, target_nominal_total=1.10, clusters=[])
    assert math.isclose(sum(mistaken["weights"].values()), 1.10)
    assert math.isclose(sum(mistaken["weights"].values()) * 100.0,
                        sum(correct["weights"].values()))


def test_b5_rejects_nonpositive_target():
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), target_nominal_total=0.0, clusters=_clusters())
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), target_nominal_total=-1.10, clusters=_clusters())


def test_b5_rejects_nan_and_infinite_target():
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), target_nominal_total=float("nan"), clusters=_clusters())
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), target_nominal_total=float("inf"), clusters=_clusters())
    with pytest.raises(ValueError):
        build_b5_nominal_budget(_roster(), target_nominal_total=float("-inf"), clusters=_clusters())


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
