from __future__ import annotations

import copy
import inspect
import json
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

import level1_sleeve_robustness_preregistration_validator as authority
import risk_level1_acquisition as acquisition
import risk_level1_attempt2_attestation as attempt2_attestation
import risk_level1_core as core
import risk_level1_data_manifest_validator as manifest_validator
import risk_level1_runner as runner
from test_level1_sleeve_robustness_preregistration_validator import raw_study_evidence


def bar(day: str, close: float = 100.0) -> dict:
    return {"date": day, "open": close, "high": close, "low": close, "close": close, "volume": 1.0}


def document(rows, events=(), provider="YAHOO_FINANCE_CHART"):
    return {"schema_version": "1.0", "instrument": "TEST", "provider": provider,
            "adjustment": "RAW_CLOSE_PLUS_EXPLICIT_EVENTS", "rows": list(rows), "events": list(events)}


def test_authority_and_frozen_implementation_config_identity():
    assert not authority.validate_repository().errors
    config = core.load_yaml(core.CONFIG_PATH)
    assert core.sha256_file(core.PROTOCOL_PATH) == config["authority"]["protocol_sha256"]
    assert core.sha256_file(core.PREREG_PATH) == config["authority"]["preregistration_sha256"]
    assert config["execution"]["exact_registered_cell_count"] == 777
    assert config["execution"]["reserve_trials"] == 0


def test_source_hierarchy_and_whole_path_fallback_are_exact():
    config = core.load_yaml(core.CONFIG_PATH)
    prereg = core.load_yaml(core.PREREG_PATH)
    assert prereg["fallback_order"]["equities_etfs"] == ["ALPACA_MARKET_DATA", "YAHOO_FINANCE_CHART", "ABSTAIN"]
    assert prereg["fallback_order"]["crypto"] == ["ALPACA_CRYPTO", "COINBASE_EXCHANGE", "ABSTAIN"]
    assert config["acquisition"]["equities_etfs"]["whole_path_only"] is True
    assert config["acquisition"]["crypto"]["whole_path_only"] is True
    assert config["acquisition"]["equities_etfs"]["parameters"]["feed"] == "sip"


@pytest.mark.parametrize("mutation", [
    lambda rows: rows + [copy.deepcopy(rows[-1])],
    lambda rows: [{**rows[0], "high": 90.0}] + rows[1:],
    lambda rows: [{**rows[0], "close": 0.0}] + rows[1:],
])
def test_data_quality_duplicate_and_ohlc_failures(mutation):
    rows = [bar("2022-01-03"), bar("2022-01-04")]
    quality = acquisition.bar_quality(document(mutation(rows)), crypto=False)
    assert quality["duplicates"] or quality["invalid_ohlc"]


def test_structured_gap_inventory_and_no_zero_fill():
    rows = [bar("2022-01-03"), bar("2022-01-05")]
    quality = acquisition.bar_quality(document(rows), crypto=True)
    assert quality["missing_count"] == 1
    assert quality["gap_blocks"] == [{"start": "2022-01-04", "end": "2022-01-04", "count": 1}]
    with pytest.raises(core.IntegrityError):
        core.total_return_index(document([bar("2022-01-03")]), "2022-01-03", "2022-01-04")


def test_total_return_credits_dividend_once_and_does_not_credit_split():
    rows = [bar("2022-01-03"), bar("2022-01-04")]
    dividend = {"action_type": "cash_dividend", "ex_date": "2022-01-04", "rate": 1.0}
    split = {"action_type": "split", "ex_date": "2022-01-04", "new_rate": 2.0, "old_rate": 1.0}
    div_index = core.total_return_index(document(rows, [dividend]), "2022-01-03", "2022-01-04")
    split_index = core.total_return_index(document(rows, [split]), "2022-01-03", "2022-01-04")
    assert div_index[-1][1] == pytest.approx(1.01)
    assert split_index[-1][1] == pytest.approx(1.0)


def test_alpaca_dividend_is_put_on_split_adjusted_share_basis_without_double_count():
    rows = [bar("2022-01-03"), bar("2022-01-04"), bar("2022-01-06")]
    events = [
        {"action_type": "cash_dividend", "ex_date": "2022-01-04", "rate": 2.0},
        {"action_type": "split", "ex_date": "2022-01-05", "new_rate": 2.0, "old_rate": 1.0},
    ]
    index = core.total_return_index(document(rows, events, provider="ALPACA_MARKET_DATA"), "2022-01-03", "2022-01-06")
    assert index[-1][1] == pytest.approx(1.01)


def test_yahoo_close_is_already_split_adjusted_without_importing_adjusted_close_total_return():
    stamps = [int(__import__("datetime").datetime.fromisoformat(day + "T14:30:00+00:00").timestamp())
              for day in ("2022-01-03", "2022-01-04", "2022-01-06")]
    payload = {"chart": {"result": [{"timestamp": stamps,
               "indicators": {"quote": [{"open": [50, 51, 51], "high": [50, 51, 51],
                                            "low": [50, 51, 51], "close": [50, 51, 51],
                                            "volume": [1, 1, 2]}]},
               "events": {"splits": {"x": {"date": int(__import__("datetime").datetime.fromisoformat("2022-01-05T14:30:00+00:00").timestamp()),
                                                     "numerator": 2, "denominator": 1}}}}]}}
    normalized = acquisition.normalize_yahoo("TEST", payload)
    assert [row["close"] for row in normalized["rows"]] == [50.0, 51.0, 51.0]
    index = core.total_return_index(normalized, "2022-01-03", "2022-01-06")
    assert index[-1][1] == pytest.approx(1.02)


def test_gold_path_has_no_second_expense_subtraction_surface():
    source = Path(core.ROOT / "risk_level1_core.py").read_text(encoding="utf-8")
    assert "expense_ratio" not in source
    assert "second expense" not in source.lower()


def dff_doc(start: str, end: str, rate: str = "3.60"):
    business = core.federal_business_days(start, end)
    return {"schema_version": "1.0", "series": "DFF", "provider": "FRED",
            "rows": [{"date": day, "rate_pct": rate} for day in business]}


def test_dff_actual_360_one_business_day_lag_weekend_and_year_boundary():
    doc = dff_doc("2021-12-15", "2022-01-10")
    value, missing = core.dff_total_return(doc, "2021-12-30", "2022-01-04")
    assert not missing
    # Five calendar accrual days at a constant 3.60% actual/360 rate.
    assert value == pytest.approx((1.0 + 0.036 / 360.0) ** 5 - 1.0)


def test_dff_holiday_lag_and_no_lookahead():
    doc = dff_doc("2021-12-15", "2022-01-10", "0.00")
    for row in doc["rows"]:
        if row["date"] == "2021-12-30":
            row["rate_pct"] = "36.00"
    before, _ = core.dff_total_return(doc, "2021-12-29", "2022-01-02")
    through_lawful_day, _ = core.dff_total_return(doc, "2021-12-29", "2022-01-03")
    after_lawful_day, _ = core.dff_total_return(doc, "2021-12-29", "2022-01-04")
    assert before == pytest.approx(0.0)
    assert through_lawful_day == pytest.approx(before)
    assert after_lawful_day > through_lawful_day


def test_dff_missing_required_business_observation_is_unavailable():
    doc = dff_doc("2021-12-15", "2022-01-10")
    doc["rows"] = [row for row in doc["rows"] if row["date"] != "2021-12-30"]
    value, missing = core.dff_total_return(doc, "2021-12-29", "2022-01-04")
    assert value is None
    assert "2021-12-30" in missing


def test_crypto_weekend_aggregation_maps_no_future_observation_backward():
    rows = [bar("2022-01-06", 100), bar("2022-01-07", 110), bar("2022-01-08", 121), bar("2022-01-09", 133.1), bar("2022-01-10", 200)]
    schedule = core.xny_schedule("2022-01-07", "2022-01-10")
    aligned = core.align_crypto_to_xnys(document(rows), "2022-01-07", "2022-01-10", schedule)
    assert aligned[0] == ("2022-01-07", 1.0)  # Jan 6 is latest completed UTC bar at Jan 7 close.
    assert aligned[-1][1] == pytest.approx(1.331)  # Jan 7-9 weekend path maps to Jan 10.
    assert aligned[-1][1] != pytest.approx(2.0)  # Jan 10 bar completes after Jan 10 XNYS close.


def test_wrong_timezone_future_crypto_and_exchange_session_mismatch_fail_closed():
    with pytest.raises((ValueError, core.IntegrityError)):
        core.align_crypto_to_xnys(document([bar("not-a-date"), bar("2022-01-01")]), "2022-01-01", "2022-01-05", core.xny_schedule("2022-01-01", "2022-01-05"))
    assert not core.xny_schedule("2022-01-08", "2022-01-09")


def fake_source_inventory(prereg):
    stocks, crypto = [], []
    families = core.family_representations(prereg)
    for family, reps in families.items():
        for rep in reps:
            quality = {"first_observation": "2004-11-18", "last_observation": "2026-07-31", "row_count": 1,
                       "expected_row_count": 1, "duplicates": 0, "invalid_ohlc": 0, "gap_blocks": [], "missing_count": 0}
            record = {"instrument": rep, "selected_provider": "ALPACA_CRYPTO" if family == "CRYPTO" else "ALPACA_MARKET_DATA",
                      "selected_transformed_sha256": "a" * 64, "primary_quality": quality, "fallback_quality": None}
            (crypto if family == "CRYPTO" else stocks).append(record)
    return {"stock_and_etf_datasets": stocks, "crypto_datasets": crypto}


def test_complete_777_eligibility_preserves_preinception_action_conditional_and_sol_gap():
    prereg = core.load_yaml(core.PREREG_PATH)
    config = core.load_yaml(core.CONFIG_PATH)
    inventory = fake_source_inventory(prereg)
    documents = {rep: document([bar("2004-11-18"), bar("2026-07-31")]) for rep in core.representation_family(prereg)}
    # Re-inventoried SOL gap intersects the common and stress windows.
    sol = next(row for row in inventory["crypto_datasets"] if row["instrument"] == "SOL")
    sol["primary_quality"]["gap_blocks"] = [{"start": "2022-05-01", "end": "2022-05-02", "count": 2}]
    sol["primary_quality"]["missing_count"] = 2
    matrix = core.build_eligibility(prereg, config, inventory, documents, {"IAU"})
    assert matrix["registered_cell_count"] == 777
    assert len({(row["representation_id"], row["scenario_id"], row["window_id"]) for row in matrix["records"]}) == 777
    assert any(row["representation_id"] == "GEV" and row["window_id"] == "COVID_2020" and row["cell_missingness_state"] == "NOT_APPLICABLE_PRE_INCEPTION" for row in matrix["records"])
    assert any(row["representation_id"] == "SPGI" and row["window_id"] == "ASSET_AVAILABLE_HISTORY" and row["cell_missingness_state"] == "CORPORATE_ACTION_UNRESOLVED" for row in matrix["records"])
    assert all(row["cell_missingness_state"] == "CONDITIONAL_ASSET_NOT_ACQUIRED" for row in matrix["records"] if row["representation_id"] in ("SGOL", "GLDM"))
    assert any(row["representation_id"] == "SOL" and row["window_id"] == "CRYPTO_STRESS_2022" and row["cell_missingness_state"] == "KNOWN_DATA_GAP" for row in matrix["records"])


def test_trial_registry_has_exact_777_no_reserve_no_capacity_reuse():
    prereg = core.load_yaml(core.PREREG_PATH)
    config = core.load_yaml(core.CONFIG_PATH)
    inventory = fake_source_inventory(prereg)
    documents = {rep: document([bar("2004-11-18"), bar("2026-07-31")]) for rep in core.representation_family(prereg)}
    matrix = core.build_eligibility(prereg, config, inventory, documents, set())
    hashes = {rep: "b" * 64 for rep in core.representation_family(prereg)}
    registry = core.trial_registry(prereg, "c" * 64, matrix, hashes)
    assert len(registry["records"]) == 777
    assert len({row["cell_id"] for row in registry["records"]}) == 777
    assert registry["reserve_trials"] == 0
    assert registry["unused_capacity_reuse"] == "PROHIBITED"


def test_formula_chain_tamper_loo_injection_representation_conflict_unavailable_and_point_table():
    evidence = raw_study_evidence("CRYPTO")
    evidence["directions"]["LOWER"]["observations"][0]["reported_candidate"] = "999"
    with pytest.raises(authority.RuntimeAuthorityError):
        authority.evaluate_study_evidence(evidence)
    injected = raw_study_evidence("EQUITY")
    injected["equity_leave_one_out"] = []
    with pytest.raises(authority.RuntimeAuthorityError):
        authority.evaluate_study_evidence(injected)
    conflict = raw_study_evidence("CRYPTO")
    for observation in conflict["directions"]["LOWER"]["observations"]:
        if observation["representation_id"] == "SOL":
            observation["raw_operands"] = None
            observation["reported_candidate"] = None
            observation["reported_reference"] = None
            observation["missingness_state"] = "KNOWN_DATA_GAP"
    for observation in conflict["directions"]["HIGHER"]["observations"]:
        if observation["representation_id"] == "SOL":
            observation["raw_operands"] = None
            observation["reported_candidate"] = None
            observation["reported_reference"] = None
            observation["missingness_state"] = "KNOWN_DATA_GAP"
    assert authority.evaluate_study_evidence(conflict)["result"] == "unable_to_determine"
    assert len(authority.POINT_STATE_TABLE) == 16


def test_policy_boundary_has_no_target_weight_residual_cash_debt_margin_level2_optimizer_or_adoption_output():
    config = core.load_yaml(core.CONFIG_PATH)
    assert set(config["protected_scope"]) >= {"targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml", "allocate.py", "margin_state.py"}
    text = (core.ROOT / "risk_level1_runner.py").read_text(encoding="utf-8")
    prohibited_calls = ("allocate.plan(", "place_order(", "submit_order(", "optimize(")
    assert not any(value in text for value in prohibited_calls)
    assert '"no_policy_effect": True' in text
    assert '"automatic_adoption": False' in text


@pytest.mark.skipif(not core.MANIFEST_PATH.exists(), reason="data gate manifest is created by the prepare phase")
def test_manifest_rejects_missing_receipt_wrong_source_and_fallback_violation(tmp_path):
    manifest = core.load_yaml(core.MANIFEST_PATH)
    missing = copy.deepcopy(manifest)
    missing["datasets"][0]["pagination_page_receipts"] = ["missing-receipt.json"]
    missing_path = tmp_path / "missing.yaml"
    missing_path.write_text(__import__("yaml").safe_dump(missing, sort_keys=False))
    assert any("receipt missing" in error for error in manifest_validator.validate_manifest(missing_path))

    wrong = copy.deepcopy(manifest)
    wrong["datasets"][0]["provider"] = "WRONG_SOURCE"
    wrong_path = tmp_path / "wrong.yaml"
    wrong_path.write_text(__import__("yaml").safe_dump(wrong, sort_keys=False))
    assert any("outside frozen hierarchy" in error for error in manifest_validator.validate_manifest(wrong_path))

    fallback = copy.deepcopy(manifest)
    fallback_row = next(row for row in fallback["datasets"] if row["provider"] == "YAHOO_FINANCE_CHART")
    fallback_row["source_classification"] = "PRIMARY"
    fallback_path = tmp_path / "fallback.yaml"
    fallback_path.write_text(__import__("yaml").safe_dump(fallback, sort_keys=False))
    assert any("fallback order" in error for error in manifest_validator.validate_manifest(fallback_path))


GOLD_PEER_KEYS = (
    "peer_id", "identity_and_inception", "unresolved_required_session_gaps",
    "dividend_split_action_treatment", "overlap_total_return_correlation",
    "overlap_annualized_return_difference_pp", "overlap_max_drawdown_difference_pp",
)


def gold_peer_fixture(peer_id="IAU"):
    return {
        "peer_id": peer_id,
        "identity_and_inception": "COMPLETE",
        "unresolved_required_session_gaps": 0,
        "dividend_split_action_treatment": "COMPLETE",
        "overlap_total_return_correlation": "1.0000",
        "overlap_annualized_return_difference_pp": "0.0000",
        "overlap_max_drawdown_difference_pp": "0.0000",
    }


def ordered_runner_fixture():
    observation = {
        "scenario_id": "LOWER",
        "research_family": "FUND_GLD_DEFENSIVE",
        "representation_id": "GLD",
        "metric_id": "EXPOSURE_SCALED_DRAWDOWN_LOSS",
        "window_id": "ASSET_AVAILABLE_HISTORY",
        "raw_operands": {"drawdown": "-0.125"},
        "reported_candidate": "1.875",
        "reported_reference": "2.5",
        "missingness_state": "ELIGIBLE",
    }
    return {
        "study_id": "RISK-0001",
        "research_family": "FUND_GLD_DEFENSIVE",
        "gold_peer_evidence": [gold_peer_fixture()],
        "directions": {
            "LOWER": {"observations": [observation]},
            "HIGHER": {"observations": [{**observation, "scenario_id": "HIGHER"}]},
        },
    }


def mapping_orders(value):
    orders = []
    if type(value) is dict:
        orders.append(tuple(value))
        for item in value.values():
            orders.extend(mapping_orders(item))
    elif type(value) is list:
        for item in value:
            orders.extend(mapping_orders(item))
    return orders


def assert_gold_rejected(record):
    prereg = core.load_yaml(core.PREREG_PATH)
    with pytest.raises(authority.RuntimeAuthorityError):
        authority._admitted_gold_peers(prereg, [record])


def test_gold_peer_evidence_exact_schema_round_trip_and_admission_are_preserved():
    prereg = core.load_yaml(core.PREREG_PATH)
    original = {"gold_peer_evidence": [gold_peer_fixture()]}
    loaded = core.load_schema_json_bytes(core.schema_json_bytes(original))
    assert tuple(loaded["gold_peer_evidence"][0]) == GOLD_PEER_KEYS
    assert loaded == original
    assert authority._admitted_gold_peers(prereg, loaded["gold_peer_evidence"]) == ("IAU",)


def test_every_ordered_nested_runner_mapping_survives_deterministic_round_trip():
    original = ordered_runner_fixture()
    first = core.schema_json_bytes(original)
    loaded = core.load_schema_json_bytes(first)
    second = core.schema_json_bytes(loaded)
    assert first == second
    assert loaded == original
    assert mapping_orders(loaded) == mapping_orders(original)
    assert mapping_orders(loaded) == [
        ("study_id", "research_family", "gold_peer_evidence", "directions"),
        GOLD_PEER_KEYS,
        ("LOWER", "HIGHER"),
        ("observations",),
        ("scenario_id", "research_family", "representation_id", "metric_id", "window_id", "raw_operands", "reported_candidate", "reported_reference", "missingness_state"),
        ("drawdown",),
        ("observations",),
        ("scenario_id", "research_family", "representation_id", "metric_id", "window_id", "raw_operands", "reported_candidate", "reported_reference", "missingness_state"),
        ("drawdown",),
    ]


@pytest.mark.parametrize("mutation", [
    lambda value: {key: item for key, item in value.items() if key != "identity_and_inception"},
    lambda value: {**value, "inserted_key": "REJECT"},
    lambda value: {key: value[key] for key in reversed(tuple(value))},
])
def test_gold_peer_evidence_missing_extra_and_reordered_keys_fail_closed(mutation):
    assert_gold_rejected(mutation(gold_peer_fixture()))


@pytest.mark.parametrize("substitution", [None, [], "scalar", 1])
def test_gold_peer_evidence_wrong_mapping_types_fail_closed(substitution):
    prereg = core.load_yaml(core.PREREG_PATH)
    with pytest.raises(authority.RuntimeAuthorityError):
        authority._admitted_gold_peers(prereg, [substitution])


def test_nested_duplicate_key_parser_boundary_fails_closed():
    payload = b'{"outer":{"peer_id":"IAU","peer_id":"SGOL"}}\n'
    with pytest.raises(core.IntegrityError, match="duplicate JSON object key"):
        core.load_schema_json_bytes(payload)


def test_sorted_hash_serialization_reproduces_defect_and_evaluator_still_rejects():
    prereg = core.load_yaml(core.PREREG_PATH)
    payload = {"gold_peer_evidence": [gold_peer_fixture()]}
    defect = core.load_schema_json_bytes(core.canonical_json_bytes(payload))
    assert tuple(defect["gold_peer_evidence"][0]) != GOLD_PEER_KEYS
    with pytest.raises(authority.RuntimeAuthorityError, match="exact keys/order"):
        authority._admitted_gold_peers(prereg, defect["gold_peer_evidence"])


def test_schema_persistence_and_canonical_hash_paths_are_distinct_and_stable():
    left = {"z": {"b": 2, "a": 1}, "a": 3}
    right = {"a": 3, "z": {"a": 1, "b": 2}}
    assert left == right
    assert core.canonical_hash(left) == core.canonical_hash(right)
    assert core.canonical_json_bytes(left) == core.canonical_json_bytes(right)
    assert core.schema_json_bytes(left) != core.schema_json_bytes(right)
    before = core.canonical_hash(left)
    round_tripped = core.load_schema_json_bytes(core.schema_json_bytes(left))
    assert core.canonical_hash(round_tripped) == before
    assert core.schema_json_bytes(round_tripped) == core.schema_json_bytes(left)


def test_runner_and_attestation_have_no_direct_canonical_hash_serializer_persistence():
    for name in ("risk_level1_runner.py", "risk_level1_attempt2_attestation.py"):
        source = (core.ROOT / name).read_text(encoding="utf-8")
        assert "canonical_json_bytes(" not in source
        assert ".write_bytes(" not in source


def test_schema_round_trip_preserves_numeric_values_types_and_punctuation():
    value = {
        "identity": "IAU / GLD: punctuation — Ω",
        "integer": 7,
        "negative": -0.125,
        "zero": 0,
        "boolean": False,
        "nested": {"reported_candidate": "1.8750", "reported_reference": "2.5000"},
    }
    loaded = core.load_schema_json_bytes(core.schema_json_bytes(value))
    assert loaded == value
    assert {key: type(item) for key, item in loaded.items()} == {key: type(item) for key, item in value.items()}


def test_unknown_or_punctuated_gold_peer_identity_fails_closed():
    assert_gold_rejected(gold_peer_fixture("IAU!"))


def test_attempt_namespaces_are_disjoint_and_attempt_1_evidence_is_immutable():
    before = {
        path.name: core.sha256_file(path)
        for path in core.ATTEMPT_1.iterdir()
        if path.is_file()
    }
    assert core.ATTEMPT_1 != core.ATTEMPT_2
    assert core.ATTEMPT_1_FREEZE_PATH != core.ATTEMPT_2_STAGE_A_PATH
    assert not str(core.RESULTS).startswith(str(core.ATTEMPT_1))
    after = {
        path.name: core.sha256_file(path)
        for path in core.ATTEMPT_1.iterdir()
        if path.is_file()
    }
    assert after == before


def test_attempt_2_fixture_validation_creates_no_execution_marker_or_results():
    assert not runner.EXECUTION_RECEIPT.exists()
    assert not runner.RAW_EVIDENCE_PATH.exists()
    assert not runner.CELL_RESULTS_PATH.exists()
    assert not runner.DISPOSITION_PATH.exists()
    assert not core.RESULTS.exists()


def review_receipt_fixture(**overrides):
    current_head = __import__("subprocess").run(
        ["git", "rev-parse", "HEAD"], cwd=core.ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    review_id = 9999999999
    receipt = {
        "schema_version": "2.0",
        "repository": attempt2_attestation.REPOSITORY_IDENTITY,
        "pull_request_number": attempt2_attestation.IMPLEMENTATION_PR_NUMBER,
        "study_id": "RISK-0001",
        "attempt_id": core.ATTEMPT_2_ID,
        "authority_decision_id": "RISK-0002",
        "authority_decision_sha256": attempt2_attestation.RISK_0002_SHA256,
        "review_type": "MANDATORY_INDEPENDENT_PREEXECUTION_EXACT_HEAD",
        "review_reference_kind": "GITHUB_PULL_REQUEST_REVIEW",
        "review_id": review_id,
        "reviewed_head": current_head,
        "stage_a_attestation_sha256": core.sha256_file(core.FREEZE_PATH),
        "preexecution_metadata_sha256": core.sha256_file(core.ATTEMPT_2_METADATA_PATH),
        "reviewer_github_login": "independent-review-fixture",
        "reviewer_identity": "INDEPENDENT_SESSION:fixture-reviewer",
        "implementation_author_identity": attempt2_attestation.IMPLEMENTATION_AUTHOR_IDENTITY,
        "independence_basis": "DISTINCT_SESSION_IDENTITIES_BOUND_TO_DURABLE_GITHUB_REVIEW",
        "disposition": "PASS",
        "github_review_state": "COMMENTED",
        "review_url": f"https://github.com/{attempt2_attestation.REPOSITORY_IDENTITY}/pull/{attempt2_attestation.IMPLEMENTATION_PR_NUMBER}#pullrequestreview-{review_id}",
        "reviewed_at_utc": "2026-08-14T00:00:00Z",
    }
    receipt.update(overrides)
    return receipt


def test_attempt_2_prepare_and_review_gate_are_fail_closed_before_review():
    with pytest.raises(core.IntegrityError, match="prepare/reacquisition is prohibited"):
        runner.prepare()
    with pytest.raises(core.IntegrityError, match="review receipt is absent"):
        runner._verify_independent_preexecution_review()
    assert not runner.EXECUTION_RECEIPT.exists()


def test_preexecution_review_receipt_rejects_wrong_exact_head(tmp_path, monkeypatch):
    receipt_path = tmp_path / "independent_preexecution_review.json"
    core.write_schema_json(receipt_path, review_receipt_fixture(reviewed_head="0" * 40))
    monkeypatch.setattr(core, "ATTEMPT_2_REVIEW_RECEIPT_PATH", receipt_path)
    with pytest.raises(core.IntegrityError, match="current exact head"):
        runner._verify_independent_preexecution_review()


def test_runtime_freeze_gate_rejects_changed_protocol_before_execution(tmp_path, monkeypatch):
    changed_protocol = tmp_path / "PROTOCOL_V1.md"
    changed_protocol.write_bytes(core.PROTOCOL_PATH.read_bytes() + b"\nTAMPER\n")
    monkeypatch.setattr(core, "PROTOCOL_PATH", changed_protocol)
    with pytest.raises(core.IntegrityError, match="protocol"):
        runner._verify_freeze()


def test_runtime_freeze_gate_requires_preexecution_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(core, "ATTEMPT_2_METADATA_PATH", tmp_path / "absent.json")
    with pytest.raises(core.IntegrityError, match="metadata"):
        runner._verify_freeze()


def test_review_receipt_rejects_arbitrary_url_and_implementation_author(tmp_path, monkeypatch):
    receipt_path = tmp_path / "independent_preexecution_review.json"
    core.write_schema_json(receipt_path, review_receipt_fixture(
        reviewer_identity=attempt2_attestation.IMPLEMENTATION_AUTHOR_IDENTITY,
        review_url="https://example.invalid/not-pr-316",
    ))
    monkeypatch.setattr(core, "ATTEMPT_2_REVIEW_RECEIPT_PATH", receipt_path)
    with pytest.raises(core.IntegrityError, match="repository|pull request|review|independent"):
        runner._verify_independent_preexecution_review()


def test_execution_marker_transition_follows_all_pre_cell_loading():
    source = inspect.getsource(runner.execute)
    assert source.index("_load_verified_execution_inputs") < source.index("_verify_independent_preexecution_review")
    assert source.index("_verify_independent_preexecution_review") < source.index("_resolve_first_eligible_registered_cell")
    assert source.index("_resolve_first_eligible_registered_cell") < source.index("_consume_attempt_2_authorization")
    assert source.index("_consume_attempt_2_authorization") < source.index("_cell_index")


@pytest.mark.parametrize(("field", "value"), [
    ("repository", "someone/else"),
    ("pull_request_number", 315),
    ("attempt_id", core.ATTEMPT_1_ID),
    ("authority_decision_id", "RISK-0001"),
    ("authority_decision_sha256", "0" * 64),
    ("review_reference_kind", "ARBITRARY_URL"),
    ("review_id", 0),
    ("reviewed_head", "0" * 40),
    ("stage_a_attestation_sha256", "0" * 64),
    ("preexecution_metadata_sha256", "0" * 64),
    ("reviewer_identity", attempt2_attestation.IMPLEMENTATION_AUTHOR_IDENTITY),
    ("reviewer_identity", "self-asserted-reviewer"),
    ("implementation_author_identity", "wrong-author"),
    ("independence_basis", "SELF_ASSERTED_TRUE"),
    ("disposition", "CHANGES_REQUIRED"),
    ("github_review_state", "DISMISSED"),
    ("review_url", "https://example.invalid/not-a-review"),
    ("reviewed_at_utc", "not-a-timestamp"),
])
def test_preexecution_review_binding_adversarial_matrix(field, value, tmp_path, monkeypatch):
    receipt_path = tmp_path / "independent_preexecution_review.json"
    receipt = review_receipt_fixture()
    receipt[field] = value
    core.write_schema_json(receipt_path, receipt)
    monkeypatch.setattr(core, "ATTEMPT_2_REVIEW_RECEIPT_PATH", receipt_path)
    with pytest.raises(core.IntegrityError):
        runner._verify_independent_preexecution_review()
    assert not runner.EXECUTION_RECEIPT.exists()


def test_preexecution_review_missing_binding_field_fails_closed(tmp_path, monkeypatch):
    receipt_path = tmp_path / "independent_preexecution_review.json"
    receipt = review_receipt_fixture()
    del receipt["repository"]
    core.write_schema_json(receipt_path, receipt)
    monkeypatch.setattr(core, "ATTEMPT_2_REVIEW_RECEIPT_PATH", receipt_path)
    with pytest.raises(core.IntegrityError, match="exact keys/order"):
        runner._verify_independent_preexecution_review()


@pytest.mark.parametrize(("path_attribute", "label"), [
    ("PROTOCOL_PATH", "protocol"),
    ("PREREG_PATH", "preregistration"),
    ("CONFIG_PATH", "implementation_config"),
    ("ELIGIBILITY_PATH", "eligibility"),
    ("TRIAL_REGISTRY_PATH", "trial_registry"),
])
def test_runtime_gate_rejects_changed_governed_file(path_attribute, label, tmp_path, monkeypatch):
    original = getattr(core, path_attribute)
    changed = tmp_path / original.name
    changed.write_bytes(original.read_bytes() + b"\nTAMPER\n")
    monkeypatch.setattr(core, path_attribute, changed)
    with pytest.raises(core.IntegrityError, match=label.replace("_", " ") + "|" + label):
        runner._verify_freeze()
    assert not runner.EXECUTION_RECEIPT.exists()


def test_runtime_gate_rejects_changed_risk_0002_authority(tmp_path, monkeypatch):
    changed = tmp_path / "RISK-0002.md"
    changed.write_bytes(attempt2_attestation.RISK_0002_PATH.read_bytes() + b"\nTAMPER\n")
    monkeypatch.setattr(attempt2_attestation, "RISK_0002_PATH", changed)
    with pytest.raises(core.IntegrityError, match="RISK-0002 authority"):
        runner._verify_freeze()
    assert not runner.EXECUTION_RECEIPT.exists()


def _runtime_stage_contract():
    prereg, eligibility, registry = attempt2_attestation._verify_frozen_repository_inputs()
    provider = attempt2_attestation._verify_provider_identity(prereg)
    transplant = attempt2_attestation._verify_transplant_destinations()
    stage_a = core.load_schema_json(core.ATTEMPT_2_STAGE_A_PATH)
    return stage_a, prereg, eligibility, registry, provider, transplant


def _set_nested(value, path, replacement):
    target = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


@pytest.mark.parametrize(("path", "replacement"), [
    (("authority", "decision_sha256"), "0" * 64),
    (("authority_hashes", "protocol"), "0" * 64),
    (("authority_hashes", "preregistration"), "0" * 64),
    (("implementation_config_sha256",), "0" * 64),
    (("eligibility_matrix_sha256",), "0" * 64),
    (("trial_registry_sha256",), "0" * 64),
    (("forensic_identity", "material_aggregate_sha256"), "0" * 64),
    (("frozen_input_aggregates", "raw"), "0" * 64),
    (("frozen_input_aggregates", "receipts"), "0" * 64),
    (("frozen_input_aggregates", "transformed"), "0" * 64),
    (("frozen_input_aggregates", "quarantine"), "0" * 64),
    (("transplant_manifest", "sha256"), "0" * 64),
    (("calendar_sha256",), "0" * 64),
    (("provider_fallback_identity", "provider_selection_sha256"), "0" * 64),
    (("stage_a", "status"), "FAIL"),
    (("drift_confirmations", "no_provider_or_fallback_drift"), False),
    (("attempt_authorization_consumed",), True),
])
def test_runtime_stage_a_contract_rejects_tampered_identity_or_assertion(path, replacement):
    stage_a, prereg, eligibility, registry, provider, transplant = _runtime_stage_contract()
    _set_nested(stage_a, path, replacement)
    with pytest.raises(core.IntegrityError):
        attempt2_attestation._verify_runtime_stage_a(
            stage_a, prereg, eligibility, registry, provider, transplant,
        )
    assert not runner.EXECUTION_RECEIPT.exists()


def test_runtime_gate_rejects_tampered_preexecution_metadata(tmp_path, monkeypatch):
    metadata = core.load_schema_json(core.ATTEMPT_2_METADATA_PATH)
    metadata["raw_aggregate_sha256"] = "0" * 64
    path = tmp_path / "preexecution_metadata.json"
    core.write_schema_json(path, metadata)
    monkeypatch.setattr(core, "ATTEMPT_2_METADATA_PATH", path)
    with pytest.raises(core.IntegrityError, match="metadata"):
        runner._verify_freeze()
    assert not runner.EXECUTION_RECEIPT.exists()


def test_runtime_transplant_gate_rejects_changed_manifest_identity(tmp_path, monkeypatch):
    changed = tmp_path / "frozen_artifact_transplant_manifest.json"
    changed.write_bytes(core.ATTEMPT_2_TRANSPLANT_MANIFEST_PATH.read_bytes() + b"\n")
    monkeypatch.setattr(core, "ATTEMPT_2_TRANSPLANT_MANIFEST_PATH", changed)
    with pytest.raises(core.IntegrityError, match="transplant manifest identity"):
        attempt2_attestation._verify_transplant_destinations()


def test_runtime_provider_and_fallback_identity_mismatches_fail_closed(tmp_path, monkeypatch):
    prereg = core.load_yaml(core.PREREG_PATH)
    source = core.load_schema_json(core.SOURCE_INVENTORY_PATH)
    source["stock_and_etf_datasets"][0]["selected_provider"] = "WRONG_PROVIDER"
    source_path = tmp_path / "source_inventory.json"
    core.write_schema_json(source_path, source)
    monkeypatch.setattr(core, "SOURCE_INVENTORY_PATH", source_path)
    with pytest.raises(core.IntegrityError, match="provider drift"):
        attempt2_attestation._verify_provider_identity(prereg)

    monkeypatch.setattr(core, "SOURCE_INVENTORY_PATH", core.ROOT / "research/level1_sleeve_robustness/data/source_inventory.json")
    manifest = core.load_yaml(core.MANIFEST_PATH)
    manifest["provider_fallback_hierarchy"]["crypto"] = ["COINBASE_EXCHANGE", "ABSTAIN"]
    manifest_path = tmp_path / "data_manifest.yaml"
    manifest_path.write_text(__import__("yaml").safe_dump(manifest, sort_keys=False), encoding="utf-8")
    monkeypatch.setattr(core, "MANIFEST_PATH", manifest_path)
    with pytest.raises(core.IntegrityError, match="fallback hierarchy"):
        attempt2_attestation._verify_provider_identity(prereg)


def test_pre_cell_calendar_and_dff_load_failures_leave_authorization_unconsumed(tmp_path, monkeypatch):
    config = core.load_yaml(core.CONFIG_PATH)
    prereg = core.load_yaml(core.PREREG_PATH)
    eligibility = core.load_schema_json(core.ELIGIBILITY_PATH)

    fake_data = tmp_path / "data"
    calendar_path = fake_data / "transformed/XNYS_sessions.json"
    calendar_path.parent.mkdir(parents=True)
    calendar_path.write_bytes((core.DATA / "transformed/XNYS_sessions.json").read_bytes() + b"\n")
    monkeypatch.setattr(core, "DATA", fake_data)
    with pytest.raises(core.IntegrityError, match="calendar identity"):
        runner._load_verified_execution_inputs(config, prereg, eligibility)
    assert not runner.EXECUTION_RECEIPT.exists()

    monkeypatch.setattr(core, "DATA", core.ROOT / "research/level1_sleeve_robustness/data")
    source = core.load_schema_json(core.SOURCE_INVENTORY_PATH)
    source["comparator_dataset"]["selected_transformed_sha256"] = "0" * 64
    source_path = tmp_path / "source_inventory.json"
    core.write_schema_json(source_path, source)
    monkeypatch.setattr(core, "SOURCE_INVENTORY_PATH", source_path)
    with pytest.raises(core.IntegrityError, match="DFF identity"):
        runner._load_verified_execution_inputs(config, prereg, eligibility)
    assert not runner.EXECUTION_RECEIPT.exists()


def test_all_pre_cell_inputs_load_and_first_eligible_registry_resolves_without_consumption():
    config = core.load_yaml(core.CONFIG_PATH)
    prereg = core.load_yaml(core.PREREG_PATH)
    eligibility = core.load_schema_json(core.ELIGIBILITY_PATH)
    inputs = runner._load_verified_execution_inputs(config, prereg, eligibility)
    first_eligible = runner._resolve_first_eligible_registered_cell(inputs)
    assert first_eligible["preexecution_missingness_state"] == "ELIGIBLE"
    assert first_eligible is inputs["registry"]["records"][0]
    assert len(inputs["registry_lookup"]) == 777
    assert not runner.EXECUTION_RECEIPT.exists()


def test_atomic_first_cell_boundary_consumes_once_and_post_start_failure_cannot_rerun(tmp_path):
    marker = tmp_path / "results/execution_receipt.json"
    review = review_receipt_fixture()
    assert not marker.exists()
    runner._consume_attempt_2_authorization(
        "RISK-0001|FIXTURE-FIRST-ELIGIBLE-CELL", review, marker,
        started_at_utc="2026-08-14T00:00:00Z",
    )
    written = core.load_schema_json(marker)
    assert written["status"] == "FIRST_REGISTERED_ELIGIBLE_CELL_COMMENCING_NO_RERUN_PERMITTED"
    assert written["first_registered_cell_id"] == "RISK-0001|FIXTURE-FIRST-ELIGIBLE-CELL"
    with pytest.raises(core.IntegrityError, match="rerun prohibited"):
        runner._consume_attempt_2_authorization(
            "RISK-0001|FIXTURE-FIRST-ELIGIBLE-CELL", review, marker,
        )
    assert marker.exists()
    assert not runner.EXECUTION_RECEIPT.exists()
