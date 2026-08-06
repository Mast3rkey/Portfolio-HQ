"""Tests for contender_registry_validator.py (CONTENDER-0002 §E/§I/§J scope).

Every schema-shape test below constructs its own synthetic fixture — no
real portfolio ticker or real investment judgment appears in any synthetic
fixture in this file, matching test_relationship_validator.py's own
authorized-scope discipline. The tests reading the real generated
intelligence/contenders/registry.yaml (below, under "real registry") are
the sole exception.
"""

import ast
from pathlib import Path

import pytest
import yaml

import contender_registry_validator as crv


# ── fixtures ─────────────────────────────────────────────────────────────

def _flags(**overrides) -> dict:
    flags = dict.fromkeys(crv.SECONDARY_FLAG_KEYS, False)
    flags.update(overrides)
    return flags


def _entry(**overrides) -> dict:
    entry = {
        "canonical_symbol": "ZZZQ",
        "asset_type": "equity",
        "primary_disposition": "evaluation_ready",
        "secondary_flags": _flags(),
        "provenance": [{"source": "targets.yaml", "role": "discovery"}],
        "investability_status": "investable",
        "research_status": "governed_record_exists",
        "evidence_freshness_status": "current_per_owned_freshness_fields",
        "classification_status": "not_applicable",
        "current_policy_status": {},
        "existing_disposition": None,
        "duplicate_of": None,
        "reason": "synthetic fixture reason",
        "review_trigger": None,
        "next_required_action": "synthetic next action",
    }
    entry.update(overrides)
    return entry


def _registry(entries: list[dict], **header_overrides) -> dict:
    header = {
        "schema_version": 1,
        "source_commit_sha": "deadbeef",
        "generated_at": "2026-08-06T00:00:00Z",
        "governing_authority": "governance/decisions/CONTENDER-0002-...",
    }
    header.update(header_overrides)
    header["entries"] = entries
    return header


# ── §E.2 closed vocabulary ───────────────────────────────────────────────

def test_twelve_value_vocabulary_exact():
    assert len(crv.PRIMARY_DISPOSITIONS) == 12
    assert len(crv.PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER) == 12
    assert set(crv.PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER) == crv.PRIMARY_DISPOSITIONS


def test_valid_entry_passes():
    result = crv.validate_entry(_entry())
    assert result.valid, result.errors


def test_unknown_disposition_rejected():
    result = crv.validate_entry(_entry(primary_disposition="made_up_value"))
    assert not result.valid
    assert any("primary_disposition" in e for e in result.errors)


@pytest.mark.parametrize("disposition", sorted(crv.PRIMARY_DISPOSITIONS))
def test_every_closed_vocabulary_value_accepted(disposition):
    entry = _entry(primary_disposition=disposition)
    if disposition == "duplicate_or_alias":
        entry["duplicate_of"] = "SOME_OTHER_SYMBOL"
    result = crv.validate_entry(entry, known_symbols=frozenset({"SOME_OTHER_SYMBOL", "ZZZQ"}))
    assert result.valid, result.errors


# ── §E.3 secondary flags ─────────────────────────────────────────────────

def test_secondary_flags_missing_key_rejected():
    flags = _flags()
    del flags["has_current_gate"]
    result = crv.validate_entry(_entry(secondary_flags=flags))
    assert not result.valid
    assert any("secondary_flags" in e and "missing" in e for e in result.errors)


def test_secondary_flags_extra_key_rejected():
    flags = _flags()
    flags["not_a_real_flag"] = True
    result = crv.validate_entry(_entry(secondary_flags=flags))
    assert not result.valid


def test_secondary_flags_non_boolean_rejected():
    flags = _flags()
    flags["current_holding"] = "yes"
    result = crv.validate_entry(_entry(secondary_flags=flags))
    assert not result.valid


def test_eight_secondary_flags_exact():
    assert len(crv.SECONDARY_FLAG_KEYS) == 8


# ── §C duplicate/alias integrity ─────────────────────────────────────────

def test_duplicate_or_alias_requires_duplicate_of():
    result = crv.validate_entry(_entry(primary_disposition="duplicate_or_alias", duplicate_of=None))
    assert not result.valid
    assert any("duplicate_of" in e for e in result.errors)


def test_duplicate_of_must_resolve_to_known_symbol():
    result = crv.validate_entry(
        _entry(primary_disposition="duplicate_or_alias", duplicate_of="GHOST"),
        known_symbols=frozenset({"ZZZQ"}),
    )
    assert not result.valid
    assert any("does not resolve" in e for e in result.errors)


def test_no_duplicate_canonical_symbols_in_registry():
    data = _registry([_entry(canonical_symbol="AAA"), _entry(canonical_symbol="AAA")])
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("duplicate canonical_symbol" in e for e in result.errors)


# ── §I ordering / header ─────────────────────────────────────────────────

def test_entries_must_be_alphabetically_ordered():
    data = _registry([_entry(canonical_symbol="ZZZ"), _entry(canonical_symbol="AAA")])
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("alphabetical order" in e for e in result.errors)


def test_missing_header_key_rejected():
    data = _registry([_entry()])
    del data["source_commit_sha"]
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("header missing" in e for e in result.errors)


def test_valid_registry_passes():
    data = _registry([_entry(canonical_symbol="AAA"), _entry(canonical_symbol="BBB")])
    result = crv.validate_registry_data(data)
    assert result.valid, result.errors


# ── §G legacy-gap record shape ────────────────────────────────────────────

def _legacy_gap(**overrides) -> dict:
    gap = {
        "known_unenumerated_legacy_gap": True,
        "reported_count": "approximately 41",
        "source_authority": "PHQ-2026-02",
        "clone_depth_at_generation": "shallow",
        "recovery_status": "unavailable_in_current_clone",
        "registry_entries_created": 0,
        "next_action": "separately_authorized_history_recovery_sub_unit",
    }
    gap.update(overrides)
    return gap


def test_legacy_gap_valid_shape_passes():
    data = _registry([_entry()])
    data["legacy_gap"] = _legacy_gap()
    result = crv.validate_registry_data(data)
    assert result.valid, result.errors


def test_legacy_gap_valid_shape_passes_complete_clone_branch():
    data = _registry([_entry()])
    data["legacy_gap"] = _legacy_gap(
        clone_depth_at_generation="complete",
        recovery_status="reachable_but_recovery_not_attempted_this_generation",
    )
    result = crv.validate_registry_data(data)
    assert result.valid, result.errors


def test_legacy_gap_nonzero_entries_created_rejected():
    data = _registry([_entry()])
    data["legacy_gap"] = _legacy_gap(registry_entries_created=3, next_action="x")
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("must be exactly 0" in e for e in result.errors)


def test_legacy_gap_missing_key_rejected():
    data = _registry([_entry()])
    data["legacy_gap"] = {"known_unenumerated_legacy_gap": True}
    result = crv.validate_registry_data(data)
    assert not result.valid


def test_legacy_gap_unknown_clone_depth_rejected():
    data = _registry([_entry()])
    data["legacy_gap"] = _legacy_gap(clone_depth_at_generation="somewhat_shallow")
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("clone_depth_at_generation" in e for e in result.errors)


def test_legacy_gap_unknown_recovery_status_rejected():
    data = _registry([_entry()])
    data["legacy_gap"] = _legacy_gap(recovery_status="fully_recovered_and_verified")
    result = crv.validate_registry_data(data)
    assert not result.valid
    assert any("recovery_status" in e for e in result.errors)


def test_clone_depth_and_recovery_status_vocabularies_are_closed():
    assert crv.CLONE_DEPTH_VALUES == {"shallow", "complete"}
    assert crv.RECOVERY_STATUS_VALUES == {
        "unavailable_in_current_clone",
        "recovered_n_of_41",
        "recovery_ambiguous",
        "reachable_but_recovery_not_attempted_this_generation",
    }


# ── §B provenance ──────────────────────────────────────────────────────────

def test_unauthorized_source_label_rejected():
    result = crv.validate_entry(_entry(provenance=[{"source": "not_a_real_source", "role": "discovery"}]))
    assert not result.valid
    assert any("authorized" in e for e in result.errors)


def test_unknown_role_rejected():
    result = crv.validate_entry(_entry(provenance=[{"source": "targets.yaml", "role": "invented_role"}]))
    assert not result.valid


def test_empty_provenance_rejected():
    result = crv.validate_entry(_entry(provenance=[]))
    assert not result.valid


# ── §J bidirectional reconciliation ─────────────────────────────────────

def test_reconcile_clean_passes():
    r = crv.reconcile(
        discovered_symbols=frozenset({"AAA", "BBB", "NOISE"}),
        registry_symbols=frozenset({"AAA", "BBB"}),
        excluded_with_reason=frozenset({"NOISE"}),
    )
    assert r.valid, r.errors
    assert r.discovered_count == 3
    assert r.registered_count == 2
    assert r.excluded_with_reason_count == 1


def test_reconcile_fails_on_unaccounted_discovery():
    r = crv.reconcile(
        discovered_symbols=frozenset({"AAA", "MISSING"}),
        registry_symbols=frozenset({"AAA"}),
        excluded_with_reason=frozenset(),
    )
    assert not r.valid
    assert any("MISSING" in e for e in r.errors)


def test_reconcile_fails_on_invented_registry_entry():
    r = crv.reconcile(
        discovered_symbols=frozenset({"AAA"}),
        registry_symbols=frozenset({"AAA", "INVENTED"}),
        excluded_with_reason=frozenset(),
    )
    assert not r.valid
    assert any("INVENTED" in e for e in r.errors)


# ── file I/O ───────────────────────────────────────────────────────────

def test_validate_registry_file_missing(tmp_path):
    result = crv.validate_registry_file(tmp_path / "nope.yaml")
    assert not result.valid


def test_validate_registry_file_empty(tmp_path):
    p = tmp_path / "empty.yaml"
    p.write_text("")
    result = crv.validate_registry_file(p)
    assert not result.valid


def test_validate_registry_file_roundtrip(tmp_path):
    data = _registry([_entry(canonical_symbol="AAA")])
    p = tmp_path / "registry.yaml"
    p.write_text(yaml.safe_dump(data))
    result = crv.validate_registry_file(p)
    assert result.valid, result.errors


# ── real, generated registry ─────────────────────────────────────────────

_REAL_REGISTRY_PATH = Path(__file__).resolve().parent / "intelligence" / "contenders" / "registry.yaml"


@pytest.mark.skipif(not _REAL_REGISTRY_PATH.is_file(), reason="registry.yaml not yet generated")
def test_real_registry_validates_clean():
    result = crv.validate_registry_file(_REAL_REGISTRY_PATH)
    assert result.valid, result.errors


@pytest.mark.skipif(not _REAL_REGISTRY_PATH.is_file(), reason="registry.yaml not yet generated")
def test_real_registry_has_no_brk_dash_b_duplicate_row():
    data = yaml.safe_load(_REAL_REGISTRY_PATH.read_text())
    symbols = {e["canonical_symbol"] for e in data["entries"]}
    assert "BRK.B" in symbols
    assert "BRK-B" not in symbols


@pytest.mark.skipif(not _REAL_REGISTRY_PATH.is_file(), reason="registry.yaml not yet generated")
def test_real_registry_worked_cases():
    data = yaml.safe_load(_REAL_REGISTRY_PATH.read_text())
    by = {e["canonical_symbol"]: e for e in data["entries"]}

    for sym in ("RKLB", "TSLA"):
        assert by[sym]["primary_disposition"] == "insufficient_evidence"
        assert by[sym]["secondary_flags"]["has_current_gate"] is True
        assert by[sym]["secondary_flags"]["has_prior_deferral_superseded"] is True
        assert by[sym]["secondary_flags"]["current_target"] is True

    for sym in ("GNRC", "RTX"):
        assert by[sym]["secondary_flags"]["has_current_gate"] is False
        assert by[sym]["secondary_flags"]["has_prior_deferral_superseded"] is True

    assert by["QQQ"]["primary_disposition"] == "benchmark_or_index"
    assert by["CASH"]["primary_disposition"] == "synthetic_or_test_fixture"
    assert by["RESERVE"]["primary_disposition"] == "synthetic_or_test_fixture"
    assert by["SNDK"]["primary_disposition"] == "requires_research"
    assert by["WDC"]["primary_disposition"] != "stale_or_superseded"


# ── static source guarantees ─────────────────────────────────────────────

def test_module_source_contains_no_write_mode_file_opens():
    """The VALIDATOR never writes — mirrors relationship_validator.py's and
    intelligence_validator.py's identical guarantee. (The separate generator
    module does write its own output file and is not covered by this test.)"""
    with open(crv.__file__) as f:
        source = f.read()
    tree = ast.parse(source)
    write_modes = {"w", "a", "x", "w+", "a+", "r+", "wb", "ab", "xb"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "attr", None) or getattr(func, "id", None)
            if name == "open":
                for arg in list(node.args)[1:2] + node.keywords:
                    value = arg.value if isinstance(arg, ast.keyword) else arg
                    if isinstance(value, ast.Constant) and value.value in write_modes:
                        pytest.fail(f"found a write-mode open() call: {ast.dump(node)}")
            if name in ("mkdir", "makedirs"):
                pytest.fail(f"found a directory-creation call: {ast.dump(node)}")


def _imported_names(path: str) -> set[str]:
    with open(path) as f:
        tree = ast.parse(f.read())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_validator_imports_no_allocator_margin_or_brokerage_code():
    imported = _imported_names(crv.__file__)
    for forbidden in ("allocate", "margin_state", "alpaca_client", "target_variants"):
        assert forbidden not in imported


def test_allocate_does_not_import_contender_registry_validator():
    imported = _imported_names("allocate.py")
    assert "contender_registry_validator" not in imported


def test_margin_state_does_not_import_contender_registry_validator():
    imported = _imported_names("margin_state.py")
    assert "contender_registry_validator" not in imported
