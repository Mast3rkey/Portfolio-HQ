"""Tests for valuation_result_validator.py (WS-0015 VALUATION-0006 Stage-4
valuation-result scaffold: schema + validator only).

Every fixture in this file is entirely fictional -- tickers like "ZZFAKE1",
"ZZFAKE2" name no real company, and every figure (valuation ranges,
discount-rate/terminal-growth assumptions, peer identities, scenario
variables/probabilities) is invented for test purposes only. This file
asserts against no real company's actual valuation output, matching the
synthetic-fixture-only discipline every prior validator test suite in this
repository already follows.

No `intelligence/valuation_results/` directory exists anywhere in this
repository at this implementation's own head -- VALUATION-0006 SS A/SS S
authorizes zero real-company population, so every directory-scan test below
either (a) confirms the real, non-existent repository directory validates
as a valid, zero-coverage state, or (b) exercises a `tmp_path`-scoped
synthetic directory that is never committed.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

import valuation_archetype_validator as vav
import valuation_evidence_validator as vev
import valuation_result_validator as vrv

REPO_ROOT = Path(__file__).resolve().parent


# ── archetype fixture builder ────────────────────────────────────────────

def _archetype(*, ticker: str = "ZZFAKE1", primary: str = "A", secondary: str | None = None, **overrides) -> dict:
    rationale = overrides.pop(
        "rationale",
        "Fictional test rationale for automated test purposes only, describing invented "
        "business-economics characteristics.",
    )
    if secondary is not None and "archetype-f test:" not in rationale.lower():
        rationale += " Archetype-F test: F was considered but not selected for fictional reasons."
    gap = overrides.pop(
        "evidence_gap_statement",
        "Fictional evidence gap statement." if primary == "unable_to_determine_archetype" else None,
    )
    d = {
        "schema_version": "1.0",
        "ticker": ticker,
        "primary_archetype": primary,
        "secondary_archetype": secondary,
        "rationale": rationale,
        "evidence_quality": {
            "primary_source_coverage": "comprehensive",
            "uncertainty_statement": "Fictional uncertainty statement for automated testing.",
        },
        "disclosed_evidence_conflicts": None,
        "evidence_gap_statement": gap,
        "portfolio_context": None,
        "lifecycle_status": "sealed",
        "sealed_at": "2026-08-09T00:00:00Z",
        "governing_decision": "VALUATION-0003",
        "drafting_session_or_shard_id": "test-shard",
        "cohort_manifest_entry": f"intelligence/valuation_archetype/COHORT_MANIFEST.yaml#{ticker}",
    }
    d.update(overrides)
    d["content_sha256"] = vav.canonical_record_hash(d)
    return d


# ── evidence fixture builders (subset of test_valuation_evidence_
# validator.py's own pattern, reproduced locally so this test file stays
# self-contained) ────────────────────────────────────────────────────────

def _source(**overrides) -> dict:
    d = {
        "source_identifier": "Synthetic fictional source",
        "source_type": "secondary",
        "as_of_date": "2026-08-09",
        "access_status": "consulted_via_search_aggregation",
    }
    d.update(overrides)
    return d


def _provenance(*sources, **overrides) -> dict:
    return {"sources": list(sources) or [_source(**overrides)]}


def _line_item(**overrides) -> dict:
    d = {
        "item_category": "revenue", "value": 100.0, "unit": "usd_millions",
        "value_basis": "reported", "provenance": _provenance(),
    }
    d.update(overrides)
    return d


def _period(**overrides) -> dict:
    d = {
        "period_type": "annual", "fiscal_period_end_date": "2025-01-01", "as_of_date": "2026-08-09",
        "restated": False, "line_items": [_line_item()],
    }
    d.update(overrides)
    return d


def _financial_evidence(**overrides) -> dict:
    d = {"periods": [_period()]}
    d.update(overrides)
    return d


def _segment_evidence_abstained(reason: str = "No segment data disclosed.") -> dict:
    return {"segments": [], "abstention_reason": reason}


def _market_observed_evidence_abstained(reason: str = "No market-observed input available.") -> dict:
    return {"inputs": [], "abstention_reason": reason}


def _discount_component(**overrides) -> dict:
    d = {"value": 0.045, "provenance_label": "market_derived", "provenance": _provenance()}
    d.update(overrides)
    return d


def _discount_rate_evidence(**overrides) -> dict:
    d = {
        "risk_free_rate": _discount_component(),
        "cost_of_debt": _discount_component(value=0.055),
        "tax_rate": _discount_component(value=0.21, tax_rate_type="effective"),
        "capital_structure": {
            "debt_weight": 0.3, "equity_weight": 0.7,
            "provenance_label": "historically_observed", "provenance": _provenance(),
        },
        "beta_observation": _discount_component(value=1.1),
    }
    d.update(overrides)
    return d


def _discount_rate_evidence_abstained(reason: str = "No discount-rate evidence sourced.") -> dict:
    return {"abstention_reason": reason}


def _peer_candidate(**overrides) -> dict:
    d = {
        "identity": "FAKEPEER1", "comparability_rationale": "Synthetic comparable for testing.",
        "provenance": _provenance(), "as_of_date": "2026-08-09",
        "inclusion_status": "included", "inclusion_rationale": "Fictional inclusion rationale.",
    }
    d.update(overrides)
    return d


def _peer_set_evidence(candidates: list[dict] | None = None, **overrides) -> dict:
    if candidates is None:
        candidates = [
            _peer_candidate(identity="FAKEPEER1"),
            _peer_candidate(identity="FAKEPEER2"),
        ]
    d = {"candidates": candidates}
    d.update(overrides)
    return d


def _peer_set_evidence_abstained(reason: str = "No valid peer set could be identified.") -> dict:
    return {"candidates": [], "abstention_reason": reason}


def _scenario_variable(**overrides) -> dict:
    d = {
        "variable_name": "fictional_growth_rate", "evidence_basis": "Synthetic evidence basis.",
        "provenance_label": "assumed_for_illustration",
    }
    d.update(overrides)
    return d


def _scenario_entry(**overrides) -> dict:
    d = {"scenario_name": "Fictional upside case", "variables": [_scenario_variable()]}
    d.update(overrides)
    return d


def _scenario_evidence(scenarios: list[dict] | None = None, **overrides) -> dict:
    if scenarios is None:
        scenarios = [
            _scenario_entry(scenario_name="Fictional upside case"),
            _scenario_entry(scenario_name="Fictional downside case"),
        ]
    d = {"scenarios": scenarios}
    d.update(overrides)
    return d


def _scenario_evidence_abstained(reason: str = "Unable to determine a defensible scenario set.") -> dict:
    return {"scenarios": [], "abstention_reason": reason}


def _freshness_state() -> dict:
    return {
        "most_recent_evidence_date": "2026-08-09", "review_cadence_days": 90,
        "next_review_due_date": "2026-11-07", "stale": False,
    }


def _evidence(*, ticker: str = "ZZFAKE1", **overrides) -> dict:
    """Fully-populated-by-default evidence record (discount rate, peer
    candidates, and scenarios all populated) -- individual tests abstain
    specific domains via overrides to exercise the bearing-domain/conflict-
    propagation and family_status: completed vs. partial paths."""
    financial = overrides.pop("financial_evidence", _financial_evidence())
    segment = overrides.pop("segment_evidence", _segment_evidence_abstained())
    market = overrides.pop("market_observed_evidence", _market_observed_evidence_abstained())
    discount = overrides.pop("discount_rate_evidence", _discount_rate_evidence())
    peers = overrides.pop("peer_set_evidence", _peer_set_evidence())
    scenarios = overrides.pop("scenario_evidence", _scenario_evidence())

    abstention_index = overrides.pop("abstention_index", None)
    if abstention_index is None:
        abstention_index = []
        if not financial.get("periods") and financial.get("abstention_reason"):
            abstention_index.append({"domain": "financial_evidence", "reason": financial["abstention_reason"]})
        if not segment.get("segments") and segment.get("abstention_reason"):
            abstention_index.append({"domain": "segment_evidence", "reason": segment["abstention_reason"]})
        if not market.get("inputs") and market.get("abstention_reason"):
            abstention_index.append({"domain": "market_observed_evidence", "reason": market["abstention_reason"]})
        if discount.get("abstention_reason"):
            abstention_index.append({"domain": "discount_rate_evidence", "reason": discount["abstention_reason"]})
        if not peers.get("candidates") and peers.get("abstention_reason"):
            abstention_index.append({"domain": "peer_set_evidence", "reason": peers["abstention_reason"]})
        if not scenarios.get("scenarios") and scenarios.get("abstention_reason"):
            abstention_index.append({"domain": "scenario_evidence", "reason": scenarios["abstention_reason"]})

    data = {
        "schema_version": "1.0", "ticker": ticker, "asset_class": "equity",
        "financial_evidence": financial, "segment_evidence": segment,
        "market_observed_evidence": market, "discount_rate_evidence": discount,
        "peer_set_evidence": peers, "scenario_evidence": scenarios,
        "uncertainty_summary": "Synthetic overall uncertainty statement.",
        "abstention_index": abstention_index,
        "freshness_state": overrides.pop("freshness_state", _freshness_state()),
        "record_status": "sealed",
    }
    data.update(overrides)
    data.setdefault("sealed_at", "2026-08-09T00:00:00Z")
    data.setdefault("governing_decision", "VALUATION-0005")
    data.setdefault("drafting_session_or_shard_id", "test-shard")
    data.setdefault("cohort_manifest_entry", ticker)
    data["content_sha256"] = vev.canonical_record_hash(data)
    return data


def evidence_domain_names_bearing(evidence: dict) -> set[str]:
    """Test-side mirror of the module's own live-recompute -- which
    domains carry a domain-level abstention_reason."""
    return {
        d for d in vrv._EVIDENCE_DOMAIN_NAMES
        if isinstance(evidence.get(d), dict) and evidence[d].get("abstention_reason")
    }


# ── result fixture builders ──────────────────────────────────────────────

def _assumption(**overrides) -> dict:
    d = {
        "assumption_name": "peer_multiple", "value": 15.0,
        "provenance_label": "market_derived", "source_or_derivation_note": "Synthetic derivation note.",
    }
    d.update(overrides)
    return d


def _range(**overrides) -> dict:
    d = {
        "low": 10.0, "base": 15.0, "high": 20.0,
        "unit_and_basis": "USD per diluted share, equity value",
        "governing_sensitivity": "Fictional governing sensitivity.",
    }
    d.update(overrides)
    return d


def _scenario_outcome(**overrides) -> dict:
    d = {"scenario_name": "Fictional upside case", "value": 20.0}
    d.update(overrides)
    return d


def _scenario_range(outcomes: list[dict] | None = None, *, exhaustive: bool = True, **overrides) -> dict:
    if outcomes is None:
        outcomes = [
            _scenario_outcome(scenario_name="Fictional upside case", value=25.0, probability_weight=0.5, probability_weight_provenance_label="assumed_for_illustration"),
            _scenario_outcome(scenario_name="Fictional downside case", value=8.0, probability_weight=0.5, probability_weight_provenance_label="assumed_for_illustration"),
        ]
    d = {
        "scenario_outcomes": outcomes,
        "unit_and_basis": "USD per diluted share, equity value",
        "governing_sensitivity": "Fictional scenario probability weighting.",
        "scenario_set_is_exhaustive": exhaustive,
    }
    d.update(overrides)
    return d


def _family_entry(**overrides) -> dict:
    d = {
        "family_id": "family_5_relative_valuation",
        "governed_role": "primary_candidate",
        "family_status": "completed",
        "valuation_range": _range(),
        "assumptions_ledger": [_assumption()],
        "applied_peers": ["FAKEPEER1", "FAKEPEER2"],
    }
    d.update(overrides)
    return d


def _cross_asset_handoff(families: list[dict], *, ticker: str, asset_class: str, result_status: str, eqs: dict) -> dict:
    return {
        "ticker": ticker, "asset_class": asset_class, "result_status": result_status,
        "family_summary": [
            {"family_id": f["family_id"], "governed_role": f["governed_role"], "family_status": f["family_status"]}
            for f in families
        ],
        "evidence_quality_summary_echo": eqs,
    }


def _evidence_quality_summary(evidence: dict) -> dict:
    return {
        "access_status_values_present": sorted(vrv._true_access_status_values(evidence)),
        "domain_abstentions_echoed": sorted(vrv._true_domain_abstentions(evidence)),
    }


def _result(
    *, archetype: dict, evidence: dict, families: list[dict] | None = None,
    result_status: str = "completed", abstention_reason: str | None = None,
    conflicts: list[dict] | None = None, **overrides,
) -> dict:
    ticker = archetype["ticker"]
    if families is None:
        families = [_family_entry()]
    eqs = overrides.pop("evidence_quality_summary", None)
    if eqs is None:
        eqs = _evidence_quality_summary(evidence)
    if conflicts is None:
        conflicts = []
        for dom in evidence_domain_names_bearing(evidence):
            conflicts.append({"domain": dom, "pointer_type": "domain_abstention", "pointer_note": f"Evidence abstained on {dom}."})

    data = {
        "schema_version": "1.0", "ticker": ticker, "asset_class": "equity",
        "governing_decisions": ["VALUATION-0006"],
        "archetype_reference": {
            "source_file": f"intelligence/valuation_archetype/{ticker}.yaml",
            "content_sha256": archetype["content_sha256"],
        },
        "evidence_reference": {
            "source_file": f"intelligence/valuation_evidence/{ticker}.yaml",
            "content_sha256": evidence["content_sha256"],
        },
        "as_of_date": "2026-08-09",
        "methodology_families_applied": families,
        "sensitivity_disclosure": "Fictional sensitivity disclosure for automated testing.",
        "uncertainty_summary": "Fictional overall uncertainty summary for automated testing.",
        "evidence_quality_summary": eqs,
        "conflicts_carried_forward": conflicts,
        "result_status": result_status,
        "abstention_reason": abstention_reason,
        "record_status": "sealed",
    }
    data["cross_asset_handoff"] = overrides.pop(
        "cross_asset_handoff",
        _cross_asset_handoff(families, ticker=ticker, asset_class="equity", result_status=result_status, eqs=eqs),
    )
    data.update(overrides)
    data.setdefault("sealed_at", "2026-08-09T00:00:00Z")
    data.setdefault("governing_decision", "VALUATION-0006")
    data.setdefault("drafting_session_or_shard_id", "test-shard")
    data.setdefault("cohort_manifest_entry", f"intelligence/valuation_results/COHORT_MANIFEST.yaml#{ticker}")
    data["content_sha256"] = vrv.canonical_record_hash(data)
    return data


def assert_valid(result: vrv.ValidationResult) -> None:
    assert result.valid, f"expected valid, got errors: {result.errors}"


def assert_invalid(result: vrv.ValidationResult, *, contains: str | None = None) -> None:
    assert not result.valid
    if contains:
        assert any(contains in e for e in result.errors), result.errors


def _validate(result_data: dict, archetype: dict, evidence: dict) -> vrv.ValidationResult:
    return vrv.validate_result_data(result_data, archetype_data=archetype, evidence_data=evidence)


def _reseal(data: dict) -> dict:
    data["content_sha256"] = vrv.canonical_record_hash(data)
    return data


# ═══════════════════════════════════════════════════════════════════════
# 1-6: valid records across every shape
# ═══════════════════════════════════════════════════════════════════════

class TestValidRecords:
    def test_valid_completed_dcf_style_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1")  # discount_rate_evidence populated by default
        families = [_family_entry(
            family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="completed",
            valuation_range=_range(governing_sensitivity="terminal growth rate"),
            assumptions_ledger=[
                _assumption(assumption_name="terminal_growth", value=0.02, provenance_label="assumed_for_illustration"),
                _assumption(assumption_name="applicable_discount_rate", value=0.09, provenance_label="market_derived"),
            ],
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        assert_valid(_validate(res, arch, evid))

    def test_valid_sotp_style_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="F")
        evid = _evidence(ticker="ZZFAKE1", segment_evidence={"segments": [
            {"segment_name": "Fictional Segment A", "revenue": _line_item(value=500.0)},
            {"segment_name": "Fictional Segment B", "revenue": _line_item(value=300.0)},
        ]})
        families = [_family_entry(
            family_id="family_1_asset_based_sotp", governed_role="primary_candidate", family_status="completed",
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        assert_valid(_validate(res, arch, evid))

    def test_valid_relative_valuation_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="B")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid, result_status="completed")
        assert_valid(_validate(res, arch, evid))

    def test_valid_scenario_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="D")
        evid = _evidence(ticker="ZZFAKE1")
        families = [_family_entry(
            family_id="family_7_scenario_probability_weighted", governed_role="primary_candidate",
            family_status="completed", valuation_range=_scenario_range(),
            assumptions_ledger=[_assumption(assumption_name="fictional_growth_rate", value=0.1)],
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        assert_valid(_validate(res, arch, evid))

    def test_valid_partial_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=_discount_rate_evidence_abstained())
        families = [_family_entry(
            family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="partial",
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial",
                       abstention_reason="Discount-rate evidence unavailable for this fictional entity.")
        assert_valid(_validate(res, arch, evid))

    def test_valid_unable_to_determine_result(self):
        arch = _archetype(ticker="ZZFAKE1", primary="unable_to_determine_archetype")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid, families=[], result_status="unable_to_determine",
                       abstention_reason="Pinned archetype record itself abstained.", conflicts=[])
        assert_valid(_validate(res, arch, evid))


# ═══════════════════════════════════════════════════════════════════════
# 7-11: schema failures
# ═══════════════════════════════════════════════════════════════════════

class TestSchemaFailures:
    def test_missing_required_envelope_field(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["as_of_date"]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="as_of_date")

    def test_unknown_envelope_key(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["fair_value_estimate"] = 42.0
        _reseal(res)
        assert_invalid(_validate(res, arch, evid))

    @pytest.mark.parametrize("path,key", [
        ("methodology_families_applied[0]", "invalid_key"),
        ("methodology_families_applied[0].valuation_range", "invalid_key"),
        ("archetype_reference", "invalid_key"),
        ("evidence_reference", "invalid_key"),
        ("evidence_quality_summary", "invalid_key"),
        ("cross_asset_handoff", "invalid_key"),
    ])
    def test_unknown_key_at_each_nested_level(self, path, key):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        if path == "methodology_families_applied[0]":
            res["methodology_families_applied"][0][key] = "x"
        elif path == "methodology_families_applied[0].valuation_range":
            res["methodology_families_applied"][0]["valuation_range"][key] = "x"
        elif path == "archetype_reference":
            res["archetype_reference"][key] = "x"
        elif path == "evidence_reference":
            res["evidence_reference"][key] = "x"
        elif path == "evidence_quality_summary":
            res["evidence_quality_summary"][key] = "x"
        elif path == "cross_asset_handoff":
            res["cross_asset_handoff"][key] = "x"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid))

    def test_unknown_key_in_assumptions_ledger_entry(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["assumptions_ledger"][0]["extra"] = "x"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid))

    def test_unknown_key_in_conflicts_carried_forward_entry(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=_discount_rate_evidence_abstained())
        families = [_family_entry(family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="partial", applied_peers=None)]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial", abstention_reason="x")
        res["conflicts_carried_forward"][0]["extra"] = "x"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid))

    def test_invalid_result_status(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["result_status"] = "not_a_real_status"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="result_status")

    def test_invalid_record_status(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["record_status"] = "not_a_real_status"
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid), contains="record_status")


# ═══════════════════════════════════════════════════════════════════════
# 12-15: range-not-point
# ═══════════════════════════════════════════════════════════════════════

class TestRangeNotPoint:
    def test_point_only_valuation_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["valuation_range"] = {
            "low": 15.0, "unit_and_basis": "USD per share", "governing_sensitivity": "x",
        }
        _reseal(res)
        r = _validate(res, arch, evid)
        assert_invalid(r, contains="single point is never a valid range")

    def test_inverted_low_base_high_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["valuation_range"] = _range(low=20.0, base=15.0, high=10.0)
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="low")

    def test_valid_ordered_range_accepted(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        assert_valid(_validate(res, arch, evid))

    def test_scenario_family_forbids_low_base_high(self):
        arch = _archetype(ticker="ZZFAKE1", primary="D")
        evid = _evidence(ticker="ZZFAKE1")
        families = [_family_entry(
            family_id="family_7_scenario_probability_weighted", governed_role="primary_candidate",
            family_status="completed",
            valuation_range={**_scenario_range(), "low": 5.0},
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        assert_invalid(_validate(res, arch, evid), contains="must not carry low/base/high")

    def test_non_scenario_family_forbids_scenario_outcomes(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["valuation_range"]["scenario_outcomes"] = [_scenario_outcome()]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="only family 7 may carry scenario_outcomes")


# ═══════════════════════════════════════════════════════════════════════
# 16-18: provenance
# ═══════════════════════════════════════════════════════════════════════

class TestAssumptionProvenance:
    def test_missing_assumption_provenance(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["methodology_families_applied"][0]["assumptions_ledger"][0]["provenance_label"]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="provenance_label")

    def test_invalid_assumption_provenance(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["assumptions_ledger"][0]["provenance_label"] = "not_a_real_label"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="provenance_label")

    @pytest.mark.parametrize("label", [
        "market_derived", "historically_observed", "analyst_consensus_cited", "assumed_for_illustration",
    ])
    def test_every_allowed_provenance_label_accepted(self, label):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["assumptions_ledger"][0]["provenance_label"] = label
        _reseal(res)
        assert_valid(_validate(res, arch, evid))


# ═══════════════════════════════════════════════════════════════════════
# 19-22: method compatibility
# ═══════════════════════════════════════════════════════════════════════

class TestMethodCompatibility:
    def test_prohibited_method_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")  # family_1 prohibited for A
        evid = _evidence(ticker="ZZFAKE1", segment_evidence={"segments": [{"segment_name": "x", "revenue": _line_item()}]})
        families = [_family_entry(family_id="family_1_asset_based_sotp", governed_role="prohibited", family_status="unable_to_determine", valuation_range=None, applied_peers=None)]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="unable_to_determine", abstention_reason="x")
        assert_invalid(_validate(res, arch, evid), contains="is 'prohibited'")

    def test_insufficient_basis_method_rejected(self):
        # No cell in VALUATION-0002 SS2's table resolves insufficient_basis_for_adoption
        # today -- declaring it is therefore always a mismatch against the live table.
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1")
        families = [_family_entry(
            family_id="family_2_fcff_dcf", governed_role="insufficient_basis_for_adoption",
            family_status="unable_to_determine", valuation_range=None, applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="unable_to_determine", abstention_reason="x")
        assert_invalid(_validate(res, arch, evid), contains="does not match")

    def test_governed_role_mismatch_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        # family_5 is primary_candidate for A -- declare secondary_corroborative instead.
        res["methodology_families_applied"][0]["governed_role"] = "secondary_corroborative"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="does not match")

    @pytest.mark.parametrize("archetype_letter,family_id,expected_role", [
        ("A", "family_2_fcff_dcf", "primary_candidate"),
        ("G", "family_3_fcfe_dcf", "primary_candidate"),
        ("F", "family_1_asset_based_sotp", "primary_candidate"),
        ("D", "family_7_scenario_probability_weighted", "primary_candidate"),
        ("E", "family_7_scenario_probability_weighted", "primary_candidate"),
        ("B", "family_5_relative_valuation", "primary_candidate"),
        ("G", "family_4_earnings_fcf_yield", "secondary_corroborative"),
        ("B", "family_6_roic_reinvestment", "secondary_corroborative"),
        ("C", "family_5_relative_valuation", "adjustment_required"),
    ])
    def test_valid_method_archetype_combinations_across_archetype_classes(self, archetype_letter, family_id, expected_role):
        arch = _archetype(ticker="ZZFAKE1", primary=archetype_letter)
        evid = _evidence(ticker="ZZFAKE1", segment_evidence={"segments": [{"segment_name": "x", "revenue": _line_item()}]})
        range_value = _scenario_range() if family_id == "family_7_scenario_probability_weighted" else _range()
        families = [_family_entry(
            family_id=family_id, governed_role=expected_role, family_status="partial",
            valuation_range=range_value,
            assumptions_ledger=[], applied_peers=(["FAKEPEER1", "FAKEPEER2"] if family_id == "family_5_relative_valuation" else None),
        )]
        if families[0]["applied_peers"] is None:
            del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial", abstention_reason="Only a partial family attempted for this fictional test.")
        assert_valid(_validate(res, arch, evid))


# ═══════════════════════════════════════════════════════════════════════
# 23-26: hash / references
# ═══════════════════════════════════════════════════════════════════════

class TestReferences:
    def test_stale_archetype_hash_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["archetype_reference"]["content_sha256"] = "0" * 64
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="archetype_reference.content_sha256")

    def test_stale_evidence_hash_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["evidence_reference"]["content_sha256"] = "0" * 64
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="evidence_reference.content_sha256")

    def test_ticker_mismatch_across_references_rejected(self):
        arch = _archetype(ticker="ZZFAKE1")
        other_arch = _archetype(ticker="ZZFAKE2")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        # point the reference at a *different* ticker's archetype record
        res["archetype_reference"] = {"source_file": "intelligence/valuation_archetype/ZZFAKE2.yaml", "content_sha256": other_arch["content_sha256"]}
        _reseal(res)
        r = vrv.validate_result_data(res, archetype_data=other_arch, evidence_data=evid)
        assert_invalid(r, contains="does not match this record's own ticker")

    def test_correct_live_style_synthetic_references_accepted(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        assert_valid(_validate(res, arch, evid))


# ═══════════════════════════════════════════════════════════════════════
# 27-29: terminal growth
# ═══════════════════════════════════════════════════════════════════════

class TestTerminalGrowth:
    def _dcf_result(self, terminal_growth: float, discount_rate: float, evid_discount=None):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=(evid_discount or _discount_rate_evidence()))
        families = [_family_entry(
            family_id="family_2_fcff_dcf", governed_role="primary_candidate",
            family_status="completed" if evid_discount is None else "partial",
            assumptions_ledger=[
                _assumption(assumption_name="terminal_growth", value=terminal_growth, provenance_label="assumed_for_illustration"),
                _assumption(assumption_name="applicable_discount_rate", value=discount_rate, provenance_label="market_derived"),
            ],
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        status = "completed" if evid_discount is None else "partial"
        kwargs = {} if evid_discount is None else {"abstention_reason": "x"}
        res = _result(archetype=arch, evidence=evid, families=families, result_status=status, **kwargs)
        return arch, evid, res

    def test_g_less_than_r_accepted(self):
        arch, evid, res = self._dcf_result(0.02, 0.09)
        assert_valid(_validate(res, arch, evid))

    def test_g_equals_r_rejected(self):
        arch, evid, res = self._dcf_result(0.05, 0.05)
        assert_invalid(_validate(res, arch, evid), contains="strictly less than")

    def test_g_greater_than_r_rejected(self):
        arch, evid, res = self._dcf_result(0.10, 0.05)
        assert_invalid(_validate(res, arch, evid), contains="strictly less than")


# ═══════════════════════════════════════════════════════════════════════
# 30-33: peers
# ═══════════════════════════════════════════════════════════════════════

class TestPeers:
    def test_invented_peer_outside_stage3_candidates_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1", primary="B"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["applied_peers"] = ["FAKEPEER1", "INVENTEDPEER"]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="not present among")

    def test_completed_relative_result_below_minimum_peer_count_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1", primary="B"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["applied_peers"] = ["FAKEPEER1"]
        res["methodology_families_applied"][0]["family_status"] = "completed"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="at least 2 applied peers")

    def test_partial_result_handles_thin_peer_set_as_governed(self):
        arch, evid = _archetype(ticker="ZZFAKE1", primary="B"), _evidence(ticker="ZZFAKE1")
        families = [_family_entry(family_status="partial", applied_peers=["FAKEPEER1"])]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial", abstention_reason="Only one comparable peer available for this fictional test.")
        assert_valid(_validate(res, arch, evid))

    def test_valid_sourced_subset_accepted(self):
        arch, evid = _archetype(ticker="ZZFAKE1", primary="B"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["applied_peers"] = ["FAKEPEER1"]  # subset of the 2 included
        res["methodology_families_applied"][0]["family_status"] = "partial"
        res["result_status"] = "partial"
        res["abstention_reason"] = "Below the two-peer minimum for a completed determination."
        res["cross_asset_handoff"]["result_status"] = "partial"
        res["cross_asset_handoff"]["family_summary"][0]["family_status"] = "partial"
        _reseal(res)
        assert_valid(_validate(res, arch, evid))


# ═══════════════════════════════════════════════════════════════════════
# 34-38: scenario
# ═══════════════════════════════════════════════════════════════════════

class TestScenarioProbability:
    def _scenario_result(self, outcomes, *, exhaustive=True):
        arch = _archetype(ticker="ZZFAKE1", primary="D")
        evid = _evidence(ticker="ZZFAKE1")
        families = [_family_entry(
            family_id="family_7_scenario_probability_weighted", governed_role="primary_candidate",
            family_status="completed", valuation_range=_scenario_range(outcomes, exhaustive=exhaustive),
            assumptions_ledger=[], applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        return arch, evid, res

    def test_invalid_probability_sum_rejected(self):
        outcomes = [
            _scenario_outcome(scenario_name="Fictional upside case", value=25.0, probability_weight=0.9, probability_weight_provenance_label="assumed_for_illustration"),
            _scenario_outcome(scenario_name="Fictional downside case", value=8.0, probability_weight=0.9, probability_weight_provenance_label="assumed_for_illustration"),
        ]
        arch, evid, res = self._scenario_result(outcomes)
        assert_invalid(_validate(res, arch, evid), contains="outside the disclosed")

    def test_valid_coherent_set_accepted(self):
        arch, evid, res = self._scenario_result(None)
        assert_valid(_validate(res, arch, evid))

    def test_missing_probability_provenance_rejected(self):
        outcomes = [
            _scenario_outcome(scenario_name="Fictional upside case", value=25.0, probability_weight=0.5),
            _scenario_outcome(scenario_name="Fictional downside case", value=8.0, probability_weight=0.5, probability_weight_provenance_label="assumed_for_illustration"),
        ]
        arch, evid, res = self._scenario_result(outcomes)
        assert_invalid(_validate(res, arch, evid), contains="probability_weight_provenance_label")

    def test_invented_scenario_rejected(self):
        outcomes = [
            _scenario_outcome(scenario_name="An invented scenario never named in Stage-3 evidence", value=25.0),
        ]
        arch, evid, res = self._scenario_result(outcomes)
        assert_invalid(_validate(res, arch, evid), contains="not present among the pinned evidence record")

    def test_non_exhaustive_set_exempt_from_sum_requirement(self):
        outcomes = [
            _scenario_outcome(scenario_name="Fictional upside case", value=25.0, probability_weight=0.3, probability_weight_provenance_label="assumed_for_illustration"),
            _scenario_outcome(scenario_name="Fictional downside case", value=8.0, probability_weight=0.3, probability_weight_provenance_label="assumed_for_illustration"),
        ]
        arch, evid, res = self._scenario_result(outcomes, exhaustive=False)
        assert_valid(_validate(res, arch, evid))

    def test_silent_normalization_not_permitted_raw_weights_checked_as_declared(self):
        """No renormalization occurs anywhere -- the coherence check runs
        against the declared weights exactly as recorded."""
        outcomes = [
            _scenario_outcome(scenario_name="Fictional upside case", value=25.0, probability_weight=0.4, probability_weight_provenance_label="assumed_for_illustration"),
            _scenario_outcome(scenario_name="Fictional downside case", value=8.0, probability_weight=0.4, probability_weight_provenance_label="assumed_for_illustration"),
        ]
        arch, evid, res = self._scenario_result(outcomes)  # sums to 0.8, exhaustive=True by default
        assert_invalid(_validate(res, arch, evid), contains="outside the disclosed")


# ═══════════════════════════════════════════════════════════════════════
# 39-41: conflicts
# ═══════════════════════════════════════════════════════════════════════

class TestConflictPropagation:
    def test_required_carried_forward_conflict_omitted_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=_discount_rate_evidence_abstained())
        families = [_family_entry(family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="partial", applied_peers=None)]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial",
                       abstention_reason="Discount-rate evidence unavailable.", conflicts=[])
        assert_invalid(_validate(res, arch, evid), contains="conflicts_carried_forward is missing")

    def test_valid_reference_accepted(self):
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=_discount_rate_evidence_abstained())
        families = [_family_entry(family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="partial", applied_peers=None)]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial",
                       abstention_reason="Discount-rate evidence unavailable.")
        assert_valid(_validate(res, arch, evid))

    def test_completed_family_forbidden_when_required_domain_bears_conflict(self):
        """Reviewer-judgment-only materiality is never falsely encoded as
        deterministic logic -- only the mechanically detectable signal
        (domain-level abstention / non-empty disclosed_conflicts) forces
        this; nothing here claims to judge economic materiality itself."""
        arch = _archetype(ticker="ZZFAKE1", primary="A")
        evid = _evidence(ticker="ZZFAKE1", discount_rate_evidence=_discount_rate_evidence_abstained())
        families = [_family_entry(
            family_id="family_2_fcff_dcf", governed_role="primary_candidate", family_status="completed",
            applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="completed")
        assert_invalid(_validate(res, arch, evid), contains="may not be 'completed'")


# ═══════════════════════════════════════════════════════════════════════
# 42-44: abstention
# ═══════════════════════════════════════════════════════════════════════

class TestAbstention:
    def test_abstention_without_reason_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="unable_to_determine_archetype")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid, families=[], result_status="unable_to_determine",
                       abstention_reason=None, conflicts=[])
        assert_invalid(_validate(res, arch, evid), contains="abstention_reason is required")

    def test_unable_to_determine_with_valuation_output_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="unable_to_determine_archetype")
        evid = _evidence(ticker="ZZFAKE1")
        families = [_family_entry(applied_peers=["FAKEPEER1", "FAKEPEER2"])]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="unable_to_determine",
                       abstention_reason="x")
        assert_invalid(_validate(res, arch, evid), contains="methodology_families_applied must be empty")

    def test_valid_abstention_accepted(self):
        arch = _archetype(ticker="ZZFAKE1", primary="unable_to_determine_archetype")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid, families=[], result_status="unable_to_determine",
                       abstention_reason="Pinned archetype record itself abstained.", conflicts=[])
        assert_valid(_validate(res, arch, evid))

    def test_completed_result_forbids_abstention_reason(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["abstention_reason"] = "should not be here"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="must be absent when result_status is 'completed'")


# ═══════════════════════════════════════════════════════════════════════
# 45-49: leakage / isolation
# ═══════════════════════════════════════════════════════════════════════

class TestLeakage:
    def test_opaque_score_leakage_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["methodology_families_applied"][0]["opaque_score"] = 88
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid))

    def test_target_tier_allocation_field_leakage_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["target_pct"] = 0.05
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid))

    def test_fair_value_field_leakage_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["fair_value"] = 42.0
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid))

    @pytest.mark.parametrize("word", ["buy", "sell", "add", "hold", "trim", "exit", "wait", "stage"])
    def test_trading_directive_language_leakage_rejected(self, word):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["uncertainty_summary"] = f"An analyst might {word} this position based on the range."
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="directive word")

    def test_directive_word_does_not_false_positive_on_holdings(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["uncertainty_summary"] = "This fictional analysis makes no claim about current holdings."
        _reseal(res)
        assert_valid(_validate(res, arch, evid))

    def test_chart_domain_leakage_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["sensitivity_disclosure"] = "The range is most sensitive to the recent moving average."
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="chart-derived terminology")

    def test_zero_allocator_margin_import_coupling(self):
        import ast
        source = Path("valuation_result_validator.py").read_text()
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert "allocate" not in imported
        assert "margin_state" not in imported


# ═══════════════════════════════════════════════════════════════════════
# 50-53: population / lifecycle / determinism / manifest
# ═══════════════════════════════════════════════════════════════════════

class TestPopulationAndLifecycle:
    def test_absent_result_directory_accepted_at_scaffold_state(self):
        result = vrv.validate_valuation_results_directory(REPO_ROOT / "intelligence" / "valuation_results", repo_root=REPO_ROOT)
        assert result.valid
        assert result.record_count == 0

    def test_zero_real_company_population_in_repository(self):
        assert not (REPO_ROOT / "intelligence" / "valuation_results").exists(), (
            "VALUATION-0006 SS A/SS S authorizes zero real-company population -- this "
            "implementation must not create any real result file"
        )

    def test_deterministic_canonical_hash(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        h1 = vrv.canonical_record_hash(res)
        h2 = vrv.canonical_record_hash(copy.deepcopy(res))
        assert h1 == h2

    def test_hash_changes_on_content_change(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        h1 = vrv.canonical_record_hash(res)
        mutated = copy.deepcopy(res)
        mutated["as_of_date"] = "2026-08-10"
        h2 = vrv.canonical_record_hash(mutated)
        assert h1 != h2

    def test_manifest_reconciliation_valid(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        records = {"ZZFAKE1": res}
        manifest = {
            "schema_version": "1.0", "governing_decision": "VALUATION-0006",
            "cohort": [{
                "ticker": "ZZFAKE1", "sealed_at": res["sealed_at"], "content_sha256": res["content_sha256"],
                "schema_version": "1.0", "governing_decision": "VALUATION-0006",
                "record_path": "intelligence/valuation_results/ZZFAKE1.yaml",
            }],
        }
        result = vrv.validate_cohort_manifest(manifest, records)
        assert_valid(result)

    def test_manifest_reconciliation_hash_mismatch_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        records = {"ZZFAKE1": res}
        manifest = {
            "schema_version": "1.0", "governing_decision": "VALUATION-0006",
            "cohort": [{
                "ticker": "ZZFAKE1", "sealed_at": res["sealed_at"], "content_sha256": "0" * 64,
                "schema_version": "1.0", "governing_decision": "VALUATION-0006",
                "record_path": "intelligence/valuation_results/ZZFAKE1.yaml",
            }],
        }
        result = vrv.validate_cohort_manifest(manifest, records)
        assert_invalid(result, contains="content_sha256 mismatch")

    def test_manifest_orphan_record_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        records = {"ZZFAKE1": res}
        manifest = {"schema_version": "1.0", "governing_decision": "VALUATION-0006", "cohort": []}
        result = vrv.validate_cohort_manifest(manifest, records)
        assert_invalid(result, contains="no corresponding cohort manifest entry")

    def test_authorized_cohort_missing_and_extra(self):
        arch1, evid1 = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res1 = _result(archetype=arch1, evidence=evid1)
        records = {"ZZFAKE1": res1}
        result = vrv.validate_authorized_cohort(records, frozenset({"ZZFAKE1", "ZZFAKE2"}))
        assert_invalid(result, contains="missing ticker(s)")

        result2 = vrv.validate_authorized_cohort(records, frozenset())
        assert_invalid(result2, contains="outside the authorized population")

    def test_authorized_cohort_exact_match(self):
        arch1, evid1 = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res1 = _result(archetype=arch1, evidence=evid1)
        records = {"ZZFAKE1": res1}
        result = vrv.validate_authorized_cohort(records, frozenset({"ZZFAKE1"}))
        assert_valid(result)


# ═══════════════════════════════════════════════════════════════════════
# Additional: seal / draft-state, reference structural failures, YAML
# round-trip via tmp_path (mirrors sibling validators' own file/dir tests)
# ═══════════════════════════════════════════════════════════════════════

class TestSealAndDraftState:
    def test_draft_record_skips_seal_requirements(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["record_status"] = "draft"
        for k in ("sealed_at", "governing_decision", "drafting_session_or_shard_id", "content_sha256", "cohort_manifest_entry"):
            res.pop(k, None)
        r = vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid)
        assert_valid(r)

    def test_sealed_record_missing_seal_field_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["sealed_at"]
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid), contains="missing required seal field")

    def test_sealed_record_hash_mismatch_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["content_sha256"] = "0" * 64
        assert_invalid(vrv.validate_result_data(res, archetype_data=arch, evidence_data=evid), contains="does not reproduce")


class TestReferenceStructuralFailures:
    def test_missing_reference_field(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["archetype_reference"]["source_file"]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="archetype_reference")

    def test_reference_wrong_source_prefix(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        res["archetype_reference"]["source_file"] = "intelligence/valuation_evidence/ZZFAKE1.yaml"
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="must live under")


class TestFileAndDirectoryValidation:
    def test_valid_result_directory_round_trip(self, tmp_path):
        repo_root = tmp_path
        archetype_dir = repo_root / "intelligence" / "valuation_archetype"
        evidence_dir = repo_root / "intelligence" / "valuation_evidence"
        results_dir = repo_root / "intelligence" / "valuation_results"
        archetype_dir.mkdir(parents=True)
        evidence_dir.mkdir(parents=True)
        results_dir.mkdir(parents=True)

        arch = _archetype(ticker="ZZFAKE1")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)

        (archetype_dir / "ZZFAKE1.yaml").write_text(yaml.safe_dump(arch))
        (evidence_dir / "ZZFAKE1.yaml").write_text(yaml.safe_dump(evid))
        (results_dir / "ZZFAKE1.yaml").write_text(yaml.safe_dump(res))
        manifest = {
            "schema_version": "1.0", "governing_decision": "VALUATION-0006",
            "cohort": [{
                "ticker": "ZZFAKE1", "sealed_at": res["sealed_at"], "content_sha256": res["content_sha256"],
                "schema_version": "1.0", "governing_decision": "VALUATION-0006",
                "record_path": "intelligence/valuation_results/ZZFAKE1.yaml",
            }],
        }
        (results_dir / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))

        result = vrv.validate_valuation_results_directory(results_dir, repo_root=repo_root)
        assert_valid_dir(result)

    def test_filename_mismatch_rejected(self, tmp_path):
        repo_root = tmp_path
        archetype_dir = repo_root / "intelligence" / "valuation_archetype"
        evidence_dir = repo_root / "intelligence" / "valuation_evidence"
        results_dir = repo_root / "intelligence" / "valuation_results"
        archetype_dir.mkdir(parents=True)
        evidence_dir.mkdir(parents=True)
        results_dir.mkdir(parents=True)

        arch = _archetype(ticker="ZZFAKE1")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        (results_dir / "WRONGNAME.yaml").write_text(yaml.safe_dump(res))

        result = vrv.validate_valuation_results_directory(results_dir, repo_root=repo_root)
        assert not result.valid
        assert any("does not match" in e for r in result.results for e in r.errors)

    def test_missing_manifest_when_records_exist_rejected(self, tmp_path):
        repo_root = tmp_path
        archetype_dir = repo_root / "intelligence" / "valuation_archetype"
        evidence_dir = repo_root / "intelligence" / "valuation_evidence"
        results_dir = repo_root / "intelligence" / "valuation_results"
        archetype_dir.mkdir(parents=True)
        evidence_dir.mkdir(parents=True)
        results_dir.mkdir(parents=True)

        arch = _archetype(ticker="ZZFAKE1")
        evid = _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        (results_dir / "ZZFAKE1.yaml").write_text(yaml.safe_dump(res))

        result = vrv.validate_valuation_results_directory(results_dir, repo_root=repo_root)
        assert not result.valid
        assert any("COHORT_MANIFEST.yaml is required" in e for r in result.results for e in r.errors)


def assert_valid_dir(result: vrv.DirectoryValidationResult) -> None:
    if not result.valid:
        details = [(r.source, r.errors) for r in result.results if not r.valid]
        raise AssertionError(f"expected valid directory, got: {details}")


# ═══════════════════════════════════════════════════════════════════════
# schema-only path (no archetype_data/evidence_data supplied) -- covers
# the "isolated schema test" mode the module docstring names explicitly.
# ═══════════════════════════════════════════════════════════════════════

class TestSchemaOnlyValidationWithoutLiveReferences:
    def test_schema_only_validation_flags_structural_errors_without_cross_checks(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["as_of_date"]
        _reseal(res)
        result = vrv.validate_result_data(res)
        assert not result.valid
        assert any("as_of_date" in e for e in result.errors)

    def test_schema_only_validation_of_an_otherwise_valid_record_has_no_cross_check_errors(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        result = vrv.validate_result_data(res)
        # Without archetype_data/evidence_data, no cross-check errors fire --
        # only structural/schema issues would appear, and there are none.
        assert result.valid, result.errors


class TestNonDictRoot:
    @pytest.mark.parametrize("bad_root", [None, "a string", 42, [1, 2, 3]])
    def test_non_dict_root_rejected(self, bad_root):
        result = vrv.validate_result_data(bad_root)
        assert not result.valid


class TestGovernedRoleTableIntegrity:
    def test_table_covers_all_seven_archetypes_for_every_family(self):
        for family_id in vrv._FAMILY_IDS:
            assert set(vrv._GOVERNED_ROLE_TABLE[family_id].keys()) == vrv._ARCHETYPE_LETTERS

    def test_governed_role_for_returns_none_for_unrecognized_family(self):
        assert vrv.governed_role_for("not_a_real_family", "A") is None

    def test_families_4_and_6_never_reach_primary_candidate(self):
        for family_id in ("family_4_earnings_fcf_yield", "family_6_roic_reinvestment"):
            roles = set(vrv._GOVERNED_ROLE_TABLE[family_id].values())
            assert "primary_candidate" not in roles


class TestManifestClosedSchema:
    def test_manifest_unknown_top_level_key_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        manifest = {
            "schema_version": "1.0", "governing_decision": "VALUATION-0006", "cohort": [],
            "extra_top_level_key": "x",
        }
        result = vrv.validate_cohort_manifest(manifest, {"ZZFAKE1": res})
        assert_invalid(result, contains="unexpected top-level key")

    def test_manifest_row_missing_required_key_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        manifest = {
            "schema_version": "1.0", "governing_decision": "VALUATION-0006",
            "cohort": [{"ticker": "ZZFAKE1", "content_sha256": res["content_sha256"]}],
        }
        result = vrv.validate_cohort_manifest(manifest, {"ZZFAKE1": res})
        assert_invalid(result, contains="missing required key")

    def test_manifest_duplicate_ticker_rejected(self):
        arch, evid = _archetype(ticker="ZZFAKE1"), _evidence(ticker="ZZFAKE1")
        res = _result(archetype=arch, evidence=evid)
        row = {
            "ticker": "ZZFAKE1", "sealed_at": res["sealed_at"], "content_sha256": res["content_sha256"],
            "schema_version": "1.0", "governing_decision": "VALUATION-0006",
            "record_path": "intelligence/valuation_results/ZZFAKE1.yaml",
        }
        manifest = {"schema_version": "1.0", "governing_decision": "VALUATION-0006", "cohort": [row, dict(row)]}
        result = vrv.validate_cohort_manifest(manifest, {"ZZFAKE1": res})
        assert_invalid(result, contains="more than once")


class TestScenarioOutcomeClosedSchema:
    def test_scenario_outcome_unknown_key_rejected(self):
        arch = _archetype(ticker="ZZFAKE1", primary="D")
        evid = _evidence(ticker="ZZFAKE1")
        outcomes = [_scenario_outcome(scenario_name="Fictional upside case", value=25.0, extra_key="x")]
        families = [_family_entry(
            family_id="family_7_scenario_probability_weighted", governed_role="primary_candidate",
            family_status="partial", valuation_range=_scenario_range(outcomes, exhaustive=False),
            assumptions_ledger=[], applied_peers=None,
        )]
        del families[0]["applied_peers"]
        res = _result(archetype=arch, evidence=evid, families=families, result_status="partial", abstention_reason="x")
        assert_invalid(_validate(res, arch, evid))


class TestFamilyEntryMissingRequiredKey:
    def test_family_entry_missing_family_id_rejected(self):
        arch, evid = _archetype(), _evidence()
        res = _result(archetype=arch, evidence=evid)
        del res["methodology_families_applied"][0]["family_id"]
        _reseal(res)
        assert_invalid(_validate(res, arch, evid), contains="missing required key")
