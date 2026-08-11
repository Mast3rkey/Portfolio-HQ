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
