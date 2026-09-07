"""Tests for freshness_validator.py (AUTO-0002 bounded local-foundation
scope).

All fixtures use fictional/synthetic tickers only. No real portfolio
judgment appears in this file.
"""

import ast
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

import freshness_validator as fval


# ── fixtures ─────────────────────────────────────────────────────────────

def _registry_row(**overrides) -> dict:
    row = {
        "ticker": "ZZZZ",
        "company_record_authority": "PI-9999",
        "enrollment_authority": "AUTO-0001",
        "enrolled_at": "2026-07-19",
        "template_version": "v1",
        "filing_trigger_profile": "domestic_issuer_v1",
        "refresh_policy": "path_a_fixed_scope_v1",
        "monitoring_enabled": False,
    }
    row.update(overrides)
    return row


def _checkpoint_row(**overrides) -> dict:
    row = {
        "ticker": "ZZZZ",
        "checkpoint_status": "pending",
        "channels": {},
        "established_by": None,
    }
    row.update(overrides)
    return row


def _registry_doc(rows: list[dict]) -> dict:
    return {"schema_version": 1, "tickers": rows}


def _checkpoints_doc(rows: list[dict]) -> dict:
    return {"schema_version": 1, "tickers": rows}


def _domestic_channel(name: str, **overrides) -> dict:
    form = fval._CHANNEL_OFFICIAL_FORM_TYPE[name]
    ch = {
        "channel_name": name,
        "official_form_type": form,
        "stable_source_id": f"acc-{name}",
        "official_source_date": "2026-01-01",
        "fiscal_period": "FY2026Q1",
        "incorporation_reference": "PR#1",
    }
    ch.update(overrides)
    return ch


def _complete_domestic_channels(ticker_suffix: str = "") -> dict:
    return {
        name: _domestic_channel(name, stable_source_id=f"acc-{name}{ticker_suffix}")
        for name in fval._DOMESTIC_CHANNELS
    }


# Distinguishes "argument omitted" from "explicit None" -- a bare `None`
# default would make an explicit `earnings_release=None` call
# indistinguishable from omission, silently building a default complete
# object instead of the null value the caller actually asked for.
_UNSET = object()


def _complete_fpi_channels(ticker_suffix: str = "", earnings_release=_UNSET) -> dict:
    """Three distinct, explicit states for earnings_release:
    - omitted (default) -> a default complete channel object;
    - explicit None -> the null value itself, unmodified;
    - explicit mapping -> that mapping, unmodified."""
    channels = {}
    for name in ("annual_20f", "earnings_6k_watermark"):
        channels[name] = _domestic_channel(name, stable_source_id=f"acc-{name}{ticker_suffix}")
    if earnings_release is _UNSET:
        channels["earnings_release"] = _domestic_channel(
            "earnings_release", stable_source_id=f"acc-er{ticker_suffix}"
        )
    else:
        channels["earnings_release"] = earnings_release
    return channels


# ── top-level document schema ──────────────────────────────────────────────

@pytest.mark.parametrize("bad_root", [["a", "list"], "a string", 5, None])
def test_non_mapping_root_is_rejected_for_both_files(bad_root):
    result = fval.validate_registry_and_checkpoints(bad_root, bad_root)
    assert result.valid is False
    assert any("mapping" in e for e in result.errors)


def test_missing_schema_version_is_distinct_from_malformed():
    doc = {"tickers": []}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is False
    assert any("missing required top-level key: schema_version" in e for e in result.errors)


@pytest.mark.parametrize("bad_version", [2, "1", 1.0, True])
def test_malformed_schema_version_is_rejected(bad_version):
    doc = {"schema_version": bad_version, "tickers": []}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is False
    assert any("schema_version" in e and "missing" not in e for e in result.errors)


def test_schema_version_exactly_1_is_accepted():
    doc = {"schema_version": 1, "tickers": []}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    # both empty and bijective -> no cross-file errors either
    assert result.valid is True


def test_missing_tickers_key_is_distinct_error():
    doc = {"schema_version": 1}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is False
    assert any("missing required top-level key: tickers" in e for e in result.errors)


def test_malformed_tickers_not_a_list_is_rejected():
    doc = {"schema_version": 1, "tickers": {"not": "a list"}}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is False
    assert any("tickers must be a list" in e for e in result.errors)


def test_non_mapping_ticker_row_is_rejected():
    doc = {"schema_version": 1, "tickers": ["not-a-mapping"]}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is False
    assert any("tickers[0] must be a mapping" in e for e in result.errors)


def test_unexpected_top_level_keys_permitted():
    doc = {"schema_version": 1, "tickers": [], "extra_future_key": "whatever"}
    result = fval.validate_registry_and_checkpoints(doc, doc)
    assert result.valid is True


# ── registry row schema ──────────────────────────────────────────────────

def _valid_pair():
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([_checkpoint_row()])
    return reg, chk


def test_valid_minimal_pair_passes():
    reg, chk = _valid_pair()
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True
    assert result.errors == []


@pytest.mark.parametrize("missing_key", sorted(fval._REGISTRY_ROW_REQUIRED_KEYS))
def test_registry_row_missing_each_required_key(missing_key):
    row = _registry_row()
    del row[missing_key]
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("missing required key" in e and missing_key in e for e in result.errors)


@pytest.mark.parametrize("key", ["ticker", "company_record_authority", "enrollment_authority",
                                  "template_version", "refresh_policy"])
@pytest.mark.parametrize("bad_value", ["", "   ", 5, None, []])
def test_registry_row_required_string_fields_rejected(key, bad_value):
    row = _registry_row(**{key: bad_value})
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False


def test_registry_row_unrecognized_keys_permitted():
    row = _registry_row(some_future_field="ok")
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_registry_duplicate_ticker_case_sensitive_uniqueness():
    reg = _registry_doc([_registry_row(), _registry_row()])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("duplicate ticker row in registry" in e for e in result.errors)


def test_registry_ticker_no_normalization_lowercase_is_distinct():
    # "zzzz" and "ZZZZ" are NOT the same ticker -- no normalization.
    reg = _registry_doc([_registry_row(ticker="ZZZZ"), _registry_row(ticker="zzzz")])
    chk = _checkpoints_doc([_checkpoint_row(ticker="ZZZZ"), _checkpoint_row(ticker="zzzz")])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


@pytest.mark.parametrize("bad_profile", [
    "DOMESTIC_ISSUER_V1", "domestic", "", None, 5,
    [],                          # unhashable -- `in` against a set must not raise TypeError
    {},                            # unhashable
    ["domestic_issuer_v1"],         # unhashable, and would even textually resemble a valid value
    {"profile": "domestic_issuer_v1"},  # unhashable
])
def test_registry_invalid_filing_trigger_profile_rejected(bad_profile):
    row = _registry_row(filing_trigger_profile=bad_profile)
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)  # must not raise TypeError
    assert result.valid is False
    assert any("filing_trigger_profile" in e for e in result.errors)


@pytest.mark.parametrize("good_profile", sorted(fval._FILING_TRIGGER_PROFILES))
def test_registry_valid_filing_trigger_profiles_accepted(good_profile):
    row = _registry_row(filing_trigger_profile=good_profile)
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


@pytest.mark.parametrize("bad_bool", [0, 1, "true", "false", None, "True"])
def test_registry_monitoring_enabled_exact_bool_enforcement(bad_bool):
    row = _registry_row(monitoring_enabled=bad_bool)
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("monitoring_enabled" in e for e in result.errors)


@pytest.mark.parametrize("good_bool", [True, False])
def test_registry_monitoring_enabled_accepts_real_bools(good_bool):
    row = _registry_row(monitoring_enabled=good_bool)
    chk_row = _checkpoint_row(
        checkpoint_status="verified" if good_bool else "pending",
        channels=_complete_domestic_channels() if good_bool else {},
    )
    reg = _registry_doc([row])
    chk = _checkpoints_doc([chk_row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


# ── local ISO-date rule ─────────────────────────────────────────────────────

@pytest.mark.parametrize("good_date", [date(2026, 7, 19), "2026-07-19", "2000-01-01"])
def test_iso_date_rule_accepts_date_object_and_strict_string(good_date):
    assert fval._is_valid_local_date(good_date) is True


@pytest.mark.parametrize("bad_date", [
    datetime(2026, 7, 19, 12, 0, 0),
    "2026/07/19",
    "07-19-2026",
    "2026-13-01",
    "not-a-date",
    "2026-7-19",
    12345,
    None,
])
def test_iso_date_rule_rejects_datetime_and_malformed(bad_date):
    assert fval._is_valid_local_date(bad_date) is False


def test_registry_enrolled_at_rejects_datetime():
    row = _registry_row(enrolled_at=datetime(2026, 7, 19, 1, 2, 3))
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("enrolled_at" in e for e in result.errors)


def test_registry_enrolled_at_accepts_date_object():
    row = _registry_row(enrolled_at=date(2026, 7, 19))
    reg = _registry_doc([row])
    chk = _checkpoints_doc([_checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


# ── checkpoint row schema ───────────────────────────────────────────────────

@pytest.mark.parametrize("missing_key", sorted(fval._CHECKPOINT_ROW_REQUIRED_KEYS))
def test_checkpoint_row_missing_each_required_key(missing_key):
    row = _checkpoint_row()
    del row[missing_key]
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("missing required key" in e and missing_key in e for e in result.errors)


@pytest.mark.parametrize("bad_status", [
    "Pending", "VERIFIED", "", None, 5,
    [],                     # unhashable -- `in` against a set must not raise TypeError
    {},                       # unhashable
    ["pending"],               # unhashable
    {"status": "pending"},      # unhashable
])
def test_checkpoint_status_closed_vocabulary(bad_status):
    row = _checkpoint_row(checkpoint_status=bad_status)
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)  # must not raise TypeError
    assert result.valid is False
    assert any("checkpoint_status" in e for e in result.errors)


def test_established_by_required_but_nullable():
    row = _checkpoint_row(established_by=None)
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_established_by_non_empty_string_accepted():
    row = _checkpoint_row(established_by="PR#42")
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


@pytest.mark.parametrize("bad_value", ["", "   ", 5, [], {}])
def test_established_by_rejects_non_null_non_string(bad_value):
    row = _checkpoint_row(established_by=bad_value)
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("established_by" in e for e in result.errors)


def test_pending_checkpoint_with_populated_structurally_valid_channels_not_rejected_for_being_pending():
    row = _checkpoint_row(checkpoint_status="pending", channels=_complete_domestic_channels())
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_checkpoint_duplicate_ticker_rejected():
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([_checkpoint_row(), _checkpoint_row()])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("duplicate ticker row in checkpoints" in e for e in result.errors)


# ── channel object schema ───────────────────────────────────────────────────

@pytest.mark.parametrize("missing_key", sorted(fval._CHANNEL_REQUIRED_KEYS))
def test_channel_object_missing_each_required_key(missing_key):
    ch = _domestic_channel("annual_filing")
    del ch[missing_key]
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("annual_filing" in e and "missing required key" in e for e in result.errors)


def test_channel_name_must_match_parent_key():
    ch = _domestic_channel("annual_filing")
    ch["channel_name"] = "quarterly_filing"
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("channel_name" in e for e in result.errors)


@pytest.mark.parametrize("name,expected_form", sorted(fval._CHANNEL_OFFICIAL_FORM_TYPE.items()))
def test_every_official_form_mapping(name, expected_form):
    ch = _domestic_channel(name)
    assert ch["official_form_type"] == expected_form
    profile = "foreign_private_issuer_v1" if name in fval._FPI_CHANNELS and name != "earnings_release" else "domestic_issuer_v1"
    row = _checkpoint_row(channels={name: ch})
    reg = _registry_doc([_registry_row(filing_trigger_profile=profile)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_channel_wrong_official_form_type_rejected():
    ch = _domestic_channel("annual_filing", official_form_type="10-Q")
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("official_form_type" in e for e in result.errors)


@pytest.mark.parametrize("key", ["stable_source_id", "incorporation_reference"])
@pytest.mark.parametrize("bad_value", ["", "   ", 5, None, []])
def test_channel_required_string_fields_rejected(key, bad_value):
    ch = _domestic_channel("annual_filing", **{key: bad_value})
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False


def test_channel_official_source_date_rejects_datetime():
    ch = _domestic_channel("annual_filing", official_source_date=datetime(2026, 1, 1, 1, 1, 1))
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("official_source_date" in e for e in result.errors)


def test_channel_official_source_date_accepts_date_object():
    ch = _domestic_channel("annual_filing", official_source_date=date(2026, 1, 1))
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


@pytest.mark.parametrize("fiscal_period", [None, "FY2026Q1", ""])
def test_channel_fiscal_period_required_but_nullable_string(fiscal_period):
    ch = _domestic_channel("annual_filing", fiscal_period=fiscal_period)
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    # empty string is still a string -- spec never closes format/vocabulary
    assert result.valid is True


@pytest.mark.parametrize("bad_fiscal_period", [5, [], {}])
def test_channel_fiscal_period_rejects_non_string_non_null(bad_fiscal_period):
    ch = _domestic_channel("annual_filing", fiscal_period=bad_fiscal_period)
    row = _checkpoint_row(channels={"annual_filing": ch})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("fiscal_period" in e for e in result.errors)


def test_null_channel_value_permitted_when_not_verified():
    row = _checkpoint_row(channels={"annual_filing": None})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


# ── verified checkpoint exact channel sets ──────────────────────────────────

def test_domestic_verified_exact_channel_set_all_complete_passes():
    row = _checkpoint_row(checkpoint_status="verified", channels=_complete_domestic_channels())
    reg = _registry_doc([_registry_row(monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_domestic_verified_missing_one_channel_key_fails():
    channels = _complete_domestic_channels()
    del channels["earnings_release"]
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("verified checkpoint's channel key set" in e for e in result.errors)


def test_domestic_verified_earnings_release_null_rejected():
    channels = _complete_domestic_channels()
    channels["earnings_release"] = None
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("earnings_release" in e and "must not be null" in e for e in result.errors)


@pytest.mark.parametrize("null_channel", ["annual_filing", "quarterly_filing", "event_filing_watermark"])
def test_domestic_verified_every_other_channel_rejects_null(null_channel):
    channels = _complete_domestic_channels()
    channels[null_channel] = None
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False


def test_fpi_verified_exact_channel_set_all_complete_passes():
    # earnings_release omitted -> helper builds a default complete object.
    channels = _complete_fpi_channels()
    assert isinstance(channels["earnings_release"], dict)
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_fpi_verified_earnings_release_explicit_complete_object_passes():
    # earnings_release explicitly supplied as a complete mapping (distinct
    # from the omitted-default case above) -- also succeeds.
    explicit_object = _domestic_channel("earnings_release", stable_source_id="acc-er-explicit")
    channels = _complete_fpi_channels(earnings_release=explicit_object)
    assert channels["earnings_release"] == explicit_object
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_fpi_verified_missing_channel_key_fails():
    channels = _complete_fpi_channels()
    del channels["annual_20f"]
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("verified checkpoint's channel key set" in e for e in result.errors)


def test_fpi_verified_earnings_release_nullable():
    channels = _complete_fpi_channels(earnings_release=None)
    # Prior bug: the helper treated a bare `None` default as "omitted"
    # and silently built a default complete object instead, so this
    # assertion is what actually proves the null case is being
    # exercised -- without it, the test below would pass even if
    # earnings_release were never really null.
    assert channels["earnings_release"] is None
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


@pytest.mark.parametrize("null_channel", ["annual_20f", "earnings_6k_watermark"])
def test_fpi_verified_annual_20f_and_6k_reject_null(null_channel):
    channels = _complete_fpi_channels()
    channels[null_channel] = None
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False


# ── cross-file invariants ───────────────────────────────────────────────────

def test_ticker_set_mismatch_registry_orphan():
    reg = _registry_doc([_registry_row(ticker="AAAA"), _registry_row(ticker="BBBB")])
    chk = _checkpoints_doc([_checkpoint_row(ticker="AAAA")])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("BBBB" in e and "no checkpoint row" in e for e in result.errors)


def test_ticker_set_mismatch_checkpoint_orphan():
    reg = _registry_doc([_registry_row(ticker="AAAA")])
    chk = _checkpoints_doc([_checkpoint_row(ticker="AAAA"), _checkpoint_row(ticker="BBBB")])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("BBBB" in e and "no registry row" in e for e in result.errors)


def test_monitoring_true_with_pending_checkpoint_is_invalid():
    reg = _registry_doc([_registry_row(monitoring_enabled=True)])
    chk = _checkpoints_doc([_checkpoint_row(checkpoint_status="pending")])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("monitoring_enabled is true" in e for e in result.errors)


def test_monitoring_false_with_pending_checkpoint_is_valid():
    reg = _registry_doc([_registry_row(monitoring_enabled=False)])
    chk = _checkpoints_doc([_checkpoint_row(checkpoint_status="pending")])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_channel_not_valid_for_profile_rejected():
    channels = {"annual_20f": _domestic_channel("annual_20f")}
    row = _checkpoint_row(channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="domestic_issuer_v1")])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("not valid for filing_trigger_profile" in e for e in result.errors)


def test_pending_domestic_checkpoint_rejects_fpi_only_channel_key_even_when_null():
    """A domestic-profile ticker's checkpoint populating {"annual_20f":
    None} is invalid -- a null value is not a shortcut around key
    validity, and this must be rejected even while checkpoint_status is
    still pending."""
    row = _checkpoint_row(checkpoint_status="pending", channels={"annual_20f": None})
    reg = _registry_doc([_registry_row(filing_trigger_profile="domestic_issuer_v1")])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("annual_20f" in e and "not valid for filing_trigger_profile" in e for e in result.errors)


def test_pending_fpi_checkpoint_rejects_domestic_only_channel_key_even_when_null():
    row = _checkpoint_row(checkpoint_status="pending", channels={"annual_filing": None})
    reg = _registry_doc([_registry_row(filing_trigger_profile="foreign_private_issuer_v1")])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("annual_filing" in e and "not valid for filing_trigger_profile" in e for e in result.errors)


def test_pending_checkpoint_rejects_unknown_channel_key_with_null_value():
    row = _checkpoint_row(checkpoint_status="pending", channels={"unknown_channel": None})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("unknown_channel" in e and "closed channel-name universe" in e for e in result.errors)


def test_pending_checkpoint_rejects_unknown_populated_channel_key():
    row = _checkpoint_row(
        checkpoint_status="pending",
        channels={"unknown_channel": _domestic_channel("annual_filing", channel_name="unknown_channel")},
    )
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("unknown_channel" in e and "closed channel-name universe" in e for e in result.errors)


@pytest.mark.parametrize("bad_key", [5, 5.0, True, None, (1, 2)])
def test_non_string_channel_key_rejected(bad_key):
    row = _checkpoint_row(checkpoint_status="pending", channels={bad_key: None})
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("channel key must be a string" in e for e in result.errors)


def test_verified_checkpoint_malformed_heterogeneous_keys_returns_invalid_not_typeerror():
    """A verified checkpoint whose channels mapping mixes int/tuple/str
    keys must never crash the diagnostic that reports the mismatched key
    set (which sorts the actual keys for the error message) -- it must
    return a normal invalid ValidationResult."""
    channels = {5: None, (1, 2): "not-even-a-mapping", "annual_filing": None}
    row = _checkpoint_row(checkpoint_status="verified", channels=channels)
    reg = _registry_doc([_registry_row(filing_trigger_profile="domestic_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)  # must not raise
    assert result.valid is False
    assert result.errors


def test_verified_checkpoint_still_valid_when_channel_keys_are_all_governed_and_complete():
    """Sanity companion to the heterogeneous-key crash test: a verified
    domestic checkpoint with only governed, correctly-typed keys still
    validates cleanly (the new key checks don't over-reject valid input)."""
    row = _checkpoint_row(checkpoint_status="verified", channels=_complete_domestic_channels())
    reg = _registry_doc([_registry_row(filing_trigger_profile="domestic_issuer_v1", monitoring_enabled=True)])
    chk = _checkpoints_doc([row])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_duplicate_stable_source_id_across_two_tickers_rejected():
    reg = _registry_doc([_registry_row(ticker="AAAA"), _registry_row(ticker="BBBB")])
    channels_a = {"annual_filing": _domestic_channel("annual_filing", stable_source_id="shared-id")}
    channels_b = {"annual_filing": _domestic_channel("annual_filing", stable_source_id="shared-id")}
    chk = _checkpoints_doc([
        _checkpoint_row(ticker="AAAA", channels=channels_a),
        _checkpoint_row(ticker="BBBB", channels=channels_b),
    ])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is False
    assert any("shared-id" in e and "claimed under two different tickers" in e for e in result.errors)


def test_same_stable_source_id_same_ticker_multiple_channels_allowed():
    channels = {
        "annual_filing": _domestic_channel("annual_filing", stable_source_id="dup-id"),
        "quarterly_filing": _domestic_channel("quarterly_filing", stable_source_id="dup-id"),
    }
    reg = _registry_doc([_registry_row()])
    chk = _checkpoints_doc([_checkpoint_row(channels=channels)])
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


# ── real committed seed files ───────────────────────────────────────────────

def test_committed_seed_files_are_valid():
    repo_root = Path(__file__).resolve().parent
    result = fval.validate_registry_and_checkpoints_files(
        repo_root / "intelligence" / "freshness_registry.yaml",
        repo_root / "intelligence" / "freshness_checkpoints.yaml",
    )
    assert result.valid is True
    assert result.errors == []


def test_committed_seed_files_parsed_and_validated_in_memory():
    repo_root = Path(__file__).resolve().parent
    reg = yaml.safe_load((repo_root / "intelligence" / "freshness_registry.yaml").read_text())
    chk = yaml.safe_load((repo_root / "intelligence" / "freshness_checkpoints.yaml").read_text())
    result = fval.validate_registry_and_checkpoints(reg, chk)
    assert result.valid is True


def test_validate_files_missing_file_reports_error():
    result = fval.validate_registry_and_checkpoints_files(
        "/nonexistent/path/registry.yaml", "/nonexistent/path/checkpoints.yaml"
    )
    assert result.valid is False
    assert result.errors


# ── no replacement-authorization behavior ──────────────────────────────────

def test_module_has_no_replacement_authorization_functions():
    public_names = [n for n in dir(fval) if not n.startswith("_")]
    for name in public_names:
        assert "replacement" not in name.lower()


def test_module_never_reads_freshness_replacements_directory():
    """The docstring documents that replacement-authorization validation
    is out of scope (mentioning the path in prose is fine) -- what must
    never exist is executable code that opens, globs, or constructs a
    Path against it."""
    tree = ast.parse(Path(fval.__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if "freshness_replacements" in node.value:
                # only permitted inside the module's own docstring
                assert node.value.lstrip().startswith("freshness_validator.py"), (
                    f"unexpected non-docstring reference to freshness_replacements: {node.value!r}"
                )


# ── architectural / isolation invariants ────────────────────────────────────

def _is_main_guard(node: ast.stmt) -> bool:
    """True for exactly `if __name__ == "__main__": ...` -- the one
    permitted top-level statement shape that isn't itself executed at
    import time."""
    if not isinstance(node, ast.If):
        return False
    test = node.test
    return (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and len(test.comparators) == 1
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == "__main__"
    )


def test_module_has_no_top_level_side_effecting_statements():
    tree = ast.parse(Path(fval.__file__).read_text())
    allowed_top_level = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef, ast.Assign, ast.AnnAssign, ast.Expr)
    for node in tree.body:
        if _is_main_guard(node):
            continue
        assert isinstance(node, allowed_top_level), f"unexpected top-level statement: {ast.dump(node)}"
        if isinstance(node, ast.Expr):
            assert isinstance(node.value, ast.Constant)


def test_module_imports_no_network_or_subprocess_libraries():
    tree = ast.parse(Path(fval.__file__).read_text())
    forbidden = {"requests", "urllib", "socket", "http.client", "subprocess"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & forbidden)


def test_module_does_not_import_allocate_or_margin_state():
    tree = ast.parse(Path(fval.__file__).read_text())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert "allocate" not in imported
    assert "margin_state" not in imported


def test_module_does_not_import_intelligence_validator_or_report():
    source = Path(fval.__file__).read_text()
    tree = ast.parse(source)
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.add(node.module)
    assert "intelligence_validator" not in imported_names
    assert "intelligence_report" not in imported_names


def test_module_never_opens_files_in_write_mode():
    source = Path(fval.__file__).read_text()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "open":
                for kw in node.keywords:
                    if kw.arg == "mode":
                        assert isinstance(kw.value, ast.Constant)
                        assert "w" not in kw.value.value and "a" not in kw.value.value
    assert "write_text" not in source
    assert "write_bytes" not in source


def test_public_api_includes_validate_registry_and_checkpoints():
    assert hasattr(fval, "validate_registry_and_checkpoints")
    assert callable(fval.validate_registry_and_checkpoints)
