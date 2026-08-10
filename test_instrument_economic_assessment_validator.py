"""
test_instrument_economic_assessment_validator.py -- focused/adversarial test
suite for instrument_economic_assessment_validator.py, authored against
XASSET-0010 supporting artifact SS10's full test-item list, for the one
implementation PR authorized by XASSET-0011.

Synthetic fixtures only, except the dedicated "real corpus" test class,
which validates the six actual sealed records this same implementation PR
creates under intelligence/instrument_economic_assessment/.
"""

from __future__ import annotations

import copy
import json
from hashlib import sha256
from pathlib import Path

import pytest
import yaml

import crypto_classification_validator as _crypto
import etf_classification_validator as _etf
import instrument_economic_assessment_validator as v

REPO_ROOT = Path(__file__).resolve().parent


# ── synthetic classification-layer fixtures (for structural_reference
#    live-hash tests) -- minimal, valid records under each real schema ─────

def _minimal_etf_classification_record(instrument_id: str) -> dict:
    return {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "etf",
        "structural_role": {"role_category": "broad_market_beta"},
        "constituent_exposure": {
            "geographic_concentration": "domestic_us",
            "sector_concentration": "broad_diversified",
            "currency_exposure": "usd_only",
        },
        "overlap_and_concentration": {
            "not_applicable": False, "measured_by_existing_mechanism": True, "unmeasured_flag": False,
        },
        "cost_and_tracking_quality": {"expense_ratio_pct": 0.05, "tracking_quality_category": "not_yet_measured"},
        "liquidity": {"liquidity_tier": "high_liquidity"},
        "structure_and_methodology": {
            "replication_method": "physical_full_replication", "benchmark_type": "published_market_index",
        },
        "evidence_quality": {"primary_source_coverage": "partial", "thesis_uncertainty_statement": "x"},
        "provenance": {"sources": [{
            "source_identifier": "x", "source_type": "secondary", "as_of_date": "2026-08-10",
            "access_status": "consulted_via_search_aggregation",
        }]},
        "uncertainty_summary": "x",
        "evidence_quality_status": "partial",
        "structural_risk_flags": {"unmeasured_flag": False, "not_applicable": False},
        "record_status": "sealed",
        "valuation_and_economic_assessment_readiness": {"status": "valuation_required", "rationale": "x"},
        "cross_asset_handoff": {
            "role_summary": "broad_market_beta", "evidence_quality_summary": "partial",
            "uncertainty_summary": "x", "liquidity_risk_summary": "high_liquidity",
            "overlap_or_correlation_signal": {"unmeasured_flag": False, "not_applicable": False},
            "valuation_readiness": "valuation_required",
        },
        "abstention_index": [],
    }


def _minimal_crypto_classification_record(instrument_id: str) -> dict:
    return {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "cryptocurrency",
        "network_fundamentals": {"consensus_mechanism": "proof_of_work", "adoption_trend_category": "growing_usage"},
        "economic_model": {"supply_model": "fixed_capped_supply", "fee_accrual_applicable": False, "staking_applicable": False},
        "liquidity_and_market_structure": {"liquidity_tier": "high_liquidity", "market_structure_notes": "x"},
        "custody_and_counterparty_risk": {
            "custody_model": "exchange_custodied", "smart_contract_risk_category": "base_layer_minimal_smart_contract_surface",
        },
        "correlation_and_volatility": {"historical_volatility_category": "high_volatility", "cross_coin_correlation_status": "not_yet_measured"},
        "regulatory_and_structural_uncertainty": {"disclosed_regulatory_matter_exists": False, "structural_uncertainty_category": "disclosed_and_unresolved"},
        "evidence_quality": {"primary_source_coverage": "partial", "thesis_uncertainty_statement": "x"},
        "provenance": {"sources": [{
            "source_identifier": "x", "source_type": "secondary", "as_of_date": "2026-08-10",
            "access_status": "consulted_via_search_aggregation",
        }]},
        "uncertainty_summary": "x",
        "evidence_quality_status": "partial",
        "structural_risk_flags": {
            "custody_model": "exchange_custodied", "smart_contract_risk_category": "base_layer_minimal_smart_contract_surface",
            "cross_coin_correlation_status": "not_yet_measured",
        },
        "record_status": "sealed",
        "valuation_and_economic_assessment_readiness": {"status": "valuation_required", "rationale": "x"},
        "cross_asset_handoff": {
            "role_summary": "x", "evidence_quality_summary": "partial", "uncertainty_summary": "x",
            "liquidity_risk_summary": "high_liquidity", "overlap_or_correlation_signal": "not_yet_measured",
            "valuation_readiness": "valuation_required",
        },
        "abstention_index": [],
    }


@pytest.fixture
def classification_repo(tmp_path: Path) -> Path:
    """A tmp_path repo root with real, valid ETF/crypto classification
    records for all six instruments under the real directory layout, so
    structural_reference live-hash checks can be exercised against a
    genuine repo_root without touching the real repository files."""
    etf_dir = tmp_path / "intelligence" / "etf_classification"
    crypto_dir = tmp_path / "intelligence" / "crypto_classification"
    etf_dir.mkdir(parents=True)
    crypto_dir.mkdir(parents=True)
    for t in v.ETF_INSTRUMENTS:
        (etf_dir / f"{t}.yaml").write_text(yaml.safe_dump(_minimal_etf_classification_record(t)))
    for t in v.CRYPTO_INSTRUMENTS:
        (crypto_dir / f"{t}.yaml").write_text(yaml.safe_dump(_minimal_crypto_classification_record(t)))
    return tmp_path


def _live_hash(repo_root: Path, instrument_id: str, asset_type: str) -> str:
    sub = "etf_classification" if asset_type == "etf" else "crypto_classification"
    fn = _etf.canonical_record_hash if asset_type == "etf" else _crypto.canonical_record_hash
    data = yaml.safe_load((repo_root / "intelligence" / sub / f"{instrument_id}.yaml").read_text())
    return fn(data)


# ── synthetic instrument-economic-assessment fixtures ──────────────────────

def _valid_etf_record(repo_root: Path, instrument_id: str = "SPY") -> dict:
    ref_hash = _live_hash(repo_root, instrument_id, "etf")
    return {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "etf",
        "structural_reference": {
            "source_instrument_id": instrument_id,
            "source_schema": "etf_classification",
            "source_file": f"intelligence/etf_classification/{instrument_id}.yaml",
            "referenced_content_sha256": ref_hash,
        },
        "cost_and_tracking_quality_economic_significance": {
            "significance_category": "in_line_with_category",
            "rationale": "Sourced comparison against same-category peers found a broadly comparable cost profile.",
        },
        "evidence_quality": {"primary_source_coverage": "partial", "thesis_uncertainty_statement": "Secondary sources only."},
        "provenance": {"sources": [{
            "source_identifier": "WebSearch aggregation on peer comparison",
            "source_type": "secondary", "as_of_date": "2026-08-10",
            "access_status": "consulted_via_search_aggregation",
        }]},
        "uncertainty_summary": "Secondary sources only.",
        "evidence_quality_status": "partial",
        "record_status": "draft",
        "cross_asset_handoff": {
            "economic_characterization_summary": "in_line_with_category",
            "evidence_quality_summary": "partial",
            "uncertainty_summary": "Secondary sources only.",
        },
        "abstention_index": [],
    }


def _valid_crypto_record(repo_root: Path, instrument_id: str = "BTC") -> dict:
    ref_hash = _live_hash(repo_root, instrument_id, "cryptocurrency")
    return {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "cryptocurrency",
        "structural_reference": {
            "source_instrument_id": instrument_id,
            "source_schema": "crypto_classification",
            "source_file": f"intelligence/crypto_classification/{instrument_id}.yaml",
            "referenced_content_sha256": ref_hash,
        },
        "macro_behavioral_characterization": {
            "historical_equity_market_drawdown_behavior": {
                "behavior_category": "historically_mixed",
                "rationale": "Sourced material shows co-decline during acute macro liquidity panics.",
                "single_asset_disclosure": (
                    "This finding characterizes this coin's own single-asset historical price behavior "
                    "only. It does not compute, constitute, imply, or substitute for a whole-portfolio "
                    "diversification-benefit or correlation finding specific to Portfolio-HQ's own "
                    "current holdings; that remains the separate, still-forced-abstention job of the "
                    "overlap model's defensive_offset_interface dimension."
                ),
            },
            "historical_inflation_sensitivity_narrative": {
                "sensitivity_category": "historically_mixed_or_inconsistent",
                "rationale": "Sourced academic material is genuinely divided on this question.",
            },
        },
        "evidence_quality": {"primary_source_coverage": "partial", "thesis_uncertainty_statement": "Secondary sources only."},
        "provenance": {"sources": [{
            "source_identifier": "WebSearch aggregation on historical drawdown behavior",
            "source_type": "secondary", "as_of_date": "2026-08-10",
            "access_status": "consulted_via_search_aggregation",
        }]},
        "uncertainty_summary": "Secondary sources only.",
        "evidence_quality_status": "partial",
        "record_status": "draft",
        "cross_asset_handoff": {
            "economic_characterization_summary": {
                "historical_equity_market_drawdown_behavior": "historically_mixed",
                "historical_inflation_sensitivity_narrative": "historically_mixed_or_inconsistent",
            },
            "evidence_quality_summary": "partial",
            "uncertainty_summary": "Secondary sources only.",
        },
        "abstention_index": [],
    }


def _set_uncertainty(data: dict, text: str) -> None:
    """Update uncertainty_summary consistently across all three locations
    the schema's own read-only-projection-consistency rule requires stay
    in exact sync (envelope, evidence_quality.thesis_uncertainty_statement,
    cross_asset_handoff.uncertainty_summary) -- used by tests that only
    care about exercising a free-text scan, not the projection-consistency
    check itself."""
    data["uncertainty_summary"] = text
    data["evidence_quality"]["thesis_uncertainty_statement"] = text
    data["cross_asset_handoff"]["uncertainty_summary"] = text


def _seal(data: dict) -> dict:
    data = copy.deepcopy(data)
    data["record_status"] = "sealed"
    data["sealed_at"] = "2026-08-10T00:00:00Z"
    data["governing_decision"] = "XASSET-0011"
    data["drafting_session_or_shard_id"] = "test-shard"
    data["cohort_manifest_entry"] = f"intelligence/instrument_economic_assessment/COHORT_MANIFEST.yaml#{data['instrument_id']}"
    data["content_sha256"] = v.canonical_record_hash(data)
    return data


# ══════════════════════════════════════════════════════════════════════
# Happy path
# ══════════════════════════════════════════════════════════════════════

class TestHappyPath:
    @pytest.mark.parametrize("instrument_id", sorted(v.ETF_INSTRUMENTS))
    def test_valid_etf_record_each_instrument(self, classification_repo, instrument_id):
        data = _valid_etf_record(classification_repo, instrument_id)
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    @pytest.mark.parametrize("instrument_id", sorted(v.CRYPTO_INSTRUMENTS))
    def test_valid_crypto_record_each_instrument(self, classification_repo, instrument_id):
        data = _valid_crypto_record(classification_repo, instrument_id)
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_valid_sealed_etf_record(self, classification_repo):
        data = _seal(_valid_etf_record(classification_repo, "SPY"))
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_valid_sealed_crypto_record(self, classification_repo):
        data = _seal(_valid_crypto_record(classification_repo, "BTC"))
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Malformed / missing / extra keys at every level
# ══════════════════════════════════════════════════════════════════════

class TestSchemaShape:
    def test_missing_required_envelope_field_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        del data["uncertainty_summary"]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_top_level_key_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["extra_field"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("extra_field" in e for e in result.errors)

    def test_extra_key_in_structural_reference_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["structural_reference"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_cost_tracking_axis_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_macro_behavioral_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_drawdown_sub_field_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_inflation_sub_field_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_evidence_quality_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["evidence_quality"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_cross_asset_handoff_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cross_asset_handoff"]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_extra_key_in_provenance_source_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["provenance"]["sources"][0]["extra"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_no_deployability_summary_field_permitted(self, classification_repo):
        """AA SS4.6: this schema has no deployability_and_optionality axis,
        so cross_asset_handoff must never carry a deployability_summary
        field -- unlike the GLD/CASH_LIKE_CAPITAL schema."""
        data = _valid_etf_record(classification_repo)
        data["cross_asset_handoff"]["deployability_summary"] = "x"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid


# ══════════════════════════════════════════════════════════════════════
# Population enforcement
# ══════════════════════════════════════════════════════════════════════

class TestPopulationEnforcement:
    @pytest.mark.parametrize("bad_id", ["GLD", "CASH_LIKE_CAPITAL", "DEBT_REDUCTION", "QQQ", "TSLA", ""])
    def test_instrument_outside_population_rejected(self, classification_repo, bad_id):
        data = _valid_etf_record(classification_repo)
        data["instrument_id"] = bad_id
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_seventh_instrument_not_authorized_by_default_population(self):
        assert len(v.AUTHORIZED_POPULATION) == 6
        assert v.AUTHORIZED_POPULATION == {"SPY", "VEA", "VWO", "BTC", "ETH", "SOL"}


# ══════════════════════════════════════════════════════════════════════
# asset_type-conditional shape enforcement, both directions
# ══════════════════════════════════════════════════════════════════════

class TestAssetTypeConditionalShape:
    def test_asset_type_mismatched_against_instrument_id_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo, "SPY")
        data["asset_type"] = "cryptocurrency"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_cost_tracking_axis_present_on_crypto_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"] = {
            "significance_category": "in_line_with_category", "rationale": "x",
        }
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("forbidden" in e for e in result.errors)

    def test_cost_tracking_axis_missing_on_etf_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        del data["cost_and_tracking_quality_economic_significance"]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_macro_behavioral_present_on_etf_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["macro_behavioral_characterization"] = {
            "historical_equity_market_drawdown_behavior": {
                "behavior_category": "historically_mixed", "rationale": "x",
                "single_asset_disclosure": "This is a single-asset finding.",
            },
            "historical_inflation_sensitivity_narrative": {
                "sensitivity_category": "historically_mixed_or_inconsistent", "rationale": "x",
            },
        }
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("forbidden" in e for e in result.errors)

    def test_macro_behavioral_missing_on_crypto_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        del data["macro_behavioral_characterization"]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid


# ══════════════════════════════════════════════════════════════════════
# structural_reference -- live hash verification
# ══════════════════════════════════════════════════════════════════════

class TestStructuralReference:
    def test_correct_live_hash_accepted(self, classification_repo):
        data = _valid_etf_record(classification_repo, "VEA")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_stale_hash_rejected_etf(self, classification_repo):
        data = _valid_etf_record(classification_repo, "SPY")
        data["structural_reference"]["referenced_content_sha256"] = "0" * 64
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("stale" in e for e in result.errors)

    def test_stale_hash_rejected_crypto(self, classification_repo):
        data = _valid_crypto_record(classification_repo, "ETH")
        data["structural_reference"]["referenced_content_sha256"] = "0" * 64
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("stale" in e for e in result.errors)

    def test_wrong_source_schema_for_asset_type_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo, "SPY")
        data["structural_reference"]["source_schema"] = "crypto_classification"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_wrong_source_file_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo, "SPY")
        data["structural_reference"]["source_file"] = "intelligence/etf_classification/VEA.yaml"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_source_instrument_id_mismatch_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo, "SPY")
        data["structural_reference"]["source_instrument_id"] = "VEA"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_missing_source_file_on_disk_rejected(self, tmp_path):
        (tmp_path / "intelligence" / "etf_classification").mkdir(parents=True)
        (tmp_path / "intelligence" / "crypto_classification").mkdir(parents=True)
        data = _valid_etf_record(tmp_path, "SPY") if False else None
        # Build directly without relying on a live hash, since the file
        # genuinely does not exist in this tmp_path.
        data = {
            "schema_version": "1.0", "instrument_id": "SPY", "asset_type": "etf",
            "structural_reference": {
                "source_instrument_id": "SPY", "source_schema": "etf_classification",
                "source_file": "intelligence/etf_classification/SPY.yaml",
                "referenced_content_sha256": "a" * 64,
            },
            "cost_and_tracking_quality_economic_significance": {
                "significance_category": "in_line_with_category", "rationale": "x",
            },
            "evidence_quality": {"primary_source_coverage": "partial", "thesis_uncertainty_statement": "x"},
            "provenance": {"sources": [{
                "source_identifier": "x", "source_type": "secondary", "as_of_date": "2026-08-10",
                "access_status": "consulted_via_search_aggregation",
            }]},
            "uncertainty_summary": "x", "evidence_quality_status": "partial", "record_status": "draft",
            "cross_asset_handoff": {
                "economic_characterization_summary": "in_line_with_category",
                "evidence_quality_summary": "partial", "uncertainty_summary": "x",
            },
            "abstention_index": [],
        }
        result = v.validate_instrument_economic_assessment_data(data, repo_root=tmp_path)
        assert not result.valid
        assert any("does not exist" in e for e in result.errors)

    def test_repo_root_none_skips_live_hash_check(self, classification_repo):
        """When repo_root is None, a non-empty hash string is accepted
        without live recomputation -- used for pure schema-shape tests."""
        data = _valid_etf_record(classification_repo, "SPY")
        data["structural_reference"]["referenced_content_sha256"] = "totally-not-a-real-hash-but-non-empty"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=None)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Cross-schema field-name leakage -- one test per named group
# ══════════════════════════════════════════════════════════════════════

class TestCrossSchemaLeakage:
    @pytest.mark.parametrize("key", sorted(v._EQUITY_FIELD_LEAKAGE))
    def test_equity_field_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    @pytest.mark.parametrize("key", sorted(v._ETF_CLASSIFICATION_FIELD_LEAKAGE))
    def test_etf_classification_field_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    @pytest.mark.parametrize("key", sorted(v._CRYPTO_CLASSIFICATION_FIELD_LEAKAGE))
    def test_crypto_classification_field_leakage_rejected(self, classification_repo, key):
        data = _valid_crypto_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    @pytest.mark.parametrize("key", sorted(v._FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE))
    def test_functional_doctrine_field_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    @pytest.mark.parametrize("key", sorted(v._OVERLAP_MODEL_FIELD_LEAKAGE))
    def test_overlap_model_field_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    @pytest.mark.parametrize("key", sorted(v._ECONOMIC_ASSESSMENT_FIELD_LEAKAGE))
    def test_economic_assessment_gld_cash_field_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = "leak"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_leakage_scan_is_recursive_not_top_level_only(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cross_asset_handoff"]["nested"] = {"deeply": {"nested": {"conviction": "High"}}}
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid


# ══════════════════════════════════════════════════════════════════════
# Numeric leakage -- no carve-out of any kind
# ══════════════════════════════════════════════════════════════════════

class TestNumericLeakage:
    @pytest.mark.parametrize("key", sorted(v._NUMERIC_LEAKAGE_KEYS))
    def test_numeric_key_leakage_rejected(self, classification_repo, key):
        data = _valid_etf_record(classification_repo)
        data["provenance"][key] = 1
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_bare_numeric_percent_token_in_rationale_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["rationale"] = "Cost is 0.09% vs peers."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("numeric-percent" in e for e in result.errors)

    def test_bare_numeric_percent_token_no_carve_out_even_for_disclosed_structural_fact(self, classification_repo):
        """Unlike the ETF classification framework's own scoped
        expense_ratio_pct exception, this schema forbids restating any
        percent-shaped figure in free text under any circumstance."""
        data = _valid_etf_record(classification_repo)
        data["uncertainty_summary"] = "The expense ratio is 0.0945% by structural reference only."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_no_numeric_percent_token_is_clean(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Chart-terminology leakage
# ══════════════════════════════════════════════════════════════════════

class TestChartTerminologyLeakage:
    @pytest.mark.parametrize("term", v._CHART_TERMS)
    def test_chart_term_rejected(self, classification_repo, term):
        data = _valid_etf_record(classification_repo)
        data["uncertainty_summary"] = f"This mentions {term} somewhere in free text."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid, term


# ══════════════════════════════════════════════════════════════════════
# Directive/trading-language leakage, including a false-positive guard
# ══════════════════════════════════════════════════════════════════════

class TestDirectiveLanguageLeakage:
    @pytest.mark.parametrize("word", v._DIRECTIVE_WORDS)
    def test_directive_word_rejected(self, classification_repo, word):
        data = _valid_etf_record(classification_repo)
        data["uncertainty_summary"] = f"One should {word} this position under some framing."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid, word

    def test_holdings_noun_not_falsely_flagged_as_hold(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        _set_uncertainty(data, "This concerns the fund's own broad diversified holdings only.")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_address_not_falsely_flagged_as_add(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        _set_uncertainty(data, "This record does not address every possible peer fund.")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_exiting_not_falsely_flagged_as_exit(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        _set_uncertainty(data, "No comment is made about investors exiting or entering this fund.")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_directive_word_exempted_inside_citation_field(self, classification_repo):
        """provenance.sources[].source_identifier/.limitation are pure
        citation strings, exempted from the directive scan only -- the
        same exemption every prior validator in this repository applies."""
        data = _valid_etf_record(classification_repo)
        data["provenance"]["sources"][0]["source_identifier"] = "Article titled 'Buy and Hold Investing Explained'"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Predictive-language leakage -- scoped to the two crypto sub-fields
# ══════════════════════════════════════════════════════════════════════

class TestPredictiveLanguageLeakage:
    @pytest.mark.parametrize("term", v._PREDICTIVE_TERMS)
    def test_predictive_term_in_drawdown_rationale_rejected(self, classification_repo, term):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["rationale"] = (
            f"Analysts {term} this coin will behave similarly next time."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid, term

    @pytest.mark.parametrize("term", v._PREDICTIVE_TERMS)
    def test_predictive_term_in_inflation_rationale_rejected(self, classification_repo, term):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]["rationale"] = (
            f"Some sources {term} this trend to continue."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid, term

    def test_predictive_term_outside_scoped_fields_not_flagged_by_this_check(self, classification_repo):
        """The predictive-language scan is deliberately scoped to exactly
        the two crypto sub-fields' own free text (AA SS9 point 9) -- a
        forward-looking word in uncertainty_summary is not this check's
        job (though it may separately be caught by other scans if it
        happens to collide with them, which 'projected' does not)."""
        data = _valid_crypto_record(classification_repo)
        _set_uncertainty(data, "Figures are projected across multiple sources with some variance.")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Crypto/overlap-model non-duplication (check 10)
# ══════════════════════════════════════════════════════════════════════

class TestCryptoOverlapModelNonDuplication:
    def test_missing_single_asset_disclosure_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        del data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_empty_single_asset_disclosure_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = "   "
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_single_asset_disclosure_lacking_required_marker_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "This is a general finding about the coin's own price."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_rationale_asserting_portfolio_diversification_claim_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["rationale"] = (
            "This coin provides a genuine diversification benefit to the current portfolio."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_rationale_never_gets_negation_exception(self, classification_repo):
        """Unlike single_asset_disclosure, rationale is scanned
        unconditionally -- it is never expected to discuss the
        portfolio-level boundary at all, disclaiming or otherwise."""
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["rationale"] = (
            "This does not compute a diversification benefit to the current portfolio, historically."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_single_asset_disclosure_with_unnegated_portfolio_claim_rejected(self, classification_repo):
        """A genuine positive assertion in single_asset_disclosure, with
        no disclaiming negation anywhere in its own sentence, must still
        be rejected -- the negation exception is not a blanket exemption."""
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "This is a single-asset finding, and this coin diversifies the whole portfolio effectively."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_single_asset_disclosure_with_properly_negated_claim_accepted(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "This is a single-asset, historical finding only. It does not compute, constitute, imply, "
            "or substitute for a whole-portfolio diversification-benefit or correlation finding specific "
            "to Portfolio-HQ's own current holdings."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_cross_sentence_bypass_still_rejected(self, classification_repo):
        """A negation in one sentence must never be treated as governing
        a genuine, unnegated claim asserted in a LATER, separate
        sentence -- the disclaiming cue and the claim must share a
        sentence."""
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "This does not establish anything about the portfolio directly. "
            "Separately, this coin diversifies the whole portfolio in practice."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_ordering_reversed_claim_before_negation_in_same_sentence_still_accepted(self, classification_repo):
        """Sentence-scoped, not position-order-scoped: the disclaiming
        cue may appear anywhere in the same sentence as the claim."""
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "A whole-portfolio diversification benefit to the current portfolio is never asserted or "
            "implied here, and this finding remains separately governed by the overlap model. This is "
            "a single-asset finding only."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_declarative_deferral_phrasing_accepted(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["single_asset_disclosure"] = (
            "This is a single-asset finding only, and any portfolio-level diversification benefit "
            "remains separately governed by the overlap model's own dimension."
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Cross-coin-correlation non-leakage (check 11) -- materially independent
# mechanism from check 10 and from the general numeric scan
# ══════════════════════════════════════════════════════════════════════

class TestCrossCoinCorrelationLeakage:
    @pytest.mark.parametrize("phrase", [
        "BTC and ETH are highly correlated with each other.",
        "ETH is not correlated with SOL in any meaningful way.",
        "Bitcoin and Ethereum move in tandem during most market cycles.",
        "Solana and Bitcoin track each other closely.",
        "ETH and BTC trade in lockstep during risk-off periods.",
        "There is a correlation between BTC and Solana worth noting.",
    ])
    def test_cross_coin_correlation_claim_rejected(self, classification_repo, phrase):
        data = _valid_crypto_record(classification_repo, "BTC")
        data["uncertainty_summary"] = phrase
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid, phrase

    def test_numeric_correlation_coefficient_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo, "BTC")
        data["uncertainty_summary"] = "The correlation is approximately 0.72 in recent data."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_negative_correlation_coefficient_rejected(self, classification_repo):
        data = _valid_crypto_record(classification_repo, "BTC")
        data["uncertainty_summary"] = "Correlation of -0.31 was reported in one source."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_single_coin_only_discussion_accepted(self, classification_repo):
        """A record discussing only its own single-asset historical
        behavior against equities, with no cross-coin claim, must be
        accepted -- confirming this scan does not over-fire on ordinary,
        legitimate single-asset content."""
        data = _valid_crypto_record(classification_repo, "BTC")
        _set_uncertainty(data, "This record concerns only BTC's own historical price behavior.")
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_bare_mention_of_second_coin_without_correlation_word_accepted(self, classification_repo):
        """Merely naming another coin (e.g. for a structural contrast) is
        not itself a correlation claim -- only a correlation-shaped word
        co-occurring with two coin names triggers this check."""
        data = _valid_crypto_record(classification_repo, "BTC")
        _set_uncertainty(
            data, "Unlike Ethereum's smart-contract-heavy design, BTC's own smart-contract surface is minimal.",
        )
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_full_coin_names_also_caught_not_just_tickers(self, classification_repo):
        data = _valid_crypto_record(classification_repo, "BTC")
        data["uncertainty_summary"] = "Bitcoin's correlation with Ethereum has varied over time."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_correlation_leakage_scan_applies_to_etf_records_too(self, classification_repo):
        """Check 11 runs unconditionally on every record regardless of
        asset_type -- a stray cross-coin claim inside an ETF record
        (however implausible) must still be caught."""
        data = _valid_etf_record(classification_repo, "SPY")
        data["uncertainty_summary"] = "Unrelated note: BTC and ETH are correlated with each other."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid


# ══════════════════════════════════════════════════════════════════════
# Abstention behavior
# ══════════════════════════════════════════════════════════════════════

class TestAbstentionBehavior:
    def test_unable_to_determine_without_abstention_reason_rejected_etf_axis(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["significance_category"] = "unable_to_determine"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_unable_to_determine_with_abstention_reason_accepted_etf_axis(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["significance_category"] = "unable_to_determine"
        data["cost_and_tracking_quality_economic_significance"]["abstention_reason"] = "No peer data located."
        data["cross_asset_handoff"]["economic_characterization_summary"] = "unable_to_determine"
        data["abstention_index"] = [{
            "axis": "cost_and_tracking_quality_economic_significance", "field": "significance_category",
            "value": "unable_to_determine", "reason": "No peer data located.",
        }]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_unable_to_determine_without_abstention_reason_rejected_drawdown(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]["behavior_category"] = "unable_to_determine"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_unable_to_determine_without_abstention_reason_rejected_inflation(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]["sensitivity_category"] = "unable_to_determine"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_abstention_reason_present_but_not_abstained_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["abstention_reason"] = "Should not be here."
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_not_applicable_value_rejected_everywhere_in_this_schema(self, classification_repo):
        """This schema defines no not_applicable value anywhere in
        either axis's own closed vocabulary (AA SS6.2's own closing
        paragraph) -- a record attempting to use it must be rejected as
        an invalid enum value, not silently accepted."""
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["significance_category"] = "not_applicable"
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid

    def test_fully_abstained_crypto_record_accepted_as_sealed_eligible(self, classification_repo):
        data = _valid_crypto_record(classification_repo, "SOL")
        drawdown = data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]
        drawdown["behavior_category"] = "unable_to_determine"
        drawdown["abstention_reason"] = "No clean signal located for SOL specifically."
        inflation = data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]
        inflation["sensitivity_category"] = "unable_to_determine"
        inflation["abstention_reason"] = "No sourced narrative located."
        data["cross_asset_handoff"]["economic_characterization_summary"] = {
            "historical_equity_market_drawdown_behavior": "unable_to_determine",
            "historical_inflation_sensitivity_narrative": "unable_to_determine",
        }
        data["abstention_index"] = [
            {
                "axis": "macro_behavioral_characterization.historical_equity_market_drawdown_behavior",
                "field": "behavior_category", "value": "unable_to_determine",
                "reason": "No clean signal located for SOL specifically.",
            },
            {
                "axis": "macro_behavioral_characterization.historical_inflation_sensitivity_narrative",
                "field": "sensitivity_category", "value": "unable_to_determine",
                "reason": "No sourced narrative located.",
            },
        ]
        result = v.validate_instrument_economic_assessment_data(_seal(data), repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# abstention_index reconciliation, both directions; non-cascading
# ══════════════════════════════════════════════════════════════════════

class TestAbstentionIndexReconciliation:
    def test_missing_abstention_index_entry_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["cost_and_tracking_quality_economic_significance"]["significance_category"] = "unable_to_determine"
        data["cost_and_tracking_quality_economic_significance"]["abstention_reason"] = "x"
        # abstention_index deliberately left empty.
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("missing an entry" in e for e in result.errors)

    def test_extra_abstention_index_entry_with_no_real_abstention_rejected(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        data["abstention_index"] = [{
            "axis": "cost_and_tracking_quality_economic_significance", "field": "significance_category",
            "value": "unable_to_determine", "reason": "phantom",
        }]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert not result.valid
        assert any("does not correspond" in e for e in result.errors)

    def test_non_cascading_abstention_drawdown_only(self, classification_repo):
        """One crypto sub-field's abstention must never force or imply
        the other's."""
        data = _valid_crypto_record(classification_repo)
        drawdown = data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]
        drawdown["behavior_category"] = "unable_to_determine"
        drawdown["abstention_reason"] = "x"
        data["cross_asset_handoff"]["economic_characterization_summary"] = {
            "historical_equity_market_drawdown_behavior": "unable_to_determine",
            "historical_inflation_sensitivity_narrative": "historically_mixed_or_inconsistent",
        }
        data["abstention_index"] = [{
            "axis": "macro_behavioral_characterization.historical_equity_market_drawdown_behavior",
            "field": "behavior_category", "value": "unable_to_determine", "reason": "x",
        }]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors

    def test_non_cascading_abstention_inflation_only(self, classification_repo):
        data = _valid_crypto_record(classification_repo)
        inflation = data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]
        inflation["sensitivity_category"] = "unable_to_determine"
        inflation["abstention_reason"] = "x"
        data["cross_asset_handoff"]["economic_characterization_summary"] = {
            "historical_equity_market_drawdown_behavior": "historically_mixed",
            "historical_inflation_sensitivity_narrative": "unable_to_determine",
        }
        data["abstention_index"] = [{
            "axis": "macro_behavioral_characterization.historical_inflation_sensitivity_narrative",
            "field": "sensitivity_category", "value": "unable_to_determine", "reason": "x",
        }]
        result = v.validate_instrument_economic_assessment_data(data, repo_root=classification_repo)
        assert result.valid, result.errors


# ══════════════════════════════════════════════════════════════════════
# Manifest validation
# ══════════════════════════════════════════════════════════════════════

class TestManifestValidation:
    def _record_and_row(self, classification_repo, instrument_id, asset_type):
        record = _seal(
            _valid_etf_record(classification_repo, instrument_id) if asset_type == "etf"
            else _valid_crypto_record(classification_repo, instrument_id)
        )
        row = {
            "instrument_id": instrument_id, "asset_type": asset_type,
            "sealed_at": record["sealed_at"], "content_sha256": record["content_sha256"],
            "schema_version": "1.0", "governing_decision": "XASSET-0011",
            "record_path": f"intelligence/instrument_economic_assessment/{instrument_id}.yaml",
        }
        return record, row

    def test_valid_manifest_reconciles(self, classification_repo):
        records = {}
        rows = []
        for iid, atype in [("SPY", "etf"), ("BTC", "cryptocurrency")]:
            rec, row = self._record_and_row(classification_repo, iid, atype)
            records[iid] = rec
            rows.append(row)
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": rows}
        result = v.validate_cohort_manifest(manifest, records, authorized_population=frozenset({"SPY", "BTC"}))
        assert result.valid, result.errors

    def test_duplicate_manifest_entry_rejected(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row, row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY"}))
        assert not result.valid
        assert any("more than once" in e for e in result.errors)

    def test_missing_authorized_instrument_rejected(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY", "VEA"}))
        assert not result.valid
        assert any("missing authorized" in e for e in result.errors)

    def test_extra_instrument_outside_population_rejected(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset())
        # authorized_population=frozenset() short-circuits the missing/extra
        # check entirely (falsy) -- use a real, narrower population instead.
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"VEA"}))
        assert not result.valid
        assert any("outside the authorized" in e for e in result.errors)

    def test_orphan_sealed_record_with_no_manifest_entry_rejected(self, classification_repo):
        rec, _ = self._record_and_row(classification_repo, "SPY", "etf")
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": []}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset())
        assert not result.valid
        assert any("no corresponding cohort manifest entry" in e for e in result.errors)

    def test_hash_mismatch_between_manifest_and_recomputed_rejected(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        row["content_sha256"] = "f" * 64
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY"}))
        assert not result.valid
        assert any("mismatch" in e for e in result.errors)

    def test_asset_type_mismatch_in_manifest_row_rejected(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        row["asset_type"] = "cryptocurrency"
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY"}))
        assert not result.valid

    def test_wrong_record_path_value_rejected_even_with_matching_hash(self, classification_repo):
        """MINOR-2 (independent review, PR #297): record_path being merely
        *present* is not enough -- a row citing an entirely wrong path,
        with an otherwise-correct hash and instrument_id, must still be
        rejected. Reproduces the exact bypass the review demonstrated
        before this correction (record_path: 'totally/wrong/path/does/
        not/exist.yaml' validating clean)."""
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        row["record_path"] = "totally/wrong/path/does/not/exist.yaml"
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY"}))
        assert not result.valid
        assert any("record_path" in e for e in result.errors)

    def test_correct_record_path_value_accepted(self, classification_repo):
        rec, row = self._record_and_row(classification_repo, "SPY", "etf")
        assert row["record_path"] == "intelligence/instrument_economic_assessment/SPY.yaml"
        manifest = {"schema_version": "1.0", "governing_decision": "XASSET-0011", "cohort": [row]}
        result = v.validate_cohort_manifest(manifest, {"SPY": rec}, authorized_population=frozenset({"SPY"}))
        assert result.valid, result.errors

    def test_missing_directory_is_valid_zero_coverage_state(self, tmp_path):
        result = v.validate_instrument_economic_assessment_directory(tmp_path / "does_not_exist")
        assert result.valid
        assert result.record_count == 0


# ══════════════════════════════════════════════════════════════════════
# Determinism
# ══════════════════════════════════════════════════════════════════════

class TestDeterminism:
    def test_hash_deterministic_across_repeated_calls(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        h1 = v.canonical_record_hash(data)
        h2 = v.canonical_record_hash(data)
        assert h1 == h2

    def test_hash_changes_on_content_change(self, classification_repo):
        data = _valid_etf_record(classification_repo)
        h1 = v.canonical_record_hash(data)
        data["cost_and_tracking_quality_economic_significance"]["rationale"] = "Different text now."
        h2 = v.canonical_record_hash(data)
        assert h1 != h2

    def test_hash_unaffected_by_seal_metadata_fields(self, classification_repo):
        """Varying only the seal-metadata fields themselves (sealed_at,
        governing_decision, drafting_session_or_shard_id,
        cohort_manifest_entry) -- holding record_status and every
        substantive field fixed -- must never change the hash, since
        those four fields are excluded from the hashable key set.
        record_status itself is NOT a seal-metadata field and correctly
        does change the hash between 'draft' and 'sealed', tested
        separately below."""
        data = _valid_etf_record(classification_repo)
        data["record_status"] = "sealed"
        variant_a = copy.deepcopy(data)
        variant_a.update({
            "sealed_at": "2026-08-10T00:00:00Z", "governing_decision": "XASSET-0011",
            "drafting_session_or_shard_id": "shard-a",
            "cohort_manifest_entry": "intelligence/instrument_economic_assessment/COHORT_MANIFEST.yaml#SPY",
        })
        variant_b = copy.deepcopy(data)
        variant_b.update({
            "sealed_at": "2099-01-01T00:00:00Z", "governing_decision": "SOME-OTHER-DECISION",
            "drafting_session_or_shard_id": "shard-b-entirely-different",
            "cohort_manifest_entry": "a/totally/different/path.yaml#SPY",
        })
        assert v.canonical_record_hash(variant_a) == v.canonical_record_hash(variant_b)

    def test_hash_changes_between_draft_and_sealed_record_status(self, classification_repo):
        """record_status is an ordinary envelope field, not a seal-
        metadata field -- it correctly participates in the hash."""
        draft = _valid_etf_record(classification_repo)
        assert draft["record_status"] == "draft"
        sealed_status_only = copy.deepcopy(draft)
        sealed_status_only["record_status"] = "sealed"
        assert v.canonical_record_hash(draft) != v.canonical_record_hash(sealed_status_only)

    def test_directory_validation_deterministic(self):
        r1 = v.validate_instrument_economic_assessment_directory(REPO_ROOT / "intelligence" / "instrument_economic_assessment", repo_root=REPO_ROOT)
        r2 = v.validate_instrument_economic_assessment_directory(REPO_ROOT / "intelligence" / "instrument_economic_assessment", repo_root=REPO_ROOT)
        assert r1.valid == r2.valid
        assert [e.errors for e in r1.results] == [e.errors for e in r2.results]


# ══════════════════════════════════════════════════════════════════════
# Protected-path isolation
# ══════════════════════════════════════════════════════════════════════

class TestProtectedPathIsolation:
    @pytest.mark.parametrize("relpath", [
        "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
        "allocate.py", "margin_state.py", "levels.py",
        "intelligence/economic_assessment/GLD.yaml",
        "intelligence/economic_assessment/CASH_LIKE_CAPITAL.yaml",
        "intelligence/etf_classification/SPY.yaml",
        "intelligence/etf_classification/GLD.yaml",
        "intelligence/crypto_classification/BTC.yaml",
    ])
    def test_protected_path_unmodified_by_this_implementation(self, relpath):
        """This validator module never opens any file in write/append/
        update mode -- confirmed structurally, not merely asserted, by
        running the real validator against the real repository and then
        re-checking the target file's own bytes are unchanged."""
        target = REPO_ROOT / relpath
        assert target.is_file(), f"{relpath} should exist in the real repository"
        before = target.read_bytes()
        v.validate_instrument_economic_assessment_directory(
            REPO_ROOT / "intelligence" / "instrument_economic_assessment", repo_root=REPO_ROOT,
        )
        after = target.read_bytes()
        assert before == after


# ══════════════════════════════════════════════════════════════════════
# Allocator/margin import-coupling isolation
# ══════════════════════════════════════════════════════════════════════

class TestAllocatorMarginDecoupling:
    def test_module_does_not_import_allocate_or_margin_state(self):
        import ast

        source = (REPO_ROOT / "instrument_economic_assessment_validator.py").read_text()
        tree = ast.parse(source)
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        assert "allocate" not in imported_modules
        assert "margin_state" not in imported_modules

    def test_allocate_and_margin_state_do_not_import_this_module(self):
        for modname in ("allocate.py", "margin_state.py"):
            source = (REPO_ROOT / modname).read_text()
            assert "instrument_economic_assessment_validator" not in source

    def test_module_does_not_import_economic_assessment_validator(self):
        """This schema is permanently separate from GLD/CASH_LIKE_CAPITAL's
        own economic_assessment_validator.py (XASSET-0010 SSG) -- neither
        module imports the other."""
        import ast

        source = (REPO_ROOT / "instrument_economic_assessment_validator.py").read_text()
        tree = ast.parse(source)
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        assert "economic_assessment_validator" not in imported_modules

        ea_source = (REPO_ROOT / "economic_assessment_validator.py").read_text()
        assert "instrument_economic_assessment_validator" not in ea_source


# ══════════════════════════════════════════════════════════════════════
# Real corpus -- the six actual sealed records this implementation creates
# ══════════════════════════════════════════════════════════════════════

class TestRealCorpus:
    DIR = REPO_ROOT / "intelligence" / "instrument_economic_assessment"

    def test_directory_exists_with_exactly_six_records(self):
        assert self.DIR.is_dir()
        yaml_files = sorted(p.stem for p in self.DIR.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml")
        assert yaml_files == sorted(v.AUTHORIZED_POPULATION)

    def test_manifest_exists(self):
        assert (self.DIR / "COHORT_MANIFEST.yaml").is_file()

    def test_whole_directory_validates_clean(self):
        result = v.validate_instrument_economic_assessment_directory(self.DIR, repo_root=REPO_ROOT)
        assert result.valid, [e for r in result.results if not r.valid for e in r.errors]
        # 6 records + 1 manifest.
        assert result.record_count == 7

    @pytest.mark.parametrize("instrument_id", sorted(v.AUTHORIZED_POPULATION))
    def test_each_real_record_sealed_and_valid(self, instrument_id):
        result = v.validate_instrument_economic_assessment_file(
            self.DIR / f"{instrument_id}.yaml", repo_root=REPO_ROOT,
        )
        assert result.valid, result.errors
        data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
        assert data["record_status"] == "sealed"
        assert data["governing_decision"] == "XASSET-0011"

    def test_every_hash_reproduces(self):
        for instrument_id in sorted(v.AUTHORIZED_POPULATION):
            data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
            expected = v.canonical_record_hash(data)
            assert data["content_sha256"] == expected, instrument_id

    def test_etf_axis_only_on_etf_instruments(self):
        for instrument_id in sorted(v.ETF_INSTRUMENTS):
            data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
            assert "cost_and_tracking_quality_economic_significance" in data
            assert "macro_behavioral_characterization" not in data

    def test_crypto_axis_only_on_crypto_instruments(self):
        for instrument_id in sorted(v.CRYPTO_INSTRUMENTS):
            data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
            assert "macro_behavioral_characterization" in data
            assert "cost_and_tracking_quality_economic_significance" not in data

    def test_no_gld_cash_like_capital_debt_reduction_qqq_anywhere(self):
        for instrument_id in sorted(v.AUTHORIZED_POPULATION):
            text = (self.DIR / f"{instrument_id}.yaml").read_text()
            for forbidden in ("GLD", "CASH_LIKE_CAPITAL", "DEBT_REDUCTION", "QQQ"):
                assert forbidden not in text, f"{instrument_id} unexpectedly mentions {forbidden}"

    def test_no_cross_coin_correlation_claim_anywhere_in_real_corpus(self):
        for instrument_id in sorted(v.CRYPTO_INSTRUMENTS):
            data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
            errors = []
            v._scan_cross_coin_correlation_leakage(data, instrument_id, errors)
            assert errors == [], errors

    def test_sol_drawdown_behavior_genuinely_abstained(self):
        """SOL's own record is expected to abstain on
        historical_equity_market_drawdown_behavior specifically, given
        this implementation's own disclosed evidence confound (no 2020
        data, FTX-confounded 2022 data) -- confirming the abstention path
        was genuinely used, not merely available."""
        data = yaml.safe_load((self.DIR / "SOL.yaml").read_text())
        drawdown = data["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"]
        assert drawdown["behavior_category"] == "unable_to_determine"
        assert data["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"]["sensitivity_category"] != "unable_to_determine"

    def test_gld_and_cash_like_capital_records_untouched(self):
        """This implementation must never edit the permanently separate
        GLD/CASH_LIKE_CAPITAL economic-assessment schema (XASSET-0010
        SSG)."""
        import economic_assessment_validator as ea

        for subject in ("GLD", "CASH_LIKE_CAPITAL"):
            path = REPO_ROOT / "intelligence" / "economic_assessment" / f"{subject}.yaml"
            assert path.is_file()
            data = yaml.safe_load(path.read_text())
            assert data["content_sha256"] == ea.canonical_record_hash(data)

    def test_all_six_structural_references_reproduce_live(self):
        for instrument_id in sorted(v.AUTHORIZED_POPULATION):
            data = yaml.safe_load((self.DIR / f"{instrument_id}.yaml").read_text())
            errors: list[str] = []
            v._validate_structural_reference(
                data["structural_reference"], instrument_id=instrument_id,
                asset_type=data["asset_type"], repo_root=REPO_ROOT, errors=errors,
            )
            assert errors == [], (instrument_id, errors)
