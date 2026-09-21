from pathlib import Path
from decimal import Decimal, localcontext

import pytest
import yaml

from margin_current_s3_preregistration_validator import REGISTER, _finite, main, validate
from margin_simulation import PortfolioState, RepaymentDecision, ScenarioConfig, _leverage_capped_margin, simulate
from repayment_lib import r1_deposits_first, r2_dividends_first


def _mutated(tmp_path: Path, mutate) -> Path:
    data = yaml.safe_load(REGISTER.read_text())
    mutate(data)
    path = tmp_path / "scope.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def test_scoping_register_is_incomplete_and_consistent():
    assert validate() == []


def test_current_inventory_numeric_owners_and_roster_counts_match_live_yaml():
    targets = yaml.safe_load(Path("targets.yaml").read_text())
    rows = targets["destination"]
    assert len(rows) == 36
    assert sum(row["target_pct"] for row in rows) == pytest.approx(99.25)
    assert targets["caps"]["clusters"] == [
        {"name": "semis", "pct": 25.0, "tickers": ["ASML", "TSM", "NVDA", "AVGO", "KLAC"]},
        {"name": "power_infra", "pct": 20.0, "tickers": ["ETN", "GEV", "PWR"]},
        {"name": "oil", "pct": 20.0, "tickers": []},
    ]
    assert targets["margin"] == {"leverage_cap": 1.8, "buffer_floor_pct": 30.0}
    assert targets["levels"] == {"rung_atr_multipliers": [1.0, 2.0, 3.0], "practicality_cap_pct": 25, "swing_low_sessions": 60}
    assert targets["gates"] == {"min_lot_dollars": 25, "trend_rsi_override": 30, "earnings_blackout_days": 7}


@pytest.mark.parametrize("mutation", [
    lambda d: d.update(study_id="SWAPPED"),
    lambda d: d.update(status="PREREGISTERED_NOT_EXECUTED"),
    lambda d: d["required_unresolved_decisions"].pop(),
    lambda d: d["execution"].update(historical_execution_authorized=True),
    lambda d: d["exposure_and_coverage_ledger"]["successor_fresh_period"].update(status="FRESH"),
    lambda d: d["candidate_registry"].update(status="FROZEN"),
    lambda d: d["trial_budget"].update(status="DEFINED"),
])
def test_authority_and_scope_mutations_fail_closed(tmp_path, mutation):
    assert validate(_mutated(tmp_path, mutation))


def test_duplicate_key_and_nonfinite_and_wrong_type_fail_closed(tmp_path):
    duplicate = tmp_path / "duplicate.yaml"
    duplicate.write_text(REGISTER.read_text() + "\nstudy_id: AGAIN\n")
    assert "duplicate key" in validate(duplicate)[0]
    nonfinite = tmp_path / "nonfinite.yaml"
    nonfinite.write_text(REGISTER.read_text() + "\nnonfinite: .nan\n")
    assert validate(nonfinite) == ["register must be a finite mapping with string keys"]
    assert validate(_mutated(tmp_path, lambda d: d.update(required_unresolved_decisions="wrong")))


@pytest.mark.parametrize("mutation, expected", [
    (lambda d: d.update(required_unresolved_decisions=[{}]), "missing, duplicate, or changed unresolved-decision register"),
    (lambda d: d.update(candidate_registry=None), "candidate registry must remain undefined"),
    (lambda d: d.update(trial_budget=[]), "trial budget must remain undefined"),
    (lambda d: d["exposure_and_coverage_ledger"].update(original_margin_track_2=None), "original Track 2 exposure record must be a mapping"),
    (lambda d: d["exposure_and_coverage_ledger"].update(successor_fresh_period=None), "successor fresh-period record must be a mapping"),
])
def test_nested_malformed_values_return_clear_errors(tmp_path, mutation, expected):
    assert expected in validate(_mutated(tmp_path, mutation))


def test_huge_integer_returns_error_instead_of_crashing(tmp_path):
    path = tmp_path / "huge.yaml"
    path.write_text(REGISTER.read_text() + f"\nunexpected_huge_integer: {1 << 4096}\n")
    assert validate(path) == ["register must be a finite mapping with string keys"]


def test_recursive_yaml_alias_returns_controlled_failure_without_traceback(tmp_path, capsys):
    path = tmp_path / "recursive.yaml"
    path.write_text(REGISTER.read_text() + "\nrecursive: &recursive [*recursive]\n")
    expected = ["register must be a finite mapping with string keys"]
    assert validate(path) == expected
    assert main(path) == 1
    captured = capsys.readouterr()
    assert captured.out == "ERROR: register must be a finite mapping with string keys\n"
    assert captured.err == ""


def test_ordinary_reused_aliases_remain_valid(tmp_path):
    path = tmp_path / "shared.yaml"
    path.write_text(REGISTER.read_text() + "\nshared: &shared [alpha, {beta: 1}]\nleft: *shared\nright: *shared\n")
    assert validate(path) == []


def test_deep_and_exponentially_shared_acyclic_structures_are_bounded():
    deep: object = "leaf"
    for _ in range(5000):
        deep = [deep]
    assert _finite(deep)

    shared: object = "leaf"
    for _ in range(5000):
        shared = [shared, shared]
    assert _finite(shared)


def test_margin_cost_source_and_whole_portfolio_costs_are_not_conflated():
    scope = yaml.safe_load(REGISTER.read_text())
    inherited = scope["preserved_design_requirements_from_margin_0005"]
    assert inherited["costs_bps_one_way"] == ["0", "5", "15"]
    assert inherited["excluded_cost_registry"] == "PORTFOLIO_ROBUSTNESS_V2_0_10_25_BPS_NOT_IMPORTED"
    oracle = scope["proposed_accounting_contract"]["synthetic_oracle_10bps_fixture_only"]
    assert oracle["classification"] == "SYNTHETIC_ARITHMETIC_NOT_MARGIN_0005_COST_CELL_OR_ACCOUNT_FACT"


def test_cost_aware_synthetic_oracle_and_book_conservation():
    with localcontext() as context:
        context.prec = 50
        G_o, D_o, C_o, F, L = map(Decimal, ("180", "80", "0", "100", "1.25"))
        s = b = Decimal("0.001")
        N_o, B_o = G_o - D_o, G_o + C_o - D_o
        C_a, B_a = C_o + F, B_o + F
        repayment = min(F, D_o, max(Decimal(0), G_o / L - N_o))
        assert repayment == Decimal("44")
        G_i, D_i, C_i = G_o, D_o - repayment, C_a - repayment
        N_i, B_i = G_i - D_i, G_i + C_i - D_i
        A_i, P_i = F - repayment, C_o
        assert (G_i, D_i, C_i, N_i, B_i, A_i, P_i) == tuple(map(
            Decimal, ("180", "36", "56", "144", "200", "56", "0")
        ))
        assert B_i == B_a  # cash repayment lowers cash and debt equally
        assert C_i == A_i + P_i

        legacy_capacity = Decimal(str(_leverage_capped_margin(
            float(G_i), float(D_i), float(A_i), float(L), float("inf"))))
        assert legacy_capacity == Decimal("14")
        legacy_purchase = (A_i + legacy_capacity) / (1 + b)
        legacy_leverage = (G_i + legacy_purchase) / (N_i + legacy_purchase - legacy_capacity)
        assert legacy_purchase.quantize(Decimal("0.0000000001")) == Decimal("69.9300699301")
        assert legacy_leverage.quantize(Decimal("0.0000000001")) == Decimal("1.2500874432")
        assert legacy_leverage > L  # raw helper is not fee-safe when its full capacity is used

        wrong_arrival_reuse = (
            (1 + b) * (L * N_i - G_i) + (L - 1) * F
        ) / (1 + L * b)
        wrong_purchase = (A_i + wrong_arrival_reuse) / (1 + b)
        wrong_leverage = (G_i + wrong_purchase) / (
            N_i + wrong_purchase - wrong_arrival_reuse
        )
        assert wrong_arrival_reuse.quantize(Decimal("0.0000000001")) == Decimal("24.9687890137")
        assert wrong_leverage.quantize(Decimal("0.000000000001")) == Decimal("1.304967285887")
        assert wrong_leverage > L

        cost_capacity = (
            (1 + b) * (L * N_i - G_i) + (L - 1) * A_i
        ) / (1 + L * b)
        p_cap = (A_i + cost_capacity) / (1 + b)
        assert cost_capacity.quantize(Decimal("0.0000000001")) == Decimal("13.9825218477")
        assert p_cap.quantize(Decimal("0.0000000001")) == Decimal("69.9126092385")
        assert (G_i + p_cap) / (N_i + p_cap - cost_capacity) == L
        C_e, D_e, G_e = C_i + cost_capacity - (1 + b) * p_cap, D_i + cost_capacity, G_i + p_cap
        assert C_e == P_i
        assert G_e + C_e - D_e == B_i - b * p_cap

        zero_cost_capacity = (L * N_i - G_i) + (L - 1) * A_i
        assert zero_cost_capacity == legacy_capacity

        p_cash = A_i / (1 + b)
        assert p_cash.quantize(Decimal("0.0000000001")) == Decimal("55.9440559441")
        assert G_i + (C_i - (1 + b) * p_cash) + p_cash - D_i == B_i - b * p_cash

        partial_purchase = Decimal("20")
        partial_cost = b * partial_purchase
        partial_draw = max(Decimal(0), (1 + b) * partial_purchase - A_i)
        residual_cash = A_i + partial_draw - partial_purchase - partial_cost
        assert partial_draw == 0
        assert residual_cash == Decimal("35.980")
        assert partial_draw < cost_capacity

        above_cap_G, above_cap_D, cash = map(Decimal, ("160", "40", "1"))
        above_cap_N = above_cap_G - above_cap_D
        assert above_cap_G / above_cap_N > L
        infeasible_capacity = max(Decimal(0), (
            (1 + b) * (L * above_cap_N - above_cap_G) + (L - 1) * cash
        ) / (1 + L * b))
        assert infeasible_capacity == 0
        assert cash == Decimal("1")  # no gap means no draw, no fee, and explicit residual cash

        q = (G_o - L * N_o) / (1 - L * s)
        assert q.quantize(Decimal("0.0000000001")) == Decimal("55.0688360451")
        lhs = (G_o - q) - (D_o - (1 - s) * q)
        rhs = N_o - s * q
        assert abs(lhs - rhs) < Decimal("1e-24")


@pytest.mark.parametrize("debt, repayment, expected", [
    pytest.param("80", "0", ("180", "80", "110", "100", "210", "100", "10"), id="none"),
    pytest.param("80", "44", ("180", "36", "66", "144", "210", "56", "10"), id="partial-source"),
    pytest.param("80", "80", ("180", "0", "30", "180", "210", "20", "10"), id="full-debt-not-full-source"),
    pytest.param("150", "100", ("180", "50", "10", "130", "140", "0", "10"), id="full-source"),
])
def test_staged_cash_sources_none_partial_full_repayment_and_protected_cash(debt, repayment, expected):
    G_o, D_o, C_o, F = map(Decimal, ("180", debt, "10", "100"))
    P_o, E_o, R = Decimal("10"), Decimal("0"), Decimal(repayment)
    assert C_o == P_o + E_o
    G_a, D_a, C_a = G_o, D_o, C_o + F
    B_a = G_a + C_a - D_a
    G_i, D_i, C_i = G_a, D_a - R, C_a - R
    N_i, B_i = G_i - D_i, G_i + C_i - D_i
    A_i, P_i = E_o + F - R, P_o
    assert (G_i, D_i, C_i, N_i, B_i, A_i, P_i) == tuple(map(Decimal, expected))
    assert B_i == B_a
    assert C_i == A_i + P_i
    b = Decimal("0.001")
    p_executed = min(Decimal("10"), A_i / (1 + b))
    x_actual = max(Decimal(0), (1 + b) * p_executed - A_i)
    assert x_actual == 0
    G_e, D_e = G_i + p_executed, D_i + x_actual
    C_e = C_i + x_actual - (1 + b) * p_executed
    assert C_e == P_i + (A_i - (1 + b) * p_executed)
    assert G_e + C_e - D_e == B_i - b * p_executed


def test_two_arrivals_and_preexisting_cash_route_sequentially_without_reset_or_recredit():
    G, D, C = map(Decimal, ("180", "80", "30"))
    P, E = Decimal("10"), Decimal("20")
    assert C == P + E
    opening_book = G + C - D
    routed = []
    residuals = {}
    for source, family, arrival, eligible in (
        ("E", "explicit_r1_formula", Decimal("0"), E),
        ("F_deposit", "r1", Decimal("60"), Decimal("60")),
        ("F_dividend", "r2_treatment", Decimal("40"), Decimal("40")),
    ):
        C += arrival
        N = G - D
        if family in {"explicit_r1_formula", "r1"}:
            repay = min(eligible, D, max(Decimal(0), G / Decimal("1.25") - N))
        else:
            repay = min(eligible, D)
        C, D = C - repay, D - repay
        routed.append(repay)
        residuals[source] = eligible - repay
    R = sum(routed, Decimal(0))
    A_i = sum(residuals.values(), Decimal(0))
    N_i, B_i = G - D, G + C - D
    assert routed == [Decimal("20"), Decimal("24"), Decimal("36")]
    assert R == Decimal("80")  # includes r_E and each source exactly once
    assert (G, D, C, N_i, B_i, A_i, P) == tuple(map(
        Decimal, ("180", "0", "50", "180", "230", "40", "10")
    ))
    assert B_i == opening_book + Decimal("100")
    assert C == P + A_i


def _route_source_cash(source, selection, eligible, debt, gross, target):
    """Independent synthetic reconstruction of the proposed dispatcher."""
    eligible, debt, gross, target = map(Decimal, (eligible, debt, gross, target))
    applicability = {
        "R1_DEPOSIT_TARGET_RESTORATION": "EXTERNAL_DEPOSIT",
        "R2_DIVIDEND_TREATMENT": "DIVIDEND",
        "R2_DIVIDEND_REINVEST_CONTROL": "DIVIDEND",
    }
    if selection in applicability and source != applicability[selection]:
        raise ValueError("routing family is not applicable to source")
    if selection == "R1_DEPOSIT_TARGET_RESTORATION":
        net = gross - debt
        return min(eligible, debt, max(Decimal(0), gross / target - net))
    if selection == "R2_DIVIDEND_TREATMENT":
        return min(eligible, debt)
    if selection in {"R2_DIVIDEND_REINVEST_CONTROL", "NO_REPAYMENT_ROUTE"}:
        return Decimal(0)
    raise ValueError("explicit existing-cash rule is not supplied")


@pytest.mark.parametrize("gross,debt", [("130", "36"), ("180", "36"), ("220", "36")])
@pytest.mark.parametrize("dividend,expected", [("20", "20"), ("36", "36"), ("40", "36")])
def test_r2_treatment_is_debt_limited_not_target_limited_across_leverage_states(gross, debt, dividend, expected):
    repayment = _route_source_cash(
        "DIVIDEND", "R2_DIVIDEND_TREATMENT", dividend, debt, gross, "1.25"
    )
    assert repayment == Decimal(expected)
    residual = Decimal(dividend) - repayment
    ending_debt = Decimal(debt) - repayment
    assert repayment + residual == Decimal(dividend)
    assert ending_debt >= 0 and residual >= 0

    state = PortfolioState(0, float(dividend), {}, float(debt), float(gross))
    retained = r2_dividends_first(state, dividend_cash=float(dividend))
    assert Decimal(str(retained.repay_amount)) == repayment


def test_r2_zero_debt_reinvest_control_and_source_nonapplicability():
    assert _route_source_cash("DIVIDEND", "R2_DIVIDEND_TREATMENT", "40", "0", "180", "1.25") == 0
    assert _route_source_cash("DIVIDEND", "R2_DIVIDEND_REINVEST_CONTROL", "40", "36", "180", "1.25") == 0
    state = PortfolioState(0, 40.0, {}, 36.0, 180.0)
    assert r2_dividends_first(state, dividend_cash=40.0, reinvest=True).repay_amount == 0
    for source, selection in (
        ("CORPORATE_ACTION", "R2_DIVIDEND_TREATMENT"),
        ("EXTERNAL_DEPOSIT", "R2_DIVIDEND_TREATMENT"),
        ("DIVIDEND", "R1_DEPOSIT_TARGET_RESTORATION"),
        ("PRE_EXISTING_CASH", "R2_DIVIDEND_TREATMENT"),
    ):
        with pytest.raises(ValueError, match="not applicable"):
            _route_source_cash(source, selection, "40", "36", "180", "1.25")


def test_old_target_limited_r2_substitution_is_rejected_by_validator(tmp_path):
    old_universal = "r_j=min(U_j,D_j_pre,max(0,G_j_pre/L_star-N_j_pre))"
    path = _mutated(tmp_path, lambda d: d["proposed_accounting_contract"]["stages"]
                    ["source_events_j"]["routing_rules"].update(
                        R2_DIVIDEND_TREATMENT=old_universal))
    assert validate(path) == ["source-specific cash routing contract changed or incomplete"]
    assert main(path) == 1

    # Reproduce the defect: at the recorded post-R1 state it repays zero,
    # whereas the source-defined R2 treatment clears the 36 debt and leaves 4.
    G, D, dividend, target = map(Decimal, ("180", "36", "40", "1.25"))
    old_result = min(dividend, D, max(Decimal(0), G / target - (G - D)))
    assert old_result == 0
    assert _route_source_cash("DIVIDEND", "R2_DIVIDEND_TREATMENT", dividend, D, G, target) == 36


def test_optional_trim_off_and_on_branches_are_distinct_and_conserve_book_net_of_cost():
    G_c, D_c, C_c, L, s = map(Decimal, ("180", "80", "10", "1.25", "0.001"))
    N_c, B_c = G_c - D_c, G_c + C_c - D_c
    candidate_q = max(Decimal(0), (G_c - L * N_c) / (1 - L * s))
    assert candidate_q.quantize(Decimal("0.0000000001")) == Decimal("55.0688360451")

    # No selected/authorized trim event: the candidate formula is not executed.
    q_off = r_off = Decimal(0)
    assert (G_c - q_off, D_c - r_off, C_c, N_c, B_c) == (G_c, D_c, C_c, N_c, B_c)

    # Selected/authorized synthetic branch: direct net proceeds repay debt and sale cost reduces book.
    q_on = candidate_q
    r_on = (1 - s) * q_on
    assert q_on <= G_c and r_on <= D_c
    G_i, D_i, C_i = G_c - q_on, D_c - r_on, C_c
    N_i, B_i = G_i - D_i, G_i + C_i - D_i
    assert abs(N_i - (N_c - s * q_on)) < Decimal("1e-24")
    assert abs(B_i - (B_c - s * q_on)) < Decimal("1e-24")


def _assert_cost_capacity_evidence(scope):
    contract = scope["proposed_accounting_contract"]
    stages = contract["stages"]
    assert stages == {
        "window_open_0": {
            "scope": "LOCAL_ACCOUNTING_WINDOW_AFTER_ANY_PRIOR_MANDATORY_CURE_AND_INTEREST; NOT_A_FULL_DAILY_ENGINE",
            "definitions": ["G_0", "D_0", "C_0", "N_0=G_0-D_0", "B_0=G_0+C_0-D_0"],
            "cash_partition": "C_0=P_0+E_0; P_0=PROTECTED_OR_NONDEPLOYABLE; E_0=EXPLICITLY_ADMITTED_PRE_EXISTING_CASH",
        },
        "source_events_j": {
            "disjoint_indices": "J={E} UNION K; E=PRE_EXISTING_ADMITTED_BUCKET; K=SOURCE_ARRIVAL_BUCKETS; E_NOT_IN_K",
            "event_amounts": "f_E=0; U_E=E_0; FOR_k_IN_K f_k=F_k_AND_U_k=F_k",
            "predecessor": "EACH_j_READS_ONLY_STATE_j_minus_1; NO_EVENT_READS_WINDOW_OPEN_0_AFTER_A_PREDECESSOR_EXISTS",
            "before_route": ["G_j_pre=G_j_minus_1", "D_j_pre=D_j_minus_1", "C_j_pre=C_j_minus_1+f_j", "N_j_pre=G_j_pre-D_j_pre", "B_j_pre=G_j_pre+C_j_pre-D_j_pre"],
            "routing_selection": "EXACTLY_ONE_FAMILY_SOURCE_CONTROL_RULE_PER_EVENT; NO_IMPLICIT_COMPOSITION",
            "routing_rules": {
                "R1_DEPOSIT_TARGET_RESTORATION": "SOURCE_MUST_BE_EXTERNAL_DEPOSIT; r_j=min(U_j,D_j_pre,max(0,G_j_pre/L_star-N_j_pre))",
                "R2_DIVIDEND_TREATMENT": "SOURCE_MUST_BE_ADMITTED_DIVIDEND; r_j=min(U_j,D_j_pre); EXCESS_U_j_MINUS_r_j_REMAINS_RESIDUAL_ONLY_AFTER_DEBT_CLEARS",
                "R2_DIVIDEND_REINVEST_CONTROL": "SOURCE_MUST_BE_ADMITTED_DIVIDEND; r_j=0",
                "EXISTING_CASH_EXPLICIT_RULE": "SOURCE_MUST_BE_E; ROUTE_REQUIRES_SEPARATELY_ADMITTED_RULE_AND_AMOUNT_OTHERWISE_r_j=0",
                "NO_REPAYMENT_ROUTE": "r_j=0",
            },
            "source_applicability": "CORPORATE_ACTION_PROTECTED_AND_PRE_EXISTING_CASH_ARE_NOT_DIVIDENDS; EXTERNAL_DEPOSIT_IS_NOT_DIVIDEND; CLASSIFICATION_CANNOT_CHANGE_TO_SELECT_A_RULE",
            "route_bounds": "0_le_r_j_le_min(U_j,D_j_pre); REPAYMENT_RULES_NEVER_BORROW",
            "after_route": ["G_j=G_j_pre", "D_j=D_j_pre-r_j", "C_j=C_j_pre-r_j", "N_j=N_j_pre+r_j", "B_j=B_j_pre"],
            "classification": "EACH_F_k_RETAINS_EXTERNAL_FLOW_OR_RETURN_CASH_CLASSIFICATION; EACH_U_j_IS_ROUTED_AT_MOST_ONCE",
        },
        "cash_routing_c": {
            "total": "R=r_E+sum_k_in_K(r_k)",
            "terminal_state": ["G_c=G_last", "D_c=D_0-R", "C_c=C_0+sum_k_in_K(F_k)-R", "N_c=G_c-D_c", "B_c=G_c+C_c-D_c"],
            "residual_partition": "A_c=(E_0-r_E)+sum_k_in_K(F_k-r_k); P_c=P_0; C_c=P_c+A_c",
            "bounds": ["0_le_r_E_le_E_0", "0_le_r_k_le_F_k", "0_le_A_c_le_C_c", "NO_RESET_NO_CUMULATIVE_RECREDIT_NO_DOUBLE_ROUTE"],
        },
        "post_routing_i": {
            "trim_off_branch": "IF_NO_SEPARATELY_SELECTED_AND_AUTHORIZED_TRIM_EVENT_THEN_q=0_AND_r_trim=0_AND_STATE_i=STATE_c",
            "trim_on_branch": "IF_SELECTED_AUTHORIZED_TRIM_EVENT_THEN_q=max(0,(G_c-L_star*N_c)/(1-L_star*s))_SUBJECT_TO_0_le_q_le_G_c_AND_0_le_(1-s)*q_le_D_c; r_trim=(1-s)*q",
            "trim_on_identities": ["G_i=G_c-q", "D_i=D_c-r_trim", "C_i=C_c", "N_i=N_c-s*q", "B_i=B_c-s*q"],
            "residual_deployable_cash": "A_i=A_c; P_i=P_c; C_i=P_i+A_i",
            "admission_rule": "ONLY_UNROUTED_DISJOINT_BUCKET_RESIDUALS_ENTER_A_i; ALL_OTHER_CASH_IS_P_i",
            "bounds": ["0_le_A_i_le_C_i", "0_le_P_i_le_C_i", "NO_SOURCE_DOLLAR_ROUTED_OR_DEPLOYED_TWICE"],
        },
        "purchase_e": {
            "identities": ["x_actual=max(0,(1+b)*p_executed-A_i)", "G_e=G_i+p_executed", "D_e=D_i+x_actual", "C_e=C_i+x_actual-(1+b)*p_executed", "N_e=G_e-D_e", "B_e=G_e+C_e-D_e=B_i-b*p_executed"],
            "residual": "C_e=P_i+(A_i+x_actual-(1+b)*p_executed)",
        },
    }
    assert contract["identities"]["cost_aware_full_deployment_capacity"] == (
        "x_cap=max(0,((1+b)*(H*N_i-G_i)+(H-1)*A_i)/(1+H*b))"
    )
    assert contract["identities"]["executed_draw_cash_first"] == (
        "x_actual=max(0,(1+b)*p_executed-A_i)"
    )
    assert contract["identities"]["cash_repayment_dispatch"] == (
        "r_j=THE_SINGLE_SELECTED_SOURCE_APPLICABLE_RULE_IN_stages.source_events_j.routing_rules"
    )
    oracle = contract["synthetic_oracle_10bps_fixture_only"]
    assert oracle["inputs"] == {
        "G_o": "180", "D_o": "80", "C_o": "0", "source_arrival_F_deposit": "100",
        "L_star": "1.25", "sale_cost_s": "0.001", "buy_cost_b": "0.001",
    }
    assert oracle["staged_state"] == {
        "R": "44", "G_i": "180", "D_i": "36", "C_i": "56", "N_i": "144",
        "B_i": "200", "residual_deployable_A_i": "56", "protected_P_i": "0",
    }
    legacy = oracle["inherited_zero_buy_cost_capacity"]
    proposed = oracle["proposed_cost_aware_capacity"]
    assert legacy == {
        "raw_legacy_comparator_x": "14",
        "full_deployment_with_10bps_purchase_p": "69.9300699301",
        "resulting_leverage": "1.2500874432",
        "disposition": "OVERSHOOTS_1_25_NOT_COST_SAFE_CAPACITY_NOT_ACTUAL_DRAW",
    }
    assert proposed == {
        "maximum_new_draw_x": "13.9825218477",
        "full_gap_purchase_p": "69.9126092385",
        "resulting_leverage": "1.25",
        "actual_draw": "GAP_LOT_GATE_DEPENDENT_MAY_BE_LOWER_OR_ZERO",
    }
    assert contract["deployment_semantics"]["COST_AWARE_CAPACITY_PROPOSAL"]["classification"] == (
        "PROPOSED_FEE_RESERVATION_BEFORE_WEIGHTED_GAP_ALLOCATION_NOT_IMPLEMENTED"
    )
    proposal = contract["deployment_semantics"]["COST_AWARE_CAPACITY_PROPOSAL"]
    assert proposal["execution"] == (
        "CASH_FIRST; x_actual=max(0,(1+b)*p_executed-A_i); x_actual_le_x_cap"
    )
    assert proposal["infeasible"] == (
        "IF_N_i_LE_0_OR_PRE_PURCHASE_G_i/N_i_ABOVE_H_THEN_NO_NEW_DRAW_AND_MANDATORY_CURE_OR_FAILED_CELL"
    )


def test_cost_capacity_claim_is_bound_to_adverse_evidence_mutations():
    scope = yaml.safe_load(REGISTER.read_text())
    _assert_cost_capacity_evidence(scope)
    for section, field, bad in (
        ("inherited_zero_buy_cost_capacity", "resulting_leverage", "1.25"),
        ("inherited_zero_buy_cost_capacity", "disposition", "COST_SAFE"),
        ("proposed_cost_aware_capacity", "maximum_new_draw_x", "14"),
        ("proposed_cost_aware_capacity", "actual_draw", "FORCED_TO_CAPACITY"),
    ):
        mutated = yaml.safe_load(REGISTER.read_text())
        mutated["proposed_accounting_contract"]["synthetic_oracle_10bps_fixture_only"][section][field] = bad
        with pytest.raises(AssertionError):
            _assert_cost_capacity_evidence(mutated)

    for mutate in (
        lambda d: d["proposed_accounting_contract"]["stages"].pop("post_routing_i"),
        lambda d: d["proposed_accounting_contract"]["stages"]["post_routing_i"].update(
            residual_deployable_cash="A_i=F"
        ),
        lambda d: d["proposed_accounting_contract"]["stages"]["cash_routing_c"].update(total="R=0"),
        lambda d: d["proposed_accounting_contract"]["stages"]["source_events_j"].update(
            after_route=["G_j=G_j_pre", "D_j=D_j_pre", "C_j=C_j_pre"]
        ),
        lambda d: d["proposed_accounting_contract"]["stages"]["source_events_j"].update(
            predecessor="EVERY_EVENT_RESETS_TO_WINDOW_OPEN_0"
        ),
        lambda d: d["proposed_accounting_contract"]["stages"]["post_routing_i"].update(
            trim_off_branch="ALWAYS_COMPUTE_q"
        ),
        lambda d: d["proposed_accounting_contract"]["identities"].update(
            cost_aware_full_deployment_capacity="x_cap=FORMULA_USING_ORIGINAL_F"
        ),
        lambda d: d["proposed_accounting_contract"]["synthetic_oracle_10bps_fixture_only"]["staged_state"].update(
            residual_deployable_A_i="100"
        ),
    ):
        mutated = yaml.safe_load(REGISTER.read_text())
        mutate(mutated)
        with pytest.raises(AssertionError):
            _assert_cost_capacity_evidence(mutated)


def test_three_deployment_semantics_and_source_ledger_remain_distinct():
    scope = yaml.safe_load(REGISTER.read_text())
    contract = scope["proposed_accounting_contract"]
    assert set(contract["deployment_semantics"]) == {
        "CASH_ONLY_NO_NEW_DRAW_PROPOSAL",
        "INHERITED_DEPOSIT_DAY_CAPACITY_AND_WEIGHTED_GAPS",
        "COST_AWARE_CAPACITY_PROPOSAL",
        "GENUINE_END_CYCLE_TARGET_PROPOSAL",
    }
    inherited = contract["deployment_semantics"]["INHERITED_DEPOSIT_DAY_CAPACITY_AND_WEIGHTED_GAPS"]
    assert inherited["meaning"].startswith("LEGACY_RAW_CAPACITY_IGNORES_BUY_FEES")
    assert "same_cycle_reborrow" in contract["repayment_source_ledger"]["fields"]
    assert scope["candidate_mapping_proposal"]["status"] == "PARTIAL_SOURCE_DERIVED_NOT_ACCEPTED_REGISTRY"


def test_reviewer_source_dispositions_do_not_claim_acquisition_or_admission():
    text = Path("research/current_architecture_readiness/EVIDENCE_AND_INPUT_REMEDIATION.md").read_text()
    assert "illustrative first-day VWAP values 414.44/21.08" in text
    assert "not proof of coverage or admission" in text
    assert "no archive path, returned bytes, byte count, hash, or receipt" in text


def test_r1_pretrade_reproduction_requires_future_event_order_regression():
    dates = ["2000-01-03", "2000-01-04"]
    calls = 0

    def hook(state, prior_gross):
        nonlocal calls
        calls += 1
        if calls == 1:
            return RepaymentDecision(leverage_target=1.8)
        return r1_deposits_first(state, prior_gross, is_deposit_day=True, target_leverage=1.25)

    result = simulate(
        ScenarioConfig("synthetic", 1.8, 0.0, 0.0, pre_trade_fn=hook),
        {"X": 1.0}, {"X": ([100.0, 100.0], 0)}, dates, dates,
        deposit_amount=100.0, min_lot=1.0,
    )
    repayments = [e for e in result.events if e["kind"] == "repayment"]
    day1 = [e for e in result.events if e["day"] == 1]
    assert result.gross_series == pytest.approx([180.0, 200.0])
    assert result.debt_series == pytest.approx([80.0, 25.0])
    assert result.cash_series == pytest.approx([0.0, 25.0])
    assert repayments == [{"day": 1, "kind": "repayment", "amount": pytest.approx(55.0), "source": "pre_trade"}]
    assert [e["kind"] for e in day1].index("repayment") < [e["kind"] for e in day1].index("deposit")
    assert result.tax_lot_events[0]["shares_sold"] == pytest.approx(0.55)
    assert result.tax_lot_events[0]["sale_day"] == 1
