"""Tests for reconciliation_validator.py (WS-0005 Milestone 7 baseline-
reconciliation schema, TIER-0007 scope).

Schema/behavior tests below construct their own synthetic fixtures -- no
real ticker's judgment content is asserted against, matching
test_classification_validator.py/test_relationship_validator.py's own
authorized-scope discipline. A small number of tests exercise the real
repository's intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml
artifact, authored under this one implementation PR.
"""

import copy
from pathlib import Path

import pytest
import yaml

import reconciliation_validator as rv

REPO_ROOT = Path(__file__).resolve().parent
ARTIFACT_PATH = REPO_ROOT / "intelligence" / "reconciliation" / "MILESTONE7_BASELINE_RECONCILIATION.yaml"


# ── fixtures ─────────────────────────────────────────────────────────────

def _ticker_entry(ticker="ZZZA", **overrides) -> dict:
    entry = {
        "ticker": ticker,
        "sealed_economic_role": {
            "economic_system_ref": "AI & Compute Infrastructure",
            "company_role": "synthetic role",
            "role_basis": "synthetic role basis",
        },
        "current_role_context": {
            "portfolio_role_ref": "T1",
            "target_pct": 3.0,
            "gate_status": None,
            "note": "synthetic role-context note",
        },
        "role_comparison": "synthetic role comparison narrative",
        "sealed_capital_priority": {
            "status": "maintain_current_weight",
            "comparator_set": ["ZZZB", "ZZZC"],
            "rationale": "synthetic rationale",
            "assessed_date": "2026-08-05",
        },
        "current_capital_priority_context": "synthetic current capital-priority context, target_pct=3.0%",
        "capital_priority_comparison": "synthetic capital-priority comparison narrative",
        "target_context_comparison": {
            "status": "categorically_consistent",
            "rationale": "synthetic categorical rationale",
        },
        "sealed_risk_concentration": {
            "cluster_cap_membership": [],
            "issuer_lookthrough_membership": False,
            "relationship_record_coverage": [],
            "unmeasured_flag": True,
            "notes": "",
        },
        "current_structural_representation": {
            "cluster_cap_membership": [],
            "issuer_lookthrough_membership": False,
            "relationship_record_coverage": [],
            "computed_unmeasured": True,
        },
        "structural_risk_comparison": "synthetic structural-risk comparison narrative",
        "sealed_evidence_quality": {
            "primary_source_coverage": "comprehensive",
            "highest_disclosed_risk_severity": "moderate",
            "thesis_uncertainty_statement": "synthetic thesis uncertainty",
            "review_trigger_notes": "",
        },
        "current_evidence_posture": "synthetic current evidence posture",
        "evidence_quality_comparison": "synthetic evidence-quality comparison narrative",
        "primary_disposition": "aligned",
        "secondary_conditions": ["structural_measurement_gap"],
        "supporting_evidence": ["synthetic citation one", "synthetic citation two"],
        "uncertainty": "synthetic uncertainty narrative",
        "later_governance_action": "synthetic later-governance-action narrative",
    }
    entry.update(overrides)
    return entry


def _artifact(entries=None, **overrides) -> dict:
    if entries is None:
        entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZB", primary_disposition="divergence_requires_review", secondary_conditions=[])]
    data = {
        "schema_version": "1.0",
        "governing_decision": "TIER-0007",
        "artifact_purpose": "synthetic purpose",
        "source_main_sha": "0" * 40,
        "sealed_cohort_reference": {
            "governing_decision": "TIER-0005",
            "sealed_at_merge_commit": "1107c5b70801ff5e7027efddf6a2aa916030dce2",
            "cohort_manifest": "intelligence/classification/COHORT_MANIFEST.yaml",
            "record_count": 27,
        },
        "integrity_checks_performed": {
            "classification_validator_result": "OK (28 result(s))",
            "content_sha256_recomputation": "synthetic",
            "manifest_bidirectional_reconciliation": "synthetic",
            "lifecycle_status_sealed_confirmed": "synthetic",
            "diff_since_tier0006_merge": "zero diff (synthetic)",
            "comparison_source_main_sha": "0" * 40,
        },
        "chart_evidence_used": False,
        "reconciliation": entries,
        "aggregate": {"primary_disposition_counts": {}, "secondary_condition_counts": {}},
    }
    data.update(overrides)
    return data


# ── ticker-entry schema ─────────────────────────────────────────────────

def test_valid_entry_passes():
    result = rv.validate_ticker_entry(_ticker_entry(), index=0)
    assert result.valid, result.errors


def test_entry_missing_required_key_fails():
    entry = _ticker_entry()
    del entry["uncertainty"]
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("uncertainty" in e for e in result.errors)


def test_entry_extra_key_fails():
    entry = _ticker_entry()
    entry["conviction_score"] = 5
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_entry_not_a_mapping_fails():
    result = rv.validate_ticker_entry("not a dict", index=0)
    assert not result.valid


@pytest.mark.parametrize("field_name", list(rv._REQUIRED_NON_EMPTY_TEXT_FIELDS))
def test_required_text_fields_reject_empty_string(field_name):
    entry = _ticker_entry(**{field_name: ""})
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any(field_name in e for e in result.errors)


def test_supporting_evidence_must_be_non_empty_list():
    entry = _ticker_entry(supporting_evidence=[])
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_supporting_evidence_rejects_empty_string_citation():
    entry = _ticker_entry(supporting_evidence=["real citation", ""])
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


# ── primary_disposition ──────────────────────────────────────────────────

@pytest.mark.parametrize("value", sorted(rv._PRIMARY_DISPOSITIONS))
def test_primary_disposition_accepts_each_closed_value(value):
    entry = _ticker_entry(primary_disposition=value)
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_primary_disposition_rejects_unknown_value():
    entry = _ticker_entry(primary_disposition="strongly_recommend_buy")
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("primary_disposition" in e for e in result.errors)


def test_primary_disposition_none_fails():
    entry = _ticker_entry(primary_disposition=None)
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


# ── secondary_conditions ─────────────────────────────────────────────────

def test_secondary_conditions_accepts_empty_list():
    entry = _ticker_entry(secondary_conditions=[])
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_secondary_conditions_accepts_both_values():
    entry = _ticker_entry(secondary_conditions=["unresolved_evidence", "structural_measurement_gap"])
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_secondary_conditions_rejects_unknown_value():
    entry = _ticker_entry(secondary_conditions=["chart_pattern_bullish"])
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_secondary_conditions_rejects_duplicate():
    entry = _ticker_entry(secondary_conditions=["unresolved_evidence", "unresolved_evidence"])
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("duplicate" in e for e in result.errors)


def test_secondary_conditions_rejects_more_than_two():
    entry = _ticker_entry(secondary_conditions=["unresolved_evidence", "structural_measurement_gap", "unresolved_evidence"])
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_secondary_conditions_rejects_non_list():
    entry = _ticker_entry(secondary_conditions="unresolved_evidence")
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


# ── target_context_comparison ────────────────────────────────────────────

@pytest.mark.parametrize("status", sorted(rv._TARGET_CONTEXT_STATUSES))
def test_target_context_comparison_accepts_each_closed_value(status):
    entry = _ticker_entry(target_context_comparison={"status": status, "rationale": "synthetic"})
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_target_context_comparison_rejects_unknown_status():
    entry = _ticker_entry(target_context_comparison={"status": "bullish", "rationale": "synthetic"})
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_target_context_comparison_requires_rationale():
    entry = _ticker_entry(target_context_comparison={"status": "categorically_consistent", "rationale": ""})
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


# ── prohibited numeric target / recommendation content ───────────────────

def test_forbidden_key_proposed_target_pct_rejected():
    entry = _ticker_entry()
    entry["target_context_comparison"]["proposed_target_pct"] = 4.5
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("proposed_target_pct" in e for e in result.errors)


def test_forbidden_key_score_rejected():
    entry = _ticker_entry()
    entry["current_capital_priority_context"] = {"score": 7}
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_forbidden_key_ranking_rejected():
    entry = _ticker_entry()
    entry["sealed_capital_priority"]["ranking"] = 1
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_target_pct_permitted_in_current_role_context():
    entry = _ticker_entry()
    entry["current_role_context"]["target_pct"] = 5.0
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_target_pct_permitted_in_current_capital_priority_context_dict_form():
    entry = _ticker_entry(current_capital_priority_context={"target_pct": 2.25, "note": "synthetic"})
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_target_pct_rejected_outside_permitted_contexts():
    entry = _ticker_entry()
    entry["structural_risk_comparison"] = "synthetic narrative"
    entry["sealed_risk_concentration"]["target_pct"] = 3.0
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("target_pct" in e for e in result.errors)


@pytest.mark.parametrize(
    "phrase",
    [
        "the target should be increased to 4%",
        "we recommend a target of 5%",
        "this warrants a new target percentage",
        "issuing a buy recommendation",
        "issuing a sell recommendation",
        "issuing a trim recommendation",
    ],
)
def test_forbidden_recommendation_phrases_rejected(phrase):
    entry = _ticker_entry(uncertainty=phrase)
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("forbidden recommendation-shaped phrase" in e for e in result.errors)


def test_ordinary_target_pct_citation_prose_is_permitted():
    entry = _ticker_entry(
        current_capital_priority_context="Destination target_pct=3.0% is configured; no active reconsideration flag exists."
    )
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


# ── artifact-level schema ────────────────────────────────────────────────

def test_valid_artifact_passes_without_universe_check():
    data = _artifact()
    result = rv.validate_reconciliation_data(data)
    # 2-ticker synthetic artifact will fail the "exactly 27" count check but
    # nothing else -- isolate that specific, expected failure.
    assert all("exactly 27" in e for e in result.errors), result.errors


def test_artifact_governing_decision_must_be_tier_0007():
    data = _artifact(governing_decision="TIER-0006")
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("governing_decision" in e for e in result.errors)


def test_artifact_chart_evidence_used_must_be_false():
    data = _artifact(chart_evidence_used=True)
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("chart_evidence_used" in e for e in result.errors)


def test_artifact_chart_evidence_used_missing_fails():
    data = _artifact()
    del data["chart_evidence_used"]
    result = rv.validate_reconciliation_data(data)
    assert not result.valid


def test_artifact_source_main_sha_required():
    data = _artifact(source_main_sha="")
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("source_main_sha" in e for e in result.errors)


def test_artifact_sealed_cohort_reference_must_match_tier0006_merge():
    data = _artifact()
    data["sealed_cohort_reference"]["sealed_at_merge_commit"] = "deadbeef" * 5
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("sealed_at_merge_commit" in e for e in result.errors)


def test_artifact_integrity_checks_diff_required():
    data = _artifact()
    del data["integrity_checks_performed"]["diff_since_tier0006_merge"]
    result = rv.validate_reconciliation_data(data)
    assert not result.valid


def test_artifact_top_level_extra_key_fails():
    data = _artifact()
    data["proposed_new_targets"] = {}
    result = rv.validate_reconciliation_data(data)
    assert not result.valid


def test_artifact_reconciliation_not_a_list_fails():
    data = _artifact(reconciliation="ZZZA")
    result = rv.validate_reconciliation_data(data)
    assert not result.valid


def test_artifact_duplicate_ticker_fails():
    entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("duplicate" in e for e in result.errors)


def test_artifact_non_alphabetical_order_fails():
    entries = [_ticker_entry("ZZZB"), _ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    result = rv.validate_reconciliation_data(data)
    assert not result.valid
    assert any("alphabetical" in e for e in result.errors)


def test_artifact_missing_required_universe_ticker_fails():
    entries = [_ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    universe = frozenset({"ZZZA", "ZZZB"})
    result = rv.validate_reconciliation_data(data, canonical_universe=universe)
    assert not result.valid
    assert any("missing required ticker" in e for e in result.errors)


def test_artifact_extra_ticker_outside_universe_fails():
    entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZQ", primary_disposition="aligned")]
    data = _artifact(entries=entries)
    universe = frozenset({"ZZZA"})
    result = rv.validate_reconciliation_data(data, canonical_universe=universe)
    assert not result.valid
    assert any("outside the sealed 27-name population" in e for e in result.errors)


def test_artifact_exact_universe_match_passes_count_check():
    entries = [_ticker_entry(t, primary_disposition="aligned") for t in ("ZZZA", "ZZZB")]
    data = _artifact(entries=entries)
    universe = frozenset({"ZZZA", "ZZZB"})
    result = rv.validate_reconciliation_data(data, sealed_universe=universe)
    # Passes ticker-set/order checks; still fails the fixed "exactly 27" rule
    # since this is a 2-ticker synthetic fixture, not the real 27-name cohort.
    assert all("exactly 27" in e for e in result.errors), result.errors


# ── real repository artifact ─────────────────────────────────────────────

def test_real_artifact_file_parses_and_validates():
    assert ARTIFACT_PATH.is_file()
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from relationship_validator import load_canonical_universe

    canonical = load_canonical_universe(REPO_ROOT)
    result = rv.validate_reconciliation_file(ARTIFACT_PATH, canonical_universe=canonical, sealed_universe=canonical)
    assert result.valid, result.errors


def test_real_artifact_covers_exactly_the_27_sealed_tickers():
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    import classification_validator as clv

    classification_dir = REPO_ROOT / "intelligence" / "classification"
    sealed_tickers = {
        p.stem for p in classification_dir.glob("*.yaml") if p.stem != "COHORT_MANIFEST"
    }
    assert len(sealed_tickers) == 27

    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    reconciled_tickers = {entry["ticker"] for entry in data["reconciliation"]}
    assert reconciled_tickers == sealed_tickers


def test_real_artifact_zero_coupling_with_allocate_or_margin_state():
    text = (REPO_ROOT / "reconciliation_validator.py").read_text()
    assert "import allocate" not in text
    assert "import margin_state" not in text
    assert "from allocate" not in text
    assert "from margin_state" not in text


def test_real_artifact_no_edit_to_sealed_classification_records():
    """This validator/artifact must never itself be the thing that opens a
    sealed record in write mode -- static import-shape check."""
    text = Path(__file__).with_name("reconciliation_validator.py").read_text()
    assert '"w"' not in text
    assert "'w'" not in text
    assert '"a"' not in text
    assert "'a'" not in text


def test_real_artifact_aggregate_counts_are_internally_consistent():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    entries = data["reconciliation"]
    counts = data["aggregate"]["primary_disposition_counts"]
    total = sum(len(v) for v in counts.values())
    assert total == 27
    for disposition, tickers in counts.items():
        actual = sorted(e["ticker"] for e in entries if e["primary_disposition"] == disposition)
        assert actual == sorted(tickers), disposition


def test_real_artifact_secondary_condition_counts_are_internally_consistent():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    entries = data["reconciliation"]
    counts = data["aggregate"]["secondary_condition_counts"]
    for condition, tickers in counts.items():
        actual = sorted(e["ticker"] for e in entries if condition in e["secondary_conditions"])
        assert actual == sorted(tickers), condition


def test_real_artifact_no_ticker_has_more_than_two_secondary_conditions():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    for entry in data["reconciliation"]:
        assert len(entry["secondary_conditions"]) <= 2


def test_real_artifact_deep_copy_round_trip_is_stable():
    """Sanity check that the artifact is pure data (no yaml aliasing/anchors
    that could silently share mutable state across entries)."""
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    cloned = copy.deepcopy(data)
    cloned["reconciliation"][0]["primary_disposition"] = "no_policy_conclusion"
    assert data["reconciliation"][0]["primary_disposition"] != "no_policy_conclusion"
