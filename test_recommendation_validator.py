"""Tests for recommendation_validator.py (WS-0005 Milestone 8 policy-
recommendation-package schema, TIER-0009 scope).

Schema/behavior tests below construct their own synthetic fixtures -- no
real ticker's judgment content is asserted against, matching
test_classification_validator.py/test_reconciliation_validator.py's own
authorized-scope discipline. A small number of tests exercise the real
repository's
intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml
artifact, authored under this one implementation PR.
"""

import copy
import re
from pathlib import Path

import pytest
import yaml

import recommendation_validator as rv

REPO_ROOT = Path(__file__).resolve().parent
ARTIFACT_PATH = REPO_ROOT / "intelligence" / "recommendations" / "MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml"


# ── fixtures ─────────────────────────────────────────────────────────────

def _area_entry(primary_status="retain_current_baseline", secondary_conditions=None, **overrides) -> dict:
    entry = {
        "primary_status": primary_status,
        "secondary_conditions": list(secondary_conditions) if secondary_conditions else [],
        "rationale": "synthetic rationale narrative",
        "supporting_evidence": ["synthetic citation one"],
        "later_governance_action": (
            "None -- synthetic, no gap to escalate."
            if primary_status == "retain_current_baseline"
            else "synthetic future governance action naming a real step"
        ),
    }
    entry.update(overrides)
    return entry


def _policy_areas(**area_overrides) -> dict:
    base = {
        "role": _area_entry(),
        "tier_architecture": _area_entry(),
        "capital_priority": _area_entry(),
        "target_and_range": _area_entry(primary_status="valuation_required"),
        "maximum_position_size": _area_entry(primary_status="valuation_required"),
        "overlap_and_concentration": _area_entry(),
        "monitoring_and_thesis_break": _area_entry(),
        "add_hold_trim_exit_discipline": _area_entry(),
    }
    base.update(area_overrides)
    return base


def _ticker_entry(ticker="ZZZA", **overrides) -> dict:
    entry = {
        "ticker": ticker,
        "milestone7_reference": {"primary_disposition": "aligned", "secondary_conditions": []},
        "policy_areas": _policy_areas(),
        "uncertainty": "synthetic uncertainty narrative",
    }
    entry.update(overrides)
    return entry


def _aggregate_for(entries: list[dict]) -> dict:
    return rv._recompute_aggregate(entries) | {
        "cross_tabulation_disclaimer": "synthetic disclaimer -- no score, rank, or implied action priority is derived from any count."
    }


def _artifact(entries=None, **overrides) -> dict:
    if entries is None:
        entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZB")]
    data = {
        "schema_version": "1.0",
        "governing_decision": "TIER-0009",
        "artifact_purpose": "synthetic purpose describing the eight policy areas, including add/hold/trim/exit-review discipline",
        "source_main_sha": "0" * 40,
        "milestone_references": {
            "milestone6_governing_decision": "TIER-0006",
            "milestone6_sealed_at_merge_commit": "1107c5b70801ff5e7027efddf6a2aa916030dce2",
            "milestone7_governing_decision": "TIER-0008",
            "milestone7_artifact": "intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml",
            "milestone7_source_main_sha": "1" * 40,
        },
        "integrity_checks_performed": {"synthetic_check": "OK"},
        "chart_evidence_used": False,
        "equity_scope_disclosure": (
            "This recommendation package covers the 27 canonical equity destinations only. "
            "ETF, cryptocurrency, cash/reserve, GLD/defensive-asset, debt-reduction, and "
            "broader contender-universe policy remain governed separately."
        ),
        "generation_date": "2026-08-07",
        "cohort_size": 27,
        "recommendations": entries,
        "aggregate": _aggregate_for(entries),
    }
    data.update(overrides)
    return data


# ── area-entry schema ────────────────────────────────────────────────────

def test_valid_area_entry_passes():
    errors: list[str] = []
    rv.validate_area_entry(_area_entry(), ticker="ZZZA", area="role", errors=errors)
    assert not errors


def test_area_entry_missing_required_key_fails():
    entry = _area_entry()
    del entry["rationale"]
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("missing required key" in e for e in errors)


def test_area_entry_extra_key_fails():
    entry = _area_entry()
    entry["extra_field"] = "not permitted"
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("unexpected key" in e for e in errors)


def test_area_entry_not_a_mapping_fails():
    errors: list[str] = []
    rv.validate_area_entry("not a mapping", ticker="ZZZA", area="role", errors=errors)
    assert any("must be a mapping" in e for e in errors)


# ── primary_status vocabulary and area restriction ──────────────────────

@pytest.mark.parametrize("value", sorted(rv._PRIMARY_STATUSES))
def test_primary_status_is_a_closed_seven_value_vocabulary(value):
    assert value in rv._PRIMARY_STATUSES


def test_primary_status_rejects_unknown_value():
    entry = _area_entry(primary_status="not_a_real_status")
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("is not one of" in e for e in errors)


@pytest.mark.parametrize(
    "area,allowed",
    sorted(rv._AREA_ALLOWED_PRIMARY.items()),
)
def test_every_reachable_primary_status_per_area_passes(area, allowed):
    for value in sorted(allowed):
        entry = _area_entry(primary_status=value)
        errors: list[str] = []
        rv.validate_area_entry(entry, ticker="ZZZA", area=area, errors=errors)
        assert not errors, (area, value, errors)


@pytest.mark.parametrize("area", list(rv._AREA_KEYS))
def test_primary_status_not_reachable_for_area_fails(area):
    unreachable = sorted(rv._PRIMARY_STATUSES - rv._AREA_ALLOWED_PRIMARY[area])
    if not unreachable:
        pytest.skip(f"{area} permits every primary_status value")
    entry = _area_entry(primary_status=unreachable[0])
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area=area, errors=errors)
    assert any("is not reachable for area" in e for e in errors)


def test_target_and_range_only_permits_valuation_required():
    assert rv._AREA_ALLOWED_PRIMARY["target_and_range"] == frozenset({"valuation_required"})


def test_maximum_position_size_only_permits_valuation_required():
    assert rv._AREA_ALLOWED_PRIMARY["maximum_position_size"] == frozenset({"valuation_required"})


# ── secondary_conditions ─────────────────────────────────────────────────

def test_secondary_conditions_accepts_empty_list():
    errors: list[str] = []
    rv.validate_area_entry(_area_entry(secondary_conditions=[]), ticker="ZZZA", area="role", errors=errors)
    assert not errors


def test_secondary_conditions_accepts_unresolved_evidence_alone():
    errors: list[str] = []
    rv.validate_area_entry(
        _area_entry(secondary_conditions=["unresolved_evidence"]), ticker="ZZZA", area="role", errors=errors
    )
    assert not errors


def test_secondary_conditions_accepts_structural_measurement_gap_alone_on_role():
    errors: list[str] = []
    rv.validate_area_entry(
        _area_entry(secondary_conditions=["structural_measurement_gap"]), ticker="ZZZA", area="role", errors=errors
    )
    assert not errors


def test_secondary_conditions_accepts_both_together_on_role():
    errors: list[str] = []
    rv.validate_area_entry(
        _area_entry(secondary_conditions=["unresolved_evidence", "structural_measurement_gap"]),
        ticker="ZZZA",
        area="role",
        errors=errors,
    )
    assert not errors


def test_secondary_conditions_rejects_unknown_value():
    errors: list[str] = []
    rv.validate_area_entry(_area_entry(secondary_conditions=["made_up_flag"]), ticker="ZZZA", area="role", errors=errors)
    assert any("unknown value" in e for e in errors)


def test_secondary_conditions_rejects_duplicate():
    errors: list[str] = []
    rv.validate_area_entry(
        _area_entry(secondary_conditions=["unresolved_evidence", "unresolved_evidence"]),
        ticker="ZZZA",
        area="role",
        errors=errors,
    )
    assert any("duplicate" in e for e in errors)


def test_secondary_conditions_rejects_more_than_two():
    errors: list[str] = []
    entry = _area_entry()
    entry["secondary_conditions"] = ["unresolved_evidence", "structural_measurement_gap", "unresolved_evidence"]
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("maximum is two" in e or "duplicate" in e for e in errors)


def test_secondary_conditions_rejects_non_list():
    entry = _area_entry()
    entry["secondary_conditions"] = "unresolved_evidence"
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("must be a list" in e for e in errors)


def test_overlap_area_rejects_structural_measurement_gap_as_secondary():
    """TIER-0009 SS H: for overlap_and_concentration, the structural gap is
    the primary-status-forcing condition -- never a secondary annotation."""
    entry = _area_entry(
        primary_status="retain_current_baseline", secondary_conditions=["structural_measurement_gap"]
    )
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="overlap_and_concentration", errors=errors)
    assert any("forbidden as a secondary flag" in e for e in errors)


def test_overlap_area_permits_unresolved_evidence_as_secondary():
    entry = _area_entry(primary_status="retain_current_baseline", secondary_conditions=["unresolved_evidence"])
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="overlap_and_concentration", errors=errors)
    assert not errors


# ── rationale / supporting_evidence / later_governance_action ───────────

def test_rationale_must_be_non_empty_string():
    entry = _area_entry()
    entry["rationale"] = ""
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("rationale must be a non-empty string" in e for e in errors)


def test_supporting_evidence_must_be_non_empty_list():
    entry = _area_entry()
    entry["supporting_evidence"] = []
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("supporting_evidence must be a non-empty list" in e for e in errors)


def test_supporting_evidence_rejects_empty_string_citation():
    entry = _area_entry()
    entry["supporting_evidence"] = [""]
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("supporting_evidence must be a non-empty list" in e for e in errors)


def test_later_governance_action_missing_fails():
    entry = _area_entry()
    entry["later_governance_action"] = ""
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("later_governance_action must be a non-empty string" in e for e in errors)


def test_later_governance_action_required_when_not_retain_current_baseline():
    entry = _area_entry(primary_status="review_warranted", later_governance_action="None -- nothing to do.")
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert any("must name a real future action" in e for e in errors)


def test_later_governance_action_none_is_fine_for_retain_current_baseline():
    entry = _area_entry(primary_status="retain_current_baseline", later_governance_action="None -- no gap.")
    errors: list[str] = []
    rv.validate_area_entry(entry, ticker="ZZZA", area="role", errors=errors)
    assert not errors


# ── prohibited content: forbidden keys ───────────────────────────────────

@pytest.mark.parametrize("key", sorted(rv._FORBIDDEN_KEY_NAMES))
def test_forbidden_key_names_rejected(key):
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["role"][key] = "smuggled numeric field"
    errors: list[str] = []
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("forbidden key name" in e for e in result.errors)


def test_forbidden_key_target_range_nested_inside_evidence_dict_rejected():
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["target_and_range"]["supporting_evidence"] = [{"target_range": "10-15%"}]
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("forbidden key name" in e for e in result.errors)


# ── prohibited content: forbidden recommendation-shaped phrases ─────────

@pytest.mark.parametrize(
    "phrase",
    [
        "should be increased to 5%",
        "recommend a target of 4.0%",
        "new target percentage",
        "buy recommendation",
        "sell recommendation",
        "trim recommendation",
    ],
)
def test_forbidden_recommendation_phrases_rejected(phrase):
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["role"]["rationale"] = f"synthetic text containing: {phrase}"
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


# ── prohibited content: numeric-percent-shaped tokens (G.4/G.5 only) ────

def test_percent_token_rejected_in_target_and_range_rationale():
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["target_and_range"]["rationale"] = "synthetic text citing 12.5% somewhere"
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("numeric-percent-shaped token" in e for e in result.errors)


def test_percent_token_rejected_in_maximum_position_size_supporting_evidence():
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["maximum_position_size"]["supporting_evidence"] = ["cites 8% ceiling"]
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("numeric-percent-shaped token" in e for e in result.errors)


def test_percent_token_permitted_outside_g4_g5_areas():
    """Milestone 7's own already-accepted content legitimately carries
    disclosed financial percentages (revenue mix, growth rates) in
    role/capital_priority/uncertainty text -- only the two doctrinally-fixed
    numeric areas are percent-restricted."""
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["role"]["rationale"] = "AWS operating income grew 28% YoY per the sealed record"
    entry["uncertainty"] = "customer concentration at 21%/17%/16% of revenue"
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


# ── prohibited content: directive language ───────────────────────────────

@pytest.mark.parametrize("word", list(rv._DIRECTIVE_WORDS))
def test_each_directive_word_is_caught_as_an_actual_directive(word):
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["add_hold_trim_exit_discipline"]["rationale"] = f"{word.capitalize()} this position now."
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("directive word" in e for e in result.errors), result.errors


def test_directive_word_hold_does_not_false_positive_on_holdings_noun():
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["role"]["rationale"] = "current holdings.yaml describes the factual position"
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_real_style_absence_of_directive_language_passes():
    """The pattern this repository's own generated content actually uses --
    describing the *absence* of a directive without using the literal
    directive vocabulary."""
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["add_hold_trim_exit_discipline"]["rationale"] = (
        "A review-trigger mechanism exists and appears adequate. This area-entry "
        "issues no directional instruction, sizing action, or timing directive of "
        "any kind, under any framing, for the position itself."
    )
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


def test_directive_word_scan_does_not_apply_to_top_level_metadata():
    """Top-level artifact_purpose must be free to name the eighth policy
    area ('add/hold/trim/exit-review discipline') by title."""
    data = _artifact()
    assert "add/hold/trim/exit" in data["artifact_purpose"]
    result = rv.validate_recommendation_data(data, sealed_universe=frozenset({"ZZZA", "ZZZB"}))
    # Fails only on the fixed "exactly 27" population rule, never on the
    # directive-word scan against artifact_purpose.
    assert not any("directive word" in e for e in result.errors)


# ── prohibited content: chart-derived terminology ────────────────────────

@pytest.mark.parametrize(
    "term",
    [
        "support level",
        "resistance level",
        "breakout above",
        "trend line",
        "moving average crossover",
        "RSI reading",
        "MACD signal",
        "candlestick pattern",
        "chart pattern forming",
        "technical analysis suggests",
        "oversold conditions",
        "overbought territory",
        "Fibonacci retracement",
        "volume profile",
        "price target of",
        "momentum indicator",
    ],
)
def test_chart_terminology_rejected(term):
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["role"]["rationale"] = f"synthetic text noting {term} here"
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("chart-derived terminology" in e for e in result.errors), result.errors


def test_ordinary_support_word_does_not_leak_when_avoided():
    """This repository's own generated rationale avoids the bare word
    'support' entirely -- the real artifact (tested below) proves the
    generated content is chart-term-clean without relying on a narrower
    scan than TIER-0009 requires."""
    entry = _ticker_entry("ZZZA")
    entry["policy_areas"]["target_and_range"]["rationale"] = (
        "no governed valuation methodology of any kind exists anywhere in this "
        "repository capable of producing a numeric target or target range"
    )
    result = rv.validate_ticker_entry(entry, index=0)
    assert result.valid, result.errors


# ── ticker-entry schema ───────────────────────────────────────────────────

def test_valid_ticker_entry_passes():
    result = rv.validate_ticker_entry(_ticker_entry(), index=0)
    assert result.valid, result.errors


def test_ticker_entry_missing_required_key_fails():
    entry = _ticker_entry()
    del entry["uncertainty"]
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("missing required key" in e for e in result.errors)


def test_ticker_entry_extra_key_fails():
    entry = _ticker_entry()
    entry["extra_top_field"] = "nope"
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("unexpected key" in e for e in result.errors)


def test_ticker_entry_not_a_mapping_fails():
    result = rv.validate_ticker_entry("not a mapping", index=0)
    assert not result.valid


def test_ticker_entry_missing_policy_area_fails():
    entry = _ticker_entry()
    del entry["policy_areas"]["monitoring_and_thesis_break"]
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("missing required area" in e for e in result.errors)


def test_ticker_entry_extra_policy_area_fails():
    entry = _ticker_entry()
    entry["policy_areas"]["ninth_bogus_area"] = _area_entry()
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("unexpected area" in e for e in result.errors)


def test_milestone7_reference_requires_valid_primary_disposition():
    entry = _ticker_entry()
    entry["milestone7_reference"]["primary_disposition"] = "not_real"
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid


def test_uncertainty_missing_fails():
    entry = _ticker_entry()
    entry["uncertainty"] = ""
    result = rv.validate_ticker_entry(entry, index=0)
    assert not result.valid
    assert any("uncertainty must be a non-empty string" in e for e in result.errors)


# ── artifact-level schema ─────────────────────────────────────────────────

def test_valid_artifact_passes_without_universe_check():
    data = _artifact()
    result = rv.validate_recommendation_data(data, sealed_universe=frozenset({"ZZZA", "ZZZB"}))
    assert all("exactly 27" in e for e in result.errors), result.errors


@pytest.mark.parametrize("bad_top_level", [None, "not a mapping", ["a", "list"], 42, True])
def test_validate_recommendation_data_rejects_non_dict_top_level(bad_top_level):
    result = rv.validate_recommendation_data(bad_top_level)
    assert not result.valid
    assert any("must be a mapping" in e for e in result.errors)
    assert result.source == "MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml"


def test_artifact_governing_decision_must_be_tier_0009():
    data = _artifact(governing_decision="TIER-0001")
    result = rv.validate_recommendation_data(data)
    assert any("governing_decision must be" in e for e in result.errors)


def test_artifact_chart_evidence_used_must_be_false():
    data = _artifact(chart_evidence_used=True)
    result = rv.validate_recommendation_data(data)
    assert any("chart_evidence_used must be exactly" in e for e in result.errors)


def test_artifact_cohort_size_must_be_27():
    data = _artifact(cohort_size=26)
    result = rv.validate_recommendation_data(data)
    assert any("cohort_size must be exactly 27" in e for e in result.errors)


def test_artifact_equity_scope_disclosure_required():
    data = _artifact(equity_scope_disclosure="unrelated text")
    result = rv.validate_recommendation_data(data)
    assert any("equity_scope_disclosure" in e for e in result.errors)


def test_artifact_source_main_sha_required():
    data = _artifact(source_main_sha="")
    result = rv.validate_recommendation_data(data)
    assert any("source_main_sha" in e for e in result.errors)


def test_artifact_milestone_references_wrong_governing_decision_fails():
    data = _artifact()
    data["milestone_references"]["milestone6_governing_decision"] = "TIER-0001"
    result = rv.validate_recommendation_data(data)
    assert any("milestone6_governing_decision" in e for e in result.errors)


def test_artifact_milestone_references_wrong_merge_commit_fails():
    data = _artifact()
    data["milestone_references"]["milestone6_sealed_at_merge_commit"] = "f" * 40
    result = rv.validate_recommendation_data(data)
    assert any("does not match the known TIER-0006 merge commit" in e for e in result.errors)


def test_artifact_top_level_extra_key_fails():
    data = _artifact()
    data["bogus_top_level"] = True
    result = rv.validate_recommendation_data(data)
    assert any("unexpected key" in e for e in result.errors)


def test_artifact_top_level_missing_key_fails():
    data = _artifact()
    del data["integrity_checks_performed"]
    result = rv.validate_recommendation_data(data)
    assert any("missing required key" in e for e in result.errors)


def test_artifact_recommendations_not_a_list_fails():
    data = _artifact()
    data["recommendations"] = "not a list"
    result = rv.validate_recommendation_data(data)
    assert any("recommendations must be a list" in e for e in result.errors)


def test_artifact_duplicate_ticker_fails():
    entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    result = rv.validate_recommendation_data(data)
    assert any("duplicate ticker" in e for e in result.errors)


def test_artifact_wrong_ticker_order_fails():
    entries = [_ticker_entry("ZZZB"), _ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    result = rv.validate_recommendation_data(data)
    assert any("alphabetical" in e for e in result.errors)


def test_artifact_missing_required_universe_ticker_fails():
    entries = [_ticker_entry("ZZZA")]
    data = _artifact(entries=entries)
    universe = frozenset({"ZZZA", "ZZZB"})
    result = rv.validate_recommendation_data(data, sealed_universe=universe)
    assert any("missing required ticker" in e for e in result.errors)


def test_artifact_extra_ticker_outside_universe_fails():
    entries = [_ticker_entry("ZZZA"), _ticker_entry("ZZZQ")]
    data = _artifact(entries=entries)
    universe = frozenset({"ZZZA", "ZZZB"})
    result = rv.validate_recommendation_data(data, sealed_universe=universe)
    assert any("outside the sealed 27-name population" in e for e in result.errors)


# ── G.4/G.5 forced check ─────────────────────────────────────────────────

def test_g4_target_and_range_wrong_forced_value_fails():
    entries = [
        _ticker_entry("ZZZA", policy_areas=_policy_areas(target_and_range=_area_entry())),
        _ticker_entry("ZZZB"),
    ]
    data = _artifact(entries=entries)
    result = rv.validate_recommendation_data(data)
    assert any(
        "target_and_range.primary_status must be exactly 'valuation_required'" in e for e in result.errors
    )


def test_g5_maximum_position_size_wrong_forced_value_fails():
    entries = [
        _ticker_entry("ZZZA", policy_areas=_policy_areas(maximum_position_size=_area_entry())),
        _ticker_entry("ZZZB"),
    ]
    data = _artifact(entries=entries)
    result = rv.validate_recommendation_data(data)
    assert any(
        "maximum_position_size.primary_status must be exactly 'valuation_required'" in e for e in result.errors
    )


def test_g4_g5_correct_forced_value_passes_that_check():
    data = _artifact()
    result = rv.validate_recommendation_data(data)
    assert not any("valuation_required" in e and "must be exactly" in e for e in result.errors)


# ── G.6 live-recomputed structural-gap assignment ────────────────────────

def test_g6_live_recompute_forces_relationship_measurement_required_for_unmeasured_ticker():
    """SPGI is a live-confirmed structurally-unmeasured canonical ticker
    (no caps.clusters/issuer_lookthrough/relationship-record coverage)."""
    entry = _ticker_entry(
        "SPGI",
        policy_areas=_policy_areas(overlap_and_concentration=_area_entry(primary_status="retain_current_baseline")),
    )
    data = _artifact(entries=[entry])
    result = rv.validate_recommendation_data(data, repo_root=REPO_ROOT)
    assert any(
        "must be 'relationship_measurement_required'" in e and "SPGI" in e for e in result.errors
    ), result.errors


def test_g6_live_recompute_rejects_stale_forcing_on_measured_ticker():
    """NVDA is live-confirmed structurally measured (semis cluster-cap
    member) -- forcing relationship_measurement_required for it would be
    stale drift, not a legitimate finding."""
    entry = _ticker_entry(
        "NVDA",
        policy_areas=_policy_areas(
            overlap_and_concentration=_area_entry(primary_status="relationship_measurement_required")
        ),
    )
    data = _artifact(entries=[entry])
    result = rv.validate_recommendation_data(data, repo_root=REPO_ROOT)
    assert any("is live-recomputed as structurally measured" in e for e in result.errors), result.errors


def test_g6_live_recompute_accepts_correct_assignment_both_directions():
    unmeasured_entry = _ticker_entry(
        "SPGI",
        policy_areas=_policy_areas(
            overlap_and_concentration=_area_entry(primary_status="relationship_measurement_required")
        ),
    )
    measured_entry = _ticker_entry(
        "NVDA", policy_areas=_policy_areas(overlap_and_concentration=_area_entry(primary_status="retain_current_baseline"))
    )
    data = _artifact(entries=[unmeasured_entry, measured_entry])
    result = rv.validate_recommendation_data(data, repo_root=REPO_ROOT)
    assert not any("overlap_and_concentration" in e for e in result.errors), result.errors


def test_g6_live_recompute_skipped_without_repo_root():
    entry = _ticker_entry(
        "SPGI",
        policy_areas=_policy_areas(overlap_and_concentration=_area_entry(primary_status="retain_current_baseline")),
    )
    data = _artifact(entries=[entry])
    result = rv.validate_recommendation_data(data)  # no repo_root passed
    assert not any("live-recomputed" in e for e in result.errors)


# ── aggregate reconciliation ──────────────────────────────────────────────

def test_aggregate_reconciles_for_valid_fixture():
    data = _artifact()
    result = rv.validate_recommendation_data(data)
    assert not any("does not reconcile" in e for e in result.errors), result.errors


def test_aggregate_mismatch_detected():
    data = _artifact()
    # Corrupt one recorded count so it no longer matches the raw entries.
    data["aggregate"]["per_area_primary_status_counts"]["role"]["retain_current_baseline"] = ["ZZZA"]
    result = rv.validate_recommendation_data(data)
    assert any("does not reconcile" in e for e in result.errors)


def test_aggregate_secondary_mismatch_detected():
    data = _artifact()
    data["aggregate"]["per_area_secondary_condition_counts"]["role"]["unresolved_evidence"] = ["ZZZA", "ZZZB"]
    result = rv.validate_recommendation_data(data)
    assert any("does not reconcile" in e for e in result.errors)


def test_aggregate_missing_disclaimer_fails():
    data = _artifact()
    del data["aggregate"]["cross_tabulation_disclaimer"]
    result = rv.validate_recommendation_data(data)
    assert any("cross_tabulation_disclaimer" in e for e in result.errors)


# ── determinism ────────────────────────────────────────────────────────

def test_validation_is_deterministic_across_repeated_calls():
    data = _artifact()
    result1 = rv.validate_recommendation_data(data, repo_root=REPO_ROOT)
    result2 = rv.validate_recommendation_data(data, repo_root=REPO_ROOT)
    assert result1.valid == result2.valid
    assert result1.errors == result2.errors


def test_real_artifact_validation_is_deterministic_across_repeated_reads():
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from relationship_validator import load_canonical_universe

    canonical = load_canonical_universe(REPO_ROOT)
    result1 = rv.validate_recommendation_file(
        ARTIFACT_PATH, canonical_universe=canonical, sealed_universe=canonical, repo_root=REPO_ROOT
    )
    result2 = rv.validate_recommendation_file(
        ARTIFACT_PATH, canonical_universe=canonical, sealed_universe=canonical, repo_root=REPO_ROOT
    )
    assert result1.valid == result2.valid == True
    assert result1.errors == result2.errors == []


# ── file-read error branches ──────────────────────────────────────────────

def test_validate_recommendation_file_missing_file_reports_os_error(tmp_path):
    missing = tmp_path / "does_not_exist.yaml"
    result = rv.validate_recommendation_file(missing)
    assert not result.valid
    assert len(result.errors) == 1
    assert "could not read" in result.errors[0]
    assert str(missing) in result.errors[0]
    assert result.source == str(missing)


def test_validate_recommendation_file_unreadable_directory_reports_os_error(tmp_path):
    """A path that exists but cannot be read as a file (a directory) also
    exercises the OSError branch of _read_yaml, not just a missing path."""
    a_directory = tmp_path / "a_directory"
    a_directory.mkdir()
    result = rv.validate_recommendation_file(a_directory)
    assert not result.valid
    assert len(result.errors) == 1
    assert "could not read" in result.errors[0]


def test_validate_recommendation_file_malformed_yaml_reports_parse_error(tmp_path):
    bad_yaml = tmp_path / "malformed.yaml"
    bad_yaml.write_text("top: [unclosed\n  - this: is not valid yaml\n")
    result = rv.validate_recommendation_file(bad_yaml)
    assert not result.valid
    assert len(result.errors) == 1
    assert "YAML parse error" in result.errors[0]
    assert str(bad_yaml) in result.errors[0]
    assert result.source == str(bad_yaml)


def test_validate_recommendation_file_empty_file_is_none_not_a_mapping(tmp_path):
    """An empty (but readable, syntactically valid) YAML file parses to
    None -- exercised separately from the OSError/YAMLError branches."""
    empty = tmp_path / "empty.yaml"
    empty.write_text("")
    result = rv.validate_recommendation_file(empty)
    assert not result.valid
    assert any("must be a mapping" in e for e in result.errors)


# ── real repository artifact ──────────────────────────────────────────────

def test_real_artifact_file_parses_and_validates():
    assert ARTIFACT_PATH.is_file()
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from relationship_validator import load_canonical_universe

    canonical = load_canonical_universe(REPO_ROOT)
    result = rv.validate_recommendation_file(
        ARTIFACT_PATH, canonical_universe=canonical, sealed_universe=canonical, repo_root=REPO_ROOT
    )
    assert result.valid, result.errors


def test_real_artifact_covers_exactly_the_27_sealed_tickers():
    classification_dir = REPO_ROOT / "intelligence" / "classification"
    sealed_tickers = {p.stem for p in classification_dir.glob("*.yaml") if p.stem != "COHORT_MANIFEST"}
    assert len(sealed_tickers) == 27

    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    recommended_tickers = {entry["ticker"] for entry in data["recommendations"]}
    assert recommended_tickers == sealed_tickers


def test_real_artifact_g4_g5_forced_on_all_27():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    for entry in data["recommendations"]:
        assert entry["policy_areas"]["target_and_range"]["primary_status"] == "valuation_required", entry["ticker"]
        assert entry["policy_areas"]["maximum_position_size"]["primary_status"] == "valuation_required", entry["ticker"]


def test_real_artifact_g6_matches_live_structural_gap_set():
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from relationship_validator import load_canonical_universe

    canonical = load_canonical_universe(REPO_ROOT)
    live_unmeasured = rv._recompute_unmeasured_tickers(REPO_ROOT, canonical)
    # Reproduces REL-0007's own independently-computed 11-name finding.
    expected = frozenset(
        {"SNPS", "PANW", "ISRG", "TMO", "ICE", "SPGI", "V", "COST", "WM", "RTX", "RKLB"}
    )
    assert live_unmeasured == expected

    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    for entry in data["recommendations"]:
        status = entry["policy_areas"]["overlap_and_concentration"]["primary_status"]
        if entry["ticker"] in live_unmeasured:
            assert status == "relationship_measurement_required", entry["ticker"]
        else:
            assert status != "relationship_measurement_required", entry["ticker"]


def test_real_artifact_aggregate_counts_are_internally_consistent():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    entries = data["recommendations"]
    recomputed = rv._recompute_aggregate(entries)
    for area in rv._AREA_KEYS:
        for pv, tickers in recomputed["per_area_primary_status_counts"][area].items():
            recorded = data["aggregate"]["per_area_primary_status_counts"][area][pv]
            assert sorted(recorded) == sorted(tickers), (area, pv)
        for sv, tickers in recomputed["per_area_secondary_condition_counts"][area].items():
            recorded = data["aggregate"]["per_area_secondary_condition_counts"][area][sv]
            assert sorted(recorded) == sorted(tickers), (area, sv)


def test_real_artifact_no_more_than_two_secondary_conditions_anywhere():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    for entry in data["recommendations"]:
        for area, area_entry in entry["policy_areas"].items():
            assert len(area_entry["secondary_conditions"]) <= 2, (entry["ticker"], area)


def test_real_artifact_never_carries_structural_measurement_gap_as_overlap_secondary():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    for entry in data["recommendations"]:
        overlap = entry["policy_areas"]["overlap_and_concentration"]
        assert "structural_measurement_gap" not in overlap["secondary_conditions"], entry["ticker"]


def test_real_artifact_deep_copy_round_trip_is_stable():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    cloned = copy.deepcopy(data)
    cloned["recommendations"][0]["policy_areas"]["role"]["primary_status"] = "no_policy_conclusion"
    assert data["recommendations"][0]["policy_areas"]["role"]["primary_status"] != "no_policy_conclusion"


def test_real_artifact_chart_evidence_used_is_false():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    assert data["chart_evidence_used"] is False


def test_real_artifact_zero_coupling_with_allocate_or_margin_state():
    text = (REPO_ROOT / "recommendation_validator.py").read_text()
    assert "import allocate" not in text
    assert "import margin_state" not in text
    assert "from allocate" not in text
    assert "from margin_state" not in text


def test_recommendation_validator_module_never_opens_files_for_writing():
    """Static import-shape check -- this validator must never itself be the
    thing that writes to a sealed Milestone 6/7 record or its own artifact."""
    text = Path(__file__).with_name("recommendation_validator.py").read_text()
    assert '"w"' not in text
    assert "'w'" not in text
    assert '"a"' not in text
    assert "'a'" not in text


def test_real_artifact_no_edit_to_sealed_classification_or_reconciliation_content():
    """Protected-scope regression: the Milestone 6/7 files this artifact
    depends on remain byte-identical in shape -- 27 classification records,
    one reconciliation artifact, both still independently valid."""
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    import classification_validator as clv
    import reconciliation_validator as recv
    from relationship_validator import load_canonical_universe

    canonical = load_canonical_universe(REPO_ROOT)
    cls_result = clv.validate_classification_directory(REPO_ROOT / "intelligence" / "classification")
    assert cls_result.valid, cls_result.errors

    recon_result = recv.validate_reconciliation_file(
        REPO_ROOT / "intelligence" / "reconciliation" / "MILESTONE7_BASELINE_RECONCILIATION.yaml",
        canonical_universe=canonical,
        sealed_universe=canonical,
    )
    assert recon_result.valid, recon_result.errors


def test_real_artifact_matches_recorded_source_main_sha_field_shape():
    data = yaml.safe_load(ARTIFACT_PATH.read_text())
    assert re.fullmatch(r"[0-9a-f]{40}", data["source_main_sha"])
    assert re.fullmatch(r"[0-9a-f]{40}", data["milestone_references"]["milestone7_source_main_sha"])
