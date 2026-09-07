"""Tests for etf_classification_validator.py (WS-0014 ETF blind-
classification schema, XASSET-0002/XASSET-0003 scope).

Every schema/behavior test below constructs its own synthetic fixture -- no
real fund's judgment content is asserted against in this file, same
authorized-scope discipline test_classification_validator.py/
test_relationship_validator.py already follow. The directory-scan tests
exercise the real repository's intelligence/etf_classification/ directory,
authored under this one implementation PR.
"""

from pathlib import Path

import pytest
import yaml

import etf_classification_validator as ev

REPO_ROOT = Path(__file__).resolve().parent


# ── fixtures ─────────────────────────────────────────────────────────────

def _structural_role(**overrides) -> dict:
    d = {"role_category": "broad_market_beta"}
    d.update(overrides)
    return d


def _constituent_exposure(**overrides) -> dict:
    d = {
        "geographic_concentration": "domestic_us",
        "sector_concentration": "broad_diversified",
        "currency_exposure": "usd_only",
    }
    d.update(overrides)
    return d


def _overlap(**overrides) -> dict:
    d = {
        "not_applicable": False,
        "measured_by_existing_mechanism": True,
        "unmeasured_flag": False,
    }
    d.update(overrides)
    return d


def _cost_and_tracking(**overrides) -> dict:
    d = {"expense_ratio_pct": 0.09, "tracking_quality_category": "not_yet_measured"}
    d.update(overrides)
    return d


def _liquidity(**overrides) -> dict:
    d = {"liquidity_tier": "high_liquidity"}
    d.update(overrides)
    return d


def _structure_and_methodology(**overrides) -> dict:
    d = {"replication_method": "physical_full_replication", "benchmark_type": "published_market_index"}
    d.update(overrides)
    return d


def _evidence_quality(**overrides) -> dict:
    d = {
        "primary_source_coverage": "partial",
        "thesis_uncertainty_statement": "Synthetic uncertainty statement.",
    }
    d.update(overrides)
    return d


def _sources() -> list:
    return [
        {
            "source_identifier": "Synthetic fund fact sheet",
            "source_type": "secondary",
            "as_of_date": "2026-08-07",
            "access_status": "consulted_via_search_aggregation",
        }
    ]


def _record(*, sealed: bool = False, instrument_id: str = "SPY", overlap_kwargs: dict | None = None, **axis_overrides) -> dict:
    overlap = axis_overrides.get("overlap_and_concentration", _overlap(**(overlap_kwargs or {})))
    structural_role = axis_overrides.get("structural_role", _structural_role())
    liquidity = axis_overrides.get("liquidity", _liquidity())
    evidence_quality = axis_overrides.get("evidence_quality", _evidence_quality())
    valuation = axis_overrides.get(
        "valuation_and_economic_assessment_readiness",
        {"status": "valuation_required", "rationale": "Synthetic rationale -- no valuation methodology exists."},
    )

    structural_risk_flags = axis_overrides.get(
        "structural_risk_flags",
        {"unmeasured_flag": overlap.get("unmeasured_flag"), "not_applicable": overlap.get("not_applicable")},
    )
    handoff = axis_overrides.get(
        "cross_asset_handoff",
        {
            "role_summary": structural_role.get("role_category"),
            "evidence_quality_summary": evidence_quality.get("primary_source_coverage"),
            "uncertainty_summary": evidence_quality.get("thesis_uncertainty_statement"),
            "liquidity_risk_summary": liquidity.get("liquidity_tier"),
            "overlap_or_correlation_signal": {
                "unmeasured_flag": overlap.get("unmeasured_flag"),
                "not_applicable": overlap.get("not_applicable"),
            },
            "valuation_readiness": valuation.get("status"),
        },
    )

    data = {
        "schema_version": "1.0",
        "instrument_id": instrument_id,
        "asset_type": "etf",
        "structural_role": structural_role,
        "constituent_exposure": axis_overrides.get("constituent_exposure", _constituent_exposure()),
        "overlap_and_concentration": overlap,
        "cost_and_tracking_quality": axis_overrides.get("cost_and_tracking_quality", _cost_and_tracking()),
        "liquidity": liquidity,
        "structure_and_methodology": axis_overrides.get("structure_and_methodology", _structure_and_methodology()),
        "evidence_quality": evidence_quality,
        "provenance": axis_overrides.get("provenance", {"sources": _sources()}),
        "uncertainty_summary": axis_overrides.get("uncertainty_summary", evidence_quality.get("thesis_uncertainty_statement")),
        "evidence_quality_status": axis_overrides.get("evidence_quality_status", evidence_quality.get("primary_source_coverage")),
        "structural_risk_flags": structural_risk_flags,
        "record_status": "draft",
        "valuation_and_economic_assessment_readiness": valuation,
        "cross_asset_handoff": handoff,
        "abstention_index": axis_overrides.get("abstention_index", []),
    }
    if sealed:
        data["record_status"] = "sealed"
        data["sealed_at"] = "2026-08-07T21:32:11Z"
        data["governing_decision"] = "XASSET-0003"
        data["drafting_session_or_shard_id"] = "shard-test"
        data["cohort_manifest_entry"] = f"intelligence/etf_classification/COHORT_MANIFEST.yaml#{instrument_id}"
        data["content_sha256"] = ev.canonical_record_hash(data)
    return data


def _gld_record(*, sealed: bool = False) -> dict:
    return _record(
        sealed=sealed,
        instrument_id="GLD",
        structural_role=_structural_role(role_category="precious_metals_or_commodity"),
        constituent_exposure=_constituent_exposure(
            geographic_concentration="not_applicable", sector_concentration="not_applicable", currency_exposure="usd_only",
        ),
        overlap_and_concentration={"not_applicable": True},
        cost_and_tracking_quality=_cost_and_tracking(expense_ratio_pct=0.40),
        structure_and_methodology=_structure_and_methodology(
            replication_method="direct_physical_commodity_holding", benchmark_type="spot_commodity_price",
        ),
    )


# ── 1-4: valid happy-path records (SPY, VEA, VWO, GLD) ─────────────────────

def test_valid_spy_record_passes():
    result = ev.validate_etf_classification_data(_record(instrument_id="SPY"))
    assert result.valid, result.errors


def test_valid_vea_record_passes():
    result = ev.validate_etf_classification_data(
        _record(
            instrument_id="VEA",
            structural_role=_structural_role(role_category="developed_ex_us_equity"),
            constituent_exposure=_constituent_exposure(geographic_concentration="developed_ex_us", currency_exposure="foreign_currency_mixed"),
        )
    )
    assert result.valid, result.errors


def test_valid_vwo_record_passes():
    result = ev.validate_etf_classification_data(
        _record(
            instrument_id="VWO",
            structural_role=_structural_role(role_category="emerging_market_equity"),
            constituent_exposure=_constituent_exposure(geographic_concentration="emerging_markets", currency_exposure="foreign_currency_mixed"),
            structure_and_methodology=_structure_and_methodology(replication_method="physical_sampling"),
        )
    )
    assert result.valid, result.errors


def test_valid_gld_record_passes():
    result = ev.validate_etf_classification_data(_gld_record())
    assert result.valid, result.errors


def test_valid_sealed_record_passes():
    result = ev.validate_etf_classification_data(_record(sealed=True))
    assert result.valid, result.errors


# ── 5-6: malformed top-level / instrument (axis-level) schema ──────────────

def test_malformed_top_level_not_a_mapping_rejected():
    result = ev.validate_etf_classification_data(["not", "a", "mapping"])
    assert not result.valid
    assert any("root document must be a mapping" in e for e in result.errors)


def test_malformed_axis_missing_required_subfield_rejected():
    record = _record(structural_role={})
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_role missing required key" in e for e in result.errors)


# ── 7-8: extra unknown key at envelope / axis level ─────────────────────────

def test_extra_unknown_key_at_envelope_level_rejected():
    record = _record()
    record["conviction_score"] = 5
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("unexpected top-level field" in e for e in result.errors) or any("forbidden key name" in e for e in result.errors)


def test_extra_unknown_key_at_axis_level_rejected():
    record = _record(structural_role=_structural_role(**{"role_category": "broad_market_beta", "extra_field": "x"}))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_role contains unexpected key" in e for e in result.errors)


# ── 9: missing required key ─────────────────────────────────────────────────

def test_missing_required_key_rejected():
    record = _record()
    del record["evidence_quality"]
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("missing required field: evidence_quality" in e for e in result.errors)


# ── 10: wrong asset type ────────────────────────────────────────────────────

def test_wrong_asset_type_rejected():
    record = _record()
    record["asset_type"] = "cryptocurrency"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("asset_type must be exactly" in e for e in result.errors)


# ── 11: crypto-field leakage ─────────────────────────────────────────────────

def test_crypto_field_leakage_rejected():
    record = _record()
    record["network_fundamentals"] = {"consensus_mechanism": "proof_of_work"}
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("crypto-classification-shaped field" in e for e in result.errors)


# ── 12: equity-field leakage ─────────────────────────────────────────────────

def test_equity_field_leakage_rejected():
    record = _record()
    record["economic_role"] = {"economic_system_ref": "AI & Compute Infrastructure"}
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("equity-classification-shaped field" in e for e in result.errors)


def test_capital_priority_leakage_rejected():
    record = _record()
    record["structural_role"]["capital_priority"] = "case_for_review"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("equity-classification-shaped field" in e for e in result.errors)


# ── 13: invalid evidence citation ───────────────────────────────────────────

def test_invalid_evidence_citation_missing_type_rejected():
    record = _record(provenance={"sources": [{"source_identifier": "x", "as_of_date": "2026-08-07", "access_status": "consulted_via_search_aggregation"}]})
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("provenance.sources[0] missing required key" in e for e in result.errors)


def test_invalid_evidence_citation_bad_source_type_rejected():
    record = _record(
        provenance={"sources": [{"source_identifier": "x", "source_type": "tertiary", "as_of_date": "2026-08-07", "access_status": "consulted_via_search_aggregation"}]}
    )
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("source_type must be one of" in e for e in result.errors)


# ── 14: invalid access-status shape ─────────────────────────────────────────

def test_invalid_access_status_rejected():
    record = _record(
        provenance={"sources": [{"source_identifier": "x", "source_type": "secondary", "as_of_date": "2026-08-07", "access_status": "read_it_myself"}]}
    )
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("access_status must be one of" in e for e in result.errors)


def test_empty_sources_list_rejected():
    record = _record(provenance={"sources": []})
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("provenance.sources must be a non-empty list" in e for e in result.errors)


# ── 15: invalid abstention ──────────────────────────────────────────────────

def test_unable_to_determine_without_abstention_reason_rejected():
    record = _record(structural_role=_structural_role(role_category="unable_to_determine"))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("abstention_reason is required" in e for e in result.errors)


def test_unable_to_determine_with_abstention_reason_accepted():
    record = _record(
        structural_role=_structural_role(role_category="unable_to_determine", abstention_reason="Evidence insufficient."),
        abstention_index=[{"axis": "structural_role", "field": "role_category", "value": "unable_to_determine", "reason": "Evidence insufficient."}],
    )
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


def test_abstention_reason_present_on_determined_record_rejected():
    record = _record(structural_role=_structural_role(role_category="broad_market_beta", abstention_reason="Should not be here."))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("must be absent unless role_category is 'unable_to_determine'" in e for e in result.errors)


# ── 16: invalid not_applicable ───────────────────────────────────────────────

def test_not_applicable_on_axis_without_that_state_rejected():
    # cost_and_tracking_quality has no not_applicable state at all -- an
    # invalid enum value for tracking_quality_category is simply rejected.
    record = _record(cost_and_tracking_quality=_cost_and_tracking(tracking_quality_category="not_applicable"))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("tracking_quality_category must be one of" in e for e in result.errors)


def test_gld_not_applicable_overlap_accepted():
    result = ev.validate_etf_classification_data(_gld_record())
    assert result.valid, result.errors


def test_overlap_not_applicable_true_with_leftover_fields_rejected():
    record = _gld_record()
    record["overlap_and_concentration"] = {"not_applicable": True, "unmeasured_flag": False}
    record["structural_risk_flags"] = {"unmeasured_flag": False, "not_applicable": True}
    record["cross_asset_handoff"]["overlap_or_correlation_signal"] = {"unmeasured_flag": False, "not_applicable": True}
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("must be absent (not merely null) when not_applicable is true" in e for e in result.errors)


# ── 17-19: duplicate / missing / extra fund in directory-level checks ──────

def test_duplicate_instrument_in_manifest_rejected():
    spy = _record(sealed=True, instrument_id="SPY")
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0003",
        "cohort": [
            {"instrument_id": "SPY", "sealed_at": spy["sealed_at"], "content_sha256": spy["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
            {"instrument_id": "SPY", "sealed_at": spy["sealed_at"], "content_sha256": spy["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
        ],
    }
    result = ev.validate_cohort_manifest(manifest, {"SPY": spy}, authorized_population=frozenset({"SPY"}))
    assert not result.valid
    assert any("lists 'SPY' more than once" in e for e in result.errors)


def test_missing_instrument_from_authorized_population_rejected():
    spy = _record(sealed=True, instrument_id="SPY")
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0003",
        "cohort": [
            {"instrument_id": "SPY", "sealed_at": spy["sealed_at"], "content_sha256": spy["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
        ],
    }
    result = ev.validate_cohort_manifest(manifest, {"SPY": spy}, authorized_population=frozenset({"SPY", "VEA"}))
    assert not result.valid
    assert any("missing authorized instrument(s): ['VEA']" in e for e in result.errors)


def test_extra_instrument_beyond_authorized_population_rejected():
    spy = _record(sealed=True, instrument_id="SPY")
    qqq = _record(sealed=True, instrument_id="QQQ")
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0003",
        "cohort": [
            {"instrument_id": "SPY", "sealed_at": spy["sealed_at"], "content_sha256": spy["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
            {"instrument_id": "QQQ", "sealed_at": qqq["sealed_at"], "content_sha256": qqq["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
        ],
    }
    result = ev.validate_cohort_manifest(manifest, {"SPY": spy, "QQQ": qqq}, authorized_population=frozenset({"SPY"}))
    assert not result.valid
    assert any("outside the authorized population: ['QQQ']" in e for e in result.errors)


# ── 20: QQQ inclusion rejected (population enforcement) ────────────────────

def test_qqq_instrument_id_rejected():
    record = _record(instrument_id="QQQ")
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("QQQ" in e and "explicitly excluded" in e for e in result.errors)


# ── 21-23: target_pct / score / rank leakage ────────────────────────────────

def test_target_pct_leakage_rejected():
    record = _record()
    record["structural_role"]["target_pct"] = 15.0
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("numeric score/rank/target-shaped field" in e for e in result.errors)


def test_score_leakage_rejected():
    record = _record()
    record["evidence_quality"]["score"] = 7
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("numeric score/rank/target-shaped field" in e for e in result.errors)


def test_rank_leakage_rejected():
    record = _record()
    record["liquidity"]["rank"] = 1
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("numeric score/rank/target-shaped field" in e for e in result.errors)


# ── 24: chart terminology leakage rejected ──────────────────────────────────

@pytest.mark.parametrize("term", list(ev._CHART_TERMS))
def test_chart_terminology_leakage_rejected(term):
    record = _record(evidence_quality=_evidence_quality(thesis_uncertainty_statement=f"This fund shows a {term} pattern."))
    record["uncertainty_summary"] = record["evidence_quality"]["thesis_uncertainty_statement"]
    record["cross_asset_handoff"]["uncertainty_summary"] = record["uncertainty_summary"]
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("chart-derived terminology" in e for e in result.errors)


# ── 25: directive-language leakage rejected ─────────────────────────────────

@pytest.mark.parametrize("word", list(ev._DIRECTIVE_WORDS))
def test_directive_language_leakage_rejected(word):
    record = _record(evidence_quality=_evidence_quality(thesis_uncertainty_statement=f"Investors should {word} this position soon."))
    record["uncertainty_summary"] = record["evidence_quality"]["thesis_uncertainty_statement"]
    record["cross_asset_handoff"]["uncertainty_summary"] = record["uncertainty_summary"]
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("directive word" in e for e in result.errors)


def test_directive_word_as_noun_holdings_not_flagged():
    record = _record(evidence_quality=_evidence_quality(thesis_uncertainty_statement="The fund's holdings are broadly diversified."))
    record["uncertainty_summary"] = record["evidence_quality"]["thesis_uncertainty_statement"]
    record["cross_asset_handoff"]["uncertainty_summary"] = record["uncertainty_summary"]
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


# ── 26: wrong valuation readiness rejected ──────────────────────────────────

def test_wrong_valuation_readiness_status_rejected():
    record = _record(valuation_and_economic_assessment_readiness={"status": "fair_value_computed", "rationale": "x"})
    record["cross_asset_handoff"]["valuation_readiness"] = "fair_value_computed"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("must be exactly 'valuation_required'" in e for e in result.errors)


# ── 27: issuer-lookthrough mismatch rejected (live recompute) ──────────────

def test_issuer_lookthrough_mismatch_rejected_for_known_carrier(tmp_path, monkeypatch):
    # SPY IS a fund carrier in the real issuer_lookthrough.yaml -- asserting
    # not_applicable=True for it must be rejected by the live recompute.
    record = _record(instrument_id="SPY", overlap_and_concentration={"not_applicable": True})
    result = ev.validate_etf_classification_data(record, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("must be false for 'SPY'" in e for e in result.errors)


def test_issuer_lookthrough_correct_for_gld_not_a_carrier():
    result = ev.validate_etf_classification_data(_gld_record(), repo_root=REPO_ROOT)
    assert result.valid, result.errors


# ── 28: GLD false constituent look-through rejected ─────────────────────────

def test_gld_false_constituent_lookthrough_rejected():
    record = _gld_record()
    record["overlap_and_concentration"] = {"not_applicable": False, "measured_by_existing_mechanism": True, "unmeasured_flag": False}
    record["structural_risk_flags"] = {"unmeasured_flag": False, "not_applicable": False}
    record["cross_asset_handoff"]["overlap_or_correlation_signal"] = {"unmeasured_flag": False, "not_applicable": False}
    result = ev.validate_etf_classification_data(record, repo_root=REPO_ROOT)
    assert not result.valid
    assert any("must be true for 'GLD'" in e for e in result.errors)


# ── 29: cross_asset_handoff projection mismatch rejected ────────────────────

def test_cross_asset_handoff_role_summary_mismatch_rejected():
    record = _record()
    record["cross_asset_handoff"]["role_summary"] = "emerging_market_equity"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("role_summary must exactly equal structural_role.role_category" in e for e in result.errors)


def test_uncertainty_summary_envelope_mismatch_rejected():
    record = _record()
    record["uncertainty_summary"] = "A different sentence entirely."
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("uncertainty_summary must exactly equal evidence_quality.thesis_uncertainty_statement" in e for e in result.errors)


def test_evidence_quality_status_mismatch_rejected():
    record = _record()
    record["evidence_quality_status"] = "comprehensive"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("evidence_quality_status must exactly equal" in e for e in result.errors)


def test_structural_risk_flags_mismatch_rejected():
    record = _record()
    record["structural_risk_flags"] = {"unmeasured_flag": True, "not_applicable": False}
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags must exactly project" in e for e in result.errors)


# ── 30-31: record hash / manifest mismatch rejected ─────────────────────────

def test_record_hash_mismatch_rejected():
    record = _record(sealed=True)
    record["content_sha256"] = "0" * 64
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("content_sha256 does not reproduce" in e for e in result.errors)


def test_manifest_hash_mismatch_rejected():
    spy = _record(sealed=True, instrument_id="SPY")
    manifest = {
        "schema_version": "1.0",
        "governing_decision": "XASSET-0003",
        "cohort": [
            {"instrument_id": "SPY", "sealed_at": spy["sealed_at"], "content_sha256": "f" * 64, "schema_version": "1.0", "governing_decision": "XASSET-0003", "record_path": "x"},
        ],
    }
    result = ev.validate_cohort_manifest(manifest, {"SPY": spy}, authorized_population=frozenset({"SPY"}))
    assert not result.valid
    assert any("content_sha256 mismatch" in e for e in result.errors)


# ── 32: deterministic generation ────────────────────────────────────────────

def test_deterministic_hash_generation():
    record = _record(sealed=True, instrument_id="SPY")
    h1 = ev.canonical_record_hash(record)
    h2 = ev.canonical_record_hash(record)
    assert h1 == h2


def test_deterministic_directory_validation():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    r1 = ev.validate_etf_classification_directory(directory, repo_root=REPO_ROOT)
    r2 = ev.validate_etf_classification_directory(directory, repo_root=REPO_ROOT)
    assert r1.valid == r2.valid
    assert [e.errors for e in r1.results] == [e.errors for e in r2.results]


# ── 33: protected-path isolation ────────────────────────────────────────────

@pytest.mark.parametrize("relative_path", [
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
    "intelligence/classification/COHORT_MANIFEST.yaml",
    "intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml",
])
def test_protected_path_untouched_by_validator_import(relative_path):
    path = REPO_ROOT / relative_path
    before = path.read_bytes() if path.exists() else None
    ev.validate_etf_classification_directory(REPO_ROOT / "intelligence" / "etf_classification", repo_root=REPO_ROOT)
    after = path.read_bytes() if path.exists() else None
    assert before == after


# ── 34: allocator/margin import-coupling check ──────────────────────────────

def test_no_allocate_or_margin_state_import():
    source = (REPO_ROOT / "etf_classification_validator.py").read_text()
    assert "import allocate" not in source
    assert "from allocate" not in source
    assert "import margin_state" not in source
    assert "from margin_state" not in source


# ── 35: legitimate expense_ratio_pct accepted ───────────────────────────────

def test_legitimate_expense_ratio_pct_accepted():
    record = _record(cost_and_tracking_quality=_cost_and_tracking(expense_ratio_pct=0.0945))
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


def test_negative_expense_ratio_pct_rejected():
    record = _record(cost_and_tracking_quality=_cost_and_tracking(expense_ratio_pct=-0.1))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("must be non-negative" in e for e in result.errors)


# ── additional coverage: missing abstention_reason on cost_and_tracking ────

def test_missing_expense_ratio_requires_abstention_reason():
    record = _record(cost_and_tracking_quality={"tracking_quality_category": "not_yet_measured"})
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("cost_and_tracking_quality.abstention_reason is required" in e for e in result.errors)


def test_missing_expense_ratio_with_abstention_reason_accepted():
    record = _record(
        cost_and_tracking_quality={
            "tracking_quality_category": "not_yet_measured",
            "abstention_reason": "Expense ratio not currently sourceable.",
        }
    )
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


# ── additional coverage: structure_and_methodology other_benchmark path ────

def test_other_benchmark_requires_benchmark_basis():
    record = _record(structure_and_methodology=_structure_and_methodology(benchmark_type="other_benchmark"))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("benchmark_basis is required" in e for e in result.errors)


def test_other_benchmark_with_basis_accepted():
    record = _record(
        structure_and_methodology=_structure_and_methodology(benchmark_type="other_benchmark", benchmark_basis="A synthetic proprietary benchmark.")
    )
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


# ── additional coverage: draft record doesn't require seal fields ──────────

def test_draft_record_without_seal_fields_valid():
    record = _record(sealed=False)
    assert "content_sha256" not in record
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


def test_sealed_record_missing_seal_fields_rejected():
    record = _record(sealed=False)
    record["record_status"] = "sealed"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("missing required seal field" in e for e in result.errors)


# ── additional coverage: overlap consistency (measured/unmeasured logical negation) ─

def test_overlap_measured_and_unmeasured_both_true_rejected():
    record = _record(overlap_and_concentration=_overlap(measured_by_existing_mechanism=True, unmeasured_flag=True))
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("logical negation" in e for e in result.errors)


# ── directory-level real-repository tests ───────────────────────────────────

def test_real_repository_etf_classification_directory_valid():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    result = ev.validate_etf_classification_directory(directory, repo_root=REPO_ROOT)
    assert result.valid, [
        (r.source, e) for r in result.results if not r.valid for e in r.errors
    ]


def test_real_repository_has_exactly_four_records():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    yaml_files = sorted(p.stem for p in directory.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml")
    assert yaml_files == ["GLD", "SPY", "VEA", "VWO"]


def test_real_repository_no_crypto_content_anywhere():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    for p in directory.glob("*.yaml"):
        text = p.read_text()
        assert "asset_type: cryptocurrency" not in text
        for forbidden in ("network_fundamentals", "economic_model", "custody_and_counterparty_risk", "correlation_and_volatility", "regulatory_and_structural_uncertainty"):
            assert forbidden not in text


def test_real_repository_no_valuation_output_anywhere():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    for p in directory.glob("*.yaml"):
        data = yaml.safe_load(p.read_text())
        if not isinstance(data, dict) or "instrument_id" not in data:
            continue
        assert data["valuation_and_economic_assessment_readiness"]["status"] == "valuation_required"


def test_real_repository_missing_directory_is_valid_zero_coverage():
    result = ev.validate_etf_classification_directory(REPO_ROOT / "intelligence" / "does_not_exist")
    assert result.valid
    assert result.record_count == 0


def test_manifest_required_when_records_exist_but_missing(tmp_path):
    (tmp_path / "SPY.yaml").write_text(yaml.safe_dump(_record(sealed=True, instrument_id="SPY")))
    result = ev.validate_etf_classification_directory(tmp_path, authorized_population=frozenset({"SPY"}))
    assert not result.valid
    assert any("COHORT_MANIFEST.yaml is required" in e for r in result.results for e in r.errors)


# ── v1.1 bounded correction: independent-review MINOR-1/MINOR-2/MINOR-3 ────

def test_missing_structural_risk_flags_rejected():
    # MINOR-1: structural_risk_flags is a required envelope field -- omitting
    # it entirely must be independently rejected, not silently pass because
    # the projection-consistency comparison no-ops on a non-dict.
    record = _record()
    del record["structural_risk_flags"]
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags must be a mapping" in e for e in result.errors)


def test_structural_risk_flags_wrong_type_rejected():
    record = _record()
    record["structural_risk_flags"] = "not-a-mapping"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags must be a mapping" in e for e in result.errors)


def test_structural_risk_flags_extra_key_rejected():
    record = _record()
    record["structural_risk_flags"] = {"unmeasured_flag": False, "not_applicable": False, "extra": 1}
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("structural_risk_flags contains unexpected key" in e for e in result.errors)


@pytest.mark.parametrize("text", [
    "The expense ratio should be increased to 0.50%.",
    "We recommend a target of 10% for this fund.",
    "See the new target pct for this instrument.",
    "This record carries a buy recommendation.",
    "This record carries a sell recommendation.",
    "This record carries a trim recommendation.",
    "This fund represents 5% of book target for the sleeve.",
])
def test_forbidden_recommendation_shaped_phrase_rejected(text):
    # MINOR-2: XASSET-0002 SS9 explicitly requires this as its own test
    # item, distinct from the directive-word and chart-term scans.
    record = _record(evidence_quality=_evidence_quality(thesis_uncertainty_statement=text))
    record["uncertainty_summary"] = text
    record["cross_asset_handoff"]["uncertainty_summary"] = text
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("forbidden recommendation-shaped phrase" in e for e in result.errors)


def test_unable_to_determine_without_matching_abstention_index_entry_rejected():
    # MINOR-3: a genuine unable_to_determine abstention must appear in
    # abstention_index -- a self-declared empty list must not pass.
    record = _record(structural_role=_structural_role(role_category="unable_to_determine", abstention_reason="Evidence insufficient."))
    record["cross_asset_handoff"]["role_summary"] = "unable_to_determine"
    result = ev.validate_etf_classification_data(record)
    assert not result.valid
    assert any("abstention_index is missing an entry for structural_role.role_category" in e for e in result.errors)


def test_unable_to_determine_with_matching_abstention_index_entry_accepted():
    record = _record(
        structural_role=_structural_role(role_category="unable_to_determine", abstention_reason="Evidence insufficient."),
        abstention_index=[{"axis": "structural_role", "field": "role_category", "value": "unable_to_determine", "reason": "Evidence insufficient."}],
    )
    record["cross_asset_handoff"]["role_summary"] = "unable_to_determine"
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


def test_not_yet_measured_does_not_require_abstention_index_entry():
    # Deliberately disclosed, not resolved: not_yet_measured is a distinct
    # vocabulary value from unable_to_determine and is not treated as an
    # abstention by this completeness check (module docstring v1.1 note).
    record = _record(cost_and_tracking_quality=_cost_and_tracking(tracking_quality_category="not_yet_measured"))
    result = ev.validate_etf_classification_data(record)
    assert result.valid, result.errors


def test_real_repository_records_pass_new_abstention_and_risk_flags_checks():
    directory = REPO_ROOT / "intelligence" / "etf_classification"
    result = ev.validate_etf_classification_directory(directory, repo_root=REPO_ROOT)
    assert result.valid, [(r.source, e) for r in result.results if not r.valid for e in r.errors]
