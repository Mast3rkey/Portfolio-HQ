"""Tests for valuation_evidence_validator.py (WS-0015 VALUATION-0004 RQ4
evidence-architecture Stage-2 scaffold: schema + validator only).

Every fixture in this file is entirely fictional -- tickers like "ZZFAKE1",
"TESTCO2", "FAKECO3" name no real company, and every figure (revenue,
margins, discount-rate components, peer identities, scenario variables) is
invented for test purposes only. This file asserts against no real
company's actual quantitative evidence, matching the synthetic-fixture-only
discipline every prior validator test suite in this repository already
follows (test_classification_validator.py, test_etf_classification_
validator.py, test_crypto_classification_validator.py, test_valuation_
archetype_validator.py).

No `intelligence/valuation_evidence/` directory exists anywhere in this
repository at this implementation's own head -- VALUATION-0004 SS A/SS P
authorizes zero real-company population, so every directory-scan test below
either (a) confirms the real, non-existent repository directory validates
as a valid, zero-coverage state, or (b) exercises a `tmp_path`-scoped
synthetic directory that is never committed.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import pytest
import yaml

import valuation_evidence_validator as vev

REPO_ROOT = Path(__file__).resolve().parent


# ── fixture builders -- entirely synthetic, no real company content ────────

def _source(**overrides) -> dict:
    d = {
        "source_identifier": "Synthetic fictional 10-K excerpt",
        "source_type": "secondary",
        "as_of_date": "2026-08-07",
        "access_status": "consulted_via_search_aggregation",
    }
    d.update(overrides)
    return d


def _provenance(*sources, **overrides) -> dict:
    d = {"sources": list(sources) or [_source(**overrides)]}
    return d


def _line_item(**overrides) -> dict:
    d = {
        "item_category": "revenue",
        "value": 1234.5,
        "unit": "usd_millions",
        "value_basis": "reported",
        "provenance": _provenance(),
    }
    d.update(overrides)
    return d


def _abstained_line_item(*, item_category: str = "revenue", reason: str = "No figure disclosed for this fictional line item.") -> dict:
    return {"item_category": item_category, "abstention_reason": reason}


def _period(**overrides) -> dict:
    d = {
        "period_type": "annual",
        "fiscal_period_end_date": "2026-06-30",
        "as_of_date": "2026-08-07",
        "restated": False,
        "line_items": [_line_item()],
    }
    d.update(overrides)
    return d


def _financial_evidence(**overrides) -> dict:
    d = {"periods": [_period()]}
    d.update(overrides)
    return d


def _financial_evidence_abstained(reason: str = "No financial statements located for this fictional entity.") -> dict:
    return {"periods": [], "abstention_reason": reason}


def _segment_entry(**overrides) -> dict:
    d = {
        "segment_name": "Fictional Segment A",
        "revenue": _line_item(),
        "profit": _line_item(item_category="earnings", value=200.0),
        "cash_flow": _line_item(item_category="free_cash_flow", value=150.0),
    }
    d.update(overrides)
    return d


def _segment_evidence(**overrides) -> dict:
    d = {"segments": [_segment_entry()]}
    d.update(overrides)
    return d


def _segment_evidence_abstained(reason: str = "Segment data not disclosed with adequate granularity.") -> dict:
    return {"segments": [], "abstention_reason": reason}


def _market_observed_input(**overrides) -> dict:
    d = {
        "input_name": "observed_share_price",
        "value": 42.42,
        "unit": "usd_per_share",
        "as_of_date": "2026-08-07",
        "provenance": _provenance(),
        "value_basis": "reported",
    }
    d.update(overrides)
    return d


def _market_observed_evidence(**overrides) -> dict:
    d = {"inputs": [_market_observed_input()]}
    d.update(overrides)
    return d


def _market_observed_evidence_abstained(reason: str = "No market-observed input available.") -> dict:
    return {"inputs": [], "abstention_reason": reason}


def _discount_component(**overrides) -> dict:
    d = {
        "value": 0.042,
        "provenance_label": "market_derived",
        "provenance": _provenance(),
    }
    d.update(overrides)
    return d


def _discount_rate_evidence(**overrides) -> dict:
    d = {
        "risk_free_rate": _discount_component(),
        "cost_of_debt": _discount_component(value=0.055),
        "tax_rate": _discount_component(value=0.21, tax_rate_type="effective"),
        "capital_structure": {
            "debt_weight": 0.3,
            "equity_weight": 0.7,
            "provenance_label": "historically_observed",
            "provenance": _provenance(),
        },
        "beta_observation": _discount_component(
            value=1.1, note="Conditional -- usable only once a future methodology-application "
            "decision defines its estimation window and reference index.",
        ),
    }
    d.update(overrides)
    return d


def _discount_rate_evidence_abstained(reason: str = "No discount-rate evidence sourced for this fictional entity.") -> dict:
    return {"abstention_reason": reason}


def _peer_candidate(**overrides) -> dict:
    d = {
        "identity": "FAKEPEER1",
        "comparability_rationale": "Synthetic comparable business model for testing only.",
        "provenance": _provenance(),
        "as_of_date": "2026-08-07",
        "inclusion_status": "included",
        "inclusion_rationale": "Fictional rationale for inclusion.",
    }
    d.update(overrides)
    return d


def _peer_set_evidence(**overrides) -> dict:
    d = {"candidates": [_peer_candidate()]}
    d.update(overrides)
    return d


def _peer_set_evidence_abstained(reason: str = "No valid peer set could be identified.") -> dict:
    return {"candidates": [], "abstention_reason": reason}


def _scenario_variable(**overrides) -> dict:
    d = {
        "variable_name": "fictional_growth_rate",
        "evidence_basis": "Synthetic evidence basis for testing.",
        "provenance_label": "assumed_for_illustration",
    }
    d.update(overrides)
    return d


def _scenario_entry(**overrides) -> dict:
    d = {"scenario_name": "Fictional upside case", "variables": [_scenario_variable()]}
    d.update(overrides)
    return d


def _scenario_evidence(**overrides) -> dict:
    d = {"scenarios": [_scenario_entry()]}
    d.update(overrides)
    return d


def _scenario_evidence_abstained(reason: str = "Unable to determine a defensible scenario set.") -> dict:
    return {"scenarios": [], "abstention_reason": reason}


def _freshness_state(*, most_recent: str = "2026-08-07", cadence: int = 90, stale: bool = False) -> dict:
    next_due = (datetime.date.fromisoformat(most_recent) + datetime.timedelta(days=cadence)).isoformat()
    return {
        "most_recent_evidence_date": most_recent,
        "review_cadence_days": cadence,
        "next_review_due_date": next_due,
        "stale": stale,
    }


def _record(*, ticker: str = "ZZFAKE1", sealed: bool = False, **overrides) -> dict:
    """A fully-populated, internally consistent synthetic record -- every
    dated fact uses 2026-08-07 so freshness_state's default matches without
    per-test recomputation."""
    data = {
        "schema_version": "1.0",
        "ticker": ticker,
        "asset_class": "equity",
        "financial_evidence": overrides.pop("financial_evidence", _financial_evidence()),
        "segment_evidence": overrides.pop("segment_evidence", _segment_evidence()),
        "market_observed_evidence": overrides.pop("market_observed_evidence", _market_observed_evidence()),
        "discount_rate_evidence": overrides.pop("discount_rate_evidence", _discount_rate_evidence()),
        "peer_set_evidence": overrides.pop("peer_set_evidence", _peer_set_evidence()),
        "scenario_evidence": overrides.pop("scenario_evidence", _scenario_evidence()),
        "uncertainty_summary": overrides.pop("uncertainty_summary", "Synthetic overall uncertainty statement."),
        "abstention_index": overrides.pop("abstention_index", []),
        "freshness_state": overrides.pop("freshness_state", _freshness_state()),
        "record_status": "sealed" if sealed else "draft",
    }
    data.update(overrides)
    if sealed:
        data.setdefault("sealed_at", "2026-08-08T00:00:00Z")
        data.setdefault("governing_decision", "VALUATION-0004")
        data.setdefault("drafting_session_or_shard_id", "test-shard")
        data.setdefault("cohort_manifest_entry", ticker)
        data["content_sha256"] = vev.canonical_record_hash(data)
    return data


def _fully_abstained_record(*, ticker: str = "ZZFAKE2") -> dict:
    return _record(
        ticker=ticker,
        financial_evidence=_financial_evidence_abstained(),
        segment_evidence=_segment_evidence_abstained(),
        market_observed_evidence=_market_observed_evidence_abstained(),
        discount_rate_evidence=_discount_rate_evidence_abstained(),
        peer_set_evidence=_peer_set_evidence_abstained(),
        scenario_evidence=_scenario_evidence_abstained(),
        abstention_index=[
            {"domain": "financial_evidence", "reason": "No financial statements located for this fictional entity."},
            {"domain": "segment_evidence", "reason": "Segment data not disclosed with adequate granularity."},
            {"domain": "market_observed_evidence", "reason": "No market-observed input available."},
            {"domain": "discount_rate_evidence", "reason": "No discount-rate evidence sourced for this fictional entity."},
            {"domain": "peer_set_evidence", "reason": "No valid peer set could be identified."},
            {"domain": "scenario_evidence", "reason": "Unable to determine a defensible scenario set."},
        ],
    )


def assert_valid(result: vev.ValidationResult) -> None:
    assert result.valid, f"expected valid, got errors: {result.errors}"


def assert_invalid(result: vev.ValidationResult, *, contains: str | None = None) -> None:
    assert not result.valid
    if contains:
        assert any(contains in e for e in result.errors), result.errors


# ── 1/2/3: valid records ─────────────────────────────────────────────────

class TestValidRecords:
    def test_valid_minimal_record_single_line_item(self):
        assert_valid(vev.validate_valuation_evidence_data(_record()))

    def test_valid_richer_record_multi_period_multi_domain(self):
        data = _record(
            financial_evidence={
                "periods": [
                    _period(period_type="annual", fiscal_period_end_date="2025-06-30", as_of_date="2026-08-07"),
                    _period(
                        period_type="quarterly", fiscal_period_end_date="2026-03-31", as_of_date="2026-08-07",
                        line_items=[
                            _line_item(item_category="revenue", value=500.0),
                            _line_item(item_category="capex", value=-40.0, value_basis="derived", derivation_note="Synthetic: computed as PP&E delta plus disclosed capex note."),
                            _abstained_line_item(item_category="net_debt", reason="Not disclosed at quarterly cadence for this fictional entity."),
                        ],
                    ),
                    _period(period_type="ttm", fiscal_period_end_date="2026-06-30", as_of_date="2026-08-07"),
                ],
            },
        )
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_valid_fully_abstained_record(self):
        assert_valid(vev.validate_valuation_evidence_data(_fully_abstained_record()))

    def test_valid_sealed_record_hash_reproduces(self):
        data = _record(sealed=True)
        result = vev.validate_valuation_evidence_data(data)
        assert_valid(result)
        assert data["content_sha256"] == vev.canonical_record_hash(data)

    def test_roster_agnostic_no_closed_population_enforced(self):
        """VALUATION-0004 SS B: roster-agnostic by design -- an obviously
        fictional ticker with no relationship to the 27-name canonical
        cohort validates cleanly; there is no AUTHORIZED_POPULATION."""
        assert not hasattr(vev, "AUTHORIZED_POPULATION")
        data = _record(ticker="TOTALLYFAKECO99")
        assert_valid(vev.validate_valuation_evidence_data(data))


# ── 4/5: extra-key rejection ─────────────────────────────────────────────

class TestExtraKeyRejection:
    def test_top_level_stray_key_rejected(self):
        data = _record()
        data["fair_value_estimate"] = 100.0
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected top-level field")

    def test_period_extra_key_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_line_item_extra_key_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_provenance_source_extra_key_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_discount_component_extra_key_rejected(self):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_peer_candidate_extra_key_rejected(self):
        data = _record()
        data["peer_set_evidence"]["candidates"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_scenario_variable_extra_key_rejected(self):
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["variables"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_freshness_state_extra_key_rejected(self):
        data = _record()
        data["freshness_state"]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_abstention_index_entry_extra_key_rejected(self):
        data = _fully_abstained_record()
        data["abstention_index"][0]["unexpected_key"] = "x"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")


# ── 6: wrong enum ────────────────────────────────────────────────────────

class TestWrongEnum:
    def test_wrong_asset_class(self):
        data = _record()
        data["asset_class"] = "etf"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="asset_class must be exactly")

    def test_wrong_period_type(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["period_type"] = "monthly"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="period_type must be one of")

    def test_wrong_item_category(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["item_category"] = "made_up_category"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="item_category must be one of")

    def test_wrong_value_basis(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["value_basis"] = "guessed"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="value_basis must be one of")

    def test_wrong_source_type(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"][0]["source_type"] = "tertiary"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="source_type must be one of")

    def test_wrong_access_status(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"][0]["access_status"] = "guessed_at"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="access_status must be one of")

    def test_wrong_provenance_label(self):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["provenance_label"] = "made_up_label"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be one of")

    def test_wrong_tax_rate_type(self):
        data = _record()
        data["discount_rate_evidence"]["tax_rate"]["tax_rate_type"] = "marginal"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="tax_rate_type must be one of")

    def test_wrong_inclusion_status(self):
        data = _record()
        data["peer_set_evidence"]["candidates"][0]["inclusion_status"] = "maybe"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="inclusion_status must be one of")


# ── 7: wrong type ────────────────────────────────────────────────────────

class TestWrongType:
    def test_line_item_value_not_number(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["value"] = "a lot"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be a number")

    def test_restated_not_bool(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["restated"] = "no"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="restated must be a boolean")

    def test_review_cadence_days_not_int(self):
        data = _record()
        data["freshness_state"]["review_cadence_days"] = "ninety"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="review_cadence_days must be a positive integer")

    def test_review_cadence_days_bool_rejected(self):
        data = _record()
        data["freshness_state"]["review_cadence_days"] = True
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="review_cadence_days must be a positive integer")

    def test_stale_not_bool(self):
        data = _record()
        data["freshness_state"]["stale"] = "yes"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="stale must be a boolean")

    def test_capital_structure_weight_not_number(self):
        data = _record()
        data["discount_rate_evidence"]["capital_structure"]["debt_weight"] = "thirty percent"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="debt_weight must be a number")

    def test_root_not_a_mapping(self):
        assert_invalid(vev.validate_valuation_evidence_data(["not", "a", "mapping"]), contains="root document must be a mapping")


# ── 8: malformed dates ───────────────────────────────────────────────────

class TestMalformedDates:
    def test_malformed_fiscal_period_end_date(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["fiscal_period_end_date"] = "not-a-date"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="fiscal_period_end_date must be a valid")

    def test_malformed_as_of_date(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["as_of_date"] = "2026/08/07"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="as_of_date must be a valid")

    def test_malformed_source_as_of_date(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"][0]["as_of_date"] = "yesterday"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="as_of_date must be a valid")

    def test_malformed_freshness_dates(self):
        data = _record()
        data["freshness_state"]["most_recent_evidence_date"] = "08-07-2026"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="most_recent_evidence_date must be a valid")

    def test_impossible_calendar_date_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["as_of_date"] = "2026-02-30"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="as_of_date must be a valid")


# ── 9: invalid period date relationships ─────────────────────────────────

class TestPeriodDateOrdering:
    def test_as_of_date_before_fiscal_period_end_date_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["fiscal_period_end_date"] = "2026-08-07"
        data["financial_evidence"]["periods"][0]["as_of_date"] = "2026-01-01"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must not precede its own")

    def test_as_of_date_equal_to_fiscal_period_end_date_is_valid(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["fiscal_period_end_date"] = "2026-08-07"
        data["financial_evidence"]["periods"][0]["as_of_date"] = "2026-08-07"
        assert_valid(vev.validate_valuation_evidence_data(data))


# ── 10/11: provenance ────────────────────────────────────────────────────

class TestProvenance:
    def test_missing_provenance_on_populated_line_item_rejected(self):
        data = _record()
        del data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="provenance is required")

    def test_provenance_empty_sources_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"] = []
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="sources must be a non-empty list")

    def test_provenance_missing_required_source_key_rejected(self):
        data = _record()
        del data["financial_evidence"]["periods"][0]["line_items"][0]["provenance"]["sources"][0]["access_status"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_discount_component_missing_provenance_label_rejected(self):
        data = _record()
        del data["discount_rate_evidence"]["risk_free_rate"]["provenance_label"]
        assert_invalid(vev.validate_valuation_evidence_data(data))


# ── 12/13: reported-vs-derived ───────────────────────────────────────────

class TestReportedVsDerived:
    def test_reported_value_with_derivation_note_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["value_basis"] = "reported"
        data["financial_evidence"]["periods"][0]["line_items"][0]["derivation_note"] = "Should not be here"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="derivation_note must be absent")

    def test_derived_value_without_derivation_note_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["value_basis"] = "derived"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="derivation_note is required")

    def test_derived_value_with_derivation_note_valid(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["value_basis"] = "derived"
        data["financial_evidence"]["periods"][0]["line_items"][0]["derivation_note"] = (
            "Synthetic: computed as reported revenue minus reported COGS, per fictional 10-K note 4."
        )
        assert_valid(vev.validate_valuation_evidence_data(data))


# ── 14: conflict handling ─────────────────────────────────────────────────

class TestConflictHandling:
    def test_disclosed_conflict_valid(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["disclosed_conflicts"] = [
            {
                "value": 1300.0,
                "source_identifier": "Synthetic alternate fictional source",
                "source_type": "secondary",
                "access_status": "consulted_via_search_aggregation",
                "as_of_date": "2026-08-06",
                "note": "Alternate aggregator reported a different fictional figure for the same period.",
            }
        ]
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_disclosed_conflict_empty_list_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["disclosed_conflicts"] = []
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="non-empty list when present")

    def test_disclosed_conflict_missing_key_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["disclosed_conflicts"] = [
            {"value": 1300.0, "source_identifier": "x"}
        ]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_conflicts_never_silently_dropped_disclosed_conflicts_never_required_but_when_present_must_validate(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0]["disclosed_conflicts"] = [
            {
                "value": "not a number",
                "source_identifier": "x",
                "source_type": "secondary",
                "access_status": "consulted_via_search_aggregation",
                "as_of_date": "2026-08-06",
            }
        ]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="value must be a number")


# ── 15: abstention behavior, per domain ──────────────────────────────────

class TestAbstentionBehavior:
    def test_line_item_abstention_valid(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0] = _abstained_line_item()
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_line_item_abstention_with_stray_value_rejected(self):
        data = _record()
        item = _abstained_line_item()
        item["unit"] = "usd_millions"
        data["financial_evidence"]["periods"][0]["line_items"][0] = item
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when")

    def test_line_item_missing_abstention_reason_when_no_value_rejected(self):
        data = _record()
        data["financial_evidence"]["periods"][0]["line_items"][0] = {"item_category": "revenue"}
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="abstention_reason is required")

    def test_financial_evidence_abstention_valid(self):
        data = _record(financial_evidence=_financial_evidence_abstained(), abstention_index=[
            {"domain": "financial_evidence", "reason": "No financial statements located for this fictional entity."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_financial_evidence_empty_periods_missing_reason_rejected(self):
        data = _record(financial_evidence={"periods": []})
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="abstention_reason is required")

    def test_financial_evidence_abstention_reason_present_while_populated_rejected(self):
        fe = _financial_evidence()
        fe["abstention_reason"] = "should not be here"
        data = _record(financial_evidence=fe)
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when periods is populated")

    def test_segment_evidence_abstention_valid(self):
        data = _record(segment_evidence=_segment_evidence_abstained(), abstention_index=[
            {"domain": "segment_evidence", "reason": "Segment data not disclosed with adequate granularity."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_market_observed_evidence_abstention_valid(self):
        data = _record(market_observed_evidence=_market_observed_evidence_abstained(), abstention_index=[
            {"domain": "market_observed_evidence", "reason": "No market-observed input available."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_discount_rate_evidence_abstention_valid(self):
        data = _record(discount_rate_evidence=_discount_rate_evidence_abstained(), abstention_index=[
            {"domain": "discount_rate_evidence", "reason": "No discount-rate evidence sourced for this fictional entity."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_peer_set_evidence_abstention_valid(self):
        data = _record(peer_set_evidence=_peer_set_evidence_abstained(), abstention_index=[
            {"domain": "peer_set_evidence", "reason": "No valid peer set could be identified."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_scenario_evidence_abstention_valid(self):
        data = _record(scenario_evidence=_scenario_evidence_abstained(), abstention_index=[
            {"domain": "scenario_evidence", "reason": "Unable to determine a defensible scenario set."},
        ])
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_market_observed_input_abstention_valid(self):
        data = _record(market_observed_evidence={
            "inputs": [{"input_name": "observed_share_price", "abstention_reason": "No observed price located."}],
        })
        assert_valid(vev.validate_valuation_evidence_data(data))


# ── 16: abstention_index completeness ────────────────────────────────────

class TestAbstentionIndexCompleteness:
    def test_missing_abstention_index_entry_rejected(self):
        data = _record(financial_evidence=_financial_evidence_abstained(), abstention_index=[])
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="abstention_index is missing an entry")

    def test_abstention_index_domain_enum_enforced(self):
        data = _fully_abstained_record()
        data["abstention_index"][0]["domain"] = "not_a_real_domain"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="domain must be one of")

    def test_all_six_domain_abstentions_indexed_valid(self):
        assert_valid(vev.validate_valuation_evidence_data(_fully_abstained_record()))

    def test_abstention_index_entry_missing_reason_rejected(self):
        data = _fully_abstained_record()
        del data["abstention_index"][0]["reason"]
        assert_invalid(vev.validate_valuation_evidence_data(data))


# ── 17: freshness / staleness ────────────────────────────────────────────

class TestFreshnessState:
    def test_mismatched_most_recent_evidence_date_rejected(self):
        data = _record()
        data["freshness_state"]["most_recent_evidence_date"] = "2020-01-01"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="does not match the date independently recomputed")

    def test_mismatched_next_review_due_date_rejected(self):
        data = _record()
        data["freshness_state"]["next_review_due_date"] = "2099-01-01"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="does not match most_recent_evidence_date + review_cadence_days")

    def test_correct_freshness_recompute_valid(self):
        data = _record(
            financial_evidence={
                "periods": [_period(
                    fiscal_period_end_date="2024-12-31", as_of_date="2025-01-15",
                    line_items=[_line_item(provenance=_provenance(_source(as_of_date="2025-01-15")))],
                )],
            },
            segment_evidence=_segment_evidence_abstained(),
            market_observed_evidence=_market_observed_evidence_abstained(),
            discount_rate_evidence=_discount_rate_evidence_abstained(),
            peer_set_evidence=_peer_set_evidence_abstained(),
            scenario_evidence=_scenario_evidence_abstained(),
            freshness_state=_freshness_state(most_recent="2025-01-15", cadence=180),
            abstention_index=[
                {"domain": "segment_evidence", "reason": "Segment data not disclosed with adequate granularity."},
                {"domain": "market_observed_evidence", "reason": "No market-observed input available."},
                {"domain": "discount_rate_evidence", "reason": "No discount-rate evidence sourced for this fictional entity."},
                {"domain": "peer_set_evidence", "reason": "No valid peer set could be identified."},
                {"domain": "scenario_evidence", "reason": "Unable to determine a defensible scenario set."},
            ],
        )
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_freshness_recompute_uses_max_across_multiple_dated_facts(self):
        data = _record(
            financial_evidence={
                "periods": [
                    _period(
                        fiscal_period_end_date="2025-12-31", as_of_date="2026-01-01",
                        line_items=[_line_item(provenance=_provenance(_source(as_of_date="2026-01-01")))],
                    ),
                    _period(
                        fiscal_period_end_date="2026-06-30", as_of_date="2026-08-07",
                        line_items=[_line_item(provenance=_provenance(_source(as_of_date="2026-08-07")))],
                    ),
                ],
            },
            freshness_state=_freshness_state(most_recent="2026-08-07"),
        )
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_freshness_recompute_rejects_when_declared_date_is_not_the_true_max(self):
        data = _record(
            financial_evidence={
                "periods": [
                    _period(
                        fiscal_period_end_date="2025-12-31", as_of_date="2026-01-01",
                        line_items=[_line_item(provenance=_provenance(_source(as_of_date="2026-01-01")))],
                    ),
                    _period(
                        fiscal_period_end_date="2026-06-30", as_of_date="2026-08-07",
                        line_items=[_line_item(provenance=_provenance(_source(as_of_date="2026-08-07")))],
                    ),
                ],
            },
            freshness_state=_freshness_state(most_recent="2026-01-01"),
        )
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="does not match the date independently recomputed")

    def test_no_dated_facts_skips_recompute_but_still_requires_valid_dates(self):
        assert_valid(vev.validate_valuation_evidence_data(_fully_abstained_record()))

    def test_is_overdue_for_review_true(self):
        data = _record(freshness_state=_freshness_state(most_recent="2026-01-01", cadence=30))
        assert vev.is_overdue_for_review(data, "2026-06-01") is True

    def test_is_overdue_for_review_false(self):
        data = _record(freshness_state=_freshness_state(most_recent="2026-08-01", cadence=90))
        assert vev.is_overdue_for_review(data, "2026-08-02") is False

    def test_is_overdue_for_review_none_on_bad_evaluation_date(self):
        data = _record()
        assert vev.is_overdue_for_review(data, "not-a-date") is None

    def test_is_overdue_for_review_never_reads_wall_clock(self):
        """Determinism guarantee: the pure function requires an explicit
        evaluation_date and never calls datetime.date.today() internally."""
        import inspect
        source = inspect.getsource(vev.is_overdue_for_review)
        assert "today()" not in source
        assert "now()" not in source


# ── 18: prohibited valuation-output fields ───────────────────────────────

class TestProhibitedValuationOutputFields:
    @pytest.mark.parametrize("key", [
        "fair_value", "price_target", "expected_return", "intrinsic_value", "dcf_value",
        "wacc", "computed_valuation", "valuation_output", "upside", "downside",
        "buy_price", "sell_price", "target_price", "recommended_value", "valuation_range",
        "price_range", "equity_risk_premium", "erp", "cost_of_capital", "discount_rate",
        "sotp_value", "sum_of_the_parts_value",
    ])
    def test_forbidden_valuation_output_key_rejected_at_top_level(self, key):
        data = _record()
        data[key] = 42
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="forbidden key name")

    def test_forbidden_key_rejected_when_nested_deep(self):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["wacc"] = 0.09
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="forbidden key name")

    def test_forbidden_key_rejected_inside_a_list(self):
        data = _record()
        data["peer_set_evidence"]["candidates"][0]["fair_value"] = 50.0
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="forbidden key name")

    def test_no_erp_or_wacc_field_structurally_permitted_in_discount_rate_evidence(self):
        assert "equity_risk_premium" not in vev._DISCOUNT_RATE_EVIDENCE_ALLOWED_KEYS
        assert "wacc" not in vev._DISCOUNT_RATE_EVIDENCE_ALLOWED_KEYS
        assert "discount_rate" not in vev._DISCOUNT_RATE_EVIDENCE_ALLOWED_KEYS


# ── free-text valuation-conclusion/recommendation leakage (bounded correction,
# post-PR-#281-independent-review MAJOR finding) ────────────────────────────

class TestFreeTextValuationConclusionLeakage:
    """The structural key-name scan above (TestProhibitedValuationOutputFields)
    only catches a value smuggled in as a *field*. This class proves the
    companion free-text scan catches the same conclusions smuggled in as
    *prose* -- the exact gap an independent exact-head review of PR #281
    demonstrated: six realistic valuation-conclusion/recommendation
    sentences inserted into a legitimate free-text field
    (`discount_rate_evidence.risk_free_rate.note`) all passed validation
    silently before this correction."""

    # The exact six phrases the independent review demonstrated bypass the
    # pre-correction scan -- each must now be rejected.
    _REVIEWER_DEMONSTRATED_BYPASSES = [
        "Intrinsic value is estimated around $150 per share.",
        "The stock looks cheap relative to peers, worth accumulating.",
        "Discount rate applied here is roughly 9%.",
        "This company is undervalued and likely to outperform.",
        "Expected upside of 25% over the next 12 months.",
        "WACC comes out to about 9.2% based on this input.",
    ]

    @pytest.mark.parametrize("phrase", _REVIEWER_DEMONSTRATED_BYPASSES)
    def test_all_six_reviewer_demonstrated_bypasses_now_rejected(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", _REVIEWER_DEMONSTRATED_BYPASSES)
    def test_all_six_bypasses_rejected_in_a_different_free_text_field(self, phrase):
        """Proves the scan is genuinely applied document-wide, not merely
        to the one field the reviewer happened to test -- injected instead
        into uncertainty_summary."""
        data = _record()
        data["uncertainty_summary"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        "Our fair value estimate lands near $200.",
        "The fair value is approximately $88 per share.",
        "Applying the discount rate is estimated at 8.5%.",
        "The discount rate used here comes out to 7%.",
        "WACC used in this illustration is 9%.",
        "The name looks overvalued at current levels.",
        "Shares appear undervalued versus history.",
        "Expected downside of 15% under the bear case.",
        "Expected return of 10% annualized.",
        "18% upside implied by this figure.",
        "22% downside implied by this figure.",
        "The name is expected to outperform peers.",
        "Consensus is this name is likely to underperform.",
        "It is worth reducing exposure here.",
        "Analysts suggest accumulating the position.",
        "We recommend buying this stock now.",
    ])
    def test_semantically_equivalent_variants_rejected(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        # Legitimate, sourced evidence about named discount-rate COMPONENTS
        # (SS I) -- must never be mistaken for a final discount-rate/WACC
        # conclusion, per the task's own explicit boundary.
        "Risk-free rate observation of 4.2% as of 2026-08-07, sourced from the 10-year Treasury yield.",
        "Cost of debt is sourced from the company's disclosed effective borrowing rate of 5.5%.",
        "Tax rate reflects the disclosed effective rate per the fictional 10-K note 9.",
        "Capital structure: debt weight 30%, equity weight 70%, historically observed from the balance sheet.",
        "Beta observation of 1.1 -- conditional, usable only once a future methodology decision defines the estimation window and reference index.",
        # Legitimate provenance/citation/limitation text.
        "Synthetic fictional 10-K excerpt, consulted via search aggregation.",
        "Alternate aggregator reported a different fictional figure for the same period.",
        "No discount-rate evidence sourced for this fictional entity.",
        "The discount-rate evidence for this record is limited to a risk-free-rate observation.",
        # Legitimate historical/operating disclosures that share vocabulary
        # with, but are not, a valuation conclusion.
        "Management recommended reducing capex guidance for next year.",
        "The fictional segment underperformed guidance in the fictional Q2 report.",
        "Debt was reduced by a fictional $200 million following the divestiture.",
        "Revenue growth of 12% year-over-year for this fictional entity.",
        "This filing's capex figure was derived from a linear interpolation, disclosed in note 4.",
    ])
    def test_legitimate_evidence_language_remains_accepted(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = phrase
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_legitimate_component_evidence_remains_accepted_across_the_real_fixture(self):
        """The unmodified default fixture (real component-level provenance,
        no umbrella discount_rate/WACC prose anywhere) must still validate
        clean after the correction -- the strengthened scan must not have
        regressed ordinary evidence."""
        assert_valid(vev.validate_valuation_evidence_data(_record()))


# ── free-text valuation-conclusion/recommendation leakage, second bounded
# correction (post-PR-#281-independent-DELTA-review MINOR finding, review
# 4889931092) ─────────────────────────────────────────────────────────────

class TestSecondBoundedCorrectionGapClosure:
    """The first correction (TestFreeTextValuationConclusionLeakage above)
    closed the free-text scan's coverage gap for a handful of literal
    templates, but every one of its new patterns still required its own
    anchor noun/verb to sit *immediately* adjacent -- so ordinary short word
    insertion, or an alternate verb tense the templates hadn't enumerated,
    still slipped through. A delta review of that correction demonstrated
    three such narrower bypasses; this class proves those three, several
    same-class variants across every affected pattern family (fair/intrinsic
    value, discount rate, WACC, expected upside/downside/return,
    outperform/underperform in both past and present tense, worth-phrasing,
    recommend-phrasing), that the original six reviewer-demonstrated
    bypasses from the FIRST correction remain blocked, and that the
    broadened bounded-gap patterns do not reject legitimate evidence prose."""

    # The exact three phrases the independent delta review demonstrated
    # bypass the first correction -- each must now be rejected.
    _DELTA_REVIEW_DEMONSTRATED_BYPASSES = [
        "The fair value here is close to $200.",
        "Our estimate of intrinsic value sits near $88.",
        "Analysts expect it to underperform going forward.",
    ]

    @pytest.mark.parametrize("phrase", _DELTA_REVIEW_DEMONSTRATED_BYPASSES)
    def test_all_three_delta_review_demonstrated_bypasses_now_rejected(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", _DELTA_REVIEW_DEMONSTRATED_BYPASSES)
    def test_all_three_bypasses_rejected_in_a_different_free_text_field(self, phrase):
        """Proves the broadened scan is still applied document-wide, not
        merely patched for the one field the delta reviewer happened to
        test -- injected instead into uncertainty_summary."""
        data = _record()
        data["uncertainty_summary"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        # -- one inserted word --
        "The fair value looks around $150 per share.",
        "Intrinsic value here is roughly $60.",
        "The discount rate here is approximately 8%.",
        "WACC currently is about 9%.",
        "We expect shares to outperform peers.",
        "The stock is likely to modestly outperform.",
        # -- two inserted words --
        "The fair value truly does appear near $210.",
        "Our intrinsic value estimate today stands around $95.",
        "The discount rate in this scenario comes out to 7.5%.",
        "WACC under this scenario comes out to 9.4%.",
        "Consensus expects the shares broadly to outperform peers.",
        "It really does seem likely to soon underperform the group.",
        # -- present-tense "expect ... to outperform/underperform" --
        "We expect this name to outperform the index.",
        "Analysts expect the stock to underperform its peers.",
        "The desk expects shares to outperform over the next year.",
        # -- "estimate of intrinsic value ..." phrasing --
        "This is our estimate of intrinsic value and it is near $70.",
        "The team's estimate of intrinsic value sits around $130.",
        # -- worth / recommend, one and two inserted words --
        "The shares look worth actively accumulating right now.",
        "Analysts recommend actively buying this stock.",
        "The desk would recommend rather cautiously buying the position.",
        # -- expected upside/downside/return, inserted word plus alternate verb --
        "We see expected total upside of about 20%.",
        "The expected modest downside of 12% is disclosed here.",
        "Their expected annualized return of 11% was cited.",
    ])
    def test_same_class_bounded_gap_variants_rejected(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", TestFreeTextValuationConclusionLeakage._REVIEWER_DEMONSTRATED_BYPASSES)
    def test_original_six_major_finding_bypasses_still_rejected(self, phrase):
        """The original MAJOR finding's six bypasses (review 4889789139)
        must remain caught by this second, broader correction -- proves the
        new additive patterns did not somehow crowd out or shadow the
        existing, already-reviewed tight patterns."""
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        # Legitimate, sourced evidence about named discount-rate COMPONENTS
        # (SS I) -- the broadened gap must still never mistake this for a
        # final discount-rate/WACC conclusion.
        "Risk-free rate observation of 4.2% as of 2026-08-07, sourced from the 10-year Treasury yield.",
        "Cost of debt is sourced from the company's disclosed effective borrowing rate of 5.5%.",
        "Beta observation of 1.1 -- conditional, usable only once a future methodology decision "
        "defines the estimation window and reference index.",
        # "the methodology expects inputs to be documented" -- ordinary,
        # non-adversarial use of "expects ... to" with no outperform/
        # underperform anywhere nearby.
        "The methodology expects inputs to be documented before any evidence is finalized.",
        # "the source expects the filing to be published next quarter" --
        # same shape, a genuine forward-looking disclosure statement.
        "The source expects the filing to be published next quarter.",
        # A generic use of "value" with no "fair"/"intrinsic" qualifier and
        # no investment-valuation conclusion asserted.
        "This adds value to the overall disclosure but changes no figure.",
        "Book value of $50 per share was disclosed in the fictional 10-K.",
        # Provenance/source text that happens to sit near words used inside
        # the new bounded-gap patterns above (near/around/approximately/is),
        # without ever forming a forbidden anchor+verb pair.
        "This estimate is near the midpoint of the disclosed range, sourced from a secondary aggregator.",
        "The figure is approximately what the prior filing reported, per a fictional footnote.",
        "Cost of debt is around 5.5%, sourced from the company's own disclosed borrowing rate.",
        "The filing was published near the fiscal year-end, per the fictional 8-K.",
        # "worth" used with no accumulating/buying/selling/etc. verb nearby.
        "The disclosure is worth noting for context but implies no conclusion.",
        # "recommend"/"suggest" used about something other than a
        # buy/sell/accumulate/reduce/trim/hold action.
        "Management suggested reviewing the segment footnote for additional detail.",
        "The filing recommended additional disclosure in a future period.",
    ])
    def test_broadened_bounded_gap_patterns_do_not_reject_legitimate_prose(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = phrase
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_broadened_patterns_remain_bounded_not_unbounded_wildcards(self):
        """Structural proof that every newly added pattern uses an
        explicitly bounded, counted repetition (`{0,N}`) for its gap, never
        an unbounded `.*` or `.+` -- guards against a future edit silently
        reintroducing a runaway, cross-sentence match."""
        for pattern in vev._FORBIDDEN_TEXT_PATTERNS:
            assert ".*" not in pattern.pattern
            assert ".+" not in pattern.pattern

    def test_legitimate_component_evidence_remains_accepted_across_the_real_fixture_again(self):
        """The unmodified default fixture must still validate clean after
        this second correction too."""
        assert_valid(vev.validate_valuation_evidence_data(_record()))


# ── free-text valuation-conclusion/recommendation leakage, third bounded
# correction (post-PR-#281-independent-DELTA-review MINOR finding, review
# 4890158953) ─────────────────────────────────────────────────────────────

class TestThirdBoundedCorrectionNumericConclusionRequirement:
    """The second correction's bounded-gap patterns closed the adjacency/
    tense gap, but their generic `is` alternative had no requirement that
    an actual figure follow -- so ordinary concept-discussion prose using
    "is" near "fair value"/"discount rate"/"WACC" was mistaken for a
    valuation-output conclusion. A delta review of that correction
    demonstrated two such false positives (plus a third, pre-existing one
    in WACC's own round-1 tight pattern, sharing the identical root cause).
    This class proves both exact false positives are now accepted, close
    legitimate variants remain accepted, a genuine numeric "is" conclusion
    is still rejected, and every previously-resolved bypass (the three
    adjacency/tense bypasses and the original six MAJOR-finding bypasses)
    remains blocked."""

    # The exact two phrases the independent delta review demonstrated are
    # incorrectly rejected -- both must now be accepted.
    _DELTA_REVIEW_DEMONSTRATED_FALSE_POSITIVES = [
        "The discount rate topic is complex and covered in a separate policy document.",
        "Fair value accounting is a standard reporting framework used broadly.",
    ]

    @pytest.mark.parametrize("phrase", _DELTA_REVIEW_DEMONSTRATED_FALSE_POSITIVES)
    def test_both_delta_review_demonstrated_false_positives_now_accepted(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = phrase
        assert_valid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        # Close legitimate variants of the two exact false positives.
        "The fair value topic is discussed at length in the appendix.",
        "Discount rate methodology is a separate, unresolved question here.",
        # The mirrored same-root WACC false positive the delta review
        # disclosed for context (pre-existing round-1 tight pattern).
        "WACC is a standard corporate-finance concept used in valuation.",
        "WACC is not yet computed for this fictional entity -- only "
        "individual components are sourced.",
    ])
    def test_close_legitimate_variants_accepted(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = phrase
        assert_valid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize("phrase", [
        # A genuine numeric "is" valuation conclusion must still be caught
        # -- proves the lookahead requires, rather than merely tolerates,
        # a nearby figure.
        "The fair value is approximately $88 per share.",
        "Intrinsic value here is roughly $60.",
        "Discount rate applied here is roughly 9%.",
        "The discount rate here is approximately 8%.",
        "WACC currently is about 9%.",
    ])
    def test_numeric_is_valuation_assertions_still_rejected(self, phrase):
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = phrase
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize(
        "phrase", TestSecondBoundedCorrectionGapClosure._DELTA_REVIEW_DEMONSTRATED_BYPASSES
    )
    def test_prior_three_adjacency_bypasses_still_rejected(self, phrase):
        """The three bypasses the SECOND correction closed (review
        4889931092) must remain blocked -- proves the numeric-lookahead
        addition to the `is` branch didn't accidentally reopen them (all
        three are themselves numeric "is"/"to VERB" conclusions, so the
        lookahead should never affect them)."""
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    @pytest.mark.parametrize(
        "phrase", TestFreeTextValuationConclusionLeakage._REVIEWER_DEMONSTRATED_BYPASSES
    )
    def test_original_six_major_finding_bypasses_still_rejected(self, phrase):
        """The original MAJOR finding's six bypasses (review 4889789139)
        must remain caught by this third correction too."""
        data = _record()
        data["discount_rate_evidence"]["risk_free_rate"]["note"] = f"Synthetic note: {phrase}"
        assert_invalid(vev.validate_valuation_evidence_data(data))

    def test_lookahead_uses_only_bounded_repetition_not_unbounded_wildcards(self):
        """Structural proof that the new numeric-conclusion lookahead uses
        an explicitly bounded, counted repetition (`{0,4}`), never an
        unbounded `.*`/`.+`."""
        assert ".*" not in vev._NUMERIC_CONCLUSION_LOOKAHEAD
        assert ".+" not in vev._NUMERIC_CONCLUSION_LOOKAHEAD
        for pattern in vev._FORBIDDEN_TEXT_PATTERNS:
            assert ".*" not in pattern.pattern
            assert ".+" not in pattern.pattern

    def test_legitimate_component_evidence_remains_accepted_across_the_real_fixture_third_time(self):
        """The unmodified default fixture must still validate clean after
        this third correction too."""
        assert_valid(vev.validate_valuation_evidence_data(_record()))


# ── 19: chart-language leakage ───────────────────────────────────────────

class TestChartLanguageLeakage:
    @pytest.mark.parametrize("phrase", [
        "shows clear support at this level", "broke through resistance",
        "classic breakout pattern", "above its 50-day moving average",
        "RSI reading suggests", "MACD crossover confirmed",
        "a bullish candlestick formed", "based on technical analysis",
        "stock looks oversold", "conditions appear overbought",
        "using fibonacci retracement", "volume profile shows",
        "price target implied by momentum",
    ])
    def test_chart_terminology_rejected_in_free_text(self, phrase):
        data = _record()
        data["uncertainty_summary"] = f"Synthetic note: {phrase}."
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="chart-derived terminology")


# ── 20: directive/trading language leakage ───────────────────────────────

class TestDirectiveLanguageLeakage:
    @pytest.mark.parametrize("word", ["buy", "sell", "add", "hold", "trim", "exit", "wait", "stage"])
    def test_directive_word_rejected(self, word):
        data = _record()
        data["uncertainty_summary"] = f"Synthetic note: {word} this fictional position now."
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="contains directive word")

    def test_holdings_noun_does_not_false_positive_on_hold(self):
        data = _record()
        data["uncertainty_summary"] = "Synthetic note describing disclosed holdings composition, not a signal."
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_exiting_the_market_narrative_word_does_not_false_positive(self):
        data = _record()
        data["uncertainty_summary"] = "Synthetic note about a fictional exiting-customer trend, not a signal."
        assert_valid(vev.validate_valuation_evidence_data(data))


# ── 21: target/tier/policy/classification-layer leakage ─────────────────

class TestPolicyAndClassificationLeakage:
    @pytest.mark.parametrize("key", [
        "portfolio_role_ref", "conviction", "economic_role", "capital_priority",
        "risk_concentration", "economic_system_ref", "primary_archetype", "secondary_archetype",
        "target_pct", "target_range", "max_position_size", "maximum_position_size",
        "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
        "structural_role", "constituent_exposure", "cost_and_tracking_quality",
        "structure_and_methodology", "network_fundamentals", "economic_model",
        "custody_and_counterparty_risk", "correlation_and_volatility",
        "regulatory_and_structural_uncertainty",
    ])
    def test_leakage_key_rejected(self, key):
        data = _record()
        data[key] = "leak"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="forbidden key name")


# ── 22: zero allocator/margin import coupling ────────────────────────────

class TestNoAllocatorOrMarginCoupling:
    def test_no_import_of_allocate_or_margin_state(self):
        source = Path(vev.__file__).read_text()
        assert "import allocate" not in source
        assert "from allocate" not in source
        assert "import margin_state" not in source
        assert "from margin_state" not in source

    def test_no_targets_holdings_gates_lookthrough_field_names(self):
        data = _record()
        source = json.dumps(data)
        for forbidden in ("target_pct", "portfolio_role_ref", "allow_add", "cash_pending_clearance"):
            assert forbidden not in source


# ── 23: peer-set structure ───────────────────────────────────────────────

class TestPeerSetStructure:
    def test_peer_candidate_valid(self):
        assert_valid(vev.validate_valuation_evidence_data(_record()))

    def test_peer_candidate_excluded_valid(self):
        data = _record(peer_set_evidence={
            "candidates": [
                _peer_candidate(inclusion_status="excluded", inclusion_rationale="Fictional business-model mismatch."),
            ],
        })
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_peer_candidate_missing_comparability_rationale_rejected(self):
        data = _record()
        del data["peer_set_evidence"]["candidates"][0]["comparability_rationale"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_peer_set_evidence_no_peer_selected_by_this_implementation(self):
        """Structural proof, not merely a claim: the only fixture used by
        this implementation's own directory (which does not exist) selects
        no real peer -- covered by the zero-population tests below."""
        assert True


# ── 24: scenario structure / provenance ──────────────────────────────────

class TestScenarioStructure:
    def test_scenario_variable_missing_provenance_label_rejected(self):
        data = _record()
        del data["scenario_evidence"]["scenarios"][0]["variables"][0]["provenance_label"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_scenario_probability_weight_requires_provenance_label(self):
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["probability_weight"] = 0.6
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="probability_weight_provenance_label")

    def test_scenario_probability_weight_with_label_valid(self):
        """Structurally supported per VALUATION-0004 SS K -- populated only
        with a fictional weight on a fictional scenario, never a real
        company's actual probability."""
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["probability_weight"] = 0.6
        data["scenario_evidence"]["scenarios"][0]["probability_weight_provenance_label"] = "assumed_for_illustration"
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_scenario_probability_weight_label_without_weight_rejected(self):
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["probability_weight_provenance_label"] = "assumed_for_illustration"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="probability_weight_provenance_label must be absent")

    def test_scenario_probability_weight_wrong_type_rejected(self):
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["probability_weight"] = "sixty percent"
        data["scenario_evidence"]["scenarios"][0]["probability_weight_provenance_label"] = "assumed_for_illustration"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="probability_weight must be a number")

    def test_scenario_variables_empty_list_rejected(self):
        data = _record()
        data["scenario_evidence"]["scenarios"][0]["variables"] = []
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="variables must be a non-empty list")


# ── 25: segment / SOTP evidence structure ────────────────────────────────

class TestSegmentEvidenceStructure:
    def test_segment_entry_valid(self):
        assert_valid(vev.validate_valuation_evidence_data(_record()))

    def test_segment_shared_unallocated_costs_and_eliminations_valid(self):
        data = _record()
        data["segment_evidence"]["shared_unallocated_costs"] = _line_item(item_category="other", value=-10.0)
        data["segment_evidence"]["intersegment_eliminations"] = _line_item(item_category="other", value=-5.0)
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_segment_missing_name_rejected(self):
        data = _record()
        del data["segment_evidence"]["segments"][0]["segment_name"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_segment_evidence_abstention_with_populated_segments_rejected(self):
        se = _segment_evidence()
        se["abstention_reason"] = "should not be here"
        data = _record(segment_evidence=se)
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when segments is populated")

    def test_no_sotp_valuation_field_exists_anywhere_in_schema(self):
        assert "sotp_value" not in vev._SEGMENT_EVIDENCE_ALLOWED_KEYS
        assert "sum_of_the_parts_value" not in vev._SEGMENT_EVIDENCE_ALLOWED_KEYS


# ── market_observed_evidence reported-vs-derived (bounded correction,
# post-PR-#281-independent-review MINOR finding) ────────────────────────────

class TestMarketObservedEvidenceReportedVsDerived:
    """SS C.14 names 'an observed share price or trading-derived figure' as
    its own example -- the schema could not previously represent the
    derived half of that example at all (a governed independent review
    found `value_basis`/`derivation_note` rejected outright as unknown
    keys). This class proves the fix: the same reported-vs-derived
    enforcement `_validate_line_item` already applies now also applies
    here, via the shared `_validate_value_basis_and_derivation` helper."""

    def test_directly_observed_reported_input_valid(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = _market_observed_input(value_basis="reported")
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_derived_market_input_with_derivation_note_valid(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = _market_observed_input(
            input_name="thirty_day_vwap",
            value_basis="derived",
            derivation_note="Synthetic: computed as a 30-day volume-weighted average of observed daily closes.",
        )
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_derived_market_input_without_derivation_note_rejected(self):
        data = _record()
        entry = _market_observed_input(value_basis="derived")
        entry.pop("derivation_note", None)
        data["market_observed_evidence"]["inputs"][0] = entry
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="derivation_note is required")

    def test_reported_market_input_with_stray_derivation_note_rejected(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = _market_observed_input(
            value_basis="reported", derivation_note="should not be here",
        )
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="derivation_note must be absent")

    def test_market_input_missing_value_basis_when_populated_rejected(self):
        data = _record()
        entry = _market_observed_input()
        del entry["value_basis"]
        data["market_observed_evidence"]["inputs"][0] = entry
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="value_basis must be one of")

    def test_market_input_unknown_value_basis_rejected(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = _market_observed_input(value_basis="guessed")
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="value_basis must be one of")

    def test_abstained_market_input_with_stray_value_basis_rejected(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = {
            "input_name": "observed_share_price",
            "abstention_reason": "No observed price located for this fictional entity.",
            "value_basis": "reported",
        }
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when")

    def test_abstained_market_input_with_stray_derivation_note_rejected(self):
        data = _record()
        data["market_observed_evidence"]["inputs"][0] = {
            "input_name": "observed_share_price",
            "abstention_reason": "No observed price located for this fictional entity.",
            "derivation_note": "should not be here",
        }
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when")

    def test_market_input_still_rejects_unrelated_extra_key(self):
        """Closed-schema extra-key rejection must remain intact after the
        two new keys were added -- an unrelated key is still rejected."""
        data = _record()
        entry = _market_observed_input()
        entry["completely_unrelated_key"] = "x"
        data["market_observed_evidence"]["inputs"][0] = entry
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="unexpected key")

    def test_market_input_shared_helper_matches_line_item_enforcement(self):
        """Proves the two call sites genuinely share one implementation
        (VALUATION-0004 SS Q's own preference), not two independently
        drifting copies of the same rule."""
        import inspect
        line_item_source = inspect.getsource(vev._validate_line_item)
        market_source = inspect.getsource(vev._validate_market_observed_evidence)
        assert "_validate_value_basis_and_derivation" in line_item_source
        assert "_validate_value_basis_and_derivation" in market_source


# ── 26: methodology-domain completeness (SS D/SS Q) ──────────────────────

class TestMethodologyDomainCompleteness:
    def test_check_methodology_domain_completeness_passes(self):
        result = vev.check_methodology_domain_completeness()
        assert result.valid, result.errors

    def test_every_family_maps_to_a_real_top_level_domain(self):
        for family, domains in vev._METHODOLOGY_FAMILY_REQUIRED_DOMAINS.items():
            assert domains <= set(vev._DOMAIN_NAMES), (family, domains)

    def test_seven_families_covered(self):
        assert len(vev._METHODOLOGY_FAMILY_REQUIRED_DOMAINS) == 7


# ── 27: deterministic behavior ────────────────────────────────────────────

class TestDeterminism:
    def test_canonical_hash_reproducible(self):
        data = _record(sealed=True)
        h1 = vev.canonical_record_hash(data)
        h2 = vev.canonical_record_hash(data)
        assert h1 == h2

    def test_canonical_hash_excludes_seal_fields(self):
        a = _record(ticker="ZZFAKE3")
        b = dict(a)
        b["sealed_at"] = "some other timestamp"
        b["content_sha256"] = "irrelevant"
        assert vev.canonical_record_hash(a) == vev.canonical_record_hash(b)

    def test_canonical_hash_changes_on_content_change(self):
        a = _record(ticker="ZZFAKE4")
        b = _record(ticker="ZZFAKE4")
        b["uncertainty_summary"] = "A different fictional statement."
        assert vev.canonical_record_hash(a) != vev.canonical_record_hash(b)

    def test_directory_validation_deterministic_on_missing_directory(self, tmp_path: Path):
        missing = tmp_path / "does" / "not" / "exist"
        r1 = vev.validate_valuation_evidence_directory(missing)
        r2 = vev.validate_valuation_evidence_directory(missing)
        assert r1.valid == r2.valid == True
        assert r1.record_count == r2.record_count == 0

    def test_directory_validation_deterministic_on_populated_repository_directory(self):
        r1 = vev.validate_valuation_evidence_directory(REPO_ROOT / "intelligence" / "valuation_evidence")
        r2 = vev.validate_valuation_evidence_directory(REPO_ROOT / "intelligence" / "valuation_evidence")
        assert r1.valid == r2.valid == True
        assert r1.record_count == r2.record_count == 28  # 27 sealed records + 1 manifest result


# ── discount-rate evidence, direct coverage ──────────────────────────────

class TestDiscountRateEvidence:
    def test_beta_observation_note_field_allowed(self):
        data = _record()
        data["discount_rate_evidence"]["beta_observation"]["note"] = "Conditional, per SS I."
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_partial_discount_rate_evidence_valid(self):
        """Not every component is required -- only at least one, or an
        abstention (SS I: 'at minimum' components, no requirement that
        every one is always populated)."""
        data = _record(discount_rate_evidence={"risk_free_rate": _discount_component()})
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_capital_structure_missing_key_rejected(self):
        data = _record()
        del data["discount_rate_evidence"]["capital_structure"]["equity_weight"]
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required key")

    def test_discount_rate_evidence_abstention_with_populated_component_rejected(self):
        dre = _discount_rate_evidence()
        dre["abstention_reason"] = "should not be here"
        data = _record(discount_rate_evidence=dre)
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="must be absent when at least one component is populated")


# ── 29: filename-stem matching ────────────────────────────────────────────

class TestFilenameStemMatching:
    def test_matching_filename_valid(self, tmp_path: Path):
        data = _record(ticker="ZZFAKE5", sealed=True)
        p = tmp_path / "ZZFAKE5.yaml"
        p.write_text(yaml.safe_dump(data))
        result = vev.validate_valuation_evidence_file(p)
        assert_valid(result)

    def test_mismatched_filename_rejected(self, tmp_path: Path):
        data = _record(ticker="ZZFAKE5", sealed=True)
        p = tmp_path / "WRONGNAME.yaml"
        p.write_text(yaml.safe_dump(data))
        result = vev.validate_valuation_evidence_file(p)
        assert_invalid(result, contains="does not match the record's own ticker")

    def test_malformed_yaml_rejected(self, tmp_path: Path):
        p = tmp_path / "BROKEN.yaml"
        p.write_text("ticker: [unclosed")
        result = vev.validate_valuation_evidence_file(p)
        assert_invalid(result, contains="invalid YAML")

    def test_empty_file_rejected(self, tmp_path: Path):
        p = tmp_path / "EMPTY.yaml"
        p.write_text("")
        result = vev.validate_valuation_evidence_file(p)
        assert_invalid(result, contains="file is empty")

    def test_missing_file_rejected(self, tmp_path: Path):
        result = vev.validate_valuation_evidence_file(tmp_path / "does_not_exist.yaml")
        assert_invalid(result, contains="could not read file")


# ── 30: manifest validation ───────────────────────────────────────────────

class TestCohortManifest:
    def _sealed(self, ticker: str) -> dict:
        return _record(ticker=ticker, sealed=True)

    def _manifest_row(self, record: dict) -> dict:
        return {
            "ticker": record["ticker"],
            "sealed_at": record["sealed_at"],
            "content_sha256": record["content_sha256"],
            "schema_version": record["schema_version"],
            "governing_decision": record["governing_decision"],
            "record_path": f"intelligence/valuation_evidence/{record['ticker']}.yaml",
        }

    def test_manifest_roundtrip_valid(self, tmp_path: Path):
        r1 = self._sealed("ZZFAKE6")
        r2 = self._sealed("ZZFAKE7")
        records_by_ticker = {"ZZFAKE6": r1, "ZZFAKE7": r2}
        manifest = {"schema_version": "1.0", "governing_decision": "VALUATION-0004", "cohort": [self._manifest_row(r1), self._manifest_row(r2)]}
        result = vev.validate_cohort_manifest(manifest, records_by_ticker)
        assert_valid(result)

    def test_manifest_missing_row_for_sealed_record_rejected(self, tmp_path: Path):
        r1 = self._sealed("ZZFAKE8")
        manifest = {"cohort": []}
        result = vev.validate_cohort_manifest(manifest, {"ZZFAKE8": r1})
        assert_invalid(result, contains="no corresponding cohort manifest entry")

    def test_manifest_orphan_row_no_matching_record_rejected(self):
        manifest = {"cohort": [{
            "ticker": "GHOSTCO", "sealed_at": "x", "content_sha256": "deadbeef",
            "schema_version": "1.0", "governing_decision": "VALUATION-0004", "record_path": "x",
        }]}
        result = vev.validate_cohort_manifest(manifest, {})
        assert_invalid(result, contains="no corresponding sealed record file")

    def test_manifest_duplicate_ticker_rejected(self):
        r1 = self._sealed("ZZFAKE9")
        row = self._manifest_row(r1)
        manifest = {"cohort": [row, dict(row)]}
        result = vev.validate_cohort_manifest(manifest, {"ZZFAKE9": r1})
        assert_invalid(result, contains="more than once")

    def test_manifest_hash_mismatch_rejected(self):
        r1 = self._sealed("ZZFAKE10")
        row = self._manifest_row(r1)
        row["content_sha256"] = "0" * 64
        manifest = {"cohort": [row]}
        result = vev.validate_cohort_manifest(manifest, {"ZZFAKE10": r1})
        assert_invalid(result, contains="content_sha256 mismatch")

    def test_manifest_no_closed_population_constraint(self):
        """Roster-agnostic: validate_cohort_manifest takes no
        authorized_population parameter, unlike the ETF/crypto sibling
        validators' closed-population design (VALUATION-0004 SS B)."""
        import inspect
        sig = inspect.signature(vev.validate_cohort_manifest)
        assert "authorized_population" not in sig.parameters


# ── 31: directory validation ──────────────────────────────────────────────

class TestDirectoryValidation:
    def test_missing_directory_is_valid_zero_coverage(self, tmp_path: Path):
        result = vev.validate_valuation_evidence_directory(tmp_path / "intelligence" / "valuation_evidence")
        assert result.valid is True
        assert result.record_count == 0

    def test_nonexistent_arbitrary_path_is_valid_zero_coverage(self, tmp_path: Path):
        result = vev.validate_valuation_evidence_directory(tmp_path / "does" / "not" / "exist")
        assert result.valid is True
        assert result.record_count == 0

    def test_synthetic_directory_with_two_sealed_records_and_manifest_valid(self, tmp_path: Path):
        d = tmp_path / "valuation_evidence"
        d.mkdir()
        r1 = _record(ticker="ZZFAKE11", sealed=True)
        r2 = _record(ticker="ZZFAKE12", sealed=True)
        (d / "ZZFAKE11.yaml").write_text(yaml.safe_dump(r1))
        (d / "ZZFAKE12.yaml").write_text(yaml.safe_dump(r2))
        manifest = {
            "schema_version": "1.0",
            "governing_decision": "VALUATION-0004",
            "cohort": [
                {
                    "ticker": r["ticker"], "sealed_at": r["sealed_at"], "content_sha256": r["content_sha256"],
                    "schema_version": r["schema_version"], "governing_decision": r["governing_decision"],
                    "record_path": f"intelligence/valuation_evidence/{r['ticker']}.yaml",
                }
                for r in (r1, r2)
            ],
        }
        (d / "COHORT_MANIFEST.yaml").write_text(yaml.safe_dump(manifest))
        result = vev.validate_valuation_evidence_directory(d)
        assert result.valid is True
        assert result.record_count == 3  # two records + one manifest result

    def test_synthetic_directory_missing_manifest_when_records_exist_rejected(self, tmp_path: Path):
        d = tmp_path / "valuation_evidence"
        d.mkdir()
        r1 = _record(ticker="ZZFAKE13", sealed=True)
        (d / "ZZFAKE13.yaml").write_text(yaml.safe_dump(r1))
        result = vev.validate_valuation_evidence_directory(d)
        assert result.valid is False


# ── 32: seal validation ───────────────────────────────────────────────────

class TestSealValidation:
    def test_draft_record_needs_no_seal_fields(self):
        data = _record(sealed=False)
        assert "content_sha256" not in data
        assert_valid(vev.validate_valuation_evidence_data(data))

    def test_sealed_record_missing_seal_fields_rejected(self):
        data = _record(sealed=False)
        data["record_status"] = "sealed"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="missing required seal field")

    def test_sealed_record_wrong_hash_rejected(self):
        data = _record(sealed=True)
        data["content_sha256"] = "0" * 64
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="does not reproduce")

    def test_invalid_record_status_rejected(self):
        data = _record()
        data["record_status"] = "published"
        assert_invalid(vev.validate_valuation_evidence_data(data), contains="record_status must be one of")


# ── 33/34: zero real-company population, absolute ────────────────────────

class TestAuthorizedCohortPopulation:
    """VALUATION-0005 authorized exactly one bounded Stage-3 population unit:
    the 27-name canonical equity cohort. These tests supersede the prior
    TestZeroRealCompanyPopulation class, which asserted the opposite (zero
    population) -- accurate for the Stage-2 scaffold this validator shipped
    with, not for this implementation, which performs the authorized
    population itself. The schema and this validator module remain
    roster-agnostic (SS B) -- these tests check the *content* of this one
    population, not a closed-population rule inside the validator itself."""

    _AUTHORIZED_27 = frozenset({
        "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC", "GOOGL",
        "ICE", "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR",
        "RKLB", "RTX", "SNPS", "SPGI", "TMO", "TSLA", "TSM", "V", "WM",
    })

    def test_valuation_evidence_directory_exists_with_authorized_cohort(self):
        d = REPO_ROOT / "intelligence" / "valuation_evidence"
        assert d.is_dir()
        tickers = {p.stem for p in d.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        assert tickers == self._AUTHORIZED_27

    def test_cohort_manifest_is_committed_and_reconciles(self):
        manifest_path = REPO_ROOT / "intelligence" / "valuation_evidence" / "COHORT_MANIFEST.yaml"
        assert manifest_path.is_file()
        manifest = yaml.safe_load(manifest_path.read_text())
        rows = {row["ticker"] for row in manifest["cohort"]}
        assert rows == self._AUTHORIZED_27

    def test_validator_source_contains_no_hardcoded_authorized_population(self):
        """The module may legitimately mention real tickers only inside
        prose citing other governance decisions/validators (e.g. the
        docstring's own references to VALUATION-0003's 27-name cohort) --
        it must never hardcode the authorized population as validator
        logic, since the schema itself stays roster-agnostic (SS B)."""
        assert not hasattr(vev, "AUTHORIZED_POPULATION")
        assert not hasattr(vev, "DEFAULT_TICKER")

    def test_repository_directory_scan_returns_exactly_27_records(self):
        result = vev.validate_valuation_evidence_directory(REPO_ROOT / "intelligence" / "valuation_evidence")
        assert result.valid is True
        assert result.record_count == 28  # 27 sealed records + 1 manifest result

    def test_every_sealed_record_is_marked_sealed_and_hash_matches(self):
        d = REPO_ROOT / "intelligence" / "valuation_evidence"
        for ticker in self._AUTHORIZED_27:
            data = yaml.safe_load((d / f"{ticker}.yaml").read_text())
            assert data["record_status"] == "sealed"
            assert data["content_sha256"] == vev.canonical_record_hash(data)

    def test_authorized_cohort_helper_confirms_exact_match_against_live_targets(self):
        sys.path.insert(0, str(REPO_ROOT))
        from relationship_validator import load_canonical_universe

        canonical = load_canonical_universe(REPO_ROOT)
        assert canonical == self._AUTHORIZED_27

        d = REPO_ROOT / "intelligence" / "valuation_evidence"
        records_by_ticker = {}
        for p in d.glob("*.yaml"):
            if p.name == "COHORT_MANIFEST.yaml":
                continue
            data = yaml.safe_load(p.read_text())
            records_by_ticker[data["ticker"]] = data

        result = vev.validate_authorized_cohort(records_by_ticker, canonical)
        assert result.valid is True
        assert result.errors == []
