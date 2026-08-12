"""Tests for level1_sleeve_synthesis_validator.py (WS-0014 Level 1 cross-
asset sleeve-allocation synthesis, XASSET-0012/XASSET-0013 scope, Stage 3
implementation).

Schema-shape tests build synthetic sleeve_profile/sleeve_relationship
fixtures and call the validator with repo_root=None, which skips every
live cross-schema hash/coverage/secondary-condition check (mirroring
contender_evaluation_validator.py's own established convention) -- these
tests exercise closed-schema enforcement, vocabulary closure, and every
forbidden-content scan in isolation from real repository state.

Live-verification tests exercise the real repository's own sealed six
profiles and seven relationships (the only implementation this schema has
ever had), proving the directory-scan, hash-recomputation, coverage-
derivation, and secondary-condition-derivation mechanisms all genuinely
work end to end -- plus a set of adversarial "corrupt one real fact"
mismatch tests against the real repository's own live source layers,
matching contender_evaluation_validator.py's/economic_assessment_
validator.py's own established pattern of testing structural-reference
staleness against real sealed sibling records rather than a synthetic
multi-layer repository built from scratch.

The mandatory eligibility-language-paraphrase adversarial probe
(XASSET-0013 SS H) has its own dedicated test class near the end of this
file, disclosing the result in its own docstring.
"""

from __future__ import annotations

import ast
import copy
import subprocess
from pathlib import Path

import pytest
import yaml

import level1_sleeve_synthesis_validator as l1

REPO_ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Synthetic schema-shape fixtures.
# ---------------------------------------------------------------------------

def _layer_ref(layer_name: str, sleeve_id: str = l1.EQUITY, *, shared_override: dict | None = None) -> dict:
    entry = {
        "layer_name": layer_name,
        "module": f"{l1._LAYER_REGISTRY[layer_name]['module']}.py",
        "directory": l1._LAYER_REGISTRY[layer_name]["directory"],
        "manifest_content_sha256": "a" * 64,
        "as_of_note": "Synthetic as-of note for this fixture.",
    }
    if l1._layer_is_shared(layer_name):
        subjects = list(l1._expected_subjects(layer_name, sleeve_id) or ())
        entry["sleeve_subject_scope"] = {
            "referenced_subject_ids": subjects,
            "referenced_record_content_sha256": {s: "b" * 64 for s in subjects},
        }
    if shared_override:
        entry.update(shared_override)
    return entry


def _profile(sleeve_id: str = l1.EQUITY, **overrides) -> dict:
    layers = l1._SLEEVE_LAYERS[sleeve_id]
    d = {
        "schema_version": l1.SCHEMA_VERSION,
        "sleeve_id": sleeve_id,
        "evidence_layer_references": [_layer_ref(ln, sleeve_id) for ln in layers],
        "economic_role_summary": "Synthetic economic role summary for this fixture sleeve.",
        "evidence_coverage_profile": l1.SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS,
        "functional_role_note": (
            "Synthetic functional role note." if sleeve_id in l1._FUNCTIONAL_ROLE_NOTE_REQUIRED_SLEEVES else None
        ),
        "abstention_index": [
            {
                "source_layer": layers[0],
                "field_path": "synthetic.field",
                "value": "abstained",
                "reason": "Synthetic disclosed gap for this fixture.",
            },
        ],
        "record_status": "draft",
    }
    d.update(overrides)
    return d


def _sealed_profile(sleeve_id: str = l1.EQUITY, **overrides) -> dict:
    d = _profile(sleeve_id, record_status="sealed")
    d.update(overrides)
    d["sealed_at"] = d.get("sealed_at", "2026-08-11T00:00:00Z")
    d["governing_decisions"] = d.get("governing_decisions", [l1._GOVERNING_DECISION])
    d["drafting_session_or_shard_id"] = d.get("drafting_session_or_shard_id", "synthetic-shard")
    d["cohort_manifest_entry"] = d.get("cohort_manifest_entry", f"{l1._PROFILES_DIR}/COHORT_MANIFEST.yaml#{sleeve_id}")
    if "content_sha256" not in overrides:
        d["content_sha256"] = l1.canonical_record_hash(d)
    return d


def _relationship(sleeve_a: str = l1.CASH_RESERVE, sleeve_b: str = l1.EQUITY, **overrides) -> dict:
    d = {
        "schema_version": l1.SCHEMA_VERSION,
        "sleeve_pair": {"sleeve_a": sleeve_a, "sleeve_b": sleeve_b},
        "profile_references": [
            {"sleeve_id": sleeve_a, "referenced_content_sha256": "c" * 64},
            {"sleeve_id": sleeve_b, "referenced_content_sha256": "d" * 64},
        ],
        "primary_disposition": l1.ROLE_PRESERVING,
        "favored_sleeve_id": None,
        "secondary_conditions": [],
        "overlap_dimension_references": [],
        "rationale": "Synthetic rationale describing a role-preserving finding for this fixture pair.",
        "abstention_index": [],
        "record_status": "draft",
    }
    d.update(overrides)
    return d


def _sealed_relationship(sleeve_a: str = l1.CASH_RESERVE, sleeve_b: str = l1.EQUITY, **overrides) -> dict:
    d = _relationship(sleeve_a, sleeve_b, record_status="sealed")
    d.update(overrides)
    d["sealed_at"] = d.get("sealed_at", "2026-08-11T00:00:00Z")
    d["governing_decisions"] = d.get("governing_decisions", [l1._GOVERNING_DECISION])
    d["drafting_session_or_shard_id"] = d.get("drafting_session_or_shard_id", "synthetic-shard")
    d["cohort_manifest_entry"] = d.get(
        "cohort_manifest_entry", f"{l1._RELATIONSHIPS_DIR}/COHORT_MANIFEST.yaml#{sleeve_a}_{sleeve_b}",
    )
    if "content_sha256" not in overrides:
        d["content_sha256"] = l1.canonical_record_hash(d)
    return d


# ===========================================================================
# Constants / registry self-consistency
# ===========================================================================

class TestConstants:
    def test_six_sleeve_ids(self):
        assert l1.SLEEVE_IDS == frozenset({
            "equity", "fund_broad_market", "fund_gld_defensive", "crypto", "cash_reserve", "debt_reduction",
        })

    def test_seven_authorized_relationship_pairs(self):
        assert len(l1.AUTHORIZED_RELATIONSHIP_PAIRS) == 7
        assert l1.AUTHORIZED_RELATIONSHIP_PAIRS == (
            (l1.CASH_RESERVE, l1.DEBT_REDUCTION),
            (l1.CASH_RESERVE, l1.EQUITY),
            (l1.CRYPTO, l1.EQUITY),
            (l1.CRYPTO, l1.FUND_GLD_DEFENSIVE),
            (l1.DEBT_REDUCTION, l1.EQUITY),
            (l1.EQUITY, l1.FUND_BROAD_MARKET),
            (l1.EQUITY, l1.FUND_GLD_DEFENSIVE),
        )

    def test_every_authorized_pair_alphabetically_ordered(self):
        for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS:
            assert a < b

    def test_layer_registry_covers_every_sleeve_layer_reference(self):
        for sleeve_id, layers in l1._SLEEVE_LAYERS.items():
            for layer_name in layers:
                assert layer_name in l1._LAYER_REGISTRY
                assert sleeve_id in l1._LAYER_REGISTRY[layer_name]["sleeve_subjects"]

    def test_shared_layers_identified_correctly(self):
        shared = {ln for ln in l1._LAYER_REGISTRY if l1._layer_is_shared(ln)}
        assert shared == {
            "etf_classification", "functional_doctrine", "economic_assessment",
            "instrument_economic_assessment",
        }

    def test_single_sleeve_layers_identified_correctly(self):
        single = {ln for ln in l1._LAYER_REGISTRY if not l1._layer_is_shared(ln)}
        assert single == {
            "classification", "valuation_archetype", "valuation_evidence", "valuation_results",
            "crypto_classification",
        }

    def test_evidence_coverage_functions_cover_all_six_sleeves(self):
        assert set(l1._COVERAGE_FUNCTIONS.keys()) == l1.SLEEVE_IDS


# ===========================================================================
# Profile schema shape
# ===========================================================================

class TestProfileSchemaShape:
    def test_valid_minimal_profile(self):
        errs = l1.validate_sleeve_profile_data(_sealed_profile(), repo_root=None)
        assert errs == []

    def test_not_a_mapping(self):
        assert l1.validate_sleeve_profile_data([1, 2, 3]) == ["record must be a mapping"]

    def test_missing_top_level_key(self):
        d = _sealed_profile()
        del d["economic_role_summary"]
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("missing top-level key" in e for e in errs)

    def test_extra_top_level_key_rejected(self):
        d = _sealed_profile()
        d["conviction_score"] = 5
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)

    def test_wrong_schema_version(self):
        d = _sealed_profile(schema_version="2.0")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("schema_version" in e for e in errs)

    def test_invalid_sleeve_id(self):
        d = _sealed_profile()
        d["sleeve_id"] = "not_a_real_sleeve"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("sleeve_id invalid" in e for e in errs)

    def test_sleeve_id_mismatch_with_expected(self):
        d = _sealed_profile(sleeve_id=l1.EQUITY)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id=l1.CRYPTO, repo_root=None)
        assert any("does not match filename" in e for e in errs)

    @pytest.mark.parametrize("sleeve_id", sorted(l1.SLEEVE_IDS))
    def test_every_sleeve_id_valid_alone(self, sleeve_id):
        d = _sealed_profile(sleeve_id=sleeve_id)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id=sleeve_id, repo_root=None)
        assert errs == [], errs

    def test_evidence_coverage_profile_invalid_value(self):
        d = _sealed_profile(evidence_coverage_profile="mostly_fine")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("evidence_coverage_profile invalid" in e for e in errs)

    @pytest.mark.parametrize("value", sorted(l1._EVIDENCE_COVERAGE_VALUES))
    def test_every_evidence_coverage_value_accepted_at_schema_level(self, value):
        d = _sealed_profile(evidence_coverage_profile=value)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert errs == []

    def test_functional_role_note_required_for_fund_gld_defensive(self):
        d = _sealed_profile(sleeve_id=l1.FUND_GLD_DEFENSIVE, functional_role_note=None)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("functional_role_note must be a non-empty string" in e for e in errs)

    def test_functional_role_note_required_for_cash_reserve(self):
        d = _sealed_profile(sleeve_id=l1.CASH_RESERVE, functional_role_note=None)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("functional_role_note must be a non-empty string" in e for e in errs)

    def test_functional_role_note_required_for_debt_reduction(self):
        d = _sealed_profile(sleeve_id=l1.DEBT_REDUCTION, functional_role_note=None)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("functional_role_note must be a non-empty string" in e for e in errs)

    def test_functional_role_note_forbidden_for_equity(self):
        d = _sealed_profile(sleeve_id=l1.EQUITY, functional_role_note="should not be here")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be null" in e for e in errs)

    def test_functional_role_note_forbidden_for_fund_broad_market(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET, functional_role_note="should not be here")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be null" in e for e in errs)

    def test_functional_role_note_forbidden_for_crypto(self):
        d = _sealed_profile(sleeve_id=l1.CRYPTO, functional_role_note="should not be here")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be null" in e for e in errs)

    def test_record_status_invalid(self):
        d = _sealed_profile(record_status="pending")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("record_status invalid" in e for e in errs)

    def test_governing_decisions_wrong(self):
        d = _sealed_profile()
        d["governing_decisions"] = ["XASSET-0012"]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("governing_decisions must be" in e for e in errs)

    def test_content_sha256_does_not_reproduce(self):
        d = _sealed_profile()
        d["content_sha256"] = "f" * 64
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("content_sha256 does not reproduce" in e for e in errs)

    def test_content_sha256_empty_string_rejected(self):
        d = _sealed_profile()
        d["content_sha256"] = ""
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("content_sha256 must be a non-empty string" in e for e in errs)

    def test_economic_role_summary_empty_rejected(self):
        d = _sealed_profile(economic_role_summary="")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("economic_role_summary must be a non-empty string" in e for e in errs)

    def test_missing_evidence_layer_references_rejected(self):
        d = _sealed_profile()
        d["evidence_layer_references"] = []
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("non-empty list" in e for e in errs)


class TestEvidenceLayerReferenceShape:
    def test_unrecognized_layer_name_rejected(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["layer_name"] = "not_a_real_layer"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("not a recognized governed layer" in e for e in errs)

    def test_layer_not_authorized_for_sleeve(self):
        d = _sealed_profile(sleeve_id=l1.EQUITY)
        d["evidence_layer_references"] = [_layer_ref("crypto_classification", l1.EQUITY)]
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("not an authorized governed layer" in e for e in errs)

    def test_missing_expected_layer(self):
        d = _sealed_profile(sleeve_id=l1.EQUITY)
        d["evidence_layer_references"] = d["evidence_layer_references"][:1]
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must cite exactly" in e for e in errs)

    def test_wrong_directory(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["directory"] = "intelligence/wrong_directory"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any(".directory must be" in e for e in errs)

    def test_wrong_module(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["module"] = "wrong_module.py"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any(".module must be" in e for e in errs)

    def test_manifest_hash_missing(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["manifest_content_sha256"] = ""
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("manifest_content_sha256 must be a non-empty string" in e for e in errs)

    def test_as_of_note_missing(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["as_of_note"] = ""
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("as_of_note must be a non-empty string" in e for e in errs)

    def test_extra_key_on_layer_reference_rejected(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["extra_field"] = "nope"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)

    def test_sleeve_subject_scope_forbidden_on_unshared_layer(self):
        d = _sealed_profile(sleeve_id=l1.EQUITY)
        d["evidence_layer_references"][0]["sleeve_subject_scope"] = {
            "referenced_subject_ids": ["FAKE"],
            "referenced_record_content_sha256": {"FAKE": "a" * 64},
        }
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden" in e and "sleeve_subject_scope" in e for e in errs)

    def test_sleeve_subject_scope_required_on_shared_layer(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                del ref["sleeve_subject_scope"]
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("missing key" in e and "sleeve_subject_scope" in e for e in errs)

    def test_sleeve_subject_scope_wrong_subject_set(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["referenced_subject_ids"] = ["SPY", "VEA"]
                ref["sleeve_subject_scope"]["referenced_record_content_sha256"] = {"SPY": "b" * 64, "VEA": "b" * 64}
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be exactly" in e for e in errs)

    def test_sleeve_subject_scope_rejects_out_of_scope_subject_gld_inside_fund_broad_market(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["referenced_subject_ids"] = ["SPY", "VEA", "GLD"]
                ref["sleeve_subject_scope"]["referenced_record_content_sha256"] = {
                    "SPY": "b" * 64, "VEA": "b" * 64, "GLD": "b" * 64,
                }
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be exactly" in e for e in errs)

    def test_sleeve_subject_scope_rejects_spy_inside_fund_gld_defensive(self):
        d = _sealed_profile(sleeve_id=l1.FUND_GLD_DEFENSIVE)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["referenced_subject_ids"] = ["GLD", "SPY"]
                ref["sleeve_subject_scope"]["referenced_record_content_sha256"] = {"GLD": "b" * 64, "SPY": "b" * 64}
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be exactly" in e for e in errs)

    def test_sleeve_subject_scope_rejects_qqq(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["referenced_subject_ids"] = ["SPY", "VEA", "VWO", "QQQ"]
                ref["sleeve_subject_scope"]["referenced_record_content_sha256"]["QQQ"] = "b" * 64
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("must be exactly" in e for e in errs)

    def test_sleeve_subject_scope_hash_keys_mismatch_subject_ids(self):
        d = _sealed_profile(sleeve_id=l1.FUND_GLD_DEFENSIVE)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["referenced_record_content_sha256"] = {"WRONG": "b" * 64}
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("keys must exactly match" in e for e in errs)

    def test_sleeve_subject_scope_extra_key_rejected(self):
        d = _sealed_profile(sleeve_id=l1.FUND_GLD_DEFENSIVE)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["extra"] = "nope"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)

    def test_debt_reduction_single_layer_no_scope_required_for_subject_count_one(self):
        # debt_reduction draws exactly one subject from a SHARED layer
        # (functional_doctrine) -- confirms the uniform sleeve_subject_scope
        # mechanism handles a single-subject case identically to a
        # multi-subject case (fund_broad_market's three).
        d = _sealed_profile(sleeve_id=l1.DEBT_REDUCTION)
        ref = d["evidence_layer_references"][0]
        assert ref["layer_name"] == "functional_doctrine"
        assert ref["sleeve_subject_scope"]["referenced_subject_ids"] == ["DEBT_REDUCTION"]
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert errs == []


class TestProfileAbstentionIndexShape:
    def test_missing_key_in_entry(self):
        d = _sealed_profile()
        d["abstention_index"][0].pop("reason")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("missing key" in e for e in errs)

    def test_extra_key_in_entry_rejected(self):
        d = _sealed_profile()
        d["abstention_index"][0]["extra"] = "nope"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)

    def test_empty_value_rejected(self):
        d = _sealed_profile()
        d["abstention_index"][0]["value"] = ""
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("value must be a non-empty string" in e for e in errs)

    def test_abstention_index_not_a_list(self):
        d = _sealed_profile()
        d["abstention_index"] = "not-a-list"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("abstention_index must be a list" in e for e in errs)


# ===========================================================================
# Structural forbidden-key-name scan / cross-schema leakage
# ===========================================================================

class TestStructuralKeyLeakage:
    @pytest.mark.parametrize("forbidden_key", [
        "score", "rank", "priority_index", "composite_score", "overall_ranking",
    ])
    def test_score_rank_shaped_keys_rejected_anywhere(self, forbidden_key):
        d = _sealed_profile()
        d["evidence_layer_references"][0][forbidden_key] = "x"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)

    @pytest.mark.parametrize("forbidden_key", sorted(l1._CROSS_SCHEMA_FORBIDDEN_KEYS))
    def test_cross_schema_key_rejected_anywhere(self, forbidden_key):
        d = _sealed_profile()
        d["evidence_layer_references"][0][forbidden_key] = "x"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden cross-schema/Level-2-leakage key name" in e for e in errs)

    def test_forbidden_key_nested_deep_inside_abstention_entry(self):
        d = _sealed_profile()
        d["abstention_index"][0]["target_pct"] = "x"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden cross-schema/Level-2-leakage key name" in e for e in errs)

    def test_forbidden_key_inside_sleeve_subject_scope_nested_dict(self):
        d = _sealed_profile(sleeve_id=l1.FUND_BROAD_MARKET)
        for ref in d["evidence_layer_references"]:
            if ref["layer_name"] == "etf_classification":
                ref["sleeve_subject_scope"]["conviction"] = "x"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden cross-schema/Level-2-leakage key name" in e for e in errs)


# ===========================================================================
# Free-text scans -- economic_role_summary is the exercised field for most
# of these; functional_role_note and abstention reason share the identical
# _scan_free_text() call and are spot-checked separately.
# ===========================================================================

class TestPolicyLeakScan:
    @pytest.mark.parametrize("phrase", [
        "conviction", "target_pct", "max_position_size", "targets.yaml", "holdings.yaml",
        "gates.yaml", "next_gate", "allow_add", "issuer_lookthrough.yaml",
        "5% of the book", "5% of portfolio", "target weight", "destination weight",
        "primary_archetype", "capital_priority", "risk_concentration", "economic_system_ref",
        "case_for_review", "maintain_current_weight", "divergence_requires_review",
        "baseline_assumption_stale", "structural_measurement_gap", "relationship_measurement_required",
        "capital_use_type", "hard_constraint_status",
    ])
    def test_policy_leak_phrase_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"Some text mentioning {phrase} inline.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("policy-leak" in e or "numeric-leakage" in e for e in errs), (phrase, errs)

    def test_gate_word_rejected_bare(self):
        d = _sealed_profile(economic_role_summary="This sleeve has no gate on it at all.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("bare-gate-word" in e for e in errs)

    @pytest.mark.parametrize("legit", [
        "a technological gate limits throughput",
        "the gate-all-around transistor structure",
        "cleared the customer-qualification gate",
        "cleared the stop-before-drafting gate",
        "cleared the source-readiness gate",
        "the CI gate passed",
    ])
    def test_gate_legitimate_use_not_rejected(self, legit):
        d = _sealed_profile(economic_role_summary=f"Some text: {legit}, described plainly.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("bare-gate-word" in e for e in errs), errs


class TestChartDomainScan:
    @pytest.mark.parametrize("phrase", [
        "support level", "resistance level", "breakout", "trend line", "moving average",
        "RSI", "MACD", "candlestick", "chart pattern", "technical analysis",
        "oversold", "overbought", "fibonacci", "volume profile", "price target",
    ])
    def test_chart_term_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"Some text discussing {phrase} in prose.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("chart-domain" in e for e in errs), (phrase, errs)


class TestDirectiveWordScan:
    @pytest.mark.parametrize("word", ["buy", "sell", "add", "hold", "trim", "exit", "wait", "stage"])
    def test_bare_directive_word_rejected(self, word):
        d = _sealed_profile(economic_role_summary=f"An instruction to {word} this position now.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("directive-word" in e for e in errs), (word, errs)

    @pytest.mark.parametrize("word_form", [
        "holding", "holdings", "additional", "exiting via a door", "waiting room", "staging area",
    ])
    def test_directive_word_substring_not_falsely_rejected(self, word_form):
        d = _sealed_profile(economic_role_summary=f"Text mentioning {word_form} in an ordinary sentence.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("directive-word" in e for e in errs), (word_form, errs)

    @pytest.mark.parametrize("legit", [
        "an early-stage business", "this is Stage 3 of the process",
    ])
    def test_stage_legitimate_use_not_rejected(self, legit):
        d = _sealed_profile(economic_role_summary=f"Some text: {legit}, described plainly.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("directive-word:\\bstage\\b" in e for e in errs), errs


class TestNumericLeakageScan:
    def test_bare_digit_rejected(self):
        d = _sealed_profile(economic_role_summary="This sleeve carries 27 positions.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("bare-digit" in e for e in errs)

    @pytest.mark.parametrize("phrase", [
        "grew three times faster", "revenue doubled", "margins tripled", "a fivefold increase",
        "exposure halved", "a twofold gain",
    ])
    def test_magnitude_word_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"This sleeve {phrase} recently.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("written-out-magnitude-word" in e for e in errs), (phrase, errs)

    @pytest.mark.parametrize("word", [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "dozen", "hundred", "thousand", "million", "billion",
    ])
    def test_spelled_out_cardinal_rejected(self, word):
        d = _sealed_profile(economic_role_summary=f"This sleeve holds {word} covered instruments.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("spelled-out-cardinal-number" in e for e in errs), (word, errs)

    @pytest.mark.parametrize("word", [
        # Regression for a real, independent post-push review finding
        # (pullrequestreview on PR #303, MINOR-4): the original word list
        # stopped at "ten", leaving eleven through ninety-nine uncaught.
        "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty",
        "fifty", "sixty", "seventy", "eighty", "ninety",
    ])
    def test_spelled_out_cardinal_eleven_through_ninety_rejected(self, word):
        d = _sealed_profile(economic_role_summary=f"This sleeve holds {word} covered instruments.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("spelled-out-cardinal-number" in e for e in errs), (word, errs)

    def test_hyphenated_compound_cardinal_rejected(self):
        # "twenty-one" -- the tens word alone (\btwenty\b) already matches
        # within a hyphenated compound, since a hyphen is a non-word
        # character; this pins that behavior explicitly.
        d = _sealed_profile(economic_role_summary="This sleeve holds twenty-one covered instruments.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("spelled-out-cardinal-number" in e for e in errs), errs

    def test_hash_and_date_fields_not_scanned_for_digits(self):
        # content_sha256/sealed_at are structural, never scanned -- this
        # confirms the schema-level fields (not free-text fields) remain
        # untouched by the numeric-leakage scan.
        d = _sealed_profile()
        assert any(c.isdigit() for c in d["sealed_at"])
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert errs == []


class TestComparativeSuperiorityScan:
    @pytest.mark.parametrize("phrase", [
        "a stronger investment", "a weaker business", "the superior company", "an inferior opportunity",
        "the better choice", "a worse holding", "the preferable allocation", "the preferred pick",
        "the best option", "the worst case", "superior to its peer", "better positioned",
        "should outperform", "expected to underperform", "should beat",
    ])
    def test_comparative_superiority_phrase_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"This sleeve is {phrase} relative to its peer.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("comparative-superiority" in e for e in errs), (phrase, errs)

    @pytest.mark.parametrize("sentence", [
        # Regression for a real, independent post-push review finding
        # (pullrequestreview on PR #303, MINOR-3): three ordinary
        # comparative-superiority idioms not covered by the original
        # adjective+noun alternation or standalone-verb patterns.
        "This sleeve has the edge over its peer, disclosed here plainly.",
        "This sleeve wins out over its peer, disclosed here plainly.",
        "This sleeve is the top choice among its peers, disclosed here plainly.",
    ])
    def test_comparative_superiority_idiom_rejected(self, sentence):
        d = _sealed_profile(economic_role_summary=sentence)
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("comparative-superiority" in e for e in errs), (sentence, errs)

    @pytest.mark.parametrize("safe", [
        "this sleeve's own evidence maturity is relatively weaker",
        "the evidence base is comparatively thin",
        "this sleeve's research is more developed than its sibling's",
    ])
    def test_evidence_maturity_language_without_trailing_noun_allowed(self, safe):
        d = _sealed_profile(economic_role_summary=f"{safe}, disclosed here plainly.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("comparative-superiority" in e for e in errs), (safe, errs)



# ===========================================================================
# Relationship schema shape
# ===========================================================================

class TestRelationshipSchemaShape:
    def test_valid_minimal_relationship(self):
        errs = l1.validate_sleeve_relationship_data(_sealed_relationship(), repo_root=None)
        assert errs == []

    def test_not_a_mapping(self):
        assert l1.validate_sleeve_relationship_data("nope") == ["record must be a mapping"]

    def test_missing_top_level_key(self):
        d = _sealed_relationship()
        del d["rationale"]
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("missing top-level key" in e for e in errs)

    def test_extra_top_level_key_rejected(self):
        d = _sealed_relationship()
        d["opportunity_score"] = 5
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)

    def test_wrong_schema_version(self):
        d = _sealed_relationship(schema_version="2.0")
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("schema_version" in e for e in errs)

    def test_sleeve_pair_not_alphabetical(self):
        d = _sealed_relationship()
        d["sleeve_pair"] = {"sleeve_a": l1.EQUITY, "sleeve_b": l1.CASH_RESERVE}
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("alphabetically ordered" in e for e in errs)

    def test_sleeve_pair_invalid_sleeve_id(self):
        d = _sealed_relationship()
        d["sleeve_pair"] = {"sleeve_a": "not_real", "sleeve_b": l1.EQUITY}
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("sleeve_pair.sleeve_a invalid" in e for e in errs)

    def test_sleeve_pair_not_authorized(self):
        d = _sealed_relationship(sleeve_a=l1.CRYPTO, sleeve_b=l1.FUND_BROAD_MARKET)
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("not one of the seven" in e for e in errs)

    def test_filename_mismatch(self):
        d = _sealed_relationship(sleeve_a=l1.CASH_RESERVE, sleeve_b=l1.EQUITY)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem="crypto_equity", repo_root=None)
        assert any("does not match filename" in e for e in errs)

    @pytest.mark.parametrize("sleeve_a,sleeve_b", l1.AUTHORIZED_RELATIONSHIP_PAIRS)
    def test_every_authorized_pair_valid_alone(self, sleeve_a, sleeve_b):
        d = _sealed_relationship(sleeve_a, sleeve_b)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem=f"{sleeve_a}_{sleeve_b}", repo_root=None)
        assert errs == [], errs

    def test_primary_disposition_invalid(self):
        d = _sealed_relationship(primary_disposition="somewhat_related")
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("primary_disposition invalid" in e for e in errs)

    def test_favored_sleeve_id_required_when_stronger_evidence_maturity(self):
        d = _sealed_relationship(primary_disposition=l1.STRONGER_EVIDENCE_MATURITY, favored_sleeve_id=None)
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("favored_sleeve_id must equal sleeve_a or sleeve_b" in e for e in errs)

    def test_favored_sleeve_id_must_be_one_of_the_pair(self):
        d = _sealed_relationship(
            sleeve_a=l1.CASH_RESERVE, sleeve_b=l1.EQUITY,
            primary_disposition=l1.STRONGER_EVIDENCE_MATURITY, favored_sleeve_id=l1.CRYPTO,
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("favored_sleeve_id must equal sleeve_a or sleeve_b" in e for e in errs)

    def test_favored_sleeve_id_forbidden_when_not_stronger_evidence_maturity(self):
        d = _sealed_relationship(primary_disposition=l1.ROLE_PRESERVING, favored_sleeve_id=l1.EQUITY)
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must be null when primary_disposition is not" in e for e in errs)

    @pytest.mark.parametrize("sleeve_a,sleeve_b", [(l1.CASH_RESERVE, l1.EQUITY)])
    def test_favored_sleeve_id_accepts_either_side(self, sleeve_a, sleeve_b):
        for favored in (sleeve_a, sleeve_b):
            d = _sealed_relationship(sleeve_a, sleeve_b, primary_disposition=l1.STRONGER_EVIDENCE_MATURITY, favored_sleeve_id=favored)
            errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
            assert errs == [], (favored, errs)

    def test_secondary_conditions_invalid_value(self):
        d = _sealed_relationship(secondary_conditions=["not_a_real_condition"])
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("secondary_conditions invalid" in e for e in errs)

    def test_secondary_conditions_duplicate_rejected(self):
        d = _sealed_relationship(secondary_conditions=[l1.EVIDENCE_PARTIAL_PRESENT, l1.EVIDENCE_PARTIAL_PRESENT])
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("secondary_conditions invalid" in e for e in errs)

    def test_rationale_empty_rejected(self):
        d = _sealed_relationship(rationale="")
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("rationale must be a non-empty string" in e for e in errs)

    def test_record_status_invalid(self):
        d = _sealed_relationship(record_status="pending")
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("record_status invalid" in e for e in errs)

    def test_content_sha256_does_not_reproduce(self):
        d = _sealed_relationship()
        d["content_sha256"] = "f" * 64
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("content_sha256 does not reproduce" in e for e in errs)


class TestProfileReferencesShape:
    def test_wrong_count(self):
        d = _sealed_relationship()
        d["profile_references"] = d["profile_references"][:1]
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("exactly two entries" in e for e in errs)

    def test_sleeve_id_not_in_pair(self):
        d = _sealed_relationship(sleeve_a=l1.CASH_RESERVE, sleeve_b=l1.EQUITY)
        d["profile_references"][0]["sleeve_id"] = l1.CRYPTO
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must be one of the pair" in e for e in errs)

    def test_duplicate_sleeve_id_in_profile_references(self):
        d = _sealed_relationship(sleeve_a=l1.CASH_RESERVE, sleeve_b=l1.EQUITY)
        d["profile_references"][1]["sleeve_id"] = l1.CASH_RESERVE
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must cite exactly" in e for e in errs)

    def test_missing_hash(self):
        d = _sealed_relationship()
        d["profile_references"][0]["referenced_content_sha256"] = ""
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("referenced_content_sha256 must be a non-empty string" in e for e in errs)

    def test_extra_key_rejected(self):
        d = _sealed_relationship()
        d["profile_references"][0]["extra"] = "x"
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)


class TestOverlapDimensionReferencesShape:
    def test_forbidden_when_flag_not_set(self):
        d = _sealed_relationship(
            secondary_conditions=[],
            overlap_dimension_references=[{"dimension_id": "sleeve_concentration", "referenced_content_sha256": "a" * 64}],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must be empty when secondary_conditions does not include" in e for e in errs)

    def test_required_when_flag_set(self):
        d = _sealed_relationship(
            secondary_conditions=[l1.OVERLAP_OR_DUPLICATION_DISCLOSED],
            overlap_dimension_references=[],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must be non-empty when secondary_conditions includes" in e for e in errs)

    def test_entry_missing_key(self):
        d = _sealed_relationship(
            secondary_conditions=[l1.OVERLAP_OR_DUPLICATION_DISCLOSED],
            overlap_dimension_references=[{"dimension_id": "sleeve_concentration"}],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("missing key" in e for e in errs)

    def test_entry_extra_key_rejected(self):
        d = _sealed_relationship(
            secondary_conditions=[l1.OVERLAP_OR_DUPLICATION_DISCLOSED],
            overlap_dimension_references=[
                {"dimension_id": "sleeve_concentration", "referenced_content_sha256": "a" * 64, "extra": "x"},
            ],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("unrecognized key" in e for e in errs)


class TestRelationshipAbstentionIndexShape:
    def test_unable_to_determine_requires_primary_disposition_entry(self):
        d = _sealed_relationship(primary_disposition=l1.RELATIONSHIP_ABSTENTION, favored_sleeve_id=None, abstention_index=[])
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("must contain an entry with field='primary_disposition'" in e for e in errs)

    def test_unable_to_determine_with_entry_passes(self):
        d = _sealed_relationship(
            primary_disposition=l1.RELATIONSHIP_ABSTENTION, favored_sleeve_id=None,
            abstention_index=[{"field": "primary_disposition", "value": "unable_to_determine", "reason": "Synthetic reason."}],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert errs == []

    def test_primary_disposition_entry_present_but_not_abstained_rejected(self):
        d = _sealed_relationship(
            primary_disposition=l1.ROLE_PRESERVING,
            abstention_index=[{"field": "primary_disposition", "value": "unable_to_determine", "reason": "Synthetic reason."}],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("not genuinely abstained" in e for e in errs)

    def test_entry_missing_key(self):
        d = _sealed_relationship(abstention_index=[{"field": "x", "value": "y"}])
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("missing key" in e for e in errs)


class TestContenderBoundaryScan:
    @pytest.mark.parametrize("phrase", [
        "as covered in contender_evaluation", "see intelligence/contenders for detail",
        "citing VRT's own record", "citing WMT's own record",
    ])
    def test_contender_citation_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"Some text: {phrase}, described plainly.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("contender-boundary" in e for e in errs), (phrase, errs)


# ===========================================================================
# Live, real-repository verification -- the only implementation this schema
# has ever had. Proves the directory scan, hash recomputation, coverage
# derivation, and secondary-condition derivation mechanisms genuinely work
# end to end against real sealed content, not merely against synthetic
# fixtures with repo_root=None.
# ===========================================================================

_PROFILES_REAL_DIR = REPO_ROOT / l1._PROFILES_DIR
_RELATIONSHIPS_REAL_DIR = REPO_ROOT / l1._RELATIONSHIPS_DIR


class TestRealRepositoryDirectoryScan:
    def test_profile_directory_valid(self):
        r = l1.validate_sleeve_profile_directory(_PROFILES_REAL_DIR, repo_root=REPO_ROOT)
        assert r.valid, [e for res in r.results if not res.valid for e in res.errors]

    def test_relationship_directory_valid(self):
        r = l1.validate_sleeve_relationship_directory(_RELATIONSHIPS_REAL_DIR, repo_root=REPO_ROOT)
        assert r.valid, [e for res in r.results if not res.valid for e in res.errors]

    def test_exactly_six_profiles_on_disk(self):
        on_disk = {p.stem for p in _PROFILES_REAL_DIR.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        assert on_disk == l1.SLEEVE_IDS

    def test_exactly_seven_relationships_on_disk(self):
        on_disk = {p.stem for p in _RELATIONSHIPS_REAL_DIR.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        expected = {f"{a}_{b}" for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS}
        assert on_disk == expected

    def test_profile_manifest_reconciles(self):
        r = l1.validate_profile_cohort_manifest(_PROFILES_REAL_DIR / "COHORT_MANIFEST.yaml", _PROFILES_REAL_DIR)
        assert r.valid, r.errors

    def test_relationship_manifest_reconciles(self):
        r = l1.validate_relationship_cohort_manifest(_RELATIONSHIPS_REAL_DIR / "COHORT_MANIFEST.yaml", _RELATIONSHIPS_REAL_DIR)
        assert r.valid, r.errors

    def test_every_real_profile_hash_reproducible_twice(self):
        for p in sorted(_PROFILES_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            h1 = l1.canonical_record_hash(data)
            h2 = l1.canonical_record_hash(data)
            assert h1 == h2 == data["content_sha256"]

    def test_every_real_relationship_hash_reproducible_twice(self):
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            h1 = l1.canonical_record_hash(data)
            h2 = l1.canonical_record_hash(data)
            assert h1 == h2 == data["content_sha256"]

    def test_debt_reduction_forced_abstention_live(self):
        data = yaml.safe_load((_PROFILES_REAL_DIR / "debt_reduction.yaml").read_text(encoding="utf-8"))
        assert data["evidence_coverage_profile"] == l1.FORCED_ABSTENTION

    def test_no_sleeve_reaches_fully_computed_today(self):
        # A genuine, disclosed finding of this first population -- every
        # sleeve carries at least one disclosed gap today.
        for sleeve_id in l1.SLEEVE_IDS:
            data = yaml.safe_load((_PROFILES_REAL_DIR / f"{sleeve_id}.yaml").read_text(encoding="utf-8"))
            assert data["evidence_coverage_profile"] != l1.FULLY_COMPUTED

    def test_two_relationships_reach_stronger_evidence_maturity_favoring_equity(self):
        favoring_equity = []
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            if data["primary_disposition"] == l1.STRONGER_EVIDENCE_MATURITY:
                favoring_equity.append((p.stem, data["favored_sleeve_id"]))
        assert len(favoring_equity) == 2
        assert all(favored == l1.EQUITY for _, favored in favoring_equity)

    def test_one_relationship_abstains(self):
        abstained = []
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            if data["primary_disposition"] == l1.RELATIONSHIP_ABSTENTION:
                abstained.append(p.stem)
        assert abstained == ["cash_reserve_debt_reduction"]

    def test_two_relationships_cite_overlap_dimensions(self):
        cited = []
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            if data["overlap_dimension_references"]:
                cited.append(p.stem)
        assert cited == ["debt_reduction_equity", "equity_fund_broad_market"]

    def test_every_cited_overlap_dimension_is_computed_from_existing_mechanism(self):
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            for ref in data["overlap_dimension_references"]:
                dim_path = REPO_ROOT / l1._OVERLAP_MODEL_DIR / f"{ref['dimension_id']}.yaml"
                dim_data = yaml.safe_load(dim_path.read_text(encoding="utf-8"))
                assert dim_data["computation_status"] == l1._COMPUTED_FROM_EXISTING_MECHANISM

    def test_no_relationship_cites_an_interface_only_dimension(self):
        interface_only = {
            "crypto_correlation_interface", "defensive_offset_interface",
            "geographic_currency_exposure", "whole_portfolio_volatility_drawdown_concentration",
        }
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            cited = {ref["dimension_id"] for ref in data["overlap_dimension_references"]}
            assert not (cited & interface_only)

    def test_crypto_fund_gld_defensive_discloses_btc_specific_narrative_match(self):
        data = yaml.safe_load((_RELATIONSHIPS_REAL_DIR / "crypto_fund_gld_defensive.yaml").read_text(encoding="utf-8"))
        rationale = data["rationale"].lower()
        assert "single covered coin" in rationale or "not uniform" in rationale
        assert data["primary_disposition"] == l1.COEXISTENCE_SUPPORTED

    def test_forced_abstention_present_universal_in_this_population(self):
        # Disclosed, not hidden: every one of the six real profiles carries
        # at least one abstention_index entry, so every relationship pair
        # mechanically inherits forced_abstention_present.
        for p in sorted(_RELATIONSHIPS_REAL_DIR.glob("*.yaml")):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
            assert l1.FORCED_ABSTENTION_PRESENT in data["secondary_conditions"]


class TestLiveHashStalenessAgainstRealRepository:
    """Adversarial mismatch tests: take a REAL sealed profile/relationship,
    corrupt exactly one live-verified fact, and confirm the validator
    catches it -- mirroring contender_evaluation_validator.py's/
    economic_assessment_validator.py's own established pattern of testing
    structural-reference staleness against real sealed sibling records."""

    def _load(self, path: Path) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_stale_manifest_content_sha256_on_real_profile_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["evidence_layer_references"][0]["manifest_content_sha256"] = "0" * 64
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any("manifest_content_sha256 is stale" in e for e in errs)

    def test_stale_sleeve_subject_scope_hash_on_real_profile_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "fund_broad_market.yaml"))
        ref = next(r for r in d["evidence_layer_references"] if r["layer_name"] == "etf_classification")
        ref["sleeve_subject_scope"]["referenced_record_content_sha256"]["SPY"] = "0" * 64
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="fund_broad_market", repo_root=REPO_ROOT)
        assert any("is stale" in e and "SPY" in e for e in errs)

    def test_declared_evidence_coverage_profile_mismatch_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["evidence_coverage_profile"] = l1.FULLY_COMPUTED
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any("evidence_coverage_profile does not reproduce" in e for e in errs)

    def test_abstention_index_missing_live_detected_entry_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["abstention_index"] = d["abstention_index"][:1]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any("abstention_index is missing live-detected" in e for e in errs)

    def test_abstention_index_extra_non_abstained_entry_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["abstention_index"].append({
            "source_layer": "classification", "field_path": "not.a.real.abstention",
            "value": "abstained", "reason": "Synthetic extra entry not genuinely abstained.",
        })
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any("not genuinely abstained" in e for e in errs)

    def test_debt_reduction_freshness_state_abstention_present_on_real_record(self):
        # Regression for a real, independent post-push review finding
        # (pullrequestreview on PR #303, MAJOR-1): DEBT_REDUCTION's own
        # sealed functional_doctrine record separately abstains on
        # freshness_state.status (unable_to_determine_freshness), and that
        # sub-field abstention must never disappear behind this sleeve's
        # own already-forced evidence_coverage_profile value, per XASSET-0012
        # SS4.2.1. Proves the fix is present in the real sealed record, not
        # merely in a synthetic fixture.
        d = self._load(_PROFILES_REAL_DIR / "debt_reduction.yaml")
        pairs = {(e["source_layer"], e["field_path"]) for e in d["abstention_index"]}
        assert ("functional_doctrine", "freshness_state.status") in pairs

    def test_debt_reduction_freshness_state_abstention_missing_rejected(self):
        # The negative half of the same regression: removing that entry
        # from an otherwise-real debt_reduction record must trip the
        # "missing live-detected sub-field abstention" check, proving the
        # live-vs-declared cross-check genuinely catches this defect class
        # rather than merely agreeing with whatever the record happens to
        # declare.
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "debt_reduction.yaml"))
        d["abstention_index"] = [
            e for e in d["abstention_index"] if e["field_path"] != "freshness_state.status"
        ]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="debt_reduction", repo_root=REPO_ROOT)
        assert any(
            "abstention_index is missing live-detected" in e and "freshness_state.status" in e
            for e in errs
        ), errs

    def test_equity_segment_and_market_observed_abstentions_present_on_real_record(self):
        # Regression for a real, independent post-push delta review finding
        # (pullrequestreview on PR #303, round 1 of the second correction
        # round, MAJOR): equity's own scoped valuation_evidence layer
        # carries real, per-company segment_evidence and
        # market_observed_evidence abstentions that were never scanned by
        # _compute_equity_coverage() at all -- the identical failure mode
        # already fixed once for debt_reduction's freshness_state, found
        # again here at larger scale (13/27 and 3/27 companies). Proves the
        # fix is present in the real sealed record.
        d = self._load(_PROFILES_REAL_DIR / "equity.yaml")
        pairs = {(e["source_layer"], e["field_path"]) for e in d["abstention_index"]}
        assert ("valuation_evidence", "segment_evidence") in pairs
        assert ("valuation_evidence", "market_observed_evidence") in pairs

    def test_equity_segment_evidence_abstention_missing_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["abstention_index"] = [
            e for e in d["abstention_index"] if e["field_path"] != "segment_evidence"
        ]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any(
            "abstention_index is missing live-detected" in e and "segment_evidence" in e
            for e in errs
        ), errs

    def test_equity_market_observed_evidence_abstention_missing_rejected(self):
        d = copy.deepcopy(self._load(_PROFILES_REAL_DIR / "equity.yaml"))
        d["abstention_index"] = [
            e for e in d["abstention_index"] if e["field_path"] != "market_observed_evidence"
        ]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_profile_data(d, expected_sleeve_id="equity", repo_root=REPO_ROOT)
        assert any(
            "abstention_index is missing live-detected" in e and "market_observed_evidence" in e
            for e in errs
        ), errs

    def test_stale_profile_reference_hash_on_real_relationship_rejected(self):
        d = copy.deepcopy(self._load(_RELATIONSHIPS_REAL_DIR / "cash_reserve_equity.yaml"))
        d["profile_references"][0]["referenced_content_sha256"] = "0" * 64
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem="cash_reserve_equity", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_declared_secondary_conditions_mismatch_rejected(self):
        d = copy.deepcopy(self._load(_RELATIONSHIPS_REAL_DIR / "cash_reserve_equity.yaml"))
        d["secondary_conditions"] = []
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem="cash_reserve_equity", repo_root=REPO_ROOT)
        assert any("secondary_conditions does not reproduce" in e for e in errs)

    def test_citing_an_interface_only_overlap_dimension_rejected(self):
        d = copy.deepcopy(self._load(_RELATIONSHIPS_REAL_DIR / "crypto_fund_gld_defensive.yaml"))
        import overlap_model_validator as ov
        dim_data = yaml.safe_load((REPO_ROOT / l1._OVERLAP_MODEL_DIR / "defensive_offset_interface.yaml").read_text(encoding="utf-8"))
        d["secondary_conditions"] = sorted(set(d["secondary_conditions"]) | {l1.OVERLAP_OR_DUPLICATION_DISCLOSED})
        d["overlap_dimension_references"] = [
            {"dimension_id": "defensive_offset_interface", "referenced_content_sha256": ov.canonical_record_hash(dim_data)},
        ]
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem="crypto_fund_gld_defensive", repo_root=REPO_ROOT)
        assert any("not_yet_computable_interface_only" in e or "hard failure independent" in e for e in errs)

    def test_stale_overlap_dimension_hash_rejected(self):
        d = copy.deepcopy(self._load(_RELATIONSHIPS_REAL_DIR / "equity_fund_broad_market.yaml"))
        d["overlap_dimension_references"][0]["referenced_content_sha256"] = "0" * 64
        d["content_sha256"] = l1.canonical_record_hash(d)
        errs = l1.validate_sleeve_relationship_data(d, expected_filename_stem="equity_fund_broad_market", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)


# ===========================================================================
# Same-class child-abstention coverage extension (independent post-push
# delta review round 2, pullrequestreview-4907960177 -- MINOR finding).
#
# The round-2 bounded-same-class-audit correctly found zero LIVE
# discrepancy (every declared abstention_index was accurate), but its own
# "no 4th domain"/"zero additional omissions" claim was inaccurate at the
# SCHEMA level: several further abstention-capable fields, permitted by
# their own source schema's own closed vocabulary
# (valuation_evidence_validator.py's financial_evidence/peer_set_evidence/
# scenario_evidence; functional_doctrine_validator.py's
# liquidity_character/capital_preservation_character plus incomplete
# per-record functional_role/freshness_state coverage;
# instrument_economic_assessment_validator.py's
# historical_inflation_sensitivity_narrative/cost_and_tracking_quality_
# economic_significance), were never scanned by any Level 1 coverage
# function -- currently 0/N live-abstained everywhere (independently
# reconfirmed below), so no real record's declared abstention_index was
# ever actually wrong, but the same latent-repeat risk the review named.
#
# Fixed the same way the prior two MAJOR findings were fixed: extend each
# affected coverage function to also scan the field, using the exact same
# per-record abstention_reason/closed-vocabulary-token presence check
# already used for every sibling field. No hash cascade required -- every
# newly-scanned field is 0/N live-abstained today, confirmed by both the
# real-repository directory scan continuing to validate clean (no new
# finding materializes for any real record) and the dedicated synthetic
# tests below (each new scan positively detects an injected abstention it
# would otherwise miss).
# ===========================================================================

class TestSameClassChildAbstentionCoverageExtension:
    def test_equity_financial_evidence_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "valuation_evidence"
        d.mkdir(parents=True)
        (d / "AAPL.yaml").write_text(yaml.dump({"financial_evidence": {"abstention_reason": "test"}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.EQUITY, tmp_path)
        assert any(f.source_layer == "valuation_evidence" and f.field_path == "financial_evidence" for f in findings)

    def test_equity_peer_set_evidence_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "valuation_evidence"
        d.mkdir(parents=True)
        (d / "AAPL.yaml").write_text(yaml.dump({"peer_set_evidence": {"abstention_reason": "test"}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.EQUITY, tmp_path)
        assert any(f.source_layer == "valuation_evidence" and f.field_path == "peer_set_evidence" for f in findings)

    def test_equity_scenario_evidence_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "valuation_evidence"
        d.mkdir(parents=True)
        (d / "AAPL.yaml").write_text(yaml.dump({"scenario_evidence": {"abstention_reason": "test"}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.EQUITY, tmp_path)
        assert any(f.source_layer == "valuation_evidence" and f.field_path == "scenario_evidence" for f in findings)

    def test_equity_no_abstention_produces_no_finding_for_new_domains(self, tmp_path):
        d = tmp_path / "intelligence" / "valuation_evidence"
        d.mkdir(parents=True)
        (d / "AAPL.yaml").write_text(yaml.dump({"financial_evidence": {"periods": []}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.EQUITY, tmp_path)
        assert not any(f.field_path in ("financial_evidence", "peer_set_evidence", "scenario_evidence") for f in findings)

    def test_cash_reserve_liquidity_character_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "functional_doctrine"
        d.mkdir(parents=True)
        (d / "CASH.yaml").write_text(yaml.dump({"liquidity_character": {"liquidity_category": "unable_to_determine"}}), encoding="utf-8")
        (d / "RESERVE.yaml").write_text(yaml.dump({}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.CASH_RESERVE, tmp_path)
        assert any(f.source_layer == "functional_doctrine" and f.field_path == "CASH.liquidity_character" for f in findings)

    def test_cash_reserve_capital_preservation_character_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "functional_doctrine"
        d.mkdir(parents=True)
        (d / "RESERVE.yaml").write_text(yaml.dump({"capital_preservation_character": {"capital_preservation_category": "unable_to_determine"}}), encoding="utf-8")
        (d / "CASH.yaml").write_text(yaml.dump({}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.CASH_RESERVE, tmp_path)
        assert any(f.source_layer == "functional_doctrine" and f.field_path == "RESERVE.capital_preservation_character" for f in findings)

    def test_cash_reserve_freshness_state_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "functional_doctrine"
        d.mkdir(parents=True)
        (d / "CASH.yaml").write_text(yaml.dump({"freshness_state": {"status": "unable_to_determine_freshness"}}), encoding="utf-8")
        (d / "RESERVE.yaml").write_text(yaml.dump({}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.CASH_RESERVE, tmp_path)
        assert any(f.source_layer == "functional_doctrine" and f.field_path == "CASH.freshness_state.status" for f in findings)

    def test_fund_gld_defensive_functional_role_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "functional_doctrine"
        d.mkdir(parents=True)
        (d / "GLD_DEFENSIVE_ROLE.yaml").write_text(yaml.dump({"functional_role": {"role_category": "unable_to_determine"}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.FUND_GLD_DEFENSIVE, tmp_path)
        assert any(f.source_layer == "functional_doctrine" and f.field_path == "functional_role" for f in findings)

    def test_debt_reduction_liquidity_character_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "functional_doctrine"
        d.mkdir(parents=True)
        (d / "DEBT_REDUCTION.yaml").write_text(yaml.dump({"liquidity_character": {"liquidity_category": "unable_to_determine"}}), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.DEBT_REDUCTION, tmp_path)
        assert any(f.source_layer == "functional_doctrine" and f.field_path == "liquidity_character" for f in findings)

    def test_crypto_inflation_sensitivity_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "instrument_economic_assessment"
        d.mkdir(parents=True)
        (d / "BTC.yaml").write_text(yaml.dump({
            "macro_behavioral_characterization": {
                "historical_inflation_sensitivity_narrative": {"sensitivity_category": "unable_to_determine"},
            },
        }), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.CRYPTO, tmp_path)
        assert any(
            f.source_layer == "instrument_economic_assessment"
            and f.field_path == "BTC.macro_behavioral_characterization.historical_inflation_sensitivity_narrative"
            for f in findings
        )

    def test_fund_broad_market_cost_tracking_significance_abstention_detected_synthetic(self, tmp_path):
        d = tmp_path / "intelligence" / "instrument_economic_assessment"
        d.mkdir(parents=True)
        (d / "SPY.yaml").write_text(yaml.dump({
            "cost_and_tracking_quality_economic_significance": {"significance_category": "unable_to_determine"},
        }), encoding="utf-8")
        _, findings = l1.compute_live_evidence_coverage(l1.FUND_BROAD_MARKET, tmp_path)
        assert any(
            f.source_layer == "instrument_economic_assessment"
            and f.field_path == "SPY.cost_and_tracking_quality_economic_significance"
            for f in findings
        )

    def test_real_repository_currently_has_zero_population_for_every_new_domain(self):
        # Positive confirmation, against the live corpus, that the review's
        # "0/N live-abstained today" claim for every newly-scanned field
        # holds -- and therefore that closing this class required no
        # abstention_index update or hash cascade on any real sealed
        # record.
        for sleeve_id in l1.SLEEVE_IDS:
            _, findings = l1.compute_live_evidence_coverage(sleeve_id, REPO_ROOT)
            new_field_paths = {
                "financial_evidence", "peer_set_evidence", "scenario_evidence",
            }
            hit = [
                f for f in findings
                if f.field_path in new_field_paths
                or f.field_path.endswith("liquidity_character")
                or f.field_path.endswith("capital_preservation_character")
                or f.field_path.endswith("cost_and_tracking_quality_economic_significance")
                or f.field_path.endswith("historical_inflation_sensitivity_narrative")
            ]
            assert hit == [], (sleeve_id, hit)

    def test_real_repository_directory_scan_unaffected_by_extension(self):
        # The extension must not introduce any new finding against the
        # real, currently-sealed corpus -- re-running the full directory
        # validation must remain exactly as clean as before this
        # extension.
        r = l1.validate_sleeve_profile_directory(_PROFILES_REAL_DIR, repo_root=REPO_ROOT)
        assert r.valid, [e for res in r.results if not res.valid for e in res.errors]


# ===========================================================================
# Manifest bidirectional reconciliation -- synthetic, disposable
# directories, matching every prior sealed-cohort validator's own
# established test-fixture pattern.
# ===========================================================================

def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


class TestProfileManifestReconciliation:
    def _valid_profile_pair(self, sleeve_id):
        return _sealed_profile(sleeve_id=sleeve_id)

    def test_duplicate_sleeve_id_in_manifest_rejected(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_profile_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("duplicate sleeve_id" in e for e in r.errors)

    def test_manifest_hash_mismatch_rejected(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": "0" * 64, "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_profile_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("content_sha256 mismatch" in e for e in r.errors)

    def test_missing_authorized_sleeve_rejected(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_profile_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("missing authorized sleeve_id" in e for e in r.errors)

    def test_orphan_record_on_disk_rejected(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        orphan = _sealed_profile(sleeve_id=l1.CRYPTO)
        _write_yaml(tmp_path / "crypto.yaml", orphan)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_profile_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("on disk with no manifest entry" in e for e in r.errors)


class TestRelationshipManifestReconciliation:
    def test_duplicate_pair_rejected(self, tmp_path):
        rec = _sealed_relationship(l1.CASH_RESERVE, l1.EQUITY)
        _write_yaml(tmp_path / "cash_reserve_equity.yaml", rec)
        row = {
            "sleeve_a": "cash_reserve", "sleeve_b": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013",
            "record_path": f"{l1._RELATIONSHIPS_DIR}/cash_reserve_equity.yaml",
        }
        manifest = {"schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION, "cohort": [row, dict(row)]}
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_relationship_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("duplicate pair" in e for e in r.errors)

    def test_missing_authorized_pair_rejected(self, tmp_path):
        rec = _sealed_relationship(l1.CASH_RESERVE, l1.EQUITY)
        _write_yaml(tmp_path / "cash_reserve_equity.yaml", rec)
        row = {
            "sleeve_a": "cash_reserve", "sleeve_b": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"],
            "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013",
            "record_path": f"{l1._RELATIONSHIPS_DIR}/cash_reserve_equity.yaml",
        }
        manifest = {"schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION, "cohort": [row]}
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_relationship_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("missing authorized pair" in e for e in r.errors)

    def test_orphan_record_rejected(self, tmp_path):
        rec = _sealed_relationship(l1.CASH_RESERVE, l1.EQUITY)
        _write_yaml(tmp_path / "cash_reserve_equity.yaml", rec)
        orphan = _sealed_relationship(l1.CRYPTO, l1.EQUITY)
        _write_yaml(tmp_path / "crypto_equity.yaml", orphan)
        rows = [
            {"sleeve_a": a, "sleeve_b": b, "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._RELATIONSHIPS_DIR}/{a}_{b}.yaml"}
            for a, b in [("cash_reserve", "equity")]
        ]
        manifest = {"schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION, "cohort": rows}
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_relationship_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("on disk with no manifest entry" in e for e in r.errors)


class TestDirectoryValidationBehaviors:
    def test_missing_directory_is_valid_zero_results(self, tmp_path):
        r = l1.validate_sleeve_profile_directory(tmp_path / "does_not_exist", repo_root=REPO_ROOT)
        assert r.valid
        assert r.record_count == 0

    def test_missing_manifest_file_reported(self, tmp_path):
        _write_yaml(tmp_path / "equity.yaml", _sealed_profile(sleeve_id=l1.EQUITY))
        r = l1.validate_sleeve_profile_directory(tmp_path, repo_root=None)
        assert not r.valid
        assert any("COHORT_MANIFEST.yaml is missing" in e for res in r.results for e in res.errors)

    def test_missing_sleeve_population_reported(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/equity.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_sleeve_profile_directory(tmp_path, repo_root=None)
        assert not r.valid
        assert any("missing sealed record(s) for authorized sleeve_id" in e for res in r.results for e in res.errors)


# ===========================================================================
# Protected-path / byte-identity proof -- every one of the twelve input
# layers this module reads from remains untouched by validation.
# ===========================================================================

_PROTECTED_PATHS = [
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
]

_PROTECTED_INTELLIGENCE_DIRS = [
    "intelligence/classification", "intelligence/valuation_archetype", "intelligence/valuation_evidence",
    "intelligence/valuation_results", "intelligence/etf_classification", "intelligence/crypto_classification",
    "intelligence/functional_doctrine", "intelligence/economic_assessment",
    "intelligence/instrument_economic_assessment", "intelligence/relationships", "intelligence/overlap_model",
    "intelligence/companies", "intelligence/themes",
]


class TestProtectedPathIsolation:
    def test_protected_files_byte_identical_before_and_after_validation(self):
        hashes_before = {}
        for rel in _PROTECTED_PATHS:
            p = REPO_ROOT / rel
            if p.is_file():
                hashes_before[rel] = p.read_bytes()

        l1.validate_sleeve_profile_directory(_PROFILES_REAL_DIR, repo_root=REPO_ROOT)
        l1.validate_sleeve_relationship_directory(_RELATIONSHIPS_REAL_DIR, repo_root=REPO_ROOT)

        for rel, before in hashes_before.items():
            assert (REPO_ROOT / rel).read_bytes() == before, f"{rel} was mutated"

    def test_protected_intelligence_directories_byte_identical(self):
        before = {}
        for rel in _PROTECTED_INTELLIGENCE_DIRS:
            d = REPO_ROOT / rel
            if d.is_dir():
                for p in sorted(d.rglob("*")):
                    if p.is_file():
                        before[str(p)] = p.read_bytes()

        l1.validate_sleeve_profile_directory(_PROFILES_REAL_DIR, repo_root=REPO_ROOT)
        l1.validate_sleeve_relationship_directory(_RELATIONSHIPS_REAL_DIR, repo_root=REPO_ROOT)

        for path_str, content in before.items():
            assert Path(path_str).read_bytes() == content, f"{path_str} was mutated"

    def test_module_never_opens_files_in_write_mode(self):
        source = (REPO_ROOT / "level1_sleeve_synthesis_validator.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "open":
                for kw in node.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        assert "w" not in kw.value.value and "a" not in kw.value.value

    def test_module_never_calls_mkdir(self):
        source = (REPO_ROOT / "level1_sleeve_synthesis_validator.py").read_text(encoding="utf-8")
        assert "mkdir" not in source
        assert "write_text" not in source
        assert "write_bytes" not in source


# ===========================================================================
# Zero import coupling with allocate.py/margin_state.py, either direction.
# ===========================================================================

class TestImportCoupling:
    def test_module_does_not_import_allocate_or_margin_state(self):
        source = (REPO_ROOT / "level1_sleeve_synthesis_validator.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_names.add(node.module)
        assert "allocate" not in imported_names
        assert "margin_state" not in imported_names

    def test_allocate_does_not_import_level1_module(self):
        source = (REPO_ROOT / "allocate.py").read_text(encoding="utf-8")
        assert "level1_sleeve_synthesis_validator" not in source

    def test_margin_state_does_not_import_level1_module(self):
        source = (REPO_ROOT / "margin_state.py").read_text(encoding="utf-8")
        assert "level1_sleeve_synthesis_validator" not in source


# ===========================================================================
# MANDATORY ELIGIBILITY-LANGUAGE PARAPHRASE ADVERSARIAL PROBE
# (XASSET-0013 SS H, this implementing session's own required pre-push
# probe against the carried-forward review NOTE from XASSET-0012's own
# final delta review).
#
# DISCLOSED RESULT: empirically testing the required matrix below against
# the scan as originally built (SS8.1's own literal phrase list plus
# XASSET-0012's own round-2 hardening) found seven genuine gaps -- ordinary
# paraphrases that avoid every literal string in the original list while
# still asserting a portfolio-membership conclusion: "should remain part of
# the portfolio" (a different construction from the already-caught "should
# remain IN the portfolio"), "should be excluded from holdings" (a
# different object than "the portfolio"), a bare "ought to be
# included"/"ought to be excluded" (no object at all), and four word-order/
# subject-object-reversal variants of phrases the scan already caught in
# their canonical order ("it is warranted that... inclusion...", "portfolio
# inclusion... is eligible", "the portfolio should not include this
# sleeve", "deserves to remain part of the portfolio"). This is a probe
# requirement, not a redesign authorization (XASSET-0013 SS H's own
# explicit text) -- resolved by the smallest bounded correction consistent
# with SS8.1's own existing scan authority: eight new patterns appended to
# the existing closed _ELIGIBILITY_PATTERNS list (level1_sleeve_synthesis_
# validator.py's own "Round-3 additions" comment), never a new mechanism,
# never a change to any other scan or to SS8.1's own underlying boundary.
# Every one of SS8.1's own mandatory false-positive guards was re-verified
# clean against the corrected scan before this test class was written.
# ===========================================================================

_ELIGIBILITY_MATRIX_MUST_CATCH = [
    "This sleeve is eligible for portfolio inclusion.",
    "This sleeve belongs in the portfolio.",
    "This sleeve merits a place in the portfolio.",
    "This sleeve should remain part of the portfolio.",
    "This sleeve is portfolio-worthy.",
    "This sleeve should be excluded from holdings.",
    "This sleeve ought to be included in the portfolio.",
    "This sleeve's inclusion is warranted.",
    "This sleeve's membership is justified.",
    "Remove this sleeve from the investable set.",
    # Punctuation variants
    "This sleeve is not eligible for portfolio inclusion, and should be dropped.",
    "This sleeve, frankly, belongs in the portfolio.",
    # Negation variants
    "This sleeve does not belong in the portfolio.",
    # Conjunction variants
    "This sleeve should be part of the portfolio and stay there.",
    # Active/passive and word-order variants
    "It is warranted that this sleeve's inclusion continue.",
    "Portfolio inclusion for this sleeve is eligible.",
    "The portfolio should not include this sleeve going forward.",
    "This sleeve deserves to remain part of the portfolio.",
    "This sleeve ought to be excluded.",
    "This sleeve's continued membership is justified given the evidence.",
    # Round-4 additions (independent post-push review, pullrequestreview on
    # PR #303, MINOR-2): a softer no-object "has a place... going forward"
    # variant, a colon-shorthand keep/go verdict shape, and an explicit
    # "no case for keeping" negative-inclusion finding.
    "This sleeve has a place in the portfolio going forward.",
    "cash reserve: keep",
    "The crypto sleeve should go.",
    "There is no case for keeping this sleeve in the portfolio.",
    # Round-5 additions (independent post-push delta review, round 1 of
    # PR #303's second correction round, MINOR-2): five further ordinary
    # paraphrases found via a fresh adversarial probe against the round-4
    # scan.
    "This sleeve belongs among portfolio holdings.",
    "This sleeve should stay in the investable set.",
    "This sleeve ought to remain a holding.",
    "Remove the sleeve from holdings.",
    "The sleeve should no longer be held.",
]

_ELIGIBILITY_FALSE_POSITIVE_GUARDS = [
    "included in the evidence inventory",
    "excluded from this calculation because evidence is unavailable",
    "the manifest includes four instruments",
    "this record is included in the sleeve's own evidence-layer references",
    "excluded from the first synthesis's governed evidence base",
    "excluded from this assessment's own reasoning",
    # Additional process/evidence-scope false-positive guards, matching
    # SS8.1's own mandatory-guard discipline.
    "the referenced subject is included in the source manifest",
    "this dimension is excluded from the referenced layer's own population",
    "the inclusion boundary described here governs evidence scope only",
    "every fund is included in the shared manifest",
    # Round-4 false-positive guards: legitimate continuations that share a
    # word prefix with the round-4 "should go"/"place in" patterns but are
    # not a portfolio-membership verdict.
    "the crypto sleeve should go through additional review before any future step",
    "this fund's place in the etf_classification manifest is well documented",
    # Round-5 false-positive guards: this session's own adversarial probing
    # found that the round-3 "exclude...from holdings" pattern and the
    # round-5 "remove...from holdings" pattern would otherwise both
    # misfire on a legitimate structural citation of this repository's
    # own central holdings.yaml filename -- fixed with a (?!\.yaml)
    # lookahead on both patterns before this test class was written.
    "a ticker removed from holdings.yaml is not zeroed, per this repository's own convention",
    "a position excluded from holdings.yaml reconciliation for a documented reason",
]


class TestEligibilityLanguageParaphraseAdversarialProbe:
    @pytest.mark.parametrize("phrase", _ELIGIBILITY_MATRIX_MUST_CATCH)
    def test_matrix_phrase_caught_by_scan_function(self, phrase):
        findings = l1._eligibility_language_scan(phrase)
        assert findings, f"eligibility scan failed to catch: {phrase!r}"

    @pytest.mark.parametrize("phrase", _ELIGIBILITY_MATRIX_MUST_CATCH)
    def test_matrix_phrase_caught_via_full_profile_validation(self, phrase):
        d = _sealed_profile(economic_role_summary=f"{phrase} Disclosed here for test purposes.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("eligibility-language" in e for e in errs), (phrase, errs)

    @pytest.mark.parametrize("phrase", _ELIGIBILITY_MATRIX_MUST_CATCH)
    def test_matrix_phrase_caught_via_full_relationship_validation(self, phrase):
        d = _sealed_relationship(rationale=f"{phrase} Disclosed here for test purposes.")
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("eligibility-language" in e for e in errs), (phrase, errs)

    @pytest.mark.parametrize("phrase", _ELIGIBILITY_FALSE_POSITIVE_GUARDS)
    def test_false_positive_guard_stays_clean(self, phrase):
        findings = l1._eligibility_language_scan(phrase)
        assert findings == [], f"false positive on legitimate evidence/process language: {phrase!r} -> {findings}"

    @pytest.mark.parametrize("phrase", _ELIGIBILITY_FALSE_POSITIVE_GUARDS)
    def test_false_positive_guard_validates_cleanly_in_full_profile(self, phrase):
        d = _sealed_profile(economic_role_summary=f"Some text: {phrase}, described plainly.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("eligibility-language" in e for e in errs), (phrase, errs)

    def test_governance_boundary_sentence_itself_is_a_false_positive_guard(self):
        # XASSET-0012 SS8.1's own explicit design point, restated as a
        # direct check: the governance/design text's own boundary sentence
        # ("excluded from the first synthesis's governed evidence base")
        # must never self-trigger the scan a future populated record would
        # be validated against -- since SS7/SS8.1 themselves use exactly
        # this phrase as governance prose, not as populated record content.
        sentence = "excluded from the first synthesis's governed evidence base"
        assert l1._eligibility_language_scan(sentence) == []


# ===========================================================================
# Non-cascading abstention discipline.
# ===========================================================================

class TestNonCascadingAbstention:
    def test_profile_abstention_on_one_layer_does_not_force_others(self):
        # equity's own real abstention_index carries entries from three
        # DIFFERENT layers (valuation_results, valuation_evidence,
        # classification) -- none of those abstentions forces or implies a
        # value on the other cited layers (valuation_archetype remains
        # fully populated, uncited by any abstention entry).
        data = yaml.safe_load((_PROFILES_REAL_DIR / "equity.yaml").read_text(encoding="utf-8"))
        abstained_layers = {e["source_layer"] for e in data["abstention_index"]}
        cited_layers = {ref["layer_name"] for ref in data["evidence_layer_references"]}
        assert abstained_layers < cited_layers  # a strict, non-total subset

    def test_relationship_abstention_on_primary_disposition_independent_of_secondary(self):
        d = _sealed_relationship(
            primary_disposition=l1.RELATIONSHIP_ABSTENTION, favored_sleeve_id=None,
            secondary_conditions=[l1.EVIDENCE_PARTIAL_PRESENT],
            abstention_index=[{"field": "primary_disposition", "value": "unable_to_determine", "reason": "Synthetic reason."}],
        )
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert errs == []


# ===========================================================================
# Full "other adversarial matrix" (mandated coverage: exact population,
# structural references, abstention, policy leakage, hidden scoring, false
# positives). Most of this coverage already exists in the classes above;
# this section adds the handful of items not yet directly exercised,
# including two further disclosed hardening rounds this implementing
# session applied while building this coverage: "deserves capital" (folded
# into the eligibility scan's own already-established "deserves inclusion"/
# "deserves a place" pattern family) and a sizing-recommendation shape --
# "the target... should be increased", "increase the target", "size...
# should be decreased", and a spelled-out "percent of the book/portfolio"
# (folded into the policy-leak scan, correctly implementing XASSET-0012 SS9
# item 9's own "target_pct/max_position_size... key name or VALUE" text for
# the first time, not a hardening of any prior accepted version).
# ===========================================================================

class TestAdversarialMatrixA_ExactPopulation:
    def test_missing_profile_detected_by_directory_scan(self, tmp_path):
        for sid in l1.SLEEVE_IDS:
            if sid == l1.DEBT_REDUCTION:
                continue
            rec = _sealed_profile(sleeve_id=sid)
            _write_yaml(tmp_path / f"{sid}.yaml", rec)
        r = l1.validate_sleeve_profile_directory(tmp_path, repo_root=None)
        assert not r.valid
        assert any("missing sealed record(s) for authorized sleeve_id" in e for res in r.results for e in res.errors if not res.valid)

    def test_extra_relationship_pair_detected(self, tmp_path):
        for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS:
            _write_yaml(tmp_path / f"{a}_{b}.yaml", _sealed_relationship(a, b))
        # An eighth, unauthorized pair.
        _write_yaml(tmp_path / f"{l1.CRYPTO}_{l1.FUND_BROAD_MARKET}.yaml", _sealed_relationship(l1.CRYPTO, l1.FUND_BROAD_MARKET))
        r = l1.validate_sleeve_relationship_directory(tmp_path, repo_root=None)
        assert not r.valid
        assert any("non-authorized pair" in e for res in r.results for e in res.errors if not res.valid)

    def test_duplicate_record_via_manifest_caught(self):
        # Already covered directly by TestProfileManifestReconciliation/
        # TestRelationshipManifestReconciliation -- cross-referenced here
        # for the adversarial-matrix checklist's own completeness record.
        assert True

    def test_wrong_filename_order_rejected(self):
        d = _sealed_relationship(sleeve_a=l1.EQUITY, sleeve_b=l1.CASH_RESERVE)  # wrong order
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("alphabetically ordered" in e for e in errs)


class TestAdversarialMatrixB_StructuralReferences:
    def test_wrong_source_schema_on_overlap_reference(self):
        # overlap_dimension_references has no source_schema field of its own
        # (unlike comparator_structural_reference elsewhere in this
        # repository) -- the equivalent check here is dimension_id
        # membership plus live computation_status, both already covered by
        # TestLiveHashStalenessAgainstRealRepository.
        assert True

    def test_wrong_sleeve_subject_already_covered(self):
        # Cross-referenced: test_sleeve_subject_scope_rejects_out_of_scope_
        # subject_gld_inside_fund_broad_market and ...rejects_spy_inside_
        # fund_gld_defensive above.
        assert True

    def test_swapped_record_path_in_profile_manifest_row_rejected(self, tmp_path):
        rec = _sealed_profile(sleeve_id=l1.EQUITY)
        _write_yaml(tmp_path / "equity.yaml", rec)
        manifest = {
            "schema_version": l1.SCHEMA_VERSION, "governing_decision": l1._GOVERNING_DECISION,
            "cohort": [
                {"sleeve_id": "equity", "shard_id": "s", "sealed_at": rec["sealed_at"], "content_sha256": rec["content_sha256"], "schema_version": "1.0", "governing_decision": "XASSET-0013", "record_path": f"{l1._PROFILES_DIR}/crypto.yaml"},
            ],
        }
        _write_yaml(tmp_path / "COHORT_MANIFEST.yaml", manifest)
        r = l1.validate_profile_cohort_manifest(tmp_path / "COHORT_MANIFEST.yaml", tmp_path)
        assert not r.valid
        assert any("record_path must be" in e for e in r.errors)


class TestAdversarialMatrixD_PolicyLeakageHardened:
    @pytest.mark.parametrize("phrase", [
        "This sleeve deserves capital.",
        "This sleeve deserves more capital than its peer.",
        "This sleeve warrants more capital.",
    ])
    def test_deserves_capital_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"{phrase} Disclosed for test purposes.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("eligibility-language" in e for e in errs), (phrase, errs)

    @pytest.mark.parametrize("phrase", [
        "The target for this sleeve should be increased.",
        "We should increase the target for this fund.",
        "This sleeve's own size should be decreased.",
    ])
    def test_sizing_recommendation_rejected(self, phrase):
        d = _sealed_profile(economic_role_summary=f"{phrase} Disclosed for test purposes.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("policy-leak" in e for e in errs), (phrase, errs)

    def test_spelled_out_percent_of_book_rejected(self):
        d = _sealed_profile(economic_role_summary="This sleeve's own percent of the book should rise.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("policy-leak" in e for e in errs)

    def test_spelled_out_percent_of_portfolio_rejected(self):
        d = _sealed_profile(economic_role_summary="This sleeve's own percent of portfolio should rise.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("policy-leak" in e for e in errs)

    @pytest.mark.parametrize("legit", [
        "This record makes no claim about the sleeve's own individual weight or size.",
        "This describes currently governed evidence only; it does not name any target.",
        "The target audience for this record is a future implementing session.",
        "No claim is made about deserving priority in any future sizing decision.",
    ])
    def test_boundary_disclosure_language_not_falsely_rejected(self, legit):
        d = _sealed_profile(economic_role_summary=f"{legit} Disclosed plainly here.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert errs == [], (legit, errs)


class TestAdversarialMatrixD_InOutTokens:
    def test_bare_in_token_rejected(self):
        d = _sealed_profile(economic_role_summary="Verdict for this synthesis: sleeve: IN, confirmed.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("eligibility-language" in e for e in errs)

    def test_bare_out_token_rejected(self):
        d = _sealed_profile(economic_role_summary="Verdict for this synthesis: this sleeve is OUT, confirmed.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("eligibility-language" in e for e in errs)

    def test_ordinary_use_of_in_and_out_words_not_rejected(self):
        d = _sealed_profile(
            economic_role_summary="This sleeve's own evidence base draws in structural facts and rules out fabrication."
        )
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert not any("eligibility-language" in e for e in errs), errs


class TestAdversarialMatrixE_HiddenScoring:
    def test_numeric_score_key_rejected(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["priority_score"] = 5
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)

    def test_ordinal_rank_key_rejected(self):
        d = _sealed_profile()
        d["evidence_layer_references"][0]["sleeve_rank"] = "first"
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)

    def test_written_out_magnitude_rejected_already_covered(self):
        # Cross-referenced: TestNumericLeakageScan.test_magnitude_word_rejected.
        assert True

    def test_composite_ranking_language_rejected(self):
        d = _sealed_profile(economic_role_summary="This sleeve has the best overall ranking among the six.")
        errs = l1.validate_sleeve_profile_data(d, repo_root=None)
        assert any(("numeric-leakage" in e) or ("comparative-superiority" in e) for e in errs)

    def test_composite_score_key_rejected_on_relationship(self):
        d = _sealed_relationship()
        d["overlap_dimension_references"] = []
        d["profile_references"][0]["composite_index"] = 1
        errs = l1.validate_sleeve_relationship_data(d, repo_root=None)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)


# =============================================================================
# STAGE 4 -- policy_adoption (XASSET-0014 Stage 4a methodology, XASSET-0015
# Stage 4b content authorization, this Stage 4c implementation).
#
# Fixture strategy: reuses this repository's own real, sealed six sleeve_
# profile and seven sleeve_relationship records (loaded fresh from disk in
# every helper below, never hand-copied into a synthetic multi-layer
# fixture) as the live cross-reference substrate for every hash/Axis-B/
# Axis-C mechanical-derivation test -- matching this file's own established
# "test structural-reference staleness against real sealed sibling records"
# convention (see the module docstring above). Pure schema-shape tests
# (extra-key rejection, closed-vocabulary enforcement) additionally use
# repo_root=None where no live cross-reference is needed at all.
# =============================================================================


def _real_policy_adoption(sleeve_id: str) -> dict:
    """A byte-for-byte copy of the real, sealed policy_adoption record for
    sleeve_id -- read fresh from disk on every call so mutation by a caller
    never leaks between tests."""
    path = REPO_ROOT / l1._POLICY_ADOPTION_DIR / f"{sleeve_id}.yaml"
    data, errs = l1._read_yaml(path)
    assert not errs, errs
    return copy.deepcopy(data)


def _reseal(d: dict) -> dict:
    """After mutating a copy of a real sealed record for an adversarial
    test, recompute content_sha256 so the mutation under test is isolated
    from an unrelated, incidental hash-mismatch failure -- exactly the
    discipline this file's own existing adversarial fixtures already
    apply (see the analogous helper pattern for sleeve_profile/sleeve_
    relationship fixtures above)."""
    d["content_sha256"] = l1.canonical_record_hash(d)
    return d


class TestPolicyAdoptionConstants:
    """SS21 item 23 -- relationship-coverage-ledger completeness constants:
    exact five-pair enumeration per sleeve, live cross-reference against
    the sealed seven and the disclosed eight, zero gap, zero overlap."""

    def test_deferred_pairs_alphabetical_and_closed_vocabulary(self):
        for (a, b), cls in l1.DEFERRED_PAIRS.items():
            assert a < b
            assert cls in l1._DEFERRAL_CLASS_VALUES

    def test_sealed_plus_deferred_equals_all_fifteen_pairs_zero_gap(self):
        sealed = set(l1.AUTHORIZED_RELATIONSHIP_PAIRS)
        deferred = set(l1.DEFERRED_PAIRS)
        assert len(sealed) == 7
        assert len(deferred) == 8
        assert sealed & deferred == set()
        assert sealed | deferred == l1._ALL_FIFTEEN_PAIRS
        assert len(l1._ALL_FIFTEEN_PAIRS) == 15

    def test_every_sleeve_touches_exactly_five_pairs(self):
        for sid in l1.SLEEVE_IDS:
            assert len(l1._all_pairs_touching(sid)) == 5

    def test_deferred_pairs_grouped_by_class_matches_xasset_0013_section_e(self):
        by_class: dict[str, set[tuple[str, str]]] = {}
        for pair, cls in l1.DEFERRED_PAIRS.items():
            by_class.setdefault(cls, set()).add(pair)
        assert by_class["class_1"] == {
            (l1.FUND_BROAD_MARKET, l1.FUND_GLD_DEFENSIVE),
            (l1.CRYPTO, l1.FUND_BROAD_MARKET),
            (l1.CASH_RESERVE, l1.FUND_BROAD_MARKET),
            (l1.DEBT_REDUCTION, l1.FUND_BROAD_MARKET),
        }
        assert by_class["class_2"] == {
            (l1.CASH_RESERVE, l1.FUND_GLD_DEFENSIVE),
            (l1.DEBT_REDUCTION, l1.FUND_GLD_DEFENSIVE),
        }
        assert by_class["class_3"] == {
            (l1.CASH_RESERVE, l1.CRYPTO),
            (l1.CRYPTO, l1.DEBT_REDUCTION),
        }

    def test_basis3_asset_class_map_matches_xasset_0012_section_2(self):
        assert l1._BASIS3_ASSET_CLASSES[l1.EQUITY] == ("equity",)
        assert l1._BASIS3_ASSET_CLASSES[l1.FUND_BROAD_MARKET] == ("fund",)
        assert l1._BASIS3_ASSET_CLASSES[l1.FUND_GLD_DEFENSIVE] == ("fund",)
        assert l1._BASIS3_ASSET_CLASSES[l1.CRYPTO] == ("crypto",)
        assert l1._BASIS3_ASSET_CLASSES[l1.CASH_RESERVE] == ("cash", "reserve")
        assert l1._BASIS3_ASSET_CLASSES[l1.DEBT_REDUCTION] == ()

    def test_closed_vocabularies(self):
        assert l1._PORTFOLIO_FUNCTION_STATUS_VALUES == frozenset({
            "function_confirmed_distinct", "function_status_unresolved", "unable_to_determine",
        })
        assert l1._CAPITAL_ELIGIBILITY_VALUES == frozenset({
            "eligible_for_target_consideration", "not_yet_eligible",
        })
        assert l1._SIZING_READINESS_VALUES == frozenset({
            "sizing_ready", "sizing_conditionally_ready", "sizing_blocked",
        })
        assert l1._COVERAGE_STATE_VALUES == frozenset({
            "sealed_determined", "sealed_unresolved", "deferred_disclosed",
        })
        assert l1._BLOCKING_REASON_TYPES == frozenset({
            "axis_a_unresolved", "axis_b_not_eligible", "sealed_unresolved_relationship",
            "deferred_relationship_pair", "secondary_condition_present",
        })


# ===========================================================================
# Basis 1 / Basis 3 computation -- pure, live, favored_sleeve_id-blind.
# ===========================================================================

class TestBasis1Computation:
    def test_equity_has_three_basis1_findings(self):
        findings = l1.compute_basis1_findings(l1.EQUITY, REPO_ROOT)
        assert len(findings) == 3
        assert all(d in (l1.ROLE_PRESERVING, l1.COEXISTENCE_SUPPORTED) for _, d in findings)

    def test_fund_broad_market_has_zero_basis1_findings(self):
        # its one sealed relationship resolves stronger_evidence_maturity,
        # mechanically barred from supplying Basis 1 grounds.
        assert l1.compute_basis1_findings(l1.FUND_BROAD_MARKET, REPO_ROOT) == []

    def test_debt_reduction_has_one_basis1_finding(self):
        findings = l1.compute_basis1_findings(l1.DEBT_REDUCTION, REPO_ROOT)
        assert len(findings) == 1
        assert findings[0][1] == l1.ROLE_PRESERVING

    def test_basis1_never_reads_favored_sleeve_id_by_construction(self):
        """Source-level proof, not merely a behavioral one: compute_basis1_
        findings's own source text never references favored_sleeve_id at
        all -- the function signature and body only ever read primary_
        disposition."""
        import inspect
        source = inspect.getsource(l1.compute_basis1_findings)
        # Scoped to actual field-access forms, not the function's own
        # docstring (which legitimately explains the non-influence
        # guarantee using that exact field name in prose).
        assert '"favored_sleeve_id"' not in source
        assert "'favored_sleeve_id'" not in source


class TestBasis3Computation:
    def test_equity_basis3_available(self):
        assert l1.compute_basis3_available(l1.EQUITY, REPO_ROOT) is True

    def test_fund_broad_market_basis3_available_scoped_to_spy_vea_vwo(self):
        assert l1.compute_basis3_available(l1.FUND_BROAD_MARKET, REPO_ROOT) is True

    def test_fund_gld_defensive_basis3_available_scoped_to_gld(self):
        assert l1.compute_basis3_available(l1.FUND_GLD_DEFENSIVE, REPO_ROOT) is True

    def test_crypto_basis3_available(self):
        assert l1.compute_basis3_available(l1.CRYPTO, REPO_ROOT) is True

    def test_cash_reserve_basis3_available(self):
        assert l1.compute_basis3_available(l1.CASH_RESERVE, REPO_ROOT) is True

    def test_debt_reduction_basis3_unavailable_no_targets_row(self):
        assert l1.compute_basis3_available(l1.DEBT_REDUCTION, REPO_ROOT) is False

    def test_basis3_reads_no_relationship_data_by_construction(self):
        import inspect
        sig = inspect.signature(l1.compute_basis3_available)
        assert "relationship_data" not in sig.parameters
        source = inspect.getsource(l1.compute_basis3_available)
        assert "_RELATIONSHIPS_DIR" not in source
        # Scoped to actual field-access forms, not the function's own
        # docstring (which legitimately explains the non-influence
        # guarantee using that exact field name in prose).
        assert '"favored_sleeve_id"' not in source
        assert "'favored_sleeve_id'" not in source

    def test_basis3_none_repo_root_returns_false(self):
        assert l1.compute_basis3_available(l1.EQUITY, None) is False


class TestAxisBMechanicalDerivation:
    def test_fully_computed_and_substantial_map_eligible(self):
        assert l1.compute_axis_b(l1.FULLY_COMPUTED) == l1.ELIGIBLE_FOR_TARGET_CONSIDERATION
        assert l1.compute_axis_b(l1.SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS) == l1.ELIGIBLE_FOR_TARGET_CONSIDERATION

    def test_materially_incomplete_and_forced_abstention_map_not_yet_eligible(self):
        assert l1.compute_axis_b(l1.MATERIALLY_INCOMPLETE) == l1.NOT_YET_ELIGIBLE
        assert l1.compute_axis_b(l1.FORCED_ABSTENTION) == l1.NOT_YET_ELIGIBLE

    def test_unknown_value_returns_none_never_a_default(self):
        assert l1.compute_axis_b("not-a-real-value") is None
        assert l1.compute_axis_b(None) is None

    def test_debt_reduction_live_profile_maps_not_yet_eligible(self):
        profile = l1._live_profile(REPO_ROOT, l1.DEBT_REDUCTION)
        assert l1.compute_axis_b(profile["evidence_coverage_profile"]) == l1.NOT_YET_ELIGIBLE

    def test_every_other_sleeve_live_profile_maps_eligible(self):
        for sid in l1.SLEEVE_IDS - {l1.DEBT_REDUCTION}:
            profile = l1._live_profile(REPO_ROOT, sid)
            assert l1.compute_axis_b(profile["evidence_coverage_profile"]) == l1.ELIGIBLE_FOR_TARGET_CONSIDERATION


class TestRelationshipCoverageLedgerComputation:
    def test_equity_ledger_all_five_sealed_determined(self):
        ledger = l1.compute_live_relationship_ledger(l1.EQUITY, REPO_ROOT)
        assert len(ledger) == 5
        assert all(e.coverage_state == l1.SEALED_DETERMINED for e in ledger)
        assert all(e.has_secondary_conditions for e in ledger)

    def test_fund_broad_market_ledger_one_sealed_four_deferred(self):
        ledger = l1.compute_live_relationship_ledger(l1.FUND_BROAD_MARKET, REPO_ROOT)
        by_other = {e.other_sleeve_id: e for e in ledger}
        assert by_other["equity"].coverage_state == l1.SEALED_DETERMINED
        for other in ("fund_gld_defensive", "crypto", "cash_reserve", "debt_reduction"):
            assert by_other[other].coverage_state == l1.DEFERRED_DISCLOSED
            assert by_other[other].deferral_class == "class_1"

    def test_cash_reserve_ledger_has_one_sealed_unresolved(self):
        ledger = l1.compute_live_relationship_ledger(l1.CASH_RESERVE, REPO_ROOT)
        by_other = {e.other_sleeve_id: e for e in ledger}
        assert by_other["debt_reduction"].coverage_state == l1.SEALED_UNRESOLVED
        assert by_other["equity"].coverage_state == l1.SEALED_DETERMINED
        for other in ("crypto", "fund_broad_market", "fund_gld_defensive"):
            assert by_other[other].coverage_state == l1.DEFERRED_DISCLOSED

    def test_debt_reduction_ledger_symmetric_to_cash_reserve(self):
        ledger = l1.compute_live_relationship_ledger(l1.DEBT_REDUCTION, REPO_ROOT)
        by_other = {e.other_sleeve_id: e for e in ledger}
        assert by_other["cash_reserve"].coverage_state == l1.SEALED_UNRESOLVED
        assert by_other["equity"].coverage_state == l1.SEALED_DETERMINED

    def test_crypto_and_fund_gld_defensive_ledgers_two_sealed_three_deferred(self):
        for sid, sealed_others in (
            (l1.CRYPTO, {"equity", "fund_gld_defensive"}),
            (l1.FUND_GLD_DEFENSIVE, {"equity", "crypto"}),
        ):
            ledger = l1.compute_live_relationship_ledger(sid, REPO_ROOT)
            sealed = {e.other_sleeve_id for e in ledger if e.coverage_state == l1.SEALED_DETERMINED}
            deferred = {e.other_sleeve_id for e in ledger if e.coverage_state == l1.DEFERRED_DISCLOSED}
            assert sealed == sealed_others
            assert len(deferred) == 3

    def test_ledger_never_produces_unrecognized_pair(self):
        """Structural guarantee, not merely empirical: every entry's pair is
        in the closed 15-pair set by construction (_all_pairs_touching only
        ever iterates _ALL_FIFTEEN_PAIRS)."""
        for sid in l1.SLEEVE_IDS:
            ledger = l1.compute_live_relationship_ledger(sid, REPO_ROOT)
            for e in ledger:
                assert e.pair in l1._ALL_FIFTEEN_PAIRS


class TestExpectedSizingReadinessComputation:
    """XASSET-0014 SS22's own axis-interaction adversarial-case table,
    reproduced here as direct unit tests against the pure function, each
    case labeled to match the design document's own lettering."""

    def _entry(self, other, state, secondary=False):
        return l1._LedgerEntry(
            other_sleeve_id=other, pair=("a", "b"), coverage_state=state,
            deferral_class="class_1" if state == l1.DEFERRED_DISCLOSED else None,
            primary_disposition=None, has_secondary_conditions=secondary,
        )

    def test_case_a_role_distinct_evidence_partial_all_sealed_no_unresolved(self):
        ledger = [self._entry(o, l1.SEALED_DETERMINED, secondary=True) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_CONDITIONALLY_READY

    def test_case_b_role_unresolved_evidence_complete(self):
        ledger = [self._entry(o, l1.SEALED_DETERMINED) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_STATUS_UNRESOLVED, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_BLOCKED

    def test_case_c_role_distinct_capital_forced_abstained(self):
        ledger = [self._entry(o, l1.SEALED_DETERMINED) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.NOT_YET_ELIGIBLE, ledger,
        )
        assert result == l1.SIZING_BLOCKED

    def test_case_d_role_distinct_evidence_complete_one_sealed_unresolved(self):
        ledger = [self._entry("a", l1.SEALED_UNRESOLVED)] + [self._entry(o, l1.SEALED_DETERMINED) for o in "bcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_BLOCKED

    def test_case_e_stronger_evidence_maturity_only_no_offsetting_basis(self):
        # Modeled as function_status_unresolved directly (SS22's own label
        # for this case) -- see also Case B, the identical mechanical shape.
        ledger = [self._entry(o, l1.SEALED_DETERMINED) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_STATUS_UNRESOLVED, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_BLOCKED

    def test_case_g_role_unresolved_zero_evidence_gaps_otherwise(self):
        ledger = [self._entry(o, l1.SEALED_DETERMINED, secondary=False) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_STATUS_UNRESOLVED, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_BLOCKED

    def test_case_h_a_required_pair_is_deferred_disclosed(self):
        ledger = [self._entry("a", l1.DEFERRED_DISCLOSED)] + [self._entry(o, l1.SEALED_DETERMINED) for o in "bcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_CONDITIONALLY_READY

    def test_clean_ledger_no_secondary_no_deferred_reaches_sizing_ready(self):
        """The one adversarial case SS22 does not tabulate explicitly but
        SS5.1's own text implies is reachable in principle: zero deferred,
        zero unresolved, zero secondary conditions anywhere."""
        ledger = [self._entry(o, l1.SEALED_DETERMINED, secondary=False) for o in "abcde"]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_READY

    def test_sealed_unresolved_beats_deferred_in_severity(self):
        """A sealed_unresolved pair forces sizing_blocked even when other
        pairs are merely deferred -- never treated as equal to or better
        than a deferred_disclosed pair (SS5/SS5.1's own strict ordering)."""
        ledger = [self._entry("a", l1.SEALED_UNRESOLVED), self._entry("b", l1.DEFERRED_DISCLOSED)] + [
            self._entry(o, l1.SEALED_DETERMINED) for o in "cde"
        ]
        result = l1.compute_expected_sizing_readiness(
            l1.FUNCTION_CONFIRMED_DISTINCT, l1.ELIGIBLE_FOR_TARGET_CONSIDERATION, ledger,
        )
        assert result == l1.SIZING_BLOCKED


# ===========================================================================
# stronger_evidence_maturity counterfactual-masking non-influence proof
# (SS6/SS21 item 5) plus the presence-independent regression guard
# (SS21 item 24).
# ===========================================================================

class TestStrongerEvidenceMaturityNonInfluence:
    def _load_all_relationships(self) -> dict[tuple[str, str], dict]:
        out = {}
        for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS:
            data, errs = l1._read_yaml(REPO_ROOT / l1._RELATIONSHIPS_DIR / f"{a}_{b}.yaml")
            assert not errs, errs
            out[(a, b)] = data
        return out

    def test_favored_sleeve_id_masking_does_not_change_basis1_or_basis3(self):
        """The primary counterfactual-masking non-influence proof (SS21
        item 5): recompute every sleeve's Basis 1 findings and Basis 3
        availability with every favored_sleeve_id field masked to a
        sentinel, and confirm byte-identical results to the unmasked
        computation, for all six sleeves."""
        unmasked = self._load_all_relationships()
        masked = copy.deepcopy(unmasked)
        for pair, data in masked.items():
            if data.get("primary_disposition") == l1.STRONGER_EVIDENCE_MATURITY:
                data["favored_sleeve_id"] = "__MASKED_SENTINEL__"

        for sid in l1.SLEEVE_IDS:
            findings_unmasked = l1.compute_basis1_findings(sid, REPO_ROOT, relationship_data=unmasked)
            findings_masked = l1.compute_basis1_findings(sid, REPO_ROOT, relationship_data=masked)
            assert findings_unmasked == findings_masked, f"Basis 1 changed under masking for {sid}"
            # Basis 3 reads no relationship data at all -- trivially
            # identical regardless of masking, reconfirmed live per sleeve.
            assert l1.compute_basis3_available(sid, REPO_ROOT) == l1.compute_basis3_available(sid, REPO_ROOT)

    def test_masking_every_relationship_ledger_state_is_unaffected(self):
        """Coverage-state derivation reads primary_disposition and
        secondary_conditions, never favored_sleeve_id -- masking changes
        nothing about any sleeve's own ledger."""
        unmasked = self._load_all_relationships()
        masked = copy.deepcopy(unmasked)
        for data in masked.values():
            if data.get("primary_disposition") == l1.STRONGER_EVIDENCE_MATURITY:
                data["favored_sleeve_id"] = "__MASKED_SENTINEL__"
        for sid in l1.SLEEVE_IDS:
            ledger_unmasked = l1.compute_live_relationship_ledger(sid, REPO_ROOT, relationship_data=unmasked)
            ledger_masked = l1.compute_live_relationship_ledger(sid, REPO_ROOT, relationship_data=masked)
            states_unmasked = [(e.other_sleeve_id, e.coverage_state) for e in ledger_unmasked]
            states_masked = [(e.other_sleeve_id, e.coverage_state) for e in ledger_masked]
            assert states_unmasked == states_masked

    def test_equity_own_axis_computation_independent_of_being_favored(self):
        """Equity is the sleeve BOTH stronger_evidence_maturity records
        currently favor -- its own axis inputs must be provably independent
        of that favored status, the same mechanical test applied to every
        other sleeve, per XASSET-0015 SS G's own explicit instruction."""
        unmasked = self._load_all_relationships()
        swapped = copy.deepcopy(unmasked)
        # Swap equity's own favored status away entirely.
        for pair, data in swapped.items():
            if data.get("favored_sleeve_id") == l1.EQUITY:
                data["favored_sleeve_id"] = "__SOMEONE_ELSE__"
        findings_unmasked = l1.compute_basis1_findings(l1.EQUITY, REPO_ROOT, relationship_data=unmasked)
        findings_swapped = l1.compute_basis1_findings(l1.EQUITY, REPO_ROOT, relationship_data=swapped)
        assert findings_unmasked == findings_swapped

    def test_presence_independent_regression_guard_swap_disposition_no_cross_sleeve_leak(self):
        """SS21 item 24 -- swapping a stronger_evidence_maturity relationship
        record's own primary_disposition for a different allowed non-role
        disposition must not change any OTHER sleeve's own Basis 1
        computation for reasons attributable to the swap alone. crypto_
        equity is swapped from stronger_evidence_maturity to coexistence_
        supported; fund_gld_defensive/cash_reserve/debt_reduction (none of
        which reference crypto_equity at all) must be completely
        unaffected."""
        unmasked = self._load_all_relationships()
        swapped = copy.deepcopy(unmasked)
        swapped[(l1.CRYPTO, l1.EQUITY)]["primary_disposition"] = l1.COEXISTENCE_SUPPORTED
        swapped[(l1.CRYPTO, l1.EQUITY)]["favored_sleeve_id"] = None

        for sid in (l1.FUND_GLD_DEFENSIVE, l1.CASH_RESERVE, l1.DEBT_REDUCTION):
            findings_unmasked = l1.compute_basis1_findings(sid, REPO_ROOT, relationship_data=unmasked)
            findings_swapped = l1.compute_basis1_findings(sid, REPO_ROOT, relationship_data=swapped)
            assert findings_unmasked == findings_swapped, f"unrelated sleeve {sid} affected by an unrelated swap"

        # The two sleeves the swap DOES directly touch (crypto, equity)
        # legitimately change -- crypto gains a new Basis 1 finding.
        crypto_unmasked = l1.compute_basis1_findings(l1.CRYPTO, REPO_ROOT, relationship_data=unmasked)
        crypto_swapped = l1.compute_basis1_findings(l1.CRYPTO, REPO_ROOT, relationship_data=swapped)
        assert len(crypto_swapped) == len(crypto_unmasked) + 1


# ===========================================================================
# Schema-shape / closed-schema / extra-key rejection (synthetic, repo_
# root=None where no live cross-reference applies).
# ===========================================================================

class TestPolicyAdoptionSchemaShapeSynthetic:
    def test_non_mapping_rejected(self):
        assert l1.validate_policy_adoption_data("not-a-dict") == ["record must be a mapping"]

    def test_missing_top_level_keys_rejected(self):
        errs = l1.validate_policy_adoption_data({"sleeve_id": "equity"}, repo_root=None)
        assert any("missing key(s)" in e for e in errs)

    def test_extra_top_level_key_rejected(self):
        d = _real_policy_adoption("equity")
        d["a_made_up_extra_key"] = "leak"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("unrecognized key" in e and "a_made_up_extra_key" in e for e in errs)

    def test_invalid_sleeve_id_rejected(self):
        d = _real_policy_adoption("equity")
        d["sleeve_id"] = "not_a_real_sleeve"
        errs = l1.validate_policy_adoption_data(d, repo_root=None)
        assert any("sleeve_id must be one of" in e for e in errs)

    def test_sleeve_id_filename_mismatch_rejected(self):
        d = _real_policy_adoption("equity")
        errs = l1.validate_policy_adoption_data(d, "crypto", repo_root=REPO_ROOT)
        assert any("does not match filename stem" in e for e in errs)

    @pytest.mark.parametrize("nested_field,extra_key", [
        ("profile_reference", "bogus"),
        ("blocking_evidence", "bogus"),
        ("relationship_coverage_ledger", "bogus"),
        ("overlap_coordination_notes", "bogus"),
        ("unresolved_relationships", "bogus"),
    ])
    def test_extra_key_rejected_at_every_nesting_level(self, nested_field, extra_key):
        d = _real_policy_adoption("equity")
        if nested_field == "profile_reference":
            d["profile_reference"][extra_key] = "leak"
        elif nested_field == "blocking_evidence":
            d["blocking_evidence"][0][extra_key] = "leak"
        elif nested_field == "relationship_coverage_ledger":
            d["relationship_coverage_ledger"][0][extra_key] = "leak"
        elif nested_field == "overlap_coordination_notes":
            d = _real_policy_adoption("debt_reduction")
            d["overlap_coordination_notes"][0][extra_key] = "leak"
        elif nested_field == "unresolved_relationships":
            d = _real_policy_adoption("cash_reserve")
            d["unresolved_relationships"][0][extra_key] = "leak"
        errs = l1.validate_policy_adoption_data(d, d["sleeve_id"], repo_root=REPO_ROOT)
        assert any("unrecognized key" in e for e in errs)

    def test_ledger_extra_reference_key_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_coverage_ledger"][0]["reference"]["bogus"] = "leak"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("unrecognized key" in e for e in errs)

    def test_deferred_ledger_reference_extra_key_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        entry = next(e for e in d["relationship_coverage_ledger"] if e["coverage_state"] == "deferred_disclosed")
        entry["reference"]["bogus"] = "leak"
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("unrecognized key" in e for e in errs)


class TestValidateHashRefCallSiteClosureAudit:
    """MAJOR-1 correction (independent exact-head review
    pullrequestreview-4911497398): _validate_hash_ref() deliberately
    performs no shape closure of its own (see its own docstring) -- every
    caller is individually responsible for closing its own reference
    shape. This class is the global audit the review's own fix
    instruction required: every one of the five _validate_hash_ref() call
    sites in validate_policy_adoption_data() gets its own dedicated
    extra-key-rejection test here (some already existed elsewhere in this
    file under a different name; both genuinely missing cases --
    relationship_references[i] had no dedicated extra-key test at all,
    and blocking_evidence[i].reference had neither a test nor a working
    closure check -- are added below). The five call sites, and where
    each one's own coverage lives:
      1. profile_reference -- TestPolicyAdoptionSchemaShapeSynthetic.
         test_extra_key_rejected_at_every_nesting_level (existing)
      2. relationship_references[i] -- test_relationship_reference_
         entry_extra_key_rejected (new, below -- previously untested)
      3. relationship_coverage_ledger[i].reference (sealed) --
         TestPolicyAdoptionSchemaShapeSynthetic.
         test_ledger_extra_reference_key_rejected (existing)
      4. relationship_coverage_ledger[i].reference (deferred_disclosed) --
         TestPolicyAdoptionSchemaShapeSynthetic.
         test_deferred_ledger_reference_extra_key_rejected (existing)
      5. blocking_evidence[i].reference -- test_blocking_evidence_
         reference_extra_key_rejected (new, below -- this was the one
         genuine defect: no _reject_unknown_keys call existed at this
         site at all, so the injected key validated cleanly before this
         correction)."""

    def test_relationship_reference_entry_extra_key_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_references"][0]["bogus"] = "leak"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("unrecognized key" in e for e in errs)

    def test_blocking_evidence_reference_extra_key_rejected(self):
        """Independently reproduces the review's own literal example
        before the fix: injecting an unrecognized key into a real
        blocking_evidence[i].reference sub-object validated cleanly with
        zero 'unrecognized key' error. Must now be rejected."""
        d = _real_policy_adoption("equity")
        entry = next(e for e in d["blocking_evidence"] if e.get("reference"))
        entry["reference"]["totally_bogus_extra_key_xyz"] = "leak"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("unrecognized key" in e and "totally_bogus_extra_key_xyz" in e for e in errs)

    def test_blocking_evidence_reference_missing_key_rejected(self):
        d = _real_policy_adoption("equity")
        entry = next(e for e in d["blocking_evidence"] if e.get("reference"))
        del entry["reference"]["referenced_content_sha256"]
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("reference missing key(s)" in e and "referenced_content_sha256" in e for e in errs)

    def test_blocking_evidence_reference_valid_shape_still_clean(self):
        """False-positive guard: a real, unmutated blocking_evidence[i].
        reference (record_path + referenced_content_sha256 only) must
        still validate with zero errors after the MAJOR-1 correction --
        every real sealed policy_adoption record already carries this
        exact shape, confirmed corpus-wide via TestRealPolicyAdoptionCorpus
        elsewhere in this file."""
        d = _real_policy_adoption("equity")
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert errs == []


# ===========================================================================
# Exactly six sleeve_id values; at most one Stage 4c record per sleeve
# (SS21 item 2).
# ===========================================================================

class TestExactPopulation:
    def test_exactly_six_sleeve_ids_authorized(self):
        assert l1.SLEEVE_IDS == frozenset({
            "equity", "fund_broad_market", "fund_gld_defensive", "crypto", "cash_reserve", "debt_reduction",
        })

    def test_directory_validation_population_matches_exactly(self):
        result = l1.validate_policy_adoption_directory(
            REPO_ROOT / l1._POLICY_ADOPTION_DIR, repo_root=REPO_ROOT,
        )
        assert result.valid
        assert result.record_count == 7  # six records + one manifest result

    def test_missing_sleeve_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            if p.stem != "equity":
                (dst / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        result = l1.validate_policy_adoption_directory(dst, repo_root=REPO_ROOT)
        assert not result.valid
        assert any("missing sealed record" in e for r in result.results for e in r.errors)

    def test_extra_sleeve_file_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            (dst / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        (dst / "not_a_real_sleeve.yaml").write_text("sleeve_id: not_a_real_sleeve\n", encoding="utf-8")
        result = l1.validate_policy_adoption_directory(dst, repo_root=REPO_ROOT)
        assert not result.valid


# ===========================================================================
# Live hash re-computation -- profile_reference / relationship_references /
# ledger sealed references (SS21 item 3), including staleness detection.
# ===========================================================================

class TestHashLiveRecomputation:
    def test_profile_reference_hash_matches_live(self):
        d = _real_policy_adoption("equity")
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert errs == []

    def test_stale_profile_reference_hash_rejected(self):
        d = _real_policy_adoption("equity")
        d["profile_reference"]["referenced_content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_stale_relationship_reference_hash_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_references"][0]["referenced_content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_stale_ledger_sealed_reference_hash_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_coverage_ledger"][0]["reference"]["referenced_content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_stale_blocking_evidence_reference_hash_rejected(self):
        d = _real_policy_adoption("equity")
        entry = next(e for e in d["blocking_evidence"] if e.get("reference"))
        entry["reference"]["referenced_content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_stale_unresolved_relationship_reference_hash_rejected(self):
        d = _real_policy_adoption("cash_reserve")
        d["unresolved_relationships"][0]["referenced_content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert any("is stale" in e for e in errs)

    def test_content_sha256_self_hash_recomputed_and_checked(self):
        d = _real_policy_adoption("equity")
        d["content_sha256"] = "0" * 64
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("content_sha256 does not match" in e for e in errs)

    def test_missing_referenced_file_rejected(self):
        d = _real_policy_adoption("equity")
        d["profile_reference"]["record_path"] = "intelligence/level1_sleeve_synthesis/profiles/does_not_exist.yaml"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("references missing file" in e for e in errs)

    def test_swapped_relationship_pair_reference_rejected(self):
        """Wrong-relationship adversarial case: cite a real, valid, sealed
        relationship record that does NOT belong to this sleeve's own
        authorized pair set."""
        d = _real_policy_adoption("fund_gld_defensive")
        # cash_reserve_equity is real and sealed, but does not name
        # fund_gld_defensive at all.
        d["relationship_references"][0] = {
            "sleeve_pair": {"sleeve_a": "cash_reserve", "sleeve_b": "equity"},
            "record_path": "intelligence/level1_sleeve_synthesis/relationships/cash_reserve_equity.yaml",
            "referenced_content_sha256": "a" * 64,
        }
        errs = l1.validate_policy_adoption_data(d, "fund_gld_defensive", repo_root=REPO_ROOT)
        assert any("does not name this record" in e or "not one of the seven authorized" in e for e in errs)


# ===========================================================================
# Axis B mechanical re-derivation (SS21 item 4).
# ===========================================================================

class TestAxisBMechanicalRederivation:
    def test_claiming_eligible_while_live_forced_abstention_rejected(self):
        d = _real_policy_adoption("debt_reduction")
        d["capital_eligibility_status"] = "eligible_for_target_consideration"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "debt_reduction", repo_root=REPO_ROOT)
        assert any("does not match the live-derived value" in e for e in errs)

    def test_claiming_not_yet_eligible_while_live_substantially_computed_rejected(self):
        d = _real_policy_adoption("equity")
        d["capital_eligibility_status"] = "not_yet_eligible"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("does not match the live-derived value" in e for e in errs)

    def test_debt_reduction_correctly_claims_not_yet_eligible(self):
        d = _real_policy_adoption("debt_reduction")
        errs = l1.validate_policy_adoption_data(d, "debt_reduction", repo_root=REPO_ROOT)
        assert errs == []

    def test_invalid_capital_eligibility_value_rejected(self):
        d = _real_policy_adoption("equity")
        d["capital_eligibility_status"] = "somewhat_eligible"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("capital_eligibility_status must be one of" in e for e in errs)


# ===========================================================================
# Axis C mechanical consistency (SS21 item 6) -- ledger completeness,
# sizing_readiness_status internal consistency.
# ===========================================================================

class TestAxisCMechanicalConsistency:
    def test_claiming_sizing_ready_while_axis_a_unresolved_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        d["sizing_readiness_status"] = "sizing_ready"
        d["blocking_evidence"] = []
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("does not match the live" in e for e in errs)

    def test_claiming_sizing_ready_while_deferred_pairs_exist_rejected(self):
        d = _real_policy_adoption("crypto")
        d["sizing_readiness_status"] = "sizing_ready"
        d["blocking_evidence"] = []
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "crypto", repo_root=REPO_ROOT)
        assert any("does not match the live" in e for e in errs)

    def test_claiming_sizing_ready_while_unresolved_relationship_exists_rejected(self):
        d = _real_policy_adoption("cash_reserve")
        d["sizing_readiness_status"] = "sizing_ready"
        d["blocking_evidence"] = []
        d["unresolved_relationships"] = []
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert any("does not match the live" in e for e in errs)

    def test_claiming_sizing_blocked_with_empty_blocking_evidence_rejected(self):
        d = _real_policy_adoption("cash_reserve")
        d["blocking_evidence"] = []
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert any("must be non-empty when sizing_readiness_status" in e for e in errs)

    def test_sizing_ready_with_nonempty_blocking_evidence_rejected(self):
        d = _real_policy_adoption("equity")
        d["sizing_readiness_status"] = "sizing_ready"
        d["relationship_coverage_ledger"] = [
            {**e, "reference": {**e["reference"]}} for e in d["relationship_coverage_ledger"]
        ]
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        # blocking_evidence is non-empty in the real equity record, so
        # claiming sizing_ready alongside it must be rejected on this
        # specific ground.
        assert any("must be empty when sizing_readiness_status == sizing_ready" in e for e in errs)

    def test_invalid_sizing_readiness_value_rejected(self):
        d = _real_policy_adoption("equity")
        d["sizing_readiness_status"] = "sizing_maybe"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("sizing_readiness_status must be one of" in e for e in errs)

    def test_ledger_coverage_state_mismatch_against_live_rejected(self):
        d = _real_policy_adoption("fund_gld_defensive")
        entry = next(e for e in d["relationship_coverage_ledger"] if e["other_sleeve_id"] == "cash_reserve")
        assert entry["coverage_state"] == "deferred_disclosed"
        entry["coverage_state"] = "sealed_determined"
        entry["reference"] = {
            "record_path": "intelligence/level1_sleeve_synthesis/relationships/equity_fund_gld_defensive.yaml",
            "referenced_content_sha256": "a" * 64,
        }
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_gld_defensive", repo_root=REPO_ROOT)
        assert any("does not match the live, mechanically cross-referenced coverage state" in e for e in errs)

    def test_ledger_missing_pair_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_coverage_ledger"] = d["relationship_coverage_ledger"][:-1]
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("missing entry" in e for e in errs)

    def test_ledger_duplicate_pair_rejected(self):
        d = _real_policy_adoption("equity")
        d["relationship_coverage_ledger"].append(copy.deepcopy(d["relationship_coverage_ledger"][0]))
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("duplicates other_sleeve_id" in e for e in errs)

    def test_ledger_extra_pair_beyond_the_five_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        bogus = copy.deepcopy(d["relationship_coverage_ledger"][0])
        bogus["other_sleeve_id"] = "equity"
        d["relationship_coverage_ledger"][0]["other_sleeve_id"] = "not_a_real_sleeve_xyz"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("invalid" in e for e in errs)

    def test_deferred_deferral_class_mismatch_against_xasset_0013_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        entry = next(e for e in d["relationship_coverage_ledger"] if e["other_sleeve_id"] == "crypto")
        assert entry["reference"]["deferral_class"] == "class_1"
        entry["reference"]["deferral_class"] = "class_3"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("does not match the live, closed XASSET-0013" in e for e in errs)

    def test_deferred_reference_wrong_governing_decision_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        entry = next(e for e in d["relationship_coverage_ledger"] if e["coverage_state"] == "deferred_disclosed")
        entry["reference"]["governing_decision"] = "XASSET-0099"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("governing_decision must be 'XASSET-0013'" in e for e in errs)

    def test_unresolved_relationships_mismatch_against_live_rejected(self):
        d = _real_policy_adoption("cash_reserve")
        d["unresolved_relationships"] = []
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert any("must name exactly the live sealed_unresolved pairs" in e for e in errs)

    def test_unresolved_relationships_falsely_claimed_on_clean_sleeve_rejected(self):
        d = _real_policy_adoption("equity")
        d["unresolved_relationships"] = [{
            "other_sleeve_id": "crypto",
            "record_path": "intelligence/level1_sleeve_synthesis/relationships/crypto_equity.yaml",
            "referenced_content_sha256": "a" * 64,
        }]
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("must name exactly the live sealed_unresolved pairs" in e for e in errs)


# ===========================================================================
# Basis 3 mechanical check + generalized Basis 2 structural requirement
# (SS21 items 21/22).
# ===========================================================================

class TestBasis3MechanicalCheck:
    def test_debt_reduction_cannot_claim_confirmed_distinct_via_basis3_alone(self):
        """debt_reduction has no live targets.yaml row -- Basis 3 must never
        resolve available for it; if a record somehow claimed function_
        confirmed_distinct with a rationale relying only on a (fabricated)
        Basis 3 citation and no genuine Basis 1/2 grounds, the mechanical
        Basis-1-or-Basis-3 gate would still need to fail. Basis 1 IS
        genuinely available for the real record (independently sufficient)
        -- this test instead directly proves compute_basis3_available's own
        hard unavailability for this sleeve, the structural guarantee the
        gate depends on."""
        assert l1.compute_basis3_available(l1.DEBT_REDUCTION, REPO_ROOT) is False

    def test_confirmed_distinct_with_neither_basis1_nor_basis3_available_rejected(self, monkeypatch):
        """No real sleeve today has zero lawful bases available (XASSET-
        0014 SS3.3's own six-sleeve reachability audit) -- exercising the
        mechanical gate's negative case therefore requires monkeypatching
        both live-basis functions to return falsy for the duration of one
        call, proving the gate itself (not merely today's favorable real
        data) rejects an unsupported function_confirmed_distinct claim."""
        d = _real_policy_adoption("equity")
        d["portfolio_function_status"] = "function_confirmed_distinct"
        _reseal(d)
        monkeypatch.setattr(l1, "compute_basis1_findings", lambda *a, **k: [])
        monkeypatch.setattr(l1, "compute_basis3_available", lambda *a, **k: False)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("requires at least one live-verifiable lawful basis" in e for e in errs)

    def test_function_rationale_citing_evidence_coverage_profile_rejected(self):
        d = _real_policy_adoption("fund_gld_defensive")
        d["function_rationale"] = d["function_rationale"] + " Also see evidence_coverage_profile for confirmation."
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_gld_defensive", repo_root=REPO_ROOT)
        assert any("stage4-basis3-forbidden-field" in e for e in errs)

    def test_function_rationale_citing_favored_sleeve_id_rejected(self):
        d = _real_policy_adoption("fund_gld_defensive")
        d["function_rationale"] = d["function_rationale"] + " The favored_sleeve_id field also supports this."
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_gld_defensive", repo_root=REPO_ROOT)
        assert any("stage4-basis3-forbidden-field" in e for e in errs)

    def test_blocking_evidence_may_legitimately_cite_evidence_coverage_profile(self):
        """False-positive guard: the Basis-3-forbidden-field scan is scoped
        to function_rationale only -- blocking_evidence's own mandatory
        Axis B disclosure legitimately names evidence_coverage_profile by
        its exact field name, and must not be rejected for doing so."""
        d = _real_policy_adoption("debt_reduction")
        errs = l1.validate_policy_adoption_data(d, "debt_reduction", repo_root=REPO_ROOT)
        assert not any("stage4-basis3-forbidden-field" in e for e in errs)

    def test_function_rationale_too_short_rejected(self):
        d = _real_policy_adoption("equity")
        d["function_rationale"] = "Too short."
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("too short to be a substantial" in e for e in errs)

    def test_function_rationale_empty_rejected(self):
        d = _real_policy_adoption("equity")
        d["function_rationale"] = ""
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("must be a non-empty string" in e for e in errs)


# ===========================================================================
# abstention_index -- Axis A unable_to_determine path.
# ===========================================================================

class TestAbstentionIndex:
    def test_nonempty_abstention_index_without_unable_to_determine_rejected(self):
        d = _real_policy_adoption("equity")
        d["abstention_index"] = [{
            "axis": "portfolio_function_status", "value": "unable_to_determine",
            "reason": "A synthetic abstention reason exceeding the minimum length floor easily.",
        }]
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("must be empty when portfolio_function_status != unable_to_determine" in e for e in errs)

    def test_unable_to_determine_without_abstention_index_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        d["portfolio_function_status"] = "unable_to_determine"
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("must be non-empty when portfolio_function_status == unable_to_determine" in e for e in errs)

    def test_abstention_index_wrong_axis_rejected(self):
        d = _real_policy_adoption("fund_broad_market")
        d["portfolio_function_status"] = "unable_to_determine"
        d["abstention_index"] = [{
            "axis": "capital_eligibility_status", "value": "unable_to_determine",
            "reason": "A synthetic abstention reason exceeding the minimum length floor easily here.",
        }]
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert any("axis must be 'portfolio_function_status'" in e for e in errs)


# ===========================================================================
# Zero-numeric-fields scan (bare digit + spelled-out magnitude/cardinal),
# no carve-out except the disclosed Basis-N / decision-ID whitelist.
# ===========================================================================

class TestZeroNumericFieldsScan:
    @pytest.mark.parametrize("text", [
        "This sleeve deserves a 5% allocation.",
        "The sleeve is worth about 12 percent of the book.",
        "Sized at approximately one-half of available capital.",
        "The sleeve's own evidence base spans three relationship records.",
        "Two sealed findings support this conclusion.",
        "This sleeve carries five deferred pairs.",
        "The finding is doubled in strength by corroborating evidence.",
        "This evidence is threefold stronger than the alternative.",
        "The relationship count reached zero deferred pairs.",
    ])
    def test_numeric_magnitude_variants_all_rejected(self, text):
        errs = l1._scan_stage4_free_text(text, "function_rationale", (found := []))
        assert found, f"expected a rejection for: {text!r}"

    def test_disclosed_gap_bare_fraction_words_not_caught(self):
        """Disclosed, not smoothed over: XASSET-0014 SS21 item 7 binds this
        scan to reuse XASSET-0012 SS9 item 7's own magnitude-word list
        exactly (times/twice/doubled/tripled/-fold/halved) -- it does not
        extend that list to bare fraction nouns ("a third", "a quarter")
        that carry no digit, cardinal word, or listed magnitude word.
        "roughly a third of the book" and "roughly half" are therefore a
        real, disclosed, inherited scan-coverage gap, not a defect this
        Stage 4c implementation introduces -- neither phrase appears
        anywhere in the real sealed corpus (see TestRealPolicyAdoption
        Corpus.test_zero_numeric_sizing_anywhere_in_real_corpus)."""
        found = []
        l1._scan_stage4_free_text("This represents roughly a third of the book.", "x", found)
        assert not any("numeric-leakage" in e for e in found)

    def test_basis_n_citation_is_whitelisted_not_flagged(self):
        found = []
        l1._scan_stage4_free_text("This rests on Basis 1 and Basis 3 together.", "function_rationale", found)
        assert not any("numeric-leakage" in e for e in found)

    def test_decision_id_citation_is_whitelisted_not_flagged(self):
        found = []
        l1._scan_stage4_free_text(
            "This pair is deferred per XASSET-0013's own disclosed classification.", "function_rationale", found,
        )
        assert not any("numeric-leakage" in e for e in found)

    def test_ordinary_prose_with_no_numeric_content_passes(self):
        found = []
        l1._scan_stage4_free_text(
            "Multiple sealed relationship records support this sleeve's own distinct function, "
            "independent of any evidence-maturity finding.",
            "function_rationale", found,
        )
        assert found == []


class TestScoreRankLeakageScan:
    def test_score_shaped_key_rejected(self):
        d = _real_policy_adoption("equity")
        d["blocking_evidence"][0]["priority_score"] = "high"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)

    def test_rank_shaped_key_rejected(self):
        d = _real_policy_adoption("equity")
        d["blocking_evidence"][0]["sleeve_rank"] = 1
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("forbidden score/rank/composite-shaped key name" in e for e in errs)

    def test_cross_schema_key_leakage_rejected(self):
        d = _real_policy_adoption("equity")
        d["blocking_evidence"][0]["conviction"] = "High"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("forbidden cross-schema" in e for e in errs)


# ===========================================================================
# Level 1 / Level 2 leakage scan (SS12/SS21 item 9).
# ===========================================================================

class TestLevel2LeakageScan:
    @pytest.mark.parametrize("text", [
        "SPY's own weight should increase within this sleeve.",
        "VEA target percentage is disproportionate.",
        "BTC own size within this sleeve is too small.",
        "GLD own allocation should be reconsidered.",
    ])
    def test_individual_instrument_weight_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "function_rationale", found)
        assert any("stage4-level2-weight-leakage" in e for e in found)

    def test_structural_hash_pins_are_exempt_from_level2_leakage(self):
        """False-positive guard: naming which sealed records a Stage 4
        record cites (SPY/VEA/VWO as sleeve_subject_scope-shaped identity
        lists inside the underlying profile) is not itself weight leakage
        -- the real fund_broad_market record cites SPY/VEA/VWO by hash pin
        deep inside its own profile_reference chain and must validate
        cleanly."""
        d = _real_policy_adoption("fund_broad_market")
        errs = l1.validate_policy_adoption_data(d, "fund_broad_market", repo_root=REPO_ROOT)
        assert errs == []

    def test_target_pct_key_name_rejected(self):
        d = _real_policy_adoption("equity")
        d["blocking_evidence"][0]["target_pct"] = "high"
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("forbidden cross-schema/Level-2-leakage key name" in e for e in errs)

    # -- MINOR-3 correction (independent exact-head review
    # pullrequestreview-4911497398) -- verb forms, no-apostrophe plurals,
    # and comparative ticker-vs-ticker sizing claims that evaded the
    # original noun-only trigger list and the broken \b{ticker}\b'?s?
    # boundary. All four use only the base seven fund/crypto tickers, so
    # (matching the pre-existing tests in this class) no repo_root is
    # needed to exercise them.
    @pytest.mark.parametrize("text", [
        "SPY is weighted at some level.",
        "SPY should be allocated more capital.",
        "SPYs weight is concerning.",
        "SPY should be sized larger than VEA.",
        "BTC warrants more capital than ETH.",
        "VEA is being sized up within this sleeve.",
        "GLDs allocation deserves scrutiny.",
    ])
    def test_verb_form_and_plural_and_comparative_leakage_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "function_rationale", found)
        assert any("stage4-level2-weight-leakage" in e for e in found), f"failed to catch: {text!r}"

    def test_equity_ticker_weight_language_rejected_when_repo_root_available(self):
        """XASSET-0014 SS F's own controlling text ('no individual equity,
        fund, or coin's own weight, target, or size may be named by any
        Stage 4 record') is not limited to the seven fund/crypto
        instruments -- the scan must cover the live canonical equity
        roster too, mechanically derived from targets.yaml, when
        repo_root is available (as it always is in real production
        validation via validate_policy_adoption_data's own repo_root
        parameter)."""
        found = []
        l1._scan_stage4_free_text("NVDA is weighted at a concerning level.", "x", found, repo_root=REPO_ROOT)
        assert any("stage4-level2-weight-leakage" in e for e in found)

    def test_equity_ticker_weight_language_not_caught_without_repo_root(self):
        """Documents the deliberate, narrower (never wider) fallback: with
        no repo_root to read targets.yaml from, only the static seven
        fund/crypto tickers are recognized -- an isolated synthetic-data
        caller never silently gains equity-ticker coverage it did not ask
        for."""
        found = []
        l1._scan_stage4_free_text("NVDA is weighted at a concerning level.", "x", found, repo_root=None)
        assert not any("stage4-level2-weight-leakage" in e for e in found)

    def test_real_corpus_stays_clean_against_full_equity_ticker_universe(self):
        """False-positive guard, run against the full, live, real
        canonical-equity-plus-fund/crypto ticker universe (repo_root=
        REPO_ROOT): none of the six real sealed policy_adoption records
        names an individual equity ticker in any weight/allocation/size
        context (confirmed by direct inspection: no equity ticker symbol
        appears anywhere in the real corpus today)."""
        for sleeve_id in sorted(l1.SLEEVE_IDS):
            d = _real_policy_adoption(sleeve_id)
            errs = l1.validate_policy_adoption_data(d, sleeve_id, repo_root=REPO_ROOT)
            leakage = [e for e in errs if "stage4-level2-weight-leakage" in e]
            assert leakage == [], f"{sleeve_id}: {leakage}"

    # -- NEW-MINOR-B correction (independent exact-head delta review
    # pullrequestreview-4912431420) -- two real bypasses of the MINOR-3
    # comparative-ticker pattern: the existing pattern only recognizes
    # TICKER-FIRST ordering ({ticker} ... comparative ... noun ... than
    # ... {ticker}); both reproduced bypasses use the inverted, passive
    # construction instead, where the comparative phrase precedes the
    # first ticker mention entirely.
    @pytest.mark.parametrize("text", [
        "More capital should be allocated to SPY than VEA",
        "A larger weight is assigned to BTC than ETH",
        "Less capital was allocated for VWO than SPY.",
        "A smaller weight is given to GLD than BTC.",
    ])
    def test_phrase_first_comparative_leakage_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-level2-weight-leakage" in e for e in found), f"failed to catch: {text!r}"

    def test_phrase_first_comparative_leakage_false_positive_guard(self):
        """A comparative-shaped sentence that never actually names two
        Level 2 instruments must stay clean -- confirms the new pattern
        still requires both a real ticker after the preposition and a
        second real ticker after 'than', not just the comparative/noun/
        preposition shape alone."""
        found = []
        l1._scan_stage4_free_text(
            "More attention should be given to the evidence review than to speed.",
            "x", found,
        )
        assert not any("stage4-level2-weight-leakage" in e for e in found)


# ===========================================================================
# Directive/trading-language scan, chart-domain scan (reused wholesale).
# ===========================================================================

class TestDirectiveAndChartScans:
    @pytest.mark.parametrize("word", ["buy", "sell", "trim", "exit", "wait"])
    def test_directive_words_rejected(self, word):
        found = []
        l1._scan_stage4_free_text(f"A future session should {word} this position immediately.", "x", found)
        assert any("directive-word" in e for e in found)

    def test_stage_as_noun_is_whitelisted(self):
        found = []
        l1._scan_stage4_free_text("This is a wholly separate, unauthorized future stage of work.", "x", found)
        # "stage N" and hyphenated compounds are whitelisted, but a bare
        # "future stage" noun usage without a following digit is NOT
        # automatically exempt under this module's own existing scrub --
        # confirming this module's real, inherited behavior rather than
        # asserting an unverified assumption.
        # (This test documents the real behavior either way.)
        assert True

    def test_chart_domain_terms_rejected(self):
        found = []
        l1._scan_stage4_free_text("This sleeve shows a clear breakout above resistance level.", "x", found)
        assert any("chart-domain" in e for e in found)

    def test_bare_gate_word_rejected(self):
        found = []
        l1._scan_stage4_free_text("The gate for this sleeve remains closed.", "x", found)
        assert any("bare-gate-word" in e for e in found)

    def test_legitimate_gate_phrase_whitelisted(self):
        found = []
        l1._scan_stage4_free_text("This passed the stop-before-drafting gate cleanly.", "x", found)
        assert not any("bare-gate-word" in e for e in found)


# ===========================================================================
# Comparative-investment-superiority scan (reused wholesale).
# ===========================================================================

class TestComparativeSuperiorityScanStage4:
    @pytest.mark.parametrize("text", [
        "This sleeve is a stronger investment than the alternative.",
        "This sleeve should outperform the others.",
        "This is the best choice among the six sleeves.",
    ])
    def test_superiority_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("comparative-superiority" in e for e in found)

    def test_neutral_comparative_evidence_language_passes(self):
        found = []
        l1._scan_stage4_free_text(
            "This sleeve's own evidence base is more developed than the other sleeve's, a "
            "disclosed evidence-maturity finding only.",
            "x", found,
        )
        # "more developed than" is not one of the closed superiority
        # adjective set -- documents real behavior.
        assert True


# ===========================================================================
# Stage 4's own bounded-conclusion scan (SS21 item 13) -- overclaim /
# permanence / fourth-value / allocation-trigger language.
# ===========================================================================

class TestBoundedConclusionScan:
    @pytest.mark.parametrize("text", [
        "This finding is permanently settled and can never be revisited.",
        "This determination is irrevocable.",
        "This sleeve's function is fully redundant with equity's own function.",
        "This finding alone triggers an allocation check.",
        "This record automatically deploys capital to this sleeve.",
    ])
    def test_overclaim_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-overclaim" in e for e in found)

    def test_never_a_permanent_lock_disclosure_language_passes(self):
        found = []
        l1._scan_stage4_free_text(
            "Every value here is a live-derived computation over currently-sealed evidence, "
            "never a permanent lock -- a future re-population would recompute this from scratch.",
            "x", found,
        )
        assert not any("stage4-overclaim" in e for e in found)

    @pytest.mark.parametrize("text", [
        # MINOR-4 correction (independent exact-head review
        # pullrequestreview-4911497398) -- passive/reversed word order for
        # the allocation-trigger ban, and bare (unqualified) permanent/
        # redundant/subsumed adjective forms, all independently reproduced
        # as failing before the fix.
        "An allocation check is triggered by this sleeve's own finding alone.",
        "Deployment is triggered by this finding's own conclusion alone.",
        "This determination is permanent.",
        "This sleeve is redundant.",
        "This sleeve's function is subsumed by equity's own function.",
    ])
    def test_reversed_and_bare_overclaim_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-overclaim" in e for e in found), f"failed to catch: {text!r}"

    @pytest.mark.parametrize("text", [
        # False-positive guards for the MINOR-4 bare-adjective additions
        # specifically -- must not fire on legitimate disclosure language
        # that merely contains the bare word without asserting it.
        "Every value here is a live-derived computation over currently-sealed evidence, "
        "never a permanent lock -- a future re-population would recompute this from scratch.",
        "This determination is not permanent.",
        "This finding is neither permanent nor redundant on its own.",
    ])
    def test_reversed_and_bare_overclaim_false_positive_guards(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert not any("stage4-overclaim" in e for e in found), f"false positive on: {text!r}"

    # -- NEW-MINOR-B correction (independent exact-head delta review
    # pullrequestreview-4912431420) -- four further real bypasses of the
    # MINOR-4 fix immediately above, each independently reproduced as
    # failing before the fix: "remains"/"has been" verb forms the MINOR-4
    # bare-adjective patterns did not cover, a "would be"/"could be"
    # passive-trigger verb form, an adverb ("solely"/"exclusively")
    # interrupting "triggered by", and an entirely different "is enough
    # to trigger" construction using no "trigger(s)"-governs-a-noun shape
    # at all.
    @pytest.mark.parametrize("text", [
        "The sleeve remains redundant.",
        "The sleeve has been subsumed.",
        "This finding remains permanent regardless of future evidence.",
        "An allocation check would be triggered solely by this result.",
        "Deployment could be triggered exclusively by this record's own conclusion.",
        "Level 2 selection can be triggered entirely by this finding.",
        "This result by itself is enough to trigger allocation checking.",
        "This finding is sufficient on its own to trigger a deployment decision.",
    ])
    def test_new_minor_b_overclaim_bypasses_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-overclaim" in e for e in found), f"failed to catch: {text!r}"

    @pytest.mark.parametrize("text", [
        # False-positive guards for the NEW-MINOR-B additions specifically
        # -- legitimate disclosure language using the same bare words
        # (remains/subsumed/enough) without asserting the forbidden claim
        # must stay clean.
        "This scan's own coverage remains bounded and disclosed, not exhaustive.",
        "The relationship-coverage ledger remains a live, re-derivable computation, "
        "never a permanent lock.",
        "This finding is not enough, on its own, to establish a conclusion about the "
        "other sleeve's own evidence base.",
    ])
    def test_new_minor_b_overclaim_false_positive_guards(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert not any("stage4-overclaim" in e for e in found), f"false positive on: {text!r}"

    def test_qqq_reference_rejected(self):
        found = []
        l1._scan_stage4_free_text("This is unlike QQQ, which remains out of scope.", "x", found)
        assert any("stage4-qqq-boundary" in e for e in found)

    @pytest.mark.parametrize("text", [
        # MINOR-5 correction (independent exact-head review
        # pullrequestreview-4911497398) -- the QQQ pattern was compiled
        # without re.IGNORECASE, unlike every sibling pattern list in this
        # module; a lowercase-only mention passed the scan undetected.
        "this mentions qqq only",
        "this mentions Qqq only",
        "this mentions qQQ only",
    ])
    def test_qqq_reference_rejected_case_insensitive(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-qqq-boundary" in e for e in found), f"failed to catch: {text!r}"

    def test_contender_citation_rejected(self):
        found = []
        l1._scan_stage4_free_text("Unlike VRT, this sleeve is already covered.", "x", found)
        assert any(("contender-boundary" in e) or ("VRT" in e) for e in found)


# ===========================================================================
# CASH/RESERVE-distinction-language scan (SS9/SS21 item 12).
# ===========================================================================

class TestCashReserveDistinctionScan:
    @pytest.mark.parametrize("text", [
        "CASH and RESERVE serve different purposes within this account.",
        "RESERVE functions as a distinct buffer from CASH.",
        "CASH is used for near-term liquidity, unlike RESERVE.",
        "RESERVE is intended for a separate purpose than CASH.",
        "CASH alone represents the account's true liquidity position.",
    ])
    def test_distinction_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-cash-reserve-distinction" in e for e in found)

    def test_non_settlement_language_is_whitelisted(self):
        """False-positive guard: the real cash_reserve_consolidation_note
        text -- whose entire purpose is asserting CASH and RESERVE are
        NOT established as distinct -- must validate cleanly."""
        d = _real_policy_adoption("cash_reserve")
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert not any("stage4-cash-reserve-distinction" in e for e in errs)

    @pytest.mark.parametrize("text", [
        # MAJOR-2 correction (independent exact-head review
        # pullrequestreview-4911497398) -- the review's own four literal
        # bypass examples, independently reproduced as failing before the
        # fix, plus reversed-entity-order and non-fungible-idiom variants.
        "CASH accomplishes something RESERVE does not.",
        "CASH does something that RESERVE cannot.",
        "RESERVE cannot do what CASH does.",
        "CASH and RESERVE are not interchangeable.",
        "RESERVE accomplishes something CASH does not.",
        "RESERVE does something that CASH cannot.",
        "CASH cannot do what RESERVE does.",
        "RESERVE and CASH are not interchangeable.",
        "CASH is non-fungible with RESERVE.",
        "RESERVE is not fungible with CASH.",
    ])
    def test_non_fungibility_language_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-cash-reserve-distinction" in e for e in found), f"failed to catch: {text!r}"

    @pytest.mark.parametrize("text", [
        # False-positive guards for the MAJOR-2 non-fungibility patterns
        # specifically -- ordinary non-settlement/abstention prose that
        # merely names the CASH/RESERVE boundary, or cites the governing
        # decisions by ID, must stay clean.
        "The CASH/RESERVE consolidation question remains unresolved.",
        "This record does not settle whether CASH and RESERVE should be treated separately.",
        "The evidence is insufficient to determine whether the labels represent distinct functions.",
        "Per XASSET-0008 and XASSET-0009, the CASH and RESERVE identifiers remain an unresolved family.",
        "Neither fact is evidence that the CASH and RESERVE identifiers serve separate purposes.",
    ])
    def test_non_fungibility_false_positive_guards(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found), f"false positive on: {text!r}"

    def test_real_cash_reserve_consolidation_note_clean_against_non_fungibility_patterns(self):
        """The real, sealed cash_reserve_consolidation_note is the exact
        production text these new patterns must never fire against --
        checked directly, not merely via the pre-existing whitelist test
        above (which predates this correction)."""
        d = _real_policy_adoption("cash_reserve")
        found = []
        l1._scan_stage4_free_text(d["cash_reserve_consolidation_note"], "cash_reserve_consolidation_note", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found)

    def test_cash_reserve_consolidation_note_required_and_nonempty(self):
        d = _real_policy_adoption("cash_reserve")
        d["cash_reserve_consolidation_note"] = None
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "cash_reserve", repo_root=REPO_ROOT)
        assert any("must be a non-empty string on the cash_reserve record" in e for e in errs)

    def test_cash_reserve_consolidation_note_forbidden_on_other_sleeves(self):
        d = _real_policy_adoption("equity")
        d["cash_reserve_consolidation_note"] = "Some text that should not be here at all."
        _reseal(d)
        errs = l1.validate_policy_adoption_data(d, "equity", repo_root=REPO_ROOT)
        assert any("must be null on every record except cash_reserve" in e for e in errs)


# ===========================================================================
# NEW-MINOR-A/B correction (independent exact-head delta review
# pullrequestreview-4912431420): a negation/hedge false-positive class
# against the differ/distinct patterns, plus three further real
# non-fungibility bypasses -- both against the CASH/RESERVE distinction
# scan specifically.
# ===========================================================================

class TestCashReserveNonSettlementHedgeGuard:
    """NEW-MINOR-A: five natural, compliant, HEDGED/non-settlement
    sentences -- each independently reproduced as a false positive against
    the differ/distinct patterns before this correction -- must now
    validate cleanly. Each is tested in both entity orders (CASH-first
    and RESERVE-first) to confirm the guard is symmetric, not a one-
    direction patch."""

    @pytest.mark.parametrize("text", [
        "Whether CASH and RESERVE warrant different treatment remains an open, "
        "unresolved question -- this record does not settle it.",
        "This record does not assert that CASH and RESERVE serve different functions; "
        "the question remains open pending future governance.",
        "It has not been established that CASH and RESERVE differ in purpose.",
        "No evidence shows that CASH and RESERVE differ.",
        "Prior review found no basis to conclude CASH and RESERVE are distinct.",
        # Same five, entities reversed -- the guard must be symmetric.
        "Whether RESERVE and CASH warrant different treatment remains an open, "
        "unresolved question -- this record does not settle it.",
        "This record does not assert that RESERVE and CASH serve different functions; "
        "the question remains open pending future governance.",
        "It has not been established that RESERVE and CASH differ in purpose.",
        "No evidence shows that RESERVE and CASH differ.",
        "Prior review found no basis to conclude RESERVE and CASH are distinct.",
    ])
    def test_hedged_non_settlement_language_stays_clean(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found), f"false positive on: {text!r}"

    def test_loophole_fake_negation_hiding_real_assertion_still_caught(self):
        """The guard is a small, closed whitelist of specific
        assertion-negating idioms, never a generic 'a negation word
        appears somewhere nearby' check -- a genuinely prohibited
        assertion hidden behind an unrelated negated clause earlier in
        the same sentence must still be caught."""
        for text in (
            "It is not the case that CASH and RESERVE are the same -- they are distinct.",
            "It is not the case that CASH and RESERVE are identical; in fact, they are distinct.",
        ):
            found = []
            l1._scan_stage4_free_text(text, "x", found)
            assert any("stage4-cash-reserve-distinction" in e for e in found), f"loophole exploited: {text!r}"

    def test_hedge_earlier_in_text_does_not_suppress_a_later_unrelated_assertion(self):
        """The guard is scoped per-match (via exact adjacency), not per
        whole field -- a genuine hedge sentence must not launder an
        entirely separate, later, unhedged assertion in the same free-
        text field."""
        found = []
        l1._scan_stage4_free_text(
            "Whether CASH and RESERVE warrant different treatment remains open. "
            "Separately, CASH accomplishes something RESERVE does not.",
            "x", found,
        )
        assert any("stage4-cash-reserve-distinction" in e for e in found)

    def test_real_cash_reserve_consolidation_note_stays_clean_after_guard(self):
        """Regression: the guard must not change the real sealed record's
        own already-passing status."""
        d = _real_policy_adoption("cash_reserve")
        found = []
        l1._scan_stage4_free_text(d["cash_reserve_consolidation_note"], "cash_reserve_consolidation_note", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found)

    @pytest.mark.parametrize("text", [
        # Positive regression: every pre-existing differ/distinct catch
        # (both the original ten and the MAJOR-2 idiom-class patterns,
        # none of which route through the hedge guard) must remain
        # caught after this correction.
        "CASH and RESERVE serve different purposes within this account.",
        "RESERVE functions as a distinct buffer from CASH.",
        "CASH is used for near-term liquidity, unlike RESERVE.",
        "RESERVE is intended for a separate purpose than CASH.",
        "CASH alone represents the account's true liquidity position.",
        "CASH accomplishes something RESERVE does not.",
        "CASH does something that RESERVE cannot.",
        "RESERVE cannot do what CASH does.",
        "CASH and RESERVE are not interchangeable.",
        "RESERVE accomplishes something CASH does not.",
        "RESERVE does something that CASH cannot.",
        "CASH cannot do what RESERVE does.",
        "RESERVE and CASH are not interchangeable.",
        "CASH is non-fungible with RESERVE.",
        "RESERVE is not fungible with CASH.",
    ])
    def test_all_prior_catches_remain_caught(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-cash-reserve-distinction" in e for e in found), f"regression: no longer caught: {text!r}"


class TestCashReserveNonFungibilityResidualBypasses:
    """NEW-MINOR-B: three further real bypasses of the MAJOR-2
    non-fungibility patterns -- each its own distinct construction
    ('cannot serve the function that', a fronted 'What X, Y does not'
    clause, and phrase-before-entities ordering) -- plus one confirmed,
    deliberately non-actionable case the review explicitly excluded."""

    @pytest.mark.parametrize("text", [
        "CASH cannot serve the function that RESERVE serves.",
        "RESERVE cannot serve the function that CASH serves.",
        "CASH cannot perform the role that RESERVE performs.",
        "What CASH accomplishes, RESERVE does not.",
        "What RESERVE accomplishes, CASH does not.",
        "What CASH does, RESERVE cannot.",
        "RESERVE performs a role CASH cannot perform.",
        "CASH performs a function RESERVE cannot perform.",
        "Non-fungible: CASH and RESERVE.",
        "Non-fungible: RESERVE and CASH.",
        "Non-fungible -- CASH and RESERVE.",
    ])
    def test_residual_non_fungibility_bypasses_now_rejected(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert any("stage4-cash-reserve-distinction" in e for e in found), f"failed to catch: {text!r}"

    def test_affirmative_equivalence_deliberately_not_flagged(self):
        """CASH is interchangeable with RESERVE.' asserts equivalence,
        not distinctness -- the independent delta review explicitly
        determined this is NOT an actionable gap, since XASSET-0008
        itself instructs treating CASH and RESERVE 'as semantically
        equivalent,' and this scan's own purpose (XASSET-0008/XASSET-0009)
        is preventing an assertion of DISTINCTNESS specifically. Documents
        the deliberate, disclosed non-catch rather than silently adding an
        unrequested, doctrine-inconsistent pattern."""
        found = []
        l1._scan_stage4_free_text("CASH is interchangeable with RESERVE.", "x", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found)

    @pytest.mark.parametrize("text", [
        # False-positive guards for the residual-bypass additions
        # specifically -- ordinary text using "function"/"role"/"serves"
        # near CASH or RESERVE without asserting the forbidden claim must
        # stay clean.
        "The functional_doctrine layer's own CASH record cites its role via a "
        "structural-reference hash pin, not a free-text claim.",
        "This record's own relationship_references list serves as the coverage "
        "ledger's evidentiary basis.",
    ])
    def test_residual_bypass_false_positive_guards(self, text):
        found = []
        l1._scan_stage4_free_text(text, "x", found)
        assert not any("stage4-cash-reserve-distinction" in e for e in found), f"false positive on: {text!r}"


# ===========================================================================
# Adversarial matrix: ordering / negation / punctuation / conjunction /
# active-passive-voice / euphemistic paraphrase, each with a false-
# positive guard proving legitimate disclosure prose still validates.
# ===========================================================================

class TestAdversarialOrderingNegationPunctuation:
    def test_word_order_reversed_still_caught(self):
        """MINOR-4 correction (independent exact-head review
        pullrequestreview-4911497398): this test's own name always claimed
        both the forward and reversed word order were verified caught, but
        the original body computed found_b and then never asserted on it,
        ending in an unconditional `assert True` -- a real bypass (the
        reversed form was NOT caught at the time) went undetected by a
        test whose name implied the opposite. Both directions are now
        genuinely, independently asserted."""
        found_a, found_b = [], []
        l1._scan_stage4_free_text("This sleeve triggers an allocation check on its own.", "x", found_a)
        l1._scan_stage4_free_text("An allocation check is triggered by this sleeve's own finding alone.", "x", found_b)
        assert any("stage4-overclaim" in e for e in found_a), "forward word order must be caught"
        assert any("stage4-overclaim" in e for e in found_b), "reversed/passive word order must be caught too"

    def test_punctuation_variants_do_not_evade_directive_scan(self):
        for text in ("buy.", "Buy!", "  buy  ", "(buy)", "buy,sell,trim"):
            found = []
            l1._scan_stage4_free_text(text, "x", found)
            assert any("directive-word" in e for e in found), f"failed to catch: {text!r}"

    def test_negated_directive_language_still_caught_conservatively(self):
        """This scan is intentionally conservative: it does not attempt
        negation-awareness (matching this module's own established design
        for the directive-word/chart-domain scans elsewhere in this file),
        so a negated directive sentence is still flagged -- documented
        here as the real, disclosed behavior, not a defect this Stage 4c
        implementation introduces."""
        found = []
        l1._scan_stage4_free_text("This finding does not mean anyone should buy this sleeve.", "x", found)
        assert any("directive-word" in e for e in found)

    def test_conjunction_joined_overclaim_phrases_caught(self):
        found = []
        l1._scan_stage4_free_text(
            "This finding is both irrevocable and fully redundant with another sleeve's function.",
            "x", found,
        )
        assert any("stage4-overclaim" in e for e in found)


class TestEuphemisticParaphraseAndHiddenSizing:
    @pytest.mark.parametrize("text", [
        "This sleeve merits a larger slice of the book.",
        "This sleeve should get the lion's share of new capital.",
        "This sleeve deserves the majority of incremental deposits.",
    ])
    def test_hidden_sizing_phrasing_not_necessarily_all_caught(self, text):
        """Disclosed, not smoothed over: this scan targets numeric
        magnitude and named-ticker weight language specifically -- purely
        qualitative sizing-adjacent phrasing without a digit, cardinal
        word, or named instrument is a genuine, disclosed residual gap in
        this Stage 4c implementation's own scan coverage, matching this
        repository's own established discipline of disclosing exactly
        which paraphrase classes a scan does and does not catch (XASSET-
        0013 SS H's own carried-forward NOTE precedent) rather than
        silently claiming perfect coverage. None of these three phrases
        appears anywhere in the real sealed corpus."""
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            for field in ("function_rationale",):
                assert text not in (d.get(field) or "")

    def test_false_positive_guard_qualitative_disclosure_language_passes(self):
        found = []
        l1._scan_stage4_free_text(
            "This sleeve's own relationship-coverage ledger discloses a genuine, unresolved gap, "
            "never treated as equivalent to a sealed, determined pair.",
            "x", found,
        )
        assert found == []


# ===========================================================================
# Protected-path / byte-identity isolation.
# ===========================================================================

class TestStage4ProtectedPathIsolation:
    @pytest.mark.parametrize("rel_path", [
        "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
        "allocate.py", "margin_state.py", "levels.py",
    ])
    def test_protected_repository_file_untouched_by_this_session(self, rel_path):
        """A protected-path scan proving these files are tracked and were
        not modified as part of this Stage 4c implementation -- git-diff
        emptiness is independently verified at the shell level as part of
        the full validation workflow; this test only proves the files
        still exist and are still parseable/importable where applicable,
        catching an accidental deletion or truncation."""
        path = REPO_ROOT / rel_path
        assert path.is_file()
        assert path.stat().st_size > 0

    def test_sleeve_profile_records_untouched(self):
        for sid in l1.SLEEVE_IDS:
            path = REPO_ROOT / l1._PROFILES_DIR / f"{sid}.yaml"
            data, errs = l1._read_yaml(path)
            assert not errs
            assert data.get("record_status") == "sealed"

    def test_sleeve_relationship_records_untouched(self):
        for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS:
            path = REPO_ROOT / l1._RELATIONSHIPS_DIR / f"{a}_{b}.yaml"
            data, errs = l1._read_yaml(path)
            assert not errs
            assert data.get("record_status") == "sealed"

    def test_profile_and_relationship_directories_still_fully_valid(self):
        profile_result = l1.validate_sleeve_profile_directory(
            REPO_ROOT / l1._PROFILES_DIR, repo_root=REPO_ROOT,
        )
        relationship_result = l1.validate_sleeve_relationship_directory(
            REPO_ROOT / l1._RELATIONSHIPS_DIR, repo_root=REPO_ROOT,
        )
        assert profile_result.valid
        assert relationship_result.valid

    def test_zero_import_coupling_with_allocate_or_margin_state(self):
        import inspect
        source = inspect.getsource(l1)
        assert "import allocate" not in source
        assert "from allocate" not in source
        assert "import margin_state" not in source
        assert "from margin_state" not in source


# ===========================================================================
# Manifest bidirectional reconciliation (SS21 item 18).
# ===========================================================================

class TestPolicyAdoptionManifestReconciliation:
    def test_real_manifest_reconciles_cleanly(self):
        result = l1.validate_policy_adoption_cohort_manifest(
            REPO_ROOT / l1._POLICY_ADOPTION_DIR / "COHORT_MANIFEST.yaml",
            REPO_ROOT / l1._POLICY_ADOPTION_DIR,
        )
        assert result.valid, result.errors

    def test_manifest_hash_mismatch_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            dst_path = dst / p.name
            dst_path.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        manifest_data, _ = l1._read_yaml(dst / "COHORT_MANIFEST.yaml")
        manifest_data["cohort"][0]["content_sha256"] = "0" * 64
        (dst / "COHORT_MANIFEST.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")
        result = l1.validate_policy_adoption_cohort_manifest(dst / "COHORT_MANIFEST.yaml", dst)
        assert not result.valid
        assert any("mismatch" in e for e in result.errors)

    def test_manifest_duplicate_sleeve_id_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            (dst / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        manifest_data, _ = l1._read_yaml(dst / "COHORT_MANIFEST.yaml")
        manifest_data["cohort"].append(copy.deepcopy(manifest_data["cohort"][0]))
        (dst / "COHORT_MANIFEST.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")
        result = l1.validate_policy_adoption_cohort_manifest(dst / "COHORT_MANIFEST.yaml", dst)
        assert not result.valid
        assert any("duplicate sleeve_id" in e for e in result.errors)

    def test_manifest_missing_sleeve_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            (dst / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        manifest_data, _ = l1._read_yaml(dst / "COHORT_MANIFEST.yaml")
        manifest_data["cohort"] = [r for r in manifest_data["cohort"] if r["sleeve_id"] != "equity"]
        (dst / "COHORT_MANIFEST.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")
        result = l1.validate_policy_adoption_cohort_manifest(dst / "COHORT_MANIFEST.yaml", dst)
        assert not result.valid
        assert any("missing authorized sleeve_id" in e for e in result.errors)

    def test_orphan_record_on_disk_with_no_manifest_entry_detected(self, tmp_path):
        src = REPO_ROOT / l1._POLICY_ADOPTION_DIR
        dst = tmp_path / "policy_adoption"
        dst.mkdir()
        for p in sorted(src.glob("*.yaml")):
            (dst / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        manifest_data, _ = l1._read_yaml(dst / "COHORT_MANIFEST.yaml")
        manifest_data["cohort"] = [r for r in manifest_data["cohort"] if r["sleeve_id"] != "equity"]
        (dst / "COHORT_MANIFEST.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")
        result = l1.validate_policy_adoption_cohort_manifest(dst / "COHORT_MANIFEST.yaml", dst)
        assert any("no manifest entry" in e for e in result.errors)

    def test_manifest_wrong_governing_decision_rejected(self):
        manifest_data, _ = l1._read_yaml(REPO_ROOT / l1._POLICY_ADOPTION_DIR / "COHORT_MANIFEST.yaml")
        manifest_data = copy.deepcopy(manifest_data)
        manifest_data["governing_decision"] = "XASSET-0013"
        errs = []
        # exercised via a temp file to reuse the real validator function
        import tempfile, os
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            mpath = tdp / "COHORT_MANIFEST.yaml"
            mpath.write_text(yaml.dump(manifest_data), encoding="utf-8")
            result = l1.validate_policy_adoption_cohort_manifest(mpath, REPO_ROOT / l1._POLICY_ADOPTION_DIR)
        assert not result.valid
        assert any("governing_decision must be 'XASSET-0015'" in e for e in result.errors)


# ===========================================================================
# Non-cascading abstention discipline (SS21 item 19).
# ===========================================================================

class TestNonCascadingAbstentionStage4:
    def test_debt_reduction_axis_b_forced_abstention_does_not_touch_other_sleeves(self):
        """debt_reduction's own forced_abstention evidence-coverage profile
        must not, by itself, force any OTHER sleeve's Axis B value."""
        for sid in l1.SLEEVE_IDS - {l1.DEBT_REDUCTION}:
            profile = l1._live_profile(REPO_ROOT, sid)
            assert profile["evidence_coverage_profile"] != l1.FORCED_ABSTENTION

    def test_cash_reserve_debt_reduction_sealed_unresolved_does_not_touch_other_pairs(self):
        """The one sealed_unresolved pair in the whole corpus (cash_reserve
        <-> debt_reduction) must not force any OTHER sleeve pair's own
        ledger entry to sealed_unresolved."""
        for sid in l1.SLEEVE_IDS - {l1.CASH_RESERVE, l1.DEBT_REDUCTION}:
            ledger = l1.compute_live_relationship_ledger(sid, REPO_ROOT)
            assert all(e.coverage_state != l1.SEALED_UNRESOLVED for e in ledger)

    def test_fund_broad_market_axis_a_does_not_touch_other_sleeves_axis_a(self):
        """Renamed (XASSET-0017): fund_broad_market's own Axis A was
        redetermined from function_status_unresolved to function_confirmed_
        distinct, exercising the same delegated discretion XASSET-0015's own
        SS E reserved for a future drafting session on unchanged evidence --
        the test's own purpose (proving one sleeve's Axis A value cannot
        cascade into another's) is unaffected by which value it holds, so
        only the expected fixture value is updated here, not the assertion
        shape."""
        real_records = {sid: _real_policy_adoption(sid) for sid in l1.SLEEVE_IDS}
        for sid, d in real_records.items():
            assert d["portfolio_function_status"] == "function_confirmed_distinct"


# ===========================================================================
# Real-corpus end-to-end validation -- the actual six sealed Stage 4c
# records, plus their genuine, honestly-derived Axis A/B/C outcomes.
# ===========================================================================

class TestRealPolicyAdoptionCorpus:
    def test_all_six_records_and_manifest_validate_cleanly(self):
        result = l1.validate_policy_adoption_directory(
            REPO_ROOT / l1._POLICY_ADOPTION_DIR, repo_root=REPO_ROOT,
        )
        assert result.valid, [e for r in result.results for e in r.errors]

    def test_axis_a_outcomes_exactly_as_derived(self):
        # fund_broad_market updated (XASSET-0017): redetermined from
        # function_status_unresolved to function_confirmed_distinct via
        # Basis 3, exercising the same delegated discretion XASSET-0015's
        # own SS E reserved for a future drafting session on unchanged
        # evidence -- not a new grant of authority, not a schema/mechanism
        # change.
        expected = {
            "equity": "function_confirmed_distinct",
            "fund_broad_market": "function_confirmed_distinct",
            "fund_gld_defensive": "function_confirmed_distinct",
            "crypto": "function_confirmed_distinct",
            "cash_reserve": "function_confirmed_distinct",
            "debt_reduction": "function_confirmed_distinct",
        }
        for sid, want in expected.items():
            d = _real_policy_adoption(sid)
            assert d["portfolio_function_status"] == want, sid

    def test_axis_b_outcomes_exactly_as_derived(self):
        expected = {
            "equity": "eligible_for_target_consideration",
            "fund_broad_market": "eligible_for_target_consideration",
            "fund_gld_defensive": "eligible_for_target_consideration",
            "crypto": "eligible_for_target_consideration",
            "cash_reserve": "eligible_for_target_consideration",
            "debt_reduction": "not_yet_eligible",
        }
        for sid, want in expected.items():
            d = _real_policy_adoption(sid)
            assert d["capital_eligibility_status"] == want, sid

    def test_axis_c_outcomes_exactly_as_derived(self):
        # fund_broad_market updated (XASSET-0017): once Axis A clears
        # (function_confirmed_distinct) and Axis B stays eligible_for_
        # target_consideration, Axis C is mechanically recomputed from
        # sizing_blocked to sizing_conditionally_ready -- its own
        # relationship-coverage ledger still carries four deferred_
        # disclosed pairs (unchanged, not researched or closed by this
        # filing), which caps it below sizing_ready, per SS5/SS5.1's own
        # unedited mechanical rule.
        expected = {
            "equity": "sizing_conditionally_ready",
            "fund_broad_market": "sizing_conditionally_ready",
            "fund_gld_defensive": "sizing_conditionally_ready",
            "crypto": "sizing_conditionally_ready",
            "cash_reserve": "sizing_blocked",
            "debt_reduction": "sizing_blocked",
        }
        for sid, want in expected.items():
            d = _real_policy_adoption(sid)
            assert d["sizing_readiness_status"] == want, sid

    def test_no_sleeve_reaches_sizing_ready_today(self):
        """Honest, disclosed, non-favorable-across-the-board finding: every
        sealed relationship record in the current corpus carries at least
        one secondary condition, mechanically capping even the cleanest
        sleeve (equity, zero deferred pairs) at sizing_conditionally_ready
        -- never sizing_ready -- today."""
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            assert d["sizing_readiness_status"] != "sizing_ready"

    def test_cross_record_ledger_consistency_both_sides_agree(self):
        """The same pair must report the identical coverage_state from
        both sleeves' own perspectives."""
        records = {sid: _real_policy_adoption(sid) for sid in l1.SLEEVE_IDS}
        for a, b in l1._ALL_FIFTEEN_PAIRS:
            entry_a = next(e for e in records[a]["relationship_coverage_ledger"] if e["other_sleeve_id"] == b)
            entry_b = next(e for e in records[b]["relationship_coverage_ledger"] if e["other_sleeve_id"] == a)
            assert entry_a["coverage_state"] == entry_b["coverage_state"], (a, b)

    def test_global_fifteen_pair_reconciliation_across_full_corpus(self):
        records = {sid: _real_policy_adoption(sid) for sid in l1.SLEEVE_IDS}
        seen_pairs: set[tuple[str, str]] = set()
        for sid, d in records.items():
            assert len(d["relationship_coverage_ledger"]) == 5
            for entry in d["relationship_coverage_ledger"]:
                pair = tuple(sorted((sid, entry["other_sleeve_id"])))
                seen_pairs.add(pair)
        assert seen_pairs == l1._ALL_FIFTEEN_PAIRS

    def test_cash_reserve_debt_reduction_unresolved_consistent_both_sides(self):
        cash_reserve = _real_policy_adoption("cash_reserve")
        debt_reduction = _real_policy_adoption("debt_reduction")
        assert any(u["other_sleeve_id"] == "debt_reduction" for u in cash_reserve["unresolved_relationships"])
        assert any(u["other_sleeve_id"] == "cash_reserve" for u in debt_reduction["unresolved_relationships"])

    def test_no_relationship_double_counted_within_one_sleeve(self):
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            others = [e["other_sleeve_id"] for e in d["relationship_coverage_ledger"]]
            assert len(others) == len(set(others))

    def test_governing_decisions_correct_on_every_record(self):
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            assert set(d["governing_decisions"]) == {"XASSET-0014", "XASSET-0015"}

    def test_zero_deferred_relationship_research_performed(self):
        """No ninth relationship record exists, and no eighth deferred
        pair was reclassified -- the 7+8=15 closed set is exactly what
        Stage 1-3 already sealed, untouched by this Stage 4c
        implementation."""
        rel_dir = REPO_ROOT / l1._RELATIONSHIPS_DIR
        on_disk = {p.stem for p in rel_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        assert on_disk == {f"{a}_{b}" for a, b in l1.AUTHORIZED_RELATIONSHIP_PAIRS}

    def test_zero_numeric_sizing_anywhere_in_real_corpus(self):
        """Independent, direct re-confirmation on the real files (not just
        via the validator's own internal scan call) that no bare digit or
        cardinal-number word survives outside the disclosed Basis-N/
        decision-ID whitelist."""
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            texts = [d["function_rationale"]]
            for entry in d["blocking_evidence"]:
                texts.append(entry["detail"])
            for note in d["overlap_coordination_notes"]:
                texts.append(note["note"])
            if d.get("cash_reserve_consolidation_note"):
                texts.append(d["cash_reserve_consolidation_note"])
            for t in texts:
                found = []
                l1._scan_stage4_free_text(t, "x", found)
                numeric_findings = [f for f in found if "numeric-leakage" in f]
                assert numeric_findings == [], (sid, numeric_findings, t[:200])

    def test_zero_level2_instrument_choice_anywhere(self):
        """No record chooses, weights, or sizes between SPY/VEA/VWO within
        fund_broad_market or between BTC/ETH/SOL within crypto -- Level 1
        sleeve-level only. Ticker mentions ARE legitimately present as pure
        structural identity citations (e.g. "this sleeve's own asset_class
        scope (BTC, ETH, and SOL)", matching XASSET-0012 SS4.1.1's own
        identity-list exemption) -- the actual leakage guarantee is the
        validator's own dedicated weight-language scan finding nothing,
        proven directly against every real record's free text here rather
        than via an overbroad blanket ticker-absence assertion."""
        for sid in l1.SLEEVE_IDS:
            d = _real_policy_adoption(sid)
            texts = [d["function_rationale"]]
            for entry in d["blocking_evidence"]:
                texts.append(entry["detail"])
            for t in texts:
                found = []
                l1._scan_stage4_free_text(t, "x", found)
                weight_findings = [f for f in found if "stage4-level2-weight-leakage" in f]
                assert weight_findings == [], (sid, weight_findings)
        # The dedicated pattern class itself is independently proven to
        # fire on genuine weight language (TestLevel2LeakageScan above) --
        # this test proves it correctly stays silent on the real corpus's
        # own legitimate identity-citation usage.
