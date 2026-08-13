"""Adversarial tests for LEVEL2-0001's closed research-cohort freeze."""

from __future__ import annotations

import copy
from pathlib import Path

import yaml

import research_cohort_freeze_validator as rcfv


REPO_ROOT = Path(__file__).resolve().parent


def _artifact() -> dict:
    return yaml.safe_load((REPO_ROOT / rcfv.ARTIFACT_PATH).read_text(encoding="utf-8"))


def _errors(data: dict) -> tuple[str, ...]:
    return rcfv.validate_data(data, repo_root=REPO_ROOT, verify_sources=True).errors


def test_real_freeze_validates():
    result = rcfv.validate_file(repo_root=REPO_ROOT)
    assert result.valid, result.errors


def test_core_is_exactly_34_unique_instruments():
    data = _artifact()
    ids = [row["instrument_id"] for row in data["core_cohort"]]
    assert len(ids) == 34
    assert len(set(ids)) == 34
    assert tuple(ids) == rcfv.CORE


def test_missing_core_identity_rejected():
    data = _artifact()
    data["core_cohort"].pop()
    assert any("exact 34 identities" in error for error in _errors(data))


def test_duplicate_core_identity_rejected():
    data = _artifact()
    data["core_cohort"][-1] = copy.deepcopy(data["core_cohort"][0])
    errors = _errors(data)
    assert any("exact 34 identities" in error for error in errors)
    assert any("duplicate" in error for error in errors)


def test_wrong_sleeve_rejected():
    data = _artifact()
    data["core_cohort"][0]["sleeve"] = "CRYPTO"
    assert any("AMZN: incorrect sleeve" in error for error in _errors(data))


def test_core_disposition_cannot_become_final_selection():
    data = _artifact()
    data["core_cohort"][0]["disposition"] = "SELECTED"
    assert any("core disposition" in error for error in _errors(data))


def test_conditional_candidate_cannot_be_promoted():
    data = _artifact()
    data["conditional_sidecar"][0]["disposition"] = "RESEARCH_COHORT_INCLUDED"
    assert any("must remain CONDITIONAL" in error for error in _errors(data))


def test_unnormalized_peer_cannot_gain_invented_ticker():
    data = _artifact()
    peer = next(row for row in data["conditional_sidecar"] if row["candidate_id"] == "SPY_PEER_VANGUARD_SP500_ETF")
    peer["normalized_instrument_id"] = "VOO"
    assert any("governed source representation" in error for error in _errors(data))


def test_qqq_cannot_enter_core():
    data = _artifact()
    data["core_cohort"][0]["instrument_id"] = "QQQ"
    errors = _errors(data)
    assert any("exact 34 identities" in error for error in errors)
    assert any("QQQ/CASH/RESERVE" in error for error in errors)


def test_cash_cannot_enter_core():
    data = _artifact()
    data["core_cohort"][0]["instrument_id"] = "CASH"
    assert any("QQQ/CASH/RESERVE" in error for error in _errors(data))


def test_spgi_no_policy_conclusion_must_be_preserved():
    data = _artifact()
    row = next(row for row in data["core_cohort"] if row["instrument_id"] == "SPGI")
    row["caveat_codes"].remove("SPGI_NO_POLICY_CONCLUSION_PRESERVED")
    assert any("SPGI must preserve" in error for error in _errors(data))


def test_sol_drawdown_abstention_must_be_preserved():
    data = _artifact()
    row = next(row for row in data["core_cohort"] if row["instrument_id"] == "SOL")
    row["caveat_codes"].remove("SOL_DRAWDOWN_EVIDENCE_ABSTENTION")
    assert any("SOL must preserve" in error for error in _errors(data))


def test_crypto_internal_weighting_assumption_rejected_by_missing_caveat():
    data = _artifact()
    row = next(row for row in data["core_cohort"] if row["instrument_id"] == "BTC")
    row["caveat_codes"].remove("INTERNAL_WEIGHTING_METHOD_UNRESOLVED")
    assert any("internal weighting" in error for error in _errors(data))


def test_legacy_gap_cannot_be_silently_omitted():
    data = _artifact()
    data["abstained_population"].pop("legacy_population")
    errors = _errors(data)
    assert any("abstained_population keys mismatch" in error for error in errors)
    assert any("approximately-41" in error for error in errors)


def test_named_abstention_reason_must_reconcile_to_registry():
    data = _artifact()
    data["abstained_population"]["named_instruments"][0]["source_registry_disposition"] = "evaluation_ready"
    assert any("AAPL: abstention reason/source disposition mismatch" in error for error in _errors(data))


def test_exclusion_is_current_freeze_scoped():
    data = _artifact()
    data["excluded_population"][0]["disposition"] = "PERMANENTLY_EXCLUDED"
    assert any("current-freeze exclusion envelope mismatch" in error for error in _errors(data))


def test_source_hash_tampering_rejected():
    data = _artifact()
    data["source_pins"][0]["sha256"] = "0" * 64
    errors = _errors(data)
    assert any("source path/hash pin mismatch" in error for error in errors)
    assert any("live source hash does not reconcile" in error for error in errors)


def test_source_pin_omission_rejected():
    data = _artifact()
    data["source_pins"].pop()
    assert any("exact canonical pin set" in error for error in _errors(data))


def test_numeric_weight_field_rejected_structurally():
    data = _artifact()
    data["core_cohort"][0]["target_weight"] = 1
    errors = _errors(data)
    assert any("keys mismatch" in error for error in errors)
    assert any("prohibited sizing/ranking key" in error for error in errors)


def test_level2_sizing_percentage_field_rejected_structurally():
    data = _artifact()
    data["conditional_sidecar"][0]["provisional_pct"] = "1.00"
    errors = _errors(data)
    assert any("keys mismatch" in error for error in errors)
    assert any("prohibited sizing/ranking key" in error for error in errors)


def test_rank_and_score_fields_rejected_structurally():
    data = _artifact()
    data["core_cohort"][0]["rank"] = 1
    data["core_cohort"][0]["score"] = 1
    errors = _errors(data)
    assert sum("prohibited sizing/ranking key" in error for error in errors) >= 2


def test_percentage_shaped_string_rejected():
    data = _artifact()
    data["conditional_sidecar"][5]["source_label"] = "10% allocation"
    assert any("percentage-shaped strings" in error for error in _errors(data))


def test_float_value_rejected():
    data = _artifact()
    data["cohort_summary"]["core_total"] = 34.0
    assert any("floating-point values are prohibited" in error for error in _errors(data))


def test_final_membership_authority_cannot_be_enabled():
    data = _artifact()
    data["authority_boundary"]["final_portfolio_membership"] = "ESTABLISHED"
    assert any("non-authorization boundary" in error for error in _errors(data))


def test_backtest_cannot_be_automatically_authorized():
    data = _artifact()
    data["authority_boundary"]["backtest_authority"] = "AUTHORIZED"
    assert any("non-authorization boundary" in error for error in _errors(data))


def test_refreeze_trigger_cannot_be_removed():
    data = _artifact()
    data["refreeze_triggers"].remove("PINNED_SOURCE_HASH_CHANGE")
    assert any("refreeze_triggers must equal" in error for error in _errors(data))


def test_registry_is_fully_partitioned_without_overlap():
    data = _artifact()
    data["abstained_population"]["named_instruments"][0]["instrument_id"] = "AMZN"
    assert any("population overlap" in error for error in _errors(data))


def test_cli_validator_succeeds():
    assert rcfv.main() == 0
